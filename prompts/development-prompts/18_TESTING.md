# Prompt 18 — Comprehensive Testing and Quality Gates

Implement a serious test strategy suitable for a technical assessment submission.

## Backend tests
Cover:
- schema validation
- ingestion
- missing values
- duplicates
- outliers
- yield calculations
- failure analysis
- feature engineering
- leakage audit
- model training/evaluation
- model persistence/loading
- anomaly scoring
- SHAP/evidence generation
- API endpoints

## Frontend tests
Cover critical components, empty/error states, upload flow, filters and evidence rendering.

## Test categories
Mark unit, integration and end-to-end tests clearly. Add fixtures for tiny datasets, one-class targets, missing columns, all-null fields, duplicate rows, unseen categories and insufficient anomaly samples.

## Quality commands
Provide one documented command for backend checks and one for frontend checks. Add coverage reporting where practical.

## CI
Create a lightweight CI workflow that runs lint/type checks/tests/build without requiring proprietary credentials.
