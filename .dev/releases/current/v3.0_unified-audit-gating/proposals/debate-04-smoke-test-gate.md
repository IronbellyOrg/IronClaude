# Debate Transcript — Proposal 04: Smoke Test Gate at Release Tier

**Debate ID**: D-04
**Proposal under debate**: proposal-04-smoke-test-gate.md (Gate ID: G-012)
**Scoring framework**: scoring-framework.md
**Incident context**: cli-portify-executor-noop-forensic-report.md
**Date**: 2026-03-17
**Format**: 3-round adversarial debate + axis-by-axis scoring

---

## Participants

- **Proponent**: Argues for adoption of the smoke test gate as specified.
- **Devil's Advocate**: Argues against adoption or for fundamental redesign.

---

## Round 1 — Opening Positions

---

### Proponent — Opening Statement

The smoke test gate is the only proposal in this suite that answers the question the incident actually posed: *did the pipeline do real work?*

Every other gate in the existing infrastructure — and every other proposal in this backlog — evaluates documents. They ask: does this file exist? Does it have the right frontmatter? Does it reference the right identifiers? These are all reasonable questions when the pipeline produces documents as its primary artifact. But they are entirely orthogonal to the question that the cli-portify no-op exposed.

The forensic report is unambiguous on this point (§7, "The Systemic Blind Spot"): "Every gate follows the signature `(content: str) -> bool` or `(output_file: Path, criteria) -> tuple[bool, str|None]`. They validate that generated documents have correct structure. No gate anywhere asks: 'Does the code connect its components?'" The smoke test gate is the only proposal that breaks this constraint by running the thing and watching what happens.

Consider the three independent failure signals the smoke gate would have produced against the known no-op:

**Signal 1: Timing.** The no-op executor races through 12 steps in milliseconds. Wall-clock time: approximately 0.12 seconds. The smoke gate's no-op ceiling is 5 seconds. This check is deterministic. It requires no inference, no LLM judgment, no heuristic. If the process exits in under 5 seconds, it did not perform real work. This is a physical fact about the execution environment: config validation and filesystem I/O alone take longer than 1 second on any realistic hardware. An LLM step cannot complete in under 5 seconds. The ceiling is not a threshold to be tuned — it is a classification boundary grounded in the physics of API calls.

**Signal 2: Intermediate artifact absence.** A no-op writes exactly one file: `return-contract.yaml`. The smoke gate requires at least 2 intermediate artifacts beyond that file. A real run writes `discover-components.md`, `analyze-workflow.md`, and others. The presence or absence of these files is a binary fact. The no-op produces zero of them. This check would have fired independently of the timing check and independently of any content analysis.

**Signal 3: Content evidence.** Even if a future no-op variant somehow wrote fake intermediate files, the content evidence checks would catch it: the artifacts must contain proper nouns drawn from the fixture input (`InputValidator`, `DataProcessor`, `OutputFormatter`). These names appear in the fixture's `SKILL.md`. No generic template and no simple no-op can produce them without reading the fixture file.

All three signals fire simultaneously against the known bug. Any single one is sufficient to block the release.

The critical advantage of the smoke test gate over static analysis approaches (Proposal 03) is that it catches bugs that static analysis cannot see. Static analysis can verify that `step_runner` is typed as `Optional[Callable]` and warn that it defaults to `None`. But it cannot verify that a real LLM call returns substantive output, that filesystem discovery reads a real directory tree, or that artifact content is derived from real input rather than a template. A step that is correctly wired but calls the wrong function, or returns a plausible-looking but empty artifact, or silently substitutes a stub for a production implementation — these all pass static analysis and all fail the smoke test gate.

The smoke gate is also the only proposal that catches regressions. Once the bug is fixed, the gate protects against re-introduction. If a future refactor inadvertently re-introduces a no-op default — through a merge conflict, a refactored constructor, a misconfigured dependency injection — the smoke gate catches it at the next release. No other proposal provides this ongoing regression protection.

The implementation is well-scoped: approximately 3 days of work for `smoke_gate.py`, unit tests, fixture creation, and CI integration. This is commensurate with the severity of the bug class it prevents.

---

### Devil's Advocate — Opening Statement

