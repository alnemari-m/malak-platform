# Reproducing Paper Results

This directory contains scripts to reproduce the experimental results reported in our paper.

## CIFAR-10 Image Classification

**Paper Section**: Experiments & Results
**Objective**: Validate Malak Platform's quantization pipeline on standard benchmark
**Model**: MobileNetV2 (2.2M parameters)
**Dataset**: CIFAR-10 (50k train, 10k test, 10 classes, 32×32 RGB)

### Quick Reproduction

```bash
# Install dependencies
pip install -r ../requirements.txt

# Run experiment (takes ~2-3 hours on CPU)
python simple_experiment.py

# Results will be saved to experiment_results/
```

### Expected Results

| Configuration | Accuracy | Δ vs. FP32 | Model Size | Latency |
|--------------|----------|------------|------------|---------|
| **FP32 Baseline** | ~89.28% | - | 8.76 MB | 0.667 ms |
| **INT8 PTQ** | ~89.26% | -0.02% | 8.73 MB | 0.668 ms |
| **INT8 QAT** | ~88.78% | -0.50% | 8.73 MB | 0.668 ms |

**Key Finding**: Only 0.5% accuracy degradation with quantization-aware training.

---

## Detailed Instructions

### 1. System Requirements

**Hardware**:
- CPU: Any modern x86_64 processor (tested on Intel/AMD)
- RAM: 8 GB minimum (16 GB recommended)
- Storage: 2 GB free (for dataset + models)
- GPU: Optional (experiment uses CPU by default)

**Software**:
- Python 3.8 or higher
- pip (latest version)
- Internet connection (for dataset download)

### 2. Environment Setup

#### Option A: Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv malak_env

# Activate it
source malak_env/bin/activate  # Linux/Mac
# or
malak_env\Scripts\activate      # Windows

# Install dependencies
pip install -r ../requirements.txt
```

#### Option B: Conda Environment

```bash
# Create conda environment
conda create -n malak python=3.10

# Activate it
conda activate malak

# Install PyTorch
conda install pytorch torchvision -c pytorch

# Install other dependencies
pip install tqdm numpy
```

### 3. Running the Experiment

```bash
cd experiments
python simple_experiment.py
```

**What happens**:
1. Downloads CIFAR-10 dataset (~170 MB, automatic)
2. Trains MobileNetV2 for 100 epochs (~2 hours on CPU)
3. Applies post-training quantization (INT8 PTQ)
4. Fine-tunes with quantization-aware training (INT8 QAT, 10 epochs)
5. Evaluates all three models on test set
6. Measures inference latency
7. Saves results to `experiment_results/`

**Progress monitoring**:
```
Epoch [1/100]: 100%|████████| 391/391 [01:23<00:00]
Train Loss: 1.8234, Train Acc: 32.45%, Test Acc: 45.67%
...
Epoch [100/100]: 100%|████████| 391/391 [01:20<00:00]
Train Loss: 0.0234, Train Acc: 98.83%, Test Acc: 89.28%

✓ FP32 training complete: 89.28% accuracy
✓ INT8 PTQ applied: 89.26% accuracy (-0.02%)
✓ INT8 QAT applied: 88.78% accuracy (-0.50%)
```

### 4. Output Files

After completion, check `experiment_results/`:

```
experiment_results/
├── results.json              # Machine-readable results
├── paper_summary.txt         # Human-readable summary
├── model_fp32_best.pth       # Trained FP32 model (8.76 MB)
├── model_int8_ptq.pth        # INT8 PTQ model (8.73 MB)
└── model_int8_qat.pth        # INT8 QAT model (8.73 MB)
```

**results.json** contains:
```json
{
  "accuracy": {
    "fp32_baseline": 89.28,
    "int8_ptq": 89.26,
    "int8_qat": 88.78
  },
  "performance": {
    "fp32_latency_ms": 0.667,
    "int8_latency_ms": 0.668
  },
  "model_size": {
    "fp32_mb": 8.76,
    "int8_mb": 8.73
  }
}
```

### 5. Troubleshooting

#### Dataset Download Fails
```bash
# Manual download
wget https://www.cs.toronto.edu/~kriz/cifar-10-python.tar.gz
tar -xzf cifar-10-python.tar.gz -C data/
```

#### Out of Memory
```python
# Reduce batch size in simple_experiment.py
BATCH_SIZE = 64  # Default is 128
```

#### Slow Training
```python
# Use GPU if available
DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Or reduce epochs for quick test
EPOCHS_FP32 = 10  # Instead of 100
```

#### Different Results
Results may vary slightly (±0.5%) due to:
- Random initialization
- Hardware differences
- PyTorch version differences

This is normal for neural network training.

---

## Understanding the Code

### Training Pipeline

```python
# 1. Load CIFAR-10
trainset = torchvision.datasets.CIFAR10(root='./data', train=True)

