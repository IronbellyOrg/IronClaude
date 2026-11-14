# QA Report: R3-B2 cross-reference chain lens (doc-qualitative, fix_authorization: false)

**Topic:** DESIGN `docs/designs/orchestrator-mode.md` after items 3.1 to 3.4 (R3-B2, several scoped Dispatch rows on one pane session)
**Date:** 2026-11-09
**Gate folder:** `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/qa/r3-b2/`
**Lens:** follow each new note literal through 7.2, 11, 12, 13, 14 and 18; every line or section number the new text cites must exist and say what is claimed.
**Fix cycle:** 1 (first review of this gate)

## Scope and method

DESIGN read from disk (1026 lines; `wc -l` confirmed), in chunks of at most 150 lines: lines 1-80, 449-518 (7.2), 596-643, 728-752 (11), 753-802 (12), 805-866 (13, 14), 868-965 (15), 967-1026 (17, 18). Inputs read: research/04 lines 120-176, research/09 Gap 4 (lines 139-175), `r3-b2-mechanical.md`, `docs/designs/orchestrator-mode-review-3.md` (grep for m11 and R3-B2), `ccsession` lines 560-617. A diff of the 1013-line base copy (`artifacts/design-base.md`) against the current DESIGN was used to see which hunks exist; the R3-B2 hunks are the 7.2 worker bullet, the `test_classify.py` row, the FR-010 row, D9, SP-29 and the R3-B2 row of section 18.

## Checks

| Check | What it verified | Result | Severity if FAIL |
|---|---|---|---|
| C1 | Anchors in `r3-b2-mechanical.md` (7.2 = 449-517, worker bullet = 498, section 11 = 728-752, hit lines 498/743/768/819/857/1015/1026, totals at 821 and 997) match the file on disk | PASS | |
| C2 | Literal `conflict: one pane session matches several Dispatch rows` reaches 7.2 (498), 11 (743, two fixtures), 12 (768, as `conflict:`) and 18 (1026); 13 (819) and 14 (857) carry the rule, not the literal, as research/04 edit 4 asks | PASS | |
| C3 | Literal `pane moved to a later session`: 7.2 (498) to 11 (743) to 18 R2-B1 row (1015); no stray copy elsewhere | PASS | |
| C4 | Literal `joined by pane: latest session of the pane`: 7.2 (498) to 11 (743) to 18 (1015) | PASS | |
| C5 | Literal `Dispatch time window not observable`: 7.2 (498) to 11 (743) to open item 23 (995) | PASS | |
| C6 | Pointers inside the new 7.2 text resolve: "Duplicate Dispatch bullet of this section" is line 509 and says "No row wins by position"; "the bullet that follows this one" is line 499 and holds `Orca pane session, not in scoped Runs`; "R3-B2 rule below" is the later part of the same bullet | PASS | |
| C7 | Each of the three 7.2 outcomes (one window holds, two or more hold, none holds) has a fixture in section 11; the order and terminal-handle fixtures exist; the seven R3-B2 fixture names each occur once (`uniq -c`) and do not collide with the R3-B1 names | PASS | |
| C8 | FR-010 row (768): cited sections 2.2 GQ-108, 7.1, 7.2, 13 exist; test files named in it exist in section 11; `test_probes_allowlist.py` Covers cell carries FR-010 (742) and `test_classify.py` Covers cell carries FR-010, SP-29, D9 (743) | PASS | |
| C9 | FR-010 (768), D9 (819) and SP-29 (857) wording agrees with 7.2 (one window holds; `conflict:` when two or more) | PASS | |
| C10 | Section 18 R3-B2 row (1026) names 7.2, 11, 12, 13, 14, all of which carry edits; m11 exists in review-3 (line 137) and is about the note order the new last sentence of 7.2 settles | PASS | |
| C11 | No line number of DESIGN itself is cited in the new text; the line anchors in research/04 (494, 495, 505, 739, 764, 815, 853) are stale by +4 and were correctly replaced by descriptive pointers; the DESIGN has no self-citation of lines 490-869 (regex sweep, all hits are SPEC, GAPS or REPORT lines) | PASS | |
| C12 | Open item 22 and capture item 13 (named by research/04 3.6), open item 23 and capture item 4 (named by 7.2) exist and agree; "Behaviour until closed" of items 22 and 23 keeps the several-rows rule inert until 1.0a | PASS | |
| C13 | Gate counters: one `Total: 9 deviations.` (821), one `Total: 23 open items.` (997), em-dash count 0, no `TODO` or `TBD` (grep exit 1), reproduced by my own commands | PASS | |
| C14 | Section 1 status block (lines 7-11) against the applied fix | FAIL | MINOR (F1) |
| C15 | The several-rows rule against the incomplete-tail rule and against line 499 and D9 wording | FAIL | MINOR (F2, F3) |
| C16 | Scope of the `tail_complete` default and fixture coverage for the parenthetical branch of 7.2 | FAIL | MINOR (F4) |
| C17 | D9 Source column (819) against the review that added the rule | FAIL | MINOR (F5) |
| C18 | Label consistency of `conflict:` (note versus reason) across 7.2 | FAIL | MINOR (F6) |

