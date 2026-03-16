---
high_severity_count: 3
medium_severity_count: 7
low_severity_count: 4
total_deviations: 14
validation_complete: true
tasklist_ready: false
---

## Deviation Report

### DEV-001
- **ID**: DEV-001
- **Severity**: HIGH
- **Deviation**: Roadmap places preflight executor in a new file `preflight.py` instead of spec-mandated `executor.py`
- **Spec Quote**: "Modified Files: `src/superclaude/cli/sprint/executor.py` — Add `execute_preflight_phases()` function; modify `execute_sprint()` to call preflight and skip non-claude phases"
- **Roadmap Quote**: "Files created: `src/superclaude/cli/sprint/preflight.py` — `execute_preflight_phases()` core logic"
- **Impact**: The spec explicitly places `execute_preflight_phases()` inside the existing `executor.py`. The roadmap creates a new file `preflight.py` instead. This contradicts the spec's architecture section (§4.2) and module dependency graph (§4.4), which show `executor.py (MODIFIED)` — not a new module. Implementers following the roadmap will create a file the spec doesn't call for and miss the required modification to `executor.py`.
- **Recommended Correction**: Move `execute_preflight_phases()` back into `executor.py` as the spec requires, or explicitly justify the deviation and update the spec's architecture section to match.

### DEV-002
- **ID**: DEV-002
- **Severity**: HIGH
- **Deviation**: Roadmap modifies `process.py` for sprint integration instead of spec-mandated `executor.py`
- **Spec Quote**: "Modified Files: `src/superclaude/cli/sprint/executor.py` — modify `execute_sprint()` to call preflight and skip non-claude phases"
- **Roadmap Quote**: "Files modified: `src/superclaude/cli/sprint/process.py` — Add preflight call + skip logic in `execute_sprint()`"
- **Impact**: The spec's architecture (§4.2, §4.4) clearly states `executor.py` contains `execute_sprint()` and is the file to modify. The roadmap targets `process.py` instead. If `execute_sprint()` actually lives in `process.py`, the spec is wrong and should be corrected; if it lives in `executor.py`, the roadmap is wrong. Either way, they disagree on where the core integration point is.
- **Recommended Correction**: Verify which file contains `execute_sprint()` and align both documents. The roadmap must match the spec's file references or the spec must be updated.

### DEV-003
- **ID**: DEV-003
- **Severity**: HIGH
- **Deviation**: Roadmap changes classifier return values from spec-defined labels
- **Spec Quote**: "Returns classification label string (e.g., `'WORKING'`, `'BROKEN'`, `'CLI FAILURE'`)" and "`empirical_gate_v1`: lambda ... `'CLI FAILURE'` if exit_code != 0 else `'WORKING'` if `'PINEAPPLE'` in stdout else `'BROKEN'`"
- **Roadmap Quote**: "Returns classification label (e.g., `'pass'`, `'fail'`)" and "Classifier exceptions caught, logged at WARNING, return `'error'` classification"
- **Impact**: The spec defines specific label strings (`WORKING`, `BROKEN`, `CLI FAILURE`) for `empirical_gate_v1` with exact logic. The roadmap describes generic `pass`/`fail` labels, which contradicts the spec's classifier contract (§4.5, §5.2) and would break any downstream code or tests that depend on the spec-defined labels.
- **Recommended Correction**: Restore the spec-defined labels (`WORKING`, `BROKEN`, `CLI FAILURE`) in the roadmap's classifier description. The `error` label for exception handling is a valid addition (per GAP-03) but must not replace the spec's labels.

### DEV-004
- **ID**: DEV-004
- **Severity**: MEDIUM
- **Deviation**: Roadmap adds a validation rule not in the spec (empty command in python-mode tasks)
- **Spec Quote**: "Tasks without a `**Command:**` field have `command == ''`" (FR-PREFLIGHT.3). No validation rule requiring commands in python-mode phases.
- **Roadmap Quote**: "Add explicit validation for python-mode tasks with empty commands — If a phase has `execution_mode == 'python'` and any task has `command == ''`, raise `click.ClickException`"
- **Impact**: The spec allows empty commands on tasks without specifying what happens when a python-mode phase contains such tasks. The roadmap adds a fail-fast validation. This is a reasonable addition (likely from adversarial review) but is not in the spec and could reject valid tasklists if a python-mode phase intentionally has tasks without commands (e.g., documentation tasks grouped with shell tasks).
- **Recommended Correction**: Either add this validation to the spec as an explicit acceptance criterion under FR-PREFLIGHT.2 or FR-PREFLIGHT.3, or document it as a roadmap-originated enhancement.

