# Merge Log

## Metadata
- Base variant: Variant 3 (opus:refactorer), `variant-3-original.md`
- Plan: `refactor-plan.md` (9 planned changes plus the R3-F6 relabel and coverage line; 3 rejected)
- Other inputs: `variant-1-original.md`, `variant-2-original.md`, `invariant-probe.md`, `debate-transcript.md` (evidence only)
- Merge date: 2026-11-04T18:56:00Z
- Output: `merged-verdict.yaml`
- Convergence score: 0.95

## Changes Applied

| # | Planned change | Status | Resulting finding |
|---|----------------|--------|-------------------|
| 1 | Downgrade R3-F1 to minor | applied | M-01 (severity minor; class drift kept) |
| 2 | Replace R3-F8 with V1 R1-F1 class and remedy | applied | M-08 (class grounding_gap, severity minor, remedy: delete only the gitignored mirror file after `make sync-dev`, `make verify-sync` to exit 0, never `git add` `.claude/`; sources 1, 2, 3) |
| 3 | Narrow R3-F4 per INV-002 | applied | M-04 (last-segment meaning only for `analysis/analyze-<scope>.md`; `refs/chains.md:7` unchanged) |
| 4 | Merge R2-F2 into R3-F5 | applied | M-05 (sources 2, 3; `refs/claim.md:58` added to file_line) |
| 5 | Merge R2-F4 into R3-F7 | applied | M-07 (sources 2, 3; probe case `<REPORT.md` -> no match) |
| 6 | Add V2 R2-F3 | applied | M-10 (minor) |
| 7 | Add V1 R1-F3 as authorized no-change note | applied | M-11 (class authorized, minor) |
| 8 | Add INV-001 | applied | M-12 (grounding_gap, minor) |
| 9 | Add A-001 + INV-007 handoff note | applied | M-13 (grounding_gap, minor) |
| - | R3-F6 marked informational (minor) | applied | M-06 (claim begins "Informational"; severity minor) |
| - | V2 coverage line recorded in verdict header | applied | `coverage_check: "9/9 spec spans present (variant-2)"` |

Unchanged base findings carried over: R3-F2 -> M-02, R3-F3 -> M-03, R3-F9 -> M-09.

Not applied (rejected in the plan, not included): V1 R1-F4 (import fails; refuted), V1 `<target>` placeholder rename (withdrawn in Round 2), V1 "blocking" grade for the stale mirror (conceded to minor in Round 2).

## Post-Merge Validation
- YAML parses: checked with a YAML loader after writing (result recorded in the final report).
- Every finding has all fields: id, file_line, claim, class, severity, recommendation, source_variants (13 of 13). Class values are within authorized | necessary | drift | grounding_gap; severity values are within blocking | minor.
- Counts: blocking_count 0, minor_count 13, matching the findings list.
- Citations: every file_line string reuses locations as they appear in the inputs; none were invented.
- Contradictions: none introduced. M-04 keeps `refs/chains.md:7` unchanged, consistent with M-05 (exact `analyze-<scope>.md` literal) and M-11 (`SKILL.md:66` untouched). M-08 (delete the mirror after `make sync-dev`) does not conflict with the `.claude/` no-staging rule.
- Provenance: each entry has a `# Source:` comment naming its origin and change number.

## Summary
All 9 planned changes plus the R3-F6 relabel and coverage line were applied to the Variant 3 base. The result has 13 findings, 0 blocking and 13 minor. Verdict is PASS (with notes).
