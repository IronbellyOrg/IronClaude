# Scoring Pass 2 (qualitative layer, reverse order V3, V2, V1)

Protocol: `sc-adversarial-protocol/refs/scoring-protocol.md` A.2 (30 criteria, 6 dimensions x 5, binary, Claim-Evidence-Verdict). Quantitative layer not applied. Pass 1 not read.

## Basis and interpretation

- Artifacts scored are the three reviewer cards (deviation-audit tables), not the plan. Each rubric criterion is applied to the card as a review document.
- Debate facts taken as settled: C-001, C-002, C-003, C-005, C-008, U-003, U-004 are real defects; V2's "No Regression found" was refuted; the grant-file swap is not Drift (Necessary or Authorized); U-005 and C-013 did not hold.
- MET needs a quoted passage from the variant. Where none could be quoted the verdict is NOT MET, with the sections searched named.
- Completeness 1 is read as "the card captures the HIGH and MEDIUM established defects C-001, C-002, C-003". No card captures all seven, so a stricter reading would cost V1 and V3 one point each and leave V2 unchanged.
- Risk Coverage 1 accepts the Sev column as impact. It accepts a stated certainty ("cannot hold", "exits non-zero") or a hedge ("likely", "may") as probability.

---

## Dimension 1: Completeness

### V3

| # | Criterion | Claim | Evidence | Verdict |
|---|---|---|---|---|
| 1 | Covers explicit requirements | Captures C-001, C-002, C-003 | #1 "`cmp` of 'every file under src/superclaude/commands/' includes README.md and __init__.py, which are not installed"; #3 "clean-tracked-tree check conflicts with the planned plan-file edit"; #2 "`find ... -name return-contract.yaml` ... is never empty because tracked files exist" | MET |
| 2 | Edge cases / failure scenarios | Describes the failure path | #1 "exits non-zero, install line FAIL, all live tasks `not run`"; Advisory "lc18's before/after comparison may fail falsely" | MET |
| 3 | Dependencies / prerequisites | Notes the gating dependency | #1 "all live tasks `not run` (plan:21, :36)"; #7 "`--parent-worktree active` not re-checked on Orca 1.4.245" | MET |
| 4 | Success / completion criteria | States the pass rule at issue | #1 "install line FAIL"; #2 "false FAIL" | MET |
| 5 | Out of scope stated | States what was not checked | Notes "install_skills.py:88-98 ... (not checked)"; "lc15 omits `--output <file>` and lc13 uses --report-dir; both follow source.md" | MET |

Subtotal 5/5.

### V2

| # | Criterion | Claim | Evidence | Verdict |
|---|---|---|---|---|
| 1 | Covers explicit requirements | Misses C-001, C-002, C-003 | "this reviewer did not find the README.md install-line defect or the Task 23 find defect that reviewers 1 and 3 found"; no row for the clean-tree check | NOT MET |
| 2 | Edge cases / failure scenarios | No failure scenario is described | No evidence found. Searched #1-#7, "No Regression found" paragraph, Advisory. Rows #1-#7 are all LOW classifications with no failing case | NOT MET |
| 3 | Dependencies / prerequisites | No dependency analysis | No evidence found. #2 only cites "spec 7.2 step 1 and WORKER-CONTRACT.md:174" as justification | NOT MET |
| 4 | Success / completion criteria | States a pass rule | #4 "keeps step 3's pass rule and does not require 'step 6 shows nothing written'" | MET |
| 5 | Out of scope stated | Bounds its scan | "No Regression found (every command line in Tasks 2-24 matches source.md:51-79)"; #6 "matrix trace debt, not a plan defect"; Advisory "spec 2.1 permits both, so no rule is breached" | MET |

Subtotal 2/5.

### V1

