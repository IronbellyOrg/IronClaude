# Option B — Adopt #197's INSTANCE-LEVEL independence

**Thesis:** Accept #197's instance-level-independence model as canonical. Executor class stays in the reviewer pool; `--executor-model`/`EXECUTOR_MODEL_CLASS` accepted as provenance and ignored; the three exclusion telemetry fields removed; class diversity preserved as a soft preference (`t2_model_class_diversity: full|degraded`). Guarantee rests on fresh subagent spawn + no formation context + blind calibration.

## 1. Anti-self-confirmation strength
- The §1/Mehta failure mode names the **instance carrying formation context** re-grading its own work: *"…present when it re-evaluates."* A fresh subagent, with no executor reasoning-trail and a blind-calibrated card, is **not that instance** — the named failure mode is defeated by construction even at same class.
- #197 keeps all three §1 mechanisms (heterogeneous ensemble, blind calibration, evidence-validator). Executor-class exclusion is NOT one of §1's three named mechanisms — it is a master-only add-on layered on top.

## 2. Diversity guarantee
- Exclusion can only **shrink** the representational frame (HEAD §7.1: executor `opus` + pool `{sonnet,haiku,opus}` minus `opus` = the smaller `{sonnet,haiku}`). Instance-level keeps the executor's class as one more frame *and* still prefers maximal distinct-class coverage.
- In a rich multi-vendor proxy the soft preference will, in practice, almost always seat ≥1 off-class reviewer anyway — capturing the representational-bias benefit **without** master's failure modes.

## 3. Robustness
- Instance-level **never collapses T2→T1 on executor identity**. Master's exclusion throws away the entire heterogeneous-ensemble (mechanism #1, its *strongest* mechanism) whenever the executor class collides and backfill can't reach a disjoint N=2 — trading the whole review to honor a class-purity constraint.
- It deletes a **fail-open** resolver: master falls back to a commit-author log heuristic and, when unknown, emits `executor_class_resolved: false` — the guarantee silently evaporates exactly when provenance is missing.

## 4. Enforceability
- The deleted exclusion telemetry was **NON-STABLE** and read by no §9.3 consumer (per the 1.5.1 changelog note) → removing it is non-breaking. The instance-level guarantee is enforced structurally by the spawn mechanism + blind calibration, which remain graded.
- A graded invariant you can't satisfy in alias-poor moments (forcing T1) is worse than a structural guarantee that always holds.

## 5. Merge cost
- Lands as authored in #197 (commit 658bf8f) — no reconciliation against an exclusion shell. EV-1…EV-4 + the task-builder CLI-mode clause-1 ("pin to OUR instance-level skill, NOT a class-removing variant") are written **assuming this model**, so they integrate with zero polarity rework.

**Strongest concession:** representational bias lives in the weights; a fresh same-class reviewer shares the executor's blind spots, so on the *weight-level* axis instance-level is strictly weaker than exclusion — decisive in a class-poor environment.
