---
proposal_id: 3
persona: qa
model: haiku
lens: test surface, edge cases, regression risk, acceptance criteria
---

# Proposal 3 — QA: Define the Failure Modes First, Then Pick the Implementation

## Position

Neither the architect's subsystem nor the refactorer's library-wrap is a sufficient answer on its own, because **both are talking about the shape of the implementation before agreeing on what "correct" means under failure**. Rate limiting is a system that *says no* — and "saying no" has a richer failure surface than "saying yes". I want the failure modes nailed down before either of those proposals enters code review, because they will be the difference between an enterprise customer renewing and filing a SEV-2 ticket on day 30.

## Failure modes I expect to find (and that must be tested for)

1. **Redis is briefly unavailable.** What happens? Fail-open (let the request through) or fail-closed (429 everything)? The seed brief doesn't say. The architect's proposal implies fail-open via the `CounterStore` abstraction; the refactorer's library default is fail-closed. These are different products for the customer. **Decision must be explicit, documented, and policy-configurable per endpoint** — read endpoints likely fail-open, write/mutation endpoints likely fail-closed.

2. **Clock skew between gateway replicas.** The dialogue raises this as an open question. With Redis-Lua atomic increments, the *Redis* clock is authoritative — so skew between gateway pods doesn't corrupt the counter, but it does corrupt the `X-RateLimit-Reset` header (each pod computes "reset" from its own clock). Must test that all replicas agree on reset timestamp to within 1 second. If they don't, the customer's retry logic compounds badly.

3. **Window-boundary doubling.** Fixed-window algorithms have a well-known failure: a client can burst 2x the limit by hitting the last second of one window and the first second of the next. The refactorer's "just use the library" path inherits whatever the library does. **Test this explicitly:** generate load at window boundaries and assert that no client exceeds 1.0× limit averaged over any rolling 60s slice.

4. **Bypass token compromise.** The internal-service bypass header is a high-value secret. Tests must cover: rotated key during a rolling deploy (both old and new keys must be accepted for the rotation window), unknown key rejected (and audited), missing key (treated as not-bypassed, not as error).

5. **Plan-tier change mid-request-stream.** Customer upgrades from `free` to `pro` while sending traffic. Does the new limit apply immediately or at next window? **Specify: immediately at window boundary**, document, test that no in-flight request sees an inconsistent limit.

6. **Header tampering / spoofing.** Anonymous IP path uses `X-Forwarded-For` (or equivalent). Must use the trusted upstream proxy's resolution, not the raw header — otherwise any client can rotate "IPs" trivially and bypass the anonymous limit. Test that spoofed `X-Forwarded-For` is ignored.

7. **429 backpressure overwhelm.** When the limiter is dropping requests at a high rate, the JSON body serialization itself becomes a load source. Test: at sustained 1000 req/s rejection rate, gateway CPU stays under 80%.

8. **Telemetry blind spots.** Without a counter labeled by `(endpoint, plan_tier, outcome)`, we cannot debug "why did this customer get rate-limited" tickets. **Mandatory** — non-negotiable acceptance criterion.

## Test plan (concrete, non-negotiable)

- **Unit (≥30 cases)**: window math (incl. boundary doubling proof), header generation under each outcome, config parsing including malformed cases, bypass-key rotation handling.
- **Integration (≥10 cases)**: middleware + real Redis (Testcontainer), end-to-end through FastAPI test client. Cover Redis unavailability (fail-open vs fail-closed policy), concurrent requests across replicas, plan-tier change mid-stream.
- **E2E load (≥3 scenarios)**: 5-minute sustained at 2x free-tier rate from one principal (expect 1.0× limit enforced, ±2%); burst at window boundary from multiple principals (no client exceeds limit averaged); webhook endpoint excluded scenario (no false-429s).
- **Chaos**: kill Redis mid-test, verify documented behavior; rotate bypass key during load, verify zero false-rejects.

## Acceptance criteria additions (beyond what's in the seed brief)

- Fail-open vs fail-closed behavior is documented per endpoint and tested.
- `X-RateLimit-Reset` agrees across replicas within 1 second.
- Window-boundary doubling test passes (no client exceeds 1.0× over any rolling 60s window).
- `X-Forwarded-For` spoofing test passes (only trusted proxy chain accepted).
- Telemetry includes `rate_limit_decision{endpoint, plan_tier, outcome}` counter — present in canary dashboards before rollout.
- Runbook includes a "customer says they were rate-limited and shouldn't have been" debug procedure with concrete queries.

## What I'd push back on

The architect's proposal is rich but is silent on Redis unavailability behavior — that omission alone is a SEV. The refactorer's proposal is small but inherits library defaults on every failure mode I've listed, which means the *first time we see one of these failures in prod we won't know it's coming*. The right answer adopts the refactorer's "ship soon" instinct but spends the budget on **failure-mode coverage**, not on speculative algorithm pluggability. Test surface comes before scaffolding.

## Cost

~1 extra engineering day vs the refactorer's plan to bring the test surface up. Worth it. Without it we are shipping a system whose failure modes we cannot articulate to the customer.
