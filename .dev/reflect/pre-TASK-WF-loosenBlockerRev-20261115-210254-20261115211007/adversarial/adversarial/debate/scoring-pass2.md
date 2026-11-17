# Scoring pass 2 (evaluation order: Variant 2, then Variant 1)

Variant 1 = reviewer-1 card (analyzer, haiku class). Variant 2 = reviewer-2 card (qa, opus class).
PLAN = .dev/tasks/to-do/TASK-WF-loosenBlockerRev-20261115-210254/TASK-WF-loosenBlockerRev-20261115-210254.md (552 lines).
Live checks done: every PLAN line cited by either card exists and holds the quoted text (spot-checked about 35 of V2's 59 refs and all of V1's 22; the rest cross-confirmed by invariant-probe INV-009, INV-012, INV-013). Brief format read from reviewer-briefs/reviewer-1.md:140-148.

## 1. Quantitative metrics

Source requirements = the 9 content points C-001..C-009 (covered = the card reports the point).

| Metric | V2 | V1 |
|---|---|---|
| RC (covered / 9) | C-001, C-002, C-005, C-006, C-007, C-008, C-009 = 7/9 = 0.778 | C-001, C-002, C-003, C-004 = 4/9 = 0.444 |
| Claims counted (findings + asserting Checked bullets) | 6 findings + 9 Checked = 15 | 4 findings + 3 asserting Checked bullets (disclaimer bullet excluded) = 7 |
| Overstated or false (debate concessions) | 1.5 (F3 first half "unpassable": both advocates agree "neither/minor", round1-advocate-2 concession 2, round2-advocate-1:7; F1 "bypass" overstated per round1-advocate-2 concession 1 plus the misapplied SKILL.md:72 quote, round1-advocate-1 weakness 4 and INV-017, but contested in round 2 and INV-020 backs the blocking grade, so 0.5) | 1.5 (F2 "contradicts the required count of exactly 11": conceded, round1-advocate-1 concession 3 = 1.0; F3 blocking grade: its own advocate dropped it to Medium in round 2, but round2-advocate-2:7 and INV-006 hold blocking, so 0.5) |
| IC = 1 - flawed/total | 1 - 1.5/15 = 0.900 | 1 - 1.5/7 = 0.786 |
| SR concrete / (concrete + vague) | concrete 18 (6 wrong-result statements, 3 fixes with named alternatives in F3, F4, F5, 9 Checked bullets), vague 0 = 18/18 = 1.000 | concrete 10 (4 wrong-result, fixes in F2 and F4, 4 Checked bullets incl. the disclaimer), vague 1 (F1 fix: "must specify how that entry is staged", no alternative named) = 10/11 = 0.909 |
| DC resolved refs / total refs | 59/59 = 1.000 (F1 6, F2 4, F3 6, F4 4, F5 1, F6 6, Checked 32; the SKILL.md:72 line exists and holds the quoted text, its misapplication is scored in IC) | 22/22 = 1.000 (F1 3, F2 6, F3 5, F4 2, Checked 6) |
| SC sections / max sections | 4/4 = 1.000 (Verdict, Findings, Checked, Self-report) | 4/4 = 1.000 |

quant = 0.30 RC + 0.25 IC + 0.15 SR + 0.15 DC + 0.15 SC

- V2: 0.30(0.778) + 0.25(0.900) + 0.15(1.000) + 0.15(1.000) + 0.15(1.000) = 0.2333 + 0.2250 + 0.4500 = **0.908**
- V1: 0.30(0.444) + 0.25(0.786) + 0.15(0.909) + 0.15(1.000) + 0.15(1.000) = 0.1333 + 0.1964 + 0.1364 + 0.3000 = **0.766**

## 2. Qualitative CEV (30 binary criteria)

Completeness (C), Correctness (Q), Structure (S), Clarity (L), Risk (R), Invariant and edge-case (I).

