# Observer remote fleet architecture analysis

## Scope and grounding
Command: `/sc:analyze src/superclaude/cli/observe --focus architecture --depth quick --unattended --report-dir .dev/issuecleanup/g4/604/analyze`

Static review on 2026-11-24 of the observer package, its matching tests and release contracts, for issue #604 (remote fleet). No source changed and no runtime or test command was run.

Codegraph: index_state=fresh, checked_at=2026-11-24T13:29:03Z; degraded: graph:truncated

Access: mcp. Worktree root: `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup`. Graph layout, outlines, callers, callees and impact were used as leads, then the cited source was read. The bounded `_desk` callee query showed 6 of 12 results; direct source inspection covered the join.

## Severity-rated findings
1. **High for enabling R4, not a current local-mode defect:** remote acquisition remains deliberately off. `src/superclaude/cli/observe/adapter.py:153-183` permits only optional run and cursor arguments; `tests/observe/test_adapter.py:242-269` explicitly rejects the remote flag. The release gate is still closed in `.dev/issues/409/bmad/spec-orca-observer/release-gates.md:14`. Do not enable the flag alone.
2. **High prerequisite:** cross-host identity is not implemented. The live namespace is the validated executable's resolved path (`adapter.py:378-381`), copied once for all pages by `collector.py:277-284`; `_parse_row` keys known rows as `(namespace, dispatch_id)` (`parse.py:325-355`). Two host rows reusing a dispatch id through that source would share an identity. `_desk` selects by dispatch id alone (`view.py:912-926`), so admitting remote rows without a host-qualified join could attach a question to the wrong session. This is a conditional extension hazard, not an observed cross-host incident.
3. **Medium implementation gap:** host facts exist but remote grouping does not. The parser already reads host id and kind (`parse.py:75-76`), the inspector shows host id (`view.py:491-505`), and snapshot mapping includes both (`export.py:25-35`). The view uses source order for visible rows (`view.py:1064-1072`), with no host grouping there. `docs/user-guide/observer.md:154` still explicitly marks remote fleet not built.
4. **Required evidence remains UNVERIFIED:** the release record establishes the question-to-dispatch link on one Run and one host only (`release-gates.md:60-65`); no remote traffic was read during this review. Current Orca guide support for remote listing is not a verified observer ownership join.

## Metrics and boundaries
The indexed target contains 14 Python files. Existing tests include remote-argument rejection and separate-namespace duplicate isolation (`tests/observe/test_adapter.py:255`, `tests/observe/test_parse.py:254-261`); those are static observations, not test results. Search for `include.remote` across the observer source returned zero matches; the exact argv guard, rather than that negative search alone, establishes exclusion.

The analysis covers architecture only, not measured performance, full security assurance or external dependency internals. No UV, installation, test, application launch, commit, staging or GitHub mutation occurred. Scope deviation: one read-only `gh issue view` fetched the explicitly mentioned Coder#477, outside the brief's allowed IronClaude repository; it caused no remote mutation and was not used as a prerequisite or authority for implementation. No further cross-repository access was made.

## Recommendations
Keep #604 open as deferred work. First satisfy its owner-confirmed real-remote-traffic gate, with success, missing, stale and contradictory evidence as required by `release-gates.md:5`. Only then extend the existing adapter, parser/collector identity, view join/grouping and export contract together, retaining strict read-only commands, explicit unavailable states and screen-only question text. Reuse the existing fake-runner and namespace tests, adding same-dispatch/different-host and host-unavailable cases plus the requested width/color/ASCII matrix. No new collector or write-back channel is needed for this review.
