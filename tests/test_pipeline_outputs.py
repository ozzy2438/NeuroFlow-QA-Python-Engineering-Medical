from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[1]
PROCESSED_DIR = BASE_DIR / "data" / "processed"
QC_FILE = PROCESSED_DIR / "qc_features_scored_100_subjects.csv"
MANIFEST_FILE = PROCESSED_DIR / "synthetic_mri_fmri_manifest.csv"


def test_manifest_has_expected_subject_count():
    manifest_df = pd.read_csv(MANIFEST_FILE)
    assert len(manifest_df) == 100
    assert manifest_df["subject_id"].is_unique


def test_manifest_paths_exist():
    manifest_df = pd.read_csv(MANIFEST_FILE)
    for column_name in ["t1_path", "fmri_path", "metadata_path"]:
        assert manifest_df[column_name].map(lambda path_value: Path(path_value).exists()).all()


def test_qc_scores_are_valid():
    qc_df = pd.read_csv(QC_FILE)
    assert qc_df["qc_score"].between(0, 100).all()
    assert set(qc_df["qc_status"].unique()).issubset({"pass", "flag"})


def test_flagged_scans_have_reasons():
    qc_df = pd.read_csv(QC_FILE)
    flagged_df = qc_df[qc_df["qc_status"] == "flag"]
    assert len(flagged_df) > 0
    assert flagged_df["qc_fail_reasons"].fillna("").str.len().gt(0).all()
