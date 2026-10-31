---
name: sc:graph-protocol
description: "Readiness report for this worktree's code-graph index (cli_version, pin_match, index_state, worktree_relation, counts, pending files, telemetry, next_action) and the read-only preflight for /sc:graph init. Never runs init itself."
allowed-tools: Read, Write, Bash(codegraph --version), Bash(codegraph status), Bash(codegraph telemetry status), Bash(git rev-parse --show-toplevel), Bash(realpath *), Bash(pgrep -f *), Bash(printenv SUPERCLAUDE_CODEGRAPH_PRIMITIVES), mcp__codegraph__codegraph_status
---

<!-- Extended metadata (for documentation, not parsed):
category: utility
complexity: basic
mcp-servers: [codegraph]
-->

# sc:graph-protocol

Backs `/sc:graph` (`~/.claude/commands/sc/graph.md`, or the project `.claude/commands/sc/graph.md`). It reports whether this worktree's index is ready and decides whether a user-typed `/sc:graph init` may run. It never builds an index: the build call lives only in the command body, after this skill's preflight. No other skill calls this one.

Codegraph usage rules: read `~/.claude/CODEGRAPH.md` (in a dev checkout without an install, the labelled fallback is `src/superclaude/core/CODEGRAPH.md`).

Indexing model (Phase 2): the session-start hook starts an init in every new checkout (switch it off with `SUPERCLAUDE_CODEGRAPH_AUTOINIT=0`); `/sc:graph init` is the manual path for a nested worktree that answers from its parent's index, a switched-off hook, or a failed or interrupted init. `SUPERCLAUDE_CODEGRAPH_PRIMITIVES=off` switches off codegraph use in primitives only.

## Inputs and flags

| Flag | Type | Default | Validation | STOP (`status: blocked`, chat message, no Bash) |
|---|---|---|---|---|
| positional subcommand | `status` \| `init` | `status` | zero or one positional | any other word, or two positionals → "Unknown subcommand `<x>`; use `status` or `init`" |
| `--worktree-local` | bool | `false` | only with `init` | given with `status` → "`--worktree-local` applies only to `init`" |
| `--output-dir` | path | unset (screen only) | absolute after resolution; not inside `<worktree_root>/.git/` or `<worktree_root>/.codegraph/`; created if missing | inside `.git`/`.codegraph` → blocked; not creatable or writable → `status: failed`, reason printed only |
| `--post-init <exit-code>` | int 0-255 | unset | set only by `commands/graph.md` after its init call; requires `status` | misuse can only fill the `init` block of the contract; it runs nothing |

There is no `--caller` flag.

## Readiness check (guide section 2, one check per run)

| Step | Call | Classification |
|---|---|---|
| R1 | `printenv SUPERCLAUDE_CODEGRAPH_PRIMITIVES` | `off` → `index_state: disabled`, `access: none`, `worktree_relation: unknown`, token `graph:disabled`; skip R3-R6 |
| R2 | `git rev-parse --show-toplevel`, then `realpath <that>` | `worktree_root`; passed as `projectPath` on the MCP call. Not a git tree → `realpath .`, `worktree_relation: unknown` |
| R3 | `codegraph --version` | missing command → binary absent. Else `cli_version`; compare with the guide's `Pinned codegraph version:` line → `pin`, `pin_match`. Differs → `graph:version_mismatch` + `graph:provenance_unproven`; unreadable → `cli_version: unknown`, `pin_match: unknown`, `graph:provenance_unproven` |
| R4 | `mcp__codegraph__codegraph_status {"projectPath": "<worktree_root>"}` when it is in this session's tool list → `access: mcp`. Else, only when `pgrep -f 'codegraph\.js (init|index)'` prints nothing, `codegraph status` run in `worktree_root` → `access: cli`. When `pgrep` prints a line: do not run `status`; `index_state: stale`, `worktree_relation: unknown`, token `graph:stale`, `init_running: true`, and skip R5. No binary and no MCP tool → `access: none`, `index_state: absent`, `graph:absent` | MCP presence is read from the tool list, never from the kind of run; MCP status needs no guard |
| R5 | classify the R4 text | "belongs to a different git working tree" → `foreign_index`, `worktree_relation: parent`, `graph:foreign_index`; CLI "Not initialized" or MCP "isn't indexed with codegraph" → `not_initialized`, `worktree_relation: none`, `graph:not_initialized`; CLI "Index is up to date" or MCP "Changes since index: 0 added, 0 modified, 0 removed" → `fresh`, `own`; a CLI "Pending Changes:" list or non-zero MCP change counts → `stale`, `own`, `graph:stale`; anything else → `error`, `graph:parse_failed` |
| R6 | `mcp__codegraph__codegraph_callers` in the tool list? | `mcp_tools_listed: true|false`; MCP status answered but the lookup tools are missing → `graph:unlisted` (status-only branch) |

