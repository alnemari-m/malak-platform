"""Smoke tests for malak.compression.pruning module."""

import torch
import torch.nn as nn
from malak.compression import MagnitudePruner, StructuredPruner


def _conv_model():
    return nn.Sequential(
        nn.Conv2d(3, 8, 3, padding=1),
        nn.ReLU(),
        nn.Flatten(),
        nn.Linear(8 * 4 * 4, 10),
    )


def test_magnitude_pruning():
    model = _conv_model()
    pruner = MagnitudePruner()
    model = pruner.prune(model, amount=0.5)
    # Model should still work
    x = torch.randn(1, 3, 4, 4)
    out = model(x)
    assert out.shape == (1, 10)

    model = pruner.remove_masks(model)
    nonzero, total, sparsity = pruner.sparsity(model)
    assert sparsity > 0.3  # Should be close to 0.5


def test_structured_pruning():
    model = _conv_model()
    pruner = StructuredPruner()
    model = pruner.prune(model, amount=0.3)
    x = torch.randn(1, 3, 4, 4)
    out = model(x)
    assert out.shape == (1, 10)
