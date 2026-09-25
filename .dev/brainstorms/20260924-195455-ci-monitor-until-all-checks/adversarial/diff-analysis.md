# Diff Analysis: spec Comparison

## Metadata
- Generated: 2026-09-24T20:05:00Z
- Variants compared: 3
- Categories: structural (2), content (4), contradictions (0), unique (3), shared assumptions (3)

## Structural Differences

| # | Area | V1 architect | V2 refactorer | V3 qa | Severity |
|---|------|--------------|---------------|-------|----------|
| S-001 | Org | Problem → thesis → FRs → files | Problem → wait≠fix → FRs | Goals → AC tables → edges | Low |
| S-002 | Depth | File delta + spec FM-CI-7 rewrite | Smallest file list | Test IDs + false-clean catalog | Low |

## Content Differences

| # | Topic | V1 | V2 | V3 | Severity |
|---|-------|----|----|----|----------|
| C-001 | Wave 8 after HALT_MAX_ROUNDS | wait-only; auto-fix stays budget-gated | same; FM-CI-7 is the debt | same; G-3 | Low (same conclusion) |
| C-002 | as_array empty | fail-soft, one JSON line | `${1:-[]}` / never `--argjson ""` | T-CI-POLL-AS-ARRAY-EMPTY | Low |
| C-003 | empty vs parse-fail | `[]` + state=polling → polling | unparsed ≠ parsed empty | AC-CLS-8 / FC catalog | Low |
| C-004 | `--ci-timeout` | defer until measured | defer | out of AC set | Low |

## Contradictions

None. All three keep `fsm.py` frozen, no new EventType, no `gh run rerun`.

## Unique Contributions

| # | Variant | Contribution | Value |
|---|---------|--------------|-------|
| U-001 | V1 | Explicit Wave 8 **entry table** in `ci-poll.md` / SKILL | High |
| U-002 | V2 | Wait ≠ fix split; findings after halt → REPORT_ONLY not Waves 3–5 | High |
| U-003 | V3 | Mix pending+pass AC; false-clean catalog FC-1–FC-12; E9 required-only | High |

## Shared Assumptions

| # | Assumption | Classification | Promoted |
|---|------------|----------------|----------|
| A-001 | In-session Monitor is enough (no daemon) | STATED | no |
| A-002 | `--required` nonempty means optional pending is OK | UNSTATED | yes — E9 |
| A-003 | 600s after source-flip is enough until measured otherwise | STATED (defer `--ci-timeout`) | no |

## Summary
- Highest-severity: none High. Convergence expected high.
- Agreement: wait after halt; poller fail-soft; pending wins over pass.
