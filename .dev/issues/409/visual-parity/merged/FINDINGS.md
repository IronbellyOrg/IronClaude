# Visual parity findings, merged (issue #606, sub-issue of #409)

- **Date:** 2026-11-17
- **Reviewers:** Opus 5.5 (`claude-opus-5-5`) and GPT 6 Astra (`gpt-6-astra`), each confirmed from its own file header. Each worked from the same inputs, then debated in three file rounds. Coordinator: the main session (merged, ruled and re-checked here).
- **Sources (all under `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/issues/409/visual-parity/`):** `round1/opus-findings.md` (36 findings), `round1/astra-findings.md` (13), `round2/opus-response.md`, `round2/astra-response.md`, `round3/opus-final.md`, `round3/astra-final.md`.
- **Scope rule used:** replicate the theme, styling and layout techniques of the mockups, not the images. A difference caused by data the observer does not have, or by a standing constraint, is an accepted divergence, not a fix request.
- **Evidence limits:** the renders are synthetic captures (`inputs/current/<width>/*.txt`); no live observer, no NO_COLOR or ASCII capture and no product test was run by anyone. The reviewers' quoted lines were machine-checked against the captures by each reviewer; the coordinator re-checked the 36 current-render lines quoted below as whole lines against the captures (all present; the ANSI exports hold 0 escape bytes).
- **Ids:** M-nn is a merged finding; the reviewers' own ids are listed so every one of the 49 round-1 findings can be traced (see "Trace").

## Summary

| Class | Count |
|---|---|
| Findings to fix (PARITY-GAP or DEFECT) | 18: 5 High, 9 Medium, 4 Low |
| Of these, DEFECT (plain rendering bug, not only a mockup difference) | 3: M-08, M-10, M-11 |
| Spec guards (acceptance criteria for the fix, not present defects) | 2: G-1, G-2 |
| Accepted divergences | 7: AD-1 to AD-7 |
| Open items (both final positions kept) | 3 severity or scope items (OPEN-1 to OPEN-3) and 1 owner decision (O-1) |

**Verdict:** the visual-parity gap is real and large. Both reviewers independently confirmed all five claims in the issue: zero escape bytes in all nine ANSI exports, no titled panes, no two-column desk, no count tile, no RETAIN CONTEXT pane. The three screens at three widths each have at least one finding.

**Needs the owner (O-1):** two High layout findings (M-03 questions screen, M-04 Decision Desk) reverse the recorded rendering choice "one stacked block at every width" (`rendering-rules.md` lines 43 and 57). Adopting columns at 160 and 116 needs the owner to say yes. Both reviewers agree on this.

## Findings to fix

### High

#### M-01: No colour or weight styling anywhere (THEME-COLOUR, PARITY-GAP, High)
- Reviewer ids: F-opus-01, F-astra-04. Agreed by both.
- Mockups: every `mockups/<width>/*.ansi` (24-bit foreground only: base, amber, cyan, slate, muted, green, red, violet; bold on titles and counts).
- Current: all nine `inputs/current/<width>/ansi-*.txt` hold 0 escape bytes; `render.py` builds `Text(line, no_wrap=True, overflow="crop")` per line with no style. Example, the title line is plain: `ORCA OBSERVER  mode=fixture  SYNTHETIC FIXTURE base, not Orca data  scope=all  as of 12:00:00`.
- Fix direction: styled spans from one named theme (semantic roles, not fixed RGB), same text so NO_COLOR and the text records stay identical. Acceptance checks inside this item: M-08 (muted unknowns) and M-09 (state colours).

#### M-02: No boxed, titled panes (FRAME-PANE, PARITY-GAP, High)
- Reviewer ids: F-opus-03, F-astra-05. Agreed by both.
- Mockups: `mockups/160/decision-desk.txt`, `mockups/160/signal-bridge.txt` (heavy amber boxes for attention content, rounded slate boxes for secondary content, cyan for counts, titles inset in the border).
- Current: section titles are bare lines: `COORDINATOR QUESTIONS`, `worker-reported, not questions`, `DECISION DESK`.
- Fix direction: frame each logical region with a titled pane; attention region emphasised, supporting regions subordinate; required caveat text is kept in full, never squeezed into a border title (Astra, accepted by Opus in round 3).

