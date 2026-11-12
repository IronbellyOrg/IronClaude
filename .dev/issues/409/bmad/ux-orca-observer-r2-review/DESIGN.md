---
name: Orca Observer
description: Visual identity for the read-only Orca terminal observer (IronClaude issue 409)
status: draft
created: 2026-11-08
updated: 2026-11-08
colors:
  bg: '#101820'
  ink: '#e1e9ee'
  muted: '#a5b6c2'
  line: '#526c80'
  accent: '#70cde2'
  warn: '#fab219'
  bad: '#f08d96'
  good: '#8bd7af'
  frozen: '#c2adf2'
typography:
  body:
    fontFamily: { note: 'terminal monospace; the terminal owns the font' }
    fontWeight: 400
    lineHeight: { note: '1 terminal row' }
  strong:
    fontFamily: { note: 'terminal monospace' }
    fontWeight: 700
  muted:
    fontFamily: { note: 'terminal monospace; colour {colors.muted}, never SGR 2 faint' }
    fontWeight: 400
rounded:
  DEFAULT: { note: 'light panel: rounded corners and light edges; --ascii gives + - |' }
  sm: { note: 'heavy square panel; --ascii gives + - |' }
spacing:
  '1': '1ch'
  '2': '2ch'
  gutter: '2ch'
  column-gap: '1ch'
  frame: '1ch'
  row: { note: '1 terminal row; vertical spacing is counted in rows' }
components:
  header:
    textColor: '{colors.ink}'
    titleColor: '{colors.accent}'
    titleWeight: '{typography.strong.fontWeight}'
  fixture-badge:
    textColor: '{colors.warn}'
    fontWeight: '{typography.strong.fontWeight}'
  freshness-strip:
    textColor: '{colors.muted}'
    okColor: '{colors.ink}'
    staleColor: '{colors.warn}'
    failedColor: '{colors.bad}'
    notPolledColor: '{colors.muted}'
    unverifiedColor: '{colors.warn}'
  counts-strip:
    labelColor: '{colors.muted}'
    valueColor: '{colors.ink}'
    partialColor: '{colors.warn}'
    unavailableColor: '{colors.muted}'
  gap-notice:
    textColor: '{colors.warn}'
    fontWeight: '{typography.strong.fontWeight}'
  status-line:
    textColor: '{colors.muted}'
    changedColor: '{colors.accent}'
  ledger:
    borderColor: '{colors.line}'
    shape: '{rounded.DEFAULT}'
    titleColor: '{colors.ink}'
    titleWeight: '{typography.strong.fontWeight}'
    headerColor: '{colors.muted}'
    columnGap: '{spacing.column-gap}'
    gutter: '{spacing.gutter}'
  ledger-row:
    textColor: '{colors.ink}'
    unknownColor: '{colors.muted}'
    ageColor: '{colors.muted}'
  ledger-row-selected:
    cursorColor: '{colors.accent}'
    note: 'reverse video (SGR 7) across the row; cursor glyph in gutter cell 1 (PROPOSED)'
  change-mark:
    textColor: '{colors.accent}'
  inspector:
    labelColor: '{colors.muted}'
    valueColor: '{colors.ink}'
    reportedLabelColor: '{colors.warn}'
    unknownColor: '{colors.muted}'
    padding: '{spacing.2}'
  footer:
    textColor: '{colors.muted}'
    ruleColor: '{colors.line}'
    keyColor: '{colors.ink}'
  diagnostic:
    textColor: '{colors.warn}'
    fontWeight: '{typography.strong.fontWeight}'
  fixture-state-marks:
    settledColor: '{colors.good}'
    frozenColor: '{colors.frozen}'
---

# Orca Observer: Design Spine

## Brand & Style

This is a quiet instrument panel for a dark terminal. The design package asks for "strong framed hierarchy, fine dim rules, quiet white values, amber attention and labeled semantic markers" (design package `DESIGN-CONTRACT.md:14`). Values stay neutral.

Colour marks state and attention, but it never carries meaning on its own. Every coloured element also has a word or a glyph (EXPERIENCE.md, "Accessibility Floor"). There is no animation, gradient, ornament or decorative glyph.

