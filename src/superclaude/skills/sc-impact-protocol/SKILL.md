---
name: sc:impact-protocol
description: "Codegraph-backed dependents report: definitions, production and test dependents with shown/total and call-site resolution, optional advisory test list from codegraph affected; writes impact.md and return-contract.yaml; never stops its caller."
allowed-tools: Read, Grep, Glob, Write, Edit, Bash(printenv SUPERCLAUDE_CODEGRAPH_PRIMITIVES), Bash(pgrep -f *), Bash(git rev-parse *), Bash(realpath *), Bash(git diff *), Bash(codegraph --version), Bash(codegraph status), Bash(codegraph query *), Bash(codegraph node *), Bash(codegraph callers *), Bash(codegraph impact *), Bash(codegraph affected *), mcp__codegraph__codegraph_status, mcp__codegraph__codegraph_search, mcp__codegraph__codegraph_node, mcp__codegraph__codegraph_callers, mcp__codegraph__codegraph_impact
---

<!-- Extended metadata (for documentation, not parsed):
category: analysis
complexity: standard
mcp-servers: [codegraph]
-->

# sc:impact-protocol

Backs `/sc:impact` (`~/.claude/commands/sc/impact.md`, or the project `.claude/commands/sc/impact.md`). Callers invoke it directly with `> Skill sc:impact-protocol` and the arguments their own skill names, then read only `<output-dir>/return-contract.yaml`. It never stops a caller: every failure ends in `status: partial`, `blocked` or `failed` with the reason recorded, and callers treat `blocked` and `failed` like `graph:absent`.

Codegraph usage rules: read `~/.claude/CODEGRAPH.md` (in a dev checkout without an install, the labelled fallback is `src/superclaude/core/CODEGRAPH.md`). Read it once per run; the readiness check, the closed token list, the pin line, the E-1 line and the call-site procedure come from it.

## 1. Flags (step 1 validates them)

| Flag | Default | Validation | STOP → `status: blocked` (contract still written when `--output-dir` resolves) |
|---|---|---|---|
| `<symbol>...` | none | 1-30 items, each `^[A-Za-z_$][A-Za-z0-9_$]*$` | none and no `--diff`; both symbols and `--diff`; more than 30; a dotted or path-qualified name ("pass the bare name; codegraph has no `Class/method` addressing") |
| `--diff [<base>]` | `HEAD` when given without a value | `git rev-parse --verify --quiet <base>^{commit}` succeeds | the ref does not resolve |
| `--depth` | `2` | integer 1-3 | outside 1-3 |
| `--limit` | `20` | integer 1-100 | outside 1-100 |
| `--tests` | `false` | — | — |
| `--test-depth` | unset | integer 1-5, only with `--tests` | without `--tests`; outside 1-5 |
| `--output-dir` | `<worktree_root>/.dev/impact/<slug>-<YYYYMMDDTHHMMSSZ>/`; `<slug>` = first symbol or `diff-<base>`, lowercased, non-alphanumerics → `-`, max 40 chars | absolute after resolution; not inside `.git/` or `.codegraph/`; created if missing; existing outputs are overwritten | inside `.git`/`.codegraph` → blocked; not creatable or writable → `status: failed`, reason printed |
| `--caller` | unset | `^[a-z0-9][a-z0-9:-]{0,63}$` | malformed |

With `--caller` set, chat output is three lines: status, `degraded`, contract path. Without it, print the `## Summary` table of `impact.md`.

## 2. Step sequence

