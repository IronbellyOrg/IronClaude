# Phase 3 -- Execution Engine and Reporter

**Phase Goal:** Build the per-eval lifecycle, parallel orchestrator, and report writer with strict N'-vs-K contract enforcement. RunOrchestrator runs a 3-eval suite in parallel, Reporter emits summary.{md,json} with `len(outcomes) == counts.expanded_n_prime` invariant enforced, SIGINT cancels in-flight evals and writes a partial report, and exit-code semantics pass.

### T03.01 -- Add DM-001 EvalOutcome frozen dataclass

| Field | Value |
|---|---|
| Roadmap Item IDs | R-045 |
| Why | DM-001 is the per-eval outcome record emitted by EvalRunner with fields covering status (PASS/FAIL/ERRORED/TIMEOUT/INTERRUPTED/SKIPPED/XFAIL/XPASS), duration, expects, skip metadata, artifacts, and error_class. |
| Effort | M |
| Risk | Low |
| Risk Drivers | None |
| Tier | STANDARD |
| Confidence | [████████--] 80% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0045 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0045/spec.md`
- `TASKLIST_ROOT/artifacts/D-0045/notes.md`
- `TASKLIST_ROOT/artifacts/D-0045/evidence.md`

**Deliverables:**
- `EvalOutcome` frozen dataclass in `src/superclaude/cli/eval/models.py` with all 9 fields from DM-001.

**Steps:**
1. **[PLANNING]** Read DM-001 fields; identify status Literal set.
2. **[PLANNING]** Confirm ExpectResult (T01.15) is importable for `expects` field.
3. **[EXECUTION]** Add `EvalOutcome` frozen dataclass with the 9 fields and Literal status.
4. **[EXECUTION]** Implement `to_dict()` and validation for status membership.
5. **[VERIFICATION]** Run `uv run pytest tests/cli/eval/test_eval_outcome.py -v`.
6. **[COMPLETION]** Save evidence under `TASKLIST_ROOT/evidence/T03.01/`.

**Acceptance Criteria:**
- Class `EvalOutcome` in `src/superclaude/cli/eval/models.py` is frozen and exposes the 9 fields named in DM-001.
- Invalid status raises `ValueError`; valid statuses are exactly the 8 listed in DM-001.
- `to_dict()` produces deterministic JSON-serializable output.
- `TASKLIST_ROOT/artifacts/D-0045/spec.md` records the field contract.

**Validation:**
- Manual check: build an EvalOutcome with status `PASS` and one with invalid status; confirm second raises.
- Evidence: linkable artifact produced (spec/test log/screenshot/doc).

**Dependencies:** T01.15
**Rollback:** TBD (if not specified in roadmap)
**Notes:** Consumed by COMP-008 Reporter (T03.13) and RunOrchestrator (T03.15).

### T03.02 -- Add DM-003 EvalResult dataclass

| Field | Value |
|---|---|
| Roadmap Item IDs | R-046 |
| Why | DM-003 carries per-eval result data consumed by reporter: eval_id, outcome, start, end, duration_sec, stdout, stderr, artifacts, optional error. |
| Effort | S |
| Risk | Low |
| Risk Drivers | None |
| Tier | STANDARD |
| Confidence | [████████--] 80% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0046 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0046/spec.md`
- `TASKLIST_ROOT/artifacts/D-0046/notes.md`
- `TASKLIST_ROOT/artifacts/D-0046/evidence.md`

**Deliverables:**
- `EvalResult` dataclass in `src/superclaude/cli/eval/models.py` with the 9 fields from DM-003.

**Steps:**
1. **[PLANNING]** Confirm `EvalOutcome` (T03.01) interface.
2. **[PLANNING]** Choose datetime representation (ISO 8601 strings).
3. **[EXECUTION]** Add `EvalResult` dataclass with the 9 DM-003 fields.
4. **[EXECUTION]** Implement `to_dict()` for serialization.
5. **[VERIFICATION]** Run `uv run pytest tests/cli/eval/test_eval_result.py -v`.
6. **[COMPLETION]** Save evidence under `TASKLIST_ROOT/evidence/T03.02/`.

**Acceptance Criteria:**
- Class `EvalResult` exposes fields `eval_id,outcome,start,end,duration_sec,stdout,stderr,artifacts,error`.
- `EvalResult.to_dict()` returns a JSON-serializable mapping deterministically.
- `duration_sec` is computed from `end - start` consistently.
- `TASKLIST_ROOT/artifacts/D-0046/spec.md` records the contract.

**Validation:**
- Manual check: build EvalResult with start/end and confirm duration computation.
- Evidence: linkable artifact produced (spec/test log/screenshot/doc).

**Dependencies:** T03.01
**Rollback:** TBD (if not specified in roadmap)
**Notes:** EvalResult is the reporter's primary input; EvalOutcome is the runner emission.

### T03.03 -- Add DM-010 EvalContext runtime record

| Field | Value |
|---|---|
| Roadmap Item IDs | R-047 |
| Why | DM-010 is the runtime context passed to every ExpectCallable: eval_spec, home, home_path, artifacts_dir, run_dir, env, stdout/stderr paths, transcript path, jsonl paths, exit_code, stdout, stderr, duration_sec, artifacts. |
| Effort | M |
| Risk | Low |
| Risk Drivers | None |
| Tier | STANDARD |
| Confidence | [████████--] 80% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0047 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0047/spec.md`
- `TASKLIST_ROOT/artifacts/D-0047/notes.md`
- `TASKLIST_ROOT/artifacts/D-0047/evidence.md`

**Deliverables:**
- `EvalContext` dataclass (immutable view) in `src/superclaude/cli/eval/models.py` with the 15 fields from DM-010.

**Steps:**
1. **[PLANNING]** Confirm HomeIsolation (T02.11) provides home/home_path and EvalSpec (T01.03) is available.
2. **[PLANNING]** Decide on immutability strategy (frozen dataclass).
3. **[EXECUTION]** Add `EvalContext` frozen dataclass with the 14 DM-010 fields.
4. **[EXECUTION]** Provide factory `from_runner_state(...)` building EvalContext from runner internals.
5. **[VERIFICATION]** Run `uv run pytest tests/cli/eval/test_eval_context.py -v`.
6. **[COMPLETION]** Save evidence under `TASKLIST_ROOT/evidence/T03.03/`.

**Acceptance Criteria:**
- Class `EvalContext` is frozen and exposes the 15 fields named in DM-010.
- `EvalContext` instances reject mutation (FrozenInstanceError on attempted set).
- `from_runner_state()` constructs an EvalContext from EvalSpec + HomeIsolation + run outputs deterministically.
- `TASKLIST_ROOT/artifacts/D-0047/spec.md` records the contract.

**Validation:**
- Manual check: build an EvalContext via factory and assert immutability.
- Evidence: linkable artifact produced (spec/test log/screenshot/doc).

**Dependencies:** T01.03, T02.04, T02.11
**Rollback:** TBD (if not specified in roadmap)
**Notes:** ExpectCallable signature is `(ctx: EvalContext) -> ExpectResult`.

### T03.04 -- Define FR-LC1 EvalRunner lifecycle spec

| Field | Value |
|---|---|
| Roadmap Item IDs | R-048 |
| Why | FR-LC1 defines the lifecycle: build isolation -> deploy hooks -> spawn -> inject -> observe -> assert -> teardown. ERRORED on harness exception; PASS only when all Expects pass. |
| Effort | L |
| Risk | Medium |
| Risk Drivers | None |
| Tier | STANDARD |
| Confidence | [████████--] 85% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | None | Preferred: Sequential, Context7 |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0048 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0048/spec.md`
- `TASKLIST_ROOT/artifacts/D-0048/notes.md`
- `TASKLIST_ROOT/artifacts/D-0048/evidence.md`

