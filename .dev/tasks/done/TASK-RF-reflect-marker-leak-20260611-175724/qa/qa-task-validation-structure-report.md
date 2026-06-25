# QA Report — Task Integrity (Phase Structure Lens)

**Topic:** Fix reflect-wrapper marker leakage (strip marker from §6.1 step 5.5 verification subprocess only)
**Date:** 2026-06-11
**Phase:** task-integrity
**Fix cycle:** N/A

---

## Overall Verdict: FAIL

**Confidence:** Verified: 9/9 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
**Tool engagement:** Read: 9 attempts (5 content-bearing, 4 failed/empty-range/missing-path) | Grep: 0 dedicated (Bash grep used once because no dedicated Grep tool is available in this runtime) | Glob: 0 | Bash: 6 | tavily_search: 0 | tavily_extract: 0 | web_search_fallback: 0 | web_fetch_fallback: 0

## Items Reviewed
| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | YAML frontmatter complete + well-formed | FAIL | Parsed frontmatter with `uv run python`; YAML loads, but required task-integrity fields `created`, `template`, and `tracks` are absent while `created_date` exists instead. See task lines 0-60 and parser output. |
| 2 | Mandatory Template-02 sections present | FAIL | Read Template 02 Part 2 headings from `.claude/templates/workflow/02_mdtm_template_complex_task.md` lines 1159-1443 and target task lines 62-333. Target has overview/objectives/prereqs/execution context/detailed instructions/task log, but no `## Post-Completion Actions` section. |
| 3 | Phase ordering logical | FAIL | Target task phases appear in order at lines 152, 163, 177, and 194; implementation precedes sync/validation and QA follows. However dependency edges inside later phases are incomplete: Step 4.1 does not read the Step 2.3 deferral artifact when contract editing is deferred, and Step 4.12 references a second fix cycle without explicit repeat steps. |
| 4 | Anti-orphaning final order | PASS | Read lines 236-240 and confirmed by offset check: Step 4.14 precedes Step 4.15, and both occur before the final Task Log section. Status-to-Done is the last checklist item; POST reflect is penultimate. |
| 5 | Task Log present at bottom | PASS | Read lines 242-333: `## Task Log / Notes` is present after all checklist items with Task Summary, Execution Log, phase findings, Phase Gate Findings, Follow-Up Items, and Deviations sections. |
| 6 | Final QA gate has >=6 report-only agents + serialized fix + verification | PASS | Read lines 199-218 and 221-228. Steps 4.2-4.7 define 3 `rf-qa` structural report-only agents and 3 `rf-qa-qualitative` report-only agents, each with specific embedded lens and `fix_authorization:false`; Step 4.9 is one serialized `rf-qa` fix agent with `fix_authorization:true`; Steps 4.10-4.11 are verification agents. Parser count confirmed 3+3 initial report-only agents and 8 total report/verification agents. |
| 7 | Validation items present and correctly ordered after implementation before QA | PASS | Read lines 177-192: Step 3.1 `make sync-dev`, Step 3.2 `make verify-sync`, Step 3.3 `uv run ruff format --check src/ tests/`, Step 3.4 `uv run ruff check src/ tests/`, and Step 3.5 `uv run pytest ...` occur after Phase 2 implementation lines 163-175 and before Phase 4 QA line 194. |
| 8 | POST reflect gate wrapper shell-out with skip guard and fallback | FAIL | Read Step 4.14 lines 236-237 and task-builder canonical POST pattern from `src/superclaude/skills/task-builder/SKILL.md` grep output around lines 2200-2202 and validation rule around 2260. Step 4.14 includes the guarded `superclaude reflect run ... --depth deep --fix --promote` command and skill-load-path fallback handling, but omits the canonical precondition to stage new task artifacts so the wrapper audits the complete diff. |
| 9 | Estimated item count reasonable and Open Questions documented | PASS | Parser output found 27 checklist items across phases 1-4, reasonable for a medium Template-02 task. Read lines 97-100: open questions/operator-awareness items are documented, including named-surface divergence, contract carve-out caution, and POST skill-load-path caveat. |

## Summary
- Checks passed: 4 / 9
- Checks failed: 5
- Critical issues: 1
- Important issues: 6
- Minor issues: 0
- Issues fixed in-place: 0 (fix_authorization: false)