The smoke test gate is the most operationally expensive proposal in this suite, and its apparent strength — "just run it and check" — conceals several deep problems that will make it unreliable in practice and difficult to maintain over time.

**Attack 1: The gate requires a working LLM API and is therefore inherently flaky in CI.**

The proposal acknowledges this in §8.2: "CI environments may lack Claude API access, have rate limits, or have different filesystem performance characteristics." The mitigation offered is a `transient` failure class and a `--mock-llm` flag. But consider what this means in practice. A CI pipeline that fails due to API rate limiting does not distinguish between "the gate found a bug" and "the API was temporarily unavailable." The operator must investigate. This is exactly the kind of friction that causes teams to start skipping gates.

The `--mock-llm` flag makes things worse, not better. If the smoke test runs in mock mode for most CI executions and real mode only for final release checks, then the gate provides no protection for the 90% of runs that use mock mode. And if real-mode runs are infrequent, the gate has little opportunity to catch regressions before release day.

**Attack 2: The smoke test is the most expensive gate in the system by an order of magnitude.**

The proposal estimates 30-300 seconds for a real run against the minimal fixture, with a maximum timeout of 600 seconds. Every other gate in the existing system runs in milliseconds (document content checks) or seconds (LLM fidelity reports). A 2-5 minute blocking gate at the release tier adds meaningful latency to every release workflow. The proposal argues this is acceptable because releases are infrequent. But as the system matures and release cadence increases, this becomes a tax on every release — and one that cannot be parallelized (the gate must run serially, because it uses a subprocess).

**Attack 3: The gate validates end-to-end behavior but cannot localize the failure.**

When the smoke gate fails, the developer knows that "the pipeline did not produce real artifacts." They do not know which step failed, why it failed, or where to look. The gate failure report (Appendix A) points to `run_portify()` missing `step_runner`, but this diagnosis is hardcoded — it assumes the bug is always the same one. A future regression might be a different wiring failure: a correctly-provided `step_runner` that routes to a stub implementation, a step that silently short-circuits due to a configuration condition, a step that produces output but from a cached result rather than real execution. The smoke gate's diagnostic output will say "timing check failed" or "content evidence absent" without pointing to the specific code path that failed. This makes the gate a fire alarm without a sprinkler system.

**Attack 4: The gate is inherently reactive, not preventive.**

This is the most fundamental objection. The smoke test gate catches the bug only after the fix has been attempted. Its mechanism is: "run the pipeline; if it behaves correctly, the release may proceed." This means the gate cannot be deployed until Fix 1 (wire `run_portify()` to step dispatch) and Fix 2 (add validation call) are complete. The proposal states this explicitly in §8.5: "The smoke gate is a release gate, not a bug fix. It must not be deployed as a substitute for Fix 1 and Fix 2."

What would the smoke gate do in a world where Fix 1 is never applied? It would permanently block every release. The gate does not tell you *what* to fix, only that *something* is wrong. The developer who encounters a failing smoke gate for the first time — without the forensic report as context — must debug a subprocess invocation to understand what the gate is checking. This is a poor developer experience and increases the probability that the gate gets disabled rather than investigated.

**Attack 5: LLM non-determinism makes "content evidence anchors" fragile.**

The proposal argues (§8.1) that content evidence checks match against fixture-specific component names (`InputValidator`, `DataProcessor`, `OutputFormatter`), which a real LLM analysis will always reference. But LLM behavior is not deterministic. A real analysis might summarize the components under different terminology, paraphrase the component names in a discussion, or produce an analysis so high-level that individual component names do not appear. The proposal's mitigation — "these names will appear in any genuine analysis" — is an assumption, not a verified property. If the LLM changes its output format, or if a model update produces more abstract summaries, the content evidence check becomes a false positive factory: legitimate real runs fail the gate, while a no-op (which the gate is designed to catch) was already caught by the timing and artifact-absence checks.

In summary: the smoke gate is expensive, flaky in CI, cannot localize failures, is reactive rather than preventive, and has at least one fragile check. The value it adds — catching the specific timing and artifact-absence signals — can be partially replicated by cheaper static analysis (Proposal 03) that detects the structural condition that enables the no-op rather than relying on observing the no-op's effects.

