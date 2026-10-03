# Prompt 16 — Production-Quality Next.js ATE UI

Build the frontend for an ATE/test engineer, prioritizing usability and evidence visibility over decorative effects.

## Screens
1. Upload/landing
2. Overview dashboard
3. Data Quality
4. Yield & Failures
5. Failure Investigation
6. AI Analysis
7. Prediction
8. About/Methodology

## UX
Provide clear loading, empty, error, insufficient-data, and success states. Never show fake metrics.

## Investigation
Allow selecting/filtering device, lot, wafer and test. Show measured value alongside lower/upper limits, result, failure mode, retest count, anomaly score, model prediction and evidence.

## AI Analysis
Visually separate Observed Evidence, Model Evidence, Possible Interpretations, and Limitations.

## Prediction
Allow upload/paste of unseen records using the validated schema and return prediction plus probability and explanation.

## Visual design
Use a professional semiconductor engineering dashboard aesthetic. Use accessible contrast, responsive layout, keyboard-friendly controls, clear units, and restrained animation.

## Engineering
Use typed API clients, reusable components, query caching, error boundaries, and environment-based API configuration.
