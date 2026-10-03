"""
Statistical Anomaly Detection Layer:
- Median Absolute Deviation (MAD) & IQR per Test_ID
- Specification Boundary Proximity (Borderline detection)
- Specification Violations
"""

from typing import Dict, List, Tuple
import numpy as np
import pandas as pd


def compute_statistical_anomalies(df: pd.DataFrame) -> pd.DataFrame:
    """
    Computes statistical z-score/MAD and specification-violation signals grouped by Test_ID.
    Returns DataFrame with statistical anomaly scores and flags.
    """
    result_df = df.copy()
    
    # Initialize metric columns
    result_df["stat_z_score"] = 0.0
    result_df["stat_mad_deviation"] = 0.0
    result_df["spec_proximity"] = 1.0  # 0 = at limit boundary, 1 = nominal center
    result_df["is_spec_violation"] = False
    result_df["is_statistical_outlier"] = False

    if "Test_ID" not in result_df.columns or "Measured_Value" not in result_df.columns:
        return result_df

    for test_id, group_indices in result_df.groupby("Test_ID").groups.items():
        sub_df = result_df.loc[group_indices]
        vals = pd.to_numeric(sub_df["Measured_Value"], errors="coerce")
        valid_vals = vals.dropna()

        if len(valid_vals) < 3:
            continue

        median = float(valid_vals.median())
        mad = float(np.median(np.abs(valid_vals - median)))
        std = float(valid_vals.std()) or 1e-6
        mad = mad if mad > 1e-6 else (std * 0.6745)

        # Standard Z-Score and MAD-based modified Z-score
        z_scores = np.abs((vals - median) / std)
        mad_scores = np.abs(0.6745 * (vals - median) / mad)

        result_df.loc[group_indices, "stat_z_score"] = z_scores.fillna(0.0).round(3)
        result_df.loc[group_indices, "stat_mad_deviation"] = mad_scores.fillna(0.0).round(3)
        result_df.loc[group_indices, "is_statistical_outlier"] = (mad_scores > 3.5) | (z_scores > 3.5)

        # Spec proximity
        if "Lower_Limit" in sub_df.columns and "Upper_Limit" in sub_df.columns:
            ll = pd.to_numeric(sub_df["Lower_Limit"], errors="coerce")
            ul = pd.to_numeric(sub_df["Upper_Limit"], errors="coerce")
            
            span = np.maximum(ul - ll, 1e-6)
            dist_lower = vals - ll
            dist_upper = ul - vals
            
            # Spec violation
            is_violation = (dist_lower < 0) | (dist_upper < 0)
            result_df.loc[group_indices, "is_spec_violation"] = is_violation

            # Proximity: min distance to either boundary normalized by span
            min_dist = np.minimum(dist_lower, dist_upper)
            proximity = np.clip(min_dist / span, 0.0, 1.0)
            result_df.loc[group_indices, "spec_proximity"] = proximity.round(4)

    return result_df
