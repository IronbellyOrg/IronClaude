---
schema: workflow-plan/1.2
source: ./source.md
strategy: systematic
depth: standard
slug: TASK-WF-brainstormFixBri-20261106-113538
version: "1"
priority: Medium
created_date: "2026-11-06"
---

# Brainstorm: nested analyze folder only when /sc:analyze ran (plan from the amended brief)

Source: ./source.md
Goal: `/sc:brainstorm` under `--unattended` says, in its skill, its command file and its routing ref, that the nested `analyze` directory is written only by a `/sc:analyze` call, and that the auggie scan and the `fallback_1` scan (codegraph, then Glob and Grep) write no nested directory and no nested contract. Tests pin both halves of that rule, and the worker-contract spec carries a live-check sentence that requires the folder only after an actual `Skill` call to `sc:analyze`, never by `quality_tier`.

## Constraints

- Background: the P1 live check lc10 failed because the codebase-enrichment wave ran on `quality_tier: fallback_1` (the auggie tool was not available in the worker session) and wrote no `nested/analyze-1/` directory, while the live plan expected one. The owner decided on 2026-11-05 that the check wording was wrong, not the worker. The archived record is in `.dev/tasks/done/TASK-WF-p1LivePlanBrief-20261105-164506/` (`artifacts/lc10-result.md`, `artifacts/p1-owner-decisions-20261105.md`); those files are read, never edited.
- This plan replaces two earlier plans for the same work, packages `TASK-WF-brainstormFixBri-20261106-001016` and `TASK-WF-brainstormFixBri-20261106-021737`. An independent review found the first not ready to run (its Task 6 wording decided the nested folder by `quality_tier`, its Task 7 status check could not pass on the current tree, and the owner rule was not fully pinned). A second review found that the second plan's live-check sentence required the folder whenever any `Skill`, `Agent` or `Task` call passed the flag text, so a `Task` prompt followed by an auggie or `fallback_1` scan would fail a correct run; the owner amended the brief's Part 4 on 2026-11-06 and this plan carries the amended text. Both earlier packages are left as they are.
- Edit only these six files: `src/superclaude/skills/sc-brainstorm-protocol/SKILL.md`, `src/superclaude/skills/sc-brainstorm-protocol/refs/handoff-routing.md`, `src/superclaude/commands/brainstorm.md`, `tests/skills/test_brainstorm_protocol.py`, `tests/skills/test_worker_contract.py` and `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`. `make sync-dev` also rewrites the gitignored copies under `.claude/`; those are output, not edits, and are never staged.
- `src/superclaude/` is the source of truth. `plugins/superclaude/commands/brainstorm.md` is a copy that already differs from the `src` file, and no test requires the two to match (`tests/commands/test_routing_plugin_parity.py` covers only the `sc-recommend` skill). It is not edited. This is this plan's resolution of spec open item 8 for `brainstorm.md`. Task 7 confirms nothing under `plugins/` changed.
- No new text in the installed files (the skill, its refs, the command file) may name a `src/superclaude/` path or an Orca command; `tests/skills/test_worker_contract.py` (`_check_unattended_section`) fails on both.
- UV for every Python command: `uv run pytest ...`, `uv run python ...`. Test runs use `-p no:cacheprovider` and `PYTHONDONTWRITEBYTECODE=1`. No `superclaude install` (the owner updates the installed copies under `~/.claude/` later). No git commit, push, merge or PR.
- The edits reach the next live plan only after the owner commits and merges them; this plan does not commit.
- Open conflict, no change planned here: from phase P2 brainstorm's research enrichment also passes a nested report directory, and the research-deep fallback is itself a nested command. The corrected wording covers only the codebase-enrichment wave. This is an open conflict for the owner and the P2 live-plan author.
- Starting state: the working tree already holds uncommitted edits to `src/superclaude/cli/install_core.py` and `tests/cli/test_how_we_work_install.py` that are not part of this work, and a staged archive of the earlier live plan under `.dev/tasks/done/`. Task 1 records this state before any edit and Task 7 compares against it.

