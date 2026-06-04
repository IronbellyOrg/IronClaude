---
convergence_score: 0.55
rounds_completed: 2
---

# Adversarial Debate: Opus vs Sonnet Roadmap Variants

## Round 1 — Initial Positions

### Divergence 1: Timeline (16 weeks vs 10 weeks)

**Variant A (Opus, 16 weeks):** The wave-pipeline spine (M2→M3→M4→M5) is irreducible, and each wave carries non-trivial integration risk: M2 alone bundles Wave 0 preflight + schema + 8-lens registry + §11.5 enforcement across 3 prompt paths + injection-guard parity tests. Compressing this to one week is fantasy. Uniform 2-week blocks give engineers slack to absorb OQ resolutions, transport flakiness, and the inevitable schema churn after the first end-to-end run. A 16-week plan that ships is worth more than a 10-week plan that slips.

**Variant B (Sonnet, 10 weeks):** Opus's uniform 2-week allocation is over-padded for milestones like M4 (12 items) and M5 (11 items). Effort scales with item count and risk, not calendar symmetry. M1 at 1 week is feasible because it's contract definition — pure design work, no integration. M2 at 2 weeks reflects its real density (dispatch + state + transport + observability), and the 1-week milestones (M3/M4/M5) are tightly scoped concern bundles. The 10-week schedule is achievable with a fluent team; pretending otherwise builds in slack that becomes Parkinson's-law work.

### Divergence 2: Milestone Decomposition (Wave-aligned vs Concern-bundled)

**Variant A (Opus):** Wave-alignment mirrors the architecture document 1:1. Each milestone has a single architectural locus (M2=Wave 0, M3=Wave 1, M4=Wave 2, M5=Wave 3), making exit criteria sharp and reviewable. Engineers reading the spec can trace any item to a wave and any wave to a milestone. This is the lowest cognitive-load decomposition.

**Variant B (Sonnet):** Concern-bundling reduces cross-milestone handoffs. Bundling dispatch+state+transport+observability into M2 means they're built by the same engineers in the same week with shared mental model — that's how real teams build cohesive subsystems. Opus's wave-decomposition creates 7+ handoff interfaces; mine creates 3-4. Handoffs are where bugs live.

### Divergence 3: Foundation Scope (29 items vs 45 items)

**Variant A (Opus):** M1 should freeze only what's needed to start M2: data models, module shape, CLI group placeholder. Front-loading all 19 ACs into M1 (Sonnet) commits to architectural rules before they're bound to real code — those decisions deserve to be made when context is richest, not at week 1. 45 items in 1 week is incoherent.

**Variant B (Sonnet):** Architectural constraints (AC-001 through AC-019) are *declarations*, not implementations. Listing them in M1 documents the rules engineers will be held to in M2-M8; it doesn't claim they're "implemented" in week 1. The 45 items are mostly contract/model declarations (20 DM items, 19 ACs, 6 COMP stubs). Opus's deferral risks constraint drift — by the time M5 enforces NFR-008's 30 LOC ceiling, the merge module may already be 80 lines.

### Divergence 4: Dedicated Validation Milestone (Sonnet M6)

**Variant A (Opus):** Embedding per-IMM and per-INV tests in the milestone that introduces the invariant catches defects at the earliest possible moment. A dedicated validation milestone at the end (Sonnet M6) defers test work and creates a "test crunch" — exactly the anti-pattern that ships bugs. NFR-007 belongs distributed across M3/M5/M8.

**Variant B (Sonnet):** A dedicated validation milestone provides what continuous testing cannot: a single, auditable release-readiness signal. Stakeholders need to point at "M6 green" before authorizing M7 migration. Without it, "release readiness" is a fuzzy emergent property of M8 completion. The 9 TEST-### items in M6 are *integration* tests across IMMs/INVs — they belong in a gate, not scattered.

### Divergence 5: Operational Rollout Milestone (Sonnet M8)

