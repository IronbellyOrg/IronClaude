# Validation Report — Orca Observer (R2 coordinator questions)

- **DESIGN.md:** `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/issues/409/bmad/ux-orca-observer-r2-review/DESIGN.md`
- **EXPERIENCE.md:** `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/issues/409/bmad/ux-orca-observer-r2-review/EXPERIENCE.md`
- **Run at:** 2026-11-12
- **Mode:** headless Validate; lenses run: rubric walker, accessibility (terminal UI), adversarial (honesty of states)
- **Spines reviewed are the 2026-11-08 copies; the review target is the release-2 coordinator-questions panel (rendering-rules.md, view.py, render.py, tests/observe/test_render.py R2 section).**
- **Renders:** produced with the test fixtures' fake runner and fake clock (synthetic, not Orca data); no Orca command was run.

## R2 panel findings

42 of 46 findings concern the new panel or how it fits the screen, most serious first. Locations are code or spine lines in this checkout, or the exact screen text with the width and height where it was seen. Full notes are in "Findings by severity" below under the same IDs.

1. **F01 (critical)** The one-line summary shows an empty read as "observed open 0; read OK" and drops every caveat
   - Where: view.py:657 (summary, used as gap_notice); render.py:364-377 (collapse when spare < 1), :326-335 (too narrow / too small); seen at 116x14, 160x14, 80x14-19, 70x24
   - Change: Build the summary from the same fields as the panel and never print a bare number: empty read -> "observed open 0 (source window only; not proof none exist)"; window full -> "observed open 100+ (window full)"; always keep "best effort, coverage unknown"; add "k left window" and "retention reset HH:MM" when they apply; say "last read OK" not "read OK". Add one test per state for the summary string.
2. **F02 (critical)** UJ-5 still describes the retired question design
   - Where: EXPERIENCE.md:479-490 (UJ-5); new design: rendering-rules.md:40, :43, :63; PRD FR-17
   - Change: Rewrite UJ-5 as the R2 flow (start, read the panel, find the oldest line, know the count is a bounded observation). Move select / inspect / affected-session steps to an R3 flow under QUESTION-LINK.
3. **F03 (critical)** Screen inventory, B geometry and B shrink order describe components R2 does not build
   - Where: EXPERIENCE.md:69-70 (screens 5-6), :74, :165-168, :172-177 (right = width - 43); rendering-rules.md:41; real renders at 160/116/80
   - Change: Replace these rows with the stacked panel and its width / height behaviour; mark two-column B, RETAIN CONTEXT and the question inspector "design reference, not R2" (or move them to R3).
4. **F04 (high)** The per-question state word is clipped off at normal subject lengths
   - Where: view.py:622-624 (suffix after subject); render.py:309 (clip at line end); seen 116x30 and 80x30
   - Change: Put the state first and clip only the subject: "1h  [left window]  <subject>". Reserve the status cells. Add a test with a subject longer than width minus the prefix.
5. **F05 (high)** Handled questions stay "observed open" and the screen never says the source has no read marker
   - Where: questions.py:9-12 (docstring states the limit); view.py:635 (counts line); view.py:648-652 (empty_text suppressed when retained lines exist)
   - Change: Add one fixed line, "no read/closed marker in source: answered questions stay listed". Show "3 seen, 3 no longer returned by source". Show the empty-read sentence even when retained rows exist: "latest read returned 0 questions; rows below are old". Open question: rename the count to "seen, not resolved: n".
6. **F06 (high)** Oldest-first windowing hides the newest questions, and no key reaches them
   - Where: view.py:207-215 (lines[:keep]); render.py:309-311; seen "7/20 shown", "22/100 shown"
   - Change: Open question: newest-first when cut, or keep in-window rows ahead of left-window rows, or a scroll key. At minimum print "7 oldest of 20 shown; 13 newer not shown (e exports all)", reword the source caveat as "Orca returned 100 rows (cap): older questions not returned", and change the key line to "j/k move workers".
7. **F07 (high)** The freshness-strip cell for questions has no state word, so a FAILED or STALE source reads as a fresh read
   - Where: view.py:733-737; seen in "fenced after ok" (header "last read 0s ago" above "FAILED (consumer-fenced) 0s") and "pure STALE" (header "last read 50s ago", no STALE)
   - Change: Use the same grammar: "coordinator questions OK 0s" / "STALE 50s" / "FAILED (consumer-fenced), last good read 3h ago" / "NOT READ YET"; put the Run id in the cell.
8. **F08 (high)** At 80 columns the key line is cut before "e export" and "q quit"
   - Where: view.py:75 (KEYS_LINE); render.py:416 (clip of help_line); seen at 80x30 and 80x24: "... m mark  e exp>"
   - Change: Wrap the key line like the footer counts, drop "Esc back" and "h historical" at 80, or print "e export  q quit" on a second line.
9. **F09 (high)** No Key Flow for a coordinator question arriving
   - Where: EXPERIENCE.md:355 and rendering-rules.md:49 (change marks cover worker rows only)
   - Change: Add a flow "A coordinator question arrives" with a climax beat and the failure path "the list is longer than the screen". Open question: does the owner want a new-question cue (k new since HH:MM)?
