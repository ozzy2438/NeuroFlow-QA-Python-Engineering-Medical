# NeuroFlow QA - Release Notes

## Version

v1.0-local-portfolio

## What is included

This release contains a synthetic 100-subject brain MRI/fMRI quality assurance project. It includes synthetic NIfTI image files, metadata JSON files, a manifest, extracted QC features, scored QC outputs, summary tables, plots, an HTML report, documentation, a runnable pipeline script, and basic tests.

## Dataset summary

- Synthetic subjects: 100
- Approximate project size: 482.8 MB
- Passed scans: 62
- Flagged scans: 38

## Key outputs

- `README.md`
- `data/processed/synthetic_mri_fmri_manifest.csv`
- `data/processed/qc_features_scored_100_subjects.csv`
- `reports/neuroflow_qa_report.html`
- `reports/qc_score_by_subject.png`
- `reports/qc_fail_reasons.png`
- `src/run_qc_pipeline.py`
- `tests/test_pipeline_outputs.py`

## Known limitations

This project uses synthetic data only. It is not a diagnostic medical device. The quality-control thresholds are explainable engineering rules, not clinically validated thresholds.

## Suggested next phase

Publish code to GitHub, store large imaging data in AWS S3, and optionally run the QC pipeline on AWS EC2 or AWS Batch.