| # | Criterion | Claim | Evidence | Verdict |
|---|---|---|---|---|
| 1 | Covers explicit requirements | Captures C-001, C-002, C-003 (and C-005, C-008) | #1 "cmp ... includes README.md and __init__.py, which the installer never copies"; #2 "Task 1 requires `git status --porcelain` to show no modified tracked file"; #7 "pass rule 'find output is empty' cannot hold"; #5, #12 | MET |
| 2 | Edge cases / failure scenarios | Describes the failure path | #1 "every live task records `not run: install precondition failed`" | MET |
| 3 | Dependencies / prerequisites | Notes task dependence | Advisory (2) "Live tasks depend only on Task 1; a concurrent run would pollute `check --run` and the machine-wide `pgrep`" | MET |
| 4 | Success / completion criteria | States the pass rule at issue | #7 "pass rule 'find output is empty' cannot hold: ... no pre-run baseline is saved" | MET |
| 5 | Out of scope stated | No scope or not-checked statement | No evidence found. Searched header, table, Advisory. The Advisory lists gaps but excludes nothing | NOT MET |

Subtotal 4/5.

---

## Dimension 2: Correctness

### V3

| # | Criterion | Claim | Evidence | Verdict |
|---|---|---|---|---|
| 1 | No factual errors | Contains errors | #5 "stated reason for dropping the grant file does not explain it" is refuted by plan:52 and APPROVED.md G1; #3 "the modified APPROVED.md" was stale at HEAD 0b443745 | NOT MET |
| 2 | Feasible technical approach | The reasoning is technically sound | #1 cites "src/superclaude/cli/install_commands.py:11, :40" (verified by all advocates); Advisory "`pgrep -af -- '--watch'` likely matches the Bash tool's own shell" (verified) | MET |
| 3 | Terminology accurate | Misapplies a class | #5 labelled "Drift" for a swap that has an inline rationale, which the taxonomy excludes from Drift (line 58) | NOT MET |
| 4 | No internal contradictions | Header and table agree | Header "Regression 1, Drift 4, Necessary 2, Authorized 1" matches rows #1, #2/#3/#5/#6, #4/#7, #8 | MET |
| 5 | Claims supported | Rows carry citations | #1 "src/superclaude/cli/install_commands.py:11, :40; plan:21, :36, :61" | MET |

Subtotal 3/5.

### V2

| # | Criterion | Claim | Evidence | Verdict |
|---|---|---|---|---|
| 1 | No factual errors | Contains a refuted claim | "No Regression found" refuted: the install line returns rc=2 for README.md and `__init__.py` | NOT MET |
| 2 | Feasible technical approach | The audit method cannot find executable defects | "every command line in Tasks 2-24 matches source.md:51-79" is text-to-text only; the card admits "did not find the README.md install-line defect" | NOT MET |
| 3 | Terminology accurate | Misapplies a class | #6 labelled "Drift" while the Finding says "matrix trace debt, not a plan defect"; V2 reclassified it as a process note in Round 2 | NOT MET |
| 4 | No internal contradictions | Header and table agree | Header "Regression 0, Drift 2, Necessary 4, Authorized 1" matches #5/#6, #1-#4, #7 | MET |
| 5 | Claims supported | Rows carry citations | #5 "p1-static-report.md:29"; #1 "source.md:79" | MET |

Subtotal 2/5.

### V1

| # | Criterion | Claim | Evidence | Verdict |
|---|---|---|---|---|
| 1 | No factual errors | Contains stale or unsupported claims | #2 "the tree already had tracked changes (APPROVED.md, plan file)" is stale at HEAD 0b443745; #8 (C-013) rests on a spec clause that does not exist; #2 "the checks conflict" (P:58 v P:65) was withdrawn | NOT MET |
| 2 | Feasible technical approach | The reasoning is technically sound | #1 "src/superclaude/cli/install_commands.py:11 (_EXCLUDE_FILES = {"README.md"}), :40 (glob("*.md"))" | MET |
| 3 | Terminology accurate | Classes match the taxonomy | #4 "Necessary" for the swap; #3 "Drift" for the quoting gap; Regression-class for #1 accepted in debate | MET |
| 4 | No internal contradictions | Header and table agree | Header "Regression 1, Drift 6, Necessary 3, Authorized 2" matches rows #1, #2/#3/#5/#7/#8/#12, #4/#6/#9, #10/#11 | MET |
| 5 | Claims supported | Rows carry citations | #12 ".dev/tasks/done/TASK-WF-writeTheP1Static-.../p1-static-report.md:29" | MET |

Subtotal 4/5.

