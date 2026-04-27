# GitHub Handoff Guide - NeuroFlow QA

## What to upload to GitHub

Upload the code-only project contents, not the full raw synthetic imaging dataset.

Recommended GitHub contents:

- README.md
- requirements.txt
- src/
- tests/
- docs/
- reports/
- data/processed/
- .github/workflows/
- .gitignore

## What not to upload directly to GitHub

Do not upload `data/raw_synthetic/` directly to GitHub. It contains the large synthetic NIfTI files and makes the repository unnecessarily heavy.

## Where to keep the large data

For the cloud phase, keep large image files in AWS S3. The README can explain that the full dataset is available as a release artifact or in S3.

## Suggested first GitHub commands

```bash
git init
git add README.md requirements.txt src tests docs reports data/processed .github .gitignore
git commit -m "Initial NeuroFlow QA portfolio release"
git branch -M main
git remote add origin <your-github-repo-url>
git push -u origin main
```

## Suggested repository description

Synthetic brain MRI/fMRI quality-assurance pipeline with NIfTI data handling, metadata validation, QC scoring, reporting, tests, and cloud-ready structure.

## Suggested GitHub topics

medical-imaging, neuroimaging, mri, fmri, nifti, healthcare-ai, data-engineering, quality-control, python, portfolio-project
