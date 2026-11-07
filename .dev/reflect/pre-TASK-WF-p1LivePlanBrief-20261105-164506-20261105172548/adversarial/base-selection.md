# Base Selection Report

Folder F = `.dev/reflect/pre-TASK-WF-p1LivePlanBrief-20261105-164506-20261105172548/adversarial/`. Algorithm: `~/.claude/skills/sc-adversarial-protocol/refs/scoring-protocol.md` (A.1 to A.5); layout: `refs/artifact-templates.md` Section 3.
Variants: V1 = reviewer-1 card (analyzer), V2 = reviewer-2 card (qa), V3 = reviewer-3 card (refactorer); files `variant-N-original.md`.
Inputs: `scoring-pass-1.md` (forward order V1, V2, V3; quantitative + qualitative), `scoring-pass-2.md` (reverse order V3, V2, V1; qualitative only), `diff-analysis.md`, `round1-advocate-1..3.md`, `round2-advocate-1..3.md`.
Verdict codes: M = MET, NM = NOT MET.

## Quantitative Scoring (50% weight)

Taken from pass 1 (`scoring-pass-1.md` sections A.0 to A.6). Requirement list (pass 1 A.0): R1 C-001, R2 C-002, R3 C-003, R4 C-005, R5 C-008, R6 U-003, R7 U-004, R8 grant-swap class, R9 tip-pin class, R10 child-worktree class.

| Metric | Weight | V1 (analyzer) | V2 (qa) | V3 (refactorer) |
|---|---|---|---|---|
| requirement_coverage | 0.30 | 0.800 (8/10; no U-003, U-004) | 0.400 (4/10; no C-001/2/3/5, U-003/4) | 0.800 (8/10; no C-008, grant swap as Drift) |
| internal_consistency | 0.25 | 0.821 (1 - 2.5/14) | 0.850 (1 - 1.5/10) | 0.750 (1 - 3.0/12) |
| specificity_ratio | 0.15 | 0.923 (24/26) | 1.000 (17/17) | 0.900 (18/20) |
| dependency_completeness | 0.15 | 0.929 (13/14; WC-9 unresolved) | 0.667 (8/12) | 0.727 (8/11) |
| section_coverage | 0.15 | 0.750 (3/4 blocks) | 1.000 (4/4) | 1.000 (4/4) |
| **quant_score** | | **0.8356** | **0.7325** | **0.8216** |

Arithmetic re-check (one full recomputation per variant, unrounded inputs):

- V1: 0.30x0.8000 + 0.25x(1 - 2.5/14 = 0.82143) + 0.15x(24/26 = 0.92308) + 0.15x(13/14 = 0.92857) + 0.15x0.75 = 0.24000 + 0.20536 + 0.13846 + 0.13929 + 0.11250 = **0.83561**. Matches pass 1 (0.8357; rounding). Also re-checked the V1 header tally against its rows: Regression #1; Drift #2, #3, #5, #7, #8, #12 = 6; Necessary #4, #6, #9 = 3; Authorized #10, #11 = 2; total 12. Matches.
- V2: 0.30x0.40 + 0.25x(1 - 1.5/10 = 0.85) + 0.15x1.0 + 0.15x(8/12 = 0.66667) + 0.15x1.0 = 0.12000 + 0.21250 + 0.15000 + 0.10000 + 0.15000 = **0.73250**. Matches.
- V3: 0.30x0.80 + 0.25x(1 - 3/12 = 0.75) + 0.15x(18/20 = 0.90) + 0.15x(8/11 = 0.72727) + 0.15x1.0 = 0.24000 + 0.18750 + 0.13500 + 0.10909 + 0.15000 = **0.82159**. Matches.

Note on IC: pass 1 counted claims refuted in the debate as contradictions (pass 1 A.0), which is wider than the protocol's "contradicting claims within the same variant" (scoring-protocol.md IC step 2). The quantitative layer is taken as given per instruction; the effect on criterion 2.4 is handled in the re-evaluation below.

## Qualitative Scoring (50% weight) - Additive Binary Rubric

Final verdicts after position-bias reconciliation. Evidence is a quote from the variant; where a verdict is NOT MET, the searched sections are named. Rows marked (R) were re-evaluated; the side-by-side comparison is in the Position-Bias Mitigation section.

### Completeness (5 criteria)

