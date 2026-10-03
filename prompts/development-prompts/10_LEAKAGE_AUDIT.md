# Prompt 10 — Automated Leakage Audit

Build a dedicated leakage-audit module that can inspect a proposed prediction feature set.

## Detect
- direct target columns
- post-outcome fields
- duplicate identifiers that trivially identify records
- features generated using full-dataset information before splitting
- target-derived aggregates
- suspiciously perfect/highly predictive fields
- train/test overlap at device/wafer/lot levels where relevant

## Output
Return a machine-readable report with severity, field, reason, detection method, and recommended action.

## Important
Do not automatically delete a feature merely because it is correlated. Explain whether the correlation is legitimate and available at prediction time.

## Tests
Include deliberate leakage fixtures and legitimate correlated-feature fixtures.
