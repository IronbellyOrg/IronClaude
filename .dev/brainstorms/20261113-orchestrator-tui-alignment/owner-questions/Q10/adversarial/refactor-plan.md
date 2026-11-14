# Refactoring Plan: Q10 merged answer

## Overview
- Base variant: variant-3-original.md (proposal C)
- Incorporated variants: proposal A (one change), proposal B (one change); one correction found by all three advocates; one fact found by A's advocate
- Planned changes: 4
- Overall risk: Low
- Merged output path: ../merged-answer.md (in the Q10 folder)

## Planned Changes

### Change 1: correct only the bullet; keep the true header value
- Source: all three advocates on A-001 (B and C REJECT, A QUALIFY).
- Target: base "Answer" and the second bullet of "What happens next".
- Approach: modify. The three-sentence replacement ("This command reads no messages. A plain `check` consumes them. Whether `check --all --types question` consumes on a live Run is not established.") goes into the bullet at `report.py:534-535` only. The header value "Messages coverage: partial" at `report.py:199` stays (it is true, pinned by `tests/sweep/test_report.py:590`, shown at `docs/designs/orchestrator-mode.md:610`). SW-07 criterion (3), which says both lines "carry exactly" the text (`merged-requirements.md:196`), is reworded accordingly.
- Rationale: A-001 (C amended, 85%).
- Risk: Low.

### Change 2: a reopen trigger
- Source: proposal A ("If OB-03 shows consumption, this answer turns into 'never'") and C's advocate verdict.
- Target: base "What happens next", third bullet.
- Approach: replace "nothing is scheduled for that" with: Q10 is reopened when OB-03 and OB-04 have recorded results with the build pinned (OB-05), or if Q6 parks the observer's read; if OB-03 shows consumption, Q10 becomes "neither program reads questions".
- Rationale: C-001, X-001 (C, leave open), A's and C's advocates.
- Risk: Low.

### Change 3: any sweep read needs a new owner-signed allow-list
- Source: proposal B's framing and B's advocate verdict.
- Target: base "What happens next", first bullet.
- Approach: append "Any later sweep read of messages needs a new owner-signed allow-list entry (NFR-014); this answer does not grant one."
- Rationale: C-003; `merged-requirements.md:571`.
- Risk: Low.

### Change 4: the coordinator already receives its questions
- Source: A's advocate concession 1, verified at `WORKER-CONTRACT.md:100-103`.
- Target: base "What it costs or risks", third bullet (replace the claim that a sweep-only coordinator sees no questions).
- Approach: modify. The coordinator's own wait already wakes on `question` messages and handles each batch before acknowledging it, so the sweep not reading questions costs the coordinator a second view, not its only view; the cost falls on a person who wants a summary screen, which is the observer's job.
- Rationale: C-001, A-002.
- Risk: Low.

## Base weaknesses addressed
| Issue | Better variant | Fix |
|---|---|---|
| Same text for a header and a bullet | all advocates | Change 1 |
| No reopen condition | A | Change 2 |
| "For now" could read as an open door to the allow-list | B | Change 3 |
| Overstated cost for the coordinator | A's advocate | Change 4 |

## Changes NOT Being Made
| Diff point | Non-base approach | Why rejected |
|---|---|---|
| C-001, C-003 | A: an eleventh allow-list template after the tests | The seeded and live tests do not cover the coordinator's own live Run (merged-requirements.md:252); the coordinator already gets questions (WORKER-CONTRACT.md:100-103); A's own advocate voted C |
| C-002, X-002 | B: leave the sentence until OB-03 | Keeps text ADJ rejected (ADJ:813) with no date; B's own advocate voted C |
| C-001 | B: "never" as a standing rule | Not tied to evidence; Change 3 keeps the practical effect (no read without a new signature) |

## Risk Summary
| Change | Risk | Impact | Rollback |
|---|---|---|---|
| 1 | Low | SW-07 criterion (3) reworded | Revert wording |
| 2 | Low | Ledger trigger | Remove |
| 3 | Low | One sentence | Remove |
| 4 | Low | Accurate cost | Revert |

## Review Status
Auto-approved, 2026-11-14 (non-interactive).
