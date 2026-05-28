# Tier 1 Observation — Calibration miss reproducer

## Symptom (replicated structurally from pr86 substrate)

In pr86, all three Tier 2 cards marked `Evidence grounding = 0.5` with the SAME stated reason — calibrator lacked Bash to `git show <pinned-sha>:<file>` and verify PR-pinned snippets. Yet:

- RCA card calibrated to **0.90** (4 × 1.0 + 0.5 = 4.5 / 5 = 0.90)
- QE card calibrated to **0.60** ONLY because fix-directness ALSO dropped to 0.5 (3 × 1.0 + 2 × 0.5 = 4.0 / 5 = 0.80, then narrative pulled to 0.60 in the report)

The H3 miss matches the RCA fingerprint exactly: one grounding-class dimension at 0.5, four other dimensions strong → arithmetic mean clears the 0.85 gate → REFUTE shipped at 0.95.

## Reproducer (arithmetic, not runtime)

Given the rubric (`escalation-rubric.md:19`):
```
calibrated = (evidence + symptom + repro + fix + domain) / 5
```
H3 case modelled:
- evidence = 0.5 (source-only; runtime unverified)
- symptom = 1.0
- repro = 1.0
- fix = 1.0
- domain = 1.0
- → 4.5 / 5 = 0.90, rounded up by narrative to 0.95 = REFUTE high-confidence.

This is structural, not flaky. The bug is in the *aggregation function*, not the individual scoring.

## No-MCP grounding fallback noted

Per `--no-mcp`: auggie/serena/context7/tavily skipped. All grounding via Read + native logic against the substrate dir and mechanism artefacts.
