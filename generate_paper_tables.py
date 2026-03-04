#!/usr/bin/env python3
"""
Generate LaTeX tables for paper from all experiment results
"""

import json
from pathlib import Path

def load_results():
    """Load all experiment results"""
    results = {}

    files = {
        'baseline': 'experiment_results/results.json',
        'pruning': 'experiment_results/pruning/pruning_results.json',
        'architectures': 'experiment_results/architectures/architecture_comparison.json',
        'fashion_mnist': 'experiment_results/fashion_mnist/results.json'
    }

    for name, path in files.items():
        p = Path(path)
        if p.exists():
            with open(p, 'r') as f:
                results[name] = json.load(f)

    return results

def generate_compression_table(results):
    """Generate compression comparison table"""
    latex = r"""\begin{table}[h]
\centering
\caption{Compression Strategy Comparison on CIFAR-10}
\label{tab:compression_comparison}
\begin{tabular}{lcccc}
\hline
\textbf{Method} & \textbf{Accuracy} & \textbf{$\Delta$ vs. FP32} & \textbf{Size (MB)} & \textbf{Ratio} \\
\hline
"""

    if 'baseline' in results:
        b = results['baseline']
        latex += f"FP32 Baseline & {b['fp32']['accuracy']:.2f}\\% & - & {b['fp32']['model_size_mb']:.2f} & 1.0$\\times$ \\\\\n"
        latex += f"INT8 PTQ & {b['int8_ptq']['accuracy']:.2f}\\% & {b['int8_ptq']['accuracy_degradation']:.2f}\\% & {b['int8_ptq']['model_size_mb']:.2f} & {b['fp32']['model_size_mb']/b['int8_ptq']['model_size_mb']:.2f}$\\times$ \\\\\n"
        latex += f"INT8 QAT & {b['int8_qat']['accuracy']:.2f}\\% & {b['int8_qat']['accuracy_degradation']:.2f}\\% & {b['int8_qat']['model_size_mb']:.2f} & {b['fp32']['model_size_mb']/b['int8_qat']['model_size_mb']:.2f}$\\times$ \\\\\n"

    if 'pruning' in results:
        p = results['pruning']
        # Add magnitude 30% pruning
        if 'magnitude_30' in p:
            m30 = p['magnitude_30']
            latex += f"Magnitude Pruning (30\\%) & {m30['accuracy_after_finetune']:.2f}\\% & {m30['accuracy_drop']:.2f}\\% & {m30['model_size_mb']:.2f} & {m30['compression_ratio']:.2f}$\\times$ \\\\\n"

        # Add magnitude 50% pruning
        if 'magnitude_50' in p:
            m50 = p['magnitude_50']
            latex += f"Magnitude Pruning (50\\%) & {m50['accuracy_after_finetune']:.2f}\\% & {m50['accuracy_drop']:.2f}\\% & {m50['model_size_mb']:.2f} & {m50['compression_ratio']:.2f}$\\times$ \\\\\n"

    latex += r"""\hline
\end{tabular}
\end{table}
"""

    return latex

def generate_architecture_table(results):
    """Generate architecture comparison table"""
    latex = r"""\begin{table}[h]
\centering
\caption{Architecture Comparison on CIFAR-10}
\label{tab:architecture_comparison}
\begin{tabular}{lcccc}
\hline
\textbf{Architecture} & \textbf{Parameters} & \textbf{FP32 Acc} & \textbf{INT8 Acc} & \textbf{$\Delta$} \\
\hline
"""

    if 'baseline' in results:
        b = results['baseline']
        params = "2.2M"  # MobileNetV2
        latex += f"MobileNetV2 & {params} & {b['fp32']['accuracy']:.2f}\\% & {b['int8_qat']['accuracy']:.2f}\\% & {b['int8_qat']['accuracy_degradation']:.2f}\\% \\\\\n"

    if 'architectures' in results:
        for arch_name, arch_data in results['architectures'].items():
            params_str = f"{arch_data['parameters']/1e6:.1f}M"
            latex += f"{arch_name} & {params_str} & {arch_data['fp32']['accuracy']:.2f}\\% & {arch_data['int8']['accuracy']:.2f}\\% & {arch_data['int8']['accuracy_drop']:.2f}\\% \\\\\n"

    latex += r"""\hline
\end{tabular}
\end{table}
"""

    return latex

