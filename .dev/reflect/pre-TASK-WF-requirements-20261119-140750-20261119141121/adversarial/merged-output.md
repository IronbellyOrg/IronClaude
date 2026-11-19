<!-- Provenance: This document was produced by /sc:adversarial (merge-executor) -->
<!-- Base: Variant 3 (opus:refactorer), reviewer-cards/reviewer-3-card.md -->
<!-- Merge date: 2026-11-19 -->

# Merged reflection verdict: v4 plan (UC-1 pre-execution)

<!-- Source: Variant 3 (base) - header and verdict line; Round 2 verdict for the counts -->
Plan file: /home/coder/workspaces/worktrees/IronClaude/claim-handoff-planb/.dev/tasks/to-do/TASK-WF-requirements-20261119-140750/TASK-WF-requirements-20261119-140750.md (`plan:N` is a line of it; `source.md:N` is a line of `source.md` next to it; `guard` is src/superclaude/hooks/scripts/launch-level-guard.sh; paths below are relative to the worktree root).
Verdict: FAIL as advice. 5 blocking (P4-1 Safety; P4-2 to P4-5 Decision), 6 medium (P4-6 to P4-11), 11 notes (P4-12 to P4-22). Owner decisions needed: none. Convergence 0.784 against 0.80: NOT_CONVERGED (see "Convergence and the unresolved point").

<!-- Source: Variant 1, Variant 2, Variant 3 (card status lines); Round 2 verdict for Q-1 (X-001), Q-6 (X-002), Q-10 (X-003) -->
Confirmed fixed: Q-1 PARTIAL (the guard pattern is fixed except for the case in P4-4; stays PARTIAL while that finding is open); Q-2 FIXED; Q-3 FIXED, with the empty-Pipeline gap of P4-2; Q-4 FIXED; Q-5 FIXED; Q-6 PARTIAL at Note level (P4-16); Q-7 FIXED; Q-8 FIXED; Q-9 FIXED; Q-10 PARTIAL at Note level (P4-21). The six owner decisions: ship gate FIXED, `updatedAt` observation FIXED, self-approval warn-only FIXED (with P4-15), tamper token FIXED, four pipelines end at In review FIXED, extra guard refusals PARTIAL (P4-4, P4-19).

## Findings (register P4-1 to P4-22)

Grades follow the owner's rule: Blocking only when the fix changes a named decision, a required behaviour or an acceptance check (Decision), a required deliverable is absent (Missing), or following the plan breaks a safety boundary (Safety); otherwise Medium or Note. Grades are the final ones of `adversarial/adversarial/round2-rebuttals.md` section 3. Evidence lines marked "carried" were not re-read in this run.

### Blocking

<!-- Source: Variant 3 B-1 (base); Round 2 verdict C-001 Blocking (Safety), 3/3 advocates agree; refactor plan R-01 -->
### P4-1 BLOCKING (Safety)
- Task: Tasks 15, 16, 11, 14, 23. Affected action: the coordinator's plan-approval gate for any repo other than IronClaude. Live even with the gate closed, because level None starts plan workers.
- Evidence: `stage-status` has no repo argument; it calls `gh.reread(runner, budget, issue, _timeout)` (src/superclaude/cli/issue_pipeline/cli.py:279) and `reads.read_stage_evidence(runner, issue, _timeout, budget)` (cli.py:282) and defaults `--config` to `~/.config/superclaude/issue-watch.json` (cli.py:343-348). `read_stage_evidence` calls `gh.events` and `gh.edits` with no repo (src/superclaude/cli/issue_pipeline/reads.py:142,148) and the comments read goes through `argv_comments_projected(n, page)` with no repo (reads.py:65-67). `REPO = "IronbellyOrg/IronClaude"` (src/superclaude/cli/issue_watch/github.py:37) and the literal in `EDITS_QUERY` (github.py:75) and `PROJECT_ITEMS_QUERY` (github.py:89) fix every read to that repo. Task 15 keeps `REPO` as the default "so reads.py ... keep working unchanged" (plan:227); Task 16 passes `cfg.repo` only "from the cycle" (plan:238); Task 23 serves every allowed-owner repo (plan:313). `WORKER-CONTRACT.md:298` tells the coordinator to "read GitHub through `stage-status` at each gate or wake"; `WORKER-CONTRACT.md:242` says every such action targets `IronbellyOrg/IronClaude`. Result: a coordinator for repo X running `stage-status N` reads the approval evidence of IronClaude issue N. It fails closed in the usual case (no plan reply there) and can fail open if `--plan-dir` is omitted and an issue number collides (cli.py:293-294). Confidence 0.80 (the fail-open path needs a number collision).
- Fix: Task 16 adds `src/superclaude/cli/issue_pipeline/cli.py`, `reads.py` and their tests to its files. `stage-status` takes `--repo`, default the `repo` key of the chosen `--config`, and passes it to `gh.reread`, `read_stage_evidence`, `gh.events`, `gh.edits` and the comments read; Task 15 gives `argv_comments_projected` and `read_stage_evidence` a `repo` parameter. Test: with a second repo every argv carries that repo and none carries `IronbellyOrg/IronClaude`; an approval label on the IronClaude issue of the same number never approves the other repo's issue. Task 11: reword `WORKER-CONTRACT.md:242` to "the repo the issue belongs to, never the SuperClaude upstream" (the ":293 covers claims at every level" rewrite is already planned). Alternative if not done: Task 23 serves only `IronbellyOrg/IronClaude` until it is. Add `issue_pipeline/cli.py` (Tasks 14, 16) to plan:30.

