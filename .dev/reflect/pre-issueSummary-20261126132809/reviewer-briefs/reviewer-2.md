## T1 card excerpt

Persona lens: qa (coverage and acceptance). This is a PRE-execution audit: the work under audit is the PLAN and the driving spec is the SPEC. Audit the coverage matrix AGAINST the spec body in your grounding hunks; surface any requirement-bearing span absent from the matrix (parsed or inferred) as a finding. Also check that each task's acceptance criteria can actually be passed or failed as written.

spec_path: /home/coder/workspaces/worktrees/IronClaude/issue-834-rest/.dev/tasks/to-do/TASK-WF-issueSummary-20261126-132314/source.md
plan_path: /home/coder/workspaces/worktrees/IronClaude/issue-834-rest/.dev/tasks/to-do/TASK-WF-issueSummary-20261126-132314/TASK-WF-issueSummary-20261126-132314.md
diff_scope: none (pre-execution)


- C9 (Grounded). Mechanical coverage is 6 of 13 inferred requirement rows matched (coverage_pct_union 0.4615, S_dev_density 0.5385; artifacts/coverage-matrix.json). The single-task containment rule undercounts rows whose coverage spans several tasks (INF-001, INF-009) or sits in the plan's Constraints section, which is not a matchable task item (INF-003 reopening, INF-005 claim boundary). Read by hand, every unmapped row has coverage somewhere in the plan except the "revisit the estimate" half of INF-007 (see C8).
- C10 (Grounded). The plan keeps the secret-material exception as a qualification and does not remove it (plan line 20, Task 3 and Task 9), as source.md:11 requires.
- C11 (Grounded). The plan opens the pull request with `Refs #834` unless every criterion is delivered with run evidence, and leaves `Fixes #834` to the lead (Task 11), as source.md:43 requires.
- C12 (INFERRED). Task 1 says the reader "drops the empty marker `None`" but does not say it must ignore the HTML comment block inside each section of src/superclaude/skills/sc-issue-protocol/templates/draft-notes.md (lines 7 and 13), whose text contains words that look like items. An implementer may count comment text as items.
- C13 (INFERRED). Task 9 asks for a verdict on "the six acceptance criteria of the issue" quoted "through the summary", but the summary only paraphrases them; the exact criterion text is in the issue body on GitHub, not in source.md.

## Grounding hunks

codegraph run state: index_state=stale checked_at=2026-11-26T13:23:40Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/issue-834-rest projectPath=/home/coder/workspaces/worktrees/IronClaude/issue-834-rest

### .dev/tasks/to-do/TASK-WF-issueSummary-20261126-132314/source.md:1-45

