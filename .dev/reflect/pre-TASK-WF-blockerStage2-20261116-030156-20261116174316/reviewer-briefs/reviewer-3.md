# Reviewer brief

Run: pre-TASK-WF-blockerStage2-20261116-030156-20261116174316 (UC-1). Plan and spec paths are in the T1 card header. You are read-only: Read, Grep, Glob and codegraph/search tools only. Audit the supplied hunks and the live files they cite; run nothing.

## T1 card excerpt

### F3 [MEDIUM, grounded] Task 1 entry check is narrower than the Constraints promise
Constraints say Task 1 checks that the stage 1 modules and "the `classify` command exist" (plan:20). Task 1's check imports only `follow_ups`, `safety_route`, `classifier_inputs` (plan:44). `classify_cmd.py`/`classifier.py` (Task 7 runs `superclaude review classify`, plan:126), `refs/scale-map.md` (Tasks 2 and 4 read it, plan:56, 88) and the registry row state `legacy` (Task 6 reads it, plan:113) are not checked. A missing one fails late (Task 4, 6 or 7), after edits.

### F4 [MEDIUM, grounded] `follow-ups write` input format is not defined
Task 2 says `write` "imports the non-blocking rows of reviewer report tables" (plan:56) but names no parser or table format; Task 4 only says "add two fields to the finding row" in five prompt templates (plan:88). Tests use fixture reports (plan:60-62), so nothing ties the real reviewer output to the parser; an unparsable report gives `capture_state: incomplete`, which would make every real run partial.

### F6 [MINOR, grounded] tech-research safety route depends on a "nobody reachable" signal it cannot know
Task 4: "with nobody reachable it records and does not wait" (plan:88), but tech-research has no unattended mode (plan:102), so the skill has no stated way to choose `--unattended`.

## Grounding hunks

codegraph run state: index_state=fresh checked_at=2026-11-16T17:48:47Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel projectPath=/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel (index covers py/yaml/js/ts, not Markdown: use Read/Grep for the plan, skills and spec)

### .dev/tasks/to-do/TASK-WF-blockerStage2-20261116-030156/TASK-WF-blockerStage2-20261116-030156.md:17-33

````markdown
## Constraints

