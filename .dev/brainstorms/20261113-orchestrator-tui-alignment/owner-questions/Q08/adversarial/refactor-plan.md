# Refactoring Plan: Q8 merged answer

## Overview
- Base variant: variant-3-original.md (proposal C)
- Incorporated variants: proposal A (two changes), proposal B (one change); plus one correction conceded by C's advocate
- Planned changes: 4
- Overall risk: Low
- Merged output path: ../merged-answer.md (in the Q08 folder)

## Planned Changes

### Change 1: the record covers every field the gate checks, deferring release-3 fields explicitly
- Source: A ("When the record is finally written, it can also cover release 3's own choices") and C's advocate concession 1.
- Target: base "Answer" and "What happens next"; remove the gate-field risk from "What it costs or risks" and replace it with the cost of the longer paragraph.
- Approach: modify. Fields (from `origin/master` `acceptance-tests.md:70`): date, option, who decided, where the owner's statement lives, the default before questions are observed, the default after, the post-link choice or deferral, the fallback date, the stack confirmation, the command name, the confirmed production-integration reading. The post-link choice and fallback date may be written "deferred to release 3".
- Rationale: C-004 (C extended, 60%); `release-gates.md:22`.
- Risk: Low.

### Change 2: an honest status line for #409
- Source: C's advocate concession 3; A on C-002.
- Target: base "What happens next", the BC-18 bullet.
- Approach: replace "met by the owner's record of <date>, path" with "direction selected 2026-11-08 (staged); confirmed in the owner's record of <date>, <path>, written after releases 1 and 2 shipped".
- Rationale: C-002 (65%).
- Risk: Low.

### Change 3: interim line if the record is not written in time
- Source: proposal A, "What happens next" first bullet.
- Target: base "What happens next" (new bullet).
- Approach: insert. If the record does not exist when the #409 correction pass (OB-08) posts, BC-18 posts as proposed ("not met as recorded") instead of being left out, as the spec default would.
- Rationale: verdicts of A's and C's advocates.
- Risk: Low.

### Change 4: cite the earlier decisions as background, not as the record
- Source: proposal B ("the evidence already exists in the owner's own 2026-11-08 record ... and 2026-11-11 record").
- Target: base "What it unlocks", third bullet.
- Approach: modify. The paragraph may cite the 2026-11-08 and 2026-11-11 decisions and says the staged direction still stands; it notes that the 2026-11-08 file was "Recorded by an Orca worker" (its line 3), so it supports but cannot replace the owner-written record.
- Rationale: X-001 (C, 95%); A-001 (C, 85%).
- Risk: Low.

## Base weaknesses addressed
| Issue | Better variant | Fix |
|---|---|---|
| Three-field paragraph does not meet the gate | A | Change 1 |
| "Met" overstates the order of events | A, C's advocate | Change 2 |
| No interim text if the owner is late | A | Change 3 |

## Changes NOT Being Made
| Diff point | Non-base approach | Why rejected |
|---|---|---|
| C-001, X-002 | B: amend criterion 1 | Leaves `release-gates.md:22` and `acceptance-tests.md:70` unmet and needs a second repository change; B's own advocate voted C |
| C-001, C-003 | A: write the record only at release 3 | Release 3 is deferred with no date; the production-integration reading stays at the strict default meanwhile (`release-gates.md:34`); A's own advocate voted C |

## Risk Summary
| Change | Risk | Impact | Rollback |
|---|---|---|---|
| 1 | Low | Longer owner paragraph | Shorten |
| 2 | Low | More accurate #409 text | Revert wording |
| 3 | Low | One interim status line | Edit issue |
| 4 | Low | Clearer evidence | Remove |

## Review Status
Auto-approved, 2026-11-14 (non-interactive).
