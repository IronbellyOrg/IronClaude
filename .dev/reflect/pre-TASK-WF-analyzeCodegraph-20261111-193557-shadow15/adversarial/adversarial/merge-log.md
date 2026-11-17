# Merge Log — shadow15 adversarial merge

## Metadata

- Base: Variant 2 (qa / haiku / claude-haiku-5-5), combined score 0.816 (base-selection.md)
- Executor: compact single-agent merge (this session, same honesty note as debate-transcript.md)
- Changes applied: 7 of 7 planned | skipped: 0 | failed: 0
- Status: success
- Timestamp: 2026-11-13T03:0x Z (session time)

## Changes Applied

| # | Change (from refactor-plan.md) | Status | Before → After | Provenance tag |
|---|-------------------------------|--------|----------------|----------------|
| 1 | Insert V1-F1 as family head (symbolsOnly/wildcard ban ungated) | Applied | Not in base → merged F1 | `<!-- Source: Variant 1 (analyzer) -->` via F1 provenance field |
| 2 | Insert V1-F3 (access:mcp gate ungated) | Applied | Not in base → merged F2 | `<!-- Source: Variant 1 (analyzer) -->` |
| 3 | Re-scope base F1 (drop matrix-row clause, keep AC-level gap) | Applied | V2-F1 (0.6) → merged F3 (0.6), refutation recorded in-card | `<!-- Source: Base (Variant 2), modified -->` |
| 4 | Unbundle base F2 (drop return-contract clause; symbolsOnly → F1; keep 25-line cap → F3) | Applied | V2-F2 split 3 ways; only cap residue survives inside F3 | `<!-- Source: Base (Variant 2), modified -->` |
| 5 | Keep base F3/F4 verbatim | Applied | V2-F3 → merged F4 (INV-004 re-scope of one clause, noted in provenance); V2-F4 → merged F5 verbatim | `<!-- Source: Base (Variant 2) -->` |
| 6 | Insert V3-F1 (guide verb-list duplication) | Applied | Not in base → merged F6 | `<!-- Source: Variant 3 (refactorer) -->` |
| 7 | Insert V3-F3 reduced-scope (density at execution commit only) | Applied | V3-F3 (0.6) → merged F7 (0.55) | `<!-- Source: Variant 3 (refactorer), modified -->` |

Structural: the family grouping from Round 2 (V1 rebuttal, adopted) is realized as F1/F2/F3 sharing one missing-requirement family narrative with cross-references in provenance fields, rather than a nested sub-structure — keeps the findings-v2 block machine-parseable (one JSON object per line).

## Post-Merge Validation

- Structural integrity: PASS — H1 title, 7-finding fenced findings-v2 block, one object per line, calibration block, provenance comments per skill template.
- Internal references: PASS — refutation table cross-references diff-point IDs (X-001..X-004) that exist in diff-analysis.md; provenance fields reference debate winners that exist in debate-transcript.md scoring matrix.
- Contradiction re-scan: PASS — no new contradictions. The one candidate (F3 mentions its own refuted clause) is self-consistent: the claim states the refutation outcome, matching the refutation table.
- Citation spot-check: 13/13 citations verified against Read/git evidence this session; F1's tasklist citation spans the Task 1 AC block (lines 33-34), the correct anchor for an AC-absence claim.

## Summary

- Planned: 7 | Applied: 7 | Failed: 0 | Skipped: 0
- Refuted findings dropped with refutations recorded: 4 (V1-F2, V2-F1 matrix clause, V2-F2 return-contract clause, V3-F2) — recorded in merged-output.md "Refuted findings" table and debate-transcript.md
- Merged output: `../merged-output.md` (work-dir root, one level above this adversarial/ directory)
