# Reflect REPORT: pre-execution audit of the pr-submit merge guard plan (UC-1, Tier 2, shadow engine)

```yaml
contract_version: 1.8.0
status: success
mode: pre
tier_reached: 2
confidence_calibrated: 0.65
citations_total: 111
citations_revalidated: 111
citations_dropped: 0
citations_inferred: 0
citation_budget_policy: full_reread
coverage_degraded: parsed-sparse
```

Spec: `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md` (378 lines). Plan: `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md` (200 lines, 13 tasks).
Run: `pre-TASK-WF-designSpec-20261107-075614-comboD-r3` (model combination D: orchestrator Sonnet class `claude-gw-tier1b`, reviewers Sonnet / Haiku / GPT 6 Luna).

> Zero-drop flag: the evidence validator dropped 0 of 111 citations. Per the protocol a clean pass on a report this size is an audit flag, not proof; the validator's two partial-support caveats are listed under Grounding notes.

## Verdict

- The plan covers the spec. No finding is blocking: 17 merged findings, 0 blocking, 2 MAJOR non-blocking (M-15, M-16), 15 MINOR.
- The two MAJOR items are specification gaps the plan inherits: nothing says where the per-cycle edit count for the release decision comes from, and the fold's `cycle_id` update rule is never stated.
- Both reviewer-raised blockers were downgraded in debate: the Wave 0 bullet test wording (plan 137-140) and the cycle-id minting overlap (plan 124, 150). All three advocates ended at MINOR after reading the lines.
- Debate convergence 1.00 (17 of 17 diff points agreed), invariant probe found no HIGH item.

## Coverage (UC-1)

- Pass 1 found 0 labelled requirement IDs; Pass 2 extracted 62 quote-pinned requirement rows. `coverage_pct` is null (no parsed IDs); `coverage_pct_union` = 0.7742; `S_dev_density` = 0.2258; `coverage_degraded` = parsed-sparse, so Tier 1 could not stop.
- Lexically unmapped rows (14): INF-005, INF-014, INF-018, INF-024, INF-028, INF-030, INF-036, INF-039, INF-040, INF-041, INF-046, INF-051, INF-057, INF-059. Lexical containment is weak evidence; the reviewers' semantic checks (rows observed 20, 23 and 18 of their assigned 20, 24 and 18) replace it for the findings below.
- Tasks by lexical hits: Task 1 5, Task 2 2, Task 3 10, Task 4 7, Task 5 0, Task 6 1, Task 7 2, Task 8 13, Task 9 4, Task 10 0, Task 11 3, Task 12 1, Task 13 0.

## Merged findings

Each finding below is one line of the merged findings block (`adversarial/adversarial/merged-output.md`); all quotes were re-read inside their cited line ranges by the evidence validator.

### Finding M-01 [MINOR]: Task 9 asks for a Wave 0 bullet that carries no L3 or draft condition yet must say it prints the off line at L

- **Category:** contradiction. **Rows:** INF-006, INF-007
- **Claim:** Task 9 asks for a Wave 0 bullet that carries no L3 or draft condition yet must say it prints the off line at L3 with no draft call. A substring test for L3 or draft fails; the test must target gating wording only. Spec 59 and 241 carry the same tension.
- **Evidence (plan):** `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md:137-137` "carries no L3 or `draft` condition"
- **Evidence (plan):** `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md:140-140` "when it names an L3 or `draft` condition"
- **Evidence (spec):** `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md:241-241` "contains no L3 or `draft` condition"
- **Evidence (spec):** `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md:59-59` "`--merge-guard off` at L3"

### Finding M-02 [MINOR]: Task 8 and Task 10 both direct that the cycle id is minted; Task 10's criteria do not require its bullet to na