<!-- Source: Variant 3 B-2 (base); Round 2 verdict C-002 Blocking (Decision), 2/3 advocates agree; refactor plan R-02 -->
### P4-2 BLOCKING (Decision)
- Task: Tasks 3, 5. Affected action: the void rule for an empty Pipeline, the only level the closed gate lets launch.
- Evidence: `_project_item` maps a null `fieldValueByName` to `None` (github.py:764-775; the Status branch at :770-774). Task 3 says an absent Pipeline value is Python `None` with `pipeline_changed_at: datetime | None` (plan:61) and that a malformed time gives `non_json` or `unreadable` at the read layer, "not an exception" (plan:65). Task 5 says "an unreadable time also refuses" (plan:84) and its acceptance covers "an unreadable time refuses" with no empty-Pipeline case (plan:87-88). Absent and unreadable are the same value at the predicate, so read literally every issue with an empty Pipeline ends `edited_after_approval`, and an empty Pipeline is the decided None launch path (plan:95, plan:27).
- Fix: Task 3: "An absent Pipeline value is `pipeline_name = None`, `pipeline_changed_at = None` and means no time, not unreadable; a malformed time fails the whole read." Task 5: "the later of the value times that exist; an absent Pipeline contributes none; a Status name with no Status time refuses." Acceptance rows: an empty Pipeline with a Status time before the approval passes and launches with `--pipeline none`; a malformed time gives the read refusal; a Pipeline cleared after approval launches at None (lowest level, no authority raised) and the design note says so; a Pipeline value changed after approval refuses.

<!-- Source: Variant 2 QA-2 (V3 located the rule); Round 2 verdict C-003 Blocking (Decision), 2/3 advocates agree; refactor plan R-03 -->
### P4-3 BLOCKING (Decision)
- Task: Task 11.
- Evidence: plan:176 puts "a claim-time event is refused as plan approval" in `tests/issue_pipeline/test_approval_record.py`. `record_create` takes a plan hash, a channel (checked against `CHANNELS`), an evidence id and an actor, each only pattern-checked, and its only state check is that an adoption row exists (src/superclaude/cli/issue_pipeline/approval_record.py:313-338); nothing in it tells a claim-time event from a plan one. The rule that does exist is in `stage_predicates._label_channel`: a label counts only if `e.created_at > reply.created_at`, otherwise `label-before-plan` or `no-label` (src/superclaude/cli/issue_pipeline/stage_predicates.py:161-170); it is already tested for the same reason (tests/issue_pipeline/test_stage_predicates.py:281). No task edits `approval_record.py` or `stage_predicates.py` (plan:30, plan:173). The half "refused without a plan hash" is already true (`--plan-hash required=True`, cli.py:52: carried, not re-read). The stated check cannot pass where the plan puts it. Confidence 0.60; Variant 3 held Medium (the minority grade).
- Fix: replace the first Task 11 acceptance bullet: "`tests/issue_pipeline/test_stage_predicates.py` and `test_stage_status.py` show an approval label carrying the claim-time event id and approver id (fixture from `dispatch.json`), dated before the plan reply, gives `approved: false` and `label-before-plan`; `tests/issue_pipeline/test_approval_record.py` shows `record_create` refuses a missing or malformed plan hash and a missing adoption row. The duties text says the coordinator calls `record-create` only with evidence that `stage-status` reports as accepted." No code change; the rule exists.

