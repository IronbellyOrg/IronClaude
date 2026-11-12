---
schema: workflow-plan/1.2
source: ./source.md
strategy: systematic
depth: quick
slug: TASK-WF-removeNineWordin-20261112-002102
version: "1"
priority: Medium
created_date: "2026-11-12"
---

# Remove nine wording ambiguities from the codegraph instructions of /sc:analyze and /sc:design

Source: ./source.md
Goal: The codegraph instructions in the analyze command, the design command and the shared guide say, in one clause or sentence each, what the smoke test found unclear (nine items), with tests that fail if any fix is reverted, and no change to behaviour, flags or the four standing rules.

## Constraints

- Edit only `src/superclaude/commands/analyze.md`, `src/superclaude/commands/design.md`, `src/superclaude/core/CODEGRAPH.md`, `plugins/superclaude/core/CODEGRAPH.md` (a test pins it byte-identical to the source), `tests/skills/test_codegraph_adoption.py` and `tests/core/test_codegraph_guide.py`. The plugin twins of analyze.md and design.md already differ from the source (no codegraph text, `mcp-servers: []`) and no test pins them, so they stay untouched. `scripts/eval_workflow_vs_task_builder.py` pins skill tool lists, which this plan does not change, so it stays untouched unless a test run shows otherwise.
- Do not change behaviour, flags, the one-check-per-run rule, the fresh-and-`access: mcp` rule, the Grep/Read floor or the never-halt rule. Every fix is a clause or one sentence.
- `src/superclaude/core/CODEGRAPH.md` is shared by every primitive: additive clarifications only; it stays at 120 lines or fewer, names no `src/superclaude/` path, adds no `graph:*` token outside the closed list of its section 3 (which already holds `graph:empty` and `graph:truncated`), and names `explore` and the mutating verbs only in its Never section. Each phrase changed is grepped across `src/superclaude` first so no other primitive contradicts it.
- Reference the smoke report only through `./source.md`; never add a `src/superclaude` read path to an installed primitive. Never stage `.claude/`; no commit, no push, no PR.
- All nine report quotes were re-verified against the worktree before planning: the quotes sit at the stated lines of analyze.md (30, 32, 36, 63, 67), design.md (55, 57, 61, 65, 74) and CODEGRAPH.md (13, 22, 50, 74). None is rebutted.

## Phase 1: Shared guide says it once

## Task 1: Edit the shared guide in src/superclaude/core/CODEGRAPH.md

In section 2, step 3, add the wait on the MCP path: before the single `codegraph_status` call, if `pgrep -f 'codegraph\.js (init|index)'` prints a line, wait for it to end (poll up to 60 s) and then make the one check; if it is still running after 60 s, record `index_state: stale` with `graph:stale` and make no status call; still exactly one status call per run (item 1). Rewrite the tail of section 5 rule 7, "MCP `codegraph_status` needs no guard", so it no longer contradicts this: the CLI `status` stays guarded and skipped while an init runs, the MCP `status` waits as step 3 says. In step 7, say that `checked_at` is taken with one `date -u +%Y-%m-%dT%H:%M:%SZ` (Bash) immediately after the status call (item 4). In the section 4 row "Overview", change the MCP form to `codegraph_files {format:"grouped", maxDepth:2, path?}` and add that `path` set to the target's directory is recommended when the target is narrower than the repo (item 2). For item 7, section 3 already defines `graph:empty`, `graph:truncated` and `graph:unresolved`: add one clause to section 3 saying a single failed or empty lookup records the matching one of these tokens in the host's `degraded` list, and that no new token is added.

Acceptance criteria:
- `src/superclaude/core/CODEGRAPH.md` contains the pgrep-then-wait-up-to-60-s clause in section 2 with the `graph:stale` outcome and still states one status call per run; rule 7 no longer says the MCP status "needs no guard".
- The same file names the `date -u +%Y-%m-%dT%H:%M:%SZ` source for `checked_at` and a `path` argument on the `codegraph_files` row, and the section 3 clause about single failed or empty lookups.
- `uv run pytest tests/core/test_codegraph_guide.py -q` passes: at most 120 lines, tokens inside the closed list, banned names only in Never, no `src/superclaude/` text.

## Task 2: Mirror the guide into plugins/superclaude/core/CODEGRAPH.md

Depends on: Task 1

Copy `src/superclaude/core/CODEGRAPH.md` byte for byte to `plugins/superclaude/core/CODEGRAPH.md`, because `test_plugin_copy_is_byte_identical` in `tests/core/test_codegraph_guide.py` pins them identical.

Acceptance criteria:
- `cmp src/superclaude/core/CODEGRAPH.md plugins/superclaude/core/CODEGRAPH.md` prints nothing.

## Phase 2: Commands say the same thing

## Task 3: Edit the analyze command in src/superclaude/commands/analyze.md

Depends on: Task 1