#### M-03: Questions screen has no two-column composition (LAYOUT, PARITY-GAP, High; needs O-1)
- Reviewer ids: F-opus-21; F-astra-03 (part). Astra agreed.
- Mockups: `mockups/160/agent-focus-attention-ledger.txt` and `mockups/116/agent-focus-attention-ledger.txt`: questions pane on the left; count tile and context pane on the right. At 80 the mockup stacks.
- Current: one stacked column: `COORDINATOR QUESTIONS`, `one Run only: run_14cfcbd8edf2`, `question read: OK 0s`, then the list, then the worker table.
- Fix direction: at 160 and 116 questions left, count tile and supported-context pane right; stacked framed panes at 80. Reverses `rendering-rules.md` line 43 (O-1).

#### M-04: Decision Desk stacked, not two-column (LAYOUT, PARITY-GAP, High; needs O-1)
- Reviewer ids: F-opus-30, F-astra-06; parts of F-opus-34 (other-questions pane) and F-opus-36 (worker table repeated under the desk). Agreed by both.
- Mockups: `mockups/160/decision-desk.txt` (question and other questions left, evidence right); `mockups/116/decision-desk.txt` (question full width over two side-by-side panes); `mockups/80/decision-desk.txt` (three stacked panes).
- Current: the desk is one tall column between the list and the worker table: `DECISION DESK`, `msg_000000000000  age 1h`, `Choose schema compatibility policy`, `dispatchId: w-001`.
- Fix direction: question and linked-session evidence side by side at 160 and 116, stacked at 80; the single linked session is shown as one session and no affected list is invented (AD-4). Lets the question list act as the "other questions" pane. Reverses `rendering-rules.md` lines 43 and 57 (O-1).

#### M-05: SEEN IS NOT RESOLVED count has no visual weight (INFO-HIERARCHY, PARITY-GAP, High)
- Reviewer ids: F-opus-22, F-astra-01. Both High (Opus raised its Medium in round 2).
- Mockups: `mockups/160/agent-focus-attention-ledger.txt` lines 6-18 and `mockups/116/agent-focus-attention-ledger.txt` (cyan-framed tile, large amber digit, caption).
- Current: `seen, not resolved: 3 | closed by evidence: unavailable (no source)`, same weight as the caveat lines around it.
- Fix direction: a framed tile with a prominent count at 160 and 116. Keep the exact text forms for NO_COLOR, ASCII and 80 columns (`SEEN IS NOT RESOLVED n`, `100+ (window full)`, `unknown (...)`, `closed by evidence: unavailable (no source)`). An exact five-row block digit is not required.

### Medium

#### M-06: Ledger has no attention slot, observation pane or count tiles (LAYOUT / FRAME-PANE, PARITY-GAP, Medium)
- Reviewer ids: F-opus-09 (reviewer rated High), F-opus-10, F-opus-11, F-opus-13; F-astra-05 (part). Severity settled at Medium: Opus compromised to Medium in round 3, Astra held Medium.
- Mockups: `mockups/160/signal-bridge.txt` lines 6-44 (HUMAN QUESTION pane, OBSERVATION WINDOW, SESSION REGISTER, SIGNALS tiles); `mockups/80/signal-bridge.txt` (stacked).
- Current: one full-width table under bare titles; the question gap notice and the source freshness are run-on lines: `Human questions: source UNVERIFIED, 0 rows interpreted, not "no questions"`, `worker-list OK 0s  messages UNVERIFIED (not read)`, and the counts mid-line: `collected 80 / reported 80  scope=all  source counts: active 54 / reclaimable 0 / retained 13 / released 13  runs seen: 8  SETTLED unavailable (no source)`.
- Decisive measurement (Opus, re-checked by the coordinator below): the mockup's centre register pane is 74 cells wide; the spec's full ledger needs 153 cells (`rendering-rules.md` line 30), so an exact three-column grid would drop spec-required columns. **Exact three columns are not required.**
- Fix direction (both reviewers accept this geometry): a framed compact source-gap notice in the attention style, a framed secondary source-freshness region, source counts as tiles (160) or a bold strip (116, 80), then one full-width titled worker register; side by side at wide widths where everything fits, stacked at 80. No bars and no invented states (AD-2).

