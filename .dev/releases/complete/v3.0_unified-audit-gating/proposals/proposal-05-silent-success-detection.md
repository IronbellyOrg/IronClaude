# Proposal 05 — Silent Success Detection

**Date**: 2026-03-17
**Proposal dimension**: Silent success anti-pattern detection
**Reference incident**: cli-portify executor no-op bug (v2.24 – v2.25)
**Status**: Draft for debate

---

## 1. Problem Statement

### 1.1 The Anti-Pattern

The cli-portify no-op bug exhibits a precise failure mode: a function that does no real work returns
a tuple indistinguishable from a real success. In `executor.py:393-415`:

```python
def _execute_step(self, step: PortifyStep) -> PortifyStatus:
    if self._step_runner is not None:
        exit_code, stdout, timed_out = self._step_runner(step)
    else:
        # Default: no-op (real subprocess invocation belongs in process.py)
        exit_code, stdout, timed_out = 0, "", False
```

Because `run_portify()` at `executor.py:1395-1401` never passes `step_runner`, every step returns
`(exit_code=0, stdout="", timed_out=False)`. The status classifier `_determine_status()` sees
`exit_code=0`, no `EXIT_RECOMMENDATION_MARKER` in `stdout`, and no artifact file on disk — and
returns `PortifyStatus.PASS_NO_REPORT` (not an error; no retry; pipeline continues). Twelve steps
complete in milliseconds, `return-contract.yaml` reports `outcome: SUCCESS`, and the process exits.
No real work was performed.

### 1.2 Why Every Existing Gate Missed It

The gate infrastructure is organized around document content validation:

| Gate | What It Checks | Why It Missed the No-Op |
|------|---------------|-------------------------|
| `SPEC_FIDELITY_GATE` (`roadmap/gates.py:633-656`) | LLM-generated spec-vs-roadmap severity report | Validates document structure; no visibility into runtime execution |
| `TASKLIST_FIDELITY_GATE` (`tasklist/gates.py:20-43`) | LLM-generated roadmap-vs-tasklist severity report | Same; the tasklist itself lacked a wiring task, so nothing was missing |
| G-000 through G-011 (`cli_portify/gates.py`) | Artifact file existence, frontmatter fields, section headers, sentinel removal | None of these artifacts were ever created; gates were never reached |
| Sprint executor exit code check | `subprocess.run()` exit code == 0 | The no-op returned exit_code=0; gate passed |
| `pipeline/gates.py:gate_passed()` | File existence, min lines, YAML fields, semantic checks | Preconditioned on a file existing; no file means no gate invocation |

The forensic report (Section 7) summarizes this as: "Every gate follows the signature
`(content: str) -> bool` or `(output_file: Path, criteria) -> tuple[bool, str|None]`. They validate
that generated documents have correct structure. No gate anywhere asks: 'Does the code connect its
components?'" The no-op produced `return-contract.yaml` with `outcome: SUCCESS` — a valid document
with valid structure — so every document-level check that was reachable approved it.

### 1.3 The Three Signatures of Silent Success

The specific no-op manifests three observable signals simultaneously, each suspicious alone but
collectively diagnostic:

1. **Empty stdout** — `stdout=""` across all 12 steps. Real CLI tools write progress, errors, or
   confirmation messages. An entire 12-step pipeline producing zero bytes of output is anomalous.

2. **Zero elapsed time** — 12 pipeline steps completing in under 100ms wall-clock time. Steps
   like `panel-review` carry `timeout_s=1200` in `STEP_REGISTRY`. Even the fastest real step
   (config validation) involves filesystem I/O and YAML parsing. Sub-millisecond "execution" of
   a step with a 20-minute timeout budget is physically impossible for real work.

3. **Minimal artifact set** — Only `return-contract.yaml` was produced. The pipeline is specified
   to produce per-step artifacts: `workflow-analysis.md`, `pipeline-design.md`,
   `portify-release-spec.md`, `phase1-approval.yaml`, `phase2-approval.yaml`, etc. A successful
   12-step pipeline producing only the terminal contract document is structurally incomplete.

No single signal has zero legitimate explanations. A fast config-validation step that fails early
might have empty stdout and short elapsed time. A step that reads and re-emits an existing file
might not look "fresh". But the combination of all three signals, across all 12 steps, has no
plausible legitimate explanation. This proposal formalizes that combination into a composite
suspicion score that triggers a blocking gate failure.

### 1.4 Scope of This Proposal

This proposal addresses runtime execution quality: did the pipeline actually do work? It is
complementary to, and does not replace:

- **Proposal 03** (Code Integration Gate): static analysis of whether components are wired
- **Proposal 04** (Smoke Test Gate): black-box test that invokes the CLI and inspects output

