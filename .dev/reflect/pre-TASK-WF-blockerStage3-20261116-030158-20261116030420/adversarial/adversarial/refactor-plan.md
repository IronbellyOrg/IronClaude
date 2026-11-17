# Refactoring plan (step 4): merge two reviewer cards into one review card

## Overview

- Base variant: variant-2-original.md (reviewer 2, qa persona, opus class). Selected in `base-selection.md` (combined scores 0.893 vs 0.8875, inside the 5 percent band, tiebreak on debate points 6 to 4).
- Incorporated: variant-1-original.md (reviewer 1, analyzer, haiku class), the debate (round 1 and round 2 of both advocates), and the invariant probe (`invariant-probe.md`).
- Output: `<run>/adversarial/merged-review-card.md`, one card of 15 findings: 7 blocking (F1 to F7), 8 non-blocking (F8 to F15).
- Risk: Low (a text merge; every citation below was re-read against the live files by the orchestrator before it was written here: 92 of 92 citations matched).
- Aliases used in citations (declare them in an HTML comment at the top of the card): PLAN = `.dev/tasks/to-do/TASK-WF-blockerStage3-20261116-030158/TASK-WF-blockerStage3-20261116-030158.md`; SRC = `.dev/tasks/to-do/TASK-WF-blockerStage3-20261116-030158/source.md`; S0 = `.dev/tasks/to-do/TASK-WF-blockerStage0-20261116-021044/TASK-WF-blockerStage0-20261116-021044.md`; S1 = `.dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/TASK-WF-blockerStage1-20261116-030154.md`; S2 = `.dev/tasks/to-do/TASK-WF-blockerStage2-20261116-030156/TASK-WF-blockerStage2-20261116-030156.md`; SPEC = `.dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/02-brainstorm/merged-requirements.md`; README = `.dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/stage-requests/README.md`. All other paths are repo-relative.

## Planned Changes

Format of each finding in the merged card (same as the prior reflect cards): `F<n> | severity <MAJOR|MINOR> | blocking <true|false> | <category> | <claim> | citations:` followed by one bullet per citation `- <path>:<line> "<verbatim quote>"`. Copy every citation string exactly as written below (each quote is a verbatim substring of the cited line). Keep the claim text as written, in plain English, without new facts.

### Change 1: F1 (base: reviewer-2 F1; incorporated: reviewer-1 F2; debate C-001, C-007, X-002; probe INV-001, INV-002)
severity MAJOR | blocking true | category unpassable-check
Claim: Task 1's entry check on the shadow runs cannot be met from the file it names, and the entry checks run after the six-agent spawn. PLAN:37 requires the stage 2 summary to state at least 5 observed shadow runs with zero safety misses and no capture failure. The stage 2 plan has that summary state "the number of shadow runs observed so far (zero is allowed)" and writes it at the end of its own package (S2:114). source.md:3 lists "exists and the owner has read it" and "at least 5 shadow runs have been observed" as two separate conditions; the plan merged them into one file check. No task produces a summary that shows 5 runs (stage 2's `shadow_summary.py` could, but nothing here runs it), and "Task 1 checks them" (PLAN:20) points to acceptance lines that run after the body has spawned the reviewers (PLAN:33). The owner's go (PLAN:36) has to follow the owner reading the regenerated summary, so regenerating it inside this package after the go is too late. A fix pass must also not edit the stage 2 summary, the result file or the ledger row to make a check pass: refs/qa.md stops an "executor-invented approval" but names no rewrite of a result file. "Cannot exist by construction" is too strong, because 5 runs may exist when the summary is rewritten. Fix: regenerate a dated summary from the shadow-run folders before the owner reads it and says go, name that file in the ledger row, have Task 1 read it, run every entry check before the first spawn, and add a halt clause for a missing or short count.
Citations:
- PLAN:20 "(Task 1 checks them)"
- PLAN:33 "Spawn three reviewer agents for each pass"
- PLAN:36 "has an owner go for stage 3 with a date"
- PLAN:37 "states at least 5 observed shadow runs with zero safety misses and no capture failure"
- S2:114 "states the number of shadow runs observed so far (zero is allowed)"
- SRC:3 "exists and the owner has read it"
- SRC:3 "at least 5 shadow runs have been observed with zero safety misses"
- src/superclaude/skills/sc-implement-protocol/refs/qa.md:249 "executor-invented approval"
- src/superclaude/skills/sc-implement-protocol/SKILL.md:145 "exactly one fix pass"

