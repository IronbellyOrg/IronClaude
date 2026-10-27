---
total_diff_points: 12
shared_assumptions_count: 14
---

## Shared Assumptions and Agreements

1. **Scope: 6 strictly-additive FRs** (FR-CONV.1..6) imported from `/sc:tasklist` into task-builder skill
2. **Q-DM-1 is a CRITICAL blocker** requiring Engineering Lead decision before FR-CONV.1 implementation
3. **Strictly-additive governance (A-002)** — no existing items renamed/renumbered/removed
4. **Serial landing order** PR-06 → PR-01 → PR-04 → PR-07 → PR-02 → PR-03
5. **GA target end of 2026-Q3** (2026-09-30); start 2026-05-14/15
6. **Token-cost ceiling NFR-CONV.4 ≤1.10** measured on 5 representative BUILD_REQUESTs
7. **K-003 audit** on first 5 real rf-qa-qualitative runs post-FR-CONV.3
8. **rf-team-lead.md:417 preserved verbatim** (NO DRIFT) for all-agents-fail escalation
9. **5 invariants preserved** (NFR-CONV.6..10): self-contained-item, evidence-bound-item, persistent `.dev/tasks/`, zero-trust QA, parallel-research
10. **Intent-port over implementation-port** strategy
11. **Five Adversarial Axes** (AX-1..AX-5 + `none` sentinel) annotate only, not replace 15-item checklist
12. **Anti-inflation rule** at rf-qa-qualitative.md:766-775 byte-stable
13. **`make verify-sync` PASS** required pre-commit (A-001 sync discipline)
14. **PR-05 deferred** to Phase-2; not in v3.9 scope

## Divergence Points

### 1. Milestone Decomposition Strategy
- **Opus:** 6 milestones (M1 Foundation, M2 FR1, M3 FR2, M4 FR3+FR4, M5 FR5+FR6, M6 Hardening) — granular per-FR or per-PR pairing
- **Haiku:** 5 milestones (M1 Foundation, M2 Structural+Header, M3 Verdict+Axes, M4 Retry+DNSP, M5 Validation) — layered by technical concern
- **Impact:** Opus enables finer per-FR rollback gates and clearer commit-to-milestone mapping; Haiku reduces milestone overhead and aligns to TDD phase numbering more directly

### 2. Timeline Distribution
- **Opus:** M1=1wk, M2=2wk, M3=1wk, M4=2wk, M5=2wk, M6=12wk (heavy post-merge audit tail)
- **Haiku:** M1=1wk, M2=4wk, M3=4wk, M4=4wk, M5=6.5wk
- **Impact:** Opus reserves majority of calendar for post-GA hardening/measurement; Haiku front-loads implementation weeks and compresses validation

### 3. Item Granularity / Row Count
- **Opus:** 108 numbered items across 6 milestones; each FR decomposed into TB-Add/COMP/TEST/NFR/MIG sub-items
- **Haiku:** 110 items across 5 milestones; flatter per-milestone tables with explicit DM/API/INV/NFR/SC/REL prefixes
- **Impact:** Opus produces more traceable per-PR rollback; Haiku produces a more contract-first surface that surfaces invariants and data-models earlier

### 4. M1 Foundation Composition
- **Opus M1:** 15 items focused on DM-001..005 + API-001..005 + GOV-1..4 (contract definition heavy)
- **Haiku M1:** 20 items including all NFR-CONV.* SLOs, all INVs, scope guardrails (NG-001), JTBD mapping (JTBD-001), and dependency ledger (D-001)
- **Impact:** Haiku front-loads non-functional contracts and scope guardrails as M1 deliverables; Opus defers NFR validation rows to the milestone where the FR lands

### 5. Test Fixture Placement
- **Opus:** Tests (TEST-001..025) distributed across M2-M5 alongside their corresponding FR implementation
- **Haiku:** Tests split — TEST-001..006 in M2, TEST-007..014 in M3, TEST-015..022 in M4, TEST-023..025 in M5
- **Impact:** Both functionally equivalent; Haiku's grouping mirrors layered milestones, Opus's mirrors per-FR delivery

### 6. Rollout/Migration Steps (MIG-001..007)
- **Opus:** MIG-001..006 embedded in M2-M5 as the closing item of each FR's milestone; MIG-007 (audit) in M6
- **Haiku:** All MIG-001..007 collected together in M5 as a single rollout sequence
- **Impact:** Haiku creates an explicit "rollout milestone" with sequencing visible at one glance; Opus keeps the commit landing co-located with its content, easier per-PR review