- **Category:** missing-requirement. **Rows:** INF-046, INF-049
- **Claim:** Task 8 and Task 10 both direct that the cycle id is minted; Task 10's criteria do not require its bullet to name the single place Task 1 O1 finds, and no criterion checks that the guard, the push triad and rereview_requested share one cycle_id (the acceptance trace checks order only).
- **Evidence (plan):** `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md:124-124` "in the single place named by Task 1 O1"
- **Evidence (plan):** `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md:150-150` "and mints the cycle id"
- **Evidence (plan):** `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md:170-170` "The acceptance-trace test asserts the exact event order"
- **Evidence (spec):** `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md:251-251` "uses the same id as the `cycle_id` of the push triad"

### Finding M-03 [MINOR]: Spec 240 says the ref carries the procedure of sections 3 and 4

- **Category:** missing-requirement. **Rows:** INF-021, INF-034
- **Claim:** Spec 240 says the ref carries the procedure of sections 3 and 4.1 to 4.4, but Task 8 lists sections 3, 4.1, 4.5, 4.6 and 5. The event payload fields and the idempotency_key format of 4.2 and the script contract of 4.4 never reach the ref, so the SKILL writer and the fold could disagree.
- **Evidence (plan):** `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md:124-124` "from ./source.md sections 3, 4.1, 4.5, 4.6 and 5"
- **Evidence (spec):** `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md:240-240` "The procedure of sections 3 and 4.1 to 4.4"
- **Evidence (spec):** `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md:182-185`

### Finding M-04 [MINOR]: The ENGAGE decision must carry auto_merge_armed in notes, but Task 4 asserts only action, reason and cause, an

- **Category:** missing-requirement. **Rows:** none
- **Claim:** The ENGAGE decision must carry auto_merge_armed in notes, but Task 4 asserts only action, reason and cause, and no task has the ref surface it, although converting to draft disarms an armed auto-merge.
- **Evidence (spec):** `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md:143-143` "`notes` carries `auto_merge_armed` when set"
- **Evidence (plan):** `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md:73-73` "asserts the returned `action`, `reason` and `cause`"
- **Evidence (spec):** `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md:333-333` "converting disarms an armed auto-merge"

### Finding M-05 [MINOR]: Spec says a first skip also sets original_is_draft and Task 3 repeats it, but the fold criterion checks only d

- **Category:** missing-requirement. **Rows:** INF-010
- **Claim:** Spec says a first skip also sets original_is_draft and Task 3 repeats it, but the fold criterion checks only disabled_cause for the already_draft skip, so a fold that drops original_is_draft still passes.
- **Evidence (spec):** `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md:200-200` "a first skip also sets `original_is_draft`"
- **Evidence (plan):** `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md:60-60` "settled(draft, skipped, already_draft)` gives `DISABLED`"
- **Evidence (plan):** `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md:56-56` "taken only from the first guard record or a first skip"

### Finding M-06 [MINOR]: The release-failure path (one retry, already in target state counts as confirmed, release_pending) has no beha

- **Category:** missing-requirement. **Rows:** none
- **Claim:** The release-failure path (one retry, already in target state counts as confirmed, release_pending) has no behavioural criterion: Task 8 says one retry, Task 11 requires only the test name, and the settled(ready, failed) fold row and resume rows 7 and 8 are named nowhere.
- **Evidence (spec):** `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md:315-315` "one retry, `already_in_state` counts as confirmed"
- **Evidence (spec):** `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md:205-205` "`settled(ready, failed)`"
- **Evidence (plan):** `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md:124-124` "one retry"
- **Evidence (plan):** `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md:169-169` "test_guard_release_failure_retries_once_and_reports"

### Finding M-07 [MINOR]: Spec makes --to idempotent in both directions and resume re-issues it

- **Category:** missing-requirement. **Rows:** none
- **Claim:** Spec makes --to idempotent in both directions and resume re-issues it. Task 7 tests only the draft-side no-op, so a --to ready that calls the GitHub CLI on an already-ready PR passes every listed check.
- **Evidence (spec):** `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md:234-234` "`--to` is idempotent, so a retry or a resume re-issue is safe"
- **Evidence (spec):** `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md:232-232` "`--to ready` | same with"
- **Evidence (plan):** `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md:111-111` "`--to draft` on a draft PR makes no `pr ready` call"

