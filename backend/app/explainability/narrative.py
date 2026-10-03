"""
Narrative Generation:
Converts structured evidence objects into clear, engineering-grade diagnostic text.
Strictly preserves the distinction between deterministic facts and inferred causes.
"""

from typing import Dict, Any
from backend.app.explainability.evidence_engine import AIAnalysisReport


def generate_narrative_text(report: AIAnalysisReport) -> str:
    lines = []
    lines.append("=== ATE SEMICONDUCTOR FAILURE INTELLIGENCE REPORT ===")
    lines.append(f"Target: Device {report.device_id} | Test: {report.test_id} | Lot: {report.lot_id} | Wafer: {report.wafer_id}")
    lines.append(f"Recorded Result: {report.observed_result} | Logged Failure Mode: {report.recorded_failure_mode}")
    lines.append(f"Diagnostic Confidence: {report.confidence_level}\n")
    
    lines.append("--- 1. DETERMINISTIC OBSERVED EVIDENCE ---")
    if not report.observed_evidence:
        lines.append("  (No abnormal physical telemetry points detected)")
    for ev in report.observed_evidence:
        lines.append(f"  [{ev.category}]: {ev.finding}")
        
    lines.append("\n--- 2. MODEL & ANOMALY SIGNALS ---")
    lines.append(f"  Model Failure Probability: {report.model_evidence.get('predicted_probability_fail')}")
    lines.append(f"  Anomaly Composite Score: {report.anomaly_evidence.get('anomaly_score')}")

    lines.append("\n--- 3. POSSIBLE ENGINEERING INTERPRETATIONS ---")
    for interp in report.possible_interpretations:
        lines.append(f"  * {interp}")

    lines.append("\n--- 4. LIMITATIONS & UNKNOWNS ---")
    for lim in report.limitations_and_unknowns:
        lines.append(f"  ! {lim}")

    return "\n".join(lines)
