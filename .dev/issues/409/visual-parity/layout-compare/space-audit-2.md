# Screen-space audit 2 (image-based): questions, Decision Desk, worker ledger

Method note: the six `layout-compare/*.png` files did not exist on disk. I rendered them from `layout-compare/screens/*.json` with the repo's `rasterise.py` (output to /tmp/sa2, nothing in the repo changed) and opened all six, plus the 160/116/80 mockups (desk, signal bridge, attention ledger; I did not open every combination, I opened 116 all three, 160 desk, ledger and bridge, 80 desk, ledger and bridge). Current screens read as text. RR = rendering-rules.md.

## 1. The first audit against what the images show

Right:
- Per-line `reason unknown` is the biggest repeat. In the images it also does visible damage: at 116 two-column and at 80 it wraps and leaves `unknown` or `reason unknown` alone on its own row (questions-116 B, desk-116 B, questions-80, desk-80).
- Three status fields plus the worktree sentence waste the desk (desk-160 A: 10 rows of mostly `active active none`).
- Dropping the ledger rule row, `flags` column and `+N more` row: correct.

Wrong or weak:
- It merges into pipe rows (`dispatch active | terminal active | outcome none`, `wt-1 (this session only) | ...`). In a framed screen that reads as a log line, no alignment, no colour hook. Rejected, see 2.
- `reasons: unknown for all` in the title is fine as wording but wrong as a rule: the day a reason exists, the title lies. Show the reason on a row only when it is known; the title carries `reasons: none in source` as the unknown-is-not-none statement.
- It kept the raw question line shape, so the hash wrap stays the main ugliness (the 64 hex line is wider than the pane at 116 and 80 and is wrapped or cut with an ellipsis in desk-116 B).
- Its 80-column mock keeps a 2-row disclosure above the questions.

Missed (only visible in the images):
1. The same question text is on screen twice on the desk: bold amber in the desk pane and again as the selected `▸` list row, both with the full hash (desk-160 A and B, desk-116, desk-80). Worst repeat in the product.
2. The big count `3` is drawn, and the line next to it says `seen, not resolved: 3 | closed by evidence...` again (questions-160 B, questions-116 B). Tile title `SEEN IS NOT RESOLVED` is a third echo of the same words.
3. `one Run only: run_14cfcbd8edf2` appears in the stacked box and again in RETAIN CONTEXT (questions-160 B); live screens also carry the Run in the header and the freshness line. Four times.
4. `question read OK 0s` vs header `coordinator questions OK 0s`: one fact, two places.
5. The caveat and its pair are split: `no read marker...` is at the top of the stacked box, `retention reset...` at the bottom. They are one thought.
6. Hierarchy: in stacked A the question is the 5th line of the box; four caveat lines sit above the thing the human came for. Questions should come first, caveats under them.
7. Two-column questions (questions-160 B): the left amber box ends 6 rows above the right column; the empty block under it looks unfinished. The RETAIN CONTEXT box is prose wrapped to 5-6 narrow lines.
8. `msg_000000000000` is the first, bold amber line of the desk. An internal id has the highest visual weight in the screen.
9. Desk label column is raw field names (`resource.worktreeId:`, `nextAction.kind:`), 21 cells of label for 4 cells of value, and the label eats the box width at 116.
10. The mockups themselves repeat: every session in the affected pane gets a second row `not observed / not admitted | fresh | not frozen`, identical for each; the desk shows `Affected: S001...` and then lists the same sessions below. Do not copy that.
11. Ledger: the `alive` column says `alive` 40 times in the current 116 ledger (and `alive (terminal)` in the questions fixture).

## 2. First-audit cuts I would reject, and what to do instead

- Pipe-joined status rows. Instead: aligned label column (about 9 cells), value column, only rows that carry information. Status: one badge `ACTIVE` (green) when dispatchStatus=active, terminalState=active, outcome=none; otherwise three separate rows (`dispatch`, `terminal`, `outcome`), amber, raw values, absent = `unknown`. Keeps RR L71 (separate facts, raw values) and AC unknown-not-none; the common case costs 1 row.
- `closed by evidence: unavailable` losing the word: keep `unavailable`; only drop `(no source)` (the word already says it).
- Dropping the disclosure to a shortened form at 80 (RR L49 verbatim): keep it verbatim; move it below the list (hierarchy), and let it wrap. It is a safety message.
- Hash collapse at 4+4 hex (`0123..cdef`): too short to compare. Use first 8 + `..` + last 4 (`01234567..cdef`), full text in the inspector and export. Needs owner decision (see 5).
- Merging the two state lines `question read` and header cell: fine, but do it by deleting the header cell, not the panel state line (RR L45 first state line must stay in the panel).
- Shortening liveness to the verdict word: fine; I go further with a dot (below).

## 3. Final list per screen (R = needs an RR edit with line; S = safety message, stays in fewer words)