# 2. Create MobileNetV2
model = torchvision.models.mobilenet_v2(num_classes=10)

# 3. Train with SGD + Cosine Annealing
optimizer = torch.optim.SGD(model.parameters(), lr=0.1, momentum=0.9)
scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=100)

# 4. Train for 100 epochs
for epoch in range(100):
    train_epoch(model, trainloader, criterion, optimizer)
    test_accuracy = evaluate(model, testloader)
```

### Quantization Pipeline

```python
# Post-Training Quantization (PTQ)
model_int8_ptq = torch.quantization.quantize_dynamic(
    model,
    {nn.Linear, nn.Conv2d},
    dtype=torch.qint8
)

# Quantization-Aware Training (QAT)
model.qconfig = torch.quantization.get_default_qat_qconfig('fbgemm')
model_prepared = torch.quantization.prepare_qat(model)
# Fine-tune for 10 epochs
model_int8_qat = torch.quantization.convert(model_prepared)
```

### Performance Measurement

```python
# Measure latency
latencies = []
for images, _ in testloader:
    start = time.time()
    _ = model(images)
    end = time.time()
    latencies.append((end - start) * 1000)  # Convert to ms

avg_latency = np.mean(latencies)
```

---

## Extending the Experiments

### Test on Different Architectures

```python
# In simple_experiment.py, replace MobileNetV2 with:
from torchvision.models import resnet18, efficientnet_b0

model = resnet18(num_classes=10)
# or
model = efficientnet_b0(num_classes=10)
```

### Try Different Datasets

```python
# CIFAR-100 (100 classes)
trainset = torchvision.datasets.CIFAR100(root='./data', train=True)

# Fashion-MNIST (grayscale clothing)
trainset = torchvision.datasets.FashionMNIST(root='./data', train=True)
```

### Add More Compression Techniques

```python
# Pruning
import torch.nn.utils.prune as prune
prune.l1_unstructured(model.features[0], name='weight', amount=0.3)

# Knowledge Distillation
# (Requires teacher model - see docs)
```

---

## Validation Checklist

After running the experiment, verify:

- [ ] Training completes without errors
- [ ] FP32 accuracy ≥ 88% (within 1-2% of reported 89.28%)
- [ ] Quantized accuracy within 1% of FP32
- [ ] Model files saved to `experiment_results/`
- [ ] `results.json` contains all metrics
- [ ] Inference latency < 1 ms per image

---

## Citation

If you use this experiment in your research:

```bibtex
@article{alnemari2026malak,
  title={Malak Platform: An End-to-End Framework for Edge AI Deployment},
  author={Alnemari, Mohammed},
  journal={arXiv preprint},
  year={2026}
}
```

---

## Questions?

- **Issues**: [GitHub Issues](https://github.com/alnemari-m/malak_platform/issues)
- **Discussions**: [GitHub Discussions](https://github.com/alnemari-m/malak_platform/discussions)
- **Email**: See main README.md

---

**Last Updated**: March 2026
**Experiment Version**: 1.0
**Paper Version**: Submitted
