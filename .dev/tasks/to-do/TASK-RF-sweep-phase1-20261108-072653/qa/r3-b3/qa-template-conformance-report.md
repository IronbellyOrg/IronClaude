# QA Report: R3-B3 template-conformance lens

**Topic:** R3-B3 edits (items 4.1 to 4.5) to `docs/designs/orchestrator-mode.md`
**Date:** 2026-11-09
**Phase:** fix-cycle gate review (template-conformance lens), `fix_authorization: false`
**Design file state:** 1030 lines, untracked in git, so no `git diff` baseline exists. I read every edited region in full (lines 449-518, 559-598, 731-755, 756-777, 1000-1030, 1-36) and ran form checks over the whole file. I cannot prove by diff that no other line changed; I can only say no form break turned up anywhere I checked.

## Scope of what I tried to break

| Attack | Result |
|---|---|
| 7.2 bullet breaks the list style | Not broken. Line 501 sits between lines 500 and 502 in the `Joins` list, with the same `- ` marker, one paragraph, one period-ended run of sentences, and a lead-in label like `Rule 1 notes (M6):` and `Age (SP-26, D5):`. |
| A table row with a changed cell count | Not broken. Every edited row (746, 771, 1030) has the same pipe count as its table. |
| A 7.4 sentence that changes the JSON key set | Not broken. The 7.4 code block (563-593) is untouched in its keys, and line 595 is prose after the block that adds no key. |
| Em-dash | 0 (`grep -c '—'`), and 0 non-ASCII characters in the whole file. |
| `TODO`, `TBD`, `FIXME` | 0 (case-insensitive). |

## Findings

All findings are MINOR. None blocks the gate.

### F1 (MINOR) Shared Given says "the join guard otherwise holds" but the full-page fixture trips guard case 2

- Evidence: `docs/designs/orchestrator-mode.md:746` (shared Given: "joined to no Orca row, and the join guard otherwise holding (path A, `session_join` present on every scoped row)"; full-page fixture: "scoped R1 with exactly `WORKER_LIST_PAGE` (100) rows ... none joined to T"). Guard case 2 is at `:502` ("Orca returned at least one worker row and no transcript joined any Orca row").
- What is wrong: with 100 worker rows and T (the only transcript named) joined to none, case 2 fires. The guard does not "otherwise hold". T would then also carry the SP-16 literal and the `could not join Orca workers to transcripts (tab map empty or stale)` line prints. The fixture's Then lists only the `origin unknown:` note. The same gap applies to the `call_failed` fixture if R1 returns any row. The control fixture avoids it by having a second transcript that joins a row; the three new fixtures do not say that.
- Smallest fix: add to the shared Given "a second transcript U joins an Orca row of R1", or say the SP-16 note may also be present and that the assertion is note inclusion, not equality.

### F2 (MINOR) Note precedence between `origin unknown:` and the non-guard join notes is not stated

- Evidence: `:501` says "in that order when several hold, before any join-guard note". Line `:499` gives a tab-map-entry transcript the note `Orca pane session, not in scoped Runs`, and `:498` gives path-B transcripts `pane moved to a later session`, `session started before this Dispatch window` and similar. None of those is a "join-guard note" (the guard cases are at `:502`).
- What is wrong: `:501` says "Every unjoined transcript is then None with note ...", which includes the tab-map-entry and path-B ones, but the order against their notes is open. Section 11 (`:746`) tests order only against `tab map join not observable`.
- Smallest fix: change "before any join-guard note" to "before any other join note".

### F3 (MINOR) "each differs from the control by one input" is loose

- Evidence: `:746`: "the first three each differ from the complete-negative-join control by one input".
- What is wrong: the outage fixture sets `orca_available` False and `orca_rows` empty. The `call_failed` fixture adds a second Run R2. The full-page fixture changes both `truncated` and the row count. These are single causes but not single input fields.
- Smallest fix: say "each differs from the control in one list-completeness cause".

### F4 (MINOR) Notes-order fixture does not give its rows

- Evidence: `:746`: `test_fr010_incomplete_notes_order` "(outage together with guard case 1, `session_join` None ...)". The outage fixture above it has `orca_rows` empty. Guard case 1 (`:502`) needs a scoped Dispatch row whose `session_join` is None.
- What is wrong: with no rows, case 1 cannot hold, so the first half of this fixture cannot be built from the Given of the outage fixture. It needs rows kept from before the outage (FR-002: a later unavailable result keeps already collected evidence).
- Smallest fix: add "with one retained R1 row whose `session_join` is None" to that fixture.

### F5 (MINOR) The R3-B3 log row quotes cycle 2's wording differently from the row it corrects

- Evidence: `:1030` quotes `"changed three to four incomplete cases"`; the source row at `:1018` reads `changed "three" to "four" incomplete cases (11)`. The `:1018` row is left unchanged, which research/04 section 4.2 item 4 allows.
- What is wrong: quotation marks sit in different places. The mechanical check 4 (one `four incomplete cases` hit, at `:1030`) passes only because of the paraphrase.
- Smallest fix: quote `:1018` exactly, or drop the quote marks at `:1030`.

### F6 (MINOR, not an R3-B3 edit) Table at `:55-:64` has a 6-cell row in a 5-cell table

