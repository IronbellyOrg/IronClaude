# Phase 2 -- Classifier Registry

Create the classifier registry module with built-in classifiers, lookup validation, and exception handling. This phase produces a standalone `classifiers.py` module that is independent of Phase 1 and can be developed in parallel. All code is in `src/superclaude/cli/sprint/classifiers.py`.

---

### T02.01 -- Create `classifiers.py` with CLASSIFIERS Registry

| Field | Value |
|---|---|
| Roadmap Item IDs | R-015, R-016 |
| Why | The classifier registry provides a central lookup for named classifiers that evaluate subprocess output at preflight execution time. The registry pattern allows future classifier additions without modifying executor code. |
| Effort | S |
| Risk | Low |
| Risk Drivers | None matched |
| Tier | STANDARD |
| Confidence | [████████--] 82% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | Preferred: Sequential |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0011 |

**Artifacts (Intended Paths):**
- .dev/releases/current/v2.25.5-PreFlightExecutor/artifacts/D-0011/evidence.md

**Deliverables:**
- `src/superclaude/cli/sprint/classifiers.py` containing `CLASSIFIERS: dict[str, Callable[[int, str, str], str]]` registry

**Steps:**
1. **[PLANNING]** Review the `src/superclaude/cli/sprint/` package to understand module organization conventions
2. **[PLANNING]** Confirm no existing classifier module or registry exists
3. **[EXECUTION]** Create `src/superclaude/cli/sprint/classifiers.py`
4. **[EXECUTION]** Define `CLASSIFIERS: dict[str, Callable[[int, str, str], str]] = {}` at module level
5. **[EXECUTION]** Add type annotation: each classifier takes `(exit_code: int, stdout: str, stderr: str)` and returns a classification label `str`
6. **[VERIFICATION]** Import the module successfully: `from superclaude.cli.sprint.classifiers import CLASSIFIERS`
7. **[COMPLETION]** Record module location and registry structure in evidence

**Acceptance Criteria:**
- File `src/superclaude/cli/sprint/classifiers.py` exists with `CLASSIFIERS` dict exported at module level
- `CLASSIFIERS` type is `dict[str, Callable[[int, str, str], str]]`
- Module is importable without errors: `from superclaude.cli.sprint.classifiers import CLASSIFIERS`
- CLASSIFIERS registry is importable and accepts classifier registrations

**Validation:**
- `uv run python -c "from superclaude.cli.sprint.classifiers import CLASSIFIERS; print(type(CLASSIFIERS))"` outputs `<class 'dict'>`
- Evidence: linkable artifact at .dev/releases/current/v2.25.5-PreFlightExecutor/artifacts/D-0011/evidence.md

**Dependencies:** None
**Rollback:** Delete `src/superclaude/cli/sprint/classifiers.py`

---

### T02.02 -- Implement `empirical_gate_v1` Classifier

| Field | Value |
|---|---|
| Roadmap Item IDs | R-017 |
| Why | The built-in classifier interprets subprocess exit codes and output to produce a deterministic pass/fail classification label for preflight task results. |
| Effort | S |
| Risk | Low |
| Risk Drivers | None matched |
| Tier | STANDARD |
| Confidence | [████████--] 80% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | Preferred: Sequential |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0012 |

**Artifacts (Intended Paths):**
- .dev/releases/current/v2.25.5-PreFlightExecutor/artifacts/D-0012/evidence.md

**Deliverables:**
- `empirical_gate_v1(exit_code: int, stdout: str, stderr: str) -> str` function registered in `CLASSIFIERS["empirical_gate_v1"]`

**Steps:**
1. **[PLANNING]** Review the roadmap definition: classifier returns classification label (e.g., `"pass"`, `"fail"`)
2. **[PLANNING]** Design simple, deterministic logic: exit_code == 0 -> "pass", else "fail"
3. **[EXECUTION]** Implement `empirical_gate_v1` function in `classifiers.py`
4. **[EXECUTION]** Register it: `CLASSIFIERS["empirical_gate_v1"] = empirical_gate_v1`
5. **[VERIFICATION]** Test: `empirical_gate_v1(0, "output", "")` returns `"pass"` and `empirical_gate_v1(1, "", "error")` returns `"fail"`
6. **[COMPLETION]** Record classifier logic and test results in evidence

**Acceptance Criteria:**
- `CLASSIFIERS["empirical_gate_v1"]` resolves to a callable function
- `empirical_gate_v1(0, "any stdout", "")` returns `"pass"`
- `empirical_gate_v1(1, "", "error output")` returns `"fail"`
- `empirical_gate_v1(127, "", "command not found")` returns `"fail"` (general non-zero exit code contract)
- Classifier logic is simple and deterministic with no external dependencies

**Validation:**
- `uv run python -c "from superclaude.cli.sprint.classifiers import CLASSIFIERS; print(CLASSIFIERS['empirical_gate_v1'](0, 'ok', ''))"` outputs `pass`
- Evidence: linkable artifact at .dev/releases/current/v2.25.5-PreFlightExecutor/artifacts/D-0012/evidence.md

**Dependencies:** T02.01
**Rollback:** Remove the function and its registry entry

---

### T02.03 -- Add Classifier Lookup Validation and Exception Handling

| Field | Value |
|---|---|
| Roadmap Item IDs | R-018, R-019 |
| Why | Missing classifier names must fail closed with `KeyError`, and classifier exceptions during invocation must be caught, logged at WARNING, and treated as task failure to prevent silent misclassification. |
| Effort | S |
| Risk | Low |
| Risk Drivers | None matched |
| Tier | STRICT |
| Confidence | [████████--] 85% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena |
| Fallback Allowed | No |
| Sub-Agent Delegation | Recommended |
| Deliverable IDs | D-0013 |

