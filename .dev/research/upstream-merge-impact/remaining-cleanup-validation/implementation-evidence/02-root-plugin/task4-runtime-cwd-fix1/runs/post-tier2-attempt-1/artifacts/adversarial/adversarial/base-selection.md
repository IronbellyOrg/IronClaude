# Base Selection Report

## Metadata
- Step 3 author: sc:debate-orchestrator (opus), resumed run, 2026-10-25.
- Context: debate status BLOCKED_BY_INVARIANTS (INV-006). Base selection runs as the error-handling `no_convergence` force-selection by score; non-convergence is documented in debate-transcript.md and invariant-probe.md.
- Quantitative layer: computed deterministically by the orchestrator (`uv run --no-project python` line/regex counts over the variant text; no LLM judgment).
- Qualitative layer: two independent read-only scorer Tasks (general-purpose, model opus). Pass 1 forward order (V1 then V2), agentId a77e58179482c6469. Pass 2 reverse order (V2 then V1), agentId ad5288a0e2a5f4d0f. Both ran in parallel and neither saw the debate or probe artifacts. Disagreements went to a third read-only re-evaluation Task (general-purpose, opus, agentId a4b0274602da97075), whose verdict is final.
- Variant identities: Variant 1 = reviewer-1, sonnet:analyzer, calibrated C = 0.90. Variant 2 = reviewer-2, haiku:qa (env alias grok-4.7[1m]), calibrated C = 0.92. Self-reported confidences (0.85 / 0.8) are not used anywhere in scoring.

## Quantitative Scoring (50% weight)

| Metric | Weight | Variant 1 (sonnet:analyzer) | Variant 2 (haiku:qa) |
|--------|--------|-----------------------------|----------------------|
| requirement_coverage | 0.30 | 1.000 (R-001, R-002, R-003 all grep-matched; source = spec.md, 3 IDs) | 1.000 (R-001, R-002, R-003 all grep-matched) |
| internal_consistency | 0.25 | 0.929 (2 intra-variant contradictions X-002, X-003 / 28 scorable claims) | 1.000 (0 contradictions / 32 scorable claims) |
| specificity_ratio | 0.15 | 0.925 (37 concrete / (37 + 3 vague) substantive lines) | 0.917 (33 concrete / (33 + 3 vague)) |
| dependency_completeness | 0.15 | 1.000 (internal refs G1/G2/G3 and "see recommendation below" all resolve to ordinal entries; T1/t1-card refs external, excluded) | 1.000 (internal refs "G1" ×2 resolve; T1 external, excluded) |
| section_coverage | 0.15 | 1.000 (10 top-level keys / max 10) | 1.000 (10 / 10) |
| **quant_score** | | **0.971** (0.30 + 0.2321 + 0.1388 + 0.15 + 0.15 = 0.9709) | **0.988** (0.30 + 0.25 + 0.1375 + 0.15 + 0.15 = 0.9875) |

Computation notes (deterministic, re-runnable):
- Scorable claims = 3 fields per grounding gap (evidence_missing, why_not_classifiable, next_evidence_needed) × 3 gaps + agreements + disagreements + risks + recommendations + 3 verdict fields + findings. V1: 9 + 5 + 2 + 5 + 3 + 3 + 1 = 28. V2: 9 + 7 + 1 + 6 + 5 + 3 + 1 = 32. Contradiction counts come from diff-analysis X-002/X-003 (intra-V1). X-001 is a schema-range violation against an external contract, so it is scored in qualitative T5, not IC.
- Specificity: substantive lines exclude the two orchestrator header comments and bare keys. A line is concrete if it has a `file.ext:N` citation or a number. Vague-term regex: appropriate | as needed | properly | adequate | should consider | might | may | various | etc. | best practices | industry standard. V1 vague hits: L39-40 "may fail", L79 "may not import", L81 "adequate". V2 vague hits: L15 "may raise", L37 "may fail", L41 "might hold".
- Section coverage: these are YAML cards with no H2 headings, so top-level YAML keys are the section analogue (protocol deviation, documented). Both have reviewer, persona, findings, grounding_gaps, agreements_with_t1, disagreements_with_t1, risks, recommendations, verdict, self_reported_confidence.

