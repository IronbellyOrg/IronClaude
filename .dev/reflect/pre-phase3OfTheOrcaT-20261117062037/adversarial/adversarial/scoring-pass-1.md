# Qualitative scoring, pass 1 (V1, V2, V3)

Basis: the three variant cards, debate-transcript.md (Round 2 final rulings), round-2-v3.md (final candidate list). Final rulings used as ground truth: C-001/C-002/C-003 BLOCKING (C-001 Gap, C-002 Regression, C-003 Gap); C-004/005/006/009/011/012/013 MEDIUM; C-007/008/010/014/015 NOTE. Static reading only; no tests run.

## Summary

| Variant | Completeness | Correctness | Structure | Clarity | Risk | Invariant/edge | Total /30 | Edge floor (>=1/5) |
|---|---|---|---|---|---|---|---|---|
| V1 | 4 | 5 | 5 | 4 | 5 | 5 | 28 | pass |
| V2 | 5 | 3 | 5 | 4 | 5 | 4 | 26 | pass |
| V3 | 5 | 3 | 5 | 4 | 5 | 4 | 26 | pass |

## V1 (analyzer, sonnet)

### Completeness (4/5)
1. Covers requirements. CLAIM: names uncovered requirements. EVIDENCE: "uncovered_requirements: INF-001 ... INF-009 ... INF-013" and the long `checked` list. MET.
2. Edge cases. EVIDENCE: F2 (first `n` press cannot be gated on `view.desk`), F4 (desk collapses the list), F5 (`unknown` sentinel). MET.
3. Dependencies/prerequisites. CLAIM: names ordering or prerequisite dependencies. EVIDENCE: none; fields to add are named (F2, F4) but no task ordering or prerequisite is stated. NOT MET.
4. Success criteria for fixes. EVIDENCE: F1 "add a test_commands test that `--once` with a linked reply gives `dispatchId=` and `link=linked` in the record and a screen showing the ask text". MET.
5. Out of scope/not checked. EVIDENCE: "No tests run." plus the list of what was read and confirmed. MET (marginal).

### Correctness (5/5)
1. No factual errors. EVIDENCE: F1, F4, F5, F8 (HELP string, not docstring) all match the debate rulings; severity under-grades (F3, F6) were conceded, but the facts hold. MET.
2. Feasible approaches. EVIDENCE: F4 "compute desk height first, replace it with the one-line notice when spare would fall below 1, never remove the list". MET.
3. Terminology. EVIDENCE: F8 correctly says "HELP string". MET.
4. No contradictions. EVIDENCE: none found; verdict FAIL is consistent with the BLOCKING F1. MET.
5. Evidence-supported. EVIDENCE: file:line citations in every finding, e.g. "render.py:304-323, 369-395". MET.

### Structure (5/5)
1. Ordering: findings run in plan-task order within severity, notes last. MET.
2. Hierarchy: the same field set in every finding. MET.
3. Separation: findings, uncovered_requirements and checked are separate blocks. MET.
4. Navigation: F-ids and INF-ids, with "(F1)" cross-references. MET.
5. Required card format: persona, model_class, verdict, confidence, findings, uncovered_requirements, checked. MET.

### Clarity (4/5)
1. Unambiguous. EVIDENCE: plan_says/reality/wrong_outcome/fix per finding. MET.
2. Concrete. EVIDENCE: "about 107 chars; ... about 121 chars = 2 lines at width 116 or 120". MET.
3. Clear purpose per finding. MET.
4. Terms defined on first use. EVIDENCE: INF-xxx, "UNKNOWN sentinel", "spare", "[INFERRED]" are never defined. NOT MET.
5. Actionable next steps. EVIDENCE: every F has a `fix:`. MET.

### Risk coverage (5/5)
1. At least 3 risks with severity and impact. EVIDENCE: F1 BLOCKING, F2-F6 MEDIUM, each with wrong_outcome. MET.
2. Fix for each. EVIDENCE: `fix:` on F1-F8. MET.
3. Failure modes and recovery. EVIDENCE: F4 wrong_outcome, with a degrade-without-losing-the-list fix. MET.
4. External dependencies/failure. EVIDENCE: F5 (absent or sentinel id from source), F7 (malformed payload dispatchId). MET.
5. Detection. EVIDENCE: F1 `--once` test; F6 "assert only the `questions` group plus byte-identity with the link-off snapshot". MET.

