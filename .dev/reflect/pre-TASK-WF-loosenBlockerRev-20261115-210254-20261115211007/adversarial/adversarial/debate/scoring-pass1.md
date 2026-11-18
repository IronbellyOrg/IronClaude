# Scoring pass 1 (order V1, V2)

Evaluator: independent step-3 scorer, hybrid (quantitative + qualitative). Order of evaluation: Variant 1, then Variant 2.

PLAN = `.dev/tasks/to-do/TASK-WF-loosenBlockerRev-20261115-210254/TASK-WF-loosenBlockerRev-20261115-210254.md`. V1 = variant-1-original.md, V2 = variant-2-original.md.

Live-file verification done for this pass: every PLAN line cited by either card was re-read and resolves (V1: 87, 93, 199, 203, 303, 319, 322, 328, 342, 364, 368, 370, 477, 482, 490, 493, 494, 546, 549; V2: 20, 139, 164, 170, 199, 303, 376, 394, 401, 455, 477, 482, 546). Also re-read: `agent_template_analysis.md:466`, `spec-panel.md:220`, `sc-implement-protocol/SKILL.md:46,56,72,87`, `merged-requirements.md:918,920,947`, `source.md:22,41,43,47`, `refs/qa.md:52`. One citation resolves but is misapplied: V2 F1 quotes SKILL.md:72 "Do not STOP. Do not split." as a phase-gate rule, but that line is the N>=20 compaction notice.

## 1. Debate outcomes (advocates' final per-point winners)

Final = Round 2 line where one exists, else Round 1 (both advocates agreeing, or the later line).

| Point | R1 adv-1 | R1 adv-2 | R2 adv-1 | R2 adv-2 | Final winner |
|---|---|---|---|---|---|
| S-001 | V2 | both | - | - | split (V2 / both): not counted |
| C-001 | both | both | - | - | both |
| C-002 | both | both | - | - | both |
| C-003 | V1 | V1 | - | - | V1 |
| C-004 | V1 | V1 | V1 (Medium) | V1 (blocking) | V1 (grade disputed) |
| C-005 | V2 | V2 | V2 | V2 | V2 |
| C-006 | V2 | V2 | V2 | V2 | V2 |
| C-007 | V2 | neither | neither | neither | neither |
| C-008 | V2 | V2 | - | - | V2 |
| C-009 | neither | V2 | V2 | V2 | V2 |
| A-001 | both | neither | both | both | both |
| A-002 | both | both | - | - | both |

Points won: V1 = 2 (C-003, C-004); V2 = 4 (C-005, C-006, C-008, C-009); both = 4 (C-001, C-002, A-001, A-002); neither = 1 (C-007); S-001 split.

## 2. Quantitative metrics

Source requirements = the 9 content points C-001..C-009. A variant covers a point if it reports it.

Coverage per point: V1 reports C-001 (F1), C-002 (F4), C-003 (F2), C-004 (F3). V2 reports C-001 (F3 second half), C-002 (F5), C-005 (F1), C-006 (F2), C-007 (F3 first half), C-008 (F4), C-009 (F6).

| Metric | V1 | V2 |
|---|---|---|
| RC = covered / 9 (w .30) | 4/9 = 0.444 | 7/9 = 0.778 |
| Claims counted (findings + Checked bullets) | 4 + 4 = 8 | 6 + 7 = 13 |
| Overstated or false claims | 1.5 (see below) | 2.5 (see below) |
| IC = 1 - overstated/total (w .25) | 1 - 1.5/8 = 0.8125 | 1 - 2.5/13 = 0.8077 |
| SR = concrete / (concrete + vague) (w .15) | 12/(12+2) = 0.857 | 18/(18+1) = 0.947 |
| DC = resolved refs / total refs (w .15) | 22/22 = 1.000 | 25/25 = 1.000 |
| SC = sections / max sections (w .15) | 4/4 = 1.000 | 4/4 = 1.000 |
| **quant** | **0.765** | **0.877** |

Arithmetic: V1 quant = .30(0.4444) + .25(0.8125) + .15(0.8571) + .15(1) + .15(1) = 0.1333 + 0.2031 + 0.1286 + 0.15 + 0.15 = 0.7650. V2 quant = .30(0.7778) + .25(0.8077) + .15(0.9474) + .15 + .15 = 0.2333 + 0.2019 + 0.1421 + 0.15 + 0.15 = 0.8774.

