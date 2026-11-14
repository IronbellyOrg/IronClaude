# QA Report: cross-reference chain, R3-B3 (doc-qualitative, cross-reference lens)

**Topic:** `origin unknown:` literals and `orca worker-list <run>` through DESIGN 7.1, 7.2, 7.4, 11, 12, 17 (open items 4 and 5) and 18
**Date:** 2026-11-09
**Phase:** doc-qualitative (adversarial, `fix_authorization: false`)
**Fix cycle:** 1 (first review of the 4.1 to 4.5 edits)
**Design file:** `docs/designs/orchestrator-mode.md` (1030 lines on disk at review time; the prompt said 1013 at build time, so every line number below is from the file as read now)

Inputs read in chunks of at most 150 lines: DESIGN lines 1-36, 62-67, 216-221, 223-350, 351-448, 449-523, 519-618, 619-646, 731-760, 756-807, 808-870, 871-920, 966-1030; research/04 lines 170-232; SPEC `merged-requirements.md` lines 95-124, 234-236, 255, 284-291, 316-322; `r3-b3-mechanical.md` lines 1-136. Two Bash calls: one read-only batch of greps and `sed -n` counts, one `orca-ide orchestration worker-list --help`.

## Link map (what I followed)

| Literal or reference | Where it is on disk | Claimed by | Result |
|---|---|---|---|
| `origin unknown: Orca unavailable`, `... worker list truncated`, `... worker list call failed` | DESIGN 7.2 line 501; section 11 line 746; bare prefix `origin unknown:` in section 18 line 1030 | research/04 4.2 items 1, 2, 4 | Present, spelled identically in 7.2 and 11 (batch C7: exactly 3 literals on each of lines 501 and 746). Absent from 7.1, 7.4, 12 and 17, which is correct because none of them needs the text |
| `orca worker-list <run>` | 7.2 line 501; 7.4 line 595; section 18 line 1030; instance `orca worker-list R2` at line 746 | research/04 4.2 item 2 | Present, same spelling, placeholder form in prose and instance form in the fixture |
| 7.1 | lines 374-378 (`OrcaResult.kind` includes `unavailable` and `call_failed`), 392 (`collect` returns `SweepInput`) | research/04 4.5 ("`collect` sets from result kinds already defined in 7.1") | Kinds exist. 7.1 does not say `collect` names the per-Run source row or sets `truncated` (M3) |
| 7.2 | `SweepInput.orca_available`, `truncated`, `sources` (line 456); `SourceCoverage.unscanned` (line 467) | line 501 reads these three | All three fields exist |
| 7.4 | line 595 | research/04 4.2 item 2, DESIGN line 1030 "(7.4)" | Exists, says what is claimed |
| 11 | line 746 | research/04 4.2 item 1 | Applied; "the four incomplete cases" is gone from 11 |
| 12 | FR-010 row, line 771 | research/04 4.2 item 3 | Applied in both columns |
| 17 open item 4 | line 979 | cited as "(open item 4)" at line 746 | Exists; says a nonzero `worker-list` exit on call one is `unavailable`, which is what 746 uses it for. Closed by 1.0a item 8, which is 15.1 row 8 (line 896) |
| 17 open item 5 | line 980 | research/04 4.4 evidence; not cited in DESIGN text for the new rule | Exists; says a full page of `WORKER_LIST_PAGE` rows sets `truncated`. Consistent with 7.2 line 501 and 7.3 line 548. Closed by 1.0a item 3, which is 15.1 row 3 (line 891) |
| 18 Fix cycle 3, R3-B3 | line 1030 (heading "### Fix cycle 3" at line 1022) | research/04 4.2 item 4 | Present; its "(11)", "(7.2)", "(12)", "(7.4)" pointers all resolve |
| SPEC FR-010 reasons | SPEC line 104 | 7.2 line 501 "(SPEC FR-010)" | Three of the four SPEC reasons carried; the fourth is not (M4) |
| SPEC cursor template | SPEC line 320 | DESIGN line 557 | Resolves, says "one extra template after the capture" |
| `orca call failed (exit <n>)` | SPEC line 287 | DESIGN line 595 and fixture at 746 | Resolves, same wording |

## Checks

