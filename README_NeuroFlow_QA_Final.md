# NeuroFlow QA

## Synthetic Brain MRI/fMRI Quality Assurance Pipeline on AWS

NeuroFlow QA is a portfolio-ready medical imaging data engineering and quality-assurance project. It simulates a real-world request from a mid-sized hospital or medical imaging centre that wants to reduce manual review effort for MRI/fMRI scan quality checks before downstream analysis.

The project builds an end-to-end pipeline that generates and processes synthetic brain MRI/fMRI data, validates metadata, extracts image-quality features, scores every scan, flags potentially problematic studies, produces QC reports, and demonstrates how the same workflow can be executed in a cloud environment using AWS S3, EC2, IAM, and GitHub.

This project does **not** use real patient data. All imaging files and metadata are synthetic and created only for learning, demonstration, and portfolio purposes.

---

## 1. Business objective

A hospital, research clinic, or neuroimaging centre may receive many MRI/fMRI scans every day. Some scans can be unsuitable for analysis because the patient moved, the signal is unstable, the image is noisy, or the file structure is incomplete. Manually checking every scan is slow and inconsistent.

The objective of NeuroFlow QA is to automate the first layer of MRI/fMRI quality assurance so that technical teams can quickly identify scans that are safe to continue with and scans that need review.

In simple terms:

> The system looks at every synthetic brain scan, measures quality, gives it a score, and marks suspicious scans before a human analyst spends time on them.

---

## 2. Project snapshot

| Item | Value |
|---|---:|
| Synthetic subjects | 100 |
| Approximate project size | 482.8 MB |
| Passed scans | 62 |
| Flagged scans | 38 |
| Main imaging format | NIfTI `.nii.gz` |
| Metadata format | JSON |
| Main language | Python |
| Cloud services used | AWS S3, EC2, IAM |
| CI/CD tool | GitHub Actions |
| Test framework | Pytest |

---

## 3. What this project demonstrates

NeuroFlow QA demonstrates practical skills across medical imaging, data engineering, cloud engineering, and reproducible analytics:

- Medical imaging file handling with NIfTI `.nii.gz` files
- Synthetic MRI/fMRI dataset structure similar to real neuroimaging workflows
- Metadata validation using JSON files
- Feature extraction from imaging arrays using Python and Nibabel
- Rule-based quality scoring and scan flagging
- Batch processing for 100 synthetic subjects
- Reproducible pipeline execution locally and on AWS EC2
- S3-based cloud storage for raw and processed data
- IAM role-based access from EC2 to S3
- GitHub repository structure and GitHub Actions test workflow
- Reporting outputs for technical and non-technical audiences

---

## 4. Dataset design

The project uses synthetic neuroimaging files organised by subject.

Example structure:

```text
neuroflow_qa_project/
  data/
    raw_synthetic/
      sub-001/
        anat/
          sub-001_T1w.nii.gz
        func/
          sub-001_task-rest_bold.nii.gz
        metadata/
          sub-001_dicom_metadata.json
      sub-002/
      ...
    processed/
      synthetic_mri_fmri_manifest.csv
      qc_features_scored_from_script.csv
      qc_status_summary.csv
      qc_fail_reason_summary.csv
  docs/
  reports/
  src/
  tests/
```

### Key file types

| File type | Example | Meaning |
|---|---|---|
| T1-weighted MRI | `sub-001_T1w.nii.gz` | Structural brain image, like a 3D anatomy photo of the brain. |
| Resting-state fMRI | `sub-001_task-rest_bold.nii.gz` | Time-series brain signal file, like a short movie of brain activity. |
| Metadata JSON | `sub-001_dicom_metadata.json` | Scanner and study information such as modality, site, and anonymisation status. |
| Manifest CSV | `synthetic_mri_fmri_manifest.csv` | Index file that tells the pipeline where each subject's files are located. |

---

## 5. Main quality-control features

