---
schema: workflow-plan/1.2
source: ./source.md
strategy: systematic
depth: standard
slug: TASK-WF-createQuestionEv-20261126-170236
version: "1"
priority: Medium
created_date: "2026-11-26"
---

# Notes-contract tests and controlled-run evidence for the /sc:issue --create question rule (issue 834)

Source: ./source.md
Goal: Close what pull request 852 left open on issue 834: notes-contract tests that count the questions the shipped rule asks for each notes scenario, and recorded quick, standard and deep create runs with the actual question and post counts, all with GitHub writes blocked, plus a criterion-by-criterion verdict that cites file and line and says plainly which criteria are only partly evidenced.

## Constraints

- Pull request 852 already delivered the rule text (`src/superclaude/skills/sc-issue-protocol/refs/create.md:84-86`), the notes template (`src/superclaude/skills/sc-issue-protocol/templates/draft-notes.md`), the worker guidance, the command and docs text, and the static wording tests (`tests/skills/test_issue_protocol.py:1335-1526`). Do not redo or reword any of them. Keep every existing test as it is. Nothing under `src/superclaude/` changes and no production decision code is added (R-024).
- The secret-material exception (`src/superclaude/skills/sc-issue-protocol/refs/create.md:59` and `src/superclaude/skills/sc-issue-protocol/templates/draft-notes.md:13`) is deliberate: a would-be secret is listed under Contradictions and causes the one question. It is covered by a fixture test only and has no controlled run. Record it as a qualification in every verdict it touches; never remove it (R-009).
- The notes-contract tests of Phase 1 check the shipped template and rule text as written. They do not prove that a model follows the rule, and no verdict may say they do (R-002).
- No live test issues and no GitHub writes of any kind (R-003). The `gh` binary is not the only write path, so every run also blocks the others: an isolated home and configuration directory outside the package, no GitHub-capable MCP server, no credential helper, a non-pushable remote, and a read-only after-run check of fork activity (R-012). Synthetic values only; never a real credential, token or text from the environment files.
- Matrix-wide stop (R-014): an unknown `gh` call, an uninterceptable write, a change in fork activity or a run that read an installed copy of the skill or workers stops every remaining run at every depth. Report it to the lead before any other run starts.
- The installed user copy of the skill and workers differs from `src/` today: the create rule in the installed copy is the old one, and the installed claim files differ through earlier changes (not through 852). Controlled runs load the `src/` copy, and the user's installed copy is never modified (R-010).
- Base branch is `integration`. The pull request is opened with `Refs #834` unless every acceptance criterion is delivered with run evidence. The issue was closed on GitHub on 2026-11-26; reopening it and the closing-keyword decision belong to the lead (R-021).
- Paths written `./artifacts/...` mean the `artifacts` folder inside this plan's package directory, not a folder at the repository root. Commands that use them run from the package directory (the directory that holds this plan).
- Never stage or commit anything under `.claude/` or `.dev/issues/`.
- Raw event logs, dry-run excerpts and any other raw run output are written to a scratch directory outside the repository (Task 4 names it), are scanned by Task 9, and only scanned files are copied into `./artifacts/` (B-4).

## Phase 1: Notes-contract tests for the create question rule

## Task 1: Create the notes-contract test module with a notes builder, a notes reader and template drift guards

Covers: R-001, R-002

Create `tests/skills/test_issue_create_question_scenarios.py`. Import the path constants and helpers that `tests/skills/test_issue_protocol.py` already defines (`REFS`, `TEMPLATES`, `_text`, `headings`; `tests` is an importable package, and `test_issue_protocol.py` itself imports from `tests.skills.test_issue_worker_agents`). If an import is not clean, copy the few lines instead.

The module docstring says that these are notes-contract tests: they check the shipped notes template and the rule text as written and do not prove that a model follows the rule.

