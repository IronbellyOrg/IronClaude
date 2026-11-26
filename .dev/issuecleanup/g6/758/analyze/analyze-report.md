# Issue 758 architecture analysis

## Scope and grounding
Command: `/sc:analyze src/superclaude/output-styles/pragmatic.md --focus architecture --depth quick --unattended --report-dir .dev/issuecleanup/g6/758/analyze`.

Read-only static review on 2026-11-24. The sole existing installed command copy passed the brief guard; the project command copy is absent. Source scope is one Markdown policy file, with adjacent regression tests, installer and sync rules inspected only to trace delivery.

Codegraph: index_state=fresh, checked_at=2026-11-24T15:58:59Z; degraded: graph:empty

Codegraph returned no files for the Markdown-only target directory; its guide excludes Markdown. The review therefore uses direct source Reads and Grep, not graph absence as evidence.

## Severity-rated findings
- **Medium, feature gap:** `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/output-styles/pragmatic.md:40-44` already requires self-sufficient messages, answer consequences and a before-sending check for readers unfamiliar with the work. Lines 52-57 require one decision at a time and self-sufficient options. They do not explicitly require a compact context/implications/risks lead-in for every question, an existing-file detail link, a ban on creating a file merely to link it, or the no-existing-file fallback. This is partial overlap, not completion of issue #758.
- **Low, issue delivery instructions are inaccurate:** `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/Makefile:109-163` syncs skills, agents, commands, hooks and templates, not output styles; the whole Makefile has no output-style reference. `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/cli/install_user_setup.py:186-201` instead installs styles to the user's home configuration and reports files kept. Do not claim `make sync-dev` updates a project style mirror, or treat `make verify-sync` as proof of style delivery.
- **Low, missing targeted regression coverage:** `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/tests/commands/test_pragmatic_plain_english.py:18-26,50-74` protects four existing bullets and wrap-up headings, not the requested decision context, risk or existing-file rules.

## Metrics and boundaries
One primary Markdown policy target, three adjacent source/test/build files inspected for behavior, and the optional core rule section inspected for overlap. The existing dedicated regression module contains three tests. No runtime code, schema, API or worker-message change is required for the narrow feature. No source changes, tests, installs, syncs, staging or commits were performed. Dynamic effectiveness and current test/sync results are UNVERIFIED; the brief forbids uv and writes outside this report directory.

## Recommendations
Keep issue #758 open as still-relevant, simple / S / P2. Add the missing concise question rule in the existing Decision requests section and extend its existing content tests, preserving one-question, self-sufficient-option and answer-lines requirements. Keep the core rules and worker contract unchanged for this style-only requirement. Validate source text and the no-existing-file fallback before testing delivery in an isolated installation; leave installed styles untouched during this review. The merged predecessor PR #608 (a04ed5273129dcb785cd2755eac3e15171ca0716) supplies the current general clarity rules, not this missing feature.
