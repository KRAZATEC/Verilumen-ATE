"""
Unified Anomaly Scoring, Ranking, and Aggregations for Task 3:
- Combines statistical deviations, spec boundary proximity, and Isolation Forest
- Normalizes into a documented 0-100 Anomaly Score
- Ranks top suspicious records with evidence flags
- Compares anomalies with PASS/FAIL outcomes and Failure Modes
- Aggregates anomaly rates across Devices, Tests, Lots, and Wafers
"""

from typing import List, Dict, Any, Optional, Tuple
import numpy as np
import pandas as pd
from pydantic import BaseModel
from backend.app.anomaly.statistical import compute_statistical_anomalies
from backend.app.anomaly.isolation_forest import run_isolation_forest


class AnomalyRecord(BaseModel):
    rank: int
    device_id: str
    test_id: str
    test_name: str
    lot_id: str
    wafer_id: str
    anomaly_score: float
    is_anomaly: bool
    measured_value: Optional[float]
    lower_limit: Optional[float]
    upper_limit: Optional[float]
    result: str
    failure_mode: str
    retest_count: int
    detector_evidence: List[str]
    possible_interpretation: str


class AnomalySummary(BaseModel):
    total_records_analyzed: int
    total_anomalies_flagged: int
    anomaly_rate_pct: float
    max_anomaly_score: float
    avg_anomaly_score: float
    anomaly_vs_fail_matrix: Dict[str, int]
    top_suspicious_records: List[AnomalyRecord]
    suspicious_by_lot: List[Dict[str, Any]]
    suspicious_by_wafer: List[Dict[str, Any]]
    suspicious_by_test: List[Dict[str, Any]]