#### M-07: Question list: caveats outweigh the questions, no row emphasis or separation (INFO-HIERARCHY, PARITY-GAP, Medium; see OPEN-1)
- Reviewer ids: F-astra-03 (High, umbrella), F-opus-23, F-opus-24 (Medium), F-opus-25 (Low component, age gutter).
- Mockup: `mockups/116/agent-focus-attention-ledger.txt` (first content line of the pane is the question; ages in a fixed gutter; bold question text; rules between questions).
- Current at 116: seven title, scope and caveat lines before three equal-weight rows:
  `bounded best effort; coverage unknown; at most 100 rows per read, not 100 questions; bursts over 100 rows between` / `reads may be lost` / `  1h  Choose schema compatibility policy  reason unknown` / `  59m  Confirm deployment window  reason unknown`.
- Fix direction: keep every required caveat visible but subordinate (muted, pane foot or title area); question text and age emphasised; separation between rows; age gutter sized for the widest age and the optional bracket text.
- **Component, ruled PARITY-GAP Low (not a DEFECT):** the age offset (`  1h  ...` against `  59m  ...`) follows the spec format `<age>  [no longer in source window]  <subject>  reason unknown` (`rendering-rules.md` line 50), so the output matches the spec; it is typography.

#### M-08: Absent values are not muted (THEME-COLOUR, DEFECT, Medium)
- Reviewer ids: F-opus-07. Astra: AGREE.
- Rule unmet: `rendering-rules.md` line 70, absent field is "literal `unknown`, muted (plain under NO_COLOR)".
- Current: `  59m  Confirm deployment window  reason unknown`, and `source counts: unknown` in the questions-screen header.
- Fix direction: mute every `unknown` and `unavailable (no source)` token in colour mode; plain under NO_COLOR.

#### M-09: State values carry no state colour (THEME-COLOUR, PARITY-GAP, Medium)
- Reviewer ids: F-opus-14. Astra: AGREE.
- Mockup: `attachments/signal-bridge.png`, `mockups/160/signal-bridge.ansi` (running cyan, settled green, failed red, frozen violet, stale amber).
- Current: `   w-002                  run-c        blocked      blocked        active         none         review           alive (terminal)       13s` looks like an idle row.
- Fix direction: colour the raw `workerState` and `dispatchStatus` text from a fixed table; unknown values neutral; `nextAction.kind` stays uncoloured and verbatim (`rendering-rules.md` line 31). No invented "settled" mapping (AD-2).

#### M-10: No column heading at 116 and 80 (DEGRADED-WIDTH, DEFECT, Medium; coordinator ruling R-1)
- Reviewer ids: F-opus-16, F-astra-07. Both agree on the fix and on Medium. They disagree on the class (see R-1).
- Mockups: `mockups/116/signal-bridge.txt` line 15, `mockups/80/signal-bridge.txt` line 17 (caption line at every width).
- Current: `   none               w-001                                                alive          10s` (116) and `   none           w-001                                  10s` (80): the first value is a bare `nextAction.kind` with nothing saying so.
- Evidence for the class: `render.py` `_columns` defines the compact names `kind`, `dispatchId`, `liveness`, `age` for the 116 and 80 widths, but `render()` prints a header only when `policy.width_class == "full"`. The headings exist and are suppressed by one condition.
- Fix direction: a short muted heading at every width; no new fields; `kind` is not classified.

#### M-11: 80-column ledger key list is cut; `q quit` lost (KEYS-FOOTER, DEFECT, Medium)
- Reviewer ids: F-opus-19, F-astra-08. Both: DEFECT, Medium.
- Mockup: `mockups/80/signal-bridge.txt` line 41 (whole hint line fits).
- Current: `Up/Down j/k move  Enter detail  Esc back  / filter  h historical  m mark  e exp>`.
- Cause: `_help_lines` clips the key list when questions are off and wraps it only when they are on.
- Fix direction: never cut the key list; wrap it between key groups (or shorten labels) at 80.

