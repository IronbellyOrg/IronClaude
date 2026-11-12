---
name: Orca Observer
description: Experience contract for the read-only Orca terminal observer (IronClaude issue 409)
status: draft
created: 2026-11-08
updated: 2026-11-12
sources:
  - .dev/issues/409/bmad/ux-orca-observer-r2-review/validation-report.md (the R2 review that drove the 2026-11-12 update; findings cited as F01..F47)
  - .dev/issues/409/bmad/spec-orca-observer/adapter-contract.md
  - _bmad-output/planning-artifacts/orca-observer/prd.md
  - _bmad-output/planning-artifacts/orca-observer/addendum.md
  - _bmad-output/specs/spec-orca-observer/SPEC.md
  - _bmad-output/specs/spec-orca-observer/rendering-rules.md
  - _bmad-output/specs/spec-orca-observer/release-gates.md
  - _bmad-output/specs/spec-orca-observer/acceptance-tests.md
  - _bmad-output/specs/spec-orca-observer/snapshot-export-schema.md
  - _bmad-output/specs/spec-orca-observer/write-back-future-stage.md
  - _bmad-output/specs/spec-orca-observer/stack.md
  - IronClaude/issue-409-mvp/.dev/design/orca-observer-20261106/ (text exports only)
---

# Orca Observer — Experience Spine

> **Update 2026-11-12 (release 2, coordinator questions).** Owner rule for this update: respect the original design where possible; do not throw it away. Nothing below was deleted. Where release 2 builds something different from the original design, the original wording is kept readable and carries one of two marks:
> - **[Design reference / R3 (QUESTION-LINK), not built in R2]**: the original design stays as the target for a later release.
> - **[Superseded in R2 by X]**: R2 builds X instead, and X is described next to it.
>
> **[R2 as built]** marks the new panel and its rules. Strings in code font are the exact on-screen strings the owner gave for R2. The code is being changed in parallel to match them; where this document and the build differ, this document wins (spines win on conflict).
>
> **Words.** The on-screen title is `COORDINATOR QUESTIONS`. Orca has no human recipient field (rendering-rules.md), so this document says "coordinator question" everywhere except where it quotes the gap-notice literal `Human questions: source UNVERIFIED, 0 rows interpreted, not "no questions"`, which the spec keeps (F30).
>
> **Owner decisions of 2026-11-12** (stated to the update run; not an owner-written file in the repository):
>
> | # | Decision | Where it lands |
> |---|---|---|
> | 1 | When the question list is cut to fit the screen, the OLDEST questions stay on screen (oldest first). Newer ones are reachable by export (`e`) only, and the screen says so. | Component Patterns, "Coordinator questions panel" |
> | 2 | On a short terminal the QUESTIONS win over the worker ledger: the ledger is squeezed first. | Responsive & Platform, "R2 panel height order" |
> | 3 | The count is called "seen, not resolved" (the original SEEN IS NOT RESOLVED wording), not "observed open". | counts line, summary, Voice and Tone |
> | 4 | A full window (exactly 100 rows) shows the count as `100+`. | counts line, collapsed summary |

## Foundation

**Product.** A full-screen, read-only terminal observer for the Orca fleet. It is built in Python and Rich as a `superclaude observe`-style subcommand in IronClaude. The final command name is OQ-3; `superclaude observe` is the recommendation, not a decision. It answers one question at a glance: what is the fleet doing, according to the sources the observer can actually read, and what does it not know?

**Who.** *The supervisor*: one human who watches 5-10 orchestrators and 50-100 sessions from one terminal (prd.md personas). Secondary users:
- the reviewer, who judges the R0 fixture gallery;
- the owner, who alone decides the gates;
- a later machine consumer of the JSON snapshot.

Agents, workers and staff teams are not users.

**Stance.** Observer, never operator. No key and no screen element calls Orca or changes Orca state (T3). Every value is shown with its source. A value the observer could not read says so in words, and it is never shown as zero, false, a dash or a blank.

**Releases this document covers** (owner decision 1; the brief's names are on the left, the spec's in brackets):

| Release | What the supervisor gets | Gate before it |
|---|---|---|
| R0 (spec R0) | Offline fixture replay of all three directions (A Signal Bridge, B Attention Ledger, C Decision Desk) at 160, 116 and 80 columns, each with degraded versions, plus the key-reader spike. Synthetic data only. | none (first task) |
| R1 (spec R1) | Signal Bridge's worker ledger on the verified `worker-list` source, with the COUNTS strip, the freshness strip, the inspector, the text export, and Attention Ledger's one-line "question source UNVERIFIED" notice. | DIRECTION-SELECTED (not yet passed; OQ-1) |
| B (spec R2) | Attention Ledger: open human questions as the main view, with A's ledger one key away. **[R2 as built: superseded in R2 by the stacked `COORDINATOR QUESTIONS` panel for one named Run, shown on the ledger screen. The two-column Attention Ledger (`OPEN HUMAN QUESTIONS`, `SEEN IS NOT RESOLVED`, `RETAIN CONTEXT`) and "one key away" are design reference / R3 (QUESTION-LINK), not built in R2.]** | QUESTION-OBSERVATION |
| C (spec R3) | Decision Desk: for one selected question, the affected sessions with their worker-list evidence. **[Design reference / R3 (QUESTION-LINK), not built in R2.]** | QUESTION-LINK |
| Later | R4 remote fleet; write-back as a separate future stage (see "Future Stage: Write-back"). | separate boundary change |

The production-integration reading of the R0/R1 boundary is UNVERIFIED (OQ-2). This document applies the stricter reading: until DIRECTION-SELECTED passes, only offline R0 exists.

**Which Signal Bridge is R1.** R1 is the spec's composition (rendering-rules.md:6, release-gates.md:3). It contains the worker ledger, the COUNTS strip, the freshness strip, the gap notice and the inspector. It is neither of the two Signal Bridge layouts in the design package:

| Source | What it describes | Used in R1? |
|---|---|---|
| PLAN.md:43 cockpit | owner rows, a narrow intervention rail, a footer change ribbon | No. Owner rows do not exist in `worker-list`. The intervention rail is write-back, which is out of R1. The change ribbon becomes the `changed since HH:MM (k)` line plus `*` row marks. |
| Built `layouts/group_a.py:61`, shown in the 160-column Signal Bridge export; the 116- and 80-column builds drop SIGNALS (rendering-rules.md:85) | HUMAN QUESTION panel, OBSERVATION WINDOW (sources), SESSION REGISTER, SIGNALS counts and bars | In part. SESSION REGISTER becomes the worker ledger. OBSERVATION WINDOW becomes the freshness strip. SIGNALS becomes the COUNTS strip, with no bars. HUMAN QUESTION becomes the one-line gap notice, because no question source is verified. |

The spec treats the design-package prototype as a visual reference only and records that the built layout departs from it: the prototype's 116-column collapse claim does not match the built prototype (rendering-rules.md:8, X-001), and the built Signal Bridge's 116- and 80-column builds drop SIGNALS (rendering-rules.md:85). Neither the spec nor the PRD names the PLAN.md cockpit. The owner has not confirmed that R1 may differ from both of them, so this is open question UX-OQ-1.

### Where it runs (R2; PROPOSED, the owner has not chosen)

**Fact.** An Orca terminal that holds no Run is fenced out of every Run it does not hold. The one test of this (Q-1, 2026-11-11) is recorded FAIL (`consumer_fenced`): a plain terminal with a handle but no Run was refused when it read a Run bound to another terminal, and no rows came back (`artifacts/q1-result.md` in `.dev/tasks/to-do/TASK-WF-release2OfTheOrc-20261111-203306/`). `run-use` is forbidden for the observer (adapter-contract.md). So the observer cannot read a Run by name from wherever it happens to start. It must run where it already holds the Run, or hold a Run of its own. When it starts in the wrong place the first screen is the FAILED panel (UJ-7), not an edge case.

| # | Place | How | Tested? | What it costs |
|---|---|---|---|---|
| 1 | The coordinator's own terminal | A foreground command from a shell that terminal holds. | **Not tested.** UNVERIFIED that the command inherits the terminal's binding. | The terminal is taken while the observer runs. |
| 2 | A background child of the coordinator agent's shell | The child loops `--once` and writes the snapshot file; a separate pane reads that file. | **Not tested.** UNVERIFIED that a child process shares the binding. A viewer-only mode (a pane that only reads the snapshot file) is NOT built. | Needs a viewer the build does not have. |
| 3 | Its own terminal | The terminal creates a Run of its own (`run-create`) and is told to be the target of questions (`send --to run:<observer run>`). | **The only variant tested**: the sample in `artifacts/t17-sample.md` (a throwaway Run created from a plain terminal, 5 synthetic questions; two reads 6 s apart returned the same 5 rows). It says nothing about real traffic. | A change in how questions are addressed. Questions sent to the coordinator's Run are not seen. |

**Recommendation (not a choice):** place 1 for a quick start; place 3 if questions can be routed to the observer's Run. **Open question UX-OQ-9:** which place does the owner want, and can questions be addressed to a Run of the observer's own? Nothing in this document depends on the answer except the action line shown under a FAILED fence (`start the observer in the terminal that holds <runId>`).