---

## Round 2 — Cross-Examination

---

### Proponent addresses "requires bug fix first" — can smoke tests catch bugs proactively, or are they inherently reactive?

The Devil's Advocate frames the gate's dependency on Fix 1 as a fundamental limitation: the gate "catches bugs only after the fix has been attempted." This mischaracterizes how the gate operates in the lifecycle of a system.

The smoke gate is not designed to catch a bug during the session in which the bug is being fixed. No regression test is. A regression test's value is in the releases that follow — in the months and years of continued development where the same bug class can re-emerge from a different cause. The forensic report documents that the no-op pattern has already appeared in three independent subsystems: `PortifyExecutor._execute_step()`, `DEVIATION_ANALYSIS_GATE` (defined but not wired into `_build_steps()`), and `TrailingGateRunner` (defined but never called from `execute_sprint()`). The common thread is not a single bug — it is a recurring pattern: "defined but not wired." This pattern will recur.

When it recurs, the smoke gate is proactive. If a future refactor of `run_portify()` drops `step_runner` from the constructor call — perhaps in a merge conflict, perhaps during a dependency injection refactor, perhaps when a developer adds a new optional parameter and resets the constructor to defaults — the smoke gate fires at the next release. No static analysis catches this class of regression reliably, because the code is structurally valid: `step_runner=None` is a legal constructor call, and the parameter is typed as `Optional[Callable]`. The no-op is not a syntax error. Static analysis can only catch it if it explicitly searches for `Optional[Callable]` parameters with no-op defaults and verifies they are provided in all production call sites — a heuristic that will generate substantial false positives across the codebase.

The smoke gate's proactive value also extends to bugs that static analysis cannot represent. Consider: Fix 1 wires `run_portify()` to the step dispatch map. A year later, a developer refactors the step dispatch map and introduces a new step without adding it to the dispatch. The step exists, is listed in `STEP_REGISTRY`, but the dispatch map entry is missing. Static analysis may or may not catch this depending on the analysis tool's understanding of dictionary key coverage. The smoke gate catches it definitively: the missing step either times out or produces no output, and the artifact-absence check fires.

The correct framing is not "reactive versus preventive" but "when in the development cycle does the gate fire." The smoke gate fires at release tier — after implementation, before shipping. This is exactly where a regression guard should fire. Preventive gates (static analysis, constructor audits) fire earlier and are complementary, not substitutes. The proposal correctly positions the smoke gate as release-tier protection, not development-time feedback.

The Devil's Advocate's implicit argument — that a gate which cannot run before the fix is not worth having — would also invalidate every integration test in every system. Integration tests require a working implementation before they pass. They are not therefore useless.

---

### Devil's Advocate attacks the timing check — what if a real run is also fast? What if infrastructure makes legitimate runs slow?

The Proponent has characterized the timing check as a "classification boundary grounded in the physics of API calls." This framing deserves scrutiny, because the physics are less deterministic than the Proponent claims.

**The fast-real-run scenario.** The smoke gate's no-op ceiling is 5 seconds. The proposal argues this is safe because "even the fastest programmatic step (validate-config) reads and parses YAML from disk." But consider a scenario where the fixture validation succeeds instantly (the fixture is cached, the YAML is small, the filesystem is fast) and the step dispatch is wired to a stub that returns in under 1 second per step. In CI, it is common to use mocked LLM responses or cached API responses for speed. If the CI configuration for the smoke gate uses such a cache, a complete pipeline run could complete in under 5 seconds — passing every step, producing real artifacts from cached responses, and triggering the timing check false positive.

The proposal's response to this is the `--mock-llm` flag, but that flag is proposed as a way to bypass the LLM calls entirely for non-release CI runs. If the flag bypasses the LLM, it also bypasses the only thing that forces real-run latency. The timing check and the mock-mode flag are in direct tension: you cannot have a fast CI mode and a meaningful timing threshold simultaneously.

