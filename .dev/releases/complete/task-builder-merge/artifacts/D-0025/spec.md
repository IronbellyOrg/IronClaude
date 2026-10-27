# D-0025 — T02.11 Spec: MIG-002 PR-01 Landing Migration

**Task:** T02.11 (Phase 2)
**Roadmap items:** R-047, R-048
**Date:** 2026-05-17
**Status:** PASS (landed at commit `2648be8`)

---

## 1. Scope

MIG-002 is the single-commit landing migration for the FR-CONV.2 `## Execution Context` header emission in generated MDTM task files (M2). The migration is strictly additive: existing BUILD_REQUEST schema, MALFORMED retry max-2 failure-mode, per-item Context evidence-binding, and TB-Add-8 enforcement are all preserved byte-identical (verified by quality-engineer sub-agent — see `evidence.md` § 4).

## 2. FF_EXECUTION_CONTEXT_HEADER feature flag

| Field | Value |
|---|---|
| Flag name | `FF_EXECUTION_CONTEXT_HEADER` |
| Scope | Header emission in generated MDTM task files (rf-task-builder.md emission step + SKILL.md template stub + EXECUTION CONTEXT BLOCK emitter spec) |
| Default value at M2 | `ON` (DEFAULT-ON at landing) |
| Activation commit | `2648be8` on `feat/mig-002-execution-context-header` |
| Governance file | This spec (`D-0025/spec.md`) |
| Cleanup window | **M7 consolidation** (post-M3..M6 stabilization) — when no regressions have been observed, the optional `EXECUTION_CONTEXT_REQUIREMENTS` signal is folded into the BUILD_REQUEST contract proper and the flag is retired. |
| Cross-references | Phase 2 task T02.11 (this artifact); M7 consolidation entry (TBD when M7 task list is generated); roadmap items R-047 (single-commit landing) and R-048 (governance) |

## 3. Per-line rollback path (commit body authoritative)

Documented in the MIG-002 commit body (`git log 2648be8`):

1. **SKILL.md** — comment out the `EXECUTION CONTEXT BLOCK` emitter section (region containing the `Emit an \`## Execution Context\` section` instruction block). The rendered template stub heading + reader-aid HTML comment may remain inert; emitter no-op suppresses materialization.
2. **SKILL.md** — in the BUILD_REQUEST schema section, set `EXECUTION_CONTEXT_REQUIREMENTS` default to `SUPPRESS` (was `AUTO`).
3. **rf-task-builder.md** — skip the header-emission step in the task-file assembly sequence (the step labeled "Execution Context header").
4. **rf-qa.md** — TB-Add-7 reverts to the M1 simple form (drop degraded-form tolerance + consumer-side grep spot-check); since the header is absent after step 3, the M1 INACTIVE branch fires automatically.

**Invariant during rollback:** per-item Context fields are untouched at every step. TB-Add-8 (per-item evidence-binding) continues to enforce `file:line` citations regardless of header state.

## 4. Acceptance Criteria mapping

| AC (phase-2-tasklist.md L542–546) | Evidence location |
|---|---|
| `make verify-sync` exits 0 immediately after MIG-002 commit | `evidence.md` § 3 (logged exit code) |
| Commit body documents header-generation-block disable path as rollback | `git show 2648be8` commit body, "Rollback path (per-line revert)" section |
| Sub-agent report confirms strictly-additive change (no existing item modified beyond named edit ranges) | `evidence.md` § 4 (quality-engineer report transcript) |
| FF_EXECUTION_CONTEXT_HEADER entry recorded with cleanup window cross-referenced to M7 | This spec § 2 |

## 5. Dependencies

- T02.10 PASS (`D-0024/evidence.md` — NFR-CONV.7 preservation confirmed by 10-case pytest run)
- T02.06 mid-checkpoint PASS (`CP-P02-T01-T05.md`)
- T02.07 PASS (`D-0021/evidence.md` — SKILL.md template + guidance edits)
- T02.08 PASS (rf-task-builder.md header emission, +34 lines, in commit `2648be8`)
- T02.09 PASS (`D-0023/evidence.md` — TEST-004..006 fixtures)

## 6. Risk + mitigation

| Risk | Mitigation |
|---|---|
| Header emitter regression introduces file:line leak | NFR-CONV.3 hidden-input guard at producer-side (SKILL.md EXECUTION CONTEXT BLOCK § "Hidden-input determinism") + consumer-side `grep -cE "src/\|/.*:[0-9]+"` re-check in TB-Add-7 |
| Degraded-form fixture FAILs TB-Add-7 | TB-Add-7 degraded-form tolerance emits `tb-add-7-degraded-tolerated` verdict (not FAIL); confirmed by D-0020 evidence |
| Per-item Context regression | TB-Add-8 continues to enforce file:line citations; D-0024 evidence shows verdict matrix unchanged from M1 |
| Schema drift | API-001-M2 contract row in SKILL.md preserves the 15-field BUILD_REQUEST schema (D-0018 evidence) |
