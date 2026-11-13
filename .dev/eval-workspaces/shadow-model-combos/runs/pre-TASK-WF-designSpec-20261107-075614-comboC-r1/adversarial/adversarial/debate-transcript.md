# Adversarial Debate Transcript

## Metadata
- Depth: standard
- Rounds completed: 2 (+ Round 2.5 invariant probe)
- Convergence achieved: 100% by the >=2/3 agreement rule (20/20 points); unanimous on 14/20 points (70%)
- Convergence threshold: 80%
- Focus areas: correctness, coverage, deviation-classification
- Advocate count: 3 (V1 advocate haiku class, V2 advocate opus class, V3 advocate sonnet class; the judge is the orchestrator, sonnet class: judge_class_collision with the V3 advocate and with reviewer 1)

## Round 1: Advocate Statements

### Variant 1 Advocate
#### Round 1 Advocate Statement: Variant 1 (analyzer reviewer card)

Sources: spec = `input/TASK-WF-designSpec-20261107-075614/source.md`; plan = `input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md`. "L" = line in those files.

##### Position summary

V1 is the only card that traces the decision tables across cycles. It shows that a faithful build of this plan releases a PR while an earlier cycle's fix is unpublished (F2), and that one Task 7 check cannot fail (F1). Its weakness is that it grades F2 non-blocking.

##### Steelman: Variant 2 (qa)

Strongest version: the plan's acceptance criteria are the only mechanical gate before build, and many pass empty or wrong implementations. V2 is right on three counts. The release retry is unspecified: spec L315 names it only in the test table, no release row (L147-157) yields a retry, and the script never emits `already_in_state` (L231-232). Its F1 is real: plan L25 cites "non-goals of source.md", which has no such section, and spec L61 engages CI-fix cycles despite the plan's "not held through ... CI". Its F5 is real: plan L172 forbids `pr ready` without `--undo` only for originally draft PRs.

##### Steelman: Variant 3 (refactorer)

Strongest version: a scheduler that follows `Depends on:` lines runs tasks in the order the plan declares, and spec L363 requires one line per consumed output. V3 finds that Tasks 9, 10, 12 and 13 consume Task 1's record without a Task 1 line (plan L132-135, L148, L177-193). It also finds that Task 12 edits `test_merge_guard_protocol.py` and the classification table, which Tasks 9 and 10 also edit (plan L137, L150, L180-181), with no dependency. That is a real collision risk, and V3 correctly treats the structural pins as a separate review concern.

##### Strengths claimed

1. F2 (carry-over release). Spec L6: "an exit with unpublished fixes keeps the PR draft." Engage row 7 returns `NOOP(already_held)` for a second cycle while HELD (L139). Release row 7, `applied_edits == 0 → RELEASE(no_edits)` (L155), is checked before HOLD row 9 (L157), and plan L75 requires it. A zero-edit fix-2 therefore marks the PR ready while fix-1's commit is still local. This comes from the tables, not from inference about code.
2. F1 (unfailable count). Plan L111-113 asserts key names and the null-timeline case only. Spec L230 requires `gh api --paginate` and a count of `convert_to_draft` and `ready_for_review` events. A one-type or unpaginated count passes.
3. F3 (fold branch). Spec L201 returns a settled `not_applied` ready request to `RELEASE_PENDING` after a failed release. Plan L60 tests only the `HELD` result.

##### Weaknesses identified in other variants

1. V2 inflates blocking status. Its F6 (plan L169, L173) says test names without bodies pass. That is a build-process check, not a design defect, yet it is rated MAJOR and blocking.
2. V2 misses the decision-table trace. None of its 12 findings follows a release path across cycles, so it misses the carry-over case the diff analysis rates High (C-004).
3. V3's F3 misreads plan L142, which bars edits to "any existing test expectation." A new `WRITE_VERB_CLASSIFICATION` key is not an existing expectation, so the claimed contradiction is weak.
4. V3 rates the Task 12 collision (its F2) MINOR, though a parallel run could clobber an edit to a shared file.
5. None of V3's four findings reaches a decision row, fold rule or script output. Its coverage is structural only.

##### Concessions

1. I marked all three findings `blocking: false`. F2 should be blocking: plan L75 makes the wrong release a passing criterion, so a correct build ships it.
2. My "dependencies complete" claim covered only the import chain. Spec L363 asks for every consumed output, and V3 shows that is not met.
3. I missed V2's F3 (retry), F5 (`--undo` on the ready call) and F7 (auto-merge value). Each is a real gap I should have checked.

