# Prompt 04 — Data Quality and Preprocessing Engine

Build the data-quality pipeline required for the assessment.

## Implement
1. Missing-value profiling by column and overall.
2. A justified, configurable missing-value strategy based on data type and role.
3. Duplicate detection including exact duplicates and a report of duplicate counts.
4. Explicit duplicate handling policy that never silently deletes records.
5. Abnormal/outlier measurement detection using robust methods such as IQR/MAD and specification-aware checks where limits exist.
6. A configurable policy distinguishing statistical anomaly from invalid data.
7. Before/after quality summaries.

## Critical distinction
Do not equate an outlier with a bad chip. A measurement can be statistically unusual yet valid, or specification-compliant yet suspicious. Preserve evidence and explain the classification.

## Output
Create structured quality reports suitable for both API and UI, including counts, rates, affected columns, actions taken, and rationale.

## Tests
Include no-missing-data, all-missing-column, duplicates-only, extreme-value, constant-column, and tiny-dataset cases.
