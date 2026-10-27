# Adversarial Debate: v3.0 Unified Audit Gating -- Proposed Evals

**Date**: 2026-03-19
**Format**: 3-round structured debate
**Expert A**: Advocate (defends eval value, identifies priorities)
**Expert B**: Skeptic (identifies redundancy, questions feasibility, proposes alternatives)

**Evidence base**: 4454 collected tests across roadmap (981), audit (709), integration (35), sprint, pipeline, and unit suites. Key files examined: test_gates_data.py (13-gate definitions), test_pipeline_integration.py (12-step E2E with mock runner), test_integration_v5_pipeline.py (v5 scenarios SC-1 through SC-6), test_convergence.py (27 tests on DeviationRegistry/regression), test_wiring_gate.py (106 tests on wiring analysis), test_wiring_analyzer.py (AST analysis), test_sprint_wiring.py (4-mode hook tests), test_resume_restore.py (resume/state), test_semantic_layer.py (rubric scoring/debate protocol), test_agent_regression.py (agent .md validation).

---

## ROUND 1: Initial Positions

### Expert A (Advocate)

I will defend the proposed evals by focusing on what they add beyond the existing 4454 tests. Let me be precise about the gap each fills.

**Eval 1 -- Full Pipeline Smoke (E2E)**
The existing test_pipeline_integration.py runs a 12-step pipeline with a mock runner that writes gate-passing output. But it uses `_gate_passing_content()` to generate synthetic files that always pass. A true smoke eval would use *realistic* synthetic inputs -- documents that resemble actual spec output with natural variance in formatting, heading structure, and frontmatter values. The existing test proves the orchestration loop works; it does not prove the gates are calibrated to accept realistic production content. That is a real gap.

**Eval 2 -- Gate Rejection Fidelity**
test_gates_data.py validates gate definitions and semantic check functions in isolation. What we lack is a parameterized test that feeds each of the 13 gates a matrix of failure modes (missing frontmatter fields, below min_lines, failing each semantic check independently) through the actual `gate_passed()` function. The existing tests call individual `_*` functions; they do not exercise the full gate evaluation path with composed failure modes. This is the single highest-value eval proposed.

**Eval 3 -- Spec-Fidelity Chain**
test_integration_v5_pipeline.py covers SC-1 through SC-6 with 4 deviation types. But it does not cover: (a) zero-deviation passthrough, (b) AMBIGUOUS-blocks-pipeline, or (c) 3-failed-remediations-halt. The halt test exists in test_integration_v5_pipeline as SC-6 but only tests 2 failed remediations. This eval adds genuine scenario coverage.

**Eval 4 -- Wiring Against Real Codebases**
test_wiring_gate.py has 106 tests but all use inline `textwrap.dedent()` snippets. No test uses a multi-file fixture project that exercises cross-file import resolution, nested class wiring, decorator patterns, or alias detection. Precision/recall measurement against known-ground-truth fixtures is a qualitatively different kind of test.

**Eval 5 -- Convergence Regression**
test_convergence.py has 27 tests covering registry CRUD and split tracking. However, it does not test the 3-run sequence pattern (run1 baseline, run2 improvement, run3 regression detection). The regression detection logic in `_check_regression` is tested in isolation but not as a multi-run sequence with registry persistence across runs.

**Eval 6 -- Resume/State Under Failure**
test_resume_restore.py covers agent restoration, gate diagnostics, dependency-aware resume, and save_state guards. However, the "stale spec detection" and "corrupted state file" scenarios are not present. These are defensive scenarios that matter when the pipeline is interrupted ungracefully.

**Eval 7 -- Sprint Wiring Hook Modes**
test_sprint_wiring.py already tests all 4 modes (off/shadow/soft/full) with SC-006 compliance. This eval as proposed is substantially covered.

**Eval 8 -- Performance/Scale**
No existing benchmark test targets the wiring analysis subsystem with a 200-file project. test_benchmark.py and test_nfr_benchmarks.py exist in the audit and sprint directories respectively, but I would need to verify their scope. Performance regression detection is valuable if deterministic.

