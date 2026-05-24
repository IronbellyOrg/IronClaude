# D-0021 — T02.07 Evidence: Edit COMP-001-M2 SKILL.md template + guidance

**Task:** T02.07 (Phase 2, COMP-001-M2)
**Roadmap items:** R-040, R-041
**Date:** 2026-05-17
**Status:** PASS

---

## 1. Scope

T02.07 lands the M2 SKILL.md template + guidance edits for COMP-001-M2:

- Confirm Execution Context block specification is inserted in the MDTM template.
- Update BUILD_REQUEST guidance to enumerate the 3-labeled-line form vs the degraded References-only form.
- Cite NFR-CONV.3 hidden-input determinism rule by name in the guidance.

The acceptance-criterion line ranges (`SKILL.md:1407–1487`, `:715–725`) were authored against a pre-Phase-2 estimate of the file. Phase 2 tasks T02.01–T02.06 have expanded the file (current length: 2027 lines). Per CP-P02-T01-T05 § 3 V1, the `## Execution Context` template heading is at the accepted position post-Phase-2 work. This evidence file documents both the embedded block spec and the new guidance enumeration.

## 2. Deliverable A — Execution Context block specification

The Execution Context block specification is embedded in SKILL.md in three coordinated locations, all landed by prior Phase 2 tasks (T02.01–T02.05) and confirmed by CP-P02-T01-T05.

| Location | Line range | Purpose |
|---|---|---|
| EXECUTION_CONTEXT_REQUIREMENTS field in BUILD_REQUEST schema (API-001-M2) | `SKILL.md:779–799` | Optional signal; AUTO / REQUIRED / SUPPRESS values with MALFORMED retry max-2 failure-mode |
| EXECUTION CONTEXT BLOCK section in builder prompt | `SKILL.md:878–974` | Full DM-001 emitter spec (References / Source areas / Key constraints) + degradation rule + hidden-input guard |
| Rendered template stub | `SKILL.md:1751–1757` | `## Execution Context` heading + reader-aid HTML comment + three-bullet form |

### Grep verification

