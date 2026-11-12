# R4 WC-14 hits in docs/designs/orchestrator-mode.md (item 5.1)

Classes: `coordinator loop (rename)`, `worker rule (keep)`, `historical name (keep)`. The third class is only for a hit that names the SPEC's or the REPORT's earlier WC-14 draft (section 13 row D6, section 13 row 1.17).

## Before (`grep -n 'WC-14' docs/designs/orchestrator-mode.md`, 16 hits)
```
5:Status: design for review, issue #339 Phase 1, written 2026-11-08 by `/sc:design --type architecture --forma
13:Phase 1 adds one read-only command, `superclaude sweep run`, a thin `/sc:sweep` command and `sc-sweep-proto
666:## 8. WC-14 and the never-as-worker list
668:**Gate.** Steps 1.17 to 1.19 are written only after the owner answers GQ-11 (step 1.0b) and the PR #422 ov
675:### WC-14. Coordinator loop
684:- Add to `RULE_PHRASES` (the dict at line 25; WC-13 is at line 155): `"WC-14": ("WC-14", ["WC-14. Coordina
702:| R2 | Same file, `## Orca coordination` (line 396) | One bullet after the never-workers bullet (line 403)
708:| R8 | `CHANGELOG.md`, `## [Unreleased]` (line 5) | One `### Added` entry: `superclaude sweep run`, `/sc:s
722:# superclaude sweep reports: dated, operator-local, never posted (WC-14). Never tracked.
784:| FR-023 | WC-14 and the never-as-worker addition (8) | `tests/skills/test_worker_contract.py` |
819:| D6 | WC-14 text of SPEC section 10 (lines 404-408) | The same text with one sentence appended: the coord
842:| 1.17 | The REPORT's WC-14 draft | The SPEC section 10 text plus D6 (section 8) |
933:| 1.17 | | WC-14 in `src/superclaude/core/WORKER-CONTRACT.md` | 8 | 1.0b (GQ-11 answered), 1.16a |
960:| WC-14 with the D6 sentence, the line 23 never-as-worker entry, the `RULE_PHRASES` entry, the `NEVER_AS_W
995:| 20 | Owner decisions GQ-10, GQ-11 (WC-14 approval), GQ-35, GQ-61 and GQ-63 | Step 1.0b | Steps 1.17 to 1
996:| 21 | PR #422 overlap with WC-14, the never-as-worker list and the #409 dimensions | Step 1.16a | Steps 1
```

| Line | Class |
|---|---|
| 5 | coordinator loop (rename) |
| 13 | coordinator loop (rename) |
| 666 | coordinator loop (rename) |
| 668 | coordinator loop (rename) |
| 675 | coordinator loop (rename) |
| 684 | coordinator loop (rename) |
| 702 | coordinator loop (rename) |
| 708 | coordinator loop (rename) |
| 722 | coordinator loop (rename) |
| 784 | coordinator loop (rename) |
| 819 | historical name (keep) |
| 842 | historical name (keep) |
| 933 | coordinator loop (rename) |
| 960 | coordinator loop (rename) |
| 995 | coordinator loop (rename) |
| 996 | coordinator loop (rename) |

## After item 5.1 (section 8 only)
```
5:Status: design for review, issue #339 Phase 1, written 2026-11-08 by `/sc:design --type architecture --forma
13:Phase 1 adds one read-only command, `superclaude sweep run`, a thin `/sc:sweep` command and `sc-sweep-proto
668:**Gate.** Steps 1.17 to 1.19 are written only after the owner answers GQ-11 (step 1.0b) and the PR #422 ov
702:| R2 | Same file, `## Orca coordination` (line 396) | One bullet after the never-workers bullet (line 403)
708:| R8 | `CHANGELOG.md`, `## [Unreleased]` (line 5) | One `### Added` entry: `superclaude sweep run`, `/sc:s
722:# superclaude sweep reports: dated, operator-local, never posted (WC-14). Never tracked.
784:| FR-023 | WC-14 and the never-as-worker addition (8) | `tests/skills/test_worker_contract.py` |
819:| D6 | WC-14 text of SPEC section 10 (lines 404-408) | The same text with one sentence appended: the coord
842:| 1.17 | The REPORT's WC-14 draft | The SPEC section 10 text plus D6 (section 8) |
933:| 1.17 | | WC-14 in `src/superclaude/core/WORKER-CONTRACT.md` | 8 | 1.0b (GQ-11 answered), 1.16a |
960:| WC-14 with the D6 sentence, the line 23 never-as-worker entry, the `RULE_PHRASES` entry, the `NEVER_AS_W
995:| 20 | Owner decisions GQ-10, GQ-11 (WC-14 approval), GQ-35, GQ-61 and GQ-63 | Step 1.0b | Steps 1.17 to 1
996:| 21 | PR #422 overlap with WC-14, the never-as-worker list and the #409 dimensions | Step 1.16a | Steps 1
```

| Line | Class |
|---|---|
| 5 | coordinator loop (rename) |
| 13 | coordinator loop (rename) |
| 668 | worker rule (keep) |
| 702 | coordinator loop (rename) |
| 708 | coordinator loop (rename) |
| 722 | coordinator loop (rename) |
| 784 | coordinator loop (rename) |
| 819 | historical name (keep) |
| 842 | historical name (keep) |
| 933 | coordinator loop (rename) |
| 960 | coordinator loop (rename) |
| 995 | coordinator loop (rename) |
| 996 | coordinator loop (rename) |

Section 8 (lines 666-693) now has one WC-14 hit, line 668, the new sentence "WC-14 and WC-15 on master are worker duties from PR #434 and are not changed." (class worker rule). The remaining `coordinator loop (rename)` hits are in sections 1, 9, 10, 12, 15, 16 and 17 and belong to items 5.2 and 5.3.

## Check
- `grep -n 'WC-16. Coordinator loop' docs/designs/orchestrator-mode.md`:
```
675:### WC-16. Coordinator loop
684:- Add to `RULE_PHRASES` (the dict at line 25), after the `"WC-15"` entry (lines 165-172) and before the `"heartbeats
```

## After item 5.2 (sections 9 and 10)

- WC-14 hits in sections 9 and 10 (lines 695-730): 0 (expect 0)
- `grep -c 'sweeps on every wake\.\*\*'`: 0 (expect 0)
- `grep -c 'sweeps on every wake, at most once every 5 minutes\.\*\*'`: 1 (expect 1, the R2 bullet)
- The `.gitignore` block reads `(WC-16). Never tracked` in section 10: 1 (expect 1)
- Remaining WC-14 hits: 10 (lines 5 13 668 784 819 842 933 960 995 996 )

## After item 5.3 (sections 1, 12, 13, 14, 15, 16 and 17)

```
668:**Gate.** Steps 1.17 to 1.19 are written only after the owner answers GQ-11 (step 1.0b) and the 
819:| D6 | WC-14 (WC-16 in this design) text of SPEC section 10 (lines 404-408) | The same text with
842:| 1.17 | The REPORT's WC-14 (WC-16 in this design) draft | The SPEC section 10 text plus D6 (sec
```

| Line | Class |
|---|---|
| 668 | worker rule (keep) |
| 819 | historical name (keep) |
| 842 | historical name (keep) |

- `grep -c 'WC-14 (WC-16 in this design)' docs/designs/orchestrator-mode.md`: 2 (expect 2, the section 13 rows D6 and 1.17)
- `grep -n '^Total: 23 open items.' docs/designs/orchestrator-mode.md`: 1000:Total: 23 open items.
- Every remaining WC-14 hit is the section 8 sentence about WC-14 and WC-15 on master (worker rule, keep) or one of the two section 13 rows that name the SPEC's and the REPORT's earlier draft (historical name, keep). No coordinator-loop mention of WC-14 remains.

## After R4 fix cycle 1 (item 5.23)

The fix cycle changed the DESIGN from 1041 to 1043 lines, so the DESIGN line numbers above moved. The current WC-14 hits (4):
```
668:**Gate.** Steps 1.17 to 1.19 are written only after the owner answers GQ-11 (step 1.0b) and step 1.16a has
831:| D6 | WC-14 (WC-16 in this design) text of SPEC section 10 (lines 404-408) | The same text renumbered WC-
854:| 1.17 | The REPORT's WC-14 (WC-16 in this design) draft | The SPEC section 10 text plus D6 (section 8) |
1043:| R4 | DESIGN was written against base `e8db2fe6`; master `5dc29d23` already has WC-14 and WC-15, a coord
```

| Line | Class |
|---|---|
| 668 | worker rule (keep) |
| 831 | historical name (keep) |
| 854 | historical name (keep) |
| 1043 | worker rule (keep) |
