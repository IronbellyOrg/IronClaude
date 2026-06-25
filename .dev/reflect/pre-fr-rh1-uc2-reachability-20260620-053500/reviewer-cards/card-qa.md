# UC-2 Reachability Gate -- QA PRE-Execution Coverage/Gap Audit

**Reviewer:** Tier-2 Reflect Reviewer (QA, haiku-class)
**Spec:** `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/.dev/reflect/pre-uc2-reachability-gate-20260620-041729/REPORT.md`
**Tasklist:** `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/.dev/tasks/to-do/TASK-RF-uc2-reachability-gate-20260620-043410/TASK-RF-uc2-reachability-gate-20260620-043410.md`
**Date:** 2026-06-20
**Lens:** Testability -- can each obligation be EXECUTABLY falsified, not merely asserted in prose?

---

## Per-Obligation Testability Table

### R1 -- Real-boot-only Regression

| Dimension | Detail |
|---|---|
| **Spec rule** | Only `real boot` observing sink absent can set `unreachable`/Regression |
| **Tasklist coverage** | Phase 3: prose updates to SKILL.md, taxonomy, template, rubric, grader-extensions. Phase 5: consumer tests + eval case `uc2-reachability-real-boot-regression-proof` (conditional: "if implementable in the harness") |
| **Executable assertion today** | NONE. `test_verdict_mapping.py` tests `halted_regression` via `regression_present: true` but has no reachability-specific falsifier. No test asserts that `derive_verdict` requires `reachability_real_boot_ran: true` when `reachability_unreachable > 0`. |
| **Verification gap** | The consumer test at Phase 5 item 3 asserts "proxy/oracle-only evidence cannot satisfy real-boot Regression proof" -- this is a negative control, not a positive falsifier. The real-boot eval case is conditional. Missing: a unit test that sets `reachability_unreachable: 1` + `reachability_real_boot_ran: false` and asserts Regression is NOT set. |
| **Severity** | HIGH |
| **Fix suggestion** | Add `test_real_boot_required_for_regression()` to `test_verdict_mapping.py`: load `pass.yaml`, set `reachability_unreachable=1`, `reachability_real_boot_ran=false`, assert `regression_present` is NOT set or verdict does NOT route to HALTED. |

### R2 -- Telemetry-only --no-reachability

| Dimension | Detail |
|---|---|
| **Spec rule** | `--no-reachability` sets skip telemetry, MUST NOT create Grounding Gap, `needs_human_decision`, or `status: partial` |
| **Tasklist coverage** | Phase 5: YAML fixture + eval case `uc2-reachability-no-reachability-skip`; wrapper tests for `--print-command --no-reachability` |
| **Executable assertion today** | PARTIAL. The fixture asserts null ledger + zero counters. No `derive_verdict` unit test proving that a contract with `reachability_skip_reason: "--no-reachability"` does NOT route to HALTED/BLOCKED. |
| **Verification gap** | Grader assertions (`yaml_field`, `regex_absent`) can check fixture outputs, but the verdict mapper is not tested against this telemetry shape. A future change could set `status: partial` on skip and `derive_verdict` would route HALTED without any unit test catching it. |
| **Severity** | MEDIUM |

### R3 -- Telemetry-only spec-and-tasklist-absent

| Dimension | Detail |
|---|---|
| **Spec rule** | No spec/tasklist = telemetry-only skip, no Grounding Gap, no `needs_human_decision`, no status change |
| **Tasklist coverage** | Phase 5: eval case `uc2-reachability-missing-inputs-skip`; YAML fixture with null ledger + zero counters |
| **Executable assertion today** | IDENTICAL GAP to R2. Consumer fixture checks shape; no `derive_verdict` falsifier. |
| **Severity** | MEDIUM |

### R4 -- Contract version 1.6.0

