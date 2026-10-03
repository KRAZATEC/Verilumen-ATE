# Prompt 20 — Final Verilumen Assessment Compliance Audit

Act as an independent senior reviewer. Do not modify code initially. Audit the entire repository against every requirement in the assessment PDF.

## Produce a traceability matrix
For every requirement record:
- requirement
- implementation file/module
- API/UI surface
- test or verification method
- status: PASS / PARTIAL / FAIL / NOT APPLICABLE
- evidence
- remediation needed

## Explicitly audit
### Task 1
Profiling, missing values, duplicates, abnormal measurements, yield/fail rate, test/lot/wafer yield, top failures, failure modes, 4+ visualizations, engineering summary.

### Task 2
Target definition, feature rationale, leakage-safe preprocessing, at least two classifiers, comparison metrics, imbalance, influential features, model persistence, reusable prediction, unseen records, accuracy limitation.

### Task 3
Anomaly detection, ranking, suspicious devices/tests, comparison with results/failure modes, explanation, algorithm/parameter documentation, observed vs inferred causes.

### Task 4
Upload/process/dashboard/investigation/AI analysis/prediction flow, evidence grounding, insufficient-evidence behavior.

### Submission
Runnable source, README, assumptions, commands, EDA, conclusions, ML evaluation, saved/reproducible model, working UI/API, tests, documentation, demo readiness.

## Final gates
Also inspect:
- hard-coded values
- data leakage
- fake UI metrics
- missing error states
- broken fresh-install setup
- missing environment documentation
- unsafe file upload handling
- unsupported causal claims
- undocumented assumptions
- reproducibility

## Output
Create `reports/final_assessment_audit.md` with findings ordered by severity and a concrete remediation checklist. Only after the audit, implement fixes and rerun tests.
