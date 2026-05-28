# Variant 2 — Refactorer Requirements

## Position

Start with the smallest safe CLI feature flag layer: a registry, read/write override helpers, and a Click command group that follows existing SuperClaude CLI conventions.

## Requirements

1. Define flags centrally in source with boolean-only values for the first iteration.
2. Add `flags list`, `flags show`, `flags enable`, `flags disable`, `flags unset`, and `flags validate` commands if these names align with the existing CLI command style.
3. Store local overrides outside generated `.claude/` mirrors and document any tracked versus ignored config behavior in command help.
4. Use deterministic precedence: environment read-only override if supported, then project override, then user override, then registry default; or omit environment support for v1 if risk is too high.
5. Add tests at the CLI boundary and registry boundary.

## Risks

- Supporting typed variants immediately may over-expand scope.
- Environment variables can create surprising behavior if writable commands cannot show them clearly.
- Persisted project overrides need a careful tracked/ignored decision.

## Acceptance Criteria

- Boolean flags can be listed, toggled, unset, and validated.
- Overrides never require editing generated mirrors.
- Tests prove precedence and unknown-key handling.
