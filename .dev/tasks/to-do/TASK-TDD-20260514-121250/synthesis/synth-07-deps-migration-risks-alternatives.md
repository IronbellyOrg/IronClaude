# TDD Synthesis — §18 Dependencies, §19 Migration & Rollout, §20 Risks & Mitigations, §21 Alternatives Considered

**Status:** Complete
**Date:** 2026-05-14
**Synthesis agent:** synth-07 (Dependencies / Migration / Risks / Alternatives)
**Source corpus:** 00-prd-extraction.md, 02-sc-tasklist-source-mechanisms.md, 14-invariant-preservation.md, web-01-adversarial-taxonomies.md, web-02-monotonicity-patterns.md, qa/research-gate-consolidated.md (SC-1..SC-8)
**Release:** Task-Builder Convergence v3.9 — inverse-direction merge (sc-tasklist → task-builder)

---

## §18 Dependencies

### §18.1 External Dependencies

**NONE.**

Per NFR-CONV.5 (PRD §14.2): "No new external dependencies; gate additions are local checks; no synchronous network calls added." The verification clause is explicit: "Inspect rf-qa.md and SKILL.md diffs: only existing tools (Read, Grep, Glob, Bash) permitted." All six FRs are markdown-level additions to existing skill/agent definition files — there is no runtime, no package, no service, and no network surface introduced by this release.

| Dependency | Version | Type | Status | Justification |
|------------|---------|------|--------|---------------|
| — | — | — | — | NFR-CONV.5 forbids new external dependencies; gate additions use only existing tools (Read/Grep/Glob/Bash). |

### §18.2 Internal Dependencies

All dependencies are internal artifacts of the SuperClaude repository. Sourced from PRD §11 and cross-referenced against the FR landing-order chain (PR-06 → PR-01 → PR-04 → PR-07 → PR-02 → PR-03 per SC-6 corrected order).

| Dependency | Type | Status | Interface | Consumed by |
|------------|------|--------|-----------|-------------|
| `release-spec.md` v1.0.0 (`.dev/releases/current/task-builder-merge/`) | Internal | Draft | Spec document — defines §4.6 landing order, §9 SP-10 rollback matrix, §8.3 audit rows | All 6 FRs (governance) |
| `conflict-register.md` (5 CASE-D rows: PR-01, PR-02, PR-06, PR-07, + PR-05-deferred) | Internal | Complete | Spec document — per-CASE-D conflicting `/sc:tasklist` mechanism + protected invariant | FR-CONV.1, FR-CONV.2, FR-CONV.4, FR-CONV.5 (CASE-D); FR-CONV.3 / FR-CONV.6 are CASE-B (no row) |
| `invariant-probe.md` (INV-002, INV-010, INV-012, INV-015, INV-019, INV-021) | Internal | Complete | Spec document — Round-2.5 adversarial probe; 5 UNADDRESSED-MEDIUM findings routed to FR Negative Criteria | FR-CONV.2, FR-CONV.3, FR-CONV.5, FR-CONV.6 |
| `FINAL-REPORT.md` §6.3 asymmetric finding (5 ADOPT-grade qualities, inverse direction) | Upstream (v3.8) | Complete | Spec document — establishes the merge-worthiness of the 5 mechanisms | All 6 FRs (origin rationale) |
| `FINAL-REPORT.md` §6.2 F2 (21-retry / 18-batch oscillation) + F4 (hidden-input over-engineering) | Upstream (v3.8) | Complete | Spec document — empirical motivation | FR-CONV.5 (F2), NFR-CONV.3 / PR-05 deferral (F4) |
| `rf-team-lead.md:417` escalation behavior (3 fix cycles per phase) | Internal source | Stable — verified NO-DRIFT by Partition B rf-qa (SC-6 confirms :417 correct; :414 was a discarded scope-discovery hypothesis) | Agent definition — all-agents-fail escalation ladder | FR-CONV.6 (must not replace/short-circuit; all-agents-fail guard) |
| `rf-qa.md:144-146` zero-trust verdict (verbatim PASS/FAIL at :141-142, heading at :144 per SC-8) | Internal source | Stable — verified current by invariant-preservation probe | Agent definition — "Any gap regardless of severity = FAIL" | FR-CONV.1, FR-CONV.3, FR-CONV.4, FR-CONV.5, FR-CONV.6 (NFR-CONV.9 preservation) |
| `task-builder/SKILL.md:1452-1457` per-item schema | Internal source | **Drift flagged (SC-1 CRITICAL)** — PRD §25.4 declares `{Description,Context,Acceptance,Confidence,Verification}` "preserved unchanged" here, but current source holds `{Context,Action,Output,Verification,Completion-gate}` | Skill definition — per-item self-contained schema | FR-CONV.1 (TB-Add-8), FR-CONV.2 (Negative Criterion); resolution deferred to TDD §22 Open Question |
| `.dev/tasks/` directory layout (INV-018) | Internal | Stable per release-spec.md SP-33 stability commitment | Filesystem convention — `research/`, `qa/`, `synthesis/`, `reviews/` subdirs + task-file naming | FR-CONV.3 (reads from `.dev/tasks/<task-id>/qa/`); NFR-CONV.8 preservation; all 6 FRs (portfolio-wide blast radius per K-008) |
| `make sync-dev` / `make verify-sync` pipeline (A-001) | Tooling | Operational | CLI — copies `src/superclaude/{skills,agents}` → `.claude/`; `verify-sync` is CI-friendly assertion | All 6 FRs (every FR names `src/superclaude/` paths exclusively; `make verify-sync` MUST PASS before commit per K-009) |