### DEV-005
- **ID**: DEV-005
- **Severity**: MEDIUM
- **Deviation**: Roadmap places model changes in `config.py` instead of spec-mandated `models.py`
- **Spec Quote**: "Modified Files: `src/superclaude/cli/sprint/models.py` — Add `execution_mode: str` to `Phase`; add `command: str`, `classifier: str` to `TaskEntry`; add `PREFLIGHT_PASS` to `PhaseStatus`"
- **Roadmap Quote**: "Files modified: `src/superclaude/cli/sprint/config.py` (or model file) — Extend `Phase`, `TaskEntry` dataclasses"
- **Impact**: The spec explicitly names `models.py` as the location for dataclass and enum changes. The roadmap hedges with "config.py (or model file)", creating ambiguity. Implementers may put model changes in the wrong file.
- **Recommended Correction**: Use the spec's explicit `models.py` reference. Remove the ambiguous parenthetical.

### DEV-006
- **ID**: DEV-006
- **Severity**: MEDIUM
- **Deviation**: Roadmap omits `config.py` from its modified files list
- **Spec Quote**: "Modified Files: `src/superclaude/cli/sprint/config.py` — Extend `discover_phases()` to parse Execution Mode column; extend `parse_tasklist()` to extract `**Command:**` and `| Classifier |`"
- **Roadmap Quote**: Files modified list includes only `config.py (or model file)` for dataclass changes and `process.py` for sprint integration. No entry for parser extensions in `config.py`.
- **Impact**: The spec requires `config.py` to be modified for parser extensions (`discover_phases()`, `parse_tasklist()`). The roadmap's Phase 1 narrative describes these changes but the Resource Requirements file list doesn't clearly call out `config.py` as a modified file for parsing work.
- **Recommended Correction**: Add `config.py` explicitly to the modified files table for parser extensions (`discover_phases()`, `parse_tasklist()`).

### DEV-007
- **ID**: DEV-007
- **Severity**: MEDIUM
- **Deviation**: Roadmap test file path differs from spec
- **Spec Quote**: "New Files: `tests/sprint/test_preflight.py` — Unit/integration tests" and "`tests/sprint/test_classifiers.py`"
- **Roadmap Quote**: "Files created: `tests/cli/sprint/test_preflight.py` — Unit + integration tests"
- **Impact**: The spec uses `tests/sprint/` while the roadmap uses `tests/cli/sprint/`. Implementers following the roadmap will create tests in a different directory than the spec specifies. Additionally, the roadmap doesn't list `test_classifiers.py` as a separate file.
- **Recommended Correction**: Align test file paths between spec and roadmap. Verify the actual test directory structure and use the correct path in both documents. Add `test_classifiers.py` to the roadmap's file list.

### DEV-008
- **ID**: DEV-008
- **Severity**: MEDIUM
- **Deviation**: Roadmap adds OQ-004 (`--phases` filter interaction) not mentioned in spec
- **Spec Quote**: No mention of `--phases` flag interaction with preflight anywhere in the spec.
- **Roadmap Quote**: "OQ-004 (--phases filter): Respect `--phases` for preflight phases too. If `--phases 2,3` excludes Phase 1, preflight skips it. Consistent behavior."
- **Impact**: This is a valid operational concern but represents a new requirement not present in the spec. Without spec coverage, there are no acceptance criteria for this behavior.
- **Recommended Correction**: Add `--phases` filter interaction as an acceptance criterion under FR-PREFLIGHT.2 or as a new FR-PREFLIGHT.9.

### DEV-009
- **ID**: DEV-009
- **Severity**: MEDIUM
- **Deviation**: Roadmap adds OQ-005 ordering constraint not in spec
- **Spec Quote**: The spec states preflight runs "before the main Claude-subprocess loop begins" (§2) but does not discuss ordering as a formal constraint or open question.
- **Roadmap Quote**: "OQ-005 (ordering constraint): Implement python-first ordering but do not document as a guaranteed contract. Flag for stakeholder confirmation before enshrining as permanent behavior."
- **Impact**: The roadmap introduces a new open question about ordering semantics that the spec considers settled by design ("pre-sprint hook"). This could delay implementation if stakeholder input is required.
- **Recommended Correction**: The spec's design (§2.1, §2.2) clearly establishes python-first as the architecture. Either confirm this resolves OQ-005 or escalate to the spec for clarification.

