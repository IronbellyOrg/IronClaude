# Summary (confirm set, author 2)

| candidate | NP id | usable | items | blocking items | dropped findings |
|---|---|---|---|---|---|
| C1 detachTheCcsessi | NP-2 | yes: plan sha256 equals the ledger hash, all cited plan lines match; base f90877be (task-start HEAD from q0-head, because the ledger "start sha" is a tree, not a commit); caveat: the untracked .dev/troubleshoot folder the plan cites is not at base | 9 | 0 | 5 (M3, M4, M9, M10 inferred or scope remarks; stale anchors informational) |
| C2 addTheSharedCode | none | not chosen: plan matches and base is good, but only 4 verified defects (MF-1 to MF-4), under the 5 to 12 preference; held as reserve | 0 | 0 | not extracted |
| C3 authorizedNarrow | NP-3 | yes: plan matches report lines; base 7065667a (q0-head); caveat: section 19 of the design doc that Task 4 updates exists only in the uncommitted start state, not at base | 5 | 0 | 3 (M-004 wording; two debate-rejected notes; code-level blocking records from T2 and T3 reviews excluded as code defects) |
| C4 implementFrOnb1O | none | no: task-start commit is not recorded (no q0-head, start tree not in repo) and the driving spec file is absent from every checkout | 0 | 0 | not extracted |
| C5 devGuideFenceFix | none | no: report found zero defects | 0 | 0 | 0 |
| C6 fixIssue412SVeri | none | no: only 3 minor findings, 2 are missing-AC remarks; reserve | 0 | 0 | not extracted |
| C7 designOutput | NP-4 | yes: plan matches (lines 28, 31-33, 41, 44, 46, 47); base ec259f1b (q0-head, ancestor of the implementation commit) | 6 | 0 | 4 (MF-2 and MF-10 refuted as later evolution; MF-3 vantage artifact; MF-5 code defect) |
| C8 analyzeCodegraph | NP-5 | yes: plan matches (lines 29, 33, 43, 44, 56, 57); base ec259f1b | 5 | 0 | 3 (F6, F7 design and shipped-text remarks; refuted findings) |
| C9 planTheExplicitl | none | no: only 3 findings (one MAJOR, not blocking); reserve | 0 | 0 | not extracted |
| C10 brainstormFixBri | none | no: the report reviewed the plan while it was still in to-do and prescribes plan edits that the done plan already contains (later, fixed version); not used | 0 | 0 | not extracted |

Blocking requirement not met: none of the ten reports marks a plan defect blocking, and no implementation-time review record grades a plan-text defect blocking. The only blocking records (C2 T1, C3 T2 and T3) describe defects of code written during implementation, so they are excluded.
