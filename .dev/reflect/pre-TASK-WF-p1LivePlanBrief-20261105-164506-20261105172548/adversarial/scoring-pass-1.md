# Scoring Pass 1 (input order V1, V2, V3)

Folder F = `.dev/reflect/pre-TASK-WF-p1LivePlanBrief-20261105-164506-20261105172548/adversarial/`. Algorithm: `~/.claude/skills/sc-adversarial-protocol/refs/scoring-protocol.md` (A.1 quant, A.2 qual).
Variants: V1 = reviewer-1 card (analyzer), V2 = reviewer-2 card (qa), V3 = reviewer-3 card (refactorer). Debate inputs: `diff-analysis.md`, `round1-advocate-1..3.md`, `round2-advocate-1..3.md`.

## Summary

| Variant | quant | qual | Edge-case dim | Base-eligible |
|---|---|---|---|---|
| V1 | 0.836 | 20/30 = 0.667 | 5/5 | yes |
| V2 | 0.733 | 16/30 = 0.533 | 2/5 | yes |
| V3 | 0.822 | 19/30 = 0.633 | 5/5 | yes |

Provisional combined (0.5 quant + 0.5 qual, pass 1 only, no position-bias reconciliation): V1 0.751, V2 0.633, V3 0.728. V1 vs V3 differ by 0.023 (< 0.05), so the A.4 tiebreaker applies after pass 2.

---

## A. Quantitative layer

### A.0 Conventions used (stated once, applied identically to all three)

- The source documents are not requirement-ID documents, so per the protocol edge case the "source requirements" are the **10 real defects the debate established** (the requirement list):
  R1 C-001 (Task 1 install-line `cmp` includes README.md and `__init__.py`), R2 C-002 (clean-tree check vs the plan's own edit), R3 C-003 (Task 23 `find` has no baseline), R4 C-005 (stale "grant file" wording in Task 25), R5 C-008 (D-P1-5 cited for the staging rule), R6 U-003 (`pgrep -af -- '--watch'` matches the Bash tool's shell), R7 U-004 (no `--report-path` normalisation rule), R8 correct classification of the grant-file swap (Necessary or Authorized, not Drift), R9 correct classification of the tip pin (Necessary), R10 correct classification of the child-worktree change (Necessary).
- Claims = each findings-table row, each "No Regression found"-type conclusion, each advisory item, each notes item. A claim counts as a contradiction when the debate refuted or withdrew it in whole (1.0) or in material part such as a conceded severity inflation or a withdrawn premise (0.5). A claim the debate refuted counts against IC even though the card does not contradict itself textually.
- SR: concrete = statement with file:line, number, named entity or threshold; vague = hedged or judgement-only ("may", "likely", "possible", "fuzzy"). Statement = the Finding cell, the Evidence cell, and each advisory/notes sentence.
- DC: internal references = labels used in the card (Task N, AC-x, WC-x, D-P1-x, lcNN, `#n` rows, "Advisory (n)", the header tally). Resolved = defined, glossed or backed by a row in the same card. References to plan:NN, source.md:NN, spec and WORKER-CONTRACT lines are external documents and excluded (protocol edge case).
- SC: none of the three cards has an H2 heading, so "top-level sections" are counted as top-level blocks (title/scope, findings table, regression statement/notes, advisory, notes).

### A.1 Requirement coverage (RC)

