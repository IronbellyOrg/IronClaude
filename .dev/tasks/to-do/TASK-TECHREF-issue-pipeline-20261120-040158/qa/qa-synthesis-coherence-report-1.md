# QA Report - Synthesis Gate (qualitative), lens synthesis-coherence, partition 1

**Phase:** synthesis-gate (qualitative)
**Lens:** synthesis-coherence
**Partition:** 1 (synth-01, synth-02, synth-03)
Status: Complete
**Date:** 2026-11-20
**Fix authorization:** false

[PARTITION NOTE: Cross-file checks are done on partition 1 in full; the other three synth files were read only for consistency checks (cross-partition findings are labelled).]

## Verdict: FAIL

3 BLOCKING findings (B-1, B-2, B-3) and 14 MINOR notes. Only the BLOCKING findings produce the FAIL. The research ERRATUM sections (Gap-fill c1 B-1 and F-1, c2) were applied correctly in the partition 1 files; the blocking defects are places where the synth files state different facts.

## Cross-section fact table

"Where stated" uses synth numbers (s01 to s06). "Identical" is yes only when every place says the same thing.

| # | Fact | Where stated | Identical |
|---|------|--------------|-----------|
| 1 | Watcher real cycle is BUILT-OFF (enabled:false); `enabled` defaults false, stop `not_enabled` exit 0 (cycle.py:228, 685-686) | s01 s1, 2.1, 2.3 row 1, 2.4 row 1; s02 3 tree, 4.1, 4.4, 4.6; s03 5.1 status line; s05 8.1; s06 D-06 | yes |
| 2 | `once --dry-run` ignores `enabled`, BUILT-ON | s01 row 1b; s02 4.1, 4.4; s03 5.1 table; s05 8.1 | yes |
| 3 | Watcher writes nothing to GitHub; only outward effect is one `orca agent launch` | s01 2.1, 2.3 row 1; s02 4.5; s03 purpose and 5.1.2; s05 8.1 | yes |
| 4 | Seven read-only `gh` calls G1 to G7, same argv and call sites (G2 ends `-L 100`; lines 755, 796, 907/944/996, 905/926/942, 948, 957/1013, 983) | s01 s1; s02 4.5; s03 5.1.2; s05 8.1 | yes |
| 5 | Per-cycle `gh` call limit | s01 s1 "per-cycle call cap 35 (32 ordinary plus 3 reserved)"; s02 4.1 and 4.6 "32 plus 3 reserved", G1/G2 shared and apart; s03 5.1.2 "at most 37 calls per cycle, 2 on an idle cycle"; s05 line 264 "ceiling 37, idle 2"; s06 line 94 "37 per cycle" | **NO** (B-1) |
| 6 | Launch argv is 12 elements, prompt `/sc:issue --claim <N> --pipeline none`, pattern `^/sc:issue --claim [1-9][0-9]{0,8} --pipeline none$`, no marker | s01 2.1, 2.4; s02 4.2, 4.3, 4.4; s03 5.1.3; s05 8.1, 8.3 | yes |
| 7 | 59 reason words; exit codes 0,1,2,3,4,5,6,7,75; precedence 2,6,7,5,3,4 | s01 s1; s03 5.1.4, 5.1.6; s05 10.1, 10.2 (recounted: 4+7+9+7+17+9+6 = 59 and 27+17+9+1+4+1 = 59) | yes |
| 8 | `dispatch.json`: 7 keys, 17-field entries, 6 states, T-1..T-13 | s01 s1; s02 s6; s03 5.1.3; s05 10.2 | yes |
| 9 | Lease 60 min, marker window `pending_at` minus 300 s (`SKEW_TOLERANCE_S`), clock-skew warning 60 s (`SKEW_WARN_S`), day cap 6 per 24 h, 10 candidates | s02 4.1, 4.2; s03 5.1.1, 5.1.3, 5.1.5; s05 | yes |
| 10 | Watcher package module count | s01 "8 modules ... plus an empty `__init__.py`"; s02 tree and s03 "nine modules"; s05 A.1 "exactly nine modules" | yes in fact (9 files), different counting words (M-1) |
| 11 | Numbering of the poll-cycle steps | s02 4.1: steps 0 to 14 (re-read = 11, launch step = 12, commit = 13, conclude = 14); s03 5.1.1: steps 0 to 13 (`_launch` including the re-read = 11, commit = 12, conclude = 13); s01 2.1 uses no numbers | **NO** (B-2) |
| 12 | What a dry-run executes | s02 4.1 bullet: "steps 1 to 11 and returns inside step 12", yet s02 step 11 is the re-read the bullet says does not run; s03 5.1.1: "steps 1-10"; s05 10.3: "all reads run; no probe, re-read or launch" | **NO** (B-2) |
| 13 | `--pipeline` levels `worktree`, `full`, `full --submit`, `none`; the watcher always sends `none`; `none` ends after Wave 6 | s01 s1; s02 4.2; s04 5.2; s05 8.2 | yes |
| 14 | Guard levels W, WA, F, FS; words `worktree`, `full`, `full-submit`; unknown word reads as W ("degraded") | s01 s1; s02 4.3, s6; s04 5.3; s05 8.3 | yes |
| 15 | Typed first line that releases level W | s01 2.1, s02 4.3 and 4.6, s05 8.2 and 10.2: `/sc:implement` or `/task`; s04 line 111: "`/sc:implement`, `/sc:task` or `/task`" (untagged); s04 line 268 and s06 D-23 flag `/sc:task` as contradicted | partly (M-9, cross-partition) |
| 16 | L1 guard BUILT-ON, fail-open for ordinary sessions, fail-closed for bound sessions, exit 0 or 2 only | s01 row 3; s02 3.1, 4.6; s04 5.3; s05 10.3 | yes |
| 17 | G2 rule 2: a bound worker may run `orca orchestration send/ask` only with no `--to`; every other orca verb blocked | s01 2.1, 2.3 row 6, 2.4 row 6; s02 4.3, 4.6; s04 line 281 say so; s04 line 283 and s06 D-25 say the guard matches the basename `orca` only and `orca-ide` exits 0 (observed) | **NO** (B-3, cross-partition) |
| 18 | IR-7 refusal is off by the constant `IR7_REFUSE = False` | s01 row 12 and s02 4.3, 4.4, 4.6 "BUILT-OFF (enabled:false)" with a note that it is a constant; s04 "BUILT-OFF (a constant, not an `enabled` key)"; s06 D-19 "not `enabled:false`" | same state, three label wordings (M-2) |
| 19 | `orca_worktree.py pending` has no production caller | s01 row 10 (two test callers); s02 4.3 and 4.4 (one test caller); s04 5.2 (one); s06 D-18 (two) | yes on the fact; test-caller count differs (M-6) |
| 20 | Scheduler, dispatcher, `COORD-<RepoName>` worktree, zero-setup install: not found in snapshot (recounted: `COORD-` and `zero-setup` have 0 hits in the snapshot) | s01 rows 14, 15; s02 4.4, O-1; s03 5.1 table and 5.1.7; s04 5.4; s06 D-04, D-16, U-3 | yes |
| 21 | Removed package: 10 files, 1,597 lines, 10 verbs, commit 01e7a9e23, PR #682, 2026-11-19 18:02 -0600 (git show confirms the date) | s01 s1, row 8; s02 3, 4.4, 4.6; s06 Appendix B | yes |
| 22 | Coordinator text: WC-2..WC-16 (15 rules), 339 lines, no WC-17, no "Issue pipeline duties"; test file 3,220 lines, 59 tests (recounted: 3,220 and 59) | s01 s1, rows 7, 7b; s02 3.1, 4.4; s04 5.4; s05 A.3 | yes |
| 23 | Claim writes: C1 assign, C2 ClickUp PUT, C3 and C4 two marked comments (`gh issue comment` or `gh api -X PATCH`), C5 only inside a `full --submit` agent | s01 row 2; s02 4.5; s04 5.2; s05 8.1 | yes |
| 24 | Watcher test inventory: 20 files, 19,801 lines, 867 tests, 19 fixtures (recounted: `cat | wc -l` = 19,801; `grep -c 'def test_'` sum = 867; 21 `.py` files including `__init__.py`) | s01 s1; s02 3; s05 A.1 | yes |
| 25 | Guard test inventory: 17 files, 24,388 lines, 921 tests | s01 s1; s04 line 326; s05 Appendix A files the same tests under A.2, A.3 and A.4 and adds one more file, so the totals cannot be rebuilt from Appendix A | yes between s01 and s04; not traceable to Appendix A (M-8) |
| 26 | PR 686 / rewrite design: one out-of-scope sentence | s01 line 44 only; grep of the six synth files for "686" and "rewrite" finds only line ranges such as `685-686` and the word "rewrites" for the Bash hook | yes |
| 27 | "L1 / L2 are guard layers, not pipeline levels" | s01 s1 ("Two kinds of level"); s02 4.1 reuses "L2 to L14" and "L1" as launch-step labels | present, not fully respected (M-3) |

