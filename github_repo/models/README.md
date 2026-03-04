# Pre-trained Models

This directory contains pre-trained models for the experiments.

## Available Models

### CIFAR-10 Classification

**Note**: Model files (*.pth) are not included in the repository due to size constraints.
To obtain the models, run the experiment script:

```bash
cd experiments
python simple_experiment.py
```

This will generate:
- `model_fp32_best.pth` - FP32 baseline model (8.76 MB)
- `model_int8_ptq.pth` - INT8 post-training quantization (8.73 MB)
- `model_int8_qat.pth` - INT8 quantization-aware training (8.73 MB)

## Model Details

### MobileNetV2 (CIFAR-10)

- **Architecture**: MobileNetV2
- **Parameters**: 2,236,682 (~2.2M)
- **Input**: 32×32 RGB images
- **Output**: 10 classes
- **Accuracy**: 89.28% (FP32), 88.78% (INT8 QAT)

## Using Pre-trained Models

```python
import torch
from torchvision.models import mobilenet_v2

# Load FP32 model
model = mobilenet_v2(num_classes=10)
model.load_state_dict(torch.load('model_fp32_best.pth'))
model.eval()

# Load INT8 model
model_int8 = torch.load('model_int8_qat.pth')
model_int8.eval()
```

## License

Models are released under the same MIT License as the codebase.
