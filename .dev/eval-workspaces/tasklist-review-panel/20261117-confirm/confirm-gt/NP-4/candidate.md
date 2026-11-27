---
schema: workflow-plan/1.2
source: ./source.md
strategy: systematic
depth: quick
slug: TASK-WF-designOutput-20261111-193642
version: "1"
priority: Medium
created_date: "2026-11-11"
---

# Add codegraph grounding to the /sc:design command (issue #504)

Source: ./source.md
Goal: `src/superclaude/commands/design.md` runs one codegraph readiness check per run, uses codegraph above the Glob/Grep/Read floor only when `index_state` is `fresh`, and otherwise falls back to Glob/Grep/Read with a recorded `graph:*` note, without changing any existing flag, behaviour or Boundary.

## Constraints

- Edit only `src/superclaude/commands/design.md`. No backing skill is created. Tests that pin that file change only if they must. Do not edit `src/superclaude/core/CODEGRAPH.md`, any other command, skill or agent, or anything under `.claude/`.
- The installed command must not tell an agent to read a `src/superclaude/...` path; the guide is named `~/.claude/CODEGRAPH.md`.
- No commit, no push, no PR, and no `git add` of `.claude/` contents. Staging and committing are left to the coordinator.
- The Unattended mode section (including its `.codegraph/` report-directory exclusion), the Usage flags and the Boundaries stay as they are. `tests/skills/test_worker_contract.py` pins the phrases `design-report.md`, `no gate` and `consent is never given` for design; they must remain.

## Phase 1: Add the codegraph grounding rules

## Task 1: Add the frontmatter entry and the Code-graph grounding section

In `src/superclaude/commands/design.md`, change the frontmatter line `mcp-servers: []` to `mcp-servers: [codegraph]` and leave every other frontmatter key unchanged (no `allowed-tools` key is added). Insert a new `## Code-graph grounding` section between `## Tool Coordination` and `## Key Patterns` (source sections 3.1 and 3.2). It must contain a one-line pointer to `~/.claude/CODEGRAPH.md`; exactly one readiness check per run at the start of the Analyze step (guide section 2), recording `index_state`, `checked_at`, `worktree_root` and the `projectPath` passed on every call; the rule that codegraph is used only when `index_state` is `fresh` and the lookup tools are listed, otherwise the run continues on Glob/Grep/Read, adds the matching `graph:*` token (`graph:absent`, `graph:not_initialized`, `graph:stale`, `graph:foreign_index`, `graph:disabled`, `graph:unlisted`, `graph:parse_failed`) and never stops; and the tool-to-step map. Analyze uses `codegraph_files {format:"grouped", maxDepth:2}`, `codegraph_search`, and `codegraph_node` (outline with `symbolsOnly:true`, or a symbol body with `includeCode:true`) to find existing interfaces and symbols to reuse. Plan and Design use `codegraph_callers`, `codegraph_callees` and `codegraph_impact {depth:2}` for the callers and blast radius of the component or API being designed or changed. Validate uses `codegraph_search` and `codegraph_node` to confirm the names, layering and signatures in the design match the existing structure, plus callers and impact to confirm no consumer is broken. The section also states the rules: a graph answer is a lead and the file range is Read before a `file:line` is quoted; an empty result never proves absence; caller rows are definition lines until the call site is confirmed (guide section 5); never `codegraph_explore`, never `codegraph_node` in file mode without `symbolsOnly:true`, never a mutating verb, never `codegraph init`; `SUPERCLAUDE_CODEGRAPH_PRIMITIVES=off` gives `graph:disabled`. The section ends with the fallback note rule: record the `graph:*` token, or `index_state: fresh` with the tools used, on a `Grounding` line of the design document, and under `--unattended` also in the worker contract's existing degraded list only if that contract defines one.

Acceptance criteria:
- `grep -n 'mcp-servers' src/superclaude/commands/design.md` shows `mcp-servers: [codegraph]` and the other frontmatter keys are unchanged.
- The `## Code-graph grounding` section exists between `## Tool Coordination` and `## Key Patterns` and states exactly one readiness check per run, the fresh-only rule, the Glob/Grep/Read fallback with a recorded `graph:*` token that never halts, and the tool-to-step map for Analyze, Plan/Design and Validate.
- `grep -n 'src/superclaude' src/superclaude/commands/design.md` prints no line that tells an agent to read a `src/superclaude/...` path, and the section names no `codegraph_explore` call or mutating verb other than in a "never" rule.

## Phase 2: Wire the rules into the existing flow and tools

## Task 2: Point Behavioral Flow and Tool Coordination at the new section and run the checks

Depends on: Task 1

In `src/superclaude/commands/design.md`, add a short clause to Behavioral Flow step 1 (Analyze) and step 4 (Validate) that points to the `Code-graph grounding` section, keeping the five step names and the Key behaviors bullets. Add one bullet to `## Tool Coordination` naming the codegraph tools once (`mcp__codegraph__codegraph_status`, `_search`, `_node`, `_callers`, `_callees`, `_impact`, `_files`) as a tier above the floor, leaving the Read, Grep/Glob, Write and Bash bullets unchanged (source section 3.3). Leave Usage, Examples, Unattended mode and Boundaries unchanged. Then run `make sync-dev` and `make verify-sync` from the repository root (if `verify-sync` names files this change does not own, run `make sync-dev` once more and re-check; never edit those files), and run `uv run pytest tests/skills/test_worker_contract.py tests/unit/test_cli_install.py tests/core/test_how_we_work_routing_table.py tests/recommend/test_routing_refresh.py -q`. Write the command output of the sync, verify and pytest runs to `./artifacts/t2-checks.log`.

Acceptance criteria:
- Behavioral Flow steps 1 and 4 and the Tool Coordination section each refer to the codegraph grounding rules, and the Usage flags, Unattended mode section and Boundaries match their text before this change (`git diff src/superclaude/commands/design.md` shows no edit inside them).
- `make sync-dev` and `make verify-sync` both exit 0, and the exit codes are recorded in `./artifacts/t2-checks.log`.
- The four named test files pass with `uv run pytest`, or any failure is shown in `./artifacts/t2-checks.log` and is not attributable to `design.md`.
- `git status --short` shows no staged path under `.claude/`, and `src/superclaude/commands/design.md` is the only source file modified by this plan.
