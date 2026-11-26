# Refactor-find recommendation architecture analysis

Template: /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/.dev/issuecleanup/g2/468/report-template.md (Analyze skeleton).

## Scope and grounding
- Command: `/sc:analyze src/superclaude/cli/swarm/lenses/refactor_find.py --focus architecture --depth quick --unattended --report-dir .dev/issuecleanup/g2/501/analyze`
- Checkout: `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup`, commit `a7ae3dd30fcf88aaab655c37e94e58e121c2d863`, inspected 2026-11-24.
- Narrow target: the 60-line refactor-find lens definition. Supporting reads cover its validator, command rendering, foreground substitution, command definitions and lens catalog. No source changed.
- Codegraph: index_state=fresh, checked_at=2026-11-24T02:41:43Z; degraded: none. access=mcp. Readiness checked once; later unrelated report writes by other workers did not change the target source.

## Architecture and metrics
The lens is declarative configuration, not a command implementation. It selects a findings-table recipe, three workers, a 4000-line target cap, and experimental status. The registry imports the lens; the foreground completion path takes the manifest's recommendation template and passes substitutions to reduction (`/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/cli/swarm/commands.py:2134-2163`). The renderer only formats the string; it does not resolve a command definition (`/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/cli/swarm/reduce.py:448-467`).

Measured static scope: 60 target lines; one missing follow-up command in that target. Codegraph reports one direct importing file and 12 impacted symbols/files including the target, registry, CLI and tests; these are review leads, not proof of executable call sites. The existing substitution test deliberately accepts a fictitious `/sc:foo` (`/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/tests/swarm/test_reduce.py:305-314`), so it cannot serve as the requested bundled-command availability regression.

## Severity-rated findings
1. **Medium: unavailable follow-up breaks the manual next step.** `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/cli/swarm/lenses/refactor_find.py:53` advertises `/sc:code-review --apply {compare_files}`. Exact filename searches found no packaged or installed `code-review.md`. The defect affects the experimental lens's advice; this review does not establish a failed worker run, automatic invocation, or source modification.
2. **Medium: regression coverage does not check that bundled recommendations name shipped commands.** The lens validator's check list is limited to template-file resolution, recipe registration, suspect-placeholder coupling, uniqueness, injection guard and strategy registration (`/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/cli/swarm/lenses/_validate.py:603-610`). The renderer test accepts `/sc:foo`, and no swarm test contains `code-review`. The issue's requested focused availability regression remains unverified as implemented.
3. **Implementation caution, same issue rather than an extra fix:** foreground default substitution includes `<existing-review>` (`/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/cli/swarm/commands.py:2143-2145`). An existing comparison command is not a complete solution unless the chosen path supplies real supported inputs, or explicitly requires the person to supply an existing review.

## Recommendations and roadmap
Keep issue #501 open and implement a small source/test/documentation correction in a separate authorized task. Reuse an existing report-consuming follow-up, prove its accepted options and real file inputs, and add a packaged-command existence regression for bundled lens recommendations. Do not introduce a command simply to make the stale string valid. The first milestone is a valid suggestion; the second is regression coverage and aligned current user guidance.

## Verification limits
Static quick architecture analysis only. No model calls, swarm runs, test suite or follow-up command invocation were performed; end-to-end behavior and the final replacement are UNVERIFIED. An empty graph/search result was not used as proof of dead code. Exact searches found no packaged or installed namespaced code-review definition. No source, Git index, branch or remote was changed.