### DEV-010
- **ID**: DEV-010
- **Severity**: MEDIUM
- **Deviation**: Roadmap omits `--dry-run` interaction from functional requirements
- **Spec Quote**: "GAP-02: `--dry-run` should list python-mode phases with '[preflight]' annotation. Trivial to add in `_print_dry_run()`. Can be addressed during implementation."
- **Roadmap Quote**: "OQ-002 (dry-run interaction): List python-mode phases with `[preflight]` tag in dry-run output. Low effort, high clarity. Resolved."
- **Impact**: The roadmap marks this as "Resolved" in the OQ table but does not include it as a task or deliverable in any phase. There is no phase step or test for dry-run preflight display.
- **Recommended Correction**: Add a task in Phase 4 (Sprint Integration) to implement `[preflight]` annotation in dry-run output, and add a corresponding test.

### DEV-011
- **ID**: DEV-011
- **Severity**: LOW
- **Deviation**: Spec lists 3 new files, roadmap lists 3 but with different names/groupings
- **Spec Quote**: "New Files: `classifiers.py`, `tests/sprint/test_preflight.py`, `tests/sprint/test_classifiers.py`"
- **Roadmap Quote**: "Files created: `classifiers.py`, `preflight.py`, `tests/cli/sprint/test_preflight.py`"
- **Impact**: The roadmap adds `preflight.py` (not in spec) and omits `test_classifiers.py` (in spec) from the explicit file list, though classifier tests are described in Phase 2's test section narratively.
- **Recommended Correction**: Align file lists. Either consolidate classifier tests into `test_preflight.py` with a note, or list `test_classifiers.py` explicitly.

### DEV-012
- **ID**: DEV-012
- **Severity**: LOW
- **Deviation**: Roadmap test counts don't match spec
- **Spec Quote**: §8.1 lists 14 unit tests; §8.2 lists 8 integration tests
- **Roadmap Quote**: "14 unit + 8 integration tests passing" (Phase 5) — matches counts but the individual tests listed across phases don't fully align with spec's test table
- **Impact**: Minor — the totals match but individual test names and groupings differ slightly. No functional impact if all spec-required test scenarios are covered.
- **Recommended Correction**: Cross-check that every test in spec §8.1 and §8.2 has a corresponding test in the roadmap phases.

### DEV-013
- **ID**: DEV-013
- **Severity**: LOW
- **Deviation**: Roadmap uses "Small/Medium" estimates instead of spec's LOC/task counts
- **Spec Quote**: "Estimated complexity: moderate (~400 LOC new code + ~200 LOC tests)" and §10 provides specific task counts per phase
- **Roadmap Quote**: "Phase 1: Small, Phase 2: Small, Phase 3: Medium, Phase 4: Small-Medium, Phase 5: Small"
- **Impact**: Cosmetic difference in estimation granularity. No functional impact.
- **Recommended Correction**: None required; both approaches are valid.

### DEV-014
- **ID**: DEV-014
- **Severity**: LOW
- **Deviation**: Spec §4.1 mentions `tests/sprint/test_classifiers.py` as a new file; roadmap doesn't list it separately
- **Spec Quote**: "New Files: `tests/sprint/test_classifiers.py` — Unit tests for classifier functions"
- **Roadmap Quote**: Classifier tests are described under Phase 2 tests section but no separate test file is listed in the resource requirements
- **Impact**: Minor organizational difference. Tests may be in a separate file or combined.
- **Recommended Correction**: List `test_classifiers.py` explicitly in the roadmap's file creation table, or note that classifier tests are included in `test_preflight.py`.

## Summary

**Severity Distribution:**
- **HIGH: 3** — File location mismatches (DEV-001, DEV-002) and classifier label contradictions (DEV-003)
- **MEDIUM: 7** — Undocumented additions (DEV-004, DEV-008, DEV-009), file path ambiguities (DEV-005, DEV-006, DEV-007), and missing implementation steps (DEV-010)
- **LOW: 4** — File list inconsistencies and cosmetic differences (DEV-011 through DEV-014)

**Key Findings:**

The three HIGH-severity deviations center on two themes:

1. **File location disagreements** (DEV-001, DEV-002): The spec places all preflight logic in `executor.py` and models in `models.py`. The roadmap introduces a new `preflight.py` file and targets `process.py` for integration. This is the most critical divergence — it means the roadmap's architecture doesn't match the spec's module dependency graph. This likely reflects the roadmap authors discovering that `execute_sprint()` actually lives in `process.py`, not `executor.py`, which would mean the *spec* needs correction.

2. **Classifier contract mismatch** (DEV-003): The spec defines specific label strings (`WORKING`, `BROKEN`, `CLI FAILURE`) with exact logic for `empirical_gate_v1`. The roadmap generifies these to `pass`/`fail`, breaking the classifier contract.

**Recommendation:** Resolve the three HIGH-severity items before generating a tasklist. The file location issues (DEV-001, DEV-002) likely require checking the actual codebase to determine which document is correct, then aligning both. The classifier labels (DEV-003) should be restored to match the spec.
