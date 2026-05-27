---
artifact_type: merged-requirements
topic: "implementing a feature flag system"
domain: code
strategy: systematic
depth: standard
proposal_count: 3
base_variant: sonnet/backend
convergence_score: 0.82
adversarial_status: passed
handoff_target: task
created: 2026-05-27T00:00:00Z
---

# Merged Requirements — feature-flag-system

## Problem Statement

Implement a runtime feature flag system that lets engineers and
operators toggle code paths without redeploying. The system replaces
ad-hoc env-var toggles and merged-and-forgotten code branches with a
governed, auditable, OpenFeature-compatible primitive. v1 scope is a
file-backed implementation that is OpenFeature-compatible at the SDK
boundary, ships hash-chained audit logging, and has a clean migration
seam to a Postgres + control-plane design in v2.

## Goals and Non-Goals

### Goals (v1)

- OpenFeature-compatible Python SDK boundary (boolean, string, object
  evaluation surface).
- Sub-millisecond evaluation on the hot path via in-memory dict
  lookup with no network I/O per call.
- File-backed flag store (`flags.yaml`) with watcher-driven hot
  reload; sub-2-second propagation for normal flags, sub-30-second
  end-to-end with safety margin.
- Hash-chained append-only JSONL audit log, tamper-evident,
  verifiable offline.
- Sticky bucketing for percentage rollouts (default SHA256;
  HMAC-SHA256 when flag has `sensitive: true`).
- Signed manifest verification in `prod` environment.
- Two-person review gate for prod + sensitive flag creation and
  mutation.
- Kill-switch fast-poll path (1s) separate from general flag
  propagation.
- Fail-closed default state for newly created flags.
- Test coverage >= 85% on `feature_flags/` package.

### Non-Goals (deferred to v2)

- Postgres-backed provider implementation.
- FastAPI control plane service.
- Browser-based admin UI.
- Redis pub/sub push channel.
- Per-tenant isolation within a single environment.
- PyPI distribution for external consumers.
- A/B experimentation analytics pipeline.

## Architecture Overview

```text
+-------------------+        +-------------------+
| Application code  |  -->   | OpenFeature SDK   |
| if flags.is_on()  |        | (client adapter)  |
+-------------------+        +---------+---------+
                                       |
                                       v
                             +---------+---------+
                             | Provider (abstract)|
                             +---------+---------+
                                       |
                                       v
                             +---------+---------+
                             | FileProvider (v1)  |
                             | (in-memory dict)   |
                             +---------+---------+
                                       ^
                                       |  watch + reload
                                       |
+--------------------+        +--------+--------+        +------------------+
| CLI mutator        | -----> | flags.yaml      | -----> | Hash-chained     |
| (flags set/unset)  |        | + flags.yaml.sig|        | flags-audit.jsonl|
+--------------------+        +-----------------+        +------------------+
```

## Functional Requirements

1. The SDK MUST expose `get_boolean_value`, `get_string_value`, and
   `get_object_value` methods compatible with the OpenFeature Python
   SDK signature (flag key, default, evaluation context).
2. The evaluator MUST return a value in p99 < 1ms measured under
   benchmark load.
3. The provider MUST support an abstract `Provider` interface with
   concrete `FileProvider` for v1; the interface MUST permit a
   future `PostgresProvider` without changes at SDK or evaluator.
4. The CLI MUST expose subcommands: `flags list`, `flags get`,
   `flags set`, `flags unset`, `flags audit [--verify]`.
5. Each CLI mutation MUST capture `actor` (from `--actor` arg or
   `FF_ACTOR` env var) and `reason` (from `--reason` arg).
6. Mutations to flags marked `sensitive: true` in environment `prod`
   MUST require an `--approver` argument distinct from the actor.
7. Bucketing MUST use SHA256 by default and HMAC-SHA256 with a
   per-flag secret when the flag has `sensitive: true`.
8. The audit log MUST be append-only JSONL with hash-chain entries
   (each entry includes hash of canonical-JSON-serialized previous
   entry).
9. An `flags audit --verify` command MUST walk the audit log and
   report the first index where the hash chain diverges, or
   "verified" if intact.
10. In `prod` environment, the loader MUST verify `flags.yaml.sig`
    against a trusted public key list before accepting changes.
    Signature failure MUST leave the previous good manifest in
    memory.
11. New flag creation MUST land in `state: disabled-pending-review`
    and require an explicit second-approver action to transition to
    `enabled` in prod.
