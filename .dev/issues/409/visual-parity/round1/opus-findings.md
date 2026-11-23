# Round 1 visual-parity findings: reviewer "opus" (issue #606, sub-issue of #409)

- **Model id:** claude-opus-5-5 (Opus 5.5)
- **Reviewer name:** opus
- **Date:** 2026-11-17
- **Task:** `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/issues/409/visual-parity/round1/TASK-opus.md` (task_ddaadc71b3f2). The other reviewer's file in `round1/` was not opened.
- **Inputs used** (all under `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/issues/409/visual-parity/inputs/`):
  - Text exports: `current/{160,116,80}/{ledger,questions,desk}.txt` (all nine read in full) and `mockups/{160,116,80}/{signal-bridge,agent-focus-attention-ledger,decision-desk}.txt` (all nine read).
  - ANSI exports: `current/*/ansi-*.txt` (escape bytes counted, and each compared byte-for-byte with its `.txt`); `mockups/*/*.ansi` (escape codes counted and decoded into colour roles for the title, pane-border and row lines at 160).
  - PNGs: this model can view images. Viewed `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/issues/409/attachments/{signal-bridge,attention-ledger,decision-desk}.png`. The per-width mockup PNGs under `mockups/<width>/` were not opened; per-width layout was taken from the matching `.txt` and `.ansi` files.
  - Reference only (not edited): `src/superclaude/cli/observe/{render,terminal}.py` and `.dev/issues/409/bmad/spec-orca-observer/rendering-rules.md` (cited as `spec:<line>`).
- **Method:** each finding quotes current lines in a fenced block whose info string names the current file; every quoted line was checked to exist verbatim in that file (check at the end of this file).

## Confirmation of the "known so far" list

| Claim | Verdict | Evidence |
|---|---|---|
| No colour styling at all; ANSI export holds no escape bytes | CONFIRMED | All nine `current/*/ansi-*.txt` contain 0 ESC bytes and are byte-identical to the matching `.txt`. Root cause: `render.py:524-529` builds one unstyled `Text(line)` per line. See F-opus-01. |
| No boxed titled panes | CONFIRMED | No box-drawing border characters in any current render; section titles are bare lines. F-opus-03. |
| No two-column Decision Desk | CONFIRMED | The desk is a stacked block under the question list at all three widths. F-opus-30. |
| No big count tile for "SEEN IS NOT RESOLVED" | CONFIRMED | Only the text line `seen, not resolved: 3 | ...`. F-opus-22. |
| No RETAIN CONTEXT panel | CONFIRMED | Absent at all widths (spec:41 says "not built in R2"). F-opus-27. |

## Mockup theme reference (decoded from `mockups/160/*.ansi`)

24-bit foreground colours only (no background escapes in any mockup `.ansi`): base text `225;233;238`; amber `250;178;25` (attention pane border and title, question text, `SYNTHETIC · READ ONLY`, age column, big digits); cyan `112;205;226` (screen title `◈ ...`, live session rows, SIGNALS and SEEN IS NOT RESOLVED frames); slate `82;108;128` (secondary pane borders and titles, footer rule, bar track); muted `165;182;194` (captions, second lines, key hints); green `139;215;175` (settled); red `240;141;150` (failed); violet `194;173;242` (frozen). Bold is used on pane titles, the screen title, the selected question and count tiles. Attention panes use the heavy box (`┏━ ┃ ┗`), secondary panes the rounded box (`╭─ │ ╰`).

## Findings

### A. Cross-screen findings (ledger, questions and desk; all widths)

#### F-opus-01: No colour or text styling anywhere
- **Mockup:** every `mockups/{160,116,80}/*.ansi`, whole screen (title, pane borders, rows, footer).
- **Evidence:** all nine `current/<width>/ansi-*.txt` have 0 escape bytes and equal their `.txt` files; `render.py:524-529` wraps each screen line in a plain `Text(line)` with no style. The screen title and the attention data print in the same plain weight as every caveat:
```current/160/ledger.txt
ORCA OBSERVER  mode=fixture  SYNTHETIC FIXTURE base, not Orca data  scope=all  as of 12:00:00
```
```current/160/desk.txt
Choose schema compatibility policy
```
- **Category:** THEME-COLOUR
- **Class:** PARITY-GAP
- **Severity:** High
- **Fix direction:** render styled spans from one named theme (the eight mockup roles above) instead of plain strings, keeping the same text so NO_COLOR and the text export stay identical.

