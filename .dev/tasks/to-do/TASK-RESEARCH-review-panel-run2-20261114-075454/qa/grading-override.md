# Severity grading override (owner decision A, 2026-11-14 12:47)

Scope: THIS task only (`TASK-RESEARCH-review-panel-run2-20261114-075454`), from Gate 2 onward (Gate 1 is closed under the earlier definition). It overrides the blocking/minor definition quoted inside the gate, consolidation, fix and verification items. It changes no framework file. A framework-wide change needs its own plan (`/sc:workflow`) and is a separate follow-up.

## The rule

**BLOCKING** only when at least one of these is true:
1. **A decision rests on it.** A design choice, recommendation, destination in the value inventory, conflict-log outcome, or a number or fact that the report's recommendation depends on would be wrong or unsupported because of the defect.
2. **A required deliverable or required section is missing** (for example one of the report deliverables (a) to (e), a section the template requires, a gate step that was required and not done).
3. **Security, data-loss or safety-boundary risk.** Always blocking, never downgraded by this override, whatever label or consequence a reviewer assigns.

**MINOR (a note on the follow-up list; never fixed in the gate, never rechecked)** for everything else, including:
- a false or imprecise statement that no decision, recommendation, destination or quoted number depends on;
- a miscount whose conclusion is unaffected;
- a wrong or missing tag, label or citation on a claim whose substance is true;
- a table-shape or formatting defect that does not change the meaning of a cell a later phase reads;
- a stale figure in a row or file when a sibling row or file already carries the correction and the correction is discoverable;
- an honestly logged [UNVERIFIED] limitation.

## How to apply it

- Ask for each finding: would the report's recommendation, a destination in the value inventory, a conflict outcome, or a number the recommendation rests on change if this stays as it is? If no, it is MINOR. If you cannot tell, say what the downstream use is and grade by it.
- Do not downgrade to avoid work. If the defective claim feeds a decision, it is blocking.
- Grade by this rule, not by the label a lens agent used (CRITICAL / IMPORTANT / MINOR). Keep the severity label only as information.
- Record every finding moved to MINOR by this override with the line `(minor under grading override)` so the follow-up list is complete; the follow-up list is reported to the owner at the end (one question: open an issue for the list or not).
- The cycle controls (F_0, F_1, F_2, regression, monotonicity, hard cap) count only BLOCKING findings under this rule. Everything else about the cycles is unchanged: at most 2 fix cycles, one fix agent, verification by agents that did not make the fix, halt precedence regression then monotonicity then hard cap.

## Measured effect on Gate 1 (estimate, orchestrator re-grade of the 11 review-1 findings; judgment, not a count by a reviewer)

Weights CRITICAL 3, IMPORTANT 2, MINOR 1. Review-1 blocking findings: P3-009 CRITICAL, ten IMPORTANT: total 23, average 2.09. Under this rule: blocking P3-003, P3-004, P3-005, P3-008, P3-009, P3-010 (13 points); minor P3-001, P3-002, P3-006, P3-007, P3-013 (5 points): total 18, average 1.64. Blocking count 11 to 6 (minus 45 percent); average severity score minus 22 percent. Adding the two cycle-2 table-shape findings (blocking before, minor now): average 2.08 to 1.54 (minus 26 percent), blocking count 13 to 6 (minus 54 percent). The 35 percent target on the average score is NOT reached by this rule on this sample, and the rule is not tuned to reach it.