| ID | Check | Result | Note |
|---|---|---|---|
| C1 | Section map: 7.1 (353), 7.2 (449), 7.3 (519), 7.4 (559), 11 (731), 12 (756), 17 (970), 18 (1002, Fix cycle 3 at 1022) exist at the lines the mechanical report states | PASS | Batch C6 output |
| C2 | The three `origin unknown:` literals in 7.2 line 501 match research/04 4.2 item 2 word for word and the SPEC line 104 reasons | PASS | M4 for the unmatched fourth SPEC reason |
| C3 | The same three literals in section 11 line 746 are identical to 7.2, and the four `test_fr010_*` names and their Given and Then match research/04 4.3 | PASS | M5 on Given wording |
| C4 | `orca worker-list <run>` is defined in 7.4 line 595, used in 7.2 line 501, and the fixture instance `orca worker-list R2` matches it | PASS | Batch counts: 7.2 = 1, 7.4 = 1, 11 = 0 for the placeholder form |
| C5 | Every section pointer inside the section 18 R3-B3 row ((11), (7.2), (12), (7.4)) exists and holds what the row says | PASS | |
| C6 | Open item 4 (line 979) exists and supports the "(open item 4)" claim at line 746; its "Closed by" (1.0a item 8) is 15.1 row 8 | PASS | |
| C7 | Open item 5 (line 980) exists and is consistent with 7.2 line 501, 7.3 line 548, 7.5 line 614 and 15.1 row 3 | PASS | M1 and M2 |
| C8 | 7.1 anchors the chain: `OrcaResult` kinds and `collect` exist | PASS | M3: no 7.1 text names the source row or sets `truncated` |
| C9 | Section 12 FR-010 row (line 771) agrees with 7.2 (501, 502), D9 (line 822) and SP-29 (line 860) on "three list-incomplete" plus "four join-incomplete" | PASS | |
| C10 | The 4.2 item 4 correction in section 18 is accurate about cycle 2 | PASS | M6: the quoted cycle 2 wording is not verbatim |
| C11 | Research/04 4.2 items 1 to 4 were applied to the DESIGN as written | PASS | Item 1 at 746, item 2 at 501, item 3 at 771, item 4 at 1030 |
| C12 | Mechanical gate: "four incomplete cases" only at line 1030; em-dash 0; no TODO or TBD; `Total: 9 deviations.` at 824; `Total: 23 open items.` at 1000 | PASS | Re-run by me; matches `r3-b3-mechanical.md` |
| C13 | The mechanical report's section ranges and per-section literal counts are true | PASS | My `sed -n` range counts equal its table |
| C14 | Everything the new rule depends on is defined in a DESIGN section it can be traced to ("Historical", per-Run list state, `truncated`) | FAIL (MINOR only) | M7: "Historical" is defined only in the SPEC, not in the DESIGN |
| C15 | The new fixtures do not contradict 7.2 guard cases 1 to 4 (line 502) | FAIL (MINOR only) | M5: shared Given says the guard "otherwise holds" while fixtures 2 and 3 fire case 2 as written |
| C16 | Note precedence is unambiguous across 7.2 lines 498-502 | FAIL (MINOR only) | M8 |
| C17 | The three notes cover every way a scoped worker list can be incomplete | FAIL (MINOR only) | M4 (tab map unreadable) and M9 (list never started) |

Checks passed: 13 / 17. Checks failed: 4, all MINOR-only, so none fails the gate. No BLOCKING or MAJOR finding.

## Findings

No BLOCKING and no MAJOR finding. I looked for a broken link in each hop (see the link map) and found none: every cited section, line and open-item number exists and says what the citing text claims. The nine MINOR findings are gaps in the chain, not broken links. None fails the gate. C2, C3, C7, C8 and C10 pass with a MINOR note attached (M1, M2, M3, M6) because the assertion each one makes is true; the note records what the chain still lacks.

### M1 (MINOR): `page.nextCursor` appears in the DESIGN only inside a fixture, with no source and no UNVERIFIED mark

- Evidence: DESIGN line 746, `test_fr010_full_page_uncaptured_continuation` ("a synthetic page whose `page.nextCursor` is non-null"). Grep for `nextCursor` over the DESIGN and the SPEC returns that one line only. The design's own statements about the field say it is unknown: 15.1 row 3 (line 891, "the cursor or continuation field, if any"), open item 5 (line 980, "cursor field", "no cursor template"), and 7.3 line 557 (template added only after capture).
- What is wrong: the field name is correct (`orca-ide orchestration worker-list --help` says "Opaque page cursor copied from page.nextCursor" and "Returns at most 100 local rows"), but the DESIGN never says where the name comes from, and it reads as fact next to an open item that says the field is unknown. research/04 4.5 tagged it "UNVERIFIED until step 1.0a (help text only)"; that tag did not reach the DESIGN.
- Smallest fix: at line 746 change the clause to "a synthetic page whose continuation field is non-null (`page.nextCursor` per `worker-list --help`; live shape UNVERIFIED, open item 5)".

### M2 (MINOR): the new truncated rule is not linked to open item 5, although the call_failed rule is linked to open item 4

