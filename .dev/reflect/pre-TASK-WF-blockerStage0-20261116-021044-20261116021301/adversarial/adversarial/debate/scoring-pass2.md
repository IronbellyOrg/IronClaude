# Scoring pass 2 (hybrid): stage 0 plan review cards

Evaluator order: Variant 2 first, then Variant 1.
V1 = variant-1-original.md (analyzer, haiku class, NEEDS-REVISION). V2 = variant-2-original.md (qa, opus class, PASS-with-notes).
PLAN = .dev/tasks/to-do/TASK-WF-blockerStage0-20261116-021044/TASK-WF-blockerStage0-20261116-021044.md

## 1. Quantitative metrics

Source requirements: C-001, C-002, C-003, C-004, C-005, X-001 (6 points).

| Metric (weight) | V2 | V1 | Arithmetic |
|---|---|---|---|
| RC (.30) | 0.833 | 0.500 | V2 covers C-002, C-003, C-004, C-005, X-001 = 5/6; V1 covers C-001, C-004 (Checked: fallback explicit, PLAN:104), X-001 = 3/6 |
| IC (.25) | 0.750 | 0.889 | V2: 12 claims, 3 false or overstated (PASS verdict; "cannot hold that many", retracted as too categorical in round2-advocate-2.md:7; "Only Task 9 edits a file outside ./artifacts/", false because Task 3's rerun at PLAN:52 overwrites results.md) = 1 - 3/12. V1: 9 claims, 1 overstated ("needed for ... Task 9's evidence pointer", conceded in round1-advocate-1.md:26) = 1 - 1/9 |
| SR (.15) | 0.941 | 1.000 | V2: 16 concrete, 1 vague ("every change the request lists has its text in a task") = 16/17. V1: 7 concrete, 0 vague = 7/7 |
| DC (.15) | 1.000 | 1.000 | V2: 23/23 references resolve; V1: 8/8 resolve (checked below) |
| SC (.15) | 1.000 | 1.000 | Both have 4 sections (Verdict, Findings, Checked, Self-report); max 4 |
| **quant** | **0.879** | **0.822** | V2: .30(.833)+.25(.75)+.15(.941)+.15(1)+.15(1) = .250+.1875+.1412+.15+.15 = 0.8787. V1: .30(.5)+.25(.889)+.15(1)+.15(1)+.15(1) = .150+.2222+.15+.15+.15 = 0.8222 |

DC check, PLAN line numbers (all re-read today): :17-26 Constraints; :21 only-spec-edit rule; :42 Task 2 body; :45-48 Task 2 acceptance; :52 Task 3 rerun sentence; :77 Task 5 body; :90 Task 6 body; :100 Task 7 body; :104 Task 7 advisory line; :123 Task 9 body. Other anchors that resolved: source.md:13 (contains "always staged"; the PLAN has none, grep count 0); `qa/gate5-cycle-control.md` exists, qa folder holds 139 files; spec lines 572, 609, 944, 946-947, 974, 985-986, 195-207; stage-requests/README.md:13-21, :27-29, :32; pragmatic.md:221, :231; merged-review-card.md:70 (inside "## Checked", which names F1 to F17); evaluate.py:110 (`(HERE / "results.md").write_text(...)`); results.md:54 ("Diagnosis (added by hand after the run...)") and :83-89 (kappa and per-kind table).

## 2. Qualitative: 30 binary criteria (MET = 1, NOT MET = 0)

| # | Criterion | V2 | V1 |
|---|---|---|---|
| **Completeness** | | | |
| C1 | Covers all explicit review-brief requirements | MET: checks request-vs-plan ("every change the request lists has its text in a task"), F1 missing-requirement, Task 9/4/6 anchors | NOT MET: one finding, two Checked bullets; misses C-002, C-003, C-005 and Task 10 acceptance gap |
| C2 | Edge cases / failure scenarios | MET: F3(a) recall 0.90-0.95 needs 70-140 defects; F3(b) double count | MET: F1 rerun destroys results.md:54-93 |
| C3 | Dependencies / prerequisites | MET: F3(b) "Tasks 5 and 6 both include the Task 2 sample" | MET: results.md "needed for Task 3's source citations and Task 9's evidence pointer" |
| C4 | Pass/fail criteria for findings | MET: "blocking false" on each finding, with basis (F1 "nothing goes wrong as a result") | MET: "blocking true | data-loss", severity MAJOR with consequence |
| C5 | States what was not checked | NOT MET: no statement of unchecked scope | NOT MET: none |
| **Correctness** | | | |
| K1 | No factual errors | NOT MET: wrong verdict (conceded, round2-advocate-2.md "Concede V1's blocking verdict"); "Only Task 9 edits a file outside ./artifacts/" contradicted by PLAN:52 | MET: every citation re-read true (see DC check) |
| K2 | Technical claims feasible | MET: Wilson arithmetic verified (73 at p .95, 138 at p .90, round1-advocate-1.md:21) | MET: evaluate.py:110 overwrites; no flag (round1-advocate-1.md:4) |
| K3 | Terminology consistent | MET: MINOR/MAJOR plus "blocking false" throughout | MET: "severity MAJOR | blocking true" |
| K4 | No internal contradictions | MET: verdict PASS-with-notes agrees with "none blocking" | MET: NEEDS-REVISION agrees with one blocking finding |
| K5 | Claims supported by evidence | MET: each finding has plan/file citations; F3 marks "[computed]" | MET: four citations on F1, two on Checked |
| **Structure** | | | |
| S1 | Logical order | MET: Verdict, Findings, Checked, Self-report | MET: same order |
| S2 | Consistent hierarchy | MET: F1-F3, F3 split (a)/(b) | MET: F1 with citation sub-list |
| S3 | Separation of concerns | NOT MET: F3 joins two unrelated gaps ((a) Task 7 sizing, (b) Tasks 5/6 overlap) | MET: one concern per finding |
| S4 | Navigation aids | MET: finding ids F1-F3, severity/blocking columns | MET: F1 id, labelled "citations:" list |
| S5 | Follows required card format | MET: persona/model header, Verdict, F-lines, Checked, Self-report with confidence | MET: same sections and header |
| **Clarity** | | | |
| L1 | Unambiguous | MET: each finding states the exact gap | MET: single clear defect |
| L2 | Concrete | MET: "139 files", "70 to 140 planted defects" | MET: "evaluate.py:110", "lines 83-89" |
| L3 | Each finding summarisable in one sentence | NOT MET: F3 needs two sentences (two gaps) | MET: "Task 3's rerun overwrites hand-added results" |
| L4 | Terms defined | MET: header defines PLAN and paths | MET: header defines PLAN and PF |
| L5 | Actionable next steps | NOT MET: no fix stated for F1-F3 | NOT MET: no fix stated (fix came only in debate round 2) |
| **Risk coverage** | | | |
| R1 | At least 3 risks with impact | MET: F1, F2 ("escape estimate depends on a choice nobody recorded"), F3 | NOT MET: one risk |
| R2 | Fix per risk | NOT MET: none | NOT MET: none |
| R3 | Failure modes and recovery | MET: F3(a) names the fallback ("The request allows that fallback") | NOT MET: data loss described, no recovery |
| R4 | External dependencies | MET: global CLAUDE.md binds the executor (F1); stage-requests/README.md:32 (F3) | MET: PF evaluate.py and results.md as Task 3's source |
| R5 | Validation mechanism | MET: F2 "no acceptance line requires that choice to be written down" | NOT MET: none |
| **Invariant and edge-case coverage** | | | |
| I1 | Collection boundaries | MET: "139 files in mixed formats", de-duplication frame (F2) | NOT MET |
| I2 | State interactions across components | MET: F3(b) Task 2 sample reused by Tasks 5 and 6 | MET: results.md written by Task 3, read by Task 9 |
| I3 | Guard-condition gaps | MET: F2 "how the code decides that a flaw appears uncorrected" | MET: "unconditionally replaces the existing results file rather than checking it" |
| I4 | Count divergence | MET: Checked "Task 6's card holds 17 findings (... F1 to F17)" | NOT MET |
| I5 | Interaction effects | MET: F3(b) double counting when stage 2 pools sets | MET: PLAN:52 rerun versus the PLAN:21 constraint |

Floor check (invariant dimension, at least 1/5): V2 5/5, V1 3/5. Both eligible as base.

## 3. Subtotals

| Dimension | V2 | V1 |
|---|---|---|
| Completeness | 4/5 | 3/5 |
| Correctness | 4/5 | 5/5 |
| Structure | 4/5 | 5/5 |
| Clarity | 3/5 | 4/5 |
| Risk coverage | 4/5 | 1/5 |
| Invariant and edge-case | 5/5 | 3/5 |
| **qual total** | **24/30 = 0.800** | **21/30 = 0.700** |

## 4. Points won and correctness count

Advocates' final per-point winners (round 2 where given, else round 1; round 1 A1 and A2 agree except S-001 and C-004):

| Point | Winner |
|---|---|
| C-001 | V1 |
| C-002 | V2 |
| C-003 | V2 |
| C-004 | tie (A1 round 2: V1 on grade only; A2 round 2: both) |
| C-005 | V2 |
| X-001 | V1 |
| S-001 | V2 per advocate 1 (70%), both per advocate 2: tie |
| A-001 | both |
| A-002 | V1 |

Points won: V1 3 (C-001, X-001, A-002); V2 3 (C-002, C-003, C-005); ties 3 (C-004, S-001, A-001). On the six content points: V2 3, V1 2, one tie.
Correctness count: Correctness dimension V1 5/5, V2 4/5. False or overstated claims: V2 3 of 12; V1 1 of 9. The one point that decides the merged verdict (X-001, blocking data loss in Task 3) goes to V1, and V2's PASS is conceded wrong by its own advocate.

## 5. Combined

| Variant | quant | qual | combined (.5 quant + .5 qual) |
|---|---|---|---|
| V2 | 0.879 | 0.800 | 0.839 |
| V1 | 0.822 | 0.700 | 0.761 |

Note for the merge: V2 scores higher on breadth, risk and invariant coverage and on points other than C-001, but its verdict is wrong. V1 holds the only blocking finding. The scores favour V2 as a base only if C-001 and the verdict are carried in from V1.

