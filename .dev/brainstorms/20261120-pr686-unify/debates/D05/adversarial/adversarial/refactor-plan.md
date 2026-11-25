# Refactoring Plan (Step 4): D05 merged position

Base: `variant-2-original.md` (CLAY). Incorporated from: `variant-1-original.md` (OURS), the debate (`debate-transcript.md`) and the invariant probe (`invariant-probe.md`). Paths in this file are relative to the folder `adversarial/adversarial/` unless absolute.

## Overview

- Output: a single merged position paper, `../merged-output.md`, whose sections are: Question, Merged position, Evidence both lines agree on, Where the lines differ and how the debate settled each point, Controls and what each one covers, Open items.
- Changes planned: 9 (7 incorporations from non-base or debate, 2 base weaknesses fixed). Changes rejected: 4.
- Overall risk: Low to Medium. Every change is additive or a correction; no recommendation is reversed.

## Planned Changes

| # | Change | Source | Target in base | Approach | Rationale (debate evidence) | Risk |
|---|---|---|---|---|---|---|
| 1 | Restate the owner's G1 acceptance exactly: accepted for "the one first test issue"; "Before any other issue runs through the flow, the worker must be bound to the guard (G2)" | V1 fact 2; `issue-pipeline-guard-g2.md:9` | Base Claim and fact 1 | replace the "adds no new exposure" sentence | C-007 OURS 78%; both advocates agree; base fact 1 was graded NOT MET on Correctness 1 | Low |
| 2 | Add that level FS equals Clay's own OD1 policy and that its three prohibitions are enforced by grid rows PUSHFORM, PROTECTED, MERGE (LD:113-115) | V1 Mechanism 3 | Base Mechanism | insert after item 3 | C-009 OURS 67%; U-001 | Low |
| 3 | Add: the audit verb takes `--pr <N>`, so a push to `master` with no pull request has nothing to audit; no CLAY control acts on a worker push | V1 fact 5; both Round 2 files | Base fact 7 | append a limits sentence | C-005 lean OURS 63%; conceded in full by the CLAY advocate | Low |
| 4 | Add the K22 and U42 precedent: a session-scoped hook exists (marker plus pending record; OB-CTX PASS), but the guard has no level that merges, so it cannot bind the orchestrator | V1 fact 4 corrected by both Round 2 files | Base Risks, first bullet | insert, with the correction | C-010 SPLIT 60%; U-002 shrinks from "already built" to "precedent" | Low |
| 5 | Add the live evidence for the guard's grid: implement, four commit blocks, merge block, OB-CTX; and that OB-H2's FAIL rows are verbatim-detail checks | V1 fact 6 and fact 7 | Base fact 2 | insert beside the FAIL list | C-003 SPLIT; X-002 OURS 67% | Low |
| 6 | Add the binding facts: `publish_pending` at `orca_worktree.py:1488`, `cmd_pending` at `:1515`; the marker slot was deleted with `brief.py`; `cmd_pending` runs no preflight; binding fails closed with LL-NOBIND when a marker arrives; the receipt `pending/<nonce>` gone proves binding without a session id; the G2 collisions and the `.ok` release apply only at level W | Round 2 files | Base fact 6 | replace | C-002 unresolved lean CLAY 55%; X-001 CLAY 67% | Medium |
| 7 | Add the invariant-probe limits, in plain words: binding at FS closes K12 only for plain pushes to `master` and `main`; a script run (`bash ./push.sh`) passes every gate (INV-034); `integration` or another default branch passes (INV-019); a new session id runs unbound while the receipt reads clean (INV-003); "second real issue" cannot be counted (INV-015); K12 is closed only by a push-time control outside the worker (INV-037) | `invariant-probe.md` | new section "Controls and what each one covers" | insert | 7 HIGH UNADDRESSED items block convergence; the merge carries them forward as stated limits | Medium |
| 8 | Fix the base's ambiguous word "owner": the repository owner is `ironbelly`; "the owner (Clay)" in D:3 and D:1152 is the account `clayphi`; ruling 3's row (D:1397) omits the guard; D:970 and D:975 leave binding open | Round 2 files; `H-design681-map.md` | Base Claim, fact 8 | replace | Clarity 1 NOT MET on the base; C-007 | Low |
| 9 | Keep the base's friction finding but narrow it: reply and resolve run in scripts and work through a pinned leak; the summary-thread and fallback comments are inline `gh api` POST (GHWRITE at FS, `refs/thread-reply.md:87-100`); a bare `/sc:pr-submit --monitor 3` cycle at FS has never been observed | base fact 5; Round 2 files | Base fact 5 | replace | C-006 lean CLAY narrow 55% | Low |

## Base Weaknesses Addressed

| Issue in base | Better variant | Fix |
|---|---|---|
| States "no new exposure" while its source asks for binding before any other issue | V1 | Change 1 |
| Names no push-time control and no fallback if the binding probe fails | V1 and the debate | Changes 3, 7, and the Open items section (server-side rule on `master`, owner action) |

## Changes NOT Being Made

| Diff point | Non-base approach | Why the base approach stands |
|---|---|---|
| X-003 | V1 Claim: "nothing the system starts runs ungoverned" | False today (LD:23, LD:349); conceded by the OURS advocate. The merged text states it as the rule that should hold, not as the state of master |
| C-004 | V1 reading of R33 as honest gating only | R33 gates only the watcher's claim launches (`launch.py:48`); both advocates agree it does not forbid binding a `worker-start` worker. Merged text says exactly that |
| C-001 | V2 "the design must not make workers wait for the guard" | The debate settled for requiring binding, staged behind a probe (OURS 71%); the merged text keeps staging, not exemption |
| C-008 | V1 or V2 proposing a ruleset | Neither paper proposed one and the debate did not decide it; the merged text lists it as an open owner action with the live value, not a recommendation made by the merge |

## Risk Summary

Changes 6 and 7 carry the most risk: they add many specific line citations. Each is taken from a source the advocates re-read; the merge must keep UNVERIFIED marks (`worker-start` delivery of the marker as a hook event; whether a hook timeout lets a call through; whether Claude Code issues a new session id on `/clear` or resume; the worker's HOME, PATH, MCP set and host operating system). Rollback for every change: delete the inserted sentence; the base text stands.

## Review Status

Auto-approved (non-interactive, `--unattended`). Timestamp 2026-11-20.