IC evidence (concessions in the debate; a contested item counts 0.5, a conceded or verified flaw counts 1):
- V1 F2 "contradicts the required count of exactly 11": overstated (round1-advocate-1 concession 3: the count is only Task 16's own acceptance line, no later test pins it). 1.0.
- V1 F3 blocking grade: round2-advocate-1 lowers it to Medium, round2-advocate-2 holds blocking; invariant-probe INV-006 favours blocking. Contested. 0.5.
- V2 F1: quote of SKILL.md:72 misapplied (verified above; invariant-probe INV-017; round1-advocate-1 weakness 4). The "run straight through, no owner go" claim was also conceded as overstated by advocate-2 (round1 concession 1, round2 "drop inevitable bypass") though invariant-probe INV-020 backs the core. 1.0.
- V2 F3 first half "unpassable": conceded as avoidable by a path-only list (round1-advocate-2 concession 2; both advocates grade C-007 neither/minor in round 2). 1.0.
- V2 F6 "maps ... to task 0": imprecise per round1-advocate-2 concession 4, but round2-advocate-1 verified `best_task: 0` on exactly those ids. 0.5.
- No other claim in either card was refuted in the debate or by my re-reads.

SR evidence: V1 vague = F1 "the plan must specify how that entry is staged" (no concrete staging) and the self-report line; V2 vague = self-report line only (F1, F2 state defects and give no fix, which I do not count as vague statements). Concrete = findings, fixes that name an action, Checked bullets with citations, verdict.

DC: V1 22 refs (F1 3, F2 6, F3 5, F4 2, Checked 6); V2 25 findings-level refs (F1 6, F2 4, F3 6, F4 4, F5 1, F6 4). All resolve to the quoted text on live files; V2's SKILL.md:72 resolves but is misapplied (scored under IC, not DC).

## 3. Qualitative CEV table (30 binary criteria)

| # | Criterion | V1 verdict + evidence | V2 verdict + evidence |
|---|---|---|---|
| Comp-1 | Covers all explicit requirements of the review brief | NOT MET: no coverage-matrix or request-coverage check anywhere in the card (lines 7-26); misses owner gates and spec items | MET: audits request coverage and the matrix: line 27 "Every change the request lists has a task", F6 matrix omissions (reviewer-2.md:21 requires the matrix audit) |
| Comp-2 | Edge cases / failure scenarios | MET: F1 line 13 "rejects missing allow-listed files, but that mirror is created only in Phase 5" | MET: F1 line 13 "fails with `E-PLAN-CHANGED` if the plan is changed after the first task starts" |
| Comp-3 | Dependencies / prerequisites | MET: F1 line 13 mirror "created only in Phase 5"; F3 "no stage 2 task consumes that population" | MET: F2 line 15 "Task 31 is the first task inside Phase 4 ... Task 33 depends on Task 31 being finished" |
| Comp-4 | Pass/fail criteria for findings | MET: "blocking true" vs "blocking false"; F4 line 19 "Mechanical sequencing with clear intent" | MET: "blocking true/false"; F5 line 21 "The fix is mechanical" |
| Comp-5 | States what was not checked | MET: line 26 "No files changed; no commands or tests run. Described failures follow from written requirements, not observed execution." | NOT MET: Checked (lines 27-35) lists what held; no statement of what was not checked or not run |
| Corr-1 | No factual errors | NOT MET: F2 "contradicts the required count of exactly 11" (line 15) conceded overstated | NOT MET: F1 line 13 quotes "Do not STOP. Do not split." (SKILL.md:72, the N>=20 compaction notice) as a phase rule |
| Corr-2 | Technical claims feasible | MET: F2/F3 failure paths verified on PLAN:199/203/303/490/494 and 87/93 | MET: F1 verified on SKILL.md:56 and :87 (no phase option; Phase is a group heading) |
| Corr-3 | Terminology consistent | MET: "digest", "registry row", "reverse scan" used uniformly | MET: "owner gate", "pointer-only", "seeded-recall" used uniformly |
| Corr-4 | No internal contradictions | MET: no finding opposes another; line 26 disclaimer matches findings | MET: line 27 "Every change ... has a task" is reconciled with F6 ("matrix-quality issue only") |
| Corr-5 | Claims supported by evidence | MET: every finding carries re-verified PLAN citations | MET: every finding carries re-verified PLAN/SKILL/spec citations |
| Str-1 | Logical order | MET: Verdict, Findings (MAJOR then MINOR), Checked, Self-report | MET: same order; MAJOR F1-F4 then MINOR F5-F6 |
| Str-2 | Consistent hierarchy | MET: uniform `F# | severity | blocking | category | text | citations` rows | MET: same row shape for all six |
| Str-3 | Separation of concerns | MET: findings vs Checked vs self-report | MET: same |
| Str-4 | Navigation aids | MET: F1-F4 ids, severity and blocking flags | MET: F1-F6 ids plus "Who:" / "Wrong result:" lead-ins |
| Str-5 | Follows required card format | MET: persona/model header, Verdict, Findings, Checked, Self-report | MET: same sections and header |
| Cla-1 | Unambiguous | MET: each finding states one defect and cause (lines 13-19) | NOT MET: F3 line 17 bundles two defects (scale-map self-trip and plugin-mirror existence check), so a fixer can close one and leave the other |
| Cla-2 | Concrete | MET: line-cited quotes, e.g. line 15 "PLAN:490 ... Each gets the digest and pointer" | MET: line 19 names Task 25, `commands/spec-panel.md` line 220 |
| Cla-3 | Each finding summarisable in one sentence | MET: all four reduce to one sentence | NOT MET: F3 (line 17) is a two-defect paragraph; F1/F4 span several sentences |
| Cla-4 | Terms defined | NOT MET: "reverse scan", "digest", "registry" used without gloss (line 15) | MET: line 13 explains `E-PLAN-CHANGED` and "one phase at a time"; line 19 "T3 fails when a carrier contains `src/superclaude`" |
| Cla-5 | Actionable next steps | MET: F4 line 19 "edit the registry before copying, or repeat the copy afterward"; F2 "plan must choose whether ..." | MET: F4 line 19 "exempt pointer-only rows ... or edit spec-panel line 220"; F5 "add the row first, or copy again" |
| Risk-1 | At least 3 risks with impact | MET: F1 "cannot pass", F2 "fails the reverse scan", F3 "without evaluating the classifier" | MET: F1 Phase 4 switches live carriers with no owner go; F2 pragmatic.md moves to v2 without recall; F3, F4 failing checks |
| Risk-2 | Fix / mitigation per risk | NOT MET: F3 (line 17) gives no fix | NOT MET: F1 (line 13) and F2 (line 15) give no fix |
| Risk-3 | Failure modes and recovery | MET: F4 line 19 recovery; F1 "stage ... without weakening the missing-file check" | MET: F4 line 19 and F5 line 21 give recovery options |
| Risk-4 | External dependencies | NOT MET: all findings are internal to the plan; no external tool or protocol dependency is analysed | MET: F1 line 13 depends on `/sc:implement` behaviour (SKILL.md:46, :56, :87) |
| Risk-5 | Validation mechanism | MET: line 19 "plugin-parity test must pass" (PLAN:549) | MET: line 21 "the new T15 parity test fails until the folder is copied again"; F1 "No task has an acceptance line that requires a recorded owner go" |
| Inv-1 | Collection boundaries | MET: F2 line 15 "exactly 11 rows of kind `digest`" vs five template files | MET: F3 line 17 "That file sits under `src/superclaude/skills`, which the Task 40 scan covers" |
| Inv-2 | State interactions across components | MET: F1 allow-list (Task 40) vs mirror (Task 46) | MET: F3 Task 13 / Task 40 / Task 46 |
| Inv-3 | Guard-condition gaps | MET: F1 line 13 "rejects missing allow-listed files" guard vs a not-yet-existing file | MET: F2 line 15 entry condition is the first task inside the phase it gates |
| Inv-4 | Count divergence | MET: F2 line 15 11 digest rows (PLAN:203) vs five templates (PLAN:490) | NOT MET: line 32 "Exactly 11 files hold the definition sentence" checks the count but misses the 11-vs-5 divergence (invariant-probe INV-009, INV-012) |
| Inv-5 | Interaction effects | MET: F4 line 19 registry edit after copy breaks the parity check | MET: F3 line 17 "the scan fails after Task 46 copies `rule.md` and `scale-map.md` into the plugin" |

## 4. Subtotals

| Dimension | V1 | V2 |
|---|---|---|
| Completeness (5) | 4 | 4 |
| Correctness (5) | 4 | 4 |
| Structure (5) | 5 | 5 |
| Clarity (5) | 4 | 3 |
| Risk coverage (5) | 3 | 4 |
| Invariant and edge-case coverage (5) | 5 | 4 |
| **qual = MET / 30** | **25/30 = 0.833** | **24/30 = 0.800** |
| Correctness criteria MET | 4 of 5 | 4 of 5 |

Floor rule (last dimension under 1/5 is ineligible as base): V1 5/5, V2 4/5. Both eligible.

## 5. Combined

| | V1 | V2 |
|---|---|---|
| quant | 0.765 | 0.877 |
| qual | 0.833 | 0.800 |
| **combined = .5 quant + .5 qual** | **0.799** (.5 x 0.7650 + .5 x 0.8333) | **0.839** (.5 x 0.8774 + .5 x 0.8000) |

Reading: V2 leads on requirement coverage (7 vs 4 of 9 points, 4 vs 2 debate wins, including the two highest-severity items C-005 and C-006). V1 leads slightly on card clarity (single-defect findings) and count-divergence coverage (C-003). The qualitative scores are close; the quant gap is driven by RC.