10. **F10 (high)** No flow for the question source failing, being fenced, going stale or restarting
   - Where: view.py:60-62, :585-599; adapter-contract.md:61; release-gates.md Q-1
   - Change: Add failure paths ending in the exact on-screen words and the one action the supervisor can take outside the observer. Open question: design FAILED as the main screen for that case.
11. **F11 (high)** No component row in either spine for the Coordinator questions panel or its parts
   - Where: DESIGN.md Components; EXPERIENCE.md Component Patterns
   - Change: Add one DESIGN.md row (anatomy, roles) and one EXPERIENCE.md pattern (what replaces the gap notice and when, what the summary is, what is never cut, lines are listed not selectable).
12. **F12 (high)** State vocabulary and view-level tables contain no question-panel rows
   - Where: EXPERIENCE.md:276-283, :287-300
   - Change: Add the exact strings from view.py:52-69 and, per state, what happens to retained questions and to the open count (never lowered).
13. **F13 (high)** Retired vocabulary is still in the spines
   - Where: "OPEN HUMAN QUESTIONS": EXPERIENCE.md:176, :482, DESIGN.md:178; "marked looked": EXPERIENCE.md:484; "SEEN IS NOT RESOLVED" and "RETAIN CONTEXT" as panels: EXPERIENCE.md:69-70, :168, :177; rotation phrase "read k of N Runs since start": :216, :550; "one key away" / UX-OQ-3: :41, :69, :336, :529; auto-switch anti-pattern :423 and view rule :58
   - Change: Replace or mark each as superseded; close UX-OQ-3; re-scope OQ-13; reword the one-screen rules.
14. **F14 (high)** m is still described as moving a question to "marked looked"; the key table and footer do not say m marks worker rows only
   - Where: EXPERIENCE.md:484, :320; view.py:75 ("m mark"); rendering-rules.md:40, :63
   - Change: Key table: "mark a look for worker rows; questions are not marked". Open question: footer wording "m mark rows".
15. **F15 (medium)** FAILED outranks STALE, and the age means "since last good read" with a different meaning than the worker cell
   - Where: view.py:574-583, :592
   - Change: Under FAILED or STALE print "list as of HH:MM:SS (last good read)" above the list; use "FAILED (<code>), last good read <age> ago" or the spine's combined form (EXPERIENCE.md:283).
16. **F16 (medium)** Scope mixing: header and COUNTS say scope=all and "runs seen", the panel says one Run only
   - Where: view.py:722 ("one Run only" added only for a bound worker scope); adapter-contract.md:68; renders at 160/116/80
   - Change: Open question (build or spec): add "questions: one Run only <id>" to the header; add "questions from other Runs are not read" to the panel.
17. **F17 (medium)** The FAILED sentence is inexact for no-active-terminal and gives no action
   - Where: view.py:60-62, :594-595; adapter-contract.md "One named Run"
   - Change: One sentence per code with the action, marked as inferred: consumer-fenced -> "this terminal is bound to another Run; start the observer in the terminal that holds <run id>"; no-active-terminal -> "no Orca terminal identity; start the observer from inside the Run's terminal".
18. **F18 (medium)** Spec-vs-code drift: text the spec promises is not rendered
   - Where: rendering-rules.md:41 (SEEN IS NOT RESOLVED block), :45 ("Questions stay until explicit resolution.", "No reply observed is not delivery failure."), :61 ("last seen HH:MM"), :63 (per-question "open, closure source unavailable"); view.py:67-69, :622-624
   - Change: Render each item or mark it dropped in the spec; adopt one string for the left-window flag. Open question for the spec owner.
19. **F19 (medium)** Identical lines, no id, unlabelled age, spoofable subject, ASCII "?" substitution
   - Where: view.py:622-628; terminal.py:156-158; seen 4x "59m  Should I rebase onto master or merge?  reason unknown" and "1h  h?llo ?  reason unknown"
   - Change: Add a short id suffix, a "waiting" column header, quote or bracket the subject, group repeats as x5, and in ASCII mode show \uXXXX or add "(non-ASCII shown as ?)" once. Open question: short id on each line?
20. **F20 (medium)** "retention exceeded" hides a number the code knows
   - Where: questions.py:21-24; view.py:610-614; seen at 116x40 "observed open: unknown (retention exceeded) (retained 1000)"
   - Change: Open question: "at least 1,000 observed open (retention exceeded; oldest dropped)".
21. **F21 (medium)** "observed open: 100" reads as exact; "window full" is printed far below it
   - Where: view.py:635, :669; seen 116x40: count at line 9, "window full" 24 lines later
   - Change: Open question: "observed open: 100+ (window full)", or put window-full on the counts line.
22. **F22 (medium)** Height budget: the ledger is squeezed to 2 rows and the x/y shown line is not budgeted
   - Where: render.py:371-373 (comment promises at least 3 ledger rows); seen 116x24 and 80x24 "2/4 shown  +2 more"; EXPERIENCE.md:144-163 has no panel rows
   - Change: Budget the cut line; add the panel to the shrink order. Open question: which block wins when height is short, ledger or questions?
23. **F23 (medium)** State, count and caveats are not findable at a glance
   - Where: view.py:585-599, :635; seen 160 and 80
   - Change: One first line under the title: "question read: OK | STALE 50s | FAILED (...) | pending", then the count, then the list, then the caveats as a block after the data.
