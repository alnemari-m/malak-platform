"""Smoke tests for malak.compiler module."""

import pytest
import torch
import torch.nn as nn
from pathlib import Path
from malak.compiler import export_onnx


def _simple_model():
    return nn.Sequential(
        nn.Flatten(),
        nn.Linear(3 * 4 * 4, 10),
    )


@pytest.mark.skipif(
    not pytest.importorskip("onnx", reason="onnx not installed"),
    reason="onnx not installed",
)
def test_onnx_export(tmp_path):
    model = _simple_model()
    out_path = tmp_path / "test_model.onnx"
    result = export_onnx(model, str(out_path), input_shape=(1, 3, 4, 4))
    assert out_path.exists()
    assert result["output_path"] == str(out_path)
    assert result["size_mb"] > 0