**Eval 9 -- Agent Spec Completeness**
test_agent_regression.py already does exactly this -- it parses 5 agent .md files for wiring-related keywords, checks for REVIEW:wiring signals, Optional[Callable] triggers, registry patterns, provider directories, and cross-references. This eval is fully redundant.

**Eval 10 -- Cross-Gate Data Flow**
This is a genuinely new test concept. The existing tests validate individual gate behavior and the pipeline orchestration, but no test traces a single Finding object through all 4 pipeline stages (spec-fidelity, deviation, remediation, certification) asserting ID stability, severity preservation, and status transitions. This tests the data model contract across subsystem boundaries.

### Expert B (Skeptic)

Let me push back on each, grounded in the actual test files I have examined.

**Eval 1 -- Full Pipeline Smoke**
The existing test_pipeline_integration.py already exercises the full orchestration path with 12 steps (now 13 with the additional gate). The "realistic synthetic inputs" distinction is hand-waving. Either the gate checks are deterministic (they are -- they parse frontmatter and count lines) or they require LLM judgment (they do not for structural checks). If the concern is gate calibration, that is better tested by Eval 2's parameterized rejection matrix. A separate E2E smoke test that does essentially the same thing but with "more realistic" fixtures is a maintenance burden with marginal return. I would merge this into Eval 2.

**Eval 2 -- Gate Rejection Fidelity**
I agree this has value. However, let me note that test_gates_data.py already tests many semantic check functions with both passing and failing inputs. The gap is narrower than Expert A claims -- it is specifically the *composed* path through `gate_passed()` with multiple simultaneous failure modes. That is worth testing but could be 13 * 3 = 39 parameterized cases, not the "hundreds" implied by "all gates x failure modes."

**Eval 3 -- Spec-Fidelity Chain**
The zero-deviation passthrough is a trivial case that is arguably tested by any gate-passing pipeline run. The AMBIGUOUS scenario is genuinely useful. The 3-failed-remediation halt is an increment over the existing 2-failed test in SC-6. I would keep the AMBIGUOUS scenario and the halt-at-3 scenario, but drop the zero-deviation and SLIP-only cases as they are covered.

**Eval 4 -- Wiring Against Real Codebases**
This is infeasible as described. "Measure precision/recall" requires ground-truth annotation of every wiring issue in a fixture project. That is a manual labeling task. The inline snippets in test_wiring_gate.py are actually better because each one tests a known, isolated behavior. Multi-file fixture projects create coupling between test expectations and fixture complexity. I would refactor this to "add specific multi-file cross-import scenarios to existing wiring tests" rather than creating whole fixture projects.

**Eval 5 -- Convergence Regression**
This has value. The 3-run sequence pattern is not tested. But the scope should be narrow: test that `_check_regression` correctly identifies when a previously-resolved HIGH reappears. That is 3-4 test cases, not a full eval.

**Eval 6 -- Resume/State Under Failure**
"Corrupted state file" -- what does corruption mean? A truncated JSON file? A file with wrong schema version? These are defensive edge cases. The stale spec detection (spec hash changed between runs) is genuinely useful. I would keep stale-spec and drop the vague "corrupted state" scenarios unless we enumerate specific corruption modes.

**Eval 7 -- Sprint Wiring Hook Modes**
Fully redundant with test_sprint_wiring.py. Drop.

**Eval 8 -- Performance/Scale**
Performance tests are notoriously flaky in CI. "Wiring analysis < 10s" depends on the CI runner's CPU, disk speed, and load. "Memory < 256MB" requires memory profiling instrumentation. This eval is valuable in principle but expensive to make deterministic. I would keep it as a P2 benchmark that runs outside normal CI, not a gating eval.

**Eval 9 -- Agent Spec Completeness**
Fully redundant with test_agent_regression.py. Drop.

**Eval 10 -- Cross-Gate Data Flow**
This is the most interesting proposed eval. Tracing a Finding through the full chain tests something no existing test covers: the data model contract across subsystem boundaries. However, it overlaps with Eval 3 (which also tests the chain). I would merge them: the chain eval should trace specific Finding objects through the 5 scenarios.

---

## ROUND 2: Rebuttals and Refinements

