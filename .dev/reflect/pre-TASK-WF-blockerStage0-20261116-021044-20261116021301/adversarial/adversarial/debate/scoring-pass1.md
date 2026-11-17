# Scoring pass 1 (hybrid): variant 1 then variant 2

- Evaluator: independent scorer, pass 1. Order: V1 first, then V2.
- D = `.dev/reflect/pre-TASK-WF-blockerStage0-20261116-021044-20261116021301/adversarial/adversarial/`; PLAN = `.dev/tasks/to-do/TASK-WF-blockerStage0-20261116-021044/TASK-WF-blockerStage0-20261116-021044.md`; PF = `.dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115`.
- Source requirements for the quantitative metrics: C-001..C-005 and X-001 (6 points).

## 1. Quantitative metrics

Citation check: every PLAN line and every live file line cited by either card was re-read on 2026-11-16 (evaluate.py:110, results.md:54 and 83-89, merged-requirements.md:572/609/944/947/974/985-986/195, pragmatic.md:221/231, source.md:13, stage-requests/README.md:13-21/27-29/32, merged-review-card.md:70, QA folder holds 139 files, gate5-cycle-control.md exists).

| Metric | V1 | V2 | Arithmetic |
|---|---|---|---|
| RC (covered / 6, w .30) | 0.500 | 0.667 | V1 covers C-001 (F1), C-004 (Checked: fallback explicit, PLAN:104), X-001 (NEEDS-REVISION, sustained) = 3/6. V2 covers C-002 (F1), C-003 (F2), C-004 (F3a), C-005 (F3b) = 4/6; its X-001 position (PASS-with-notes) is not "correct": V2's own advocate conceded it (round1-advocate-2.md:9), so it is not counted. |
| IC (1 - bad/total, w .25) | 0.889 | 0.714 | V1: 9 claims, 1 overstated (deletes "Task 9's evidence pointer": the path survives, only content goes; round1-advocate-1.md:26) = 1 - 1/9. V2: 14 claims, 4 false or overstated = 1 - 4/14: (i) the PASS verdict, (ii) F2 "a choice nobody recorded" (PLAN:46 requires a reproducible script; round2-advocate-1.md:6), (iii) F3a "cannot hold that many" (retracted, round2-advocate-2.md:7), (iv) Checked "Only Task 9 edits a file outside `./artifacts/`" (false: the Task 3 rerun overwrites PF `08-test/results.md`, PLAN:52, evaluate.py:110). |
| SR (concrete / (concrete + vague), w .15) | 1.000 | 0.923 | V1: 8 statements, 8 concrete. V2: 13 statements, 12 concrete; the vague one is the sweeping verdict clause "every change the request lists has its text in a task". |
| DC (resolved / total refs, w .15) | 1.000 | 1.000 | V1: 8/8 (PLAN:52, :21, :104; evaluate.py:110; results.md:54, 83-89; spec 572, 609). V2: 20/20 (plan :17-26, :42, :45-48, :77, :90, :100, :123; source.md:13; README:13-21, :27-29, :32; spec 572, 609, 944, 946-947, 974, 985-986, 195-207; pragmatic.md:221, :231; card:70; gate5 file). |
| SC (sections / max, w .15) | 1.000 | 1.000 | Both: Verdict, Findings, Checked, Self-report = 4/4. |
| **quant** | **0.822** | **0.817** | V1: .30(.500)+.25(.889)+.15(1)+.15(1)+.15(1) = .1500+.2222+.1500+.1500+.1500 = 0.8222. V2: .30(.667)+.25(.714)+.15(.923)+.15+.15 = .2000+.1786+.1385+.1500+.1500 = 0.8170. |

Sensitivity: if V2's wrong X-001 verdict were counted as covered, RC(V2) = 5/6 and quant(V2) = 0.867. I did not use that reading, because RC counts a point only when the variant reports it or correctly states its position.

Note: diff-analysis.md:22 says V2's Checked bullets record that Task 3's figures were not re-derived. The V2 card text (variant-2-original.md:17-21) has no such bullet. I scored the card text.

## 2. Qualitative: 30 binary criteria (CEV)