**Deliverables:**
- Lifecycle spec doc + skeleton implementation in `src/superclaude/cli/eval/runner.py` defining the FR-LC1 sequence and status mapping rules.

**Steps:**
1. **[PLANNING]** Confirm HomeIsolation (T02.11), hook adapter (T02.14), PtyDriver (T02.16), ClaudeProcessAdapter (T02.19) interfaces.
2. **[PLANNING]** Define exception->status mapping (harness exception -> ERRORED; assertion fail -> FAIL).
3. **[EXECUTION]** Author `run_eval(spec) -> EvalOutcome` skeleton executing the 7-step sequence.
4. **[EXECUTION]** Add teardown honoring `keep` flag from atomic setup.
5. **[VERIFICATION]** Run `uv run pytest tests/cli/eval/test_eval_lifecycle.py -v`.
6. **[COMPLETION]** Save evidence under `TASKLIST_ROOT/evidence/T03.04/`.

**Acceptance Criteria:**
- Function `run_eval(spec)` in `src/superclaude/cli/eval/runner.py` executes the 7-step lifecycle and returns an `EvalOutcome`.
- Harness exceptions during the lifecycle produce status `ERRORED`; assertion failures produce status `FAIL`.
- `PASS` only emitted when all Expects pass.
- `TASKLIST_ROOT/artifacts/D-0048/spec.md` documents the lifecycle and status mapping.

**Validation:**
- Manual check: run `run_eval` against a one-eval stub and inspect emitted EvalOutcome.
- Evidence: linkable artifact produced (spec/test log/screenshot/doc).

**Dependencies:** T02.11, T02.14, T02.16, T02.19, T03.01
**Rollback:** TBD (if not specified in roadmap)
**Notes:** COMP-004 (T03.05) wraps this into a class for parallel orchestration.

### T03.05 -- Implement COMP-004 EvalRunner class

| Field | Value |
|---|---|
| Roadmap Item IDs | R-049 |
| Why | COMP-004 wraps FR-LC1 in a full EvalRunner class: emits EvalOutcome, logs to per-eval JSONL, respects per-eval timeout. |
| Effort | L |
| Risk | Medium |
| Risk Drivers | None |
| Tier | STANDARD |
| Confidence | [████████--] 80% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | None | Preferred: Sequential, Context7 |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0049 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0049/spec.md`
- `TASKLIST_ROOT/artifacts/D-0049/notes.md`
- `TASKLIST_ROOT/artifacts/D-0049/evidence.md`

**Deliverables:**
- `EvalRunner` class in `src/superclaude/cli/eval/runner.py` exposing `run(spec) -> EvalOutcome` plus per-eval JSONL logging.

**Steps:**
1. **[PLANNING]** Confirm FR-LC1 (T03.04) skeleton is landed.
2. **[PLANNING]** Define per-eval JSONL path under `home_path/.eval-logs/`.
3. **[EXECUTION]** Implement `EvalRunner.run(spec)` class method wrapping `run_eval`.
4. **[EXECUTION]** Log structured lifecycle events to per-eval JSONL with deterministic format.
5. **[VERIFICATION]** Run `uv run pytest tests/cli/eval/test_runner_class.py -v`.
6. **[COMPLETION]** Save evidence under `TASKLIST_ROOT/evidence/T03.05/`.

**Acceptance Criteria:**
- Class `EvalRunner` in `src/superclaude/cli/eval/runner.py` exposes `run(spec) -> EvalOutcome`.
- Per-eval JSONL log file is written under `home_path/.eval-logs/` with at least the events `setup_started`, `spawn_started`, `assertion_started`, `teardown_started`.
- Per-eval timeout is honored: tasks exceeding `EvalSpec.timeout_sec` return outcome with status `TIMEOUT`.
- `TASKLIST_ROOT/artifacts/D-0049/spec.md` documents the class and logging contract.

**Validation:**
- Manual check: run EvalRunner against a 2-step fixture eval and inspect the JSONL log.
- Evidence: linkable artifact produced (spec/test log/screenshot/doc).

**Dependencies:** T03.04
**Rollback:** TBD (if not specified in roadmap)
**Notes:** Per-eval JSONL becomes input for Expect.jsonl primitive (T04.03).

### T03.06 -- Checkpoint: Phase 3 / Tasks T03.01-T03.05

| Field | Value |
|---|---|
| Roadmap Item IDs | R-045,R-046,R-047,R-048,R-049 |
| Why | Gate: verify EvalOutcome, EvalResult, EvalContext, FR-LC1 lifecycle, and EvalRunner class before signal handling and reporter wiring land. |
| Effort | XS |
| Risk | Low |
| Risk Drivers | None |
| Tier | LIGHT |
| Confidence | [██████████] 100% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Quick sanity check |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-CP03-MID-T01-T05 |

**Checkpoint Report Path:** `TASKLIST_ROOT/checkpoints/CP-P03-T01-T05.md`

**Purpose:** Confirm runtime models + lifecycle + runner class before signal/timeout + reporter land.

**Verification:**
- `EvalOutcome`, `EvalResult`, `EvalContext` dataclasses constructable; serialization deterministic.
- `EvalRunner.run(spec)` executes the FR-LC1 lifecycle and emits an EvalOutcome.
- Per-eval JSONL log contains lifecycle events.

**Exit Criteria:**
- `uv run pytest tests/cli/eval/test_eval_outcome.py tests/cli/eval/test_eval_result.py tests/cli/eval/test_eval_context.py tests/cli/eval/test_eval_lifecycle.py tests/cli/eval/test_runner_class.py -v` exits 0.
- Per-eval JSONL log file format documented in T03.05 spec.
- Checkpoint report `CP-P03-T01-T05.md` records pass/fail per upstream task.

**Steps:**
1. **[VERIFICATION]** Confirm each artifact listed in Verification is present.
2. **[VERIFICATION]** Re-run the tier-proportional checks for the covered tasks.
3. **[VERIFICATION]** Write the checkpoint report to the Checkpoint Report Path above.

**Acceptance Criteria:**
- File `TASKLIST_ROOT/checkpoints/CP-P03-T01-T05.md` exists and contains `status: PASS`.
- All 3 Verification bullets are confirmed.
- All 3 Exit Criteria bullets are met.
- Checkpoint report includes the task IDs it covers (T03.01-T03.05).

**Validation:**
- Manual check: reviewer confirms the report at the Checkpoint Report Path.
- Evidence: the generated checkpoint markdown file.

**Dependencies:** T03.01..T03.05
**Rollback:** N/A (checkpoints are read-only verifications)

### T03.07 -- Implement NFR-REL1 signal handling and per-eval timeout enforcement

| Field | Value |
|---|---|
| Roadmap Item IDs | R-050 |
| Why | NFR-REL1 requires SIGINT/SIGTERM cancel in-flight evals (mark INTERRUPTED), write partial summary, exit 3; per-eval timeout kills PtyDriver, reaps zombies, marks TIMEOUT. |
| Effort | M |
| Risk | Medium |
| Risk Drivers | None |
| Tier | STANDARD |
| Confidence | [████████--] 80% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | None | Preferred: Sequential, Context7 |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0050 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0050/spec.md`
- `TASKLIST_ROOT/artifacts/D-0050/notes.md`
- `TASKLIST_ROOT/artifacts/D-0050/evidence.md`

