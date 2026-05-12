# QA Report -- Task Qualitative Review (E2E Pipeline Verification)

**Topic:** TASK-E2E-20260402-prd-pipeline-rerun
**Date:** 2026-04-02
**Phase:** task-qualitative
**Fix cycle:** 1
**Fix authorization:** true

---

## Overall Verdict: PASS (after in-place fixes)

3 issues found and fixed in-place. No remaining issues.

---

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Gate/command dry-run | PASS | Verified bash commands reference existing CLI flags (--prd-file, --tdd-file, --input-type in commands.py lines 106-132), correct paths (test fixtures verified at .dev/test-fixtures/), and correct uv run prefix throughout all 67 items. |
| 2 | Project convention compliance | PASS | All items use `uv run superclaude` (never bare `superclaude`). Source edits target src/superclaude/ per CLAUDE.md rules. Test file exists at tests/cli/test_tdd_extract_prompt.py. |
| 3 | Intra-phase execution order simulation | PASS | Phase 1 items 1.1-1.7 are independent (read task, create dirs, verify CLI, run tests, verify sync, check fixtures, run new tests). Phase 2: 2.1 creates fixture before 2.2 checks it and 2.3 runs detection. Phase 3: 3.1-3.4, 3.6-3.8 are independent dry-runs; 3.5 reviews results last (correct despite out-of-order numbering). Phase 4: 4.1 runs pipeline before 4.2-4.9b check outputs. No dependency violations found. |
| 4 | Function signature verification | PASS | Verified: detect_input_type(spec_file: Path) -> str at executor.py:63. _route_input_files(input_files, explicit_tdd, explicit_prd, explicit_input_type) at executor.py:188. build_tasklist_generate_prompt(roadmap_file, tdd_file=None, prd_file=None) at tasklist/prompts.py:151. build_tasklist_fidelity_prompt(roadmap_file, tasklist_dir, tdd_file=None, prd_file=None) at tasklist/prompts.py:17. build_spec_fidelity_prompt(spec_file, roadmap_path, tdd_file=None, prd_file=None) at prompts.py:661. All match task descriptions. |
| 5 | Module context analysis | PASS | Verified tasklist/prompts.py imports _OUTPUT_FORMAT_BLOCK from roadmap.prompts (line 14). Both fidelity and generate prompts append this block. Item 7.5's inline Python test correctly exercises all 4 argument combinations. |
| 6 | Downstream consumer analysis | PASS | Extraction output consumed by generate, diff, debate, score, merge steps. EXTRACT_TDD_GATE (19 fields) at gates.py:797 enforces frontmatter for TDD path. EXTRACT_GATE (13 fields) at gates.py:765 for spec path. State file fields (tdd_file, prd_file, input_type) at executor.py:1897-1899 consumed by resume auto-wire logic at executor.py:2201-2230 and tasklist auto-wire at tasklist/commands.py:115-158. |
| 7 | Test validity | PASS | Item 7.5 exercises build_tasklist_generate_prompt with 4 distinct scenarios (none, tdd_only, prd_only, both) and checks for specific substring presence/absence. Items 2.2 uses sentinel greps with specific expected counts. Item 1.7 runs 23 actual unit tests across 5 test classes (verified by --collect-only). |
| 8 | Test coverage of primary use case | PASS | The task covers both primary paths (TDD+PRD in Phase 4, spec+PRD in Phase 5) end-to-end through the full pipeline. Phase 3 dry-runs verify flag acceptance before committing to 30-60 min pipeline runs. Phase 6 tests auto-wire. Phase 7 tests validation enrichment. Phase 8-9 provide cross-run comparison. |
| 9 | Error path coverage | PASS | Item 3.4 tests redundancy guard (TDD+TDD). Item 2.3 tests PRD-as-sole-input rejection (verified "PRD cannot be the sole primary input" at executor.py:243). Item 1.3 tests --input-type prd rejection. Item 6.4 tests graceful degradation when auto-wired file path does not exist. Item 6.5 tests no-state-file scenario. |
| 10 | Runtime failure path trace | PASS | The pipeline trace from input through extract -> generate x2 -> diff -> debate -> score -> merge -> anti-instinct -> test-strategy -> spec-fidelity -> wiring-verification is correctly described. Known failure point (anti-instinct gate) is documented as expected. Items account for downstream steps being skipped when anti-instinct halts pipeline (items 4.8, 4.9, 5.6 all say "if not produced, note SKIPPED"). |
| 11 | Completion scope honesty | PASS | Open Questions are tracked: AI-1 (anti-instinct impact) deferred to Phase 9, TG-1 (tasklist generation limitation) documented as known limitation with explanation in Phase 7, AW-1 marked RESOLVED with code evidence, RG-1 marked UPDATED. Deferred Work items are honest about what cannot be tested (tasklist generate CLI, anti-instinct fix). |
| 12 | Ambient dependency completeness | PASS | All required directories, fixtures, and output paths are addressed. Phase 1 creates directories (1.2), verifies fixtures (1.6), verifies sync (1.5), and runs tests (1.4, 1.7) before proceeding. Phase 2 creates the PRD fixture before Phase 3 dry-runs use it. |
| 13 | Kwarg sequencing red flags | PASS | Item 7.5 correctly uses keyword arguments (tdd_file=p, prd_file=p) matching the function signature. No items pass positional args where kwargs are required. |
| 14 | Function existence claims require verification | PASS (after fix) | Verified via grep: detect_input_type at executor.py:63, _route_input_files at executor.py:188, build_tasklist_fidelity_prompt at tasklist/prompts.py:17, build_tasklist_generate_prompt at tasklist/prompts.py:151, build_spec_fidelity_prompt at prompts.py:661, EXTRACT_TDD_GATE at gates.py:797, EXTRACT_GATE at gates.py:765. All exist at claimed locations. |
| 15 | Cross-reference accuracy for templates | PASS | Verified TDD fidelity checks reference S15, S19, S10, S7, S8 which correspond to actual TDD template sections. PRD fidelity checks reference S7 (User Personas), S19 (Success Metrics), S12/S22 (Scope/Journey), S5 (Business Context). Spec-fidelity dims 7-11 are conditional on tdd_file (confirmed at prompts.py:714). PRD dims 12-15 are conditional on prd_file (confirmed at prompts.py:750). |

