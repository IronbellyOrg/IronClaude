# Scoring Pass 1 (input order: Variant 1, Variant 2, Variant 3)

- Step 3, hybrid scoring and base selection, evaluator pass 1. Algorithm: `~/.claude/skills/sc-adversarial-protocol/refs/scoring-protocol.md` (A.1 to A.4).
- Inputs read: `diff-analysis.md`, `debate/round2-advocate-3.md` section 3, `invariant-probe.md`, `variant-1-original.md`, `variant-2-original.md`, `variant-3-original.md`. No other scoring-pass file was read.
- Ground truth for correctness (settled by the debate): blocking C-001, C-002; minor C-003 to C-009, C-011, C-013, C-014, N-1; dropped C-010, C-012, C-015, S-001, S-002, X-001, X-003; probe MEDIUM items INV-006, INV-007, INV-008, INV-012, INV-017.
- Card ownership of the settled items: V1 raised C-001 to C-009 (all kept). V2 raised C-001, C-011 (kept) and C-010, C-012 (dropped); its labels produce S-002 and X-003 (dropped as card defects, scored here under consistency). V3 raised C-001, C-003, C-006, C-009, C-013, C-014 (kept) and C-015 (dropped); its verdict "files ... end up consistent" was conceded wrong for one pair (X-002 folded into C-006). No card raised any probe MEDIUM item.

## Quantitative method (applied identically to all three)

- **RC**: 12 review-coverage items. R1 to R7 = Tasks 1 to 7 each addressed by a finding or a Checked statement. R8 = earlier-review findings F3/F4/F5/F6/F9/F12/F13 checked. R9 = Tasks 1 to 6 compared with base Tasks 41 to 46. R10 = step-by-step walk of Task 6's order. R11 = coverage matrix checked against the source request. R12 = grading done on the stated rule (blocking/minor) without a second scale.
- **IC**: scorable claims = finding rows plus specific Checked/Notes/verdict claims; contradiction = two statements in the same card about the same subject that disagree.
- **SR**: statements = finding rows, bullet lines and full-sentence lines (grep `^(F[0-9]|D[0-9]|- |  - |[A-Z][a-z].*\.$)`); concrete = those with a number, backtick literal or quote; vague = hits of appropriate / as needed / properly / adequate / should consider / might / various / etc / may / possibly / perhaps. SR = concrete / (concrete + vague).
- **DC**: internal references = card-local abbreviation keys (P4, OLD, plan, stage1/stage3 plan) and cross-references to the card's own finding ids. Test ids from the stage 1 plan (T1, T2, T3, T15), spec ids (FR-8, L1, INF-002) and earlier-review ids (F3...F13 in V2) are external and excluded.
- **SC**: H2 count / max H2 count (max = 5, V2).

---

## Variant 1 (reviewer 1, analyzer, sonnet class)

### Quantitative

| Metric | Value | Computation |
|---|---|---|
| RC | 0.583 | 7/12. Met: R1 (F1, F3, F8), R2 (Checked "the four rule prompts at lines 11, 27, 27 and 28"), R3 (F4), R4 (F9, Checked `grep -c` prints 1), R5 (F2, F5, F7), R6 (F2 "Task 6 runs three"; Checked plan:104), R12 (MAJOR/blocking agree on every row). Not met: R7 (Task 7 never named), R8, R9, R10, R11. |
| IC | 1.000 | 0 contradictions / ~20 claims. Verdict "two blocking defects" = F1, F2; Checked "Task 1's first check (plan:36) is meetable" does not conflict with F1 (line 2). |
| SR | 1.000 | 20 concrete / (20 + 0 vague). |
| DC | 0.750 | 3/4 resolve: `plan` (full path in F1), `stage3 plan` (full path in F1), "the mapping test" (defined in F2); `stage1 plan` (F7, Checked) has no path anywhere in the card. |
| SC | 0.800 | 4 H2 / 5. |
| **quant** | **0.808** | 0.30(0.583) + 0.25(1.000) + 0.15(1.000) + 0.15(0.750) + 0.15(0.800) = 0.175 + 0.250 + 0.150 + 0.113 + 0.120 |

