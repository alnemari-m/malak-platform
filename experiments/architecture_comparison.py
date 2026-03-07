#!/usr/bin/env python3
"""
Architecture Comparison Experiment for Malak Platform
Tests ResNet18 and EfficientNet-B0 on CIFAR-10 with REAL quantization.

Replaces the old placeholder (int8_acc = fp32_acc) with actual
dynamic PTQ quantization.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import torch
import torch.nn as nn
from torchvision import models
import json
import time
from pathlib import Path

from malak.training import Trainer, get_cifar10
from malak.quantization import DynamicPTQ
from malak.quantization.ptq import evaluate_quantized, model_size_mb


class ResNet18_CIFAR10(nn.Module):
    """ResNet18 adapted for CIFAR-10 (32x32 images)."""
    def __init__(self, num_classes=10):
        super().__init__()
        self.model = models.resnet18(weights=None)
        self.model.conv1 = nn.Conv2d(3, 64, kernel_size=3, stride=1, padding=1, bias=False)
        self.model.maxpool = nn.Identity()
        self.model.fc = nn.Linear(512, num_classes)

    def forward(self, x):
        return self.model(x)


class EfficientNetB0_CIFAR10(nn.Module):
    """EfficientNet-B0 adapted for CIFAR-10."""
    def __init__(self, num_classes=10):
        super().__init__()
        self.model = models.efficientnet_b0(weights=None)
        self.model.classifier[1] = nn.Linear(
            self.model.classifier[1].in_features, num_classes
        )

    def forward(self, x):
        return self.model(x)


ARCHITECTURES = {
    "ResNet18": ResNet18_CIFAR10,
    "EfficientNet-B0": EfficientNetB0_CIFAR10,
}

def main():
    DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    EPOCHS = 15
    BATCH_SIZE = 128
    RESULTS_DIR = Path("experiment_results/architectures")
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    print("=" * 80)
    print("ARCHITECTURE COMPARISON FOR MALAK PLATFORM")
    print(f"Device: {DEVICE}")
    print("=" * 80)

    train_loader, test_loader, _, _ = get_cifar10(batch_size=BATCH_SIZE)
    all_results = {}

    for arch_name, arch_class in ARCHITECTURES.items():
        print(f"\n{'=' * 80}")
        print(f"TESTING: {arch_name}")
        print("=" * 80)

        model = arch_class(num_classes=10)
        params = sum(p.numel() for p in model.parameters())
        print(f"Parameters: {params:,}")

        # ── Train FP32 ────────────────────────────────────────
        print(f"\nTraining {arch_name} for {EPOCHS} epochs...")
        trainer = Trainer(
            model, device=DEVICE, lr=0.01,
            optimizer_type="sgd", scheduler_type="cosine"
        )
        train_result = trainer.train(
            train_loader, test_loader, epochs=EPOCHS,
            save_dir=str(RESULTS_DIR / arch_name.lower().replace("-", ""))
        )

        # Load best model
        best_path = RESULTS_DIR / arch_name.lower().replace("-", "") / "best_model.pth"
        model.load_state_dict(torch.load(best_path, map_location=DEVICE))
        model = model.to(DEVICE)

        fp32_acc, fp32_latency = trainer.evaluate(test_loader)
        fp32_size = model_size_mb(model)

        print(f"\nFP32: Acc={fp32_acc:.2f}%, Lat={fp32_latency:.3f}ms, Size={fp32_size:.2f}MB")

        # ── REAL Dynamic INT8 PTQ ─────────────────────────────
        print(f"\nApplying REAL dynamic INT8 quantization to {arch_name}...")
        dptq = DynamicPTQ()
        model_int8 = dptq.quantize(model)

        int8_acc, int8_latency = evaluate_quantized(model_int8, test_loader)
        int8_size = model_size_mb(model_int8)

        print(f"INT8:  Acc={int8_acc:.2f}%, Lat={int8_latency:.3f}ms, Size={int8_size:.2f}MB")
        print(f"Drop:  {fp32_acc - int8_acc:.2f}%, Compression: {fp32_size/int8_size:.2f}x")

        all_results[arch_name] = {
            "parameters": params,
            "fp32": {
                "accuracy": fp32_acc,
                "latency_ms": fp32_latency,
                "model_size_mb": fp32_size,
            },
            "int8": {
                "accuracy": int8_acc,
                "latency_ms": int8_latency,
                "model_size_mb": int8_size,
                "accuracy_drop": fp32_acc - int8_acc,
                "compression_ratio": fp32_size / int8_size,
            },
        }

    # ── Save results ──────────────────────────────────────────
    with open(RESULTS_DIR / "architecture_comparison.json", "w") as f:
        json.dump(all_results, f, indent=2)

    print(f"\n{'=' * 80}")
    print("SUMMARY")
    print("=" * 80)
    print(f"{'Architecture':<20} {'Params':<12} {'FP32 Acc':<10} {'INT8 Acc':<10} {'Drop':<8} {'Compr.'}")
    print("-" * 80)
    for name, r in all_results.items():
        print(
            f"{name:<20} {r['parameters']:>10,}  "
            f"{r['fp32']['accuracy']:>6.2f}%   "
            f"{r['int8']['accuracy']:>6.2f}%   "
            f"{r['int8']['accuracy_drop']:>5.2f}%  "
            f"{r['int8']['compression_ratio']:>5.2f}x"
        )

    print(f"\nResults saved to {RESULTS_DIR}/architecture_comparison.json")


if __name__ == "__main__":
    main()
