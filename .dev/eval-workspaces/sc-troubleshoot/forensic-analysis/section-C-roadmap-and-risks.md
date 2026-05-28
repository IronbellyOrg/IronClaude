---
section: C — Roadmap, Planning, Tests, Risks
feature: /sc:forensic + sc:forensic-protocol
sources:
  - roadmap/roadmap.md (v1, 904 lines, 2026-02-26)
  - roadmap/roadmap-2.md (v2, 593 lines, 2026-02-28)
  - roadmap/dependency-graph.md (282 lines)
  - roadmap/risk-register.md (242 lines)
  - roadmap/test-strategy-2.md (402 lines)
  - roadmap/spec-amendments-checklist.md (458 lines)
  - roadmap/extraction-2.md (225 lines)
date: 2026-05-21
---

# Section C — Roadmap, Dependencies, Tests, Risks

## Phased Execution Plan

### v2 Plan (Authoritative, 7 Milestones)

`roadmap-2.md:60-71` declares 7 milestones with collision suffix `-2` (output dir already contained v1 — `roadmap-2.md:534`). Calendar estimate: 10-13 weeks XL (`roadmap-2.md:24`). Complexity 0.87 HIGH (`roadmap-2.md:13`).

| ID | Name | Effort | Source |
|----|------|--------|--------|
| M0 | Spec Finalization Tier 1 (5 blockers: P-001, P-004, P-005, P-002, P-013) | M 3-5d | `roadmap-2.md:64,139` |
| M1 | Spec Finalization Tiers 2-3 (16 proposals P-006-P-016, P-021) | M 3-5d | `roadmap-2.md:65,203` |
| M2 | Foundation: command shell + skill shell + 9 finalized schemas | L 6-10d | `roadmap-2.md:66,262` |
| M3 | Phase 0 recon agents + domain discovery | M 3-5d | `roadmap-2.md:67,310` |
| M4 | Phase 1 (investigation) + Phase 3 (fix proposals) — fan-out phases | L 6-10d | `roadmap-2.md:68,363` |
| M5 | Phases 2+3b adversarial + Phases 4-6 pipeline (largest authoring milestone) | L 6-10d | `roadmap-2.md:69,376,436` |
| M6 | Testing + sync + verify-sync + docs | L 6-10d | `roadmap-2.md:70,507` |

Deliverables: 2 (`.claude/commands/sc/forensic.md` mirroring `src/superclaude/commands/forensic.md`, and `src/superclaude/skills/sc-forensic-protocol/SKILL.md` — `roadmap-2.md:18-22`).

### MVP/Shipping Gates

- **M0 gate**: 5 Tier-1 normative blockers — without these, "estimated rework cost is 3-5x" (`roadmap-2.md:105-106`).
- **M2 gate**: containers exist + 9 schemas finalized — required for parallel authoring downstream (`roadmap-2.md:215-217`).
- **M6 gate**: `make sync-dev && make verify-sync` exits 0; all 58 success criteria SC-001-SC-058 pass (`test-strategy-2.md:374`); no SKILL.md stub sections (`roadmap-2.md:502`).

### Cross-Milestone Proposal Map

`roadmap-2.md:548-572` maps each of 22 proposals to milestone+task. Note P-022 was REJECTED (convergence 0.76) and incorporated as note-only at T5.22 (`roadmap-2.md:540`).

## Dependency Graph

### Milestone Critical Path (v2)

`roadmap-2.md:78-90` declares the v2 chain **fully linear**:
```
M0 → M1 → M2 → M3 → M4 → M5 → M6
```
"All sequential, no parallelism — spec correctness is a prerequisite for each authoring stage" (`roadmap-2.md:89-90`).

**Intra-milestone parallelism opportunities**:
- M4: Phase 1 and Phase 3 agent authoring shares no dependencies (`roadmap-2.md:93-94`).
- M5: Phases 4 and 5 can proceed in parallel (`roadmap-2.md:94`).

### Pipeline Phase Data Flow (Runtime)

