---
stage: 10
stage_name: wiring-verification
depth: standard
gate: WIRING_GATE
verdict: NEEDS-REVISION
---

# Stage 10: wiring-verification -- Adversarial Review

## Q1: Meaningful Output

The wiring-verification stage will produce **meaningful but potentially vacuous output** when run against the eval spec's target codebase.

The eval spec (FR-EVAL-001) describes adding a single new file (`progress.py`) and modifying three existing files (`executor.py`, `commands.py`, `gates.py`). The wiring analysis runs three detectors:

- **G-001 (Unwired Callables)**: Scans for `Optional[Callable]` constructor parameters never wired at any call site. `progress.py` as described in the eval spec's Section 4.5 defines two dataclasses (`StepProgress`, `PipelineProgress`) with no `Optional[Callable]` parameters. This detector will produce **zero findings** for the new code.

- **G-002 (Orphan Modules)**: Detects modules in provider directories (`steps/`, `handlers/`, `validators/`, `checks/`) with zero inbound imports. `progress.py` lives in `src/superclaude/cli/roadmap/`, not a provider directory. This detector will produce **zero findings** for the new code.

- **G-003 (Broken Registries)**: Detects dict assignments matching `*_REGISTRY`, `*_DISPATCH`, etc. with unresolvable values. The eval spec adds no new registries. This detector will produce **zero findings** for the new code.

The gate will **trivially pass** with `total_findings: 0`, `blocking_findings: 0`, and all five semantic checks satisfied. This is not inherently a problem -- a clean wiring report is valid output -- but it means the eval spec does **not** exercise the wiring gate's ability to detect and correctly report actual findings. The gate's value is entirely in its structural validation (16 frontmatter fields present, semantic consistency checks pass), not in its analytical power.

**Risk**: A broken `emit_report()` that silently produces zero findings due to a bug (e.g., wrong `source_dir`) would still pass. The eval spec cannot distinguish "clean codebase" from "analyzer misconfigured."

## Q2: v3.0 Changes

Wiring-verification is **entirely new in v3.0**. There is no equivalent stage on the `master` branch. The changes are:

1. **New pipeline step**: `wiring-verification` is added as step 9 (0-indexed) in `_build_steps()` at `executor.py:526-538`. It is the first step that does NOT invoke a Claude subprocess -- it runs `run_wiring_analysis()` directly in-process (lines 244-259).

2. **New gate definition**: `WIRING_GATE` in `src/superclaude/cli/audit/wiring_gate.py:973-1026` defines 16 required frontmatter fields and 5 semantic checks. This is the most field-dense gate in the pipeline (EXTRACT_GATE has 13, DEVIATION_ANALYSIS_GATE has 9).

3. **TRAILING gate mode**: The step uses `gate_mode=GateMode.TRAILING`, meaning gate failures do not block subsequent steps. Combined with `rollout_mode="soft"` (hardcoded at executor.py:248), this creates a double-safety net -- even if findings exist, only criticals block in soft mode, and TRAILING mode prevents those blocks from halting the pipeline anyway.

4. **Deterministic execution**: `timeout_seconds=60`, `retry_limit=0`. No LLM variance. The analysis is pure Python AST parsing with deterministic output for a given codebase snapshot.

5. **New module hierarchy**: Three new files (`wiring_gate.py`, `wiring_config.py`, `wiring_analyzer.py`) in `src/superclaude/cli/audit/` with explicit NFR-007 compliance (no imports from pipeline logic, only from pipeline models).

## Q3: Artifact Verification

**Artifact**: `{output_dir}/wiring-verification.md` -- a Markdown file with YAML frontmatter.

**Third-party verification checklist**:

1. **Frontmatter completeness**: Parse the YAML frontmatter and verify all 16 fields are present: `gate`, `target_dir`, `files_analyzed`, `rollout_mode`, `analysis_complete`, `unwired_callable_count`, `orphan_module_count`, `unwired_registry_count`, `critical_count`, `major_count`, `info_count`, `total_findings`, `blocking_findings`, `whitelist_entries_applied`, `files_skipped`, `audit_artifacts_used`.

2. **Semantic invariant 1 (category consistency)**: `total_findings == unwired_callable_count + orphan_module_count + unwired_registry_count`. Verifiable by arithmetic on frontmatter values.

3. **Semantic invariant 2 (severity consistency)**: `critical_count + major_count + info_count == total_findings`. Same.

4. **Semantic invariant 3 (blocking logic)**: For `rollout_mode: shadow`, `blocking_findings` must be 0. For `soft`, blocking equals critical count. For `full`, blocking equals critical + major.

5. **Section completeness**: 7 Markdown sections must be present: Summary, Unwired Optional Callable Injections, Orphan Modules / Symbols, Unregistered Dispatch Entries, Suppressions and Dynamic Retention, Recommended Remediation, Evidence and Limitations.

6. **Reproducibility**: Run `run_wiring_analysis()` independently against the same `source_dir` and compare the report. Because the analysis is deterministic, byte-for-byte comparison should match (modulo `scan_duration_seconds`).

**Weakness**: A verifier cannot confirm that `files_analyzed` is correct without independently counting Python files in the target directory and applying the same exclude patterns. The report is self-consistent but not externally anchored.

## Q4: Most Likely Failure Mode

**The most likely failure mode is `source_dir` misconfiguration causing the analyzer to scan the wrong directory (or an empty directory), producing a trivially clean report that masks real wiring issues.**

