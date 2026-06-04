---
total_diff_points: 12
shared_assumptions_count: 14
---

# Comparative Diff Analysis: Opus vs Sonnet Roadmap Variants

## Shared Assumptions and Agreements

Both variants converge on the following 14 architectural and process commitments:

1. **Python ≥3.10 + UV-only toolchain** (AC-001) — no `pip`/`python -m` invocations.
2. **`superclaude swarm` as a new top-level CLI verb** (AC-002), not nested under sprint/roadmap.
3. **Module shape mirrors `cli/sprint/`** (AC-003, NFR-015) for operator familiarity.
4. **Concurrency via `superclaude.execution.parallel.ParallelExecutor`** wrapping `ThreadPoolExecutor` (AC-004, IMM-3, INV-002, NFR-001) — shell `swarm_dispatch.sh` retired.
5. **httpx as the Phase-1 reference transport** (AC-005, COMP-032) with a deterministic stub for tests (COMP-033/FR-023).
6. **Mechanical-only merge boundary**: ≤30 LOC ceiling, 4 structural guards, no scoring/dedup/reorder/filter (FR-012, NFR-008/009, AC-011/012/018) — `/sc:adversarial` retains scored-merge ownership.
7. **Manifest as durable source-of-truth for resume** (INV-001/016) with `--force-relens` opt-in escape hatch (FR-025).
8. **Prompt-injection guard (§11.5) enforced uniformly across all 3 prompt-input paths** (lens / JSON-Schema / custom-prompt-dir) with INV-003/INV-014 parity tests.
9. **Empty-target STOP guard** (IMM-4): <50 non-whitespace bytes → `failed`/`target-too-small` before dispatch.
10. **Success-first status policy** (IMM-5): floor=2, success_first=true, with M==N==2→success edge case.
11. **Atomic writes via tmp+os.replace** (IMM-6, NFR-002) and lock-coordinated JSONL appends (NFR-002).
12. **Three amalgamation modes** (raw / normalize / normalize+merge) with `normalize` as default (FR-011).
13. **8-entry lens registry** (bare-review, refactor-find, edge-case-hunt, spec-completeness, feasibility-probe, troubleshoot-hypothesis, doc-completeness, custom) — FR-009/COMP-024-030.
14. **6-recipe normalizer registry** with `custom-py:module:func` dynamic loader (FR-010, COMP-015-021).

Plus full agreement on: opt-in `--tui` (INV-012), tmux detached mode (FR-014/AC-008), provider-neutral contract surface (AC-013/NFR-016), non-Claude caller compatibility (FR-030), source-of-truth discipline (AC-019), Phase-1 modality exclusions (AC-016), and `sc-bare-review` thin-caller migration with A/B parity (FR-029).

## Divergence Points

### 1. **Total Timeline: 16 vs 10 weeks**

- **Opus:** 16 weeks (8 milestones × 2 weeks each), with note that M6/M7 could overlap to compress to ~14 weeks if resourced in parallel.
- **Sonnet:** 10 weeks total — M1=1wk, M2=2wk, M3=1wk, M4=1wk, M5=1wk, M6=2wk, M7=1wk, M8=1wk.

**Impact:** Opus is more conservative and allocates uniform 2-week blocks per milestone, allowing slack for the irreducible wave-pipeline spine. Sonnet is more aggressive — likely realistic only if engineers are already fluent with the patterns and dependencies are pre-resolved.

### 2. **Milestone Decomposition: Wave-Aligned vs Concern-Aligned**

- **Opus:** Decomposes by Wave (M2=Wave 0, M3=Wave 1, M4=Wave 2, M5=Wave 3, M6=Resume, M7=Observability, M8=Migration). Each milestone is one architectural layer.
- **Sonnet:** Decomposes by concern bundles (M1=contracts+models, M2=dispatch+state+transport+observability together, M3=normalization+reduction+merge together, M4=lenses+preflight+resume together, M5=CLI surface, M6=validation, M7=migration, M8=ops rollout).

**Impact:** Opus's wave-aligned approach maps cleanly to the architecture diagram and produces tighter per-milestone exit criteria but more cross-milestone integration handoffs. Sonnet's concern-bundled approach reduces handoffs but creates wider, riskier milestones (M2 bundles 4 distinct concerns; M4 bundles lens+guard+resume).

### 3. **Foundation Milestone Scope**

- **Opus M1:** 29 items — strict foundation (data models + module shape + CLI group placeholder only). 2 weeks.
- **Sonnet M1:** 45 items — bundles ALL architectural constraints (AC-001 through AC-019), all 20 data models, AND module boundary creation including preflight/schema/commands stubs. 1 week.

