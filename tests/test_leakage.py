import pytest
import pandas as pd
from backend.app.ml.leakage import audit_feature_leakage
from backend.app.ml.features import prepare_training_matrices


def test_leakage_audit():
    # Attempting to use post-outcome fields
    bad_features = ["VDD_V", "Temperature_C", "Result", "Failure_Mode"]
    audit = audit_feature_leakage(bad_features, target_col="Result")
    assert audit.is_leakage_free is False
    assert "Result" in audit.forbidden_features_detected
    assert "Failure_Mode" in audit.forbidden_features_detected

    # Clean pre-test features
    good_features = ["VDD_V", "Temperature_C", "Lower_Limit", "Upper_Limit"]
    clean_audit = audit_feature_leakage(good_features, target_col="Result")
    assert clean_audit.is_leakage_free is True


def test_prepare_training_matrices():
    df = pd.DataFrame({
        "Device_ID": ["D1", "D2", "D3"],
        "Test_ID": ["T1", "T1", "T2"],
        "Lot_ID": ["L1", "L1", "L2"],
        "Wafer_ID": ["W1", "W1", "W2"],
        "VDD_V": [1.2, 1.2, 1.2],
        "Temperature_C": [25.0, 25.0, 85.0],
        "Measured_Value": [1.5, 1.6, 9.9],
        "Lower_Limit": [0.0, 0.0, 0.0],
        "Upper_Limit": [2.0, 2.0, 2.0],
        "Result": ["PASS", "PASS", "FAIL"],
        "Failure_Mode": ["NONE", "NONE", "POWER_ANOMALY"],
        "Retest_Count": [0, 0, 1],
    })
    
    X, y, num_cols, cat_cols = prepare_training_matrices(df, scenario="Scenario B - Measurement-Aware")
    assert "Result" not in X.columns
    assert "Failure_Mode" not in X.columns
    assert len(y) == 3
    assert y.iloc[2] == 1  # FAIL = 1
