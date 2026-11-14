# QA Report: R4 template-conformance lens

**Topic:** `docs/designs/orchestrator-mode.md` after R4 items 5.1 to 5.11 (1041 lines on disk today)
**Date:** 2026-11-09
**Phase:** fix-cycle gate R4, template-conformance domain lens (research/09 Gap 5)
**fix_authorization:** false. No file edited except this report.

Baseline used for "was it already like this": `.dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/artifacts/design-base.md` (1013 lines, read-only grep only).

## Method

- Read the DESIGN in 7 chunks of at most 150 lines (1-150, 150-300, 300-449, 449-598, 598-748, 748-895, 895-1041).
- Read research/07 (lines 1-173), research/08 (1-125), r4-mechanical.md (1-155), r4-wc14-hits.md (1-110) and r4-reanchor.md (1-129).
- Table cell counts came from an awk pass of my own (code fences skipped, `\|` removed, header column count compared to every row of the same table). I did not reuse the producer's counts.

## Checks

| ID | Check | Result |
|---|---|---|
| C1 | `## N.` headings run 1 to 18 in order, once each, no gap or repeat (grep of `^## ` outside fences; the repeated "Waiting" heading is inside the section 7.5 code fence, 603-635) | PASS |
| C2 | Subsection numbers: 2.1-2.3, 3.1-3.4, 7.1-7.6, 15.1-15.2, all in order | PASS |
| C3 | Section 9 table (709-718): header and all 8 rows (R1 to R8) have 4 cells | PASS |
| C4 | Section 12 table (770-816): header and all 45 rows have 3 cells | PASS |
| C5 | Section 15 tables: 15.1 capture table (897-911) 3 cells x 13 rows; 15.2 step table (921-957) 5 cells x 35 rows, including the new 1.16a row at 942 | PASS |
| C6 | Section 16 table (965-976): 2 cells x 10 rows, the edited WC-16 row at 970 included | PASS |
| C7 | Section 18 tables (1016, 1026, 1036): 3 cells in every row, including the R4 row at 1041 | PASS |
| C8 | Section 8 heading form: `## 8. WC-16 and the never-as-worker list` at 666 matches the `## N. Title` form; `### WC-16. Coordinator loop` at 675 sits inside the ```markdown fence 674-678 and carries the rule ident on the heading line; no real `### WC-14` heading remains | PASS |
| C9 | Em-dash and en-dash count is 0; no non-ASCII character anywhere (`grep -c '—'` = 0, `grep -c '–'` = 0, `grep -nP '[^\x00-\x7F]'` empty) | PASS |
| C10 | `TODO`, `TBD`, `FIXME` (word match and substring match) return nothing | PASS |
| C11 | Every other table in the file has a consistent cell count (22 tables checked) | FAIL (MINOR m1, already in `design-base.md:64`, not caused by R4) |
| C12 | Code fences balanced (28 fence lines) and no table runs into text outside a fence | PASS |
| C13 | Remaining `WC-14` hits are exactly 4: 668 (worker rule, keep), 829 and 852 (each followed by "(WC-16 in this design)"), 1041 (R4 row naming master). `WC-16` appears in sections 1, 8, 9, 10, 12, 13, 15, 16, 17, 18 | PASS |
| C14 | No stale pre-R4 anchor in the whole file: `after line 561`, `519-561`, `245-254`, `line 545/865/470/398/624`, `lines 156/158`, `WC-13 is at` all return nothing. `after line 565` appears at 28, 932, 968 | PASS |
| C15 | Totals still true: `Total: 9 deviations.` at 834 (table 822-832 has D1 to D9); `Total: 23 open items.` at 1010 (table 984-1008 has rows 1 to 23); section 8 "Pins (five edits)" lists exactly 5 bullets (684-688) | PASS |
| C16 | The four `RULE_PHRASES["WC-16"]` phrases each occur verbatim in the WC-16 text (677): `WC-16. Coordinator loop` (675), `On every coordinator wake`, `it is never posted`, `It never stops watching on its own`. The WC-16 text has no code span starting `make`, `uv`, `bash` or `python` (research/07 (e), `_check_repo_setup_gated`) | PASS |
| C17 | Every in-document `section N` or `section N.M` reference points at a section that exists; `section 5.1/5.2/5.3` at 110, 151, 561, 825, 860 are all prefixed "SPEC"; no `](#` anchor link exists to break | PASS |
| C18 | Revision-log ID form: rows use `B1`, `R2-B1`, `R3-B1` (cycle plus finding number); the R4 row (1041) is bare `R4` | FAIL (MINOR m2) |
| C19 | The R4 row's claims about where it edited match the file | FAIL (MINOR m3) |
| C20 | Producer evidence (`r4-mechanical.md`, `r4-wc14-hits.md`, `r4-reanchor.md`) agrees with the file on the points it states and that I re-ran: section map, WC-14 hit list, em-dash 0, TODO/TBD 0, totals, `after line 565` x2. Cited anchors re-read on disk: `WORKER-CONTRACT.md:110, 273, 275`; `test_worker_contract.py:89, 165, 173, 382, 391, 912, 1322`; `main.py:563, 565, 568` | PASS (one narrative slip, MINOR m5) |