## Phase 1: Say it in the installed primitives

## Task 1: State in the skill that the auggie scan and the fallback tier write no nested directory

First, before any edit, save the output of `git status --porcelain` to `./artifacts/status-before.txt`. Task 7 compares against that file.

In `src/superclaude/skills/sc-brainstorm-protocol/SKILL.md`, the Wave 2A paragraph whose bold lead-in is "Under `--unattended`" (line 195) currently ends: "The codebase row invokes `/sc:analyze` with `--unattended --report-dir <report-dir>/nested/analyze-<n>/` (`<n>` starts at 1); the `mcp__auggie__codebase-retrieval` alternative is unchanged and writes no nested contract. The nested contract is listed in `artifacts`." Replace everything after "(`<n>` starts at 1)" with this exact text, copied character for character:

```text
; the `mcp__auggie__codebase-retrieval` alternative and the `fallback_1` tier (codegraph, then native Glob and Grep, `refs/handoff-routing.md` Tier 2) are unchanged and write no nested directory and no nested contract, so `nested/analyze-<n>/` is written only by a `/sc:analyze` call, and `enrichment_used` does not show whether it exists. The nested contract is listed in `artifacts`, also when the call failed.
```

The wording names the writer (a tool or a tier), never a recorded `quality_tier` or a run. A clean `/sc:analyze` run is also `primary`, and `enrichment_used` records `source` and `quality_tier` as separate fields that do not name the tool, so a statement that depended on the tier would be wrong for an analyze run. It states no tier for any `/sc:analyze` outcome and keeps the nested contract listed unconditionally, a failed call's included. Change nothing else in the file.

Acceptance criteria:
- `./artifacts/status-before.txt` exists and was written before the first edit of this plan.
- The paragraph with the bold lead-in "Under `--unattended`" in the Wave 2A section of `SKILL.md` contains `fallback_1`, `write no nested directory and no nested contract`, ``only by a `/sc:analyze` call``, `nested/analyze-` and `skipped`, ends with "The nested contract is listed in `artifacts`, also when the call failed.", and a regular-expression search for `only for a nested command that r[a]n` finds nothing in it.
- `git diff --stat -- src/superclaude/skills/sc-brainstorm-protocol/SKILL.md` shows one line changed (one insertion, one deletion).
- With `S` set to this package's `source.md` and the command run from the repository root, `X=$(sed -n '231s/.*with: "\(.*\)" Task 1 AC.*/\1/p' "$S")` is non-empty, `grep -cxF -- "$X"` on this plan prints 1, and `grep -cF -- "$X" src/superclaude/skills/sc-brainstorm-protocol/SKILL.md` prints 1.
- `PYTHONDONTWRITEBYTECODE=1 uv run pytest tests/skills/test_brainstorm_protocol.py -q -p no:cacheprovider` still passes before Task 4 changes the tests.

## Task 2: State the same rule in the routing ref for both codebase tiers

In `src/superclaude/skills/sc-brainstorm-protocol/refs/handoff-routing.md`, the "Codebase enrichment" section has two tier lists. The list under `**Tier 1 (primary)**` (line 16) ends with the line `- quality_tier: ` followed by `primary` in backticks (line 22). The list under `**Tier 2 (fallback_1)**: codegraph, then native Glob/Grep` (line 24) ends with the line `- Activation: if Tier 1 returns error OR empty result` (line 31), and the line `**Final fallback**` (line 33) follows it. Add the bullet below, identical text, as the last bullet of each of the two lists: once after the Tier 1 `quality_tier` line, and once after the Tier 2 `Activation` line, both before the next `**Final fallback**` or `**Tier 2` anchor. The Tier 2 bullet must stay inside the span that `tests/skills/test_codegraph_adoption.py` reads in `test_brainstorm_tier2_names_codegraph_files_and_search` (from `**Tier 2 (fallback_1)**: codegraph` to the line starting `**Final fallback`).