def generate_dataset_table(results):
    """Generate dataset comparison table"""
    latex = r"""\begin{table}[h]
\centering
\caption{Cross-Dataset Validation}
\label{tab:dataset_comparison}
\begin{tabular}{lcccc}
\hline
\textbf{Dataset} & \textbf{Model} & \textbf{FP32 Acc} & \textbf{INT8 Acc} & \textbf{$\Delta$} \\
\hline
"""

    if 'baseline' in results:
        b = results['baseline']
        latex += f"CIFAR-10 & MobileNetV2 & {b['fp32']['accuracy']:.2f}\\% & {b['int8_qat']['accuracy']:.2f}\\% & {b['int8_qat']['accuracy_degradation']:.2f}\\% \\\\\n"

    if 'fashion_mnist' in results:
        f = results['fashion_mnist']
        latex += f"Fashion-MNIST & SimpleCNN & {f['fp32']['accuracy']:.2f}\\% & {f['int8_ptq']['accuracy']:.2f}\\% & {f['int8_ptq']['accuracy_drop']:.2f}\\% \\\\\n"

    latex += r"""\hline
\end{tabular}
\end{table}
"""

    return latex

def generate_pruning_analysis_table(results):
    """Generate detailed pruning analysis"""
    if 'pruning' not in results:
        return ""

    latex = r"""\begin{table}[h]
\centering
\caption{Pruning Impact Analysis}
\label{tab:pruning_analysis}
\begin{tabular}{lccccc}
\hline
\textbf{Method} & \textbf{Sparsity} & \textbf{Acc (before)} & \textbf{Acc (after)} & \textbf{$\Delta$} & \textbf{Size} \\
\hline
"""

    p = results['pruning']

    for key in ['magnitude_30', 'magnitude_50', 'magnitude_70', 'structured_30', 'structured_50']:
        if key in p:
            data = p[key]
            method = data['method'].replace('_', ' ').title()
            sparsity = f"{data['actual_sparsity']*100:.0f}\\%"
            acc_before = data['accuracy_before_finetune']
            acc_after = data['accuracy_after_finetune']
            drop = data['accuracy_drop']
            size = data['model_size_mb']

            latex += f"{method} & {sparsity} & {acc_before:.2f}\\% & {acc_after:.2f}\\% & {drop:.2f}\\% & {size:.2f} MB \\\\\n"

    latex += r"""\hline
\end{tabular}
\end{table}
"""

    return latex

def main():
    print("="*80)
    print("GENERATING PAPER TABLES")
    print("="*80)

    # Load results
    results = load_results()

    if not results:
        print("❌ No results found. Run experiments first.")
        return

    print(f"\n📊 Loaded results from {len(results)} experiments")

    # Generate tables
    output_dir = Path('experiment_results/paper_tables')
    output_dir.mkdir(parents=True, exist_ok=True)

    tables = {
        'compression_comparison.tex': generate_compression_table(results),
        'architecture_comparison.tex': generate_architecture_table(results),
        'dataset_comparison.tex': generate_dataset_table(results),
        'pruning_analysis.tex': generate_pruning_analysis_table(results)
    }

    # Save tables
    for filename, latex in tables.items():
        if latex:
            output_path = output_dir / filename
            with open(output_path, 'w') as f:
                f.write(latex)
            print(f"  ✅ Generated: {filename}")

    # Create combined file
    combined_path = output_dir / 'all_tables.tex'
    with open(combined_path, 'w') as f:
        f.write("% All experiment tables for Malak Platform paper\n")
        f.write("% Generated automatically from experiment results\n\n")
        for filename, latex in tables.items():
            if latex:
                f.write(f"% {filename}\n")
                f.write(latex)
                f.write("\n\n")

    print(f"\n📁 All tables saved to: {output_dir}/")
    print(f"📄 Combined file: {combined_path}")

    # Generate summary statistics
    print("\n" + "="*80)
    print("SUMMARY STATISTICS")
    print("="*80)

    if 'baseline' in results:
        b = results['baseline']
        print(f"\nCIFAR-10 (MobileNetV2):")
        print(f"  FP32: {b['fp32']['accuracy']:.2f}%")
        print(f"  INT8 QAT: {b['int8_qat']['accuracy']:.2f}% (Δ {b['int8_qat']['accuracy_degradation']:.2f}%)")

    if 'pruning' in results and 'magnitude_30' in results['pruning']:
        p = results['pruning']['magnitude_30']
        print(f"\nPruning (30% sparsity):")
        print(f"  Accuracy: {p['accuracy_after_finetune']:.2f}% (Δ {p['accuracy_drop']:.2f}%)")
        print(f"  Compression: {p['compression_ratio']:.2f}x")

    if 'fashion_mnist' in results:
        f = results['fashion_mnist']
        print(f"\nFashion-MNIST (SimpleCNN):")
        print(f"  FP32: {f['fp32']['accuracy']:.2f}%")
        print(f"  INT8: {f['int8_ptq']['accuracy']:.2f}% (Δ {f['int8_ptq']['accuracy_drop']:.2f}%)")

    print("\n✅ Table generation complete!")

if __name__ == '__main__':
    main()