Proposal 03 would catch the no-op at development time via static analysis of `step_runner=None`.
Proposal 04 would catch it via integration test. This proposal catches it during any production
pipeline run, without requiring a separate test harness, by examining the execution trace the
pipeline already produces.

---

## 2. Proposed Solution

### 2.1 Overview

Introduce a `SilentSuccessDetector` module that runs as a post-execution audit step after the
pipeline's main execution loop completes but before `return-contract.yaml` is written. It collects
three classes of signals — artifact content validation, execution trace verification, and output
freshness cross-referencing — scores each signal, combines them into a composite suspicion score,
and fails the pipeline with a structured diagnostic if the score exceeds a configurable threshold.

The detector does not modify execution semantics. It is purely observational: it reads the execution
trace the executor already captures (step durations, stdout byte counts, subprocess spawn counts)
and the filesystem state after execution. Existing steps, gates, and the status classifier are
unchanged.

### 2.2 Placement in Execution Flow

```
run_portify(config)
    └── executor.run()
            ├── for step in steps: _execute_step(step)   [existing]
            ├── _emit_return_contract()                   [existing, deferred to after detector]
            └── SilentSuccessDetector.evaluate(trace)    [NEW — before contract emission]
                    ├── artifact_content_signals()
                    ├── execution_trace_signals()
                    ├── output_freshness_signals()
                    └── composite_score()
                            └── if score >= THRESHOLD: raise SilentSuccessError
```

`_emit_return_contract()` is moved to after the detector. If the detector raises
`SilentSuccessError`, the contract is written with `outcome: SILENT_SUCCESS_SUSPECTED` rather than
`outcome: SUCCESS`, and the CLI exits non-zero.

### 2.3 Design Principles

1. **No subprocess dependency** — the detector reads data already collected by the executor; it
   never spawns subprocesses.
2. **No LLM dependency** — all signals are deterministic; the detector is a pure Python function.
3. **Configurable thresholds** — all thresholds are declared as named constants; the module exposes
   a `SilentSuccessConfig` dataclass for per-deployment tuning.
4. **Override path** — a `--allow-silent-steps <step-id>` flag at the CLI level allows individual
   steps to be exempted (e.g., steps that legitimately produce no output in dry-run mode).
5. **Evidence-first output** — every failure includes the specific signal values that triggered it,
   not just a conclusion.

---

## 3. Signal Specification

### 3.1 Signal S1 — Artifact Content Validation

**What it measures**: After all steps complete, how many expected output artifacts exist, and do
they contain substantive content?

**Measurement method**: The executor already tracks `completed_steps` (the list of step IDs that
returned PASS, PASS_NO_SIGNAL, or PASS_NO_REPORT). For each completed step, the detector looks up
its expected output file from the step's `output_file` attribute and evaluates:

- `S1a` (existence): Does the file exist on disk?
- `S1b` (line count): Does the file meet the minimum line threshold for its step type?
- `S1c` (section count): Does the file contain at least the minimum number of `##` section headers
  for its step type (non-trivial structure, not just a YAML frontmatter block)?
- `S1d` (non-header content ratio): Of the file's lines, what fraction are non-blank, non-header
  content? A file that is 80% `##` headers with no body text fails this check.

**Per-step-type thresholds** (drawn from existing gate criteria in `cli_portify/gates.py`):

| Step ID | Min lines | Min `##` sections | Min non-header content ratio |
|---------|-----------|------------------|-----------------------------|
| `validate-config` | 0 (EXEMPT) | 0 | 0.0 |
| `discover-components` | 5 | 1 | 0.3 |
| `analyze-workflow` | 20 | 5 | 0.4 |
| `design-pipeline` (step-graph-design) | 30 | 3 | 0.4 |
| `models-gates-design` | 10 | 2 | 0.3 |
| `prompts-executor-design` | 10 | 2 | 0.3 |
| `pipeline-spec-assembly` | 20 | 3 | 0.4 |
| `synthesize-spec` | 20 | 3 | 0.5 |
| `brainstorm-gaps` | 10 | 2 | 0.3 |
| `panel-review` | 20 | 3 | 0.4 |

**Aggregate threshold**: For a 12-step pipeline to pass S1, at least 80% of non-EXEMPT steps must
have an artifact that passes all four sub-checks. A pipeline where 0 of 11 non-EXEMPT steps
produced qualifying artifacts scores 0.0 on S1 (maximum suspicion).

**Failure condition**: S1 score < 0.5 (fewer than half of expected artifacts pass content checks).

**Signal weight in composite**: 0.35 (highest weight — absence of artifacts is the most
unambiguous indicator of no-op execution).

