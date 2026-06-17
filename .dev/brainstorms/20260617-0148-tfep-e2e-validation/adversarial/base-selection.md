# Base Selection + Scoring

## Hybrid score (quantitative + qualitative), standard depth

| Criterion (weight) | A (opus:qa) | B (sonnet:analyzer) | C (haiku:devops) |
|--------------------|:-----------:|:-------------------:|:----------------:|
| Coverage of the 4 outcome dimensions (0.20) | 0.95 | 0.92 | 0.90 |
| Acceptance-criteria rigor / falsification (0.25) | **0.97** | 0.90 | 0.80 |
| Determinism + 3× reproducibility (0.20) | 0.82 | **0.96** | 0.84 |
| Delegability of the embedded prompts (0.15) | 0.88 | 0.86 | **0.92** |
| Audit-trail / aggregation operability (0.15) | 0.84 | 0.88 | **0.95** |
| Concision / signal density (0.05) | 0.75 | 0.85 | 0.88 |
| **Weighted total** | **0.893** | 0.913 | 0.872 |

B edges A slightly on the weighted total (its determinism machinery is the single strongest mechanism),
but **A is selected as the BASE** for these reasons:

1. **Most complete spec body**: A's per-test structure (ID, scope w/ explicit ignore-list, embedded
   prompt, ordered probes, binary criteria, evidence schema) is the cleanest skeleton to graft onto.
2. **The `--fix` nuance**: A alone identified that a naïve `rg -c -- "--fix" == 0` is WRONG (the file
   legitimately contains "NO --fix" prohibition clauses) and specified the correct check
   `FIX_TOTAL == FIX_PROHIBITION`. This is the highest-value insight in the whole debate and protects
   the single most dangerous regression.
3. **Re-derivation-free audit trail** is most explicitly argued in A (command+stdout+exit behind every
   claim → a reviewer trusts-or-reruns one command per criterion, never re-traces the protocol).
4. **Cleanest test boundaries** with an explicit, justified overlap (`--fix` on E3∩E4).

B's higher score is concentrated in **mechanisms** (digest, locale, sha256, class labels) that graft
cleanly ONTO A's body — so the merge takes A's structure and B's determinism engine, losing nothing.

**Base = Proposal A.** Grafts = B's reproducibility/determinism engine + C's orchestration/dashboard.
Convergence 0.88 → PASS.
