# Accessibility review (terminal UI): release-2 COORDINATOR QUESTIONS panel

Lens: ACCESSIBILITY. Review only; no spine or source file changed. Evidence: `/tmp/r2render/out.txt` plus my own renders (`/tmp/r2render-a11y/x.py`: too narrow 70x24, too small 116x7, long subject 116/80, NO_COLOR 80x24, collapsed fenced/open 116x14). Code read: `view.py`, `render.py`, `terminal.py`, `export.py`, spines, `rendering-rules.md`.

## Verdict

The panel passes the basic floor. Meaning is carried by words, not colour (`PALETTE` is empty, `terminal.py:42`), there is no blink or motion, and `Live(screen=True, auto_refresh=False)` repaints only on update. The too-narrow (70 cols) and too-small (7 rows) diagnostics keep the open count and the FAILED/consumer-fenced state, which is good.

It does not pass for a keyboard or screen-reader user who has more questions than fit, or a narrow or short terminal. Four high findings:

- The line-end `>` cut removes the "no longer in source window" caveat.
- Questions past the `x/y shown` window cannot be reached from the live screen, and the hidden ones are the newest.
- The short-terminal collapse drops the list and both caveats without saying so.
- At 80 columns the key line is cut before `e export` and `q quit`, and export is the only way to read the hidden questions.

The spines are also stale on colour and contrast, which the built UI no longer has.

## Findings

Severity is downstream impact. "[R2]" marks the new panel or its screen fit.

### NO_COLOR and monochrome

- **[R2] medium: state, count and caveats are not findable at a glance.** (`view.py:585-599`, `635`; seen at 160/80)
  - In the OK state the panel has no state word. `read OK` exists only in the collapsed summary, and the header line says "last read 0s ago".
  - FAILED and STALE appear as a bare line (`FAILED (consumer-fenced) 0s`, `STALE 50s`) after the 2-line disclosure and before the count, unstyled and unlabelled.
  - The count is mid-line (`observed open: 5 | closed by evidence: ...`).
  - With no styling, a user must read about 35 words of boilerplate to reach the data.
  - Change: put one first line directly under the title, `question read: OK|STALE 50s|FAILED (consumer-fenced) 0s|pending`, then `observed open: 5` (move `closed by evidence: unavailable` to its own line or after the list), then the list, then the disclosure and retention lines as a block of caveats after the data.
- **[R2] medium: the header contradicts the panel on FAILED.**
  - The "fenced after ok" render shows header `coordinator questions: one Run, last read 0s ago` above `FAILED (consumer-fenced) 0s`.
  - "last read" can mean the failed read or the last successful one, and the screen does not say which.
  - Change: `last read OK 12s ago` / `last read FAILED 0s ago`, or drop the "last read" clause when the panel is shown.
- Good: no emphasis is needed for the words `FAILED`, `STALE`, `unavailable`, `unknown`. `NO_COLOR` is trivially satisfied (checked at 80x24, identical to the colour-off output).

### Motion and flicker

- No finding. `commands.py:255` uses an alternate screen with manual refresh; there is no SGR 5/6.
- Not verified: how often the loop calls `refresh`. If it repaints every tick with identical text, a screen reader on the alternate screen may re-announce the whole page. That is the spine's stated "no promise" for the live screen, but the spine should say so in the R2 section.

### ASCII mode

- **[R2] medium: `?` substitution makes subjects ambiguous and can hide that it happened.** (`terminal.py:156-158`, `render.py:309` via `clip`)
  - Seen: `1h  h?llo ?  reason unknown`.
  - Two different subjects can collapse to the same text.
  - A substituted character is indistinguishable from a literal `?`, and questions often end with one ("... or merge?").
  - The panel line has no id, so the user cannot recover the identity. The spine's rule (`\uXXXX` in the inspector and export) does not help, because questions have no inspector.
  - Change: either show a short id prefix in the line, or in ASCII mode render replaced characters as `\uXXXX` (or `{U+00E9}`) in the question line too, or append `(non-ASCII shown as ?)` once to the disclosure when any substitution occurred.
- low: the `>` truncation marker is also an ordinary subject character, so "cut or literal `>`" is ambiguous. Same fix as the high finding below (a separate field for the cut subject plus a trailing `...>` fixed place).

### Screen reader and linear reading order

- **[R2] medium: repeated identical lines with no ordinal.** (seen: 4x `59m  Should I rebase onto master or merge?  reason unknown`)
  - Items are distinguishable only by position, and a speaker cannot say "item 3 of 5".
  - `reason unknown` repeats on every line, and the age is coarse (see low finding).
  - Change: number the lines (`1 of 5`), or prefix a short message-id tail; hoist `reason unknown` into the disclosure once ("reason not available from Orca") and drop it from rows.
- **[R2] medium: three different "shown" strings with no noun.** (`7/20 shown`, `2/4 shown  +2 more`, footer `shown 2/4 | collected ...`; seen at 116x24)
  - A reader hears `7/20 shown` and cannot tell it means questions, nor that the next `2/4 shown` means workers.
  - Change: `questions shown 7 of 20` and `workers shown 2 of 4`; keep the footer as is or align it.
- Columns that rely on alignment: the question lines do not (two-space separators), so linear reading is sentence-like (`age subject reason unknown`) and works. The worker table at 160 columns is alignment-based, but that is pre-existing, and the 116/80 forms are line forms.
- Good: the disclosure comes before the list, and the caveat words come before the data they qualify.

### Width truncation and wrapping