| Criterion | V1 | Evidence | V2 | Evidence | V3 | Evidence |
|---|---|---|---|---|---|---|
| 1.1 Covers all explicit requirements (R) | NM | 8/10; no U-003, U-004 | NM | 4/10; "did not find the README.md install-line defect or the Task 23 find defect" | NM | 8/10; no C-008; #5 grant swap "Drift" |
| 1.2 Edge cases and failure scenarios (R for V2) | M | #1 "the install line can never pass and every live task records `not run: install precondition failed`" | NM | Searched #1-#7, regression paragraph, Advisory: all LOW classifications, no failing case | M | #1 "exits non-zero, install line FAIL, all live tasks `not run` (plan:21, :36)" |
| 1.3 Dependencies and prerequisites | M | Advisory (2) "Live tasks depend only on Task 1" | NM | Searched rows and Advisory: no prerequisite statement | M | #1 "all live tasks `not run` (plan:21, :36)" |
| 1.4 Success/completion criteria (R) | NM | Searched header, table, Advisory: no completion criterion for the review or a fix | NM | Same search; #4 describes the plan's rule, defines none | NM | Same search; #1 and #2 report rules that fail, define none |
| 1.5 Out of scope stated (R for V2) | NM | Searched header, table, Advisory: no exclusion | NM | "every command line in Tasks 2-24 matches source.md:51-79" bounds what was checked but states no exclusion | M | Notes "install_skills.py:88-98 ... (not checked)" |
| **Subtotal** | **2/5** | | **0/5** | | **3/5** | |

### Correctness (5 criteria)

| Criterion | V1 | Evidence | V2 | Evidence | V3 | Evidence |
|---|---|---|---|---|---|---|
| 2.1 No factual errors | NM | #2 "the tree already had tracked changes (APPROVED.md, plan file)" stale at 0b443745; "so the checks conflict" withdrawn (round2-advocate-1 row 4); #8 rests on a "same tree" spec clause that does not exist | NM | "No Regression found" withdrawn (round2-advocate-2 row 1) | NM | #5 "stated reason ... does not explain it" contradicted by APPROVED.md G1; #3 "the modified APPROVED.md" stale |
| 2.2 Technical approach feasible (R for V2) | M | #1 "install_commands.py:11 (_EXCLUDE_FILES = {"README.md"}), :40 (glob("*.md"))", reproduced by all three advocates | M | "every command line in Tasks 2-24 matches source.md:51-79" is a feasible bounded check; #4 (C-009) and #5 (C-008) verified by advocates | M | #1 same installer citation; Advisory (1) pgrep self-match reproduced by three advocates |
| 2.3 Terminology accurate (R for V2) | M | Header "Regression 1, Drift 6, Necessary 3, Authorized 2" matches rows; #4 "Necessary" for the swap | NM | #6 classed "Drift" while its own Finding says "matrix trace debt, not a plan defect"; advocate conceded "not a plan Drift" (round2-advocate-2 row 7) | NM | #5 "Drift" for a swap with inline rationale; taxonomy excludes it (advocate conceded, round2-advocate-3 row 1) |
| 2.4 No internal contradictions (R for V3) | M | Header tally matches rows; IC 0.821 | M | Header tally matches rows; IC 0.850 | M | Header "Regression 1, Drift 4, Necessary 2, Authorized 1" matches rows #1 / #2,#3,#5,#6 / #4,#7 / #8; no self-contradicting pair found |
| 2.5 Claims supported by evidence | M | #12 evidence "p1-static-report.md:29" | M | #1 evidence "APPROVED.md:66-71"; #4 "source.md:70, :72" | M | #1 "install_commands.py:11, :40; plan:21, :36, :61" |
| **Subtotal** | **4/5** | | **3/5** | | **3/5** | |

### Structure (5 criteria)

| Criterion | V1 | Evidence | V2 | Evidence | V3 | Evidence |
|---|---|---|---|---|---|---|
| 3.1 Logical ordering | M | Path key, then table, then "Advisory correctness gaps" | M | Table, then "No Regression found ... Notes", then "Advisory" | M | Table, "Advisory:", "Notes:" |
| 3.2 Consistent hierarchy | M | Single heading, flat blocks | M | Same | M | Same |
| 3.3 Separation of concerns | M | "Advisory correctness gaps: (1) ... (2)" separate from table | M | Advisory paragraph separate | M | "Advisory:" and "Notes:" separate |
| 3.4 Navigation aids (R for V2) | M | Path key "Plan = `.dev/tasks/to-do/...`; brief = `source.md`" | NM | Searched table and trailing paragraphs: no path key, no in-card cross-reference | M | #5 "collides with #3" |
| 3.5 Artifact conventions | M | `# / Class / Location / Finding / Evidence / Sev` | M | Same columns | M | Same columns |
| **Subtotal** | **5/5** | | **4/5** | | **5/5** | |

