# A.10.5 Task file qualitative validation, consolidated (cycle 1)

Date: 2026-11-08
Task file: TASK-RF-sweep-phase1-20261108-072653.md (2863 lines, 351 items)

## Items Reviewed

| Report | Lens | Partition | Verdict | Blocking | Minor |
|---|---|---|---|---|---|
| qa-qualitative-operational-report-p1.md | operational-correctness | Phases 1-7 | FAIL | 7 IMPORTANT (Q-01 to Q-07) | 11 |
| qa-qualitative-operational-report-p2.md | operational-correctness | Phases 8-14 | FAIL | 2 IMPORTANT (OPS-01, OPS-02) | 8 |
| qa-qualitative-sufficiency-report.md | qa-gate-sufficiency | all gates | FAIL | 1 CRITICAL (QS-01), 1 IMPORTANT (QS-02) | 8 |

Combined: 11 blocking, 27 minor.

## Blocking findings (full text and item numbers in each report)

- QS-01 (CRITICAL): the final gate is sized from the 1013-line DESIGN but reviews the whole change set (more than 1500 lines), so it needs 5 rf-qa + 5 rf-qa-qualitative before domain lenses; it has 4+4+2.
- QS-02: the final and fidelity fix agents may edit DESIGN under `docs/`, so a fidelity finding could be closed by rewriting its source. Fidelity and final fix agents must not edit DESIGN or SPEC.
- Q-01: item 2.1 duplicates fields and breaks the DESIGN table.
- Q-02: the r3-b1 gate checks for the R3-B2 rule, which is not written yet.
- Q-03: item 2.6 drops the m2 edit.
- Q-04: an unrecorded SPEC deviation (record it in DESIGN section 13).
- Q-05: R2 says "sweeps on every wake", which contradicts master's section 4 limit "at most once every 5 minutes" (`WORKER-CONTRACT.md:110`); align R2 with master, per R4.
- Q-06: item 6.4's `^| R5 |` check can never pass.
- Q-07: item 5.10's grep always passes.
- OPS-01: items 14.9 and 14.43 count four files that were already untracked at the base (the design and the three `orchestrator-mode-review-*.md`) as task output.
- OPS-02: item 14.8 Branch A applies the 30 s limit to the pipx build, install and help; REPORT:1300 sets it for the help run only.

## Also open, not part of this fix cycle

- N-01 (A.10, after its review cap): item 5.12 places DESIGN line 835 in section 14; it is in section 13. Escalated to the coordinator (`msg_d3fa170b4220`); not to be fixed here without that decision.