**Legitimate edge cases**:
- Steps that correctly return PASS_NO_REPORT due to early exit (e.g., config validation failure)
  are excluded from the denominator if the pipeline itself exited non-SUCCESS.
- EXEMPT-tier steps are excluded from the denominator unconditionally.
- Steps that are SKIPPED due to `--resume` or `--dry-run` are excluded.

---

### 3.2 Signal S2 — Execution Trace Verification

**What it measures**: Did the steps do real work, as evidenced by time elapsed and subprocess
activity?

**Measurement method**: The executor's `_execute_step()` method is instrumented to record, per
step:

- `wall_clock_ms`: `time.monotonic()` delta from before `self._step_runner(step)` call to after
  return. This wraps the existing call; no behavioral change.
- `stdout_bytes`: `len(stdout.encode("utf-8"))` of the stdout string returned.
- `subprocess_spawned`: A boolean flag. If `step_runner` uses `subprocess.run()` or equivalent,
  the flag is set by the runner itself (via a convention: runners that do real work annotate their
  return tuple, or the detector checks `wall_clock_ms > SUBPROCESS_FLOOR_MS`).

These three values are stored in a `StepTrace` dataclass that is appended to
`PortifyExecutor._step_traces: list[StepTrace]` after each step.

**Per-step thresholds**:

| Signal | Suspicious threshold | Near-certain no-op threshold |
|--------|---------------------|------------------------------|
| `wall_clock_ms` | < 50ms for any non-EXEMPT step | < 10ms for any non-EXEMPT step |
| `stdout_bytes` | == 0 for a step type that normally produces output | == 0 for all steps combined |
| Combined: all steps < 50ms AND total stdout_bytes == 0 | Strong signal | Very strong signal |

**S2 score calculation**: Each non-EXEMPT, non-SKIPPED step contributes to S2:
- If `wall_clock_ms < 10`: counts as a "near-certain no-op step"
- If `wall_clock_ms` is between 10ms and 50ms AND `stdout_bytes == 0`: counts as "suspicious step"
- Otherwise: counts as "plausible real step"

`S2 = plausible_real_steps / total_evaluated_steps`

**Failure condition**: S2 score < 0.5 AND total `stdout_bytes` across all steps == 0.

**Signal weight in composite**: 0.35 (equal weight to S1 — time and output data are hard evidence).

**Legitimate edge cases**:
- Fast-failing steps (config validation that exits in 5ms with an error) produce `exit_code != 0`
  and are excluded because the pipeline outcome would be FAILURE, not SUCCESS.
- Dry-run mode (`--dry-run`) legitimately skips subprocess invocation for ANALYSIS and later
  phases. The detector is aware of dry-run mode and reduces its S2 threshold for dry-run runs
  (suspicion only if non-dry-run-eligible steps are also fast).
- Test harness injection: when `step_runner` is explicitly provided (test mode), S2 thresholds
  apply but can be overridden via `SilentSuccessConfig(s2_enabled=False)`.

**Instrumentation approach** — minimal executor change:

```python
# In _execute_step(), wrapping the existing call:
import time
t0 = time.monotonic()
if self._step_runner is not None:
    exit_code, stdout, timed_out = self._step_runner(step)
else:
    exit_code, stdout, timed_out = 0, "", False
wall_ms = (time.monotonic() - t0) * 1000

self._step_traces.append(StepTrace(
    step_id=step.step_id,
    wall_clock_ms=wall_ms,
    stdout_bytes=len(stdout.encode("utf-8")),
    exit_code=exit_code,
    timed_out=timed_out,
))
```

This is additive only. The existing call sites, status classifier, retry logic, and ledger
consumption are unchanged.

---

### 3.3 Signal S3 — Output Freshness Cross-Referencing

**What it measures**: If a step claims to have produced an output file, was the file actually
written during this pipeline run?

**Measurement method**: Before the pipeline begins, the detector snapshots:
- `pipeline_start_time`: `time.time()` (wall clock, not monotonic, so it can be compared to
  `os.path.getmtime()`).
- For each step's expected output file path: if the file already exists, record its
  `(mtime, size_bytes, content_hash_prefix)` in a `pre_run_snapshot: dict[Path, FileSnapshot]`.

After all steps complete, for each step that reported a PASS/PASS_NO_SIGNAL status, the detector
checks the step's output file:

- `S3a` (mtime freshness): `os.path.getmtime(output_file) >= pipeline_start_time - 1.0`
  (1-second tolerance for filesystem timestamp granularity). A file whose mtime predates the
  pipeline start was not written by this run.
- `S3b` (content change): If the file existed in the pre-run snapshot, its current content hash
  prefix must differ from the snapshot value. A file with identical content was not regenerated.
