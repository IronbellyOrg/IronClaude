# Design spec: codegraph grounding in /sc:workflow (issue #504, workflow part)

Type: component. Format: spec. Targets: `src/superclaude/commands/workflow.md` and `src/superclaude/skills/sc-workflow-protocol/` (SKILL.md and refs/). Source of the codegraph rules: the installed guide `~/.claude/CODEGRAPH.md` (source `src/superclaude/core/CODEGRAPH.md`, read-only for this work).

## 1. Goal

`/sc:workflow` uses codegraph, when the index is fresh, to ground the plan it writes in the real code: resolve the files and symbols each task will touch, list the real callers and dependents so tasks and acceptance criteria name them, size and order tasks by blast radius, and use the same grounding in the advisory pre-check. When the index is not fresh, the existing Grep/Glob/Read floor does the same job and a `graph:*` note is recorded. The run never halts because of codegraph.

## 2. Hard constraints (must stay exactly as today)

- Flags: `--strategy`, `--depth`, `--handoff`, `--unattended`, `--report-dir`; banned flags and STOP codes unchanged.
- Package schema `workflow-plan/1.2`, package contract 1.1 and worker contract: no new keys, no new STOP code, no change to status mapping.
- Wave order 0 Parse, 1 Structure, 2 Synthesize, 3 Gate, 4 Reflect, 5 Contract. Gate rules in `refs/quality-gates.md` unchanged (no checkbox or numbered lines, no verification-only task, repo-relative delivery paths).
- Plan only: no product code, no Task fan-out, no new agents, plan never edited from reflect findings.
- Pinned by tests/commands/test_workflow_command.py: the command text keeps `mcp-servers: []` and `Skill sc:workflow-protocol`; the SKILL.md template reference and Wave 3 < 4 < 5 order stay; `src/superclaude/templates/workflow/` is not named in SKILL.md; `plugins/superclaude/commands/workflow.md` and `plugins/superclaude/skills/sc-workflow-protocol/**` must equal the src copies byte for byte, so the plugin mirror is updated by copying the final src files.
- Installed primitives must not tell an agent to read `src/superclaude/...`: cite only `~/.claude/CODEGRAPH.md`.

## 3. Components

### 3.1 Command file `commands/workflow.md`

- Keep frontmatter as is (including `mcp-servers: []`).
- Behavioral Summary: one added sentence: one codegraph readiness check per run (in the protocol), fresh index grounds the plan and the pre-check, otherwise Grep/Read with a recorded note.
- New section `## Codegraph grounding` (before `## Unattended mode`), short, with:
  - the single rule: one readiness check per run, owned by the protocol (`~/.claude/CODEGRAPH.md` section 2); the command never repeats it;
  - a table of which tool serves which step (see 3.3);
  - fallback: any state other than `fresh` (or a failing lookup) means Grep/Glob/Read for that step plus the matching `graph:*` token in the grounding note; never a STOP, never a gate;
  - the switch `SUPERCLAUDE_CODEGRAPH_PRIMITIVES=off` is honoured (`graph:disabled`);
  - under `--unattended` the same rules apply with no gate and no person-mode flag.
- Boundaries: Will adds "ground the plan in the real code through codegraph when fresh"; Will Not unchanged.

### 3.2 Skill `skills/sc-workflow-protocol/SKILL.md`

- Frontmatter `allowed-tools`: append exactly `mcp__codegraph__codegraph_status, mcp__codegraph__codegraph_search, mcp__codegraph__codegraph_node, mcp__codegraph__codegraph_callers, mcp__codegraph__codegraph_callees, mcp__codegraph__codegraph_impact` (the list sc-reflect-protocol uses; no wildcard). Add the extended-metadata comment block carrying `mcp-servers: [codegraph]` the way sc-reflect-protocol and sc-troubleshoot-protocol do. `Bash` is already allowed (needed for `printenv`, `git rev-parse`, `pgrep`).
- Execution vocabulary: add a row `Codegraph lookup | mcp__codegraph__codegraph_<tool> (exact names), only when index_state is fresh`.
- New `## Codegraph grounding` section (between the vocabulary and Wave 0) holding the rules below, so each wave step stays one line.

