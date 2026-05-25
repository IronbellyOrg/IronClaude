---
proposal_id: 1
agent_label: Agent A
persona: architect
blind_mode: true
lens: long-term system fit, extensibility, structural correctness
---

# Proposal 1 — Agent A: Build a Cohesive Auth Core With Plugin-Style Per-Service Adapters

## Position

The right shape is **one core + per-service adapter plugins**, not "one core called by three thin facades". The protocol-specific concerns (CSRF for web, OAuth2 PKCE for mobile, HMAC/api-key for api) belong as **first-class extension points in the core**, not as leftover logic in service entry-points. If we keep protocol-specific code in three different repos, we have not solved the drift problem — we have **moved** it from `_login.py` files into `_entry.py` files.

## Architecture

`services/shared/auth_core/`:

1. **`core/authenticator.py`** — orchestrates principal resolution + lockout check + password verification + audit emit. Returns `AuthResult` value object.
2. **`flows/`** — one plugin per flow: `password_flow.py`, `oauth2_client_credentials.py`, `oauth2_pkce.py`, `api_key.py`, `biometric_step_up.py`. Each conforms to a `Flow` protocol (Python `typing.Protocol`).
3. **`policy/`** — single source of truth: `password_policy.py`, `lockout_policy.py`, `csrf_policy.py`. Each is a dataclass + validator function. Per-service override allowed but requires a documented security-review sign-off (enforced at config-load time via a registry of approved overrides).
4. **`audit/`** — unified event publisher. Emits CloudEvents-shaped events to a single Kafka topic; legacy adapters consume from that topic and re-emit to CloudWatch / Splunk / S3 during the 90-day overlap.
5. **`adapters/`** — per-service: `web_adapter.py`, `api_adapter.py`, `mobile_adapter.py`. Each is ~150 lines: wires the relevant `Flow` plugins, handles the HTTP-shape concerns (session-cookie set/clear for web, bearer-token headers for api, OAuth2 redirect handling for mobile).

## Why this shape

**Plugin flows enable structural-CVE-asymmetry prevention.** A CVE in `oauth2_pkce.py` is one PR; all three services consume from the same plugin so all three pick it up on next deploy. CVE asymmetry becomes structurally impossible at the *flow* level, not just at the *primitive* level.

**Adapter pattern keeps service entry-points small.** ~150 lines of HTTP-shape glue is auditable in one PR; 800-1200 lines of intermixed flow + glue (today's state) is auditable in many.

**Override-with-sign-off registry replaces silent divergence.** Today: three lockout thresholds (5/15min, 10/5min, 7/10min) with no documented reason. With registry: choose one as the default (likely 7/10min, the most-recent), allow per-service overrides only if security review approves them at config-load time. Drift becomes opt-in and audited.

**Unified audit via Kafka + 90-day legacy adapters** — this is the *only* design that lets us hit the 90-day overlap requirement without writing the new core's audit pathway twice.

## Migration sequencing

1. Phase 0: build core + adapters in a feature branch; comprehensive unit + contract tests; shadow-mode runner. ~4 engineer-weeks.
2. Phase 1: migrate `services/api` (fewest behaviors, lowest blast radius, best validation of the adapter pattern). ~3 engineer-weeks including shadow → 5% → 50% → 100%.
3. Phase 2: migrate `services/web` (most familiar to most engineers; CSRF correctness validation here). ~4 engineer-weeks.
4. Phase 3: migrate `services/mobile_bff` (largest blast radius, OAuth2 PKCE + biometric step-up). ~5 engineer-weeks.
5. Phase 4: delete legacy modules, decommission 90-day audit-overlap adapters, finalize unified-audit-as-canonical. ~2 engineer-weeks.

Total: ~18 engineer-weeks across ~4 calendar months — fits Q3 deadline.

## What I'd push back on

A proposal that says "thin facades calling core" without addressing **where protocol-specific code lives** has not solved the problem. The drift will re-emerge in the facades because that's where the divergence pressure naturally accumulates — every protocol-specific bug fix lands in a per-service facade, and three months later we have three slightly-different facades.

## Cost

~18 engineer-weeks, single PR set per phase, one release per phase. Single-quarter deliverable for the engineering work; rollout phases extend slightly into Q4.

## Confidence

High on the plugin-flow architecture (Auth0's Universal Login does this; `authlib` is structured this way). Medium on the Kafka-based audit unification — durability under the legacy S3 path may need extra care.
