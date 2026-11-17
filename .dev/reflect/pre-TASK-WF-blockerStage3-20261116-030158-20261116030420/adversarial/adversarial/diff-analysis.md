# Diff Analysis: reviewer-card comparison (stage 3 plan, pre-execution)

## Metadata

- Generated: 2026-11-16 (orchestrator, step 1 of /sc:adversarial Mode A)
- Variants compared: 2 (variant-1 = reviewer 1 card, analyzer, haiku class, calibrated C 0.83; variant-2 = reviewer 2 card, qa, opus class, calibrated C 0.79)
- Plan under review: `.dev/tasks/to-do/TASK-WF-blockerStage3-20261116-030158/TASK-WF-blockerStage3-20261116-030158.md` (line numbers `PLAN:n`); its source `source.md`
- Total diff points: 21 (structural 1, content 7, contradictions 2, unique 7, shared assumptions 4)
- Grading rule both cards were given: blocking = a requirement or check that cannot be met, a wrong or missing result, or data loss; minor = wording or format.

## Structural Differences

| # | Area | Variant 1 | Variant 2 | Severity |
|---|------|-----------|-----------|----------|
| S-001 | Card shape | 8 findings; every finding carries `Category: Drift`; "Checked and sound" lists 7 bullets | 11 findings, no category label; "Checked and sound" maps the prior review's recommendations R-002, R-003, R-005 and lists exact line cites checked | Low |

## Content Differences

| # | Topic | Variant 1 approach | Variant 2 approach | Severity |
|---|-------|--------------------|--------------------|----------|
| C-001 | Task 1 entry check on the stage 2 summary (`PLAN:37`) | F2 blocking: the stage 2 summary (stage 2 plan line 110 "zero runs") is not refreshed; says the T1 card's "cannot exist by construction" is too strong; fix: regenerate a dated summary from the run folders with the stage 2 script | F1 blocking: file cannot hold the count; source.md:3 lists the two conditions separately and the plan merged them; a fix cycle may edit the other package's summary and fake the gate; fix: first step runs `shadow_summary.py`, check entry conditions before spawning, add a halt clause | Low (both blocking, same fix idea) |
| C-002 | Old rule injected into the new-rule pass (Task 1) | F3 blocking: `pragmatic-subagent.js:15` injects the instructions; Task 1 neither overrides the injected rule nor requires disclosure; also unstated matching reviewer configurations | F4 blocking: `pragmatic-subagent.js:7` reads `~/.claude/output-styles/pragmatic.md`; stage 0 plan :76 names the same confound for its re-grade and this plan does not | Low |
| C-003 | Pass or fail rule and the advisory fallback (`PLAN:33`, `PLAN:62`) | F4 blocking: stage 0 plan :110 lets a class's pass line be advisory; Task 3 needs "pass on all three"; no rule for an advisory outcome or the owner ruling that lets the run continue | F2 blocking: no rule says how pass or fail is judged (exact equality on a small set is noise); an advisory class can never show pass so Task 3 halts by construction; spec :680 says "same reviewers", plan only fresh spawns | Medium |
| C-004 | Tasks 4 and 5 read `./artifacts/stage0-inventory-freeze.md` (`PLAN:73`, `PLAN:85`) | F5 blocking: the file is written by stage 0 Task 1; points into this package's folder | F3 blocking: same facts; `PLAN:27` says `./artifacts/` is this package; acceptance `PLAN:77` has no input file; `PLAN:19` (earlier evidence read by package id) is not weighed | Medium (calibrators: grade high because `PLAN:19`) |
| C-005 | Stale numbering from the renumbering (`PLAN:147` "Tasks 34 to 37", `PLAN:126` `t38`) | F8 non-blocking; says `t38` name is cosmetic | F10 non-blocking; fix renames the artifact | Low |
| C-006 | Registry check `grep -n "sc-review-severity"` (`PLAN:116`) | F7 non-blocking | F11 non-blocking | Low |
| C-007 | Order of the entry checks versus the spawn (T1-card O5) | "Checked and sound": disagrees; the Constraints prohibit starting before entry conditions hold | F1 fix says check entry conditions before spawning; "Checked and sound" disagrees only with the package-id part of O5 (stage ledger `README.md:17`, `PLAN:19`) | Medium |

## Contradictions