**The slow-CI scenario.** Now consider the opposite: a legitimate real run that takes under 5 seconds because the API responds unusually fast (a local LLM, a cached response, a lightweight test model), or unusually slow because a CI machine is overloaded and the timing ceiling is exceeded not by execution but by scheduler latency. The proposal acknowledges the overloaded-machine scenario and dismisses it: "If a CI machine is so slow that a no-op takes 5 seconds, all other timeouts will be proportionally exceeded and the run will fail anyway." But "fail anyway" is not the same as "fail with the right diagnosis." An overloaded CI machine where the no-op takes 7 seconds and then the first real step times out at 120 seconds will produce a timeout failure, not a no-op detection. The gate's diagnostic output points developers in the wrong direction.

**The more fundamental problem.** The timing check is not a property of correctness — it is a property of performance. A correctly-wired pipeline that happens to be fast looks like a no-op to the timing check. A no-op pipeline running on a slow machine looks like a real run to the timing check. The check is calibrated to the current implementation's performance characteristics. As the implementation evolves — faster models, more efficient step implementations, cached intermediate results — the 5-second ceiling will require tuning. And every time it is tuned, there is a window where the gate is either too permissive (no-ops pass) or too restrictive (real runs fail).

The artifact-absence check is more robust than the timing check precisely because it does not depend on time. The proposal should position artifact presence as the primary check and timing as a secondary diagnostic hint, rather than making the timing check "the fastest-failing check" that "runs first." A timing check that fails fast is only valuable if it fails accurately — and the timing check's accuracy degrades as the implementation evolves.

---

## Round 3 — Synthesis

---

### Is this a preventive gate or a regression guard? Can it be both?

The debate has clarified a genuine tension in the proposal's positioning. The Devil's Advocate is correct that the gate is fundamentally reactive: it cannot run against the no-op implementation and report "this will fail" before the no-op is fixed. But the Proponent is correct that "reactive at release tier" is the appropriate and valuable position for a regression guard in a production system.

The resolution is that the smoke test gate is simultaneously:

1. **A regression guard** — its primary value. Once Fix 1 is applied, the gate permanently protects against re-introduction of the no-op pattern. Any future change that removes or bypasses the step dispatch mechanism will be caught before the next release. This is high value in a codebase where the forensic report has already identified three independent instances of "defined but not wired."

2. **A preventive gate for new pipelines** — secondary value. When a new CLI pipeline is introduced (analogous to cli-portify), the smoke gate framework provides a template for immediately adding release-tier execution validation. The gate's existence as an institutionalized release check makes it harder to ship a new pipeline without demonstrating that it does real work.

3. **Not a development-time detector** — acknowledged limitation. The gate does not fire during development when the no-op is introduced. It fires at release. This means the no-op can exist undetected for multiple development cycles if no release is attempted. In the incident, the no-op existed across three releases because each release's gate system validated documents, not execution. With the smoke gate in place, the no-op would have been caught at the first release attempt after its introduction — not earlier.

The Devil's Advocate's timing-check critique points to a real design issue. The synthesis position: the artifact-absence check is the gate's primary mechanism; the timing check is a fast-fail shortcut that should be treated as a hint rather than a definitive classification. The implementation should weight its failure modes accordingly:

- Timing check failure: `WARN` level diagnosis, not `BLOCKING` on its own. Alert the operator but proceed to artifact checks. A timing check failure with artifact checks passing is a surprising state that warrants investigation, not automatic release block.
- Artifact absence: `BLOCKING`. This is deterministic and cannot produce false positives in a correctly-wired system.
- Content evidence failure: `BLOCKING`. If artifacts exist but contain no fixture-specific content, the gate correctly identifies a templated or stub run.

This reweighting addresses the Devil's Advocate's fast-CI concern without weakening the gate's primary detection mechanism. A fast-but-real run that produces correct artifacts passes the gate; a no-op that produces no artifacts fails regardless of timing.

---

### At what point in the pipeline should the smoke gate run — pre-release vs. post-implementation?

The proposal places the smoke gate at "release tier" — specifically in the `audit_release_running` state, before `audit_release_passed`. This is the correct position for the following reasons:

**Why not post-implementation (task tier)?** A post-implementation smoke test requires that Fix 1 is fully complete before the test can be written — a test that fires against a no-op executor will always fail, and the developer implementing Fix 1 needs to complete their work before the smoke test becomes a useful feedback mechanism rather than a constant blocking condition. Additionally, running the full CLI pipeline as a task-level check is expensive (2-5 minutes per run) and would be triggered far too frequently during development.

