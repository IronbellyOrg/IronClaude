# Diff Analysis: owner-answer proposal comparison (Q21, machine-started label)

## Metadata
- Generated: 2026-11-14
- Mode: A (compare), depth quick (Round 1 only)
- Variants compared: 3 (variant-1 = proposal-A, variant-2 = proposal-B, variant-3 = proposal-C)
- Total differences found: 13
- Categories: structural (1), content (5), contradictions (3), unique (3), shared assumptions (1)
- Prerequisites validated: output path is under `.dev/`, not under `.claude/skills|agents|commands`; all three inputs exist.

## Structural Differences

| # | Area | Variant 1 | Variant 2 | Variant 3 | Severity |
|---|---|---|---|---|---|
| S-001 | Section layout | Same five sections (Answer, Next, Unlocks, Costs, Unresolved) | Same | Same | Low |

## Content Differences

| # | Topic | Variant 1 (watcher record) | Variant 2 (Phase 2, Orca rows after FU-1) | Variant 3 (not now) | Severity |
|---|---|---|---|---|---|
| C-001 | Signal source for the label | Watcher's own record joined by operation id or worktree path; Orca `prompt`/`paneKey` only as notes | Orca `worktree ps` agent row fields in the shape FU-1 records | No label | High |
| C-002 | Allow-list impact (NFR-014) | Widen for `issue-watch status --json`, or approve a file read | None: `worktree ps --json` already allowed (`probes.py:55`) | None | High |
| C-003 | Timing | Phase 2 (W4), after FU-1 | Phase 2 (W4), after FU-1 | Reopen when SW-13 design is accepted | Medium |
| C-004 | Effect on WA-07 handoff gate | Feeds item (3) via labelled row | Feeds item (3) via labelled row | Item (3) must use "bound to a Run" route or reopen Q21 | Medium |
| C-005 | Failure handling when signal is unusable | Falls back to worktree-path matching (coarse) | SW-10 records "no reliable signal" and stops | Not applicable | Medium |

## Contradictions

| # | Point of Conflict | Variant 1 | Variant 2 | Variant 3 | Impact |
|---|---|---|---|---|---|
| X-001 | Is Orca's agent row a trustworthy enough input? | "never by guessing from the `prompt` and `paneKey` fields" | "label ... by reading Orca's `worktree ps` agent rows ... only in the exact shape FU-1 records" | "No code on a signal nobody has measured" | High |
| X-002 | Should a cross-program input be added to the sweep? | Yes (watcher record, contract-note registered) | No new input | No new input | High |
| X-003 | Is the label needed at all before the handoff design? | Yes | Yes | "Avoids building a label that the handoff design may make unnecessary" | Medium |

## Unique Contributions

| # | Variant | Contribution | Value |
|---|---|---|---|
| U-001 | 1 | Positive-match rule: "machine-started" only on a match with a watcher record, which makes a false positive unlikely | Medium |
| U-002 | 2 | Explicit stop rule: if FU-1 shows no usable signal, SW-10 records "no reliable signal" and does not guess | High |
| U-003 | 3 | Observation that WA-07 item (3) already accepts "bound to a Run" as an alternative, so the label may be unnecessary | Medium |

## Shared Assumptions

| A-NNN | Assumption | Source Agreement | Impact | Status |
|---|---|---|---|---|
| A-001 | [SHARED-ASSUMPTION] FU-1 (WA-04) will actually run and record items (e) and (f); all three variants rely on it (V1 and V2 to build, V3 to keep evidence). FU-1 itself waits on Q2 and Q20 (UNSTATED in V1) | All variants cite FU-1 as the evidence source | If FU-1 never runs, V1 and V2 never start and V3 becomes the de facto outcome | UNSTATED, promoted |

Stated assumptions (not promoted): the error direction "watcher session shown as a person's" is the safer one because person sessions are never messaged (STATED in V2 and V3).

## Summary
- Structural 1, content 5, contradictions 3, unique 3, shared assumptions 1 (UNSTATED 1).
- Highest-severity items: C-001, C-002, X-001, X-002.
- Taxonomy tags for the debate: L1 S-001; L2 C-001, C-002, C-004, X-002; L3 C-003, C-005, X-001, X-003, A-001 (guard and state: when the label may fire, what happens on an unusable signal).