### Expert A (Rebuttal)

I concede the following points to Expert B:

1. **Eval 7 (Sprint Wiring Modes)**: Agreed, fully redundant. Drop.
2. **Eval 9 (Agent Spec Completeness)**: Agreed, fully redundant. Drop.
3. **Eval 8 (Performance)**: Agreed that CI flakiness is a real concern. I accept P2 classification with explicit "benchmark-only, not gating" designation.

I push back on:

**Eval 1 vs Eval 2 merger**: Expert B suggests merging Eval 1 into Eval 2. I partially agree but want to preserve one key aspect: the E2E smoke should verify that the *happy path* works with realistic content, while Eval 2 focuses on *rejection*. These are complementary. The existing test_pipeline_integration.py uses content generated by `_gate_passing_content()` which is a helper that knows exactly what each gate requires -- it is a tautological test. A smoke test with content that was NOT reverse-engineered from gate definitions would verify gate calibration. I propose: keep Eval 1 as a single lightweight smoke test (not parameterized, just one realistic run), and keep Eval 2 as the parameterized rejection matrix.

**Eval 4 (Wiring/Real Codebases)**: Expert B calls precision/recall measurement infeasible. I agree that full ground-truth annotation is too heavy. But I would refine this to: 3 targeted multi-file fixture projects, each with 3-5 known planted issues and 2-3 known non-issues. The test asserts that all planted issues are found (recall = 1.0 for known issues) and no non-issues are flagged (precision check on the known clean items). This is deterministic and maintainable.

**Eval 6 (Resume/State)**: Expert B asks what "corrupted state" means. I will be specific: (a) truncated JSON (simulating process kill during write), (b) missing required keys (schema drift), (c) step results referencing nonexistent output files. These are enumerable and deterministic.

**Eval 3 + Eval 10 merger**: Expert B suggests merging the chain eval with Finding tracing. I agree this is a natural combination. The merged eval would run 5 scenarios, each tracing at least one Finding through all pipeline stages, asserting ID stability, severity preservation, status transitions, and source_layer propagation.

### Expert B (Rebuttal)

I accept Expert A's refinements on Evals 4 and 6. Let me refine my positions:

**Eval 1 (Smoke)**: I accept the "single lightweight smoke" framing but with a condition: the realistic content must be checked into the test fixtures directory as static files, not generated by a helper. If the content is generated, it will inevitably be reverse-engineered from gate definitions and become tautological. Static fixture files maintained separately from gate code provide genuine independence.

**Eval 2 (Gate Rejection)**: Agreed as the highest-priority eval. I want to add one requirement: the parameterization should cover *at least* one test per enforcement tier (STRICT, STANDARD, LIGHT) to verify tier-specific behavior, not just pass/fail.

**Eval 3+10 (Merged Chain)**: Agreed on the merger. The 5 scenarios should be:
- (a) Zero deviations -- Finding enters, exits clean
- (b) SLIP-only -- Finding transitions through remediation
- (c) Mixed types -- Verify routing accuracy
- (d) AMBIGUOUS blocks pipeline -- Verify halt
- (e) Remediation budget exhaustion -- Verify halt with Finding preservation

This gives us both the scenario coverage of Eval 3 and the data-flow tracing of Eval 10.

**Eval 4 (Wiring Fixtures)**: I accept the "planted issues with known ground truth" framing. 3 fixtures with 3-5 planted issues each is maintainable. But I want each fixture to be a minimal reproduction -- not a realistic 50-file project, but a 5-8 file project that exercises specific cross-file patterns (aliased imports, re-exports, nested class registration, decorator-based wiring).

**Eval 5 (Convergence)**: Agreed it should be narrow. 4 test cases: (1) baseline establishes IDs, (2) second run resolves some, (3) third run reintroduces resolved -- regression detected, (4) third run introduces new -- not flagged as regression.

**New eval proposal**: Neither set covers **gate ordering invariants**. The 13 gates execute in a specific sequence where later gates depend on earlier gate outputs. No test verifies that reordering gates produces failures, or that the dependency graph between gates is correctly enforced. This is a structural property of the pipeline that could silently break.

