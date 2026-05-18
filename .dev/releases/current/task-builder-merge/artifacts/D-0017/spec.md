# D-0017 — DM-001 Emitters (References / SourceAreas / KeyConstraints) Spec

**Task:** T02.02 — Implement DM-001 emitters (References / SourceAreas / KeyConstraints)
**Phase:** Phase 2 / Milestone M2 (FR-CONV.2 / PR-01)
**Roadmap rows:** R-033 (DM-001.References), R-034 (DM-001.SourceAreas), R-035 (DM-001.KeyConstraints)
**Branch:** feat/sufficiency-challenge-and-branch-trace-mitigation
**Generated:** 2026-05-17
**Dependencies satisfied:** T02.01 (D-0016 PASS); DM-001 contract-freeze (T01.13 / D-0011)

---

## 1. Scope

Three single-bullet emitters render the body of the `## Execution Context` block emitted by `rf-task-builder` per the FR-CONV.2 wrapper landed in T02.01. The wrapper itself (heading + commented placeholder bullets) lives in the MDTM Output Structure template at `src/superclaude/skills/task-builder/SKILL.md:1561-1568`. T02.02 implements the rules that turn BUILD_REQUEST signal into the three labeled-line outputs.

| Emitter | Roadmap row | Source field in BUILD_REQUEST | Rendered form |
|---|---|---|---|
| References | R-033 | `GOAL`, `WHY`, `related_docs` | `- **References:** R-001: <line>; R-002: <line>; …` |
| Source areas | R-034 | Research notes (module / package / agent-prompt names) | `- **Source areas:** <area-1>, <area-2>, <area-3>[, …]` |
| Key constraints | R-035 | `QA_GATE_REQUIREMENTS` / `VALIDATION_REQUIREMENTS` / `TESTING_REQUIREMENTS` / research findings | `- **Key constraints:** <invariant-1>; <invariant-2>[; <invariant-3>]` |

## 2. Implementation Location

`src/superclaude/skills/task-builder/SKILL.md` EXECUTION CONTEXT BLOCK narrative at lines 856–909 (the spawn-prompt body the task-builder agent reads at runtime). The three emitters are codified as named bullets:

- **References emitter (DM-001.References — R-033):** `SKILL.md:868–877`
- **Source areas emitter (DM-001.SourceAreas — R-034):** `SKILL.md:878–891`
- **Key constraints emitter (DM-001.KeyConstraints — R-035):** `SKILL.md:892–901`

**Venue note (deviation from roadmap M2-row "rf-task-builder.md" column):** The roadmap rows R-033/R-034/R-035 nominate `rf-task-builder.md` as the implementation venue. In this repo, `rf-task-builder.md` is the agent-card interface; the operational manual the agent reads at spawn time is the task-builder SKILL.md spawn-prompt body (already the surface where the EXECUTION CONTEXT BLOCK narrative lives). Placement is consolidated in SKILL.md to keep the emission rules adjacent to the wrapper template (`SKILL.md:1561-1568`) and the spawn-prompt narrative (`SKILL.md:851`, `:856-909`) — a single edit surface for the M2 conversion. The agent card `rf-task-builder.md` reads the SKILL.md spec at runtime, so the emission rules are still consumed by `rf-task-builder` per the roadmap's intent. An earlier attempt to encode the rules at `rf-task-builder.md:186` was reverted by a project linter, confirming SKILL.md is the authoritative venue.

The MDTM Output Structure template at `src/superclaude/skills/task-builder/SKILL.md:1561-1568` was already wired by T02.01 with the three labeled bullets in their final order; T02.02 supplies the derivation rules consumed by the builder at emission time.

## 3. Per-emitter Rules

### 3.1 References emitter (R-033, DM-001.References)

- **Always present** whenever the `## Execution Context` block is emitted — never blank, never omitted.
- **Format:** `R-###: <ref-line>` per ref, with `###` zero-padded starting at `001`.
- **Stable ordering:** GOAL first, then WHY, then each `related_docs` entry in BUILD_REQUEST source order.
- **`<ref-line>` is verbatim** from the source field. Only trailing whitespace may be stripped.
- **Degradation form:** Under minimal BUILD_REQUEST (GOAL-only), `R-001` derives from GOAL alone — the line is still emitted (References-only is the surviving form).

### 3.2 Source areas emitter (R-034, DM-001.SourceAreas)

