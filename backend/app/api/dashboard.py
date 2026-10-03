from fastapi import APIRouter, HTTPException
from backend.app.services.session import session_store

router = APIRouter(prefix="", tags=["Dashboard"])


@router.get("/overview")
def get_overview():
    if not session_store.is_loaded():
        return {"loaded": False, "message": "No dataset currently loaded."}

    return {
        "loaded": True,
        "filename": session_store.filename,
        "dataset_id": session_store.dataset_id,
        "yield_summary": session_store.yield_summary.model_dump() if session_store.yield_summary else None,
        "quality_score": session_store.quality_report.overall_health_score if session_store.quality_report else None,
        "total_anomalies": session_store.anomaly_summary.total_anomalies_flagged if session_store.anomaly_summary else 0,
        "anomaly_rate": session_store.anomaly_summary.anomaly_rate_pct if session_store.anomaly_summary else 0.0,
        "engineering_summary": session_store.engineering_summary.model_dump() if session_store.engineering_summary else None,
    }


@router.get("/data-quality")
def get_data_quality():
    if not session_store.is_loaded():
        raise HTTPException(status_code=400, detail="No dataset loaded. Please upload a CSV first.")
    
    return {
        "schema_report": session_store.schema_report.model_dump() if session_store.schema_report else None,
        "quality_report": session_store.quality_report.model_dump() if session_store.quality_report else None,
    }


@router.get("/yield")
def get_yield_analytics():
    if not session_store.is_loaded():
        raise HTTPException(status_code=400, detail="No dataset loaded. Please upload a CSV first.")

    return {
        "overall": session_store.yield_summary.model_dump() if session_store.yield_summary else None,
        "by_lot": [y.model_dump() for y in (session_store.lot_yields or [])],
        "by_wafer": [y.model_dump() for y in (session_store.wafer_yields or [])],
        "by_test": [y.model_dump() for y in (session_store.test_yields or [])],
    }


@router.get("/failures")
def get_failure_analytics():
    if not session_store.is_loaded():
        raise HTTPException(status_code=400, detail="No dataset loaded. Please upload a CSV first.")

    return {
        "top_failing_tests": [t.model_dump() for t in (session_store.top_failing_tests or [])],
        "failure_modes": [m.model_dump() for m in (session_store.failure_modes or [])],
    }


@router.get("/anomalies")
def get_anomalies():
    if not session_store.is_loaded():
        raise HTTPException(status_code=400, detail="No dataset loaded. Please upload a CSV first.")

    return session_store.anomaly_summary.model_dump() if session_store.anomaly_summary else {}


@router.get("/model-performance")
def get_model_performance():
    if not session_store.is_loaded() or not session_store.ml_results:
        raise HTTPException(status_code=400, detail="No trained ML models available. Please upload data first.")

    return session_store.ml_results
