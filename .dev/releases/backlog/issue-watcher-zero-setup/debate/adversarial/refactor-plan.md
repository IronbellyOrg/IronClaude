# Refactoring Plan: merge into the base (V2, per-project instances)

## Overview
- Base: V2. Incorporated from V1: items 1 to 4. Carried from the invariant probe: items 5 to 12.
- Approval: auto-approved (non-interactive run).

## Planned Changes
| # | Change | Source | Rationale | Risk |
|---|---|---|---|---|
| 1 | The loop lives in the `issue-watch` entry point (a verb such as `run-all`), not in a wrapper script, and it is also the R8 sweep. | V1 | V2 advocate accepted (Round 2) | Low |
| 2 | One loop-level account rate wait, stored once in a loop-level file, applied only for the plain `rate_limited` reason (not `rate_limit_clamped`), children never write each other's stores. | V1, limited by V2 | github.py:418-431 | Medium |
| 3 | `MAX_LAUNCHES_PER_CYCLE` becomes one per sweep (the loop stops after the first `launched` child); `DAY_CAP` stays per repo and `status` prints it. The repo order rotates each sweep so one repo cannot hold the slot. | V1 and V2 Round 2; INV-005 | cycle.py:35, 36, 872-876 | Medium |
| 4 | Total loop cap about 270 s plus a per-child kill timer that is longer than the child's own 240 s deadline; unfinished repos are skipped and reported. | Both; INV-006 | cycle.py:41, 1091-1099 | Medium |
| 5 | The config generator always writes an explicit absolute `state_dir` per repo. | INV-001 | cycle.py:259-266 | High if missed |
| 6 | The repo is threaded from config into `github.py` (`REPO`, lines 37, 187, 208, 259) and `launch.py` (`ORIGIN_REPO`, lines 50, 249). This is code change, not reuse. | X-001, INV-003, INV-009 | both advocates verified | Medium |
| 7 | Each repo's `Coordinator` worktree exists with its origin matching the repo; the loop checks this before the child runs. | INV-003, INV-004, owner 2026-11-18 | launch.py:249 | High if missed |
| 8 | Labels `issue-watch:trigger` and `issue-watch:approved` are created on each repo by the per-project init (R11); a missing label is reported, not silent. | INV-010 | predicates.py:224-225 | High if missed |
| 9 | When `projectsV2` returns zero Projects, skip and report; several Projects, choose the one named in the central config and report the choice. | INV-007 | cycle.py:958 | Medium |
| 10 | A failed or timed-out `orca repo list` is an error exit, not "zero repos". Temporary and foreign-owner repos are skipped. | INV-007, INV-008 | requirements.md | Low |
| 11 | A newly generated config starts `enabled: false` until the owner switches it on; this stays a manual gate and is stated in the zero-setup requirements. | INV-011 | cycle.py:685-686 | Low |
| 12 | The design is not complete without R6 (scheduler), R9 (coordinator session) and R10 (Coordinator worktree) from the requirements file. | INV-012 | requirements.md | High |

## Changes NOT Being Made
- A single multi-project configuration file with a new schema version: not needed; both sides keep one config per repo (X-002).
- A shared day cap across repos: rejected; the count lives per store and a global one needs a new shared counter (V2 Round 2).
- Parallel children: not needed unless a measured sweep exceeds the cap (both advocates' stated condition).

## Risk Summary
Highest risk: items 6 and 7 (code threading and the worktree origin). Rollback for the loop: remove the scheduler entry; each repo's `DISABLED` file still stops that repo.

## Review Status
auto-approved.
