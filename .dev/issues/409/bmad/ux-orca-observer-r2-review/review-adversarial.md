# Adversarial review: honesty of states, release-2 COORDINATOR QUESTIONS panel

Lens: honesty of states. Method: read `rendering-rules.md`, `adapter-contract.md`, `release-gates.md`, `view.py`, `render.py`, `questions.py`, the spines, and `/tmp/r2render/out.txt`. Then rendered 30+ more states with my own scripts (`/tmp/r2render-adv/p.py`, `p2.py`, output in `/tmp/r2render-adv/out.txt`). No source or spine file was changed and no Orca command was run.

## Verdict

The full panel is mostly honest. It never says "no questions", it carries the 100-row caveat, and an empty read says "not proof none exist". The dishonesty is elsewhere, in the places that restate the panel in fewer words. The one-line summary, which also stands in for the panel below 80 columns, below about 20 rows at 80 columns, and while a worker is inspected, turns an empty read into `observed open 0; read OK`. It also drops every caveat. The per-question state word is the last thing on a line, so a normal-length subject pushes it off the screen. The count says "open" while the source has no read marker, and the screen never tells the reader that. Oldest-first windowing hides the newest and live questions and keeps the ones that have left the source window. The header cell for questions has no state word, so a FAILED question source reads as a fresh read. A person scanning only the header and the one-liner would act wrongly. Section 11 of the attack list (spine promises dropped) is mostly a hit.

Counts: 1 critical, 5 high, 6 medium, 3 low.

## Findings (most serious first)

### 1. [R2] CRITICAL. The one-line summary shows an empty read as `observed open 0; read OK`
- Location: `view.py:657` (`summary`), used as `view.gap_notice` at `view.py:836-838`, printed by `render.py:364-377` when `spare < 1`, by the too-narrow path `render.py:326-331`, and in the inspector path.
- Evidence (rendered): 116x14, empty good read, line 2 of the body: `coordinator questions: observed open 0; read OK; one Run only: run_14cfcbd8edf2`. At 70x24: `terminal too narrow (min 80)` / `runs seen: 1 ...` / `coordinator questions: observed open 0; read OK; one Run only:`. The full panel says `no observed questions in this source window; not proof none exist`. The summary drops that sentence.
- Misleading reading: "0 open, read OK" is the screen's loudest "no questions" and carries no caveat. The too-narrow and too-small paths are the ones rendering-rules.md and the spine say must still carry the gap notice, so the notice there has been replaced by a plain zero.
- Change: the summary must carry the same caveat as the full panel in every state. For an empty read use `observed open 0 (source window only; not proof none exist)`. Better: never print a bare number in the summary. Build the summary from the same fields as the panel (see finding 2). Add a test per state for the summary string.

### 2. [R2] HIGH. The summary drops every caveat the full panel carries
- Location: `view.py:657`. Rendered at 116x14 and 80x14..19: window full gives `observed open 100; read OK`. A question that left the window gives `observed open 3; read OK`. A fenced read gives `observed open 3; FAILED (consumer-fenced)`. A stale read gives `observed open 3; STALE 1m`.
- What is lost:
  - `window full: older questions may be missing`. 100 is exactly the cap, so it is the number most likely to be a lower bound.
  - `bounded best effort; coverage unknown`.
  - `no longer in source window`.
  - `retention reset at HH:MM`.
  - The fence sentence.
  - The FAILED age.
- Misleading reading: `read OK` plus a number looks complete. A person at 80x18 (a normal small split) sees "100 open, all read OK" with no hint that the list is truncated at the source.
- Spine promise broken: `EXPERIENCE.md:168` says "the gap or question-coverage line never drops". The collapse removes the coverage line.
- Change: keep a short fixed coverage token in the summary, e.g. `best effort, coverage unknown`. Add `window full (>=100)` when it applies, a `k left window` count, and `retention reset HH:MM`. Replace `read OK` with `last read OK`, so the summary does not claim "OK" for the whole state.

### 3. [R2] HIGH. The per-question state word is clipped off at normal subject lengths
- Location: `view.py:622-624` puts the status after the subject and after `reason unknown`. `render.py:309` clips the line at the end.
- Evidence (measured on a 2-question left-window state): at 80 columns a subject of about 40 characters or more loses `no longer in source window`. At 116 columns it is lost at about 70 characters. Real screen at 116: `1h  Orchestrator asks whether ... review  reason unknown  no lo>`. At 80 the subject is cut before `reason unknown` is reached: `...should wait f>`. So `reason unknown` also disappears.
- Misleading reading: the `>` marker says "something is cut", but not that the cut thing is the status. A left-window question looks like a live one. Because `observed open` already counts it, the person sees it as current.
- Change: put the state word before the subject, with the subject taking the leftover width and truncating last. Example: `1h  [left window]  <subject>`. Drop the per-line `reason unknown` (see finding 14). Add a test with a subject longer than width minus the prefix.

