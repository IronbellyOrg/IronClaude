# PRD Extraction — Task-Builder Convergence v3.9

**Status:** Complete
**Date:** 2026-05-14
**Source:** .dev/releases/current/task-builder-merge/PRD_TASK_BUILDER_CONVERGENCE.md

**Known-Drift Disclosures (verbatim from instructions):**
- PRD cites `rf-qa.md:140-142` (zero-trust verdict) — current source has it at `rf-qa.md:144-146` `[NEEDS-VERIFICATION-IN-PHASE-2]`
- PRD cites `rf-qa.md:264-287` (20-item checklist) — current source has it at `rf-qa.md:266-287` `[NEEDS-VERIFICATION-IN-PHASE-2]`
- PRD cites `rf-team-lead.md:417` (3 fix cycles per phase) — current source has it at `rf-team-lead.md:414` `[NEEDS-VERIFICATION-IN-PHASE-2]`

All other PRD-asserted `file:line` citations in sections 2–5 are flagged `[NEEDS-VERIFICATION-IN-PHASE-2]` for downstream sed-verification.

---

## Section 1 — Four Epics (PRD §21.1.1)

| Epic # | Epic Name | Features (FRs) | Stories | Priority | Phase |
|--------|-----------|----------------|---------|----------|-------|
| 1 | Structural Gate Reinforcement | FR-CONV.1, FR-CONV.2 | 2 (US-1.1, US-1.2) | P0 | Phase-1 |
| 2 | Inter-Agent Verdict Channel | FR-CONV.3, FR-CONV.4 | 2 (US-2.1, US-2.2) | P0 | Phase-1 |
| 3 | Retry & Exhaust Resilience | FR-CONV.5, FR-CONV.6 | 2 (US-3.1, US-3.2) | P0 | Phase-1 |
| 4 | Tier-History Advisory (DEFERRED) | PR-05 | 1 (US-4.1) | P2 | Phase-2 |

**Epic 1 — Structural Gate Reinforcement.** Strengthen rf-qa's task-integrity gate and the generated MDTM file's task-level readability. Includes US-1.1 (TB-Add catalogue lands in rf-qa A.10) and US-1.2 (Execution Context header lands in generated MDTM files). FR membership: FR-CONV.1 (PR-06), FR-CONV.2 (PR-01). Priority P0. Phase-1.

**Epic 2 — Inter-Agent Verdict Channel.** Make the rf-qa → rf-qa-qualitative verdict explicit and annotate adversarial findings by named axis. Includes US-2.1 (Inherited Structural Verdict block lands in rf-qa-qualitative spawn) and US-2.2 (Five Adversarial Axes overlay lands in rf-qa-qualitative output). FR membership: FR-CONV.3 (PR-04), FR-CONV.4 (PR-07). Priority P0. Phase-1.

**Epic 3 — Retry & Exhaust Resilience.** Halt oscillating retry loops on regression-or-non-shrink; surface partition-agent exhaust as a HIGH-severity synthetic finding. Includes US-3.1 (Retry monotonicity + regression halt-conditions land in existing retry loops) and US-3.2 (DNSP synthetic-finding emission contract lands in partition agents). FR membership: FR-CONV.5 (PR-02), FR-CONV.6 (PR-03 BASE). Priority P0. Phase-1.

**Epic 4 — Tier-History Advisory (DEFERRED Phase-2).** US-4.1: PR-05 advisory re-evaluation when historical-data threshold reached. Deferred per release-spec.md §2.1; trigger: `.dev/tasks/done/TASK-RF-*` ≥10 with ≥3 distinct task_types. FR membership: PR-05 only. Priority P2. Phase-2.

---

## Section 2 — Six Functional Requirements (PRD §14.1)

### FR-CONV.1: Structural Gate Additions

- **Proposal-ID:** PR-06
- **CASE:** D (conflict-register.md row PR-06)
- **Landing order:** 1st (lands first)
- **Conflicting `/sc:tasklist` mechanism:** 17-point gate bulk import
- **Protected invariant:** zero-trust QA

**Description (verbatim):** Append 8 structural checks (TB-Add-1..8) to rf-qa's task-integrity checklist (currently 9 items at `SKILL.md:898-906` `[NEEDS-VERIFICATION-IN-PHASE-2]`; `rf-qa.md:264-287` `[NEEDS-VERIFICATION-IN-PHASE-2]` (known-drift: current source has 20-item checklist at `rf-qa.md:266-287`) has the 20-item form) and mirror in the 15-item validation block (`SKILL.md:1491-1507` `[NEEDS-VERIFICATION-IN-PHASE-2]`). Per CB-3 (per-check, not bulk) from `/sc:tasklist`'s 17-point gate (checks 11/13/14/15/16/17). TB-Add-7 (Execution-Context source-areas reappear in items) absorbs PR-01 failure-mode #4 cross-validation. TB-Add-8 (per-item Context field file:line citation OR justified absence) resolves INV-015.

