

---
functional_requirements: 6
complexity_score: 0.45
complexity_class: moderate
---

## 1. Functional Requirements

1. **FR-EVAL-001.1 — Progress File Writer**: After each pipeline step completes (pass or fail), write a JSON entry to the progress file containing `step_id`, `status` (pass/fail/skip), `duration_ms`, `gate_verdict` (pass/fail/null), and `output_file`. File must be valid JSON after every write. Parallel steps (generate-A, generate-B) must produce independent entries with correct timing. File is created on first step completion.

2. **FR-EVAL-001.2 — CLI Option for Progress File**: Add `--progress-file` option to `superclaude roadmap run` accepting a file path. Default: `{output_dir}/progress.json`. Parent directory must be validated before pipeline starts. Existing file is overwritten, not appended.

3. **FR-EVAL-001.3 — Dry-Run Gate Summary**: When `--dry-run` is used, output a Markdown table with columns: Step, Gate Tier, Required Fields, Semantic Checks. All steps including conditional ones (remediate, certify) must be listed. Conditional steps must be explicitly marked.

4. **FR-EVAL-001.4 — Deviation Analysis Sub-Reporting**: Capture each deviation analysis iteration from the spec-fidelity convergence loop as a sub-entry in the progress file. Record the convergence loop's pass count.

5. **FR-EVAL-001.5 — Remediation Trigger Reporting**: When remediation is triggered by "significant findings" in spec-fidelity, the progress entry for the remediate step must include `trigger_reason` and `finding_count`. Entry only written when remediation actually executes. Certification step entry must reference the remediation it validates.

6. **FR-EVAL-001.6 — Wiring Verification Integration**: Wiring step progress entry must include `unwired_count`, `orphan_count`, `blocking_count`, and `rollout_mode` from wiring gate configuration. Gate verdict must correctly reflect `WIRING_GATE` semantic check results.

### Implicit Functional Requirements

7. **Atomic File Writes**: Progress file must use write-to-tmp + `os.replace()` pattern for crash-safe writes (derived from Section 2.1 and NFR-EVAL-001.2).

8. **StepProgress Data Model**: Implement `StepProgress` dataclass with fields: `step_id`, `status`, `duration_ms`, `gate_verdict`, `output_file`, `metadata` (dict). Implement `PipelineProgress` dataclass with fields: `spec_file`, `started_at` (ISO 8601), `steps` (list), `completed` (bool).

9. **Gate Summary Method**: Add `summary()` method to gate constants in `gates.py` for dry-run reporting.

10. **Post-Step Callback Integration**: Wire progress reporter into `execute_pipeline()` callback mechanism, invoked sequentially even for parallel steps.

11. **Resume Behavior**: `--resume` must append to existing progress file without overwriting prior entries (from test plan Section 8.2).

## 2. Non-Functional Requirements

1. **NFR-EVAL-001.1 — Write Latency**: Progress file write latency must be < 50ms per step. Measured via step duration delta with/without progress reporting.

2. **NFR-EVAL-001.2 — Crash Safety**: Progress file must survive pipeline crash. Atomic writes via write-to-tmp + `os.replace()`. File must be valid JSON after any interruption.

3. **NFR-EVAL-001.3 — No Import Side Effects**: `progress.py` must have zero I/O at import time. Verified by importing the module and checking no files are created.

4. **Backward Compatibility** (implicit): `summary()` on gate constants is additive; no signature changes to existing methods (from Risk Assessment).

5. **Sequential Callback Safety** (implicit): `on_step_complete` callback is invoked sequentially by `execute_pipeline()` even for parallel steps, preventing concurrent file corruption.

## 3. Complexity Assessment

**Score: 0.45 — Moderate**

**Justification**:
- **Single new file** (`progress.py`) plus modifications to 3 existing files — limited blast radius.
- **No threading or concurrency concerns** — callback is sequential by design.
- **Well-defined data models** — straightforward dataclass serialization.
- **Moderate integration surface** — hooks into executor callback, CLI options, gate constants, convergence loop, and wiring gate (5 touch points).
- **Two intentional ambiguities** elevate complexity slightly: deviation sub-entry schema is undefined, and remediation trigger threshold is vague.
- **Implementation is linear** with one parallel step opportunity (CLI option + gate summary method).

## 4. Key Architectural Constraints

1. **Hook mechanism must use existing post-step callback** in `execute_pipeline()` — no observer threads or file watchers.
2. **Progress format is wrapped JSON** (not JSONL, CSV, or YAML) — atomic rewrite on every step completion.
3. **Single new file only** — `src/superclaude/cli/roadmap/progress.py`. No new directories or modules.
4. **No modifications to gate validation logic** — `pipeline/gates.py` enforcement code is out of scope.
5. **No real-time streaming** (WebSocket/SSE) — file-based only.
6. **Dependency graph**: `commands.py → executor.py → progress.py → models.py, gates.py`; `executor.py → audit/wiring_gate.py`.
7. **Implementation order is partially sequential**: progress.py (step 1) → CLI + gates in parallel (step 2) → executor wiring (step 3) → dry-run enrichment (step 4) → deviation sub-reporting (step 5).

## 5. Open Questions and Ambiguities

1. **BLOCKING — Deviation sub-entry schema undefined (GAP-002)**: FR-EVAL-001.4 requires sub-entries for deviation analysis iterations but specifies no schema. How do these nest inside `PipelineProgress`? Are they child entries in `StepProgress.metadata`, a nested list, or separate `StepProgress` entries with a parent reference? The `StepProgress` data model has a generic `metadata: dict` field that could hold them, but no contract is defined.

2. **WARNING — "Significant findings" threshold undefined (GAP-003)**: FR-EVAL-001.5 uses "significant findings" as the remediation trigger, but the workflow diagram (Section 2.2) specifies "spec-fidelity FAIL with HIGH findings." These may not be equivalent. What severity level(s) constitute "significant"? Is it only HIGH, or does it include MEDIUM?

3. **Resume vs. overwrite conflict**: FR-EVAL-001.2 states "if progress file already exists, it is overwritten." However, test plan Section 8.2 includes `test_resume_preserves_progress` which expects `--resume` to append to existing progress. The spec does not define how `--resume` and `--progress-file` interact — does `--resume` override the overwrite behavior?

4. **Progress file rotation/size limits absent (GAP-001)**: No specification for what happens if the progress file grows large over repeated runs. Acknowledged as low severity.

5. **Section 4.3 missing**: Architecture section jumps from 4.2 to 4.4 — either a numbering error or omitted content (e.g., a constants/config section).

6. **Completed flag semantics**: `PipelineProgress.completed` is a boolean but no requirement specifies when it is set to `True` — after the last step? After certification? Only on success? What value does it hold if the pipeline crashes mid-run?

7. **Metadata field usage**: `StepProgress.metadata` is a generic dict. FR-EVAL-001.5 requires `trigger_reason` and `finding_count`; FR-EVAL-001.6 requires `unwired_count`, `orphan_count`, `blocking_count`, `rollout_mode`. Are these top-level fields on `StepProgress` or keys within `metadata`? The data model suggests `metadata`, but the acceptance criteria list them as direct entry fields.