def detect_and_score_anomalies(
    df: pd.DataFrame,
    contamination: float = 0.04
) -> Tuple[pd.DataFrame, AnomalySummary]:
    # 1. Statistical anomaly pass
    stat_df = compute_statistical_anomalies(df)
    
    # 2. Isolation forest pass
    iso_flags, iso_scores = run_isolation_forest(stat_df, contamination=contamination)
    stat_df["iso_score"] = iso_scores
    stat_df["iso_flag"] = iso_flags

    # 3. Blended Anomaly Score (0 to 100)
    # Component 1: MAD deviation scaled (0 to 40 pts)
    mad_pts = np.clip(stat_df["stat_mad_deviation"] / 6.0 * 40.0, 0, 40.0)
    
    # Component 2: Spec proximity & violation (0 to 35 pts)
    # 0 proximity -> right at limit -> 25 pts; violation -> 35 pts
    spec_pts = np.where(
        stat_df["is_spec_violation"],
        35.0,
        (1.0 - np.clip(stat_df["spec_proximity"], 0.0, 1.0)) * 25.0
    )

    # Component 3: Isolation Forest normalized (0 to 25 pts)
    iso_min = iso_scores.min()
    iso_max = iso_scores.max()
    iso_span = (iso_max - iso_min) if (iso_max - iso_min) > 1e-6 else 1.0
    norm_iso = (iso_scores - iso_min) / iso_span
    iso_pts = norm_iso * 25.0

    total_score = np.round(mad_pts + spec_pts + iso_pts, 2)
    stat_df["anomaly_score"] = total_score
    stat_df["is_anomaly"] = (total_score >= 60.0) | stat_df["iso_flag"] | stat_df["is_spec_violation"]

    # Rank records descending by anomaly_score
    sorted_df = stat_df.sort_values(by="anomaly_score", ascending=False).reset_index(drop=True)
    sorted_df["anomaly_rank"] = np.arange(1, len(sorted_df) + 1)

    # Anomaly vs Result Matrix
    res_s = sorted_df["Result"].astype(str).str.strip().str.upper()
    is_anom = sorted_df["is_anomaly"]
    
    matrix = {
        "Anomaly_FAIL": int(((is_anom) & (res_s == "FAIL")).sum()),
        "Anomaly_PASS": int(((is_anom) & (res_s == "PASS")).sum()),  # Suspicious golden passes
        "Normal_PASS": int(((-is_anom) & (res_s == "PASS")).sum()),
        "Normal_FAIL": int(((-is_anom) & (res_s == "FAIL")).sum()),
    }

    # Build Top Suspicious Records
    top_records: List[AnomalyRecord] = []
    for idx, row in sorted_df.head(50).iterrows():
        evidences = []
        if row["is_spec_violation"]:
            evidences.append(f"Measured value ({row['Measured_Value']}) violates specification limits [{row['Lower_Limit']}, {row['Upper_Limit']}].")
        elif row["spec_proximity"] < 0.1:
            evidences.append(f"Borderline measurement: within {round(row['spec_proximity']*100, 1)}% of limit boundary.")

        if row["stat_mad_deviation"] > 3.5:
            evidences.append(f"Statistically extreme measurement: MAD deviation is {row['stat_mad_deviation']}x.")

        if row["iso_flag"]:
            evidences.append(f"Multivariate Isolation Forest identified outlier density.")

        if row.get("Retest_Count", 0) > 0:
            evidences.append(f"Device was retested {row['Retest_Count']} time(s).")

        # Interpretation
        if row["Result"] == "PASS" and row["anomaly_score"] >= 60.0:
            interp = "Marginal pass unit with abnormal parametric drift; high risk of field reliability failure."
        elif row["Result"] == "FAIL":
            interp = f"Confirmed test failure under mode {row.get('Failure_Mode', 'UNKNOWN')}."
        else:
            interp = "Device demonstrates unusual distribution behavior requiring engineering curve-trace."

        top_records.append(AnomalyRecord(
            rank=int(row["anomaly_rank"]),
            device_id=str(row["Device_ID"]),
            test_id=str(row["Test_ID"]),
            test_name=str(row.get("Test_Name", row["Test_ID"])),
            lot_id=str(row.get("Lot_ID", "UNKNOWN")),
            wafer_id=str(row.get("Wafer_ID", "UNKNOWN")),
            anomaly_score=float(row["anomaly_score"]),
            is_anomaly=bool(row["is_anomaly"]),
            measured_value=float(row["Measured_Value"]) if pd.notna(row["Measured_Value"]) else None,
            lower_limit=float(row["Lower_Limit"]) if pd.notna(row["Lower_Limit"]) else None,
            upper_limit=float(row["Upper_Limit"]) if pd.notna(row["Upper_Limit"]) else None,
            result=str(row.get("Result", "UNKNOWN")),
            failure_mode=str(row.get("Failure_Mode", "NONE")),
            retest_count=int(row.get("Retest_Count", 0)),
            detector_evidence=evidences,
            possible_interpretation=interp,
        ))

    # Aggregations by Lot, Wafer, Test
    suspicious_by_lot = []
    if "Lot_ID" in sorted_df.columns:
        for lot, grp in sorted_df.groupby("Lot_ID"):
            cnt = int(grp["is_anomaly"].sum())
            suspicious_by_lot.append({"lot_id": str(lot), "anomaly_count": cnt, "rate_pct": round(cnt / len(grp) * 100, 2)})

    suspicious_by_wafer = []
    if "Wafer_ID" in sorted_df.columns:
        for waf, grp in sorted_df.groupby("Wafer_ID"):
            cnt = int(grp["is_anomaly"].sum())
            suspicious_by_wafer.append({"wafer_id": str(waf), "anomaly_count": cnt, "rate_pct": round(cnt / len(grp) * 100, 2)})

    suspicious_by_test = []
    if "Test_ID" in sorted_df.columns:
        for t_id, grp in sorted_df.groupby("Test_ID"):
            cnt = int(grp["is_anomaly"].sum())
            suspicious_by_test.append({"test_id": str(t_id), "anomaly_count": cnt, "rate_pct": round(cnt / len(grp) * 100, 2)})

    total_flagged = int(sorted_df["is_anomaly"].sum())
    total_len = len(sorted_df)

    summary = AnomalySummary(
        total_records_analyzed=total_len,
        total_anomalies_flagged=total_flagged,
        anomaly_rate_pct=round(total_flagged / total_len * 100, 2) if total_len > 0 else 0.0,
        max_anomaly_score=float(sorted_df["anomaly_score"].max()) if total_len > 0 else 0.0,
        avg_anomaly_score=round(float(sorted_df["anomaly_score"].mean()), 2) if total_len > 0 else 0.0,
        anomaly_vs_fail_matrix=matrix,
        top_suspicious_records=top_records,
        suspicious_by_lot=sorted(suspicious_by_lot, key=lambda x: x["rate_pct"], reverse=True),
        suspicious_by_wafer=sorted(suspicious_by_wafer, key=lambda x: x["rate_pct"], reverse=True),
        suspicious_by_test=sorted(suspicious_by_test, key=lambda x: x["rate_pct"], reverse=True),
    )

    return sorted_df, summary
