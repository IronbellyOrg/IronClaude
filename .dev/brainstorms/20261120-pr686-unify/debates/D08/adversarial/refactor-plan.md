# Refactoring Plan (D08)

Base: Variant 1 (OURS). Approval: auto-approved (unattended).

## Overview
- Base variant: Variant 1 (`variant-1-original.md`)
- Incorporated from Variant 2: 6 changes
- Corrections to the base: 5
- Overall risk: Low (additive plus factual corrections)

## Planned Changes

| # | Title | Source | Target in base | Approach | Rationale (debate evidence) | Risk |
|---|---|---|---|---|---|---|
| 1 | Keep Clay's flag set and `--sub` | V2 fact 1; D:133 | Claim, command row | append | Advocate 2 R1 strength 3: OURS had no flags; A1 R2 accepted; capability OURS lacked | Low |
| 2 | Species terms and contract section | V2 mechanism; D:799, ADD1 D:135 | Mechanism | replace "qualifiers" list | A1 R2 point (4): use "person-opened coordinator" and "standing-grant coordinator"; ADD1 section kept inside WORKER-CONTRACT section 4 | Low |
| 3 | Report coordinator, deployed names unchanged | V2 fact 5; `config.json:11-12`, D:714, OD6 | Costs and Claim | replace | A1 R1 conceded X-005; both agree | Low |
| 4 | Process name "orchestrated issue flow" | V2; ADD1, `common.py:134` | Claim | insert | A1 R2 point (5) accepted | Low |
| 5 | Nesting table for 339, 423, 444, Clay's design, report session | A1 R2 final table, A2 R1 table | new section | insert | Both originals lacked a usable table; fixes dangling reference | Low |
| 6 | Settle persisted names before PR 686 merges | V2 weakness 7 | Costs | insert | A2 R1 strength 6; wire strings pinned in `wake.py:46-47`, `test_wake.py`, `test_launch.py:98-99` | Low |

## Corrections to the base
1. IronOrchestrator is a design-doc and repo name, not an identifier PR 686 adds (0 hits in pr-a src and tests).
2. `orchestrator_tier` is 15 lines (10 src, 5 tests), not 13.
3. R10's "everywhere" sits in a row about the worktree and branch name; the command-name conclusion rests on R9 line 40, R10 line 41 and R17 line 43 together, plus the ORCH- to COORD- session rename.
4. Q26 `final.md` defines the coordinator at line 3, not line 6.
5. "Cheap" holds only until PR 686 merges.

## Changes NOT Being Made
| Diff point | Non-base approach | Why the base stands |
|---|---|---|
| C-001, C-002 | `/sc:orchestrator`, `sc-orchestrator-protocol`, "orchestrator" as the session noun | R9/R10/R17, Orca role table, 63-file collision; Advocate 2 withdrew |
| C-003 | Second noun for authority | Authority belongs to a recorded grant, not a noun (INV-001) |
| C-005 | "host coordinator" for 339 | Not in 339's text; "all-sessions coordinator" is |
| X-001 | Treating OQ5 as an owner decision | OQ5 owner column is "no"; not among OD1 to OD15 |

## Risk Summary
All low. The one open item is the ccsession tag form (INV-002), a build check.

## Review Status
auto-approved
