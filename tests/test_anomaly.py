import pytest
import pandas as pd
from backend.app.anomaly.scoring import detect_and_score_anomalies
from backend.app.explainability.evidence_engine import build_evidence_analysis


def test_anomaly_and_evidence():
    df = pd.read_csv("data/demo_ate_data.csv").head(500)
    annotated_df, anom_summary = detect_and_score_anomalies(df)
    assert anom_summary.total_records_analyzed == len(df)
    assert anom_summary.total_anomalies_flagged >= 0
    assert 0.0 <= anom_summary.max_anomaly_score <= 100.0

    # Evidence engine on flagged record
    rec = df.iloc[0].to_dict()
    analysis = build_evidence_analysis(rec, overall_yield_fail_rate=7.2, anomaly_score=85.0)
    assert analysis.confidence_level in ["HIGH", "MEDIUM", "LOW", "INSUFFICIENT"]
    assert len(analysis.limitations_and_unknowns) > 0
    # Strict separation
    assert isinstance(analysis.observed_evidence, list)
    assert isinstance(analysis.possible_interpretations, list)
