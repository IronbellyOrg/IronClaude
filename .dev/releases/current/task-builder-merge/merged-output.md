<!-- Provenance: This document was produced by /sc:adversarial Mode A pipeline -->
<!-- Base: PR-03 (CASE-B, combined score 0.959) -->
<!-- Merge date: 2026-05-14 -->
<!-- Type: consolidated portfolio document (not single-proposal replacement) -->

# task-builder-merge — Consolidated Portfolio (Phase-1 Adoption Plan)

## Portfolio Overview

This document is the merged output of the `/sc:adversarial` Mode A pipeline applied to 7 distinct proposals (PR-01 through PR-07) for importing qualities of `/sc:tasklist` into the `task-builder` skill. The proposals were evaluated together as a portfolio, not as competing variants.

**Convergence**: 0.88 (threshold 0.80) — CONVERGED after Round 2 + invariant probe.

**Verdict distribution**: ADOPT 5 + REVISE 2 + REJECT 0.

**Base proposal**: PR-03 (CASE-B, score 0.959) — selected by combined hybrid scoring (quant 0.50 + qual 0.50) with Level-1 tiebreaker (debate performance). PR-03 wins by paradigm-neutral external evidence (P3 39/50 in FINAL-REPORT), CASE-B no-conflict classification, and dual-invariant reinforcement.

**Five task-builder invariants** (load-bearing across portfolio — no adopted change weakens any):
1. self-contained-item (5-field schema per checklist item)
2. evidence-bound-item (file:line citation mandatory)
3. persistent-.dev/tasks/-artifact (research/qa/ persist)
4. zero-trust QA (any gap = FAIL)
5. parallel-research (rf-analyst / rf-qa partitioning)

---

## Phase-1 Adopted Entries (in landing order)

### 1. PR-06 — Structural Gate Additions (lands first)

<!-- Source: PR-06 (CASE-D, score 0.963), absorbing PR-01 failure-mode #4 as TB-Add-7 -->

**Mechanism**: Import 7 specific structural checks from sc:tasklist's 17-point gate (per CB-3 per-check classification, not bulk import) into rf-qa's task-integrity checklist.

**Edits**:
- `src/superclaude/agents/rf-qa.md:264-287` — add TB-Add-1 through TB-Add-7
- `src/superclaude/skills/task-builder/SKILL.md:898-906` — mirror in A.10 9-item checklist
- `src/superclaude/skills/task-builder/SKILL.md:1491-1507` — mirror in 15-item validation