## Qualitative Scoring (50% weight) — Additive Binary Rubric

Final verdicts after dual-pass reconciliation. Evidence is condensed from the scorer CEV tables; line refs are variant line numbers.

### Completeness (5 criteria)

| Criterion | Variant 1 | Evidence | Variant 2 | Evidence |
|-----------|-----------|----------|-----------|----------|
| Covers all explicit requirements | MET | L11 R-001, L12 R-002, L23/L58 R-003 | MET | L27-30 R-001..R-003 and "every requirement-bearing spec span is in the matrix" |
| Addresses edge cases/failures | MET | L47/L80 None/0/whitespace; L38-41 import failure | MET | L15 ModuleNotFoundError; L20-21 None/0/whitespace/non-str |
| Includes dependencies/prerequisites | MET | L34-36 no package markers; L26 needs a run | MET | L14 no markers/config; verification_ran false |
| Defines success/completion criteria | MET | L91 exit-code outcomes; L87 hunk maps to T-103 | MET | L49 "exit 0 with 2 passed"; L45 G1 close condition |
| Specifies out-of-scope items | NOT MET | No evidence found (searched gaps, recs, disagreements) | MET | L30 spec.md:1-3 not a MUST; L61 user confirms out of scope |
| **Subtotal** | **4/5** | | **5/5** | |

### Correctness (5 criteria)

| Criterion | Variant 1 | Evidence | Variant 2 | Evidence |
|-----------|-----------|----------|-----------|----------|
| No factual errors / hallucinations | NOT MET (re-eval) | L35-36 refers to "the audit root's pyproject.toml", which does not exist in audit_repo_root (re-evaluator listing) | MET | git-inventory:5/7-9, task-diff-map:23-38, test:11 all match S |
| Feasible technical approaches | MET | L86-94 regenerate patch / run pytest | MET | L48 conditional run-then-fix |
| Consistent terminology | MET (re-eval) | Drift/Regression/Grounding Gap used per taxonomy:62/80/107-108; L49 uses the term correctly (misfiling is K4) | MET | consistent class names |
| No internal contradictions | NOT MET | L82 vs L13/L20 citations; L45-49 G3 filed as a gap yet denied | MET | none found |
| Claims supported by evidence | MET | file:line citations throughout (L7-13, L57-61) | MET | file:line on nearly every bullet (L26-32) |
| **Subtotal** | **3/5** | | **5/5** | |

### Structure (5 criteria)

| Criterion | Variant 1 | Evidence | Variant 2 | Evidence |
|-----------|-----------|----------|-----------|----------|
| Logical section ordering | MET | findings → gaps → agreements → disagreements → risks → recs → verdict | MET | same schema order |
| Consistent hierarchy depth | MET | uniform two-level lists | MET | uniform depth |
| Separation of concerns | NOT MET | G3 in grounding_gaps while L49/L94 say it belongs elsewhere; meta note under risks (L82) | MET | sections distinct |
| Navigation aids | MET | R-/T-/H1 IDs, G-labels, file:line cross-refs | MET | R-/T-IDs, G1 refs, file:line |
| Artifact-type conventions | NOT MET | L99 `66.7` violates `<float 0.0-1.0>` (SKILL.md:1136) | MET | L64 `0.667` in range |
| **Subtotal** | **3/5** | | **5/5** | |

### Clarity (5 criteria)

