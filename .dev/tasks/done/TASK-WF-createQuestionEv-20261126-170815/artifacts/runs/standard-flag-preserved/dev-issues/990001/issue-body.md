<!-- /sc:issue bug template (simple). Filled from the description and a standard /sc:analyze pass; unverified choices are labelled assumptions. -->

## Bug Summary

Make `superclaude install` print, as its last line, how many skills it copied. The existing skills-phase count is followed by other installation and retirement output rather than being the final line.

[synthetic run marker: qev-standard-flag-preserved-182850]

Classification: bug; area: cli; depth: standard; complexity: Medium (user-supplied classification retained).

## Environment (OS, version)

- OS: Not known yet (no affected runtime supplied).
- Version: Not known yet (no affected package version supplied).

## Current Behavior

Static inspection shows that the skills phase prints its message before ccsession, hooks, templates, user setup, codegraph and retirement phases. The batch installer reports an installed count when nonzero, but the command has no final copied-skills summary. The final line depends on retirement outcomes; when no retired files are present, it is `   No retired commands, skills or agents present.` Runtime reproduction has not been performed.

## Expected Behavior

The last line of `superclaude install` states how many skills it copied during that invocation.

## Steps to Reproduce

1. In a disposable test home, with normal installation prerequisites available, run `superclaude install`.
2. Inspect the final output line and compare it with the earlier skills-phase message. Current control flow finishes with retirement output, not the copied-skills count.

These are proposed reproduction steps based on code inspection, not an executed reproduction.

## Impact Assessment (Severity, Blast Radius)

- Severity: low — missing end-of-command summary; no installation failure is established by this request.
- Blast Radius: users reading `superclaude install` output; installation and retirement behavior should remain unchanged.

## Error Messages

```text
Not known yet
```

## Codebase Context (from `/sc:analyze`)

- `src/superclaude/cli/main.py:202-208`: `install` invokes `install_all_skills` and prints its message during step 4, not at command completion.
- `src/superclaude/cli/main.py:210-296`: subsequent phases print output; retired-file cleanup is the final phase, followed by the aggregate failure exit check.
- `src/superclaude/cli/install_skills.py:62-150`: `install_all_skills` returns `(success, message)` and tracks installed, skipped, failed and command-served skills separately. Its installed count is derived from successful calls, not the number of directories already present.
- `src/superclaude/cli/install_skill.py:46-55`: forced replacement removes the old skill directory; successful copying uses `shutil.copytree`.
- `src/superclaude/cli/install_retired_files.py:269-305`: retirement prints per-item results, an empty-state line, or a restart notice, explaining why there is no single fixed final line today.
- `src/superclaude/cli/install_user_setup.py:323-366`: Orca skill installation is delegated to another CLI and reports presence/completion, not a reliable per-run copied count.
- `tests/unit/test_cli_install.py:683-727`: existing batch-install coverage protects command-activated and protocol skills. `tests/cli/test_install_retired_mcp.py:514-549` provides stubbed CLI invocation and exit-code coverage suitable for extending output assertions.

Analysis used Glob, Grep and Read; codegraph MCP and Auggie tools were unavailable, and CLI codegraph was not initialized. No installer or tests were executed.

Codegraph: index_state=not_initialized, checked_at=2026-11-26T18:30:35Z; degraded: graph:not_initialized; access=cli.

## Related Issues

None found by the scout lookup in `IronbellyOrg/IronClaude`; no related issue link is known.

## Priority

Low: the “Cosmetic, wording, or docs only” trigger applies to the missing terminal summary; no failed command, blocked work, security exposure or data loss is established.

## Fix approach

Repo: IronbellyOrg/IronClaude. Base branch: integration.

Commands, in order: `/sc:workflow "Plan the final copied-skills summary for superclaude install" --depth standard --handoff none`, then `/sc:implement <actual printed plan path>`, then `/sc:pr-submit --monitor 3` after verification.

Steps, in order:

- Step 1: In `src/superclaude/cli/install_skills.py`, expose structured successful-copy statistics to the CLI without parsing human-readable messages. Preserve existing `(success, message)` callers through a compatible wrapper or optional statistics channel; audit `main.py`'s update path and existing test stubs if the interface changes.
- Step 2: In `src/superclaude/cli/main.py`, retain the per-run count and emit one final summary after both retirement phases and before the aggregate failure exit. Preserve existing exit codes and diagnostics; do not print later normal-phase output after the summary.
- Step 3: Extend `tests/unit/test_cli_install.py` and the stubbed CLI coverage in `tests/cli/test_install_retired_mcp.py` for count accuracy and final-line ordering, including retirement diagnostics.

Assumption: “skills it copied” means successfully copied SuperClaude batch skill directories during this invocation, including forced replacements, excluding existing skipped skills, command-served skills, failures, and separately delegated Orca skill installation.

Assumption: use the final-line format `Skills copied: N`, including zero, on completed normal installation paths even when a handled phase fails; preserve failure status and leave `install --list` and `update` output contracts unchanged.

## Test plan

- Tests to add or change: in `tests/unit/test_cli_install.py`, exercise fresh copies, skipped existing skills, forced replacements, command-served exclusions, no available skills and mixed copy failures; assert structured counts represent successful skill-directory copies only. Keep protocol-skill regressions intact.
- Tests to add or change: in `tests/cli/test_install_retired_mcp.py`, use `CliRunner` with an isolated home and stub external installers, codegraph and retirement calls. Assert `result.output.splitlines()[-1]` is exactly `Skills copied: N`; cover a zero-copy rerun, nonzero count, retirement messages/exceptions and handled installation failure. Verify exit codes remain unchanged and `--list` does not emit a copied summary.
- Regression gate: run the focused installer tests, then `uv run pytest`, `make lint`, and `make verify-sync`. If primitive files change during implementation, edit canonical source and run `make sync-dev` before the sync check; never hand-edit generated mirrors.
- How a reviewer verifies: inspect the count source and final print placement, run the focused tests, and review captured output proving no later stdout/stderr diagnostics follow the summary on covered handled paths. Optionally reproduce in a disposable home, never against a real customized installation.

Assumption: deterministic stubbed CLI tests are the primary verification so this output change does not require network downloads, real MCP registration changes or modifying the reviewer's home.

<!-- sc:issue:create template=issue-bug-simple -->