##### Shared assumptions

- **A-001: QUALIFY.** A later fix cycle can start after a HOLD. Engage row 7 (spec L139) handles a second engage while HELD, so the design expects it. But the spec never says what a later zero-edit cycle does with earlier unpublished fixes. That gap is F2, so the assumption holds only with this qualifier.
- **A-002: ACCEPT** as the review standard. The plan sets it: Task 3 requires each fold case to "fail if the row is implemented wrongly" (plan L60). V2's F6 and my F1 apply it to criteria that name tests or keys. V3's F3 and F4 do not depend on it; they concern internal contradictions.

### Variant 2 Advocate
#### Round 1 advocate, Variant 2

##### Position summary
V2 is the only card that checks whether each criterion would fail on a wrong implementation, which spec 366 requires. Three of its criterion gaps hold: F5 (`--undo`), F7 (the auto-merge value) and F4 (cycle-id reuse). V2 over-used `blocking:true`: none of its seven blocking flags survives a careful read, and F1 and F3 are partly wrong.

##### Steelman
- **V1.** F2 is the deepest finding of the three cards. After fix-1 ends in `HOLD` (spec 157), fix-2 gets `NOOP(already_held)` (spec 139) and, with zero edits, reaches `RELEASE(no_edits)` (spec 155). Plan 75 requires that release, which breaks spec 69. Critique: the defect is in the spec and the plan copies it faithfully. It depends on A-001. V1 files a "data-loss" category as non-blocking. It also claims the dependencies are complete, but Task 13 uses "the base-commit record of Task 1" (plan 195) and declares only Tasks 2, 10, 11 and 12 (plan 190-193).
- **V3.** Its F1 breaches an explicit plan rule: "one `Depends on:` line per dependency … the protocol tasks need the pre-build record" (spec 363). Tasks 9, 10 and 12 (plan 134-135, 148, 179-180) do not declare Task 1. Critique: V3 grades that breach MINOR, and it never tests whether a criterion can fail, so it misses C-003, C-007 and C-008.

##### Strengths claimed
1. **F5.** The draft call needs `--undo` (spec 231). The Task 7 checks cover only "`--repo` or a `repos/` path" (plan 113). Plan 172 requires `--undo` only "for an originally draft PR". A script that leaves out `--undo` passes every criterion unless the fake `gh` keeps PR state, which the plan does not require.
2. **F7.** Engage row 11 carries `auto_merge_armed` in `notes` (spec 143). Task 4 asserts only "`action`, `reason` and `cause`" (plan 73), and Task 7 checks only that the `autoMergeRequest` key is present (plan 111).
3. **F4.** Spec 251 requires the push triad and `rereview_requested` to reuse the guard's id. Plan 127 and 129 check only where the id is minted, and plan 170 checks event order only.
4. **F10.** Task 10 says "byte-identical" but compares only "the literal start text" (plan 154).
5. **F9 and F11.** Plan 98 and 150 state the rule in the task body with no criterion, and no check covers the PR-body gate (spec 326).

##### Weaknesses identified in other variants
1. V1's claim that the dependencies are complete is contradicted by plan 190-195.
2. V1 F2 gives no plan-versus-spec classification. It should be filed as a spec defect, not as plan drift.
3. V3 rates a breach of spec 363 as MINOR.
4. Neither applies the failability test of spec 366.

##### Concessions
- **F1 is overstated.** "Not held through … CI" (plan 25) agrees with releasing "before the CI re-poll" (spec 241). Only the wrong label "non-goals" remains: MINOR.
- **F2 is not blocking.** The task body narrows the check to "no `L3 only` or `draft` gate wording" (plan 137), and the criterion wording comes from spec 241. MINOR.
- **F3 is wrong as written.** Plan 124 states "one retry; `already in target state` counts as confirmed", and spec 137, 169 and 205 carry the mechanism. The only gap left is that no criterion limits the release to one retry: MINOR.
- **F6 is overstated.** Plan 170-172 assert content, so empty stubs would fail them. MINOR.
- **F4, F5 and F7 stay MAJOR but not blocking.** F4 and F5 fail safe: they end in held or `verify_failed`.
- V1 F1 (plan 111 checks only that the timeline-count key exists) is a real gap that V2 missed.

