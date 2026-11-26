## T1 card excerpt

Persona lens: analyzer (root-cause and deviation). This is a PRE-execution audit: the work under audit is the PLAN (plan_path below) and the driving spec is the SPEC (spec_path below). Find where the plan omits, contradicts or goes beyond the spec, and where a task as written cannot be carried out or cannot pass its own acceptance criteria. The spec's 'Revision 1' section lists findings of an earlier review that the plan must not repeat: check the plan against each of them as well. Ground every finding at file:line.

spec_path: /home/coder/workspaces/worktrees/IronClaude/issue-834-rest/.dev/tasks/to-do/TASK-WF-createQuestionEv-20261126-142533/source.md
plan_path: /home/coder/workspaces/worktrees/IronClaude/issue-834-rest/.dev/tasks/to-do/TASK-WF-createQuestionEv-20261126-142533/TASK-WF-createQuestionEv-20261126-142533.md
diff_scope: none (pre-execution)


- C1 (Grounded). The three blocking findings of the first review each have a covering task or constraint in the new plan. M-01 (tests of a test-local rule): the Constraints call the Phase 1 tests notes-contract tests (plan line 21), and Task 9 caps criteria 2 and 5 at "partly evidenced" for scenarios no run exercises (plan line 205). M-02 (no stop when the harness cannot observe questions): Task 4 ends in a stop report and "Task 5 does not start until the lead's reply is written into this file" (plan line 104, acceptance at line 108). M-03 (GitHub write paths and unscanned logs): the Constraints list the extra write paths to block (plan line 22), Task 5 builds the fake `gh`, the run script and the secret scan (plan line 116), and Task 9 runs the scan before anything is staged (plan line 191).
- C2 (Grounded). The matrix-wide stop that the first plan kept only in the last run task is now in the Constraints (plan line 23) and in a preamble before Task 6 (plan line 134).
- C3 (Grounded). The plan states that the installed copy of the skill and workers differs from `src/` and that runs must load `src/` (plan line 24), and Task 5 asks for `read-files.txt` per run, built from the run's own event log (plan line 120), instead of relying on the self-test hash list alone.
- C4 (Grounded). The closing keyword rule is `Refs #834` unless every criterion is delivered with run evidence (plan lines 25 and 234), with AC2 and AC5 capped by Task 9 (plan line 205), so the expected outcome is `Refs #834`, as the lead's scope change requires (source.md:43).
- C5 (Grounded). Mechanical coverage: parsed 24 of 24 requirements matched by exact id, union 0.8421 over 38 rows, `S_dev_density` 0.1579, no `coverage_degraded` (artifacts/coverage-matrix.json). The six unmapped inferred rows (INF-001, 002, 003, 004, 007, 009) are each covered by hand: INF-001 and INF-009 across Tasks 5 to 9, INF-002 by the Constraints and Task 9, INF-003 by the issue-state read in Task 9 (plan line 191) and the Constraints (plan line 25), INF-004 by Tasks 1 to 3, INF-007 by Task 4 (plan line 104).
- C6 (INFERRED). When Task 4's stop report triggers, the plan cannot finish without a reply from the lead; an unattended executor would stop at Task 4. That is intended by the spec (source.md:35), but the plan does not say who writes the reply into the file or how the executor waits.
- C7 (INFERRED). The plan still sets no time or cost ceiling on the nine controlled runs; only stop conditions end the matrix early.
- C8 (INFERRED). Task 5 builds three scripts and a self-test in one task (plan lines 116 to 127), which is large for one task, although each file is named.


## Grounding hunks

codegraph run state: index_state=stale checked_at=2026-11-26T13:23:40Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/issue-834-rest projectPath=/home/coder/workspaces/worktrees/IronClaude/issue-834-rest

### src/superclaude/skills/sc-issue-protocol/refs/create.md:84-86

