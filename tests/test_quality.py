import pytest
import pandas as pd
import numpy as np
from backend.app.analytics.quality import run_data_quality_audit
from backend.app.data.preprocessing import clean_dataset


def test_data_quality_audit():
    df = pd.DataFrame({
        "Device_ID": ["D1", "D1", "D2"],
        "Test_ID": ["T1", "T1", "T1"],
        "Measured_Value": [1.0, 1.0, np.nan],
        "Lower_Limit": [0.0, 0.0, 0.0],
        "Upper_Limit": [2.0, 2.0, 2.0],
        "Result": ["PASS", "PASS", "FAIL"],
        "Retest_Count": [0, 0, 1],
    })
    report = run_data_quality_audit(df)
    assert report.total_records == 3
    assert report.duplicate_summary.total_duplicate_rows == 1
    
    # Clean dataset
    clean_df, audit = clean_dataset(df, drop_exact_duplicates=True)
    assert len(clean_df) == 2
    assert audit["duplicates_removed"] == 1
    assert "Measured_Value" in audit["missing_imputations"]
