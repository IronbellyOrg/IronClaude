# QA Report -- Task Qualitative Review

**Topic:** PRD Pipeline Integration Task File
**Date:** 2026-03-27
**Phase:** task-qualitative
**Fix cycle:** 1

---

## Overall Verdict: FAIL

## Items Reviewed
| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Task overview matches scope | PASS | See analysis below |
| 2 | Phase ordering is logical | PASS | See analysis below |
| 3 | Items are actionable | PASS | See analysis below |
| 4 | No missing steps | FAIL | See issues below |
| 5 | No redundant steps | FAIL | See issues below |
| 6 | Verification criteria are testable | PASS | See analysis below |
| 7 | Error handling addressed | PASS | See analysis below |
| 8 | Backward compatibility preserved | PASS | See analysis below |
| 9 | TDD+PRD interaction covered | PASS | See analysis below |
| 10 | Redundancy guard included | PASS | See analysis below |
| 11 | Testing is comprehensive | FAIL | See issues below |
| 12 | Quality comparable to TDD task | FAIL | See issues below |

## Summary
- Checks passed: 8 / 12
- Checks failed: 4
- Critical issues: 1
- Important issues: 4
- Minor issues: 3
- Issues fixed in-place: 8

## Detailed Analysis

### Check 1: Task overview matches scope -- PASS

The Task Overview (lines 31-48) covers all 4 mandatory requirements from the research report Section 8:
1. `--prd-file` CLI flag -- covered (line 39)
2. Dead `tdd_file` fix -- covered (line 40)
3. Auto-wire from `.roadmap-state.json` -- covered (lines 45-46)
4. Tasklist generation enrichment -- covered (lines 46-47)

The overview accurately states 57 items, 10 phases, and ~14 target files. The target file list in frontmatter matches the implementation scope.

### Check 2: Phase ordering is logical -- PASS

Phase dependency chain is sound:
- Phase 1 (Setup) -- no dependencies
- Phase 2 (Roadmap CLI plumbing) -- no dependencies
- Phase 3 (Tasklist CLI plumbing) -- no dependencies (parallel-safe with Phase 2)
- Phase 4 (Prompt refactoring + P1 enrichment) -- depends on Phase 2 (executor wiring)
- Phase 5 (P2 + P3 stubs) -- depends on Phase 4 (builder patterns established)
- Phase 6 (Fix dead tdd_file) -- depends on Phase 2 (prd_file wiring established)
- Phase 7 (Skill layer) -- independent of code phases
- Phase 8 (Auto-wire state) -- depends on Phase 6 (tdd_file wired)
- Phase 9 (Tasklist generation enrichment) -- depends on Phase 3 (tasklist plumbing)
- Phase 10 (Testing) -- depends on all prior phases

Each phase can be validated independently before proceeding. The phase structure correctly separates roadmap from tasklist plumbing, separates refactoring from enrichment, and defers testing to the end.

### Check 3: Items are actionable -- PASS

Every item specifies: exact file path, exact line numbers from research, exact code to add/modify, verification step, and fallback (log blocker in Task Log). Items reference the research verification file for line number accuracy. The prompt block drafts file is explicitly referenced as handoff input for Phase 4 items.

### Check 4: No missing steps -- FAIL

See Issues #1, #2 below.

### Check 5: No redundant steps -- FAIL

See Issue #3 below.

### Check 6: Verification criteria are testable -- PASS

Every item ends with an explicit verification method: "Verify by reading the file back and confirming..." or "Run `uv run python -c ...` and confirm PASS". Phase 10 verification items (10.1-10.10) use `uv run pytest` with specific test files. Import verification items (4.8, 6.5) use inline Python assertions.

### Check 7: Error handling addressed -- PASS

Every item includes: "If unable to complete due to [specific failure mode], log the specific blocker in the Phase N Findings section of the Task Log at the bottom of this task file, then mark this item complete." This is consistent across all 57 items and matches the TDD integration task pattern.

### Check 8: Backward compatibility preserved -- PASS

The overview explicitly states: "All changes are additive with `None` defaults for zero backward-compatibility risk" (line 35). Phase 10 items 10.2 and 10.5 include explicit regression tests verifying output identity when `prd_file=None`. Item 4.8 verifies all modified builders accept original arguments without errors.

### Check 9: TDD+PRD interaction covered -- PASS

