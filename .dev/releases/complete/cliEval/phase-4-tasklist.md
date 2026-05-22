# Phase 4 -- Expect Primitives and CLI Surface

**Phase Goal:** Land the assertion DSL primitives (`Expect.*`) against the real `EvalContext`, and complete the `superclaude eval` Click group with all flags wired (including `--junit` per OQ-7 and `--no-pty` exclusion set per OQ-3). All seven Expect primitives are covered by tests; manifest `expects:` blocks executable in both declarative and programmatic forms; coverage-gate CLI entry green for a one-matcher fixture suite.

### T04.01 -- Implement FR-EXP1 Expect.* primitive package

| Field | Value |
|---|---|
| Roadmap Item IDs | R-064 |
| Why | FR-EXP1 implements the 7 primitives (file/jsonl/settings_json/exit_code/stderr/stdout/duration) against real `EvalContext`; each returns an `ExpectCallable` returning `ExpectResult`; declarative YAML + programmatic forms supported. |
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
| Deliverable IDs | D-0064 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0064/spec.md`
- `TASKLIST_ROOT/artifacts/D-0064/notes.md`
- `TASKLIST_ROOT/artifacts/D-0064/evidence.md`

**Deliverables:**
- Updated `src/superclaude/cli/eval/expect.py` replacing the M1 stubs (T01.14) with real primitives backed by `EvalContext`.

**Steps:**
1. **[PLANNING]** Confirm M1 ExpectDSL interface (T01.14), EvalContext (T03.03), ExpectResult (T01.15), ExpectFailure (T01.16).
2. **[PLANNING]** Plan named-argument signatures per COMP-010.1..6.
3. **[EXECUTION]** Replace `NotImplementedError("M4")` stubs with primitive implementations.
4. **[EXECUTION]** Ensure each primitive supports both declarative (YAML) and programmatic invocation.
5. **[VERIFICATION]** Run `uv run pytest tests/cli/eval/test_expect_primitives.py -v`.
6. **[COMPLETION]** Save evidence under `TASKLIST_ROOT/evidence/T04.01/`.

**Acceptance Criteria:**
- `src/superclaude/cli/eval/expect.py` exports working primitives `Expect.file`, `Expect.jsonl`, `Expect.settings_json`, `Expect.exit_code`, `Expect.stderr`, `Expect.stdout`, `Expect.duration`; none raise `NotImplementedError`.
- Each primitive returns an `ExpectCallable` that accepts an `EvalContext` and returns an `ExpectResult`.
- Both declarative (YAML mapping) and programmatic (direct method call) forms produce equivalent results.
- `TASKLIST_ROOT/artifacts/D-0064/spec.md` documents the 7 named-argument signatures.

**Validation:**
- Manual check: invoke `Expect.exit_code(equals=0)` on a stub EvalContext and assert ExpectResult.passed=True.
- Evidence: linkable artifact produced (spec/test log/screenshot/doc).

**Dependencies:** T01.14, T01.15, T01.16, T03.03
**Rollback:** TBD (if not specified in roadmap)
**Notes:** Individual primitive subtasks T04.02-T04.08 deliver per-primitive tests + edge cases.

### T04.02 -- Implement Expect.file primitive (COMP-010.1)

| Field | Value |
|---|---|
| Roadmap Item IDs | R-065 |
| Why | COMP-010.1 asserts file exists/content matches with args `path,exists,contains,regex,equals`; ExpectResult includes diff on failure. |
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
| Deliverable IDs | D-0065 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0065/spec.md`
- `TASKLIST_ROOT/artifacts/D-0065/notes.md`
- `TASKLIST_ROOT/artifacts/D-0065/evidence.md`

**Deliverables:**
- `Expect.file(path, exists=None, contains=None, regex=None, equals=None)` primitive + pytest module covering all argument combinations.

**Steps:**
1. **[PLANNING]** Confirm FR-EXP1 package skeleton (T04.01) is landed.
2. **[PLANNING]** Define diff representation for failure detail.
3. **[EXECUTION]** Implement `Expect.file` body with the 5 named arguments.
4. **[EXECUTION]** Author tests covering positive/negative cases for each argument.
5. **[VERIFICATION]** Run `uv run pytest tests/cli/eval/test_expect_file.py -v`.
6. **[COMPLETION]** Save evidence under `TASKLIST_ROOT/evidence/T04.02/`.

**Acceptance Criteria:**
- Function `Expect.file(path, exists, contains, regex, equals)` returns an ExpectCallable producing ExpectResult.
- Failure ExpectResult includes a unified diff snippet between expected and actual content.
- File `tests/cli/eval/test_expect_file.py` covers all 5 named-argument combinations with pass/fail cases.
- `TASKLIST_ROOT/artifacts/D-0065/spec.md` documents the signature and diff format.

**Validation:**
- Manual check: create a fixture file and invoke `Expect.file(path=..., contains="foo")` against an EvalContext.
- Evidence: linkable artifact produced (spec/test log/screenshot/doc).

**Dependencies:** T04.01
**Rollback:** TBD (if not specified in roadmap)
**Notes:** Used by E1 sticky lifecycle assertion (T05.02).

### T04.03 -- Implement Expect.jsonl primitive (COMP-010.2)

