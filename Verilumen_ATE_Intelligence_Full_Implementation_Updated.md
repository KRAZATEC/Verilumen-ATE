# Verilumen ATE Intelligence Platform — Full Implementation Specification

## 1. Purpose

Build a production-style AI engineering application for the Verilumen Labs AI Engineer Fresher assessment.

The application must analyze ATE semiconductor test data, identify data-quality problems, calculate yield/failure intelligence, predict PASS/FAIL outcomes, detect anomalies, investigate devices/tests, and produce evidence-grounded engineering explanations.

The real assessment CSV will be supplied later. Development must therefore use a high-fidelity synthetic replica dataset and a strict schema contract. The implementation must remain dataset-agnostic and must work with a new CSV having the same schema.

This document is the master implementation plan. It should be followed phase-by-phase and used as the basis for implementation prompts, coding, testing, and final assessment validation.

---

# 2. Assessment Requirements Covered

The implementation must cover every requirement stated in the assessment:

## Candidate instructions

- Use the supplied CSV as the primary assessment dataset.
- AI coding assistants are permitted.
- Submitted code must be understandable and explainable by the candidate.
- Do not hard-code answers.
- Do not manually label records to force expected results.
- Application must work when a new CSV with the same schema is supplied.
- Document assumptions.
- Document preprocessing decisions.
- Document model choices.
- Document limitations.
- Provide reproducible execution.

## Task 1 — ATE Data Quality & Yield Analysis

Must:

- Profile dataset size.
- Report schema.
- Report missing values.
- Detect duplicates.
- Report basic statistics.
- Clean missing values using a justified strategy.
- Detect and handle duplicates.
- Detect abnormal/outlier measurements.
- Explain outlier methodology.
- Calculate overall PASS yield.
- Calculate FAIL rate.
- Calculate yield by Test_ID.
- Calculate yield by Test_Name.
- Calculate yield by Lot_ID.
- Calculate yield by Wafer_ID.
- Identify top failing tests.
- Identify common failure modes.
- Produce at least four meaningful visualizations.
- Produce a concise engineering summary.

## Task 2 — ML-Based ATE Failure Prediction

Must:

- Define prediction target.
- Justify target.
- Select useful features.
- Explain feature relevance.
- Preprocess without data leakage.
- Train at least two classification models.
- Compare models using appropriate metrics.
- Consider class imbalance.
- Explain influential features.
- Save final model.
- Expose reusable prediction function/API.
- Demonstrate predictions on unseen records.

## Task 3 — ATE Anomaly Detection & Failure Intelligence

Must:

- Implement anomaly detection or statistical abnormality detection.
- Generate anomaly score or equivalent ranking.
- Identify suspicious devices/tests.
- Compare anomalies with known PASS/FAIL information.
- Compare anomalies with failure-mode information.
- Explain why a record was flagged.
- Explain algorithm and important parameters.
- Separate observed evidence from inferred possible causes.

## Task 4 — AI Engineering Application

Required application flow:

1. Upload CSV.
2. Validate/load/process data.
3. Dashboard.
4. Failure Investigation.
5. AI Analysis.
6. Prediction.

Application requirements:

- Upload dataset.
- Validate and process it.
- Show yield/failure information.
- Investigate a device/test.
- Inspect measurements and limits.
- Generate evidence-based AI analysis.
- Run trained ML prediction on new input.
- Ground AI output in supplied data.
- Show evidence used for conclusions where practical.
- State insufficient evidence instead of inventing a root cause.
- LLM/RAG is optional; evidence-based AI/ML explanation is required.

## Submission

Must provide:

- Complete runnable source code.
- README.
- Setup instructions.
- Architecture.
- Assumptions.
- Commands.
- Usage.
- EDA/data-quality findings.
- Engineering conclusions.
- ML training/evaluation.
- Saved model or reproducible training.
- Working UI/API.
- Tests.
- 5–10 minute demo.

---

# 3. Evaluation Strategy

The implementation should prioritize:

1. AI/reasoning/explainability.
2. ML/evaluation.
3. ATE data understanding and analysis.
4. Python/data engineering.
5. Generalization/problem solving.
6. Application/API.
7. Testing/documentation/code quality.
8. UI/usability.

Do not spend disproportionate time on visual polish at the expense of data quality, ML validity, leakage prevention, explainability, or engineering correctness.

---

# 4. Technology Stack

## Frontend

- Next.js
- React
- TypeScript
- Tailwind CSS
- shadcn/ui
- Recharts or Apache ECharts
- Lucide React
- Framer Motion

## Backend

- Python 3.12+
- FastAPI
- Pydantic v2
- Uvicorn

## Data

- Pandas
- Polars
- NumPy
- DuckDB
- PyArrow

## ML

- scikit-learn
- CatBoost
- XGBoost
- SHAP
- joblib

## Testing / Quality

- pytest
- Ruff
- Black
- MyPy

## Infrastructure