```markdown
### Contradiction prompt rule (default D14)

Ask only when `draft-notes.md` lists a supported contradiction of the user's own description, instruction or flag: reversed choice, dropped requirement, changed flag, or a user-stated fact contradicted by verified code (each with the user's own words and the conflicting evidence). Empty notes, or notes with only `None` under both headings, ask zero questions and Wave 5 posts. One or more supported contradiction items ask exactly one question (AskUserQuestion), once per run, naming every item, with the choices "keep my wording" (change the draft to honor the user's words), "keep the draft" (accept the draft's change) and "edit". Apply the answer to `<D>/issue-body.md` before Wave 5; it changes only the contradicted items. Every New material item, assumptions included, stays in the body and in `draft-notes.md` whatever the answer, and is listed in the final output. A worker's disagreement with a supplied flag is not a contradiction when the issue is filed with the user's flag (Wave 2, line "The issue is filed with the user's flags when the user gave them"); it stays the pushback comment of Wave 5 step 7. The full body is never shown for approval (B1).
```

### src/superclaude/skills/sc-issue-protocol/refs/create.md:38-38

```markdown
Every choice is written to `<D>/flags.md` from `templates/flags-decision.md` (mode, type, issue type, complexity, reasons); `flags-user.md` and `flags-t1.md` use the same template. The `Issue type` row is derived by the orchestrator from the mode and the area by the rule of `refs/labels.md` (a bug is Bug, a feature in the area `tests` is Test, any other feature is Feature), after any worker returns. The issue is filed with the user's flags when the user gave them (the pushback comment explains any disagreement; the issue is not silently reclassified), else with the worker's choice.
```

### src/superclaude/skills/sc-issue-protocol/refs/create.md:57-59

```markdown
At deep depth the `issue-worker-t1` spawn falls back to `issue-worker-t2` as described in Wave 2. The worker fills the chosen template into `<D>/issue-body.md`, keeping every heading and writing "Not known yet" where the description and the codebase pass give nothing (no invented facts), except in the three required plan sections defined in the next subsection. It lists, in `<D>/draft-notes.md` (from `templates/draft-notes.md`), under New material every addition beyond the description (assumptions included), which is kept without any question, and under Contradictions only a supported contradiction of the user's own words. A contradiction is one of exactly four categories: reversed choice (the draft reverses a choice the user stated), dropped requirement (the draft omits a requirement the user stated), changed flag (the drafted issue would not honor `--mode`, `--type` or `--depth` as given) and user-stated fact contradicted by verified code (the worker read the code and the user's stated fact is false). Each contradiction line carries its category, the user's own words in quotes (or the flag as passed) and the conflicting evidence (draft text, or a `path:line` the worker read); a line missing any of the three is recorded as New material instead. An addition that is the only evidence of a contradiction is listed under Contradictions.

Secrets rule: the drafting worker never copies anything that looks like a secret (a key, token, password, credential, or a connection string with a password) or any text from `~/.env`, environment variables or credential files into the issue body or the notes. If the draft would contain such material, the worker leaves the value out and lists that under Contradictions (naming the place, never the value), so the contradiction question is asked.
```

### src/superclaude/skills/sc-issue-protocol/templates/draft-notes.md:1-15

```markdown
# Draft notes

Leave a list empty (write "None") when there is nothing to report. "None" is the empty marker, never an item, and `- None` under both headings is the same state as empty notes. Items under New material cause no question: they are kept in the issue body and printed in the final output. One or more supported items under Contradictions cause exactly one question to the user.

## New material

<!-- Facts added to the issue body that the description did not contain, one per line, each with its source (path:line or command). List an assumption as `Assumption: <text>`. A contradiction line that lacks its category, the user's own words or its conflicting evidence belongs here instead. -->

- None

## Contradictions

<!-- Only a supported contradiction of the user's own description, instruction or flag, one per line, in this form: category (reversed choice, dropped requirement, changed flag, or user-stated fact contradicted by verified code), the user's own words in quotes (or the flag as passed), and the conflicting evidence (draft text, or a path:line the worker read). A line missing any of the three parts belongs under New material. A worker's disagreement with a user-supplied flag is not a contradiction when the issue is filed with the user's flag. An addition that is the only evidence of a contradiction is listed here. Secrets rule: the worker never copies anything that looks like a secret (a key, token, password, credential, or a connection string with a password) or any text from ~/.env, environment variables or credential files into the issue body or these notes; if the draft would contain such material, list that here (the place, never the value) so the contradiction question is asked. -->

- None
```

