# Malak Platform Paper - TikZ + Humanized Writing Edition

## 🎨 What's New

This updated version includes:
- ✅ **TikZ Figures**: All 4 figures created as vector graphics (no external PDFs needed!)
- ✅ **Humanized Writing**: More natural, engaging writing style (optional - you can use original too)
- ✅ **Auto-Compilation**: Figures compile directly in LaTeX
- ✅ **Professional Quality**: Publication-ready vector graphics

## 📦 Files Included

### LaTeX Files
- `main_updated.tex` - Main document with TikZ support (USE THIS ONE)
- `abstract_humanized.tex` - Conversational abstract
- `introduction_humanized.tex` - Engaging introduction
- `abstract.tex` - Original academic abstract
- `introduction.tex` - Original academic introduction
- All other section files (unchanged)

### TikZ Figures (in `fig/` directory)
- `platform_architecture.tex` - Complete system diagram
- `jellyfish_latency.tex` - Performance bar chart
- `neuro_performance.tex` - Medical app benchmark
- `pareto_frontier.tex` - Accuracy-latency trade-off plot

### Documentation
- `README_TIKZ.md` - TikZ figure documentation
- This guide

## 🚀 Upload to Overleaf

### Step 1: Create ZIP for Upload

```bash
cd /home/malak/alnemari_lab/08_rdia_collaborations/malak_platform
# ZIP file will be created with command below
```

### Step 2: Upload to Overleaf

1. Go to https://www.overleaf.com
2. Click "New Project" → "Upload Project"
3. Upload the ZIP file
4. Wait for extraction

### Step 3: Configure Project

1. Click menu icon (☰)
2. **Set Main document:** `main_updated.tex` ⚠️ IMPORTANT
3. **Set Compiler:** pdfLaTeX
4. **Set TeX Live version:** 2024 or 2025
5. Click "Recompile"

## 🎯 Choosing Writing Style

The updated main.tex gives you two options:

### Option 1: Humanized (Conversational, Engaging) - DEFAULT
```latex
\input{abstract_humanized}
\input{introduction_humanized}
```

**Writing style:**
- More natural and conversational
- Uses "we" and "you"
- Engaging tone with metaphors
- Still academically rigorous

**Example:** *"Getting deep learning models to run efficiently on tiny embedded devices is surprisingly hard..."*

### Option 2: Original (Traditional Academic)
```latex
\input{abstract}
\input{introduction}
```

**Writing style:**
- Formal academic tone
- Traditional phrasing
- More passive voice
- Standard conference style

**Example:** *"Edge AI deployment on resource-constrained devices presents significant challenges..."*

**To switch:** Edit `main_updated.tex` and uncomment/comment the appropriate lines.

## 🖼️ How TikZ Figures Work

### Advantages
✅ **Vector graphics** - Perfect at any zoom level
✅ **Self-contained** - No external image files
✅ **Consistent fonts** - Matches paper typography
✅ **Easy to update** - Just edit coordinates
✅ **Version control** - Source code, not binaries

### Compilation
When you click "Recompile" in Overleaf:
1. LaTeX processes `main_updated.tex`
2. When it hits `\input{fig/platform_architecture.tex}`, it compiles the TikZ code
3. Figure is rendered directly in the PDF
4. First compilation takes ~30-60 seconds (TikZ is thorough!)
5. Subsequent compilations are faster (cached)

### Customizing Figures

All figures are in `fig/*.tex` - you can edit them directly in Overleaf:

**Change colors:**
```latex
\definecolor{malakblue}{RGB}{52, 101, 164}  % Adjust RGB values
```

**Update data:**
```latex
\addplot coordinates {
    (42.1, 0)  % Change these numbers
    (2.3, 1)
    ...
};
```

**Resize:**
Figures auto-resize with `\resizebox` in main tex files. No changes needed!

## 📊 Expected Compilation Time

| Component | First Compile | Subsequent |
|-----------|---------------|------------|
| Text sections | ~5 sec | ~2 sec |
| TikZ figures | ~30 sec | ~3 sec (cached) |
| Bibliography | ~5 sec | ~2 sec |
| **Total** | **~60 sec** | **~15 sec** |

