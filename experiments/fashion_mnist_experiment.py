#!/usr/bin/env python3
"""
Fashion-MNIST Experiment for Malak Platform
Tests SimpleCNN with dynamic PTQ using malak API.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import torch
import torch.nn as nn
import json
from pathlib import Path

from malak.training import Trainer, get_fashion_mnist
from malak.quantization import DynamicPTQ
from malak.quantization.ptq import evaluate_quantized, model_size_mb


class SimpleCNN(nn.Module):
    """Simple CNN for Fashion-MNIST."""
    def __init__(self, num_classes=10):
        super().__init__()
        self.features = nn.Sequential(
            nn.Conv2d(1, 32, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2),
            nn.Conv2d(32, 64, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2),
            nn.Conv2d(64, 64, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
        )
        self.classifier = nn.Sequential(
            nn.Linear(64 * 7 * 7, 128),
            nn.ReLU(inplace=True),
            nn.Dropout(0.5),
            nn.Linear(128, num_classes),
        )

    def forward(self, x):
        x = self.features(x)
        x = torch.flatten(x, 1)
        x = self.classifier(x)
        return x


def main():
    DEVICE = torch.device("cpu")
    RESULTS_DIR = Path("experiment_results/fashion_mnist")
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    print("=" * 80)
    print("FASHION-MNIST EXPERIMENT FOR MALAK PLATFORM")
    print("=" * 80)

    train_loader, test_loader, train_ds, test_ds = get_fashion_mnist(batch_size=128)
    print(f"Fashion-MNIST: {len(train_ds)} train / {len(test_ds)} test")

    model = SimpleCNN(num_classes=10)
    params = sum(p.numel() for p in model.parameters())
    print(f"SimpleCNN: {params:,} parameters")

    # Train
    print("\nTraining for 20 epochs...")
    trainer = Trainer(
        model, device=DEVICE, lr=0.001,
        optimizer_type="adam", scheduler_type=None
    )
    train_result = trainer.train(
        train_loader, test_loader, epochs=20, save_dir=str(RESULTS_DIR)
    )

    # Load best
    model.load_state_dict(torch.load(RESULTS_DIR / "best_model.pth", map_location=DEVICE))

    fp32_acc, fp32_latency = trainer.evaluate(test_loader)
    fp32_size = model_size_mb(model)
    print(f"\nFP32: Acc={fp32_acc:.2f}%, Lat={fp32_latency:.3f}ms, Size={fp32_size:.2f}MB")

    # Dynamic PTQ
    print("\nApplying dynamic INT8 quantization...")
    dptq = DynamicPTQ()
    model_int8 = dptq.quantize(model)

    int8_acc, int8_latency = evaluate_quantized(model_int8, test_loader)
    int8_size = model_size_mb(model_int8)
    print(f"INT8:  Acc={int8_acc:.2f}%, Lat={int8_latency:.3f}ms, Size={int8_size:.2f}MB")
    print(f"Drop:  {fp32_acc - int8_acc:.2f}%, Compression: {fp32_size/int8_size:.2f}x")

    results = {
        "dataset": "Fashion-MNIST",
        "model": "SimpleCNN",
        "parameters": params,
        "fp32": {
            "accuracy": fp32_acc,
            "latency_ms": fp32_latency,
            "model_size_mb": fp32_size,
        },
        "int8_ptq": {
            "accuracy": int8_acc,
            "latency_ms": int8_latency,
            "model_size_mb": int8_size,
            "accuracy_drop": fp32_acc - int8_acc,
            "compression_ratio": fp32_size / int8_size,
        },
    }

    with open(RESULTS_DIR / "results.json", "w") as f:
        json.dump(results, f, indent=2)

    print(f"\nResults saved to {RESULTS_DIR}/results.json")


if __name__ == "__main__":
    main()