### §18.3 Infrastructure Dependencies

**N/A.** This release introduces no infrastructure. There is no database, no message queue, no compute allocation, no deployment target. The "deployable artifact" is a set of edited markdown definition files (`src/superclaude/agents/rf-qa.md`, `src/superclaude/agents/rf-analyst.md`, `src/superclaude/agents/rf-qa-qualitative.md`, `src/superclaude/agents/rf-task-builder.md`, `src/superclaude/skills/task-builder/SKILL.md`) that propagate to `.claude/` via the existing `make sync-dev` tooling. The only "infrastructure" touched is the source-of-truth → dev-copy sync discipline (A-001), already covered as an internal tooling dependency in §18.2.

---

## §19 Migration & Rollout Plan

### §19.1 Migration Strategy

This is a **strictly-additive, per-FR serially-sequenced** migration (governance assumption A-002). There is no data migration, no schema backfill, and no cutover event. "Migration" here means landing six independent markdown-level additions in a fixed order, each gated by `make verify-sync` PASS before the next begins. Each FR is its own commit; each commit is independently revertable (subject to the co-revert matrix in §19.4).

| Phase | FR / Proposal-ID | Description | Duration | Rollback Plan |
|-------|------------------|-------------|----------|---------------|
| **M1.1** | FR-CONV.1 (PR-06) — lands **1st** | Append TB-Add-1..8 structural checks to rf-qa task-integrity checklist + mirror in 15-item validation block. Strictly-additive per A-002 — no existing check renamed/renumbered/removed. | TBD | Revert specific TB-Add append lines individually (each TB-Add is a discrete append) OR full revert of the PR-06 commit. |
| **M1.2** | FR-CONV.2 (PR-01) — lands **2nd** | Insert task-level `## Execution Context` header in generated MDTM files (after frontmatter, before checklist). Header scope-confined: NO file paths in header; per-item Context fields keep file:line citations. | TBD | Disable header generation; per-item Context fields are unchanged so MDTM files degrade gracefully to References-only / pre-header form. |
| **M1.3** | FR-CONV.3 (PR-04) — lands **3rd** | Inject rf-qa task-integrity verdict table verbatim into rf-qa-qualitative spawn prompt under `## Inherited Structural Verdict`. Operationalises an already-stated rule. | TBD | Disable passthrough block; rf-qa-qualitative falls back to current behavior (independent structural re-checking). |
| **M1.4** | FR-CONV.4 (PR-07) — lands **4th** | Insert "Five Adversarial Axes" header subsection BEFORE rf-qa-qualitative's 15-item checklist + axis-annotation column on the Items Reviewed table. Overlay-only. | TBD | Remove the axis column + the `drift-axis-inactive` annotation; the 15-item checklist is untouched and runs unchanged. |
| **M1.5** | FR-CONV.5 (PR-02) — lands **5th** | Add two stop-conditions (monotonicity guard + regression detection) to EXISTING retry loops. No new loop/stage. | TBD | Disable the two guards individually; existing retry loops + per-gate caps (rf-task-builder.md I16) continue to govern. |
| **M1.6** | FR-CONV.6 (PR-03 BASE) — lands **6th** | Emit synthetic HIGH-severity `synthetic-dnsp` finding when a partition agent's escalation ladder exhausts. All-agents-fail guard preserved. | TBD | Revert the DNSP edit sites; existing `rf-team-lead.md:417` all-agents-fail escalation already handles the zero-partitions-succeeded path with no DNSP. |
| **M1.7** | Post-merge audit + NFR-CONV.4 measurement | Audit the first 5 rf-qa-qualitative runs after FR-CONV.3 lands (K-003 / X-002 audit-target); measure token-cost on 5 representative BUILD_REQUESTs (NFR-CONV.4 ≤10% ceiling). | 1–2 weeks | If audit shows inflation → roll back FR-CONV.3 (see §19.4). If token ceiling exceeded → summarise the FR-CONV.3 verdict table rather than emit verbatim. |

