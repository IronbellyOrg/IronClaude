# Proposed text for the IronbellyOrg/run-evidence repo

**Not applied: a separate change in that repo, made by the owner when this merges.** Nothing in this file has been written to the evidence repo, and no file of that repo was changed or pushed by this plan.

## 1. A pointer in `tools/archive-workspace.sh`

Add this comment near the top of the script, under its existing description:

```text
# To save the untracked and ignored .dev/ files of one finished worktree, use the
# archive step of the worktree cleanup in the IronClaude repo instead of copying by
# hand:
#   uv run --no-project python scripts/worktree_cleanup.py archive <worktree>
# It saves the files into this repo under <repo>/<author>/<date>_pr<N>_<subject>/,
# checks the saved copy against GitHub and prints VERIFIED. It removes nothing.
```

## 2. A note for `README.md`

Add this section to the README of the evidence repo:

```text
## Saves made by the worktree cleanup

The worktree cleanup in the IronClaude repo (`scripts/worktree_cleanup.py`, run through
`/sc:worktrees`) saves the untracked and ignored `.dev/` files of a finished worktree
here before it removes the worktree. Each save is one folder,
`<repo>/<author>/<date>_pr<N>_<subject>/`, with a `MANIFEST.md`, a `files/` folder, an
`ignored.tar.gz` (split into parts when it is large) and a `saved-paths.txt` that lists
exactly the paths that were saved. A folder is never overwritten: a repeat run verifies
it, and new files go to a folder with the suffix `-r2` or `-r3`. A possible secret in a
file stops the save and names the file; the value is never printed.
```

## What the owner does

When the pull request for issue 687 merges, the owner of the evidence repo makes these two edits there as one change. Until then the cleanup works without them.
