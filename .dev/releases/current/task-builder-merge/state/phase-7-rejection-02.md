# Phase 7 — Rejection 02

**Finding ID**: SP-12
**Expert**: Michael Nygard
**Severity**: HIGH
**Section targeted**: FR-CONV.6 + K-006 (DNSP Synthetic Finding + Risk K-006)

## Expert Quote (verbatim from release-spec.review.md)

> **Finding**: K-006 ("Synthetic-dnsp findings mask real issues") rates probability=low / impact=low, but the **all-agents-fail guard** is the only protection against degenerate cases — and the spec doesn't define **partial-failure-rate** triggers (e.g., if 5 of 6 partitions emit synthetic-dnsp, that's a systemic failure, not a per-partition flake). Currently each partition silently synthesizes; the team-lead has no aggregate signal.
>
> **Recommendation**: Add to FR-CONV.6 Negative Criterion: "When ≥50% of partitions emit synthetic-dnsp findings in a single A.8 or A.10 gate, the gate MUST escalate to rf-team-lead with severity=CRITICAL rather than collapse via dedup — synthetic-dnsp is a per-partition signal, not a systemic substitute."
>
> **Conflicts-with-G6**: **yes** — extends PR-03's emission contract; PR-03 was CASE-B precisely because it didn't conflict with task-builder behavior, and this recommendation introduces a new aggregate-severity rule not in the original PR-03.

## Five-Step Conflict Resolution

### Step 1 — Classify
The recommendation maps to **CASE-D** if accepted (would convert PR-03 from CASE-B "no conflict" to CASE-D "ADOPT-ADAPTED with new aggregate-severity rule"). It introduces a NEW logic layer — partial-failure-rate detection at the gate level — that PR-03's paradigm-neutral emission contract does not contain. This is a CASE-D-equivalent mechanism extension.

### Step 2 — Identify Invariant
The invariant challenged is **zero-trust QA** (its existing instantiation as the all-agents-fail guard) plus **parallel-research** (cohort-independence per INV-021). PR-03 was selected as BASE on three explicit grounds (per release-spec.md L62 and per-proposal-verdicts.md):
1. Paradigm-neutral by external evidence (39/50 unique win, §6.1)
2. CASE-B no-conflict by direct classification
3. Dual-invariant reinforcement (zero-trust QA + evidence-bound-item)

Adding an aggregate-severity rule introduces a *gate-level* aggregation behavior that did not exist in the original PR-03 and was not analyzed in any of the proposal's adversarial-debate variants.

### Step 3 — FINAL-REPORT Evidence Citation

**§6.1 (P3: DNSP — Proposed Winner with no Conservative Alternative)**:
> | P3: DNSP | **39/50** | **39/50** | Proposed (B) | **ADOPT** | 0.80 |

The Proposed variant (which contains no aggregate-severity rule) is the WINNER. The Conservative variant exists in §6 of the v3.8 adversarial transcript but did not win — and even THAT Conservative variant did not propose partial-failure-rate aggregation.

**§6.3 (Dominant Pattern — Over-Engineering)**:
> "4 of 5 proposals directly ported RF mechanisms that are designed for RF's execution context... When applied to SC's generation context, the same mechanisms introduced unnecessary complexity."

The proposed aggregate-severity rule is a NEW mechanism (not even an RF→SC port — it's an invention beyond PR-03's scope). Inventing new mechanisms during release-spec review is precisely the failure mode §6.3 documents.

**§9 K3 (Accepted disposition)**:
> "K3 DNSP synthetic findings masking real issues. Severity: Low. Mitigation: The synthetic finding is strictly more informative than the current behavior (total validation abort). Conservative HIGH severity ensures the flag is not overlooked. Status: **Accepted**."

K3 explicitly accepts the masking risk at Low severity. SP-12 re-opens this accepted decision and proposes a NEW mitigation (aggregate-severity rule) that was never validated by adversarial debate.

**§9 K1 (Open-status risk acknowledgment)**:
> "K1 Validation agent compliance with gate evidence — Status: Open — requires Sprint execution data"

The FINAL-REPORT pattern is to leave aggregate behavior in Open status pending empirical data, not to invent new aggregation logic during spec drafting. SP-12 violates this pattern.

**INV-021 (parallel-research invariant)**:
The release-spec NFR-CONV.10 reads: "DNSP fires within-agent-instance, not across the cohort (INV-021) ... on one agent's escalation exhaust, N-1 continue to completion before DNSP synthesises a finding". SP-12's aggregate-severity rule is a CROSS-COHORT mechanism — it computes 50% across all partitions, which is exactly the cohort-collapsing behavior INV-021 forbids.

### Step 4 — Decide
**FR supports the invariant (parallel-research cohort-independence + accepted K3 + paradigm-neutrality) → REJECT.**

Adding aggregate-severity rule would:
1. Convert PR-03 from CASE-B to CASE-D (retroactive scope inflation, requires conflict-register row)
2. Violate INV-021 (DNSP fires within-agent-instance, NOT across the cohort) — this is documented in NFR-CONV.10
3. Override §9 K3's accepted disposition (Low severity, accepted as-is, no aggregate mechanism)
4. Invent a NEW mechanism beyond any adversarial-debate variant of PR-03 (Proposed/Conservative both lack this)
5. Re-introduce the §6.3 over-engineering pattern under a different guise (cross-cohort aggregation = new mechanism)

## Protected Invariant
- **Primary**: parallel-research (cohort-independence per INV-021, operationalized in NFR-CONV.10)
- **Secondary**: zero-trust QA (existing all-agents-fail guard already addresses degenerate case)
- **Tertiary**: PR-03 paradigm-neutral CASE-B status (BASE selection foundation)
- **Quaternary**: §6.3 intent-not-implementation principle

## Rationale
The all-agents-fail guard is NOT "the only protection against degenerate cases" as SP-12 claims — it is the protection against the SYSTEMIC degenerate case (zero partitions succeeded). The per-partition case (where N-1 succeed and 1 emits synthetic) is INTENTIONALLY a per-partition signal: the team-lead reads N findings and treats each independently. The synthetic finding's HIGH severity ensures visibility per K3.

Adding a 50%-aggregate-rule would cross-couple partitions in a way that:
- Breaks INV-021 cohort-independence
- Requires the gate to know about partition cardinality (which currently varies by gate stage)
- Forces a meta-mechanism (gate-level severity = f(partition severities)) not present anywhere else in task-builder
- Forces re-analysis of K3's Accepted disposition without new empirical data (K1 pattern violated)

Nygard's release-engineering concern is legitimate at the meta-level (we should know when things are going systemically wrong), but the mechanism to detect this already exists: rf-team-lead reads ALL findings from ALL partitions, and N HIGH findings will trigger its existing escalation behavior (rf-team-lead.md:417, 3 fix cycles per phase). The aggregate threshold is a HUMAN judgment based on inspecting the rf-qa output, not a structural property of the synthetic-dnsp emission.

## Decision
**REJECT SP-12.** Spec remains unchanged. PR-03's emission contract stays at per-partition independence; the all-agents-fail guard and HIGH severity per-partition emission together provide the visibility required.
