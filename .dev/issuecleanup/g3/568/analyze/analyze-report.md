# Architecture analysis: swarm command help

## Scope and method
Command: `/sc:analyze src/superclaude/cli/swarm/commands.py --focus architecture --depth quick --unattended --report-dir .dev/issuecleanup/g3/568/analyze`.

Read-only static review on 2026-11-24 at checkout `a7ae3dd30fcf88aaab655c37e94e58e121c2d863`. The narrow target contains both help surfaces identified by issue #568. Read adjacent registration, custom-prompt preflight and existing help tests only to trace their contracts. No source, dependency, environment or GitHub mutation.

Codegraph: index_state=fresh, checked_at=2026-11-24T13:14:28Z; degraded: none. Access=mcp; worktree_root=/home/coder/workspaces/worktrees/IronClaude/Issuecleanup. Used grouped file discovery, command outline, validate-lenses body/callers/callees and scaffold impact; confirmed relevant source with Read. Graph caller rows were leads, not proof of executed calls.

## Severity-rated findings
1. **Medium, user-facing help/parser contract mismatch (issue #568 remains).** `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/cli/swarm/commands.py:435-439` describes a `--custom-prompt-dir` option in validate-lenses help, and the scaffold lens-option help at the same absolute path, lines 3902-3909, repeats that option. The run command's complete decorator block at lines 1368-1557 has no such option; its shared decorator at lines 158-170 adds only `--auto-inject-guard`. The registration at `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/cli/swarm/__init__.py:136-154` installs those actual commands. Following the help sends a user to an unsupported option, not to a missing custom-prompt capability.
2. **Small regression-coverage gap in the checked help tests.** `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/tests/swarm/test_scaffold_cmd.py:63-69` checks only the lens/output option names; `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/tests/swarm/test_validate_lenses_cmd.py:145-152` checks only warning-mode. Neither assertion guards the misleading custom-directory guidance. This is not a claim that the entire test suite lacks custom-prompt tests.

## Metrics and impact
Two affected public help surfaces in one Python source file; three existing command-specific test files are relevant: scaffold, validate-lenses and run. Graph discovery enumerated 36 Python files under the swarm target directory; the analysis did not audit all 36. The defect needs wording plus focused regression assertions, not a new parser option or a change in job execution. No performance measurements or security audit were performed.

## Recommendations
Replace both public help mentions with the job-file fields `lens: custom` and `custom_prompt_dir`, pointing to spec-file or standard-input mode. `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/cli/swarm/preflight.py:1594-1619` reads these fields and `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/cli/swarm/preflight.py:1704-1709` applies custom prompts before schema validation. Existing error guidance already points to the job file at `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/cli/swarm/commands.py:1164-1169`.

Extend the two help tests to require the field spelling and reject the flag spelling, and add a parser-level unsupported-option assertion before dispatch. Preserve custom-prompt validation and run semantics. Treat the fix as a small standalone help correction; it does not depend on resume or dashboard repairs.

## Limits
Static analysis only. Runtime exit codes, rendered help, tests and historical private captures were not re-run or independently reproduced here: UNVERIFIED for this checkout. The live issue's November 16 report records an exit-2 rejection on its two frozen revisions, not a newly observed run. The brief forbids UV, dependency installation and writes outside the assigned report folder, so no test suite, application command or index initialization was run. A missing project command mirror was observed; the installed analyze command has Unattended mode and the guard passed with the missing copy skipped. One report edit was initially blocked because the freshness hook required an explicit Read after the stub write; Read was performed and the same Edit succeeded without bypassing the hook.
