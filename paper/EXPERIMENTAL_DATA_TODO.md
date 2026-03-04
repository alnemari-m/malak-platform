# Experimental Data TODO - Replace Placeholder Values

## ⚠️ IMPORTANT: All experimental data in this paper is currently PLACEHOLDER

You need to run actual experiments and replace the example numbers with your real results.

## 📊 Where to Update Experimental Data

### 1. Abstract (`abstract_humanized.tex` or `abstract_clean.tex`)

**Current Placeholder:**
- "sub-50ms inference on Cortex-M7"
- "under 2% accuracy loss"
- "less than 10mJ per inference"

**Action:** Update with your actual measured values

---

### 2. Experiments Section (`experiments.tex`)

#### Vision Jellyfish Dataset (Lines 10-17)
**Placeholder:**
```
Size: 15,000 annotated images (12,000 train, 1,500 validation, 1,500 test)
Classes: 8 jellyfish species + background
Resolution: 320×240 RGB images
```

**Action:** Update with your actual dataset specs
- [ ] Number of images
- [ ] Train/val/test split
- [ ] Number of classes
- [ ] Image resolution

#### Model Architecture (Lines 19-26)
**Placeholder:**
```
Baseline: MobileNetV2-SSDLite (3.2M parameters)
Student: Custom lightweight detector (680K parameters)
```

**Action:** Update with your actual model specs
- [ ] Baseline model name and size
- [ ] Student model name and size
- [ ] Architecture details

#### Energy Optimization Dataset (Lines 46-52)
**Placeholder:**
```
Size: 19,735 samples (4.5 months of 10-minute readings)
Features: 29 inputs
```

**Action:** Update with actual dataset if you have one, or remove this application

#### Neuro MS Dataset (Lines 70-77)
**Placeholder:**
```
Source: ISBI 2015 Longitudinal MS Lesion Segmentation Challenge
Size: 14 patients, 5 timepoints each
```

**Action:** Update with actual dataset or remove this application

---

### 3. Results Section (`results.tex`)

#### Table 1: Vision Jellyfish Accuracy (Lines 9-20)
**ALL PLACEHOLDER DATA:**
```latex
FP32 Baseline         & 82.4\%  & -       \\
INT8 PTQ             & 80.1\%  & -2.3\%  \\
INT8 QAT             & 81.9\%  & -0.5\%  \\
INT4/INT8 QAT        & 79.7\%  & -2.7\%  \\
30\% Pruned + INT8   & 81.2\%  & -1.2\%  \\
50\% Pruned + INT8   & 78.5\%  & -3.9\%  \\
```

**Action:** Run experiments and fill in real accuracy values
- [ ] Train FP32 baseline model
- [ ] Apply INT8 post-training quantization (PTQ)
- [ ] Apply INT8 quantization-aware training (QAT)
- [ ] Try INT4/INT8 mixed precision
- [ ] Test pruning at different sparsity levels
- [ ] Measure accuracy on test set for each configuration

#### Table 2: Vision Jellyfish Performance (Lines 45-54)
**ALL PLACEHOLDER DATA:**
```latex
Malak Platform  & 42 ms   & 8.2 mJ  & 384 KB \\
TFLite Micro    & 68 ms   & 13.1 mJ & 512 KB \\
CMSIS-NN        & 51 ms   & 9.8 mJ  & 420 KB \\
MicroTVM        & 47 ms   & 9.1 mJ  & 440 KB \\
```

**Action:** Benchmark on actual hardware
- [ ] Measure inference latency (milliseconds)
- [ ] Measure energy per inference (millijoules) - need power monitor
- [ ] Measure peak RAM usage (kilobytes)
- [ ] Compare against other frameworks if possible

#### Figure: Jellyfish Latency Breakdown (`fig/jellyfish_latency_fixed.tex`)
**ALL PLACEHOLDER DATA (Lines 30-48):**
```latex
(42.1, 0)  % Total
(2.3, 1)   % Post-Processing
(8.7, 2)   % Detection Head
(15.2, 3)  % Feature Extraction
(12.4, 4)  % Backbone Conv
(3.5, 5)   % Input Pre-Processing
```

**Action:** Profile your model to get per-layer timings
- [ ] Use profiling tools to measure each layer
- [ ] Update coordinates with real millisecond values
- [ ] Ensure they sum to total inference time

#### Table 3: Energy Forecasting Accuracy (Lines 88-95)
**ALL PLACEHOLDER - Update or Remove**

#### Table 4: Energy Performance (Lines 101-110)
**ALL PLACEHOLDER - Update or Remove**

#### Table 5: MS Lesion Segmentation (Lines 135-145)
**ALL PLACEHOLDER - Update or Remove**

#### Figure: Neuro Performance (`fig/neuro_performance_fixed.tex`)
**ALL PLACEHOLDER - Update or Remove**

#### Figure: Pareto Frontier (`fig/pareto_frontier_fixed.tex`)
**ALL PLACEHOLDER DATA (Lines 27-67):**
```latex
% Vision Jellyfish data points
(89, 82.4)   % FP32
(42, 81.9)   % INT8 QAT
(51, 80.1)   % INT8 PTQ
... etc
```

