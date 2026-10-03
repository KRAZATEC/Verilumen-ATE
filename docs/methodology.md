# Verilumen ATE Intelligence Platform — Architecture & Methodology

## 1. High-Level Architecture

```text
       ┌────────────────────────┐
       │   ATE Telemetry CSV    │
       └───────────┬────────────┘
                   │
                   ▼
       ┌────────────────────────┐
       │   Schema Validation    │ (Canonical ATE contract & alias tolerance)
       └───────────┬────────────┘
                   │
                   ▼
       ┌────────────────────────┐
       │  Data Quality Engine   │ (Audit trail, missing imputation, exact deduplication)
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
│  FastAPI API  │     │ Streamlit/UI  │
└───────────────┘     └───────────────┘
```

## 2. Methodology & Engineering Decisions

### 2.1 Schema Contract & Dataset Agnosticism

- Supports canonical ATE fields: `Device_ID`, `Test_ID`, `Test_Name`, `Lot_ID`, `Wafer_ID`, `VDD_V`, `Temperature_C`, `Measured_Value`, `Lower_Limit`, `Upper_Limit`, `Result`, `Failure_Mode`, `Retest_Count`.
- Tolerates common industry aliases (e.g., `temp` -> `Temperature_C`, `ll` -> `Lower_Limit`, `val` -> `Measured_Value`).
- **Never assumes hard-coded values**: No fixed row count, hard-coded lot IDs, or hard-coded yields. All metrics are computed dynamically.

### 2.2 Data Quality & Preprocessing

- **Raw Data Preservation**: The raw dataframe is never mutated in place. Clean layers are created with complete audit logs.
- **Deduplication Policy**: Exact duplicate rows are detected, quantified, and filtered in the clean layer while retaining the original records.
- **Missing Values**: Type-aware imputation (median for continuous physical measurements to preserve robust central tendencies; explicit categories such as `"UNKNOWN"` or `"NONE"` for categorical fields).
- **Outliers**: Combines Tukey IQR (1.5x span) with direct electrical specification boundary tests (`Measured_Value < Lower_Limit` or `> Upper_Limit`).

### 2.3 Yield & Failure Analysis

- Deterministic formula calculation:
  $$\text{PASS Yield} = \frac{\text{PASS records}}{\text{Valid records}} \times 100$$
- Grouped multi-dimensional yields computed dynamically across `Lot_ID`, `Wafer_ID`, and `Test_ID`.
- Pareto failure rankings reporting both failure count and failure rate percentage to avoid misleading conclusions from low-volume tests.

### 2.4 Machine Learning Classification & Leakage Prevention

- **Target Definition**: Binary test outcome `Result` (FAIL = 1, PASS = 0).
- **Strict Leakage Prevention**: `Result` and `Failure_Mode` are strictly excluded from predictive matrices ($X$).
- **Stratified Group Validation**: `StratifiedGroupKFold` grouped by `Device_ID` ensures that multiple test measurements from the same physical silicon die do not leak across training and validation splits.
- **Class Imbalance**: Semiconductor testing exhibits sharp class imbalance (~93% PASS, ~7% FAIL). Balanced class weighting (`class_weight='balanced'`) is applied to all estimators, and performance is evaluated using PR-AUC, F1-Score, and ROC-AUC rather than raw accuracy.
- **Multi-Model Comparison**: Evaluates 3 distinct architectures:
  1. _Logistic Regression_ (Linear interpretable baseline)
  2. _HistGradientBoosting_ (Fast modern gradient boosting ensemble)
  3. _Random Forest_ (Challenger non-linear bagging ensemble)

### 2.5 Multi-Layer Anomaly Detection

- **Layer 1 (Statistical & Limits)**: Group-level Median Absolute Deviation (MAD), modified Z-score, and normalized specification boundary proximity.
- **Layer 2 (Multivariate Isolation Forest)**: Evaluates high-dimensional density across continuous electrical and thermal dimensions.
- **Unified Anomaly Score (0–100)**: Blends statistical deviation (40 pts), spec boundary proximity/violation (35 pts), and isolation forest score (25 pts).
- Distinguishes **Golden Anomalies** (devices passing specification limits but exhibiting abnormal parametric drift) from catastrophic failures.

### 2.6 Evidence Engine & Causal Boundaries

- The central reasoning engine strictly separates:
  - **Deterministic Observed Evidence**: Direct physical measurements, test limits, thermal corners, and retest counts.
  - **Inferred Hypotheses**: Engineering hypotheses regarding silicon process variation, thermal stress, or socket probe contact wear.
  - **Limitations & Unknowns**: Explicitly states that physical failure analysis (SEM/TEM/EMMI) and inline fab metrology are necessary for conclusive physical causation.
  - Returns `"Insufficient evidence for a reliable engineering interpretation."` when data points are lacking.