**Deliverables:**
- Signal handler in `src/superclaude/cli/eval/signal_handler.py` binding SIGINT/SIGTERM; per-eval timeout enforcement inside `EvalRunner.run()`.

**Steps:**
1. **[PLANNING]** Confirm EvalRunner (T03.05) and PtyDriver (T02.16) interfaces.
2. **[PLANNING]** Design cooperative cancellation flag for in-flight evals.
3. **[EXECUTION]** Install signal handlers binding SIGINT/SIGTERM to set the cancellation flag.
4. **[EXECUTION]** Wire per-eval timeout via `signal.alarm` or async timeout; kill PtyDriver + reap zombie on expiry.
5. **[VERIFICATION]** Run `uv run pytest tests/cli/eval/test_signal_handling.py -v`.
6. **[COMPLETION]** Save evidence under `TASKLIST_ROOT/evidence/T03.07/`.

**Acceptance Criteria:**
- Sending SIGINT during a parallel run marks in-flight evals as `INTERRUPTED` and writes a partial summary file; process exits 3.
- A per-eval timeout kills the PtyDriver subprocess and reaps the zombie; outcome status is `TIMEOUT`.
- No zombie processes remain after a timeout (verified by `ps` snapshot fixture).
- `TASKLIST_ROOT/artifacts/D-0050/spec.md` documents the signal + timeout contract.

**Validation:**
- Manual check: run a 3-eval suite, send SIGINT mid-run, inspect partial summary and exit 3.
- Evidence: linkable artifact produced (spec/test log/screenshot/doc).

**Dependencies:** T02.16, T03.05
**Rollback:** TBD (if not specified in roadmap)
**Notes:** Exit-code semantics aligned with TEST-008 (T04.19).

### T03.08 -- Implement NFR-REL2 bounded retry policy

| Field | Value |
|---|---|
| Roadmap Item IDs | R-051 |
| Why | NFR-REL2 disables retries by default; `--eval` subset re-run path documented; OQ-10 retry semantics gated to MCP-flaky tag only. |
| Effort | S |
| Risk | Low |
| Risk Drivers | None |
| Tier | STANDARD |
| Confidence | [████████--] 85% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0051 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0051/spec.md`
- `TASKLIST_ROOT/artifacts/D-0051/notes.md`
- `TASKLIST_ROOT/artifacts/D-0051/evidence.md`

**Deliverables:**
- Default `retry_count=0` policy enforced in EvalRunner; documentation of `--eval` subset re-run path.

**Steps:**
1. **[PLANNING]** Confirm EvalRunner (T03.05) and OQ-10 resolution status.
2. **[PLANNING]** Define MCP-flaky tag detection rule for future R3-mit (T05.23).
3. **[EXECUTION]** Set default retry_count=0 in EvalRunner; expose `--eval` subset path in docs.
4. **[EXECUTION]** Add an explicit `MCP_FLAKY_TAG` constant for future retry-once logic.
5. **[VERIFICATION]** Run `uv run pytest tests/cli/eval/test_retry_policy.py -v`.
6. **[COMPLETION]** Save evidence under `TASKLIST_ROOT/evidence/T03.08/`.

**Acceptance Criteria:**
- EvalRunner default `retry_count=0`; verified by a test that monkeypatches EvalRunner and confirms no retries occur on failure.
- `--eval <id>` subset re-run path is documented in `docs/eval/retry.md`.
- `MCP_FLAKY_TAG` constant is defined for use by R3-mit (T05.23).
- `TASKLIST_ROOT/artifacts/D-0051/spec.md` records the retry policy.

**Validation:**
- Manual check: induce a fail in a fixture eval, run twice via `--eval`, confirm independent results.
- Evidence: linkable artifact produced (spec/test log/screenshot/doc).

**Dependencies:** T03.05
**Rollback:** TBD (if not specified in roadmap)
**Notes:** OQ-10 retry semantics resolve empirically in M3/M5 per debate convergence.

### T03.09 -- Add DM-004 RunSummary aggregate dataclass

| Field | Value |
|---|---|
| Roadmap Item IDs | R-052 |
| Why | DM-004 holds aggregate run summary: run_id, started_at, finished_at, duration_sec, suite, manifest_version, parallel, counts, totals, evals[], artifacts. |
| Effort | M |
| Risk | Low |
| Risk Drivers | None |
| Tier | STANDARD |
| Confidence | [████████--] 80% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0052 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0052/spec.md`
- `TASKLIST_ROOT/artifacts/D-0052/notes.md`
- `TASKLIST_ROOT/artifacts/D-0052/evidence.md`

**Deliverables:**
- `RunSummary` dataclass in `src/superclaude/cli/eval/models.py` with the 11 fields from DM-004 and `to_dict()`.

**Steps:**
1. **[PLANNING]** Confirm EvalOutcome/EvalResult (T03.01/T03.02) interfaces.
2. **[PLANNING]** Define counts sub-structure (manifest_n, expanded_n_prime, kept_k, skipped_s, kept_plus_skipped_equals_n_prime).
3. **[EXECUTION]** Add `RunSummary` dataclass with the 11 DM-004 fields including nested counts dict.
4. **[EXECUTION]** Implement `to_dict()` for serialization.
5. **[VERIFICATION]** Run `uv run pytest tests/cli/eval/test_run_summary.py -v`.
6. **[COMPLETION]** Save evidence under `TASKLIST_ROOT/evidence/T03.09/`.

