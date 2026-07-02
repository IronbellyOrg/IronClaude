# OQ-2 Reflect Readiness Surface Decision

Status: Complete

- Open Question: OQ-2 / Fork B — reflect readiness surface
- Recommended default: `sibling-cli-command`
- Selected value: `sibling-cli-command`
- Exact command shape: `superclaude reflect contract-status [--validate] --repo --pr`
- Decision recorded at: 2026-07-01 19:20 UTC
- Decision source: user selected Sibling CLI (Recommended) after rejecting the invalid `both` ambiguity.

## Rationale

The design recommends a sibling Click command because the existing `superclaude reflect` surface is a Click group and the readiness path is unit-testable via `CliRunner`. This keeps readiness logic out of markdown orchestration while still updating `/sc:reflect` source command and skill documentation to describe the approved readiness bypass.

## Source Files That Must Stay Coherent

- `/config/workspace/IronClaude/src/superclaude/cli/reflect/commands.py`
- `/config/workspace/IronClaude/src/superclaude/commands/reflect.md`
- `/config/workspace/IronClaude/src/superclaude/skills/sc-reflect-protocol/SKILL.md`
- `/config/workspace/IronClaude/src/superclaude/commands/pr-submit.md`
- `/config/workspace/IronClaude/src/superclaude/skills/sc-pr-submit-protocol/SKILL.md`

## Dependent Phases Unlocked

- Phase 3 reflect CLI/docs implementation must implement exactly one readiness surface: `superclaude reflect contract-status [--validate] --repo --pr`.
- Phase 4 reflect CLI tests must verify the approved readiness surface and must not test a second slash-command-only surface unless a future decision replaces this file with `slash-command-flag`.
- Phase 5 final fidelity must verify source command and skill docs point operators to the approved sibling CLI readiness command and preserve diagnose/validate-first, no-default-write behavior.

## Blocking Status

Decision is non-PENDING. Phase 3 may use the sibling CLI command after the prior Phase 1 and Phase 2 gates pass. The `slash-command-flag` alternative is not approved by this decision.
