# Round 1: advocate for Variant 1 (reviewer-1 card, analyzer, sonnet)

Plan: `.dev/tasks/to-do/TASK-WF-requirements-20261119-140750/TASK-WF-requirements-20261119-140750.md` (`plan:N` = line of it). Cards and diff analysis are in `.dev/reflect/pre-TASK-WF-requirements-20261119-140750-20261119141121/`. Everything cited as `file:line` below was read in this round.

## 1. Steelman of the other cards

**Card 2 (qa, haiku).** Its two best findings are QA-2 and QA-1, and both are real. QA-2 sees that Task 11 requires a test where "a claim-time event is refused as plan approval" (plan:176), yet `record_create` (`approval_record.py:313-359`) takes the plan hash, channel, evidence id and actor and only checks that an adoption row exists. Nothing in it can tell a claim-time event id from a worker-`ask` event, and no task edits that module. QA-1 sees that Task 27, the only task for R6 and R9, drops the lifecycle text of those rows (install cron, start the daemon, restore exactly one entry on every boot, check the coordinator at boot and on every watcher run, restart a stopped session). It also spots that Task 24 and Task 19 disagree on several Projects (QA-4), which card 1 missed.

**Card 3 (refactorer, opus).** Its strongest finding is B-1. `stage-status` calls `gh.reread` and `reads.py` calls `gh.events` and `gh.edits` with no repo, and `github.py:37` hard-wires `REPO = "IronbellyOrg/IronClaude"`. Task 15 keeps `REPO` as the default "so reads.py ... keep working unchanged" (plan:227). Task 23 then enables every repo of an allowed owner (plan:313), so a coordinator for repo X reads the approval of IronClaude#N. B-2 is also sharp: Task 3 makes an absent Pipeline `None` and Task 5 says "an unreadable time also refuses". B-3 shows a real contradiction between Task 6 (the brief is used only at level None, plan:102) and Task 11's brief test at Worktree, Full and Full Submit (plan:177). Its remediation re-check is the most careful of the three (Q-6, Q-10).

## 2. Strengths of card 1, and where cards 2 and 3 go wrong

Strengths of card 1 (all re-checked here):
- Its line cites hold. Guard `launch-level-guard.sh` lines 10, 444, 653, 764, 786 and 790 match. The `cycle.py` order (events, approval, `unchanged_since`, items, `project_check` in `_examine`; approval reread, then items reread, then `project_check` in `_revalidate`) matches. `status_report` rebuilds the retry prompt with `build_claim_prompt(n)` only.
- C-007 and C-009 are correct, and C-008 is real though minor.
- U-005 (N-1, GRID_CLASSES and the import-time assert) and the over-match analysis (C-004) are concrete and checkable.
- It correctly graded nothing as Blocking where the plan's own text still leaves a defect to the executor's judgment.

Where card 1 is weaker (conceded): it missed C-001, C-003 and C-005, and it rated Q-1 FIXED when the `p.complete.run()` case is unmatchable (X-001). That is a real miss on card 1's side.

Critique of card 2:
- Its verdict is internally inconsistent (S-002): it says "Blocking" in prose but MEDIUM in its own column. Grade by the rule, not the label.
- It says the Task 10/11 order "is sound" (C-010) without noticing Task 10 also edits `WORKER-CONTRACT.md`.
- It is thin on reading: it never checked the guard's real surface, the `status_report` retry path, `check-config`, or the Task 5 call order. It misses C-007, C-008 and C-009.
- It marks R33 "partial" without saying which item.
- QA-1 is graded Blocking (Missing) although Task 27 does carry R6 and R9 as listed rows (plan:361) and issues 515 and 516 hold the lifecycle text (source.md:36, :40).

Critique of card 3:
- It over-grades. B-3 is a mismatch between a design note decision and an acceptance line, which the executor can settle in Task 6 (Task 6 owns the table at plan:101-102). B-2 is a wording gap that a parse test would catch. Neither changes a decision by itself.
- M-5 (the goal sentence) is a Note: it is prose, not a check or behaviour.
- M-1 is a Note: the plan's own rule says tasks run "in plan order" (plan:30), and Task 2 < Task 10 < Task 11 already by number.
- It lists N-1 and M-3 of card 1 as Note and Medium (C-009). That is the right call on N-1 (see below).
- B-1 is real but sits partly outside card 3's own evidence: it did not check that the plan's Task 16 threads `repo` through every `github.*` call of the cycle (so the watcher itself is safe), only `reads.py` is left.