#### F-opus-02: Console colour system cannot show the mockup palette
- **Mockup:** `mockups/160/signal-bridge.ansi`, all regions (24-bit escapes such as `38;2;250;178;25` amber and `38;2;82;108;128` slate).
- **Evidence:** `terminal.py:121` builds every console with `color_system="standard"` (16 colours), so even once styles exist the amber, slate and muted greys would be snapped to the nearest of 16 ANSI colours and the slate/muted distinction is lost. Same unstyled header at every width:
```current/116/questions.txt
ORCA OBSERVER  mode=live  scope=all  as of 12:00:00
```
- **Category:** THEME-COLOUR
- **Class:** PARITY-GAP
- **Severity:** Medium
- **Fix direction:** let the console use truecolor where the terminal supports it with a 256-colour fallback, and keep `None` under NO_COLOR.

#### F-opus-03: No boxed, titled panes on any screen
- **Mockup:** all nine mockups; e.g. `mockups/160/signal-bridge.txt` lines 6-44 (`┏━ HUMAN QUESTION ━...┓`, `╭─ SESSION REGISTER ─...╮`, `┏━ SIGNALS ━...┓`).
- **Evidence:** section titles are bare lines with no frame, at every width:
```current/160/questions.txt
COORDINATOR QUESTIONS
worker-reported, not questions
```
```current/80/desk.txt
DECISION DESK
```
- **Category:** FRAME-PANE
- **Class:** PARITY-GAP
- **Severity:** High
- **Fix direction:** draw each block as a titled pane: heavy amber box for the attention block (questions, Decision Desk question), rounded slate box for secondary blocks, cyan for count tiles; titles inset in the top border.

#### F-opus-04: Title bar has no title/badge split and no read-only badge
- **Mockup:** all mockups, lines 2-4 (e.g. `mockups/116/signal-bridge.txt`: `◈ SIGNAL BRIDGE` bold cyan at left, `SYNTHETIC · READ ONLY` amber right-aligned, then a muted freshness line).
- **Evidence:** one run-on line; nothing right-aligned; the screen never says READ ONLY; at 80 the clock wraps onto its own line:
```current/160/ledger.txt
ORCA OBSERVER  mode=fixture  SYNTHETIC FIXTURE base, not Orca data  scope=all  as of 12:00:00
worker-list OK 0s  messages UNVERIFIED (not read)
```
```current/80/ledger.txt
ORCA OBSERVER  mode=fixture  SYNTHETIC FIXTURE base, not Orca data  scope=all
as of 12:00:00
```
- **Category:** TYPOGRAPHY-EMPHASIS
- **Class:** PARITY-GAP
- **Severity:** Medium
- **Fix direction:** left-aligned bold title with a glyph, right-aligned amber mode badge (`SYNTHETIC FIXTURE` or `LIVE` plus `READ ONLY`), and the spec header-1 tokens (spec:17) moved to a muted second line so they wrap there, not the title.

#### F-opus-05: Header line "8 owners / 80 sessions / 80 mapped trees"
- **Mockup:** all mockups, line 3.
- **Evidence:** the observer shows source counts instead:
```current/160/ledger.txt
collected 80 / reported 80  scope=all  source counts: active 54 / reclaimable 0 / retained 13 / released 13  runs seen: 8  SETTLED unavailable (no source)
```
- **Category:** INFO-HIERARCHY
- **Class:** ACCEPTED-DIVERGENCE: the observer has no owner or mapped-tree data; the COUNTS strip (spec:20) is the real-data equivalent. Only its styling is in scope (F-opus-01).
- **Severity:** Low
- **Fix direction:** none for content; style the COUNTS strip as the muted sub-header line.

#### F-opus-06: Footer lacks the rule, the `·` key separators and muted styling
- **Mockup:** all mockups, last three lines (full-width slate `───` rule, `j/k select · tab pane · / filter · enter evidence · p hold view` muted, provenance line `LOCAL FIXTURE · source coverage is not fleet-wide assurance`).
- **Evidence:** keys and counts on one unstyled line with no rule above:
```current/160/ledger.txt
Up/Down j/k move  Enter detail  Esc back  / filter  h historical  m mark  e export  q quit  shown 39/54 | collected 80 / reported 80
```
- **Category:** KEYS-FOOTER
- **Class:** PARITY-GAP (the key set itself differs by spec:21, which is ACCEPTED-DIVERGENCE; only the presentation is the gap)
- **Severity:** Low
- **Fix direction:** a full-width slate rule above the footer, key hints muted with ` · ` separators, the `shown x/y | collected n / reported T` counts on their own line.

