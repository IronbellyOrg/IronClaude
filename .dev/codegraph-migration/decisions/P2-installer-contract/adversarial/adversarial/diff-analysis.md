# Diff Analysis: installer-contract decision comparison

## Metadata
- Generated: 2026-10-29
- Variants compared: 3 (V1 = option-a, V2 = option-b, V3 = option-c); shared baseline `context.md` applies to all
- Total differences found: 22
- Categories: structural (2), content (9), contradictions (4), unique (4), shared assumptions (4 surfaced, 3 promoted)
- Orchestrator verification (read this session): `update.sh:2-10`; `main.py:254-275` (required phase, aggregated exit); `main.py:161-186` (`--list` block); `main.py:508-512` doctor exit 1; `doctor.py:16-49` (5 checks); `Makefile:42` greps "SuperClaude is healthy"; `install_mcp.py:858-864` refuses to replace a user entry that has `env`/`headers` and returns failure; `install_core.py:62-71` copies core files with `--force` (so `~/.claude/CLAUDE.md` is overwritten before doctor runs in `update.sh`); `phase-3-codegraph-adoption-spec.md:17,22` asks Phase 2 to add `CODEGRAPH_MCP_TOOLS` to the entry `env`; orchestration README line 13: "make `superclaude install` install it by default and `./update.sh` install it on existing workspaces".

## Structural Differences

| # | Area | V1 (A) | V2 (B) | V3 (C) | Severity |
|---|---|---|---|---|---|
| S-001 | Contract sections | Phase, doctor, removal, receipt | Phase, doctor, removal, receipt ("no") | Phase, doctor, removal (+receipt inline), old version dirs | Low |
| S-002 | Lifecycle surface location | Install + `superclaude mcp --uninstall` CLI | Install + docs | Install + `install --list` ownership view + docs | Medium |

## Content Differences

| # | Topic | V1 (A) | V2 (B) | V3 (C) | Severity |
|---|---|---|---|---|---|
| C-001 | Phase failure and exit code | Required; exit 1 after all phases | Non-fatal; stderr recovery command; exit 0 | Required; exit 1 after all phases, stage named | High |
| C-002 | Doctor strictness | Hard fail on missing/drifted binary, absent/different entry, upstream leftovers | Always `passed: True`, details only | Fail only when entry exists and `command` is not executable; rest is details | High |
| C-003 | Removal path | Re-scoped `superclaude mcp --uninstall --servers codegraph [--yes] [--dry-run]` | Documented `claude mcp remove` + `rm -rf` fixed paths + `codegraph uninit` | Documented `claude mcp remove` + delete receipt-listed paths; `--list` shows owned vs external | High |
| C-004 | Ownership receipt | Yes (tag, sha256, paths) | No | Yes (tag, tarball sha256, link targets) | Medium |
| C-005 | Old version dir on pin bump | Not specified | Not specified | Delete receipt-listed older dirs not used by a running daemon (`~/.codegraph/daemons/`), else defer | Medium |
| C-006 | Coder ordering dependency | Bake must precede pin bump; doctor is a 2nd failure point | Forgiving; Coder must assert registration itself | Bake must precede pin bump | High |
| C-007 | Code size | ~370 lines, ~35 tests | ~250 lines, ~22 tests | ~290 lines, ~28 tests | Medium |
| C-008 | Upstream leftovers (`CODEGRAPH_START`, prompt hook) | Doctor fails | Doctor reports | Doctor reports | Medium |
| C-009 | Proof for Coder CI (`--network=none`, `expect_rc 0`) | Exit code proves it | Exit code proves nothing; Coder adds its own assertion | Exit code proves it | High |

## Contradictions

| # | Point of Conflict | V1 (A) | V2 (B) | V3 (C) | Impact |
|---|---|---|---|---|---|
| X-001 | Can "installed by default" be met without failing install? | No: failure must exit 1 | Yes: default attempt + warning suffices | No (C §Contract: "This is what makes 'installed by default' true") | High |
| X-002 | Does doctor need to re-enforce presence? | Yes, hard | No | No, because install enforces it and `update.sh` (`set -e`) only reaches doctor after install exits 0 | Medium |
| X-003 | Is a removal CLI justified after Phase 1 deletes `--uninstall`? | Yes, keep it | No | No | Medium |
| X-004 | Are manual `rm -rf` paths safe without a receipt? | No (receipt gates deletion) | Yes, "only thing at those paths unless the user ran upstream install.sh" | No (receipt lists paths) | Medium |

## Unique Contributions

| # | Variant | Contribution | Value |
|---|---|---|---|
| U-001 | V3 | Doctor fails only on a dangling registered `command` (the one state that breaks every Claude session) | High |
| U-002 | V3 | `install --list` prints owned vs external paths from the receipt | Medium |
| U-003 | V3 | Daemon-aware deferred deletion of older receipt-listed version dirs | Medium |
| U-004 | V2 | Failure message names the exact manual recovery command on stderr | Medium |

## Shared Assumptions

| # | Agreement Source | Assumption | Classification | Promoted |
|---|---|---|---|---|
| A-001 | All register `command` = realpath with an `env` object; all reuse "never replace an entry carrying env/headers that the user wrote" | The existing guard (`install_mcp.py:858-864`) refuses any entry with `env`. IronClaude's own codegraph entry always has `env` and its realpath changes on every pin bump (new version dir), so a re-run would hit the guard on its own entry unless the guard distinguishes IronClaude's known env keys from user-written env. Under A/C this makes every pin bump exit 1; under B it leaves a stale entry. | UNSTATED | Yes |
| A-002 | A and C write a receipt; C deletes "receipt-listed older version dirs" | The receipt must record every IronClaude-owned version dir (a list), not only the current tag, or a pin bump loses ownership of the previous dir. | UNSTATED | Yes |
| A-003 | All: Coder bakes the binary before the pin bump (context constraint 3, install-update-flow §5.3 step 1) | The bake is at the exact pin and on PATH, so the reuse path wins with no network inside the 60 s bound; stated for A/C, relied on implicitly by B. | STATED | No |
| A-004 | All: `~/.claude/CLAUDE.md` `CODEGRAPH_START` leftover check | `install --force` already overwrites `~/.claude/CLAUDE.md` before doctor in `update.sh`, so the block check only matters for standalone `doctor`. | UNSTATED | Yes |

## Summary
- Structural: 2; content: 9; contradictions: 4; unique: 4; shared assumptions surfaced: 4 (UNSTATED 3, STATED 1, CONTRADICTED 0); promoted A-001, A-002, A-004.
- Highest-severity items: C-001, C-002, C-003, C-006, C-009, X-001, A-001.
- Similarity: well above 10% difference; debate proceeds.
- Taxonomy pre-tag: L1 S-001; L2 S-002, C-003, C-004, C-006, C-007, C-009, X-003, X-004, U-002, U-004; L3 C-001, C-002, C-005, C-008, X-001, X-002, U-001, U-003, A-001, A-002, A-004.