### Invariant and edge-case coverage (5/5)
1. Collection boundaries. EVIDENCE: F4 "spare >= 1 else the whole panel collapses". MET.
2. State interactions across components. EVIDENCE: F2 "CycleResult ..., Session and View carry no link field". MET.
3. Guard-condition gaps. EVIDENCE: F2 (gating `n` on `view.desk is not None`); F5 "UNKNOWN is a truthy sentinel". MET.
4. Count divergence. EVIDENCE: F3 "about 107 chars ... about 121 chars = 2 lines at width 116 or 120; ... `spare` drops one". MET.
5. Interaction effects. EVIDENCE: F3 (link off with questions on); F4 (desk height against list). MET.

Total V1 = 28/30. Edge floor: 5/5, eligible.

## V2 (qa, haiku)

### Completeness (5/5)
1. Requirements. EVIDENCE: uncovered INF-001/007/008/010/013 plus "INF-002 has explicit malformed and missing payload checks ... INF-011 covered by Tasks 1 and 7". MET.
2. Edge cases. EVIDENCE: F4 missing worker fields, stale or failed worker read. MET.
3. Dependencies. EVIDENCE: "the new question_message builder is created before its dependents; declared dependencies have no ordering defect". MET.
4. Success criteria. EVIDENCE: F3 "add a byte-for-byte link-off screen comparison with questions enabled at all three widths". MET.
5. Not checked/out of scope. EVIDENCE: "No commands run."; "INF-009 is not untested: ...". MET (marginal).

### Correctness (3/5)
1. No factual errors. EVIDENCE: F1 "a linked question necessarily shares its dispatch id with one of those rows" is overstated, since a linked question whose worker is absent can pass (V2 conceded); confidence 0.97 was ruled too high. NOT MET.
2. Feasible. EVIDENCE: F1 fix limits the exclusion to the `questions` group, which V3 adopted. MET.
3. Terminology. EVIDENCE: F1 is labelled "Regression"; the final ruling is Gap (V2 conceded). NOT MET.
4. No contradictions. MET.
5. Evidence-supported. EVIDENCE: "export.py:26 ... line 195", "view.py:914". MET.

### Structure (5/5)
1. Ordering: BLOCKING first, then MEDIUM. MET.
2. Hierarchy. MET.
3. Separation. MET.
4. Navigation. EVIDENCE: F-ids, INF-ids, "(F2)" cross-references. MET.
5. Format. MET.

### Clarity (4/5)
1. Unambiguous. MET.
2. Concrete. EVIDENCE: F2 "lines 224-230 choose between a width-bound screen and record_text". MET.
3. Purpose. MET.
4. Terms defined. EVIDENCE: "R1 surface" and INF-xxx are undefined. NOT MET.
5. Actionable. EVIDENCE: each F has a concrete `fix:`. MET.

### Risk coverage (5/5)
1. At least 3 risks with severity and impact. EVIDENCE: 3 BLOCKING + 1 MEDIUM with wrong_outcome. MET.
2. Fix each. MET.
3. Failure modes. EVIDENCE: F1 "executor removes worker identifiers (weakening the snapshot contract) or leaves the matching worker out of the test". MET.
4. External failure. EVIDENCE: F4 "failed or stale worker-read cases asserting the freshness qualification". MET.
5. Detection. EVIDENCE: F2 command-level tests with a distinctive synthetic payload. MET.

### Invariant and edge-case coverage (4/5)
1. Boundary conditions. EVIDENCE: F3 "all three widths". MET.
2. State interactions. EVIDENCE: F2 (command wiring to Collector default `link=False`); F1 (snapshot vs worker rows). MET.
3. Guard gaps. EVIDENCE: F3 "view.py:914 selects QUESTIONS_KEYS_LINE whenever a question panel exists, independent of the link switch". MET.
4. Count divergence. EVIDENCE: only "its length can alter wrapping and the height budget", with no numbers. NOT MET.
5. Interaction effects. EVIDENCE: F3 "questions on and link off". MET.