- Spec: the merged spec `02-brainstorm/merged-requirements.md` inside the program folder `BLOCKER-CLASSIFICATION-PROGRAM-20261115` (found by that folder name under the repository's task folder). This plan calls that folder PF and the spec file the spec. Section numbers, requirement ids (REQ-nn), loop changes (L1 to L6), guardrails (GR1 to GR12), tests (T1 to T17) and owner decisions (OD1 to OD17) refer to the spec. PF also holds the 5-run results in `08-test/results.md`, the reconciliation in `09-plan-input.md`, the scored table in `04-historical/master-table.md`, the panel consensus in `05-scoring/consensus.md`, `OPEN-QUESTIONS.md` and the stage ledger and the five stage requests in `stage-requests/`. Evidence of earlier stages is read from their packages by package id (the ids are in the stage ledger), found by that folder name in the to-do or done subfolder of the repository task folder.
- One package, one stage. This is stage 2 of five packages (one plan per stage). The old definition still decides every gate outcome. The only exception the spec allows is the GR12 safety route, which asks a reachable person about a possible safety finding that was graded non-blocking and, with nobody reachable, records and does not wait. The sweep only records (`promote` off), the classifier has no authority, and the one sweep call sits in the final review step of `/sc:implement`. tech-research gets no sweep call and no offer. The package runs only after the stage 1 package is done (its modules `follow_ups.py`, `safety_route.py`, `classifier_inputs.py` and the `classify` command exist; Task 1 checks that) and the owner has said go in chat. Stage 3 starts only after the owner reads this package's summary and says go; its entry also needs at least 5 observed shadow runs, which the owner or operator produces over time and no task here can produce.
- Carrier decision (owner, 2026-11-16, recorded in `OPEN-QUESTIONS.md`): the follow-up carrier is the final review step of `/sc:implement`, record and print only. That step prints a list and asks nothing, because `refs/qa.md` of the `/sc:implement` protocol says its final summary "is informational and never asks the user anything" and closes the list of interrupts, so the edit goes into that protocol's `SKILL.md` and `refs/managed-workspace.md` only; the once-per-run offer question stays with the top-level session through the output style (the `pragmatic.md` Medium rule, changed from per loop to per run by the stage 3 package) and with the consent-bound filing path (OD15), and stage 2 adds no question to `/sc:implement`.
- Retired carriers are not edited. `/sc:task` and task-builder are being retired (owner, 2026-11-16). No task edits `src/superclaude/skills/task/`, `src/superclaude/skills/task-builder/`, `src/superclaude/agents/rf-task-builder.md` or anything that exists only for those; they keep today's text until the retirement removes them. Tests that exist only to pin them are not re-pinned here, and when a test pins both a retired and an active carrier this plan re-pins the active carrier's part only. The stage 1 scale map lists them as exempt-by-retirement by path.
- Plugin surface. IronClaude is installed from the Coder template or from a git clone plus `superclaude install`, not as a plugin, so this package creates no plugin surface (no new plugin mirror, no plugin parity test, no registry row for a plugin path). One existing hand-kept twin is touched: `plugins/superclaude/skills/sc-implement-protocol/` is pinned byte for byte to its source by `test_h_implement_protocol_plugin_twins_byte_equal` in `tests/skills/test_review_severity_rule.py` and by the managed-workspace mirror check in `tests/skills/test_reflect_input_snapshot.py`. Task 3 therefore copies exactly the two edited files to it, and for no other reason. The owner has not confirmed removing plugin parity (`OPEN-QUESTIONS.md` section 3.4); this plan does not decide it.
- Ledger decision (owner question 5): `follow-ups.md` stays a separate file in version 1. No task here maps its rows to `review-ledger/1` rows or edits `src/superclaude/cli/review/ledger.py`; the stage 1 reuse-audit result decides whether a mapping is ever added.
- Owner decisions use the spec's recommendations unless the owner changes them: OD1 skill folder `sc-review-severity`; OD2 once per run plus at any escalation halt (the offer itself is the top-level session's, see the carrier decision); OD4 the classifier has no authority in version 1; OD9 reviewer-named consumer, code-checked where quotable; OD11 replace label-max merging at all 13 lines in 10 files, staged; OD12 yes; OD13 short Note rows; OD14 a finding with an unknown consumer keeps the reviewer's label (no deferral); OD15 consent-bound body file posted by the attended top-level session; OD16 option (b) at stage 3. OD3 (finding text leaving the machine), OD5 to OD8 and OD10 are not decided here and no task depends on a different answer.
- Not built here: any Jev or other external judge call, any TypeSafe account or key, a Jev or LLM judge class (they wait for OD3), any change to `src/superclaude/skills/sc-implement-protocol/refs/qa.md` (it keeps its own scale; its SHA-256 is recorded in Task 1 and compared in Task 3 and Task 8), any change to the own-scale primitives listed in spec section 9.3 as unchanged, code-assigned severity in `src/superclaude/cli/**/*.py` (for example `fmea_classifier.py` and `remediate_parser.py`, out of scope by spec section 10.3), the 35 percent score target, and any change to the cap of 2 fix cycles. No edit of `pragmatic.md`, `rf-qa.md`, `rf-qa-qualitative.md`, `rf-analyst.md`, templates, rule prompts, builders or researchers, and no promotion of swept rows to Blocking.
- Command ownership. Stage 1 owns `classify_cmd.py` (the `classify` command). This package owns `follow_ups_cmd.py` (the `follow-ups` command group with the subcommands `write`, `safety`, `sweep` and `summary`) because it also builds `sweep.py`, which the group wraps. Both register through the tuple of subcommand module names in `src/superclaude/cli/review/__init__.py`. The stage 1 acceptance line saying that only the new module and its command wiring mention `follow_ups` describes the end of stage 1; after Task 2 two more files mention it.
- Classifier facts that bind every classifier task: the 5-run test (stage 0 package, `stage0a-result.md`, from PF `08-test/results.md`) used a text-only stand-in judge and got agreement with the panel of 58.5 percent (Cohen's kappa 0.27), and the missing-item, constraint and contradiction questions (M, C, E) were at chance without code-supplied inputs. So M, C and E run only when code supplies the required-item list, the constraint lines and the verified evidence (the classifier-inputs supplier of stage 1), the "M or C is Y gives BLOCKING" row is never enabled for any gate, and confidence is reported as an ordinal band, never as a probability. The only judge classes that exist are `FixtureJudge` (recorded answers) and `ReviewerJudge` (the reviewer's own label read back); a live shadow run has no recorded judge unless the run owner supplies an answers file, so its `classifier` column reads `unavailable` and `ReviewerJudge` agreement (100 percent by construction) never counts as a figure.
- Safety misses. The stage 3 entry needs zero safety misses and no capture failure. A safety miss is defined in the spec's stage 0 draft (a finding that a later review or the owner confirms as a security, data-loss or safety-boundary risk that a shadow run recorded as a follow-up or Note and did not route through GR12). A ledger holds no such confirmation, so the Task 8 script reads a confirmation file and prints "not computable" without one, never a bare zero.
- Pins are by content. An acceptance check that must survive a task's own edit quotes the sentence it protects; it does not name a line number, because the edit moves the line. Line numbers in a task body are where the text sits today and are re-read before editing. An acceptance line that a later task of this package makes false carries its end point ("until Task N"). New text added to installed primitives avoids the words the existing static pins scan for (the halt, stop and ruling words of `tests/skills/test_implement_severity_static.py`, the old cap wording and the sweep-phrase patterns of `tests/skills/test_review_severity_rule.py`) and cites no `SKILL.md:<number>` style pointer.
- `src/superclaude/` is the source of truth. Edit there, then run `make sync-dev`; nothing under the project `.claude/` folder is staged (only `.claude/settings.json` is tracked). Installed primitives name installed paths (`~/.claude/skills/...`) first and project `.claude/...` second, never a `src/superclaude/` path.
- Python work uses UV only: `uv run pytest ...` and `uv run python ...`, never `python -m` or bare `pip`.
- Task-owned evidence and generated outputs go under `./artifacts/` in this package. `.dev/tasks/` is always staged (`git add .dev/tasks`), packages and their `./artifacts/` included, and no document a task writes says it is not staged. Staging is not committing.
````

