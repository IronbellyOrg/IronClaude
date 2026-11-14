# Refactoring Plan: Q4

## Overview
- Base variant: Variant 2 (proposal-B)
- Incorporated from: Variant 1 (present facts, Q18 statement), Variant 3 (TUIBBS kept visible), debate consensus on A-001, A-002, A-003, X-002
- Planned changes: 5
- Overall risk: Low to Medium (the reply line changes; the meaning stays `superclaude observe`)
- Rule carried: do not claim a TUIBBS screen exists or is planned.

## Planned Changes

### Change 1: replace the answer and reply line with the converged line
- Source: all three advocates' amended recommendations; Variant 1 facts (ADJ E-01, glossary line 77)
- Target: base title, "Answer", step 2
- Approach: replace
- New line: "TUI Panel = `superclaude observe` (the #409 dashboard); single-host and read-only today; later readers, including a possible TUIBBS screen, not decided."
- Rationale: names the built program firmly (C-001, X-003), keeps properties scoped to today (C-002, A-003), keeps a TUIBBS screen visible without claiming a plan (V3 advocate).
- Risk: Medium

### Change 2: drop "provisional"; the ledger records "the owner's meaning, with today's properties"
- Source: Variant 2 advocate concession 4
- Target: base step 1
- Approach: replace wording
- Risk: Low

### Change 3: state Q18 stays at "not yet"
- Source: Variant 1 (won C-004, 3 of 3)
- Target: base step 3
- Approach: replace "Q18 stays open and unanswered" with Q18's recommended "not before observer release R4 or an owner statement that a TUIBBS screen is planned" (`merged-requirements.md:545`), unchanged by this answer.
- Risk: Low

### Change 4: the owner sees the exact line before it is posted; the line names the #409 dashboard
- Source: debate A-001, A-002
- Target: base "What happens next", step 2, and "What stays unresolved"
- Approach: insert
- Rationale: the phrase appears in no owner-written file and Coder#477 lists Coder template files, so a Coder-side panel is not ruled out (UNVERIFIED); the reply is public in another repository.
- Risk: Low

### Change 5: record the 2026-11-08 Python plus Rich decision
- Source: X-002 (verified, ADJ line 187)
- Target: base "What it unlocks" (the reasoning for not treating #409's Go lineage as TUIBBS intent)
- Approach: append
- Risk: Low

## Changes NOT Being Made

| Diff point | Non-base approach | Why rejected |
|---|---|---|
| C-002, X-001 | Variant 1: "single-host; read-only" as unscoped properties | 2 to 3 of 3: reads as a lasting limit; cannot test Q3's "stays single-host"; "read-only" may not survive R3 (UNVERIFIED). Kept only as "today". |
| C-001, C-004 | Variant 3: a TUIBBS screen is planned | 3 of 3: no owner source; contradicts "Background, not deciding"; would satisfy Q18's trigger by its own wording. |

## Risk Summary

| Change | Risk | Impact | Rollback |
|---|---|---|---|
| 1 | Medium | the public reply line | revert to `variant-2-original.md` line |
| 2 to 5 | Low | wording and notes | remove |

## Review Status
- Approval: auto-approved (non-interactive), 2026-11-14