| Field | Value |
|---|---|
| Roadmap Item IDs | R-066 |
| Why | COMP-010.2 asserts JSONL entries match predicate; supports per-eval hook telemetry assertions used by sticky-lifecycle and matcher-coverage evals. |
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
| Deliverable IDs | D-0066 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0066/spec.md`
- `TASKLIST_ROOT/artifacts/D-0066/notes.md`
- `TASKLIST_ROOT/artifacts/D-0066/evidence.md`

**Deliverables:**
- `Expect.jsonl(path, line_count=None, filter=None, assert_each=None, assert_any=None)` primitive + pytest module.

**Steps:**
1. **[PLANNING]** Confirm FR-EXP1 (T04.01) and predicate helpers from T01.14.
2. **[PLANNING]** Define filter/assert_each/assert_any callable signature.
3. **[EXECUTION]** Implement `Expect.jsonl` body iterating lines, applying filter, then assertions.
4. **[EXECUTION]** Author tests covering hook telemetry fixture inputs.
5. **[VERIFICATION]** Run `uv run pytest tests/cli/eval/test_expect_jsonl.py -v`.
6. **[COMPLETION]** Save evidence under `TASKLIST_ROOT/evidence/T04.03/`.

**Acceptance Criteria:**
- Function `Expect.jsonl(path, line_count, filter, assert_each, assert_any)` returns an ExpectCallable producing ExpectResult.
- `assert_any` returns `passed=True` if at least one filtered line satisfies the predicate.
- File `tests/cli/eval/test_expect_jsonl.py` covers all 5 named-argument combinations with pass/fail cases.
- `TASKLIST_ROOT/artifacts/D-0066/spec.md` documents predicate semantics.

**Validation:**
- Manual check: create a fixture JSONL and invoke `Expect.jsonl(path=..., line_count=3)` against an EvalContext.
- Evidence: linkable artifact produced (spec/test log/screenshot/doc).

**Dependencies:** T04.01
**Rollback:** TBD (if not specified in roadmap)
**Notes:** Anchor for hook telemetry assertions (E1, E2.x).

### T04.04 -- Implement Expect.settings_json primitive (COMP-010.3)

| Field | Value |
|---|---|
| Roadmap Item IDs | R-067 |
| Why | COMP-010.3 asserts `~/.claude/settings.json` shape with args `path, key_path, equals, exists`; resolves against HomeIsolation.home_path. |
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
| Deliverable IDs | D-0067 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0067/spec.md`
- `TASKLIST_ROOT/artifacts/D-0067/notes.md`
- `TASKLIST_ROOT/artifacts/D-0067/evidence.md`

**Deliverables:**
- `Expect.settings_json(path, key_path, equals=None, exists=None)` primitive + pytest module.

**Steps:**
1. **[PLANNING]** Confirm FR-EXP1 (T04.01) and HomeIsolation.home_path (T02.11).
2. **[PLANNING]** Define key_path syntax (dot-separated dict keys).
3. **[EXECUTION]** Implement `Expect.settings_json` body resolving path against home_path; navigate key_path.
4. **[EXECUTION]** Author tests covering hooks.matchers presence/equality.
5. **[VERIFICATION]** Run `uv run pytest tests/cli/eval/test_expect_settings_json.py -v`.
6. **[COMPLETION]** Save evidence under `TASKLIST_ROOT/evidence/T04.04/`.

**Acceptance Criteria:**
- Function `Expect.settings_json(path, key_path, equals, exists)` returns an ExpectCallable producing ExpectResult.
- `path` resolves against `HomeIsolation.home_path` rather than the real `~/.claude/`.
- File `tests/cli/eval/test_expect_settings_json.py` covers key_path navigation + equals + exists.
- `TASKLIST_ROOT/artifacts/D-0067/spec.md` documents path resolution and key_path syntax.

**Validation:**
- Manual check: build a fixture settings.json in scratch HOME and invoke `Expect.settings_json` against it.
- Evidence: linkable artifact produced (spec/test log/screenshot/doc).

**Dependencies:** T02.11, T04.01
**Rollback:** TBD (if not specified in roadmap)
**Notes:** Anchor for coverage-gate matcher assertions.

### T04.05 -- Implement Expect.exit_code primitive (COMP-010.4)

| Field | Value |
|---|---|
| Roadmap Item IDs | R-068 |
| Why | COMP-010.4 asserts subprocess exit code with args `equals, in_set, not_equals`; default `equals 0`. |
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
| Deliverable IDs | D-0068 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0068/spec.md`
- `TASKLIST_ROOT/artifacts/D-0068/notes.md`
- `TASKLIST_ROOT/artifacts/D-0068/evidence.md`

**Deliverables:**
- `Expect.exit_code(equals=0, in_set=None, not_equals=None)` primitive + pytest module.

**Steps:**
1. **[PLANNING]** Confirm FR-EXP1 (T04.01) and EvalContext.exit_code (T03.03).
2. **[PLANNING]** Define mutually-exclusive argument validation.
3. **[EXECUTION]** Implement `Expect.exit_code` body honoring default and the 3 modes.
4. **[EXECUTION]** Author tests covering each argument mode.
5. **[VERIFICATION]** Run `uv run pytest tests/cli/eval/test_expect_exit_code.py -v`.
6. **[COMPLETION]** Save evidence under `TASKLIST_ROOT/evidence/T04.05/`.

**Acceptance Criteria:**
- Function `Expect.exit_code(equals, in_set, not_equals)` returns an ExpectCallable producing ExpectResult.
- Default `equals=0` applies when no argument is passed.
- Specifying both `equals` and `in_set` raises `ValueError` (mutually exclusive).
- `TASKLIST_ROOT/artifacts/D-0068/spec.md` documents the contract.

**Validation:**
- Manual check: invoke `Expect.exit_code(in_set={0,1})` on an EvalContext with exit_code=1.
- Evidence: linkable artifact produced (spec/test log/screenshot/doc).

**Dependencies:** T04.01
**Rollback:** TBD (if not specified in roadmap)
**Notes:** Most common Expect across the eval suite.

### T04.06 -- Checkpoint: Phase 4 / Tasks T04.01-T04.05

| Field | Value |
|---|---|
| Roadmap Item IDs | R-064,R-065,R-066,R-067,R-068 |
| Why | Gate: verify FR-EXP1 package and first 4 primitives (file, jsonl, settings_json, exit_code) before the remaining 3 primitives and CLI surface land. |
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
| Deliverable IDs | D-CP04-MID-T01-T05 |

**Checkpoint Report Path:** `TASKLIST_ROOT/checkpoints/CP-P04-T01-T05.md`

**Purpose:** Confirm FR-EXP1 + Expect.{file,jsonl,settings_json,exit_code} before stderr/stdout/duration + CLI wiring.

**Verification:**
- `Expect.file`, `Expect.jsonl`, `Expect.settings_json`, `Expect.exit_code` invocations against fixture EvalContexts succeed.
- No primitive raises `NotImplementedError("M4")`.
- ExpectResult diffs populated on failure paths.

**Exit Criteria:**
- `uv run pytest tests/cli/eval/test_expect_primitives.py tests/cli/eval/test_expect_file.py tests/cli/eval/test_expect_jsonl.py tests/cli/eval/test_expect_settings_json.py tests/cli/eval/test_expect_exit_code.py -v` exits 0.
- No stubs remain in `src/superclaude/cli/eval/expect.py` for the 4 primitives.
- Checkpoint report `CP-P04-T01-T05.md` records pass/fail per upstream task.

**Steps:**
1. **[VERIFICATION]** Confirm each artifact listed in Verification is present.
2. **[VERIFICATION]** Re-run the tier-proportional checks for the covered tasks.
3. **[VERIFICATION]** Write the checkpoint report to the Checkpoint Report Path above.

**Acceptance Criteria:**
- File `TASKLIST_ROOT/checkpoints/CP-P04-T01-T05.md` exists and contains `status: PASS`.
- All 3 Verification bullets are confirmed.
- All 3 Exit Criteria bullets are met.
- Checkpoint report includes the task IDs it covers (T04.01-T04.05).

**Validation:**
- Manual check: reviewer confirms the report at the Checkpoint Report Path.
- Evidence: the generated checkpoint markdown file.

**Dependencies:** T04.01..T04.05
**Rollback:** N/A (checkpoints are read-only verifications)

### T04.07 -- Implement Expect.stderr / Expect.stdout primitives (COMP-010.5)

| Field | Value |
|---|---|
| Roadmap Item IDs | R-069 |
| Why | COMP-010.5 asserts TTY transcripts match patterns with args `contains, regex, not_contains`; operates on ANSI-stripped buffer from COMP-011 PtyStream. |
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
| Deliverable IDs | D-0069 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0069/spec.md`
- `TASKLIST_ROOT/artifacts/D-0069/notes.md`
- `TASKLIST_ROOT/artifacts/D-0069/evidence.md`