C14 to C18 are marked FAIL only because each carries a MINOR finding below. No check carries a BLOCKING or MAJOR finding.

## Findings

No BLOCKING and no MAJOR finding. Every number, section and line the new R3-B2 text cites exists and says what is claimed (C1 to C13). All findings below are MINOR notes and do not fail the gate.

### F1 (MINOR) Section 1 still describes R3-B2 as open
- Evidence: `docs/designs/orchestrator-mode.md:7` ("Three blocking findings were still open ... carried as the first required design-fix tasks") and `:10` (R3-B2 described as having "no rule decides"), while `:498`, `:743`, `:768`, `:819`, `:857` and `:1026` now carry the rule.
- What is wrong: the status block and the fix are both in the file, so a reader meets "no rule decides" and the rule in the same document. The earlier R3-B1 gate accepted the same state (`qa/r3-b1/verify-cycle1-rf-qa.md:74`), and line 7 says each finding is closed "by its own review gate", so this is expected until the gate closes.
- Smallest fix: when the R3-B1, R3-B2 and R3-B3 gates have all passed, rewrite lines 7-11 to say the three findings were closed in fix cycle 3 (section 18). No change needed in this gate.

### F2 (MINOR) The several-rows rule does not say how it combines with the incomplete-tail rule
- Evidence: `:498` has the single-row sentence "When the window is observable but the transcript has `tail_complete` False ... That match does not join: the row is could not determine with note `session start not observable: transcript tail only`, and that transcript is None with the same note", and later the several-rows sentences "If exactly one matching row's window holds the transcript ...". The `tail_complete` note literal appears nowhere in the several-rows text, and `:743` has only the single-row fixture `test_path_b_incomplete_tail_has_no_session_start`.
- What is wrong: with an incomplete tail and two rows, `first_record_ts` is not a session start, so "window holds the transcript" is not decidable, yet the several-rows sentence reads as if it were. A builder can implement either order.
- Smallest fix: add one sentence at the end of the several-rows text in `:498`: "With `tail_complete` False the incomplete-tail rule above applies first, to every matching row; the several-rows rule is not reached." Optionally add one two-row fixture next to `test_path_b_incomplete_tail_has_no_session_start`.

### F3 (MINOR) Line 499, D9 and SP-29 are not reconciled with the new priority rule from their own side
- Evidence: `:499` ("A transcript whose tab-map entry joins no scoped Orca row ... gets None with note `Orca pane session, not in scoped Runs`"), `:819` D9 ("A tab-map entry that joins no scoped row gives None with note `Orca pane session, not in scoped Runs`") and `:857` SP-29 ("a tab-map entry that joins no scoped row gets `person_started` None"). The new last sentence of `:498` says an entry that fails the window "takes these notes instead of `Orca pane session, not in scoped Runs` (in the bullet that follows this one)".
- What is wrong: the pointer runs one way only. An entry that matched a row but failed the window is also, in plain words, an entry that "joins no scoped row", so `:499` read alone gives the older note. The priority is stated only in `:498`.
- Smallest fix: in `:499` add "except an entry that matched a Dispatch row by path B and failed the window (worker bullet above)". D9 and SP-29 can stay as they are.

### F4 (MINOR) The `tail_complete` default is scoped to the R3-B1 fixtures, and one branch of the 7.2 text has no fixture
- Evidence: `:743` introduces the R3-B2 fixtures with "all under path B and all with aware UTC times"; the sentence "`tail_complete` is True unless a fixture says otherwise" sits later in the same cell and opens with "The R3-B1 path-B window fixtures". None of the seven R3-B2 fixtures sets `tail_complete`. Separately, `:498` has "(or `Dispatch time window not observable` when it has no observable window)" for an other matching row in the one-holds outcome, and no fixture exercises it (the mechanical table checks only the three outcomes).
- What is wrong: the R3-B2 fixtures depend on a default that is stated for another group of fixtures; a builder who picks `tail_complete` False would hit the incomplete-tail rule and fail all seven. The parenthetical branch is specified but untested.
- Smallest fix: change "all with aware UTC times" in the R3-B2 lead-in of `:743` to "all with aware UTC times and `tail_complete` True". Optionally add a fixture "D1 holds, D2 has `dispatch_started` None: S joins D1; D2 is could not determine with `Dispatch time window not observable`".