**Variant A (Opus):** Runbook, observability procedures, and rollback are byproducts of feature completion, not separate work. Distributing operational items across M7 (observability) and M8 (migration docs) keeps the team focused on the actual deliverable. A separate "rollout" milestone reads as cargo-cult process.

**Variant B (Sonnet):** Production handoff is a discipline, not a byproduct. OPS-001 (runbook), OPS-002 (env readiness), OPS-004 (rollback) exist as first-class items because *they will not get done* otherwise — engineers ship features, not runbooks. Opus's roadmap has zero items dedicated to rollback procedure. That's a gap.

### Divergence 6: CLI Surface Timing (M5 Sonnet vs M7 Opus)

**Variant A (Opus):** Operators should not see `attach`/`kill` before resume (M6) is proven correct. Shipping the full surface in M5 before crash-recovery validation creates a window where operators can attach to detached jobs that may not resume properly. M7 timing means operators get the surface only after the underlying reliability is established.

**Variant B (Sonnet):** Operators need the full surface to *exercise* resume during M6 validation. Shipping `run --resume` without `status`/`logs`/`kill` means operators can't actually test resume behavior — they're flying blind. CLI surface and resume must ship together (M5) so M6 can validate them holistically.

### Divergence 7: Resume Independence (Opus M6 vs Sonnet M4)

**Variant A (Opus):** Resume is a reliability investment with its own risk profile (R-3 lens mutation, R-7 schema evolution, manifest immutability invariants INV-001/010/016). It deserves a dedicated milestone where the team thinks specifically about crash recovery, not as a side-effect of preflight work.

**Variant B (Sonnet):** Resume IS preflight-in-resume-mode. The manifest rehydration logic (INV-001) lives in preflight.py. Splitting it from M4 (where preflight is built) means M4 ships an incomplete preflight module that M6 has to reopen. That's an anti-pattern. Resume is structurally a preflight concern.

### Divergence 8: INV-005/INV-007 Commitment

**Variant A (Opus):** Worker-pool guard semantics (warn vs STOP) and empty-pool failure path are architectural decisions that benefit from being made with full pipeline context. Pre-committing at roadmap time (Sonnet) locks in semantics before the team understands the operational profile.

**Variant B (Sonnet):** Open questions that block schema design (OQ-007/008) must resolve before M2 dispatch is built — there's no benefit to deferral. Listing them as M4 items with explicit owner+target forces resolution; Opus's "defer to architect decision" is a recipe for drift.

### Divergence 9: Risk Granularity (10 vs 23 risks)

**Variant A (Opus):** 10 well-chosen risks beat 23 inflated ones. Sonnet's register includes risks like R-020 "rollout starts without operator observability" and R-021 "documentation diverges from CLI contract" — these are not risks, they are *process failures* that belong in a checklist, not a risk register.

**Variant B (Sonnet):** Operational risks are real risks. Opus's register has zero entries for rollout, documentation drift, or environment readiness. When something goes wrong in production because the runbook diverged from CLI flags, "process failure" is cold comfort. Granular risk surface = better mitigation planning.

## Round 2 — Rebuttals

### On Timeline (rebuttal cluster)

**Variant A rebuts B:** Sonnet's claim that M1 is "pure design work" ignores that 45 items demand *review and approval* from architect+security+devops, plus OQ-006/008/009/010 resolution by M1 exit. Even pure-design work hits coordination latency. A 1-week M1 with 4 blocking open questions is calendar fiction.

**Variant B rebuts A:** Opus's 2-week M4 has 12 items and 2-week M5 has 11 items — that's ~6 items/week, which is *light*. The argument that "engineers need slack" is real but doesn't justify pretending 11-12 items takes 2 weeks. Either compress those milestones or admit the schedule has 4+ weeks of explicit buffer. If buffer is the intent, label it as such instead of inflating milestone duration.

### On Decomposition (rebuttal cluster)

**Variant A rebuts B:** Sonnet's M2 bundles dispatch+state+transport+observability — that's 4 distinct concerns with different specialist owners (backend for dispatch, devops for observability, security for transport env handling). Bundling them in one 2-week milestone means whichever specialist is slowest becomes the bottleneck, with no cleanup parallelism. Wave-aligned decomposition lets specialists work in their wave without blocking others.