---

## Issues Found

| # | Severity | Location | Issue | Required Fix | Status |
|---|----------|----------|-------|-------------|--------|
| 1 | IMPORTANT | Item 3.4 | Incorrect claim that "same-file guard should trigger a UsageError." Code analysis shows: step 10 redundancy guard fires first (executor.py:292-296), nullifies tdd_file to None, then step 11 same-file guard sees tdd_file=None and does not trigger. Command succeeds with a warning, not a UsageError. Also claims "redundancy guard moved to execute_roadmap (C-111 fix)" but it is actually in _route_input_files() at step 10. | Rewrite item 3.4 to expect redundancy guard warning ("Ignoring --tdd-file") and successful completion, not UsageError. Correct location reference. | FIXED in-place |
| 2 | IMPORTANT | Item 1.3 | Negative test for --input-type prd uses `--help` flag: `uv run superclaude roadmap run --input-type prd --help`. Click processes --help before validating other options, so this would display help text and exit 0 instead of producing the expected invalid choice error. | Remove --help from the negative test command; use `--dry-run` with a valid input file instead. | FIXED in-place |
| 3 | MINOR | Item 3.6 | Parenthetical "(redundancy guard nullifies supplementary TDD when primary is TDD)" is misleading. In the two-file positional case, tdd_file was never set -- TDD becomes primary via spec_file slot (step 7), and supplementary tdd_file stays None. The redundancy guard is not involved. | Correct parenthetical to explain actual routing behavior. | FIXED in-place |
| 4 | MINOR | Line 79 (Pipeline Code) | States "redundancy guard (moved to execute_roadmap per C-111)" but the guard is in _route_input_files() at step 10. | Correct location reference. | FIXED in-place |

---

## Actions Taken

1. **Fixed item 3.4** -- Rewrote expected behavior from "same-file guard UsageError" to "redundancy guard warning + successful completion." Corrected location from "execute_roadmap" to "_route_input_files() step 10." Specified the exact warning message ("Ignoring --tdd-file: primary input is already a TDD document.") and its delivery mechanism (Python logging to stderr).

2. **Fixed item 1.3** -- Changed negative test command from `--input-type prd --help` to `--input-type prd .dev/test-fixtures/test-spec-user-auth.md --dry-run` with explanatory note about Click's --help processing order.

3. **Fixed item 3.6** -- Changed misleading parenthetical from "redundancy guard nullifies supplementary TDD when primary is TDD" to "TDD-as-primary assigns TDD to spec_file slot; supplementary tdd_file is never set because no second TDD file was detected."