**Artifacts (Intended Paths):**
- .dev/releases/current/v2.25.5-PreFlightExecutor/artifacts/D-0013/evidence.md

**Deliverables:**
- Classifier lookup validation: `CLASSIFIERS["nonexistent"]` raises `KeyError`; wrapper function catches classifier exceptions, logs at WARNING, returns `"error"` classification

**Steps:**
1. **[PLANNING]** Review how classifiers will be invoked from the preflight executor (T03.01)
2. **[PLANNING]** Design a wrapper function `run_classifier(name, exit_code, stdout, stderr) -> str`
3. **[EXECUTION]** Implement `run_classifier()` in `classifiers.py` that looks up `CLASSIFIERS[name]` (KeyError propagates on missing)
4. **[EXECUTION]** Wrap the classifier call in `try/except Exception`: on exception, `logger.warning(f"Classifier {name} raised {exc}")` and return `"error"`
5. **[EXECUTION]** Document that `"error"` classification maps to `TaskStatus.FAIL` at the executor level
6. **[VERIFICATION]** Test: `run_classifier("nonexistent", 0, "", "")` raises `KeyError`; a classifier that raises `ValueError` returns `"error"`
7. **[COMPLETION]** Record wrapper design and error handling behavior in evidence

**Acceptance Criteria:**
- `CLASSIFIERS["nonexistent_classifier"]` raises `KeyError` (dict default behavior, not suppressed)
- `run_classifier()` catches exceptions from classifier functions and returns `"error"` classification
- Exception is logged at WARNING level with classifier name and exception message
- `"error"` classification returned by `run_classifier()` is mapped to `TaskStatus.FAIL` by the executor (verifiable via T03.01 integration)

**Validation:**
- `uv run pytest tests/cli/sprint/test_preflight.py -v -k classifier` exits 0
- Evidence: linkable artifact at .dev/releases/current/v2.25.5-PreFlightExecutor/artifacts/D-0013/evidence.md

**Dependencies:** T02.01, T02.02
**Rollback:** Remove `run_classifier()` function; callers use direct dict lookup

---

### T02.04 -- Unit Tests for Classifier Registry

| Field | Value |
|---|---|
| Roadmap Item IDs | R-020, R-021, R-022 |
| Why | Unit tests validate the classifier registry, the built-in `empirical_gate_v1` classifier, KeyError behavior on missing classifiers, and exception handling in classifier invocation. |
| Effort | S |
| Risk | Low |
| Risk Drivers | None matched |
| Tier | EXEMPT |
| Confidence | [█████████-] 90% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Skip verification |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0014 |

**Artifacts (Intended Paths):**
- .dev/releases/current/v2.25.5-PreFlightExecutor/artifacts/D-0014/evidence.md

**Deliverables:**
- Unit tests covering: `empirical_gate_v1` with known pass/fail inputs; `KeyError` on missing classifier name; exception handling in classifier invocation returning `"error"`

**Steps:**
1. **[PLANNING]** Review existing test file structure in `tests/cli/sprint/`
2. **[PLANNING]** Plan 4 test functions matching R-020, R-021, R-022 (R-020 split into pass and fail tests)
3. **[EXECUTION]** Write `test_empirical_gate_v1_pass()` and `test_empirical_gate_v1_fail()` in test file
4. **[EXECUTION]** Write `test_missing_classifier_raises_keyerror()` asserting `KeyError` on `CLASSIFIERS["nonexistent"]`
5. **[EXECUTION]** Write `test_classifier_exception_returns_error()` with a mock classifier that raises `ValueError`
6. **[VERIFICATION]** Run `uv run pytest tests/cli/sprint/test_preflight.py -v -k classifier` and verify all pass
7. **[COMPLETION]** Record test results in evidence

**Acceptance Criteria:**
- `uv run pytest tests/cli/sprint/test_preflight.py -v -k classifier` exits 0 with 4+ tests passing
- Tests cover pass input, fail input, missing classifier KeyError, and exception handling
- No test depends on external services or mutable global state
- Tests are marked with `@pytest.mark.unit`

**Validation:**
- `uv run pytest tests/cli/sprint/test_preflight.py -v -k classifier` exits 0
- Evidence: linkable artifact at .dev/releases/current/v2.25.5-PreFlightExecutor/artifacts/D-0014/evidence.md

**Dependencies:** T02.01, T02.02, T02.03
**Rollback:** Delete the test functions; no production code affected

---

### Checkpoint: End of Phase 2

**Purpose:** Gate for Phase 3: confirm the classifier registry is operational with built-in classifier, lookup validation, and exception handling, all covered by unit tests.
**Checkpoint Report Path:** .dev/releases/current/v2.25.5-PreFlightExecutor/checkpoints/CP-P02-END.md
**Verification:**
- `src/superclaude/cli/sprint/classifiers.py` exists with `CLASSIFIERS` registry and `empirical_gate_v1`
- `run_classifier()` handles missing classifiers (KeyError) and classifier exceptions (WARNING + "error")
- All classifier unit tests pass: `uv run pytest tests/cli/sprint/test_preflight.py -v -k classifier`
**Exit Criteria:**
- All 4 tasks (T02.01-T02.04) have status completed with evidence artifacts
- Module is importable and registry contains `empirical_gate_v1`
- No regressions in existing test suite
