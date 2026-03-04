#!/usr/bin/env python3
"""
Master script to run all experiments for Malak Platform paper
Runs experiments in order and generates final results summary
"""

import subprocess
import json
import time
from pathlib import Path
from datetime import datetime

def run_experiment(script_name, description):
    """Run an experiment script and track timing"""
    print("\n" + "="*80)
    print(f"RUNNING: {description}")
    print("="*80)
    print(f"Script: {script_name}")
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    start_time = time.time()

    try:
        result = subprocess.run(
            ['python3', script_name],
            capture_output=True,
            text=True,
            timeout=7200  # 2 hour timeout
        )

        elapsed = time.time() - start_time

        if result.returncode == 0:
            print(f"\n✅ SUCCESS ({elapsed/60:.1f} minutes)")
            return {
                'status': 'success',
                'elapsed_seconds': elapsed,
                'script': script_name,
                'description': description
            }
        else:
            print(f"\n❌ FAILED ({elapsed/60:.1f} minutes)")
            print(f"Error: {result.stderr}")
            return {
                'status': 'failed',
                'elapsed_seconds': elapsed,
                'script': script_name,
                'description': description,
                'error': result.stderr
            }

    except subprocess.TimeoutExpired:
        print(f"\n⏱️  TIMEOUT (exceeded 2 hours)")
        return {
            'status': 'timeout',
            'script': script_name,
            'description': description
        }

    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        return {
            'status': 'error',
            'script': script_name,
            'description': description,
            'error': str(e)
        }

def check_baseline_exists():
    """Check if baseline CIFAR-10 experiment has been run"""
    baseline_path = Path('experiment_results/model_fp32.pth')
    return baseline_path.exists()

def generate_summary():
    """Generate master summary from all experiment results"""
    print("\n" + "="*80)
    print("GENERATING MASTER SUMMARY")
    print("="*80)

    summary = {
        'timestamp': datetime.now().isoformat(),
        'experiments': {}
    }

    # Collect results from each experiment
    result_files = {
        'baseline': 'experiment_results/results.json',
        'pruning': 'experiment_results/pruning/pruning_results.json',
        'architectures': 'experiment_results/architectures/architecture_comparison.json',
        'fashion_mnist': 'experiment_results/fashion_mnist/results.json'
    }

    for exp_name, result_file in result_files.items():
        result_path = Path(result_file)
        if result_path.exists():
            with open(result_path, 'r') as f:
                summary['experiments'][exp_name] = json.load(f)
            print(f"  ✅ Loaded: {exp_name}")
        else:
            print(f"  ⚠️  Missing: {exp_name}")

    # Save master summary
    output_path = Path('experiment_results/MASTER_SUMMARY.json')
    with open(output_path, 'w') as f:
        json.dump(summary, f, indent=2)

    print(f"\n📁 Master summary saved: {output_path}")

    return summary

def print_final_report(experiment_results, summary):
    """Print final report of all experiments"""
    print("\n" + "="*80)
    print("FINAL EXPERIMENT REPORT")
    print("="*80)

    print("\n📊 Experiment Status:")
    print("-" * 80)
    for result in experiment_results:
        status_icon = "✅" if result['status'] == 'success' else "❌"
        duration = f"{result.get('elapsed_seconds', 0)/60:.1f} min" if 'elapsed_seconds' in result else "N/A"
        print(f"{status_icon} {result['description']:<50} {duration:>10}")

    print("\n📈 Key Results:")
    print("-" * 80)

    # CIFAR-10 baseline
    if 'baseline' in summary['experiments']:
        baseline = summary['experiments']['baseline']
        print(f"\nCIFAR-10 MobileNetV2:")
        print(f"  FP32:     {baseline['fp32']['accuracy']:.2f}%")
        print(f"  INT8 PTQ: {baseline['int8_ptq']['accuracy']:.2f}% (Δ {baseline['int8_ptq']['accuracy_degradation']:.2f}%)")
        print(f"  INT8 QAT: {baseline['int8_qat']['accuracy']:.2f}% (Δ {baseline['int8_qat']['accuracy_degradation']:.2f}%)")

    # Pruning
    if 'pruning' in summary['experiments']:
        pruning = summary['experiments']['pruning']
        print(f"\nPruning (best results):")
        # Find best magnitude pruning result
        best_mag = max(
            [(k, v) for k, v in pruning.items() if 'magnitude' in k],
            key=lambda x: x[1].get('accuracy_after_finetune', 0)
        )
        if best_mag:
            print(f"  Magnitude 30%: {best_mag[1]['accuracy_after_finetune']:.2f}% (Δ {best_mag[1]['accuracy_drop']:.2f}%)")

    # Architectures
    if 'architectures' in summary['experiments']:
        archs = summary['experiments']['architectures']
        print(f"\nOther Architectures:")
        for arch_name, arch_data in archs.items():
            print(f"  {arch_name:<15}: {arch_data['fp32']['accuracy']:.2f}% ({arch_data['parameters']:,} params)")

    # Fashion-MNIST
    if 'fashion_mnist' in summary['experiments']:
        fashion = summary['experiments']['fashion_mnist']
        print(f"\nFashion-MNIST SimpleCNN:")
        print(f"  FP32:     {fashion['fp32']['accuracy']:.2f}%")
        print(f"  INT8 PTQ: {fashion['int8_ptq']['accuracy']:.2f}% (Δ {fashion['int8_ptq']['accuracy_drop']:.2f}%)")

    total_time = sum(r.get('elapsed_seconds', 0) for r in experiment_results)
    print(f"\n⏱️  Total experiment time: {total_time/60:.1f} minutes ({total_time/3600:.1f} hours)")

def main():
    print("="*80)
    print("MALAK PLATFORM - COMPLETE EXPERIMENTAL VALIDATION")
    print("="*80)
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    # Check if baseline exists
    if not check_baseline_exists():
        print("⚠️  WARNING: Baseline CIFAR-10 experiment not found.")
        print("   Run simple_experiment.py first for complete results.")
        print("   Continuing anyway...\n")

    # Define experiments
    experiments = [
        ('simple_experiment.py', 'Baseline CIFAR-10 (MobileNetV2 + quantization)'),
        ('fashion_mnist_experiment.py', 'Fashion-MNIST validation'),
        ('pruning_experiment.py', 'Pruning experiments (magnitude + structured)'),
        ('architecture_comparison.py', 'Architecture comparison (ResNet18, EfficientNet)'),
    ]

    # Run experiments
    experiment_results = []

    for script, description in experiments:
        if not Path(script).exists():
            print(f"\n⚠️  Skipping {script} (not found)")
            experiment_results.append({
                'status': 'skipped',
                'script': script,
                'description': description
            })
            continue

        result = run_experiment(script, description)
        experiment_results.append(result)

        # Short break between experiments
        time.sleep(2)

    # Generate summary
    summary = generate_summary()

    # Print final report
    print_final_report(experiment_results, summary)

    # Save execution log
    log_path = Path('experiment_results/execution_log.json')
    with open(log_path, 'w') as f:
        json.dump({
            'timestamp': datetime.now().isoformat(),
            'experiments': experiment_results
        }, f, indent=2)

    print(f"\n📁 Execution log: {log_path}")
    print(f"\n✅ ALL EXPERIMENTS COMPLETE!")
    print(f"   Finished: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Count successes
    successes = sum(1 for r in experiment_results if r['status'] == 'success')
    total = len(experiment_results)
    print(f"   Success rate: {successes}/{total} ({100*successes/total:.0f}%)")

if __name__ == '__main__':
    main()