12. The kill-switch field on a flag MUST be evaluated before rollout
    rules; a true kill switch MUST return the default value
    regardless of rollout / allowlist.
13. The watcher MUST hot-reload `flags.yaml` within 2 seconds of file
    mtime change; kill-switch flips MUST propagate within 30 seconds
    end-to-end including poll jitter.
14. On cold start when the manifest is unreachable, the SDK MUST
    fail-closed (return the default value baked into the flag
    definition embedded in code via the SDK helper).
15. Configuration of trusted signing keys MUST be via a separate
    file (`feature_flags-trusted-keys.pem`) that itself is managed
    out-of-band from the flag manifest.

## Non-Functional Requirements

- **Performance**: p99 < 1ms eval; CLI mutation < 500ms end-to-end
  including signature + audit-log write.
- **Reliability**: Loader rejects malformed manifest atomically; old
  cache stays live. Audit-writer failure buffers in-memory and
  retries; never blocks evaluation.
- **Auditability**: Every mutation produces a hash-chain entry. Log
  is shippable to Splunk / Elasticsearch via standard JSONL
  collectors.
- **Security**: Signed manifest in prod; HMAC bucketing for
  sensitive flags; two-person approval gate on prod sensitive
  mutations; actor identity required on every write.
- **Maintainability**: Follows existing `src/superclaude/` layout
  conventions; tests under `tests/feature_flags/`; UV for all
  Python ops.
- **Portability**: OpenFeature SDK compat means downstream consumers
  can swap to LaunchDarkly / Flagsmith / Unleash by replacing the
  provider only.

## Acceptance Criteria

- Given a valid `flags.yaml`, when SDK evaluates a flag with a
  matching rollout, then the result is deterministic per
  targeting key and consistent across calls.
- Given a flag with `kill_switch: true` and `rollout: 100`, when
  SDK evaluates, then the result is the default (kill switch wins).
- Given a sensitive flag in prod, when `flags set` is invoked
  without `--approver`, then the CLI exits non-zero with a clear
  error.
- Given an audit log with intact hash chain, when
  `flags audit --verify` runs, then it reports "verified".
- Given a tampered audit log entry, when `flags audit --verify`
  runs, then it reports the first divergent index.
- Given an unsigned manifest in prod environment, when the loader
  runs, then it rejects the manifest and keeps the previous good
  state.
- Given a flag change to `flags.yaml`, when the watcher fires, then
  the SDK returns the new value within 2 seconds.
- Given test coverage measurement, when `pytest --cov` runs over
  `feature_flags/`, then coverage is >= 85%.

## Provenance

This requirements artifact is the adversarial-merged synthesis of
three parallel proposals generated during Wave 3 of the
sc:brainstorm pipeline:

- **proposal-1-opus-architect.md** (opus, architect persona):
  Contributed the OpenFeature SDK conformance scope, the abstract
  `Provider` interface enabling v2 migration, and the kill-switch
  fast-poll separation. Postgres + FastAPI control plane elements
  deferred to v2.
- **proposal-2-sonnet-backend.md** (sonnet, backend persona):
  Selected as base variant (weighted score 4.20 in
  `adversarial/base-selection.md`). Contributed the file-backed
  YAML store, watchdog-driven hot reload, atomic CLI mutator, and
  operational-simplicity v1 scope.
- **proposal-3-haiku-security.md** (haiku, security persona):
  Contributed signed-manifest verification (scoped to prod),
  hash-chained JSONL audit log, `sensitive: true` opt-in
  metadata with HMAC bucketing, two-person review gate for prod +
  sensitive flags, and fail-closed-on-create semantics.

Adversarial pipeline metadata:

- Wave 3 convergence score: 0.82 (threshold 0.65; PASS).
- Round-by-round debate captured in
  `adversarial/debate-transcript.md`.
- Pairwise conflict resolution captured in
  `adversarial/diff-analysis.md` (8 conflicts, 0 unresolved).
- Element-level adoption captured in `adversarial/merge-log.md`
  (3 base + 8 layered + 3 deferred-to-v2).
- Refactor sequencing captured in `adversarial/refactor-plan.md`
  (9 implementation steps).
- Domain `code` + handoff `task` route to `feature-template` in
  Wave 4 (see `handoff/task-feature-flag-system.md`).
- Enrichment: Wave 2A skipped (generic topic, no @file reference);
  proposals reference OpenFeature spec from training knowledge.
- Models rotated: opus → architect (P1), sonnet → backend (P2),
  haiku → security (P3); blind_mode: false; depth: standard.