Add a builder `build_notes(additions, contradictions)` that starts from the real `src/superclaude/skills/sc-issue-protocol/templates/draft-notes.md` text (never a copy of it held in the test) and replaces the `- None` line under `## New material` and under `## Contradictions` with the given items, keeping `- None` for an empty list. Add a reader `read_notes(text)` that splits a notes file by those two headings, ignores every line inside an HTML comment block (single-line or multi-line, from its opening marker to its closing marker, because the comment text under each heading reads like item lists), drops the empty marker `None`, and returns the two item lists. The reader raises when either heading is missing or renamed, so a template change breaks every scenario instead of passing silently.

Add drift-guard tests in the style of the existing mutation tests (`tests/skills/test_issue_protocol.py:1465-1481`): a copy of the template with `## Contradictions` renamed, one with a `- None` marker removed, and one with a third heading added must each make `build_notes` or `read_notes` raise; and a copy whose comment block holds an item-like line must still read as two empty lists.

Acceptance criteria:
- `uv run pytest tests/skills/test_issue_create_question_scenarios.py -q` collects and passes the new module.
- `build_notes([], [])` reproduces the real template's two sections byte for byte, and `read_notes` of that result returns two empty lists.
- Four drift-guard tests fail the builder or reader for a renamed heading, a deleted `- None` marker, an added third heading and (as a pass test) the item-like comment line, and each is named so the failure says which template property broke.
- The module holds no copy of the template text, and its docstring states the contract-test limit above.

## Task 2: Add the question-count scenarios for empty, None, additions-only, contradiction-only, multiple and mixed notes

Covers: R-001, R-002
Depends on: Task 1

In `tests/skills/test_issue_create_question_scenarios.py` add a function `questions_for(notes_text)` that returns the number of questions the shipped rule asks for the given notes file: zero when no supported item is listed under Contradictions, otherwise exactly one. It treats only an item under `## Contradictions` as a contradiction, whatever the number of items under `## New material`.

Add one parametrized test that reads the `### Contradiction prompt rule` section of `src/superclaude/skills/sc-issue-protocol/refs/create.md` (`src/superclaude/skills/sc-issue-protocol/refs/create.md:84-86`) and asserts that it states the two outcomes `questions_for` implements: zero questions for empty notes or notes with only `None`, and exactly one question naming every item otherwise. This ties the counting function to the shipped rule text, so a rule change that the function no longer matches fails the test.

Add the scenario tests, each building its notes with `build_notes` and asserting the count and the item counts:
- empty notes (both `- None`): zero questions, zero additions, zero contradictions
- notes where `None` is the only item under both headings: the same state as empty, zero questions
- additions-only with three items, one of them `Assumption: ...`: zero questions, three additions kept
- contradiction-only with one supported item: exactly one question
- three supported contradictions in one notes file: exactly one question, not three, and the reader reports all three items so the single question can name every one
- mixed, two additions and one contradiction: exactly one question, and the two additions are still listed

Acceptance criteria:
- `uv run pytest tests/skills/test_issue_create_question_scenarios.py -q` passes with at least the six scenarios above present as separate test ids.
- Changing the number of items under New material never changes the question count in any scenario (a parametrized addition count of 0, 1 and 5).
- The rule-text test fails when the phrase that states zero questions, or the phrase that states exactly one question, is removed from a copy of `refs/create.md` (two mutation tests next to it).

## Task 3: Add the four categories, the incomplete-line routing, the preserved user flag and the secret-material scenarios

Covers: R-001, R-002, R-009
Depends on: Task 2

In `tests/skills/test_issue_create_question_scenarios.py` make `read_notes` and `questions_for` honor the template rule that an item under Contradictions counts only when it carries all three parts (a category, the user's own words in quotes or the flag as passed, and conflicting evidence); a line missing any part belongs under New material (`src/superclaude/skills/sc-issue-protocol/templates/draft-notes.md:7,13`). Take the first three category names from the `CONFLICT_CATEGORIES` constant (`tests/skills/test_issue_protocol.py:1337-1342`); its fourth entry is the fragment "contradicted by verified code" (the rule's name for the category is "a user-stated fact contradicted by verified code"), so match that category by the fragment.