## 3. Shared assumptions

- **A-001: ACCEPT.** I re-read the guard lines (10, 444, 653, 764, 786, 790), `predicates.py` `project_check` (262-271), `approval_of` and `unchanged_since`, `cycle.py` `_examine` and `_revalidate`, and `status_report`; they hold. The plan itself tells the executor to re-run Grep before editing (plan:125, :161). The residual risk is a few un-read line cites in tests and docs, which a re-grep handles.
- **A-002: QUALIFY.** The plan does address it: Task 4 says it needs the owner's hands and "does not continue until the owner answers" (plan:73), and Task 3 says to stop and return the fallback (plan:61). It holds only for an attended `/sc:implement` run; the plan does not say what an unattended run does. Mark it STATED, not UNSTATED.
- **A-003: ACCEPT.** Stated at plan:24 ("a script or another HTTP client is not seen") and plan:202 ("best effort, not a control").
- **A-004: ACCEPT.** Plan:25 states it. Card 1 checked the code; I only confirmed the plan text.
- **A-005: QUALIFY.** All tests use fake runners (plan:22), so a defect only shows when a task writes a case for it. That is true for C-001, where no task names `stage-status` or `reads.py` as a caller to thread. It is not a general blind spot: Tasks 15 and 16 do write cross-repo tests for the watcher path.

## 4. The decisive questions: C-001 to C-014 against the real files

Rule used: Blocking only if Decision, Missing or Safety; otherwise Medium or Note.

