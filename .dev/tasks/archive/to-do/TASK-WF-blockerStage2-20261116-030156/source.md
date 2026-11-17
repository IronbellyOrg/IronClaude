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

## Revision 2 (2026-11-16)

Edited in place from `stage-requests/revision2-brief.md`. The plan file name, slug and frontmatter are unchanged. The pre-execution review of this stage did not finish; its three reviewer cards were verified against the live files before use, and the claims relayed from one advocate's Round 2 were verified the same way.

### Shared decisions applied

- **Decision 1 (retired carriers).** Every task that edited `src/superclaude/skills/task/SKILL.md` is dropped (old Task 2 and the task-skill half of old Task 5). The Constraints name the task skill, task-builder and `rf-task-builder.md` as not edited. The plan re-pins only the active carrier's part of shared tests (tech-research; the `/sc:implement` protocol).
- **Decision 2 (follow-up carrier).** The sweep call and the printed list moved from the task skill's "Post-Completion Validation (Final Phase Only)" to the final review step of `/sc:implement`: `SKILL.md` "Done" and the archive gate of `refs/managed-workspace.md` (new Task 3). Record and print only: one read-only call, no `--promote`, no `--write`, no question. `refs/qa.md` is not edited (SHA-256 `93e232f5d49207624c24da25bc6f2e9a0686b4f7f7ca99a38e4b95f56edaf004`, source and plugin twin equal, recorded in Task 1 and compared in Tasks 3 and 8). The once-per-run offer question stays with the top-level session through the output style (changed from per loop to per run at stage 3) and with the consent-bound filing path (OD15); the Constraints say so in one sentence.
- **Decision 3.** tech-research keeps its ledger-writing edit (Task 4); no sweep, no offer, and the halt-offer sentences beside its two cap sentences are dropped because no offer exists in this stage.
- **Decision 4 (plugin surface).** No new plugin surface. The one existing hand-kept twin touched is `plugins/superclaude/skills/sc-implement-protocol/` (two files, copied byte for byte in Task 3), because `test_h_implement_protocol_plugin_twins_byte_equal` and the managed-workspace mirror check in `test_reflect_input_snapshot.py` pin it. Registry counts are not touched by this package.
- **Decision 5 (ledger).** `follow-ups.md` stays a separate file; no mapping to `review-ledger/1`; `ledger.py` is not edited.
- **Decision 6.** No `/sc:implement` run, no commit, no push; `.dev/tasks` staged only.

### Review findings

- **R1-1, R3-1 (no command exists for the writer, safety route or sweep): applied.** Verified: `src/superclaude/cli/review/__init__.py` registers nine subcommand modules and none for these. New Task 2 builds `follow_ups_cmd.py` (group `follow-ups`: `write`, `safety`, `sweep`, `summary`) and registers it. Ownership: stage 1 owns `classify_cmd.py`; this package owns `follow_ups_cmd.py` because it builds `sweep.py`. Cross-stage need reported.
- **R1-2, R3-3 (no `--unattended` branch for the offer): applied by removal.** No offer is made in this stage; the sweep asks nothing; the safety route records and does not wait when nobody is reachable. Task 5 adds a test that the unattended commands make no GitHub call and ask no question. The task skill paragraph pinned by `test_task_skill_returns_the_qa_halt_to_an_unattended_caller` is no longer touched. The wording "except the GR12 safety route" was added to the Constraints.
- **R1-3, R2-1 (safety-miss count not computable from ledgers): applied.** Verified: the stage 0 definition needs a later confirmation that no ledger holds. Task 8's script takes `--confirmed-misses <file>` and prints "not computable" without it. The definition is marked proposed in the spec; the Constraints say so.
- **R1-4, R3-2 (no live judge): applied.** Verified: only `FixtureJudge` and `ReviewerJudge` exist (stage 1 Task 9). Live shadow rows read `classifier=unavailable` unless the run owner holds a recorded answers file; Task 8 splits agreement by judge id, prints the `unavailable` count and counts no reviewer-label row.
- **R1-5 (replicate rule per agent): applied** in Task 7 (each agent is its own judge id, median of 3, blind table only, per-agent figures).
- **R1-6, R2-2 (stage 3 entry sentence incomplete): applied.** "zero safety misses and no capture failure" in Task 8 and the Constraints.
- **R1-7, R2-3, R3-4 (Task 6 inputs): applied.** Task 7 names PF `04-historical/master-table.md`, PF `05-scoring/consensus.md`, `stage0b-sample.md`, `fresh-findings.md` and `stage0-heldout-ids.json`, and counts `@E2` rows separately (the supplier runs no subprocess). Task 1 checks that the ledger holds the stage 0 and stage 1 package ids.
- **R1-8 ("Findings Consolidation" ambiguity; no-edit list): partly applied.** The task skill is no longer edited, so the ambiguity is moot (not applied). The request's no-edit list is copied into the Constraints (applied). Advocate claim that the phrase appears at two sites of the task skill: verified, relevant only to the dropped task.
- **R2-4, R3-6 (checks missing for edited text): applied.** Verified: `pytest -k tech_research` selects nothing (95 deselected), because test ids spell `tech-research`. Tasks 3 and 4 now name the test files explicitly, including `test_review_prompt_overrides.py`, `test_worker_contract.py` and the `/sc:implement` pin tests. Task 8 adds the `git diff --stat HEAD` no-edit check.
- **R3-5 (owner go checked after edits): applied.** Task 1 opens with "Before any edit".
- **R3-7 (sweep has no input contract): applied.** Task 1 fixes arguments (ledgers, deliverables, kind) and counts skipped kinds.
- **R3-8 (tech-research halt may show no offer): not applied.** No offer exists in stage 2 by decision 2, so there is nothing to show at a halt.

