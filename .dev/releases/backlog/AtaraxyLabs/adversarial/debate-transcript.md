# Debate Transcript: Eval+Incorporation Release Plan

- Depth: standard (Round 1 parallel + Round 2 rebuttals + Round 2.5 invariant probe)
- Convergence threshold: 0.75
- Advocates: V1 (opus/architect), V2 (sonnet/analyzer), V3 (haiku/devops)

## Round 1 — Parallel Advocate Statements (synthesized from variant content + self-assessments)

### V1 (architect) — position
**Summary:** The plan must be a reversible state machine; without the S0–S4 + S-KILL skeleton, between-tool gates, and the "seam not weld" surface doctrine, the eval rigor and cost accounting have nowhere to live and the framework risks irreversible Rust coupling.
**Steelman of V2:** V2 is right that my gate thresholds (≥30%, ≥95%, ≥50%) are placeholders without a labeling/sample-size methodology — a gate with no statistical power is theater.
**Steelman of V3:** V3 is right that I provide cost *slots* but no real numbers; the multi-vendor token economics is something my lens never priced.
**Concession:** My eval and cost sections are deliberately shallow (self-flagged §10/§11).

### V2 (analyzer) — position
**Summary:** Incorporate only if tools beat concrete IronClaude baselines (Auggie pass, native git merge) on real workflows; every vendor number is a hypothesis, inspect's keyword judge is rejected, and graduation requires predeclared thresholds + stratified evidence.
**Steelman of V1:** V1's state machine is the right container — my 7-step lifecycle maps onto S0–S4 cleanly, and its between-tool gate enforces my "if sem fails, pause inspect/weave" rule architecturally.
**Steelman of V3:** V3's multi-vendor token attribution sharpens my CP-1 token metric — I measured token delta but assumed its value; V3 shows the value is provider-conditional.
**Concession:** I'm thin on the actual adapter/wiring design and on real maintenance-cost figures.

### V3 (devops) — position
**Summary:** Three Rust binaries in a UV-only Python framework is infrastructure, not a feature; incorporation must be kill-first against measured all-in TCO with hard numeric budgets, and token savings on cheap providers may be economically irrelevant.
**Steelman of V1:** V1's reversibility doctrine is exactly the rollback property my C5 domain demands; "never link sem-core" is the architectural rule that keeps my TCO bounded.
**Steelman of V2:** V2's metric catalog is the quality measurement my cost plan lacks — a zero-cost false-positive tool still has negative value, which my lens underweights.
**Concession:** I hand-wave the integration architecture and the *quality* judging methodology.

## Round 2 — Rebuttals & Per-Point Resolution

| Diff point | Winner | Confidence | Rationale |
|-----------|--------|-----------|-----------|
| S-001 spine | V1 | High | State machine is the most reusable container; V2/V3 phases map onto it |
| S-003 gate language | V2+V3 | High | Gates need BOTH V2's qualitative pass/fail lists AND V3's numeric TCO budgets, hung on V1's states |
| C-001/C-005 token bar + harness form | V2≈V3 | High | Unanimous: ≥30% vs Auggie, `.dev/` scripts first |
| C-006/X-002 sample size | V2 | High | Tiered: V3's 5/3 = shadow directional; V2's 20/10 = graduate; confidence-capping adopted |
| X-003 inspect precision | V2 (+V1+V3) | High | Joint gate: precision floor (V2) ∧ recall-loss ceiling (V1) ∧ FP/PR budget (V3) |
| X-004 weave % | V2 | Medium | ≥60% native (strictest defensible) + 90% synthetic stretch |
| X-005 token-value conditionality | **V3** | High | Genuine insight — reshapes gate: token savings weighted by provider; not absolute value |
| U-001..005 architecture | V1 | High | Uncontested — V2/V3 defer architecture to V1 |
| U-006..009 eval rigor | V2 | High | Uncontested — V1/V3 defer methodology to V2 |
| U-010..012 cost rigor | V3 | High | Uncontested — V1/V2 defer cost instrumentation to V3 |

## Round 2.5 — Invariant Probe (fault-finder, 6 categories)

| ID | Category | Assumption probed | Status | Severity |
|----|----------|-------------------|--------|----------|
| INV-001 | guard_conditions | Native eval feasible without first proving corpus exists (A-001) | UNADDRESSED→**now addressed** via mandatory Phase 0 corpus inventory | HIGH |
| INV-002 | interaction_effects | Token-value assumed absolute; collapses on cheap-provider routing (A-002/X-005) | UNADDRESSED→**now addressed** via provider-weighted token gate | HIGH |
| INV-003 | state_variables | Install assumed to succeed; cargo-in-CI cost could exceed budget before value measured (A-003) | UNADDRESSED→**now addressed** via Phase 0 install gate (prebuilt-binary requirement) | HIGH |
| INV-004 | collection_boundaries | sem-core entity model on Markdown-heavy `.md` skill files — weakest tree-sitter support, yet skills ARE the repo (A-004) | UNADDRESSED→**now addressed** via CP-1 substrate-trust gate stratified by file type | HIGH |
| INV-005 | sufficiency_challenge | "Tool passes its gate" ALONE does not green "tool delivers net value" — maintenance TCO can swamp per-invocation wins | ADDRESSED — V3 CP-2 cumulative-cost freeze + value/cost ratio >1 requirement | MEDIUM |
| INV-006 | count_divergence | inspect top-60 cap is a hard recall hole on large PRs; "recall@60 must include all criticals" | ADDRESSED — V2 RQ-5 recall@60 gate + V1 disclosure requirement | MEDIUM |

**All 4 HIGH UNADDRESSED items resolved** by promoting A-001..A-004 into mandatory Phase 0 pre-flight gates and adopting X-005's provider-weighted token model. No HIGH item remains unaddressed → convergence not blocked.

## Convergence Assessment

- Diff points total: 18 (+ 6 invariant findings)
- Points with agreed resolution: 17/18 directional + all 6 invariants addressed
- The single high-impact contention (X-005) resolved in V3's favor and folded into the merged gate model
- **Final convergence: 0.88** (HIGH). Zero irreconcilable contradictions; merge is a structured union, not a compromise.