**Why not pre-release (sprint tier)?** A pre-release smoke test runs before the sprint executor marks the task complete. This is closer to a useful position — it would catch the no-op before marking the release task complete — but it creates a dependency: the sprint executor needs access to the CLI invocation infrastructure, which adds coupling and complexity that the proposal's release-tier integration avoids.

**Why release tier is correct.** The release tier represents a natural checkpoint: work is done, artifacts are assembled, and the system is being evaluated for shipping. This is precisely when a "does it actually run?" check belongs. The gate runs once per release, not per task or per commit. Its cost (2-5 minutes) is amortized over the full release cycle. Its blocking semantics are appropriately strict: at release tier, a gate failure means the release does not ship until the problem is resolved.

The proposal's integration point (§6.3, Appendix B) correctly identifies the `ready_for_audit_release → released` transition as the gating point. The smoke gate must pass before this transition. This aligns with the unified-audit-gating v1.2.1 state machine and does not require changes to the existing `GateScope.RELEASE` enforcement path.

One addition the debate reveals as valuable: a **standalone CLI command** (`superclaude cli-portify smoke-test`) that developers can run during implementation. This is already in the proposal (§6.3, Point 2) and deserves emphasis. The standalone command turns the gate into a development tool, not just a release check. Developers fixing the executor can run `smoke-test` after each iteration to verify their fix is complete before triggering the full release audit. This partially addresses the "reactive" objection: while the gate is release-tier blocking, the standalone command enables developers to use it as a proactive verification tool during implementation.

---

## Scoring — Axis-by-Axis Evaluation

---

### Axis 1 — Catch Rate (weight 25%)

**Score: 10**

**Evidence**: The forensic report establishes three independent observable signals that the smoke gate checks:

1. *Timing*: The no-op completes in ~0.12 seconds. The smoke gate's ceiling is 5 seconds. This check is deterministic: `elapsed_s < SMOKE_NOOP_CEILING_S` → FAIL (proposal §5.3). The no-op cannot take 5 seconds on any realistic hardware unless the machine is severely overloaded, in which case other timeouts would also be exceeded.

2. *Artifact absence*: The no-op produces exactly one file (`return-contract.yaml`). The smoke gate requires at least 2 intermediate artifacts beyond this file (§4.1). The no-op produces zero such artifacts. This check fires independently of timing and would block the release alone.

3. *Content evidence*: Even if a future no-op wrote fake artifacts, the content evidence check requires fixture-specific component names (`InputValidator`, `DataProcessor`, `OutputFormatter`) that a generic template cannot contain (§4.3).

All three checks would have fired simultaneously against the known no-op. The proposal includes a formal acceptance criterion (AC-001) specifically covering the `step_runner=None` case. Catch rate is definitively 10: the gate would have blocked the pipeline deterministically before any release.

**Strongest counter-argument**: The gate requires Fix 1 to be applied before it can demonstrate a passing run; without Fix 1, the gate catches the bug only by failing. The Devil's Advocate argues this is reactive. The response: a catch rate score of 10 requires deterministic detection, and the gate produces exactly that — a deterministic FAIL against the no-op condition. Whether that FAIL prompts remediation (which it does) or whether it could have been caught earlier (yes, but that is a different gate's job) does not affect catch rate.

---

### Axis 2 — Generalizability (weight 25%)

**Score: 7**

**Evidence**: The smoke gate catches the "defined but not wired" bug class wherever a CLI pipeline can be run against a test fixture. The forensic report identifies three additional instances of this pattern:

- `DEVIATION_ANALYSIS_GATE` defined in `roadmap/gates.py:712-758` but not wired into `_build_steps()` — not catchable by the cli-portify smoke gate (wrong pipeline), but the smoke gate *framework* provides the template for a roadmap-pipeline smoke test that would catch this
- `SprintGatePolicy` stub in `sprint/executor.py:47-90` — a sprint-pipeline smoke test using the same framework would catch unwired policy execution
- `TrailingGateRunner` never called from `execute_sprint()` — same as above