- **[R2] high: the end-of-line `>` cut removes the state caveat.** (`view.py:622-624`, `render.py:309`)
  - The line is `age  subject  reason unknown[  no longer in source window]`, cut as one string.
  - Seen 116x30: `1h  Orchestrator asks ... for the review  reason unknown  no lo>`. At 80 columns, with an 85-character subject, every question ends `... wait f>`, so `reason unknown` is lost on every line and `no longer in source window` is lost on any long one.
  - A question that left the window looks the same as a live one.
  - Change: put the state first (`1h  [left window]  subject ...`) and clip only the subject field to the remaining width, so the age, the flag and the reason are never cut.
- **[R2] medium: header line 4 cuts a state word at 80 columns.** (`SETTLED unavailable (no source)  POLICY FROZEN unavailable (no source)  cost un>`)
  - `cost un>` hides "unavailable". Not verified whether R2 introduced this; the R2 header2 text is the longer one.
  - Change: let `counts_lines` wrap to a third line at 80, or shorten to `cost n/a`.
- **[R2] high: at 80 columns the key line is cut to `... m mark  e exp>`.** (`render.py:416`, `view.py:75`; seen at 80x30, 80x24)
  - `e export` and `q quit` are the two keys the user needs, and export is the only way to read all questions.
  - Change: wrap the key line like the footer counts, or drop `Esc back`/`h historical` at 80, or print a second line `e export  q quit`.
- Too narrow (<80) and too small (<8 rows): the diagnostics keep the open count, the FAILED state and the Run id (checked 70x24 and 116x7). The summary reads `observed open 3; FAILED (consumer-fenced); one Run only: ...`; it does not say that `bounded best effort` applies (see the collapse finding).
- low: the long disclosure wraps cleanly at 80 and at 116 (`... not 100` / `questions; ...`), but a break between "not 100" and "questions" is slightly awkward. Optionally split the sentence at the semicolons into short lines.

### Height fit and the collapse

- **[R2] high: the collapse to the one-line summary silently loses the list and both caveats.** (`render.py:371-377`; seen 160x14, 80x14, 116x16 with 100 rows)
  - The summary `coordinator questions: observed open 20; read OK; one Run only: run_...` drops the questions, the `bounded best effort; coverage unknown` disclosure and the `retention reset ... not retained` line.
  - Left like this, the count can be read as complete.
  - It also says nothing about why the list is gone or what to do.
  - The threshold is high. Derived from the code, not measured: at 116 columns with 4 workers the panel needs about 17-18 rows before it shows even one question, so 16 rows and below collapse.
  - Change: the summary should say `observed open 20 (bounded best effort; list hidden: enlarge terminal to 18 rows or press e)` and keep `retention reset at HH:MM`; or keep the three-line minimum (state, count, disclosure) and drop the ledger first.
- **[R2] medium: the worker ledger gets squeezed to 2 rows.** (116x24 and 80x24: `2/4 shown  +2 more`)
  - The comment at `render.py:373` says "at least 3 ledger rows stay", but 2 are shown.
  - It is a priority choice (questions over workers) that is not in the spines.
  - Change: either hold the 3-row promise in the code, or state the priority in the spine.
- Good: the footer and the `x/y shown` line stay on screen at 24 rows.

### Keyboard operability

- **[R2] high: questions beyond the window are unreachable from the live screen, and the hidden ones are the newest.** (`view.py:215` `lines[:keep]`; oldest first; seen `7/20 shown`, `22/100 shown`)
  - Up/Down and `j/k` move the worker rows only. The key line reads "Up/Down j/k move" with no object, so a user will press Down expecting the questions to scroll.
  - `window full: older questions may be missing` implies the oldest are lost, while the display also hides the newest.
  - The only way to the full list is `e` export, which includes every question with its full id (`export.py:101-116`). The screen never says so.
  - Change: append `all questions: e export or --once` to the `x/y shown` line; show the newest first, or keep both ends (`oldest 4 ... newest 3`); say in the key line `j/k move workers`.
- The questions are not selectable, so there is no focus marker and `m` has no effect on them, as the spec says. There is nothing to announce for focus.

### Cognitive load and jargon

- **[R2] medium: jargon.**
  - `bounded best effort; coverage unknown; at most 100 rows per read, not 100 questions; bursts over 100 rows between reads may be lost` is one 28-word run-on.
  - `consumer-fenced` and `no-active-terminal` are the raw source codes, kept on purpose, but the next line explains them well (`this terminal does not hold the named Run`).
  - `Run` is capitalised with no definition.
  - `reason unknown` does not say whose reason.
  - Change (needs a human decision on wording): `May be incomplete. Shows what this terminal saw in its last read (up to 100 messages).` Keep the technical sentence only in the export or the help.
- low: ages are coarse. `1h` followed by `59m` reads as out of order, and `unknown` age is shown as a bare word. Show `1h 00m`, or the minutes up to 119, or the clock time `since 11:01`.
- low: spine drift. `EXPERIENCE.md` Accessibility Floor and `DESIGN.md` still describe colour ratios (7.63:1 to 14.56:1), muted `unknown`, the `▸`/`@` selection glyph and the `\uXXXX` rule for lists. The built UI has an empty palette, no selected question and `?` in list lines. Update the spines to the built behaviour and add the R2 panel to the Accessibility Floor.

## Open questions (human decision needed)

1. Should the newest or the oldest questions stay on screen when the window cuts? The spec says oldest first; the Run's current ask is more likely newest.
2. Is the "questions before worker rows" priority at 24 rows intended (2 worker rows left), or should the 3-row promise hold?
3. How much of the disclosure may be paraphrased in plain words? It is a data-honesty statement and its exact text may be pinned by tests or by the owner.
4. Is a screen-reader path in scope for the live screen, or only for `--once`? If only `--once`, say so in the key line or `--help`.
5. Do you want a short id on each question line (needed for ASCII-mode disambiguation and for matching against the export)?

## Counts

high 4, medium 8, low 4 (findings only; no critical).
