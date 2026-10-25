# Base Selection Report

- Generated: 2026-10-24T21:40:53Z (Step 3, sc:debate-orchestrator, Mode A, 2 variants, depth standard)
- Variant 1 (V1, called "A" in diff-analysis.md) = `variant-1-original.md`. sc:reflect-reviewer, persona **analyzer**, slot sonnet, model `claude-sonnet-5-5[1m]`.
- Variant 2 (V2, called "B" in diff-analysis.md) = `variant-2-original.md`. sc:reflect-reviewer, persona **qa**, slot haiku, which resolved to `grok-4.7[1m]`.
- Inputs used:
  - `diff-analysis.md`, `debate-transcript.md`, `invariant-probe.md`, `round-*.md`, `scoring-pass-1.md` (order V1, V2), `scoring-pass-2.md` (order V2, V1).
  - Source requirements: `reviewer-snapshot/root/spec.md:5-12` (R-001..R-003) and `completed.md:6-8` (T-101..T-103).
- Debate status carried forward: **BLOCKED_BY_INVARIANTS** (INV-004 HIGH, UNADDRESSED). Base selection does not depend on convergence, but the block carries into Step 4 and Step 5 (see `refactor-plan.md`).
- Judge model-class disclosure: the orchestrator, the advocates, the fault-finder and both scoring passes all ran on opus (`debate-transcript.md:14`). The quantitative layer below is computed mechanically to limit judge discretion.

## Quantitative Scoring (50% weight)

### Computation rules (deterministic, applied identically to both variants)

| Metric | Rule applied |
|---|---|
| **RC** (Requirement Coverage) | Grep each source ID (R-001, R-002, R-003, T-101, T-102, T-103) in the variant. RC = IDs matched / 6. |
| **Substantive statements** | Every non-empty line, excluding: headings, the HTML provenance comment, table header and separator rows, code-fence markers, and the leading metadata lines (`**Reviewer persona**`, `**Grounding root**`, `**Diff scope**`, `**Timestamp**`, `**Model**`, `**Model actually running**`). |
| Concrete statement | A substantive line with at least one concrete indicator: a digit, a backticked path or identifier, or a named entity (pytest, ValueError, Python, sys.path, Drift, Regression, Grounding Gap, sonnet/grok/haiku, conftest, pyproject, f-string, None). |
| **SR** (Specificity Ratio) | Concrete / substantive statements (the `scoring-protocol.md:18` definition). Vague-only lines (vague words with no concrete indicator) numbered 0 in both variants, so the `:72` form gives 1.0 for both. The stricter `:18` form is used because it is the only one that discriminates. |
| **IC** (Internal Consistency) | Scorable claims = concrete statements. Contradictions = opposing claims about the same subject inside one variant. |
| **DC** (Dependency Completeness) | Internal references, meaning uses of internal IDs other than their defining row, "see below/above", and "recommendation N" pointing inside the card. References to the T1 card, the taxonomy or the map are external and excluded (`scoring-protocol.md:87`). |
| **SC** (Section Coverage) | H2 count / max H2 count. |

### Per-variant evidence

**V1**
- RC: all 6 IDs found. Hit counts: R-001 = 4, R-002 = 5, R-003 = 4, T-101 = 1, T-102 = 1, T-103 = 6.
- SR: 32 substantive statements, 29 concrete. The 3 non-concrete lines are L10, L70 and L72.
- IC: 0 contradictions in 29 claims.
  - GG-1/Risk 2 ("could be Drift") is wrong against the taxonomy (X-001), but V1 states it the same way throughout, so it is not an internal contradiction.
  - The `:5-9` and `:7-9` ranges cite different scopes (whole hunk and code lines), so they do not conflict.
