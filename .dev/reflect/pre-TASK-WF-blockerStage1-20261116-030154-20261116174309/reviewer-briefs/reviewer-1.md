# Reviewer brief 1 (analyzer)

## T1 card excerpt

## Check (a): are the first-review findings really fixed in the live plan?

| First-review finding | Live plan evidence | State |
|---|---|---|
| F1 Task 7 grep line has no end point | PLAN:125 now reads "Until Task 10 adds an importer, `grep -rln "follow_ups" src/superclaude/cli/review` lists only `follow_ups.py`. From Task 10 on, the only other files it may list are `classifier_inputs.py`, `classify_cmd.py` and `safety_route.py`..."; the words "command wiring" are gone | text fixed; see new finding N1 (the grep itself) |
| F2 stoprule row has no in-repo defining file | PLAN:64 marks the row `installed-only`, names the two `~/.claude/` paths, exempts it from the exists line and T4 (PLAN:70, PLAN:223, PLAN:231); both installed files exist (batch c12) | fixed |
| F3 allow-list narrower than stage 3 scan | PLAN:66 and PLAN:73 list `cli/roadmap/remediate_parser.py` and `cli/pipeline/fmea_classifier.py` as `allowed`; both files hold the phrases (batch c09) | fixed |
| F4 ledger mapping decision | PLAN:120 records "Version 1: follow-ups.md stays a separate file ... no mapping to review-ledger/1 rows"; PLAN:22 adds ledger.py to not-built; PLAN:237 reports the verdict | fixed |
| F5 scale-map shape | PLAN:62 fixes columns, pair format, path root, `none`, `installed-only`; Tasks 9, 12, 15 depend on Task 3 (PLAN:144, 182, 221) | fixed |
| F6 Task 10 dependency | PLAN:157 `Depends on: Task 7, Task 9` | fixed |
| F7 Task 11 tests need later code | `run_questions` in Task 9 (PLAN:146), `questions_to_ask` in Task 10 (PLAN:159); safety-route half of T12 in Task 13 (PLAN:196); Task 13 depends on 7 and 9 (PLAN:194) | fixed |
| F8 nits | Task 2 grep uses the full path (PLAN:56); Task 12 names seven subcommands (PLAN:184) | fixed (nit: PLAN:184 says `verify`, the command is named `verify-citations` in `verify_cmd.py`) |
| F9 sweep-flagged | PLAN:81 defines it as a ninth state, no rollout stage named (PLAN:87) | fixed |

## Check (b): new defects introduced by the revision

Mechanical structure (batch d01 to d05): 16 "Acceptance criteria:" labels for 16 tasks; `Depends on` targets are all lower task numbers; no checkbox or numbered-list lines; no absolute paths or `.dev/tasks/to-do/` prefixes; no "never staged" wording.

N1 (candidate, blocking). PLAN:125 acceptance line "lists only `follow_ups.py`" cannot be met as written. `grep -rln` also lists binary files, and `src/superclaude/cli/review/__pycache__/` holds `*.cpython-311.pyc` and `*-pytest-9.2.0.pyc` for every module (batch c01 and d20: the same grep for "ledger" lists 10 `.pyc` files besides the 5 `.py` files). Task 7's first acceptance line runs pytest, which writes `follow_ups.cpython-311*.pyc`, and from Task 10 on the importers' `.pyc` files also contain the name. The check lists extra paths whatever the code does. (`.gitignore:2` ignores `__pycache__/`, so the fix is to restrict the grep to `*.py`.)

N2 (candidate, non-blocking). Task 9 (PLAN:146) makes `ReviewerJudge` read the reviewer's label "through the scale map" from the `labels` column of `refs/scale-map.md`, but the same word has different outcomes in different rows (tasklist Medium is Blocking, `card_convert.py` medium is Note, rf-qa MINOR, auggie Medium). The plan never says which family row a finding's label is read against (the ledger `source`/`origin` columns could key it); Task 12's disagreement matrix (PLAN:184) has the same gap. An implementer must invent the key.

N3 (candidate, non-blocking). Task 3 fixes one outcome per label (PLAN:62: Blocking, Medium, Note), but SPEC:739 gives spec-panel MAJOR as "Blocking only when it names a concrete wrong outcome, else Medium" and SPEC:738 maps `false-claim` more broadly than the rule; a single `LABEL=Outcome` pair cannot hold a conditional mapping.

N4 (candidate, non-blocking). REQ-09 (SPEC:396, cross-run matching of declined, filed and resolved rows) is not named in Task 7 (PLAN:120) or in any T7 failure condition, although the identity tuple is.

N5 (candidate, minor). Task 8 (PLAN:132) takes the repository from `origin_repo.py`, which is a script, not an importable package (`tests/issue_watch/test_origin_parity.py:3`; `cli/issue_watch/launch.py:206` copies its rules), and says nothing about how code calls it or how the tests fake it.

