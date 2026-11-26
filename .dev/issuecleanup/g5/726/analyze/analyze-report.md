# Observer architecture analysis

## Scope and grounding
Command: `/sc:analyze src/superclaude/cli/observe --focus architecture --depth quick --unattended --report-dir .dev/issuecleanup/g5/726/analyze`.
Scope: the observer package, the narrowest common source directory covering question selection, input handling, retention, file output and the interaction loop for issue #726. Static inspection only.
Codegraph: index_state=fresh, checked_at=2026-11-24T14:16:13Z; degraded: none
Discovery found 14 Python files including the fixtures package initializer. Graph outlines, run_loop callees and QuestionRecord impact were checked against current source. Issue #726 and its one comment, dependency #727, and PRs #592, #598 and #730 were read on 2026-11-24.

## Current architecture
- Pure state and display: `questions.py:28-33` retains `(Run id, message id)` and a parsed question; `view.py:1246-1300` handles selection, filtering, export and quitting. `view.py:1162-1167` contains only NONE, EXPORT and QUIT effects.
- Loop and I/O: `commands.py:325-355` collects state, calls the pure key handler and handles local exports. Exports already write on input, so voting would not be the first write-from-input.
- Files: `export.py:236-274` supplies the observer state directory and atomic file replacement. That is reusable plumbing, not an existing vote store, restart loader or agreed storage architecture.
- Missing data: `parse.py:416-436` has question identity and sanitized question text but no answer/decision field. `questions.py:1-11` explains why an answered question can remain listed as open.
- Privacy: `export.py:89-118` excludes question text from text exports; `export.py:158-176` exports only question identifiers, times and counts to JSON. `tests/observe/test_export.py:312-326` pins text exclusion.

## Findings and severity
1. Medium, feature absent: no vote action, judgement field, decision note, durable feedback schema or restart readback was found in the inspected package. Evidence: complete key handler and effect enum, question data classes, local export loop and a Python-source search for vote/judgement/judgment/intervention with no matches. The Decision Desk is a foundation, not completion of #726.
2. Medium, sequencing: the 2026-11-22 owner comment on #726 relaxes read-only direction but explicitly defers voting until #727's architecture/storage evaluation. Local-file persistence is a candidate, not an approved decision or an unresolved general permission to write.
3. Medium, privacy acceptance prerequisite: merged PR #598 (10f6ec670bf55f0fe768be8e0ef2067d5c5d879e) and `.dev/issues/409/bmad/spec-orca-observer/release-gates.md:64` retain the screen-only question-text boundary. The newer direction permits two-way work but does not specify how sensitive text is stored. Resolve the specific text-retention exception, size cap and redaction policy in #727 before implementing acceptance criterion 2.
4. Medium, decision capture: question-only data cannot supply what was actually decided. Specify an explicit decision-note input or another verified answer source, without treating disappearance from the source window as proof of resolution.

## Recommendations and limits
Keep #726 open as still-relevant, medium complexity, size M, P2. First complete #727's architecture/storage evaluation and owner scheduling, including privacy and the source of decision text. Then add selected-question yes/no input, persistent records keyed by Run/message, restart readback, clear save-error handling and tests, using the chosen storage rather than assuming local files. Keep Orca action boundaries unchanged for this issue; answering, approval, dispatch and training remain outside its scope.

No source, Git index, GitHub issue or PR was changed. Tests, builds, package tools and live dashboard interactions were not run under the brief's restrictions. Runtime behavior and production storage requirements beyond the inspected source are UNVERIFIED. No numeric quality/security/performance score is inferred from this architecture-only quick review.

Verification limitation: first section-population Edit calls were rejected by the freshness hook because the newly written stub had not been Read; after a tracked Read they succeeded. No hook or edit pathway was bypassed.