**Impact:** Opus reserves architectural-constraint enforcement to later milestones (where they bind to real code). Sonnet front-loads them into M1 as cross-cutting commitments. Sonnet's M1 may be infeasible at 1 week given 45 items; Opus's split is more defensible but creates risk of constraint drift.

### 4. **Dedicated Validation Milestone**

- **Opus:** No standalone validation milestone — testing distributed across M3/M5/M8 with per-IMM/per-INV coverage (NFR-007 in M8).
- **Sonnet:** Dedicated **M6: Invariant and Integration Validation** with 9 explicit TEST-### items (TEST-001 IMM suite, TEST-002 INV suite, TEST-003 parity, TEST-004 lens validation, TEST-005 non-Claude caller, TEST-006 mechanical merge boundary, TEST-007 resume E2E, TEST-008 migration verification).

**Impact:** Sonnet's explicit validation gate creates a clean release-readiness signal but defers test work, risking discovery-of-defect cost. Opus's continuous testing approach finds defects earlier per-wave but lacks a single "go/no-go" milestone — release readiness is implicit in M8 completion.

### 5. **Dedicated Operational Rollout Milestone**

- **Opus:** No operational rollout milestone — runbook/observability/rollback subsumed under M7 (Observability) and migration documentation under M8.
- **Sonnet:** Dedicated **M8: Operational Rollout and Documentation** with 6 OPS-### items (runbook, env readiness, observability procedure, rollback, lens contribution policy, post-release metrics review).

**Impact:** Sonnet treats operational maturity as a first-class deliverable. Opus treats it as a release-completion concern. Sonnet's approach is better for production handoff; Opus's compresses time-to-feature-complete.

### 6. **CLI Surface Sequencing**

- **Opus:** Defers full CLI surface (`status`/`logs`/`attach`/`kill`/`scaffold`) to **M7** after pipeline + resume are complete. `run`/`validate`/`validate-lenses` land earlier in M2/M3.
- **Sonnet:** Bundles entire operator surface (all 8 subcommands + TUI + tmux + `--resume`) into **M5** after dispatch/normalize/reduce/lenses exist.

**Impact:** Opus's later CLI delivery means resume (M6) ships before attach/kill (M7) — operators get pipeline correctness before lifecycle controls. Sonnet's earlier CLI delivery means operators see the full surface in M5 but with resume not yet validated (M5 ships before M6 validation).

### 7. **Resume Milestone Independence**

- **Opus:** **M6: Resume, Crash Recovery & Manifest** is a dedicated reliability milestone after M5 (reduce+merge).
- **Sonnet:** Folds resume into **M4** alongside lens registry and preflight (`FR-015` is an M4 item), because Sonnet sees resume as a preflight-rehydration concern.

**Impact:** Opus surfaces resume as a distinct reliability investment with its own risk profile. Sonnet treats it as natural extension of preflight, which is structurally accurate but may obscure the resume-specific risks (R-3 lens-mutation interaction, R-7 schema evolution).

### 8. **INV-005/INV-007 Placement (Worker-Count + Empty-Pool Guards)**

- **Opus:** Not explicitly enumerated as milestone items; flagged as open questions OQ-007/OQ-008 to resolve before M3 entry.
- **Sonnet:** Lands as explicit M4 items (INV-005 worker count vs model pool guard; INV-007 empty model pool failure path) with completed behavior specifications.

**Impact:** Sonnet commits to behavior at roadmap time; Opus defers commitment pending architect decision. Sonnet's approach risks pre-committing to wrong semantics; Opus's risks underspecified milestone exit.

### 9. **Milestone-to-Milestone Dependency Density**

- **Opus dependency graph:** Mostly linear with M6/M7 branching from M5. Total deps: ~10 edges.
- **Sonnet dependency graph:** Explicitly declares "M1→M2→M3→M4→M5→M6→M7→M8 + M1→M4 + M2→M5 + M3→M6 + M4→M6 + M6→M8" — more cross-milestone edges.

**Impact:** Opus's sparser dependency graph permits parallel execution of M6 (resume) and M7 (observability). Sonnet's denser graph implies tighter sequencing and less parallelization opportunity, but better captures real bind-points (e.g., M3 recipes → M6 validation).

### 10. **Risk Register Granularity**

