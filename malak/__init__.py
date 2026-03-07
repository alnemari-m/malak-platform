"""
Malak: A Python toolkit for edge AI model optimization.

Provides training, quantization, pruning, distillation,
ONNX export, inference benchmarking, and monitoring utilities.
"""

__version__ = "0.1.0"
__author__ = "Mohammed Alnemari"
__license__ = "MIT"

from . import training
from . import quantization
from . import compression
from . import compiler
from . import runtime
from . import monitoring