**Deliverables:**
- `Expect.stderr(contains, regex, not_contains)` and `Expect.stdout(contains, regex, not_contains)` primitives + pytest module.

**Steps:**
1. **[PLANNING]** Confirm FR-EXP1 (T04.01), PtyStream ANSI-strip (T02.17), EvalContext stdout/stderr (T03.03).
2. **[PLANNING]** Define ANSI-stripped buffer source.
3. **[EXECUTION]** Implement `Expect.stderr` and `Expect.stdout` reusing the same internal predicate engine.
4. **[EXECUTION]** Author tests covering contains + regex + not_contains.
5. **[VERIFICATION]** Run `uv run pytest tests/cli/eval/test_expect_stdio.py -v`.
6. **[COMPLETION]** Save evidence under `TASKLIST_ROOT/evidence/T04.07/`.

**Acceptance Criteria:**
- Functions `Expect.stderr` and `Expect.stdout` return ExpectCallables producing ExpectResult; both operate on ANSI-stripped buffers.
- `not_contains` returns passed=True when the pattern is absent from the buffer.
- File `tests/cli/eval/test_expect_stdio.py` covers `contains`, `regex`, `not_contains` for both primitives.
- `TASKLIST_ROOT/artifacts/D-0069/spec.md` documents ANSI-strip dependency.

**Validation:**
- Manual check: feed an ANSI-laden transcript fixture and invoke `Expect.stdout(contains="ready")`.
- Evidence: linkable artifact produced (spec/test log/screenshot/doc).

**Dependencies:** T02.17, T04.01
**Rollback:** TBD (if not specified in roadmap)
**Notes:** Both primitives share the same predicate engine.

### T04.08 -- Implement Expect.duration primitive (COMP-010.6)

| Field | Value |
|---|---|
| Roadmap Item IDs | R-070 |
| Why | COMP-010.6 asserts eval duration within bound with args `max_sec, min_sec`; informational PASS records duration even if outside bound when only one bound set. |
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
| Deliverable IDs | D-0070 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0070/spec.md`
- `TASKLIST_ROOT/artifacts/D-0070/notes.md`
- `TASKLIST_ROOT/artifacts/D-0070/evidence.md`

**Deliverables:**
- `Expect.duration(max_sec=None, min_sec=None)` primitive + pytest module covering both bounds and informational mode.

**Steps:**
1. **[PLANNING]** Confirm FR-EXP1 (T04.01) and EvalContext.duration_sec (T03.03).
2. **[PLANNING]** Define informational PASS semantics for single-bound case.
3. **[EXECUTION]** Implement `Expect.duration` body honoring max_sec, min_sec, both, or neither.
4. **[EXECUTION]** Author tests covering both bounds + single-bound informational behavior.
5. **[VERIFICATION]** Run `uv run pytest tests/cli/eval/test_expect_duration.py -v`.
6. **[COMPLETION]** Save evidence under `TASKLIST_ROOT/evidence/T04.08/`.

**Acceptance Criteria:**
- Function `Expect.duration(max_sec, min_sec)` returns an ExpectCallable producing ExpectResult.
- When only one bound is set, the primitive records duration informationally even if the (missing) other bound would have failed.
- File `tests/cli/eval/test_expect_duration.py` covers max-only, min-only, both, and neither cases.
- `TASKLIST_ROOT/artifacts/D-0070/spec.md` documents informational-PASS semantics.

**Validation:**
- Manual check: build EvalContext with duration_sec=5 and invoke `Expect.duration(max_sec=3)` (fail) and `Expect.duration(min_sec=2)` (pass).
- Evidence: linkable artifact produced (spec/test log/screenshot/doc).

**Dependencies:** T04.01
**Rollback:** TBD (if not specified in roadmap)
**Notes:** Informational mode supports benchmarking without forcing assertions.

### T04.09 -- Register top-level eval_group Click commands (COMP-001)

| Field | Value |
|---|---|
| Roadmap Item IDs | R-071 |
| Why | COMP-001 exposes the top-level Click group with `run/list/describe/doctor` subcommands; group registered in superclaude entry point. |
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
| Deliverable IDs | D-0071 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0071/spec.md`
- `TASKLIST_ROOT/artifacts/D-0071/notes.md`
- `TASKLIST_ROOT/artifacts/D-0071/evidence.md`