**Why serial, not parallel:** release-spec.md §4.6 mandates strict serial sequencing. The dependency chain is real: FR-CONV.2 depends on FR-CONV.1 (TB-Add-7 cross-validation + TB-Add-8 scope-confinement must be live first); FR-CONV.3 depends on FR-CONV.1 (the TB-Add catalogue IS the verdict content) and FR-CONV.2; FR-CONV.4 depends on FR-CONV.3 (axes apply to items NOT covered by inherited PASS); FR-CONV.5 depends on FR-CONV.1 (gate produces `F_n`) and FR-CONV.6 (synthetic-dnsp consumed by monotonicity per INV-012); FR-CONV.6 depends on FR-CONV.5 for the dedup-key composition rule. K-007 specifically calls out PR-04-before-PR-06 sequencing inversion as a MEDIUM-impact risk — strict serial enforcement is the primary mitigation.

### §19.2 Feature Flags & Progressive Delivery

There is **no GrowthBook / LaunchDarkly / runtime flag system** — and none is needed. Each FR is a self-contained, code-level (markdown-definition-level) addition with **revert-by-line or revert-by-commit granularity**. The "feature flag" is the git revert itself: disabling a feature means reverting its append line(s) or its commit. This is the appropriate granularity for a skill/agent-definition release with no runtime.

| Flag (logical) | Description | Default | Rollout Plan | Cleanup Date | Owner |
|----------------|-------------|---------|--------------|--------------|-------|
| `TB_ADD_1_THROUGH_8` | FR-CONV.1 — each TB-Add is a separate append line, revertable individually. TB-Add-2 ships as `[ADVISORY]` (warn-not-block) until INV-006 calibration. | Enabled at merge | v3.9 ships → 100%; TB-Add-2 stays `[ADVISORY]` until OPEN-INV-006 calibration produces empirical bounds | Post-v3.9 GA + 30 days: remove any fallback paths; TB-Add-2 advisory→hard pending Phase-2 calibration | rf-qa maintainer |
| `EXECUTION_CONTEXT_HEADER` | FR-CONV.2 — `## Execution Context` header generation in rf-task-builder / SKILL.md template | Enabled at merge | v3.9 ships → 100% | Post-v3.9 GA + 30 days: remove References-only degradation fallback if unused | task-builder maintainer |
| `INHERITED_STRUCTURAL_VERDICT` | FR-CONV.3 — verdict passthrough block in rf-qa-qualitative spawn prompt | Enabled at merge | First 5 real rf-qa-qualitative runs audited (K-003 / X-002) before declaring stable | Post-K-003 audit pass (release-spec.md §8.3 row 4) | QA Lead |
| `FIVE_ADVERSARIAL_AXES` | FR-CONV.4 — axis-annotation overlay on the 15-item checklist | Enabled at merge | v3.9 ships → 100% | Post-v3.9 GA + 30 days: tune annotation rules per axis-distribution audit (K-004) | rf-qa-qualitative maintainer |
| `RETRY_MONOTONICITY_GUARDS` | FR-CONV.5 — monotonicity halt + regression halt conditions | Enabled at merge | v3.9 ships → 100% | Post-v3.9 GA + 30 days: confirm false-halt rate acceptable (K-005) | rf-task-builder maintainer |
| `SYNTHETIC_DNSP_EMISSION` | FR-CONV.6 — partition-exhaust HIGH-severity synthetic finding | Enabled at merge | v3.9 ships → 100% | Post-v3.9 GA + 30 days: inspect emission-count metric (K-006) | rf-analyst / rf-qa maintainers |