### Clarity (5 criteria)

| Criterion | V1 | Evidence | V2 | Evidence | V3 | Evidence |
|---|---|---|---|---|---|---|
| 4.1 Unambiguous language | NM | Advisory (1) "may resolve"; #3 "is a fuzzy test" | M | "spec 2.1 permits both, so no rule is breached" | NM | Advisory (1) "likely matches"; Notes "possible further problem" |
| 4.2 Concrete | M | "plan:58 (Task 1 install line)" | M | "(lines 16, 23, 30, 36-44, 70, 78, 87)" | M | "install_skills.py:88-98"; "plan:451, :465" |
| 4.3 Clear purpose per section | M | "Advisory correctness gaps" | M | "Advisory:" | M | "Advisory:", "Notes:" |
| 4.4 Terms defined on first use | NM | "WC-9", "AC-1.8", "D-P1-5" undefined | NM | "G1", "WC-9", "D-P1-5", "lc18" undefined | NM | "lc18", "lc15", "lc13" undefined |
| 4.5 Actionable next steps | NM | Searched table and Advisory: no fix or decision | NM | Same search | NM | Same search |
| **Subtotal** | **2/5** | | **3/5** | | **2/5** | |

### Risk Coverage (5 criteria)

| Criterion | V1 | Evidence | V2 | Evidence | V3 | Evidence |
|---|---|---|---|---|---|---|
| 5.1 >= 3 risks with probability and impact | M | #1 HIGH "can never pass"; #7 MEDIUM "cannot hold"; Advisory (2) "would pollute" | NM | All 7 rows LOW; no likelihood language | M | #1 HIGH "exits non-zero"; #2 MEDIUM "false FAIL"; Advisory (1) "likely matches ... may fail falsely" |
| 5.2 Mitigation for each risk | NM | Searched table and Advisory: none | NM | None | NM | None |
| 5.3 Failure modes and recovery (R) | NM | Failure mode "records `not run`" stated; no recovery step | NM | Neither | NM | Failure mode "install line FAIL" stated; no recovery step |
| 5.4 External dependencies | M | Advisory (1) "`--parent-worktree active` may resolve to the Orca UI's active worktree" | NM | #2 cites `p0-live-orca-help.txt` as justification only | M | #7 "`--parent-worktree active` not re-checked on Orca 1.4.245"; Advisory (1) pgrep vs the Bash tool |
| 5.5 Monitoring/validation mechanism (R) | NM | Advisory (2) names a threat to the plan's checks; proposes no mechanism | M | "every command line in Tasks 2-24 matches source.md:51-79"; "reviewer verified the plan implements each" | NM | Advisory (1) names a threat to lc18's check; proposes no mechanism |
| **Subtotal** | **2/5** | | **1/5** | | **2/5** | |

### Invariant and Edge Case Coverage (5 criteria)

| Criterion | V1 | Evidence | V2 | Evidence | V3 | Evidence |
|---|---|---|---|---|---|---|
| 6.1 Collection boundaries | M | #7 "pass rule "find output is empty" cannot hold: the branch tracks many return-contract.yaml files" | NM | Searched #1-#7: none | M | #2 "is never empty because tracked files exist" |
| 6.2 State interactions across boundaries (R for V2) | M | #2 "Task 1 requires `git status --porcelain` to show no modified tracked file" vs the plan's edit | M | #4 "the brief's phase header at source.md:70 contradicts lc18's own row (a contract is written)" | M | #3 "conflicts with the planned plan-file edit (plan:52) ... and the plan's own no-commit rule (plan:24)" |
| 6.3 Guard condition gaps (R for V2) | M | #1 "includes README.md and __init__.py, which the installer never copies" | NM | #4 reports a guard the plan correctly drops, not a missing guard; "No Regression found" asserts none | M | Advisory (2) "No rule normalises the worker's `--report-path`" |
| 6.4 Count divergence | M | #1 source set wider than installed set | M | #6 "seven requirement-bearing spans of source.md have no matrix row" | M | #1 "includes README.md and __init__.py, which are not installed" |
| 6.5 Interaction effects | M | Advisory (2) "a concurrent run would pollute `check --run` and the machine-wide `pgrep`" | NM | "spec 2.1 permits both" dismisses the combination | M | Advisory (1) pgrep vs the Bash tool's own shell |
| **Subtotal** | **5/5** | | **2/5** | | **5/5** | |

