# Patch Checklist
Generated: 2026-03-16
Total edits: 8 across 4 files

## File-by-file edit checklist

- phase-1-tasklist.md
  - [ ] Add failure triage step and acceptance criterion to T01.01 (from finding M1)

- phase-2-tasklist.md
  - [ ] Strengthen T02.01 acceptance criteria with explicit freshness guard, zero-byte, stale, mkdir, OSError semantics (from finding M2)
  - [ ] Add exact WARNING format to T02.03 T-005 description (from finding L2)
  - [ ] Change T02.03 validation command to remove `-k` filter (from finding L3)

- phase-3-tasklist.md
  - [ ] Update T03.01 DEBUG log requirement with both primary labels and parenthetical context (from finding M3)
  - [ ] Add PASS_NO_REPORT enum preservation acceptance criterion to T03.05 (from finding M4)
  - [ ] Name the three ordered calls explicitly in T03.02 acceptance criteria (from finding L4)

- phase-4-tasklist.md
  - [ ] Add OQ-001 attribute-name verification acceptance criterion to T04.02 (from finding M5)

## Cross-file consistency sweep
- [ ] Verify all validation commands use full file run (no `-k` filters) unless explicitly scoped

---

## Precise diff plan

### 1) phase-1-tasklist.md

#### Section/heading to change
- T01.01 Steps and Acceptance Criteria

#### Planned edits

**A. Add triage step (M1)**
Current issue: Step 5 says "Confirm all tests pass" but lacks triage/resolve workflow for failures.
Change: Add to step 5: "if any failures exist, triage and resolve before proceeding to Phase 2"
Diff intent: Step 5 becomes: "**[VERIFICATION]** Confirm all tests pass; if any failures exist, triage and resolve before proceeding to Phase 2"

**B. Add triage acceptance criterion (M1)**
Current issue: AC bullet 2 says "No pre-existing failures" but doesn't mention triage workflow.
Change: Reword AC bullet 2 to: "If any baseline failures found, they are triaged and resolved before Phase 2 begins"
Diff intent: "No pre-existing failures that could mask regressions from the fix" -> "Any baseline failures are triaged and resolved before Phase 2 begins; no pre-existing failures mask regressions"

### 2) phase-2-tasklist.md

#### Section/heading to change
- T02.01 Acceptance Criteria
- T02.03 Steps and Validation

#### Planned edits

**A. Strengthen T02.01 acceptance (M2)**
Current issue: AC bullet 2 says "Function writes exactly `EXIT_RECOMMENDATION: CONTINUE\n` when file is absent, zero-byte, or stale"
Change: Replace with explicit guard semantics
Diff intent: Replace bullet 2 with: "Freshness guard: `exists()` AND `st_size > 0` AND `st_mtime >= started_at` triggers no-op (return `False`); zero-byte and stale files (`st_mtime < started_at`) treated as absent and overwritten with `EXIT_RECOMMENDATION: CONTINUE\n`; `mkdir(parents=True, exist_ok=True)` before write; `try/except OSError` with WARNING log returns `False`"

**B. Add exact WARNING format to T02.03 (L2)**
Current issue: Step 6 says WARNING logged containing "preliminary result write failed"
Change: Add exact format requirement
Diff intent: In step 6, after "WARNING logged", add: "with exact format: `preliminary result write failed: %s; phase may report PASS_NO_REPORT`"

**C. Fix T02.03 validation command (L3)**
Current issue: Validation says `uv run pytest tests/sprint/test_executor.py -v -k "preliminary_result"`
Change: Remove `-k` filter
Diff intent: `uv run pytest tests/sprint/test_executor.py -v -k "preliminary_result"` -> `uv run pytest tests/sprint/test_executor.py -v`

### 3) phase-3-tasklist.md

#### Section/heading to change
- T03.01 Steps and Acceptance Criteria
- T03.02 Acceptance Criteria
- T03.05 Acceptance Criteria

#### Planned edits

**A. Fix T03.01 DEBUG log (M3)**
Current issue: Step 5 has only `option_d`/`option_a_or_noop` parenthetical context, missing primary labels.
Change: Add primary labels `executor-preliminary`/`agent-written` to step 5 and AC bullet 3.
Diff intent: Step 5 log format becomes: `debug_log(f"preliminary_result_write executor-preliminary path={'option_d' if _wrote_preliminary else 'agent-written/option_a_or_noop'}")`
AC bullet 3 becomes: "DEBUG log emits combined terminology with primary labels `executor-preliminary`/`agent-written` and parenthetical `option_d`/`option_a_or_noop`"

**B. Add PASS_NO_REPORT preservation to T03.05 (M4)**
Current issue: T03.05 acceptance criteria only cover test results.
Change: Add new AC bullet
Diff intent: Add after last AC bullet: "`PhaseStatus.PASS_NO_REPORT` remains in the enum and is reachable via direct classifier invocation (SC-010, NFR-004)"

**C. Name ordered calls in T03.02 (L4)**
Current issue: AC bullet 1 says "Three function calls identified with line numbers"
Change: Name the calls explicitly
Diff intent: "Three function calls identified with line numbers in `execute_sprint()`" -> "Three calls identified in `execute_sprint()`: `_write_preliminary_result()`, `_determine_phase_status()`, `_write_executor_result_file()` -- with line numbers confirming strict sequential ordering"

### 4) phase-4-tasklist.md

#### Section/heading to change
- T04.02 Acceptance Criteria

#### Planned edits

**A. Add OQ-001 verification (M5)**
Current issue: AC only checks section ordering and as_posix() path.
Change: Add new AC bullet
Diff intent: Add after last AC bullet: "Attribute name used in `build_prompt()` for phase access confirmed to match `ClaudeProcess.__init__` (OQ-001 verification from M0)"
