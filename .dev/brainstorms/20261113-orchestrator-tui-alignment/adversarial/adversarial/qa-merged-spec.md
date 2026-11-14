# QA Report: Independent review of the merged alignment spec

**Topic:** Orchestrator / TUI alignment merged spec (`adversarial/merged-spec.md`)
**Date:** 2026-11-13
**Phase:** report-validation (independent, read-only; fix authorization: none)
**Fix cycle:** N/A

---

## Overall Verdict: FAIL

2 blocking findings (B1 TB-GIT gate cycle on SW-01; B2 no per-action grant for pushes and the thread resolve on PR #539), 10 minor notes. 33 fact spot checks: 30 CONFIRMED, 3 WRONG (line-number drift on true claims, minor). Everything else checked held: ids, edges, waves, INV-008 first and unresolved, honesty about L1 and L2, all 16 UNADDRESSED probe items carried by concrete rules, and section 6 complete for an orchestrator session.

## Method

- Read the merged spec in full (lines 1-1345, ten chunked Reads), the seed brief (113 lines), the Round 2.5 invariant probe (98 lines), the merge-executor steps and acceptance checks A1-A15 of `refactor-plan.md` (lines 636-680), and targeted parts of ADJ (lines 67, 148-175 Part 1.3, 192, 206, 442, 450-465, 710).
- Mechanical checks ran as read-only scripts in private `/tmp/ironclaude-batch.*` folders (removed by trap): a grep/awk/sort/comm batch (ids, Q ids, placeholders, headings, edge numbering) and one `uv run python -I` parser of the 4.2 edge table (endpoints, cycles, wave order, table-cell versus edge consistency).
- Fact checks: one read-only bash batch (14 commands; `git show origin/master:...`, `sed -n`, `ls`, `git worktree list`), two Grep calls on sweep and observer code, `gh pr view 539/541` and `gh api repos/IronbellyOrg/IronClaude/pulls/539/comments` (GET only), and ADJ greps.
- No file other than this report was written. No GitHub, git or Orca write.

## Check 1: Mechanical

| Sub-check | Method | Result |
|---|---|---|
| Work-item ids defined | grep `^\| (SW\|OB\|WA\|CO\|V2\|XC)-nn \|` rows in lines 160-460 | 50 unique, no duplicate rows: SW 14, OB 9, WA 7, CO 4, V2 5, XC 11. Matches 0.2/4.1 claim "V1's 46 plus SW-14, V2-05, XC-10, XC-11" |
| Every id used is defined | ids used outside the appendix id map (lines 1199-1256) and outside HTML comments, minus defined set (`comm -23`) | empty set. PASS |
| Graph mentions every item | defined set minus ids in edge rows 646-771 | empty set. PASS (plan A4) |
| Edge endpoints exist | parsed 123 rows (311 From-To pairs); each endpoint checked against items, Q1-Q33, 8 K-nodes, 10 TB-nodes, LIVE, ORCA-AVAILABLE, SWEEP-RUNNABLE, TB-GIT-ROW, OWNER-MERGE, `GRANT(<item>,<9 listed actions>)` | 0 undefined endpoints. PASS (plan A3) |
| Edge numbering | `^\| n \|` in 4.2 | 123 rows, 1 to 123, contiguous |
| Q ids | `\bQ[0-9]+\b` outside comments | exactly Q1 to Q33, all defined in section 3; `Q-1`/`Q-2`/`Q-3` used 7/4/2 times as Orca gate tests, defined in 0.2 and 4.1. PASS |
| Leftover placeholders | grep `TODO\|TBD\|FIXME\|RF_PLACEHOLDER\|RESUME\|{{\|XXX` | NO_MATCH. PASS |
| Heading hierarchy | all `^#{1,6} ` lines | one H1; eight H2 0 to 7 in plan order, then four `Appendix` H2s (plan A15); H3 numbering contiguous per section (0.1-0.6, 1.1-1.5, 2.1-2.6, 4.1-4.5, 5.1-5.6, 6.1-6.10, 7.1-7.5). The eight `#` lines at 789-824 are inside the ```` ```text ```` block, not headings. PASS |
| Internal section references | read every "section N", "N.N", "(6.8)", "XC-02 (6)", "Weak point Wn", "4.1"/"4.2" reference while reading | all resolve (6.3 PR session, 6.8 grant table, XC-02 (6) skip rule, W1-W6 present, Change numbers in comments are provenance only) |
| Per-item cells versus the 4.2 table | parser compared each row's blocked-by/blocks work-item ids with hard and SOFT edges | mismatches exist (see minor note M1); the spec declares 4.2 authoritative (line 587), so not blocking. Real gaps besides row 119/122 generic edges: SW-07 -> XC-07 (edge 114) missing from both cells; XC-08 "blocks" OB-09 and V2-01 but no edge exists; XC-08 -> OB-08 (edge 54) and XC-08 -> V2-03 (edge 91) missing from the blocked-by cells; SW-05 blocks cell omits SW-11, SW-14, XC-04, XC-06 |
| Gate-node cycles | traced satisfaction conditions of every gate/TB node used as a GATE From | **TB-GIT -> SW-01 (edge 2) is a cycle**: TB-GIT is "Satisfied only when SW-02's landed test covers every channel ... or Q1 = F3 is recorded" (line 630), SW-02 needs SW-01 (edge 4), and SW-01's blocked-by is "Q1; TB-GIT" (line 190). See blocking finding B1 |

## Check 2: Waves

Wave assignment taken from 5.1 (lines 858-863): W0 = SW-01, SW-03, SW-04, SW-06, XC-01, XC-02, XC-09, XC-10 (8); W1 = SW-02, OB-01, OB-02, OB-03, OB-04, WA-01, WA-02, WA-03, CO-01, CO-02, XC-03, XC-05, XC-08, V2-05 (14); W2 = SW-05, OB-05, OB-06, OB-08, WA-04 (5); W3 = SW-07, SW-08, SW-09, OB-07, WA-05, WA-06, V2-01, XC-04, XC-06, XC-07, XC-11 first-release (11); W4 = SW-10, SW-14, V2-02, V2-03 (4); W5 = SW-11, SW-12, SW-13, WA-07, OB-09, CO-03, CO-04, V2-04, XC-11 end-to-end (8 + XC-11).

| Sub-check | Result |
|---|---|
| Every item in a wave | all 50 placed; none missing. XC-11 appears in W3 and W5 by design (two scopes, stated in XC-11 and 5.1); recorded as minor note M5 |
| No hard edge from a later wave to an earlier one | 0 backward hard edges among items. Same-wave hard edges all appear in that wave's serial column (OB-03 -> OB-04, WA-01 -> WA-02, XC-05 -> CO-02, CO-02 -> CO-01, WA-02 -> CO-01, OB-05 -> OB-06, SW-07/XC-06/XC-04 -> XC-07, SW-09 -> V2-01, SW-14 -> V2-02, V2-02 -> V2-03, XC-10 -> XC-09/SW-03, XC-01 -> XC-02 -> SW-06). PASS (plan A5) |
| Backward SOFT edges | 3: XC-03 ~> SW-06 (edge 19), XC-04 ~> OB-08 (edge 58), V2-01 ~> V2-05 (edge 99). All are declared SOFT ("never block a wave"); each item's text handles the late input (SW-06 row added later; OB-08 (6) omits "join key"; V2-05 ungated per ADJ line 710). Acceptable |
| No cycle among work items | DFS over hard item-to-item edges: no cycle. The only cycle is through the TB-GIT gate node (B1) |
| Gates that nothing satisfies | LIVE, ORCA-AVAILABLE are external host conditions (defined 4.1); SWEEP-RUNNABLE <- SW-05, Q29 (edge 107); TB-GIT-ROW written by the coordinator (6.4 rule 1); OWNER-MERGE defined but replaced on edges by `GRANT(<item>,merge)`. TB-GIT: satisfiable only after SW-01, which it gates (B1). No other unsatisfiable gate |
| 5.2 three lists | recounted: 17 waiting for SW-05 + 32 never waiting + SW-05 = 50, matches the spec. Spot-traced SW-09 (via OB-08, CO-01, XC-08: no SW-05 path) and OB-09 (via XC-07 <- SW-05) |

## Check 3: Safety and guardrails

`WORKER-CONTRACT.md` lines read: 23 (never-as-worker list includes `/sc:pr-submit`), 41 (WC-9: push and PR are off for a worker; "the coordinator performs those actions"), 42 (worker commit only by quoted grant), 62 (WC-13), 243 (PRs via pr-submit "in an ordinary top-level session ... never as a worker"), 244 (show unseen commits before push), 288 (WC-16), 298 (brief template). All cited correctly by the spec.

| Guardrail | Where stated in the spec | Result |
|---|---|---|
| INV-008 first, UNRESOLVED-EXTERNAL, no code fix | 0.1 (line 28-36) is the first subsection; "This spec does **not** specify the code fix"; frontmatter status; SW-01/SW-02 give requirement and test, not a fix; 6.4 rule 1; 6.9; R25-INV-018 row | PASS |
| No worker runs `/sc:pr-submit` | 6.3 Worker "Never does"; PR session row; 6.4 rule 2; 7.2 Interaction row; every PR item's runs-in cell says "a supervised worker makes and tests the change to `worker_done`; the PR session opens the PR" | PASS (plan A11) |
| No worker creates worktrees or dispatches workers (WC-13) | 0.5, 5 intro, 6.3 Worker row ("calls `agent launch`"), 6.4 rule 4, 6.5 row, 6.9, TB-WC13 with edge 120 | PASS |
| Fork-only PRs, never upstream | TB-UPSTREAM; 6.4 rule 2 (`--repo IronbellyOrg/IronClaude`, URL check, no push/fetch/PR/issue/comment/remote with `SuperClaude-Org/SuperClaude_Framework`); 6.5 wrong-fork row; 6.9 | PASS. Minor M4: 6.1 "Live state" row writes `gh pr view` without `--repo` (6.4 rule 2 still governs) |
| `.claude/` mirrors never staged | 6.4 rule 3; 6.9 | PASS |
| `.dev/tasks/` always staged | XC-01; 6.1 ledger row; 6.4 rule 3 ("staging is not committing") | PASS |
| Worktrees only via Orca with `--agent` | 0.5, 5.4, 6.2 (exact command), 6.4 rule 4, 6.9, XC-09 (3) "never both" | PASS |
| No outward write without a recorded per-action owner grant | GRANT node (4.1), 6.8 grant table, 6.4 rule 2, 6.9; issue posts, merges, thread reply, live reads/tests, pr-submit each have GRANT edges | **FAIL (B2)**: pushes to PR #539 by the #539 author (SW-02 "the PR is pushed", SW-03 (5), SW-05 (1)) and the Augment thread resolve (SW-03 (4)) have no GRANT edge; `push` is not in the action vocabulary (line 607, line 1045), yet 6.8 says "A push grant satisfies neither ..." (line 1045). SW-03's push is scheduled in W0 |
| JOIN not before the INV-008 requirement is met in the code actually run | XC-04 (4), (5); edge 106 (TB-GIT, TB-GIT-ROW, SW-05, SWEEP-RUNNABLE); 5.3 last-but-one row; record names revision and `--root`; old `.dev/sweeps/` reports excluded | PASS |
| Coordinator ledger not in the #539 checkout by default | XC-01 location "never in the #539 checkout"; XC-09 runs-in; Q26 default "XC-09 does not start; the owner keeps the ledger by hand"; 5.4; 6.4 rules 3 and 15 | PASS |

## Check 4: Honesty

| Sub-check | Method | Result |
|---|---|---|
| No claim that L1 (watcher-to-orchestrator handoff) or L2 (orchestrator manages work) exists | grep `handoff\|hands (an\|off)\|manages work` minus lines carrying DEFERRED/NOT BUILT/not built/No/does not/SW-13/WA-07/SW-12/later | remaining hits are the SEED target sentence (line 121), the contract completion rule (157), SW-13/WA-07 acceptance text (DEFERRED rows), V2-03's `--handoff design` flag and 6.10's "Evidence handoff" title. 0.3 rows (76-77), 0.4 item 7, 1.1 L1/L2 rows "**No.**", 1.2 "still broken at L1 and L3", 6 intro "L2 is not built", 6.9 "Claim that a chain link (L1 to L4) works" forbidden. PASS (plan A7) |
| Unbuilt links labelled with the item that closes them | 1.1 column "Work item that closes it": L1 WA-07 via SW-13, L2 SW-12, L3 V2-04, L4 OB-09, each with gate; 7.5 slots | PASS |
| UNVERIFIED / PLAN INFERENCE kept | counts in the file: UNVERIFIED 22, PLAN INFERENCE 74, UNRESOLVED-EXTERNAL 9; spot instances: #541 branch name UNVERIFIED (SW-04), PR-session sequential launch UNVERIFIED (Q25, 6.3), worktree names PLAN INFERENCE (5.4), partial-file behaviour UNVERIFIED (2.1 interface) | PASS |
| Withdrawn findings (ADJ Part 1.3, lines 148-175) not re-opened | compared each of the 19 withdrawn rows with the spec: persistence is Q9 Phase 2; no "#539 needs a rebase"; "re-run only" forbidden (SW-05 (1), 6.5); Collision Lens "synthetic image, not built" (V2-01); W-3 not added (OB-08 (8)); seeded test "necessary, not sufficient"; PARTIAL steady state; repo filter does not close the thread (0.1); labelling by prompt gated on D-B (SW-10) | PASS |

## Check 5: Fact spot-check

33 claims, spread over all six systems. CONFIRMED 30, WRONG 3 (all three are moved line numbers on true claims, inherited from ADJ citations; graded minor), UNVERIFIABLE 0 (one sub-part noted).

| # | System | Claim (spec location) | Evidence | Result |
|---|---|---|---|---|
| 1 | XC | Task package `.dev/tasks/to-do/TASK-RESEARCH-sub-orchestrator-mode-20261108-181115` exists (0.4 item 5) | `ls -d` | CONFIRMED |
| 2 | XC | Task package `.dev/tasks/to-do/TASK-TECHREF-orchestration-20261110-050239` exists | `ls -d` | CONFIRMED |
| 3 | XC | `docs/architecture/SUPERVISED-ORCHESTRATION-TECHNICAL-REFERENCE.md` exists | `ls` | CONFIRMED |
| 4 | SW | PR #539 OPEN, head `873599d59`, 1003 files, UNSTABLE (2.1) | `gh pr view 539 --repo IronbellyOrg/IronClaude --json ...`: OPEN, `873599d59bc9...`, changedFiles 1003, UNSTABLE, not draft | CONFIRMED |
| 5 | SW | PR #541 OPEN, CLEAN, head `779e58b17`, one file `tests/core/test_claude_md_worktree_rule.py` (0.3) | `gh pr view 541`: OPEN, CLEAN, `779e58b175...`, 1 file, that path | CONFIRMED (branch is `fix/claude-md-worktree-rule-test`; spec marks it UNVERIFIED, honest) |
| 6 | SW | Six review threads; Augment at `probes.py:1052`, Codex security at `probes.py:1211` (2.1) | `gh api .../pulls/539/comments`: six root comments, augmentcode at `probes.py:1052`, chatgpt-codex at `probes.py:1211` | CONFIRMED (resolved/unresolved state needs GraphQL; not checked, GET-only rule) |
| 7 | OB | `QUESTION_GATE_PASSED = False` at `observe/commands.py:63-67`, constant at :67 (0.3, 2.2) | `git show origin/master:...commands.py \| sed -n 60,68p`: line 67 `QUESTION_GATE_PASSED = False`, comment 63-66 | CONFIRMED |
| 8 | WA | `launch.PROMPT_PATTERN` at `launch.py:33` has no `--pipeline` (2.3) | `git show origin/master:` line 33 `re.compile(r"^/sc:issue --claim [1-9][0-9]{0,8}$")` | CONFIRMED |
| 9 | WA | `build_claim_prompt` at `:84-92` | same file lines 84-92 | CONFIRMED |
| 10 | WA | `OPERATION_ID_PATHS` at `launch.py:39-45` is a guess | lines 39-45, comment "[PROPOSAL, UNVERIFIED]" | CONFIRMED |
| 11 | OB | `main.py:572-574` on master registers observe; 576-578 on #539 head (0.3) | `git show origin/master:` 572 import, 574 `add_command`; HEAD 576-578 same | CONFIRMED |
| 12 | OB | `issue-409-mvp` at `f104ca51a [409-Phase2]` (0.3, 5.4) | `git worktree list` | CONFIRMED |
| 13 | XC | `issue-394-launch-level-hook` at `e6febfa2f` (5.4) | `git worktree list` | CONFIRMED |
| 14 | XC | Main checkout `/home/coder/workspaces/IronClaude` on `docs/409-orca-dashboard-designs` at `495eb96d1` (Q26, 5.4) | `git worktree list` | CONFIRMED |
| 15 | SW | Four `.dev/sweeps/` reports `20261112-031151` to `20261112-034511` (4.1 TB-GIT-ROW, XC-04 (5)) | `ls .dev/sweeps/`: 031151, 031209, 031239, 034511 | CONFIRMED |
| 16 | SW | `ALLOWED_GIT` exact one-entry list at `probes.py:64-67` (2.1) | lines 64-67 | CONFIRMED |
| 17 | SW | Version check compares text before the first hyphen, `report.py:160`, `:23` (2.1) | :160 `observed.split("-", 1)[0] == CHECKED_ORCA_VERSION`; :23 `"1.4.245"` | CONFIRMED |
| 18 | SW | `ROW_KEYS` at `tests/sweep/test_report.py:1255`; NFR-001 at `test_readonly.py:300`, `test_cli_contract.py:1474`, `orchestrator-mode.md:128` (2.1, K-nodes) | `sed -n` each line | CONFIRMED |
| 19 | OB | `HISTORICAL_STATES = ("released", "retained")` at `view.py:35` | master line 35 | CONFIRMED |
| 20 | OB | `XDG_STATE_HOME` accepted only when absolute, `export.py:241-242` | master lines 241-242 | CONFIRMED |
| 21 | OB | mode 0600 at `export.py:26` (2.2) | line 26 is `SNAPSHOT_NAME`; mode 0600 is at line 260 (Grep) | WRONG (line only; claim true; ADJ citation) |
| 22 | OB | caps `adapter.py:29,57` (limit 100, 5 calls) | :29 `--limit 100` template, :57 `MAX_CALLS_PER_CYCLE = 5` | CONFIRMED |
| 23 | OB | `tests/observe/record_golden.py` exists on `origin/master` (OB-05) | `git cat-file -e` | CONFIRMED |
| 24 | XC | Contract note `docs/designs/observe-sweep-contract.md` not written (0.3) | `ls` fails | CONFIRMED |
| 25 | XC | `NOTE_DUPLICATE_DISPATCH` at `classify.py:893-896` (XC-04 (2)) | constant at :76, used at :898; 893-896 is `health=`/`result=`/`forced =` | WRONG (line drift; claim true; ADJ citation) |
| 26 | XC | Join basis `row_id = orca:<dispatch>` at `probes.py:435`, `classify.py:891` (2.6) | classify.py:891 `row_id=f"orca:{o.dispatch}"` CONFIRMED; probes.py:435 reads `dispatchId`, not `row_id` | WRONG for the `probes.py:435` half (line drift; ADJ citation) |
| 27 | XC | `sc-pr-submit-protocol/SKILL.md:19` attended poll loop, `:47` main session only, `:70` "augment review" re-trigger, `:234` open or attach, `:241` `--merge-guard` default draft (6.3, 6.8) | `sed -n` each line | CONFIRMED |
| 28 | SW | `sc-sweep-protocol/SKILL.md:23-24`: `uv run` fallback only on "command not found" (6.6, 7.3) | lines 23-24 | CONFIRMED |
| 29 | XC | `sweep/commands.py:220-240`: `--root` defaults from the current folder, output `<root>/.dev/sweeps/` (XC-04 (4)) | lines in range: `--root` help "found from the current folder", report folder "Default: `<root>/.dev/sweeps/`" | CONFIRMED |
| 30 | WA | `docs/designs/issue-watcher-setup.md` mentions `forfeit-guarantee` (WA-03) | grep: lines 504, 509 | CONFIRMED |
| 31 | XC | ADJ line 442 publication order; line 710 "may be done ahead"; line 206 probe experiment; line 67 Q-1 to Q-3 are Orca gate tests | `sed -n` on ADJ | CONFIRMED |
| 32 | OB/SW | 513 rows (E-14), 28 of 53 Runs without `coordinator_handle` (INV-024), at least 18 of 29 worktrees share one `.git/config` (INV-008), X-016 61 percent, #409 body 30,030 to 30,758 bytes (A-010); ADJ Part 5.1 has 16 rows | grep ADJ lines 173, 196, 206, 331, 333, 329, 456, 465; `5.1 ... (16 rows)` at line 450 | CONFIRMED |
| 33 | XC | Id counts: 50 items (46 + 4 new), Q1-Q33, 123 edges, 5.2 lists 17 + 32 + 1 | Check 1 and Check 2 scripts | CONFIRMED |

WORKER-CONTRACT line citations (23, 41, 42, 62, 243, 244, 288, 298) were also all CONFIRMED (Check 3) and are not counted above.

## Check 6: Invariant coverage (the 16 UNADDRESSED probe items)

For each item I opened the locations the coverage appendix (lines 1307-1322) points to and looked for an operative rule, not just a table row.

| Probe id | Rule found (spec line) | Concrete? |
|---|---|---|
| R25-INV-001 (HIGH) PR actor | 6.3 PR session row (962): owner-designated top-level session, launched after `worker_done` is admitted and the worker's session has ended; 6.4 rule 2 (973); XC-09 (3) (457) "never both", coordinator never runs pr-submit; Q25 (552) with default "no PR opened, lane held". Sequential launch in a `worker-start` worktree marked UNVERIFIED | Yes |
| R25-INV-002 (HIGH) coordinator home | XC-01 location (449), XC-09 runs-in (457), Q26 (553) with accepted-cost sentence and default, 5.4 row (898), 6.2 (949), 6.4 rule 3 (974) | Yes |
| R25-INV-003 (HIGH) skip rule | XC-02 (6) (450): skipped recorded, next link eligible, skipped satisfies the order edge only, never DEC or content; Q2/Q3/Q20 defaults (529-530, 547); 6.5 row (996); 7.4 item 14 | Yes |
| R25-INV-004 (HIGH) other git channels | 0.1 "Channels in scope" (36); SW-01 (4); SW-02 (1) adds `filter.probe.process` and "every further channel the ruling puts in scope, so a fix that blanks only `.clean` fails it" (191); TB-GIT (630); Q1 (b) (528); 7.3 row 1 | Yes |
| R25-INV-005 (HIGH) pr-submit on #539 | SW-02 runs-in and SW-03 (5) (191-192); SW-05 (6) (194) incl. stop before any fix on a ruling-needing finding; 6.3 #539 author row (963); 6.5 row (1007); 6.9 (1062); Q28 (555) with `--merge-guard off` | Yes |
| R25-INV-006 sweep not runnable | SWEEP-RUNNABLE (601) with exit-0 test; edge 107; 6.5 row (1006); 6.6 note (1029); 7.3 row 2; Q29 (556) | Yes |
| R25-INV-007 JOIN actor and location | XC-04 (4) (452): after SW-05, master code, record actor, revision, `--root`, destination; W3 placement | Yes |
| R25-INV-008 OB-04 target Run | OB-04 (1), (4) (252): owner-approved disposable representative Run, never the alignment coordinator's own, held if none; Q30 (557); 6.3 read-capture row (964) | Yes |
| R25-INV-009 Orca down | ORCA-AVAILABLE (604) on every live lane; 6.5 row (1005) with retry bound and owner ask; 5.6; 7.4 item 12 | Yes |
| R25-INV-010 owner cron | 6.6 cadence record (1014-1024), last row status = Q31; Q31 (558) default does not pick from memory | Yes |
| R25-INV-011 F3 inventory | SW-02 F3 branch (191): `git grep -n -i -E` at ruling time over #539's file list, at least 16 locations, plugin mirror byte-equal | Yes |
| R25-INV-012 SW-02 plan package | SW-02 (5) (191): reuse check first, else only under Q27, else coordinator home by absolute path, named-path staging; 6.4 rules 5, 15; Q27 (554) | Yes |
| R25-INV-013 per-PR per-action approval | GRANT node (607) replaces M-APPROVAL; 6.8 grant table columns incl. lifetime and revocation (1045); "Each row is itself the owner's approval; no agent writes one" | Yes, but the action list omits `push` (B2) |
| R25-INV-014 pr-submit writes | 6.8 "What a `pr-submit` row lists" (1048): create/attach, fix commits, troubleshoot artifacts, push, replies/resolves, re-trigger comments, draft toggle or `--merge-guard off`, resume effects; merge never in it | Yes |
| R25-INV-015 worker commits | 6.4 rule 14 (985); 6.3 Worker row (961); 6.10 brief (1068); Q32 (559) | Yes |
| R25-INV-016 TB-1 as ledger row | TB-GIT-ROW (610); XC-04 (5) (452); 6.4 rule 1 (972); 7.4 item 11 | Yes |

All 16 have an operative rule at the cited location; the residual on R25-INV-013 is reported as B2. INV-018 (ADJ INV-008) stays UNRESOLVED-EXTERNAL with no fix design (line 1324). ADJ's own 16 UNADDRESSED rows (Part 5.1) are each mapped in 7.1 (lines 1085-1100); I matched the id list against ADJ lines 450-465.

## Check 7: Usability for the orchestrator (section 6)

| Needed piece | Present? | Where |
|---|---|---|
| Inputs | yes | 6.1 (spec, ADJ, SEED, ledger, worker contract, orchestration guide with CLI resolution order, existing packages, system docs, live state) |
| Worktree map | yes | 5.4 (verified rows plus PLAN INFERENCE rows) and 6.2 (exact create command, per-row recording rule) |
| Roles | yes | 6.3: owner, coordinator, worker, PR session, #539 author, read-capture operator, seed-test operator, single editor, independent reviewer, each with Does / Never does |
| Guardrails | yes | 6.4 rules 1-15 |
| Stop and escalation rules | yes | 6.5 (14 triggers incl. Orca down, sweep missing, wrong fork, ruling-needing finding, WC-16 cases, source conflicts) |
| Cadence | yes | 6.6 cadence record and notes |
| Decision ledger | yes | 6.8 row format, grant table format, pr-submit row content; 6.7 status output |
| Never-do list | yes | 6.9 |
| Resume and handoff | yes | 5.6, 6.10 |
| Wave gates and ask order | yes | 5.1, section 3 ask order (523) |

Gaps (minor, M2 and M3): the ledger package name is left as `.dev/tasks/<program-package>/` with no naming rule; the spec never says whether the coordinator creates its own Orca Run (`run-create`) for `worker-start` dispatch or which Run it binds, although 6.3/OB-04 refer to "the alignment coordinator's own" Run. Both are recoverable from the orchestration guide and the owner's Q26 answer, so they do not block. The literal reading of edge 2 (B1) would stall the session on its first action; that is the one usability defect that blocks.

## Seed-brief success criteria and plan acceptance checks

| Criterion | Result | Evidence |
|---|---|---|
| SEED 1-7 per system (scope, current state with source, target, items with ids and checkable AC, blocked-by/blocks, Q with recommendation and default, risks and reversibility) | PASS for all six systems (2.1-2.6 each have Scope, Current state, Target state, Work items table with Observe: cells, Risks with a Reversibility bullet; Q column plus section 3 table with recommended and default) | lines 167-515, 526-560 |
| SEED 8 dependency graph, no dangling reference | dangling: PASS (0 undefined endpoints). Graph validity: FAIL through B1 (gate cycle on SW-01) | 4.1-4.4 |
| SEED 9 ordered waves with parallel lanes, serial items and gates | PASS | 5.1-5.6 |
| SEED 10 chain to target | PASS | 1.1-1.5 |
| SEED 11 closing orchestrator section | PASS on content; section 6 is not the last section (7 and appendices follow, per the plan's fixed H2 order); minor M6 | section 6 |
| SEED 12 convergence by invariant coverage, INV-008 first | PASS | 0.1, 7.1, R25 appendix, provenance appendix item 4 |
| SEED constraints (read-only, project rules, Q not decided, labels kept, single host, A-004) | PASS except the per-action grant gap B2 against the "owner-gated outward action" intent | 0.4, 6.4, 6.9 |
| Plan A1 R25-INV-001..016 rule and location | PASS | Check 6 |
| Plan A2 used minus defined empty | PASS | Check 1 |
| Plan A3 endpoints exist | PASS | Check 1 |
| Plan A4 graph covers 50 items | PASS | Check 1 |
| Plan A5 waves respect edges, no cycle | item-level PASS; the spec's own 4.3 item 2 "No cycle" is false once gate nodes are included (B1) | Check 2 |
| Plan A6 INV-008 first and unresolved, no fix design | PASS | 0.1 |
| Plan A7 no L1/L2 claim | PASS | Check 4 |
| Plan A8 20 facts sourced | PASS (33 checked; 3 line drifts inherited from ADJ) | Check 5 |
| Plan A9 project rules in 6.4 | PASS | 6.4 rules 2-4 |
| Plan A10 read-only stated | PASS | 0.4 item 1 |
| Plan A11 no worker runs pr-submit | PASS | Check 3 |
| Plan A12 id spaces kept apart | PASS on spot reads (0.1, 6.4, 7.1, R25 appendix use `R25-INV-nnn`; bare `INV-nnn` only for ADJ ids such as INV-010, INV-011) | sampled |
| Plan A13 every Q has a default with no outward step | PASS (Q1-Q33 each have a default cell; none posts, merges or edits) | section 3 |
| Plan A14 map validation | PASS (a), (d) by script; (b), (c) sampled through the appendix map | appendix |
| Plan A15 heading structure | PASS | Check 1 |

## Issues Found

### Blocking

| # | Severity | Location | Issue | Required fix |
|---|---|---|---|---|
| B1 | IMPORTANT (blocking: broken dependency, false "No cycle" claim) | merged-spec.md 4.2 edge 2 (line 649), TB-GIT definition (line 630), SW-01 blocked-by "Q1; TB-GIT" (line 190), text graph line 790, 4.3 item 2 (line 776) and item 3 (line 777) | **TB-GIT gate cycle on the first action.** Line 587 says `A -> B` means A "must be done (or decided, or hold) before B starts". TB-GIT holds "only when SW-02's landed test covers every channel the ruling puts in scope, or Q1 = F3 is recorded" (line 630). SW-02 needs SW-01 (edge 4), and the F3 record is SW-01's own output. So SW-01 (the INV-008 ruling, the spec's first action) waits for a node that only SW-02 or SW-01 can satisfy. An orchestrator applying the "authoritative" table literally stalls at W0. 4.3 item 2 claims "No cycle" and item 3 lists SW-01 as a root; both checked only work-item edges. Edges 15 (TB-GIT -> SW-05) and 106 (TB-GIT -> XC-04) use the satisfaction meaning correctly | Remove edge 2 or give it a non-gating kind (for example a "names the boundary" declaration, not GATE), drop TB-GIT from SW-01's blocked-by cell and from line 790, and correct 4.3 items 2 and 3 to cover gate nodes |
| B2 | IMPORTANT (blocking: guardrail gap and internal contradiction) | 4.1 GRANT action list (line 607), 6.8 grant table actions and "A push grant ..." sentence (line 1045), 6.4 rule 2 (line 973), SW-02 (line 191), SW-03 (4)-(5) (line 192), SW-05 (1) (line 194), W0 L-539 lane (line 858) | **Pushes and the thread resolve on PR #539 have no per-action owner grant.** 6.4 rule 2 says "the owner grants each outward action separately in the ledger". SW-02, SW-03 and SW-05 (1) require hand pushes to PR #539 by the #539 author, and SW-03 (4) resolves the Augment review thread; none has a `GRANT(...)` edge (edges 4-17), and `push` is not one of the nine grant actions, although 6.8 refers to "a push grant". SW-03's push is scheduled in W0, before any grant row exists. WC-9 (`WORKER-CONTRACT.md:41`) classes push as an outward action. Q33 names who pushes; it is not a recorded per-action grant | Add `push` to the action vocabulary in 4.1 and 6.8; add `GRANT(SW-02,push)`, `GRANT(SW-03,push)`, `GRANT(SW-03,thread-reply)` (resolve) and `GRANT(SW-05,push)` edges and cells; or state explicitly that the owner's Q33 answer is recorded as those grant rows |

### Minor notes (do not fail the review)

| # | Location | Note |
|---|---|---|
| M1 | Section 2 blocked-by/blocks cells versus 4.2 | Cells and edges disagree in places: SW-07 -> XC-07 (edge 114) is in neither cell; XC-08's blocks cell names OB-09 and V2-01 with no edge; OB-08 and V2-03 cells omit XC-08 (edges 54, 91); SW-05's blocks cell omits SW-11, SW-14, XC-04, XC-06; 5.1 W2 gate for OB-08 omits XC-08. Wave order stays safe because the 4.2 table is authoritative (line 587) |
| M2 | XC-01, 6.1, 6.4 rule 3 | Ledger package named only as `.dev/tasks/<program-package>/`; give a naming rule |
| M3 | Section 6 | The coordinator's own Orca Run (create or bind, record its id) is not stated, though OB-04 and 6.3 refer to it |
| M4 | 6.1 "Live state" row (line 945) | `gh pr view` written without `--repo IronbellyOrg/IronClaude`; 6.4 rule 2 still requires it |
| M5 | 5.1 | XC-11 appears in W3 and W5 (two scopes, stated); not "exactly one wave" literally |
| M6 | Section order | SEED criterion 11 asks for a closing section; section 6 is followed by 7 and the appendices (plan-mandated order) |
| M7 | 4.3 item 4 (line 778) | "XC-07 feeds only K-NOTE and XC-11" is wrong: edge 60 XC-07 -> OB-09 is a hard GATE |
| M8 | 7.4 item 1 (line 1166) | The Q1-never-answered list omits SW-14, XC-04, OB-09, WA-07 and XC-11 that 5.2 lists as waiting on SW-05 |
| M9 | 2.2 `export.py:26`; 2.6/XC-04 `classify.py:893-896`, `probes.py:435` | Line numbers drifted (mode 0600 is at `export.py:260`; `NOTE_DUPLICATE_DISPATCH` at `classify.py:76`, used at :898; `probes.py:435` reads `dispatchId`). Claims are true; citations are ADJ's |
| M10 | SW-04 runs-in | #541's branch, marked UNVERIFIED, is `fix/claude-md-worktree-rule-test` (`gh pr view 541`) |

## Confidence

- Checklist items: 7 lead checks + 1 contract check (SEED 1-12 and plan A1-A15) = 8. VERIFIED 8, UNVERIFIABLE 0, UNCHECKED 0.
- **Confidence:** Verified: 8/8 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- Sub-item not verifiable under the GET-only rule: whether the #539 Augment and Codex threads are still unresolved (needs GraphQL); thread anchors were verified.
- **Tool engagement:** Read: 15 | Grep: 4 | Glob: 0 | Bash: 7 (two mechanical batch scripts, one Python edge-table parser, one fact batch, one gh GET call set, two ADJ/WORKER-CONTRACT reads). No web research.
- Not done: did not read `merge-log.md`; did not re-run plan check A14 (b), (c) exhaustively (sampled); did not open V2/V3 variants.

## QA Complete

---

## Re-review 2 (after fix cycle 1; review 2 of max 3)

**Date:** 2026-11-13. **Input:** `merged-spec.md` (1347 lines). I read the merge-log FIX CYCLE 1 entries (lines 694-732) as claims only and checked each one myself.

### Verdict: PASS (with notes)

0 blocking findings open. B1 and B2 are fixed. 2 new minor notes (R2-N1, R2-N2). The earlier minor notes M2, M3, M5 and M6 are still open by design; under the severity rule they are not rechecked. Monotonicity: open blocking findings went from 2 to 0.

### Method

I wrote a new parser and ran it once (`uv run python -I` in a private `/tmp/ironclaude-batch.*` folder, removed by trap). It finds section 2, section 3 and 4.2 by heading rather than fixed line ranges. It builds the **full** graph from the edge table, with every Q, K, TB, gate and GRANT node counted as a node. On that graph it runs cycle detection, a wave-direction check that follows paths through gate nodes, endpoint validation against the action vocabulary it reads from 4.1, a 4.1-versus-6.8 vocabulary comparison, and a comparison of the section 2 cells with the edges. I also ran one grep batch over the changed lines, and I reused the Grep and `gh` outputs from review 1 for the citation facts.

### B1: TB-GIT gate cycle. FIXED

| Check | Evidence | Result |
|---|---|---|
| Full graph has no cycle | parser: 145 nodes, 308 hard From-To pairs, **0 cycles** | PASS |
| SW-01's only predecessor is the owner | parser, predecessors of SW-01 in every edge kind: `Q1`, `TB-EDIT` (PROC, the version-checked-edit rule), and `GRANT(SW-01,thread-reply)` / `GRANT(SW-01,thread-resolve)`, which apply only when someone other than the owner acts (edge 3, line 650). All of these are owner decisions or process rules; no work item and no TB-GIT. SW-01 blocked-by cell (line 190): "Q1 only (the owner); ... the ruling decides TB-GIT's scope and never waits for it" | PASS |
| TB-GIT gates SW-05 and sweep runs, not SW-01 | TB-GIT predecessors {SW-01, SW-02} (edge 2, line 649); successors {SW-05 (edge 15), XC-04 (edge 106)}. 4.1 TB-GIT row (line 630) cites edge row 2. 4.4 line 792 `{SW-01, SW-02} -> TB-GIT -> {SW-05, XC-04}` | PASS |
| 4.3 graph checks now true | item 2 (line 777) "No cycle, gate nodes included"; item 3 (line 778) "SW-01 ... waits for the owner (Q1) only" | PASS |
| Wave table consistent | SW-01 W0 and SW-02 W1 -> TB-GIT -> SW-05 W2 and XC-04 W3. Following paths through gate nodes finds 0 backward edges | PASS |

### B2: per-action grants on PR #539. FIXED

| Check | Evidence | Result |
|---|---|---|
| `push` and `thread-resolve` in the vocabulary | 4.1 GRANT line (607) lists 11 actions incl. `push` and `thread-resolve`; parser: the 6.8 action set (line 1047) equals the 4.1 set exactly | PASS |
| Every hand push on #539 has its own GRANT edge | push GRANT edges go to SW-02 (edge 8), SW-03 (edge 10) and SW-05 (edge 17). The same grants appear in each item's blocked-by cell and in its acceptance text (SW-03 (5), SW-05 (1)) | PASS |
| Every thread resolve has its own GRANT edge | `GRANT(SW-03,thread-resolve)` (edge 10; SW-03 (4)) and `GRANT(SW-01,thread-resolve)` (edge 3, when not the owner) | PASS |
| No other item pushes or resolves on #539 by hand | grep of the SW rows and of 6.3/6.4: SW-05 (6) pr-submit is under its existing `pr-submit` row; there are no other hand pushes | PASS (see R2-N1 for `update-branch`) |
| No grant widened; merge separate | parser: every GRANT edge's item equals its edge target (0 mismatches); merge grants stay separate (11 items, each its own row); 6.8 (line 1047): "A push grant satisfies neither a merge, an issue write, a thread resolve nor a live test", and a `push` row and a `pr-submit` row do not satisfy each other; 6.4 rule 2 (line 975): "naming the #539 author (Q33) is not a grant" | PASS |

### Re-run of mechanical checks 1 and 2

| Check | Result |
|---|---|
| Ids defined | 50 unique (SW 14, OB 9, WA 7, CO 4, V2 5, XC 11), no duplicate rows |
| Used minus defined (outside the id map and comments) | empty |
| Edge rows | 124, numbered 1-124 with no gaps; 319 From-To pairs; **0 undefined endpoints** (actions validated against the 11-action list) |
| Graph coverage | all 50 items appear in the edge table |
| New edge 124 `XC-08 -> V2-01, OB-09` | XC-08 is in W1, and V2-01 (W3) and OB-09 (W5) are later: no backward edge |
| Wave placement and direction | all 50 placed; XC-11 in W3 and W5 by design; 0 backward hard edges, including paths through gate nodes |

### Spot checks of 10 changed claims

| # | Claim (spec line) | Evidence | Result |
|---|---|---|---|
| 1 | M1: SW-05 blocks cell now has SW-11, SW-14, XC-04, XC-06, SWEEP-RUNNABLE (194) | cell text | CONFIRMED |
| 2 | M1: SW-07 blocks XC-07, and XC-07's blocked-by has SW-07 (196, 455) | cell text; edge 114 | CONFIRMED |
| 3 | M1: OB-08 and V2-03 blocked-by cells have XC-08 (256, 400) | cell text; edges 54, 91 | CONFIRMED |
| 4 | M1: 5.1 W2 gate for OB-08 has XC-08 | "OB-08 needs CO-01 posted, OB-01, OB-02, XC-08, Q8, Q16" | CONFIRMED |
| 5 | M4: 6.1 Live state uses `gh pr view <N> --repo IronbellyOrg/IronClaude` (947) | line text | CONFIRMED |
| 6 | M8: 7.4 item 1 lists SW-14, OB-09, WA-07, XC-04, XC-11 (1168) | line text; matches 5.2's 17 items | CONFIRMED |
| 7 | M9: mode 0600 at `export.py:260` (237) | review-1 Grep: line 260 "mode 0600" | CONFIRMED |
| 8 | M9: `NOTE_DUPLICATE_DISPATCH` defined at `classify.py:76`, used at `:898` (452) | review-1 Grep: 76 definition, 898 `forced.insert(0, NOTE_DUPLICATE_DISPATCH)` | CONFIRMED |
| 9 | M9: `probes.py:435` reads `dispatchId`; join basis is `classify.py:891` (436) | review-1 batch f11 and Grep | CONFIRMED |
| 10 | M10: #541 branch `fix/claude-md-worktree-rule-test` (193) | review-1 `gh pr view 541 --json headRefName` | CONFIRMED |

Also confirmed: M7 (4.3 item 4, line 779, "XC-07 feeds K-NOTE, OB-09 and XC-11").

### New issues introduced by the fixes

| # | Severity | Location | Note |
|---|---|---|---|
| R2-N1 | MINOR (Medium: a real but non-blocking weakness; follow-up candidate) | SW-05 (1) (line 194); 2.1 (175); 6.5 CI row (1005) | SW-05 (1) still offers "or update-branch is used" as the alternative to a hand push. An update-branch is an outward write to the #539 branch, but no grant action covers it: 6.8 scopes a `push` row to "a hand push outside `/sc:pr-submit`". 6.4 rule 2's general rule (every outward action needs its own grant) still applies, so a session would have to ask the owner; it would not act. Fix: say that update-branch on #539 counts as `push` under `GRANT(SW-05,push)`, or drop the alternative. |
| R2-N2 | MINOR | V2-01 blocked-by (398), OB-09 blocked-by (257) | New edge 124 `XC-08 -> V2-01, OB-09` is in XC-08's blocks cell but not in the blocked-by cells of V2-01 or OB-09. Wave order is safe (W1 before W3/W5), and 4.2 is authoritative. |

The parser found no other new contradictions and no new dangling ids. Its remaining cell-versus-edge differences are SOFT edges (XC-03 ~>, V2-05 ~>, XC-07 ~> V2-03, WA-01/CO-01 ~> V2-01), the generic rows 119/122 (XC-09, XC-11), and parenthetical text the parser strips (OB-06 "(no XC-05 edge ...)").

### Confidence (re-review)

- Checklist: B1, B2, mechanical 1, mechanical 2, spot checks, new-defect scan = 6 items. VERIFIED 6, UNVERIFIABLE 0, UNCHECKED 0. **Confidence:** Verified: 6/6 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement (re-review):** Read: 2 | Grep: 1 | Glob: 0 | Bash: 3 (one Python graph parser, two grep batches). No web research; no write other than this section.

## Re-review 2 complete