### Qualitative (CEV: claim | evidence | verdict)

**Completeness (2/5)**

| # | Claim | Evidence | Verdict |
|---|---|---|---|
| 1 | All 12 coverage items covered | RC 7/12; no Task 7, base-task, earlier-finding, matrix or Task 6 walk text | NOT MET |
| 2 | Edge/failure scenarios | F8 "A missing go still halts the run, but only after the edits exist" | MET |
| 3 | Dependencies/prerequisites | F2 "The stage 3 plan edits no spec-panel text ... So stage 4 must make the change" | MET |
| 4 | Success/completion criteria | No fix or done condition stated; searched Verdict, Findings, Checked | NOT MET |
| 5 | Out of scope stated | No scope or not-checked statement; searched all sections | NOT MET |

**Correctness (5/5)**

| # | Claim | Evidence | Verdict |
|---|---|---|---|
| 1 | No factual errors vs settled findings | F1 to F9 map to C-001 to C-009, all kept by the debate; none dropped | MET |
| 2 | Approaches feasible | F2 "So stage 4 must make the change" matches the settled C-002 fix (Task 5 re-pins MAP) | MET |
| 3 | Terminology consistent | Every row "MAJOR \| blocking true" or "MINOR \| blocking false" | MET |
| 4 | No internal contradictions | IC = 1.000 | MET |
| 5 | Claims evidenced | Every F row ends with "citations:" and quoted lines, e.g. F6 `test_review_brief_placement.py:134` | MET |

**Structure (4/5)**

| # | Claim | Evidence | Verdict |
|---|---|---|---|
| 1 | Logical order | Verdict, Findings, Checked, Self-report | MET |
| 2 | Consistent hierarchy | H2 only, no orphan subsections | MET |
| 3 | Separation of concerns | Defects only in Findings; Checked holds only meetable checks | MET |
| 4 | Navigation aids | No cross-reference between findings or sections; searched all | NOT MET |
| 5 | Artifact conventions | F-line format, Checked, Self-report with confidence | MET |

**Clarity (4/5)**

| # | Claim | Evidence | Verdict |
|---|---|---|---|
| 1 | Unambiguous language | 0 hits of should consider / might / as appropriate | MET |
| 2 | Concrete | Checked "agent_template_qa.md 85/158/161/333" | MET |
| 3 | Section purpose | Verdict "two blocking defects ... Everything else is minor" | MET |
| 4 | Terms defined on first use | "stage1 plan", "T3", "FR-8" used undefined (F5, F7) | NOT MET |
| 5 | Actionable next step | F2 "So stage 4 must make the change" | MET |

**Risk coverage (2/5)**

| # | Claim | Evidence | Verdict |
|---|---|---|---|
| 1 | 3+ risks with probability and impact | Impact given ("Wrong result:"), no probability anywhere | NOT MET |
| 2 | Mitigation per risk | No fix line on any F row | NOT MET |
| 3 | Failure modes and recovery | F1 "The run halts at Task 1, or QA passes it on a guess"; no recovery | NOT MET |
| 4 | External dependencies | F2 "its own acceptance needs this test green with spec-panel unchanged" (stage 3) | MET |
| 5 | Validation mechanism | F6 "pinning tests that cover edited files are never run in stage 4" | MET |

**Invariant and edge case (5/5)**

| # | Claim | Evidence | Verdict |
|---|---|---|---|
| 1 | Collection boundaries | Checked "Task 6's grep (plan:104) can print nothing"; "`grep -c` prints 1" | MET |
| 2 | State across components | F6 plugin prompt "byte-identical to the source, but Task 5 says edit each file in place" | MET |
| 3 | Guard gaps | F7 "The `pointer-only` check in T3 passes without a pointer, so nothing forces it" | MET |
| 4 | Count divergence | Checked "11 files hold ... matching the 11 `digest` rows" | MET |
| 5 | Interaction effects | F2 Task 5 edit x mapping test x stage 3 acceptance | MET |