**Acceptance Criteria:**
- Class `RunSummary` exposes the 11 fields listed in DM-004 with nested `counts` containing the 5 sub-fields.
- `to_dict()` returns a deterministic JSON-serializable mapping.
- `RunSummary` constructor validates `counts.kept_plus_skipped_equals_n_prime` boolean and asserts the equation holds.
- `TASKLIST_ROOT/artifacts/D-0052/spec.md` records the contract.

**Validation:**
- Manual check: build a RunSummary with mismatched counts and confirm the equation assertion fires.
- Evidence: linkable artifact produced (spec/test log/screenshot/doc).

**Dependencies:** T03.01, T03.02
**Rollback:** TBD (if not specified in roadmap)
**Notes:** Counts subfields are central to FR-RPT1 invariant (T03.11).

### T03.10 -- Define DM-012 summary.json schema

| Field | Value |
|---|---|
| Roadmap Item IDs | R-053 |
| Why | DM-012 is the canonical machine-readable summary schema covering run_id, counts, totals, evals[] required for downstream consumption. |
| Effort | M |
| Risk | Low |
| Risk Drivers | None |
| Tier | STANDARD |
| Confidence | [████████--] 80% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0053 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0053/spec.md`
- `TASKLIST_ROOT/artifacts/D-0053/notes.md`
- `TASKLIST_ROOT/artifacts/D-0053/evidence.md`

**Deliverables:**
- `summary.schema.json` under `src/superclaude/cli/eval/schemas/` defining the canonical summary contract.

**Steps:**
1. **[PLANNING]** Confirm DM-004 RunSummary (T03.09) fields.
2. **[PLANNING]** Decide on JSON-schema version (Draft 2020-12).
3. **[EXECUTION]** Author `summary.schema.json` with the 9 top-level fields and required `counts` + `totals` shape.
4. **[EXECUTION]** Add fixtures: schema-valid and schema-invalid summary files.
5. **[VERIFICATION]** Run `uv run pytest tests/cli/eval/test_summary_schema.py -v`.
6. **[COMPLETION]** Save evidence under `TASKLIST_ROOT/evidence/T03.10/`.

**Acceptance Criteria:**
- File `src/superclaude/cli/eval/schemas/summary.schema.json` exists and validates the reference RunSummary serialization.
- Required fields enumerated: `run_id,started_at,duration_sec,suite,manifest_version,parallel,counts,totals,evals`.
- `counts` requires the 5 sub-fields from DM-012; `totals` requires `passed,failed,skipped,errored,interrupted,timeout`.
- `TASKLIST_ROOT/artifacts/D-0053/spec.md` records the schema contract.

**Validation:**
- Manual check: validate a reference summary.json against the schema using `jsonschema`.
- Evidence: linkable artifact produced (spec/test log/screenshot/doc).

**Dependencies:** T03.09
**Rollback:** TBD (if not specified in roadmap)
**Notes:** Schema fidelity tested by TEST-007 (T04.17).

### T03.11 -- Implement FR-RPT1 aggregated run report (N'-vs-K invariant)

| Field | Value |
|---|---|
| Roadmap Item IDs | R-054 |
| Why | FR-RPT1 emits summary.md, summary.json, optional junit.xml with strict `len(evals[]) == counts.expanded_n_prime` invariant; mismatch raises ReporterContractViolation exit 2. |
| Effort | L |
| Risk | Medium |
| Risk Drivers | None |
| Tier | STANDARD |
| Confidence | [████████--] 85% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | None | Preferred: Sequential, Context7 |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0054 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0054/spec.md`
- `TASKLIST_ROOT/artifacts/D-0054/notes.md`
- `TASKLIST_ROOT/artifacts/D-0054/evidence.md`

**Deliverables:**
- Aggregated run report module emitting summary.md, summary.json, optional junit.xml with the N'-vs-K invariant guard.

**Steps:**
1. **[PLANNING]** Confirm DM-012 schema (T03.10) and RunSummary (T03.09) interfaces.
2. **[PLANNING]** Define `ReporterContractViolation` exception class.
3. **[EXECUTION]** Implement `write_aggregated_report(summary, output_dir)` emitting all three artifacts.
4. **[EXECUTION]** Wire the N'-vs-K guard: raise `ReporterContractViolation` (exit 2) when `len(evals[]) != counts.expanded_n_prime`.
5. **[VERIFICATION]** Run `uv run pytest tests/cli/eval/test_run_report.py -v`.
6. **[COMPLETION]** Save evidence under `TASKLIST_ROOT/evidence/T03.11/`.

**Acceptance Criteria:**
- Function `write_aggregated_report(summary, output_dir)` writes `summary.md`, `summary.json`, and (when enabled) `junit.xml` under `output_dir`.
- A summary with mismatched N'-vs-K raises `ReporterContractViolation` and process exits 2.
- SKIPPED rows are included in `evals[]` with `skip_reason` populated.
- `TASKLIST_ROOT/artifacts/D-0054/spec.md` documents the invariant guard.

**Validation:**
- Manual check: build a RunSummary with len(evals)=4 and expanded_n_prime=5; confirm exit 2.
- Evidence: linkable artifact produced (spec/test log/screenshot/doc).

**Dependencies:** T03.09, T03.10
**Rollback:** TBD (if not specified in roadmap)
**Notes:** N'-vs-K is the canonical reporter contract; mismatch is always a contract bug.

### T03.12 -- Checkpoint: Phase 3 / Tasks T03.07-T03.11

| Field | Value |
|---|---|
| Roadmap Item IDs | R-050,R-051,R-052,R-053,R-054 |
| Why | Gate: verify signal handling, retry policy, RunSummary, summary.json schema, and FR-RPT1 invariant before Reporter and Orchestrator land. |
| Effort | XS |
| Risk | Low |
| Risk Drivers | None |
| Tier | LIGHT |
| Confidence | [██████████] 100% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Quick sanity check |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-CP03-MID-T07-T11 |

**Checkpoint Report Path:** `TASKLIST_ROOT/checkpoints/CP-P03-T07-T11.md`

**Purpose:** Confirm signal/timeout + retry policy + RunSummary + schema + FR-RPT1 invariant before Reporter and Orchestrator land.

**Verification:**
- SIGINT during a 3-eval run marks in-flight as INTERRUPTED and exits 3.
- `write_aggregated_report` raises `ReporterContractViolation` on N'-vs-K mismatch.
- `summary.schema.json` validates a reference RunSummary serialization.

**Exit Criteria:**
- `uv run pytest tests/cli/eval/test_signal_handling.py tests/cli/eval/test_retry_policy.py tests/cli/eval/test_run_summary.py tests/cli/eval/test_summary_schema.py tests/cli/eval/test_run_report.py -v` exits 0.
- No zombie processes remain after a fixture timeout.
- Checkpoint report `CP-P03-T07-T11.md` records pass/fail per upstream task.

