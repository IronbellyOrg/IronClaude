

---
functional_requirements: 6
complexity_score: 0.45
complexity_class: moderate
---

## 1. Functional Requirements

1. **FR-EVAL-001.1 — Progress File Writer**: After each pipeline step completes (pass or fail), write a JSON entry to the progress file containing `step_id`, `status` (pass/fail/skip), `duration_ms`, `gate_verdict` (pass/fail/null), and `output_file`. File must be valid JSON after every write. Parallel steps (generate-A, generate-B) must produce independent entries with correct timing. File is created on first step completion.

2. **FR-EVAL-001.2 — CLI Option for Progress File**: Add `--progress-file` option to `superclaude roadmap run` accepting a file path. Default: `{output_dir}/progress.json`. Parent directory must be validated before pipeline starts. Existing file is overwritten, not appended.

3. **FR-EVAL-001.3 — Dry-Run Gate Summary**: When `--dry-run` is used, output a Markdown table with columns: Step, Gate Tier, Required Fields, Semantic Checks. All steps listed including conditional ones (remediate, certify). Conditional steps explicitly marked.

4. **FR-EVAL-001.4 — Deviation Analysis Sub-Reporting**: Capture each deviation analysis iteration within the spec-fidelity convergence loop as a sub-entry in the progress file. Record the convergence loop's pass count.

5. **FR-EVAL-001.5 — Remediation Trigger Reporting**: When remediation triggers due to findings in spec-fidelity, the progress entry must include `trigger_reason` and `finding_count`. Entry only written when remediation actually executes. Certification step entry must reference the remediation it validates.

6. **FR-EVAL-001.6 — Wiring Verification Integration**: Wiring step progress entry must include `unwired_count`, `orphan_count`, `blocking_count`, and `rollout_mode` from wiring gate configuration. Gate verdict must correctly reflect `WIRING_GATE` semantic check results.

### Implicit Functional Requirements

7. **Progress file uses atomic writes** (write-to-tmp + `os.replace()`) per Section 2.1 and NFR-EVAL-001.2.

8. **`PipelineProgress` data model**: Must track `spec_file`, `started_at` (ISO 8601), `steps` list, and `completed` boolean as defined in Section 4.5.

9. **`StepProgress` data model**: Must include `metadata` dict field for extensible per-step data (wiring counts, deviation iterations, remediation triggers).

10. **Gate constants must expose a `summary()` method** for dry-run reporting (Section 4.2).

11. **`--resume` must append to existing progress file** without overwriting prior entries (Section 8.2, `test_resume_preserves_progress`).

12. **Progress callback invoked sequentially** by `execute_pipeline()` even for parallel steps, preventing concurrent file corruption (Section 7, Risk table).

## 2. Non-Functional Requirements

1. **NFR-EVAL-001.1 — Write Latency**: Progress file write must complete in < 50ms per step. Measured via step duration delta with/without progress writing.

2. **NFR-EVAL-001.2 — Crash Safety**: Progress file must be valid JSON after any interruption. Achieved via atomic write (write-to-tmp + `os.replace()`).

3. **NFR-EVAL-001.3 — No Import Side Effects**: `progress.py` must produce zero I/O at import time. Verified by importing the module and checking no files are created.

4. **Backward Compatibility** (implicit): `summary()` on gate constants is additive; no signature changes to existing methods (Section 7).

5. **Single-File Output** (implicit from Section 2.1): Progress uses a single JSON file, not directory sprawl or multiple files.

## 3. Complexity Assessment

**Score: 0.45 — Moderate**

**Justification**:
- **Limited blast radius**: One new file (`progress.py`), three modified files. No changes to gate enforcement logic itself.
- **Straightforward integration pattern**: Post-step callback hook in an existing executor — no threading, no new async patterns.
- **Well-defined data model**: Two dataclasses with simple serialization.
- **Moderate complexity drivers**: Atomic file writes, parallel step timing correctness, deviation sub-entry nesting, and conditional step handling add non-trivial edge cases but are individually simple.
- **Single-sprint scope**: 5 implementation tasks + 3 test tasks + 1 doc task, with clear dependency ordering.

## 4. Key Architectural Constraints

1. **Hook mechanism must use existing `execute_pipeline()` callback** — no separate observer threads or file watchers.
2. **JSON format with atomic rewrite** — not JSONL, CSV, or YAML. Write-to-tmp + `os.replace()` pattern required.
3. **Sequential callback invocation** even for parallel steps — the executor serializes `on_step_complete` calls.
4. **Implementation order is constrained**: `progress.py` models first → CLI option and gate summary in parallel → executor wiring → dry-run enrichment → deviation sub-reporting.
5. **No modifications to `pipeline/gates.py` enforcement code** — out of scope.
6. **Dry-run gate summary must be inline Markdown table** — consistent with existing dry-run output format.
7. **Module dependency direction**: `commands.py → executor.py → progress.py → models.py/gates.py`. No circular dependencies.

## 5. Open Questions and Ambiguities

1. **BLOCKING — Deviation sub-entry schema undefined (GAP-002)**: FR-EVAL-001.4 requires sub-entries for deviation analysis iterations but specifies no schema. How do these nest inside `progress.json`? Are they children of the spec-fidelity `StepProgress` entry (via `metadata` dict)? A separate list field? This blocks data model validation.

2. **WARNING — "Significant findings" threshold undefined (GAP-003)**: FR-EVAL-001.5 uses "significant findings" as the remediation trigger, but the spec-fidelity gate uses "HIGH severity findings." The term "significant" is ambiguous — does it mean HIGH only, or HIGH + MEDIUM? This prevents deterministic acceptance criteria verification.

3. **`--resume` behavior underspecified**: The test plan (Section 8.2) states `--resume` should append to existing progress, but FR-EVAL-001.2 states existing files are overwritten. These contradict. Resolution needed: does `--resume` get special handling to preserve prior entries while a fresh run overwrites?

4. **Progress file rotation/size limits absent (GAP-001)**: No specification for what happens if progress files grow large across many runs. Acknowledged as low severity.

5. **Section 4.3 missing**: The spec jumps from 4.2 to 4.4 in the Architecture section. Minor structural gap — no content appears lost.

6. **`metadata` dict usage unspecified**: The `StepProgress.metadata` field is defined but no requirements specify which steps populate it or with what keys. FR-EVAL-001.5 implies `trigger_reason`/`finding_count` go somewhere, and FR-EVAL-001.6 implies `unwired_count`/`orphan_count`/`blocking_count`/`rollout_mode` go somewhere — presumably in `metadata`, but this is not stated.

7. **Certification step "references" remediation**: FR-EVAL-001.5 says the certification entry must "reference" the remediation it validates, but no field or mechanism for this reference is defined.