<!-- Source: Variant 2 QA-3, Variant 3 M-4, Variant 1 M-5; Round 2 verdict C-004 + X-001 Blocking (Decision), 1/3 advocates agree (the unresolved point); refactor plan R-04, R-24 -->
### P4-4 BLOCKING (Decision)
- Task: Task 13. Q-1 stays PARTIAL until this is closed.
- Evidence: the pattern list at plan:202 (five new alternatives, all containing `issue-pipeline` or `issue_pipeline`) and the acceptance at plan:207 contradict each other. The matcher runs on `$T`, the command text with quotes and backslashes deleted and `/` runs squeezed (guard:428), and the coordinator-only `case` is at guard:444. A case run by the orchestrator on the real normalisation (`round2-rebuttals.md` section 1; carried, I did not re-run it): bare `p.complete.run()` (plan:207) is ALLOWED, since no `issue_pipeline` token appears; `superclaude issue-pipeline plan-hash .dev/issues/5/completed/plan.md` (must-allow at plan:207) is REFUSED by `*issue-pipeline*complete*`; `git add docs/designs/issue-pipeline-fu1.md && git commit -m "... complete ..."` is REFUSED; `sed -n`, `git diff` and `ruff check` on `issue_pipeline/complete.py` are REFUSED. The other five listed refusals and the other must-allow cases behave as the plan says. The body (plan:202) offers "record the over-match as accepted and tested" for the hyphen alternative, which contradicts the must-allow line of plan:207. The plan calls the pattern best effort (plan:202), which is true but does not rescue two acceptance lines that fail as written. Confidence 0.65. Variants 1 and 3 graded Medium, Variant 2 Blocking (Decision).
- Fix: replace `*issue-pipeline*complete*` by `*issue-pipeline[[:space:]]complete[[:space:]]*` and `*issue-pipeline[[:space:]]complete` (tested on the case run; the end-of-text form needs its own test row). Delete the option "record the over-match as accepted" at plan:202. In plan:207 replace bare `p.complete.run()` by `python -c "from superclaude.cli import issue_pipeline as p; p.complete.run()"` (matched by `*issue_pipeline*complete.run*`) and state that string-built forms (`getattr`, `importlib` with split names) are known unmatched. Add as accepted and tested over-matches: governed commands naming `issue_pipeline/complete.py` (`sed`, `git diff`, `ruff`).

<!-- Source: Variant 3 B-3 (base); Round 2 verdict C-006 Blocking (Decision), 2/3 advocates agree; refactor plan R-05 -->
### P4-5 BLOCKING (Decision)
- Task: Tasks 6, 10, 11. Affected action: Task 11's brief acceptance check, and Debug at level None.
- Evidence: Task 6 decides the brief is used only at `none`; at the other levels the launched agent runs the command from its launch prompt (plan:102). Task 11 asks the brief test to show "the limited form of `/sc:troubleshoot` at Worktree and the `--fix` form at Full and Full Submit" and has no None row (plan:177). `brief.build(issue, type_, complexity, nonce)` has no level parameter (src/superclaude/cli/issue_pipeline/brief.py:51-74) and the template substitutes only `{N}` and `{NONCE}` (brief.py:73-74), so the check has nothing to vary unless a level slot is added, which Task 6 decides against. Whether Debug at None runs `--fix` (code edits before plan approval) is untested although the brief runs before plan approval. Confidence 0.65; Variant 1 held Medium.
- Fix: Task 11 acceptance: one brief row per Status at level None, and Debug at None states whether `--fix` runs (the Task 6 table decides). Move "limited `/sc:troubleshoot` at Worktree, `--fix` at Full and Full Submit" to the launch-prompt tests of Task 7 and Task 10 (`tests/issue_watch/test_launch.py`, `tests/commands/test_issue_command.py`, `tests/skills/test_issue_protocol.py`).

### Medium