MET = 1, NOT MET = 0. Evidence is quoted or cited as file:line (V1 = variant-1-original.md, V2 = variant-2-original.md).

| Criterion | V1 verdict + evidence | V2 verdict + evidence |
|---|---|---|
| **Completeness** | | |
| C1 all explicit brief requirements | NOT MET: no dropped-constraint, Task 2 frame or Task 10 check (C-002, C-003 absent) | NOT MET: misses the Task 3 overwrite; neither card reports Task 10's missing acceptance lines (diff-analysis.md:60) |
| C2 edge cases / failure scenarios | MET: V1:11 rerun "unconditionally replaces the existing results file" | MET: V2:15 "every gating class will almost certainly fall back to an advisory pass line"; "pools them the same findings are counted twice" |
| C3 dependencies / prerequisites | MET: V1:11 results.md needed for "Task 3's source citations and Task 9's evidence pointer" | MET: V2:15 "Tasks 5 and 6 both include the Task 2 sample" |
| C4 pass/fail criteria for findings | MET: V1:11 "severity MAJOR, blocking true, category data-loss", plus the PLAN:21 constraint as the test | MET: V2:11 "blocking false ... nothing goes wrong as a result" (a reason per finding) |
| C5 states what was not checked | NOT MET: V1:17-19 lists only what was checked | NOT MET: V2:7 "every live path I checked exists"; no unchecked list |
| **Correctness** | | |
| K1 no factual errors | NOT MET: "Task 9's evidence pointer" deleted is overstated (round1-advocate-1.md:26) | NOT MET: V2:21 "Only Task 9 edits a file outside `./artifacts/`" is false given PLAN:52 + evaluate.py:110; PASS conceded wrong (round1-advocate-2.md:9) |
| K2 technical claims feasible | MET: evaluate.py:110 `(HERE / "results.md").write_text(...)` confirmed on disk | MET: Wilson figures 73 (p .95) to 138 (p .90) confirmed (round1-advocate-1.md:21); V2:15 "[computed]" |
| K3 terminology consistent | MET: PLAN / PF used throughout, defined at V1:5 | MET: "plan :n" = PLAN, defined at V2:5 |
| K4 no internal contradictions | MET: NEEDS-REVISION with "blocking true" (V1:8, :11) | MET: "none blocking" matches F1 MINOR, F2 MAJOR with blocking false, F3 MINOR (V2:7-15) |
| K5 claims supported by evidence | MET: F1 has 4 citations, all resolve | NOT MET: the headline "no blocking defect" never tests Task 3's command (round1-advocate-1.md:19); refuted by evaluate.py:110 |
| **Structure** | | |
| S1 logical order | MET: Verdict, Findings, Checked, Self-report (V1:7-23) | MET: same order (V2:7-25) |
| S2 consistent hierarchy | MET: four H2 sections, one finding with a citation list | MET: four H2 sections, three findings in one format |
| S3 separation of concerns | MET: findings (V1:10-15) apart from checked (V1:17-19) | MET: findings (V2:10-15) apart from checked (V2:17-21) |
| S4 navigation aids | MET: finding id `F1`, severity, blocking and category fields (V1:11) | MET: ids `F1` to `F3` and the same fields (V2:11, :13, :15) |
| S5 follows required card format | MET: fields id, severity, blocking, category, text, citations (V1:11) | MET: same fields and section headings (V2:11) |
| **Clarity** | | |
| L1 unambiguous | MET: single finding, one reading (V1:11) | MET: each statement has one reading; F2 uses the plan's own wording "appears uncorrected" (V2:13) |
| L2 concrete | MET: names files, lines and the exact command (V1:12-15) | MET: names files, lines, counts (V2:13 "139 files") |
| L3 each finding summarisable in one sentence | MET: "Task 3 reruns a script that overwrites its own evidence" | NOT MET: F3 bundles two unrelated gaps, (a) recall sizing and (b) double counting (V2:15), under one MINOR label; the debate graded them differently (minor vs Medium, round2-advocate-1.md:6-7) |
| L4 terms defined | MET: PLAN, PF defined (V1:5); hand-added sections named by the quoted heading (V1:14) | NOT MET: "frame", "gating class", "Wilson half-width" used undefined; only PLAN defined (V2:5) |
| L5 actionable next steps | NOT MET: no fix in the card (V1:11); the fix exists only in round2-advocate-1.md:10 | NOT MET: no fix for F1, F2 or F3 (V2:11-15) |
| **Risk coverage** | | |
| R1 at least 3 risks with impact | NOT MET: one finding (V1:11) | MET: three findings with impacts (V2:11 "nothing goes wrong", V2:13 estimate rests on an unrecorded choice, V2:15 advisory fallback / double count) |
| R2 fix per risk | NOT MET: none in the card | NOT MET: none in the card |
| R3 failure modes and recovery | NOT MET: data loss named, no recovery path (git recovery is only in round1-advocate-1.md:8) | NOT MET: no recovery stated |
| R4 external dependencies | MET: depends on PF `08-test/evaluate.py` and `results.md` (V1:13-14) | MET: global CLAUDE.md rule (V2:11), run-2 QA folder (V2:13), request `source.md:13` |
| R5 validation mechanism | NOT MET: no acceptance line or check proposed (no hash, no diff line) | NOT MET: none proposed |
| **Invariant and edge-case coverage** | | |
| I1 collection boundaries | NOT MET: no set or population boundary examined | MET: V2:13 "139 files in mixed formats" de-duplication frame; V2:15 n per gating class |
| I2 state interactions across components | MET: V1:11 evaluate.py write vs results.md vs Task 3 and Task 9 | MET: V2:15 Task 5 and Task 6 share the Task 2 sample; README:32 has stage 2 read both |
| I3 guard-condition gaps | MET: V1:11 "unconditionally replaces ... rather than checking it" | MET: V2:13 "no acceptance line requires that choice to be written down"; V2:11 dropped constraint |
| I4 count divergence | NOT MET: no count compared | MET: V2:20 "Task 6's card holds 17 findings (F1 to F17)" checked against the card (card:70 confirms) |
| I5 interaction effects | MET: V1:11 PLAN:52 command vs PLAN:21 constraint | MET: V2:15 pooled sets counted twice in stage 2 |

