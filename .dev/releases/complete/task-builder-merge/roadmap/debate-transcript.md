---
convergence_score: 0.72
rounds_completed: 2
---

# Structured Debate: Opus vs Haiku Roadmap Variants

## Round 1: Initial Positions

### Variant A (Opus) — Opening Statement

**Position:** Six milestones organized by FR-PR pairing with a 12-week post-merge audit tail is the correct decomposition for this release.

**Key claims:**

1. **Per-FR milestone granularity matches the rollback unit.** Since release-spec §19.4 makes each FR individually revertable and the §4.6 landing order is strictly serial (PR-06 → PR-01 → PR-04 → PR-07 → PR-02 → PR-03), milestone boundaries should map 1:1 to commit-revert boundaries. M3 (FR-CONV.2 alone, 1 week) exists precisely because PR-01 is the only commit in that window — collapsing it into M2 would mean a milestone "passes" with two independently revertable units inside, hiding rollback signal from PM reporting.

2. **MIG rows belong adjacent to their FR work.** MIG-001..006 each represent the act of landing a specific PR. Co-locating them with their FR's COMP/TEST rows means the milestone reader sees content → land in a single milestone window. Haiku's consolidation of all MIG-001..007 into M5 forces the reader to cross-reference back to M2-M4 to know what is being landed, and creates a 6.5-week milestone that mixes rollout commits, post-merge audits, NFR measurement, and operational runbook authoring — four distinct phases under one milestone label.

3. **The 12-week audit tail is non-negotiable.** K-003 audit requires *first 5 real rf-qa-qualitative runs* (not synthetic fixtures), NFR-CONV.4 token measurement requires real BUILD_REQUEST traffic, and the GA+30-day fallback removal cannot start until GA. These are calendar-bound by traffic, not effort — compressing them to 6.5 weeks (Haiku M5) assumes a traffic velocity the spec does not commit to. Audit gates that need real runs cannot be parallelized with implementation.

4. **Decision-summary depth is load-bearing.** Eleven rows with explicit alternative-rejection rationale (e.g., "Bulk-implementation-port REJECTED — would re-introduce v3.8 over-engineering pattern per FINAL-REPORT §6.3") gives the future maintainer the *why* of every architectural choice. Haiku's compression to 9 rows drops cross-references to FINAL-REPORT §6.2 F4 (PR-05 deferral rationale) and §6.3 (asymmetric finding).

### Variant B (Haiku) — Opening Statement

**Position:** Five milestones layered by technical concern with NFR SLOs frozen at M1 is the correct decomposition for this release.

**Key claims:**

1. **Contract-first layering catches integration risk earlier.** M1 freezes all NFR SLOs (NFR-CONV.1..10), all invariants (INV-002, 010, 012, 015, 019, 021), scope guardrails (NG-001), and JTBD coverage (JTBD-001) before any prompt surface is touched. This means by week 1 the team has a single-source-of-truth contract sheet that downstream FR work validates *against*. Opus's M1 defers NFR-CONV.6/7/8/9/10 reinforcement rows into each implementing milestone — meaning the same SLO gets re-stated at four different milestones, increasing drift risk between definitions.

2. **DNSP and retry sub-components are individually assignable.** Promoting DNSP-EXH-1 (exhaust vocabulary), DNSP-DEDUP-1 (within-cycle merge), RETRY-REG-1 (regression precedence), RETRY-MONO-1 (non-shrink check) to standalone rows means each is a discrete work item with explicit acceptance criteria. Opus folds these into FR-CONV.5/6 acceptance language, so an implementer assigned to RETRY-MONO-1 has to read through FR-CONV.5's bullet list to find their contract. Row inflation here is information density, not noise.

3. **Front-loading calendar to implementation is more honest.** Real engineering velocity on a 6-FR serial chain is not 6 weeks of code + 12 weeks of waiting. Each FR's M+1.x phase in TDD §23.1 needs implementation depth (TDD says "1 week" but that is *minimum* before fix-cycles). Allocating 4+4+4 weeks to M2-M4 gives realistic per-FR landing windows; Opus's 2+1+2+2 = 7-week implementation block compresses M3 (FR-CONV.2) into a single week and M4 (two FRs FR-CONV.3+4) into two weeks, which is optimistic.

4. **Consolidated rollout milestone gives a single release-readiness view.** When the release manager scans M5, they see: all 6 MIGs in landing order, all 7 OPS runbooks, all 6 open questions, all gate measurements, GA readiness criterion REL-001. Opus scatters this across M2 (MIG-001), M3 (MIG-002), M4 (MIG-003+004), M5 (MIG-005+006), and M6 (MIG-007 + OPS + open questions) — release readiness becomes a multi-milestone synthesis.

