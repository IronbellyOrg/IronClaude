---
schema_version: "1.0"
topic: "implementing a feature flag system"
domain: code
strategy: systematic
depth: standard
proposals_target: 3
handoff_target: task
intent_summary: |
  Implement a runtime feature flag system for the Python codebase that lets
  engineers and operators toggle code paths without redeploys. v1 ships an
  OpenFeature-compatible Python SDK boundary backed by a file-based provider
  with hash-chained audit logging, sticky percentage bucketing, kill
  switches, and fail-closed defaults — with a clean v2 seam to a Postgres
  + control-plane upgrade.
context_anchors:
  - kind: convention
    ref: "Python stack (UV + pytest + click) per CLAUDE.md"
    why: "v1 SDK + CLI must align with existing toolchain and package layout"
  - kind: standard
    ref: "OpenFeature spec (openfeature.dev) — Python SDK"
    why: "SDK boundary must be OpenFeature-compatible so provider can swap to LaunchDarkly/Flagsmith/Unleash later"
  - kind: constraint
    ref: "Sub-millisecond hot-path evaluation, in-memory cache, no per-call network I/O"
    why: "Flag eval sits on critical request paths and cannot add latency"
  - kind: constraint
    ref: "Auditable mutations (actor, timestamp, old/new value, reason) for SOX/SOC2-style compliance"
    why: "Production flag changes are governance-relevant events"
  - kind: scope
    ref: "domain=code, strategy=systematic, depth=standard, handoff=task"
    why: "Implementation feature (not greenfield platform) using well-trodden patterns, decomposable into a single MDTM task"
must_preserve:
  - "OpenFeature SDK boundary compatibility (get_boolean_value / get_string_value / get_object_value)"
  - "p99 < 1ms evaluation latency on hot path via in-memory dict cache"
  - "Append-only hash-chained JSONL audit log with offline verifiability"
  - "Sticky percentage bucketing keyed off OpenFeature targeting_key"
  - "Kill switches evaluated before rollout rules; <30s end-to-end propagation"
  - "Fail-closed default for newly created flags"
  - "Two-person approval gate for prod + sensitive flag mutations"
  - "Signed manifest verification in prod environment"
  - ">=85% test coverage on feature_flags/ package"
out_of_scope:
  - "Postgres-backed provider (v2)"
  - "FastAPI/HTTP control plane service (v2)"
  - "Browser-based admin UI (v2)"
  - "Redis pub/sub push channel (v2)"
  - "Per-tenant isolation within a single environment (v2)"
  - "PyPI distribution for external consumers (v2)"
  - "A/B experimentation analytics pipeline (separate system)"
  - "Non-Python SDKs (later, via OpenFeature provider pattern)"
source_confidence: medium
created: 2026-05-27T00:00:00Z
non_interactive: true
---

# Seed Brief: feature-flag-system

## Intent Summary

Implement a runtime feature flag system that lets engineers and operators
toggle code paths without redeploying. The system replaces ad-hoc env-var
toggles and merged-and-forgotten code branches with a governed, auditable,
OpenFeature-compatible primitive.

v1 scope is a file-backed Python implementation that is OpenFeature-compatible
at the SDK boundary, ships hash-chained audit logging, and has a clean
migration seam to a Postgres + control-plane design in v2. The system serves
internal engineering teams as primary users and product managers as
secondary stakeholders for rollout decisions.

Strategy is `systematic`: prefer well-trodden patterns (OpenFeature
conformance, percentage rollouts with sticky bucketing, kill switches,
signed manifests, hash-chained audit logs) over agile experimentation or
enterprise vendor-comparison matrices. Depth is `standard`: production-grade
v1 covering the core 80% without exhaustive edge-case coverage. Handoff is
`task` so the merged requirements decompose into a single MDTM task
artifact via task-builder.

## Context Anchors

- **Stack convention** — Python-first (UV + pytest + click) per project
  CLAUDE.md. v1 implementation lives in `src/superclaude/feature_flags/`
  with tests in `tests/feature_flags/`. Other-language SDKs are deferred.