```text
- Under `--unattended` this tier writes no nested directory and no nested contract; `nested/analyze-<n>/` is written only by a `/sc:analyze` call (the skill's other codebase action), and the scan is recorded in `enrichment_used` with this tier's `quality_tier`.
```

The bullet names `/sc:analyze` as the only writer so that a reader of this ref alone does not conclude that codebase enrichment never nests. Do not touch the research tiers (line 35 onward) or the `nested/adversarial-` text.

Acceptance criteria:
- `grep -c 'writes no nested directory' src/superclaude/skills/sc-brainstorm-protocol/refs/handoff-routing.md` prints 2 (kept as a smoke check; Task 4 pins each tier separately).
- `git diff --stat -- src/superclaude/skills/sc-brainstorm-protocol/refs/handoff-routing.md` shows two lines added and none deleted; one added bullet follows the Tier 1 `quality_tier` line and the other follows the Tier 2 `Activation` line.
- `PYTHONDONTWRITEBYTECODE=1 uv run pytest tests/skills/test_codegraph_adoption.py -q -p no:cacheprovider` passes with the edit in place.
- With `S` as in Task 1, `X=$(sed -n '232s/.*31): "\(.*\)" .grep.*/\1/p' "$S")` is non-empty, `grep -cxF -- "$X"` on this plan prints 1, and `grep -cxF -- "$X" src/superclaude/skills/sc-brainstorm-protocol/refs/handoff-routing.md` prints 2.

## Task 3: State the same rule in the command file's Unattended mode section

In `src/superclaude/commands/brainstorm.md`, the `## Unattended mode` section has a bullet `**Nested invocations.**` (line 157) that says the `/sc:analyze` codebase enrichment receives `--unattended --report-dir <report-dir>/nested/analyze-<n>/`. Append this text to the end of that bullet, after "so a nested directory is never reused.", copied character for character:

```text
A codebase scan through `mcp__auggie__codebase-retrieval` or through the `fallback_1` tier (codegraph, then Glob and Grep) is not a nested command and writes no nested directory and no nested contract, so `nested/analyze-<n>/` is written only by a `/sc:analyze` call; `enrichment_used` records the scan's tier, which does not show whether that directory exists.
```

Leave the existing sentence "`adversarial_artifacts_dir` and the nested contracts are listed in `artifacts`" unchanged. Do not edit `plugins/superclaude/commands/brainstorm.md`.

Acceptance criteria:
- The `**Nested invocations.**` bullet of `src/superclaude/commands/brainstorm.md` contains `writes no nested directory and no nested contract` and ``only by a `/sc:analyze` call``, and still contains `nested/analyze-`, `nested/adversarial-` and "`adversarial_artifacts_dir` and the nested contracts are listed in `artifacts`".
- `PYTHONDONTWRITEBYTECODE=1 uv run pytest tests/skills/test_worker_contract.py -q -p no:cacheprovider` passes with the edit in place.
- `git diff --stat -- src/superclaude/commands/brainstorm.md` shows one line changed (one insertion, one deletion).
- With `S` as in Task 1, `X=$(sed -n '233s/.*bullet: "\(.*\)" Leave.*/\1/p' "$S")` is non-empty, `grep -cxF -- "$X"` on this plan prints 1, and `grep -cF -- "$X" src/superclaude/commands/brainstorm.md` prints 1.
- `git diff --stat -- plugins` prints nothing.

## Phase 2: Pin the wording with tests

## Task 4: Pin the skill and routing-ref wording in test_brainstorm_protocol.py

Depends on: Task 1, Task 2

In `tests/skills/test_brainstorm_protocol.py`, the test `test_brainstorm_unattended_nested_directories_are_named` starts at line 39. It asserts `nested/analyze-` and `skipped` in the Wave 2A section (`_wave2a_section()`, line 44) and `nested/adversarial-` in `refs/handoff-routing.md` (line 47). Keep every existing assertion unchanged. Add a sibling test next to it, using the file's own helpers (`_wave2a_section`, `_BRAINSTORM`) and, for the routing ref, the slicing pattern of the `_section(text, start, end_pattern)` helper in `tests/skills/test_codegraph_adoption.py` (it splits the text at `start`, then splits the rest at `end_pattern` with `re.M` and keeps the first part). The new test asserts:

- Paragraph slice: take `_wave2a_section()`, split at the bold lead-in ``**Under `--unattended`**``, and keep the text up to the next blank line. The slice contains `fallback_1`, `write no nested directory and no nested contract` and ``only by a `/sc:analyze` call``, and the text `Quality-tier tracking` is not in it, so a slicer that returns the whole section fails.
- Tier slices of `refs/handoff-routing.md` (the file next to the SKILL file): the Tier 1 slice runs from the first `**Tier 1 (primary)**` to the line starting `**Tier 2 (fallback_1)**: codegraph`; the Tier 2 slice runs from there to the line starting `**Final fallback`. Each slice contains `writes no nested directory and no nested contract` exactly once and ``only by a `/sc:analyze` call`` exactly once.

All pins are exact substring checks. On the pre-change text every paragraph-slice pin and every tier-slice pin fails; only the `Quality-tier tracking` absence check passes there, because it guards the slice boundary and not the new wording.

Acceptance criteria:
- `tests/skills/test_brainstorm_protocol.py` contains the new sibling test with the paragraph-slice pins and both tier-slice pins above, and every earlier assertion of `test_brainstorm_unattended_nested_directories_are_named` is unchanged.
- `PYTHONDONTWRITEBYTECODE=1 uv run pytest tests/skills/test_brainstorm_protocol.py -q -p no:cacheprovider` passes.
- `git show HEAD:src/superclaude/skills/sc-brainstorm-protocol/SKILL.md | grep -c 'write no nested directory and no nested contract'` and `git show HEAD:src/superclaude/skills/sc-brainstorm-protocol/refs/handoff-routing.md | grep -c 'writes no nested directory and no nested contract'` both print 0, and `git cat-file -e` exits 0 for both `HEAD:` paths, which shows the shared directory pins fail on the pre-change text.

## Task 5: Pin the command-file wording in test_worker_contract.py

Depends on: Task 3

In `tests/skills/test_worker_contract.py`, `UNATTENDED_EXPECT["brainstorm"]` is the entry that starts at line 286; its `phrases` list opens at line 288 and holds `research enrichment is off`, `exactly as passed`, `never reused`, `nested/analyze-`, `nested/adversarial-` and `dry-run`.

First, before editing, save the output of `PYTHONDONTWRITEBYTECODE=1 uv run pytest tests/skills/test_worker_contract.py -p no:cacheprovider --collect-only -q -k brainstorm` to `./artifacts/t5-collect-before.txt`. Today the summary line reports 17 collected cases, but that number is not a constant; the saved file is the baseline.

Then add the two phrases `writes no nested directory and no nested contract` and ``only by a `/sc:analyze` call`` to that `phrases` list. The removed-token tests (`_removals`, built from `UNATTENDED_EXPECT`) pick up both phrases and add one case for each; do not add a separate mutation by hand. The mutation list near line 711 (lines 704 to 724) rewrites a made-up section and does not read the real brainstorm text, so it needs no change.

Acceptance criteria:
- `UNATTENDED_EXPECT["brainstorm"]["phrases"]` in `tests/skills/test_worker_contract.py` contains `writes no nested directory and no nested contract` and ``only by a `/sc:analyze` call``.
- The collect-only command above, run again after the edit, reports a collected count equal to the count in `./artifacts/t5-collect-before.txt` plus 2; the plan does not hard-code that number.
- `PYTHONDONTWRITEBYTECODE=1 uv run pytest tests/skills/test_worker_contract.py -q -p no:cacheprovider` passes.
- `git show HEAD:src/superclaude/commands/brainstorm.md | grep -c 'writes no nested directory and no nested contract'` prints 0, and `git cat-file -e HEAD:src/superclaude/commands/brainstorm.md` exits 0, which shows the new phrase fails on the pre-change command file.

