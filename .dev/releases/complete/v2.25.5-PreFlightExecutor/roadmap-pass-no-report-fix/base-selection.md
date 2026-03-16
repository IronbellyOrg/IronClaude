---
base_variant: A
variant_scores: "A:81 B:74"
---

## Scoring Criteria

Derived from debate convergence points and remaining disputes:

1. **Implementation Precision** (25 pts) — Explicit flags, exact attribute names, concrete insertion points, no ambiguous instructions
2. **Test Strategy Soundness** (20 pts) — Risk-appropriate test placement, coverage of full state matrix
3. **OQ/Risk Tracking Rigor** (15 pts) — Named identifiers, explicit resolution tracking for blocking unknowns
4. **Phase Structure & Project Management** (15 pts) — Milestone clarity, timeline concreteness, sequential discipline
5. **Documentation & Architectural Synthesis** (15 pts) — Architect summary, inline principle placement, concurrency debt documentation
6. **Operational Clarity** (10 pts) — Log terminology, role specification, handoff readiness

---

## Per-Criterion Scores

### Criterion 1: Implementation Precision (25 pts)

| Variant | Score | Evidence |
|---------|-------|----------|
| A (Opus) | 23 | Explicit `mkdir(parents=True, exist_ok=True)`, `started_at.timestamp()` as float, DEBUG label `option_d`/`option_a_or_noop`, exact signature `(config: SprintConfig, phase: Phase, started_at: float) -> bool`. Debate confirmed Haiku conceded `mkdir` flags entirely. |
| B (Haiku) | 18 | "Create parent directory if needed" — underspecified (debate-confirmed deficiency). Function signature present but lacks float-conversion call-site detail. Log labels `executor-preliminary`/`agent-written/no-op` are operationally cleaner but lose spec-traceability at DEBUG level. |

### Criterion 2: Test Strategy Soundness (20 pts)

| Variant | Score | Evidence |
|---------|-------|----------|
| A (Opus) | 16 | Interleaved tests with immediate feedback loops. T-001–T-005 in P2, T-003/T-006 in P3. Debate outcome: adopt Opus cadence as default. Risk of compound error on mtime/freshness semantics is real. |
| B (Haiku) | 15 | Consolidated Phase 4 with well-structured 5-layer validation framework (Functional / Backward Compatibility / Prompt Contract / Regression / Architect Sign-off). Debate partially vindicated B's framework structure. Score close; B's framework is superior but cadence is the weaker default. |

### Criterion 3: OQ/Risk Tracking Rigor (15 pts)

| Variant | Score | Evidence |
|---------|-------|----------|
| A (Opus) | 13 | OQ-001 through OQ-008 named with specific resolution actions (read `ClaudeProcess.__init__`, grep for `_write_crash_recovery_log()` etc.). Enables cross-referencing. Debate: identifiers retained in merged roadmap. |
| B (Haiku) | 9 | "Verify key structural assumptions" collapses 8 OQs into implicit checklist. Resolved OQ-001–OQ-004 and OQ-007 by name in Phase 0 deliverables but loses granularity. Debate confirmed B's approach weaker for handoff scenarios. |

### Criterion 4: Phase Structure & Project Management (15 pts)

| Variant | Score | Evidence |
|---------|-------|----------|
| A (Opus) | 11 | 5-phase plan, clear exit criteria per phase. Missing explicit Phase 0 milestone (baseline recon absorbed into P1). Qualitative effort labels only; debate accepted Haiku's numeric estimates as superior for sprint planning. |
| B (Haiku) | 13 | 6-phase plan with explicit Phase 0 milestone (M0). Numeric estimates (0.25/0.5/0.25/0.25/0.75/0.5 = 2.5 phase-days). Named team roles (1 backend engineer, 1 QA reviewer, lightweight arch review). Debate: Phase 0 separation prevents recon being absorbed under time pressure. |

### Criterion 5: Documentation & Architectural Synthesis (15 pts)

| Variant | Score | Evidence |
|---------|-------|----------|
| A (Opus) | 12 | Inline principle placement at implementation phases. SC table well-structured. Missing explicit Architect Recommendation Summary section. Debate: A conceded synthesis section as valuable. |
| B (Haiku) | 14 | Dedicated "Architect Recommendation Summary" section with 5 numbered principles. Explicit concurrency debt documentation. Debate: B's synthesis section is a first-class architectural record Opus lacks. |

