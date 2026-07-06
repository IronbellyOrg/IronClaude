# QA Report — Task Integrity (B2 Self-Containment)

**Topic:** Implement Locked Detection Contract Setup Flow
**Date:** 2026-07-01
**Phase:** task-integrity
**Fix cycle:** N/A

---

## Overall Verdict: FAIL

This task file does **not** pass the B2 self-containment gate. The failures are systemic: checklist items are oversized batch prompts, agent-spawning items do not embed full prompts, completion gates allow items to be marked complete after blockers rather than after full completion, and several items use relative `.claude/` / `.dev/` references despite the absolute-path requirement.

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Task file read in full | PASS | Read `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-detection-contract-20260701-164700/TASK-RF-detection-contract-20260701-164700.md` lines 1-406. |
| 2 | Template B2 standard read | PASS | Read `/config/workspace/IronClaude/.claude/templates/workflow/02_mdtm_template_complex_task.md` lines 147-164; B2 requires context, action, exact output, ensuring-clause verification, failure-only evidence, and explicit completion gate. |
| 3 | Checklist inventory | PASS | `uv run python` counted 50 checklist items at lines 147, 151, 155, 159, 163, 167, 171, 173, 175, 177, 179, 187, 191, 195, 199, 203, 207, 211, 215, 219, 223, 225, 227, 235, 239, 243, 247, 251, 253, 255, 263, 267, 271, 275, 279, 283, 287, 291, 295, 297, 299, 307, 311, 315, 317, 321, 323, 327, 331, 335. |
| 4 | B2 context/action/output/verification/completion per checklist item | FAIL | All 50 items have an action and some location/output, but the completion-gate wording conflicts with B2. Several items also lack explicit context WHY wording; automated keyword pass flagged lines 187, 195, 199, 207, 211, 215, 255, 271, 275, 279, 299, 307, 323, 335 for missing `because`/equivalent reason clauses. |
| 5 | No batch items | FAIL | Multiple checklist items combine independent actions: line 215 creates two modules; line 227 consolidates reports, spawns a fix agent, and spawns verification agents; line 271 creates two test files; line 291 runs two validations and writes three artifacts; line 331 stages files and runs reflect. |
| 6 | Fully embedded agent prompts | FAIL | Agent-spawning items at lines 171, 173, 223, 225, 251, 253, 295, 297, 315, 321 specify mode/lens/output, but do not embed full standalone prompts/checklists; several use shorthand such as “each with adversarial framing” or “writing reports under ...”. |
| 7 | Absolute paths | FAIL | Most concrete source/output paths are absolute, but several checklist items use relative path tokens as operative locations or constraints: `.claude/`, `.claude/commands/`, `.claude/skills/`, `.dev/pr-monitor/detection-contract.locked.md`, and `.claude/settings.json` appear in checklist items without absolute equivalents. |
| 8 | No `[CODE-CONTRADICTED]` / `[UNVERIFIED]` as implementation facts | PASS | `uv run python` scan found zero `[CODE-CONTRADICTED]` or `[UNVERIFIED]` tags in the task file; research scan found zero such tags across `01-file-inventory.md`, `02-patterns-integration.md`, `03-validation-tests.md`, and `04-template-examples.md`. |
| 9 | B2 one-paragraph checklist shape | PASS with concern | Every checklist item is a single physical paragraph beginning with `- [ ]`, but many are 900-1902 characters and functionally too large to execute without scrolling; this is captured under no-batch/atomicity failures. |
| 10 | No standalone context-only items | PASS | All 50 items include at least one action beyond reading (update/create/spawn/run/write/verify), based on full task read and checklist extraction. |

## Summary

- Checks passed: 5 / 10
- Checks failed: 5
- Critical issues: 4
- Important issues: 3
- Issues fixed in-place: 0 (fix authorization: false)

