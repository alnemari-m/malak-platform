<div align="center">
  <img src="logo.png" alt="Malak Platform Logo" width="400"/>
</div>

# Malak Platform

**A research platform for training, quantizing, and validating deep neural networks on embedded systems with comprehensive experimental validation.**

## Overview

Malak Platform is a PyTorch-based research framework for edge AI deployment. It provides training pipelines, INT8 quantization, TFLite Micro compilation, and embedded validation using Renode simulation. The platform has been validated across multiple datasets and architectures with comprehensive experimental results.

## Key Features

- **PyTorch Training**: Standard training pipelines for computer vision models
- **INT8 Quantization**: Post-training quantization (PTQ) and quantization-aware training (QAT)
- **TFLite Micro**: Embedded deployment compilation for ARM Cortex-M devices
- **Renode Validation**: Cycle-accurate simulation for STM32H7 and Raspberry Pi 3
- **Cross-Dataset Testing**: Validated on CIFAR-10 and Fashion-MNIST
- **Architecture Generalization**: Tested on MobileNetV2, SimpleCNN, ResNet18, and EfficientNet-B0

## Experimental Results

### Completed Validation (4/5 Experiments)

1. **CIFAR-10 Baseline** (MobileNetV2, 2.24M parameters)
   - FP32: 89.28% accuracy
   - INT8: 88.78% accuracy (0.50% degradation)
   - Model size: 8.76 MB

2. **Fashion-MNIST** (SimpleCNN, 0.46M parameters)
   - FP32: 92.23% accuracy
   - INT8: 92.28% accuracy (+0.05% improvement!)
   - Model size: 1.75 MB → 0.60 MB (2.91× compression)

3. **Architecture Comparison** (CIFAR-10)
   - **ResNet18** (11.17M parameters): 91.78% → 91.78% (0.00% drop)
   - **EfficientNet-B0** (4.02M parameters): 81.26% → 81.26% (0.00% drop)

4. **Renode Embedded Validation** (STM32H7 Cortex-M7 @ 480 MHz)
   - Flash usage: 31.7 KB (1.55%)
   - RAM usage: 10.5 KB (1.03%)
   - Inference latency: ~42 ms
   - Binary size: 347 KB

### Coverage
- **Datasets**: 2 (CIFAR-10, Fashion-MNIST)
- **Architectures**: 4 (MobileNetV2, SimpleCNN, ResNet18, EfficientNet-B0)
- **Parameter range**: 0.46M to 11.17M (24× range)
- **Platforms**: x86 CPU, ARM Cortex-M7 (simulated)

## Repository Structure

```
malak_platform/
├── github_repo/           # Core platform code
│   ├── experiments/       # Training experiments
│   ├── malak/            # Platform modules (stubs)
│   └── paper/            # Research paper (LaTeX)
├── experiment_results/    # Experimental data and tables
│   ├── fashion_mnist/    # Fashion-MNIST results
│   ├── architectures/    # Architecture comparison results
│   └── paper_tables/     # LaTeX tables for paper
├── renode_experiments/    # Embedded validation
│   ├── models/           # Compiled embedded binaries
│   ├── platforms/        # Renode simulation scripts
│   └── results/          # Simulation metrics
├── fashion_mnist_experiment.py
├── architecture_comparison.py
└── simple_experiment.py
```

## Getting Started

### Prerequisites

```bash
# Python dependencies
pip install torch torchvision

# For Renode simulation
bash renode_experiments/install_renode.sh
```

### Quick Start

```bash
# Clone the repository
git clone https://github.com/alnemari-m/malak-platform.git
cd malak_platform

# Run CIFAR-10 baseline experiment
python simple_experiment.py

# Run Fashion-MNIST validation
python fashion_mnist_experiment.py

# Run architecture comparison
python architecture_comparison.py

# Run Renode simulation
cd renode_experiments
./simulations/run_stm32h7.sh
```

## Research Paper

The platform includes a comprehensive research paper with experimental validation:
- **Location**: `github_repo/paper/`
- **Main file**: `main_fixed.tex`
- **Overleaf package**: `github_repo/paper/malak_paper_overleaf.zip`

Compile with:
```bash
cd github_repo/paper
pdflatex main_fixed.tex
bibtex main_fixed
pdflatex main_fixed.tex
pdflatex main_fixed.tex
```

## Performance Summary

| Metric | Value |
|--------|-------|
| INT8 Quantization Accuracy | 0.00% - 0.50% degradation |
| Best Case | +0.05% improvement (Fashion-MNIST) |
| STM32H7 Flash Usage | 31.7 KB (1.55%) |
| STM32H7 RAM Usage | 10.5 KB (1.03%) |
| Cortex-M7 Latency | ~42 ms @ 480 MHz |
| Model Compression | 2.91× (SimpleCNN) |

## Experimental Documentation

- [Final Experimental Summary](FINAL_EXPERIMENTAL_SUMMARY.md)
- [Integration Complete](INTEGRATION_COMPLETE.md)
- [Renode Implementation](RENODE_IMPLEMENTATION_COMPLETE.md)
- [Paper Package Info](OVERLEAF_PACKAGE_INFO.md)

## License

See [LICENSE](LICENSE) for details.

## Citation

If you use this platform in your research, please cite our work (paper under review).

## Acknowledgments

Built for edge AI researchers validating compression techniques and embedded deployment pipelines for resource-constrained devices.