#### F-opus-07: Absent values print as plain `unknown`, not muted (spec rule unmet)
- **Mockup:** `mockups/160/signal-bridge.ansi` captions and second lines use muted `165;182;194`; spec:70 says an absent field is "literal `unknown`, muted (plain under NO_COLOR)".
- **Evidence:**
```current/160/questions.txt
collected 6 / reported 6  scope=all  source counts: unknown  runs seen: 2  SETTLED unavailable (no source)  POLICY FROZEN unavailable (no source)
  59m  Confirm deployment window  reason unknown
```
- **Category:** THEME-COLOUR
- **Class:** DEFECT (the spec already requires the muting; the render does not apply it)
- **Severity:** Medium
- **Fix direction:** style every `unknown` and `unavailable (no source)` token muted in colour mode, plain under NO_COLOR.

#### F-opus-08: ASCII mode has no box mapping ready for panes
- **Mockup:** all mockups use `┏━┃┗` and `╭─│╰` borders; spec:25 says `--ascii` "replaces box drawing with `+-|`".
- **Evidence:** today the only drawing glyphs are the table rule and the selection mark, both covered by the glyph table (`terminal.py:30-34`); every other non-ASCII character becomes `?` (`terminal.py:133-135`), and `safe_box` (`terminal.py:123`) does not force an ASCII box on a UTF-8 stream. Current glyph use:
```current/116/desk.txt
▸ 1h  Choose schema compatibility policy  reason unknown
```
- **Category:** NO_COLOR-ASCII
- **Class:** PARITY-GAP (forward risk: adding panes without this breaks `--ascii`)
- **Severity:** Medium
- **Fix direction:** when panes are added, pick an explicit ASCII box (`+-|`) under `--ascii`, and keep every emphasis that colour carries also in text (bold, title words, glyphs) so NO_COLOR keeps the hierarchy.

### B. Ledger screen (`current/<width>/ledger.txt` against `signal-bridge`)

#### F-opus-09: One full-width table instead of the three-column bridge
- **Mockup:** `mockups/160/signal-bridge.txt` lines 6-44: left column (HUMAN QUESTION over OBSERVATION WINDOW), centre SESSION REGISTER, right SIGNALS. At 116 (`mockups/116/signal-bridge.txt`) the question pane spans the width and REGISTER sits beside OBSERVATION WINDOW; at 80 everything stacks.
- **Evidence:** a single wide table under a bare title:
```current/160/ledger.txt
worker-reported, not questions
   dispatchId             run          workerState  dispatchStatus terminalState  outcome      nextAction.kind  liveness               evidence age flags
```
- **Category:** LAYOUT
- **Class:** PARITY-GAP
- **Severity:** High
- **Fix direction:** at 160 lay out a three-column grid (status panes left, register centre, count tiles right); at 116 two columns; at 80 stacked panes, as in the mockups.

#### F-opus-10: Source freshness is a run-on line, not the OBSERVATION WINDOW pane
- **Mockup:** `mockups/160/signal-bridge.txt` lines 16-44, left column: per-source CAPS label in bold cyan (`WORKERS`, `MESSAGES`, `CHECKS`, `COST`, `RESOURCES`) with `status | age` beneath, footnote `Stale does not mean failed`.
- **Evidence:** the same facts exist but are packed into header lines:
```current/160/ledger.txt
worker-list OK 0s  messages UNVERIFIED (not read)
POLICY FROZEN unavailable (no source)  cost unavailable
```
- **Category:** INFO-HIERARCHY
- **Class:** PARITY-GAP (the CHECKS and RESOURCES rows have no observer source; showing them as `unavailable (no source)` or omitting them is ACCEPTED-DIVERGENCE)
- **Severity:** Medium
- **Fix direction:** at 160 and 116 render the freshness cells as a slate pane with one label/value pair per source (worker-list, messages or coordinator questions, cost); keep the one-line strip at 80.

#### F-opus-11: Source counts are inline text, not count tiles
- **Mockup:** `mockups/160/signal-bridge.txt` lines 6-44, right `SIGNALS` pane: large bold number plus CAPS label per state (`48  RUNNING`, `24  SETTLED`, ...); at 80 a compact strip `RUN 48  SETTLED 24  UNKNOWN 8  STALE 5` (`mockups/80/signal-bridge.txt` line 14).
- **Evidence:** the real counts are buried mid-line:
```current/116/ledger.txt
collected 80 / reported 80  scope=all  source counts: active 54 / reclaimable 0 / retained 13 / released 13
```
- **Category:** INFO-HIERARCHY
- **Class:** PARITY-GAP
- **Severity:** Medium
- **Fix direction:** show the source-reported counts (active, reclaimable, retained, released, collected/reported) as bold number + label tiles in a cyan pane at 160, and as a bold compact strip at 116 and 80; numbers and denominators only.