| Dimension | Detail |
|---|---|
| **Spec rule** | Reachability fields ship under `contract_version: "1.6.0"`; `1.5.0` = D13-only |
| **Tasklist coverage** | Phase 3: bump version in SKILL.md, report-template, cost-profile. Phase 6: `rf-qa` agent with `LENS: evidence-quality-and-contract-schema` adversarially checks `1.6.0` + D13-only `1.5.0` preservation |
| **Executable assertion today** | WEAK. Relies on a report-only QA agent + grader `yaml_field` assertions in eval. No unit test asserts `1.5.0` fixtures do NOT contain `reachability_*` fields. No schema-validation test rejecting reachability fields under `1.5.0`. |
| **Verification gap** | The existing `pass.yaml` fixture is `contract_version: "1.3.0"` -- no `1.5.0` fixture exists at all. No test enforces the invariant "reachability fields present => contract_version >= 1.6.0". |
| **Severity** | MEDIUM |

### R5 -- Wrapper plumbing + docs parity

| Dimension | Detail |
|---|---|
| **Spec rule** | `superclaude reflect run` exposes `--reachability/--no-reachability`; `_build_prompt()` forwards disabled exactly once; docs parity |
| **Tasklist coverage** | Phase 4: models.py (`reachability: bool`), config.py, commands.py (Click option), runner.py (`_build_prompt()`), docs + parity test updates. Phase 5: help/prompt/tmux/--print-command tests |
| **Executable assertion today** | STRONGEST of all obligations. Existing test surface (`test_cli_smoke.py`, `test_docs_cli_parity.py`, `test_promote_plumbing.py`) already covers help, docs parity, print-command, tmux forwarding patterns. New tests plug into established patterns. |
| **Verification gap** | Minor: no integration test running `superclaude reflect run --no-reachability` end-to-end against a fake tasklist and asserting the telemetry-only contract output. The existing tests mock `ClaudeProcess`. This is acceptable for unit coverage but leaves the tmux forwarding seam untested in a real subprocess. |
| **Severity** | LOW |

### R6 -- Producer eval fixture

| Dimension | Detail |
|---|---|
| **Spec rule** | Producer-level eval fixture forcing Step 5.6 to produce reachability fields from real inputs |
| **Tasklist coverage** | Phase 5: eval cases under `.dev/eval-workspaces/sc-reflect/evals/evals.json` + grader assertions |
| **Executable assertion today** | WEAK. The eval harness runs against pre-recorded outputs in `with_skill/outputs/`. It does NOT invoke the actual `/sc:reflect` skill to exercise Step 5.6. The grader checks that produced output files contain expected strings/YAML. This is a consumer-of-producer check, not a producer-level invocation. |
| **Verification gap** | No test invokes `grader.py` or the eval runner to verify the full pipeline. The "real-boot-proven" case is explicitly deferred ("if implementable"). The eval harness as currently structured cannot exercise the producer -- it can only grade its outputs. |
| **Severity** | HIGH |

### R7 -- Field-presence + consistency rules (7 reachability_* fields)

| Dimension | Detail |
|---|---|
| **Spec rule** | UC-2 contracts must emit 7 reachability fields with consistency invariants |
| **Tasklist coverage** | Phase 3: SKILL.md stable contract section adds field definitions + consistency YAML rules. Phase 6: `rf-qa` schema agent checks fields |
| **Executable assertion today** | NONE. No unit test for the 5 consistency rules (gate-ran => non-null ledger; unreachable>0 => real_boot_ran; unproven>0 => grounding_gaps_path; skip_reason => zero counters; etc.). No `derive_verdict` test exercises these invariants. |
| **Verification gap** | The consistency rules are YAML pseudocode in SKILL.md, not enforced in Python. A change could set `reachability_unreachable: 1` + `reachability_real_boot_ran: false` + `regression_present: false` and no unit test would catch the invariant violation. Missing a `test_reachability_consistency_invariants()` module. |
| **Severity** | HIGH |

### R8 -- Bounded cost

