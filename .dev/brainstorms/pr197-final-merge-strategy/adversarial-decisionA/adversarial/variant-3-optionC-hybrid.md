# Option C — HYBRID: instance-level floor + hard class-diversity preference with graded invariant

**Thesis:** Take both structural protections and let the environment decide which binds. Instance-level independence is the **always-on floor**; executor-class disjointness is a **hard preference** enforced whenever the executor class reliably resolves — with the graded invariant retained and a loud (never tier-collapsing) degrade signal when it genuinely cannot be satisfied.

## Construction
1. **Floor (always):** every Tier-2 reviewer is a fresh subagent, brief carries no executor formation context, every card blind-calibrated (#197 §7.1 mechanisms 1–3). The tier is **never degraded T2→T1 on the basis of model-class identity** — this removes master's worst failure mode.
2. **Hard preference (when class resolves):** when the executor class is **reliably** known (`--executor-model` / `EXECUTOR_MODEL_CLASS` / task-builder frontmatter `executor_model_class` — NOT the commit-author heuristic), reflect composes the panel to **exclude the executor class via backfill** (master §7.1:630 logic), preserving master's "≥1 weight-disjoint reviewer" guarantee.
3. **Graceful, observable degrade:** if exclusion cannot be satisfied (alias-poor) the panel fills with the best available distinct classes (repeating only as last resort) and emits a loud `t2_model_class_diversity: degraded` + a new `executor_exclusion_unsatisfiable: true` — but **stays Tier-2**. No silent same-class pass; no tier collapse on a guess.
4. **Graded invariant retained, conditionally:** keep `executor_model_class NOT IN reviewer_model_classes` as a graded assertion **gated on `executor_class_source ∈ {flag, env, frontmatter}`** (asserted when identity is reliable; waived — not failed — when only the heuristic or unknown).

## 1. Anti-self-confirmation strength
- Strongest of the three: defeats **both** the context/instance failure mode (floor) **and** the weight-level representational-bias failure mode (hard preference) that §1 mechanism #1 targets. Neither pole covers both.

## 2. Diversity guarantee
- Matches master's "≥1 weight-disjoint reviewer" in the common (rich-alias + reliable-identity) case, while never paying #197's silent-same-class risk; and never shrinks below a full Tier-2 panel.

## 3. Robustness
- Inherits #197's no-tier-collapse robustness (floor) AND surfaces diversity deficits loudly (master's signal), but as a warning that keeps the review running rather than killing it.

## 4. Enforceability
- Keeps a graded invariant — but **honestly conditioned** on identity reliability, so it never fails-open silently (B's flaw) and never fails the run on a bad guess (A's flaw).

## 5. Merge cost
- **Highest.** Net-new design not present in master or #197: the conditional graded assertion, the `executor_exclusion_unsatisfiable` signal, the source-reliability gating, and eval fixtures for the new degrade path. Requires its own spec/tasklist; bundling it into this merge widens scope and delays the additive value (doc skills, EV gates).

**Strongest concession:** it is the only option that is *not yet built*; choosing it converts a merge-adjudication into a feature project and risks scope creep on a PR whose primary value is additive.