### Change 2: F2 (base: reviewer-2 F4; incorporated: reviewer-1 F3; reviewer-2 F2 part; debate C-002)
severity MAJOR | blocking true | category other
Claim: The seeded-recall measurement that gates the rule switch carries the old rule in both passes. The hook registered at hooks.json:173 runs `pragmatic-subagent.js`, which reads `~/.claude/output-styles/pragmatic.md` (the old text today) and injects it into every subagent (:7, :15). A reviewer in the "new rule text" pass therefore holds the old three definition bullets from the hook and the digest from its brief. The stage 0 plan names this confound for its own re-grade (S0:76); Task 1 neither controls it nor requires the result file to report it. Task 1 also does not say that both passes use the same reviewer configuration (same model class and brief), while spec 8.3 says "with the same reviewers" (SPEC:680). Fix: state how the injected rule is handled in the new-rule pass (for example a brief that names the digest as the rule in force), keep model class and brief identical across the passes, and require the result file to record which rule text each reviewer reported applying and the remaining confound.
Citations:
- src/superclaude/hooks/hooks.json:173 "pragmatic-subagent.js"
- src/superclaude/hooks/scripts/pragmatic-subagent.js:7 "path.join(os.homedir(), '.claude', 'output-styles', 'pragmatic.md')"
- src/superclaude/hooks/scripts/pragmatic-subagent.js:15 "PRAGMATIC MODE ACTIVE"
- S0:76 "states the old-rule injection confound"
- PLAN:33 "once with today's rule text"
- SPEC:680 "with the same reviewers"

### Change 3: F3 (base: reviewer-2 F2; incorporated: reviewer-1 F4; debate C-003; probe INV-003, INV-012)
severity MAJOR | blocking true | category unpassable-check
Claim: Task 3's gate can never read "pass" in the cases the stage 0 plan itself expects. PLAN:62 requires pass on all three requirements. Stage 0 lets a class's pass line be marked advisory (S0:110) and says the advisory fallback is the expected outcome (S0:106). "The cosmetic block share falls" (PLAN:33) cannot hold when the old rule blocks no cosmetic defect at all. The plan also does not say what counts as "found" when three reviewers see the same defects (any reviewer, a majority, or each), and three reviewers on one set are not independent trials. A run on an underpowered set therefore halts by construction or passes on noise, and the executor has to invent the rule. The computable rule exists (equality, within 5 points, the share falls); what is missing is the outcome for an advisory class, a zero base and a small n, and the recorded owner ruling that lets the run continue (dated after the result file and citing its hash, so that a fix pass cannot edit its way to a pass). Fix: add that outcome table to Task 1 and the matching line to Task 3's acceptance.
Citations:
- PLAN:62 "shows pass on all three requirements"
- S0:110 "marks that class's pass line advisory"
- S0:106 "the advisory fallback is the expected outcome"
- PLAN:33 "the cosmetic block share falls"
- SPEC:680 "with the same reviewers"

