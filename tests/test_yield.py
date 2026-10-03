import pytest
import pandas as pd
from backend.app.analytics.yield_analysis import compute_overall_yield, compute_grouped_yield
from backend.app.analytics.failures import analyze_failure_modes, identify_top_failing_tests


def test_yield_calculations():
    df = pd.DataFrame({
        "Device_ID": ["D1", "D2", "D3", "D4"],
        "Test_ID": ["T1", "T1", "T2", "T2"],
        "Lot_ID": ["L1", "L1", "L2", "L2"],
        "Wafer_ID": ["W1", "W1", "W1", "W2"],
        "Result": ["PASS", "PASS", "FAIL", "PASS"],
        "Failure_Mode": ["NONE", "NONE", "TIMING_VIOLATION", "NONE"],
        "Retest_Count": [0, 0, 1, 0]
    })
    
    summary = compute_overall_yield(df)
    assert summary.total_records == 4
    assert summary.pass_count == 3
    assert summary.fail_count == 1
    assert summary.pass_yield_pct == 75.0
    assert summary.fail_rate_pct == 25.0
    
    lot_yields = compute_grouped_yield(df, "Lot_ID")
    assert len(lot_yields) == 2
    
    modes = analyze_failure_modes(df)
    assert len(modes) == 1
    assert modes[0].failure_mode == "TIMING_VIOLATION"
    assert modes[0].count == 1