| Dimension | Detail |
|---|---|
| **Spec rule** | Replace zero-cost claims with bounded estimates; cap 12 scanned, 36 turns, 1 real-boot invocation |
| **Tasklist coverage** | Phase 3: update `cost-profile.yaml` and `ops-integration.md` |
| **Executable assertion today** | MINIMAL. Only verifiable via grader `regex_absent` (no `reachability_gate_added_tokens: 0`) and `yaml_field` on the cost-profile. No test asserting the numerical bounds are consistent (e.g., 12 * 3 = 36). |
| **Verification gap** | Trivial but load-bearing: if someone sets `reachability_gate_max_side_effect_requirements_scanned: 99` without adjusting the cap, no test catches the arithmetic inconsistency. The spec works the example (12 * 3 = 36) but does not enforce it mechanically. |
| **Severity** | LOW |

### R9 -- Advisory-only semantic fallback

| Dimension | Detail |
|---|---|
| **Spec rule** | Only explicit `durable_sink:`/`@sink` annotations trigger blocking gate; semantic classification = advisory only |
| **Tasklist coverage** | Phase 3: SKILL.md + taxonomy updates. Phase 5: eval case for semantic-fallback advisory + consumer test "semantic fallback does not route to DEGRADED/HALTED by itself" |
| **Executable assertion today** | PARTIAL. The consumer test checks that semantic evidence alone does not affect verdict routing. No falsifier proves that an input WITH `durable_sink:` annotation but NO real-boot proof correctly produces `unproven` (not `unreachable`). The `durable_sink:` annotation predicate has no dedicated test. |
| **Verification gap** | Missing: a test that semantic-only signals cannot set `reachability_unproven > 0` (the spec says semantic fallback "MUST NOT set `reachability_unproven`"). The grader `regex_absent` on fixture output can check this, but only at eval time. No unit test in the verdict mapper. |
| **Severity** | MEDIUM |

---

## POST Reflect Wrapper Shape Check

| Check | Status |
|---|---|
| Item shape: `superclaude reflect run <tasklist> --depth deep --fix --promote` | PASS -- matches spec |
| No `--base` | PASS |
| No `--reflect` | PASS |
| No `<base>..HEAD` range | PASS |
| No `/sc:task` | PASS |
| No agent-spawn directive | PASS |
| Recursion guard (`SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE`) | PASS -- existing `test_marker_suppression.py` covers |
| Exit-code handling (0=proceed, 10/11/2=surface) | PASS |

## Final QA Gate Agent Count

| Phase | Agents | Report-only? |
|---|---|---|
| Phase 2 gate | 2 (rf-qa + rf-qa-qualitative) | Yes |
| Phase 3 gate | 2 (rf-qa + rf-qa-qualitative) | Yes |
| Phase 4 gate | 2 (rf-qa + rf-qa-qualitative) | Yes |
| Phase 5 gate | 2 (rf-qa + rf-qa-qualitative) | Yes |
| Phase 6 M3/I20 | 6 (3 rf-qa + 3 rf-qa-qualitative) | Yes |
| Phase 6 fix agent | 1 (rf-qa, fix_authorized=true) | No (edits) |
| Phase 6 structural verify | 1 (rf-qa) | Yes |
| Phase 6 semantic verify | 1 (rf-qa-qualitative) | Yes |

**Total distinct agents spawned:** 21 over the task lifetime. The Phase 6 gate uses >=6 report-only lens agents (PASS). Fix is serialized behind consolidated findings (PASS).

---

## Coverage Summary

| Obligation | Executable Test Coverage | coverage_pct | best_practice_grade |
|---|---|---|---|
| R1 -- Real-boot-only Regression | Negative control only; no positive falsifier | 0.30 | 2/5 |
| R2 -- Telemetry-only --no-reachability | Fixture shape checked; no verdict-mapper test | 0.50 | 3/5 |
| R3 -- Telemetry-only spec-absent | Same as R2 | 0.50 | 3/5 |
| R4 -- Contract 1.6.0 | QA agent + grader; no schema-enforcement test | 0.40 | 2/5 |
| R5 -- Wrapper plumbing | Strong unit test coverage; missing e2e | 0.80 | 4/5 |
| R6 -- Producer eval fixture | Consumer-of-output grading; no producer invocation | 0.30 | 2/5 |
| R7 -- 7 fields + consistency | Prose rules only; zero unit tests for invariants | 0.10 | 1/5 |
| R8 -- Bounded cost | Regex checks only | 0.60 | 3/5 |
| R9 -- Advisory semantic fallback | Consumer test exists; no durable_sink falsifier | 0.50 | 3/5 |
| **WEIGHTED AVERAGE** | | **0.42** | **2.6/5** |