**Deliverables:**
- `eval_group` Click group in `src/superclaude/cli/eval/commands.py` exporting `run`,`list`,`describe`,`doctor`.

**Steps:**
1. **[PLANNING]** Confirm M1 doctor/list/describe (T01.13, T01.21, T01.22) and FR-G3 registration (T01.26).
2. **[PLANNING]** Identify entry point for `run` subcommand (lands in T04.10).
3. **[EXECUTION]** Build `eval_group` Click group importing the 4 subcommands.
4. **[EXECUTION]** Confirm `superclaude eval --help` lists all 4.
5. **[VERIFICATION]** Run `uv run pytest tests/cli/eval/test_eval_group.py -v`.
6. **[COMPLETION]** Save evidence under `TASKLIST_ROOT/evidence/T04.09/`.

**Acceptance Criteria:**
- `superclaude eval --help` lists `run`, `list`, `describe`, `doctor` as subcommands.
- Click group is registered at the superclaude CLI entry point so existing commands remain unaffected.
- `superclaude --help` continues to list the eval group from T01.26 wiring.
- `TASKLIST_ROOT/artifacts/D-0071/spec.md` documents the group export.

**Validation:**
- Manual check: run `superclaude eval --help` and confirm all 4 subcommands listed.
- Evidence: linkable artifact produced (spec/test log/screenshot/doc).

**Dependencies:** T01.13, T01.21, T01.22, T01.26
**Rollback:** TBD (if not specified in roadmap)
**Notes:** `run` subcommand body lands in T04.10.

### T04.10 -- Implement FR-CLI1 `eval run` subcommand with all flags

| Field | Value |
|---|---|
| Roadmap Item IDs | R-072 |
| Why | FR-CLI1 wires all flags: `--suite, --parallel, --eval, --no-mcp, --no-pty, --output-dir, --keep-home, --timeout-mult, --max-disk-mb, --json, --verbose, --junit`. |
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
| Deliverable IDs | D-0072 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0072/spec.md`
- `TASKLIST_ROOT/artifacts/D-0072/notes.md`
- `TASKLIST_ROOT/artifacts/D-0072/evidence.md`

**Deliverables:**
- Click `eval run` subcommand exposing 12 flags wired to RunOrchestrator + CapabilityGates + Reporter + disk-budget.

**Steps:**
1. **[PLANNING]** Confirm RunOrchestrator (T03.15), disk budget (T03.19), DOC-OQ7 (T04.15), DOC-OQ3 (T04.16) statuses.
2. **[PLANNING]** Enumerate flag-to-component wiring.
3. **[EXECUTION]** Add `eval_run` Click command exposing the 12 flags.
4. **[EXECUTION]** Wire each flag to its target (parallel -> orchestrator, no-pty -> excluded set, etc.).
5. **[VERIFICATION]** Run `uv run pytest tests/cli/eval/test_eval_run.py -v`.
6. **[COMPLETION]** Save evidence under `TASKLIST_ROOT/evidence/T04.10/`.

**Acceptance Criteria:**
- `superclaude eval run --help` lists all 12 flags named in FR-CLI1.
- Each flag is validated: `--parallel 0` clamps to 1; `--parallel 16` clamps to 15; `--output-dir` resolves through AC12 allowlist.
- A one-eval run completes end-to-end with `--suite real --eval E1`.
- `TASKLIST_ROOT/artifacts/D-0072/spec.md` documents flag wiring.

**Validation:**
- Manual check: run `superclaude eval run --suite real --eval E1` and inspect exit code 0 and summary.
- Evidence: linkable artifact produced (spec/test log/screenshot/doc).

**Dependencies:** T03.15, T03.19, T04.09, T04.15, T04.16
**Rollback:** TBD (if not specified in roadmap)
**Notes:** Anchor for FR-G6 single-command runnability test (T04.11).

### T04.11 -- Single-command local runnability (FR-G6)

| Field | Value |
|---|---|
| Roadmap Item IDs | R-073 |
| Why | FR-G6 smoke test on clean Linux host completes 1-eval suite end-to-end with no manual setup beyond `make dev`. |
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
| Deliverable IDs | D-0073 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0073/spec.md`
- `TASKLIST_ROOT/artifacts/D-0073/notes.md`
- `TASKLIST_ROOT/artifacts/D-0073/evidence.md`

**Deliverables:**
- Smoke test `tests/cli/eval/test_single_command.py` running `uv run superclaude eval run --suite real --eval E1` end-to-end on a clean dev machine.

**Steps:**
1. **[PLANNING]** Confirm FR-CLI1 (T04.10) is landed.
2. **[PLANNING]** Define clean-host preconditions (fresh `make dev` install).
3. **[EXECUTION]** Author smoke test invoking `subprocess.run(['uv','run','superclaude','eval','run','--suite','real','--eval','E1'])`.
4. **[EXECUTION]** Assert exit code 0 and presence of summary.{md,json}.
5. **[VERIFICATION]** Run `uv run pytest tests/cli/eval/test_single_command.py -v`.
6. **[COMPLETION]** Save evidence under `TASKLIST_ROOT/evidence/T04.11/`.

**Acceptance Criteria:**
- File `tests/cli/eval/test_single_command.py` runs the full `uv run superclaude eval run --suite real --eval E1` invocation and exits 0.
- Test asserts presence of `summary.md` and `summary.json` under the per-run directory.
- No manual setup beyond `make dev` is required (test docstring records this).
- `TASKLIST_ROOT/artifacts/D-0073/spec.md` documents the clean-host contract.

**Validation:**
- Manual check: on a fresh container, run `make dev && uv run superclaude eval run --suite real --eval E1`.
- Evidence: linkable artifact produced (spec/test log/screenshot/doc).

**Dependencies:** T04.10
**Rollback:** TBD (if not specified in roadmap)
**Notes:** E1 (T05.02) must exist for end-to-end validation; pre-E1 phase smoke uses a stub eval.