### Finding M-08 [MINOR]: Spec says a CI-fix cycle from Wave 8 also engages (kind ci)

- **Category:** missing-requirement. **Rows:** INF-001
- **Claim:** Spec says a CI-fix cycle from Wave 8 also engages (kind ci). Task 11's scenario list has no CI-fix case and the Wave 8 check only asserts that a sentence exists.
- **Evidence (spec):** `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md:61-61` "CI-fix cycle from Wave 8"
- **Evidence (plan):** `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md:166-166` "Cover the cases of the section 5 table"
- **Evidence (plan):** `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md:153-153` "the Wave 8 test asserts the CI-fix sentence"

### Finding M-09 [MINOR]: Spec 274 requires the engage-failure message to name --merge-guard off and print the clear command

- **Category:** missing-requirement. **Rows:** INF-016
- **Claim:** Spec 274 requires the engage-failure message to name --merge-guard off and print the clear command. Task 8 requires only the terminal_halted halt with reason draft_guard_unavailable, so no criterion asserts the message text.
- **Evidence (spec):** `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md:274-274` "Message names `--merge-guard off` and prints the clear command."
- **Evidence (plan):** `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md:129-129`

### Finding M-10 [MINOR]: Spec requires the PR body to state the release gate plainly

- **Category:** missing-requirement. **Rows:** INF-055
- **Claim:** Spec requires the PR body to state the release gate plainly. The plan records it in the Task 1 record and the command text only; no task authors or checks a PR body. Advisory: the PR is opened outside the plan.
- **Evidence (spec):** `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md:326-326` "the PR body states the gate plainly"
- **Evidence (plan):** `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md:33-33` "the PR body states the gate plainly"
- **Evidence (plan):** `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md:182-182` "the PR body states the release gate"

### Finding M-11 [MINOR]: Spec 377 asks for byte-identical checks against literal string constants of the pinned sentences; Task 10 reco

- **Category:** unpassable-check. **Rows:** none
- **Claim:** Spec 377 asks for byte-identical checks against literal string constants of the pinned sentences; Task 10 records only the literal start text, so a later change inside a pinned sentence may pass. Marginal: the existing pins may themselves be start-text pins.
- **Evidence (spec):** `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md:377-377` "compare against literal string constants taken from the existing pins"
- **Evidence (plan):** `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md:154-154` "the literal start text recorded in"

### Finding M-12 [MINOR]: The Wave 0 test checks --resume, position, gate wording and the off line, but not the second trigger (a run lo

- **Category:** missing-requirement. **Rows:** INF-007
- **Claim:** The Wave 0 test checks --resume, position, gate wording and the off line, but not the second trigger (a run log that already holds guard events) or that the off line is printed once; a bullet missing either still passes.
- **Evidence (spec):** `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md:241-241` "or when the run log holds guard events"
- **Evidence (spec):** `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md:59-59` "prints once"
- **Evidence (plan):** `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md:137-137` "literal `off` line"

### Finding M-13 [MINOR]: Task 12 extends the protocol test file that Tasks 9 and 10 extend without depending on them, and Task 13 compa

- **Category:** other. **Rows:** INF-057
- **Claim:** Task 12 extends the protocol test file that Tasks 9 and 10 extend without depending on them, and Task 13 compares against Task 1's record without a direct Depends on line for it. Both are reached in listed order, so only a parallel executor is affected.
- **Evidence (spec):** `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md:363-363` "Declare dependencies completely, one `Depends on:` line per dependency"
- **Evidence (plan):** `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md:179-180`
- **Evidence (plan):** `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md:190-193`

### Finding M-14 [MINOR]: The plan constraint that protocol prose carries no file:NNN pointers, and the statement that the new ref has n