```
$ grep -n "## Execution Context" src/superclaude/skills/task-builder/SKILL.md
780:      the `## Execution Context` block emission in the generated MDTM. Governs
873:       - ## Execution Context (OPTIONAL — see EXECUTION CONTEXT BLOCK below)
879:    Emit an `## Execution Context` section immediately after frontmatter
950:    The block heading `## Execution Context` remains; the
960:    range from the `## Execution Context` heading line through the
1072:16. TB-Add-7: Execution Context source areas reappear in items …
1648:     stub-bulleted). The `## Execution Context` heading and the
1655:  `## Execution Context` heading through the closing `---` separator,
1751:## Execution Context
1825:- [ ] TB-Add-7: Every `## Execution Context` "Source areas:" entry reappears …
```

The block heading is materialized at `SKILL.md:1751` (the rendered template stub). The acceptance-criterion target range (`1407–1487`) reflects pre-Phase-2 file geometry; the actual post-Phase-2 position has been accepted by CP-P02-T01-T05 § 3 V1 as the canonical heading position.

## 3. Deliverable B — BUILD_REQUEST guidance enumeration

The "Optional BUILD_REQUEST signals" section in the Builder Agent Prompt guidance (`SKILL.md:1620–1664`) was expanded by this task to enumerate the two valid rendered forms verbatim:

1. **Fully-populated 3-labeled-line form** — emits all three labeled bullets in order: `**References:**` (R-033), `**Source areas:**` (R-034), `**Key constraints:**` (R-035). Source-field and ordering rules quoted directly from the DM-001 contract.
2. **Degraded References-only form** (R-038) — emits the `**References:**` bullet only; Source areas and Key constraints bullets are absent from the rendered block (not blank-but-present, not stub-bulleted). Heading and HTML reader-aid comment remain.

Both forms are enumerated as the only two valid shapes ("no third intermediate form exists"), matching the DM-001 contract-freeze at T01.13 / D-0011 § 1.

### Grep verification

```
$ grep -n "Fully-populated 3-labeled-line form\|Degraded References-only form" src/superclaude/skills/task-builder/SKILL.md
1627:  1. **Fully-populated 3-labeled-line form** (rollup signal present —
1639:  2. **Degraded References-only form** (R-038 — minimal BUILD_REQUEST,
```

## 4. Deliverable C — NFR-CONV.3 citation in guidance

NFR-CONV.3 hidden-input determinism is now cited by name in the Builder Agent Prompt guidance section (in addition to the existing citations within the prompt template body at `SKILL.md:914` and `:956`):

```
$ grep -n "NFR-CONV.3" src/superclaude/skills/task-builder/SKILL.md
914:      guard (NFR-CONV.3 hidden-input determinism — MANDATORY
956:    Header-wide hidden-input guard (R-039 — NFR-CONV.3 enforcement at the
1653:  **NFR-CONV.3 hidden-input determinism (R-039 — MANDATORY for both
```

The new guidance citation at `SKILL.md:1653` describes the rule scope (byte range from `## Execution Context` heading through closing `---` separator), the verification command (`grep -cE "src/|/.*:[0-9]+"` returns 0), and the uniform applicability to both rendered forms.

## 5. Acceptance Criteria Verification

| # | Criterion | Status | Evidence |
|---|---|---|---|
| AC1 | `grep -n "## Execution Context" src/superclaude/skills/task-builder/SKILL.md` returns a line for the rendered template heading | **PASS** (deviation: actual line 1751, not 1407–1487 — pre-Phase-2 line-range estimate stale; CP-P02-T01-T05 § 3 V1 already accepted post-Phase-2 position) | § 2 grep |
| AC2 | BUILD_REQUEST guidance enumerates the 3-line vs degraded forms verbatim | **PASS** | § 3 — `SKILL.md:1627–1648` enumerates both forms |
| AC3 | NFR-CONV.3 hidden-input rule referenced by name in the guidance | **PASS** | § 4 — `SKILL.md:1653` |
| AC4 | Evidence at `artifacts/D-0021/evidence.md` | **PASS** | This file |

## 6. Deviation Note (AC1 line-range)

The phase-2-tasklist.md acceptance criterion for AC1 specifies that the `## Execution Context` heading appear within `SKILL.md:1407–1487`. The actual post-Phase-2 heading position is `SKILL.md:1751` (rendered template stub). This deviation arises because Phase 2 tasks T02.01–T02.05 expanded the file substantially (BUILD_REQUEST EXECUTION_CONTEXT_REQUIREMENTS field, EXECUTION CONTEXT BLOCK section with three DM-001 emitter specs, degradation rule, header-wide hidden-input guard) — all landed before this task per the M2 task ordering.

The pre-existing checkpoint CP-P02-T01-T05 § 3 V1 already documented and accepted the heading at `SKILL.md:1712` (later shifted to 1751 by this task's additions to the guidance section). The block is materially present, correctly positioned (after frontmatter / Prerequisites & Dependencies, before Phase 1), and consumed by the sample MDTM outputs in D-0017 and D-0020. The deviation is line-range bookkeeping, not a functional gap.

## 7. Files Modified

| File | Lines | Change |
|---|---|---|
| `src/superclaude/skills/task-builder/SKILL.md` | 1620–1664 | Expanded "Optional BUILD_REQUEST signals" entry for EXECUTION_CONTEXT_REQUIREMENTS: enumerated fully-populated 3-line form and degraded References-only form verbatim; cited NFR-CONV.3 hidden-input determinism by name with verification command and uniform-applicability clause. |
| `.claude/skills/task-builder/SKILL.md` | (mirrors src) | Synced via `make sync-dev`. `make verify-sync` reports `✅ All components in sync.` |

## 8. Sync Verification

```
$ make sync-dev   →  ✅ Sync complete.
$ make verify-sync → ✅ All components in sync.
```

## 9. Verdict

**PASS** — All 4 acceptance criteria satisfied (AC1 with documented deviation on stale pre-Phase-2 line-range estimate, materially confirmed by CP-P02-T01-T05 § 3 V1). Deliverables A, B, C present and verified.

Dependencies satisfied: T02.06 (CP-P02-T01-T05) **PASS**.
Unblocks: T02.08 (rf-task-builder header emission), T02.11 (MIG-002 landing migration).