### T04.12 -- Checkpoint: Phase 4 / Tasks T04.07-T04.11

| Field | Value |
|---|---|
| Roadmap Item IDs | R-069,R-070,R-071,R-072,R-073 |
| Why | Gate: verify stderr/stdout, duration, eval_group, eval run, and single-command runnability before reproducible artifacts and coverage gate land. |
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
| Deliverable IDs | D-CP04-MID-T07-T11 |

**Checkpoint Report Path:** `TASKLIST_ROOT/checkpoints/CP-P04-T07-T11.md`

**Purpose:** Confirm Expect.stderr/stdout/duration + Click group + eval run + FR-G6 single-command before artifact layout + coverage gate.

**Verification:**
- `Expect.stderr`, `Expect.stdout`, `Expect.duration` invocations succeed against fixtures.
- `superclaude eval run --help` lists all 12 flags.
- Smoke test runs `uv run superclaude eval run` end-to-end and exits 0.

**Exit Criteria:**
- `uv run pytest tests/cli/eval/test_expect_stdio.py tests/cli/eval/test_expect_duration.py tests/cli/eval/test_eval_group.py tests/cli/eval/test_eval_run.py tests/cli/eval/test_single_command.py -v` exits 0.
- All 7 Expect primitives reachable (no stubs remaining).
- Checkpoint report `CP-P04-T07-T11.md` records pass/fail per upstream task.

**Steps:**
1. **[VERIFICATION]** Confirm each artifact listed in Verification is present.
2. **[VERIFICATION]** Re-run the tier-proportional checks for the covered tasks.
3. **[VERIFICATION]** Write the checkpoint report to the Checkpoint Report Path above.

**Acceptance Criteria:**
- File `TASKLIST_ROOT/checkpoints/CP-P04-T07-T11.md` exists and contains `status: PASS`.
- All 3 Verification bullets are confirmed.
- All 3 Exit Criteria bullets are met.
- Checkpoint report includes the task IDs it covers (T04.07-T04.11).

**Validation:**
- Manual check: reviewer confirms the report at the Checkpoint Report Path.
- Evidence: the generated checkpoint markdown file.

**Dependencies:** T04.07..T04.11
**Rollback:** N/A (checkpoints are read-only verifications)

### T04.13 -- Implement FR-G4 reproducible artifact layout

| Field | Value |
|---|---|
| Roadmap Item IDs | R-074 |
| Why | FR-G4 requires per-run artifact tree under `.dev/eval-runs/<ISO>/<run-id>/` containing `summary.{md,json}`, `junit.xml` (when enabled), and `per-eval/{logs.jsonl,tty.transcript,artifacts/}`. |
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
| Deliverable IDs | D-0074 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0074/spec.md`
- `TASKLIST_ROOT/artifacts/D-0074/notes.md`
- `TASKLIST_ROOT/artifacts/D-0074/evidence.md`

**Deliverables:**
- Run artifact writer placing each run under `.dev/eval-runs/<ISO>/<run-id>/` with the prescribed per-eval subtree.

**Steps:**
1. **[PLANNING]** Confirm Reporter (T03.13) and EvalRunner JSONL (T03.05) interfaces.
2. **[PLANNING]** Define run-id generation (ISO timestamp + short suffix).
3. **[EXECUTION]** Implement `compose_run_dir(output_root, started_at) -> Path` returning `.dev/eval-runs/<ISO>/<run-id>/`.
4. **[EXECUTION]** Route Reporter writes + per-eval logs into this layout.
5. **[VERIFICATION]** Run `uv run pytest tests/cli/eval/test_artifact_layout.py -v`.
6. **[COMPLETION]** Save evidence under `TASKLIST_ROOT/evidence/T04.13/`.

**Acceptance Criteria:**
- Each run produces a directory under `.dev/eval-runs/<ISO>/<run-id>/` containing `summary.md`, `summary.json`, and a `per-eval/` subtree per eval.
- Per-eval subtree contains `logs.jsonl`, `tty.transcript`, and `artifacts/`.
- Run-id is deterministic for a given start timestamp + suite name.
- `TASKLIST_ROOT/artifacts/D-0074/spec.md` documents the directory layout.

**Validation:**
- Manual check: invoke a run and inspect the resulting directory tree.
- Evidence: linkable artifact produced (spec/test log/screenshot/doc).

**Dependencies:** T03.05, T03.13
**Rollback:** TBD (if not specified in roadmap)
**Notes:** AC12 allowlist (T01.19) gates the root resolution.

### T04.14 -- Implement FR-G5 hook-matcher coverage gate (CLI entry)

| Field | Value |
|---|---|
| Roadmap Item IDs | R-075 |
| Why | FR-G5 computes matcher coverage map; FAILS run if any matcher pattern in `~/.claude/settings.json` lacks a corresponding eval; v1 covers `mcp__auggie__*, mcp__auggie-mcp__*, mcp__airis-mcp-gateway__*`. |
| Effort | L |
| Risk | Medium |
| Risk Drivers | scope (cross-cutting coverage gate) |
| Tier | STANDARD |
| Confidence | [████████--] 85% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | None | Preferred: Sequential, Context7 |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0075 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0075/spec.md`
- `TASKLIST_ROOT/artifacts/D-0075/notes.md`
- `TASKLIST_ROOT/artifacts/D-0075/evidence.md`

**Deliverables:**
- `coverage_gate(settings_path, suite)` checker emitting `coverage_missing:<pattern>` artifact when matchers lack covering evals; wired into `eval doctor --check-coverage` and top-of-run.

**Steps:**
1. **[PLANNING]** Confirm CapabilityGates (T01.11), doctor (T01.13), eval run (T04.10).
2. **[PLANNING]** Define matcher->eval mapping rule (tag-based registry).
3. **[EXECUTION]** Implement `coverage_gate(settings_path, suite)` enumerating matchers and resolving covering evals.
4. **[EXECUTION]** Wire to `eval doctor --check-coverage` and top-of-run gate; emit `coverage_missing:<pattern>` artifact on failure.
5. **[VERIFICATION]** Run `uv run pytest tests/cli/eval/test_coverage_gate.py -v`.
6. **[COMPLETION]** Save evidence under `TASKLIST_ROOT/evidence/T04.14/`.

