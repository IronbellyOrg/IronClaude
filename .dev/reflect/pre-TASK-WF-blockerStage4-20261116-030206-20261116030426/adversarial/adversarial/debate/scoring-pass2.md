# Scoring pass 2 (reverse order: V3, V2, V1)

- Evaluator: pass 2 of 2, position-bias mitigation. Algorithm: `~/.claude/skills/sc-adversarial-protocol/refs/scoring-protocol.md` (A.1 to A.3, edge-case floor A.2).
- Ground truth for correctness: debate settlement. Blocking: C-001, C-002. Minor: C-003..C-009, C-011, C-013, C-014, N-1. Dropped: C-010, C-012, C-015, S-001, S-002, X-001, X-003. Probe MEDIUM: INV-006, INV-007, INV-008, INV-012, INV-017.
- Repo spot checks made for this pass: `tests/skills/test_review_severity_rule.py:181-195` (S1_S3_FILES = 10 files, S5_FILES = first 6); `tests/skills/test_review_severity_mapping.py:58,71,72` pin the phrase and "once per loop"; `tdd/refs/build-request-template.md:125` has only lowercase "after 2 fix cycles"; `agent_template_qa.md:333` is a list of rf-qa-qualitative labels.
- RC source list (12 items): Tasks 1 to 7 (7 items), earlier findings F3/F4/F5/F6/F9/F12/F13, comparison with base Tasks 41 to 46, step-by-step walk of Task 6 ordering, coverage matrix vs the 20-line source request, grading by the severity rule.
- Assumptions: the card's "P4:n", "OLD:n", "plan:n" line keys and the earlier-review ids F3..F13 are external references (excluded from DC). SR uses a count of concrete statements (line citations, numbers, named files) against hedges ("may", "a guess", "careless").

---

## Variant 3 (refactorer, opus class)

### Quantitative

| Metric | Computation | Value |
|---|---|---|
| RC | Tasks 1,3,4,6 addressed by findings (F1, F5, F4, F2/F3); Task 2 and Task 5 only through Checked "Depends on" and registry-state lines (counted); Task 7 absent; earlier findings F3..F13 absent; base 41-46 comparison absent; Task 6 walk present; coverage matrix absent; severity grading present. 6 + 1 + 1 = 8 of 12 | 0.667 |
| IC | About 25 scorable claims; 0 contradictions found (verdict wording "end up consistent" is wrong against C-006 but does not contradict another line of the card) | 1.000 |
| SR | About 40 concrete statements vs 3 hedges ("may resolve", "may hunt", "depend on how ... implement") | 0.93 |
| DC | Internal refs: "F2 and F3" (Step 7), Step 1 to 7 numbering: all resolve | 1.000 |
| SC | H2 sections: Verdict, Findings, Checked, Self-report = 4; max across variants = 5 | 0.800 |
| quant | 0.30(0.667) + 0.25(1.0) + 0.15(0.93) + 0.15(1.0) + 0.15(0.8) | **0.860** |

### Qualitative

**Completeness**

| Criterion | Claim / Evidence / Verdict |
|---|---|
| 1 Covers all explicit requirements | Task 7, F3..F13 check, base 41-46 comparison, coverage matrix not in card. NOT MET |
| 2 Edge cases and failure scenarios | F1 "run halts in Task 1 unless ... edits a finished stage 3 file"; F4 consumer line inside fence. MET |
| 3 Dependencies and prerequisites | Checked "Depends on lines: Task 2 after Task 1 ... Task 6 after Task 5". MET |
| 4 Success/completion criteria | Verdict: "workable order ... One check cannot be met". MET |
| 5 Out of scope stated | "Not checked: the spec section 10.5 cap lines and the exact L1 merge text." MET |

Subtotal 4/5.

**Correctness**

| Criterion | Claim / Evidence / Verdict |
|---|---|
| 1 No factual errors | Verdict "files edited by several tasks end up consistent" fails (byte-identity pin, C-006/X-002); Step 7 "no failure expected" misses C-002; F4 first half is dropped C-015. NOT MET |
| 2 Feasible approaches | F2 "Fix: stage `plugins/superclaude/skills/sc-review-severity/` before running the three tests". MET |
| 3 Terminology consistent | "allow-list", "reverse scan", "canonical row" used the same way throughout. MET |
| 4 No internal contradictions | None found; IC 1.0. MET |
| 5 Claims supported | Every F line has file:line citations (F1 three citations). MET |

Subtotal 4/5.

**Structure**

