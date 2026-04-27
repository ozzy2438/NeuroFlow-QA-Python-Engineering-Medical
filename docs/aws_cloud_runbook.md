# AWS Cloud Runbook - NeuroFlow QA

## When to use this

Use this after the local project is complete and you are at your own computer with AWS access configured.

## Recommended simple cloud architecture

For the first cloud version, keep it simple:

1. GitHub stores the code and documentation.
2. AWS S3 stores the large synthetic NIfTI dataset and output artifacts.
3. AWS EC2 or AWS Batch runs the QC pipeline when needed.
4. Optional later step: containerize the pipeline with Docker and run it through AWS Batch.

## Step 1 - Prepare local machine

Install Python 3.11 or newer, Git, AWS CLI, and Docker if you want container support later.

## Step 2 - Configure AWS credentials

Run:

```bash
aws configure
```

Use an IAM user or IAM Identity Center profile with limited permissions. Avoid root account credentials.

## Step 3 - Create S3 buckets

Suggested buckets:

```text
neuroflow-qa-code-or-artifacts
neuroflow-qa-synthetic-data
```

Recommended S3 layout:

```text
s3://neuroflow-qa-synthetic-data/raw_synthetic/
s3://neuroflow-qa-synthetic-data/processed/
s3://neuroflow-qa-synthetic-data/reports/
```

## Step 4 - Upload large data to S3

From inside the project folder:

```bash
aws s3 sync data/raw_synthetic s3://neuroflow-qa-synthetic-data/raw_synthetic/
aws s3 sync data/processed s3://neuroflow-qa-synthetic-data/processed/
aws s3 sync reports s3://neuroflow-qa-synthetic-data/reports/
```

## Step 5 - Put code on GitHub

Recommended approach:

- Keep code, README, docs, tests, and small CSV summaries in GitHub.
- Do not commit the full 480MB+ dataset to GitHub.
- Store large NIfTI files in S3.
- Add a note in README explaining where cloud data lives.

## Step 6 - Run on EC2 first

EC2 is the simplest first compute option.

Basic idea:

```bash
git clone <your-repo-url>
cd neuroflow_qa_project
python -m pip install -r requirements.txt
aws s3 sync s3://neuroflow-qa-synthetic-data/raw_synthetic/ data/raw_synthetic/
aws s3 sync s3://neuroflow-qa-synthetic-data/processed/ data/processed/
python src/run_qc_pipeline.py
aws s3 sync data/processed s3://neuroflow-qa-synthetic-data/processed/
aws s3 sync reports s3://neuroflow-qa-synthetic-data/reports/
```

## Step 7 - Upgrade later to AWS Batch

Once EC2 works, package the pipeline as a Docker image and run it with AWS Batch. AWS Batch is better when you want repeatable jobs, queueing, and larger batch workloads.

## Step 8 - Security notes

- Do not upload real patient data.
- Do not publish AWS keys.
- Use least-privilege IAM permissions.
- Keep buckets private by default.
- If you ever use real data, you need proper governance, consent, de-identification, access logging, and compliance review.

## Suggested cloud demo story

The cloud story should be: code in GitHub, large imaging data in S3, compute on EC2 first, then Batch later. This is realistic, simple, and interview-friendly.