### Advocate claims

- **WORKER-CONTRACT writes `return-contract.yaml` only under `--unattended`: verified (WC-4).** `/sc:implement` has no unattended section yet (its WC-9 rows are deferred) and tech-research has none. Task 5 names `follow-ups summary` as the producer and Task 8 states the limit that no command emits the keys live yet.
- **Shadow summary must split by judge id, print the `unavailable` count and count only non-reviewer judges: applied** (Task 8).
- **Reviewer brief wording and the tier source: applied** (Task 4: "for every finding you grade non-blocking under your current definition"; the tier comes from `refs/scale-map.md`).

### Existing tests named in the plan

`tests/skills/test_implement_severity_static.py`, `tests/skills/test_review_severity_rule.py`, `tests/skills/test_task_workspace_lifecycle.py`, `tests/skills/test_task_workspace_smoke.py`, `tests/skills/test_workflow_archive.py`, `tests/skills/test_implement_saved_prompt_rule.py`, `tests/skills/test_reflect_input_snapshot.py`, `tests/skills/test_codegraph_adoption.py`, `tests/commands/test_impact_command.py`, `tests/skills/test_worker_contract.py`, `tests/unit/test_cli_install.py`, `tests/skills/test_review_prompt_overrides.py`, `tests/skills/test_review_severity_mapping.py`, `tests/review/test_review_cli.py`.

### Task count

7 before, 8 after (old Task 2 dropped; old Task 1 split into Tasks 1 and 2; Task 3 retargeted; old Tasks 4 to 7 became 5 to 8).

## Revision 3 (2026-11-16)

Fix cycle 2, edited in place from `stage-requests/revision2-brief.md` (with the section named Revision 3) and the review output `.dev/reflect/pre-TASK-WF-blockerStage2-20261116-030156-20261116174316/REPORT.md` (4 blocking, 14 non-blocking, one dropped to Grounding Gaps). Each finding was checked against the live files before the plan changed. The plan file name, slug, frontmatter, task count (8) and phase count (4) are unchanged. The `/sc:implement` design (record and print only, `qa.md` untouched, closed interrupt list, the two plugin-twin pins, the static scan) is kept.

### Blocking findings

- **MB-1 (safety-miss confirmations are ambiguous across runs): applied.** Verified: spec section 6.2 makes row ids run-scoped (`FU-000001` upward, per run). Task 8's `--confirmed-misses` file now holds `<run_id>:<row id>` entries (split at the last colon), each matched to the ledger whose metadata `run_id` equals its left part; a bare id is rejected, an unmatched entry makes the figure "not computable". The test adds two runs that both hold `FU-000001`. The Constraints (safety misses) state the format.
- **MB-2 (judge agents cannot be code-informed; contested): applied.** Verified: spec section 7.1 says code does every exact check first and passes the result in as state; stage 1's `questions_to_ask` asks M only with a supplied required-item list, C only with supplied constraint lines and E only with a verified evidence excerpt. Task 7 now runs the supplier first (Step A, `stage2-eval-inputs-<set>.json`), builds one input file per set holding the blind-table columns plus the supplier's inputs and the question ids to answer (Step B; still no consensus, grade, label or scale map), and has the agents answer only those ids, every other question recorded UNSET or NA by code (Step C). The limit that the agents see the blind table plus the supplier's inputs, not the full finding record, is stated in the report. The Constraints and acceptance lines say the same.
- **MB-3 (GR12 safety row must make the run `partial`): applied.** Verified: spec section 6.4 says "A possible safety finding graded non-blocking (GR12) makes the run `worker_status: partial`", and `WORKER-CONTRACT.md` WC-4 has no such mapping. The three keys cannot carry the signal. `follow-ups safety` now prints a last line `worker_status_signal: partial` (the ledger holds a row tagged `protected-risk-dispute`) or `none`; Task 5 adds the mapping and the producer to the WC-4 status-mapping bullet after the existing pinned text, and three tests (text mapping removed fails, safety output over fixtures).
- **MB-4 (phase 3 and 5 analyst and qualitative reviewers get no fields; two edited templates are legacy): applied, narrowed.** Verified in `tech-research/SKILL.md`: "Report Validation QA" and "Qualitative QA" are marked LEGACY ("Do NOT use ... for Phase 6 QA"); Step 3.1 and Step 5.N+1 run `rf-analyst` and `rf-qa-qualitative` agents, and the qualitative agents have no template of their own. Task 4 now edits four active templates (Research Analyst, Research QA, Synthesis QA, Lens-Specific QA), adds one new line under Step 3.1 and one under Step 5.N+1 covering every reviewer of the step, gives analysts a "Non-blocking findings" table, and states that the two legacy templates are not edited. `follow-ups write` finds columns by header name. Task 6's T9 test follows (four prompts and the two lines). The fidelity gate (Step 6.7) and anti-omission gate (Step 6.7b) write no ledger row in this stage; Task 8 states that limit.