24. **F24 (medium)** Three "shown" counters on one screen with no noun
   - Where: "7/20 shown" (questions), "2/4 shown  +2 more" (workers), footer "shown 2/4 | collected ..." (workers); view.py:215
   - Change: "questions shown 7 of 20", "workers shown 2 of 4".
25. **F25 (medium)** At 80 columns the COUNTS line cuts a state word: "cost un>"
   - Where: seen at every 80-column render, line 4; header text built at view.py:751-760
   - Change: Let counts wrap to a third line at 80 or shorten to "cost n/a".
26. **F26 (medium)** The disclosure is a 28-word run-on that takes 2 rows on every frame; the panel spends 5-6 rows before the first question
   - Where: view.py:54-57 (QUESTIONS_DISCLOSURE); seen at 116 and 80; jargon: "bounded best effort", "coverage unknown", "Run", "reason unknown"
   - Change: Open question: allow a plain-words version on screen ("May be incomplete. Shows what this terminal saw in its last read, up to 100 messages.") and keep the technical sentence in export / help; allow it to fold to one row.
27. **F27 (medium)** The panel replaces the gap notice after a failed first read; the spine says the gap notice stays until the source has succeeded
   - Where: view.py:673 (replaces_gap for OK and FAILED); EXPERIENCE.md:58, :233, :383
   - Change: Restate the rule: the gap notice stays until the source has been read or has failed; PENDING keeps both.
28. **F28 (medium)** The panel has no colour, weight or frame assignment, and the build is unstyled
   - Where: DESIGN.md:121-122, :146, :178; terminal.py:41-42 (PALETTE = {}); render.py:424-428
   - Change: Add a question-panel component with roles. Open question: is the unstyled build intentional for R1/R2? If so say "styles PROPOSED, not applied".
29. **F29 (medium)** UJ-1 assumes the "messages UNVERIFIED (not read)" cell and the gap notice
   - Where: EXPERIENCE.md:437, :439
   - Change: Add a "questions on" variant or state that UJ-1 is the questions-off path.
30. **F30 (medium)** Glossary split: "human questions" in the spine, "COORDINATOR QUESTIONS" on screen
   - Where: EXPERIENCE.md:41, :69, :83, :233, :383; rendering-rules.md:32, :38
   - Change: Glossary line: keep the literal; say "coordinator question" everywhere else.
31. **F31 (medium)** Question subject text carries no "worker-reported" label
   - Where: EXPERIENCE.md:376; view.py:47 (ledger title only)
   - Change: Label the subject source in the disclosure or title, or state why not.
32. **F32 (medium)** No durable wireframe of the R2 panel
   - Where: workspace has no wireframes/ or mockups/; renders exist only in /tmp/r2render/out.txt
   - Change: Copy renders (5 questions OK at 160/116/80, empty, window full, fenced, STALE, collapsed) into wireframes/ with the commit noted, mark PROPOSED where the layout is PROPOSED, link inline.
33. **F37 (low)** The retention-reset line sits last, under questions that look contradictory to it, and omits its consequence
   - Where: render.py:315; view.py:66-68
   - Change: Place it under the counts line: "restart drops questions Orca no longer returns; count restarts at 0".
34. **F38 (low)** "reason unknown" repeats on every question line
   - Where: view.py:64, :622
   - Change: Say once ("no reason field in source"). Spec asks for it per line (rendering-rules.md:43): needs the spec owner.
35. **F39 (low)** Negative age clamps to 0s, so clock skew shows a fresh question
   - Where: view.py:620
   - Change: Show "age unknown (clock skew)" when the difference is negative.
36. **F40 (low)** Ages are coarse and ragged: "1h" then "59m" reads as out of order
   - Where: view.py:316-322 (format_age)
   - Change: "1h 00m", minutes up to 119, or a clock time.
37. **F41 (low)** The ">" truncation marker is also an ordinary subject character
   - Where: terminal.py:35, :175-190
   - Change: Fix with F04 so the cut is always at a fixed place.
38. **F42 (low)** Spine accessibility floor still describes colour ratios, muted "unknown" and a selection glyph the build no longer has
   - Where: EXPERIENCE.md Accessibility Floor; DESIGN.md
   - Change: Update to built behaviour and add the R2 panel (and the "no promise for live screen readers" statement).
39. **F43 (low)** Voice and Tone has no coordinator-question strings
   - Where: EXPERIENCE.md:190-202
   - Change: Add rows: "no observed questions ...; not proof none exist" vs "no questions"; "observed open: n" vs "n unresolved"; "FAILED (consumer-fenced)" vs "disconnected".
40. **F44 (low)** The --ascii rule says "?" in ledger list cells only
   - Where: DESIGN.md:195
   - Change: Extend the rule to "list cells and panel question lines".
41. **F45 (low)** Two B shapes exist: fixture B (blocks, "NN MIN", "Affected:") and live R2 (one line per question)
   - Where: EXPERIENCE.md:492-498; rendering-rules.md:38
   - Change: Say the live panel is the R2 contract and the fixture a design reference.
42. **F46 (low)** No screen-level test pins a pure STALE panel, no-active-terminal, or the collapsed summary at 14-16 rows
   - Where: tests/observe/test_render.py:412-610
   - Change: Add one screen test per state and per collapse height.