- Evidence: line 746 cites "(open item 4)" for the `call_failed` fixture; neither line 501 nor the `test_fr010_full_page_uncaptured_continuation` text nor the FR-010 row (line 771) cites open item 5 (line 980) or 7.3 line 548. Open item 5 is the only place that says what sets `truncated` until the capture closes.
- What is wrong: a reader of 7.2 line 501 or of the fixture cannot reach the rule that decides when `truncated` is True before step 1.0a. The two sibling cases are cited unevenly.
- Smallest fix: in 7.2 line 501, after "whose continuation is not read" add "(open item 5, section 7.3)".

### M3 (MINOR): 7.1 has no text for the per-Run source row or for how `truncated` is set

- Evidence: 7.1 (lines 353-448) mentions neither `worker-list`, `truncated`, `WORKER_LIST_PAGE` nor the source-row name; `collect` is one signature line (392). research/04 4.5 says these are set "from result kinds already defined in 7.1", which holds for the kinds (374-378) but not for the mapping. The source-row name lives only in the prose line at 7.4 line 595, after the JSON block. Pre-existing gap of the same kind: section 12 FR-002 row (line 763) cites "(5, 7.1)" for "first call per Run is `worker-list`", and 7.1 does not say it (section 5 line 240 does).
- What is wrong: the signature section that a code task will implement from is silent on the one behaviour the three new rules depend on.
- Smallest fix: add one comment line under `collect` (line 392): "# per scoped Run: source row `orca worker-list <run>`; unscanned set on call_failed; truncated True on a full WORKER_LIST_PAGE page".

### M4 (MINOR): SPEC FR-010 lists four origin-unknown reasons; the DESIGN carries three

- Evidence: SPEC line 104: "Orca unavailable, worker list truncated, worker list call failed or tab map unreadable". DESIGN 7.2 line 501 and line 746 carry the first three. A grep of the DESIGN for "tab map unreadable" finds nothing. 7.1 line 401 `read_tab_map` returns a bare tuple, while the comment at line 394 says every reader returns "data plus a SourceCoverage row", so an unreadable tab map has no carrier. Research/04 4.2 item 2 says the literals "follow the SPEC reasons", and the SPEC wording is "such as", so this is not a contradiction.
- What is wrong: the FR-010 row (line 771) reads as covering the whole guard, but the tab-map-unreadable half of the SPEC guard ("the tab map is read and the join completed") has no rule or note. Under path A, an unreadable `orca-tabs/` yields no entries and line 500 can make a no-entry transcript True.
- Smallest fix: either add a fourth note `origin unknown: tab map unreadable` to line 501 with one fixture, or add a Deviation or open-item line saying the fourth reason is not carried in Phase 1 and why.

### M5 (MINOR): the shared Given of the three SPEC fixtures says the join guard "otherwise holds", but a 100-row or R1-with-rows list with no joined transcript fires guard case 2

- Evidence: line 746 shared Given: "joined to no Orca row, and the join guard otherwise holding (path A, `session_join` present on every scoped row)". Fixture 2 gives R1 exactly 100 rows "none joined to T"; fixture 3 gives R1 `worker-list` ok. Line 502, case 2: "Orca returned at least one worker row and no transcript joined any Orca row" makes the guard fail and adds the SP-16 note and the `could not join Orca workers to transcripts` line. The fixtures name no second transcript that joins a row. Also: the text says the first three "each differ from the complete-negative-join control by one input"; fixture 1 changes two (`orca_available` False and `orca_rows` empty). Fixture 4 (`test_fr010_incomplete_notes_order`) pairs the outage with guard case 1, which needs a scoped Dispatch row with `session_join` None, but fixture 1's shape has no rows; its Then also does not say where the SP-16 literal sits if case 2 holds too.
- What is wrong: as written the fixtures do not isolate the new rule from case 2, so "one input" is an overclaim. The Then assertions still hold, so no wrong behaviour results.
- Smallest fix: add to fixtures 2 and 3 "and a second transcript U joined to one of the R1 rows, so case 2 does not fire"; reword "one input" to "one named input"; in fixture 4 state that the outage came after the list returned rows.

### M6 (MINOR): section 18 misquotes cycle 2

- Evidence: line 1030 quotes cycle 2 as "changed three to four incomplete cases"; line 1018 reads `changed "three" to "four" incomplete cases (11)`. The mechanical gate (`r3-b3-mechanical.md` Check 4) finds the one remaining "four incomplete cases" hit only because of the misquote; the true cycle 2 row contains `"four" incomplete cases` and does not match that grep.
- What is wrong: a quotation that is not verbatim, in the row whose purpose is to correct that sentence.
- Smallest fix: at line 1030 write `Corrects cycle 2's 'changed "three" to "four" incomplete cases'`, then update Check 4 of the mechanical report to grep for `"four" incomplete cases` as well.

### M7 (MINOR): "Historical" is relied on by the new rule and fixtures but is defined only in the SPEC

