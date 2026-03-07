# Malak

A Python toolkit for edge AI model optimization.

Malak provides a unified API for training, quantization, pruning, distillation,
ONNX export, inference benchmarking, and monitoring — all built on PyTorch.

## Features

- **Training**: Configurable training loop with SGD/Adam, cosine annealing, CIFAR-10/Fashion-MNIST loaders
- **Quantization**: Dynamic PTQ, Static PTQ, Quantization-Aware Training (QAT)
- **Compression**: Magnitude pruning, structured pruning, knowledge distillation
- **Export**: ONNX model export with validation
- **Runtime**: Latency and throughput benchmarking
- **Monitoring**: Per-layer latency profiling, KL-divergence drift detection
- **CLI**: `edgeai` command-line tool for common tasks
- **Embedded**: Proof-of-concept C inference for ARM Cortex-M7

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

# Load data
train_loader, test_loader, _, _ = get_cifar10()

# Train a model
trainer = Trainer(model, lr=0.01, optimizer_type="sgd")
trainer.train(train_loader, test_loader, epochs=100)

# Quantize with dynamic PTQ
dptq = DynamicPTQ()
quantized = dptq.quantize(model)

# Or use QAT for better accuracy
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

## Reproducing Paper Results

Run experiments in order:

```bash
# 1. CIFAR-10 baseline + quantization (long — can run overnight)
python experiments/simple_experiment.py

# 2. Architecture comparison
python experiments/architecture_comparison.py

# 3. Fashion-MNIST (quick)
python experiments/fashion_mnist_experiment.py

# 4. Pruning (requires step 1)
python experiments/pruning_experiment.py

# 5. Update paper tables with measured results
python experiments/update_paper_tables.py
```

Results are saved as JSON in `experiment_results/`.

## Repository Structure

```
malak-platform/
├── malak/                  # Python package
│   ├── training/           # Trainer, dataset loaders
│   ├── quantization/       # DynamicPTQ, StaticPTQ, QAT
│   ├── compression/        # Pruning, distillation
│   ├── compiler/           # ONNX export
│   ├── runtime/            # Inference benchmarking
│   ├── monitoring/         # Profiling, drift detection
│   ├── cli.py              # edgeai CLI
│   └── model_card.py       # YAML model cards
├── experiments/            # Reproducible experiment scripts
├── embedded/               # ARM Cortex-M7 C inference (proof-of-concept)
├── tests/                  # pytest test suite
├── paper/                  # SoftwareX LaTeX paper
├── pyproject.toml          # Package metadata
└── LICENSE                 # MIT
```

## Tests

```bash
pip install -e ".[dev]"
pytest tests/ -v
```

## API Overview

| Module | Key Classes/Functions |
|--------|----------------------|
| `malak.training` | `Trainer`, `get_cifar10()`, `get_fashion_mnist()` |
| `malak.quantization` | `DynamicPTQ`, `StaticPTQ`, `QAT` |
| `malak.compression` | `MagnitudePruner`, `StructuredPruner`, `KnowledgeDistiller` |
| `malak.compiler` | `export_onnx()`, `validate_onnx()` |
| `malak.runtime` | `InferenceBenchmark` |
| `malak.monitoring` | `LayerProfiler`, `DriftDetector` |

## License

MIT License. See [LICENSE](LICENSE) for details.

## Citation

If you use Malak in your research, please cite our paper (under review at SoftwareX).
