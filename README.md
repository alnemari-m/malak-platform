<div align="center">
  <img src="logo.png" alt="Malak Platform Logo" width="400"/>
</div>

# Malak Platform

**A comprehensive Edge AI platform for training, optimizing, and deploying deep neural networks on embedded systems and TinyML devices.**

## Overview

Malak Platform (`malak_edge_ai`) is an end-to-end framework designed to bridge the gap between powerful deep learning models and resource-constrained edge devices. It provides a complete toolchain for developing, compressing, and deploying AI models on microcontrollers, embedded systems, and edge gateways.

## Key Features

- **Multi-Language Architecture**: Combines Python for training/tooling, C++ for efficient runtime, and Mojo for performance-critical kernels
- **Aggressive Compression**: Built-in quantization (INT8/INT4), pruning, and knowledge distillation
- **Hardware Flexibility**: Supports CPU (NEON), CUDA, NPU, and DSP backends
- **Edge-First Design**: Optimized for latency, energy efficiency, and minimal memory footprint
- **Production Ready**: Includes telemetry, monitoring, drift detection, and privacy policies

## Architecture

### Core Components

#### 1. **Apps** - Reference Applications
- **Vision Jellyfish**: Real-time marine life detection and classification
- **Energy Optimization**: Smart energy consumption prediction and optimization
- **Neuro MS**: Medical imaging analysis for Multiple Sclerosis diagnosis

#### 2. **Core** - System Specifications
- **Model Cards**: YAML-based model metadata (task, sizes, latency/energy budgets, calibration ranges)
- **Schemas**: Protobuf/FlatBuffers definitions for features, telemetry, and on-device events
- **Policies**: JSON configurations for privacy, data retention, fallback, and escalation

#### 3. **Python** - Training & Tooling
- **Training**: PyTorch pipelines with knowledge distillation, data augmentation
- **Compression**: Quantization, pruning, ONNX/TFLite export
- **Compilation**: TVM, MLIR, XLA compilation flows with per-target autotuning
- **Serving**: Lightweight gRPC/REST for edge gateways
- **Monitoring**: Drift detection, accuracy canaries, telemetry analysis
- **CLI**: Unified `edgeai` command-line tool for build, quantize, flash, eval, profile

#### 4. **C++** - Embedded Runtime
- **Runtime**: Static graph executor, memory planner, operator registry
- **Kernels**: Optimized INT8/INT4 conv, depthwise, GEMM, activation, pooling
- **Hardware Abstraction**: Pluggable backends for CPU, CUDA, NPU, DSP
- **I/O**: Camera, sensors, ring buffers, zero-copy DMA
- **Telemetry**: Performance counters, energy monitoring, on-device logging

#### 5. **Mojo** - High-Performance Kernels
- **Kernels**: MLIR-friendly quantized matmul/conv microkernels
- **Numerics**: LUT-based quantization, symmetric/asymmetric schemes, fixed-point arithmetic

#### 6. **Tools**
- **Profilers**: Latency, energy, calibration tools, benchmarking
- **Converters**: ONNX, TFLite, PyTorch → EdgeIR

#### 7. **Edge IR** - Intermediate Representation
- Custom IR optimized for edge deployment
- Optimization passes: fusion, constant folding, layout transforms, quantization
- FlatBuffers schema for compact model serialization

## Getting Started

### Prerequisites

```bash
# Python dependencies
pip install -r malak_edge_ai/requirements.txt

# C++ build tools
sudo apt-get install cmake build-essential

# (Optional) Mojo compiler
# Follow Mojo installation guide
```

### Quick Start

```bash
# Clone the repository
git clone https://github.com/alnemari-m/malak_platform.git
cd malak_platform/malak_edge_ai

# Train a model
python apps/vision_jellyfish/main.py --config apps/vision_jellyfish/config.yaml

# Quantize for edge deployment
python python/compression/quantize.py --model model.pth --bits 8

# Convert to EdgeIR
python tools/converters/pytorch_to_edgeir.py --input model.pth --output model.edgeir

# Profile on target device
python tools/profilers/latency_profiler.py --model model.edgeir --device rpi4
```

## Use Cases

- **Smart IoT Devices**: On-device inference for cameras, sensors, wearables
- **Medical Edge AI**: Privacy-preserving diagnostic tools
- **Industrial Monitoring**: Real-time anomaly detection on factory floors
- **Environmental Sensing**: Wildlife monitoring, climate analysis
- **Energy Systems**: Smart grid optimization, consumption forecasting

## Performance Targets

- **Latency**: <50ms inference on Cortex-M7 @ 480MHz
- **Memory**: <512KB flash, <128KB RAM for typical models
- **Energy**: <10mJ per inference on battery-powered devices
- **Accuracy**: <2% degradation vs. full-precision baseline

## Documentation

- [Architecture Overview](malak_edge_ai/docs/architecture.md)
- [API Reference](malak_edge_ai/docs/api_reference.md)
- [Getting Started Guide](malak_edge_ai/docs/getting_started.md)
- [Threat Model](malak_edge_ai/docs/threat_model.md)
- [Latency Budgets](malak_edge_ai/docs/latency_budgets.md)
- [Contributing](malak_edge_ai/docs/contributing.md)

## License

See [LICENSE](LICENSE) for details.

## Acknowledgments

Built for edge AI researchers, embedded systems engineers, and TinyML practitioners who demand production-grade tools for resource-constrained deployment.