## Findings

No BLOCKING and no MAJOR finding. I tried to prove the R4 edits broke section numbering, the cell counts in sections 9, 12, 15, 16 and 18, the section 8 heading form, the em-dash rule and the TODO/TBD rule. None of them broke.

### MINOR (never fail the gate)

**m1. Unescaped pipe in a code span gives the GQ-107 row 5 cells under a 4-cell header.**
- Evidence: `docs/designs/orchestrator-mode.md:64` (`` `sanitize()` escapes `|` as `\|` ``) in the table whose header is at line 55. My awk reports `MISMATCH table@55 hdr=4 line 64 cols=5`. The same row is at `artifacts/design-base.md:64`, so R4 did not introduce it.
- Why it matters: in GFM a bare `|` splits a cell even inside a code span, so the row renders with an extra cell and the Anchors text slides one column.
- Smallest fix: write the first code span as `` `\|` `` so the cell reads `escapes \| as \\|`, or reword to "escapes the pipe character as `\|`".

**m2. The R4 revision-log row breaks the ID convention and collides with routing row R4.**
- Evidence: `orchestrator-mode.md:1041` (`| R4 | DESIGN was written against base ...`) next to `R2-B1` (1028) and `R3-B1` (1038). Section 9 line 714 (`| R4 | tests/core/...`), 948 (`| 1.22 | | R4 |`) and 971 (`R1, R2, R3, R4, R5`) use R4 for a routing row. Section 8 line 672 uses "(R4)" twice to mean the revision, so a reader there can take it for routing row R4.
- Smallest fix: rename the revision-log ID to `R4-B1` (or `R4-reanchor`) and write "(R4-B1)" at line 672.

**m3. The R4 row says names were marked "in 13 and 14", but section 14 holds no WC-14 or WC-16 name.**
- Evidence: `orchestrator-mode.md:1041` ("marked the SPEC and REPORT draft names in 13 and 14"). `sed -n '854,880p' | grep -c 'WC-1[46]'` returns 0. The only marked names are at 829 (D6) and 852 (REPORT-differences row, still section 13).
- Smallest fix: change "in 13 and 14" to "in 13".

**m4. Duplicate sentence in section 7.6.**
- Evidence: `orchestrator-mode.md:655` says "No `## Unattended mode` section, no `--unattended` flag. `sweep.md` has no `## Unattended mode` section." (R4 added the second sentence for the master constraint; the first already says it.)
- Smallest fix: delete "`sweep.md` has no `## Unattended mode` section."

**m5. Producer narrative slip in the mechanical file.**
- Evidence: `r4-mechanical.md:147` (Check 4) says the cadence phrase is "in section 8 (2 lines) and in the WC-16 block (1)". The listing it prints (lines 99-103) shows 672 and 677 in section 8, and 677 is the WC-16 block, so the true split is 2 lines in section 8 (one of them the block), plus 712, 829 and 1041 elsewhere. The conclusion (phrase present) holds.
- Smallest fix: reword to "section 8 (672, 677; 677 is the WC-16 block), section 9 (712), D6 (829), R4 row (1041)".

**Observation, not R4 and not a finding:** section 1 lines 7-11 still call R3-B1 to R3-B3 "open" while section 18 "Fix cycle 3" records their changes. The same status text is in `design-base.md:7`, so it predates R4; the owner of the final status edit should reconcile it.

## Summary

- Checks passed: 17 / 20
- Checks failed: 3 (C11, C18, C19; all MINOR)
- BLOCKING: 0 | MAJOR: 0 | MINOR: 5
- Issues fixed in place: 0 (fix_authorization false)

**Confidence:** Verified: 20/20 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
**Tool engagement:** Read: 13 | Grep: 4 | Glob: 1 | Bash: 12 (read-only grep, sed -n, awk, wc, ls; no `orca`, no network, no Python)

Verdict: PASS
Blocking count: 0
