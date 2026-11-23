# Round 2 response: reviewer "opus" on astra's round-1 findings (issue #606)

- **Model id:** claude-opus-5-5 (Opus 5.5)
- **Reviewer:** opus
- **Date:** 2026-11-17
- **Task:** task_04108390b3db (round 2, debate).
- **Read:** `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/issues/409/visual-parity/round1/astra-findings.md` (13 findings, F-astra-01 to F-astra-13) and my own `round1/opus-findings.md` (36 findings). No other file in `round2/` was opened.
- **Re-checked for this response:** every line inside astra's ```` ```text ```` blocks was matched as a whole line (`grep -qxF`) against `inputs/current/*/*.txt`: 68 lines, 0 missing. Re-read `src/superclaude/cli/observe/render.py` lines 62-80 (`wrap`), 304-308 (`_help_lines`) and 495-498 (header gate), `rendering-rules.md` lines 13, 20, 21, 25, 31, 33, 40, 41, 43, 57, 61, 70 and 93 (cited as `spec:<line>`), and the RETAIN CONTEXT border colour in `inputs/mockups/160/agent-focus-attention-ledger.ansi` line 21 (slate `38;2;82;108;128`).
- **Verdict words:** AGREE, PARTIAL (what I would change), DISAGREE (with re-checked evidence). Where I change one of my own round-1 positions, the change is stated in section 2.

## 1. Verdict on each astra finding

| astra id | Verdict | Reason (and what I would change) | Overlaps opus id |
|---|---|---|---|
| F-astra-01 (SEEN count has no weight; TYPOGRAPHY-EMPHASIS, PARITY-GAP, High) | AGREE | The tile is one of the three panes of the attention-ledger screen at 160 and 116 (`mockups/160/agent-focus-attention-ledger.txt` lines 6-18) and spec:40 itself asks for a "big count of observed open questions"; High is right. I raise my F-opus-22 from Medium to High (section 2). Agree that no tile is required at 80 (spec:61 asks only for `SEEN IS NOT RESOLVED n`). | F-opus-22 |
| F-astra-02 (RETAIN CONTEXT; INFO-HIERARCHY, PARITY-GAP, Medium) | PARTIAL: severity Low, not Medium | Agree on class, on the gap and on the fix (only supported facts, others shown unavailable). Severity: in the mockup it is the lowest-contrast secondary pane (slate border, `mockups/160/agent-focus-attention-ledger.ansi`), spec:41 marks it "design reference; not built in R2", and of its seven attributes at least two (requesting orchestrator, affected stable IDs) have no source, so its effect on theme parity is smaller than the primary panes. | F-opus-27 |
| F-astra-03 (caveats dominate the question list; INFO-HIERARCHY, PARITY-GAP, High) | PARTIAL: split one part out as a DEFECT | Agree with the substance and with High for the combined "question list hierarchy" item (I concede my Medium on F-opus-23 and F-opus-24; section 2). One part is a plain rendering bug, not parity: the age gutter is unaligned, so question text starts one column later after a 3-character age (`  1h  Choose schema compatibility policy  reason unknown` vs `  59m  Confirm deployment window  reason unknown`, `current/116/questions.txt`). Keep that as a separate Low DEFECT (F-opus-25). | F-opus-23, F-opus-24, F-opus-25 |
| F-astra-04 (no colour or weight styling; THEME-COLOUR, PARITY-GAP, High) | AGREE | Same result: 0 escape bytes in all nine current ANSI exports, and `render.py` builds plain `Text`. It does not cover the 16-colour console limit (my F-opus-02, section 2). | F-opus-01 |
| F-astra-05 (no titled panes; FRAME-PANE, PARITY-GAP, High) | AGREE | Same finding. Its fix line ("ASCII-safe alternatives") touches my F-opus-08 but does not name the spec:25 ASCII box mapping (plus, minus, bar) or the `ascii_safe` `?` substitution. | F-opus-03 (and partly F-opus-08) |
| F-astra-06 (wide desk ignores horizontal space; LAYOUT, PARITY-GAP, High) | AGREE | Same finding. Its note that the worker table repeats the linked worker also matches part of my F-opus-36. Both of us record that spec:43/57 chose a stacked desk, so adopting columns needs the owner's approval. | F-opus-30 (and part of F-opus-36) |
| F-astra-07 (compact rows lose field labels; DEGRADED-WIDTH, PARITY-GAP, Medium) | PARTIAL: class DEFECT, not PARITY-GAP; category DEGRADED-WIDTH accepted | Same defect and same severity. I hold DEFECT: the header is printed only when `policy.width_class == "full"` (`render.py:497`), so at 116 and 80 a bare `nextAction.kind` value (`   none               w-001                                                alive          10s`, `current/116/ledger.txt`) sits under the title `worker-reported, not questions` with nothing saying it is a next-action kind. spec:31 requires that value to be "verbatim" and never "classified"; an unlabeled `wait` next to a question list reads as a worker state. That is a bug at a supported width whatever the mockup shows. I take astra's category DEGRADED-WIDTH over my INFO-HIERARCHY. | F-opus-16 |
| F-astra-08 (80 ledger cuts the quit key; KEYS-FOOTER, DEFECT, Medium) | AGREE | Same finding and class. Root cause re-checked: `_help_lines` clips the key list when questions are off and wraps it only when they are on (`render.py:304-308`). I take astra's category KEYS-FOOTER over my DEGRADED-WIDTH. | F-opus-19 |
| F-astra-09 (wrapped hints split key from action; KEYS-FOOTER, PARITY-GAP, Low) | PARTIAL: class DEFECT, not PARITY-GAP | Same lines, same severity. I hold DEFECT: `wrap` breaks at the last single space that fits (`render.py:72-75`, `paragraph[:cut].rfind(" ")`), but the key list's unit is the double-space group, so `n/p` and `question` land on different lines (`Up/Down j/k move workers  Enter detail  Esc back  / filter  h historical  m mark rows  e export all  q quit  n/p` then `question`, `current/116/questions.txt`). The `_help_lines` docstring promises "no key is cut"; a key separated from its action defeats that promise. No information lost is why it is Low, not why it is not a bug. | F-opus-28 |
| F-astra-10 (no READ ONLY marker; TYPOGRAPHY-EMPHASIS, PARITY-GAP, Low) | PARTIAL: merge into a wider title-bar finding at Medium | The missing READ ONLY word is real. My F-opus-04 covers the whole title-bar technique: bold left title, right-aligned amber mode badge, muted second line, and the 80-column wrap that pushes `as of 12:00:00` onto its own line (`current/80/ledger.txt`). The merged item affects every screen's first line, so Medium. | F-opus-04 |
| F-astra-11 (bars and invented states intentional; ACCEPTED-DIVERGENCE, Low) | AGREE | Same as my F-opus-05 and F-opus-12 (spec:20 "no bars", spec:93). Note that "accepted" covers the bars and the invented states only; the count-tile technique for the real source counts stays a gap (my F-opus-11). | F-opus-05, F-opus-12 |
| F-astra-12 (one linked worker is not an affected list; ACCEPTED-DIVERGENCE, Low) | AGREE | Same as my F-opus-33; the same reasoning covers requester/owner sub-lines on the question list (my F-opus-26). | F-opus-33, F-opus-26 |
| F-astra-13 (different keys and 80-column stacking valid; ACCEPTED-DIVERGENCE, Low) | AGREE | Matches the accepted part of my F-opus-36 (spec:13 no multi-pane focus; spec:21 key map) and my F-opus-30 fix direction (stacked panes at 80). | F-opus-36 (accepted part), F-opus-30 |

