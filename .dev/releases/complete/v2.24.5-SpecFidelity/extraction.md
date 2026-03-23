---
spec_source: v2.25.1-release-spec.md
generated: "2026-03-20T00:00:00Z"
generator: requirements-extraction-agent-opus-4.6
functional_requirements: 9
nonfunctional_requirements: 6
total_requirements: 15
complexity_score: 0.5
complexity_class: MEDIUM
domains_detected: [backend, cli, testing, devops]
risks_identified: 8
dependencies_identified: 4
success_criteria_count: 10
extraction_mode: standard
pipeline_diagnostics: {elapsed_seconds: 93.0, started_at: "2026-03-20T17:05:27.907954+00:00", finished_at: "2026-03-20T17:07:00.922748+00:00"}
---

## Functional Requirements

### FR-001.1: build_command() includes --tools default

**Description**: `ClaudeProcess.build_command()` must include `--tools` and `default` as adjacent list elements in the returned command list.

**Acceptance Criteria**:
- `"--tools" in cmd` is `True`
- `cmd[cmd.index("--tools") + 1] == "default"`
- Flag appears between `--no-session-persistence` and `--max-turns`

**Dependencies**: None

---

### FR-001.2: Existing command structure unchanged

**Description**: All pre-existing flags must remain in the returned command list. The `extra_args` passthrough must continue to work.

**Acceptance Criteria**:
- `--print`, `--verbose`, `--no-session-persistence`, `--max-turns`, `--output-format`, `-p` all still present
- `extra_args` list still appended after `--model`
- `--model` flag still conditional on `self.model` being non-empty

**Dependencies**: FR-001.1

---

### FR-001.3: Test coverage for the new flag

**Description**: Regression tests must assert `--tools default` is present so future edits cannot silently drop it.

**Acceptance Criteria**:
- New test `test_tools_default_in_command` exists in `tests/pipeline/test_process.py`
- `test_required_flags` updated to assert `--tools` and `default` present
- `test_stream_json_matches_sprint_flags` updated similarly
- All three tests pass under `uv run pytest tests/pipeline/test_process.py -v`

**Dependencies**: FR-001.1

---

### FR-ATL.1: Derive `_EMBED_SIZE_LIMIT` from `MAX_ARG_STRLEN`

**Description**: Replace `_EMBED_SIZE_LIMIT = 200 * 1024` with a derivation from `_MAX_ARG_STRLEN = 128 * 1024` minus `_PROMPT_TEMPLATE_OVERHEAD = 8 * 1024`.

**Acceptance Criteria**:
- `_MAX_ARG_STRLEN`, `_PROMPT_TEMPLATE_OVERHEAD`, and `_EMBED_SIZE_LIMIT` are defined as module-level constants in `executor.py`
- `_EMBED_SIZE_LIMIT` equals `_MAX_ARG_STRLEN - _PROMPT_TEMPLATE_OVERHEAD` (120 KB)
- No `import resource` line (dead code from brainstorm draft)
- Stale `# 100 KB` comment is removed
- Module-level `assert _PROMPT_TEMPLATE_OVERHEAD >= 4096` present immediately after the three constant definitions, with error message stating kernel margin rationale and measured template peak (~3.4 KB); triggered on any `import executor` call
- Each constant carries an inline comment: `_MAX_ARG_STRLEN` notes Linux kernel compile-time constant; `_PROMPT_TEMPLATE_OVERHEAD` notes 2.3x safety factor and measured peak; `_EMBED_SIZE_LIMIT` notes derivation and resulting byte value

**Dependencies**: None

---

### FR-ATL.2: Guard full composed `-p` argument

**Description**: Change the embed guard to measure `step.prompt + "\n\n" + embedded` (the actual `-p` argument value), not just `embedded`.

**Acceptance Criteria**:
- Guard evaluates `len(composed.encode("utf-8")) <= _EMBED_SIZE_LIMIT` where `composed = step.prompt + "\n\n" + embedded`
- Warning log reports "composed prompt" and actual byte count
- Fallback fires for inputs that fit individually but exceed limit when combined with prompt
- When `len(composed.encode('utf-8')) == _EMBED_SIZE_LIMIT` exactly (at-limit), inline embedding fires (not fallback) — confirming `<=` is the intended operator
- Code comment adjacent to guard explains: `<= is intentional; _EMBED_SIZE_LIMIT = 120 KB is safely below MAX_ARG_STRLEN = 128 KB`