| Feature | Simple meaning | Why it matters |
|---|---|---|
| `t1_snr` | How clean or noisy the anatomy image is | Noisy anatomy scans can break segmentation and downstream processing. |
| `fmri_tsnr` | How stable the fMRI signal is over time | fMRI is time-based; unstable signal makes analysis unreliable. |
| `motion_mm` | Estimated subject movement | Motion can create fake brain activity patterns. |
| `dvars_proxy` | Sudden signal changes between fMRI frames | Sudden jumps can indicate motion or acquisition artifacts. |
| `brain_volume_ml` | Plausibility of extracted brain-like volume | Helps catch broken files, empty files, or unrealistic image values. |
| `qc_score` | Overall quality score | Simple score for review prioritisation. |
| `qc_status` | Pass or flag decision | Tells the reviewer which scans need attention. |
| `qc_fail_reasons` | Reason for flagging | Explains why a scan was marked for review. |

---

## 6. Pipeline flow

The project follows a simple but professional data pipeline structure.

```text
Synthetic MRI/fMRI files
        ↓
Manifest CSV
        ↓
Python QC pipeline
        ↓
Feature extraction
        ↓
Quality scoring
        ↓
Pass / flag decision
        ↓
CSV summaries + HTML/PNG reports
        ↓
Upload processed outputs back to S3
```

### Step-by-step process

1. **Generate or prepare synthetic imaging files**  
   The project contains synthetic T1 MRI, fMRI, and JSON metadata files for 100 subjects.

2. **Create a manifest file**  
   The manifest works like a map. It stores file paths for each subject so the pipeline knows where to find each scan.

3. **Load imaging files with Python**  
   The pipeline uses Nibabel to open `.nii.gz` neuroimaging files.

4. **Extract QC features**  
   The script calculates quality-related metrics such as SNR, temporal SNR, motion, DVARS-style variation, and brain-volume plausibility.

5. **Score each scan**  
   Each subject receives a QC score and a pass/flag decision.

6. **Generate outputs**  
   The pipeline writes processed CSV files and summary tables.

7. **Run the same process in AWS**  
   Raw synthetic files are stored in S3, processed on EC2, and outputs are uploaded back to S3.

---

## 7. AWS cloud engineering workflow

This project was also tested as a small cloud engineering workflow using AWS.

### AWS services used

| Service | Role in project |
|---|---|
| Amazon S3 | Stores raw synthetic MRI/fMRI files and processed outputs. |
| Amazon EC2 | Runs the Python QC pipeline on a cloud virtual machine. |
| IAM Role | Gives EC2 permission to read from and write to S3 without hard-coded access keys. |
| GitHub | Stores code, documentation, tests, and CI/CD workflow. |
| GitHub Actions | Runs automated checks/tests when code changes. |

### Cloud flow

```text
Local project
   ↓ upload
Amazon S3 bucket
   ↓ sync to EC2
Amazon EC2 instance
   ↓ run Python pipeline
Processed QC results
   ↓ upload back
Amazon S3 processed folder
```

### EC2 execution summary

On the EC2 instance, the following high-level actions were performed:

1. Connected to the EC2 instance using SSH and a `.pem` key pair.
2. Installed or verified Python and pip packages.
3. Cloned the GitHub repository.
4. Synced raw synthetic data from S3 into the EC2 file system.
5. Ran the QC pipeline:

```bash
python3 src/run_qc_pipeline.py
```

6. Confirmed successful execution:

```text
QC pipeline: 100%|█████████████████████████████| 100/100
Saved data/processed/qc_features_scored_from_script.csv
```

7. Uploaded processed outputs back to S3:

```bash
aws s3 cp data/processed/qc_features_scored_from_script.csv s3://<bucket-name>/processed/
aws s3 ls s3://<bucket-name>/processed/
```

---

## 8. Local setup

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Run the pipeline:

```bash
python src/run_qc_pipeline.py
```

Run tests:

```bash
pytest -q
```

---

## 9. Cloud setup summary

### Upload data to S3

```bash
aws s3 sync data/raw_synthetic/ s3://<bucket-name>/raw_synthetic/
aws s3 sync data/processed/ s3://<bucket-name>/processed/
aws s3 sync reports/ s3://<bucket-name>/reports/
```

### Connect to EC2

```bash
chmod 400 ~/Downloads/neuroflow-qa-key.pem
ssh -i ~/Downloads/neuroflow-qa-key.pem ec2-user@<EC2_PUBLIC_IP>
```

### Install dependencies on EC2

```bash
sudo dnf install git python3-pip -y
pip3 install -r requirements.txt
```

### Pull project code

```bash
git clone https://github.com/<username>/<repo-name>.git
cd <repo-name>
```

