Implementer claims (not evidence):
- Built remove_worktree in scripts/worktree_cleanup.py as steps 1 to 7 of source section 3, each step returning a RemovalResult (removed, kept or failed) and the order the acceptance criteria name.
- Re-uses the archive step of Task 9 and adds a digests field so a saved file edited after the save is never cleared.
- Believed T11.AC1 to AC4 met by the order test, the runner refusals, the forbidden-command scan and the tracked edit and later commit cases.
- Believed T11.AC5 met for a worktree Orca listed before; the review shows the read back skips the Orca reply when Orca had no row for the worktree.
- The A1 fix pass changed the Orca read back to read JSON and compare paths and ids for equality.