- **OpenFeature standard** — The de-facto industry spec for flag SDK
  boundaries (openfeature.dev). The Python SDK signature
  (`get_boolean_value`, `get_string_value`, `get_object_value` accepting
  flag key, default, evaluation context) is the conformance target. This
  guarantees swap-ability to LaunchDarkly / Flagsmith / Unleash without
  touching call sites.
- **Latency constraint** — Hot-path evaluation must be sub-millisecond
  (p99 < 1ms) with no per-evaluation network I/O. The implementation
  pattern is: pull config once, cache in-memory dict, hot-reload on file
  change via watcher. Network I/O happens out-of-band on mutation, never
  on read.
- **Governance constraint** — Every flag mutation must produce an audit
  event capturing actor, timestamp, old value, new value, and reason.
  Auditability is SOX / SOC2-relevant; the audit log must be tamper-evident
  (hash-chained) and offline-verifiable. Mutations to flags marked
  `sensitive: true` in `prod` require a distinct second-approver.
- **Scope envelope** — Domain `code` (a software feature being built),
  strategy `systematic` (well-trodden patterns), depth `standard`
  (production-grade core 80%), handoff `task` (single MDTM task file).
  This rules out greenfield platform redesign, customer-facing product
  surfaces, and enterprise vendor-comparison RFP exercises.

## Must Preserve

- **OpenFeature SDK boundary compatibility** — The public API must match
  the OpenFeature Python SDK shape so the in-house provider can later be
  swapped for LaunchDarkly / Flagsmith / Unleash without changing any
  call site.
- **Sub-millisecond hot-path evaluation** — p99 < 1ms via in-memory dict
  lookup with no per-call network I/O. Validated by benchmark under load.
- **Append-only hash-chained audit log** — Each entry includes hash of
  canonical-JSON-serialized previous entry. JSONL format. A `flags audit
  --verify` command walks the chain and reports first divergent index or
  "verified".
- **Sticky percentage bucketing** — Same `targeting_key` always returns
  the same variant for a given flag. SHA256 by default; HMAC-SHA256 with
  per-flag secret when flag is `sensitive: true`.
- **Kill-switch precedence and propagation** — Kill switch evaluated
  before rollout/allowlist rules. End-to-end propagation under 30
  seconds including watcher reload and poll jitter.
- **Fail-closed defaults** — Newly created flags land in
  `disabled-pending-review`. On cold start with unreachable manifest,
  SDK returns the default value baked into the flag definition.
- **Two-person approval gate** — Prod + sensitive flag creation and
  mutation require an `--approver` argument distinct from the actor.
- **Signed manifest verification in prod** — Loader verifies
  `flags.yaml.sig` against a trusted public key list before accepting
  changes. Signature failure leaves the previous good manifest in memory.
- **Test coverage ≥85% on feature_flags/ package** — `pytest --cov`
  measurement is part of acceptance.

## Out of Scope

- **Postgres-backed provider** — File-backed only for v1; Postgres
  deferred to v2 (provider interface designed to permit it without SDK
  changes).
- **FastAPI / HTTP control plane service** — v1 uses CLI-only mutation
  (`flags set`, `flags unset`, etc.); HTTP control plane is v2.
- **Browser-based admin UI** — v1 ships CLI only; admin UI deferred to v2.
- **Redis pub/sub push channel** — v1 uses watcher-driven hot reload on
  local file mtime change; Redis push is v2.
- **Per-tenant isolation within a single environment** — v1 isolates per
  environment (dev/staging/prod) only; per-tenant isolation is v2.
- **PyPI distribution for external consumers** — In-monorepo Python
  package only for v1.
- **A/B experimentation analytics pipeline** — Flags enable experiments;
  the analytics pipeline that measures them is a separate system.
- **Non-Python SDKs** — Other-language SDKs added later via the
  OpenFeature provider pattern; out of scope for v1.
- **Codebase / research enrichment fetch** — Wave 2A skipped this run
  (non-interactive eval, no `@file` reference, well-known OpenFeature
  pattern referenced inline from training knowledge). Source confidence
  recorded as `medium` in frontmatter.
