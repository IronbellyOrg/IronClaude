# Invariant Probe Results (Round 2.5)

Independent fault-finder probed the emerging consensus across 6 categories; findings verified against the live tree.

| ID | Category | Assumption | Status | Severity | Evidence |
|----|----------|-----------|--------|----------|----------|
| INV-201 | state_variables | C's "retain master's §11.3 grader + §7.1 backfill as **dormant** scaffolding" while shipping the instance-level floor | **UNADDRESSED→ADDRESSED (R3)** | **HIGH** | #197 HEAD already **deleted** the grader assertion (grep NOT FOUND) and the instance-level rewrite **occupies** §7.1:627/§11.3:1217 ("no executor-class exclusion is applied"); contract :699 "1.5.1 replaces exclusion". Floor+dormant-machinery is one tree-state that cannot exist → near-term is **binary A-or-B**. |
| INV-202 | guard_conditions | `executor_model_class` frontmatter is a usable reliable-identity source today | **UNADDRESSED** | MEDIUM | task-builder WRITES it (CLI mode); reflect READS it nowhere (grep: 0 consumer) — "accepted-and-ignored". The C fast-follow must ADD the reader. |
| INV-203 | guard_conditions | "Retain `t2_model_class_diversity` telemetry" = real observability | ADDRESSED | LOW | That field HAS a consumer (meta-eval aggregator + grader). But it measures class spread, not executor-overlap → not a substitute for the deleted `executor_exclusion_degraded`. |
| INV-204 | count_divergence | N same-class reviewers under the floor = N independent votes | ADDRESSED (disclosed) | MEDIUM | #197:629 concedes "a fresh same-class reviewer still shares the executor's representational stack". N instances ≈ 1 correlated representational vote; merge math still tallies N. Floor-alone does NOT defend the weight-level miss. |
| INV-205 | collection_boundaries | C degrades correctly in a single-vendor window | UNADDRESSED (C-only, not built) | MEDIUM | C's "unsatisfiable but stay-T2" panel becomes all-same-class-as-executor = silently identical to B, while emitting a "still-T2" signal that *reads* as defended → C's safety claim collapses to B in the exact degenerate window where weight-level bias is likeliest. |
| INV-206 | interaction_effects | "EV-1..EV-4" all live in reflect SKILL.md; floor choice flips task-builder clause-1 | ADDRESSED | LOW | Only EV-1 (:688) + EV-2 (:810) are in reflect SKILL; **EV-3/EV-4 live in task-builder** (confirms the merge-strategy artifact). EV-1 checks reviewer-card COUNT (orthogonal to class) → floor choice does not weaken it. |
| INV-207 | sufficiency_challenge | "Ship floor + fast-follow C" ALONE achieves the anti-self-confirmation goal | **UNADDRESSED→ADDRESSED (R3)** | **HIGH** | Falsifier (conceded): if fast-follow unfunded → shipped = pure B → agreed-real weight-level miss undefended across 6 post-merge gates (author tasklist → fund → build reader → add gated grader → add telemetry → eval). **A enforces class-disjointness at 1 gate (merge time)** → A is strictly safer-by-default. |

## Summary
- Total findings: 7 — HIGH: 2 (INV-201, INV-207), MEDIUM: 3, LOW: 2.
- The 2 HIGH items were **UNADDRESSED at the close of Round 2** → blocked convergence → forced **Round 3**, where all advocates conceded and updated (both now ADDRESSED).
- Net effect: the probe **falsified the "cheap C via dormant scaffolding" framing** and established that the path to end-state C is cheapest **from A** (subtractive edits to existing graded machinery), and that A is **safer-by-default** for the agreed-real weight-level miss.
