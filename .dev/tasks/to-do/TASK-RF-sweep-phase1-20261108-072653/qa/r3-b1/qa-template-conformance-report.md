# QA Report: R3-B1 template-conformance lens

**Topic:** DESIGN `docs/designs/orchestrator-mode.md` after items 2.1 to 2.6 (R3-B1)
**Date:** 2026-11-09
**Phase:** fix-gate review, template-conformance lens (`fix_authorization: false`)
**Fix cycle:** 0 (first review of R3-B1)

Method: I read the DESIGN regions the R3-B1 edits touch (lines 1-36, 51-80, 353-399, 445-516, 724-753, 764-767, 815-818, 853-856, 866-901, 963-1023), research/04 lines 75-233, research/09 Gap 4 and the mechanical log. I re-ran the mechanical greps myself with Bash and did not rely on the log. The DESIGN file is untracked in git, so no diff was available. Instead I accounted for line count: 1013 at build time plus 2 (the time-parsing paragraph and its blank line) plus 8 (the `### Fix cycle 3` block) gives 1023, the file's actual `wc -l`. No other lines were added or removed.

## Findings

None BLOCKING. None MAJOR. Six MINOR notes (minor findings never fail the gate).

### m1 (MINOR): `### Fix cycle 3` intro does not copy the cycle 2 intro form

- Evidence: `docs/designs/orchestrator-mode.md:1009` (cycle 2 intro) names the review file `docs/designs/orchestrator-mode-review-2.md` and adds a sentence saying which minor notes were applied and which were not. `docs/designs/orchestrator-mode.md:1019` (cycle 3 intro) says only "Changes made for the blocking findings of review 3 and the re-anchor to master `5dc29d23`." It has no file path and no minor-note sentence.
- What is wrong: the table form is copied exactly, but the intro form is not. `docs/designs/orchestrator-mode-review-3.md` exists, so the path can be named. The R3-B1 edits apply minor notes m2, m4 and m5 (and m11 once R3-B2 lands). The intro does not say so.
- Note: the intro sentence is the wording task item 2.6 dictated (task file line 282), and the word "re-anchor" anticipates the R4 row from a later item. So this is a gap in the task wording, not a producer error.
- Smallest fix: write "Changes made for the blocking findings of `docs/designs/orchestrator-mode-review-3.md` and the re-anchor to master `5dc29d23`. Minor notes m2, m4, m5 and m11 were applied because they fall inside the R3-B1 and R3-B2 edits; the other minor notes are not addressed in this cycle."

### m2 (MINOR): the R3-B1 revision row does not name every change

- Evidence: `docs/designs/orchestrator-mode.md:1023`. Research/04 edit 9 (line 95) says the row "still names every change". The row omits (a) the correction of the cycle 2 R2-B1 row wording (m2, now at line 1013), and (b) the new note literal `Dispatch time window not observable` in 7.2 (line 496) and open item 23 (line 993) (m5). The cycle 2 row at line 1013 does name its minor-note change ("(m4)").
- Smallest fix: append to the line 1023 Change cell: "; the cycle 2 R2-B1 row now says the earliest `timestamp` in the transcript tail (m2); a match on a row with no observable window now gets note `Dispatch time window not observable` (7.2, 17) (m5)".

### m3 (MINOR): the new fixtures test a unit that 7.1 does not name

- Evidence: `docs/designs/orchestrator-mode.md:740` (three fixtures say "The `worker-show` parser builds `OrcaObservation`" and "Parser"), `docs/designs/orchestrator-mode.md:468` (the time-parsing rule names no function or module), `docs/designs/orchestrator-mode.md:353-399` (section 7.1 "Module signatures" lists only `collect` and the readers; it has no `worker-show` parser or time-parse signature). Section 7.1's own preface says its list holds every name the design proposes.
- What is wrong: section 11 maps tests to design elements, and this element is not in 7.1. A task-builder cannot tell what to call. The fixtures can still run through `collect` with `_orca` patched (section 11, line 732), so this is wording, not a missing deliverable.
- Smallest fix: in the three `test_worker_show_dispatch_times_*` fixtures replace "The `worker-show` parser builds `OrcaObservation`" with "`collect` with `_orca` patched builds `OrcaObservation`", or add one 7.1 signature for the parse helper.

### m4 (MINOR): one new sentence is long and nested

