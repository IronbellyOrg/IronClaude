T12 notes (informational, no verdict change)
- In `commands/sc-recommend.md` the keyword rule (line 117) and the `improve_category` block name a recommendation category, not the command; both stay (the plan said to drop the keyword; keeping it keeps the category rule coherent). After the Augment review on the PR the block now routes to `/sc:sc:analyze --focus quality` first (documented flag) and offers `/sc:sc:cleanup --type code --safe` as a secondary entry, not as the only primary.
- `performance_category` now has `secondary_commands: []` (its only entry was the removed command).
- `commands/sc-troubleshoot.md` line 120 now points to `/sc:sc:implement` for broader refactoring (the root tree's own feature command, as the `/sc:build` removal did).
