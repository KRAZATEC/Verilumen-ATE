# Prompt 19 — Official CSV Compatibility Audit

The official Verilumen CSV has now been provided. Do not immediately rewrite the application.

## First perform an audit
Compare the official CSV against the schema contract:
- columns
- data types
- unique values
- missingness
- duplicate structure
- row count
- target distribution
- limits
- measurement ranges
- identifiers
- failure modes
- retest behavior

Produce a compatibility report.

## Then adapt safely
Only change assumptions that are demonstrably incompatible with the official data. Keep the pipeline generalized. Never hard-code results from this specific CSV.

## ML audit
Re-evaluate prediction timing and leakage. Remove any feature that is unavailable before the prediction point.

## Validation
Run the full pipeline on the official data and generate the assessment report. If a requested metric is undefined because the data lacks the required class/field, report that honestly and explain why.

## Deliverables
Save a reproducible audit report and update documentation with dataset-specific observations while keeping the code generic.