- `S3c` (size threshold): `os.path.getsize(output_file) >= MIN_SIZE_BYTES[step_type]`. Minimum
  sizes mirror the min-line thresholds from S1 (approximately 200 bytes for STANDARD steps,
  500 bytes for STRICT steps).

**S3 score calculation**:

`S3 = freshly_written_outputs / claimed_successful_steps`

where "freshly written" means the output file passes S3a AND (S3b if pre-existed) AND S3c.

**Failure condition**: S3 score < 0.5 AND at least 3 steps claimed PASS status.

**Signal weight in composite**: 0.30 (lower weight than S1/S2 because filesystem timestamp
precision can create false positives on very fast machines or NFS-mounted workdirs).

**Legitimate edge cases**:
- A step that reads an existing file and re-emits it unchanged (e.g., a passthrough copy step)
  legitimately fails S3b. These steps must be declared as `content_passthrough=True` in
  `STEP_REGISTRY` to be exempted from S3b.
- Clock skew on networked filesystems may cause `mtime < pipeline_start_time` even for freshly
  written files. The 1-second tolerance in S3a mitigates this; `SilentSuccessConfig` exposes
  `s3_mtime_tolerance_s` for environments requiring a larger window.
- Steps that write to a path that is a symlink to a pre-existing file: the detector resolves
  symlinks before comparing mtimes.

---

## 4. Composite Scoring Model

### 4.1 Formula

```
suspicion_score = (S1_raw * 0.35) + (S2_raw * 0.35) + (S3_raw * 0.30)
```

where each raw signal is inverted so that **higher suspicion_score = more evidence of no-op**:

```
S1_raw = 1.0 - S1_score      # S1_score=0 (no artifacts) → S1_raw=1.0 (max suspicion)
S2_raw = 1.0 - S2_score      # S2_score=0 (all near-instant) → S2_raw=1.0
S3_raw = 1.0 - S3_score      # S3_score=0 (no fresh outputs) → S3_raw=1.0
```

A perfectly legitimate run (all steps produce substantive artifacts, take measurable time, and
write fresh files) produces `suspicion_score ≈ 0.0`.

The cli-portify no-op run produces:
- `S1_score = 0.0` (no step artifacts exist → `S1_raw = 1.0`)
- `S2_score = 0.0` (all steps < 1ms, stdout_bytes = 0 → `S2_raw = 1.0`)
- `S3_score = 0.0` (no fresh output files → `S3_raw = 1.0`)
- `suspicion_score = (1.0 × 0.35) + (1.0 × 0.35) + (1.0 × 0.30) = 1.0`

### 4.2 Threshold and Gate Behavior

| suspicion_score | Action |
|-----------------|--------|
| 0.0 – 0.29 | Pass — no suspicious signals |
| 0.30 – 0.49 | Warn — log diagnostic, continue; outcome unchanged |
| 0.50 – 0.74 | Soft fail — outcome demoted to `SUSPICIOUS_SUCCESS`; CLI exits non-zero; override available |
| 0.75 – 1.00 | Hard fail — outcome set to `SILENT_SUCCESS_SUSPECTED`; pipeline blocked; no override at release tier |

Default blocking threshold: **0.50** (soft fail). Override behavior follows unified audit gating
v1.2.1 governance rules: task/milestone overrides are permitted with an `OverrideRecord`; release
overrides are forbidden.

### 4.3 Combination Rationale

Any individual signal may have legitimate explanations:

- Empty stdout alone: some steps write only to files, not stdout.
- Short elapsed time alone: a config validation step that finds a cached result may be fast.
- Stale output file alone: a step that decided its existing output was still valid may not rewrite.

But the combination of all three — no artifacts, sub-millisecond timing, no fresh files — has no
legitimate explanation for a 12-step pipeline claiming SUCCESS. The composite score formalizes this
reasoning: each signal independently contributes evidence, but the threshold is calibrated so that
a single weak signal does not trigger a failure.

### 4.4 Signal Independence

S1 and S3 are partially correlated (both measure output artifacts), but S1 measures content quality
while S3 measures freshness. A step that regenerates an artifact with identical content passes S1
but fails S3b. A step that creates a fresh one-line file fails S1b (below min lines) but passes
S3a. The signals are complementary rather than redundant.

S2 is independent of both S1 and S3: it measures execution process characteristics, not output
characteristics.

---

## 5. Implementation Plan

### 5.1 New Module: `cli_portify/silent_success.py`

A new module containing:

- `FileSnapshot(mtime: float, size_bytes: int, content_hash_prefix: str)` dataclass
- `StepTrace(step_id: str, wall_clock_ms: float, stdout_bytes: int, exit_code: int, timed_out: bool)` dataclass
- `SilentSuccessConfig` dataclass (all thresholds as named fields with defaults)
- `SilentSuccessDetector` class with:
  - `__init__(config: SilentSuccessConfig)`
  - `snapshot_pre_run(steps: list[PortifyStep], workdir: Path) -> None`
  - `evaluate(traces: list[StepTrace], completed_steps: list[str], pipeline_start_time: float, steps: list[PortifyStep]) -> SilentSuccessResult`
  - `_signal_s1(...)`, `_signal_s2(...)`, `_signal_s3(...)` private methods
- `SilentSuccessResult(suspicion_score: float, s1_score: float, s2_score: float, s3_score: float, diagnostics: list[str])` dataclass
- `SilentSuccessError(result: SilentSuccessResult)` exception

Estimated size: ~300 lines including docstrings and tests.

### 5.2 Executor Changes: `cli_portify/executor.py`

Three targeted changes, all additive:

**Change A** — Add `_step_traces: list[StepTrace]` to `PortifyExecutor.__init__()` and
`_step_traces = []` initialization. (2 lines)

**Change B** — Wrap the `_step_runner` call in `_execute_step()` with `time.monotonic()` and
append a `StepTrace` to `self._step_traces`. The no-op branch also gets wrapped, so a no-op
produces `StepTrace(wall_clock_ms < 1, stdout_bytes=0, ...)`. (8 lines)

**Change C** — In `run()`, before `_emit_return_contract()`, instantiate and call the detector:

```python
detector = SilentSuccessDetector(config=self._silent_success_config)
result = detector.evaluate(
    traces=self._step_traces,
    completed_steps=self._completed_steps,
    pipeline_start_time=self._pipeline_start_time,
    steps=self.steps,
)
if result.suspicion_score >= self._silent_success_config.hard_fail_threshold:
    outcome = PortifyOutcome.SILENT_SUCCESS_SUSPECTED
elif result.suspicion_score >= self._silent_success_config.soft_fail_threshold:
    outcome = PortifyOutcome.SUSPICIOUS_SUCCESS
```

**Change D** — Add `pipeline_start_time = time.time()` at the top of `run()` and
`detector.snapshot_pre_run(self.steps, self.workdir)` before the step loop. (4 lines)

Total executor changes: approximately 20 lines, all additive, no existing logic modified.

### 5.3 Model Changes: `cli_portify/models.py`

- Add `PortifyOutcome.SILENT_SUCCESS_SUSPECTED` and `PortifyOutcome.SUSPICIOUS_SUCCESS` enum values.
- Add `silent_success_config: SilentSuccessConfig` field to `PortifyExecutor.__init__()` signature
  with a default of `SilentSuccessConfig()` (uses default thresholds; not a breaking change).
- Add `_pipeline_start_time: float` field to `PortifyExecutor`.

### 5.4 Return Contract Changes

`return-contract.yaml` gains a new optional `silent_success_audit` block:

```yaml
silent_success_audit:
  suspicion_score: 1.0
  s1_artifact_coverage: 0.0
  s2_execution_activity: 0.0
  s3_output_freshness: 0.0
  diagnostics:
    - "0 of 11 non-EXEMPT steps produced qualifying artifacts"
    - "All 12 steps completed in < 1ms (total: 3ms wall clock)"
    - "0 fresh output files found after pipeline completion"
  gate_decision: SILENT_SUCCESS_SUSPECTED
```

This block is always written (even when `suspicion_score = 0.0`) so that legitimate runs can
confirm the detector ran and found no issues.

### 5.5 Test Changes: `tests/cli_portify/test_silent_success.py`

New test file covering:

- `test_no_op_pipeline_scores_1_0()` — feed the detector traces from a simulated no-op run; assert
  `suspicion_score == 1.0` and `gate_decision == SILENT_SUCCESS_SUSPECTED`.
- `test_real_pipeline_passes()` — feed traces from a simulated real run with artifacts, timing,
  and fresh files; assert `suspicion_score < 0.30`.
- `test_fast_exempt_step_not_penalized()` — validate-config EXEMPT step at 0ms does not affect score.
- `test_dry_run_reduces_s2_weight()` — dry-run mode with legitimately skipped steps does not
  trigger S2 failure.
- `test_single_signal_below_threshold()` — each signal alone at max suspicion does not reach the
  0.50 threshold.
- `test_override_permitted_at_task_scope()` — soft-fail outcome allows override at task scope.
- `test_override_blocked_at_release_scope()` — hard-fail outcome cannot be overridden at release.

Estimated: ~200 lines.