#### F-opus-12: SIGNALS bar meters and the SETTLED / POLICY FROZEN / UNKNOWN / STALE tiles
- **Mockup:** `mockups/160/signal-bridge.txt` right pane, bar rows `█████████████████░░░░░░░░░░░` under each count.
- **Evidence:**
```current/160/ledger.txt
POLICY FROZEN unavailable (no source)  cost unavailable
```
- **Category:** INFO-HIERARCHY
- **Class:** ACCEPTED-DIVERGENCE: spec:20 says the COUNTS strip is "numbers and denominators only, no bars, no health name" and spec:93 says there is "No verified mapping from `workerState`/`outcome` to "settled""; SETTLED and POLICY FROZEN have no source.
- **Severity:** Low
- **Fix direction:** none; keep the `unavailable (no source)` tokens, styled muted (F-opus-07).

#### F-opus-13: The question gap notice is a plain line, not the HUMAN QUESTION pane slot
- **Mockup:** `mockups/{160,116,80}/signal-bridge.txt` lines 6-13 at 160 and 6-12 at 116 and 80, heavy amber `HUMAN QUESTION` pane at top-left (160) or full width (116, 80).
- **Evidence:** in fixture mode the question area is one unframed line among the header lines:
```current/160/ledger.txt
Human questions: source UNVERIFIED, 0 rows interpreted, not "no questions"
```
- **Category:** FRAME-PANE
- **Class:** PARITY-GAP (the pane's content, owner/scope/affected, is ACCEPTED-DIVERGENCE: no source)
- **Severity:** Medium
- **Fix direction:** reserve the amber attention pane in the mockup's position and put the gap notice (or, when questions are read, the oldest open question) inside it, so the question area keeps its place and weight.

#### F-opus-14: Worker state values carry no state colour
- **Mockup:** `attachments/signal-bridge.png` and `mockups/160/signal-bridge.ansi` register rows: running cyan, settled green, failed red, frozen violet, stale amber; second line muted.
- **Evidence:** a blocked row looks the same as an idle one:
```current/160/ledger.txt
   w-002                  run-c        blocked      blocked        active         none         review           alive (terminal)       13s
   w-007                  run-h        idle         active         active         none         none             alive (terminal)       28s
```
- **Category:** THEME-COLOUR
- **Class:** PARITY-GAP
- **Severity:** Medium
- **Fix direction:** colour the raw `workerState` / `dispatchStatus` value by its literal text from a fixed table (unknown values stay neutral), without classifying or renaming them; `nextAction.kind` stays uncoloured verbatim (spec:31).

#### F-opus-15: Register row format and camelCase column headers
- **Mockup:** `mockups/160/signal-bridge.txt` SESSION REGISTER: two lines per session (`S001    running  / work`, then `not observed / not admitted | stale | not frozen`) under a caption line.
- **Evidence:**
```current/160/ledger.txt
   dispatchId             run          workerState  dispatchStatus terminalState  outcome      nextAction.kind  liveness               evidence age flags
   w-001                  run-b        idle         active         active         none         none             alive (terminal)       10s
```
- **Category:** TYPOGRAPHY-EMPHASIS
- **Class:** ACCEPTED-DIVERGENCE: spec:30-31 require the separate raw fields with `nextAction.kind` verbatim, and admission/frozen state has no source. Only the header styling (muted caption, slate rule) is in scope, under F-opus-01.
- **Severity:** Low
- **Fix direction:** keep the columns; style the header row muted bold and the rule slate.

#### F-opus-16: No column header at 116 and 80
- **Mockup:** `mockups/116/signal-bridge.txt` line 15 and `mockups/80/signal-bridge.txt` line 17: the register keeps its caption `SESSION / LIFECYCLE / PHASE; RESULT / ADMISSION BELOW` at every width.
- **Evidence:** the header is drawn only for the full width class (`render.py:497`), so at 116 and 80 the first column (`nextAction.kind`) shows bare `none` / `review` / `wait` that read like a status:
```current/116/ledger.txt
worker-reported, not questions
   none               w-001                                                alive          10s
```
```current/80/ledger.txt
worker-reported, not questions
   none           w-001                                  10s
```
- **Category:** INFO-HIERARCHY
- **Class:** DEFECT
- **Severity:** Medium
- **Fix direction:** print a one-line muted column header (`kind  dispatchId  liveness  age`, or the 80 subset) at every width class.

#### F-opus-17: A wide blank band between the id and the next column at 116 and 80
- **Mockup:** `mockups/116/signal-bridge.txt` register rows keep id and state close (`S001    running  / work`).
- **Evidence:** the id column is up to 60 cells (`render.py:195`) and 5-character ids leave about 50 empty cells; the question-panel worker rows show the same:
```current/116/ledger.txt
   review             w-002                                                alive          13s
```
```current/80/questions.txt
   wait           w-001                                  3s
```
- **Category:** LAYOUT
- **Class:** DEFECT
- **Severity:** Medium
- **Fix direction:** size the id column to the longest id shown (capped), and give the spare width to the right-hand columns or leave it after the row.

#### F-opus-18: Lifecycle state dropped at 116 and 80
- **Mockup:** `mockups/{116,80}/signal-bridge.txt` register rows keep the lifecycle word at every width (`S002    running  / review`).
- **Evidence:** the 116 and 80 rows have no `workerState`:
```current/116/ledger.txt
   wait               w-006                                                alive          25s
```
- **Category:** INFO-HIERARCHY
- **Class:** PARITY-GAP (spec:33 sets the 116 form to kind, dispatchId, verdict, age; following the mockup needs a spec change)
- **Severity:** Low
- **Fix direction:** fit a short `workerState` column (freed by F-opus-17) at 116, and at 80 if width allows.

#### F-opus-19: At 80 the ledger key list is cut, losing `e export` and `q quit`
- **Mockup:** `mockups/80/signal-bridge.txt` line 41: the whole key hint line fits at 80.
- **Evidence:** the ledger footer is clipped with `>` (`render.py:307`), while the questions and desk screens wrap the same list:
```current/80/ledger.txt
Up/Down j/k move  Enter detail  Esc back  / filter  h historical  m mark  e exp>
```
- **Category:** DEGRADED-WIDTH
- **Class:** DEFECT
- **Severity:** Medium
- **Fix direction:** never cut the key list: wrap it at key boundaries (or shorten the labels) at 80, as the questions screen already does.

#### F-opus-20: At 80 COUNTS tokens are cut mid-token and four tokens disappear
- **Mockup:** `mockups/80/signal-bridge.txt` line 14: a compact count strip that fits.
- **Evidence:** `runs seen: 8`, `SETTLED`, `POLICY FROZEN` and `cost` tokens are lost after a mid-word cut (the same cut on the questions screen ends in `cost un>`):
```current/80/ledger.txt
source counts: active 54 / reclaimable 0 / retained 13 / released 13  runs seen>
```
```current/80/questions.txt
SETTLED unavailable (no source)  POLICY FROZEN unavailable (no source)  cost un>
```
- **Category:** DEGRADED-WIDTH
- **Class:** PARITY-GAP (spec:20 allows `>` on lower-priority tokens, so this is legal; the result is still a fragment)
- **Severity:** Low
- **Fix direction:** drop whole low-priority tokens (with a count of hidden tokens) rather than cutting inside one, or use short labels at 80 like the mockup strip.

### C. Questions screen (`current/<width>/questions.txt` against `agent-focus-attention-ledger`)

#### F-opus-21: Questions stacked above the ledger instead of the two-column ledger
- **Mockup:** `mockups/160/agent-focus-attention-ledger.txt` lines 6-44 (same arrangement in `mockups/116/agent-focus-attention-ledger.txt`): heavy amber `OPEN HUMAN QUESTIONS` pane on the left, `SEEN IS NOT RESOLVED` and `RETAIN CONTEXT` stacked on the right.
- **Evidence:** one stacked column of lines, then the worker table:
```current/160/questions.txt
COORDINATOR QUESTIONS
one Run only: run_14cfcbd8edf2
question read: OK 0s
```
- **Category:** LAYOUT
- **Class:** PARITY-GAP (spec:43 chose "One stacked block at every width" for R2 with the two-column layout kept as "design reference"; adopting the mockup layout reverses that recorded choice and needs the owner's approval)
- **Severity:** High
- **Fix direction:** at 160 and 116 put the questions pane left (width - 43 per spec:12) with the count tile and context pane in a 42-wide right column; stacked at 80.

#### F-opus-22: "seen, not resolved" is a text line, not the big count tile
- **Mockup:** `mockups/160/agent-focus-attention-ledger.txt` lines 6-18, cyan `SEEN IS NOT RESOLVED` pane with a 5-row amber block digit `3` and the caption `observed questions`.
- **Evidence:** the count sits in the fourth line of caveats, same weight as them:
```current/160/questions.txt
seen, not resolved: 3 | closed by evidence: unavailable (no source)
```
- **Category:** INFO-HIERARCHY
- **Class:** PARITY-GAP (spec:40 itself asks for a "big count of observed open questions")
- **Severity:** Medium
- **Fix direction:** a cyan-framed tile with large amber digits and the caption, the `closed by evidence: unavailable (no source)` sub-line muted; the exact counts-line text (including `100+ (window full)` and `unknown (...)` forms) stays for NO_COLOR, ASCII and 80 (spec:61 `SEEN IS NOT RESOLVED n`).

#### F-opus-23: Five caveat lines come before the first question
- **Mockup:** `mockups/160/agent-focus-attention-ledger.txt` line 9: the first question is the first content line of the pane; caveats live in the footer line and the side panes.
- **Evidence:** the three questions start on line 11, after these lines:
```current/160/questions.txt
bounded best effort; coverage unknown; at most 100 rows per read, not 100 questions; bursts over 100 rows between reads may be lost
no read marker in source: answered questions stay listed
```
At 116 and 80 the disclosure alone takes two lines:
```current/116/questions.txt
bounded best effort; coverage unknown; at most 100 rows per read, not 100 questions; bursts over 100 rows between
reads may be lost
```
- **Category:** INFO-HIERARCHY
- **Class:** PARITY-GAP (the lines are spec-required, spec:44-49, but the order after the state line is PROPOSED and spec:38 puts the disclosure in the pane title)
- **Severity:** Medium
- **Fix direction:** keep every required line but render the disclosure and caveat muted in the pane title or pane foot, so the questions are the first bright content.

#### F-opus-24: Question rows have no emphasis or separation
- **Mockup:** `mockups/160/agent-focus-attention-ledger.txt` lines 9-28: fixed-width bold amber age (`45 MIN`), bold question text, muted sub-lines, slate rule between questions.
- **Evidence:** every part of the row is plain, including the spec-required `reason unknown` (spec:50) that repeats on each row:
```current/160/questions.txt
  1h  Choose schema compatibility policy  reason unknown
  59m  Confirm deployment window  reason unknown
```
- **Category:** TYPOGRAPHY-EMPHASIS
- **Class:** PARITY-GAP
- **Severity:** Medium
- **Fix direction:** bold amber age, bold base-colour question text, `reason unknown` muted; at 160 and 116 a thin slate rule or blank line between questions.

#### F-opus-25: Question age column is not aligned
- **Mockup:** `mockups/160/agent-focus-attention-ledger.txt` lines 9, 17, 25: ages padded so every question text starts in the same column.
- **Evidence:** the text starts one column later after a 3-character age (all widths):
```current/80/questions.txt
  1h  Choose schema compatibility policy  reason unknown
  59m  Confirm deployment window  reason unknown
```
- **Category:** LAYOUT
- **Class:** DEFECT
- **Severity:** Low
- **Fix direction:** pad the age to a fixed width (the widest age shown) before the question text.

#### F-opus-26: Requester, owner and Affected sub-lines
- **Mockup:** `mockups/160/agent-focus-attention-ledger.txt` lines 11-12 (`O01 requests / Human operator`, `Affected: S001, S011, S021, S031`).
- **Evidence:** rows carry only age, text and reason:
```current/116/questions.txt
  59m  Name the release reviewer  reason unknown
```
- **Category:** INFO-HIERARCHY
- **Class:** ACCEPTED-DIVERGENCE: no requester, owner or multi-session affected source (spec:38 notes Orca has no human recipient field).
- **Severity:** Low
- **Fix direction:** none.

#### F-opus-27: No RETAIN CONTEXT panel
- **Mockup:** `mockups/160/agent-focus-attention-ledger.txt` lines 21-38, slate `RETAIN CONTEXT` pane listing seven retained attributes with `7/7 lines shown`.
- **Evidence:** only the retention note exists:
```current/160/questions.txt
retention reset at 12:00; questions observed before this start are not retained
```
- **Category:** FRAME-PANE
- **Class:** PARITY-GAP for the pane (spec:41 says "design reference; not built in R2"); rows without a source (requesting orchestrator, affected stable IDs) are ACCEPTED-DIVERGENCE and would read `unavailable (no source)`.
- **Severity:** Low
- **Fix direction:** at 160 and 116 a slate pane listing each attribute with its live availability as spec:41 words it, plus the retention note; at 80 leave it to the inspector (spec:61).

#### F-opus-28: Key list wraps inside a key binding
- **Mockup:** `mockups/{116,80}/agent-focus-attention-ledger.txt` line 41: the key hint line fits on one line.
- **Evidence:** wrapping breaks at single spaces, splitting `n/p question` at 116 and `m mark rows` at 80 (questions and desk screens):
```current/116/questions.txt
Up/Down j/k move workers  Enter detail  Esc back  / filter  h historical  m mark rows  e export all  q quit  n/p
question
```
```current/80/desk.txt
Up/Down j/k move workers  Enter detail  Esc back  / filter  h historical  m
mark rows  e export all  q quit  n/p question
```
- **Category:** KEYS-FOOTER
- **Class:** DEFECT
- **Severity:** Low
- **Fix direction:** wrap only at the double-space gaps between key groups.

#### F-opus-29: At 80 there is no focused question card and no invariant lines
- **Mockup:** `mockups/80/agent-focus-attention-ledger.txt` lines 7-9 (the oldest question with its evidence above the list) and lines 12-18 (`SELECTED SIGNALS` pane with `Q01 45m ...` rows and the lines `Questions stay until explicit resolution.` / `No reply observed is not delivery failure.`).
- **Evidence:** at 80 the list is unframed and neither invariant line appears:
```current/80/questions.txt
no read marker in source: answered questions stay listed
  1h  Choose schema compatibility policy  reason unknown
```
- **Category:** DEGRADED-WIDTH
- **Class:** PARITY-GAP (spec:61 still lists both invariant lines for 80; whether the R2 panel rules of spec:43-56 replaced them is UNVERIFIED). Owner and evidence fields of the card are ACCEPTED-DIVERGENCE (no source).
- **Severity:** Low
- **Fix direction:** at 80 frame the question list in one pane and keep the two invariant lines (muted) at its foot.

### D. Desk screen (`current/<width>/desk.txt` against `decision-desk`)

#### F-opus-30: Decision Desk stacked under the list instead of the two-column desk
- **Mockup:** `mockups/160/decision-desk.txt` lines 6-44 (HUMAN QUESTION and OTHER OBSERVED QUESTIONS on the left, AFFECTED SESSION EVIDENCE on the right); `mockups/116/decision-desk.txt` (question full width, then two panes side by side); `mockups/80/decision-desk.txt` (three stacked panes).
- **Evidence:** the desk is a stacked block between the question list and the worker table, at every width:
```current/160/desk.txt
  59m  Name the release reviewer  reason unknown
DECISION DESK
msg_000000000000  age 1h
```
- **Category:** LAYOUT
- **Class:** PARITY-GAP (spec:43 and spec:57 chose "one stacked Decision Desk block" for R3; the two-column layout reverses that recorded choice and needs the owner's approval)
- **Severity:** High
- **Fix direction:** at 160 a left column (question pane over other-questions pane) and a right session-evidence pane; at 116 the question pane full width over two side-by-side panes; at 80 stacked framed panes.

#### F-opus-31: The desk leads with an id line, not the question
- **Mockup:** `mockups/160/decision-desk.txt` line 7: the first line inside the amber pane is the question text in bold amber; age is a secondary line.
- **Evidence:** title, then message id and age, then the question text in plain weight:
```current/116/desk.txt
DECISION DESK
msg_000000000000  age 1h
Choose schema compatibility policy
```
- **Category:** INFO-HIERARCHY
- **Class:** PARITY-GAP
- **Severity:** Medium
- **Fix direction:** put `DECISION DESK` in the pane border, the question text first in bold amber, then the id and age muted on one line.

#### F-opus-32: Linked session fields are an unaligned `label: value` dump
- **Mockup:** `mockups/160/decision-desk.txt` lines 6-15, right pane: a caption line, then per session a cyan state line and a muted detail line.
- **Evidence:** nine plain lines, labels and values the same weight and not aligned:
```current/160/desk.txt
dispatchId: w-001
workerState: running
nextAction.kind: wait
resource.worktreeId: wt-1
```
- **Category:** TYPOGRAPHY-EMPHASIS
- **Class:** PARITY-GAP (the raw labels are spec-required, spec:57; only the presentation is the gap)
- **Severity:** Medium
- **Fix direction:** a two-column key/value grid with labels muted in a fixed-width column and values in base colour (state values coloured as in F-opus-14), inside a slate `SESSION EVIDENCE` pane.

#### F-opus-33: Multi-session Affected list, owner and scope lines
- **Mockup:** `mockups/160/decision-desk.txt` lines 8-10 (`Owner: Human operator`, `Scope: 4 sessions`, `Affected: S001, S011, S021, S031`) and the four-session evidence pane (`4/4 shown`).
- **Evidence:** the desk links exactly one session and says so:
```current/80/desk.txt
worktree is evidence for this one session; other sessions in it are not
inferred affected
```
- **Category:** INFO-HIERARCHY
- **Class:** ACCEPTED-DIVERGENCE: no owner or multi-session affected source; spec:57 (AC-7) forbids inferring other sessions from a shared worktree.
- **Severity:** Low
- **Fix direction:** none; keep the note, styled muted at the foot of the evidence pane.

#### F-opus-34: No OTHER OBSERVED QUESTIONS pane
- **Mockup:** `mockups/160/decision-desk.txt` lines 16-44, slate pane with the other questions in bold amber and `2/2 other questions shown`.
- **Evidence:** the other questions appear only as plain list lines above the desk:
```current/160/desk.txt
  59m  Confirm deployment window  reason unknown
```
- **Category:** LAYOUT
- **Class:** PARITY-GAP (owner and `2 affected` sub-lines are ACCEPTED-DIVERGENCE: no source)
- **Severity:** Low
- **Fix direction:** in the two-column desk let the question list itself become the other-questions pane, with a `n/m questions shown` foot.

#### F-opus-35: The retention note is separated from the question list by the desk
- **Mockup:** `mockups/160/decision-desk.txt`: each pane's notes sit at its own foot (`2/2 other questions shown`).
- **Evidence:** on the questions screen the note follows the list; on the desk screen the desk block sits between them (`render.py:383-387` appends panel notes after the desk):
```current/116/desk.txt
worktree is evidence for this one session; other sessions in it are not inferred affected
retention reset at 12:00; questions observed before this start are not retained
```
- **Category:** INFO-HIERARCHY
- **Class:** DEFECT
- **Severity:** Low
- **Fix direction:** keep panel notes directly under the question list (or in the list pane's foot), before the desk.

#### F-opus-36: Selection shown by a glyph only, and the worker table still repeats under the desk
- **Mockup:** `mockups/160/decision-desk.txt`: the selected question is the content of the amber pane, and the screen holds only the desk panes (no worker table).
- **Evidence:** the selected row differs only by `▸`, and the full worker table (with `w-001` again) follows the desk:
```current/160/desk.txt
▸ 1h  Choose schema compatibility policy  reason unknown
   w-001                  run-0        running      active         active         none         wait             alive (terminal)       3s
```
- **Category:** INTERACTION
- **Class:** PARITY-GAP for emphasis on the selected line (bold amber; no reverse video or blink needed). The worker table staying on screen and the absent `tab pane` focus are ACCEPTED-DIVERGENCE: spec:39 keeps the ledger in this view and spec:13 rules out multi-pane focus.
- **Severity:** Low
- **Fix direction:** style the selected question line bold amber in addition to `▸`; in the two-column desk, give the worker table the lower band so the desk panes come first.

## Coverage: screen and width

Cross-screen findings F-opus-01, 02, 03, 07 and 08 hold at every screen and width (no file at any width has escape bytes, a pane border or an ASCII box path). The table lists the findings whose quoted evidence comes from that exact current file. Every one of the nine combinations has at least one finding, so there is no "none found" line.

| Screen | 160 | 116 | 80 |
|---|---|---|---|
| ledger (`ledger.txt` vs `signal-bridge`) | 01, 04, 05, 06, 09, 10, 12, 13, 14, 15 | 11, 16, 17, 18 | 04, 16, 19, 20 |
| questions (`questions.txt` vs `agent-focus-attention-ledger`) | 03, 07, 21, 22, 23, 24, 27 | 02, 23, 26, 28 | 17, 20, 25, 29 |
| desk (`desk.txt` vs `decision-desk`) | 01, 30, 32, 34, 36 | 08, 31, 35 | 03, 28, 33 |

## Summary

- 36 findings: 24 PARITY-GAP, 7 DEFECT (F-opus-07, 16, 17, 19, 25, 28, 35), 5 ACCEPTED-DIVERGENCE (F-opus-05, 12, 15, 26, 33).
- Severity: 5 High (F-opus-01 no styling, 03 no panes, 09 ledger layout, 21 questions layout, 30 desk layout), 16 Medium, 15 Low.
- Two of the High layout gaps (F-opus-21, F-opus-30) reverse choices recorded in the spec (spec:43 and spec:57, "one stacked block"); they need the owner's approval before a fix plan adopts the mockup columns.
- The SIGNALS bars (F-opus-12) stay out: spec:20 forbids bars on the COUNTS strip and spec:93 records no verified settled mapping.

## Quote check

Every line inside a fenced block whose info string is `current/<width>/<file>.txt` was checked as a whole line with `grep -qxF` against that file under `inputs/`: 73 quoted lines, 0 missing (run 2026-11-17, after the last content edit). Mockup line numbers were rechecked with `grep -n` against the mockup `.txt` files and corrected where they were off.
