---
stage: 9
stage_name: spec-fidelity + deviation-analysis
depth: standard
gate: SPEC_FIDELITY_GATE + DEVIATION_ANALYSIS_GATE
verdict: NEEDS-REVISION
---

# Stage 9: spec-fidelity + deviation-analysis -- Adversarial Review

## Q1: Meaningful Output

The eval spec (FR-EVAL-001) is a MEDIUM complexity new feature with 6 functional requirements, which provides substantive surface area for spec-fidelity checking. This is not a trivially passing scenario. Specifically:

**Non-trivial pass conditions**: The SPEC_FIDELITY_GATE requires `high_severity_count: 0` via the `_high_severity_count_zero` semantic check. Given the two seeded ambiguities (FR-EVAL-001.4 missing schema, FR-EVAL-001.5 terminology mismatch), the fidelity checker SHOULD detect at least one HIGH severity deviation (the missing deviation sub-entry schema is a structural gap that blocks implementation). This means the gate should legitimately FAIL on first pass, requiring remediation before it can pass -- exactly the behavior v3.0 intends to validate.

**DEVIATION_ANALYSIS_GATE has 6 semantic checks** (no_ambiguous_deviations, validation_complete_true, routing_ids_valid, slip_count_matches_routing, pre_approved_not_in_fix_roadmap, total_analyzed_consistent). These cross-validate frontmatter arithmetic, so an LLM-generated artifact with inconsistent counts will be caught. This is genuinely useful validation -- not a rubber stamp.

**Risk of trivial failure**: If the LLM fidelity checker fails to produce valid YAML frontmatter at all (missing `---` delimiters, wrong field names), the gate fails on structural grounds before reaching semantic checks. This would be a "trivial failure" that masks whether the eval spec's seeded ambiguities were actually detected. The eval must verify failure REASON, not just failure status.

**Assessment**: Output will be meaningful IF the eval harness inspects the body of the fidelity report for specific findings, not just the gate pass/fail bit.

## Q2: v3.0 Changes

v3.0 introduces three major changes to this stage compared to master:

### 2a. Convergence-controlled gate bypass
In `executor.py` line 521, when `config.convergence_enabled` is True, the spec-fidelity step's gate is set to `None`:
```python
gate=None if config.convergence_enabled else SPEC_FIDELITY_GATE,
```
This means the standalone SPEC_FIDELITY_GATE is NOT evaluated when convergence is active. Instead, the convergence engine (`convergence.py`) manages the pass/fail logic through its `ConvergenceResult` with `passed`, `final_high_count`, and `regression_detected` fields. This is a fundamental architectural change: the gate shifts from a single-shot frontmatter check to an iterative convergence loop.

### 2b. DeviationRegistry with stable finding IDs
The `DeviationRegistry` class provides persistent, file-backed finding tracking across runs using deterministic SHA-256 IDs computed from `(dimension, rule_id, spec_location, mismatch_type)`. This enables:
- Run-to-run memory (FR-10): findings persist across convergence iterations
- Automatic FIXED detection: findings absent in a new run are marked FIXED
- Debate verdict recording: findings can be downgraded via adversarial debate

Master has no equivalent -- findings were ephemeral per-run.

### 2c. Structural vs. semantic HIGH separation (BF-3)
`_check_regression()` only triggers on structural HIGH increases, not semantic fluctuations. The `DeviationRegistry.merge_findings()` tracks `source_layer` ("structural" vs "semantic") separately. This means the convergence loop can tolerate semantic HIGH count fluctuation (logged as warnings) while enforcing monotonic decrease of structural HIGHs.

### 2d. Deviation-analysis as logical phase within convergence
The `DEVIATION_ANALYSIS_GATE` exists in `ALL_GATES` but deviation-analysis runs WITHIN the convergence loop as a logical phase, not as a standalone pipeline step. The freshness check in `_check_annotate_deviations_freshness()` resets both `spec-fidelity` and `deviation-analysis` gate state on roadmap hash mismatch (line 778).

## Q3: Artifact Verification

### Artifacts produced

1. **spec-fidelity.md** -- Fidelity report with YAML frontmatter containing severity counts, total_deviations, validation_complete, tasklist_ready. Body contains per-finding details with dimension, severity, description, location, evidence, fix_guidance.

2. **deviation-analysis output** (within convergence) -- Analysis with frontmatter: schema_version, total_analyzed, slip_count, intentional_count, pre_approved_count, ambiguous_count, routing fields, analysis_complete.