5. **Symmetric AX-0..AX-5 enumeration matches the spec vocabulary.** TDD §8.5 closed vocabulary is `{AX-1, AX-2, AX-3, AX-4, AX-5, none}` — six values. Treating `none` as AX-0 sentinel row makes the vocabulary visually parallel and prevents the "none sentinel" rule from being lost in GOV-1 paragraph prose.

## Round 2: Rebuttals

### Variant A (Opus) — Rebuttal to Haiku

**On NFR front-loading (Haiku claim 1):** Freezing NFR SLOs at M1 sounds like contract discipline, but it conflates *definition* with *binding*. NFR-CONV.6 (self-contained-item invariant) cannot be validated until FR-CONV.1 lands TB-Add-1 fail-closed behavior — its M1 definition row in Haiku is paper-only until M2 anyway. Opus's pattern of (define-and-validate per FR) means each NFR row's acceptance criteria are written next to the fixture that proves it. Haiku's M1 carries 20 rows of which 10 are NFR/INV definitions that are not testable until M2-M4, inflating M1's apparent deliverable count without adding executable progress.

**On sub-component row promotion (Haiku claim 2):** DNSP-EXH-1, DEDUP-1, RETRY-REG-1, MONO-1 are not independently work-plannable — they are clauses *within* a single PR commit (PR-02 or PR-03). Splitting them creates the illusion of parallelism where none exists: you cannot assign RETRY-REG-1 to engineer X and RETRY-MONO-1 to engineer Y, because both edit the same fix-loop dispatch in rf-task-builder.md:334-361 and rf-qa.md:~308-315. A single engineer ships PR-02 as one commit. Row-level decomposition that does not map to assignable units is bookkeeping, not planning.

**On calendar honesty (Haiku claim 3):** The 4+4+4 implementation allocation assumes fix-cycle iteration *during* the milestone. But fix-cycles are bounded by per-gate caps (research-gate 3, synthesis-gate 2, etc.), so a single FR commit's iteration window is bounded above by ~2 weeks worst-case, not 4. Haiku's 4-week M2 covers FR-CONV.1 *plus* FR-CONV.2 (per the table), which means PR-06 and PR-01 both land in M2 — collapsing two distinct rollback events into one milestone signal. The "extra" implementation weeks Haiku adds are not buying additional rigor; they are buying schedule cushion at the cost of milestone resolution.

**On consolidated rollout (Haiku claim 4):** A "single release-readiness view" at M5 sounds attractive but it means M5 is monolithically pass/fail across 25 rows spanning landings, audits, measurements, runbooks, and GA. Opus's M6 is narrower: it is exclusively post-merge work — by the time M6 starts, all 6 FRs are already landed in M2-M5. Rollback decisions at MIG-007 in Opus operate on a completed merge surface; in Haiku, MIG-005 (FR-CONV.5 landing) happens in the same milestone as REL-001 (GA readiness), which is a 6.5-week scope.

### Variant B (Haiku) — Rebuttal to Opus

**On per-FR milestone granularity (Opus claim 1):** Milestone boundaries do not have to match rollback boundaries — that is what release-spec §19.4 rollback matrix is for. Milestones are PM reporting cadence; rollback is a commit-level operation. A 1-week M3 milestone (Opus) covering a single FR is too granular for portfolio reporting: it would generate weekly milestone-status updates whose only content is "FR-CONV.2 landed, fixtures green." The natural PM unit is the *technical phase* (TDD §23.1 already groups M1.1+M1.2 as "Phase 1: Structural Gate Reinforcement"), and Haiku aligns to those phase boundaries.

**On MIG-row co-location (Opus claim 2):** Co-locating MIG with FR work creates the *opposite* problem from what Opus claims: each MIG row is functionally identical ("single revertable commit; serial landing position N; make verify-sync PASS"), so distributing them across M2-M5 forces the reader to assemble landing order from 5 different milestone windows. Haiku's MIG-001..007 sequence in M5 *is* the release runbook, read top-to-bottom. Opus's claim that "the milestone reader sees content → land in a single window" overstates how often a reader scans one milestone in isolation — release managers read across milestones to plan deployments.

**On 12-week audit tail (Opus claim 3):** K-003 audit on "first 5 real runs" does not require 12 weeks. Even at one task-builder invocation per week, 5 runs = 5 weeks; in practice rf-qa-qualitative runs accumulate faster than that during dogfooding. NFR-CONV.4 token measurement on 5 representative BUILD_REQUESTs is a single afternoon of work once instrumentation lands at OPS-002/004/005. GA+30-day fallback removal is itself a single commit. Opus is allocating 12 weeks of calendar to 2-3 weeks of actual work plus waiting, which is not a milestone — it is an open-ended pause. Haiku's 6.5-week M5 is honest: it includes implementation depth for the audit work itself.

