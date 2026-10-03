# Prompt 11 — Anomaly Detection and Ranking

Implement Task 3 as a separate anomaly layer rather than mixing it with classifier predictions.

## Methods
Combine:
1. robust statistical evidence (IQR/MAD and specification-aware abnormality)
2. Isolation Forest or another justified unsupervised detector

Normalize component scores into a documented anomaly score and rank records.

## Output
For each flagged record provide:
- anomaly score
- rank
- detector evidence
- relevant measurement and limits
- deviation/margin
- device/test/lot/wafer identifiers
- PASS/FAIL status if available
- failure mode if available
- retest count if available
- concise reason for flagging

## Investigation views
Aggregate anomalies by device, test, lot and wafer. Compare anomaly prevalence with PASS/FAIL and failure modes.

## Explainability
Clearly distinguish statistical abnormality from suspected physical cause. A flagged record is not automatically a failed device.

## Edge cases
Handle too few rows, constant features, missing measurements, missing limits, and unavailable failure labels.
