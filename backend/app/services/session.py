"""
Session & Data Pipeline Manager:
Manages in-memory / local session state for uploaded datasets, clean layers,
yield summaries, anomaly models, and trained ML pipelines.
Enables instant zero-latency dashboard queries and multi-step investigation.
"""

from typing import Optional, Dict, Any
import pandas as pd
from backend.app.data.schema import SchemaValidationReport
from backend.app.analytics.quality import DataQualityReport
from backend.app.analytics.yield_analysis import OverallYieldSummary, YieldGroupRecord
from backend.app.analytics.failures import FailureModeRecord, TopFailingTest
from backend.app.analytics.summaries import EngineeringSummary
from backend.app.anomaly.scoring import AnomalySummary


class SessionState:
    def __init__(self):
        self.raw_df: Optional[pd.DataFrame] = None
        self.clean_df: Optional[pd.DataFrame] = None
        self.annotated_df: Optional[pd.DataFrame] = None
        self.dataset_id: Optional[str] = None
        self.filename: Optional[str] = None
        self.schema_report: Optional[SchemaValidationReport] = None
        self.quality_report: Optional[DataQualityReport] = None
        self.yield_summary: Optional[OverallYieldSummary] = None
        self.lot_yields: Optional[list[YieldGroupRecord]] = None
        self.wafer_yields: Optional[list[YieldGroupRecord]] = None
        self.test_yields: Optional[list[YieldGroupRecord]] = None
        self.top_failing_tests: Optional[list[TopFailingTest]] = None
        self.failure_modes: Optional[list[FailureModeRecord]] = None
        self.engineering_summary: Optional[EngineeringSummary] = None
        self.anomaly_summary: Optional[AnomalySummary] = None
        self.ml_results: Optional[Dict[str, Any]] = None

    def is_loaded(self) -> bool:
        return self.raw_df is not None and not self.raw_df.empty


# Global singleton session for local development
session_store = SessionState()