---

## Dimension 3: Structure

### V3

| # | Criterion | Claim | Evidence | Verdict |
|---|---|---|---|---|
| 1 | Logical ordering | Header, table, Advisory, Notes | Heading, then table, then "Advisory:", then "Notes:" | MET |
| 2 | Consistent hierarchy | One H1, no orphans | Single `#` heading, flat sections | MET |
| 3 | Separation of concerns | Findings, advisory and notes are separate | "Advisory: (1) ... (2) ..." and "Notes: possible further problem ..." are separate paragraphs | MET |
| 4 | Navigation aids | Row numbers and an in-card cross-reference | Row #5 "collides with #3"; `#` column | MET |
| 5 | Follows artifact conventions | Reviewer-card table | "| # | Class | Location | Finding | Evidence | Sev |" with a class-tally header | MET |

Subtotal 5/5.

### V2

| # | Criterion | Claim | Evidence | Verdict |
|---|---|---|---|---|
| 1 | Logical ordering | Header, table, stance, Advisory | Heading, table, "No Regression found ... Notes:", "Advisory:" | MET |
| 2 | Consistent hierarchy | One H1, no orphans | Single `#` heading | MET |
| 3 | Separation of concerns | Advisory is separate | "Advisory: lc15 omits `--output <file>` ..." stands apart | MET |
| 4 | Navigation aids | Only a `#` column and a tally | No evidence found. Searched table and trailing paragraphs; no row cross-reference and no path key | NOT MET |
| 5 | Follows artifact conventions | Reviewer-card table | "| # | Class | Location | Finding | Evidence | Sev |" | MET |

Subtotal 4/5.

### V1

| # | Criterion | Claim | Evidence | Verdict |
|---|---|---|---|---|
| 1 | Logical ordering | Path key before table | "Plan = `.dev/tasks/to-do/TASK-WF-p1LivePlanBrief-.../...md`; brief = `source.md` ..." precedes the table; Advisory follows | MET |
| 2 | Consistent hierarchy | One H1, no orphans | Single `#` heading | MET |
| 3 | Separation of concerns | Advisory is separate | "Advisory correctness gaps: (1) ... (2) ..." | MET |
| 4 | Navigation aids | Path key and `#` column | "Plan = ...; brief = `source.md` in the same folder" lets every `plan:NN` resolve | MET |
| 5 | Follows artifact conventions | Reviewer-card table | Same 6-column table and tally header | MET |

Subtotal 5/5.

---

## Dimension 4: Clarity

### V3

| # | Criterion | Claim | Evidence | Verdict |
|---|---|---|---|---|
| 1 | Unambiguous language | Hedged wording | "`pgrep -af -- '--watch'` likely matches"; "possible further problem"; "so the skills cmp could fail if the branch diff touches one" | NOT MET |
| 2 | Concrete | Specific cites | "install_commands.py:11, :40; plan:21, :36, :61" | MET |
| 3 | One-sentence purpose per section | Labelled sections | Header tally; "Advisory:"; "Notes:" | MET |
| 4 | Terms defined on first use | Undefined terms | No evidence found. "lc18", "Task 23", "AC-1.7", "--report-path" are used without definition | NOT MET |
| 5 | Actionable next steps | No fix or decision step | No evidence found. Searched table and Advisory/Notes; the Sev column ranks but nothing says what to do | NOT MET |

Subtotal 2/5.

### V2

| # | Criterion | Claim | Evidence | Verdict |
|---|---|---|---|---|
| 1 | Unambiguous language | Definite statements | "spec 2.1 permits both, so no rule is breached"; "matrix trace debt, not a plan defect" | MET |
| 2 | Concrete | Specific cites | "seven requirement-bearing spans of source.md ... (lines 16, 23, 30, 36-44, 70, 78, 87)" | MET |
| 3 | One-sentence purpose per section | Labelled sections | Header tally; "Advisory:" | MET |
| 4 | Terms defined on first use | Undefined terms | No evidence found. "lc18", "AC-1.6", "D-P1-5" are undefined | NOT MET |
| 5 | Actionable next steps | No fix or decision step | No evidence found. Searched all rows and the Advisory | NOT MET |

