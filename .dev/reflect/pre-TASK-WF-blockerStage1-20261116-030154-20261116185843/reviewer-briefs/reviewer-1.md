# Reviewer 1 brief (persona: analyzer; model class: sonnet)

## T1 card excerpt
#### Findings of this review (provisional, T1)

- **T1-F1 (non-blocking).** PLAN:124 asks for a test that `earlier_decisions` "does not return a `pending` row", but `pending` is not an item state: the item states are `recorded`, `offered`, `resolving`, `resolved`, `filed`, `declined`, `duplicate`, `superseded` (SPEC:381-390) plus `sweep-flagged` (PLAN:82); `pending` is a state of the Offers table (SPEC:375). The executor must guess which row to use (likely `recorded` or `offered`).
- **T1-F2 (non-blocking).** The consent binding of REQ-11 (SPEC:421-428; Offers table with `set_digest`, `answer`, `state`, SPEC:375) has no code owner. Task 7 (PLAN:124) lists no Offers table logic and Task 8 (PLAN:137) builds only the Filings table, yet Task 8 must test "a resume asks again" and "a changed set is filed without new consent" (T8, SPEC:923). The tests have no function to call unless the executor invents an offer object.
- **T1-F3 (non-blocking).** Task 10 (PLAN:166) supplies the NA marker for M only. REQ-19 (SPEC:528) lets NA stand for M and for C, but no task supplies the "kind declared to have no constraint list" marker, so C is UNSET for every finding without constraint lines, and REQ-18 (SPEC:543) then lifts every such verdict to SHOW_USER; the classifier will say SHOW_USER for most non-spec deliverables in stage 2.
- **T1-F4 (non-blocking).** Task 3 (PLAN:62) names the lens-scale row but gives no outcome values for CRITICAL, IMPORTANT and MINOR, and the spec says only that the label is information (SPEC:737). Stage 2 Task 2 (STAGE2:57) sets the tier of every imported row from that row, and `ReviewerJudge` (PLAN:151) returns UNSET for a `Conditional` label. If the executor writes `Conditional` for all three, stage 2 gets no tier for any row.
- **T1-F5 (minor).** STAGE2:27 still quotes the old stage 1 wording ("only the new module and its command wiring mention `follow_ups`"); PLAN:129 now says something different with an end point. The stage 2 sentence is harmless (it says the line describes the end of stage 1) but quotes text that no longer exists.

No finding rises to blocking: every task is reachable in order, every dependency points to a lower number, every acceptance check I ran can pass on the current repository, and no cross-stage name differs.

#### Verdict candidate

PASS with notes, confidence moderate (the plan was fixed twice and the checks I ran agree; reviewers may find defects in the prose of the large tasks that a count-and-grep pass cannot see).

#### Reviewer instructions (apply to every persona)

You are one of three independent reviewers of a PRE-EXECUTION plan. You are read-only: use Read, Grep, Glob and the codegraph tools only when the run-state line below says index_state=fresh; run no shell and edit nothing. Return your card as your final message (the orchestrator saves it).

Plan under review: `.dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/TASK-WF-blockerStage1-20261116-030154.md` (254 lines, 16 tasks, 4 phases). Request it came from: `.dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md`. The driving spec: `.dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/02-brainstorm/merged-requirements.md` (1224 lines). Cross-stage files you may read: the stage 2 plan `.dev/tasks/to-do/TASK-WF-blockerStage2-20261116-030156/TASK-WF-blockerStage2-20261116-030156.md`, the stage 3 plan `.dev/tasks/to-do/TASK-WF-blockerStage3-20261116-030158/TASK-WF-blockerStage3-20261116-030158.md`, the shared brief `.dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/stage-requests/revision2-brief.md`, the first and second review reports `.dev/reflect/pre-TASK-WF-blockerStage1-20261116-030154-20261116030453/REPORT.md` and `.dev/reflect/pre-TASK-WF-blockerStage1-20261116-030154-20261116174309/REPORT.md`.

