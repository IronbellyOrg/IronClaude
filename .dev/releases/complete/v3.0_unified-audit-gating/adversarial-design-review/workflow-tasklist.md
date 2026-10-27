# Workflow Tasklist: Solution C — Leading Whitespace Fix
<!-- compliance: strict -->
<!-- spec: adversarial-design-review/merged-design-spec.md -->
<!-- executor: sc:task-unified --compliance strict -->

## Metadata
- **Generated**: 2026-03-18
- **Source spec**: `adversarial-design-review/merged-design-spec.md`
- **Target file**: `src/superclaude/cli/roadmap/executor.py`
- **Test file**: `tests/roadmap/test_executor.py`
- **Total tasks**: 11
- **Phases**: 4 (Fix → Test → Verify → Sync)
- **Dependencies**: Sequential within phases; Phase N depends on Phase N-1

---

## Phase 1: Code Fixes (3 tasks)

### Task 1.1: Replace `_sanitize_output` function body
- **Compliance**: STRICT
- **File**: `src/superclaude/cli/roadmap/executor.py`
- **Lines**: 82-120 (entire function body)
- **Action**: Replace the function `_sanitize_output` with the version from the merged design spec §1 Fix 1
- **Key changes**:
  1. Rename local variable `content` → `raw` for the initial `read_text` call
  2. Add `content = raw.lstrip("\n\r\t ")` after reading
  3. Replace the early-return block (lines 100-102) with a conditional that writes back stripped content when `content != raw` and `content.startswith("---")`
  4. Update the preamble-stripping path to account for leading whitespace already stripped from `raw`
  5. Compute `preamble_bytes` as `len(raw.encode("utf-8")) - len(cleaned.encode("utf-8"))` to include both leading whitespace and conversational preamble
- **Acceptance criteria**:
  - [ ] Function strips leading `\n\r\t ` characters before checking for `---`
  - [ ] When content has leading whitespace but starts with `---` after stripping: file is rewritten atomically (`.tmp` + `os.replace`), returns byte count of stripped whitespace
  - [ ] When content already starts with `---` (no leading whitespace): returns 0, file untouched
  - [ ] When content has conversational preamble: existing behavior preserved (preamble stripped)
  - [ ] When no frontmatter found: returns 0, file untouched
  - [ ] `FileNotFoundError` still returns 0
- **Depends on**: None
- **Rollback**: Revert to original function. Fix 2 independently handles `test-strategy` case.

---

### Task 1.2: Harden `_inject_provenance_fields` with lstrip + idempotency
- **Compliance**: STRICT
- **File**: `src/superclaude/cli/roadmap/executor.py`
- **Lines**: 155-184
- **Action**: Two changes to `_inject_provenance_fields`:
  - **1.2a — lstrip**: Change line 166-168 from:
    ```python
    content = output_file.read_text(encoding="utf-8")
    if not content.startswith("---"):
        return
    ```
    To:
    ```python
    content = output_file.read_text(encoding="utf-8").lstrip("\n\r\t ")
    if not content.startswith("---"):
        return
    ```
  - **1.2b — idempotency**: Replace the unconditional provenance injection block (lines 175-184) with field-existence checks:
    ```python
    frontmatter = content[3:end_idx]

    fields_to_inject = []
    if "spec_source:" not in frontmatter:
        fields_to_inject.append(f"spec_source: {spec_source}")
    if "generated:" not in frontmatter:
        generated = datetime.now(timezone.utc).isoformat()
        fields_to_inject.append(f'generated: "{generated}"')
    if "generator:" not in frontmatter:
        fields_to_inject.append("generator: superclaude-roadmap-executor")

    if not fields_to_inject:
        return

    provenance_block = "\n".join(fields_to_inject)
    new_content = content[:end_idx] + "\n" + provenance_block + content[end_idx:]
    output_file.write_text(new_content, encoding="utf-8")
    ```
- **Acceptance criteria**:
  - [ ] `.lstrip("\n\r\t ")` applied to `read_text` result
  - [ ] Each provenance field checked for existence before injection
  - [ ] Calling twice on same file does NOT produce duplicate `spec_source:` keys
  - [ ] Fields already present are preserved (not overwritten)
  - [ ] Missing fields are still injected correctly
  - [ ] No-frontmatter and unclosed-frontmatter cases still return early
- **Depends on**: None (independent of Task 1.1 — belt-and-suspenders)
- **Rollback**: Revert to original. Fix 1 ensures clean input.

---