##### Shared assumptions
- **A-001 — QUALIFY.** The spec never says whether a new cycle follows a release `HOLD`. A `push_not_completed` may end the run, and "held_through_redrive" (spec 167) suggests the same cycle is redriven. A `head_mismatch` makes a continuing run plausible, so V1 F2 is a conditional spec risk.
- **A-002 — QUALIFY.** The principle is sound, and spec 366 mandates it. A criterion must still be read together with its task body and the other criteria of that task. Read that way, V2 F6 and V3 F3 and F4 shrink, while F5 and F7 survive.

### Variant 3 Advocate
#### Round 1 statement: advocate for Variant 3 (refactorer card)

##### Position summary

V3 is a narrow but accurate card. It checks plan structure (task order, `Depends on:` lines, shared-file edit order, the stale-classification rule) against spec sections 4.7, 6 and 10. Its four MINOR findings are each grounded in a spec rule or a plan contradiction. V3 is weak on behavioural coverage, and I concede that below. I argue its severities are the best calibrated of the three cards.

##### Steelman

**V1.** Its strongest form is the F2 trace. After a release HOLD (row 9), a later zero-edit cycle meets engage row 7 (`NOOP(already_held)`). Release row 7 then returns `RELEASE(no_edits)` before row 9 is reached. The PR goes ready while an earlier cycle's fix is unpublished, which conflicts with spec line 69 ("Any exit after engage with no confirmed push ... PR stays draft"). Task 4 turns this into a criterion. V1 also has a real, failable gap in F1 (Task 7 never checks timeline count or `--paginate`). My critique is below.

**V2.** Its strongest form is that it audits the criteria themselves, which is what a pre-execution audit is for. The `--undo` gap is real: spec line 231 requires it, and Task 7's criteria assert only `--repo`. The auto-merge `notes` gap is real: spec line 143 against plan lines 73 and 111. The unpassable Wave 0 criterion is real. V3 missed the first two.

##### Strengths claimed

1. F1 is a direct spec requirement. Spec line 363 says a task "depends on every earlier task whose output it imports or consumes", and names "the protocol tasks need the pre-build record". Tasks 9, 12 and 13 declare no `Depends on: Task 1`, although each cites `./artifacts/pre-build-gate.md` (plan 137, 182, 195). V1 calls dependencies "complete for the import chain", but the spec rule is wider than imports.
2. F2 is a real race on shared files. Task 12 (plan 177-182) extends `test_merge_guard_protocol.py` and the classification table, as Tasks 9 and 10 do, yet depends only on Tasks 6 and 8.
3. F4 is an internal contradiction. Plan 108 makes `_RESOLUTION_SCRIPTS` conditional on O2. Plan 113 requires the script to pass those tests unconditionally.
4. The "what held" list is evidence a reader can use. It confirms the stale-entry ordering, with the entries added last in Tasks 7 and 8, as spec 4.7 requires. It confirms byte-identical pins checked against constants, as spec 377 requires. It confirms the import-cycle check in Task 5. No other card covers these.
5. V3 does not duplicate T1 F2 and F4. It confirms them without inflating the count.

##### Weaknesses in other variants

1. V2 F1 (blocking) overstates. Spec has no "non-goals" heading, so the plan's attribution at line 25 is loose. But spec Wave 8 (line 241) releases "after `push_completed` before the CI re-poll", so "not held through CI" matches the spec. This is a labelling slip, not a blocking contradiction.
2. V2 F3 (blocking) says FR-16 has "no mechanism". The mechanism exists: `RETRY_RELEASE` (engage row 5, resume row 7), `settled(ready, failed)` returning to `RELEASE_PENDING` (spec 205), and `confirmed, not changed` (spec 202, 204). Plan line 124 says "one retry; `already in target state` counts as confirmed". At most this is a MINOR criterion gap.
3. V2 F6 (blocking) overstates. Task 11 criterion 1 names the tests. Criteria 2-4 (plan 170-172) assert event order, real `detect_crash_window` output and forbidden gh calls, so empty stubs would fail them.
4. V2 sets blocking=true on seven findings; several are MINOR-grade criterion tightening. That makes the verdict "not ready", but the plan has no inverted or missing task.
5. V1 F2 is a spec defect, not a plan defect. Spec 107 states "a zero-edit cycle after a fixing cycle still releases with `no_edits`". The plan copies it faithfully. In a plan-against-spec audit it belongs under "spec gap", not data-loss in the plan.