## Overall verdict

The spine pair is a sound R1 contract (tokens complete, section order correct, required sections present) but not a usable R2 contract. Everything about questions in both spines (release row B, screens 5-6, B geometry and shrink order, SEEN IS NOT RESOLVED / RETAIN CONTEXT, the m and Enter behaviour, UJ-5, the glossary) still describes the retired two-column "OPEN HUMAN QUESTIONS" ledger with rotation, a view switch and selectable questions. The built panel (one stacked block, one named Run, listed not selectable) has no Key Flow, component row, state row or shrink rule in either spine. Run an Update on the question parts before any R2 story work.

The accessibility and adversarial lenses move the picture on the panel itself. Meaning is carried by words (empty palette, no blink), and the full panel is mostly honest: it never says "no questions", it carries the 100-row caveat, and an empty read says "not proof none exist". The dishonesty is in the places that restate the panel in fewer words: the one-line summary shown on short or narrow terminals turns an empty read into "observed open 0; read OK" and drops every caveat; the per-question state word is clipped at normal subject lengths; "observed open" never tells the reader that the source has no read marker; oldest-first windowing hides the newest questions with no key to reach them; and the freshness-strip cell for questions has no state word. Fix those before the panel is judged done.

## Category verdicts

- Flow coverage — broken
- Token completeness — adequate
- Component coverage — thin
- State coverage — thin
- Visual reference coverage — thin
- Bloat & overspecification — adequate
- Inheritance discipline — thin
- Shape fit — strong

Severity counts (consolidated, de-duplicated across lenses): critical 3, high 11, medium 21, low 11. Raw lens totals before de-duplication: rubric 38 (2/9/19/8), accessibility 16 (0/4/8/4), adversarial 15 (1/5/6/3).

## Findings by severity

### Critical (3)

**F01 [State coverage]** — [R2] The one-line summary shows an empty read as "observed open 0; read OK" and drops every caveat (view.py:657 (summary, used as gap_notice); render.py:364-377 (collapse when spare < 1), :326-335 (too narrow / too small); seen at 116x14, 160x14, 80x14-19, 70x24)
When the panel does not fit (about 16 rows or fewer at 116 columns, below 80 columns, or while a worker is inspected) it collapses to "coordinator questions: observed open N; read OK; one Run only: <id>". An empty good read becomes "observed open 0; read OK": the loudest "no questions" on any screen, with no "not proof none exist". Window full becomes "observed open 100; read OK" (a lower bound shown as exact). A fenced read loses the fence sentence and a left-window question loses its flag. The disclosure "bounded best effort; coverage unknown" and the retention-reset line vanish. EXPERIENCE.md:168 says the coverage line never drops.
Fix: Build the summary from the same fields as the panel and never print a bare number: empty read -> "observed open 0 (source window only; not proof none exist)"; window full -> "observed open 100+ (window full)"; always keep "best effort, coverage unknown"; add "k left window" and "retention reset HH:MM" when they apply; say "last read OK" not "read OK". Add one test per state for the summary string.

**F02 [Flow coverage]** — [R2] UJ-5 still describes the retired question design (EXPERIENCE.md:479-490 (UJ-5); new design: rendering-rules.md:40, :43, :63; PRD FR-17)
Step 2 opens "OPEN HUMAN QUESTIONS" with SEEN IS NOT RESOLVED, step 3 selects a question and presses Enter for an inspector with RETAIN CONTEXT, step 4 presses m to move it to "marked looked". R2 has one named Run, a stacked COORDINATOR QUESTIONS panel, questions listed but not selectable, no inspector, no "marked looked" split, and m never changes the question count.
Fix: Rewrite UJ-5 as the R2 flow (start, read the panel, find the oldest line, know the count is a bounded observation). Move select / inspect / affected-session steps to an R3 flow under QUESTION-LINK.

**F03 [Component coverage]** — [R2] Screen inventory, B geometry and B shrink order describe components R2 does not build (EXPERIENCE.md:69-70 (screens 5-6), :74, :165-168, :172-177 (right = width - 43); rendering-rules.md:41; real renders at 160/116/80)
The spine specifies a two-column B (left OPEN HUMAN QUESTIONS, right SEEN IS NOT RESOLVED and RETAIN CONTEXT) plus a question inspector. The build is one stacked block at every width; RETAIN CONTEXT is "not built in R2"; SEEN IS NOT RESOLVED is folded into the counts line; there is no question inspector. A consumer would build the wrong layout.
Fix: Replace these rows with the stacked panel and its width / height behaviour; mark two-column B, RETAIN CONTEXT and the question inspector "design reference, not R2" (or move them to R3).

### High (11)

**F04 [State coverage]** — [R2] The per-question state word is clipped off at normal subject lengths (view.py:622-624 (suffix after subject); render.py:309 (clip at line end); seen 116x30 and 80x30)
A line is "age  subject  reason unknown[  no longer in source window]", cut as one string. At 116 columns a 90-character subject reads "... reason unknown  no lo>"; at 80 columns a subject of about 40 characters or more cuts before "reason unknown", so a question that left the source window looks like a live one that is still counted open.
Fix: Put the state first and clip only the subject: "1h  [left window]  <subject>". Reserve the status cells. Add a test with a subject longer than width minus the prefix.