| ID | TRUE? | Evidence read | Severity | Confidence |
|---|---|---|---|---|
| C-001 | TRUE | `issue_pipeline/cli.py:279` (`gh.reread(runner, budget, issue, _timeout)`, no repo), `reads.py:142,148` (`gh.events`, `gh.edits`, no repo), `github.py:37` (`REPO` constant), plan:227 (keeps `REPO` as default), plan:313 (every allowed-owner repo), `WORKER-CONTRACT.md:242` ("Every such action targets IronbellyOrg/IronClaude") | **Blocking (Safety)**: conceded. Following the plan, a coordinator for another repo reads an approval from IronClaude's issue of the same number, at level None, so the closed ship gate does not help. | 0.65 |
| C-002 | TRUE as an ambiguity | plan:61 (absent value is `None`, `pipeline_changed_at: datetime \| None`), plan:84 ("an unreadable time also refuses"), plan:87-88 (no empty-Pipeline case). Plan:65 says a malformed time gives `non_json` or `unreadable` at the read layer, which supports reading "unreadable" as a failed parse, not an absent field. | **Medium**. The read layer already separates the two; a literal reading is possible but the Task 7 (empty Pipeline prompt) and Task 8 (None launches) tests would expose it. Fix needs one test case. | 0.55 |
| C-003 | TRUE | `approval_record.py:313-359` (no input tells claim-time from plan approval; only `no-adoption`, `bad-channel`, `bad-evidence-id`, `bad-actor`); `cli.py:52` (`--plan-hash` already required, so "refused without a plan hash" is already true); Task 11 lists no change to `approval_record.py` (plan:173) and plan:30 does not list it | **Blocking (Decision)**: conceded. R29 (source.md:55) requires a test that refuses a claim-time event, and no task builds the thing that could refuse it. | 0.7 |
| C-004 | TRUE, two parts | Guard `:444` (every alternative needs `issue-pipeline` or `issue_pipeline`), so `p.complete.run()` alone matches none; plan:202 option "record the over-match as accepted" contradicts plan:207 (`plan-hash` with "completed" must stay allowed, but `*issue-pipeline*complete*` refuses it) | **Medium** (X-001: I withdraw card 1's FIXED for Q-1). The executor sees a failing test and fixes it mechanically (add a pattern or anchor on the verb); no decision changes. Would accept Blocking (Decision) only if the arbiter reads "an acceptance case cannot pass as written" as changing an acceptance check. | 0.5 |
| C-005 | TRUE | plan:356-363 lacks "install cron, start daemon, restore exactly one entry at every boot", "check at boot and on every watcher run", "restart a stopped session" (source.md:36, :40); plan:361 only asks for R1, R6, R9... "with the Coder issue number where one exists and the value or text the template must use" | **Medium**. The row for R6 and R9 is required by the acceptance, and issues 515 and 516 hold the lifecycle text. Becomes Missing only if the arbiter counts the handoff body as the sole carrier. Fix: add the two lifecycle bullets. | 0.5 |
| C-006 | TRUE | plan:102 (brief used only at `none`; the launched agent runs the command at the other levels) vs plan:177 (brief test at Worktree, Full, Full Submit); `worker-brief.txt` is a plan-writing worker whose rows "stop before /sc:implement" | **Medium**. Task 6 owns the Status-by-level table (plan:101) and the executor can resolve it there. The Debug-at-None `--fix` question is real and not answered, but it is a design-note item, not a changed decision yet. | 0.55 |
| C-007 | TRUE | `cycle.py` `status_report`: retry built from `build_claim_prompt(n)` with no gh and no Status/Pipeline (docstring "Reads `dispatch.json` ... no `gh`"); plan:123, :131 want a valid retry per Status; no task adds a stored field | **Medium** | 0.75 |
| C-008 | TRUE, minor | `_examine` reads items before `project_check` (`cycle.py`), so Task 5 can select the item inline; the helper arrives in Task 7. Real gap: what Task 5's predicate does with zero or several items (it may return `edited_after_approval` where `project_mismatch` is right) | **Medium** (low) | 0.55 |
| C-009 | TRUE | `cycle.py:767-768` (`self.account_id` is set at run time from `gh api user`; `cfg.owner_account_id` is the optional config field); `cli.py:183-198` `check-config` is offline | **Note**. The sentence says "the config's own account id", so the intent is clear; only the cite is wrong. Downgrade from my own card's Medium. | 0.6 |
| C-010 | TRUE | Task 10 lists `WORKER-CONTRACT.md` and both `docs/designs` runbooks as files it edits (plan:161); plan:30 names only Tasks 11 and 14 for `WORKER-CONTRACT.md`; Task 2 edits the same two docs (plan:48) | **Note**. Plan:30 says tasks run "in plan order", and 2 < 10 < 11 already. Cheap to fix. | 0.6 |
| C-011 | TRUE | `reply-resolve-thread.sh:73,131,141` and `review-retrigger.md:27` use `gh api` writes; guard `:560-585` classifies any `gh api` with a write method or `graphql` as GHWRITE, denied at all four levels (`:798`); `remediation-proposal.md:132` flagged it as "out of scope, flagged"; plan:27 says Full Submit "runs `/sc:pr-submit --monitor 3`" | **Medium**. Pre-existing guard behaviour, hidden by the closed gate; the plan dropped the flag. Fix: one line in Task 6 and Task 26. | 0.7 |
| C-012 | TRUE | plan:15 ("can never write ... at any level") vs plan:24-25 (text check only; the claim session is ungoverned and posts two comments) | **Note** | 0.7 |
| C-013 | PLAUSIBLE, [INFERRED] | `_examine` reads events, edits and items before the gate can fire (the gate needs the Pipeline from the items, plan:137); every skip is re-examined per cycle today. I did not measure the 35-call budget. | **Note** | 0.4 |
| C-014 | TRUE | plan:268 (Task 19: several Projects use the defaults map id) vs plan:323 (Task 24: "Project count is exactly one"); plan:328 has no Project-count case; R14 (source.md:34) lists it | **Medium** | 0.65 |

## 5. Summary of position

- Blocking after this round: C-001 (Safety) and C-003 (Decision). I concede both to cards 3 and 2; card 1 missed them.
- Medium: C-002, C-004, C-005, C-006, C-007, C-008, C-011, C-014.
- Note: C-009, C-010, C-012, C-013.
- Contradictions: X-001 conceded (Q-1 is PARTIAL because the `p.complete.run()` case cannot match); X-002 and X-003 (card 3's PARTIAL) are Notes, not Blocking.
- Not run: no tests were executed; `test_*` line cites and docs were not re-read; C-013 stays an inference.