##### Concessions

- V3 has no behavioural findings. It misses V1 F2, V2 F5 and F7, and the Task 7 count gap. Its "no drift" scope verdict missed the loose line 25.
- V3 F3 is arguable. Adding a classification entry may not count as editing "an existing test expectation".
- V3 confirms T1 F2 (Wave 0 wording) but raises no card entry. Its severity is therefore unrecorded, and V2's MAJOR is the only recorded one.
- All four V3 findings are covered transitively, so MINOR is right but they carry little weight.

##### Shared assumptions

**A-001: QUALIFY.** Engage row 7 (`NOOP(already_held)`) shows the spec expects a second cycle to start in phase `HELD`. The spec never says a run continues to a new cycle after a release-row-9 HOLD specifically. If it does, the flaw sits in the spec's own `applied_edits` rule (spec 107), not in the plan.

**A-002: QUALIFY.** It holds for a criterion whose only content is test names (Task 11 criterion 1). It fails where the criterion also runs the tests and the task body names the cases (Task 11 criteria 2-4, Task 3 criteria). Failability must be judged on body plus criteria together.

## Round 2: Rebuttals

### Variant 1 Rebuttal
#### Round 2 Rebuttal: Variant 1 (analyzer)

##### Response to criticisms

1. **"F2 is a spec defect, not a plan deviation" (V2, V3). Partly conceded.** The origin is spec L107: "a zero-edit cycle after a fixing cycle still releases with `no_edits`." But spec L6 says "an exit with unpublished fixes keeps the PR draft", and L69 keeps the PR draft unless there is "zero-edit proof". Plan L75 turns the release into a passing criterion, so a faithful build ships it. It is spec-origin and plan-pinned, and it breaks an owner decision. It stays blocking.

2. **"A-001 is unstated" (V2).** Conceded as a qualifier. The trace needs a run that continues after a release-row-9 HOLD. The design expects that path: engage row 7 (L139) returns `NOOP(already_held)` for a second engage while HELD. If the run halts after HOLD, the finding narrows to a note.

3. **"Data loss filed as non-blocking; dependencies complete" (V2).** Conceded. The flag was wrong and I withdraw "complete". V3 F1 holds: Task 9 cites `pre-build-gate.md` (plan L137) with no Task 1 line.

4. **Missed V2's F3, F5 and F7 (my round 1).** F5 (`--undo`, spec L231) and F7 (`notes`, spec L143) are real. F3 is a criterion gap, not a missing mechanism: plan L124 says "one retry; `already in target state` counts as confirmed".

##### Updated assessment of other variants

- **V2:** Its advocate withdraws most of its blocking flags, and I accept F1, F3 and F6 as MINOR. F2 stays blocking. Its "L3 only" reading comes from the test sentence at plan L137, but the acceptance criterion at L140 binds: it fails any bullet that "names an L3 or `draft` condition", and spec L59 requires the off line at L3. F4, F5 and F7 are real criterion gaps.
- **V3:** F1, F2 and F4 are real. F3 is arguable. Its lack of behavioural findings is a scope limit, not an error.

##### New evidence

- Task 7's `transitions` feeds `classify_toggles` (spec L118, L120). A script that prints a fixed count gives `observed < run_toggles`, which is `unreadable`, so every release HOLDs (release row 5, L153). Task 7's criteria (L111) would still pass. The result is a held PR, not a wrong release, so V1 F1 is MAJOR and non-blocking.
- A missing `--undo` is caught by the verify step: "A verification mismatch after a mutation is `ok:false, error:"verify_failed"`" (spec L234). That also fails safe.

##### Final rulings

C-004: keep MAJOR true
C-001: keep MAJOR true
C-002: keep MAJOR false
C-003: keep MAJOR false
C-007: keep MAJOR false
C-008: keep MAJOR false
C-005: downgrade MINOR false
C-006: downgrade MINOR false
C-009: downgrade MINOR false
C-010: keep MINOR false
C-011: keep MINOR false

### Variant 2 Rebuttal
#### Round 2 Rebuttal: Variant 2 (qa)

##### Response to criticisms

