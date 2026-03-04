# GitHub Repository Setup for Paper Submission

## ⚠️ Current Status

**Repository URL**: https://github.com/alnemari-m/malak_platform
**Status**: Not publicly accessible (404 error)

The paper's conclusion section references this URL for code availability. **You must create and populate this repository before submitting the paper**, as reviewers will verify code availability.

---

## 📋 Required Steps

### 1. Create Repository (if not exists)

1. Go to https://github.com/alnemari-m
2. Click "New repository"
3. Repository name: `malak_platform`
4. **Make it PUBLIC** (required for paper submission)
5. Add description: "Malak Platform: End-to-End Framework for Edge AI Deployment"
6. Initialize with README

### 2. Repository Structure

Create the following directory structure:

```
malak_platform/
├── README.md                    ← Overview and quick start
├── LICENSE                      ← Open source license (MIT recommended)
├── requirements.txt             ← Python dependencies
├── setup.py                     ← Package installation
│
├── malak/                       ← Main platform code
│   ├── __init__.py
│   ├── training/
│   ├── quantization/
│   ├── compiler/
│   └── runtime/
│
├── experiments/
│   ├── simple_experiment.py    ← CIFAR-10 reproduction script
│   ├── README.md               ← How to reproduce results
│   └── requirements.txt
│
├── models/                      ← Pre-trained models
│   ├── cifar10_fp32.pth
│   ├── cifar10_int8.pth
│   └── README.md
│
├── docs/
│   ├── installation.md
│   ├── quickstart.md
│   ├── architecture.md
│   └── api_reference.md
│
├── paper/                       ← Paper source files
│   ├── main_fixed.tex
│   ├── experiments_REAL.tex
│   └── figures/
│
└── .gitignore
```

---

## 🔧 Quick Setup Commands

### Option 1: Initialize from Current Directory

```bash
cd /home/malak/alnemari_lab/08_rdia_collaborations/malak_platform

# Initialize git repository
git init
git remote add origin https://github.com/alnemari-m/malak_platform.git

# Create basic structure
mkdir -p malak experiments models docs paper/figures

# Copy experiment script
cp simple_experiment.py experiments/

# Copy paper files
cp paper/*.tex paper/
cp paper/fig/*.tex paper/figures/

# Create README
cat > README.md << 'EOF'
# Malak Platform

End-to-End Framework for Edge AI Deployment on Resource-Constrained Devices

## Overview

Malak Platform provides a unified toolchain for deploying deep neural networks on edge devices, integrating training, compression, compilation, and runtime in a single framework.

## Quick Start

```bash
pip install -r requirements.txt
python experiments/simple_experiment.py
```

## Reproducing Paper Results

See [experiments/README.md](experiments/README.md) for instructions to reproduce the CIFAR-10 results reported in our paper.

## Citation

If you use Malak Platform in your research, please cite:

```bibtex
@article{malak2026,
  title={Malak Platform: An End-to-End Framework for Edge AI Deployment on Resource-Constrained Devices},
  author={[Your Name]},
  journal={[Journal Name]},
  year={2026}
}
```

## License

MIT License (see LICENSE file)
EOF

# Create .gitignore
cat > .gitignore << 'EOF'
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
.env
.venv
env/
venv/
*.pth
data/
experiment_results/
*.log
.DS_Store
EOF

# Create requirements.txt
cat > requirements.txt << 'EOF'
torch>=2.0.0
torchvision>=0.15.0
numpy>=1.24.0
tqdm>=4.65.0
EOF

# Add all files
git add .
git commit -m "Initial commit: Malak Platform with CIFAR-10 validation"

# Push to GitHub (requires authentication)
git push -u origin main
```

### Option 2: Create on GitHub First, Then Clone

```bash
# Create repository on GitHub website first
# Then clone:
git clone https://github.com/alnemari-m/malak_platform.git
cd malak_platform

# Copy files
cp -r /home/malak/alnemari_lab/08_rdia_collaborations/malak_platform/simple_experiment.py experiments/
cp -r /home/malak/alnemari_lab/08_rdia_collaborations/malak_platform/paper .

# Add, commit, push
git add .
git commit -m "Add CIFAR-10 experiment and paper"
git push
```

---

## 📄 Essential Files to Include

