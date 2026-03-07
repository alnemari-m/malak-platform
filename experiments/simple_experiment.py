#!/usr/bin/env python3
"""
Simple Benchmark Experiment for Malak Platform Paper
Trains MobileNetV2 on CIFAR-10 and measures:
  - FP32 baseline
  - Dynamic INT8 PTQ
  - Real Quantization-Aware Training (QAT)

All results are measured, not hardcoded.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import torch
import torch.nn as nn
import torchvision
import json
from pathlib import Path

from malak.training import Trainer, get_cifar10
from malak.quantization import DynamicPTQ, QAT
from malak.quantization.ptq import evaluate_quantized, model_size_mb

# ── Configuration ──────────────────────────────────────────────
BATCH_SIZE = 128
EPOCHS_FP32 = 15
EPOCHS_QAT = 5
LEARNING_RATE = 0.01
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
OUTPUT_DIR = Path("./experiment_results")


def main():
    OUTPUT_DIR.mkdir(exist_ok=True)

    print("=" * 70)
    print("MALAK PLATFORM - SIMPLE BENCHMARK EXPERIMENT")
    print(f"Device: {DEVICE}")
    print("=" * 70)

    # ── Data ───────────────────────────────────────────────────
    train_loader, test_loader, train_ds, test_ds = get_cifar10(
        batch_size=BATCH_SIZE
    )
    print(f"CIFAR-10: {len(train_ds)} train / {len(test_ds)} test")

    # ── Model ──────────────────────────────────────────────────
    model = torchvision.models.mobilenet_v2(weights=None, num_classes=10)
    model.features[0][0] = nn.Conv2d(3, 32, kernel_size=3, stride=1, padding=1, bias=False)

    total_params = sum(p.numel() for p in model.parameters())
    print(f"MobileNetV2 (CIFAR-10): {total_params:,} parameters")

    # ── Train FP32 baseline ───────────────────────────────────
    print("\n" + "=" * 70)
    print("PHASE 1: TRAINING FP32 BASELINE")
    print("=" * 70)

    trainer = Trainer(
        model, device=DEVICE, lr=LEARNING_RATE,
        optimizer_type="sgd", scheduler_type="cosine"
    )
    trainer.train(
        train_loader, test_loader, epochs=EPOCHS_FP32, save_dir=str(OUTPUT_DIR)
    )

    # Load best model
    model.load_state_dict(torch.load(OUTPUT_DIR / "best_model.pth", map_location=DEVICE))
    model = model.to(DEVICE)

    fp32_accuracy, fp32_latency = trainer.evaluate(test_loader)
    fp32_size = model_size_mb(model)

    print(f"\nFP32 Results:")
    print(f"  Accuracy:  {fp32_accuracy:.2f}%")
    print(f"  Latency:   {fp32_latency:.3f} ms/image")
    print(f"  Size:      {fp32_size:.2f} MB")

    # ── Dynamic INT8 PTQ ──────────────────────────────────────
    print("\n" + "=" * 70)
    print("PHASE 2: DYNAMIC INT8 POST-TRAINING QUANTIZATION")
    print("=" * 70)

    dptq = DynamicPTQ()
    model_dptq = dptq.quantize(model)

    dptq_accuracy, dptq_latency = evaluate_quantized(model_dptq, test_loader)
    dptq_size = model_size_mb(model_dptq)

    print(f"\nDynamic PTQ Results:")
    print(f"  Accuracy:  {dptq_accuracy:.2f}% (drop: {fp32_accuracy - dptq_accuracy:.2f}%)")
    print(f"  Latency:   {dptq_latency:.3f} ms/image")
    print(f"  Size:      {dptq_size:.2f} MB (compression: {fp32_size/dptq_size:.2f}x)")

    # ── Real QAT ──────────────────────────────────────────────
    print("\n" + "=" * 70)
    print("PHASE 3: QUANTIZATION-AWARE TRAINING (REAL)")
    print("=" * 70)

    # Use quantization-ready MobileNetV2 from torchvision
    qat_model = torchvision.models.quantization.mobilenet_v2(
        weights=None, num_classes=10, quantize=False
    )
    qat_model.features[0][0] = nn.Conv2d(3, 32, kernel_size=3, stride=1, padding=1, bias=False)

    # Load FP32 weights (best-effort; architecture may differ slightly)
    try:
        fp32_state = torch.load(OUTPUT_DIR / "best_model.pth", map_location="cpu")
        qat_model.load_state_dict(fp32_state, strict=False)
        print("Loaded FP32 weights into QAT model (strict=False)")
    except Exception as e:
        print(f"Could not load FP32 weights: {e}")
        print("Training QAT model from scratch")

    qat = QAT()
    qat_model = qat.prepare(qat_model, backend="fbgemm")
    qat_model = qat.train(
        qat_model, train_loader, test_loader,
        epochs=EPOCHS_QAT, lr=0.001
    )
    qat_quantized = qat.convert(qat_model)

    qat_accuracy, qat_latency = evaluate_quantized(qat_quantized, test_loader)
    qat_size = model_size_mb(qat_quantized)

    print(f"\nQAT Results:")
    print(f"  Accuracy:  {qat_accuracy:.2f}% (drop: {fp32_accuracy - qat_accuracy:.2f}%)")
    print(f"  Latency:   {qat_latency:.3f} ms/image")
    print(f"  Size:      {qat_size:.2f} MB (compression: {fp32_size/qat_size:.2f}x)")

    # ── Save results ──────────────────────────────────────────
    print("\n" + "=" * 70)
    print("SAVING RESULTS")
    print("=" * 70)

    results = {
        "dataset": {
            "name": "CIFAR-10",
            "train_size": len(train_ds),
            "test_size": len(test_ds),
            "classes": 10,
            "resolution": "32x32 RGB",
        },
        "model": {
            "architecture": "MobileNetV2",
            "parameters": total_params,
            "fp32_size_mb": fp32_size,
        },
        "fp32": {
            "accuracy": fp32_accuracy,
            "latency_ms": fp32_latency,
            "model_size_mb": fp32_size,
        },
        "dynamic_ptq": {
            "accuracy": dptq_accuracy,
            "latency_ms": dptq_latency,
            "model_size_mb": dptq_size,
            "accuracy_drop": fp32_accuracy - dptq_accuracy,
            "compression_ratio": fp32_size / dptq_size,
        },
        "qat": {
            "accuracy": qat_accuracy,
            "latency_ms": qat_latency,
            "model_size_mb": qat_size,
            "accuracy_drop": fp32_accuracy - qat_accuracy,
            "compression_ratio": fp32_size / qat_size,
        },
    }

    with open(OUTPUT_DIR / "results.json", "w") as f:
        json.dump(results, f, indent=2)

    # Save quantized models
    torch.save(model_dptq.state_dict(), OUTPUT_DIR / "model_dynamic_ptq.pth")
    torch.save(qat_quantized.state_dict(), OUTPUT_DIR / "model_qat.pth")

    print(f"\nResults saved to {OUTPUT_DIR}/results.json")
    print("Experiment complete.")


if __name__ == "__main__":
    main()
