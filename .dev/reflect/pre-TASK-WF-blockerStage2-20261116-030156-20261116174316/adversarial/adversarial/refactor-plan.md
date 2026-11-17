# Refactoring Plan (Step 4)

## Overview
- Base: variant-3-original.md (reviewer card 3). Output: a merged finding register (one card) with the plan verdict, graded by consequence (blocking = a requirement or check that cannot be met, a wrong or missing result, or data loss; minor = wording or format; Medium = a real non-blocking weakness, reported under follow-up candidates).
- Approval: auto-approved (non-interactive).

## Planned changes
| # | Change | Source | Target in base | Rationale (debate) | Risk |
|---|---|---|---|---|---|
| P-1 | Add finding MB-1 (Task 8 confirmation ids are bare, ledger ids are run-scoped; require `run_id:id`) as BLOCKING | V2 R2-1 | Findings, first | A1 80, A2 95 blocking; A3 "fixable one-line gap" does not change the consequence (a stage 3 entry number is ambiguous) | Low |
| P-2 | Add finding MB-2 (Task 7 agents see only the blind table, so M, C, E answers cannot be code-informed; contested, graded by consequence) as BLOCKING | V2 R2-2 | Findings | A2 90; A1 minor 65, A3 wording 40; consequence: the evaluation the owner reads for the stage 3 go measures the text-only judge that plan:28 says is at chance | Medium |
| P-3 | Add finding MB-3 (GR12 safety row -> `partial` missing from Task 5 and its tests; "follow-ups alone never change" has no exception) as BLOCKING | V1 R1-2 | Findings | spec:438; A1 70, A2 conceded; A3 R1 agrees | Low |
| P-4 | Keep and narrow MB-4 (R3-3/C-007: Phases 3 and 5 analyst and qualitative reviewers get no `rests_on` fields; two of the five edited templates are LEGACY) as BLOCKING | V3 R3-3 | Findings | A2 95, A3 65 after new evidence (SKILL.md:479-487, 507-516, 819, 952, 1003; rf-analyst.md:195-202) | Low |
| P-5 | Downgrade R3-1 (tag persistence, C-005) to non-blocking Medium MN-1, add INV-001 (second `write` may reset tags) | V3 R3-1 + INV-001 | Follow-ups | A3 conceded to minor 55 (stage1 plan:196 "tags the row"); A1 blocking 60 only if safety_route.py does not save it; nothing tests it | Low |
| P-6 | Downgrade R3-2 (tier mapping, report format) to non-blocking MN-2 | V3 R3-2 | Follow-ups | A3 conceded; stage1 plan:62 LABEL=Outcome pairs; rf-qa.md:448 Severity column; residue: no family selector, two column layouts | Low |
| P-7 | Add MN-3 /sc:implement sweep has no ledger and the printed line is unconditional | V1 R1-1 (+ V3 follow-up) | Follow-ups | A1 and A3 minor after round 2 (plan:138 states the tech-research-only limit); the printed "recorded and not filed" line is false in a zero-ledger run | Low |
| P-8 | Add minor items from V1: call-line (merge with R3-5), printed-list producer (R1-4), no unattended mode (merge with R3-7) | V1 | Minor | agreed minor by all advocates | Low |
| P-9 | Add fault-finder items INV-002, 003, 004, 005, 006, 007, 008, 009, 010 as follow-up or minor | invariant-probe.md | Follow-ups | no HIGH unaddressed; MEDIUM are warnings | Low |
| P-10 | Keep R3-4 (entry check), R3-6, R3-8 as minor; withdraw R2-3 (traceability only, withdrawn by its advocate) and T1 F5/F7 as non-defects | V3, V2 | Minor / Refuted | R3-4 "after edits" overstated (plan:59); F5 body vs acceptance is a wording tension kept as MN-minor via INV-009 | Low |

## Changes NOT being made
- V2 R2-3 (matrix omissions) is not a plan finding: its advocate withdrew it; the by-hand disposition shows no requirement missing.
- V3 R3-1 "by construction" claim: rejected as stated (conceded by its advocate).
- V1 R1-1 stays out of the blocking list (consequence: misleading printed line, no data loss; both its advocate and the base advocate rated it minor after round 2).

## Review status: auto-approved