## 2. Findings astra missed, and my findings astra classifies differently

### 2a. Missed by astra (opus findings with no astra counterpart)

Ordered by severity. Each keeps the evidence and verbatim quotes given in `round1/opus-findings.md`.

- **F-opus-09 (High, LAYOUT): the ledger has no three-column Signal Bridge layout.** astra has no ledger-layout finding; F-astra-05 covers frames only and F-astra-06 covers the desk only. The ledger is the default screen, and `mockups/160/signal-bridge.txt` lines 6-44 show its three columns, against one full-width table in `current/160/ledger.txt`.
- **F-opus-21 (High, LAYOUT): the questions screen has no two-column layout.** astra's hypothesis table names two columns only for the desk; F-astra-03 is about hierarchy inside the stacked list. `mockups/{160,116}/agent-focus-attention-ledger.txt` place the questions pane left and the tile and context panes right. Like F-astra-06, this needs the owner's approval because spec:43 chose a stacked block.
- **F-opus-02 (Medium, THEME-COLOUR): the console is limited to 16 colours.** `terminal.py:121` sets `color_system="standard"`. Adding styles (F-astra-04's fix) would still snap the mockup's 24-bit amber, slate and muted greys to 16 ANSI colours, merging slate and muted. F-astra-04's fix direction ("restrained semantic ANSI palette") does not address it.
- **F-opus-07 (Medium, THEME-COLOUR, DEFECT): `unknown` is not muted.** spec:70 already requires "literal `unknown`, muted (plain under NO_COLOR)"; the render does not do it (`source counts: unknown`, `reason unknown` in `current/160/questions.txt`). This is a spec rule unmet, not only parity.
- **F-opus-08 (Medium, NO_COLOR-ASCII): no ASCII box path.** spec:25 maps box drawing to `+-|` under `--ascii`, but `ascii_safe` turns every non-ASCII character into `?` and `safe_box` does not force an ASCII box on a UTF-8 stream. Once panes are added, `--ascii` would print `?` borders unless this is planned. F-astra-05 mentions "ASCII-safe alternatives" without the mechanism.
- **F-opus-10, F-opus-11 and F-opus-13 (Medium): the ledger's OBSERVATION WINDOW pane, count tiles and HUMAN QUESTION slot.** Each uses data the observer already has (freshness cells, source counts, the gap notice), so they are not covered by F-astra-11's accepted divergence.
- **F-opus-14 (Medium, THEME-COLOUR): state values have no state colour.** F-astra-04 names "differentiated status colours" only in its mockup description, with no finding or fix for the rows (`   w-002                  run-c        blocked      blocked        active         none         review           alive (terminal)       13s`).
- **F-opus-17 (Medium, LAYOUT, DEFECT): the blank band of about 50 cells between id and liveness at 116 and 80** (`render.py:195` id width up to 60). F-astra-07 quotes these lines but only for the missing headings.
- **F-opus-31 and F-opus-32 (Medium): the desk leads with `msg_000000000000  age 1h` instead of the question, and the session fields are an unaligned `label: value` dump.** F-astra-06 quotes the same lines but only for column use.
- **Low findings astra missed:** F-opus-06 (footer rule and separators; F-astra-09's fix touches it), F-opus-18 (`workerState` dropped at 116 and 80), F-opus-20 (80-column COUNTS tokens cut mid-word: `... released 13  runs seen>`), F-opus-29 (80-column invariant lines from spec:61 absent), F-opus-34 (no other-questions pane), F-opus-35 (the retention note is separated from the list by the desk block, DEFECT).

### 2b. My findings astra classifies differently

- **F-opus-22 vs F-astra-01 (severity): I withdraw Medium and take High.** Reason: spec:40 makes the big count a required element of the wide layout, and it is one of the three panes of the screen.
- **F-opus-23 and F-opus-24 vs F-astra-03 (severity): I withdraw Medium and take High for the merged question-hierarchy item.** Reason: at 116 seven title and caveat lines come before three unemphasised question lines (`current/116/questions.txt` lines 5-14), and the question list is the purpose of the screen.
- **F-opus-25 vs F-astra-03 (class): I hold DEFECT, Low.** The misaligned age gutter is a layout bug regardless of the mockup (evidence in section 1).
- **F-opus-16 vs F-astra-07 (class): I hold DEFECT;** I accept the category DEGRADED-WIDTH. Evidence in section 1 (`render.py:497`, spec:31).
- **F-opus-28 vs F-astra-09 (class): I hold DEFECT, Low.** Evidence in section 1 (`render.py:72-75`).
- **F-opus-19 vs F-astra-08 (category): I withdraw DEGRADED-WIDTH and take KEYS-FOOTER.** The defect is the key list.
- **F-opus-27 vs F-astra-02 (severity): I hold Low.** Evidence in section 1 (slate secondary pane, spec:41 design reference, two attributes with no source).
- **F-opus-04 vs F-astra-10 (scope and severity): I hold Medium for the merged title-bar item;** F-astra-10's READ ONLY marker becomes one part of it.

## 3. Overlaps to merge (opus id with astra id)

- F-opus-01 with F-astra-04: no colour or weight styling.
- F-opus-03 with F-astra-05: no titled panes (F-opus-08 is the ASCII part of the same work).
- F-opus-30 with F-astra-06: the wide Decision Desk layout (part of F-opus-36, the worker table repeated under the desk, is also in F-astra-06).
- F-opus-22 with F-astra-01: the SEEN IS NOT RESOLVED count tile.
- F-opus-27 with F-astra-02: RETAIN CONTEXT.
- F-opus-23, F-opus-24 and F-opus-25 with F-astra-03: question-list hierarchy, emphasis and age alignment.
- F-opus-16 with F-astra-07: no column headings at 116 and 80.
- F-opus-19 with F-astra-08: the 80-column ledger key list cut.
- F-opus-28 with F-astra-09: key/action pairs split by wrapping.
- F-opus-04 with F-astra-10: title bar and READ ONLY badge.
- F-opus-05 and F-opus-12 with F-astra-11: accepted, no owners or mapped trees, no bars or settled states.
- F-opus-33 (and F-opus-26) with F-astra-12: accepted, one linked worker and no requester or owner.
- F-opus-36 (accepted part) and F-opus-30 (80-column stacking) with F-astra-13: accepted, key map and 80-column stacking.

## 4. Positions still disputed after this response

- F-astra-02 / F-opus-27: RETAIN CONTEXT severity, astra Medium against opus Low.
- F-astra-07 / F-opus-16: missing headings at 116 and 80, astra PARITY-GAP against opus DEFECT.
- F-astra-09 / F-opus-28: key/action split by wrapping, astra PARITY-GAP against opus DEFECT.
- F-astra-03 / F-opus-25: whether the age misalignment is a separate DEFECT or part of astra's PARITY-GAP.
- F-astra-10 / F-opus-04: READ ONLY marker alone at Low against the whole title bar at Medium.
- Not disputed but unanswered by astra: the 18 opus-only findings in 2a, including two High layout gaps (F-opus-09 ledger, F-opus-21 questions).
