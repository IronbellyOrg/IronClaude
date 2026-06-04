# Reviewer Card — R1.3 UC-2 Adversarial Review

**Reviewer:** haiku (automated)
**Date:** 2026-06-02
**Branch:** refactor/roadmap-pipeline-r0-r1-rewrite
**Parent commit:** 90a8fa67

---

## Q1: `assert_step_reachable` generalization beyond `_build_steps` literals

**Verdict:** Drift — justified generalization but not faithful to §MVR §2 wording

**Evidence:**
- BUILD-REQUEST §MVR §2 line 115: "Wire `build_certify_step()` as the final step; CodeAssertion guarantees no future step ships unwired." The word "unwired" implies reachability, not literal containment.
- `src/superclaude/cli/roadmap/code_assertions.py:27-123` — `assert_step_reachable` accepts EITHER shape 1 (Step literal in `_build_steps`) OR shape 2 (`build_certify_step` has a production caller).
- `src/superclaude/cli/roadmap/code_assertions.py:187-228` — `_build_certify_step_has_production_caller` walks the entire executor.py AST for any `Call(func=Name("build_certify_step"))`, excluding self-calls.
- Task Step 8.1 (task L508): The design doc asked for the AST walk to "confirm `step.id == 'certify'` appears in the `_build_steps` dispatch map."
- `src/superclaude/cli/roadmap/code_assertions.py:38-44` (docstring): Explicitly documents the two legitimate dispatch shapes and cites design doc §7.3 option (a).

**Analysis:** The task instruction (Step 8.1) scoped the assertion to `_build_steps` literals. The delivered code generalizes to include dynamic dispatch via `_build_certify_step_has_production_caller`. §MVR §2's verbatim text ("CodeAssertion guarantees no future step ships unwired") actually SUPPORTS the broader interpretation — "unwired" = unreachable from any production path, not "absent from a specific list literal." The generalization is semantically more faithful to the BUILD-REQUEST than the narrow task instruction, but it deviates from what Step 8.1 explicitly asked for.

**Deviation class:** Drift (justified — the BUILD-REQUEST wording supports the broader interpretation; no harm done)
**Confidence:** 0.92

---

## Q2: CRITICAL — `gate_passed` code_assertions enforcement at RUNTIME

**Verdict:** Regression — fail-open shim is runtime-dormant for the certify assertion

**Evidence:**
- `src/superclaude/cli/pipeline/gates.py:93-98` — When `code_assertions` are defined but `envelope is None or repo_root is None`, the function returns `True, None` (FAIL-OPEN). This is the backward-compat shim.
- `src/superclaude/cli/pipeline/executor.py:267` — The live production call site: `gate_passed(gate_target, step.gate)` — **no `envelope=`, no `repo_root=`** passed.
- `src/superclaude/cli/pipeline/executor.py:329` — The remediation recheck: `gate_passed(gate_target, step.gate)` — **same omission**.
- `src/superclaude/cli/pipeline/gates.py:36-40` (docstring): "When either is `None` and the criteria define code_assertions, the assertions are silently skipped -- backward-compat shim for R1.3 call sites that do not yet plumb envelope/repo_root. R1.6 cleanup deletes this skip-path once all callers pass both."

**Analysis:** The CERTIFY_GATE has `code_assertions=[CodeAssertion(..., check_fn=assert_step_reachable, ...)]`. At runtime, `gate_passed` is called from `pipeline/executor.py` WITHOUT the `envelope` and `repo_root` keyword arguments. This means the `envelope is None` branch at `gates.py:94` is ALWAYS taken, and `assert_step_reachable` is **NEVER invoked at runtime**. The assertion is enforced only by the CI test (`tests/roadmap/test_dispatch_reachability.py:test_certify_step_reachable`), which calls the assertion function directly.

This is a self-contradiction: the entire purpose of §MVR §2 / Contract #2 is to enforce dispatch-reachability as a live gate, not just a unit test. The fail-open shim was documented as "backward-compat" for pre-R1.3 gates that predate the code_assertions slot, but applying it to a NEW gate whose sole reason for existence is this assertion makes it a regression — the gate passes even if the certify step is unwired, as long as envelope/repo_root aren't plumbed.

The task's Phase 10 summary line (task L10) even flags this: "R1.6 CARRY-FORWARD (High): delete gate_passed shim + plumb envelope into live cli/pipeline/executor.py gate path or certify assertion stays runtime-dormant."

**Deviation class:** Necessary staging deviation (explicitly acknowledged by the team as a carry-forward; not an accidental regression, but still a gap that should be flagged). The fail-open behavior itself is consistent with Contract #5/R1.6 targets for deletion, but applying it to a NEW assertion whose sole purpose is to catch an unwiring is self-defeating.

**Confidence:** 0.97

---

## Q3: `assert_envelope_artifacts_present` — task-required or dead-but-tested?

**Verdict:** Authorized but dead code — implemented but never wired into any gate

**Evidence:**
- Task Step 8.3 (L516): "a function `assert_envelope_artifacts_present(envelope, repo_path) -> Finding | None` analogous for envelope coverage."
- `src/superclaude/cli/roadmap/code_assertions.py:126-184` — The function is implemented.
- Grep across `src/`: Zero references outside `code_assertions.py:126` (definition). Not imported by `gates.py`, not wired into any `GateCriteria`.
- Grep across `tests/`: Only referenced in `test_dispatch_reachability.py:20` (import) and `test_dispatch_reachability.py:147` (signature invariant test).
- No test actually exercises the function's logic (no `test_envelope_artifacts_present_*`).

**Analysis:** The function was task-required (Step 8.3 L516). It is defined and exported, passes the signature invariant test, but is never wired into a gate. It is dead code that happens to be tested for shape compliance only. No gate calls `assert_envelope_artifacts_present.check_fn`.