#### M-12: Decision Desk: the question does not lead and the evidence is an unaligned dump (TYPOGRAPHY-EMPHASIS / INFO-HIERARCHY, PARITY-GAP, Medium)
- Reviewer ids: F-opus-31, F-opus-32; F-astra-06 (part). Both Medium.
- Mockup: `mockups/160/decision-desk.txt` lines 6-15 (question in bold amber; evidence as aligned state and detail lines).
- Current: `DECISION DESK` / `msg_000000000000  age 1h` / `Choose schema compatibility policy` then `dispatchId: w-001`, `workerState: running`, `nextAction.kind: wait`, `resource.worktreeId: wt-1` (labels and values same weight).
- **Ruling:** the line order stays as the spec fixes it (title, id and age line, question text; `rendering-rules.md` line 57). Both reviewers agree moving the id line is not required. The fix is emphasis: question text bold in the attention colour, id and age muted, evidence as a muted-label, base-colour-value grid with state colours (M-09).

#### M-13: Title bar: no read-only badge and no title and mode split (TYPOGRAPHY-EMPHASIS, PARITY-GAP; see OPEN-3)
- Reviewer ids: F-opus-04, F-astra-10.
- Mockup: all nine mockups, line 2: bold title at the left, `SYNTHETIC · READ ONLY` right-aligned in amber, muted freshness line.
- Current: `ORCA OBSERVER  mode=fixture  SYNTHETIC FIXTURE base, not Orca data  scope=all` / `as of 12:00:00` (80), one run-on line with no READ ONLY (160). 
- Agreed: the READ ONLY badge is in scope; title weight and colour belong to M-01 and the frame to M-02 (no double counting); the 80-column clock wrap is not a separate point. Severity and the right-alignment scope are OPEN-3. The header contract in `rendering-rules.md` (line 17) must be reconciled deliberately, not silently changed.

#### M-14: RETAIN CONTEXT: supported facts are scattered (INFO-HIERARCHY / FRAME-PANE, PARITY-GAP; see OPEN-2)
- Reviewer ids: F-astra-02, F-opus-27, F-opus-35 (note placement, ruled a gap, not a DEFECT: the note text is correct, visible and applies to the enclosing panel).
- Mockup: `mockups/160/agent-focus-attention-ledger.txt` lines 21-38 (low-contrast slate pane listing retained attributes).
- Current: the facts exist in three places: `one Run only: run_14cfcbd8edf2`, `no read marker in source: answered questions stay listed`, `retention reset at 12:00; questions observed before this start are not retained`. The earlier claim "only the retention note exists" was too narrow (Opus withdrew it).
- Agreed fix: group only supported facts (Run scope, closure availability, process-local retention) in a subordinate pane at 160 and 116; attributes with no source are omitted or shown `unavailable (no source)`; a mostly-unavailable seven-row panel is not wanted; at 80 the context stays compact (`rendering-rules.md` line 61); question text stays screen-only. `rendering-rules.md` line 41 calls this pane a design reference not built in R2, so adding it also changes the spec.

### Low

#### M-15: Footer: key pairs split by wrapping, no rule or separators (KEYS-FOOTER, PARITY-GAP, Low; coordinator ruling R-2)
- Reviewer ids: F-opus-28, F-astra-09, F-opus-06.
- Current at 116: `Up/Down j/k move workers  Enter detail  Esc back  / filter  h historical  m mark rows  e export all  q quit  n/p` then `question`. Every key and action is printed; the pair `n/p question` is split.
- Fix direction: wrap only between key groups (the double-space gaps), a slate rule above the footer, muted hints, counts on their own line.

#### M-16: 80-column counts are cut inside a token (DEGRADED-WIDTH, PARITY-GAP, Low)
- Reviewer ids: F-opus-20. Astra: AGREE.
- Current: `source counts: active 54 / reclaimable 0 / retained 13 / released 13  runs seen>` and `SETTLED unavailable (no source)  POLICY FROZEN unavailable (no source)  cost un>`. Legal under `rendering-rules.md` line 20 but leaves a fragment.
- Fix direction: drop whole low-priority tokens (with a count of what is hidden) instead of cutting inside one.

#### M-17: Wide blank band after the id at 116 and 80 (LAYOUT, PARITY-GAP, Low; optional)
- Reviewer ids: F-opus-17. Both final: PARITY-GAP Low (Opus conceded DEFECT; values are aligned, correctly paired and in the specified order).
- Current: `   review             w-002                                                alive          13s` (116), `   wait           w-001                                  3s` (80).
- Fix direction (optional): tighter id allocation for short ids; Astra's caution stands: dynamic widths must not shift columns between refreshes, and real ids must still fit.