### Criterion 6: Operational Clarity (10 pts)

| Variant | Score | Evidence |
|---------|-------|----------|
| A (Opus) | 6 | `option_d`/`option_a_or_noop` as DEBUG labels requires spec lookup. Debate synthesis: use B's primary labels with A's as parenthetical context. Solo implementer assumption implicit. |
| B (Haiku) | 5 | `executor-preliminary`/`agent-written/no-op` operator-readable. Explicit role specification (1 engineer + 1 QA + arch review). However, B scores slightly lower because the debate synthesis favors combining both label approaches, not pure B. |

---

## Overall Scores

| Variant | C1 | C2 | C3 | C4 | C5 | C6 | Total |
|---------|----|----|----|----|----|----|-------|
| A (Opus) | 23 | 16 | 13 | 11 | 12 | 6 | **81** |
| B (Haiku) | 18 | 15 | 9 | 13 | 14 | 5 | **74** |

**A wins by 7 points.** The margin is driven primarily by implementation precision (C1: +5) and OQ tracking rigor (C3: +4), which are the highest-risk failure modes for a sequencing-sensitive patch executed under time pressure.

---

## Base Variant Selection Rationale

**Variant A (Opus) is the base.**

The core strength of A is actionability at the point of implementation. Explicit `mkdir(parents=True, exist_ok=True)`, named OQ identifiers with resolution actions, and interleaved tests that catch mtime-semantics bugs before integration complexity is layered on — these are not style preferences; they are defect-prevention mechanisms for the specific risks this patch carries.

The debate confirmed Haiku conceded the two most consequential technical points: `mkdir` flag specification and sentinel contract comment timing (P5 → P2). These were not minor — an implementer following B's original guidance would have written a defect in directory creation and deferred a critical comment to the phase most likely to be skipped.

A's weaker areas (Phase 0 separation, timeline concreteness, Architect Recommendation Summary) are all additive improvements that can be incorporated from B without changing A's structure.

---

## Improvements to Incorporate from Variant B

These are concrete additions to Variant A to produce the merged roadmap:

**1. Phase 0 as Explicit Milestone (from B §Phase 0)**
Extract A's Phase 1 verification steps into a dedicated Phase 0 with milestone M0 ("Implementation prerequisites verified, no hidden blockers found") and a 0.25 phase-day estimate. This prevents baseline recon from being absorbed into implementation under sprint time pressure.

**2. Numeric Timeline Estimates (from B §6)**
Replace A's qualitative effort labels (Small/Medium/Small/Small) with B's numeric breakdown: P0=0.25, P1=0.5, P2=0.25, P3=0.25, P4=0.75, P5=0.5 (total: 2.5 phase-days). Annotate as subject to revision after P0 closes open questions (A's caveat from Round 2 rebuttal).

**3. Architect Recommendation Summary section (from B §Architect Recommendation Summary)**
Append B's five-principle synthesis section verbatim as a named section. Per debate convergence: principles should also appear inline at relevant phases (A's approach), AND as a standalone summary (B's approach). Both are included.

**4. 5-Layer Validation Framework labels (from B §Validation Approach)**
Reorganize A's Phase 5 acceptance criteria under B's named validation layers: Baseline / Unit / Integration / Regression / Architect Sign-off. This provides structural clarity for the QA reviewer role without changing what is tested.

**5. Explicit team role specification (from B §Resource Requirements)**
Add to A's Resource Requirements: "1 backend/CLI engineer, 1 QA reviewer, lightweight architecture review recommended" with B's rationale (anchoring bias on self-review).

**6. Log label synthesis (from Round 2 convergence)**
A's Phase 3 injection step should specify: primary log labels `executor-preliminary` / `agent-written` (INFO/WARNING visibility), with `option_d` / `option_a_or_noop` as parenthetical context in DEBUG messages. Neither label set is excluded.

**7. Critical Path statement (from B §Timeline)**
Add B's explicit critical-path statement: "Phases 0–2 before any new tests; Phase 4 immediately after prompt and integration; do not merge until Phase 5 full sprint regression passes."
