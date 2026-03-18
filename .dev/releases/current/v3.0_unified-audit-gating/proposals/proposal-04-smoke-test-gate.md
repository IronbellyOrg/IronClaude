# Proposal 04: Smoke Test Gate at Release Tier

**Proposal ID**: P-04
**Target release**: unified-audit-gating-v1.2.1
**Author**: forensic investigation team
**Date**: 2026-03-17
**Status**: Draft

---

## Table of Contents

1. [Problem Statement](#1-problem-statement)
2. [Proposed Solution](#2-proposed-solution)
3. [Fixture Specification](#3-fixture-specification)
4. [Artifact Validation Rules](#4-artifact-validation-rules)
5. [Timeout and Resource Budget](#5-timeout-and-resource-budget)
6. [Implementation Plan](#6-implementation-plan)
7. [Acceptance Criteria](#7-acceptance-criteria)
8. [Risk Assessment](#8-risk-assessment)
9. [Estimated Effort](#9-estimated-effort)

---

## 1. Problem Statement

### 1.1 Why document-level gates cannot detect no-op pipelines

Every gate in the current infrastructure follows one of two signatures:

```python
(content: str) -> bool                              # semantic check
(output_file: Path, criteria: GateCriteria) -> tuple[bool, str | None]  # pipeline gate
```

Both forms evaluate *documents that have already been produced*. The gate infrastructure assumes that if an output file exists with valid structure, the step that created it performed real work.

This assumption breaks in the presence of a no-op executor. The forensic report (`cli-portify-executor-noop-forensic-report.md`, §1) shows that `PortifyExecutor._execute_step()` contains:

```python
else:
    # Default: no-op
    exit_code, stdout, timed_out = 0, "", False
```

When `step_runner` is `None` (the production default), every step returns `(0, "", False)` regardless of what real implementation exists in `steps/`. The executor then writes `return-contract.yaml` listing all 12 steps as completed with `outcome: SUCCESS`. This single file satisfies the only artifact existence check that runs: the cli-portify pipeline verifies `return-contract.yaml` exists and contains `outcome: SUCCESS`. Both conditions are true. The gate system approves the run.

### 1.2 The structural gap

The pipeline's gate hierarchy (forensic report §7) operates at three levels:

| Level | Gates | What they check |
|-------|-------|-----------------|
| Pipeline step gates | G-000 through G-011 | Generated document structure: frontmatter fields, section counts, EXIT_RECOMMENDATION markers |
| Fidelity gates | SPEC_FIDELITY_GATE, TASKLIST_FIDELITY_GATE | LLM-generated severity reports on spec-to-roadmap and roadmap-to-tasklist alignment |
| Release gate (proposed) | Smoke test — does not yet exist | Actual CLI execution against real input, real artifact content validation |

The missing level is a gate that answers the question: **"When I run the CLI command, does real work happen?"**

No existing gate asks this because the gate infrastructure was designed for document pipelines where a document's existence and structure are reliable proxies for the work that produced it. For an executor that dispatches to real step implementations, those proxies break when the dispatch mechanism is absent.

### 1.3 What the no-op produced that looked valid

The no-op run of `superclaude cli-portify run sc-tasklist --output <path> --name tasklist` produced:

```yaml
# return-contract.yaml
completed_steps:
  - validate-config
  - discover-components
  - protocol-mapping
  - analysis-synthesis
  - user-review-p1
  - step-graph-design
  - models-gates-design
  - prompts-executor-design
  - pipeline-spec-assembly
  - user-review-p2
  - release-spec-synthesis
  - panel-review
outcome: SUCCESS
remaining_steps: []
resume_command: ''
suggested_resume_budget: 0
```

This is structurally identical to what a real run would produce. The pipeline exited with code 0. No gate detected the problem because:

1. `return-contract.yaml` exists — file existence check passes
2. `outcome: SUCCESS` is present — frontmatter check passes
3. `completed_steps` lists all 12 steps — completeness check passes
4. Total elapsed time: milliseconds — no gate checks elapsed time
5. No intermediate artifacts were expected by any gate — their absence is not checked

A smoke test gate would have failed condition 4 immediately (execution well under minimum real-work threshold) and failed conditions not yet checked (zero intermediate artifacts, no step implementations invoked).

---

## 2. Proposed Solution

### 2.1 Overview

Add a **smoke test gate** that runs the actual `superclaude cli-portify run` CLI command against a minimal test fixture and validates that:

1. The run takes longer than the no-op threshold (at least 10 seconds of real execution)
2. Intermediate artifacts are produced beyond `return-contract.yaml`
3. At least one intermediate artifact meets minimum content criteria (non-trivial lines, required sections)
4. The step implementations leave evidence of invocation (step-specific content patterns that a no-op cannot produce)

The smoke test gate operates at **release tier** — it is always BLOCKING, no override is permitted (consistent with `resolve_gate_mode()` in `pipeline/trailing_gate.py:607-609` where `GateScope.RELEASE` always returns `GateMode.BLOCKING`).

### 2.2 Gate identity and position in the release workflow

```
Release check sequence (proposed):
  1. Document structure gates (G-000 through G-011) — existing
  2. Fidelity gates (SPEC_FIDELITY_GATE, TASKLIST_FIDELITY_GATE) — existing
  3. SMOKE_TEST_GATE [NEW] — runs before release can be marked complete
     |- Fixture execution
     |- Execution time check (>= MIN_REAL_EXECUTION_SECONDS)
     |- Intermediate artifact presence check (>= MIN_INTERMEDIATE_ARTIFACTS)
     |- Artifact content check (per-artifact rules in §4)
     |- Step invocation evidence check
```

Gate ID: `G-012` (continuing the existing G-000 through G-011 sequence in `cli_portify/gates.py`).

Enforcement tier: `STRICT`, scope: `RELEASE` (always blocking, no override).

### 2.3 Design principles

**The gate must be self-contained.** It creates its own isolated output directory under `tests/fixtures/cli_portify/smoke/` or a `tmp` path, runs the command, validates output, and cleans up. It must not touch any real output directory.

**The gate must distinguish no-op from real.** The central invariant: a no-op run completes in under 1 second; a real run requires at minimum one LLM call per Claude-assisted step, which cannot complete in under 10 seconds on any realistic hardware. The gate exploits this gap.

**The gate validates content, not just existence.** Each intermediate artifact is checked for content patterns that step implementations generate and that a no-op cannot produce (e.g., `analyze-workflow` output must contain workflow-specific component names drawn from the fixture input, not just section headers that could be templated).

**The gate is deterministic in its pass/fail logic.** The smoke test invokes real execution but applies deterministic checks to the result. If execution fails for environmental reasons (network unavailable, Claude API unreachable), the gate fails with class `transient` rather than `policy`, enabling retry without a release block.

---

## 3. Fixture Specification

### 3.1 What constitutes a minimal valid fixture

The `superclaude cli-portify run` command requires a workflow target (a skill directory path), an `--output` path, and a `--name`. The workflow target must resolve to a directory containing at least one component with a `SKILL.md` file (validated by `has_component_inventory()` in `cli_portify/gates.py:143`).

A minimal fixture therefore requires:

```
tests/fixtures/cli_portify/smoke/
  sc-smoke-skill/             # workflow target
    SKILL.md                  # required: triggers has_component_inventory check
    refs/
      minimal-protocol.md     # one ref document (gives discover-components a real component tree)
```

The fixture is "minimal" in that it contains exactly one skill, one `SKILL.md`, and one ref document. This is the smallest input that passes `validate_portify_config()` and produces a non-trivial component tree for `discover-components`.

The fixture is "real" (exercises actual dispatch) because:
- `discover-components` reads the filesystem to build a component inventory — it must find `SKILL.md`
- `analyze-workflow` must process the component tree to generate section-structured output
- `validate-config` checks that required config fields resolve to real paths

A fixture with a nonexistent directory would be caught by `validate_portify_config()` (after Fix 2 from the forensic report is applied). A fixture with an empty `SKILL.md` would produce a trivially-short `discover-components` artifact, which the minimum-lines check in G-001 would catch.

### 3.2 SKILL.md minimum content for the smoke fixture

The smoke fixture `SKILL.md` must contain enough structure to drive real output from the analysis steps. Minimum requirements:

```markdown
---
skill: sc-smoke-skill
version: 0.1.0
description: Minimal smoke test fixture for cli-portify gate validation
---

## Purpose

A minimal skill used exclusively for smoke testing the cli-portify executor.
This skill is not intended for production use.

## Steps

1. Input validation
2. Data processing
3. Output formatting

## Components

- InputValidator: validates input parameters
- DataProcessor: core processing logic
- OutputFormatter: formats results
```

Minimum: 20 lines, one `---` frontmatter block with `skill:` and `description:` fields, at least 2 `##` section headers, at least 2 named components. This ensures `analyze-workflow` can populate the "Source Components" and "Component Analysis" sections with fixture-specific content (the component names "InputValidator", "DataProcessor", "OutputFormatter"), which the smoke gate uses as content evidence checks.

### 3.3 Where fixtures live

```
tests/
  fixtures/
    cli_portify/
      smoke/
        sc-smoke-skill/
          SKILL.md
          refs/
            minimal-protocol.md
        README.md              # describes fixture purpose and maintenance rules
```

Rationale for `tests/fixtures/cli_portify/smoke/` over alternatives:

- Co-located with existing `tests/cli_portify/` test suite — consistent with existing test organization
- Separate from `tests/cli_portify/fixtures/` (which contains Python mock harness code, not filesystem fixtures)
- The `smoke/` subdirectory isolates smoke fixtures from any future unit test fixtures

### 3.4 Fixture maintenance rules

1. The smoke fixture must not be modified without updating the content evidence patterns in the smoke gate (§4.3).
2. The fixture `SKILL.md` must retain the component names `InputValidator`, `DataProcessor`, `OutputFormatter` unless the gate's content checks are updated simultaneously.
3. The fixture must not grow to be a production-representative skill. Its purpose is minimality and speed, not realism.
4. CI must run the smoke test before any release gate is approved. The fixture must therefore remain runnable on the CI environment (no local-only dependencies, no private API keys beyond the standard Claude API key).

---

## 4. Artifact Validation Rules

### 4.1 Artifact presence requirement

A real run of `superclaude cli-portify run` produces intermediate artifacts in addition to `return-contract.yaml`. The smoke gate requires the following artifacts to exist in the output directory:

| Artifact | Step that produces it | Minimum presence check |
|----------|-----------------------|------------------------|
| `return-contract.yaml` | executor (always) | Must exist |
| `discover-components.md` (or equivalent) | step 2 | Must exist |
| `analyze-workflow.md` (or equivalent) | step 3/4 | Must exist |

If only `return-contract.yaml` exists, the gate fails with:
```
SMOKE_TEST_GATE FAILED: intermediate-artifact-absence
  Expected: at least 2 intermediate artifacts beyond return-contract.yaml
  Found: 0
  Diagnosis: Executor likely ran in no-op mode (step implementations not invoked)
```

### 4.2 Minimum content criteria per artifact

Each present artifact must meet tier-proportional content criteria:

**`return-contract.yaml`** (always present — existing check):
- `outcome: SUCCESS`
- `completed_steps` list is non-empty

**`discover-components.md`** (new check):
- Minimum 15 lines
- Contains `SKILL.md` reference (checked by `has_component_inventory()`)
- Contains `source_skill` frontmatter field with value matching fixture skill name (`sc-smoke-skill`)

**`analyze-workflow.md`** (new check):
- Minimum 40 lines
- Contains at least 5 `##` section headers (existing `_check_min_sections(c, 5)` logic)
- Contains `EXIT_RECOMMENDATION` marker
- Must pass content evidence check (§4.3)

### 4.3 Content evidence checks — distinguishing real from stub output

Content evidence checks verify that artifacts contain content that the step implementation generates from the specific fixture input, and that cannot be produced by a no-op returning `(0, "", False)`.

The no-op produces no artifacts whatsoever. But a more sophisticated stub might produce templated artifacts. The evidence checks defend against both.

**Evidence check for `analyze-workflow.md`**: The artifact must contain at least one of the component names from the smoke fixture (`InputValidator`, `DataProcessor`, `OutputFormatter`). These names come from the fixture `SKILL.md`; a generic template cannot contain them without reading the fixture.

```python
def _check_analyze_workflow_content_evidence(content: str) -> bool:
    """Verify analyze-workflow artifact references fixture-specific component names."""
    fixture_components = ["InputValidator", "DataProcessor", "OutputFormatter"]
    return any(name in content for name in fixture_components)
```

**Evidence check for `discover-components.md`**: The artifact must reference `sc-smoke-skill` (the fixture skill name). A template artifact using a different skill name fails this check.

```python
def _check_discover_components_content_evidence(content: str) -> bool:
    """Verify discover-components artifact references the smoke fixture skill."""
    return "sc-smoke-skill" in content
```

**Failure condition**: If an artifact exists but fails a content evidence check, the gate fails with:
```
SMOKE_TEST_GATE FAILED: content-evidence-absent
  Artifact: analyze-workflow.md
  Check: analyze_workflow_content_evidence
  Reason: Artifact does not reference any fixture-specific component names
  Diagnosis: Step may have run with templated/stub output rather than real execution
```

### 4.4 Non-trivial content patterns

Beyond evidence checks, artifacts must not exhibit stub signatures:

1. **No placeholder sentinels**: `{{SC_PLACEHOLDER:*}}` patterns indicate an unreplaced template. The existing `has_zero_placeholders()` check applies.
2. **No zero-content sections**: A section header followed immediately by another section header (no body text between) indicates a stub. Minimum 3 non-blank lines between consecutive `##` headers.
3. **No repeated boilerplate**: If the same paragraph (>20 words) appears in two different artifacts, both artifacts are flagged as likely templated.

### 4.5 What the gate does NOT check

The smoke gate does not validate:
- Semantic correctness of the analysis (LLM output quality is out of scope for a gate)
- Section content accuracy against the fixture (would require LLM judgment)
- Exact line counts (these would make the gate brittle to minor prompt changes)

The gate checks existence, structure, and fixture-specific content markers. This is sufficient to distinguish real execution from no-op or templated output.

---

## 5. Timeout and Resource Budget

### 5.1 The no-op / real-run time gap

The forensic report establishes the key observable: the no-op run completes in milliseconds. Specifically, the executor races through 12 steps with `(0, "", False)` returns and writes `return-contract.yaml` with no I/O beyond that single file write. Wall-clock time is under 1 second.

A real run requires, at minimum:
- Config validation and filesystem discovery: ~1 second
- One LLM call per Claude-assisted step: ~10-60 seconds each depending on model and context length
- User review steps (paused, or bypassed in `--dry-run` mode): 0 seconds if bypassed

For the smoke gate, we run with an additional flag `--skip-review` (or equivalent) to bypass interactive user review steps. With review steps skipped, a real run of the 5 Claude-assisted steps on the minimal smoke fixture should complete in 30-300 seconds depending on API response times.

### 5.2 Timeout budget definitions

| Budget | Value | Rationale |
|--------|-------|-----------|
| `SMOKE_NOOP_CEILING_S` | 5 seconds | Any run completing in under 5 seconds is definitionally a no-op or near-no-op. Real config validation + filesystem I/O alone takes longer. |
| `SMOKE_MIN_REAL_EXECUTION_S` | 10 seconds | Lower bound for a run that invokes at least one real step implementation. Even the fastest programmatic step (validate-config) reads and parses YAML from disk. |
| `SMOKE_TIMEOUT_S` | 600 seconds | Upper bound for the full smoke run. 10 minutes allows for slow API responses and CI environment variability without indefinitely blocking release. |
| `SMOKE_STEP_TIMEOUT_S` | 120 seconds | Per-step timeout passed to the executor. Consistent with existing `turn_budget` parameters in the executor. |

### 5.3 How the gate uses timing to catch no-ops

```python
def _check_execution_time(elapsed_s: float) -> tuple[bool, str]:
    if elapsed_s < SMOKE_NOOP_CEILING_S:
        return False, (
            f"Execution completed in {elapsed_s:.2f}s — below no-op ceiling "
            f"({SMOKE_NOOP_CEILING_S}s). Pipeline likely ran in no-op mode."
        )
    return True, ""
```

The timing check is the fastest-failing check. It runs first. If it fails, artifact checks are skipped and the gate fails immediately with diagnosis pointing to the no-op executor pattern.

The no-op ceiling (5 seconds) is conservative: even if CI environments are slow, a no-op executor cannot take 5 seconds unless the machine is severely under load. If a CI machine is so slow that a no-op takes 5 seconds, all other timeouts will be proportionally exceeded and the run will fail anyway.

### 5.4 Resource constraints

**Disk**: The smoke run writes to a temporary directory under `tests/fixtures/cli_portify/smoke/output/` or a `tempfile.mkdtemp()` path. Maximum expected output: 10 artifact files, each under 50KB. Total disk budget: 2MB.

**CPU**: The smoke run is single-process with subprocess invocations for Claude steps. No parallel execution constraint beyond what the executor already manages.

**Network**: The smoke run requires Claude API access. If the API is unavailable, the gate fails with `transient` failure class (retryable). The gate must not be classified as `policy` failure when the root cause is network unavailability.

**Environment isolation**: The smoke run uses `--output` pointing to a temporary directory that is created fresh for each run and deleted on completion (success or failure). It must never write to the real output directory of the release being gated.

### 5.5 Isolation strategy

```python
import tempfile
import shutil
from pathlib import Path

def run_smoke_test(fixture_path: Path) -> SmokeTestResult:
    tmpdir = Path(tempfile.mkdtemp(prefix="sc_smoke_"))
    try:
        result = _execute_smoke_run(fixture_path, output_dir=tmpdir)
        return _validate_smoke_artifacts(result, output_dir=tmpdir)
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)
```

The `finally` block ensures cleanup even if the validation raises an exception. The `ignore_errors=True` flag prevents cleanup failures from masking the real gate result.

---

## 6. Implementation Plan

### 6.1 Files to create

**`tests/fixtures/cli_portify/smoke/sc-smoke-skill/SKILL.md`**
The minimal smoke fixture skill document as specified in §3.2.

**`tests/fixtures/cli_portify/smoke/sc-smoke-skill/refs/minimal-protocol.md`**
A minimal ref document (10-20 lines) providing the component descriptions that `analyze-workflow` will reference.

**`tests/fixtures/cli_portify/smoke/README.md`**
Maintenance instructions: what the fixture contains, what must remain stable (component names), and what the gate checks.

**`src/superclaude/cli/cli_portify/smoke_gate.py`**
New module implementing:
- `SmokeTestConfig` dataclass (fixture path, output dir, timeout budgets)
- `SmokeTestResult` dataclass (elapsed_s, artifacts_found, gate_failures)
- `run_smoke_test(config: SmokeTestConfig) -> SmokeTestResult`
- `_check_execution_time(elapsed_s: float) -> tuple[bool, str]`
- `_check_intermediate_artifacts(output_dir: Path) -> tuple[bool, str]`
- `_check_artifact_content(artifact_path: Path, checks: list[SemanticCheck]) -> tuple[bool, str]`
- `SMOKE_TEST_GATE: GateCriteria` (enforcement_tier="STRICT", with all checks registered)

**`tests/cli_portify/test_smoke_gate.py`**
Unit tests for the smoke gate logic:
- `test_noop_run_fails_timing_check` — mock execution returning in <5s fails the gate
- `test_missing_intermediate_artifacts_fails` — only `return-contract.yaml` present fails the gate
- `test_content_evidence_absent_fails` — artifact without fixture component names fails
- `test_real_run_artifacts_pass` — well-formed artifacts matching fixture names pass
- `test_transient_failure_on_api_error` — network error produces `transient` not `policy` failure class

### 6.2 Files to modify

**`src/superclaude/cli/cli_portify/gates.py`**
Add `SMOKE_TEST_GATE` (G-012) to `GATE_REGISTRY`:
```python
GATE_REGISTRY["smoke-test"] = SMOKE_TEST_GATE
```

**`src/superclaude/cli/pipeline/trailing_gate.py`**
No changes required to `TrailingGateRunner` or `resolve_gate_mode()`. The smoke gate uses the existing `GateScope.RELEASE` path which already returns `GateMode.BLOCKING`.

**`src/superclaude/cli/cli_portify/commands.py`**
Add smoke gate invocation to the release check path. Before any completion/release transition is allowed, call `run_smoke_test()`. This is separate from the existing step-level gate checks and runs once at the end of the pipeline, not per-step.

### 6.3 Integration points in the release workflow

The smoke test gate integrates at two points:

**Point 1: Pre-release check in the sprint executor**

Before `superclaude sprint` can mark a cli-portify release task as complete, the sprint executor must verify the smoke gate has passed. This integrates with the unified-audit-gating v1.2.1 `audit_release_passed` state transition. Concretely: the release task enters `ready_for_audit_release`, the smoke gate runs, and only `audit_release_passed` permits transition to `released`.

**Point 2: Standalone CLI command**

```bash
superclaude cli-portify smoke-test --fixture tests/fixtures/cli_portify/smoke/sc-smoke-skill
```

This allows developers to run the smoke gate independently during development, before triggering a full release audit. It produces a human-readable report of which checks passed or failed.

### 6.4 Gate infrastructure fit

The smoke gate does **not** use `TrailingGateRunner`. Trailing gates are designed for post-step artifact checks that can run asynchronously. The smoke gate is a pre-release blocking check that requires serial execution:

1. Run the CLI command (blocking, with timeout)
2. Validate artifacts (deterministic, fast)
3. Report pass/fail (blocking, no retry)

The smoke gate uses `GateScope.RELEASE` and `resolve_gate_mode(GateScope.RELEASE)` which always returns `GateMode.BLOCKING`. There is no trailing, deferred, or retry-once behavior: the smoke gate either passes or blocks the release.

The smoke gate does **not** extend `GateCriteria` + `gate_passed()`. The `gate_passed()` function in `pipeline/gates.py` validates an existing artifact against criteria. The smoke gate must first *produce* artifacts by running the CLI, then validate them. It uses `GateCriteria` for the per-artifact validation phase only.

The smoke gate fits the `GateFailure` dataclass from `cli_portify/gates.py` for reporting failures:
```python
GateFailure(
    gate_id="G-012",
    check_name="execution_time",
    diagnostic="Execution completed in 0.12s — below no-op ceiling (5s)",
    artifact_path=str(output_dir / "return-contract.yaml"),
    tier="STRICT",
)
```

---

## 7. Acceptance Criteria

### 7.1 Would a smoke test gate have caught the no-op pipeline?

Yes, definitively. Three independent checks would have fired:

| Check | No-op result | Gate decision |
|-------|-------------|---------------|
| Execution time | ~0.12 seconds (well under 5s ceiling) | FAIL: timing check |
| Intermediate artifact presence | Zero intermediate artifacts, only `return-contract.yaml` | FAIL: artifact absence |
| Content evidence | No artifacts to check (no intermediate files) | FAIL: vacuously (absence implies no evidence) |

Any single one of these failures is sufficient to block the release. All three would fire simultaneously.

### 7.2 Formal acceptance criteria for the gate implementation

**AC-001**: Given the no-op executor (step_runner=None), the smoke gate must fail with `check_name="execution_time"` when elapsed time is under `SMOKE_NOOP_CEILING_S`.

**AC-002**: Given a run that produces only `return-contract.yaml` and no intermediate artifacts, the gate must fail with `check_name="intermediate-artifact-absence"`.

**AC-003**: Given a run that produces artifacts without fixture-specific content (e.g., templated artifacts with generic placeholder text), the gate must fail with `check_name="content-evidence-absent"` for the relevant artifact.

**AC-004**: Given a real run against the smoke fixture that completes in more than `SMOKE_MIN_REAL_EXECUTION_S`, produces at least 2 intermediate artifacts, and passes all content evidence checks, the gate must pass.

**AC-005**: Given a run that fails due to Claude API unavailability (network error, HTTP 429, HTTP 503), the gate must fail with `failure_class="transient"`, not `failure_class="policy"`.

**AC-006**: The smoke gate must clean up its temporary output directory on both pass and fail. After gate execution, no files must remain in the temporary output path.

**AC-007**: The smoke gate must not write to any path outside the designated temporary output directory. Real release output directories must not be touched.

**AC-008**: The gate must complete within `SMOKE_TIMEOUT_S` (600 seconds). If the CLI invocation exceeds this budget, the gate fails with `failure_class="timeout"`.

### 7.3 Regression check

As a standalone validation, run the gate against the known-bad executor (with `step_runner` not provided) and verify exit code is non-zero and the gate report contains at least one `SMOKE_TEST_GATE FAILED` entry. This regression check must be included in the CI test suite as a permanently-preserved test case documenting the exact bug class the gate was designed to catch.

---

## 8. Risk Assessment

### 8.1 Flaky tests due to LLM non-determinism

**Risk**: Claude API responses vary between runs. A real execution may produce artifacts with different content on each run, making content evidence checks unreliable if they pattern-match against specific phrases.

**Mitigation**: Content evidence checks match against fixture-specific names (`InputValidator`, `DataProcessor`, `OutputFormatter`) that are drawn from the fixture input, not from LLM output phrasing. A real LLM processing the fixture will reference these component names because they appear in the `SKILL.md` it is analyzing. The checks do not match against analysis conclusions, quality judgments, or phrasing — only against proper nouns from the fixture.

**Residual risk**: Low. The fixture component names are distinctive and will appear in any genuine analysis of the fixture, regardless of LLM variation.

### 8.2 Environment-dependent failures

**Risk**: CI environments may lack Claude API access, have rate limits, or have different filesystem performance characteristics, causing the smoke gate to fail for environmental rather than code reasons.

**Mitigation**:
1. Network failures produce `transient` failure class, which is retryable (per §5.2 and AC-005).
2. The `SMOKE_NOOP_CEILING_S` (5 seconds) is conservative enough to accommodate slow CI environments. A no-op cannot take 5 seconds except on severely overloaded machines.
3. The `SMOKE_TIMEOUT_S` (600 seconds) provides a wide window for slow API responses.

**Residual risk**: Medium. CI environments with no API access require either a mock mode or CI skip configuration. This must be documented in the `smoke/README.md` (§3.4). A `--mock-llm` flag on the smoke test command could allow CI to validate all non-LLM checks without hitting the API.

### 8.3 Smoke fixture drift

**Risk**: The smoke fixture `SKILL.md` is modified (e.g., component names changed), but the content evidence checks in the gate are not updated. The gate then fails against a legitimate real run.

**Mitigation**:
1. The `smoke/README.md` documents the stability contract for component names.
2. The content evidence check patterns are co-located in `smoke_gate.py` with a comment linking to the fixture: `# Matches component names in tests/fixtures/cli_portify/smoke/sc-smoke-skill/SKILL.md`.
3. A separate unit test (`test_fixture_content_matches_gate_patterns`) reads the fixture `SKILL.md` and verifies that the component names in the gate's evidence checks are present in the fixture. This test fails fast if the fixture is updated without updating the gate.

**Residual risk**: Low if the co-location comment and unit test are maintained.

### 8.4 Smoke test false negatives from superficially-real stubs

**Risk**: A future no-op variant writes fake intermediate artifacts with fixture component names without actually invoking step implementations.

**Mitigation**: The timing check (elapsed time > 5 seconds) still fires for a synchronous fake-artifact writer that completes in milliseconds. A stub fast enough to produce multiple files with correct structure and fixture-specific content in under 5 seconds is not a practical attack on the gate — any code that does that work is, by definition, doing real work.

**Residual risk**: Very low. The gate is designed to catch accidental no-ops (development placeholders that became production behavior), not adversarial bypass attempts.

### 8.5 Interaction with Fix 1 and Fix 2 from the forensic report

**Risk**: The smoke gate is designed assuming Fix 1 (wire `run_portify()` to step dispatch) and Fix 2 (add `validate_portify_config()` call) are applied. Without Fix 1, the smoke gate will catch the no-op but cannot distinguish "Fix 1 not applied" from "real execution failure." Without Fix 2, the gate may fail because the fixture path resolution is not validated before execution.

**Mitigation**: The smoke gate is a release gate, not a bug fix. It must not be deployed as a substitute for Fix 1 and Fix 2. The implementation plan in §6 is ordered: Fix 1 and Fix 2 are prerequisite to deploying the smoke gate in production. The gate then provides ongoing regression protection.

**Residual risk**: None, given correct deployment order.

### 8.6 Long smoke test duration in release workflows

**Risk**: The smoke test takes 2-5 minutes. In a release workflow where releases are frequent, this adds meaningful wall-clock latency.

**Mitigation**:
1. The smoke test runs once per release, not per step or per commit. Release frequency is low (weekly or less).
2. The `--mock-llm` mode (§8.2) can be used for pre-release developer checks; only the final release gate invocation requires real API calls.
3. The 600-second timeout is a ceiling, not an expectation. Typical runs against the minimal fixture should complete in 60-120 seconds.

**Residual risk**: Low. Release gate latency is acceptable for a release-tier check.

---

## 9. Estimated Effort

| Work item | Effort |
|-----------|--------|
| Create smoke fixture (`SKILL.md`, `minimal-protocol.md`, `README.md`) | 2 hours |
| Implement `smoke_gate.py` (core gate logic, timing check, artifact checks, content evidence checks, isolation) | 1 day |
| Implement `test_smoke_gate.py` (unit tests, regression test for no-op case, AC-001 through AC-008) | 1 day |
| Integrate gate into `commands.py` release path and `GATE_REGISTRY` | 3 hours |
| Add CI configuration for smoke test (API key, skip logic for environments without API access, mock mode) | 4 hours |
| Documentation: update `smoke/README.md`, add stability contract notes | 1 hour |
| **Total** | **~3 days** |

### Prerequisites (not counted in this estimate)

- Fix 1 from forensic report: wire `run_portify()` to step dispatch (~1 day, separate work item)
- Fix 2 from forensic report: add `validate_portify_config()` call to `commands.py` (~2 hours, separate work item)

Both prerequisites must be complete before the smoke gate can pass a real run. The gate implementation can be developed and unit-tested in parallel with Fix 1, using mocked invocations, but integration testing requires Fix 1.

### Sequencing

```
Week 1: Fix 1 + Fix 2 (prerequisite bug fixes)
Week 2: smoke_gate.py + unit tests
Week 3: Integration, CI configuration, regression test
         → smoke gate operational at release tier
```

---

## Appendix A: Gate Failure Report Format

The smoke gate produces a structured failure report when any check fails:

```
SMOKE_TEST_GATE (G-012) FAILED
================================
Run: superclaude cli-portify run sc-smoke-skill --output <tmpdir> --name smoke
Elapsed: 0.12s

FAILED CHECKS:
  1. execution_time [STRICT]
     Elapsed 0.12s is below no-op ceiling (5.0s)
     Diagnosis: Executor likely ran in no-op mode (step_runner=None)
     Fix: Verify run_portify() passes step_runner to PortifyExecutor

  2. intermediate-artifact-absence [STRICT]
     Found 0 intermediate artifacts (expected >= 2)
     Artifacts present: ['return-contract.yaml']
     Diagnosis: Step implementations were not invoked
     Fix: See Fix 1 in forensic report: wire run_portify() to step dispatch

PASSED CHECKS: none

GATE DECISION: BLOCKED (release cannot proceed)
```

---

## Appendix B: Relationship to Unified Audit Gating v1.2.1

The smoke gate proposal is a concrete implementation of the "Smoke test gate at release tier" item identified in the forensic report (§8, "What Would Make It 8+/10") and listed as Mitigation 5 (§10).

Within the unified-audit-gating v1.2.1 framework (release spec §4.1), the smoke gate occupies the `audit_release_running` state of the release scope state machine. It must pass before `audit_release_passed` can be reached. If it fails, the state transitions to `audit_release_failed` and the `ready_for_audit_release -> released` path remains blocked until the underlying code is fixed and the gate is retried.

The gate does not conflict with any locked decision in the v1.2.1 spec (§2.1). Specifically:
- Locked Decision 3 ("Overrides allowed only for task/milestone, never release") is respected: the smoke gate has no override path.
- Locked Decision 2 ("Tier-1 gate is required even for LIGHT/EXEMPT flows") is unaffected: the smoke gate is an additional release-tier check, not a replacement for existing tier-1 checks.

The smoke gate addresses the gap identified in the forensic report's scoring table (§8, "Would detect silent success / no-op fallback: 1/10") and raises the system's ability to detect the cli-portify no-op class from 1/10 to a definitive catch.