- Docker
- Docker Compose

## Optional, only after the core system is stable

- MLflow
- PostgreSQL
- LLM provider

Do not introduce optional infrastructure merely for appearance. Every component must have a clear engineering purpose.

---

# 5. High-Level Architecture

```text
                    ┌─────────────────────────┐
                    │       CSV UPLOAD        │
                    └────────────┬────────────┘
                                 ↓
                    ┌─────────────────────────┐
                    │   SCHEMA VALIDATION     │
                    └────────────┬────────────┘
                                 ↓
                    ┌─────────────────────────┐
                    │ DATA QUALITY PIPELINE   │
                    │ Missing / Duplicates    │
                    │ Outliers / Validation   │
                    └────────────┬────────────┘
                                 ↓
              ┌──────────────────┼──────────────────┐
              ↓                  ↓                  ↓
       ┌────────────┐     ┌────────────┐     ┌────────────┐
       │   YIELD    │     │ ML ENGINE  │     │  ANOMALY   │
       │  ANALYSIS  │     │            │     │  ENGINE    │
       └─────┬──────┘     └─────┬──────┘     └─────┬──────┘
             │                  │                  │
             └──────────────────┼──────────────────┘
                                ↓
                    ┌─────────────────────────┐
                    │  ENGINEERING DASHBOARD │
                    └────────────┬────────────┘
                                 ↓
                ┌────────────────┼─────────────────┐
                ↓                ↓                 ↓
        Failure Investigation  Prediction     AI Analysis
                │                │                 │
                └────────────────┼─────────────────┘
                                 ↓
                    Evidence-Based Explanation
```

---

# 6. Repository Structure

```text
verilumen-ate-intelligence/
│
├── frontend/
│   ├── app/
│   ├── components/
│   ├── lib/
│   ├── hooks/
│   ├── types/
│   ├── public/
│   ├── package.json
│   └── ...
│
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   │
│   │   ├── api/
│   │   │   ├── upload.py
│   │   │   ├── dashboard.py
│   │   │   ├── prediction.py
│   │   │   ├── anomaly.py
│   │   │   ├── investigation.py
│   │   │   └── analysis.py
│   │   │
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   └── logging.py
│   │   │
│   │   ├── data/
│   │   │   ├── schema.py
│   │   │   ├── ingestion.py
│   │   │   ├── validation.py
│   │   │   └── preprocessing.py
│   │   │
│   │   ├── analytics/
│   │   │   ├── quality.py
│   │   │   ├── yield_analysis.py
│   │   │   ├── failures.py
│   │   │   └── summaries.py
│   │   │
│   │   ├── ml/
│   │   │   ├── features.py
│   │   │   ├── train.py
│   │   │   ├── evaluate.py
│   │   │   ├── predict.py
│   │   │   ├── model_registry.py
│   │   │   └── leakage.py
│   │   │
│   │   ├── anomaly/
│   │   │   ├── statistical.py
│   │   │   ├── isolation_forest.py
│   │   │   └── scoring.py
│   │   │
│   │   ├── explainability/
│   │   │   ├── shap_explainer.py
│   │   │   ├── evidence_engine.py
│   │   │   └── narrative.py
│   │   │
│   │   └── services/
│   │       ├── pipeline.py
│   │       └── session.py
│   │
│   ├── scripts/
│   │   ├── generate_demo_data.py
│   │   ├── train_models.py
│   │   └── run_assessment_audit.py
│   │
│   ├── requirements.txt
│   └── pyproject.toml
│
├── data/
│   ├── demo_ate_data.csv
│   └── README.md
│
├── models/
│
├── notebooks/
│   └── development_analysis.ipynb
│
├── tests/
│   ├── test_schema.py
│   ├── test_ingestion.py
│   ├── test_preprocessing.py
│   ├── test_quality.py
│   ├── test_yield.py
│   ├── test_features.py
│   ├── test_leakage.py
│   ├── test_models.py
│   ├── test_evaluation.py
│   ├── test_anomaly.py
│   ├── test_explanation.py
│   └── test_api.py
│
├── docs/
│   ├── architecture.md
│   ├── methodology.md
│   ├── requirements_traceability.md
│   ├── ml_evaluation.md
│   └── demo_script.md
│
├── prompts/
│   └── development-prompts/
│
├── reports/
│
├── docker/
│
├── docker-compose.yml
├── README.md
├── .gitignore
└── LICENSE
```

---

# 7. Schema Contract

The development system must support the assessment-described ATE schema.

Core columns:

```text
Device_ID
Test_ID
Test_Name
Lot_ID
Wafer_ID
VDD_V
Temperature_C
Measured_Value
Lower_Limit
Upper_Limit
Result
Failure_Mode
Retest_Count
```

The implementation must not assume:

- a specific number of rows
- specific Device_ID values
- specific Lot_ID values
- specific Wafer_ID values
- specific tests
- specific failure modes
- specific PASS/FAIL ratio
- specific distributions

