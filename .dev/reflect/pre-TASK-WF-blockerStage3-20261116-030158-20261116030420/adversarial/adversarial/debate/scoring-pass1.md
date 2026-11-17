# Scoring pass 1 (variants evaluated in order V1, V2), sonnet class, agent af7f9560b210a719f

(Persisted verbatim by the orchestrator from the agent's final message; hand-back frame indentation removed.)

## Quantitative layer

| | RC | IC | SR | DC | SC | quant |
|---|---|---|---|---|---|---|
| V1 | 8/12 = 0.667 | 1.00 (0 contradictions in about 16 claims) | 0.71 (about 24 concrete, 10 vague) | 1.00 (6/6 spot checks) | 1.00 (4/4) | **0.857** |
| V2 | 10/12 = 0.833 | 0.95 (1 contradiction in about 20 claims) | 0.79 (about 38 concrete, 10 vague) | 1.00 (6/6 spot checks) | 1.00 (4/4) | **0.906** |

- **RC, V1 raises:** C-001 (F2), C-002 (F3), C-003 (F4), C-004 (F5), C-005 (F8), C-006 (F7), U-001 (F1) and U-002 (F6). It misses U-003 to U-006.
- **RC, V2 raises:** C-001 (F1), C-002 (F4), C-003 (F2), C-004 (F3), C-005 (F10), C-006 (F11), U-003 (F5), U-004 (F6), U-005 (F7) and U-006 (F8). It misses U-001 and U-002.
- **IC, V2's one contradiction:** F3 says Tasks 4 and 5 have "no input file". Its own sound bullet says the package id is read from the ledger per plan line 19.
- **SC:** both cards have Findings, Checked and sound, Self-reported confidence, plus the attached calibration block.
- **DC, cites that held (V1):** plan 37, 62, 116, 147 and 162; `pragmatic-subagent.js:7` and `:15`; Makefile `sync-dev` at 109 with no `output-styles` anywhere in it; stage 2 plan 110 ("zero runs"); stage 0 plan 110; spec 985.
- **DC, cites that held (V2):** plan 37, 62, 116, 122, 126 and 147; stage 2 plan 114; stage 0 plan 106 and 110; spec 974; `test_review_severity_rule.py:181`; hook line 7.
- **DC, not checked:** `hooks.json:173` and stage 1 plan line 209 (V2).

## Qualitative layer (criteria met)

| Dimension | V1 | V2 |
|---|---|---|
| Completeness | 1,2,3,5 | 1,2,3,5 |
| Correctness | 1,2,3,4,5 | 2,3,5 |
| Structure | 1,2,3,4,5 | 1,2,3,4,5 |
| Clarity | 1,2,3,5 | 1,2,3,5 |
| Risk coverage | 1,2,3,4,5 | 1,2,3,4,5 |
| Invariant and edge-case | 1,2,3,4,5 | 1,2,3,4,5 |
| **Subtotal** | **28/30 = 0.933** | **26/30 = 0.867** |

**Evidence notes**
- **Completeness (both):** both are NOT MET on criterion 4, because neither gives a fix check for every finding. V1 maps the earlier F2, F3, F9, F11 and F13. V2 maps R-002, R-003 and R-005.
- **Correctness V1:** cites verified. Its F5 grade is high, and the debate conceded that, but the fact itself holds.
- **Correctness V2:** NOT MET on criterion 1. F9 says "Tasks 3 and 4" although Task 4 runs no tests (advocate 2 conceded this). F1 says "fails every time" and "before any run has happened", but stage 2 line 114 allows zero runs.
- **Correctness V2:** NOT MET on criterion 4 because of the F3 tension noted above.
- **Clarity (both):** criterion 4 is NOT MET. V1 uses "O1", "O5", "O8" and "earlier F2/F3/F9/F13" undefined. V2 uses "R-002", "T1 card's O5" and "REQ-03" undefined.
- **Risk coverage V1:** F1 gives a digest-match check as detection. F4 covers the advisory-result halt.
- **Risk coverage V2:** F1 names the risk that a fix cycle fakes the gate. F6 adds a pytest acceptance line. F4 asks for the confound to be reported in the result file.
- **Invariant coverage V1:** F2 (zero runs), F4 (advisory class), F1 (installed vs source style), F8 (task count), F3/F6 (task interactions).
- **Invariant coverage V2:** F1 and F2 (zero runs, advisory class), F4 (installed copy), F5 (baseline), F6 and F8 (v2 vs legacy registry rows), and the 11-file count in its sound section.

## Combined and floor

- V1 = 0.5 × 0.857 + 0.5 × 0.933 = **0.895**
- V2 = 0.5 × 0.906 + 0.5 × 0.867 = **0.887**
- The gap is 0.009, inside the 0.05 band, so the tie-break applies.
- **Edge-case floor:** both score 5/5 on the last dimension, so neither is ineligible.

## Tie-break and selected base

The tie-break is points won in the debate, counted only where both advocates agree or the opposing advocate conceded in round 2.
- V1 won X-001, U-007, U-001 and U-002 (4).
- V2 won U-003, U-004, U-005, U-006, plus C-007 and X-002 (advocate 1 conceded the entry-check ordering gap in round 2) (6).

**Selected base: Variant 2.**
1. It wins the debate tie-break 6 to 4, after a combined-score difference of only 0.009.
2. It carries 10 of 12 consensus items, including the four it alone raised (U-003 to U-006). Its fixes are the more specific ones, such as running `shadow_summary.py` before any spawn and adding the registry test to the acceptance lines.
3. Its weaknesses are fixable by edit: it misses U-001 and U-002, and F9 and the "fails every time" wording are overstated.

## Strengths of Variant 1 to merge into the base

- **U-001 (highest severity):** `pragmatic-subagent.js:7` reads `~/.claude/output-styles/pragmatic.md`, and `make sync-dev` (Makefile:109) never copies output styles. So Task 3 never makes the new rule live. The merged card should say that the switch steps (b) release and (c) per-machine refresh, plus the `make doctor` check, are not named in the plan (advocate 2's narrowing).
- **U-002:** plan line 162 ("no revert trigger can be judged until the audit window has run") contradicts RT1 (spec 985, "Any safety-class escape in the audit or the seeded set"). Task 1 produces the seeded-set result before the window. Merge advocate 2's addition: Task 3's "equals the old rule's" is weaker than RT1's "any".
- **C-001 wording:** V1 softens the "cannot exist by construction" claim, since five runs could already exist when the stage 2 summary is written. It also frames the defect as a stale summary with no refresh owner. Merge this with V2's fix, with the added clause "do not rewrite historical evidence".
- **C-002:** V1 adds that reviewer configurations must match across the two passes.
- **C-004, C-006, C-005 grades:** keep them at minor, as the debate settled. V1's F5 blocking grade should not carry over.