`dependency-graph.md:120-243` documents the 7-phase runtime data flow. Critical handoffs:
- Phase 0 → `investigation-domains.json` consumed by Phase 1 (`dependency-graph.md:133,140`).
- Phase 2 → `base-selection.md` consumed by orchestrator filter (`dependency-graph.md:154,156`); zero hypotheses path → terminal report (`dependency-graph.md:158`).
- Phase 3b → `fix-selection.md` is the **PRIMARY DECISION POINT** (`dependency-graph.md:182-183`).
- Phase 4 → produces `baseline-test-results.md` BEFORE any fix is applied (`dependency-graph.md:192-193`).
- Phase 6 reads **only 6 summary artifacts** (no raw source) — architectural constraint preserved (`dependency-graph.md:226-232`).

### External Dependencies

`dependency-graph.md:249-258`:
- `/sc:adversarial` (HIGH risk R-01 — runtime) — required by Phases 2 and 3b.
- Serena/Context7/Sequential MCP (LOW risk R-04, with fallback) — required by Phases 0b, 1, 3, 4.
- Haiku/Sonnet/Opus tier availability (MEDIUM risk R-02).
- `uv run ruff check`, `uv run pytest` (Low risk).

### Proposal-to-Proposal Dependencies

`dependency-graph.md:267-279`:
- **P-001 is the root** — must execute first; "all other proposals" depend on it establishing the spec baseline.
- P-017 → P-018 → P-019 chain (baseline test → exit state → `--clean` guard).
- P-020 → P-017 (baseline test results need redaction).
- P-009 → P-021 (multi-root path records reference domain_id).

## Test Strategy

### Philosophy

`test-strategy-2.md:16-32` — HIGH complexity → interleave ratio 1:1 (every authoring task pairs with a test/validation task). "Behavioral contract testing, not implementation testing" — tests validate schema-conforming artifacts on schema-defined inputs; not internal model tier heuristics or prompt wording (`test-strategy-2.md:28-32`). "Continuous parallel validation" at each milestone boundary, not deferred to a final test milestone (`test-strategy-2.md:23-26`).

### Test Classification

`test-strategy-2.md:38-46`: 6 types — Smoke (per-phase), Integration, Edge case, Schema conformance, Security, Manual review. **All gated at M6** — no upstream gating.

### Test Inventory (10 files, M6)

`roadmap-2.md:456-470` declares deliverables D6.1-D6.13:
- D6.1-D6.4: Phase 0/1/3/5 smoke tests (`tests/sprint/forensic/test_phase*_smoke.py`).
- D6.5: `test_checkpoint_resume.py` — validates `run_id` stability + `phase_status_map`.
- D6.6: `test_zero_hypotheses.py` (P-016 edge case).
- D6.7: `test_tiny_target.py` (P-015 — <5 files → single domain bypass).
- D6.8: `test_dry_run.py` (P-003).
- D6.9: `test_redaction.py` (P-020 — must redact ≥4 secret pattern types).
- D6.10: `test_schemas.py` — all 9 schemas with positive+negative variants (`test-strategy-2.md:299-311`).

### Fixture Design

`test-strategy-2.md:154-163` — single 5-file synthetic Python project: `main.py` (subprocess), `auth.py` (bare except), `utils.py` (untested), `tests/test_main.py` (partial coverage). Engineered to produce ≥2 domains and observable Phase 0 output. Canned artifacts per phase boundary at `tests/sprint/forensic/fixtures/canned_artifacts/{phase0,phase2,phase4}_output/` (`test-strategy-2.md:340-345`).

### Coverage Targets / Markers

- Schema tests → `@pytest.mark.unit` (`test-strategy-2.md:402`).
- Smoke tests → `@pytest.mark.integration` (`test-strategy-2.md:399-400`).
- 58 total success criteria SC-001 through SC-058 (`test-strategy-2.md:374`).

### Stop-and-Fix Severity

`test-strategy-2.md:351-358`: CRITICAL (schema/checkpoint/contract breaks) → stop immediately; HIGH (missing proposal integration) → fix in current milestone; default threshold = CRITICAL+HIGH always halt.

### Per-Milestone Gates

`test-strategy-2.md:50-145` defines gates: M0/M1 = peer review; M2 = `make verify-sync`+file existence; M3/M4/M5 = content review; M6 = full pytest suite + sync exits 0. **M6 rule**: "ALL tests must pass before release. Any failing test, even in an 'optional' category, is fixed before marking M6 complete. Zero exceptions" (`test-strategy-2.md:143-144`).

## Risk Register