The palette comes from the design package prototype (`canvas.py:7`). The spec defines no visual tokens, so adopting this palette is open for owner confirmation (EXPERIENCE.md UX-OQ-7). The prototype is a visual reference only; no code is taken from it.

## Colors

The observer draws on the terminal's own background. `{colors.bg}` (#101820) is the background the prototype was designed and contrast-checked against.

PROPOSED: the observer does not paint the background, so a light terminal theme may lower contrast. The prototype's `panel` fill (#16232e, `canvas.py:7`) is not adopted, because R1 has no filled panels.

| Token | Hex | Used for | Never used for |
|---|---|---|---|
| `{colors.ink}` | #e1e9ee | Every source value, ledger rows, inspector values | State emphasis |
| `{colors.muted}` | #a5b6c2 | Labels, column headers, ages, footer, `unknown`, `unavailable (no source)`, `NOT POLLED` | Any known value |
| `{colors.line}` | #526c80 | Panel borders and rules | Text |
| `{colors.accent}` | #70cde2 | Header title, selection cursor, change mark, `changed since` count | A worker's status |
| `{colors.warn}` | #fab219 | `STALE`, `PARTIAL`, `UNVERIFIED`, the gap notice, the fixture header `SYNTHETIC FIXTURE <variant>, not Orca data` (rendering-rules.md:17), the separate T50 render marking `synthetic fixture, not live evidence` (acceptance-tests.md:44), the `worker-reported` label, the too-small diagnostic | Failure |
| `{colors.bad}` | #f08d96 | `FAILED (...)` source cells only | Stale or frozen states, worker outcomes |
| `{colors.good}` | #8bd7af | Fixture-only `SETTLED` marks | Any live value in R1 |
| `{colors.frozen}` | #c2adf2 | Fixture-only `FROZEN` marks | Any live value in R1 |

Raw worker fields stay `{colors.ink}` whatever their value. This covers `workerState`, `dispatchStatus`, `terminalState`, `projection.outcome`, `nextAction.kind` and `liveness.verdict`. Their full vocabularies are UNVERIFIED, so the observer must not colour them as good or bad.

Contrast against `{colors.bg}` is taken from design package `QA.md:13`. It was not re-measured here, so it is UNVERIFIED.

| Token | Ratio |
|---|---|
| ink | 14.56:1 |
| muted | 8.58:1 |
| accent | 9.82:1 |
| warn | 9.75:1 |
| bad | 7.63:1 |
| good | 10.60:1 |
| frozen | 8.99:1 |

With `NO_COLOR` set to a non-empty value, no colour SGR is emitted. Every token falls back to the terminal default, and the words and glyphs carry the meaning.

## Typography

The observer uses one face, the terminal's monospace font, and never sets it.
- `{typography.body}` (regular) is used for all values.
- `{typography.strong}` (bold, SGR 1) is used for the header title, panel titles, the gap notice, the fixture badge and the too-small diagnostic.
- `{typography.muted}` is a colour role, not a weight. Faint (SGR 2) is never emitted.
- Italic, underline, blink (SGR 5 and 6) and size changes are not used.

Width is measured in display cells. A wide character counts as 2 cells and a zero-width character as 0.

## Layout & Spacing

The grid is the terminal cell grid.

Horizontal spacing is counted in cells:
- `{spacing.1}` is 1 cell;
- `{spacing.column-gap}` (1 cell) separates columns;
- `{spacing.gutter}` (2 cells) holds the selection and change marks;
- `{spacing.frame}` (1 cell) is a panel border.

Vertical spacing is counted in rows, with at most one blank row between regions.

The width bands are 160, 116 and 80 columns, with a notice below 80. EXPERIENCE.md, "Responsive & Platform", holds the PROPOSED column budgets, the PROPOSED 44-row budget and the shrink order.

## Elevation & Depth

There is no elevation; a terminal has no shadows or layers. Hierarchy comes only from:
- the frame weight (`{rounded.sm}` heavy versus `{rounded.DEFAULT}` light);
- bold titles;
- the ink/muted split.

The inspector replaces the ledger area instead of overlaying it; header line 1, the freshness strip and the COUNTS strip stay above it (rendering-rules.md:13, :19).

## Shapes

