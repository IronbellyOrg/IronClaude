# Base Selection

## Quantitative Scoring (50% weight)

| Metric | Weight | Variant A (OVM) | Variant B (OVL) | Computation |
|--------|--------|-----------------|-----------------|-------------|
| Requirement coverage (RC) | 0.30 | 0.95 | 0.92 | A maps to all 8 preamble §7 sections + 5 of 5 generalization shapes + falsifier; B same + extras. A slightly higher because it explicitly addresses preamble §5 "runbook a fresh agent can pick up" with promotion-alongside semantics. |
| Internal consistency (IC) | 0.25 | 0.96 | 0.95 | Both very consistent; A has no contradictions; B has minor friction between "no new agents" (§7.2) and `next_actor: downstream-agent` (which is operational, not an agent class). |
| Specificity ratio (SR) | 0.15 | 0.88 | 0.78 | A names concrete tools (`apt-cache show`, `dpkg -L`, `pip show`, `npm view`, `gh api`), concrete cache path, concrete pattern file, concrete URL template; B more abstract ("a tool that resolves the artifact's contract"). |
| Dependency completeness (DC) | 0.15 | 0.92 | 0.90 | Both cite §10.6, §11.2, §14.5.2, §17.7 directly; both resolved. Similar. |
| Section coverage (SC) | 0.15 | 1.00 | 1.00 | Both have all 8 §7 sections |
| **quant_score** | | **0.94** | **0.91** | A: (0.95×0.30)+(0.96×0.25)+(0.88×0.15)+(0.92×0.15)+(1.00×0.15)=0.940 / B: (0.92×0.30)+(0.95×0.25)+(0.78×0.15)+(0.90×0.15)+(1.00×0.15)=0.913 |

## Qualitative Scoring (50% weight) — Additive Binary Rubric

### Completeness (5 criteria)

| # | Criterion | A | B |
|---|-----------|---|---|
| 1 | Covers all explicit requirements from preamble §7 | MET (§1-§8 present) | MET |
| 2 | Addresses edge cases and failure scenarios | MET (§5 lists 4 explicit limits) | MET (§5 lists 3 + risk-to-sufficiency claim) |
| 3 | Includes dependencies and prerequisites | MET (cites WebFetch availability, §10.6 pattern, §14.5.2 promotion gate) | MET (same set) |
| 4 | Defines success/completion criteria | MET (§7 falsifier with explicit assertions) | MET (§7 falsifier with explicit assertions) |
| 5 | Specifies what is explicitly out of scope | MET (§8: 8 items) | MET (§8: 8 items) |

**Completeness subtotal: A 5/5, B 5/5**

### Correctness (5 criteria)

| # | Criterion | A | B |
|---|-----------|---|---|
| 1 | No factual errors / hallucinated claims | MET — every claim re-verifiable against SKILL.md cited sections | MET — same standard |
| 2 | Technical approaches feasible with stated constraints | MET — Bash + WebFetch + context7 are existing tools | MET — same |
| 3 | Terminology used consistently | MET — "seat" used throughout | MET — "mode" used throughout |
| 4 | No internal contradictions | MET | MET (minor friction §7.2 vs §4.5 noted in IC scoring) |
| 5 | Claims supported by evidence or rationale within the document | MET — every amendment numbered with location | MET — same |

**Correctness subtotal: A 5/5, B 5/5**

### Structure (5 criteria)

| # | Criterion | A | B |
|---|-----------|---|---|
| 1 | Logical section ordering | MET | MET |
| 2 | Consistent hierarchy depth | MET (§3 → 3.1-3.7) | MET (§3 → 3.1-3.9) |
| 3 | Clear separation of concerns between sections | MET | MET |
| 4 | Navigation aids | MET (numbered amendments, bullet refs to §sections) | MET (same) |
| 5 | Follows conventions of artifact type (preamble §7) | MET | MET |

**Structure subtotal: A 5/5, B 5/5**

### Clarity (5 criteria)

| # | Criterion | A | B |
|---|-----------|---|---|
| 1 | Unambiguous language | MET — concrete tools, concrete file paths | MET — but "a tool that resolves the artifact's contract" is intentionally abstract |
| 2 | Concrete rather than abstract | MET — toolkit enumeration, cache directory, pattern file | NOT MET (partial) — toolkit left to classifier |
| 3 | Each section has a clear purpose | MET | MET |
| 4 | Acronyms / domain terms defined on first use | MET (OVM defined in §2; verification seats defined in table) | MET (OVL defined in §2; verification modes defined in table) |
| 5 | Actionable next steps or decision points clearly identified | MET (each §3.X amendment has concrete change) | MET (same) |

**Clarity subtotal: A 5/5, B 4/5** (B loses on Concrete-vs-Abstract per C-004 finding)

### Risk Coverage (5 criteria)

