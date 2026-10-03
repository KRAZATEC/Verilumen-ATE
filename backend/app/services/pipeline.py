"""
End-to-End Analytics & ML Pipeline Execution Service:
Runs the sequence:
1. Ingestion & Schema Validation
2. Data Quality Audit & Clean Layer Creation
3. Deterministic Yield & Failure Analytics
4. Multi-Layer Anomaly Detection & Ranking
5. ML Model Training & Grouped Evaluation
6. Engineering Summary Synthesis
"""

import uuid
from typing import Dict, Any, Union, BinaryIO
import pandas as pd
from backend.app.core.logging import logger
from backend.app.data.ingestion import load_csv, normalize_column_names, validate_schema
from backend.app.data.preprocessing import clean_dataset
from backend.app.analytics.quality import run_data_quality_audit
from backend.app.analytics.yield_analysis import compute_overall_yield, compute_grouped_yield
from backend.app.analytics.failures import analyze_failure_modes, identify_top_failing_tests
from backend.app.analytics.summaries import generate_engineering_summary
from backend.app.anomaly.scoring import detect_and_score_anomalies
from backend.app.ml.train import train_and_compare_models
from backend.app.services.session import session_store


def process_dataset(file_or_path: Union[str, BinaryIO, bytes], filename: str = "uploaded_dataset.csv") -> Dict[str, Any]:
    logger.info(f"Processing dataset '{filename}'...")
    
    # 1. Ingestion
    raw_df = load_csv(file_or_path)
    norm_df, aliases_used = normalize_column_names(raw_df)
    
    # 2. Schema Validation
    schema_report = validate_schema(norm_df)
    if not schema_report.is_valid:
        logger.warning(f"Schema validation reported errors: {schema_report.errors}")

    # 3. Data Quality Audit
    quality_report = run_data_quality_audit(norm_df)

    # 4. Clean Layer Creation
    clean_df, clean_audit = clean_dataset(norm_df, drop_exact_duplicates=True)

    # 5. Deterministic Yield Analytics
    yield_summary = compute_overall_yield(clean_df)
    lot_yields = compute_grouped_yield(clean_df, "Lot_ID")
    wafer_yields = compute_grouped_yield(clean_df, "Wafer_ID")
    test_yields = compute_grouped_yield(clean_df, "Test_ID")

    # 6. Failure Modes & Top Failing Tests
    top_fails = identify_top_failing_tests(clean_df, top_n=10)
    fail_modes = analyze_failure_modes(clean_df)

    # 7. Anomaly Engine
    annotated_df, anom_summary = detect_and_score_anomalies(clean_df)

    # 8. ML Classifier Training (if sufficient rows & target classes)
    ml_results = None
    try:
        ml_results = train_and_compare_models(clean_df, scenario="Scenario B - Measurement-Aware")
    except Exception as e:
        logger.warning(f"ML Model training skipped or failed: {str(e)}")

    # 9. Engineering Summary
    eng_summary = generate_engineering_summary(
        yield_summary=yield_summary,
        lot_yields=lot_yields,
        wafer_yields=wafer_yields,
        top_fails=top_fails,
        fail_modes=fail_modes,
        quality_report=quality_report,
    )

    # Store in session
    session_store.raw_df = raw_df
    session_store.clean_df = clean_df
    session_store.annotated_df = annotated_df
    session_store.dataset_id = str(uuid.uuid4())
    session_store.filename = filename
    session_store.schema_report = schema_report
    session_store.quality_report = quality_report
    session_store.yield_summary = yield_summary
    session_store.lot_yields = lot_yields
    session_store.wafer_yields = wafer_yields
    session_store.test_yields = test_yields
    session_store.top_failing_tests = top_fails
    session_store.failure_modes = fail_modes
    session_store.engineering_summary = eng_summary
    session_store.anomaly_summary = anom_summary
    session_store.ml_results = ml_results

    logger.info(f"Dataset '{filename}' successfully ingested and processed. Total records: {len(clean_df)}")

    return {
        "dataset_id": session_store.dataset_id,
        "filename": filename,
        "total_records": len(clean_df),
        "schema_valid": schema_report.is_valid,
        "health_score": quality_report.overall_health_score,
        "overall_yield": yield_summary.pass_yield_pct,
        "best_ml_model": ml_results.get("best_model") if ml_results else "None",
        "total_anomalies": anom_summary.total_anomalies_flagged,
    }