Additional columns should be tolerated unless they conflict with required semantics.

The schema validator should return:

- missing required columns
- unexpected columns
- type problems
- invalid categorical values
- nullability issues
- numerical validation problems

Never silently modify a dataset to force it to fit the schema.

---

# 8. Synthetic Development Dataset

Create a high-fidelity synthetic dataset because the official assessment CSV will be supplied later.

The synthetic dataset must reproduce the kinds of properties described in the assessment:

- multiple devices
- multiple lots
- multiple wafers
- multiple test types
- electrical conditions
- thermal conditions
- measurements
- specification limits
- PASS/FAIL
- failure modes
- retests
- missing values
- duplicate records
- abnormal measurements

Recommended development scale:

- 10,000+ records
- multiple lots
- multiple wafers per lot
- thousands of devices
- at least 8–15 test types
- realistic PASS majority
- meaningful minority FAIL class

Inject data-quality problems deliberately.

## Missing values

Inject missing values into selected numerical and categorical fields at a controlled rate.

## Duplicates

Create exact duplicate rows and document how they were generated.

## Outliers

Create abnormal measurement values that are statistically unusual.

## Borderline values

Create measurements close to Lower_Limit or Upper_Limit.

## Failures

Create realistic failure clusters rather than completely random labels.

## Failure modes

Use multiple categories, for example:

```text
TIMING_VIOLATION
VOLTAGE_MARGIN
THERMAL_STRESS
SIGNAL_INTEGRITY
SCAN_CHAIN
POWER_ANOMALY
UNKNOWN
```

These are synthetic development categories and must not be assumed to be the official dataset's exact categories.

---

# 9. Data Ingestion

Implement:

```text
load_csv(file)
validate_schema(df)
normalize_types(df)
profile_dataset(df)
```

Input:

- uploaded CSV

Output:

```text
DatasetContext
├── raw_dataframe
├── schema_report
├── quality_report
├── cleaned_dataframe
└── processing_metadata
```

Do not perform destructive transformations on the raw dataframe.

Maintain a clear distinction:

```text
RAW DATA
CLEAN DATA
DERIVED DATA
```

---

# 10. Data Quality Engine

## Required profiling

Calculate:

- number of rows
- number of columns
- memory footprint
- data types
- missing count
- missing percentage
- unique values
- numerical statistics
- categorical distributions
- duplicate count

## Missing-value strategy

Use type-aware handling.

Numerical:

- median or robust statistic where justified.

Categorical:

- explicit missing category or appropriate mode strategy.

Never impute target labels blindly.

Always record:

```text
column
original_missing_count
strategy
filled_count
```

## Duplicate strategy

Detect exact duplicates.

Do not silently remove them.

Return:

```text
duplicate_count
duplicate_percentage
rows_removed
reason
```

## Outlier strategy

Use multiple signals:

- IQR
- robust MAD
- specification limits
- optionally z-score when distribution assumptions are reasonable

Do not automatically delete every outlier.

Instead classify:

```text
STATISTICAL_OUTLIER
SPECIFICATION_VIOLATION
BORDERLINE_SPECIFICATION
NORMAL
```

This preserves engineering information.

---

# 11. Yield Analytics

Calculate:

```text
total_records
pass_count
fail_count
pass_yield
fail_rate
```

Formula:

```text
PASS Yield = PASS records / total valid records × 100
FAIL Rate = FAIL records / total valid records × 100
```

Calculate grouped yield for:

- Test_ID
- Test_Name
- Lot_ID
- Wafer_ID

For every grouping provide:

```text
total
pass
fail
yield
fail_rate
```

Top failing tests:

Sort by meaningful failure count/rate and provide both count and rate to avoid misleading rankings.

Failure-mode analysis:

```text
Failure_Mode
count
percentage
```

---

# 12. Visualization Layer

At least four visualizations are required.

Implement:

1. PASS vs FAIL distribution.
2. Yield by Test.
3. Yield by Lot.
4. Yield by Wafer.
5. Failure-mode distribution.
6. Measurement vs lower/upper specification limits.
7. Temperature vs measurement.
8. Retest distribution.
9. Anomaly score distribution.

All visualizations must use current uploaded data.

No hard-coded values.

Include:

- empty state
- loading state
- error state
- tooltips
- filters
- accessible labels

---

# 13. Engineering Summary

Generate an automated summary.

Example structure:

```text
DATASET SUMMARY

Records:
Devices:
Lots:
Wafers:
Tests:

PASS Yield:
FAIL Rate:

DATA QUALITY

Missing values:
Duplicates:
Outliers:

FAILURE INTELLIGENCE

Top failing tests:
Most common failure modes:

ANOMALY INTELLIGENCE

Anomalies:
Highest anomaly score:

ENGINEERING OBSERVATIONS

- ...
- ...
- ...

LIMITATIONS

- ...
```

Never invent conclusions.