## Information Architecture

One view model feeds every view, the inspector and the export (T48). The default view is chosen once at start-up and never switches by itself (INV-021, T45). If the question source has not succeeded in this process, the observer starts on the R1 ledger with the gap notice, even in a release whose gate has passed.

**[R2 as built]** R2 has no second view to switch to: the `COORDINATOR QUESTIONS` panel is stacked on the ledger screen when `--questions` is on. The start-up rule above is unchanged and stays as the design reference for the R3 B and C views. One sentence of the original is superseded: the gap notice no longer waits for the question source to succeed. It stays while the question source has not read, and the panel replaces it once the source has read or failed (F27), because a failed first read is stated by the panel itself. While the panel reads `question read pending`, both show.

### Screen inventory per release

| # | Surface | Release | Reached from | Purpose |
|---|---|---|---|---|
| 0 | Fixture gallery: A, B, C at 160/116/80, each with degraded variants | R0 only | fixture-replay start-up | Lets the reviewer and owner compare directions for DIRECTION-SELECTED. Header line 1 reads `SYNTHETIC FIXTURE <variant>, not Orca data` (rendering-rules.md:17). Separately, every R0 render carries the T50 marking "synthetic fixture, not live evidence" (acceptance-tests.md:44, rendering-rules.md:5). |
| 1 | Worker ledger (default view) | R1 | start-up | Shows one row per worker from `worker-list` under the header, freshness strip, COUNTS strip and gap notice. |
| 2 | Worker inspector | R1 | `Enter` on a ledger row; `Esc` goes back | Shows every field of one worker, untruncated, with full IDs. It is the only place `projection.stage.*` renders. |
| 3 | Too-small diagnostic | R1 (all later views) | the terminal is resized below the minimum height | Explains that the screen is too small and keeps coverage, scope and `PARTIAL` visible. Under 80 columns the line `terminal too narrow (min 80)` appears above the COUNTS strip. |
| 4 | Text export (`e` in session, or `--once`) | R1 | `e` key, or the `--once` flag (the only mode on Windows) | Writes the same view model as plain text, with no ESC bytes, full IDs and no truncation (T27, T48). Separately, `export(view)` writes the versioned JSON snapshot on every R1 cycle, with no key press (FR-16, prd.md:86); `--once` runs one cycle, so it writes one snapshot. The snapshot's destination is open (UX-OQ-4). |
| 5 | Attention Ledger | B | start-up, only when the question source succeeded in this process | Shows open human questions, oldest first, beside `SEEN IS NOT RESOLVED` and `RETAIN CONTEXT`. The R1 ledger is one key away; the key is not defined (UX-OQ-3). **[Design reference / R3 (QUESTION-LINK), not built in R2. Superseded in R2 by screen 5a. The title `OPEN HUMAN QUESTIONS` is retired.]** |
| 6 | Question inspector | B | `Enter` on a question | Shows the full question record and the seven RETAIN CONTEXT attributes. At 80 columns this is the only place RETAIN CONTEXT appears. **[Design reference / R3 (QUESTION-LINK), not built in R2: R2 questions are listed, not selectable, so there is no question inspector and no RETAIN CONTEXT.]** |
| 5a | Coordinator questions panel **[R2 as built]** | R2 | Part of screen 1, stacked above the worker ledger in the place of the gap notice (PROPOSED position), only when `--questions` is on and QUESTION-OBSERVATION has passed | Lists the messages of type `question` of one named Run, oldest first, with the state of the read, the count `seen, not resolved`, and every caveat. Listed, not selectable: no cursor, no inspector, `Enter` and `Esc` do nothing on it. One layout at every width. |
| 7 | Decision Desk | C | after QUESTION-LINK; how it is entered and whether it is the default view are open (OQ-B/C, OI-4, OI-9) | For one selected question, shows the affected sessions with their worker-list evidence and the other observed questions. **[Design reference / R3 (QUESTION-LINK), not built in R2.]** |
| 8 | Affected-session inspector | C | `Enter` on an affected session | Same content as screen 2, reached from the question context. **[Design reference / R3 (QUESTION-LINK), not built in R2.]** |

Release count: R1 has 4 surfaces (1-4), B adds 2 (5-6), C adds 2 (7-8). Screen 0 exists only for R0 review. **[R2 as built: release B adds the one panel 5a, not 5-6; screens 5-8 are design reference / R3.]**

Filter input, export confirmation, the `changed since` line and the historical-rows count are states of screen 1, not separate screens.

### Screen 1 composition, top to bottom (R1)

1. Header line 1: `ORCA OBSERVER  mode=live  scope=<result.scope.source or "scope unknown">  as of <local time of last good poll>` (rendering-rules.md:17), displayed as `HH:MM:SS`. When the scope is `bound`, `one Run only` follows it (adapter-contract.md:63; risk K4, prd.md:363).
2. Header line 2, the freshness strip: `worker-list OK 4s` (or `STALE 52s` / `FAILED (exit 2) 1m` / `NOT POLLED`) and `messages UNVERIFIED (not read)`.
3. COUNTS strip (1 or 2 lines, never dropped): `collected n / reported T`, `PARTIAL` when it applies, the scope, `source counts: active a / reclaimable r / retained t / released l`, `SETTLED unavailable (no source)`, `FROZEN unavailable (no source)`, `cost unavailable`. While a filter is active, `filter <expr>: k of n collected` sits directly after `source counts: ...` (rendering-rules.md:56).
4. Gap notice: `Human questions: source UNVERIFIED, 0 rows interpreted, not "no questions"`.
5. Status line (PROPOSED position): `changed since HH:MM (k)` after a mark, `k historical hidden (h)`, `k duplicate rows ignored`, and the last export result.
6. Ledger panel titled `worker-reported, not questions`, with its column header and rows.
7. Footer: the key list plus `shown x/y | collected n / reported T`.

**Screen 1 with questions on (R2 as built).** Items 2 and 4 change; the rest stay.
- Item 2, freshness strip: the cell `messages UNVERIFIED (not read)` is replaced by `coordinator questions OK 0s (one Run <runId>)` / `STALE 50s` / `FAILED (consumer-fenced)` / `not read yet`.
- Item 4, gap notice: it stays while the question source has not read. Once the source has read or failed, the `COORDINATOR QUESTIONS` panel (Component Patterns) takes its place.
- Item 6, ledger: its row-count line reads `workers shown 2 of 4`.
- Header line 1 (`scope=...`) and the COUNTS strip describe the workers of every Run in scope; the panel describes one Run only. Whether the header also names the Run for questions, and whether the panel says "questions from other Runs are not read", is open (UX-OQ-12).

**Spec text the R2 panel does not render (F18).** The spec promises more than R2 draws. Each item is either design reference or replaced:

| Spec text (rendering-rules.md) | R2 status |
|---|---|
| A `SEEN IS NOT RESOLVED` block with a big count | Superseded in R2 by the counts line `seen, not resolved: <n> | closed by evidence: unavailable (no source)`. The original block is design reference / R3. |
| "Questions stay until explicit resolution." | Superseded in R2 by the standing caveat `no read marker in source: answered questions stay listed`. |
| "No reply observed is not delivery failure." | Design reference / R3: R2 shows no reply or delivery state. |
| `no longer in source window (last seen HH:MM)` | Superseded in R2 by one string, `[no longer in source window]`. The `(last seen HH:MM)` form is design reference. |
| Per-question `open, closure source unavailable` | Superseded in R2 by the counts line's `closed by evidence: unavailable (no source)` and the per-line `reason unknown`. A listed question is never shown as resolved. |

The spec owner confirms this table; the spec files other than the R2 panel paragraph still carry the original wording.

## Responsive & Platform

The terminal size is the only responsive input. The layout is recomputed on every resize and every 15 s refresh. Every rendered line satisfies `cell_len <= W` (T23). Widths are measured in display cells, not characters, so CJK and emoji are cut by cell width (T30).

**Source status of the numbers below.** The spec names three Round 2 artifacts: A's width matrix, B's x/width coordinates and C's 44-row height contract. It does not define their contents (rendering-rules.md:8; OQ-14). Only these values are specified:
- the 160/116/80 breakpoints;
- B's `right = width - 43`;
- the 116 and 80 ledger line forms;
- the under-80 notice;
- the minimum content.

Every other number in this section is **PROPOSED** and needs owner confirmation.

### Width bands (R1 ledger)

| Terminal width | Ledger form | Columns shown | Source |
|---|---|---|---|
| ≥ 160 | full table | `dispatchId`, run, `workerState`, `dispatchStatus`, `terminalState`, `projection.outcome` (raw), `projection.nextAction.kind` (verbatim), `liveness.verdict (liveness.source)`, evidence age | rendering-rules.md:29 |
| 116-159 | line form | `<kind> <dispatchId> <liveness.verdict> <age>`; the other fields move to the inspector | rendering-rules.md:32 |
| 80-115 | short form | `kind`, the dispatch ID cut with `>`, age | rendering-rules.md:32 |
| < 80 | short form at the reduced width | `terminal too narrow (min 80)` above the COUNTS strip; the strip's denominators still print | rendering-rules.md:12 |

**PROPOSED column budget at 160** (inside a 2-cell frame, 1 space between columns):

