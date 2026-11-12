# QA Report: R3-B2 template-conformance lens

**Topic:** DESIGN `docs/designs/orchestrator-mode.md` after items 3.1 to 3.4 (R3-B2, several Dispatch rows on one pane session)
**Date:** 2026-11-09
**Phase:** fix-gate review, domain lens (template conformance; research/09 Gap 5 sizing row 500-1500 lines, DESIGN is 1026 lines)
**fix_authorization:** false (no file edited except this report)

## What I read

- DESIGN lines 1-36, 449-517, 726-803, 805-866, 997-1026 (each read in chunks of at most 150 lines).
- research/04 lines 118-177 (section 3 R3-B2 edits 1 to 5 and fixtures 3.4).
- research/09 lines 139-179 (Gap 4, start of Gap 5).
- `phase-outputs/test-results/r3-b2-mechanical.md` (117 lines).
- Independent mechanical checks run by me (awk pipe count per table row, grep for em dash, en dash, ` - `, `TODO`, `TBD`, `FIXME`, grep for the note literals and the seven fixture names, grep for review-ID tokens). I did not rely on the producer's mechanical report.

## Findings

### F1 (MINOR) Review ID in 7.2 prose points at a rule that carries no such label

- Evidence: `docs/designs/orchestrator-mode.md:498`, "Several matching rows follow the R3-B2 rule below." Grep of the whole design finds `R3-B2` in body prose only here (other hits: 10, 742, 743 in section 11 fixture prose, 1026 in the revision log).
- What is wrong: the rest of 7.2 names its authorities by the catalogued IDs (GQ-108, SP-16, SP-29, M6, D5, D9). The R3-B2 rule that follows is unlabelled, so "the R3-B2 rule" cannot be found by a reader of 7.2. research/04 line 90 planted this pointer for the R3-B1 edit; research/04 section 3.3 edit 1 did not say to reword it once the rule landed.
- Smallest fix: change the sentence to "Several matching rows follow the several-rows rule below." (or delete it, since the new text starts "Several scoped Dispatch rows can match one tab-map entry by path B"). Does not block.

### F2 (MINOR) Serial comma in a list, against the surrounding 7.2 style

- Evidence: `docs/designs/orchestrator-mode.md:498`, "(a reused pane, a retry, or two rows on one terminal handle)". Neighbouring lists in 7.2 have no serial comma: line 511 "the root, a scanned project-key folder or the `orca-tabs/` folder"; line 498 earlier part "`/clear`, a resume or a person running the command again".
- Smallest fix: "(a reused pane, a retry or two rows on one terminal handle)".

### F3 (MINOR) D9 Source cell does not cite the review that added the R3-B2 wording

- Evidence: `docs/designs/orchestrator-mode.md:819`, Source cell is "Review 1 B2; review 2 R2-B1 and R2-B2". The Design cell of the same row now carries the several-rows clause (R3-B2) and, from the earlier batch, the time-window clause (R3-B1).
- What is wrong: the Source column lists where each deviation clause came from, and the row's own text ends "Pinned by the D9 join fixtures", but review 3 items are absent. Cell count is correct (6 pipes, 5 cells), so the form holds; only the provenance is stale. research/04 edit 4 did not ask for it, so this is not a deviation from the plan.
- Smallest fix: "Review 1 B2; review 2 R2-B1 and R2-B2; review 3 R3-B1 and R3-B2".

### F4 (MINOR) FR-010 test column names fixtures for R3-B1 but not for R3-B2

- Evidence: `docs/designs/orchestrator-mode.md:768`. The test column reads "`sweep/test_classify.py` (the D9 join fixtures and the SPEC line 236 fixture), `sweep/test_probes_allowlist.py` (the six reader and parser fixtures of the path-B time fields), ...". The design column gained the several-rows clause (R3-B2), the test column did not gain a matching phrase.
- Smallest fix: after "the SPEC line 236 fixture" add ", the seven several-rows fixtures". research/04 edit 3 limits itself to the design column, so this is optional.

### F5 (MINOR) Mechanical report evidence is weaker than its PASS lines say

- Evidence: `r3-b2-mechanical.md:59-64` (Command 2 output is cut to 60 characters per hit, so it never shows the literals it greps for), `:80-84` (Command 5 prints "(no output expected ...)" and not a captured result). I re-ran the equivalent greps myself and the conclusions hold (0 em dashes, 0 `TODO` or `TBD`, literals at 498, 743, 1026).
- Smallest fix: re-run the gate with untruncated output and a printed `exit=1` line for Command 5. Does not change any verdict.

### F6 (MINOR, outside this lens, for the qualitative reviewers)

- `docs/designs/orchestrator-mode.md:498`: the incomplete-tail sentence (window observable, `tail_complete` False gives `session start not observable: transcript tail only`) and the new several-rows rule (which counts "windows that hold" the transcript) do not say which note wins when two matching rows exist and the tail is incomplete. A fixture list for 743 has no such case. Not a form defect; flagged so the logic reviewers can grade it.
- `docs/designs/orchestrator-mode.md:9-11` still lists R3-B2 as an open blocking finding and `:743` still says "the four incomplete cases". Both belong to the status closure and to R3-B3, not to items 3.1 to 3.4.