```markdown
# Summary: #834 [FEATURE] /sc:issue --create asks the user a question only when the draft contradicts what the user said

- Issue: https://github.com/IronbellyOrg/IronClaude/issues/834
- Type: feature
- Complexity: medium (rubric: `refs/claim.md`; remaining work is over 4 and up to 16 hours in the single issue-create subsystem)
- Effort estimate: 8 hours
- spec-route: design — Medium complexity with explicit acceptance criteria; design the remaining scenario verification rather than redoing the merged rule changes.

## What the issue asks for

Issue creation should keep and disclose helpful additions without asking permission, and ask one combined question only for supported conflicts with the user's words or explicit flags. Pull request #852 already delivered the core rules, notes template, worker guidance, command/docs alignment and static wording tests; the issue's old source citations and earlier claim's 12-hour estimate are outdated. What remains is scenario regression coverage and recorded quick, standard and deep create runs demonstrating actual question/post counts, response application, addition retention and preserved user flags, followed by the required verification gates. The live issue was closed on 2026-11-26 at 13:14:10 UTC during this check, so the orchestrator must re-check that state and not treat these files as permission to reopen it or continue claim writes. The merged secrets rule deliberately adds a question-triggering exception; #852's review reply calls it intended, so verification must state this qualification rather than silently remove that safeguard.

## Relevant files and systems (cheatsheet)

| Path or system | Why it matters |
|---|---|
| `src/superclaude/skills/sc-issue-protocol/refs/create.md:53-59,65-71,84-99` | Depth/worker routing, four conflict categories, secret-material exception, preserved planning/assumptions, single question before posting and addition disclosure. |
| `src/superclaude/skills/sc-issue-protocol/SKILL.md:76,86,102-103` | Core no-preview rule, closed-claim stop and create summary; already changed by #852. |
| `src/superclaude/skills/sc-issue-protocol/templates/draft-notes.md:3-15` | Separate notes lists, None sentinel, user quotation/evidence and flag-disagreement carve-out. |
| `src/superclaude/agents/issue-worker-t1.md:24`, `issue-worker-t2.md:24`, `issue-worker-t3.md:24` | All three drafting workers already share the supported-conflict classification guidance; exercise their depth paths. |
| `src/superclaude/commands/issue.md:19,85` | Already describes the narrow question exception and retained additions. |
| `docs/designs/sc-issue-command.md:223-225,460`; `docs/user-guide/commands.md:357` | Already aligned for ordinary contradiction-only creation; no routine full-body approval. |
| `tests/skills/test_issue_protocol.py:1335-1526` | Existing guards inspect/mutate Markdown strings. They do not execute notes-state scenarios or measure questions/posts. Keep them and add genuinely exercised cases. |
| `tests/commands/test_issue_command.py:287-343` | Static command/skill agreement guards, not create-run evidence. |
| `tests/skills/test_worker_contract.py:3113-3119` | Exact-line side-effect allowlist adjusted for the new output wording, not a decision test. |
| `src/superclaude/skills/sc-issue-protocol/refs/claim.md:80-95`; `templates/launch-prompt.md:23-28` | Preserve claim's direct posting, staged-recommendation distinction and worktree-only plan approval boundary. |
| `Makefile:109-136,166-250`; skill installers | Project mirror sync is not a home-install refresh. Controlled runs must load the revised skill, not a stale installed copy. No new production decision service is requested. |
| #852 and its CI run `45739062371` | Historical checks report success and the PR is merged. They do not supply actual create question/post counts or prove the precise submission command used. |

## Analysis

- [Standard codebase analysis and remaining verification plan](analysis/analyze-sc-issue-protocol.md).
- [Claim-by-claim accuracy check and all six acceptance-criterion verdicts](accuracy-check.md).

**Estimate is for what is still left**, not the already merged implementation: approximately 3 hours for executable scenario coverage, 3 hours for controlled cross-depth runs and their evidence, and 2 hours for gate results/review/closeout evidence. Assumption: an isolated runner can intercept question and GitHub-post tools without live test issues; if that is unavailable, the estimate must be revisited, not replaced with a second copy of the decision rule that only tests itself. This is one issue-create subsystem despite the multiple text/test surfaces, not a new cross-system feature.

Observed locally: the requested focused selection passed **17 tests, 186 deselected, in 0.26 seconds**. The PR body reports 1023 focused tests and clean lint/sync; its check rollup confirms historical test/lint/sync job success. Full suite, lint and sync were not rerun here, and controlled create-run counts are Not known yet. Exact `/sc:pr-submit --monitor 3` invocation for #852 is Not known yet, although both review services left reviews. Source inspection is pinned to `862384852faebe3255c2876527103696cfd3cf3b`, not the subsequently advanced integration tip. Codegraph/auggie MCP tools were unavailable; analysis continued with Grep, Glob and Read.

## Decided for this work (iteration 3)

- **Scope:** its Fix approach says base branch master, but the default branch is integration: branch from integration; pull request 852 (it replaced the closed 849) already carries this work: continue on it (step 1, open pull request check) instead of starting a second one.

Lead's scope change (26 Nov 2026, Clay's go), which replaces the open-pull-request part of the line above: pull request 852 already merged to integration with 'Refs #834' and delivered the rule text, the notes template, the command and docs, and the static wording tests in tests/skills/test_issue_protocol.py (focused tests pass, CI was green). There is no open pull request to continue, so work starts from origin/integration in this worktree (the older issue-834 worktree holds abandoned work and is not used). Do only what 852 left undone: (1) regression tests for added-material-only, empty, contradiction-only and mixed notes, multiple contradictions sharing one question, all four categories, and a user flag preserved despite a worker's disagreement; (2) the controlled-run evidence of actual question and post counts across quick, standard and deep create runs, with GitHub writes intercepted or disposable issues explicitly authorized (no live test issues without asking the lead). If a criterion is already delivered, say so with the file and line. Base branch is integration, not master. The pull request is opened with `Refs #834` unless it delivers every criterion.