**Steps:**
1. **[VERIFICATION]** Confirm each artifact listed in Verification is present.
2. **[VERIFICATION]** Re-run the tier-proportional checks for the covered tasks.
3. **[VERIFICATION]** Write the checkpoint report to the Checkpoint Report Path above.

**Acceptance Criteria:**
- File `TASKLIST_ROOT/checkpoints/CP-P03-T07-T11.md` exists and contains `status: PASS`.
- All 3 Verification bullets are confirmed.
- All 3 Exit Criteria bullets are met.
- Checkpoint report includes the task IDs it covers (T03.07-T03.11).

**Validation:**
- Manual check: reviewer confirms the report at the Checkpoint Report Path.
- Evidence: the generated checkpoint markdown file.

**Dependencies:** T03.07..T03.11
**Rollback:** N/A (checkpoints are read-only verifications)

### T03.13 -- Implement COMP-008 Reporter / AggregatedRunReport methods

| Field | Value |
|---|---|
| Roadmap Item IDs | R-055 |
| Why | COMP-008 implements the 4 emitter methods (to_markdown, to_yaml, to_json, to_junit) and wires the N'-vs-K assertion guard; pattern reference `cli/sprint/executor.py:190-335`. |
| Effort | L |
| Risk | Medium |
| Risk Drivers | None |
| Tier | STANDARD |
| Confidence | [████████--] 85% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | None | Preferred: Sequential, Context7 |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0055 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0055/spec.md`
- `TASKLIST_ROOT/artifacts/D-0055/notes.md`
- `TASKLIST_ROOT/artifacts/D-0055/evidence.md`

**Deliverables:**
- `Reporter` (a.k.a. `AggregatedRunReport`) class in `src/superclaude/cli/eval/reporter.py` exposing `to_markdown`, `to_yaml`, `to_json`, `to_junit`.

**Steps:**
1. **[PLANNING]** Confirm FR-RPT1 (T03.11) and DM-012 (T03.10) artifacts.
2. **[PLANNING]** Read pattern reference `cli/sprint/executor.py:190-335` for shape.
3. **[EXECUTION]** Implement `Reporter` class with the 4 emitter methods.
4. **[EXECUTION]** Wire assertion guard inside each emitter so contract violation exits 2.
5. **[VERIFICATION]** Run `uv run pytest tests/cli/eval/test_reporter.py -v`.
6. **[COMPLETION]** Save evidence under `TASKLIST_ROOT/evidence/T03.13/`.

**Acceptance Criteria:**
- Class `Reporter` exposes `to_markdown()`,`to_yaml()`,`to_json()`,`to_junit()` and the assertion guard fires before any emitter writes output on mismatch.
- All 4 emitter outputs are byte-stable for a given RunSummary input (verified by hashing).
- JUnit XML emitter is feature-gated and only emitted when explicitly requested.
- `TASKLIST_ROOT/artifacts/D-0055/spec.md` documents the emitter contract.

**Validation:**
- Manual check: emit all 4 reports from a fixture RunSummary and diff against snapshot.
- Evidence: linkable artifact produced (spec/test log/screenshot/doc).

**Dependencies:** T03.10, T03.11, T03.14
**Rollback:** TBD (if not specified in roadmap)
**Notes:** Pattern reference `cli/sprint/executor.py:190-335` is read-only. Dep on T03.14 (COMP-015) follows roadmap COMP-008 deps `FR-RPT1, COMP-015`.

### T03.14 -- Pin AggregatedPhaseReport pattern probe (COMP-015)

| Field | Value |
|---|---|
| Roadmap Item IDs | R-056 |
| Why | COMP-015 smoke test pins shape reference for `AggregatedRunReport`; fails on upstream refactor of `cli/sprint/executor.py:190-335`. |
| Effort | S |
| Risk | Low |
| Risk Drivers | None |
| Tier | STANDARD |
| Confidence | [████████--] 85% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0056 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0056/spec.md`
- `TASKLIST_ROOT/artifacts/D-0056/notes.md`
- `TASKLIST_ROOT/artifacts/D-0056/evidence.md`

**Deliverables:**
- Probe test `tests/cli/eval/test_phase_report_probe.py` pinning the AggregatedPhaseReport surface used as a shape reference.

**Steps:**
1. **[PLANNING]** Inspect `cli/sprint/executor.py:190-335` to identify AggregatedPhaseReport surface.
2. **[PLANNING]** Decide which symbols to pin (class name, method names, expected fields).
3. **[EXECUTION]** Author probe test using `inspect` to confirm symbol shape.
4. **[EXECUTION]** Add docstring linking failure to upstream refactor.
5. **[VERIFICATION]** Run `uv run pytest tests/cli/eval/test_phase_report_probe.py -v` against current tree.
6. **[COMPLETION]** Save evidence under `TASKLIST_ROOT/evidence/T03.14/`.

**Acceptance Criteria:**
- File `tests/cli/eval/test_phase_report_probe.py` asserts the AggregatedPhaseReport class name and method names exist at `cli/sprint/executor.py:190-335`.
- Test fails when a synthetic method name change is applied.
- Test is read-only (no AggregatedPhaseReport instances constructed).
- `TASKLIST_ROOT/artifacts/D-0056/spec.md` records the pinned surface.

**Validation:**
- Manual check: temporarily rename a method in the source and confirm probe fails.
- Evidence: linkable artifact produced (spec/test log/screenshot/doc).

**Dependencies:** None
**Rollback:** TBD (if not specified in roadmap)
**Notes:** Sibling to COMP-012 (T02.05); both pin upstream shapes read-only.

### T03.15 -- Implement COMP-003 RunOrchestrator with ThreadPoolExecutor + as_completed

