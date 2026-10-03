# Prompt 08 — Production-Quality Classification Pipeline

Implement Task 2's classification pipeline.

## Models
Train at least two genuinely different classifiers. Use:
- Logistic Regression as an interpretable baseline.
- CatBoost as the primary mixed-tabular model when available.
- XGBoost as an optional challenger if dependency/runtime constraints permit.

Do not assume one model will always win.

## Validation
Use stratified validation where independent rows are appropriate. If repeated observations share device/wafer/lot, implement a leakage-aware group strategy such as StratifiedGroupKFold when feasible and explain the selected grouping level.

## Imbalance
Measure class distribution. Use appropriate class weights, sampling or threshold tuning only when justified. Report the method.

## Training artifact
Persist preprocessing + model together as a versioned artifact. Save metadata: training timestamp, feature list, target, validation strategy, package versions where practical, random seed, and metrics.

## Prediction interface
Create a reusable `predict()` service that accepts unseen records and returns prediction, probability/score, model version, and explanation metadata when available.

## Failure handling
If the target has only one class or there are too few valid samples, return an explicit insufficient-data result instead of crashing.

## Tests
Train on fixtures, save/load artifacts, predict unseen rows, and verify deterministic behavior under a fixed seed.