### Task 1.3: Harden `_inject_pipeline_diagnostics` with lstrip + idempotency
- **Compliance**: STRICT
- **File**: `src/superclaude/cli/roadmap/executor.py`
- **Lines**: 123-152
- **Action**: Two changes to `_inject_pipeline_diagnostics`:
  - **1.3a — lstrip**: Change line 133-135 from:
    ```python
    content = output_file.read_text(encoding="utf-8")
    if not content.startswith("---"):
        return
    ```
    To:
    ```python
    content = output_file.read_text(encoding="utf-8").lstrip("\n\r\t ")
    if not content.startswith("---"):
        return
    ```
  - **1.3b — idempotency**: After `end_idx` check, add:
    ```python
    frontmatter = content[3:end_idx]
    if "pipeline_diagnostics:" in frontmatter:
        return  # Already injected
    ```
- **Acceptance criteria**:
  - [ ] `.lstrip("\n\r\t ")` applied to `read_text` result
  - [ ] `pipeline_diagnostics:` checked for existence before injection
  - [ ] Calling twice on same file does NOT produce duplicate `pipeline_diagnostics:` keys
  - [ ] No-frontmatter and unclosed-frontmatter cases still return early
- **Depends on**: None (independent of Tasks 1.1 and 1.2)
- **Rollback**: Revert to original. Fix 1 ensures clean input.

---

## Phase 2: Test Implementation (4 tasks)

### Task 2.1: Add `TestSanitizeOutputLeadingWhitespace` test class
- **Compliance**: STRICT
- **File**: `tests/roadmap/test_executor.py`
- **Action**: Add new test class with 8 test cases per merged spec §3.1
- **Tests**:
  1. `test_leading_newlines_stripped` — `\n\n---\n...` → returns 2, file starts with `---`
  2. `test_leading_crlf_stripped` — `\r\n\n---\n...` → returns 3, file starts with `---`
  3. `test_single_leading_newline_stripped` — `\n---\n...` → returns 1
  4. `test_no_leading_whitespace_unchanged` — `---\n...` → returns 0, untouched
  5. `test_no_frontmatter_with_leading_whitespace` — `\n\nJust text` → returns 0, untouched
  6. `test_leading_newlines_plus_preamble` — `\n\nHere is result:\n\n---\n...` → returns total stripped bytes
  7. `test_empty_file` — `""` → returns 0
  8. `test_only_whitespace` — `\n\n\n` → returns 0, unchanged
- **Acceptance criteria**:
  - [ ] All 8 tests pass with `uv run pytest tests/roadmap/test_executor.py::TestSanitizeOutputLeadingWhitespace -v`
  - [ ] Uses `tmp_path` fixture for file creation
  - [ ] Imports `_sanitize_output` from `superclaude.cli.roadmap.executor`
- **Depends on**: Task 1.1

---

### Task 2.2: Add `TestInjectProvenanceFields` test class
- **Compliance**: STRICT
- **File**: `tests/roadmap/test_executor.py`
- **Action**: Add new test class with 8 test cases per merged spec §3.2 (full pytest code provided in spec)
- **Tests**:
  1. `test_injects_into_clean_frontmatter` — baseline injection
  2. `test_injects_with_leading_blank_lines` — THE BUG regression test
  3. `test_noop_without_frontmatter` — plain text unchanged
  4. `test_noop_empty_file` — empty file unchanged
  5. `test_noop_unclosed_frontmatter` — no closing `---`
  6. `test_idempotent_double_call` — no duplicate keys on retry
  7. `test_partial_provenance_present` — only missing fields injected
  8. `test_empty_frontmatter_block` — empty `---\n---` gets fields
- **Acceptance criteria**:
  - [ ] All 8 tests pass with `uv run pytest tests/roadmap/test_executor.py::TestInjectProvenanceFields -v`
  - [ ] Imports `_inject_provenance_fields` from `superclaude.cli.roadmap.executor`
- **Depends on**: Task 1.2

---

### Task 2.3: Add `TestInjectPipelineDiagnostics` test class
- **Compliance**: STRICT
- **File**: `tests/roadmap/test_executor.py`
- **Action**: Add new test class with 2 test cases per merged spec §3.3 (full pytest code provided in spec)
- **Tests**:
  1. `test_injects_with_leading_blank_lines` — leading whitespace doesn't prevent injection
  2. `test_idempotent_double_call` — no duplicate `pipeline_diagnostics:` on retry
- **Acceptance criteria**:
  - [ ] Both tests pass with `uv run pytest tests/roadmap/test_executor.py::TestInjectPipelineDiagnostics -v`
  - [ ] Imports `_inject_pipeline_diagnostics` and `datetime`/`timezone` from correct modules
- **Depends on**: Task 1.3

---