## Issues Found
| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | CRITICAL | Frontmatter lines 0-60 | Frontmatter is well-formed YAML but incomplete for the task-integrity schema: `created`, `template`, and `tracks` are missing. The file has `created_date`, but the gate contract requires the mandatory fields to be present with non-empty values. | Add the required frontmatter fields, e.g. `created: "2026-06-11"`, `template: "02"`, and an appropriate non-empty `tracks:` value/list, or update the governing task-integrity schema if `created_date` is intended to supersede `created`. |
| 2 | IMPORTANT | Document structure; Template 02 Part 2 vs task lines 194-240 | Mandatory Template-02 post-completion structure is not represented as `## Post-Completion Actions`. The final actions are folded into Phase 4, which weakens template conformance and makes post-completion validation harder to identify mechanically. | Add a `## Post-Completion Actions` section before `## Task Log / Notes`, or explicitly justify this task-builder variant and ensure all I17 post-completion validation items are still present as checklist items before the status update. |
| 3 | IMPORTANT | Final completion gate, Step 4.15 lines 239-240 | I17 post-completion validation is incomplete. Before setting Done, the template requires validating all checklist items are marked, all specified output files exist, blockers have resolution notes, relevant tests pass, and final lens QA passed. Step 4.15 checks only POST summary and Task Summary, plus final QA/POST evidence. It does not explicitly verify all `- [ ]` items are complete or all expected output files exist. | Insert a pre-Done checklist item (or expand Step 4.15) to verify every checklist item is marked complete, every output path specified in checklist items exists, blocker entries have resolution notes, source tests passed, and final QA/POST evidence exists before any Done transition. |
| 4 | IMPORTANT | QA fix-cycle control, Step 4.12 lines 230-231 | Step 4.12 mentions halting after two standard-intensity fix cycles, but the task encodes only one consolidation → fix → verification path. Template I16/I20 requires explicit cycle-control logic; if verification fails, the task must repeat from consolidation with new/unfixed findings up to the max cycle count. | Add explicit IF/ELSE cycle-control instructions or additional checklist items that re-enter consolidation/fix/verification for cycle 2, preserving serialized fix authorization and verification before halting/escalating. |
| 5 | IMPORTANT | Status protocol line 143 vs Step 4.15 line 240 | Blocked status is internally inconsistent: the frontmatter update protocol says use `⚪ Blocked`, while the final Step 4.15 says use `🔴 Blocked`. This can cause executor drift and invalid status transitions. | Normalize every blocked-status instruction to the template-supported value. Based on the template status options, use `🔴 Blocked` consistently unless the project schema has intentionally changed. |
| 6 | IMPORTANT | Step 4.1 line 197 and Step 2.3 line 172 | Contract carve-out deferral is not wired into the final aggregation dependency. Step 2.3 allows creating `phase-outputs/plans/contract-carveout-deferral.md`, but Step 4.1 reads the contract if present and test-result summaries; it does not explicitly read the deferral artifact before claiming contract edit or deferral status. | Update Step 4.1 to read `phase-outputs/plans/contract-carveout-deferral.md` when present and include that artifact in the final-output-summary evidence trail. |
| 7 | IMPORTANT | POST reflect Step 4.14 line 237 vs task-builder canonical pattern | The POST reflect shell-out omits the canonical staging precondition from the task-builder wrapper pattern: new task artifacts must be staged so the wrapper audits the complete diff. Without this, the POST gate can pass while omitting never-`git add`-ed files such as new regression tests or task-local artifacts. | Add a safe staging precondition for allowed paths only, explicitly excluding forbidden `.claude/` mirrors, before invoking `superclaude reflect run ... --depth deep --fix --promote`. |

## Actions Taken
- Created this QA report at `/config/workspace/IronClaude/.claude/worktrees/ReflectGateWiring/.dev/tasks/to-do/TASK-RF-reflect-marker-leak-20260611-175724/qa/qa-task-validation-structure-report.md` with an immediate header, then appended verified findings incrementally.
- No task file modifications were made because `fix_authorization: false`.

## Recommendations
- Do not execute this MDTM task until the CRITICAL frontmatter schema issue is fixed.
- Fix the IMPORTANT structural issues before handing to an executor: add/restore post-completion validation, encode cycle-2 control, normalize blocked status, wire contract-deferral evidence, and add the POST wrapper staging precondition.
- Re-run task-integrity QA after fixes, with special attention to Template-02 conformance and anti-orphaning.

## QA Complete

VERDICT: FAIL
