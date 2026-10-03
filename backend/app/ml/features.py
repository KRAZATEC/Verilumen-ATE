"""
Feature Engineering Pipeline:
- Leakage-safe derivation of engineering features
- Preprocessing transformers compatible with scikit-learn
- Scenario A (Pre-test) vs Scenario B (Measurement-aware) feature sets
- Handles missing values, scaling, and categorical encoding without leakage
"""

from typing import List, Tuple, Dict, Any, Optional
import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from backend.app.ml.leakage import FORBIDDEN_PREDICTIVE_FEATURES


class ATEFeatureExtractor(BaseEstimator, TransformerMixin):
    """
    Computes semiconductor engineering domain features:
    - spec_range = Upper_Limit - Lower_Limit
    - spec_margin_lower = Measured_Value - Lower_Limit
    - spec_margin_upper = Upper_Limit - Measured_Value
    - spec_normalized_pos = (Measured_Value - Lower_Limit) / spec_range
    - temp_deviation_from_room = Temperature_C - 25.0
    - vdd_deviation_from_nominal = VDD_V - 1.2
    """
    def __init__(self, include_measurements: bool = True):
        self.include_measurements = include_measurements

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        df = X.copy() if isinstance(X, pd.DataFrame) else pd.DataFrame(X)
        
        # Spec range
        if "Upper_Limit" in df.columns and "Lower_Limit" in df.columns:
            df["spec_range"] = df["Upper_Limit"] - df["Lower_Limit"]
            df["spec_center"] = (df["Upper_Limit"] + df["Lower_Limit"]) / 2.0
        else:
            df["spec_range"] = 1.0
            df["spec_center"] = 0.0

        if "Temperature_C" in df.columns:
            df["temp_deviation"] = df["Temperature_C"] - 25.0
        else:
            df["temp_deviation"] = 0.0

        if "VDD_V" in df.columns:
            df["vdd_deviation"] = df["VDD_V"] - 1.2
        else:
            df["vdd_deviation"] = 0.0

        if self.include_measurements and "Measured_Value" in df.columns:
            df["margin_lower"] = df["Measured_Value"] - df.get("Lower_Limit", 0.0)
            df["margin_upper"] = df.get("Upper_Limit", 0.0) - df["Measured_Value"]
            # Avoid divide-by-zero
            denom = np.where(df["spec_range"].abs() > 1e-6, df["spec_range"], 1.0)
            df["norm_spec_pos"] = (df["Measured_Value"] - df.get("Lower_Limit", 0.0)) / denom
        elif not self.include_measurements and "Measured_Value" in df.columns:
            # Exclude Measured_Value in strict pre-test scenario
            df = df.drop(columns=["Measured_Value"])

        return df


def build_preprocessor(
    numeric_features: List[str],
    categorical_features: List[str]
) -> ColumnTransformer:
    num_pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler()),
    ])

    cat_pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="constant", fill_value="UNKNOWN")),
        ("encoder", OneHotEncoder(handle_unknown="ignore", sparse_output=False)),
    ])

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", num_pipeline, numeric_features),
            ("cat", cat_pipeline, categorical_features),
        ],
        remainder="drop"
    )
    return preprocessor


def prepare_training_matrices(
    df: pd.DataFrame,
    scenario: str = "Scenario B - Measurement-Aware"
) -> Tuple[pd.DataFrame, pd.Series, List[str], List[str]]:
    """
    Extracts X, y and feature lists safely ensuring NO TARGET LEAKAGE.
    Target binary mapping: PASS = 0, FAIL = 1.
    """
    clean_df = df.copy()

    # Normalize Result
    if "Result" not in clean_df.columns:
        raise ValueError("Missing 'Result' target column in dataset.")

    res_norm = clean_df["Result"].astype(str).str.strip().str.upper()
    valid_mask = res_norm.isin(["PASS", "FAIL"])
    clean_df = clean_df[valid_mask].reset_index(drop=True)
    res_norm = res_norm[valid_mask].reset_index(drop=True)

    y = (res_norm == "FAIL").astype(int)

    # Candidate feature definitions
    categorical_cols = [c for c in ["Test_ID", "Lot_ID", "Wafer_ID"] if c in clean_df.columns]
    
    if scenario.startswith("Scenario A"):
        # Pre-test only: exclude Measured_Value
        numeric_cols = [c for c in ["VDD_V", "Temperature_C", "Lower_Limit", "Upper_Limit", "Retest_Count"] if c in clean_df.columns]
    else:
        # Measurement-aware
        numeric_cols = [c for c in ["VDD_V", "Temperature_C", "Measured_Value", "Lower_Limit", "Upper_Limit", "Retest_Count"] if c in clean_df.columns]

    X = clean_df[numeric_cols + categorical_cols].copy()
    
    # Audit for target leakage
    for forbidden in FORBIDDEN_PREDICTIVE_FEATURES:
        if forbidden in X.columns:
            X = X.drop(columns=[forbidden])

    return X, y, numeric_cols, categorical_cols
