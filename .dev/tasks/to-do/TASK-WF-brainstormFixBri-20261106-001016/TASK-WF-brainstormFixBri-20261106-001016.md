---
schema: workflow-plan/1.2
source: ./source.md
strategy: systematic
depth: standard
slug: TASK-WF-brainstormFixBri-20261106-001016
version: "1"
priority: Medium
created_date: "2026-11-06"
---

# Brainstorm: nested analyze folder only when /sc:analyze ran

Source: ./source.md
Goal: `/sc:brainstorm` under `--unattended` says in its skill, command file and routing ref that only a scan that ran as `/sc:analyze` writes a nested `analyze` directory; the auggie tier and the `fallback_1` tier (codegraph, then native Glob and Grep) write none. Tests pin that wording, and the worker-contract spec carries the corrected live-check wording for future live plans.

## Constraints

- Background: the P1 live check lc10 failed because the codebase-enrichment wave ran on `quality_tier: fallback_1` (the auggie tool was not available in the worker session) and wrote no `nested/analyze-1/` directory, while the live plan expected one. The owner decided on 2026-11-05 that the check wording was wrong, not the worker (record: `.dev/tasks/done/TASK-WF-p1LivePlanBrief-20261105-164506/artifacts/p1-owner-decisions-20261105.md` and `lc10-result.md` in the same folder). Those archived files are read, never edited.
- Edit only these files: `src/superclaude/skills/sc-brainstorm-protocol/SKILL.md`, `src/superclaude/skills/sc-brainstorm-protocol/refs/handoff-routing.md`, `src/superclaude/commands/brainstorm.md`, `tests/skills/test_brainstorm_protocol.py`, `tests/skills/test_worker_contract.py` and `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`. `make sync-dev` also rewrites the gitignored copies under `.claude/`; those are output, not edits, and are never staged.
- `src/superclaude/` is the source of truth. `plugins/superclaude/commands/brainstorm.md` is a copy that already differs from the `src` file, no test requires the two to match (`tests/commands/test_routing_plugin_parity.py` covers only the `sc-recommend` skill), and the spec lists the sync mechanism as an open item (spec line 443). It is not edited by this plan; Task 7 confirms it is untouched.
- No new text in the two installed primitives (the skill and its refs, the command file) may name a `src/superclaude/` path or an Orca command (`tests/skills/test_worker_contract.py` `_check_unattended_section` fails on both).
- UV for every Python command: `uv run pytest ...`, `uv run python ...`. Test runs use `-p no:cacheprovider` and `PYTHONDONTWRITEBYTECODE=1`. No `superclaude install` (the installed copies under `~/.claude/` are updated later by the owner).
- No git commit, push, merge or PR.

## Phase 1: Say it in the installed primitives

## Task 1: State in the skill that the fallback tier writes no nested folder