## Findings

| ID | Severity | Location(s) | Problem | Evidence | Required fix |
|----|----------|-------------|---------|----------|--------------|
| B-1 | BLOCKING | s01 section 1 "Key statistics", Watcher surface row (line 34) versus s03 5.1.2 CallBudget row (line 151), s05 line 264, s06 line 94 | s01 gives "per-cycle call cap 35 (32 ordinary plus 3 reserved)". s03, s05 and s06 say the per-issue budget is 35, G1 and G2 are shared calls counted apart and never refused, so one cycle makes at most 37 calls (2 when idle). Two sections give different per-cycle limits. | Snapshot `github.py`: `CALL_CAP = 35` (docstring "Most gh calls one cycle may make"); `CallBudget.spend()` refuses at 32 or 35 against `self.calls` only; `spend_shared()` adds to `shared_calls` and is never refused; `total` = calls + shared_calls (lines 437-463). R01 summary line 656: "37 calls worst case, 2 idle". | In s01 write "per-issue call cap 35 (32 ordinary plus 3 reserved) plus the two shared calls G1 and G2: at most 37 `gh` calls per cycle, 2 when idle". Do not call 35 a per-cycle cap anywhere. |
| B-2 | BLOCKING | s02 4.1 (table steps 11 to 14 and the bullet at line 139) versus s03 5.1.1 (diagram and table, lines 51-87) | The two sections number the same cycle differently. s02 says a dry-run "runs steps 1 to 11 and returns inside step 12 at L1", but its own step 11 is "Re-read before launch", which the same bullet says a dry-run never does. s03 says a dry-run runs steps 1-10 and returns inside the launch step. s02 also lists the re-read (step 11) before the launch step (step 12), while in the code the re-read is called inside `_launch` after the probe and prompt build (and s02's own step 12 text lists "probe, prompt, re-read" in that order). The owner reads "step 12" as the launch step in s02 and as the commit in s03. | Snapshot `cycle.py:1026-1035` (dry-run returns before `find_orca`); `cycle.py:1048-1058` (probe, prompt, then `_revalidate`). s03 line 129 "runs steps 1-10". | Use one numbering (s03's: 10 candidates, 11 `_launch` including the re-read, 12 commit, 13 conclude) in both sections. Fold s02 step 11 (G7, G3', G6') into the launch-step row. Change the s02 bullet to "a dry-run runs steps 1 to 10 and returns at the top of step 11 (`cycle.py:1029-1035`)". |
| B-3 | BLOCKING (cross-partition) | s01 2.1 (line 105), 2.3 row 6 (line 154), 2.4 row 6 (line 179); s02 4.6 "Level grid" row; versus s04 line 283 and s06 D-25 (line 245) | The ledger, the integration map and the diagram present G2 rule 2 and the orca allow-list as working ("every other `orca` verb off the allow-list is blocked", status BUILT-ON) with no caveat. s04 and s06 record that the guard matches the basename `orca` only, that `orca-ide` (the first name `find_orca` tries and the default binary of `sweep/probes.py`) is not recognised, and that a bound session ran `orca-ide orchestration send --to run:run_1` with exit 0 (observed, cases EXTRA-2 and EXTRA-3). The owner reading the ledger would conclude the no-`--to` rule holds for the real Orca binary. | Snapshot `launch-level-guard.sh` line 457 `orca)` is the only orca case; `grep -c orca-ide` on the guard = 0. s04 line 283: "Consequence: G2 rule 2 and the ESCAPE class do not constrain the `orca-ide` spelling". s06 D-25 DEFECT CANDIDATE, Q-17. | Add to ledger row 6 Note and to 2.4 row 6: "recognises the command word `orca` only; `orca-ide` is not constrained (observed exit 0), see Section 5.3 and Section 14 D-25". Add the same pointer to ledger row 3. |
| M-1 | MINOR | s01 line 33 versus s02 line 16, s03 line 41 | "8 modules ... plus an empty `__init__.py`" versus "nine modules". Same 9 files, different counting words. | `wc -l` of the package: 9 `.py` files, `__init__.py` is 0 lines | Say "eight modules plus an empty `__init__.py` (nine files)" everywhere. |
| M-2 | MINOR | s01 row 12; s02 4.3, 4.4, 4.6; s04 lines 26, 321; s06 D-19 | The IR-7 status label is written three ways: "BUILT-OFF (enabled:false)", "BUILT-OFF (a constant, not an `enabled` key)", "BUILT-OFF (`IR7_REFUSE = False`; not `enabled:false`)". The state is the same; s01 explains its use of the label, s06 negates it. | text comparison | Pick one wording for the assembled document, for example "BUILT-OFF (IR7_REFUSE = False; a constant, not the `enabled` key)". |
| M-3 | MINOR | s02 4.1 step 12 ("Launch step L2 to L14") and line 139 ("at L1"); s03 crash points "C1 to C5" versus s02 4.5 claim writes "C1 to C5"; "G1 to G7" `gh` calls versus guard "G1", "G2 rule 1/2" (s01 rows 6, 9; s04 5.3); s04 worker tiers "T1/T2/T3" versus watcher "T-1..T-13" | The same short labels name different things in one document. The required L1/L2 disambiguation exists only in s01 section 1 and is not respected where s02 reuses L1/L2 for launch-step labels. "G2" means the `gh issue list` call in the watcher and the guard rule in the ledger. | s01 line 27 versus s02 lines 128, 139 | Rename the launch-step labels (for example "launch sub-step 2 to 14") and add a one-line glossary: "G1..G7 = watcher `gh` calls; guard rules are written 'guard rule 1/2'; claim writes C1..C5; crash points written 'crash point C1..C5'". |
| M-4 | MINOR | s02 section 4 intro (line 91) | "touch each other only through GitHub comments and files". The watcher reaches the claim through an `orca agent launch --prompt` process start, not a comment or file. The same sentence says the watcher "starts one Orca session". | s01 2.4 row 1; s03 5.1.3 | "... through GitHub comments, one Orca launch prompt and files". |
| M-5 | MINOR | s01 line 144 | "rows 1b, 7b and 9 to 18 are additional rows" omits row 12b. | ledger rows | Add 12b. |
| M-6 | MINOR | s02 4.3 (line 199) and 4.4 (line 218) versus s01 row 10 | s02 names one test caller of `orca_worktree.py pending` (`test_launch_level_guard_worker.py:287`); s01 and s06 name two (`test_issue_orca_worktree.py:2472-2498` too). | s01 row 10; s06 D-18 | Name both in s02. |
| M-7 | MINOR | s02 line 11, s03 line 11, s04 line 9, s05 line 7 | Each synth file defines its own path shorthand (`P/`, `P`, `H/`, `HK/`, `GD`, `OW`, `SK/`). Joined into one document the same file has several short names. | the four convention lines | The assembler keeps one key and expands it once. |
| M-8 | MINOR (cross-partition) | s01 line 40 versus s05 Appendix A | "14 table files plus 3 claim-side pin files" refers to a table in research file 05 that is not in the reference; Appendix A files the same tests under A.2, A.3 and A.4 and adds `test_freshness_subagent_start_policy.py`, so 17 files / 24,388 lines / 921 tests cannot be rebuilt from Appendix A. | R05 lines 530-539 | State the file list or point to Appendix A rows; drop "table". |
| M-9 | MINOR (cross-partition) | s04 line 111 versus s04 line 268, s05 lines 69 and 223, s06 D-23 | The `worktree` level row says approval is a prompt starting `/sc:implement`, `/sc:task` or `/task` with no tag; the guard accepts only `/sc:implement` and `/task`. | guard line 347 per s04 | Tag the row [CODE-CONTRADICTED] or drop `/sc:task` and cite the template line. |
| M-10 | MINOR | s01 row 15 | "`dispatcher` hits are unrelated (swarm, Orca shim)". A grep of `src`, `plugins`, `docs` finds hits under `cli/eval`, `cli/swarm`, `core/HOW-WE-WORK.md` and two skill refs; the parenthetical does not name eval. The conclusion (unrelated) stands. | grep in snapshot | Say "unrelated (eval, swarm and doc text)". |
| M-11 | MINOR | s03 5.1.8 row 1 | The DES:827 skew row stays in a table titled "Contradictions found" with tag [CODE-VERIFIED]. R03 erratum item 1 says to drop it from the contradiction list (an optional ambiguity note is allowed). The row is honest about this, but a reader scanning the table sees a non-contradiction. | R03 lines 525-537 | Move to a note under the table. |
| M-12 | MINOR | s03 ("S1 halt", "DF-50"), s01 2.3 ("IR-4", "OB-H1..3", "FU-2") | Design-document codes are used with little or no gloss for an owner who has not read the designs. IR-4 and OB-H are explained by name in context; "S1" is not. | s03 lines 260, 309 | Add "S1 = the one-launch-per-cycle halt" at first use. |
| M-13 | MINOR | s02 4.4 hand-off rows versus s01 row 17 | The same hand-off is tagged NOT BUILT in the ledger and trigger table and [UNVERIFIED - doc-only] in 4.2 step 7 and O-7. The tags answer different questions (no code versus unconfirmed doc text) but the document does not say so. | s02 lines 169, 220, 346 | One sentence: "NOT BUILT = no code or contract text found; [UNVERIFIED] = the prose claim itself". |
| M-14 | MINOR | s02 3 tree (line 41) | `require-orca-worktree-agent.sh` is listed as a fourth hook script (registered at hooks.json per s05 line 98, pinned by a test per s05 A.2), but s01 (row 3, 2.2) does not say whether it belongs to the issue pipeline's guard layers. | s05 lines 98, 346 | One line in s01 2.2: "global hook, not an issue-pipeline layer; blocks a bare `worktree create` in a governed session". |

