# Recipe reviews (REQ-08, AO-2)

One row per recipe. A person who has not seen the ground truth replaces the domain nouns of the recipe by placeholders, reads it again, and signs with the statement below. A row is complete when reviewer and date are filled and the date is before the freeze.

Statement: "domain nouns replaced by placeholders, still reads correctly, no issue-specific word".

| Recipe | Status | Reviewer | Date |
|---|---|---|---|
| C1 | DONE | claude-sonnet-5-5 session (a model, chosen by the owner in place of a person) | 2026-11-15 |
| C2 | DONE | claude-sonnet-5-5 session, round 2 on the reworded text (a model, chosen by the owner in place of a person) | 2026-11-15 |
| C3 | DONE | claude-sonnet-5-5 session (a model, chosen by the owner in place of a person) | 2026-11-15 |
| C4 | DONE | claude-sonnet-5-5 session, round 2 on the reworded text (a model, chosen by the owner in place of a person) | 2026-11-15 |
| C5 | DONE | claude-sonnet-5-5 session, round 2 on the reworded text (a model, chosen by the owner in place of a person) | 2026-11-15 |
| C6 | DONE | claude-sonnet-5-5 session (a model, chosen by the owner in place of a person) | 2026-11-15 |
| C7 | DONE | claude-sonnet-5-5 session (a model, chosen by the owner in place of a person) | 2026-11-15 |
| C8 | DONE | claude-sonnet-5-5 session, round 2 on the reworded text (a model, chosen by the owner in place of a person) | 2026-11-15 |

Review record, 2026-11-15 (RL session). A fresh Sonnet session worked in a folder holding only copies of the recipe files, with no ground-truth access (a post-check of its tool calls is in `implement-report/recipe-review/`). Its full report is `implement-report/recipe-review/review-1.md`. C1, C3, C6 and C7 passed. C2, C4, C5 and C8 failed:
- C2: the trigger words "halts, reports or returns" read as run-time behaviour verbs; "the candidate" is undefined in the block (every other recipe says "the plan"); it asks for up to 10 rules but allows 6 rows.
- C4: "case included", "picks fewer or other checks than the criterion needs" and "it may already contain finished work" name one defect shape or one review setup.
- C5: the list "changelogs, readmes, guides" and "mirrored copies" reads like the places a past defect hid; "Grade it with the grading check; never drop it" refers to a check the block does not define.
- C8: the folders `tests scripts docs` and the command `git grep -l -F` are hard-coded for one repository layout.
The recipe wording was the text of the requirements (`recipes_equal_mr_quotes` pins it byte for byte), so rewording needed the owner's approval. The owner approved it in the RL session on 2026-11-15; the reworded C2, C4, C5, C6 and C8 are recorded as `override` entries in `recipes.json` (recipe version 2). Round 2 (`implement-report/recipe-review/review-2.md`, a fresh Sonnet session, same restrictions, tool calls checked: 5 reads of the copied recipe files and one write, no other path): all eight recipes PASS, with borderline words listed there as notes. The four rows above that failed in round 1 are marked DONE on the strength of round 2. The pre-override text is in `implement-report/recipe-review/review-1.md` and `recipes-proposed-1.json` holds the applied text.
