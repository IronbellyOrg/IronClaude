# Proposal 3 — haiku / security

## Stance

A feature flag system is a runtime authorization surface. The
auditability, governance, and fail-closed semantics are not "extra
features" — they are the core of the system. Build the audit + RBAC +
fail-closed paths first; performance is a constraint to satisfy, not a
goal to maximize.

## Core Design

- **Signed flag manifest** (`feature_flags/manifest/`): Flag definitions
  shipped as a signed manifest file. Loader verifies the signature
  before accepting changes. Prevents unauthenticated tampering with
  the flag store.
- **Audit-first evaluator** (`feature_flags/evaluator.py`): Every
  evaluation emits a structured event to a ring buffer; events flushed
  to durable audit log asynchronously. Configurable sampling for
  high-traffic flags to manage volume.
- **RBAC on mutation**: Flag writes require an authenticated actor
  with `flags:write` permission on the relevant namespace. Actor
  identity captured in the audit record. No anonymous writes ever.
- **Fail-closed by default**: New flags are created in
  `state: disabled-pending-review` and require an explicit second-
  approver action before they can be enabled in production.
- **Kill switch**: Separate, fast path. Kill switches are a single
  boolean per flag, evaluated BEFORE rollout rules. Flipping a kill
  switch bypasses the normal propagation poll cycle via a push
  channel (Redis pub/sub or webhook).
- **Bucketing**: HMAC-SHA256 of `<targeting-key>` keyed on a per-flag
  secret salt mod 10000. Prevents attackers from predicting their own
  bucket assignment for sensitive flags (e.g. "is_admin_ui_enabled").

## Configuration

- Manifest signed with an org-controlled key; signature verified at
  load time and on every refresh. Rotation supported via key list.
- RBAC policies in a separate `flags-rbac.yaml`, also signed.
- Audit log written to append-only storage with cryptographic chain
  (each entry includes hash of previous entry). Tamper-evident.

## Failure Modes

- Manifest signature invalid → reject load; keep previous good
  manifest; alert. NEVER fall back to unsigned.
- Audit log writer unreachable → buffer in-memory ring; drop oldest
  events on overflow but never drop evaluations. Alert on buffer >
  50% full.
- RBAC check fails → reject mutation with structured error; do not
  partial-apply.
- Kill-switch push channel down → fall back to poll with WARN; kill
  switches still propagate but slower.

## Tradeoffs

- Pro: SOC2 / SOX-friendly by construction. Audit trail is
  tamper-evident.
- Pro: Fail-closed default + two-person review prevents a single
  compromised account from enabling a sensitive flag.
- Pro: Bucketing is cryptographically unpredictable per-flag.
- Con: Two-person review on flag creation adds friction. May be
  overkill for low-risk flags (e.g. UI copy changes).
- Con: HMAC-SHA256 bucketing is slower than Murmur (~10x). Still
  sub-ms but eats budget. Worth measuring.
- Con: Signing infrastructure + key management is a real operational
  cost not amortized in v1.

## Acceptance Criteria

- Manifest signature verified on every load; tampered manifests
  rejected with structured error.
- All mutations require authenticated actor; anonymous writes
  rejected with 403.
- Audit log entries form a hash chain; verifier tool detects any
  tampering with O(n) scan.
- New flags require two-person approval before transitioning to
  `enabled`.
- Kill-switch evaluation occurs before rollout rules; verified by
  test with a "rollout=100% + kill_switch=true" combination
  returning false.
- Test coverage >= 85% with explicit negative-path tests for
  every failure mode.
