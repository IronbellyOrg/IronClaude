# Refactoring Plan: Merge into Base (Variant 3, reviewer-3 card)

## Overview
- Base: Variant 3 (`reviewer-cards/reviewer-3-card.md`, refactorer, opus), final score 0.906 (`base-selection.md`).
- Incorporating strengths from: V2 (`reviewer-2-card.md`) and V1 (`reviewer-1-card.md`), plus orchestrator verification (`round2-rebuttals.md`).
- Planned changes: 31 register rows (R-01 to R-31): 5 Blocking (R-01 to R-05), 6 Medium (R-06 to R-10 and R-23), the rest Notes, status tables and not-checked lists. The merge executor writes ONE register in the base's B/M/N format, ordered by grade then plan task.
- Risk level: Low overall. This is a review register, not plan code; no plan or production file is edited by the merge.
- Plan under review: `.dev/tasks/to-do/TASK-WF-requirements-20261119-140750/TASK-WF-requirements-20261119-140750.md` (`plan:N`). `guard` = `src/superclaude/hooks/scripts/launch-level-guard.sh`.
- Grades follow the owner's rule. Convergence 0.784, NOT_CONVERGED (threshold 0.80); the arbiter's grade is final where advocates split (`round2-rebuttals.md` section 3).

## Planned Changes (one register row each: id, source cards, final grade, plan task, fix text)

### Blocking

**R-01 | C-001 | V3 B-1 (V1/V2 missed; all three advocates agree) | Blocking (Safety) | Tasks 15, 16, 11, 14, 23**
Affected action: the coordinator's plan-approval gate for any repo other than IronClaude. Evidence: `src/superclaude/cli/issue_pipeline/cli.py:279,282,343-348`, `reads.py:67,142,148`, `github.py:37,75,89`, plan:227, plan:238, plan:313, `WORKER-CONTRACT.md:242,293-298`.
Fix: Task 16 (add `src/superclaude/cli/issue_pipeline/cli.py`, `reads.py` and their tests to its files; `stage-status` takes `--repo`, default the `repo` key of the chosen `--config`; pass it to `gh.reread`, `read_stage_evidence`, `gh.events`, `gh.edits` and the comments read; Task 15 gives `argv_comments_projected` and `read_stage_evidence` a `repo` parameter). Test: with a second repo every argv carries that repo and none carries `IronbellyOrg/IronClaude`; an approval label on the IronClaude issue of the same number never approves the other repo's issue. Task 11: reword `WORKER-CONTRACT.md:242` to "the repo the issue belongs to, never the SuperClaude upstream" (and `:293` "covers claims at every level" already planned). Alternative if not done: Task 23 serves only `IronbellyOrg/IronClaude` until it is. Add `issue_pipeline/cli.py` (Tasks 14, 16) to plan:30.

**R-02 | C-002 | V3 B-2 | Blocking (Decision) | Tasks 3, 5**
Affected action: the void rule for an empty Pipeline, the only level the closed gate lets launch. Evidence: `github.py:764-775`, plan:61, :65, :84, :87-88, :95.
Fix: Task 3: "An absent Pipeline value is `pipeline_name = None`, `pipeline_changed_at = None` and means no time, not unreadable; a malformed time fails the whole read." Task 5: "the later of the value times that exist; an absent Pipeline contributes none; a Status name with no Status time refuses." Acceptance rows: empty Pipeline with a Status time before the approval passes and launches with `--pipeline none`; a malformed time gives the read refusal; a Pipeline cleared after approval launches at None (lowest level, no authority raised) and the design note says so; a Pipeline value changed after approval refuses.

