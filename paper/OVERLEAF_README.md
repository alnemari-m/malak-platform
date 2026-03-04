# Malak Platform Paper - Overleaf Upload Guide

## 📦 Files Ready for Overleaf

All paper files are ready to upload to Overleaf. This guide will help you set up the project.

## 📋 Required Files Checklist

### Core LaTeX Files (✅ All Present)
- [x] `main.tex` - Main document
- [x] `abstract.tex` - Abstract and keywords
- [x] `introduction.tex` - Introduction
- [x] `related_work.tex` - Literature review
- [x] `methodology.tex` - Research methodology
- [x] `architecture.tex` - System architecture
- [x] `experiments.tex` - Experimental setup
- [x] `results.tex` - Results and analysis
- [x] `discussion.tex` - Discussion
- [x] `conclusion.tex` - Conclusion
- [x] `references.bib` - Bibliography (40+ references)

### Figures Directory
- [x] `fig/` - Directory for figures (create placeholder PDFs if needed)

## 🚀 Overleaf Setup Instructions

### Method 1: Upload ZIP File (Recommended)

1. **Create a ZIP file** containing all paper files:
   ```bash
   cd /home/malak/alnemari_lab/08_rdia_collaborations/malak_platform
   zip -r malak_paper.zip paper/*.tex paper/*.bib paper/fig/
   ```

2. **Go to Overleaf**: https://www.overleaf.com

3. **Create New Project**:
   - Click "New Project" → "Upload Project"
   - Upload `malak_paper.zip`
   - Overleaf will automatically extract and set up the project

4. **Set Main Document**:
   - In Overleaf, click the menu icon (☰)
   - Under "Main document", select `main.tex`

5. **Set Compiler**:
   - In the menu, set "Compiler" to **pdfLaTeX**
   - Set "TeX Live version" to **2024** or **2025** (latest)

### Method 2: Manual Upload

1. **Create New Project** in Overleaf:
   - Click "New Project" → "Blank Project"
   - Name it "Malak Platform Paper"

2. **Upload Files One by One**:
   - Click "Upload" button
   - Upload all `.tex` files
   - Upload `references.bib`

3. **Create fig/ Directory**:
   - Click "New Folder"
   - Name it `fig`

4. **Set Main Document** to `main.tex`

### Method 3: GitHub Integration (Advanced)

1. **Push to GitHub**:
   ```bash
   cd /home/malak/alnemari_lab/08_rdia_collaborations/malak_platform
   git add paper/
   git commit -m "Add complete journal paper"
   git push
   ```

2. **Import from GitHub** in Overleaf:
   - Click "New Project" → "Import from GitHub"
   - Select your repository
   - Overleaf will sync with GitHub

## ⚙️ Overleaf Configuration

Once uploaded, configure these settings:

### Compiler Settings
- **Compiler**: pdfLaTeX
- **TeX Live version**: 2024 or 2025
- **Main document**: main.tex

### Build Process
Overleaf automatically runs:
1. pdfLaTeX (first pass)
2. BibTeX (process references)
3. pdfLaTeX (second pass - resolve citations)
4. pdfLaTeX (third pass - resolve cross-references)

No manual intervention needed!

## 📊 Project Structure in Overleaf

```
malak_paper/
├── main.tex              # Main document (set as main)
├── abstract.tex          # Abstract section
├── introduction.tex      # Introduction
├── related_work.tex      # Literature review
├── methodology.tex       # Methodology
├── architecture.tex      # Architecture
├── experiments.tex       # Experiments
├── results.tex          # Results
├── discussion.tex       # Discussion
├── conclusion.tex       # Conclusion
├── references.bib       # Bibliography
└── fig/                 # Figures directory
    ├── README.md        # Figures documentation
    └── (add PDFs here)
```

## 🎨 Creating Placeholder Figures

If you don't have figures yet, create placeholders to avoid compilation warnings:

### Option 1: Using Overleaf's Built-in Tools
1. In Overleaf, create a new file in `fig/`
2. Use TikZ to create simple placeholder boxes

### Option 2: Upload Blank PDFs
Create blank PDFs locally and upload to `fig/`:
- `platform_architecture.pdf`
- `jellyfish_latency.pdf`
- `neuro_performance.pdf`
- `pareto_frontier.pdf`

### Option 3: Comment Out Figures Temporarily
In each `.tex` file, comment out `\includegraphics` lines:
```latex
% \includegraphics[width=0.48\textwidth]{fig/platform_architecture.pdf}
```

## ✅ Compilation Checklist

Before sharing or submitting:

- [ ] All `.tex` files uploaded
- [ ] `references.bib` uploaded
- [ ] Main document set to `main.tex`
- [ ] Compiler set to pdfLaTeX
- [ ] Paper compiles without errors
- [ ] All citations resolve correctly
- [ ] Figures uploaded (or placeholders created)
- [ ] Author information updated in `main.tex`
- [ ] Acknowledgments added in `conclusion.tex`

## 🔧 Troubleshooting

### IEEEtran Class Not Found
**Solution**: Overleaf includes IEEEtran by default. If it fails:
1. Menu → TeX Live version → Select 2024 or 2025
2. If still failing, download `IEEEtran.cls` and upload to project root

### Bibliography Not Showing
**Solution**:
1. Ensure `references.bib` is uploaded
2. Check that `\bibliography{references}` in `main.tex` is correct
3. Click "Recompile" button to run full build cycle

### Figures Not Displaying
**Solution**:
1. Check that figure files are in `fig/` directory
2. Verify file names match exactly (case-sensitive)
3. Ensure PDFs are not corrupted

### Compile Timeout
**Solution**:
1. Overleaf free tier has 60-second timeout
2. This paper should compile in ~10-20 seconds
3. If timing out, try commenting out sections temporarily

## 🌐 Sharing Your Overleaf Project

### Share Link (View Only)
1. Click "Share" button
2. Choose "Turn on link sharing"
3. Set to "View only" or "Edit"
4. Copy link to share with collaborators

### Download PDF
1. Click "Download PDF" button
2. Save to your computer
3. Submit to conference/journal

### Export Source
1. Menu → "Source" → "Download source"
2. Downloads ZIP of all project files
3. Use for final submission or archival

## 📝 Collaboration Tips

### Multiple Authors
1. Invite co-authors: Share → Enter email → Set permissions
2. Track changes: Use "Review" mode
3. Comments: Add comments inline for discussions
4. Version history: Menu → History (view past versions)

### Real-time Editing
- Overleaf shows who's editing in real-time
- Changes sync automatically
- Conflicts resolved automatically

## 🎯 Next Steps After Upload

1. **Compile and verify** - Ensure paper compiles successfully
2. **Update author info** - Edit `main.tex` with your details
3. **Create figures** - Add actual figures or use placeholders
4. **Review content** - Proofread all sections
5. **Check page count** - Should be 6-8 pages for conferences
6. **Prepare submission** - Download PDF when ready

## 📞 Support

- **Overleaf Documentation**: https://www.overleaf.com/learn
- **LaTeX Help**: https://tex.stackexchange.com
- **IEEEtran Guide**: https://www.ctan.org/pkg/ieeetran

## 🎉 You're Ready!

Your Malak Platform paper is fully prepared for Overleaf. Simply:
1. Create ZIP file (or use manual upload)
2. Upload to Overleaf
3. Set main.tex as main document
4. Click "Recompile"
5. Download your PDF!

Good luck with your publication! 🚀