### F5 (MINOR) D9 Source column omits the review that added the new rule
- Evidence: `:819`, Source column: "Review 1 B2; review 2 R2-B1 and R2-B2". The D9 design cell now also carries the several-rows rule (R3-B2) and the time-window rule (R3-B1, `:819` "a path-B join also needs the Dispatch row's time window").
- What is wrong: the traceability of the deviation to its source reviews is incomplete; `:1025` and `:1026` are the only places that tie R3-B1 and R3-B2 to D9.
- Smallest fix: change the Source cell of D9 to "Review 1 B2; review 2 R2-B1 and R2-B2; review 3 R3-B1 and R3-B2".

### F6 (MINOR) `conflict:` is a "note" in the new text and a "reason" in the existing bullets
- Evidence: `:498` ("each of those rows is could not determine with note `conflict: one pane session matches several Dispatch rows`") against `:509` ("could not determine with reason `conflict: duplicate Dispatch rows disagree`") and `:510` ("reason `conflict: inconsistent observation`"). `:768` uses the bare prefix `conflict:`.
- What is wrong: the same prefix is called a note in one bullet and a reason in two others, in the same section. Nothing in DESIGN defines whether `conflict:` text goes to `Classification.notes` or to the could-not-determine reason line. The path-B literals around it (`pane moved to a later session`) are notes, so the choice here is defensible, but it is not stated.
- Smallest fix: in `:498` say "note and could-not-determine reason" for the `conflict:` literal, or add one line to the 7.2 observation rules saying a `conflict:` text is carried as a note and printed as the reason.

## Observations that are not findings
- The mechanical file's seven checks were reproduced by my own commands (C1, C13) and all hold. Its outcome-to-fixture table is correct.
- The producer changed research/04's "(line 505)" and "(line 495)" to descriptive pointers and added a forward pointer ("Several matching rows follow the R3-B2 rule below.") earlier in the bullet. Both are correct and avoid the +4 line drift.
- Existing citations next to the new text (`ccsession:574-602`, `:607-613`) were checked against `src/superclaude/skills/ccsession-tag/ccsession`: 574-605 is `orca_tab_session` (the write is at 601-602), 607-613 is the "same terminal means a person ran the command again" comment. Accurate.
- research/04 and research/09 quote DESIGN lines 494, 739, 764, 815 and 853; on disk these are now 498, 743, 768, 819 and 857. These are research notes, not DESIGN text, and nothing in DESIGN points at them.

## Inherited Structural Verdict, Reliance Audit
No `## Inherited Structural Verdict` section was in the spawn prompt, so this review ran standalone and re-checked structure itself.

## Self-Audit

**(a) Reliance list, rf-qa PASS items skipped for structural re-check:**
- None. The mechanical report `r3-b2-mechanical.md` was treated as a claim to test, not as ground truth.

**(b) Independent semantic checks (at least 1 required, INV-019):**
- Mechanical anchors reproduced: `wc -l` gave 1026; `grep -c` for the em-dash gave 0; `grep -nw 'TODO\|TBD'` exited 1; Read of lines 449-518 and 728-752 confirmed the section ranges and line 498; Grep with `-o` located every note literal (498, 743, 768, 819, 857, 995, 1015, 1026).
- Outcome-to-fixture mapping checked by reading the 7.2 sentences (`:498`) against the fixture cell (`:743`), including the boundary-second and terminal-handle fixtures; each fixture name occurs once (`grep -o | sort | uniq -c`).
- m11 checked in `orchestrator-mode-review-3.md:137` and matched to the last sentence of the 7.2 worker bullet.
- Diff of `artifacts/design-base.md` (1013 lines) against the current file listed 15 hunks, all in the R3-B1 and R3-B2 areas.
- Interplay of the new rule with `:499`, `:501`, `:819` and the incomplete-tail rule was read and produced F2 and F3.

**Confidence:** Verified: 18/18 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0% (13 PASS, 5 with a MINOR finding)
**Tool engagement:** Read: 14 | Grep: 10 | Glob: 2 | Bash: 4
**Web research:** none performed (no Tavily or fallback calls).

## Verdict

Verdict: PASS

Blocking count: 0

