# Research: Invariant Preservation Probe — NFR-CONV.6..10

**Status:** Complete
**Date:** 2026-05-14
**Agent type:** Architecture Analyst
**Source corpus:** all 6 source files at invariant-anchor lines + invariant-probe.md

---

## Section 1 — 5 Load-Bearing Invariants Table

Each row maps an invariant to (a) its verified operational source, (b) a verbatim mechanism quote from that source, (c) the NFR-CONV.6..10 row that pins preservation, and (d) the FR Acceptance Criteria that route any MEDIUM invariant-probe finding through gate-visible behavior.

| # | Invariant | Operational source (file:line, verified current) | Mechanism — verbatim quote | NFR-CONV mapping | FR(s) routing MEDIUM probe findings |
|---|-----------|--------------------------------------------------|----------------------------|------------------|-------------------------------------|
| 1 | **self-contained-item** | `src/superclaude/skills/task-builder/SKILL.md:1452-1457` | `- [ ] **1.1 — [Step Title]** / **Context**: [...] / **Action**: [...] / **Output**: [...] / **Verification**: [...] / **Completion gate**: [...]` (5-field schema, verified at the cited lines) | NFR-CONV.6 — "5-field per-item schema MUST remain operational across all 8 TB-Add checks and the Execution Context header" (`PRD_TASK_BUILDER_CONVERGENCE.md:555`) | FR-CONV.2 (header is task-level, not item-level — INV-014, INV-015 route here) |
| 2 | **evidence-bound-item** | `src/superclaude/skills/task-builder/SKILL.md:1530` rule #2 | "**Evidence-based claims only.** Every finding must cite actual file paths, line numbers, function names. No assumptions, no inferences, no guessing. If unverifiable, mark as 'Unverified.'" | NFR-CONV.7 — "Every per-item Context referencing code surface MUST retain file:line citation OR justified-absence (TB-Add-8 enforces)" (`PRD_TASK_BUILDER_CONVERGENCE.md:556`) | FR-CONV.1 (TB-Add-8) and FR-CONV.2 (Negative scopes the header) — routes INV-015 |
| 3 | **persistent-.dev/tasks/-artifact** | `SKILL.md:1536` rule #5 ("Preserve research artifacts...persist after the task file is built") combined with OPEN-INV-018 (shared assumption A-001 promoted in invariant-probe.md:33) | "**Preserve research artifacts.** Research files, analyst reports, and QA reports persist after the task file is built. They serve as the evidence trail. Do NOT delete intermediate files." | NFR-CONV.8 — "Research/qa persistence in `.dev/tasks/<task-id>/` MUST remain unchanged" (`PRD_TASK_BUILDER_CONVERGENCE.md:557`) | FR-CONV.3 (Inherited Structural Verdict block reads from `.dev/tasks/<task-id>/qa/` — INV-018 portfolio note) |
| 4 | **zero-trust QA** | `src/superclaude/agents/rf-qa.md:144-146` | "**PASS** — All checks pass, no gaps of any severity. Green light for synthesis. / **FAIL** — Any gaps exist (CRITICAL, IMPORTANT, or MINOR). [...] ALL gaps must be resolved before proceeding — no severity level is exempt." | NFR-CONV.9 — "'Any gap regardless of severity = FAIL' stance (rf-qa.md:140-142) MUST remain operative; no TB-Add or PR-04 mechanism weakens it" (`PRD_TASK_BUILDER_CONVERGENCE.md:558`) | FR-CONV.3 (anti-inflation), FR-CONV.4 (severity floor), FR-CONV.5 (monotonicity), FR-CONV.6 (synthetic-dnsp HIGH) — routes INV-002, INV-019 |
| 5 | **parallel-research** | `rf-qa.md:49-77` ("Parallel Partitioning"); `rf-qa-qualitative.md:50-82` ("Parallel Partitioning"); INV-021 | "When the workload is large (many files to verify), the orchestrator can spawn **multiple rf-qa instances in parallel**, each assigned a different subset of files. This prevents context rot — no single QA agent needs to hold all files in context simultaneously." (`rf-qa.md:51`) and identically in `rf-qa-qualitative.md:52` | NFR-CONV.10 — "rf-analyst / rf-qa partition cohort MUST remain parallel; DNSP fires within-agent-instance (INV-021)" (`PRD_TASK_BUILDER_CONVERGENCE.md:559`) | FR-CONV.6 (synthetic-dnsp fires within-agent-instance) — routes INV-021 |

