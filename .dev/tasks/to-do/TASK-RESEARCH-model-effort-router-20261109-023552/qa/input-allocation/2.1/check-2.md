# QA Report: 2.1 allocation page check (check-2)

Status: Complete
Date: 2026-11-13
Verifier: rf-qa, adversarial, report-only, Tier1b, fix_authorization false (run run_c974cafd0eb6)
Object under check: `qa/local-source-allocation.md` v2 (107 lines), topic 2.1 section (lines 30-40) plus shared lines 5-28, 101-107

## Inputs read
Revision: worktree HEAD 933cf3a4f. TASK lines 140-161 read in full; manifest v2 read whole (107 lines); check-1.md (81 lines) read whole; input-bindings.md (32) read whole; item-2.1 PRODUCER-ONLY passage (TASK line 224, bounded excerpt) read for the obligation list. Metadata only on F01: wc -l (1975), function-definition greps, exec-site grep, brace/esac greps, one-line sed peeks at 116/137/141/881/1298/1833 and 556-562, 1294-1298. No full source reads. No prior check-2.md existed (stub created by me).

## Check (a): cycle-1 blocking findings corrected in v2
- B3 (setup_shim ownership, session_place straddle, selection-state edge): CORRECTED. setup_shim 962-1155 wholly in slice-2 (def edge 1155 `}` confirmed); session_place 1358-1406 declared as shared edge (1358-1400 slice-3, 1401-1406 slice-4); selection-state edge declared.
- B1 (obligations without an aspect): PARTLY corrected. Obligation map (line 40) exists, but three entries are wrong (see B3 below).
- B2 (parser in wrong slice): PARTLY corrected. Option loop 730-821 now in slice-2 (correct), but the pre-parse `case` is assigned to the wrong slice (see B2 below).
Result: FAIL (two of three cycle-1 blockers only half-fixed).

## Check (b): range coverage
F01 ranges 1-560, 561-1155, 1156-1400, 1401-1975 = 560+595+245+575 = 1975. Contiguous, no gap, no overlap. F02 249, F03 47, F04 217 whole in slice-5 (wc matches v1 measurements). Union complete: PASS.
Boundary quality: 1155/1156 is a def edge (setup_shim `}` 1155, apply_profile 1157). 560/561 falls inside the comment block (557-565) that introduces `orca_tab_file` 566: not mid-function, but not a def edge (minor M1). 1400/1401 cuts `session_place` mid-body; declared, but the next def edge 1406/1407 would avoid it at no cost (minor M2).

## Check (c): producer-spec obligation map (verified against F01 line positions)
| Obligation | v2 owner | Measured location | Result |
|---|---|---|---|
| parser option loop | slice-2 | 730-821 (done 821) | ok |
| pre-parse `case` | slice-1 "at the range's tail" | `case` at 684, inside slice-2 (561-1155) | WRONG (B2) |
| apply_profile / apply_tier_selection / export_selection | slice-3 | 1157-1189 / 1191-1233 / 1235-1281 | ok |
| setup_shim | slice-2 | 962-1155 | ok |
| six exec sites | slice-4 | 1904, 1906, 1964, 1966, 1971, 1973 | ok |
| passthrough `--claude-args` | slice-2 | 749 | ok |
| duplicate model/settings options | slice-2 (+4 exec lines) | 798, 849/1175/1226, 1150/1259 | ok |
| permissions | "slices 2/4", marker "881" | defaults 137-141 are in slice-1; 881 is a private-profile comment, not permissions | WRONG (B3) |
| private-profile | slices 1/2/4 | 116, 881, 1833 | ok |
| resume | slice-4 "1298(comment)/1964-1966" | 1298 is in 1156-1400 (slice-3); only 1964/1966 are slice-4 | WRONG (B3) |
| immediate callers | "slices 3/4" | the caller of ccsession is ccsession-orca line 54 (F02), slice-5; slices 3/4 hold no caller code | WRONG (B3) |
| session-only vs per-request policy, negative searches | not named | spec text, not a range | minor (M4) |