| Column | Cells |
|---|---|
| gutter (selection + change mark) | 2 |
| `dispatchId` | 26 |
| run | 14 |
| `workerState` | 10 |
| `dispatchStatus` | 10 |
| `terminalState` | 10 |
| `projection.outcome` | 12 |
| `nextAction.kind` | 18 |
| `liveness.verdict (source)` | 24 |
| age | 7 |

The total is 133 cells plus 9 separators. Extra width goes to `dispatchId` first. The real ID length is UNVERIFIED, so any cut ID ends with `>` and the full ID is always in the inspector.

**PROPOSED budget at 116:** gutter 2, kind 20, `dispatchId` up to 60, verdict 16, age 7. **At 80:** gutter 2, kind 18, `dispatchId` up to 46, age 7.

From 116 to 159 the 116 form is used, padded. Nothing interpolates between bands.

### The 44-row height contract

The spec fixes the minimum content and the rule that a too-small diagnostic replaces the view (rendering-rules.md:13, T49). The drop order and the minimum row count are not defined (OQ-14). The design exports are 48 rows at 160 columns and 42 rows at 116 and 80 (DESIGN-CONTRACT.md:8, concepts.md:36). The design plan gives ranges, not a contract: "Wide target around 44-52 rows; compact target around 36-44" (design PLAN.md:57). 44 sits at the edge of both ranges, but no source fixes it as the contract height. That is UX-OQ-2.

**Rows that never drop.** The spec fixes only the COUNTS strip as never dropped (rendering-rules.md:19) and coverage, scope and `PARTIAL` as minimum content (rendering-rules.md:13, T49). The other rows in this list are PROPOSED design choices, not spec statements:
- header line 1 (PROPOSED);
- the freshness strip (PROPOSED);
- the COUNTS strip, which wraps to 2 lines before any token is cut (spec, rendering-rules.md:19);
- the gap notice (PROPOSED; the spec places it above the ledger at every width, rendering-rules.md:31, but does not say it survives height pressure);
- the footer, carrying `shown x/y | collected n / reported T` (PROPOSED).

Coverage, scope and `PARTIAL` (spec minimum content, rendering-rules.md:13) sit inside these rows.

**PROPOSED R1 budget at 44 rows, 160 columns:**

| Rows | Content |
|---|---|
| 1 | header |
| 2 | freshness strip |
| 3-4 | COUNTS strip (row 4 blank unless it wraps) |
| 5 | gap notice |
| 6 | status line |
| 7 | ledger frame top, with the title |
| 8 | column header |
| 9-42 | 34 ledger rows |
| 43 | ledger frame bottom |
| 44 | footer |

**PROPOSED shrink order when height falls** (first to go first):
1. Ledger rows shrink. The window keeps the selected row visible and shows `x/y shown` and `+N more`.
2. The status line folds into the footer.
3. The ledger frame is replaced by a plain rule.
4. Below the PROPOSED minimum of 12 rows (the fixed rows plus at least 3 ledger rows), the too-small diagnostic (screen 3) replaces the ledger. It keeps every row that never drops: the header, freshness, COUNTS, the gap notice and the footer.

**PROPOSED B order** (Attention Ledger, ≥116 columns) **[design reference / R3 (QUESTION-LINK), not built in R2; superseded in R2 by "R2 panel height order" below]**:
1. `RETAIN CONTEXT` shrinks first; it is reachable from the inspector.
2. Then the embedded ledger rows.
3. Then question blocks, oldest kept. `SEEN IS NOT RESOLVED` and the gap or question-coverage line never drop.

**C**: no layout is specified beyond the design exports. Its order is part of OQ-14.

