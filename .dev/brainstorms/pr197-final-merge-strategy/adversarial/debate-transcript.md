# Adversarial Debate Transcript — PR #197 Merge Adjudication

Grounded 3-agent panel (read-only, branch `feat/rf-harness-sync` vs `git show origin/master`). Each agent carried a verified facts-sheet to prevent fact re-derivation drift.

## Decision A — anti-self-confirmation model (EXCLUSION vs INSTANCE-LEVEL)

### Agent 1 — assigned stance: defend INSTANCE-LEVEL (#197)
- **Honest verdict:** instance-level is the stronger guarantee **in this rich-alias environment**, confidence **0.72**.
- Key points: §1/Mehta names the *instance*; #197 keeps all three §1 mechanisms; exclusion can only shrink the frame; demotes the right thing (diversity) to a soft preference, not the guarantee; deletes a brittle commit-author resolver that fails open.
- **Conceded strongest counter:** representational bias lives in the weights → a fresh same-class reviewer shares the executor's blind spots; "decisive in a class-poor environment — but this is not that environment."
- Boundary: master strictly stronger only in class-poor/single-vendor environments.

### Agent 2 — assigned stance: defend EXCLUSION (master)
- **Honest verdict:** master's exclusion is the stronger guarantee **in this environment**, confidence **0.62**.
- Key points: #197 contradicts its own unchanged §1 mechanism #1 (per-model bias stacking is a weight-level property); demotes the §1-load-bearing property to a "soft good" so a same-class panel passes silently; deletes the only graded invariant (`executor_model_class NOT IN reviewer_model_classes`); backfill in a rich-alias env keeps the panel full *and* class-disjoint-from-executor; the collapse path is rare and is a *loud true signal*; frontmatter `executor_model_class` neutralizes the brittle-heuristic objection.
- **Conceded strongest counter:** the empirical magnitude of "executor's *own* class as reviewer" as a miss source is unquantified in the cited literature; the dominant gain may come from fresh-spawn + blind calibration (which #197 keeps).
- **Proposed merged design (Option C):** instance-independence as the floor + exclusion+backfill as a *hard* preference with the graded invariant when class identity resolves — "would beat both."

### Synthesis (orchestrator)
Near-even split (0.72 vs 0.62), both moderate. Convergent facts: instance-level wins the context/robustness/simplicity axes; exclusion wins the weight-level-bias axis and keeps a graded invariant. Both independently surfaced the same hybrid (Option C) as superior. → **Genuine product fork requiring user sign-off.** Recommended default = **keep master's exclusion** (stronger on the specific guarantee here; smaller change; asymmetric risk favors conservatism — see RISKS §8). Option C filed as a follow-up, not a merge blocker.

## Decision B — runner `inline_directive` + guard loosening

### Agent 3 — assigned task: try to FALSIFY "the directive is dead, reject it"
- **Falsification attempt: failed — "none survive."**
- Decisive evidence: `_build_prompt()` is consumed only on the Tier-1 branch (`runner.py:462`), never the ensemble branch (`runner.py:452-456` → `run_tier2_ensemble` via in-process swarm dispatch, `ensemble.py:3-5`); Tier-1 has no Wave 3/3C/4 (`SKILL.md:688, 143, 1936`). The directive instructs the only recipient that reaches it to perform waves that don't exist on its path. The directive self-declares non-structural (`runner.py:382-385`).
- **Guard loosening risk:** real but mild. The only new `"subagent"` tokens are inside the directive (`runner.py:381/389/391`); the loosening exists solely to admit them. The bare-`"subagent"` ban is load-bearing against prose/string-described nesting — the exact failure mode #197 reintroduces.
- **Verdict:** REJECT directive + guard-loosening + `test_inline_directive.py`; keep master's strict guard. Confidence **0.9**.

### Synthesis (orchestrator)
High-confidence convergence. The ensemble route is the structural fix; the directive is dead-and-wrong and its only effect is to weaken a safety invariant. → **REJECT.**