- `{rounded.DEFAULT}` is the light panel with rounded corners (╭ ╮ ╰ ╯, ─ │). It is used for the R1 ledger and every data panel.
- `{rounded.sm}` is the heavy square panel (┏ ┓ ┗ ┛, ━ ┃). It is kept for attention panels from release B onward (`OPEN HUMAN QUESTIONS`). R1 does not use it.
- A panel title is drawn as ` TITLE ` in bold on the top border, starting 2 cells in. It is clipped to the frame.

### Glyphs and ASCII fallbacks (`--ascii`)

| Glyph | Meaning | ASCII |
|---|---|---|
| ╭ ╮ ╰ ╯ ┏ ┓ ┗ ┛ | panel corners | `+` |
| ─ ━ | horizontal edge, rule | `-` |
| │ ┃ | vertical edge | `\|` |
| ▸ | selection cursor (PROPOSED) | `@` |
| `*` | changed since last look | `*` |
| `>` | cell truncated | `>` |
| · | footer key separator | `.` |

The prototype maps `▸` to `>` (`canvas.py:8`). This spine maps it to `@` instead (PROPOSED), because `>` is the spec's truncation marker (EXPERIENCE.md UX-OQ-5).

PROPOSED: under `--ascii`, any other non-ASCII character in source text is shown as `?` in ledger list cells only. In the inspector and the export, non-ASCII characters are written as `\uXXXX` escapes so every ID stays full and distinct (rendering-rules.md:24-25). This happens after sanitizing (EXPERIENCE.md, "Untrusted Text and Identifiers").

## Components

| Component | Anatomy | Colour and state |
|---|---|---|
| Header `{components.header}` | Line 1: the `ORCA OBSERVER` title, then mode, scope and `as of`. | Title accent bold, the rest ink. Fixture mode adds `{components.fixture-badge}` in warn bold. |
| Freshness strip `{components.freshness-strip}` | Line 2: one cell per source. | The state word is coloured: OK ink, STALE warn, FAILED bad, NOT POLLED muted, UNVERIFIED warn. |
| COUNTS strip `{components.counts-strip}` | 1 or 2 lines of `label value` tokens, with no bars. | Labels muted, numbers ink, `PARTIAL` warn, `unavailable (no source)` muted. |
| Gap notice `{components.gap-notice}` | One full-width line above the ledger. | warn bold. The word `UNVERIFIED` carries the meaning without colour. |
| Status line `{components.status-line}` | One line: changed-since count, hidden and duplicate counts, export result. (The filter count sits in the COUNTS strip, beside the source counts, rendering-rules.md:56.) | muted. The changed-since count is accent. |
| Ledger `{components.ledger}` | Light frame titled ` worker-reported, not questions `, a muted column header, then rows. | Border line, title ink bold. |
| Ledger row `{components.ledger-row}` | A 2-cell gutter, then the band's columns. | Values ink; `unknown` and ages muted; a cut cell ends in `>`. |
| Selected row `{components.ledger-row-selected}` | `▸` in gutter cell 1 (PROPOSED). | Reverse video across the row; the cursor glyph is accent. |
| Change mark `{components.change-mark}` | `*` in gutter cell 2. | accent. |
| Inspector `{components.inspector}` | The ledger area, below header line 1, the freshness strip and the COUNTS strip; one `label: value` per line. Values wrap and are never cut. | Labels muted, values ink, the `worker-reported` label warn, `unknown (absent in source)` muted. |
| Footer `{components.footer}` | A light rule, then the key list and the shown and collected counts. | Keys ink, the rest muted, the rule line. |
| Too-small diagnostic `{components.diagnostic}` | One sentence, plus the rows that are never dropped. | warn bold. |

## Do's and Don'ts

| Do | Don't |
|---|---|
| Pair every colour with a word or glyph | Use colour as the only signal |
| Keep raw source values in ink | Colour `workerState`, `outcome` or `nextAction.kind` as good or bad |
| Use `{colors.warn}` for stale, partial and unverified | Use `{colors.bad}` for stale or frozen |
| Show `unknown` in muted for absent data | Print `0`, `false`, `-` or a blank |
| End a cut cell with `>` | Use `…`, or split a wide character |
| Repaint in place on refresh | Blink, pulse, fade or scroll by itself |
| Keep every box glyph replaceable by `+ - \|` | Add a glyph without an ASCII fallback |
| Leave the background to the terminal | Fill panels with the prototype's `panel` colour |