| Criterion | V2 verdict + evidence | V1 verdict + evidence |
|---|---|---|
| C1 covers all explicit brief requirements | MET. Four required sections (V2:7-40); qa-persona coverage-matrix audit is F6 (V2:23); owner gates, not-built list, classifier limits in Checked (V2:27, :34, :35) | NOT MET. The analyzer persona must test the T1 card's self-trip and gate-risk observations (reviewer-1.md:21); V1:13-26 has no finding or Checked bullet on either |
| C2 edge cases / failure scenarios | MET. F2: "`pragmatic.md` moves to digest v2 in the same run even when safety recall falls below the old rule's" (V2:15) | MET. F2: "Leaving it unregistered fails the reverse scan" (V1:15) |
| C3 dependencies / prerequisites | MET. F1 "Task 11 ... Depends on: Task 10 only" (V2:13); F3 "mirror is created only in Task 46" (V2:17) | MET. F1 "that mirror is created only in Phase 5" (V1:13) |
| C4 pass/fail criteria for findings | MET. "blocking true/false" per finding and F5 reason "The fix is mechanical" (V2:21) | MET. "blocking false" with F4 "Mechanical sequencing with clear intent" (V1:19) |
| C5 states what was not checked | NOT MET. No Checked bullet or note says what was skipped (V2:25-35) | MET. "No files changed; no commands or tests run. Described failures follow from written requirements, not observed execution." (V1:26) |
| Q1 no factual errors | NOT MET. F3 "unpassable" overstated (round2-advocate-1:7); "Do not STOP. Do not split." misapplied to gates (INV-017; SKILL.md:72 is the N>=20 notice) | NOT MET. F2 "contradicts the required count of exactly 11" conceded as overstated (round1-advocate-1 concession 3) |
| Q2 technical claims feasible | MET. SKILL.md:46, :56, :87 confirm no phase option and `E-PLAN-CHANGED` (live read) | MET. PLAN:490 "Each gets the digest and pointer" with PLAN:199 lacking the analysis row (live read, 0 matches) |
| Q3 terminology consistent | MET. "pointer-only", "digest", "carrier" used one way throughout | MET. "digest", "registry row", "mirror" used one way |
| Q4 no internal contradictions | MET. No finding opposes another; Checked "Every change the request lists has a task" (V2:27) is compatible with F6 "matrix-quality issue only" | MET. Checked PLAN:328/:342 agrees with F3's use of PLAN:328 |
| Q5 claims supported by evidence | MET. Every finding carries 1-6 quoted refs; DC 59/59 | MET. Every finding carries quoted refs; DC 22/22 |
| S1 logical order | MET. Verdict, Findings (MAJOR then MINOR), Checked, Self-report | MET. Same order |
| S2 consistent hierarchy | MET. "F<n> \| sev \| blocking \| category \| prose \| citations" on all six | MET. Same shape on all four |
| S3 separation of concerns | NOT MET. F3 bundles two defects (scale-map self-trip and missing plugin mirror) with two fix paths (round1-advocate-1 weakness 1) | MET. F1 to F4 each hold one cause |
| S4 navigation aids | MET. F-ids and "Who:" / "Wrong result:" labels (V2:13-23) | MET. F-ids and a citations field on each finding (V1:13-19) |
| S5 follows required card format | NOT MET. Brief says Checked "(file:line each)" (reviewer-1.md:146); V2:35 "The not-built list holds. No task edits `sc-implement-protocol/refs/qa.md` ..." has no line numbers | MET. Four sections, allowed categories, 1-6 citations; Checked bullets carry PLAN lines (V1:23-25), the last is a disclaimer |
| L1 unambiguous | MET. Each finding names Who and Wrong result | MET. Each finding names the executor and the wrong result |
| L2 concrete | MET. Task numbers and quoted lines throughout | MET. Same |
| L3 each finding one-sentence summarisable | NOT MET. F3 has two unrelated defects and a two-way fix choice (V2:17) | MET. e.g. F3 "no stage 2 task consumes that population" (V1:17) |
| L4 terms defined | MET. Inline: "`E-PLAN-CHANGED` if the plan is changed after the first task starts" (V2:13); "T3 fails when a carrier contains `src/superclaude`" (V2:19) | NOT MET. "digest", "carrier registry", "reverse scan", "fence opener" used without a gloss (V1:15) |
| L5 actionable next steps | MET. F4 "exempt pointer-only rows from the path check, or edit spec-panel line 220" (V2:19) | MET. F4 "edit the registry before copying, or repeat the copy afterward" (V1:19) |
| R1 at least 3 risks with impact | MET. Six findings, each with a "Wrong result" | MET. Three blocking plus one minor, with the verdict sentence on impact (V1:9) |
| R2 fix or mitigation per risk | NOT MET. F1, F2 and F6 give no fix (V2:13, :15, :23) | NOT MET. F3 gives no fix and F1's fix is only "must specify how" (V1:13, :17) |
| R3 failure modes and recovery | MET. F1 "fails with `E-PLAN-CHANGED`"; F5 "fails until the folder is copied again" (V2:13, :21) | MET. F4 "differ immediately before their parity check ... or repeat the copy afterward" (V1:19) |
| R4 external dependencies | MET. Depends on the `/sc:implement` protocol and the merged spec (SKILL.md:56; merged-requirements.md:947) | NOT MET. Reasons only inside the plan and one template file; no executor or spec dependency named |
| R5 validation mechanism | MET. Checked states live-file verification of anchors (V2:33 "Code and test anchors exist") | MET. States method and limit (V1:26) |
| I1 collection boundaries | MET. F3: scan "covers case-insensitively" `src/superclaude/skills`, allow-list omits the file (V2:17) | MET. F1/F2: allow-list and 11-row registry boundaries (V1:13, :15) |
| I2 state interactions across components | MET. F1 `/sc:implement` versus plan gates (V2:13) | MET. F2 template versus registry versus reverse scan (V1:15) |
| I3 guard-condition gaps | MET. F2 entry condition sits inside the phase it guards; Task 33 depends on Task 31 finishing, not passing (V2:15) | NOT MET. No gate or entry guard gap reported; F1's missing-file guard is not itself a gap |
| I4 count divergence | MET. F6 "maps INF-008, INF-022, INF-027 and INF-028 to task 0"; Checked "Exactly 11 files hold the definition sentence" (V2:23, :32) | MET. F2 "contradicts the required count of exactly 11" (V1:15), the count claim is overstated but the divergence is real (INV-009) |
| I5 interaction effects | MET. F3: leaving the mirror off "fails after Task 46 copies `rule.md` and `scale-map.md` into the plugin" (V2:17) | MET. F1: stage the entry "without weakening the missing-file check" (V1:13) |

