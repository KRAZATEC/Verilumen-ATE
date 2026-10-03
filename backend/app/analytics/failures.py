"""
Failure Mode and Top Failing Test Analytics for Task 1:
- Top failing tests by rate and by raw volume
- Failure mode counts and distributions
- Retest impact analysis
"""

from typing import List, Dict, Any
import pandas as pd
from pydantic import BaseModel


class FailureModeRecord(BaseModel):
    failure_mode: str
    count: int
    percentage_of_failures: float
    percentage_of_all_records: float


class TopFailingTest(BaseModel):
    test_id: str
    test_name: str
    total_executions: int
    fail_count: int
    fail_rate_pct: float
    dominant_failure_mode: str


def analyze_failure_modes(df: pd.DataFrame) -> List[FailureModeRecord]:
    if "Result" not in df.columns or "Failure_Mode" not in df.columns or len(df) == 0:
        return []

    total_records = len(df)
    res_series = df["Result"].astype(str).str.strip().str.upper()
    fails_df = df[res_series == "FAIL"]
    total_fails = len(fails_df)

    if total_fails == 0:
        return []

    mode_counts = fails_df["Failure_Mode"].astype(str).value_counts()
    records = []
    for mode, cnt in mode_counts.items():
        pct_fails = round((cnt / total_fails * 100), 2)
        pct_all = round((cnt / total_records * 100), 2)
        records.append(FailureModeRecord(
            failure_mode=str(mode),
            count=int(cnt),
            percentage_of_failures=pct_fails,
            percentage_of_all_records=pct_all,
        ))
    return records


def identify_top_failing_tests(df: pd.DataFrame, top_n: int = 10) -> List[TopFailingTest]:
    if "Test_ID" not in df.columns or "Result" not in df.columns or len(df) == 0:
        return []

    res_series = df["Result"].astype(str).str.strip().str.upper()
    temp_df = df.copy()
    temp_df["_is_fail"] = (res_series == "FAIL").astype(int)

    has_test_name = "Test_Name" in df.columns
    has_fail_mode = "Failure_Mode" in df.columns

    results = []
    for test_id, grp in temp_df.groupby("Test_ID"):
        total = len(grp)
        fails = int(grp["_is_fail"].sum())
        fail_rate = round((fails / total * 100), 2) if total > 0 else 0.0

        test_name = str(grp["Test_Name"].iloc[0]) if has_test_name else str(test_id)
        
        dominant_mode = "NONE"
        if has_fail_mode and fails > 0:
            fail_modes = grp[grp["_is_fail"] == 1]["Failure_Mode"].astype(str).mode()
            if not fail_modes.empty:
                dominant_mode = str(fail_modes[0])

        results.append(TopFailingTest(
            test_id=str(test_id),
            test_name=test_name,
            total_executions=total,
            fail_count=fails,
            fail_rate_pct=fail_rate,
            dominant_failure_mode=dominant_mode,
        ))

    # Sort primarily by fail_count descending, then fail_rate_pct
    sorted_tests = sorted(results, key=lambda x: (x.fail_count, x.fail_rate_pct), reverse=True)
    return sorted_tests[:top_n]
