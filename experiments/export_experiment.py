#!/usr/bin/env python3
"""
ONNX Export Experiment for Malak Platform
Exports FP32 and quantized models to ONNX and reports sizes.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import torch
import torch.nn as nn
import torchvision
import json
from pathlib import Path

from malak.compiler import export_onnx, validate_onnx
from malak.quantization import DynamicPTQ
from malak.quantization.ptq import model_size_mb


RESULTS_DIR = Path("experiment_results/export")
RESULTS_DIR.mkdir(parents=True, exist_ok=True)
FP32_MODEL_PATH = Path("experiment_results/best_model.pth")


def create_mobilenetv2(num_classes=10):
    model = torchvision.models.mobilenet_v2(weights=None, num_classes=num_classes)
    model.features[0][0] = nn.Conv2d(3, 32, kernel_size=3, stride=1, padding=1, bias=False)
    return model


def main():
    print("=" * 80)
    print("ONNX EXPORT EXPERIMENT FOR MALAK PLATFORM")
    print("=" * 80)

    model = create_mobilenetv2()

    if FP32_MODEL_PATH.exists():
        model.load_state_dict(torch.load(FP32_MODEL_PATH, map_location="cpu"))
        print(f"Loaded model from {FP32_MODEL_PATH}")
    else:
        print("WARNING: No pretrained model found. Using random weights.")

    results = {}

    # ── FP32 ONNX export ──────────────────────────────────────
    print("\nExporting FP32 model to ONNX...")
    fp32_result = export_onnx(
        model,
        RESULTS_DIR / "mobilenetv2_fp32.onnx",
        input_shape=(1, 3, 32, 32),
    )
    try:
        validate_onnx(RESULTS_DIR / "mobilenetv2_fp32.onnx")
        fp32_result["valid"] = True
    except Exception:
        fp32_result["valid"] = False

    results["fp32_onnx"] = fp32_result

    # ── Dynamic PTQ export ────────────────────────────────────
    # Note: quantized models may not export cleanly to ONNX
    # depending on PyTorch/ONNX version. Document honestly.
    print("\nExporting dynamic PTQ model to ONNX...")
    dptq = DynamicPTQ()
    model_int8 = dptq.quantize(model)

    try:
        int8_result = export_onnx(
            model_int8,
            RESULTS_DIR / "mobilenetv2_int8_dptq.onnx",
            input_shape=(1, 3, 32, 32),
        )
        try:
            validate_onnx(RESULTS_DIR / "mobilenetv2_int8_dptq.onnx")
            int8_result["valid"] = True
        except Exception:
            int8_result["valid"] = False
        results["int8_dptq_onnx"] = int8_result
    except Exception as e:
        print(f"  INT8 ONNX export failed: {e}")
        print("  This is expected — not all quantized ops have ONNX support.")
        results["int8_dptq_onnx"] = {
            "status": "failed",
            "reason": str(e),
        }

    # ── PyTorch model sizes for comparison ────────────────────
    results["pth_sizes"] = {
        "fp32_mb": model_size_mb(model),
        "int8_dptq_mb": model_size_mb(model_int8),
    }

    with open(RESULTS_DIR / "export_results.json", "w") as f:
        json.dump(results, f, indent=2)

    print(f"\nResults saved to {RESULTS_DIR}/export_results.json")


if __name__ == "__main__":
    main()