### 1. Experiment Reproduction Script
**File**: `experiments/simple_experiment.py`
**Source**: Already created at `/home/malak/alnemari_lab/08_rdia_collaborations/malak_platform/simple_experiment.py`

### 2. Experiment README
**File**: `experiments/README.md`

```markdown
# Reproducing Paper Results

## CIFAR-10 Image Classification

This experiment validates the Malak Platform quantization pipeline.

### Requirements
```bash
pip install torch torchvision numpy tqdm
```

### Run Experiment
```bash
python simple_experiment.py
```

### Expected Results
- **FP32 Baseline**: ~89.28% accuracy
- **INT8 PTQ**: ~89.26% accuracy (-0.02%)
- **INT8 QAT**: ~88.78% accuracy (-0.50%)
- **Inference Latency**: ~0.67 ms/image (CPU)

### Hardware
Tested on:
- CPU: Intel/AMD x86_64
- RAM: 8GB minimum
- Storage: 2GB for dataset + models

### Runtime
- Training: ~2-3 hours on CPU
- Quantization: ~5 minutes
- Total: ~3 hours
```

### 3. Pre-trained Models (Optional but Recommended)
Upload the trained models from `experiment_results/`:
- `model_fp32_best.pth`
- `model_int8_ptq.pth`

Use Git LFS for large files:
```bash
git lfs install
git lfs track "*.pth"
git add .gitattributes
```

### 4. LICENSE File
Recommended: MIT License

```
MIT License

Copyright (c) 2026 [Your Name]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction...
```

---

## ✅ Verification Checklist

Before submitting the paper, verify:

- [ ] Repository is **PUBLIC** (not private)
- [ ] URL https://github.com/alnemari-m/malak_platform is accessible
- [ ] README.md explains project and provides quick start
- [ ] `experiments/simple_experiment.py` is included
- [ ] `experiments/README.md` has reproduction instructions
- [ ] `requirements.txt` lists all dependencies
- [ ] Paper LaTeX sources included in `paper/` directory
- [ ] LICENSE file added (MIT or Apache 2.0 recommended)
- [ ] .gitignore prevents committing large data files
- [ ] (Optional) Pre-trained models uploaded with Git LFS
- [ ] Test: Clone fresh copy and run experiment successfully

---

## 🔗 Testing Repository Access

After setup, test that reviewers can access it:

```bash
# Incognito/private browser window
curl -I https://github.com/alnemari-m/malak_platform

# Should return: HTTP/2 200
# If returns 404, repository is not public
```

---

## 📊 What Reviewers Will Check

Reviewers typically verify:

1. **Repository exists and is public** ✓
2. **Code matches paper claims** ✓
3. **Dependencies clearly listed** ✓
4. **Reproduction instructions provided** ✓
5. **License allows academic use** ✓
6. **README is informative** ✓

---

## ⏰ Timeline

**CRITICAL**: Set up repository **BEFORE** paper submission.

Many journals require code availability statements to include working URLs. A 404 error will raise red flags during review.

### Suggested Timeline:
1. **Day 1**: Create repository, upload basic structure
2. **Day 2**: Add experiment script and README
3. **Day 3**: Test reproduction on clean environment
4. **Day 4**: Upload paper sources
5. **Day 5**: Final verification and paper submission

---

## 🆘 Need Help?

### GitHub Authentication Issues
If push fails with authentication error:
```bash
# Generate personal access token
# Go to: GitHub Settings → Developer settings → Personal access tokens
# Use token as password when pushing
```

### Git LFS for Large Models
```bash
# Install Git LFS
git lfs install

# Track large files
git lfs track "*.pth"
git lfs track "*.onnx"

# Commit and push
git add .gitattributes
git commit -m "Add LFS tracking"
git push
```

---

## 📝 Summary

**Current Issue**: Paper references GitHub repository that doesn't exist publicly.

**Solution**: Create and populate repository with:
- Experiment reproduction script
- Documentation
- License
- Paper sources

**Priority**: HIGH - Required before paper submission

**Estimated Time**: 2-3 hours to set up properly

---

**Status**: 🔴 REPOSITORY SETUP REQUIRED
**URL**: https://github.com/alnemari-m/malak_platform (currently 404)
