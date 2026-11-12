# Synthesis-Gate Fix Log (Phase 5, fix cycle 2: repeat cycle 1)

**Task:** TASK-RESEARCH-orchestrator-supervision-20261107-073942 (issue #339, orchestrator mode Phase 1)
**Date:** 2026-11-07
**Input:** `qa/qa-consolidated-findings-phase5-cycle1.md` (|F_1| = 3, C1-01 to C1-03)
**Scope:** targeted Edits in `synthesis/` only; evidence re-read from `research/` and the task file. MINOR notes not fixed.

## Entries

| ID | File | Line(s) | Change | Evidence (path:line) | Status |
|---|---|---|---|---|---|
| C1-01 | `synthesis/synth-03-external-findings.md` | 114 | Replaced "Phase 1 can keep person-wait time out of any age it prints." with "Phase 1 keeps person-wait time out of activity ages and the 6 h activity window; the waiting-on-a-person list prints the time since the wait began (R4)." Now agrees with R4 (`:216`) and S5 step 1.5 (`:63`). | `research/scope-04-409-layout.md:87` ("original age" is a retained fact); `research/web-01-agent-supervisor-session-health.md:171` (wait excluded from stalled and the activity window); `synthesis/synth-05-implementation-plan.md:63` | fixed |
| C1-02 | `synthesis/synth-05-implementation-plan.md` | 10 ("Research question" row) | Class list reworded to "(waiting on a person, working, stalled (proved), finished, could not determine, idle: the research question's six; Section C adds fenced as a seventh, the working default, OQ-13)". Optional S1 `:15` alignment not done (not required). | Task file GOAL `TASK-RESEARCH-orchestrator-supervision-20261107-073942.md:54`, `:90` (six classes, no fenced); `research/research-notes.md:188`, `:194` (seven, fenced own class); `synthesis/synth-05-implementation-plan.md:225` (OQ-13) | fixed |
| C1-03 | `synthesis/synth-03-external-findings.md`; `synthesis/synth-02-target-gaps.md` | S3 183; S2 290 | S3: "three external sources contradict WC-10" replaced by "four external patterns contradict WC-10 and are rejected" (D5, D6, D1, D2 in part), plus a sentence that D3 and D4 are rejected as naming or actions, not as contradictions of absence-is-not-death; "Kubernetes node status at the status layer" kept in the supporting list. S2 4.8 row: "Harmonograf and Kubernetes act on a timeout" replaced by Kubernetes taint/eviction and probe restart, Harmonograf "stuck" label with UI alert only; only D1 contradicts WC-10. | `research/web-01-agent-supervisor-session-health.md:136` (eviction "exactly what WC-10 forbids"), `:159` (agents-fleet automatic abort), `:163` (Harmonograf alert only, no restart), `:181-184` (D1-D4); `research/web-02-static-status-report-conventions.md:28`, `:30`, `:50` (Kubernetes status layer supports; Grafana contradicts); `synthesis/synth-03-external-findings.md:81`, `:169-174` | fixed |

## Result

Fixed 3 of 3 blocking findings. No MINOR note was fixed. No fact was added beyond the research; nothing routed to Section 9.