**F05 [State coverage]** — [R2] Handled questions stay "observed open" and the screen never says the source has no read marker (questions.py:9-12 (docstring states the limit); view.py:635 (counts line); view.py:648-652 (empty_text suppressed when retained lines exist))
The source has no read or acknowledged marker, so an answered question is listed again for as long as Orca returns it, and "observed open" calls everything open. "closed by evidence: unavailable" implies closure will come later. After a good empty read with retained rows the screen shows "observed open: 3" and three "no longer in source window" lines, with no sentence that the latest read returned nothing.
Fix: Add one fixed line, "no read/closed marker in source: answered questions stay listed". Show "3 seen, 3 no longer returned by source". Show the empty-read sentence even when retained rows exist: "latest read returned 0 questions; rows below are old". Open question: rename the count to "seen, not resolved: n".

**F06 [State coverage]** — [R2] Oldest-first windowing hides the newest questions, and no key reaches them (view.py:207-215 (lines[:keep]); render.py:309-311; seen "7/20 shown", "22/100 shown")
The cut keeps the oldest rows, so the question that just arrived is the first one off screen. "x/y shown" sits above "window full: older questions may be missing", so two kinds of missing (not displayed: newer; not returned by Orca: older) look like one. Up/Down and j/k move worker rows only; the key line says "Up/Down j/k move" with no object. Only e export holds the full list and the screen does not say so. After a shifted window every visible line can be "no longer in source window".
Fix: Open question: newest-first when cut, or keep in-window rows ahead of left-window rows, or a scroll key. At minimum print "7 oldest of 20 shown; 13 newer not shown (e exports all)", reword the source caveat as "Orca returned 100 rows (cap): older questions not returned", and change the key line to "j/k move workers".

**F07 [Component coverage]** — [R2] The freshness-strip cell for questions has no state word, so a FAILED or STALE source reads as a fresh read (view.py:733-737; seen in "fenced after ok" (header "last read 0s ago" above "FAILED (consumer-fenced) 0s") and "pure STALE" (header "last read 50s ago", no STALE))
The worker-list cell has OK / STALE / FAILED words; the questions cell does not, and "last read" can mean the failed attempt or the last success. The freshness strip is the line that never drops. EXPERIENCE.md:81, :218-221 give every source a state word.
Fix: Use the same grammar: "coordinator questions OK 0s" / "STALE 50s" / "FAILED (consumer-fenced), last good read 3h ago" / "NOT READ YET"; put the Run id in the cell.

**F08 [State coverage]** — [R2] At 80 columns the key line is cut before "e export" and "q quit" (view.py:75 (KEYS_LINE); render.py:416 (clip of help_line); seen at 80x30 and 80x24: "... m mark  e exp>")
Export is the only way to read hidden questions and quit is the escape key; both are cut at the narrowest supported width.
Fix: Wrap the key line like the footer counts, drop "Esc back" and "h historical" at 80, or print "e export  q quit" on a second line.

**F09 [Flow coverage]** — [R2] No Key Flow for a coordinator question arriving (EXPERIENCE.md:355 and rendering-rules.md:49 (change marks cover worker rows only))
A new question adds a line and raises the count, but nothing marks it as new, and the window may hide it (F06).
Fix: Add a flow "A coordinator question arrives" with a climax beat and the failure path "the list is longer than the screen". Open question: does the owner want a new-question cue (k new since HH:MM)?

**F10 [Flow coverage]** — [R2] No flow for the question source failing, being fenced, going stale or restarting (view.py:60-62, :585-599; adapter-contract.md:61; release-gates.md Q-1)
FAILED (consumer-fenced), FAILED (no-active-terminal), STALE with retained questions, a question that left the window and the restart reset are real paths with fixed screen words and appear in no flow or failure path. Q-1 is recorded FAIL, so for an observer started in a separate terminal FAILED is the first screen a supervisor sees, not an edge case.
Fix: Add failure paths ending in the exact on-screen words and the one action the supervisor can take outside the observer. Open question: design FAILED as the main screen for that case.

**F11 [Component coverage]** — [R2] No component row in either spine for the Coordinator questions panel or its parts (DESIGN.md Components; EXPERIENCE.md Component Patterns)
Title, run line, disclosure, state line, counts line, question line, x/y shown line, window-full line, retention line and the one-line summary have no anatomy or behaviour entry. The spines name only the gap notice, which the panel replaces.
Fix: Add one DESIGN.md row (anatomy, roles) and one EXPERIENCE.md pattern (what replaces the gap notice and when, what the summary is, what is never cut, lines are listed not selectable).

**F12 [State coverage]** — [R2] State vocabulary and view-level tables contain no question-panel rows (EXPERIENCE.md:276-283, :287-300)
None of PENDING, OK, STALE, FAILED (two codes), empty good read, window full, left window, retention reset, ignored-row notes, x/y shown or the collapsed summary is listed.
Fix: Add the exact strings from view.py:52-69 and, per state, what happens to retained questions and to the open count (never lowered).

