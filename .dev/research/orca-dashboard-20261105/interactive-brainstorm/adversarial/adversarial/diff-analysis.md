# Diff Analysis: Terminal Dashboard Visual-Design Proposal Comparison

## Metadata
- Generated: 2026-11-05T21:52:00Z
- Variants compared: 2 (V1 = variant-1-opus-frontend.md, 164 lines; V2 = variant-2-sonnet-architect.md, 153 lines; both within the 180-line cap)
- Material debate points (S + C + X + A): 8 (cap 8). Unique contributions (U, not debated): 6
- Categories: structural (2), content (3), contradictions (1), unique (6), shared assumptions (2)
- Taxonomy tags (L1 surface / L2 structural / L3 state mechanics): L1 = C-001; L2 = S-001, S-002, X-001; L3 = C-002, C-003, A-001, A-002
- Similarity check: both share the six-section skeleton and pick Screen A + Textual, but 3 of 5 screen geometries differ; well above the 10% difference floor, so debate proceeds.

## Structural Differences

| # | Area | V1 (opus:frontend) | V2 (sonnet:architect) | Severity | Level |
|---|------|--------------------|-----------------------|----------|-------|
| S-001 | Set of five whole-screen compositions | Triage rail + preview; 2x2 quadrants; time-axis wait lanes; single centered card column (narrow-first); request banner over state columns | Rail + fleet table; horizontal card bands; three-pane thread inspector; kanban state columns; tile grid with 1-cell-per-worker map | High | L2 |
| S-002 | Default screen (both "A") geometry | Left rail stacks requests, blockers and worker counts only; right is a full-height request preview with inline thread | Left column holds ask rail plus selected-ask detail; right is a fleet table of routine worker rows; thread opens as an overlay | Medium | L2 |

## Content Differences

| # | Topic | V1 Approach | V2 Approach | Severity | Level |
|---|-------|-------------|-------------|----------|-------|
| C-001 | Urgency encoding | Glyph plus color on every screen (`!!` over 30m, `!` over 15m), monochrome and NO_COLOR named, thresholds marked as placeholders | "ASCII first, color is enhancement"; age bars and `!!` appear on some screens only (B, D), no thresholds stated | Medium | L1 |
| C-002 | Missing-data guard for impact and blocker links | Shows impact as fact ("2 workers waiting; 1 of 2 reported blockers"); unknown marker used for counts and thread length only | States impact and blocker-to-worker links may not be derivable from Orca; fallback "impact unknown ?"; "reported done" labelled self-reported | High | L3 |
| C-003 | Update placement and selection under state transitions | "N new below" footer counter; preview refreshes in place; cursor follows identity when a card changes column (E) | New asks insert by age without moving selection; list re-sorts only on Esc (C); selected card pinned with a ghost marker if it leaves its column (D) | High | L3 |

## Contradictions

| # | Point of Conflict | V1 Position | V2 Position | Impact | Level |
|---|-------------------|-------------|-------------|--------|-------|
| X-001 | Which framework best fits the bar/tile dashboard compositions | Ratatui fits the bar quadrants (B) and lanes (C) "most directly" via charts, sparklines and gauges | Bubble Tea + Lip Gloss is "strongest" for the card band (B) and tile grid (E); Ratatui suits columns and grid | Medium | L2 |

## Unique Contributions
| # | Variant | Contribution | Value Assessment |
|---|---------|-------------|-----------------|
| U-001 | V1 | Wait Timeline (C): requests as lanes on a 60-minute axis, blocker ticks, time scrub, PAUSED +N queued in the frame | High |
| U-002 | V1 | Focus Column (D): narrow-first centered card column, only the selected card expands; fits a split beside Orca chat | High |
| U-003 | V1 | Urgency thresholds explicitly flagged as placeholders for user calibration | Medium |
| U-004 | V2 | Request Inspector (C): ask list / thread / facts panes, thread inline, "no human reply observed" line | High |
| U-005 | V2 | Instrument Panel (E): worker map with one cell per worker plus a COVERAGE tile (inbox partial, spend not observed, read-only) | Medium |
| U-006 | V2 | Named component split for the default (ask rail, fleet table, detail pane over one read model) | Low |

## Shared Assumptions

Agreement points scanned: both default to Screen A list/preview, both pick Textual, both key selection by identity, both size the request area for three requests.

| # | Agreement Source | Assumption | Classification | Promoted |
|---|------------------|-----------|----------------|----------|
| - | Risks sections | Non-consuming decision enumeration is unverified; 100-message cap | STATED (both) | No |
| - | Shared conventions | Pause freezes rendering only, Orca unaffected | STATED (both) | No |
| A-001 | Identity-keyed selection (V1 sec 2, V2 sec 2) | Orca observations give each request and worker an identity that stays stable across repeated reads and cursor pages | UNSTATED | Yes |
| A-002 | Every request rail/banner/card row sized for the 3-request scene | The request area stays readable when requests exceed the visible rows (dozens of worktrees can raise many) | UNSTATED | Yes |

| A-NNN | Assumption | Source Agreement | Impact | Status | Level |
|-------|-----------|------------------|--------|--------|-------|
| A-001 | Stable request/worker identity across observation reads | Selection stability conventions | High: without it the "selection never jumps" guarantee has no key | Open for debate | L3 (boundary/state) |
| A-002 | Request area overflow behaviour beyond visible rows | Request-first layouts on all screens | Medium: the one region meant to stay loud can silently truncate | Open for debate | L3 (boundary) |

## Summary
- Total structural differences: 2
- Total content differences: 3
- Total contradictions: 1
- Total unique contributions: 6
- Total shared assumptions surfaced: 4 (UNSTATED: 2, STATED: 2, CONTRADICTED: 0)
- Highest-severity items: S-001, C-002, C-003, A-001
