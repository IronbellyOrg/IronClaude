# QA Report: 2.2-allocate-check cycle 2 (topic 2.2 allocation page, manifest v2)

Status: Complete
Verifier: rf-qa, report-only, Tier1b. Run: run_c974cafd0eb6. Object: `qa/local-source-allocation.md` v2 lines 42-50 (topic 2.2) plus shared context lines 19-28 and 101-103. Revision: worktree HEAD 933cf3a4f. Procedure passage TASK 140-161 (22 lines) read. Producer spec for 2.2: TASK line 226. Bindings: `qa/input-bindings.md` (32) read. Cycle-1 report `check-1.md` (42) read.

VERDICT: FAIL

## Result
FAIL. 2 blocking, 5 minor. File-line coverage of F05/F06/F07/F09 is complete with def-edge cuts, and cycle-1 B2/B3 are fixed. But the F01 caller side is still incomplete: 7 `models.py` call sites in `ccsession` are in no 2.2 slice, and the one exclusion the page justifies (1161-1190) is justified falsely.

## Checks (a)-(g)

| Check | Result | Evidence |
|---|---|---|
| (a) cycle-1 findings corrected | FAIL | See regression table: B1 and B4 are not fully corrected. |
| (b) line coverage, boundaries | PASS for F05/F06/F07/F09/F08; FAIL for F01 | `wc -l`: models.py 1111, json 173, env 31, MODEL-TIERS 216, README 772, ccsession 1975. F05 1-526 + 527-747 + 748-1111 = 526+221+364 = 1111, no gap/overlap. Lines 525-526 blank, def `user_access` 527; 746-747 blank, def `_settings_key` 748: both cuts at def edges. F08 430-703 starts at heading `## Tiers (Coder workspaces)` 430; README tier/profile mentions are 23, 430-703 and 762 only (762 is a PATH sentence, 23 is a file-table row). F01 ranges 1079-1160, 1191-1300, 1750-1850: cuts at 1079 (inside `setup_shim` 962-1155), 1160 (inside `apply_profile` 1157-1190), 1300 (inside `workspace_name` 1283-1304) are not def edges; see B2. |
| (c) obligations to slices | FAIL (selection callers, cache/fingerprint callers, allowed-aliases caller) | Aspect lines now exist per slice (cycle-1 M2 fixed). Source-side obligations map: defaults parser 325/381 and registry 182-198 slice-1; identity/access slice-2; resolve/windows/compaction slice-2; fingerprint slice-3. Caller-side obligations do not: B1. |
| (d) budgets | PASS on numbers as stated; arithmetic note | Recomputed: slice-1 526+40+344=910; slice-2 221+173+31+30+344=799; slice-3 364+30+344=738; slice-4 82+110+101+40+344=677; slice-5 274+216+30+344=864. All match. All ≤1000 even at fixed 424 (990 / 879 / 818 / 757 / 944). Minor M1 on the 344 derivation and M2 on unpinned rows. |
| (e) unique outputs | PASS | Header names `research/source-slices/2.2/slice-{1..5}.md`; five unique paths. Directory exists and is empty. |
| (f) ordering | PASS | `qa/input-allocation/2.2/` holds only dispatch-check.md, check-1.md, dispatch-check-2.md and this report; `research/source-slices/2.2/` is empty; check item (TASK 190) precedes the producer barrier (TASK 226). |
| (g) counterpart/shared edges, exclusions | FAIL | Slice-4 F01 ranges are labelled COUNTERPART and the 2.2-slice-4 to 2.1 edge is declared (line 103). F08 owner named (slice-5). The only exclusion evidence given for F01 is for 1161-1190, and it is false (B2). No exclusion evidence is given for any other F01 gap (1-1078, 1301-1749 outside call sites) although call sites sit there (B1). |

## Cycle-1 regression table

| Cycle-1 finding | Status in v2 | Evidence |
|---|---|---|
| B1 F01 1-120 wrong, selection callers unassigned | NOT FIXED | 1-120 dropped (correct), but 700-1000, which cycle-1 reported as holding real selection code, was also dropped and replaced by call sites from 1079 on. Real call sites at 883, 895, 983, 994, 995, 1168, 1170 are unassigned. |
| B2 F08 1-120 wrong | FIXED | 430-703 plus F09 whole; F08 owner named. |
| B3 F05 cut mid `user_access` | FIXED | `user_access` 527-627 whole in slice-2. |
| B4 mandatory context omitted from budgets | PARTLY | Rows are now charged and every total is ≤1000, but the rows are named by count only (M2) and the "344" fixed context does not follow from its own components (M1). |
| M1 label F08 counterpart | FIXED | Slice-5 names F08 owner. |
| M2 outputs and aspects | FIXED | Outputs in header; aspect line per slice. |
| M3 unmeasured brief figure | NOT FIXED (minor) | Brief "≤70", prompt "~180", role "~80", template "~40" are all estimates. |

## Blocking findings