#### M-18: Selected question marked by a glyph only (INTERACTION, PARITY-GAP, Low)
- Reviewer ids: F-opus-36 (the gap part). Astra: PARTIAL (accepts the accepted-divergence part).
- Current: `▸ 1h  Choose schema compatibility policy  reason unknown`.
- Fix direction: bold attention colour on the selected line in addition to the glyph; no blink, no reverse video, no mouse.

## Spec guards (not present defects; acceptance criteria for the fix)

- **G-1 ASCII panes (F-opus-08, both: SPEC-GUARD).** Today the only non-ASCII drawing characters are `─` and `▸`, and both have ASCII forms (`terminal.py` `GLYPHS`). New panes must emit `+`, `-` and `|` under `--ascii` (`rendering-rules.md` line 25), never fall through to `?` borders; NO_COLOR and ASCII keep the hierarchy through text, bold and glyphs.
- **G-2 Colour depth (F-opus-02, both: SPEC-GUARD).** `terminal.py` builds the console with `color_system=None if policy.no_color else "standard"`. With no styles today nothing is lost; once styled, the theme must keep its roles distinct at the real capability (truecolor, 256 or 16), and NO_COLOR stays `None`. Exact 24-bit values are not required. The spec decides the targeted depth and detection (the issue asks it to).

## Accepted divergences (not fix requests)

| Id | Difference | Reason | Reviewer ids |
|---|---|---|---|
| AD-1 | Header line "8 owners / 80 sessions / 80 mapped trees" | No owner or mapped-tree data; the COUNTS strip (`rendering-rules.md` line 20) is the real-data equivalent. Only its styling is in scope (M-01). | F-opus-05, F-astra-11 |
| AD-2 | SIGNALS bars; SETTLED, POLICY FROZEN, UNKNOWN, STALE tiles | `rendering-rules.md` line 20 ("no bars, no health name") and line 93 (no verified settled mapping); no source. Muted `unavailable (no source)` stays. | F-opus-12, F-astra-11 |
| AD-3 | Two-line register rows and prose lifecycle words | The spec requires separate raw fields and a verbatim `nextAction.kind` (lines 30-31); admission and frozen state have no source. | F-opus-15 |
| AD-4 | Requester, owner, `Affected:` list, scope count, `4 sessions shown` | No requester, owner or multi-session source; a shared worktree must not be read as affected sessions (line 57). One linked session is shown as one. | F-opus-26, F-opus-33, F-astra-12 |
| AD-5 | Different key map; no `tab pane` focus; worker ledger stays under the desk | `rendering-rules.md` lines 13, 21 and 39. | F-opus-36 (accepted part), F-astra-13 |
| AD-6 | No `workerState` column at 80 (and optional at 116) | Compact forms are fixed by `rendering-rules.md` line 33; an extra column at 116 is optional once M-17 frees room. | F-opus-18 |
| AD-7 | Missing 80-column sentence "Questions stay until explicit resolution." and a forced focused card with no selection | The sentence would promise more than the observer keeps (`rendering-rules.md` line 42: in memory, this process only; reset notice); a card with no selection would invent a selection. Both reviewers agree the older design slogan loses to the truthful retention text. A qualified retention line and the no-reply-is-not-failure reminder are optional. | F-opus-29 (rejected), F-astra-13 |

## Coordinator rulings (where the two final positions crossed)

The reviewers answered round 3 without seeing each other's final file, so on three class points each conceded to the other's old position and they ended up swapped. I ruled by the evidence below, not by model.

- **R-1 (M-10) DEFECT, Medium.** The compact heading names already exist in `_columns` and one condition (`width_class == "full"`) suppresses them, leaving a verbatim `nextAction.kind` value unlabelled at the two compact widths. If the owner states the suppression was intentional, reclassify as PARITY-GAP; the fix and the severity do not change.
- **R-2 (M-15) PARITY-GAP, Low.** No key or action is lost; the `_help_lines` promise "no key is cut" is kept literally. The class is Low either way.
- **R-3 (M-07 component) PARITY-GAP, Low.** The age offset follows the specified format (`rendering-rules.md` line 50).