### .dev/tasks/to-do/TASK-WF-blockerStage2-20261116-030156/TASK-WF-blockerStage2-20261116-030156.md:84-96

````markdown
## Task 4: Make tech-research write the follow-up ledger

Depends on: Task 2

Edit `src/superclaude/skills/tech-research/SKILL.md` by adding new lines only; the lines the existing tests pin stay as they are (the "INDEPENDENT STANCE" sentence with "no minimum count", the severity and verdict lines of the prompts, and the two cap sentences "After 2 fix cycles (3 reviews), HALT and escalate to the user with the open blocking findings"; this package adds no text beside the cap sentences because it makes no offer). Five reviewer prompt templates (Research QA, Synthesis QA, Report Validation QA, Qualitative QA, Lens-Specific QA) each get one added paragraph: for every finding you grade non-blocking under your current definition, add two fields to the finding row, `rests_on` (the named consumer that does not change, or `none`, or `unknown`) and `why not blocking` (one line); blocking findings need neither. The three consolidation checklist items of phases 3, 5 and 6 (the ones that write `qa-consolidated-findings-phase3.md`, `phase5` and `phase6`) each get one added line: the run owner writes `${TASK_DIR}qa/follow-ups.md` with `superclaude review follow-ups write` over the reviewer reports of that phase (the tier of a native label is the shared outcome that `~/.claude/skills/sc-review-severity/refs/scale-map.md` gives it, project `.claude/skills/sc-review-severity/refs/scale-map.md` second), then runs `superclaude review follow-ups safety` over the ledger: with a person reachable it shows the rows the command prints before the gate passes, and with nobody reachable it records and does not wait. One added line says the classifier is called in shadow mode only when the run owner holds a recorded judge-answers file (`superclaude review classify`), that otherwise the `classifier` column stays `unavailable`, and that its verdict changes no gate outcome. The Output Locations table gets one row for the ledger. One sentence says this skill makes no sweep call and no offer. Run `make sync-dev` afterwards.

Acceptance criteria:
- The five prompt templates each contain `rests_on` and `why not blocking`, `${TASK_DIR}qa/follow-ups.md` appears in the file, and the three consolidation items each name `superclaude review follow-ups write`.
- `git diff -U0 HEAD -- src/superclaude/skills/tech-research/SKILL.md | grep '^+' | grep -ci "sweep"` prints 0 (the one sentence that says there is no sweep avoids the word), and the diff removes no line (`git diff --numstat HEAD -- src/superclaude/skills/tech-research/SKILL.md` shows 0 deleted lines).
- The sentence "After 2 fix cycles (3 reviews), HALT and escalate to the user with the open blocking findings" still appears at each place it appears today, unchanged.
- `uv run pytest tests/skills/test_review_prompt_overrides.py tests/skills/test_review_severity_rule.py tests/skills/test_review_severity_mapping.py tests/skills/test_worker_contract.py tests/unit/test_cli_install.py -v` passes (the pytest keyword filter `tech_research` selects nothing because the test ids spell `tech-research`, so the files are named instead).

## Phase 3: Add the worker-contract keys and pin the new text
````

### .dev/tasks/to-do/TASK-WF-blockerStage2-20261116-030156/TASK-WF-blockerStage2-20261116-030156.md:52-64

````markdown
## Task 2: Add the follow-ups command group

Depends on: Task 1

Read `src/superclaude/cli/review/__init__.py` (it registers nine subcommand modules today and none for follow-ups, the safety route or the sweep, so a skill can name no working command until this task adds one) and the stage 1 modules `follow_ups.py` and `safety_route.py`, and write `./artifacts/follow-ups-cmd-wiring.md` naming each stage 1 function the commands call. Create `src/superclaude/cli/review/follow_ups_cmd.py` exporting `command` (a click group named `follow-ups`), add `"follow_ups_cmd"` to the tuple in `__init__.py`, and give it four subcommands. `write --ledger <path> --report <reviewer report> (repeatable) --run-id <id> --gate-id <id> [--expected-revision <n>]` imports the non-blocking rows of reviewer report tables through the stage 1 writer (the run owner is the only writer; a reviewer report row carries the fields `rests_on` and `why not blocking`; the tier of a row is the shared outcome that `refs/scale-map.md` gives its native label; Blocking rows are never written; a Medium row without `why not blocking` is refused by the writer and reported; a report that cannot be read sets `capture_state: incomplete` with the reason). `safety --ledger <path> [--judge-answers <file>] [--unattended]` runs the stage 1 safety route over the ledger and prints what it returns: attended text names the person prompt, unattended output sets the signal that makes the run `partial`. `sweep --root <dir> | --ledger <path> (repeatable) --deliverable <path> (repeatable) --kind auto|report|spec|tasklist|code|other [--promote] [--write] [--output <file>]` calls Task 1's sweep, prints the flagged rows (id, deliverable, section) and the skipped count, writes the same text to `--output` when given, exits 0 whenever it ran (flagged rows are information) and non-zero only when it cannot run. `summary --ledger <path>` prints exactly the three worker-contract keys as YAML (`follow_up_ledger`, `follow_up_counts` with `follow_up`, `note` and `show_user`, `follow_up_capture_state`); this is the named producer of those keys for Task 5. No subcommand calls `gh`, a network or a judge. Create `tests/review/test_review_follow_ups_cmd.py`.