| Field | Value |
|---|---|
| Roadmap Item IDs | R-057 |
| Why | COMP-003 schedules evals via ThreadPoolExecutor + as_completed (AC6 pattern); max_workers=8 default clamped to [1,15]; per-eval timeout enforced; emits EvalOutcome per expanded spec. |
| Effort | L |
| Risk | Medium |
| Risk Drivers | scope (concurrency) |
| Tier | STANDARD |
| Confidence | [████████--] 85% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | None | Preferred: Sequential, Context7 |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0057 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0057/spec.md`
- `TASKLIST_ROOT/artifacts/D-0057/notes.md`
- `TASKLIST_ROOT/artifacts/D-0057/evidence.md`

**Deliverables:**
- `RunOrchestrator` class in `src/superclaude/cli/eval/orchestrator.py` scheduling EvalRunners via `ThreadPoolExecutor + as_completed`.

**Steps:**
1. **[PLANNING]** Confirm EvalRunner (T03.05), signal handler (T03.07), and reference pattern `cli/prd/executor.py:774-802`.
2. **[PLANNING]** Define max_workers clamp [1,15] with default 8.
3. **[EXECUTION]** Implement `RunOrchestrator.run(specs, parallel)` using ThreadPoolExecutor + as_completed.
4. **[EXECUTION]** Wire per-eval timeout and signal handler cancellation flag.
5. **[VERIFICATION]** Run `uv run pytest tests/cli/eval/test_orchestrator.py -v`.
6. **[COMPLETION]** Save evidence under `TASKLIST_ROOT/evidence/T03.15/`.

**Acceptance Criteria:**
- Class `RunOrchestrator` exposes `run(specs, parallel)` and emits one EvalOutcome per expanded spec.
- `parallel=20` clamps to 15; `parallel < 1` is rejected per clamp range `[1,15]`.
- A 3-eval suite runs in parallel and completes faster than 3x the slowest-eval duration.
- `TASKLIST_ROOT/artifacts/D-0057/spec.md` documents the scheduler contract.

**Validation:**
- Manual check: run a 3-eval suite at `--parallel 3` and measure wall-clock vs sequential.
- Evidence: linkable artifact produced (spec/test log/screenshot/doc).

**Dependencies:** T03.05, T03.07
**Rollback:** TBD (if not specified in roadmap)
**Notes:** Honors AC6 pattern; no asyncio.

### T03.16 -- Integration test: parallel execution of 15 evals (FR-G2)

| Field | Value |
|---|---|
| Roadmap Item IDs | R-058 |
| Why | FR-G2 runs 15 evals in parallel with concurrency=8 default; integration test asserts strict isolation (own HOME, session_id, telemetry namespace) and max=15 clamp enforced. |
| Effort | L |
| Risk | Medium |
| Risk Drivers | scope (concurrency) |
| Tier | STANDARD |
| Confidence | [████████--] 85% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | None | Preferred: Sequential, Context7 |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0058 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0058/spec.md`
- `TASKLIST_ROOT/artifacts/D-0058/notes.md`
- `TASKLIST_ROOT/artifacts/D-0058/evidence.md`

**Deliverables:**
- Integration test `tests/cli/eval/test_parallel_15.py` running 15 evals at `--parallel 8` and confirming clamp + isolation.

**Steps:**
1. **[PLANNING]** Confirm RunOrchestrator (T03.15) and HomeIsolation (T02.11) are landed.
2. **[PLANNING]** Build 15-eval fixture suite using fast stub commands.
3. **[EXECUTION]** Author `tests/cli/eval/test_parallel_15.py` exercising the orchestrator at parallel 8.
4. **[EXECUTION]** Add an assertion that `parallel=16` clamps to 15.
5. **[VERIFICATION]** Run `uv run pytest tests/cli/eval/test_parallel_15.py -v`.
6. **[COMPLETION]** Save evidence under `TASKLIST_ROOT/evidence/T03.16/`.

**Acceptance Criteria:**
- File `tests/cli/eval/test_parallel_15.py` runs a 15-eval fixture suite at `--parallel 8` and exits 0.
- Each eval receives its own HOME, session_id, and telemetry namespace (verified by per-eval JSONL inspection).
- `parallel=16` clamps to 15; recorded in test assertions.
- `TASKLIST_ROOT/artifacts/D-0058/spec.md` documents the integration scenario.

**Validation:**
- Manual check: run the 15-eval integration test and inspect per-eval JSONL directories.
- Evidence: linkable artifact produced (spec/test log/screenshot/doc).

**Dependencies:** T02.11, T03.15
**Rollback:** TBD (if not specified in roadmap)
**Notes:** Anchors the AC5 isolation guarantee for high-concurrency runs.

### T03.17 -- Verify NFR-PERF2 concurrency resource bounds (RAM ceiling + free-RAM precheck)

| Field | Value |
|---|---|
| Roadmap Item IDs | R-059 |
| Why | NFR-PERF2 documents <=2.25 GB resident at `--parallel 15`; doctor warns when free RAM < 2.25 GB before accepting --parallel 15. |
| Effort | S |
| Risk | Low |
| Risk Drivers | None |
| Tier | STANDARD |
| Confidence | [████████--] 80% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0059 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0059/spec.md`
- `TASKLIST_ROOT/artifacts/D-0059/notes.md`
- `TASKLIST_ROOT/artifacts/D-0059/evidence.md`

**Deliverables:**
- Benchmark + doctor precheck recording `<=2.25 GB resident at --parallel 15` and warning when free RAM is insufficient.

**Steps:**
1. **[PLANNING]** Confirm FR-G2 integration test (T03.16) is available.
2. **[PLANNING]** Identify free-RAM query approach (e.g., `psutil.virtual_memory()`).
3. **[EXECUTION]** Add benchmark capturing RSS at peak parallel run; record in `PROVENANCE/perf-notes`.
4. **[EXECUTION]** Wire doctor precheck warning when free RAM <2.25 GB before accepting --parallel 15.
5. **[VERIFICATION]** Run `uv run pytest tests/cli/eval/test_perf_resource_bounds.py -v`.
6. **[COMPLETION]** Save evidence under `TASKLIST_ROOT/evidence/T03.17/`.

**Acceptance Criteria:**
- Benchmark confirms peak RSS <=2.25 GB at `--parallel 15` on the dev host (or xfail with documented host limitation).
- Doctor emits a warning string containing `2.25 GB` when free RAM is insufficient and `--parallel 15` is requested.
- Benchmark report is saved to `TASKLIST_ROOT/evidence/T03.17/perf-ram.json`.
- `TASKLIST_ROOT/artifacts/D-0059/spec.md` documents the ceiling and precheck.

**Validation:**
- Manual check: run the benchmark and inspect peak RSS.
- Evidence: linkable artifact produced (spec/test log/screenshot/doc).

**Dependencies:** T03.16
**Rollback:** TBD (if not specified in roadmap)
**Notes:** Hosts with <4 GB free RAM are out-of-scope per infrastructure requirements.

### T03.18 -- Checkpoint: Phase 3 / Tasks T03.13-T03.17

| Field | Value |
|---|---|
| Roadmap Item IDs | R-055,R-056,R-057,R-058,R-059 |
| Why | Gate: verify Reporter, AggregatedPhaseReport probe, RunOrchestrator, FR-G2 parallel-15, and resource-bound benchmark before disk-budget poller and PTY lifecycle tests close M3. |
| Effort | XS |
| Risk | Low |
| Risk Drivers | None |
| Tier | LIGHT |
| Confidence | [██████████] 100% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Quick sanity check |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-CP03-MID-T13-T17 |

**Checkpoint Report Path:** `TASKLIST_ROOT/checkpoints/CP-P03-T13-T17.md`

**Purpose:** Confirm Reporter + orchestrator + FR-G2 parallel-15 + resource bounds before disk-budget poller + PTY lifecycle tests close M3.

**Verification:**
- `Reporter.to_markdown/yaml/json/junit` produce byte-stable output and trigger contract guard on mismatch.
- 15-eval parallel run at `--parallel 8` exits 0 with isolated per-eval HOMEs.
- Peak RSS at `--parallel 15` is recorded and <=2.25 GB.

**Exit Criteria:**
- `uv run pytest tests/cli/eval/test_reporter.py tests/cli/eval/test_phase_report_probe.py tests/cli/eval/test_orchestrator.py tests/cli/eval/test_parallel_15.py tests/cli/eval/test_perf_resource_bounds.py -v` exits 0.
- Benchmark report `perf-ram.json` exists.
- Checkpoint report `CP-P03-T13-T17.md` records pass/fail per upstream task.

**Steps:**
1. **[VERIFICATION]** Confirm each artifact listed in Verification is present.
2. **[VERIFICATION]** Re-run the tier-proportional checks for the covered tasks.
3. **[VERIFICATION]** Write the checkpoint report to the Checkpoint Report Path above.

**Acceptance Criteria:**
- File `TASKLIST_ROOT/checkpoints/CP-P03-T13-T17.md` exists and contains `status: PASS`.
- All 3 Verification bullets are confirmed.
- All 3 Exit Criteria bullets are met.
- Checkpoint report includes the task IDs it covers (T03.13-T03.17).

**Validation:**
- Manual check: reviewer confirms the report at the Checkpoint Report Path.
- Evidence: the generated checkpoint markdown file.

**Dependencies:** T03.13..T03.17
**Rollback:** N/A (checkpoints are read-only verifications)

### T03.19 -- Enforce disk budget via NFR-PERF4 poller (--max-disk-mb)

| Field | Value |
|---|---|
| Roadmap Item IDs | R-060 |
| Why | NFR-PERF4 polls disk every 5s with default 1024 MB budget; on breach in-flight evals complete, no new evals scheduled, exit 2 with `disk_budget_exceeded` artifact. |
| Effort | M |
| Risk | Low |
| Risk Drivers | None |
| Tier | STANDARD |
| Confidence | [████████--] 85% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0060 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0060/spec.md`
- `TASKLIST_ROOT/artifacts/D-0060/notes.md`
- `TASKLIST_ROOT/artifacts/D-0060/evidence.md`