`checked_at` is the UTC time of R4 (`YYYY-MM-DDTHH:MM:SSZ`). `index_state` is one of `fresh`, `stale`, `not_initialized`, `foreign_index`, `absent`, `disabled`, `error`. `worktree_relation` is one of `own`, `parent`, `none`, `unknown` (`unknown` for `absent`, `disabled`, `error`). `access` is one of `mcp`, `cli`, `none`.

## `status` (default)

1. **G-R Readiness.** Run R1-R6 above and keep every field.
2. **G-T Telemetry.** If the binary is present: `codegraph telemetry status`, then classify the line that starts with `Telemetry:` (codegraph 1.6.2 prints a blank first line, then for example `Telemetry: enabled (your saved choice)`): `enabled` or `on` → `telemetry: on` and token `graph:telemetry_on`; `disabled` or `off` → `off`; no such line → `unknown`. The report prints the opt-out the user applies: add `export CODEGRAPH_TELEMETRY=0` (or `export DO_NOT_TRACK=1`) to the shell profile. This skill never changes the telemetry setting.
3. **G-C Counts.** From the R4 text: CLI `Files:`, `Nodes:`, `Edges:` lines (printed with thousands separators, for example `8,824`; drop the commas), or MCP `Files indexed:`, `Total nodes:`, `Total edges:` (inside `**…**` markup) → integer `counts {files, nodes, edges}`; a miss gives `counts: null` and `graph:parse_failed`, not an error. When R4 skipped `status` because an init is running, there is no text to parse: `counts: null`, `pending: unknown` and `worktree_relation: unknown`, with no `graph:parse_failed`. codegraph 1.6.2 reports pending changes as counts, not file names (Phase 3 experiment E-1), so `pending` is a sorted list only when file names are printed, else `unknown`; the screen shows the pending count when one is printed.
4. **G-N next_action** (first match wins):

   | Condition | `next_action` | Message line |
   |---|---|---|
   | `disabled` | `enable_codegraph` | "codegraph use in primitives is switched off by `SUPERCLAUDE_CODEGRAPH_PRIMITIVES=off`; unset it to use the graph" |
   | `absent` | `install_codegraph` | "codegraph is not installed; run `./update.sh` (IronClaude's installer owns codegraph)" |
   | MCP status answered, lookup tools not listed | `status_only_branch` | "Phase 2 shipped the status-only tool list; lookups use the CLI or Read/Grep" |
   | `not_initialized` | `run_graph_init` | "type `/sc:graph init` to index this worktree (the session-start hook normally does this; about 4.5 s and 34 MB per 500 files)" |
   | `foreign_index` | `run_graph_init_worktree_local` | "this nested worktree is answered from the parent index; type `/sc:graph init --worktree-local`" |
   | `pin_match: false` | `align_version` | "codegraph `<v>` differs from the pin `<pin>`; run `./update.sh`" |
   | `stale` | `wait_for_sync` | `init_running` → "an init or index is running (usually the session-start hook); wait and run `/sc:graph status`"; else "N files pending; the watcher syncs while an MCP session is open" |
   | `error` | `check_codegraph_error` | first error line, verbatim |
   | otherwise | `none` | "index ready" |

5. **G-O Outputs.** Print the screen report. If `--output-dir` is set, write `<output-dir>/return-contract.yaml`.

## `init` (preflight only; the command body runs the build)

1. **G-P Preflight (read-only).** Run G-R, then decide `init.form` (first match wins):

   | State | Flag | Result |
   |---|---|---|
   | `disabled` | any | blocked, `refused_reason: disabled` |
   | `absent` | any | blocked, `refused_reason: absent`, `next_action: install_codegraph` |
   | `pgrep -f 'codegraph\.js (init|index)'` prints a line | any | blocked, `refused_reason: init_running`, `next_action: wait_for_sync`, message "an init or index is running (usually the session-start hook); wait and run `/sc:graph status`" |
   | `fresh` or `stale` with `worktree_relation: own` | any | blocked, `refused_reason: already_initialized` (rebuilding an index is not offered) |
   | `foreign_index` | no `--worktree-local` | blocked, `refused_reason: nested_worktree`, `next_action: run_graph_init_worktree_local` |
   | `foreign_index` | `--worktree-local` | `form: worktree_local` |
   | `not_initialized` | no flag | `form: default` |
   | `not_initialized` | `--worktree-local` | blocked, `refused_reason: worktree_local_not_nested` |
   | `error` | any | blocked, `refused_reason: status_error` |

   `form: worktree_local` also needs the session's working directory to equal `worktree_root`; otherwise blocked, `refused_reason: cwd_mismatch`, and the report names the directory to run `/sc:graph init --worktree-local` from. The skill returns `init.form` to the command body and runs no build command.