N6 (candidate, minor). Task 4 copies spec sections 6.1 to 6.7; SPEC:485 mentions `.dev/pr-monitor/`, which Task 5's folder-wide grep (PLAN:97) forbids; Task 4 comes first, so the executor must drop it from the copy. The first review dropped this as an executor-avoidable point.

## Grounding hunks

codegraph run state: index_state=fresh checked_at=2026-11-16T17:50:54Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel projectPath=/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel

### .dev/reflect/pre-TASK-WF-blockerStage1-20261116-030154-20261116174309/artifacts/wave1a-checks.md (orchestrator read-only check results; re-run what you rely on)

### .dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/02-brainstorm/merged-requirements.md (the merged spec the plan implements; read-only; the stage 1 row is SPEC:945; sections 6, 7, 9, 11.2 and 12 are the ones the plan builds)

### .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/TASK-WF-blockerStage1-20261116-030154.md:18-30

```text
18: 
19: - Spec: the merged spec `02-brainstorm/merged-requirements.md` inside the program folder `BLOCKER-CLASSIFICATION-PROGRAM-20261115` (found by that folder name under the repository's task folder). This plan calls that folder PF and the spec file the spec. Section numbers, requirement ids (REQ-nn), loop changes (L1 to L6), guardrails (GR1 to GR12), tests (T1 to T17) and owner decisions (OD1 to OD17) refer to the spec. PF also holds the 5-run results in `08-test/results.md`, the reconciliation in `09-plan-input.md` and the stage ledger and the five stage requests in `stage-requests/`. Evidence of earlier stages is read from their packages by package id (the ids are in the stage ledger), found by that folder name in the to-do or done subfolder of the repository task folder.
20: - One package, one stage. This is stage 1 of five packages (one plan per stage, the owner's decision of 2026-11-16). It creates new files only (the skill folder, new CLI modules, new tests, one doctor check) and edits no review-loop carrier (`pragmatic.md`, agents, templates, rule prompts, the task skill, tech-research, `sc-implement-protocol`, `WORKER-CONTRACT.md`); every registry `digest` row stays `legacy`. It runs only after the stage 0 package is done, the owner has read the stage 0 summary and said go in chat, and the go is recorded in the stage ledger (Task 1 checks that). Stage 2 starts only after the owner reads this package's summary and says go.
21: - Owner decisions use the spec's recommendations unless the owner changes them: OD1 skill folder `sc-review-severity`; OD2 once per run plus at any escalation halt; OD4 the classifier has no authority in version 1; OD9 reviewer-named consumer, code-checked where quotable; OD11 replace label-max merging at all 13 lines in 10 files, staged; OD12 yes; OD13 short Note rows; OD14 a finding with an unknown consumer keeps the reviewer's label (no deferral); OD15 consent-bound body file posted by the attended top-level session; OD16 option (b) at stage 3. OD3 (finding text leaving the machine), OD5 to OD8 and OD10 are not decided here and no task depends on a different answer.
22: - Not built here: any Jev or other external judge call, any TypeSafe account or key, a Jev or LLM judge class (they wait for OD3), any change to `src/superclaude/skills/sc-implement-protocol/refs/qa.md` (it keeps its own scale), any change to the own-scale primitives listed in spec section 9.3 as unchanged, code-assigned severity in `src/superclaude/cli/**/*.py` (for example `fmea_classifier.py` and `remediate_parser.py`, out of scope by spec section 10.3), the 35 percent score target, any change to the cap of 2 fix cycles, and any edit or replacement of `src/superclaude/cli/review/ledger.py`.
23: - Classifier facts that bind every classifier task: the 5-run test (stage 0 package, `stage0a-result.md`, from PF `08-test/results.md`) used a text-only stand-in judge and got agreement with the panel of 58.5 percent (Cohen's kappa 0.27), and the missing-item, constraint and contradiction questions (M, C, E) were at chance without code-supplied inputs. So M, C and E run only when code supplies the required-item list, the constraint lines and the verified evidence (the classifier-inputs supplier of stage 1), the "M or C is Y gives BLOCKING" row is never enabled for any gate, and confidence is reported as an ordinal band, never as a probability.
24: - Retired carriers (owner decision of 2026-11-16: `/sc:task` and task-builder are being retired). No task of this program edits `src/superclaude/skills/task/`, `src/superclaude/skills/task-builder/`, `src/superclaude/agents/rf-task-builder.md` or anything that exists only for those; they keep today's text until the retirement removes them. Task 3 lists them in the "Merge-rule allow-list" section as `exempt-by-retirement` (by path only), and that exemption ends when the retirement removes the file. Tests that exist only to pin those files are not re-pinned here; a test that pins both a retired and an active carrier is re-pinned for the active carrier's part only.
25: - Follow-up carrier. The end-of-run follow-up list is carried by the final review step of `/sc:implement`, which records and prints only. `refs/qa.md` of that skill is not edited (it keeps its own scale and its final summary "never asks the user anything"), and the once-per-run offer question stays with the top-level session through the output style and with the consent-bound filing path (OD15), so this program adds no question to `/sc:implement`. `tech-research` is an active workflow that writes the ledger and neither sweeps nor offers. Stage 1 edits none of these files.
26: - Plugin surface. IronClaude is installed from the Coder template or from a git clone plus `superclaude install`, not as a plugin, so this program creates no plugin surface: no `plugins/superclaude/skills/sc-review-severity/` mirror, no plugin parity test and no `canonical` registry row for a plugin path. The two existing hand-kept plugin twins (`plugins/superclaude/commands/spec-panel.md` and `plugins/superclaude/rules/prompts/document_review_loop_prompts.md`) are touched only where an existing test pins them and the active source carrier changes; this package touches neither. The owner has not confirmed removing plugin parity (the program's open-questions file, section 3.4); this is the plan author's reassessment.
27: - Pins are by content. An acceptance check that must survive a task's own edit quotes the sentence it protects; it does not name a line number, because the edit moves the line. Line numbers in a task body are where the text sits today and are re-read before editing. An acceptance line that a later task of this package makes false carries its end point ("until Task N").
28: - `src/superclaude/` is the source of truth. Edit there, then run `make sync-dev`; keep everything under the project `.claude/` folder out of `git add` (only `.claude/settings.json` is tracked). Installed primitives name installed paths (`~/.claude/skills/...`) first and project `.claude/...` second, never a `src/superclaude/` path.
29: - Python work uses UV only: `uv run pytest ...`, never `python -m` or bare `pip`.
30: - Task-owned evidence and generated outputs go under `./artifacts/` in this package. `.dev/tasks/` is always staged (`git add .dev/tasks`), packages and their `./artifacts/` included, and no document a task writes tells a reader to keep `.dev/tasks/` out of `git add`. Staging is not committing.
```

