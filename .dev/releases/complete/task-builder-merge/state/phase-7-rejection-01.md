# Phase 7 — Rejection 01

**Finding ID**: SP-08
**Expert**: Alistair Cockburn
**Severity**: HIGH
**Section targeted**: FR-CONV.6 (DNSP Synthetic Finding — PR-03 emission contract)

## Expert Quote (verbatim from release-spec.review.md)

> **Finding**: The synthetic-dnsp `recommendation` field is hard-coded to "Manual review required — partition agent failed twice". But the use-case (primary actor: human reviewer) doesn't have a clear next step — there's no instruction on **what** to review, **where** the agent's partial output is, or **how** to disposition the finding (accept / re-run / escalate).
>
> **Recommendation**: Expand the recommendation field schema to require three sub-fields: `next_action: <accept-with-justification | re-run-partition | escalate-to-team-lead>`, `review_target: <file:line range OR spawn-log>`, `disposition_owner: <rf-team-lead | task-author>`. Without this, the synthetic finding is a dead-end signal.
>
> **Conflicts-with-G6**: **yes** — challenges PR-03's CASE-B classification by pushing the recommendation contract beyond paradigm-neutral intent-port.

## Five-Step Conflict Resolution

### Step 1 — Classify
The recommendation maps to **CASE-D** if accepted (would convert PR-03 from CASE-B "no conflict, paradigm-neutral port" to CASE-D "ADOPT-ADAPTED with scope extension"). The change is not a simple addition; it expands the emission-contract schema from a paradigm-neutral 5-field shape (severity, source, affected_range, evidence, recommendation) to a 7-field shape (adding next_action, review_target, disposition_owner). This is a CASE-D-equivalent scope inflation.

### Step 2 — Identify Invariant
The invariant challenged is **evidence-bound-item** as it applies to PR-03's emission contract, plus PR-03's **paradigm-neutral CASE-B status** (the foundation of its BASE selection per merged-output.md L9-13 and per-proposal-verdicts.md L4). PR-03 was selected as BASE on Level-1 tiebreaker precisely because it was the ONLY proposal in the v3.8 portfolio that won 39/50 without revision (FINAL-REPORT §6.1) — its paradigm-neutrality is load-bearing.

### Step 3 — FINAL-REPORT Evidence Citation

**§6.1 (P3: DNSP Verdict ADOPT, 39/50 Proposed=Winner)**:
> | P3: DNSP | **39/50** | **39/50** | Proposed (B) | **ADOPT** | 0.80 |

This is the unique row in §6.1 where Proposed equals Winner without a "Conservative Alternative" revision. PR-03's emission contract is the paradigm-neutral baseline that survived adversarial debate without modification.

**§6.3 (Dominant Pattern)**:
> "4 of 5 proposals directly ported RF mechanisms that are designed for RF's execution context... When applied to SC's generation context, the same mechanisms introduced unnecessary complexity. The conservative alternatives succeeded by adapting the *intent* of each RF mechanism to SC's architectural constraints rather than porting the *implementation*."

SP-08 proposes adding three implementation-specific sub-fields (next_action enum, review_target file:line, disposition_owner role) — this is *implementation* detail beyond the *intent* of "manual review required". Per §6.3, this is the precise over-engineering pattern the FINAL-REPORT documented as the dominant rejected approach across 4 of 5 RF->SC ports.

**§9 K3 (Synthetic findings risk)**:
> "K3 DNSP synthetic findings masking real issues — if a failed agent's task range contains critical issues, the synthetic 'manual review required' finding understates the problem. Severity: Low. Mitigation: The synthetic finding is strictly more informative than the current behavior (total validation abort). Conservative HIGH severity ensures the flag is not overlooked. Status: Accepted."

K3 explicitly accepts the bare "manual review required" recommendation as sufficient with HIGH severity. SP-08's expansion would add three fields that K3 deems unnecessary.

### Step 4 — Decide
**FR supports the invariant (paradigm-neutrality + accepted K3 contract) → REJECT.**

Adding `next_action`, `review_target`, `disposition_owner` would:
1. Convert PR-03 from CASE-B to CASE-D (requires conflict-register row, retroactive scope inflation)
2. Re-introduce the §6.3 over-engineering pattern (porting implementation specifics, not intent)
3. Override §9 K3's accepted disposition (Low severity, accepted as-is)
4. Weaken the Level-1 tiebreaker that selected PR-03 as BASE (paradigm-neutral 39/50 unique win)

## Protected Invariant
- **Primary**: evidence-bound-item (emission contract minimalism)
- **Secondary**: PR-03's paradigm-neutral CASE-B status (BASE selection foundation)
- **Tertiary**: §6.3 intent-not-implementation principle (the dominant rejected pattern across v3.8)

## Rationale
The synthetic-dnsp recommendation field's brevity is a feature, not a bug. The minimal "Manual review required — partition agent failed twice" recommendation pairs with HIGH severity (per K3) to ensure visibility without prescribing disposition. Disposition logic belongs to rf-team-lead's existing 3-fix-cycle escalation (rf-team-lead.md:417), not to the synthetic finding itself. Expanding the contract would route disposition through the synthetic finding's schema — which is precisely the kind of mechanism-replacement that §6.3 documents as over-engineering.

Cockburn's use-case-rigor concern is legitimate but addressed at a different layer: the `evidence: <log-path>` field already provides the "where to review" (the spawn log), and rf-team-lead's escalation behavior already provides the "how to disposition". Adding fields to the synthetic finding duplicates these mechanisms.

## Decision
**REJECT SP-08.** Spec remains unchanged. PR-03's emission contract stays at the 5-field paradigm-neutral shape.
