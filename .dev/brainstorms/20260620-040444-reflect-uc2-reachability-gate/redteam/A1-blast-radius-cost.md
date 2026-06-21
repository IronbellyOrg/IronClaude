# Red-Team A1 — False-Positive Blast Radius + Cost (quality-engineer, adversarial)

Verdict: **NET-NEGATIVE as proposed.** Salvageable core = advisory-only, opt-in via explicit
machine-readable `durable_sink:` field, capped L2, exempt from rule-3 escalation, reframed from
"real-boot proof" to "does any test assert against the declared sink symbol."

## Governing collision
The host skill is constitutionally **fail-OPEN** (SKILL.md:565 "never abort"; SKILL.md:490 "never STOP";
SKILL.md:962-974 "any unmapped exit → Grounding Gap, never silently Regression"). The proposal's
"fail-closed: unreachable/oracle_mismatch = Regression" **inverts** that load-bearing invariant. The skill
under-claims under uncertainty; the gate as proposed over-claims under uncertainty.

## Findings
1. **BLOCKER — static-scan false positives → halt-fatigue.** `_ =` best-effort discards, lazy/`init()`/`sync.Once`
   binding, plugin/service-locator DI are *idiomatic* and statically indistinguishable from the bug. Routing
   them to `unproven`→Grounding Gap does NOT contain them — SKILL.md:1003-1008 makes a non-empty
   grounding-gaps row *unconditionally* force `status: partial` + `needs_human_decision: true`. 3-8 such
   hits/run on a moderate Go service trains operators to rubber-stamp the exact alarm the gate exists to raise.
   Containment: cap pure-static hits at **advisory L2** (the reuse-auditor precedent SKILL.md:492); never let a
   static finding alone flip `status: partial`.
2. **BLOCKER — real-boot verifier cannot exist under §6.1.1.** Metachar rejection (SKILL.md:503), verb allowlist
   {pytest,ruff,mypy,make,uv,npm,tsc,cargo} (SKILL.md:501 — the prod binary's name isn't in it), 120s/cwd
   (SKILL.md:503,505) structurally forbid booting a real binary. The only "boot" expressible is running the
   executor's OWN test suite — the same suite whose wrong oracle (greps journald) is the bug. **Circularity:**
   the verifier certifies the failure it targets. Containment: descope to "does any test reference the contracted
   sink symbol" (a coverage/Drift signal, advisory).
3. **MAJOR — oracle-identity inference is fragile + slog false-positive.** Resolving the contracted-sink identity
   from prose needs Pass-2 LLM inference (SKILL.md:300/306 — the authors' own fenced-fragile path). A correct
   slog-as-durable-sink architecture gets hardcoded as `oracle_mismatch`. Containment: gate on an explicit
   machine-readable sink declaration, never on inference; absent → out-of-scope, not Grounding Gap.
4. **MAJOR — rule-3 escalation drag kills "Tier-1 only."** SKILL.md:392: UC-2 + any Regression candidate →
   ESCALATE. A static hit declared a "Regression candidate" trips it → whole run to T2 (35-70k vs 3-8k, ~5-9×).
   Containment: exempt reachability findings from rule-3, OR price honestly as T2.
5. **MAJOR — unit-vs-integration stub discrimination is not statically possible.** Legit integration-covered code
   with mixed unit stubs → false `unproven` halt. Containment: drop the discrimination; check only "does any
   test assert against the declared sink symbol."

Most dangerous over-fire: finding 1 (halt-fatigue making the gate's own true-positive invisible).