If evidence is insufficient, explicitly say so.

---

# 14. Prediction Target

Primary target:

```text
Result
```

Binary representation:

```text
PASS = 0
FAIL = 1
```

But first verify actual values in the real CSV.

Never assume capitalization or exact string formatting.

Do not use:

```text
Result
Failure_Mode
```

as predictive features.

---

# 15. Prediction Timing

Create two clearly documented scenarios.

## Scenario A — Pre-test prediction

Only features available before test completion.

Potential features:

- Test_ID
- Test_Name
- Lot_ID
- Wafer_ID
- VDD_V
- Temperature_C
- legitimate historical features

## Scenario B — Measurement-aware prediction/diagnosis

Can include measurement-related fields when they are explicitly described as available at that stage.

The system must document feature availability and avoid claiming a pre-test prediction if post-test information was used.

---

# 16. Feature Engineering

Potential derived features:

```text
spec_range
lower_margin
upper_margin
specification_position
out_of_spec
temperature_deviation
vdd_deviation
```

Formula examples:

```text
spec_range = Upper_Limit - Lower_Limit

lower_margin = Measured_Value - Lower_Limit

upper_margin = Upper_Limit - Measured_Value

specification_position =
    (Measured_Value - Lower_Limit) /
    (Upper_Limit - Lower_Limit)

out_of_spec =
    Measured_Value < Lower_Limit OR
    Measured_Value > Upper_Limit
```

Only calculate features when their information availability is valid for the selected prediction scenario.

---

# 17. ML Models

Train at least two models.

Implement three:

## Baseline

Logistic Regression.

## Primary tabular model

CatBoost.

## Challenger

XGBoost.

Do not predeclare a winner.

Train all valid models and compare their results.

---

# 18. Validation Strategy

Avoid naïve random splitting when records are correlated.

Investigate grouping by:

- Device_ID
- Wafer_ID
- Lot_ID

Use a grouped stratified approach when supported by the actual data.

Potential method:

```text
StratifiedGroupKFold
```

Document the selected grouping strategy and why it is appropriate.

Ensure preprocessing is fitted only on training folds.

---

# 19. Class Imbalance

Calculate class distribution.

If imbalance exists, consider:

- class weights
- threshold tuning
- stratified/grouped evaluation
- precision-recall analysis
- PR-AUC

Do not manipulate labels or fabricate failures.

---

# 20. Evaluation

For every model calculate:

```text
Accuracy
Precision
Recall
F1
ROC-AUC
PR-AUC
Confusion Matrix
```

Also provide:

```text
classification_report
class_distribution
cross_validation_statistics
```

The dashboard should compare models in a table.

Do not hard-code a selected model.

The final model can be selected according to the assessment objective and actual validation results, with the selection rationale documented.

---

# 21. Model Persistence

Store:

```text
models/
├── selected_model/
├── preprocessing_pipeline/
├── feature_metadata.json
├── evaluation_metrics.json
└── model_metadata.json
```

Metadata should include:

```text
model_name
version
training_timestamp
features
target
validation_strategy
metrics
class_distribution
random_seed
```

Use joblib or native model serialization where appropriate.

---

# 22. Prediction API

Implement:

```text
POST /api/predict
```

Response:

```json
{
  "prediction": "FAIL",
  "probability": 0.87,
  "model": "CatBoost",
  "explanation": {...}
}
```

The actual schema must be validated using Pydantic.

Do not return fabricated probability values.

---

# 23. Unseen Record Demonstration

Create a UI form that allows a new record to be submitted.

Show:

- prediction
- probability
- model
- top contributing features
- explanation
- warning if required information is missing

---

# 24. Anomaly Detection

Implement two layers.

## Layer 1 — Statistical

Use:

- IQR
- MAD
- specification violation
- specification proximity
- distribution deviation

## Layer 2 — Isolation Forest

Use numerical features appropriate to the actual data.

Important parameters:

```text
contamination
n_estimators
max_samples
random_state
```

Document why each parameter was selected.

Do not blindly use a fixed contamination value without checking the dataset.

---

# 25. Anomaly Score

Normalize or clearly document the meaning of the anomaly score.

Return:

```text
anomaly_flag
anomaly_score
anomaly_rank
```

Rank suspicious records.

Also provide aggregated suspicious:

- devices
- tests
- lots
- wafers

---

# 26. Compare Anomalies With Known Results

For each anomaly calculate:

```text
Result
Failure_Mode
Retest_Count
Out-of-spec status
```

This allows the dashboard to show cases such as:

```text
Anomaly + FAIL
Anomaly + PASS
Anomaly + known failure mode
Anomaly + no recorded failure mode
```

Do not equate anomaly with failure.

---

# 27. Anomaly Explanation

Every anomaly must have evidence.

Example:

