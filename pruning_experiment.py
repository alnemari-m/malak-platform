#!/usr/bin/env python3
"""
Pruning Experiments for Malak Platform
Tests magnitude pruning and structured pruning on CIFAR-10
"""

import torch
import torch.nn as nn
import torch.nn.utils.prune as prune
from torchvision import datasets, transforms
from torch.utils.data import DataLoader
import time
import json
from pathlib import Path

# Import MobileNetV2 from simple_experiment
import sys
sys.path.insert(0, str(Path(__file__).parent))
from simple_experiment import MobileNetV2_CIFAR10

def count_nonzero_parameters(model):
    """Count non-zero parameters in the model"""
    total = 0
    nonzero = 0
    for param in model.parameters():
        total += param.numel()
        nonzero += torch.count_nonzero(param).item()
    return nonzero, total

def magnitude_pruning(model, amount=0.3):
    """Apply unstructured magnitude pruning"""
    for name, module in model.named_modules():
        if isinstance(module, nn.Conv2d) or isinstance(module, nn.Linear):
            prune.l1_unstructured(module, name='weight', amount=amount)
    return model

def structured_pruning(model, amount=0.3):
    """Apply structured pruning (filter pruning for Conv2d)"""
    for name, module in model.named_modules():
        if isinstance(module, nn.Conv2d):
            prune.ln_structured(module, name='weight', amount=amount, n=2, dim=0)
        elif isinstance(module, nn.Linear):
            prune.l1_unstructured(module, name='weight', amount=amount)
    return model

def remove_pruning_reparametrization(model):
    """Remove pruning reparametrization to make pruning permanent"""
    for name, module in model.named_modules():
        if isinstance(module, nn.Conv2d) or isinstance(module, nn.Linear):
            try:
                prune.remove(module, 'weight')
            except:
                pass
    return model

def evaluate_model(model, dataloader, device):
    """Evaluate model accuracy and latency"""
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

def fine_tune(model, train_loader, device, epochs=10, lr=0.001):
    """Fine-tune pruned model"""
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)

    model.train()
    for epoch in range(epochs):
        running_loss = 0.0
        for i, (images, labels) in enumerate(train_loader):
            images, labels = images.to(device), labels.to(device)

            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            running_loss += loss.item()

            if i % 100 == 99:
                print(f'  Epoch [{epoch+1}/{epochs}], Step [{i+1}], Loss: {running_loss/100:.4f}')
                running_loss = 0.0

    return model

def get_model_size_mb(model):
    """Calculate model size in MB"""
    torch.save(model.state_dict(), '/tmp/temp_model.pth')
    size_mb = Path('/tmp/temp_model.pth').stat().st_size / (1024 * 1024)
    Path('/tmp/temp_model.pth').unlink()
    return size_mb

