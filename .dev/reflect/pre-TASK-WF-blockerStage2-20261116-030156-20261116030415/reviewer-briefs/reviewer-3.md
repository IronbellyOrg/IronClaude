# Reviewer 3 brief (refactorer, model class opus)

## T1 card excerpt

Assignment: independent pre-execution review of the plan `.dev/tasks/to-do/TASK-WF-blockerStage2-20261116-030156/TASK-WF-blockerStage2-20261116-030156.md` against its request `.dev/tasks/to-do/TASK-WF-blockerStage2-20261116-030156/source.md` (UC-1, advisory, read-only). Lens (refactorer): structure and feasibility against the real code. Check that each file, function, section, line number and count the plan names is real and says what the plan says it says, that the interfaces the plan assumes from the stage 1 and stage 0 plans exist under those names, that an executor can actually do each edit with the surfaces that exist, and look for defects introduced by splitting one 46-task plan into five.

The T1 points below are UNVERIFIED LEADS written by the orchestrator, not conclusions. Verify each against the files, drop the ones you cannot reproduce, and add defects the card missed. Severity rule (use exactly): BLOCKING = a requirement or check in the plan that cannot be met as written, a wrong or missing result, or data loss; MINOR = wording or format. Say for each finding whether the plan can still be executed correctly by an executor who follows it literally.

Return your findings as your final message (you cannot write files); the orchestrator saves them. For each finding give: id (R3-1, R3-2, ...), grade (blocking or minor), the plan location (PLAN:line), your evidence as file:line with a short quote, what the executor would do wrong, and the smallest fix. At most 8 findings, each under 700 characters. If a T1 lead is wrong, say so in a final section 'Leads dropped' with one line each. Cite only lines you have Read.

Plan = `.dev/tasks/to-do/TASK-WF-blockerStage2-20261116-030156/TASK-WF-blockerStage2-20261116-030156.md` (cited as PLAN:n). Spec = its `source.md` (SRC:n), the stage 2 request. Program spec = `.dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/02-brainstorm/merged-requirements.md` (PSPEC:n). Stage 1 plan = `.dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/TASK-WF-blockerStage1-20261116-030154.md` (S1:n). Stage 0 plan = `.dev/tasks/to-do/TASK-WF-blockerStage0-20261116-021044/TASK-WF-blockerStage0-20261116-021044.md` (S0:n).

**T1-1 (blocking?)** The skill edits call code that has no callable surface. Task 2 makes the task skill "write `qa/follow-ups.md` through the follow-up writer", make "the one sweep call", and run the safety route (PLAN:50). The stage 1 plan builds `follow_ups.py` and `safety_route.py` as modules with tests only (S1:110, S1:183) and its only new command is `classify` (S1:171); stage 2 Task 1 builds `sweep.py` as a module with tests only (PLAN:33). `superclaude review` lists no follow-ups, sweep or safety subcommand (`src/superclaude/cli/review/__init__.py`, ledger_cmd.py pattern). The task skill is Markdown, so the only way to "call" them is prose naming a `uv run python -c` snippet whose signature no task fixes. Task 2's acceptance lines only grep for words (PLAN:53-58).

**T1-7 (non-blocking?)** Existing tests that pin the edited skills are not run by Tasks 2 and 3: `tests/skills/test_review_prompt_overrides.py:274-276`, `test_task_builder_merge.py`, `test_review_loop_extension.py` (named in `artifacts/codegraph-grounding.md` "Dependents"). Acceptance runs only the two severity tests (PLAN:58) and `-k "tech_research or review_severity"` (PLAN:67), which selects no tech-research test file (none exists).

