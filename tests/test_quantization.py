"""Smoke tests for malak.quantization module."""

import torch
import torch.nn as nn
from malak.quantization import DynamicPTQ
from malak.quantization.ptq import model_size_mb


def _simple_model():
    return nn.Sequential(
        nn.Flatten(),
        nn.Linear(3 * 4 * 4, 32),
        nn.ReLU(),
        nn.Linear(32, 10),
    )


def test_dynamic_ptq():
    model = _simple_model()
    dptq = DynamicPTQ()
    quantized = dptq.quantize(model)
    # Should still produce output
    x = torch.randn(1, 3, 4, 4)
    out = quantized(x)
    assert out.shape == (1, 10)


def test_model_size():
    model = _simple_model()
    size = model_size_mb(model)
    assert size > 0
