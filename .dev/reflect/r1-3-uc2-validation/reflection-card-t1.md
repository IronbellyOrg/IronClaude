---
artifact: reflection-card-t1
mode: post (UC-2)
target: Phase 8 / R1.3 — GateCriteria.code_assertions + first CodeAssertion
task: TASK-RF-20260531-042405
parent_commit: 90a8fa67
created_date: 2026-06-02
---

# Tier 1 Grounded Reflection Card — R1.3

## Scope (grounded via git diff + Read)

- Modified: `pipeline/models.py` (+37), `pipeline/gates.py` (+36/-2),
  `roadmap/gates.py` (+17), `roadmap/executor.py` (+82).
- New: `roadmap/code_assertions.py`, `tests/roadmap/test_dispatch_reachability.py`.
- PRESERVE files (`commands.py`, `structural_checkers.py`, `convergence.py`):
  `git diff --stat` empty — UNCHANGED. ✅ (grounded)
- S_scope = 6 files; S_domains = 2 (code + tests).

## Grounded findings (per adversarial point)

### Point 1 — design §6.2-vs-§7.3 inconsistency + assertion generalization
- GROUNDED: `code_assertions.py:assert_step_reachable` PASSES if EITHER
  `"certify" in _build_steps` step ids OR `build_certify_step` has a
  production caller in executor.py (`_build_certify_step_has_production_caller`).
- Design doc §6.2 scoped to `_build_steps` only; §7.3 wired dynamically
  (outside `_build_steps`). The two §§ were internally inconsistent.
- vs BUILD-REQUEST §MVR §2 ("reachable"): the generalization is MORE faithful
  to the spec word "reachable from a production entry point," not less.
- Documented in Phase 8 Findings ("DESIGN DEVIATION") + aggregation.
- PRELIM CLASS: **Necessary deviation** (vs the Step-8.1 design doc, the agent's
  own intermediate plan) — forced by a discovered inconsistency, documented,
  does NOT contradict the authoritative spec. vs the spec itself: compliant.

### Point 2 — gate_passed envelope-None shim → certify assertion runtime-dormant
- GROUNDED: `pipeline/gates.py:94-98` returns `True, None` when `envelope is
  None or repo_root is None` AND code_assertions are defined.
- GROUNDED: ALL production `gate_passed(...)` call sites omit envelope/repo_root
  — `pipeline/executor.py:267` and `:329` (the live runtime gate path),
  `sprint/executor.py:842`, `cli_portify/executor.py:417`,
  `cleanup_audit/executor.py:137`. None pass envelope.
- THEREFORE: the CERTIFY_GATE code_assertion is SKIPPED at pipeline runtime;
  enforced ONLY via `test_dispatch_reachability.py` (CI).
- vs §MVR §2 "CodeAssertion guarantees no future step ships unwired": the
  guarantee is provided via CI (a PR that unwires certify fails the test), not
  at runtime. The spec does not mandate runtime-vs-CI enforcement locus.
- Documented: Phase Findings PG8.1, aggregation, proceed-decision, Follow-Up
  Items (High priority R1.6 carry-forward).
- RISK FLAG: the shim is a NEW fail-OPEN default (`return True` on None). The
  task's own Contract #5 / R1.6 explicitly targets fail-open defaults for
  deletion. Introducing a new (temporary, documented) fail-open path is in
  tension with the task's anti-fail-open thrust.
- PRELIM CLASS: **Necessary deviation** (R1.3→R1.6 staging; documented; spec
  guarantee met via CI) — NOT Regression. But the fail-open-introduction risk
  is a legitimate finding to escalate.

### Point 3 — assert_envelope_artifacts_present: required or expansion?
- GROUNDED: task item Step 8.3 (task file L516) explicitly says: "a function
  `assert_envelope_artifacts_present(envelope, repo_path) -> Finding | None`
  analogous for envelope coverage."
- PRELIM CLASS: **Authorized** (task-specified verbatim). NOT scope creep.
- Sub-note: it is implemented but NOT wired into any gate (no gate references
  it). It is dead-but-tested today. Worth noting it has no production consumer
  yet (analogous to build_certify_step's prior state, ironically).

### Point 4 — step-count budget (13 _build_steps + dynamic certify = 14 ≤ 14)
- GROUNDED: `_build_steps` returns 13 Step constructions; `ALL_GATES` and
  `_get_all_step_ids` enumerate 14 (certify is 14th).
- Before R1.3 certify NEVER executed (zero callers) → effective live count 13.
- After R1.3 certify executes after remediate-PASS → live count 14.
- Acceptance gate #6 baseline "current (14)" = ALL_GATES count. 14 ≤ 14 holds.
- PRELIM CLASS: **Authorized / compliant** — within budget. NOT sleight-of-hand.
- PRECISION FLAG: the helper docstring + execute_roadmap comment say the budget
  is "unaffected." Precise truth: the `_build_steps` RETURN count is unaffected
  (13); the LIVE EXECUTED count INCREASES 13→14 (certify now runs). Within
  budget, but "unaffected" undersells the new runtime step.

### Point 5 — build_certify_step executing in production
- GROUNDED: `executor.py:2170` `roadmap_run_step(certify_step, config, lambda:
  False)` — certify is an LLM step (not a special-cased branch), so it spawns a
  ClaudeProcess. Call site `execute_roadmap:3409`, post-success path.
- vs §MVR §2 "Wire build_certify_step() as the final step": executing it is
  SPEC-MANDATED. **Authorized**.
- BEHAVIORAL-CHANGE FLAG: `roadmap run` now spawns an additional LLM certify
  subprocess (+latency, +token cost, +certification-report.md) on every
  successful run where remediate passes. Authorized by spec, but a notable
  runtime change that should be explicitly surfaced for user awareness.

## Preliminary deviation tally (T1, pre-ensemble)
- Authorized: 2 (assert_envelope_artifacts_present; certify execution)
- Necessary: 2 (assertion generalization; runtime-dormant shim staging)
- Drift: 0
- Regression: 0 (point #2 examined as regression-candidate → NOT a regression)

## Escalation trigger
§5.3 rule 3: UC-2 + regression-candidate (point #2) → ESCALATE to T2.
User explicitly requested the heterogeneous anti-bias check.

## Open risks for ensemble scrutiny
1. New fail-open shim vs task's anti-fail-open Contract #5 thrust.
2. assert_envelope_artifacts_present has no production consumer (dead-but-tested).
3. "budget unaffected" wording vs live-count 13→14 increase.
4. certify now executes on every run — unflagged magnitude of behavioral change?