### Non-blocking findings

- **MN-1 (tag persistence): applied.** Task 2 `safety` saves the tag through the stage 1 writer (or the command does when the route only returns rows); a test shows the tag in the ledger after `safety` and after a second `write`. The wiring file states which case holds.
- **MN-2 (tier lookup and table layouts): applied.** `write` reads the label-to-outcome pairs from the lens-scale row of `refs/scale-map.md` at run time and parses both reviewer layouts and the analyst section; fixture reports of all three and a remapped-label test are in Task 2.
- **MN-3 (the sweep finds no ledger in a `/sc:implement` run): applied.** Verified: a grep of the protocol folder for "follow-up" finds only the verdict note in `refs/ledger.md`. `sweep` prints `ledgers found: N` first; Task 3 prints "No follow-up ledger was written in this run." for 0 and the recorded-and-not-filed line only for 1 or more; Task 3 and Task 8 state the limit.
- **MN-4 (Task 1 entry check too narrow): applied.** Task 1 also checks `classify --help`, `classify_cmd` import, `refs/scale-map.md` and `refs/registry.yaml`.
- **MN-5 (no call line): applied.** The call is a one-line fenced code block in each file; prose with "never `--promote` and never `--write`" sits on other lines; stage 3's call-line wording still holds.
- **MN-6 (tech-research has no unattended mode): applied.** Task 4 says tech-research always runs the attended route and calls `safety` without `--unattended`.
- **MN-7 (printed list had no producer): applied.** `sweep` prints counts, relative ledger paths and `show_user` rows first, so Task 3 needs no second command.
- **MN-8 (file count in the Constraints): applied.** Reworded to "more files, at least `sweep.py` and `follow_ups_cmd.py`" (the exact count is not claimed).
- **MN-9 (ban on judges versus `--judge-answers`): applied.** The ban names live judges; `--judge-answers` reads recorded answers through `FixtureJudge`.
- **MN-10 (Task 4 body versus `grep -ci sweep`): not applied.** Both requirements are met together (the one sentence that says there is no sweep avoids the word); the review itself found no defect.
- **MN-11 (`./artifacts/` from the repository root): applied as a precaution (the finding was dropped to Grounding Gaps as inferred).** The Task 7 and Task 8 commands now say they run from the package folder.
- **MN-12 (empty confirmation file printed 0): applied.** The file needs a `reviewed: <date> by <name>` line; without it (empty file included) the figure is "not computable". Cross-stage: the stage 3 entry describes the file as "one row id per line" and "an empty file means none"; it must change to the format above.
- **MN-13 (no empty-input convention): applied.** New Constraints bullet; Task 7 adds `classifier_eval.py` and its test; Task 8's test covers zero runs and zero non-blocking rows.
- **MN-14 (`incomplete` capture reset by a later write): applied.** `incomplete` is sticky in a ledger; tested in Task 2.
- **MN-15 (three probe items): INV-006 applied (the paragraph title is pinned in Tasks 3 and 6); INV-010 applied (the new paragraph follows the closing fence of the `FINAL:` code block); INV-007 partly applied (fidelity and anti-omission reviewers excluded with a stated limit; the registry tuple count belongs to stage 1 and is not changed here).**

### Task count

8 before, 8 after. No task added or removed; the registry counts (11 digest, 1 canonical, 2 pointer-only, 5 installed-only) are not touched by this package.