Make these edits, each a clause or one sentence:
- Item 1: in the paragraph before step 1, add one clause that on the MCP path the single check first waits for a running `init`/`index` as section 2 of the guide says (pgrep, up to 60 s, then `graph:stale`), still one status call.
- Item 4: in the same paragraph, say `checked_at` is taken with one `date -u +%Y-%m-%dT%H:%M:%SZ` (Bash) immediately after the status call.
- Items 2 and 3, Discover step: rewrite so that `codegraph_files {format:"grouped", maxDepth:2}` takes `path` set to the target's directory when the target is narrower than the repo; for a directory or package target use `codegraph_files` with `path` and then `codegraph_node` with `symbolsOnly:true` on its main files; use `codegraph_search` only when the target names a symbol.
- Item 3, Scan step: symbol bodies (`includeCode:true`) are taken only for symbols Discover found; file outlines (`symbolsOnly:true`) stay as they are.
- Item 5, "Leads, not citations" bullet: add one sentence: at `--depth quick` a line found by Grep need not be re-Read, but a graph row cited as a finding is still confirmed by Grep or Read.
- Item 7: in the same bullet or the Use-only bullet, say a single lookup that fails or returns nothing records `graph:empty` (or `graph:truncated` for a short caller list, `graph:unresolved` for an unconfirmed row) on the Codegraph line and falls back to the floor for that lookup.
- Item 8: in the Report step, say that with `--format json` the line goes in a top-level `"codegraph"` string field of the JSON, and in other formats it stays one line of the report.
- Item 9: change "(read it when you use codegraph)" to "(read it before the first codegraph call)".

Acceptance criteria:
- `src/superclaude/commands/analyze.md` contains the pgrep/wait clause, the `date -u +%Y-%m-%dT%H:%M:%SZ` source, `path` on the `codegraph_files` call, the directory-target wording, the quick-depth sentence, a lookup-level token sentence naming tokens from the guide's section 3, the `"codegraph"` JSON field rule and "read it before the first codegraph call".
- The file still holds the `index_state: fresh` with `access: mcp` rule, the "never halt, never ask" sentence and one readiness check per run; `uv run pytest tests/skills/test_codegraph_adoption.py -q` passes for this file.

## Task 4: Edit the design command in src/superclaude/commands/design.md

Depends on: Task 1

Make these edits, each a clause or one sentence:
- Item 1: in "Readiness check, once per run", add one clause for the wait on a running `init`/`index` (pgrep, up to 60 s, then `graph:stale`), still one status call.
- Item 4: in the same paragraph, say `checked_at` is taken with one `date -u +%Y-%m-%dT%H:%M:%SZ` (Bash) immediately after the status call.
- Item 2: in the Analyze table row for `codegraph_files`, write `{format:"grouped", maxDepth:2, path?}` and add that `path` is set to the target's directory when it is narrower than the repo.
- Item 6: in the Validate row, change "then `codegraph_callers` and `codegraph_impact` for the consumers" so `codegraph_impact` runs at Validate only if it was not already run for the same symbol in Plan or Design.
- Item 7: in the sentence "A single lookup that fails or returns nothing falls back to the floor for that lookup in the same way", add that the matching lookup-level token (`graph:empty`, `graph:truncated` or `graph:unresolved`, all in the guide's section 3) is recorded in the Grounding line.
- Item 8: in "Grounding line", say that for `--format code` or `--format diagram` the line is the first comment line or a caption line of the output; for `spec` it stays a line of the document.
- Item 9: the first sentence of "Code-graph grounding" already says "read ... before the first codegraph call"; keep it, and make the Tool Coordination bullet's pointer say the same ("guide `~/.claude/CODEGRAPH.md`, read before the first codegraph call").

Acceptance criteria:
- `src/superclaude/commands/design.md` contains the pgrep/wait clause, the `date -u +%Y-%m-%dT%H:%M:%SZ` source, `path` on the `codegraph_files` row, the "only if not already run for the same symbol" Validate wording, the lookup-level token sentence, the code/diagram Grounding placement and the "before the first codegraph call" wording.
- The file still states one readiness check per run, the `fresh`-only rule, the floor and "never stops and never asks"; `uv run pytest tests/skills/test_codegraph_adoption.py -q` passes for this file.

## Phase 3: Tests pin the new wording

## Task 5: Add regression tests in tests/skills/test_codegraph_adoption.py and tests/core/test_codegraph_guide.py

Depends on: Task 3, Task 4

In `tests/skills/test_codegraph_adoption.py` add tests that read `src/superclaude/commands/analyze.md`, `src/superclaude/commands/design.md` and `src/superclaude/core/CODEGRAPH.md` and assert, each with its own test or parametrized case and a message naming the missing clause: the pgrep wait clause with `60 s` (guide and both commands); `path` on the `codegraph_files` call (guide, analyze, design); `date -u +%Y-%m-%dT%H:%M:%SZ` (guide, analyze, design); the quick-depth sentence (analyze); the top-level `"codegraph"` JSON field rule (analyze) and the first-comment-or-caption rule (design); the Validate-row "not already run" wording (design); "before the first codegraph call" (analyze and design). In `tests/core/test_codegraph_guide.py` extend `test_guide_names_switches_and_status_guard` (or add one test) so the guide must still say rule 7 no longer claims the MCP status "needs no guard". Then run the full check set and record one mutant: remove the pgrep/wait clause from `src/superclaude/commands/analyze.md` in a scratch copy of the test run (restore it afterwards) and show the new test failing; write that output to `./artifacts/mutant-analyze-pgrep.log`.

Acceptance criteria:
- Each new assertion fails when its clause is removed (mutant evidence in `./artifacts/mutant-analyze-pgrep.log`) and passes on the edited files.
- `uv run pytest tests/skills/test_codegraph_adoption.py tests/commands tests/agents tests/cli/eval tests/core/test_codegraph_guide.py -q` passes, plus any other test file that greps analyze.md, design.md or CODEGRAPH.md (found with a grep of `tests/` and `scripts/`).
- `make sync-dev` then `make verify-sync` pass; `uv run ruff check src tests scripts` passes and `uv run ruff format --check` passes on the touched Python files.
- `git diff --stat` lists only the permitted files, and `grep -rn 'src/superclaude' src/superclaude/commands/analyze.md src/superclaude/commands/design.md src/superclaude/core/CODEGRAPH.md` shows no new read path.