```text
ANOMALY DETECTED

Device:
ATE...

Test:
...

Anomaly Score:
...

Evidence:
- Measurement is statistically unusual.
- Measurement is close to/over specification boundary.
- Temperature deviates from typical test conditions.
- Retest count is elevated.

Observed Result:
FAIL

Recorded Failure Mode:
...

Possible Interpretation:
The record warrants further engineering investigation.

Limitation:
This interpretation is not a confirmed root cause.
```

---

# 28. SHAP Explainability

Implement:

## Global explanation

Feature importance across the model.

## Local explanation

For an individual prediction:

```text
prediction
probability
feature
contribution
direction
```

Example:

```text
Temperature_C      +0.28
Measured_Value     +0.24
Retest_Count       +0.11
VDD_V              -0.03
```

Do not interpret SHAP values as proof of physical causality.

---

# 29. Evidence Engine

The evidence engine receives:

```text
raw_record
quality_context
statistics
prediction
probability
SHAP_values
anomaly_score
failure_mode
specification_limits
```

It returns:

```text
observed_evidence
model_evidence
anomaly_evidence
possible_interpretations
confidence
limitations
```

The engine must never invent facts.

If evidence is insufficient:

```text
Insufficient evidence for a reliable engineering interpretation.
```

---

# 30. Optional LLM Layer

An LLM is optional.

If implemented:

```text
Raw Dataset
    ↓
Deterministic Analytics
    ↓
ML
    ↓
SHAP
    ↓
Anomaly Detection
    ↓
Evidence Object
    ↓
LLM
    ↓
Natural Language Explanation
```

The LLM receives only structured evidence.

It must:

- summarize
- explain
- distinguish evidence from interpretation
- state uncertainty
- avoid unsupported causal claims

The deterministic pipeline remains the source of truth.

---

# 31. FastAPI Endpoints

Implement:

```text
POST /api/upload
POST /api/process

GET /api/overview
GET /api/data-quality
GET /api/yield
GET /api/failures
GET /api/anomalies

GET /api/device/{device_id}
GET /api/test/{test_id}

POST /api/predict
POST /api/explain

GET /api/model-performance
GET /api/health
```

Keep route handlers thin.

Business logic belongs in services.

---

# 32. Frontend Pages

Implement:

```text
/
 /data-quality
 /yield
 /failures
 /anomalies
 /investigation
 /prediction
 /ai-analysis
 /model-performance
```

---

# 33. Frontend States

Every major page must handle:

```text
Initial
Loading
Success
Empty
Validation error
Backend error
Insufficient data
```

Never show stale results from an earlier uploaded dataset.

---

# 34. Overview Dashboard

Before upload:

```text
ATE INTELLIGENCE

Analyze • Predict • Investigate • Explain

[ Upload ATE Dataset ]

Supported format: CSV
```

After processing:

```text
Total Records
PASS Yield
FAIL Rate
Anomalies
Devices
Lots
Wafers
```

Then charts and key findings.

No fabricated numbers.

---

# 35. Data Quality Page

Display:

- dataset dimensions
- column schema
- missing values
- duplicates
- numerical statistics
- outliers
- cleaning actions
- data-quality warnings

Provide expandable details for each issue.

---

# 36. Yield Page

Display:

- overall yield
- fail rate
- yield by test
- yield by test name
- yield by lot
- yield by wafer
- top failing tests
- failure modes

Provide filters.

---

# 37. Failure Investigation Page

Inputs:

```text
Device selector
Test selector
```

Display:

```text
Device information
Lot
Wafer
Test
Test name

VDD
Temperature

Measured value
Lower limit
Upper limit
Margins
Result
Failure mode
Retest count
```

Also show historical/contextual information if valid.

---

# 38. Anomaly Page

Display:

- total anomalies
- anomaly distribution
- ranked suspicious records
- filters by device/test/lot/wafer/result
- anomaly details
- evidence

---

# 39. Prediction Page

Provide:

## Existing record mode

Select device/test.

## New record mode

Enter model-supported features.

Show:

```text
Prediction
Probability
Model
SHAP explanation
Evidence
```

---

# 40. AI Analysis Page

Show:

```text
Observed Evidence
Model Findings
Anomaly Findings
Recorded Failure Mode
Possible Interpretation
Confidence
Limitations
```

Use clear labels so users can distinguish facts from inference.

---

# 41. Model Performance Page

Display:

```text
Model comparison

Logistic Regression
CatBoost
XGBoost
```

Metrics:

```text
Accuracy
Precision
Recall
F1
ROC-AUC
PR-AUC
```

Also:

- confusion matrix
- class distribution
- feature importance
- SHAP global summary

---

# 42. Automated Tests

Create tests for:

```text
Schema validation
CSV ingestion
Type normalization
Missing-value handling
Duplicate detection
Outlier detection
Yield calculation
Grouped yield calculation
Feature engineering
Leakage detection
Model training
Model evaluation
Prediction
Anomaly scoring
Anomaly explanation
Evidence generation
API endpoints
```

