# Adversarial Debate Transcript

## Metadata
- Depth: deep
- Rounds completed: 2 (Advocate + Skeptic)
- Focus areas: value, complexity
- Advocate count: 3 (one per variant) + 1 Skeptic
- Convergence: 83% (10 of 12 proposals have advocate/skeptic within 3 points on value)

---

## Round 1: Advocate Statements

### V1 Advocate (Proposals A-E)

**A (Code-level evidence tier)**: Value 8, Complexity 3. Evidence: 4 of 31 metrics (W-1, W-8, W-9, R-8) scored from code analysis, not pipeline execution. Without evidence tiers, scores.jsonl is misleading for programmatic consumers.

**B (Correct failure classification)**: Value 9, Complexity 5. Evidence: spec-fidelity FAILED correctly — detected 3 HIGH fabricated-ID deviations. Current spec cannot distinguish "gate caught a defect" from "gate is broken." Needs `expected_gate_failures` in eval suite YAML.

**C (CONDITIONAL_PASS verdict)**: Value 9, Complexity 2. Evidence: eval report YAML frontmatter invented `release_quality_gate: CONDITIONAL_PASS`. EvalReport.overall_passed:bool cannot represent this. Cheapest proposal — one field rename, one enum expansion.

**D (Regression-guard scoring mode)**: Value 7, Complexity 4. Evidence: steps 1-8 treated as binary PASS/REGRESSION guards, explicitly excluded from delta numerator. 80% of stages needed a scoring mode the spec doesn't define. Saves 40 unnecessary judge calls per evaluation.

**E (Duration variance thresholds)**: Value 4, Complexity 1. Evidence: 28% variance on generate-opus. Weakest proposal — cheap insurance policy, not high-value feature.

### V2 Advocate (Proposals F-J)

**F (Partial run scoring)**: Value 8, Complexity 9 (low effort). Evidence: all 4 runs were PARTIAL. RunResult has no steps_completed/steps_total. Trivial: 2 integer fields, 20-30 lines across 2 files.

**G (Gate rejection vs functional failure)**: Value 7, Complexity 6 (medium effort). Evidence: global runs exited 0 but internal min_lines gate rejected output. Current L2 checks (_exit_code_zero, _artifacts_produced) both PASS, wasting judge tokens on 9-line garbage.

**H (Per-step variance tracking)**: Value 6, Complexity 5. Evidence: debate step 28% duration variance + 48% artifact size variance vs extract 10%. NFR-EVAL.3 is meaningless at run level when steps vary this much.

**I (Minimum completeness thresholds)**: Value 5, Complexity 8 (low effort). Evidence: global runs completing 3/8 steps counted toward minimum. Interacts with F — if per-step aggregation exists, this becomes a warning rather than a hard threshold.

**J (Worktree reuse policy)**: Value 4, Complexity 9 (trivial). Evidence: real execution reused one worktree sequentially. FR-EVAL.6 underspecifies lifecycle. One AC addition.

### V3 Advocate (Proposals K, L→C+L, M)

**K (--eval-mode / --continue-on-fail)**: Value 9, Complexity 2. Evidence: unconditional fail-fast prevented wiring-verification from executing. Root cause of CONDITIONAL_PASS. 3 lines in EvalConfig, 5-10 lines in executor. Most practical proposal for eliminating incomplete coverage.

**C+L (Ternary verdict — merged)**: Value 8, Complexity 2. Evidence: two independent analyses converged on identical solution. ABComparison already uses string verdicts — EvalReport is the inconsistent outlier.

**M (Auto-detect LLM fabrication)**: Value 7, Complexity 3. Evidence: both local runs independently fabricated IDs with 100% consistency. Structural safety net catches fabrication regardless of which pipeline or prompt is used.

---

## Round 2: Skeptic Rebuttals

**A**: Value 3, Complexity 5. "Fix execution gap with K, don't add a tier for it. This is premature formalization of a transient problem."

**B**: Value 6, Complexity 4. "Real need, but may be a reporting concern rather than data model concern. The gate *did* fail."

**C+L**: Value 9, Complexity 3. "ACCEPT — the eval literally violated the spec to express the result. Strongest evidence in the set."

**D**: Value 4, Complexity 4. "Existing spec handles this through Layer 4 configuration. Risk of creating two diverging scoring tracks."

**E**: Value 2, Complexity 2. "Arbitrary threshold from one observation. Duration is infrastructure noise, not quality signal."

**F**: Value 7, Complexity 2. "ACCEPT — minimal, clean extension. Only question: coordinate with C+L to avoid overlap."

**G**: Value 3, Complexity 5. "Pipeline-specific concern, not a framework concern. L2 correctly catches this as functional failure."

**H**: Value 3, Complexity 6. "N=2 is not statistics. Premature formalization."

**I**: Value 2, Complexity 3. "Existing fail-fast and FR-EVAL.14 handle this. Redundant."

**J**: Value 3, Complexity 1. "Implementation detail, not spec-level. But trivial to add."

**K**: Value 7, Complexity 3. "ACCEPT — practical, low risk. Note: belongs on pipeline spec, eval spec documents usage."

**M**: Value 5, Complexity 4. "Clever but narrow. Fix the prompt instead."

---

## Scoring Matrix

| Proposal | Advocate Value | Skeptic Value | Avg Value | Advocate Complexity | Skeptic Complexity | Avg Complexity | Agreement |
|----------|---------------|---------------|-----------|--------------------|--------------------|----------------|-----------|
| A | 8 | 3 | 5.5 | 3 | 5 | 4.0 | SPLIT |
| B | 9 | 6 | 7.5 | 5 | 4 | 4.5 | PARTIAL |
| C+L | 9/8 | 9 | 8.7 | 2/2 | 3 | 2.3 | AGREED |
| D | 7 | 4 | 5.5 | 4 | 4 | 4.0 | PARTIAL |
| E | 4 | 2 | 3.0 | 1 | 2 | 1.5 | AGREED |
| F | 8 | 7 | 7.5 | 9* | 2 | 2.0† | AGREED |
| G | 7 | 3 | 5.0 | 6 | 5 | 5.5 | SPLIT |
| H | 6 | 3 | 4.5 | 5 | 6 | 5.5 | PARTIAL |
| I | 5 | 2 | 3.5 | 8* | 3 | 3.0† | SPLIT |
| J | 4 | 3 | 3.5 | 9* | 1 | 1.0† | PARTIAL |
| K | 9 | 7 | 8.0 | 2 | 3 | 2.5 | AGREED |
| M | 7 | 5 | 6.0 | 3 | 4 | 3.5 | PARTIAL |

*V2 Advocate used inverted complexity scale (9=easy). †Normalized to standard scale (1=trivial, 10=massive).

## Convergence Assessment
- Points agreed (within 2 on value): C+L, E, F, K = 4/12 = 33%
- Points partially agreed (within 4): B, D, H, J, M = 5/12 = 42%
- Points split (>4 gap): A, G, I = 3/12 = 25%
- Overall convergence: 75% (partial+agreed)
