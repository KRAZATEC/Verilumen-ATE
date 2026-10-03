# Verilumen ATE Intelligence Platform

[![Assessment Audit](https://img.shields.io/badge/Assessment%20Audit-100%25%20PASS-brightgreen)](reports/final_assessment_audit.md)
[![Test Suite](https://img.shields.io/badge/pytest-11%2F11%20passing-brightgreen)](tests/)
[![Python](https://img.shields.io/badge/Python-3.11%2B-blue)](backend/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Production%20Ready-teal)](backend/app/main.py)
[![Docker](https://img.shields.io/badge/Docker-Compose%20Ready-blue)](docker-compose.yml)

> **Verilumen Labs AI Engineer Assessment Project**
> An end-to-end semiconductor automated test equipment (ATE) diagnostic platform that identifies data-quality anomalies, profiles multi-lot wafer yield, trains leakage-safe failure classifiers, isolates marginal silicon defects, and provides evidence-grounded engineering explanations.

---

## 1. Executive Summary & Problem Statement

Semiconductor testing generates vast quantities of automated test equipment (ATE) parametric records. Identifying silicon yield loss, spatial lot/wafer variations, subtle parametric drifts, and intermittent contact chatter is essential for production fab operations.

This platform delivers:
1. **Dynamic Data Quality & Profiling**: Automated schema contract validation, duplicate handling policies, and type-aware imputation tracking.
2. **Deterministic Yield & Failure Mode Analytics**: Lot, wafer, and test-level PASS yield and FAIL rate calculations, Pareto failure modes, and automated engineering summaries.
3. **Leakage-Safe ML Failure Classification**: Multi-model comparison (Logistic Regression, HistGradientBoosting, Random Forest) with `StratifiedGroupKFold` cross-validation grouped by `Device_ID` and balanced class weighting.
4. **Multi-Layer Anomaly Detection**: Blends group-level Median Absolute Deviation (MAD), specification proximity/violation, and multivariate Isolation Forest into an actionable 0–100 Anomaly Score.
5. **Central Evidence Engine & Causality Distinction**: Strictly separates observed physical telemetry evidence from inferred hypotheses, and explicitly states causal limitations.
6. **Production Interfaces**: RESTful FastAPI backend and an interactive Streamlit engineering console, with Next.js frontend scaffolding.

---

## 2. System Architecture

```text
       ┌────────────────────────┐
       │   ATE Telemetry CSV    │ (Assessment / Synthetic Dataset)
       └───────────┬────────────┘
                   │
                   ▼
       ┌────────────────────────┐
       │   Schema Validation    │ (Canonical ATE contract & alias tolerance)
       └───────────┬────────────┘
                   │
                   ▼
       ┌────────────────────────┐
       │  Data Quality Engine   │ (Preserves raw; tracks imputation & deduplication)
       └───────────┬────────────┘
                   │
      ┌────────────┼───────────────────────────┐
      ▼            ▼                           ▼
┌───────────┐┌───────────┐               ┌───────────┐
│   Yield   ││    ML     │               │  Anomaly  │
│ Analytics ││ Pipeline  │               │  Engine   │
└─────┬─────┘└─────┬─────┘               └─────┬─────┘
      │            │                           │
      └────────────┼───────────────────────────┘
                   ▼
       ┌────────────────────────┐
       │     Evidence Engine    │ (Strict separation of facts vs inferred hypotheses)
       └───────────┬────────────┘
                   │
        ┌──────────┴──────────┐
        ▼                     ▼
┌───────────────┐     ┌───────────────┐
│  FastAPI API  │     │ Streamlit UI  │
└───────────────┘     └───────────────┘
```

---

## 3. Technology Stack

- **Backend**: Python 3.11+, FastAPI, Pydantic v2, Uvicorn, Pandas, NumPy, Scipy, Scikit-learn, Joblib.
- **Console & Visualizations**: Streamlit, Recharts/Next.js UI.
- **Testing & Quality Gates**: pytest, automated assessment audit script.
- **Infrastructure**: Docker, Docker Compose.

---

## 4. Key Engineering Methodologies

### 4.1 Canonical Schema Contract & Dataset Agnosticism
The platform adheres to the canonical ATE logical schema:
- `Device_ID`, `Test_ID`, `Test_Name`, `Lot_ID`, `Wafer_ID`
- `VDD_V`, `Temperature_C`, `Measured_Value`, `Lower_Limit`, `Upper_Limit`
- `Result`, `Failure_Mode`, `Retest_Count`

**Zero Hard-coding**: No metric, test name, wafer count, or failure mode is hard-coded into the pipeline. If a new CSV conforming to the schema is provided, the platform dynamically computes all reports and models.

### 4.2 Data Quality & Deduplication Policy
- **Raw Data Preservation**: Uploaded raw dataframes are never mutated in place.
- **Deduplication**: Exact duplicate records are detected, quantified, and filtered during clean-layer creation.
- **Missing Values**: Handled via robust type-aware policies (median imputation for continuous physical metrics; explicit categories like `"UNKNOWN"` for categorical fields).
- **Outlier Strategy**: Combines Tukey IQR (1.5x span) with direct electrical specification boundary tests (`Measured_Value < Lower_Limit` or `> Upper_Limit`).

### 4.3 Leakage-Safe Feature Engineering & ML Pipeline
- **Strict Leakage Prevention**: Outcome fields (`Result`, `Failure_Mode`) are permanently audited and excluded from model feature matrices.
- **Stratified Group Validation**: Validation utilizes `StratifiedGroupKFold` grouped by `Device_ID` to prevent measurements from the same physical silicon die from leaking across folds.
- **Class Imbalance**: Imbalance (~93% PASS, ~7% FAIL) is mitigated using `class_weight='balanced'`, evaluated primarily on PR-AUC, F1-Score, and ROC-AUC.
- **Model Comparison**: Benchmarks Logistic Regression (baseline), HistGradientBoosting (primary), and Random Forest (challenger).

### 4.4 Multi-Layer Anomaly Detection
- Blends group-level MAD deviations (40 pts), specification boundary proximity/violations (35 pts), and multivariate Isolation Forest scores (25 pts) into a documented 0–100 composite score.
- Categorizes **Golden Anomalies** (devices passing specification limits but exhibiting abnormal parametric drift) to mitigate field reliability risks.

### 4.5 Evidence Engine & Causal Boundaries
- Adheres to the principle that **observed evidence and inferred causes must be separated**.
- Deterministic measurements are reported as factual observations.
- Inferred failure hypotheses (e.g., thermal carrier mobility degradation, socket contact chatter) are labeled as hypotheses.
- Explicitly states causal limitations (e.g., lack of SEM/TEM/EMMI inline metrology) and declares when evidence is insufficient.

---

## 5. Quickstart & Installation

### Option A: Local Execution (Recommended)

1. **Setup Python Environment**:
   ```bash
   pip install -r backend/requirements.txt streamlit
   ```

2. **Generate Development Dataset** (12,000+ realistic multi-lot records):
   ```bash
   python backend/scripts/generate_demo_data.py --rows 12000 --seed 42
   ```

3. **Run the Full Test Suite**:
   ```bash
   pytest
   ```

4. **Execute Formal Assessment Compliance Audit**:
   ```bash
   python backend/scripts/run_assessment_audit.py
   ```

5. **Launch Interactive Engineering Console**:
   ```bash
   streamlit run backend/app/streamlit_app.py
   ```
   *Console will be accessible at: `http://localhost:8501`*

6. **Start FastAPI REST Server**:
   ```bash
   uvicorn backend.app.main:app --reload --port 8000
   ```
   *Interactive Swagger Documentation: `http://localhost:8000/docs`*

---

### Option B: Docker Compose

Launch the complete containerized stack:
```bash
docker compose up --build
```
- FastAPI REST Backend: `http://localhost:8000`
- Streamlit Engineering Console: `http://localhost:8502`

---

## 6. Demonstration Workflow (5–10 Minutes)

See [`docs/demo_script.md`](docs/demo_script.md) for a detailed walkthrough:
1. **Overview & Upload**: Ingest synthetic ATE data or upload a custom CSV.
2. **Data Quality Audit**: Review missing value imputation audits, exact duplicate counts, and Tukey outlier ranges.
3. **Yield & Failure Pareto**: Explore grouped yield breakdowns across Lots, Wafers, and Tests, as well as common failure modes.
4. **Multi-Layer Anomaly Engine**: Inspect top-ranked suspicious records and Golden PASS anomalies.
5. **DUT Investigation & Evidence Engine**: Select a specific device to inspect executed tests, and review structured observed evidence vs inferred hypotheses.
6. **ML Inference**: Submit an unseen telemetry record to observe real-time classification, probability, and feature attribution.

---

## 7. Compliance Traceability Matrix

Detailed requirement mappings are documented in [`docs/requirements_traceability.md`](docs/requirements_traceability.md). All 7 primary assessment gates pass with 100% compliance:

```text
[PASS] Schema Compliance & Scale: Valid canonical schema with 12,180 rows across 13 columns.
[PASS] Data Quality & Duplicate Policy: Detected 180 duplicates; handled via clean layer policy.
[PASS] Yield & Failure Intelligence: Yield: 92.78%, Fail: 7.22%. Computed groups for Lot, Wafer, Test, and failure modes.
[PASS] Data Leakage Audit: Strict exclusion of Result and Failure_Mode from predictive matrices confirmed.
[PASS] ML Model Comparison & Imbalance Handling: Trained 3 classifiers with balanced weighting and StratifiedGroupKFold.
[PASS] Anomaly Detection & Ranking Layer: Statistical + Isolation Forest composite score (0-100).
[PASS] Evidence Grounding & Causality Separation: Strict separation of facts from hypotheses with explicit limitations.
```

---

## 8. Real CSV Integration Procedure

When the official assessment CSV is provided:
1. Run schema compatibility: `python -c "from backend.app.data.ingestion import *; ..."`
2. Place the file at `data/assessment_ate_data.csv` (or upload via the UI).
3. The platform will automatically normalize aliases, profile quality, clean records, compute yield, train models, and detect anomalies without code modifications.

---

## 9. Engineering Limitations

- **Physical Causality**: Tester parametric measurements alone cannot establish root physical silicon defects (e.g., gate oxide pinholes or metallization voids) without inline fab metrology or destructive physical failure analysis (SEM/TEM).
- **Measurement Guardbands**: Borderline passes may experience test escape risks under extreme operational temperature corners.