### .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/TASK-WF-blockerStage1-20261116-030154.md:58-75

```text
58: ## Task 3: Write the scale map
59: 
60: Depends on: Task 1
61: 
62: Create `src/superclaude/skills/sc-review-severity/refs/scale-map.md` with one row per family of spec section 9.3, in a single Markdown table whose columns are `family`, `defining file`, `labels`, `model` and `file kind`, because Tasks 9 and 12 read the table in code and the T4 test of Task 15 parses it. `labels` holds each native label with its shared outcome as `LABEL=Outcome` pairs separated by semicolons (outcomes: Blocking, Medium, Note), or the word `none` for a family with no native label. `model` is either "graded by the three conditions" or "keeps its own model because <reason>". `file kind` is `repo` or `installed-only`. For a `repo` row the `defining file` cell holds the path relative to the `src/superclaude/` folder, written without that prefix (for example `agents/rf-qa.md`), so the installed file never names a `src/superclaude/` path; for an `installed-only` row it holds the `~/.claude/...` path of a file that exists only in an installed copy. The rows are the 12 families of that table: the CRITICAL, IMPORTANT, MINOR lens scale (defining file `agents/rf-qa.md`, not the retired task skill); the `/sc:implement` `refs/qa.md` checklist; spec-panel; the stoprule rubric and `finding-grader`; the reflect deviation taxonomy; tasklist High, Medium, Low; roadmap validate; `card_convert.py`; findings-v1 and v2; `sc-auggie-review-protocol/SKILL.md:228`; the PR severity router and Auggie rubric; and the code-assigned family (`labels` is `none`; its defining files are `cli/roadmap/remediate_parser.py` and `cli/pipeline/fmea_classifier.py`).
63: 
64: The stoprule and `finding-grader` row has no defining file in the repository: the spec files both as installed-only (they exist under `~/.claude/` and not under `src/superclaude/`, and whether they ever move into `src/` is owner decision OD10, not decided here). That row is therefore marked `installed-only`, names `~/.claude/skills/sc-spec-panel-stoprule-protocol/refs/rubric.md` and `~/.claude/agents/finding-grader.md`, and is exempt from the exists-in-repository line below and from T4 (Task 15 repeats the exemption). It cites no `.dev/` path.
65: 
66: Include the sentence that a keep of a fixed FAIL trigger (L6) is recorded here, and a section "Merge-rule allow-list" with one bullet per file: the path relative to `src/superclaude/` in backticks, then `allowed` or `exempt-by-retirement`. It lists by path only the files allowed to contain the three merge-rule phrases of spec section 10.3, and never writes those phrases or the old definition sentence, so the stage 3 scan test reads its allow-list from one place. The `allowed` entries are the auggie file (`skills/sc-auggie-review-protocol/SKILL.md`), `skills/sc-review-severity/refs/rule.md`, the six stage 4 files (`skills/tech-reference/SKILL.md`, `skills/readme/SKILL.md`, `skills/tdd/refs/build-request-template.md`, `skills/operational-guide/SKILL.md`, `templates/documents/agent_template_qa.md`, `templates/documents/agent_template_analysis.md`) and the two code files that hold the phrases and are not changed because they assign severity in code (`cli/roadmap/remediate_parser.py` and `cli/pipeline/fmea_classifier.py`, out of scope by spec section 10.3). The `exempt-by-retirement` entries are the retired carriers `skills/task/SKILL.md`, `skills/task-builder/` (every file in the folder) and `agents/rf-task-builder.md`, with the sentence that the exemption ends when the retirement removes the file. No plugin path is listed: no plugin mirror of this skill folder is made by any package.
67: 
68: Acceptance criteria:
69: - `refs/scale-map.md` has a row for each of the 12 families with the five columns above, and each `repo` row names a defining file that exists in the repository under `src/superclaude/`.
70: - The stoprule and `finding-grader` row is marked `installed-only`, names the two `~/.claude/` paths, and is exempt from the exists-in-repository line above and from T4; the code-assigned row has `labels` equal to `none`.
71: - The tasklist row states that Medium is blocking today on 7 lines of `skills/sc-tasklist-protocol/SKILL.md` and that no stage 1 to 4 task changes it.
72: - The `card_convert.py` row states that its word translator maps `important` and `medium` to non-blocking while `agents/rf-qa.md` treats IMPORTANT as blocking.
73: - The "Merge-rule allow-list" section exists and lists the auggie file, `refs/rule.md`, the six stage 4 files, `cli/roadmap/remediate_parser.py` and `cli/pipeline/fmea_classifier.py` as `allowed`, and `skills/task/SKILL.md`, `skills/task-builder/` and `agents/rf-task-builder.md` as `exempt-by-retirement` with the sentence that the exemption ends when the retirement removes the file; the plugin mirror is not listed.
74: - `grep -n "src/superclaude" src/superclaude/skills/sc-review-severity/refs/scale-map.md` prints nothing.
75: - `grep -n -i "highest severity\|more severe rating\|higher severity" src/superclaude/skills/sc-review-severity/refs/scale-map.md` prints nothing.
```

