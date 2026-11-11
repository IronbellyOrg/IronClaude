---
schema: workflow-plan/1.2
source: ./source.md
strategy: systematic
depth: quick
slug: TASK-WF-designWorkflowCo-20261111-193918
version: "1"
priority: Medium
created_date: "2026-11-11"
---

# Ground /sc:workflow in codegraph (issue 504, workflow part)

Source: ./source.md
Goal: `/sc:workflow` runs one codegraph readiness check per run and, only when the index is fresh, uses codegraph to ground the generated plan and its advisory pre-check in the real code; otherwise it uses Grep/Glob/Read and records a `graph:*` note, and it never halts. Every existing flag, STOP code, the `workflow-plan/1.2` schema, package contract 1.1 and the wave order stay as they are.

## Constraints

- Edit only `src/superclaude/skills/sc-workflow-protocol/SKILL.md`, `src/superclaude/commands/workflow.md` and, because `tests/commands/test_workflow_command.py::test_plugin_mirror_matches_src` pins them byte for byte, the two matching files under `plugins/superclaude/`. Do not edit `.claude/`, `src/superclaude/core/CODEGRAPH.md`, any other command, skill or agent, or any file another session owns.
- Cite only the installed guide `~/.claude/CODEGRAPH.md`; add no instruction that tells an agent to read a `src/superclaude/...` path.
- Keep `mcp-servers: []` and `Skill sc:workflow-protocol` in the command file, the template reference `refs/00_mdtm_template_simple_task.md` in SKILL.md, the Wave 3, 4, 5 order, and the `## Unattended mode` section and `refs/return-contract.md` wording that `tests/skills/test_worker_contract.py` parses.
- No commit, no push, no pull request, no `git add` of any `.claude/` path.

## Phase 1: Add the codegraph rules to the protocol and the command

## Task 1: Add the codegraph grounding rules to the protocol SKILL.md

Edit `src/superclaude/skills/sc-workflow-protocol/SKILL.md` as specified in `./source.md` sections 3.2 to 3.8 and 4. In the frontmatter, append exactly these tools to `allowed-tools`: `mcp__codegraph__codegraph_status`, `mcp__codegraph__codegraph_search`, `mcp__codegraph__codegraph_node`, `mcp__codegraph__codegraph_callers`, `mcp__codegraph__codegraph_callees`, `mcp__codegraph__codegraph_impact` (no wildcard), and add an extended-metadata comment block carrying `mcp-servers: [codegraph]` in the style of `src/superclaude/skills/sc-reflect-protocol/SKILL.md`. Add a vocabulary row for codegraph lookups (exact tool names, only when `index_state` is `fresh`). Add a `## Codegraph grounding` section between the vocabulary table and Wave 0 that states: the one readiness check per run runs at the start of Wave 1 following section 2 of `~/.claude/CODEGRAPH.md` and is never repeated; the result `index_state`, `checked_at`, `worktree_root`, `projectPath` plus access and tokens is written to `<pkg>/artifacts/codegraph-grounding.md`; the tool-to-step table of `./source.md` section 3.3 (Wave 1 `codegraph_search`, `codegraph_node` with `symbolsOnly:true`, `codegraph_files`; Wave 2 `codegraph_node` with `includeCode:true`, `codegraph_callers`, `codegraph_callees`, `codegraph_impact`; Wave 4 pre-check); the fresh-only rule with the permanent Grep/Glob/Read floor and the closed `graph:*` token list from the guide, never a STOP, a gate failure or a status change; Read before cite, caller rows verified at the call site, an empty graph answer never meaning no callers; and that any sub-agent brief the protocol writes carries `index_state`, `checked_at`, `worktree_root` and the `projectPath` to pass, with the receiver using codegraph only when `index_state: fresh`. Add one line each in Wave 1 (readiness check, resolve named files and symbols), Wave 2 (name real callers and dependents in task bodies and acceptance criteria, order and split tasks by blast radius, within the depth cap) and Wave 4 (advisory read-only pre-check before the existing reflect call, findings under `## Pre-check` in the grounding artifact, the plan never edited).