**F13 [Inheritance discipline]** — [R2] Retired vocabulary is still in the spines ("OPEN HUMAN QUESTIONS": EXPERIENCE.md:176, :482, DESIGN.md:178; "marked looked": EXPERIENCE.md:484; "SEEN IS NOT RESOLVED" and "RETAIN CONTEXT" as panels: EXPERIENCE.md:69-70, :168, :177; rotation phrase "read k of N Runs since start": :216, :550; "one key away" / UX-OQ-3: :41, :69, :336, :529; auto-switch anti-pattern :423 and view rule :58)
A consumer reading the spines would build the old design. No "revisit" token remains (good).
Fix: Replace or mark each as superseded; close UX-OQ-3; re-scope OQ-13; reword the one-screen rules.

**F14 [Inheritance discipline]** — [R2] m is still described as moving a question to "marked looked"; the key table and footer do not say m marks worker rows only (EXPERIENCE.md:484, :320; view.py:75 ("m mark"); rendering-rules.md:40, :63)
New rule: m marks worker rows only and never changes the question count. A supervisor may press m expecting to mark a question.
Fix: Key table: "mark a look for worker rows; questions are not marked". Open question: footer wording "m mark rows".

### Medium (21)

**F15 [State coverage]** — [R2] FAILED outranks STALE, and the age means "since last good read" with a different meaning than the worker cell (view.py:574-583, :592)
A question source failing for three hours reads "FAILED (consumer-fenced) 3h" and never STALE. Retained questions render exactly as when OK, ages still counting up, with no "as of". "FAILED ... 50s" here means last good read 50 s ago; the worker cell's age is the failure age. A first-read failure has no age.
Fix: Under FAILED or STALE print "list as of HH:MM:SS (last good read)" above the list; use "FAILED (<code>), last good read <age> ago" or the spine's combined form (EXPERIENCE.md:283).

**F16 [Inheritance discipline]** — [R2] Scope mixing: header and COUNTS say scope=all and "runs seen", the panel says one Run only (view.py:722 ("one Run only" added only for a bound worker scope); adapter-contract.md:68; renders at 160/116/80)
The ledger beside the panel lists workers from every Run, titled "worker-reported, not questions". "runs seen: 1" plus "one Run only" reads as "these are all the questions"; it is derived from worker rows. At 116 and 80 columns the ledger has no run column.
Fix: Open question (build or spec): add "questions: one Run only <id>" to the header; add "questions from other Runs are not read" to the panel.

**F17 [State coverage]** — [R2] The FAILED sentence is inexact for no-active-terminal and gives no action (view.py:60-62, :594-595; adapter-contract.md "One named Run")
"this terminal does not hold the named Run" is a fair reading of consumer-fenced; for no-active-terminal the process holds no terminal at all. It is inferred from the error code alone. "the observer never binds to a Run" is an internal rule, not an instruction.
Fix: One sentence per code with the action, marked as inferred: consumer-fenced -> "this terminal is bound to another Run; start the observer in the terminal that holds <run id>"; no-active-terminal -> "no Orca terminal identity; start the observer from inside the Run's terminal".

**F18 [Inheritance discipline]** — [R2] Spec-vs-code drift: text the spec promises is not rendered (rendering-rules.md:41 (SEEN IS NOT RESOLVED block), :45 ("Questions stay until explicit resolution.", "No reply observed is not delivery failure."), :61 ("last seen HH:MM"), :63 (per-question "open, closure source unavailable"); view.py:67-69, :622-624)
None of these is in the real output at any width; the PENDING panel omits the disclosure and retention line; the spec itself says "no longer in source window" at :43 and "... (last seen HH:MM)" at :61. The central promise "seen is not resolved" survives only as "closed by evidence: unavailable (no source)".
Fix: Render each item or mark it dropped in the spec; adopt one string for the left-window flag. Open question for the spec owner.

**F19 [Component coverage]** — [R2] Identical lines, no id, unlabelled age, spoofable subject, ASCII "?" substitution (view.py:622-628; terminal.py:156-158; seen 4x "59m  Should I rebase onto master or merge?  reason unknown" and "1h  h?llo ?  reason unknown")
Five lines differing only by 1h / 59m cannot be told from one question asked five times; the id is only in the export. The leading age has no label while the ledger's evidence age means something else. A subject can imitate a state word ("RESOLVED by owner"). In ASCII mode a replaced character looks like a literal "?" and questions often end with one.
Fix: Add a short id suffix, a "waiting" column header, quote or bracket the subject, group repeats as x5, and in ASCII mode show \uXXXX or add "(non-ASCII shown as ?)" once. Open question: short id on each line?

**F20 [State coverage]** — [R2] "retention exceeded" hides a number the code knows (questions.py:21-24; view.py:610-614; seen at 116x40 "observed open: unknown (retention exceeded) (retained 1000)")
Double parentheses, wraps mid-sentence at 80, and the open total is known as a lower bound (nothing closes).
Fix: Open question: "at least 1,000 observed open (retention exceeded; oldest dropped)".

**F21 [State coverage]** — [R2] "observed open: 100" reads as exact; "window full" is printed far below it (view.py:635, :669; seen 116x40: count at line 9, "window full" 24 lines later)
Spec wording is "observed open: n" (rendering-rules.md:62).
Fix: Open question: "observed open: 100+ (window full)", or put window-full on the counts line.