## Phase 3: Record the corrected live-check wording

## Task 6: Add the corrected wording to the worker-contract spec in two places

In `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` make two edits, each on one existing line.

First, the section 2.1 bullet `**Nested propagation rule**` (line 62) ends with "Each command's `## Unattended mode` section names its nested invocations." Append this sentence to that line, copied character for character:

```text
A nested directory `nested/<command>-<n>/` exists only for a nested command that actually ran, a run that failed included; a command that does the same work through a tool or a native-search fallback (brainstorm's codebase scan through `mcp__auggie__codebase-retrieval`, or through codegraph, then Glob and Grep) writes no nested directory and records the tier it used in its own contract, and brainstorm's live-check extra for this is in 7.2 step 4.
```

Second, section 7.2 step 4 is the line that begins "4. Check the contract (PyYAML is a declared dependency" (line 286) and ends "At P0, AC-0.4 replaces this step." The fenced shell block for that step follows on the next lines and is not edited. Append this sentence to the end of the step 4 line, copied character for character:

```text
A live-check extra for brainstorm's codebase-enrichment wave reads: "when the brief passes `--codebase`, or the contract's `domain` is `code`, `architecture` or `incident` and the brief does not pass `--no-codebase`, `enrichment_used` holds a `source: codebase` entry; every `nested/analyze-<n>/return-contract.yaml` that exists is listed in `artifacts`; a `nested/analyze-<n>/` directory is required, and must then hold its own `return-contract.yaml` with every `artifacts` entry under it existing, only when a `Skill` tool call (not a `Task` or `Agent` call whose prompt only names `/sc:analyze`) in the worker's session file or in one of its subagent files (7.2 step 5) invokes `sc:analyze` with `--report-dir <report directory>/nested/analyze-<n>/` and a number for `<n>` and returns no tool error, the `codebase` entry is not `skipped` (the per-source enrichment timeout records `skipped` and can stop `/sc:analyze` before it writes) and `/sc:analyze` did not refuse that directory, because neither `quality_tier` nor `source` records whether `/sc:analyze` ran; when the session file is not verifiable, this last clause is recorded `not verifiable`, never PASS" (P1 check lc10 is the origin of this rule).
```

Placement and wording are a Necessary deviation from the brief, recorded here. The brief allows either the live-check section or a note in the P1 rows, and sketches the wording as "a fallback_1 or auggie primary scan is recorded as the tier used with no nested folder". This plan puts the live-check sentence in 7.2 step 4 because every later live plan attaches its step-4 extras there, and sections 7.2 and 7.3 hold no per-command extras list of their own, so the P2 live-plan author reads 7.2 step 4. The wording departs from the sketch because tier does not decide whether the folder must exist: a clean `/sc:analyze` run is also `primary`, and neither `quality_tier` nor `source` names the tool. The trigger is an actual `Skill` call that invokes `sc:analyze`, because a `Task` or `Agent` prompt that only names the command can be followed by an auggie or `fallback_1` scan that writes no folder. The whole-text check in the acceptance criteria is required by the brief's rule that each correction's verifier has an equivalent check; it is not one of the pins correction F-7 lists. Task 6's second acceptance criterion also checks that the old trigger wording ``a `Skill`, `Agent` or `Task` tool call`` is gone; this goes beyond the pins correction F-7 lists, on purpose, because three of the four positive pins are also in the old sentence.

