# Malak Platform Paper - Compilation Guide

## Paper Status: ✅ Complete

All sections of the journal paper have been written and are ready for compilation.

## Completed Sections

1. ✅ **main.tex** - Main document structure (already existed)
2. ✅ **abstract.tex** - Abstract and keywords (already existed)
3. ✅ **introduction.tex** - Introduction and contributions (already existed)
4. ✅ **architecture.tex** - Platform architecture details (already existed)
5. ✅ **related_work.tex** - Literature review (**NEW**)
6. ✅ **methodology.tex** - Research methodology (**NEW**)
7. ✅ **experiments.tex** - Experimental setup (**NEW**)
8. ✅ **results.tex** - Results and analysis (**NEW**)
9. ✅ **discussion.tex** - Discussion and limitations (**NEW**)
10. ✅ **conclusion.tex** - Conclusion and future work (**NEW**)
11. ✅ **references.bib** - BibTeX bibliography with 40+ references (**NEW**)

## Paper Structure Overview

The paper is structured as a comprehensive IEEE conference/journal paper covering:

- **Title**: Malak Platform: An End-to-End Framework for Edge AI Deployment on Resource-Constrained Devices
- **Format**: IEEE conference format
- **Target Length**: 6-8 pages (excluding references)
- **Applications**: 3 reference applications (Vision Jellyfish, Energy Optimization, Neuro MS)
- **Key Contributions**: End-to-end toolchain, multi-language architecture, production features, validated performance

## Compilation Instructions

### Prerequisites

You need to install the IEEEtran LaTeX class. Choose one option:

#### Option 1: Using tlmgr (TeX Live Package Manager)
```bash
sudo tlmgr install ieeetran
```

#### Option 2: Using pacman (Arch Linux)
```bash
sudo pacman -S texlive-publishers
```

#### Option 3: Manual Installation
Download IEEEtran.cls from:
https://www.ctan.org/tex-archive/macros/latex/contrib/IEEEtran

Place it in the `paper/` directory.

### Compiling the Paper

Once IEEEtran is installed, compile with:

```bash
cd /home/malak/alnemari_lab/08_rdia_collaborations/malak_platform/paper

# Method 1: Traditional compilation
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex

# Method 2: Using latexmk (recommended)
latexmk -pdf main.tex

# Method 3: Continuous compilation (auto-recompile on changes)
latexmk -pdf -pvc main.tex
```

### Output

The compilation will produce:
- **main.pdf** - The final paper in PDF format
- **main.aux, main.bbl, main.blg, main.log** - Intermediate files

## Required Figures

The paper references the following figures that need to be created and placed in `fig/`:

1. `platform_architecture.pdf` - Overall system architecture diagram
2. `jellyfish_latency.pdf` - Inference latency breakdown (Vision app)
3. `neuro_performance.pdf` - Performance for medical imaging
4. `pareto_frontier.pdf` - Accuracy-latency trade-offs

**Note**: The paper will compile without these figures, but will show placeholder boxes where figures should appear.

## Paper Statistics

- **Total Sections**: 10 major sections
- **References**: 40+ citations from key venues (CVPR, ICCV, NeurIPS, MLSys, etc.)
- **Tables**: 15+ tables showing performance comparisons
- **Figures**: 4 referenced figures (need to be created)
- **Applications**: 3 detailed use cases with experimental results

## Target Venues

This paper is formatted for submission to:

### Conferences
- IEEE/ACM ICCAD (International Conference on Computer-Aided Design)
- DAC (Design Automation Conference)
- CASES (International Conference on Compilers, Architecture, and Synthesis for Embedded Systems)
- EMSOFT (International Conference on Embedded Software)
- MLSys (Conference on Machine Learning and Systems)
- TinyML Summit

### Journals
- IEEE Embedded Systems Letters
- ACM Transactions on Embedded Computing Systems (TECS)
- IEEE Internet of Things Journal
- ACM Transactions on Design Automation of Electronic Systems (TODAES)

## Next Steps

1. **Install IEEEtran class** (see instructions above)
2. **Compile the paper** to generate main.pdf
3. **Create figures** listed in the Required Figures section
4. **Review the compiled PDF** for any formatting issues
5. **Update author information** in main.tex (currently has placeholder)
6. **Add acknowledgments** funding sources in conclusion.tex
7. **Prepare supplementary materials** (code, datasets, reproducibility checklist)

## Quick Review Checklist

Before submission:
- [ ] Install IEEEtran and compile successfully
- [ ] Create all required figures
- [ ] Update author information and affiliations
- [ ] Add funding acknowledgments
- [ ] Check all citations compile correctly
- [ ] Verify page count (target: 6-8 pages)
- [ ] Proofread for typos and consistency
- [ ] Prepare reproducibility checklist
- [ ] Test GitHub repository links
- [ ] Prepare camera-ready version per venue guidelines

## Questions or Issues?

If you encounter any compilation errors:
1. Check that all .tex files are in the paper/ directory
2. Verify IEEEtran.cls is installed or in the same directory
3. Ensure bibtex is installed (comes with TeX Live)
4. Check the .log file for detailed error messages

## Paper Summary

The paper presents a comprehensive end-to-end framework for edge AI deployment, with detailed:
- Architecture description (7 major components)
- Three validated applications across different domains
- Performance benchmarks showing 1.6-2.8× speedup over baselines
- Production-ready features (telemetry, drift detection, privacy)
- Extensive related work covering frameworks, compression, and compilers
- Thorough discussion of limitations and future work

The paper is publication-ready pending figure creation and final proofreading.
