# Gate 1 Fix Log - Fix Cycle 2 (Item 3.22)

Input: `qa/qa-consolidated-findings-phase3-c2.md` (F_1 = 2). fix_authorization: true. Edits limited to `research/`. No research agent was spawned (no new investigation needed).

## Findings

| ID | File | Row | Change made | Status |
|----|------|-----|-------------|--------|
| P3-C2-001 | research/24-value-ledger-evidence-consumers.md | VL-24-211 (L224) | In the claim cell, escaped the pipe inside the backticked command: `diff src plugin \| grep -c '^[<>]'`. Wording, tags and citations unchanged. | FIXED |
| P3-C2-002 | research/20-value-ledger-e2-study.md | VL-20-625 (L636) | In the claim cell, escaped the pipe inside the backticked command: `...combos \| wc -l`. Wording, tags and citations unchanged. | FIXED |

## Read-only pipe check (after the fixes)

Rule: every row starting `| VL-` must have exactly 7 pipes once each backslash-escaped pipe (`\|`) is removed (awk: strip `\|`, count the remaining `|`).

| Ledger | VL rows | Exactly 7 unescaped pipes | Other |
|--------|---------|---------------------------|-------|
| research/19-value-ledger-handoffs.md | 886 | 886 | 0 |
| research/20-value-ledger-e2-study.md | 868 | 868 | 0 |
| research/21-value-ledger-brainstorms.md | 1685 | 1685 | 0 |
| research/22-value-ledger-collab-designs.md | 955 | 955 | 0 |
| research/23-value-ledger-e1-e3-code.md | 796 | 796 | 0 |
| research/24-value-ledger-evidence-consumers.md | 589 | 589 | 0 |

## Additional rows with the same defect

None. The check found no row outside VL-24-211 and VL-20-625 with a pipe count other than 7 (those two were fixed before the check ran).

## Not fixable

Nothing. Minor findings from the review were left alone as instructed.
