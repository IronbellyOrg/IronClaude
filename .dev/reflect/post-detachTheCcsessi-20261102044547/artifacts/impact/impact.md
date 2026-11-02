---
status: partial
caller: sc-reflect-protocol
index_state: fresh
checked_at: 2026-11-02T04:46:54Z
advisory: false
degraded: []
contract_path: /home/coder/workspaces/IronClaude/.dev/worktrees/ccsession-proxy-stall/.dev/reflect/post-detachTheCcsessi-20261102044547/artifacts/impact/return-contract.yaml
---

## Summary

Diff mode against HEAD (f90877be1db0fc68c40205a763bd6b7d874aa0db), uncommitted changes in 4 files. No changed hunk overlaps an indexed symbol span, so no symbol was derived and no dependent was looked up. All 4 files are unmapped (see below).

| symbol | definition | prod (shown/total) | test (shown/total) | transitive | truncated |
|---|---|---|---|---|---|
| (none derived) | - | - | - | - | - |

## How to read this

Rows locate code and are not citations until marked `call-site-verified`. An empty list never proves there are no dependents. While `advisory: true`, nothing here may change a severity, gate or verdict.

## Readiness

| field | value |
|---|---|
| access | mcp |
| index_state | fresh |
| checked_at | 2026-11-02T04:46:54Z |
| cli_version | 1.6.2 |
| pin | 1.6.2 |
| pin_match | true |
| worktree_root | /home/coder/workspaces/IronClaude/.dev/worktrees/ccsession-proxy-stall |
| project_path | /home/coder/workspaces/IronClaude/.dev/worktrees/ccsession-proxy-stall |
| worktree_relation | own |

## Input

changed_files: CHANGELOG.md, src/superclaude/skills/ccsession-tag/ccsession, src/superclaude/skills/ccsession-tag/local-gateway-alias-proxy.py, tests/unit/test_ccsession_tiers.py

| name | file | start | end | mapped_by |
|---|---|---|---|---|
| (none) | | | | |

## Definitions

None derived.

## Production dependents

None looked up (no changed symbol).

## Test dependents

None looked up (no changed symbol).

## Unmapped files

| file | reason |
|---|---|
| CHANGELOG.md | not_indexed |
| src/superclaude/skills/ccsession-tag/ccsession | not_indexed |
| src/superclaude/skills/ccsession-tag/local-gateway-alias-proxy.py | no_span_match |
| tests/unit/test_ccsession_tiers.py | not_indexed |

The proxy hunk (new lines 859-867) sits in the module-level `if __name__ == "__main__":` block; the file outline (`codegraph_node` symbolsOnly) has no symbol whose span covers those lines (nearest: `ThreadingServer` :852, `srv` :869). The bash launcher and the tests file are not in the index (`codegraph_node` reports "No indexed file matches" for the tests file).

## Limits

No lists, so no truncation; call-site budget unused (verified 0 / unresolved 0 / dropped 0).

## Degraded and fallbacks

No `graph:*` token. Unmapped files lower the status to partial; no Grep fallback rows were invented.