**Confidence:** Verified: 10/10 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
**Tool engagement:** Read: 2 | Grep: 0 | Glob: 0 | Bash: 4

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | CRITICAL | All checklist items, lines 147-335 | Completion gates are not B2-compliant. Template B2 requires: “This item cannot be marked as done until the actions are completed in their entirety exactly as described. Once done, mark this item as complete.” The task instead repeatedly says blockers can be logged and “then mark this item complete,” which permits completion without the action being completed. | Rewrite each item’s ending so blocked/incomplete work is not marked complete as successful completion. Use a blocked status/log path and reserve completion for actions completed exactly as described. |
| 2 | CRITICAL | QA/fix/verification batch items at lines 227, 255, 299, 317, 323 | Items combine consolidation, conditional fix spawning, and verification spawning into one checkbox. These are distinct operations with separate outputs and dependencies, violating “no batch items” and making execution-order simulation impossible. | Split each into separate items: consolidate findings; decide fix/no-fix; run exactly one fix agent if needed; verify structurally; verify qualitatively; gate on PASS. |
| 3 | CRITICAL | Agent-spawning items at lines 171, 173, 179, 223, 225, 251, 253, 295, 297, 315, 321 | Agent prompts are not fully embedded. Items name lens/mode/output but do not provide complete prompt bodies with all required input paths, checklist, expected report structure, and pass/fail criteria. Shorthand like “each with adversarial framing” is not independently executable after rollover. | Embed the full prompt for each spawned agent or create separate checklist items per agent with complete `QA_MODE`, lens, assigned files/scope, exact verification checklist, output path, and verdict rules. |
| 4 | CRITICAL | Line 331 | Step 5.6 instructs `git -C /config/workspace/IronClaude add -A`, which is a broad staging operation in the same item as reflect execution. Even with a caveat about `.claude/`, this is not B2-safe or scope-safe and conflicts with the project’s absolute rule not to stage `.claude/` mirrors. | Replace with a scoped, explicit staging plan or avoid staging inside the task item. If staging is required, list exact absolute tracked paths or include a preflight `git diff --name-only`/`.claude` rejection gate as a separate item before staging. |
| 5 | IMPORTANT | Lines 215, 271, 275, 279, 291, 311 | Several implementation/test items batch multiple files or commands into one checkbox: line 215 creates `lockgate.py` and `writer.py`; line 271 creates evidence and validation tests; line 275 creates writer and integration tests; line 291 runs pytest and ruff; line 311 runs pytest, ruff, and verify-sync. | Split by file or command so each item has one primary action, one primary output, and one verification target. |
| 6 | IMPORTANT | Lines 215, 219, 239, 247, 251, 275, 307, 331 | Relative path tokens are used in checklist items despite the absolute-path requirement: `.claude/`, `.claude/commands/`, `.claude/skills/`, `.dev/pr-monitor/detection-contract.locked.md`, `.claude/settings.json`. | Replace relative path tokens in actionable checklist text with absolute paths, e.g. `/config/workspace/IronClaude/.claude/` and `/config/workspace/IronClaude/.dev/pr-monitor/detection-contract.locked.md`, while still preserving the source-of-truth warning. |
| 7 | IMPORTANT | Lines 187, 195, 199, 207, 211, 215, 255, 271, 275, 279, 299, 307, 323, 335 | Several items do not use explicit B2 context-with-WHY wording for every required context source. Some have “to confirm”/“to reuse,” but others list files and actions without an explicit reason tied to that item’s output. | Add explicit `because ...` rationale for every context source group, especially generated/future artifacts consumed by later items. |

## Actions Taken

No task-file changes were made. `fix_authorization: false`.

## Recommendations

- Do not execute this task file until the B2 failures are fixed.
- First fix the systemic completion-gate wording across all checklist items.
- Then split batch items, especially QA consolidation/fix/verification chains and multi-file test/module creation items.
- Finally expand every agent-spawning item into a complete embedded prompt and replace relative path references with absolute paths.

## QA Complete

VERDICT: FAIL
