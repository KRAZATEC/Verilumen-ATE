# Prompt 07 — Leakage-Safe Feature Engineering

Design and implement a reusable feature-engineering pipeline for pre-test classification.

## First define the prediction question
The primary task should be framed as predicting a relevant outcome before that outcome is known. Document the prediction timing and what information is legitimately available at prediction time.

## Leakage prevention
Explicitly exclude outcome/post-outcome fields such as Result and Failure_Mode from predictors when predicting test outcome. Audit fields for direct and indirect leakage. Keep the audit machine-readable.

## Features
Build numeric and categorical features from legitimate fields. Candidate derived features include specification range, normalized position within limits, distance to lower/upper limits, temperature deviation, VDD deviation, and safe historical aggregates only when they can be computed without future information.

Do not force every candidate feature into the final model. Provide a feature-selection rationale.

## Pipeline
Use sklearn-compatible transformers so preprocessing is fit only on training data. Handle missing numeric/categorical values, unseen categories, scaling where appropriate, and sparse/dense compatibility.

## Tests
Test transformation determinism, no leakage, unseen categories, missing values, and train/test isolation.
