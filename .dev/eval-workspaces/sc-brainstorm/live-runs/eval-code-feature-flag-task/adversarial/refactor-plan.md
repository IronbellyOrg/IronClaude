# Refactor / Implementation Plan — feature-flag-system

## Base = sonnet/backend; Layered Adoptions

### Step 1 — SDK + Provider Interface (from opus + sonnet)

- Add `feature_flags/sdk/openfeature_client.py` exposing
  OpenFeature-compatible `get_boolean_value`, `get_string_value`,
  `get_object_value`.
- Add `feature_flags/provider/base.py` with abstract `Provider` class:
  `resolve_boolean`, `resolve_string`, `resolve_object`.
- Add `feature_flags/provider/file_provider.py` implementing
  `Provider` backed by the file loader (v1 implementation).

### Step 2 — File Store + Watcher (from sonnet)

- `feature_flags/storage/file_loader.py` reads `flags.yaml` and
  validates via Pydantic schema.
- `feature_flags/storage/watcher.py` uses `watchdog` to detect
  changes, parses atomically, swaps in-memory map. Holds previous
  state on parse error.
- Schema enforces: key, type, default, rules, kill_switch, owner,
  sensitive (default false), created.

### Step 3 — Bucketing (sonnet + haiku)

- `feature_flags/bucketing.py`:
  - Default: SHA256 of `<flag-key>:<targeting-key>` mod 10000.
  - If flag has `sensitive: true`: HMAC-SHA256 with per-flag secret
    salt fetched from a secrets store (env var for dev,
    secrets-manager for prod).
- Unit tests verify stickiness (same input → same bucket) and
  distribution (Kolmogorov-Smirnov against uniform with N=10000).

### Step 4 — Audit Log (from haiku)

- `feature_flags/audit/jsonl_writer.py`:
  - Append-only JSONL at `flags-audit.jsonl`.
  - Each entry: `{ts, actor, flag, old, new, reason, prev_hash, hash}`.
  - `hash = sha256(prev_hash || canonical_json(entry_without_hash))`.
  - Bootstrap entry has `prev_hash = sha256("genesis")`.
- `feature_flags/audit/verifier.py` walks log, recomputes hashes,
  reports first divergence.

### Step 5 — CLI (sonnet, RBAC layered from haiku)

- `feature_flags/cli.py` with click subcommands:
  - `flags list [--env]`
  - `flags get <key>`
  - `flags set <key> <value> [--reason TEXT]`
  - `flags unset <key>`
  - `flags audit [--since TS] [--verify]`
- `flags set` in prod environment + sensitive flag → requires
  `--approver <user>` and validates approver != actor.
- All mutations require `FF_ACTOR` env var or `--actor` arg;
  rejected otherwise.

### Step 6 — Signed Manifest (from haiku, scoped to prod)

- `feature_flags/signing/verifier.py` verifies detached signature
  `flags.yaml.sig` against a public key listed in
  `feature_flags-trusted-keys.pem`.
- Only applied when `FF_ENV=prod`; dev/staging skip verification
  with INFO log.
- Manifest rejection leaves previous good state in memory.

### Step 7 — Kill-Switch Fast Path (from opus)

- Kill switch evaluation precedes rollout rules in evaluator.
- Watcher poll interval reduced from default 2s to 1s when any flag
  has `kill_switch_armed: true` (set by recent manipulation).
- Test: simulate kill-switch flip + measure propagation latency
  (< 30s under load).

### Step 8 — Tests

- Unit tests for evaluator, bucketing, audit writer/verifier, signed
  manifest verifier, CLI commands.
- Integration test: write flag via CLI → watcher reloads → SDK
  returns new value within 2s.
- Coverage gate: >= 85% on `feature_flags/` excluding `__init__.py`.

### Step 9 — Documentation

- `docs/feature-flags.md` covering: schema, CLI usage, audit
  verification, signing setup, sensitive-flag conventions.
- Inline docstrings on public SDK methods.

### Out of v1 Scope (deferred to v2)

- Postgres-backed provider.
- FastAPI control plane.
- Admin UI.
- Redis pub/sub push channel for sub-second propagation.
- Multi-tenant isolation within a single environment.
- PyPI publication.