| Req | V1 | V2 | V3 |
|---|---|---|---|
| R1 C-001 | yes (#1) | no | yes (#1) |
| R2 C-002 | yes (#2) | no | yes (#3) |
| R3 C-003 | yes (#7) | no | yes (#2) |
| R4 C-005 | yes (#5) | no | yes (#6) |
| R5 C-008 | yes (#12) | yes (#5) | no |
| R6 U-003 | no | no | yes (advisory 1) |
| R7 U-004 | no | no | yes (advisory 2) |
| R8 grant swap | yes (#4 Necessary; correct) | yes (#1 Necessary; correct) | **no** (#5 Drift; debate withdrew it) |
| R9 tip pin | yes (#9 Necessary) | yes (#3 Necessary) | yes (#4 Necessary) |
| R10 child worktree | yes (#6 Necessary) | yes (#2 Necessary) | yes (#7 Necessary) |
| Matched | 8 | 4 | 8 |
| **RC** | **8/10 = 0.800** | **4/10 = 0.400** | **8/10 = 0.800** |

### A.2 Internal consistency (IC)

| | V1 | V2 | V3 |
|---|---|---|---|
| Claims | 12 rows + 2 advisories = 14 | 7 rows + "No Regression found" + 2 advisories = 10 | 8 rows + 2 advisories + 2 notes = 12 |
| Refuted (1.0) | #2 (premise "tree already had tracked changes" stale; "checks conflict" withdrawn by V1 itself) = 1.0 | "No Regression found" (withdrawn by V2 advocate, X-001) = 1.0 | #5 grant swap as Drift (withdrawn by V3 advocate) = 1.0; U-005 note (does not fire) = 1.0 |
| Partly refuted (0.5) | #3 ("fuzzy", MEDIUM, conceded to LOW) 0.5; #7 (severity conceded to LOW) 0.5; #8 C-013 (no "same tree" clause in spec; dropped to a note) 0.5 | #6 C-010 filed as Drift (reclassified a process note) 0.5 | #2 ("never empty ... false FAIL", conceded LOW) 0.5; #3 (stale APPROVED.md premise, "cannot be met" conceded) 0.5 |
| Contradictions | 2.5 | 1.5 | 3.0 |
| **IC = 1 - c/n** | 1 - 2.5/14 = **0.821** | 1 - 1.5/10 = **0.850** | 1 - 3.0/12 = **0.750** |

### A.3 Specificity ratio (SR)

| | V1 | V2 | V3 |
|---|---|---|---|
| Statements | 12x2 + 2 advisories = 26 | 7x2 + regression statement + 2 advisories = 17 | 8x2 + 2 advisories + 2 notes = 20 |
| Vague | 2 (#3 "fuzzy test"; advisory 1 "may resolve") | 0 | 2 (advisory 1 "likely matches"; notes "possible further problem ... (not checked)") |
| Concrete | 24 | 17 | 18 |
| **SR** | 24/26 = **0.923** | 17/17 = **1.000** | 18/20 = **0.900** |

### A.4 Dependency completeness (DC)

| | V1 | V2 | V3 |
|---|---|---|---|
| References (resolved/total) | Task 1, 23, 24, 25 (4 ok); AC-1.8, AC-1.3, AC-1.7 (3 ok, each glossed); D-P1-5 (ok, glossed); Constraints bullet, `<OWNER INSTRUCTION>` (2 ok, glossed in row 3); Advisory (1), (2) (2 ok); header tally 1+6+3+2=12 matches rows (ok); WC-9 (not glossed) = **13/14** | header tally 0+2+4+1=7 matches rows (ok); lc18, Task 19, Task 24, "Tasks 2-24", G1, coverage matrix, AC-1.6 (7 ok); lc15, lc13, D-P1-5, WC-9 (4 unresolved) = **8/12** | header tally 1+4+2+1=8 matches rows (ok); Task 1, Task 25, `#3`, branch-tip.txt, grant file, Advisory (1), (2) (7 ok); lc18, lc15, lc13 (3 unresolved) = **8/11** |
| **DC** | **0.929** | **0.667** | **0.727** |

### A.5 Section coverage (SC)

| | V1 | V2 | V3 |
|---|---|---|---|
| Blocks | title/scope, findings table, advisory = 3 | title, findings table, regression statement + notes, advisory = 4 | title, findings table, advisory, notes = 4 |
| **SC** (max 4) | 3/4 = **0.750** | 4/4 = **1.000** | 4/4 = **1.000** |

### A.6 Quant score = 0.30 RC + 0.25 IC + 0.15 SR + 0.15 DC + 0.15 SC

| | RC x0.30 | IC x0.25 | SR x0.15 | DC x0.15 | SC x0.15 | **quant** |
|---|---|---|---|---|---|---|
| V1 | 0.800 -> 0.2400 | 0.821 -> 0.2054 | 0.923 -> 0.1385 | 0.929 -> 0.1393 | 0.750 -> 0.1125 | **0.8357** |
| V2 | 0.400 -> 0.1200 | 0.850 -> 0.2125 | 1.000 -> 0.1500 | 0.667 -> 0.1000 | 1.000 -> 0.1500 | **0.7325** |
| V3 | 0.800 -> 0.2400 | 0.750 -> 0.1875 | 0.900 -> 0.1350 | 0.727 -> 0.1091 | 1.000 -> 0.1500 | **0.8216** |

---

## B. Qualitative layer (30 criteria, Claim-Evidence-Verdict)

Rules applied: a MET verdict needs a quoted line from the variant; otherwise NOT MET. The rubric is written for plans, so "source input" is read as the plan and brief under audit, and "the document" as the reviewer card. Two interpretation rules, applied identically: criterion 1.1 requires all 10 requirements listed in A.0; criterion 2.4 is cross-validated with IC and is MET only if IC >= 0.80.

### Dimension 1: Completeness

| # | Criterion | V1 | V2 | V3 |
|---|---|---|---|---|
| 1.1 | Covers all explicit requirements | NOT MET. 8/10; no U-003, U-004 | NOT MET. 4/10; no C-001/2/3/5, U-003/4 | NOT MET. 8/10; no C-008, grant swap misclassified |
| 1.2 | Edge cases and failure scenarios | MET. "so the install line can never pass and every live task records `not run: install precondition failed`" | MET. "the brief's phase header at source.md:70 contradicts lc18's own row (a contract is written)" | MET. "exits non-zero, install line FAIL, all live tasks `not run` (plan:21, :36)" |
| 1.3 | Dependencies and prerequisites | MET. "Live tasks depend only on Task 1; a concurrent run would pollute `check --run`" | NOT MET. Searched rows 1-7 and Advisory: no prerequisite or dependency statement | MET. "all live tasks `not run` (plan:21, :36)" ties every live task to the Task 1 gate |
| 1.4 | Success/completion criteria defined | NOT MET. No completion criterion for the review | NOT MET. "reviewer verified the plan implements each" is a check, not a criterion | NOT MET. No completion criterion |
| 1.5 | Out of scope stated | NOT MET. No exclusions listed | NOT MET. "did not find the README.md install-line defect" is a gap, not a scope statement | MET. "(not checked)" on the install_skills.py concern names what was left unchecked |
| | **Subtotal** | **2** | **1** | **3** |

### Dimension 2: Correctness

| # | Criterion | V1 | V2 | V3 |
|---|---|---|---|---|
| 2.1 | No factual errors or hallucinated claims | NOT MET. Row 2 "the tree already had tracked changes (APPROVED.md, plan file)" stale; "so the checks conflict" withdrawn by V1 | NOT MET. "No Regression found" refuted; withdrawn in round 2 | NOT MET. Row 5 "stated reason ... does not explain it" contradicted by APPROVED.md G1; U-005 note does not fire |
| 2.2 | Technical approach feasible | MET. "src/superclaude/cli/install_commands.py:11 (_EXCLUDE_FILES = {"README.md"}), :40 (glob("*.md"))" is a checkable, verified method (cmp rc=2 reproduced by 3 advocates) | MET. "every command line in Tasks 2-24 matches source.md:51-79" is a feasible, bounded check, and C-009 (row 4) was verified | MET. Same installer citation as V1; `pgrep` self-match reproduced by 3 advocates |
| 2.3 | Terminology consistent and accurate | MET. Header "12 deviations (Regression 1, Drift 6, Necessary 3, Authorized 2)" matches its rows; no row carries a class opposite to the settled one | MET. Header "7 deviations (Regression 0, Drift 2, Necessary 4, Authorized 1)" matches rows; settled classes not reversed | NOT MET. Row 5 labelled "Drift" for a swap with inline rationale (taxonomy excludes Drift; debate settled Necessary/Authorized) |
| 2.4 | No internal contradictions (IC >= 0.80) | MET. IC 0.821 | MET. IC 0.850 | NOT MET. IC 0.750 |
| 2.5 | Claims supported by evidence in the document | MET. Every row has an Evidence cell, e.g. "plan:541, :544; spec AC-1.3 (spec line 319, "no return-contract.yaml appears")" | MET. e.g. row 4 evidence "source.md:70, :72; spec AC-1.6 row" | MET. e.g. "src/superclaude/cli/install_commands.py:11, :40; plan:21, :36, :61" |
| | **Subtotal** | **4** | **4** | **2** |

### Dimension 3: Structure

| # | Criterion | V1 | V2 | V3 |
|---|---|---|---|---|
| 3.1 | Logical ordering | MET. Scope line, then findings table, then "Advisory correctness gaps" | MET. Table, then "No Regression found ... Notes", then "Advisory" | MET. Table, then "Advisory", then "Notes" |
| 3.2 | Consistent hierarchy depth | MET. One table level plus one advisory paragraph; no orphans | MET. Same flat shape | MET. Same flat shape |
| 3.3 | Separation of concerns | MET. Findings table separate from "Advisory correctness gaps: (1) ... (2)" | MET. Findings, regression stance and advisory in separate blocks | MET. Findings, advisory and "Notes:" separate |
| 3.4 | Navigation aids | MET. Path key "Plan = `.dev/tasks/to-do/...`; brief = `source.md`" plus numbered rows and a Location column | MET. Numbered rows, Location column and header tally "7 deviations (...)" | MET. Numbered rows, Location column and row cross-reference "collides with #3" |
| 3.5 | Follows artifact-type conventions | MET. Columns `# / Class / Location / Finding / Evidence / Sev` with the four taxonomy classes | MET. Same columns and classes | MET. Same columns and classes |
| | **Subtotal** | **5** | **5** | **5** |

### Dimension 4: Clarity

| # | Criterion | V1 | V2 | V3 |
|---|---|---|---|---|
| 4.1 | Unambiguous language | NOT MET. "`--parent-worktree active` may resolve to the Orca UI's active worktree"; "is a fuzzy test" | MET. Searched all rows and Advisory: no hedge words; "spec 2.1 permits both, so no rule is breached" | NOT MET. "`pgrep -af -- '--watch'` likely matches"; "possible further problem" |
| 4.2 | Concrete rather than abstract | MET. "plan:58 (Task 1 install line)"; named files and lines in every row | MET. "(lines 16, 23, 30, 36-44, 70, 78, 87)" | MET. "install_skills.py:88-98"; "plan:451, :465" |
| 4.3 | Clear purpose per section | MET. Each block is summarisable in one sentence ("Advisory correctness gaps") | MET. "Advisory:" and "No Regression found" blocks each have one purpose | MET. "Advisory:" and "Notes:" blocks each have one purpose |
| 4.4 | Terms defined on first use | NOT MET. "WC-9", "<OWNER INSTRUCTION>" origin and "AC-1.8" used without a definition line | NOT MET. "G1", "WC-9", "D-P1-5", "lc18" never defined | NOT MET. "lc18", "lc15", "lc13" never defined |
| 4.5 | Actionable next steps / decision points | NOT MET. Rows state defects with a severity but no fix or decision | NOT MET. "matrix trace debt, not a plan defect" classifies; no step | NOT MET. No fix or decision stated |
| | **Subtotal** | **2** | **3** | **2** |

### Dimension 5: Risk Coverage

| # | Criterion | V1 | V2 | V3 |
|---|---|---|---|---|
| 5.1 | >= 3 risks with probability and impact | MET. Rows 1 (HIGH, "can never pass"), 7 (MEDIUM, "cannot hold") and advisory 2 ("would pollute") state likelihood and impact | NOT MET. All 7 rows are LOW/qualitative with impact only; no likelihood language | MET. Rows 1 (HIGH, "exits non-zero"), 2 (MEDIUM, "false FAIL") and advisory 1 ("likely matches ... may fail falsely") |
| 5.2 | Mitigation for each risk | NOT MET. No mitigation stated for any row | NOT MET. None | NOT MET. None |
| 5.3 | Failure modes and recovery | NOT MET. Failure mode stated ("`not run`"), no recovery | NOT MET. Neither | NOT MET. Failure mode stated ("false FAIL"), no recovery |
| 5.4 | External dependencies and failure scenarios | MET. "`--parent-worktree active` may resolve to the Orca UI's active worktree, not the coordinator's" | NOT MET. Row 2 cites `p0-live-orca-help.txt` only as justification; no failure scenario | MET. "`pgrep -af -- '--watch'` likely matches the Bash tool's own shell, so lc18's before/after comparison may fail falsely" |
| 5.5 | Monitoring/validation mechanism | NOT MET. No detection mechanism proposed | MET. "every command line in Tasks 2-24 matches source.md:51-79" and "reviewer verified the plan implements each" document a validation pass | NOT MET. No mechanism proposed |
| | **Subtotal** | **2** | **1** | **2** |

### Dimension 6: Invariant & Edge Case Coverage

| # | Criterion | V1 | V2 | V3 |
|---|---|---|---|---|
| 6.1 | Collection boundaries (empty/single/max) | MET. "pass rule "find output is empty" cannot hold: the branch tracks many return-contract.yaml files" | NOT MET. Searched rows 1-7: no collection boundary | MET. "`find ... -name return-contract.yaml` over a checkout of the branch is never empty because tracked files exist" |
| 6.2 | State interactions across boundaries | MET. "Task 1 requires `git status --porcelain` to show no modified tracked file; ... plan:65 tolerates baseline-modified files" | MET. "the brief's phase header at source.md:70 contradicts lc18's own row (a contract is written)" | MET. "clean-tracked-tree check conflicts with the planned plan-file edit (plan:52) ... and the plan's own no-commit rule (plan:24)" |
| 6.3 | Guard condition gaps | MET. "cmp of "every file under src/superclaude/commands/" includes README.md and __init__.py, which the installer never copies" | NOT MET. No unguarded assumption identified; "No Regression found" asserts none | MET. "No rule normalises the worker's `--report-path` against `<R>/return-contract.yaml`" |
| 6.4 | Count divergence | MET. Source folder files vs installed files: "includes README.md and __init__.py, which the installer never copies" | MET. "seven requirement-bearing spans of source.md have no matrix row" (brief spans vs matrix rows) | MET. "includes README.md and __init__.py, which are not installed" |
| 6.5 | Interaction effects | MET. "a concurrent run would pollute `check --run` and the machine-wide `pgrep`" | NOT MET. "spec 2.1 permits both, so no rule is breached" dismisses the flag combination rather than analysing it | MET. "`pgrep -af -- '--watch'` likely matches the Bash tool's own shell" (tool and check interaction) |
| | **Subtotal** | **5** | **2** | **5** |

### Qualitative summary

| Dimension | V1 | V2 | V3 |
|---|---|---|---|
| 1 Completeness | 2 | 1 | 3 |
| 2 Correctness | 4 | 4 | 2 |
| 3 Structure | 5 | 5 | 5 |
| 4 Clarity | 2 | 3 | 2 |
| 5 Risk Coverage | 2 | 1 | 2 |
| 6 Invariant & Edge Case | 5 | 2 | 5 |
| **Total / 30** | **20** | **16** | **19** |
| **qual_score** | **0.667** | **0.533** | **0.633** |

### Edge Case Floor check (dimension 6 must be >= 1/5)

| Variant | Dim 6 | Eligible as base |
|---|---|---|
| V1 | 5/5 | yes |
| V2 | 2/5 | yes |
| V3 | 5/5 | yes |

No variant is below the floor; no warning needed.

---

## Notes for pass 2 and reconciliation

- Criteria most sensitive to evaluation order or interpretation: 1.1 (strict all-10 reading), 2.1 (any single refuted claim), 2.3 and 2.4 (V3 loses both on the grant-swap withdrawal and IC 0.750), 4.5 and 5.2/5.3 (no card proposes fixes; all NOT MET), 6.2 and 6.4 for V2 (judged MET on one row each).
- Quant gap V1 over V3 comes from SC (0.75 vs 1.0 for V3, counted by blocks) and DC (0.929 vs 0.727); V3 is lower on IC (0.750 vs 0.821). RC ties at 0.800.
- V2 is clean on precision (highest IC and SR, best Clarity 4.1) but lowest on RC (0.400) and Risk/Edge coverage.
