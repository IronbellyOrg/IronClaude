# QA Report: 2.5-allocate-check cycle 2 (topic 2.5 allocation page, manifest v2)

**Object:** `qa/local-source-allocation.md` lines 72-99 (topic 2.5, 22 slices) plus shared sections (lines 1-28, 101-103)
**Date:** 2026-11-13
**Phase:** allocation check, report-only, fix_authorization false, Tier1b. Review 2 of 3 (final permitted round for this gate per the dispatch brief).
**Fix cycle:** 1 (v1 -> v2)

---

## Overall Verdict

VERDICT: FAIL

Cycle-1 B1 (context budget) is corrected. Cycle-1 B2 (per-slice aspects, caller discovery) is only partly corrected, and v2 adds two new blocking defects (boundary claims that are false, caller search that skips tests).

## Input measurement
Read: brief 17 lines; TASK 140-161 (22); TASK line 196 (one long line); allocation file lines 1-40 and 72-108; check-1.md 45; input-bindings.md 32. Metadata only: `git rev-parse` (HEAD 933cf3a4f, unchanged), `wc -l` of the 8 topic-2.5 files, one `grep -rl` for `wire_ccsession|install_ccsession`, one-line `sed -n Np` looks at each cut line. No full source reads. About 240 lines, under 1000.

## Items Reviewed
| # | Check | Result | Evidence |
|---|-------|--------|----------|
| a | Cycle-1 findings corrected | PARTIAL | B1 fixed (slice-0 holds all 591 scope/notes lines; others carry a 40-line caller table). B2 caller part: slice-0 assigned, but see F2. B2 aspect part: not fixed, see F3. N1 (bisected tests): not fixed, see F1. N2 (7 workers) gone. N3 (failed drafts) gone. N4 (template) now charged in fixed context. |
| b | Complete line coverage, boundaries at def/test edges | FAIL (F1) | Counts match `wc -l`: F14 3399, F15 4823, F16 323, F17 1106, F18 409, F12 133, F11 172, F13 569. Unions have no gap or overlap: F14 1-560..3051-3399, F15 nine ranges to 4823, F16 1-160/161-323, F17 1-560/561-1106, F13 1-303/304-569. Edges are NOT at test boundaries (F1). |
| c | Producer-spec obligations mapped to a named slice aspect | FAIL (F2, F3) | See findings. |
| d | Charged total at most 1000, arithmetic shown | PASS (note N2) | Rechecked every line: 560+40+344=944; 600+40+344=984; 526+384=910; 571+384=955; 295+384=679; 498+384=882; 349+384=733; F15 540+384=924, 463+384=847; F17 560+384=944, 546+384=930; slice-10 460+163+20+344=987; slice-19 409+160+20+344=933; slice-20 608+40+344=992; slice-21 266+40+344=650. All at most 1000. Slice-0 stated 915; true charge at the 344 baseline is 591+344=935, plus up to 30 lines of search output, 965. Still at most 1000. |
| e | Unique output paths | PASS | `slice-{1..21}.md` plus `slice-0-context-callers.md`; no two share a path. Final `research/05-test-contracts.md` distinct. |
| f | Check-before-source ordering | PASS with note N3 | TASK regions still place allocation checks before source slices. v2 dropped the explicit sentence; the TASK structure still enforces it. Slice-0 to slices 1-21 order is not declared (N3). |
| g | Counterpart/shared-edge declarations with exclusion evidence | FAIL (F1, F2) | Line 103 declares edges for topics 2.1-2.4 only; 2.5 declares none, and no exclusion evidence for any cut. |

## Findings
### F1 (BLOCKING): v2 claims boundaries at whole-test/helper edges; most are mid-test, with no overlap or edge declared
Line 99 says "boundaries at whole-test/helper edges" and line 80/81 say slice-4 ends at "test ending 2257" and slice-5 ends at "test 2538-2552 WHOLE". Checked each cut line. F14: 560/561 inside a parametrize list (`("1b", 850000),` / `("2", 500000),`); 1160/1161 inside the injected-clock test (1151-1174); 2257/2258 inside a call (`cwd=d,` / `env=env,`), so "test ending 2257" is false; 3050/3051 splits `def test_older_ccsession_ignores_the_rules_line` from its docstring. F14 1686/1687 and 2552/2553 are true edges. F15: 560/561 (`with socket.socket()` / `probe.bind`), 1100/1101, 1560/1561 (assert pair), 2120/2121, 3240/3241 (signature tail / comment), 3800/3801, 4360/4361 all fall inside tests. F16 160/161 and F13 303/304 are edges; F17 560/561 is between tests. Cycle-1 N1 asked for cuts snapped to test boundaries or a declared overlap. v2 did neither, and states the opposite. Procedure (TASK line 152) requires "boundary overlap and cross-slice entry/exit ... edges". A test's tail goes to a worker that never saw its setup, and no edge register exists. This is a false claim plus a missing required declaration, so it blocks.
Required correction: snap every cut to a test/def boundary (each slice has 16-424 spare lines at the charged totals, so most snap within budget; recompute totals), or declare an overlap and edge for each mid-test cut, and correct the false statements on lines 80, 81, 99.