| # | Step | Exact calls | Output / fallback |
|---|---|---|---|
| 1 | Validate flags | none | section 1 STOPs |
| 2 | Readiness | the guide's readiness check, once: `printenv SUPERCLAUDE_CODEGRAPH_PRIMITIVES`; `git rev-parse --show-toplevel` then `realpath`; `codegraph --version` against the guide pin; `mcp__codegraph__codegraph_status {"projectPath": "<worktree_root>"}` when listed, else CLI `codegraph status` only when `pgrep -f 'codegraph\.js (init|index)'` prints nothing (a printed line → `index_state: stale`, `graph:stale`, no `status` call); whether `mcp__codegraph__codegraph_callers` is listed | the `readiness` fields; tokens. Lookups are allowed for `fresh`, `stale`, or a version token on an otherwise fresh index. Transport: lookup tools listed → MCP; only `codegraph_status` listed (`graph:unlisted`) and `codegraph --version` equals the pin → CLI transport (`access: cli`); otherwise step 9 |
| 3 | Inputs, symbol mode | per symbol: `mcp__codegraph__codegraph_search {"query": "<sym>", "limit": 10, "projectPath": "<project_path>"}`; keep rows whose name equals `<sym>` exactly | 0 matches → Grep `^\s*(def|class|function|func|fn)\s+<sym>([^A-Za-z0-9_$]|$)|(^|[^A-Za-z0-9_$])<sym>\s*=\s*(function|\()` → `mapped_by: grep`, token `graph:empty` (never "does not exist"). More than one → `ambiguous[]` lists all; keep at most 3 definitions (by file, then line), token `graph:ambiguous` |
| 3' | Inputs, diff mode | D1 `git diff --name-only HEAD` when `--diff` has no base, else `git diff --name-only --merge-base <base>`; D2 `git diff -U0 HEAD` when there is no base, else `git diff -U0 --merge-base <base>` (both compare against a commit, so staged and unstaged edits count), new-side ranges of `@@ -a,b +c,d @@`; D3 per changed file (max 30 files): `mcp__codegraph__codegraph_node {"file": "<repo-relative path>", "symbolsOnly": true, "projectPath": "<project_path>"}` → candidate names; D4 per candidate (max 30 per run): `codegraph query <name> --json --limit 20` in `worktree_root`; keep entries whose `filePath` equals the changed file and whose `startLine..endLine` overlaps a hunk | each hit → `changed_symbols[]` with `start`, `end`, `mapped_by: hunk`. Files with no hit, deleted files, files over the cap and non-indexed files (Markdown) → `unmapped_files[]` with `reason: no_span_match|deleted|cap|not_indexed|query_refused|no_graph` |
| 4 | Direct callers | per definition: `mcp__codegraph__codegraph_callers {"symbol": "<sym>", "file": "<def file>", "limit": <--limit>, "projectPath": "<project_path>"}` | parse `Callers of <sym> (<n> found)` and `Showing <shown> of <total> callers`. If `total > shown` and `total <= 100`: re-query once with `"limit": <total>`. Still short or `total > 100`: `truncated: true`, token `graph:truncated`. No rows → `graph:empty` |
| 5 | Transitive dependents | per definition: `mcp__codegraph__codegraph_impact {"symbol": "<sym>", "file": "<def file>", "depth": <--depth>, "projectPath": "<project_path>"}` | first drop the row that is the queried definition itself (same name, file and start line; codegraph lists it first); it is never a dependent and never counted in `transitive.count`. The other rows not already found in step 4 are added with `source: impact`; the MCP text gives no per-row depth, so they get `hop: 2` (meaning "two or more") unless the CLI JSON form below gives the edge path. Unparsable → `graph:parse_failed`, step-4 rows kept |
| 5' | Status-only branch transport (CLI, before any Grep fallback) | when step 2 chose the CLI transport, steps 3-5 use the CLI forms captured in Phase 3 experiment E-2, run in `worktree_root`: `codegraph query <sym> --json --limit 10`; `codegraph node --file <path> --symbols-only` (no `--json` on `node`); `codegraph callers <sym> --file <def file> --json --limit <--limit>`; `codegraph impact <sym> --file <def file> --depth <--depth> --json` | JSON `callers[]` and `affected[]` rows (the first `affected[]` row is the queried definition itself and is dropped, as in step 5); `edges[].line` is a call-site candidate for step 7, still confirmed by CS2-CS4. A refused or failed CLI call → step 9 for that symbol and the error line in `errors[]` |
| 6 | Partition | Read `~/.claude/skills/sc-reflect-protocol/refs/runtime-surface.md` (else `.claude/skills/sc-reflect-protocol/refs/runtime-surface.md`) section 2 language table, once per run | each row `partition: prod|test|unknown` by path markers; inline test markers are not checked, so lists are floors; unknown language → `unknown` |
| 7 | Call-site confirmation | the guide's call-site procedure CS1-CS5 (section 4 below) for the rows shown in `impact.md` tables: first 5 `prod` rows with `hop: 1` per symbol (sort order of step 10), at most 20 per run. A `hop` 2 row (step 5) is never confirmed: its body need not call the queried symbol, so it keeps `resolution: def-line`, is cited only as a definition and is never dropped by CS5 | `resolution: call-site-verified` with `call_site_line`; rows over the budget stay `def-line` (graph) or `unresolved` (grep) and are only counted (token `graph:unresolved`); failing rows are dropped from the tables and counted in `call_sites.dropped` |
| 8 | Tests (only `--tests`) | changed files = definition files (symbol mode) or D1 files that exist (diff mode); `codegraph affected <file>... --json --quiet` (+ `--depth <--test-depth>`), files as arguments, never a pipeline | `tests[]` with `source: affected`. Heuristic: for each changed `<stem>.<ext>`, Glob `**/test_<stem>.*`, `**/<stem>_test.*`, `**/<stem>.test.*`, `**/<stem>.spec.*`, plus every `test` partition file of steps 4-5 → `source: heuristic`; both → `both`. `selection_source: advisory` when `affected` contributed, else `heuristic_only`. Unparsable JSON → `graph:parse_failed`, heuristic only. Skipped when `index_state` is not `fresh` or `stale` |
| 9 | Grep fallback (lookups not allowed in step 2, or the CLI transport failed) | symbol mode: Grep `(^|[^A-Za-z0-9_$])<sym>\s*\(` over the worktree, excluding `.git/`, `.codegraph/`, `.dev/`; cap 100 hits per symbol. Diff mode: D1 and D2 still run (git only); D3-D4 need codegraph and do not run, so no symbol is derived | symbol mode: rows `source: grep`, `resolution: unresolved`, `caller: null`, partition by step 6; definitions from the step-3 Grep. Diff mode: every D1 file goes to `unmapped_files[]` with `reason: no_graph`, no dependent row is invented, and step 8's heuristic still uses the D1 files. `status: partial` |
| 10 | Write outputs | Write `<output-dir>/impact.md` (section 6), then `<output-dir>/return-contract.yaml` (section 5) | rows sorted by `symbol`, `partition` (prod first), `file`, `def_line`; the contract holds at most 40 dependent rows and 6 KB, the rest only in `impact.md` |