## Checks performed

1. Story connects (trigger, cycle, launch prompt, claim, worktree and level, guard hooks). Read s01 2.1 diagram and 2.4 map, s02 4.1 to 4.3, s03 5.1.1 to 5.1.3 end to end and compared names, constants and status words in 27 facts (table above). Re-read in the snapshot: `_steps` order (cycle.py:711-737), `_login_step`, `_launch` (1026-1112), `CallBudget` (github.py:437-463), constants (cycle.py:30-48), `PROMPT_PATTERN` and `build_claim_prompt` (launch.py:33, 84-92), guard level words (launch-level-guard.sh:262-272), counts (`wc -l`, `grep -c`), git date of 01e7a9e23. The chain is consistent except B-1, B-2 and B-3.
2. Ledger versus status lines versus trigger and writes tables. Watcher BUILT-OFF (enabled:false) and "writes to GitHub: none" agree in s01 rows 1, 1b and 2.4, s02 4.1, 4.4, 4.5, 4.6, s03 5.1 and 5.1.2, s05 8.1, s06 D-06. IR-7 label wording differs (M-2). G2 rule 2 status lacks the observed `orca-ide` limit (B-3).
3. Required content (a) ledger, (b) writes table, (c) trigger table is present (s01 2.3, s02 4.5, s02 4.4); rows 1 to 8 are the eight named pieces and status words are limited to the four allowed words. "No trigger found in snapshot" statements agree across s01, s02, s03, s04 and s06 (recounted: `COORD-` and `zero-setup` have 0 hits in the snapshot).
4. Contradictions between research files: the 300 s versus 60 s skew erratum, the dead constant (14 constants, 13 read), the `/sc:task` approval mismatch and the `orca-ide` gap are surfaced with tags rather than silently resolved. The one research figure that was narrowed without comment is the 37-call worst case (B-1).
5. Verified fact versus [UNVERIFIED] versus evidence limits: s01 "Evidence limits", s02 O-1..O-9, s03 5.1 table and 5.1.8, s06 U-1..U-11 agree (tests read not run; only the L1 guard executed on 44 payloads; no runtime state in a snapshot).
6. Aspirational content: none stated as current. The cron entry, FU items, hand-off to a worker, scheduler and coordinator duties are NOT BUILT, [UNVERIFIED] or REMOVED wherever they appear in partition 1.
7. L1/L2 disambiguation: present in s01 section 1; s02 4.1 reuses the labels (M-3). All other uses of "L1" and "L2" in s01, s02 and s03 mean the guard layers.
8. PR 686 and the rewrite design: exactly one sentence (s01 line 44); no other mention in any of the six files.
9. Owner readability: tables first throughout; some dense cells (s01 2.3 rows 1b, 2, 8; s02 4.5 C5), unexplained design codes (M-12) and label collisions (M-3).

