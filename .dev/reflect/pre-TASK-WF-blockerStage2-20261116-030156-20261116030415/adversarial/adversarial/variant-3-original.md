persona: refactorer
model_class: opus
model: claude-gw-tier1a[1m]
agent_type: reflect-reviewer

# Reviewer 3 (refactorer): pre-execution review of TASK-WF-blockerStage2-20261116-030156

I found 8 defects: 4 blocking and 4 minor. Of the T1 leads, T1-1 is confirmed and blocking. T1-7 is confirmed in part, and T1-8 (a), (b) and (c) are confirmed. T1-8 (d) and the parts of T1-7 that name `test_task_builder_merge.py` and `test_review_loop_extension.py` are dropped.

### R3-1 (blocking): the skills are told to call Python functions that no command exposes (T1-1 confirmed)
- **Plan:** PLAN:50 and PLAN:62. Task 2 says to write the ledger "through the follow-up writer", to make "the one sweep call", and that "the safety route (GR12) is live". Task 3 asks for the same.
- **Evidence:** `cli/review/__init__.py:19-29` registers 9 subcommands, none for follow-ups, the sweep or the safety route. S1:171 adds only `classify`. CLAUDE.md:95 says package code "NOT installed to `~/.claude/`... reach package behavior through the `superclaude` CLI".
- **Executor would:** write `uv run python -c "from superclaude.cli.review..."` into an installed skill, or have the agent hand-edit the ledger, which breaks REQ-08 (single writer with a revision check). The acceptance lines at PLAN:53-58 only grep for words, so neither would be caught.
- **Fix:** add a task before Task 2 that creates subcommands for the ledger write, the sweep and the safety route through the `__init__` tuple. Make Tasks 2 and 3 name those commands in the skills and add acceptance lines that check for them.

