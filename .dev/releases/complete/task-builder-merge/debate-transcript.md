---
convergence_score: 0.55
rounds_completed: 2
---

# Structured Adversarial Debate: Opus vs Haiku Roadmap Variants

## Round 1 — Initial Positions

### Divergence 1 & 3: Milestone Decomposition and Granularity

**Variant A (Opus — 7 milestones, per-FR):**
Each FR-CONV.X gets its own milestone with explicit calendar windows. This is the only structure that makes per-FR rollback a first-class roadmap citizen. Release-spec §9 SP-10 explicitly requires per-FR rollback granularity; aligning milestone boundaries with FR boundaries means each rollback target is a discrete schedule unit with its own entry/exit gates, fixtures, mitigations, and `make verify-sync` checkpoint. The 151-item count reflects that every FR carries non-trivial structural commitments (catalogue mirror across 3 surfaces, DM schemas, NFR enforcement) that deserve explicit row-level tracking rather than being subsumed into thematic groupings.

**Variant B (Haiku — 5 milestones, layered):**
Per-FR rollback is preserved through the strict landing order PR-06→PR-01→PR-04→PR-07→PR-02→PR-03 and per-FR MIG-001..006 entries — milestone boundaries don't have to mirror FR boundaries to deliver it. A dedicated M1 "Decision and Contract Foundation" freezes all DM-001..005, API-001..004, COMP-001..006, and NFR contracts before any FR implementation. This catches contract conflicts early (Q-DM-1, DM-003 field shape, API-004 halt-string ABI) when changes are cheap. 5 milestones reduce ceremony and context-switching — 96 vs 151 items is 36% less tracking overhead for the same six FRs.

### Divergence 2: Contract Definition Timing

**Variant A:** Just-in-time. Define DM-001 inside FR-CONV.2's milestone where it is consumed; define DM-003 inside FR-CONV.6's milestone where it is emitted. Iterative implementation reveals contract edge cases that an upfront freeze cannot anticipate (e.g., dedup_key 2-tuple shape only became obvious once FR-CONV.5 monotonicity composition was specified — INV-012 mutual coupling). Locking contracts in M1 risks premature commitment to shapes that need revision once consumers materialize.

**Variant B:** Front-loaded. M1 enumerates DM-001..005 and API-001..004 with full field lists, freezing the wire ABI before any agent file is touched. This is exactly how mature engineering teams ship interface-bearing releases: producer/consumer agreements are negotiated and signed *before* implementation, not discovered during it. The mutual coupling Opus cites (INV-012 dedup_key) is a reason to define both shapes upfront in M1, not a reason to defer them.

### Divergence 4: Timeline Anchoring

**Variant A:** Concrete calendar dates (2026-05-15 → 2026-08-21). Stakeholders need commitments; ambiguous "Week N" schedules slip silently. Q3 GA buffer is visible (~6 weeks before Q3 close).

**Variant B:** Week-relative ("Week 1-14"), anchored to "TDD Design Complete 2026-05-21" and Q-DM-1 resolution. Q-DM-1 is a CRITICAL blocker owned by Engineering Lead with no committed resolution date — pinning calendar dates before that resolves creates false precision. Week-relative honors the actual dependency chain.

### Divergence 9: NFR Placement

**Variant A:** NFRs distributed to enforcement point (NFR-CONV.1/.5 in M1, .7 in M2, .10 in M6, .2/.3/.4/.8/.9 in M7). NFRs become testable only when the FR they constrain is implemented; placing them earlier is documentation theater.

**Variant B:** All NFR-CONV.1..10 + NFR-CONV-R1 enumerated as M1 deliverables. NFRs are *contracts* — they need to be agreed upon before implementation choices foreclose them. NFR-CONV.4 (token ceiling ≤1.10), NFR-CONV.5 (no new deps), NFR-CONV.10 (parallel-research preservation) constrain *every* downstream FR; treating them as M7 line items is treating contracts as audits.

### Divergence 10: Feature Flag Governance

**Variant A:** Flags co-located with their FR (FF_TB_ADD_1_THROUGH_8 in M1, FF_EXECUTION_CONTEXT_HEADER in M2, etc.). Each flag's lifecycle (enable→audit→cleanup) lives next to the change it gates — easier to audit a single FR's rollback envelope.

