---
proposal_id: 1
persona: architect
model: opus
lens: long-term platform fit, runtime governance, allowlist discipline
---

# Proposal 1 — Architect: Pilot-Only With Governance Hooks, Default Posture "Disallow Without Pilot"

## Position

This is a **runtime-allowlist decision**, not a "is Bun cool" decision. The right output is a policy document with governance teeth, not a benchmark chart. The platform team's job is to make this question answerable for every team going forward, not to bless a single service. The default posture should be **disallow without explicit pilot approval**, with a clear path through pilot → graduate → general-allow that's identical to how we'd treat any new runtime, framework, or load-bearing dep.

## Recommended policy shape

```
status: pilot-only-with-conditions
conditions:
  - one (1) pilot service at a time
  - revert playbook rehearsed before customer traffic
  - observability parity statement signed off by SRE
  - native-dep matrix verified for the pilot's deps
  - 90-day pilot window, mandatory review
graduation_criteria:
  - zero SEV-1/SEV-2 attributable to runtime
  - observability stack at parity (no silent gaps)
  - revert path remained mechanical (no API drift)
  - explicit recommendation from the pilot team + SRE
next_review: 2026-Q4
```

## Why "pilot-only-with-conditions" beats both alternatives

**vs "disallow"**: Bun's WebSocket numbers are real enough that a flat disallow leaves measurable performance on the table for exactly the workload the new service needs. We'd be saying no on incomplete evidence.

**vs "allow"**: Bun is younger than Node; single-vendor (Oven); has known gaps in observability auto-instrumentation that matter to *our* stack specifically. "Allow" implies we have evidence at scale on our exact workload. We don't.

**The middle path forces evidence collection.** A 90-day bounded pilot with a revert playbook is the cheapest way to convert "claimed benchmarks" into "tested on our infra." If the pilot succeeds on objective criteria, graduate. If it doesn't, revert and document. Either outcome is defensible to leadership.

## Governance hooks that must exist day one

1. **Lint discipline**: `eslint-plugin-no-restricted-globals` rule banning `Bun.*` API usage in pilot codebases. Mechanical revert depends on this. Without it, a junior engineer introduces `Bun.file()` in week 3 and the revert costs days.
2. **Version pinning**: Pilot service pins to a specific Bun minor (e.g., 1.2.x). Bumps require platform-team approval, just like Node LTS bumps. FR7.
3. **Observability gate**: Before pilot traffic, SRE signs off on the observability parity statement (FR5). Any gap is either shimmed or marked as a manual instrumentation procedure with a runbook entry. No silent gaps.
4. **Pilot exit criteria written *before* pilot start**: not "we'll know it when we see it." Specific failure surfaces (one SEV-2 attributable to runtime; one observability gap that hid degradation; one native-dep regression that broke prod) trigger revert. Documented.
5. **Bun version owner**: Named individual on the platform team owns the Bun-version policy parallel to whoever owns Node LTS today. Without an owner, the policy decays.

## What I'd push back on

The "just adopt Bun, it's faster" framing is wrong even if the numbers are right. Runtime adoption without governance is how you end up with five runtimes nobody owns, security policies that diverge, observability that's silently degraded, and a hiring story that's "well, depends which service." We have one of these stories already (the NestJS service); we don't need a second axis of fragmentation.

The "we should do a quick comparison and decide" framing also misses the point: the comparison is the *easy* part. The hard part is the governance discipline that survives the comparison.

## Cost

The pilot itself is ~3 engineering weeks (porting + observability work + revert rehearsal). The policy + governance work is ~1 week of platform time. Total: ~4 weeks of engineering against a 90-day pilot calendar.

## Tradeoff this proposal accepts

The WebSocket gateway team waits ~3 weeks longer than they would if we just said yes today. That's the cost of doing this defensibly. The alternative — saying yes without governance — pushes risk onto every service that comes after.