<!-- Source: Round 2 verdict A-002 / I-10 (all cards, none questioned); refactor plan R-23 -->
### P4-6 MEDIUM (not verified against the executor)
- Task: Task 4.
- Evidence: plan:73 "does not continue until the owner answers" and plan:77 "no later task that reads the value times starts". I did not read how `/sc:implement` handles an unattended stop; `~/.claude/CLAUDE.md` level 3 only says a rerun continues from the first unfinished step. None of the three cards questioned it (A-002, `diff-analysis.md`).
- Fix: Task 4: "Task 4 is a planned halt: the executor writes the owner question and the step reached into `progress.md`, ends the run with status `awaiting-owner`, and a rerun resumes at Task 4."

<!-- Source: Variant 1 M-1; Round 2 verdict C-008 Medium, 3/3 advocates agree; refactor plan R-08 -->
### P4-7 MEDIUM
- Task: Tasks 5, 7, 12.
- Evidence: `_examine` reads the items before `project_check` (src/superclaude/cli/issue_watch/cycle.py:957-958). Today `project_check` selects the one live item inside itself and returns only a reason (src/superclaude/cli/issue_watch/predicates.py:262-271). Task 5 needs the item's value times first, but the helper that returns the one live item is added in Task 7 (plan:123, plan:84), and Task 5 does not say what its predicate does for zero or several items.
- Fix: move the one-live-item helper from Task 7 to Task 5; zero or several items make the Task 5 predicate pass through so `project_check` returns `project_mismatch`; add a test; Tasks 7 and 12 reuse it.

<!-- Source: Variant 1 M-2, Variant 3 M-2; Round 2 verdict C-007 Medium, 3/3 advocates agree; refactor plan R-07 -->
### P4-8 MEDIUM
- Task: Task 7.
- Evidence: `status_report` rebuilds the retry from `launch.build_claim_prompt(n)` for entries in state `unknown` (cycle.py:1308-1314). `Entry` holds no Status, Pipeline or prompt (src/superclaude/cli/issue_watch/record.py:68-88). Task 7 requires a valid retry for every Status (plan:123, :131) but changes no store field, so a retry rebuilt from the issue number alone cannot equal the launched prompt for a non-default Status or level. It prints a command for a person to run, offline, with the gate closed, so no level above None can result; hence Medium. Confidence 0.85.
- Fix: store the launched Status and Pipeline in the pending entry (closed set); `status_report` rebuilds the retry from them and prints no command when they are absent; test: the retry argv equals the launched argv for each Status. Add `record.py` and its tests to Task 7 and to plan:30.

<!-- Source: Variant 3 M-3 (overstated; reworded per Round 2), orchestrator verification; Round 2 verdict C-011 Medium, 3/3 advocates agree; refactor plan R-09 -->
### P4-9 MEDIUM
- Task: Tasks 6, 26, 28.
- Evidence: Full Submit "runs /sc:pr-submit --monitor 3" (plan:27). The guard classes any `gh api` with a quote, `$`, a method, field or input word, `graphql` or a merge endpoint as GHWRITE (guard:553-581) and refuses GHWRITE at all four levels (guard:798). The pr-submit wrapper scripts (`reply-resolve-thread.sh:73,131,141`, `refs/thread-reply.md:12,47,67`, `refs/review-retrigger.md:27`; carried, not re-read) run as `bash <script>`, so the guard sees only that command text and not the writes inside them (text-only limit, plan:24). Inline forms are refused at every level. `gh pr create` and `gh pr ready` are SUBMIT and pass at Full Submit (guard:653, guard:790). The earlier remediation recorded this as "out of scope, flagged" (`remediation-proposal.md:132`, carried) and the plan drops the flag. Variant 3's "refuses both" overstated the wrapper path; true for inline use.
- Fix: one sentence in Task 6 and Task 26: "At Full Submit the guard refuses inline `gh api` writes and any `gh api` command containing a quote or `$`; the pr-submit wrapper scripts are not seen (text-only). Before the gate flips, run `/sc:pr-submit --monitor 3` end to end at Full Submit under the guard." Add it to Task 28's open decisions. Not "pr-submit is refused".

<!-- Source: Variant 2 QA-4; Round 2 verdict C-014 Medium, 2/3 advocates agree (Variant 2 argued Blocking (Decision)); refactor plan R-10 -->
### P4-10 MEDIUM
- Task: Tasks 19, 24.
- Evidence: Task 19 lets several Projects pass when the defaults map names one (plan:268); Task 24 says "the Project count is exactly one (Task 19 rule)" (plan:323); Task 24's acceptance has no zero or several Project case (plan:328) although R14 asks for it (`source.md:34`). A mapped multi-Project repo that the generator accepts is skipped by every sweep. It fails closed and no stated check breaks.
- Fix: Task 24 rule: the check passes when the config's `project_id` is one of the repo's Projects (exactly one, or one chosen by the defaults map); otherwise it reports `project_missing` or `project_ambiguous`. Add existing-config cases for zero, several and mapped Projects (no child starts on refusal). Replace "(Task 19 rule)" with the real rule.

