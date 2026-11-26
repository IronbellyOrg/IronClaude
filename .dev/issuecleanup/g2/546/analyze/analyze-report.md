# Model policy hook architecture analysis
## Scope and grounding
Command: `/sc:analyze src/superclaude/hooks --focus architecture --depth quick --unattended --report-dir .dev/issuecleanup/g2/546/analyze`.

Scope: the hook source directory, with installer and alias-policy tests checked only to distinguish adjacent mechanisms. Checkout: `a7ae3dd30fcf88aaab655c37e94e58e121c2d863`, reviewed 2026-11-24. Confidence is high for the source inventory and issue disposition, not for runtime event coverage.

Codegraph: index_state=fresh, checked_at=2026-11-24T02:46:08Z; degraded: graph:ambiguous, graph:truncated.

The graph mixed a historical experiment checkout into installer results despite a file filter; no historical rows or unverified caller locations are cited. Source reads and searches supply the evidence floor.
## Architecture and metrics
The hook directory contains 21 files: 16 shell scripts, one JavaScript script, one Python package marker, one JSON registry, one Markdown README and one example text file. This inventory comes from Glob; the graph indexes only two files in that directory.

Registrations are centralized in `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/hooks/hooks.json:84-135`: five PreToolUse groups cover freshness, bare-Python prevention, worktree-agent presence, launch-level permissions and job identity. The Agent and Skill matcher routes into the launch-level guard, not a model-policy checker.

The guard parser reads skill names, paths, isolation and commands, not an Agent model field (`/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/hooks/scripts/launch-level-guard.sh:186-207`). Its Agent/Task branch checks remote isolation only (`/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/hooks/scripts/launch-level-guard.sh:752-754`). The JavaScript SubagentStart hook injects output-style instructions (`/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/hooks/scripts/pragmatic-subagent.js:9-18`).

Installation copies scripts and merges registry entries into settings (`/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/cli/install_hooks.py:176-199,216-221`). Any future model hook would need a script, registration and installer regression coverage. No implementation is proposed now.
## Severity-rated findings
1. **High functional gap, intentionally deferred:** no source registration or hook model parser implements issue #546's requested deny-on-model-mismatch check. Grep of `src/` and `tests/` for `model.policy|model_policy|deniedModels|inherit_check|unknown_model|build_flag|verify-run` returned no matches. The registry and guard reads above corroborate the narrow conclusion: the proposed model-policy mechanism is not built in this checkout. This does not claim that every model-related feature is absent.
2. **Important issue-record discrepancy:** #546's last comment says implementation is blocked on #551, but #551's later 2026-11-17 closure comment says the owner dropped the model-policy hook effort for now and explicitly left #546 unchanged. Its state reason is `NOT_PLANNED`. This changes triage from an active blocked build to not-planned work, not completed work.
3. **Adjacent mechanism is not a substitute:** `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/tests/skills/test_model_alias_policy.py:1-12` describes static alias checks under #384. Such file-text checks do not validate a live event against per-stage model permissions.
## Recommendations and roadmap
Do not build the dropped hook as part of issue cleanup. Record the recommended disposition as not-planned and let the coordinator seek the owner's explicit go before any issue action. If the owner revives the effort, first recover and validate the referenced design, resolve its legitimate-use restrictions, verify the actual pre-event visibility, then plan the policy, checker, installer integration and allowed/denied/malformed-policy tests. Keep dynamic model routing separate from deterministic enforcement.
## Verification limits
Static quick-depth analysis only: no runtime model launches, hook execution, benchmarks or test suite runs. Zero security/performance defects are asserted because those domains were not tested. GitHub reads used only the brief's allowed issue/pr view/list verbs on the fork.

Full timeline events are UNVERIFIED: `gh issue view --json timelineItems` failed because that field is unsupported; comments, current state, state reason, dependency edges and closing PR references were read instead. No API or browser workaround was used because those surfaces are outside the brief's allowlist. Glob found no historical design file at its cited checkout path; the historical incident artifacts were not independently inspected. Their contents, exact requirement count and token totals remain UNVERIFIED. Augment retrieval first failed on default branch `main`; retry on `master` succeeded and located the static alias-policy tests.