**Variant B:** All FLAG-* consolidated in M5. Release-readiness is a collective decision — owners want to see all six flags, their cleanup windows, and their rollback paths on one page when authorizing GA. Centralization makes that audit possible.

### Divergence 5: OPS/MET Visibility

**Variant A:** OPS-001..007 and metrics fold into M7 integration-point tables and risk-register narrative.

**Variant B:** OPS-001..007 + MET-001..006 + FLAG-* are numbered M5 rows. Operational deliverables that are not numbered rows get deprioritized; explicit MET items with target thresholds make production-readiness measurable, not aspirational.

## Round 2 — Rebuttals

### Variant A rebutting Variant B

- **On contract-first M1:** Haiku's M1 lists 26 deliverables including all 6 COMP rows, 5 DM rows, 4 API rows, and 11 NFR rows — but only 2 of those (DM-004 and OPEN-INV-018) actually block M1 exit. The other 24 are *definitions documented in the TDD*, restated as roadmap rows. This is documentation duplication, not contract freezing. The TDD already holds these contracts; the roadmap should track the work to *implement and verify* them, which is exactly what Opus's per-FR placement does.
- **On per-FR rollback preservation:** Haiku claims per-FR rollback via landing order, but the §19.4 co-revert matrix specifies that FR-CONV.5 ↔ FR-CONV.6 are *jointly revertable* due to INV-012 dedup-key composition. Opus surfaces this mutual coupling in the dependency graph ("M5/M6 mutual-shape coupling"); Haiku's flat linear graph (M1→M2→M3→M4→M5) hides it because PR-02 and PR-03 are both in M4. A reader of Haiku's roadmap cannot see that PR-02 and PR-03 form a co-revert pair without reading the underlying spec.
- **On week-relative scheduling:** Haiku's M1 entry condition is "no earlier than 2026-05-21 design approval and Q-DM-1 ownership" — but Q-DM-1 is owned, not resolved. If Q-DM-1 resolves in week 1, week-relative scheduling is identical to Opus's calendar; if it slips, the entire schedule slips uniformly under either model. The "flexibility" Haiku claims is illusory because the dependency chain is identical.
- **On NFR consolidation:** Putting NFR-CONV.10 (parallel-research) in M1 as a contract row does not make it testable. The fixture (TEST-021) lives in M6 in both variants because that is where partition concurrency surfaces. Haiku's M1 NFR rows are aspirational labels; Opus's M7 placement is where the measurement actually happens.

### Variant B rebutting Variant A

- **On documentation duplication:** Roadmaps are not the TDD — they are the *plan to execute the TDD*. M1 deliverable rows are not restatements; they are commitments that DM-001..005 and API-001..004 will exist in a frozen form before FR work starts. Opus's "just-in-time" approach means contract shape can shift mid-implementation, and the only artifact that catches that shift is the diff log. M1 contract-freeze makes shift visible at the milestone gate, not at post-hoc review.
- **On mutual-coupling visibility:** Opus's dependency graph annotations are valuable, but they're prose that lives outside the milestone tables. Haiku's M4 explicitly bundles FR-CONV.5 and FR-CONV.6 into one milestone with shared exit criteria, which is the structural reflection of co-revert coupling — not a documentation overlay. A reader who only sees Haiku's M4 entry/exit knows immediately that PR-02 and PR-03 ship as a unit. A reader of Opus's M5 and M6 needs to cross-reference the dependency graph to learn the same fact.
- **On per-FR rollback granularity:** Both variants preserve per-FR MIG rollback paths. The release-spec §9 SP-10 requirement is satisfied by the per-FR commit-revertability, not by milestone-boundary alignment. Opus over-indexes on milestone-to-FR isomorphism — 7 milestones with 2-week durations is ceremony that adds project-management overhead without changing rollback capability.
- **On schedule commitment:** Opus's calendar dates (2026-05-15 → 2026-08-21) imply a Q-DM-1 resolution by ~2026-05-15. Q-DM-1 is owned by Engineering Lead with no resolution commitment. Publishing those dates creates a stakeholder commitment the team cannot guarantee. Week-relative anchoring honors the actual blocker and is honest about uncertainty.
- **On centralized governance:** Opus's per-FR flag placement means GA approval requires reading 6 milestone tables to enumerate the flag-cleanup commitments. Haiku's M5 FLAG-* and MET-* rows put the GA-readiness checklist on one page — that is the working artifact for the GA-tagging decision, and it benefits from centralization.

