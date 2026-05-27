# Codebase Context

## Relevant Existing Code

- `src/superclaude/cli/` — existing Python CLI package area where a feature flag command group or supporting module would integrate.
- `src/superclaude/commands/brainstorm.md` — command definition conventions, output expectations, and source-of-truth rules for command artifacts.
- `src/superclaude/skills/sc-brainstorm-protocol/SKILL.md` — brainstorm protocol contract for seed briefs, adversarial outputs, handoff routing, and return contract shape.
- `.dev/eval-workspaces/sc-brainstorm/SPEC.md` — eval expectations for live brainstorm runs and artifact structure.

## Architecture & Patterns

- Source-of-truth edits belong under `src/superclaude/`; generated `.claude/` mirrors must not be edited directly.
- Python operations use UV only.
- CLI-related behavior is tested through the Python test suite under `tests/` and should align with existing command conventions.
- Feature flag management should be source-backed and validation-friendly rather than ad hoc environment checks scattered through command handlers.

## Integration Points

- Add or extend a CLI command group under `src/superclaude/cli/`.
- Add a feature flag registry module under `src/superclaude/` or `src/superclaude/cli/`, depending on whether flags are CLI-only or framework-wide.
- Add tests for registry validation and CLI behavior under the relevant `tests/` area.
- If command definitions or skills mention the new commands, edit `src/superclaude/commands/` first and sync generated mirrors with `make sync-dev` outside this requirements run.

## Constraints Identified

- Do not write implementation artifacts into `.claude/` generated mirrors.
- Do not stage or commit from this live eval.
- Preserve existing command behavior unless a feature flag is explicitly enabled.
- Prefer a small, auditable first iteration over a broad dynamic flag platform.
