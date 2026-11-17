Rule 6 bold heading of `agents/rf-qa-qualitative.md` for stage 4: **A contradiction a decision rests on stays Blocking**

# Kept mechanical gates (stage 3)

Format: path relative to `src/superclaude/`, the gate's quoted words, the condition it maps to, the reason.

## agents/rf-qa.md (Task 4)

Frozen inventory source: `.dev/tasks/done/TASK-WF-blockerStage0-20261116-021044/artifacts/stage0-inventory-freeze.md` rows for `src/superclaude/agents/rf-qa.md`.

- `agents/rf-qa.md`: "Generic steps like "create a service" = FAIL" | Missing (a required step named by the task is absent in substance when it is only generic) | kept: it is a mechanical check of one item's own result, an example of what makes that check fail, and the label does not decide the grade.
- `agents/rf-qa.md`: "Missing fields = FAIL" (frontmatter schema check) | Missing (a required field is absent) | kept: a fixed mechanical check of required fields; absent required content is the Missing condition itself.
- `agents/rf-qa.md`: "that's a FAIL" for a phase header whose claimed item count differs from the actual count (phase header accuracy check) | Decision (a quoted number the deliverable rests on is wrong) | kept: a recomputed count either matches or does not, so no judgment is involved.
- `agents/rf-qa.md`: "that's a FAIL" for an overview whose quantitative claim differs from the checklist (prose count accuracy check) | Decision (a quoted number the deliverable rests on is wrong) | kept: same reason, a recomputed count.

Rewritten, not kept (no longer fail by label): "Any incomplete file = FAIL", "Any untagged doc claim = FAIL" (both now graded by the review severity rule as Missing), the gap-severity bullets and the "Any CRITICAL or IMPORTANT gap = overall FAIL" line, the PASS and FAIL bullets of the research gate (now "blocking gap"), "Flag exact duplicates as IMPORTANT" (now a Note unless a condition holds), "For each blocking (CRITICAL or IMPORTANT) issue", and the summary-message counts.

## agents/rf-qa-qualitative.md (Task 5)

Frozen inventory source: `.dev/tasks/done/TASK-WF-blockerStage0-20261116-021044/artifacts/stage0-inventory-freeze.md`, rows for `src/superclaude/agents/rf-qa-qualitative.md` (lines 84, 108 to 111, 184, 240, 291, 332, 362, 429, 500, 567, 746, 784, 809, 858, 990, 994).

All eight verdict pairs (the FAIL bullets at the old lines 240, 291, 362, 429, 500, 567, 746 and 784, each with its PASS bullet one line above) were rewritten to "Any blocking issue exists" and none is kept as a named gate. The merge rule (84), principle 8, Rules 6, 9 and 10, the two cap sentences (809, 994), the relay lines and the summary message were rewritten. Lines 108 to 111 were changed by Task 3.

Kept, not rewritten, with the reason:

- `agents/rf-qa-qualitative.md`: line 184 `"System should be fast" = FAIL` | the testable-user-stories check's own example | an example of one check's own result, not a grade of a finding.
- `agents/rf-qa-qualitative.md`: line 332 `"Handle errors gracefully" = FAIL` | the error-handling check's own example | an example of one check's own result, not a grade of a finding.
- `agents/rf-qa-qualitative.md`: line 858 "Failing checks (Result = FAIL) MUST carry one of `AX-1..AX-5`" | the Result column of the check table | it names a check result, and the grade of a finding still comes from the review severity rule.