**Deliverables:**
- Disk-budget poller integrated into RunOrchestrator with 5s tick, configurable via `--max-disk-mb`, default 1024 MB.

**Steps:**
1. **[PLANNING]** Confirm RunOrchestrator (T03.15) interface and signal handler (T03.07).
2. **[PLANNING]** Identify disk-usage measurement scope (per-run output dir).
3. **[EXECUTION]** Add background poller thread ticking every 5s, summing run-dir disk usage.
4. **[EXECUTION]** On breach: stop scheduling, allow in-flight to finish, exit 2 with `disk_budget_exceeded` artifact.
5. **[VERIFICATION]** Run `uv run pytest tests/cli/eval/test_disk_budget.py -v`.
6. **[COMPLETION]** Save evidence under `TASKLIST_ROOT/evidence/T03.19/`.

**Acceptance Criteria:**
- RunOrchestrator polls disk usage every 5s when `--max-disk-mb` is set (default 1024 MB).
- A test that fills the run dir past 1024 MB triggers `disk_budget_exceeded` artifact and exit 2; in-flight evals complete, new evals are not scheduled.
- When `--max-disk-mb 0` is set, the poller is disabled and no breach is ever signaled (verified by a fixture that fills the run dir past 2 GB and asserts the run completes without interruption).
- `TASKLIST_ROOT/artifacts/D-0060/spec.md` documents the poller cadence and breach semantics.

**Validation:**
- Manual check: run with `--max-disk-mb 1` and a fixture that writes >1 MB; confirm exit 2.
- Evidence: linkable artifact produced (spec/test log/screenshot/doc).

**Dependencies:** T03.15
**Rollback:** TBD (if not specified in roadmap)
**Notes:** `--max-disk-mb 0` disables the budget per roadmap AC.

### T03.20 -- Assert no shared mutable state at concurrency (NFR-ISO1)

| Field | Value |
|---|---|
| Roadmap Item IDs | R-061 |
| Why | NFR-ISO1 ensures no shared HOMEs, no shared file handles (e.g., `auggie-first.jsonl`), and no port collisions at `--parallel 15`. Tests run N×15 trials. |
| Effort | M |
| Risk | Medium |
| Risk Drivers | scope (concurrency) |
| Tier | STANDARD |
| Confidence | [████████--] 80% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0061 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0061/spec.md`
- `TASKLIST_ROOT/artifacts/D-0061/notes.md`
- `TASKLIST_ROOT/artifacts/D-0061/evidence.md`

**Deliverables:**
- Integration test `tests/cli/eval/test_no_shared_state.py` running N×15 trials and asserting no shared state across concurrent evals.

**Steps:**
1. **[PLANNING]** Confirm FR-G2 integration (T03.16) is available.
2. **[PLANNING]** Design assertions: each eval's HOME, session_id, telemetry path are unique.
3. **[EXECUTION]** Author integration test running 3 trials of 15-eval parallel runs.
4. **[EXECUTION]** Assert HOME paths are pairwise distinct, session_ids unique, JSONL paths unique.
5. **[VERIFICATION]** Run `uv run pytest tests/cli/eval/test_no_shared_state.py -v`.
6. **[COMPLETION]** Save evidence under `TASKLIST_ROOT/evidence/T03.20/`.

**Acceptance Criteria:**
- File `tests/cli/eval/test_no_shared_state.py` runs 3 trials of 15-eval parallel runs and exits 0.
- Across all trials, per-eval HOME paths, session_ids, and JSONL paths are pairwise distinct.
- No port-collision errors are recorded.
- `TASKLIST_ROOT/artifacts/D-0061/spec.md` documents the no-shared-state contract.

**Validation:**
- Manual check: run the integration test and inspect per-trial uniqueness assertions.
- Evidence: linkable artifact produced (spec/test log/screenshot/doc).

**Dependencies:** T03.16
**Rollback:** TBD (if not specified in roadmap)
**Notes:** N×15 trials catch low-probability race conditions.

### T03.21 -- Track NFR-PERF3 full-suite runtime trend

| Field | Value |
|---|---|
| Roadmap Item IDs | R-062 |
| Why | NFR-PERF3 records baseline full-suite duration and budget <10 min documented; `--eval` subset path documented. |
| Effort | S |
| Risk | Low |
| Risk Drivers | None |
| Tier | STANDARD |
| Confidence | [████████--] 80% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0062 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0062/spec.md`
- `TASKLIST_ROOT/artifacts/D-0062/notes.md`
- `TASKLIST_ROOT/artifacts/D-0062/evidence.md`