**TB-Add catalogue**:
| ID | Check | Source | Status |
|----|-------|--------|--------|
| TB-Add-1 | Placeholder scan (no "TBD"/"TODO"/title-only) | sc:tasklist check 11 | Hard check |
| TB-Add-2 | Item count bounds (≥3 / ≤40 track / ≤50 single-track) | sc:tasklist check 13 | **ADVISORY-fail until calibrated** (INV-006) |
| TB-Add-3 | Clarification adjacency to blocked items | sc:tasklist check 14 | Hard check |
| TB-Add-4 | Circular dependency detection (DAG check) | sc:tasklist check 15 | Hard check |
| TB-Add-5 | Granularity check (XL items have subtasks) | sc:tasklist check 16 | Hard check |
| TB-Add-6 | Confidence/Verification format consistency | sc:tasklist check 17 | Hard check |
| TB-Add-7 | Execution Context source-areas reappear in items | (absorbed from PR-01 failure-mode #4) | Hard check (validates PR-01) |

**Why first**: Establishes the structural-check catalogue that PR-01 (TB-Add-7), PR-04 (inherited verdict richens), and PR-07 (axis annotation overlay) all depend on.

**Risk**: Low — additive, never subtractive; TB-Add-2 ADVISORY-fail mitigates calibration uncertainty.

**Invariants strengthened**: zero-trust QA (additive checks); self-contained-item (TB-Add-1 enforces 5-field schema).

### 2. PR-01 — Execution Context Header (lands second; REVISE-then-adopt)

<!-- Source: PR-01 (CASE-D, score 0.912, REVISE), cross-validation absorbed into PR-06 TB-Add-7; INV-015 acceptance criterion added as TB-Add-8 -->

**Mechanism**: Add a task-level `## Execution Context` block (References + Source areas + Key constraints) to generated MDTM task files. Strictly NO specific file paths in the block — only named modules/packages. Per-item Context fields and research/*.md retain file:line citations.

**Edits**:
- `src/superclaude/skills/task-builder/SKILL.md:228-238` — template-selection note
- `src/superclaude/skills/task-builder/SKILL.md:1409-1485` — output schema
- `src/superclaude/skills/task-builder/SKILL.md:719` — rf-task-builder spawning instruction

**REVISE acceptance criterion (resolves INV-015)**: Add TB-Add-8 to PR-06 catalogue — "Every per-item Context field that references a code surface includes at least one file:line citation OR a justified absence comment." This is the structural test that proves the scope-confinement rule is operational.

**Cross-validation (TB-Add-7)**: rf-qa task-integrity verifies Execution Context source-areas re-appear in per-item Context fields (prevents header drift).

**Risk**: Low — header is optional; degrades to References-only when BUILD_REQUEST minimal.

**Invariants protected**: evidence-bound-item — scope-confined to header only; per-item evidence preserved.

### 3. PR-04 — Gate Results Passthrough (lands third)

<!-- Source: PR-04 (CASE-B, score 0.934), with INV-002/INV-010/INV-019 acceptance criteria appended -->

**Mechanism**: rf-qa's task-integrity verdict (PASS/FAIL per item) is injected verbatim into rf-qa-qualitative's spawn prompt as `## Inherited Structural Verdict`. Instruction: "PASS items machine-verified — skip structural re-checking; FAIL items machine-verified defects — flag HIGH. Focus on semantic quality."

**Edits**:
- `src/superclaude/skills/task-builder/SKILL.md:923-1000` — A.10.5 spawn description
- `src/superclaude/agents/rf-qa-qualitative.md:794` — operationalises existing rule

**Three acceptance criteria**:
1. **INV-002 (verdict re-injection)**: When rf-qa re-runs after a fix cycle, orchestrator MUST re-inject the new verdict; rf-qa-qualitative MUST NOT use a stale verdict from a prior cycle.
2. **INV-010 (sequencing with PR-06)**: PR-04 prompt template uses dynamic checklist enumeration that auto-picks up PR-06's TB-Add items. No manual edit when TB-Adds go live.
3. **INV-019 (anti-inflation)**: rf-qa-qualitative's first run after PR-04 lands must produce a Self-Audit entry listing relied-on rf-qa PASS items AND include at least one semantic check where rf-qa PASS is insufficient (e.g., section-content-quality vs. section-numbering).

**Risk**: Low — anti-inflation rule strengthened, not weakened.

**Invariants protected**: zero-trust QA — semantic verification required; only mechanical re-verification skipped.

### 4. PR-07 — Adversarial Category Naming (lands fourth)

<!-- Source: PR-07 (CASE-D, score 0.913), with drift-baseline operationalisation -->

**Mechanism**: Insert "Five Adversarial Axes" header subsection BEFORE rf-qa-qualitative's existing 15-item task-qualitative checklist + axis annotation requirement on Items Reviewed table.

**Five axes**:
- **Drift** — paraphrasing weakens BUILD_REQUEST.GOAL
- **Contradictions** — internal inconsistency between items or fields
- **Omissions** — BUILD_REQUEST QA/Validation/Testing requirements missing from checklist
- **Weakened criteria** — acceptance criteria phrased more permissively than warranted
- **Invented content** — references to files/modules NOT in research/*.md evidence

**Edits**:
- `src/superclaude/agents/rf-qa-qualitative.md:527-583` — axis subsection
- `src/superclaude/agents/rf-qa-qualitative.md:675-714` — output template axis annotation
- `src/superclaude/skills/task-builder/SKILL.md:961` — reference the new 5-axis lens

**Acceptance criterion (PR-07 failure-mode #3 drift baseline)**: rf-qa-qualitative's task-qualitative checklist MUST contain an item that captures BUILD_REQUEST.GOAL verbatim BEFORE the drift check is applied. If no such item exists, drift axis is INACTIVE for this task; surface as `drift-axis-inactive` annotation.

**Risk**: Low — naming-only overlay; no code-path changes.

**Invariants strengthened**: zero-trust QA — adversarial stance sharpened.

### 5. PR-02 — Retry Monotonicity Guards (lands fifth)

<!-- Source: PR-02 (CASE-D, score 0.965, highest), with INV-012 PR-03 composition acceptance criterion -->

**Mechanism**: Add two stop conditions to EXISTING retry loops (no new loop or stage):
1. **Monotonicity guard**: HALT if |gate_failures| does not strictly shrink between cycles
2. **Regression detection**: HALT if any item that PASSed at cycle N FAILs at cycle N+1

**Precedence (from Round-2 spec)**: Regression > monotonicity. Halt message: "Regression detected on Item X.Y — previously PASS at cycle N, now FAIL. Halt overrides monotonicity check."

**Edits**:
- `src/superclaude/skills/task-builder/SKILL.md:870, 1550` — new "Retry Monotonicity Protocol" subsection
- `src/superclaude/agents/rf-task-builder.md:336-359` — per-gate fix-cycle integration
- `src/superclaude/agents/rf-qa.md:310-313` — 3-fix-cycle integration

**Acceptance criterion (INV-012 — PR-02 + PR-03 composition)**: Synthetic findings from PR-03 DNSP COUNT as failures for |F_n| monotonicity, BUT a synthetic for the same `(assigned_files_range, escalation_ladder_exhaust_point)` key across consecutive cycles is a dedup case, NOT a regression. Explicit specification in Retry Monotonicity Protocol subsection.

**Risk**: Low — conservative thresholds preserve legitimate slow-cycle correction; independent counters preserved.

**Invariants strengthened**: zero-trust QA — strictest possible halt-conditions.

### 6. PR-03 — DNSP Synthetic Finding (BASE; lands sixth)

<!-- Source: PR-03 (CASE-B, score 0.959, BASE), with Round-2 dedup-key specification -->

**Mechanism**: After the entire escalation ladder exhausts on a partition agent (rf-analyst or rf-qa partition), emit a synthetic HIGH-severity finding rather than silently aborting the gate.

**Emission contract**:
- `severity: HIGH`
- `source: "synthetic-dnsp"`
- `affected_range`: agent's `assigned_files` slice
- `evidence`: spawn-log path (or stub citing log absence per failure-mode #3)
- `recommendation`: "Manual review required — partition agent failed twice"

**Dedup key (Round-2 specification)**: `(assigned_files_range, escalation_ladder_exhaust_point)`. Two synthetic findings with identical key collapse into one with "found N times" note. Composes cleanly with PR-02 monotonicity (synthetic counts as failure; dedup is not regression).

**All-agents-fail guard preserved**: If zero partition agents succeeded, escalate normally (existing behavior — Bucket D rf-team-lead.md:417 3 fix cycles per phase).

**Edits**:
- `src/superclaude/skills/task-builder/SKILL.md:574-654` — A.8 research gate
- `src/superclaude/skills/task-builder/SKILL.md:872-916` — A.10 task integrity
- `src/superclaude/agents/rf-analyst.md:60-69` — partition protocol
- `src/superclaude/agents/rf-qa.md:70-77` — partition protocol
- `src/superclaude/agents/rf-qa-qualitative.md:72-78` — partition protocol (if applicable)

**Why selected as BASE**: P3 39/50 — the only proposal across 5 RF→SC ports to win without revision. Paradigm-neutral evidence. CASE-B no-conflict. Dual-invariant reinforcement (zero-trust QA + evidence-bound-item).

**Risk**: Low — DNSP fires only after escalation exhausts; all-agents-fail guard preserves existing escalation.

**Invariants strengthened**: zero-trust QA (visible gap > silent abort); evidence-bound-item (synthetic finding cites range + log); parallel-research (N-1 partitions complete).

---

## Phase-2 Deferred Entries

### PR-05 — Tier History Advisory

<!-- Source: PR-05 (CASE-D, score 0.862, REVISE-deferral) — Phase-2 candidate -->

**Disposition**: NOT adopted in Phase-1.

**Re-evaluation trigger**: `.dev/tasks/done/` accumulates ≥10 completed tasks of ≥3 distinct task_types.

**Rationale**:
- Author-acknowledged Phase-2 framing (proposal lines 12, 61).
- INV-003 MEDIUM concern: "Disclaimer presence ≠ disclaimer obeyed" — advisory operational obedience cannot be structurally enforced in agent-exploratory paradigm.
- Lowest combined score in portfolio (0.862).
- "LOW immediate value until 10+ done tasks exist."

**Latent value**: cross-task tier consistency once data volume accumulates. Mechanism (frontmatter-only reading) avoids privacy/leakage risk. Mitigations stacked (advisory-only label, rf-qa task-integrity disclaimer check, min-2 historical threshold).

**Action when triggered**: Re-run adversarial scoring on PR-05 with the new data context.

---

## Cross-Cutting Recommendations

These apply to the portfolio as a whole, regardless of individual change adoption:

### 1. Sequencing Enforcement

Land in the order: **PR-06 → PR-01 → PR-04 → PR-07 → PR-02 → PR-03**.

PR-05 lands separately when Phase-2 trigger fires.

### 2. Sync-Discipline (A-001)

All 6 adopted changes edit files in `src/superclaude/`. After integration:
1. Run `make sync-dev`
2. Run `make verify-sync`
3. Commit only after verify-sync passes

### 3. Zero-Trust Governance (A-002)

Every adopted gate-touching change (PR-02, PR-03, PR-04, PR-06, PR-07) is additive. No existing check removed or weakened. Existing rf-qa "any gap regardless of severity = FAIL" stance (Bucket D rf-qa.md:140-142) governs all five.

### 4. CASE-Label Adaptability (A-003)

The portfolio explicitly demonstrates that CASE classifications are not infinitely binding. PR-05's CASE-D classification stands, but the Phase-2 deferral shows that downstream evidence (Phase-2 framing acknowledged by author + INV-003 MEDIUM invariant concern) can re-prioritize within the portfolio plan.

### 5. End-to-End Test Gate

After all 6 changes land, run a fresh task-builder pipeline end-to-end against a synthetic BUILD_REQUEST that exercises all 5 invariants. Verify:

| Test | Validates | Invariant |
|------|-----------|-----------|
| Per-item Context fields retain file:line citations | TB-Add-8 / INV-015 | evidence-bound-item |
| Inherited verdict re-injected on fix-cycle re-runs | PR-04 / INV-002 | zero-trust QA |
| TB-Add-7 cross-validates PR-01 header | PR-01 + PR-06 / INV-011 | evidence-bound-item |
| PR-02 monotonicity correctly classifies PR-03 synthetics | PR-02 + PR-03 / INV-012 | zero-trust QA |
| PR-07 drift axis INACTIVE when no GOAL-baseline item | PR-07 / failure-mode #3 | zero-trust QA |
| Partition-failure emits synthetic-dnsp finding | PR-03 / U-003 | parallel-research + zero-trust QA |

### 6. Provenance Annotations

Per-section attribution required in all derived artifacts (rf-qa output, gate logs, retry logs). Each TB-Add cites its source check ID. Synthetic findings carry `source: "synthetic-dnsp"`. Inherited Structural Verdict cites rf-qa run timestamp.

### 7. Invariant Probe MEDIUMs

5 MEDIUM invariant concerns surfaced in `adversarial/invariant-probe.md` are ALL addressed via per-change acceptance criteria. Summary:

| INV | Concern | Owner | Resolution |
|-----|---------|-------|------------|
| INV-002 | PR-04 verdict re-injection | PR-04 acceptance criterion | Explicit re-injection mandate on fix-cycle re-runs |
| INV-003 | PR-05 advisory obedience | PR-05 disposition | Phase-2 deferral (operationally unprovable) |
| INV-010 | PR-04 + PR-06 sequencing | Sequencing order + PR-04 dynamic enumeration | PR-06 lands first; PR-04 uses dynamic checklist |
| INV-012 | PR-02 + PR-03 composition | PR-02 acceptance criterion | Synthetic counts as failure; dedup key prevents false regression |
| INV-015 | PR-01 scope-confinement test | TB-Add-8 | New structural check enforces scope-confinement |

### 8. Documentation Updates

Update Bucket C digest with per-check mapping table once PR-06 integration completes. Update `KNOWLEDGE.md` with the merge sequencing rationale.

---

## Unresolved Tensions

These items remain at convergence ceiling but do not block adoption:

### S-003 / S-005 — cosmetic differences (failure-mode count, length)

Low-severity surface differences between proposals. No merge action required.

### X-002 — PR-04 anti-inflation operational test

PR-04 commits to specific prompt language but the operational distinction between "skip mechanical re-verification" and "rely on another agent's verdict" is subtle. INV-019 acceptance criterion (Self-Audit listing) is the structural mitigation, but proving the distinction holds in production requires empirical observation post-landing.

**Resolution path**: After PR-04 lands, audit the first 5 rf-qa-qualitative runs for Self-Audit completeness. If any run shows MET items derived solely from inherited verdict without independent semantic engagement, fail the gate and re-tune the prompt.

### LOW Invariants (INV-006, INV-017, INV-018)

- INV-006: PR-06 TB-Add-2 bounds calibration — already ADVISORY-fail-until-calibrated
- INV-017: PR-05 historical file staleness — academic given Phase-2 deferral
- INV-018: `.dev/tasks/` directory structure assumption — portfolio-wide note; if structure changes, all 7 proposals require re-integration

---

## Convergence Score and Status

- Convergence: 0.88 (22/25 diff points resolved; threshold 0.80)
- Status: **CONVERGED**
- Taxonomy coverage: L1 ✓ (S-001 to S-005), L2 ✓ (C-001 to C-006), L3 ✓ (X-001 to X-003, A-002)
- Invariant-probe gate: NO HIGH-severity UNADDRESSED items; convergence NOT blocked
- Rounds completed: Round 1 (parallel, 7 advocates) + Round 2 (sequential, 7 rebuttals) + Round 2.5 (invariant probe)
- Round 3: SKIPPED (`--depth standard` + convergence ≥ threshold)