### Pull data from S3

```bash
mkdir -p data/raw_synthetic data/processed reports
aws s3 sync s3://<bucket-name>/raw_synthetic/ data/raw_synthetic/
aws s3 sync s3://<bucket-name>/processed/ data/processed/
```

### Run pipeline

```bash
python3 src/run_qc_pipeline.py
```

### Push output back to S3

```bash
aws s3 cp data/processed/qc_features_scored_from_script.csv s3://<bucket-name>/processed/
aws s3 ls s3://<bucket-name>/processed/
```

---

## 10. Main outputs

| Output | Purpose |
|---|---|
| `data/processed/synthetic_mri_fmri_manifest.csv` | Master file index for all subjects. |
| `data/processed/qc_features_scored_from_script.csv` | Final EC2-generated scored QC table. |
| `data/processed/qc_status_summary.csv` | Pass vs flag summary. |
| `data/processed/qc_fail_reason_summary.csv` | Reasons why scans were flagged. |
| `reports/neuroflow_qa_report.html` | Portfolio-ready QC report. |
| `reports/qc_score_by_subject.png` | QC score visualisation. |
| `reports/qc_fail_reasons.png` | Failure reason visualisation. |

---

## 11. Results

The pipeline processed 100 synthetic MRI/fMRI subjects.

| Metric | Result |
|---|---:|
| Total synthetic subjects | 100 |
| Passed scans | 62 |
| Flagged scans | 38 |
| Flag rate | 38% |
| Output file generated on EC2 | `qc_features_scored_from_script.csv` |
| Cloud storage verified | S3 raw and processed folders |
| Runtime on EC2 | Completed successfully in seconds |

The result is a reproducible cloud-enabled quality-control workflow that can help imaging teams prioritise scans that need review before downstream research or analytics.

---

## 12. Example interpretation

A row like this:

```text
subject_id = sub-004
qc_score = 70
qc_status = flag
qc_fail_reasons = high_motion
```

means:

> Subject 004 was processed successfully, but the scan should be reviewed because the motion indicator was high.

A row like this:

```text
subject_id = sub-001
qc_score = 100
qc_status = pass
```

means:

> Subject 001 passed the automated quality checks and is suitable for the next processing step.

---

## 13. CI/CD and testing

The repository includes basic automated checks using Pytest and GitHub Actions.

The purpose of this is to show that the project is not just a notebook experiment. It follows a more professional software-engineering structure:

- Source code is version-controlled in GitHub.
- Tests validate key assumptions.
- GitHub Actions can run checks automatically.
- Large medical imaging files are stored in S3 instead of GitHub.

This mirrors a common real-world pattern:

```text
GitHub = code and documentation
S3 = large data files
EC2 = compute environment
IAM = secure access control
```

---

## 14. Why large files are stored in S3, not GitHub

Medical imaging files can be large. GitHub is designed for code, documentation, and small project assets, not large datasets.

Therefore, this project follows a professional structure:

- GitHub stores source code, tests, documentation, and reports.
- AWS S3 stores raw `.nii.gz` imaging data and processed outputs.
- EC2 pulls data from S3 when the pipeline needs to run.

This is closer to how production data science and cloud engineering teams organise projects.

---

## 15. Important disclaimer

This is **not** a diagnostic medical device. It does not detect disease and must not be used for clinical decision-making.

It is a synthetic-data portfolio project designed to demonstrate:

- medical imaging data engineering,
- automated quality assurance,
- Python pipeline development,
- AWS cloud workflow design,
- reproducible reporting,
- and CI/CD awareness.

---

## 16. Resume-friendly project paragraph

Built NeuroFlow QA, an AWS-enabled synthetic brain MRI/fMRI quality-assurance pipeline for a mid-sized medical imaging centre use case. The project used Python, Nibabel, Pandas, AWS S3, EC2, IAM, GitHub, GitHub Actions, and Pytest to process 100 synthetic neuroimaging subjects, extract scan-quality metrics such as SNR, temporal SNR, motion, DVARS-style variation, and brain-volume plausibility, then generate pass/flag decisions and QC reports. The workflow stored large imaging files in S3, executed the pipeline on EC2, and uploaded processed outputs back to cloud storage, flagging 38% of scans for review while allowing 62% to pass automated QC.