**Dependencies**: FR-ATL.1

---

### FR-ATL.3: Rename misleading test

**Description**: Rename `test_100kb_guard_fallback` to `test_embed_size_guard_fallback` and update docstrings/comments referencing "100KB".

**Acceptance Criteria**:
- Method renamed to `test_embed_size_guard_fallback`
- Class docstring updated to reference `_EMBED_SIZE_LIMIT` not "100KB"
- Test logic unchanged (imports `_EMBED_SIZE_LIMIT`, auto-adapts to new value)

**Dependencies**: FR-ATL.1

---

### FR-ATL.4: Test composed-string guard behavior

**Description**: Add a test verifying the fallback fires when `prompt + embedded` exceeds the limit even though `embedded` alone fits.

**Acceptance Criteria**:
- Test creates a file at 90% of `_EMBED_SIZE_LIMIT`
- Test creates a prompt large enough that combined exceeds limit
- Asserts file content is NOT in captured prompt (fallback fired)
- Asserts `--file` flags are present in `extra_args`

**Dependencies**: FR-ATL.1, FR-ATL.2

---

### FR-ATL.5: Validate `--file` fallback (BLOCKING pre-condition)

**Description**: Empirically test whether `claude --print --file /bare/path` delivers file content to the model. This is a blocking gate that determines whether Phase 1.5 conditional fixes activate.

**Sub-requirements**:

#### FR-ATL.5a: Phase 0 — Empirical validation (unconditional)
- Manual test executed using unique timestamp sentinel (`PINEAPPLE` test)
- Result recorded as WORKING, BROKEN, or CLI FAILURE
- CLI prerequisite verified (`claude --print -p "hello" --max-turns 1`)

#### FR-ATL.5b: Phase 1.5 — Conditional fixes (only if BROKEN)
- If BROKEN: `remediate_executor.py:177` fixed to use inline embedding instead of `--file`
- If BROKEN: fallback path in `executor.py`, `validate_executor.py`, and `tasklist/executor.py` fixed to use inline embedding
- If WORKING: Phase 1.5 marked N/A

**Dependencies**: None (run first — gates all other tasks)

---

### FR-ATL.5-IMPLICIT: Phase 0 CLI prerequisite check

**Description** (implicit requirement): Before the `--file` empirical test can produce valid results, the CLI must be installed, authenticated, and able to complete a basic `--print` request. This is stated as a prerequisite in Phase 0 but represents a distinct validation step.

**Acceptance Criteria**:
- `claude --print -p "hello" --max-turns 1` succeeds with exit code 0
- If this fails, resolve CLI issues before proceeding to the PINEAPPLE test

**Dependencies**: None

---

## Non-Functional Requirements

### NFR-001.1: No performance regression

**Description**: Subprocess start time must remain unchanged. `--tools default` adds <1ms to flag parsing.

**Measurement**: Timing comparison of subprocess launch with and without flag.

---

### NFR-001.2: Backwards compatible

**Description**: All existing callers of `build_command()` must remain unaffected.

**Measurement**: Full test suite green with no modifications to callers.

---

### NFR-ATL.1: No new module dependencies

**Description**: Zero new imports added to any modified file.

**Measurement**: `grep` for new import lines in changed files.

---

### NFR-ATL.2: Behavioral change is crash-to-fallback (strictly better)

**Description**: For inputs below 120 KB, behavior is identical to pre-fix. For inputs 120-200 KB (previously crashed), behavior is now graceful fallback.

**Measurement**: Existing tests pass unchanged; no regression for small inputs.

---

### NFR-ATL.3: Existing test suite passes without modification

**Description**: 100% pass rate on pre-existing tests (only renamed/updated tests change).

**Measurement**: `uv run pytest` full suite green.

---

### NFR-ATL.4: Constants are self-documenting