**T1-8 (non-blocking?)** Smaller points. (a) Task 1 gives the sweep no input contract: how it finds "decision-basis sections" per deliverable kind (PSPEC:246-252) is left open (PLAN:33). (b) Nothing in the package shows that the request's no-edit list was respected: the stage 1 plan has a `git diff --stat` check (S1:221), this plan has none (PLAN:112-115). (c) PLAN:20 says the old definition "still decides every gate outcome" while Task 2 makes GR12 live, which can stop an attended gate for a person (PSPEC:322). (d) Task 3 forbids the word "sweep" in tech-research (PLAN:65) while also saying in prose that it gets no sweep call (PLAN:62), so the one-offer sentence must avoid the word.

## Items checked and found sound

Cap-sentence count matches: `task/SKILL.md` lines 258, 372, 409 and `tech-research/SKILL.md` lines 490, 555 hold the exact sentence; "highest severity" occurs on 2 lines of `task/SKILL.md` (252, 361); no "sweep" in either skill today; the "Post-Completion Validation (Final Phase Only)" heading exists (`task/SKILL.md:288`); WC-4's key list is `WORKER-CONTRACT.md:33` and "the coordinator opens it" is :39; `pragmatic.md:225` holds the legacy definition sentence; no plugin mirror exists for the task or tech-research skills. Stage 1 creates `follow_ups.py`, `safety_route.py`, `classifier_inputs.py`, the `classify` command, `registry.yaml` and `stage1-summary-for-owner.md` (S1:110, 183, 148, 171, 96, 221). The stage 0 package creates `fresh-findings.md`, `stage0-heldout-ids.json` (S0:82, 96).

## Self-assessed confidence (not used for routing; the blind calibrator re-grades it)

0.72. T1-1 to T1-3 were verified against the files cited; none was reproduced by running anything because the stage 1 modules do not exist yet.


## Grounding hunks

codegraph run state: index_state=fresh checked_at=2026-11-16T03:12:04Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel projectPath=/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel


### .dev/tasks/to-do/TASK-WF-blockerStage2-20261116-030156/TASK-WF-blockerStage2-20261116-030156.md:31-41

```markdown
## Task 1: Build the final-gate sweep in record-only form

Create `src/superclaude/cli/review/sweep.py` for GR7: at the last gate before delivery, every open Medium row is re-tested, and a row whose flawed text or figure appears, uncorrected, in a decision-basis section of the final deliverable is flagged. The function has a `promote` switch that defaults to off. With it off (stage 2) a flagged row is written to the ledger as `sweep-flagged` and no grade changes; with it on (from the stage 3 package) the flagged row becomes Blocking at that gate. Today no final gate reads a ledger (the task skill's "Post-Completion Validation (Final Phase Only)" section runs one final validation and names no ledger; tech-research's Gate 5 enumerates findings and reads no ledger). Create `tests/review/test_review_sweep.py` for T16 and for the stage 2 rule.

Acceptance criteria:
- The stage ledger `stage-requests/README.md` in PF has an owner go for stage 2 with a date (the go is a chat message recorded there by the session that received it); when the row has none, this check fails and the run halts for the owner's Ruling.
- `uv run python -c "from superclaude.cli.review import follow_ups, safety_route, classifier_inputs"` succeeds (the stage 1 modules exist) and the stage 1 package's `./artifacts/stage1-summary-for-owner.md` (read by package id) exists.
- `uv run pytest tests/review/test_review_sweep.py -v` passes; with `promote` off a Medium row whose flawed figure reaches the final decision basis uncorrected is returned as `sweep-flagged` and no verdict changes; with `promote` on the same row is returned as Blocking, and a corrected one is not flagged either way.
- The sweep never lowers a grade and never touches a Note row.
- The module reads only the ledger path that the ledger reader returns (no second reader of `follow-ups.md`).
- A test asserts that with the default (`promote` off) the result of a gate that includes the sweep equals the result of the same gate without it.
```

### .dev/tasks/to-do/TASK-WF-blockerStage2-20261116-030156/TASK-WF-blockerStage2-20261116-030156.md:60-67