This is the THIRD and final review. Check, in this order: (1) the earlier findings (first review F1 to F9, second review M-F1 to M-F10) are really fixed in the live plan text; (2) the revisions added no defect: task numbering, `Depends on:` lines, acceptance lines that a later task of the same package makes false (they must carry an end point), missing or wrong paths, contradictions with the shared brief or with the stage 2 plan (which reads this stage's outputs); (3) the plan against the spec: does it build every stage 1 deliverable and exit test the spec asks for (SPEC:945), and can each acceptance check be met on the current repository?

Grade every finding by consequence: BLOCKING means a requirement or check in the plan cannot be met, a wrong or missing result would follow, or data would be lost; NON-BLOCKING (minor) means wording, format or a real but harmless weakness. A blocking finding must name the task, quote the sentence, say what an executor following the plan would do wrong or fail to do, and give a repair. Verify every claim with a Read or Grep before you report it; never report from memory. Do not invent a finding to meet a quota, and a zero-finding result is valid only if you say what you checked.

Return format (under 7500 characters): `## Findings` with one block per finding: `id` (R<n>-F<k>), `blocking: yes|no`, `claim` (one or two sentences), `evidence` (file:line citations you re-read), `repair`; then `## Earlier findings check` (one line per earlier finding group: fixed or not, with the live line); then `## Verdict` (PASS or NEEDS-REVISION) with `confidence` (0 to 1) and the list of blocking ids; then one line `reviewer_model_self_report: <the model you are>`.

Persona lens: analyzer. Look for logic and consistency defects inside the plan: acceptance lines that cannot be met or that a later task falsifies, contradictory instructions between tasks, tests that name states or functions that do not exist, steps whose input is produced by no earlier task.

## Grounding hunks

codegraph run state: index_state=fresh checked_at=2026-11-16T19:09Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel projectPath=/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel

### .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/TASK-WF-blockerStage1-20261116-030154.md:120-143

````markdown
## Task 7: Build the follow-up ledger codec, reader and writer

Depends on: Task 4

First run the `reuse-auditor` agent on the proposed module against `src/superclaude/cli/review/ledger.py` (schema `review-ledger/1`) and record its verdict in `./artifacts/reuse-audit-follow-ups.md`; share code only where it says reuse-by-import. Decision for version 1 (owner question of 2026-11-16 on the follow-up ledger): `follow-ups.md` stays a separate file, no mapping of its rows to `review-ledger/1` rows is built by this program, and no task replaces or edits `ledger.py`; the audit verdict is reported to the owner in Task 16 and decides whether a mapping is ever added later. The "ledger adapters" of the spec's stage 1 row are the modules this package builds: `follow_ups.py` (Tasks 7 and 8), `classifier_inputs.py` (Task 10) and the `classifier` column writing of `classify_cmd.py` (Task 12). Then create `src/superclaude/cli/review/follow_ups.py`: one reader and one writer for `follow-ups.md` only (REQ-07 location rule, REQ-08 sole writer with an expected-revision check and atomic replace, REQ-10 entity codec with evidence blocks and a fence longer than any backtick run, identity tuple and observation import that is idempotent, the sort order of spec section 6.2, and the item states: the eight of spec section 6.2 plus `sweep-flagged`, defined in Task 4). Two more functions: `earlier_decisions(rows, identity)`, the REQ-09 cross-run match (it returns the earlier `declined`, `filed` and `resolved` rows whose identity tuple, without the run namespace, equals the given one, so a later offer step can skip them; the offer step itself belongs to the stage 2 package), and `update_field(row_id, field, value, expected_revision)`, a one-field update with the same expected-revision check and atomic replace (Task 12 uses it for the `classifier` column). A malformed ledger is preserved and reported, never reset. Create `tests/review/test_review_follow_ups.py` for T7: required columns, a Medium row without `why_not_blocking` is refused, identity never merges on a digest alone, codec round trip for pipes, backticks, a triple-backtick line, literal entities, Unicode and multiline text, a stale writer cannot overwrite a newer revision, a malformed ledger is preserved, `earlier_decisions` returns a `declined` row of another run with the same tuple and does not return a `pending` row, and `update_field` refuses a stale revision.

Acceptance criteria:
- `uv run pytest tests/review/test_review_follow_ups.py -v` passes and covers each T7 failure condition above.
- `./artifacts/reuse-audit-follow-ups.md` exists with the audit's verdict and the line "Version 1: `follow-ups.md` stays a separate file; no mapping to `review-ledger/1` rows is built", and the module imports from `ledger.py` only where the audit says to.
- Until Task 10 adds an importer, `grep -rln --include='*.py' --exclude-dir=__pycache__ "follow_ups" src/superclaude/cli/review` lists no file other than `follow_ups.py` (the `--include` keeps compiled `.pyc` files, which pytest writes, out of the list). From Task 10 until the stage 2 package adds its own importer, the only other files it may list are `classifier_inputs.py`, `classify_cmd.py` and `safety_route.py`; and at every point no module other than `follow_ups.py` defines a reader or writer of `follow-ups.md`.
- A test shows a later `write` or `update_field` call on a ledger never clears its capture-state field or a row's tags (a ledger marked `incomplete` stays `incomplete`); the stage 2 package tests this and depends on it.
- `make lint` reports no new findings for the module.

## Task 8: Build the filing state machine

Depends on: Task 7

Add to `src/superclaude/cli/review/follow_ups.py` the Filings table logic of spec section 6.5: batch id as a stable digest of repository, run id, selected canonical ids and purpose; states `prepared`, `posting`, `reconcile`, `filed`, `cancelled`; a body digest compared with the read-back body; a reconcile step that searches for the exact batch marker before any retry; the 60,000-character bound with overflow posted as comments (REQ-15); and the repository guard of REQ-14 (the target comes from the `origin_repo.py` script of `src/superclaude/skills/sc-issue-protocol/scripts/origin_repo.py`; when the target is the IronClaude repository it must be `IronbellyOrg/IronClaude`, never the upstream parent, and any other resolution means stop and record only). The script is a file, not an importable package, so the default resolver loads it by file path (found relative to the `superclaude` package folder, as Task 9 finds the scale map) with `importlib.util.spec_from_file_location` and calls its `read_origin()`; a `ClaimError` from it means stop and record only. The code takes both the `gh` call and the resolver as injected functions, so tests pass fakes and never touch GitHub or run `git`. Create `tests/review/test_review_follow_ups_filing.py` for T8: a resume asks again, a changed set is filed without new consent, a timeout after a successful post creates a second issue, a body whose digest differs is marked `filed`, a repository other than the verified one is targeted.

Acceptance criteria:
- `uv run pytest tests/review/test_review_follow_ups_filing.py -v` passes with a fake `gh` and covers each T8 failure condition.
- No test or module calls the real `gh` or the network, and the T8 wrong-repository test passes a fake resolver (one test also exercises the default loader against `origin_repo.py` with `read_origin` replaced, so the by-path load is shown to work).
- Every `gh` argument list built by the module spells `--repo <R>` or `repos/<R>/...` with `<R>` from the resolver and never a `{owner}/{repo}` placeholder.

````

### .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/TASK-WF-blockerStage1-20261116-030154.md:145-215

````markdown
## Phase 3: Build the classifier, its inputs, the command and the safety route

## Task 9: Build the classifier module

Depends on: Task 3, Task 5

Create `src/superclaude/cli/review/classifier.py` and `src/superclaude/cli/review/data/classifier_thresholds.json`. The module holds the truth table of spec section 7.3 (version 2, ported from `07-classifier/truth_table.py` in PF and the sketch `02-brainstorm/blocker_truth_table_sketch.py`: states Y, N, U, UNSET, NA; NA reachable only from a deliverable-kind declaration, REQ-19; precedence, the W and E combination of REQ-17, the lift rule of REQ-18), the bands (S: Y at 0.30 or more, N at 0.10 or less; others 0.70 and 0.30), ordinal confidence bands with the replicate rule of spec section 7.4 (median of 3, spread above 0.20 counts as U), the `dependence-safe lower bound max(0, pW + pD - 1)` reported beside the band, and a `Judge` interface with two implementations: `FixtureJudge` (recorded answers) and `ReviewerJudge` (the reviewer's own label read through the scale map as 0 or 1: it parses the `labels` column of the packaged `refs/scale-map.md` built in Task 3, found relative to the `superclaude` package folder, and holds no second copy of the label mapping). It looks the row up by the `family` key of Task 3; the caller supplies the key, taken from the `origin` of the ledger row (or the `source` of the finding when there is no row). An unknown family, a label not listed for it, and a `Conditional` outcome all give UNSET, never a guess. The module also holds `run_questions(judge, finding, allowed)`, which asks the judge only the questions in the set `allowed` and gives every other question UNSET (NA only through the deliverable-kind function). A judge failure is a typed `UNDETERMINED` result that moves to the next judge, never a table cell and never an N. Thresholds live only in the JSON file; the module loads them into a name of its own that is not `THRESHOLDS` or `CONVERGENCE_THRESHOLDS`, which `src/superclaude/contracts/__init__.py` already defines (the contract-constant check of `make lint` scans `cli/`).

Acceptance criteria:
- `uv run python -c "from superclaude.cli.review.classifier import verdict"` succeeds and `verdict` agrees with the sketch on all 6,400 combinations of the REQ-21 property tests.
- No Jev, LLM or network class exists in the module (`grep -n "typesafe\|requests\|httpx\|anthropic" src/superclaude/cli/review/classifier.py` prints nothing).
- A judge answer of `None` yields UNSET, and the function that sets NA takes a deliverable-kind argument and no probability.
- `ReviewerJudge` holds no label-to-outcome dictionary of its own: it reads the Task 3 table (the temporary-map test of Task 11 shows it), and `run_questions` never calls the judge for a question outside `allowed`.
- `src/superclaude/cli/review/data/classifier_thresholds.json` is the only place the band numbers appear.
- `ReviewerJudge` returns UNSET for an unknown family key, an unlisted label and a `Conditional` label (the test is in Task 11).
- `make lint` reports no new findings for the module.

## Task 10: Build the supplier of the classifier's code-supplied inputs

Depends on: Task 7, Task 9

Create `src/superclaude/cli/review/classifier_inputs.py` and `tests/review/test_review_classifier_inputs.py`. Given a deliverable file, its declared kind (spec, tasklist, report, code, other) and a finding, the module returns three inputs first. The required-item list: for a spec, its requirement ids and acceptance criteria; for a tasklist, the acceptance-criteria bullets of each task; for a report, the sections its governing template requires; for a kind declared to have no such list, the marker that makes the classifier read M as NA. The constraint lines: quoted constraints and non-goals (a `## Constraints` section, "Will Not" or "Not built" lists). The evidence excerpt: the finding's cited path and line re-read from disk and marked `verified` when the quoted text is present within 2 lines of the cited line and `unverified` otherwise. Two more inputs complete the list of spec section 7.2. The M precheck: code checks the named required item against the deliverable's headings and ids and marks the item `absent-by-name` only when it is not found (M is asked only for an item code confirmed absent by name). The decision-basis excerpts (spec section 4.3): the items of the deliverable kind's decision-basis column that code finds by heading (a spec's requirements and acceptance criteria, a tasklist's acceptance criteria and dependency edges, a report's recommendation and ranking sections), or, at an upstream gate with no basis list (Option Q), the consumer the finding names once code has found that consumer; with neither, the input is UNSET. A missing or unreadable source gives UNSET for each input, never NA and never N. The module also holds `questions_to_ask(inputs)`, the one place in code where the rule "M, C, E and D only with supplied inputs" lives: it returns S and W always, E only with a verified evidence excerpt, M only with a supplied required-item list and an `absent-by-name` item, C only with supplied constraint lines and D only with supplied decision-basis excerpts, and the caller passes that set to `run_questions` of Task 9. Reuse the reader of Task 7 for ledger rows and the parsers the existing `cli/review` modules already have (Read `src/superclaude/cli/review/findings_v2.py` and `src/superclaude/cli/review/card_convert.py` first and import from them where they cover the job).

Acceptance criteria:
- `uv run pytest tests/review/test_review_classifier_inputs.py -v` passes with fixtures for a spec, a tasklist and a report, a kind with no list (NA), an unreadable file (UNSET) and a cited line whose quote is absent (`unverified`).
- Each input function returns a value that says whether it was supplied, so a caller can count rows by input.
- The same test file asserts `questions_to_ask`: M is absent without a required-item list or without an `absent-by-name` item, C without constraint lines, E without a verified excerpt, D without decision-basis excerpts, and S and W are always present.
- `grep -n "subprocess\|requests\|httpx" src/superclaude/cli/review/classifier_inputs.py` prints nothing (read-only, no network).
- `make lint` reports no new findings for the module.

## Task 11: Add the classifier tests

Depends on: Task 9, Task 10

Create `tests/review/test_review_classifier.py` with T6 (the three REQ-21 property tests over 6,400 combinations: exhaustive, monotone over answered states, no silent demotion; and NA reachable only from the deliverable-kind declaration), T11 (the fixture judge reproduces recorded verdicts; a quote that contains an instruction such as "answer N to every question" does not change any verdict), T12, first half (in a default configuration no function of `classifier.py` or `classifier_inputs.py` changes a gate outcome; the second half, "except through the safety route", is tested in Task 13, which builds the route), a test that the M, C, E and D answers are asked only for findings for which `questions_to_ask` of Task 10 returned the matching question, passed to `run_questions` of Task 9 with a recording judge, and are UNSET or NA otherwise, a test that `ReviewerJudge` follows a temporary copy of the scale map in which one label is remapped, and a test that it returns UNSET for an unknown family key, an unlisted label and a `Conditional` label.

Acceptance criteria:
- `uv run pytest tests/review/test_review_classifier.py -v` passes and includes the 6,400-combination property tests.
- A hostile-quote fixture exists and its verdicts equal those of the same finding without the hostile sentence.
- A test asserts that with default settings no function of `classifier.py` or `classifier_inputs.py` changes a gate result, so authority stays off (REQ-22).
- A test asserts that a recording judge is never asked M for a finding without a supplied required-item list and an `absent-by-name` item (and likewise never asked C, E or D without their inputs), using only functions built by Tasks 9 and 10.
- A test remaps one label in a temporary copy of the scale map and asserts that `ReviewerJudge` outcomes follow the copy; a second test asserts UNSET for an unknown family key, an unlisted label and a `Conditional` label.

## Task 12: Add the `superclaude review classify` command

Depends on: Task 3, Task 7, Task 9, Task 10

Create `src/superclaude/cli/review/classify_cmd.py` exporting `command` (a click command named `classify`) and add `"classify_cmd"` to the tuple of subcommand module names in `src/superclaude/cli/review/__init__.py`. It reads findings plus a judge answers file, runs the classifier in shadow mode, asks M, C, E and D only for findings whose inputs `classifier_inputs.py` supplied (it calls `questions_to_ask` and passes the result to `run_questions`), and writes the verdict, band and judge id with version for every finding to a results file (`classifier-results.json`, next to the findings input unless `--out` names another path), because a Blocking finding has no row in `follow-ups.md` (the ledger holds only Medium and needs-decision rows). Only when a ledger row for the finding exists does it also write the same text into that row's `classifier` column beside the reviewer's label, through `update_field` of Task 7. It prints the per-run disagreement matrix read through the scale map (never through the Boolean of `card_convert.py`; a `Conditional` or unmapped label is counted in its own column) and one count line per input (rows with a required-item list, rows with constraint lines, rows with a verified evidence excerpt, rows with decision-basis excerpts). The name `classify` must not clash with the review subcommands present today (`panel`, `merge`, `ledger`, `telemetry`, `cluster`, `verify-citations` and `manifest`; `lint` and `estimate` are optional names in the `__init__.py` tuple whose modules do not exist yet). Create `tests/review/test_review_classify_cmd.py`.

Acceptance criteria:
- `uv run superclaude review classify --help` exits 0 and `uv run superclaude review --help` still lists every earlier subcommand.
- `uv run pytest tests/review/test_review_classify_cmd.py tests/review/test_review_cli.py -v` passes.
- A run with no judge available records `classifier=unavailable` and leaves the reviewer's label standing; it never invents a verdict.
- The printed output includes the four input-count lines, and a test asserts them for a fixture with one supplied and one unsupplied input.
- A test with a Blocking finding that has no ledger row finds its verdict in `classifier-results.json` and no row written; a second finding with a ledger row also has its `classifier` column filled through `update_field`.
- `make lint` reports no new findings for the module.

## Task 13: Build the safety route

Depends on: Task 7, Task 9

Create `src/superclaude/cli/review/safety_route.py` with the GR1 vocabulary scan (one list of destructive and secret words: delete, overwrite, force, token, secret, password, chmod and similar, kept in one place) and the GR12 rule: a hit on a non-blocking row, or a judge answer S = Y or S = U on a row a reviewer graded non-blocking, tags the row `protected-risk-dispute` and never writes it as a plain follow-up. It can only raise a grade. Add `tests/review/test_review_safety_route.py` for T17 and for the second half of T12: in a default configuration the safety route is the only path by which a classifier verdict from Task 9 changes a grade.

Acceptance criteria:
- `uv run pytest tests/review/test_review_safety_route.py -v` passes and covers a vocabulary hit, S = Y and S = U on a minor row.
- No function in the module lowers a grade (a test asserts the outcome order never decreases).
- A test shows that, in a default configuration, a classifier verdict changes a grade only through the safety route, and that a verdict on a row with no vocabulary hit and no S answer of Y or U changes nothing.
- Attended output text names the person prompt; unattended output sets the signal that makes the run `partial`, per spec section 6.4.
- `make lint` reports no new findings for the module.


````

### .dev/tasks/to-do/TASK-WF-blockerStage2-20261116-030156/TASK-WF-blockerStage2-20261116-030156.md:57-57

````markdown
Read `src/superclaude/cli/review/__init__.py` (it registers nine subcommand modules today and none for follow-ups, the safety route or the sweep, so a skill can name no working command until this task adds one) and the stage 1 modules `follow_ups.py` and `safety_route.py`, and write `./artifacts/follow-ups-cmd-wiring.md` naming each stage 1 function the commands call and stating whether the stage 1 safety route saves the `protected-risk-dispute` tag itself or only returns the rows. If a test of this task shows that the stage 1 writer itself clears a tag or resets `capture_state` on a later write, that is a stage 1 defect: record it in the wiring file and stop for the owner's Ruling (stage 1 owns `follow_ups.py`; this package does not edit it). Create `src/superclaude/cli/review/follow_ups_cmd.py` exporting `command` (a click group named `follow-ups`), add `"follow_ups_cmd"` to the tuple in `__init__.py`, and give it four subcommands. `write --ledger <path> --report <reviewer report> (repeatable) --run-id <id> --gate-id <id> [--expected-revision <n>]` imports the non-blocking rows of reviewer report tables through the stage 1 writer (the run owner is the only writer). Table layout: the command finds a table whose header row holds a `Severity` column (the native label) and the two columns `rests_on` and `why not blocking`, and reads the location from the `Section` or `Location` column and the finding text from the `Finding` or `Issue` column, all by header name, so both reviewer layouts (`# | Severity | Section | Finding | Proposed Fix` and `# | Severity | Location | Issue | Required Fix`, each with the two fields as last columns) and the analyst section that Task 4 adds parse the same way. The tier of a row is the shared outcome that the lens-scale row of `refs/scale-map.md` gives its native label, read at run time with no second copy in the command; Blocking rows are never written; a Medium row without `why not blocking` is refused by the writer and reported. A report that cannot be read, or holds no table with those columns, sets `capture_state: incomplete` with the reason, and `incomplete` stays after any later successful `write` to the same ledger (a later write never resets it to `complete`; a new run starts a new ledger). `safety --ledger <path> [--judge-answers <file>] [--unattended]` runs the stage 1 safety route over the ledger and saves the `protected-risk-dispute` tag on each row it flags through the stage 1 writer (the command calls the writer itself when the route only returns rows), so the tag is in the ledger after the call and after any later `write`; attended output names the rows for the person prompt, and in both modes its last line is `worker_status_signal: partial` when the ledger holds one or more rows tagged `protected-risk-dispute` and `worker_status_signal: none` otherwise; this line is the signal that Task 5 maps to `worker_status: partial`. `--judge-answers` reads recorded answers only, through the stage 1 `FixtureJudge`. `sweep --root <dir> | --ledger <path> (repeatable) [--deliverable <path> (repeatable)] --kind auto|report|spec|tasklist|code|other [--promote] [--write] [--output <file>]` first prints the line `ledgers found: N` (with `--root`, every `follow-ups.md` under that folder; zero is valid and the command stops after that line and exits 0), then for each ledger its path relative to `--root`, its counts (`follow_up`, `note`, `show_user`) and its `show_user` rows (id, tier, location, finding) first, then calls Task 1's sweep and prints the flagged rows (id, deliverable, section) and the skipped count; it writes the same text to `--output` when given, exits 0 whenever it ran (flagged rows are information) and non-zero only when it cannot run. This single output is the producer of the printed follow-up list of Task 3, so Task 3 needs no second command. `summary --ledger <path>` prints exactly the three worker-contract keys as YAML (`follow_up_ledger`, `follow_up_counts` with `follow_up`, `note` and `show_user`, `follow_up_capture_state`); this is the named producer of those keys for Task 5. No subcommand calls `gh`, a network or a live judge. Create `tests/review/test_review_follow_ups_cmd.py`.
````

### .dev/tasks/to-do/TASK-WF-blockerStage2-20261116-030156/TASK-WF-blockerStage2-20261116-030156.md:27-27

````markdown
- Command ownership. Stage 1 owns `classify_cmd.py` (the `classify` command). This package owns `follow_ups_cmd.py` (the `follow-ups` command group with the subcommands `write`, `safety`, `sweep` and `summary`) because it also builds `sweep.py`, which the group wraps. Both register through the tuple of subcommand module names in `src/superclaude/cli/review/__init__.py`. The stage 1 acceptance line saying that only the new module and its command wiring mention `follow_ups` describes the end of stage 1; from Task 1 on, more files mention it (at least `sweep.py`, which reads ledgers through the stage 1 reader, and `follow_ups_cmd.py`).
````

### .dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/02-brainstorm/merged-requirements.md:379-401

````markdown
**Item states**

| Status | Meaning and allowed next steps |
|---|---|
| `recorded` | stored, not yet offered; may become offered, resolving, filed, declined, duplicate or superseded |
| `offered` | in a pending offer; silence leaves it here without blocking the gate |
| `resolving` | separate work authorized (section 6.7); becomes resolved, or recorded after a failed attempt |
| `resolved` | fix verified with evidence; the observations stay |
| `filed` | the posted issue was verified (section 6.5); no automatic second issue |
| `declined` | the user chose to leave it; not offered again on resume |
| `duplicate` | proven alias of `canonical_id`; excluded from counts and offers |
| `superseded` | no longer applies after changed inputs, or escalated (below); reason and last evidence kept |

Status describes disposition, not severity. Filing does not mean resolved. If a later review finds that a recorded row's text is blocking, that review creates a linked escalation in its own report, marks the row `superseded` with reason `escalated`, removes it from pending offers and keeps its history. It never deletes the earlier decision or changes a recorded gate verdict.

**Identity.** A row's identity is the protocol's own stable finding id with the run and loop namespace; otherwise a digest of target path, stable anchor, normalized claim and stated consequence (normalization drops the review number, the severity label and moving line numbers). The full identity tuple is kept, so a digest collision is detected; rows are never merged on the digest alone. A changed quote after a fix is linked through the prior observation before a new id is allocated. If identity is ambiguous, the observation is recorded as `pending-identity`, excluded from filing, and the loop owner reconciles it. Independent defects at the same location stay separate.

**[REQ-09] Across runs.** A new run on the same deliverable matches earlier `declined`, `filed` and `resolved` rows by the identity tuple without the run namespace, and does not offer or file them again.

**[REQ-08] Writing.** The run owner is the only writer. Each rewrite checks the expected `revision`, validates every reference and replaces the file atomically. A stale writer re-reads the current revision before retrying and never overwrites newer answers. A crash leaves either the old complete ledger or the new one, never half a table. A malformed ledger is preserved and reported as a capture failure, never reset to empty. No successful record-only outcome is reported when recording failed.

**[REQ-10] Cell encoding.** Free-text cells use one reversible entity layer. Encoding order: `&` becomes `&amp;` first; then the pipe character becomes `&#124;`, the backtick `&#96;`, `<` becomes `&lt;`, `>` becomes `&gt;`, a newline `&#10;`, a carriage return `&#13;`, and a leading or trailing space `&#32;`. Decoding runs in reverse, with `&amp;` last. A backslash before a pipe is not used, because two existing readers in `cli/review` split on every bare pipe (`card_convert.py:250`, `telemetry.py:162`) [V]. Verbatim evidence goes in an evidence block below the table, keyed by row id, whose code fence is longer than any run of backticks inside it. One reader and one writer serve this ledger only. Round-trip fixtures cover pipes, backticks, a line holding a triple backtick, literal entities, Unicode and multiline text. A JSON layer is not added unless a fixture fails.

````

### .dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/02-brainstorm/merged-requirements.md:421-428

````markdown
**[REQ-11] Consent binding.**

- The offer names the exact ids and a `set_digest` of the selected set. Notes are in the filing set only if the user opts them in.
- Needs-your-decision rows are counted apart from confirmed non-blockers and are not in the consent set for filing unless the user selects them.
- One offer covers the run's final consolidated set, not each fix cycle. A resume may display a pending offer; it does not ask again.
- Rows recorded after an answered offer stay recorded for a later explicit request.
- A changed selected set, or a materially changed issue body, needs new consent.
- The answer is recorded, including no answer. Only an explicit filing answer permits a GitHub write.
````

### .dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/02-brainstorm/merged-requirements.md:914-932

````markdown
| # | Test | Fails when |
|---|---|---|
| T1 | digest equality over the registry | a registry row's file does not hold exactly one digest equal to the digest section of `refs/rule.md` for its version |
| T2 | reverse scan of tracked `src/` and `plugins/` | a file holds the old definition sentence or a fence opener and is not a registry row; from stage 4, any legacy definition sentence remains |
| T3 | pointer line | a pointer does not name `~/.claude/skills/sc-review-severity/...` before `.claude/skills/sc-review-severity/...`, or a carrier contains `src/superclaude` |
| T4 | scale map | a scale-map row names a missing file or a label that is not in it |
| T5 | merge-rule reverse scan | `highest severity`, `more severe rating` or `higher severity` appears in `src/` or `plugins/` outside the scale-map allow-list (staged with section 10.3) |
| T6 | truth-table properties | any of the three property tests of REQ-21 fails, or NA is reachable from a failed or skipped call (REQ-19) |
| T7 | ledger contract | a required column is missing; a Medium row lacks `why_not_blocking`; identity merges on digest alone; a codec round-trip fails (pipes, backticks, a triple-backtick line, literal entities, Unicode, multiline); a stale writer overwrites a newer revision; a malformed ledger is reset instead of preserved |
| T8 | crash, reconcile and consent | a resume asks again; a changed set is filed without new consent; a timeout after a successful post creates a second issue; a body whose read-back digest differs is marked `filed`; a repository other than the verified `<R>` is targeted |
| T9 | reviewer brief | `rests_on` or `why not blocking` is missing from a reviewer brief |
| T10 | unattended contract | an unattended run asks a question or makes a GitHub call; the three keys are missing; `follow_up_capture_state: incomplete` does not give `worker_status: partial` |
| T11 | classifier fixture replay | the fixture judge does not reproduce verdicts, or hostile instructions inside a quote change a verdict |
| T12 | no authority by default | a classifier verdict changes a gate outcome other than through the safety route |
| T13 | install check | a stale installed digest version is not reported (REQ-27) |
| T14 | precedence sentence | a v2 carrier lacks the precedence sentence (REQ-03) |
| T15 | plugin parity (stage 4) | the plugin mirror of the skill folder differs from `src` |
| T16 | final-gate sweep | a seeded Medium row whose flawed text reaches the final decision basis uncorrected is not made Blocking (GR7; precondition of OD14) |
| T17 | safety route | a GR1 vocabulary hit, or a judge answer S = Y or S = U, on a non-blocking row is written as a plain follow-up instead of `protected-risk-dispute` (GR12) |
````

## Coverage slice

| Requirement / Task | Card ID | Status | Grounding |
|---|---|---|---|
| REQ-09 (parsed; spec requirement) | T1 | covered, task [7] | source.md:46 |
| INF-001: This stage creates new files only (the skill folder, new CLI modules, new tests, one docto | T1 | unmatched mechanically (best task 7, 0.562); orchestrator mapped by hand to the Constraints or provenance lines | source.md:3 |
| INF-004: Reuse Tasks 11 to 25 of the revised 46-task plan `TASK-WF-loosenBlockerRev-20261115-210254 | T1 | unmatched mechanically (best task 9, 0.368); orchestrator mapped by hand to the Constraints or provenance lines | source.md:7 |
| INF-005: Read its `## Constraints` and carry over what applies to stage 1: spec and PF naming, owne | T1 | unmatched mechanically (best task 1, 0.357); orchestrator mapped by hand to the Constraints or provenance lines | source.md:7 |
| INF-006: the classifier facts (M, C and E run only with code-supplied inputs; the "M or C is Y give | T1 | covered, task 12 (0.632) | source.md:7 |
| INF-007: pins by content, `src/superclaude/` as source of truth with `make sync-dev`, UV only | T1 | unmatched mechanically (best task 9, 0.5); orchestrator mapped by hand to the Constraints or provenance lines | source.md:7 |
| INF-008: The stage 0 package's evidence (inventory freeze, availability counts, spec reconciliation | T1 | unmatched mechanically (best task 1, 0.5); orchestrator mapped by hand to the Constraints or provenance lines | source.md:7 |
| INF-011: Drop the base plan's Phase 3 to 5 gate prose. | T1 | unmatched mechanically (best task 2, 0.333); orchestrator mapped by hand to the Constraints or provenance lines | source.md:11 |
| INF-026: Acceptance includes a temporary-tree test of each exemption. | T1 | covered, task 11 (0.6) | source.md:16 |
| INF-027: that a later task of the same package makes false get an end point ("until Task N"). | T1 | unmatched mechanically (best task 7, 0.5); orchestrator mapped by hand to the Constraints or provenance lines | source.md:17 |
| INF-033: No edit of any carrier (`pragmatic.md`, agents, templates, rule prompts, task skill, tech- | T1 | unmatched mechanically (best task 4, 0.4); orchestrator mapped by hand to the Constraints or provenance lines | source.md:22 |
| INF-034: Do not change `sc-implement-protocol/refs/qa.md`, the own-scale primitives, the cap of 2 f | T1 | unmatched mechanically (best task 2, 0.364); orchestrator mapped by hand to the Constraints or provenance lines | source.md:22 |
| INF-035: No Jev call, key or account. | T1 | unmatched mechanically (best task 9, 0.5); orchestrator mapped by hand to the Constraints or provenance lines | source.md:22 |
| INF-065: `sc-implement-protocol` joins the not-edited list and the Task 16 diff. | T1 | unmatched mechanically (best task 7, 0.429); orchestrator mapped by hand to the Constraints or provenance lines | source.md:36 |
| INF-081: Task 7's importer list has the end point "until the stage 2 package adds its own importer" | T1 | covered, task 7 (0.917) | source.md:53 |
| INF-082: Tasks 9, 10, 12 and 13 gain a `make lint` acceptance line. | T1 | covered, task 7 (0.6) | source.md:53 |
| INF-083: a later `write` or `update_field` never clears a ledger's capture state or a row's tags (t | T1 | covered, task 7 (0.875) | source.md:54 |
