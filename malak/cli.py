"""``edgeai`` CLI entry point.

Usage::

    edgeai train --dataset cifar10 --model mobilenetv2 --epochs 100
    edgeai quantize --model path/to/model.pth --method ptq-static
    edgeai evaluate --model path/to/model.pth --dataset cifar10
    edgeai export --model path/to/model.pth --format onnx
    edgeai profile --model path/to/model.pth
"""

import argparse
import json
import sys
import torch
import torch.nn as nn
import torchvision


def _get_model(name, num_classes=10):
    """Instantiate a model by name."""
    if name == "mobilenetv2":
        model = torchvision.models.mobilenet_v2(weights=None, num_classes=num_classes)
        model.features[0][0] = nn.Conv2d(
            3, 32, kernel_size=3, stride=1, padding=1, bias=False
        )
        return model
    elif name == "resnet18":
        model = torchvision.models.resnet18(weights=None, num_classes=num_classes)
        model.conv1 = nn.Conv2d(3, 64, kernel_size=3, stride=1, padding=1, bias=False)
        model.maxpool = nn.Identity()
        return model
    else:
        raise ValueError(f"Unknown model: {name}. Supported: mobilenetv2, resnet18")


def cmd_train(args):
    from malak.training import Trainer, get_cifar10, get_fashion_mnist

    if args.dataset == "cifar10":
        train_loader, test_loader, _, _ = get_cifar10(batch_size=args.batch_size)
    elif args.dataset == "fashionmnist":
        train_loader, test_loader, _, _ = get_fashion_mnist(batch_size=args.batch_size)
    else:
        print(f"Unknown dataset: {args.dataset}")
        sys.exit(1)

    model = _get_model(args.model)
    trainer = Trainer(
        model, lr=args.lr, optimizer_type=args.optimizer, scheduler_type="cosine"
    )
    result = trainer.train(
        train_loader, test_loader, epochs=args.epochs, save_dir=args.output
    )
    print(json.dumps({"best_accuracy": result["best_accuracy"]}, indent=2))


def cmd_quantize(args):
    from malak.quantization import DynamicPTQ, StaticPTQ

    state = torch.load(args.model, map_location="cpu", weights_only=True)
    model = _get_model(args.arch)
    model.load_state_dict(state)

    if args.method == "ptq-dynamic":
        q = DynamicPTQ()
        quantized = q.quantize(model)
    elif args.method == "ptq-static":
        from malak.training import get_cifar10

        loader, _, _, _ = get_cifar10(batch_size=64)
        q = StaticPTQ()
        quantized = q.quantize(model, loader, backend=args.backend)
    else:
        print(f"Unknown method: {args.method}")
        sys.exit(1)

    out = args.output or args.model.replace(".pth", f"_{args.method}.pth")
    torch.save(quantized.state_dict(), out)
    print(f"Saved quantized model to {out}")


def cmd_evaluate(args):
    from malak.training import get_cifar10, get_fashion_mnist
    from malak.quantization.ptq import evaluate_quantized

    state = torch.load(args.model, map_location="cpu", weights_only=True)
    model = _get_model(args.arch)
    model.load_state_dict(state)

    if args.dataset == "cifar10":
        _, test_loader, _, _ = get_cifar10(batch_size=128)
    else:
        _, test_loader, _, _ = get_fashion_mnist(batch_size=128)

    acc, lat = evaluate_quantized(model, test_loader)
    print(json.dumps({"accuracy": acc, "latency_ms": lat}, indent=2))


def cmd_export(args):
    from malak.compiler import export_onnx

    state = torch.load(args.model, map_location="cpu", weights_only=True)
    model = _get_model(args.arch)
    model.load_state_dict(state)

    out = args.output or args.model.replace(".pth", ".onnx")
    result = export_onnx(model, out)
    print(json.dumps(result, indent=2))


def cmd_profile(args):
    from malak.monitoring import LayerProfiler

    state = torch.load(args.model, map_location="cpu", weights_only=True)
    model = _get_model(args.arch)
    model.load_state_dict(state)

    profiler = LayerProfiler(model)
    dummy = torch.randn(1, 3, 32, 32)
    profiler.run(dummy, iterations=args.iterations)
    report = profiler.report()

    print(f"\n{'Layer':<50} {'Time (ms)':<12} {'Fraction'}")
    print("-" * 75)
    for entry in report[:20]:
        print(
            f"{entry['layer']:<50} {entry['mean_ms']:>8.4f}    "
            f"{entry['fraction']*100:>5.1f}%"
        )


def main():
    parser = argparse.ArgumentParser(
        prog="edgeai", description="Malak edge AI toolkit CLI"
    )
    sub = parser.add_subparsers(dest="command")

    # train
    p = sub.add_parser("train", help="Train a model")
    p.add_argument("--dataset", default="cifar10", choices=["cifar10", "fashionmnist"])
    p.add_argument("--model", default="mobilenetv2")
    p.add_argument("--epochs", type=int, default=100)
    p.add_argument("--batch-size", type=int, default=128)
    p.add_argument("--lr", type=float, default=0.01)
    p.add_argument("--optimizer", default="sgd", choices=["sgd", "adam"])
    p.add_argument("--output", default="./output")

    # quantize
    p = sub.add_parser("quantize", help="Quantize a model")
    p.add_argument("--model", required=True, help="Path to .pth file")
    p.add_argument("--arch", default="mobilenetv2")
    p.add_argument(
        "--method",
        default="ptq-dynamic",
        choices=["ptq-dynamic", "ptq-static"],
    )
    p.add_argument("--backend", default="fbgemm", choices=["fbgemm", "qnnpack"])
    p.add_argument("--output", default=None)

    # evaluate
    p = sub.add_parser("evaluate", help="Evaluate a model")
    p.add_argument("--model", required=True)
    p.add_argument("--arch", default="mobilenetv2")
    p.add_argument("--dataset", default="cifar10")

    # export
    p = sub.add_parser("export", help="Export model to ONNX")
    p.add_argument("--model", required=True)
    p.add_argument("--arch", default="mobilenetv2")
    p.add_argument("--output", default=None)

    # profile
    p = sub.add_parser("profile", help="Profile per-layer latency")
    p.add_argument("--model", required=True)
    p.add_argument("--arch", default="mobilenetv2")
    p.add_argument("--iterations", type=int, default=50)

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        sys.exit(0)

    cmds = {
        "train": cmd_train,
        "quantize": cmd_quantize,
        "evaluate": cmd_evaluate,
        "export": cmd_export,
        "profile": cmd_profile,
    }
    cmds[args.command](args)


if __name__ == "__main__":
    main()