**On decision-summary depth (Opus claim 4):** Roadmap decision tables should not duplicate TDD §8 architectural decisions — that is the TDD's job. Haiku's 9-row table covers the roadmap-shaping decisions (intent-port vs implementation-port, governance model, axis model, halt logic, timeline anchoring); the FINAL-REPORT cross-references Opus carries forward live in the TDD, where they belong. Increasing roadmap verbosity past what the roadmap reader needs creates a parallel source-of-truth that will drift from TDD §8 over time. Compression here is rigor, not loss.

**On sub-component row debate (counter to Opus's rebuttal):** Opus argues PR-02 ships as one commit so RETRY-REG-1 and RETRY-MONO-1 cannot be parallelized. True for the *commit*, but acceptance criteria need not be parallelized to be individually trackable. When TEST-016 (regression halt fixture) fails, the bug is in RETRY-REG-1 specifically — the row exists so the test failure points to a discrete contract, not to "somewhere in FR-CONV.5's 8-line acceptance bullet list." This is fixture-to-contract traceability, not parallelism.

## Convergence Assessment

### Areas of Agreement

1. **Foundation milestone necessity:** Both variants agree M1 must close Q-DM-1, lock data-model entities (DM-001..005), define inter-agent contracts (API-001..005), establish sync-discipline tooling, and validate conflict-register.md before any FR work begins. Disagreement is only on what *else* belongs in M1 (NFR/INV definitions per Haiku vs deferred-to-implementing-milestone per Opus).

2. **Serial landing order:** Both variants honor the strict PR-06 → PR-01 → PR-04 → PR-07 → PR-02 → PR-03 sequence and treat it as non-negotiable. Both flag K-007 (sequencing inversion) as a tracked risk.

3. **Risk register substance:** K-001 through K-010 risk content, mitigations, and owners are functionally identical between variants. Disagreement is only on which milestone column each risk appears in.

4. **Test fixture content:** TEST-001..025 are described with equivalent acceptance criteria in both variants — only their milestone bucket differs.

5. **GA target:** Both variants land on 2026-09-30 (end of 2026-Q3) as the GA date with the same critical-path narrative through Q-DM-1.

6. **Negative scope:** Both variants agree PR-05 is deferred to Phase-2, no new external dependencies are permitted (NFR-CONV.5), and `rf-team-lead.md:417` remains byte-stable.

### Remaining Disputes

1. **Milestone count (5 vs 6) — UNRESOLVED.** Variant A holds the 12-week audit-tail-as-its-own-milestone position; Variant B holds the validation-and-rollout-as-single-milestone position. The dispute reduces to: is the post-merge audit window a PM reporting unit (Opus) or a phase of the validation milestone (Haiku)?

2. **NFR/INV definition timing — UNRESOLVED.** Variant A insists define-and-validate per-FR keeps contracts executable; Variant B insists front-loading contracts at M1 prevents drift. Both have merit; the choice reflects whether the team prefers contract-sheet discipline (Haiku) or fixture-adjacent definition (Opus).

3. **MIG row placement — PARTIALLY RESOLVED.** Both sides acknowledge MIG rows are bookkeeping for the landing event; the debate is whether bookkeeping is more readable adjacent to the work (Opus) or in sequence as a runbook (Haiku). No factual resolution — preference dispute.

4. **Sub-component row promotion — PARTIALLY RESOLVED.** Variant B's fixture-to-contract traceability argument is strong; Variant A's no-parallelism rebuttal is also strong. Suggests a hybrid: keep sub-component IDs in acceptance criteria (Opus) AND surface them as fixture-traceable references (Haiku).

5. **Decision-summary depth — UNRESOLVED.** Whether roadmap should duplicate TDD §8 cross-references is a documentation-philosophy question that neither variant can resolve without an external editorial standard.

6. **Calendar allocation — UNRESOLVED.** 12-week audit tail vs 4+4+4+6.5 implementation/validation balance reflects different assumptions about real-traffic velocity that the spec does not commit to.

### Convergence Score Justification

Score: **0.72**

- Shared assumptions (14) and identical content surfaces (risk register, tests, FR scope, landing order, GA date) drive baseline agreement.
- Six divergence points remain genuinely unresolved after two rounds — these are structural preferences, not factual disagreements.
- Both variants would produce an acceptable executable plan; the choice is editorial. No variant exposes a fatal flaw in the other.
- A merged roadmap could adopt Haiku's M1 contract-sheet completeness, Opus's per-FR milestone granularity for M2-M4 implementation, and either party's M5/M6 structure — convergence is structurally feasible.
