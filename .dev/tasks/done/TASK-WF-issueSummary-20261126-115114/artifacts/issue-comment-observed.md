Implemented the three performance cues in the canonical troubleshoot skill: `too long to load`, `takes forever`, and `hangs`.

Observed manual classification of the exact issue text `ccsession is taking too long to load`, with no `--type` override:
- The changed checkout skill emitted `Wave 0 complete: type=performance depth=quick` and wrote an audit header with `type: performance`.
- `takes forever` and `hangs` also selected performance. The ambiguous input `leak` stayed unset (`type: auto`) and retained security candidates.
- `leak` remains in both rows because it can describe resource leakage or sensitive-data disclosure. The existing ambiguity rule is preserved and its reason is now written beside it.

Verification scope: actual Skill-tool calls in a fresh local-plugin session loaded a byte-identical copy of the changed checkout skill. This was a complete Wave 0-only classification check, not default installed slash-name resolution or a full diagnostic/specialist run. The global installation was not changed. All four audit files and completion lines were produced; the CLI process subsequently ended with a budget-exhaustion error (exit 1), so this is not claimed as a clean end-to-end CLI run. An earlier launch failed during argument parsing; both attempts are retained.

`make sync-dev` and `make verify-sync` both exited 0. Existing `tests/troubleshoot/` tests: **404 passed**. Bounded searches found no existing keyword-table test, so no new matcher/test framework was introduced, as requested.

Evidence is retained in the workflow package `TASK-WF-issueSummary-20261126-115114` under `.dev/tasks/` (classification stream, four audits, consumed-copy hashes, test and synchronization logs). No Jev/preflight/gateway change was made.

