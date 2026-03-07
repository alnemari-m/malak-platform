"""Smoke tests for malak.training module."""

import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset
from malak.training import Trainer


def _tiny_model():
    return nn.Sequential(nn.Flatten(), nn.Linear(3 * 4 * 4, 10))


def _tiny_loaders():
    x = torch.randn(32, 3, 4, 4)
    y = torch.randint(0, 10, (32,))
    ds = TensorDataset(x, y)
    loader = DataLoader(ds, batch_size=8)
    return loader, loader


def test_trainer_runs():
    model = _tiny_model()
    train_loader, test_loader = _tiny_loaders()
    trainer = Trainer(model, lr=0.01, optimizer_type="sgd")
    result = trainer.train(train_loader, test_loader, epochs=2)
    assert "best_accuracy" in result
    assert result["best_accuracy"] >= 0


def test_trainer_evaluate():
    model = _tiny_model()
    _, test_loader = _tiny_loaders()
    trainer = Trainer(model, lr=0.01)
    acc, lat = trainer.evaluate(test_loader)
    assert 0 <= acc <= 100
    assert lat >= 0  # may be 0.0 on fast hardware with tiny models
