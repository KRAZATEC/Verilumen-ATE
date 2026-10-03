# Prompt 13 — Evidence Engine and Engineering Reasoning

Build the central evidence engine that powers the Investigation and AI Analysis screens.

## Inputs
Combine only computed evidence:
- raw/cleaned record values
- data-quality findings
- specification limits and margins
- yield/failure analytics
- anomaly detector outputs
- model prediction/probability
- SHAP/local feature contributions
- failure mode and retest information
- relevant lot/wafer/test aggregates

## Output structure
Return:
- observed evidence
- model evidence
- anomaly evidence
- contextual evidence
- possible interpretations
- confidence/strength of evidence
- limitations/unknowns
- source fields/record identifiers

## Critical rule
Observed evidence and inferred causes must be separate sections. If the supplied data cannot support a causal explanation, explicitly state that the evidence is insufficient.

## Reproducibility
The same input record and model version should produce the same structured evidence under deterministic configuration.

## Tests
Create fixtures proving that unsupported causal claims are not generated.
