"""
Yield Analytics Engine for Task 1:
- Overall PASS Yield and FAIL Rate
- Grouped yield by Test_ID, Test_Name, Lot_ID, Wafer_ID
- Top failing tests (both rate & volume)
- Common failure modes
- Retest analysis and condition correlations
"""

from typing import List, Dict, Any, Optional
import numpy as np
import pandas as pd
from pydantic import BaseModel, Field


class YieldGroupRecord(BaseModel):
    group_name: str
    group_value: str
    total_tests: int
    pass_count: int
    fail_count: int
    pass_yield_pct: float
    fail_rate_pct: float


class OverallYieldSummary(BaseModel):
    total_records: int
    total_devices: int
    total_lots: int
    total_wafers: int
    total_tests: int
    pass_count: int
    fail_count: int
    pass_yield_pct: float
    fail_rate_pct: float
    retest_records: int
    retest_rate_pct: float


def compute_overall_yield(df: pd.DataFrame) -> OverallYieldSummary:
    total = len(df)
    if total == 0:
        return OverallYieldSummary(
            total_records=0, total_devices=0, total_lots=0, total_wafers=0, total_tests=0,
            pass_count=0, fail_count=0, pass_yield_pct=0.0, fail_rate_pct=0.0,
            retest_records=0, retest_rate_pct=0.0
        )
    
    # Normalize Result column: PASS, FAIL, or UNKNOWN
    res_series = df["Result"].astype(str).str.strip().str.upper() if "Result" in df.columns else pd.Series(["UNKNOWN"] * total)
    pass_count = int((res_series == "PASS").sum())
    fail_count = int((res_series == "FAIL").sum())
    
    # Calculate yield against valid outcomes
    valid_outcomes = pass_count + fail_count
    pass_yield = round((pass_count / valid_outcomes * 100), 2) if valid_outcomes > 0 else 0.0
    fail_rate = round((fail_count / valid_outcomes * 100), 2) if valid_outcomes > 0 else 0.0

    devices = int(df["Device_ID"].nunique()) if "Device_ID" in df.columns else 0
    lots = int(df["Lot_ID"].nunique()) if "Lot_ID" in df.columns else 0
    wafers = int(df["Wafer_ID"].nunique()) if "Wafer_ID" in df.columns else 0
    tests = int(df["Test_ID"].nunique()) if "Test_ID" in df.columns else 0

    retest_cnt = 0
    if "Retest_Count" in df.columns:
        retests = pd.to_numeric(df["Retest_Count"], errors="coerce").fillna(0)
        retest_cnt = int((retests > 0).sum())
    retest_rate = round((retest_cnt / total * 100), 2) if total > 0 else 0.0

    return OverallYieldSummary(
        total_records=total,
        total_devices=devices,
        total_lots=lots,
        total_wafers=wafers,
        total_tests=tests,
        pass_count=pass_count,
        fail_count=fail_count,
        pass_yield_pct=pass_yield,
        fail_rate_pct=fail_rate,
        retest_records=retest_cnt,
        retest_rate_pct=retest_rate,
    )


def compute_grouped_yield(df: pd.DataFrame, group_col: str) -> List[YieldGroupRecord]:
    if group_col not in df.columns or "Result" not in df.columns or len(df) == 0:
        return []

    res_series = df["Result"].astype(str).str.strip().str.upper()
    temp_df = df.copy()
    temp_df["_norm_result"] = res_series

    grouped = temp_df.groupby(group_col)
    records = []

    for group_val, grp in grouped:
        total = len(grp)
        p_cnt = int((grp["_norm_result"] == "PASS").sum())
        f_cnt = int((grp["_norm_result"] == "FAIL").sum())
        valid = p_cnt + f_cnt
        p_yield = round((p_cnt / valid * 100), 2) if valid > 0 else 0.0
        f_rate = round((f_cnt / valid * 100), 2) if valid > 0 else 0.0

        records.append(YieldGroupRecord(
            group_name=group_col,
            group_value=str(group_val),
            total_tests=total,
            pass_count=p_cnt,
            fail_count=f_cnt,
            pass_yield_pct=p_yield,
            fail_rate_pct=f_rate,
        ))

    return sorted(records, key=lambda x: x.fail_rate_pct, reverse=True)
