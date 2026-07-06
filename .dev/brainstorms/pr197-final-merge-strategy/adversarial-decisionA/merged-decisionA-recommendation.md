<!-- Provenance: produced by /sc:adversarial (Mode A, deep, 3 rounds + invariant probe) -->
<!-- Base: Variant 1 (Option A) -->
<!-- Incorporated: Variant 3 (Option C) as funded fast-follow; Variant 2 (Option B) observability point -->
<!-- Convergence: ~0.86 (CONVERGED after forced Round 3) -->

# Decision A — Merged Recommendation (adversarial, 3 rounds)

## Verdict

**Near-term (this merge): Option A — keep master's executor-class EXCLUSION. Reject #197's instance-level rewrite.**
**End-state (funded, non-blocking fast-follow): Option C — soften A into the hybrid.**
**Option B (pure #197 instance-level): rejected** as a near-term target.

Confidence in near-term = A: **~0.82** (up from the pre-debate 0.62). The deep debate did not rubber-stamp the prior — the strongest opposing advocate (C) **reversed onto A** for the near-term, and the independent invariant probe **falsified** the only framing under which B/floor-now was cheap.

## Why the debate moved the needle (new evidence beyond Round-0)

1. **The near-term choice is binary A-or-B — "instance-level floor + dormant exclusion machinery" cannot exist (INV-201).** #197 already *deleted* master's §11.3 grader assertion + §7.1 backfill + 3 telemetry fields, and its instance-level prose *occupies the same regions*. You merge one or the other. This collapsed C's "cheap decomposition" and forced the real comparison.

2. **A is safer-by-default for the agreed-REAL weight-level miss (INV-207).** All three advocates agreed: two fresh *same-class* reviewers share the executor's training-level blind spots (#197 concedes this verbatim at §7.1:629), and the Tier-2 merge math still counts them as N independent votes (INV-204). A enforces class-disjointness **at merge time (1 gate)**; B leaves the miss undefended across **6 unenforced post-merge gates** unless a fast-follow is funded.

3. **The cheapest path to the agreed end-state C starts from A, not B (C-advocate reversal, R3).** From A the fast-follow is *subtractive editing* of existing graded machinery (remove tier-collapse, narrow the trigger, relax the grader). From B every piece is *net-new authoring into regions occupied by contradictory instance-level prose*.

4. **Pure #197 (B) over-deleted observability (B-advocate concession).** It dropped `t2_model_class_diversity` observability along with the enforcer — "indefensible as a pair." Even a pure-B world would need that telemetry back.

## What ships in THIS merge (Option A)

Exactly the Decision-A rows of the parent strategy artifact (`../merged-requirements.md` §2, §4, §5):
- **REJECT** #197's instance-level rewrite: restore master's `refs/reviewer-spec.md` + `refs/reflection-rubric.md`; keep master's §7.1 exclusion, §11.3 three-way partition + grader assertion, and the 3 telemetry fields; keep `contract_version: "1.7.0"`.
- **PORT regardless** (model-agnostic, unaffected by Decision A): EV-1/EV-2 (reflect SKILL §8/§9), EV-3/EV-4 + `reflect_post_mode`/`--cli` (task-builder), the 3 doc skills, tech-* rewrites, `/task` lens QA, rf-agents.
- **One coupling edit:** flip the task-builder CLI-mode clause-1 polarity to the exclusion model ("pin to OUR `sc-reflect-protocol` skill (executor-class-exclusion), NOT a non-excluding variant").

## The funded fast-follow (Option C) — separate tasklist, NOT a merge blocker

Edit A → C (all *subtractive/narrowing* on existing graded machinery):
1. **Remove the destructive tier-collapse**: on executor-class collision that cannot reach a disjoint N=2, stay **Tier-2**, fill best-available distinct classes, and emit `executor_exclusion_unsatisfiable: true` + `t2_model_class_diversity: degraded` (loud, non-collapsing).
2. **Narrow the exclusion trigger to reliable identity** `executor_class_source ∈ {flag, env, frontmatter}`; **drop the commit-author `log-heuristic`** from the trigger (it is the live fail-open footgun — A-advocate + B-advocate + C-advocate all flagged it).
3. **Add the reflect-side reader** for `executor_model_class` (today written by task-builder frontmatter but unread — INV-202).
4. **Gate the graded invariant** `executor_model_class NOT IN reviewer_model_classes` on identity reliability: *asserted* when reliable, *waived-not-failed* otherwise.
5. **Eval**: prove a same-class panel is actually avoided when identity is reliable, and that the unsatisfiable branch stays Tier-2.

## Honest open item (the one unresolved MEDIUM — X-004)

A's "enforced-at-merge" defense is only as strong as executor-class *resolution*. On the primary path (task-builder POST writes `executor_model_class` to frontmatter) it is reliable; on a bare-CLI/heuristic path it can fail open. **The resolver hit-rate on this proxy is unmeasured** (B-advocate's standing reservation). Cheap de-risk before/with the merge: emit `executor_class_source` to telemetry and check, over a handful of real reflect runs, how often it is `flag|env|frontmatter` vs `log-heuristic|unknown`. If `log-heuristic`/`unknown` dominates, **raise the priority of the fast-follow** (which drops the heuristic) — A's day-1 guarantee is weaker than it looks in that regime, though still ≥ B (which has no enforcement at all).

## One-line sequencing
Merge **A** now (reject the rewrite; land all the additive/EV value); open the **A→C** fast-follow tasklist as a funded, scheduled, non-blocking follow-up; add the `executor_class_source` telemetry check to size its urgency.