**Subtotals V1:** completeness 2, correctness 5, structure 4, clarity 4, risk 2, invariant 5 = **22/30, qual 0.733**. Edge-case floor: 5/5, eligible.

---

## Variant 2 (reviewer 2, qa, haiku class)

### Quantitative

| Metric | Value | Computation |
|---|---|---|
| RC | 0.833 | 10/12. Met: R1 to R7 ("41 -> 1" to "46 -> 6" and "Task 7: Adds the requested owner summary"), R8 ("Earlier stage-4 findings checked": F3/F9, F4, F5/F12, F6, F13), R9 ("Base Tasks 41–46 comparison"), R11 (D4 on `coverage-matrix.yaml:10-12`). Not met: R10 (only "registration -> allow-list -> copy -> combined-test order", no step walk), R12 (second scale "Table severity: MEDIUM/LOW" next to MAJOR/MINOR). |
| IC | 0.909 | 2 contradictions / ~22 claims: D1 "MAJOR; blocking true" vs "Table severity: MEDIUM"; D2 same pair. |
| SR | 0.955 | 21 concrete / (21 + 1 vague: "may" in D2). |
| DC | 0.800 | 4/5 resolve: P4 (orchestrator comment), D1, D2, D3; `OLD:486-552` undefined. |
| SC | 1.000 | 5 H2 / 5. |
| **quant** | **0.890** | 0.250 + 0.227 + 0.143 + 0.120 + 0.150 |

### Qualitative (CEV)

**Completeness (4/5)**

| # | Claim | Evidence | Verdict |
|---|---|---|---|
| 1 | All 12 coverage items covered | RC 10/12; no Task 6 step walk | NOT MET |
| 2 | Edge/failure scenarios | D2 "The audit may genuinely pass while this acceptance line still fails" | MET |
| 3 | Dependencies/prerequisites | "41 -> 1: Removed the cross-package Task 40 dependency" | MET |
| 4 | Success/completion criteria | "Spec units audited: 17 ... Fully adherent ... 14" | MET |
| 5 | Out of scope stated | "No files changed and no tests were run. Execution results ... were not available" | MET |

**Correctness (1/5)**

| # | Claim | Evidence | Verdict |
|---|---|---|---|
| 1 | No errors vs settled findings | D1 "MAJOR; blocking true" is C-010, dropped; D4 is C-012, dropped; C-002 blocking missed | NOT MET |
| 2 | Approaches feasible | D1's implied remedy (generate later) cannot be made by any plan edit (settled drop reason, R2-A3 C-010) | NOT MET |
| 3 | Terminology consistent | MAJOR/MINOR and MEDIUM/LOW on the same rows (S-002) | NOT MET |
| 4 | No internal contradictions | D1 "MAJOR; blocking true" vs "Table severity: MEDIUM" (X-003) | NOT MET |
| 5 | Claims evidenced | Each D row has "Evidence:" with quotes, e.g. D2 "same file:162" | MET |

**Structure (3/5)**

| # | Claim | Evidence | Verdict |
|---|---|---|---|
| 1 | Logical order | Verdict, Deviations, Adherence summary, Notes, Self-report | MET |
| 2 | Consistent hierarchy | H2 sections; two H3 only under Notes | MET |
| 3 | Separation of concerns | Notes holds an unlisted finding: Task 7 "a minor ordering ambiguity" | NOT MET |
| 4 | Navigation aids | "Finding D2", "Finding D3" cross-references in Notes | MET |
| 5 | Artifact conventions | "used the deviation-table format instead of the F-line format" | NOT MET |

**Clarity (4/5)**

| # | Claim | Evidence | Verdict |
|---|---|---|---|
| 1 | Unambiguous language | 0 hits of should consider / might / as appropriate | MET |
| 2 | Concrete | D4 "Location: artifacts/coverage-matrix.yaml:10-12" | MET |
| 3 | Section purpose | Verdict "The plan needs revision before execution" | MET |
| 4 | Terms defined | "OLD", "INF-002", "T3", "F12" undefined | NOT MET |
| 5 | Actionable next step | Verdict "needs revision before execution" | MET |