**Action:** Create Pareto plot from your real compression experiments
- [ ] Plot latency vs accuracy for all configurations
- [ ] Update coordinate pairs (latency_ms, accuracy_%)

---

### 4. Discussion Section (`discussion.tex`)

**Multiple placeholder claims throughout:**
- "1.6-2.2× speedup" (Line 30)
- "5-7% accuracy boost" (Line 44)
- "15-25% energy savings" (Line 47)

**Action:** Update all performance claims with real measured values

---

## 🎯 Recommended Approach

### Option 1: Focus on Vision Jellyfish Only (Simplest)
1. **Keep only** the Vision Jellyfish application
2. **Remove** Energy Optimization and Neuro MS sections entirely
3. Run real experiments for jellyfish detection
4. Update only vision-related tables and figures

### Option 2: Use Existing Datasets (Faster)
1. Pick a **public benchmark dataset** (e.g., COCO, ImageNet subset)
2. Train and compress models using your framework
3. Update all experimental data with real results from this dataset
4. Change application description to match dataset

### Option 3: Simulation/Estimation (Not Recommended)
- Use **model analysis tools** to estimate latency/memory
- Note in paper: "estimated" or "projected" performance
- Less convincing for reviewers

---

## 📝 Files to Update with Real Data

| File | What to Update | Priority |
|------|----------------|----------|
| `abstract_humanized.tex` | Performance claims | HIGH |
| `abstract_clean.tex` | Performance claims | HIGH |
| `experiments.tex` | Dataset specs, model sizes | HIGH |
| `results.tex` | All tables with numbers | HIGH |
| `fig/jellyfish_latency_fixed.tex` | Latency breakdown coords | HIGH |
| `fig/pareto_frontier_fixed.tex` | All plot coordinates | HIGH |
| `fig/neuro_performance_fixed.tex` | Bar chart values (or remove) | MEDIUM |
| `discussion.tex` | Performance improvement claims | MEDIUM |
| `conclusion.tex` | Summary of achievements | LOW |

---

## 🔬 Minimum Viable Experiments

To make paper publishable, you need **at minimum**:

### 1. One Working Application
- ✅ Train a model (even simple one)
- ✅ Apply INT8 quantization
- ✅ Deploy on one embedded device
- ✅ Measure: latency, accuracy, memory

### 2. Basic Comparisons
- ✅ Compare FP32 vs INT8 accuracy
- ✅ Compare against ONE baseline (e.g., TFLite Micro)
- ✅ Show it actually works on real hardware

### 3. One Figure with Real Data
- ✅ At least the Pareto frontier (accuracy vs latency)
- Shows trade-offs of your compression approach

---

## 🚀 Quick Start: Replace Placeholder Data

### Step 1: Run Your Experiments
```bash
# Example workflow
python train.py --dataset your_data --model mobilenet
python quantize.py --model model.pth --bits 8
python deploy.py --target stm32h7
python benchmark.py --measure latency,energy,memory
```

### Step 2: Collect Results
Create a spreadsheet with:
- Configuration name (FP32, INT8, INT4, etc.)
- Accuracy (%)
- Latency (ms)
- Energy (mJ)
- Memory (KB)

### Step 3: Update Paper
1. Open `results.tex` in Overleaf
2. Replace placeholder numbers with your real data
3. Update figure coordinates
4. Recompile

---

## 💡 Alternative: Theory/Framework Paper

If you **don't have experimental results yet**, consider:

### Option A: Framework Description Paper
- Focus on **architecture and design**
- Explain **why** your approach is novel
- Show **how** the system works
- Include **implementation details**
- Mark experiments as "future work"

### Option B: Workshop/ArXiv Version
- Submit to workshop (less strict requirements)
- Post on ArXiv as "work in progress"
- Add experiments later for journal version

### Option C: Simulation Results
- Use **model analysis** to estimate performance
- Clearly state these are estimates
- Explain methodology for estimation
- Promise real hardware results in future work

---

## ✅ Action Items Checklist

Before submitting paper:

- [ ] Decide which application(s) to include
- [ ] Run experiments and collect real data
- [ ] Update all placeholder numbers in results.tex
- [ ] Update figure coordinates with real values
- [ ] Update abstract with real performance claims
- [ ] Remove or update Energy/Neuro MS sections if not using
- [ ] Verify all numbers are consistent across sections
- [ ] Add error bars/confidence intervals if possible
- [ ] Include experimental setup details (hardware, software versions)
- [ ] Make sure you can reproduce all numbers

---

## 🎯 Bottom Line

**Current paper status:** Architecture and writing are complete, but **100% of experimental data is placeholder**.

**To publish:** You need to run at least **basic experiments** and replace placeholder numbers with real measurements.

**Fastest path:** Focus on one application, run experiments, update `results.tex` and figure files.

Good luck with your experiments! 🚀