### .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/TASK-WF-blockerStage1-20261116-030154.md:116-126

```text
116: ## Task 7: Build the follow-up ledger codec, reader and writer
117: 
118: Depends on: Task 4
119: 
120: First run the `reuse-auditor` agent on the proposed module against `src/superclaude/cli/review/ledger.py` (schema `review-ledger/1`) and record its verdict in `./artifacts/reuse-audit-follow-ups.md`; share code only where it says reuse-by-import. Decision for version 1 (owner question of 2026-11-16 on the follow-up ledger): `follow-ups.md` stays a separate file, no mapping of its rows to `review-ledger/1` rows is built by this program, and no task replaces or edits `ledger.py`; the audit verdict is reported to the owner in Task 16 and decides whether a mapping is ever added later. The "ledger adapters" of the spec's stage 1 row are the modules this package builds: `follow_ups.py` (Tasks 7 and 8), `classifier_inputs.py` (Task 10) and the `classifier` column writing of `classify_cmd.py` (Task 12). Then create `src/superclaude/cli/review/follow_ups.py`: one reader and one writer for `follow-ups.md` only (REQ-07 location rule, REQ-08 sole writer with an expected-revision check and atomic replace, REQ-10 entity codec with evidence blocks and a fence longer than any backtick run, identity tuple and observation import that is idempotent, the sort order of spec section 6.2, and the item states: the eight of spec section 6.2 plus `sweep-flagged`, defined in Task 4). A malformed ledger is preserved and reported, never reset. Create `tests/review/test_review_follow_ups.py` for T7: required columns, a Medium row without `why_not_blocking` is refused, identity never merges on a digest alone, codec round trip for pipes, backticks, a triple-backtick line, literal entities, Unicode and multiline text, a stale writer cannot overwrite a newer revision, a malformed ledger is preserved.
121: 
122: Acceptance criteria:
123: - `uv run pytest tests/review/test_review_follow_ups.py -v` passes and covers each T7 failure condition above.
124: - `./artifacts/reuse-audit-follow-ups.md` exists with the audit's verdict and the line "Version 1: `follow-ups.md` stays a separate file; no mapping to `review-ledger/1` rows is built", and the module imports from `ledger.py` only where the audit says to.
125: - Until Task 10 adds an importer, `grep -rln "follow_ups" src/superclaude/cli/review` lists only `follow_ups.py`. From Task 10 on, the only other files it may list are `classifier_inputs.py`, `classify_cmd.py` and `safety_route.py`, and no module other than `follow_ups.py` defines a reader or writer of `follow-ups.md`.
126: - `make lint` reports no new findings for the module.
```

