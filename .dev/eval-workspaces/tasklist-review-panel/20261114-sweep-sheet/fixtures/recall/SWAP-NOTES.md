# Swap test notes (AO-2, REQ-08)

Reviewer: second-author-session claude-sonnet-5-5 (a fresh session, not a person). Date: 2026-11-15 (UTC).
Method: for each card, read `definition` and `question_template`, replace every name of a file, tool, command or product of this repository by a neutral placeholder, and ask whether the check is still stated clearly and in general terms.

Result: C1 to C8 pass. No card failed, so no `swap_test` field was left empty and no card was edited except its `swap_test` field.

Words kept as general vocabulary of the method, not as repository nouns: plan, task, criterion, test, candidate, tree, hit, row, PROBLEM (the answer token the sheet defines). Replacing them by placeholders would change the method itself, not hide a repository name.

| Card | Result | Reason |
|---|---|---|
| C1 | pass | Names no file, tool or command; speaks only of a criterion, an instruction and a set. |
| C2 | pass | Speaks of a driving document, a plan and a rule; nothing depends on which document. |
| C3 | pass | Speaks of a value, a row or a task; the placeholder is filled by the sheet, not by a repository name. |
| C4 | pass | Speaks of a command, pattern or test selector in general; no tool or flag is named. |
| C5 | pass | General (count, claim, copy in a second location). Observation, not a fail: "plan-unnamed hit" only reads clearly next to the list of hits the sheet shows, so it depends on the sheet layout, not on a repository noun. |
| C6 | pass | Names the words all, only, never and the set a sentence covers; "run one count or listing command over the tree" names no tool. |
| C7 | pass | Speaks of dictated text and the clauses of a constraint; no repository name. |
| C8 | pass | Speaks of a file the plan edits and a test that pins it; no repository name. |

Cards that failed: none.
