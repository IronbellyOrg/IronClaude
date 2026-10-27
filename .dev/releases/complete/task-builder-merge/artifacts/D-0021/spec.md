# D-0021 — COMP-001-M2 SKILL.md Template + Guidance Edits

**Task:** T02.07
**Phase:** Phase 2 — M2 Execution Context Header
**Roadmap items:** R-040, R-041
**Component:** COMP-001 (task-builder skill body, M2 increment)
**Date:** 2026-05-17

---

## 1. Purpose

Land the COMP-001-M2 SKILL.md edits required to expose the Execution Context block to the Builder Agent Prompt guidance surface. Two coordinated edits:

1. **Execution Context block specification** present in the MDTM template embedded in SKILL.md (heading + reader-aid HTML comment + three-bullet form). This was landed by T02.01–T02.05; T02.07 confirms presence.
2. **BUILD_REQUEST guidance** in the "Optional BUILD_REQUEST signals" subsection of the Builder Agent Prompt section enumerates the 3-labeled-line form vs the degraded References-only form verbatim and cites NFR-CONV.3 hidden-input determinism by name.

## 2. Inputs

- Phase 1 frozen contracts: API-001 (T01.14), DM-001 (T01.13 / D-0011 § 1), DM-005 (T01.13).
- Prior Phase 2 PASS state: CP-P02-T01-T05 § 3 (V1/V2/V3 all CONFIRMED).
- Phase 2 roadmap rows R-032 through R-039 implementation evidence (D-0016 through D-0020).

## 3. Outputs

| Output | Path |
|---|---|
| Enhanced BUILD_REQUEST guidance | `src/superclaude/skills/task-builder/SKILL.md:1620–1664` |
| Mirrored dev copy | `.claude/skills/task-builder/SKILL.md` (via `make sync-dev`) |
| Evidence | `artifacts/D-0021/evidence.md` |

## 4. Acceptance Criteria

1. `grep -n "## Execution Context"` returns the rendered template heading line (deviation accepted: actual line 1751, not 1407–1487; see evidence § 6).
2. BUILD_REQUEST guidance section enumerates the 3-line vs degraded forms verbatim.
3. NFR-CONV.3 hidden-input rule referenced by name in the guidance.
4. Evidence file written.

## 5. Failure Modes

- Guidance enumeration misses the "no third intermediate form" invariant → reject (DM-001 contract violation).
- NFR-CONV.3 cited only in prompt-template body, not in guidance → AC3 FAIL.
- `make verify-sync` non-zero → sync drift; must rerun `make sync-dev`.

## 6. Rollback

Strictly-additive guidance enhancement. Revert by deleting the inserted enumeration block in `SKILL.md:1626–1664` (the original 6-line entry remains intact). No template behavior changes; per-item Context fields untouched.

## 7. Forward Linkage

- T02.08 consumes this guidance via rf-task-builder header emission specification.
- T02.09 fixtures (TEST-004/005/006) assert behavior against MDTM generated from the updated guidance.
- T02.11 (MIG-002) commits the strictly-additive landing.