<!-- Source: Variant 2 QA-1; Round 2 verdict C-005 Medium (Variant 2 and the arbiter-contested Blocking (Missing) not adopted), 2/3 advocates agree; refactor plan R-06 -->
### P4-11 MEDIUM
- Task: Task 27.
- Evidence: `source.md:36` (R6: install cron, start the daemon at every boot from `startup.sh`, keep exactly one entry on every boot because the crontab and `/etc` are outside the persisted volume) and `source.md:40` (R9: check the `Coordinator` branch, worktree and running session at boot and on every watcher run, create what is missing, restart a stopped session). Task 27's content list (plan:356) has the cron line, defaults file, branch and worktree rules, session name and launch text, credential row, guard install step and the R20 note, but none of the lifecycle clauses. The deliverable is present, under-specified, not absent: R6 and R9 are filed as Coder issues 515 and 516 (`source.md:36,40`) and plan:361 requires a row for each. Confidence 0.60.
- Fix: add to the content list "R6: install the cron package, start the daemon at every boot from `startup.sh`, ensure exactly one watcher entry on every boot (crontab and `/etc` are outside the persisted volume)" and "R9: at boot and on every watcher run check the `Coordinator` branch, worktree and running session `COORD-<RepoName>`, create what is missing, restart a stopped session"; acceptance: `grep -c` finds each clause.

### Notes

<!-- Source: Variant 3 M-5; Round 2 verdict C-012 Note, 3/3 agree; folds A-004 (claim session ungoverned) and A-003 (text-only guard), already stated at plan:24-25; refactor plan R-14, R-26, R-27 -->
### P4-12 NOTE
- Task: Goal (plan:15).
- Evidence: plan:15 "A launched agent can never write to an issue, a label or a Project at any level" against plan:24-25 (the check is text-only; the claim session at level None is not governed and posts two comments; the coordinator is not governed).
- Fix: "An agent launched at Worktree, Full or Full Submit is refused `gh issue`, `gh label` and `gh project` writes by a text check; the claim session at level None and the coordinator are not governed (plan:24-25)."

<!-- Source: Variant 3 N-2; refactor plan R-19 -->
### P4-13 NOTE
- Task: Task 5.
- Evidence: plan:84 says "one-second resolution, line 257". `unchanged_since` compares raw datetimes (predicates.py:257); the whole-second truncation is in `parse_utc` (predicates.py:24) and `approval_of` (predicates.py:181-182, :205); those three lines are carried, not re-read.
- Fix: name `parse_utc` (whole seconds) as the source of the resolution; state that `unchanged_since` compares raw datetimes (:257) and `approval_of` truncates.

<!-- Source: Variant 1 M-4 [INFERRED]; Round 2 verdict C-013 Note, 3/3 agree, confidence 0.50; refactor plan R-15 -->
### P4-14 NOTE [INFERRED]
- Task: Task 8.
- Evidence: `level_gated` is a skip raised in `_examine`, and the Pipeline value is known only after the last read (cycle.py:957). A gated issue is re-examined every cycle at a cost of about four reads, bounded by the 35-call cap with 3 reserved (github.py:46-49); the failure is closed.
- Fix: one design-note sentence that a gated issue is re-examined every cycle at a cost of about four reads; no reorder.

<!-- Source: Variant 1 M-3, Variant 3 N-1; Round 2 verdict C-009 Note, 2/3 agree; refactor plan R-12 -->
### P4-15 NOTE
- Task: Task 9.
- Evidence: plan:149 cites `self.account_id` for the `check-config` warning. That is set at run time from the `gh` user read (cycle.py:766-767) and `check-config` is offline; the config's own value is `Config.owner_account_id`, optional (cycle.py:104, :768). The sentence says "the config's own account id", so intent is clear and the cite is wrong; the null case is unsaid.
- Fix: cite `Config.owner_account_id`, not `self.account_id`; state that a null id prints no warning (and one info line).