In `src/superclaude/skills/sc-brainstorm-protocol/SKILL.md`, the Wave 2A paragraph whose bold lead-in is "Under --unattended" (line 195) ends with: "The codebase row invokes `/sc:analyze` with `--unattended --report-dir <report-dir>/nested/analyze-<n>/` (`<n>` starts at 1); the `mcp__auggie__codebase-retrieval` alternative is unchanged and writes no nested contract. The nested contract is listed in `artifacts`." Replace the part after `(<n>` starts at 1)` so it reads, in substance: the `mcp__auggie__codebase-retrieval` alternative and the `fallback_1` tier (codegraph, then native Glob and Grep, `refs/handoff-routing.md` Tier 2) are unchanged and write no nested directory and no nested contract; a nested `analyze` directory exists only when `/sc:analyze` ran; `enrichment_used` records the tier that did run; a nested contract is listed in `artifacts` only for a nested command that ran. Use the exact phrase `write no nested directory` and keep the existing strings `nested/analyze-` and `skipped` in the paragraph. Change nothing else in the file.

Acceptance criteria:
- The Wave 2A paragraph under `--unattended` in `src/superclaude/skills/sc-brainstorm-protocol/SKILL.md` contains the phrases `fallback_1`, `write no nested directory` and `nested/analyze-`, and states that the nested directory exists only when `/sc:analyze` ran.
- `git diff --stat -- src/superclaude/skills/sc-brainstorm-protocol/SKILL.md` shows only that paragraph changed (one line replaced).
- `PYTHONDONTWRITEBYTECODE=1 uv run pytest tests/skills/test_brainstorm_protocol.py -q -p no:cacheprovider` still passes before the test change of Task 4.

## Task 2: State the same rule in the routing ref for both codebase tiers

In `src/superclaude/skills/sc-brainstorm-protocol/refs/handoff-routing.md`, the codebase enrichment section has a Tier 1 (primary) heading for `mcp__auggie__codebase-retrieval` (line 16) and a Tier 2 (fallback_1) heading for codegraph, then native Glob and Grep (line 24), each with a bullet list that ends with its `quality_tier` line. Add one bullet to each tier's list, worded: Under --unattended this tier writes no nested directory and no nested contract; the scan is recorded in enrichment_used with this tier's quality_tier. The exact phrase `writes no nested directory` must appear in both bullets. Do not touch the research tiers (lines 36 onward) or the `nested/adversarial-` text.

Acceptance criteria:
- `grep -c 'writes no nested directory' src/superclaude/skills/sc-brainstorm-protocol/refs/handoff-routing.md` prints 2, one in the Tier 1 list and one in the Tier 2 list of the codebase section.
- `git diff --stat -- src/superclaude/skills/sc-brainstorm-protocol/refs/handoff-routing.md` shows two added lines and no deletion.

## Task 3: State the same rule in the command file's Unattended mode section

In `src/superclaude/commands/brainstorm.md`, the `## Unattended mode` section has a bullet `**Nested invocations.**` (line 157) that says the `/sc:analyze` codebase enrichment receives `--unattended --report-dir <report-dir>/nested/analyze-<n>/`. Append to that bullet: a codebase scan done through `mcp__auggie__codebase-retrieval` or through the `fallback_1` tier (codegraph, then Glob and Grep) is not a nested command; it writes no nested directory and no nested contract, `enrichment_used` records its tier, and the nested `analyze` directory exists only when `/sc:analyze` ran. Use the exact phrase `writes no nested directory`. Do not name a `src/superclaude/` path or an Orca command, and keep the strings `nested/analyze-` and `nested/adversarial-`. Do not edit `plugins/superclaude/commands/brainstorm.md`.

Acceptance criteria:
- The `**Nested invocations.**` bullet of `src/superclaude/commands/brainstorm.md` contains the phrase `writes no nested directory` and still contains `nested/analyze-` and `nested/adversarial-`.
- `PYTHONDONTWRITEBYTECODE=1 uv run pytest tests/skills/test_worker_contract.py -q -p no:cacheprovider` passes with the edit in place.
- `git diff --stat -- plugins` prints nothing.

## Phase 2: Pin the wording with tests

## Task 4: Pin the skill and routing-ref wording in test_brainstorm_protocol.py

Depends on: Task 1, Task 2

In `tests/skills/test_brainstorm_protocol.py`, the test `test_brainstorm_unattended_nested_directories_are_named` (line 37) asserts `nested/analyze-` and `skipped` in the Wave 2A section (line 44) and `nested/adversarial-` in `refs/handoff-routing.md`. Extend it, or add a sibling test next to it with the same helpers (`_wave2a_section`, `_BRAINSTORM`), so that it also asserts: the Wave 2A section contains `fallback_1` and `write no nested directory`; and `refs/handoff-routing.md` contains `writes no nested directory` at least twice. Keep every existing assertion.

Acceptance criteria:
- `tests/skills/test_brainstorm_protocol.py` asserts the three new facts above, and every earlier assertion of that test is unchanged.
- `PYTHONDONTWRITEBYTECODE=1 uv run pytest tests/skills/test_brainstorm_protocol.py -q -p no:cacheprovider` passes.
- The new assertions are exact-substring checks (no pattern that the old sentence could also satisfy), so the pre-change text of the skill, which lacks `write no nested directory`, fails them.

