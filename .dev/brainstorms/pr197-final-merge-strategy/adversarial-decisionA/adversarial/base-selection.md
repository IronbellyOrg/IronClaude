# Base Selection — Decision A

## Qualitative rubric (merge-decision dimensions, additive binary)

| Dimension | A (exclusion) | B (instance-level) | C (hybrid) |
|-----------|:---:|:---:|:---:|
| Anti-self-confirmation — context/instance axis | 1 | 1 | 1 |
| Anti-self-confirmation — weight-level axis (the agreed-real miss) | 1 | 0 | 1 |
| Diversity guarantee enforced (not just preferred) | 1 | 0 | 1 |
| Observability of same-class panels | 1 | 0→1* | 1 |
| Robustness — no destructive tier-collapse | 0 | 1 | 1 |
| Enforceable graded invariant present | 1 | 0 | 1 |
| Merge-readiness (built today) | 1 | 1 | 0 |
| Cheapest path to the agreed end-state C | 1 | 0 | n/a |
| **Near-term suitability subtotal** | **7** | **3–4*** | **5 (unbuilt)** |

\* B reaches 4 only with its conceded mandatory fix (retain `t2_model_class_diversity` telemetry). It still scores 0 on weight-level defense and enforced diversity.

## Selection
**Base = Option A (executor-class exclusion) as the near-term merge floor**, with **Option C grafted as a funded, non-blocking fast-follow** (the agreed end-state). Option B is **not selected** — its sole near-term advantage (instance-level floor) is preserved as the fast-follow's *target behavior*, while its costs (deletes the enforced + graded + observable weight-level defense) are conceded defects, and INV-201 shows the path to C is dramatically more expensive starting from B.

### Why A wins the near-term (debate evidence)
1. **Defends the agreed-real weight-level miss at merge time** (1 gate) vs B's 6 unenforced post-merge gates (INV-207; conceded by all three advocates in R3).
2. **Cheapest path to C**: from A the fast-follow is *subtractive editing* of existing graded machinery; from B it is *re-authoring* into regions now occupied by contradictory instance-level prose (INV-201; C-advocate reversal in R3).
3. **Retains a graded, observable invariant** (`executor_model_class NOT IN reviewer_model_classes` + telemetry) — auditability that B deletes (conceded defect).
4. **Smallest change for this merge**: keep master; reject #197's rewrite; the only edit is flipping the task-builder CLI-mode clause-1 polarity.

### Strengths to incorporate from non-base (→ refactor plan / fast-follow)
- From **C**: remove the destructive T2→T1 tier-collapse (stay-T2 + `executor_exclusion_unsatisfiable`); restrict the exclusion trigger to reliable identity `{flag, env, frontmatter}` and drop the commit-author `log-heuristic`; relax the graded predicate to *waived-not-failed* when identity is unreliable.
- From **B**: adopt/keep instance-level independence framing as the always-on floor underneath exclusion (it composes — A-002 orthogonality, unanimous); ensure `--executor-model` is meaningful (it is, under A) and emit a clear signal.
- From **INV-202**: the fast-follow must add the reflect-side *reader* for `executor_model_class` (today written-but-unread).

### Edge-case floor check
All options score ≥1/5 on invariant/edge-case awareness (the debate itself surfaced empty-alias, single-vendor, and correlated-vote edge cases). No floor suspension needed. A selected.
