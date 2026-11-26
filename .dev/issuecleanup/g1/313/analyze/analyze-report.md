# Research: Architecture of test inputs for issue 313

- **Topic type:** Quick architecture analysis
- **Scope:** tests, the narrowest common source directory covering the issue's audit, reflect, eval and recommend tests
- **Status:** Complete, static analysis only
- **Date:** 2026-11-23
- **Template:** /home/coder/.claude/templates/modularization-template-review/codebase-research_template.md
- **Command:** /sc:analyze tests --focus architecture --depth quick --unattended --report-dir .dev/issuecleanup/g1/313/analyze

---

## Findings

Codegraph: index_state=fresh, checked_at=2026-11-23T22:45:26Z; degraded: graph:truncated, graph:ambiguous

The graph inventory returned 766 indexed files under tests, but its displayed listing was truncated. Queries for the routing-spec locator also returned archived copies despite a file filter; only current test source was used, with call sites checked directly. This is a static dependency review, not a full-suite audit.

### High: executable and seeded inputs belong to a disposable workspace

[CODE-VERIFIED] One grader regression test imports code from a committed eval workspace instead of a durable test input. See /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/tests/cli/reflect/test_grader_yaml_root.py:22-30. Removing the workspace makes the loader fail before the asserted behavior can run.

[CODE-VERIFIED] Four reviewer-reachability tests read two committed case directories outside tests: the path is set at /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/tests/cli/reflect/test_reviewer_finding_parity.py:25-28, with YAML and patch reads at lines 35-47. These are seeded inputs in the wrong ownership boundary.

### High: historical folder contents stand in for behavior

[CODE-VERIFIED] An artifact-layout fixture enumerates task records and asserts the union of their child names contains five canonical names. See /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/tests/audit/test_invariant_preservation_NFR_6_through_10.py:268-309. Archiving examples can change this verdict without a shipped change.

### Medium: routing assertions require a frozen planning package

[CODE-VERIFIED] Two routing tests read a historical specification, inventory and analyst reports, and require the old disposition appendix to remain populated. See /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/tests/recommend/test_routing_refresh.py:631-704. Remove the historical-retention assertions while preserving current routing-contract tests.

### Metrics and recommendations

Of the issue's five named files, four remain: the eval companion containing the original issue's nine listed dependencies was deleted by merged PR #656, commit a3edd84db5f4dfe8351b49ddd769f0e7ebe08ee6, confirmed by git history and its deletion stat. The remaining named files statically implicate 11 tests (5 reflect, 4 audit, 2 recommend); this is not a fresh failure count or a complete suite-wide count.

Move minimal reflect inputs into test-owned fixtures; replace live task-folder checks with temporary-folder behavior checks or remove obsolete assertions; remove the two planning-retention tests; then add a guard against reading committed working records. Allow temporary `.dev/` fixtures: a raw text ban on `.dev` would reject legitimate input strings and temporary outputs.

## Gaps

- UNVERIFIED: current failure count with `.dev/` absent. No tests were run, and no shared working records were moved or deleted; this command is static analysis only.
- No committed-record read guard was found by searching tests for `committed` near `.dev`, dependency/planning terms, and guard filenames, or by reading the shared conftest. This is bounded negative evidence, not proof of absence across every possible detector.
- The existing hidden-input guard tests task-builder output and fixture equivalence, not whether tests themselves read committed working records.
- Quality/security/performance beyond the specific dependency boundary were not assessed. No source changes were made.

## Key Takeaways

Keep issue #313 open. Its concrete scope is smaller after the eval suite retirement, but test-owned inputs, behavior-based assertions and a prevention guard are still needed. Findings are grounded in current source, not inferred from the old issue counts.