**F22 [State coverage]** — [R2] Height budget: the ledger is squeezed to 2 rows and the x/y shown line is not budgeted (render.py:371-373 (comment promises at least 3 ledger rows); seen 116x24 and 80x24 "2/4 shown  +2 more"; EXPERIENCE.md:144-163 has no panel rows)
The panel base is 6-8 rows before any question; at 24 rows it takes 17 and the worker ledger gets 2.
Fix: Budget the cut line; add the panel to the shrink order. Open question: which block wins when height is short, ledger or questions?

**F23 [Component coverage]** — [R2] State, count and caveats are not findable at a glance (view.py:585-599, :635; seen 160 and 80)
In the OK state the panel has no state word. FAILED and STALE are a bare line after the two-line disclosure; the count is mid-line; about 35 words of boilerplate come before data. The palette is empty, so nothing replaces emphasis.
Fix: One first line under the title: "question read: OK | STALE 50s | FAILED (...) | pending", then the count, then the list, then the caveats as a block after the data.

**F24 [Bloat & overspecification]** — [R2] Three "shown" counters on one screen with no noun ("7/20 shown" (questions), "2/4 shown  +2 more" (workers), footer "shown 2/4 | collected ..." (workers); view.py:215)
A reader cannot tell which list each refers to.
Fix: "questions shown 7 of 20", "workers shown 2 of 4".

**F25 [State coverage]** — [R2] At 80 columns the COUNTS line cuts a state word: "cost un>" (seen at every 80-column render, line 4; header text built at view.py:751-760)
"unavailable" is hidden. Not checked whether R2 introduced it.
Fix: Let counts wrap to a third line at 80 or shorten to "cost n/a".

**F26 [Bloat & overspecification]** — [R2] The disclosure is a 28-word run-on that takes 2 rows on every frame; the panel spends 5-6 rows before the first question (view.py:54-57 (QUESTIONS_DISCLOSURE); seen at 116 and 80; jargon: "bounded best effort", "coverage unknown", "Run", "reason unknown")
Wording may be pinned by tests or the owner.
Fix: Open question: allow a plain-words version on screen ("May be incomplete. Shows what this terminal saw in its last read, up to 100 messages.") and keep the technical sentence in export / help; allow it to fold to one row.

**F27 [State coverage]** — [R2] The panel replaces the gap notice after a failed first read; the spine says the gap notice stays until the source has succeeded (view.py:673 (replaces_gap for OK and FAILED); EXPERIENCE.md:58, :233, :383)
The FAILED line plus "observed open: unknown (no question read yet)" is honest, so the spine is the part to change.
Fix: Restate the rule: the gap notice stays until the source has been read or has failed; PENDING keeps both.

**F28 [Token completeness]** — [R2] The panel has no colour, weight or frame assignment, and the build is unstyled (DESIGN.md:121-122, :146, :178; terminal.py:41-42 (PALETTE = {}); render.py:424-428)
"bad" is for FAILED source cells only; title, disclosure, state line and window-full have no role. The spine specifies colour, bold titles and a heavy frame for the question panel; the build emits unstyled text.
Fix: Add a question-panel component with roles. Open question: is the unstyled build intentional for R1/R2? If so say "styles PROPOSED, not applied".

**F29 [Flow coverage]** — [R2] UJ-1 assumes the "messages UNVERIFIED (not read)" cell and the gap notice (EXPERIENCE.md:437, :439)
With questions on the strip reads "coordinator questions: one Run, ..." and the panel replaces the gap notice.
Fix: Add a "questions on" variant or state that UJ-1 is the questions-off path.

**F30 [Inheritance discipline]** — [R2] Glossary split: "human questions" in the spine, "COORDINATOR QUESTIONS" on screen (EXPERIENCE.md:41, :69, :83, :233, :383; rendering-rules.md:32, :38)
The gap notice keeps its literal "Human questions: source UNVERIFIED ..." by spec; the title was retired because Orca has no human recipient field.
Fix: Glossary line: keep the literal; say "coordinator question" everywhere else.

**F31 [Inheritance discipline]** — [R2] Question subject text carries no "worker-reported" label (EXPERIENCE.md:376; view.py:47 (ledger title only))
The panel prints sanitized source text with no statement of where it came from.
Fix: Label the subject source in the disclosure or title, or state why not.

**F32 [Visual reference coverage]** — [R2] No durable wireframe of the R2 panel (workspace has no wireframes/ or mockups/; renders exist only in /tmp/r2render/out.txt)
A consumer has nothing to compare against.
Fix: Copy renders (5 questions OK at 160/116/80, empty, window full, fenced, STALE, collapsed) into wireframes/ with the commit noted, mark PROPOSED where the layout is PROPOSED, link inline.

**F33 [Inheritance discipline]** — EXPERIENCE.md sources frontmatter paths do not resolve and omit adapter-contract.md and owner-decisions-and-risks.md; updated date is stale (EXPERIENCE.md:7-17)
Paths point to _bmad-output/...; files are under .dev/issues/409/bmad/. Both files say updated 2026-11-08.
Fix: Correct paths, add the two sources, bump updated.

**F34 [Inheritance discipline]** — Line citations into rendering-rules.md have drifted (e.g. gap-notice rule cited :31 (now :32), unknown/absent :50-51 (now :53-54), stale :53 (now :56))
Not every citation checked.
Fix: Re-anchor by section name.