The smoke gate framework (fixture + timing check + artifact-absence check + content evidence) is directly applicable to any CLI pipeline in the codebase. Each pipeline needs its own fixture, but the gate architecture transfers completely.

The gate also catches a broader class than just no-ops: it catches any execution path that produces plausible-looking but empty results — a correctly-wired step that calls the wrong function and returns templated output, a step that silently short-circuits based on a configuration flag, a step that produces output from a cache rather than real execution. These are bugs that no static analysis proposal can detect.

Score is 7 rather than 8-9 because the gate does not directly address the other "defined but not wired" instances — it catches the cli-portify case definitively and provides a framework for catching others, but each additional pipeline requires its own smoke fixture and integration work. The generalization is an architectural pattern, not an automatic coverage extension.

---

### Axis 3 — Implementation Complexity (weight 20%, inverted)

**Score: 5**

**Evidence**: The proposal's implementation plan (§6) requires:

- 3 new files: `smoke_gate.py`, `test_smoke_gate.py`, fixture files (`SKILL.md`, `minimal-protocol.md`, `README.md`)
- 2 modified files: `gates.py` (add `SMOKE_TEST_GATE` to registry), `commands.py` (add smoke gate invocation to release path)
- Estimated effort: ~3 days

This falls in the 7-10 file / 3-5 new abstraction range on the scoring rubric. New abstractions introduced: `SmokeTestConfig`, `SmokeTestResult`, `run_smoke_test()`, the CI configuration for API key handling, and the `--mock-llm` flag mode.

The implementation also requires CI configuration work (§8.2) — an orthogonal concern that adds operational complexity beyond the code changes. Running a gate that requires a live Claude API in CI is a genuinely different class of operational requirement from gates that run deterministic document checks.

The Devil's Advocate correctly identifies the CI API dependency as a complexity amplifier: the gate requires managing API credentials, handling rate limits, implementing retry logic for `transient` failures, and deciding how mock mode interacts with release-tier gate enforcement. This is not counted in the 3-day estimate.

Score is 5 rather than 4 because the proposal is well-scoped and the implementation plan is specific. The abstractions are clean and the failure cases are well-defined. But the real complexity is operational, not just code volume.

---

### Axis 4 — False Positive Risk (weight 15%, inverted)

**Score: 6**

**Evidence**: The proposal identifies two legitimate false positive scenarios:

1. **Environment-dependent failures** (§8.2): Claude API unavailability, rate limiting, CI network restrictions. The `transient` failure class mitigates this but does not eliminate it. A CI runner that can never reach the Claude API will produce a permanent transient failure that blocks releases until configuration is resolved.

2. **Fixture drift** (§8.3): If the fixture's component names are changed without updating the content evidence checks in `smoke_gate.py`, real runs will fail the content evidence check. The proposal mitigates this with a `test_fixture_content_matches_gate_patterns` unit test, but this test must be maintained and the co-location comment must be respected.

3. **Timing check boundary** (identified in debate, Round 2): A real run that completes faster than 5 seconds due to cached API responses, a local LLM, or an unusually fast execution environment will fail the timing check despite being a genuine real run. The synthesis in Round 3 recommends demoting the timing check from `BLOCKING` to `WARN` to address this.

The `--skip-review` flag (§5.1) and `--mock-llm` mode create configuration surfaces where a legitimate real run might not match the gate's expectations, depending on which flags are active.

Score is 6 rather than 4-5 because most of the false positive scenarios are escapable: the `transient` class allows retry, the fixture unit test catches drift, and the timing threshold is configurable. But the CI API dependency creates a class of environment-dependent false positives that cannot be escaped without changing the gate's execution model — a real operational risk for organizations with strict CI network policies.

---

### Axis 5 — Integration Fit (weight 15%)

**Score: 6**

**Evidence**: The proposal's integration analysis (§6.4) correctly identifies that the smoke gate does *not* extend the existing `gate_passed()` + `GateCriteria` pattern, because it must first produce artifacts by running the CLI before validating them. This means the smoke gate is a new architectural pattern in the gate infrastructure, not an extension of an existing one.

