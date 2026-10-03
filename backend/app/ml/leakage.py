"""
Automated Data Leakage Audit Engine.
Enforces the assessment rule:
- Post-outcome fields (Result, Failure_Mode) MUST NEVER be predictive features.
- Audits pre-test vs measurement-aware feature timing.
- Verifies that target labels are completely excluded from X.
"""

from typing import List, Dict, Any, Tuple
import pandas as pd
from pydantic import BaseModel


FORBIDDEN_PREDICTIVE_FEATURES = [
    "Result",
    "result",
    "Failure_Mode",
    "failure_mode",
    "fail_mode",
]


class LeakageAuditReport(BaseModel):
    is_leakage_free: bool
    forbidden_features_detected: List[str]
    target_column: str
    feature_columns: List[str]
    timing_scenario: str
    audit_notes: List[str]


def audit_feature_leakage(
    feature_cols: List[str],
    target_col: str = "Result",
    scenario: str = "Scenario A - Pre-Test Prediction"
) -> LeakageAuditReport:
    """
    Audits feature set to guarantee no target leakage exists.
    """
    forbidden_found = [c for c in feature_cols if c in FORBIDDEN_PREDICTIVE_FEATURES or c.lower() == target_col.lower()]
    
    notes = []
    if forbidden_found:
        notes.append(f"CRITICAL LEAKAGE: Direct target/post-outcome features detected in feature set: {forbidden_found}")
    else:
        notes.append("Audit confirmed: No direct target (Result) or post-outcome fields (Failure_Mode) in feature set.")

    if scenario.startswith("Scenario A"):
        # Pre-test scenario: Measured_Value should not be used if predicting before test execution
        if "Measured_Value" in feature_cols:
            notes.append("WARNING: 'Measured_Value' included in Scenario A (Pre-test). This should only be used in Scenario B (Measurement-aware diagnosis).")

    is_clean = len(forbidden_found) == 0

    return LeakageAuditReport(
        is_leakage_free=is_clean,
        forbidden_features_detected=forbidden_found,
        target_column=target_col,
        feature_columns=feature_cols,
        timing_scenario=scenario,
        audit_notes=notes,
    )