---

## ROUND 3: Convergence and Final Positions

### Expert A (Final Position)

I accept all of Expert B's Round 2 refinements. Let me state my final position on each:

| Eval | Verdict | Rationale |
|------|---------|-----------|
| 1 - Pipeline Smoke | KEEP (refined) | Single run with static fixture files, not generated content. Lightweight. |
| 2 - Gate Rejection | KEEP (highest priority) | Parameterized 13 gates x failure modes through gate_passed(). Include tier coverage. |
| 3+10 - Chain + Data Flow | MERGE | 5 scenarios tracing Finding objects through all stages. |
| 4 - Wiring Fixtures | KEEP (refined) | 3 minimal multi-file fixtures with planted ground truth. |
| 5 - Convergence Regression | KEEP (narrow) | 4 test cases covering multi-run regression sequence. |
| 6 - Resume/State | KEEP (refined) | 3 specific corruption modes + stale spec detection. |
| 7 - Sprint Wiring Modes | DROP | Fully covered by test_sprint_wiring.py. |
| 8 - Performance | KEEP as P2 | Benchmark-only, not gating. Run outside CI. |
| 9 - Agent Spec | DROP | Fully covered by test_agent_regression.py. |
| NEW - Gate Ordering | ADD | Verify gate dependency graph and ordering invariants. |

I accept Expert B's new proposal for gate ordering invariants. The pipeline's correctness depends on gates executing in order, and no test currently verifies that the ordering itself is correct or that violating it produces detectable failures.

### Expert B (Final Position)

I concur with Expert A's table. Let me add one additional point:

The **merged Eval 3+10** is the second-highest priority after Eval 2. It tests the most complex interaction pattern in the system -- data flowing across subsystem boundaries -- and is the most likely place for regressions when any individual subsystem changes.

I also want to note that the **new Gate Ordering eval** should test two things: (1) that `_build_steps()` produces steps in the correct order with correct `inputs` references, and (2) that if a gate's input file is missing (simulating out-of-order execution), the gate fails gracefully rather than crashing.

Final priority assessment:

- **P0** (must have before release): Eval 2 (Gate Rejection), Eval 3+10 (Chain + Data Flow)
- **P1** (should have): Eval 4 (Wiring Fixtures), Eval 5 (Convergence Regression), NEW (Gate Ordering)
- **P2** (nice to have): Eval 1 (Smoke), Eval 6 (Resume/State), Eval 8 (Performance)

My rationale for Eval 1 at P2: the existing test_pipeline_integration.py, while tautological, does exercise the full orchestration path. The static-fixture version adds calibration confidence but is not a release blocker.

My rationale for Eval 6 at P2: the existing resume tests cover the primary scenarios. Corruption edge cases are defensive and unlikely in practice given the atomic write pattern already used in `_save_state`.

---

## FINAL SYNTHESIS AND RECOMMENDATIONS

### Consensus Assessment

| Point | Convergence | Agreement |
|-------|-------------|-----------|
| Eval 7 (Sprint Wiring) should be dropped | FULL | 100% |
| Eval 9 (Agent Spec) should be dropped | FULL | 100% |
| Eval 2 is highest priority | FULL | 100% |
| Eval 3 and 10 should merge | FULL | 100% |
| Eval 8 should be benchmark-only, not gating | FULL | 100% |
| Eval 4 should use planted-issue fixtures, not precision/recall | FULL | 100% |
| Gate Ordering is a genuine gap worth adding | FULL | 100% |
| Eval 1 should use static fixtures | FULL | 100% |
| Eval 1 priority (P0 vs P2) | PARTIAL | 70% -- A leans P1, B says P2 |
| Eval 6 priority | PARTIAL | 80% -- both accept P2 |

**Overall convergence: 95%** -- substantive disagreement only on the priority of Eval 1.

### KEEP AS-IS

None. All kept evals have been refined during debate.

### MERGE

- **Eval 3 (Spec-Fidelity Chain) + Eval 10 (Cross-Gate Data Flow)** into a single eval: "Finding Lifecycle Chain." 5 scenarios, each tracing Finding objects through spec-fidelity, deviation, remediation, and certification stages. Asserts ID stability, severity preservation, status transitions, source_layer propagation, and routing correctness.