Subtotal 3/5.

### V1

| # | Criterion | Claim | Evidence | Verdict |
|---|---|---|---|---|
| 1 | Unambiguous language | Hedged wording | Advisory (1) "`--parent-worktree active` may resolve to the Orca UI's active worktree" | NOT MET |
| 2 | Concrete | Specific cites | #1 "src/superclaude/cli/install_commands.py:11 ... :40" | MET |
| 3 | One-sentence purpose per section | Labelled sections | Path key line; header tally; "Advisory correctness gaps" | MET |
| 4 | Terms defined on first use | Undefined terms | No evidence found. "AC-1.8", "D-P1-5", "WC-9" are undefined (only plan and brief are keyed) | NOT MET |
| 5 | Actionable next steps | No fix or decision step | No evidence found. Searched table and Advisory | NOT MET |

Subtotal 2/5.

---

## Dimension 5: Risk Coverage

### V3

| # | Criterion | Claim | Evidence | Verdict |
|---|---|---|---|---|
| 1 | At least 3 risks with probability and impact | Three | #1 HIGH, certain ("exits non-zero"); #2 MEDIUM, certain ("never empty"); Advisory (1) "likely matches ... may fail falsely" | MET |
| 2 | Mitigation for each | None given | No evidence found. Searched table, Advisory, Notes | NOT MET |
| 3 | Failure modes and recovery | Failure path and the plan's fallback | #1 "install line FAIL, all live tasks `not run` (plan:21, :36)" | MET |
| 4 | External dependencies | Orca and installer | #7 "`--parent-worktree active` not re-checked on Orca 1.4.245"; #1 installer `install_commands.py` | MET |
| 5 | Monitoring or validation mechanism | Examines the plan's detection mechanism | Advisory "lc18's before/after comparison may fail falsely" | MET |

Subtotal 4/5.

### V2

| # | Criterion | Claim | Evidence | Verdict |
|---|---|---|---|---|
| 1 | At least 3 risks with probability and impact | No risks, only LOW classifications | No evidence found. Searched #1-#7: every Sev is LOW and none states a failing outcome | NOT MET |
| 2 | Mitigation for each | None | No evidence found | NOT MET |
| 3 | Failure modes and recovery | None | No evidence found | NOT MET |
| 4 | External dependencies | None with a failure scenario | No evidence found. #2 cites "p0-live-orca-help.txt:49,69" only as justification | NOT MET |
| 5 | Monitoring or validation mechanism | None for risk detection | No evidence found. Its own check ("every command line ... matches") is a fidelity comparison, shown ineffective for risk | NOT MET |

Subtotal 0/5.

### V1

| # | Criterion | Claim | Evidence | Verdict |
|---|---|---|---|---|
| 1 | At least 3 risks with probability and impact | Three | #1 HIGH "can never pass"; #7 MEDIUM "cannot hold"; Advisory (2) "a concurrent run would pollute `check --run` and the machine-wide `pgrep`" | MET |
| 2 | Mitigation for each | None given | No evidence found. Searched table and Advisory | NOT MET |
| 3 | Failure modes and recovery | Failure path and the plan's fallback | #1 "every live task records `not run: install precondition failed`" | MET |
| 4 | External dependencies | Orca selector | Advisory (1) "`--parent-worktree active` may resolve to the Orca UI's active worktree"; cites "p0-live-orca-help.txt:36,49,69" | MET |
| 5 | Monitoring or validation mechanism | Examines the plan's detection mechanism | Advisory (2) "`check --run` and the machine-wide `pgrep`" | MET |

Subtotal 4/5.

---

## Dimension 6: Invariant and Edge Case Coverage

### V3

