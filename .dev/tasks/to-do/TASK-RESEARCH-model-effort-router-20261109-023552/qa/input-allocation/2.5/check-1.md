# QA Report: 2.5-allocate-check (topic 2.5 allocation page)

**Object:** `qa/local-source-allocation.md` lines 89-109 (topic 2.5, 14 slices)
**Date:** 2026-11-13
**Phase:** allocation check (report-only, fix_authorization false, Tier1b)
**Fix cycle:** N/A (review 1)

---

## Overall Verdict

VERDICT: FAIL

Two blocking findings (B1 context budget, B2 caller/aspect assignment). Range coverage, ordering and output paths are sound.

## Input measurement
Read: dispatch brief 19 lines; TASK passage lines 140-161 (22); allocation file topic-2.5 section and shared-context section (each Read under 100 lines); input-bindings.md 32; item 2.5 producer spec (TASK line 232, one physical line of about 9,000 characters; the brief's "line 221" is stale because the TASK file now has 705 lines, and the PRODUCER-ONLY marker for 2.5 is at line 232); the item's own check text (TASK line 196). Metadata only: `wc -l` of the eight topic-2.5 files, scope-01..04 and research-notes; `awk` lookups of the enclosing `def` at each cut line. No full source reads. Total about 330 lines, under 1000.

## Items Reviewed (checks a-f)
| # | Check | Result | Evidence |
|---|-------|--------|----------|
| a | Complete coverage, no gaps or overlaps | PASS (note N1) | `wc -l` at HEAD 933cf3a4f matches every count: F14 3399, F15 4823, F16 323, F17 1106, F18 409, F12 133, F11 172, F13 569. Unions: F14 1-850, 851-1700, 1701-2550, 2551-3399; F15 1-850, 851-1700, 1701-2550, 2551-3400, 3401-4250, 4251-4823; F17 1-560, 561-1106; F18 1-200, 201-409; F13 1-280, 281-569; F16, F12, F11 whole. Zero gaps, zero overlaps. `git status` clean for src/tests; HEAD unchanged. |
| b | Counterpart reads labeled | PASS | Inside 2.5 every file is owned (full-coverage duty), so none is a counterpart. Other topics label their F14/F15 reads counterpart and leave full coverage with 2.5 (allocation lines 76, 87). |
| c | Producer-spec keywords map to a slice aspect | FAIL (B2) | The 2.5 section assigns ranges only; no aspect text per slice, unlike 2.1 (line 48). "Discovered actual callers" appears in the Files line (91) but no slice, range or budget exists for it. |
| d | Lifetime total at most 1000 | FAIL (B1) | Stated totals (927, 973, 837, 832, 662, 478) are right for their listed terms but omit mandatory context. |
| e | Unique output paths | PASS | TASK line 196 fixes `research/source-slices/2.5/slice-1..14.md`, one per slice; final output `research/05-test-contracts.md` is distinct. |
| f | Producer before consumer | PASS | Allocation-check region (TASK 186-198) precedes the `local-source-slices` region (202-203); allocation line 113 and item 196 both say checks run before source dispatch. |

## Findings
### B1 (BLOCKING): mandatory scope and notes context is not charged to slices 1-13
The producer spec (TASK line 232) says "Read all four `research/scope-*.md` inputs and `research/research-notes.md`", and allocation line 91 lists them as 2.5 context. Measured: scope-01 138 + scope-02 142 + scope-03 92 + scope-04 107 + research-notes 112 = 591 lines. Slices 1-9 are stated as 850 + 22 + 55 = 927, leaving 73 lines; scope-04 alone (107) already overflows them (1034), and the full set gives 1518. Slice 10 (973) leaves 27. Slices 11-12 (837, 832) fit one scope file but not 591. Slice 13 (662) leaves 338, short of 591. Slice 14 charges research-notes (112) but gives no line count for its "scope files digest rows". Sibling topics charge scope files as separate terms (2.1 line 44: scope-01 138; 2.2 line 60: scope-04 107), and the shared-context section (line 34) promises "a pinned range of its scope files", yet 2.5 gives no pinned range. The 55-line brief cannot hold 591 lines. Procedure (TASK line 148): "Reserve actual mandatory context first, then allocate remaining capacity to source"; missing measurements invalidate admission.
Required correction: re-partition F14/F15 so source + 22 + brief + the actual scope/notes context (pinned ranges with line counts, and the governing-template Read) is at most 1000 for every slice, then re-check.

### B2 (BLOCKING): caller discovery and per-slice aspects are not assigned
The producer spec requires "discovered actual callers without execution" and "all shared callers are covered or bounded with negative evidence". Allocation line 91 names "+ discovered actual callers" but assigns no slice, search scope or line budget. Slices 1-9 have 73 spare lines, so callers cannot be found inside them. No slice states its aspect (explicit model/tier, inherited/role/default, non-tier/profile, effort/settings, context/windows/compaction, permissions, stream/tools/history, fallback, installation/package). If every slice applies the whole prompt to its range, the page must say so; if aspects are split, they must be mapped. Check (c) cannot be confirmed as written. Procedure (TASK line 152): new callers trigger new bounded allocation and checks before reading.
Required correction: add a counted caller-discovery assignment and a per-slice aspect statement.

### Minor notes (do not fail the review)
- N1 (Medium, follow-up candidate): cuts bisect tests with no declared overlap or boundary-question register. F14 at 850 (test 845-864), 1700 (helper `_real_launch` 1687-1733), 2550 (test 2538-2552); F15 at 850 (848-881), 2550 (2526-2551), 3400 (3389-3413), 4250 (4217-4257); F18 at 200 (194-222); F13 at 280 (inside `install`, 46-303). A tail in the next slice could go unread by the head's owner. Snap cuts to test boundaries or add a few overlap lines within the corrected budget. Whether to open an issue is the user's call; none opened.
- N2: allocation line 93 says "across 7 workers" but 14 slices follow.
- N3: line 105 keeps failed-arithmetic drafts (1046, 969) before the final split; final 11/12 numbers (837, 832) are correct.
- N4: the governing-template Read for the output skeleton is not charged in any slice; include it in the B1 correction.

## Self-Audit
Attempted to disprove FAIL. (1) Maybe the 55-line brief includes scope context: disproved, because 2.1 line 44 and 2.2 line 60 charge scope files separately from the brief, and 55 lines cannot hold 591. (2) Maybe slices need only digest rows: the page gives no digest line counts for slices 1-13, slice 14's are uncounted, and the producer spec says Read all four scope inputs. Checked and held: all `wc -l` counts, range unions, no gap or overlap, output-path uniqueness (TASK 196), ordering (TASK 186-203), stale line-221 reference (actual 232), HEAD and git cleanliness. Not checked: any test or source content (no source reads, per brief), and whether per-slice emitted items will repair B1 (they do not exist yet).