**R-03 | C-003 | V2 QA-2 (V3 located the rule) | Blocking (Decision) | Task 11**
Evidence: `approval_record.py:313-359` (no discriminator), `stage_predicates.py:161-170` (rule exists), `test_stage_predicates.py:281`, plan:176.
Fix: replace the first Task 11 acceptance bullet: "`tests/issue_pipeline/test_stage_predicates.py` and `test_stage_status.py` show an approval label carrying the claim-time event id and approver id (fixture from `dispatch.json`), dated before the plan reply, gives `approved: false` and `label-before-plan`; `tests/issue_pipeline/test_approval_record.py` shows `record_create` refuses a missing or malformed plan hash and a missing adoption row. The duties text says the coordinator calls `record-create` only with evidence that `stage-status` reports as accepted." No code change; the rule exists.

**R-04 | C-004 + X-001 | V2 QA-3, V3 M-4, V1 M-5 | Blocking (Decision) | Task 13**
Evidence: case run on the real normalisation (`round2-rebuttals.md` section 1): bare `p.complete.run()` allowed; `plan-hash` with a `completed` path refused; `git commit -m "... complete ..."`, `sed`/`git diff`/`ruff` on `issue_pipeline/complete.py` refused; plan:202 vs plan:207.
Fix: replace `*issue-pipeline*complete*` by `*issue-pipeline[[:space:]]complete[[:space:]]*` and `*issue-pipeline[[:space:]]complete` (tested form; add a test row for end of text); delete the option "record the over-match as accepted" at plan:202; in plan:207 replace bare `p.complete.run()` by `python -c "from superclaude.cli import issue_pipeline as p; p.complete.run()"` and state that string-built forms (`getattr`, `importlib` with split names) are known unmatched; add as accepted and tested over-matches: governed commands naming `issue_pipeline/complete.py` (`sed`, `git diff`, `ruff`). Q-1 stays PARTIAL until then.

**R-05 | C-006 | V3 B-3 | Blocking (Decision) | Tasks 6, 10, 11**
Evidence: plan:102 vs plan:177; `brief.py:51-74` has no level parameter; template slots `{N}`, `{NONCE}` only.
Fix: Task 11 acceptance: one brief row per Status at level None, and Debug at None states whether `--fix` runs (Task 6 table decides; the brief runs before plan approval). Move "limited `/sc:troubleshoot` at Worktree, `--fix` at Full and Full Submit" to the launch-prompt tests of Task 7 and Task 10 (`tests/issue_watch/test_launch.py`, `tests/commands/test_issue_command.py`, `tests/skills/test_issue_protocol.py`).

### Medium

**R-06 | C-005 | V2 QA-1 | Medium | Task 27** (V2 and A2 argued Blocking (Missing); arbiter Medium)
Evidence: `source.md:36,40`, plan:356-363; issues 515 and 516 hold the text.
Fix: add to the content list "R6: install the cron package, start the daemon at every boot from `startup.sh`, ensure exactly one watcher entry on every boot (crontab and `/etc` are outside the persisted volume)" and "R9: at boot and on every watcher run check the `Coordinator` branch, worktree and running session `COORD-<RepoName>`, create what is missing, restart a stopped session"; acceptance: `grep -c` finds each clause.

**R-07 | C-007 | V1 M-2, V3 M-2 | Medium | Task 7**
Evidence: `cycle.py:1308-1314`, `record.py:68-88`, plan:123, :131.
Fix: store the launched Status and Pipeline in the pending entry (closed set); `status_report` rebuilds the retry from them and prints no command when absent; test: the retry argv equals the launched argv for each Status. Add `record.py` and its tests to Task 7 and to plan:30.

**R-08 | C-008 | V1 M-1 | Medium | Tasks 5, 7, 12**
Evidence: `cycle.py:957-958`, `predicates.py:262-271`, plan:84, :123.
Fix: move the one-live-item helper from Task 7 to Task 5; zero or several items make the Task 5 predicate pass through so `project_check` returns `project_mismatch`; add a test; Tasks 7 and 12 reuse it.

