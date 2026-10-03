"""
Evidence Engine & Engineering Reasoning:
The core reasoning engine that powers Failure Investigation and AI Analysis screens.
Enforces strict rules:
1. Observed evidence and Inferred causes MUST BE SEPARATE.
2. Grounded strictly in supplied data: does not hallucinate root causes.
3. If evidence is insufficient, explicitly states:
   'Insufficient evidence for a reliable engineering interpretation.'
"""

from typing import List, Dict, Any, Optional
import pandas as pd
from pydantic import BaseModel, Field


class ObservedEvidence(BaseModel):
    category: str
    finding: str
    data_points: Dict[str, Any]


class AIAnalysisReport(BaseModel):
    device_id: str
    test_id: str
    lot_id: str
    wafer_id: str
    observed_result: str
    recorded_failure_mode: str
    observed_evidence: List[ObservedEvidence]
    model_evidence: Dict[str, Any]
    anomaly_evidence: Dict[str, Any]
    possible_interpretations: List[str]
    confidence_level: str  # HIGH, MEDIUM, LOW, INSUFFICIENT
    limitations_and_unknowns: List[str]


def build_evidence_analysis(
    record: Dict[str, Any],
    overall_yield_fail_rate: float = 7.2,
    model_pred_prob: Optional[float] = None,
    anomaly_score: Optional[float] = None,
) -> AIAnalysisReport:
    """
    Synthesizes multi-dimensional evidence into a rigorous engineering diagnostic report.
    """
    dev_id = str(record.get("Device_ID", "UNKNOWN"))
    test_id = str(record.get("Test_ID", "UNKNOWN"))
    lot_id = str(record.get("Lot_ID", "UNKNOWN"))
    wafer_id = str(record.get("Wafer_ID", "UNKNOWN"))
    res = str(record.get("Result", "UNKNOWN")).upper()
    fail_mode = str(record.get("Failure_Mode", "NONE"))

    meas = record.get("Measured_Value")
    ll = record.get("Lower_Limit")
    ul = record.get("Upper_Limit")
    temp = record.get("Temperature_C")
    vdd = record.get("VDD_V")
    retest = record.get("Retest_Count", 0)

    observed: List[ObservedEvidence] = []
    interpretations: List[str] = []
    limitations: List[str] = []

    # 1. Electrical / Limit Evidence
    if meas is not None and ll is not None and ul is not None:
        meas_val = float(meas)
        ll_val = float(ll)
        ul_val = float(ul)
        span = ul_val - ll_val
        is_oob = (meas_val < ll_val) or (meas_val > ul_val)
        
        observed.append(ObservedEvidence(
            category="Parametric Limits",
            finding=f"Measured value is {meas_val} vs Spec Limits [{ll_val}, {ul_val}]. Spec Out-of-Bounds: {is_oob}.",
            data_points={"measured": meas_val, "lower_limit": ll_val, "upper_limit": ul_val, "out_of_spec": is_oob}
        ))
        
        if is_oob:
            interpretations.append(
                f"Direct electrical specification violation on test {test_id}. Silicon parameter failed to settle within guaranteed operating bounds."
            )
        elif span > 0:
            margin_low = meas_val - ll_val
            margin_up = ul_val - meas_val
            min_margin = min(margin_low, margin_up)
            if (min_margin / span) < 0.08:
                interpretations.append(
                    f"Measurement is near the specification boundary (margin: {round(min_margin, 3)}). Possible process corner or measurement guardband risk."
                )
            else:
                interpretations.append(
                    f"Measurement resides safely within the specification window with {round(min_margin, 3)} units of margin to closest limit."
                )

    # 2. Thermal / Environmental Evidence
    if temp is not None:
        t_val = float(temp)
        if t_val >= 85.0:
            observed.append(ObservedEvidence(
                category="Environmental Stress",
                finding=f"Test executed at elevated thermal corner ({t_val}°C).",
                data_points={"temperature_c": t_val}
            ))
            interpretations.append(
                f"Thermal stress ({t_val}°C) increases carrier mobility degradation and subthreshold leakage, exacerbating marginal timing or leakage behavior."
            )

    # 3. Retest Evidence
    if retest and int(retest) > 0:
        observed.append(ObservedEvidence(
            category="Test Retest Telemetry",
            finding=f"Unit required {retest} retest execution(s) before logging final outcome.",
            data_points={"retest_count": int(retest)}
        ))
        interpretations.append(
            "Multiple retests suggest socket probe contact resistance instability, tester pin contact wear, or marginal device latch-up."
        )

    # Determine confidence level
    if len(observed) >= 3 or (meas is not None and ll is not None and ul is not None and is_oob):
        confidence = "HIGH"
    elif len(observed) >= 1:
        confidence = "MEDIUM"
    else:
        confidence = "INSUFFICIENT"
        interpretations.append("Insufficient evidence for a reliable engineering interpretation.")

    # Model & Anomaly Evidence summaries
    model_ev = {
        "predicted_probability_fail": model_pred_prob if model_pred_prob is not None else "N/A",
        "model_agreement": (res == "FAIL" and (model_pred_prob or 0) > 0.5) or (res == "PASS" and (model_pred_prob or 0) <= 0.5),
    }
    
    anom_ev = {
        "anomaly_score": anomaly_score if anomaly_score is not None else "N/A",
        "is_flagged_anomaly": (anomaly_score or 0) >= 60.0,
    }

    # Strict limitations
    limitations.append("Physical failure analysis (SEM/TEM/EMMI) is required to establish true physical causation.")
    limitations.append("Inline wafer fab metrology data is not linked in this ATE telemetry feed.")
    limitations.append("Reported hypotheses are bounded solely by tester parametric measurements.")

    return AIAnalysisReport(
        device_id=dev_id,
        test_id=test_id,
        lot_id=lot_id,
        wafer_id=wafer_id,
        observed_result=res,
        recorded_failure_mode=fail_mode,
        observed_evidence=observed,
        model_evidence=model_ev,
        anomaly_evidence=anom_ev,
        possible_interpretations=interpretations,
        confidence_level=confidence,
        limitations_and_unknowns=limitations,
    )
