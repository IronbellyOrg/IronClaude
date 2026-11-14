# Diff Analysis: owner-answer proposal comparison (Q22, stale age)

## Metadata
- Generated: 2026-11-14
- Mode: A (compare), depth quick (Round 1 only)
- Variants compared: 3 (variant-1 = proposal-A rule of three intervals, variant-2 = proposal-B no number now, variant-3 = proposal-C fixed 2 minutes)
- Total differences found: 12
- Categories: structural (1), content (5), contradictions (3), unique (2), shared assumptions (1)
- Prerequisites validated: output path under `.dev/`; all three inputs exist.

## Structural Differences

| # | Area | Variant 1 | Variant 2 | Variant 3 | Severity |
|---|---|---|---|---|---|
| S-001 | Section layout | Same five sections | Same | Same | Low |

## Content Differences

| # | Topic | Variant 1 | Variant 2 | Variant 3 | Severity |
|---|---|---|---|---|---|
| C-001 | Form of the answer | Rule: 3 x producer's nominal interval | Interim rule: older than 1 producer cycle, number deferred | One fixed number, 2 minutes | High |
| C-002 | Observer snapshot threshold | 45 s | about 15 s (one cycle) | 120 s | High |
| C-003 | Coder workspace record threshold | 3 x its interval, set when CO-03 is designed | deferred to when a reader exists | 2 minutes, a hard requirement on CO-03 now | Medium |
| C-004 | Coder#477 placeholder (CO-02) | Replaced by a formula | Kept, reply says deferred | Replaced by "2 minutes" | Medium |
| C-005 | Copy delay of the TUIBBS channel (CO-04) | Added to the interval when designed | Not addressed (deferred) | Must deliver within 2 minutes | Low |

## Contradictions

| # | Point of Conflict | Variant 1 | Variant 2 | Variant 3 | Impact |
|---|---|---|---|---|---|
| X-001 | Should the snapshot's stale age match the observer's own feed rule (45 s)? | Yes, same meaning everywhere | No, stricter (one cycle) | No, looser (2 min); mapping table must explain the gap | High |
| X-002 | Is it right to decide now, before any reader exists? | Decide the rule now, numbers per producer later | No | Yes, a number now | Medium |
| X-003 | Does a healthy producer in error backoff (up to 60 s) read stale? | Yes, after 45 s | Yes, after 15 s | No | Medium |

## Unique Contributions

| # | Variant | Contribution | Value |
|---|---|---|---|
| U-001 | 1 | Keeps the interval in the note, not in the file, so "publishes nothing new in version 1" holds | Medium |
| U-002 | 2 | Points out the interim one-cycle rule flickers with ordinary timing jitter | High (a defect in the ADJ default) |

## Shared Assumptions

| A-NNN | Assumption | Source Agreement | Impact | Status |
|---|---|---|---|---|
| A-001 | [SHARED-ASSUMPTION] Readers can trust `generatedAt` against their own clock: all three compare a file's `generatedAt` with the reader's current time. Clock skew between the Coder workspace and the TUIBBS host is not discussed; the observer's own 45 s rule uses a monotonic clock in one process (`view.py:32-34`) | All variants measure age from `generatedAt` | A cross-host reader with a skewed clock can misjudge any threshold, small ones most | UNSTATED, promoted |

## Summary
- Structural 1, content 5, contradictions 3, unique 2, shared assumptions 1 (UNSTATED 1).
- Highest-severity items: C-001, C-002, X-001.
- Taxonomy tags: L1 S-001; L2 C-001, C-003, C-004, C-005, X-002; L3 C-002, X-001, X-003, A-001 (boundary: threshold values, clock).
