# Diff Analysis: position papers on the K-arm lead-in (DD-14)

## Metadata
- Generated: 2026-11-15, by the orchestrating session after Round 1 and updated after Round 2.
- Variants compared: 3 (V1 haiku defender, V2 sonnet prosecutor, V3 sonnet architect). Mode B (generated position papers), so the structural and content tables are about the argument, not about section layout.
- Total differences found: 9 content, 4 contradictions, 4 unique contributions, 5 shared assumptions.

## Structural Differences
| # | Area | V1 | V2 | V3 | Severity |
|---|---|---|---|---|---|
| S-001 | Section layout | Required 7 sections, 43 lines | Required 7 sections, 54 lines | 8 sections, adds a requirements list, a design and a draft-against-design table | Low |

## Content Differences
| # | Topic | V1 (defender) | V2 (prosecutor) | V3 (architect) | Severity |
|---|---|---|---|---|---|
| C-001 | Verdict | NO blocking defect | NO blocking defect (looked for one, found none) | NO blocking defect | Low |
| C-002 | Replacement text | none | none | an own design (140 chars: "Here are the eight checks. Apply each one to the plan. ... may fail none of them ...") | Medium |
| C-003 | Strongest case against own side | "your own review" against CB-5 | same, plus cost of a fix (splits RL copy) | the apply verb could turn K into SS-lite | Low |
| C-004 | Direction of bias | unknown, UNVERIFIED | favours SS by an unknown amount (only via "none") | leans toward SS via the missing apply verb (Round 1); weakened to a hypothesis in Round 2 | Medium |
| C-005 | "A plan may have none" | possible suppression, UNVERIFIED | weak or none; base and CB-2 push the other way | symmetric, no discouragement | Low |
| C-006 | Length and tone | the treatment, not a confound | the treatment (K 1,226 chars, SS 1,712 + sheet) | the treatment | Low |
| C-007 | Equivalence of information | not equivalent, by design | not equivalent, by design | not equivalent, by design | Low |
| C-008 | Definition (2) with no source document | not raised in Round 1; note in Round 2 | note N-4 | note N-4 | Medium |
| C-009 | Draft marker on line 1 | stale label, not contamination | stays in the frozen file (test-pinned) | stays (test-pinned) | Low |

## Contradictions
| # | Point of conflict | Position A | Position B | Impact |
|---|---|---|---|---|
| X-001 | Does time matter to D7? | V3 table row: "time is not an input to D7" | V1 Round 2: time reallocation changes found fraction | Low; resolved in Round 2 (V3: not a computed input, but a behavioural path) |
| X-002 | Direction of the apply-verb effect | V3 Round 1 row 1 names a direction (toward SS) | V3 Round 1 row 2 says "unknowable" for a similar sentence; V2 says no neutral wording exists | Medium; resolved in Round 2 (V3 drops "established direction") |
| X-003 | Size of the wording effect | V2 Round 1: 0.01-0.02 "below what these runs can resolve" | V1 Round 2: no calculation supports it | Low; V2 withdrew the number |
| X-004 | A ninth class card | V2 N-3: "Eight kinds" would sit over nine entries silently | `tests/test_briefs.py` line 190 asserts `len(cs) == 8` | Low; corrected (CORR-1) |

## Unique Contributions
| # | Variant | Contribution | Value |
|---|---|---|---|
| U-001 | V3 | Design requirements, an alternative lead-in and the reading sentences for the owner | High |
| U-002 | V1 (Round 2) | `analysis/analyze.py` never reads `no_source` (confirmed, CORR-7) | High |
| U-003 | V2 | The "Eight" hard-coding and the stale DESIGN 724 sentence | Low |
| U-004 | fault-finder | Untracked files and no hash in the owner record; RL copy drift; no K spike; D7 noise; run-set equality in the arithmetic; CB-1 already covers definition (2); judge blindness | High |

## Shared Assumptions
| A-NNN | Assumption | Source agreement | Impact | Status |
|---|---|---|---|---|
| A-001 | No real-model K run exists, so every statement about the wording effect is unmeasured | all three, F9 | High | STATED |
| A-002 | The owner's definition of K (MR 1035) is correct and is not under review | all three | High | UNSTATED as an assumption; stated as a boundary |
| A-003 | D7 (and the K-versus-RL row) are the only places K feeds a decision; D2 never reads K | all three | Medium | UNSTATED |
| A-004 | Every decision plan has a source document | V2, V3 (as UNVERIFIED) | Medium | STATED as UNVERIFIED |
| A-005 | The freeze (14.5) happens before any K run and keeps the approved bytes | all three | Medium | UNSTATED; probed in Round 2.5 (INV-001, INV-002) |

## Summary
- Structural 1, content 9, contradictions 4, unique 4, shared assumptions 5 (STATED 2, UNSTATED 3, CONTRADICTED 0).
- Highest-severity items: C-002, C-004, C-008, X-002, U-004.