The gate correctly uses `GateScope.RELEASE` and `GateMode.BLOCKING` (§2.2) — these are existing infrastructure concepts. The `GateFailure` dataclass (§6.4) reuses the existing failure reporting structure. The gate ID `G-012` continues the existing sequence.

However, the gate does not plug into `TrailingGateRunner` or the `ALL_GATES` registry in the same way as other gates. It requires a custom invocation path in `commands.py` (§6.2), which is a new hook point. The proposal notes: "The smoke gate does not use `TrailingGateRunner`. Trailing gates are designed for post-step artifact checks that can run asynchronously. The smoke gate is a pre-release blocking check that requires serial execution."

The integration footprint is: existing concepts (`GateScope.RELEASE`, `GateFailure`, gate IDs), new invocation path (custom in `commands.py`), no modification to `TrailingGateRunner` or `trailing_gate.py`. This is adjacent to the existing infrastructure rather than a clean extension of it.

Score is 6: the gate reuses existing abstractions where it can and introduces a new invocation model where necessary. It does not conflict with existing gates and does not require architectural restructuring, but it is not as cleanly integrated as a gate that simply extends `GateCriteria`.

---

## Composite Score

```
Composite = (Catch_Rate × 0.25)
          + (Generalizability × 0.25)
          + (Complexity × 0.20)
          + (FP_Risk × 0.15)
          + (Integration_Fit × 0.15)

         = (10 × 0.25)
         + (7 × 0.25)
         + (5 × 0.20)
         + (6 × 0.15)
         + (6 × 0.15)

         = 2.50 + 1.75 + 1.00 + 0.90 + 0.90

         = 7.05
```

---

## Scoring Table

| Axis | Weight | Score | Weighted | Evidence Summary |
|------|--------|-------|----------|-----------------|
| Catch Rate | 25% | 10 | 2.50 | All 3 independent checks fire deterministically against the no-op: timing (0.12s < 5s ceiling), artifact absence (0 intermediate files), content evidence (no fixture-specific names) |
| Generalizability | 25% | 7 | 1.75 | Catches "defined but not wired" class across all CLI pipelines; framework transfers but each pipeline needs its own fixture; does not auto-extend to roadmap/sprint unwired gates |
| Implementation Complexity (inverted) | 20% | 5 | 1.00 | 5+ files, new abstraction layer (`SmokeTestConfig`, `SmokeTestResult`), CI API credential management, mock-mode flag — commensurate with a new subsystem at the release tier |
| False Positive Risk (inverted) | 15% | 6 | 0.90 | Mitigatable FP scenarios (fixture drift, timing boundary); one structural FP class (CI API unavailability) that `transient` class cannot fully resolve for all environments |
| Integration Fit | 15% | 6 | 0.90 | Reuses `GateScope.RELEASE`, `GateFailure`, gate ID sequence; requires new invocation path in `commands.py`; does not extend `TrailingGateRunner` |
| **Composite** | **100%** | — | **7.05** | **Tier 2 — Implement in Phase 2** |

---

## Final Verdict

**Composite Score: 7.05**
**Tier: Tier 2 — Implement in Phase 2** (range: 6.0–7.4)

---

### Adoption Profile

**Adopt, with the following conditions:**

1. **Prerequisites are non-negotiable.** Fix 1 (wire `run_portify()` to step dispatch) and Fix 2 (add `validate_portify_config()` call) must be complete before the smoke gate is deployed in production. The gate provides regression protection; it is not a bug fix. Deploying the gate before Fix 1 creates a permanently-blocking release gate with no actionable path forward.

2. **Demote the timing check from primary to advisory.** As established in Round 3 synthesis: the artifact-absence check is the gate's primary mechanism. The timing check should report at `WARN` level and not independently block the release. If artifacts are present and content-validated, a sub-5-second execution is unusual and worth logging but should not block a release. This change reduces false positive risk on Axis 4 by eliminating the fast-CI timing boundary scenario.

3. **Invest in the `--mock-llm` flag before CI integration.** The CI API dependency is the gate's primary operational risk. A `--mock-llm` mode that validates all non-LLM checks (artifact presence, content structure, timing heuristics against mock responses) allows the gate to run in restricted CI environments without API access. Real-mode gate execution is then reserved for the final release audit. This is more operationally sound than relying on `transient` failure classification to manage API unavailability.

