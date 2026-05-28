# Variant 1 — Architect Requirements

## Position

Implement feature flag management as a typed, source-backed CLI subsystem. The CLI should manage flag discovery, overrides, validation, and effective-value explanation while preserving existing command behavior by default.

## Requirements

1. Add a source-backed feature flag registry with key, description, owner, default value, lifecycle status, and optional expiry metadata.
2. Add CLI commands to list flags, show a single flag, set/unset overrides, and explain effective values.
3. Support scoped overrides with explicit precedence and source reporting.
4. Add CI-friendly validation for duplicate keys, unknown override keys, invalid values, and expired active flags.
5. Keep generated `.claude/` mirrors out of scope for persistence.

## Risks

- Flag sprawl if lifecycle metadata is not enforced.
- Ambiguous precedence if user/project/environment scopes are added without clear ordering.
- Hidden behavior if effective value reporting is omitted.

## Acceptance Criteria

- Existing CLI behavior remains unchanged without overrides.
- Unknown flags fail with actionable diagnostics.
- Validation catches duplicate or expired active flags.
- Effective-value output identifies default or override source.