Sort before the step-7 selection, so the confirmed rows are deterministic. Same inputs and the same index give byte-identical files.

## 3. Advisory rule

`advisory` is `true` while the guide's line reads `Freshness experiment E-1: pending`, and under `outcome-B` for every run with `access: cli`; it is `false` otherwise (the guide currently reads `outcome-A`). While `advisory` is `true`, no consumer may change a severity, gate or verdict from this contract. In every state, no "no dependents" or "no tests" conclusion is drawn from an empty list: an empty graph answer never proves absence.

## 4. Call-site confirmation (guide section 5; budget 5 per symbol, 20 per run)

Only `hop: 1` rows (direct callers) enter CS1-CS5; `hop` 2 rows keep `def-line` (step 7). In every Grep pattern of this skill, a name (`<sym>`, `<callee>`) is written regex-escaped (`$` as `\$`) between the boundaries `(^|[^A-Za-z0-9_$])` and `([^A-Za-z0-9_$]|$)` or `\s*\(`, never `\b`: `\b` cannot sit beside a `$`, so `\b$foo` never matches.

- **CS1** `codegraph query <caller> --json --limit 20`; keep the entry whose `filePath` equals the row's file and whose `startLine` equals the row's `def_line`. None → `unresolved`.
- **CS2** Grep `(^|[^A-Za-z0-9_$])<callee>\s*\(` with line numbers in that file; keep matches inside `startLine..endLine`.
- **CS3** Reject matches in comments, string literals or docstrings, bare-name assignments and attribute-only matches. Several matches → cite each as a candidate, or none.
- **CS4** Read the matched line. It must still contain the call → `call-site-verified`, `call_site_line` set.
- **CS5** Any failure → drop the row from cited output; never repair it. `def-line` rows are cited only as definitions.