**B1. Seven `models.py` call sites in `ccsession` are assigned to no 2.2 slice, so the selection-callers obligation is incomplete.** `grep 'CCSESSION_MODELS' ccsession` gives these `python3 "$CCSESSION_MODELS" ...` calls: 883 `tier-mode` (sets `TIER_MODE=1` at 884, the entry of the default-channel decision), 895 `tiers` (builds the usable-tier list that gates the Opus alias, an allowed-aliases caller), 983 `shim-upstream-check`, 994 `settings-digest`, 995 `code-digest` (the cache/fingerprint callers), 1168 `resolve` and 1170 `profiles`. Slice-4 covers only 1079-1160, 1191-1300 and 1750-1850, so none of these is read. The producer spec (TASK 226) requires "selection callers" and tracing of allowed aliases and cache/fingerprint "cross-referenced to launcher/proxy owners". Assuming missing callers, the caller half of those three obligations is empty. Slice-4 has about 260 lines of headroom (737 at fixed 404), so adding 880-896, 980-996 and 1157-1190 (about 70 lines) fits.

**B2. The one exclusion the page justifies is false, and the slice-4 cut splits `apply_profile`.** The page says 1161-1190 is excluded because it is the "setup_shim tail owned by 2.1-slice-2". `setup_shim` is 962-1155 (the page's own line 11); 1157-1190 is `apply_profile` (def at 1157, `apply_tier_selection` starts 1191), and 1168/1170 inside it call `resolve` and `profiles`. 2.1-slice-2 ends at 1155; 2.1-slice-3 owns 1156-1400. The range 1079-1160 therefore ends 4 lines into `apply_profile` and drops the remaining 30 lines with no declared edge and a wrong justification. Per the procedure, exact selective exclusions need source-backed relevance justification, and cuts belong at def edges. Fix: extend the range to 1157-1190 (def edge at 1191), fix the evidence text.

## Minor notes
- M1. Fixed context "344" does not follow from its stated parts: 22 + 70 + 180 + 32 + 100-line excerpt = 404, not 344 (344 = 424 minus 80, which drops role and template entirely). Correct totals at 404: 970 / 859 / 798 / 737 / 924, still ≤1000 for topic 2.2. Outside this topic: 2.1-slice-2 is 595+40+404 = 1039 > 1000; the coordinator should recheck that page.
- M2. Context rows are named by count ("rows 40") with no path inclusive range or revision; the emitted item must pin them. No slice reads all four files that the copied prompt says to Read (scope-01, scope-02, scope-04, research-notes), so each emitted item must restate which pinned subset replaces that sentence.
- M3. Fixed-context components (70, 180, 80, 40) are estimates, not measurements (carried from cycle-1 M3). Slice-1 is at 990 under the 424 baseline, so measure it first.
- M4. Slice-4 start 1750 sits two lines before `show_help` (1753) in the tail of the previous function, and end 1300 is inside `workspace_name` (1283-1304); end at 1282 and start at 1753 instead.
- M5. TASK item 2.2-allocate-check (line 190) still describes the v1 plan (slices 1-3, F01 1-120 and 700-1000, F08 1-120); the manifest supersedes it, so the coordinator should record that. Also 2.1-slice-3 labels `export_selection` as 1157-1281 but 1157 is `apply_profile` and `export_selection` starts at 1235 (2.1 topic, not graded here).

## Confidence denominator
Checked 7 of 7 requested checks (a)-(g) and 6 of 6 cycle-1 blocking/minor items. Evidence: `wc -l` on 6 corpus files and 6 context files, def listing of models.py 440-830, def listing and boundary-line reads of `ccsession` at 1070-1320 and 1700-1900, a full `grep CCSESSION_MODELS ccsession` (21 hits), README heading and tier-mention listing, directory listings for ordering. Confidence in FAIL: high (B1 and B2 are direct observations of line numbers and text).

## Self-Audit
Attempted disproof of each blocking finding. B1: checked whether the seven call sites might fall inside a slice-4 range (883, 895 < 1079; 983, 994, 995 between 962 and 1078, below 1079; 1168 and 1170 fall in 1161-1190, excluded by the page); tried the argument that 2.1 owns F01 in full, but the producer spec requires selection callers for 2.2 and the page itself assigns F01 counterparts to slice-4, so unread call sites are a 2.2 gap; tried the argument that "tier call sites 1079/1132" stand for all callers, but those are `CC_CACHE_TIER_MODE` uses, not `models.py` invocations. B2: re-read lines 1157-1161 and the def listing to confirm 1157 is `apply_profile`, not the `setup_shim` tail. No disproof succeeded. Also tried to find fault with the passing parts: F05 cuts, F08 start edge, all five totals recomputed. Limit: I did not read the full source files, only metadata, def listings and targeted greps, as the brief required; I did not verify that 1-1078 or 1301-1749 contain no further callers beyond the grep hits, since the grep covers every `CCSESSION_MODELS` use. Report-only; no edits outside this file.
