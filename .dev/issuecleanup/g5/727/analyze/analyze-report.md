# Observer architecture analysis

## Scope and grounding

Command: `/sc:analyze src/superclaude/cli/observe --focus architecture --depth quick --unattended --report-dir .dev/issuecleanup/g5/727/analyze`.

Static observer-package review for issue #727, covering collection, retained questions, views, input handling and existing persistence. The broader coordinator and watcher were not audited.

Codegraph: index_state=fresh, checked_at=2026-11-24T14:17:01Z; degraded: none

Worktree: `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup`. Graph discovery returned 14 Python files, including the fixtures package. Inspected outlines for commands, questions, view, adapter and export; inspected the run-loop call graph and input-handler impact graph. Confirmed cited behavior from source rather than graph summaries.

## Prioritized findings

These are gaps relative to the requested future platform, not defects in today's deliberately read-only observer. Source citations below are relative to the worktree named above.

1. **High, future action boundary:** voting and responding are not implemented. The loop handles only quit and local export effects (`src/superclaude/cli/observe/commands.py:340-355`; enum at `view.py:1162-1167`). The adapter permits only three exact command shapes and explicitly rejects send/reply/dispatch (`adapter.py:29-49,135-170`). A two-way design needs a separately specified authorization, routing, stale-question, duplicate-response and receipt boundary, not a broad loosening of this read adapter.
2. **Medium, persistence gap:** question retention is process-local and capped at 1,000 entries; it has no closure evidence (`questions.py:1-11,40-67`). The collector merges each read with the previous cycle's questions (`collector.py:205-245`). Existing disk output is a snapshot and text export, not a decision history (`export.py:158-180,236-274`). Question snapshots intentionally omit question text. Persisting question/decision content changes that privacy boundary and needs an explicit retention and access design.
3. **Medium, project architecture not chosen:** no database/vector/vote implementation was found by targeted search of this observer package for postgres, psycopg, sqlalchemy, sqlite, vector and vote. This is bounded negative evidence, not proof that no such facility exists elsewhere. The issue requires evaluating per-project Postgres and shared coordinator history before implementing responses. Existing global per-user export storage is not evidence of a chosen project database design.
4. **Low, wording correction:** the observer already writes local files on export and snapshot (`commands.py:332-354`); 'read-only' means it does not change Orca. A vote would add new persisted semantics, not introduce the first file write. Issue #726's body should not be treated as the architectural authority on this point.

## Metrics and limitations

- Static inspection only. No observer, test, build, Python, UV, install, database or browser was run. No source changed.
- Existing checks were read, not executed: `tests/observe/test_session.py:359-391` checks that input handling has no adapter/collector access; `tests/observe/test_adapter.py:155-190,274-286` covers forbidden verbs. Their current passing status is UNVERIFIED.
- Live GitHub issue #727 is open and has no comments. Issue #726's 2026-11-22 owner-ruling comment relaxes the read-only direction but explicitly leaves voting pending #727's architecture/storage evaluation. This review does not authorize implementation or database provisioning.
- Live issue #731 reports a first dashboard planning pass and 88 unfiled drafts on another branch. Its proposed artifacts are absent from this checkout; their actual contents, approval coverage and satisfaction of #727's deliverable are UNVERIFIED.
- GitHub search for PRs mentioning 727 returned unrelated broad matches (#500, #539), not verified implementations. Observer/dashboard title searches found baseline work but no PR verified to fulfill #727. This search is not an exhaustive branch audit.

## Recommendations

Keep #727 open as planning in progress, with implementation not built in this observer. First reconcile the initial planning reported in #731 against the exact #727 acceptance criteria. Complete current-version evaluation and the required deep architecture brainstorm; cover per-project Postgres, shared history, privacy, authorization, response identity and duplicate/stale handling before selecting storage or adding actions. Preserve current local exports and Orca read restrictions until an approved write contract replaces them. Have the owner schedule releases and the coordinator file the approved release issues; do not turn the release roadmap into an authorization to build.

Expected future change surface: adapter/action boundary, collection and question identity, view/effects, command loop, export/schema/storage, key hints, observer tests/fixtures/goldens, user guide and coordinator/watcher contracts. No claim is made that those surfaces have been implemented or tested here.
