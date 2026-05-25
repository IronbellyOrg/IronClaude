---
proposal_id: 1
agent: opus:analyzer
focus: root cause, evidence chain, timeline reconstruction
---

# Proposal 1 — Analyzer Lens

## Frame

A post-mortem that cannot name its root cause is just a story. The
first obligation is to reconstruct what actually happened, in order,
with evidence — not the on-caller's recollection at 4am. Everything
else (prevention, comms, runbook updates) is downstream of getting the
timeline and the causal chain right.

## Investigation Spine

1. **Timeline reconstruction (minute-level granularity).**
   Pull from at least three independent sources: deploy system audit
   log (start, finish, who triggered), application logs (first error
   line, error rate inflection), and infra metrics (CPU/memory/latency
   shape change). Cross-reference until each event has at least two
   sources confirming it. If a step has only one source, mark it
   "single-witness" and prioritize evidence gap closure before
   concluding root cause.

2. **Diff the deploy.**
   The deployed artifact differs from the previous known-good build by
   exactly some set of: code commits, config changes, dependency
   bumps, infra-as-code changes, secret/credential rotation. Enumerate
   all five. The change-surface enumeration is the candidate-cause
   pool. Anything not in that pool is excluded by construction.

3. **Failure mode classification.**
   Tag the failure: (a) deterministic on-startup, (b) deterministic on
   first request, (c) load-dependent, (d) time-dependent, (e)
   data-dependent (only triggered by certain payloads), (f) external
   dependency drift. Each tag has a different evidence signature —
   e.g., (c) shows up as latency tail growth before error rate jump.
   Picking the wrong class wastes hours.

4. **Hypothesis testing.**
   Form 2-3 competing hypotheses. For each, list the evidence that
   would support and the evidence that would refute. Run the cheap
   refutations first. Bias-check: the first hypothesis is usually
   wrong because it pattern-matches to the on-caller's most recent
   debugging session, not to this incident.

5. **Root cause vs. contributing factors.**
   Root cause is the smallest change that, reversed in isolation, would
   have prevented the incident. Contributing factors are conditions
   that turned the root cause into an outage — missing test coverage,
   off-hours deploy with no canary, no automated rollback, no paging on
   staging-only failures. The post-mortem must list both, separately.

## Acceptance for "investigation complete"

- Timeline events each have ≥2 source citations.
- Exactly one root cause named, written as a counterfactual ("had X
  not changed, the incident would not have occurred").
- Contributing factors listed with prevention leverage per item.
- Hypotheses considered but rejected are documented with the refuting
  evidence (avoids re-debating the same theories next week).

## Prevention Priorities

Order by leverage, not by recency. A test that catches this single bug
is low-leverage. A pre-deploy gate that catches the *class* of bug
(e.g., schema validation at deploy time, config diff review for
production-shaped configs, dependency lock verification) is
high-leverage. The post-mortem must explicitly call out which proposed
prevention items are class-level vs. case-level, and bias funding
toward class-level.

## Open Questions Surfaced

- Is there a deploy-system audit log granular enough to reconstruct
  minute-level timeline, or does this incident reveal an observability
  gap that itself needs an action item?
- Was the manual revert idempotent and verified, or did the on-caller
  have to verify state by hand? If the latter, that is a separate
  contributing factor.
- Has any post-mortem in the last 90 days named a similar root-cause
  category? Pattern detection is a force multiplier for prevention
  prioritization.