<!-- Source: Variant 3 (Q-6 PARTIAL), orchestrator X-002; Round 2 verdict X-002 Note (PARTIAL), 2/3 agree; refactor plan R-16 -->
### P4-16 NOTE
- Task: Task 12. Closes Q-6.
- Evidence: Task 12 has the string test that the result marker does not contain the claim marker (plan:191). `marker_comments` selects with `contains(CLAIM_MARKER)` (github.py:61-63), so the property follows, but the earlier proposal's named test "`marker_comments` evidence ignores a result comment" (`remediation-proposal.md:205`, carried) is not a reader-level assertion in the plan.
- Fix: one assertion in `test_complete.py` or `test_github.py` that `marker_comments` evidence ignores a result-marker comment.

<!-- Source: Variant 1 N-1 + Variant 3 test pins; refactor plan R-17 -->
### P4-17 NOTE
- Task: Task 13.
- Evidence: `GRID_CLASSES` is at tests/hooks/test_launch_level_guard.py:775, the import-time assert `set(GRID_CLASSES) | {"NONE"} == set(EXPECTED)` at :843, and `len(set(GRID_CLASSES)) == 16` at :3391 (re-read by Grep in this run). Plan:205 names only "the expected-result grid".
- Fix: name all three pins in the acceptance: the class list, the import-time assert and the count.

<!-- Source: Variant 1 N-2, Variant 3 N-3; refactor plan R-18 -->
### P4-18 NOTE
- Task: Task 13.
- Evidence: `docs/architecture/SUPERVISED-ORCHESTRATION-TECHNICAL-REFERENCE.md` lines 1070 and 1443 matched a version grep for cards 1 and 3. A Grep for "version 1" and "guard version" in this run did not surface those two lines; the matched text is not confirmed (carried, unverified).
- Fix: read lines 1070 and 1443; if they quote guard version 1, add them to the bump list at plan:202.

<!-- Source: Variant 3 N-4; refactor plan R-20 -->
### P4-19 NOTE
- Task: Task 13.
- Evidence: the new `ISSUE` row is meant to fire wherever `gh` appears (plan:202). The H3 case runs on the words of a segment (guard:626-655) and the SUBMIT row already over-matches outside command position the same way; plan:202 does not list this for ISSUE.
- Fix: list as an accepted, tested over-match that the ISSUE class fires on a `gh issue|label|project` word outside command position (a commit message, `grep`).

<!-- Source: Variant 3 N-5; refactor plan R-21 -->
### P4-20 NOTE
- Task: Task 19.
- Evidence: plan:275 says Task 19's argv builders "are covered by the scan Task 12 extends", but `tests/issue_watch/test_security_invariants.py` is not among Task 19's files (plan:30 lists it for Tasks 3, 7, 12, 15).
- Fix: add `tests/issue_watch/test_security_invariants.py` to Task 19's files or state that the scan finds modules generically.

<!-- Source: Variant 3 M-1 (graded Note by the arbiter); Round 2 verdict C-010 + X-003 Note, 2/3 agree; refactor plan R-13 -->
### P4-21 NOTE
- Task: plan:30 (Tasks 2, 7, 10, 11, 14, 16). Closes Q-10 (PARTIAL).
- Evidence: plan:30 lists `WORKER-CONTRACT.md` for Tasks 11 and 14 only, but plan:161 gives it to Task 10 as well, and Tasks 2 and 10 both edit the two design docs (plan:48, plan:161). Tasks 10 and 11 have identical dependencies (plan:159, plan:171). The same line says "Tasks that edit the same file run in plan order, never in parallel", which covers the omitted pairs; hence Note, not Medium.
- Fix: add `WORKER-CONTRACT.md` (Tasks 10, 11, 14), `docs/designs/issue-watcher.md` and `issue-watcher-setup.md` (Tasks 2, 10, 26), `issue_pipeline/cli.py` (Tasks 14, 16) and `record.py` (Task 7) to plan:30; or add "Depends on: Task 2" to Task 10 and "Task 10" to Task 11.

<!-- Source: Round 2 shared assumption A-001 (all three cards; stated as "not checked" by each); refactor plan R-25 -->
### P4-22 NOTE
- Task: plan risks (plan:125, plan:161).
- Evidence: all three cards carried line numbers from plan v3 and the proposal for `guard`, `cycle.py`, `predicates.py`, `github.py` and the tests and each lists them as not checked; no plan risk line says to re-read them. A counter-example already in the plan: plan:84 "one-second resolution" (P4-13).
- Fix: add a plan risk line: "line numbers carried from v3 were re-read for the guard, `cycle.py`, `predicates.py`, `github.py`; re-run Grep before editing (plan:125, :161)."