## Self-Audit

**(a) Reliance list - rf-qa PASS items skipped for structural re-check:**
- No Inherited Structural Verdict was supplied in the spawn prompt, so nothing was relied on; the structure reports (`qa/qa-synthesis-structure-report-1.md` and `-2.md`) were not read. Section numbering and heading structure were not re-checked because they are outside the coherence lens.

**(b) Independent semantic checks (at least 1 required, INV-019):**
- Per-cycle `gh` call limit -- verified by reading `github.py` lines 40-52 and 437-463 and `cycle.py` 575-592 in the snapshot; led to B-1.
- Dry-run extent and step numbering -- verified by reading `cycle.py` 680-840 and 1020-1112; led to B-2.
- G2 rule 2 coverage -- verified by reading `launch-level-guard.sh` 450-500 and `grep -c orca-ide` = 0, then s04 line 283 and s06 D-25; led to B-3.
- Counts in s01 statistics -- recomputed `wc -l` of the watcher package (4,795) and watcher tests (19,801), `grep -c 'def test_'` (867 watcher tests; 59 in `test_worker_contract.py`), WC rule ids (WC-2..WC-16), `git show -s` date of 01e7a9e23, and the negative greps (`COORD-`, `zero-setup`, `release-worker`, `Issue pipeline duties`, `pipeline.json`): all match.
- Reason-word total -- recounted the groups in s03 5.1.6 (4+7+9+7+17+9+6 = 59) and s05 10.2 (27+17+9+1+4+1 = 59).

**Confidence (Confidence Gate Protocol).** Verified: 9/9 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%. The other three synth files were read only where they restate a partition 1 fact (synth-04 in full, synth-05 lines 1-245 and 296-375, synth-06 lines 140-290). Text outside those parts was not read line by line, so a cross-partition contradiction elsewhere cannot be ruled out.

**Tool engagement:** Read: 14 | Grep: 12 | Glob: 0 | Bash: 9. Each call maps to a check above. No web research was done (Tavily not used).

## Recommendations

1. Fix B-1, B-2 and B-3 in s01 and s02 (three small text edits) before assembly; no research re-run is needed.
2. Optionally apply M-3 and M-4 at the same time; the rest stay as notes.
3. After the fix, only the three BLOCKING findings need re-checking; minor findings are not rechecked.

Status: Complete