Total V2 = 26/30. Edge floor: 4/5, eligible.

## V3 (refactorer, opus)

### Completeness (5/5)
1. Requirements. EVIDENCE: "INF-001 partly ... INF-007 narrowed ..." plus a `checked` list covering the spec corpus (AD-18, T50-T56). MET.
2. Edge cases. EVIDENCE: F2 (first `n` selection), F9 "evicted selected identity shows `selected <id> no longer in source window`". MET.
3. Dependencies. EVIDENCE: F4 "Task 6 depends only on 4a"; F8 shared conftest helper. MET.
4. Success criteria. EVIDENCE: F1 "add a test_commands check that --once with a payload reply prints link=linked". MET.
5. Not checked. EVIDENCE: "Not checked: rows T57 to T66 and unverified-register.md line 33"; deliberate omissions are listed. MET (the line 33 claim itself is wrong, scored under Correctness).

### Correctness (3/5)
1. No factual errors. EVIDENCE: "unverified-register.md line 33 (they exist only after execution)" is wrong (line 33 exists now); "INF-009: only a constraint" is wrong because test_commands.py:652-667 pins the argv; both conceded. NOT MET.
2. Feasible. EVIDENCE: F4 split into 4a/4b; F8 `payload=` arguments on `make_question_rows`. MET.
3. Terminology. EVIDENCE: F5 is labelled "Drift"; the final ruling is Gap (conceded). NOT MET.
4. No contradictions. MET.
5. Evidence-supported. EVIDENCE: F6 quotes AD-18 `[ADOPTED]` at ARCHITECTURE-SPINE.md:178, 285. MET.
Note: F7's fix (update the pinned assertion at test_commands.py:740) and F5's fix ("drop that clause") were conceded as weaker or wrong. They count against criterion 1, not as separate deductions.

### Structure (5/5)
1. Ordering. MET.
2. Hierarchy. MET.
3. Separation. MET.
4. Navigation. EVIDENCE: F1-F12, INF ids, spec file:line references. MET.
5. Format. MET.

### Clarity (4/5)
1. Unambiguous. MET.
2. Concrete. EVIDENCE: F4 "one task changes five types or functions and two test files with about 13 pinned behaviours". MET.
3. Purpose. MET.
4. Terms defined. EVIDENCE: "AD-18", "CAP-12", "Stage C" and INF-xxx are undefined. NOT MET.
5. Actionable. EVIDENCE: F6 "add to Task 7 an edit of AD-18 and line 285". MET.

### Risk coverage (5/5)
1. At least 3 risks with severity and impact. MET.
2. Fix each. EVIDENCE: F1-F12 all carry a fix. MET.
3. Failure modes/recovery. EVIDENCE: F4 "too big to review or roll back as one unit". MET.
4. External dependencies. EVIDENCE: F8 observed recorded message-row shape; F10 optional owner re-confirm. MET (marginal).
5. Detection. EVIDENCE: F1 test_commands check; F8 never-kept test. MET.

### Invariant and edge-case coverage (4/5)
1. Boundary conditions. EVIDENCE: F9 evicted selection; F2 first `n`. MET.
2. State interactions. EVIDENCE: F2 "CycleResult has no link field ... View.desk exists only once a question is selected". MET.
3. Guard gaps. EVIDENCE: F3 "QUESTIONS_KEYS_LINE is used whenever the question panel exists; with link off the footer advertises dead n/p keys". MET.
4. Count divergence. EVIDENCE: no off-by-one or cap count is given; "about 13 pinned behaviours" is a size estimate. NOT MET.
5. Interaction effects. EVIDENCE: F5 "dispatchId appears through the workers array, so the 'no dispatch id' assertion fails on a natural fixture". MET.

Total V3 = 26/30. Edge floor: 4/5, eligible.

## Notes for the merge
- V1 is strongest on measured edge cases (F3 character counts, F4 collapse, F2 first-press gate) but under-graded F3 and F6.
- V2 has the best severity grading and the best C-002 test, but overstates F1 and lacks counts.
- V3 is the broadest, with the only AD-18, rendering-rules and conftest findings, but carries three conceded errors (register line 33, INF-009, the F7 fix) and the weaker F5 fix.