Acceptance criteria:
- `uv run superclaude review follow-ups --help` exits 0 and lists `write`, `safety`, `sweep` and `summary`; `uv run superclaude review --help` still lists every earlier subcommand (and `classify` from the stage 1 package) and now lists `follow-ups`.
- `uv run pytest tests/review/test_review_follow_ups_cmd.py tests/review/test_review_cli.py tests/review/test_review_sweep.py -v` passes.
- A test shows `sweep` without `--promote` and `--write` leaves the ledger bytes unchanged and does not promote, and `write` run twice on the same report leaves the ledger as after the first run.
- A test shows `summary` prints exactly the three keys, and `follow_up_capture_state` reads `incomplete` with a reason after an unreadable report.
- `grep -n "subprocess\|requests\|httpx\|\bgh\b" src/superclaude/cli/review/follow_ups_cmd.py` prints nothing.
- `./artifacts/follow-ups-cmd-wiring.md` names each stage 1 function used and states that this package owns `follow_ups_cmd.py`.
````

### src/superclaude/cli/review/__init__.py:1-40

````python
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

````

### .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/TASK-WF-blockerStage1-20261116-030154.md:116-125

````markdown
## Task 7: Build the follow-up ledger codec, reader and writer

Depends on: Task 4

First run the `reuse-auditor` agent on the proposed module against `src/superclaude/cli/review/ledger.py` (schema `review-ledger/1`) and record its verdict in `./artifacts/reuse-audit-follow-ups.md`; share code only where it says reuse-by-import. Decision for version 1 (owner question of 2026-11-16 on the follow-up ledger): `follow-ups.md` stays a separate file, no mapping of its rows to `review-ledger/1` rows is built by this program, and no task replaces or edits `ledger.py`; the audit verdict is reported to the owner in Task 16 and decides whether a mapping is ever added later. The "ledger adapters" of the spec's stage 1 row are the modules this package builds: `follow_ups.py` (Tasks 7 and 8), `classifier_inputs.py` (Task 10) and the `classifier` column writing of `classify_cmd.py` (Task 12). Then create `src/superclaude/cli/review/follow_ups.py`: one reader and one writer for `follow-ups.md` only (REQ-07 location rule, REQ-08 sole writer with an expected-revision check and atomic replace, REQ-10 entity codec with evidence blocks and a fence longer than any backtick run, identity tuple and observation import that is idempotent, the sort order of spec section 6.2, and the item states: the eight of spec section 6.2 plus `sweep-flagged`, defined in Task 4). A malformed ledger is preserved and reported, never reset. Create `tests/review/test_review_follow_ups.py` for T7: required columns, a Medium row without `why_not_blocking` is refused, identity never merges on a digest alone, codec round trip for pipes, backticks, a triple-backtick line, literal entities, Unicode and multiline text, a stale writer cannot overwrite a newer revision, a malformed ledger is preserved.

Acceptance criteria:
- `uv run pytest tests/review/test_review_follow_ups.py -v` passes and covers each T7 failure condition above.
- `./artifacts/reuse-audit-follow-ups.md` exists with the audit's verdict and the line "Version 1: `follow-ups.md` stays a separate file; no mapping to `review-ledger/1` rows is built", and the module imports from `ledger.py` only where the audit says to.
- Until Task 10 adds an importer, `grep -rln "follow_ups" src/superclaude/cli/review` lists only `follow_ups.py`. From Task 10 on, the only other files it may list are `classifier_inputs.py`, `classify_cmd.py` and `safety_route.py`, and no module other than `follow_ups.py` defines a reader or writer of `follow-ups.md`.
````

### .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/TASK-WF-blockerStage1-20261116-030154.md:142-165

````markdown
## Task 9: Build the classifier module

Depends on: Task 3, Task 5