**Deliverables:**
- Baseline runtime artifact `TASKLIST_ROOT/evidence/T03.21/suite-runtime.json` recording full-suite duration_sec; docs entry for `--eval` subset path.

**Steps:**
1. **[PLANNING]** Confirm RunOrchestrator (T03.15) records duration in RunSummary.
2. **[PLANNING]** Define baseline scenario (15-eval suite at parallel 8).
3. **[EXECUTION]** Run the baseline and capture `duration_sec` from summary.json to `suite-runtime.json`.
4. **[EXECUTION]** Document `--eval` subset re-run path in `docs/eval/runtime.md`.
5. **[VERIFICATION]** Inspect `suite-runtime.json` and assert duration <600 (10 min).
6. **[COMPLETION]** Save evidence under `TASKLIST_ROOT/evidence/T03.21/`.

**Acceptance Criteria:**
- File `TASKLIST_ROOT/evidence/T03.21/suite-runtime.json` exists and records `duration_sec` for a 15-eval baseline at parallel 8.
- `docs/eval/runtime.md` documents the `--eval` subset re-run path.
- Baseline duration <600 seconds (or test marked xfail with host limitation).
- `TASKLIST_ROOT/artifacts/D-0062/spec.md` documents the baseline budget.

**Validation:**
- Manual check: run the baseline scenario and confirm output.
- Evidence: linkable artifact produced (spec/test log/screenshot/doc).

**Dependencies:** T03.15
**Rollback:** TBD (if not specified in roadmap)
**Notes:** Adoption budget per R6 mitigation.

### T03.22 -- TEST-006 PTY lifecycle integration tests (FR-G1 enforcement)

| Field | Value |
|---|---|
| Roadmap Item IDs | R-063 |
| Why | TEST-006 asserts real `claude` binary spawned via pexpect (FR-G1); prompt readiness observed; input injected; transcript exists; timeout reaps child; ban-import lint rule rejects `anthropic` SDK imports. |
| Effort | L |
| Risk | Low |
| Risk Drivers | None |
| Tier | STANDARD |
| Confidence | [████████--] 85% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | None | Preferred: Sequential, Context7 |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0063 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0063/spec.md`
- `TASKLIST_ROOT/artifacts/D-0063/notes.md`
- `TASKLIST_ROOT/artifacts/D-0063/evidence.md`

**Deliverables:**
- Integration test `tests/cli/eval/test_pty_lifecycle.py` covering real claude spawn, prompt readiness, input injection, timeout reaping, transcript existence, and ban-import lint check.

**Steps:**
1. **[PLANNING]** Confirm PtyDriver (T02.16), PtyStream (T02.17), ClaudeProcessAdapter (T02.19), and EvalRunner (T03.05) are landed.
2. **[PLANNING]** Build a single-eval fixture that drives claude via PTY end-to-end.
3. **[EXECUTION]** Author `tests/cli/eval/test_pty_lifecycle.py` running the fixture.
4. **[EXECUTION]** Configure `tool.ruff.lint.flake8-tidy-imports.banned-api` in `pyproject.toml` (per COMP-013) to reject `anthropic` imports under `src/superclaude/cli/eval/`; inject a synthetic `import anthropic` in a fixture and confirm `ruff check` exits non-zero.
5. **[VERIFICATION]** Run `uv run pytest tests/cli/eval/test_pty_lifecycle.py tests/cli/eval/test_ban_import_rule.py -v && uv run ruff check src/superclaude/cli/eval/`.
6. **[COMPLETION]** Save evidence under `TASKLIST_ROOT/evidence/T03.22/`.

**Acceptance Criteria:**
- File `tests/cli/eval/test_pty_lifecycle.py` runs a single-eval fixture spawning the real claude binary via PTY and exits 0.
- Test asserts: prompt readiness observed, input injected, transcript file written, timeout reaps the child.
- `uv run ruff check src/superclaude/cli/eval/` exits 0 on the clean tree AND exits non-zero when a synthetic `import anthropic` is injected (verified by test in `tests/cli/eval/test_ban_import_rule.py`); `tool.ruff.lint.flake8-tidy-imports.banned-api` declares the rule per COMP-013.
- `TASKLIST_ROOT/artifacts/D-0063/spec.md` documents the lifecycle test matrix and the ban-import rule configuration.

**Validation:**
- Manual check: run the lifecycle test and inspect the captured transcript file.
- Evidence: linkable artifact produced (spec/test log/screenshot/doc).

**Dependencies:** T02.16, T02.17, T02.19, T03.05
**Rollback:** TBD (if not specified in roadmap)
**Notes:** First-class FR-G1 enforcement test for the harness.

### T03.23 -- Checkpoint: End of Phase 3

| Field | Value |
|---|---|
| Roadmap Item IDs | R-045..R-063 |
| Why | M3 exit gate: RunOrchestrator runs a 3-eval suite in parallel, Reporter emits summary.md/json with N'-vs-K invariant enforced, SIGINT cancels in-flight evals and writes partial report, exit-code semantics pass. |
| Effort | XS |
| Risk | Low |
| Risk Drivers | None |
| Tier | LIGHT |
| Confidence | [██████████] 100% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Quick sanity check |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-CP03 |

**Checkpoint Report Path:** `TASKLIST_ROOT/checkpoints/CP-P03-END.md`

**Purpose:** M3 exit gate: execution engine + reporter + concurrency + disk-budget + PTY lifecycle tests verified.

**Verification:**
- `RunOrchestrator` completes 3-eval suite in parallel and emits expected EvalOutcomes.
- `Reporter` emits `summary.md/json` with N'-vs-K invariant enforced; SIGINT exits 3 with partial summary.
- `tests/cli/eval/test_pty_lifecycle.py` passes (FR-G1 enforced via real claude spawn).

**Exit Criteria:**
- `uv run pytest tests/cli/eval/ -v` passes for M3 modules.
- `uv run ruff check src/superclaude/cli/eval/` exits 0.
- Checkpoint report `CP-P03-END.md` records pass/fail per task in Phase 3.

**Steps:**
1. **[VERIFICATION]** Confirm each artifact listed in Verification is present.
2. **[VERIFICATION]** Re-run the tier-proportional checks for the covered tasks.
3. **[VERIFICATION]** Write the checkpoint report to the Checkpoint Report Path above.

**Acceptance Criteria:**
- File `TASKLIST_ROOT/checkpoints/CP-P03-END.md` exists and contains `status: PASS`.
- All 3 Verification bullets are confirmed.
- All 3 Exit Criteria bullets are met.
- Checkpoint report includes the task IDs it covers (T03.01-T03.22).

**Validation:**
- Manual check: reviewer confirms the report at the Checkpoint Report Path.
- Evidence: the generated checkpoint markdown file.

**Dependencies:** T03.01..T03.22
**Rollback:** N/A (checkpoints are read-only verifications)