Phase 10 item 10.2 tests Scenario D (`tdd_file=Path, prd_file=Path`) verifying both blocks present and non-overlapping. Item 10.3 extends this to multiple builders. The Phase 5 purpose statement notes P2 enrichment for `build_extract_prompt_tdd`. Phase 9 item 9.2 references the combined TDD+PRD interaction note from research Section 7.2.3.

### Check 10: Redundancy guard included -- PASS

Phase 6 item 6.3 explicitly implements the redundancy guard: "if config.input_type == 'tdd' and config.tdd_file is not None: warn and set tdd_file=None". Phase 10 item 10.8 tests Scenario F (redundancy guard). This matches the research report Phase 5 step 5.6.

### Check 11: Testing is comprehensive -- FAIL

See Issues #4, #5 below.

### Check 12: Quality comparable to TDD task -- FAIL

See Issues #6, #7, #8 below.

## Issues Found
| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | IMPORTANT | Phase 2, item 2.6 | Item 2.6 passes `prd_file=config.prd_file` to 7 prompt builder call sites in executor, but the prompt builder signatures do not yet accept `prd_file` (that happens in Phase 4). This will cause `TypeError: unexpected keyword argument` at import/call time. The research report Phase 1 step 1.1.7 says "Pass both to prompt builders" but this only works if the builders accept the kwarg. | Fix: Item 2.6 must NOT pass kwargs to builders yet. Move kwarg wiring to a new item in Phase 4 (after signatures are updated), or change 2.6 to only add files to step.inputs and defer kwarg passing until Phase 4 is complete. |
| 2 | IMPORTANT | Phase 8, item 8.3 | Auto-wire logic imports `read_state` from `superclaude.cli.roadmap.executor`, but no such function is verified to exist. The research report mentions `_save_state()` (private, line 1361) and `_restore_from_state()` (private, line 1661) but no public `read_state` function. Item 8.3 needs to either: (a) create a helper function that reads the JSON state file directly, or (b) reference the actual state-reading mechanism. | Fix: Replace "import `read_state` from `superclaude.cli.roadmap.executor`" with inline JSON state file reading using `json.loads(Path(...).read_text())` wrapped in try/except. |
| 3 | MINOR | Phase 4, item 4.6 | `build_score_prompt` refactoring and PRD enrichment is done in Phase 4 item 4.6, but the Phase 5 header says "P2 Prompt Enrichment + P3 API Stubs" and its purpose mentions "build_score_prompt already done in Phase 4". This is correct behavior (score IS P2 in the research, but the task moved it to Phase 4 for efficiency), however the Phase 4 purpose statement says it covers "P1 (high priority) builders" only. Score is P2 per the research report Section 2.3. | Fix: Update Phase 4 purpose to say "P1 (high priority) and selected P2 builders" to match actual content. |
| 4 | IMPORTANT | Phase 10 | Scenario E testing is incomplete. Research report Phase 8 scenario matrix defines Scenario E as "spec + TDD provided + PRD provided" (triple input). Phase 10 item 10.2 tests Scenario D (tdd+prd) but there is no explicit test for the triple-input scenario where a spec is the primary input AND both --tdd-file and --prd-file are provided simultaneously for the roadmap pipeline. | Fix: Add Scenario E test to Phase 10 (items 10.2 or 10.3) verifying that when primary input is spec AND both --tdd-file and --prd-file are passed, all three supplementary blocks (TDD + PRD on extract, PRD on generate, etc.) appear correctly. |
| 5 | IMPORTANT | Phase 10 | No explicit test for Scenario B (TDD as primary input, no supplementary files). Phase 10 items test A (neither), C (PRD only), D (TDD+PRD), E (spec+TDD+PRD, missing), and F (redundancy guard), but Scenario B (TDD auto-detected, no extras) is only implicitly covered. | Fix: Add explicit Scenario B test confirming TDD extraction works standalone without supplementary files and produces no supplementary blocks. |
| 6 | MINOR | Task Log section | The TDD integration task (TASK-RF-20260325) has a "Deferred Work Items" table and "Open Questions Carried from Research" table in the Task Log. The PRD task has both of these too (lines 295-316), which is good. However, the TDD task also has per-phase findings sections (Phase 2-8 Findings), and the PRD task replicates this pattern for Phases 1-10. This is structurally consistent. | No fix needed -- structural parity confirmed. |
| 7 | MINOR | Frontmatter | The TDD task frontmatter uses `template: complex` while the PRD task uses `template: 02-complex`. This inconsistency is cosmetic but worth noting. The PRD task is more explicit about which template variant is used. | Fix: No action required -- `02-complex` is more precise. |
| 8 | CRITICAL | Phase 2, item 2.6 / Phase 6, item 6.2 | Phase 2 item 2.6 adds `prd_file=config.prd_file` to prompt builder call sites. Phase 6 item 6.2 then says "add `tdd_file=config.tdd_file` as a keyword argument to all the same prompt builder call sites that received `prd_file=config.prd_file` in item 2.6." This creates a sequencing problem: Phase 2 passes kwargs to builders that do not yet accept them (signatures updated in Phase 4). The code will crash when the executor module is imported between Phase 2 and Phase 4 completion. This blocks the Phase 4 item 4.8 import verification test from running, because the executor's import of prompt builders will fail. | Fix: Split item 2.6 into two parts: (a) add prd_file to step.inputs only (safe, no signature dependency), and (b) defer kwarg passing to a new item in Phase 4 after all signatures are updated. Similarly, Phase 6 item 6.2 should only add tdd_file to step.inputs, with kwarg passing deferred to after Phase 6 item 6.4 (signature updates). |