**Description**: Zero magic numbers in the embed guard implementation. Every constant has a derivation comment.

**Measurement**: Code review confirms inline comments on all three constants.

---

## Complexity Assessment

**Score**: 0.5 / 1.0
**Class**: MEDIUM

**Rationale**:
- **Code change surface area** (Low): FIX-001 is a 2-line addition to one method. FIX-ARG-TOO-LONG modifies constants and one guard condition in one file. Total touched files: 4-8 depending on Phase 1.5 activation.
- **Conditional execution paths** (Medium): Phase 0 blocking gate creates a branching implementation plan. Phase 1.5 is conditional on empirical results, requiring two distinct completion scenarios.
- **Cross-module interaction** (Medium): Two independent fixes share `build_command()` as a delivery mechanism. Non-inheriting executors create a secondary concern tracked as OQ-4.
- **Testing complexity** (Low-Medium): Unit tests are straightforward mocking. The Phase 0 empirical test requires a live CLI environment.
- **Risk profile** (Low-Medium): 80% probability that `--file` fallback is broken elevates conditional path complexity, but mitigations are well-defined.

---

## Architectural Constraints

1. **Single edit point for FIX-001**: `--tools default` must be added in `ClaudeProcess.build_command()` only — not in subclasses or call sites. All subclasses inherit automatically.

2. **Flag placement**: `--tools default` must appear between `--no-session-persistence` and `--max-turns` in the command list to keep session-control flags grouped.

3. **Constant derivation**: `_EMBED_SIZE_LIMIT` must be derived from `_MAX_ARG_STRLEN - _PROMPT_TEMPLATE_OVERHEAD`, not hardcoded. This encodes the OS constraint relationship.

4. **Linux kernel constraint**: `MAX_ARG_STRLEN = 128 KB` is a compile-time constant in the Linux kernel; it cannot be queried at runtime via `getrlimit()`.

5. **No new dependencies**: Zero new imports permitted in modified files. No `import resource`.

6. **Implementation order**: Phase 0 (empirical test) is a blocking gate. Phase 1.1 (FIX-001) must complete before any combined test suite run due to flag position shifts.

7. **Scope boundary**: `remediate_executor.py`, `validate_executor.py`, and `tasklist/executor.py` do NOT inherit from `ClaudeProcess`. Adding `--tools default` to these is out of scope unless Phase 1.5 activates.

8. **Out of scope**: Stdin prompt delivery (deferred to v2.26), prompt compression, Windows 32 KB limit, sprint orchestration logic.

9. **UV only**: All test execution must use `uv run pytest`, never bare `python -m pytest`.

---

## Risk Inventory

1. **[Medium] `--file` fallback is broken** — 80% probability per code review. Impact: High — fallback path is non-functional, all oversized inputs crash. Mitigation: Phase 0 empirical test is a blocking gate; Phase 1.5 contingency plan defined with specific file fixes.

2. **[Low] `--tools default` enables unintended tool** — Default tool set may include unexpected tools. Impact: Medium — model could invoke unintended tools. Mitigation: Default set is stable, already used in interactive mode; subprocess was the anomaly.

3. **[Low] Subclass overrides `build_command()` without `super()`** — Could bypass the fix. Impact: Low — no current overrides exist. Mitigation: Read subclass files before editing to confirm inheritance chain.

4. **[Low] Index-based test assertions break** — `--tools default` shifts flag positions in command list. Impact: Low — tests fail but code is correct. Mitigation: Phase 1.1 must land before Phase 3 combined test run; update positional assertions.

5. **[Low] 8 KB overhead too conservative** — Unnecessary `--file` fallback for 112-120 KB inputs. Impact: Low — fallback is functional, just slower. Mitigation: Full-string measurement (FR-ATL.2) is the real safety gate.

6. **[Low] Future template exceeds 8 KB** — Narrows safe embed window. Impact: Medium — more inputs hit fallback. Mitigation: `_PROMPT_TEMPLATE_OVERHEAD` is a named constant, easy to update.

7. **[Low] Windows 32 KB command-line limit** — Cross-platform users affected. Impact: Medium — Windows pipeline runs would fail earlier. Mitigation: Deferred; Linux-first fix is correct priority.