**TB-Add catalogue (verbatim):**
- TB-Add-1: Placeholder scan ("TBD"/"TODO"/title-only) — Hard check
- TB-Add-2: Item count bounds (≥3 / ≤40 track / ≤50 single-track) — `[ADVISORY]`-fail-until-calibrated (INV-006 LOW)
- TB-Add-3: Clarification adjacency to blocked items — Hard check
- TB-Add-4: Circular dependency detection (DAG check) — Hard check
- TB-Add-5: Granularity check (XL items have subtasks) — Hard check
- TB-Add-6: Confidence/Verification format consistency — Hard check
- TB-Add-7: Execution Context source-areas reappear in items (cross-validates PR-01) — Hard check
- TB-Add-8: Every per-item Context field referencing a code surface includes ≥1 file:line citation OR justified-absence comment — Hard check

**Acceptance Criteria:**
- ✅ **Observable behavior:** Each of TB-Add-1..8 fires a distinct, item-ID-naming error message when its condition is violated; TB-Add-2 emits an `[ADVISORY]` prefix and does NOT block the gate; TB-Add-1..7 (excluding 2) block the gate on failure.
- ✅ **Verification method:** `grep -nE "TB-Add-[1-8]" src/superclaude/agents/rf-qa.md src/superclaude/skills/task-builder/SKILL.md` must return ≥3 hits per ID (`rf-qa.md:264-287` + `SKILL.md:898-906` + `SKILL.md:1491-1507` `[NEEDS-VERIFICATION-IN-PHASE-2]`); synthetic fixture with one placeholder-titled item runs rf-qa and TB-Add-1 emits in the gate log.
- ✅ **Negative criterion (Out of scope / Must not break):** No existing rf-qa check is renamed, renumbered, or removed; the 9-item A.10 and 15-item validation existing-items are preserved verbatim; bundle-specific `/sc:tasklist` checks (phase-file naming, index references) MUST NOT appear in any TB-Add.

**Dependencies:** None (lands first).

**PRD-cited insertion points:** `SKILL.md:898-906`, `rf-qa.md:264-287`, `SKILL.md:1491-1507` (all `[NEEDS-VERIFICATION-IN-PHASE-2]`).

---

### FR-CONV.2: Execution Context Header

- **Proposal-ID:** PR-01 (revise-then-adopt)
- **CASE:** D (conflict-register.md row PR-01)
- **Landing order:** 2nd (lands second)
- **Conflicting `/sc:tasklist` mechanism:** `## Execution Context` block per FINAL-REPORT §7-R2
- **Protected invariant:** evidence-bound-item