- **Emit when ≥3 distinct named areas are inferable** from research findings; otherwise OMIT the bullet entirely.
- **Format:** comma-separated named modules / packages / agent-prompt names (e.g., `task-builder skill body`, `rf-qa agent prompt`).
- **No-file-paths guard (NFR-CONV.3 — MANDATORY pre-emission scan):** regex `src/|/.*:[0-9]+` MUST return zero hits against the candidate bullet. On any hit, rewrite the area names to remove paths and `:NN` line numbers, then re-scan.
- **Degradation form:** Under minimal BUILD_REQUEST, the bullet is **absent** (not present-and-blank).

### 3.3 Key constraints emitter (R-035, DM-001.KeyConstraints)

- **Emit 1–3 entries** when invariants are present; otherwise OMIT the bullet entirely.
- **Format:** `<invariant-1>; <invariant-2>[; <invariant-3>]` — semicolon-separated.
- **Verbatim source:** entries are copied verbatim from BUILD_REQUEST `QA_GATE_REQUIREMENTS` / `VALIDATION_REQUIREMENTS` / `TESTING_REQUIREMENTS` (priority order) or top-severity research invariants. No paraphrasing.
- **Bounded:** strictly 1–3 entries. When >3 candidates exist, keep the top 3 by priority order and drop the rest — do not concatenate.
- **Degradation form:** Under minimal BUILD_REQUEST, the bullet is **absent**.

## 4. Invariants Asserted (frozen, T01.13 / D-0011)

1. **References always present** — never blank under any emission path (R-033).
2. **No-file-paths in header** — `grep -cE "src/|/.*:[0-9]+"` against the header range returns 0 (NFR-CONV.3 hidden-input determinism, R-034).
3. **Bounded Key constraints** — between 1 and 3 entries when present (R-035).
4. **Degradation by absence, not blanking** — Source areas / Key constraints bullets are absent (not blank-but-present) under minimal BUILD_REQUEST. Wired in T02.05; T02.02's emitters embed the omit-when-degraded semantics in their per-rule text so T02.05 only needs the minimal-fixture verification.
5. **Per-item Context preservation (CASE-D PR-01)** — the no-file-paths rule applies ONLY to this header. Per-item `**Context**:` fields retain `file:line` citations; TB-Add-7 / TB-Add-8 enforce.

## 5. Acceptance Criteria (per phase-2-tasklist.md L91-95)

| # | Criterion | Verification |
|---|-----------|--------------|
| AC1 | `grep -cE "src/|/.*:[0-9]+" <header-range>` returns 0 | `evidence.md` § 2 — count = 0 against `sample-emitter-output.md` lines 41..49 |
| AC2 | References list populated as `R-###: <ref-line>` per row from BUILD_REQUEST GOAL/WHY/related_docs | `evidence.md` § 3 — sample renders R-001..R-005 with verbatim ref-lines |
| AC3 | Key constraints list has between 1 and 3 entries per BUILD_REQUEST | `evidence.md` § 3 — sample renders 3 entries |
| AC4 | Evidence at `TASKLIST_ROOT/artifacts/D-0017/evidence.md` | `evidence.md` present |

## 6. Producer / Consumer Contract Reference

- **Producer:** `rf-task-builder` agent (Step 5a.i, this spec).
- **Template authority:** MDTM Output Structure block in `src/superclaude/skills/task-builder/SKILL.md:1561-1568` (T02.01 / D-0016).
- **Consumer:** task executor reads the block as a task-level rollup; `rf-qa` cross-validates via TB-Add-7.
- **Schema:** DM-001 v1.0.0 frozen at T01.13 (D-0011 § 1).

## 7. Rollback

Per roadmap: deleting the Step 5a.i block in `src/superclaude/agents/rf-task-builder.md` restores M1 surface — the `## Execution Context` wrapper from T02.01 (D-0016) becomes a heading-with-template-placeholders again. Per-item Context fields are untouched.

## 8. Cross-References

- DM-001 frozen contract: `artifacts/D-0011/spec.md` § 1
- FR-CONV.2 wrapper landing: `artifacts/D-0016/spec.md`
- Phase 2 tasklist row: `phase-2-tasklist.md` L55–103 (T02.02)
- Roadmap M2 row R-033/R-034/R-035: `roadmap.md` L165–167
