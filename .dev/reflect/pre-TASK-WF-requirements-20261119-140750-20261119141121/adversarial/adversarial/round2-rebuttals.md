# Round 2: rebuttals and verdicts (orchestrator-verified)

Plan = `.dev/tasks/to-do/TASK-WF-requirements-20261119-140750/TASK-WF-requirements-20261119-140750.md` (`plan:N`). Advocates: A1 = `round1-advocate-1.md` (card 1), A2 = `round1-advocate-2.md` (card 2), A3 = `round1-advocate-3.md` (card 3). `guard` = `src/superclaude/hooks/scripts/launch-level-guard.sh`. Every `file:line` below was read in this round (paths relative to the worktree root).

Grading rule used (owner's): Blocking only if the fix changes a named decision, a required behaviour or an acceptance check (Decision), a required deliverable is absent (Missing), or following the plan breaks a safety boundary (Safety); else Medium (real weakness, nothing named rests on it) or Note (form only).

How I read "changes an acceptance check" (the crux of C-003, C-004, C-006): an acceptance check that already stands in the plan and cannot pass as written, or contradicts another named item, is Decision. A missing extra test, or a wrong pointer that leaves every stated check passable, is Medium or Note. I apply this the same way to every point.

## 1. The two factual disputes, settled by reading and by running

### C-003: does the refusal rule exist, and is Task 11's test in the right file?

Read: `src/superclaude/cli/issue_pipeline/stage_predicates.py:145-189` (`_label_channel`), `src/superclaude/cli/issue_pipeline/approval_record.py:313-371` (`record_create`), `src/superclaude/cli/issue_pipeline/cli.py:134-158` (`record-create` verb), `tests/issue_pipeline/test_stage_predicates.py:281`, `tests/issue_pipeline/test_stage_status.py:63`.

- The rule exists. `stage_predicates.py:161-170`: a label counts only if `e.event == "labeled" and e.created_at > reply.created_at`; with none after the plan reply the channel is refused with `label-before-plan` (when a label exists earlier) or `no-label`. `evaluate` (`:279`) sets `approved` only from an accepted channel. A claim-time approval label always predates the plan reply, so it is refused as plan approval there. A test for exactly that reason already exists (`test_stage_predicates.py:281`: `status.label.reason == "label-before-plan"`).
- `record_create` has no way to tell a claim-time event from a plan one. Its inputs are a plan hash, a channel (checked against `CHANNELS`), an evidence id and an actor, each only pattern-checked (`:331-335`); the only state check is that an adoption row exists (`:337-338`). The CLI verb passes the caller's `--evidence-id` straight in (`cli.py:154-158`).
- Task 11's acceptance (`plan:176`) puts "a claim-time event is refused as plan approval" in `tests/issue_pipeline/test_approval_record.py`. Nothing in `record_create` can refuse it, and no task edits `approval_record.py` or `stage_predicates.py` (plan:30, plan:173). The half "refused without a plan hash" is already true (`cli.py:52` `--plan-hash required=True`).
- So both cards are partly right. A3 is right that the enforcement point exists and no code change is needed. A2 is right that the stated check cannot pass where the plan puts it. Under the reading above this is Decision: the check has to be re-pointed at `stage_predicates.evaluate` / `stage-status`, using a claim-time event id from a `dispatch.json` fixture.

Rebuttals (from Round 1 evidence only):
- A2 for Blocking: `record_create` takes "a hash, channel, evidence id and actor"; "adding a syntactically valid hash to claim evidence is not distinguished here" (A2 C-003, citing `approval_record.py:313-359`). A test that fails only on a missing hash proves half of the sentence.
- A3 for Medium: "An enforcement point does exist, just not in `approval_record.py`: `stage_predicates._label_channel` ... `label-before-plan` (`stage_predicates.py:161-170`) ... The defect is that Task 11 places the test in `test_approval_record.py`" (A3 section 2). The fix does not change a decision.

Verdict: **Blocking (Decision), confidence 0.60.** Deciding evidence: `plan:176` names a check that `record_create` (`approval_record.py:313-359`) cannot satisfy, and the rule that can satisfy it lives in `stage_predicates.py:161-170`. The fix is small and needs no new code. A3's Medium is the minority grade; it would be right if the executor were told to read plan:176 loosely, but the plan says "A test in `tests/issue_pipeline/test_approval_record.py`".

### C-004: does the guard see the listed spellings?

Read: `guard:415-448` (normalisation, `T`, line 444 pattern), `guard:548-582` (GHWRITE), `guard:597-660` (H3), plan:202 and plan:207, `remediation-proposal.md:120,127,132`.

Facts on the matcher: the coordinator-only `case` at `guard:444` runs on `$T`, the whole command text with quotes and backslashes deleted and `/` runs squeezed (`guard:428`). No `issue_pipeline`/`issue-pipeline` token needs to start a word; each alternative is a substring glob over the whole text. I ran the real normalisation (the `sed` of `guard:428`, copied verbatim) and a `case` with the five alternatives of Task 13 (plan:202), in a private `/tmp` directory removed afterwards. Existing line-444 alternatives matched none of the spellings (`old=N` every row). Results (A1..A5 are the five new alternatives in the order of plan:202):

| Spelling | Plan wants | Result | Matched by |
|---|---|---|---|
| `superclaude issue-pipeline complete --repo o/r --issue 5` | refuse | REFUSE | A1 `*issue-pipeline*complete*` |
| `uv run superclaude issue-pipeline complete --repo o/r --issue 5` | refuse | REFUSE | A1 |
| `python -m superclaude.cli.issue_pipeline.complete` | refuse | REFUSE | A2 `*issue_pipeline.complete*` |
| `from superclaude.cli.issue_pipeline import complete` | refuse | REFUSE | A4 `*issue_pipeline*import*complete*` |
| `from superclaude.cli.issue_pipeline.complete import run` | refuse | REFUSE | A2 |
| **`p.complete.run()` (bare, plan:207)** | refuse | **ALLOW** | none (no `issue_pipeline` in the text) |
| `python -c "from superclaude.cli.issue_pipeline import complete; complete.run()"` | refuse | REFUSE | A4, A5 |
| `python -c "from superclaude.cli import issue_pipeline as p; p.complete.run()"` | refuse | REFUSE | A5 `*issue_pipeline*complete.run*` |
| `python -c "import superclaude.cli.issue_pipeline as p; p.complete.run()"` | refuse | REFUSE | A5 |
| `python -c "import superclaude.cli.issue_pipeline.complete as c; c.run()"` | refuse | REFUSE | A2 |
| `importlib.import_module("superclaude.cli.issue_pipeline.complete")` | refuse | REFUSE | A2 |
| `exec(open("src/superclaude/cli/issue_pipeline/complete.py").read())` | refuse | REFUSE | A3 |
| `getattr(p, "comp"+"lete").run()` | known miss | ALLOW | none (text-only limit, `remediation-proposal.md:132`) |
| `superclaude issue-pipeline plan-hash .dev/issues/5/plan.md` | allow | ALLOW | |
| `superclaude issue-pipeline check-approval --issue 5` | allow | ALLOW | |
| `uv run pytest tests/issue_pipeline/test_complete.py` | allow | ALLOW | |
| `uv run pytest tests/issue_pipeline/test_complete_cli.py` | allow | ALLOW | |
| **`superclaude issue-pipeline plan-hash .dev/issues/5/completed/plan.md`** | allow (plan:207) | **REFUSE** | A1 |
| `git add docs/designs/issue-pipeline-fu1.md && git commit -m "docs: complete the fu1 design"` | not listed | REFUSE | A1 |
| `sed -n 1,20p src/superclaude/cli/issue_pipeline/complete.py`, `git diff -- ...complete.py`, `uv run ruff check ...complete.py` | not listed | REFUSE (all three) | A3 |
| `uv run pytest tests/issue_pipeline -q`, `grep -n complete src/superclaude/cli/issue_pipeline/cli.py` | not listed | ALLOW | |

Two checks in the plan's own acceptance (plan:207) fail with the plan's own alternatives: the bare `p.complete.run()` is not refused, and `plan-hash` with a path containing "completed" is refused. The body (plan:202) offers "record the over-match as accepted and tested" for the hyphen alternative, which contradicts the must-allow line of plan:207. I also tested a fix: replacing A1 with `*issue-pipeline[[:space:]]complete[[:space:]]*` (plus the end-of-text form `*issue-pipeline[[:space:]]complete`): refuses the two verb spellings, allows `plan-hash` for a `completed` path and the `git commit -m "... complete ..."` case (all tested; the end-of-text form follows from the pattern and needs its own test row). Bare `p.complete.run()` cannot be matched without a pattern like `*complete.run*`, which over-matches; the sound fix is to replace that case by a full statement that imports the module (A5 matches it).

Rebuttals (from Round 1 evidence only):
- A2 for Blocking: "`:202` adds five alternatives, all containing `issue-pipeline` or `issue_pipeline`. Its `:207` requires bare `p.complete.run()` to produce the tamper code, although neither token is present ... This is a literal mismatch, not speculation about an exotic bypass" (A2 C-004). Best-effort status "does not excuse failing an explicitly enumerated test".
- A3 for Medium: "A real command that runs `p.complete.run()` must import the module first, for example `python -c "from superclaude.cli import issue_pipeline as p; p.complete.run()"`. That text contains `issue_pipeline` and `complete.run`, so it matches" (A3 section 2); "It is not Blocking, because the plan calls the pattern best effort and not a control (`plan:202`)" (A3 C-004).
- A1: Medium, withdrawing its FIXED, and "would accept Blocking (Decision) only if the arbiter reads 'an acceptance case cannot pass as written' as changing an acceptance check" (A1 C-004).

Verdict: **Blocking (Decision), confidence 0.65.** A3's practical point is confirmed by the run (a usable bypass spelling is refused), and the best-effort status is true; neither rescues plan:207, whose literal bare case and `plan-hash`-with-`completed` case fail as written, nor the contradiction between plan:202 and plan:207. The executor cannot finish Task 13 without changing a stated acceptance line, so under the reading above this is Decision. Q-1 is PARTIAL (X-001). Medium side items fold in: over-matches on `git`/`sed`/`ruff` of `complete.py` (accepted, listed, tested), N-1 three pins, N-4 position.

## 2. The five verifications asked for

### C-001: repo in `stage-status`, `reads.py`, `github.py`: TRUE, Blocking (Safety), confidence 0.80
Read: `src/superclaude/cli/issue_pipeline/cli.py:266-305,343-348,368-391`, `src/superclaude/cli/issue_pipeline/reads.py:65-67,130-151`, `src/superclaude/cli/issue_watch/github.py:37,74-103`, `src/superclaude/core/WORKER-CONTRACT.md:242,293-300`. `_stage_status` has no repo argument; it calls `gh.reread(runner, budget, issue, _timeout)` (`cli.py:279`) and `reads.read_stage_evidence(runner, issue, _timeout, budget)` (`:282`), which calls `gh.events` and `gh.edits` with no repo (`reads.py:142,148`) and builds comments via `_argv_rest_page(n, "comments", ...)` (`reads.py:67`). Everything resolves to `REPO = "IronbellyOrg/IronClaude"` (`github.py:37`) or the literal in `EDITS_QUERY` (`:75`). `stage-status` has no `--repo` and defaults `--config` to the one hand-written file (`cli.py:343-348`). Task 15 keeps `REPO` as the default "so reads.py ... keep working unchanged" (plan:227); Task 16 passes `cfg.repo` only "from the cycle" (plan:238); Task 23 serves every allowed-owner repo (plan:313). The coordinator duty is to read GitHub through `stage-status` at each gate (`WORKER-CONTRACT.md:298`), live at level None. Result: for a repo X coordinator, `stage-status N` reads the approval evidence of IronClaude issue N. It fails closed in the usual case (no plan reply there) and can fail open when `--plan-dir` is omitted (A3's second case, `cli.py:293-294`). This breaks the per-repo provenance boundary. All three advocates agree; A1 and A2 concede; A3 owns it. Confidence is held at 0.80 because the fail-open path needs an issue-number collision.

### C-002: absent Pipeline value: TRUE as a required-behaviour gap, Blocking (Decision), confidence 0.70
Read: `src/superclaude/cli/issue_watch/github.py:764-775` (`_project_item`): `status = d.get("fieldValueByName")`; a null value gives `None`. Task 3 extends this to an aliased `pipeline` read and says an absent value is Python `None` (plan:61), with `pipeline_changed_at: datetime | None`. Task 3 also says a malformed time gives `non_json` or `unreadable` at the read layer, "not an exception" (plan:65), so a malformed time never reaches the predicate. Task 5 then says "an unreadable time also refuses" (plan:84) and its acceptance tests "an unreadable time refuses" (plan:87), with no empty-Pipeline case (plan:87-88). The only value the predicate can see as unreadable is `None`, which is exactly the empty Pipeline (a null `fieldValueByName` has no value, so no `createdAt`/`updatedAt`). An empty Pipeline is the decided None launch path (plan:95, R25) and, with the gate closed (plan:27), the only level that launches. A literal Task 5 refuses every such issue with `edited_after_approval`. Rebuttals: A1 (Medium, 0.55): "the read layer already separates the two ... Task 7 and Task 8 tests would expose it"; A2/A3 (Blocking): absent and unreadable are the same value in the plan, and the fix is a sentence plus three rows. The tests A1 names do not run through Task 5's predicate with a real item. Verdict: Blocking (Decision). A2's caution stands: a cleared-after-approval Pipeline has no time, so it cannot be told from "never set"; the plan must say it launches at None (lowest level, no authority raised).

### C-005: R6 and R9 against Task 27: TRUE, Medium, confidence 0.60
Read: `source.md:36` (R6), `:40` (R9), plan:356-363. R6 requires the image to install cron, start the daemon at every boot from `startup.sh` and keep exactly one entry on every boot (crontab outside the persisted volume). R9 requires checking branch, worktree and running session at boot and on every watcher run, creating missing parts and restarting a stopped session. Task 27's content list has the cron line, defaults file, branch and worktree rules, session name and launch text, credential row, guard install step and R20; it has none of the lifecycle clauses. But the handoff is one of two carriers: R6 and R9 are filed as Coder issues 515 and 516 (`source.md:36,40`) and the acceptance (plan:361) requires a row for each with "the value or text the template must use". The deliverable is present, under-specified, not absent. A1/A3: Medium. A2: Blocking (Missing), conceding "Task 27 names R6 and R9". Verdict: Medium; fix is two bullets plus a grep check.

### C-006: Task 6 versus Task 11: TRUE, Blocking (Decision), confidence 0.65
Read: plan:102 (brief used only at `none`; at the other levels the launched agent runs the command from its launch prompt), plan:177 (brief test at Worktree, Full and Full Submit, no None row), `src/superclaude/cli/issue_pipeline/brief.py:51-74`, `src/superclaude/cli/issue_pipeline/templates/worker-brief.txt`. `brief.build(issue, type_, complexity, nonce)` has no level parameter; the template's only slots are `{N}` and `{NONCE}`; its rows are keyed by complexity and "stop before /sc:implement and /task". A test of "the limited form of `/sc:troubleshoot` at Worktree and the `--fix` form at Full and Full Submit" in the brief has nothing to vary unless a level slot is added, which Task 6 decides against. The None-level Debug row (does `--fix` run before plan approval) is the live path and is untested. A1 (Medium): Task 6 owns the table and the executor can settle it. A2/A3 (Blocking, 0.96/0.60). The existing acceptance line cannot pass as written, so Decision. The fix moves the three non-None checks to the launch-prompt tests of Tasks 7 and 10 and adds the None rows to Task 11.

### C-007: `status_report`, `record.py`: TRUE, Medium, confidence 0.85
Read: `src/superclaude/cli/issue_watch/cycle.py:1270-1325` (retry argv from `launch.build_claim_prompt(n)` for entries in state `unknown`; docstring: "no `gh`"), `src/superclaude/cli/issue_watch/record.py:68-88` (`Entry` has no status, pipeline or prompt). Task 7 requires a valid retry for every Status (plan:123, :131) but changes no store field. A retry rebuilt from the issue number alone cannot equal the launched prompt for a non-default Status or level. It prints a command for a person to run (offline, gate closed, so no level above None can result), hence Medium. Unanimous.

### C-008: Task 5 versus Task 7 helper: TRUE (underspecified), Medium, confidence 0.80
`cycle.py:957-958` reads items before `project_check`; `predicates.py:262-271` selects the one live item inside `project_check` and returns only a reason (A2). Task 5 needs the item's value times before the helper exists in Task 7 (plan:123). Task 5 can select inline, but it does not say what it does for zero or several items (it must pass through so `project_check` gives `project_mismatch`). Unanimous Medium.

### C-009 (Note), C-010 (Note), C-011, C-012, C-013, C-014
- **C-009: Note, 0.70.** `cycle.py:767-768` sets `self.account_id` at run time; `check-config` (`cli.py:185-198`) is offline. The sentence says "the config's own account id", so intent is clear; the cite is wrong and the null case is unsaid. A1/A2 Note, A3 Medium (withdrawn in its own text only for card 3's Note, then raised to Medium). Rebuttal for Medium (A3): the warning has no input without `Config.owner_account_id`, which is optional. Rebuttal for Note (A2): the task states the intended configured-account comparison. Note.
- **C-010: Note, 0.70.** plan:30 lists `WORKER-CONTRACT.md` for Tasks 11 and 14 only, but plan:161 gives it to Task 10 too, and Tasks 2 and 10 both edit the two design docs (plan:48, :161). The same line also says "Tasks that edit the same file run in plan order, never in parallel", which covers the omitted pairs (A1, A2). A3: Medium because 10 and 11 have identical dependencies. The prose rule decides: Note. X-003 follows.
- **C-011: Medium, 0.60.** Read: `guard:553-582` and `:798`; `src/superclaude/skills/sc-pr-submit-protocol/scripts/reply-resolve-thread.sh:73,131,141`, `scripts/retrigger-review.sh:56`, `refs/thread-reply.md:5-7,12,47,67`, `refs/review-retrigger.md:27`, `refs/merge-guard.md:89`, `refs/conflict-mechanical.md:147`. Does the guard see the pr-submit `gh api` calls? The wrapper scripts run as `bash <script>`; the guard sees only that command text, so the writes inside the scripts are not seen (text-only limit, plan:24). The refs also show inline forms (`gh api --method POST ...`, `gh api graphql ...`, and quoted `gh api "repos/${REPO}/..."`, which `guard:557` classes as GHWRITE because a quote or `$` is outside its plain-GET form); if an agent inlines those it is refused at every level. `gh pr create` and `gh pr ready` are SUBMIT and pass at Full Submit (`guard:653`, `:790`). So A3's M-3 is overstated for the wrapper path and true for inline use. It is pre-existing, the remediation recorded it as "out of scope, flagged" (`remediation-proposal.md:132`), and the plan drops the flag. Medium for all three advocates: a recorded limit before the gate flips.
- **C-012: Note, 0.70.** plan:15 "can never write ... at any level" against plan:24-25.
- **C-013: Note, 0.50 [INFERRED].** The Pipeline value is known only after the last read in `_examine` (A3; `cycle.py:957`), so a gate cannot run before the reads without reordering; the cost is bounded by the 35-call cap (`github.py:46-49`), and the failure is closed. A1's M-4 fix can be a design-note line.
- **C-014: Medium, 0.70.** plan:268 (several Projects allowed with a defaults-map entry) against plan:323 ("Project count is exactly one (Task 19 rule)"), and plan:328 has no zero or several case although R14 asks for it (`source.md:34`). A mapped multi-Project repo that the generator accepts is skipped by every sweep. It fails closed and no stated check breaks; A2's Blocking rests on the conflict choosing loop behaviour. Medium; the fix is one clause plus cases.

### X-001, X-002, X-003
- **X-001: Q-1 PARTIAL, 0.80.** Settled by C-004 (A1 withdraws FIXED; A2 PARTIAL; A3 FIXED is overruled by the run).
- **X-002: Q-6 PARTIAL at Note level, 0.60.** `remediation-proposal.md:205` lists the test "`marker_comments` evidence ignores a result comment"; Task 12 (plan:191) has the string test only. The property follows from `github.py:61-63` (`marker: contains(CLAIM_MARKER)`) plus the plan:191 assertion that the result marker does not contain `CLAIM_MARKER`. One reader-level assertion closes it. A1/A3: Note; A2: Blocking (named check omitted). Note.
- **X-003: Q-10 PARTIAL, Note, 0.80** (= C-010).

## 3. Final grade of every point, with per-point convergence

Convergence = advocates (of 3) whose Round 1 final grade equals my final grade. A1's conditional ("would accept Blocking if ...") is counted as Medium.

| ID | A1 | A2 | A3 | Final grade | Conf. | Agree/3 |
|---|---|---|---|---|---|---|
| C-001 | Blocking (Safety) | Blocking (Safety) | Blocking (Safety) | **Blocking (Safety)** | 0.80 | 3/3 = 1.00 |
| C-002 | Medium | Blocking (Decision) | Blocking (Decision) | **Blocking (Decision)** | 0.70 | 2/3 = 0.67 |
| C-003 | Blocking (Decision) | Blocking (Decision) | Medium | **Blocking (Decision)** | 0.60 | 2/3 = 0.67 |
| C-004 | Medium | Blocking (Decision) | Medium | **Blocking (Decision)** | 0.65 | 1/3 = 0.33 |
| C-005 | Medium | Blocking (Missing) | Medium | Medium | 0.60 | 2/3 = 0.67 |
| C-006 | Medium | Blocking (Decision) | Blocking (Decision) | **Blocking (Decision)** | 0.65 | 2/3 = 0.67 |
| C-007 | Medium | Medium | Medium | Medium | 0.85 | 3/3 = 1.00 |
| C-008 | Medium | Medium | Medium | Medium | 0.80 | 3/3 = 1.00 |
| C-009 | Note | Note | Medium | Note | 0.70 | 2/3 = 0.67 |
| C-010 | Note | Note | Medium | Note | 0.70 | 2/3 = 0.67 |
| C-011 | Medium | Medium | Medium | Medium | 0.60 | 3/3 = 1.00 |
| C-012 | Note | Note | Note | Note | 0.70 | 3/3 = 1.00 |
| C-013 | Note | Note | Note | Note | 0.50 | 3/3 = 1.00 |
| C-014 | Medium | Blocking (Decision) | Medium | Medium | 0.70 | 2/3 = 0.67 |
| X-001 (Q-1 PARTIAL) | PARTIAL | PARTIAL | FIXED | PARTIAL (= C-004) | 0.80 | 2/3 = 0.67 |
| X-002 (Q-6) | Note | Blocking | Note | Note (PARTIAL) | 0.60 | 2/3 = 0.67 |
| X-003 (Q-10) | Note | Note | PARTIAL (Note) | Note (PARTIAL) | 0.80 | 3/3 = 1.00 |

Sum of agreement = 13.33 of 17 points. **Overall convergence = 13.33 / 17 = 0.784. Threshold 0.80: NOT_CONVERGED on grade.** The shortfall is one point: C-004 (1/3); had C-004 been graded Medium the figure would be 0.804. On the facts the advocates agree almost everywhere (every C point TRUE; C-013 inferred); the disagreement is the reading of "changes an acceptance check". Unresolved by agreement, settled by arbiter: C-004, then the 2/3 points C-002, C-003, C-006.

**Final Blocking list: C-001 (Safety), C-002 (Decision), C-003 (Decision), C-004 (Decision, with X-001), C-006 (Decision).**
Medium: C-005, C-007, C-008, C-011, C-014. Note: C-009, C-010 (X-003), C-012, C-013, X-002.

Not run: no repo test suite; the case test covered the guard's matcher text only, not the full hook (the hook also runs other classes on the same text).
