import pytest
from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"


def test_demo_and_overview_pipeline():
    # Process demo dataset
    proc_res = client.post("/api/process-demo")
    assert proc_res.status_code == 200
    
    # Overview
    ov_res = client.get("/api/overview")
    assert ov_res.status_code == 200
    ov_data = ov_res.json()
    assert ov_data["loaded"] is True
    assert "yield_summary" in ov_data

    # Data Quality
    dq_res = client.get("/api/data-quality")
    assert dq_res.status_code == 200

    # Yield
    y_res = client.get("/api/yield")
    assert y_res.status_code == 200

    # Anomalies
    a_res = client.get("/api/anomalies")
    assert a_res.status_code == 200

    # Prediction API
    pred_res = client.post("/api/predict", json={
        "Device_ID": "DEV_API_TEST",
        "Test_ID": "T101_LEAKAGE",
        "Test_Name": "Standby Leakage Current",
        "Lot_ID": "LOT_2026A",
        "Wafer_ID": "W01",
        "VDD_V": 1.2,
        "Temperature_C": 25.0,
        "Measured_Value": 2.5,
        "Lower_Limit": 0.05,
        "Upper_Limit": 5.00,
        "Retest_Count": 0
    })
    assert pred_res.status_code == 200
    pdata = pred_res.json()
    assert pdata["prediction"] in ["PASS", "FAIL"]