### .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/TASK-WF-blockerStage1-20261116-030154.md:128-137

```text
128: ## Task 8: Build the filing state machine
129: 
130: Depends on: Task 7
131: 
132: Add to `src/superclaude/cli/review/follow_ups.py` the Filings table logic of spec section 6.5: batch id as a stable digest of repository, run id, selected canonical ids and purpose; states `prepared`, `posting`, `reconcile`, `filed`, `cancelled`; a body digest compared with the read-back body; a reconcile step that searches for the exact batch marker before any retry; the 60,000-character bound with overflow posted as comments (REQ-15); and the repository guard of REQ-14 (the target comes from the `origin_repo.py` script of `src/superclaude/skills/sc-issue-protocol/scripts/origin_repo.py`; when the target is the IronClaude repository it must be `IronbellyOrg/IronClaude`, never the upstream parent, and any other resolution means stop and record only). The code takes the `gh` call as an injected function so tests never touch GitHub. Create `tests/review/test_review_follow_ups_filing.py` for T8: a resume asks again, a changed set is filed without new consent, a timeout after a successful post creates a second issue, a body whose digest differs is marked `filed`, a repository other than the verified one is targeted.
133: 
134: Acceptance criteria:
135: - `uv run pytest tests/review/test_review_follow_ups_filing.py -v` passes with a fake `gh` and covers each T8 failure condition.
136: - No test or module calls the real `gh` or the network.
137: - Every `gh` argument list built by the module spells `--repo <R>` or `repos/<R>/...` with `<R>` from the resolver and never a `{owner}/{repo}` placeholder.
```

### .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/TASK-WF-blockerStage1-20261116-030154.md:142-153

```text
142: ## Task 9: Build the classifier module
143: 
144: Depends on: Task 3, Task 5
145: 
146: Create `src/superclaude/cli/review/classifier.py` and `src/superclaude/cli/review/data/classifier_thresholds.json`. The module holds the truth table of spec section 7.3 (version 2, ported from `07-classifier/truth_table.py` in PF and the sketch `02-brainstorm/blocker_truth_table_sketch.py`: states Y, N, U, UNSET, NA; NA reachable only from a deliverable-kind declaration, REQ-19; precedence, the W and E combination of REQ-17, the lift rule of REQ-18), the bands (S: Y at 0.30 or more, N at 0.10 or less; others 0.70 and 0.30), ordinal confidence bands with the replicate rule of spec section 7.4 (median of 3, spread above 0.20 counts as U), the `dependence-safe lower bound max(0, pW + pD - 1)` reported beside the band, and a `Judge` interface with two implementations: `FixtureJudge` (recorded answers) and `ReviewerJudge` (the reviewer's own label read through the scale map as 0 or 1: it parses the `labels` column of the packaged `refs/scale-map.md` built in Task 3, found relative to the `superclaude` package folder, and holds no second copy of the label mapping). The module also holds `run_questions(judge, finding, allowed)`, which asks the judge only the questions in the set `allowed` and gives every other question UNSET (NA only through the deliverable-kind function). A judge failure is a typed `UNDETERMINED` result that moves to the next judge, never a table cell and never an N. Thresholds live only in the JSON file.
147: 
148: Acceptance criteria:
149: - `uv run python -c "from superclaude.cli.review.classifier import verdict"` succeeds and `verdict` agrees with the sketch on all 6,400 combinations of the REQ-21 property tests.
150: - No Jev, LLM or network class exists in the module (`grep -n "typesafe\|requests\|httpx\|anthropic" src/superclaude/cli/review/classifier.py` prints nothing).
151: - A judge answer of `None` yields UNSET, and the function that sets NA takes a deliverable-kind argument and no probability.
152: - `ReviewerJudge` holds no label-to-outcome dictionary of its own: it reads the Task 3 table (the temporary-map test of Task 11 shows it), and `run_questions` never calls the judge for a question outside `allowed`.
153: - `src/superclaude/cli/review/data/classifier_thresholds.json` is the only place the band numbers appear.
```

### .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/TASK-WF-blockerStage1-20261116-030154.md:155-165