### Qualitative Summary

| Dimension | V1 | V2 | V3 |
|---|---|---|---|
| Completeness | 2/5 | 0/5 | 3/5 |
| Correctness | 4/5 | 3/5 | 3/5 |
| Structure | 5/5 | 4/5 | 5/5 |
| Clarity | 2/5 | 3/5 | 2/5 |
| Risk Coverage | 2/5 | 1/5 | 2/5 |
| Invariant & Edge Case | 5/5 | 2/5 | 5/5 |
| **qual_score** | **20/30 = 0.667** | **13/30 = 0.433** | **20/30 = 0.667** |

For comparison: pass 1 gave 20 / 16 / 19; pass 2 gave 24 / 13 / 24.

### Edge Case Floor check (Invariant & Edge Case >= 1/5)

| Variant | Dim 6 | Eligible as base |
|---|---|---|
| V1 | 5/5 | yes |
| V2 | 2/5 | yes |
| V3 | 5/5 | yes |

No variant is below the floor; the floor is not suspended and no warning is needed.

## Position-Bias Mitigation

### Per-criterion table (Pass 1 / Pass 2 / agreement / final)

| # | Criterion | V1 P1 / P2 / Agr / Final | V2 P1 / P2 / Agr / Final | V3 P1 / P2 / Agr / Final |
|---|---|---|---|---|
| 1.1 | Covers all explicit requirements | NM / M / DIS / **NM** | NM / NM / agree / **NM** | NM / M / DIS / **NM** |
| 1.2 | Edge cases and failures | M / M / agree / **M** | M / NM / DIS / **NM** | M / M / agree / **M** |
| 1.3 | Dependencies and prerequisites | M / M / agree / **M** | NM / NM / agree / **NM** | M / M / agree / **M** |
| 1.4 | Success/completion criteria | NM / M / DIS / **NM** | NM / M / DIS / **NM** | NM / M / DIS / **NM** |
| 1.5 | Out of scope stated | NM / NM / agree / **NM** | NM / M / DIS / **NM** | M / M / agree / **M** |
| 2.1 | No factual errors | NM / NM / agree / **NM** | NM / NM / agree / **NM** | NM / NM / agree / **NM** |
| 2.2 | Technical approach feasible | M / M / agree / **M** | M / NM / DIS / **M** | M / M / agree / **M** |
| 2.3 | Terminology accurate | M / M / agree / **M** | M / NM / DIS / **NM** | NM / NM / agree / **NM** |
| 2.4 | No internal contradictions | M / M / agree / **M** | M / M / agree / **M** | NM / M / DIS / **M** |
| 2.5 | Claims supported | M / M / agree / **M** | M / M / agree / **M** | M / M / agree / **M** |
| 3.1 | Logical ordering | M / M / agree / **M** | M / M / agree / **M** | M / M / agree / **M** |
| 3.2 | Consistent hierarchy | M / M / agree / **M** | M / M / agree / **M** | M / M / agree / **M** |
| 3.3 | Separation of concerns | M / M / agree / **M** | M / M / agree / **M** | M / M / agree / **M** |
| 3.4 | Navigation aids | M / M / agree / **M** | M / NM / DIS / **NM** | M / M / agree / **M** |
| 3.5 | Artifact conventions | M / M / agree / **M** | M / M / agree / **M** | M / M / agree / **M** |
| 4.1 | Unambiguous language | NM / NM / agree / **NM** | M / M / agree / **M** | NM / NM / agree / **NM** |
| 4.2 | Concrete | M / M / agree / **M** | M / M / agree / **M** | M / M / agree / **M** |
| 4.3 | Clear purpose per section | M / M / agree / **M** | M / M / agree / **M** | M / M / agree / **M** |
| 4.4 | Terms defined on first use | NM / NM / agree / **NM** | NM / NM / agree / **NM** | NM / NM / agree / **NM** |
| 4.5 | Actionable next steps | NM / NM / agree / **NM** | NM / NM / agree / **NM** | NM / NM / agree / **NM** |
| 5.1 | >= 3 risks with probability and impact | M / M / agree / **M** | NM / NM / agree / **NM** | M / M / agree / **M** |
| 5.2 | Mitigation for each risk | NM / NM / agree / **NM** | NM / NM / agree / **NM** | NM / NM / agree / **NM** |
| 5.3 | Failure modes and recovery | NM / M / DIS / **NM** | NM / NM / agree / **NM** | NM / M / DIS / **NM** |
| 5.4 | External dependencies | M / M / agree / **M** | NM / NM / agree / **NM** | M / M / agree / **M** |
| 5.5 | Monitoring/validation mechanism | NM / M / DIS / **NM** | M / NM / DIS / **M** | NM / M / DIS / **NM** |
| 6.1 | Collection boundaries | M / M / agree / **M** | NM / NM / agree / **NM** | M / M / agree / **M** |
| 6.2 | State interactions | M / M / agree / **M** | M / NM / DIS / **M** | M / M / agree / **M** |
| 6.3 | Guard condition gaps | M / M / agree / **M** | NM / M / DIS / **NM** | M / M / agree / **M** |
| 6.4 | Count divergence | M / M / agree / **M** | M / M / agree / **M** | M / M / agree / **M** |
| 6.5 | Interaction effects | M / M / agree / **M** | NM / NM / agree / **NM** | M / M / agree / **M** |

