# Reviewer 1 brief (analyzer, model class sonnet)

## T1 card excerpt

Assignment: independent pre-execution review of the plan `.dev/tasks/to-do/TASK-WF-blockerStage2-20261116-030156/TASK-WF-blockerStage2-20261116-030156.md` against its request `.dev/tasks/to-do/TASK-WF-blockerStage2-20261116-030156/source.md` (UC-1, advisory, read-only). Lens (analyzer): root-cause and deviation. Compare the plan with its request (SRC) and with the program spec and the two earlier stage plans: does the plan do what the request says, is anything the request requires missing, does the plan contradict its sources or itself, and are the findings of the earlier review (prior report, F1, F6, F7, F8) that touch stage 2 resolved here?

The T1 points below are UNVERIFIED LEADS written by the orchestrator, not conclusions. Verify each against the files, drop the ones you cannot reproduce, and add defects the card missed. Severity rule (use exactly): BLOCKING = a requirement or check in the plan that cannot be met as written, a wrong or missing result, or data loss; MINOR = wording or format. Say for each finding whether the plan can still be executed correctly by an executor who follows it literally.

Return your findings as your final message (you cannot write files); the orchestrator saves them. For each finding give: id (R1-1, R1-2, ...), grade (blocking or minor), the plan location (PLAN:line), your evidence as file:line with a short quote, what the executor would do wrong, and the smallest fix. At most 8 findings, each under 700 characters. If a T1 lead is wrong, say so in a final section 'Leads dropped' with one line each. Cite only lines you have Read.

Plan = `.dev/tasks/to-do/TASK-WF-blockerStage2-20261116-030156/TASK-WF-blockerStage2-20261116-030156.md` (cited as PLAN:n). Spec = its `source.md` (SRC:n), the stage 2 request. Program spec = `.dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/02-brainstorm/merged-requirements.md` (PSPEC:n). Stage 1 plan = `.dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/TASK-WF-blockerStage1-20261116-030154.md` (S1:n). Stage 0 plan = `.dev/tasks/to-do/TASK-WF-blockerStage0-20261116-021044/TASK-WF-blockerStage0-20261116-021044.md` (S0:n).

**T1-2 (blocking?)** `--unattended` is not carried into the offer text. Task 2 adds "the end-of-run offer is shown with the halt message" at each of the three cap sentences (PLAN:50), but `task/SKILL.md:55-57` makes those halts return the open blocking findings to the caller as a question under `--unattended`, WC-2 forbids chat offers there, and PSPEC:430-441 says an unattended run only records (offer state `unattended`). Task 4's check is on the contract text only (PLAN:79). Existing pin: `tests/skills/test_worker_contract.py:1715`.

**T1-3 (blocking?)** "Count of safety misses by the stage 0 definition" cannot be computed from ledgers. The stage 0 definition needs a later review or the owner to confirm a risk on a row that was recorded as a follow-up or Note (S0:130), but the script reads only run folders and `qa/follow-ups.md` (PLAN:110). No confirmation input is specified, so the script can only print 0, and Task 7 then states that stage 3 needs "zero safety misses" (PLAN:114). A silent wrong number goes to the owner.

**T1-4 (non-blocking?)** The judge in live shadow runs is never named. PLAN:50 says "the classifier is called in shadow mode"; OD3 is undecided and no external judge is built (PLAN:21-22); stage 1's judges are `FixtureJudge` and `ReviewerJudge` (S1:136), and PSPEC:586 says that with only the reviewer's label left the row records `classifier=unavailable`. So "shadow agreement" (PLAN:110) is either empty or trivially 1.0, and no task says so.

**T1-5 (non-blocking?)** Task 6 does not say how three blind agents times three replicates become judge verdicts: per agent (three judge ids; PSPEC:586 says results from different judges are not compared) or pooled (PLAN:98). Figures per set depend on it.


## Grounding hunks

codegraph run state: index_state=fresh checked_at=2026-11-16T03:12:04Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel projectPath=/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel


### .dev/tasks/to-do/TASK-WF-blockerStage2-20261116-030156/source.md:1-19

```markdown
# Stage 2 plan request: shadow beside the old rule (issue #552)

Third of five plan packages (see `stage-requests/README.md`). Generate it only after the stage 1 package's `./artifacts/stage1-summary-for-owner.md` has been read and the owner has said go in chat; the stage ledger rows for stages 0 and 1 hold their package ids. The old definition still decides every gate outcome in this stage.

## Base text

Reuse Tasks 26 to 30 of the revised 46-task plan `TASK-WF-loosenBlockerRev-20261115-210254` (Phase 3, stage 2; found by that folder name under `.dev/tasks/to-do/`), renumbered 1 onward, with its `## Constraints` (stage 2 parts). Stage 0 and stage 1 evidence is read by package id.

## Changes to apply

- **Constraints.** State this is stage 2: the sweep only records (`promote` off), the classifier has no authority, the one sweep call and one offer sit in the task skill's "Post-Completion Validation (Final Phase Only)", tech-research gets neither. Stage 3 starts only after the owner reads this package's summary and says go; the stage 3 entry also needs at least 5 observed shadow runs, which the owner or operator produces over time and no task here can produce.
- **Cap-site offers (base Tasks 27 and 28).** The halt-offer text goes beside each cap sentence in the task skill and in tech-research only; the two `rf-qa.md` cap sites are not touched here (stage 3). Acceptance quotes the cap sentence "After 2 fix cycles (3 reviews), HALT and escalate to the user with the open blocking findings" and names no line numbers.
- **New task: classifier evaluation on the stage 0 populations (finding F7).** Run the classifier of the stage 1 modules (`classify` command, `classifier_inputs.py` supplier, the question set v1, recorded fixture answers produced by three blind agents that did not write the questions, no Jev) on the three sets built in stage 0: the fresh-findings set, the held-out half of the 318 rows, and the reviewer-called-minor set (read by the stage 0 package's id, its `./artifacts/fresh-findings.md`, `stage0-heldout-ids.json`, `stage0b-sample.md`). Write `./artifacts/stage2-classifier-eval.md`: agreement with the panel consensus, Cohen's kappa, confusion matrix, recall on the panel's blockers, flip rate over three replicates, split by deliverable kind, the count of rows that had each code-supplied input, and the limits. State that it is not an authority test (OD4).
- **New task: shadow summary script and stage 2 exit summary (finding F8).** Write `./artifacts/shadow_summary.py` (run with `uv run python`) that reads a list of shadow-run folders and their `qa/follow-ups.md` ledgers and prints the stage 2 exit numbers the spec defines (ledger volume per run, share of `consumer-unknown` rows, offers made and answered, shadow agreement, count of runs observed, count of safety misses by the stage 0 definition, capture failures), with a test over fixture ledgers. Then write `./artifacts/stage2-summary-for-owner.md`: the classifier evaluation headline, the script's output over the shadow runs that exist so far (zero is a valid and stated result), and the sentence that the owner's go for stage 3 is given in chat and not by this file.
- **Acceptance lines inside this package** that a later task of the same package makes false get an end point.

## Not to be done by the plan

No edit of `pragmatic.md`, `rf-qa.md`, `rf-qa-qualitative.md`, `rf-analyst.md`, templates, rule prompts, builders or researchers, and no promotion of swept rows to Blocking. Do not change `sc-implement-protocol/refs/qa.md`, the own-scale primitives, the cap of 2 fix cycles or the 35 percent target. No Jev call, key or account.
```

### .dev/tasks/to-do/TASK-WF-blockerStage2-20261116-030156/TASK-WF-blockerStage2-20261116-030156.md:17-27

```markdown
## Constraints

- Spec: the merged spec `02-brainstorm/merged-requirements.md` inside the program folder `BLOCKER-CLASSIFICATION-PROGRAM-20261115` (found by that folder name under the repository's task folder). This plan calls that folder PF and the spec file the spec. Section numbers, requirement ids (REQ-nn), loop changes (L1 to L6), guardrails (GR1 to GR12), tests (T1 to T17) and owner decisions (OD1 to OD17) refer to the spec. PF also holds the 5-run results in `08-test/results.md`, the reconciliation in `09-plan-input.md` and the stage ledger and the five stage requests in `stage-requests/`. Evidence of earlier stages is read from their packages by package id (the ids are in the stage ledger), found by that folder name in the to-do or done subfolder of the repository task folder.
- One package, one stage. This is stage 2 of five packages (one plan per stage). The old definition still decides every gate outcome: the sweep only records (`promote` off), the classifier has no authority, the one sweep call and the one offer sit in the task skill's "Post-Completion Validation (Final Phase Only)" and tech-research gets neither. It runs only after the stage 1 package is done (its modules `follow_ups.py`, `safety_route.py` and `sweep`'s inputs exist; Task 1 checks that) and the owner has said go in chat. Stage 3 starts only after the owner reads this package's summary and says go; its entry also needs at least 5 observed shadow runs, which the owner or operator produces over time and no task here can produce.
- Owner decisions use the spec's recommendations unless the owner changes them: OD1 skill folder `sc-review-severity`; OD2 once per run plus at any escalation halt; OD4 the classifier has no authority in version 1; OD9 reviewer-named consumer, code-checked where quotable; OD11 replace label-max merging at all 13 lines in 10 files, staged; OD12 yes; OD13 short Note rows; OD14 a finding with an unknown consumer keeps the reviewer's label (no deferral); OD15 consent-bound body file posted by the attended top-level session; OD16 option (b) at stage 3. OD3 (finding text leaving the machine), OD5 to OD8 and OD10 are not decided here and no task depends on a different answer.
- Not built here: any Jev or other external judge call, any TypeSafe account or key, a Jev or LLM judge class (they wait for OD3), any change to `src/superclaude/skills/sc-implement-protocol/refs/qa.md` (it keeps its own scale), any change to the own-scale primitives listed in spec section 9.3 as unchanged, code-assigned severity in `src/superclaude/cli/**/*.py` (for example `fmea_classifier.py` and `remediate_parser.py`, out of scope by spec section 10.3), the 35 percent score target, and any change to the cap of 2 fix cycles.
- Classifier facts that bind every classifier task: the 5-run test (stage 0 package, `stage0a-result.md`, from PF `08-test/results.md`) used a text-only stand-in judge and got agreement with the panel of 58.5 percent (Cohen's kappa 0.27), and the missing-item, constraint and contradiction questions (M, C, E) were at chance without code-supplied inputs. So M, C and E run only when code supplies the required-item list, the constraint lines and the verified evidence (the classifier-inputs supplier of stage 1), the "M or C is Y gives BLOCKING" row is never enabled for any gate, and confidence is reported as an ordinal band, never as a probability.
- Pins are by content. An acceptance check that must survive a task's own edit quotes the sentence it protects; it does not name a line number, because the edit moves the line. Line numbers in a task body are where the text sits today and are re-read before editing. An acceptance line that a later task of this package makes false carries its end point ("until Task N").
- `src/superclaude/` is the source of truth. Edit there, then run `make sync-dev`; never stage anything under the project `.claude/` folder (only `.claude/settings.json` is tracked). Installed primitives name installed paths (`~/.claude/skills/...`) first and project `.claude/...` second, never a `src/superclaude/` path.
- Python work uses UV only: `uv run pytest ...`, never `python -m` or bare `pip`.
- Task-owned evidence and generated outputs go under `./artifacts/` in this package. `.dev/tasks/` is always staged (`git add .dev/tasks`), packages and their `./artifacts/` included, and no document a task writes says it is never staged. Staging is not committing.
```

### .dev/tasks/to-do/TASK-WF-blockerStage2-20261116-030156/TASK-WF-blockerStage2-20261116-030156.md:46-58

```markdown
## Task 2: Make the task skill write the ledger, call the sweep and make the offer in shadow mode

Depends on: Task 1

Edit `src/superclaude/skills/task/SKILL.md`: the reviewer brief at the Phase-Gate QA step asks each reviewer for `rests_on` (the named consumer, or `none`, or `unknown`) and a one-line `why not blocking` for every Medium or Note finding (GR2); the Findings Consolidation step keeps its present merge text in this stage but also writes `qa/follow-ups.md` through the follow-up writer (REQ-07, the run owner is the only writer); the Follow-Up Items bullet in the final-phase notes points at that ledger; the safety route (GR12) is live; the classifier is called in shadow mode and its verdict is recorded and gates nothing. The one sweep call (`promote` off) and the one end-of-run offer (spec section 6.3, replacing the output style's once-per-loop ask for this run only) are placed in the section "Post-Completion Validation (Final Phase Only)", because tech-research runs inside `/task` and shares that final gate. The offer also appears at an escalation halt: at each sentence "After 2 fix cycles (3 reviews), HALT and escalate to the user with the open blocking findings" in this file (today at the Conditional Proceed step, the Escalation item of the fix-cycle list, and the Fidelity Verification step) the text says the end-of-run offer is shown with the halt message. The old definition still decides every gate outcome. Run `make sync-dev` afterwards.

Acceptance criteria:
- The reviewer brief in `src/superclaude/skills/task/SKILL.md` contains `rests_on` and `why not blocking`.
- The skill names `qa/follow-ups.md` as the ledger path and names the run owner as its only writer.
- The sentence "Preserve the highest severity rating when duplicates disagree" still appears in the file (the merge rule is deliberately unchanged in this stage); `grep -c "highest severity" src/superclaude/skills/task/SKILL.md` prints the same count as before the edit.
- The section "Post-Completion Validation (Final Phase Only)" names the sweep call and the offer once each, and `grep -n "sweep" src/superclaude/skills/task/SKILL.md` shows no other call site.
- The sentence "After 2 fix cycles (3 reviews), HALT and escalate to the user with the open blocking findings" still appears at each place it appears today, with the halt-offer text beside it.
- `uv run pytest tests/skills/test_review_severity_rule.py tests/skills/test_review_severity_mapping.py -v` still passes (no pinned text moved).
```

### .dev/tasks/to-do/TASK-WF-blockerStage2-20261116-030156/TASK-WF-blockerStage2-20261116-030156.md:72-79

```markdown
## Task 4: Add the three follow-up keys to the worker contract

Edit `src/superclaude/core/WORKER-CONTRACT.md`: WC-4 (the bullet that enumerates the top-level keys, `worker_contract_version`, `worker_status`, `command`, `report_path`, `artifacts`) gains `follow_up_ledger` (path), `follow_up_counts` with `follow_up`, `note` and `show_user`, and `follow_up_capture_state` (`complete`, or `incomplete` with a reason); the status mapping maps `incomplete` capture to `worker_status: partial`; the coordinator duties (the bullet that says "the coordinator opens it") name the three keys as things to read; follow-ups alone never change `worker_status` from `succeeded`; the ledger is listed in `artifacts` only when it is a tracked path (WC-4 keeps gitignored paths out). Update `tests/skills/test_worker_contract.py` and add T10 cases.

Acceptance criteria:
- `src/superclaude/core/WORKER-CONTRACT.md` lists the three new keys in the bullet that enumerates top-level keys.
- `uv run pytest tests/skills/test_worker_contract.py -v` passes and a new test fails when a contract with `follow_up_capture_state: incomplete` is not mapped to `partial`.
- A test asserts an unattended run that records follow-ups makes no GitHub call and asks no question.
```

### .dev/tasks/to-do/TASK-WF-blockerStage2-20261116-030156/TASK-WF-blockerStage2-20261116-030156.md:106-115

```markdown
## Task 7: Write the shadow summary script and the stage 2 owner summary

Depends on: Task 1, Task 2, Task 3, Task 4, Task 5, Task 6

Write `./artifacts/shadow_summary.py` (run with `uv run python`) that reads a list of shadow-run folders and their `qa/follow-ups.md` ledgers and prints the stage 2 exit numbers the spec defines in its section 12 stage 2 row (as edited by the stage 0 package: ledger volume per run, the share of rows tagged `consumer-unknown`, offers made and answered, the shadow agreement figures, the count of runs observed, the count of safety misses by the stage 0 definition, and the count of capture failures), with a test over fixture ledgers under `./artifacts/`. Then write `./artifacts/stage2-summary-for-owner.md`: the classifier evaluation headline from Task 6, the script's output over the shadow runs that exist so far (zero runs is a valid and stated result), the sweep and offer wiring results from Tasks 1 to 5, the limits, and the sentence that the owner's go for stage 3 is given in chat and not by this file.

Acceptance criteria:
- `./artifacts/shadow_summary.py` runs with `uv run python ./artifacts/shadow_summary.py --help` and its fixture test passes (the command and the pytest or script output are recorded in the summary).
- `./artifacts/stage2-summary-for-owner.md` names the headline of Tasks 1 to 6 with the file that holds it, states the number of shadow runs observed so far (zero is allowed), and states plainly that the stage 3 entry needs at least 5 observed runs with zero safety misses.
- The summary ends with the sentence that the owner's go for stage 3 is given in chat and not by this file.
```

### src/superclaude/skills/task/SKILL.md:55-55

```markdown
The same applies to the two other "ask the user" points that wait for a person: the Phase-Gate QA step that halts after the second fix cycle ("present the QA report findings to the user, and ask for guidance") and the "Any step FAIL with unfixable issues" rule. Under `--unattended` (token after the task file path), each stops the run and returns the open blocking findings, as a question, to the caller instead of asking and waiting; the caller (tdd) writes its blocked worker contract from it.
```

### src/superclaude/skills/task/SKILL.md:258-258

```markdown
9. **Conditional Proceed (M3 Step 8)** — IF both verification agents report PASS, proceed to the next phase. IF either reports FAIL, repeat Steps 6-8 (consolidate new + remaining findings, fix, verify). Maximum 2 fix cycles total (per I16 (MDTM template rule: maximum 2 fix-verify cycles per gate)). After 2 fix cycles (3 reviews), HALT and escalate to the user with the open blocking findings — log all remaining issues in Task Log, present the QA report findings to the user, and ask for guidance. Do NOT continue to the next phase without user approval.
```

### src/superclaude/skills/task/SKILL.md:372-372

```markdown
6. **Escalation:** After 2 fix cycles (3 reviews), HALT and escalate to the user with the open blocking findings; log all remaining issues in the Task Log.
```

### src/superclaude/skills/task/SKILL.md:409-409

```markdown
**Step 6 (Fidelity Verification):** Spawn minimum 2 verification agents to confirm fidelity fixes were applied correctly. Maximum 2 fix cycles (per I16). After 2 fix cycles (3 reviews), HALT and escalate to the user with the open blocking findings.
```

### src/superclaude/core/WORKER-CONTRACT.md:31-39

```markdown
- **WC-2. No person-blocking step in unattended mode.** Under `--unattended` the command never calls `AskUserQuestion`, never ends its turn on a chat question or `[yes / no]` offer, and never says STOP AND WAIT. Each gate resolves one of three ways, listed in the command's `## Unattended mode` section: (a) a documented default; (b) a value the caller supplied as a flag; (c) **blocked**: the command writes its contract with `worker_status: blocked` and the exact question in `blocked_question` (WC-4), and stops. What the worker does next is fixed by the brief (WC-3).
- **WC-4. One report file, known before dispatch, written on every outcome.** In unattended mode the command writes `<report-dir>/return-contract.yaml`, where `<report-dir>` is the one report directory the brief passes (section 1): either the command's own directory-valued `--output` / `--output-dir`, or `--report-dir`. The coordinator therefore knows the path before dispatch even when the command's own deliverable lands at a generated or fixed location (for example workflow's `TASK-WF-<subject>-<YYYYMMDD>-<HHMMSS>` package, cleanup-audit's `.claude-audit/`, implement's ledger, research's `claudedocs/research_[topic]_[timestamp].md`); the contract then points at that deliverable.
  - The worker fields are top-level keys: `worker_contract_version` (`"1"`), `worker_status` (one of `succeeded`, `partial`, `failed`, `blocked`), `command` (the exact command line), `report_path` (the main human-readable deliverable, if any), `artifacts` (every other file written), `blocked_question` when blocked, and `reason` when failed (for `/sc:implement`, also when blocked, carrying the STOP code).
  - `artifacts` leaves out paths git ignores and paths outside the repository, because WC-9 stages every listed path and git refuses them. This applies to every command's `artifacts` list, including a fixed list in the command's own section.
  - The status field is named `worker_status`, not `status`, because existing contracts already use `status` with other values (`success | partial | failed` in workflow's and adversarial's contracts; reflect's `stopped-precondition`). A command that already writes `return-contract.yaml` in the report directory itself (brainstorm and reflect, `<output>/return-contract.yaml`) keeps every existing field, including its own `status`, and adds the worker fields beside them. Where its own contract lives elsewhere (workflow's package; adversarial's `<output>/adversarial/return-contract.yaml`, whose fields sit in a nested `return_contract:` block), the worker contract at `<report-dir>/return-contract.yaml` lists that file in `artifacts` and the command's own file is left unchanged.
  - Mapping from a command's own status: `success` → `succeeded`, `partial` → `partial`, `failed` → `failed`, `stopped-precondition` → `failed` (precondition in `reason`), and the flag-STOP `blocked` of impact and graph → `failed` (the STOP in `reason`).
  - The contract is written on success, failure, blocked and partial outcomes, including stops before any other output exists.
  - Under `--unattended` with no report directory, or with both a directory-valued output flag and `--report-dir`, the command does no work, writes nothing, and prints in chat the exact error `unattended mode needs exactly one report directory: --report-dir <dir>, or this command's own directory output flag`; WC-5 then gives `failed` because no report exists.
  - The worker passes the contract path as `worker_done --report-path`. Orca does not check the file, so the coordinator opens it.
```

### .dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/02-brainstorm/merged-requirements.md:322-323

```markdown
5. **[REQ-16]** The only question asked inside a gate is the safety route (GR12, section 8.1): a possible safety finding that was graded non-blocking is shown to the person before the gate passes. Nothing else halts an attended run for a person in version 1: a classifier verdict of SHOW_USER, or a `consumer-unknown` row, leaves the reviewer's label in force, tags the row (`unsettled` or `consumer-unknown`), and puts it first in the end-of-run offer.
6. At the end of the run, and at any escalation halt, the top-level session shows the offer (section 6.3). It never offers per loop. During stage 2 of the rollout, a carrier's per-run offer replaces the output style's "once per loop" ask for that run; the output-style ask applies only at gates with no carrier offer, and the two test pins on that text move at stage 3 (section 12).
```

### .dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/02-brainstorm/merged-requirements.md:430-441

```markdown
### 6.4 Unattended runs

<!-- Source: Base (original, modified) - return contract replaced per Change #PC-22 (three keys, visible capture failure; BW-09); tracked-path and nesting rules per RM-1; safety route per Change #PC-10; absence rule per RM-5; final report line and judge-call rule from Variant 3 section 4.6 -->

- The run records only. It writes the ledger and keeps `report_path` as its main report. It lists the ledger in `artifacts` only when the ledger is a tracked path (WC-4 keeps gitignored paths out of `artifacts`, `WORKER-CONTRACT.md:34`) [V]. Follow-ups alone never change `worker_status` from `succeeded`.
- **[REQ-12]** The return contract gains exactly three keys: `follow_up_ledger` (the path), `follow_up_counts` with `follow_up`, `note` and `show_user`, and `follow_up_capture_state` (`complete`, or `incomplete` with a reason). `follow_up_capture_state: incomplete` maps to `worker_status: partial`, added to the WC-4 status mapping. Because WC-4 enumerates the top-level keys (`WORKER-CONTRACT.md:33`) [V], each key is an edit to `core/WORKER-CONTRACT.md`; the old claim that the contract already allows extra keys was wrong. The coordinator duties name the three keys as things to read (the coordinator opens the contract, `WORKER-CONTRACT.md:39`) [V].
- `show_user` counts all three needs-your-decision groups (`consumer-unknown`, `unsettled`, `protected-risk-dispute`).
- Nested runs keep their own ledgers. A parent sees them only through the nested return contracts and never counts them twice.
- A possible safety finding graded non-blocking (GR12) makes the run `worker_status: partial`, is counted in `show_user`, and is named in the final report line. With no person reachable, the row is recorded and the run does not wait.
- A classifier verdict of SHOW_USER means the reviewer's own label stands and the row is tagged `unsettled`.
- Filing is done by the coordinator or the top-level session after the person says yes. Workers have no outward actions, and `/sc:issue` is on the never-as-worker list [V: `WORKER-CONTRACT.md:23`]. Workers also make no paid external judge call; external classifier experiments belong to the coordinator (section 7.8).
- The final report line states the counts, the ledger path, the capture state and "recorded only, no issue created".
```

### .dev/tasks/to-do/TASK-WF-blockerStage0-20261116-021044/TASK-WF-blockerStage0-20261116-021044.md:130-130

```markdown
Edit PF `02-brainstorm/merged-requirements.md` where the program results made it stale, and write the list of edits to `./artifacts/spec-reconciliation.md`. The edits: the thresholds bullet of section 7.4 (the sentence that says 30 to 40 rows leave a held-out half of 15 to 20 rows; the table has 318 rows and the held-out half is the set of Task 5); the "Missing table" row and the "Table" row of the section 7.6 table (the table exists and scored 318 findings with threshold 4); stage 0 of the section 12 table (steps 0a and 0c are not skipped); the section 14 risk RK8 ("Over-fitting the classifier to 30 to 40 rows", spec line 1011) and the section 17.3 line about "a calibration table of 30 or more scored findings" (spec line 1108), both stale because the table exists and has 318 rows; and any other line of section 17 or Appendix A that says the table is empty or absent (a Grep for "empty" found none when this plan was written; the task re-runs it and records what it finds in `./artifacts/spec-reconciliation.md`). Add one sentence to section 7.2 that M, C and E are answerable only with code-supplied inputs, citing PF `08-test/results.md` and `./artifacts/classifier-input-availability.md` (those questions were at chance in the text-only variant). Then draft three further edits, each marked in the spec as "proposed, for owner acceptance at the stage 1 go": (a) in the section 12 table, a definition of "safety miss" for the stage 3 entry count: a finding that a later review or the owner confirms is a security, data-loss or safety-boundary risk that a shadow run recorded as a follow-up or Note and did not route through the GR12 safety route; (b) in the section 12 stage 2 row, the exit numbers made measurable: ledger volume per run, the share of rows tagged `consumer-unknown`, offers made and answered, and the shadow agreement figures of the classifier against the reviewers' labels; (c) in the section 12 stage 3 row, a pointer to the revert triggers RT1 and RT2 of section 13.2 and metric M12 of section 13.1 as the audit-window numbers (quote their existing text; do not redefine them). Also record, in sections 10 and 12 of the spec, three staging decisions: the merge-rule allow-list in `refs/scale-map.md` lists files by path only and the plugin mirror joins it only in stage 4; `agent_template_analysis.md` gets the merge-rule text only and the registry keeps exactly 11 `digest` rows; T3's `src/superclaude` check applies to `digest` and `canonical` rows only and a `pointer-only` row is checked only once its pointer is present.
```

### .dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/stage-requests/README.md:13-21

```markdown
## Stage ledger

| Stage | Request file | Base tasks (revised plan) | Package id | Owner go (date, where) |
|---|---|---|---|---|
| 0 Measurement | `stage0-request.md` | 1 to 10 | `TASK-WF-blockerStage0-20261116-021044` (generated 2026-11-16; its pre-execution review says NEEDS-REVISION, 2 blocking findings, so revise before running it) | not needed (no change under `src/`) |
| 1 Offline scaffold | `stage1-request.md` | 11 to 25 | | |
| 2 Shadow | `stage2-request.md` | 26 to 30 | | |
| 3 Pilot | `stage3-request.md` | 31 to 40 | | |
| 4 Propagation | `stage4-request.md` | 41 to 46 | | |
```

### .dev/reflect/pre-TASK-WF-loosenBlockerRev-20261115-210254-20261115211007/REPORT.md:39-55

```markdown
| # | Blocking | Finding |
|---|---|---|
| F1 | yes | The three owner gates (four go points in PLAN:20) cannot be enforced: `/sc:implement` has no phase option, no pause path, ignores a plan edited after the first task, and QA anchors a constraint breach only in a diff. |
| F2 | yes | Task 31 only reports the seeded-recall result and Task 33 depends on it finishing, not passing. A stronger `Depends on` line would gate nothing because `/sc:implement` ignores it; only an acceptance line on Task 33 works, and Task 31 cannot move out of Phase 4. |
| F3 | yes | Task 40's allow-list names the plugin mirror of `rule.md` and requires every named file to exist, but Task 46 creates the mirror later; Task 13's allow-list text does not list it. |
| F4 | yes | Task 41 gives `agent_template_analysis.md` a digest and a `v2` registry row, but the registry has exactly 11 digest rows without it and the file has no definition sentence. |
| F5 | yes | Task 25's T3 check fails on `commands/spec-panel.md:220` (and its plugin twin, line 218, and the installed variants). |
| F6 | yes | Later tasks make earlier acceptance lines false (Tasks 16, 25, 27, 13), so the final review cannot pass and the package cannot archive. New, from the probe. |
| F7 | yes | The fresh-findings set and the held-out split are never evaluated by any task. |
| F8 | yes | "Safety miss" is defined nowhere, and the stage 2 and 3 exit numbers have no task that measures them, so the owner has no numbers to read at the gates. New, from the probe. |
| F9 | no | Task 46 copies the skill folder before adding the plugin `canonical` registry row (part of the F3 combined fix). |
| F10 | no | The seeded-recall pass line has no minimum sample size. |
| F11 | no | Task 31 does not alternate pass order or require fresh spawns. |
| F12 | no | T3 may fail a `pointer-only` row before its pointer exists. |
| F13 | no | Wording-dependent scan trips: `scale-map.md` naming the three phrases, `rule.md` quoting the old sentence. |
| F14 | no | Coverage-matrix omissions in the review run. |
| F15 | no | Installed reference files cite package-relative `.dev/` paths. |
```

## Coverage slice

| Requirement / Task | Card ID | Status | Grounding |
|---|---|---|---|
| INF-002: The old definition still decides every gate outcome in this stage. | Task 2 | covered | source.md:3 |
| INF-005: State this is stage 2: the sweep only records (`promote` off), the classifier has no autho | Task 2 | covered | source.md:11 |
| INF-006: Stage 3 starts only after the owner reads this package's summary and says go; the stage 3  | Task 7 | covered | source.md:11 |
| INF-007: The halt-offer text goes beside each cap sentence in the task skill and in tech-research o | Task 2 | covered | source.md:12 |
| INF-008: Acceptance quotes the cap sentence "After 2 fix cycles (3 reviews), HALT and escalate to t | Task 2 | covered | source.md:12 |
| INF-015: No edit of `pragmatic.md`, `rf-qa.md`, `rf-qa-qualitative.md`, `rf-analyst.md`, templates, | none | partial | PLAN:22 names part of the list; no task or check covers rf-qa.md, rf-qa-qualitative.md, rf-analyst.md, templates, rule prompts |
| INF-016: Do not change `sc-implement-protocol/refs/qa.md`, the own-scale primitives, the cap of 2 f | none | covered | PLAN:22 |
