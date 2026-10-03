import pytest
import pandas as pd
from backend.app.data.schema import REQUIRED_COLUMNS
from backend.app.data.ingestion import validate_schema, normalize_column_names


def test_schema_valid_synthetic_data():
    df = pd.read_csv("data/demo_ate_data.csv")
    norm_df, _ = normalize_column_names(df)
    report = validate_schema(norm_df)
    assert report.is_valid is True
    assert len(report.missing_required_columns) == 0
    assert report.total_rows > 1000


def test_schema_missing_column_detection():
    df = pd.DataFrame({
        "Device_ID": ["D1", "D2"],
        "Test_ID": ["T1", "T2"],
        "Result": ["PASS", "FAIL"],
    })
    report = validate_schema(df)
    assert report.is_valid is False
    assert "Lot_ID" in report.missing_required_columns
    assert "Measured_Value" in report.missing_required_columns


def test_schema_column_aliases():
    df = pd.DataFrame({
        "device": ["D1"],
        "test_num": ["T1"],
        "test": ["Standby"],
        "lot": ["L1"],
        "wafer": ["W1"],
        "vdd": [1.2],
        "temp": [25.0],
        "measured": [1.5],
        "ll": [0.0],
        "ul": [3.0],
        "result": ["PASS"],
        "fail_mode": ["NONE"],
        "retest": [0]
    })
    norm_df, aliases = normalize_column_names(df)
    assert "Device_ID" in norm_df.columns
    assert "Test_ID" in norm_df.columns
    assert "Measured_Value" in norm_df.columns
    report = validate_schema(norm_df)
    assert report.is_valid is True
