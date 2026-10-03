# Verilumen ATE Intelligence — Master AI Coding Rules

## Purpose
You are contributing to a production-quality AI engineering assessment project for semiconductor ATE/test-result analysis. Build incrementally, preserve previous work, and keep the implementation dataset-agnostic.

## Non-negotiable rules
1. The supplied official CSV is the primary dataset. The synthetic CSV is development-only.
2. Never hard-code expected yields, failure modes, anomaly IDs, model scores, thresholds, or dashboard numbers.
3. Never manually label records merely to force expected results.
4. The application must accept a new CSV with the same logical schema without source-code rewrites.
5. Preserve raw uploaded data. Create explicit cleaned/derived layers; never silently mutate the raw dataset.
6. Every cleaning decision must be observable in data-quality reports.
7. Do not silently drop duplicates or outliers. Detect, classify, document, and apply an explicit policy.
8. Never use post-outcome information for a pre-test prediction model. Treat Result, Failure_Mode, post-test measurements, and other outcome-derived fields as leakage unless the prediction task explicitly defines otherwise.
9. Prefer group-aware validation when multiple rows belong to the same device/wafer/lot and explain the grouping decision.
10. Evaluate more than accuracy: include precision, recall, F1, ROC-AUC, PR-AUC and confusion matrix where technically applicable.
11. Handle class imbalance explicitly and report the method used.
12. Model explanations are evidence about model behavior, not proof of physical causality.
13. Separate observed evidence from inferred/possible causes in all AI analysis.
14. If evidence is insufficient, say so. Never invent an engineering explanation.
15. Deterministic analytics/ML are the source of truth. An optional LLM may only verbalize structured evidence and must not invent measurements or statistics.
16. Dynamic UI must never display fake metrics when no dataset is loaded.
17. APIs must validate inputs, return structured errors, and remain usable with unseen records.
18. Keep business/engineering logic out of UI components. Keep API routes thin and call services.
19. Write unit/integration tests for important logic and edge cases.
20. Add logging without exposing sensitive uploaded data unnecessarily.
21. Use type hints and clear schemas. Prefer small testable modules over monolithic files.
22. Preserve backwards compatibility when extending existing modules.
23. Before changing architecture, explain the reason and impact in the relevant documentation.
24. Every assessment requirement must map to implementation and/or an automated/manual verification step.
25. Run formatting, linting and tests after meaningful changes.

## Engineering standard
Use configuration instead of magic constants. Use deterministic random seeds for development data. Make pipelines reproducible. Fail gracefully on insufficient data. Return machine-readable results from backend services. Keep documentation synchronized with behavior.

## Expected stack
Backend: Python 3.12+, FastAPI, Pydantic v2, Pandas/Polars, NumPy, scikit-learn, CatBoost, XGBoost, SHAP, joblib, pytest, Ruff, Black, MyPy.
Frontend: Next.js, React, TypeScript, Tailwind CSS, shadcn/ui, Recharts or ECharts, Lucide React, Framer Motion.
Infrastructure: Docker/Docker Compose.

## Definition of done for every prompt
- Existing functionality is preserved.
- New functionality is implemented, not mocked.
- Edge cases are handled.
- Tests are added/updated.
- Documentation is updated if behavior or architecture changed.
- No hard-coded assessment answers.
- The implementation remains compatible with a new same-schema CSV.
