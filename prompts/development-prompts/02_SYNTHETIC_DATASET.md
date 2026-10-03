# Prompt 02 — High-Fidelity Synthetic ATE Dataset

Act as a semiconductor test-data engineer and Python data-generation specialist. Implement a realistic development dataset generator that mirrors the logical structure described in the assessment without hard-coding any expected analysis answers.

## Goal
Create `backend/scripts/generate_demo_data.py` that generates `data/demo_ate_data.csv` with at least 10,000 rows and a configurable seed.

## Schema
Support core fields including:
- Device_ID
- Lot_ID
- Wafer_ID
- Test_ID
- Test_Name
- VDD_V
- Temperature_C
- Measured_Value
- Lower_Limit
- Upper_Limit
- Result
- Failure_Mode
- Retest_Count

You may add realistic metadata columns, but clearly document every additional field. Keep the generator configurable.

## Realism requirements
Generate multiple lots, wafers, devices and 8–15 test types. Create realistic dependencies among lot/wafer/device/test, electrical/thermal conditions and measurements. Make PASS the majority class but include meaningful failures and multiple failure modes.

Intentionally include:
- missing values
- exact duplicate records
- near-duplicate records where useful
- borderline measurements near specification limits
- clear outliers/abnormal measurements
- retests
- different failure modes
- lot/wafer effects
- temperature/VDD effects

Do not make every failure an obvious deterministic threshold. Include noise and overlapping distributions so the ML/anomaly pipeline has a meaningful problem.

## Reproducibility
Use a deterministic seed and CLI options for row count, seed, output path, and proportions. Validate generated schema and basic quality expectations.

## Tests
Add generator tests checking row count, required columns, value domains, duplicates, missingness, failure modes, and reproducibility.

## Documentation
Explain that this dataset is development-only and must never be used to hard-code expected assessment outputs.