**F35 [Bloat & overspecification]** — EXPERIENCE.md restates sources and carries non-UX content (EXPERIENCE.md:338-349 (key-reader spike), :500-517 (Future Stage), :536-559 (carried OQ list))
About 560 lines against about 80 in the examples.
Fix: Cut to pointers naming the owning file.

### Low (11)

**F37 [State coverage]** — [R2] The retention-reset line sits last, under questions that look contradictory to it, and omits its consequence (render.py:315; view.py:66-68)
"questions observed before this start are not retained" sits under 1h-old listed lines. A restart drops left-window questions, so the open count can fall.
Fix: Place it under the counts line: "restart drops questions Orca no longer returns; count restarts at 0".

**F38 [Bloat & overspecification]** — [R2] "reason unknown" repeats on every question line (view.py:64, :622)
It carries no per-question information and is the first thing clipped.
Fix: Say once ("no reason field in source"). Spec asks for it per line (rendering-rules.md:43): needs the spec owner.

**F39 [State coverage]** — [R2] Negative age clamps to 0s, so clock skew shows a fresh question (view.py:620)
Unknown and skew look new.
Fix: Show "age unknown (clock skew)" when the difference is negative.

**F40 [Component coverage]** — [R2] Ages are coarse and ragged: "1h" then "59m" reads as out of order (view.py:316-322 (format_age))
No fixed-width age cell.
Fix: "1h 00m", minutes up to 119, or a clock time.

**F41 [Component coverage]** — [R2] The ">" truncation marker is also an ordinary subject character (terminal.py:35, :175-190)
A cut and a literal ">" look the same.
Fix: Fix with F04 so the cut is always at a fixed place.

**F42 [Inheritance discipline]** — [R2] Spine accessibility floor still describes colour ratios, muted "unknown" and a selection glyph the build no longer has (EXPERIENCE.md Accessibility Floor; DESIGN.md)
Empty palette, no selected question.
Fix: Update to built behaviour and add the R2 panel (and the "no promise for live screen readers" statement).

**F43 [Shape fit]** — [R2] Voice and Tone has no coordinator-question strings (EXPERIENCE.md:190-202)
No Do / Don't rows for the new wording.
Fix: Add rows: "no observed questions ...; not proof none exist" vs "no questions"; "observed open: n" vs "n unresolved"; "FAILED (consumer-fenced)" vs "disconnected".

**F44 [Inheritance discipline]** — [R2] The --ascii rule says "?" in ledger list cells only (DESIGN.md:195)
Question lines are not ledger cells but are substituted too.
Fix: Extend the rule to "list cells and panel question lines".

**F45 [Flow coverage]** — [R2] Two B shapes exist: fixture B (blocks, "NN MIN", "Affected:") and live R2 (one line per question) (EXPERIENCE.md:492-498; rendering-rules.md:38)
The R0 walkthrough steps through the fixture B.
Fix: Say the live panel is the R2 contract and the fixture a design reference.

**F46 [State coverage]** — [R2] No screen-level test pins a pure STALE panel, no-active-terminal, or the collapsed summary at 14-16 rows (tests/observe/test_render.py:412-610)
These render correctly in the lens runs but nothing pins them (and the collapsed summary is where F01 lives).
Fix: Add one screen test per state and per collapse height.

**F47 [Visual reference coverage]** — "Spines win on conflict" is not stated once; design-package exports are cited without saying which section each informs (EXPERIENCE.md:405-413)
One sentence and a short table.
Fix: Add both.

## Open questions for a human

1. When the window cuts, should the newest or the oldest questions stay on screen, and should a scroll key exist? (F06)
2. Which block wins when height is short: the worker ledger or the questions? Should the 3-row ledger promise hold? (F22)
3. Keep "observed open" or rename to "seen, not resolved"? Show "100+" when the window is full, and "at least n" for retention exceeded? (F05, F20, F21)
4. Is the single-column layout at 160 and 116 columns a deliberate change from the two-column B in the spec, and where does SEEN IS NOT RESOLVED live now? (F03)
5. Is the unstyled build (PALETTE = {}) intentional for R1 and R2, or should DESIGN.md's colours apply? (F28)
6. Does R2 satisfy PRD UJ-5 ("find the oldest question and inspect its evidence") in part, given there is no selection or inspector? (F02)
7. May the disclosure and per-line "reason unknown" be reworded or folded, or is the text pinned by the owner or tests? (F26, F38)
8. Where does the observer run in practice? With Q-1 recorded FAIL, a separate-terminal observer starts in FAILED; should that get its own design? (F10, F17)
9. Should each question line carry a short id, and should the header cell name the Run? (F19, F07, F16)
10. Is a screen-reader path in scope for the live screen, or only for --once? (A11y lens)

## Assumptions

- The spines in this folder are the unchanged 2026-11-08 copies; the "new design" is rendering-rules.md plus the code and tests at this worktree's HEAD.
- Line numbers are from this checkout and were read during the run; the rubric walker's spine line numbers refer to the copies in this folder.
- Screen behaviour was observed by rendering fixtures at 160, 116 and 80 columns and several heights; the collapse threshold (about 16 rows at 116 columns) is derived from the renders, not measured exhaustively.
- No persona, brand or scope was invented.

## Reviewer files

- `review-rubric.md`
- `review-accessibility.md`
- `review-adversarial.md`
