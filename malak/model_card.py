"""YAML model card loader and generator."""

from pathlib import Path


def load_model_card(path):
    """Load a YAML model card.

    Returns:
        dict with model card fields.
    """
    try:
        import yaml
    except ImportError:
        raise ImportError("PyYAML is required: pip install pyyaml")

    with open(path, "r") as f:
        card = yaml.safe_load(f)
    return card


def generate_model_card(
    model_name,
    architecture,
    dataset,
    accuracy,
    model_size_mb,
    quantization=None,
    description="",
    output_path=None,
):
    """Generate a YAML model card.

    Returns:
        dict representing the model card.
    """
    card = {
        "model_name": model_name,
        "architecture": architecture,
        "dataset": dataset,
        "metrics": {
            "top1_accuracy": accuracy,
            "model_size_mb": model_size_mb,
        },
        "quantization": quantization,
        "description": description,
        "framework": "PyTorch",
        "license": "MIT",
    }

    if output_path:
        try:
            import yaml

            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, "w") as f:
                yaml.dump(card, f, default_flow_style=False, sort_keys=False)
            print(f"Model card saved to {output_path}")
        except ImportError:
            print("Warning: PyYAML not installed; cannot write YAML file.")

    return card
