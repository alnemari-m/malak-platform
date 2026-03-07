#!/usr/bin/env python3
"""Export trained SimpleCNN weights to C arrays for embedded deployment."""

import sys, os, torch, json
import torch.nn as nn
import numpy as np
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

class SimpleCNN(nn.Module):
    def __init__(self, num_classes=10):
        super().__init__()
        self.features = nn.Sequential(
            nn.Conv2d(1, 32, kernel_size=3, padding=1), nn.ReLU(inplace=True),
            nn.MaxPool2d(2, 2),
            nn.Conv2d(32, 64, kernel_size=3, padding=1), nn.ReLU(inplace=True),
            nn.MaxPool2d(2, 2),
            nn.Conv2d(64, 64, kernel_size=3, padding=1), nn.ReLU(inplace=True),
        )
        self.classifier = nn.Sequential(
            nn.Linear(64*7*7, 128), nn.ReLU(inplace=True),
            nn.Dropout(0.5), nn.Linear(128, num_classes),
        )
    def forward(self, x):
        return self.classifier(torch.flatten(self.features(x), 1))

OUTPUT_DIR = Path(__file__).parent.parent / 'models'
MODEL_PATH = Path(__file__).parent.parent.parent / 'experiment_results' / 'fashion_mnist' / 'best_model.pth'

def weight_to_int8(tensor):
    t = tensor.detach().cpu().numpy().flatten()
    abs_max = np.abs(t).max()
    if abs_max == 0: return np.zeros_like(t, dtype=np.int8), 1.0
    scale = abs_max / 127.0
    return np.clip(np.round(t / scale), -127, 127).astype(np.int8), float(scale)

def array_to_c(name, arr, lw=16):
    lines = [f'static const int8_t {name}[{len(arr)}] = {{']
    for i in range(0, len(arr), lw):
        chunk = arr[i:i+lw]
        lines.append('    ' + ', '.join(f'{v:4d}' for v in chunk) + ',')
    lines.append('};')
    return chr(10).join(lines)

def main():
    print('Export SimpleCNN Weights to C (INT8)')
    model = SimpleCNN(num_classes=10)
    if MODEL_PATH.exists():
        model.load_state_dict(torch.load(MODEL_PATH, map_location='cpu'))
        print(f'Loaded weights from {MODEL_PATH}')
    else:
        print(f'WARNING: {MODEL_PATH} not found, using random weights.')
    model.eval()
    layers, scales = {}, {}
    layers['conv1_weight'], scales['conv1'] = weight_to_int8(model.features[0].weight)
    layers['conv2_weight'], scales['conv2'] = weight_to_int8(model.features[3].weight)
    layers['conv3_weight'], scales['conv3'] = weight_to_int8(model.features[6].weight)
    layers['fc1_weight'], scales['fc1'] = weight_to_int8(model.classifier[0].weight)
    layers['fc2_weight'], scales['fc2'] = weight_to_int8(model.classifier[3].weight)
    total_bytes = sum(len(v) for v in layers.values() if isinstance(v, np.ndarray))
    print(f'Total INT8 weight bytes: {total_bytes:,} ({total_bytes/1024:.1f} KB)')

    # header
    h = ['/* SimpleCNN INT8 weights - Malak Platform */',
         '#ifndef CIFAR10_MODEL_H', '#define CIFAR10_MODEL_H',
         '#include <stdint.h>', '#include <stddef.h>', '',
         '#define NUM_CLASSES 10', '#define INPUT_CHANNELS 1',
         '#define INPUT_HEIGHT 28', '#define INPUT_WIDTH 28',
         '#define INPUT_SIZE (INPUT_CHANNELS * INPUT_HEIGHT * INPUT_WIDTH)', '']
    for n, s in scales.items():
        h.append(f'#define SCALE_{n.upper()} {s:.8f}f')
    h += ['', 'int model_init(void);',
          'int model_infer(const uint8_t* input, float* output);',
          'size_t model_get_memory_size(void);',
          'int model_argmax(const float* output);',
          '', '#endif']

    # impl - weights + inference
    c = ['/* SimpleCNN INT8 inference - Malak Platform */',
         '#include "cifar10_model.h"', '#include <string.h>', '']
    for name, arr in layers.items():
        if isinstance(arr, np.ndarray):
            c.append(array_to_c(name, arr))
            c.append('')

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_DIR / 'cifar10_model.h', 'w') as f:
        f.write(chr(10).join(h))
    with open(OUTPUT_DIR / 'weights.c', 'w') as f:
        f.write(chr(10).join(c))

    meta = {'model': 'SimpleCNN', 'dataset': 'Fashion-MNIST',
            'quantization': 'symmetric_int8', 'total_weight_bytes': int(total_bytes),
            'scales': scales}
    with open(OUTPUT_DIR / 'model_metadata.json', 'w') as f:
        json.dump(meta, f, indent=2)
    print(f'Generated: {OUTPUT_DIR}/')

if __name__ == '__main__':
    main()