```markdown
## Task 3: Make tech-research write the ledger in shadow mode

Edit `src/superclaude/skills/tech-research/SKILL.md`: the same reviewer-brief fields (`rests_on` and `why not blocking`), ledger path `qa/follow-ups.md` next to the consolidated findings, the safety route and the shadow classifier call as Task 2. It gets no sweep call and no offer of its own: it runs inside `/task` (its step "Execution transfers to /task"), which owns the one sweep and the one offer at the end of the run. At each sentence "After 2 fix cycles (3 reviews), HALT and escalate to the user with the open blocking findings" in this file (today two checklist items of the task-file template in section A.7, near lines 490 and 555) add one sentence that the escalation's offer is the task skill's end-of-run offer, so a halt shows one offer and not two. Run `make sync-dev` afterwards.

Acceptance criteria:
- `src/superclaude/skills/tech-research/SKILL.md` names `qa/follow-ups.md` and the reviewer-brief fields, and `grep -n "sweep" src/superclaude/skills/tech-research/SKILL.md` prints nothing.
- The sentence "After 2 fix cycles (3 reviews), HALT and escalate to the user with the open blocking findings" still appears at each place it appears today, each with the one-offer sentence beside it.
- `uv run pytest tests/skills -k "tech_research or review_severity" -v` passes.
```

### .dev/tasks/to-do/TASK-WF-blockerStage2-20261116-030156/TASK-WF-blockerStage2-20261116-030156.md:81-89

```markdown
## Task 5: Pin the shadow-stage reviewer briefs

Depends on: Task 2, Task 3

Create `tests/skills/test_review_brief_rests_on.py` for T9: the reviewer brief of `src/superclaude/skills/task/SKILL.md` and of `src/superclaude/skills/tech-research/SKILL.md` must carry the `rests_on` and `why not blocking` fields. Also assert that the legacy definition text of `src/superclaude/output-styles/pragmatic.md` (the sentence "Grade every review finding as blocking or minor" and the bullets around it) is unchanged, while the registry row for `output-styles/pragmatic.md` in `src/superclaude/skills/sc-review-severity/refs/registry.yaml` is in state `legacy`; once that row is `v2` the assertion is skipped, so the stage 3 package's pragmatic.md task does not turn the test red.

Acceptance criteria:
- `uv run pytest tests/skills/test_review_brief_rests_on.py -v` passes and fails when either field is removed from either skill.
- A test fails if the legacy definition text of `pragmatic.md` changes while its registry row is `legacy`, and a test shows the assertion is skipped when the row is set to `v2` in a temporary registry copy.
```

### .dev/tasks/to-do/TASK-WF-blockerStage2-20261116-030156/TASK-WF-blockerStage2-20261116-030156.md:94-104

```markdown
## Task 6: Evaluate the classifier on the stage 0 populations

Depends on: Task 1, Task 2, Task 3, Task 4, Task 5

Run the classifier of the stage 1 modules (`superclaude review classify`, the `classifier_inputs.py` supplier, the question set v1) on the three sets the stage 0 package built, read by package id: the fresh-findings set (`./artifacts/fresh-findings.md`), the held-out half of the 318 rows (`./artifacts/stage0-heldout-ids.json`) and the reviewer-called-minor set (its ids in that file, its scores in `fresh-findings.md`, section for the Task 2 sample). The judge answers come from three blind agents that did not write the questions, three replicates each, recorded in fixture files; no Jev and no external service is called. Report each set separately and never pool them. Write `./artifacts/stage2-classifier-eval.md`: per set the agreement with the panel consensus, Cohen's kappa, the confusion matrix, recall on the panel's blockers, the flip rate over three replicates, the split by deliverable kind, the count of rows that had each code-supplied input (required-item list, constraint lines, verified evidence excerpt), and the limits. State that this is not an authority test (OD4).

Acceptance criteria:
- `./artifacts/stage2-classifier-eval.md` has one section per set (fresh findings, held-out half, reviewer-called-minor set) with the figures above, and no pooled figure.
- The three blind agents' ids are recorded and the file states none of them wrote the questions; the answer files are named and exist under `./artifacts/`.
- The file states that no judge other than the recorded blind agents was used, that no external service was called, and that no classifier authority follows (OD4).
- The file reports the count of rows per code-supplied input for each set, and each row where an input was not supplied has its answer recorded as UNSET or NA, never N.
```