Evidence for this assessment:

1. In `executor.py:249`, the source directory is computed as:
   ```python
   source_dir = config.output_dir.parent if hasattr(config, 'output_dir') else Path(".")
   ```
   This is fragile. `config.output_dir` is the pipeline's output directory (where artifacts are written), and `.parent` may or may not point to the actual source code root. For a typical invocation like `superclaude roadmap run spec.md --output ./out`, `output_dir` would be `./out` and `source_dir` would be `.` (current working directory), which happens to be correct. But if `output_dir` is an absolute path like `/tmp/roadmap-output/`, then `source_dir` becomes `/tmp/roadmap-output` -- which contains no Python source files at all.

2. The `_collect_python_files()` function silently returns an empty list when no `.py` files are found, producing `files_analyzed: 0` and `total_findings: 0`. All five semantic checks still pass. The gate passes. No error, no warning.

3. The eval spec does not define where the pipeline output directory will be relative to the source tree, so this failure mode is plausible in eval runs.

**Secondary failure mode**: The hardcoded `rollout_mode="soft"` in executor.py:248 disagrees with the eval spec's FR-EVAL-001.6 acceptance criterion that the progress entry must include `rollout_mode` "from the wiring gate configuration." If the eval expects the mode to come from a CLI flag or config file rather than being hardcoded, the test will fail on expectation mismatch.

## Q5: Eval Spec Coverage

FR-EVAL-001.6 specifies three acceptance criteria for the wiring-verification progress entry:

1. **`unwired_count`, `orphan_count`, `blocking_count` in progress entry**: The eval spec requires these values to be captured in `progress.json`. This requires the progress reporter (new `progress.py`) to extract values from the wiring report's frontmatter or from the `WiringReport` object directly. The eval spec does **not** specify which extraction method to use (parse frontmatter vs. pass the WiringReport object), creating implementation ambiguity.

2. **`rollout_mode` from wiring gate config**: The eval spec says "from the wiring gate configuration," but the v3.0 implementation hardcodes `rollout_mode="soft"` in the executor. The wiring gate config (`WiringConfig`) defaults to `"shadow"`. The actual report will say `"soft"` because that is what the executor passes. The eval spec's phrasing is ambiguous about whether it means the WiringConfig default or the executor's override.

3. **Gate verdict reflects WIRING_GATE semantic check results**: Because the gate mode is TRAILING, the gate verdict is computed but does not block. The eval spec does not acknowledge TRAILING mode at all. FR-EVAL-001.1 defines `gate_verdict` as "pass/fail/null" but does not define a distinct status for "evaluated but non-blocking" (TRAILING). This means the progress entry will record a verdict of "pass" or "fail" without indicating that the verdict was advisory-only.

**Coverage gap**: The eval spec's Section 2.2 workflow diagram shows wiring-verification as step 10, which is correct. However, the eval spec does not account for the fact that wiring-verification is the only step that runs in-process (no Claude subprocess). The progress reporter's timing measurement (`duration_ms`) will be qualitatively different (milliseconds vs. minutes) from other steps. While this is not a functional gap, it means integration tests that validate timing ranges will need wiring-specific thresholds.

**Coverage gap**: The eval spec's data model (Section 4.5) defines `StepProgress.metadata` as `dict` but does not define the schema for wiring-specific metadata keys (`unwired_count`, `orphan_count`, `blocking_count`, `rollout_mode`). FR-EVAL-001.6 requires these fields but does not specify whether they go in `metadata` or as top-level fields. This is a spec-internal inconsistency that will surface during implementation.

**Does the eval spec account for v3.0 changes?** Partially. FR-EVAL-001.6 explicitly references `WIRING_GATE` and the wiring-specific fields, demonstrating awareness of the new stage. However, it does not account for:
- TRAILING gate mode semantics in the progress entry
- The in-process execution model (no subprocess timing)
- The `source_dir` derivation logic
- The hardcoded `rollout_mode="soft"` override vs. WiringConfig default

## Verdict

**NEEDS-REVISION**

The eval spec correctly identifies the wiring-verification stage and its key outputs (FR-EVAL-001.6), but has three issues requiring revision:

1. **Trivially passing gate**: The eval spec's target codebase (adding `progress.py` and modifying three files) will produce zero wiring findings, meaning the gate passes without exercising any of its analytical detectors. The eval should either (a) include a synthetic test fixture with known wiring defects to verify detection, or (b) explicitly acknowledge that this stage's eval value is limited to structural gate validation only.

2. **TRAILING mode not reflected in progress schema**: FR-EVAL-001.1 defines `gate_verdict` as "pass/fail/null" but does not define how TRAILING (non-blocking) verdicts are recorded. The progress entry needs a `gate_mode` field or a distinct verdict value like "advisory-pass"/"advisory-fail" to distinguish blocking from non-blocking outcomes.

3. **Metadata schema gap**: FR-EVAL-001.6 requires `unwired_count`, `orphan_count`, `blocking_count`, and `rollout_mode` in the progress entry, but Section 4.5's data model (`StepProgress`) does not define where these live. They must be explicitly placed in the `metadata` dict with defined key names to be testable.

None of these are blocking -- the pipeline will run and the gate will pass. But the eval's ability to verify the wiring-verification integration is weakened by these gaps, reducing the stage from a meaningful validation checkpoint to a structural completeness check.
