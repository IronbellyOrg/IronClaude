# Base Selection: REFACTOR-PROPOSAL Cross-Env

## Quantitative Layer

| Metric                    | Weight | Variant 1 (pr86) | Variant 2 (T4-env) | Notes                                                                            |
| ------------------------- | ------ | ---------------- | ------------------ | -------------------------------------------------------------------------------- |
| Requirement coverage      | 0.30   | 0.75             | 0.85               | V2 covers Cause #1 + #2 + #3 + #4; V1 covers #2 + #3a + #4 (misses Cause #1)     |
| Internal consistency      | 0.25   | 0.95             | 0.90               | V1's formula is one mechanism end-to-end; V2 has 3 enforcement layers, all consistent |
| Specificity ratio          | 0.15   | 0.90             | 0.85               | V1 has concrete diff sketches with +/- markers; V2 has concrete content but no diff markers |
| Dependency completeness    | 0.15   | 0.85             | 0.75               | V1 explicitly shows Changes A+B+C compositional dependency; V2 has weaker dependency narrative |
| Section coverage          | 0.15   | 0.85             | 0.95               | V2 has explicit "What this does NOT fix" + 5 hard-fail rules + 5 verification tests |
| **Quant score (weighted)** | —      | **0.852**        | **0.857**          | (computed as RC×0.30 + IC×0.25 + SR×0.15 + DC×0.15 + SC×0.15)                    |

## Qualitative Layer (30-criterion rubric, abbreviated for quick depth)

| Dimension                            | V1 Met | V2 Met | Notes                                                                                                                            |
| ------------------------------------ | ------ | ------ | -------------------------------------------------------------------------------------------------------------------------------- |
| Completeness (5 criteria)             | 4/5    | 4/5    | V1 misses Cause #1 coverage; V2 misses eval-corpus + migration                                                                   |
| Correctness (5 criteria)              | 5/5    | 3/5    | V2's file-path is wrong (`.claude/` instead of `src/superclaude/`) — counts as 2 correctness failures (wrong target + violates rule) |
| Structure (5 criteria)                | 5/5    | 4/5    | V1 uses true diff fences; V2 uses markdown insertions                                                                            |
| Clarity (5 criteria)                  | 4/5    | 5/5    | V2's numbered sections are cleaner; V1's per-change deep-dives are denser                                                        |
| Risk Coverage (5 criteria)            | 4/5    | 5/5    | V2's "What this does NOT fix" + GitHub-URL detection + asymmetry smell catches more failure modes                                |
| Invariant & Edge Case Coverage (5)   | 5/5    | 4/5    | V1's Change E corpus is the explicit invariant guard; V2's V1-V5 are one-off                                                     |
| **Qual score**                       | **27/30 = 0.900** | **25/30 = 0.833** | Edge-case floor (1/5) satisfied for both                                                              |

**Edge-case floor check**: Both variants score ≥1/5 on Invariant & Edge Case Coverage. Both eligible as base.

## Position Bias Mitigation

- Pass 1 (V1, V2 order): V1 wins on correctness + structure + invariants; V2 wins on clarity + risk coverage.
- Pass 2 (V2, V1 order): Same verdicts. No position bias detected.

## Combined Scoring

| Variant | Quant (50%) | Qual (50%) | **Combined** |
| ------- | ----------- | ---------- | ------------ |
| V1 (pr86 substrate)  | 0.852       | 0.900      | **0.876**    |
| V2 (T4 environment)  | 0.857       | 0.833      | **0.845**    |

## Tiebreaker

Variants are within 5% (0.876 vs 0.845 — 3.5% delta), so tiebreaker applies.

- **Level 1 (Debate performance)**: V1 won 9 diff points; V2 won 5; 7 ties or shared. **V1 wins.**
- Level 2 not needed.

## Selected Base: Variant 1 (pr86-substrate)

**Rationale**:

1. V1 correctly targets `src/superclaude/*` (SoT) per CLAUDE.md ABSOLUTE RULE; V2's `.claude/*` paths are a project-rule violation that must be migrated before merge regardless.
2. V1's gated-minimum formula is more auditable than V2's three-cap precedence rules.
3. V1's Change E (eval corpus) is a load-bearing prevention-of-regression artifact V2 lacks.
4. V1's migration table is a real backward-compat asset V2 lacks.

**Critical V2 contributions that MUST be merged into the base**:

1. **Change 4 (Tier 2 audit gate)** — closes Cause #1 which V1 entirely misses. This is the single most-important integration.
2. **Evidence-class typed taxonomy** — V2's 5-value `evidence_class` is more expressive than V1's binary `runtime_check`; merge as an extension to V1's frontmatter.
3. **Hard-fail rule 4 (GitHub WebFetch URL detection)** — operational signal V1 doesn't surface.
4. **V1-V5 verification plan (real-card replay)** — co-exists with V1's Change E fixtures.

## Failure-mode coverage matrix (post-merge target)

| Cause                                                    | V1 closes? | V2 closes? | Merged closes? |
| -------------------------------------------------------- | ---------- | ---------- | -------------- |
| #1 — Calibrator non-execution (the dominant defect)       | ✗          | ✓ (Ch 4)   | ✓              |
| #2 — Rubric evidence-class disjunction                   | ✓          | ✓          | ✓              |
| #3a — Verdict-direction asymmetry                         | ✓          | ✓ (partial) | ✓              |
| #3b — Falsification standard                              | ✓          | ✗          | ✓              |
| #4 — Eval-suite silent-green                              | ✓ (Ch E)   | ✗          | ✓              |