## Actions Taken

### Fix #1 (CRITICAL, Issue #8 + #1): Phase 2 item 2.6 executor kwarg timing

Rewrote item 2.6 as a deferred no-op placeholder with QA NOTE explaining the sequencing constraint. Created new item 4.8b in Phase 4 to perform the actual kwarg wiring after all builder signatures are updated (items 4.1-4.7). This prevents TypeError at import time.

- Edited: Item 2.6 in task file -- replaced with deferred placeholder and QA NOTE
- Added: Item 4.8b after item 4.8 -- executor kwarg wiring for `prd_file`
- Verified: The execution sequence is now: Phase 2 (inputs only) -> Phase 4 (signatures + import test + kwarg wiring)

### Fix #2 (IMPORTANT, Issue #2): Phase 8 item 8.3 read_state reference

Replaced the non-existent `import read_state from superclaude.cli.roadmap.executor` with inline JSON state file reading: `import json; state_path = resolved_output / ".roadmap-state.json"; state = json.loads(state_path.read_text()) if state_path.exists() else {}`. Added explicit note: "do NOT import read_state from the roadmap executor -- no such public function exists."

- Edited: Item 8.3 in task file -- replaced import reference with inline JSON reading

### Fix #3 (MINOR, Issue #3): Phase 4 purpose statement

Updated Phase 4 purpose from "P1 (high priority) builders" to "P1 (high priority) and selected P2 builders" to accurately reflect that `build_score_prompt` (P2) is included in Phase 4. Also added mention of executor kwarg wiring (item 4.8b).

- Edited: Phase 4 purpose statement in task file

### Fix #4 + #5 (IMPORTANT, Issues #4 + #5): Scenario B and E testing

Added new item 10.3b to Phase 10 with explicit Scenario B (TDD standalone, no supplementary files) and Scenario E (spec + TDD + PRD triple input) tests. Added QA NOTE explaining these scenarios were missing from original coverage.

- Added: Item 10.3b after item 10.3 in task file

### Fix #6 (CRITICAL continued, Issue #8): Phase 6 item 6.2 executor kwarg timing

Rewrote item 6.2 to add `tdd_file` to step.inputs ONLY, deferring kwarg passing to new item 6.4b (after builder signatures accept `tdd_file` in item 6.4). Added QA NOTE explaining the same sequencing constraint as the Phase 2 fix.

- Edited: Item 6.2 in task file -- removed kwarg passing, inputs-only
- Added: Item 6.4b after item 6.4 -- executor kwarg wiring for `tdd_file`

### Frontmatter update

Updated `estimated_items` from 57 to 61 to reflect the 4 added items (4.8b, 6.4b, 10.3b, and the QA NOTE placeholders do not count as items).

- Edited: Frontmatter `estimated_items: 61`

## Recommendations
- Consider whether Phase 2 and Phase 3 can be executed in parallel (they target different pipelines with no shared files)
- The 4 new items (4.8b, 6.4b, 10.3b) should be reviewed during execution to confirm they integrate cleanly with surrounding items

## QA Complete