## Open items (both final positions kept; nobody's tie is broken here)

- **OPEN-1, severity of the question-list hierarchy (M-07).** Astra: High, as one combined item with Low and Medium components. Opus: Medium, to avoid counting the same lost question primacy three times (it is already High as M-01, M-02 and M-03); Opus says it should go back to High only if M-03 is not counted as High. M-03 is High (both agreed), so by Opus's own condition it is Medium. Handling in the spec: treated as Medium (gated).
- **OPEN-2, severity of RETAIN CONTEXT (M-14).** The final positions crossed: Opus ended at Medium (grouping three scattered facts is a real hierarchy gain), Astra ended at Low (low-contrast secondary pane, content partly unavailable, design reference only). Handling in the spec: treated as Medium (gated) until the owner rules; it is scheduled in a late phase either way.
- **OPEN-3, title bar (M-13).** Opus: Low, with the left-title and right-badge split in scope (it appears on line 2 of all nine mockups, so it is a technique). Astra: Medium for one combined identity-region item, with the badge a Low component and exact left and right alignment and the diamond glyph optional. Handling in the spec: treated as Medium (gated); the badge is required, exact alignment is the owner's or the claiming agent's call.
- **O-1, owner decision.** Adopt two-column layouts for the questions screen and the Decision Desk at 160 and 116, reversing the "one stacked block" choice in `rendering-rules.md` lines 43 and 57? Recommendation: yes, because the visual-parity target requires it, with 80 columns staying stacked and the spec text updated in the same change.

The "gated as Medium" handling exists because a phase may close only when all High and Medium criteria pass: it is the cautious reading of a severity the two reviewers could not settle.

## Coverage: screen and width

Every combination has at least one finding (findings whose quoted evidence comes from that exact capture; cross-screen findings M-01, M-02, G-1, G-2 hold at all nine).

| Screen | 160 | 116 | 80 |
|---|---|---|---|
| ledger | M-01, M-06, M-09, M-13, M-15 | M-06, M-10, M-16, M-17 | M-10, M-11, M-13, M-16 |
| questions | M-03, M-05, M-07, M-08, M-14 | M-03, M-07, M-15 | M-07, M-14, M-16, AD-7 |
| desk | M-04, M-12, M-18 | M-04, M-12, M-14 | M-04, M-12, M-15 |

## Trace: every round-1 finding to its merged id

| Reviewer id | Merged | | Reviewer id | Merged |
|---|---|---|---|---|
| F-opus-01 | M-01 | | F-opus-19 | M-11 |
| F-opus-02 | G-2 | | F-opus-20 | M-16 |
| F-opus-03 | M-02 | | F-opus-21 | M-03 |
| F-opus-04 | M-13 | | F-opus-22 | M-05 |
| F-opus-05 | AD-1 | | F-opus-23, 24, 25 | M-07 |
| F-opus-06 | M-15 | | F-opus-26 | AD-4 |
| F-opus-07 | M-08 | | F-opus-27 | M-14 |
| F-opus-08 | G-1 | | F-opus-28 | M-15 |
| F-opus-09, 10, 11, 13 | M-06 | | F-opus-29 | AD-7 |
| F-opus-12 | AD-2 | | F-opus-30 | M-04 |
| F-opus-14 | M-09 | | F-opus-31, 32 | M-12 |
| F-opus-15 | AD-3 | | F-opus-33 | AD-4 |
| F-opus-16 | M-10 | | F-opus-34 | M-04 |
| F-opus-17 | M-17 | | F-opus-35 | M-14 |
| F-opus-18 | AD-6 | | F-opus-36 | M-18, AD-5 |
| F-astra-01 | M-05 | | F-astra-08 | M-11 |
| F-astra-02 | M-14 | | F-astra-09 | M-15 |
| F-astra-03 | M-07, M-03 | | F-astra-10 | M-13 |
| F-astra-04 | M-01 | | F-astra-11 | AD-1, AD-2 |
| F-astra-05 | M-02, M-06 | | F-astra-12 | AD-4 |
| F-astra-06 | M-04, M-12 | | F-astra-13 | AD-5, AD-7 |
| F-astra-07 | M-10 | | | |