### §19.3 Rollout Stages

There is no canary / percentage-based rollout — the release ships as a unit (v3.9) once all six FRs have landed in serial order. The "stages" are the six landing steps plus the audit window:

1. **Stage 0 — Pre-merge.** SC-1 CRITICAL (PRD §25.4 vs SKILL.md schema drift) MUST be resolved by Engineering Lead decision before FR-CONV.1 lands, since TB-Add-8 and FR-CONV.2's Negative Criterion both reference the per-item schema. Carried as TDD §22 Open Question.
2. **Stages 1–6 — Serial FR landing.** PR-06 → PR-01 → PR-04 → PR-07 → PR-02 → PR-03 (release-spec.md §4.6). Each FR is its own commit; `make verify-sync` MUST PASS before the next FR begins (K-009 mitigation).
3. **Stage 7 — Post-merge audit window (1–2 weeks).** First 5 rf-qa-qualitative runs audited for inflation (K-003); NFR-CONV.4 token-cost measured on 5 representative BUILD_REQUESTs.
4. **Stage 8 — GA + 30 days.** Fallback paths and degradation branches removed; advisory rules promoted pending Phase-2 calibration.

### §19.4 Rollback Procedure

Rollback is per-FR git revert. Because the FRs form a dependency chain, some reverts force co-reverts. The co-revert matrix is taken from release-spec.md §9 SP-10:

| Reverted FR | Co-Revert Required | Reason |
|-------------|--------------------|--------|
| FR-CONV.5 (monotonicity guards) | FR-CONV.6 dedup-key emission | INV-012 composition (synthetic-dnsp findings counting toward `\|F_n\|` with dedup-key non-regression semantics) is no longer needed once monotonicity is gone. |
| FR-CONV.1 (TB-Add catalogue) | FR-CONV.3 dynamic-enumeration consumer | INV-010 — the TB-Add catalogue is the source the FR-CONV.3 dynamic checklist enumeration auto-picks up. Remove the catalogue and the consumer references a non-existent source. |
| FR-CONV.2, FR-CONV.4 | Independently revertable | A-002 strictly-additive — no downstream FR consumes their output as a structural dependency. |
| FR-CONV.6 (synthetic-dnsp) | FR-CONV.5 `\|F_n\|` definition adjustment | Inverse edge of the FR-CONV.5→FR-CONV.6 co-revert: if FR-CONV.6 is reverted alone, FR-CONV.5's `\|F_n\|` definition must drop the synthetic-finding term. Treat the FR-CONV.5/FR-CONV.6 pair as jointly revertable. |

**Rollback Decision Criteria** (from PRD §20.2 contingencies / §21.3):

- **K-003 inflation detected** — audit of first 5 rf-qa-qualitative runs shows any item marked VERIFIED without independent semantic-check engagement in the Self-Audit listing → **revert FR-CONV.3** (fall back to current independent-re-checking behavior).
- **FR-CONV.5 false-halt rate too high** — monotonicity/regression guard halts a legitimate slow-cycle correction in >50% of observed fix-cycles → **disable the two guards individually**; existing per-gate caps (rf-task-builder.md I16) still bound the loop.
- **TB-Add false-positive volume unacceptable** — a specific TB-Add fires false positives that waste fix-cycles → **revert that specific TB-Add append line**; document the false-positive class (K-001 contingency).
- **Token ceiling NFR-CONV.4 exceeded by >10%** — profile per-FR token contribution; **summarise the FR-CONV.3 Inherited Structural Verdict table** rather than emit it verbatim (K-010 contingency).
- **INV-018 `.dev/tasks/` layout change** — directory restructuring invalidates the portfolio-wide assumption → **re-integration commit covering all 6 FRs** at the new layout (K-008 contingency; HIGH impact, LOW probability).
- **A-001 sync-discipline violated** — `.claude/` edited directly without `make verify-sync` → **revert the `.claude/` direct edit**, re-run from `src/superclaude/` (K-009 contingency).