2. **G-V Re-check.** When the command body calls back with `status --post-init <exit-code>`, re-run G-R once and fill the `init` block (`ran: true`, `exit_code`).

## `return-contract.yaml` (only with `--output-dir`)

| Field | Type | Allowed values / rule |
|---|---|---|
| `schema_version` | int | `1` |
| `command` | string | `graph` |
| `subcommand` | enum | `status` \| `init` (`init` whenever `--post-init` is set or the preflight ran) |
| `status` | enum | `success` \| `partial` \| `blocked` \| `failed` |
| `contract_path` | string | absolute path of this file |
| `output_dir` | string | absolute |
| `checked_at`, `access`, `index_state`, `worktree_root`, `worktree_relation`, `cli_version`, `pin`, `pin_match` | see Readiness check | |
| `mcp_tools_listed` | bool | `true` when `mcp__codegraph__codegraph_callers` is in the tool list |
| `counts` | map or null | `{files: int, nodes: int, edges: int}` |
| `pending` | list[string] or `unknown` | repo-relative paths, sorted |
| `telemetry` | enum | `on` \| `off` \| `unknown` |
| `telemetry_opt_out` | string | `export CODEGRAPH_TELEMETRY=0 (or DO_NOT_TRACK=1) in your shell profile` |
| `kill_switch` | string | `SUPERCLAUDE_CODEGRAPH_PRIMITIVES=off` |
| `next_action` | enum | `none` \| `run_graph_init` \| `run_graph_init_worktree_local` \| `install_codegraph` \| `enable_codegraph` \| `status_only_branch` \| `align_version` \| `wait_for_sync` \| `check_codegraph_error` |
| `degraded` | list[string] | `graph:*` tokens from the guide's closed list, sorted, unique |
| `init.requested` | bool | |
| `init.form` | enum or null | `default` \| `worktree_local` \| `null` |
| `init.ran` | bool | `true` only when `--post-init` was given |
| `init.exit_code` | int or null | |
| `init.refused_reason` | enum or null | `disabled` \| `absent` \| `init_running` \| `already_initialized` \| `nested_worktree` \| `worktree_local_not_nested` \| `status_error` \| `cwd_mismatch` \| `null` |

Status rules: `status` → `success` only when `index_state: fresh`, `pin_match: true` and `mcp_tools_listed: true`; `partial` for any other state (the report is complete, the index is not ready); `blocked` for a flag STOP. `init` → `blocked` on a preflight refusal; `failed` when `init.exit_code` is not 0; `success` when exit 0 and the re-check reads `fresh`; `partial` when exit 0 but the re-check is not `fresh`.

Example (after `/sc:graph init --output-dir .dev/graph/run1`; paths are placeholders):

```yaml
schema_version: 1
command: graph
subcommand: init
status: success
contract_path: /path/to/worktree/.dev/graph/run1/return-contract.yaml
output_dir: /path/to/worktree/.dev/graph/run1
checked_at: 2026-10-31T09:12:44Z
access: mcp
index_state: fresh
worktree_root: /path/to/worktree
worktree_relation: own
cli_version: 1.6.2
pin: 1.6.2
pin_match: true
mcp_tools_listed: true
counts: {files: 500, nodes: 9926, edges: 23949}
pending: []
telemetry: off
telemetry_opt_out: "export CODEGRAPH_TELEMETRY=0 (or DO_NOT_TRACK=1) in your shell profile"
kill_switch: SUPERCLAUDE_CODEGRAPH_PRIMITIVES=off
next_action: none
degraded: []
init: {requested: true, form: default, ran: true, exit_code: 0, refused_reason: null}
```

## Screen report

Eight lines, fixed order:

1. `codegraph <cli_version> (pin <pin>: match|MISMATCH|unknown)`
2. `index: <index_state> (<worktree_relation>), checked <checked_at>`
3. `access: <access>; MCP lookup tools listed: yes|no`
4. `counts: <files> files, <nodes> nodes, <edges> edges`
5. `pending: <n|unknown>`
6. `telemetry: <on|off|unknown> — opt out: <telemetry_opt_out>`
7. `switch off codegraph in primitives: SUPERCLAUDE_CODEGRAPH_PRIMITIVES=off`
8. `next: <message line>`

## Will Not

- Build, rebuild, sync or remove an index, or change telemetry or MCP registration
- Run CLI `codegraph status` while `pgrep -f 'codegraph\.js (init|index)'` prints a line
- Be called by another skill or agent