Add the scenarios:
- one test per category (reversed choice, dropped requirement, changed flag, user-stated fact contradicted by verified code), each a notes file with exactly one complete item, asserting exactly one question
- a contradiction line missing its quoted user words, one missing its evidence and one missing its category: each is treated as New material, so zero questions
- the preserved user flag, two cases (B-3): a worker's disagreement with a supplied `--mode` or `--type` recorded under New material with the flag named, so zero questions; and a Contradictions item of category changed flag that states the flag as passed and that the drafted issue uses a different value, so exactly one question; also assert that the Wave 2 section of `src/superclaude/skills/sc-issue-protocol/refs/create.md` (the text between the `## Wave 2` and `## Wave 3` headings, where the sentence is at line 38) holds the sentence "The issue is filed with the user's flags when the user gave them", and that Wave 5 step 7 (the pushback comment, about line 98) still posts a disagreement after creation
- the secret-material exception: a Contradictions item that names a place and never a value counts as one question even though it quotes no user words, because `src/superclaude/skills/sc-issue-protocol/refs/create.md:59` and `src/superclaude/skills/sc-issue-protocol/templates/draft-notes.md:13` say so; the test reads both files and asserts that both carry the exception sentence

Acceptance criteria:
- The module has separate test ids for each of the four categories, the three incomplete-line cases, the two preserved-flag cases (B-3) and the secret-material case.
- The preserved-flag test fails when the cited sentence is removed from the Wave 2 section of a copy of `refs/create.md` (removing only the copy quoted inside the prompt rule at line 86 must not make it pass), and fails when the Wave 5 step 7 pushback is removed.
- The secret-material test fails when the exception sentence is removed from a copy of either file.
- `uv run pytest tests/skills/test_issue_protocol.py tests/skills/test_issue_create_question_scenarios.py -q` passes, and the 17 existing tests selected by `-k "contradiction or draft_notes or create_question or additions or evidence"` in `tests/skills/test_issue_protocol.py` still pass unchanged.

## Phase 2: Controlled-run harness

## Task 4: Settle how a controlled create run loads the revised skill, observes questions, takes an answer and blocks every write, and stop if it cannot

Covers: R-010, R-011, R-012

