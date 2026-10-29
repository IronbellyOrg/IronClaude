# P3 interface design: `/sc:impact` and `/sc:graph` (issue #323)

Produced by `/sc:design "/sc:impact and /sc:graph command and protocol-skill interfaces …" --type api --format spec`, 2026-10-30. Planning artifact only: no source file, test or index was touched.

## 0. Inputs and binding decisions

Abbreviations (all under `.dev/codegraph-migration/`):

| Code | File | Binding content used here |
|---|---|---|
| CMD | `decisions/P3-command-set/adversarial/merged-recommendation.md` | exactly two commands, their signatures, outputs, callers |
| ACC | `decisions/P3-access-model/adversarial/P3-access-model-merged.md` | MCP for lookups, the six CLI verbs, readiness states, `graph:*` tokens, fallbacks |
| EVAL | `research/codegraph-evaluation.md` §3-§6 | tool parameters and CLI verbs |
| SPEC | `specs/phase-3-codegraph-adoption-spec.md` §1.1, §4 | job → tool map, standing rules, shared guide `~/.claude/CODEGRAPH.md` |
| BRS | `brainstorm/P3-codegraph-opportunities/merged-requirements.md` | FR-01 … FR-24, K-2, K-4 (cited, not reopened) |

Name decision (given in the brief, settles the CMD open point "Name conflict"): the index command is `/sc:graph` with skill `sc:graph-protocol`; the other is `/sc:impact` with skill `sc:impact-protocol`. Outputs are `impact.md` and `return-contract.yaml`; the directory flag is `--output-dir`.

Conventions copied from the repo:

- Thin command → `## Activation` block `> Skill sc:<x>-protocol` (`src/superclaude/commands/troubleshoot.md`, section "Activation").
- Skill frontmatter `name: sc:<x>-protocol`, `description`, `allowed-tools`, then an `<!-- Extended metadata … -->` comment (`src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md:1-12`).
- `return-contract.yaml` with `status: success|partial|blocked|failed`, absolute paths, `--caller` recorded, written under `--output-dir`; status merge order `failed > blocked > partial > success` (troubleshoot Wave 5, common epilogue and step 4.5).
- Installed-path rule (repo `CLAUDE.md`, "Never Hardcode `src/superclaude/` Paths"): skills point to `~/.claude/CODEGRAPH.md` with the one labelled in-checkout fallback from SPEC §4; any other primitive is named by installed path first, then the project `.claude/` copy.
- New commands get no plugin twin: `plugins/superclaude/commands/` ships only a subset of commands (for example no `pr-submit.md`, `auggie-review.md` or `validate-roadmap.md`; `ls plugins/superclaude/commands`, 2026-10-30), and the command-set context says twins are added only where the plugin ships the command.

### 0.1 What lives where

The rules shared by every codegraph consumer live once in the guide (SPEC §4, P3-D2; CMD "Shared rules"). The skills cite the guide section and own only their own sequence.

