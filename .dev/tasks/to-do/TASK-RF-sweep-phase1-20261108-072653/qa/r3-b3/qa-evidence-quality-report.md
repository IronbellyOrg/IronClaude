# QA Report: R3-B3 evidence-quality lens

**Topic:** R3-B3 (three SPEC FR-010 incomplete-case fixtures), items 4.1 to 4.5 in `docs/designs/orchestrator-mode.md`
**Date:** 2026-11-09
**Phase:** fix-cycle gate review (evidence-quality lens), `fix_authorization: false`
**Files read (in chunks of at most 150 lines):** DESIGN lines 1-36, 236-305, 340-349, 351-448, 449-518, 519-618, 731-775, 871-950, 968-1030; research/04 lines 1-60 and 170-215; SPEC `merged-requirements.md` lines 95-121, 284-295, 318-321, 430-447; `phase-outputs/test-results/r3-b3-mechanical.md` lines 1-137.
**Live evidence gathered:** `orca-ide orchestration worker-list --help` (read-only help text, run once by this reviewer).

## Scope of the lens

Every statement the R3-B3 text makes about `worker-list`: the 100-row default, `page.nextCursor`, and the `call_failed` shape. Each is traced to research/04 section 4 and then to what is on disk. The R3-B3 text lives at DESIGN lines 11, 501 (new 7.2 bullet), 595 (7.4 source row), 746 (section 11 `test_classify.py` row), 771 (FR-010 row) and 1030 (Fix cycle 3 row).

## Evidence established

| Claim | Where DESIGN states it | What backs it |
|---|---|---|
| Default page is at most 100 rows | 299, 548, 614, 980 | The live help text (run now): "Returns at most 100 local rows, newest first, by default", and `--limit <1-100>`. SPEC line 320. research/04 line 38 and line 208. Backed. |
| Continuation is in `page.nextCursor` | 746 only | The same help text: "Opaque page cursor copied from page.nextCursor". It is help text, not a captured JSON body. research/04 lines 38 and 213 mark the JSON shape UNVERIFIED until step 1.0a item 3. |
| Reason `orca call failed (exit <n>)` for a later nonzero exit | 595, 746 | SPEC lines 287 and 439 define the string and the rule (first Orca call nonzero is `unavailable`; a later one is `call_failed`). It is classified by exit code, so no Orca output shape is involved. |
| Non-first `call_failed` was never induced against live Orca | not stated in DESIGN | research/04 line 214. Step 1.0a item 8 covers only the unknown-Run shape. The DESIGN fixture is a harness-injected failure, so it makes no claim about Orca output. |

## Findings

No BLOCKING and no MAJOR finding. The 100-row claim is backed. The `call_failed` text rests on SPEC-defined reason strings, not on an unverified Orca shape. The one place the DESIGN names `page.nextCursor` is a labelled synthetic fixture, which I grade MINOR (reasoning under E1).

### E1 (MINOR): `page.nextCursor` named in a pure-classify fixture with no UNVERIFIED tag

- Evidence: `docs/designs/orchestrator-mode.md:746`, the `test_fr010_full_page_uncaptured_continuation` text: "`truncated` True from a synthetic page whose `page.nextCursor` is non-null". It is the only DESIGN sentence that names `page.nextCursor`. None of the 13 `UNVERIFIED` hits (lines 49, 65, 126, 457, 498, 521, 610, 892, 903, 959, 990, 998, 1028) is near it.
- What is wrong: (a) The key name and location come from help text only (research/04:38, :213), and the sentence carries no UNVERIFIED tag and no pointer to open item 5 (line 980) or capture item 3 (line 891), which both hedge ("cursor field, if any"). (b) The sentence is in the wrong layer. `test_classify.py` is pure over `SweepInput` (the AST import test at line 746 bars `subprocess`, `os` and the rest), so no page JSON is parsed there. Per 7.3 (line 548) and open item 5 (line 980), `truncated` comes from the row count, and 7.2 line 501 says "whose continuation is not read". The cursor is inert, yet the sentence reads as if `truncated` derives from it.
- Why MINOR and not blocking: line 740 already treats hand-made fixtures as synthetic until step 1.0a, and the name is the one the CLI help itself prints, so it is a labelled stand-in, not a false claim.
- Smallest fix: at line 746 replace "from a synthetic page whose `page.nextCursor` is non-null" with "(a `SweepInput` with `truncated` True; the cursor name `page.nextCursor` is from `worker-list --help` and stays UNVERIFIED until step 1.0a item 3, open item 5)".

### E2 (MINOR): no section 11 test covers 100 rows to `truncated` True (SPEC AC) or the `Orca rows: 100 shown` line

- Evidence: DESIGN 346 says "section 8 paging" and 614 prints the banner. SPEC 321: "a 100-row fixture sets `truncated` and prints the lower-bound line". A grep of the DESIGN for `full page|100-row|paging not yet captured` finds no row in `test_probes_allowlist.py` (745) or `test_report.py` (747) that tests either. Only the `test_classify.py` fixture at 746 mentions a full page, and it receives `truncated` ready-made.
- What is wrong: the one place that turns a 100-row page into `truncated` (`collect`, 7.3 `WORKER_LIST_PAGE`) and the banner have no named test. The R3-B3 fixture's wording lets a reader assume the derivation is covered. This gap existed before R3-B3 and is not introduced by items 4.1 to 4.5.
- Smallest fix: add to the `test_probes_allowlist.py` "Result classes" list "a 100-row `worker-list` body sets `truncated`; 99 rows do not", and to `test_report.py` "the `Orca rows: 100 shown` line when `truncated`".