### 5.6 File Summary

| File | Change type | Estimated lines |
|------|-------------|----------------|
| `src/superclaude/cli/cli_portify/silent_success.py` | New | ~300 |
| `src/superclaude/cli/cli_portify/executor.py` | Additive (4 changes) | ~20 |
| `src/superclaude/cli/cli_portify/models.py` | Additive (new enums + field) | ~10 |
| `tests/cli_portify/test_silent_success.py` | New | ~200 |
| `src/superclaude/cli/cli_portify/gates.py` | No change | 0 |
| `src/superclaude/cli/pipeline/gates.py` | No change | 0 |

Total new/modified lines: approximately 530.

---

## 6. Acceptance Criteria

### 6.1 Would This Have Detected the No-Op Pipeline?

Yes, deterministically. The no-op pipeline produces the following signal values:

| Signal | Value in no-op run | Detection outcome |
|--------|--------------------|-------------------|
| S1 (artifact coverage) | 0 of 11 non-EXEMPT steps have artifacts | S1_score = 0.0 → S1_raw = 1.0 |
| S2 (execution activity) | All 12 steps complete in < 5ms total, stdout_bytes = 0 | S2_score = 0.0 → S2_raw = 1.0 |
| S3 (output freshness) | 0 fresh output files after pipeline completes | S3_score = 0.0 → S3_raw = 1.0 |
| Composite | (1.0 × 0.35) + (1.0 × 0.35) + (1.0 × 0.30) = **1.0** | Hard fail threshold (0.75) exceeded |

Pipeline outcome would be changed from `SUCCESS` to `SILENT_SUCCESS_SUSPECTED`. `return-contract.yaml`
would include the `silent_success_audit` block with all three signals at maximum suspicion. CLI
would exit non-zero. The forensic report's "Only `return-contract.yaml` produced; outcome: SUCCESS"
would instead be "outcome: SILENT_SUCCESS_SUSPECTED" with an actionable diagnostic.

### 6.2 Formal Acceptance Criteria

**AC-01**: When `PortifyExecutor` is constructed without `step_runner` (the no-op default), running
`executor.run()` against any non-trivial step list produces `suspicion_score >= 0.75` and outcome
`SILENT_SUCCESS_SUSPECTED`.

**AC-02**: When `PortifyExecutor` is constructed with a real `step_runner` that produces artifacts,
takes > 50ms per step, and writes fresh files, `suspicion_score <= 0.15`.

**AC-03**: The `return-contract.yaml` written by a no-op run includes the `silent_success_audit`
block with `gate_decision: SILENT_SUCCESS_SUSPECTED`.

**AC-04**: The CLI exits with a non-zero exit code when `suspicion_score >= soft_fail_threshold`.

**AC-05**: EXEMPT-tier steps (e.g., `validate-config`) do not contribute to any signal's
denominator.

**AC-06**: Steps SKIPPED due to `--resume` or `--dry-run` do not contribute to any signal's
denominator.

**AC-07**: A soft-fail (`suspicion_score` in 0.50–0.74) can be overridden with an `OverrideRecord`
at task and milestone scopes, but not at release scope.

**AC-08**: A hard-fail (`suspicion_score >= 0.75`) cannot be overridden at any scope at release
tier.

**AC-09**: All signal thresholds are declared as named constants in `SilentSuccessConfig`; no
threshold is a magic number in application code.

**AC-10**: The `test_no_op_pipeline_scores_1_0` test passes with the executor in its current
state (no `step_runner` provided), confirming the detector catches the existing bug.

---

## 7. Risk Assessment

### 7.1 False Positive Scenarios

**Risk R1: Fast config-validation step**

A `validate-config` step that finds the config invalid exits quickly with a non-zero code. This is
handled: `_determine_status()` returns `PortifyStatus.ERROR` for non-zero exit codes, which
terminates the pipeline with `PortifyOutcome.FAILURE`. The detector only runs when the pipeline
reaches `outcome=SUCCESS`, which never occurs after an ERROR status. **FP risk: zero.**

**Risk R2: Dry-run mode**

`--dry-run` legitimately prevents execution of SYNTHESIS and later phase types. These steps are
returned as SKIPPED by `_should_execute()`. The detector excludes SKIPPED steps from all signal
denominators. For the steps that do execute in dry-run (PREREQUISITES, ANALYSIS, USER_REVIEW), S2
thresholds are relaxed if `config.dry_run=True` in `SilentSuccessConfig`. **FP risk: low with
dry-run awareness.**

**Risk R3: New step types during scaffolding**