Tests must validate behavior rather than hard-coding synthetic row-level results.

---

# 43. Assessment Requirement Traceability

Create:

```text
docs/requirements_traceability.md
```

Use this table:

| Assessment requirement | Implementation | Test | Status |
|---|---|---|---|
| Dataset profiling | quality.py | test_quality.py | |
| Missing values | preprocessing.py | test_preprocessing.py | |
| Duplicates | quality.py | test_quality.py | |
| Outliers | statistical.py | test_anomaly.py | |
| Overall yield | yield_analysis.py | test_yield.py | |
| Test yield | yield_analysis.py | test_yield.py | |
| Lot yield | yield_analysis.py | test_yield.py | |
| Wafer yield | yield_analysis.py | test_yield.py | |
| Top failing tests | failures.py | test_yield.py | |
| Failure modes | failures.py | test_yield.py | |
| Four+ visualizations | frontend | integration/manual | |
| Model 1 | train.py | test_models.py | |
| Model 2 | train.py | test_models.py | |
| Class imbalance | train.py | test_models.py | |
| Evaluation metrics | evaluate.py | test_evaluation.py | |
| Feature influence | shap_explainer.py | test_explanation.py | |
| Saved model | model_registry.py | test_models.py | |
| Unseen prediction | predict.py | test_api.py | |
| Anomaly detection | anomaly/ | test_anomaly.py | |
| Anomaly score | scoring.py | test_anomaly.py | |
| Anomaly explanation | evidence_engine.py | test_explanation.py | |
| CSV upload | upload.py | test_api.py | |
| Dashboard | frontend | integration/manual | |
| Investigation | investigation.py | test_api.py | |
| AI analysis | evidence_engine.py | test_explanation.py | |
| Prediction | prediction.py | test_api.py | |
| README | README.md | manual | |
| Tests | tests/ | pytest | |
| Demo | docs/demo_script.md | manual | |

Do not mark a requirement complete without implementation evidence.

---

# 44. Final Assessment Audit

Create:

```text
scripts/run_assessment_audit.py
```

It should check:

```text
schema
data quality
yield
failure analysis
visualization readiness
feature pipeline
model availability
metrics
anomaly pipeline
explanation pipeline
saved artifacts
API health
```

The audit should produce:

```text
PASS
WARN
FAIL
```

with explanations.

This is an internal readiness tool, not a claim about hidden evaluator tests.

---

# 45. Real CSV Integration Procedure

When the official CSV is received:

## Step 1

Run schema compatibility.

## Step 2

Do not alter the official data manually.

## Step 3

Run data-quality profiling.

## Step 4

Review:

- actual columns
- actual data types
- actual categories
- missingness
- duplicates
- class balance
- distributions
- ranges

## Step 5

Run leakage audit.

## Step 6

Train models.

## Step 7

Evaluate models.

## Step 8

Run anomaly detection.

## Step 9

Run complete API.

## Step 10

Run frontend.

## Step 11

Run pytest.

## Step 12

Run final assessment audit.

---

# 46. Real CSV Audit Prompt

When the official dataset arrives, use this development prompt:

```text
The official Verilumen ATE assessment CSV has now been provided.

Do not modify the dataset to force compatibility.

Audit the existing application against the actual dataset.

Check:

1. schema compatibility
2. required columns
3. unexpected columns
4. data types
5. categorical values
6. missing values
7. duplicates
8. numerical ranges
9. class balance
10. feature availability timing
11. target leakage
12. device/lot/wafer leakage
13. anomaly pipeline compatibility
14. ML pipeline compatibility
15. API compatibility
16. frontend compatibility

For every mismatch provide:

- issue
- evidence
- impact
- recommended fix
- affected files
- required tests

Do not silently change behavior.

Only implement fixes after identifying and documenting them.
```

---

# 47. Development Prompt Sequence

Keep development prompts incremental.

```text
00_project_specification
01_synthetic_dataset
02_schema_validation
03_data_quality
04_yield_analysis
05_visualization
06_feature_engineering
07_ml_pipeline
08_model_evaluation
09_leakage_audit
10_anomaly_detection
11_shap_explainability
12_evidence_engine
13_optional_llm
14_fastapi
15_nextjs
16_frontend_backend_integration
17_testing
18_real_csv_audit
19_final_compliance_audit
```

AI coding assistants may be used, but all generated code must be reviewed and understood before submission.

---

# 48. Documentation Requirements

README must include:

1. Project overview.
2. Problem statement.
3. ATE domain assumptions.
4. Architecture.
5. Technology stack.
6. Dataset schema.
7. Synthetic dataset purpose.
8. Data cleaning.
9. Outlier methodology.
10. Yield methodology.
11. Feature engineering.
12. Prediction target.
13. Leakage prevention.
14. Model choices.
15. Validation strategy.
16. Evaluation metrics.
17. Class imbalance.
18. Explainability.
19. Anomaly detection.
20. Evidence engine.
21. Optional LLM.
22. API.
23. Frontend.
24. Testing.
25. Installation.
26. Running locally.
27. Docker.
28. Limitations.
29. Future improvements.

