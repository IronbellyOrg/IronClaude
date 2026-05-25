---
proposal_id: 2
agent_label: Agent B
persona: refactorer
blind_mode: true
lens: smallest-blast-radius, paying off existing debt, minimum viable consolidation
---

# Proposal 2 — Agent B: Extract Common Trunk, Leave Per-Service Tails — Don't Build a Plugin Framework

## Position

Agent A's "plugin flows + adapters" design is engineering work justified by a model of how drift happens that I do not think survives contact with the actual codebase. The drift that hurts us is in **the primitives** (lockout threshold, password policy enforcement location, JWT library import path), not in the flows. Most of the per-service code today is genuinely service-specific (session-cookie handling has no analog in mobile; PKCE has no analog in api) and **forcing it into a plugin framework adds abstraction without removing duplication**. The right move is the smallest one that eliminates the *measured* drift sources.

## What to build

`services/shared/auth_core/` containing **only the policies and the audit emitter**:

1. **`policy.py`** — single password_policy, lockout_policy, jwt_validation, audit_event_schema. ~300 LOC total. This is what eliminates Incident 1 (JWT CVE asymmetry) and Incident 2 (password policy update missed mobile).
2. **`audit_emitter.py`** — single CloudEvents emitter writing to one Kafka topic. ~150 LOC. Plus three small legacy-shim consumers (one each for CloudWatch, Splunk, S3) — ~50 LOC each, deleted after 90 days. ~300 LOC total.

Per-service `auth/*.py` files **stay**, but are refactored to import policy + audit from the core. Each loses ~300-400 LOC of duplicated policy/audit code; each retains its protocol-specific flow logic (CSRF, PKCE, api-key HMAC) in the service repo where the team that owns the protocol can iterate without coordinating across teams. Net change: -1200 LOC duplicated, +450 LOC in the new core, three service modules slimmer and clearer.

## Why this shape

**The measured drift incidents were primitive-level, not flow-level.** Incident 1 was a transitive import of `security_utils/jwt.py` — solved by having one `jwt_validation` policy in the core that all three import explicitly. Incident 2 was a password-policy length update — solved by having one `password_policy` constant. Neither was a flow-level drift.

**Plugin frameworks have a re-cost.** Every protocol-specific concern someone wants to add later (a new SAML SSO flow, a new device-fingerprint check) requires either changing the plugin interface or working around it. The three service-repo locations let each team move at their own pace.

**Per-service flow code is more honest about ownership.** Mobile_bff team owns PKCE; api team owns OAuth2 client_credentials; web team owns CSRF + sessions. Putting all of that in a shared core means **three teams now coordinate on every flow change** — that's an organizational tax that doesn't show up on the architecture diagram.

**~300 LOC of shared policy + ~300 LOC of shared audit is auditable in two PRs.** ~3000 LOC of plugin framework is auditable in… many.

## Migration sequencing

1. Phase 0: build core (policies + emitter + legacy shims). ~2 engineer-weeks.
2. Phase 1: refactor `services/api` to import from core. Shadow-mode → 5% → 50% → 100%. ~2 engineer-weeks.
3. Phase 2: refactor `services/web`. ~2 engineer-weeks (CSRF stays in web; only policy + audit imports change).
4. Phase 3: refactor `services/mobile_bff`. ~3 engineer-weeks (biggest test surface; PKCE flow stays in mobile_bff).
5. Phase 4: delete duplicated policy/audit code in each service; decommission legacy shims after 90-day overlap. ~1 engineer-week.

Total: ~10 engineer-weeks, comfortably fits Q3 with margin for the inevitable surprise.

## What I'd push back on

Agent A is treating the consolidation as an opportunity to **rebuild** auth, not to **deduplicate** auth. The original ask was "stop having three different lockout thresholds", not "rebuild login as a plugin framework". The plugin design is genuinely useful if we are also planning to add SAML, OIDC, biometric variants, and per-tenant configuration in the next 12 months — and we are **not**, per the seed brief.

## Cost

~10 engineer-weeks, well inside Q3 with margin for surprises. Roughly half of Agent A's estimate.

## Confidence

High on the smaller-scope claim. The measurable drift sources from the seed brief's Q5 and Q12 are policy-level; addressing them with shared policy + shared audit is necessary AND sufficient. Lower on whether the team would resist a future SAML/OIDC need under this design — but that's a "we'll know when it happens" risk, not a now-cost.
