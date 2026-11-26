# Ground-truth authoring summary

| document | items | blocking items | dropped findings |
|---|---|---|---|
| HX-1 | 2 | 0 | 3 |
| HX-2 | 6 | 1 | 5 |
| HX-3 | 12 | 0 | 7 |

Dropped counts include implementation-time findings that were code defects, not plan defects (HX-1: 3, HX-3: 1). For HX-3 the earlier report (070955) was unusable as a whole because its reviewed plan hash differs from the plan file.

HX-2 caveat: its base (119622e3) lacks the five files the plan edits, because they existed only uncommitted when the plan was written. See HX-2/notes.md.
