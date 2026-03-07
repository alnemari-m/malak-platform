"""Model loading and inference benchmarking."""

import torch
import time
import os
from pathlib import Path


class InferenceBenchmark:
    """Benchmark a model's latency and throughput.

    Args:
        model: PyTorch model.
        device: torch.device (quantized models must use CPU).
    """

    def __init__(self, model, device=None):
        self.device = device or torch.device("cpu")
        self.model = model.to(self.device).eval()

    def measure_latency(self, input_shape=(1, 3, 32, 32), warmup=10, iterations=100):
        """Measure per-sample inference latency.

        Returns:
            dict with mean_ms, std_ms, min_ms, max_ms.
        """
        dummy = torch.randn(*input_shape).to(self.device)

        with torch.no_grad():
            for _ in range(warmup):
                self.model(dummy)

        latencies = []
        with torch.no_grad():
            for _ in range(iterations):
                if self.device.type == "cuda":
                    torch.cuda.synchronize()
                start = time.time()
                self.model(dummy)
                if self.device.type == "cuda":
                    torch.cuda.synchronize()
                latencies.append((time.time() - start) * 1000)

        import statistics

        return {
            "mean_ms": statistics.mean(latencies),
            "std_ms": statistics.stdev(latencies) if len(latencies) > 1 else 0.0,
            "min_ms": min(latencies),
            "max_ms": max(latencies),
        }

    def measure_throughput(self, input_shape=(1, 3, 32, 32), duration_s=5.0):
        """Measure throughput (images per second).

        Returns:
            dict with images_per_second and total_images.
        """
        dummy = torch.randn(*input_shape).to(self.device)
        count = 0
        start = time.time()

        with torch.no_grad():
            while time.time() - start < duration_s:
                self.model(dummy)
                count += 1

        elapsed = time.time() - start
        return {
            "images_per_second": count / elapsed,
            "total_images": count,
            "duration_s": elapsed,
        }

    @staticmethod
    def model_size_mb(model, tmp_path="/tmp/_malak_bench_model.pth"):
        """Get serialized model size in MB."""
        torch.save(model.state_dict(), tmp_path)
        size = os.path.getsize(tmp_path) / (1024 * 1024)
        Path(tmp_path).unlink(missing_ok=True)
        return size
