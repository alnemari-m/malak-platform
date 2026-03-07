"""ONNX model export and validation."""

import torch
import os
from pathlib import Path


def export_onnx(
    model,
    output_path,
    input_shape=(1, 3, 32, 32),
    opset_version=13,
    dynamic_axes=None,
):
    """Export a PyTorch model to ONNX format.

    Args:
        model: PyTorch model (must be on CPU for quantized models).
        output_path: Path to save the .onnx file.
        input_shape: Tuple for dummy input shape.
        opset_version: ONNX opset version.
        dynamic_axes: Optional dict for dynamic batch size.

    Returns:
        dict with output_path and file_size_mb.
    """
    model.eval()

    try:
        device = next(model.parameters()).device
    except StopIteration:
        device = torch.device("cpu")

    dummy_input = torch.randn(*input_shape).to(device)

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if dynamic_axes is None:
        dynamic_axes = {"input": {0: "batch"}, "output": {0: "batch"}}

    torch.onnx.export(
        model,
        dummy_input,
        str(output_path),
        opset_version=opset_version,
        input_names=["input"],
        output_names=["output"],
        dynamic_axes=dynamic_axes,
    )

    size_mb = os.path.getsize(output_path) / (1024 * 1024)
    print(f"Exported ONNX model to {output_path} ({size_mb:.2f} MB)")

    return {"output_path": str(output_path), "file_size_mb": size_mb}


def validate_onnx(onnx_path):
    """Validate an ONNX model file.

    Returns:
        True if valid, raises on error.
    """
    try:
        import onnx

        model = onnx.load(str(onnx_path))
        onnx.checker.check_model(model)
        print(f"ONNX model {onnx_path} is valid.")
        return True
    except ImportError:
        print("Warning: onnx package not installed; skipping validation.")
        return True
    except Exception as e:
        print(f"ONNX validation failed: {e}")
        raise