During active development, a developer may add a new step to `STEP_REGISTRY` before implementing
its runner. This is structurally identical to the no-op bug — which is the intended detection
target. If a developer wants to scaffold without implementing, they should use `--dry-run` or set
the step's phase_type to one filtered by dry-run, not rely on the no-op default. **FP risk:
intentional — this is a true positive for the bug class.**

**Risk R4: Content-passthrough steps**

A hypothetical step that reads an existing file and re-emits it unchanged fails S3b (content
unchanged). Mitigation: declare such steps as `content_passthrough=True` in `STEP_REGISTRY`; the
detector exempts them from S3b. As of the current codebase, no such steps exist. **FP risk: zero
for current codebase; manageable for future steps.**

**Risk R5: Clock skew on network filesystems**

NFS and some containerized filesystems have coarser mtime granularity (1-second resolution on some
NFS implementations). The S3a mtime check uses a 1-second tolerance (`mtime >= start_time - 1.0`)
to mitigate this. `SilentSuccessConfig.s3_mtime_tolerance_s` is exposed for environments needing
a larger tolerance. **FP risk: low; configurable.**

**Risk R6: Steps writing to symlinks or indirect paths**

If `step.output_file` resolves through a symlink to a pre-existing file on a different filesystem
partition, mtime comparison may be unreliable. The detector calls `Path.resolve()` before mtime
checks. **FP risk: low.**

**Risk R7: Test harness producing intentional empty output**

Unit tests that inject a mock `step_runner` returning `(0, "", False)` will trigger the detector
if they also check pipeline outcome. Tests must either:
(a) Use `SilentSuccessConfig(enabled=False)` to disable the detector in tests that are testing
executor logic independent of output quality, or
(b) Use a `step_runner` that produces realistic output and writes real artifact files.
Existing tests that use mocked steps will need to be updated to pass `silent_success_config` with
`enabled=False`, or updated to produce realistic step traces. **FP risk: moderate impact on test
suite; manageable with `enabled=False` flag.**

### 7.2 False Negative Scenarios

**Risk FN1: Partially-wired pipeline**

If 6 of 12 steps are wired and 6 are no-ops, the composite score might fall below the 0.50
threshold, depending on which steps are wired. Mitigation: the S1 failure condition requires at
least 50% of non-EXEMPT steps to produce qualifying artifacts. If the 6 wired steps include the
STRICT-tier steps (which have higher content thresholds), the score may still pass. This is an
acceptable partial detection — partial wiring is better than no wiring, and the remaining no-op
steps will fail their individual artifact gates (G-001 through G-011) when those gates are reached
by the portion of the pipeline that does produce output.

**Risk FN2: A no-op that happens to find pre-existing artifacts**

If a previous run produced all artifacts, and a subsequent no-op run finds them on disk with recent
mtimes, S3 might pass (files exist and are "fresh" relative to the previous run). S1 would still
check content, but the content from a previous real run would pass S1's checks. S2 (timing) would
still detect zero elapsed time. With S1_raw ≈ 0, S2_raw = 1.0, S3_raw ≈ 0: composite score ≈
(0 × 0.35) + (1.0 × 0.35) + (0 × 0.30) = 0.35, which falls in the warn range but below soft-fail.
Mitigation: the S3 pre-run snapshot includes content hashes; a no-op that finds pre-existing files
fails S3b (content unchanged = not regenerated). With S3b failure, S3_raw increases, pushing the
composite toward the soft-fail threshold. Full mitigation requires ensuring S3b comparison uses
content hashes from the *current* run start, not prior runs. **This is the most significant partial
detection gap.** It is addressed by ensuring the pre-run snapshot is always taken at the start of
each pipeline invocation.

---

## 8. Estimated Effort

### 8.1 Implementation

| Component | Effort |
|-----------|--------|
| `silent_success.py` — detector module | 2 days |
| `executor.py` — trace instrumentation (4 additive changes) | 0.5 days |
| `models.py` — new outcome enums + executor field | 0.5 days |
| Return contract schema extension | 0.5 days |
| Unit tests (`test_silent_success.py`) | 1.5 days |
| Integration with unified audit gating v1.2.1 `GateResult` schema | 1 day |
| Documentation updates | 0.5 days |
| **Total** | **6.5 days** |

### 8.2 Dependencies

This proposal has no dependencies on other proposals. It can be implemented independently and
deployed before Proposals 01, 02, 03, or 04.

It has a soft dependency on unified audit gating v1.2.1 Phase 1 (deterministic contracts +
evaluator) for the `GateResult` integration path. If v1.2.1 Phase 1 is not yet available,
`SilentSuccessResult` can be emitted as a standalone artifact in the `return-contract.yaml`
`silent_success_audit` block without requiring the full `GateResult` schema.

