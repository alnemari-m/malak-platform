# Malak Platform

**End-to-End Framework for Edge AI Deployment on Resource-Constrained Devices**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.0+-red.svg)](https://pytorch.org/)

## Overview

Malak Platform provides a unified toolchain for deploying deep neural networks on edge devices. It integrates **training**, **compression**, **compilation**, and **runtime** in a single framework, addressing the fragmentation that complicates current edge AI workflows.

### Key Features

- **🔄 End-to-End Pipeline**: From PyTorch training to embedded deployment
- **📦 Model Compression**: INT8/INT4 quantization, pruning, knowledge distillation
- **🔧 Multi-Compiler Support**: TVM, MLIR, XLA backends
- **⚡ Optimized Runtime**: C++ runtime with hardware abstraction
- **🛡️ Production Ready**: Built-in telemetry, drift detection, privacy policies
- **📊 Validated**: CIFAR-10 benchmark achieving 89.28% → 88.78% accuracy (0.5% loss) after INT8 quantization

## Quick Start

### Installation

```bash
# Clone repository
git clone https://github.com/alnemari-m/malak_platform.git
cd malak_platform

# Install dependencies
pip install -r requirements.txt
```

### Run CIFAR-10 Experiment

Reproduce the paper results:

```bash
cd experiments
python simple_experiment.py
```

Expected output:
- **FP32 Baseline**: ~89.28% accuracy
- **INT8 PTQ**: ~89.26% accuracy (-0.02%)
- **INT8 QAT**: ~88.78% accuracy (-0.50%)
- **Inference**: ~0.67 ms/image

See [experiments/README.md](experiments/README.md) for detailed reproduction instructions.

## Architecture

```
┌─────────────────────────────────────────┐
│     Reference Applications              │
├─────────────────────────────────────────┤
│  Python API (Training & Compression)    │
│  - PyTorch integration                  │
│  - Quantization (INT8/INT4)             │
│  - Model optimization                   │
├─────────────────────────────────────────┤
│  EdgeIR (Intermediate Representation)   │
│  - Graph optimization                   │
│  - Hardware-aware compilation           │
├─────────────────────────────────────────┤
│  Multi-Compiler Backend                 │
│  - TVM | MLIR | XLA                     │
├─────────────────────────────────────────┤
│  C++ Runtime                            │
│  - ARM Cortex-M | x86 | RISC-V          │
└─────────────────────────────────────────┘
```

## Performance

**CIFAR-10 Image Classification** (MobileNetV2, 2.2M parameters):

| Configuration | Accuracy | Model Size | Latency (CPU) |
|--------------|----------|------------|---------------|
| FP32 Baseline | 89.28% | 8.76 MB | 0.667 ms |
| INT8 PTQ | 89.26% | 8.73 MB | 0.668 ms |
| INT8 QAT | 88.78% | 8.73 MB | 0.668 ms |

*Minimal accuracy degradation (0.5%) with quantization*

## Repository Structure

```
malak_platform/
├── README.md                 # This file
├── LICENSE                   # MIT License
├── requirements.txt          # Python dependencies
├── setup.py                  # Package installation
│
├── malak/                    # Main platform code
│   ├── training/            # Training utilities
│   ├── quantization/        # Compression techniques
│   ├── compiler/            # Multi-compiler backends
│   └── runtime/             # C++ runtime interface
│
├── experiments/              # Reproducible experiments
│   ├── simple_experiment.py # CIFAR-10 validation
│   └── README.md            # Reproduction guide
│
├── models/                   # Pre-trained models
│   └── README.md
│
├── docs/                     # Documentation
│   ├── installation.md
│   ├── quickstart.md
│   └── api_reference.md
│
└── paper/                    # Paper LaTeX sources
    ├── main_fixed.tex
    └── figures/
```

## Documentation

- **[Installation Guide](docs/installation.md)**: Detailed setup instructions
- **[Quick Start Tutorial](docs/quickstart.md)**: First steps with Malak Platform
- **[API Reference](docs/api_reference.md)**: Complete API documentation
- **[Experiments Guide](experiments/README.md)**: Reproducing paper results

## Use Cases

Malak Platform is designed for:

- 🏥 **Healthcare**: On-device medical imaging analysis
- 🏭 **Industrial IoT**: Predictive maintenance on edge sensors
- 🤖 **Robotics**: Real-time vision and control
- 📱 **Mobile AI**: Privacy-preserving smartphone applications
- 🌐 **Edge Computing**: Distributed intelligence across IoT networks

## Roadmap

### Current (v0.1)
- ✅ PyTorch integration
- ✅ INT8 quantization (dynamic)
- ✅ CIFAR-10 validation
- ✅ CPU runtime

### Near-term (v0.2)
- ⏳ Static INT8 quantization (4× compression)
- ⏳ ARM Cortex-M deployment
- ⏳ Pruning support
- ⏳ ImageNet validation

### Future (v1.0)
- 🔮 INT4 quantization
- 🔮 Hardware accelerator support (NPU, DSP)
- 🔮 Transformer models
- 🔮 Federated learning

## Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

Areas where we need help:
- 🐛 Bug reports and fixes
- 📚 Documentation improvements
- 🧪 Additional benchmarks
- 🔧 New compression techniques
- 💻 Hardware backend support

## Citation

If you use Malak Platform in your research, please cite:

```bibtex
@article{alnemari2026malak,
  title={Malak Platform: An End-to-End Framework for Edge AI Deployment on Resource-Constrained Devices},
  author={Alnemari, Mohammed},
  journal={arXiv preprint},
  year={2026}
}
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

Built on top of excellent open-source projects:
- [PyTorch](https://pytorch.org/) - Deep learning framework
- [TVM](https://tvm.apache.org/) - Tensor compiler
- [MLIR](https://mlir.llvm.org/) - Compiler infrastructure
- [CIFAR-10](https://www.cs.toronto.edu/~kriz/cifar.html) - Dataset for validation

## Contact

- **Author**: Mohammed Alnemari
- **GitHub**: [@alnemari-m](https://github.com/alnemari-m)
- **Issues**: [GitHub Issues](https://github.com/alnemari-m/malak_platform/issues)

## Paper

📄 **Paper**: [Malak Platform: An End-to-End Framework for Edge AI Deployment](paper/)

**Abstract**: Getting deep learning models to run efficiently on resource-constrained devices is challenging. Malak Platform addresses this by providing a unified toolchain that spans training, compression, compilation, and deployment. We validate the platform on CIFAR-10, achieving 89.28% accuracy with only 0.5% degradation after INT8 quantization-aware training.

---

**Status**: 🚀 Active Development | 📊 Research Preview | ⭐ Star us on GitHub!