### tests/skills/test_issue_protocol.py:1337-1347

```python
CONFLICT_CATEGORIES = [
    "reversed choice",
    "dropped requirement",
    "changed flag",
    "contradicted by verified code",
]
# The old broad trigger and the old first choice are built from fragments, so no
# whole copy of either sits in tests/ (a search of tests/ for them finds nothing).
OLD_TRIGGER = "new" + " material" + " or a" + " contradiction"
OLD_KEEP_ALL = '"keep' + ' all"'

```

### tests/skills/test_issue_protocol.py:1365-1381

```python
def create_question_problems(ref: str, skill: str) -> list[str]:
    """Problems with the rule that create asks only for a supported contradiction."""
    section = prompt_rule_section(ref)
    problems = [
        f"prompt rule section lacks the category {name!r}"
        for name in CONFLICT_CATEGORIES
        if name not in section
    ]
    for needle in ("exactly one", "before Wave 5", "zero questions"):
        if needle not in section:
            problems.append(f"prompt rule section lacks {needle!r}")
    for where, text in (("refs/create.md", ref), ("SKILL.md", skill)):
        if OLD_TRIGGER in text:
            problems.append(f"{where} still carries the old broad trigger")
    if OLD_KEEP_ALL in ref:
        problems.append("refs/create.md still offers the old keep-all choice")
    return problems
```

### .dev/tasks/to-do/TASK-WF-createQuestionEv-20261126-142533/TASK-WF-createQuestionEv-20261126-142533.md:17-27

```markdown
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
```

### .dev/tasks/to-do/TASK-WF-createQuestionEv-20261126-142533/TASK-WF-createQuestionEv-20261126-142533.md:31-90

```markdown
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
- a preserved user flag: a worker's disagreement with a supplied `--mode` or `--type` is written as an ordinary New material line, or as a Contradictions line without the user's quoted words, so zero questions; also assert that the Wave 2 section of `src/superclaude/skills/sc-issue-protocol/refs/create.md` (the text between the `## Wave 2` and `## Wave 3` headings, where the sentence is at line 38) holds the sentence "The issue is filed with the user's flags when the user gave them", and that Wave 5 step 7 (the pushback comment, about line 98) still posts a disagreement after creation
- the secret-material exception: a Contradictions item that names a place and never a value counts as one question even though it quotes no user words, because `src/superclaude/skills/sc-issue-protocol/refs/create.md:59` and `src/superclaude/skills/sc-issue-protocol/templates/draft-notes.md:13` say so; the test reads both files and asserts that both carry the exception sentence

Acceptance criteria:
- The module has separate test ids for each of the four categories, the three incomplete-line cases, the preserved-flag case and the secret-material case.
- The preserved-flag test fails when the cited sentence is removed from the Wave 2 section of a copy of `refs/create.md` (removing only the copy quoted inside the prompt rule at line 86 must not make it pass), and fails when the Wave 5 step 7 pushback is removed.
- The secret-material test fails when the exception sentence is removed from a copy of either file.
- `uv run pytest tests/skills/test_issue_protocol.py tests/skills/test_issue_create_question_scenarios.py -q` passes, and the 17 existing tests selected by `-k "contradiction or draft_notes or create_question or additions or evidence"` in `tests/skills/test_issue_protocol.py` still pass unchanged.

