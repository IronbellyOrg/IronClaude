---
status: success
caller: null
index_state: fresh
checked_at: '2026-10-31T15:35:16Z'
advisory: false
degraded: []
contract_path: /home/coder/workspaces/IronClaude/.dev/worktrees/codegraph-adoption/.dev/codegraph-migration/experiments/P3-T11-impact/return-contract.yaml
---

## Summary
The index found two direct production callers of `install_core_files`. Both call sites were verified against the current source. No additional transitive rows or test rows were returned; empty index results do not prove absence.

| symbol | definition | prod (shown/total) | test (shown/total) | transitive | truncated |
|---|---|---|---|---|---|
| install_core_files | src/superclaude/cli/install_core.py:28-101 | 2/2 | 0/0 | 0 | false |

## How to read this
Rows locate code and are not citations until marked `call-site-verified`.
An empty list never proves there are no dependents.
While `advisory: true`, nothing here may change a severity, gate or verdict.

## Readiness
| field | value |
|---|---|
| access | mcp |
| index_state | fresh |
| checked_at | 2026-10-31T15:35:16Z |
| cli_version | 1.6.2 |
| pin | 1.6.2 |
| pin_match | true |
| worktree_root | /home/coder/workspaces/IronClaude/.dev/worktrees/codegraph-adoption |
| project_path | /home/coder/workspaces/IronClaude/.dev/worktrees/codegraph-adoption |
| worktree_relation | own |

The primitives switch was unset. MCP status reported 0 added, 0 modified and 0 removed files. Lookup tools were listed.

## Input
Mode: symbols. Requested symbol: `install_core_files`. Depth: 2. Caller limit: 20. Tests: not requested. Caller: unset.

Output directory: `/home/coder/workspaces/IronClaude/.dev/worktrees/codegraph-adoption/.dev/codegraph-migration/experiments/P3-T11-impact`.

## Definitions
| name | file:start-end | kind | mapped_by |
|---|---|---|---|
| install_core_files | src/superclaude/cli/install_core.py:28-101 | function | name |

Only exact-name matches were retained. The search also returned `install_hooks`, which was excluded because its name differs.

## Production dependents
### install_core_files

| caller | file | def_line | call_site_line | resolution | hop | source |
|---|---|---|---|---|---|---|
| install | src/superclaude/cli/main.py | 46 | 178 | call-site-verified | 1 | callers |
| update | src/superclaude/cli/main.py | 340 | 365 | call-site-verified | 1 | callers |

Caller spans from CLI queries were `install`: 46-280 and `update`: 340-429 in the same file. Grep located the calls inside those spans. Read confirmed executable calls at lines 178 and 365, not comments, strings, docstrings or attribute-only references.

## Test dependents
### install_core_files

| caller | file | def_line | call_site_line | resolution | hop | source |
|---|---|---|---|---|---|---|

Shown/total: 0/0 indexed test dependents. This is not evidence that no tests exist. Test selection was not requested and no tests were run.

## Limits
- Production shown/total: 2/2. Test shown/total: 0/0. Unknown shown/total: 0/0.
- Direct callers: 2/2; no re-query needed and no dependent list was truncated.
- Depth 2 impact returned the queried definition and the same two direct callers. The definition was excluded and duplicate callers were not added: additional transitive count 0.
- Call-site budget: 5/symbol, 20/run. Verified/unresolved/dropped: 2/0/0.
- Contract dependent rows: 2; omitted: 0. Cap: 40 rows and 6 KB.
- Partition uses path markers only; inline test markers are not checked, so lists are floors.
- Caller-span search results were capped at 20; both exact caller/file/start-line matches were present, so their confirmation was unaffected.
- No code was edited, no tests were run and no index was built, synced or removed.
- Independent review verdict: **PASS**.
- Resolved finding (initial verdict FAIL): section 5 requires `errors[]` to contain the verbatim first line of each failed call; the original contract appended `; read the labelled in-checkout fallback.` instead. Independently re-read the corrected contract: that commentary is removed and the entry now contains the actual failed Read first line supplied by the coordinator. This resolves the sole finding.
- Correction self-audit: re-read the full contract, confirmed the other fields and two dependent rows remain unchanged, and remeasured 2051 bytes (limit 6000). The original source/count/layout checks below still apply; 2016 bytes was the pre-correction measurement. No further investigation, tests or index mutations were performed.
- Self-audit: read both artifacts and governing sections 5–6; checked required fields, types, allowed values, section order, warning sentences and absence of unfilled placeholders. Measured the contract at 2016 bytes (limit 6000); counted 2 dependent rows (limit 40), both production, with 0 omitted. Matched report/contract counts (production 2/2, test 0/0, unknown 0/0, transitive 0; call sites 2/0/0), definition span 28–101, caller definitions 46 and 340, imports, and executable calls at main.py:178 and :365 against current source. Neither dependent is the target definition; excluding that target and deduplicating the two direct callers leaves 0 additional transitive rows. No other layout/count/source findings. Historical readiness and graph completeness were not independently re-established; no tests or index-mutating commands were run. Only this existing Limits section was changed.

## Degraded and fallbacks
Degraded tokens: `[]`. No lookup fallback was needed.

Guide read failure: `File does not exist: /home/coder/.claude/CODEGRAPH.md`. The labelled in-checkout fallback `src/superclaude/core/CODEGRAPH.md` was read successfully. Its pin is 1.6.2 and its freshness experiment reads `outcome-A`; advisory is false.

The requested directory already contained an unpopulated report stub and a failed contract from an earlier run. This run populated the existing skeleton and replaced the contract with current observations.