**R-09 | C-011 | V3 M-3 | Medium | Tasks 6, 26, 28**
Evidence: `guard:553-582,653,790,798`; `scripts/reply-resolve-thread.sh:73,131,141`; `refs/thread-reply.md:12,47,67`; `refs/review-retrigger.md:27`; `remediation-proposal.md:132`.
Fix: one sentence in Task 6 and Task 26: "At Full Submit the guard refuses inline `gh api` writes and any `gh api` command containing a quote or `$`; the pr-submit wrapper scripts are not seen (text-only). Before the gate flips, run `/sc:pr-submit --monitor 3` end to end at Full Submit under the guard." Add it to Task 28's open decisions. Not "pr-submit is refused".

**R-10 | C-014 | V2 QA-4 | Medium | Tasks 19, 24**
Evidence: plan:268, :323, :328, `source.md:34`.
Fix: Task 24 rule: the check passes when the config's `project_id` is one of the repo's Projects (exactly one, or one chosen by the defaults map); otherwise it reports `project_missing` or `project_ambiguous`. Add existing-config cases for zero, several and mapped Projects (no child starts on refusal). Replace "(Task 19 rule)" with the real rule.

**R-11 | Q-6 gap (X-002) | V3 | Medium by V3, Note by arbiter | Task 12** — graded Note, see R-16.

### Notes and card-only items

**R-12 | C-009 | V1 M-3, V3 N-1 | Note | Task 9**
Fix: cite `Config.owner_account_id` (optional, `cycle.py:97-107,768`), not `self.account_id` (`cycle.py:767-768`, runtime); state that a null id prints no warning (and one info line).

**R-13 | C-010 + X-003 | V3 M-1 | Note | plan:30 (Tasks 2, 10, 11, 14)**
Fix: add `WORKER-CONTRACT.md` (Tasks 10, 11, 14), `docs/designs/issue-watcher.md` and `issue-watcher-setup.md` (Tasks 2, 10, 26), `issue_pipeline/cli.py` (Tasks 14, 16), `record.py` (Task 7); or add "Depends on: Task 2" to Task 10 and "Task 10" to Task 11.

**R-14 | C-012 | V3 M-5 | Note | Goal (plan:15)**
Fix: "An agent launched at Worktree, Full or Full Submit is refused `gh issue`, `gh label` and `gh project` writes by a text check; the claim session at level None and the coordinator are not governed (plan:24-25)."

**R-15 | C-013 | V1 M-4 [INFERRED] | Note | Task 8**
Fix: design-note sentence that a gated issue is re-examined every cycle at a cost of about four reads (the Pipeline is known only after the last read, `cycle.py:957`); no reorder.

**R-16 | X-002 (Q-6) | V3 | Note | Task 12**
Fix: one assertion in `test_complete.py` or `test_github.py`: `marker_comments` evidence ignores a result-marker comment (`remediation-proposal.md:205`; property follows from `github.py:61-63` plus plan:191).

**R-17 | V1 N-1 + V3 test pins | Note | Task 13**
Evidence: `tests/hooks/test_launch_level_guard.py:775,843`; `len(set(GRID_CLASSES)) == 16` at `:3391` (A3). Fix: name all three pins in the acceptance: the class list, the import-time assert and the count.

**R-18 | V1 N-2, V3 N-3 | Note | Task 13**
Fix: read `docs/architecture/SUPERVISED-ORCHESTRATION-TECHNICAL-REFERENCE.md` lines 1070 and 1443; if they quote guard version 1, add them to the bump list.

**R-19 | V3 N-2 | Note | Task 5** Fix: change "one-second resolution, line 257" to name `parse_utc` (whole seconds, `predicates.py:24`); `unchanged_since` compares raw datetimes (`:257`) and `approval_of` truncates (`:181-182,205`).

**R-20 | V3 N-4 | Note | Task 13** Fix: list as an accepted, tested over-match that the ISSUE class fires on a `gh issue|label|project` word outside command position (commit message, `grep`), as the SUBMIT row already does (`guard:626-653`).

**R-21 | V3 N-5 | Note | Task 19** Fix: add `tests/issue_watch/test_security_invariants.py` to Task 19's files or state that the scan finds modules generically.