**Variant B rebuts A:** Opus's "specialists per wave" model is fiction in a team this size. The same backend engineers build dispatch (M3) AND normalize (M4) AND reduce (M5). Sequencing them across 3 milestones doesn't add parallelism — it adds context-switch cost. My concern-bundles match how the work actually flows.

### On Foundation Scope (rebuttal cluster)

**Variant A rebuts B:** "Declarations not implementations" is sophistry. If AC-008 ("Optional tmux dependency") is "declared" in M1 but tmux integration ships in M5, what was actually delivered in M1? An entry in a roadmap document. That's not a milestone exit criterion — that's a TODO. Real milestones produce code or contracts, not aspirations.

**Variant B rebuts A:** The 20 DM-xxx items ARE the contracts — they're dataclasses with frozen field lists serialized into manifests, state files, and result contracts. Freezing them in M1 is not aspiration; it's the *only way* M2-M8 can build against stable schemas. Opus also has 20 DM items in M1; the divergence is the AC declarations, which my variant captures as commitments and Opus elides.

### On Validation Gate (rebuttal cluster)

**Variant A rebuts B:** A "release-readiness signal" can be a CI status check (NFR-007 distributed test markers all green) — it doesn't need a 2-week milestone. Sonnet's M6 is 9 TEST items in 2 weeks, which means ~5 days of dedicated test writing. If tests are this concentrated, they were under-built earlier; if they were built earlier, M6 is mostly waiting. Either way, M6 isn't 2 weeks of work.

**Variant B rebuts A:** TEST-005 (non-Claude caller cross-language integration) and TEST-007 (kill-then-resume E2E) are *new* integration tests that can only run once everything is built. They can't be embedded earlier because their dependencies don't exist. A 2-week integration validation milestone is industry standard for this scope.

### On Operational Rollout (rebuttal cluster)

**Variant A rebuts B:** OPS-001 through OPS-006 are 6 documentation items in 1 week. That's a tech writer's sprint, not a milestone. If operational rollout matters, embed runbook authoring into M7 release packaging where it belongs, alongside MIG-004 release notes (which Sonnet *already has* in M7). M8 duplicates M7's documentation effort.

**Variant B rebuts A:** MIG-004 covers release notes; OPS-001 covers operator workflow runbook — these are different audiences (release readers vs operators) and different content (what changed vs how to use it). Conflating them is exactly why operators get poor handoff documentation in real projects.

### On CLI Timing (rebuttal cluster)

**Variant A rebuts B:** M6 validation can use direct artifact inspection (read .swarm-state.json, tail JSONL) — it doesn't require `status`/`logs` subcommands. Sonnet's argument that operators need the surface to test resume confuses "testing the implementation" with "testing the operator UX." The first only needs artifacts; the second is M7 work.

**Variant B rebuts A:** If `swarm status` doesn't exist when validating resume, then M6 also has to validate `swarm status` *after the fact* in M7 — meaning Opus splits resume validation across two milestones. My M5+M6 sequencing validates the operator-facing contract once, holistically.

### On Resume Placement (rebuttal cluster)

**Variant A rebuts B:** Resume's complexity isn't in preflight.py — it's in the *coordination* between preflight (rehydrate), dispatch (skip succeeded), reduce (regenerate merge). That cross-cuts M2-M5 and demands its own milestone to think about end-to-end. Sonnet's M4 bundling buries this complexity inside preflight, which is structurally wrong.

**Variant B rebuts A:** The cross-cutting coordination Opus describes is INV-010 (resume merge regen) which lives in reduce.py, not preflight. My M3 builds reduce.py with INV-010 explicit; my M4 wires up resume through preflight. The "dedicated milestone" framing inflates a feature into a phase.

### On Risk Register (rebuttal cluster)

