# Documentation Context Card

**Generated**: 2026-11-23T19:14:41Z
**Wave**: 1.5
**Scope**: src/superclaude/cli/swarm/commands.py

## Release context

Release v5.0.0 post-release records: .dev/releases/current/v5.0.0/post-release/CONSOLIDATED-PLAN.md:334-339 says to describe the JobSpec custom_prompt_dir field and spec-file invocation instead of a flag. Parent directly read these lines. Branch A confidence 0.95; original FR-021 PRD/TDD not located. Complete/completed release folders absent. These records are contextual, not successful current-run evidence.

## Architectural docs consulted

- docs/swarm/command-reference.md:56-61: current by equal doc/component mtimes 1795451558 and no stale header marker; parent read directly. Explicitly says custom_prompt_dir is a JobSpec field with lens custom, not a run option.
- docs/swarm/user-guide.md:446-488: current under the same mtime/header check; branch B read the spec-file example and guard migration distinction.
- docs/dev/lens-contribution-policy.md:170-195,234-242: current under that check, but version-specific 5.0.0 wording is advisory. All branches degraded to native retrieval after Augment403; no unsupported freshness promise beyond that mechanical check.

## Restrictions / decisions that constrain the fix

- src/superclaude/cli/swarm/schema.py:695-734 enforces that a nonempty custom_prompt_dir requires lens custom; inline custom prompts without this directory remain permitted.
- src/superclaude/cli/swarm/preflight.py:1574-1615 reads that field before schema validation and retains the injection-guard path. Branch C additionally located system.txt required-substring and metadata-mapping constraints at preflight.py:691-697,837; preserve them, do not broaden the fix.

## Re-frame signals

- Current source and current docs agree on job-file configuration; the two generated help passages diverge. Correct help, not parser semantics.
- Do not add a flag, change custom lens behavior or weaken guard enforcement to match stale wording.
- No successful custom-job execution was observed by this diagnostic; its conclusion is limited to help/parser consistency.
