# Malak Platform Research Paper

This directory contains the LaTeX source for the Malak Platform research paper.

## Structure

- `main.tex` - Main document file
- `abstract.tex` - Abstract and keywords
- `introduction.tex` - Introduction and contributions
- `related_work.tex` - Literature review
- `methodology.tex` - Research methodology
- `architecture.tex` - Platform architecture details
- `experiments.tex` - Experimental setup
- `results.tex` - Results and analysis
- `discussion.tex` - Discussion and limitations
- `conclusion.tex` - Conclusion and future work
- `references.bib` - BibTeX bibliography
- `fig/` - Figures and diagrams directory

## Required Figures

Place the following figures in the `fig/` directory:

1. `platform_architecture.pdf` - Overall system architecture diagram
2. `training_pipeline.pdf` - Training and compression workflow
3. `quantization_comparison.pdf` - Accuracy vs. bit-width analysis
4. `latency_breakdown.pdf` - Per-layer latency profiling
5. `energy_consumption.pdf` - Energy measurements across devices
6. `jellyfish_results.pdf` - Vision application results
7. `energy_app_results.pdf` - Energy optimization results
8. `neuro_ms_results.pdf` - Medical imaging results
9. `memory_footprint.pdf` - RAM/Flash usage comparison
10. `drift_detection.pdf` - Distribution drift visualization

## Compilation

To compile the paper:

```bash
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```

Or use:

```bash
latexmk -pdf main.tex
```

## Target Venues

This paper is structured for submission to:

- IEEE/ACM conferences: ICCAD, DAC, CASES, EMSOFT
- ML conferences: MLSys, TinyML Summit
- Journals: IEEE Embedded Systems Letters, ACM TECS

## Citation

```bibtex
@inproceedings{malak2025platform,
  title={Malak Platform: An End-to-End Framework for Edge AI Deployment on Resource-Constrained Devices},
  author={Your Name},
  booktitle={Conference Name},
  year={2025}
}
```

## Notes

- Follow IEEE conference formatting guidelines
- Maintain 6-8 page limit (excluding references)
- Include reproducibility checklist
- Provide GitHub repository link for code availability
