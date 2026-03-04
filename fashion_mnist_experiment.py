#!/usr/bin/env python3
"""
Fashion-MNIST Experiment for Malak Platform
Quick validation on simpler dataset
"""

import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms
from torch.utils.data import DataLoader
import time
import json
from pathlib import Path

class SimpleCNN(nn.Module):
    """Simple CNN for Fashion-MNIST"""
    def __init__(self, num_classes=10):
        super(SimpleCNN, self).__init__()
        self.features = nn.Sequential(
            nn.Conv2d(1, 32, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2),
            nn.Conv2d(32, 64, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2),
            nn.Conv2d(64, 64, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
        )
        self.classifier = nn.Sequential(
            nn.Linear(64 * 7 * 7, 128),
            nn.ReLU(inplace=True),
            nn.Dropout(0.5),
            nn.Linear(128, num_classes)
        )

    def forward(self, x):
        x = self.features(x)
        x = torch.flatten(x, 1)
        x = self.classifier(x)
        return x

def train_model(model, train_loader, device, epochs=20, lr=0.001):
    """Train model"""
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=lr)

    model.train()
    for epoch in range(epochs):
        running_loss = 0.0
        correct = 0
        total = 0

        for i, (images, labels) in enumerate(train_loader):
            images, labels = images.to(device), labels.to(device)

            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            running_loss += loss.item()
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()

        train_acc = 100 * correct / total
        print(f'  Epoch [{epoch+1}/{epochs}], Loss: {running_loss/len(train_loader):.4f}, Acc: {train_acc:.2f}%')

    return model

def evaluate_model(model, dataloader, device):
    """Evaluate model"""
    model.eval()
    correct = 0
    total = 0
    latencies = []

    with torch.no_grad():
        for images, labels in dataloader:
            images, labels = images.to(device), labels.to(device)

            start = time.time()
            outputs = model(images)
            latency = time.time() - start
            latencies.append(latency)

            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()

    accuracy = 100 * correct / total
    avg_latency = sum(latencies) / len(latencies) * 1000  # ms

    return accuracy, avg_latency

def count_parameters(model):
    """Count parameters"""
    return sum(p.numel() for p in model.parameters() if p.requires_grad)

def get_model_size_mb(model):
    """Get model size"""
    torch.save(model.state_dict(), '/tmp/temp_model.pth')
    size_mb = Path('/tmp/temp_model.pth').stat().st_size / (1024 * 1024)
    Path('/tmp/temp_model.pth').unlink()
    return size_mb

def main():
    print("="*80)
    print("FASHION-MNIST EXPERIMENT FOR MALAK PLATFORM")
    print("="*80)

    # Setup
    device = torch.device('cpu')
    results_dir = Path('experiment_results/fashion_mnist')
    results_dir.mkdir(parents=True, exist_ok=True)

    # Data loading
    print("\n1. Loading Fashion-MNIST dataset...")
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.2860,), (0.3530,))
    ])

    train_dataset = datasets.FashionMNIST(root='./data', train=True, download=True, transform=transform)
    test_dataset = datasets.FashionMNIST(root='./data', train=False, download=True, transform=transform)

    train_loader = DataLoader(train_dataset, batch_size=128, shuffle=True, num_workers=2)
    test_loader = DataLoader(test_dataset, batch_size=128, shuffle=False, num_workers=2)

    print(f"   Training samples: {len(train_dataset)}")
    print(f"   Test samples: {len(test_dataset)}")

    # Create model
    print("\n2. Creating SimpleCNN model...")
    model = SimpleCNN(num_classes=10).to(device)
    params = count_parameters(model)
    print(f"   Parameters: {params:,}")

    # Train model
    print("\n3. Training for 20 epochs...")
    model = train_model(model, train_loader, device, epochs=20, lr=0.001)

    # Evaluate FP32
    print("\n4. Evaluating FP32 model...")
    fp32_acc, fp32_latency = evaluate_model(model, test_loader, device)
    fp32_size = get_model_size_mb(model)

    print(f"   Accuracy: {fp32_acc:.2f}%")
    print(f"   Latency: {fp32_latency:.3f} ms")
    print(f"   Model size: {fp32_size:.2f} MB")

    # Save FP32 model
    torch.save(model.state_dict(), results_dir / 'model_fp32.pth')

    # Apply quantization
    print("\n5. Applying dynamic INT8 quantization...")
    model_int8 = torch.quantization.quantize_dynamic(
        model,
        {nn.Linear, nn.Conv2d},
        dtype=torch.qint8
    )

    # Evaluate INT8
    print("\n6. Evaluating INT8 model...")
    int8_acc, int8_latency = evaluate_model(model_int8, test_loader, device)
    int8_size = get_model_size_mb(model_int8)

    print(f"   Accuracy: {int8_acc:.2f}%")
    print(f"   Latency: {int8_latency:.3f} ms")
    print(f"   Model size: {int8_size:.2f} MB")
    print(f"   Accuracy drop: {fp32_acc - int8_acc:.2f}%")
    print(f"   Compression ratio: {fp32_size / int8_size:.2f}x")

    # Save INT8 model
    torch.save(model_int8.state_dict(), results_dir / 'model_int8.pth')

    # Store results
    results = {
        'dataset': 'Fashion-MNIST',
        'model': 'SimpleCNN',
        'parameters': params,
        'fp32': {
            'accuracy': fp32_acc,
            'latency_ms': fp32_latency,
            'model_size_mb': fp32_size
        },
        'int8_ptq': {
            'accuracy': int8_acc,
            'latency_ms': int8_latency,
            'model_size_mb': int8_size,
            'accuracy_drop': fp32_acc - int8_acc,
            'compression_ratio': fp32_size / int8_size
        }
    }

    # Save results
    with open(results_dir / 'results.json', 'w') as f:
        json.dump(results, f, indent=2)

    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)
    print(f"Model: SimpleCNN")
    print(f"Parameters: {params:,}")
    print(f"\nFP32:")
    print(f"  Accuracy: {fp32_acc:.2f}%")
    print(f"  Size: {fp32_size:.2f} MB")
    print(f"\nINT8:")
    print(f"  Accuracy: {int8_acc:.2f}% (drop: {fp32_acc - int8_acc:.2f}%)")
    print(f"  Size: {int8_size:.2f} MB (ratio: {fp32_size / int8_size:.2f}x)")

    print(f"\n✅ Fashion-MNIST experiment complete!")
    print(f"📁 Results: {results_dir}/")

    return results

if __name__ == '__main__':
    results = main()