### E3 (MINOR): `call_failed` defined as "`unscanned` set"

- Evidence: `docs/designs/orchestrator-mode.md:501` "result is `call_failed` (its `sources` row `orca worker-list <run>` has `unscanned` set)" and `:595`. SPEC 287 and 292 make `call_failed` imply `unscanned`, but `unscanned` is also set when no call was made (under 1 s of budget left, SPEC 292) or after an unavailable result.
- What is wrong: the parenthetical reads as an iff. A Run whose `worker-list` never started would get the note `origin unknown: worker list call failed`. The class outcome (None, could not determine, not Historical) stays right. Only the note wording is imprecise.
- Smallest fix: "(its `sources` row `orca worker-list <run>` has `unscanned` set by a failed call)".

### E4 (MINOR): fixture 4 and the "differ by one input" claim are under-specified

- Evidence: `docs/designs/orchestrator-mode.md:746`. `test_fr010_outage_older_transcript_unknown_not_historical` sets `orca_rows` empty. `test_fr010_incomplete_notes_order` then needs "outage together with guard case 1, `session_join` None", and guard case 1 (line 502) needs at least one scoped Dispatch row. The sentence "the first three each differ from the complete-negative-join control by one input" is also loose: the outage fixture changes two inputs (`orca_available` and `orca_rows`), and the `call_failed` fixture adds a second Run.
- Smallest fix: say that the combined outage case keeps R1's rows collected before the outage, and change "by one input" to "by the list-incompleteness input".

## Notes (not findings)

- research/04 line 215 says nothing in the three rules depends on the capture. The DESIGN does not repeat that sentence, and it should not: counting a "full page" in `collect` needs the captured rows key (step 1.4 is gated on 1.0a, line 919).
- The mechanical report (`r3-b3-mechanical.md`) checks literal presence only. Its 9 checks cannot catch E1 to E4. I re-ran its counts: DESIGN is 1030 lines, em-dash count 0, no TODO or TBD, each `origin unknown:` literal appears twice (lines 501 and 746), and `four incomplete cases` appears once, in the Fix cycle 3 row. All agree with that report.
- Section 17 has no entry saying a non-first `call_failed` was never induced. This is not needed, because classification is by exit code (SPEC 287) and the DESIGN claims no Orca-side shape.

## Checks

A FAIL here carries only a MINOR finding, which never fails the gate.

| ID | Check | Result | Finding |
|---|---|---|---|
| C1 | The "100 rows by default" claim (DESIGN 299, 548, 614, 980) against research/04 :38, :208 and the live `worker-list --help` | PASS | none |
| C2 | Every DESIGN sentence naming `page.nextCursor` is tagged UNVERIFIED or sits in a labelled synthetic fixture | FAIL | E1 (MINOR) |
| C3 | The `call_failed` reason `orca call failed (exit <n>)` and the "later nonzero exit" rule trace to SPEC 287 and 439 | PASS | none |
| C4 | Fixture 3 (R2 `call_failed`, not call one) agrees with SPEC 287 and open item 4 (DESIGN 979) | PASS | none |
| C5 | DESIGN 7.2 bullet (line 501) equals research/04 section 4.2 item 2 word for word | PASS | none |
| C6 | DESIGN fixtures at 746 match the research/04 section 4.3 Given/When/Then rows | PASS | none |
| C7 | The three SPEC FR-010 acceptance fixtures (SPEC 104) are all present and named | PASS | none |
| C8 | Open item 5 and capture item 3 (DESIGN 980, 891) hedge the cursor field and page size | PASS | none |
| C9 | `call_failed` is defined without over-claiming (lines 501, 595) | FAIL | E3 (MINOR) |
| C10 | The "100 rows gives `truncated`" derivation and the banner have a test in section 11 | FAIL | E2 (MINOR, pre-existing) |
| C11 | The fixture set is internally feasible and the "one input" claim holds | FAIL | E4 (MINOR) |
| C12 | The mechanical report's facts re-verified (1030 lines, 0 em-dashes, no TODO or TBD, literal counts, section ranges) | PASS | none |
| C13 | Items 4.1 to 4.5 are present: 746, 501, 771, 1030, and the 595 source row | PASS | none |
| C14 | "four incomplete cases" survives only in the Fix cycle 3 quote (line 1030) | PASS | none |

## Confidence

Verified: 14/14 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%

The only unverifiable thing is the live `page.nextCursor` JSON location. It is a claim under review, not a check, and it stays UNVERIFIED until step 1.0a.

Tool engagement: Read: 17 | Grep: 11 | Glob: 0 | Bash: 2 (the `worker-list --help` run and the DESIGN count script). One earlier Bash call used a wrong tool name and did not run. No web research was done.

Self-audit: I can point to reads of every cited DESIGN range, the SPEC rows 104, 287, 320, 439, the research/04 section 4, and a live help run. The four findings are all MINOR. I did not find a sentence that states the cursor location or the non-first `call_failed` shape as an Orca fact. The nearest is line 746 (E1).

Verdict: PASS
Blocking count: 0