def main():
    print("="*80)
    print("PRUNING EXPERIMENTS FOR MALAK PLATFORM")
    print("="*80)

    # Setup
    device = torch.device('cpu')
    results_dir = Path('experiment_results/pruning')
    results_dir.mkdir(parents=True, exist_ok=True)

    # Data loading
    print("\n1. Loading CIFAR-10 dataset...")
    transform_test = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.4914, 0.4822, 0.4465), (0.2023, 0.1994, 0.2010)),
    ])

    transform_train = transforms.Compose([
        transforms.RandomCrop(32, padding=4),
        transforms.RandomHorizontalFlip(),
        transforms.ToTensor(),
        transforms.Normalize((0.4914, 0.4822, 0.4465), (0.2023, 0.1994, 0.2010)),
    ])

    train_dataset = datasets.CIFAR10(root='./data', train=True, download=True, transform=transform_train)
    test_dataset = datasets.CIFAR10(root='./data', train=False, download=True, transform=transform_test)

    train_loader = DataLoader(train_dataset, batch_size=128, shuffle=True, num_workers=2)
    test_loader = DataLoader(test_dataset, batch_size=128, shuffle=False, num_workers=2)

    # Load baseline model
    print("\n2. Loading baseline FP32 model...")
    baseline_model = MobileNetV2_CIFAR10(num_classes=10)

    if Path('experiment_results/model_fp32.pth').exists():
        baseline_model.load_state_dict(torch.load('experiment_results/model_fp32.pth'))
        print("   Loaded existing model from experiment_results/model_fp32.pth")
    else:
        print("   WARNING: Baseline model not found. Using random initialization.")
        print("   Run simple_experiment.py first for accurate results.")

    baseline_model = baseline_model.to(device)

    # Evaluate baseline
    print("\n3. Evaluating baseline model...")
    baseline_acc, baseline_latency = evaluate_model(baseline_model, test_loader, device)
    baseline_nonzero, baseline_total = count_nonzero_parameters(baseline_model)
    baseline_size = get_model_size_mb(baseline_model)

    print(f"   Accuracy: {baseline_acc:.2f}%")
    print(f"   Latency: {baseline_latency:.3f} ms")
    print(f"   Parameters: {baseline_total:,} (100% non-zero)")
    print(f"   Model size: {baseline_size:.2f} MB")

    # Results storage
    all_results = {
        'baseline': {
            'accuracy': baseline_acc,
            'latency_ms': baseline_latency,
            'parameters_total': baseline_total,
            'parameters_nonzero': baseline_nonzero,
            'sparsity': 0.0,
            'model_size_mb': baseline_size
        }
    }

    # Experiment 1: Magnitude Pruning at different sparsity levels
    print("\n" + "="*80)
    print("EXPERIMENT 1: MAGNITUDE PRUNING")
    print("="*80)

    sparsity_levels = [0.3, 0.5, 0.7, 0.9]

    for sparsity in sparsity_levels:
        print(f"\n--- Sparsity: {sparsity*100:.0f}% ---")

        # Create pruned model
        pruned_model = MobileNetV2_CIFAR10(num_classes=10)
        pruned_model.load_state_dict(baseline_model.state_dict())
        pruned_model = pruned_model.to(device)

        # Apply magnitude pruning
        print(f"   Applying magnitude pruning ({sparsity*100:.0f}% sparsity)...")
        pruned_model = magnitude_pruning(pruned_model, amount=sparsity)

        # Evaluate before fine-tuning
        print("   Evaluating before fine-tuning...")
        acc_before, lat_before = evaluate_model(pruned_model, test_loader, device)
        print(f"   Accuracy (before fine-tune): {acc_before:.2f}%")

        # Fine-tune
        print("   Fine-tuning for 10 epochs...")
        pruned_model = fine_tune(pruned_model, train_loader, device, epochs=10, lr=0.001)

        # Evaluate after fine-tuning
        print("   Evaluating after fine-tuning...")
        acc_after, lat_after = evaluate_model(pruned_model, test_loader, device)

        # Make pruning permanent
        pruned_model = remove_pruning_reparametrization(pruned_model)

        nonzero, total = count_nonzero_parameters(pruned_model)
        actual_sparsity = 1.0 - (nonzero / total)
        model_size = get_model_size_mb(pruned_model)

        print(f"   Accuracy (after fine-tune): {acc_after:.2f}%")
        print(f"   Latency: {lat_after:.3f} ms")
        print(f"   Parameters: {nonzero:,} / {total:,} ({actual_sparsity*100:.1f}% sparse)")
        print(f"   Model size: {model_size:.2f} MB")
        print(f"   Accuracy drop: {baseline_acc - acc_after:.2f}%")

        # Save results
        all_results[f'magnitude_{int(sparsity*100)}'] = {
            'method': 'magnitude_pruning',
            'target_sparsity': sparsity,
            'actual_sparsity': actual_sparsity,
            'accuracy_before_finetune': acc_before,
            'accuracy_after_finetune': acc_after,
            'accuracy_drop': baseline_acc - acc_after,
            'latency_ms': lat_after,
            'parameters_total': total,
            'parameters_nonzero': nonzero,
            'model_size_mb': model_size,
            'compression_ratio': baseline_size / model_size
        }

        # Save model
        torch.save(pruned_model.state_dict(),
                   results_dir / f'model_magnitude_{int(sparsity*100)}.pth')

    # Experiment 2: Structured Pruning
    print("\n" + "="*80)
    print("EXPERIMENT 2: STRUCTURED PRUNING")
    print("="*80)

    for sparsity in [0.3, 0.5]:  # Structured pruning is more aggressive
        print(f"\n--- Sparsity: {sparsity*100:.0f}% ---")

        # Create pruned model
        pruned_model = MobileNetV2_CIFAR10(num_classes=10)
        pruned_model.load_state_dict(baseline_model.state_dict())
        pruned_model = pruned_model.to(device)

        # Apply structured pruning
        print(f"   Applying structured pruning ({sparsity*100:.0f}% sparsity)...")
        pruned_model = structured_pruning(pruned_model, amount=sparsity)

        # Evaluate before fine-tuning
        print("   Evaluating before fine-tuning...")
        acc_before, lat_before = evaluate_model(pruned_model, test_loader, device)
        print(f"   Accuracy (before fine-tune): {acc_before:.2f}%")

        # Fine-tune
        print("   Fine-tuning for 10 epochs...")
        pruned_model = fine_tune(pruned_model, train_loader, device, epochs=10, lr=0.001)

        # Evaluate after fine-tuning
        print("   Evaluating after fine-tuning...")
        acc_after, lat_after = evaluate_model(pruned_model, test_loader, device)

        # Make pruning permanent
        pruned_model = remove_pruning_reparametrization(pruned_model)

        nonzero, total = count_nonzero_parameters(pruned_model)
        actual_sparsity = 1.0 - (nonzero / total)
        model_size = get_model_size_mb(pruned_model)

        print(f"   Accuracy (after fine-tune): {acc_after:.2f}%")
        print(f"   Latency: {lat_after:.3f} ms")
        print(f"   Parameters: {nonzero:,} / {total:,} ({actual_sparsity*100:.1f}% sparse)")
        print(f"   Model size: {model_size:.2f} MB")
        print(f"   Accuracy drop: {baseline_acc - acc_after:.2f}%")

        # Save results
        all_results[f'structured_{int(sparsity*100)}'] = {
            'method': 'structured_pruning',
            'target_sparsity': sparsity,
            'actual_sparsity': actual_sparsity,
            'accuracy_before_finetune': acc_before,
            'accuracy_after_finetune': acc_after,
            'accuracy_drop': baseline_acc - acc_after,
            'latency_ms': lat_after,
            'parameters_total': total,
            'parameters_nonzero': nonzero,
            'model_size_mb': model_size,
            'compression_ratio': baseline_size / model_size
        }

        # Save model
        torch.save(pruned_model.state_dict(),
                   results_dir / f'model_structured_{int(sparsity*100)}.pth')

    # Save all results
    print("\n" + "="*80)
    print("SAVING RESULTS")
    print("="*80)

    with open(results_dir / 'pruning_results.json', 'w') as f:
        json.dump(all_results, f, indent=2)

    print(f"\nResults saved to: {results_dir}/pruning_results.json")

    # Print summary table
    print("\n" + "="*80)
    print("SUMMARY TABLE")
    print("="*80)
    print(f"{'Method':<20} {'Sparsity':<10} {'Accuracy':<10} {'Drop':<8} {'Size (MB)':<10} {'Ratio':<8}")
    print("-"*80)

    print(f"{'Baseline':<20} {'0%':<10} {baseline_acc:>6.2f}%   {'-':<8} {baseline_size:>6.2f}     {'1.0x':<8}")

    for key, result in all_results.items():
        if key == 'baseline':
            continue

        method = result['method'].replace('_', ' ').title()
        sparsity = f"{result['actual_sparsity']*100:.0f}%"
        acc = result['accuracy_after_finetune']
        drop = result['accuracy_drop']
        size = result['model_size_mb']
        ratio = result['compression_ratio']

        print(f"{method:<20} {sparsity:<10} {acc:>6.2f}%   {drop:>5.2f}%  {size:>6.2f}     {ratio:>4.2f}x")

    print("\n✅ Pruning experiments complete!")
    print(f"📁 Results: {results_dir}/")

    return all_results

if __name__ == '__main__':
    results = main()
