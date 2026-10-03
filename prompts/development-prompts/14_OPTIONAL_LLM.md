# Prompt 14 — Optional Evidence-Grounded LLM Layer

Implement an optional LLM narrative layer only after the deterministic pipeline works.

## Architecture
The deterministic evidence engine remains the source of truth. The LLM receives a compact structured evidence object and is forbidden from inventing values, identifiers, statistics, failure modes, or physical causes.

## Prompt contract
Require the LLM to:
- summarize only supplied evidence
- distinguish observation from inference
- state when evidence is insufficient
- cite evidence keys/record fields in the generated response
- avoid claiming causality without direct evidence
- avoid fabricated confidence

## Fallback
If no LLM credentials are configured, the application must use deterministic templated narratives and continue to function.

## Privacy
Do not send the full uploaded dataset to an external model. Send only the minimum structured evidence required for the selected investigation, and make provider configuration explicit.

## Tests
Use a mock LLM client and verify prompt construction, grounding, fallback behavior, and refusal to fabricate absent evidence.
