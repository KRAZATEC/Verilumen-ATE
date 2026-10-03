# Prompt 09 — Rigorous Model Evaluation

Implement evaluation that satisfies the assessment and avoids misleading conclusions.

## Metrics
Report at minimum:
- precision
- recall
- F1
- ROC-AUC when defined
- PR-AUC / average precision when defined
- confusion matrix
- support/class distribution

Include accuracy as a contextual metric, not the sole decision metric.

## Why accuracy can be insufficient
Document that in imbalanced failure detection, a model can obtain high accuracy while missing a large fraction of failures. Explain this using the dataset's actual class distribution rather than a fabricated example.

## Threshold analysis
Support configurable classification thresholds and show precision/recall trade-offs. Do not silently choose a threshold solely to maximize a metric without documenting the criterion.

## Comparison
Produce a structured model comparison object. Do not produce an overall ranking/winner claim automatically; show the measurements and selection rationale separately.

## Tests
Use deterministic fixtures where expected metric values can be calculated exactly.
