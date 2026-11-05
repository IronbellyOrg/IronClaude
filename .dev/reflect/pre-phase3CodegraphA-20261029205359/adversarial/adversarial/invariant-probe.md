# Invariant Probe Results

## Round 2.5 — Fault-Finder Analysis

The fault-finder probed `consensus-draft.md` (M-01..M-18). One independent general-purpose agent did this, separate from both advocates. The Status column shows the probe-time status. The Resolution column shows where the merge carries each item.

| ID | Category | Assumption | Status | Severity | Evidence | Resolution |
|----|----------|------------|--------|----------|----------|------------|
| INV-001 | guard_conditions | M-01: the body text can be passed literally to `gh pr create --body "…"` | UNADDRESSED | HIGH | `sc-pr-submit-protocol/SKILL.md:189` puts `--body` in double quotes, so backticks and `$` inside it expand | folded into M-01 |
| INV-002 | state_variables | M-06: copying the package into the worktree is enough | UNADDRESSED | HIGH | `sc-implement-protocol/SKILL.md:64` keeps the ledger at `<package>/progress.md`; the Q0 and Q2 snapshots and diffs (:110-121) run in the current checkout; plan:20 and :37 create the worktree inside Task 1 | folded into M-06 (worktree and inputs set up before the run) |
| INV-003 | interaction_effects | M-06 × M-09: copied inputs get staged | UNADDRESSED | MEDIUM | plan:45, :26 | folded into M-06 |
| INV-004 | guard_conditions | M-17: T1-T10 need no live tool | UNADDRESSED | HIGH | source.md:30; plan:51 (E-1 and E-6 are MCP); plan:65, :67, :96 consume them | M-17 rewritten (keep the H1 stop after the CLI-only experiments; log the departure; severity minor) |
| INV-005 | guard_conditions | every gate row has an owner | UNADDRESSED | MEDIUM | plan:37 maps G1-G4 and G6 only; source.md:27 | folded into M-17 |
| INV-006 | collection_boundaries | the baseline failure file is empty | UNADDRESSED | HIGH | source.md:271 records existing failures without fixing them; plan:82, :125, :190 run whole directories | new finding M-19 |
| INV-007 | collection_boundaries | an empty failure file means the tests ran | UNADDRESSED | LOW | the source.md:271 regex misses collection errors; plan:43 | folded into M-04 |
| INV-008 | sufficiency_challenge | M-08: re-checking `gh pr checks` covers the push made after the monitor | UNADDRESSED | MEDIUM | plan:221 | folded into M-08 |
| INV-009 | state_variables | commit SHAs and Task 13 results survive a rebase | UNADDRESSED | MEDIUM | plan:218; SKILL.md:189 (Wave 0 rebase); source.md:307 | folded into M-08 |
| INV-010 | count_divergence | the installed-path count can only stay equal | UNADDRESSED | LOW | plan:207 `-eq` | folded into M-14 |
| INV-011 | sufficiency_challenge | `sync` is the only verb at risk outside "Never" | UNADDRESSED | LOW | plan:71; source.md:254-257 | folded into M-13 |
| INV-012 | sufficiency_challenge | the membership set is the only routing test the new rows can break | UNADDRESSED | LOW | `tests/core/test_how_we_work_routing_table.py:339-344` (ASCII-only guide) | folded into M-03 |
| INV-013 | guard_conditions | `origin/master` is a stable base for the diff | UNADDRESSED | LOW | consensus M-12; plan:218 | folded into M-12 |
| INV-014 | interaction_effects | M-11 and M-03 collide in Task 12 | ADDRESSED | LOW | different files; plan:126 | none |
| INV-015 | interaction_effects | M-15 breaks the 120-line cap or the verb test | ADDRESSED | LOW | one line, no forbidden verb; DES:478 | none |
| INV-016 | interaction_effects | M-02, M-08 and M-09 commit lists disagree | ADDRESSED | LOW | the body sits in `progress/` | none |

## Summary

- **Total findings**: 16
- **ADDRESSED**: 3
- **UNADDRESSED**: 13
  - HIGH: 4 (INV-001, INV-002, INV-004, INV-006)
  - MEDIUM: 4 (INV-003, INV-005, INV-008, INV-009)
  - LOW: 5

## Gate

```text
CONVERGENCE BLOCKED: 4 HIGH-severity UNADDRESSED invariant(s) detected
Blocking items: INV-001, INV-002, INV-004, INV-006
These invariant violations must be resolved before convergence can be declared.
```

```text
WARNING: 4 MEDIUM-severity UNADDRESSED invariant(s) detected
Items: INV-003, INV-005, INV-008, INV-009
```

The orchestrator checked the evidence for INV-001, INV-002, INV-006 and INV-012 against the repository (`SKILL.md:189`, `sc-implement-protocol/SKILL.md:64,108-121`, `test_how_we_work_routing_table.py:339-344`). It then sent the four HIGH amendments to both advocates as a confirmation round. Their verdicts are recorded in `debate-transcript.md` under "Invariant-gate confirmation round".
