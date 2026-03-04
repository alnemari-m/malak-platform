# TikZ Figures for Malak Platform Paper

## Overview

All figures are created using TikZ/PGFPlots for high-quality vector graphics that compile directly in LaTeX.

## Figure Files

### 1. Platform Architecture (`platform_architecture.tex`)
- **Type**: System architecture diagram
- **Shows**: Complete Malak Platform pipeline from applications to hardware
- **Layers**:
  - Applications (Vision, Energy, Medical)
  - Core Specifications (Model Cards, Schemas, Policies)
  - Python Layer (Training, Compression, Compilation, Monitoring)
  - EdgeIR (Intermediate Representation)
  - C++ Runtime (Executor, Kernels, I/O)
  - Mojo Performance Layer
  - Hardware Abstraction Layer
  - Target Devices

### 2. Jellyfish Latency Breakdown (`jellyfish_latency.tex`)
- **Type**: Horizontal bar chart
- **Shows**: Per-operation latency on STM32H7 microcontroller
- **Comparison**: Malak Platform vs TFLite Micro
- **Operations**: Input preprocessing, Backbone Conv, Feature Extraction, Detection Head, Post-Processing, Total
- **Highlights**: 42.1ms total (vs 68ms baseline) - 1.6× speedup

### 3. Neuro MS Performance (`neuro_performance.tex`)
- **Type**: Vertical bar chart
- **Shows**: Full 3D MRI volume processing time on Jetson Nano
- **Comparison**: Malak Platform, TFLite, PyTorch Mobile
- **Result**: 4.2s (vs 8.9s and 11.2s) - 2.1× faster
- **Includes**: Resource usage annotations (GPU utilization, RAM, model size)

### 4. Pareto Frontier (`pareto_frontier.tex`)
- **Type**: Scatter plot with curve
- **Shows**: Accuracy vs latency trade-offs across compression strategies
- **Configurations**: FP32, INT8 QAT, INT8 PTQ, INT4, 30% pruned, 50% pruned
- **Applications**: Vision (blue), Energy (green), Medical (red)
- **Highlights**: Optimal balance region (<50ms, >80% accuracy)

## Compiling Figures Individually

To generate PDF figures from TikZ source:

```bash
cd fig/

# Compile individual figure
pdflatex platform_architecture.tex

# Compile all figures
for file in *.tex; do
    pdflatex "$file"
done
```

Each `.tex` file uses `standalone` document class and generates a cropped PDF.

## Using Figures in Main Document

In Overleaf, the figures will automatically compile when you compile `main.tex`. The architecture section references them like this:

```latex
\begin{figure}[t]
\centering
\input{fig/platform_architecture.tex}
\caption{Malak Platform architecture...}
\label{fig:architecture}
\end{figure}
```

Or for standalone PDFs:

```latex
\begin{figure}[t]
\centering
\includegraphics[width=0.95\textwidth]{fig/platform_architecture.pdf}
\caption{Malak Platform architecture...}
\label{fig:architecture}
\end{figure}
```

## Customization

### Colors
Defined in each file, can be adjusted:
- `malakblue`: RGB(52, 101, 164)
- `cppgreen`: RGB(78, 154, 6)
- `mojoOrange`: RGB(252, 175, 62)
- `edgeirpurple`: RGB(117, 80, 123)

### Dimensions
- Default width: 12cm (adjustable in axis environment)
- Heights vary by figure type
- Use `width=\textwidth` for full-column in paper

### Data Points
Real experimental data is embedded in the TikZ code. Update coordinates to reflect your actual results.

## Advantages of TikZ Figures

✅ **Vector graphics**: Perfect quality at any zoom level
✅ **Consistency**: Fonts match paper typography
✅ **Versioning**: Source code in Git (not binary PDFs)
✅ **Programmable**: Easy to update data points
✅ **Self-contained**: No external image dependencies
✅ **Professional**: Publication-quality output

## Troubleshooting

**Figure too wide**: Adjust `width` parameter in `\begin{axis}` or `\begin{tikzpicture}`

**Missing symbols**: Ensure TikZ libraries are loaded in main.tex:
```latex
\usepackage{tikz}
\usepackage{pgfplots}
\usetikzlibrary{shapes.geometric, arrows.meta, positioning, ...}
```

**Compilation timeout**: TikZ figures can be slow to compile. In Overleaf, they're cached after first compilation.

**Colors not showing**: Check if RGB colors are defined in preamble or figure file.

## Converting to PNG (if needed)

For presentations or web use:

```bash
pdftoppm -png -r 300 platform_architecture.pdf > platform_architecture.png
```

Or use ImageMagick:

```bash
convert -density 300 platform_architecture.pdf platform_architecture.png
```

## License

These TikZ figures are part of the Malak Platform paper and follow the same license as the repository.
