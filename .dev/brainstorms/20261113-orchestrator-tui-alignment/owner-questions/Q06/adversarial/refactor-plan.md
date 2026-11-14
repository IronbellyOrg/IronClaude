# Refactoring Plan: Q6 merged answer

## Overview
- Base variant: variant-3-original.md (proposal C)
- Incorporated variants: proposal B (one observation), proposal A (one fallback)
- Planned changes: 2
- Overall risk: Low (both additive)
- Merged output path: ../merged-answer.md (in the Q06 folder)

## Planned Changes

### Change 1: tell the owner what the narrow scope really means
- Source: proposal B, "What it unlocks", third bullet (the pinned Run `run_93bfa00cae2b` is an old "Claim issue 375" Run).
- Target: base section "Answer" (one added sentence) and "What stays unresolved".
- Integration approach: append.
- Rationale: debate points C-002 and X-001; B's advocate kept dissent there; C's advocate conceded it (round1-advocate-C.md, concession 1); A's advocate also noted it in the steelman of B. Confidence 65 percent.
- Risk: Low. Must not turn into choosing the scope for the owner: the sentence stays the owner's (ADJ:776).

### Change 2: a non-circular park fallback when the live lanes cannot run
- Source: proposal A "What happens next" (dated park entry in the ledger) and A's advocate concession 1 (trigger "release 3 is opened" is circular, merged-requirements.md:257).
- Target: base section "What happens next if the owner picks it" (new last bullet).
- Integration approach: insert.
- Rationale: debate point C-005, won by A at 65 percent; C's advocate concession 4 ("C degrades to A in effect ... without A's clean ledger entry").
- Risk: Low. Trigger wording: "the Orca app answers a read verb and Q24 and Q30 are answered" (the ORCA-AVAILABLE gate, merged-requirements.md:604), not "release 3 opens".

## Base weaknesses addressed
| Issue | Better variant | Fix |
|---|---|---|
| Deferral presented as a free choice between two useful scopes | B | Change 1 |
| No defined outcome if live Orca never becomes available | A | Change 2 |

## Changes NOT Being Made
| Diff point | Non-base approach | Why rejected |
|---|---|---|
| C-002, X-001 | B: owner writes "any Run my terminal holds" now | ADJ:814 lists recommending that scope now as a change not being made; 2 of 3 advocates kept the sentence after the evidence |
| C-003, X-002 | B: build OB-06 in W1 | Violates OB-06's blocked-by list and its "not opened" default (merged-requirements.md:254); B's advocate conceded |
| C-004 | B: "held by this terminal" detection | UNVERIFIED mechanism; the observer may not run `run-use` (merged-requirements.md:573) |
| C-001 | A: do not run the seeded test | Leaves ADJ X-016 open indefinitely; A's advocate voted C |

## Risk Summary
| Change | Risk | Impact | Rollback |
|---|---|---|---|
| 1 | Low | Owner informed of a fact already in the spec | Remove the sentence |
| 2 | Low | Adds a dated park outcome | Remove the bullet |

## Review Status
Auto-approved, 2026-11-14 (non-interactive).
