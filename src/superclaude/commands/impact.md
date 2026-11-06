---
name: impact
description: "List the definitions of symbols (or of the symbols a diff touches) and their production and test dependents from the code graph, with an advisory test list on --tests. Fails open to Grep when codegraph or the graph is missing."
category: analysis
complexity: standard
mcp-servers: [codegraph]
personas: [analyzer]
argument-hint: "<symbol>... | --diff [<base>] [--depth 1-3] [--limit N] [--tests] [--test-depth N] [--output-dir <dir>] [--caller <name>]"
---

# /sc:impact

Answers "what depends on this before I change it": for named symbols, or for the symbols a diff touches, it lists their definitions, their production and test dependents (direct callers plus transitive impact), confirms the call sites of the rows it shows, and with `--tests` adds an advisory list of test files. It never stops its caller: when codegraph, the switch, the index or the lookup tools are not usable it falls back to Grep and reports `status: partial`.

Codegraph usage rules: read `~/.claude/CODEGRAPH.md` (in a dev checkout without an install, the labelled fallback is `src/superclaude/core/CODEGRAPH.md`).

## Usage

```bash
/sc:impact parse_config                         # dependents of one symbol
/sc:impact load_spec write_report --depth 3     # several symbols, three hops
/sc:impact --diff                               # symbols changed in the working tree vs HEAD
/sc:impact --diff origin/master --tests         # symbols a branch changed, plus advisory tests
/sc:impact parse_config --caller sc-implement-protocol --output-dir .dev/impact/t3
/sc:impact parse_config --unattended --report-dir .dev/impact/run1   # worker mode: contract written there
```

## Options

| Flag | Default | Description |
|------|---------|-------------|
| `<symbol>...` | none | 1-30 bare names (no `Class.method` or path). Either symbols or `--diff`, never both. |
| `--diff [<base>]` | `HEAD` when given without a value | Map the changed hunks of `git diff` (or `git diff --merge-base <base>`) to the symbols they touch. |
| `--depth` | `2` | Transitive depth for impact, 1-3. |
| `--limit` | `20` | Caller rows per symbol, 1-100. |
| `--tests` | `false` | Add an advisory test list from `codegraph affected` plus a path heuristic. It can add tests to a selection, never remove any. |
| `--test-depth` | codegraph's own | 1-5, only with `--tests`. |
| `--output-dir` | `<worktree>/.dev/impact/<slug>-<timestamp>/` | Where `impact.md` and `return-contract.yaml` are written. Never inside `.git/` or `.codegraph/`. |
| `--caller` | unset | Name of the calling skill; shortens chat output to three lines (status, degraded tokens, contract path). |
| `--unattended` | `false` | Worker mode: no step waits for a person; see Unattended mode. |
| `--report-dir` | unset | With `--unattended`, the directory that holds the worker contract (instead of `--output-dir`, never both). |

## Activation

**MANDATORY**: Before executing any protocol steps, invoke:
> Skill sc:impact-protocol

Pass the user's arguments unchanged. Do NOT proceed with protocol execution using only this command file. The readiness check, lookups, call-site confirmation, outputs and failure handling are in the protocol skill.

## Outputs

- `<output-dir>/impact.md`: the human report (12 fixed sections).
- `<output-dir>/return-contract.yaml`: the capped machine contract (at most 40 dependent rows, 6 KB). Calling skills read only this file.

## Unattended mode

The shared rules are in `~/.claude/WORKER-CONTRACT.md`; read it first. This section lists only what `/sc:impact` resolves itself.

- **Switch.** It applies only when `--unattended` is a standalone argument token outside any quoted argument; otherwise nothing here applies and no worker contract is written.
- **Report directory.** Exactly one of `--output-dir <dir>` or `--report-dir <dir>`, passed explicitly: the default `<worktree>/.dev/impact/...` directory does not satisfy it, and both, or neither, is refused before any work. `--report-dir` follows the path rules of `--output-dir` (never inside `.git/` or `.codegraph/`, never under the distributable skill, agent or command folders of a `.claude/` folder, created if missing and writable); a directory that fails them counts as no report directory known, so the refusal is printed in chat only.
- **Contract.** With `--output-dir` the worker fields (`worker_contract_version`, `worker_status`, `artifacts`, and `reason` when failed) are added to the existing `<output-dir>/return-contract.yaml` beside every existing field. With `--report-dir` alone, `impact.md` and the command's own contract stay in the default directory, and the skill writes `<report-dir>/return-contract.yaml` with the existing fields plus the worker fields, listing `impact.md` and the own contract in `artifacts`. `command` and `report_path` keep their existing values (`report_path` is already `impact.md`). The own status values success, partial and failed map to succeeded, partial and failed, and a flag-STOP `blocked` maps to failed with the STOP in `reason`.
- **Gates.** None: the command never stops its caller and falls back to Grep. Nested invocations: none.
- **Outward actions.** It edits no code, runs no tests, and pushes, commits and stages nothing.

## Boundaries

**Will:**

- Locate definitions and dependents and label every row `def-line`, `call-site-verified` or `unresolved`
- Report `shown/total` counts and say when a list was cut
- Fall back to Grep and keep going whenever codegraph is not usable

**Will Not:**

- Edit code, run tests, or build, sync or remove an index (use `/sc:graph` for index status)
- Conclude that a symbol has no dependents or no tests from an empty graph answer
- Change any caller's severity, gate or verdict while the contract says `advisory: true`