### 8.3 Scoring Framework Assessment

Using the standardized scoring framework from `proposals/scoring-framework.md`:

| Axis | Score | Evidence |
|------|-------|---------|
| Catch Rate (25%) | 10 | Deterministically catches the no-op: `suspicion_score = 1.0` |
| Generalizability (25%) | 7 | Catches any pipeline with silent-success anti-pattern; applies to sprint executor and any future pipeline using the same executor pattern; less applicable to static wiring bugs |
| Implementation Complexity (20%, inverted) | 6 | ~530 lines across 4 files; 2 new abstractions (`SilentSuccessDetector`, `StepTrace`); moderate test coverage required |
| False Positive Risk (15%, inverted) | 7 | Main FP risk is test harness impact (R7), mitigated by `enabled=False`; dry-run FP risk is low |
| Integration Fit (15%) | 8 | Integrates as a post-loop hook in `executor.run()`; no changes to gate infrastructure; reuses `GateResult` schema from v1.2.1 |

**Composite**: (10×0.25) + (7×0.25) + (6×0.20) + (7×0.15) + (8×0.15)
= 2.5 + 1.75 + 1.20 + 1.05 + 1.20 = **7.70**

This places Proposal 05 in **Tier 1 (Implement Immediately)** by the scoring framework's bands
(7.5–10 = high ROI, low risk, catches incident class).

### 8.4 Recommended Phasing

- **Phase 1 (immediate)**: Implement `silent_success.py`, executor instrumentation, and
  `test_no_op_pipeline_scores_1_0`. This alone would have blocked the no-op pipeline in any of the
  three v2.24–v2.25 releases.
- **Phase 2 (with v1.2.1 Phase 1)**: Integrate `SilentSuccessResult` into the `GateResult` schema
  so that silent success failures appear in the unified audit trail with `failure_class: policy`.
- **Phase 3 (with v1.2.1 rollout)**: Expose `suspicion_score` in the sprint TUI and `/sc:audit-gate`
  output so that operators can see the signal values before promoting a run.

---

## Appendix A: The No-Op Execution Path in Full

For completeness, the exact path through which the no-op produces `outcome: SUCCESS`:

1. `commands.py:run()` calls `run_portify(config)` without calling `validate_portify_config(config)` first.
2. `run_portify()` at `executor.py:1367` builds `steps` from `STEP_REGISTRY` metadata (step IDs, phase types, timeouts — no function references).
3. `PortifyExecutor` is constructed without `step_runner` (`step_runner=None` default at `executor.py:1395`).
4. `executor.run()` begins the step loop.
5. For each step, `_execute_step()` checks `self._step_runner is not None` → False → returns `(0, "", False)`.
6. `_determine_status(0, False, "", None)` sees: exit_code=0, not timed_out, no `EXIT_RECOMMENDATION_MARKER` in `""`, `artifact_path=None` so `artifact_exists=False` → returns `PortifyStatus.PASS_NO_REPORT`.
7. `PASS_NO_REPORT` is in the set `{PASS, PASS_NO_SIGNAL, PASS_NO_REPORT}` → step appended to `_completed_steps`.
8. No gate is invoked because artifact gates require an artifact file to exist.
9. Loop completes, `outcome = PortifyOutcome.SUCCESS`, `return-contract.yaml` is written.
10. CLI exits 0.

The proposed detector inserts at step 9: before writing the contract, it observes that 0 artifacts exist, all 12 steps completed in < 5ms total, and 0 fresh files were written, computes `suspicion_score = 1.0`, and changes `outcome` to `SILENT_SUCCESS_SUSPECTED` before the contract is emitted.

---

## Appendix B: Relationship to Other Proposals

| Proposal | Relationship |
|----------|-------------|
| 01 (Link 3: Tasklist→Code) | Complementary. Proposal 01 prevents no-op code from being approved at the task gate. Proposal 05 catches it if no-op code ships to a pipeline run. |
| 02 (Spec Fidelity Hardening) | Upstream. Proposal 02 prevents the roadmap from dropping the dispatch requirement. Proposal 05 catches the symptom if the requirement was dropped. |
| 03 (Code Integration Gate) | Complementary. Proposal 03 is a static analysis gate that detects `step_runner=None` in source code before any run. Proposal 05 is a runtime gate that detects no-op behavior during a run. Both are needed: Proposal 03 catches it pre-commit, Proposal 05 catches it if the static check was bypassed or not yet deployed. |
| 04 (Smoke Test Gate) | Complementary. Proposal 04 runs the pipeline against a test fixture. Proposal 05 runs as part of every production pipeline invocation. Proposal 04 catches the bug pre-release; Proposal 05 catches it in any run, including production. |
