# Prompt 05 — Yield, Failure and Engineering Analytics

Implement the deterministic analytics engine for Task 1.

## Required outputs
- overall PASS yield and FAIL rate
- counts and percentages
- yield by Test_ID/Test_Name
- yield by Lot_ID
- yield by Wafer_ID
- top failing tests
- common failure modes
- retest statistics
- useful condition summaries by temperature/VDD where available

Use the dataset's actual Result values. Normalize obvious case/whitespace variations through a documented mapping; do not invent labels.

## Engineering summary
Generate a structured summary containing observations such as highest-failure tests, lots/wafers with unusual yield, dominant failure modes, retest concentration, and data-quality caveats. Keep observations separate from hypotheses.

## API/UI compatibility
Return JSON-serializable objects with stable field names. Avoid enormous payloads; support top-N parameters.

## Tests
Verify calculations against small hand-built fixtures, including missing Result values and zero-denominator groups.
