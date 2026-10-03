"""
Concise, evidence-grounded Engineering Summaries for Task 1:
- Automatically synthesizes key engineering observations
- Strictly distinguishes observed data evidence from inferred physical hypotheses
- Flags limitations and areas of insufficient evidence
"""

from typing import List, Dict, Any
from pydantic import BaseModel
from backend.app.analytics.yield_analysis import OverallYieldSummary, YieldGroupRecord
from backend.app.analytics.failures import FailureModeRecord, TopFailingTest
from backend.app.analytics.quality import DataQualityReport


class EngineeringSummary(BaseModel):
    dataset_overview: Dict[str, Any]
    quality_findings: Dict[str, Any]
    yield_findings: Dict[str, Any]
    top_failing_tests: List[Dict[str, Any]]
    dominant_failure_modes: List[Dict[str, Any]]
    key_observations: List[str]
    limitations_and_caveats: List[str]


def generate_engineering_summary(
    yield_summary: OverallYieldSummary,
    lot_yields: List[YieldGroupRecord],
    wafer_yields: List[YieldGroupRecord],
    top_fails: List[TopFailingTest],
    fail_modes: List[FailureModeRecord],
    quality_report: DataQualityReport,
) -> EngineeringSummary:
    observations = []
    limitations = []

    # 1. Overall Yield Observation
    observations.append(
        f"Overall PASS Yield is {yield_summary.pass_yield_pct}% (FAIL Rate: {yield_summary.fail_rate_pct}%) "
        f"across {yield_summary.total_records:,} test executions on {yield_summary.total_devices:,} devices."
    )

    # 2. Lot & Wafer variations
    if lot_yields:
        lowest_lot = lot_yields[0]
        if lowest_lot.fail_rate_pct > (yield_summary.fail_rate_pct * 1.25):
            observations.append(
                f"Lot {lowest_lot.group_value} exhibited an elevated failure rate of {lowest_lot.fail_rate_pct}% "
                f"compared to baseline average ({yield_summary.fail_rate_pct}%)."
            )

    # 3. Top Failing Test
    if top_fails:
        worst_test = top_fails[0]
        observations.append(
            f"Primary failure contributor is '{worst_test.test_name}' ({worst_test.test_id}) "
            f"with {worst_test.fail_count} failures ({worst_test.fail_rate_pct}% failure rate), "
            f"predominantly driven by {worst_test.dominant_failure_mode}."
        )

    # 4. Failure Modes
    if fail_modes:
        top_mode = fail_modes[0]
        observations.append(
            f"The dominant recorded failure mode is '{top_mode.failure_mode}', accounting for "
            f"{top_mode.percentage_of_failures}% of all observed test failures."
        )

    # 5. Retest impact
    if yield_summary.retest_rate_pct > 0:
        observations.append(
            f"Retest rate is {yield_summary.retest_rate_pct}%, indicating contact chatter or marginal spec recoveries."
        )

    # Limitations & Rigor
    limitations.append(
        "Identified correlations between lots/wafers and failure modes are observational and do not constitute root-cause proof."
    )
    if quality_report.duplicate_summary.total_duplicate_rows > 0:
        limitations.append(
            f"Data ingestion noted {quality_report.duplicate_summary.total_duplicate_rows} duplicate rows which were filtered in the clean layer."
        )
    limitations.append(
        "Conclusions are grounded strictly in the supplied dataset schema; external inline fab metrology or packaging data is unavailable."
    )

    return EngineeringSummary(
        dataset_overview={
            "records": yield_summary.total_records,
            "devices": yield_summary.total_devices,
            "lots": yield_summary.total_lots,
            "wafers": yield_summary.total_wafers,
            "tests": yield_summary.total_tests,
        },
        quality_findings={
            "health_score": quality_report.overall_health_score,
            "duplicates": quality_report.duplicate_summary.total_duplicate_rows,
            "caveats": quality_report.engineering_caveats,
        },
        yield_findings={
            "pass_yield": yield_summary.pass_yield_pct,
            "fail_rate": yield_summary.fail_rate_pct,
            "retest_rate": yield_summary.retest_rate_pct,
        },
        top_failing_tests=[t.model_dump() for t in top_fails[:5]],
        dominant_failure_modes=[f.model_dump() for f in fail_modes[:5]],
        key_observations=observations,
        limitations_and_caveats=limitations,
    )