**Description (verbatim):** Insert a task-level `## Execution Context` block in generated MDTM task files (after frontmatter, before checklist). Block contains: References (BUILD_REQUEST GOAL, WHY, related-doc IDs), Source areas (named modules/packages — **strictly NO specific file paths**), Key constraints (top 1-3 invariants from BUILD_REQUEST). Edits at `SKILL.md:228-238`, `SKILL.md:1409-1485`, `SKILL.md:719` `[NEEDS-VERIFICATION-IN-PHASE-2]`. The "no specific paths" rule is **scope-confined to the header**: per-item Context fields and research/*.md retain file:line citations to preserve the **evidence-bound-item** invariant. INV-015 is resolved by TB-Add-8.

**Acceptance Criteria:**
- ✅ **Observable behavior:** Generated MDTM task files contain a `## Execution Context` block with exactly three labeled lines (References / Source areas / Key constraints); when BUILD_REQUEST is minimal, the block degrades to References-only with WHY/source-area lines explicitly omitted (PR-01 failure-mode #2).
- ✅ **Verification method:** `grep -n "## Execution Context" <generated-task-file>` returns line N; the next 10 lines contain ≥1 of `References:` / `Source areas:` / `Key constraints:`; `grep -E "src/|/.*:[0-9]+" <header-block-range>` returns zero hits (no file paths or file:line citations within the header).
- ✅ **Negative criterion (Out of scope / Must not break):** Per-item Context fields elsewhere in the file MUST retain file:line citations OR justified-absence comments (validated by TB-Add-8); the per-item self-contained 5-field schema MUST NOT be altered or supplemented by header content.

**Dependencies:** FR-CONV.1 (TB-Add-7 cross-validation + TB-Add-8 scope-confinement test must already be live).

**PRD-cited insertion points:** `SKILL.md:228-238`, `SKILL.md:1409-1485`, `SKILL.md:719` (all `[NEEDS-VERIFICATION-IN-PHASE-2]`).

---

### FR-CONV.3: Gate Results Passthrough

- **Proposal-ID:** PR-04
- **CASE:** B (no conflict — correctly absent from conflict-register.md)
- **Landing order:** 3rd (lands third)
- **Conflicting `/sc:tasklist` mechanism:** N/A (no conflict)
- **Invariant alignment:** zero-trust QA (semantic verification still required)

**Description (verbatim):** Inject rf-qa's task-integrity verdict table verbatim into rf-qa-qualitative's spawn prompt under the heading `## Inherited Structural Verdict`, with prompt language: "PASS items machine-verified — skip structural re-checking; FAIL items machine-verified defects — flag HIGH. Focus on semantic quality." Edits at `SKILL.md:923-1000` and `rf-qa-qualitative.md:794` `[NEEDS-VERIFICATION-IN-PHASE-2]`. Operationalises an already-stated rule.

**Acceptance Criteria:**
- ✅ **Observable behavior:** rf-qa-qualitative's spawn prompt contains `## Inherited Structural Verdict` with the rf-qa table verbatim; on a fix-cycle re-run, the orchestrator re-injects the NEW verdict (INV-002); the spawn prompt's checklist enumeration is dynamic (auto-picks up TB-Add catalogue from FR-CONV.1, INV-010); rf-qa-qualitative's first run after FR-CONV.3 lands produces a `## Self-Audit` entry listing relied-on rf-qa PASS items AND ≥1 semantic check where rf-qa PASS is insufficient (INV-019).
- ✅ **Verification method:** Capture rf-qa-qualitative spawn-prompt log; `grep -n "## Inherited Structural Verdict" <spawn-log>` returns line N; the block immediately below matches rf-qa's emitted verdict table byte-for-byte; on a synthetic 2-cycle fixture, the second cycle's spawn log shows the NEW (cycle-2) verdict, not the stale (cycle-1) verdict; the same fixture's rf-qa-qualitative output contains a Self-Audit section with ≥1 entry per category above.
- ✅ **Negative criterion (Out of scope / Must not break):** rf-qa-qualitative MUST NOT mark any item VERIFIED solely from the inherited verdict — every VERIFIED item must show an independent semantic-check engagement in the Self-Audit listing; anti-inflation rule `rf-qa-qualitative.md:766-775` `[NEEDS-VERIFICATION-IN-PHASE-2]` MUST NOT be weakened, removed, or rephrased; no stale verdict from a prior fix cycle is permitted to govern current-cycle decisions.

**Dependencies:** FR-CONV.1 (TB-Add catalogue is the verdict content); FR-CONV.2 (TB-Add-7 cross-validation runs at A.10 before A.10.5 spawn).

**PRD-cited insertion points:** `SKILL.md:923-1000`, `rf-qa-qualitative.md:794` (all `[NEEDS-VERIFICATION-IN-PHASE-2]`).

---

### FR-CONV.4: Adversarial Category Naming

- **Proposal-ID:** PR-07
- **CASE:** D (conflict-register.md row PR-07)
- **Landing order:** 4th (lands fourth)
- **Conflicting `/sc:tasklist` mechanism:** 5-category adversarial agent prompt
- **Protected invariant:** zero-trust QA

**Description (verbatim):** Insert a "Five Adversarial Axes" header subsection BEFORE rf-qa-qualitative's existing 15-item task-qualitative checklist, with axis-annotation requirement on the Items Reviewed table. Five axes: drift / contradictions / omissions / weakened criteria / invented content. Edits at `rf-qa-qualitative.md:527-583`, `rf-qa-qualitative.md:675-714`, `SKILL.md:961` `[NEEDS-VERIFICATION-IN-PHASE-2]`. Overlay annotation, not replacement.

**Acceptance Criteria:**
- ✅ **Observable behavior:** rf-qa-qualitative's output renders a "Five Adversarial Axes" subsection BEFORE the 15-item checklist; the Items Reviewed table contains an `axis` column populated with one of {drift, contradictions, omissions, weakened-criteria, invented-content, none} per row; when no item captures BUILD_REQUEST.GOAL verbatim, output includes a single-line `drift-axis-inactive` annotation.
- ✅ **Verification method:** `grep -n "Five Adversarial Axes" <rf-qa-qualitative-output>` returns line N; the Items Reviewed table parses to N rows each with a non-empty `axis` value from the canonical set; synthetic fixture with no GOAL-baseline item produces `drift-axis-inactive` in the output.
- ✅ **Negative criterion (Out of scope / Must not break):** The existing 15-item task-qualitative checklist MUST NOT be removed, reordered, or replaced — axes annotate, they do not substitute; the severity floor at `rf-qa-qualitative.md:789` `[NEEDS-VERIFICATION-IN-PHASE-2]` MUST NOT be weakened; no axis may rely on a code-path change (overlay-only, per CB-3).

**Dependencies:** FR-CONV.3 (5 axes apply to items NOT covered by inherited PASS — composition is clean per INV-013).

**PRD-cited insertion points:** `rf-qa-qualitative.md:527-583`, `rf-qa-qualitative.md:675-714`, `SKILL.md:961`, `rf-qa-qualitative.md:789` (all `[NEEDS-VERIFICATION-IN-PHASE-2]`).

---

### FR-CONV.5: Retry Monotonicity Guards

- **Proposal-ID:** PR-02
- **CASE:** D (conflict-register.md row PR-02)
- **Landing order:** 5th (lands fifth)
- **Conflicting `/sc:tasklist` mechanism:** Stages 9-10 monotonicity guard + regression detection + full-set re-validation
- **Protected invariant:** zero-trust QA

**Description (verbatim):** Add two stop-conditions to EXISTING retry loops (no new loop or stage): (1) Monotonicity guard — HALT if `|gate_failures|` does not strictly shrink between cycles (`F_{n+1} >= F_n` halts); (2) Regression detection — HALT if any item that PASSed at cycle N FAILs at cycle N+1. Precedence: **Regression > monotonicity**. Halt message format: `"Regression detected on Item X.Y — previously PASS at cycle N, now FAIL. Halt overrides monotonicity check."` Edits at `SKILL.md:870`, `SKILL.md:1550`, `rf-task-builder.md:336-359`, `rf-qa.md:310-313` `[NEEDS-VERIFICATION-IN-PHASE-2]`.

**INV-012 composition criterion:** Synthetic findings emitted by FR-CONV.6 (DNSP) COUNT as failures for `|F_n|` monotonicity. BUT a synthetic finding with identical dedup-key `(assigned_files_range, escalation_ladder_exhaust_point)` across consecutive cycles is a dedup case, NOT a regression.

**Acceptance Criteria:**
- ✅ **Observable behavior:** On a fix-cycle where `F_{n+1} >= F_n`, the loop emits `[HALT-MONOTONICITY] |F|=<n>` and exits; on a cycle where Item X.Y was PASS at cycle N and is FAIL at cycle N+1, the loop emits the verbatim regression halt message and exits BEFORE the monotonicity check; on a cycle where a synthetic-dnsp finding with identical dedup-key appears in both N and N+1, no halt fires (dedup recognized).
- ✅ **Verification method:** Synthetic 3-cycle fixture with `F_1=5, F_2=5, F_3=5` halts at cycle 2 with `[HALT-MONOTONICITY]`; synthetic 2-cycle fixture with Item 3.2 PASS@1/FAIL@2 halts at cycle 2 with the regression message; synthetic 2-cycle fixture with one synthetic-dnsp finding (same `assigned_files_range`+`escalation_ladder_exhaust_point` in both cycles) proceeds to cycle 3 without halting; `grep -n "Retry Monotonicity Protocol" src/superclaude/skills/task-builder/SKILL.md` returns ≥2 lines (`SKILL.md:870` + `SKILL.md:1550`).
- ✅ **Negative criterion (Out of scope / Must not break):** Legitimate slow-cycle correction MUST NOT be halted — any cycle where `|F|` strictly shrinks (even by 1) continues; the four independent retry counters MUST NOT be collapsed into a shared monotonicity state; no halt-on-slow-convergence threshold (e.g., `F_{n+1} = F_n - 1`) is permitted (X-003 REJECTED).

**Dependencies:** FR-CONV.1 (gate produces `F_n` count); FR-CONV.6 (synthetic-dnsp findings consumed by monotonicity per INV-012).

**PRD-cited insertion points:** `SKILL.md:870`, `SKILL.md:1550`, `rf-task-builder.md:336-359`, `rf-qa.md:310-313` (all `[NEEDS-VERIFICATION-IN-PHASE-2]`).

---

### FR-CONV.6: DNSP Synthetic Finding

- **Proposal-ID:** PR-03 (BASE)
- **CASE:** B (no conflict — correctly absent from conflict-register.md)
- **Landing order:** 6th (lands sixth)
- **Conflicting `/sc:tasklist` mechanism:** N/A (no conflict)
- **Invariant alignment:** zero-trust QA + evidence-bound-item + parallel-research

**Description (verbatim):** After the entire escalation ladder exhausts on a partition agent (rf-analyst or rf-qa partition), emit a synthetic HIGH-severity finding rather than silently aborting the gate. **Emission contract**: `severity: HIGH; source: "synthetic-dnsp"; affected_range: <agent's assigned_files slice>; evidence: <spawn-log path, OR stub citing log absence>; recommendation: "Manual review required — partition agent failed twice"`. **Dedup key**: `(assigned_files_range, escalation_ladder_exhaust_point)`. **All-agents-fail guard preserved**: if zero partition agents succeeded, escalate normally (`rf-team-lead.md:417` `[NEEDS-VERIFICATION-IN-PHASE-2]` — known-drift: current source has "3 fix cycles per phase" at `rf-team-lead.md:414` — 3 fix cycles per phase) and DO NOT emit synthetic. Edits at `SKILL.md:574-654`, `SKILL.md:872-916`, `rf-analyst.md:60-69`, `rf-qa.md:70-77`, `rf-qa-qualitative.md:72-78` `[NEEDS-VERIFICATION-IN-PHASE-2]`.

**Acceptance Criteria:**
- ✅ **Observable behavior:** When a partition agent's escalation ladder exhausts, the agent's output stream emits a JSON-or-block finding with all 5 fixed fields; two synthetic findings with identical dedup-key collapse with a `found 2 times` note; when zero partitions succeeded, no synthetic emits (existing all-agents-fail escalation runs).
- ✅ **Verification method:** Inject a partition-agent fixture that times out twice; verify synthetic-dnsp finding appears in the gate output with all 5 required fields; inject two identical exhaust events; verify only one finding emits with `found N times`; inject all-agents-fail fixture; verify zero synthetic emits and existing escalation path activates; `grep -n "synthetic-dnsp" src/superclaude/agents/rf-analyst.md src/superclaude/agents/rf-qa.md` returns ≥1 hit per file at the partition-protocol section.
- ✅ **Negative criterion (Out of scope / Must not break):** Synthetic-dnsp MUST NOT emit before the escalation ladder exhausts — proposal line 35 all-agents-fail guard runs first; the existing escalation behavior at `rf-team-lead.md:417` `[NEEDS-VERIFICATION-IN-PHASE-2]` (3 fix cycles per phase) MUST NOT be replaced or short-circuited; synthetic findings MUST NOT mask real findings — HIGH severity ensures gate-level visibility; the dedup-key collapse MUST NOT cross-cycle (PR-02 monotonicity treats dedup as not-regression per INV-012).

**Dependencies:** FR-CONV.5 (PR-02 monotonicity consumes synthetic-dnsp per INV-012 dedup-key rule).

**PRD-cited insertion points:** `SKILL.md:574-654`, `SKILL.md:872-916`, `rf-analyst.md:60-69`, `rf-qa.md:70-77`, `rf-qa-qualitative.md:72-78`, `rf-team-lead.md:417` (all `[NEEDS-VERIFICATION-IN-PHASE-2]`; known-drift on rf-team-lead.md:417 → 414).

---

## Section 3 — Ten Non-Functional Requirements (PRD §14.2)

| ID | Requirement | Target | Measurement |
|----|-------------|--------|-------------|
| NFR-CONV.1 | Determinism scope — gate outputs deterministic | Gate-results structure (TB-Add-* PASS/FAIL, synthetic-dnsp 5 fields, dedup-key) MUST be deterministic for fixed BUILD_REQUEST + fixed source tree | Re-run task-builder on identical BUILD_REQUEST twice; diff the rf-qa A.10 verdict table; structural fields must be byte-identical |
| NFR-CONV.2 | Determinism scope — research-driven prose excluded | Per-item Context prose and rf-qa-qualitative semantic-check prose remain LLM-research-driven; NOT required to be byte-deterministic | Diff prose between two runs; non-byte-equality acceptable; structural fields (axis annotations, finding-counts) must remain byte-equal |
| NFR-CONV.3 | Hidden-input guard (per FR §6.2 F4) | Task-builder MUST NOT read any input outside BUILD_REQUEST + source-tree that could modify behavior; PR-05 advisory mechanism REJECTED for Phase-1 | Fixture-populated `.dev/tasks/done/` MUST produce byte-identical structural output to empty `.dev/tasks/done/` |
| NFR-CONV.4 | Token ceiling | ≤10% token-cost increase over pre-merge task-builder baseline per equivalent BUILD_REQUEST | Sample 5 representative BUILD_REQUESTs; record pre-merge and post-merge token counts; ratio ≤1.10 |
| NFR-CONV.5 | Wall-clock | No new external dependencies; gate additions are local checks; no synchronous network calls added | Inspect rf-qa.md and SKILL.md diffs: only existing tools (Read, Grep, Glob, Bash) permitted |
| NFR-CONV.6 | **Invariant preservation — self-contained-item** (protected invariant: **self-contained-item**) | 5-field per-item schema MUST remain operational across all 8 TB-Add checks and the Execution Context header | Synthetic fixture with all 5 fields passes all TB-Add checks; same with one field stripped fails TB-Add-1 — fails closed |
| NFR-CONV.7 | **Invariant preservation — evidence-bound-item** (protected invariant: **evidence-bound-item**) | Every per-item Context referencing code surface MUST retain file:line citation OR justified-absence (TB-Add-8 enforces) | Synthetic fixture with bare `Context: src/foo` (no `:N`) fails TB-Add-8; same with `Context: src/foo:42` passes; same with `Context: <none — pure refactor> [justified-absence]` passes |
| NFR-CONV.8 | **Invariant preservation — persistent-`.dev/tasks/`-artifact** (protected invariant: **persistent-`.dev/tasks/`-artifact**) | Research/qa persistence in `.dev/tasks/<task-id>/` MUST remain unchanged | Diff `.dev/tasks/` directory layout pre- and post-merge; no path, no naming pattern altered |
| NFR-CONV.9 | **Invariant preservation — zero-trust QA** (protected invariant: **zero-trust QA**) | "Any gap regardless of severity = FAIL" stance (`rf-qa.md:140-142` `[NEEDS-VERIFICATION-IN-PHASE-2]` — known-drift: current source at `rf-qa.md:144-146`) MUST remain operative; no TB-Add or PR-04 mechanism weakens it | Synthetic fixture with 1 LOW finding fails the gate; FR-CONV.3 inherited verdict does NOT mark items VERIFIED in absence of independent semantic check |
| NFR-CONV.10 | **Invariant preservation — parallel-research** (protected invariant: **parallel-research**) | rf-analyst / rf-qa partition cohort MUST remain parallel; DNSP fires within-agent-instance (INV-021) | Spawn-log inspection: N partition agents run concurrently; on one agent's escalation exhaust, N-1 continue to completion before DNSP synthesises a finding |

---

## Section 4 — Five Load-Bearing Invariants (PRD §14.3 + release-spec.md §1.0)

1. **self-contained-item** — Mechanism: Every checklist item carries the five fields {Description, Context, Acceptance, Confidence, Verification} sufficient to execute it without reading other items.
   - **PRD-cited operational source:** `SKILL.md:1452-1457` `[NEEDS-VERIFICATION-IN-PHASE-2]`
   - **Current-source value:** unverified; phase-2 sed-verification required.

2. **evidence-bound-item** — Mechanism: Every per-item Context field referencing a code surface includes a `file:line` citation OR a justified-absence comment.
   - **PRD-cited operational source:** `SKILL.md:1530 rule #2` `[NEEDS-VERIFICATION-IN-PHASE-2]`
   - **Current-source value:** unverified; phase-2 sed-verification required.

3. **persistent-`.dev/tasks/`-artifact** — Mechanism: Research and QA outputs persist to `.dev/tasks/<task-id>/` with stable naming.
   - **PRD-cited operational source:** §11 OPEN-INV-018 (release-spec.md §1.0); no specific code line — convention-bound.
   - **Current-source value:** convention; not line-citable.

4. **zero-trust QA** — Mechanism: "Any gap regardless of severity = FAIL" stance at the task-integrity gate.
   - **PRD-cited operational source:** `rf-qa.md:140-142` `[NEEDS-VERIFICATION-IN-PHASE-2]`
   - **Current-source value (known-drift):** `rf-qa.md:144-146` (zero-trust verdict; per instructions).

5. **parallel-research** — Mechanism: rf-analyst and rf-qa partition cohorts run concurrently; per-partition failures do not serialize the cohort.
   - **PRD-cited operational source:** NFR-CONV.10; INV-021 (PRD §14.2; no single line).
   - **Current-source value:** verified by spawn-log inspection; not line-citable.

---

## Section 5 — G6 Four-Case Conflict Rule (PRD §14.3)

| CASE | Definition | Disposition rule | Conflict-register row required? |
|------|-----------|-----------------|--------------------------------|
| **CASE-A** | `/sc:tasklist` has a mechanism; task-builder has a conflicting mechanism. | Explicit decision; one of {ADOPT-ADAPTED, REJECT}. | **YES** — row naming the conflicting mechanism and the protected invariant. |
| **CASE-B** | `/sc:tasklist` has a mechanism; task-builder is silent (no conflict). | ADOPT (or ADOPT-ADAPTED). | **NO** — no conflict-register row required. |
| **CASE-C** | `/sc:tasklist` is silent; task-builder has a mechanism. | Keep task-builder behavior; nothing to import. | **NO** — nothing to register. |
| **CASE-D** | `/sc:tasklist` has a mechanism; task-builder has a *related but non-conflicting* mechanism. | ADOPT-ADAPTED with scope-confinement or per-check classification (CB-3). | **YES** — row required. |

**Portfolio distribution (verbatim PRD):** PR-01 D, PR-02 D, PR-03 B, PR-04 B, PR-05 D (deferred), PR-06 D, PR-07 D. Conflict-register has exactly 5 rows (one per CASE-D proposal); CASE-B proposals correctly omitted.

---

## Section 6 — Ten K-Risks (PRD §20.1 + §20.2)

| ID | Risk | Probability | Impact | Mitigation | Contingency |
|----|------|-------------|--------|------------|-------------|
| K-001 | TB-Add false positives waste fix-cycles | low | low | Each TB-Add cites source-check-ID for traceability; TB-Add-2 `[ADVISORY]`; FR-CONV.1 negative criterion forbids removing items, but each TB-Add can be individually disabled by reverting its append line | Disable specific TB-Add line; document false-positive class |
| K-002 | Execution Context header drift (header says X, items say Y) | low | low | TB-Add-7 cross-validates header source-areas reappear in items; on drift, gate fails and rf-task-builder retries; header is optional (degrades to References-only) | Header optional fallback |
| K-003 | PR-04 passthrough causes inflation despite anti-inflation rule | low | med | INV-019 acceptance criterion mandates Self-Audit listing on first run; X-002 flagged as audit target — first 5 rf-qa-qualitative runs after FR-CONV.3 lands MUST be audited | If any audit shows inflation, disable passthrough and fall back to current behavior |
| K-004 | 5-axis annotation ambiguity over-flags items | low | low | Axes are annotation-only; existing 15-item checklist still runs; severity floor preserved; `drift-axis-inactive` annotation when GOAL-baseline missing | Audit axis distribution; tune annotation rules |
| K-005 | Retry monotonicity halts legitimate slow-cycle correction | low | low | Strict-shrink threshold (`F_{n+1} >= F_n`); any forward motion permits continuation; X-003 "halt on slow convergence" REJECTED | Rollback by disabling guards individually |
| K-006 | Synthetic-dnsp findings mask real issues | low | low | HIGH severity ensures gate-level visibility; all-agents-fail guard preserves existing escalation path; dedup-key prevents over-emission while preserving the failure signal | Inspect synthetic-dnsp emission count metric weekly |
| K-007 | PR-04 + PR-06 sequencing inversion (PR-04 lands before PR-06) | low | med | Sequencing rule PR-06 → PR-04 enforced in §4.6; PR-04 prompt uses dynamic checklist enumeration so it richens automatically when TB-Add items go live (INV-010 mitigation) | Re-merge in correct order; verify INV-010 |
| K-008 | INV-018 `.dev/tasks/` directory structure changes invalidate all 7 proposals | low | high | Portfolio-wide note; SP-33 stability commitment; if directory structure changes, re-integrate all 7 proposals at the new layout | Re-integration commit covering all six FRs |
| K-009 | sync-discipline (A-001) violated: `.claude/` edited directly without `make verify-sync` | low | med | All FRs name `src/superclaude/` paths exclusively; CLAUDE.md mandates the sync workflow; `make verify-sync` MUST pass before commit | Revert `.claude/` direct edit; re-run from `src/superclaude/` |
| K-010 | Token ceiling NFR-CONV.4 exceeded by >10% | low | low | Empirical measurement post-merge; if exceeded, profile per-FR contribution and revise FR-CONV.3 Inherited Structural Verdict block (verdict table can be summarised rather than verbatim) | FR-CONV.3 verdict-table summarisation |

---

## Section 7 — Six Open Questions (PRD §13)

### OPEN-PR05
- **Question:** When does `.dev/tasks/done/` reach the ≥10-tasks-of-≥3-task_types threshold to re-evaluate PR-05?
- **Impact:** Determines Phase-2 release timing.
- **Resolution target:** Re-check at each major release; document in `KNOWLEDGE.md`.

### OPEN-INV-006
- **Question:** Empirical calibration of TB-Add-2 item-count bounds (≥3 / ≤40 track / ≤50 single-track).
- **Impact:** TB-Add-2 stays `[ADVISORY]` until calibrated.
- **Resolution target:** Phase-2 with PR-05.

### OPEN-INV-017
- **Question:** Historical-file staleness check for PR-05 advisory citations.
- **Impact:** Academic given PR-05 Phase-2 deferral.
- **Resolution target:** Resolve when PR-05 re-evaluated.

### OPEN-INV-018
- **Question:** If `.dev/tasks/` directory layout changes, all 7 proposals require re-integration.
- **Impact:** Portfolio-wide blast radius.
- **Resolution target:** Document layout-change contract; re-integrate on demand.

### OPEN-X-002
- **Question:** PR-04 anti-inflation operational test — "reliance ≠ verification" distinction empirically observable, not structurally provable.
- **Impact:** First 5 rf-qa-qualitative runs after FR-CONV.3 lands MUST be audited (K-003).
- **Resolution target:** Post-merge audit per release-spec.md §8.3 row 4.

### OPEN-TOKEN
- **Question:** NFR-CONV.4 token-ceiling empirical measurement.
- **Impact:** Confirms ≤10% increase target.
- **Resolution target:** Post-merge measurement on 5 representative BUILD_REQUESTs.

---

## Section 8 — Five PRD §25 Data-Model Schemas (verbatim)

### 25.1 Execution Context Header (FR-CONV.2)

```yaml
"## Execution Context":
  References:        # list of BUILD_REQUEST refs (GOAL, WHY, related-doc IDs)
    - "R-###: <ref-line>"
  Source areas:      # list of named modules/packages — NEVER specific file paths
    - "<package-or-module-name>"
  Key constraints:   # top 1-3 invariants from BUILD_REQUEST
    - "<invariant statement>"
```

**Key constraints (from PRD body):**
- References: BUILD_REQUEST GOAL, WHY, related-doc IDs.
- Source areas: named modules/packages — **strictly NO specific file paths**.
- Key constraints: top 1-3 invariants from BUILD_REQUEST.

### 25.2 Inherited Structural Verdict Block (FR-CONV.3)

```yaml
"## Inherited Structural Verdict":
  rf_qa_table_verbatim: <copy of rf-qa task-integrity table at spawn time>
  prompt_directive: "PASS items machine-verified — skip structural re-checking; FAIL items machine-verified defects — flag HIGH. Focus on semantic quality."
  reinjection_rule: "On fix-cycle re-run, orchestrator MUST re-inject the NEW verdict; stale verdicts forbidden."
```

### 25.3 Synthetic DNSP Finding (FR-CONV.6)

```yaml
synthetic_dnsp_finding:
  severity: HIGH                                # fixed
  source: "synthetic-dnsp"                      # fixed
  affected_range: "<agent's assigned_files slice>"
  evidence: "<spawn-log path, OR stub citing log absence>"
  recommendation: "Manual review required — partition agent failed twice"
  dedup_key: "(assigned_files_range, escalation_ladder_exhaust_point)"
  found_n_times: <int, default 1>               # increments on dedup collapse
```

### 25.4 Per-Item Checklist Schema (referenced by NFR-CONV.6)

```yaml
per_item_schema:
  Description: "<one-line task-item action statement>"
  Context: "<file:line citation OR justified-absence comment>"     # TB-Add-8 enforced
  Acceptance: "<observable success condition>"
  Confidence: "<HIGH|MEDIUM|LOW> — with one-line rationale"
  Verification: "<command, file inspection, or test to confirm Acceptance>"
```

### 25.5 Phase Contract: rf-qa → rf-qa-qualitative

```yaml
phase_contract:
  producer: rf-qa
  consumer: rf-qa-qualitative
  artifact: "## Inherited Structural Verdict block in spawn prompt"
  schema_version: "1.0.0"
  delivery_semantics: "at-most-once-per-cycle"
  freshness_rule: "On fix-cycle re-run, orchestrator re-injects NEW verdict; stale verdicts forbidden (INV-002)"
  enumeration_rule: "Checklist enumeration is dynamic — auto-picks up TB-Add catalogue from FR-CONV.1 (INV-010)"
  consumer_obligation: "Self-Audit listing relied-on PASS items AND ≥1 semantic check (INV-019)"
  anti_inflation: "Mechanical re-checking SKIPPED for PASS items; semantic verification STILL REQUIRED (rf-qa-qualitative.md:766-775)"
  failure_mode: "If rf-qa fails to emit a verdict, rf-qa-qualitative MUST NOT spawn — gate halts at A.10 before A.10.5"
```

---

## Extraction Complete

All 8 canonical sections extracted from PRD_TASK_BUILDER_CONVERGENCE.md (lines 1–1057). All PRD-asserted `file:line` citations in sections 2–5 carry `[NEEDS-VERIFICATION-IN-PHASE-2]` markers for downstream FR-investigation agent sed-verification. Three known-drift citations explicitly flagged: `rf-qa.md:140-142` → 144-146, `rf-qa.md:264-287` → 266-287, `rf-team-lead.md:417` → 414.

