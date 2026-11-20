Implementer claims (not evidence):
- Built the four verbs (list, archive, retire, prune) in scripts/worktree_cleanup.py with find_worktrees, assess, RepoLocks, a summary line, the two prune files and the exit codes 0, 64 and 69.
- The A1 fix pass added a Decision.unread flag for reasons that come from an unreadable fact, an orca_known flag so an unreadable Orca list keeps every worktree, an output folder check for every verb, and OSError handling for the lock and the output files.
- Believed T12.AC1, AC2 and AC4 met; the review accepts them.
- Believed T12.AC3 met for the verdicts of the eight rules; the review shows that an unreadable fact found only at the re-check after the terminals are closed (remove_worktree) comes back as status kept, which counts neither as failed nor as exit 69.
