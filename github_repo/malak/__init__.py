"""
Malak Platform: End-to-End Framework for Edge AI Deployment

A unified toolchain for deploying deep neural networks on resource-constrained
edge devices, integrating training, compression, compilation, and runtime.
"""

__version__ = "0.1.0"
__author__ = "Mohammed Alnemari"
__license__ = "MIT"

# Core modules
from . import training
from . import quantization
from . import compiler
from . import runtime

__all__ = [
    "training",
    "quantization",
    "compiler",
    "runtime",
]