**Acceptance Criteria:**
- Function `coverage_gate(settings_path, suite)` reads matcher patterns from settings.json and resolves at least one covering eval per pattern.
- For v1, the gate confirms coverage for `mcp__auggie__*`, `mcp__auggie-mcp__*`, `mcp__airis-mcp-gateway__*`.
- Missing coverage produces a `coverage_missing:<pattern>` artifact file and fails the run with exit 2.
- `TASKLIST_ROOT/artifacts/D-0075/spec.md` documents the matcher->eval mapping.

**Validation:**
- Manual check: stub a settings.json with a 4th matcher and confirm gate fails.
- Evidence: linkable artifact produced (spec/test log/screenshot/doc).

**Dependencies:** T01.11, T01.13, T04.10
**Rollback:** TBD (if not specified in roadmap)
**Notes:** Full coverage validation runs against real settings.json in M5 (T05.25).

### T04.15 -- DOC-OQ7 `--junit` flag wiring decision

| Field | Value |
|---|---|
| Roadmap Item IDs | R-076 |
| Why | DOC-OQ7 decides and implements `--junit` flag wiring per OQ-7 resolution OR removes the conditional language from spec §9. |
| Effort | S |
| Risk | Low |
| Risk Drivers | None |
| Tier | EXEMPT |
| Confidence | [█████████-] 90% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Skip verification |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0076 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0076/spec.md`
- `TASKLIST_ROOT/artifacts/D-0076/notes.md`
- `TASKLIST_ROOT/artifacts/D-0076/evidence.md`

**Deliverables:**
- Decision recorded in `.dev/releases/current/cliEval/decisions.md`; either `--junit` wired into FR-CLI1 or spec §9 corrected.

**Steps:**
1. **[PLANNING]** Read OQ-7 status and proposed resolution.
2. **[PLANNING]** Confirm Reporter `to_junit()` (T03.13) is available if wiring.
3. **[EXECUTION]** Record decision (wire or remove) in decisions.md.
4. **[EXECUTION]** Apply the chosen action (add --junit flag in T04.10 OR update spec §9).
5. **[VERIFICATION]** Manual review of decisions.md entry.
6. **[COMPLETION]** Save evidence under `TASKLIST_ROOT/evidence/T04.15/`.

**Acceptance Criteria:**
- File `.dev/releases/current/cliEval/decisions.md` contains a DOC-OQ7 entry recording the decision (wire or remove).
- If wired, `superclaude eval run --junit` produces `junit.xml` under the run directory.
- If removed, spec §9 no longer references `--junit`.
- `TASKLIST_ROOT/artifacts/D-0076/spec.md` records the rationale.

**Validation:**
- Manual check: confirm decisions.md entry and consistent FR-CLI1 implementation.
- Evidence: linkable artifact produced (spec/test log/screenshot/doc).

**Dependencies:** T03.13
**Rollback:** TBD (if not specified in roadmap)
**Notes:** Carried from M1 OPS-001 (T01.25); finalization happens here.

### T04.16 -- DOC-OQ3 `--no-pty` exclusion set in real.yaml

| Field | Value |
|---|---|
| Roadmap Item IDs | R-077 |
| Why | DOC-OQ3 writes the exclusion set to `suites/real.yaml` as `no_pty: skip` per eval; `--no-pty` honors the tag; documented in `eval describe`. |
| Effort | S |
| Risk | Low |
| Risk Drivers | None |
| Tier | EXEMPT |
| Confidence | [█████████-] 90% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Skip verification |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0077 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0077/spec.md`
- `TASKLIST_ROOT/artifacts/D-0077/notes.md`
- `TASKLIST_ROOT/artifacts/D-0077/evidence.md`

**Deliverables:**
- `no_pty: skip` annotation added to each PTY-required eval in `suites/real.yaml`; eval run wired to honor the tag under `--no-pty`.

**Steps:**
1. **[PLANNING]** Identify PTY-required evals from the E1-E15 inventory.
2. **[PLANNING]** Confirm eval describe (T01.22) and eval run (T04.10) wiring.
3. **[EXECUTION]** Add `no_pty: skip` to each PTY-required eval entry in `suites/real.yaml`.
4. **[EXECUTION]** Wire `--no-pty` flag to skip tagged evals with `skip_reason="--no-pty"`.
5. **[VERIFICATION]** Run `uv run pytest tests/cli/eval/test_no_pty_exclusion.py -v`.
6. **[COMPLETION]** Save evidence under `TASKLIST_ROOT/evidence/T04.16/`.

**Acceptance Criteria:**
- File `suites/real.yaml` annotates each PTY-required eval with `no_pty: skip`.
- `superclaude eval run --no-pty` skips the tagged evals and emits status `SKIPPED` with `skip_reason="--no-pty"`.
- `superclaude eval describe --suite real --eval <id>` surfaces the `no_pty` tag.
- `TASKLIST_ROOT/artifacts/D-0077/spec.md` records the exclusion set and rationale.

**Validation:**
- Manual check: run `superclaude eval run --suite real --no-pty` and confirm tagged evals are skipped.
- Evidence: linkable artifact produced (spec/test log/screenshot/doc).

**Dependencies:** T01.22, T04.10
**Rollback:** TBD (if not specified in roadmap)
**Notes:** Carried from M1 OPS-001 (T01.25); finalization happens here.

### T04.17 -- TEST-007 reporter contract tests