- **Category:** missing-requirement. **Rows:** INF-059
- **Claim:** The plan constraint that protocol prose carries no file:NNN pointers, and the statement that the new ref has no python fence, have no matching criterion in Tasks 8, 9, 10 or 12.
- **Evidence (plan):** `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md:23-23` "Protocol prose carries no `file:NNN` pointers."
- **Evidence (plan):** `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md:128-128`

### Finding M-15 [MAJOR]: Spec says applied_edits for the release decision is this cycle's count, not the run-wide output field, but nei

- **Category:** missing-requirement. **Rows:** INF-022
- **Claim:** Spec says applied_edits for the release decision is this cycle's count, not the run-wide output field, but neither plan nor spec says where the per-cycle count comes from. An implementer who passes the run-wide count cannot meet the zero-edit-after-a-fixing-cycle case.
- **Evidence (spec):** `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md:107-107` "`applied_edits` is THIS cycle's count of applied edits"
- **Evidence (plan):** `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md:124-124` "this cycle's applied-edit count"

### Finding M-16 [MAJOR]: The fold keeps a cycle_id field and held_cycle_published compares against it, but the effect table never says 

- **Category:** missing-requirement. **Rows:** INF-023
- **Claim:** The fold keeps a cycle_id field and held_cycle_published compares against it, but the effect table never says when cycle_id is set or updated. If it stays fix-1, a normal push of fix-2 before a crash is not seen as published and the PR stays draft after resume.
- **Evidence (spec):** `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md:190-190` "phase, phase_before_request, cycle_id"
- **Evidence (spec):** `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md:196-206`
- **Evidence (plan):** `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md:56-56`

### Finding M-17 [MINOR]: Resume row 4 re-enters release_decision with push_completed true but names no values for applied_edits and tar

- **Category:** missing-requirement. **Rows:** INF-033
- **Claim:** Resume row 4 re-enters release_decision with push_completed true but names no values for applied_edits and target_sha; release row 7 precedes the head check in row 8, so an unspecified zero edit count releases without checking the head.
- **Evidence (spec):** `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md:166-166` "re-enter `release_decision` with `push_completed=True`"
- **Evidence (plan):** `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md:77-77` "re-enter `release_decision` with `push_completed=True`"

## Recommendations

All targets are the plan file `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md` unless stated.

### Recommendation R-001: Pin the per-cycle edit count and the fold's cycle id rule

- **File:** the plan, Tasks 3, 4 and 8 (and spec lines 107 and 190-206 if the owner agrees to amend the spec)
- **Change:** State where `release_decision` gets this cycle's `applied_edits` (for example, count `fix_applied` events carrying the guard's `cycle_id`), state when the fold sets or updates `cycle_id`, and name the `applied_edits` and `target_sha` that resume row 4 passes.
- **Verifier:** add a Task 3 test where fix-1 is released, fix-2 engages, a normal `push_completed` for fix-2 is logged, and `held_cycle_published` is true; it must fail on a fold that keeps `fix-1`. `grep -n "cycle_id" <plan>` shows the new criterion.
- **Linked findings:** M-15, M-16, M-17
- **Priority:** P1

### Recommendation R-002: Carry the event, key and script contract into the protocol ref task

- **File:** the plan, Task 8
- **Change:** Change the source list to spec sections 3 and 4.1 to 4.4 as spec line 240 states, and add criteria that the ref states the `draft_guard_requested` and `draft_guard_settled` payload fields, the `idempotency_key` format, the one retry of a failed release, and the engage-failure message that names `--merge-guard off` and prints the clear command.
- **Verifier:** the Task 8 protocol test asserts those four phrases; `uv run pytest tests/pr_submit/test_merge_guard_protocol.py -q` fails when any is removed.
- **Linked findings:** M-03, M-06, M-09
- **Priority:** P1

### Recommendation R-003: Make the Wave 0 bullet test passable and complete