**Deviation class:** Necessary staging deviation (the function is implemented as asked, but wiring is deferred — likely because the envelope's artifact-tracking is not fully live yet in R1.3, and the assertion is a placeholder for when it is).

**Confidence:** 0.95

---

## Q4: Step count budget — ≤14 genuinely met?

**Verdict:** Compliant — step count is 13 + 1 dynamic = 14 live

**Evidence:**
- `src/superclaude/cli/roadmap/gates.py:1547-1562` — `ALL_GATES` has 14 entries: extract, generate-A, generate-B, diff, debate, score, merge, anti-instinct, test-strategy, spec-fidelity, wiring-verification, deviation-analysis, remediate, certify.
- `src/superclaude/cli/roadmap/executor.py:2182` — `_build_steps` constructs 13 `Step(...)` objects (certify is NOT a Step literal in this function).
- `src/superclaude/cli/roadmap/executor.py:2108-2179` — `_run_certify_after_remediate` dynamically constructs + executes a 14th step (certify) via `build_certify_step()`.
- `src/superclaude/cli/roadmap/executor.py:3409` — `execute_roadmap` calls `_run_certify_after_remediate(config, results)` at the end.
- Task L102 / L185: Acceptance gate #6 — step count ≤ 14.

**Analysis:** The `_build_steps` function returns 13 Step constructions. ALL_GATES lists 14 gate entries (certify is the 14th). The certify step is constructed dynamically after remediate passes, so the live execution runs 14 steps. The "budget:unaffected" wording in the docstring (executor.py L2121) is slightly misleading — the budget IS affected in that 14 steps run instead of 13, but the acceptance criterion (≤14) is met. The implementation choice (dynamic construction vs. Step literal in `_build_steps`) is an engineering decision to avoid modifying `_build_steps` while still executing the step.

**Deviation class:** Compliant
**Confidence:** 0.98

---

## Q5: `build_certify_step` runs a real LLM subprocess every successful roadmap run

**Verdict:** Authorized by §MVR §2 — behavioral scope is exactly what was requested

**Evidence:**
- BUILD-REQUEST §MVR §2 line 115: "Wire `build_certify_step()` as the final step"
- `src/superclaude/cli/roadmap/executor.py:2165-2170` — `build_certify_step()` constructs a Step with `CERTIFY_GATE`, then `roadmap_run_step(certify_step, config, lambda: False)` executes it as a ClaudeProcess subprocess.
- `src/superclaude/cli/roadmap/executor.py:2133-2138` — Guard: no-op when no remediate step PASSED.
- `src/superclaude/cli/roadmap/executor.py:3403-3409` (execute_roadmap): `_run_certify_after_remediate(config, results)` is the wiring point.
- The certify step has always been an LLM step (it generates a certification-report.md). The R1.3 change is about HOW it is wired into the dispatch, not WHETHER it invokes an LLM.

**Analysis:** The certify step was already part of ALL_GATES (14th entry). Before R1.3, the task states (task L10, research/02 §1.3) that `build_certify_step` had "ZERO production callers" — meaning the certify step was defined but never actually executed in the production dispatch. R1.3 fixes this by giving it a production caller (`_run_certify_after_remediate` called from `execute_roadmap`). This IS a behavioral scope expansion (from "never runs" to "runs every time remediate passes"), but it is explicitly authorized by §MVR §2 ("Wire build_certify_step() as the final step"). The BUILD-REQUEST explicitly wants the certify step to be wired and executed. The scope creep concern would only apply if the certify step were doing something beyond what its gate/prompt already specified — which it is not.

**Deviation class:** Authorized
**Confidence:** 0.95

---

## Overall Recommendation: SHIP-WITH-NOTES

### Summary

| Question | Verdict | Deviation Class | Confidence |
|----------|---------|----------------|------------|
| Q1: assert_step_reachable generalization | Justified drift | Drift | 0.92 |
| Q2: CERTIFY_GATE assertion runtime-dormant | FAIL-OPEN at runtime | Necessary staging | 0.97 |
| Q3: assert_envelope_artifacts_present dead | Implemented, not wired | Necessary staging | 0.95 |
| Q4: Step count ≤14 | Met (13+1 dynamic) | Compliant | 0.98 |
| Q5: Certify runs LLM subprocess | Explicitly authorized | Authorized | 0.95 |

### Load-bearing concern

**Q2 is the only finding that warrants attention.** The `code_assertions` slot exists in the data model, the `gate_passed` function has the dispatch branch, and the CERTIFY_GATE carries the assertion — but the production `gate_passed` call sites in `pipeline/executor.py:267,329` do not pass `envelope=` or `repo_root=`. This means the entire R1.3 code-graph assertion machinery is inert at runtime; the certify gate's `code_assertions` are always skipped because `envelope is None` triggers the backward-compat `return True` branch.

This is a known carry-forward (documented in the task file's own summary at line 10: "R1.6 CARRY-FORWARD (High): delete gate_passed shim + plumb envelope into live cli/pipeline/executor.py gate path or certify assertion stays runtime-dormant"). The team is aware. The question is whether shipping with a runtime-dormant assertion is acceptable for R1.3. It is, if the CI test is the intended enforcement mechanism for this release cycle. If the assertion is meant to be a live gate, this is a blocker.

### Notes

- Q1's generalization is defensible and arguably more correct than the narrow task instruction.
- Q3's `assert_envelope_artifacts_present` is implemented but unwired — dead code with no functional impact.
- Q4's step-count claim of "budget:unaffected" is technically true (still ≤14) but semantically misleading (13 static + 1 dynamic = 14, not 13).
- Q5's behavioral change (certify now actually executes) is the intended effect of R1.3, not scope creep.