| Criterion | Claim / Evidence / Verdict |
|---|---|
| 1 Logical ordering | Verdict, Findings, Checked, Self-report. MET |
| 2 Hierarchy depth | Flat H2 plus bullets; Task 6 steps nested under one bullet. MET |
| 3 Separation of concerns | Defects under Findings, clean passes under Checked. MET |
| 4 Navigation aids | Cross-reference "no failure expected apart from F2 and F3"; numbered Steps 1 to 7. MET |
| 5 Artifact conventions | F lines `F1 \| MAJOR \| blocking true \| ...`, Checked, Self-report as the brief asks. MET |

Subtotal 5/5.

**Clarity**

| Criterion | Claim / Evidence / Verdict |
|---|---|
| 1 Unambiguous language | F3 "T1 or T3 may resolve the wrong file"; F5 "An executor may hunt for a list". NOT MET |
| 2 Concrete | F2 names `git ls-files` scope, folder path and the three tests. MET |
| 3 Section purpose | Verdict is a three-sentence summary of the card. MET |
| 4 Acronyms defined | "T1", "T2", "T15 parity", "OLD:477", "L1" never defined. NOT MET |
| 5 Actionable next steps | F2 "Fix: stage ... or make T2 read the filesystem". MET |

Subtotal 3/5.

**Risk coverage**

| Criterion | Claim / Evidence / Verdict |
|---|---|
| 1 At least 3 risks with probability and impact | F1, F2, F3 each give Who/Wrong result, plus "F2 and F3 depend on how those packages implement T2 and T1" as the likelihood condition. MET |
| 2 Mitigation per risk | Only F2 carries a fix; F1, F3, F4, F5 have none. NOT MET |
| 3 Failure modes and recovery | F1 failure plus the hand-edit route; F2 two recovery routes. MET |
| 4 External dependencies | "Tests from stages 1 to 3 do not exist yet, so F2 and F3 depend on ..." MET |
| 5 Detection mechanism | F4 "no task runs that test"; F2 asks for a staged run before the three tests. MET |

Subtotal 4/5.

**Invariant and edge case coverage**

| Criterion | Claim / Evidence / Verdict |
|---|---|
| 1 Collection boundaries | "Allow-list end state: stage 3 lists 8 paths; Task 1 removes 2, Task 3 removes 4 ... Plugin skills folder holds ...". MET |
| 2 State across component boundaries | Task 6 walk: registry and allow-list name a missing plugin file at Step 1, existence check fails until Step 2. MET |
| 3 Guard condition gaps | F2 "T2 scans only git-tracked files ... passes without testing anything". MET |
| 4 Count divergence | "old sentence is in exactly 11 files"; "11 digest rows at v2, 2 pointer-only, 5 installed-only". MET |
| 5 Interaction effects | F4 consumer line landing inside the digest fence breaks Task 1's "T1 passes" line. MET |

Subtotal 5/5.

**V3 qual: 25/30 = 0.833**

---

## Variant 2 (qa, haiku class)

### Quantitative

| Metric | Computation | Value |
|---|---|---|
| RC | Tasks 1 to 7 each named (D2/D3/D4, base-comparison bullets 41->1 to 46->6, Task 7 note) = 7; earlier findings F3/F4/F5/F6/F9/F12/F13 all checked = 1; base comparison = 1; coverage matrix (D4) = 1; severity grading = 1; Task 6 step-by-step walk absent (only names the order registration, allow-list, copy, test) = 0. 11 of 12 | 0.917 |
| IC | About 24 claims; 2 contradictions: D1 and D2 are "MAJOR; blocking true" in the body and "Table severity: MEDIUM" in the same row | 0.917 |
| SR | About 35 concrete vs 2 hedges ("may genuinely pass", "suspected") | 0.94 |
| DC | Internal refs "Finding D2", "Findings D1 and D2", "Finding D3": all resolve | 1.000 |
| SC | H2 sections: Verdict, Deviations, Adherence summary, Notes, Self-report = 5 (max) | 1.000 |
| quant | 0.30(0.917) + 0.25(0.917) + 0.15(0.94) + 0.15(1.0) + 0.15(1.0) | **0.945** |

### Qualitative

**Completeness**

| Criterion | Claim / Evidence / Verdict |
|---|---|
| 1 Covers all explicit requirements | 11 of 12 review items; no step-by-step Task 6 walk. NOT MET |
| 2 Edge cases and failure scenarios | D2 "The audit may genuinely pass while this acceptance line still fails". MET |
| 3 Dependencies and prerequisites | D1 prerequisite of generation order; "Removed the cross-package Task 40 dependency". MET |
| 4 Success criteria | Verdict "needs revision before execution"; adherence summary 14 of 17. MET |
| 5 Out of scope | "No files changed and no tests were run. Execution results and completed upstream-stage repairs ... were not available". MET |

Subtotal 4/5.

**Correctness**

