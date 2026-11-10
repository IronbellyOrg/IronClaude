**F5. MAJOR, blocking. Expert: Wiegers (testability). Deleting a user deletes the documents they own**

- Grading sentence: an implementer who follows the stated text as written builds a user deletion that removes every document the user owns (`When a user is deleted, the documents they own are deleted with them.`, S:24), including documents shared with a team, and the team loses its data, which is wrong because the deletion destroys data other people rely on.
- Recommendation: transfer ownership instead of deleting
- Priority: High. Quality impact: deleting a user deletes the documents they own