| # | Criterion | Claim | Evidence | Verdict |
|---|---|---|---|---|
| 1 | Collection boundaries | Empty-set expectation fails | #2 "`find ... -name return-contract.yaml` ... is never empty because tracked files exist; the plan saves no pre-run find to subtract" | MET |
| 2 | State interactions across components | Check collides with the planned edit and no-commit rule | #3 "clean-tracked-tree check conflicts with the planned plan-file edit (plan:52), the modified APPROVED.md, and the plan's own no-commit rule (plan:24)" | MET |
| 3 | Guard condition gaps | Guard cannot pass; missing normalisation | #1 install-line guard includes uninstalled files; Advisory (2) "No rule normalises the worker's `--report-path` against `<R>/return-contract.yaml`" | MET |
| 4 | Count / inclusive-exclusive divergence | Source set is wider than installed set | #1 "`cmp` of 'every file under src/superclaude/commands/' includes README.md and __init__.py, which are not installed" | MET |
| 5 | Interaction effects | Feature combination | #5 "the swap forces a plan edit that collides with #3" | MET |

Subtotal 5/5.

### V2

| # | Criterion | Claim | Evidence | Verdict |
|---|---|---|---|---|
| 1 | Collection boundaries | None | No evidence found. Searched all rows | NOT MET |
| 2 | State interactions across components | None | No evidence found | NOT MET |
| 3 | Guard condition gaps | Brief's guard contradicts lc18 | #4 "does not require 'step 6 shows nothing written'; the brief's phase header at source.md:70 contradicts lc18's own row (a contract is written)" | MET |
| 4 | Count divergence | Spans versus matrix rows | #6 "seven requirement-bearing spans of source.md ... have no matrix row" | MET |
| 5 | Interaction effects | None | No evidence found. #7 lists additions but not how they combine | NOT MET |

Subtotal 2/5.

### V1

| # | Criterion | Claim | Evidence | Verdict |
|---|---|---|---|---|
| 1 | Collection boundaries | Empty-set expectation fails | #7 "pass rule 'find output is empty' cannot hold: the branch tracks many return-contract.yaml files ...; no pre-run baseline is saved" | MET |
| 2 | State interactions across components | Tracked-tree check versus the plan's own state | #2 "Task 1 requires `git status --porcelain` to show no modified tracked file; the tree already had tracked changes"; Advisory (2) concurrent runs pollute shared `pgrep` | MET |
| 3 | Guard condition gaps | Guard cannot pass | #1 "the install line can never pass and every live task records `not run`" | MET |
| 4 | Count / inclusive-exclusive divergence | Source set is wider than installed set | #1 "includes README.md and __init__.py, which the installer never copies" | MET |
| 5 | Interaction effects | Edit versus check | #2 "plan:58, :61, :65 ... checks conflict" together with the plan edit at P:52 | MET |

Subtotal 5/5. (The "checks conflict" and "tree already dirty" wording was later withdrawn or called stale. The point that the P:52 edit collides with the clean-tree check survived, so the verdict stands.)

---

## Subtotals and totals

| Dimension | V1 | V2 | V3 |
|---|---|---|---|
| Completeness | 4 | 2 | 5 |
| Correctness | 4 | 2 | 3 |
| Structure | 5 | 4 | 5 |
| Clarity | 2 | 3 | 2 |
| Risk Coverage | 4 | 0 | 4 |
| Invariant & Edge Case | 5 | 2 | 5 |
| **Total / 30** | **24** | **13** | **24** |
| qual_score | 0.800 | 0.433 | 0.800 |

## Edge Case Floor check (>= 1/5 on Invariant & Edge Case Coverage)

| Variant | Score | Eligible as base |
|---|---|---|
| V1 | 5/5 | Yes |
| V2 | 2/5 | Yes (passes the floor, but with the lowest score) |
| V3 | 5/5 | Yes |

## Notes for the merge

- V1 and V3 tie at 24/30. The tiebreak sits with the quantitative layer or the debate-performance rule.
- Where they differ:
  - V3 has a clean Completeness 5/5. It also holds U-003 and U-004, and V1 has neither. Its two losses are the Drift mislabel of the grant-file swap and the stale "modified APPROVED.md".
  - V1 has the correct swap class and the correct plan-versus-brief wording. It also holds C-008, which V3 lacks. Its losses are stale or unsupported claims (C-013, "tree already dirty") and no out-of-scope statement.
- V2 is the most precise card but has the lowest recall. Its "No Regression found" error is the only refuted headline claim in the set.
- Strengths worth carrying forward from V2: C-009, C-010 (as a process note), U-006, and its correct Necessary class for the swap.