- **File:** the plan, Task 9
- **Change:** Replace "no `L3 only` or `draft` gate wording" with an explicit list (for example: no "only at L3", no "only with draft" load condition) and add assertions for the second trigger (a run log that already holds guard events) and that the off line is printed once.
- **Verifier:** the Wave 0 test passes on a bullet that says "at L3 with `--merge-guard off`" and fails when the second trigger is missing.
- **Linked findings:** M-01, M-12
- **Priority:** P2

### Recommendation R-004: Add the missing assertions to Tasks 3, 4, 7 and 11

- **File:** the plan, Tasks 3, 4, 7 and 11
- **Change:** Assert `original_is_draft` after a first skip; assert `notes` carries `auto_merge_armed` on `ENGAGE`; name the `settled(ready, failed)` fold row and resume rows 7 and 8; test `--to ready` as a no-op on a ready PR; add a CI-fix engage case with cycle id `ci-1`; add a release-failure scenario (one retry, `release_pending`).
- **Verifier:** each new test fails against a stub that omits the behaviour; `uv run pytest tests/pr_submit -q` passes on the real implementation.
- **Linked findings:** M-04, M-05, M-06, M-07, M-08
- **Priority:** P2

### Recommendation R-005: Tie the three cycle-id users to one id

- **File:** the plan, Tasks 8 and 10
- **Change:** Require Task 10's Wave 3 bullet to name the single place Task 1 O1 finds, and extend the acceptance trace so the guard events, the push triad and `rereview_requested` carry the same `cycle_id`.
- **Verifier:** the trace test compares the `cycle_id` of the three event groups and fails when one differs.
- **Linked findings:** M-02
- **Priority:** P2

### Recommendation R-006: Complete the dependency lines and enforce the two prose constraints

- **File:** the plan, Tasks 8, 9, 10, 12 and 13
- **Change:** Add `Depends on:` lines (Task 12 on Tasks 9 and 10, Task 13 on Task 1) and add protocol-test assertions that the ref and the SKILL bullets carry no `file:NNN` pointer and the ref has no python fence.
- **Verifier:** `grep -n "Depends on" <plan>` lists the new lines; the protocol test fails on a `file:123` pointer.
- **Linked findings:** M-13, M-14
- **Priority:** P2

### Recommendation R-007: Decide who states the release gate in the PR body and pin full sentences