- Evidence: DESIGN mentions of Historical are lines 501, 629 (a heading), 746, 822 and 868; none states which rows go there. The SPEC states it at line 104 ("one with no activity inside the window goes to Historical sessions (GQ-108)") and rule 7 at SPEC line 255. DESIGN GQ-108 (line 65) does not repeat it. The new bullet (line 501, "never idle or Historical") and fixtures 1 to 3 ("not Historical", `summary.historical` 0) assert the negative of a predicate the DESIGN never writes.
- What is wrong: the link from line 501 resolves only by reading the SPEC; a task builder working from the DESIGN has no positive rule to test the negative against.
- Smallest fix: add one sentence to 7.2 near line 500: "A readable transcript with `person_started` True and no activity inside the window is Historical (SPEC FR-010); every other row stays visible."

### M8 (MINOR): precedence between `Orca pane session, not in scoped Runs` (line 499) and the new `origin unknown:` notes (line 501) is not stated

- Evidence: line 499 gives a transcript with a tab-map entry that joins no scoped row None "with note `Orca pane session, not in scoped Runs`". Line 501 gives "every unjoined transcript" the `origin unknown:` note "before any join-guard note". Line 498 states that tail, window and several-rows notes replace the line 499 note, but nothing says what happens during an outage or truncation. All four fixtures use a transcript with no tab-map entry.
- What is wrong: during an outage the line 499 note ("not in scoped Runs") asserts a fact the sweep could not observe. Both rules give `person_started` None, so the class is the same; only the notes differ.
- Smallest fix: add to line 501 "and it replaces the `Orca pane session, not in scoped Runs` note of the previous bullets", and add one fixture variant with a tab-map entry.

### M9 (MINOR): a worker-list never started for lack of budget has no `origin unknown:` note

- Evidence: line 501 names three triggers (`orca_available` False, `truncated`, `call_failed`). Section 5 line 287 makes a budget-cut call `call_failed`, so a cut call is covered. 7.1 line 371 returns None from `call_timeout()` below 1 s left and line 378 shows `unscanned: time budget reached (90 s)` as an `OrcaResult.reason`; a `worker-list` that is skipped for that reason produces an unscanned source row and no `call_failed` result. SPEC line 104 says "no relevant list or join is unscanned or truncated".
- What is wrong: that list is incomplete and unscanned but matches none of the three triggers. Only reachable with several Runs and a nearly exhausted budget.
- Smallest fix: in line 501 change "`call_failed` (its `sources` row ... has `unscanned` set)" to "`call_failed` or not started (its `sources` row ... has `unscanned` set)", keeping the same note.

## Inherited Structural Verdict: Reliance Audit

No `## Inherited Structural Verdict` block was supplied in the prompt, so I relied on no rf-qa PASS. The mechanical report `r3-b3-mechanical.md` was treated as a claim to test, not as evidence.

## Self-Audit

**(a) Reliance list: rf-qa PASS items skipped for structural re-check:**
- None. I re-ran every mechanical check myself (batch C1 to C8: counts, em-dash, TODO or TBD, both totals, section map, per-section literal counts).

**(b) Independent semantic checks (at least 1 required, INV-019):**
- Open item 4 supports the call_failed fixture: Read DESIGN 979, then SPEC 287 ("treat nonzero exit ... on the first Orca call as unavailable ... a later nonzero exit ... is `call_failed`") and the DESIGN fixture at 746 (R2, not call one). Consistent.
- Open item 5 and the cursor claim: Read DESIGN 980, 548, 557, 891; SPEC 320; ran `orca-ide orchestration worker-list --help` (100-row default, `page.nextCursor`). Found M1 and M2.
- Guard-case interplay: Read DESIGN 502 against the shared Given and Thens at 746. Found M5.
- SPEC reason coverage: Read SPEC 104 against 7.2 line 501; grep for "tab map unreadable" in the DESIGN returns nothing. Found M4.
- Historical definition: grep of "Historical" in the DESIGN and SPEC. Found M7.
- Quote accuracy: Read 1018 against 1030. Found M6.

**Counts:** claims independently verified: 30 (13 link-map rows, 17 checks). Files read: DESIGN, research/04, SPEC, `r3-b3-mechanical.md`. Why a 0 BLOCKING result is credible: each hop was followed to its target line and compared with the claim; the nine MINOR findings come from that comparison, and the strongest ones (M4, M5, M7) are real gaps that the earlier mechanical gate did not test.

**Confidence:** Verified: 17/17 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
**Tool engagement:** Read: 22 | Grep: 9 | Glob: 0 | Bash: 2 (one batch of grep or `sed -n` groups; one `orca-ide ... --help`, read-only, not bare `orca`)
**Web research:** none; the Tavily-first rule did not apply.

Verdict: PASS
Blocking count: 0
