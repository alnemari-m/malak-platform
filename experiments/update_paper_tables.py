#!/usr/bin/env python3
"""
Update paper tables with real experimental results.

Reads JSON results from experiment_results/ and replaces TBD values
in paper/main_softwarex.tex with measured numbers.

Run after all experiments complete:
    python experiments/update_paper_tables.py
"""

import json
import re
from pathlib import Path

PAPER = Path("paper/main_softwarex.tex")
RESULTS_DIR = Path("experiment_results")


def load_json(path):
    if path.exists():
        with open(path) as f:
            return json.load(f)
    return None


def fmt(val, decimals=2):
    """Format a number for LaTeX."""
    if isinstance(val, float):
        return f"{val:.{decimals}f}"
    return str(val)


def main():
    tex = PAPER.read_text()

    # ── Experiment 1: simple_experiment results ──
    r = load_json(RESULTS_DIR / "results.json")
    if r:
        fp32 = r.get("fp32", r.get("accuracy", {}))
        dptq = r.get("dynamic_ptq", {})
        qat = r.get("qat", {})

        fp32_acc = fp32.get("accuracy", fp32.get("fp32_baseline"))
        fp32_size = fp32.get("model_size_mb", r.get("model", {}).get("fp32_size_mb"))
        dptq_acc = dptq.get("accuracy", r.get("accuracy", {}).get("int8_ptq"))
        dptq_size = dptq.get("model_size_mb", r.get("model", {}).get("int8_size_mb"))
        qat_acc = qat.get("accuracy", r.get("accuracy", {}).get("int8_qat"))
        qat_size = qat.get("model_size_mb")

        if fp32_acc and dptq_acc:
            # Table: CIFAR-10 quantization
            old = r"FP32 Baseline & \textit{TBD} & \textit{TBD} & 1.0$\times$"
            new = f"FP32 Baseline & {fmt(fp32_acc)} & {fmt(fp32_size)} & 1.0$\\times$"
            tex = tex.replace(old, new)

            if dptq_size and fp32_size:
                comp = fp32_size / dptq_size
                old = r"Dynamic PTQ & \textit{TBD} & \textit{TBD} & \textit{TBD}"
                new = f"Dynamic PTQ & {fmt(dptq_acc)} & {fmt(dptq_size)} & {fmt(comp)}$\\times$"
                tex = tex.replace(old, new)

            if qat_acc and qat_size and fp32_size:
                comp = fp32_size / qat_size
                old = r"QAT (20 epochs) & \textit{TBD} & \textit{TBD} & \textit{TBD}"
                new = f"QAT (20 epochs) & {fmt(qat_acc)} & {fmt(qat_size)} & {fmt(comp)}$\\times$"
                tex = tex.replace(old, new)

            # Remove TBD note
            tex = tex.replace(
                r"\noindent\textit{Note: Values marked TBD will be populated after running}"
                "\n" + r"\texttt{experiments/simple\_experiment.py}\textit{, which performs real training and quantization (no hardcoded results).}",
                ""
            )

        print(f"  Updated Experiment 1 (CIFAR-10): FP32={fmt(fp32_acc)}%, DPTQ={fmt(dptq_acc)}%")

    # ── Experiment 2: architecture comparison ──
    r = load_json(RESULTS_DIR / "architectures" / "architecture_comparison.json")
    if r:
        for arch in ["ResNet18", "EfficientNet-B0"]:
            if arch in r:
                d = r[arch]
                fp32_a = d["fp32"]["accuracy"]
                int8_a = d["int8"]["accuracy"]
                drop = d["int8"]["accuracy_drop"]
                comp = d["int8"].get("compression_ratio", 1.0)

                old = f"{arch} & \\textit{{TBD}} & \\textit{{TBD}} & \\textit{{TBD}} & \\textit{{TBD}}"
                new = f"{arch} & {fmt(fp32_a)}\\% & {fmt(int8_a)}\\% & {fmt(drop)}\\% & {fmt(comp)}$\\times$"
                tex = tex.replace(old, new)
                print(f"  Updated {arch}: FP32={fmt(fp32_a)}%, INT8={fmt(int8_a)}%")

    # ── Experiment 3: pruning ──
    r = load_json(RESULTS_DIR / "pruning" / "pruning_results.json")
    if r:
        baseline = r.get("baseline", {})
        if baseline:
            old = r"Baseline (0\%) & \textit{TBD} & --- & 0\%"
            new = f"Baseline (0\\%) & {fmt(baseline['accuracy'])} & --- & 0\\%"
            tex = tex.replace(old, new)

        for pct in [30, 50, 70]:
            key = f"magnitude_{pct}"
            if key in r:
                d = r[key]
                acc = d["accuracy_after_finetune"]
                drop = d["accuracy_drop"]
                sparsity = d["actual_sparsity"] * 100

                old = f"{pct}\\% & \\textit{{TBD}} & \\textit{{TBD}} & \\textit{{TBD}}"
                new = f"{pct}\\% & {fmt(acc)} & {fmt(drop)}\\% & {fmt(sparsity, 1)}\\%"
                tex = tex.replace(old, new)
                print(f"  Updated pruning {pct}%: Acc={fmt(acc)}%, Drop={fmt(drop)}%")

    PAPER.write_text(tex)
    print(f"\nPaper updated: {PAPER}")


if __name__ == "__main__":
    main()
