---
name: graph
description: "Show whether this worktree's code-graph index is ready (version, pin, index state, worktree relation, counts, telemetry) and, only when you type `init`, build the index for this worktree"
category: utility
complexity: basic
mcp-servers: [codegraph]
personas: []
argument-hint: "[status|init] [--worktree-local] [--output-dir <dir>]"
allowed-tools: Skill, Bash(codegraph init --yes *), Bash(codegraph init -i)
---

# /sc:graph

Reports whether this worktree's code-graph index is ready, and is the manual indexing path. Phase 2's session-start hook already starts `codegraph init --yes` in every new checkout; type `/sc:graph init` only when the hook did not cover this worktree: a nested worktree that answers from its parent's index, the hook switched off with `SUPERCLAUDE_CODEGRAPH_AUTOINIT=0`, or an init that failed or was interrupted. No skill or agent runs init.

Codegraph usage rules: read `~/.claude/CODEGRAPH.md` (in a dev checkout without an install, the labelled fallback is `src/superclaude/core/CODEGRAPH.md`).

## Usage

```bash
/sc:graph                                 # status (default): readiness report, 8 lines
/sc:graph status --output-dir .dev/graph  # also write return-contract.yaml
/sc:graph init                            # index this worktree (user-typed only)
/sc:graph init --worktree-local           # nested worktree: build its own index instead of the parent's
/sc:graph status --unattended --output-dir .dev/graph/run1   # worker mode: contract written there
/sc:graph status --unattended --report-dir .dev/graph/run1   # worker mode: contract in the report directory
```

## Options

| Flag | Default | Description |
|------|---------|-------------|
| `status` \| `init` | `status` | Positional subcommand. Any other word, or two positionals, STOPs with `status: blocked`. |
| `--worktree-local` | `false` | Only with `init`: build a worktree-local index for a nested worktree that answers from the parent index. With `status` it STOPs. |
| `--output-dir <dir>` | unset (screen only) | Write `return-contract.yaml` there. Must not be inside `.git/` or `.codegraph/` of the worktree. |
| `--unattended` | `false` | Worker mode: no step waits for a person; see Unattended mode. |
| `--report-dir <dir>` | unset | With `--unattended`, the directory that holds the worker contract (instead of `--output-dir`, never both). |

There is no `--caller` flag: no skill calls `/sc:graph`. The skill also accepts an internal `--post-init <exit-code>` that only this command body passes after its init call.

## Activation

**MANDATORY**: Before executing any protocol steps, invoke:
> Skill sc:graph-protocol

Pass the user's subcommand and flags unchanged. Do NOT proceed with protocol execution using only this command file. The readiness check, report, contract and the read-only init preflight are in the protocol skill.

## Init (user-typed only)

These steps run only for `init`, after the skill's preflight returned `init.form` (`default` or `worktree_local`) and no refusal:

1. **Guard.** Continue only if the user's own message starts with `/sc:graph init`. Otherwise print "init runs only when you type it" and stop. A skill, an agent or another command never reaches the steps below.
2. **Run once** (timeout 600000 ms), exactly one of:
   - `form: default` → `codegraph init --yes <worktree_root>`
   - `form: worktree_local` → `codegraph init -i`, run in `worktree_root` (the skill refused with `cwd_mismatch` if the session is elsewhere). In codegraph 1.6.2 `-i` is a deprecated alias that is still accepted, and init inside a nested worktree builds its own `.codegraph/` (Phase 3 experiment E-2).
   Record the exit code. Never prefix the call with environment variables.
3. **Verify.** Invoke `> Skill sc:graph-protocol` again with `status --post-init <exit-code>`, plus the user's `--output-dir` if given. The skill re-checks the index once and reports `success`, `partial` or `failed`.

## Unattended mode

The shared rules are in `~/.claude/WORKER-CONTRACT.md`; read it first. This section lists only what `/sc:graph` resolves itself.

- **Switch.** It applies only when `--unattended` is a standalone argument token outside any quoted argument; otherwise nothing here applies and no worker contract is written.
- **Report directory.** Exactly one of `--output-dir <dir>` or `--report-dir <dir>` is required; the screen-only default does not satisfy it, and both, or neither, is refused before any work. `--report-dir` follows the path rules of `--output-dir` (not inside `.git/` or `.codegraph/` of the worktree, not under the distributable skill, agent or command folders of a `.claude/` folder, created if missing and writable); a directory that fails them counts as no report directory known, so the refusal is printed in chat only.
- **Contract.** With `--output-dir` the worker fields are added to the existing `<output-dir>/return-contract.yaml` beside every existing field. With `--report-dir` the skill writes `<report-dir>/return-contract.yaml` with the same existing fields plus the worker fields. The report is the screen report, so `report_path` is null. `command` keeps its existing value (`graph`). The own status values success and partial map to succeeded and partial, failed to failed, and the flag-STOP `blocked` to failed with the STOP in `reason`.
- **Init.** The command refuses init under `--unattended` (contract failed; `reason` says init runs only when the user types it), also in its `--worktree-local` form. The skill stops before the Init steps of this file can start, so only the `status` form runs.
- **Gates.** None else. Nested invocations: none.
- **Outward actions.** It runs no codegraph build command and pushes, commits and stages nothing.

## Boundaries

**Will:**

- Report version, pin match, index state, worktree relation, counts, pending files, telemetry and one next action
- Run `codegraph init` once, only when the user typed `/sc:graph init` and the preflight allowed it

**Will Not:**

- Run init for a skill, an agent or any automatic flow, or rebuild an existing index
- Run init while another init or index is running (the preflight refuses; wait and run `/sc:graph status`)
- Change MCP registration, install or upgrade codegraph, or change telemetry settings
