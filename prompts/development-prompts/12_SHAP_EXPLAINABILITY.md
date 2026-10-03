# Prompt 12 — SHAP and Model Explainability

Implement model explainability using SHAP when compatible with the selected model and provide a fallback feature-importance method.

## Required outputs
- global feature importance
- per-record local contribution for predictions
- direction of contribution where supported
- human-readable feature descriptions

## Safety
Explain that feature contribution describes model behavior, not physical causality. Do not convert SHAP into a statement such as “temperature caused the failure.” Instead phrase it as “temperature-related feature contributed to the model's prediction.”

## Performance
Avoid recomputing expensive explainers unnecessarily. Cache compatible explainers/artifacts.

## Tests
Verify explanation schema, unseen-record explanation, and graceful fallback if SHAP is unavailable.
