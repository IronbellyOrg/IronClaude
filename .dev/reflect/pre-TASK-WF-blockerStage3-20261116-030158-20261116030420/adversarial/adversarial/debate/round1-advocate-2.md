# Round 1: advocate for variant 2 (reviewer 2 card, qa), model class opus, agent a0b163ce50256f8da

(Persisted verbatim by the orchestrator from the agent's final message; hand-back frame indentation removed. The advocate wrote no file.)

## Position summary

Variant 2 is the more thorough and better-sourced card. Its unique findings U-003 and U-004 are real defects that variant 1 missed, and its readings of C-001 and X-002 are more accurate. Variant 2 has one large gap: it missed variant 1's U-001, the missing refresh of the installed rule file, which is the most serious finding either card makes. A merged card needs both.

## Steelman of variant 1

Variant 1 is the only card that sees that the rule switch never reaches the file the hook actually reads. `pragmatic-subagent.js:7` reads `path.join(os.homedir(), '.claude', 'output-styles', 'pragmatic.md')`. `make sync-dev` (`Makefile:109-158`) copies only into the project `.claude/` folder and never touches output styles. Spec REQ-26 (`merged-requirements.md:762`) says a switch is three steps, "(c) refresh each machine". Variant 1 also catches the `PLAN:162` versus RT1 conflict: RT1 covers "the seeded set" (`:985`), and Task 1 produces that result before the audit window opens. It correctly softens "cannot exist by construction", because five runs could already exist when the stage 2 summary is written. Its findings are fewer but sharply graded.

## Per-point positions

| Point | Winner | Final grade | Survive | Evidence |
|---|---|---|---|---|
| S-001 | V2 | not a finding | no | V2 maps R-002/R-003/R-005; V1 labels every pre-execution item "Drift", which tells the reader nothing |
| C-001 | V2 (add V1's nuance) | blocking | yes | `source.md:3` lists "the owner has read it" and "at least 5 shadow runs" separately; stage 2 `:114` "(zero is allowed)"; repair pass `qa.md:280` makes faking the gate a real risk |
| C-002 | merge | blocking | yes | V2 cites stage 0 `:76` "states the old-rule injection confound"; V1 adds matched reviewer configurations |
| C-003 | merge | blocking | yes | V2: spec `:680` "with the same reviewers"; stage 0 `:106` "the advisory fallback is the expected outcome". V1: owner-ruling path |
| C-004 | tie | minor (concede) | yes | `PLAN:19` "read from their packages by package id"; Task 4 lists the triggers inline |
| C-005 | tie | minor | yes | `PLAN:147` "Tasks 34 to 37" |
| C-006 | tie | minor | yes | `PLAN:116` |
| C-007 | V2 | minor | fold into C-001 | entry checks are acceptance lines `PLAN:36-38`, so they run after the reviewers are spawned |
| X-001 | V1 | minor | optional | `PLAN:59` asks only to run the tests; only `:67` must pass |
| X-002 | V2 | minor | fold into C-001 | `PLAN:20` "(Task 1 checks them)"; the cost is wasted spawns, not a live change |
| U-001 | V1 | blocking | yes | `pragmatic-subagent.js:7`; `Makefile:109-158`; spec `:762` step (c) |
| U-002 | V1 | blocking | yes | `PLAN:162` versus `:985` "or the seeded set" |
| U-003 | V2 | blocking | yes | spec `:974` M12 baseline "stage 2"; grep for M12, "FAIL count" or "baseline" in the stage 2 package finds nothing |
| U-004 | V2 | blocking | yes | Task 3 `:63` checks "equal to the digest section"; Tasks 4 and 5 (`:78`, `:90`) check only "exactly one digest"; `:125` omits `test_review_severity_registry.py`, last run at stage 1 `:213` "with all `digest` rows at `legacy`" |
| U-005 | V2 | minor | yes | `source.md:20` versus `PLAN:22` |
| U-006 | V2 | minor | yes | `test_review_severity_rule.py:181-192`: 10 files, 8 untouched in stage 3 |
| U-007 | V1 (same as X-001) | minor | merge with X-001 | as X-001 |

## Strengths claimed

- **U-003 (M12 baseline):** this is the prior review's F8 still unresolved. Without a stage 2 count, "flat counts falsify the pilot" cannot be judged at the stage 4 go.
- **U-004 (digest check):** the spec's T1 digest-equality test never runs on the first v2 rows, so a mistyped digest in `rf-qa.md` would ship into the live pilot.
- **C-001:** variant 2 traces the defect to its root, the plan merging two separate source conditions. Its fix (rerun `shadow_summary.py` into this package before spawning) also covers C-007 and X-002.
- **Line checks:** the "Checked and sound" section confirms each line it cites and records which prior-review items are closed.

## Weaknesses found in variant 1 (verified)

- It misses U-003, U-004, U-005 and U-006.
- It grades F5 (C-004) blocking without weighing `PLAN:19`.
- "The Constraints explicitly prohibit starting" overstates the case. `PLAN:20` names Task 1's acceptance lines as the mechanism, and those run after the spawn.
- The "Drift" label on all 8 findings misapplies the deviation taxonomy to a plan that has not been executed.
- F2's fix does not move the entry check ahead of the spawn.

## Concessions

- Variant 2 missed U-001, the highest-severity point. Its F4 used the same hook fact but drew only the confound conclusion from it.
- F3 (C-004) is overgraded; it should be minor.
- F9 is weak. `PLAN:59` requires only running the tests, and Task 4 runs none, so "Tasks 3 and 4" is wrong.
- F2's "halts by construction" holds only when the planted set cannot reach about 83 to 140 defects. Stage 0 itself predicts that outcome, but it is not certain.
- The calibrator's lower confidence on F6 is fair. It is blocking because a check is missing, not because a failure was observed.

## Shared assumptions

- **A-001: QUALIFY.** Acceptance lines are checked after the task body, but a failure goes first to a repair pass and the retry ladder, and the run halts only when "a repair could not close" it (`qa.md:280`). This strengthens C-001: the repair pass will try to make the stale summary pass.
- **A-002: ACCEPT.** Verified at `pragmatic-subagent.js:7-15` and `Makefile:109-158`. The refresh can be `superclaude update` or an install with `--force` (spec `:761`).
- **A-003: QUALIFY.** The cross-package findings are about whether the plan texts agree with each other as written, and they stand on that basis. But stage 0 is marked NEEDS-REVISION (`README.md:17`), so file names may change. A merged card should cite each finding as true of the current plan text.
- **A-004: QUALIFY.** A halt is blocking when the check fails whatever the true evidence is (C-001's stale summary; C-003 whenever the advisory fallback happens). A halt that fires only on genuinely bad evidence is the designed safe outcome and not a finding. C-004 does not depend on this assumption.

I did not open `artifacts/reviewer-calibration.yaml` or the earlier review the cards refer to.
