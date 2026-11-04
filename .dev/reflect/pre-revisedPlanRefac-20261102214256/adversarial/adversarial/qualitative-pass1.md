# Qualitative Scoring Pass 1 (order: Variant 1, 2, 3)
<!-- Returned by a read-only scoring agent (sonnet); persisted by the orchestrator. Evidence cells condensed; verdicts verbatim. The agent read the round-2 files but not the round-1 files. -->

Context facts used: R2-F3 premise refuted (probe 22:23Z); R3-F4 scripts half and R3-F1 `necessary` label conceded by V3 in Round 2.

## Variant 1
| criterion | verdict | evidence |
|---|---|---|
| C1 | MET | deviations_resolution maps D-001..D-014 |
| C2 | MET | R1-2 failed-creation leak |
| C3 | MET | R1-1 sys.modules registration before exec_module |
| C4 | MET | R1-2 assert mkdtemp dir gone |
| C5 | MET | R1-6 and F1 dispute: scripts out of scope |
| K1 | MET | R1-1, R1-2 confirmed by shell sections 5-6 |
| K2 | MET | sys.modules registration, os.rmdir feasible |
| K3 | MET | drift / authorized labels |
| K4 | NOT MET | D-001 "resolved: yes" beside R1-1 (conceded Round 2) |
| K5 | MET | R1-1 quotes plan:67, test :157-158, eval_runner.py:10,46-47 |
| T1 | MET | medium to low, then resolution, disputes, inferred |
| T2 | MET | uniform schema |
| T3 | MET | separate sections |
| T4 | MET | plan_location per deviation; T1 ids cited |
| T5 | MET | all eight fields |
| L1 | MET | R1-5 grep -n -w 'gh' on section range |
| L2 | MET | R1-3 plan:88 vs plan:111 |
| L3 | MET | R1-3 headline |
| L4 | NOT MET | Search A/B, drift, authorized undefined |
| L5 | MET | R1-4 names CLAUDE.md:70 |
| R1 | MET | six findings with severity |
| R2 | MET | every finding has a recommendation |
| R3 | MET | R1-2 rmdir on failed add; non-masking teardown |
| R4 | MET | R1-2 git add failure, remove exit 128 |
| R5 | MET | R1-2 test assertion; R1-5 section grep |
| E1 | NOT MET | no empty/single/max case |
| E2 | MET | R1-4 CLAUDE.md:70 vs positional gh rule |
| E3 | MET | R1-2 finally on unregistered dir |
| E4 | MET | D-003 note Search A 108/17, B 9/7 |
| E5 | MET | R1-3 one rule, three strengths |

## Variant 2
| criterion | verdict | evidence |
|---|---|---|
| C1 | MET | justification maps D-001..D-014 to INF-015..INF-040 |
| C2 | MET | R2-F2 global-setup failure untested |
| C3 | MET | R2-F1 how to obtain full-depth non-root checkout |
| C4 | MET | R2-F1 rerun artifact with probes |
| C5 | NOT MET | none found |
| K1 | NOT MET | R2-F3 premise refuted |
| K2 | MET | R2-F1 local clone or linked worktree, never SuperClaude-Org |
| K3 | MET | drift labels |
| K4 | MET | no self-contradiction |
| K5 | MET | R2-F1 quotes plan:176, test files :56-57, :357 |
| T1 | MET | medium first |
| T2 | MET | same schema |
| T3 | MET | separate sections |
| T4 | MET | INF mapping, plan lines |
| T5 | MET | all eight fields |
| L1 | MET | R2-F2 exit-code statement |
| L2 | MET | eval_runner.py:313 quoted |
| L3 | MET | R2-F2 headline |
| L4 | NOT MET | INF rows, Search A/B undefined |
| L5 | MET | R2-F2 add a raising test |
| R1 | MET | three findings with severity |
| R2 | MET | recommendations |
| R3 | MET | R2-F1 rerun after skip |
| R4 | MET | R2-F1 shallow/root dependencies |
| R5 | MET | R2-F1 rerun artifact |
| E1 | NOT MET | none found |
| E2 | MET | R2-F2 main() vs :313 filter |
| E3 | MET | R2-F2 startswith("local") guard |
| E4 | MET | search counts reproduced |
| E5 | MET | R2-F2 global-setup vs exit logic |

## Variant 3
| criterion | verdict | evidence |
|---|---|---|
| C1 | NOT MET | no per-deviation coverage |
| C2 | MET | R3-F3 failed add, leak, mis-reporting |
| C3 | MET | R3-F7 git init -b master, identity |
| C4 | MET | R3-F2 global-setup assertion; R3-F3 dir gone |
| C5 | NOT MET | scope limit only in Round 2 |
| K1 | NOT MET | R3-F4 scripts half conceded |
| K2 | MET | R3-F3 MasterCheckoutError, rmdir, try/finally around yield |
| K3 | NOT MET | R3-F1 `necessary` (conceded) |
| K4 | MET | no self-contradiction |
| K5 | NOT MET | R3-F7 conjecture; .venv claim withdrawn; R3-F5 premise inferred |
| T1 | MET | medium first |
| T2 | MET | uniform schema |
| T3 | MET | separate sections |
| T4 | MET | file:line locations; disputes cite R3-F1..F3 |
| T5 | MET | all eight fields |
| L1 | MET | R3-F8 replacement grep |
| L2 | MET | R3-F5 names plan lines 119, 148, 178 |
| L3 | MET | R3-F9 headline |
| L4 | NOT MET | none found |
| L5 | MET | R3-F1 registration or monkeypatch.setitem |
| R1 | MET | nine findings with severity |
| R2 | MET | recommendations |
| R3 | MET | R3-F3 rmdir and raise before try/finally |
| R4 | MET | R3-F7 host-dependent config |
| R5 | MET | R3-F2 main() tests; R3-F4 awk+grep check |
| E1 | MET | R3-F2 git worktree list back to one entry |
| E2 | MET | R3-F3 body errors mis-reported |
| E3 | MET | R3-F9 startswith("local") guard |
| E4 | MET | R3-F6 residual misses later files |
| E5 | MET | R3-F4 CLAUDE.md:50 vs plan:117 while plan:113 keeps it |

## Summary
| variant | Completeness | Correctness | Structure | Clarity | Risk | Invariant | Total/30 |
|---|---|---|---|---|---|---|---|
| Variant 1 | 5 | 4 | 5 | 4 | 5 | 4 | 27 |
| Variant 2 | 4 | 4 | 5 | 4 | 5 | 4 | 26 |
| Variant 3 | 3 | 2 | 5 | 4 | 5 | 5 | 24 |
