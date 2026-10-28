---
topic: "Decide how to handle the remaining token-only gaps in the Task 11 contract tests (auggie claim gate), or accept them; produce a remediation proposal and an ROI/risk judgement"
domain: process
strategy: systematic
depth: standard
proposals_target: 3
handoff_target: none
created: 2026-10-21
mode: non-interactive (operator brief supplied the dialogue answers)
---

# Seed Brief: task11-token-gaps

## Problem Statement

`tests/skills/test_auggie_claim_gate_contract.py` (44 tests, all pass, all 3 Task 11 acceptance criteria met) checks prose protocol files with `need(text, *substrings)` and 27 "remove one sentence" mutation tests. Three independent reviewer rounds returned `missing` (43/116, then 9, then 10 of 179 uncaught). Each fix round closed the named gaps and the next round found new ones. Ten named gaps remain (list in `enrichment/codebase-context.md`). The operator-controlled halt policy permits only an explicit operator decision. Decide: remediate (how), accept (ruling text), or hybrid, and give an ROI/risk judgement.

## Known Context (verified this session, see enrichment)

- All 10 named gaps reproduced by in-memory mutation: all survive the current checks (G7 survives only in the rubric copy; the gate copy of the same sentence is asserted and is caught).
- Arbitrary sweeps over the 7 protocol files (jq block excluded): 81% of 467 modal/negation flips and 81% of 1,112 sentence deletions survive. A needle suite cannot reach 100% without asserting nearly every sentence.
- Other checks: jq program J1-J22 (63 fixture pairs) is a RUNTIME tripwire as well as a test target; Task 12 oracle (not built) is a test-only re-implementation that only binds to the prose through the A1-A7 table equality check (AT-16); Task 13 is a regression/scope run; spec 11.3 live evaluation is a separately authorized pre-merge gate.
- Constraints: no pytest markers / conftest / pyproject changes; no edits to source.md or the plan; tests stay ordinary pytest in `tests/skills/`; new files only under paths in source section 2 (fixtures dir allowed); AT-20 bans case ids (C1-C8c, R1-R9, T1-T6) and PR numbers in fixture text; `#### C1.` appears in SKILL.md:215 and claim-gate.md:224.

## Constraints

- Analysis only. No edits under src/, tests/, or the task package. No git add/commit/push.
- Write only under `.dev/brainstorms/20261021-task11-token-gaps/`.

## Success Criteria

- One verdict (REMEDIATE / ACCEPT / HYBRID) with exact list or exact Ruling text.
- Gap-by-gap table (backstop class, severity if slips, action).
- A finite, defensible definition of "done" for static contract tests of a prose protocol.
- Top 3 risks of the recommended path.

## Open Questions

- Is a section-snapshot ("golden") check compatible with AT-20 and with later legitimate edits?
- Which gaps flip a publish/status outcome with no other backstop?