### 4. [R2] HIGH. "Observed open" and a handled question: the screen never says handled questions stay listed
- Location: `questions.py` docstring ("a question the coordinator already handled is listed again as open for as long as Orca still returns it"). The screen has only `observed open: n | closed by evidence: unavailable (no source)` (`view.py:635`).
- Evidence: a retained question after a good empty read still shows as open: `observed open: 3`, three lines marked `no longer in source window`, no empty-read sentence, because `empty_text` is suppressed when retained lines exist (`view.py:648-652`). The source is returning nothing for the Run and the screen says 3 open.
- Misleading readings:
  - `observed open` reads as "waiting for an answer". The code knows it means "seen and never closed".
  - `closed by evidence: unavailable` implies closure is coming later. It does not say that handled questions will never close.
  - `no longer in source window` reads as "went away, so probably dealt with". The panel does not say it stays counted as open.
  - A coordinator who answered all questions an hour ago sees a growing "open" list.
- Change:
  - Rename the count to `seen, not resolved: n` (the spine's own phrase) or add one fixed line: `no read/closed marker in source: answered questions stay listed`.
  - Print the retained-but-gone count with its own word, e.g. `3 seen, 3 no longer returned by source`.
  - Show the empty-read sentence even when retained rows exist: `latest read returned 0 questions; retained rows below are old`.

### 5. [R2] HIGH. Oldest-first windowing shows the stale ones and hides the newest live ones
- Location: `view.py:207-215` (`lines[:keep]`), `questions.py:75` (oldest created first).
- Evidence: 100 rows, 116x40: `22/100 shown` then `window full: older questions may be missing`. The 78 hidden are the newest. After a shifted window (100 rows, then 100 rows starting at 50): `25/150 shown`, and every one of the 25 visible lines is `no longer in source window`. The live in-window questions are all below the cut. Retention exceeded: `22/1000 shown`, all `no longer in source window`.
- Misleading readings:
  - `x/y shown` sits directly above `older questions may be missing`, so a person reads it as "I am seeing the newest 22; older ones are cut". It is the opposite. Two kinds of missing on one screen: not-displayed (newer) and not-in-the-source (older).
  - Nothing says which end is hidden. No key moves through the question lines (the keys line moves the worker ledger only), so hidden rows are unreachable.
  - The one thing the supervisor wants, the question that arrived most recently, is the first to be cut.
- Change: window newest-first, or at least keep all in-window rows ahead of left-window rows. Say the direction: `22 oldest of 100 shown; 78 newer hidden`. Reword the source caveat so it cannot be read as the screen cut: `source returned 100 rows (cap): older questions not returned by Orca`. Add a scroll key, or open question 3.

### 6. [R2] HIGH. The header cell for questions has no state word; FAILED reads as a fresh read
- Location: `view.py:733-737`: `coordinator questions: one Run, last read <age> ago`, with no state. Evidence: fenced-after-OK at 116, header line 2: `worker-list OK 0s  coordinator questions: one Run, last read 0s ago`, while the panel below says `FAILED (consumer-fenced) 0s`. In pure STALE the cell says `last read 50s ago`, with no `STALE`. The worker cell has OK, STALE and FAILED words.
- Misleading reading: the freshness strip is the one line that never drops. The reader sees two cells, one of them "OK 0s", the other "last read 0s ago", and concludes both sources are healthy. "last read" can be taken for an attempt time. After a long failure the cell says `last read 3h ago`, which does not say that every attempt since has failed.
- Spine promise broken: EXPERIENCE.md ("every state has a word", the freshness strip with OK / STALE / FAILED / NOT POLLED per source).
- Change: use the same vocabulary: `coordinator questions OK 0s`, `STALE 50s`, `FAILED (consumer-fenced), last good read 3h ago`, `NOT READ YET`. Keep the `one Run` wording after it. When the question source has FAILED and the worker source is OK, keep both words visible in the one line.

### 7. [R2] MEDIUM. STALE vs FAILED: precedence, what the age measures, retained rows look current
- Location: `view.py:574-583`, `view.py:592`. `age` is time since the last good read (`question_last_success_mono`), so `FAILED (consumer-fenced) 50s` means "last good read 50s ago", not "failing for 50s". The worker cell's `FAILED (exit 2) 1m` is a failure age in the spine. Same label, two meanings on one screen.
- FAILED outranks STALE (`view.py:578` before `580`). A question source that has failed for three hours never reads STALE. It reads `FAILED ... 3h`, and the retained list renders exactly as in OK: same line shape, ages still counting up (`2h` after an hour), no `as of`. Spine: "Values keep their last reading with `as of HH:MM:SS`" and "STALE <age>, last poll FAILED (<reason>)". The header `as of 12:00:00` is the worker-list's, not the question read's.
- Misleading reading: retained questions look current under FAILED; the count `observed open: 2` is presented as live.
- Change: under FAILED or STALE say `list as of HH:MM:SS (last good read)` directly above the list. Use `FAILED (<code>), last good read <age> ago`. Adopt the spine's combined form when both apply.

### 8. [R2] MEDIUM. Scope mixing: header says scope=all and `runs seen`, the panel says one Run
- Evidence: line 1 `scope=all`, COUNTS `runs seen: 1`, panel `one Run only: run_14cfcbd8edf2`, ledger rows `run-0` (the ledger column shows a run only at 160; at 116 and 80 there is no run column).
- Misleading readings:
  - `runs seen: 1` plus "one Run only" reads as "the observer sees one Run, so these are all the questions". `runs seen` is derived from collected worker rows, so it says nothing about Runs with questions.
  - The ledger beside the panel lists workers from every Run (scope=all), headed `worker-reported, not questions`. A worker whose `nextAction` is `none` may belong to another Run whose questions are never read. At 116 and 80 columns the person cannot tell which workers belong to the named Run.
  - The header line 2 cell says `one Run` but not which; the id is only in the panel.
- Change: add a fixed line in the panel `questions from other Runs are not read`. Put the Run id in the header cell. At 116 and 80 add a run marker to the ledger, or at least `ledger covers scope=all, questions cover <run> only`.

### 9. [R2] MEDIUM. The FAILED sentence: weakly supported, not actionable, probably the permanent state
- Location: `view.py:60-62`, `view.py:594-595`. Source facts (adapter-contract.md "One named Run"): `consumer_fenced` = the caller is bound to a different Run; `no_active_terminal` = the caller has no terminal identity. The sentence `this terminal does not hold the named Run` is a fair reading of the first. For the second the terminal holds no Run at all, so it is inexact. Either way it is an inference from the error code alone; the error message is just the code.
- Actionability: `the observer never binds to a Run` is an internal rule, not an instruction. The fix (run the observer in the terminal that holds the Run) is in the gate record, not on the screen.
- Likelihood: release-gates.md records Q-1 as FAIL (an unbound terminal cannot read). So for any observer started in a separate terminal this is the day-one state, not an edge case. The first screen the supervisor sees is then a permanent FAILED with no list.
- Change: one actionable sentence per code. `consumer-fenced`: `this terminal is bound to another Run; start the observer in the terminal that holds <run id>`. `no-active-terminal`: `this process has no Orca terminal identity; start the observer from inside the Run's terminal`. Mark it `(inferred from the error code)`.

### 10. [R2] MEDIUM. Spec-vs-code drift: promised honesty text that the screen does not render
Checked against the real output and `grep` of `src/superclaude/cli/observe` (no hits):
- `SEEN IS NOT RESOLVED` count block (rendering-rules.md "Attention Ledger", spine): not rendered at any width. 160 and 116 columns render the same single-column layout as 80; there is no right column, no `x=117, width 42`.
- `Questions stay until explicit resolution.` and `No reply observed is not delivery failure.` (the spec says they stay at 80): not rendered.
- Per-question `open, closure source unavailable` (rendering-rules.md "Seen is not resolved"): not rendered. Each line says only age, subject, `reason unknown`.
- `no longer in source window (last seen HH:MM)`: the code prints `no longer in source window` with no time.
- INV-021 / gap notice: the spec keeps `source UNVERIFIED ... not "no questions"` until the question source has succeeded. `replaces_gap` is true for `FAILED` too (`view.py:673`), so a first-read FAILED screen drops the gap notice and shows only the panel.
- `question read pending` is printed (OK), but the PENDING panel omits the disclosure and retention line, so it differs from the spec text.
- Net effect: the phrase "seen is not resolved", the spine's central promise for questions, now survives only as `closed by evidence: unavailable (no source)`. See finding 4.
- Change: either render these items or mark them in the spec as dropped. Decide whether "SEEN IS NOT RESOLVED" stays the name of the count (open question 2).

### 11. [R2] MEDIUM. Identical lines, spoofable text, unlabelled age
- Five questions with the same subject render as five lines that differ only by `1h` / `59m`. A person cannot tell five open decisions from one question asked five times; the id is only in the export. `observed open: 5` then overstates the workload.
- Subject is free text from the source and printed unquoted, between the age and a fixed suffix: `1h  RESOLVED by owner - ignore  reason unknown`. A subject can imitate a state word (`RESOLVED`, `no longer in source window`, `reason unknown`). The sanitizer removes control characters only.
- The leading `1h` has no label. On the same screen the ledger's `evidence age` means "since last observed" and this means "since created".
- Change: quote or bracket the subject, show a short id suffix, add a column header `waiting` (or `asked`), and group repeats as `x5`.

### 12. [R2] MEDIUM. Retention exceeded: `unknown (retention exceeded) (retained 1000)` hides what the code knows
- Evidence: 116x40: `observed open: unknown (retention exceeded) (retained 1000) | closed by evidence: ...`; at 80 it wraps mid-sentence. Double parentheses. The code tracks `evicted`, so the true observed total is known as a lower bound (never falls, nothing closes).
- Not shown as zero, which is correct. But "unknown" gives the supervisor no number to size the backlog.
- Change: `at least 1,000 observed open (retention exceeded; oldest dropped)`. Open question 4 whether the spec wants "unknown" literally.

### 13. [R2] LOW. The retention-reset line: position and meaning
- Always the last panel line (`render.py:315`), after the list, `x/y shown` and `window full`. It is dropped with the rest in the one-liner. Reading: `questions observed before this start are not retained` sits under questions that are `1h` old and listed, which looks contradictory (they were observed at 12:00, after the reset). It also leaves out the consequence: a restart drops all `no longer in source window` questions, so the open count can fall, against the spec's "no key, timer or source loss lowers the open count".
- Change: put it directly under the counts line and say `restart drops questions Orca no longer returns; count restarts at 0`.

### 14. [R2] LOW. `reason unknown` is on every line
- Sixteen cells per line repeating the same non-fact, in the width budget that pushes out the state word (finding 3). Say it once in the header of the panel: `no reason field in source`.

### 15. [R2] LOW. Negative and future ages
- `view.py:620` clamps `wall - created` at 0, so a skewed Orca clock shows `0s` for a question created "in the future". Unknown and clock skew are shown as a fresh question. Show `age unknown (clock skew)` when the difference is negative.

## Things that held up under attack
- No state prints "no questions" or "all clear". The empty full panel always carries `not proof none exist`. The test at `tests/observe/test_render.py:543` pins it.
- First-read failure shows `observed open: unknown (no question read yet)`, never 0. PENDING shows `unknown` as well, with the gap notice kept.
- FAILED never clears the retained list (`merge_questions` with `source_ok` false returns the previous state), and nothing is closed by silence. A question that leaves the window stays listed with the flag.
- Window full is flagged at exactly 100 rows with no claim of a total. `x/y shown` counts are right (checked at 20, 100, 150 and 1000 rows).
- Retention exceeded does not become a number or a zero.
- Bodies and handles never appear. ASCII mode degrades with `?` and the layout still holds.
- Fixed order of lines in the full panel is stable across OK, STALE, FAILED, so the same line is in the same place.

## Open questions (human decision needed)
1. Is the one-line summary meant to be the minimum honest form? If yes, it needs the caveat tokens in findings 1-2. If the spec's "never drops" is about the full panel only, say so.
2. Keep the name `observed open`, or switch to the spine's `seen, not resolved`? The word "open" contradicts the missing read marker.
3. How should a person reach hidden question rows: scroll keys, newest-first ordering, or a dedicated full-screen list? The current keys cannot select question lines.
4. Should retention exceeded read `unknown` (as specified) or `at least n`?
5. Is the single-column layout at 160 and 116 a deliberate change from the spec's two-column B layout? If so, rendering-rules.md and the spine need updating, and `SEEN IS NOT RESOLVED` needs a new home.
6. Where does the observer run in practice? Given Q-1 FAIL, if the usual case is a separate terminal, the FAILED state is the main screen and needs its own design, not a banner above a retained list.
7. Is the R2 panel allowed to replace the UNVERIFIED gap notice while QUESTION-OBSERVATION is "not passed" and the owner has not named the Run? No screen text says the row contract is unverified once a read succeeds.