Two distinct risk models exist — `risk-register.md` is the canonical doc (10 risks, scored 1-5); `roadmap-2.md:516-526` carries 10 different roadmap-execution risks.

### Canonical Risks (`risk-register.md`)

`risk-register.md:217-228` summary matrix:

| ID | Risk | Prob | Impact | Exposure | Priority | Source |
|----|------|------|--------|----------|----------|--------|
| R-01 | sc:adversarial integration failures | 3 | 5 | **15 HIGH** | HIGH | `risk-register.md:18-33` |
| R-02 | Model tier unavailability (Haiku/Sonnet/Opus) | 2 | 4 | 8 MED | MED | `risk-register.md:37-52` |
| R-03 | Orchestrator token budget overruns | 4 | 3 | 12 MED | MED | `risk-register.md:56-72` |
| R-04 | MCP server unavailability | 2 | 3 | 6 LOW | LOW | `risk-register.md:76-91` |
| R-05 | Non-deterministic Phase 0 domain discovery | 3 | 4 | 12 MED | MED | `risk-register.md:95-111` |
| R-06 | Adversarial convergence failure | 2 | 3 | 6 LOW | LOW | `risk-register.md:115-129` |
| R-07 | Phase 4 worktree isolation failures | 3 | 4 | 12 MED | MED | `risk-register.md:133-149` |
| R-08 | Resume stale-target detection gaps | 3 | 3 | 9 MED | MED | `risk-register.md:153-169` |
| R-09 | Spec amendment integration complexity | 3 | 3 | 9 MED | MED | `risk-register.md:173-189` |
| R-10 | Mock agent test infrastructure | 3 | 3 | 9 MED | MED | `risk-register.md:193-210` |

**Only R-01 (adversarial integration) is rated HIGH (15).** Residual risk after mitigation drops it to MEDIUM (`risk-register.md:33`).

### Key Mitigations (`risk-register.md:232-242`)

- **R-01 mitigation**: Pre-M6 validation of `/sc:adversarial`; three-level fallback chain (P-011) — Level 1 retry with `--depth quick`; Level 2 single Sonnet scoring agent (60s timeout, 1000 token cap); Level 3 direct passthrough with `"debate_status": "skipped"` (`risk-register.md:27-31`).
- **R-03 mitigation**: P-012 per-phase overflow table; `budget_status` field in progress.json; deterministic truncation (Phase 6: omit rejected-hypotheses) (`risk-register.md:64-68`).
- **R-05 mitigation**: Hash-based domain ID `hash(name, sorted(files_in_scope))[:8]` (P-009) — file scope determines ID even when names shift (`risk-register.md:104-109`).
- **R-09 mitigation**: P-001 executed FIRST and mechanically (verbatim move, no rephrasing); spec-amendments-checklist.md orders all 22 proposals (`risk-register.md:183-188`).
- **R-10 mitigation**: Build fixtures during M2 alongside schema definitions, not at M9 (`risk-register.md:242`).

### Roadmap-Execution Risks (`roadmap-2.md:516-526`)

Different set covering authoring: R-001 (adversarial API change, exposure 10), R-002 (slug ID instability, 8), R-003 (token ceilings too low, 9), R-008 (adversarial convergence < 0.80, **exposure 12 Medium**, mitigated by partial-result continuation only hard-aborting below 0.5). R-010 = SKILL.md grows too large to load → use refs/ pattern.

## Spec Amendments (Residual Ambiguity Signal)

The spec needed **22 proposals applied before authoring** — heaviest signal of residual ambiguity in the source spec.

### M0 — Tier 1-2 Structural Prerequisites (8 proposals)

`spec-amendments-checklist.md:16-162`:
- **P-001 (Section 17 normativity)**: blocking root — moves FR-047-FR-055, NFR-009, NFR-010, Schema 9.9 out of Section 17 into canonical sections. "MECHANICAL move — do not rephrase" (`spec-amendments-checklist.md:40`). Establishes the spec baseline that all subsequent amendments edit.
- **P-004 (path inconsistencies)**: Score 10.00/10 — adversarial output paths must be `phase-2/adversarial/*` consistently (`spec-amendments-checklist.md:45,49-54`).
- **P-009 (stable domain IDs)**: hash-based IDs replacing position-based; hypothesis IDs become `H-[a-f0-9]{8}-\d+` (`spec-amendments-checklist.md:60-69`). Note: v2 roadmap uses **slug-based** IDs (`H-{domain_slug}-{seq}` — `roadmap-2.md:158`); checklist uses **hash-based** (`H-{domain_id_short}-{seq}` — `spec-amendments-checklist.md:64-66`). This is an internal contradiction between checklist (2026-02-26) and v2 roadmap (2026-02-28).
- **P-006**: Add `new-tests-manifest.json` schema; P-013 model tier observability; P-015 minimum domain rule (1-10, not 3-10); P-014 MCP tool contract (`Edit, MultiEdit` added to `allowed-tools`); P-021 multi-root provenance.