**R2 panel height order [R2 as built; the order of the first two steps is the owner's, the rest is PROPOSED].** With questions on, the panel takes rows before the ledger does. First to go first:
1. **Worker ledger rows** (owner decision 2: the questions win; the ledger is squeezed first). The earlier "at least 3 ledger rows" comfort (the reviewed build's code comment) is no longer promised, and the R1 12-row minimum above no longer holds with questions on. The ledger keeps its `workers shown 2 of 4` line, and `+N more` counts only rows not shown. How far it may shrink, and whether it may reach zero rows, is open (UX-OQ-10).
2. **Question lines, from the newest end** (owner decision 1: the oldest stay, oldest first). The panel then shows the cut line `questions shown 7 of 20 (oldest first; 13 newer not shown; e exports all)`. That line is part of the panel's fixed rows and is budgeted: it is never the row that is dropped to make room. There is no scroll key; `e` is the only way to the newer questions (PROPOSED: `--once` too).
3. **The panel collapses to one summary line** when it cannot hold its fixed rows (PROPOSED: the title, `one Run only`, the state line, the counts line, the standing caveat and the disclosure). The same line is the diagnostic on a terminal too narrow (under 80 columns) or too short:
   `coordinator questions: seen, not resolved <count text>; <state>; one Run only: <runId>; best effort, coverage unknown`
   The count text is never a bare number: an empty read says `0 (source window only; not proof none exist)`, a full window says `100+ (window full)`, retention exceeded says `unknown (retention exceeded)`. The text for 1 to 99 is not in the owner's list; PROPOSED `<n> (source window only)` (UX-OQ-15). The state is the same words as the state line (`OK 3s`, `STALE 50s`, `FAILED (consumer-fenced) 3s`, `pending`). The reviewed build collapsed at about 16 rows at 116 columns with 4 workers; that figure was read off renders and is not a contract.

The gap notice rule is unchanged by this: while the question source has not read, the gap notice is a minimum row (T49).

### B geometry (spec values) [design reference / R3 (QUESTION-LINK), not built in R2]

| Width | Layout |
|---|---|
| ≥ 116 | Full frame with `right = width - 43`. At 160: left `OPEN HUMAN QUESTIONS` x=1 w=114, right column x=117 w=42. At 116: right = 73, question panel 70 wide, right column stays 42. |
| 80-115 | Single column: header, freshness, COUNTS, `SEEN IS NOT RESOLVED n`, question lines or the UNVERIFIED notice, then the 80-column ledger, plus the invariant lines "Questions stay until explicit resolution." and "No reply observed is not delivery failure.", which stay at this width (rendering-rules.md:42). RETAIN CONTEXT is reachable only through the inspector. |

**R2 panel geometry [R2 as built; superseded in R2 for the table above].** One stacked block at every width of 80 columns or more; no right column, no `right = width - 43`, no `SEEN IS NOT RESOLVED` or `RETAIN CONTEXT` panels. The worker ledger keeps its own width form (160 full table, 116 line form, 80 short form). Under 80 columns the line `terminal too narrow (min 80)` shows and the panel is the one summary line above. Wrapping rules:
- The disclosure wraps; it is never cut.
- A question line is `<age>  [no longer in source window]  <subject>  reason unknown`. The bracket part appears only when the question left the window. **Only the subject is ever clipped** (with `>`), so the state word is never cut (F04, F41: the cut is always at the subject's end, not at the line's end).
- At 80 columns the key line must keep `e export` and `q quit` visible, because export is the only way to the questions the screen does not show (F08; the reviewed build cut them, PROPOSED requirement).

### Platform

- POSIX terminals run interactively.
- Windows supports `--once` only (prd.md NFR).
- Non-UTF-8 terminals use `--ascii`.
- When no Orca CLI is found or none passes validation, the freshness strip shows `worker-list NOT AVAILABLE (no Orca CLI validated)` (adapter-contract.md:10); the observer does not crash.

## Voice and Tone

The voice is a careful instrument: short and literal. It names the source of every claim, and it never reassures or guesses.

| Do | Don't |
|---|---|
| `Human questions: source UNVERIFIED, 0 rows interpreted, not "no questions"` | `No questions` or `All clear` |
| `cost unavailable` | `$0` |
| `unknown (absent in source)` | `0`, `false`, `-`, a blank or `null` |
| `terminalState=released` shown raw | `done` or `complete` |
| `run` as the label for `runId` | `orchestrator` |
| `worker-reported, not questions` as the ledger title | `Action items` or `Needs you` |
| `nextAction.kind` printed verbatim | ranking it, colouring it as urgent or calling it a question |
| `STALE 52s`, with values kept `as of HH:MM:SS` | turning a stale value into `failed` or hiding it |
| `not reobserved` | `unchanged` |
| `no observed items in this source window; not proof none exist` | `Nothing here` |
| Help text: "a completed Task can still own a live terminal" | implying that a finished task means a free terminal |
| `no observed questions in this source window; not proof none exist` | `no questions`, `0 questions` or `all clear` |
| `seen, not resolved: 3` | `3 open`, `3 unresolved`, `observed open: 3` (the retired wording) |
| `seen, not resolved: 100+ (window full)` | `seen, not resolved: 100` |
| `closed by evidence: unavailable (no source)` | `resolved: 0` or `closed: 0` |
| `no read marker in source: answered questions stay listed` | implying a listed question is still waiting for an answer |
| `question read: FAILED (consumer-fenced) 3s` | `disconnected`, `offline` or `no access` |
| `[no longer in source window]` | `resolved`, `closed` or `gone` |
| `reason unknown` | a guessed reason, or a blank |

Rules:
- Labels use the source field names (`workerState`, `liveness.verdict`) wherever a field is shown.
- Words for status come from the source, never from the observer's own scale. No health name such as "healthy" or "degraded" appears anywhere.
- Numbers always carry their denominator and scope: `nextAction present: 17 of 300 collected (reported 412)`.
- No exclamation marks and no emoji.
- **[R2 as built]** One noun per list: "questions" and "workers". The gap-notice literal keeps `Human questions`; everywhere else it is "coordinator question" (F30).

## Component Patterns

Visual treatment is in DESIGN.md (`{components.*}`). This section defines behaviour.

**Header (`{components.header}`).**
- Line 1 carries the mode, scope and `as of`. Fixture mode always reads `SYNTHETIC FIXTURE <variant>, not Orca data` (rendering-rules.md:17, quoted exactly), which must not be confused with live data. The T50 marking "synthetic fixture, not live evidence" is a separate marking on each R0 render (acceptance-tests.md:44), not the header string.
- B adds `read k of N Runs since start; oldest among Runs read`. Whether every header carries that token is OQ-13 (a contradiction in the sources). **[Superseded in R2 for questions: there is no rotation set, so no `read k of N Runs since start` is shown for questions. The panel and the freshness cell say `one Run only: <runId>`. The token stays design reference for worker reads, where OQ-13 is still open.]**

**Freshness strip (`{components.freshness-strip}`).**
- One cell per source, showing collection freshness only.
- Per-row evidence age is a separate plain age, never merged into the source cell.
- When a call overruns the cycle, the strip shows `cycle overran (Ns)` (adapter-contract.md:26, T40).
- **[R2 as built]** With questions on, a cell for the question source: `coordinator questions OK 0s (one Run <runId>)` / `STALE 50s` / `FAILED (consumer-fenced)` / `not read yet`. It replaces `messages UNVERIFIED (not read)` and uses the same grammar as the worker-list cell: a name, then a state word, then an age where it has one (F07). The Run id is in the cell. The time of the last good read is not the age under FAILED or STALE; it is the panel's `list as of HH:MM:SS (last good read)` line.

**COUNTS strip (`{components.counts-strip}`).**
- Numbers and denominators only: no bars, no health name.
- Source counts (`result.counts`) are never summed with page-derived counts.
- Token priority when space runs out:
  1. `collected n / reported T`, `PARTIAL` and scope, which are never cut;
  2. source counts;
  3. source age and the `unavailable (no source)` tokens, the only tokens that may end in `>`.
- It wraps to a second line before anything is cut.

**Gap notice (`{components.gap-notice}`).**
- One line, above the ledger, in every view and at every width, until QUESTION-OBSERVATION passes and the question source succeeds in this process. **[R2 reading: it stays while the question source has not read; the panel replaces it once the source has read or failed. "Succeeds" is superseded by "has read or failed", because a failed first read is stated by the panel.]**
- It is not dismissible. It uses `{colors.warn}` plus the literal word `UNVERIFIED`, so it does not depend on colour.

**Coordinator questions panel (`{components.question-panel}`) [R2 as built; one Run only].** Shown when `--questions` is on and the question source has read or failed. It lists what the observer saw in the messages of type `question` of one named Run. It is a bounded observation, not a task list.

Lines, in the owner's order (the vertical order after the state line is PROPOSED):
1. Title `COORDINATOR QUESTIONS`.
2. `one Run only: <runId>`.
3. The state line, always first under those: `question read: OK 3s` | `question read: STALE 50s` | `question read: FAILED (consumer-fenced) 3s` | `question read: FAILED (no-active-terminal) 3s` | `question read pending`.
4. Under FAILED or STALE: `list as of HH:MM:SS (last good read)`. For the two fence codes also the sentence `this terminal does not hold the named Run; the observer never binds to a Run`, then the action line `start the observer in the terminal that holds <runId>`. The action line is the observer's inference from the error code, not an Orca message, and is marked as inferred on screen (how the mark is drawn is open, UX-OQ-16). It points at "Where it runs".
5. The counts line: `seen, not resolved: <n> | closed by evidence: unavailable (no source)`. With a full window: `seen, not resolved: 100+ (window full) | closed by evidence: unavailable (no source)`. With retention exceeded: `seen, not resolved: unknown (retention exceeded) (retained 1000)`.
6. The standing caveat, on every frame that has a count: `no read marker in source: answered questions stay listed`.
7. The disclosure, verbatim and unchanged: `bounded best effort; coverage unknown; at most 100 rows per read, not 100 questions; bursts over 100 rows between reads may be lost`. (A plain-words version, F26, is not adopted: the owner kept the sentence.)
8. One line per question, oldest first: `<age>  [no longer in source window]  <subject>  reason unknown`.
9. When the list is cut: `questions shown 7 of 20 (oldest first; 13 newer not shown; e exports all)`. The worker ledger keeps its own `workers shown 2 of 4`, so the two counters name what they count (F24).
10. Empty read: `no observed questions in this source window; not proof none exist`. If retained rows exist and the latest read returned none: `latest read returned 0 questions; the rows below are older`.
11. Window full line: `window full: older questions may be missing`. Retention line: `retention reset at HH:MM; questions observed before this start are not retained`.

Behaviour:
- **Listed, not selectable.** No cursor, no inspector. `Enter` and `Esc` do nothing on it. `m` marks worker rows only and never changes the count.
- **Seen is not resolved.** The count is never lowered by source loss, STALE, FAILED, a window shift or a restart of the read. Only explicit closure evidence could lower it, and no source records one (`closed by evidence: unavailable (no source)`). A question that left the window keeps its line with `[no longer in source window]` and stays counted.
- **Never a false "none".** An empty read is `no observed questions in this source window; not proof none exist`, never "no questions". The collapsed summary does the same (Responsive & Platform).
- **Cut.** When the list does not fit, the oldest stay (owner decision 1); newer ones are in the export only, and the cut line says so.
- **Only the subject is clipped**, so the state word `[no longer in source window]` and `reason unknown` are never cut.
- **Worker rows are unaffected.** A fenced or failed question read leaves the worker-list state and the ledger as they were (T52).
- **Per-line `reason unknown`** stays on every line, as the spec asks (rendering-rules.md); it is the same four words each time because no verified reason field exists. Folding it into one line (F38) needs the spec owner.
- **No new-question cue** exists in R2 (UX-OQ-11).
- Styles are PROPOSED, not applied (see DESIGN.md `question-panel`).

Illustration, hand-composed from the strings above at about 100 columns. It is not a render, and the vertical order after the state line is PROPOSED:

```
COORDINATOR QUESTIONS
one Run only: <runId>
question read: OK 3s
seen, not resolved: 20 | closed by evidence: unavailable (no source)
no read marker in source: answered questions stay listed
bounded best effort; coverage unknown; at most 100 rows per read, not 100 questions; bursts
over 100 rows between reads may be lost
3h  Should I rebase onto master or merge?  reason unknown
1h  [no longer in source window]  Is the schema change approved?  reason unknown
(five more lines, oldest first)
questions shown 7 of 20 (oldest first; 13 newer not shown; e exports all)
```

```
COORDINATOR QUESTIONS
one Run only: <runId>
question read: FAILED (consumer-fenced) 3s
list as of 14:02:11 (last good read)
this terminal does not hold the named Run; the observer never binds to a Run
start the observer in the terminal that holds <runId>   [inferred, not an Orca message]
seen, not resolved: 3 | closed by evidence: unavailable (no source)
no read marker in source: answered questions stay listed
```

**Ledger (`{components.ledger}`).**
- Shown in source order. The order is not re-sorted; the authoritative order for snapshot consumers is OQ-12.
- Selection is anchored to identity (source namespace + `dispatchId`), never to a row index. A refresh that reorders rows keeps the cursor on the same worker.
- If that worker disappears, the cursor row reads `selected <id> no longer in source window` until the user moves. The cursor never jumps to another worker.
- Historical rows (`terminalState` released or retained) are hidden by default, with `k historical hidden (h)` shown. Hiding them never changes the source counts. Historical evidence explicitly linked to a shown item is never hidden (rendering-rules.md:22).
- Duplicates are dropped with `k duplicate rows ignored`.
- **[R2 as built]** With questions on, the ledger is the block that is squeezed first (owner decision 2). Its row-count line reads `workers shown 2 of 4`; the footer keeps the spec's `shown x/y | collected n / reported T`, which is also about workers. Its title `worker-reported, not questions` is unchanged.
- The spec ledger has no worktree column at any width (rendering-rules.md:30). T20 (acceptance-tests.md:29) asserts the shared `resource.worktreeId` through the inspector: two sessions that share one worktree show as two rows, opening the inspector on each shows the same `resource.worktreeId`, and the session with no worktree shows `unknown (absent in source)` for it; no count divides sessions by worktrees and no `conflict` label appears for the shared worktree. PROPOSED default: the worktree is named in full in the inspector and the plain-text export only, not in the ledger row. Whether the ledger row names it at all is open (UX-OQ-8).

**Row gutter (PROPOSED).**
- Cell 1 is the selection cursor: `▸`, or `@` under `--ascii`.
- Cell 2 is the change mark `*`.
- The selected row is also drawn in reverse video (`{components.ledger-row-selected}`). The glyph alone carries the meaning when reverse video is not available.

**Inspector (`{components.inspector}`).**
- Replaces the ledger area only, not a pane; header line 1, the freshness strip and the COUNTS strip stay above the inspector fields, so a STALE or FAILED source stays visible (rendering-rules.md:13, :19).
- Fields are listed one per line, label then value. Values are wrapped by cells and never truncated.
- PROPOSED: continuation lines of a multi-line value are prefixed with a fixed indent marker (for example `  | `), in the inspector and the export, so no value line can start with a field label (adapter-contract.md:51).
- Full IDs: `dispatchId`, `taskId`, `runId`, `resource.worktreeId`, `resource.ownerDispatchId`, `resource.originDispatchId`, `projection.host.id`, `projection.workspace.id`, `projection.stage.{worker,dispatch,activity,detail}`. Stage values are labelled `worker-reported`.
- A failed poll shows its sanitized stderr here.
- An absent field reads `unknown (absent in source)`.
- The inspector shows `n unrecognised keys` for unknown source keys that were ignored (adapter-contract.md:38).
- The inspector states that caps are per observer process, so several observers multiply Orca load (adapter-contract.md:62).

**Footer (`{components.footer}`).**
- The key list for the current mode, plus `shown x/y | collected n / reported T`.
- It also shows the filter prompt while `/` is active.

**Too-small diagnostic (`{components.diagnostic}`).**
- A plain sentence: `terminal too small: need 12 rows, have N` (PROPOSED wording and number).
- Below it sit the never-dropped rows.

**Export.**
- `e` writes the export and reports the result on the status line: `exported <path>` or `export failed: <reason>` (PROPOSED wording).
- The destination path and file naming are not specified (UX-OQ-4).
- The export has the same content as the screen, with full IDs and no truncation.

## State Patterns

### State vocabulary (missing data is never zero or false)

| The brief's term | What it means | Exact rendering | Source |
|---|---|---|---|
| unknown | The source returned the record but omitted the field. | Muted literal `unknown`, plain under NO_COLOR. In the inspector: `unknown (absent in source)`. An aggregate with unknown members: `n+? (k unknown)`. | rendering-rules.md:50-51 |
| unavailable (a form of not observed) | No verified source exists for the fact. | `unavailable (no source)`, e.g. `SETTLED unavailable (no source)`, `FROZEN unavailable (no source)`, report status, acceptance, tests, human approval; also `cost unavailable`. | rendering-rules.md:52, 62-63 |
| stale | No successful poll for 3 intervals (45 s at 15 s), measured on a monotonic clock. | The freshness cell reads `STALE <age>`. Values keep their last reading with `as of HH:MM:SS`. Never turned into `failed`, and never lowers the open count. | rendering-rules.md:53 |
| partial | The page cursor still has more rows when the call cap is reached. | `PARTIAL: collected n of reported T (newest first; oldest rows not read; long-running active workers may be among them)`. Other forms: `reported T (page k)` (T comes from the last page read), `reported T1-T2 (changed during read)`, `collected n / reported T (mismatch)`, `PARTIAL (empty page k)`. When `page.total` is absent: `reported unknown` (T32). | rendering-rules.md:55, acceptance-tests.md:21 |
| not observed | The source was not read, or a row was not seen again this cycle. | `NOT POLLED` (source not yet polled); `messages UNVERIFIED (not read)`; `not reobserved` (row on an unread page); `selected <id> no longer in source window`. | rendering-rules.md:18, 23, 46 |
| failed | A poll ran and failed. | `FAILED (<exit code or timeout>) <age>`, with sanitized stderr in the inspector. A timed-out call reads `FAILED (timeout)` (T5). A response missing `result`, `result.workers` or `result.page.hasMore` reads `FAILED (shape)`, with the last good snapshot kept (T32). When the source is also stale, PROPOSED: `STALE <age>, last poll FAILED (<reason>)`. Only the source cell fails; row values never do. | rendering-rules.md:53, prd.md:181, acceptance-tests.md:21 |

### View-level states (R1)

| State | What the supervisor sees |
|---|---|
| Loading (first cycle) | Freshness `worker-list NOT POLLED` (spec). PROPOSED: header `as of not yet polled`, COUNTS `collected 0 / reported unknown`, ledger line `waiting for first worker-list poll`. No value is ever shown as 0 except the count of rows actually collected. |
| Empty | `worker-list returned 0 workers in scope=<scope>`; fixture: `no observed items in this source window; not proof none exist` (T33). |
| Partial | `PARTIAL` in the COUNTS strip (never truncated) plus the full partial sentence on the status line. |
| Stale | `STALE <age>` cell; rows keep last values; no row is removed for staleness. |
| Failed poll | `FAILED (...)` cell; last good rows kept with `as of`; retries back off up to 60 s. |
| Binary missing | `worker-list NOT AVAILABLE (no Orca CLI validated)` (adapter-contract.md:10). |
| Cycle overrun | `cycle overran (Ns)` in the freshness strip; the overrunning call is killed and reaped (adapter-contract.md:26, T40 at acceptance-tests.md:34). |
| Filter active | `filter <expr>: k of n collected` beside the unfiltered source counts. |
| Historical hidden | `k historical hidden (h)`. |
| Row order flags | A row missing both timestamps is flagged `order unknown`; a backward timestamp shows `conflict (time went back)`; an older `observedAt` never overwrites a newer one (T22, acceptance-tests.md:18). |
| Changes since mark | `changed since HH:MM (k)` and `*` on changed rows; restart shows a new-baseline notice. |
| Fixture | Header line 1 reads `SYNTHETIC FIXTURE <variant>, not Orca data` on every frame (rendering-rules.md:17). Each R0 render also carries the separate T50 marking "synthetic fixture, not live evidence" (acceptance-tests.md:44). |

### Question-source states (R2 as built)

The state words are the vocabulary above (stale, failed, unknown, unavailable) applied to the question source. In every row the retained questions stay and the count `seen, not resolved` is never lowered by the state (F12).

| State | State line (first line of the panel) | What else shows |
|---|---|---|
| Questions off, or QUESTION-OBSERVATION not passed | none (no panel) | The gap notice and `messages UNVERIFIED (not read)`, byte-identical to R1 (T47). |
| Not read yet | `question read pending` | The gap notice stays (the source has not read). Header cell `not read yet`. Counts line: not in the owner's list; PROPOSED `seen, not resolved: unknown (no question read yet)`. |
| OK | `question read: OK 3s` | The counts line, the standing caveat, the disclosure, the question lines. Header cell `coordinator questions OK 0s (one Run <runId>)`. |
| OK, empty read, nothing retained | `question read: OK 3s` | `no observed questions in this source window; not proof none exist`. |
| OK, empty read, rows retained | `question read: OK 3s` | `latest read returned 0 questions; the rows below are older`. The older rows carry `[no longer in source window]`. |
| OK, window full (exactly 100 rows) | `question read: OK 3s` | Counts `seen, not resolved: 100+ (window full)` and the line `window full: older questions may be missing`. A 99-row read shows neither. |
| STALE (45 s without a good read, monotonic clock) | `question read: STALE 50s` | `list as of HH:MM:SS (last good read)`. Retained questions stay with the ages they had. Header cell `STALE 50s`. |
| FAILED, consumer-fenced | `question read: FAILED (consumer-fenced) 3s` | `list as of HH:MM:SS (last good read)`, the fence sentence, the inferred action line. The worker-list cell is unchanged (T52). Header cell `FAILED (consumer-fenced)`. |
| FAILED, no-active-terminal | `question read: FAILED (no-active-terminal) 3s` | The same lines as consumer-fenced. |
| FAILED on the first read | the FAILED line | There is no good read, so `list as of` has no time to show; PROPOSED: that line is left out and the counts line reads as for "Not read yet". |
| Question left the window | (no change) | Its line reads `[no longer in source window]`. It stays counted. |
| Retention exceeded (more than 1,000 retained) | (no change) | `seen, not resolved: unknown (retention exceeded) (retained 1000)`. The oldest are evicted and the count is never lowered. |
| Observer restarted | (no change) | `retention reset at HH:MM; questions observed before this start are not retained`. Questions Orca no longer returns are gone from this process, so the count starts again from what the first read returns (F37). |
| List cut | (no change) | `questions shown 7 of 20 (oldest first; 13 newer not shown; e exports all)`. |
| Panel does not fit | none | The one summary line (Responsive & Platform, "R2 panel height order"). |

### Truncation marker rules

- List cells cut by display-cell width and end with a visible `>` (rendering-rules.md:24). The design package's prototype uses `…` (ASCII `~`, canvas.py:23); the spec's `>` wins for the product.
- Never truncated: `collected n / reported T`, `PARTIAL`, scope, any value in the inspector, any value in the export.
- `x/y shown` on any list that does not fit; `+N more` counts only rows not shown and never the selected row.
- Cuts never split a multi-cell character; a wide character that does not fit is replaced by `>`.

## Interaction Primitives

### Keyboard model (spec, rendering-rules.md:20)

| Key | Ledger (screen 1) | Inspector (screen 2) | Filter input |
|---|---|---|---|
| Up / Down, `k` / `j` | move the selection one worker row **[R2: moves workers only; the questions have no cursor]** | PROPOSED: move the inspector view one line when it is taller than the screen | `j`/`k` are typed as text |
| `Enter` | open the inspector for the selected row | none | apply the filter and return to the ledger |
| `Esc` | clear an active filter (PROPOSED) | back to the ledger, same selection | cancel the edit, keeping the previous filter (PROPOSED) |
| `/` | open the filter input in the footer | none | typed as text |
| `h` | show or hide historical rows | none | typed as text |
| `m` | mark a look for worker rows: start of the `changed since` window. **[R2: questions are not marked, and `m` never changes the `seen, not resolved` count. The original design moved a question to `marked looked`; that is design reference / R3.]** | same as ledger | typed as text |
| `e` | write an export **[R2: it holds every question, including those the screen does not show]** | same as ledger | typed as text |
| `q` | quit and restore the terminal | quit | typed as text |
| `Backspace` | none | none | delete one character |
| `Ctrl-C` | quit and restore the terminal (SIGINT) | same | same |

- There is no `r` key; refresh is the fixed 15 s cycle. There is no help key, no mouse, no themes and no animation. No key maps to an Orca call (T3).
- PROPOSED: help text is the `superclaude observe --help` output; it carries "a completed Task can still own a live terminal" (rendering-rules.md:52) and the per-observer-process caps sentence (adapter-contract.md:62).
- Keys not in the table do nothing and show nothing.

### Focus

- There is one focus at a time, and it is never split across panes. No per-panel scrolling and no multi-pane focus (rendering-rules.md:13).
- Focus is the ledger list, or the inspector, or the filter input.
- The footer always shows which mode is active by listing only that mode's keys (PROPOSED).
- A refresh never moves focus or selection. It never closes the inspector or the filter input, and it never clears the filter text being typed.
- B and later: moving between B and the A ledger needs a key the spec does not define (UX-OQ-3). **[R2: does not arise, because R2 has no B view to move to; UX-OQ-3 stays open for R3.]**
- **[R2 as built]** The questions panel never takes focus. Focus stays on the worker ledger, the inspector or the filter input. The footer key line should read "move workers" for the movement keys, and "m mark rows" is the proposed wording for `m` (F14, open as UX-OQ-12).

### The key-reader spike (R0 gate, stack.md:22-23)

The first task is a spike: Rich Live plus a POSIX standard-library key reader (termios, tty, select). If it fails, the stack switches to Textual; both are never built. The spec gives no pass/fail criteria. The UX needs these **PROPOSED** criteria:

1. Every key in the table above is recognised, including Esc on its own, distinguished from arrow-key escape sequences within a short timeout.
2. Typing into the filter is not lost or reordered while a 15 s refresh redraws.
3. Selection stays on the same identity across a refresh that reorders rows.
4. The terminal is restored (echo, cursor, alternate screen) on `q`, Ctrl-C, SIGTERM and an unhandled exception.
5. A resize redraws within one cycle with `cell_len <= W` on every line.
6. No visible flicker or leftover characters after a redraw at 160, 116 and 80 columns.

If Textual replaces Rich, this document's keyboard, focus and state rules stay unchanged.

### Changes since last look

- The first observation in a process is the baseline. A restart says that a new baseline was taken.
- `m` records a mark in memory only.
- After a mark, added, removed or changed rows show `*` and are counted in `changed since HH:MM (k)`. "Changed" means a change in `stage`, `nextAction.kind` or `liveness.verdict`; which `stage` subfield counts is OQ-15.
- Rows on unread pages read `not reobserved`.
- **[R2 as built]** Change marks cover worker rows only. A coordinator question gets no `*` and no "new since" count. A new question adds a line at the newest end of the list and raises the count; when the list is cut (owner decision 1: oldest stay) the new line is among the ones not shown. Whether a cue such as `k new since HH:MM` is wanted is open (UX-OQ-11).

### Motion

- Nothing blinks, scrolls by itself or animates. SGR 5 and 6 are never emitted (T28).
- A refresh repaints in place; there are no transitions.
- The only change between frames is new data, plus the `*` marks the supervisor asked for with `m`.

## Untrusted Text and Identifiers

All text that comes from Orca or a worker is untrusted, including stage detail, outcome, kind, IDs and stderr.

- **Sanitized before render** (adapter sanitizer). The sanitizer removes:
  - CSI and OSC sequences, both terminated and unterminated;
  - C1 control characters;
  - bare C0 control characters, except newline in the inspector;
  - Unicode format characters (category Cf).

  The same sanitized string feeds the screen and the export.
- **Shown literally.** Text is never parsed as Rich markup (T44, T29). `[bold]x[/bold]` from a worker prints as those exact characters.
- **Labelled as reported.** Worker-supplied text carries the label `worker-reported`. It is never restated as the observer's own claim.
- **Never interpreted.** `nextAction.kind` is shown verbatim. It may be used as a labelled local filter, never as a ranking, a colour or an action.
- **Full IDs in the selected detail.** The ledger may cut an ID with `>`. The inspector and the export always show every ID in full, wrapped by cells.
- **No bodies or secrets.** R1 shows and exports no message bodies, prompts, file contents or credentials (snapshot-export-schema.md:11).
- **Question subjects (R2 as built).** The subject on a question line is sanitized message text, shown literally and clipped by cells. It was written by whatever sent the message to the Run's mailbox, and it can imitate a state word. The panel puts the state word first in brackets (`[no longer in source window]`) so a subject cannot push it off the line. The panel carries no `worker-reported` label on the subject: the owner's disclosure sentence is fixed and unchanged, and a label would add words to it. Whether to label the subject's source is open (UX-OQ-13, F31).

### The "source UNVERIFIED" notice

`Human questions: source UNVERIFIED, 0 rows interpreted, not "no questions"` sits above the ledger in every view and at every width, until QUESTION-OBSERVATION passes and the question source has succeeded in this process.

B's live question-panel block reads `Question rows: source UNVERIFIED. 0 rows interpreted. This is not "no questions".` Any other question area uses the shared core `source UNVERIFIED, 0 rows interpreted, not "no questions"` (rendering-rules.md:31).

The notice shows no number, and nothing is derived from `result.count`.

**[R2 as built]** With `--questions` on and QUESTION-OBSERVATION passed, the notice stays while the question source has not read; the `COORDINATOR QUESTIONS` panel replaces it once the source has read or failed. With questions off, or before the gate passes, the notice is exactly as written above (T47).

## Accessibility Floor

- **Meaning never depends on colour alone.**
  - Every state has a word: `STALE`, `FAILED`, `PARTIAL`, `UNVERIFIED`, `unknown`, `unavailable`.
  - Every mark has a glyph: `*` for changed, `▸`/`@` for the selection, `>` for a cut.
  - Colour only repeats what the text already says.
- **NO_COLOR.**
  - `NO_COLOR=1` and `NO_COLOR=yes` turn off all SGR colour. The labels, glyphs and layout are unchanged.
  - Muted `unknown` becomes plain `unknown`.
- **ASCII.** `--ascii` replaces box drawing with `+ - |` and every non-ASCII glyph with its fallback (DESIGN.md glyph table). The ASCII screen carries the same information.
- **Contrast.** The palette's text colours on the dark background range from 7.63:1 (`bad`) to 14.56:1 (`ink`) (design package QA.md:13). Values above 4.5:1 meet WCAG AA for normal text. These ratios are the design package's figures and have not been re-measured (UNVERIFIED). The terminal's own theme may override colours.
- **No motion.** No blinking (no SGR 5/6, T28), no animation and no auto-scroll.
- **Keyboard only.** Everything works from the keyboard, and no mouse is needed or used.
- **Screen readers.** The export (`--once`) is plain text with no ESC bytes (T27), so it can be read by assistive tools. The live screen makes no screen-reader promise.
- **Text size.** Text size is the terminal's own; the layout adapts by width bands only.
- **[R2 update, F42; as reviewed at commit 3cde36331, the build is being changed.]** Four of the bullets above describe the design, not the build:
  - The contrast ratios and the muted `unknown` belong to the DESIGN.md palette. The reviewed build applied no colour (an empty palette), so every state is carried by its word and `NO_COLOR` output equals colour output. Styles are PROPOSED, not applied. Whether the unstyled build is intended for R1 and R2 is open (UX-OQ-14).
  - The `▸` / `@` selection glyph applies to worker rows. Questions are not selectable and have no glyph.
  - In `--ascii`, non-ASCII characters in question lines are shown as `?`, as in ledger cells (F44). A replaced character can look like a literal `?`, and questions often end with one; the full text is in the export.
  - Screen readers: the live screen makes no promise. The path for assistive tools is the plain-text export (`--once` or `e`), which also holds the questions the screen does not show. The panel reads in a linear order: title, Run, state, count, caveats, then lines.

## Inspiration & Anti-patterns

**Inspiration.** The only visual reference is the design package. It is used by reference to its text exports only:
- `exports/{160,116,80}/signal-bridge.txt`, `decision-desk.txt` and `agent-focus/exports/*/attention-ledger.txt`;
- the `.ascii.txt` variants;
- `DESIGN-CONTRACT.md`;
- `concepts.md`.

That package lives at `IronClaude/issue-409-mvp/.dev/design/orca-observer-20261106/`. Its prototype is a visual reference only, and no code is imported (X-001). TUIBBS is background only, and no code is copied from it (AGPL-3.0).

**Anti-patterns (each is ruled out by a source):**

| Anti-pattern | Why it is out |
|---|---|
| Health score, traffic-light summary, "all green" | No health name in COUNTS (rendering-rules.md:19) |
| Bars or gauges from counts, tokens or activity | SIGNALS bars are a non-goal; no progress bar from tokens (rendering-rules.md:62) |
| `no questions` or an empty question panel when the source is unread | Gap notice rule (T33) |
| Treating `nextAction.kind` as a to-do or question list | Verbatim-only rule (rendering-rules.md:30) |
| Auto-switching to B when questions appear | Start-up-only view choice (INV-021, T45). **[R2: there is no B to switch to; the rule stays as design reference for R3.]** |
| `no questions`, `0 questions` or a bare `0` for an empty or failed question read, including in the one-line summary | Never-false-none rule (T33); the empty read says `not proof none exist` |
| A bare `100` for a full window, or a bare number in the collapsed summary | Owner decision 4: `100+ (window full)` |
| Showing a listed question as answered, resolved or closed | The source has no read marker (`no read marker in source: answered questions stay listed`) |
| Binding the observer to a Run (`run-use`) to make a fenced read work | Forbidden set (adapter-contract.md) |
| A refresh key, or any key that calls Orca | No `r` key; T3 |
| Reply, retry, kill or approve buttons in R1 | Read-only (owner decision 3) |
| Silently dropping stale or vanished rows | `not reobserved`, `selected <id> no longer in source window` |
| Blinking or pulsing alerts | T28 |

## Key Flows

The protagonist is **the supervisor**, the PRD persona: one human watching 5-10 orchestrators and 50-100 sessions. The sources give no further persona detail, so none is invented. Journey IDs are from prd.md:65-69.

### UJ-1 Fleet glance (R1)

1. The supervisor runs the observer command (name: OQ-3) in a terminal of 160 columns.
2. Screen 1 opens on the R1 ledger, which is the start-up default.
3. They read header line 1 for mode and scope, then the freshness strip: `worker-list OK 4s`, `messages UNVERIFIED (not read)`.
4. They read the COUNTS strip: `collected 87 / reported 87`, `source counts: active ...`.
5. They read the gap notice and know that question data is not being read.
6. **Climax:** in one look they see how many workers the source reports, how fresh that is, and what the screen cannot tell them.

**Failure path.** The poll times out three times in a row:
- Each timed-out call shows `FAILED (timeout) <age>` in the freshness cell, and the cycle still ends within the 15 s budget (T5).
- After 3 intervals with no successful poll the source is also stale. PROPOSED: the cell then reads `STALE 52s, last poll FAILED (timeout)`, so both facts show.
- Rows keep their last values with `as of HH:MM:SS`. No row value turns into `failed`, and no row disappears (rendering-rules.md:53).
- If `page.hasMore` is still true at the 5-call cap, `PARTIAL: collected 500 of reported 612` appears (T4; the reported total here is an example) and is never cut.

**UJ-1 as written is the questions-off path** (steps 3 and 5 name `messages UNVERIFIED (not read)` and the gap notice). **Questions-on variant [R2 as built]:**
- Step 3 reads `worker-list OK 4s` and `coordinator questions OK 0s (one Run <runId>)` in place of `messages UNVERIFIED (not read)`.
- Step 5: the `COORDINATOR QUESTIONS` panel stands where the gap notice stood. Its first line is the state of the read, then `seen, not resolved: <n>`, then the caveats. Until the first question read has returned, both the gap notice and `question read pending` show.
- **Climax:** in one look they also see how many coordinator questions the observer has seen on one Run, how fresh that read is, and that the count is a bounded observation.
- **Failure path:** the question read fails or the observer is in the wrong terminal; see UJ-7. If the machine is not the place that holds the Run, see "Where it runs".

### UJ-2 What changed (R1)

1. The supervisor presses `m`. The status line reads `changed since 14:02 (0)`.
2. They work elsewhere. The 15 s cycle keeps running.
3. They come back. Rows whose `nextAction.kind`, `liveness.verdict` or `stage` changed carry `*`, and the line reads `changed since 14:02 (5)`.
4. **Climax:** they see the five changed rows without re-reading 87.

**Failure path.**
- Some pages were not read this cycle: their rows read `not reobserved`, not "unchanged".
- The observer restarted: the mark is gone, and the screen says that a new baseline was taken.

### UJ-3 Inspect (R1)

1. The supervisor moves with `j`/`k` to a row whose `nextAction.kind` reads `unknown`.
2. They press `Enter`. The inspector shows every field.
3. They read the full `dispatchId`, `taskId`, `runId` and `resource.worktreeId`, and `projection.stage.*` labelled `worker-reported`.
4. **Climax:** they can copy the full IDs into an Orca command they run themselves, outside the observer.
5. `Esc` returns to the ledger on the same worker.

**Failure path.** While the inspector is open, the worker leaves the source window:
- The inspector keeps its last values.
- Back in the ledger, the cursor row reads `selected <id> no longer in source window` and does not jump.

### UJ-4 Export (R1)

1. The supervisor presses `e`, or runs the command with `--once` (on Windows, the only mode).
2. The observer writes the plain-text view. Missing values read `unknown`, exactly as on screen (rendering-rules.md:51), with full IDs and no ESC bytes. The string `UNKNOWN` belongs only to the JSON snapshot (snapshot-export-schema.md:10). (The JSON snapshot does not depend on this key: `export(view)` writes it on every cycle, FR-16.)
3. **Climax:** the status line confirms the export (PROPOSED: `exported <path>`). The file matches what was on screen (T48).

**Failure path.** The write fails: the status line reads `export failed: <reason>` (PROPOSED), and the screen is unchanged. The destination path is UX-OQ-4.

### UJ-5 Find the oldest question (B, then C; gated)

> **[Design reference / R3 (QUESTION-LINK), not built in R2. Superseded in R2 by UJ-6 (a question arrives) and UJ-7 (the read fails).]** The original text below is kept as written. Steps 3 and 4 (select, inspector, RETAIN CONTEXT, `marked looked`) and step 5 (Decision Desk) need a selectable question and QUESTION-LINK. In R2 the questions are listed, not selectable, and `m` marks worker rows only. What R2 does keep of this journey is step 1's start-up, the oldest-first order (step 2) and the "seen is not resolved" count; the oldest question is the first line of the list.

1. After QUESTION-OBSERVATION, the supervisor starts the observer. The question source succeeds, so start-up opens B.
2. `OPEN HUMAN QUESTIONS` lists questions oldest first, and `SEEN IS NOT RESOLVED` shows the open count.
3. They select the oldest question and press `Enter` for its inspector, including RETAIN CONTEXT.
4. They press `m`, which moves it to `marked looked`; the open count stays the same. **[Design reference / R3: in R2, `m` marks worker rows only and no question is moved to `marked looked`.]**
5. After QUESTION-LINK, the Decision Desk (C) shows the affected sessions with worker-list evidence.
6. **Climax:** they know who asked, how long ago, and which sessions are affected, without the observer replying for them.

**Failure path.** The question source fails at start-up:
- The observer opens on the R1 ledger with the gap notice and stays there for the session (INV-021).
- Open questions are never lowered by source loss; each reads `open, closure source unavailable`. **[R2: the count is still never lowered; the per-line words `open, closure source unavailable` are superseded in R2 by the counts line's `closed by evidence: unavailable (no source)`. See "Spec text the R2 panel does not render".]**

### UJ-6 A coordinator question arrives (R2 as built)

The protagonist is the supervisor. The observer runs with `--questions` on, in a place that holds the named Run (see "Where it runs").

1. The panel reads `question read: OK 3s` and `seen, not resolved: 4 | closed by evidence: unavailable (no source)`.
2. A worker sends a question to the Run. At the next 15 s cycle the read returns it. The count becomes 5 and a new line appears at the newest end of the list.
3. The supervisor glances at the count and the last line: its age is the smallest on the list.
4. **Climax:** they know a coordinator question exists in the source window, how long it has waited, and that this is a bounded observation: `no read marker in source: answered questions stay listed`, and the disclosure says the read is best effort. They act outside the observer; no key in it replies.

**Failure path: the list is longer than the screen.**
- The list is cut and says so: `questions shown 7 of 20 (oldest first; 13 newer not shown; e exports all)`. The new question is among the 13 not shown (owner decision 1), but the count and the "newer not shown" number have gone up.
- The supervisor presses `e`; the export holds all 20, with their full ids.
- If the read returned exactly 100 rows the counts line reads `100+ (window full)` and `window full: older questions may be missing`.
- If someone answered a question elsewhere, it is still listed: the source has no read marker.
- No cue marks the new line (UX-OQ-11).

### UJ-7 The question read fails, goes stale or restarts (R2 as built)

1. The supervisor starts the observer with `--questions` in a terminal that does not hold the named Run (or holds no Run). This is the likely first screen for an observer started in a separate terminal (Q-1 FAIL), not an edge case.
2. The panel reads `question read: FAILED (consumer-fenced) 3s`, or `FAILED (no-active-terminal) 3s`. There is no list yet. The sentence reads `this terminal does not hold the named Run; the observer never binds to a Run`, followed by the action line `start the observer in the terminal that holds <runId>` (inferred, not an Orca message).
3. The worker ledger is unaffected: `worker-list OK 4s`.
4. **Climax:** the screen says which thing is wrong (this terminal is not the Run's holder) and the one action that fixes it, which the supervisor takes outside the observer: restart it where the Run is held (UX-OQ-9).

**Variants.**
- After a good read, the read fails: the list stays, with `list as of HH:MM:SS (last good read)`, and `seen, not resolved` does not fall.
- No good read for 45 s without an error: `question read: STALE 50s`, same `list as of` line, retained questions kept.
- The observer is restarted: `retention reset at HH:MM; questions observed before this start are not retained`. Questions Orca no longer returns are gone; the count restarts from what the first read returns.
- A question leaves the source window: it keeps its line as `[no longer in source window]` and stays counted.

### R0 owner review (DIRECTION-SELECTED walkthrough, prd.md:463)

1. The reviewer runs fixture replay.
2. They step through A, B and C at 160, 116 and 80 columns, each beside its degraded variants (stale, partial, empty, failed). Every frame's header reads `SYNTHETIC FIXTURE <variant>, not Orca data` (rendering-rules.md:17), and every render carries the T50 marking "synthetic fixture, not live evidence" (acceptance-tests.md:44).
3. **Climax:** the owner records a direction selection. Where that record lives is OQ-1.

**Failure path.** The key-reader spike fails its criteria: the stack switches to Textual before R1 starts, and this document is unchanged.

**[Two B shapes exist (F45).]** Fixture B (one block per question with `NN MIN` and `Affected:`, in the two-column Attention Ledger) is the design reference the owner compares in this walkthrough, and it stays. The live R2 panel (one line per question, stacked) is the R2 contract.

## Future Stage: Write-back (not R1)

**R1 has no controls.** No key, button, rail or menu in R0, R1, B or C sends anything to Orca. The snapshot carries no write-back path. rendering-rules.md lists no operational controls. This section is design intent only, from write-back-future-stage.md, and nothing in it is built.

**Boundary.** Write-back needs two things first:
- an explicit boundary change on issue 409 (OQ-11);
- a TUIBBS FR-X-13 amendment.

It would live in a later Go TUIBBS screen, not in this Python observer and not in the snapshot. Whether a Go screen may read the snapshot first needs a licence opinion (OQ-9). Whether TUIBBS becomes the staff platform is OQ-10.

**What the observer may do before then.** Decision Desk may show the exact `orca orchestration reply` command as plain text for the supervisor to copy and run themselves. Showing it never runs it.

**Future interaction outline (not specified, not approved):**
- The reply is composed in the future screen, never inline in the observer.
- Delivery shows as `delivered`, `pending` or `unknown`. `No reply observed is not delivery failure`.
- How Orca authenticates a `reply` sender is an open question (write-back-future-stage.md:50).

Until the boundary change is approved, this section adds no requirement to any release.

## Open Questions

Every question is carried open. None is resolved here (owner decision 6).

### Raised by this UX spec

| ID | Question | Why it matters to the UX |
|---|---|---|
| UX-OQ-1 | The R1 composition matches neither the PLAN.md:43 cockpit (owner rows, intervention rail, change ribbon) nor the built `layouts/group_a.py` layout that every Signal Bridge export shows. Is it the confirmed R1 look? | It decides what screen 1 looks like. This document follows the spec composition. |
| UX-OQ-2 | The 44-row contract versus the exports: 160-column exports are 48 rows, and 116/80-column exports are 42; the design plan's ranges are 44-52 (wide) and 36-44 (compact) (PLAN.md:57). What is the minimum height, and what is the drop order? (part of OQ-14) | The R1 44-row budget, the 12-row minimum and the shrink order are PROPOSED. |
| UX-OQ-3 | Which key moves between B and A's ledger ("one key away")? The spec's key list has none. | B is not navigable as specified. **[R2: does not arise; no B view is built. Stays open for R3.]** |
| UX-OQ-4 | The destination path and file naming of the `e` / `--once` text export and of the per-cycle JSON snapshot, and the wording of the confirmation and failure messages | The `e` feedback is PROPOSED and the text export path is not specified. For the snapshot, snapshot-export-schema.md:16 sets the path by a PROPOSED `--snapshot PATH` option whose default is the per-user state directory `~/.local/state/superclaude/observe/`; the file is created owner-only (0600) and replaced atomically each live cycle. The destination stays open. |
| UX-OQ-5 | Truncation glyph: the spec's `>` versus the prototype's `…` / `~` | This document uses `>`, per the spec. |
| UX-OQ-6 | The key-reader spike has no pass/fail criteria in the spec | The six criteria under Interaction Primitives are PROPOSED. |
| UX-OQ-7 | The colour palette exists only in the prototype (canvas.py:7). The spec defines no colours. | DESIGN.md adopts the prototype palette; the owner should confirm it. |
| UX-OQ-8 | T20 (acceptance-tests.md:29) asserts the shared `resource.worktreeId` through the inspector, and the spec ledger has no worktree column (rendering-rules.md:30). Should the ledger row name the worktree at all, and if so where and how at each width? | Adding a column changes every width budget. PROPOSED default: inspector and export only; the ledger row does not name it. |
| UX-OQ-9 | **Where does the observer run?** (F10, F17; see "Where it runs".) Place 1 (the coordinator's own terminal) is untested; place 2 (a background child plus a viewer pane) is untested and its viewer is not built; place 3 (its own terminal and its own Run) is the only one tested. PROPOSED recommendation: 1 for a quick start, 3 if questions can be routed to the observer's Run. Can questions be addressed to a Run of the observer's own (`send --to run:<observer run>`)? | Decides the first screen every supervisor sees. Started in the wrong place, the panel is FAILED (UJ-7). |
| UX-OQ-10 | With the questions winning on a short terminal, how far may the worker ledger shrink, and may it reach zero rows? (F22.) The R1 12-row minimum and the 3-row comfort no longer hold with questions on. | Sets the lowest height at which the ledger still shows a row. |
| UX-OQ-11 | Does the owner want a new-question cue, for example `k new since HH:MM`? (F09.) R2 has none, and with the oldest-stay cut the newest question is the first one off screen. | Without a cue a new question is visible only as a changed count. |
| UX-OQ-12 | Should the header also say `questions: one Run only <runId>` and the panel say "questions from other Runs are not read" (F16)? Should the footer read "move workers" and "m mark rows" (F14)? Should each question line carry a short id (F19)? | The header and COUNTS strip describe workers of every Run in scope; the panel describes one Run. |
| UX-OQ-13 | Should the question subject carry a label of its source (F31)? The disclosure sentence is unchanged, so R2 adds none. | Subject text is written by whatever sent the message. |
| UX-OQ-14 | Is the unstyled R1/R2 build intentional (F28)? DESIGN.md says "styles PROPOSED, not applied". | Decides whether the `question-panel` colour roles are built. |
| UX-OQ-15 | What does the collapsed summary's count text say for 1 to 99 questions? The owner gave the forms for 0, 100+ and retention exceeded. PROPOSED `<n> (source window only)`. | The summary must never be a bare number. |
| UX-OQ-16 | How is the "inferred" mark on the action line drawn (`start the observer in the terminal that holds <runId>`)? | The owner asked that it be marked inferred, not an Orca message. |

### Carried from the PRD and spec (verbatim IDs, prd.md:414-453)

- OQ-1: DIRECTION-SELECTED, and where the selection record lives.
- OQ-2: the production-integration reading.
- OQ-3: the final command name; `superclaude observe` is recommended.
- OQ-4: the fallback date for QUESTION-OBSERVATION.
- OQ-5: permission for sample capture.
- OQ-6: message-content exposure.
- OQ-7: what identifies a human question.
- OQ-8: the multi-observer restriction.
- OQ-9: a licence opinion before a Go screen reads the snapshot.
- OQ-10: whether TUIBBS becomes the staff platform.
- OQ-11: whether the write-back boundary change is approved.
- OQ-12: the authoritative row order for snapshot consumers.
- OQ-13: whether `read k of N Runs since start` goes in B's header only or in every header (CONTRADICTION). **[Re-scoped in R2: for questions there is no rotation set, so the token is not shown for messages (rendering-rules.md); it stays open for worker reads.]**
- OQ-14: A's width matrix, B's coordinates, and C's 44-row contract.
- OQ-15: which `projection.stage.*` subfield drives change detection, and whether stage.detail/activity may enter the snapshot.
- Spec extras:
  - which of B or C is the default view after QUESTION-LINK (rendering-rules.md:87; OI-4, OI-9);
  - how Orca authenticates a `reply` sender (write-back-future-stage.md:50).
- Open items that touch the UX:
  - OI-6: no test exists for `selected <id> no longer in source window`, and the snapshot schema test ID is unassigned;
  - OI-7: the AC 11 design images have no requirement;
  - OI-12: `projection.evidence.lastObservedAt` versus `evidence.lastObservedAt` for the evidence age.