**Risk coverage (2/5)**

| # | Claim | Evidence | Verdict |
|---|---|---|---|
| 1 | 3+ risks with probability and impact | Severity only, no probability | NOT MET |
| 2 | Mitigation per risk | No fix on any D row | NOT MET |
| 3 | Failure modes and recovery | D2 failure stated; no recovery path | NOT MET |
| 4 | External dependencies | "Actual T3 implementation remains an earlier-stage prerequisite, not verified" | MET |
| 5 | Validation mechanism | D3 "provide no cap-content pin" | MET |

**Invariant and edge case (4/5)**

| # | Claim | Evidence | Verdict |
|---|---|---|---|
| 1 | Collection boundaries | No empty/single/max case; searched Deviations, Notes | NOT MET |
| 2 | State across components | D2 "Stage 3 produces the summary before that window" | MET |
| 3 | Guard gaps | D3 "provide no cap-content pin" | MET |
| 4 | Count divergence | "Spec units audited: 17 — the matrix's 16 inferred units plus the omitted" | MET |
| 5 | Interaction effects | "registration -> allow-list -> copy -> combined-test order in P4:99-102" | MET |

**Subtotals V2:** completeness 4, correctness 1, structure 3, clarity 4, risk 2, invariant 4 = **18/30, qual 0.600**. Edge-case floor: 4/5, eligible.

---

## Variant 3 (reviewer 3, refactorer, opus class)

### Quantitative