## Convergence and the unresolved point

Convergence 13.33 of 17 points = 0.784 against a threshold of 0.80: NOT_CONVERGED, by 1.6 points (`adversarial/adversarial/debate-transcript.md`, `round2-rebuttals.md` section 3). Two rounds were run; no round 3. C-004 (P4-4) alone decides it: only Variant 2 held Blocking (1 of 3 advocates); had C-004 been graded Medium the figure would be 0.804. The advocates agree on the facts almost everywhere (every C point TRUE; C-013 inferred); the disagreement is how to read "changes an acceptance check". The arbiter's reading: an acceptance check already in the plan that cannot pass as written, or contradicts another named item, is Decision; a missing extra test or a wrong pointer that leaves every stated check passable is Medium or Note. Under that reading P4-4 (plan:202 vs plan:207), P4-3 and P4-5 are Decision. Under the narrower reading in which a best-effort pattern's failure cannot be Blocking, P4-4 would be Medium. The grade stays Blocking (Decision), confidence 0.65, set by the arbiter. This verdict is advice and the grade of P4-4 is the one open point.

## Decisions needed from the owner

None. P4-1 states an alternative (serve only IronClaude until the repo is threaded), but the plan already scopes the work to IronClaude (plan:19), so it is an implementer choice, not an owner decision. The reading of "changes an acceptance check" in P4-4 is an arbiter call recorded above.

## No-finding list

<!-- Source: Variant 1 Checked line; Round 2 verification -->
- Variant 1 found and Round 2 left standing: the guard line numbers 10, 70-71, 444, 652-654, 764, 786, 790 and 798, the `cycle.py` ordering (949-961, 1007-1016, 1054-1058) and the test-file line cites. Within this run I re-read guard:425-448, :548-582, :624-656, :786-801 and `cycle.py` :95-108, :764-770, :953-961, :1300-1317.
<!-- Source: Variant 3 Q-list and fixed-line citations; refactor plan R-22 -->
- Q-2 (ship gate, Task 8), Q-4 (reason order, plan:123), Q-5 (Task 12), Q-7, Q-8 and Q-9 were found fixed by the cards and not contradicted by the debate.
- Task split: no finding. Tasks 7 and 13 are large but a split leaves the suite red between tasks (Variant 3 N-6); keep both whole. The other 26 tasks have a single purpose.
- Coverage: R1 to R33 each map to a task; no orphan task. Variant 2 marks R6, R9, R14, R29 and R33 partial: R6 and R9 are P4-11, R14 is P4-10, R29 is P4-3, and R33 follows P4-4 and P4-15.
- Shared assumption A-005 (fakes only, so a cross-repo defect shows no failing test) is partly false: the plan has live read-only checks (plan:22, plan:61, plan:73). The real gap is the missing second-repo test, covered by P4-1.
- No contradictions were introduced by the merge (re-scan in `merge-log.md`).

## Not checked

<!-- Source: Variant 1, 2, 3 Not-checked lines; refactor plan R-31 -->
- Not read by any card: `audit.py` row counts, `tests/issue_watch/test_security_invariants.py:911-919`, `record.py:545`, `orca_worktree.py:986`, live GitHub timestamp behaviour (the Task 4 observation settles it at run time), cron authentication, and how `/sc:implement` stops on an owner step (P4-6).
- `approval_record.py` was read only by Variant 3 and the orchestrator (P4-3), and by me at lines 310-361.
- Variant 3 only: the H3 handling of `gh project item-edit` (assumed UNKNOWN), the DF-14 rationale, the grounding artifact, full `launch.py` and `github.py`.
- Variant 1: `docs` line cites for Task 2, the 45-line `--pipeline none` count, `test_security_invariants.py:712-730`, the `pr-submit` flow under the new ISSUE class.
- The orchestrator did not run the repo test suite; the guard case run of P4-4 covered the matcher text only, not the full hook, and I did not repeat it (carried).
- Carried, not re-read by me: `cli.py:52` and `cli.py:134-158`, `test_stage_status.py:63`, `predicates.py:24,181-182,205`, the pr-submit wrapper and refs lines of P4-9, `remediation-proposal.md:132,205`, and the two doc lines of P4-18.