| Text | Lives in | Read by |
|---|---|---|
| Pin line `Pinned codegraph version: 1.6.2` and gate line `Freshness experiment E-1: pending` | guide §1 (new; see decision D-1) | both skills |
| Readiness check R1-R6 (section 3.1 below) and the state → token table | guide §2 | both skills, every caller that runs its own check |
| Closed `graph:*` vocabulary (BRS FR-02) | guide §4 | both skills, callers |
| Call-site confirmation procedure CS1-CS5 (section 4.3.6 below) | guide §4 | `sc:impact-protocol`; callers that cite graph rows themselves |
| `/sc:impact` step sequence, flags, contract | `sc-impact-protocol/SKILL.md` | — |
| `/sc:graph` status sequence, preflight, contract | `sc-graph-protocol/SKILL.md` | — |
| The literal `init` commands | `commands/graph.md` only (ACC §7: the FR-23 grep test's single exception is `init` in `commands/graph.md`) | the user-typed `/sc:graph init` run |

The guide lookup line every file below carries (SPEC §4, verbatim):

```text
Codegraph usage rules: read `~/.claude/CODEGRAPH.md` (in a dev checkout without an install, the labelled fallback is `src/superclaude/core/CODEGRAPH.md`).
```

## 1. Shared vocabulary

### 1.1 Readiness fields

| Field | Type | Allowed values | Source |
|---|---|---|---|
| `access` | enum | `mcp` \| `cli` \| `none` | ACC §6.1 (BRS K-1 gains `mcp`) |
| `index_state` | enum | `fresh` \| `stale` \| `not_initialized` \| `foreign_index` \| `absent` \| `disabled` \| `error` | ACC §6.1 (CMD's `/sc:graph` list plus `error` from ACC) |
| `worktree_relation` | enum | `own` \| `parent` \| `none` \| `unknown` | CMD `/sc:graph` Status; `unknown` added for `absent`/`disabled`/`error` |
| `checked_at` | string | ISO-8601 UTC, `YYYY-MM-DDTHH:MM:SSZ` | CMD "Freshness" |
| `cli_version` | string | semver from `codegraph --version`, or `unknown` | ACC §6.2 |
| `pin` | string | the guide's pin line value, or `unknown` | decision D-1 |
| `pin_match` | enum | `true` \| `false` \| `unknown` | BRS NFR-09 |
| `worktree_root` | string | absolute realpath of `git rev-parse --show-toplevel` | ACC §6.3 |
| `project_path` | string | same value; passed as `projectPath` on every MCP call | ACC §4, §6.3 |
| `advisory` | bool | `true` while the guide says `E-1: pending` | CMD "Freshness"; BRS FR-05 |

### 1.2 Closed token list (BRS FR-02; consumers invent none)

`graph:absent`, `graph:disabled`, `graph:unlisted`, `graph:not_initialized`, `graph:foreign_index`, `graph:stale`, `graph:version_mismatch`, `graph:provenance_unproven`, `graph:telemetry_on`, `graph:empty`, `graph:ambiguous`, `graph:truncated`, `graph:parse_failed`, `graph:unresolved`.

### 1.3 Exact tool names

MCP (ACC §2, §3): `mcp__codegraph__codegraph_node`, `mcp__codegraph__codegraph_search`, `mcp__codegraph__codegraph_callers`, `mcp__codegraph__codegraph_callees`, `mcp__codegraph__codegraph_impact`, `mcp__codegraph__codegraph_files`, `mcp__codegraph__codegraph_status`. explore is blocked by the env list and is named nowhere (BRS FR-10).

CLI (ACC §5): `codegraph --version`, `codegraph status` (only when MCP is absent), `codegraph telemetry status`, `codegraph query <name> --json`, `codegraph affected … --json --quiet`, and `codegraph init` only in the user-typed `/sc:graph init`. Never `Bash(codegraph *)`.

---

## 2. `/sc:graph`

### 2.a Frontmatter

`src/superclaude/commands/graph.md`:

```yaml
---
name: graph
description: "Show whether this worktree's codegraph index is ready (version, pin, index state, worktree relation, counts, telemetry) and, only when you type `init`, build the index for this worktree"
category: utility
complexity: basic
mcp-servers: [codegraph]
personas: []
argument-hint: "[status|init] [--worktree-local] [--output-dir <dir>]"
allowed-tools: Skill, Bash(codegraph init --yes *), Bash(codegraph init -i)
---
```

- There is no `--caller` flag: skills never call `/sc:graph` (CMD "Callers and mode").
- `allowed-tools` on a command pre-approves the two init forms only while the user-typed command runs. Whether a command's `allowed-tools` carries into the skill it invokes is UNVERIFIED; the design does not rely on it, because the init Bash call is made from the command body, not from the skill.

`src/superclaude/skills/sc-graph-protocol/SKILL.md`:

```yaml
---
name: sc:graph-protocol
description: "Readiness report for this worktree's codegraph index (cli_version, pin_match, index_state, worktree_relation, counts, pending files, telemetry, next_action) and the read-only preflight for /sc:graph init. Never runs init itself."
allowed-tools: Read, Write, Bash(codegraph --version), Bash(codegraph status), Bash(codegraph telemetry status), Bash(git rev-parse --show-toplevel), Bash(realpath *), Bash(printenv IRONCLAUDE_CODEGRAPH), mcp__codegraph__codegraph_status
---

<!-- Extended metadata (for documentation, not parsed):
category: utility
complexity: basic
mcp-servers: [codegraph]
-->
```

Command body sections (thin, troubleshoot style): `# /sc:graph`, `## Usage`, `## Options`, `## Activation` (`> Skill sc:graph-protocol`), `## Init (user-typed only)` (section 2.c step G-I), `## Boundaries`. The guide lookup line appears once in the command and once in the skill.

### 2.b Flags

| Flag | Type | Default | Validation | STOP (`status: blocked`, chat message, no Bash) |
|---|---|---|---|---|
| positional subcommand | enum `status` \| `init` | `status` | exactly zero or one positional | any other word, or two positionals → "Unknown subcommand `<x>`; use `status` or `init`" |
| `--worktree-local` | bool | `false` | only with `init` | given with `status` → "`--worktree-local` applies only to `init`" |
| `--output-dir` | path | unset (screen only) | resolved to an absolute path; must not be inside `<worktree_root>/.git/` or `<worktree_root>/.codegraph/`; created if missing | inside `.git`/`.codegraph` → blocked; not creatable/writable → `status: failed` (nothing to write the contract into, so the reason is printed only) |
| `--post-init <exit-code>` | int | unset | set only by `commands/graph.md` after its init call; integer 0-255; requires subcommand `status` | given by anyone else is not detectable; its only effect is to fill the `init` block of the contract, so misuse cannot run anything |

Run-time STOPs that are not flag errors (all return `status: blocked`, never stop a caller because there are no skill callers):

- `init` when the preflight refuses (section 2.c G-P).
- `init` reached outside a user message that starts with `/sc:graph init` (command body guard, step G-I0).

### 2.c Step sequence

`status` (default) — skill:

1. **G-R Readiness.** Run guide §2 R1-R6 (section 3.1). Record every readiness field of section 1.1.
2. **G-T Telemetry.** If the binary is present: `codegraph telemetry status` → `telemetry: on|off|unknown` (first line contains `enabled`/`on` → `on`; `disabled`/`off` → `off`; else `unknown`; exact wording UNVERIFIED, E-2). `on` adds `graph:telemetry_on` (BRS FR-22). The report prints the opt-out the user applies: add `export CODEGRAPH_TELEMETRY=0` or `export DO_NOT_TRACK=1` to the shell profile (EVAL §1). The skill never names the telemetry write verbs (BRS FR-23 regex).
3. **G-C Counts.** From the status text of R4: `Files: N  Nodes: N  Edges: N` → `counts {files, nodes, edges}` (EVAL §5.4 format; MCP text form UNVERIFIED, so a miss gives `counts: null` and `graph:parse_failed`, not an error). Pending-file lines → `pending[]` sorted, else `pending: unknown`.
4. **G-N next_action** (first match wins):

   | Condition | `next_action` | Message line |
   |---|---|---|
   | `disabled` | `enable_codegraph` | "codegraph is switched off by `IRONCLAUDE_CODEGRAPH=off`; unset it to use the graph" |
   | `absent` | `install_codegraph` | "codegraph is not installed; run `./update.sh` (IronClaude's installer owns codegraph)" |
   | MCP lookup tools not listed | `add_mcp_tool_list` | "the codegraph MCP entry lacks `CODEGRAPH_MCP_TOOLS`; re-run `./update.sh`" |
   | `not_initialized` | `run_graph_init` | "type `/sc:graph init` to index this worktree (about 4.5 s and 34 MB per 500 files, EVAL §5.4)" |
   | `foreign_index` | `run_graph_init_worktree_local` | "this nested worktree is answered from the parent index; type `/sc:graph init --worktree-local`" |
   | `pin_match: false` | `align_version` | "codegraph `<v>` differs from the pin `<pin>`; run `./update.sh`" |
   | `stale` | `wait_for_sync` | "N files pending; the watcher syncs while an MCP session is open" |
   | `error` | `check_codegraph_error` | first error line, verbatim |
   | otherwise | `none` | "index ready" |

5. **G-O Outputs.** Print the report (section 2.e). If `--output-dir` is set, write `<output-dir>/return-contract.yaml` (section 2.d).

`init` — skill preflight, then command body:

1. **G-P Preflight (skill, read-only).** Run G-R. Decide `init.form`:

   | State | Flag | Result |
   |---|---|---|
   | `disabled` | any | blocked, `refused_reason: disabled` |
   | `absent` | any | blocked, `refused_reason: absent`, `next_action: install_codegraph` |
   | `fresh` or `stale` with `worktree_relation: own` | any | blocked, `refused_reason: already_initialized` (rebuild verbs are forbidden, BRS FR-04) |
   | `foreign_index` | no `--worktree-local` | blocked, `refused_reason: nested_worktree`, `next_action: run_graph_init_worktree_local` (CMD `/sc:graph` Init) |
   | `foreign_index` | `--worktree-local` | `form: worktree_local` |
   | `not_initialized` | no flag | `form: default` |
   | `not_initialized` | `--worktree-local` | blocked, `refused_reason: worktree_local_not_nested` |
   | `error` | any | blocked, `refused_reason: status_error` |

   `form: worktree_local` also needs the session's working directory to equal `worktree_root` (`codegraph init -i` takes no documented path argument: UNVERIFIED until E-2). If it differs: blocked, `refused_reason: cwd_mismatch`, and the report prints the literal line the user can run in that directory. The skill returns `init.form`; it never runs init and never contains the literal command.
2. **G-I0 Guard (command body).** Continue only if the user's own message starts with `/sc:graph init`. Otherwise print "init runs only when you type it" and stop.
3. **G-I Run (command body, the one FR-23 exception).** `form: default` → `codegraph init --yes <worktree_root>` (EVAL §3 `init [--yes] [path]`). `form: worktree_local` → `codegraph init -i` (EVAL §5.8). One call, timeout 600000 ms (init cost scales with repo size, EVAL §4; the timeout value is a proposal). Record the exit code.
4. **G-V Verify.** Invoke `> Skill sc:graph-protocol` with `status --post-init <exit-code>` plus the user's `--output-dir` if given. The skill re-runs G-R once. Whether a running MCP watcher picks up a brand-new index without a restart is UNVERIFIED (BRS OQ-3); EVAL §4 says the server re-checks per call, so no restart is advised.

### 2.d `return-contract.yaml` (written only with `--output-dir`)

| Field | Type | Allowed values / rule |
|---|---|---|
| `schema_version` | int | `1` |
| `command` | string | `graph` |
| `subcommand` | enum | `status` \| `init` (`init` whenever `--post-init` is set or the preflight ran) |
| `status` | enum | `success` \| `partial` \| `blocked` \| `failed` (rules below) |
| `contract_path` | string | absolute path of this file |
| `output_dir` | string | absolute |
| `checked_at`, `access`, `index_state`, `worktree_root`, `worktree_relation`, `cli_version`, `pin`, `pin_match` | see section 1.1 | |
| `mcp_tools_listed` | bool | `true` when `mcp__codegraph__codegraph_callers` is in the tool list |
| `counts` | map or null | `{files: int, nodes: int, edges: int}` |
| `pending` | list[string] or `unknown` | repo-relative paths, sorted |
| `telemetry` | enum | `on` \| `off` \| `unknown` |
| `telemetry_opt_out` | string | `export CODEGRAPH_TELEMETRY=0 (or DO_NOT_TRACK=1) in your shell profile` |
| `kill_switch` | string | `IRONCLAUDE_CODEGRAPH=off` (BRS FR-24) |
| `next_action` | enum | `none` \| `run_graph_init` \| `run_graph_init_worktree_local` \| `install_codegraph` \| `enable_codegraph` \| `add_mcp_tool_list` \| `align_version` \| `wait_for_sync` \| `check_codegraph_error` |
| `degraded` | list[string] | tokens of section 1.2, sorted, unique |
| `init.requested` | bool | |
| `init.form` | enum or null | `default` \| `worktree_local` \| `null` |
| `init.ran` | bool | `true` only when `--post-init` was given |
| `init.exit_code` | int or null | |
| `init.refused_reason` | enum or null | `disabled` \| `absent` \| `already_initialized` \| `nested_worktree` \| `worktree_local_not_nested` \| `status_error` \| `cwd_mismatch` \| `null` |

Status rules: `status` subcommand → `success` when `index_state: fresh`, `pin_match: true` and `mcp_tools_listed: true`; `partial` for any other state (the report is complete, the index is not ready); `blocked` for a flag STOP. `init` → `blocked` on a preflight refusal; `failed` when `init.exit_code != 0`; `success` when exit 0 and the re-check reads `fresh`; `partial` when exit 0 but the re-check is not `fresh`.

Example (after `/sc:graph init --output-dir .dev/graph/2026-10-30`):

```yaml
schema_version: 1
command: graph
subcommand: init
status: success
contract_path: /home/coder/workspaces/worktrees/IronClaude/feat-x/.dev/graph/2026-10-30/return-contract.yaml
output_dir: /home/coder/workspaces/worktrees/IronClaude/feat-x/.dev/graph/2026-10-30
checked_at: 2026-10-30T09:12:44Z
access: mcp
index_state: fresh
worktree_root: /home/coder/workspaces/worktrees/IronClaude/feat-x
worktree_relation: own
cli_version: 1.6.2
pin: 1.6.2
pin_match: true
mcp_tools_listed: true
counts: {files: 500, nodes: 9926, edges: 23949}
pending: []
telemetry: off
telemetry_opt_out: "export CODEGRAPH_TELEMETRY=0 (or DO_NOT_TRACK=1) in your shell profile"
kill_switch: IRONCLAUDE_CODEGRAPH=off
next_action: none
degraded: []
init: {requested: true, form: default, ran: true, exit_code: 0, refused_reason: null}
```

### 2.e Screen report

Eight lines, fixed order: `codegraph <cli_version> (pin <pin>: match|MISMATCH|unknown)`, `index: <index_state> (<worktree_relation>), checked <checked_at>`, `access: <access>; MCP lookup tools listed: yes|no`, `counts: <files> files, <nodes> nodes, <edges> edges`, `pending: <n|unknown>`, `telemetry: <on|off|unknown> — opt out: <telemetry_opt_out>`, `switch off for IronClaude: IRONCLAUDE_CODEGRAPH=off`, `next: <message line>`.

---

## 3. Shared readiness check (guide §2 text, used by both skills)

### 3.1 Steps (one check per run, ACC §6.1)

| Step | Call | Classification |
|---|---|---|
| R1 | `printenv IRONCLAUDE_CODEGRAPH` | value `off` → `index_state: disabled`, `access: none`, token `graph:disabled`; skip R3-R6 (BRS FR-24) |
| R2 | `git rev-parse --show-toplevel`, then `realpath <that>` | `worktree_root` = `project_path`. Not a git tree → `realpath .` and `worktree_relation: unknown` |
| R3 | `codegraph --version` | command not found → binary absent. Otherwise `cli_version`; compare with the guide pin: differs → `graph:version_mismatch` + `graph:provenance_unproven`; call refused or unparsable → `cli_version: unknown`, `graph:provenance_unproven` (ACC §6.2) |
| R4 | if `mcp__codegraph__codegraph_status` is in this session's tool list: `mcp__codegraph__codegraph_status {"projectPath": "<project_path>"}` → `access: mcp`. Else, if the binary is present: `codegraph status` run in `worktree_root` → `access: cli`. Else `access: none`, `index_state: absent`, `graph:absent` | MCP presence is read from the tool list at run time, never from the kind of run (ACC §6.4) |
| R5 | classify the R4 text | contains `belongs to a different git working tree` → `foreign_index`, `worktree_relation: parent`, `graph:foreign_index`; contains `Not initialized` → `not_initialized`, `worktree_relation: none`, `graph:not_initialized`; contains `Index is up to date` and no pending list → `fresh`, `own`; a pending list → `stale`, `own`, `graph:stale`; anything else → `error`, `graph:parse_failed` (EVAL §5.4, §5.8; MCP wording of the worktree warning UNVERIFIED, ACC §6.1) |
| R6 | lookup tools present? | `mcp__codegraph__codegraph_callers` missing from the tool list while the binary or MCP status answered → `graph:unlisted` and the absent path for lookups (ACC §2, §8) |

Freshness overrides: while the guide reads `E-1: pending`, `advisory: true`. Under E-1 Outcome B, `access: cli` runs are `stale` for the whole run (ACC §6.4). `checked_at` is the time of R4.

### 3.2 State → token → effect

| State | Token(s) | Lookups | Rows |
|---|---|---|---|
| fresh, pin match | none | MCP | usable as leads; cited only after CS1-CS5 |
| stale | `graph:stale` | MCP | leads only; no counts feed a gate |
| version differs / unknown | `graph:version_mismatch` + `graph:provenance_unproven` / `graph:provenance_unproven` | MCP | leads only, no citations, sets or counts (BRS FR-03) |
| not_initialized, foreign_index | `graph:not_initialized`, `graph:foreign_index` | none (handled as not initialized) | Grep/Read fallback |
| absent, unlisted, disabled | `graph:absent`, `graph:unlisted`, `graph:disabled` | none | Grep/Read fallback |
| error | `graph:parse_failed` | none | Grep/Read fallback |

---

## 4. `/sc:impact`

### 4.a Frontmatter

`src/superclaude/commands/impact.md`:

```yaml
---
name: impact
description: "List the definitions of symbols (or of the symbols a diff touches) and their production and test dependents from the codegraph index, with an advisory test list on --tests. Fails open to Grep when codegraph or the index is missing."
category: analysis
complexity: standard
mcp-servers: [codegraph]
personas: [analyzer]
argument-hint: "<symbol>... | --diff [<base>] [--depth 1-3] [--limit N] [--tests] [--test-depth N] [--output-dir <dir>] [--caller <name>]"
---
```

`src/superclaude/skills/sc-impact-protocol/SKILL.md`:

```yaml
---
name: sc:impact-protocol
description: "Codegraph-backed dependents report: definitions, production and test dependents with shown/total and call-site resolution, optional advisory test list from codegraph affected; writes impact.md and return-contract.yaml; never stops its caller."
allowed-tools: Read, Grep, Glob, Write, Bash(printenv IRONCLAUDE_CODEGRAPH), Bash(git rev-parse *), Bash(realpath *), Bash(git diff *), Bash(codegraph --version), Bash(codegraph status), Bash(codegraph query *), Bash(codegraph affected *), mcp__codegraph__codegraph_status, mcp__codegraph__codegraph_search, mcp__codegraph__codegraph_node, mcp__codegraph__codegraph_callers, mcp__codegraph__codegraph_impact
---

<!-- Extended metadata (for documentation, not parsed):
category: analysis
complexity: standard
mcp-servers: [codegraph]
-->
```

Pattern notes:

- `Bash(codegraph query *)` and `Bash(codegraph affected *)` are per-subcommand patterns (BRS FR-04). Whether Claude Code matches them is E-3; until E-3 passes, a refused `query` call leaves rows `unresolved` and diff files `unmapped`, and a refused `affected` call gives `selection_source: heuristic_only`. Nothing stops.
- `Bash(git diff *)` covers only the read forms in 4.c D1-D2. `Bash(git rev-parse *)` covers `--show-toplevel` and `--verify --quiet`.
- `mcp__codegraph__codegraph_callees` and `_files` are not listed: no step uses them.

### 4.b Flags

| Flag | Type | Default | Validation | STOP → `status: blocked` (contract still written when `--output-dir` resolves) |
|---|---|---|---|---|
| `<symbol>...` | list[string] | none | 1-30 items (30 = BRS NFR-01's 30-symbol budget; see D-4); each matches `^[A-Za-z_$][A-Za-z0-9_$]*$` | none and no `--diff`; both symbols and `--diff`; more than 30; a dotted or path-qualified name ("codegraph has no `Class/method` addressing, EVAL §6.2; pass the bare name") |
| `--diff [<base>]` | optional ref | `HEAD` when the flag is given without a value | `git rev-parse --verify --quiet <base>^{commit}` succeeds | ref does not resolve |
| `--depth` | int | `2` | 1-3 (CMD) | outside 1-3 or not an integer |
| `--limit` | int | `20` | 1-100 (MCP `callers` max 100, EVAL §3) | outside 1-100 |
| `--tests` | bool | `false` | — | — |
| `--test-depth` | int | unset (codegraph's own default, UNVERIFIED, BRS OQ-10) | 1-5 (upper bound proposed, not measured) and only with `--tests` | without `--tests`; outside 1-5 |
| `--output-dir` | path | `<worktree_root>/.dev/impact/<slug>-<YYYYMMDDTHHMMSSZ>/`; `<slug>` = first symbol or `diff-<base>`, lowercased, non-alnum → `-`, max 40 chars | absolute after resolution; not inside `.git/` or `.codegraph/`; created if missing; existing `impact.md` and `return-contract.yaml` are overwritten (same inputs give byte-identical files, BRS NFR-03) | inside `.git`/`.codegraph` → blocked; not creatable/writable → `status: failed`, reason printed (no file can be written) |
| `--caller` | string | unset | `^[a-z0-9][a-z0-9:-]{0,63}$` | malformed → blocked |

`--caller` changes only the chat output: with it set, the skill prints three lines (status, `degraded`, contract path) instead of the summary table, so the calling context grows as little as possible.

### 4.c Step sequence

| # | Step | Exact calls | Output / fallback |
|---|---|---|---|
| 1 | Validate flags | none | 4.b STOPs |
| 2 | Readiness | guide §2 R1-R6 (section 3.1) | readiness fields; tokens; lookups allowed only for `fresh`, `stale`, or a version token with an otherwise fresh state |
| 3 | Inputs, symbol mode | per symbol: `mcp__codegraph__codegraph_search {"query": "<sym>", "limit": 10, "projectPath": "<project_path>"}`; keep rows whose name equals `<sym>` exactly | 0 matches → Grep `^\s*(def\|class\|function\|func\|fn)\s+<sym>\b\|\b<sym>\s*=\s*(function\|\()` → `mapped_by: grep`, token `graph:empty` (never "does not exist"). >1 → `ambiguous[]` lists all; keep at most 3 definitions (sorted by file, then line), token `graph:ambiguous` |
| 3' | Inputs, diff mode | D1 `git diff --name-only --merge-base <base>` (base `HEAD` → `git diff --name-only HEAD`); D2 `git diff -U0 --merge-base <base>` (or `-U0 HEAD`), parse `@@ -a,b +c,d @@` new-side ranges; D3 per changed file (max 30 files): `mcp__codegraph__codegraph_node {"file": "<repo-relative path>", "symbolsOnly": true, "projectPath": "<project_path>"}` → candidate names; D4 per candidate (max 30 per run, issued as same-turn parallel Bash calls, at most 15 per turn): `codegraph query <name> --json --limit 20` in `worktree_root`; keep entries whose `file` equals the changed file and whose `startLine..endLine` overlaps a hunk | each hit → `changed_symbols[]` with `start`, `end`, `mapped_by: hunk` (CMD "Diff input": IronClaude-side mapping through `query --json` spans). If D3 outline rows already carry start/end lines (UNVERIFIED, E-2), D4 is skipped for that file. Files with no hit, deleted files, files over the cap and non-indexed files (Markdown, EVAL §5.4) → `unmapped_files[]` with `reason: no_span_match\|deleted\|cap\|not_indexed\|query_refused`; they get file-level scope only. Non-Python accuracy is UNVERIFIED (BRS OQ-4) |
| 4 | Direct callers | per definition: `mcp__codegraph__codegraph_callers {"symbol": "<sym>", "file": "<def file>", "limit": <--limit>, "projectPath": "<project_path>"}` | parse `Callers of <sym> (<n> found)` and `Showing <shown> of <total>`. If `total > shown` and `total <= 100`: re-query once with `"limit": <total>`. If still short or `total > 100`: `truncated: true`, token `graph:truncated` (BRS FR-08). No rows → `graph:empty` |
| 5 | Transitive dependents | per definition: `mcp__codegraph__codegraph_impact {"symbol": "<sym>", "file": "<def file>", "depth": <--depth>, "projectPath": "<project_path>"}` | rows at hop ≥ 2 added with `source: impact`, `hop`. Unparsable → `graph:parse_failed`, step-4 rows kept |
| 6 | Partition | Read `~/.claude/skills/sc-reflect-protocol/refs/runtime-surface.md` (else `.claude/skills/sc-reflect-protocol/refs/runtime-surface.md`) §2 language table once per run | each row `partition: prod\|test\|unknown` by path markers (BRS FR-09 single definition). Inline test markers need a Read and are not checked, so lists are floors; unknown language → `unknown` |
| 7 | Call-site confirmation | guide §4 CS1-CS5 (section 4.3.6) for the rows shown in `impact.md` tables: first 5 `prod` rows per symbol (sort order below), at most 20 per run | `resolution: call-site-verified` with `call_site_line`; budget-exceeded rows stay `def-line` (graph) or `unresolved` (grep) and count only; failing rows are dropped from the tables and counted in `call_sites.dropped` (CMD "Call sites") |
| 8 | Tests (only `--tests`) | changed files = definition files (symbol mode) or D1 files that exist (diff mode); `codegraph affected <file>... --json --quiet` (+ `--depth <--test-depth>` when set), files passed positionally, never a pipeline | `tests[]` with `source: affected`. Heuristic: for each changed `<stem>.<ext>`, Glob `**/test_<stem>.*`, `**/<stem>_test.*`, `**/<stem>.test.*`, `**/<stem>.spec.*`, plus every `test` partition file from steps 4-5 → `source: heuristic`; both → `both`. `selection_source: advisory` when `affected` contributed, else `heuristic_only`. JSON shape UNVERIFIED (E-2) → `graph:parse_failed`, heuristic only. Skipped when `index_state` is not `fresh`/`stale` |
| 9 | Fallback (lookups not allowed in step 2) | Grep `\b<sym>\s*\(` over the worktree, excluding `.git/`, `.codegraph/`, `.dev/`; cap 100 hits per symbol | rows `source: grep`, `resolution: unresolved`, `caller: null`, partition by step 6; definitions from the step-3 Grep. `status: partial` |
| 10 | Write outputs | Write `<output-dir>/impact.md` (4.e) then `<output-dir>/return-contract.yaml` (4.d) | rows sorted by `symbol`, `partition` (prod first), `file`, `def_line` (BRS NFR-03); `return-contract.yaml` holds at most 40 rows and 6 KB (BRS FR-10), the rest only in `impact.md` |

Sort before the step-7 selection, so the confirmed rows are deterministic.

#### 4.3.6 Call-site confirmation (guide §4 text; CMD: "written in the guide, not in a script")

- **CS1** `codegraph query <caller> --json --limit 20`; keep the entry whose `file` equals the row's file and whose `startLine` equals the row's `def_line`. None → `unresolved` (BRS FR-06).
- **CS2** Grep `\b<callee>\s*\(` with `-n` in that file; keep matches inside `startLine..endLine`.
- **CS3** Reject matches in comments, string literals or docstrings, bare-name assignments and attribute-only matches. Several matches → cite each as a candidate, or none.
- **CS4** Read the matched line. It must still contain the call → `call-site-verified`, `call_site_line` set.
- **CS5** Any failure → drop the row from cited output; never repair it. `def-line` rows are cited only as definitions.

Rows are leads, not citations, until CS4 (SPEC §1.1 standing rule 1). In callers whose citations bypass the evidence-validator (auggie-review, reflect), even `call-site-verified` rows are context only (BRS FR-06).

### 4.d `return-contract.yaml`

| Field | Type | Allowed values / rule |
|---|---|---|
| `schema_version` | int | `1` |
| `command` | string | `impact` |
| `status` | enum | `success` \| `partial` \| `blocked` \| `failed` |
| `caller` | string or null | the `--caller` value |
| `output_dir`, `report_path`, `contract_path` | string | absolute |
| `input.mode` | enum | `symbols` \| `diff` |
| `input.symbols` | list[string] | symbol mode only, else `[]` |
| `input.diff_base` | string or null | resolved commit SHA in diff mode |
| `input.changed_files` | list[string] | diff mode, repo-relative, sorted |
| `input.depth`, `input.limit` | int | |
| `input.tests` | bool | |
| `input.test_depth` | int or null | |
| `readiness` | map | every field of section 1.1 (`access`, `index_state`, `checked_at`, `cli_version`, `pin`, `pin_match`, `worktree_root`, `project_path`, `worktree_relation`) |
| `advisory` | bool | `true` while `E-1: pending`; when `true`, no consumer may change a severity, gate or verdict from this contract, and no "no dependents" / "no tests" conclusion is drawn (CMD "Freshness"; BRS FR-05, FR-07) |
| `degraded` | list[string] | section 1.2 tokens, sorted, unique |
| `symbols[]` | list[map] | per definition: `name`, `file`, `start_line` (int or null), `end_line` (int or null), `mapped_by` (`name` \| `hunk` \| `grep`), `prod` `{shown: int, total: int}`, `test` `{shown, total}`, `unknown` `{shown, total}`, `transitive` `{count: int, depth: int}`, `truncated` (bool) |
| `ambiguous[]` | list[map] | `{name, definitions: [{file, line}]}` |
| `unmapped_files[]` | list[map] | `{file, reason}`; reason as in step 3' |
| `dependents[]` | list[map], max 40 | `symbol`, `caller` (string or null), `file`, `def_line` (int or null), `call_site_line` (int or null), `resolution` (`def-line` \| `call-site-verified` \| `unresolved`), `partition` (`prod` \| `test` \| `unknown`), `hop` (1-3), `source` (`callers` \| `impact` \| `grep`) |
| `dependents_omitted` | int | rows only in `impact.md` |
| `call_sites` | map | `{verified: int, unresolved: int, dropped: int, budget: "5/symbol, 20/run"}` |
| `tests[]` | list[map] or `[]` | with `--tests`: `{path, source: heuristic \| affected \| both}` sorted by path |
| `selection_source` | enum or null | `advisory` \| `heuristic_only`; `null` without `--tests` |
| `errors[]` | list[string] | one line per failed call, verbatim first line |

Status merge (`failed > blocked > partial > success`):

- `blocked`: a flag STOP.
- `failed`: outputs could not be written, or every lookup and every Grep fallback errored.
- `partial`: any token in `degraded` other than `graph:unresolved` (budget-limited rows are normal), or any `unmapped_files`, or any fallback row.
- `success`: otherwise. `advisory: true` does not by itself lower the status, because it is true for every run until E-1.

Example (`/sc:impact install_codebase_memory_mcp --caller sc-implement-protocol --output-dir …`, values from EVAL §5.5):

```yaml
schema_version: 1
command: impact
status: success
caller: sc-implement-protocol
output_dir: /home/coder/workspaces/worktrees/IronClaude/feat-x/.dev/tasks/to-do/T-42/impact/task-3
report_path: /home/coder/workspaces/worktrees/IronClaude/feat-x/.dev/tasks/to-do/T-42/impact/task-3/impact.md
contract_path: /home/coder/workspaces/worktrees/IronClaude/feat-x/.dev/tasks/to-do/T-42/impact/task-3/return-contract.yaml
input: {mode: symbols, symbols: [install_codebase_memory_mcp], diff_base: null, changed_files: [], depth: 1, limit: 10, tests: false, test_depth: null}
readiness:
  access: mcp
  index_state: fresh
  checked_at: 2026-10-30T09:20:03Z
  cli_version: 1.6.2
  pin: 1.6.2
  pin_match: true
  worktree_root: /home/coder/workspaces/worktrees/IronClaude/feat-x
  project_path: /home/coder/workspaces/worktrees/IronClaude/feat-x
  worktree_relation: own
advisory: true
degraded: [graph:unresolved]
symbols:
  - name: install_codebase_memory_mcp
    file: src/superclaude/cli/install_mcp.py
    start_line: 815
    end_line: 913
    mapped_by: name
    prod: {shown: 2, total: 2}
    test: {shown: 21, total: 21}
    unknown: {shown: 0, total: 0}
    transitive: {count: 0, depth: 1}
    truncated: false
ambiguous: []
unmapped_files: []
dependents:
  - {symbol: install_codebase_memory_mcp, caller: install_mcp_server, file: src/superclaude/cli/install_mcp.py, def_line: 1010, call_site_line: 1026, resolution: call-site-verified, partition: prod, hop: 1, source: callers}
  - {symbol: install_codebase_memory_mcp, caller: install, file: src/superclaude/cli/main.py, def_line: 46, call_site_line: 255, resolution: call-site-verified, partition: prod, hop: 1, source: callers}
  # … test rows, 40-row cap
dependents_omitted: 0
call_sites: {verified: 2, unresolved: 21, dropped: 0, budget: "5/symbol, 20/run"}
tests: []
selection_source: null
errors: []
```

(The step-4 re-query lifts `--limit 10` to the full 23 rows because 23 ≤ 100; the 2 prod / 21 test split is the EVAL §5.5 sample. `call_sites.unresolved` counts rows not confirmed under the budget; those rows keep `resolution: def-line`.)

### 4.e `impact.md` layout

YAML front matter: `status`, `caller`, `index_state`, `checked_at`, `advisory`, `degraded`, `contract_path`. Then, in this order:

1. `## Summary`: one paragraph, then a table `symbol | definition | prod (shown/total) | test (shown/total) | transitive | truncated`.
2. `## How to read this`: three fixed sentences: rows locate code and are not citations until marked `call-site-verified`; an empty list never proves there are no dependents; while `advisory: true`, nothing here may change a severity, gate or verdict.
3. `## Readiness`: the section 1.1 fields as a two-column table.
4. `## Input`: symbol mode lists the symbols; diff mode lists `changed_files` and the `changed_symbols` table `name | file | start | end | mapped_by`.
5. `## Definitions`: `name | file:start-end | kind | mapped_by`; `### Ambiguous` when any.
6. `## Production dependents`: per symbol, `caller | file | def_line | call_site_line | resolution | hop | source`.
7. `## Test dependents`: same columns.
8. `## Unclassified dependents`: `partition: unknown` rows; omitted when empty.
9. `## Tests (advisory)`: only with `--tests`: `path | source`, then `selection_source` and the sentence "Adds tests to a selection; never removes any."
10. `## Unmapped files`: `file | reason`; omitted when empty.
11. `## Limits`: `shown/total` per list, truncation, call-site budget use (`verified/unresolved/dropped`).
12. `## Degraded and fallbacks`: each token with its one-line meaning from the guide and the fallback used.

### 4.f Failure behaviour

All rows: the run continues, outputs are written, and the caller is never stopped (CMD "Fail-open"; BRS FR-02).

| Condition | Detected by | `/sc:impact` status | `/sc:impact` token(s) | `/sc:impact` behaviour | `/sc:graph status` status / `next_action` |
|---|---|---|---|---|---|
| codegraph absent | R3 not found and no MCP status tool | partial | `graph:absent` | step 9 Grep rows; `--tests` heuristic only | partial / `install_codegraph` |
| env list missing | R6: callers tool not listed | partial | `graph:unlisted` | step 9 | partial / `add_mcp_tool_list` |
| switched off | R1 | partial | `graph:disabled` | step 9 | partial / `enable_codegraph` |
| not initialized | R5 `Not initialized` | partial | `graph:not_initialized` | step 9; report names `/sc:graph init` | partial / `run_graph_init` |
| foreign index (nested or snapshot worktree) | R5 warning text | partial | `graph:foreign_index` | handled as not initialized (ACC §8) | partial / `run_graph_init_worktree_local` |
| stale | R5 pending list | partial | `graph:stale` | graph rows kept as leads; counts never feed a gate | partial / `wait_for_sync` |
| version mismatch / unknown | R3 | partial | `graph:version_mismatch` + `graph:provenance_unproven` / `graph:provenance_unproven` | rows kept as leads; no CS1-CS5 citations; counts not used by callers | partial / `align_version` |
| truncated | step 4 after one re-query | partial | `graph:truncated` | `total` reported as a floor | n/a |
| parse failure | R5 unknown text, step 4/5/8 unparsable | partial | `graph:parse_failed` | affected step falls back to Grep (R5) or keeps earlier rows (steps 5, 8) | partial / `check_codegraph_error` |
| ambiguous name | step 3 | partial | `graph:ambiguous` | up to 3 definitions | n/a |
| empty result | steps 3-4 | partial | `graph:empty` | "no dependents found in the index", never "none exist" | n/a |
| budget-limited rows | step 7 | unchanged | `graph:unresolved` | counted, not cited | n/a |
| bad flags | step 1 | blocked | none | no lookups | blocked |
| output dir unwritable | step 10 | failed | none | reason printed | failed |

---

## 5. How callers invoke `/sc:impact`

Invocation form (repo convention, e.g. `sc-troubleshoot-protocol/SKILL.md` Wave 6 "invoke `Skill sc:workflow-protocol` …"): the caller writes the line

```text
> Skill sc:impact-protocol
```

with the arguments shown. Every caller then reads `<output-dir>/return-contract.yaml`, not `impact.md`, and copies `degraded` tokens into its own `degraded` / `degraded_components` list (BRS FR-02). Every caller treats `status: blocked|failed` like `graph:absent` (continue natively). `/sc:graph` has no skill callers; `/sc:load` and the guide's `not_initialized` message only name `/sc:graph status` to the user (CMD).

| Caller and step (CMD "Active callers") | Exact Skill call arguments | Fields read | Use |
|---|---|---|---|
| sc-reflect-protocol Step 1B.3 and chain 4/4b | `--diff <baseline_ref> --depth 1 --limit 100 --output-dir <output>/artifacts/impact --caller sc-reflect-protocol` | `status`, `advisory`, `degraded`, `readiness.index_state`, `readiness.checked_at`, `symbols[].prod`, `symbols[].test`, `symbols[].truncated` | log prod and test counts only; the "more than 5 referencing call sites" severity rule is unchanged (BRS FR-14, FR-09) |
| sc-pr-submit-protocol Wave 4, before a fix | `<symbols the fix edits> --depth 2 --output-dir <run-dir>/impact/round-<n> --caller sc-pr-submit-protocol` | `status`, `degraded`, `symbols[].prod.total`, `symbols[].transitive.count`, `report_path` | one warning line before edits |
| sc-troubleshoot-protocol `--fix` handoff (Wave 6 Phase A) | `<symbols named in Proposed Fix> --depth 2 --output-dir <output-dir>/impact --caller sc-troubleshoot-protocol` | `status`, `degraded`, `symbols[].prod.total`, `report_path` | warning line; `report_path` listed under `## References` in `remediation-source.md` |
| sc-auggie-review-protocol Wave 1 | `--diff <base> --depth 1 --output-dir <output-dir>/inputs/impact --caller sc-auggie-review-protocol` | `status`, `readiness.index_state`, `dependents[].caller`, `dependents[].file` | names and files only into the Auggie prompt; out-of-hunk downgrade unchanged (BRS FR-12 stage 1) |
| sc-pr-submit-protocol Wave 3 | `--diff <base> --depth 1 --output-dir <run-dir>/impact/wave3 --caller sc-pr-submit-protocol` | `status`, `dependents[].caller`, `dependents[].file`, `unmapped_files` | context only |
| sc-implement-protocol Q1 (rename, delete, signature tasks) | `<symbol> --depth 1 --limit 10 --output-dir <package>/impact/<task-id> --caller sc-implement-protocol` | `status`, `degraded`, `readiness.index_state`, `readiness.checked_at`, `symbols[].prod`, `symbols[].test`, `report_path` | warning and Q3 package input; ledger line carries `index_state` and `checked_at`; never widens Q1 edits (BRS FR-16) |
| sc-implement-protocol Q6 | `--diff HEAD --tests --output-dir <package>/impact/<task-id>-tests --caller sc-implement-protocol` | `status`, `tests[]`, `selection_source` | advisory extras; can add tests, never removes |
| sc-pr-submit-protocol VG-1 | `--diff <base> --tests --output-dir <run-dir>/impact/vg1 --caller sc-pr-submit-protocol` | `status`, `tests[]`, `selection_source` | print `tests[]` paths outside `<changed-area>`; the VG-1 gate is unchanged (BRS FR-13 stage 0) |
| sc-task-protocol STRICT step 7 (UNVERIFIED: not in SPEC §2.2) | `<changed symbols> --depth 2 --output-dir .dev/impact/task-<slug> --caller sc-task-protocol` | `status`, `dependents[].file`, `unmapped_files` | candidate files to check; confirmed with Grep (SPEC §1.2 row 34) |

Troubleshoot Tier 1 keeps its inline calls and `tier1-callers.md` and does not invoke `/sc:impact` (CMD; BRS FR-15).

Subagent wrapping (running the Skill inside a `Task` so only the contract path returns) is NOT the default: MCP availability in subagent spawn modes is unproven (ACC §9.2; `sc-cleanup-audit-protocol/SKILL.md:86`). It becomes an option per caller once the ACC §9.2 matrix passes for the foreground spawn mode that caller uses.

---

## 6. Token-cost argument

All figures are UNVERIFIED estimates (no run was made); CMD and BRS OQ-6 / NFR-06 leave per-call cost open.

| Work | Caller does it inline | Caller invokes `/sc:impact` |
|---|---|---|
| Procedure text in context | the guide (≤120 lines, about 1.5-2K tokens, UNVERIFIED) plus its own written steps, in every one of 6 caller skills (maintenance cost ×6) | `sc-impact-protocol/SKILL.md` loaded once at invocation (target ≤300 lines, about 4K tokens, UNVERIFIED) |
| Readiness | 3-4 calls (`printenv`, `rev-parse`, `--version`, status) per caller step | same calls, inside the skill |
| Lookups per symbol | search + callers (+ one re-query) + impact; raw MCP text of every call stays in context | same calls; raw text stays in context too (a Skill runs in the caller's context) |
| Partition | Read of `runtime-surface.md` §2 (about 1K tokens, UNVERIFIED) | same, once per run |
| Call-site confirmation | up to 5 × (query + Grep + Read) per symbol | same, under the fixed 5/20 budget |
| What later steps re-read | raw rows | `return-contract.yaml`, at most 40 rows and 6 KB (about 1.5K tokens, BRS FR-10) |

Conclusion: in the default direct-Skill form the per-call token cost is about equal to inline work plus the skill text (roughly +2-4K tokens per first call in a run, UNVERIFIED). The gain is (1) one tested procedure instead of six hand-written copies that drift, (2) later steps and ledgers read a 6 KB contract instead of raw graph text, (3) the `--caller` three-line chat output, and (4) with the subagent form after ACC §9.2, the raw lookup text leaves the caller's context entirely and only the contract path returns (saving the lookup payloads, size UNVERIFIED; BRS NFR-06's 2K-tokens-per-run graph text cap is the target). `/sc:graph` has no skill callers, so it has no caller-side cost; a skill that needs readiness runs guide §2 itself (about 4 Bash/MCP calls).

---

## 7. Tests

Style: `tests/commands/test_research_command.py` (module docstring naming the drift it guards, `_REPO = Path(__file__).resolve().parents[2]`, plain `read_text` assertions, no network). Shared helper per file: `_frontmatter(path) -> dict` that splits on the first two `---` lines and reads `key: value` pairs; `_allowed(path) -> set[str]` that splits `allowed-tools` on `, `.

Both files also need: `graph.md` and `impact.md` added to the `"commands"` lists and `sc-graph-protocol/SKILL.md`, `sc-impact-protocol/SKILL.md` added to the `"skills"` lists in `tests/unit/test_cli_install.py` (both blocks, lines 111 and 393 at HEAD; re-locate by the `"commands": _names(` anchor).

### 7.1 `tests/commands/test_impact_command.py`

Paths: `src/superclaude/commands/impact.md`, `src/superclaude/skills/sc-impact-protocol/SKILL.md`.

| Test | Asserts |
|---|---|
| `test_impact_command_frontmatter` | `name == "impact"`; `mcp-servers` contains `codegraph`; `argument-hint` contains `--diff`, `--depth`, `--limit`, `--tests`, `--test-depth`, `--output-dir`, `--caller` |
| `test_impact_command_invokes_protocol_skill` | command body contains `> Skill sc:impact-protocol` under `## Activation` |
| `test_impact_skill_name` | skill frontmatter `name == "sc:impact-protocol"` |
| `test_impact_allowed_tools_exact` | `_allowed(skill)` equals the 4.a set exactly |
| `test_impact_no_wildcards` | neither file contains `Bash(codegraph *)`, `mcp__codegraph__*` or `Bash(codegraph)` |
| `test_impact_no_mutating_verbs` | regex `codegraph (init\|index\|sync\|uninit\|unlock\|upgrade\|install\|uninstall\|telemetry (on\|off))` has 0 hits in both files (BRS FR-23) |
| `test_impact_no_explore` | neither file contains `codegraph_explore`, `codegraph explore` or `codegraph context` (BRS FR-10) |
| `test_impact_node_file_mode_has_symbols_only` | every `codegraph_node` occurrence with `"file"` also has `"symbolsOnly": true` on the same line (ACC §7) |
| `test_impact_guide_lookup_line` | skill contains `~/.claude/CODEGRAPH.md`; every `src/superclaude/` occurrence is the exact labelled fallback string `src/superclaude/core/CODEGRAPH.md` |
| `test_impact_runtime_surface_dual_surface` | skill names `~/.claude/skills/sc-reflect-protocol/refs/runtime-surface.md` before `.claude/skills/sc-reflect-protocol/refs/runtime-surface.md` |
| `test_impact_contract_fields_documented` | parametrized over the 4.d field names: each appears in the skill |
| `test_impact_status_enum` | skill contains `success`, `partial`, `blocked`, `failed` in the contract section and the merge order `failed > blocked > partial > success` |
| `test_impact_tokens_closed_vocabulary` | every `graph:[a-z_]+` in the skill is in the section 1.2 set |
| `test_impact_failure_table_rows` | parametrized over the 4.f conditions: the skill's failure table has a row naming the condition and its token |
| `test_impact_md_sections_in_order` | the 12 headings of 4.e appear in the skill in order |
| `test_impact_call_site_budget` | skill contains `5` per symbol and `20` per run and names `call-site-verified`, `def-line`, `unresolved` |
| `test_impact_advisory_rule` | skill contains `advisory` and the sentence that no severity, gate or verdict changes while it is `true` |
| `test_impact_callers_wired` (lands with the caller edits, spec task T10) | parametrized over (caller SKILL.md installed-name, `--caller` value) from section 5: the caller file contains `Skill sc:impact-protocol` and `--caller <value>`; troubleshoot SKILL.md Wave 1 does not |

### 7.2 `tests/commands/test_graph_command.py`

Paths: `src/superclaude/commands/graph.md`, `src/superclaude/skills/sc-graph-protocol/SKILL.md`.

| Test | Asserts |
|---|---|
| `test_graph_command_frontmatter` | `name == "graph"`; `mcp-servers` contains `codegraph`; `argument-hint` contains `status`, `init`, `--worktree-local`, `--output-dir` and NOT `--caller` |
| `test_graph_command_invokes_protocol_skill` | command body contains `> Skill sc:graph-protocol` |
| `test_graph_command_allowed_tools_exact` | `_allowed(command) == {"Skill", "Bash(codegraph init --yes *)", "Bash(codegraph init -i)"}` |
| `test_graph_skill_allowed_tools_exact` | `_allowed(skill)` equals the 2.a skill set exactly; contains no `init` pattern |
| `test_graph_init_only_in_command` | FR-23 regex: 0 hits in the skill; in the command every hit is `codegraph init` |
| `test_graph_init_user_typed_guard` | command `## Init (user-typed only)` section contains `/sc:graph init` and the guard that the user's own message must start with it |
| `test_graph_nested_worktree_refusal` | skill names `nested_worktree`, `--worktree-local` and `worktree_local_not_nested` |
| `test_graph_no_sync_or_explore` | neither file contains `codegraph sync`, `codegraph_explore` or `Bash(codegraph *)` |
| `test_graph_index_state_enum` | skill lists all 7 `index_state` values and the 4 `worktree_relation` values |
| `test_graph_next_action_enum` | parametrized over the 9 `next_action` values: each in the skill |
| `test_graph_contract_fields_documented` | parametrized over the 2.d field names: each in the skill |
| `test_graph_telemetry_opt_out` | skill contains `CODEGRAPH_TELEMETRY=0` and `DO_NOT_TRACK=1`, and `IRONCLAUDE_CODEGRAPH=off` |
| `test_graph_guide_lookup_line` | as `test_impact_guide_lookup_line` for both files |
| `test_graph_no_skill_callers` | no `SKILL.md` under `src/superclaude/skills/` other than `sc-graph-protocol` contains `sc:graph-protocol` |

---

## 8. Decisions this design made (inputs did not settle them)

| ID | Decision | Why |
|---|---|---|
| D-1 | The pin and the E-1 gate are two lines in guide §1 (`Pinned codegraph version: 1.6.2`, `Freshness experiment E-1: pending`), read by both skills | the Phase 2 pin file is unknown (SPEC §0 G1); the rejected K-1 capability map was where BRS put `tested_version` |
| D-2 | The literal init commands and their Bash patterns live in `commands/graph.md`; `sc:graph-protocol` only does a read-only preflight and a post-init re-check via an internal `--post-init <exit-code>` flag | keeps ACC §7's single FR-23 exception (`init` in `commands/graph.md`) and makes init unreachable from a direct Skill call |
| D-3 | `sc:impact-protocol` carries its own exact allowlist including `Bash(codegraph query *)` and `Bash(codegraph affected *)`; denied calls degrade to `unresolved` / `heuristic_only` | ACC §5 classifies orchestrators, not the new protocol skill; CMD requires `query --json` spans for `--diff` and `affected` for `--tests` |
| D-4 | `/sc:impact` caps: 30 symbols, 30 changed files, 30 span queries per run; `--test-depth` 1-5 | BRS NFR-01's 30-symbol budget; the 1-5 bound is a proposal |
| D-5 | `--diff` without a value means `HEAD` (working tree vs HEAD); with `<base>` it uses `git diff --merge-base <base>` | CMD gives `--diff [<base>]` without a default |
| D-6 | `/sc:impact` does not run `codegraph telemetry status`; only `/sc:graph` reports telemetry | saves one CLI call per run; BRS FR-22 is satisfied by `/sc:graph status` |
| D-7 | `/sc:graph status` returns `partial` for every not-ready state; `success` only for fresh + pin match + tools listed | CMD gives no status rule for `/sc:graph` |
| D-8 | `/sc:graph init` refuses an already-initialized own index (`already_initialized`) | rebuild verbs are forbidden (BRS FR-04); re-running init on an index is undocumented |
| D-9 | Callers use direct `Skill` invocation; a `Task`-wrapped form waits for ACC §9.2 | subagent MCP access is unproven |

## 9. Open points carried forward

- E-2: exact text and JSON shapes of MCP `codegraph_status`, `codegraph_callers`, `codegraph_impact`, CLI `affected --json`, `telemetry status`, and whether `init -i` takes a path or prompts.
- E-3: whether `Bash(codegraph query *)`, `Bash(codegraph affected *)`, `Bash(codegraph init --yes *)` match in practice.
- Whether a command's `allowed-tools` applies to Bash calls made in its body after a Skill returns (UNVERIFIED).
- Whether `codegraph_node {file, symbolsOnly:true}` rows carry start/end lines (decides whether D4 span queries are needed).
- Token figures in section 6 (all UNVERIFIED).
