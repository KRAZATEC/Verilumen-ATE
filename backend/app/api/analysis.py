from typing import Dict, Any
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from backend.app.explainability.evidence_engine import build_evidence_analysis, AIAnalysisReport
from backend.app.explainability.narrative import generate_narrative_text

router = APIRouter(prefix="", tags=["AI Analysis"])


class AnalysisRequest(BaseModel):
    record: Dict[str, Any]


@router.post("/analysis/explain")
def analyze_and_explain(req: AnalysisRequest):
    try:
        report = build_evidence_analysis(req.record)
        narrative = generate_narrative_text(report)
        return {
            "analysis_report": report.model_dump(),
            "narrative": narrative,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
