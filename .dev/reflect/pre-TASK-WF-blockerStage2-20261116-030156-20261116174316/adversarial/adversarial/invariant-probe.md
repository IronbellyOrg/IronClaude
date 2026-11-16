# Invariant Probe Results

## Round 2.5 - Fault-Finder Analysis (sonnet, independent; every entry cites a live file line)

| ID | Category | Assumption | Status | Severity | Evidence |
|----|----------|------------|--------|----------|----------|
| INV-001 | state_variables | A second `write` leaves rows tagged by `safety` untouched | UNADDRESSED | MEDIUM | plan:88 write then safety per phase and per fix cycle; only idempotence test is plan:61 (no `safety` between writes) |
| INV-002 | state_variables | `capture_state: incomplete` survives a later successful `write` | UNADDRESSED | MEDIUM | spec:345 single header value; plan:56; summary test plan:62 covers only the unreadable-report case |
| INV-003 | guard_conditions | A `--confirmed-misses` file means rows were reviewed | UNADDRESSED | MEDIUM | plan:138 prints "not computable" only when the file is absent; an empty file prints a bare 0; stage 3 plan:49 accepts "safety misses 0 (not "not computable")" |
| INV-004 | collection_boundaries | Zero ledgers, zero runs, zero non-blocking rows are handled | UNADDRESSED | MEDIUM | plan:56 sweep exit rule for zero ledgers unstated; plan:138 share has no divisor guard; plan:141 no empty-input test |
| INV-005 | collection_boundaries | Every Task 7 set has enough rows for kappa, recall, kind split | UNADDRESSED | MEDIUM | stage 0 plan:96 fresh set of 17; plan:126 figures with no "not computable" convention |
| INV-006 | interaction_effects | Stage 3 can find stage 2's paragraph title and "never --promote" words | UNADDRESSED | LOW | stage 3 plan:177; Task 3 acceptance (plan:77-82) and Task 6 test do not pin the title or words |
| INV-007 | count_divergence | Task 4 covers the tech-research reviewers; capture state is meaningful | UNADDRESSED | LOW | tech-research SKILL.md:1164 source-fidelity and :1207 anti-omission reviewers get no field; stage 1 makes the registry tuple ten |
| INV-008 | sufficiency_challenge | Task 8 acceptance commands run as written | UNADDRESSED | MEDIUM | plan:141 `uv run python ./artifacts/shadow_summary.py --help` from the repo root; `./artifacts/` is package-relative (plan:33) and does not exist at the root |
| INV-009 | sufficiency_challenge | Task 4 body and its `grep -ci sweep` check agree | UNADDRESSED | LOW | plan:88 vs plan:92 (same as card finding F5/C-012 wording) |
| INV-010 | sufficiency_challenge | Task 3 placement check forces the call after `FINAL: pass` | UNADDRESSED | LOW | managed-workspace.md:56 step 5, :58-60 FINAL block, :62 step 6; plan:78 only requires "after the step 5 line and before the step 6 line" |

## Summary

- **Total findings**: 10
- **ADDRESSED**: 0
- **UNADDRESSED**: 10
  - HIGH: 0
  - MEDIUM: 5 (INV-001, 002, 003, 004, 005, 008 = 6 listed MEDIUM)
  - LOW: 4
- Correction to the line above: MEDIUM = 6 (INV-001, INV-002, INV-003, INV-004, INV-005, INV-008), LOW = 4 (INV-006, INV-007, INV-009, INV-010).
- Gate: count(HIGH + UNADDRESSED) = 0, so convergence is not blocked. MEDIUM items are warnings and enter the merged register as follow-up candidates.
