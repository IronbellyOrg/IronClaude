## T1 card excerpt

Persona lens: analyzer (root-cause and deviation). This is a PRE-execution audit: the work under audit is the PLAN (plan_path below) and the driving spec is the SPEC (spec_path below). Find where the plan omits, contradicts or goes beyond the spec, and where a task as written cannot be carried out or cannot pass its own acceptance criteria. Ground every finding at file:line.

spec_path: /home/coder/workspaces/worktrees/IronClaude/issue-834-rest/.dev/tasks/to-do/TASK-WF-issueSummary-20261126-132314/source.md
plan_path: /home/coder/workspaces/worktrees/IronClaude/issue-834-rest/.dev/tasks/to-do/TASK-WF-issueSummary-20261126-132314/TASK-WF-issueSummary-20261126-132314.md
diff_scope: none (pre-execution)


- C1 (Grounded). The plan has a task for each part of the scope change: scenario tests (Tasks 1 to 3, plan lines 29-83), the controlled-run harness and runs (Tasks 4 to 8, plan lines 85-161), the evidence and verdict (Task 9, plan line 163), the gates (Task 10, plan line 180) and the pull request notes (Task 11, plan line 191). The spec asks for exactly these in source.md:43.
- C2 (Grounded). Tasks 1 to 3 put a counting function `questions_for` inside the new test module (plan line 47). The spec warns against "a second copy of the decision rule that only tests itself" (source.md:35). The plan reduces that risk with a rule-text agreement test (Task 2) and a docstring that says the tests check the notes contract and not model behavior (Task 3). The residual risk: acceptance criterion 5 ("regression coverage exercises ... notes") is met in CI only at the notes-contract level, and the behavioral evidence of Tasks 6 to 8 is one-off, not repeatable.
- C3 (Grounded). Task 3 asserts that `refs/create.md` holds the sentence "The issue is filed with the user's flags when the user gave them". It does: src/superclaude/skills/sc-issue-protocol/refs/create.md:38 (Wave 2), and the rule at create.md:86 cites it.
- C4 (Grounded). The 17 existing focused tests that Task 3 must keep passing do pass today: `uv run pytest tests/skills/test_issue_protocol.py -k "contradiction or draft_notes or create_question or additions or evidence"` printed "17 passed, 186 deselected".
- C5 (Grounded). Task 6 and Task 7 rely on `create_issue.py` not existing: src/superclaude/skills/sc-issue-protocol/scripts/ holds only clickup_claim.py, orca_worktree.py and origin_repo.py.
- C6 (Grounded). The plan states that the installed user copy of the skill differs from src/ (plan line 23) and tells the runs to load the src/ copy. The installed copy does differ (a recursive diff of ~/.claude/skills/sc-issue-protocol against src/superclaude/skills/sc-issue-protocol lists SKILL.md, refs/claim.md, refs/create.md and templates/draft-notes.md).
- C7 (INFERRED). Tasks 6 to 8 are eight model runs, each with a worker that runs a codebase analysis, and the plan sets no time or cost ceiling for them. The only abort rule is an unknown `gh` call (plan line 159).
- C8 (INFERRED). If Task 4 finds that questions cannot be observed or writes cannot be blocked, the plan does not say that Tasks 5 to 8 stop and the lead is told. The spec says the estimate "must be revisited" in that case (source.md:35); the plan only says the decision section "says what that limits" (plan line 98).


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

### .dev/tasks/to-do/TASK-WF-issueSummary-20261126-132314/TASK-WF-issueSummary-20261126-132314.md:17-26

```markdown
## Constraints

- Pull request 852 already delivered the rule text (`src/superclaude/skills/sc-issue-protocol/refs/create.md:84-86`), the notes template (`src/superclaude/skills/sc-issue-protocol/templates/draft-notes.md`), the worker guidance, the command and docs text, and the static wording tests (`tests/skills/test_issue_protocol.py:1335-1526`). Do not redo or reword any of them. Keep every existing test as it is.
- The secret-material exception (`src/superclaude/skills/sc-issue-protocol/refs/create.md:59` and `src/superclaude/skills/sc-issue-protocol/templates/draft-notes.md:13`) is deliberate: a would-be secret is listed under Contradictions and causes the one question. Record it as a qualification; never remove it and never describe the rule as "only the four categories" without it.
- No production decision code and no new command flag: the question decision stays prose that the orchestrating model follows. The tests and the harness are test and evidence tooling only. Nothing under `src/superclaude/` changes in this plan.
- No live test issues and no GitHub writes of any kind. Every `gh` call in a controlled run goes to a fake `gh` that logs it and never forwards it. Synthetic values only; never a real credential, token or text from the environment files.
- The installed user copy of the skill and of the three issue workers differs from `src/` (it is the pre-852 version: its `SKILL.md`, `refs/create.md`, `refs/claim.md`, `templates/draft-notes.md` and the three `issue-worker-t*.md` files differ). Controlled runs must load the `src/` copy. Never modify the user's installed copy to do that.
- Base branch is `integration`. The pull request is opened with `Refs #834` unless it delivers every acceptance criterion of the issue. The issue itself was closed on GitHub on 2026-11-26 (13:14 UTC); reopening it is the lead's decision, not this plan's.
- Never stage or commit anything under `.claude/` or `.dev/issues/`.

```

### .dev/tasks/to-do/TASK-WF-issueSummary-20261126-132314/TASK-WF-issueSummary-20261126-132314.md:43-83

```markdown
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
```

### .dev/tasks/to-do/TASK-WF-issueSummary-20261126-132314/TASK-WF-issueSummary-20261126-132314.md:85-115

```markdown
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
```

### .dev/tasks/to-do/TASK-WF-issueSummary-20261126-132314/TASK-WF-issueSummary-20261126-132314.md:117-161

```markdown
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
```

## Coverage slice

| Requirement / Task | Card ID | Status | Grounding |
|---|---|---|---|
| INF-002 (source.md:11) | Task 9 (best containment 0.2857) | unmapped | source.md:11 |
| INF-003 (source.md:11) | Task 11 (best containment 0.4167) | unmapped | source.md:11 |
| INF-004 (source.md:23) | Task 3 (best containment 0.5385) | unmapped | source.md:23 |
| INF-005 (source.md:26) | Task 9 (best containment 0.4615) | unmapped | source.md:26 |
| INF-006 (source.md:27) | Task 4 (best containment 0.6667) | covered | source.md:27 |
| INF-007 (source.md:35) | Task 2 (best containment 0.3333) | unmapped | source.md:35 |