| Criterion | Claim / Evidence / Verdict |
|---|---|
| 1 No factual errors | D1 graded blocking but settled as drop (C-010: no plan edit can change generation time); D4 settled drop (C-012); misses C-002. NOT MET |
| 2 Feasible approaches | No remedy given; D1's implied remedy cannot be applied to an existing plan. NOT MET |
| 3 Terminology consistent | D1 "MAJOR; blocking true" next to "Table severity: MEDIUM". NOT MET |
| 4 No internal contradictions | Same two rows disagree with themselves; IC 0.917. NOT MET |
| 5 Claims supported | Every D row has an Evidence field with file:line. MET |

Subtotal 1/5.

**Structure**

| Criterion | Claim / Evidence / Verdict |
|---|---|
| 1 Logical ordering | Verdict, Deviations, Adherence summary, Notes, Self-report. MET |
| 2 Hierarchy depth | H1 title, H2 sections, H3 under Notes only. MET |
| 3 Separation of concerns | Deviations vs base comparison vs earlier findings kept in separate subsections. MET |
| 4 Navigation aids | "Findings D1 and D2 concern the same entry-prerequisite unit"; "Finding D3". MET |
| 5 Artifact conventions | Header comment says the reviewer used a deviation table instead of the requested F lines. NOT MET |

Subtotal 4/5.

**Clarity**

| Criterion | Claim / Evidence / Verdict |
|---|---|
| 1 Unambiguous language | D2 "The audit may genuinely pass ..."; header "identity mismatch suspected". NOT MET |
| 2 Concrete | D3 quotes "the cap sentences kept by content" and P4:55. MET |
| 3 Section purpose | Each section titled by purpose; Verdict is a single sentence. MET |
| 4 Acronyms defined | "OLD:486-552", "INF-002", "P4" outside the saved header never defined. NOT MET |
| 5 Actionable next steps | Verdict: "needs revision before execution". MET |

Subtotal 3/5.

**Risk coverage**

| Criterion | Claim / Evidence / Verdict |
|---|---|
| 1 At least 3 risks with probability and impact | Impact via blocking flags, no likelihood anywhere. NOT MET |
| 2 Mitigation per risk | No mitigation in D1 to D4. NOT MET |
| 3 Failure modes and recovery | D2 names the failure; no recovery. NOT MET |
| 4 External dependencies | "Actual T3 implementation remains an earlier-stage prerequisite, not verified completed behavior." MET |
| 5 Detection mechanism | D3 flags the missing cap-content pin in P4:53-55. MET |

Subtotal 2/5.

**Invariant and edge case coverage**

| Criterion | Claim / Evidence / Verdict |
|---|---|
| 1 Collection boundaries | Restates "11-row invariant" and "five digest templates to four" but does not test the collection. NOT MET |
| 2 State across component boundaries | D2 stage 3 summary written before the window vs stage 4 check. MET |
| 3 Guard condition gaps | D3 "no cap-content pin"; D1 missing precondition guard. MET |
| 4 Count divergence | "Spec units audited: 17 ... Fully adherent: 14 ... Drift: 4 findings affecting 3 units". MET |
| 5 Interaction effects | Lists the combined acceptance run but analyses no cross-task effect. NOT MET |

Subtotal 3/5.

**V2 qual: 17/30 = 0.567**

---

## Variant 1 (analyzer, sonnet class)

### Quantitative

| Metric | Computation | Value |
|---|---|---|
| RC | Task 1 (F1, F8), Task 2 (F6, Checked anchors), Task 3 (F3, F4), Task 4 (Checked grep -c, F9), Task 5 (F2, F5, F7), Task 6 (F6, Checked) = 6; Task 7 absent; earlier findings absent; base comparison absent; Task 6 walk absent; coverage matrix absent; severity grading present = 1. 7 of 12 | 0.583 |
| IC | About 30 claims; 0 contradictions | 1.000 |
| SR | About 55 concrete vs 3 hedges ("on a guess", "careless", "silently relaxed") | 0.95 |
| DC | No internal cross-references broken (line keys external) | 1.000 |
| SC | H2 sections: Verdict, Findings, Checked, Self-report = 4; max 5 | 0.800 |
| quant | 0.30(0.583) + 0.25(1.0) + 0.15(0.95) + 0.15(1.0) + 0.15(0.8) | **0.838** |

### Qualitative

**Completeness**

