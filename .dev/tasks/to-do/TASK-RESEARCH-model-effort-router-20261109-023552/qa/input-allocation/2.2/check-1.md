# QA Report: 2.2-allocate-check (topic 2.2 allocation page)

Status: Complete
Verifier: rf-qa, report-only, Tier1b. Run: run_c974cafd0eb6. Object: `qa/local-source-allocation.md` lines 54-64 (topic 2.2). Revision checked: worktree HEAD 933cf3a4f. Procedure passage: TASK lines 140-161 (22 lines) read. Item 2.2 allocation-check contract: TASK line 190. Producer spec for item 2.2: TASK line 226 (the dispatch brief said line 215; the file has shifted and line 215 is blank). Bindings: `qa/input-bindings.md` (32 lines) read.

VERDICT: FAIL

## Result
FAIL. 4 blocking, 3 minor. The file-line union for F05/F06/F07/F09 is complete, but the page has wrong relevance claims for the F01 and F08 counterpart ranges, leaves mandatory scope inputs unassigned, and splits a function mid-body without a declared edge.

## Checks (a)-(f)

| Check | Result | Evidence |
|---|---|---|
| (a) file coverage | PASS for F05, F06, F07, F09; FAIL for F01/F08 relevance | `wc -l`: models.py 1111, ccsession-models.json 173, env.example 31, MODEL-TIERS.md 216, README.md 772, ccsession 1975. F05 1-560 + 561-1111 = 1111, no gap, no overlap. F06/F07/F09 whole. F01 and F08 ranges are not whole-file and their justification fails (B1, B2). |
| (a) boundary edge | FAIL | F05 split at 560/561 falls inside `user_access` (def at 527, next def `tier_access` at 628; lines 556-566 are the body of its `raise ValueError(tenv[ACCESS_PROBLEM])` branch). No boundary note exists for 2.2 (2.1 has one). See B3. |
| (b) counterpart labels | PARTIAL | F01 ranges are called "counterpart read, charged and attributed" (OK). F08 1-120 is not labeled counterpart and F08 has no whole-file owner in topics 2.1-2.5. Minor M1. |
| (c) obligations to slices | PARTIAL | The 2.2 section declares no aspect per slice (2.1 does). By content: defaults parser (`defaults_path` 325, `read_defaults_file` 381) slice-1; identity/access (`owner_name` 504, `owner_roles` 514, `user_access` 527-627) split across slice-1 and slice-2; default-tier/model resolution (`resolve_tiers` 645, `_all_tiers` 655) slice-2; allowed aliases (`assign_aliases` 361 slice-1, `_my_models` 876 slice-2); windows/settings/compaction (`_window` 487 slice-1; `compact_settings` 681 and `model_window` 720 slice-2); registry schema (F06 slice-2, `load` 233 slice-1); cache/fingerprint (`settings_digest` 780, `code_digest` 785 slice-2); Coder template evidence (F07 slice-2, F09 slice-3). Mapped by inference only; "selection callers" are not covered (B1). |
| (d) budgets | FAIL | Stated totals 744 / 832 / 945 (slice-3 including F08 1-120) exclude mandatory context in the producer spec (line 226): "both launcher scope inputs" (scope-01 138 + scope-02 142), research-notes (112) and scope-04 (107), and exclude the 32-line `qa/input-bindings.md` read each emitted item repeats. Slice-3: 945 + 138 + 142 = 1225 > 1000. Slice-2 with scope-01/02/04 and research-notes: 832 + 499 = 1331 > 1000. Slice-1 with scope-01/02 and research-notes added: 744 + 392 = 1136 > 1000. See B4. |
| (e) outputs unique | PASS (minor) | The 2.2 section lists no per-slice output paths; the item 2.2 check text names `research/source-slices/2.2/slice-1..3.md`, which are unique, and the directory does not exist yet. Minor M2. |
| (f) ordering | PASS | `qa/input-allocation/2.2/` held only `dispatch-check.md` before this report; `research/source-slices/2.2/` does not exist; check item at TASK line 190 precedes producer barrier at line 226. |

## Blocking findings

**B1. F01 "parser entry 1-120" is wrong, and real selection callers are unassigned.** Over `ccsession` 1-120, 0 lines are non-comment, non-blank: the range is usage-comment text only (lines 20-25 and 88-89 mention profile/tier). Tier-mode call sites sit at 1079, 1132, 1254, 1755 and 1838 (all outside 700-1000), none assigned. The 700-1000 range does hold real selection code (matches 729-903, plus `setup_shim` at 962), so it is justified. The producer spec requires "selection callers"; under "assume missing callers", the caller side of default-tier resolution is incomplete and its stated justification for 1-120 is false.

**B2. F08 README "tier/profile docs" range 1-120 is wrong, so relevant documentation is unassigned.** Tier/profile mentions in README.md fall at line 23 inside 1-120; the rest are at 430-762 (for example 430-703). Lines 1-120 are title, package contents, install and gateway setup (headings at 1, 16, 34, 44, 72, 120). The spec requires "relevant documentation" with staleness cross-validation, and F08 has no topic-level owner for that range.

**B3. F05 cut at 560/561 splits `user_access` (527-627) with no declared counterpart edge.** Username/first-role/wildcard matching is this function's job and is cut across slice-1 and slice-2. The page declares no shared boundary and no instruction that each slice cross-reference the other half. The allocation procedure (boundary overlap and cross-slice entry/exit edges) needs either a declared edge or the cut moved to a function boundary (for example 627/628, before `tier_access`).

**B4. Mandatory context omitted from budgets.** Producer spec line 226 requires reading `research/scope-04-contracts-tests.md`, both launcher scope inputs and `research/research-notes.md`. The page assigns scope-04 to slice-1 only, research-notes to slice-3 only, and scope-01/scope-02 to no slice. Adding the required inputs breaks the 1000-line lifetime limit in all three slices (1136 / 1331 / 1225 above). The page must repartition (for example a fourth slice for F01/F08 counterpart ranges) or assign pinned subsets with measured counts.

## Minor notes
- M1. Label F08 as counterpart explicitly and name its owning topic.
- M2. Add the three per-slice output paths and an aspect line to the 2.2 section of the allocation page.
- M3. The "brief ~55" figure is unmeasured; the procedure requires a measured count of the full Codebase Research Agent Prompt copy plus the bindings read.

## Confidence denominator
Checked 6 of 6 requested checks and 5 of 5 topic-2.2 facts under check (F05, F06/F07/F09, F08 range, F01 range, slice assignment). Evidence: `wc -l` on 6 corpus files and 4 context files, def-boundary listing of models.py 227-720, F01 call-site and README tier-mention greps, a 11-line read at the F05 cut. Confidence in FAIL: high (B1-B3 directly observed; B4 is arithmetic on observed counts).

## Self-Audit
Attempted disproof of each blocking finding. B1: searched `ccsession` 1-120 for non-comment code (0 lines) and for tier call sites outside 700-1000 (found 1079-1838); no parser exists in 1-120. B2: grepped README for tier/profile (only line 23 in range). B3: read lines 556-566 and listed defs 442-681 to confirm the cut sits inside `user_access`. B4: recomputed totals from the page's own numbers plus `wc -l` scope counts (138/142/107/112). A counter-argument that scope inputs are covered by digest rows does not hold: the producer spec says "Read" them and the page itself lists them as 2.2 context without measuring a substitute. No attempt to disprove succeeded. Report-only; no edits outside this file. Limit: I did not read the full source files, only metadata and targeted greps, as the brief required.