Floor rule: V2 5/5 and V1 4/5 on the last dimension, both above 1/5, both eligible as base.

### Subtotals

| Dimension | V2 | V1 |
|---|---|---|
| Completeness | 4/5 | 4/5 |
| Correctness | 4/5 | 4/5 |
| Structure | 3/5 | 5/5 |
| Clarity | 4/5 | 4/5 |
| Risk coverage | 4/5 | 3/5 |
| Invariant / edge-case | 5/5 | 4/5 |
| **qual total** | **24/30 = 0.800** | **24/30 = 0.800** |

Correctness-criteria count: V2 4/5, V1 4/5.

## 3. Combined score

combined = 0.5 quant + 0.5 qual

| | quant | qual | combined |
|---|---|---|---|
| V2 | 0.908 | 0.800 | **0.854** (0.4542 + 0.4000) |
| V1 | 0.766 | 0.800 | **0.783** (0.3831 + 0.4000) |

## 4. Debate points won (advocates' final per-point winners; round 2 where given, else round 1)

| Point | Winner |
|---|---|
| S-001 | split (advocate 1 says V2, advocate 2 says both) |
| C-001 | both |
| C-002 | both |
| C-003 | V1 |
| C-004 | V1 (both advocates agree; grade disputed: Medium per advocate 1, blocking per advocate 2) |
| C-005 | V2 |
| C-006 | V2 |
| C-007 | neither (minor) |
| C-008 | V2 |
| C-009 | V2 (minor) |
| A-001 | both (QUALIFY) |
| A-002 | both (QUALIFY) |

Totals on the nine content points: V2 won 4 (C-005, C-006, C-008, C-009), V1 won 2 (C-003, C-004), shared 2 (C-001, C-002), neither 1 (C-007).

## 5. Notes

- Neither card found the defects in invariant-probe.md that the probe rates HIGH: INV-004 (later tasks falsify earlier acceptance lines, so the final review cannot pass), INV-005 (Phase 4 and 5 entry numbers undefined or unmeasured), INV-006 (the held-out split is never used).
- V2 leads on coverage and unique high-severity points; V1 leads on structure and finding isolation. Qualitative scores tie at 24/30.