| Criterion | Variant 1 | Evidence | Variant 2 | Evidence |
|-----------|-----------|----------|-----------|----------|
| Unambiguous language | NOT MET | L40 "may fail", L79 "may not import", L94 "Optionally" | NOT MET | L15 "may raise", L37 "may fail", L41 "might hold" |
| Concrete over abstract | MET | L42 exact commands; L80 concrete value | MET | L38 "Executed coverage is 0/3"; L48 commands |
| Clear section purpose | MET | each key distinct | MET | each key distinct |
| Terms defined on first use | NOT MET | "T1", "G1-G3" undefined (L56, L65) | NOT MET | "T1", "G1" undefined (L25, L34) |
| Actionable next steps | MET | L85-96 three recs with verifier and priority | MET | L42-62 five recs with verifier and priority |
| **Subtotal** | **3/5** | | **3/5** | |

### Risk Coverage (5 criteria)

| Criterion | Variant 1 | Evidence | Variant 2 | Evidence |
|-----------|-----------|----------|-----------|----------|
| ≥3 risks with probability/impact | NOT MET | only 2 of 5 risks graded (L79, L81) | MET | L37/L38/L41 [INFERRED]-graded; impact at L37, L40 |
| Mitigation per risk | NOT MET | L81, L82 unmitigated | NOT MET | weak-oracle risk L39 has no mitigation |
| Failure modes/recovery | MET | L91 exit-code recovery map | MET | L48 conditional fix and re-run |
| External dependencies | MET | L38-41 pytest import mode; L26 no run | MET | L14 tool-unavailable; L15 import mode |
| Monitoring/validation mechanism | MET | verifiers L87/L91/L95 | MET | verifiers L45/L49/L53/L57 |
| **Subtotal** | **3/5** | | **4/5** | |

### Invariant & Edge Case Coverage (5 criteria)

| Criterion | Variant 1 | Evidence | Variant 2 | Evidence |
|-----------|-----------|----------|-----------|----------|
| Collection/degenerate boundaries | MET | L47/L80 empty, whitespace, None; L8 unmapped_hunks empty | MET | L20-22 '', None, 0, whitespace; L26 unmapped_hunks empty |
| State interactions across boundaries | MET | L32-41 test import vs src layout; L61/L78 done vs diff vs log | MET | L13 import across src/tests; L36 done vs map vs log |
| Guard condition gaps | MET | L47/L80 `if not name` unguarded for non-str/0/None | MET | L21-22 falsy guard; TypeError vs ValueError |
| Count divergence | NOT MET | no analysis; L99 itself mismatches unit | MET | L31 static 2/3 = 0.667 vs L38 executed 0/3 |
| Interaction effects | MET | L68 G3 removal plus G1/G2 still forces partial; L38-40 | MET | L15/L37 collection × marker × import mode |
| **Subtotal** | **4/5** | | **5/5** | |

### Edge Case Floor Check

| Variant | Sixth-dimension subtotal | Eligible | Floor suspended with warning |
|---------|---------------------------|----------|------------------------------|
| 1 | 4/5 | yes | no |
| 2 | 5/5 | yes | no |

### Qualitative Summary

| Dimension | Variant 1 | Variant 2 |
|-----------|-----------|-----------|
| Completeness | 4/5 | 5/5 |
| Correctness | 3/5 | 5/5 |
| Structure | 3/5 | 5/5 |
| Clarity | 3/5 | 3/5 |
| Risk Coverage | 3/5 | 4/5 |
| Invariant & Edge Case Coverage | 4/5 | 5/5 |
| **qual_score** | **20/30 = 0.667** | **27/30 = 0.900** |

## Position-Bias Mitigation

