---
schema: workflow-plan/1.2
source: ./source.md
strategy: systematic
depth: standard
slug: TASK-WF-blockerStage1-20261116-030154
version: "1"
priority: Medium
created_date: "2026-11-16"
---

# Stage 1 plan: offline scaffold for the blocker classification work (issue #552)

Source: ./source.md
Goal: Create the new skill folder, its references, the registry, the ledger and classifier modules, the classify command, the safety route, the install check and their tests, all offline; no review-loop carrier is edited and every registry `digest` row stays `legacy`. The owner reads `./artifacts/stage1-summary-for-owner.md` and decides whether to say go for stage 2.

## Constraints

- Spec: the merged spec `02-brainstorm/merged-requirements.md` inside the program folder `BLOCKER-CLASSIFICATION-PROGRAM-20261115` (found by that folder name under the repository's task folder). This plan calls that folder PF and the spec file the spec. Section numbers, requirement ids (REQ-nn), loop changes (L1 to L6), guardrails (GR1 to GR12), tests (T1 to T17) and owner decisions (OD1 to OD17) refer to the spec. PF also holds the 5-run results in `08-test/results.md`, the reconciliation in `09-plan-input.md` and the stage ledger and the five stage requests in `stage-requests/`. Evidence of earlier stages is read from their packages by package id (the ids are in the stage ledger), found by that folder name in the to-do or done subfolder of the repository task folder.
- One package, one stage. This is stage 1 of five packages (one plan per stage, the owner's decision of 2026-11-16). It creates new files only (the skill folder, new CLI modules, new tests, one doctor check) and edits no review-loop carrier (`pragmatic.md`, agents, templates, rule prompts, the task skill, tech-research, `WORKER-CONTRACT.md`); every registry `digest` row stays `legacy`. It runs only after the stage 0 package is done, the owner has read the stage 0 summary and said go in chat, and the go is recorded in the stage ledger (Task 1 checks that). Stage 2 starts only after the owner reads this package's summary and says go.
- Owner decisions use the spec's recommendations unless the owner changes them: OD1 skill folder `sc-review-severity`; OD2 once per run plus at any escalation halt; OD4 the classifier has no authority in version 1; OD9 reviewer-named consumer, code-checked where quotable; OD11 replace label-max merging at all 13 lines in 10 files, staged; OD12 yes; OD13 short Note rows; OD14 a finding with an unknown consumer keeps the reviewer's label (no deferral); OD15 consent-bound body file posted by the attended top-level session; OD16 option (b) at stage 3. OD3 (finding text leaving the machine), OD5 to OD8 and OD10 are not decided here and no task depends on a different answer.
- Not built here: any Jev or other external judge call, any TypeSafe account or key, a Jev or LLM judge class (they wait for OD3), any change to `src/superclaude/skills/sc-implement-protocol/refs/qa.md` (it keeps its own scale), any change to the own-scale primitives listed in spec section 9.3 as unchanged, code-assigned severity in `src/superclaude/cli/**/*.py` (for example `fmea_classifier.py` and `remediate_parser.py`, out of scope by spec section 10.3), the 35 percent score target, and any change to the cap of 2 fix cycles.
- Classifier facts that bind every classifier task: the 5-run test (stage 0 package, `stage0a-result.md`, from PF `08-test/results.md`) used a text-only stand-in judge and got agreement with the panel of 58.5 percent (Cohen's kappa 0.27), and the missing-item, constraint and contradiction questions (M, C, E) were at chance without code-supplied inputs. So M, C and E run only when code supplies the required-item list, the constraint lines and the verified evidence (the classifier-inputs supplier of stage 1), the "M or C is Y gives BLOCKING" row is never enabled for any gate, and confidence is reported as an ordinal band, never as a probability.
- Pins are by content. An acceptance check that must survive a task's own edit quotes the sentence it protects; it does not name a line number, because the edit moves the line. Line numbers in a task body are where the text sits today and are re-read before editing. An acceptance line that a later task of this package makes false carries its end point ("until Task N").
- `src/superclaude/` is the source of truth. Edit there, then run `make sync-dev`; never stage anything under the project `.claude/` folder (only `.claude/settings.json` is tracked). Installed primitives name installed paths (`~/.claude/skills/...`) first and project `.claude/...` second, never a `src/superclaude/` path.
- Python work uses UV only: `uv run pytest ...`, never `python -m` or bare `pip`.
- Task-owned evidence and generated outputs go under `./artifacts/` in this package. `.dev/tasks/` is always staged (`git add .dev/tasks`), packages and their `./artifacts/` included, and no document a task writes says it is never staged. Staging is not committing.

## Phase 1: Create the skill folder and its references

## Task 1: Create the skill folder entry file

Create `src/superclaude/skills/sc-review-severity/SKILL.md` (the folder does not exist today, confirmed). It states the purpose, which ref is read by whom (the table of spec section 9.1), the rule version `v2`, and "Delegate-only, no slash command", in the style of the existing `sc-bare-review` skill. Do not name any `src/superclaude/` path inside it.

Acceptance criteria:
- The stage ledger `stage-requests/README.md` in PF has an owner go for stage 1 with a date (the go is a chat message recorded there by the session that received it); when the row has none, this check fails and the run halts for the owner's Ruling.
- The stage 0 package's `./artifacts/stage0-summary-for-owner.md` (read by package id) exists.
- `src/superclaude/skills/sc-review-severity/SKILL.md` exists with frontmatter, the five refs named in spec section 9.1 (`refs/rule.md`, `refs/scale-map.md`, `refs/follow-up-ledger.md`, `refs/classifier-questions.md`, `refs/registry.yaml`) and the line "Delegate-only, no slash command".
- `grep -n "src/superclaude" src/superclaude/skills/sc-review-severity/SKILL.md` prints nothing.
- After `make sync-dev`, `make verify-sync` reports the new folder in sync.

## Task 2: Write the full rule with the pinned digest

Depends on: Task 1

Create `src/superclaude/skills/sc-review-severity/refs/rule.md`. It holds the full rule: the three blocking conditions, the Medium and Note classes, the counterfactual test and the table of spec section 4.2, the decision basis of section 4.3, the worked cases of section 5, the table-shape rule, the guardrails GR1 to GR12 of section 8.1 (GR5 names "highest severity wins" as the thing it does not re-create, so the file contains that phrase and the merge-rule scan allow-lists it), and the digest. The digest is the block of REQ-01 word for word, including REQ-02 (the unknown-consumer sentence), REQ-03 (the precedence sentence) and the cap sentence that today's `src/superclaude/output-styles/pragmatic.md` holds in its cap bullet ("A review loop (review, fix, re-review) runs at most 2 fix cycles (3 reviews), then escalate to the user with the open blocking findings; never run a fourth review and never pass open blocking findings."), placed between the HTML-comment fence lines `review-severity:digest v2 begin` and `review-severity:digest v2 end`.

Acceptance criteria:
- `grep -rn "Grade every review finding as blocking or minor" src/superclaude/skills/sc-review-severity` prints nothing outside the one fenced digest's own text (the digest does not quote the old sentence either).
- `refs/rule.md` contains exactly one fenced digest whose last sentence equals the cap sentence of `src/superclaude/output-styles/pragmatic.md` word for word.
- The digest contains the sentences of REQ-02 and REQ-03.
- Every one of the 14 worked cases of spec section 5 appears with its verdict.
- `grep -n "src/superclaude" refs/rule.md` prints nothing.

## Task 3: Write the scale map

Depends on: Task 1

Create `src/superclaude/skills/sc-review-severity/refs/scale-map.md` with one row per family of spec section 9.3: family, defining file, each native label, the shared outcome per label (Blocking, Medium, Note), and either "graded by the three conditions" or "keeps its own model because <reason>". The rows are the 12 families of that table: the CRITICAL, IMPORTANT, MINOR lens scale; the `/sc:implement` `refs/qa.md` checklist; spec-panel; the stoprule rubric and `finding-grader`; the reflect deviation taxonomy; tasklist High, Medium, Low; roadmap validate; `card_convert.py`; findings-v1 and v2; `sc-auggie-review-protocol/SKILL.md:228`; the PR severity router and Auggie rubric; and the code-assigned family. Include the sentence that a keep of a fixed FAIL trigger (L6) is recorded here, and a section "Merge-rule allow-list" that lists by path only the files allowed to contain the three merge-rule phrases of spec section 10.3 (the auggie file, `refs/rule.md`, and the six stage 4 files until the stage 4 package; this file never writes those phrases or the old definition sentence) so the stage 3 scan test reads its allow-list from one place. The plugin mirror is added to the list by the stage 4 package, not here.

Acceptance criteria:
- `refs/scale-map.md` has a row for each of the 12 families, each naming a defining file that exists in the repository.
- The tasklist row states that Medium is blocking today on 7 lines of `src/superclaude/skills/sc-tasklist-protocol/SKILL.md` and that no stage 1 to 4 task changes it.
- The `card_convert.py` row states that its word translator maps `important` and `medium` to non-blocking while `src/superclaude/agents/rf-qa.md` treats IMPORTANT as blocking.
- The "Merge-rule allow-list" section exists and lists the auggie file, `refs/rule.md` and the six stage 4 files (until the stage 4 package).
- `grep -n -i "highest severity\|more severe rating\|higher severity" src/superclaude/skills/sc-review-severity/refs/scale-map.md` prints nothing.

## Task 4: Write the follow-up ledger reference

Depends on: Task 1

Create `src/superclaude/skills/sc-review-severity/refs/follow-up-ledger.md` from spec sections 6.1 to 6.7: the flow, the ledger contract (metadata block, Items table with its columns, Notes table, Observations, Offers and Filings tables, item states, identity rules), the offer wording with consent binding (REQ-11), unattended behaviour (REQ-12), the filing path (OD15, REQ-13 to REQ-15), the location rule (REQ-07) and "resolve now" (6.7). Keep the cell codec of REQ-10 exactly: entity layer, no backslash before a pipe. State that the final-gate sweep records rows as `sweep-flagged` in stage 2 and promotes them only from the stage 3 package's task that edits the task skill's consolidation text, and that the end-of-run offer is made once, by the task skill, so a run never shows two offers.

Acceptance criteria:
- `refs/follow-up-ledger.md` contains the Items table columns of spec section 6.2 (`id`, `origin`, `tier`, `source`, `location`, `finding`, `evidence`, `rests_on`, `why_not_blocking`, `tags`, `proposed_fix`, `suggested_type`, `classifier`, `status`, `canonical_id`, `issue_url`).
- The offer wording of spec section 6.3 and the sentence "Nothing is filed until you answer." appear.
- The file states the three tags `consumer-unknown`, `unsettled` and `protected-risk-dispute` and that all three feed the single `show_user` count.
- The file states the `sweep-flagged` rule and that the task skill is the one owner of the offer.

## Task 5: Write the classifier question reference

Depends on: Task 1

Create `src/superclaude/skills/sc-review-severity/refs/classifier-questions.md`: the six decisive questions S, W, E, M, C, D of spec section 7.2 with the S wording "in a way the task did not ask for", the code-supplied input each needs, the Option Q replacement for D at upstream gates, and the optional explanation questions T, F, I and G (they feed no cell of the truth table). Add a version line `question-set v1`. State that M, C and E are asked only when code supplies their inputs, and say why in words (they were at chance in the five-run text-only test); this file cites no `.dev/` or `./artifacts/` path.

Acceptance criteria:
- `grep -rn "\.dev/\|artifacts/" src/superclaude/skills/sc-review-severity` prints nothing: no file of the skill folder cites a `.dev/` or `./artifacts/` path.
- `refs/classifier-questions.md` has the six questions with a "Needs from code" column and the line `question-set v1`.
- No question text contains the word "blocking" (`grep -in blocking` over the question table rows prints nothing).
- The file states that a failed or skipped answer is UNSET and never N.

## Task 6: Write the carrier registry with every digest row set to legacy

Depends on: Task 2, Task 3

Create `src/superclaude/skills/sc-review-severity/refs/registry.yaml`. Each row has the logical path relative to the install root, a `kind` (`digest`, `canonical`, `pointer-only` or `installed-only`), surfaces (source, installed, project `.claude/`, plugin, or `installed-only`), rollout stage, a state (`legacy` for a digest row until its file is moved), and an own-scale flag. Rows of kind `digest`, exactly the 11 definition carriers of spec section 10.1: `output-styles/pragmatic.md`, `agents/rf-qa.md`, `agents/rf-qa-qualitative.md`, `templates/documents/agent_template_qa.md`, `templates/documents/skill_template.md`, `templates/workflow/01_mdtm_template_generic_task.md`, `templates/workflow/02_mdtm_template_complex_task.md`, `rules/prompts/automated_qa_workflow_qa_prompt.md`, `rules/prompts/doc_code_analyst_qa_prompt.md`, `rules/prompts/documentation_expert_qa_prompt.md`, `rules/prompts/recruiting_expert_qa_prompt.md`. One row of kind `canonical`: `skills/sc-review-severity/refs/rule.md` (the one source digest; the stage 4 package adds its plugin mirror). Two rows of kind `pointer-only` (a pointer plus the ledger sentence, no digest): `rules/prompts/document_review_loop_prompts.md` and `commands/sc/spec-panel.md` (source `commands/spec-panel.md`). Five rows of kind `installed-only`: `commands/sc/spec-panel-armb.md`, `spec-panel-diffgate.md`, `spec-panel-ledger.md`, `spec-panel-ponytail.md` and `spec-panel-stoprule.md`. `skills/task/SKILL.md` gets no row: it is not a digest carrier. `templates/documents/agent_template_analysis.md` gets no row either: it holds no definition sentence, only a merge-rule line, which the stage 4 package edits as text only.

Acceptance criteria:
- `refs/registry.yaml` parses with `uv run python -c "import yaml,sys; yaml.safe_load(open(sys.argv[1]))" src/superclaude/skills/sc-review-severity/refs/registry.yaml`.
- It has exactly 11 rows of kind `digest` (each with a source path that exists, state `legacy`, stage 3 for `pragmatic.md`, `rf-qa.md` and `rf-qa-qualitative.md`, stage 4 for the rest), 1 of kind `canonical`, 2 of kind `pointer-only` and 5 of kind `installed-only`, 19 rows in all.
- No row names `skills/task/SKILL.md`.


## Phase 2: Build the ledger codec and the filing logic

## Task 7: Build the follow-up ledger codec, reader and writer

Depends on: Task 4

First run the `reuse-auditor` agent on the proposed module against `src/superclaude/cli/review/ledger.py` (schema `review-ledger/1`) and record its verdict in `./artifacts/reuse-audit-follow-ups.md`; share code only where it says reuse-by-import. Then create `src/superclaude/cli/review/follow_ups.py`: one reader and one writer for `follow-ups.md` only (REQ-07 location rule, REQ-08 sole writer with an expected-revision check and atomic replace, REQ-10 entity codec with evidence blocks and a fence longer than any backtick run, identity tuple and observation import that is idempotent, the sort order of spec section 6.2, and the item states including `sweep-flagged`). A malformed ledger is preserved and reported, never reset. Create `tests/review/test_review_follow_ups.py` for T7: required columns, a Medium row without `why_not_blocking` is refused, identity never merges on a digest alone, codec round trip for pipes, backticks, a triple-backtick line, literal entities, Unicode and multiline text, a stale writer cannot overwrite a newer revision, a malformed ledger is preserved.

Acceptance criteria:
- `uv run pytest tests/review/test_review_follow_ups.py -v` passes and covers each T7 failure condition above.
- `./artifacts/reuse-audit-follow-ups.md` exists and the module imports from `ledger.py` only where the audit says to.
- Two readers of this ledger do not exist: `grep -rn "follow_ups" src/superclaude/cli/review` shows only the new module and its command wiring.
- `make lint` reports no new findings for the module.

## Task 8: Build the filing state machine

Depends on: Task 7

Add to `src/superclaude/cli/review/follow_ups.py` the Filings table logic of spec section 6.5: batch id as a stable digest of repository, run id, selected canonical ids and purpose; states `prepared`, `posting`, `reconcile`, `filed`, `cancelled`; a body digest compared with the read-back body; a reconcile step that searches for the exact batch marker before any retry; the 60,000-character bound with overflow posted as comments (REQ-15); and the repository guard of REQ-14 (the target comes from the `origin_repo.py` script of `src/superclaude/skills/sc-issue-protocol/scripts/origin_repo.py`; when the target is the IronClaude repository it must be `IronbellyOrg/IronClaude`, never the upstream parent, and any other resolution means stop and record only). The code takes the `gh` call as an injected function so tests never touch GitHub. Create `tests/review/test_review_follow_ups_filing.py` for T8: a resume asks again, a changed set is filed without new consent, a timeout after a successful post creates a second issue, a body whose digest differs is marked `filed`, a repository other than the verified one is targeted.

Acceptance criteria:
- `uv run pytest tests/review/test_review_follow_ups_filing.py -v` passes with a fake `gh` and covers each T8 failure condition.
- No test or module calls the real `gh` or the network.
- Every `gh` argument list built by the module spells `--repo <R>` or `repos/<R>/...` with `<R>` from the resolver and never a `{owner}/{repo}` placeholder.


## Phase 3: Build the classifier, its inputs, the command and the safety route

## Task 9: Build the classifier module

Depends on: Task 5

Create `src/superclaude/cli/review/classifier.py` and `src/superclaude/cli/review/data/classifier_thresholds.json`. The module holds the truth table of spec section 7.3 (version 2, ported from `07-classifier/truth_table.py` in PF and the sketch `02-brainstorm/blocker_truth_table_sketch.py`: states Y, N, U, UNSET, NA; NA reachable only from a deliverable-kind declaration, REQ-19; precedence, the W and E combination of REQ-17, the lift rule of REQ-18), the bands (S: Y at 0.30 or more, N at 0.10 or less; others 0.70 and 0.30), ordinal confidence bands with the replicate rule of spec section 7.4 (median of 3, spread above 0.20 counts as U), the `dependence-safe lower bound max(0, pW + pD - 1)` reported beside the band, and a `Judge` interface with two implementations: `FixtureJudge` (recorded answers) and `ReviewerJudge` (the reviewer's own label read through the scale map as 0 or 1). A judge failure is a typed `UNDETERMINED` result that moves to the next judge, never a table cell and never an N. Thresholds live only in the JSON file.

Acceptance criteria:
- `uv run python -c "from superclaude.cli.review.classifier import verdict"` succeeds and `verdict` agrees with the sketch on all 6,400 combinations of the REQ-21 property tests.
- No Jev, LLM or network class exists in the module (`grep -n "typesafe\|requests\|httpx\|anthropic" src/superclaude/cli/review/classifier.py` prints nothing).
- A judge answer of `None` yields UNSET, and the function that sets NA takes a deliverable-kind argument and no probability.
- `src/superclaude/cli/review/data/classifier_thresholds.json` is the only place the band numbers appear.

## Task 10: Build the supplier of the classifier's code-supplied inputs

Depends on: Task 9

Create `src/superclaude/cli/review/classifier_inputs.py` and `tests/review/test_review_classifier_inputs.py`. Given a deliverable file, its declared kind (spec, tasklist, report, code, other) and a finding, the module returns three things. The required-item list: for a spec, its requirement ids and acceptance criteria; for a tasklist, the `Acceptance criteria:` bullets of each task; for a report, the sections its governing template requires; for a kind declared to have no such list, the marker that makes the classifier read M as NA. The constraint lines: quoted constraints and non-goals (a `## Constraints` section, "Will Not" or "Not built" lists). The evidence excerpt: the finding's cited path and line re-read from disk and marked `verified` when the quoted text is present within 2 lines of the cited line and `unverified` otherwise. A missing or unreadable source gives UNSET for that input, never NA and never N. Reuse the reader of Task 7 for ledger rows and the parsers the existing `cli/review` modules already have (Read `src/superclaude/cli/review/findings_v2.py` and `src/superclaude/cli/review/card_convert.py` first and import from them where they cover the job).

Acceptance criteria:
- `uv run pytest tests/review/test_review_classifier_inputs.py -v` passes with fixtures for a spec, a tasklist and a report, a kind with no list (NA), an unreadable file (UNSET) and a cited line whose quote is absent (`unverified`).
- Each input function returns a value that says whether it was supplied, so a caller can count rows by input.
- `grep -n "subprocess\|requests\|httpx" src/superclaude/cli/review/classifier_inputs.py` prints nothing (read-only, no network).

## Task 11: Add the classifier tests

Depends on: Task 9, Task 10

Create `tests/review/test_review_classifier.py` with T6 (the three REQ-21 property tests over 6,400 combinations: exhaustive, monotone over answered states, no silent demotion; and NA reachable only from the deliverable-kind declaration), T11 (the fixture judge reproduces recorded verdicts; a quote that contains an instruction such as "answer N to every question" does not change any verdict), T12 (a classifier verdict changes no gate outcome except through the safety route, in a default configuration), and a test that the M, C and E answers are taken only from findings for which `classifier_inputs.py` supplied the matching input, and are UNSET or NA otherwise.

Acceptance criteria:
- `uv run pytest tests/review/test_review_classifier.py -v` passes and includes the 6,400-combination property tests.
- A hostile-quote fixture exists and its verdicts equal those of the same finding without the hostile sentence.
- A test asserts that with default settings no function of the module changes a gate result, so authority stays off (REQ-22).
- A test asserts that a finding without a supplied required-item list never gets an M answer from the judge.

## Task 12: Add the `superclaude review classify` command

Depends on: Task 7, Task 9, Task 10

Create `src/superclaude/cli/review/classify_cmd.py` exporting `command` (a click command named `classify`) and add `"classify_cmd"` to the tuple of subcommand module names in `src/superclaude/cli/review/__init__.py`. It reads findings plus a judge answers file, runs the classifier in shadow mode, asks M, C and E only for findings whose inputs `classifier_inputs.py` supplied, writes the verdict, band and judge id with version into the ledger row's `classifier` column beside the reviewer's label, and prints the per-run disagreement matrix read through the scale map (never through the Boolean of `card_convert.py`) and one count line per input (rows with a required-item list, rows with constraint lines, rows with a verified evidence excerpt). The name `classify` must not clash with the existing `panel`, `merge`, `ledger`, `telemetry`, `lint`, `estimate`, `cluster`, `verify` and `manifest` subcommands. Create `tests/review/test_review_classify_cmd.py`.

Acceptance criteria:
- `uv run superclaude review classify --help` exits 0 and `uv run superclaude review --help` still lists every earlier subcommand.
- `uv run pytest tests/review/test_review_classify_cmd.py tests/review/test_review_cli.py -v` passes.
- A run with no judge available records `classifier=unavailable` and leaves the reviewer's label standing; it never invents a verdict.
- The printed output includes the three input-count lines, and a test asserts them for a fixture with one supplied and one unsupplied input.

## Task 13: Build the safety route

Depends on: Task 7

Create `src/superclaude/cli/review/safety_route.py` with the GR1 vocabulary scan (one list of destructive and secret words: delete, overwrite, force, token, secret, password, chmod and similar, kept in one place) and the GR12 rule: a hit on a non-blocking row, or a judge answer S = Y or S = U on a row a reviewer graded non-blocking, tags the row `protected-risk-dispute` and never writes it as a plain follow-up. It can only raise a grade. Add `tests/review/test_review_safety_route.py` for T17.

Acceptance criteria:
- `uv run pytest tests/review/test_review_safety_route.py -v` passes and covers a vocabulary hit, S = Y and S = U on a minor row.
- No function in the module lowers a grade (a test asserts the outcome order never decreases).
- Attended output text names the person prompt; unattended output sets the signal that makes the run `partial`, per spec section 6.4.


## Phase 4: Add the install check, the drift tests and the exit summary

## Task 14: Add the install check for digest versions

Depends on: Task 6

Add `_check_review_severity_digests` to `src/superclaude/cli/doctor.py` and call it from `run_doctor` (REQ-27). It compares the digest versions held by the installed carriers with the packaged registry of `src/superclaude/skills/sc-review-severity/refs/registry.yaml`, reading the packaged registry and not an installed copy (an installed skill folder is skipped once present, so an installed `registry.yaml` can be stale), and considers only rows of kind `digest`. Add tests to `tests/unit/test_cli_doctor.py`; keep `tests/cli/test_install_retired_mcp.py` (`test_update_and_doctor_never_mutate_and_never_change_their_exit_code`) passing because `run_doctor` must stay read-only.

Acceptance criteria:
- A test in `tests/unit/test_cli_doctor.py` builds an installed tree with a stale digest version and asserts the check reports the mismatch (T13).
- `uv run pytest tests/unit/test_cli_doctor.py tests/cli/test_install_retired_mcp.py tests/cli/test_update_command.py -v` passes.
- With every registry row at `legacy` and every installed carrier legacy, the check reports no mismatch.
- `make doctor` still runs and exits as before.

## Task 15: Add the registry drift tests

Depends on: Task 2, Task 6

Create `tests/skills/test_review_severity_registry.py` for T1 (every row of kind `digest` holds, in its file, exactly one digest whose flattened body equals the digest section of `refs/rule.md` for that row's version; a row at `legacy` is accepted; the `canonical` row holds the source digest), T2 (a reverse scan of the tracked `src/` and `plugins/` trees fails on any file that holds the old definition sentence or a fence opener and has no registry row of any kind; `canonical` and `pointer-only` rows count as registered; strict mode is a switch, off in this phase), T3 (each pointer names `~/.claude/skills/sc-review-severity/...` before `.claude/skills/sc-review-severity/...`, ; the check that no carrier contains `src/superclaude` applies to `digest` and `canonical` rows only; `pointer-only` and `installed-only` rows are checked for pointer order only, a `pointer-only` row only once its pointer is present, and the test never reads `~/.claude`), T4 (each scale-map row names an existing file and a label present in it) and T14 (a `digest` row at `v2` holds the precedence sentence).

Acceptance criteria:
- A temporary-tree test shows each T3 exemption: a `pointer-only` row whose file holds a `src/superclaude` path passes the path check, a `pointer-only` row without its pointer yet passes, and a `digest` row whose file holds such a path fails.
- `uv run pytest tests/skills/test_review_severity_registry.py -v` passes with all `digest` rows at `legacy`.
- A test flips one `digest` row to `v2` without editing its file and fails, which shows T1 can fail; a `pointer-only` row at any state does not fail T1.
- The reverse scan accepts `refs/rule.md` (it has a `canonical` row) and reports a file that holds the definition sentence and is absent from the registry, using a temporary tree in the test.

## Task 16: Write the stage 1 exit summary for the owner

Depends on: Task 1, Task 2, Task 3, Task 4, Task 5, Task 6, Task 7, Task 8, Task 9, Task 10, Task 11, Task 12, Task 13, Task 14, Task 15

Write `./artifacts/stage1-summary-for-owner.md`, the one file the owner reads before saying go for stage 2. For each of Tasks 1 to 15 give the files it created or changed and the command it ran with its observed pass count (for tests, the pytest summary line). List every file the package created. Show that no carrier was edited: `git diff --stat HEAD -- src/superclaude/output-styles src/superclaude/agents src/superclaude/templates src/superclaude/rules src/superclaude/commands src/superclaude/skills/task src/superclaude/skills/tech-research src/superclaude/core` prints nothing. List the open items and the owner decisions this stage touches (OD3 for any later external judge; OD4 authority none). End with the sentence that the owner's go for stage 2 is given in chat and not by this file.

Acceptance criteria:
- `./artifacts/stage1-summary-for-owner.md` names, for each of Tasks 1 to 15, the files and the observed result, and each named file exists.
- The file shows the carrier `git diff --stat HEAD` command above with empty output.
- The file lists OD3 and OD4 and the open items, and ends with the sentence that the owner's go for stage 2 is given in chat and not by this file.