### 3.3 Where each codegraph tool is used

| Step | Job | Tool when fresh | Floor (permanent) |
|---|---|---|---|
| Wave 1, step 0 (once per run, package exists) | Readiness check | `codegraph_status {projectPath}` per guide section 2 | CLI `codegraph status` guarded by `pgrep`, else floor |
| Wave 1 Structure | Resolve the files and symbols the source names; outline of each named file | `codegraph_search {query, kind?, limit}`, `codegraph_node {file, symbolsOnly:true}`, `codegraph_files {format:"grouped", maxDepth:2}` for an area overview | Glob, Grep for definitions, Read |
| Wave 2 Synthesize | Symbol body of what a task changes; real callers and dependents; blast radius | `codegraph_node {symbol, file?, includeCode:true}`, `codegraph_callers {symbol, file?, limit:20}`, `codegraph_callees`, `codegraph_impact {symbol, depth:1}` | Grep with word boundary then Read each site |
| Wave 4 pre-check | Cross-check that every file or symbol a task names resolves and every named dependent is real; list dependents the plan missed | same lookups, read-only | same Grep/Read |

Neither `codegraph_explore`/`codegraph context` nor `codegraph_node` file mode without `symbolsOnly:true` is ever used; no mutating verb; no environment-variable prefix on a CLI call (guide section 7).

### 3.4 Readiness rule (exactly one per run)

Run the guide's section 2 once, at the start of Wave 1 (after Wave 0 validation and package creation, before any lookup): switch, `worktree_root` (realpath of `git rev-parse --show-toplevel`, also the `projectPath` for every call), MCP detection from the session's own tool list, version pin for CLI access, classification into `index_state: fresh|stale|not_initialized|foreign_index|absent|disabled|error`, access (`mcp`, `cli` or `none`), and `checked_at` (UTC). The result is the run state `{index_state, checked_at, worktree_root, projectPath}`. It is written to `<pkg>/artifacts/codegraph-grounding.md` (package artifacts folder: package-relative, always staged with the package) and never re-run: later waves read it. The plan writes only into `.dev/tasks`, so the index is not stale because of this run.

### 3.5 Using the result