## Phase 2: Controlled-run harness
```

### .dev/tasks/to-do/TASK-WF-createQuestionEv-20261126-142533/TASK-WF-createQuestionEv-20261126-142533.md:92-133

```markdown
## Task 4: Settle how a controlled create run loads the revised skill, observes questions, takes an answer and blocks every write, and stop if it cannot

Covers: R-010, R-011, R-012

Write `./artifacts/harness-feasibility.md`. Establish and record, with the commands and their real output:
- the exact `claude` options of the installed version for a non-interactive run with a streamed event log (read `claude --help`): print mode, the input and output stream formats, permission mode, tool allow and deny lists, an option that gives an MCP configuration or disables MCP servers, extra directories, and any option that loads skills, agents or a plugin from a given directory
- how the `src/` copy of `sc-issue-protocol`, of `issue-worker-t1`, `issue-worker-t2` and `issue-worker-t3`, and of `src/superclaude/commands/issue.md` gets loaded for a run while the user's installed copy is left alone; list the options considered (a temporary home or configuration directory seeded from `src/`, a plugin directory) and pick one, noting how each resolves agents (an agent file in a project folder is read before the installed one, and a clone of the worktree has no such folder because it is gitignored); installing into the real user directory, or keeping the real home, is not an option unless the file shows that it resolves to `src/`
- how an `AskUserQuestion` call shows up in the event log, whether the run can supply the answer "keep my wording" (for example through a hook or the input stream), and what a run does when no answer comes
- how each GitHub write path is blocked in a run: the fake `gh` first on `PATH`, an empty `GH_CONFIG_DIR`, `GH_TOKEN`, `GITHUB_TOKEN` and `SSH_AUTH_SOCK` unset, the global and system git configuration pointed at an empty file, no credential helper, a run clone whose push URL for `origin` is invalid and whose pre-push hook refuses, and an MCP configuration with no GitHub-capable server; and how the read-only after-run fork-activity check works (issues, comments and branches of the fork since the start of the run, read with GET calls made by the harness process only, never by the run's model)
- that `src/superclaude/skills/sc-issue-protocol/scripts/` holds no `create_issue.py` and no `issue_logger.py` (the false facts of Tasks 6 to 8 depend on it), by listing the folder
- the sha256 of each `src/` file that a run must load, so every run record can show which copy it used

End the file with a decision section: the chosen loading option, the observation method, whether an answer can be supplied, and the stop conditions. When a dry print-mode run shows no `AskUserQuestion` event (not offered, denied or erroring), or the answer cannot be supplied, or write interception or the fork-activity check cannot be shown, the decision section is a stop report: it states what is not available, a revised estimate, whether the notes-contract tests of Phase 1 could ship alone, and the question for the lead. Task 5 does not start until the lead's reply is written into this file.

Acceptance criteria:
- `./artifacts/harness-feasibility.md` exists and answers each bullet above with a command and its real output, not a guess; a bullet the environment cannot answer is written as "not available here" with the reason.
- The decision section either says "proceed" with every control named, or is a stop report with the revised estimate; in the stop case no harness file exists under `./artifacts/harness/` until the lead's reply is recorded in the file.
- The file records the dry-run event log excerpt that shows how a question tool call appears (or that none appeared).

## Task 5: Build the fake gh, the run script, the fork-activity check and the secret scan under artifacts, and prove the controls with a self-test

Covers: R-004, R-010, R-012, R-013, R-014
Depends on: Task 4

Create `./artifacts/harness/fake_gh.py` (a stand-in `gh` executable), `./artifacts/harness/run_create.py` (the run script) and `./artifacts/harness/scan_secrets.py` (the secret scan), following the decisions of `./artifacts/harness-feasibility.md`.

The fake `gh` appends one JSON line per call (arguments, time) to a log file named by an environment variable. It answers the read calls the create protocol makes with canned, clearly synthetic output: `auth status` succeeds, the repo label list holds `enhancement` and `bug`, the issue types include Feature and Bug, the organization issue-fields lookup lists a Complexity field with its options, the duplicate search returns nothing, and an issue view or field read-back returns the values a prior fake create stored. It answers `issue create` with a fake URL on a number that does not exist as a real issue, and answers `issue comment`, `issue edit` and any `api` call with a method other than GET by logging and returning success. It never runs a real `gh`, never opens a network connection and exits non-zero with a clear message for any call it does not know.

The run script takes a run name, a depth, the flags, the description, the expected counts and an output directory. It prepares the isolated home, configuration and clone of Task 4, takes the before snapshot of fork activity, runs `/sc:issue --create` in print mode with the event log streamed to a file, supplies the answer "keep my wording" when a question tool call appears (when Task 4 showed that this is possible), takes the after snapshot, and writes into the output directory: the event log, the fake `gh` call log, the run directory's `.dev/issues` tree (`issue-body.md`, `draft-notes.md`, `flags.md`, `scout.md`), the final output text, `read-files.txt` (the skill, worker and command files that the event log shows were read or spawned, each with its sha256) and `summary.json` with the counts it can compute (questions asked as tool calls, questions asked as plain text, `issue create` calls, `issue comment` calls, other write-like calls, calls the fake did not know, fork-activity change, expected counts and whether each matched). It stops the matrix (writes a stop file that every later run checks) on the conditions of the matrix-wide stop in the Constraints.

The secret scan reads every file under a given folder and fails on token-like patterns (long key strings, `ghp_` and `sk-` style prefixes, private key headers, `password=` assignments); a synthetic planted token must be found.

Add a `--self-test` mode that makes no model call.

Acceptance criteria:
- `uv run python ./artifacts/harness/run_create.py --self-test` exits 0 and its output, saved to `./artifacts/harness/self-test.txt`, shows that an `issue create`, an `issue comment`, an `api -X POST` and an `issue edit` call each landed in the log and were not forwarded, that an unknown call exits non-zero, and that the prepared run environment has no `GH_TOKEN`, `GITHUB_TOKEN`, `SSH_AUTH_SOCK` or credential helper.
- The self-test shows that `git push` from the prepared run clone fails, that the secret scan finds a planted synthetic token and passes a clean folder, and that the stop file stops a second run.
- The self-test shows that the sha256 list of the files a run must load equals the `src/` hashes of Task 4 and differs from the installed user copy for `refs/create.md`, and states that this list is the expectation: the proof for a real run is its own `read-files.txt` (Tasks 6 to 8).
- No file under `src/` or in the user's installed skill, worker or command folders is modified by the harness (a hash list taken before and after the self-test is identical).

## Phase 3: Controlled create runs

```

### .dev/tasks/to-do/TASK-WF-createQuestionEv-20261126-142533/TASK-WF-createQuestionEv-20261126-142533.md:134-183

```markdown
Every run in this phase checks the stop file before it starts. The matrix-wide stop of the Constraints applies across Tasks 6, 7 and 8, not only to the last of them: the first stop condition met, in any run, ends the matrix and is reported to the lead before another run starts.

## Task 6: Run the quick-depth create scenarios and record their counts

Covers: R-003, R-004, R-005, R-006, R-010, R-012, R-014
Depends on: Task 5

Use `./artifacts/harness/run_create.py` for two runs at `--depth quick`, each with an output directory under `./artifacts/runs/`:
- `quick-additions-only`: description "Feature: make `superclaude install` print, as its last line, how many skills it copied." with `--mode feature --type cli --depth quick`. It states no choice, flag value or fact that the draft could contradict. Expected: 0 questions, 1 `issue create`, 0 `issue comment`; any assumption the worker adds is an addition that must appear in the body, the notes and the final output.
- `quick-contradiction`: description "Bug: `/sc:issue --create` crashes in `src/superclaude/skills/sc-issue-protocol/scripts/create_issue.py` when the description is empty." with `--mode bug --type skill --depth quick`. That file does not exist (checked in Task 4), so a supported contradiction of a user-stated fact is expected. Expected: 1 question as a question tool call, 1 `issue create` after the answer "keep my wording", 0 `issue comment`; this is also a mixed-notes case, so record whether the additions reached the body, the notes and the final output.

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

For each run record the observed numbers and the files of Task 6. For the preserved-flag run additionally record, from the fake `gh` log, whether the filed issue used the user's `--mode bug` choice (the Bug title prefix, the Bug type and the `bug` label), whether the question count is zero, and whether the pushback comment was posted as a separate call after the create call. The findings rule of Task 6 applies.

Acceptance criteria:
- Four run directories exist under `./artifacts/runs/` with the same file set as Task 6, each with a `summary.json` carrying expected and observed counts.
- The multi-contradiction record shows the number of questions and whether the single question names both items.
- The preserved-flag record states, from the fake `gh` log, the title prefix, type and labels the issue was created with and the number of `issue comment` calls.
- Any difference from the expected counts is recorded as a finding with the raw file that shows it, and each run's `read-files.txt` and fork-activity result are recorded.

## Task 8: Run the deep-depth create scenarios and record their counts

Covers: R-003, R-004, R-005, R-006, R-008, R-010, R-012, R-014
Depends on: Task 5

Use `./artifacts/harness/run_create.py` for three runs with the same descriptions and expectations as the standard runs of Task 7 but `--depth deep`, with output directories `deep-additions-only`, `deep-contradiction` and `deep-flag-preserved` under `./artifacts/runs/`. Deep runs use `issue-worker-t1`, which falls back to `issue-worker-t2` when the tier is not served; record which worker handled each run, from the line the fallback writes into the notes or flags file, and from `read-files.txt`.

Acceptance criteria:
- Three run directories exist under `./artifacts/runs/` with the same file set as Task 6, each with a `summary.json`, the worker that handled the run, and the expected and observed counts.
- The same per-scenario facts as Tasks 6 and 7 are recorded, and the deep adversarial flag check (a flag file for the user variant and one for the independent variant when all flags are given) is noted for the preserved-flag run.
- The stop file and the matrix-wide stop were checked before each run, and a stop condition met in any run is reported to the lead before another run starts.

```

## Coverage slice

| Requirement / Task | Card ID | Status | Grounding |
|---|---|---|---|
| INF-001 (source.md:11) | Task 9 (best containment 0.5) | unmapped | source.md:11 |
| INF-002 (source.md:11) | Task 9 (best containment 0.381) | unmapped | source.md:11 |
| INF-003 (source.md:11) | Task 9 (best containment 0.5833) | unmapped | source.md:11 |
| INF-004 (source.md:23) | Task 3 (best containment 0.5385) | unmapped | source.md:23 |
| INF-005 (source.md:26) | Task 9 (best containment 0.6923) | covered | source.md:26 |
| INF-006 (source.md:27) | Task 4 (best containment 0.6) | covered | source.md:27 |
| INF-007 (source.md:35) | Task 4 (best containment 0.375) | unmapped | source.md:35 |
| INF-008 (source.md:43) | Task 9 (best containment 0.96) | covered | source.md:43 |
| INF-009 (source.md:43) | Task 9 (best containment 0.5556) | unmapped | source.md:43 |
| INF-010 (source.md:43) | Task 11 (best containment 1.0) | covered | source.md:43 |
| INF-011 (source.md:43) | Task 11 (best containment 0.8) | covered | source.md:43 |
| INF-012 (source.md:43) | Task 9 (best containment 0.7778) | covered | source.md:43 |
| INF-013 (source.md:45) | Task 4 (best containment 0.75) | covered | source.md:45 |
| INF-014 (source.md:49) | Task 2 (best containment 0.6667) | covered | source.md:49 |