### REFACTOR

- **Eval 1 (Pipeline Smoke)**: Reduce to single run with static fixture files checked into tests/roadmap/fixtures/. Not generated content.
- **Eval 2 (Gate Rejection)**: Parameterize as 13 gates x N failure modes through gate_passed(). Must cover all 3 enforcement tiers. Estimated 40-60 parameterized cases.
- **Eval 4 (Wiring Fixtures)**: Replace "real codebases" with 3 minimal (5-8 file) fixture projects with planted issues. Test recall on planted issues and precision on known-clean items.
- **Eval 5 (Convergence)**: Narrow to 4 test cases covering multi-run regression detection sequence.
- **Eval 6 (Resume/State)**: Specify 3 corruption modes (truncated JSON, missing keys, dangling file refs) plus stale spec detection. 4 total scenarios.
- **Eval 8 (Performance)**: Designate as benchmark-only. Run outside normal CI. Use relative thresholds (no worse than 2x baseline) rather than absolute thresholds.

### DROP

- **Eval 7 (Sprint Wiring Hook Modes)**: Fully redundant with test_sprint_wiring.py (tests off/shadow/soft/full with SC-006).
- **Eval 9 (Agent Spec Completeness)**: Fully redundant with test_agent_regression.py (tests 5 agents for wiring keywords).

### ADD

- **NEW: Gate Ordering Invariants**: Verify (1) `_build_steps()` produces correct step ordering with correct input dependencies, (2) missing input file causes graceful gate failure not crash, (3) gate N's output is listed as gate N+1's input where applicable. Estimated 10-15 test cases.

### FINAL PRIORITIZED LIST

| Priority | Eval | Estimated Test Cases | Rationale |
|----------|------|---------------------|-----------|
| **P0** | Gate Rejection Fidelity (Eval 2) | 40-60 parameterized | Highest gap. No existing test exercises gate_passed() with failure inputs across all 13 gates. |
| **P0** | Finding Lifecycle Chain (Eval 3+10 merged) | 15-20 | Tests the most complex cross-subsystem interaction. No existing test traces a Finding through all stages. |
| **P1** | Wiring Multi-File Fixtures (Eval 4 refined) | 15-20 | All existing wiring tests use inline snippets. Cross-file patterns are untested. |
| **P1** | Convergence Multi-Run Regression (Eval 5 refined) | 4-6 | Multi-run sequence with registry persistence is untested. |
| **P1** | Gate Ordering Invariants (NEW) | 10-15 | Structural pipeline property with no existing coverage. |
| **P2** | Pipeline Smoke with Static Fixtures (Eval 1 refined) | 1-3 | Existing E2E is tautological but functional. Static fixtures add calibration confidence. |
| **P2** | Resume Under Corruption (Eval 6 refined) | 4-6 | Defensive edge cases. Existing resume tests cover primary paths. |
| **P2** | Performance Benchmark (Eval 8 refined) | 3-5 | Valuable but flaky in CI. Benchmark-only. |

**Total new test cases**: ~92-135 across 8 evals (down from 10 proposed, plus 1 new).

### UNRESOLVED DISAGREEMENTS

1. **Eval 1 priority**: Expert A argues P1 (gate calibration risk is real), Expert B argues P2 (existing E2E is sufficient for release). Resolution: classified P2 per majority weight, but should be promoted to P1 if any gate calibration bug is found during v3.0 development.

### IMPLEMENTATION NOTES

1. All fixture files should live under `tests/roadmap/fixtures/` or `tests/audit/fixtures/` as appropriate.
2. The Gate Rejection eval (P0) should be implemented first as it has the highest density of coverage per test case.
3. The Finding Lifecycle eval (P0) should reuse the existing `_make_config()` and mock runner patterns from test_integration_v5_pipeline.py.
4. The Gate Ordering eval (P1) can be implemented as a unit test against `_build_steps()` without mock runners.
5. Performance benchmarks (P2) should use `pytest-benchmark` or manual timing assertions with generous thresholds (2x baseline).