## Form checks that found no break

- Section 11 table (lines 739-749): header, separator and all 9 rows have 4 unescaped pipes (3 cells). Row 743 grew by about 2,400 characters and kept 3 cells. No unescaped `|` inside the new fixture text.
- Section 12 table (lines 757-803): all 47 lines have 4 pipes. FR-010 row (768) still has 3 cells after the R3-B2 insertion.
- Section 18 table, Fix cycle 3 (lines 1023-1026): 4 pipes on header, separator, R3-B1 and R3-B2 rows. R3-B2 row text equals research/04 edit 5 word for word, no trailing period, matching the R3-B1 row and the cycle 2 rows.
- Sections 13 and 14: D9 table (809-819) all 6 pipes (5 cells); SP-29 row (857) 4 pipes (3 cells). Both carry the clause "and, when several rows match one pane session, exactly one window holding it" (research/04 edit 4 wording).
- 7.2 sentence style: new text uses the existing forms "is could not determine with note", "is None with note", "joins ... only", backticked note literals with a colon in the same form as `conflict: duplicate Dispatch rows disagree` (line 509), `row_id`, `orca_rows` and `terminal_handle` names that exist in the data model (lines 456, 460), and fixture parentheses in the colon-and-semicolon form the R3-B1 fixtures use. Replacements of research/04's "line 494/495/505" pointers with "the Duplicate Dispatch bullet of this section" and "the bullet that follows this one" follow the design's habit of not citing its own line numbers.
- Characters: `grep -c '—'` gives 0; en dash and horizontal-bar search gives no hit; ` - ` and ` -- ` appear only at lines 306, 455, 688 (outside every R3-B2 edit; 455 is `now - window`).
- `TODO`, `TBD`, `FIXME` (case-insensitive, whole word): no hit.
- Totals: `Total: 9 deviations.` at line 821 and `Total: 23 open items.` at line 997, seen in my reads; D9 not split or added.
- Fixture names: the seven R3-B2 names in line 743 match research/04 3.4 and research/09 Gap 4 exactly, in the same order; each of the three outcomes (one window holds, two or more hold, none holds) has a fixture and a 7.2 sentence.

## Checks

| ID | Check | Result |
|---|---|---|
| C1 | Section 11 table rows keep 3 cells (4 unescaped pipes), header and separator included | PASS |
| C2 | Section 12 table rows keep 3 cells, FR-010 row intact after insertion | PASS |
| C3 | Section 18 Fix cycle 3 table rows keep 3 cells; R3-B2 row matches research/04 edit 5 | PASS |
| C4 | Sections 13 (D9) and 14 (SP-29) rows keep their cell counts and carry the edit 4 wording | PASS |
| C5 | 7.2 worker bullet: sentence style matches surrounding text (verb forms, note literal form, no own-line-number citations) | PASS |
| C6 | 7.2 pointer sentence "Several matching rows follow the R3-B2 rule below." is consistent with surrounding ID style | FAIL (MINOR, F1) |
| C7 | List punctuation in new 7.2 text matches surrounding text | FAIL (MINOR, F2) |
| C8 | Em dash count 0, no en dash, no stray dash separators in edited lines | PASS |
| C9 | No `TODO`, `TBD` or `FIXME` anywhere in the design | PASS |
| C10 | Seven fixture names in section 11 equal research/04 3.4 and research/09 Gap 4 | PASS |
| C11 | Each of the three outcomes has one 7.2 sentence and at least one section 11 fixture | PASS |
| C12 | Note literals (`conflict: one pane session matches several Dispatch rows`, `pane moved to a later session`, `joined by pane: latest session of the pane`) are identical at every hit | PASS |
| C13 | Deviation total 9 and open-item total 23 unchanged | PASS |
| C14 | Provenance cells (D9 Source) reflect the reviews whose wording the row now carries | FAIL (MINOR, F3) |
| C15 | Traceability FR-010 test column names fixtures for the new rule | FAIL (MINOR, F4) |
| C16 | Producer mechanical report reproduces and its evidence is complete | PASS with note (MINOR, F5) |

## Summary

- Checks passed: 12 / 16 (the 4 failures are all MINOR; none breaks a table, introduces an em dash, `TODO` or `TBD`, or changes a row's cell count).
- BLOCKING findings: 0. MAJOR findings: 0. MINOR findings: 6 (F1 to F6), recorded as notes and not rechecked.
- Self-audit: tool calls that back the verdict are the table-pipe awk count over lines 449-517, 728-870 and 999-1026, the em dash, en dash, dash-separator and `TODO` greps, the note-literal and fixture-name greps, the review-ID grep, and the Reads listed above. Confidence: Verified 16/16 | Unverifiable 0 | Unchecked 0 | Confidence 100.0%. Tool engagement: Read 7 | Grep 8 | Glob 0 | Bash 1.

Verdict: PASS
Blocking count: 0