- Evidence: `docs/designs/orchestrator-mode.md:64` (GQ-107 row) has an unescaped `|` inside the code span "escapes `|` as `\|`". My awk pass over every table gives one mismatch in the file, this line.
- What is wrong: GFM splits cells on the bare pipe, so the row renders with an extra cell. Items 4.1 to 4.5 do not touch GQ-107. Because the file is untracked I cannot prove it pre-dates the edits, but nothing in R3-B3 relates to it.
- Smallest fix: write `\|` inside that span too, in a separate item.

## Result of the specific attacks, with evidence

- 7.2 bullet (`:501`): note literals `origin unknown: Orca unavailable`, `origin unknown: worker list truncated`, `origin unknown: worker list call failed` match the SPEC FR-010 reason order "Orca unavailable, worker list truncated, worker list call failed" (SPEC `merged-requirements.md:104`). The bullet sits exactly where research/04 section 4.2 item 2 asks: before the "join completed" bullet (`:502`).
- Section 11 (`:746`): all four fixture names and their Given/When/Then match research/04 section 4.3 (names, `--run R1`, `WORKER_LIST_PAGE` 100, `page.nextCursor`, R2 `call_failed`, `orca call failed (exit 1)`, order sentence). The phrase "the four incomplete cases" is gone from sections 1 to 17. The `orca call failed (exit <n>)` reason form matches SPEC line 439.
- FR-010 row (`:771`): the design column adds "with its three list-incomplete cases (outage, full page, `call_failed`) and" after "completeness guard", and the test column adds "the three SPEC incomplete-case fixtures", both as research/04 item 3 asks. "four join-incomplete cases" stays consistent with `:502` ("in four cases"), D9 (`:822`) and SP-29 (`:860`).
- Fix cycle 3 (`:1030`): the R3-B3 row has the same three-cell shape as R3-B1 and R3-B2 (`:1028`, `:1029`), the same ID and past-tense style, and carries the item 4.2 text plus the "(7.4)" reference.
- 7.4 (`:595`): says the per-Run source row is named `orca worker-list <run>` and a `call_failed` result sets `unscanned`. The `sources` object at `:571` already has `name` and `unscanned`, so no key is added. The name is used identically at `:501`, `:595` and `:746`.
- Reference integrity: `call_failed` is an `OrcaResult.kind` (`:376`); `WORKER_LIST_PAGE` is defined at `:548`; `truncated` and `orca_available` are `SweepInput` fields (`:456`); `summary.historical` and `summary.total_is_lower_bound` are in the 7.4 summary object (`:588-589`).
- Totals: `Total: 9 deviations.` at `:824` (9 `D` rows counted); `Total: 23 open items.` at `:1000` (23 rows counted). Fence count is 28, so balanced.

## Checks

A check marked FAIL (MINOR only) found a MINOR defect; MINOR findings never fail the gate.

| Check | What was checked | Result |
|---|---|---|
| C1 | 7.2 bullet (`:501`) placement and list style against `:496-503` | PASS |
| C2 | 7.2 note literals and order against SPEC FR-010 (`merged-requirements.md:104`) | PASS |
| C3 | 7.4 sentence (`:595`) leaves the JSON key set and the pinned v1 paragraph unchanged | PASS |
| C4 | Cell count of the edited rows (`:746`, `:771`, `:1030`) against their tables | PASS |
| C5 | Em-dash and non-ASCII count over the whole file (0 and 0) | PASS |
| C6 | `TODO`, `TBD`, `FIXME` count (0) | PASS |
| C7 | Backtick, parenthesis and code-fence balance on edited lines and file | PASS |
| C8 | Heading structure, `Total: 9 deviations.` and `Total: 23 open items.` verified by row count | PASS |
| C9 | "four incomplete cases" absent outside `:1030`; "four join-incomplete cases" consistent in `:502`, `:771`, `:822`, `:860` | PASS |
| C10 | Section 11 cell matches research/04 4.2 item 1 and the 4.3 fixture names and Given/When/Then | PASS |
| C11 | FR-010 row matches research/04 4.2 item 3 | PASS |
| C12 | Fix cycle 3 R3-B3 row matches 4.2 item 4 and the shape of its sibling rows | PASS |
| C13 | Reference integrity: `call_failed`, `WORKER_LIST_PAGE`, `truncated`, `orca_available`, summary keys exist | PASS |
| C14 | Source name `orca worker-list <run>` and reason `orca call failed (exit <n>)` consistent across 7.2, 7.4, 11 and SPEC line 439 | PASS |
| C15 | Fixture Given against guard case 2 (F1) and notes-order fixture rows (F4) | FAIL (MINOR only) |
| C16 | Note precedence wording at `:501` against other join notes (F2); "one input" claim (F3); quote fidelity (F5) | FAIL (MINOR only) |
| C17 | Whole-file table cell consistency (F6, line 64, not an R3-B3 edit) | FAIL (MINOR only) |

## Summary

- Checks passed: 14 / 17
- Checks failed: 3, all MINOR only
- BLOCKING: 0, MAJOR: 0, MINOR: 6 (F1 to F6)
- **Confidence:** Verified: 17/17 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Limit:** the design file is untracked, so I could not diff it against a pre-edit baseline. Checks cover the five edited regions in full plus whole-file form scans.
- **Tool engagement:** Read: 9 | Grep: 6 | Glob: 0 | Bash: 10

Verdict: PASS
Blocking count: 0