Seen during the claim (13:14 UTC, 26 Nov 2026): GitHub issue 834 was closed as completed by clayphi at 13:14:08Z with a comment that pull request 852 delivered it. The claim therefore posted and edited nothing on GitHub (a closed issue stops a claim); the two earlier claim comments from 25 Nov still say 12 hours and "create defect remains present". Reopening is the lead's decision.
```

### .dev/tasks/to-do/TASK-WF-issueSummary-20261126-132314/TASK-WF-issueSummary-20261126-132314.md:1-200

```markdown
---
schema: workflow-plan/1.2
source: ./source.md
strategy: systematic
depth: standard
slug: TASK-WF-issueSummary-20261126-132314
version: "1"
priority: Medium
created_date: "2026-11-26"
---

# Scenario regression tests and controlled-run evidence for the /sc:issue --create question rule (issue 834)

Source: ./source.md
Goal: Close what pull request 852 left open on issue 834: scenario tests that run notes through the create question rule and count questions, plus recorded quick, standard and deep create runs with the actual question and post counts, all with GitHub writes intercepted, and a criterion-by-criterion verdict that cites file and line.

## Constraints

- Pull request 852 already delivered the rule text (`src/superclaude/skills/sc-issue-protocol/refs/create.md:84-86`), the notes template (`src/superclaude/skills/sc-issue-protocol/templates/draft-notes.md`), the worker guidance, the command and docs text, and the static wording tests (`tests/skills/test_issue_protocol.py:1335-1526`). Do not redo or reword any of them. Keep every existing test as it is.
- The secret-material exception (`src/superclaude/skills/sc-issue-protocol/refs/create.md:59` and `src/superclaude/skills/sc-issue-protocol/templates/draft-notes.md:13`) is deliberate: a would-be secret is listed under Contradictions and causes the one question. Record it as a qualification; never remove it and never describe the rule as "only the four categories" without it.
- No production decision code and no new command flag: the question decision stays prose that the orchestrating model follows. The tests and the harness are test and evidence tooling only. Nothing under `src/superclaude/` changes in this plan.
- No live test issues and no GitHub writes of any kind. Every `gh` call in a controlled run goes to a fake `gh` that logs it and never forwards it. Synthetic values only; never a real credential, token or text from the environment files.
- The installed user copy of the skill and of the three issue workers differs from `src/` (it is the pre-852 version: its `SKILL.md`, `refs/create.md`, `refs/claim.md`, `templates/draft-notes.md` and the three `issue-worker-t*.md` files differ). Controlled runs must load the `src/` copy. Never modify the user's installed copy to do that.
- Base branch is `integration`. The pull request is opened with `Refs #834` unless it delivers every acceptance criterion of the issue. The issue itself was closed on GitHub on 2026-11-26 (13:14 UTC); reopening it is the lead's decision, not this plan's.
- Never stage or commit anything under `.claude/` or `.dev/issues/`.

## Phase 1: Scenario regression tests for the notes rule

## Task 1: Create the scenario test module with a notes builder, a notes reader and template drift guards

Create `tests/skills/test_issue_create_question_scenarios.py`. Import the path constants and helpers that `tests/skills/test_issue_protocol.py` already defines (`REFS`, `TEMPLATES`, `_text`, `headings`; `tests` is an importable package, and `test_issue_protocol.py` itself imports from `tests.skills.test_issue_worker_agents`). If an import is not clean, copy the few lines instead.

Add a builder `build_notes(additions, contradictions)` that starts from the real `src/superclaude/skills/sc-issue-protocol/templates/draft-notes.md` text (never a copy of it held in the test) and replaces the `- None` line under `## New material` and under `## Contradictions` with the given items, keeping `- None` for an empty list. Add a reader `read_notes(text)` that splits a notes file by those two headings, drops the empty marker `None`, and returns the two item lists. The reader raises when either heading is missing or renamed, so a template change breaks every scenario instead of passing silently.