- DC: 8 internal references, all resolved. GG-1 is used at L51, L57 and L74. GG-2 is used at L31, L51, L56 and L74. "(see below)" at L8 resolves to Grounding gaps. The GG-1/GG-2 rows at L22-23 are definitions.
- SC: 8 H2s (Deviations, Grounding gaps, Challenge to the T1 card, Correctness gaps, Adherence summary, Risks, Recommendations, Notes).

**V2**
- RC: all 6 IDs found. Hit counts: R-001 = 8, R-002 = 10, R-003 = 11, T-101 = 4, T-102 = 3, T-103 = 4.
- SR: 52 substantive statements, 44 concrete. The 8 non-concrete lines are L34, L41, L54, L55, L57, L59, L60 and L61.
- IC: 1 contradiction in 44 claims. Gap 1 says "exit 0 would close it" (V2:52), but its `next_evidence_needed` also requires diff or task-log provenance (V2:53). The V2 advocate conceded this (`round-2-advocate-2.md:17`).
  - The INV-006 count mismatch is not counted here. "Unclassifiable: 1" counts spec units, while the YAML has 2 rows, so the two figures use different units. It is a merge-time issue, not a contradiction in V2 as written.
- DC: 2 internal references, both resolved. "re-run recommendation 1" (L91) points to Rec 1. "the verification run above" (L59) points to gap 1. "T1 recommendation 3" (L45, L90) is external. F-001..F-004 appear only in their defining rows.
- SC: 9 H2s (the 8 above in V2's own naming, plus Self-reported confidence).

### Scores

| Metric | Weight | Variant 1 (analyzer / sonnet) | Variant 2 (qa / grok-4.7) |
|--------|--------|-------------------|-------------------|
| requirement_coverage | 0.30 | 1.0000 (6/6) | 1.0000 (6/6) |
| internal_consistency | 0.25 | 1.0000 (1 − 0/29) | 0.9773 (1 − 1/44) |
| specificity_ratio | 0.15 | 0.9063 (29/32) | 0.8462 (44/52) |
| dependency_completeness | 0.15 | 1.0000 (8/8) | 1.0000 (2/2) |
| section_coverage | 0.15 | 0.8889 (8/9) | 1.0000 (9/9) |
| **quant_score** | | **0.9693** | **0.9712** |

Arithmetic:
- V1 = 0.30×1.0 + 0.25×1.0 + 0.15×0.90625 + 0.15×1.0 + 0.15×0.88889 = 0.3000 + 0.2500 + 0.1359 + 0.1500 + 0.1333 = **0.9693**
- V2 = 0.30×1.0 + 0.25×0.97727 + 0.15×0.84615 + 0.15×1.0 + 0.15×1.0 = 0.3000 + 0.2443 + 0.1269 + 0.1500 + 0.1500 = **0.9712**

## Qualitative Scoring (50% weight) — Additive Binary Rubric

**Criterion alignment.** Pass 1 labels the dimensions C/K/S/L/R/E and Pass 2 labels them Cm/Co/S/Cl/R/E. They are aligned by position 1-5 within each dimension. Each cell below gives the final verdict (P1 / P2 evidence condensed) under the CEV protocol.

### Completeness (5 criteria)

| Criterion | V1 | Evidence | V2 | Evidence |
|-----------|----|----------|----|----------|
| Covers all explicit requirements | MET | Adherence summary V1:49-52 covers R-001..R-003. GG-1 covers T-103. | MET | F-001..F-004 (V2:25-28); summary V2:68-71 |
| Addresses edge cases/failures | MET | Falsy, whitespace and non-string inputs (V1:44); exit-code outcomes (V1:23) | MET | Risk 3 (V2:81); exit codes 0/1/2/3/5 (V2:52) |
| Includes dependencies/prerequisites | MET | Import path depends on invocation (V1:32-36); diff scope and pytest exit needed (V1:22-23) | MET | sys.path requirement (V2:45); diff or task-log provenance (V2:53, Rec 2) |
| Defines success/completion criteria | MET | "Exit code 0 means pass" (V1:65) | MET | "0 closes R-003 exercise"; "plain pytest collects 2 tests" (V2:88, :90) |
| Specifies out-of-scope items | MET | Live root out of bounds (V1:71); whitespace kept out of the ledger (V1:37) | MET | Reachability skips are telemetry; live root not read (V2:96-98); no advisory section, with reason (V2:84) |
| **Subtotal** | **5/5** | | **5/5** | |

### Correctness (5 criteria)

| Criterion | V1 | Evidence | V2 | Evidence |
|-----------|----|----------|----|----------|
| No factual errors | MET | Both passes checked map:19, map:31, taxonomy:149-153, reuse-audit:8-21 and changes.patch:7-9 against the snapshot, and all were accurate | NOT MET | "`changes.patch` is 10 lines" (V2:44); the file has 9 (`wc -l` = 9, re-checked by the orchestrator). The `tests/__init__.py` rejection (V2:45, :90) is wrong under pytest's default prepend mode ([INFERRED]). |
| Feasible approaches | MET | Re-run and widen-scope recommendations (V1:64-66) | MET | pythonpath fix and run commands (V2:88-90) |
| Terminology consistent/accurate | NOT MET | Calls a guard inside one function a "Sibling disagreement" (V1:44), against taxonomy:161,167. GG-2's `hunk_ref` is `spec.md:11-12`, which is not a hunk. | MET | "not a sibling-symbol correctness gap (`greet` has no sibling)" (V2:81, :84) |
| No internal contradictions | MET | 0 deviations, GG routing and `partial` agree throughout (V1:8, :25, :74) | MET | Both passes: ledger, status and the missing advisory section are consistent (V2:11, :84). The quantitative IC still records 1 contradiction (V2:52 vs :53). Both qualitative passes MET this, and since they agree no re-evaluation is triggered. The point is carried into the refactor plan (Change 5). |
| Claims supported by evidence | MET | file:line on every row (V1:16-44) | MET | file:line on every finding (V2:25-28) |
| **Subtotal** | **4/5** | | **4/5** | |

### Structure (5 criteria)

| Criterion | V1 | Evidence | V2 | Evidence |
|-----------|----|----------|----|----------|
| Logical ordering | MET | Deviations, gaps, challenge, advisory, summary, risks, recs, notes | MET | Verdict, deviations, coverage, challenge, gaps, summary, risks, recs, notes |
| Consistent hierarchy | MET | H1 then flat H2s | MET | H1 then flat H2s |
| Separation of concerns | MET | Deviation, grounding-gap and correctness-gap channels kept apart (V1:12-45) | MET | Gaps marked "not a 4th-class row" (V2:27, :64) |
| Navigation aids | MET | GG-1/GG-2 reused; "(see below)" (V1:8, :51, :56-57, :74) | MET | F-IDs; "re-run recommendation 1" (V2:91) |
| Artifact conventions | NOT MET | No `decision_needed_by_user` in the gap table (taxonomy:146). Advisory channel used without siblings (taxonomy:167, 172-179). | MET | Gap YAML has all 6 fields (V2:49-62 vs taxonomy:140-147) |
| **Subtotal** | **4/5** | | **5/5** | |

### Clarity (5 criteria)

| Criterion | V1 | Evidence | V2 | Evidence |
|-----------|----|----------|----|----------|
| Unambiguous language | MET | "partial", "static" (V1:50-51) | MET | "ledger-true and acceptance-false" (V2:43) |
| Concrete | MET | `"   "`, `5`, exact commands (V1:44, :65) | MET | Exact commands and ranges (V2:53, :88) |
| Section purpose | MET | Distinct headings | MET | Distinct headings |
| Terms defined on first use | NOT MET | T1, S_dev_density, GG and "verification triangle" undefined (V1:25, :30) | NOT MET | T1, S_dev_density and "verification triangle" undefined (V2:11, :73) |
| Actionable next steps | MET | File / Change / Verifier table (V1:62-66) | MET | Numbered File / Change / Verifier (V2:88-91) |
| **Subtotal** | **4/5** | | **4/5** | |

### Risk Coverage (5 criteria)

| Criterion | V1 | Evidence | V2 | Evidence |
|-----------|----|----------|----|----------|
| ≥3 risks with probability and impact | NOT MET | 3 risks, unrated (V1:56-58) | NOT MET | 4 risks with Grounded/[INFERRED] tags only (V2:77-82) |
| Mitigation per risk | MET | Risk 1 → run the suite. Risk 2 → scope or task log. Risk 3 → both pytest modes (V1:64-65). | NOT MET | Risk 4 (weak oracle, V2:82) has no mitigation in Recs 1-4 |
| Failure modes and recovery | **NOT MET (re-evaluated; see Position-Bias)** | Failure modes are classified (V1:23, :36, :65), but no recovery procedure is given for a collection failure or a test failure | MET | Exit-code failure modes, plus a recovery path: "only if plain pytest exits 2, set `pythonpath = .`" (V2:90) |
| External dependencies | MET | Invocation mode; snapshot incompleteness (V1:36, :71) | MET | pytest path config, exit 2 at collection (V2:80) |
| Monitoring/validation | MET | Verifier column, audit re-run (V1:64-65) | MET | Verifier per rec; both exit codes kept (V2:88-91) |
| **Subtotal** | **3/5** | | **3/5** | |

### Invariant & Edge Case Coverage (5 criteria)

| Criterion | V1 | Evidence | V2 | Evidence |
|-----------|----|----------|----|----------|
| Collection boundaries (empty, single, max) | MET | Empty input; the 0/1 hunk metric cannot see a no-hunk task (V1:30, :44) | MET | Empty input; exit 5; 2-test collection check (V2:26, :52, :90) |
| State interactions across components | MET | tests→src import; claim vs diff (V1:22, :32) | MET | Patch vs disk; import; done stamp vs evidence (V2:36, :45, F-004) |
| Guard condition gaps | MET | `not name` falsy/truthy (V1:44) | MET | `if not name` (V2:81) |
| Count divergence | MET | S_dev_density denominator omits T-103 (V1:30) | MET | `:6-9` not `:5-9`; claimed 3/3 vs executed 0 (V2:44, :28) |
| Interaction effects | MET | Gap list vs T1 headline vs forced status (V1:25, :31) | MET | R-001 closure independent of the unrun test (V2:30) |
| **Subtotal** | **5/5** | | **5/5** | |

### Edge Case Floor Check

| Variant | Sixth-dimension subtotal | Eligible | Floor suspended with warning |
|---------|---------------------------|----------|------------------------------|
| V1 | 5/5 | yes | no |
| V2 | 5/5 | yes | no |

### Qualitative Summary

| Dimension | Variant 1 | Variant 2 |
|-----------|-----------|-----------|
| Completeness | 5/5 | 5/5 |
| Correctness | 4/5 | 4/5 |
| Structure | 4/5 | 5/5 |
| Clarity | 4/5 | 4/5 |
| Risk Coverage | 3/5 | 3/5 |
| Invariant & Edge Case Coverage | 5/5 | 5/5 |
| **qual_score** | **25/30 = 0.8333** | **26/30 = 0.8667** |

## Position-Bias Mitigation

Pass 1 ran in order V1, V2 and Pass 2 in order V2, V1. All 60 verdicts (30 criteria × 2 variants) were compared by position.

- **V2**: Pass 1 = 5/4/5/4/3/5 = 26 and Pass 2 = 5/4/5/4/3/5 = 26. All 30 criteria agree. The individual misses are identical in both passes: Correctness-1, Clarity-4, Risk-1 and Risk-2.
- **V1**: Pass 1 = 5/4/4/4/4/5 = 26 and Pass 2 = 5/4/4/4/3/5 = 25. 29 of 30 criteria agree. The shared misses are Correctness-3, Structure-5, Clarity-4 and Risk-1. The one disagreement is Risk-3.

| Criterion | Variant | Pass 1 | Pass 2 | Agreement | Final |
|-----------|---------|--------|--------|-----------|-------|
| Risk-3 Failure modes and recovery procedures | V1 | MET ("Exit codes 1, 2/3 and 5 each mapped to a class", L23, L65) | NOT MET ("Failure modes are classified … but no recovery path is given for a collection failure or a test failure", L36, L65) | DISAGREE | **NOT MET** |

**Re-evaluation (explicit comparison, both passes' evidence)**

The criterion is conjunctive: it requires both failure modes and recovery procedures.

Pass 1's evidence covers only the first half. V1:23 and V1:65 map exit codes 1, 2/3 and 5 to classes. That is a classification of failure modes, not a recovery.

The orchestrator re-read V1 for the second half:
- Challenge #4 (V1:36) says "If it materialises as pytest exit 2 or 3, it is a Grounding Gap, not a Regression". That is classification only.
- Recommendation row 2 (V1:65) runs both invocations but gives no action to take if one fails.
- Recommendation row 1 (V1:64) widens the diff scope, which INV-004 shows cannot produce real provenance in a zero-commit repo.
- No V1 text says what to do after exit 1, 2/3 or 5.

V2, by comparison, has a recovery step conditioned on exit 2 (V2:90).

Pass 2's reading is the better-supported one. Under CEV, a MET verdict without cited evidence for the recovery half defaults to NOT MET. **Final: NOT MET.**

- Disagreements re-evaluated: **1**
- Final verdicts changed: **1** relative to Pass 1 (V1 Risk-3 MET → NOT MET). 0 relative to Pass 2.
- No other disagreements exist. The orchestrator compared every cell, not just the subtotals.

## Combined Scoring

| Variant | Quant (×0.50) | Qual (×0.50) | **Final Score** | Debate Tiebreaker (L1) |
|---------|---------------|--------------|-----------------|-------------------|
| V1 (analyzer / sonnet) | 0.4846 | 0.4167 | **0.9013** | 3/19 points won = 15.8% |
| V2 (qa / grok-4.7) | 0.4856 | 0.4333 | **0.9190** | 9/19 points won = 47.4% |

Arithmetic:
- V1 = 0.5×0.96927 + 0.5×0.83333 = 0.48464 + 0.41667 = **0.90130**
- V2 = 0.5×0.97124 + 0.5×0.86667 = 0.48562 + 0.43333 = **0.91895**

**Margin**: 0.91895 − 0.90130 = 0.01765, i.e. 1.77 percentage points. That is below the 5% threshold (`|Δ| < 0.05`).

**Tiebreaker applied**: Yes.

- **Level 1 (debate performance)** decides it. Source: `debate-transcript.md:183-191`, scored over 19 points. V1 won 3 (C-004, C-006, X-002). V2 won 9 (S-001, S-002, S-003, S-005, S-006, C-003, C-005, X-001, X-003). 6 were merge/either and 1 (C-001) was unresolved.
  - The difference is 6/19 = 31.6 points, far outside 5%, so L1 resolves the tie in favour of **V2**.
- Levels 2 and 3 were not needed. For the record:
  - L2 (correctness count) is 4/5 vs 4/5, which would also tie.
  - L3 (input order) would pick V1.
- Sensitivity check: the merge/either and unresolved points have no winner, so excluding them gives V2 9 of the 12 decided points (75%).

## Selected Base: Variant 2 (grok-4.7[1m] : qa — sc:reflect-reviewer, haiku slot)

### Selection Rationale

The scores are a near-tie, and V2 leads on both layers:
- **Quantitative**, 0.9712 vs 0.9693: V2's full section coverage and denser cited content outweigh V1's single-contradiction advantage on IC and its higher SR.
- **Qualitative**, 26 vs 25: V2's lead is Structure-5 (schema conformance), worth +1. V1's gain on Correctness-1 is cancelled by its loss on Correctness-3. Each variant's Risk-2 / Risk-3 gain cancels the other's after the re-evaluation.

The tiebreaker is decisive. V2 won 9 debate points to V1's 3, and most of V2's wins are on the artifact skeleton a merged card needs:
- S-002: schema-exact grounding gaps.
- S-003: per-requirement acceptance table.
- S-005 / X-003: correct omission of the advisory correctness-gap channel.
- X-001: correct Drift boundary.
- C-005: explicit precedence walk and `regression_present`.

V1's wins (C-004, C-006, X-002) are local content corrections. They graft cleanly onto V2's structure. Grafting V2's schema onto V1 would mean restructuring the base instead, which is riskier.

V2's defects are correctable in the refactor plan:
- The "10 lines" claim (C-002).
- The `tests/__init__.py` rejection (C-004).
- Over-strong absence tags (X-002).
- Gap 1's internal inconsistency (C-001).
- Unscoped confidence (C-006).
- No mitigation for Risk 4.

Both variants keep the same 4-class verdict (0 Authorized / 0 Necessary / 0 Drift / 0 Regression), and base selection does not change it.

### Strengths to Preserve from Base (V2)

1. Grounding-gaps YAML with all 6 taxonomy fields (`taxonomy:140-147`), including `decision_needed_by_user` (S-002, V2:49-62).
2. Coverage findings table F-001..F-004, with a spec→task→diff→source chain and Grounded/unevidenced tags (S-003/U-003, V2:23-28).
3. Explicit precedence walk (Regression > Drift > Necessary > Authorized) and the stated reasons Regression cannot be minted (S-001/U-007, V2:19, :64).
4. Correct Drift boundary: T-103 has no hunk, so it is missing provenance, not unmapped work (X-001, V2:64; INV-014 ADDRESSED).
5. No advisory correctness-gap section, because `greet` has no sibling. Falsy and whitespace behaviour routed to Risks plus a spec amendment (S-005/X-003, V2:81, :84, :91; INV-013 ADDRESSED).
6. "Ledger-true and acceptance-false" framing; R-003 not signed off (C-003, V2:11, :43).
7. Body range `changes.patch:6-9` (header at `:5`) (C-002 body part, V2:44).
8. Runtime-surface and reachability skip check (U-006, V2:38, :96), R-001 static-closure independence (U-009, V2:30), model-identity disclosure (U-008, V2:1, :9).
9. Tagged Risks table (S-006, V2:77-82) and the conditional `pythonpath = .` recovery path (Risk-3 MET, V2:90).
10. The 4-class verdict 0/0/0/0, `status: partial`, `needs_human_decision: true` (V2:11, :69-72).

### Strengths to Incorporate from Non-Base Variant (V1)

1. **C-004**: affirm that T1 recommendation 3 (`tests/__init__.py`) is valid under pytest's default prepend mode, tagged [INFERRED]. Source: the V1 side. V1:36 and V1:65 do not rule on rec 3 themselves. Affirming it is the debate consensus (`debate-transcript.md:172, :248`), with INV-010 caveats.
2. **X-002 / U-002**: snapshot absence is not live absence, so tag it [INFERRED]. Source: V1 Challenge #4 (V1:32-36), refined by INV-003.
3. **C-001**: split the provenance gap and the execution gap into separate rows. Source: V1 GG-1 and GG-2 (V1:22-23), rendered in V2's schema.
4. **C-006**: scoped split confidence, 0.8 for `src/greeting.py` and about 0.5 overall. Source: V1:74.
5. **U-001**: `S_dev_density = 0/1` cannot see T-103. Source: V1 Challenge #2 (V1:30).
6. Mitigation for the weak `test_empty` oracle. Source: V1 Correctness gap #2 (V1:45), moved from the advisory channel into V2's Risks/Recs.