Don't panic if first compilation takes a minute - that's normal for TikZ!

## ⚠️ Troubleshooting

### "Undefined control sequence" in figures
**Solution:** Make sure `main_updated.tex` is set as main document (not `main.tex`)

### Figures not showing
**Solution:** Check that:
1. TikZ libraries are loaded in preamble
2. PGFPlots package is included
3. Fig files are in `fig/` directory

### Compilation timeout (Overleaf free tier)
**Solution:**
- First compile might timeout - just click "Recompile"
- Figures are cached after first successful compile
- Or upgrade to Overleaf premium

### Want traditional academic tone?
**Solution:** Edit `main_updated.tex`:
```latex
% Comment out these lines:
% \input{abstract_humanized}
% \input{introduction_humanized}

% Uncomment these:
\input{abstract}
\input{introduction}
```

## 🎨 Customization Examples

### Make a figure bigger
In `main_updated.tex` or section files, change:
```latex
\resizebox{0.48\textwidth}{!}{\input{fig/jellyfish_latency.tex}}
```
to:
```latex
\resizebox{0.7\textwidth}{!}{\input{fig/jellyfish_latency.tex}}
```

### Change figure colors
Edit the `.tex` file in `fig/` directory. For example, in `platform_architecture.tex`:
```latex
\definecolor{pythonblue}{RGB}{52, 101, 164}     % Current
\definecolor{pythonblue}{RGB}{0, 120, 215}      % Change to this
```

### Export figures as PDFs
In Overleaf, you can't easily compile standalone figures. Instead:
1. Download project source
2. Locally run: `pdflatex fig/platform_architecture.tex`
3. You'll get a cropped PDF of just that figure

## 📝 Comparison: Original vs Humanized

| Aspect | Original | Humanized |
|--------|----------|-----------|
| Tone | Formal, passive | Conversational, active |
| Pronouns | "This paper", "The framework" | "We", "You", "Our" |
| Metaphors | Minimal | Used for clarity |
| Jargon | Technical terms upfront | Explained contextually |
| Readability | Standard academic | Easier, more engaging |
| Rigor | High | High (maintained) |

Both versions are academically sound - choose based on venue and preference!

## 🎓 Recommended Usage

### For Traditional Venues (IEEE, ACM conferences)
Use **original** abstract/intro - they expect formal tone

### For Workshops, Posters, ArXiv
Use **humanized** - more accessible and engaging

### For Hybrid Approach
- Use original abstract (first impression for reviewers)
- Use humanized intro (hooks readers)
- Mix and match sections as needed

## 🔧 Advanced Tips

### Compile just one figure
Create a test file:
```latex
\documentclass{article}
\usepackage{tikz}
\usepackage{pgfplots}
\begin{document}
\input{fig/platform_architecture.tex}
\end{document}
```

### Change citation style
All citations in `references.bib` work with both writing styles.

### Add your own TikZ figure
1. Create new `.tex` file in `fig/`
2. Use `\documentclass[tikz,border=10pt]{standalone}`
3. Reference with `\input{fig/yourfigure.tex}`

## 📞 Quick Reference

| Task | Command/Location |
|------|------------------|
| Set main file | Menu → Main document → `main_updated.tex` |
| Change style | Edit `main_updated.tex` lines 28-34 |
| Edit figure | Open `fig/*.tex` files |
| Update data | Edit coordinates in figure files |
| View compilation log | Click log icon near "Recompile" |
| Download PDF | Click "Download PDF" button |

## ✅ Final Checklist

Before submitting:
- [ ] Compiled successfully in Overleaf
- [ ] All 4 figures rendering correctly
- [ ] Chose writing style (humanized vs original)
- [ ] Updated author information in `main_updated.tex`
- [ ] Checked all citations compile
- [ ] Verified page count (6-8 pages target)
- [ ] Proofread for typos
- [ ] Downloaded final PDF

## 🎉 You're All Set!

Your paper now has:
- ✅ Beautiful TikZ vector graphics
- ✅ Choice of writing styles
- ✅ All sections complete
- ✅ 40+ quality references
- ✅ Ready for submission

Upload to Overleaf and watch it compile into a publication-ready paper! 🚀