**R-22 | V3 N-6 | Note | split** Fix: none; keep Tasks 7 and 13 whole (a split leaves the suite red).

**R-23 | A-002 / I-10 | all cards (none questioned) | Medium (not verified against the executor) | Task 4**
Fix: "Task 4 is a planned halt: the executor writes the owner question and the step reached into `progress.md`, ends the run with status `awaiting-owner`, and a rerun resumes at Task 4."

**R-24 | V1 M-5 (guard over-matches, pins) | Note | Task 13** — merged into R-04 (accepted over-matches); kept as a pointer only.

**R-25 | A-001 | all cards | Note | plan risks** Fix: add a plan risk line "line numbers carried from v3 were re-read for the guard, `cycle.py`, `predicates.py`, `github.py`; re-run Grep before editing (plan:125, :161)". A2's counter-example: plan:84 "one-second resolution".

**R-26 | A-003 (text-only guard) | V1, V3 | Note** — already stated at plan:24 and :202; no change.

**R-27 | A-004 (claim session ungoverned) | V1, V3 | Note** — stated at plan:25; fold into R-14.

**R-28 | A-005 (fakes only) | all | Note** — partly false (live read-only checks at plan:22, :61, :73); the real gap is the missing second-repo case, covered by R-01.

**R-29 | Q-1 to Q-10 recheck | Status table** for the merged register: Q-1 PARTIAL (R-04), Q-2 FIXED, Q-3 FIXED with R-02, Q-4 FIXED, Q-5 FIXED, Q-6 PARTIAL-Note (R-16), Q-7 FIXED, Q-8 FIXED, Q-9 FIXED, Q-10 PARTIAL-Note (R-13). Decisions: ship gate FIXED, `updatedAt` observation FIXED, self-approval warn-only FIXED with R-12, tamper token FIXED, four pipelines end at In review FIXED, extra guard refusals PARTIAL (R-04, R-20).

**R-30 | Coverage | V1, V2, V3** R1 to R33 each map to a task; no orphan task; V2 marks R6, R9, R14, R29, R33 partial: R6/R9 = R-06, R14 = R-10, R29 = R-03, R33 follows R-04/R-12.

**R-31 | Not checked by any card (carry as "not checked")** `audit.py` row counts, `test_security_invariants.py:911-919`, `record.py:545`, `orca_worktree.py:986`, `approval_record.py` (V3 only now read), live GitHub timestamp behaviour, cron authentication, executor stop behaviour (R-23). The orchestrator did not run the test suite.

## Changes NOT Being Made (with rationale)

| Diff Point | Non-Base Approach | Rationale for Keeping Base |
|---|---|---|
| C-003 grade | V3: Medium | Arbiter Blocking (Decision): plan:176 as written cannot pass; V3's location of the real rule is merged as the fix |
| C-005 grade | V2: Blocking (Missing) | The handoff exists; issues 515 and 516 hold the text; Medium |
| C-014 grade | V2: Blocking (Decision) | Fails closed, no stated check breaks; Medium |
| C-010 grade | V3: Medium | The general "plan order" rule in plan:30 covers omitted pairs; Note |
| C-011 wording | V3 M-3 "refuses both" | Wrapper scripts are not seen by the guard; reworded to a recorded limit |
| X-001 | V3: FIXED | Overruled by the case run |
| X-002 | V2: Blocking | Property follows from the string test; Note |
| C-009 | V3: Medium | Intent is clear; Note |

## Risk Summary

| Change # | Risk | Impact if Failed | Rollback |
|---|---|---|---|
| R-01 to R-05 | Medium | A Blocking finding is dropped or mis-graded in the merged register | Restore the row from this file |
| R-06 to R-10 | Low | Medium finding lost | Re-add the row |
| R-12 to R-31 | Low | Note lost | none needed |

## Review Status
- [x] Auto-approved (default)
- [ ] User-approved (--interactive)
- Approved by: auto
- Approval timestamp: 2026-11-19