### F2 (BLOCKING): caller discovery scope omits tests and leaves a known caller unassigned
Slice-0 greps `wire_ccsession|install_ccsession` "across src/". A bounded grep over `src tests` also lists `tests/cli/test_install_retired_mcp.py` (776 lines; line 519 patches `superclaude.cli.install_ccsession.wire_ccsession`). That file is in no slice and slice-0's grep would not surface it. Producer spec (TASK line 232): "discovered actual callers without execution", "all shared callers covered or bounded with negative evidence". Topic 2.5 is tests/packaging/callers, so the search must cover tests, and a found file needs a slice or explicit bounded exclusion with evidence (TASK line 152: new callers trigger a new allocation and check before reading). Slice-0 also has about 30 lines of headroom, which cannot hold a 776-line file.
Required correction: widen slice-0's search to `src tests`, name the caller set found (at least this file), and assign it a slice (new allocation, re-checked) or an evidenced bounded exclusion.

### F3 (BLOCKING): per-slice aspects are still not named for 2.5
Cycle-1 B2 required a per-slice aspect statement. v2 line 99 says only "the brief carries the aspect (which test families the range holds ...)"; line 103 says each obligation maps to a slice aspect "inline above", but the 2.5 section carries none. Topic 2.1 does name aspects (lines 34-38). For 2.5, obligations (explicit model/tier, inherited/role/default, non-tier/profile, effort/settings, context/windows/compaction, permissions, stream/tools/history, fallback, installation/package) are not mapped to any slice or range. Check (c) cannot be confirmed. Related: slices 1-21 take their scope context only through slice-0's output (a pending, unaccepted producer; TASK line 142: pending rows cannot authorize consumption), and the producer spec says "Read all four `research/scope-*.md` inputs". The page must state that slice-0 is produced, coverage-checked and accepted before slices 1-21 start, or give them their own pinned scope rows.
Required correction: add a per-slice aspect/obligation map for slices 1-21, and state the slice-0 acceptance-before-dispatch order and its binding rows.

### Minor notes (do not fail the review)
- N1 (Medium, follow-up candidate): TASK line 196 still describes 14 slices, 850-line cuts and outputs `slice-1..14.md`; it no longer matches the v2 page (22 slices, `slice-{0..21}`). The coordinator should rewrite that item text when it emits concrete items. User's call whether to open an issue; none opened.
- N2: slice-0's "100 + 224" does not sum from the listed baseline terms (22+70+180+32 = 304); the correct charge is about 935-965. Still within budget.
- N3: line 99's F15 sum lists ten terms (evaluates to 5383) for nine ranges; the ranges themselves sum to 4823.
- N4: slice-0's output name differs in pattern from the header's `slice-{0..21}.md`; harmless but unify.

## Self-Audit
Tried to disprove FAIL. (1) Maybe the boundary claim is loose wording: no, line 99 asserts edges and several cited edges (2257, 3050) are demonstrably mid-statement; cycle-1 N1 was left unfixed and the procedure requires edge handling. (2) Maybe test_install_retired_mcp.py is out of topic: it is a test of the packaging caller `wire_ccsession`, squarely tests/packaging/callers, and it is not a counterpart read anywhere. (3) Maybe the brief carries aspects, so F3 is moot: a brief written at dispatch time is exactly what an allocation check must verify beforehand; 2.1 shows the manifest form. Checked and held: all `wc -l` counts, HEAD unchanged, every slice sum in check d, range unions, path uniqueness. Not checked: source or test content (no source reads per brief), whether the retired-mcp file also references the other symbol beyond line 519, and the full slice-0 grep result beyond the file list.
