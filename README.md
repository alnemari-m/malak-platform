# Malak

**A Python toolkit for edge AI model optimization.**

Malak provides a unified, high-level API for training, quantization, pruning, knowledge distillation, ONNX export, inference benchmarking, and monitoring — all built on PyTorch.

## Features

| Category | Capabilities |
|----------|-------------|
| **Training** | SGD/Adam optimizers, cosine annealing, CIFAR-10 and Fashion-MNIST loaders |
| **Quantization** | Dynamic PTQ, Static PTQ, Quantization-Aware Training (QAT) |
| **Compression** | Magnitude pruning, structured pruning, knowledge distillation |
| **Export** | ONNX model export with validation |
| **Runtime** | Latency and throughput benchmarking |
| **Monitoring** | Per-layer latency profiling, KL-divergence drift detection |
| **CLI** | `edgeai` command-line tool for common tasks |
| **Embedded** | Proof-of-concept C inference for ARM Cortex-M7 (STM32H7) |

## Installation

```bash
git clone https://github.com/alnemari-m/malak-platform.git
cd malak-platform
pip install -e .
```

For optional ONNX support:
```bash
pip install -e ".[onnx]"
```

## Quick Start

### Python API

```python
from malak.training import Trainer, get_cifar10
from malak.quantization import DynamicPTQ, QAT

# Load data and train
train_loader, test_loader, _, _ = get_cifar10()
trainer = Trainer(model, lr=0.01, optimizer_type="sgd")
trainer.train(train_loader, test_loader, epochs=100)

# Quantize with dynamic PTQ
dptq = DynamicPTQ()
quantized = dptq.quantize(model)

# Or use QAT for better compression
qat = QAT()
model = qat.prepare(model, backend="fbgemm")
model = qat.train(model, train_loader, test_loader, epochs=20)
quantized = qat.convert(model)
```

### CLI

```bash
edgeai train --dataset cifar10 --model mobilenetv2 --epochs 100
edgeai quantize --model model.pth --method ptq-dynamic
edgeai evaluate --model model.pth --dataset cifar10
edgeai export --model model.pth
edgeai profile --model model.pth
```

## Experimental Results

Validated on CIFAR-10 and Fashion-MNIST with four architectures:

### Quantization (CIFAR-10, MobileNetV2)

| Method | Accuracy | Size | Compression |
|--------|----------|------|-------------|
| FP32 Baseline | 77.81% | 8.76 MB | 1.00x |
| Dynamic PTQ | 77.84% | 8.73 MB | 1.00x |
| QAT (INT8) | 76.72% | 2.82 MB | 3.10x |

### Architecture Comparison (Dynamic INT8 PTQ, CIFAR-10)

| Model | FP32 | INT8 | Drop |
|-------|------|------|------|
| ResNet18 | 87.41% | 87.38% | 0.03% |
| EfficientNet-B0 | 66.81% | 66.68% | 0.13% |

### Pruning (MobileNetV2, with fine-tuning)

| Method | Sparsity | Accuracy | Drop |
|--------|----------|----------|------|
| Magnitude | 30% | 77.32% | 0.49% |
| Magnitude | 50% | 75.66% | 2.15% |
| Magnitude | 70% | 70.47% | 7.34% |
| Structured | 30% | 72.86% | 4.95% |
| Structured | 50% | 64.17% | 13.64% |

### Fashion-MNIST (SimpleCNN)

| Method | Accuracy | Size | Compression |
|--------|----------|------|-------------|
| FP32 Baseline | 92.19% | 1.75 MB | 1.00x |
| Dynamic PTQ | 92.20% | 0.60 MB | 2.91x |

## Reproducing Results

```bash
python experiments/simple_experiment.py          # CIFAR-10 baseline + quantization
python experiments/architecture_comparison.py    # ResNet18 vs EfficientNet-B0
python experiments/fashion_mnist_experiment.py   # Fashion-MNIST
python experiments/pruning_experiment.py         # Magnitude + structured pruning
```

Results are saved as JSON in `experiment_results/`.

## Repository Structure

```
malak-platform/
├── malak/                  # Python package (13 modules)
│   ├── training/           # Trainer, dataset loaders
│   ├── quantization/       # DynamicPTQ, StaticPTQ, QAT
│   ├── compression/        # Pruning, distillation
│   ├── compiler/           # ONNX export
│   ├── runtime/            # Inference benchmarking
│   ├── monitoring/         # Profiling, drift detection
│   └── cli.py              # edgeai CLI
├── experiments/            # Reproducible experiment scripts
├── embedded/               # ARM Cortex-M7 C inference PoC
├── tests/                  # pytest test suite
├── paper/                  # LaTeX paper source
├── pyproject.toml          # Package metadata
└── LICENSE                 # MIT
```

## API Reference

| Module | Key Classes |
|--------|------------|
| `malak.training` | `Trainer`, `get_cifar10()`, `get_fashion_mnist()` |
| `malak.quantization` | `DynamicPTQ`, `StaticPTQ`, `QAT` |
| `malak.compression` | `MagnitudePruner`, `StructuredPruner`, `KnowledgeDistiller` |
| `malak.compiler` | `export_onnx()`, `validate_onnx()` |
| `malak.runtime` | `InferenceBenchmark` |
| `malak.monitoring` | `LayerProfiler`, `DriftDetector` |

## Tests

```bash
pip install -e ".[dev]"
pytest tests/ -v
```

## Author

**Mohammed Hassan Alnemari**
Department of Computer Engineering, University of Tabuk, Saudi Arabia
AIST Research Center, University of Tabuk

## License

MIT License. See [LICENSE](LICENSE) for details.