## Convergence Assessment

**Strong agreement (no divergence):**
- Spec source, complexity, persona
- FR landing order (PR-06 → PR-01 → PR-04 → PR-07 → PR-02 → PR-03)
- Q-DM-1 critical-blocker semantics and owner
- Strictly-additive A-002 governance, no new dependencies (NFR-CONV.5)
- Token-cost ceiling NFR-CONV.4 ≤1.10 measurement design
- Determinism scope split (NFR-CONV.1 vs NFR-CONV.2)
- Anti-inflation byte-stability at rf-qa-qualitative.md:766-775
- All-agents-fail guard precedence at rf-team-lead.md:417
- 25-fixture test suite and 5+1 axis enumeration
- Retry halt precedence (regression > monotonicity > 3-cycle cap)
- DM-003 7-field DNSP schema with 2-tuple dedup_key
- K-003 first-5-runs audit window
- 14-week total duration within 2026-Q3 GA target

**Partial convergence (mechanical equivalents, not real disputes):**
- Divergence 5 (OPS placement): both deliver the same 7 runbooks; M5 vs M7 placement is cosmetic given that the audit window itself is post-merge.
- Divergence 6 & 7 (open-question placement): both surface the same questions; placement difference does not change resolution paths.
- Divergence 11 (test fixture distribution): both validate the same 25 fixtures.

**Remaining genuine disputes:**

1. **Milestone-to-FR isomorphism (D1, D3, D12):** Opus's 7-milestone structure makes mutual coupling (FR-CONV.5↔.6, FR-CONV.3↔.1) explicit at the milestone-boundary level; Haiku's 5-milestone structure makes the co-revert pair (PR-02/PR-03) structurally visible by bundling them in M4. *Both succeed at exposing coupling, by different means.* Stakeholder preference (per-FR tracking vs thematic grouping) is the real selector.

2. **Contract-freeze timing (D2, D8, D9):** This is the strongest live disagreement. Opus argues the TDD already holds contracts and roadmap duplication is wasted rows; Haiku argues a roadmap-level M1 freeze is the only artifact that catches mid-implementation contract drift before commit time. *Neither variant produces a different end-state* (all contracts ship in identical form), but they produce different *change-detection points*. A team with strong TDD-review discipline favors Opus; a team prone to contract drift during implementation favors Haiku.

3. **Schedule commitment (D4):** Opus's calendar dates are useful for stakeholders but create commitment risk if Q-DM-1 slips; Haiku's week-relative is honest about uncertainty but harder to communicate externally. *This is a communication-style preference, not a structural difference.*

4. **Feature-flag governance (D10):** Opus's per-FR lifecycle co-location optimizes for per-FR audit; Haiku's M5 consolidation optimizes for GA-readiness audit. Different audiences, different artifacts. *Hybrid possible:* per-FR placement with an M5/M7 consolidated flag-cleanup table.

**Areas where one variant is decisively stronger:**

- **Opus is decisively stronger on mutual-coupling visibility in the dependency graph.** Haiku's flat linear graph hides FR-CONV.3↔.1 INV-010 enumeration coupling and FR-CONV.5↔.6 dedup-key coupling. This is a documentation defect in Haiku, not a structural choice.
- **Haiku is decisively stronger on architectural-surface enumeration via explicit COMP-001..006 rows.** Opus's inline "Comp" column does not give a reader a single place to see the six modification points. Haiku's M1 component rows do.

**Convergence score: 0.55.** The two variants agree on every load-bearing technical fact and disagree only on roadmap *presentation* — milestone count, where contracts are restated, schedule anchoring, and where governance items are tabulated. Neither variant changes what gets built, when it ships, or how it's rolled back. The disputes are real (presentation drives reviewability), but resolvable by stakeholder preference rather than by technical argument. A merged roadmap that adopts Opus's 7-milestone per-FR structure with Opus's explicit mutual-coupling dependency graph, plus Haiku's M1 COMP-001..006 architectural-surface map and M5/M7 consolidated FLAG-*/MET-* governance table, would capture the strongest elements of both without compromising either.
