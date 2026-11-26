# Architecture analysis

Command: `/sc:analyze src/superclaude/skills/sc-troubleshoot-protocol --focus architecture --depth quick --unattended --report-dir .dev/issuecleanup/g4/612/analyze`.

The protocol directory is the narrowest existing implementation area for issue #612: it owns type selection and its audit header. Supplementary checks cover the command wrapper, CLI registration and targeted source/test searches because the proposed standalone CLI does not exist in that directory.

Snapshot: 2026-11-24; checkout commit `a7ae3dd30fcf88aaab655c37e94e58e121c2d863`. Static review only. No source changes, executable tests, API calls to TypeSafe, staging or commits.

Codegraph: index_state=fresh, checked_at=2026-11-24T13:34:32Z; degraded: graph:empty

Graph access: mcp. The graph has no files for this Markdown-only target, so Glob/Grep/Read supply the analysis floor. A supplementary CLI registration outline was available. No caller/impact conclusion is inferred from the empty Markdown graph.

## Severity-rated findings
1. **High, implementation gate, not a production defect:** live issue #611 contains no measured outcome and remains open without comments; #612 expressly requires its affirmative result. Starting a Jev integration now would violate the issue's precondition. This is a review finding about readiness, not a blocked gate in the read-only analysis command.
2. **Medium, missing conditional feature:** Wave 0 remains keyword-based and its audit header has no Jev probability. Evidence: /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md:151-176. No `preflight troubleshoot`, `TYPESAFE_API_KEY`, `jev-1.14` or companion-Noul match was found anywhere under the production source tree or tests. CLI registration at /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/cli/main.py:557-596 contains no such group. This is intentionally not classified as a regression: the feature is conditional on a comparison not yet recorded.
3. **Medium, baseline not updated:** the performance row lacks "too long to load", "takes forever", and "hangs"; "leak" occurs under both performance and security, while ambiguity leaves the type unset. Evidence: /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md:152-159. This matches outstanding step 1 (#610) and matters to the fair baseline for step 2 (#611).

## Code quality metrics
Discovery returned 19 Markdown files (the main protocol plus 18 reference files); this was a quick targeted review, not a full audit of all references. Read the Wave 0 type-selection/header section, Wave 3 specialist selection, escalation rules, command options and CLI registration. No code was changed. No runtime pass count, coverage percentage or latency measurement was collected. Tests searched for the Jev-specific integration tokens returned no matches; filename discovery found preflight tests for swarm and reflect, not this feature.

## Security and performance
Type is consequential: it chooses specialist lenses in /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md:380-391. When signal-driven escalation applies, security raises the confidence threshold to 0.95 versus the ordinary 0.85; quick depth and no-escalate take precedence: /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/skills/sc-troubleshoot-protocol/refs/escalation-rubric.md:54-73.

No present Jev prompt-sharing path was located. Issue #612 requires documenting any future prompt-to-TypeSafe path and limits it to public-repository prompts; no external data-sharing permission was inferred from this review. Model accuracy, latency, cost and current TypeSafe API behavior are UNVERIFIED here. There was no live Jev request or credential inspection.

## Recommendations
Keep #612 open as still relevant but blocked by #611's measured decision. Complete #610 first so #611 compares against the improved baseline. If the agreed result is negative, close as not justified through the coordinator after the owner's go; a missing measurement is not a negative result.

If the result is positive, add only the standalone type selector, question/spec and offline tests, integrate it at Wave 0 and document prompt sharing; preserve explicit flag precedence, abstention, keyword fallback and error visibility. Do not change the gateway or infer depth/scope/authorization flags. Pin down threshold equality and distinguish Choice probability from the companion fit probability before writing the selector.

Negative evidence and limits: the graph cannot index the Markdown target; broad keyword `preflight` returns unrelated swarm/reflect logic; no Jev-specific production/test tokens were found. Augment search on pushed master returned swarm/reflect helpers, not this feature. An initial lookup of /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/__main__.py failed because that path is absent; file discovery and /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/pyproject.toml:70-71 resolved the actual CLI entry to /home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/cli/main.py. No runtime, live API, remote branch or exhaustive unpublished-work verification was attempted. The issue links no PR, and its comments are empty; broad GitHub searches yielded unrelated candidates only.
