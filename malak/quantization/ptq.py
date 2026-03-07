"""Post-Training Quantization: dynamic and static."""

import torch
import torch.nn as nn
import time
import os
from pathlib import Path


class DynamicPTQ:
    """Dynamic INT8 post-training quantization.

    Quantizes weights statically and activations dynamically at runtime.
    No calibration data required.
    """

    def quantize(self, model, dtype=torch.qint8):
        """Apply dynamic quantization to Linear and Conv2d layers.

        Args:
            model: FP32 PyTorch model (must be on CPU).
            dtype: Quantization dtype (default: torch.qint8).

        Returns:
            Quantized model.
        """
        model = model.cpu().eval()
        quantized = torch.quantization.quantize_dynamic(
            model, {nn.Linear, nn.Conv2d}, dtype=dtype
        )
        return quantized


class StaticPTQ:
    """Static INT8 post-training quantization.

    Quantizes both weights and activations using calibration data.
    Achieves better compression (~4x) than dynamic quantization.
    """

    def quantize(self, model, calibration_loader, backend="fbgemm"):
        """Apply static quantization with calibration.

        Args:
            model: FP32 PyTorch model (must be on CPU and support
                   torch.quantization.prepare).
            calibration_loader: DataLoader for calibration.
            backend: Quantization backend ('fbgemm' for x86, 'qnnpack' for ARM).

        Returns:
            Quantized model.
        """
        model = model.cpu().eval()
        model.qconfig = torch.quantization.get_default_qconfig(backend)
        model_prepared = torch.quantization.prepare(model)

        # Calibrate with real data
        with torch.no_grad():
            for images, _ in calibration_loader:
                model_prepared(images.cpu())

        quantized = torch.quantization.convert(model_prepared)
        return quantized


def evaluate_quantized(model, test_loader, device="cpu"):
    """Evaluate a quantized model's accuracy and latency.

    Returns:
        (accuracy_percent, avg_latency_ms)
    """
    model.eval()
    correct = 0
    total = 0
    latencies = []

    with torch.no_grad():
        for images, labels in test_loader:
            images, labels = images.to(device), labels.to(device)
            start = time.time()
            outputs = model(images)
            elapsed = time.time() - start
            latencies.append(elapsed / images.size(0) * 1000)

            _, predicted = outputs.max(1)
            total += labels.size(0)
            correct += predicted.eq(labels).sum().item()

    accuracy = 100.0 * correct / total
    avg_latency = sum(latencies) / len(latencies) if latencies else 0.0
    return accuracy, avg_latency


def model_size_mb(model, tmp_path="/tmp/_malak_tmp_model.pth"):
    """Get serialized model size in MB."""
    torch.save(model.state_dict(), tmp_path)
    size = os.path.getsize(tmp_path) / (1024 * 1024)
    Path(tmp_path).unlink(missing_ok=True)
    return size