Add drift-guard tests in the style of the existing mutation tests (`tests/skills/test_issue_protocol.py:1465-1481`): a copy of the template with `## Contradictions` renamed, one with a `- None` marker removed, and one with a third heading added must each make `build_notes` or `read_notes` raise.

Acceptance criteria:
- `uv run pytest tests/skills/test_issue_create_question_scenarios.py -q` collects and passes the new module.
- `build_notes([], [])` reproduces the real template's two sections byte for byte, and `read_notes` of that result returns two empty lists.
- Three drift-guard tests fail the builder or reader for a renamed heading, a deleted `- None` marker and an added third heading, and each is named so the failure says which template property broke.
- The module holds no copy of the template text; the only template source is the file read at test time.

## Task 2: Add the question-count scenarios for empty, None, additions-only, contradiction-only, multiple and mixed notes

Depends on: Task 1

In `tests/skills/test_issue_create_question_scenarios.py` add a function `questions_for(notes_text)` that returns the number of questions the rule asks for the given notes file: zero when no supported item is listed under Contradictions, otherwise exactly one. It must treat only an item under `## Contradictions` as a contradiction, whatever the number of items under `## New material`.

Add one parametrized test that reads the rule text of `src/superclaude/skills/sc-issue-protocol/refs/create.md` (the `### Contradiction prompt rule` section, `src/superclaude/skills/sc-issue-protocol/refs/create.md:84-86`) and asserts that it states the two outcomes `questions_for` implements: zero questions for empty notes or notes with only `None`, and exactly one question naming every item otherwise. This ties the counting function to the shipped rule text, so a rule change that the function no longer matches fails the test.

Add the scenario tests, each building its notes with `build_notes` and asserting the count and the item counts:
- empty notes (both `- None`): zero questions, zero additions, zero contradictions
- notes where `None` is written as the only item under both headings: the same state as empty, zero questions
- additions-only with three items, one of them `Assumption: ...`: zero questions, three additions kept
- contradiction-only with one supported item: exactly one question
- three supported contradictions in one notes file: exactly one question, not three, and the reader reports all three items so the single question can name every one
- mixed, two additions and one contradiction: exactly one question, and the two additions are still listed

Acceptance criteria:
- `uv run pytest tests/skills/test_issue_create_question_scenarios.py -q` passes with at least the six scenarios above present as separate test ids.
- Changing the number of items under New material never changes the question count in any scenario (assert it with a parametrized addition count of 0, 1 and 5).
- The rule-text test fails when the phrase that states zero questions or the phrase that states exactly one question is removed from a copy of `refs/create.md` (add the two mutation tests next to it).

## Task 3: Add the four categories, the incomplete-line routing, the preserved user flag and the secret-material scenarios

Depends on: Task 2