| Metric | Value | Computation |
|---|---|---|
| RC | 0.667 | 8/12. Met: R1 (F1, F5), R2 ("Task 2 after Task 1"), R3 (F4, "Task 3 has no Depends on line"), R4 (F4), R5 ("Task 5 after Task 2"), R6 (F2, F3, walk), R10 ("Task 6, step by step"), R12 (MAJOR/blocking agree). Not met: R7 ("Step 7" is Task 6's step; Task 7 not named), R8, R9, R11. |
| IC | 1.000 | 0 contradictions / ~20 claims. Verdict counts (1 unmeetable, 1 vacuous, 3 minor) match F1, F2, F3 to F5. |
| SR | 0.913 | 21 concrete / (21 + 2 vague: "may" in F3, F5). |
| DC | 0.500 | 2/4 resolve: F2, F3 (Step 7); `P4` (P4:99, P4:39) and `OLD` (OLD:477) are never defined in the card. |
| SC | 0.800 | 4 H2 / 5. |
| **quant** | **0.782** | 0.200 + 0.250 + 0.137 + 0.075 + 0.120 |

### Qualitative (CEV)

**Completeness (4/5)**

| # | Claim | Evidence | Verdict |
|---|---|---|---|
| 1 | All 12 coverage items covered | RC 8/12 | NOT MET |
| 2 | Edge/failure scenarios | Step 4 "The 'repeat the copy' clause covers the case where it does change something" | MET |
| 3 | Dependencies/prerequisites | "Depends on lines: Task 2 after Task 1 ... are all correct" | MET |
| 4 | Success/completion criteria | F2 "Fix: stage `plugins/superclaude/skills/sc-review-severity/` before running the three tests" | MET |
| 5 | Out of scope stated | "Not checked: the spec section 10.5 cap lines and the exact L1 merge text" | MET |

**Correctness (4/5)**

| # | Claim | Evidence | Verdict |
|---|---|---|---|
| 1 | No errors vs settled findings | F4 first half is C-015, dropped; Verdict "files edited by several tasks end up consistent" conceded wrong (X-002); C-002 missed | NOT MET |
| 2 | Approaches feasible | F2 fix accepted as the settled C-013 remedy (R2-A3 row 3) | MET |
| 3 | Terminology consistent | Every row "MAJOR \| blocking true" or "MINOR \| blocking false" | MET |
| 4 | No internal contradictions | IC = 1.000 | MET |
| 5 | Claims evidenced | F2 cites `tests/skills/test_review_severity_rule.py:39` with quote | MET |

**Structure (5/5)**

| # | Claim | Evidence | Verdict |
|---|---|---|---|
| 1 | Logical order | Verdict, Findings, Checked, Self-report | MET |
| 2 | Consistent hierarchy | H2 only; bold sub-labels inside Checked | MET |
| 3 | Separation of concerns | Defects in Findings; walk and end states in Checked | MET |
| 4 | Navigation aids | Step 7 "no failure expected apart from F2 and F3" | MET |
| 5 | Artifact conventions | F-line format, Checked, Self-report with confidence | MET |

**Clarity (4/5)**

| # | Claim | Evidence | Verdict |
|---|---|---|---|
| 1 | Unambiguous language | 0 hits of should consider / might / as appropriate | MET |
| 2 | Concrete | "stage 3 lists 8 paths; Task 1 removes 2, Task 3 removes 4" | MET |
| 3 | Section purpose | Verdict "One check cannot be met ... One check passes without testing anything" | MET |
| 4 | Terms defined | "P4", "OLD", "T1", "T15" undefined | NOT MET |
| 5 | Actionable next step | F2 "Fix: stage ... or make T2 read the filesystem" | MET |

**Risk coverage (3/5)**

| # | Claim | Evidence | Verdict |
|---|---|---|---|
| 1 | 3+ risks with probability and impact | No probability anywhere | NOT MET |
| 2 | Mitigation per risk | Fix only on F2 | NOT MET |
| 3 | Failure modes and recovery | F1 "The run halts in Task 1 ... The owner's go row in the ledger is the record that exists after the window" | MET |
| 4 | External dependencies | "Tests from stages 1 to 3 do not exist yet, so F2 and F3 depend on how those packages implement T2 and T1" | MET |
| 5 | Validation mechanism | F4 "Stage 4 moves 8 of those rows to `v2` and no task runs that test" | MET |

**Invariant and edge case (5/5)**

| # | Claim | Evidence | Verdict |
|---|---|---|---|
| 1 | Collection boundaries | Step 5 "none under `plugins/superclaude`"; allow-list end state "That leaves ... all three exist" | MET |
| 2 | State across components | Step 4 "Tasks 1 and 2 plus stage 3 already set all 11 rows" | MET |
| 3 | Guard gaps | F2 "passes without testing anything" | MET |
| 4 | Count divergence | "Registry end state: 11 `digest` rows at `v2`, 2 `pointer-only`, 5 `installed-only`" | MET |
| 5 | Interaction effects | F4 "Task 4 edits both MDTM templates after Task 1 has placed the digest there" | MET |

**Subtotals V3:** completeness 4, correctness 4, structure 5, clarity 4, risk 3, invariant 5 = **25/30, qual 0.833**. Edge-case floor: 5/5, eligible.

---

## Final table (pass 1)

| Variant | quant | qual (met/30) | combined = 0.5 quant + 0.5 qual | Correctness | Edge-case dim | Eligible as base |
|---|---|---|---|---|---|---|
| V1 | 0.808 | 0.733 (22) | **0.770** | 5/5 | 5/5 | yes |
| V2 | 0.890 | 0.600 (18) | **0.745** | 1/5 | 4/5 | yes |
| V3 | 0.782 | 0.833 (25) | **0.808** | 4/5 | 5/5 | yes |

- Leader in pass 1: **V3 (0.808)**, then V1 (0.770), then V2 (0.745).
- Margin V3 minus V1 = 0.038, below 0.05: the A.4 tiebreaker applies once pass 2 is reconciled. Step 1 (debate diff points) belongs to the orchestrator. If it ties, step 2 favours V1 (correctness 5/5 against V3's 4/5).
- Every criterion where pass 2 disagrees goes to re-evaluation (A.5). The judgment calls most likely to differ are V1 completeness 4 (no fix stated), V2 invariant 1 (no boundary case), V2 structure 3 (finding inside Notes), and the DC treatment of undefined card keys (P4, OLD, stage1 plan).
