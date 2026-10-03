from typing import Optional
from fastapi import APIRouter, HTTPException, Query
import pandas as pd
from backend.app.services.session import session_store
from backend.app.explainability.evidence_engine import build_evidence_analysis
from backend.app.explainability.narrative import generate_narrative_text

router = APIRouter(prefix="", tags=["Investigation"])


@router.get("/investigation/devices")
def get_device_list(limit: int = 50):
    if not session_store.is_loaded():
        raise HTTPException(status_code=400, detail="No dataset loaded.")
    df = session_store.annotated_df
    devices = df["Device_ID"].dropna().unique().tolist()
    return {"devices": devices[:limit]}


@router.get("/investigation/tests")
def get_test_list():
    if not session_store.is_loaded():
        raise HTTPException(status_code=400, detail="No dataset loaded.")
    df = session_store.annotated_df
    tests = df[["Test_ID", "Test_Name"]].drop_duplicates().to_dict(orient="records")
    return {"tests": tests}


@router.get("/investigation/device/{device_id}")
def investigate_device(device_id: str):
    if not session_store.is_loaded():
        raise HTTPException(status_code=400, detail="No dataset loaded.")

    df = session_store.annotated_df
    matches = df[df["Device_ID"] == device_id]
    if matches.empty:
        raise HTTPException(status_code=404, detail=f"Device {device_id} not found in current dataset.")

    records = matches.to_dict(orient="records")
    return {
        "device_id": device_id,
        "lot_id": str(matches["Lot_ID"].iloc[0]),
        "wafer_id": str(matches["Wafer_ID"].iloc[0]),
        "total_tests_logged": len(matches),
        "fails_count": int((matches["Result"].str.upper() == "FAIL").sum()),
        "max_anomaly_score": float(matches["anomaly_score"].max()) if "anomaly_score" in matches.columns else 0.0,
        "records": records,
    }


@router.get("/investigation/record")
def investigate_specific_record(
    device_id: str = Query(...),
    test_id: str = Query(...)
):
    if not session_store.is_loaded():
        raise HTTPException(status_code=400, detail="No dataset loaded.")

    df = session_store.annotated_df
    match = df[(df["Device_ID"] == device_id) & (df["Test_ID"] == test_id)]
    if match.empty:
        raise HTTPException(status_code=404, detail="Specific test record not found for this device.")

    record_dict = match.iloc[0].to_dict()
    anom_score = float(record_dict.get("anomaly_score", 0.0))

    # Evidence engine integration
    report = build_evidence_analysis(
        record=record_dict,
        overall_yield_fail_rate=session_store.yield_summary.fail_rate_pct if session_store.yield_summary else 7.0,
        anomaly_score=anom_score,
    )
    narrative = generate_narrative_text(report)

    return {
        "record": record_dict,
        "ai_analysis": report.model_dump(),
        "narrative": narrative,
    }