In `tests/skills/test_issue_create_question_scenarios.py` make `read_notes` and `questions_for` honor the template rule that an item under Contradictions counts only when it carries all three parts (a category, the user's own words in quotes or the flag as passed, and conflicting evidence); a line missing any part belongs under New material (`src/superclaude/skills/sc-issue-protocol/templates/draft-notes.md:7,13`). Take the four category names from the shipped rule text at test time (the `CONFLICT_CATEGORIES` constant at `tests/skills/test_issue_protocol.py:1337-1342` names them), not from a new literal list.

Add the scenarios:
- one test per category (reversed choice, dropped requirement, changed flag, user-stated fact contradicted by verified code), each a notes file with exactly one complete item, asserting exactly one question
- a contradiction line missing its quoted user words, one missing its evidence and one missing its category: each is treated as New material, so zero questions
- a preserved user flag: a worker's disagreement with a supplied `--mode` or `--type` is written as an ordinary New material line, or as a Contradictions line without the user's quoted words, so zero questions; also assert that the sentence the rule cites for this case, "The issue is filed with the user's flags when the user gave them", exists in `src/superclaude/skills/sc-issue-protocol/refs/create.md` Wave 2, and that `src/superclaude/skills/sc-issue-protocol/refs/create.md` Wave 5 step 7 (the pushback comment, about line 98) still posts a disagreement after creation
- the secret-material exception: a Contradictions item that names a place and never a value (for example "secret-looking value in the Fix approach section, value left out") counts as one question even though it quotes no user words, because `src/superclaude/skills/sc-issue-protocol/refs/create.md:59` and `src/superclaude/skills/sc-issue-protocol/templates/draft-notes.md:13` say so; the test reads both files and asserts that both carry the exception sentence

Acceptance criteria:
- The module has separate test ids for each of the four categories, the three incomplete-line cases, the preserved-flag case and the secret-material case.
- The preserved-flag test fails when the cited Wave 2 sentence or the Wave 5 step 7 pushback is removed from a copy of `refs/create.md`.
- The secret-material test fails when the exception sentence is removed from a copy of either file.
- `uv run pytest tests/skills/test_issue_protocol.py tests/skills/test_issue_create_question_scenarios.py -q` passes and the existing 17 selected tests of `tests/skills/test_issue_protocol.py` (`-k "contradiction or draft_notes or create_question or additions or evidence"`) still pass unchanged.
- The module docstring states plainly that these tests check the notes contract and the counting rule as written, and do not prove that a model follows the rule; the controlled runs of Phase 3 do that.

## Phase 2: Controlled-run harness

## Task 4: Settle how a controlled create run loads the revised skill, observes questions and blocks every write

Write `./artifacts/harness-feasibility.md`. Establish and record, with the commands and their output:
- the exact `claude` options available for a non-interactive run with a streamed event log (read `claude --help` of the installed version): print mode, the output and input stream formats, permission mode, tool allow and deny lists, extra directories and any option that loads skills, agents or a plugin from a given directory
- how the `src/` copy of `sc-issue-protocol`, of `issue-worker-t1`, `issue-worker-t2` and `issue-worker-t3`, and of `src/superclaude/commands/issue.md` gets loaded for a run while the user's installed copy is left alone; list the options considered (a temporary home or config directory seeded from `src/`, a plugin directory) and pick one; installing into the real user directory is not an option
- how an `AskUserQuestion` call shows up in the event log (a tool-use event named `AskUserQuestion`), whether the run can supply an answer (for example a hook answering it), and what a run does when no answer comes; if no answer can be supplied, say so, because then the runs can evidence only the question count and not the application of the answer
- how real `gh` is made unusable in a run: an empty `GH_CONFIG_DIR`, `GH_TOKEN` and `GITHUB_TOKEN` unset, the fake `gh` first on `PATH`; and that the run directory is a local clone of the worktree whose `origin` URL is `https://github.com/IronbellyOrg/IronClaude` (the protocol reads it, and no push is ever made)
- that `src/superclaude/skills/sc-issue-protocol/scripts/` holds no `create_issue.py` (the synthetic false fact of Task 7 depends on it), by listing the folder
- the sha256 of each `src/` file that a run must load, so every run record can show which copy it used

Acceptance criteria:
- `./artifacts/harness-feasibility.md` exists and answers each bullet above with a command and its real output, not a guess.
- It ends with a decision section naming the chosen loading option, the observation method for questions, whether an answer can be supplied, and the stop conditions (what makes a run abort).
- A bullet the environment cannot answer is written as "not available here" with the reason, and the decision section says what that limits.

## Task 5: Build the fake gh and the run script under artifacts and prove they block writes

Depends on: Task 4

Create `./artifacts/harness/fake_gh.py` (a stand-in `gh` executable) and `./artifacts/harness/run_create.py` (the run script), following the decisions of `./artifacts/harness-feasibility.md`.

The fake `gh` appends one JSON line per call (arguments, time) to a log file named by an environment variable. It answers the read calls the create protocol makes with canned, clearly synthetic output: `auth status` succeeds, the repo label list holds `enhancement` and `bug`, the issue types include Feature and Bug, the organization issue-fields lookup lists a Complexity field with its options, the duplicate search returns nothing, and an issue view or field read-back returns the values a prior fake create stored. It answers `issue create` with a fake URL on a number that does not exist as a real issue, and answers `issue comment`, `issue edit` and any `api` call with a method other than GET by logging and returning success. It never runs a real `gh`, never opens a network connection and exits non-zero with a clear message for any call it does not know, so an unexpected call is visible.

The run script takes a run name, a depth, the flags, the description and an output directory. It prepares the isolated run directory and environment of the feasibility decision, runs `/sc:issue --create` with the given arguments in print mode with the event log streamed to a file, and writes into the output directory: the event log, the fake `gh` call log, the run directory's `.dev/issues` tree (`issue-body.md`, `draft-notes.md`, `flags.md`, `scout.md`), the final output text, the loaded-file sha256 list, and a `summary.json` with the counts it can compute (questions asked, `issue create` calls, `issue comment` calls, other write-like `api` calls, calls the fake did not know). Add a `--self-test` mode that makes no model call.

Acceptance criteria:
- `uv run python ./artifacts/harness/run_create.py --self-test` exits 0 and its output, saved to `./artifacts/harness/self-test.txt`, shows that an `issue create`, an `issue comment`, an `api -X POST` and an `issue edit` call each landed in the log and were not forwarded, that an unknown call exits non-zero, and that real `gh` cannot authenticate in the run environment.
- The self-test shows that the loaded-file sha256 list equals the `src/` hashes of Task 4 and differs from the installed user copy for `refs/create.md`.
- No file under `src/` or the user's home skills, agents or commands folders is modified by the harness (assert it by comparing a hash list before and after the self-test).

## Phase 3: Controlled create runs

## Task 6: Run the quick-depth create scenarios and record their counts

Depends on: Task 5

Use `./artifacts/harness/run_create.py` for two runs at `--depth quick`, each with an output directory under `./artifacts/runs/`:
- `quick-additions-only`: description "Feature: make `superclaude install` print, as its last line, how many skills it copied." with `--mode feature --type cli --depth quick`. It states no choice, flag-value or fact that the draft could contradict, so zero questions are expected and any assumption the worker adds is an addition.
- `quick-contradiction`: description "Bug: `/sc:issue --create` crashes in `src/superclaude/skills/sc-issue-protocol/scripts/create_issue.py` when the description is empty." with `--mode bug --type skill --depth quick`. That file does not exist (checked in Task 4), so a supported contradiction of a user-stated fact is expected and exactly one question.

For each run record the observed numbers whatever they are. If a run differs from the expectation, keep the record and note it as a finding for the lead; do not edit the skill, the template or the tests in this plan to make a run come out as expected. If a run needs one repeat because of an infrastructure failure (not a model choice), repeat it once and record both.

Acceptance criteria:
- `./artifacts/runs/quick-additions-only/summary.json` and `./artifacts/runs/quick-contradiction/summary.json` exist with the question count, the `issue create` count and the `issue comment` count taken from the event log and the fake `gh` log.
- Each run directory holds the event log, the fake `gh` call log, `issue-body.md`, `draft-notes.md` and the final output, so a reader can recount from raw files.
- For the additions run: the question count, whether every item under New material appears in the issue body and in the final output (`kept without approval:` lines), and whether the body was shown for approval are recorded.
- For the contradiction run: the question count, whether the question names the contradicted item, and whether the answer was applied before the `issue create` call (or, if no answer could be supplied per Task 4, an explicit "not evidenced" line) are recorded.
- No call in either fake `gh` log is an unknown call, and no real GitHub write happened (the real `gh` was unusable by construction).

## Task 7: Run the standard-depth create scenarios and record their counts

Depends on: Task 5

Use `./artifacts/harness/run_create.py` for three runs, each with an output directory under `./artifacts/runs/`:
- `standard-additions-only`: the quick additions description with `--mode feature --type cli --depth standard`.
- `standard-contradiction`: the quick contradiction description with `--mode bug --type skill --depth standard`.
- `standard-flag-preserved`: description "Feature: make `superclaude install` print, as its last line, how many skills it copied." with `--mode bug --type cli --depth standard`, all three flags given, so the standard flag check can disagree with `--mode bug`.

For each run record the observed numbers as in Task 6. For the preserved-flag run additionally record whether the filed issue (the `issue create` arguments in the fake `gh` log) used the user's `--mode bug` choice (the Bug title prefix, the Bug type and the `bug` label), whether the question count is zero, and whether a pushback comment (`issue comment` with `create-review.md`) was posted as a separate call after the create call.

Acceptance criteria:
- Three run directories exist under `./artifacts/runs/` with the same file set as Task 6, each with a `summary.json`.
- The preserved-flag run record states, from the fake `gh` log, the title prefix and labels the issue was created with and the number of `issue comment` calls.
- Any difference from the expected counts (zero questions for the additions and preserved-flag runs, one for the contradiction run) is recorded as a finding with the raw file that shows it.

## Task 8: Run the deep-depth create scenarios and record their counts

Depends on: Task 5

Use `./artifacts/harness/run_create.py` for three runs with the same descriptions and expectations as Task 7 but `--depth deep`, with output directories `deep-additions-only`, `deep-contradiction` and `deep-flag-preserved` under `./artifacts/runs/`. Deep runs use `issue-worker-t1`, which falls back to `issue-worker-t2` when the tier is not served; record which worker handled each run, from the notes or flags file line the fallback writes.

Acceptance criteria:
- Three run directories exist under `./artifacts/runs/` with the same file set as Task 6, each with a `summary.json` and the worker that handled it.
- The same per-scenario facts as Tasks 6 and 7 are recorded, and the deep adversarial flag check (a flag file for the user variant and one for the independent variant, when all flags are given) is noted for the preserved-flag run.
- Any run that tried an unknown `gh` call or an uninterceptable write stops the whole matrix and is reported to the lead before another run starts.

## Phase 4: Evidence summary and criterion verdicts

## Task 9: Write the evidence matrix and the criterion-by-criterion verdict with file and line

Depends on: Task 3, Task 6, Task 7, Task 8

Write `./artifacts/evidence-matrix.md` with two parts.

Part one is the run matrix: one row per controlled run (quick, standard and deep by additions-only, contradiction and, at standard and deep, preserved flag) giving the expected and the observed question count, the `issue create` count, the `issue comment` count, the worker that handled the run, whether additions were retained in the body, the notes and the final output, whether the user flag was honored, and the path of its raw record. Add one row for the secret-material exception that says it is evidenced by the fixture test of Task 3 only and had no controlled run, with the reason (a controlled run would put a fake secret into a model prompt and would add cost without testing more than the fixture does). Count questions and posts only from the event log and the fake `gh` log.

Part two is the verdict for each of the six acceptance criteria of the issue (the text of the issue is quoted in `./source.md` through the summary: additions-only runs ask nothing, one combined question for contradictions with the answer applied before posting, the notes template separates and defines, the sources agree and the claim and plan-approval boundary are unchanged, regression coverage, and the gates plus the monitored pull request). For each, state one of delivered by 852, delivered by this work, or not met, and cite the file and line: the existing rule, template, command, docs and static tests at `src/superclaude/skills/sc-issue-protocol/refs/create.md:84-86`, `src/superclaude/skills/sc-issue-protocol/templates/draft-notes.md:3-15`, `src/superclaude/commands/issue.md:19,85`, `docs/designs/sc-issue-command.md:223-225,460`, `docs/user-guide/commands.md:357` and `tests/skills/test_issue_protocol.py:1335-1526`, and the new tests and run records of this work. Say plainly that the secret-material exception is a qualification of the first and third criteria, and that a criterion whose evidence rests on a run that could not supply an answer is "partly evidenced".

Acceptance criteria:
- `./artifacts/evidence-matrix.md` holds a matrix row for each executed run and the secret-material row, and each count in it can be recomputed from the cited raw file.
- Each of the six criteria has a verdict and at least one `path:line` citation that was read in this work, and no criterion is marked delivered on the strength of a static wording test alone when it asks for behavior.
- The document ends with a short list of findings for the lead (runs that differed from expectation, the closed state of the issue on GitHub, the secret-material qualification), each with its evidence path.

## Phase 5: Gates and pull request notes

## Task 10: Run the verification gates and record their real results

Depends on: Task 3, Task 9

From the repository root run, and record command, exit code and the summary lines in `./artifacts/gates.md`: the focused selection (`uv run pytest tests/skills/test_issue_protocol.py tests/skills/test_issue_create_question_scenarios.py tests/commands/test_issue_command.py -q`), the full suite (`make test`), the linter (`make lint`) and the sync check (`make verify-sync`). If the full suite shows a failure, determine from the failing test names whether it involves any file this work changed, and record that; do not hide, skip or relax a failing test, and do not change `src/` to make a gate pass.

Acceptance criteria:
- `./artifacts/gates.md` lists the four commands with their actual exit codes and pass, fail and skip counts as printed.
- A failing gate is reported with the failing test ids and whether each is connected to the changed files; a gate that could not run is reported as not run with the reason.
- `git status` after the gates shows no file changed under `src/` and nothing staged under `.claude/` or `.dev/issues/`.

## Task 11: Write the pull request notes with the Refs or Fixes decision

Depends on: Task 9, Task 10

Write `./artifacts/pr-notes.md` for the story agent to use in `/sc:pr-submit --monitor 3 --head <branch> --base integration`. It holds a conventional-commit title (type `test`, scope `issue`, mentioning issue 834), a body that quotes the story's decided-for-this-work block (the base branch is `integration`; pull request 852 already merged and delivered the rule, template, command, docs and static tests; there is no open pull request to continue), the six-criterion verdict table of Task 9, the controlled-run matrix in short form, the gate results, and the findings for the lead. State the closing keyword decision: `Refs #834` unless Task 9 marks every criterion delivered with run evidence, in which case say which criteria that is and leave `Fixes #834` to the lead, because the issue is already closed on GitHub. Check whether the Generator-Constraint rule of the repository's CI (a pull request that touches a gate or validator file needs a "## Generator-Constraint Considered" section in its body) applies to the files this work touches, and include the section if it does.

Acceptance criteria:
- `./artifacts/pr-notes.md` exists with a title, a body and the closing keyword line, and states which criteria the pull request does and does not deliver.
- The body mentions no live issue creation and says every GitHub call in the runs went to the fake `gh`.
- The note on the Generator-Constraint rule says whether it applies and why, from the files in `git diff --name-only origin/integration`.
```

### src/superclaude/skills/sc-issue-protocol/refs/create.md:84-86

```markdown
### Contradiction prompt rule (default D14)

Ask only when `draft-notes.md` lists a supported contradiction of the user's own description, instruction or flag: reversed choice, dropped requirement, changed flag, or a user-stated fact contradicted by verified code (each with the user's own words and the conflicting evidence). Empty notes, or notes with only `None` under both headings, ask zero questions and Wave 5 posts. One or more supported contradiction items ask exactly one question (AskUserQuestion), once per run, naming every item, with the choices "keep my wording" (change the draft to honor the user's words), "keep the draft" (accept the draft's change) and "edit". Apply the answer to `<D>/issue-body.md` before Wave 5; it changes only the contradicted items. Every New material item, assumptions included, stays in the body and in `draft-notes.md` whatever the answer, and is listed in the final output. A worker's disagreement with a supplied flag is not a contradiction when the issue is filed with the user's flag (Wave 2, line "The issue is filed with the user's flags when the user gave them"); it stays the pushback comment of Wave 5 step 7. The full body is never shown for approval (B1).
```

## Coverage slice

| Requirement / Task | Card ID | Status | Grounding |
|---|---|---|---|
| INF-001 (source.md:11) | Task 9 (best containment 0.4231) | unmapped | source.md:11 |
| INF-002 (source.md:11) | Task 9 (best containment 0.2857) | unmapped | source.md:11 |
| INF-003 (source.md:11) | Task 11 (best containment 0.4167) | unmapped | source.md:11 |
| INF-004 (source.md:23) | Task 3 (best containment 0.5385) | unmapped | source.md:23 |
| INF-005 (source.md:26) | Task 9 (best containment 0.4615) | unmapped | source.md:26 |
| INF-006 (source.md:27) | Task 4 (best containment 0.6667) | covered | source.md:27 |
| INF-007 (source.md:35) | Task 2 (best containment 0.3333) | unmapped | source.md:35 |
| INF-008 (source.md:43) | Task 3 (best containment 0.68) | covered | source.md:43 |
| INF-009 (source.md:43) | Task 9 (best containment 0.5185) | unmapped | source.md:43 |
| INF-010 (source.md:43) | Task 11 (best containment 1.0) | covered | source.md:43 |
| INF-011 (source.md:43) | Task 11 (best containment 0.8) | covered | source.md:43 |
| INF-012 (source.md:43) | Task 11 (best containment 0.7778) | covered | source.md:43 |
| INF-013 (source.md:45) | Task 11 (best containment 0.75) | covered | source.md:45 |