### Task 2.4: Add E2E integration tests
- **Compliance**: STRICT
- **File**: `tests/roadmap/test_executor.py`
- **Action**: Add 3 integration tests per merged spec §3.4
- **Tests**:
  1. `test_test_strategy_with_leading_blanks_passes_gate` — mock subprocess writes output with `\n\n---\n...`, verify `TEST_STRATEGY_GATE` passes after full `roadmap_run_step` flow
  2. `test_extract_with_leading_blanks_passes_gate` — mock subprocess writes extract output with `\n---\n...`, verify `_inject_pipeline_diagnostics` succeeds
  3. `test_sanitize_enables_provenance_injection` — call `_sanitize_output` then `_inject_provenance_fields` on file with leading blanks, verify `spec_source` present
- **Acceptance criteria**:
  - [ ] All 3 tests pass
  - [ ] Tests verify the full sanitize → inject → gate flow, not just individual functions
- **Depends on**: Tasks 1.1, 1.2, 1.3 (all fixes must be in place)

---

## Phase 3: Verification (3 tasks)

### Task 3.1: Run regression test suite
- **Compliance**: STRICT
- **Action**: Execute existing tests to confirm no regressions
- **Commands**:
  ```bash
  uv run pytest tests/roadmap/test_executor.py -v
  uv run pytest tests/roadmap/test_gates_data.py -v
  ```
- **Acceptance criteria**:
  - [ ] All existing `TestSanitizeOutput` tests pass (5 named in spec §3.5)
  - [ ] All existing `TestTestStrategyGateIntegration` tests pass (3 named in spec §3.5)
  - [ ] All new tests from Phase 2 pass
  - [ ] Zero failures, zero errors
- **Depends on**: All Phase 2 tasks

---

### Task 3.2: Run full test suite
- **Compliance**: STRICT
- **Action**: Execute the complete test suite for cross-cutting regression detection
- **Commands**:
  ```bash
  uv run pytest tests/ -v --timeout=120
  ```
- **Acceptance criteria**:
  - [ ] Full suite passes with zero failures
  - [ ] No new warnings introduced
- **Depends on**: Task 3.1

---

### Task 3.3: Manual smoke test
- **Compliance**: STRICT
- **Action**: Run manual verification per merged spec §4.2
- **Steps**:
  1. Create test file: `printf '\n\n---\ncomplexity_class: MEDIUM\nvalidation_philosophy: continuous-parallel\nvalidation_milestones: 3\nwork_milestones: 6\ninterleave_ratio: 1:2\nmajor_issue_policy: stop-and-fix\n---\n## Test Strategy\n- item 1\n' > /tmp/test-strategy-leading-blanks.md`
  2. Run `_sanitize_output` — verify returns >0 bytes, file starts with `---`
  3. Run `_inject_provenance_fields` — verify `spec_source`, `generated`, `generator` present
- **Acceptance criteria**:
  - [ ] `_sanitize_output` returns byte count > 0
  - [ ] File starts with `---` after sanitize
  - [ ] All 3 provenance fields present after inject
- **Depends on**: Task 3.1

---

## Phase 4: Sync & Commit (1 task)

### Task 4.1: Sync, verify, and commit
- **Compliance**: STRICT
- **Action**: Sync component changes and commit
- **Steps**:
  1. `make sync-dev` — sync `src/superclaude/` to `.claude/`
  2. `make verify-sync` — confirm sync is clean
  3. Stage files:
     - `src/superclaude/cli/roadmap/executor.py`
     - `tests/roadmap/test_executor.py`
  4. Commit with message: `fix: strip leading whitespace before frontmatter provenance injection`
- **Acceptance criteria**:
  - [ ] `make verify-sync` exits 0
  - [ ] Only the 2 expected files are staged
  - [ ] Commit message follows conventional commits format
- **Depends on**: Tasks 3.1, 3.2, 3.3 (all verification passes)

---

## Dependency Graph

```
Phase 1 (parallel):
  Task 1.1 ─┐
  Task 1.2 ─┼─→ Phase 2
  Task 1.3 ─┘

Phase 2 (parallel where possible):
  Task 2.1 (depends: 1.1) ─┐
  Task 2.2 (depends: 1.2) ─┼─→ Task 2.4 (depends: 1.1, 1.2, 1.3)
  Task 2.3 (depends: 1.3) ─┘         │
                                      ↓
Phase 3 (sequential):
  Task 3.1 → Task 3.2 → Task 3.3

Phase 4:
  Task 4.1 (depends: 3.1, 3.2, 3.3)
```

## Rollback Matrix

| Task | Rollback action | Impact on other fixes |
|------|----------------|----------------------|
| 1.1 | Revert `_sanitize_output` to original | Fix 2 still handles test-strategy; Fix 3 still handles extract |
| 1.2 | Revert `_inject_provenance_fields` to original | Fix 1 ensures clean input for this function |
| 1.3 | Revert `_inject_pipeline_diagnostics` to original | Fix 1 ensures clean input for this function |
| Full | Revert all 3 fixes | Pipeline returns to broken state |
