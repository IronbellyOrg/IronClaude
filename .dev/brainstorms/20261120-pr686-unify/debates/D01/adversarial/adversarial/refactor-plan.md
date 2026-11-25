# Refactoring Plan (D01)

## Overview
- Base: Variant A (OURS), `variant-1-original.md`
- Incorporated: Variant B (CLAY) strengths 1 to 3 and the probe requirements MR-1, MR-2
- Planned changes: 6; rejected changes: 4; overall risk: Medium (the wording of a recommendation, no code is changed)

## Planned Changes

| # | Title | Source | Target in base | Approach | Rationale (debate evidence) | Risk |
|---|---|---|---|---|---|---|
| 1 | Add `plan_check` as a skip reason before approval | B, mechanism step 4 and fact 7 | "Recommended rule" and "What it gets right" | insert | C-005 B 75%; both advocates want it; pure function, no I/O (`hold.py:122-143`) | Low |
| 2 | Add `hold:backlog` as a read-only veto | B, mechanism and R1 | "Recommended rule" | insert | Both advocates accept; labels already in the discovery row; no watcher write (D09 decides label writes) | Low |
| 3 | Narrow the C-006 claim | A fact 6 | "Cited facts" 6 | restructure | Round 2: B is not silent (AD-A3, `orchestrator.md:488`); the approval's added value is binding a person's yes to the content they read, which matters when the worker can push and merge; C-006 A 65% | Medium |
| 4 | State requirement MR-1 | Probe INV-001 | "Recommended rule" | append | HIGH finding: the start-time re-check must include approval, `unchanged_since` and Status allow-list; PR 686's wave 1 re-checks only `hold:backlog` and `plan_check` (`orchestrator.md:488`); master has `_revalidate` (`cycle.py:979`) | Medium |
| 5 | State requirement MR-2 | Probe INV-002 | "Recommended rule" | append | HIGH finding: a manual `/sc:issue --claim` assigns and posts the claim marker; master's `marker_in_window` (`cycle.py:858,946-947`) prevents a second start; PR 686 has no equal | Medium |
| 6 | Add reopening condition and owner decisions | B Round 2 (b), A Round 2 (d) | new section "Conditions to revisit" | append | Both advocates: assignment alone safe only if (1) guard effective, (2) workers cannot push or merge, (3) claim-record skip, (4) owner records the R19 reversal in chat | Low |

## Changes NOT Being Made

| Diff point | Non-base approach | Rationale |
|---|---|---|
| C-001 / S-002 | Assignment alone as the start | Both advocates final: A 72 to 75%; owner records R19, R35, R36 and "Gates that stay manual"; B conceded it is decisive |
| C-004 | Treat L-1 as a reason to drop the approval | L-1 applies to every login-based signal including assignment; a speed bump still stops accidents (A Round 2); recorded as an accepted risk instead |
| C-008 | Read R35 and R36 as an owner trend to fewer gates | REQ line 62: R36 withdraws only R31; keeps the edit rule |
| C-010 | Remove approval, edit, Project and approver-file reads from `issue_watch/` | Those reads are the start signal; removing them is the contested rule (PR 686) |

## Risk Summary
- Change 3: if the owner prefers the stronger C-006 wording, revert to the original fact 6.
- Changes 4 and 5: they impose requirements on whichever tree is built; flagged for the spec.

## Review Status
auto-approved (unattended mode)
