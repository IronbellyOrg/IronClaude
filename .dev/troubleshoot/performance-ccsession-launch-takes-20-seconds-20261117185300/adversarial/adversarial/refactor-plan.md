# Refactoring Plan

## Overview
- Base variant: Variant 3 (staged: bash quick win first, then the python3 helper), file `variant-3-original.md` in this folder
- Incorporated variants: Variant 1 (2 changes), Variant 2 (3 changes); debate results and base-selection gaps (4 changes)
- Total planned changes: 9
- Overall risk: Low (all changes add text or tighten wording; no change alters the staged design)

## Planned Changes

### Change #1: name the helper and its place
- Source: Variant 1, section "Proposed change" and "Risks"
- Target: base section "Proposed change", Stage 2
- Integration approach: replace "a python3 helper" with "`scan_sessions.py` beside `retention.py` in `src/superclaude/skills/ccsession-tag/` (precedent: `ccsession:1674-1675` calls a python3 helper in `$CCSESSION_DIR`; install route: `install.sh:40` and `src/superclaude/cli/install_skill.py:52` copy the whole skill folder, so no manifest edit)"
- Rationale: debate point C-009 (Variant 1 judged better by its advocate; nobody disputed it); install route read by the root-cause-analyst worker
- Risk level: Low (additive)

### Change #2: one-record-per-line pairing as a stated risk and test
- Source: Variant 1 (U-004), "Risks"
- Target: base sections "Risks" and "Test plan"
- Integration approach: append to Risks "the helper's one-record-per-input-uuid pairing breaks if an input line is missing or odd (file names with spaces; labels reject control characters, `validate_label` at `ccsession:315`)" and a fixture "topic names with spaces and with `%2F` escapes, one topic file whose uuid has no transcript"
- Rationale: debate point U-004; E4 criterion scored MET for both helper variants
- Risk level: Low (additive)

### Change #3: invalid-UTF-8 output nuance of the locale fix
- Source: Variant 2 (C-005, all three advocates judged Variant 2 the winner)
- Target: base sections "Risks" and "Test plan"
- Integration approach: append to Risks "the C locale restores the intended byte-wise match: a UTF-8 grep may drop working folders with invalid UTF-8 bytes, a C-locale grep keeps them (worker knowledge of GNU grep, unverified); pin it with a fixture whose cwd holds invalid UTF-8 bytes"
- Rationale: unanimous debate result C-005
- Risk level: Low (additive)

### Change #4: optional skip of work for rows that are later discarded
- Source: Variant 2 (U-003)
- Target: base section "Proposed change", Stage 1 (as an optional last item)
- Integration approach: append "Optional, measure first: rows classified `other` are built and discarded after get_btime, get_mtime and format_epoch ran (ccsession:1610-1627, 1636); classifying first would skip that work (about 0.9 s on assumptions about the count of `other` rows, not derived exactly); keep only if the trace shows it and the output stays byte-identical"
- Rationale: debate unique contribution U-003 (Medium)
- Risk level: Medium (reorders computation, must keep output identical)

### Change #5: state the file count of each stage
- Source: Variant 2 (C-011, unanimous winner)
- Target: base section "Proposed change"
- Integration approach: add "Stage 1 touches 2 files (`ccsession`, `tests/unit/test_ccsession_tag.py`) and can ship as its own change; Stage 2 touches 3 to 4 (`ccsession`, `scan_sessions.py`, the test file, README only if it should mention the helper)"
- Rationale: unanimous debate result C-011; the user's rules require a written plan for more than one source file
- Risk level: Low (additive)

### Change #6: add the open assumptions with measurement gates
- Source: debate (A-001, A-002, A-004, A-006, left open or QUALIFY by every advocate)
- Target: new base section "Open assumptions and measurement gates" after "Risks"
- Integration approach: four rows. A-001: the reporter's locale and store size are unverified; capture `locale` and the number of topic files from the reporter, or reproduce with `LANG=en_US.UTF-8`. A-002: every timing and the 0.75 s prototype ran warm; measure the stage 2 helper once on a cold page cache before claiming its saving. A-004: the 1.53 ms and 1.2 ms per-spawn proxies for `dirname`, `basename` and `head` are not measurements; measure them (200 iterations) before relying on the 2.8 s saving. A-006: `session_place` (1.95 s) and the held-back output (nothing prints until the whole list is built, `ccsession:1718`) are left as they are; printing rows as they are built changes the `show_saved` contract and is a separate follow-up
- Rationale: the debate recorded no ACCEPT for these four UNSTATED assumptions
- Risk level: Low (additive)

