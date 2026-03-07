"""Smoke tests for malak.monitoring module."""

import torch
import torch.nn as nn
from malak.monitoring import LayerProfiler


def test_layer_profiler():
    model = nn.Sequential(
        nn.Conv2d(3, 8, 3, padding=1),
        nn.ReLU(),
        nn.Flatten(),
        nn.Linear(8 * 4 * 4, 10),
    )
    profiler = LayerProfiler(model)
    dummy = torch.randn(1, 3, 4, 4)
    profiler.run(dummy, iterations=5)
    report = profiler.report()
    assert len(report) > 0
    assert all("layer" in r and "mean_ms" in r for r in report)
