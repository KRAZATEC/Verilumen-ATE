import pytest
import pandas as pd
from backend.app.ml.train import train_and_compare_models
from backend.app.ml.predict import predict_record, PredictionRequest


def test_models_train_and_predict():
    df = pd.read_csv("data/demo_ate_data.csv").head(1000)
    res = train_and_compare_models(df, scenario="Scenario B - Measurement-Aware")
    assert "best_model" in res
    assert "all_metrics" in res
    assert len(res["all_metrics"]) >= 2

    # Run prediction with unseen request
    req = PredictionRequest(
        Device_ID="DEV_TEST_001",
        Test_ID="T101_LEAKAGE",
        Test_Name="Standby Leakage Current",
        Lot_ID="LOT_2026A",
        Wafer_ID="W01",
        VDD_V=1.2,
        Temperature_C=25.0,
        Measured_Value=2.0,
        Lower_Limit=0.05,
        Upper_Limit=5.00,
        Retest_Count=0
    )
    pred_res = predict_record(req)
    assert pred_res.prediction in ["PASS", "FAIL"]
    assert 0.0 <= pred_res.probability_of_fail <= 1.0