### Change #7: repair the base's scored weaknesses
- Source: base-selection.md (criteria L4, R1, R2, C5 scored NOT MET for Variant 3)
- Target: base sections "Problem statement", "Risks", new "Out of scope"
- Integration approach: (a) define on first use: `I:<n>` = line n of `/home/coder/.claude/skills/ccsession-tag/ccsession` (the installed copy, byte-identical to origin/master 10f6ec670); "Task 1 trace" = the `bash -x` PS4 timestamp trace of `ccsession --here` in diagnosability-tasklist.md Task 1; "A-core"/"A-full" = helper does index and scan with bash keeping one `stat` and one `date -d` per timestamp, or helper does stat and date strings as well. (b) add a risk table (risk, probability, impact, mitigation) covering helper drift, locale output change, python3 missing, `date --version` probe on BSD, timing window on larger stores. (c) add "Out of scope": bounding the list to N rows, a cache file, printing rows as built, the hook that records the start folder, stage 3 unless the trace shows more than about 2 s in stat and date
- Rationale: scored criteria L4, R1, R2, C5 (NOT MET for Variant 3 in both passes or after re-evaluation)
- Risk level: Low (additive)

### Change #8: bring in the measured locale probe and relabel the derived estimates
- Source: debate point C-010 (unresolved), tier1-observation.md locale probe
- Target: base sections "Evidence" and "Success measure"
- Integration approach: add the measured end-to-end result (plain `ccsession --here` 23.586, 24.663, 22.471 s vs `LC_ALL=C` 16.657, 16.244, 16.597 s, median gap 6.99 s, alternated, load fell from 9.8 to 4.2) as the measured part of stage 1; keep the remaining-time estimates (variant 1 about 13.6 s, variant 2 11.6-14.1 s, base stage 1 about 14.6 s) labelled "derived, not executed, split unresolved in the debate (C-010)"; state the stage 1 target as "at or below the derived 14.6 s on the same store, to be confirmed by the same trace"
- Rationale: C-010 had no majority; measured numbers must lead
- Risk level: Low (modifies wording of existing evidence)

### Change #9: resolve the printf/date contradiction explicitly
- Source: debate X-001 and C-002 (Variant 3 won unanimously)
- Target: base section "Proposed change", Stage 1 date item
- Integration approach: add "`printf '%(...)T'` is not used: bash 3.2 (macOS) lacks it (ccsession:1690, 1823 state the bash 3.2 floor); the `date --version` probe on GNU and the BSD-first order elsewhere keep format_epoch's text and both platforms (ccsession:1533-1537)"
- Rationale: unanimous debate results X-001 and C-002
- Risk level: Low (additive)

## Changes NOT Being Made

| Diff point | Non-base approach | Why the base approach was judged better |
|---|---|---|
| S-001 | Variant 1: ship helper and fallback in one change-set | Debate: staging puts the measured locale win first and keeps a tested fallback (unanimous for Variant 3, 73%) |
| C-001 | Variant 2: no helper, keep the bash pipeline (6.46 s scan floor, Arm 2) | Variant 3 reaches the helper at stage 2; Variant 2 advocate conceded the gap |
| C-002, X-001 | Variant 2: guarded `printf '%(...)T'` for dates | Unanimous for the ban: a branch bash 3.2 never exercises on CI |
| C-003 | Variant 2: builtin glob plus `-nt` | `-nt` tie-break against `ls -t` is unverified (Variant 2's own risks); the base keeps the exact newest-copy rule |
| C-007 | Variant 1: leave dirname, basename and `head -n 1` per row | Base (and Variant 2) replace them; the saving rests on the unmeasured proxy, hence gate A-004 |
| C-004 | Variant 2: no fallback needed because no helper | Only relevant if no helper ships; the base ships one and tests the fallback |
| Not proposed by any variant | bound the list to the N newest rows; disk cache; parallel jobs | change the output contract or break "Listing never writes any file" (README:190); rejected in the system-architect and performance-engineer cards |

## Risk Summary

| Change | Risk | Impact | Rollback |
|---|---|---|---|
| #1, #2, #3, #5, #6, #7, #9 | Low | text added to the proposal | delete the added text |
| #4 | Medium | reordering could change output | do not adopt unless the output is byte-identical |
| #8 | Low | relabels evidence | restore the earlier wording |

## Review Status
Auto-approved (non-interactive run), 2026-11-17T19:16:48Z.
