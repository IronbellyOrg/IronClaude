---
status: partial
caller: sc-reflect-protocol
index_state: fresh
checked_at: 2026-11-06T19:53:11Z
advisory: true
degraded: [graph:stale, graph:unresolved]
contract_path: /home/coder/workspaces/worktrees/IronClaude/fix-tier-limits-model-picker/.dev/tasks/done/TASK-WF-remediationSourc-20261106-121243/artifacts/reflect-post-quick/artifacts/impact/return-contract.yaml
---

## Summary
Counts-only supporting inspection, not a product-impact clearance. The captured diff inventory has 303 files: 300 task-package files and 3 product/test files. Lexical first-30-file selection is entirely task artifacts; the three product/test paths fall outside the cap. Two Python artifacts yielded four mapped callable definitions and 14 unverified direct graph rows. These counts cannot change a shipping gate.

| symbol | definition | prod (shown/total) | test (shown/total) | transitive | truncated |
|---|---|---|---|---|---|
| append | protocol_io.py, definition only | 0/7 | 0/1 | 0 additional | false |
| capture | capture_shim.py, definition only | 0/1 | 0/0 | 0 additional | false |
| git | protocol_io.py, definition only | 0/3 | 0/0 | 0 additional | false |
| snapshot | protocol_io.py, definition only | 0/2 | 0/0 | 0 additional | false |

Totals are raw graph leads, not validated call edges. In particular, common names such as append can collect unrelated attribute calls. Classification uses path markers only; Python task artifacts without test-path markers fall in the production-path bucket, not necessarily shipped production code.

## How to read this
Rows locate code and are not citations until marked `call-site-verified`.
An empty list never proves there are no dependents.
While `advisory: true`, nothing here may change a severity, gate or verdict.

## Readiness
| field | value |
|---|---|
| access | mcp |
| index_state | fresh at initial and final readiness checks |
| checked_at | 2026-11-06T19:53:11Z, final status response timestamp |
| cli_version / pin / pin_match | 1.6.2 / 1.6.2 / true |
| worktree_root / project_path | /home/coder/workspaces/worktrees/IronClaude/fix-tier-limits-model-picker |
| worktree_relation | own |
| primitive switch | unset, not disabled |
| lookup tools | search, node, callers, impact listed |
| concurrent changes | one unrelated reflection-card file was pending during lookup responses; final status reports zero pending |
| advisory | true by caller restriction; guide E-1 outcome-A itself does not require advisory mode |

Readiness was rechecked after the initial report stub was written. No index mutation was requested or run.

## Input
Base HEAD resolves to 54aba77250794b856a0c78fac026425243e157f9; depth 1; limit 100; tests false. The name-only inventory includes staged and unstaged tracked changes, not untracked files. Captured inventory source: /home/coder/.claude/projects/-home-coder-workspaces-worktrees-IronClaude-fix-tier-limits-model-picker/16861c3f-27cb-4f03-9935-b5096afad12c/tool-results/b153ze42i.txt.

The first 30 names end at the runtime-work-2/alias-haiku/lsof artifact. Only the two Python candidates within those 30 were given outline and hunk queries; remaining artifacts were not read. Hunk collection was deliberately restricted to those two candidates, rather than reading all 300 artifact contents. Callable definitions only were resolved; variable declarations were not exhaustively mapped.

The compact contract retains five relevant paths and explicit inventory omission counts instead of the full 303-path list, to meet the 6 KB output ceiling. Its changed_files and unmapped_files arrays are samples, not exhaustive inventories. This counts-only adaptation is an explicit coverage limitation.

| name | file | start | end | mapped_by |
|---|---|---|---|---|
| append | .dev/tasks/done/TASK-WF-remediationSourc-20261106-121243/artifacts/protocol_io.py | 31 | 33 | hunk |
| capture | .dev/tasks/done/TASK-WF-remediationSourc-20261106-121243/artifacts/capture_shim.py | 16 | 21 | hunk |
| git | .dev/tasks/done/TASK-WF-remediationSourc-20261106-121243/artifacts/protocol_io.py | 17 | 18 | hunk |
| snapshot | .dev/tasks/done/TASK-WF-remediationSourc-20261106-121243/artifacts/protocol_io.py | 20 | 29 | hunk |

## Definitions
| name | file:start-end | kind | mapped_by |
|---|---|---|---|
| append | protocol_io.py:31-33 | function | hunk |
| capture | capture_shim.py:16-21 | function | hunk |
| git | protocol_io.py:17-18 | function | hunk |
| snapshot | protocol_io.py:20-29 | function | hunk |
These are graph definition spans, not verified call-site citations. Exact changed-file filtering disambiguated common-name results.

## Production dependents
Counts only: 13 raw path-classified leads. Zero rows shown or cited; all remain unverified. Callback-registration edges and file/variable nodes occur in the raw answers.

## Test dependents
Counts only: 1 raw path-classified lead. Zero rows shown or cited; it remains unverified.

## Unmapped files
301 inventory files lack a mapped callable in this bounded inspection: 273 paths beyond the first-30 cap, plus 28 non-Python artifact paths within the selected window that were not content-inspected. This does not assert those 28 files are absent from the index.

| file | reason |
|---|---|
| src/superclaude/skills/ccsession-tag/ccsession | cap |
| src/superclaude/skills/ccsession-tag/models.py | cap |
| tests/unit/test_ccsession_tiers.py | cap |
Other unmapped paths are represented by counts rather than repeated here. Variables in the two mapped files were not exhaustively inspected.

## Limits
303 paths inventoried; 30 path slots considered; 2 Python file outlines queried; 4 callable candidates queried, below the 30-symbol ceiling. No other artifact contents were swept. Callers were queried with limit 100; none of the four direct lists reported truncation. Raw totals: 14 direct rows, 13 production-path, 1 test-path, 0 unknown-path. Impact self rows were removed; all remaining depth-1 rows duplicated direct answers, leaving 0 additional transitive rows. Empty additional rows are not evidence of absence.

Call-site budget: verified 0, unresolved 14, dropped 0; maximum 5/symbol and 20/run. Counts-only mode shows no dependent rows, so no row is offered as a verified citation. Grep native floor was attempted and failed with EACCES; Read floor inspected bounded source ranges in both mapped files. No tests, review fanout, Git writes, product edits, or index mutations occurred.

## Degraded and fallbacks
- graph:stale: pending concurrent changes were reported during lookups; later readiness returned fresh. Counts remain advisory.
- graph:unresolved: all 14 graph rows are counted only, never cited as call sites.
- Unmapped files and bounded non-callable coverage independently require partial status.
- Native Grep error: EACCES: permission denied, posix_spawn 'rg'. No shell bypass was attempted; bounded Read supplied the native inspection floor.