---

## Critical Gaps (Severity-Sorted)

### HIGH

1. **R7 consistency invariants have zero executable assertions.** Five consistency rules are YAML pseudocode in SKILL.md. No `derive_verdict` test, no schema validator, no grader assertion enforces `reachability_unreachable > 0 => reachability_real_boot_ran: true`. This is the most dangerous gap because the invariants are load-bearing for the R1 proof bar but have no mechanical enforcement.

2. **R1 real-boot proof bar lacks a positive falsifier.** No test asserts that `unreachable` Regression CANNOT be proven without `reachability_real_boot_ran: true`. The existing regression test (`halted_regression` fixture) predates reachability and tests `regression_present: true` directly.

3. **R6 producer eval fixture grades pre-recorded outputs, not producer behavior.** The eval harness cannot invoke Step 5.6. The "producer-level" claim is met only by manual fixture authoring, not by automated producer exercise.

### MEDIUM

4. **R4 no version-gating test.** No test enforces "reachability fields under 1.5.0 => BLOCKED" or "UC-2 without reachability fields at 1.6.0 => Grounding Gap".

5. **R2/R3 skip paths not tested in verdict mapper.** A regression in `derive_verdict` could route telemetry-only skips to HALTED without any unit test catching it.

6. **R9 no `durable_sink:` annotation falsifier.** The explicit annotation predicate has no dedicated test proving the boundary between "annotated = blocking-eligible" and "semantic-only = advisory".

### LOW

7. **R5 missing end-to-end subprocess test.** All wrapper tests mock `ClaudeProcess`. Acceptable for unit coverage but the tmux forwarding seam has no real-subprocess smoke.

8. **R8 cost arithmetic not enforced.** No test that 12 * 3 >= cap = 36.

---

## Distinction: Executable Tests vs. Prose Verification

Of the 9 obligations, the following have **ONLY prose verification** (QA agent reading files, regex checks in grader, or semantic QA lenses):

| Obligation | Only-Prose Components |
|---|---|
| R7 | All 5 consistency rules -- zero executable assertions |
| R4 | Version gating -- relies on QA agent read + grader yaml_field |
| R1 | Real-boot proof bar -- relies on spec prose in SKILL.md, no unit falsifier |
| R6 | Producer invocation -- grader checks pre-recorded output files |

The remaining obligations (R2, R3, R5, R8, R9) have at least one executable test path but lack falsifiers for the negative/invariant cases.

---

## Recommendations (Priority-Ordered)

1. **Add `test_reachability_consistency_invariants()` to `tests/cli/reflect/test_verdict_mapping.py`**: Parameterized tests for all 5 R7 consistency rules. This is the single highest-ROI test addition.

2. **Add `test_real_boot_required_for_regression()`**: Assert that `reachability_unreachable > 0` without `reachability_real_boot_ran` cannot produce a HALTED/Regression verdict.

3. **Add `test_telemetry_skip_does_not_halt()`**: Parameterized for both `--no-reachability` and `spec-and-tasklist-absent` skip reasons.

4. **Add `test_version_gating()`**: Assert 1.5.0 contracts with reachability fields are rejected or ignored.

5. **Document the eval harness limitation** in the tasklog: the "producer-level" fixture is currently a consumer-of-output grading exercise, not an actual Step 5.6 invocation. Flag as a follow-up for harness-capable real-boot eval.

---

SELF_CONFIDENCE: 0.88
