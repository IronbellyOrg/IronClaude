# Qualitative Scoring Pass 2 (reverse order: Variant 3, 2, 1)
<!-- Returned by a read-only scoring agent (sonnet); persisted by the orchestrator. Evidence cells condensed; verdicts verbatim. -->
<!-- Orchestrator arithmetic note: the agent reported Variant 1 = 24/30, but its own verdicts sum to 26/30 (C5 K4 T5 L3 R5 E4). The corrected total is used below. -->

## Variant 3
| criterion | verdict | evidence |
|---|---|---|
| C1 | NOT MET | no D-001..D-014 coverage |
| C2 | MET | R3-F3 failed add, leak, mislabelled body errors |
| C3 | MET | R3-F7 git init -b master; R3-F6 later files |
| C4 | MET | R3-F4 awk+grep; R3-F2 worktree list back to one |
| C5 | NOT MET | no out-of-scope statement |
| K1 | NOT MET | R3-F4 scripts half conceded |
| K2 | MET | R3-F1 registration; R3-F3 rmdir then raise |
| K3 | NOT MET | R3-F1 `necessary` (conceded drift) |
| K4 | MET | consistent severities and disputes |
| K5 | NOT MET | R3-F7/F8 no evidence; .venv and R3-F5 inferred |
| T1 | MET | medium first |
| T2 | MET | uniform blocks |
| T3 | MET | separate sections |
| T4 | MET | disputes cite R3-F1..F3; header cites shell section 5 |
| T5 | MET | all eight fields |
| L1 | MET | exact commands, e.g. git diff HEAD |
| L2 | MET | file:line quotes |
| L3 | NOT MET | R3-F2, F3, F4 headlines bundle 2-3 claims |
| L4 | NOT MET | fail-before, global-setup, necessary undefined |
| L5 | MET | concrete Task edits |
| R1 | MET | 9 findings with severity |
| R2 | MET | recommendations |
| R3 | MET | R3-F3 rmdir, MasterCheckoutError, try/finally around yield |
| R4 | MET | R3-F7 host config; R3-F4 gh scripts |
| R5 | MET | R3-F2 main() test; R3-F8 behavioural test |
| E1 | MET | R3-F3 no-master repo; R3-F2 back to one entry |
| E2 | MET | R3-F1 dataclasses reads sys.modules |
| E3 | MET | R3-F9 :313 filter |
| E4 | MET | R3-F6 residual misses later files |
| E5 | MET | R3-F4 CLAUDE.md:50 vs plan:117 |

## Variant 2
| criterion | verdict | evidence |
|---|---|---|
| C1 | MET | INF-015..INF-040 mapping |
| C2 | MET | R2-F2 global-setup untested |
| C3 | MET | R2-F1 full-depth non-root checkout |
| C4 | MET | R2-F1 rerun artifact with probes |
| C5 | NOT MET | none |
| K1 | NOT MET | R2-F3 premise refuted |
| K2 | MET | R2-F1 local clone or linked worktree |
| K3 | MET | drift labels |
| K4 | NOT MET | R2-F3 kept although inferred_claims says REFUTED |
| K5 | NOT MET | R2-F3 unsupported |
| T1 | MET | medium first |
| T2 | MET | uniform blocks |
| T3 | MET | separate sections |
| T4 | MET | inferred claims cite shell sections 1-2 |
| T5 | MET | all fields |
| L1 | MET | names artifact and probes |
| L2 | MET | quotes geteuid skip, :313 |
| L3 | NOT MET | R2-F1, R2-F2 headlines bundle two claims |
| L4 | NOT MET | INF rows, Search A/B, global-setup undefined |
| L5 | MET | R2-F2 raising test |
| R1 | MET | three findings with severity |
| R2 | MET | recommendations |
| R3 | NOT MET | R2-F2 failure mode without recovery; R2-F3 refuted |
| R4 | MET | R2-F1 skipif dependencies |
| R5 | MET | R2-F1 rerun artifact |
| E1 | NOT MET | none |
| E2 | MET | R2-F2 exit filter vs global-setup |
| E3 | MET | R2-F2 :313 guard |
| E4 | MET | search counts reproduced |
| E5 | MET | R2-F2 interaction with exit scope |

## Variant 1
| criterion | verdict | evidence |
|---|---|---|
| C1 | MET | 14-row deviations_resolution |
| C2 | MET | R1-2 leak; teardown may hide exception |
| C3 | MET | R1-1 registration; R1-3 Task 3 vs 4 |
| C4 | MET | R1-2 dir gone; R1-5 section grep |
| C5 | MET | R1-6 scripts outside scope |
| K1 | MET | R1-1, R1-2 confirmed; R1-3..R1-5 match quotes |
| K2 | MET | R1-2 rmdir; non-masking teardown |
| K3 | MET | drift and authorized only |
| K4 | NOT MET | D-001 resolved vs R1-1 |
| K5 | MET | plan line plus source line quotes |
| T1 | MET | task order, medium first |
| T2 | MET | uniform blocks plus table |
| T3 | MET | separate sections |
| T4 | MET | table notes reference R1-4, R1-5 |
| T5 | MET | all fields |
| L1 | NOT MET | D-002 "resolved: yes" yet note "R1-4, R1-5 remain" |
| L2 | MET | plan :88 vs :111 quotes |
| L3 | MET | R1-3 headline |
| L4 | NOT MET | resolved, drift, authorized undefined |
| L5 | MET | R1-4 CLAUDE.md:70 rewrite |
| R1 | MET | six findings with severity |
| R2 | MET | recommendations |
| R3 | MET | R1-2 rmdir; non-masking teardown |
| R4 | MET | R1-6 guarded fallback |
| R5 | MET | R1-5 grep; R1-2 assertion |
| E1 | NOT MET | none |
| E2 | MET | R1-1 dataclass needs sys.modules |
| E3 | MET | R1-2 teardown replaces exception |
| E4 | MET | D-003 counts |
| E5 | MET | R1-4 CLAUDE.md:70 vs positional form |

## Summary (corrected arithmetic)
| variant | Completeness | Correctness | Structure | Clarity | Risk | Invariant | Total/30 |
|---|---|---|---|---|---|---|---|
| Variant 3 | 3 | 2 | 5 | 3 | 5 | 5 | 23 |
| Variant 2 | 4 | 2 | 5 | 3 | 4 | 4 | 22 |
| Variant 1 | 5 | 4 | 5 | 3 | 5 | 4 | 26 (agent reported 24) |
