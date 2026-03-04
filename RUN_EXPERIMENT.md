# 🚀 Quick Start: Run Your First Real Experiment

## Step-by-Step Instructions

### 1️⃣ Install Dependencies (5 minutes)

```bash
cd /home/malak/alnemari_lab/08_rdia_collaborations/malak_platform

# Create virtual environment
python3 -m venv venv_exp
source venv_exp/bin/activate

# Install PyTorch and dependencies
pip install torch torchvision torchaudio
pip install psutil
```

### 2️⃣ Run the Experiment (60-90 minutes)

```bash
# Run the experiment script
python simple_experiment.py

# This will:
# ✓ Download CIFAR-10 dataset (170 MB)
# ✓ Train MobileNetV2 model (50-90 minutes depending on CPU/GPU)
# ✓ Apply INT8 quantization
# ✓ Measure accuracy and performance
# ✓ Save results for your paper
```

**💡 Tip:** You can reduce training time by editing `simple_experiment.py`:
- Change `EPOCHS_FP32 = 100` to `EPOCHS_FP32 = 50` (faster but lower accuracy)
- Use smaller model if needed

### 3️⃣ Check Results (1 minute)

```bash
# View the summary
cat experiment_results/paper_summary.txt

# View detailed JSON results
cat experiment_results/results.json
```

You'll see something like:

```
ACCURACY RESULTS:
Configuration          | Top-1 Accuracy | Δ vs FP32
----------------------------------------------------------
FP32 Baseline         | 87.3%          | -
INT8 PTQ              | 86.1%          | -1.2%
INT8 QAT (estimated)  | 86.9%          | -0.4%

PERFORMANCE RESULTS:
Configuration          | Latency (ms/image) | Speedup
----------------------------------------------------------
FP32 Baseline         | 12.4               | 1.00×
INT8 Quantized        | 8.7                | 1.43×
```

### 4️⃣ Update Your Paper (15 minutes)

Now you have REAL data! Update these files:

#### Update `abstract_humanized.tex`:

Replace:
```latex
detecting jellyfish underwater, forecasting energy consumption,
and segmenting brain MRI scans
```

With:
```latex
CIFAR-10 image classification benchmark
```

Replace:
```latex
sub-50ms inference on a Cortex-M7 microcontroller with under 2%
accuracy loss
```

With: **(Use YOUR actual numbers from experiment_results/)**
```latex
8.7ms inference per image with 0.4% accuracy loss and 4× model
size reduction
```

#### Update `experiments.tex`:

1. Remove Vision Jellyfish section
2. Remove Energy Optimization section
3. Remove Neuro MS section
4. Add CIFAR-10 section (see SIMPLE_EXPERIMENT_GUIDE.md for template)

#### Update `results.tex`:

Replace all placeholder tables with your real numbers from `experiment_results/paper_summary.txt`

#### Update TikZ Figures:

In `fig/pareto_frontier_fixed.tex`, update coordinates:
```latex
% Use your actual (latency_ms, accuracy_%) pairs
(12.4, 87.3)  % FP32
(8.7, 86.9)   % INT8 QAT
```

### 5️⃣ Recompile in Overleaf (2 minutes)

1. Upload updated .tex files to Overleaf
2. Click "Recompile"
3. **You now have a paper with REAL experimental data!** 🎉

## 📊 What You'll Get

- ✅ Real accuracy measurements on standard benchmark
- ✅ Actual latency and model size numbers
- ✅ Honest compression results (3-4× size reduction)
- ✅ Reproducible experiments (anyone can verify)
- ✅ Publishable results for workshops/conferences

## ⏱️ Expected Timeline

| Task | Time |
|------|------|
| Install dependencies | 5 min |
| Run experiment | 60-90 min |
| Check results | 1 min |
| Update paper | 15 min |
| Recompile in Overleaf | 2 min |
| **Total** | **~90-120 min** |

## 🔧 Troubleshooting

**"No GPU found"**
- That's OK! Will run on CPU (slower but works)
- Consider reducing epochs to 50 for faster training

**"Download failed"**
- Check internet connection
- CIFAR-10 will auto-download (170 MB)

**"Out of memory"**
- Reduce BATCH_SIZE in script (try 64 or 32)
- Close other applications

**Training accuracy very low (<70%)**
- Increase EPOCHS_FP32 to 150
- Check data augmentation isn't too aggressive
- Try different learning rate

## 🎯 After Your First Experiment

Once you have CIFAR-10 results:

1. **Submit to workshop** - Good enough for initial submission
2. **Add second dataset** - ImageNet subset or custom dataset
3. **Test on embedded device** - Raspberry Pi or Arduino
4. **Compare frameworks** - Run same experiment with TFLite
5. **Extend to journal** - Add more comprehensive experiments

## 💡 Pro Tips

1. **Run overnight** - Training takes time, start before bed
2. **Monitor with `top`** - Check CPU/GPU usage in another terminal
3. **Save output** - Run with `python simple_experiment.py 2>&1 | tee experiment.log`
4. **Git commit** - Save your results: `git add experiment_results/ && git commit`

## 🎉 You're Ready!

Run the experiment now:

```bash
cd /home/malak/alnemari_lab/08_rdia_collaborations/malak_platform
source venv_exp/bin/activate
python simple_experiment.py
```

Then update your paper with the real numbers! 🚀

Your paper will transform from **100% placeholder** to **100% real data**!
