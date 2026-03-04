# Figure Placeholders

This directory should contain the following PDF figures for the paper:

## Required Figures

1. **platform_architecture.pdf** - Overall Malak Platform architecture
   - Shows: Python training, C++ runtime, EdgeIR, compilers, hardware backends
   - Referenced in: architecture.tex (Figure 1)

2. **jellyfish_latency.pdf** - Vision Jellyfish latency breakdown
   - Shows: Per-layer inference time on STM32H7
   - Referenced in: results.tex

3. **neuro_performance.pdf** - Neuro MS performance visualization
   - Shows: Full 3D MRI processing time on Jetson Nano
   - Referenced in: results.tex

4. **pareto_frontier.pdf** - Accuracy vs latency trade-offs
   - Shows: Different compression configurations across applications
   - Referenced in: results.tex

## Creating Placeholder Figures for Overleaf

If you don't have the actual figures yet, you can create simple placeholder PDFs using TikZ in Overleaf or upload blank PDFs.

### Method 1: TikZ Placeholders (in Overleaf)

Create a file `placeholders.tex` in Overleaf with:

```latex
\documentclass{standalone}
\usepackage{tikz}
\begin{document}

\begin{tikzpicture}
\draw (0,0) rectangle (10,6);
\node at (5,3) {\Large Platform Architecture};
\node at (5,2) {(Placeholder - Replace with actual figure)};
\end{tikzpicture}

\end{document}
```

### Method 2: Comment Out Figures Temporarily

In the `.tex` files, temporarily comment out figure includes:
```latex
% \includegraphics[width=0.95\textwidth]{fig/platform_architecture.pdf}
```

### Method 3: Use Draft Mode

Add `draft` option to document class in main.tex:
```latex
\documentclass[conference,draft]{IEEEtran}
```

This will show placeholder boxes instead of figures.

## Figure Specifications

For final submission, create figures with these specifications:
- **Format**: PDF (vector graphics preferred)
- **Resolution**: 300 DPI minimum for raster elements
- **Width**: 3.5 inches (single column) or 7 inches (double column)
- **Fonts**: Embedded, matching paper font (Times/Computer Modern)
- **Colors**: Use grayscale or colorblind-friendly palettes

## Tools for Creating Figures

- **Architecture diagrams**: draw.io, Lucidchart, TikZ
- **Performance plots**: Python (matplotlib), MATLAB, R (ggplot2)
- **Export format**: PDF (vector) preferred over PNG/JPEG
