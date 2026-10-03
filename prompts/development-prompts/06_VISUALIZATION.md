# Prompt 06 — Visualization and Dashboard Analytics

Build the visualization layer required by the assessment with at least four meaningful engineering views.

## Required visualizations
Implement dynamic versions of:
1. Overall PASS/FAIL yield.
2. Yield/failure rate by test.
3. Yield by lot/wafer.
4. Failure-mode distribution.

Add useful optional views such as measurement distributions versus limits, temperature/VDD relationships, retest distribution, and anomaly score distribution.

## Rules
- All charts must be derived from the uploaded dataset.
- Never embed sample numbers in chart components.
- Handle empty/small datasets gracefully.
- Make charts accessible and readable.
- Provide tooltips and clear units.
- Avoid misleading scales and label axes precisely.

## Backend
Expose aggregated endpoints rather than sending raw full datasets unnecessarily.

## Frontend
Use reusable typed chart components. Loading, empty, error, and insufficient-data states are required.