### .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/TASK-WF-blockerStage1-20261116-030154.md:104-189

```markdown
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

```

### src/superclaude/cli/review/__init__.py:1-60

```python
"""superclaude review: deterministic helpers for document review loops.

Subcommand modules are optional, so branches that add different subcommands
merge without touching this file.
"""

from __future__ import annotations

import importlib

import click


@click.group(name="review")
def review_group() -> None:
    """Deterministic helpers for document review loops."""


for _name in (
    "panel_cmd",
    "merge_cmd",
    "ledger_cmd",
    "telemetry_cmd",
    "lint_cmd",
    "estimate_cmd",
    "cluster_cmd",
    "verify_cmd",
    "manifest_cmd",
):
    try:
        _module = importlib.import_module(f"{__name__}.{_name}")
    except ModuleNotFoundError as _exc:
        if _exc.name != f"{__name__}.{_name}":
            raise
        continue
    review_group.add_command(_module.command)
```

### tests/skills/test_review_prompt_overrides.py:268-282

```python
    assert "do not invent findings to avoid a zero" in flat, rel


@pytest.mark.parametrize(
    "rel",
    [
        "src/superclaude/skills/task/SKILL.md",
        "src/superclaude/skills/tech-reference/SKILL.md",
        "src/superclaude/skills/tech-research/SKILL.md",
        "src/superclaude/templates/workflow/01_mdtm_template_generic_task.md",
        "src/superclaude/templates/workflow/02_mdtm_template_complex_task.md",
    ],
)
def test_lens_prompts_state_no_minimum_count(rel):
    flat = _flat((_REPO / rel).read_text(encoding="utf-8"))
```

### src/superclaude/skills/tech-research/SKILL.md:488-491

```markdown
  - [ ] Spawn rf-qa (fix agent, fix_authorization: true) with consolidated blocking findings (minor findings stay as notes). Fix agent spawns additional targeted research agents for blocking gaps requiring new research (one per gap). Applies all blocking fixes.
  - [ ] Spawn rf-qa (verification, fix_authorization: false) + rf-qa-qualitative (verification, fix_authorization: false) to confirm fixes applied correctly
  - [ ] If verification finds new blocking issues (new minor findings are notes and do not restart the cycle): repeat Step 3.2 (max 2 cycles total). After 2 fix cycles (3 reviews), HALT and escalate to the user with the open blocking findings; log issues in Task Log

```

### src/superclaude/skills/tech-research/SKILL.md:553-556

```markdown
  - [ ] Spawn rf-qa (verification, fix_authorization: false) — verify fixes applied correctly, no new issues introduced. Output: `${TASK_DIR}qa/qa-fix-verification.md`
  - [ ] Spawn rf-qa-qualitative (verification, fix_authorization: false) — verify content quality maintained after fixes. Output: `${TASK_DIR}qa/qa-fix-verification-qualitative.md`
  - [ ] If blocking issues found (new minor findings are notes and do not restart the cycle): repeat Steps 6.5-6.6 (max 2 cycles). After 2 fix cycles (3 reviews), HALT and escalate to the user with the open blocking findings.

```

### src/superclaude/skills/tech-research/SKILL.md:612-615