---

# 49. Final Demo Flow

The final 5–10 minute demo should follow:

## 1. Problem

Explain the ATE test intelligence problem.

## 2. Architecture

Show:

```text
CSV → Data → ML → Anomaly → Evidence → API → UI
```

## 3. Upload

Upload the assessment CSV.

## 4. Data quality

Show:

- missing values
- duplicates
- outliers

## 5. Yield

Show:

- overall yield
- test yield
- lot/wafer yield
- failure modes

## 6. ML

Show:

- models
- evaluation
- class imbalance
- selected model rationale

## 7. Explainability

Show SHAP/global and local explanation.

## 8. Anomaly

Show suspicious record and evidence.

## 9. Investigation

Select a device/test.

## 10. AI Analysis

Show evidence-grounded explanation.

## 11. Prediction

Submit an unseen record.

## 12. Engineering conclusion

Explain what the system found and its limitations.

---

# 50. Final Pre-Submission Gate

Run:

```bash
pytest
```

Then:

```bash
python scripts/run_assessment_audit.py
```

Then:

```bash
docker compose up --build
```

Then manually verify:

```text
[ ] CSV uploads
[ ] Invalid CSV is rejected cleanly
[ ] Required columns are validated
[ ] Missing values are handled
[ ] Duplicates are handled
[ ] Outliers are detected
[ ] Overall yield works
[ ] Test yield works
[ ] Lot yield works
[ ] Wafer yield works
[ ] Failure modes work
[ ] At least four charts work
[ ] Engineering summary works
[ ] Model 1 trains
[ ] Model 2 trains
[ ] Model comparison works
[ ] Class imbalance is handled
[ ] Leakage checks pass
[ ] SHAP works
[ ] Model saves
[ ] Prediction API works
[ ] Unseen prediction works
[ ] Anomaly detection works
[ ] Anomaly ranking works
[ ] Evidence explanation works
[ ] Device investigation works
[ ] AI analysis works
[ ] Frontend works
[ ] Backend works
[ ] Tests pass
[ ] README complete
[ ] Architecture documented
[ ] Limitations documented
[ ] Demo script ready
```

---

# 51. Definition of Done

The project is NOT considered complete merely because the UI works.

It is complete only when:

```text
                    DEFINITION OF DONE

                         ┌─────────┐
                         │  CODE   │
                         └────┬────┘
                              │
            ┌─────────────────┼─────────────────┐
            ↓                 ↓                 ↓
       DATA QUALITY          ML             ANOMALY
            │                 │                 │
            └─────────────────┼─────────────────┘
                              ↓
                       EXPLAINABILITY
                              ↓
                           API
                              ↓
                         FRONTEND
                              ↓
                           TESTS
                              ↓
                       DOCUMENTATION
                              ↓
                    REQUIREMENT AUDIT
                              ↓
                       REAL CSV TEST
                              ↓
                        FINAL DEMO
```

The final implementation should be **generalized, reproducible, explainable, tested, and assessment-complete**, rather than optimized only for the synthetic development dataset.

---

# 52. Critical Rule

The synthetic dataset is a **development harness only**.

Never:

- hard-code its values into application logic
- assume its row count
- assume its model performance
- hard-code its top failing test
- hard-code its failure modes
- hard-code its anomaly records
- manually label data to force model performance
- modify the official CSV to make tests pass

The application must derive results dynamically from the uploaded dataset.

---

# 53. First Implementation Milestone

Do not build the entire application in one step.

Start with:

```text
PHASE 1

Repository
    ↓
Python environment
    ↓
Synthetic dataset generator
    ↓
demo_ate_data.csv
    ↓
Schema contract
    ↓
Schema validation tests
```

Then proceed sequentially through the phases in this document.

The synthetic dataset should be sufficiently realistic to exercise every required part of the application, including missing values, duplicates, abnormal measurements, multiple tests/lots/wafers, PASS/FAIL imbalance, failure modes, and retest behavior.

The real Verilumen CSV will later replace the synthetic dataset without requiring architectural restructuring.


# APPENDIX A — Production AI Coding Prompt Pack

The repository now includes a complete, copy-paste-ready prompt sequence under `prompts/development-prompts/`. The prompts are deliberately incremental so that an AI coding assistant can implement the system without receiving permission to rewrite the whole project at every step.

## Prompt execution contract

Before executing any prompt, read `00_MASTER_RULES.md`. Execute one prompt at a time. After each prompt:

1. Inspect the diff.
2. Run the relevant tests.
3. Run lint/type checks when applicable.
4. Check that previous functionality still works.
5. Commit the change with a meaningful message.
6. Record any architecture decision in `docs/`.

Do not ask an AI coding assistant to generate the entire repository in one uncontrolled pass. Incremental construction makes the code easier to review, test, explain in the interview, and audit against the assessment.