4. **Fixed Pipeline Code description (line 79)** -- Changed "redundancy guard (moved to execute_roadmap per C-111)" to "redundancy guard (step 10 in _route_input_files() -- nullifies tdd_file when input_type is tdd)."

All fixes verified by re-reading the edited file.

---

## Confidence Gate

**Confidence:** Verified: 15/15 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%

**Tool engagement:** Read: 18 | Grep: 16 | Glob: 0 | Bash: 4

Every checklist item was verified with at least one tool call:
- [x] 1: Read commands.py (full), grep for CLI flags, bash to check fixture files exist
- [x] 2: Read CLAUDE.md rules, verified uv run usage, bash to check test file exists
- [x] 3: Read all 11 phases sequentially, traced dependency chains
- [x] 4: Grep for all function signatures across executor.py, prompts.py, tasklist/prompts.py, gates.py
- [x] 5: Read tasklist/prompts.py:14 for _OUTPUT_FORMAT_BLOCK import, read function bodies
- [x] 6: Grep for EXTRACT_TDD_GATE (gates.py:797, 19 fields), EXTRACT_GATE (gates.py:765, 13 fields), state file fields (executor.py:1897-1899), auto-wire logic (executor.py:2201-2230, tasklist/commands.py:115-158)
- [x] 7: Bash collect-only to count 23 tests across 5 classes, read sentinel grep patterns
- [x] 8: Read full task phases 3-9 to verify E2E coverage of both paths
- [x] 9: Grep for "PRD cannot be the sole primary input" (executor.py:243), read redundancy guard, read same-file guard
- [x] 10: Read _build_steps routing, read gate definitions, read known-failure documentation
- [x] 11: Read Open Questions section, Deferred Work section, Known Issues section
- [x] 12: Read phase 1 items for prerequisite checking, phase 2 for fixture creation
- [x] 13: Read item 7.5 Python one-liner, verified kwarg usage matches function signature
- [x] 14: Grep for all claimed functions with -A context to verify existence and location
- [x] 15: Read spec-fidelity prompt (prompts.py:660-769) to verify conditional dims 7-11 and PRD dims 12-15

---

## Self-Audit

1. **Factual claims independently verified:** 22 distinct claims verified against source code (function signatures, gate field counts, routing logic, conditional dimension inclusion, test class counts, CLI flag names, error messages, state file fields, auto-wire logic, redundancy guard behavior, same-file guard behavior).

2. **Specific files read/grepped:**
   - `src/superclaude/cli/roadmap/commands.py` (full file, 360 lines)
   - `src/superclaude/cli/roadmap/gates.py` (lines 1-400, EXTRACT_GATE and EXTRACT_TDD_GATE)
   - `src/superclaude/cli/roadmap/executor.py` (detect_input_type, _route_input_files, _save_state, auto-wire)
   - `src/superclaude/cli/roadmap/prompts.py` (build_spec_fidelity_prompt lines 660-769, tdd_file/prd_file conditionals)
   - `src/superclaude/cli/tasklist/prompts.py` (full file, fidelity and generate prompt builders)
   - `src/superclaude/cli/tasklist/commands.py` (--tdd-file, --prd-file flags, auto-wire logic)
   - `src/superclaude/cli/roadmap/models.py` (input_type Literal)
   - `tests/cli/test_tdd_extract_prompt.py` (test class names and counts via --collect-only)
   - `.dev/test-fixtures/test-prd-user-auth.md` (frontmatter for detection scoring)
   - `.dev/test-fixtures/test-tdd-user-auth.md` and `test-spec-user-auth.md` (existence check)

3. **Why trust 0 remaining issues:** All 4 issues found were independently verified against source code and fixed in-place with re-verification. The fixes correct factual claims about execution behavior (redundancy guard vs same-file guard ordering, Click --help processing semantics) that would have caused test item failures during execution. The remaining 63 items were verified against source code and found correct.

---

## Recommendations

- No blocking issues remain after fixes.
- The task is ready for execution.
- Note: item 3.4's redundancy guard warning uses Python logging (_log.warning), which outputs to stderr via Python's last-resort handler. If the executor does not see the warning in captured stderr, the fallback verification is that the command succeeds without error (the redundancy guard's effect is tdd_file=None, which is observable in the state file).

## QA Complete