| Criterion | Variant | Pass 1 (V1→V2) | Pass 2 (V2→V1) | Agreement | Final |
|-----------|---------|----------------|----------------|-----------|-------|
| K1 No factual errors | 1 | MET | NOT MET | DISAGREE | NOT MET (re-eval: V1:35-36 names a nonexistent audit-root pyproject.toml; 66.7 → T5, L82 → K4, not double-counted) |
| K3 Consistent terminology | 1 | MET | NOT MET | DISAGREE | MET (re-eval: class names match taxonomy; Pass 2's items are K4/T5 defects) |
| all other 28 criteria | 1 | — | — | AGREE | as Pass 1 / Pass 2 |
| all 30 criteria | 2 | — | — | AGREE (30/30) | as both passes |

Disagreements re-evaluated: 2 (both on Variant 1)
Final verdicts changed: 1 relative to Pass 1 (K1 MET → NOT MET); 1 relative to Pass 2 (K3 NOT MET → MET)
Raw pass totals: Pass 1 V1 21/30, V2 27/30. Pass 2 V1 19/30, V2 27/30. Reconciled: V1 20/30, V2 27/30.

## Combined Scoring

| Variant | Quant (×0.50) | Qual (×0.50) | **Final Score** | Debate Tiebreaker |
|---------|---------------|--------------|-----------------|-------------------|
| 1 (sonnet:analyzer) | 0.4854 | 0.3333 | **0.819** | 0/17 points won (not needed) |
| 2 (haiku:qa) | 0.4938 | 0.4500 | **0.944** | 12/17 points won (not needed) |

**Margin**: 0.125 (12.5 percentage points; above the 5% threshold)
**Tiebreaker applied**: No

## Selected Base: Variant 2 (haiku:qa)

### Selection Rationale
Variant 2 scores higher on both layers: quant 0.988 vs 0.971, qual 27/30 vs 20/30. It also won every non-tied diff point in the debate (12 of 17; ties S-002, C-007, C-009; shared QUALIFY on A-001/A-002), and the Variant 1 advocate itself recommended V2 as base in Round 2. The decisive evidence:
- The machine-consumed completion field is in contract range (X-001; V2:64 = 0.667 = task-diff-map.yaml:34).
- There are no internal contradictions (X-002, X-003, C-004).
- The full R-001..R-003 matrix is present, with executed coverage of 0/3 (C-005).
- There is an actionable false-completion recommendation (C-006).
This selection is a force-selection under BLOCKED_BY_INVARIANTS. It does not declare convergence. INV-006 must be carried into the refactor plan.

### Strengths to Preserve from Base
1. `tasklist_completion_pct: 0.667` and the verdict triple (`regression_present: false`, `status_recommendation: partial`) (V2:63-66).
2. Per-requirement agreements R-001/R-002/R-003 with changes.patch / spec.md line refs, the "every MUST span in matrix" statement, and "Executed coverage is 0/3" (V2:26-32, 38).
3. G1 rationale: the hole is absence from the supplied diff, not tree-wide untracked status (V2:8, 34; C-002).
4. G3 kept as a grounding gap with `decision_needed_by_user: false` (V2:19-24; C-001, X-002).
5. Direct, verified citations to execution.log, git-inventory.txt and task-diff-map.yaml (C-004).
6. Precise weak-oracle statement (V2:39; C-008) and conditional collection remedy (V2:48; C-003).

### Strengths to Incorporate from Non-Base Variants
1. From Variant 1, recommendation 2 verifier (V1:91): the pytest exit-code → class map. Both advocates endorsed it in R2. It MUST be corrected per INV-006 to the full deviation-taxonomy.md:105-113 table (exit 5, 124, flaky retry, unmapped default; exit 1 is Regression only after real collection, execution and an assertion failure).
2. From Variant 1, the no-Drift basis (V1:6-9, V1:22-26): "Drift requires an unmapped hunk" (deviation-taxonomy.md:62). Reword per INV-011 as "none of the Drift signals at :62/:65/:67/:109 fire" with no run (task-diff-map.yaml:38) and `unmapped_hunks: []` (:29).
3. From the debate consensus (A-002, both advocates): scope note `--scope src/` (task-diff-map.yaml:27) in G1 and in the regeneration recommendation. Owner stays `user` (INV-005).
4. From the fault-finder (merge actions accepted by the orchestrator, not advocate-adjudicated): INV-001, INV-002, INV-004, INV-008, INV-014, INV-015, INV-016, INV-017 corrections to base wording. See refactor-plan.md.