### 7. NFR Validation Timing
- **Opus:** NFR-CONV.1, 3, 6, 7, 9, 10 reinforcement tests distributed across M2-M5
- **Haiku:** NFR-CONV.1, 2, 6, 7, 8, 9, 10 SLO definitions all in M1; validation tests (TEST-023..025) collected in M5
- **Impact:** Haiku separates SLO *definition* (M1) from *validation* (M5); Opus interleaves both per-FR

### 8. Operations Runbooks (OPS-001..007)
- **Opus:** OPS-001..007 explicitly enumerated as M6 deliverables with item IDs 98-104
- **Haiku:** OPS-001..007 enumerated identically but positioned in M5 alongside MIG/SC/REL items
- **Impact:** Identical content; differs only by milestone label

### 9. Decision Summary / Open Questions Depth
- **Opus:** 11-row Decision Summary with explicit alternatives and rationale; 5 Open Questions in M6
- **Haiku:** 9-row Decision Summary (compressed); 6 Open Questions distributed (1 in M1, 6 in M5)
- **Impact:** Opus provides more architectural reasoning per decision; Haiku is terser and consolidates open questions in validation milestone

### 10. Explicit Sub-Component Decomposition (DNSP-EXH-1, DNSP-DEDUP-1, RETRY-REG-1, RETRY-MONO-1)
- **Opus:** DNSP behaviors and retry behaviors handled inside FR-CONV.5/6 acceptance criteria without separate row IDs
- **Haiku:** Adds explicit DNSP-EXH-1 (exhaust vocabulary), DNSP-DEDUP-1 (within-cycle merge), RETRY-REG-1 (regression precedence), RETRY-MONO-1 (non-shrink check) as standalone rows
- **Impact:** Haiku surfaces these as discrete implementation contracts assignable individually; Opus folds them into FR scope

### 11. AX-0 None Sentinel as Distinct Row
- **Opus:** `none` sentinel handled as part of GOV-1 closed-vocabulary definition
- **Haiku:** AX-0 None axis sentinel called out as its own row alongside AX-1..AX-5
- **Impact:** Minor; Haiku's symmetric AX-0..AX-5 enumeration is clearer; Opus avoids row inflation

### 12. M6 / Final-Milestone Audit Window Length
- **Opus:** M6 spans 12 weeks (2026-07-10 → 2026-09-30) explicitly to absorb K-003 audit + token measurement + fallback removal at GA+30 days
- **Haiku:** M5 validation is 6.5 weeks (2026-08-17 → 2026-09-30), with implementation milestones absorbing more calendar
- **Impact:** Opus prioritizes long post-merge stabilization; Haiku assumes shorter audit suffices and uses extra weeks for implementation depth per milestone

## Areas Where One Variant Is Clearly Stronger

**Opus stronger:**
- Per-FR commit traceability via MIG-001..006 co-located with FR work — makes serial-landing enforcement more visible per milestone
- Decision Summary table is more complete (11 vs 9 rows) and cites alternative-rejection rationale
- Longer post-merge audit window directly addresses K-010 token-ceiling and K-003 inflation risks with explicit calendar runway
- Architectural-decision narrative in Executive Summary is more detailed

**Haiku stronger:**
- Cleaner separation of "what" (M1 contracts) from "where" (M2-M4 surfaces) from "verify" (M5)
- DNSP and retry behaviors decomposed into individually-trackable rows (DNSP-EXH-1, RETRY-REG-1, etc.) — better for parallel implementer assignment
- All NFR SLOs frozen in M1 — clearer single-source-of-truth for non-functional contracts
- Open Questions concentrated where they will be resolved (M5) — easier release-checklist scanning
- Scope guardrails (NG-001) and JTBD coverage map (JTBD-001) make negative scope and product-job coverage explicit

## Areas Requiring Debate to Resolve

1. **Milestone count (5 vs 6):** Should post-merge audit be its own milestone (Opus M6) or folded into a validation milestone (Haiku M5)? Affects rollback decision points and PM reporting cadence.
2. **Calendar allocation:** 12-week audit tail (Opus) vs 4+4+4+6.5 implementation/validation balance (Haiku) — which better matches actual K-003/NFR-CONV.4 measurement velocity?
3. **MIG row placement:** Co-located with FR (Opus) vs consolidated rollout milestone (Haiku) — which gives clearer per-PR rollback granularity in practice?
4. **NFR SLO timing:** Define all SLOs upfront in M1 (Haiku) vs define-and-validate-per-FR (Opus) — affects when contracts become binding for downstream rows.
5. **Sub-component row granularity:** Promoting DNSP-EXH-1/DEDUP-1, RETRY-REG-1/MONO-1 to standalone rows (Haiku) vs folding into FR acceptance (Opus) — trade-off between row inflation and assignable-task clarity.
6. **Decision-summary depth:** Is the more verbose Opus decision table worth the additional roadmap length, or is Haiku's compressed form sufficient given the upstream TDD already documents alternatives?