Create `src/superclaude/cli/review/classifier.py` and `src/superclaude/cli/review/data/classifier_thresholds.json`. The module holds the truth table of spec section 7.3 (version 2, ported from `07-classifier/truth_table.py` in PF and the sketch `02-brainstorm/blocker_truth_table_sketch.py`: states Y, N, U, UNSET, NA; NA reachable only from a deliverable-kind declaration, REQ-19; precedence, the W and E combination of REQ-17, the lift rule of REQ-18), the bands (S: Y at 0.30 or more, N at 0.10 or less; others 0.70 and 0.30), ordinal confidence bands with the replicate rule of spec section 7.4 (median of 3, spread above 0.20 counts as U), the `dependence-safe lower bound max(0, pW + pD - 1)` reported beside the band, and a `Judge` interface with two implementations: `FixtureJudge` (recorded answers) and `ReviewerJudge` (the reviewer's own label read through the scale map as 0 or 1: it parses the `labels` column of the packaged `refs/scale-map.md` built in Task 3, found relative to the `superclaude` package folder, and holds no second copy of the label mapping). The module also holds `run_questions(judge, finding, allowed)`, which asks the judge only the questions in the set `allowed` and gives every other question UNSET (NA only through the deliverable-kind function). A judge failure is a typed `UNDETERMINED` result that moves to the next judge, never a table cell and never an N. Thresholds live only in the JSON file.

Acceptance criteria:
- `uv run python -c "from superclaude.cli.review.classifier import verdict"` succeeds and `verdict` agrees with the sketch on all 6,400 combinations of the REQ-21 property tests.
- No Jev, LLM or network class exists in the module (`grep -n "typesafe\|requests\|httpx\|anthropic" src/superclaude/cli/review/classifier.py` prints nothing).
- A judge answer of `None` yields UNSET, and the function that sets NA takes a deliverable-kind argument and no probability.
- `ReviewerJudge` holds no label-to-outcome dictionary of its own: it reads the Task 3 table (the temporary-map test of Task 11 shows it), and `run_questions` never calls the judge for a question outside `allowed`.
- `src/superclaude/cli/review/data/classifier_thresholds.json` is the only place the band numbers appear.

## Task 10: Build the supplier of the classifier's code-supplied inputs

Depends on: Task 7, Task 9

Create `src/superclaude/cli/review/classifier_inputs.py` and `tests/review/test_review_classifier_inputs.py`. Given a deliverable file, its declared kind (spec, tasklist, report, code, other) and a finding, the module returns three things. The required-item list: for a spec, its requirement ids and acceptance criteria; for a tasklist, the acceptance-criteria bullets of each task; for a report, the sections its governing template requires; for a kind declared to have no such list, the marker that makes the classifier read M as NA. The constraint lines: quoted constraints and non-goals (a `## Constraints` section, "Will Not" or "Not built" lists). The evidence excerpt: the finding's cited path and line re-read from disk and marked `verified` when the quoted text is present within 2 lines of the cited line and `unverified` otherwise. A missing or unreadable source gives UNSET for that input, never NA and never N. The module also holds `questions_to_ask(inputs)`, the one place in code where the rule "M, C and E only with supplied inputs" lives: it returns S, W and D always, E only with a verified evidence excerpt, M only with a supplied required-item list and C only with supplied constraint lines, and the caller passes that set to `run_questions` of Task 9. Reuse the reader of Task 7 for ledger rows and the parsers the existing `cli/review` modules already have (Read `src/superclaude/cli/review/findings_v2.py` and `src/superclaude/cli/review/card_convert.py` first and import from them where they cover the job).

Acceptance criteria:
- `uv run pytest tests/review/test_review_classifier_inputs.py -v` passes with fixtures for a spec, a tasklist and a report, a kind with no list (NA), an unreadable file (UNSET) and a cited line whose quote is absent (`unverified`).
- Each input function returns a value that says whether it was supplied, so a caller can count rows by input.
- The same test file asserts `questions_to_ask`: M is absent without a required-item list, C without constraint lines, E without a verified excerpt, and S, W and D are always present.
- `grep -n "subprocess\|requests\|httpx" src/superclaude/cli/review/classifier_inputs.py` prints nothing (read-only, no network).
````

### .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/TASK-WF-blockerStage1-20261116-030154.md:180-203

````markdown
## Task 12: Add the `superclaude review classify` command

Depends on: Task 3, Task 7, Task 9, Task 10

Create `src/superclaude/cli/review/classify_cmd.py` exporting `command` (a click command named `classify`) and add `"classify_cmd"` to the tuple of subcommand module names in `src/superclaude/cli/review/__init__.py`. It reads findings plus a judge answers file, runs the classifier in shadow mode, asks M, C and E only for findings whose inputs `classifier_inputs.py` supplied (it calls `questions_to_ask` and passes the result to `run_questions`), writes the verdict, band and judge id with version into the ledger row's `classifier` column beside the reviewer's label, and prints the per-run disagreement matrix read through the scale map (never through the Boolean of `card_convert.py`) and one count line per input (rows with a required-item list, rows with constraint lines, rows with a verified evidence excerpt). The name `classify` must not clash with the review subcommands present today (`panel`, `merge`, `ledger`, `telemetry`, `cluster`, `verify` and `manifest`; `lint` and `estimate` are optional names in the `__init__.py` tuple whose modules do not exist yet). Create `tests/review/test_review_classify_cmd.py`.

Acceptance criteria:
- `uv run superclaude review classify --help` exits 0 and `uv run superclaude review --help` still lists every earlier subcommand.
- `uv run pytest tests/review/test_review_classify_cmd.py tests/review/test_review_cli.py -v` passes.
- A run with no judge available records `classifier=unavailable` and leaves the reviewer's label standing; it never invents a verdict.
- The printed output includes the three input-count lines, and a test asserts them for a fixture with one supplied and one unsupplied input.

## Task 13: Build the safety route

Depends on: Task 7, Task 9

Create `src/superclaude/cli/review/safety_route.py` with the GR1 vocabulary scan (one list of destructive and secret words: delete, overwrite, force, token, secret, password, chmod and similar, kept in one place) and the GR12 rule: a hit on a non-blocking row, or a judge answer S = Y or S = U on a row a reviewer graded non-blocking, tags the row `protected-risk-dispute` and never writes it as a plain follow-up. It can only raise a grade. Add `tests/review/test_review_safety_route.py` for T17 and for the second half of T12: in a default configuration the safety route is the only path by which a classifier verdict from Task 9 changes a grade.

Acceptance criteria:
- `uv run pytest tests/review/test_review_safety_route.py -v` passes and covers a vocabulary hit, S = Y and S = U on a minor row.
- No function in the module lowers a grade (a test asserts the outcome order never decreases).
- A test shows that, in a default configuration, a classifier verdict changes a grade only through the safety route, and that a verdict on a row with no vocabulary hit and no S answer of Y or U changes nothing.
- Attended output text names the person prompt; unattended output sets the signal that makes the run `partial`, per spec section 6.4.

````

### .dev/tasks/to-do/TASK-WF-blockerStage3-20261116-030158/TASK-WF-blockerStage3-20261116-030158.md:22-26

````markdown
- Owner decisions use the spec's recommendations unless the owner changes them: OD1 skill folder `sc-review-severity`; OD2 once per run plus at any escalation halt; OD4 the classifier has no authority in version 1; OD9 reviewer-named consumer, code-checked where quotable; OD11 replace label-max merging at all 13 lines in 10 files, staged; OD12 yes; OD13 short Note rows; OD14 a finding with an unknown consumer keeps the reviewer's label (no deferral); OD15 consent-bound body file posted by the attended top-level session; OD16 option (b) at stage 3. OD3 (finding text leaving the machine), OD5 to OD8 and OD10 are not decided here and no task depends on a different answer.
- Retired carriers are not edited. The owner is retiring `/sc:task` and the task-builder: no task here edits `src/superclaude/skills/task/`, `src/superclaude/skills/task-builder/` or `src/superclaude/agents/rf-task-builder.md`. `src/superclaude/skills/task/SKILL.md` still holds two merge-rule lines; the stage 1 allow-list in `refs/scale-map.md` lists that path as `exempt-by-retirement` (by path only), and the exemption ends when the retirement removes the file. Tests that exist only to pin the retired files are not re-pinned here; where one test pins both a retired and an active carrier, only the active carrier's part is re-pinned.
- Follow-up carrier. The sweep call and the printed follow-up list sit in `/sc:implement`'s final review step: the stage 2 package put them in `src/superclaude/skills/sc-implement-protocol/SKILL.md` (final summary instructions) and `src/superclaude/skills/sc-implement-protocol/refs/managed-workspace.md` (archive gate, run before the package moves). This stage only adds `--promote` to that call (Task 9). The carrier records and prints and asks nothing, because `refs/qa.md` keeps its own scale and its closed list of interrupts; the once-per-run offer question stays with the top-level session through the output style (the Medium rule of `pragmatic.md`, changed from per loop to per run in Task 5) and with the consent-bound filing path (OD15), so `/sc:implement` gains no question.
- Plugin surface. IronClaude is installed from the Coder template or from a clone plus `superclaude install`, not as a plugin, so this package creates no plugin surface (no plugin mirror of the skill folder, no plugin parity test, no plugin registry row). Nothing under `plugins/` is edited except the byte-equal twins of the two implement-protocol files that Task 9 edits, which the existing test `test_h_implement_protocol_plugin_twins_byte_equal` in `tests/skills/test_review_severity_rule.py` pins. `src/superclaude/commands/spec-panel.md` and its plugin twin keep their text in this stage: their "once per loop" wording, pinned by `tests/skills/test_review_severity_mapping.py`, `tests/skills/test_review_loop_extension.py` and `tests/skills/test_spec_panel_review_loop.py`, moves with the spec-panel narrowing in stage 4. The registry keeps exactly 11 `digest` rows, 1 `canonical`, 2 `pointer-only` and 5 `installed-only`. Whether plugin parity is dropped for good is the owner's decision and is not made here.
- Not built here: any Jev or other external judge call, any TypeSafe account or key, a Jev or LLM judge class (they wait for OD3), any change to `src/superclaude/skills/sc-implement-protocol/refs/qa.md` (it keeps its own scale), any change to the own-scale primitives listed in spec section 9.3 as unchanged, code-assigned severity in `src/superclaude/cli/**/*.py` (for example `fmea_classifier.py` and `remediate_parser.py`, out of scope by spec section 10.3), any mapping of `follow-ups.md` to `review-ledger/1` rows or edit of `src/superclaude/cli/review/ledger.py` (version 1 keeps the follow-up ledger as its own file), the 35 percent score target, any change to the cap of 2 fix cycles, and any template, rule-prompt, builder, researcher or spec-panel edit (those are stage 4).
````

### .dev/tasks/to-do/TASK-WF-blockerStage3-20261116-030158/TASK-WF-blockerStage3-20261116-030158.md:177-181

````markdown
Read the stage 2 paragraph "Follow-up sweep (record and print only)" in `src/superclaude/skills/sc-implement-protocol/SKILL.md` and its twin paragraph in `src/superclaude/skills/sc-implement-protocol/refs/managed-workspace.md` (the one sweep call, `superclaude review follow-ups sweep`, made at the final review step before the package moves) and edit only those paragraphs: add `--promote` to the call line in each file and replace the stage 2 words "never `--promote`" with the statement that the call now passes `--promote`, so a Medium row whose flawed text or figure reaches a decision-basis section of the delivered files uncorrected is returned as Blocking and printed first in the final follow-up list. Keep the sentence "It asks the user nothing" and the statements that the step makes no offer, changes no verdict, no final-review result and no archive outcome, and adds no new code; add no line that holds the words halt, Ruling, `E-HALT-QA` or `E-ARCHIVE-BLOCKED` (`tests/skills/test_implement_severity_static.py` scans new lines for them). Do not edit `refs/qa.md`. Update the stage 2 test `tests/skills/test_implement_follow_up_sweep.py` so it expects `--promote` on both call lines and replaces its "`--promote` added to the call line" mutation case with a "`--promote` removed" case; its other mutation cases (the paragraph moved after the step 6 line, a question added) stay. Copy the two edited files byte for byte with `cp` to the existing plugin twins `plugins/superclaude/skills/sc-implement-protocol/SKILL.md` and `plugins/superclaude/skills/sc-implement-protocol/refs/managed-workspace.md`: they are touched only because `test_h_implement_protocol_plugin_twins_byte_equal` in `tests/skills/test_review_severity_rule.py` pins them equal to the source files, and no other plugin file changes. Run `make sync-dev` afterwards.

Acceptance criteria:
- `grep -c "superclaude review follow-ups sweep" src/superclaude/skills/sc-implement-protocol/SKILL.md src/superclaude/skills/sc-implement-protocol/refs/managed-workspace.md` still prints 1 for each file, each call line now holds `--promote` and neither holds `--write`, and the sentence "It asks the user nothing" is still in `SKILL.md`.
- `git diff --stat -- src/superclaude/skills/sc-implement-protocol/refs/qa.md` prints nothing, and `cmp` of each of the two source files with its plugin twin prints nothing.
````

### src/superclaude/skills/tech-research/SKILL.md:129-152

````markdown
## Output Locations

All persistent artifacts go to the task folder `${TASK_DIR}` (see Variable Reference above). The topic slug is derived from the research question (e.g., `locomotion-params`, `ade-hot-reload`, `agent-memory-system`) and used in the TASK_ID.

| Artifact | Location |
|----------|----------|
| **MDTM Task File** | `${TASK_DIR}TASK-RESEARCH-<subject>-YYYYMMDD-HHMMSS.md` |
| Research notes | `${TASK_DIR}research/research-notes.md` |
| Codebase research files | `${TASK_DIR}research/[NN]-[aspect-name].md` |
| Web research files | `${TASK_DIR}research/web-[NN]-[topic].md` |
| Synthesis files | `${TASK_DIR}synthesis/synth-[NN]-[section-name].md` |
| Final research report | `${TASK_DIR}RESEARCH-REPORT-[descriptor].md` |
| Gap/question log (interim) | `${TASK_DIR}gaps-and-questions.md` |
| Analyst completeness report(s) | `${TASK_DIR}qa/analyst-completeness-report[-N].md` |
| QA research gate report(s) | `${TASK_DIR}qa/qa-research-gate-report[-N].md` |
| QA research qualitative report | `${TASK_DIR}qa/qa-research-qualitative-report.md` |
| Analyst synthesis review(s) | `${TASK_DIR}qa/analyst-synthesis-review[-N].md` |
| QA synthesis gate report(s) | `${TASK_DIR}qa/qa-synthesis-gate-report[-N].md` |
| QA synthesis qualitative report | `${TASK_DIR}qa/qa-synthesis-qualitative-report.md` |
| Lens QA reports (structural) | `${TASK_DIR}qa/qa-lens-[lens-name].md` |
| Lens QA reports (content) | `${TASK_DIR}qa/qa-lens-[lens-name].md` |
| Consolidated QA findings | `${TASK_DIR}qa/qa-consolidated-findings-phase{3,5,6}.md` |
| QA fix verification report | `${TASK_DIR}qa/qa-fix-verification.md` |
| Source fidelity report(s) | `${TASK_DIR}qa/qa-source-fidelity-report[-N].md` |
````

### src/superclaude/skills/tech-research/SKILL.md:479-492

````markdown
  - [ ] Spawn rf-analyst (completeness lens) — reads all research files, applies coverage audit + completeness + cross-reference checks from 8-item checklist. Writes to `${TASK_DIR}qa/analyst-completeness-report.md`. Embed full prompt per B2.
  - [ ] Spawn rf-analyst (cross-validation lens) — reads all research files, applies contradiction detection + gap compilation + depth assessment checks. Writes to `${TASK_DIR}qa/analyst-cross-validation-report.md`. Embed full prompt per B2.
  - [ ] Spawn rf-qa (evidence-quality lens) — reads all research files, applies file inventory + evidence density + scope coverage + doc cross-validation checks from 10-item checklist. Writes to `${TASK_DIR}qa/qa-research-evidence-report.md`. Embed full prompt per B2.
  - [ ] Spawn rf-qa (gap-detection lens) — reads all research files, applies gap severity + depth appropriateness + integration points + pattern documentation + incremental writing checks. Writes to `${TASK_DIR}qa/qa-research-gaps-report.md`. Embed full prompt per B2.
  - [ ] Spawn rf-qa-qualitative (research-depth lens) — reads all research files, evaluates whether findings are genuinely deep or superficial. Are key findings actionable or vague? Does analysis go beyond surface-level code reading? Writes to `${TASK_DIR}qa/qa-research-qualitative-report.md`. Embed full prompt per B2.
- **Parallel partitioning for large workloads:** When >6 research files exist, EACH of the 5 agent types above gets partitioned into multiple instances with `assigned_files` subsets. For example, with 10 research files: 2 completeness-analyst (5 files each) + 2 cross-validation-analyst + 2 evidence-qa + 2 gap-qa + 2 depth-qualitative = 10 parallel agents. Each writes to numbered reports. Merge after completion.

Step 3.2: Consolidate findings and apply fixes (SERIALIZED)
  - [ ] Read ALL reports from Step 3.1, consolidate into `${TASK_DIR}qa/qa-consolidated-findings-phase3.md`
  - [ ] Spawn rf-qa (fix agent, fix_authorization: true) with consolidated blocking findings (minor findings stay as notes). Fix agent spawns additional targeted research agents for blocking gaps requiring new research (one per gap). Applies all blocking fixes.
  - [ ] Spawn rf-qa (verification, fix_authorization: false) + rf-qa-qualitative (verification, fix_authorization: false) to confirm fixes applied correctly
  - [ ] If verification finds new blocking issues (new minor findings are notes and do not restart the cycle): repeat Step 3.2 (max 2 cycles total). After 2 fix cycles (3 reviews), HALT and escalate to the user with the open blocking findings; log issues in Task Log

- Compile final gaps into ${TASK_DIR}gaps-and-questions.md (merged from all reports)
````

## Coverage slice

| Row | Spec line | Quote | Containment match | By hand |
|---|---|---|---|---|
| INF-002 | source.md:11 | the sweep only records (`promote` off), the classifier has no authority | Task 4 (0.6) | Task 4 |
| INF-003 | source.md:11 | Stage 3 starts only after the owner reads this package's summary and says go | Task 8 (0.727) | Task 8 |
| INF-014 | source.md:27 | Every task that edited `src/superclaude/skills/task/SKILL.md` is dropped | none (0.5) | Constraints line 22 |
| INF-019 | source.md:30 | No new plugin surface. | Task 3 (0.667) | Constraints line 23 + Task 3 |
| INF-020 | source.md:30 | copied byte for byte in Task 3 | Task 3 (0.8) | Task 3 |
| INF-021 | source.md:31 | `follow-ups.md` stays a separate file; no mapping to `review-ledger/1`; `ledger.py` is not edited. | none (0.25) | Constraints line 24 |
| INF-022 | source.md:32 | No `/sc:implement` run, no commit, no push; `.dev/tasks` staged only. | none (0.375) | Constraints line 33 (staging); no task runs /sc:implement, commits or pushes |
| INF-023 | source.md:36 | New Task 2 builds `follow_ups_cmd.py` (group `follow-ups`: `write`, `safety`, `sweep`, `summary`) and registers it. | Task 2 (0.769) | Task 2 |
| INF-029 | source.md:42 | Task 7 names PF `04-historical/master-table.md`, PF `05-scoring/consensus.md`, `stage0b-sample.md`, `fresh-findings.md` and `stage0-heldout-ids.json`, and counts `@E2` rows separately | Task 7 (0.643) | Task 7 |
| INF-030 | source.md:42 | Task 1 checks that the ledger holds the stage 0 and stage 1 package ids. | Task 1 (0.818) | Task 1 |
| INF-034 | source.md:46 | Task 1 fixes arguments (ledgers, deliverables, kind) and counts skipped kinds. | Task 3 (0.6) | Task 1 |
