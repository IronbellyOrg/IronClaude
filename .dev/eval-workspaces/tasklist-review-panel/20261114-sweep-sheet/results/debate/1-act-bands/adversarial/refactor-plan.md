# Refactoring plan

Base: V3 (structure), amended by V2. Allowed files: `DESIGN.md` and `results/owner-decisions.md` only. Approval: auto-approved (non-interactive).

## Planned changes
| # | Source | Target | Change | Risk |
|---|---|---|---|---|
| 1 | V2, V3 | `DESIGN.md` 15.1 row 2 | keep the eight numbers; say the registration is numbers plus measure plus consequence; point to 15.1a | Low |
| 2 | V3 structure, V2 denominator | `DESIGN.md` new 15.1a | measure (act-and-survive among selected item-runs), 95% Wilson rule, not assessable under 10, report-only consequence, may-not list | Medium (new text) |
| 3 | probe INV-013 (HIGH) | 15.1a Measure | primary panel only; sets apart; hand join of `panel` and set | Low |
| 4 | probe INV-004, INV-008, INV-009, INV-015, INV-020 | 15.1a | finished-reviewer condition; shared-item counts once; may-not extended to `class_reach`, judge credit and Z0 or K rates; Stage 2 sets apart; "not assessable" note beside the REQ-45 sentence | Low |
| 5 | V2 | `DESIGN.md` 14.3 `stages.jsonl` row | one clause: stage `act` is not the band measure | Low |
| 6 | V3, probe INV-005, 017, 023 | `DESIGN.md` 15.2 | two Not-checked bullets: nothing computes the measure (applied by hand), no order check covers the text, Wilson limits, power zero for C1, C3, C6, C7, unknown class mix, transfer assumed | Low |
| 7 | probe INV-017 | `results/owner-decisions.md` | replace the open bullet: numbers unchanged, text in 15.1a, NOT confirmed, record confirmation with a commit id before the first hold-out run; text not copied (one governing source) | Low |

## Changes NOT made
| Point | Rejected | Why |
|---|---|---|
| numbers | widening or moving any band | width was not the defect; unmeasured numbers cannot be improved without data |
| C-007 | pooled band (0.223-0.456) or Z0-anchored band | pooled depends on the unregistered class mix; Z0 act is a different quantity and D2 already tests SS against Z0 |
| V1 | "report departures" with no rule | no comparison fixed before the data |
| V3 | 3-distinct-items floor | no arithmetic supports it (V3 dropped it) |
| V2 | optional pooled cross-check, 90% interval | dropped by V2 |
| V3 | a copy of the text in `owner-decisions.md` | one governing source; pointer instead |
| code | any edit to `analysis/analyze.py`, `prereg()`, tests, `TESTING.md`, `bin/` | outside the files this task may edit; recorded as not built in 15.2 |
| text | "drop the REQ-45 wording" | `TESTING.md` 149 pins that sentence; a caveat beside it instead |

## Risk summary
Overall Low to Medium: documentation only; numbers unchanged; no test pins the 15.1 wording (probe INV-016).