### M1 — Tier 3-5 Behavioral/Runtime/Hardening (14 proposals)

`spec-amendments-checklist.md:172-413`:
- P-017 (baseline test artifact); P-018 (3-state exit model success/success_with_risks/failed); P-003 (dry-run + `skipped_phases`); P-002 (`--depth` precedence); P-005 (Phase 3b canonical path).
- P-011 (three-level adversarial fallback); P-012 (token overflow table with soft/hard/action per phase); P-020 (artifact redaction, `--no-redact` flag); P-016 (zero-hypothesis terminal + `--auto-relax-threshold`); P-022 (concurrency default 5, per-phase MCP budget table — note: P-022 is MODIFY in checklist but REJECTED in v2 roadmap convergence verdict — see `roadmap-2.md:572`).
- P-007 partial (risk surface — **`secrets_exposure` REJECTED in checklist `spec-amendments-checklist.md:362` but ADDED in v2 roadmap `roadmap-2.md:155`** — internal contradiction).
- P-010 partial (fix tier uniqueness — "up to three" with `uniqueItems` constraint per checklist `spec-amendments-checklist.md:373`; but v2 roadmap mandates **exactly 3** per `roadmap-2.md:156`). Another internal contradiction.
- P-008 partial (target_paths required; `run_id`/`spec_version`/`phase_status_map` REJECTED per `spec-amendments-checklist.md:400`; but v2 roadmap REQUIRES `run_id` + `phase_status_map` per `roadmap-2.md:157`). Third internal contradiction.
- P-019 (`--clean` guard clause minimal scope).

### Explicitly Deferred to v2.0

`spec-amendments-checklist.md:445-458`: `secrets_exposure` category, `spec_version`/`run_id`/`phase_status_map` in progress.json, exactly-3-tiers constraint, `--clean=archive|delete` variants, `--redaction-config`, full MCP scheduler with semaphores.

**Signal**: Spec needed 22 proposals × major sections; multiple proposals reach the v2 roadmap with **inverted verdicts** from the checklist — indicating the team had not fully converged when v2 was authored.

## Roadmap v1 → v2 Delta

### Headline Changes

| Aspect | v1 (`roadmap.md`) | v2 (`roadmap-2.md`) |
|--------|-------------------|---------------------|
| Date | 2026-02-26 (`roadmap.md:4`) | 2026-02-28 (`roadmap-2.md:6`) |
| Milestones | **9** (M0-M9) (`roadmap.md:14,37-47`) | **7** (M0-M6) (`roadmap-2.md:17,62-71`) |
| Proposals | 22 (14 ACCEPT + 8 MODIFY) (`roadmap.md:13`) | 21 (14 ACCEPT + 7 MODIFY, P-022 REJECTED) (`roadmap-2.md:16`) |
| Convergence basis | proposal-verdicts (initial) | proposal-verdicts.md convergence 1.00 (`roadmap-2.md:38`) |
| Validation | — | PASS, 0.91 (`roadmap-2.md:25-26`) |
| Adversarial status | — | integrated (`roadmap-2.md:27`) |
| Calendar | XL 10-14 weeks (`roadmap.md:15`) | XL 10-13 weeks (`roadmap-2.md:24`) |
| Complexity | not declared in v1 | 0.87 HIGH (`roadmap-2.md:12-13`) |
| Domain ID strategy | hash-based `[a-f0-9]{8}` (per checklist, contemporaneous with v1) | slug-based `kebab-case` (`roadmap-2.md:158,304`) |

### Milestone Collapse (the architectural learning)