**Variant A concedes partially:** Sonnet's operational risks (R-020 to R-022) have merit if there's a dedicated operational milestone. If M8 stands, those risks belong there. If M8 falls (as Opus advocates), they collapse into M7 risks. The risk count tracks milestone structure.

**Variant B concedes partially:** Some of my 23 risks could consolidate — R-014/R-015/R-016 (testing risks) could merge to a single "validation coverage gap" risk. The granularity argument is real; 23 may be over-fitted to milestone boundaries.

## Convergence Assessment

### Areas of Agreement (Strong)

1. **Shared foundation is solid.** Both variants agree on all 14 shared assumptions: Python+UV, ParallelExecutor, httpx, mechanical merge ≤30 LOC + 4 guards, manifest source-of-truth, §11.5 across 3 paths, IMM-4/5/6, 8-lens registry, 6-recipe registry, three amalgamation modes. The architectural core is not in dispute.

2. **Dependency graph is largely shared.** Both agree M1 precedes everything, the wave-pipeline spine (Wave 0→1→2→3) is irreducible, migration depends on completed pipeline + CLI surface.

3. **Risk taxonomy overlap is high.** Of Opus's 10 risks, 9 appear in Sonnet's 23 (with different IDs). The disagreement is about *additional* operational risks, not about the core engineering risks.

### Areas of Agreement Reached in Debate

4. **Timeline buffer should be explicit.** Both implicitly converge: Opus's 16 weeks contains ~4 weeks of slack vs. Sonnet's tight 10. A defensible plan would be Sonnet's milestone scoping (~10-12 weeks of nominal work) with explicit named buffer milestones, not Opus's distributed slack.

5. **M1 scope distinction is partly resolved.** Both agree the 20 DM items belong in M1. The AC declarations debate reduces to: should they be enumerated as M1 commitments (Sonnet) or embedded as cross-cutting concerns (Opus)? Both are valid documentation conventions.

6. **Validation gate vs distributed testing is a false dichotomy.** Sonnet conceded TEST-005/TEST-007 are genuinely end-to-end; Opus conceded NFR-007 needs *somewhere* to consolidate. Convergent path: keep IMM/INV unit tests embedded per-wave (Opus), add a 1-week integration validation phase at end for the genuinely-late tests (Sonnet trimmed).

### Remaining Disputes (Significant)

7. **Operational rollout milestone (M8):** Unresolved. Variant A maintains it's process theater; Variant B maintains runbook+rollback need first-class status. This is a values disagreement, not an evidence disagreement — it reflects how seriously each variant treats production handoff as engineering discipline.

8. **CLI surface timing (M5 vs M7):** Unresolved. Both have logically consistent positions: A prioritizes "ship correctness before UX," B prioritizes "ship operator surface holistically." The real-world answer depends on whether the team has operators using detached mode during M6 validation (favors B) or whether validation happens in CI with artifact inspection (favors A).

9. **Resume independence (Opus M6 vs Sonnet M4):** Unresolved. Variant A's "cross-cutting reliability investment" framing and Variant B's "preflight-mode extension" framing reflect different mental models of resume. Neither is wrong; they imply different code organization (resume as a top-level module vs. resume as a flag through existing modules).

10. **INV-005/INV-007 commitment timing:** Partially resolved. Both agree OQ-007/008 must resolve before M2 dispatch is built. The disagreement is whether to enumerate the *resolution* (Sonnet's M4 items) or the *open question* (Opus's OQ register) in the roadmap. This is documentation convention.

### Convergence Score: 0.55

Strong agreement on architectural core, dependency spine, risk taxonomy, and most invariants. Substantive disagreement persists on milestone structure (8 vs 8 with different boundaries), timeline realism, and whether operational/validation work deserves dedicated milestones. The disagreements are well-reasoned on both sides and reflect genuine tradeoffs rather than confusion — neither variant collapses under scrutiny. A merged variant would adopt Sonnet's scoping discipline with Opus's wave-architecture clarity, explicitly named buffer, embedded per-wave testing + one integration phase, and a single combined release+operations milestone.