4. **Ship with the `test_fixture_content_matches_gate_patterns` unit test from day one.** Fixture drift is a real and predictable maintenance hazard. The unit test that validates co-location of fixture component names and gate patterns must not be deferred to a follow-up task.

5. **Write the regression test for the known-bad case (AC-007 note).** The proposal specifies a regression check that runs the gate against the known no-op executor and verifies non-zero exit code. This test documents exactly why the gate exists and what it catches. It must be a permanently-preserved test case, not a one-time validation.

**Phase 2 position over Phase 1**: The gate scores 7.05 rather than 7.5+ primarily due to implementation complexity (5/10) and false positive risk (6/10). These are real costs. Phase 1 should focus on the lower-complexity, higher-catch-rate proposals (static wiring verification, Proposal 03) that can be deployed without CI API integration overhead. The smoke gate is the right follow-on: once static analysis is in place to catch structural no-op conditions at commit time, the smoke gate provides the execution-layer validation that static analysis cannot offer.

---

## Top 2 Failure Conditions

### Failure Condition 1: CI API Dependency Creates Permanent Transient Failures

**Scenario**: The CI environment for the release pipeline runs in a network-restricted zone (common in enterprise CI, air-gapped environments, or CI providers with no outbound API access). The smoke gate's real-mode execution requires a live Claude API call. Every release smoke gate invocation returns `failure_class="transient"` due to network unavailability. The gate cannot be bypassed (it is `GateScope.RELEASE`, always `GateMode.BLOCKING`). Releases are permanently blocked.

**Why this is a top failure condition**: The proposal's mitigation (`--mock-llm` flag) requires the flag to be developed before CI integration. If the CI integration is shipped before `--mock-llm` is ready — a likely ordering error in practice — the gate permanently blocks releases in any CI environment without API access. This is not a hypothetical: CI environments without outbound LLM API access are common and the issue would appear immediately on first deployment.

**Leading indicator**: The first time `make release` is run in a fresh CI environment, the smoke gate fails with `failure_class="transient"` and the release workflow stalls. The diagnostic is confusing because it looks like an infrastructure problem, not a gate configuration problem.

**Mitigation**: Ship `--mock-llm` mode before enabling the gate in CI. Treat CI integration as a separate phase from gate implementation.

---

### Failure Condition 2: Fixture Drift Causes Legitimate Real Runs to Fail Content Evidence Checks

**Scenario**: Six months after deployment, a developer updates the smoke fixture's `SKILL.md` to add a new component (`DataValidator`) and rename an existing one (`InputValidator` → `ParameterValidator`). The commit message does not mention the smoke gate. The co-location comment in `smoke_gate.py` is present but not read. The `test_fixture_content_matches_gate_patterns` unit test — if it was not shipped with the gate — does not exist. The gate's content evidence check still looks for `InputValidator`. Every real run against the updated fixture fails the content evidence check with `SMOKE_TEST_GATE FAILED: content-evidence-absent`. The developer investigating the failure must trace from the gate failure back through `smoke_gate.py` to the hardcoded component name list to understand why a clearly-real run is being classified as a no-op.

**Why this is a top failure condition**: This failure is entirely silent in its setup phase and entirely confusing in its failure phase. The fixture modification is innocuous (updating a test fixture's SKILL.md is routine maintenance). The gate failure looks like an executor bug, not a fixture/gate mismatch. The developer's first instinct is "the executor is broken again," not "the fixture component names changed." This leads to wasted investigation effort and — if the pattern repeats — erodes trust in the gate until it is disabled.

**Leading indicator**: Gate failures that occur after fixture-related commits, with all other pipeline checks passing, on machines where the API is accessible and the executor is known to be correctly wired.

**Mitigation**: The `test_fixture_content_matches_gate_patterns` unit test is the single most important prevention mechanism. It must be shipped with the gate and must fail loudly if fixture component names diverge from gate patterns. This test converts a confusing runtime failure into an immediate, clearly-labeled unit test failure at the point where the fixture is modified.