## Check (d): charged totals (arithmetic re-derived)
Manifest line 28: baseline fixed 424 = procedure 22 + brief 70 + prompt 180 + role 80 + bindings 32 + template 40. Stated trim: "role/template to a jointly-measured 100-line quoted excerpt" gives fixed 344.
Re-derivation: 22+70+180+32 = 304; plus a 100-line role/template excerpt = 404, NOT 344. 344 is reached only by deleting the role entirely (424-80) while still describing a 100-line excerpt. Charged totals:
| Slice | Manifest | At 404 | At 424 |
|---|---|---|---|
| 1: 560+40+fixed | 944 | 1004 | 1024 |
| 2: 595+40+fixed | 979 | 1039 | 1059 |
| 3: 245+40+fixed | 629 | 689 | 709 |
| 4: 575+40+fixed | 959 | 1019 | 1039 |
| 5: 249+47+217+30+fixed | 887 | 947 | 967 |
Slices 1, 2 and 4 exceed 1000 under the manifest's own stated trim rule. Line 28's "at most 576 source/context lines" is also violated by its own rows (600, 635, 615). Also, brief 70, prompt 180, role 80 and template 40 are estimates (marked "~" or "≤"), while the procedure requires measured counts. FAIL (B1).

## Check (e): output paths
Directory `research/source-slices/2.1/`, files `slice-{1..5}.md`, five distinct names; consumer IDs `2.1-source-1..5` (line 107). PASS.

## Check (f): check-before-source ordering
2.1-allocate-check is TASK line 188; source-slice region and producer items come after (line 202-203 empty region, producers from 224); registration says acceptance only on independent PASS. Source slices stay unstarted until this report passes. PASS.

## Check (g): counterpart/shared-edge declarations
Present for setup_shim (slice-2 whole), session_place (3/4), selection state (2/3), exec sites (4 consumes 3 state), F02 wrapper cross-cite (slice-5). No foreign-file reads in 2.1; exclusions are none. Declarations exist, but the slice-1/slice-2 entry edge is declared in the wrong direction (B2). PASS except as noted in B2.

## Findings
### Blocking
- **B1 (CRITICAL): the 344-line fixed context is not supported by the manifest's own rule.** A 100-line role/template excerpt gives 404; slices 1, 2 and 4 then total 1004, 1039 and 1019 (over 1000). Estimates replace required measurements. Required fix: measure the real brief, prompt, role and template spans, recompute every slice total, and re-split slices 1, 2 and 4 so each is at most 1000.
- **B2 (CRITICAL): pre-parse `case` 684-727 has no owner.** Slice-1 (1-560) is told the case "lies at the range's tail" and slice-2 is told to treat it as slice-1's ENTRY EDGE, but it sits at 684-727 inside slice-2's range. The parser's dispatch is the first half of the parser obligation (cycle-1 B2). Required fix: assign 684-727 to slice-2's aspect and drop the claim from slice-1.
- **B3 (CRITICAL): three obligation map entries name the wrong slice.** (i) permissions: defaults 137-141 (slice-1) unmapped, and 881 is mislabelled as a permissions marker; (ii) resume: line 1298 is slice-3's, not slice-4's; (iii) immediate callers: the caller is `ccsession-orca` line 54 (slice-5), not slices 3/4. Required fix: correct the three owners.

### Minor / Medium
- M1: boundary 560/561 splits a comment block, not a def edge.
- M2: 1400/1401 cuts `session_place` mid-body; moving it to 1406/1407 is free.
- M3 (Medium, follow-up): slice-2 holds unnamed helper functions (orca_tab_* 566-634, auto_name 635, 822-921) that no aspect lists; slice-3 holds session_home/session_branch/load_worktrees unnamed.
- M4: policy questions (session-only vs per-request, negative searches) have no named aspect owner; they are cross-slice synthesis.
- M5: cycle-1 M4 resolved (this stub was created by me; no collision).

## Self-Audit
Attempted disproof of FAIL: (1) Maybe 344 is intentional because the full role file is not charged? Line 28 says the trim is a "100-line quoted excerpt"; 22+70+180+32+100 = 404; even 344+60 contradicts the stated 576 cap. I cannot find a derivation of 344 other than dropping the role, which line 28 does not say. (2) Maybe the case 684-727 is meant as slice-2's entry? The text says "at the range's tail" of slice-1 and slice-2 says "ENTRY EDGE: pre-parse case from slice-1": both say slice-1 owns it, and slice-1's range ends at 560 (grep `case` at 684). (3) Is 1298 in slice-4? 1298 < 1401. (4) Is the caller in slices 3/4? grep: ccsession-orca:54 sets CCSESSION; F01 functions 1156-1975 do not call F02.
Confirmed correct: line counts, F01 contiguous coverage, setup_shim/apply_*/export_selection def edges, six exec sites in slice-4, option loop in slice-2, session_place declared, output paths unique, ordering.
Not checked: 2.2-2.5 pages, scope-file contents, whether prompt text is really ~180 lines.

Blocking count: 3. Minor/Medium: 5. No edits made outside this report.

VERDICT: FAIL