### Subtotals

| Dimension | V1 | V2 |
|---|---|---|
| Completeness | 3/5 | 3/5 |
| Correctness | 4/5 | 3/5 |
| Structure | 5/5 | 5/5 |
| Clarity | 4/5 | 2/5 |
| Risk coverage | 1/5 | 2/5 |
| Invariant and edge-case | 3/5 | 5/5 |
| **Total** | **20/30 = 0.667** | **20/30 = 0.667** |

Floor on invariant and edge-case coverage (under 1/5 is ineligible as base): V1 3/5 and V2 5/5 both pass. Both are eligible.

## 3. Combined

combined = 0.5 quant + 0.5 qual

- V1: 0.5(0.8222) + 0.5(0.6667) = 0.4111 + 0.3333 = **0.744**
- V2: 0.5(0.8170) + 0.5(0.6667) = 0.4085 + 0.3333 = **0.742**

The margin (0.002) is smaller than the effect of one judgement call: counting V2's X-001 verdict as covered moves V2 to 0.767.

## 4. Points won and correctness count

Final per-point winners (round 2 where stated, else round 1):

| Point | Winner |
|---|---|
| X-001 | V1 (both advocates) |
| C-001 | V1 (both) |
| A-002 | V1 (both) |
| C-002 | V2 (both) |
| C-003 | V2 (both) |
| C-005 | V2 (both) |
| S-001 | tie (advocate 1: V2; advocate 2: both) |
| C-004 | tie (advocate 1: V1 on the grade, V2's arithmetic right; advocate 2: both) |
| A-001 | tie (both) |

Points won: V1 = 3 (X-001, C-001, A-002), V2 = 3 (C-002, C-003, C-005), ties = 3 (S-001, C-004, A-001); 9 points in all.

Correctness count (claims not false or overstated): V1 8 of 9; V2 10 of 14. CEV Correctness criteria met: V1 4 of 5; V2 3 of 5.

