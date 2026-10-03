"""
Unsupervised Anomaly Detection using Isolation Forest:
- Fits isolation forest on continuous electrical and thermal dimensions
- Yields multivariate anomaly score
"""

from typing import Tuple
import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from backend.app.core.config import settings
from backend.app.core.logging import logger


def run_isolation_forest(
    df: pd.DataFrame,
    contamination: float = 0.04
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Fits IsolationForest on numerical features.
    Returns: (anomaly_flags: bool[], raw_anomaly_scores: float[])
    """
    candidate_features = ["Measured_Value", "VDD_V", "Temperature_C", "Retest_Count"]
    features_present = [c for c in candidate_features if c in df.columns]

    if not features_present or len(df) < 10:
        return np.zeros(len(df), dtype=bool), np.zeros(len(df), dtype=float)

    X_mat = df[features_present].apply(pd.to_numeric, errors="coerce").fillna(0.0).values

    try:
        iso = IsolationForest(
            n_estimators=100,
            contamination=contamination,
            random_state=42,
            n_jobs=-1,
        )
        preds = iso.fit_predict(X_mat)
        # Decision function: lower values mean more anomalous
        scores = -iso.decision_function(X_mat)  # Invert so higher = more anomalous
        flags = (preds == -1)
        return flags, scores
    except Exception as e:
        logger.error(f"IsolationForest failed: {str(e)}")
        return np.zeros(len(df), dtype=bool), np.zeros(len(df), dtype=float)
