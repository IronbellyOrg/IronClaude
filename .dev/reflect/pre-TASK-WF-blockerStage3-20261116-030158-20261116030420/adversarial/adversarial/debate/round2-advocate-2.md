# Round 2: advocate for variant 2 (reviewer 2 card), model class opus, agent a79163e48e38918a5

(Persisted verbatim by the orchestrator from the agent's final message; hand-back frame indentation removed. The advocate wrote no file.)

# Round 2 rebuttal: advocate for variant 2 (reviewer 2 card)

## 1. Steelman, and my verdict on advocate 1's merged list

Advocate 1's strongest point: a check that is weak or under-specified is not the same as a check that cannot be met. That point correctly lowered C-006, U-006 and C-004 to minor, and I accept it.

I accept these entries as written: C-001, C-002, C-004, C-005, C-006, U-005, U-006, and the fold of C-007 and X-002 into C-001.

- C-003: I accept the narrowing. PLAN:33 does give a computable rule ("safety recall equals the old rule's; ... within 5 points"), so my interval and tolerance demand is withdrawn. What remains is the advisory outcome. Stage 0 :110 allows a class to "mark that class's pass line advisory", but PLAN:62 requires "pass on all three". The matched-reviewer point from my F2 moves into C-002.
- U-003: I dispute only its scope. My F5 also named M10b, and the merged list dropped it. Spec :972 gives M10b's baseline as "stage 3", so this package has to produce that number, and no task does.

## 2. The three grades that matter most

**(a) U-001 is blocking, but the fix should be narrowed.**
- Spec REQ-26 3 (:762) says a switch is "(a) in the repository ... re-run the drift tests; (b) ship a release ...; (c) refresh each machine ..., confirmed by the install check."
- Steps (b) and (c) can fairly belong to the owner or operator rather than the package. But the plan never names them. A search of PLAN for `superclaude update`, `--force`, `doctor`, `release` and `drift test` finds nothing.
- PLAN:162 does cover the three-step revert, but nothing covers the three-step switch.
- PLAN:158 tells the owner only that the audit window "is observed by the owner or operator".
- The hook reads only `~/.claude` (`pragmatic-subagent.js:7`, `os.homedir(), '.claude', 'output-styles'`), and `Makefile:108` reads "Sync src/superclaude/{skills,agents} → .claude/".
- What the owner would lack: the knowledge that the pilot is not live on any machine until (b) and (c) are done. Without that, the audit window behind the stage 4 go would measure the old injected rule mixed with the new digests. That is a wrong result.
- The stage 1 plan already builds the needed check (Task 14, `make doctor` digest-version check, stage 1 :193), and stage 3 never calls it.

**(b) U-002: the sentence is false, not just imprecise.**
- RT1 (:985) covers "Any safety-class escape in ... the seeded set", and Task 1 holds that data: PLAN:33 says "Score each planted defect as found or missed and as blocking or not".
- RT3 (:987) is the same test as Task 3's gate, so it has already been judged by the time Task 11 runs.
- New point: the Task 3 gate "equals the old rule's" is weaker than RT1's "any" escape. If the old rule also lets one safety defect escape, Task 3 passes while RT1 has already tripped. PLAN:162 would then tell the owner the trigger "can[not] be judged".
- The plan also contradicts itself: PLAN:158 asks for the triggers "with their current state".
- Blocking.

**(c) Both U-003 and U-004 are missing results or checks, not weaker checks.**
- U-003: PLAN:161 only requires that the summary "quotes RT1, RT2 and M12". Stage 2 :110 lists its exit numbers without any rf-qa FAIL count, and README:25 requires the summary to hold "the numbers the owner needs for the next go". The baseline number is therefore produced by nobody. Blocking.
- U-004: Task 3 checks digest equality for pragmatic (PLAN:63, "equal to the digest section"). Tasks 4 and 5 only check "exactly one digest" (PLAN:78, :90), and the PLAN:125 list leaves out `test_review_severity_registry.py`, which stage 1 :213 last ran "with all `digest` rows at `legacy`".
- REQ-26 3(a) requires "re-run the drift tests", so a required check is missing. One honest caveat: Task 8's re-pinned bullet tests and the full CI suite may catch some of the same drift. Blocking, narrowed to "required check missing".

## 3. Errors on the facts, and anything the merged list missed

- My card has two errors, both already conceded. F1's "before any run has happened" is too strong (stage 2 :110 says "zero runs is a valid and stated result"), and F9's "Tasks 3 and 4" is wrong, because Task 4 runs no tests.
- Advocate 1's round 1 called the Constraints an "explicit prohibit[ion]". PLAN:20 does say "It runs only when all of these hold" but hands the mechanism to "(Task 1 checks them)", and that ordering is now settled inside C-001.
- I re-checked these cites and they hold: stage 0 :37, :76, :106 and :110; spec :680; README:17; Makefile:109-158; hook :7 and :15.
- Coverage of the T1 observations: O1 to O7 are all covered (O1 by C-001, O2 by C-004, O3 by C-002, O4 by C-003, O5 by C-001, O6 by C-005, O7 by C-006), and O8 reports sound grounding.
- What the merged list misses: M10b (added to U-003), and the RT1-versus-Task-3 gap (added to U-002).

## 4. Shared assumptions

- **A-001, qualify.** README:3 says `/sc:implement` "cannot pause for an owner go", and a failed check goes to a repair pass before any halt. That repair attempt is exactly why the stale summary in C-001 is dangerous.
- **A-002, accept the hook behaviour; the installed file's contents are unverified.** Stage 0 :76 itself names the "old-rule injection confound".
- **A-003, qualify.** These findings are true of the current plan texts. Stage 0 is NEEDS-REVISION (README:17), so its file names may change.
- **A-004, reject the blanket form.** A halt is blocking only when it fires regardless of the true evidence: C-001 when the summary is stale, and C-003 when an advisory pass line is allowed.

## 5. Final merged finding list

| id | title | grade | survive | merged from | fix |
|---|---|---|---|---|---|
| C-001 | Stale stage 2 summary gate; entry checks not run before the spawn | blocking | yes | V1 F2, V2 F1, C-007, X-002 | First step: run stage 2's `shadow_summary.py` over the run folders into `./artifacts/`, then check all entry conditions before any spawn; never edit stage 2 files |
| C-002 | Old rule injected into the new-rule pass; reviewer setups not matched | blocking | yes | V1 F3, V2 F4, V2 F2 (part) | Same model class and brief in both passes; override or disclose the injected rule in the result file |
| C-003 | An advisory pass line has no defined outcome at Task 3 | blocking | yes | V1 F4, V2 F2 (narrowed) | Say how an advisory line is treated and what recorded owner ruling lets the run continue |
| C-004 | Inventory path points into this package | minor | yes | V1 F5, V2 F3 | Read the file from the stage 0 package by package id |
| C-005 | Stale numbers "Tasks 34 to 37" and `t38` | minor | yes | V1 F8, V2 F10 | Change to Tasks 4 to 7; renaming the artifact is optional |
| C-006 | Registry grep searches the wrong text | minor | yes | V1 F7, V2 F11 | Grep for `skills/task/SKILL.md` |
| U-001 | Switch steps (b) and (c) and the install check are never named | blocking | yes | V1 F1 | Task 11 names the release, refresh and `make doctor` check as owner steps that come before the audit window |
| U-002 | Summary falsely defers every trigger; RT1 seeded-set part not checked | blocking | yes | V1 F6, plus this round | Judge RT1's seeded part and RT3 from Task 1's result; mark only RT2 as pending |
| U-003 | M12 stage 2 baseline and M10b stage 3 baseline missing | blocking | yes | V2 F5 | Task 11 counts rf-qa FAILs from the stage 2 runs, or states the source; Task 11 measures M10b |
| U-004 | Registry drift test (T1) never re-run at the switch | blocking | yes | V2 F6 | Add `test_review_severity_registry.py` to the PLAN:125 test list |
| U-005 | Ban on stage 4 edits left out of the plan | minor | yes | V2 F7 | Add the `source.md:20` ban to the Constraints |
| U-006 | Pins for the 8 legacy rows not specified | minor | yes | V2 F8 | Legacy rows keep their frozen legacy expectations |
| X-001/U-007 | Expected test failures in Task 3 not stated | minor | no | V2 F9 | None |
| S-001 | Card format | minor | no | none | None |

I did not check the installed `~/.claude` bytes or whether CI runs the registry test.