| Criterion | Claim / Evidence / Verdict |
|---|---|
| 1 Covers all explicit requirements | Task 7, earlier findings, base comparison, matrix, Task 6 walk missing. NOT MET |
| 2 Edge cases and failure scenarios | F8 "A missing go still halts the run, but only after the edits exist"; F4 case-sensitive grep. MET |
| 3 Dependencies and prerequisites | F2 "The stage 3 plan edits no spec-panel text, and its own acceptance needs this test green". MET |
| 4 Success criteria | Verdict "two blocking defects ... Everything else is minor". MET |
| 5 Out of scope | No "not checked" or scope statement anywhere in the card. NOT MET |

Subtotal 3/5.

**Correctness**

| Criterion | Claim / Evidence / Verdict |
|---|---|
| 1 No factual errors | All nine F lines match settled C-001..C-009; "6 templates and 4 rule prompts" matches S1_S3_FILES. MET |
| 2 Feasible approaches | F2 "stage 4 must make the change" and re-pin is workable. MET |
| 3 Terminology consistent | MAJOR/MINOR plus blocking flag agree on every line. MET |
| 4 No internal contradictions | None found; IC 1.0. MET |
| 5 Claims supported | Every F line has quoted citations (F2 four citations). MET |

Subtotal 5/5.

**Structure**

| Criterion | Claim / Evidence / Verdict |
|---|---|
| 1 Logical ordering | Verdict, Findings, Checked, Self-report. MET |
| 2 Hierarchy depth | Flat. MET |
| 3 Separation of concerns | Findings vs Checked. MET |
| 4 Navigation aids | No F-id cross-references; the Verdict does not number the findings. NOT MET |
| 5 Artifact conventions | F lines with severity, blocking flag, category as the brief asks. MET |

Subtotal 4/5.

**Clarity**

| Criterion | Claim / Evidence / Verdict |
|---|---|
| 1 Unambiguous language | No "may", "might" or "as appropriate"; F2 "stays red, or is silently relaxed" names the two outcomes. MET |
| 2 Concrete | F4 gives the lowercase-only line at build-request-template.md:125. MET |
| 3 Section purpose | Verdict states the result in two sentences. MET |
| 4 Acronyms defined | "FR-8", "T3", "QA", "plan:88" undefined. NOT MET |
| 5 Actionable next steps | F2 "So stage 4 must make the change." MET |

Subtotal 4/5.

**Risk coverage**

| Criterion | Claim / Evidence / Verdict |
|---|---|
| 1 At least 3 risks with probability and impact | Impact flags only, no likelihood. NOT MET |
| 2 Mitigation per risk | No fix text in F1..F9. NOT MET |
| 3 Failure modes and recovery | F2 and F8 name failures; no recovery steps. NOT MET |
| 4 External dependencies | F2 relies on stage 3 plan not editing spec-panel (stage3 plan:122 in citations). MET |
| 5 Detection mechanism | F6 "pinning tests ... are never run in stage 4". MET |

Subtotal 2/5.

**Invariant and edge case coverage**

| Criterion | Claim / Evidence / Verdict |
|---|---|
| 1 Collection boundaries | "The six stage 4 files in Tasks 1 and 3 equal the six allow-listed stage 4 files"; "The plugin holds 4 skills". MET |
| 2 State across component boundaries | F6 plugin prompt must stay byte-identical while Task 5 edits in place. MET |
| 3 Guard condition gaps | F7 "The pointer-only check in T3 passes without a pointer". MET |
| 4 Count divergence | "11 files hold ... matching the 11 digest rows". MET |
| 5 Interaction effects | F2 Task 5 deletion vs the mapping test pin in both spec-panel copies. MET |

Subtotal 5/5.

**V1 qual: 23/30 = 0.767**

---

## Final table

| Variant | quant | qual | Combined (0.5/0.5) | Dim 6 (floor 1/5) | Eligible as base |
|---|---|---|---|---|---|
| V3 (refactorer, opus) | 0.860 | 0.833 (25/30) | **0.846** | 5/5 | yes |
| V1 (analyzer, sonnet) | 0.838 | 0.767 (23/30) | **0.802** | 5/5 | yes |
| V2 (qa, haiku) | 0.945 | 0.567 (17/30) | **0.756** | 3/5 | yes |

- Leader in this pass: V3 (0.846). Margin to V1: 0.044, which is under the 5% tiebreak band.
- V2's high quant comes from coverage breadth (RC 0.917, SC 1.0), not correctness: its blocking D1 is a settled drop and its severity labels disagree inside the card (correctness 1/5).
- V1 is the only card with C-002 and the most settled minors (9 of 14 settled findings); V3 has C-001, C-003, C-013, C-014 and half of C-006 but wrongly asserts consistency and no failure beyond F2/F3.
- Disagreement risk for the position-bias merge: criteria most likely to flip are Risk 1 (V3 MET on a conditional-likelihood reading), Clarity 1 (hedge words) and Structure 4 (V1 cross-references).
