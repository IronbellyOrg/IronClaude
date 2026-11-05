# Superseded reviewer prompts

- `T1-prompt-1-1.md` was `retries/T1/prompt-1-1.md`; `T2-prompt-1-1.md` was `retries/T2/prompt-1-1.md`. Moved unchanged (`git mv`) on 2026-11-04, on the user's instruction "Move them and archive".
- Defect: both lack the template's blank line between "Saved-probe re-check hit locations (may be empty): " and "Do not trust the implementer's report." (`~/.claude/skills/sc-implement-protocol/refs/qa.md:329-331`). The prompt-builder helper dropped it; no review criterion was added, removed or reworded.
- The two managed FINAL attempts that flagged them are ledger lines 7 and 10 of `../../progress.md` (their evidence paths name the old locations).
- Both tasks were re-reviewed with template-exact prompts (`retries/T1/prompt-1-2.md`, `retries/T2/prompt-1-2.md`): all AC met, no findings (ledger lines 8 and 9).
- Protocol gap, to fix in the lessons work: `refs/qa.md` has no rule for a saved prompt replaced by a later re-review.