- Evidence: `docs/designs/orchestrator-mode.md:468`, second sentence ("Accepted forms are SQLite ... does not accept `Z`)."), about 55 words with two nested parentheses. The surrounding 7.2 text uses shorter sentences, although line 496 (about 48 words in its first new sentence) is no longer than the sentence it replaced.
- Smallest fix: split at "and ISO 8601 ...": "Accepted forms are SQLite `YYYY-MM-DD HH:MM:SS` (no zone, read as UTC; the form `datetime('now')` writes) and ISO 8601 with `Z` or an offset. `Z` is rewritten to `+00:00` first, because Python 3.10 `datetime.fromisoformat` does not accept `Z`."

### m5 (MINOR): section 11 cells now name test functions; earlier cells never did

- Evidence: `sed -n 726,750p` finds ten backticked `test_*` names, all in the R3-B1 text at lines 740 and 741. No other section 11 cell names a test function; they describe fixtures in prose.
- Note: research/09 Gap 4 and the R3-B2 and R3-B3 gates require the names, so keep them. Record this only so the later items (3.x, 4.x) follow the same convention for all three findings and the style is not a surprise.
- Smallest fix: none needed for R3-B1.

### m6 (MINOR): the mechanical log records an odd exit status

- Evidence: `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/phase-outputs/test-results/r3-b1-mechanical.md:87-89` shows Command 5 (`grep -nw 'TODO\|TBD'`) with no output and "(exit 0)". A grep with no match exits 1. The log's PASS result is right: my case-insensitive rerun over the file for `TODO`, `TBD` and `FIXME` printed nothing (rc=1).
- Smallest fix: record "no match (grep exit 1)" in the log. No DESIGN change.

## Checks

| ID | Check | Result |
|---|---|---|
| C1 | Row `GQ-103(3)` (line 60) keeps the 4-cell shape of header line 55 (5 unescaped pipes) | PASS |
| C2 | Row `OrcaObservation` (line 455) keeps the 2-cell shape of header line 451; `\|` escapes intact (3 unescaped pipes) | PASS |
| C3 | Row `TranscriptTail` (line 457) keeps the 2-cell shape of header line 451; `\|` escapes intact (3 unescaped pipes) | PASS |
| C4 | Section 11 rows (lines 740, 741) keep the 3-cell shape of header line 737 (4 unescaped pipes each) | PASS |
| C5 | 15.1 item 4 row (line 887) keeps the 3-cell shape of header line 882; open item 23 row (line 993) keeps the 4-cell shape of header line 969 | PASS |
| C6 | `### Fix cycle 3` table: header (1021) `\| ID \| Finding \| Change \|`, separator (1022) `\|---\|---\|---\|`, row 1023 has 3 cells, blank line before the table, same layout as cycle 2 (1011-1015) | PASS |
| C7 | `### Fix cycle 3` intro paragraph follows the cycle 2 intro form | PASS with notes (m1) |
| C8 | Section numbering unchanged: the heading list matches the mechanical log's section map; the only new heading is `### Fix cycle 3` (line 1017, unique, after `### Fix cycle 2` at 1007); no numbered heading added or renumbered | PASS |
| C9 | Em-dash count 0, en-dash count 0, ` -- ` prose count 0 over the whole file (own rerun) | PASS |
| C10 | `TODO`, `TBD`, `FIXME` absent, case-insensitive (own rerun, rc=1) | PASS |
| C11 | No marketing words (grep for robust, seamless, powerful, comprehensive, leverage, elegant, holistic and similar: no hits) | PASS |
| C12 | Prose style of new text matches the surrounding text (short declarative sentences, "could not determine" and "None" used as in neighbours, no line-number cross-references added) | PASS with notes (m4, m5) |
| C13 | All nine research/04 section 2.2 edits are present at their anchors (7.2 rows 455 and 457, line 468, line 496, 7.1 line 398, GQ-103(3) line 60, 15.1 item 4, open item 23, `### Fix cycle 3` plus the cycle 2 m2 wording at line 1013); the ten fixtures of research/04 section 2.3 and research/09 Gap 4 are named in lines 740 and 741; the FR-010 row (766) carries the Gap 4 recommendation | PASS with notes (m2, m3) |
| C14 | Totals untouched: `Total: 9 deviations.` and `Total: 23 open items.` (lines 819 and 995 per the mechanical log; line 995 read by me) | PASS |

Scope exclusions applied: the forward reference "Several matching rows follow the R3-B2 rule below." (line 496) and the transcript outcome for a path-B match that does not join are Phase 3 item 3.1 work and are not findings here.

## Summary

- Checks passed: 14 / 14 (3 with MINOR notes: C7, C12, C13)
- Checks failed: 0
- BLOCKING: 0, MAJOR: 0, MINOR: 6

Confidence: Verified: 14/14 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
Tool engagement: Read: 12 | Grep: 4 | Glob: 1 | Bash: 4

Verdict: PASS
Blocking count: 0