| Field | Value |
|---|---|
| Roadmap Item IDs | R-078 |
| Why | TEST-007 covers N' vs K behavior, skipped inclusion, mismatch failure, JSON schema fidelity for the FR-RPT1 contract. |
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
| Deliverable IDs | D-0078 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0078/spec.md`
- `TASKLIST_ROOT/artifacts/D-0078/notes.md`
- `TASKLIST_ROOT/artifacts/D-0078/evidence.md`

**Deliverables:**
- Pytest module `tests/cli/eval/test_reporter_contract.py` covering the 4 TEST-007 scenarios.

**Steps:**
1. **[PLANNING]** Confirm FR-RPT1 (T03.11), DM-012 schema (T03.10), and Reporter (T03.13) are landed.
2. **[PLANNING]** Enumerate test cases: N' vs K equality, skipped inclusion, mismatch->exit 2, schema fidelity.
3. **[EXECUTION]** Author `tests/cli/eval/test_reporter_contract.py` covering all 4 cases.
4. **[EXECUTION]** Assert each scenario's exit code + artifact presence.
5. **[VERIFICATION]** Run `uv run pytest tests/cli/eval/test_reporter_contract.py -v`.
6. **[COMPLETION]** Save evidence under `TASKLIST_ROOT/evidence/T04.17/`.

**Acceptance Criteria:**
- File `tests/cli/eval/test_reporter_contract.py` contains 4 tests covering N'-vs-K equality, skipped inclusion, mismatch failure, JSON schema fidelity.
- `uv run pytest tests/cli/eval/test_reporter_contract.py -v` exits 0 with all 4 passing.
- Mismatch test asserts process exit code 2 and `ReporterContractViolation` raised.
- `TASKLIST_ROOT/artifacts/D-0078/spec.md` records the test matrix.

**Validation:**
- Manual check: run the test module and inspect assertions.
- Evidence: linkable artifact produced (spec/test log/screenshot/doc).

**Dependencies:** T03.10, T03.11, T03.13
**Rollback:** TBD (if not specified in roadmap)
**Notes:** Cross-links FR-RPT1 + DM-012.

### T04.18 -- Checkpoint: Phase 4 / Tasks T04.13-T04.17

| Field | Value |
|---|---|
| Roadmap Item IDs | R-074,R-075,R-076,R-077,R-078 |
| Why | Gate: verify artifact layout, coverage gate CLI, OQ-7/OQ-3 decisions, reporter contract tests before exit-code semantics + retention policy close M4. |
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
| Deliverable IDs | D-CP04-MID-T13-T17 |

**Checkpoint Report Path:** `TASKLIST_ROOT/checkpoints/CP-P04-T13-T17.md`

**Purpose:** Confirm FR-G4 artifact layout + FR-G5 coverage gate + DOC-OQ7/OQ3 decisions + TEST-007 reporter contract before final tests close M4.

**Verification:**
- Per-run directory layout matches FR-G4 spec for a fixture run.
- `coverage_gate` rejects a settings.json with an uncovered matcher.
- TEST-007 reporter-contract suite passes (4 tests).

**Exit Criteria:**
- `uv run pytest tests/cli/eval/test_artifact_layout.py tests/cli/eval/test_coverage_gate.py tests/cli/eval/test_no_pty_exclusion.py tests/cli/eval/test_reporter_contract.py -v` exits 0.
- DOC-OQ7 and DOC-OQ3 entries present in decisions.md.
- Checkpoint report `CP-P04-T13-T17.md` records pass/fail per upstream task.

**Steps:**
1. **[VERIFICATION]** Confirm each artifact listed in Verification is present.
2. **[VERIFICATION]** Re-run the tier-proportional checks for the covered tasks.
3. **[VERIFICATION]** Write the checkpoint report to the Checkpoint Report Path above.

**Acceptance Criteria:**
- File `TASKLIST_ROOT/checkpoints/CP-P04-T13-T17.md` exists and contains `status: PASS`.
- All 3 Verification bullets are confirmed.
- All 3 Exit Criteria bullets are met.
- Checkpoint report includes the task IDs it covers (T04.13-T04.17).

**Validation:**
- Manual check: reviewer confirms the report at the Checkpoint Report Path.
- Evidence: the generated checkpoint markdown file.

**Dependencies:** T04.13..T04.17
**Rollback:** N/A (checkpoints are read-only verifications)

### T04.19 -- TEST-008 exit-code semantics tests

| Field | Value |
|---|---|
| Roadmap Item IDs | R-079 |
| Why | TEST-008 covers process exit codes 0/1/2/3 per spec: 0 iff no FAIL/ERRORED/TIMEOUT/XPASS; 1 if any such eval; 2 harness error; 3 interrupted. |
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
| Deliverable IDs | D-0079 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0079/spec.md`
- `TASKLIST_ROOT/artifacts/D-0079/notes.md`
- `TASKLIST_ROOT/artifacts/D-0079/evidence.md`

**Deliverables:**
- Pytest module `tests/cli/eval/test_exit_codes.py` exercising clean (0), failing (1), harness-error (2), and interrupted (3) paths.

**Steps:**
1. **[PLANNING]** Confirm NFR-REL1 (T03.07) signal handling and FR-RPT1 (T03.11) contract guard.
2. **[PLANNING]** Build fixtures producing each exit-code condition deterministically.
3. **[EXECUTION]** Author `tests/cli/eval/test_exit_codes.py` with one test per exit path.
4. **[EXECUTION]** Assert each test's process exit code via `subprocess.run` + `returncode`.
5. **[VERIFICATION]** Run `uv run pytest tests/cli/eval/test_exit_codes.py -v`.
6. **[COMPLETION]** Save evidence under `TASKLIST_ROOT/evidence/T04.19/`.

**Acceptance Criteria:**
- File `tests/cli/eval/test_exit_codes.py` contains 4 tests, one per exit code (0,1,2,3).
- `uv run pytest tests/cli/eval/test_exit_codes.py -v` exits 0 with all 4 tests passing.
- Each test asserts the process exit code via `subprocess.run` against `superclaude eval run`.
- `TASKLIST_ROOT/artifacts/D-0079/spec.md` documents the exit-code policy.

**Validation:**
- Manual check: run the targeted pytest module.
- Evidence: linkable artifact produced (spec/test log/screenshot/doc).

**Dependencies:** T03.07, T03.11, T04.10
**Rollback:** TBD (if not specified in roadmap)
**Notes:** Anchors the FR-RPT1 contract behavior at the process boundary.

### T04.20 -- TEST-009 artifact reproducibility tests