```text
155: ## Task 10: Build the supplier of the classifier's code-supplied inputs
156: 
157: Depends on: Task 7, Task 9
158: 
159: Create `src/superclaude/cli/review/classifier_inputs.py` and `tests/review/test_review_classifier_inputs.py`. Given a deliverable file, its declared kind (spec, tasklist, report, code, other) and a finding, the module returns three things. The required-item list: for a spec, its requirement ids and acceptance criteria; for a tasklist, the acceptance-criteria bullets of each task; for a report, the sections its governing template requires; for a kind declared to have no such list, the marker that makes the classifier read M as NA. The constraint lines: quoted constraints and non-goals (a `## Constraints` section, "Will Not" or "Not built" lists). The evidence excerpt: the finding's cited path and line re-read from disk and marked `verified` when the quoted text is present within 2 lines of the cited line and `unverified` otherwise. A missing or unreadable source gives UNSET for that input, never NA and never N. The module also holds `questions_to_ask(inputs)`, the one place in code where the rule "M, C and E only with supplied inputs" lives: it returns S, W and D always, E only with a verified evidence excerpt, M only with a supplied required-item list and C only with supplied constraint lines, and the caller passes that set to `run_questions` of Task 9. Reuse the reader of Task 7 for ledger rows and the parsers the existing `cli/review` modules already have (Read `src/superclaude/cli/review/findings_v2.py` and `src/superclaude/cli/review/card_convert.py` first and import from them where they cover the job).
160: 
161: Acceptance criteria:
162: - `uv run pytest tests/review/test_review_classifier_inputs.py -v` passes with fixtures for a spec, a tasklist and a report, a kind with no list (NA), an unreadable file (UNSET) and a cited line whose quote is absent (`unverified`).
163: - Each input function returns a value that says whether it was supplied, so a caller can count rows by input.
164: - The same test file asserts `questions_to_ask`: M is absent without a required-item list, C without constraint lines, E without a verified excerpt, and S, W and D are always present.
165: - `grep -n "subprocess\|requests\|httpx" src/superclaude/cli/review/classifier_inputs.py` prints nothing (read-only, no network).
```

### .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/TASK-WF-blockerStage1-20261116-030154.md:180-190

```text
180: ## Task 12: Add the `superclaude review classify` command
181: 
182: Depends on: Task 3, Task 7, Task 9, Task 10
183: 
184: Create `src/superclaude/cli/review/classify_cmd.py` exporting `command` (a click command named `classify`) and add `"classify_cmd"` to the tuple of subcommand module names in `src/superclaude/cli/review/__init__.py`. It reads findings plus a judge answers file, runs the classifier in shadow mode, asks M, C and E only for findings whose inputs `classifier_inputs.py` supplied (it calls `questions_to_ask` and passes the result to `run_questions`), writes the verdict, band and judge id with version into the ledger row's `classifier` column beside the reviewer's label, and prints the per-run disagreement matrix read through the scale map (never through the Boolean of `card_convert.py`) and one count line per input (rows with a required-item list, rows with constraint lines, rows with a verified evidence excerpt). The name `classify` must not clash with the review subcommands present today (`panel`, `merge`, `ledger`, `telemetry`, `cluster`, `verify` and `manifest`; `lint` and `estimate` are optional names in the `__init__.py` tuple whose modules do not exist yet). Create `tests/review/test_review_classify_cmd.py`.
185: 
186: Acceptance criteria:
187: - `uv run superclaude review classify --help` exits 0 and `uv run superclaude review --help` still lists every earlier subcommand.
188: - `uv run pytest tests/review/test_review_classify_cmd.py tests/review/test_review_cli.py -v` passes.
189: - A run with no judge available records `classifier=unavailable` and leaves the reviewer's label standing; it never invents a verdict.
190: - The printed output includes the three input-count lines, and a test asserts them for a fixture with one supplied and one unsupplied input.
```

### .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/TASK-WF-blockerStage1-20261116-030154.md:192-202

```text
192: ## Task 13: Build the safety route
193: 
194: Depends on: Task 7, Task 9
195: 
196: Create `src/superclaude/cli/review/safety_route.py` with the GR1 vocabulary scan (one list of destructive and secret words: delete, overwrite, force, token, secret, password, chmod and similar, kept in one place) and the GR12 rule: a hit on a non-blocking row, or a judge answer S = Y or S = U on a row a reviewer graded non-blocking, tags the row `protected-risk-dispute` and never writes it as a plain follow-up. It can only raise a grade. Add `tests/review/test_review_safety_route.py` for T17 and for the second half of T12: in a default configuration the safety route is the only path by which a classifier verdict from Task 9 changes a grade.
197: 
198: Acceptance criteria:
199: - `uv run pytest tests/review/test_review_safety_route.py -v` passes and covers a vocabulary hit, S = Y and S = U on a minor row.
200: - No function in the module lowers a grade (a test asserts the outcome order never decreases).
201: - A test shows that, in a default configuration, a classifier verdict changes a grade only through the safety route, and that a verdict on a row with no vocabulary hit and no S answer of Y or U changes nothing.
202: - Attended output text names the person prompt; unattended output sets the signal that makes the run `partial`, per spec section 6.4.
```

### .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md:24-38

```text
24: ## Revision 2 (2026-11-16)
25: 
26: Applied to the plan in place (plan file name, slug and frontmatter unchanged; still 16 tasks, 4 phases). Sources: the pre-execution review `REPORT.md` of the stage 1 plan (findings F1 to F9, recommendations R-001 to R-007) and `revision2-brief.md` (shared decisions 1, 4, 5 and the follow-up carrier decision 2). This section supersedes the older lines above where they differ: the Task 13 line about "the plugin mirror is added in stage 4", and the Task 13 allow-list content.
27: 
28: - **F1, R-001 (blocking, applied).** Task 7: the line "shows only the new module and its command wiring" is replaced. It now reads: until Task 10 adds an importer, `grep -rln "follow_ups" src/superclaude/cli/review` lists only `follow_ups.py`; from Task 10 on the only other files it may list are `classifier_inputs.py`, `classify_cmd.py` and `safety_route.py`. The words "its command wiring" are gone (no task wires a command for `follow_ups`).
29: - **F2, R-002 option (a) (blocking, applied).** Task 3: the stoprule and `finding-grader` row is marked `installed-only`, names `~/.claude/skills/sc-spec-panel-stoprule-protocol/refs/rubric.md` and `~/.claude/agents/finding-grader.md`, cites no `.dev/` path, and is exempt from the exists-in-repository line; Task 15's T4 carries the same exemption (OD10 stays undecided). Checked: neither file exists under `src/` or `plugins/`; both exist installed.
30: - **F3, R-003 (applied).** Task 3's allow-list section also lists `cli/roadmap/remediate_parser.py` and `cli/pipeline/fmea_classifier.py` as `allowed` (they hold the phrases and are not changed). `stage3-request.md` line 14 repeated the old list and would have contradicted the plan, so it was edited the same way.
31: - **F4, R-004 and decision 5 (applied).** Task 7 records: `follow-ups.md` stays a separate file, no mapping to `review-ledger/1` rows, `ledger.py` untouched, the audit verdict decides whether a mapping is ever added; the "ledger adapters" are `follow_ups.py`, `classifier_inputs.py` and the classifier column writing of `classify_cmd.py`. Task 16 reports the audit verdict to the owner. `ledger.py` is added to the not-built list.
32: - **F5, R-005 (applied).** Task 3 fixes the table columns (`family`, `defining file`, `labels`, `model`, `file kind`), the `LABEL=Outcome;` pair format, the path root (relative to `src/superclaude/`, no prefix), the `none` value for a row without a native label (skipped by T4's label check) and `installed-only` rows. Tasks 9, 12 and 15 gain `Depends on: Task 3`.
33: - **F6, F7, R-006 (applied).** Task 10 depends on Task 7 and Task 9. `run_questions(judge, finding, allowed)` is assigned to Task 9 and `questions_to_ask(inputs)` to Task 10, so Task 11's M, C and E test uses only functions of Tasks 9 and 10. The second half of T12 ("except through the safety route") moves to Task 13, which now depends on Task 9 as well.
34: - **F8, F9, R-007 (applied).** Task 2's grep uses the full path; Task 12 names the seven review subcommands present today and says `lint` and `estimate` are optional names without modules; Task 4 defines `sweep-flagged` as a ninth state (the spec has eight; it comes from the stage 2 package's sweep) and the installed reference names no rollout stage.
35: - **Decision 1, retired carriers (applied).** New Constraints bullet; Task 3 lists `skills/task/SKILL.md`, `skills/task-builder/` and `agents/rf-task-builder.md` as `exempt-by-retirement` (path only) with the sentence that the exemption ends when the retirement removes the file; Task 6's note on `skills/task/SKILL.md` (no registry row) was re-read and made consistent; Task 16's carrier diff adds the task-builder folder. Of the 13 files that hold a merge-rule phrase today, only `skills/task/SKILL.md` is a retired carrier.
36: - **Decision 2, follow-up carrier (applied to stage 1 text).** New Constraints bullet and Task 4 wording: `/sc:implement`'s final review step records and prints only, the offer stays with the top-level session and the consent-bound filing path (OD15), `tech-research` writes the ledger and neither sweeps nor offers; `sc-implement-protocol` joins the not-edited list and the Task 16 diff.
37: - **Decision 4, no plugin surface (applied).** New Constraints bullet; Task 3 no longer says a plugin mirror comes in stage 4; Task 6's canonical row has no plugin surface (the word `plugin` stays only on the two pointer-only rows whose hand-kept twins exist); Task 15's T2 note says why `plugins/` is still scanned; Task 16 diff adds `plugins`. Registry counts unchanged: 11 `digest`, 1 `canonical`, 2 `pointer-only`, 5 `installed-only` (19 rows).
38: - **Gate wording (found while running the gate check).** Task 10's body quoted the "acceptance criteria" label with a colon, which broke the one-label-per-task rule; reworded. Two Constraints lines used the phrase the gate rejects for `git add`; reworded to "keep ... out of `git add`".
```

### .dev/reflect/pre-TASK-WF-blockerStage1-20261116-030154-20261116030453/REPORT.md:64-78

```text
64: ## Findings
65: 
66: Full text with all citations: `adversarial/merged-review-card.md`. Severity follows the rule in the reviewer briefs: blocking means an executor following the plan as written cannot meet a stated requirement or acceptance check, would produce a wrong or missing result, or data loss; minor means wording or format.
67: 
68: | # | Blocking | Finding |
69: |---|---|---|
70: | F1 | yes | Task 7's grep line (PLAN:115) is false once Tasks 10 and 12 reuse the ledger code (PLAN:148, PLAN:171) and has no "until Task N" end point, which the plan (PLAN:24), the source request (source.md:17) and the stage ledger (README.md:33) require. |
71: | F2 | yes | The stoprule/`finding-grader` scale-map row has no defining file in the repository: Task 3 (PLAN:62) and T4 (PLAN:209) need one, Task 5 (PLAN:87) forbids the only tracked copies (`.dev/experiments/`), and OD10 is undecided. |
72: | F3 | no | Task 3's merge-rule allow-list (PLAN:65) is narrower than the stage 3 scan: `remediate_parser.py` and `fmea_classifier.py` hold the phrases and are not listed (stage3-request.md:14). Inherited from the request; shows at stage 3. |
73: | F4 | no | No task records a decision on the `review-ledger/1` mapping (SPEC:404) or the "ledger adapters" of the stage 1 row (SPEC:945). Dissent: reviewer 2 graded it blocking. |
74: | F5 | no | The scale-map table layout, path root and label-less rows are not fixed, and Tasks 9 and 12 do not depend on Task 3, although code and T4 read the table. |
75: | F6 | no | Task 10 declares `Depends on: Task 9` only while reusing Task 7's reader. |
76: | F7 | no | Task 11's two tests need code that the plan describes under Tasks 12 and 13 (single-source probe finding). |
77: | F8 | no | PLAN:53 names a path that does not exist from the repository root (the grep passes vacuously); PLAN:171 lists `lint` and `estimate` as existing review subcommands although their modules do not exist. |
78: | F9 | no | `sweep-flagged` is an item state in Tasks 4 and 7 but not in the spec's item-state table (T1 card only, not debated). |
```

## Coverage slice

| Requirement | Source | Best task (mechanical) | Ratio | Method |
|---|---|---|---|---|
| INF-035 | source.md:26 | 1 | 0.231 | none |
| INF-036 | source.md:26 | 3 | 0.571 | none |
| INF-037 | source.md:28 | 7 | 1.0 | containment |
| INF-038 | source.md:28 | 7 | 1.0 | containment |
| INF-039 | source.md:28 | 7 | 0.5 | none |
| INF-040 | source.md:29 | 3 | 1.0 | containment |
| INF-041 | source.md:29 | 3 | 1.0 | containment |
| INF-042 | source.md:29 | 3 | 0.556 | none |
| INF-043 | source.md:30 | 3 | 0.917 | containment |
| INF-044 | source.md:31 | 7 | 0.889 | containment |
| INF-045 | source.md:31 | 7 | 0.875 | containment |
| INF-046 | source.md:31 | 7 | 0.833 | containment |
| INF-047 | source.md:31 | 7 | 0.5 | none |
| INF-048 | source.md:32 | 3 | 0.8 | containment |
| INF-049 | source.md:32 | 15 | 0.833 | containment |
| INF-050 | source.md:32 | 3 | 0.714 | containment |
| INF-051 | source.md:33 | 7 | 0.833 | containment |
| INF-052 | source.md:33 | 11 | 0.778 | containment |
| INF-053 | source.md:33 | 11 | 0.786 | containment |
| INF-054 | source.md:34 | 2 | 0.6 | containment |
| INF-055 | source.md:34 | 12 | 0.733 | containment |
| INF-056 | source.md:34 | 4 | 0.938 | containment |
| INF-057 | source.md:35 | 3 | 1.0 | containment |
| INF-058 | source.md:35 | 3 | 1.0 | containment |
| INF-059 | source.md:35 | 7 | 0.429 | none |
| INF-060 | source.md:36 | 4 | 0.938 | containment |
| INF-061 | source.md:36 | 4 | 1.0 | containment |
| INF-062 | source.md:36 | 7 | 0.429 | none |
| INF-063 | source.md:37 | 3 | 0.571 | none |
| INF-064 | source.md:37 | 6 | 0.867 | containment |
| INF-065 | source.md:37 | 15 | 0.444 | none |
| INF-066 | source.md:37 | 7 | 0.6 | containment |
| INF-067 | source.md:37 | 6 | 0.8 | containment |
| INF-068 | source.md:38 | 1 | 0.333 | none |

Persona instructions: Your lens: root-cause analysis of each first-review finding and of every defect the revision may have introduced. For each of F1 to F9 say fixed or not fixed in the LIVE plan with a plan line; then hunt for new defects (broken task numbering or dependencies, acceptance lines a later task of this package makes false with no end point, paths that do not exist, contradictions with the brief's decisions).