v1's 9 milestones M3-M8 (`roadmap.md:38-47`):
- M3 Checkpoint/Resume Protocol (separate)
- M4 Phase 0 Recon
- M5 Phase 1 + Phase 3
- M6 Adversarial Integration (Phases 2 & 3b)
- M7 Implementation & Validation (Phases 4-5)
- M8 Phase 6 + CLI Integration

Collapsed in v2 into:
- M3 Phase 0 (recon + domain discovery as one) (`roadmap-2.md:67`)
- M4 Phases 1 + 3 (`roadmap-2.md:68`)
- M5 Phases 2 + 3b + 4 + 5 + 6 — **the v2 mega-milestone** (`roadmap-2.md:69,376`)

Rationale per v2: "Fewer, larger milestones reduce coordination overhead; M3-M5 were granular enough to author but too fine for milestone tracking" (`roadmap-2.md:538`). "Phases 1 and 3 share enough structural similarity to author within a single milestone."

Specifically:
- **Checkpoint/Resume promoted into M5** (was standalone M3 in v1 per `roadmap.md:41`, `dependency-graph.md:50-54`) — became `refs/checkpoint-resume.md` deliverable D5.7 (`roadmap-2.md:390`).
- **CLI Integration absorbed into M2 Foundation** (was M8 in v1 per `roadmap.md:46`).
- **Testing/Sync remains terminal** (M9 v1 → M6 v2).

### Dependency Graph Shift

v1 dependency-graph.md is **strictly linear** with no intra-milestone parallelism declaration (`dependency-graph.md:101-105` "All milestones are on the critical path because the dependency graph is linear").

v2 (`roadmap-2.md:91-94`) explicitly declares parallelism opportunities **within M4 and M5** — Phases 1+3 can be authored by different contributors after M3; Phases 4+5 can run in parallel within M5.

### Convergence and Validation

v2 introduces validation_score (0.91), adversarial_status (integrated), and explicit proposals_integrated count of 21 (`roadmap-2.md:25-27,15-16`) — none present in v1's frontmatter. P-022 transitioned from MODIFY (v1, in M1) to REJECTED (v2, addendum note only T5.22).

### Why "-2" Suffix

`roadmap-2.md:534` "Output directory already contains prior artifacts from 2026-02-26 run; collision protocol applied" — i.e., v2 was authored as a parallel artifact, not an in-place replacement.

---

## Summary (≤200 words)

**Top-3 risks**:
1. **R-01 sc:adversarial integration failures** (P3×I5 = **15 HIGH**, `risk-register.md:219`) — the only HIGH risk. Mitigated by three-level fallback chain (P-011) + pre-M6 operational validation. Without `/sc:adversarial`, Phases 2 and 3b are non-functional.
2. **R-03 token budget overruns** (P4×I3 = 12 MED, `risk-register.md:221`) — likely for large codebases; mitigated by P-012 per-phase overflow table with deterministic truncation actions and `budget_status` observability.
3. **R-05 non-deterministic Phase 0 domain discovery** (P3×I4 = 12 MED, `risk-register.md:223`) — LLM synthesis variability breaks resume; mitigated by hash-based deterministic domain IDs (P-009).

**Critical path**: v2 is fully linear M0→M1→M2→M3→M4→M5→M6 (`roadmap-2.md:89`). M5 is the bottleneck — it absorbs adversarial integration (Phases 2+3b), implementation (Phase 4), validation (Phase 5), and synthesis (Phase 6) plus all of P-011/P-017/P-018/P-019/P-020 (`roadmap-2.md:376-440`).

**v1→v2 shift**: 9 milestones collapsed to 7 (`roadmap.md:37` vs `roadmap-2.md:62`); M3 Checkpoint/Resume folded into M5; M8 CLI Integration folded into M2 Foundation; v2 added explicit intra-milestone parallelism for M4 (Phase 1+3) and M5 (Phase 4+5) (`roadmap-2.md:91-94`). v2 also rejected P-022 (was MODIFY in v1) per convergence 0.76, and added validation/adversarial_status frontmatter. Internal contradictions remain between `spec-amendments-checklist.md` (2026-02-26) and `roadmap-2.md` (2026-02-28) on three proposals: P-007 `secrets_exposure`, P-008 `run_id`/`phase_status_map`, and P-010 exactly-3 vs ≤3 tiers — signal that convergence was not complete.
