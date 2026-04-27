from pathlib import Path
import numpy as np
import pandas as pd
import nibabel as nib
from tqdm.auto import tqdm

BASE_DIR = Path(__file__).resolve().parents[1]
PROCESSED_DIR = BASE_DIR / "data" / "processed"
MANIFEST = PROCESSED_DIR / "synthetic_mri_fmri_manifest.csv"
OUT = PROCESSED_DIR / "qc_features_scored_from_script.csv"

THRESHOLDS = {"t1_snr_min": 1.40, "fmri_tsnr_min": 3.50, "dvars_proxy_max": 0.130, "motion_mm_max": 0.40, "brain_volume_min_ml": 260, "brain_volume_max_ml": 380}

def extract_features(row_vals):
    t1_img = nib.load(row_vals["t1_path"])
    fmri_img = nib.load(row_vals["fmri_path"])
    t1_data = t1_img.get_fdata(dtype=np.float32)
    fmri_data = fmri_img.get_fdata(dtype=np.float32)
    t1_nonzero = t1_data[t1_data > 0]
    t1_snr = float(np.mean(t1_nonzero) / np.std(t1_nonzero))
    voxel_volume = float(np.prod(t1_img.header.get_zooms()[:3]))
    brain_volume_ml = float(np.sum(t1_data > 0.15) * voxel_volume / 1000)
    fmri_mean = np.mean(fmri_data, axis=3)
    fmri_std = np.std(fmri_data, axis=3)
    mask = fmri_mean > 0.15
    fmri_tsnr = float(np.mean((fmri_mean / (fmri_std + 1e-6))[mask]))
    diff_data = np.diff(fmri_data, axis=3)
    dvars_proxy = float(np.mean(np.sqrt(np.mean(diff_data[mask, :] ** 2, axis=0))))
    return t1_snr, brain_volume_ml, fmri_tsnr, dvars_proxy

def score_row(row_vals):
    reasons = []
    if row_vals["t1_snr"] < THRESHOLDS["t1_snr_min"]: reasons.append("low_t1_snr")
    if row_vals["fmri_tsnr"] < THRESHOLDS["fmri_tsnr_min"]: reasons.append("low_fmri_tsnr")
    if row_vals["dvars_proxy"] > THRESHOLDS["dvars_proxy_max"]: reasons.append("high_temporal_variation")
    if row_vals["motion_mm"] > THRESHOLDS["motion_mm_max"]: reasons.append("high_motion")
    if row_vals["brain_volume_ml"] < THRESHOLDS["brain_volume_min_ml"] or row_vals["brain_volume_ml"] > THRESHOLDS["brain_volume_max_ml"]: reasons.append("unexpected_brain_volume")
    score = 100 - 20 * ("low_t1_snr" in reasons) - 25 * ("low_fmri_tsnr" in reasons) - 20 * ("high_temporal_variation" in reasons) - 30 * ("high_motion" in reasons) - 15 * ("unexpected_brain_volume" in reasons)
    return max(int(score), 0), "pass" if len(reasons) == 0 else "flag", ",".join(reasons)

def main():
    manifest_df = pd.read_csv(MANIFEST)
    rows = []
    for _, row_vals in tqdm(manifest_df.iterrows(), total=len(manifest_df), desc="QC pipeline"):
        t1_snr, brain_volume_ml, fmri_tsnr, dvars_proxy = extract_features(row_vals)
        output_row = dict(row_vals)
        output_row.update({"t1_snr": round(t1_snr, 3), "brain_volume_ml": round(brain_volume_ml, 2), "fmri_tsnr": round(fmri_tsnr, 3), "dvars_proxy": round(dvars_proxy, 4), "motion_mm": row_vals["motion_mm_seed"]})
        score, status, reasons = score_row(output_row)
        output_row.update({"qc_score": score, "qc_status": status, "qc_fail_reasons": reasons})
        rows.append(output_row)
    pd.DataFrame(rows).to_csv(OUT, index=False)
    print("Saved " + str(OUT))

if __name__ == "__main__":
    main()