- `index_state: fresh` and lookup tools listed: use the codegraph tier above the floor for the steps in 3.3. A graph row locates code and is never a citation: Read the range before a task cites it; caller rows give the caller's definition line, so a task states "calls X" only after the call site is confirmed by the guide's section 5 rules (Grep the call in the caller's span and Read it), else it names the caller as a dependent by definition. An empty graph answer never becomes "no callers" or "no dependents".
- Plan content changes (all inside the unchanged `workflow-plan/1.2` shape): a task body names the real files and symbols it changes (repo-relative); `Acceptance criteria:` bullets name the real callers and dependents that must keep working or be updated; blast radius sizes and orders tasks: a symbol with many dependents gets its own task, the tasks that update its dependents follow with `Depends on: Task K`, and a change reaching more files than one task can hold is split; the phase and task counts still respect the depth cap.
- Any other state, or a lookup that fails or returns nothing: run the floor step for that lookup unchanged, add the matching token from the closed list (`graph:absent`, `graph:unlisted`, `graph:disabled`, `graph:not_initialized`, `graph:foreign_index`, `graph:stale`, `graph:version_mismatch`, `graph:provenance_unproven`, `graph:empty`, `graph:ambiguous`, `graph:truncated`, `graph:parse_failed`, `graph:unresolved`) to the grounding note, and continue. `graph:not_initialized` also prints the line "run `/sc:graph status`". Invent no token. No token stops the run, fails the gate, or changes the package status.
- Caps from the guide: at most 5 caller rows per symbol and 20 per run; `shown/total` recorded; a truncated list is re-queried once with a larger limit, else `graph:truncated`.
- The floor is permanent: using it is normal evidence, and a plan generated on the floor is valid and gated the same way.

### 3.6 Sub-agent and nested-skill briefs

The protocol today spawns no agent. If any brief is written (a Task brief, or any file handed to an agent), it carries the run state `index_state`, `checked_at`, `worktree_root` and the `projectPath` to pass, and states that the receiver calls codegraph only when `index_state: fresh`, otherwise Grep/Read. The Wave 4 `/sc:reflect --mode pre` call is a Skill call with flags only and cannot receive the state; reflect runs its own readiness check (its own contract) and the workflow run does not count it as a second check of its own. The workflow pre-check in 3.3 runs before that call, in the workflow's own context.

### 3.7 Pre-check (Wave 4, before the reflect call)

Advisory, read-only on the plan: for each task, confirm (fresh: codegraph; else floor) that the named files exist and the named symbols resolve, and that the dependents the task lists are real; list dependents of the touched symbols that no task names. Write the findings under `## Pre-check` in `<pkg>/artifacts/codegraph-grounding.md` and print a one-line count with the plan path. It never edits `<id>.md`, never changes `status`, and a failure of this step is only a `graph:*` note. Then the existing reflect call runs unchanged.

### 3.8 Artifact `<pkg>/artifacts/codegraph-grounding.md`

Sections: `## Run state` (the four fields, access, tokens), `## Resolved symbols` (file, symbol, source of the row: codegraph or floor), `## Dependents` (symbol, rows with `shown/total` and `resolution`), `## Pre-check`. Under `--unattended` it is listed in the worker contract `artifacts`. It is not a plan field and no existing contract key is added: the package contract stays 1.1.

## 4. Acceptance criteria for the implementation

1. `workflow.md` and the protocol both state: exactly one codegraph readiness check per run, and which codegraph tool serves which step (3.3).
2. Codegraph is used only when `index_state` is `fresh`; otherwise Grep/Glob/Read with a `graph:*` note; no path halts, fails the gate, or changes the status.
3. The run-state fields (`index_state`, `checked_at`, `worktree_root`, `projectPath`) are named as part of any sub-agent brief the protocol writes.
4. SKILL.md frontmatter lists the six `mcp__codegraph__codegraph_*` tools (exact names) and the codegraph MCP server in the extended-metadata comment.
5. `grep -rn 'src/superclaude' src/superclaude/commands/workflow.md src/superclaude/skills/sc-workflow-protocol` has no new read-instruction hit (only the pre-existing line, if any).
6. Existing behaviour untouched: flags, STOP codes, `workflow-plan/1.2`, contract 1.1, wave order, the unattended section.
7. `plugins/superclaude/commands/workflow.md` and `plugins/superclaude/skills/sc-workflow-protocol/SKILL.md` equal their src copies; `make sync-dev` and `make verify-sync` pass; `uv run pytest tests/commands/test_workflow_command.py tests/skills/test_worker_contract.py tests/skills/test_task_workspace_lifecycle.py` pass.

## 5. Files and edit order

1. `src/superclaude/skills/sc-workflow-protocol/SKILL.md` (frontmatter, vocabulary row, `## Codegraph grounding`, one line each in Waves 1, 2, 4; `.dev` wording kept).
2. `src/superclaude/commands/workflow.md` (summary sentence, `## Codegraph grounding`, Boundaries line).
3. Copy both files to `plugins/superclaude/` mirror (required by the existing mirror test).
4. `make sync-dev`, `make verify-sync`, the tests above, the grep check.

Out of scope: refs (no change needed; if a ref must mention the artifact, only `return-contract.md`'s worker `artifacts` line), other commands, skills and agents, `core/CODEGRAPH.md`, the `.claude/` folder.

## 6. Risks

- `test_mcp_servers_empty` pins `mcp-servers: []` in the command, so the server list lives in the skill, not the command.
- `tests/skills/test_worker_contract.py` parses the workflow unattended section and the return-contract ref: do not reword those headings or lines beyond the one `artifacts` mention.
- The plugin mirror is byte-pinned: a src edit without the mirror copy fails `test_plugin_mirror_matches_src`.