---

## §20 Risks & Mitigations

Full K-001..K-010 risk register from PRD §20.1 + §20.2. All ten risks were independently assessed LOW probability; impact ranges LOW to HIGH. Risk sources cited to PRD §X.Y.

| ID | Risk | Probability | Impact | Mitigation | Contingency | Source |
|----|------|-------------|--------|------------|-------------|--------|
| **K-001** | TB-Add false positives waste fix-cycles | Low | Low | Each TB-Add cites its source-check-ID for traceability; TB-Add-2 ships as `[ADVISORY]` (warn-not-block, INV-006 LOW); FR-CONV.1 negative criterion forbids removing existing items but each TB-Add is individually revertable by its append line. | Disable the specific TB-Add line; document the false-positive class. | PRD §20.1 / §20.2 |
| **K-002** | Execution Context header drift (header says X, items say Y) | Low | Low | TB-Add-7 cross-validates that header source-areas reappear in items; on drift the gate fails and rf-task-builder retries; the header is optional and degrades to References-only. | Header optional fallback to References-only. | PRD §20.1 / §20.2 |
| **K-003** | PR-04 passthrough causes inflation despite the anti-inflation rule | Low | **Med** | INV-019 acceptance criterion mandates a Self-Audit listing on the first run; X-002 flagged as audit-target — the first 5 rf-qa-qualitative runs after FR-CONV.3 lands MUST be audited (release-spec.md §8.3 row 4). | If any audit shows inflation, disable passthrough and fall back to current behavior. | PRD §20.1 / §20.2; OPEN-X-002 |
| **K-004** | 5-axis annotation ambiguity over-flags items | Low | Low | Axes are annotation-only; the existing 15-item checklist still runs; severity floor preserved; `drift-axis-inactive` annotation emitted when the GOAL-baseline item is missing. | Audit axis distribution; tune annotation rules. | PRD §20.1 / §20.2 |
| **K-005** | Retry monotonicity halts a legitimate slow-cycle correction | Low | Low | Strict-shrink threshold (`F_{n+1} >= F_n` halts; any forward motion continues); X-003 "halt on slow convergence" REJECTED so a by-1 shrink is never halted. | Roll back by disabling the guards individually. | PRD §20.1 / §20.2; FR-CONV.5 Negative Criterion |
| **K-006** | Synthetic-dnsp findings mask real issues | Low | Low | HIGH severity ensures gate-level visibility; all-agents-fail guard preserves the existing escalation path; dedup-key prevents over-emission while preserving the failure signal. | Inspect synthetic-dnsp emission-count metric weekly. | PRD §20.1 / §20.2 |
| **K-007** | PR-04 + PR-06 sequencing inversion (PR-04 lands before PR-06) | Low | **Med** | Sequencing rule PR-06 → PR-04 enforced in release-spec.md §4.6; PR-04's prompt uses dynamic checklist enumeration so it richens automatically when TB-Add items go live (INV-010 mitigation). | Re-merge in correct order; verify INV-010. | PRD §20.1 / §20.2; INV-010 |
| **K-008** | INV-018 `.dev/tasks/` directory structure changes invalidate all proposals | Low | **High** | Portfolio-wide note; SP-33 stability commitment; if directory structure changes, re-integrate all 6 FRs at the new layout. | Re-integration commit covering all six FRs. | PRD §20.1 / §20.2; OPEN-INV-018 |
| **K-009** | sync-discipline (A-001) violated: `.claude/` edited directly without `make verify-sync` | Low | **Med** | All FRs name `src/superclaude/` paths exclusively; CLAUDE.md mandates the sync workflow; `make verify-sync` MUST pass before commit. | Revert the `.claude/` direct edit; re-run from `src/superclaude/`. | PRD §20.1 / §20.2; A-001 |
| **K-010** | Token ceiling NFR-CONV.4 exceeded by >10% | Low | Low | Empirical measurement post-merge; if exceeded, profile per-FR contribution and revise the FR-CONV.3 Inherited Structural Verdict block (verdict table can be summarised rather than verbatim). | FR-CONV.3 verdict-table summarisation. | PRD §20.1 / §20.2; OPEN-TOKEN |

