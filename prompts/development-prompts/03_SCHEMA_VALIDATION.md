# Prompt 03 — Schema Validation and Ingestion

Implement a robust CSV ingestion and schema-validation layer.

## Requirements
Create typed schema definitions and a validator that:
- accepts CSV uploads
- identifies required/core columns
- tolerates additional columns
- normalizes harmless column-name variations only through explicit documented aliases
- reports missing required columns clearly
- infers numeric/categorical/date-like types safely
- reports parsing failures
- records row/column counts
- creates a dataset/session identifier
- preserves the raw data

Do not assume the synthetic dataset is the official dataset.

## Data contract
Design a schema contract around the assessment's example fields and make it configurable enough to tolerate legitimate same-schema variants.

## API/service interface
Return a structured `DatasetProfile` containing schema status, row count, column count, required fields, optional fields, inferred types, parse warnings, and quality flags.

## Edge cases
Handle empty CSV, malformed CSV, encoding problems, missing required columns, all-null columns, mixed numeric strings, duplicate column names, and very small datasets without crashing.

## Tests
Cover valid data, missing fields, extra fields, malformed values, empty input, and compatibility with the demo CSV.