**Verification of currency** — All file:line anchors above were re-read this turn (SKILL.md:1450-1460, SKILL.md:1527-1535, rf-qa.md:49-77, rf-qa.md:144-146, rf-qa-qualitative.md:50-82). No mtime drift detected in the session-context envelope.

---

## Section 2 — MEDIUM Invariant-Probe Findings Cross-Reference Matrix

Source: `.dev/releases/current/task-builder-merge/adversarial/invariant-probe.md`. The probe identified 5 UNADDRESSED-MEDIUM findings (per probe restated summary at line 53). Each is routed below to the FR Acceptance Criterion that turns the residual risk into a gate-visible test, plus to the invariant it most directly threatens.

| Probe ID | Severity / Status | Probe statement (verbatim, condensed) | Threatened invariant | FR routing (where the residual risk becomes a gate check) |
|----------|-------------------|----------------------------------------|----------------------|------------------------------------------------------------|
| **INV-002** | UNADDRESSED MEDIUM (probe line 12) | "PR-04 inherited verdict state in rf-qa-qualitative prompt may persist across fix cycles even after rf-qa re-runs and updates verdict [...] If A.10 re-runs after fix and produces new verdict, the orchestrator MUST re-inject — not specified explicitly." | zero-trust QA (#4) | **FR-CONV.3** — cycle-N+1 reinjection rule. The Negative Criterion at PRD §14.1 (`PRD line 499`) "no stale verdict from a prior fix cycle is permitted to govern current-cycle decisions" forces the verdict to be re-read at every fix cycle. |
| **INV-006** | UNADDRESSED LOW (probe line 16; listed here because it is the canonical calibration-deferral finding) | "PR-06 TB-Add-2 bounds (>=3 and <=40 track / <=50 single-track) are speculative without empirical calibration from `.dev/tasks/done/`. ADVISORY-fail (warn not block) until calibrated." | self-contained-item (#1) — granularity dimension | **Calibration OPEN-INV-006** — TB-Add-2 item-count-bounds stays `[ADVISORY]` until calibration produces empirical thresholds. Does not route to a Negative Criterion until Phase-2 (NFR-CONV.6 fixture validates schema, not bounds). |
| **INV-010** | UNADDRESSED MEDIUM (probe line 20) | "PR-04 + PR-06 sequencing: if PR-04 lands before PR-06, the inherited verdict is 'thin' (only the existing 9-item set). When PR-06 lands, the verdict richens — but rf-qa-qualitative's prompt template must be updated to reference the new TB-Add items by name." | zero-trust QA (#4) — completeness dimension | **FR-CONV.3** dynamic checklist enumeration. PRD §11 Phase-2 specifies the consumer-side template auto-richens when FR-CONV.1 catalogue grows; the Acceptance Criterion's Verification clause inspects the prompt template for dynamic enumeration rather than hardcoded names. |
| **INV-012** | UNADDRESSED MEDIUM (probe line 22) | "PR-02 + PR-03 stacking: if a partition agent fails (PR-03 DNSP fires) inside a multi-cycle retry (PR-02 governs), does the synthetic finding count as a 'failure' for monotonicity purposes? [...] synthetic findings count as failures for \|F_n\| BUT a synthetic for the same range across consecutive cycles is a dedup case [...] not a regression." | zero-trust QA (#4) + parallel-research (#5) | **FR-CONV.5 + FR-CONV.6** — dedup-key composition. FR-CONV.6 Negative (PRD line 540) "the dedup-key collapse MUST NOT cross-cycle (PR-02 monotonicity treats dedup as not-regression per INV-012)" routes this exact composition; FR-CONV.5's `|F_n|` definition includes synthetic findings. |
| **INV-013** | ADDRESSED LOW (probe line 23; routed because the composition matters) | "PR-07 5-axis overlay + PR-04 inherited verdict: when rf-qa-qualitative receives both the verdict (PR-04) AND the 5 axes (PR-07), the axes must be applied to the items NOT covered by inherited PASS." | zero-trust QA (#4) | **FR-CONV.3 + FR-CONV.4** — clean composition. The 5 axes are semantic; they live in the items rf-qa-qualitative still runs (i.e., items NOT covered by inherited structural PASS). FR-CONV.4 Negative "axes annotate, they do not substitute" prevents axis-from-overlay substitution; FR-CONV.3 Negative prevents PASS-from-inheritance substitution. |
| **INV-015** | UNADDRESSED MEDIUM (probe line 30) | "PR-01 'no specific file paths' rule could leak into per-item Context if rf-task-builder misreads scope. [...] Refactor plan should require an A.10 check: 'Every Context field that references a code surface includes at least one file:line citation.'" | evidence-bound-item (#2) | **FR-CONV.2 + FR-CONV.1** — TB-Add-8 enforces evidence-bound-item per-item; FR-CONV.2 Negative scope-confines the header to no-paths rule explicitly so the rule does NOT leak to per-item Context. |
| **INV-019** | ADDRESSED LOW (probe line 34) | "PR-04 passthrough must NOT cause rf-qa-qualitative to mark items VERIFIED that rf-qa marked PASS structurally but require semantic verification." | zero-trust QA (#4) | **FR-CONV.3 Self-Audit mandate** — anti-inflation operational test. K-003 audit-target. Negative at PRD line 499 "every VERIFIED item must show an independent semantic-check engagement in the Self-Audit listing". |
| **INV-021** | ADDRESSED LOW (probe line 36) | "PR-03 DNSP fires after the entire escalation ladder exhausts — does this serialize the partition-agent cohort? [...] DNSP preserves parallel-research by allowing N-1 partitions to complete." | parallel-research (#5) | **FR-CONV.6** — parallel-research preservation. Negative (PRD line 540) "DNSP fires within-agent-instance, not cross-cohort". |

**Routing logic summary**: every MEDIUM that the probe left UNADDRESSED is captured by at least one FR Negative Criterion, ensuring the residual risk shows up as a gate failure if violated rather than silently degrading invariant fidelity.

---

## Section 3 — Preservation-Proof Matrix

For each of the 6 FRs, the Negative Criterion is quoted verbatim from `PRD_TASK_BUILDER_CONVERGENCE.md` §14.1 (FR Acceptance Criteria, lines 473–540), then mapped to the invariant it preserves and the failure mode it forecloses.

### FR-CONV.1 — Add 8 new structural checks to rf-qa A.10 / 15-item task-qualitative bundle

**Negative Criterion (verbatim, PRD line 473):**
> "No existing rf-qa check is renamed, renumbered, or removed; the 9-item A.10 and 15-item validation existing-items are preserved verbatim; bundle-specific `/sc:tasklist` checks (phase-file naming, index references) MUST NOT appear in any TB-Add."

**Preserves: zero-trust QA (#4)** — by forbidding rename/renumber/removal of any existing rf-qa check, this clause makes the "Any gap regardless of severity = FAIL" stance (rf-qa.md:144-146) inalterable by FR-CONV.1's additive changes. The 15-item existing items are likewise preserved. Bundle-specific sc-tasklist checks are explicitly disallowed because they would be domain-mismatched and could weaken adversarial coverage in a task-builder context. **Failure mode foreclosed**: a TB-Add that quietly relaxes A.10's gate semantics.

### FR-CONV.2 — Pre-implementation Execution Context header

**Negative Criterion (verbatim, PRD line 486):**
> "Per-item Context fields elsewhere in the file MUST retain file:line citations OR justified-absence comments (validated by TB-Add-8); the per-item self-contained 5-field schema MUST NOT be altered or supplemented by header content."

**Preserves: evidence-bound-item (#2) and self-contained-item (#1)** — explicit dual preservation. The clause confines the new task-level header to no-paths scope (header IS scope-confined), while keeping per-item Context obligated to evidence (file:line OR justified-absence). The 5-field schema at SKILL.md:1452-1457 is held inviolate. **Failure mode foreclosed (INV-015)**: header's "no specific file paths" rule leaking into per-item Context fields and stripping evidence.

### FR-CONV.3 — Inherited Structural Verdict Block (PR-04 passthrough)

**Negative Criterion (verbatim, PRD line 499):**
> "rf-qa-qualitative MUST NOT mark any item VERIFIED solely from the inherited verdict — every VERIFIED item must show an independent semantic-check engagement in the Self-Audit listing; anti-inflation rule rf-qa-qualitative.md:766-775 MUST NOT be weakened, removed, or rephrased; no stale verdict from a prior fix cycle is permitted to govern current-cycle decisions."

**Preserves: zero-trust QA (#4)** — three independent guards in one clause: (a) Self-Audit-listed semantic-check engagement is mandatory for VERIFIED; (b) the anti-inflation rule at rf-qa-qualitative.md:766-775 is byte-stable; (c) cycle-N+1 reinjection forecloses stale-verdict carryover. **Failure modes foreclosed (INV-002, INV-019)**: inherited PASS quietly counting as semantic VERIFIED, anti-inflation weakening, or stale verdict governing a new cycle.

### FR-CONV.4 — 5-axis adversarial overlay on the 15-item task-qualitative checklist

**Negative Criterion (verbatim, PRD line 512):**
> "The existing 15-item task-qualitative checklist MUST NOT be removed, reordered, or replaced — axes annotate, they do not substitute; the severity floor at rf-qa-qualitative.md:789 MUST NOT be weakened; no axis may rely on a code-path change (overlay-only, per CB-3)."

**Preserves: zero-trust QA (#4)** — three guards: (a) the 15-item checklist body is byte-stable; (b) severity floor (the "Any gap = FAIL" derivative for qualitative gate) is unweakened; (c) overlay-only constraint (CB-3) — axes never replace structural code-paths. **Failure modes foreclosed (INV-013 composition risk)**: axes substituting for a check, severity floor relaxation, or hidden code-path change masquerading as "annotation".

### FR-CONV.5 — Strict-shrink monotonicity halt for fix-cycle retries

**Negative Criterion (verbatim, PRD line 527):**
> "Legitimate slow-cycle correction MUST NOT be halted — any cycle where `|F|` strictly shrinks (even by 1) continues; the four independent retry counters MUST NOT be collapsed into a shared monotonicity state; no halt-on-slow-convergence threshold (e.g., `F_{n+1} = F_n - 1`) is permitted (X-003 REJECTED)."

**Preserves: zero-trust QA (#4)** — three guards: (a) slow-shrink (|F| shrinking by 1) is permitted, so a legitimate slow cycle is not falsely halted (preserves convergence); (b) 4 independent retry counters are not collapsed (preserves INV-001 — independent counters per retry class); (c) X-003 halt-on-slow-convergence threshold is forbidden. **Failure mode foreclosed**: false-positive halt that would abandon a valid in-progress convergence and present a non-converged state as a frozen verdict.

### FR-CONV.6 — Synthetic Do-Not-Silently-Pass (DNSP) finding for failed partition agents

**Negative Criterion (verbatim, PRD line 540):**
> "Synthetic-dnsp MUST NOT emit before the escalation ladder exhausts — proposal line 35 all-agents-fail guard runs first; the existing escalation behavior at rf-team-lead.md:417 (3 fix cycles per phase) MUST NOT be replaced or short-circuited; synthetic findings MUST NOT mask real findings — HIGH severity ensures gate-level visibility; the dedup-key collapse MUST NOT cross-cycle (PR-02 monotonicity treats dedup as not-regression per INV-012)."

**Preserves: parallel-research (#5) and zero-trust QA (#4)** — four guards: (a) DNSP fires per-partition, not cross-cohort, so N-1 partitions continue (preserves parallel-research per INV-021); (b) all-agents-fail guard preserves the existing rf-team-lead.md:417 escalation (3 fix cycles per phase); (c) synthetic findings carry HIGH severity so they are gate-visible and cannot mask real findings; (d) dedup-key collapse does not cross-cycle, harmonising with FR-CONV.5 monotonicity (INV-012). **Failure modes foreclosed**: cross-cohort serialization, existing escalation short-circuit, synthetic findings shadowing real failures, dedup as silent regression.

**Coverage summary**: each FR's Negative Criterion preserves at least one of the 5 invariants. Across all 6 FRs the coverage matrix is:

| Invariant | FR-CONV.1 | FR-CONV.2 | FR-CONV.3 | FR-CONV.4 | FR-CONV.5 | FR-CONV.6 |
|-----------|:---------:|:---------:|:---------:|:---------:|:---------:|:---------:|
| #1 self-contained-item | (additive only) | ✅ | — | — | — | — |
| #2 evidence-bound-item | (TB-Add-8 lives here) | ✅ | — | — | — | — |
| #3 persistent-.dev/tasks/-artifact | — | — | (read-target) | — | — | — |
| #4 zero-trust QA | ✅ | — | ✅ | ✅ | ✅ | ✅ |
| #5 parallel-research | — | — | — | — | — | ✅ |

No invariant is left uncovered by Negative Criteria across the six FRs.

---

## Section 4 — NFR-CONV.6..10 Verification Fixtures

Per PRD §14.2, each invariant-NFR is paired with a synthetic-fixture-based Verification clause. Each row below names the fixture (or fixture pair), the pass/fail expectation, and the operational evidence the fixture exercises. All Verification clauses are quoted verbatim from `PRD_TASK_BUILDER_CONVERGENCE.md` lines 555–559.

| NFR | Invariant | Fixture (synthetic) | Pass / Fail behavior | Verbatim Verification (PRD line) |
|-----|-----------|---------------------|----------------------|----------------------------------|
| **NFR-CONV.6** | self-contained-item | (a) item with all 5 fields {Description/Context/Action/Output/Verification/Completion-gate} → PASS; (b) item with one field stripped → FAIL TB-Add-1 | All-5-fields fixture passes all 8 TB-Add checks; one-field-stripped fixture fails closed | "Synthetic fixture with all 5 fields passes all TB-Add checks; same with one field stripped fails TB-Add-1 — fails closed" (PRD line 555) |
| **NFR-CONV.7** | evidence-bound-item | (a) `Context: src/foo` → FAIL TB-Add-8 (no `:N`); (b) `Context: src/foo:42` → PASS; (c) `Context: <none — pure refactor> [justified-absence]` → PASS | Three-fixture triple: bare-path fails, file:line passes, justified-absence passes | "Synthetic fixture with bare `Context: src/foo` (no `:N`) fails TB-Add-8; same with `Context: src/foo:42` passes; same with `Context: <none — pure refactor> [justified-absence]` passes" (PRD line 556) |
| **NFR-CONV.8** | persistent-.dev/tasks/-artifact | diff of `.dev/tasks/` directory layout pre-merge vs post-merge | Zero structural changes: no new mandatory subdirectory, no rename of `research/`, `qa/`, `synthesis/`, `reviews/`; naming patterns stable | "Diff `.dev/tasks/` directory layout pre- and post-merge; no path, no naming pattern altered" (PRD line 557) |
| **NFR-CONV.9** | zero-trust QA | (a) 1-LOW-finding fixture → gate FAILs (no LOW escape); (b) FR-CONV.3 inherited verdict applied without independent semantic-check engagement → no item marked VERIFIED | LOW-finding fixture proves "Any gap regardless of severity = FAIL"; inherited-verdict fixture proves anti-inflation rule operative | "Synthetic fixture with 1 LOW finding fails the gate; FR-CONV.3 inherited verdict does NOT mark items VERIFIED in absence of independent semantic check" (PRD line 558) |
| **NFR-CONV.10** | parallel-research | spawn-log fixture: N partition agents spawned concurrently; one partition exhausts its escalation ladder | Spawn-log shows N concurrent agents; on one's exhaustion, N-1 continue to completion before DNSP synthesises; cohort is not serialised | "Spawn-log inspection: N partition agents run concurrently; on one agent's escalation exhaust, N-1 continue to completion before DNSP synthesises a finding" (PRD line 559) |

**Fixture coverage adequacy** — each fixture is **falsifiable** (concrete pass/fail), **deterministic** in its structural output (NFR-CONV.1 alignment), and uses only the existing tooling permitted by NFR-CONV.5 (Read, Grep, Glob, Bash). NFR-CONV.7's three-fixture triple is notable: it exercises the positive case AND the justified-absence escape-hatch, preventing TB-Add-8 from over-rejecting legitimate refactor items.

---

## Section 5 — Gaps and Questions

1. **INV-003 advisory operational obedience (UNADDRESSED MEDIUM, probe line 13)** — flagged by the probe and excluded from the 6 MEDIUMs routed in Section 2 because PR-05 was DEFERRED for Phase-1. If PR-05 is reintroduced in Phase-2, the rule "advisory is non-binding" requires a structural test (the PRD currently relies on agent prompt obedience to critical-rule #19). **Question**: should NFR-CONV.3 hidden-input determinism guard be strengthened to include a "tier output unchanged with fixture-populated vs empty `.dev/tasks/done/`" check that catches an advisory mistakenly weighting tier selection?
2. **INV-006 calibration empirical thresholds** — TB-Add-2 item-count bounds `[ADVISORY]` until calibration. **Gap**: no explicit Phase-2 owner is named in the PRD for performing the calibration sweep on `.dev/tasks/done/`. PRD §11 mentions Phase-2 but does not enumerate owners.
3. **INV-010 prompt-template auto-richen** — FR-CONV.3 specifies a dynamic checklist enumeration mechanism, but the **verification approach** (inspecting the prompt template for dynamic enumeration vs hardcoded names) is not yet operationalised as a TB-Add or rf-qa-qualitative check. **Question**: should an additional rf-qa A.10 check inspect the rf-qa-qualitative spawn-prompt template for placeholder syntax referencing FR-CONV.1's TB-Add catalogue?
4. **INV-018 directory-structure assumption** — all proposals assume `.dev/tasks/` layout is stable. **Gap**: no contingency in the PRD for `.dev/tasks/` restructuring (e.g., if research-artifacts are partitioned by topic). Risk is LOW per probe but unmitigated.
5. **NFR-CONV.8 verification specificity** — PRD line 557 says "no path, no naming pattern altered" but does not enumerate the path patterns being compared. A precise list (e.g., `research/`, `qa/`, `synthesis/`, `reviews/`, `adversarial/`, `task-file-name pattern`) would make the diff fixture deterministic.
6. **Spawn-log inspection tooling (NFR-CONV.10)** — the fixture requires a spawn-log artifact. **Question**: where does this log live in the project today? If no centralised spawn log exists, the fixture must be specified to capture spawn timestamps in an ad-hoc trace file as part of the Phase-1 verification harness.

---

## Section 6 — Stale Documentation Found

During this turn's re-reads against the operational sources:

- **No stale documentation detected.** All file:line anchors quoted in Section 1 were verified current within this session:
  - `src/superclaude/skills/task-builder/SKILL.md:1452-1457` — 5-field schema present and matches PRD claim that the schema lives there.
  - `src/superclaude/skills/task-builder/SKILL.md:1530` — rule #2 ("Evidence-based claims only") present at line 1530.
  - `src/superclaude/agents/rf-qa.md:144-146` — verdict definitions and "ALL gaps must be resolved before proceeding — no severity level is exempt" present.
  - `src/superclaude/agents/rf-qa.md:49-77` — Parallel Partitioning section present.
  - `src/superclaude/agents/rf-qa-qualitative.md:50-82` — Parallel Partitioning section present and substantively identical to the rf-qa version.
- **Potentially stale PRD line numbers (LOW risk)** — PRD line 499 cites `rf-qa-qualitative.md:766-775` for the anti-inflation rule, and PRD line 512 cites `rf-qa-qualitative.md:789` for the severity floor. Those line numbers were not re-verified in this turn (out of scope for the mandatory-reads list). If those anchors have drifted, FR-CONV.3 / FR-CONV.4 Negative Criteria still hold textually because they quote the *behavior* ("anti-inflation rule MUST NOT be weakened", "severity floor MUST NOT be weakened"), but the line numbers in the PRD should be revalidated by the next QA pass.
- **invariant-probe.md count discrepancy (LOW, cosmetic)** — at probe lines 43–53 the author self-corrected an UNADDRESSED total (initial "5 MEDIUMs" recount to "5 MEDIUM + 3 LOW = 8 UNADDRESSED"). This was already reconciled in the probe's "Restated summary" block; no impact on Section 2 routing.

---

## Section 7 — Summary

All 5 load-bearing task-builder invariants (self-contained-item, evidence-bound-item, persistent-`.dev/tasks/`-artifact, zero-trust QA, parallel-research) are anchored to verified operational sources at exact file:line positions and are mapped to NFR-CONV.6..10 verification fixtures plus FR Negative Criteria that act as gate-visible preservation guards. Every UNADDRESSED-MEDIUM finding from the Round-2.5 invariant probe (INV-002, INV-010, INV-012, INV-015, plus INV-019/INV-021 cross-references) is routed through at least one FR Acceptance Criterion, so a regression in any invariant manifests as a gate failure rather than silent drift. The 6 FR Negative Criteria together cover all 5 invariants — zero-trust QA appears in 4 FRs (1, 3, 4, 5, 6), evidence-bound-item in FR-CONV.1/2, parallel-research in FR-CONV.6, and self-contained-item / persistent-artifact are protected by scope-confinement (FR-CONV.2) and read-target stability (FR-CONV.3). No stale operational anchors were detected in this session; two PRD-internal line numbers (rf-qa-qualitative.md:766-775 and :789) were not in the mandatory-read set and should be revalidated by a subsequent QA pass, though the textual Negative Criteria remain behaviorally correct regardless.

---

**Status:** Complete