```markdown

1. **Invoke /task** using the Skill tool with `skill: "task"` and `args` set to the task file path from Stage A (e.g., `.dev/tasks/to-do/TASK-RESEARCH-locomotion-params-20260309-120000/TASK-RESEARCH-locomotion-params-20260309-120000.md`).
2. **Execution transfers to /task**, which reads the task file and processes each checklist item via the F1 loop — spawning subagents as specified in B2 items and running phase-gate QA after each phase (Phase 2+).
3. **No additional execution logic is needed** in this skill since all execution rules (F1 loop, F2 prohibited actions, parallel spawning, F4 modification restrictions, F5 frontmatter protocol, error handling, session resumption) are provided by /task.
```

### src/superclaude/skills/task/SKILL.md:288-292

```markdown
### Post-Completion Validation (Final Phase Only)

After the LAST phase's phase-gate QA passes and BEFORE marking the task "Done," run a final validation pass on the complete output. This catches cross-phase consistency issues and divergent execution — cases where each phase passed individually but the overall result doesn't work as a whole.

**This runs ONCE, after the final phase, not after every phase.**
```

### .dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/02-brainstorm/merged-requirements.md:246-252

```markdown
| Deliverable kind | Decision-basis items | Source of the list | Available today? |
|---|---|---|---|
| Final research report or synthesis | recommendation, option ranking, destinations in the inventory, conflict-log outcomes, numbers quoted in those, stated reasons | the report's own sections, named by its template; a code check finds the quoted figure inside them | Yes [J] |
| Research input file (an upstream gate) | the declared consumers: which later item reads which figure, row or column | a consumer line per phase output in the task file ("feeds item X, reads column Y") | No. Without it, a finding whose consumer cannot be named keeps the reviewer's label, tagged `consumer-unknown` (section 4.2); OD14 decides whether such rows may wait for the final-gate sweep [J] |
| Spec | requirements, acceptance criteria, boundary-table rows, quoted constraints and non-goals | the spec's headings | Yes [J] |
| Tasklist | acceptance criteria, ordering and dependency edges, quoted constraints | the tasklist's items | Yes [J] |
| Code change under `/sc:implement` | acceptance criteria, declared outputs, quoted constraints | `qa.md` already collects them (`ac-outcome-missing`, `quoted-constraint-breach`) [V] | Yes |
```

### .dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/02-brainstorm/merged-requirements.md:653-653

```markdown
| GR7 | Final-gate sweep. | At the last gate before delivery, every open Medium is re-tested: does its flawed text or figure appear, uncorrected, in a decision-basis section of the final deliverable? If yes, it is Blocking at that gate. This is new code: no final gate reads a ledger today (`task/SKILL.md:290-292` runs one final validation and mentions no ledger; `tech-research/SKILL.md:415-419` enumerates findings and reads no ledger) [V]. Stage 2 owns it (section 12) | RC4: by the last gate the decision basis exists; also the precondition of OD14 |
```

## Coverage slice

| Requirement / Task | Card ID | Status | Grounding |
|---|---|---|---|
| INF-003: Reuse Tasks 26 to 30 of the revised 46-task plan `TASK-WF-loosenBlockerRev-20261115-210254 | none | covered | PLAN:12-14 header and Constraints PLAN:19-23 |
| INF-004: Stage 0 and stage 1 evidence is read by package id. | Task 6 | covered | source.md:7 |
| INF-009: Run the classifier of the stage 1 modules (`classify` command, `classifier_inputs.py` supp | Task 6 | covered | source.md:13 |
| INF-010: Write `./artifacts/stage2-classifier-eval.md`: agreement with the panel consensus, Cohen's | Task 6 | covered | source.md:13 |
| INF-011: State that it is not an authority test (OD4). | Task 6 | covered | source.md:13 |
| INF-012: Write `./artifacts/shadow_summary.py` (run with `uv run python`) that reads a list of shad | Task 7 | covered | source.md:14 |
| INF-013: Then write `./artifacts/stage2-summary-for-owner.md`: the classifier evaluation headline,  | Task 7 | covered | source.md:14 |