**Risk profile summary:** 10 risks, all LOW probability. Impact distribution: 6 LOW (K-001, K-002, K-004, K-005, K-006, K-010), 3 MEDIUM (K-003, K-007, K-009), 1 HIGH (K-008). The single HIGH-impact risk (K-008) is a portfolio-wide blast-radius concern tied to a stable convention (SP-33) and is mitigated by an explicit re-integration contingency rather than prevention. The MEDIUM-impact risks all have concrete contingencies that fall back to pre-merge behavior. No risk lacks both a mitigation and a contingency.

---

## §21 Alternatives Considered

### Alternative 0: Do Nothing (mandatory baseline)

- **Description:** Leave task-builder unchanged. Continue accepting placeholder/title-only checklist items, undetected DAG cycles, rubber-stamped rf-qa-qualitative passes, silently-aborted partition-agent gates, and the 21-retry / 18-batch oscillation pattern documented in FINAL-REPORT §6.2 F2.
- **Pros:** Zero engineering cost; zero regression risk; preserves the existing pipeline byte-for-byte.
- **Cons:** Persistent silent-acceptance defects (placeholder items, undetected cycles); unbounded oscillation cost; rubber-stamp inflation risk in rf-qa-qualitative remains operationally invisible; the structural-rigor gaps remain exactly as documented in PRD §2.
- **Why Not Chosen:** The PRD §2 problem statement and FINAL-REPORT §6.3 asymmetric finding establish the structural-rigor gaps as well-evidenced and high-leverage. Doing nothing means the 21-retry / 18-batch oscillation continues indefinitely (external prior art — web-02 §2 S23 Reflexion local-minima, S25 Self-Contrast — confirms self-refinement without a no-improvement detector is the *predicted* failure mode, not an accident), and the rubber-stamp inflation risk in rf-qa-qualitative remains undetectable. The release presents 6 FRs at low blast radius with per-FR rollback granularity — the cost/benefit strongly favors acting.

### Alternative 1: Bulk-port all 17 sc-tasklist Stage-6 checks (REJECTED per CB-3)