### Change 4: F4 (base: none (new from reviewer-1 F1, narrowed by debate U-001 and round 2 of both advocates); probe INV-006, INV-014)
severity MAJOR | blocking true | category missing-requirement
Claim: The plan never says that the pilot is not live until the switch steps after the repository edit are done. The hook reads only the installed `~/.claude/output-styles/pragmatic.md`; `make sync-dev` is described as syncing skills and agents into the project `.claude/` and does nothing for output styles (Makefile:108-109); an installed output style is kept stale without `force` (SPEC:756). Spec REQ-26 makes a stage switch three steps: edit and re-run the drift tests, ship a release that names the refresh command, and refresh each machine, confirmed by the install check (SPEC:762). Task 3 names only `make sync-dev` (PLAN:59), and Task 11 states only the revert command per carrier row (PLAN:162), which also leaves out the edits that have no registry row (rf-analyst, the task skill's L1 to L3 text, and `promote` on). Until steps (b) and (c) happen, the QA of Tasks 4 to 11 runs under the new rf-qa digest plus the old injected style, the mixed-version blend the spec calls RK15, and the audit window behind the stage 4 go would measure that blend. REQ-26 puts steps (b) and (c) with the owner or operator, so this is a gap in what the plan states and checks, not a missing code edit. Fix: Task 11 names the release, the refresh command and the install check as steps that come before the audit window, says that the per-row revert covers digest rows only and how the other edits are reverted, and Task 3 gets a check that the installed style carries the digest before the audit window is called started.
Citations:
- src/superclaude/hooks/scripts/pragmatic-subagent.js:7 "path.join(os.homedir(), '.claude', 'output-styles', 'pragmatic.md')"
- Makefile:108 "Sync"
- Makefile:109 "sync-dev:"
- SPEC:756 "including an output style, is kept and listed as stale without `force`"
- SPEC:762 "(c) refresh each machine"
- PLAN:59 "Run `make sync-dev` and then the existing tests that Task 8 re-pins."
- PLAN:162 "that no revert trigger can be judged until the audit window has run"

### Change 5: F5 (base: reviewer-2 F6; debate U-004; probe INV-004, INV-010)
severity MAJOR | blocking true | category missing-requirement
Claim: A drift check the spec requires at a switch is missing from the pilot. The stage 1 plan builds `tests/skills/test_review_severity_registry.py`, whose T1 requires every `digest` row to hold exactly one digest equal to the digest section of `refs/rule.md` (S1:209). Task 8's pytest list does not include it (PLAN:125). Tasks 4 and 5 set the registry row to `v2` (PLAN:73, PLAN:85) but their acceptance lines check only "exactly one digest" (PLAN:78, PLAN:90) and none says that the row reads `v2`, so a forgotten flip passes silently because that test accepts a `legacy` row. Task 1 also tests "the digest of spec section 4.1" (PLAN:33) while Task 3 ships the digest section of `refs/rule.md` (PLAN:63), with no check that the two are equal. A mistyped digest in `rf-qa.md` or `rf-qa-qualitative.md` would ship into the pilot. Spec REQ-26 requires re-running the drift tests at a switch (SPEC:762). Fix: add the registry test to Task 8's list, add a "row reads v2" acceptance line to Tasks 4 and 5, and require that the digest Task 1 tests is the digest Task 3 ships.
Citations:
- PLAN:125 "uv run pytest tests/skills/test_review_severity_rule.py"
- S1:209 "exactly one digest whose flattened body equals the digest section of `refs/rule.md`"
- PLAN:73 "Set the registry row to `v2`."
- PLAN:85 "Update the registry row to `v2`."
- PLAN:78 "the file holds exactly one digest"
- PLAN:90 "The file holds exactly one digest"
- PLAN:63 "equal to the digest section of the skill's `refs/rule.md`"
- PLAN:33 "the digest of spec section 4.1"
- SPEC:762 "re-run the drift tests"

### Change 6: F6 (base: none (new from reviewer-1 F6; debate U-002, strengthened by advocate 2 round 2))
severity MAJOR | blocking true | category contradiction
Claim: Task 11 must tell the owner something false about the revert triggers. PLAN:162 requires the summary to state "that no revert trigger can be judged until the audit window has run". But RT1 covers "any safety-class escape in the audit or the seeded set" (SPEC:985) and RT3 is seeded recall falling more than 5 points below the old rule (SPEC:987); Task 1 produces the seeded-set result before the window, so both can already be judged from it. PLAN:158 itself asks for the triggers "with their current state", so the plan contradicts itself. The Task 3 gate (safety recall "equals the old rule's") is also weaker than RT1's "any", so the gate can pass while RT1 has tripped. Fix: Task 11 judges RT1's seeded part and RT3 from the Task 1 result and marks only the window-dependent parts (RT1's audit part and RT2) as pending.
Citations:
- PLAN:162 "that no revert trigger can be judged until the audit window has run"
- PLAN:158 "the revert triggers RT1 and RT2 in section 13.2 with their current state"
- SPEC:985 "Any safety-class escape in the audit or the seeded set"
- SPEC:987 "Seeded recall of decision-bearing or missing items falls more than 5 points below the old rule"

### Change 7: F7 (base: reviewer-2 F5; debate U-003; probe INV-013)
severity MAJOR | blocking true | category missing-requirement
Claim: Task 11 gives the owner the names of the audit-window measures but not the baselines they are read against. M12 ("flat counts falsify the pilot") has the baseline source "stage 2" (SPEC:974), but the stage 2 summary lists its exit numbers without any rf-qa FAIL count (S2:110), and Task 11 only "quotes RT1, RT2 and M12 from the spec" (PLAN:161). The same holds for M10b, whose baseline is stage 3 (SPEC:972), and for the M1 baseline that RT5 needs (SPEC:962, SPEC:989). The prior review's F8 (the owner has no numbers to read at the gate) is therefore only half closed; the stage ledger README requires each package's owner summary to hold the numbers the owner needs for the next go (README:25). Fix: Task 11 names where each baseline comes from (for example the rf-qa FAIL counts of the stage 2 shadow-run folders) and counts them, or states that none exists.
Citations:
- SPEC:974 "flat counts falsify the pilot"
- PLAN:161 "quotes RT1, RT2 and M12 from the spec"
- S2:110 "offers made and answered, the shadow agreement figures"
- SPEC:972 "M10b"
- SPEC:962 "stage 2 paired data"
- SPEC:989 "After 5 runs under stage 3, M1 is not at least 25 percent lower than stage 2"
- README:25 "Each package ends with an owner summary file"

### Change 8: F8 (base: reviewer-2 F3; incorporated: reviewer-1 F5; debate C-004, graded minor)
severity MINOR | blocking false | category other
Claim: Tasks 4 and 5 read the frozen FAIL-trigger inventory from `./artifacts/stage0-inventory-freeze.md`, which in this package is this package's own folder; the stage 0 plan writes the file (S0:37). Task 1 says "read by package id" for the stage 0 files; Tasks 4 and 5 do not, and Task 4's acceptance ("the frozen inventory for `rf-qa.md`") has no input file as written. The Constraints say earlier-stage evidence is read by package id (PLAN:19), so an executor can recover; graded minor. Fix: name the stage 0 package id and the path in both tasks.
Citations:
- PLAN:73 "./artifacts/stage0-inventory-freeze.md"
- PLAN:85 "./artifacts/stage0-inventory-freeze.md"
- S0:37 "./artifacts/stage0-inventory-freeze.md"
- PLAN:19 "Evidence of earlier stages is read from their packages by package id"
- PLAN:77 "frozen inventory for `rf-qa.md`"

### Change 9: F9 (base: reviewer-2 F10; incorporated: reviewer-1 F8; debate C-005)
severity MINOR | blocking false | category other
Claim: Stale numbering from the base plan. Task 10's first acceptance line says the scan passes "after Tasks 34 to 37", but this package has 11 tasks and Task 10 depends on Tasks 4 to 7. Task 8 names `./artifacts/t38-fixture-diff.md`, an old task number. Fix: "Tasks 4 to 7"; rename the artifact.
Citations:
- PLAN:147 "after Tasks 34 to 37"
- PLAN:142 "Depends on: Task 4, Task 5, Task 6, Task 7"
- PLAN:126 "./artifacts/t38-fixture-diff.md"

### Change 10: F10 (base: reviewer-2 F11; incorporated: reviewer-1 F7; debate C-006, graded minor)
severity MINOR | blocking false | category unpassable-check
Claim: Task 7's registry check cannot show whether a `skills/task/SKILL.md` row exists. The pattern `sc-review-severity` matches the skill folder name in the paths of other rows, so the output is the same with or without that row, although the task states the skill gets no registry row. Fix: grep for `skills/task/SKILL.md`.
Citations:
- PLAN:116 `grep -n "sc-review-severity" src/superclaude/skills/sc-review-severity/refs/registry.yaml`
- PLAN:110 "The skill gets no registry row"

### Change 11: F11 (base: reviewer-2 F7; debate U-005)
severity MINOR | blocking false | category missing-requirement
Claim: The source's third "not to be done" item, no template, rule-prompt, builder, researcher or spec-panel edit (stage 4), is not in the plan's Constraints. The "Not built here" bullet lists the Jev, `qa.md`, own-scale, cli code, 35 percent target and cap items only, so the executor's QA has no stated rule to flag such an edit. Fix: add it to the Constraints.
Citations:
- SRC:20 "No template, rule-prompt, builder, researcher or spec-panel edit (stage 4)."
- PLAN:22 "Not built here:"

### Change 12: F12 (base: reviewer-2 F8; debate U-006, graded minor after round 2; probe INV-005)
severity MINOR | blocking false | category other
Claim: Task 8 does not say what the eight legacy files stay pinned to. `canonical_rule_bullets()` reads the old bullets from `pragmatic.md` and `S1_S3_FILES` lists ten files checked against them; Task 8 makes the reader use the v2 digest and the list registry rows, while eight of the ten files (templates and rule prompts) keep the old text until stage 4, and the plan forbids dropping a pin. An executor can dispatch by registry state (v2 rows against the digest, legacy rows against a frozen copy of the old text), but the plan does not say so. Fix: state it.
Citations:
- tests/skills/test_review_severity_rule.py:79 "def canonical_rule_bullets()"
- tests/skills/test_review_severity_rule.py:181 "S1_S3_FILES = ("
- tests/skills/test_review_severity_rule.py:193 "S5_FILES = S1_S3_FILES[:6]"
- PLAN:122 "`S1_S3_FILES` and its `[:6]` slice `S5_FILES` become registry rows of kind `digest`"
- PLAN:127 "No pinning test is deleted wholesale"

### Change 13: F13 (new from probe INV-007; follow-up candidate)
severity MINOR | blocking false | category missing-requirement
Claim: The spec lists `agents/rf-qa-qualitative.md` lines 110, 809 and 994 for the cap and fix-step (L2) edits (SPEC:866); Task 5 edits none of them, and only `rf-qa.md` gets the L2 checks and the L3 choices (PLAN:73). Lines 809 and 994 hold the cap sentence. Line 994 sits in the `## Critical Rules` block whose hash Task 9 re-pins, so the choice has to be made before the hash is pinned. Carried over unchanged from the base plan (the request reuses its tasks). Real but not blocking; a follow-up candidate. Fix: decide whether Task 5 applies the L2 and cap wording to those lines.
Citations:
- SPEC:866 "`agents/rf-qa-qualitative.md` 110, 809, 994"
- src/superclaude/agents/rf-qa-qualitative.md:809 "After 2 fix cycles"
- src/superclaude/agents/rf-qa-qualitative.md:994 "After 2 fix cycles"
- PLAN:85 "Edit `src/superclaude/agents/rf-qa-qualitative.md`: replace S1, S2 and S5"

### Change 14: F14 (new from probe INV-008; follow-up candidate)
severity MINOR | blocking false | category missing-requirement
Claim: Task 2 creates `fixcheck.py` and its test only, with no subcommand or other entry point, but Tasks 4 and 7 tell the fix agent to run the L2 checks before handing back. The Fix Cycle text therefore has nothing to call. Fix: add an entry point to Task 2 or say how the text invokes the module.
Citations:
- PLAN:45 "Create `src/superclaude/cli/review/fixcheck.py` for L2"
- PLAN:73 "add the L2 pre-handback checks to the Fix Cycle section"
- PLAN:110 "the Fix Agent step requires the L2 mechanical checks before handing back"

### Change 15: F15 (new from probe INV-009; follow-up candidate)
severity MINOR | blocking false | category other
Claim: Task 4 rewrites the Fix Cycle text of `rf-qa.md` near line 402, where "Retry Monotonicity Protocol" and `INV-012` sit, and `tests/skills/test_task_builder_merge.py` pins those tokens in `rf-qa.md`; neither Task 8's list nor Task 9 (`tests/audit`) runs that file, so an edit that drops the tokens passes the plan's checks. Fix: add that file to Task 8's re-run list.
Citations:
- PLAN:73 "Fix Cycle bullet near line 402"
- src/superclaude/agents/rf-qa.md:403 "Retry Monotonicity"
- src/superclaude/agents/rf-qa.md:416 "INV-012"
- tests/skills/test_task_builder_merge.py:436 `assert "Retry Monotonicity Protocol" in rf_qa_text`
- tests/skills/test_task_builder_merge.py:439 `assert "INV-012" in rf_qa_text`

## Changes NOT Being Made (considered and rejected)

- Reviewer 1's "Drift" category label on every finding: the 4-class taxonomy is for UC-2 deviations; the findings-v2 categories are used instead.
- S-001 (card shape): not a plan defect.
- X-001 / U-007 (reviewer 2 F9, Task 3 runs tests that fail until Task 8): dropped; Task 3 asks only to run them, its pass check is the brief-rests-on test (PLAN:59 and the acceptance line that follows it), and Task 4 runs no tests. The wording "Tasks 3 and 4" was wrong.
- Reviewer 2 F2's interval-overlap and tolerance demand: withdrawn in round 2 (PLAN:33 already gives a computable rule); the useful part moved to F2 (same reviewers) and F3 (advisory, zero base).
- Reviewer 1 F5 and reviewer 2 F3 as blocking: graded minor (F8) because PLAN:19 makes the path recoverable.
- Probe INV-011 (answer key), INV-016 (allow-list read), INV-017 (owner decides after the go): not carried; PLAN:40 already requires that the answer key is not among the files given, and the go-before-result order is the source's own (SRC:3).
- Reviewer 1's "T1 card O5 is wrong" claim and the reviewer 2 disagreement on package ids: no finding; PLAN:20 and README:17 already settle them (the ordering point lives in F1).

## Risk Summary

Low. Each change is an addition to or rewording of a finding; no finding was invented by the merge; each probe item carried into the card was re-read by the orchestrator first (`invariant-probe.md`, last column).

## Review Status

Auto-approved (non-interactive).
