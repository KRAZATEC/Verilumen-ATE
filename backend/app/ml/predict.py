"""
Prediction Service for Task 2 & Task 4:
- Accepts raw or unseen single/batch ATE test records
- Performs validation and executes the trained production pipeline
- Returns binary prediction, calibrated probability, contributing features, and explanation
"""

from typing import Dict, Any, List, Union
import pandas as pd
from pydantic import BaseModel, Field
from backend.app.ml.model_registry import model_registry
from backend.app.core.logging import logger


class PredictionRequest(BaseModel):
    Device_ID: str = "DEV_UNSEEN_001"
    Test_ID: str = "T101_LEAKAGE"
    Test_Name: str = "Standby Leakage Current"
    Lot_ID: str = "LOT_2026A"
    Wafer_ID: str = "W01"
    VDD_V: float = 1.2
    Temperature_C: float = 25.0
    Measured_Value: float = 2.4
    Lower_Limit: float = 0.05
    Upper_Limit: float = 5.00
    Retest_Count: int = 0


class FeatureContribution(BaseModel):
    feature: str
    value: Any
    influence: str
    impact_note: str


class PredictionResponse(BaseModel):
    prediction: str  # PASS or FAIL
    probability_of_fail: float
    probability_of_pass: float
    model_name: str
    scenario: str
    top_contributions: List[FeatureContribution]
    engineering_summary: str


def predict_record(req_data: Union[Dict[str, Any], PredictionRequest]) -> PredictionResponse:
    if isinstance(req_data, PredictionRequest):
        data_dict = req_data.model_dump()
    else:
        data_dict = dict(req_data)

    pipeline = model_registry.load_model("production_model")
    metadata = model_registry.load_metadata("production_model") or {}
    
    if pipeline is None:
        raise RuntimeError("No trained model found in registry. Please upload dataset or train model first.")

    input_df = pd.DataFrame([data_dict])
    
    # Model inference
    try:
        y_prob = pipeline.predict_proba(input_df)[0]
        prob_pass = round(float(y_prob[0]), 4)
        prob_fail = round(float(y_prob[1]), 4)
        pred_label = "FAIL" if prob_fail >= 0.5 else "PASS"
    except Exception as e:
        logger.error(f"Inference error: {str(e)}")
        # Fallback to decision or direct predict
        pred = pipeline.predict(input_df)[0]
        pred_label = "FAIL" if pred == 1 else "PASS"
        prob_fail = 1.0 if pred == 1 else 0.0
        prob_pass = 1.0 - prob_fail

    # Determine domain feature contributions
    contributions = []
    meas = data_dict.get("Measured_Value")
    ll = data_dict.get("Lower_Limit")
    ul = data_dict.get("Upper_Limit")
    temp = data_dict.get("Temperature_C")
    vdd = data_dict.get("VDD_V")

    if meas is not None and ll is not None and ul is not None:
        margin_low = meas - ll
        margin_up = ul - meas
        span = ul - ll
        if span > 0:
            norm_pos = (meas - ll) / span
            if norm_pos < 0.1:
                contributions.append(FeatureContribution(
                    feature="Measured_Value",
                    value=meas,
                    influence="INCREASES_FAIL_RISK",
                    impact_note=f"Measurement is within {round(margin_low, 3)} of Lower Limit ({ll})."
                ))
            elif norm_pos > 0.9:
                contributions.append(FeatureContribution(
                    feature="Measured_Value",
                    value=meas,
                    influence="INCREASES_FAIL_RISK",
                    impact_note=f"Measurement is within {round(margin_up, 3)} of Upper Limit ({ul})."
                ))
            else:
                contributions.append(FeatureContribution(
                    feature="Measured_Value",
                    value=meas,
                    influence="FAVORS_PASS",
                    impact_note=f"Measurement sits securely inside specification window ({ll} to {ul})."
                ))

    if temp is not None:
        if temp >= 85.0:
            contributions.append(FeatureContribution(
                feature="Temperature_C",
                value=temp,
                influence="INCREASES_FAIL_RISK",
                impact_note=f"Elevated junction temperature ({temp}°C) increases thermal drift."
            ))
        elif temp <= -10.0:
            contributions.append(FeatureContribution(
                feature="Temperature_C",
                value=temp,
                influence="INCREASES_FAIL_RISK",
                impact_note=f"Cold corner testing ({temp}°C) tests speed/margin limits."
            ))

    retests = data_dict.get("Retest_Count", 0)
    if retests > 0:
        contributions.append(FeatureContribution(
            feature="Retest_Count",
            value=retests,
            influence="INCREASES_FAIL_RISK",
            impact_note=f"Unit required {retests} retests, signaling intermittent electrical behavior."
        ))

    model_name = metadata.get("model_name", "Classifier Pipeline")
    scenario = metadata.get("scenario", "Scenario B - Measurement-Aware")

    eng_summary = (
        f"Unit predicted {pred_label} with {round(prob_fail*100, 1)}% failure probability "
        f"by {model_name} under {scenario}."
    )

    return PredictionResponse(
        prediction=pred_label,
        probability_of_fail=prob_fail,
        probability_of_pass=prob_pass,
        model_name=model_name,
        scenario=scenario,
        top_contributions=contributions,
        engineering_summary=eng_summary,
    )
