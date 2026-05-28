---
task_id: TASK-FEATURE-FLAG-SYSTEM-001
title: "Implement v1 feature flag system (file-backed, OpenFeature-compatible)"
template: feature-template
domain: code
status: pending
priority: medium
owner: unassigned
created: 2026-05-27T00:00:00Z
source_artifact: ../merged-requirements.md
source_brainstorm: ../seed-brief.md
estimated_effort: 5-8 days
acceptance_gate: tests passing + coverage >= 85% + benchmark p99 < 1ms
---

# Task: Implement v1 Feature Flag System

## Context

This task is the Wave-4 handoff from a sc:brainstorm run on the topic
"implementing a feature flag system". The merged requirements artifact
(`../merged-requirements.md`, convergence 0.82) defines the v1 scope:
file-backed OpenFeature-compatible flag system with hash-chained audit,
signed manifest in prod, and two-person review for sensitive flags.

The base architecture is sonnet/backend's file-backed YAML store with
layered adoptions from opus/architect (SDK conformance, provider
interface, kill-switch fast-poll) and haiku/security (signing, audit
hash chain, sensitive metadata, fail-closed-on-create).

## Acceptance Criteria

(Verbatim from `../merged-requirements.md` § Acceptance Criteria.)

- Deterministic evaluation per targeting key.
- Kill switch overrides rollout rules.
- Sensitive prod mutations require `--approver` distinct from actor.
- `flags audit --verify` reports verified or first divergent index.
- Unsigned manifest in prod is rejected; previous good state kept.
- Watcher hot-reload propagates flag changes within 2 seconds.
- `pytest --cov feature_flags` >= 85%.

## Checklist

### Phase 1 — SDK and provider boundary

- [ ] Create `src/feature_flags/sdk/openfeature_client.py` with
      `get_boolean_value`, `get_string_value`, `get_object_value`.
- [ ] Create `src/feature_flags/provider/base.py` with abstract
      `Provider` class.
- [ ] Create `src/feature_flags/provider/file_provider.py`
      implementing the abstract Provider against the in-memory
      flag map.
- [ ] Unit tests for SDK method signatures vs OpenFeature spec.

### Phase 2 — File store + watcher

- [ ] Define Pydantic schema for `flags.yaml` in
      `src/feature_flags/storage/schema.py`.
- [ ] Implement `src/feature_flags/storage/file_loader.py` with
      atomic parse + previous-state preservation on error.
- [ ] Implement `src/feature_flags/storage/watcher.py` using
      `watchdog` to detect mtime changes and trigger reload.
- [ ] Unit tests for malformed YAML rejection, atomic swap.

### Phase 3 — Bucketing

- [ ] Implement `src/feature_flags/bucketing.py` with SHA256
      default and HMAC-SHA256 for `sensitive: true`.
- [ ] Per-flag secret salt resolution: env var for dev,
      secrets-manager hook stub for prod (interface only in v1).
- [ ] Unit tests for stickiness + distribution (KS test on
      uniform).

### Phase 4 — Audit log

- [ ] Implement `src/feature_flags/audit/jsonl_writer.py` writing
      hash-chained entries.
- [ ] Implement `src/feature_flags/audit/verifier.py` for the
      `--verify` path.
- [ ] Bootstrap entry with `prev_hash = sha256("genesis")`.
- [ ] Unit tests for chain integrity + tamper detection.

### Phase 5 — CLI

- [ ] Implement `src/feature_flags/cli.py` with click subcommands:
      `list`, `get`, `set`, `unset`, `audit`.
- [ ] Enforce `--actor` / `FF_ACTOR` requirement on all mutations.
- [ ] Enforce `--approver` requirement on prod + sensitive
      mutations; validate approver != actor.
- [ ] Unit + integration tests for each subcommand.

### Phase 6 — Signed manifest (prod only)

- [ ] Implement `src/feature_flags/signing/verifier.py` for
      detached signature verification.
- [ ] Trusted key list at `feature_flags-trusted-keys.pem` (out of
      band).
- [ ] Skip verification with INFO log when `FF_ENV != prod`.
- [ ] Unit tests for signature pass + fail + key rotation.

### Phase 7 — Kill-switch fast path

- [ ] Evaluator orders kill_switch check before rollout rules.
- [ ] Watcher fast-poll at 1s interval when any flag has a recent
      kill-switch mutation.
- [ ] Integration test: flip kill switch via CLI, measure SDK
      reflection latency < 30s end-to-end.

### Phase 8 — Tests and docs

- [ ] Run `uv run pytest tests/feature_flags/ -v` — all pass.
- [ ] Run `uv run pytest --cov=feature_flags` — coverage >= 85%.
- [ ] Run benchmark suite — p99 eval < 1ms.
- [ ] Author `docs/feature-flags.md` covering schema, CLI usage,
      audit verification, signing setup.

## Out-of-Scope (for v2 follow-up tasks)

- PostgresProvider implementation.
- FastAPI control plane.
- Admin UI.
- Redis pub/sub push channel.
- Per-tenant isolation within an environment.
- PyPI publication of the SDK.

## References

- Merged requirements: `../merged-requirements.md`
- Seed brief: `../seed-brief.md`
- Adversarial debate transcript: `../adversarial/debate-transcript.md`
- Base selection rationale: `../adversarial/base-selection.md`
- Refactor / implementation plan: `../adversarial/refactor-plan.md`
- Element-level merge adoption log: `../adversarial/merge-log.md`

## Provenance

Auto-generated by sc:brainstorm Wave 4 via task-builder routing
(domain=code → feature-template). Source artifact:
`../merged-requirements.md` (convergence 0.82, status=PASS).