8. **[Low] Non-inheriting executors lack `--tools default`** — `remediate_executor.py`, `validate_executor.py`, `tasklist/executor.py` build commands independently. Impact: Medium — tool schema discovery failure could recur. Mitigation: Tracked as OQ-4; assess after Phase 0.

---

## Dependency Inventory

1. **`claude` CLI** — External binary. Must be installed, authenticated, and able to complete `--print` requests. Required for Phase 0 empirical test and all E2E validation. Must support `--tools default` flag.

2. **Linux kernel `MAX_ARG_STRLEN`** — Compile-time constant (128 KB on standard kernels). The entire embed guard design depends on this value. Non-configurable at runtime.

3. **`ClaudeProcess` base class** (`src/superclaude/cli/pipeline/process.py`) — Shared by `SprintProcess`, `RoadmapProcess`, etc. FIX-001 relies on inheritance propagation.

4. **`executor.py` embed pipeline** (`src/superclaude/cli/roadmap/executor.py`) — Owns `_embed_inputs()` and `roadmap_run_step()`. FIX-ARG-TOO-LONG modifies constants and guard logic here.

---

## Success Criteria

1. **`--tools default` present in all subprocess commands**: `"--tools" in cmd and cmd[cmd.index("--tools") + 1] == "default"` for every `ClaudeProcess.build_command()` invocation.

2. **Phase 2 sprint succeeds**: `superclaude sprint run` completes Phase 2 without `InputValidationError` on `TodoWrite` or `Bash`.

3. **No `OSError [Errno 7]`**: Pipeline runs with spec files up to 120 KB complete without argument-list-too-long crashes.

4. **Fallback fires for oversized inputs**: Inputs where `prompt + embedded > 120 KB` trigger the `--file` fallback path (or inline embedding if Phase 1.5 activated).

5. **Existing tests pass unchanged**: `uv run pytest tests/pipeline/ tests/roadmap/ tests/sprint/ -v` — 100% pass rate.

6. **New regression tests pass**: `test_tools_default_in_command`, `test_embed_size_guard_fallback`, `test_prompt_plus_embedded_exceeds_limit` all green.

7. **Phase 0 result recorded**: `--file` fallback empirically tested and result documented as WORKING or BROKEN.

8. **Zero new imports**: No new `import` statements in any modified file.

9. **Constants self-documenting**: All three embed constants (`_MAX_ARG_STRLEN`, `_PROMPT_TEMPLATE_OVERHEAD`, `_EMBED_SIZE_LIMIT`) have inline derivation comments.

10. **At-limit boundary correct**: Input exactly equal to `_EMBED_SIZE_LIMIT` bytes uses inline embedding (confirms `<=` operator).

---

## Open Questions

1. **OQ-1: Does `claude --print --file /bare/path` deliver file content?** — Phase 0 blocking gate. 80% probability it's broken based on code review showing bare paths where `file_id:relative_path` format may be required. Resolution: 15-minute empirical test.

2. **OQ-2: Does `claude --print` accept prompt from stdin?** — Would enable an alternative prompt delivery mechanism bypassing `MAX_ARG_STRLEN` entirely. Deferred to v2.26 spike. Not blocking for v2.24.5.

3. **OQ-3: Is `remediate_executor.py:177` actively producing incorrect results?** — If `--file` is broken, all prior remediation runs may have been context-free (model never received target file content). Phase 0 determines; Phase 1.5 fixes if confirmed.

4. **OQ-4: Do non-`ClaudeProcess` executors need `--tools default`?** — `remediate_executor.py`, `validate_executor.py`, `tasklist/executor.py` build commands independently and don't inherit from `ClaudeProcess`. If tool schema discovery is also broken in these paths, they need the same fix. Assess after Phase 0 result is known.

5. **Implicit: What is the actual `--file` flag format?** — Code review suggests bare paths are used, but `claude --help` may document `file_id:relative_path` format. Phase 0 test resolves this empirically.

6. **Implicit: Are there other executors beyond the four identified that build subprocess commands independently?** — The spec identifies four files. A codebase search for subprocess invocation patterns would confirm completeness.