1. **Seven blocking flags inflated (V1, V3).** Conceded. None of V2's findings blocks; my round 1 already withdrew them.
2. **F3 "no mechanism" (V3, X-002).** Conceded. Plan 124 says "one retry; `already in target state` counts as confirmed". What remains is a criterion gap: no criterion asserts that one-retry phrase.
3. **F1 and F6 overstated (V3).** Conceded. Spec 241 releases "before the CI re-poll", so "not held through ... CI" (plan 25) is consistent with it. Plan 170-172 assert content, so empty stubs would fail them.
4. **F2 should stay blocking (V1 rebuttal).** Partly conceded. The contradiction is literal (see the new evidence), but it comes from the spec: spec 241 carries both "no L3 or `draft` condition" and "at L3 with `--merge-guard off`". The task body narrows the test to "no `L3 only` or `draft` gate wording" (plan 137), so a builder can resolve it. MAJOR, not blocking.
5. **V2 missed the cross-cycle trace (V1).** Conceded as a miss. The finding is conditional, though (see below).

##### Updated assessment of other variants

- **V1:** F1 is real and fails safe. F2 is narrower than claimed. Its "dependencies complete" claim is withdrawn.
- **V3:** Its findings are accurate and correctly graded MINOR. F1 is a literal breach of spec 363 only: Task 9 and Task 12 depend on Task 8, which declares `Depends on: Task 1` (plan 120), so the execution order still holds.

##### New evidence

- **C-001:** Spec 59 and plan 137 require the bullet to say "no draft call is made". So the bullet must contain the word `draft`, and the literal reading of criterion 140 cannot pass. The defect is real but comes from the spec.
- **C-004:** Release row 9 has two causes. A `head_mismatch` comes after `push_completed`, so fix-1 is already published (spec 108). Only `push_not_completed` leaves a fix unpublished, and spec 69 treats that case as an exit. Neither the plan nor the spec shows a new cycle starting after a failed push. Plan 75 copies spec 107 and spec 322 faithfully. Blocking false.
- **C-007:** A push with a different id makes `held_cycle_published` false (spec 108), so resume holds. Safe; the criterion gap stays.
- **C-008:** Without `--undo`, verify fails (spec 234) and engage halts before any edit (spec 68). Safe, but the feature is inert.

##### Final rulings

C-001: keep MAJOR false
C-002: keep MAJOR false
C-003: keep MAJOR false
C-004: keep MAJOR false
C-005: downgrade MINOR false
C-006: downgrade MINOR false
C-007: keep MAJOR false
C-008: keep MAJOR false
C-009: downgrade MINOR false
C-010: keep MINOR false
C-011: keep MINOR false
C-012: keep MINOR false

### Variant 3 Rebuttal
#### Round 2 Rebuttal: Variant 3 (refactorer)

##### Response to criticisms

1. **"No behavioural findings" (V1, V2).** Conceded. V3 audits order and structure, and missed the `--undo` and `notes` gaps. Its "no drift" verdict also missed the loose attribution at plan line 25. That is a scope limit, not an error in what it did report.
2. **F1 "transitively covered" (V2).** Conceded as a weight point. Task 9 and Task 12 reach Task 1 through Task 8 (plan 120), so execution order holds. It still breaches spec 363 ("one `Depends on:` line per dependency"), and V1 withdrew its "dependencies complete" claim. Stays MINOR.
3. **F3 arguable (V3 round 1).** Conceded. Adding a classification entry is an addition, not an edit of an "existing test expectation", so the contradiction is weak. It stays MINOR, low confidence.
4. **F2 and F4.** Not contested. F4 is a plain conditional against an unconditional criterion (plan 108 vs 113).
5. **"V3 confirmed T1 F2 with no recorded severity."** Accepted. I record it now (C-001 below).

##### Updated assessment of the other variants

- **V1:** Its F1 is real and fails safe, since an unreadable count HOLDs the PR. F2 is its strongest finding but its blocking flag does not survive (see C-004).
- **V2:** The advocate withdrew the blocking flags and the "no mechanism" claim. Plan 124 states the retry. Its criterion gaps (F4, F5, F7) are real.

##### New evidence

