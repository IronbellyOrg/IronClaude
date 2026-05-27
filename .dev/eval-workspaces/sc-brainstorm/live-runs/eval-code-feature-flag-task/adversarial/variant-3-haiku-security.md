# Variant 3 — Security Requirements

## Position

Feature flag management must be audit-safe. Unknown flags, malformed override files, and expired flags should fail closed. Commands must make hidden state visible.

## Requirements

1. Registry entries must include owner, purpose, default, allowed values, status, and expiry or review date.
2. Override loading must reject unknown keys and invalid values rather than silently ignoring them.
3. CLI output must distinguish defaults from overrides and expose the winning source.
4. Validation must be suitable for CI and fail on duplicate keys, expired active flags, malformed override files, and unsupported value types.
5. The first release should avoid remote evaluation, network calls, or dynamic code loading.
6. Help text and diagnostics must avoid leaking sensitive paths beyond what the user explicitly supplied.

## Risks

- Flags can bypass security controls if they are not clearly categorized.
- Environment overrides can be abused in automation if not visible in diagnostics.
- Expired flags become permanent attack surface without enforcement.

## Acceptance Criteria

- Malformed overrides fail closed with non-zero status.
- CI validation detects stale active flags.
- No command writes to generated mirror directories.