Write `./artifacts/harness-feasibility.md`. Establish and record, with the commands and their real output:
- the exact `claude` options of the installed version for a non-interactive run with a streamed event log (read `claude --help`): print mode, the input and output stream formats, permission mode, tool allow and deny lists, an option that gives an MCP configuration or disables MCP servers, extra directories, and any option that loads skills, agents or a plugin from a given directory
- how the `src/` copy of `sc-issue-protocol`, of `issue-worker-t1`, `issue-worker-t2` and `issue-worker-t3`, and of `src/superclaude/commands/issue.md` gets loaded for a run while the user's installed copy is left alone; list the options considered (a temporary home or configuration directory seeded from `src/`, a plugin directory) and pick one, noting how each resolves agents (an agent file in a project folder is read before the installed one, and a clone of the worktree has no such folder because it is gitignored); installing into the real user directory, or keeping the real home, is not an option unless the file shows that it resolves to `src/`
- how an `AskUserQuestion` call shows up in the event log, whether the run can supply the answer "keep my wording" (for example through a hook or the input stream), and what a run does when no answer comes
- how each GitHub write path is blocked in a run: the fake `gh` first on `PATH`, an empty `GH_CONFIG_DIR`, `GH_TOKEN`, `GITHUB_TOKEN` and `SSH_AUTH_SOCK` unset, the global and system git configuration pointed at an empty file, no credential helper, a run clone whose push URL for `origin` is invalid and whose pre-push hook refuses, and an MCP configuration with no GitHub-capable server; and how the read-only after-run fork-activity check works (issues, comments and branches of the fork since the start of the run, read with GET calls made by the harness process only, never by the run's model)
- that `src/superclaude/skills/sc-issue-protocol/scripts/` holds no `create_issue.py` and no `issue_logger.py` (the false facts of Tasks 6 to 8 depend on it), by listing the folder
- the sha256 of each `src/` file that a run must load, so every run record can show which copy it used
- the dry run itself (B-1): it happens before any write block of Task 5 exists, so run it in an isolated home and configuration directory outside the package, with `GH_TOKEN`, `GITHUB_TOKEN` and `SSH_AUTH_SOCK` unset, `gh` shadowed first on `PATH` by a stub that exits non-zero, an invalid push URL for `origin`, and a probe prompt that makes one question tool call and never invokes `/sc:issue`

Raw output of the dry run and of every later run goes to a scratch directory outside the repository, named here as `createQuestionEv-scratch` under the system temporary directory; Task 9 scans it and copies only scanned files into `./artifacts/` (B-4).

End the file with a decision section: the chosen loading option, the observation method, whether an answer can be supplied, and the stop conditions. When a dry print-mode run shows no `AskUserQuestion` event (not offered, denied or erroring), or the answer cannot be supplied, or write interception or the fork-activity check cannot be shown, the decision section is a stop report: it states what is not available, a revised estimate, whether the notes-contract tests of Phase 1 could ship alone, and the question for the lead. Task 5 does not start until the lead's reply is written into this file.

Acceptance criteria:
- `./artifacts/harness-feasibility.md` exists and answers each bullet above with a command and its real output, not a guess; a bullet the environment cannot answer is written as "not available here" with the reason.
- The decision section either says "proceed" with every control named, or is a stop report with the revised estimate; in the stop case no harness file exists under `./artifacts/harness/` until the lead's reply is recorded in the file.
- The file records the dry-run event log excerpt that shows how a question tool call appears (or that none appeared).
- The file records the dry run's command line, its environment (isolated home and configuration directory, the three unset variables, the shadowed `gh`, the invalid push URL) and its probe prompt, which never invokes `/sc:issue` (B-1).

## Task 5: Build the fake gh, the run script, the fork-activity check and the secret scan under artifacts, and prove the controls with a self-test

Covers: R-004, R-010, R-012, R-013, R-014
Depends on: Task 4

Create `./artifacts/harness/fake_gh.py` (a stand-in `gh` executable), `./artifacts/harness/run_create.py` (the run script) and `./artifacts/harness/scan_secrets.py` (the secret scan), following the decisions of `./artifacts/harness-feasibility.md`.

The fake `gh` appends one JSON line per call (arguments, time) to a log file named by an environment variable. It answers the read calls the create protocol makes with canned, clearly synthetic output: `auth status` succeeds, the repo label list holds `enhancement` and `bug`, the issue types include Feature and Bug, the organization issue-fields lookup lists a Complexity field with its options, the duplicate search returns nothing, and an issue view or field read-back returns the values a prior fake create stored. It answers `issue create` with a fake URL on a number that does not exist as a real issue, and answers `issue comment`, `issue edit` and any `api` call with a method other than GET by logging and returning success. It never runs a real `gh`, never opens a network connection and exits non-zero with a clear message for any call it does not know.

The run script takes a run name, a depth, the flags, the description, the expected counts and an output directory. It prepares the isolated home, configuration and clone of Task 4, takes the before snapshot of fork activity, runs `/sc:issue --create` in print mode with the event log streamed to a file, supplies the answer "keep my wording" when a question tool call appears (when Task 4 showed that this is possible), takes the after snapshot, and writes into the output directory: the event log, the fake `gh` call log, the run directory's `.dev/issues` tree (`issue-body.md`, `draft-notes.md`, `flags.md`, `scout.md`), the final output text, `read-files.txt` (the skill, worker and command files that the event log shows were read or spawned, each with its sha256) and `summary.json` with the counts it can compute (questions asked as tool calls, questions asked as plain text, `issue create` calls, `issue comment` calls, other write-like calls, calls the fake did not know, fork-activity change, expected counts and whether each matched). It stops the matrix (writes a stop file that every later run checks) on the conditions of the matrix-wide stop in the Constraints.

The secret scan reads every file under a given folder and fails on token-like patterns (long key strings, `ghp_` and `sk-` style prefixes, private key headers, `password=` assignments); a synthetic planted token must be found.

Add a `--self-test` mode that makes no model call.

The run script and the self-test write raw output to the scratch directory of Task 4; Task 9 scans it and copies only scanned files into `./artifacts/` (B-4).

Acceptance criteria:
- `uv run python ./artifacts/harness/run_create.py --self-test` exits 0 and its output, saved to `./artifacts/harness/self-test.txt`, shows that an `issue create`, an `issue comment`, an `api -X POST` and an `issue edit` call each landed in the log and were not forwarded, that an unknown call exits non-zero, and that the prepared run environment has no `GH_TOKEN`, `GITHUB_TOKEN`, `SSH_AUTH_SOCK` or credential helper.
- The self-test shows that `git push` from the prepared run clone fails, that the secret scan finds a planted synthetic token and passes a clean folder, and that the stop file stops a second run.
- The self-test shows that the sha256 list of the files a run must load equals the `src/` hashes of Task 4 and differs from the installed user copy for `refs/create.md`, and states that this list is the expectation: the proof for a real run is its own `read-files.txt` (Tasks 6 to 8).
- No file under `src/` or in the user's installed skill, worker or command folders is modified by the harness (a hash list taken before and after the self-test is identical).

## Phase 3: Controlled create runs

Every run in this phase checks the stop file before it starts. The matrix-wide stop of the Constraints applies across Tasks 6, 7 and 8, not only to the last of them: the first stop condition met, in any run, ends the matrix and is reported to the lead before another run starts.

## Task 6: Run the quick-depth create scenarios and record their counts

Covers: R-003, R-004, R-005, R-006, R-010, R-012, R-014
Depends on: Task 5

Use `./artifacts/harness/run_create.py` for two runs at `--depth quick`, each with an output directory under `./artifacts/runs/`:
- `quick-additions-only`: description "Feature: make `superclaude install` print, as its last line, how many skills it copied." with `--mode feature --type cli --depth quick`. It states no choice, flag value or fact that the draft could contradict. Expected: 0 questions, 1 `issue create`, 0 `issue comment`; any assumption the worker adds is an addition that must appear in the body, the notes and the final output.
- `quick-contradiction`: description "Bug: `/sc:issue --create` crashes in `src/superclaude/skills/sc-issue-protocol/scripts/create_issue.py` when the description is empty." with `--mode bug --type skill --depth quick`. That file does not exist (checked in Task 4), so a supported contradiction of a user-stated fact is expected. Expected: 1 question as a question tool call, 1 `issue create` after the answer "keep my wording", 0 `issue comment`; this is also a mixed-notes case, so record whether the additions reached the body, the notes and the final output.

Raw run output goes to the scratch directory of Task 4; Task 9 scans it and copies only scanned files into `./artifacts/runs/` (B-4).

For each run record the observed numbers whatever they are. A run that makes no `issue create` call, or asks its question as plain text, is recorded as a finding. For the contradiction run compare the issue body with the draft body and record whether the body still names `create_issue.py` as the crash location after the answer "keep my wording". If a run differs from the expectation, keep the record and note it as a finding for the lead; do not edit the skill, the template or the tests to make a run come out as expected. If a run needs one repeat because of an infrastructure failure (not a model choice), repeat it once and record both.

Acceptance criteria:
- `./artifacts/runs/quick-additions-only/summary.json` and `./artifacts/runs/quick-contradiction/summary.json` exist with the question counts, the `issue create` and `issue comment` counts, the expected counts and the after-run fork-activity result.
- Each run directory holds the event log, the fake `gh` call log, `issue-body.md`, `draft-notes.md`, the final output and `read-files.txt`; the `read-files.txt` hashes equal the `src/` list of Task 4 and no installed copy path appears in it.
- The additions run records, for each addition, whether it appears in the body, the notes and the final output, and whether the body was shown for approval; the contradiction run records the question text (does it name the contradicted item), the answer supplied and the body comparison, or an explicit "not evidenced" line when Task 4 found no way to supply an answer.
- No call in either fake `gh` log is an unknown call, and fork activity did not change.

## Task 7: Run the standard-depth create scenarios and record their counts

Covers: R-003, R-004, R-005, R-006, R-007, R-008, R-010, R-012, R-014
Depends on: Task 5

Use `./artifacts/harness/run_create.py` for four runs, each with an output directory under `./artifacts/runs/`:
- `standard-additions-only`: the quick additions description with `--mode feature --type cli --depth standard`. Expected: 0 questions, 1 `issue create`; the `issue comment` count is recorded as observed (a pushback comment appears only when the worker disagrees with a supplied flag).
- `standard-contradiction`: the quick contradiction description with `--mode bug --type skill --depth standard`. Expected: 1 question, 1 `issue create` after the answer "keep my wording".
- `standard-multi-contradiction`: description "Bug: `/sc:issue --create` crashes in `src/superclaude/skills/sc-issue-protocol/scripts/create_issue.py` when the description is empty, and the crash is written to the log by `src/superclaude/skills/sc-issue-protocol/scripts/issue_logger.py`." with `--mode bug --type skill --depth standard`. Both files do not exist (checked in Task 4). Expected: exactly 1 question that names both contradicted items (not two questions), 1 `issue create` after the answer.
- `standard-flag-preserved`: description "Make `superclaude install` print, as its last line, how many skills it copied." with `--mode bug --type cli --depth standard`, all three flags given and no mode word in the description, so the standard flag check can disagree with `--mode bug` without the description contradicting the flag. Expected: 0 questions, 1 `issue create` filed as a bug, 1 `issue comment` (the pushback comment).

Raw run output goes to the scratch directory of Task 4; Task 9 scans it and copies only scanned files into `./artifacts/runs/` (B-4).

For each run record the observed numbers and the files of Task 6. For the preserved-flag run additionally record, from the fake `gh` log, whether the filed issue used the user's `--mode bug` choice (the Bug title prefix, the Bug type and the `bug` label), whether the question count is zero, and whether the pushback comment was posted as a separate call after the create call. The findings rule of Task 6 applies.

Acceptance criteria:
- Four run directories exist under `./artifacts/runs/` with the same file set as Task 6, each with a `summary.json` carrying expected and observed counts.
- The multi-contradiction record shows the number of questions and whether the single question names both items.
- The preserved-flag record states, from the fake `gh` log, the title prefix, type and labels the issue was created with and the number of `issue comment` calls.
- Any difference from the expected counts is recorded as a finding with the raw file that shows it, and each run's `read-files.txt` and fork-activity result are recorded.

## Task 8: Run the deep-depth create scenarios and record their counts

Covers: R-003, R-004, R-005, R-006, R-008, R-010, R-012, R-014
Depends on: Task 5

Use `./artifacts/harness/run_create.py` for three runs with the same descriptions and expectations as the standard runs of Task 7 but `--depth deep`, with output directories `deep-additions-only`, `deep-contradiction` and `deep-flag-preserved` under `./artifacts/runs/`. Deep runs use `issue-worker-t1`, which falls back to `issue-worker-t2` when the tier is not served; record which worker handled each run, from the line the fallback writes into the notes or flags file, and from `read-files.txt`. Raw run output goes to the scratch directory of Task 4; Task 9 scans it and copies only scanned files into `./artifacts/runs/` (B-4).

Acceptance criteria:
- Three run directories exist under `./artifacts/runs/` with the same file set as Task 6, each with a `summary.json`, the worker that handled the run, and the expected and observed counts.
- The same per-scenario facts as Tasks 6 and 7 are recorded, and the deep adversarial flag check (a flag file for the user variant and one for the independent variant when all flags are given) is noted for the preserved-flag run.
- The stop file and the matrix-wide stop were checked before each run, and a stop condition met in any run is reported to the lead before another run starts.

## Phase 4: Evidence summary and criterion verdicts

## Task 9: Scan the run records, re-read the issue state, and write the evidence matrix and the criterion-by-criterion verdict with file and line

Covers: R-009, R-013, R-015, R-016, R-017, R-018, R-019, R-022
Depends on: Task 3, Task 6, Task 7, Task 8

First run `./artifacts/harness/scan_secrets.py` over the scratch directory of Task 4 and save the result to `./artifacts/secret-scan.txt`; a finding is removed from the raw logs (and recorded) before anything in `./artifacts/` is staged, and only the scanned files are then copied into `./artifacts/` (B-4). Then read the live state of the issue with `gh issue view 834 --repo IronbellyOrg/IronClaude --json state,closedAt,stateReason` (a read-only call by the orchestrator, not by a run) and save its output and time to `./artifacts/issue-state.txt`.

Write `./artifacts/evidence-matrix.md` with three parts.

Part one is the run matrix: one row per controlled run (quick: additions-only and contradiction; standard: additions-only, contradiction, multi-contradiction and flag-preserved; deep: additions-only, contradiction and flag-preserved) giving the expected and the observed question count, `issue create` count and `issue comment` count, the worker that handled the run, whether additions were retained in the body, the notes and the final output, whether the user flag was honored, the answer applied (or "not evidenced"), the fork-activity result and the path of its raw record. Add one row for the secret-material exception that says it is evidenced by the fixture test of Task 3 only and had no controlled run, with the reason (a controlled run would put a fake secret into a model prompt and add cost without testing more than the fixture does). Count questions and posts only from the event log and the fake `gh` log.

Part two is the verdict for each of the six acceptance criteria of the issue, quoted here in full so that the verdict is graded against the real text:
- AC1: "Across quick, standard and deep create runs, notes containing additions but no contradictions lead directly to posting, with zero questions; all additions remain in the issue and are listed in notes and final output."
- AC2: "A draft that changes an explicit flag or contradicts an instruction asks exactly one question; multiple contradictions share that question, and the answer is applied before posting."
- AC3: "The notes template clearly separates added material (no pause) from contradictions (pause), defines the four conflict categories and requires supporting user text and evidence. `None` does not count as an item."
- AC4: "`refs/create.md`, `SKILL.md`, the notes template, command description and relevant docs agree; the full body is never previewed for approval. Claim's direct flow and the launched agent's existing plan-approval boundary are unchanged."
- AC5: "Regression coverage exercises added-material-only, empty, contradiction-only and mixed notes, including multiple contradictions, all four categories, and a preserved user flag despite a worker's classification disagreement."
- AC6: "The focused tests, full suite, lint and sync check pass; the PR is opened and monitored through `/sc:pr-submit --monitor 3`."

For each, state one of "delivered by 852", "delivered by this work", "partly evidenced" or "not met" with file and line citations. The existing rule, template, command, docs and static tests are at `src/superclaude/skills/sc-issue-protocol/refs/create.md:84-86`, `src/superclaude/skills/sc-issue-protocol/templates/draft-notes.md:3-15`, `src/superclaude/commands/issue.md:19,85`, `docs/designs/sc-issue-command.md:223-225,460`, `docs/user-guide/commands.md:357` and `tests/skills/test_issue_protocol.py:1335-1526`. For AC4 read `src/superclaude/skills/sc-issue-protocol/SKILL.md:76,102-103`, `src/superclaude/skills/sc-issue-protocol/refs/claim.md:83,89-95` and `src/superclaude/skills/sc-issue-protocol/templates/launch-prompt.md:23-28`, and show that `git diff origin/integration...HEAD -- <the three files>` and `git diff HEAD -- <the three files>` are both empty (B-2; the check passes only when both are empty), before grading it. Caps: AC2 and AC5 are "partly evidenced" for every scenario in the issue's list that no controlled run exercises (empty notes, and the categories reversed choice, dropped requirement and changed flag, are exercised by the notes-contract tests only; the Phase 1 tests are contract tests and never back a "delivered by this work" verdict for behavior); a criterion whose evidence rests on a run that could not supply an answer is "partly evidenced". The secret-material exception is a qualification of AC1 and AC3. AC6 is "pending, settled by the gates and `/sc:pr-submit --monitor 3`" and is refreshed by Task 11.

Part three ends the document with a short list of findings for the lead (runs that differed from expectation, the live issue state from `./artifacts/issue-state.txt`, the secret-material qualification, the unverified items), each with its evidence path.

Acceptance criteria:
- `./artifacts/secret-scan.txt` records a clean result (or the findings removed), and `./artifacts/issue-state.txt` holds the live read of the issue with its time.
- `./artifacts/evidence-matrix.md` holds a matrix row for each executed run and the secret-material row, and each count in it can be recomputed from the cited raw file.
- Each of the six criteria is quoted in full, has a verdict and at least one `path:line` citation that was read in this work, AC4 shows both diffs empty (B-2), AC6 reads "pending", and no criterion is marked delivered by this work on the strength of a Phase 1 test or a static wording test alone when it asks for behavior.
- The document ends with the findings list, and its closing-keyword consequence is stated: with AC2 and AC5 capped, the pull request uses `Refs #834`.

## Phase 5: Gates and pull request notes

## Task 10: Run the verification gates and record their real results

Covers: R-019, R-020, R-024
Depends on: Task 3, Task 9

From the repository root run, and record command, exit code and the summary lines in `./artifacts/gates.md`: the focused selection (`uv run pytest tests/skills/test_issue_protocol.py tests/skills/test_issue_create_question_scenarios.py tests/commands/test_issue_command.py -q`), the full suite (`make test`), the linter (`make lint`) and the sync check (`make verify-sync`). If the full suite shows a failure, determine from the failing test names whether it involves any file this work changed, and record that; do not hide, skip or relax a failing test, and do not change `src/` to make a gate pass.

Acceptance criteria:
- `./artifacts/gates.md` lists the four commands with their actual exit codes and pass, fail and skip counts as printed.
- A failing gate is reported with the failing test ids and whether each is connected to the changed files; a gate that could not run is reported as not run with the reason.
- `git status` after the gates shows no file changed under `src/` and nothing staged under `.claude/` or `.dev/issues/`.

## Task 11: Write the pull request notes with the refreshed criterion 6 row and the Refs or Fixes decision

Covers: R-018, R-019, R-021, R-022, R-023
Depends on: Task 9, Task 10

Write `./artifacts/pr-notes.md` for the story agent to use in `/sc:pr-submit --monitor 3 --head <branch> --base integration`. It holds a conventional-commit title (type `test`, scope `issue`, mentioning issue 834) and a body that quotes the story's decided-for-this-work block (the base branch is `integration`; pull request 852 already merged and delivered the rule, template, command, docs and static tests; there is no open pull request to continue), the six-criterion verdict table of Task 9 with the AC6 row refreshed from `./artifacts/gates.md`, the controlled-run matrix in short form, the gate results, the secret-scan result, the findings for the lead, and the live issue state quoted from `./artifacts/issue-state.txt` (not the earlier observation). State the closing keyword decision: `Refs #834` unless Task 9 marks every criterion delivered with run evidence, in which case say which criteria that is and leave `Fixes #834` to the lead, because the issue is closed. Check whether the Generator-Constraint rule of the repository's CI (a pull request that touches a gate or validator file needs a "## Generator-Constraint Considered" section in its body) applies, using the pull request's own paths: `git diff --name-only origin/integration...HEAD` plus `git ls-files --others --exclude-standard`, compared with the path filter of `.github/workflows/contract3-generator-constraint-lint.yml`; include the section if it applies. State that nothing under `./artifacts/` is to be staged before the secret scan of Task 9 is clean.

Acceptance criteria:
- `./artifacts/pr-notes.md` exists with a title, a body and the closing keyword line, and states which criteria the pull request does and does not deliver.
- The body mentions no live issue creation and says every GitHub call in the runs went to the fake `gh` with the other write paths blocked.
- The AC6 row is refreshed from `./artifacts/gates.md`, the issue state is quoted from `./artifacts/issue-state.txt`, and the note on the Generator-Constraint rule says whether it applies and why, from the two commands above.