| Field | Value |
|---|---|
| Roadmap Item IDs | R-080 |
| Why | TEST-009 verifies run directories, transcripts, logs, stack traces, and summaries are written deterministically; run dir pattern stable; transcript path recorded. |
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
| Deliverable IDs | D-0080 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0080/spec.md`
- `TASKLIST_ROOT/artifacts/D-0080/notes.md`
- `TASKLIST_ROOT/artifacts/D-0080/evidence.md`

**Deliverables:**
- Pytest module `tests/cli/eval/test_artifact_reproducibility.py` confirming run-dir pattern, transcript presence, logs presence, stack trace on error, summary cross-link.

**Steps:**
1. **[PLANNING]** Confirm FR-G4 artifact layout (T04.13) is landed.
2. **[PLANNING]** Build fixtures producing a pass + an error scenario.
3. **[EXECUTION]** Author tests asserting each required artifact path exists and is non-empty.
4. **[EXECUTION]** Assert summary.json's `evals[]` entries cross-link to per-eval artifact paths.
5. **[VERIFICATION]** Run `uv run pytest tests/cli/eval/test_artifact_reproducibility.py -v`.
6. **[COMPLETION]** Save evidence under `TASKLIST_ROOT/evidence/T04.20/`.

**Acceptance Criteria:**
- File `tests/cli/eval/test_artifact_reproducibility.py` asserts run dir matches `.dev/eval-runs/<ISO>/<run-id>/`.
- Per-eval `logs.jsonl`, `tty.transcript` exist; stack trace recorded on ERRORED status.
- summary.json `evals[]` entries reference per-eval artifact paths.
- `TASKLIST_ROOT/artifacts/D-0080/spec.md` records the reproducibility matrix.

**Validation:**
- Manual check: run a fixture suite and inspect the artifact tree.
- Evidence: linkable artifact produced (spec/test log/screenshot/doc).

**Dependencies:** T04.13
**Rollback:** TBD (if not specified in roadmap)
**Notes:** Cross-links FR-G4 + DM-012.

### T04.21 -- Define OPS-003 artifact retention policy

| Field | Value |
|---|---|
| Roadmap Item IDs | R-081 |
| Why | OPS-003 defines default deletion and keep-home behavior: `--keep-home` default false; failed setup preserved; run summaries retained; disk budget messages include retention advice. |
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
| Deliverable IDs | D-0081 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0081/spec.md`
- `TASKLIST_ROOT/artifacts/D-0081/notes.md`
- `TASKLIST_ROOT/artifacts/D-0081/evidence.md`

**Deliverables:**
- Policy doc `docs/eval/retention.md` + assertions wired into RunOrchestrator on disk-budget breach messages.

**Steps:**
1. **[PLANNING]** Confirm `--keep-home` flag (T04.10) and disk-budget messages (T03.19).
2. **[PLANNING]** Define retention defaults: keep-home=False, failed-setup preserved (NFR-ISO2), summary retained.
3. **[EXECUTION]** Author `docs/eval/retention.md` documenting the policy.
4. **[EXECUTION]** Update disk-budget breach messages to include retention advice.
5. **[VERIFICATION]** Run `uv run pytest tests/cli/eval/test_retention_policy.py -v`.
6. **[COMPLETION]** Save evidence under `TASKLIST_ROOT/evidence/T04.21/`.

**Acceptance Criteria:**
- File `docs/eval/retention.md` documents: `--keep-home` default false, failed setups preserved, summaries retained, disk-budget advice text.
- Disk-budget breach error message contains the retention-advice string verbatim.
- `--keep-home True` test confirms per-eval HOMEs are preserved after run.
- `TASKLIST_ROOT/artifacts/D-0081/spec.md` records the policy.

**Validation:**
- Manual check: read `docs/eval/retention.md` and confirm policy entries.
- Evidence: linkable artifact produced (spec/test log/screenshot/doc).

**Dependencies:** T03.19, T04.10
**Rollback:** TBD (if not specified in roadmap)
**Notes:** Pairs with NFR-PERF4 disk-budget breach behavior.

### T04.22 -- Checkpoint: End of Phase 4

| Field | Value |
|---|---|
| Roadmap Item IDs | R-064..R-081 |
| Why | M4 exit gate: all 7 Expect primitives covered by tests, `superclaude eval run --suite real` parses every documented flag, manifest expects: blocks executable in declarative and programmatic forms, coverage-gate CLI green for one-matcher fixture suite. |
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
| Deliverable IDs | D-CP04 |

**Checkpoint Report Path:** `TASKLIST_ROOT/checkpoints/CP-P04-END.md`

**Purpose:** M4 exit gate: Expect primitives + CLI surface + coverage gate + reporter contract + artifact reproducibility verified.

**Verification:**
- All 7 Expect primitives reachable with tests passing.
- `superclaude eval run --help` lists all 12 FR-CLI1 flags.
- `coverage_gate` green for the one-matcher fixture suite; fails with `coverage_missing:<pattern>` when matcher uncovered.

**Exit Criteria:**
- `uv run pytest tests/cli/eval/ -v` passes for M4 modules.
- DOC-OQ7 and DOC-OQ3 decisions recorded in decisions.md.
- Checkpoint report `CP-P04-END.md` records pass/fail per task in Phase 4.

**Steps:**
1. **[VERIFICATION]** Confirm each artifact listed in Verification is present.
2. **[VERIFICATION]** Re-run the tier-proportional checks for the covered tasks.
3. **[VERIFICATION]** Write the checkpoint report to the Checkpoint Report Path above.

**Acceptance Criteria:**
- File `TASKLIST_ROOT/checkpoints/CP-P04-END.md` exists and contains `status: PASS`.
- All 3 Verification bullets are confirmed.
- All 3 Exit Criteria bullets are met.
- Checkpoint report includes the task IDs it covers (T04.01-T04.21).

**Validation:**
- Manual check: reviewer confirms the report at the Checkpoint Report Path.
- Evidence: the generated checkpoint markdown file.

**Dependencies:** T04.01..T04.21
**Rollback:** N/A (checkpoints are read-only verifications)
