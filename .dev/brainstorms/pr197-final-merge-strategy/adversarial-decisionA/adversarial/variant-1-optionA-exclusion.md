# Option A — Keep master's executor-class EXCLUSION (canonical)

**Thesis:** Reject #197's instance-level rewrite. Keep `sc-reflect-protocol` §7.1 executor-class exclusion + §11.3 three-way partition + the graded invariant + the three telemetry fields exactly as merged on master (`contract_version: "1.7.0"`).

## 1. Anti-self-confirmation strength
- The protocol's own §1 thesis (master SKILL.md:29) quotes Mehta: *"the same representational biases that produced the error are present when it re-evaluates."* Representational bias is a property of model **weights**, not of an instance/context. A fresh **same-class** reviewer shares those weights → shares the executor's systematic blind spots.
- §1 mechanism #1 (master:33) is explicit: reviewers run on *"different model classes … so per-model representational bias does not stack."* Exclusion is the only mechanism that **forces** ≥1 reviewer whose weights differ from the work's author.
- #197 itself concedes the gap (HEAD §7.1): *"A fresh same-class reviewer still shares the executor's representational stack."* Instance-freshness defeats context/anchoring bias only — not weight-level bias.

## 2. Diversity guarantee
- Exclusion + backfill (master §7.1:630) keeps the panel **full AND class-disjoint-from-executor**: executor=sonnet ⇒ rotation becomes `haiku, (qwen|kimi|deepseek|opus)`, restoring N=3 from the resolved alias set. In this rich multi-vendor proxy, backfill essentially always succeeds → ≥2 distinct classes, none matching the author.
- #197 demotes diversity to a *soft preference* and redefines `t2_model_class_diversity: degraded` as "NOT a weakened anti-self-confirmation guarantee" — i.e. a same-class-as-executor panel can pass **silently**.

## 3. Robustness
- The `executor_exclusion_degraded` → T1 path (master §9.3:912) fires only when backfill cannot reach N=2 disjoint — near-impossible with many classes resolvable. When it *does* fire it is a **loud, true signal** of a real diversity deficit, not a silent same-class review.
- Fail-loud-degrade > silent-soft-pass for a reliability-critical audit gate.

## 4. Enforceability
- Master keeps a **graded invariant**: `executor_model_class NOT IN reviewer_model_classes` (§11.3:1211; rubric:172) + telemetry `executor_class_source / executor_class_resolved / executor_exclusion_degraded`. A guarantee you can assert in CI is real; #197 **deletes the assertion** ("There is NO executor-class grader assertion") and the telemetry, leaving the guarantee unobservable.

## 5. Merge cost
- **Smallest change.** Reject the rewrite = restore master's `reviewer-spec.md` + `reflection-rubric.md`, keep master's §7.1/§11.3/telemetry; the only edit is flipping the task-builder CLI-mode clause-1 polarity. EV-1…EV-4 land regardless (model-agnostic). No churn to a merged, tested invariant.
- The brittle commit-author heuristic objection is **moot**: the primary integration path (task-builder POST) writes `executor_model_class` to frontmatter → `executor_class_source: flag`, deterministic.

**Strongest concession:** the empirical magnitude of "executor's *own* class as reviewer" specifically (vs fresh-spawn + blind calibration alone) is unquantified in the cited literature; the dominant gain may come from mechanisms #197 already keeps.