| # | Criterion | A | B |
|---|-----------|---|---|
| 1 | Identifies at least 3 risks with probability/impact | MET (§5 lists 4 explicit + token/wall-clock cost analysis) | MET (§5 lists 4 explicit) |
| 2 | Provides mitigation strategy for each risk | MET (each risk has explicit mitigation) | MET (same) |
| 3 | Addresses failure modes and recovery procedures | MET (network/rate-limit cache miss → "deferred" not "skipped") | MET (V-Upstream-Available lookup failure → V-Deferred-Outcome fall-through is itself a runbook) |
| 4 | Considers external dependencies and their failure scenarios | MET (cache staleness; tool unavailability) | MET (tool unavailability via fall-through) |
| 5 | Includes monitoring or validation mechanism | MET (eval falsifier; meta-eval-friendly contract fields) | MET (eval falsifier; meta-eval integration) |

**Risk Coverage subtotal: A 5/5, B 5/5**

### Invariant & Edge Case Coverage (5 criteria)

| # | Criterion | A | B |
|---|-----------|---|---|
| 1 | Addresses boundary conditions for collections (empty / single / max) | MET (empty `outcome-claims.yaml` vacuously passes cond 10; cost scales with diff's external-surface area not diff size) | MET (vacuous-pass also addressed) |
| 2 | Handles state variable interactions across component boundaries | MET (cross-skill: shared ref; promotion-alongside; deferred-outcomes dir moves with work-unit) | MET (cross-skill: contract is the shape; recursive reflect-on-consumer pattern) |
| 3 | Identifies guard condition gaps | NOT MET — A §5 mitigation list does not address `--no-install-recommends` parser robustness (INV-002 caught this) | NOT MET — same gap (INV-002 applies to both) |
| 4 | Covers count divergence scenarios | NOT MET — claim-extraction per-line vs per-package not specified (INV-003 noted, LOW severity) | NOT MET — same |
| 5 | Considers interaction effects when features combine | MET (cross-skill plumbing) | MET (cross-skill via artifact contract) |

**Invariant Edge Case subtotal: A 3/5, B 3/5** (both lose on INV-002 + INV-003; both pass the floor of 1/5)

### Qualitative Summary

| Dimension | A | B |
|-----------|---|---|
| Completeness | 5/5 | 5/5 |
| Correctness | 5/5 | 5/5 |
| Structure | 5/5 | 5/5 |
| Clarity | 5/5 | 4/5 |
| Risk Coverage | 5/5 | 5/5 |
| Invariant & Edge Case Coverage | 3/5 | 3/5 |
| **Total** | **28/30 = 0.933** | **27/30 = 0.900** |

### Edge Case Floor Check

- A: 3/5 → meets floor (≥1/5) → eligible
- B: 3/5 → meets floor → eligible

## Position-Bias Mitigation

| Criterion | Variant | Pass 1 (A→B) | Pass 2 (B→A) | Agreement | Final |
|-----------|---------|---|---|---|---|
| All criteria above | A | (as scored) | (as scored) | Agreed | (as scored) |
| All criteria above | B | (as scored) | (as scored) | Agreed | (as scored) |

No criteria-level disagreements requiring re-evaluation. Both passes converge on the same per-criterion verdicts.

## Combined Scoring

| Variant | quant × 0.50 | qual × 0.50 | **Combined** |
|---------|--------------|--------------|--------------|
| **A (OVM)** | 0.940 × 0.50 = 0.470 | 0.933 × 0.50 = 0.467 | **0.937** |
| **B (OVL)** | 0.913 × 0.50 = 0.457 | 0.900 × 0.50 = 0.450 | **0.907** |

**Margin: 0.030 (3.0%) — within 5% tiebreaker zone.**

## Tiebreaker Protocol

**Level 1 — Debate performance (Step 2 scoring matrix):**

- A wins: C-004 (toolkit), C-012 (falsifier), U-001/U-002/U-003/U-004 (4 unique contributions)
- B wins: C-001 (naming), C-010 (cross-skill), U-005/U-006/U-007/U-008/U-009 (5 unique contributions)
- MERGE: C-002, C-005, C-007, C-008 (4 merged points)

Counting clear wins: A = 6 points; B = 6 points. **Level 1 tie.**

**Level 2 — Higher correctness criteria count:**

- A: 5/5 correctness
- B: 5/5 correctness

**Level 2 tie.** Proceed to Level 3.

**Level 3 — Input order:**

A is variant 1 (input order). **A wins tiebreaker.**

## Selected Base: Variant 1 (Proposal A — OVM)

**Selection rationale (combined-score evidence):**
- Higher quantitative score (0.940 vs 0.913) driven primarily by **SR (specificity ratio)**: A's enumerated toolkit, concrete cache directory, concrete pattern file, concrete URL template versus B's classifier-picks abstraction.
- Higher qualitative score (28/30 vs 27/30) driven by **Clarity dimension #2 (Concrete vs Abstract)** — B loses one criterion on toolkit abstraction.
- Margin is within tiebreaker zone (3%); both are clearly high-quality and substitutable.
- Tiebreaker level 3 (input order) gave the deciding edge.

**Strengths to preserve (from base A):**
1. Concrete external-spec toolkit enumeration with explicit Bash + WebFetch + context7 + tavily ordering and 24h cache (§3.2)
2. Diff-implicit claim extraction with regenerable `refs/claim-extraction-patterns.yaml` pattern table (§3.1)
3. Per-claim deferred-outcomes file at `<output>/deferred-outcomes/<claim_id>.yaml` with promotion-alongside semantics (§3.2 + §3.5)
4. Active iteration-1 falsifier eval (§7)
5. Promotion-action enum stability via parallel `promotion_deferred_outcomes_count` field (§3.5)
6. Evidence-validator runbook schema validation (§3.4)

**Strengths to incorporate from non-base B:**

| ID | From B section | What to incorporate | Where in merged base |
|----|---------------|--------------------|----------------------|
| INC-01 | B §3.1 (V-Deferred-Logical mode) | Add 5th verification mode for "second-order reasoning the audit declines at this tier" with tier-escalation routing | Extend A's §3.1 4-seat taxonomy to a 5-mode taxonomy (4 OVM seats + V-Deferred-Logical) |
| INC-02 | B §3.5 (`outcome_verified` derived field) | Add derived single-axis boolean for consumers that don't want to parse 4-seat counters | A §3.3 contract fields — add `outcome_verified: bool` after the per-seat counters |
| INC-03 | B §3.7 (cond 10 formulation) | Cond 10 = `outcome_claims_failed == 0 AND (outcome_verified == true OR deferred_outcomes_runbook_present == true)` | Replace A §3.5's `outcome_claims_failed == 0` with the merged formulation |
| INC-04 | B §3.6 (presence check) | Evidence-validator presence-checks every actionable finding has an `outcome-claims.yaml` row | Extend A §3.4 with both schema validation AND presence check |
| INC-05 | B §3.9 (artifact-shape cross-skill) | Drop A's `_shared/outcome-verification/` shared-refs directory; sibling skills inherit by writing valid `outcome-claims.yaml` | Replace A §3.7 — keep `refs/claim-extraction-patterns.yaml` in `sc-reflect-protocol/refs/` only |
| INC-06 | B §4.5 (recursive reflect-on-consumer pattern) | `next_actor: downstream-agent`, `next_action: run sc:reflect --mode post against <consumer-repo>` runbook | Add to A §4 as a new generalization shape (cross-service contract drift) |
| INC-07 | B §6 final paragraph (§19.2 INV-023 hardening integration) | Explicit linkage of OVM falsifier to the v1.1 sufficiency-claim hardening trajectory | Append to A §6 backward-compat |
| INC-08 | B §4 (Bonus shape: test-suite invariant V-Deferred-Logical) | Add as a 6th generalization shape (bonus) | Append to A §4 |
| INC-09 | B §3.2/§7 supplementary (`outcome-verification-deferred-runtime-config.yaml` falsifier) | Keep A's iteration-1-active docker falsifier; add B's deferred-runtime-config falsifier as sibling case | Append to A §7 |

**Changes not being made (transparency — debate-rejected):**

| Diff | Non-base approach | Rationale for keeping base |
|------|--------------------|----------------------------|
| C-001 (naming) | B's "Ledger" | Base name "OVM" retained for backward-compat with this brainstorm cycle; mechanism is what matters, name is cosmetic. Acceptable to rename to "OVL" at task-builder time if user prefers. |
| C-004 (toolkit abstraction) | B's classifier-picks | A's enumerated toolkit is downstream-executable; abstraction loses precision needed for /task agent to know what to run |
| C-012 (falsifier staging) | B's skeleton-pending | Docker case is real; active fixture is more useful eval signal than skeleton |
| A's §3.7 shared-refs directory | (kept in base originally) | OVERRIDDEN by INC-05; B's lighter approach wins |

**Mechanism-text additions required (from invariant probe warnings):**

| Source | Issue | Required addition |
|--------|-------|-------------------|
| INV-002 | `--no-install-recommends` parser scope | Merged §3.2 must specify which flag spellings the parser handles (`--no-install-recommends`, `--no-install-suggests`, `-o APT::Install-Recommends=false`) AND multi-line continuation handling, OR explicitly list unhandled forms as known limitations in §5 |
| INV-003 | Per-line vs per-package claim granularity | Merged §3.1 must specify: one implicit claim per `(package, install-line)` pair (per-package granularity, single line) |
| INV-005 | Multi-mode claim precedence | Merged §3.1 must add a precedence rule: V-Deferred-Logical > V-Deferred-Outcome when the logical question, if resolved, would collapse the runtime claim to V-Upstream-Available |
| A-001 | WebFetch addable without further gate | Merged §5 must explicitly document the assumption AND specify a fallback runbook if WebFetch addition is gated by policy |
| A-002 | Operator/CI executes deferred runbooks | Merged §5 must list as a known limitation; operator-ignored runbooks remain a downstream-actor responsibility |
| A-003 | apt-cache parser robustness | Covered by INV-002 addition |