### Re-evaluation of disagreements (explicit comparison; verdict FINAL)

**1.1 Covers all explicit requirements, V1 and V3.**
Pass 1: NM, strict reading "all 10 requirements" (A.0 list); V1 lacks U-003, U-004; V3 lacks C-008 and misclassifies the swap.
Pass 2: MET, reading narrowed to "captures C-001, C-002, C-003"; pass 2 itself notes "No card captures all seven, so a stricter reading would cost V1 and V3 one point each".
Comparison: the criterion says "all". Neither card covers all established defects. FINAL: V1 NM, V3 NM.

**1.2 Edge cases and failure scenarios, V2.**
Pass 1: MET on #4 "the brief's phase header at source.md:70 contradicts lc18's own row (a contract is written)".
Pass 2: NM; "Rows #1-#7 are all LOW classifications with no failing case".
Comparison: #4 records a contradiction inside the brief that the plan resolves (round2-advocate-2 N1: documented at P:41). Nothing in V2 describes a scenario in which the plan fails. FINAL: NM.

**1.4 Success/completion criteria, V1, V2, V3.**
Pass 1: NM for all; no completion criterion for the review.
Pass 2: MET for all; each card "states the pass rule at issue" (V1 #7, V2 #4, V3 #1/#2).
Comparison: quoting a plan's pass rule, or saying it cannot be met, does not define a success criterion in the card (for the review or for the fix). No card states what "fixed" or "done" looks like. FINAL: NM for all three.

**1.5 Out of scope stated, V2.**
Pass 1: NM; "did not find the README.md install-line defect" is a gap admission, not scope.
Pass 2: MET; "every command line in Tasks 2-24 matches source.md:51-79" bounds the scan.
Comparison: the parenthetical names what was checked, and the advocates read the exclusion of Task 1 into it (round1-advocate-3 weakness 1), but the card never says Task 1 or S:87 were out of scope. V3's "(not checked)" is the explicit form; V2 has none. FINAL: NM.

**2.2 Technical approach feasible, V2.**
Pass 1: MET; the bounded comparison is feasible and the findings it produced (C-009, C-008) were verified.
Pass 2: NM; text-to-text only, cannot find executable defects.
Comparison: the criterion is feasibility, not sufficiency. V2's method is feasible and every row it produced survived the debate (round2-advocate-2 row 8: "no row in V2 has been refuted"). Its insufficiency is already scored in 1.1 and 2.1. FINAL: MET.

**2.3 Terminology accurate, V2.**
Pass 1: MET; header tally matches rows, settled classes not reversed.
Pass 2: NM; #6 is labelled "Drift" while the Finding says "matrix trace debt, not a plan defect".
Comparison: the card applies the Drift class (a plan change) to an audit-artifact gap it itself says is not a plan defect; the advocate conceded the class (round2-advocate-2 row 7, section 4 C-010). Pass 1 penalised V3 for the same kind of class misuse (#5), so consistency requires the same here. FINAL: NM.

**2.4 No internal contradictions, V3.**
Pass 1: NM; rule "MET only if IC >= 0.80", V3 IC 0.750.
Pass 2: MET; header "Regression 1, Drift 4, Necessary 2, Authorized 1" matches rows.
Comparison: V3's IC shortfall comes from pass 1 counting debate-refuted claims (#5 Drift, U-005 note) as contradictions. The protocol defines IC as contradicting claims "within the same variant". Searching V3 for a self-contradicting pair finds none: the tally matches, #5 "collides with #3" is consistent with #3, and the Notes do not contradict any row. The refuted claims are already penalised under 2.1 and 2.3. FINAL: MET. (Sensitivity: if this stayed NM, V3 would be 19/30 and the outcome below is unchanged.)

**3.4 Navigation aids, V2.**
Pass 1: MET; numbered rows, Location column, header tally.
Pass 2: NM; no path key and no in-card cross-reference.
Comparison: numbered rows and the Location column are the table convention all three share (scored under 3.5). V1 adds a path key; V3 adds an in-card cross-reference ("collides with #3"). V2 has neither. FINAL: NM.

**5.3 Failure modes and recovery, V1 and V3.**
Pass 1: NM; failure mode stated, no recovery.
Pass 2: MET; "failure path and the plan's fallback" (`not run`).
Comparison: the criterion needs both a failure mode and a recovery procedure. Recording `not run` is the failure outcome, not a recovery; neither card says how to recover (for example, restricting the `cmp` set). FINAL: V1 NM, V3 NM.

**5.5 Monitoring or validation mechanism, V1, V2, V3.**
Pass 1: V1 NM, V2 MET (its documented verification pass), V3 NM.
Pass 2: V1 MET and V3 MET ("examines the plan's detection mechanism"), V2 NM (fidelity comparison shown ineffective).
Comparison: V1 Advisory (2) and V3 Advisory (1) identify threats to the plan's checks; neither proposes a mechanism. V2 documents the validation it ran ("every command line in Tasks 2-24 matches source.md:51-79"; "reviewer verified the plan implements each"). Its weakness is coverage, scored in 1.1 and 2.1, not absence of a mechanism. FINAL: V1 NM, V2 MET, V3 NM.

**6.2 State interactions across boundaries, V2.**
Pass 1: MET on #4.
Pass 2: NM; no evidence.
Comparison: #4 concerns the worker writing a contract (`worker_status: failed`) while the phase rule expects "step 6 shows nothing written", and records that the plan keeps step 3's rule for Task 19. That is a state interaction between the worker's output and the checker's rule, and the debate confirmed it (round2-advocate-2 N1; round2-advocate-3 section 2). FINAL: MET.

**6.3 Guard condition gaps, V2.**
Pass 1: NM; no unguarded assumption identified.
Pass 2: MET on #4.
Comparison: #4 says the plan correctly does not apply the brief's step-6 rule to Task 19; it reports a guard correctly dropped, not a missing one. The only residue (P:49 wording) was found in the debate, not by V2. FINAL: NM.

Disagreements re-evaluated: **18** cells across 12 criteria (1.1 x2, 1.2, 1.4 x3, 1.5, 2.2, 2.3, 2.4, 3.4, 5.3 x2, 5.5 x3, 6.2, 6.3).
Final verdicts: 14 sided with pass 1, 4 sided with pass 2.
Final verdicts changed relative to pass 1: **4** (1.2 V2 M->NM, 2.3 V2 M->NM, 3.4 V2 M->NM, 2.4 V3 NM->M). Relative to pass 2: 14.

## Combined Scoring

| Variant | Quant (x0.50) | Qual (x0.50) | **Final Score** | Debate Tiebreaker |
|---|---|---|---|---|
| V1 (analyzer) | 0.8356 -> 0.4178 | 0.6667 -> 0.3333 | **0.7511** | 10/17 decided points = 58.8% |
| V3 (refactorer) | 0.8216 -> 0.4108 | 0.6667 -> 0.3333 | **0.7441** | 8/17 = 47.1% |
| V2 (qa) | 0.7325 -> 0.3663 | 0.4333 -> 0.2167 | **0.5829** | 7/17 = 41.2% |

Ranking: V1 (0.7511), V3 (0.7441), V2 (0.5829).
**Margin**: V1 - V3 = 0.0070 (0.93% of V1's score), below the 0.05 threshold.
**Tiebreaker applied**: Yes, level 1 decided it.

### Tiebreaker level 1: points won in the debate

Counting rule: for each diff point, the round 1 "Per-point judgements" of the three advocates name the superior variant(s); a variant wins the point when at least 2 of 3 advocates name it. Where round 2 changed a judgement (final positions, sections 4 and 5 of each rebuttal), the round 2 position is used. Points where all advocates rule "all equal", or where the only holder's claim was dropped, have no winner. A unique point (U-NNN) is won by its owner when at least 2 advocates accept it.

| Point | Winner(s) | Basis |
|---|---|---|
| C-001 | V1, V3 | All three R1: "V1/V3 superior"; verified rc=2 |
| C-002 | V3 | R1: A1 V1+V3, A2 V3, A3 V3; R2 agreed "with V3's P:24 argument" |
| C-003 | V1, V3 | All three R1 name V1 and V3; R2 severity LOW, still held only by V1/V3 |
| C-004 | V1, V2 | R1: A1 V1, A2 V2 (V1 quoting valid), A3 V2/V1; R2: swap not Drift (V1, V2 right), quoting half V1 only |
| C-005 | V1, V3 | All three R1 |
| C-006 | none | all equal |
| C-007 | none | all equal |
| C-008 | V1, V2 | All three R1 |
| C-009 | V2 | All three R1; R2 settled for V2 (P:41) |
| C-010 | V2 | All three R1; R2 kept as process note |
| C-011 | none | all equal |
| C-012 | V1, V2 | R1: V1 named 3/3, V2 named 2/3 |
| C-013 | none | R1 V1 only; R2 A2 and A3: not supported (no "same tree" clause), dropped to a note |
| X-001 | V1, V3 | All three R1; V2 withdrew |
| X-002 | V1, V2 | R2: not Drift (A1, A3 Authorized; A2 Necessary); V1 and V2 both classed it non-Drift |
| X-003 | V3 | All three R1 name V3 |
| U-001 | V1 | Accepted as advisory by A1, A2 (A3 qualifies under A-003) |
| U-002 | V1 | Accepted by A1, A2 |
| U-003 | V3 | Verified by all three |
| U-004 | V3 | Accepted by all three (LOW-MEDIUM) |
| U-005 | none | Conceded by all, including A3 |
| U-006 | V2 | Accepted by all three (LOW) |

Decided points: 17 of 22. Wins: **V1 10** (C-001, C-003, C-004, C-005, C-008, C-012, X-001, X-002, U-001, U-002), **V3 8** (C-001, C-002, C-003, C-005, X-001, X-003, U-003, U-004), V2 7 (C-004, C-008, C-009, C-010, C-012, X-002, U-006).
V1 vs V3: 58.8% vs 47.1%, a gap of 11.8 points, not within 5%. Level 1 selects **V1**. The result is robust to the counting rule: crediting V1 for C-002 (A1 named it) or for C-013 (round 1 only) widens the gap.

Levels 2 and 3 not needed. For the record: level 2 correctness count V1 4/5, V3 3/5 (also V1); level 3 input order V1 first (also V1).

## Selected Base: Variant 1 (reviewer-1 card, analyzer)

### Selection Rationale

V1 has the highest combined score (0.7511 vs V3 0.7441), and it wins the tiebreaker on debate points (10 vs 8). Quantitatively it ties V3 on requirement coverage (0.800) and leads on internal consistency (0.821 vs 0.750) and dependency completeness (0.929 vs 0.727; its path key resolves every `plan:NN`). Qualitatively it ties V3 at 20/30, with the edge-case floor at 5/5, and leads on Correctness (4 vs 3): its class labels survived the debate, including the swap as Necessary (C-004 / X-002), where V3's Drift was withdrawn. It is the broadest card (12 rows; C-008, C-012, U-001, U-002 held only by V1 or not by V3), and both HIGH/MEDIUM defects that every advocate verified (C-001, C-003) are already in it. V3's advantages (U-003, U-004, the P:24 argument for C-002, an explicit "not checked" note) are additive and easy to merge; V1's advantages over V3 are class correctness and breadth, which would be costlier to retrofit into V3.

### Strengths to Preserve from Base

1. **C-001 / X-001 (V1 #1)**: Regression-class, HIGH, with the installer citations `install_commands.py:11` and `:40`. Strengthen the wording with the debate's agreed label: inherited from S:87, sharpened by fix pass 1 ("the whole folder, changed or not", "PASS only when every `cmp` exits 0"), contradicts S:17 and P:21 "installed files differ" (round2-advocate-1 row 1; round2-advocate-3 E1, E2).
2. **C-004 split (V1 #4 and #3)**: the swap is Necessary (Authorized acceptable; not Drift, X-002), plus a separate quoting row, downgraded to Drift LOW with "fuzzy test" removed; add the E4 fix (P:52 states that the owner sentence replaces `NOT YET GIVEN` and P:556 copies only that sentence).
3. **C-003 (V1 #7)**: kept, downgraded to LOW; reword "cannot hold" to "the pass clause drops the exemption S:78 keeps; no saved baseline"; add the fix from round2-advocate-1 E3 and round2-advocate-3 E3 (compare against `ac13-status-after-*.txt` or `git ls-files`).
4. **C-005 (V1 #5)**, **C-008 (V1 #12)**, **C-012 (V1 #10)**, **C-011 (V1 #11)**, **C-006 (V1 #6)**, **C-007 (V1 #9)** as written.
5. **U-001 (Advisory 1)**, restated as "unverified; one read of the parent field in `lc22-worktree.json`", and **U-002 (Advisory 2)**.
6. The path key line and the 6-column class table with a matching tally.

Corrections required in the base (debate-settled): V1 #2 (C-002) drops "the tree already had tracked changes (APPROVED.md, plan file)" and "so the checks conflict" (P:65 is a tolerant superset), and becomes conditional MEDIUM; V1 #8 (C-013) is dropped to a note (no "same tree" clause in the spec).

### Strengths to Incorporate from Non-Base Variants

1. **From V3, U-003 (Advisory 1)**: `pgrep -af -- '--watch'` matches the Bash tool's own wrapper shell; reproduced by all three advocates. Scope it to lc18 (P:451, P:465; also S:72), not lc08 (P:227), per round2-advocate-3 E5. LOW-MEDIUM.
2. **From V3, U-004 (Advisory 2)**: no rule normalises the worker's `--report-path` against `<R>/return-contract.yaml` (P:41 vs P:43; `<R>` already ends in a slash). LOW-MEDIUM advisory.
3. **From V3, C-002 / X-003 (V3 #3)**: the P:24 no-commit argument and the collision with the P:52 edit, replacing V1's stale framing; add the fix from round2-advocate-1 E2 and round2-advocate-3 E4 (scope the clean-tree check to `src/`, `plugins/`, `tests/`, `.claude/`, or have P:52 say to commit the edit before launch; staging alone still shows `M`).
4. **From V3, the C-004 consequence note (V3 #5, "collides with #3")**, kept as a note on the Necessary swap, not as a Drift row.
5. **From V3, the explicit scope note** in the "(not checked)" style (criterion 1.5), applied to what the merged review did not verify (for example U-001's resolution).
6. **From V2, C-009 (V2 #4)**: Necessary LOW, documented in the plan at P:41 and consistent with spec AC-1.5/AC-1.6; add the LOW wording residue at P:49 (round2-advocate-2 N1).
7. **From V2, C-010 (V2 #6)**: as a process note, not a Drift row, with the N2 point that the uncovered spans include S:78 and S:87, the lines that carry C-003 and C-001; remedy: add matrix rows for those spans.
8. **From V2, U-006 (Advisory)**: LOW coverage note (lc13 `--report-dir` vs `--output-dir` at `WORKER-CONTRACT.md:195`; lc15 omits `--output <file>` at `:197`); no rule breached (round2-advocate-2 N5).
9. **From V2, the G1 citation** (`APPROVED.md:66-71`) as evidence on the swap row, plus the LOW provenance note from the debate that the plan cites only H1 (P:31), never G1 (round2-advocate-1 E1; round2-advocate-3 X-002).

Not to incorporate: V2's "No Regression found" (withdrawn), V3 #5's Drift class for the swap (withdrawn), V3's U-005 note (does not fire on the branch diff), V1's C-013 as a deviation row.