### R3-2 (blocking): the shadow classifier call has no live judge
- **Plan:** PLAN:50 ("the classifier is called in shadow mode") and PLAN:110 ("the shadow agreement figures").
- **Evidence:** S1:136 builds only `FixtureJudge` and `ReviewerJudge` (the reviewer's own label). S1:171 says `classify` "reads findings plus a judge answers file". S1:176 says no judge means `classifier=unavailable`. PSPEC:586 says results from different judges are not compared.
- **Executor would:** wire `ReviewerJudge`, whose agreement with the reviewer is 100% by construction, or get all rows `unavailable`. Either way Task 7 reports a meaningless agreement figure, and GR12's judge trigger (S = Y or U) never fires in a live run.
- **Fix:** Task 2 names the judge the live shadow call uses and records the judge id. Task 7 reports agreement by judge id, and says "not measurable" when the reviewer label is the only judge.

### R3-3 (blocking): the new offer has no `--unattended` branch
- **Plan:** PLAN:50 and PLAN:52-58.
- **Evidence:** `task/SKILL.md:53-55` says that under `--unattended` every point that waits for a person stops and returns to the caller. The offer asks ("Nothing is filed until you answer.", PSPEC:417). PSPEC:434 says an unattended run "records only", and PSPEC:441 requires the final report line "recorded only, no issue created". Task 2 never mentions `--unattended`, and Task 4 only pins `WORKER-CONTRACT.md`. Separately, PLAN:20 says the old definition "decides every gate outcome", while GR12 forces a person prompt (PSPEC:594).
- **Executor would:** add an offer that asks a question, and a GR12 prompt that waits, inside unattended runs.
- **Fix:** Task 2 adds the unattended rule (no offer; write the ledger and the PSPEC:441 report line) to the paragraph at line 55, plus an acceptance check for it. Reword PLAN:20 to "except the GR12 safety route".

### R3-4 (blocking): Task 6 leaves out the inputs two of the three sets need
- **Plan:** PLAN:98.
- **Evidence:** the plan names only `stage0-heldout-ids.json` and `fresh-findings.md`.
  - `stage0-heldout-ids.json` holds ids only (S0:85). The text, cited paths and panel labels of those rows are in PF `04-historical/master-table.md` and `05-scoring/consensus.md` (S0:69, S0:116). Neither file is named in the plan, including its Constraints at PLAN:19.
  - The request names `stage0b-sample.md` (SRC:13), which holds each finding's source file and quote (S0:50). The plan dropped it.
  - `@E2` rows need `git show` (S0:116), but the inputs supplier reads only from disk and runs no subprocess (S1:148, S1:153).
- **Executor would:** record the evidence and required-item inputs as UNSET for those rows, which makes the input counts and the M, C and E answers wrong.
- **Fix:** name all four sources in Task 6 and state how `@E2` rows are counted.

### R3-5 (minor): Task 1 checks the owner's go after it has already edited `src/`
- **Plan:** PLAN:33-37, against PLAN:20 ("runs only after... Task 1 checks that").
- **Evidence:** the owner-go check and the stage 1 existence check are acceptance criteria, which are checked after the task body has created `sweep.py` and its test.
- **Executor would:** write files under `src/` before finding out the run is not allowed. The files are new, so nothing is lost.
- **Fix:** open Task 1's body with "Before any edit:" followed by both checks.

### R3-6 (minor): checks are missing for text the plan edits (T1-7 and T1-8b)
- **Plan:** PLAN:58, PLAN:67 and PLAN:112-115.
- **Evidence:**
  - `test_review_prompt_overrides.py:271-283` pins "no minimum count" in the reviewer briefs of the task and tech-research skills, which are the briefs Tasks 2 and 3 edit. No task runs this test.
  - In `-k "tech_research or review_severity"`, the `tech_research` part selects nothing: the test ids spell "tech-research" with a hyphen (line 276).
  - `test_worker_contract.py:1715-1731` pins `task/SKILL.md:55`, which R3-3 edits, but only Task 4 runs it.
  - The request's no-edit list (SRC:19) has no `git diff --stat` check, unlike S1:221.
- **Fix:** add those two test files to the acceptance runs of Tasks 2 and 3, and add a `git diff --stat HEAD` check over the no-edit paths to Task 7.

### R3-7 (minor): the sweep has no input contract (T1-8a)
- **Plan:** PLAN:33.
- **Evidence:** the plan does not say how the sweep receives the final deliverable, its kind, or its decision-basis sections. PSPEC:246-252 gives a different source per kind, and one row says "Available today? No".
- **Executor would:** invent a signature that Task 2 then has to match from a Markdown skill.
- **Fix:** Task 1 fixes the arguments (ledger path, deliverable path, deliverable kind) and says that kinds with no decision-basis list are skipped and counted.

### R3-8 (minor): a tech-research halt may show no offer at all
- **Plan:** PLAN:62.
- **Evidence:** the tech-research cap sentence is a checklist item of the generated task file (`tech-research/SKILL.md:490`), which `/task` runs through its item loop (`tech-research/SKILL.md:614`). Task 2 places the halt-offer text only beside the task skill's own three cap sentences (`task/SKILL.md:258, 372, 409`) and in Post-Completion Validation.
- **Executor would:** leave a halt ordered by a task-file item with no offer, despite the OD2 default "at any escalation halt" (PLAN:21).
- **Fix:** Task 2 states the halt-offer rule for any escalation halt, including one that a task-file item orders.

## Leads dropped
- **T1-7, partly:** `test_task_builder_merge.py` and `test_review_loop_extension.py` do not reference the task or tech-research skill, so they are not affected.
- **T1-8 (d):** forbidding the word "sweep" in tech-research is satisfiable. The plan's own prose is not written into the file, so the one-offer sentence simply avoids the word.

**Not checked:** the line numbers in `WORKER-CONTRACT.md` beyond 33, 36 and 39, the location of `pragmatic.md:225`, and whether `stage0-heldout-ids.json` stores finding text. None of the stage 0 or stage 1 artifacts exist yet, so nothing was run.


```yaml
calibration:
  calibrator_model_class: sonnet
  calibrated_confidence: 0.83
  dimensions: {'citation': 0.92, 'coverage': 0.65, 'classification': 0.9, 'risk': 0.8, 'actionability': 0.9}
  citation_spot_check: "20+ ranges read, none contradicted; overreach: R3-3 'every point that waits', R3-6 'selects nothing', R3-1 did not examine ledger_cmd"
  coverage_gap: "task 5 never mentioned"
  inline_fallback: false
```