Every row carries `resolution: def-line|call-site-verified|unresolved`. Rows are leads, not citations, until CS4.

## 5. `return-contract.yaml`

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
| `readiness` | map | `access`, `index_state`, `checked_at`, `cli_version`, `pin`, `pin_match`, `worktree_root`, `project_path`, `worktree_relation` |
| `advisory` | bool | section 3 |
| `degraded` | list[string] | `graph:*` tokens from the guide's closed list, sorted, unique |
| `symbols[]` | list[map] | per definition: `name`, `file`, `start_line` (int or null), `end_line` (int or null), `mapped_by` (`name` \| `hunk` \| `grep`), `prod` `{shown, total}`, `test` `{shown, total}`, `unknown` `{shown, total}`, `transitive` `{count, depth}`, `truncated` (bool) |
| `ambiguous[]` | list[map] | `{name, definitions: [{file, line}]}` |
| `unmapped_files[]` | list[map] | `{file, reason}` |
| `dependents[]` | list[map], max 40 | `symbol`, `caller` (string or null), `file`, `def_line` (int or null), `call_site_line` (int or null), `resolution` (`def-line` \| `call-site-verified` \| `unresolved`), `partition` (`prod` \| `test` \| `unknown`), `hop` (1-3), `source` (`callers` \| `impact` \| `grep`) |
| `dependents_omitted` | int | rows only in `impact.md` |
| `call_sites` | map | `{verified, unresolved, dropped, budget: "5/symbol, 20/run"}` |
| `tests[]` | list[map] or `[]` | with `--tests`: `{path, source: heuristic \| affected \| both}`, sorted by path |
| `selection_source` | enum or null | `advisory` \| `heuristic_only`; `null` without `--tests` |
| `errors[]` | list[string] | one line per failed call, verbatim first line |

Status merge, `failed > blocked > partial > success`:

- `blocked`: a flag STOP.
- `failed`: outputs could not be written, or every lookup and every Grep fallback errored.
- `partial`: any token in `degraded` other than `graph:unresolved` (budget-limited rows are normal), or any `unmapped_files`, or any fallback row.
- `success`: otherwise. `advisory: true` does not by itself lower the status.

Example (placeholder symbol and paths; the shape, not real data):

```yaml
schema_version: 1
command: impact
status: success
caller: sc-implement-protocol
output_dir: /path/to/worktree/.dev/impact/example
report_path: /path/to/worktree/.dev/impact/example/impact.md
contract_path: /path/to/worktree/.dev/impact/example/return-contract.yaml
input: {mode: symbols, symbols: [example_symbol], diff_base: null, changed_files: [], depth: 1, limit: 10, tests: false, test_depth: null}
readiness:
  access: mcp
  index_state: fresh
  checked_at: 2026-10-31T09:20:03Z
  cli_version: 1.6.2
  pin: 1.6.2
  pin_match: true
  worktree_root: /path/to/worktree
  project_path: /path/to/worktree
  worktree_relation: own
advisory: false
degraded: [graph:unresolved]
symbols:
  - {name: example_symbol, file: pkg/module.py, start_line: 10, end_line: 42, mapped_by: name, prod: {shown: 2, total: 2}, test: {shown: 6, total: 6}, unknown: {shown: 0, total: 0}, transitive: {count: 1, depth: 1}, truncated: false}
ambiguous: []
unmapped_files: []
dependents:
  - {symbol: example_symbol, caller: run_example, file: pkg/cli.py, def_line: 20, call_site_line: 31, resolution: call-site-verified, partition: prod, hop: 1, source: callers}
  - {symbol: example_symbol, caller: test_example, file: tests/test_module.py, def_line: 5, call_site_line: null, resolution: def-line, partition: test, hop: 1, source: callers}
dependents_omitted: 0
call_sites: {verified: 2, unresolved: 6, dropped: 0, budget: "5/symbol, 20/run"}
tests: []
selection_source: null
errors: []
```

## 6. `impact.md` layout

