## Summary
- Delete the scheduled/manual framework-sync workflow, its script, and sync-state marker.
- Remove the Codecov upload step while keeping pytest's coverage command and XML/terminal reports unchanged.
- Remove obsolete workflow documentation, including upload troubleshooting and the upload-specific best-practice item.

## Scope and preserved behavior
- Only five tracked files change: three deletions and two workflow-file edits.
- The generic README template badge and all previously imported upstream content remain unchanged.
- PR #283 and `sync/framework` on origin are deliberately untouched. Closing the PR or deleting that branch requires separate approval.

## Validation
- Local runnable assertions passed: exact upload-step-only removal, parsed workflow equivalence, retained coverage command, and unchanged protected files.
- The required case-insensitive tracked-file search found no retired integration references outside `.dev/` and the exempt README template.
- `git diff --check` passed.
- Independent final implementation review passed all 12 acceptance criteria.
- Full pytest and hosted CI were not run locally for this removal-only change. CI will run on this PR.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