| # | Point of Conflict | Variant 1 Position | Variant 2 Position | Impact |
|---|-------------------|--------------------|--------------------|--------|
| X-001 | Is running the to-be-re-pinned tests in Task 3 a defect (`PLAN:59`) | Not a defect: Task 3 "requests running the old tests, not that those tests pass before Task 8"; its explicit pass check is the brief-rests-on test | F9 (non-blocking): the per-task check can flag Tasks 3 and 4 as failed; fix: state the expected failures with "until Task 8" and "until Task 9" | Low |
| X-002 | Do the Constraints already make the entry checks precede the work | Yes: "the Constraints explicitly prohibit starting before entry conditions hold" (`PLAN:20`) | No: the checks are acceptance lines `PLAN:36-38` evaluated after the body; fix adds a first step | Medium |

## Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---------|--------------|------------------|
| U-001 | 1 (F1, blocking) | `make sync-dev` (`Makefile:109`) copies project components only; the hook reads `~/.claude/output-styles/pragmatic.md`; Task 3 names no refresh, so later reviewers still get the old rule | High (spec REQ-26 puts the refresh in steps b and c of the three-step switch, outside the repository edit) |
| U-002 | 1 (F6, blocking) | `PLAN:162` has the summary say "no revert trigger can be judged until the audit window has run" but RT1 (`merged-requirements.md:985`) covers "the seeded set", which Task 1 produces before the window | Medium |
| U-003 | 2 (F5, blocking) | M12 (`merged-requirements.md:974`) has baseline source "stage 2"; the stage 2 plan's exit numbers (line 110) hold no rf-qa FAIL count; Task 11 only quotes M12 | Medium |
| U-004 | 2 (F6, blocking) | The stage 1 test `tests/skills/test_review_severity_registry.py` (T1: v2 digest equality; stage 1 plan line 209) is not in Task 8's pytest list (`PLAN:125`); Tasks 4 and 5 check only "exactly one digest" | Medium |
| U-005 | 2 (F7, non-blocking) | The source's third "not to be done" item (no template, rule-prompt, builder, researcher or spec-panel edit, `source.md:20`) is absent from `PLAN:22` | Low |
| U-006 | 2 (F8, non-blocking) | Task 8 does not say what the legacy rows of `S1_S3_FILES` (`tests/skills/test_review_severity_rule.py:181-192`) stay pinned to when `canonical_rule_bullets()` reads the v2 digest | Low |
| U-007 | 2 (F9, non-blocking) | Task 3 runs tests that fail until Tasks 8 and 9 without saying so (see X-001) | Low |

## Shared Assumptions

| # | Assumption | Source Agreement | Classification | Promoted |
|---|------------|------------------|----------------|----------|
| A-001 | `/sc:implement` evaluates each task's acceptance lines as hard checks after the task body and halts the whole run when one fails (so a failing entry check stops the package) | both cards grade entry-check problems by what happens at a halt | UNSTATED | yes |
| A-002 | Reviewers spawned by Task 1 receive the installed `~/.claude/output-styles/pragmatic.md` through the SubagentStart hook, and that file is the old rule until someone runs `superclaude update` | C-002, U-001 | STATED | no |
| A-003 | The stage 0, stage 1 and stage 2 plans will be executed as written, so the file names and contents their acceptance lines promise will exist (the stage 0 plan's own review said NEEDS-REVISION) | C-001, C-004, U-003, U-004 | UNSTATED | yes |
| A-004 | A check that halts the run for the owner is a "check that cannot be met" and so blocking, even when the halt is the plan's designed safe outcome | C-001, C-003, C-004 | UNSTATED | yes |

### Promoted shared assumptions

| # | Assumption | Impact | Status |
|---|------------|--------|--------|
| A-001 | acceptance lines are hard, halting checks | decides the consequence of every "check cannot be met" finding | open |
| A-003 | producing plans run as written | cross-package findings depend on it | open |
| A-004 | a designed safe halt counts as blocking | decides the grade of C-001, C-003, C-004 | open |

## Summary

- Total structural differences: 1
- Total content differences: 7
- Total contradictions: 2
- Total unique contributions: 7
- Total shared assumptions surfaced: 4 (UNSTATED: 3, STATED: 1, CONTRADICTED: 0)
- Highest-severity items: U-001
- Similarity check: the cards agree on 6 of the 8 findings of variant 1 in substance (C-001 to C-006), so the variants are not substantially identical; the debate runs.