- **Opus:** 10 risks (R-1 through R-10), each with single-paragraph mitigation.
- **Sonnet:** 23 risks (R-001 through R-023), per-milestone tabulated risks plus consolidated register, including operational risks (R-020 rollout-without-observability, R-021 doc-drift, R-022 env-readiness).

**Impact:** Sonnet provides finer-grained risk coverage including production-readiness risks Opus omits. Opus's terser register is easier to scan but underweights operational risk surface.

### 11. **Open Questions Inventory**

- **Opus:** 10 OQs distributed across M2/M3/M5/M6, with explicit owners and target resolution windows.
- **Sonnet:** 10 OQs distributed across M1/M4/M5, with explicit owners — but several OQs are forced to resolve in M1 (OQ-006/008/009/010 must be resolved before M1 exit) to lock the schema.

**Impact:** Sonnet's front-loading of OQs into M1 creates schedule risk if owners are slow; Opus's distribution spreads decision pressure across the pipeline but allows decisions to be made when context is richest.

### 12. **Item Count and Granularity**

- **Opus:** 133 numbered items across all milestones (M1=29, M2=27, M3=26, M4=12, M5=11, M6=8, M7=17, M8=3).
- **Sonnet:** 153 numbered items across all milestones (M1=45, M2=26, M3=18, M4=31, M5=13, M6=9, M7=5, M8=6).

**Impact:** Sonnet has ~15% more line items, primarily from front-loading M1 (45 vs 29) and adding explicit TEST/OPS items in M6/M8. Opus's per-milestone density is more even, suggesting more balanced work distribution.

## Areas Where One Variant Is Clearly Stronger

### Opus Stronger

- **Wave-architecture mapping**: M2=Wave 0, M3=Wave 1, M4=Wave 2, M5=Wave 3 mirrors the architecture exactly, making the roadmap directly traceable to the spec's pipeline diagram.
- **Critical-path clarity**: Explicitly identifies M2→M3→M4→M5 as "the irreducible wave-pipeline spine" with M6/M7 as parallelizable branches.
- **Per-milestone Integration Points tables**: Every milestone has a structured "Artifact / Type / Wired / Consumed By" table making cross-milestone bindings explicit.

### Sonnet Stronger

- **Validation as gate**: Dedicated M6 with 8 enumerated TEST items provides a clean release-readiness gate Opus lacks.
- **Operational rollout**: Dedicated M8 with runbook/readiness/rollback/policy treats production handoff as first-class — Opus omits this entirely.
- **Risk surface coverage**: 23 risks vs 10, including operational risks (env readiness, doc drift, rollout observability) Opus omits.
- **Item-level commitment to INV-005/INV-007**: Removes ambiguity Opus leaves as open questions.
- **Forward-compat schema rule** (NFR-006): explicit "orchestrator 1.1 loads spec 1.0" rule for resume durability — Opus mentions it less prominently.

## Areas Requiring Debate to Resolve

1. **Foundation milestone scope (Opus M1 vs Sonnet M1)**: Should M1 freeze ALL architectural constraints + data models + module stubs (Sonnet) or only data models + module shape (Opus)? Affects schedule realism and constraint-drift risk.

2. **Dedicated validation gate (Sonnet M6 yes/no)**: Is a single validation milestone the right release-readiness signal, or should testing be embedded per-wave (Opus)? Affects test-discovery cadence and release confidence.

3. **Dedicated operational rollout (Sonnet M8 yes/no)**: Does the project need explicit operational rollout work, or is operator documentation a byproduct of feature completion? Affects production-readiness posture.

4. **CLI surface delivery timing**: Should operators get full CLI in M5 (Sonnet) before resume is validated, or wait until M7 (Opus) after pipeline+resume are proven? Affects operator feedback loop vs feature stability.

5. **Resume as standalone milestone (Opus M6) vs preflight extension (Sonnet M4)**: Does resume deserve a dedicated reliability investment or is it naturally a preflight concern?

6. **Timeline realism**: 16 weeks (Opus, conservative) vs 10 weeks (Sonnet, aggressive). Sonnet's M1 at 1 week with 45 items and M2 at 2 weeks with 26 items spanning dispatch/state/transport/observability appears compressed. Opus's uniform 2-week blocks may be over-padded for simpler milestones like M4 (12 items) and M5 (11 items).

7. **Pre-resolution of INV-005/INV-007**: Should worker-pool guard semantics be committed at roadmap time (Sonnet) or deferred to architect decision (Opus)?

8. **Risk register granularity**: Is 10 risks (Opus) sufficient operational signal, or does 23 risks (Sonnet) better surface latent operational concerns?
