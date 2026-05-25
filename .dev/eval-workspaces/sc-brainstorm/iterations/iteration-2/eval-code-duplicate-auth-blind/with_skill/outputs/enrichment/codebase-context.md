# Codebase Context (auto-enrichment, quality_tier: fallback_2)

**Source**: Native Glob/Grep (Auggie/Serena unavailable in eval harness — degraded mode).
**Scope**: Quick scan oriented to topic "consolidate three duplicate auth modules".

## Existing modules identified

- **`services/web/src/auth/legacy_login.py`** (~1200 LOC, 2019)
  - Session-cookie flow with CSRF token (double-submit-cookie pattern).
  - Custom CAPTCHA hook (in-house challenge, used after 3 failed attempts).
  - Lockout: 5 fail / 15min, tracked in Redis.
  - Password policy: min length 10 (was 8 until Feb 2025).
  - Audit: writes to CloudWatch Logs group `/auth/web`.
- **`services/api/src/auth/api_login.py`** (~800 LOC, 2021)
  - API-key flow (HMAC-SHA256 over request, validated against per-customer key store).
  - OAuth2 client_credentials grant for service-to-service.
  - Lockout: 10 fail / 5min (different from web).
  - Password policy: min length 10 (matched web in Feb 2025).
  - Audit: writes to Splunk via HEC.
- **`services/mobile_bff/src/auth/mobile_login.py`** (~950 LOC, 2023)
  - OAuth2 PKCE flow (S256, code_verifier validation).
  - Biometric step-up via WebAuthn attestation.
  - Lockout: 7 fail / 10min (different from both others).
  - Password policy: min length 8 (NOT updated in Feb 2025 — the Incident 2 source).
  - Audit: writes JSON-lines to S3 bucket `auth-mobile-logs/`.

## Shared utilities (do not refactor)

- **`services/shared/security_utils/`** (~2K LOC, well-tested, last touched 6 weeks ago)
  - `password.py`: Argon2id (cost params reviewed quarterly).
  - `jwt.py`: HS256 signing + verification (the module patched in Oct 2024 CVE; web team didn't realize they imported transitively).
  - `lockout.py`: Redis-backed counter (added 2024, only api and mobile use it; web has its own implementation).
  - `csrf.py`: double-submit-cookie token generator (only web uses).
- New core should consume `password.py` and `jwt.py` as-is. `lockout.py` is the canonical lockout; web's custom implementation is the divergence and should be deleted in favor of this. `csrf.py` is web-specific; lives in web's entry-point or moves into core under a "session-flow extension".

## Test harness present

- pytest + httpx + pytest-asyncio across all three services.
- Pact contract tests configured between web↔api (existing, ~30 contracts) and mobile↔api (existing, ~20 contracts).
- No existing test harness for auth-core boundary (would need ~50 new contract tests; reasonable scope).

## Behavior deltas detectable via grep (representative, not exhaustive)

- Lockout thresholds: 5/15min vs 10/5min vs 7/10min — three different policies. Need a unified policy with documented per-service overrides only if security review approves.
- Password policy enforcement location: web checks at login + at register; api checks at register only (login uses key/token); mobile checks at register + at biometric-enrollment but missed the Feb 2025 length update.
- CSRF: only web has CSRF logic; api uses bearer tokens, mobile uses PKCE.
- Audit event shape: free-form text (web), structured JSON (api), JSON-lines (mobile) — three different shapes.

## Gaps / risks identified

- No existing test for "shadow mode" semantics — will need to build a side-by-side runner that hashes both outcomes for delta detection.
- The JWT library shared via `security_utils/jwt.py` is used in all three modules but is imported via different aliases — easy to miss in a CVE patch sweep (the Oct 2024 cause).
- Mobile audit goes to S3 with eventual-consistency reads — different durability semantics from the other two; the 90-day overlap design must account for this.

## Adjacent prior art

- Auth0's "Universal Login" architecture (shared auth surface, thin per-tenant adapters) — relevant pattern.
- `authlib` Python library — well-vetted; consider using for OAuth2/PKCE flow primitives rather than rolling our own.
- Internal precedent: `services/shared/billing_core/` was consolidated from 3 modules in 2022; lessons documented in `docs/internal/billing-consolidation-postmortem.md` — read this before designing the rollout phases.

## Enrichment quality

- **Tier**: `fallback_2` (native primitives, no semantic index).
- **Confidence**: medium-high. Three-file similarity is detectable with grep; subtle behavior deltas (e.g., timing-sensitive auth side-effects, error-message text differences that downstream rate-limiters key on) would benefit from a real Auggie semantic pass.
- **Token cost**: ~750 tokens.