YAML front matter: `status`, `caller`, `index_state`, `checked_at`, `advisory`, `degraded`, `contract_path`. Then, in this order:

1. `## Summary`: one paragraph, then a table `symbol | definition | prod (shown/total) | test (shown/total) | transitive | truncated`.
2. `## How to read this`: three fixed sentences: rows locate code and are not citations until marked `call-site-verified`; an empty list never proves there are no dependents; while `advisory: true`, nothing here may change a severity, gate or verdict.
3. `## Readiness`: the readiness fields as a two-column table.
4. `## Input`: symbol mode lists the symbols; diff mode lists `changed_files` and the `changed_symbols` table `name | file | start | end | mapped_by`.
5. `## Definitions`: `name | file:start-end | kind | mapped_by`; `### Ambiguous` when any.
6. `## Production dependents`: per symbol, `caller | file | def_line | call_site_line | resolution | hop | source`.
7. `## Test dependents`: same columns.
8. `## Unclassified dependents`: `partition: unknown` rows; omitted when empty.
9. `## Tests (advisory)`: only with `--tests`: `path | source`, then `selection_source` and the sentence "Adds tests to a selection; never removes any."
10. `## Unmapped files`: `file | reason`; omitted when empty.
11. `## Limits`: `shown/total` per list, truncation, call-site budget use (`verified/unresolved/dropped`).
12. `## Degraded and fallbacks`: each token with its one-line meaning from the guide and the fallback used.

## 7. Failure behaviour

The run continues, outputs are written, and the caller is never stopped.

| Condition | Detected by | Status | Token(s) | Behaviour | `/sc:graph status` status / `next_action` |
|---|---|---|---|---|---|
| codegraph absent | `codegraph --version` not found and no MCP status tool | partial | `graph:absent` | step 9 Grep rows; `--tests` heuristic only | partial / `install_codegraph` |
| lookup tools unlisted (status-only branch) | step 2: callers tool not listed | partial | `graph:unlisted` | step 5' CLI transport, else step 9 | partial / `status_only_branch` |
| switched off | `SUPERCLAUDE_CODEGRAPH_PRIMITIVES=off` | partial | `graph:disabled` | step 9 | partial / `enable_codegraph` |
| not initialized | readiness: not initialized | partial | `graph:not_initialized` | step 9; the report names `/sc:graph init` | partial / `run_graph_init` |
| foreign index (nested or snapshot worktree) | readiness: different git working tree | partial | `graph:foreign_index` | handled as not initialized | partial / `run_graph_init_worktree_local` |
| stale | readiness: pending changes, or an init running | partial | `graph:stale` | graph rows kept as leads; counts never feed a gate | partial / `wait_for_sync` |
| version mismatch / unknown | `codegraph --version` vs the pin | partial | `graph:version_mismatch` + `graph:provenance_unproven` / `graph:provenance_unproven` | rows kept as leads; no CS1-CS5 citations; counts not used by callers; no CLI transport | partial / `align_version` |
| truncated | step 4 after one re-query | partial | `graph:truncated` | `total` reported as a floor | n/a |
| parse failure | readiness text unknown, step 4/5/8 unparsable | partial | `graph:parse_failed` | the affected step falls back to Grep (readiness) or keeps earlier rows (steps 5, 8) | partial / `check_codegraph_error` |
| ambiguous name | step 3 | partial | `graph:ambiguous` | up to 3 definitions | n/a |
| empty result | steps 3-4 | partial | `graph:empty` | "no dependents found in the index", never "none exist" | n/a |
| budget-limited rows | step 7 | unchanged | `graph:unresolved` | counted, not cited | n/a |
| bad flags | step 1 | blocked | none | no lookups | blocked |
| output dir unwritable | step 10 | failed | none | reason printed | failed |

## Will Not

- Edit code, run tests, or build, sync or remove an index (Write and Edit touch only `impact.md` and `return-contract.yaml` under `--output-dir`)
- Use a file-mode `codegraph_node` call without `"symbolsOnly": true`
- Run CLI `codegraph status` while `pgrep -f 'codegraph\.js (init|index)'` prints a line
- Prefix a CLI call with environment variables