3. **deviation-registry.json** (when convergence enabled) -- Persistent JSON with schema_version, release_id, spec_hash, runs array, findings dict keyed by stable_id.

### Third-party verification methods

- **Frontmatter arithmetic**: A third party can parse the YAML frontmatter and verify `total_deviations == high_severity_count + medium_severity_count + low_severity_count` (SPEC_FIDELITY_GATE doesn't enforce this sum, which is a gap -- see Q4).
- **Routing consistency**: `total_analyzed == slip_count + intentional_count + pre_approved_count + ambiguous_count` is enforced by `_total_analyzed_consistent`.
- **Cross-reference to spec**: Each finding's `location` field should reference a real section in the eval spec. A verifier can grep the spec for the referenced section headings.
- **Registry integrity**: The `deviation-registry.json` can be independently validated: stable IDs should be reproducible from the finding's structural properties via SHA-256.
- **Regression monotonicity**: Across convergence runs, structural HIGH counts in the `runs` array should be non-increasing.

### Verification gap

There is no gate check that validates the BODY of spec-fidelity.md against the frontmatter counts. An LLM could emit `high_severity_count: 0` in frontmatter while listing HIGH findings in the body. The semantic checks only validate frontmatter-to-frontmatter consistency, not frontmatter-to-body consistency.

## Q4: Most Likely Failure Mode

**The single most likely failure mode is: the convergence gate bypass (`gate=None`) creating an untested code path when convergence is disabled.**

When `convergence_enabled=False` (the default), the SPEC_FIDELITY_GATE runs as a standard single-shot gate. When `convergence_enabled=True`, it is bypassed entirely (`gate=None`). The eval spec must exercise BOTH paths, but there is no indication it tests the convergence-enabled path where:

1. The spec-fidelity step runs without a gate
2. The convergence engine calls `merge_findings()` iteratively
3. Regression detection via `_check_regression()` enforces structural monotonicity
4. The `ConvergenceResult.passed` field becomes the actual pass/fail signal

**Why this is the most likely failure**: The eval spec describes "Pipeline Progress Reporting" with a progress.json writer. If progress.json tracks gate results, and the spec-fidelity gate is `None` under convergence, the progress reporter might record `null` for the gate result, corrupting downstream consumers. The eval spec does not specify what progress.json should contain when a gate is intentionally absent.

**Secondary failure mode**: The DEVIATION_ANALYSIS_GATE requires `ambiguous_count: 0` (via `_no_ambiguous_deviations`). The seeded ambiguity FR-EVAL-001.4 (missing schema) could legitimately be classified as AMBIGUOUS rather than HIGH, which would cause the deviation-analysis gate to fail with "ambiguous items require human review." This is correct behavior but the eval spec may not account for it.

## Q5: Eval Spec Coverage

### What v3.0 requires the eval spec to exercise

1. **Convergence loop iteration**: Multiple fidelity runs with finding merge, regression detection, and convergence scoring. The eval spec must trigger at least 2 runs to test run-to-run memory.
2. **Structural vs. semantic HIGH separation**: The eval spec must produce findings of both types and verify that only structural HIGHs trigger regression.
3. **Stable ID determinism**: Same finding across runs must produce the same stable_id (SHA-256 of structural properties).
4. **Gate bypass under convergence**: When convergence_enabled=True, the spec-fidelity step's gate is None. Progress reporting must handle this.
5. **Deviation routing**: Findings must flow through slip/intentional/pre_approved/ambiguous classification and into routing_fix_roadmap vs routing_no_action.
6. **Freshness checking**: The `_check_annotate_deviations_freshness()` function resets gate state on roadmap hash change. The eval spec should test stale-deviation detection.

### Does the eval spec account for this?

**Partially, with critical gaps**:

- **FR-EVAL-001.4 (missing deviation sub-entry schema)**: This tests whether the fidelity checker flags an underspecified schema. It SHOULD produce a finding, but the eval spec does not specify the expected schema for how convergence iteration deviations nest in progress.json. This is the seeded ambiguity working as designed -- the spec-fidelity checker should flag it as a BLOCKING deviation.

- **FR-EVAL-001.5 ("significant findings" vs "HIGH severity findings")**: This terminology mismatch should be detected by the fidelity checker as a semantic deviation. However, the SPEC_FIDELITY_GATE only checks frontmatter counts, not whether the body correctly identifies this as a finding. The gate will pass or fail based on the LLM's severity classification of this finding, not on whether it was detected at all.

- **Convergence path not exercised**: The eval spec describes a single-pass pipeline progress reporter. It does not describe multi-iteration convergence behavior. This means the convergence-enabled code path (`gate=None`, `DeviationRegistry`, `ConvergenceResult`) is NOT tested by this eval spec.

- **DEVIATION_ANALYSIS_GATE routing checks**: The eval spec does not describe how deviations are routed (fix_roadmap vs no_action). The 6 semantic checks on DEVIATION_ANALYSIS_GATE (routing_ids_valid, slip_count_matches_routing, etc.) require specific frontmatter fields that the eval spec does not mandate in its progress.json schema.

## Seeded Ambiguity Analysis

### FR-EVAL-001.4: Missing deviation sub-entry schema

**Expected behavior**: The spec-fidelity checker should flag this as a HIGH severity structural deviation. The convergence loop produces 1-N deviation analysis iterations, but no format is specified for how these nest in progress.json. This is a genuine spec gap that prevents implementation.

**Will the gate catch it?**: If the LLM fidelity checker correctly identifies this as HIGH, then `high_severity_count > 0`, and `_high_severity_count_zero` returns False, causing SPEC_FIDELITY_GATE to fail. This is the correct outcome -- the gate SHOULD block.

**Risk**: If the LLM classifies this as MEDIUM instead of HIGH, the gate may pass (high_severity_count=0) while a genuine blocking issue goes unaddressed. The gate has no mechanism to validate that a truly blocking gap was correctly classified as HIGH.

**Under convergence**: If convergence_enabled=True, the gate is bypassed (None), and the convergence engine tracks this finding via `DeviationRegistry`. The finding would need to be resolved across iterations. However, the eval spec doesn't exercise the convergence path, so this behavior is untested.

**Assessment**: PARTIAL DETECTION. The seeded ambiguity will be caught IF the LLM classifies it as HIGH AND convergence is disabled. Under convergence-enabled mode, the detection path is different and untested.

### FR-EVAL-001.5: "Significant findings" vs "HIGH severity findings"

**Expected behavior**: This terminology mismatch should be detected as a semantic deviation (WARNING level). The spec uses "significant findings" but the gate uses "HIGH severity findings" -- these may not be synonymous.

**Will the gate catch it?**: Unlikely via gate alone. The SPEC_FIDELITY_GATE checks `high_severity_count_zero` and `tasklist_ready_consistent` but neither semantic check looks for terminology mismatches in the body. The LLM fidelity checker might report it as a MEDIUM finding, which would increment `medium_severity_count` but not block the gate.

**Under convergence**: The semantic layer (`semantic_layer.py`) performs chunked comparison and could detect this as a semantic deviation. However, it would classify it via the debate protocol (prosecutor/defender) only if initially classified as HIGH.

**Assessment**: WEAK DETECTION. The terminology mismatch is a semantic issue that the gate's structural checks cannot catch. Detection depends entirely on the LLM's judgment, with no deterministic enforcement. This is the correct assessment for a WARNING-level seeded ambiguity -- it should be reported but not block.

## Verdict

**NEEDS-REVISION**

**Justification**:

1. **BLOCKING gap -- convergence path untested**: The eval spec does not exercise the `convergence_enabled=True` code path, which is the primary v3.0 change to this stage. The gate bypass (`gate=None`), DeviationRegistry iteration, regression detection, and ConvergenceResult are all v3.0-specific and unexercised. This is a significant coverage gap for a stage that is fundamentally redesigned in v3.0.

2. **WARNING -- frontmatter-to-body consistency unchecked**: Neither SPEC_FIDELITY_GATE nor DEVIATION_ANALYSIS_GATE validates that frontmatter severity counts match the actual findings in the body. An LLM could produce inconsistent output that passes the gate.

3. **WARNING -- seeded ambiguity FR-EVAL-001.4 detection depends on LLM classification**: The gate has no mechanism to verify that a genuinely blocking spec gap (missing schema) was classified at the correct severity. If the LLM misclassifies it as MEDIUM, the gate passes silently.

4. **INFO -- FR-EVAL-001.5 appropriately weak**: The terminology mismatch is correctly positioned as a WARNING-level finding. The gate is not expected to catch it deterministically, and the eval spec should document this as an expected WARNING, not a BLOCKING finding.

**Required revisions before this stage can be marked ADEQUATE**:
- Add eval scenarios for `convergence_enabled=True` exercising multi-run iteration, regression detection, and stable ID persistence
- Add a body-to-frontmatter consistency check (or document why it is intentionally omitted)
- Clarify expected severity classification for FR-EVAL-001.4 in the eval harness assertions