**C-004: can a later cycle follow a release HOLD?** The spec supports the path in part.
- Engage row 7 (spec 139) returns `NOOP(already_held)` when `guard.phase == HELD`. A run can therefore see HELD at a later engage.
- Release row 9 (spec 157) holds and leaves the phase HELD. Spec 275 also leaves it HELD after a validation failure.
- A zero-edit later cycle then meets release row 7 (spec 155, `applied_edits == 0`), which comes before row 9. It would release with `no_edits`.
- Against that: the `head_mismatch` cause has already pushed, so nothing is lost. Only `push_not_completed` leaves a fix unpublished. Nothing in spec 139, 147-157, 164-171 or 274-281 shows a new cycle starting after that case; resume row 5 (spec 167) keeps HELD through a redrive instead.
- Verdict: the scenario is reachable in principle but not shown. The rule is spec text copied faithfully into the plan, so it is a spec gap. MAJOR, not blocking.

**C-001:** Spec 241 says the Wave 0 bullet "contains no L3 or `draft` condition" and also that "at L3 with `--merge-guard off`" it prints the unprotected line. The first clause is about whether the bullet applies, the second is its content. The plan's task body (137) narrows the test to gate wording, so a builder can resolve it. A literal reading of criterion 140 fails. MINOR, not blocking.

##### Final rulings

C-001: downgrade MINOR false
C-002: keep MAJOR false
C-003: downgrade MINOR false
C-004: keep MAJOR false
C-005: downgrade MINOR false
C-006: downgrade MINOR false
C-007: downgrade MINOR false
C-008: keep MAJOR false
C-009: downgrade MINOR false
C-010: keep MINOR false
C-011: keep MINOR false
C-012: keep MINOR false

## Round 2.5: Invariant Probe
See invariant-probe.md (9 findings; 6 UNADDRESSED: 1 HIGH INV-009, 3 MEDIUM, 2 LOW). INV-009 was resolved by the orchestrator against the base-commit protocol text (see the addendum in that file), so no HIGH UNADDRESSED item remains.

## Scoring Matrix
| Diff Point | Winner | Confidence | Evidence Summary |
|---|---|---|---|
| S-001 | V3/V1 posture (no blocking findings) | 80% | V2 advocate withdrew all seven blocking flags; V1 kept only C-004 and the probe plus base protocol undercut it |
| S-002 | none (style) | 90% | cosmetic |
| S-003 | all (complementary lenses) | 85% | each lens found findings the others missed |
| C-001 | V2 (finding stands, MAJOR, non-blocking) | 70% | literal clash of plan:137 and plan:140; spec:241 has it too; V3 rated MINOR |
| C-002 | V1 (MAJOR, non-blocking) | 90% | unanimous; fails safe (an unreadable count holds) |
| C-003 | V2 (MAJOR, non-blocking) | 75% | notes/value never asserted; V3 MINOR |
| C-004 | V1 (MINOR after evidence) | 65% | scenario needs a cycle after a failed push; base protocol halts there |
| C-005 | V2 (MINOR) | 90% | plan:124 specifies the retry; only a criterion is missing |
| C-006 | V2 (MINOR) | 90% | "non-goals of source.md" is a mislabel; spec has no such section |
| C-007 | V2 (MAJOR, non-blocking) | 70% | no equality assertion; fails safe |
| C-008 | V2 (MAJOR, non-blocking) | 85% | unanimous; verify_failed catches it |
| C-009 | V2 (MINOR) | 85% | plan:170-172 assert content |
| C-010 | V3 (MINOR) | 85% | Task 1 consumers lack a direct line; execution order holds through Task 8 |
| C-011 | V1 (MINOR) | 90% | unanimous |
| C-012 | V3 (MINOR) | 85% | unanimous |
| X-001 | V1/V3 | 85% | V2 conceded blocking inflation |
| X-002 | plan:124 | 95% | retry is specified |
| X-003 | V3 | 90% | V1 withdrew "complete" |
| A-001 | QUALIFY | 80% | spec silent on a cycle after HOLD; base protocol halts on push failure |
| A-002 | QUALIFY | 80% | read the criterion with its task body |

## Convergence Assessment
- Points resolved: 20 of 20 (>=2/3 rule); unanimous: 14
- Alignment: 100% (unanimity-only 70%); sycophancy caution: the V2 advocate withdrew most of its own findings in Round 1, so agreement is partly concession
- Threshold: 80%
- Status: CONVERGED (invariant gate: HIGH UNADDRESSED = 0 after the orchestrator resolution of INV-009)
- Unresolved points: none
