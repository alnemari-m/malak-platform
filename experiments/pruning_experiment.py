#!/usr/bin/env python3
"""
Pruning Experiment for Malak Platform
Tests magnitude + structured pruning on MobileNetV2 (CIFAR-10)
using malak.compression API.

Fixes the import bug from the original (MobileNetV2_CIFAR10 did not exist).
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import torch
import torch.nn as nn
import torchvision
import json
from pathlib import Path

from malak.training import get_cifar10
from malak.compression.pruning import MagnitudePruner, StructuredPruner, fine_tune
from malak.quantization.ptq import evaluate_quantized, model_size_mb




def create_mobilenetv2(num_classes=10):
    """Create a MobileNetV2 adapted for CIFAR-10."""
    model = torchvision.models.mobilenet_v2(weights=None, num_classes=num_classes)
    model.features[0][0] = nn.Conv2d(3, 32, kernel_size=3, stride=1, padding=1, bias=False)
    return model


def main():
    DEVICE = torch.device("cpu")
    RESULTS_DIR = Path("experiment_results/pruning")
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    FP32_MODEL_PATH = Path("experiment_results/best_model.pth")

    print("=" * 80)
    print("PRUNING EXPERIMENT FOR MALAK PLATFORM")
    print("=" * 80)

    train_loader, test_loader, _, _ = get_cifar10(batch_size=128)

    # Load baseline
    print("\nLoading baseline FP32 model...")
    baseline = create_mobilenetv2()
    if FP32_MODEL_PATH.exists():
        baseline.load_state_dict(torch.load(FP32_MODEL_PATH, map_location=DEVICE))
        print(f"  Loaded from {FP32_MODEL_PATH}")
    else:
        print("  WARNING: No pretrained model found. Using random init.")
        print("  Run simple_experiment.py first for accurate results.")

    baseline = baseline.to(DEVICE)
    baseline_acc, baseline_lat = evaluate_quantized(baseline, test_loader)
    baseline_size = model_size_mb(baseline)
    params_total = sum(p.numel() for p in baseline.parameters())
    print(f"  Baseline: Acc={baseline_acc:.2f}%, Size={baseline_size:.2f}MB, Params={params_total:,}")

    all_results = {
        "baseline": {
            "accuracy": baseline_acc,
            "latency_ms": baseline_lat,
            "model_size_mb": baseline_size,
            "parameters": params_total,
        }
    }

    # ── Magnitude Pruning ─────────────────────────────────────
    print("\n" + "=" * 80)
    print("MAGNITUDE PRUNING")
    print("=" * 80)

    mag_pruner = MagnitudePruner()

    for sparsity in [0.3, 0.5, 0.7]:
        print(f"\n--- Target sparsity: {sparsity*100:.0f}% ---")
        model = create_mobilenetv2()
        if FP32_MODEL_PATH.exists():
            model.load_state_dict(torch.load(FP32_MODEL_PATH, map_location=DEVICE))
        model = model.to(DEVICE)

        model = mag_pruner.prune(model, amount=sparsity)

        acc_before, _ = evaluate_quantized(model, test_loader)
        print(f"  Before fine-tune: {acc_before:.2f}%")

        print("  Fine-tuning for 3 epochs...")
        model = fine_tune(model, train_loader, DEVICE, epochs=3, lr=0.001)

        model = mag_pruner.remove_masks(model)
        nonzero, total, actual_sparsity = mag_pruner.sparsity(model)

        acc_after, lat_after = evaluate_quantized(model, test_loader)
        size_after = model_size_mb(model)

        print(f"  After fine-tune:  Acc={acc_after:.2f}%, Sparsity={actual_sparsity*100:.1f}%")
        print(f"  Size={size_after:.2f}MB, Drop={baseline_acc - acc_after:.2f}%")

        key = f"magnitude_{int(sparsity*100)}"
        all_results[key] = {
            "method": "magnitude_pruning",
            "target_sparsity": sparsity,
            "actual_sparsity": actual_sparsity,
            "accuracy_before_finetune": acc_before,
            "accuracy_after_finetune": acc_after,
            "accuracy_drop": baseline_acc - acc_after,
            "latency_ms": lat_after,
            "parameters_nonzero": nonzero,
            "parameters_total": total,
            "model_size_mb": size_after,
        }

        torch.save(model.state_dict(), RESULTS_DIR / f"model_{key}.pth")

    # ── Structured Pruning ────────────────────────────────────
    print("\n" + "=" * 80)
    print("STRUCTURED PRUNING")
    print("=" * 80)

    struct_pruner = StructuredPruner()

    for sparsity in [0.3, 0.5]:
        print(f"\n--- Target sparsity: {sparsity*100:.0f}% ---")
        model = create_mobilenetv2()
        if FP32_MODEL_PATH.exists():
            model.load_state_dict(torch.load(FP32_MODEL_PATH, map_location=DEVICE))
        model = model.to(DEVICE)

        model = struct_pruner.prune(model, amount=sparsity)

        acc_before, _ = evaluate_quantized(model, test_loader)
        print(f"  Before fine-tune: {acc_before:.2f}%")

        print("  Fine-tuning for 3 epochs...")
        model = fine_tune(model, train_loader, DEVICE, epochs=3, lr=0.001)

        model = struct_pruner.remove_masks(model)
        nonzero, total, actual_sparsity = struct_pruner.sparsity(model)

        acc_after, lat_after = evaluate_quantized(model, test_loader)
        size_after = model_size_mb(model)

        print(f"  After fine-tune:  Acc={acc_after:.2f}%, Sparsity={actual_sparsity*100:.1f}%")

        key = f"structured_{int(sparsity*100)}"
        all_results[key] = {
            "method": "structured_pruning",
            "target_sparsity": sparsity,
            "actual_sparsity": actual_sparsity,
            "accuracy_before_finetune": acc_before,
            "accuracy_after_finetune": acc_after,
            "accuracy_drop": baseline_acc - acc_after,
            "latency_ms": lat_after,
            "parameters_nonzero": nonzero,
            "parameters_total": total,
            "model_size_mb": size_after,
        }

        torch.save(model.state_dict(), RESULTS_DIR / f"model_{key}.pth")

    # ── Save ──────────────────────────────────────────────────
    with open(RESULTS_DIR / "pruning_results.json", "w") as f:
        json.dump(all_results, f, indent=2)

    print(f"\n{'=' * 80}")
    print("SUMMARY")
    print("=" * 80)
    print(f"{'Method':<22} {'Sparsity':<10} {'Accuracy':<10} {'Drop':<8}")
    print("-" * 55)
    print(f"{'Baseline':<22} {'0%':<10} {baseline_acc:>6.2f}%   {'-':<8}")
    for k, r in all_results.items():
        if k == "baseline":
            continue
        print(
            f"{r['method']:<22} {r['actual_sparsity']*100:>5.1f}%    "
            f"{r['accuracy_after_finetune']:>6.2f}%   "
            f"{r['accuracy_drop']:>5.2f}%"
        )

    print(f"\nResults saved to {RESULTS_DIR}/pruning_results.json")


if __name__ == "__main__":
    main()
