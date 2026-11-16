---
schema: workflow-plan/1.2
source: ./source.md
strategy: systematic
depth: standard
slug: TASK-WF-loosenBlockerCla-20261115-133045
version: "1"
priority: Medium
created_date: "2026-11-15"
---

# Loosen blocker classification across the review loops (issue #552)

Source: ./source.md
Goal: Review gates grade each finding by what changes if the flawed text is corrected, record every non-blocking finding in a follow-up ledger with a once-per-run offer to file them, keep security, data-loss and safety findings blocking, and measure a blocker classifier in shadow mode without giving it any authority.

## Constraints

- Spec: the merged spec `02-brainstorm/merged-requirements.md` inside the program folder `BLOCKER-CLASSIFICATION-PROGRAM-20261115` (found by that folder name under the repository's task folder). This plan calls that folder PF and the spec file the spec. Section numbers, requirement ids (REQ-nn), loop changes (L1 to L6), guardrails (GR1 to GR12), tests (T1 to T17) and owner decisions (OD1 to OD17) refer to the spec. PF also holds the 5-run results in `08-test/results.md`, the reconciliation in `09-plan-input.md`, the blocker characteristics in `06-blocker-characteristics.md` and the classifier sketch in `07-classifier/`.
- Stage gating from spec section 12: Phases 1 to 3 are stages 0, 1 and 2 and can run in one pass. Phase 4 is stage 3 (the pilot) and Phase 5 is stage 4. Their entry conditions need things no executor can produce: the owner's go, at least 5 observed shadow runs with zero safety misses, seeded recall met, and stage 0c done. Run `/sc:implement` on Phases 1 to 3 first; do not start Phase 4 until the owner says so in chat, and do not start Phase 5 until the owner says so after the pilot's audit window.
- Owner decisions use the spec's recommendations unless the owner changes them: OD1 skill folder `sc-review-severity`; OD2 once per run plus at any escalation halt; OD4 the classifier has no authority in version 1; OD9 reviewer-named consumer, code-checked where quotable; OD11 replace label-max merging at all 13 lines in 10 files, staged; OD12 yes; OD13 short Note rows; OD14 a finding with an unknown consumer keeps the reviewer's label (no deferral); OD15 consent-bound body file posted by the attended top-level session; OD16 option (b) at stage 3. OD3 (finding text leaving the machine), OD5 to OD8 and OD10 are not decided here and no task depends on a different answer.
- Not built here: any Jev or other external judge call, any TypeSafe account or key, a Jev or LLM judge class (they wait for OD3), any change to `src/superclaude/skills/sc-implement-protocol/refs/qa.md` (it keeps its own scale), any change to the own-scale primitives listed in spec section 9.3 as unchanged, the 35 percent score target, and any change to the cap of 2 fix cycles.
- Classifier facts that bind every classifier task: the 5-run test of PF `08-test/results.md` used a text-only stand-in judge and got agreement with the panel of 58.5 percent (Cohen's kappa 0.27), and the missing-item, constraint and contradiction questions (M, C, E) were at chance without code-supplied inputs. So M, C and E run only when code supplies the required-item list, the constraint lines and the verified evidence, the "M or C is Y gives BLOCKING" row is never enabled for any gate in this plan, and confidence is reported as an ordinal band, never as a probability.
- `src/superclaude/` is the source of truth. Edit there, then run `make sync-dev`; never stage anything under the project `.claude/` folder (only `.claude/settings.json` is tracked). Installed primitives name installed paths (`~/.claude/skills/...`) first and project `.claude/...` second, never a `src/superclaude/` path.
- Python work uses UV only: `uv run pytest ...`, never `python -m` or bare `pip`.
- Task-owned evidence and generated outputs go under `./artifacts/` in this package.

## Phase 1: Close the measurement stage (stage 0)

## Task 1: Freeze the pattern inventory of spec section 10

Re-run, with plain `grep -rn` (not the Grep tool, which skips gitignored folders and so misses the project `.claude/` copies) over `src/superclaude`, `plugins/superclaude` and the project `.claude/` folder, every pattern the spec lists in section 10: the definition sentence `Grade every review finding as blocking or minor` (spec: 11 files), `Blocking is a real defect` (11), `Minor findings never fail a review` (11), `at most 2 fix cycles \(3 reviews\)` (12), `CRITICAL and IMPORTANT findings are blocking` (7), `follow-up candidates` (3 files, 7 lines), `2 fix cycles` (22 files, 120 lines), the two merge-rule patterns of section 10.3 (13 lines in 10 files), the tasklist pattern `High or Medium` and `Medium (blocking)` in `src/superclaude/skills/sc-tasklist-protocol/SKILL.md` (7 lines), and the REQ-30 fixed FAIL-trigger patterns `= FAIL`, `that's a FAIL`, `regardless of severity`, `highest severity`, `never minor`, `always IMPORTANT` over `src/superclaude/agents`, `src/superclaude/skills`, `src/superclaude/templates` and `src/superclaude/rules`. Write the counts and every hit line to `./artifacts/stage0-inventory-freeze.md`.

Acceptance criteria:
- `./artifacts/stage0-inventory-freeze.md` exists and has one table row per pattern with the columns pattern, scope, spec count, observed count and difference.
- Every REQ-30 FAIL-trigger pattern has its hit lines (file, line number, text) listed, so later tasks use this list and not a remembered one.
- A section "Differences from the spec" lists each pattern whose observed count differs from the spec count; with no difference it says so in one line.
- The file records the exact commands used so the freeze can be re-run.

## Task 2: Run the retrospective escape test on run 2 (spec section 8.4, stage 0b)

Take a random sample, with a recorded seed, of de-duplicated minor findings from Gates 2 to 5 and the final validation in the run-2 QA folder `TASK-RESEARCH-review-panel-run2-20261114-075454/qa/` (the folder is under the repository's task folder; it holds the cycle-control files and lens reports). For each sampled finding, test by code whether its flawed text or figure appears uncorrected in the run-2 final report `RESEARCH-REPORT-review-panel-unification-run2.md` in the parent folder. Write the check as `./artifacts/stage0b_escape.py` (run with `uv run python`), the sample list as `./artifacts/stage0b-sample.md`, and the result as `./artifacts/stage0b-escape-test.md` with hits over n and a Wilson 95 percent interval. State the limit the spec names: the report was itself produced under the override, so a minor that was corrected anyway cannot be told apart from one that never mattered.

Acceptance criteria:
- `./artifacts/stage0b-escape-test.md` reports hits, n, the seed and a Wilson 95 percent interval computed by `./artifacts/stage0b_escape.py`, and states the limit in one paragraph.
- Re-running `uv run python ./artifacts/stage0b_escape.py` with the recorded seed reproduces the same sample and the same count.
- n is at least 60 or equals the size of the whole frame when the frame is smaller; the file says which.
- `./artifacts/stage0b-sample.md` lists each sampled finding with its source file and the quoted flawed text or figure.

## Task 3: Re-grade the scored table under the old and the new rule text (spec stage 0c)

Depends on: Task 1

Use the 318 findings in PF `04-historical/master-table.md` through the blind copies `blind-table-1.md`, `blind-table-2.md` and `blind-table-3.md` in the same folder (columns ID, Category, Description brief, Context only). Spawn three blind agents that did not write the rule or the spec. Each re-grades every finding twice, in a paired design with the order of the two texts alternated: once under today's rule text (the lines of `src/superclaude/output-styles/pragmatic.md` from line 221 to line 231) and once under the digest of spec section 4.1 (REQ-01, the block between the quoted lines). Record each agent id and every grade in `./artifacts/stage0c-grades.jsonl` and write `./artifacts/stage0c-regrade.md` with the confusion matrix against the panel consensus in PF `05-scoring/consensus.md` (blocker at mean 4.0 or higher), how many findings graded blocking under the old text become non-blocking under the new text, the spread among the three agents, and the rows that moved from non-blocking to blocking.

Acceptance criteria:
- `./artifacts/stage0c-grades.jsonl` has 318 findings times 3 agents times 2 texts, 1908 grades, each with agent id, text version and the order position.
- `./artifacts/stage0c-regrade.md` carries the confusion matrix with counts, the old-to-new movement counts and the three-agent spread, and states that the table holds only findings filed as blocking.
- The file lists the ids of the agents used and states that none of them wrote the digest or the spec.
- Rows the old text and the new text grade differently and that the panel calls a blocker are listed by id, since they are the recall risk.

## Task 4: Split the scored table into a cluster-aware held-out set

Depends on: Task 2

Split the 318 findings of PF `04-historical/master-table.md` so that no defect cluster has rows on both sides. The clusters are the six keyword clusters of PF `06-blocker-characteristics.md` (the Phase 0 acceptance check that cannot pass, the `--unattended` flag landing before gates convert, the contract status vocabulary, the answer-as-flag and approval-gate rule, the git push classifier, and the missing `target_sha` on the resume path); rows in no cluster are split at random with a recorded seed. Add the stage 0b sample of Task 2 as a separate set of findings that a reviewer called minor. Write `./artifacts/stage0-heldout-split.md` and `./artifacts/stage0-heldout-ids.json`.

Acceptance criteria:
- `./artifacts/stage0-heldout-ids.json` lists the finding ids of the tuning half, the held-out half and the reviewer-called-minor set, with the seed.
- No cluster named in PF `06-blocker-characteristics.md` appears in both halves; the split file states each cluster's side.
- The two halves differ in size by at most 20 percent unless a cluster is too large to place, and the file says so when it is.

## Task 5: Correct the stale statements in the spec

Depends on: Task 3, Task 4

Edit PF `02-brainstorm/merged-requirements.md` where the program results made it stale, and write the list of edits to `./artifacts/spec-reconciliation.md`. The edits: the thresholds bullet of section 7.4 (the sentence that says 30 to 40 rows leave a held-out half of 15 to 20 rows; the table has 318 rows and the held-out half is the set of Task 4); the "Missing table" row and the "Table" row of the section 7.6 table (the table exists and scored 318 findings with threshold 4); stage 0 of the section 12 table (steps 0a and 0c are not skipped); and the Appendix A or section 17 line that carries the "empty table" statement. Add one sentence to section 7.2 that M, C and E are answerable only with code-supplied inputs, citing PF `08-test/results.md` (those questions were at chance in the text-only variant).

Acceptance criteria:
- The spec no longer says the scored table is empty or that the held-out half is 15 to 20 rows (`grep -n "15 to 20\|was empty"` over the spec returns no stale claim).
- `./artifacts/spec-reconciliation.md` lists each edited line with its old and new text.
- Section 7.2 of the spec carries the M, C and E sentence with a pointer to `08-test/results.md`.

## Phase 2: Offline scaffold (stage 1)

## Task 6: Create the skill folder entry file

Depends on: Task 5

Create `src/superclaude/skills/sc-review-severity/SKILL.md` (the folder does not exist today, confirmed). It states the purpose, which ref is read by whom (the table of spec section 9.1), the rule version `v2`, and "Delegate-only, no slash command", in the style of the existing `sc-bare-review` skill. Do not name any `src/superclaude/` path inside it.

Acceptance criteria:
- `src/superclaude/skills/sc-review-severity/SKILL.md` exists with frontmatter, the five refs named in spec section 9.1 (`refs/rule.md`, `refs/scale-map.md`, `refs/follow-up-ledger.md`, `refs/classifier-questions.md`, `refs/registry.yaml`) and the line "Delegate-only, no slash command".
- `grep -n "src/superclaude" src/superclaude/skills/sc-review-severity/SKILL.md` prints nothing.
- After `make sync-dev`, `make verify-sync` reports the new folder in sync.

## Task 7: Write the full rule with the pinned digest

Depends on: Task 6

Create `src/superclaude/skills/sc-review-severity/refs/rule.md`. It holds the full rule: the three blocking conditions, the Medium and Note classes, the counterfactual test and the table of spec section 4.2, the decision basis of section 4.3, the worked cases of section 5, the table-shape rule, the guardrails GR1 to GR12 of section 8.1, and the digest. The digest is the block of REQ-01 word for word, including REQ-02 (the unknown-consumer sentence), REQ-03 (the precedence sentence) and the cap sentence that today's `src/superclaude/output-styles/pragmatic.md` line 227 holds, placed between the HTML-comment fence lines `review-severity:digest v2 begin` and `review-severity:digest v2 end`.

Acceptance criteria:
- `refs/rule.md` contains exactly one fenced digest whose last sentence equals line 227 of `src/superclaude/output-styles/pragmatic.md` word for word.
- The digest contains the sentences of REQ-02 and REQ-03.
- Every one of the 14 worked cases of spec section 5 appears with its verdict.
- `grep -n "src/superclaude" refs/rule.md` prints nothing.

## Task 8: Write the scale map

Depends on: Task 6

Create `src/superclaude/skills/sc-review-severity/refs/scale-map.md` with one row per family of spec section 9.3: family, defining file, each native label, the shared outcome per label (Blocking, Medium, Note), and either "graded by the three conditions" or "keeps its own model because <reason>". The rows are the 12 families of that table: the CRITICAL, IMPORTANT, MINOR lens scale; the `/sc:implement` `refs/qa.md` checklist; spec-panel; the stoprule rubric and `finding-grader`; the reflect deviation taxonomy; tasklist High, Medium, Low; roadmap validate; `card_convert.py`; findings-v1 and v2; `sc-auggie-review-protocol/SKILL.md:228`; the PR severity router and Auggie rubric; and the code-assigned family. Include the sentence that a keep of a fixed FAIL trigger (L6) is recorded here.

Acceptance criteria:
- `refs/scale-map.md` has a row for each of the 12 families, each naming a defining file that exists in the repository.
- The tasklist row states that Medium is blocking today on 7 lines of `src/superclaude/skills/sc-tasklist-protocol/SKILL.md` and that no stage 1 to 4 task changes it.
- The `card_convert.py` row states that its word translator maps `important` and `medium` to non-blocking while `src/superclaude/agents/rf-qa.md` treats IMPORTANT as blocking.

## Task 9: Write the follow-up ledger reference

Depends on: Task 6

Create `src/superclaude/skills/sc-review-severity/refs/follow-up-ledger.md` from spec sections 6.1 to 6.7: the flow, the ledger contract (metadata block, Items table with its columns, Notes table, Observations, Offers and Filings tables, item states, identity rules), the offer wording with consent binding (REQ-11), unattended behaviour (REQ-12), the filing path (OD15, REQ-13 to REQ-15), the location rule (REQ-07) and "resolve now" (6.7). Keep the cell codec of REQ-10 exactly: entity layer, no backslash before a pipe.

Acceptance criteria:
- `refs/follow-up-ledger.md` contains the Items table columns of spec section 6.2 (`id`, `origin`, `tier`, `source`, `location`, `finding`, `evidence`, `rests_on`, `why_not_blocking`, `tags`, `proposed_fix`, `suggested_type`, `classifier`, `status`, `canonical_id`, `issue_url`).
- The offer wording of spec section 6.3 and the sentence "Nothing is filed until you answer." appear.
- The file states the three tags `consumer-unknown`, `unsettled` and `protected-risk-dispute` and that all three feed the single `show_user` count.

## Task 10: Write the classifier question reference

Depends on: Task 6

Create `src/superclaude/skills/sc-review-severity/refs/classifier-questions.md`: the six decisive questions S, W, E, M, C, D of spec section 7.2 with the S wording "in a way the task did not ask for", the code-supplied input each needs, the Option Q replacement for D at upstream gates, and the optional explanation questions T, F, I and G (they feed no cell of the truth table). Add a version line `question-set v1`. State that M, C and E are asked only when code supplies their inputs and cite PF `08-test/results.md`.

Acceptance criteria:
- `refs/classifier-questions.md` has the six questions with a "Needs from code" column and the line `question-set v1`.
- No question text contains the word "blocking" (`grep -in blocking` over the question table rows prints nothing).
- The file states that a failed or skipped answer is UNSET and never N.

## Task 11: Write the carrier registry with every row set to legacy

Depends on: Task 7, Task 8

Create `src/superclaude/skills/sc-review-severity/refs/registry.yaml`. One row per carrier of the digest, with the logical path relative to the install root, carrier kind, surfaces (source, installed, project `.claude/`, plugin, or `installed-only`), rollout stage, digest version `legacy`, and an own-scale flag. Rows: the 11 definition carriers of spec section 10.1 (`output-styles/pragmatic.md`, `agents/rf-qa.md`, `agents/rf-qa-qualitative.md`, `templates/documents/agent_template_qa.md`, `templates/documents/skill_template.md`, `templates/workflow/01_mdtm_template_generic_task.md`, `templates/workflow/02_mdtm_template_complex_task.md`, `rules/prompts/automated_qa_workflow_qa_prompt.md`, `rules/prompts/doc_code_analyst_qa_prompt.md`, `rules/prompts/documentation_expert_qa_prompt.md`, `rules/prompts/recruiting_expert_qa_prompt.md`), plus `commands/sc/spec-panel.md` and `rules/prompts/document_review_loop_prompts.md` as own-scale carriers of the cap text, and `installed-only` rows for `commands/sc/spec-panel-armb.md`, `spec-panel-diffgate.md`, `spec-panel-ledger.md`, `spec-panel-ponytail.md` and `spec-panel-stoprule.md`. Command rows map the source `commands/<name>.md` to the installed `commands/sc/<name>.md`.

Acceptance criteria:
- `refs/registry.yaml` parses with `uv run python -c "import yaml,sys; yaml.safe_load(open(sys.argv[1]))" src/superclaude/skills/sc-review-severity/refs/registry.yaml`.
- It has exactly the 11 carriers of spec section 10.1 with a source path that exists, all at digest version `legacy` and rollout stage assigned (stage 3 for `pragmatic.md`, `rf-qa.md`, `rf-qa-qualitative.md`; stage 4 for the rest).
- The five spec-panel variants carry the surface `installed-only`.

## Task 12: Build the follow-up ledger codec, reader and writer

Depends on: Task 9

First run the `reuse-auditor` agent on the proposed module against `src/superclaude/cli/review/ledger.py` (schema `review-ledger/1`) and record its verdict in `./artifacts/reuse-audit-follow-ups.md`; share code only where it says reuse-by-import. Then create `src/superclaude/cli/review/follow_ups.py`: one reader and one writer for `follow-ups.md` only (REQ-07 location rule, REQ-08 sole writer with an expected-revision check and atomic replace, REQ-10 entity codec with evidence blocks and a fence longer than any backtick run, identity tuple and observation import that is idempotent, the sort order of spec section 6.2, and the item states). A malformed ledger is preserved and reported, never reset. Create `tests/review/test_review_follow_ups.py` for T7: required columns, a Medium row without `why_not_blocking` is refused, identity never merges on a digest alone, codec round trip for pipes, backticks, a triple-backtick line, literal entities, Unicode and multiline text, a stale writer cannot overwrite a newer revision, a malformed ledger is preserved.

Acceptance criteria:
- `uv run pytest tests/review/test_review_follow_ups.py -v` passes and covers each T7 failure condition above.
- `./artifacts/reuse-audit-follow-ups.md` exists and the module imports from `ledger.py` only where the audit says to.
- Two readers of this ledger do not exist: `grep -rn "follow_ups" src/superclaude/cli/review` shows only the new module and its command wiring.
- `make lint` reports no new findings for the module.

## Task 13: Build the filing state machine

Depends on: Task 12

Add to `src/superclaude/cli/review/follow_ups.py` the Filings table logic of spec section 6.5: batch id as a stable digest of repository, run id, selected canonical ids and purpose; states `prepared`, `posting`, `reconcile`, `filed`, `cancelled`; a body digest compared with the read-back body; a reconcile step that searches for the exact batch marker before any retry; the 60,000-character bound with overflow posted as comments (REQ-15); and the repository guard of REQ-14 (the target comes from the `origin_repo.py` script of `src/superclaude/skills/sc-issue-protocol/scripts/origin_repo.py`; when the target is the IronClaude repository it must be `IronbellyOrg/IronClaude`, never the upstream parent, and any other resolution means stop and record only). The code takes the `gh` call as an injected function so tests never touch GitHub. Create `tests/review/test_review_follow_ups_filing.py` for T8: a resume asks again, a changed set is filed without new consent, a timeout after a successful post creates a second issue, a body whose digest differs is marked `filed`, a repository other than the verified one is targeted.

Acceptance criteria:
- `uv run pytest tests/review/test_review_follow_ups_filing.py -v` passes with a fake `gh` and covers each T8 failure condition.
- No test or module calls the real `gh` or the network.
- Every `gh` argument list built by the module spells `--repo <R>` or `repos/<R>/...` with `<R>` from the resolver and never a `{owner}/{repo}` placeholder.

## Task 14: Build the classifier module

Depends on: Task 10

Create `src/superclaude/cli/review/classifier.py` and `src/superclaude/cli/review/data/classifier_thresholds.json`. The module holds the truth table of spec section 7.3 (version 2, ported from `07-classifier/truth_table.py` in PF and the sketch `02-brainstorm/blocker_truth_table_sketch.py`: states Y, N, U, UNSET, NA; NA reachable only from a deliverable-kind declaration, REQ-19; precedence, the W and E combination of REQ-17, the lift rule of REQ-18), the bands (S: Y at 0.30 or more, N at 0.10 or less; others 0.70 and 0.30), ordinal confidence bands with the replicate rule of spec section 7.4 (median of 3, spread above 0.20 counts as U), the `dependence-safe lower bound max(0, pW + pD - 1)` reported beside the band, and a `Judge` interface with two implementations: `FixtureJudge` (recorded answers) and `ReviewerJudge` (the reviewer's own label read through the scale map as 0 or 1). A judge failure is a typed `UNDETERMINED` result that moves to the next judge, never a table cell and never an N. Thresholds live only in the JSON file.

Acceptance criteria:
- `uv run python -c "from superclaude.cli.review.classifier import verdict"` succeeds and `verdict` agrees with the sketch on all 6,400 combinations of the REQ-21 property tests.
- No Jev, LLM or network class exists in the module (`grep -n "typesafe\|requests\|httpx\|anthropic" src/superclaude/cli/review/classifier.py` prints nothing).
- A judge answer of `None` yields UNSET, and the function that sets NA takes a deliverable-kind argument and no probability.
- `src/superclaude/cli/review/data/classifier_thresholds.json` is the only place the band numbers appear.

## Task 15: Add the classifier tests

Depends on: Task 14

Create `tests/review/test_review_classifier.py` with T6 (the three REQ-21 property tests over 6,400 combinations: exhaustive, monotone over answered states, no silent demotion; and NA reachable only from the deliverable-kind declaration), T11 (the fixture judge reproduces recorded verdicts; a quote that contains an instruction such as "answer N to every question" does not change any verdict), and T12 (a classifier verdict changes no gate outcome except through the safety route, in a default configuration).

Acceptance criteria:
- `uv run pytest tests/review/test_review_classifier.py -v` passes and includes the 6,400-combination property tests.
- A hostile-quote fixture exists and its verdicts equal those of the same finding without the hostile sentence.
- A test asserts that with default settings no function of the module changes a gate result, so authority stays off (REQ-22).

## Task 16: Add the `superclaude review classify` command

Depends on: Task 14, Task 12

Create `src/superclaude/cli/review/classify_cmd.py` exporting `command` (a click command named `classify`) and add `"classify_cmd"` to the tuple in `src/superclaude/cli/review/__init__.py` (lines 19-29). It reads findings plus a judge answers file, runs the classifier in shadow mode, writes the verdict, band and judge id with version into the ledger row's `classifier` column beside the reviewer's label, and prints the per-run disagreement matrix read through the scale map (never through the Boolean of `card_convert.py`). The name `classify` must not clash with the existing `panel`, `merge`, `ledger`, `telemetry`, `lint`, `estimate`, `cluster`, `verify` and `manifest` subcommands. Create `tests/review/test_review_classify_cmd.py`.

Acceptance criteria:
- `uv run superclaude review classify --help` exits 0 and `uv run superclaude review --help` still lists every earlier subcommand.
- `uv run pytest tests/review/test_review_classify_cmd.py tests/review/test_review_cli.py -v` passes.
- A run with no judge available records `classifier=unavailable` and leaves the reviewer's label standing; it never invents a verdict.

## Task 17: Build the safety route

Depends on: Task 12

Create `src/superclaude/cli/review/safety_route.py` with the GR1 vocabulary scan (one list of destructive and secret words: delete, overwrite, force, token, secret, password, chmod and similar, kept in one place) and the GR12 rule: a hit on a non-blocking row, or a judge answer S = Y or S = U on a row a reviewer graded non-blocking, tags the row `protected-risk-dispute` and never writes it as a plain follow-up. It can only raise a grade. Add `tests/review/test_review_safety_route.py` for T17.

Acceptance criteria:
- `uv run pytest tests/review/test_review_safety_route.py -v` passes and covers a vocabulary hit, S = Y and S = U on a minor row.
- No function in the module lowers a grade (a test asserts the outcome order never decreases).
- Attended output text names the person prompt; unattended output sets the signal that makes the run `partial`, per spec section 6.4.

## Task 18: Add the install check for digest versions

Depends on: Task 11

Add `_check_review_severity_digests` to `src/superclaude/cli/doctor.py` and call it from `run_doctor` (REQ-27). It compares the digest versions held by the installed carriers with the packaged registry of `src/superclaude/skills/sc-review-severity/refs/registry.yaml`, reading the packaged registry and not an installed copy (an installed skill folder is skipped once present, so an installed `registry.yaml` can be stale). Add tests to `tests/unit/test_cli_doctor.py`; keep `tests/cli/test_install_retired_mcp.py` (`test_update_and_doctor_never_mutate_and_never_change_their_exit_code`) passing because `run_doctor` must stay read-only.

Acceptance criteria:
- A test in `tests/unit/test_cli_doctor.py` builds an installed tree with a stale digest version and asserts the check reports the mismatch (T13).
- `uv run pytest tests/unit/test_cli_doctor.py tests/cli/test_install_retired_mcp.py tests/cli/test_update_command.py -v` passes.
- With every registry row at `legacy` and every installed carrier legacy, the check reports no mismatch.
- `make doctor` still runs and exits as before.

## Task 19: Add the registry drift tests

Depends on: Task 11, Task 7

Create `tests/skills/test_review_severity_registry.py` for T1 (every registry row's file holds exactly one digest whose flattened body equals the digest section of `refs/rule.md` for that row's version; legacy rows are accepted while at `legacy`), T2 (a reverse scan of the tracked `src/` and `plugins/` trees fails on any file that holds the old definition sentence or a fence opener and is not a registry row; strict mode is a switch, off in this phase), T3 (each pointer names `~/.claude/skills/sc-review-severity/...` before `.claude/skills/sc-review-severity/...`, and no carrier contains `src/superclaude`), T4 (each scale-map row names an existing file and a label present in it) and T14 (a v2 carrier holds the precedence sentence).

Acceptance criteria:
- `uv run pytest tests/skills/test_review_severity_registry.py -v` passes with all carriers at `legacy`.
- A test flips one registry row to `v2` without editing its file and fails, which shows T1 can fail.
- The reverse scan reports a file that holds the definition sentence and is absent from the registry, using a temporary tree in the test.

## Phase 3: Shadow beside the old rule (stage 2)

## Task 20: Build the final-gate sweep

Depends on: Task 12

Create `src/superclaude/cli/review/sweep.py` for GR7: at the last gate before delivery, every open Medium row is re-tested, and a row whose flawed text or figure appears, uncorrected, in a decision-basis section of the final deliverable becomes Blocking at that gate. Today no final gate reads a ledger (`src/superclaude/skills/task/SKILL.md` lines 290-292 run one final validation and name no ledger; `src/superclaude/skills/tech-research/SKILL.md` lines 415-419 enumerate findings and read no ledger). Create `tests/review/test_review_sweep.py` for T16.

Acceptance criteria:
- `uv run pytest tests/review/test_review_sweep.py -v` passes; a seeded Medium row whose flawed figure reaches the final decision basis uncorrected is returned as Blocking, and one that was corrected is not.
- The sweep never lowers a grade and never touches a Note row.
- The module reads only the ledger path that the ledger reader returns (no second reader of `follow-ups.md`).

## Task 21: Make the task skill write the ledger in shadow mode

Depends on: Task 12, Task 17, Task 20

Edit `src/superclaude/skills/task/SKILL.md`: the reviewer brief at the Phase-Gate QA step asks each reviewer for `rests_on` (the named consumer, or `none`, or `unknown`) and a one-line `why not blocking` for every Medium or Note finding (GR2); the consolidation step at line 252 keeps its present merge text in this stage but also writes `qa/follow-ups.md` through the follow-up writer (REQ-07, the run owner is the only writer); the Follow-Up Items bullet at line 361 points at that ledger; the safety route (GR12) is live; the classifier is called in shadow mode and its verdict is recorded and gates nothing; the run ends with one offer per run (spec section 6.3), replacing the output style's once-per-loop ask for this run only. The old definition still decides every gate outcome. Run `make sync-dev` afterwards.

Acceptance criteria:
- The reviewer brief in `src/superclaude/skills/task/SKILL.md` contains `rests_on` and `why not blocking`.
- The skill names `qa/follow-ups.md` as the ledger path and names the run owner as its only writer.
- `grep -n "highest severity" src/superclaude/skills/task/SKILL.md` still prints lines 252 and 361 (the merge rule is deliberately unchanged in this stage).
- `uv run pytest tests/skills/test_review_severity_rule.py tests/skills/test_review_severity_mapping.py -v` still passes (no pinned text moved).

## Task 22: Make tech-research write the ledger in shadow mode

Depends on: Task 12, Task 17, Task 20

Edit `src/superclaude/skills/tech-research/SKILL.md`: the same reviewer-brief fields, ledger path `qa/follow-ups.md` next to the consolidated findings, the safety route and the shadow classifier call as Task 21, and a final-gate sweep step at Gate 5 (the Anti-Omission gate at line 415) that calls the sweep of Task 20. Run `make sync-dev` afterwards.

Acceptance criteria:
- `src/superclaude/skills/tech-research/SKILL.md` names the sweep at Gate 5 and `qa/follow-ups.md`.
- The cap lines of the skill (lines 488-490, 517-519, 555 and 562 as listed in spec section 10.5) are unchanged.
- `uv run pytest tests/skills -k "tech_research or review_severity" -v` passes.

## Task 23: Add the three follow-up keys to the worker contract

Depends on: Task 12

Edit `src/superclaude/core/WORKER-CONTRACT.md`: WC-4 (the bullet at line 33 that enumerates the top-level keys) gains `follow_up_ledger` (path), `follow_up_counts` with `follow_up`, `note` and `show_user`, and `follow_up_capture_state` (`complete`, or `incomplete` with a reason); the status mapping maps `incomplete` capture to `worker_status: partial`; the coordinator duties (line 39, "the coordinator opens it") name the three keys as things to read; follow-ups alone never change `worker_status` from `succeeded`; the ledger is listed in `artifacts` only when it is a tracked path (WC-4 keeps gitignored paths out). Update `tests/skills/test_worker_contract.py` and add T10 cases.

Acceptance criteria:
- `src/superclaude/core/WORKER-CONTRACT.md` lists the three new keys in the line that enumerates top-level keys.
- `uv run pytest tests/skills/test_worker_contract.py -v` passes and a new test fails when a contract with `follow_up_capture_state: incomplete` is not mapped to `partial`.
- A test asserts an unattended run that records follow-ups makes no GitHub call and asks no question.

## Task 24: Pin the shadow-stage reviewer briefs

Depends on: Task 21, Task 22

Create `tests/skills/test_review_brief_rests_on.py` for T9: the reviewer brief of `src/superclaude/skills/task/SKILL.md` and of `src/superclaude/skills/tech-research/SKILL.md` must carry the `rests_on` and `why not blocking` fields. Also assert that the pinned legacy text of `src/superclaude/output-styles/pragmatic.md` lines 225 to 231 is unchanged in this stage.

Acceptance criteria:
- `uv run pytest tests/skills/test_review_brief_rests_on.py -v` passes and fails when either field is removed from either skill.
- A test fails if `src/superclaude/output-styles/pragmatic.md` line 225 changes before Task 26, so the shadow stage cannot change the rule by accident.

## Phase 4: Pilot the new rule (stage 3), only after the owner's go

## Task 25: Build the post-fix mechanical-check helper

Create `src/superclaude/cli/review/fixcheck.py` for L2: over the lines a fix pass edited it runs every mechanical check that exists (table pipe count per row, byte-present quotes, recomputed counts, link existence) and returns results for the fix log; a defect that a verifier finds that the fix introduced carries `origin: fix-induced`. Add `tests/review/test_review_fixcheck.py` with the run-2 case (an unescaped pipe in a backticked command gives 8 pipes in a 7-cell row).

Acceptance criteria:
- `uv run pytest tests/review/test_review_fixcheck.py -v` passes and the run-2 pipe case is detected.
- The helper reports a result for every check it ran, including passes, so the fix log is complete.
- It edits no file (read-only over its inputs).

## Task 26: Move pragmatic.md to digest v2

Depends on: Task 25

Edit `src/superclaude/output-styles/pragmatic.md`: replace the definition bullets (line 225 S1, line 226 S2 and line 229 S5) with the digest of REQ-01 inside its fence plus the pointer line naming `~/.claude/skills/sc-review-severity/refs/rule.md` first and `.claude/skills/sc-review-severity/refs/rule.md` second; keep the cap bullet at line 227 and the own-model bullet at line 228 word for word; move the Medium and spec-panel bullets (lines 230 and 231) into the full rule and scale map; and change the reviewer brief at line 221 so reviewers hunt for defects and name their consequence instead of hunting for "false claims" (REQ-04). Set its registry row to `v2`. Run `make sync-dev` and then the existing tests listed in Task 31 as expected to change.

Acceptance criteria:
- `src/superclaude/output-styles/pragmatic.md` holds exactly one fenced digest equal to the digest section of the skill's `refs/rule.md` and its registry row says `v2`.
- Line 227 (the cap) and line 228 are unchanged word for word.
- The hook `pragmatic-subagent.js` still finds and injects the file (`grep -n "pragmatic" hooks/hooks.json` still matches and the file exists).
- `grep -c "src/superclaude" src/superclaude/output-styles/pragmatic.md` prints 0 for the new pointer line.

## Task 27: Move rf-qa.md to digest v2 and rewrite its fixed FAIL triggers

Depends on: Task 26, Task 1

Edit `src/superclaude/agents/rf-qa.md`: replace S1, S2 and S5 (line 108 and the bullets beside it) with the digest and pointer; replace the merge rule at line 83 ("take the more severe rating for shared items") with the L1 text (the consolidator grades by the rule, keeps every reviewer's grade visible, and sends a blocking grade that names no consumer back once); add the L2 pre-handback checks to the Fix Cycle section; and for each fixed FAIL trigger listed in `./artifacts/stage0-inventory-freeze.md` for this file (spec section 10.4: line 152 "Any incomplete file = FAIL", line 162, lines 168 to 170, lines 182 to 183, line 327 "Flag exact duplicates as IMPORTANT", lines 389 and 476, and the lines 221, 316, 333, 334, 494, 548 the spec lists) either rewrite it to "grade by the three conditions; the label is information" or keep it as a named mechanical gate mapped to condition 2 (Missing) and record the keep in `refs/scale-map.md`; line 327 becomes Note unless a condition holds. Update the registry row to `v2`.

Acceptance criteria:
- `grep -n "more severe rating" src/superclaude/agents/rf-qa.md` prints nothing.
- Every FAIL-trigger line in the frozen inventory for `rf-qa.md` is either changed or listed as a kept mechanical gate in `refs/scale-map.md` with a reason.
- The PASS and FAIL bullets are reworded to "any blocking gap" and the file holds exactly one digest.
- The L2 fix-cycle checks are present in the Fix Cycle section.

## Task 28: Move rf-qa-qualitative.md to digest v2 and apply OD16

Depends on: Task 26, Task 1

Edit `src/superclaude/agents/rf-qa-qualitative.md`: replace S1, S2 and S5 (line 108 area) with the digest and pointer; replace the merge rule at line 84; and rewrite Rule 6 at line 990 ("Contradictions are always IMPORTANT or CRITICAL ... that's never minor") per OD16 option (b), so a contradiction nothing rests on is a follow-up, and keep contradictions that touch a decision basis, a quoted number or a required deliverable as Blocking under condition 1. Update the registry row to `v2`.

Acceptance criteria:
- `grep -n "that's never minor" src/superclaude/agents/rf-qa-qualitative.md` prints nothing, and the new Rule 6 text names the decision-basis exception.
- The file holds exactly one digest and no `more severe rating` text.
- `tests/audit/test_severity_floor_unweakened.py` is updated in Task 32 in the same change set; the file's `## Critical Rules` block hash is re-pinned there.

## Task 29: Replace the merge rule in rf-analyst.md

Depends on: Task 26

Edit `src/superclaude/agents/rf-analyst.md` line 75 ("union of findings, take the more severe rating for shared items, merge gap compila...") to the L1 text: union the findings, keep each reviewer's own grade visible, and let the consolidator grade by the rule; keep the rest of the line (the gap compilation) unchanged.

Acceptance criteria:
- `grep -n "more severe rating" src/superclaude/agents/rf-analyst.md` prints nothing.
- The gap-compilation words that followed on the line are still present.

## Task 30: Switch the task skill's consolidation, fix and escalation text

Depends on: Task 26, Task 25

Edit `src/superclaude/skills/task/SKILL.md`: line 252 (Findings Consolidation) and line 361 replace "Preserve the highest severity rating when duplicates disagree" with the L1 text and keep the ledger writing of Task 21; line 254 (Fix Agent) requires the L2 mechanical checks before handing back and the `origin: fix-induced` tag; line 258 (Conditional Proceed) counts Blocking findings only and, at the cap, offers three choices (fix by hand, accept and file as an `accepted-blocker` follow-up, or stop) without changing the cap of 2 fix cycles (L3). Update the registry row for the task skill to `v2`.

Acceptance criteria:
- `grep -n "highest severity" src/superclaude/skills/task/SKILL.md` prints nothing.
- The cap text `at most 2 fix cycles (3 reviews), then escalate to the user with the open blocking findings` is still present word for word (`CANONICAL_CAP_TEXT` pins it).
- The escalation text lists the three choices and says the cap is unchanged.

## Task 31: Re-pin the severity tests in tests/skills

Depends on: Task 26, Task 27, Task 28, Task 30

Update `tests/skills/test_review_severity_rule.py` (`canonical_rule_bullets()` at lines 78-96 reads the digest from `refs/rule.md`; `S1_S3_FILES` and its `[:6]` slice `S5_FILES` become registry rows; `CANONICAL_CAP_TEXT` at line 215 and the banned-phrase checks stay), `tests/skills/test_review_severity_mapping.py` (the Medium and cadence pins move from "once per loop" to the once-per-run wording and to assertions on `refs/rule.md` and `refs/scale-map.md`), `tests/skills/test_implement_severity_static.py` (S4 kept word for word; the S2 assertion moves to the digest; the `qa.md` pins stay), and the two fixtures `tests/skills/fixtures/review_severity_cap_edits.yaml` and `review_severity_sweep_edits.yaml` (update only the approved changed strings). `tests/skills/test_review_loop_extension.py`, `test_review_prompt_overrides.py` and `test_spec_panel_review_loop.py` must still pass unchanged.

Acceptance criteria:
- `uv run pytest tests/skills/test_review_severity_rule.py tests/skills/test_review_severity_mapping.py tests/skills/test_implement_severity_static.py tests/skills/test_review_loop_extension.py tests/skills/test_review_prompt_overrides.py tests/skills/test_spec_panel_review_loop.py -v` passes.
- The two fixtures change only rows whose new text is the digest or the once-per-run cadence; the diff of each fixture is listed in `./artifacts/t31-fixture-diff.md`.
- No pinning test is deleted wholesale; each changed pin is replaced by a pin on the new text.

## Task 32: Re-pin the audit tests for the QA agents

Depends on: Task 27, Task 28

Update `tests/audit/test_nfr_conv_9_zero_trust.py` (byte-exact PASS and FAIL bullets of `src/superclaude/agents/rf-qa.md` and its `.claude/` mirror) to the reworded "any blocking gap" bullets on both surfaces; update `tests/audit/test_invariant_preservation_NFR_6_through_10.py` (it imports `FAIL_BULLET` and `PASS_BULLET` from the first module at lines 95-101) in the same change; re-pin `tests/audit/test_severity_floor_unweakened.py` (the SHA-256 of the `## Critical Rules` block of `rf-qa-qualitative.md` and its mirror, and Rule 6 verbatim) to the Task 28 text; leave `tests/audit/test_dnsp_all_agents_fail_bypass.py` unchanged unless the cap text moved.

Acceptance criteria:
- `uv run pytest tests/audit -v` passes.
- The re-pinned hash in `test_severity_floor_unweakened.py` matches the new `## Critical Rules` block on both the source and the mirror surface after `make sync-dev`.
- `test_dnsp_all_agents_fail_bypass.py` passes without an edit.

## Task 33: Add the merge-rule reverse-scan test

Depends on: Task 27, Task 28, Task 29, Task 30

Create `tests/skills/test_review_merge_rule_scan.py` for T5: a scan of tracked `src/` and `plugins/` that fails when `highest severity`, `more severe rating` or `higher severity` appears outside an allow-list; the allow-list is the scale-map rows (`src/superclaude/skills/sc-auggie-review-protocol/SKILL.md:228` and the stage 4 files listed in spec section 10.3, which stay allowed until Phase 5).

Acceptance criteria:
- `uv run pytest tests/skills/test_review_merge_rule_scan.py -v` passes after Tasks 27 to 30.
- A temporary-tree test with `highest severity` in a non-allow-listed file fails the scan.
- The allow-list names the six stage 4 files (`tech-reference`, `readme`, `tdd` build-request template, `operational-guide`, `agent_template_qa.md`, `agent_template_analysis.md`) so Task 36 and Task 34 remove them from it.

## Phase 5: Propagate to the remaining carriers (stage 4), only after the owner's go

## Task 34: Move the templates to digest v2

Edit the digest carriers in `src/superclaude/templates/`: `documents/agent_template_qa.md` (line 161 definition, line 85 merge rule, line 333 Rule 6 text per OD16), `documents/agent_template_analysis.md` (line 466 merge rule), `documents/skill_template.md` (line 828 definition), `workflow/01_mdtm_template_generic_task.md` (line 644) and `workflow/02_mdtm_template_complex_task.md` (line 655). Each gets the digest and pointer in place of the definition bullets and the L1 merge text; update their registry rows to `v2`. Task files already generated from the old templates keep the old text and are not migrated.

Acceptance criteria:
- Each of the five template files holds exactly one digest and no `more severe rating` text.
- Their registry rows say `v2` and T1 passes for them.
- `grep -rn "Grade every review finding as blocking or minor" src/superclaude/templates` prints nothing.

## Task 35: Move the rule prompts to digest v2

Depends on: Task 34

Edit the digest carriers in `src/superclaude/rules/prompts/`: `automated_qa_workflow_qa_prompt.md` (line 11), `doc_code_analyst_qa_prompt.md` (line 27), `documentation_expert_qa_prompt.md` (line 28), `recruiting_expert_qa_prompt.md` (line 27), and `document_review_loop_prompts.md` (the Medium wording at lines 31, 32 and 48 becomes the pointer and the ledger sentence inside an existing section; its structure and the `"src/superclaude" not in TEXT` assertion of `tests/review/test_review_rules_text.py` line 92 must still hold). Update registry rows to `v2`.

Acceptance criteria:
- Each of the five prompt files holds exactly one digest or, for `document_review_loop_prompts.md`, the pointer plus the ledger sentence.
- `uv run pytest tests/review/test_review_rules_text.py tests/skills/test_review_prompt_overrides.py -v` passes and the zero-finding and "no minimum count" sentences still exist.

## Task 36: Replace the merge rule in the builder and researcher skills

Depends on: Task 33

Edit the stage 4 merge-rule lines of spec section 10.3: `src/superclaude/skills/tech-reference/SKILL.md` lines 510 and 513, `src/superclaude/skills/readme/SKILL.md` lines 542 and 547, `src/superclaude/skills/tdd/refs/build-request-template.md` line 122 and `src/superclaude/skills/operational-guide/SKILL.md` line 511, each to the L1 text; and remove those files from the allow-list of the Task 33 test.

Acceptance criteria:
- `grep -rn "highest severity\|more severe rating\|higher severity" src/superclaude/skills/tech-reference src/superclaude/skills/readme src/superclaude/skills/tdd src/superclaude/skills/operational-guide` prints nothing.
- `tests/skills/test_review_merge_rule_scan.py` passes with the four skills removed from its allow-list.
- The cap text in each of the four files is unchanged.

## Task 37: Add the consumer line to the task builder and MDTM templates

Depends on: Task 34

Edit `src/superclaude/skills/task-builder/SKILL.md` and the MDTM templates `src/superclaude/templates/workflow/01_mdtm_template_generic_task.md` and `02_mdtm_template_complex_task.md` so the task builder writes a consumer line for each phase output ("feeds item X, reads column Y"), which gives upstream gates a declared consumer list (L4, spec section 4.3 option A for upstream outputs only). Keep the cap text in `src/superclaude/skills/task-builder/SKILL.md` line 875 and in `src/superclaude/agents/rf-task-builder.md` (lines 383-389, 415-421) unchanged.

Acceptance criteria:
- Both MDTM templates and the task-builder skill contain the consumer-line instruction.
- `uv run pytest tests/skills/test_task_builder_merge.py -v` passes.
- The cap text lines named above are unchanged.

## Task 38: Narrow spec-panel and update the plugin twins

Depends on: Task 35

Edit `src/superclaude/commands/spec-panel.md`: the Review Loop bullets at lines 259 to 261 and the always-CRITICAL dimensional-mismatch sentence at line 372 are narrowed to the three conditions (CRITICAL stays blocking, a MAJOR stays blocking only when it names a concrete wrong outcome), its `follow-up candidates` list becomes the follow-up ledger, and the Unattended mode section (starting at line 455) gains one line for the ledger and the three contract keys. Apply the same edits to the hand-kept twins `plugins/superclaude/commands/spec-panel.md` and `plugins/superclaude/rules/prompts/document_review_loop_prompts.md`; the `spec-panel` source and plugin copies differ today, so edit each file in place and do not copy one over the other.

Acceptance criteria:
- `uv run pytest tests/skills/test_spec_panel_review_loop.py tests/skills/test_review_loop_extension.py -v` passes and the cap text `at most 2 fix cycles (3 reviews)` is still in `src/superclaude/commands/spec-panel.md`.
- `grep -n "follow-up candidates" src/superclaude/commands/spec-panel.md` prints nothing and the ledger is named instead.
- The plugin twins carry the same digest and pointer as their source twins, and a parity assertion for the two files is part of `tests/skills/test_review_severity_registry.py`.

## Task 39: Mirror the skill folder into the plugin and make the drift scan strict

Depends on: Task 34, Task 35, Task 36, Task 37, Task 38

Copy `src/superclaude/skills/sc-review-severity/` to `plugins/superclaude/skills/sc-review-severity/` by hand (the plugin's `skills/` is hand-kept and holds 4 entries today), add `tests/skills/test_review_severity_plugin_parity.py` for T15 (the mirror equals the source), set every registry row to `v2` where its file now holds the digest, and switch T2 of `tests/skills/test_review_severity_registry.py` to strict mode so any legacy definition sentence left in `src/` or `plugins/` fails. Run `make sync-dev` and `make verify-sync`.

Acceptance criteria:
- `uv run pytest tests/skills/test_review_severity_plugin_parity.py tests/skills/test_review_severity_registry.py -v` passes with strict T2.
- `make verify-sync` passes.
- `grep -rn "Grade every review finding as blocking or minor" src/superclaude plugins/superclaude` prints nothing; the two installed-only spec-panel variants are outside the scan and stay listed `installed-only`.
- No file under the project `.claude/` folder other than `.claude/settings.json` appears in `git diff --cached --name-only`.
