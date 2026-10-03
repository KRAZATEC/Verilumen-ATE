# Verilumen ATE Intelligence Platform — Demonstration Script

This walkthrough guides an evaluator through a 5–10 minute demonstration of the Verilumen ATE Intelligence platform.

---

## Step 1: Problem & Architecture (1 Minute)

- **Problem**: Modern semiconductor manufacturing generates millions of Automated Test Equipment (ATE) records. Engineers must detect data quality glitches, analyze yield across lots and wafers, isolate failing tests, detect anomalies before catastrophic failure, and predict test outcomes on new units.
- **Architecture**:
  `CSV Upload` &rarr; `Schema Validation & Data Quality` &rarr; `Yield & Pareto Analytics` &rarr; `ML Models & Anomaly Engine` &rarr; `Evidence Engine` &rarr; `FastAPI REST Backend & Interactive UI`.

---

## Step 2: Ingestion & Data Quality Audit (2 Minutes)

1. Launch the interactive console:
   ```bash
   streamlit run backend/app/streamlit_app.py
   ```
2. Navigate to the **Data Quality** tab:
   - Observe the **Schema Validation** report confirming canonical schema compliance.
   - Show the **Duplicate Detection** metric: 180 exact redundant records detected and handled via the clean layer policy.
   - Inspect the **Missing Values & Imputation Audit** table displaying column-by-column missing counts and applied strategies (median for continuous metrics, explicit categories for test classifications).
   - Review the **Tukey Outlier Thresholds** and specification boundary violations.

---

## Step 3: Yield Breakdown & Pareto Failure Modes (2 Minutes)

1. Open the **Yield & Failures** tab:
   - Review overall yield metrics (PASS Yield: ~92.8%, FAIL Rate: ~7.2%, Retest Rate: ~6.2%).
   - Switch between **Lot_ID**, **Wafer_ID**, and **Test_ID** grouped yield views. Notice that `LOT_2026D` shows an elevated failure rate due to simulated process drift.
   - Inspect the Pareto chart of **Top Failing Tests** and the **Failure Mode Distribution** (TIMING_VIOLATION, POWER_ANOMALY, SIGNAL_INTEGRITY, etc.).

---

## Step 4: Multi-Layer Anomaly Detection (1.5 Minutes)

1. Open the **Anomalies** tab:
   - Explain the dual-layer detection: Group-level MAD / Modified Z-Scores + Multivariate Isolation Forest.
   - Inspect the **Ranked Suspicious Records** table.
   - Point out **Suspicious Golden PASS** records: units that met specification limits but showed severe statistical deviation, posing field reliability hazards.

---

## Step 5: Device Investigation & Evidence Engine (2 Minutes)

1. Open the **Investigation** tab:
   - Select a Device Under Test (e.g., `DEV_LOT_2026D_W04_00451`).
   - Inspect all executed tests for that device alongside limits and results.
2. Open the **AI Evidence** tab:
   - Show how the Evidence Engine strictly separates:
     - **Observed Physical Evidence (Facts)**
     - **Inferred Hypotheses & Possible Causes**
     - **Limitations & Unknowns**
   - Point out that the engine explicitly states causal boundaries rather than fabricating physical root causes.

---

## Step 6: ML Prediction on Unseen Units & Model Benchmarking (1.5 Minutes)

1. Open the **ML Prediction** tab:
   - Fill in an unseen test record with marginal parameters (e.g., temperature 95°C, measurement near upper limit).
   - Click **Execute Real-Time Model Inference**.
   - Show the predicted outcome, calibrated failure probability, and feature attribution explanation.
2. Open the **Model Comparison** tab:
   - Compare the 3 trained architectures (Logistic Regression, HistGradientBoosting, Random Forest).
   - Show cross-validation metrics under `StratifiedGroupKFold` (PR-AUC, F1-Score, ROC-AUC).
   - Highlight the class imbalance mitigation with balanced sample weighting.