Acceptance criteria:
- The SKILL.md frontmatter `allowed-tools` contains the six exact `mcp__codegraph__codegraph_*` names above and no `mcp__codegraph__*` wildcard, and the file contains `mcp-servers: [codegraph]`.
- The file states exactly one codegraph readiness check per run (Wave 1) and names which codegraph tool serves Wave 1, Wave 2 and the Wave 4 pre-check.
- The file states codegraph is used only when `index_state` is `fresh`, that otherwise Grep/Glob/Read run with a `graph:*` note, and that nothing in this feature halts the run, fails the gate or changes the package status.
- The file names `index_state`, `checked_at`, `worktree_root` and `projectPath` as the run state carried by any sub-agent brief.
- `grep -n 'src/superclaude' src/superclaude/skills/sc-workflow-protocol/SKILL.md` prints no line that tells an agent to read a `src/superclaude/...` path.
- Wave order, the template reference, the retired `--output` wording and the Wave 4 `nested/reflect-` line are unchanged: `uv run pytest tests/commands/test_workflow_command.py -k "not plugin_mirror"` passes.

## Task 2: Add the codegraph section to the command file workflow.md

Depends on: Task 1

Edit `src/superclaude/commands/workflow.md` as specified in `./source.md` section 3.1, keeping the frontmatter (including `mcp-servers: []`), the options table, the Activation section and the `## Unattended mode` section unchanged. Add one sentence to Behavioral Summary (one codegraph readiness check per run, owned by the protocol; a fresh index grounds the plan and the pre-check, otherwise Grep/Read with a recorded note). Add a short `## Codegraph grounding` section before `## Unattended mode` that states the single readiness rule and points to `~/.claude/CODEGRAPH.md` section 2, carries the tool-to-step table (Wave 1, Wave 2, Wave 4 pre-check, matching Task 1), the fallback rule (any state other than `fresh`, or a failing lookup, means Grep/Glob/Read plus the matching `graph:*` token in `<pkg>/artifacts/codegraph-grounding.md`, never a STOP or gate), the `SUPERCLAUDE_CODEGRAPH_PRIMITIVES=off` switch (`graph:disabled`), and that `--unattended` applies the same rules with no gate and no person-mode flag. Extend the `Will:` line in Boundaries with grounding the plan in the real code through codegraph when the index is fresh; leave `Will Not:` unchanged.

Acceptance criteria:
- `src/superclaude/commands/workflow.md` states exactly one codegraph readiness check per run and lists which codegraph tool serves which step, consistent with the SKILL.md table from Task 1.
- The file states codegraph is used only when `index_state` is `fresh`, otherwise Grep/Glob/Read with a recorded note, and never halts.
- `mcp-servers: []`, `Skill sc:workflow-protocol`, every flag row, the banned-flag line and the `## Unattended mode` section are byte-identical to the version before the edit (`git diff src/superclaude/commands/workflow.md` shows only added lines plus the one changed Boundaries `Will:` line).
- `grep -n 'src/superclaude' src/superclaude/commands/workflow.md` prints no new read-instruction line.
- `uv run pytest tests/commands/test_workflow_command.py tests/skills/test_worker_contract.py -k "not plugin_mirror"` passes.

## Phase 2: Mirror and sync

## Task 3: Copy the two files to the plugin mirror and sync the dev copies

Depends on: Task 2

Copy the final `src/superclaude/commands/workflow.md` to `plugins/superclaude/commands/workflow.md` and the final `src/superclaude/skills/sc-workflow-protocol/SKILL.md` to `plugins/superclaude/skills/sc-workflow-protocol/SKILL.md` (the other files in that skill folder are unchanged and already match). Then run `make sync-dev` and `make verify-sync`. If `make verify-sync` names files this plan does not own, run `make sync-dev` once more and re-check; never edit those files. Run the tests that cover the three edited files.

Acceptance criteria:
- `cmp src/superclaude/commands/workflow.md plugins/superclaude/commands/workflow.md` and `cmp src/superclaude/skills/sc-workflow-protocol/SKILL.md plugins/superclaude/skills/sc-workflow-protocol/SKILL.md` print nothing.
- `make sync-dev` and `make verify-sync` exit 0 (any failure naming a file owned by another session is reported, not fixed).
- `uv run pytest tests/commands/test_workflow_command.py tests/skills/test_worker_contract.py tests/skills/test_task_workspace_lifecycle.py` passes, including `test_plugin_mirror_matches_src`; any failure that cannot be attributed to this change is reported instead of fixed.
- `grep -rn 'src/superclaude' src/superclaude/commands/workflow.md src/superclaude/skills/sc-workflow-protocol` shows no hit that tells an agent to read a `src/superclaude/...` path beyond the hits present before this change.
- `git status --short` lists no `.claude/` path as staged and nothing is committed.