## Prompt map

| Prompt | Purpose | Primary output |
|---|---|---|
| 00 | Master rules | Global engineering constraints |
| 01 | Foundation | Backend/frontend repository skeleton |
| 02 | Synthetic data | High-fidelity development CSV generator |
| 03 | Schema | Ingestion and validation |
| 04 | Data quality | Missing/duplicate/outlier pipeline |
| 05 | Analytics | Yield/failure/engineering analytics |
| 06 | Visualization | Four+ meaningful dynamic views |
| 07 | Features | Leakage-safe feature pipeline |
| 08 | ML | Two+ production classifiers |
| 09 | Evaluation | Full metric/threshold evaluation |
| 10 | Leakage audit | Automated leakage checks |
| 11 | Anomaly | Statistical + unsupervised anomaly layer |
| 12 | Explainability | SHAP/local/global explanation |
| 13 | Evidence engine | Structured engineering reasoning |
| 14 | Optional LLM | Evidence-grounded narrative layer |
| 15 | FastAPI | Production API |
| 16 | Next.js | Professional engineering UI |
| 17 | Integration | End-to-end frontend/backend workflow |
| 18 | Testing | Unit/integration/E2E and CI quality gates |
| 19 | Official CSV | Compatibility and dataset-specific audit |
| 20 | Final audit | Assessment traceability and remediation |

## Why the prompt sequence is designed this way

The assessment explicitly allows AI coding assistants but requires the candidate to understand and explain submitted code. The sequence therefore separates data engineering, analytics, ML, anomaly detection, explainability, API, UI, testing, and compliance rather than hiding everything inside one generated application. fileciteturn0file0L20-L29

The sequence also mirrors the assessment's task structure: data quality and engineering analytics, classification and evaluation, anomaly detection and explanation, then the usable application workflow. fileciteturn0file0L47-L105

# APPENDIX B — Production Readiness Requirements

The implementation is considered complete only when all of the following are true:

- The official CSV can be uploaded without code changes when it conforms to the documented logical schema.
- The raw dataset is preserved.
- Cleaning decisions are reproducible and reported.
- Duplicate and abnormal-record handling is explicit.
- Yield/failure analytics are computed from the current dataset.
- At least four meaningful visualizations are dynamic.
- The prediction target and prediction timing are documented.
- Preprocessing is fit only on training data.
- At least two classifiers are trained and evaluated.
- Precision, recall, F1, ROC-AUC and PR-AUC are reported when mathematically defined.
- Class imbalance is addressed and documented.
- Leakage audit is executed.
- The final model artifact includes preprocessing.
- Unseen-record prediction works.
- Anomaly scoring/ranking works independently of classification.
- Anomaly explanations expose actual evidence.
- SHAP or an appropriate fallback is available.
- Evidence and inference are separated.
- Optional LLM functionality cannot override deterministic evidence.
- Upload/API security basics are implemented.
- Empty/error/insufficient-data UI states are implemented.
- Automated tests cover the core pipeline.
- README setup instructions work from a clean environment.
- A final requirements traceability matrix is generated.
- A 5–10 minute demo can follow the assessment workflow.

The assessment's submission requirements explicitly call for runnable source, README/documentation, EDA and engineering conclusions, ML evaluation and saved/reproducible model, working UI/API, tests, and a demo. fileciteturn0file0L108-L131

# APPENDIX C — Real CSV Integration Gate

When the official CSV arrives, do not assume it exactly matches the synthetic dataset. Run Prompt 19 first. The compatibility audit must determine the actual schema, missingness, duplicates, class balance, limits, measurement distributions, identifiers, and failure modes. Then adapt only the assumptions proven incompatible with the official file.

The assessment states that the supplied CSV is the primary dataset and that the application should work with a new CSV having the same schema. fileciteturn0file0L20-L44

# APPENDIX D — What the AI Must Never Do

- Never fabricate a yield or model score.
- Never hard-code IDs from the development CSV.
- Never manually assign labels to make a classifier look good.
- Never use a post-test field to claim a pre-test prediction.
- Never claim a model explanation proves physical causation.
- Never hide missing or insufficient evidence.
- Never make the dashboard appear populated when no dataset exists.
- Never send the entire uploaded dataset to an optional external LLM merely to generate a summary.
- Never remove anomalies without documenting the policy.
- Never silently change the schema contract because one file happens to differ.

# APPENDIX E — Recommended Git Milestones

```text
01-foundation
02-demo-data
03-ingestion-schema
04-data-quality
05-analytics
06-visualization
07-features
08-ml
09-evaluation
10-leakage-audit
11-anomaly
12-explainability
13-evidence
14-optional-llm
15-api
16-frontend
17-integration
18-testing-ci
19-official-csv
20-final-audit
```

This gives the evaluator a clear implementation history and makes it easier for the candidate to explain how the system evolved.