- **File:** the plan, Tasks 1, 10 and 12 (or the coordinator's PR checklist)
- **Change:** Name the owner of the PR-body gate statement, and store the full pinned sentences (not only their start) as constants for the byte-identical checks.
- **Verifier:** the Task 10 byte-identical test compares the full sentence and fails when a word later in the sentence changes.
- **Linked findings:** M-10, M-11
- **Priority:** P2

## Reviewer ensemble and identity

| Reviewer | Persona | Class requested | Pinned model (resolution.json) | Self-reported model | Calibrated C | Findings |
|---|---|---|---|---|---|---|
| 1 | analyzer | sonnet | claude-sonnet-5-5 | claude-gw-tier1b | 0.69 | 2 |
| 2 | qa | haiku | claude-haiku-5-5 | claude-haiku-5-5 | 0.55 | 12 |
| 3 | refactorer | opus | claude-opus-5-5 | gpt-6-luna | 0.71 | 2 |

- The pins in `panel/resolution.json` record the class rotation, not the served model. Reviewer 3 reported `gpt-6-luna`, which is what the `ANTHROPIC_DEFAULT_OPUS_MODEL` alias of this run serves, so `identity_mismatch_suspected` is true and `identity_source` is `requested-pinned`: no verified-independence claim is made.
- Calibrator class: the opus class (served as `gpt-6-luna` by self-report); `calibrator_diversity: degraded` because all three reviewer classes are in use. T1 card calibration C = 0.69; mean of the three card calibrations = 0.65.
- Executor class unresolved (`executor_class_resolved: false`): this audit is of a plan, not of finished work.
- Vendor diversity: multi (Anthropic and OpenAI served classes); model-class diversity: full.

## Debate (Wave 4)

- Mode A, depth standard, three advocates (model inherited from the orchestrator session), Round 2 sequential, Round 2.5 invariant probe, base selection by hybrid score: variant 2 (0.7212 vs 0.6693 and 0.6648; margin 0.0519, no tiebreaker). Merge by the merge-executor agent; the 17-line findings block is byte-identical to the verified jsonl.
- The advocates of the two variants that carried a MAJOR/blocking finding (variants 2 and 3) conceded it in Round 1; the third advocate had already rated both MINOR. Each concession rested on plan lines all three could re-read, so the merged verdict contains no blocker that survived adversarial pressure. All three advocates ran on the orchestrator's own model, so this agreement is not an independent-vendor check.
- Invariant probe: 7 entries, 0 HIGH, 2 MEDIUM unaddressed (INV-001, INV-002, carried as M-15 and M-16), 3 LOW unaddressed (INV-003, INV-004, INV-006). The probe agent disclosed reading post-execution code in the working tree for import facts only.
- Judge: the sc-adversarial return contract names no judge, so `judge_identity` is unknown and `judge_class_collision` is unknown. The orchestrator session (claude-gw-tier1b) ran the scoring inline.

## Grounding notes

- Evidence validator (Sonnet class): 49 merged-finding citations and 62 inferred-requirement rows re-read; 0 unfounded. Caveat M-06: plan lines 60 and 73 already cover the release-failure fold and resume rows in blanket wording, so "no behavioural criterion" is broader than the evidence; the narrower reading (the retry, `release_pending` and the named rows have no specific assertion) holds. Caveat M-17: spec lines 155-156, which carry the row 7 before row 8 order, are uncited.
- Reviewer 2's original card had four citations whose quote was not on the cited line (spec 369, 280, 270, 268); the merge replaced them with lines 333, 234 and 232 (the F5 finding was dropped).
- Attribution: the feature this plan describes landed after the base commit `e8db2fe6` (commit `0b8a5801d`). Reviewer 2 saw two post-execution test file names in a grep and opened neither; the probe agent read working-tree code for import facts. No citation points into `.dev/tasks/done/`.

## Inferred requirements (Pass 2)

| INF id | Verbatim quote | Citation | Match result |
|---|---|---|---|
| INF-001 | engage at the first verified Medium-or-higher finding routed to a fix | `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md:6` | containment (Task 8, ratio 0.875) |
| INF-002 | default on at `--monitor 3` via `--merge-guard {draft,off}` | `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md:6` | containment (Task 12, ratio 1.0) |
| INF-003 | release when the fix push is confirmed on the PR head, before replies and the re-trigger | `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md:6` | containment (Task 8, ratio 0.889) |
| INF-004 | an unreadable timeline or an exit with unpublished fixes keeps the PR draft and reports | `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md:6` | containment (Task 8, ratio 0.778) |
| INF-005 | Nothing mutates. A held guard found in the log is reported with the clear command. | `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md:57` | none (best ratio 0.556) |
| INF-006 | Wave 0 loads the ref (Resume and Exit report) before Wave 1: unsettled requests are reconciled before any edit, release or re-trigger | `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md:58` | containment (Task 8, ratio 0.692) |
| INF-007 | Wave 0 prints once: "Remediation is unprotected: --merge-guard off." No draft call is made. | `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md:59` | containment (Task 9, ratio 1.0) |
| INF-008 | The final report prints "PR #N is still mergeable; this run's fixes are local only." | `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md:60` | containment (Task 9, ratio 0.889) |
| INF-009 | Read, decide, request, `--to draft`, settle. Print the clear command once. | `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md:61` | containment (Task 8, ratio 0.667) |
| INF-010 | Settle `skipped/already_draft`, phase `disabled`, never mutate. | `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md:62` | containment (Task 3, ratio 0.857) |
| INF-011 | Release, cause `no_edits`. | `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md:63` | containment (Task 4, ratio 1.0) |
| INF-012 | Script `--read` must show `state == OPEN`; otherwise halt `pr_not_open`, push nothing. | `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md:64` | containment (Task 8, ratio 1.0) |
| INF-013 | Release, cause `pushed`, before reply, resolve and the S5a re-trigger. | `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md:65` | containment (Task 8, ratio 0.75) |
| INF-014 | Settle `skipped/user_override`, phase `disabled`, no more draft calls, keep pushing, report. | `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md:66` | none (best ratio 0.545) |
| INF-015 | Do not release; report `held (timeline unreadable)`; keep pushing. | `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md:67` | containment (Task 8, ratio 0.714) |
| INF-016 | Halt before any edit: `terminal_halted`, reason `draft_guard_unavailable`. | `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md:68` | containment (Task 8, ratio 1.0) |
| INF-017 | PR stays draft; report `held` with the clear command. | `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md:69` | containment (Task 8, ratio 0.857) |
| INF-018 | No `gh` or `git` word on any line, comments included (F6). | `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md:75` | none (best ratio 0.571) |
| INF-019 | `ValueError` otherwise or when `n < 1`. Never collides with `CONFLICT_CYCLE_PREFIXES`. | `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md:101` | containment (Task 3, ratio 0.6) |
| INF-020 | 1 + the highest `<kind>-<n>` seen in any event's `cycle_id`; 1 when none. | `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md:102` | containment (Task 3, ratio 0.667) |
| INF-021 | Guard requests with no matching settle, matched by `idempotency_key` | `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md:104` | containment (Task 3, ratio 0.833) |
| INF-022 | `applied_edits` is THIS cycle's count of applied edits | `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md:107` | containment (Task 4, ratio 1.0) |
| INF-023 | `True` when `guard` is not `None` and the log holds a `push_completed` event whose `cycle_id` equals `guard.cycle_id` | `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md:108` | containment (Task 3, ratio 0.778) |
| INF-024 | a test imports both modules and asserts equality, because the core cannot import `recovery` | `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md:109` | none (best ratio 0.455) |
| INF-025 | `guard_status(guard, mode, ordinal)` maps, first match wins | `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md:112` | containment (Task 3, ratio 0.75) |
| INF-026 | `failed_mutations` keeps a call that failed on the client but landed on the server from being read as a user action | `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md:127` | containment (Task 4, ratio 0.6) |
| INF-027 | `NOOP` (reason `mode_off`, `ordinal`, `conflict_cycle`) | `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md:133` | containment (Task 4, ratio 0.6) |
| INF-028 | `SKIP_ALREADY_DRAFT` | `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md:142` | none (best ratio 0.0) |
| INF-029 | `RELEASE(cause=pushed)` | `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md:156` | containment (Task 4, ratio 0.667) |
| INF-030 | `HOLD(head_mismatch or push_not_completed)` | `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md:157` | none (best ratio 0.333) |
| INF-031 | `REPORT_HELD` (no mutation; prints the clear command) | `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md:164` | containment (Task 8, ratio 0.6) |
| INF-032 | `RECONCILE`, with `reason` one of `resume_reconciled`, `not_applied`, `ambiguous` | `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md:165` | containment (Task 4, ratio 1.0) |
| INF-033 | re-enter `release_decision` with `push_completed=True` | `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md:166` | containment (Task 4, ratio 1.0) |
| INF-034 | appended and fsynced BEFORE the draft/ready call | `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md:178` | containment (Task 7, ratio 0.6) |
| INF-035 | For a draft request that was the first guard record, the whole record is erased | `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md:201` | containment (Task 3, ratio 0.857) |
| INF-036 | A corrupt line still raises, as it does today. | `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md:208` | none (best ratio 0.4) |
| INF-037 | `original_is_draft` is never read from GitHub after the first record | `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md:208` | containment (Task 3, ratio 0.833) |
| INF-038 | `SkillArgs.merge_guard: str = DEFAULT_MERGE_GUARD` | `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md:215` | containment (Task 6, ratio 1.0) |
| INF-039 | `RunConfig` and `run_skill` do not change (F5) | `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md:217` | none (best ratio 0.5) |
| INF-040 | Exit codes: 0 success; 1 `gh` failure or failed verification | `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md:234` | none (best ratio 0.571) |
| INF-041 | `--to` is idempotent, so a retry or a resume re-issue is safe. | `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md:234` | none (best ratio 0.5) |
| INF-042 | A verification mismatch after a mutation is `ok:false, error:"verify_failed"` | `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md:234` | containment (Task 7, ratio 0.857) |
| INF-043 | No new python fence | `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md:241` | containment (Task 9, ratio 1.0) |
| INF-044 | update it to 45 and name `draft_guard_requested` and `draft_guard_settled` | `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md:242` | containment (Task 2, ratio 1.0) |
| INF-045 | A `held` report always carries the reason and `gh pr ready <N> --repo <REPO>` | `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md:247` | containment (Task 8, ratio 0.889) |
| INF-046 | keep exactly one source for it (open item O1) | `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md:251` | none (best ratio 0.571) |
| INF-047 | needs one entry in `WRITE_VERB_CLASSIFICATION` | `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md:255` | containment (Task 9, ratio 1.0) |
| INF-048 | The `read-only` category is not used for these calls | `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md:255` | containment (Task 1, ratio 0.75) |
| INF-049 | Acceptance trace (must appear in this order in the run log) | `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md:270` | containment (Task 11, ratio 0.833) |
| INF-050 | Record `make lint`, `uv run ruff format --check src/ tests/` and the full-suite result | `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md:301` | containment (Task 1, ratio 0.923) |
| INF-051 | Never stage `.claude/`. | `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md:301` | none (best ratio 0.333) |
| INF-052 | Run `make sync-dev` at the end of every task that edits a file under `src/superclaude/skills/` or `src/superclaude/commands/` | `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md:301` | containment (Task 8, ratio 0.917) |
| INF-053 | A static test asserts `merge_guard.py` has no `gh` or `git` word. | `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md:322` | containment (Task 3, ratio 1.0) |
| INF-054 | No task makes a live PR call, and the run that opens the PR must not enable the feature (`--merge-guard off`). | `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md:326` | containment (Task 1, ratio 0.833) |
| INF-055 | The user guide states that draft behaviour is unverified until then, and the PR body states the gate plainly. | `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md:326` | containment (Task 1, ratio 1.0) |
| INF-056 | Cite tests and constants by symbol name | `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md:362` | containment (Task 1, ratio 0.6) |
| INF-057 | Declare dependencies completely, one `Depends on:` line per dependency | `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md:363` | none (best ratio 0.429) |
| INF-058 | Update the 43-member enumeration in `refs/loop-guard.md` in the event-enum task. | `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md:368` | containment (Task 2, ratio 0.909) |
| INF-059 | Protocol prose written by the plan never carries `file:NNN` pointers | `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md:369` | none (best ratio 0.556) |
| INF-060 | the crash scenario tests derive branches from a real `RunLog` through `detect_crash_window` and `resolve_crash_window` | `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md:375` | containment (Task 11, ratio 0.8) |
| INF-061 | the plan states that a settled `not_applied` of either direction returns to `phase_before_request` | `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md:376` | containment (Task 3, ratio 0.625) |
| INF-062 | scenario tests import only helpers and fixtures from `test_set_draft_state.py`, never `test_*` functions | `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md:377` | containment (Task 11, ratio 0.7) |

Postscript: no inferred row was dropped by the evidence validator (62 of 62 quotes verbatim at their lines).

## Inferred-claim audit

- `citations_inferred: 0`
- Inferred-fraction: `0 / 111` = 0.00

