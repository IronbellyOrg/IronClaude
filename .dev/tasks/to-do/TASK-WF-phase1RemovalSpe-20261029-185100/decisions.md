# Decisions log (Phase 1 removal, issue #323)

One line per decision: decision | options | method | rationale.

1. Issue-comment record location | (a) free-text lines in `progress.md`, (b) `artifacts/issue-comments.md` cited from the task's `complete` evidence | self | `progress.md` is the `/sc:implement` ledger; the archive helper rejects any line that is not a ledger record (`archive_workspace.py` `_parse_ledger`, "unparseable ledger line"), so a free-text comment record there would block archiving. The plan's "URL (or error) is in `$PKG/progress.md`" is met by citing `./artifacts/issue-comments.md:<line>` in the `evidence=` field of the group's last `complete` line.
