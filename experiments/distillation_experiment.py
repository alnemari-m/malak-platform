#!/usr/bin/env python3
"""
Knowledge Distillation Experiment for Malak Platform
Teacher: MobileNetV2 (pretrained on CIFAR-10)
Student: 0.5x-width MobileNetV2
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
from malak.compression import KnowledgeDistiller
from malak.quantization.ptq import evaluate_quantized, model_size_mb


DEVICE = torch.device("cpu")
RESULTS_DIR = Path("experiment_results/distillation")
RESULTS_DIR.mkdir(parents=True, exist_ok=True)
TEACHER_PATH = Path("experiment_results/best_model.pth")


def create_mobilenetv2(num_classes=10, width_mult=1.0):
    """Create MobileNetV2 adapted for CIFAR-10."""
    model = torchvision.models.mobilenet_v2(
        weights=None, num_classes=num_classes, width_mult=width_mult
    )
    # Adapt first conv for 32x32 input
    in_ch = model.features[0][0].out_channels
    model.features[0][0] = nn.Conv2d(3, in_ch, kernel_size=3, stride=1, padding=1, bias=False)
    return model


def main():
    print("=" * 80)
    print("KNOWLEDGE DISTILLATION EXPERIMENT FOR MALAK PLATFORM")
    print("=" * 80)

    train_loader, test_loader, _, _ = get_cifar10(batch_size=128)

    # ── Teacher ───────────────────────────────────────────────
    print("\nLoading teacher (MobileNetV2 1.0x)...")
    teacher = create_mobilenetv2(width_mult=1.0)
    teacher_params = sum(p.numel() for p in teacher.parameters())

    if TEACHER_PATH.exists():
        teacher.load_state_dict(torch.load(TEACHER_PATH, map_location=DEVICE))
        print(f"  Loaded from {TEACHER_PATH}")
    else:
        print("  WARNING: No pretrained teacher found. Training from scratch (30 epochs)...")
        t = Trainer(teacher, device=DEVICE, lr=0.01, optimizer_type="sgd")
        t.train(train_loader, test_loader, epochs=30, save_dir=str(RESULTS_DIR / "teacher"))
        teacher.load_state_dict(
            torch.load(RESULTS_DIR / "teacher" / "best_model.pth", map_location=DEVICE)
        )

    teacher_acc, _ = evaluate_quantized(teacher, test_loader)
    teacher_size = model_size_mb(teacher)
    print(f"  Teacher: Acc={teacher_acc:.2f}%, Params={teacher_params:,}, Size={teacher_size:.2f}MB")

    # ── Student (0.5x width) ─────────────────────────────────
    print("\nCreating student (MobileNetV2 0.5x)...")
    student = create_mobilenetv2(width_mult=0.5)
    student_params = sum(p.numel() for p in student.parameters())
    student_size_init = model_size_mb(student)
    print(f"  Student: Params={student_params:,}, Size={student_size_init:.2f}MB")

    # ── Student trained alone (baseline) ─────────────────────
    print("\nTraining student WITHOUT distillation (baseline, 30 epochs)...")
    student_baseline = create_mobilenetv2(width_mult=0.5)
    t = Trainer(student_baseline, device=DEVICE, lr=0.01, optimizer_type="sgd")
    baseline_result = t.train(
        train_loader, test_loader, epochs=30,
        save_dir=str(RESULTS_DIR / "student_baseline")
    )
    student_baseline.load_state_dict(
        torch.load(RESULTS_DIR / "student_baseline" / "best_model.pth", map_location=DEVICE)
    )
    baseline_acc, _ = evaluate_quantized(student_baseline, test_loader)
    print(f"  Student baseline: Acc={baseline_acc:.2f}%")

    # ── Distillation ─────────────────────────────────────────
    print("\nTraining student WITH distillation (30 epochs, T=4, alpha=0.7)...")
    distiller = KnowledgeDistiller(
        teacher=teacher, student=student,
        temperature=4.0, alpha=0.7
    )
    distill_result = distiller.train(
        train_loader, test_loader,
        epochs=30, lr=0.001, device=DEVICE
    )

    distill_acc, distill_lat = evaluate_quantized(distiller.student, test_loader)
    distill_size = model_size_mb(distiller.student)
    print(f"  Distilled student: Acc={distill_acc:.2f}%")
    print(f"  Improvement over baseline: {distill_acc - baseline_acc:+.2f}%")

    # ── Save results ─────────────────────────────────────────
    results = {
        "teacher": {
            "architecture": "MobileNetV2_1.0x",
            "parameters": teacher_params,
            "accuracy": teacher_acc,
            "model_size_mb": teacher_size,
        },
        "student_baseline": {
            "architecture": "MobileNetV2_0.5x",
            "parameters": student_params,
            "accuracy": baseline_acc,
            "model_size_mb": student_size_init,
            "training": "standard",
        },
        "student_distilled": {
            "architecture": "MobileNetV2_0.5x",
            "parameters": student_params,
            "accuracy": distill_acc,
            "latency_ms": distill_lat,
            "model_size_mb": distill_size,
            "training": "knowledge_distillation",
            "temperature": 4.0,
            "alpha": 0.7,
            "improvement_over_baseline": distill_acc - baseline_acc,
        },
    }

    torch.save(distiller.student.state_dict(), RESULTS_DIR / "student_distilled.pth")

    with open(RESULTS_DIR / "distillation_results.json", "w") as f:
        json.dump(results, f, indent=2)

    print(f"\nResults saved to {RESULTS_DIR}/distillation_results.json")


if __name__ == "__main__":
    main()