Questions screen
- KEEP: title row; count figure `3`; question age (amber) + text; `▸` marker (RR L50); the freshness fact once (`question read OK 0s`, RR L45); `shown 6/6`.
- KEEP (S): `seen, not resolved`, `closed by evidence: unavailable`, disclosure verbatim (RR L49), `no read marker...: answered questions stay listed` (RR L48), `retention reset at 12:00; ...` (RR L53), `worker-reported, not questions` (RR L39), `PARTIAL`/`collected n / reported T` (RR L20).
- SHORTEN: header to `ORCA OBSERVER  live  scope=all  12:00:00` (drop `mode=`, `as of`; R L17). Footer to `j/k move  Enter detail  / filter  n/p question  h history  e export  q quit` (free). Settled/frozen/cost/source counts into one dim token `no source: settled, frozen, cost, source counts` (R L20, L81, L82; S: still says no source). Counts line `(no source)` dropped (R L47).
- MERGE: the count line into the tile (figure + `seen, not resolved` + `closed by evidence: unavailable` in one box; drops the separate counts row; R L47). Caveat + retention into one RETAIN CONTEXT box, two rows (R L48, L53). Run id once, in the tile (R L44, L54: header cell loses it). Question-read state once (R L45, L54: header cell becomes `questions OK 0s`).
- ON-DEMAND (inspector): `runs seen: 2`, source counts when unknown, `msg_` ids, full hash, full paths (R L26).
- DROP: per-row `reason unknown` (R L50) once the title says `reasons: none in source`; the tile title echo is replaced by a quiet title; duplicate `scope=all` second copy (R L20).

Decision Desk
- KEEP: question text, once, in the desk pane; age on the pane title (`DECISION DESK   1h`); `session`, `state`, `alive`, `next`, `worktree`.
- KEEP (S): worktree wording `wt-1 (this session only)` (AC-7; full sentence in inspector; R L57 note); `ACTIVE` badge or the three raw rows.
- SHORTEN: labels (`state`, `next`, `alive`) replacing raw field names; `alive: yes (terminal), 3s ago` (one value from verdict, source and evidence age).
- MERGE: dispatchStatus/terminalState/outcome into the badge as above (R L57, L71).
- ON-DEMAND: `msg_000000000000`, raw field names (R L57).
- DROP: the selected list row repeating the pane text: list rows are one line, truncated with `>`; the pane holds the full wrap (R L50, L57). The second copy of retention/worker-reported lines under the desk (free).

Worker ledger
- KEEP: id, run, state, next (verbatim, R L31), age; gap notice verbatim (R L32, S); `26 historical hidden (h)` (R L23).
- SHORTEN: liveness to a coloured dot `●` with one legend `● alive (live terminal)`; any non-alive value is spelled out in amber (R L30; NO_COLOR prints the word).
- MERGE: dispatch/terminal/outcome into one `status` cell with the same ACTIVE badge rule (R L30); gap notice and `historical hidden` on one row (R L23).
- DROP: `flags` column (show `*` in the first cell, R L65), rule row, `+N more` row above a footer that already says `shown 40/54` (R L76), the repeated `scope=all` and the collected count in the footer (R L22).

## 4. Text mocks at 116 columns (fixture wording; frames and colours as in the images)

Questions (stacked: count strip, list, RETAIN CONTEXT). The hash line shows the collapse variant; without owner approval the line is cut with `>` before `hash` and the full text is in the desk.
```
ORCA OBSERVER  live  scope=all  12:00:00          worker-list OK 0s | questions OK 0s | collected 6 / reported 6
no source: settled, frozen, cost, source counts
┏━ SEEN IS NOT RESOLVED ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ ███   seen, not resolved                                                                                         ┃
┃   █   closed by evidence: unavailable                                                                            ┃
┃ ███   one Run only: run_14cfcbd8edf2                                                                             ┃
┃   █   question read OK 0s                                                                                        ┃
┃ ███                                                                                                              ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
┏━ COORDINATOR QUESTIONS   reasons: none in source ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ ▸  1h  Approve plan: edit src/superclaude/cli/observe/render.py and tests/observe/test_render.py, hash 01234567..cdef ┃
┃   59m  Confirm deployment window                                                                                 ┃
┃   59m  Name the release reviewer                                                                                 ┃
┃ bounded best effort; coverage unknown; at most 100 rows per read, not 100 questions; bursts over 100 rows between ┃
┃ reads may be lost                                                                                                ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
┌─ RETAIN CONTEXT ─────────────────────────────────────────────────────────────────────────────────────────────────┐
│ answered questions stay listed (no read marker in source)                                                        │
│ retention reset at 12:00; questions observed before this start are not retained                                  │
└──────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
worker-reported, not questions  (6 worker rows, see ledger)
j/k move  Enter detail  / filter  n/p question  h history  e export  q quit                            shown 6/6
```
Today this is 25 lines of unframed text; the mock is 24 including 4 frames, no repeated word except the unavoidable disclosure.