Residual risks of the live-check sentence are left in place on purpose; all are in the false-PASS direction, and the sentence has no known false FAIL on a correct run:
- A `/sc:analyze` call made without the nested `--report-dir` (a broken propagation, itself a defect) is not seen, so its missing folder passes. Related: INV-022 (no live check can force the analyze route).
- The required-directory clause sees only a `Skill` tool call that invokes `sc:analyze`. The spec's nested propagation rule (spec:62) names the Skill tool, but how the session file records the invoked command, its arguments and a tool error is INFERRED from Claude Code's session format (spec:302 says only "`tool_use` blocks with a `name`"); a `/sc:analyze` run made another way, or recorded under another name, is missed and its missing folder passes.
- The `skipped` carve-out also exempts an invoked `/sc:analyze` that wrote nothing and was recorded `skipped` for a reason other than the timeout, and, because `enrichment_used` holds one `codebase` entry, it exempts every `nested/analyze-<n>/` call of the run at once.
- The required-folder clause depends on the session file; when it is missing or ambiguous the clause is `not verifiable`, and spec:300 then blocks a PASS until the owner accepts the gap in writing (accepted by design, INV-023).
- An `artifacts` entry under a directory that is not required (a `skipped`, refused or tool-error call) is not checked for existence; Task 1's "also when the call failed" produces exactly this case.

Leave the `brainstorm` row of the section 3.1 table (line 142) and everything else in the spec as it is.

Acceptance criteria:
- The `**Nested propagation rule**` bullet in section 2.1 contains `only for a nested command that actually ran` and `7.2 step 4`.
- The section 7.2 step 4 line contains `lc10`, ``a `source: codebase` entry``, ``neither `quality_tier` nor `source` records`` and ``invokes `sc:analyze` ``, and does not contain ``a `Skill`, `Agent` or `Task` tool call``.
- `git diff --stat -- .dev/orca-command-refactor/specs/orca-worker-contract-spec.md` shows two lines changed (two insertions, two deletions), and `git diff -U0` on that file shows hunks only at the section 2.1 bullet and the section 7.2 step 4 line.
- With `S` as in Task 1, `X=$(sed -n 223p "$S")` and `Y=$(sed -n 219p "$S")` are non-empty, `grep -cxF` on this plan prints 1 for each, and `grep -cF` against `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` prints 1 for each.

## Phase 4: Dev copies and final checks

## Task 7: Sync the dev copies, run the affected tests and lint, and compare the tree against its starting state

Depends on: Task 1, Task 2, Task 3, Task 4, Task 5, Task 6

Run `make sync-dev` and then `make verify-sync` from the repository root so the gitignored copies under `.claude/` match `src/superclaude/`. Then run `PYTHONDONTWRITEBYTECODE=1 uv run pytest tests/skills/test_brainstorm_protocol.py tests/skills/test_worker_contract.py tests/skills/test_codegraph_adoption.py tests/skills/test_tier2_tavily_consistency.py tests/commands/test_routing_plugin_parity.py -q -p no:cacheprovider` and `make lint` (which runs `lint-architecture` and then `uv run ruff check .`). Save the outputs to `./artifacts/t7-sync.log`, `./artifacts/t7-pytest.log` and `./artifacts/t7-lint.log`, and save the output of `git status --porcelain` to `./artifacts/status-after.txt`. Append the line `exit=<status>` after each command's output in its log. Do not edit any source file in this task; it writes only the logs under `./artifacts/`. The status snapshot `./artifacts/status-after.txt` is the one non-log file it writes there, and `make sync-dev` rewrites the gitignored copies under `.claude/` (output, not edits).

Acceptance criteria:
- `./artifacts/t7-sync.log` shows `make sync-dev` and `make verify-sync` both exiting 0.
- `./artifacts/t7-pytest.log` shows the five test files passing with no failure, including `tests/skills/test_codegraph_adoption.py` and `tests/skills/test_tier2_tavily_consistency.py`, and `./artifacts/t7-lint.log` shows `make lint` exiting 0 with no new ruff finding in the two edited test files.
- Every line that is in `./artifacts/status-after.txt` and not in `./artifacts/status-before.txt` names one of the six files in Constraints or a path under this package's folder; no such line names a path under `.claude/` or `plugins/`; and every line of `./artifacts/status-before.txt` that names a path under `.dev/tasks/done/` is unchanged in `./artifacts/status-after.txt`.