- **Description:** Import the entire `/sc:tasklist` Stage 6 Structural Quality Gate (the "17-point gate", actually 20 numbered checks) into rf-qa task-integrity as TB-Add-1..17 — or, in the rf-qa-qualitative variant, replace the existing 15-item checklist outright.
- **Pros:** Higher nominal coverage; reuses gate logic that has codebase-validated provenance in sc-tasklist.
- **Cons:** Per the CB-3 per-check classification (research file 02 §2), only 8 of 17 candidate checks are intent-portable. 11 checks are **bundle-specific** — phase-file naming, index references, `T<PP>.<TT>` ID format, em-dash phase headings, checkpoint emission, end-of-phase position, checkpoint-report-path presence — and are inapplicable to task-builder's single-MDTM output (vs sc-tasklist's multi-file phase bundles). A further 3 checks (Effort/Risk/Tier completeness, D-#### deliverable uniqueness, R-### orphan detection) reference traceability schemes task-builder does not use. Bulk-porting would also force X-001's blanket "no specific file paths" rule onto per-item Context fields, which would gut task-builder's evidence-bound-item invariant.
- **Why Not Chosen:** CB-3's per-check classification (research file 02 §2 table) shows only 8 of 17 are intent-portable; the per-check approach preserves invariant safety and avoids importing implementations that simply do not apply to single-MDTM artifacts. External prior art supports the per-check / overlay framing: Travassos et al. 2001 SRS-defect taxonomy (web-01 §3 S6), IEEE 830 (web-01 S3), and Fagan inspection (web-01 S4) all treat adversarial categories as a **classification dimension layered onto an existing checklist**, not a wholesale replacement — exactly how the LLM-faithfulness literature (web-01 §2 ACM CSUR S17) layers faithfulness sub-types onto QA-evaluation methods. Removing the codebase-validated 15-item rf-qa-qualitative checklist would also lose information with no compensating gain.

### Alternative 2: Continue v3.8 RF→SC direction only (REJECTED)

- **Description:** Stop the inverse-direction merge work entirely; continue only the original v3.8 RF-to-SC direction (improvements flowing from the rf-* agents into `/sc:tasklist`).
- **Pros:** Simpler — a single merge direction with no inverse-port classification overhead.
- **Cons:** FINAL-REPORT §6.3's asymmetric finding documents 5 ADOPT-grade qualities in the *inverse* direction (sc-tasklist → task-builder): the structural gate checks, the Execution Context concept, the inherited-verdict naming pattern, the five adversarial axes, and the monotonicity/regression stop-conditions. Ignoring them leaves task-builder structurally under-rigored relative to its sister skill.
- **Why Not Chosen:** The portfolio-wide adversarial debate (Phase 4 of the orchestration pipeline) identified these 5 as worth adopting. Not adopting them means task-builder remains permanently weaker than its paired skill on exactly the dimensions — structural gating, retry convergence, adversarial coverage — where rigor matters most for an artifact-generating skill.

### Alternative 3: Ship PR-05 (Tier-History Advisory) in Phase-1 with advisory framing (REJECTED — DEFERRED to Phase-2)

- **Description:** Read frontmatter from historical `.dev/tasks/done/TASK-RF-*` task files to inform tier selection at task-builder run-time, framed as a non-binding "advisory" signal.
- **Pros:** Could improve tier-selection accuracy on task-types similar to prior completed tasks.
- **Cons:** Hidden-input determinism risk (NFR-CONV.3): task-builder MUST NOT read any input outside the BUILD_REQUEST + source-tree that could modify its behavior. PR-05 reads `.dev/tasks/done/` — a behavior-modifying hidden input. FINAL-REPORT §6.2 F4 documents this exact pattern as an over-engineering anti-pattern from v3.8 that this release explicitly avoids. The "advisory is non-binding" claim relies on agent prompt-obedience to a critical-rule, not on a structural guarantee (invariant-preservation research §5 Q1 flags this — there is no structural test that an advisory does not silently weight tier selection).
- **Why Not Chosen:** Deferred to Phase-2 per release-spec.md §2.1. Re-evaluation trigger: `.dev/tasks/done/TASK-RF-*` count reaches ≥10 with ≥3 distinct `task_type`s AND a genuinely advisory-only (not behavior-modifying) mechanism is designed. The NFR-CONV.3 hidden-input guard verification ("fixture-populated `.dev/tasks/done/` MUST produce byte-identical structural output to empty `.dev/tasks/done/`") is the gate PR-05 must pass before any Phase-2 re-introduction.

### Alternative 4: Single-FR mega-merge (REJECTED)

- **Description:** Land all 6 FRs as a single commit / single FR for one review cycle.
- **Pros:** One review cycle; a simpler, flatter git history.
- **Cons:** Eliminates per-FR rollback granularity. The per-FR rollback dependency matrix (release-spec.md §9 SP-10) and the K-003 audit-target specifically on FR-CONV.3 both require the FRs to be independently revertable. A bug detected post-merge in any single FR would force a full revert and re-land of all six. External prior art reinforces the seam: web-02 §7 (Sentry/Rollbar fingerprinting literature, S13/S15/S16; ddmin S27; CDCL S18) treats failure-grouping (dedup) and progress-detection (cardinality stall) as **orthogonal concerns** — INV-012's composition rule ("synthetic findings count toward `|F_n|`, but identical dedup-key across cycles is dedup NOT regression") *requires* FR-CONV.5 and FR-CONV.6 to be expressible independently; a mega-merge erases the seam INV-012 needs.
- **Why Not Chosen:** Per-FR rollback granularity is a stated release goal (release-spec.md §9 SP-10). The composition lives in the algorithm, not in a single monolithic data structure (web-02 §7).

### Alternative 5: X-003 "halt on slow convergence" threshold (REJECTED — FR-CONV.5 design alternative)

- **Description:** Halt the fix-loop when `F_{n+1} = F_n - 1` (a shrink of only 1), declaring slow convergence "too slow" to be worth continuing.
- **Pros:** More aggressive token conservation than the strict `|F_{n+1}| >= |F_n|` halt.
- **Cons:** Legitimate slow-cycle correction is a normal pattern — some defects genuinely require multiple cycles to converge, and later cycles tackle harder residual defects (web-02 §7 notes per-cycle work is *not* i.i.d., so "rate of convergence" cannot be estimated from a single linear trajectory). Halting on slow shrink would short-circuit legitimate work, and a rate threshold introduces a tunable parameter K with no principled value — contradicting the v3.9 goal of intent-porting a *proven* mechanism. The abstract-interpretation widening literature (web-02 §3 S29/S30) supports a binary "did the chain stabilize?" test, not rate-of-stabilization thresholds.
- **Why Not Chosen:** Per the FR-CONV.5 Negative Criterion (PRD §14.1, invariant-preservation research §3 FR-CONV.5), slow-cycle shrink — even by 1 — MUST NOT be halted. The strict-shrink threshold (`F_{n+1} >= F_n` halts; any strict decrease continues) is the operational definition. The existing max-retry cap already provides a soft "give up on slow convergence" backstop; X-003 would shadow that cap with a less principled tunable.

### Alternative 6: Pure-cardinality monotonicity, no regression precedence (REJECTED — web-02 prior art)

- **Description:** Use only the `|F_{n+1}| >= |F_n|` cardinality halt; omit regression detection entirely.
- **Pros:** Simpler — a single rule, one comparison per cycle.
- **Cons:** Misses PASS@N → FAIL@N+1 regressions where cardinality stays constant but composition changes (a fix-cycle trades an old defect for a new one of equal count — `|F|` is unchanged, the monotonicity guard passes, but the system has silently worsened). `F` is a **set with identity**, not just a count. INV-012's dedup-key composition with FR-CONV.6 requires set-identity semantics. External prior art is direct: web-02 §4 documents CI/CD pass-to-fail transition as the canonical real-regression signal (S9/S10/S11), and web-02 §6.4 notes ddmin's failure-preservation invariant (S27) — any algorithm reducing a defect set must first preserve the failure-direction invariant, which is exactly what regression-before-monotonicity precedence enforces.
- **Why Not Chosen:** Composition matters — pure cardinality would let real regressions slide. The regression-detection-before-monotonicity precedence rule (FR-CONV.5: "Regression > monotonicity") catches the equal-cardinality old-for-new swap that the cardinality check alone cannot. This regression/dedup disambiguation via dedup-key is a v3.9 composition contribution (web-02 §4.3) built on established CI/CD and ddmin primitives.

---

## Synthesis-Time Constraint Acknowledgements

- **SC-1 (CRITICAL):** The PRD §25.4 vs `SKILL.md:1452-1457` per-item schema contradiction is recorded in §18.2 as a flagged-drift internal dependency and feeds TDD §22 Open Questions. It is a Stage-0 pre-merge blocker for FR-CONV.1 — see §19.3 Stage 0.
- **SC-6:** The corrected FR landing order (PR-06 → PR-01 → PR-04 → PR-07 → PR-02 → PR-03) is used throughout §19. File 12's "FR-CONV.2 as 3rd" mis-ordering is disregarded.
- **SC-7:** TB-Add-7 origin per PRD §14.1 (absorbs PR-01 failure-mode #4 cross-validation) — file 08 authoritative; file 02's "Minimum Task Specificity Rule" speculation disregarded.
- **SC-8:** §18.2 cites the zero-trust verdict definitions at `rf-qa.md:141-142` (heading at :144) per the line-citation polish.

---

**Status:** Complete