## Task 5: Pin the command-file wording in test_worker_contract.py

Depends on: Task 3

In `tests/skills/test_worker_contract.py`, the `UNATTENDED_EXPECT["brainstorm"]["phrases"]` list (line 286) holds `research enrichment is off`, `exactly as passed`, `never reused`, `nested/analyze-`, `nested/adversarial-` and `dry-run`. Add the phrase `writes no nested directory` to that list. The removed-token tests (`_removals`, built from `UNATTENDED_EXPECT`) pick the new phrase up on their own; do not add a separate mutation by hand unless the existing parametrized tests fail to cover it.

Acceptance criteria:
- `UNATTENDED_EXPECT["brainstorm"]["phrases"]` in `tests/skills/test_worker_contract.py` contains `writes no nested directory`.
- `PYTHONDONTWRITEBYTECODE=1 uv run pytest tests/skills/test_worker_contract.py -q -p no:cacheprovider` passes, and the parametrized removed-token tests include a case for the new phrase: `PYTHONDONTWRITEBYTECODE=1 uv run pytest tests/skills/test_worker_contract.py -p no:cacheprovider --collect-only -q -k brainstorm` lists more cases than it did before the edit.

## Phase 3: Record the corrected live-check wording

## Task 6: Add the corrected live-check wording to the worker-contract spec

In `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`, the section 2.1 bullet `**Nested propagation rule**` (line 62) ends with "Each command's `## Unattended mode` section names its nested invocations." Append two sentences. First: a nested directory `nested/<command>-<n>/` exists only for a nested command that actually ran; a command that does the same work through a tool or a native-search fallback (brainstorm's codebase scan on `quality_tier` `primary` through `mcp__auggie__codebase-retrieval`, or on `fallback_1` through codegraph and Grep) writes no nested directory and records the tier it used in its own contract. Second: a live-check extra for brainstorm therefore reads "for the codebase-enrichment wave, `nested/analyze-<n>/` exists, holds its own `return-contract.yaml` and is listed in `artifacts` only when `/sc:analyze` ran; a `primary` or `fallback_1` scan is recorded as the tier used, with no nested folder", and a live plan must not expect the folder otherwise (P1 check lc10 is the origin of this rule). Change nothing else in the spec, and leave the `brainstorm` row of the section 6 table (line 142) as it is.

Acceptance criteria:
- The `**Nested propagation rule**` bullet in `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` contains the two new sentences, including the phrases `only for a nested command that actually ran` and `lc10`.
- `git diff --stat -- .dev/orca-command-refactor/specs/orca-worker-contract-spec.md` shows one line changed.

## Phase 4: Dev copies and final checks

## Task 7: Sync the dev copies and run the affected tests and lint

Depends on: Task 1, Task 2, Task 3, Task 4, Task 5, Task 6

Run `make sync-dev` and then `make verify-sync` from the repository root so the gitignored copies under `.claude/` match `src/superclaude/`. Then run `PYTHONDONTWRITEBYTECODE=1 uv run pytest tests/skills/test_brainstorm_protocol.py tests/skills/test_worker_contract.py tests/commands/test_routing_plugin_parity.py -q -p no:cacheprovider` and `make lint`. Save the command outputs to `./artifacts/t7-sync.log`, `./artifacts/t7-pytest.log` and `./artifacts/t7-lint.log`. Do not edit any file in this task.

Acceptance criteria:
- `./artifacts/t7-sync.log` shows `make sync-dev` and `make verify-sync` both exiting 0.
- `./artifacts/t7-pytest.log` shows the three test files passing with no failure, and `./artifacts/t7-lint.log` shows `make lint` exiting 0 with no new ruff finding in the two edited test files.
- `git status --porcelain` lists, among tracked paths, only the six files named in Constraints plus this package; no path under `.claude/` and no path under `plugins/` is modified or staged, and nothing under `.dev/tasks/done/` is modified.