Decision Desk (two columns: question pane over list on the left, linked session on the right). Same header as above, then:
```
┏━ DECISION DESK   1h ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓ ┌─ LINKED SESSION ────────────────────────────────┐
┃ Approve plan: edit src/superclaude/cli/observe/render.py and ┃ │ session   w-001                                 │
┃ tests/observe/test_render.py, hash                           ┃ │ state     running                               │
┃ 01234567..cdef   (Enter shows all 64)                        ┃ │ alive     yes (terminal), 3s ago                │
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛ │ next      wait                                  │
┌─ COORDINATOR QUESTIONS  reasons: none in source ─────────────┐ │ status    ACTIVE                                │
│ ▸  1h  Approve plan: edit src/superclaude/cli/obs>           │ │ worktree  wt-1  (this session only)             │
│   59m  Confirm deployment window                             │ └─────────────────────────────────────────────────┘
│   59m  Name the release reviewer                             │
│ one Run only: run_14cfcbd8edf2   read OK 0s                  │
│ bounded best effort; coverage unknown; at most 100           │
│ rows per read, not 100 questions; bursts over 100 rows       │
│ between reads may be lost                                    │
└──────────────────────────────────────────────────────────────┘
answered stay listed (no read marker); retention reset at 12:00, earlier questions not retained
```
Note the empty block under the right pane: use it for `worker-reported, not questions` plus the worker rows for the linked session only, or shrink the right pane. Desk today at 116: 38 text lines; this is about 16 rows above the ledger.

Worker ledger (live fixture with the question source unread):
```
ORCA OBSERVER  live  scope=all  12:00:00          worker-list OK 0s | messages UNVERIFIED | collected 80 / reported 80
source counts: active 54 / reclaimable 0 / retained 13 / released 13   no source: settled, frozen, cost
Human questions: source UNVERIFIED, 0 rows interpreted, not "no questions"          26 historical hidden (h)
worker-reported, not questions     ● alive (live terminal)
   id     run    state     status   next    age
   w-001  run-0  running   ACTIVE   wait    3s   ●
   w-002  run-1  idle      ACTIVE   wait    6s   ●
   w-003  run-0  running   ACTIVE   none    9s   ●
   ...   (34 more rows)
j/k move  Enter detail  / filter  h history  m mark  e export  q quit                            shown 40/54
```
(Row values are from the questions fixture workers; the ledger fixture's own state values are not shown in its 116 text, so only `id`, `next`, `age` are verbatim there.)

## 5. Ranked top 10 changes

1. Desk: show the question once (pane full text, list rows one line cut with `>`). Biggest repeat; risk none.
2. Merge the count: figure + words + `closed by evidence: unavailable` in one tile; delete the separate counts line and the tile-title echo. Risk none (R L47).
3. Per-row `reason unknown` replaced by `reasons: none in source` in the title; rows show a reason only when known. Fixes the orphaned `unknown` wraps. R L50; unknown stays visible.
4. Status badge `ACTIVE` (or three raw rows when any value is not default) in desk and ledger. R L57, L71, L30.
5. Hash display `01234567..cdef`, full in inspector/export. Touches D-6, RB-19 and the two hash canaries. Owner decision.
6. Run id once, question-read state once; remove the duplicates in header and RETAIN CONTEXT. R L44, L45, L54.
7. Questions first, caveats under them; merge caveat + retention into RETAIN CONTEXT. R L48, L53 order only.
8. Ledger: dot for alive, one `status` cell, drop `flags`, rule row, `+N more`. R L30, L65, L76.
9. Header/footer trim (`mode=`, `as of`, duplicate `scope=all`, collected in footer, key list). R L17, L22.
10. Desk labels in plain words; `msg_` id and raw field names on demand. R L57.

## 6. Owner decisions needed

1. Hash: show `first8..last4` on screen with the full text in the inspector/export (reverses D-6 and RB-19 and rewrites the hash canaries)? Recommended: yes.
2. Per-question `reason unknown` replaced by one title note and shown per row only when a reason exists? Recommended: yes.
3. Is the `ACTIVE` badge (three raw values hidden while all three are default) acceptable, given the three-separate-facts rule? Recommended: yes, any non-default value expands to its own row.
4. Is the liveness dot acceptable (word spelled out for anything not alive, and under NO_COLOR)? Recommended: yes.
5. Should `source counts`, `runs seen` and `msg_` ids leave the main screen for the inspector? Recommended: yes.

Not checked: 160 and 80 text mocks for this audit (116 only), no code or tests run, mocks drawn by script for width and not rendered as PNG. Risk: items 3 and 5 contradict verbatim RR wording and an owner-decided hash rule, so they stay proposals until approved.
