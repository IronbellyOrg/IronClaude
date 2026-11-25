# Research Completeness Verification (Gate 1)

**Topic:** IronClaude issue-to-work pipeline technical reference
**Analysis type:** completeness-verification
**Date:** 2026-11-20
**Depth tier:** Standard
**Fix authorization:** false (report only)
**Status:** Complete

---

**Files analyzed:** 6 research files (`research/01` to `research/06`, 3,021 lines in total per `phase-outputs/reports/phase-2-output-summary.md`), plus `research-notes.md` and the Phase 2 aggregation. No `gap-fill-*.md` file exists.
**Verdict:** stated once, in the last section of this report (the `## Verdict:` line).
**Source safety:** the snapshot `/home/coder/.cache/ic-snap-20261120/master` was read only (Read, Grep and read-only Bash `sed`/`grep`/`wc`/`ls`/`diff`/`git show`). Nothing was written there, no probe file, and no script was written to `/tmp` or elsewhere. The only file written is this report.
**Adversarial stance:** treated as a stance, not a quota. Every finding below is evidenced; severity BLOCKING is reserved for a missing required deliverable, a missing scope item, or a false claim.

---

## 1. Method

1. Read `research-notes.md` (EXISTING_FILES, SUGGESTED_PHASES, RECOMMENDED_OUTPUTS) and the Phase 2 aggregation.
2. Read all six research files completely (every line, in pages).
3. Re-read live snapshot source for 60+ citations (section 4) and re-counted 42 test files (lines and `def test_` counts, section 4.2).
4. Checked the eight known staleness warnings (section 3), per-file completeness and per-area deliverables (section 5), cross-references (section 6), then compiled gaps (section 7).

## 2. Coverage audit (checklist item 1): file -> research file -> covered

R01 = `research/01-watcher-decision-engine.md`, R02 = `02-watcher-io-github-launch-record.md`, R03 = `03-watcher-operator-surface-and-setup.md`, R04 = `04-claim-flow-and-orca-worktree.md`, R05 = `05-guard-stack-and-ccsession.md`, R06 = `06-coordinator-text-and-removed-code.md`. "yes (partial)" means the file is read and used, but a named part is only touched (see findings).

### 2.1 Watcher package and design docs

| Scope item (research-notes EXISTING_FILES) | Covered by | Covered |
|---|---|---|
| `issue_watch/cycle.py` (config 34-483, cycle 485-1222, status/SLO 1225-1406) | R01 (cycle), R03 (config, status, SLO) | yes |
| `issue_watch/github.py` | R02 sec 1 | yes |
| `issue_watch/record.py` | R02 sec 3, 5 | yes |
| `issue_watch/launch.py` | R02 sec 2 | yes |
| `issue_watch/predicates.py` | R01 sec 6 | yes |
| `issue_watch/audit.py` | R01 sec 7, 8 | yes |
| `issue_watch/cli.py` | R03 sec A | yes |
| `issue_watch/runner.py` | R02 sec 4 | yes |
| `cli/main.py:577-579` registration | R03 A.1 | yes |
| `docs/designs/issue-watcher.md` | R01 (sec 4.3, 6-8, 10.1, 14), R02 (sec 7, 8), R03 (sec 4, 7, 10, 14, 18) | yes (partial: sec 2, 3, 5, 9, 11-13, 15-17 unassigned, finding F-02) |
| `docs/designs/issue-watcher-setup.md` | R03 E.7 (every section 0-16), R02, R06 | yes |
| `docs/user-guide/cli-groups.md` | R03 E.8 | yes |

### 2.2 Claim flow

| Scope item | Covered by | Covered |
|---|---|---|
| `commands/issue.md` | R04 sec 1 | yes |
| `skills/sc-issue-protocol/SKILL.md` | R04 sec 2 | yes (return-contract field names not listed, F-01) |
| `refs/claim.md`, `create.md`, `chains.md`, `tiers.md`, `labels.md` | R04 sec 2, 3, 4, 5 | yes |
| `scripts/orca_worktree.py` (1906 lines, 5 subcommands) | R04 sec 8 (all ranges) | yes |
| `scripts/clickup_claim.py`, `origin_repo.py` | R04 sec 6 | yes |
| `templates/` (15 files, not 17) | R04 sec 7 | yes (R04 correctly corrects the brief's "17"; I counted 15) |
| `agents/issue-worker-t1/t2/t3.md` | R04 sec 3 | yes |
| `docs/designs/sc-issue-command.md`, `sc-issue-claim-pipeline-flag.md` | R04 sec 15 | yes |

### 2.3 Guard stack, ccsession, coordinator, removed code

| Scope item | Covered by | Covered |
|---|---|---|
| `hooks/scripts/launch-level-guard.sh` (808) | R05 sec 1, observation run (44 payloads) | yes |
| `launch-job-identity.sh` (582) | R05 sec 2 | yes |
| `launch-level-pre-push.sh` (208) | R05 sec 3 | yes |
| `hooks/hooks.json`, `cli/install_hooks.py` | R05 sec 4 | yes |
| `cli/install_ccsession.py` | R05 sec 5.1 | yes |
| `skills/ccsession-tag/ccsession-orca`, hooks, `unseed-env.py`, `ccsession` | R05 sec 5.2 (ccsession-orca read in full; the rest by whole-directory grep and test names) | yes (partial, F-08) |
| `docs/designs/sc-issue-launch-level-hook.md`, `issue-pipeline-guard-g2.md`, `issue-pipeline-guard-g2-no-to.md`, `issue-pipeline-fu1.md` | R05 Gaps table (24 rows), R06 A4 | yes |
| `core/WORKER-CONTRACT.md` (339 lines, WC-2..WC-16, no WC-17) | R06 A1, A2 | yes |
| `docs/architecture/SUPERVISED-ORCHESTRATION-TECHNICAL-REFERENCE.md` l.151-290, 1052-1145 | R06 A2 | yes |
| Removed `issue_pipeline/` package (10 files, 10 verbs, 1,597 lines), WC-17, "Issue pipeline duties", guard rule 1, 116 tests + registration test | R06 Part B (B1-B16) | yes |

### 2.4 Every test file listed in research-notes

| Test file | Row in | Covered |
|---|---|---|
| `tests/issue_watch/test_cycle.py`, `test_predicates.py`, `test_audit.py`, `test_marker_contract.py`, `conftest.py` | R01 sec 11 (5 rows) | yes |
| `tests/issue_watch/test_github.py`, `test_launch.py`, `test_record.py`, `test_concurrency.py`, `test_crash_injection.py`, `test_find_orca_parity.py`, `test_origin_parity.py`, `test_runner.py`, `fixtures/_assumed_shape/` (19 files) | R02 sec 7(a), sec 6 | yes |
| `tests/issue_watch/test_cli.py`, `test_cli_e2e.py`, `test_slo_helper.py`, `test_no_shell.py`, `test_no_text.py`, `test_security_invariants.py`, `test_module_boundaries.py` | R03 (a) (7 rows) | yes |
| `tests/skills/test_issue_protocol.py`, `test_issue_orca_worktree.py`, `test_issue_repo_resolution.py`, `test_issue_worker_agents.py`, `test_issue_t1_fallback.py`, `test_issue_l2_install.py`; `tests/commands/test_issue_command.py`; `tests/cli/test_issue_body_templates.py` | R04 sec 14 (8 rows) | yes |
| `tests/hooks/test_launch_level_guard.py`, `_l2_tokens`, `_registration`, `_with_identity`, `_worker`, `test_launch_job_identity.py`, `test_launch_level_pre_push.py`, `_pre_push_records`, `test_launch_level_observations.py` | R05 sec 11.1 | yes |
| `tests/cli/test_install_hooks.py`, `tests/unit/test_install_ccsession.py`, `test_ccsession_tag.py`, `test_ccsession_tiers.py`, `tests/core/test_orca_session_launch_guidance.py` | R05 sec 11.1 | yes |
| `tests/skills/test_worker_contract.py`; `tests/hooks/test_launch_level_guard_worker.py` (current and at `01e7a9e23^`); removed `tests/issue_pipeline/` (10 files); `tests/cli/test_issue_pipeline_registered.py` | R06 A3, B10 | yes |

Result: `ls tests/issue_watch` shows 20 `.py` files (plus `__init__.py` and `fixtures/`); all 20 have a row. `ls tests/hooks | grep -i launch` shows 9 files; all 9 have a row. Coverage: 100 percent of the listed key files and test files; two partial notes (F-02, F-08), neither a missing scope item.

## 3. Documentation staleness (checklist item 3): the eight known warnings

"Mine" = what I re-checked against the snapshot in this run.

| # | Known warning | Where confirmed or refuted in research | Verdict in research | My re-check | Status |
|---|---|---|---|---|---|
| 1 | `issue-watcher.md` skew 300 s vs `SKEW_WARN_S` 60 | R01 sec 17 row 22 and Gaps 7; R03 E.5 and Gap 1 | confirmed with a refinement: 300 is `predicates.SKEW_TOLERANCE_S` (marker window), the warning is 60 | `cycle.py:44` = 60, `predicates.py:17` = 300, `cycle.py:774` `skew > SKEW_WARN_S`; `issue-watcher.md:827` row reads "skew tolerance / 300 s / equals the cadence"; `:510` says 60 | confirmed; tags disagree between files (F-03) |
| 2 | Dead `MAX_LAUNCHES_PER_CYCLE` | R01 sec 1 and DC-1; R02 D-2; R03 B.8 | dead constant, S1 halt does the job | `grep` over `src` and `tests`: one hit, `cycle.py:35`; `orchestrator.md:368` also shows it as "(35)" (R02 Gap 11) | confirmed |
| 3a | Setup doc cites a non-existent WORKER-CONTRACT section "Issue pipeline duties" | R03 E.7 (sec 6 row), Gap 4; R06 A4 | CODE-CONTRADICTED | current contract: `grep` for `WC-17` and `Issue pipeline duties` = no hit, WC-16 at l.287; old contract has them at l.59 and l.291 (`git show 01e7a9e23^`); `issue-watcher-setup.md:170` still names it | confirmed |
| 3b | Setup doc launch commands omit `--pipeline none` | R02 Gap 14; R03 E.7 (14.1.1 row), Gap 3 | CODE-CONTRADICTED (`launch.py:92` always adds it) | `issue-watcher-setup.md:616-619` show `--prompt '/sc:issue --claim <test issue>'` for all four Orca fixtures | confirmed |
| 3c | Setup doc has no dispatcher step | R03 E.7 (last row), F.2; R01 sec 12 item 14; R06 Gap 8 | "not found in snapshot" | `grep dispatcher|COORD-|zero-setup` in the setup doc: no hit; `COORD-` has no hit anywhere in the snapshot (see F-09 for one unrelated "zero setup" hit) | confirmed |
| 3d | Live-test doc `issue-watcher-live-test.md` absent | R01 sec 12 item 13, DC-5; R02 sec 6, N-3; R03 E.1, F.2 | NOT BUILT, absent | `ls docs/designs` only holds two `issue-watcher*` files | confirmed |
| 4 | FU-1 doc uses the removed command group | R03 E.7 sec 6 row, Gap 4; R05 Gaps 11; R06 A4, Stale | CODE-CONTRADICTED | `issue-pipeline-fu1.md:64` runs `superclaude issue-pipeline plan-hash` and `check-approval`; `issue_pipeline` absent in snapshot `cli/main.py` | confirmed |
| 5a | Guard-g2 doc line refs drifted | R05 Gaps 5, 6 | CODE-CONTRADICTED (lines only) | guard now has G2 rule 2 at l.496-537, orca allow-list l.480-491 (l.457 is `orca)`), vs doc `:471-474`, `:703`, "lines 500-549" | confirmed |
| 5b | Guard-g2 route A retired | R05 Gaps 8, ledger row "G2 rule 1 / route A"; R06 B12 | REMOVED | `grep release-worker` over src, tests, plugins: no file; old guard l.444 TAMPER case present at `01e7a9e23^` per R06 | confirmed |
| 5c | Nothing calls `orca_worktree.py pending` | R04 8.7 and Defect row 1; R05 sec 12, DC-1; R06 D3 | DEFECT CANDIDATE (verb built, no production caller) | `grep` over src, plugins, tests: definition and argparse only inside `orca_worktree.py` (l.8, 1488, 1515, 1518, 1893) and callers only in tests: `test_launch_level_guard_worker.py:287`, `test_issue_orca_worktree.py:2475-2498` | confirmed (R05 omits the `:287` caller, F-04) |
| 6 | Hook design IMPL skill list vs code `implement|task|cleanup` | R05 Gaps 1, sec 1.6 | CODE-CONTRADICTED | `launch-level-guard.sh:409` `implement | task | cleanup`; `sc-issue-launch-level-hook.md:106` and `:179` list `improve`, `spawn`, `build` | confirmed |
| 7a | `sc-issue-command.md` status "Design only" | R04 sec 15, Stale | CODE-CONTRADICTED | `sc-issue-command.md:3` "Status: Design only (nothing implemented)"; command, skill, scripts, agents, 109-test worktree suite exist | confirmed |
| 7b | T3 model pin (`claude-gw-tier3` in design) | R04 sec 3, 15, Stale | CODE-CONTRADICTED (`claude-gw-tier2b`) | `agents/issue-worker-t3.md:6` `model: claude-gw-tier2b`; `SKILL.md:58-62` table agrees; design lines 107, 129, 391, 423, 449 say `tier3` | confirmed |
| 7c | Pipeline-flag default level | R04 sec 4, 10, 15, Stale | design head text "default `worktree`" superseded by prose pick at `refs/claim.md:81` | `sc-issue-claim-pipeline-flag.md:21, :43` still lead with `worktree (default)`; `claim.md:81` rule (bug -> full, etc.) read | confirmed |
| 8 | ccsession shim does not carry the launch level | R05 sec 5.2 and Gaps 22; R04 8.8 item 5 | CODE-CONTRADICTED for the claim "shim carries the level"; level travels by files only | whole-directory `grep` in R05; `orca_worktree.py:792-800` constants read here: detection only | confirmed |

All eight warnings (14 sub-items) are confirmed in at least one research file, with a tag and evidence. None is left open. R04 and R05 add further staleness rows beyond the eight (plugin `hooks.json` has two more differences than the hint said; `launch-prompt.md:23` names `/sc:task` which guard l.347 does not accept; templates folder holds 15 files, not 17).

### 3.1 Tag discipline per file (counts from the Phase 2 aggregation, plus my reading)

Every doc-sourced claim I sampled in each file carries a tag or an explicit marker: R01 sec 17 (27 rows, all tagged), R02 Gaps 1-19 (tagged) and its Stale table, R03 sec E (all rows tagged), R04 sec 15 table and Stale list, R05 Gaps "Doc claims checked" (24 rows, CV/CC/UV), R06 A2 and Stale list. No `[CODE-CONTRADICTED]` item is stated as current fact anywhere: every one is paired with the code value. File 05 and 06 use extra verification words (`OBSERVED-BY-GREP`, `READ-ONLY-READING`) next to the three tags, as the aggregation notes; this is acceptable. Only the doc claims in unassigned design sections were never tagged because never read (F-02).

## 4. Evidence quality (checklist item 2)

### 4.1 Spot-check of citations against the live snapshot (target was 15; 38 are listed, more were read)

All read from `/home/coder/.cache/ic-snap-20261120/master`. Result column: OK = the research claim matches the live line.

| # | Research file and claim | Live source read | Result |
|---|---|---|---|
| 1 | R01 sec 1: `MAX_LAUNCHES_PER_CYCLE = 1` at cycle.py:35, no other hit | `grep` over `src` and `tests`: one hit, cycle.py:35 | OK |
| 2 | R01: `SKEW_WARN_S = 60` cycle.py:44; warning at 774 | cycle.py:44, 774 | OK |
| 3 | R01/R03: `SKEW_TOLERANCE_S = 300` predicates.py:17 | predicates.py:17 | OK |
| 4 | R01: `_PRECEDENCE = (2, 6, 7, 5, 3, 4)` cycle.py:462 | cycle.py:462 | OK |
| 5 | R01 sec 2: enabled gate at 685-686; S1 halt at 833-834; `launching` at 1028 | cycle.py:685-686, 833-834, 1028 | OK |
| 6 | R01 sec 3: gate order E1-E15 in `_examine` 915-961 (state skips, day cap, owner, marker, events, approval, edits, project, launch) | read cycle.py:915-961 in full | OK (order, line numbers and reasons match) |
| 7 | R01 sec 4: launch steps L0-L14 (`_launch` 1026-1112), `pending` saved at 1091-1092 before `launch` at 1099 | read cycle.py:1026-1112 in full | OK |
| 8 | R01 sec 8: `REASON_TABLE` has 59 entries | `grep -cE '^    "[a-z_-]+": \("'` audit.py = 59 | OK |
| 9 | R02: `REPO`, `CALL_CAP` 35, `RESERVED_CALLS` 3 at github.py:37, 46, 49; `PAGE_CAP` 43; `RATE_LIMIT_MAX_WAIT_S` 376; `DISCOVERY_BOUND` 486 | github.py lines | OK |
| 10 | R02: `PROMPT_PATTERN` launch.py:33; `build_claim_prompt` 84-92; 12-element argv 103-116 | launch.py lines read | OK (12 elements counted) |
| 11 | R02: `MAX_ATTEMPTS`, `BACKOFF`, `LEASE`, `DAY_CAP_WINDOW` at record.py:434-443; `disabled()` uses `lexists` 421-423 | record.py lines | OK |
| 12 | R03: cli.py consts 31, 34-38; group at 94; `_APPROVERS_MAX_BYTES` cycle.py:75; registration main.py:577-579 | cli.py, cycle.py, main.py lines | OK |
| 13 | R03 Gap 18: `reset --rate-limit --forfeit-guarantee` passes the argument checks and the flag is ignored | cli.py:309-313 (`by_issue == rate_limit` and `by_issue and not forfeit_guarantee` only) | OK |
| 14 | R03 C.1: `disabled_since()` uses `os.stat` (follows symlink), `disabled()` uses `lexists` | record.py:421-431 | OK |
| 15 | R04: `IR7_REFUSE = False` at orca_worktree.py:822; dead branch 1757-1758 | lines 822, 1757-1758 | OK |
| 16 | R04: shim constants 792, 797-800 (`SHIM_TRIES = 5`, interval 2.0) | lines 792, 797-800 | OK |
| 17 | R04: `publish_pending` 1488, `cmd_pending` 1515, `cmd_launch` 1696, `install_l2(wt)` 1754, `publish_pending(word)` 1761, marked prompt 1779 | lines 1488, 1515, 1696, 1754, 1761, 1779 | OK |
| 18 | R04: `pending` has no production caller; only test callers | `grep` over src, plugins, tests: def/argparse in `orca_worktree.py`; callers `test_launch_level_guard_worker.py:287`, `test_issue_orca_worktree.py:2475-2498` | OK (R05 lists a different subset, F-04) |
| 19 | R04: SKILL.md picker table (t3 tier2b, t2 tier2, t1 tier1b) l.58-62; write line l.74 | SKILL.md l.58-62, 74 | OK |
| 20 | R04: `agents/issue-worker-t3.md:6` `claude-gw-tier2b` | agents/issue-worker-t3.md:6 | OK |
| 21 | R04: templates folder holds 15 files, brief says 17 | `ls templates | wc -l` = 15 | OK (R04 right, research-notes wrong) |
| 22 | R04 sec 10: `refs/claim.md:81` level rule (explicit wins; unreadable -> worktree; ...) | claim.md:81 | OK |
| 23 | R04 sec 15: `launch-prompt.md:23` lists `/sc:task` as approving first line; guard regex only `sc:implement|task` | launch-prompt.md:23, guard :347 `^[[:space:]]*/(sc:implement|task)([[:space:]]|$)` | OK (real prompt/guard mismatch) |
| 24 | R05: guard marker regex l.318; `mv pending -> .take-` l.372-374; precedence loop l.783; IMPL case l.409 | guard lines read | OK |
| 25 | R05: `orca-ide` not recognised: guard case `orca)` at l.457 | guard l.452-461 | OK |
| 26 | R05: hooks.json guard matcher l.115-124 and identity l.125-134 (after the guard) | hooks.json l.115-134 | OK |
| 27 | R05: `install_hooks.py` `_FRESHNESS_SCRIPTS` lines 90, 93, 96; callers main.py:219, 412 | lines read | OK |
| 28 | R05: plugin `hooks.json` differs from src hooks.json | `diff` gives 42 changed lines | OK (consistent with "two more differences") |
| 29 | R06: WORKER-CONTRACT 339 lines; WC-16 at l.287; no WC-17, no "Issue pipeline duties"; issue lines 23, 57, 66 | `grep`, `sed`, `wc -l` | OK |
| 30 | R06: removed commit `01e7a9e23`, 27 files in `git ls-tree` of the three removed paths, `cli.py` 395 and `approval_record.py` 416 lines at `01e7a9e23^` | `git show`, `ls-tree`, `wc -l` | OK |
| 31 | R06: old contract has WC-17 at l.59 and "### Issue pipeline duties" at l.291 | `git show 01e7a9e23^:src/superclaude/core/WORKER-CONTRACT.md | grep -n` | OK |
| 32 | R06: commit time `2026-11-19 18:02 -0600`, "retire the old plan-approval gate (issue 655, PR D) (#682)" | `git show -s --format` | OK (date convention, F-05) |
| 33 | R02 D-1: `record.disabled_present` only in record.py:748 and test_record.py:861-870 | `grep` over `*.py` | OK |
| 34 | R02 D-3 / D-4: `LaunchOutcome.detail` and `launch_login`/`launch_account_id` have no reader in `src` | `grep` over `issue_watch` and `src` | OK |
| 35 | R01 DC-3: `slo_numbers` has no caller in `src` | `grep slo_numbers src`: definition cycle.py:1359 only | OK |
| 36 | R03/R04 stale docs: `issue-watcher-setup.md:170`, `:616-619`; `issue-pipeline-fu1.md:64`; `sc-issue-command.md:3, 107, 129, 449`; `sc-issue-claim-pipeline-flag.md:21, 43` | `sed`/`grep` on each | OK |
| 37 | R05 Gaps 1: design IMPL list `sc-issue-launch-level-hook.md:106, 179` | `sed` | OK |
| 38 | R02 Gap 11: `orchestrator.md:368` shows `MAX_LAUNCHES_PER_CYCLE (35)` | `sed -n 368p` | OK |

Failures: 0 of 38. No false claim found in any file.

### 4.2 Test-file line and test counts (42 files re-counted with `wc -l` and `grep -cE '^\s*(async )?def test_'`)

Every number in the test-pin tables of R01 to R05 that I re-counted matched exactly, including: test_cycle 4982/237, test_launch 952/66, test_record 2377/147, test_github 2161/141, test_cli 1672/60, test_launch_level_guard 4631/162, test_issue_orca_worktree 2501/109, test_worker_contract 3220/59, test_issue_protocol 1055/62, test_launch_job_identity 1530/56, test_launch_level_pre_push 1194/34, test_install_hooks 1246/37, test_ccsession_tag 7101/277, test_ccsession_tiers 3821/149, and the 28 smaller files (predicates 44, audit 46, marker 3, concurrency 6, crash 6, find_orca 10, origin 7, runner 16, cli_e2e 4, slo 14, no_shell 9, no_text 22, security 16, module_boundaries 13, repo_resolution 18, worker_agents 24, t1_fallback 8, l2_install 26, issue_command 15, body_templates 5, with_identity 5, worker 11, pre_push_records 8, observations 6, registration 7, l2_tokens 7, install_ccsession 22, orca_session_launch_guidance 3). Zero mismatches. Fixture count 19 matches `ls fixtures/_assumed_shape | wc -l`.

### 4.3 Evidenced versus unsupported claims (rating per file)

| Research file | Evidence style | Unsupported claims found | Rating |
|---|---|---|---|
| R01 | path:line for every row; `Grep` commands named | 0 (items it could not check are tagged [UNVERIFIED] in Gaps 9-13) | Strong |
| R02 | path:line, argv written out, `Grep` results quoted | 0 | Strong |
| R03 | path:line, three tags on every doc row (114 CODE-VERIFIED, 18 CODE-CONTRADICTED, 30 UNVERIFIED per aggregation) | 0 | Strong |
| R04 | path:line, wave tables, exact commands | 0 (templates `scout-report.md` and `recommend-record.md` bodies marked "Not read") | Strong |
| R05 | path:line, plus 44 observed guard payloads | 0 (identity and L2 runtime not run, stated) | Strong |
| R06 | path:line and `git show` output for the removed code | 0 (the three UNVERIFIED items name why) | Strong |

## 5. Completeness of each file and required per-area deliverables (checklist items 4 and 5)

### 5.1 Structure (item 4)

| Research file | `Status: Complete` | Summary | Gaps and Questions | Stale Documentation Found | Defect Candidates / Not-Built | Key Takeaways | Rating |
|---|---|---|---|---|---|---|---|
| R01 | yes (line 4) | yes (l.654-656) | yes (l.601) | yes (l.626) | yes (l.639, DC-1..DC-8) | yes, after sec 1 to 10; sec 11 to 17 are table deliverables and doc checks without their own takeaway lines (minor, F-10) | Complete |
| R02 | yes | yes (l.470) | yes (l.415, 19 items) | yes (l.437) | yes (l.452, D-1..D-4, N-1..N-7) | yes after every section 1-7 | Complete |
| R03 | yes | yes (l.494) | yes (l.445, 20 items) | yes (l.468) | yes (l.479, 10 rows) | yes for A-F; none after G and the deliverables block (minor, F-10) | Complete |
| R04 | yes | yes (l.494) | yes (l.446, 15 items) | yes (l.465) | yes (l.479, 8 rows) | yes (sections 1-8 individually; one combined block for 9-17) | Complete |
| R05 | yes | yes (l.499) | yes (l.434, 24 doc rows + 7 questions) | yes (l.475) | yes (l.484, DC-1..DC-9) | yes after sec 1-6, 10, 11; none after sec 12 and the observation run (minor, F-10) | Complete |
| R06 | yes | yes (l.396) | yes (l.359, 10 items) | yes (l.373) | yes (l.384, D1..D5) | yes after A1, A2, A3-A4, B1-B6, B7-B10, B11-B16 | Complete |

All six headers say `Status: Complete`. No file ends mid-section.

### 5.2 Per-area deliverables (item 5): (a) test-pin table, (b) live-vs-off line, (c) GitHub writes, (d) triggers, (e) state stores, (f) gates

| File | (a) one row per assigned test file | (b) status line with the four words | (c) writes-to-GitHub with exact commands or evidenced "no write" | (d) triggers | (e) state stores | (f) gates |
|---|---|---|---|---|---|---|
| R01 | 5 rows for 5 assigned (sec 11) | sec 12 (14 rows) | "No GitHub write in this area", 4-point evidence, 7 read argv listed (sec 13) | sec 14 (`once` only; no scheduler found) | sec 15 (8 rows) | sec 16 (37 gates) |
| R02 | 8 test files + fixtures dir (sec 7a) | sec 7b (16 rows) | sec 7c, same style, 7 read argv | sec 7d | sec 7e | sec 7f (27 rows) |
| R03 | 7 rows for 7 assigned | (b) 19 rows | (c) with the operator's own `gh label create` / `gh issue edit` commands listed separately | (d) | (e) and sec D | (f) 28 rows incl. prose-only gates |
| R04 | 8 rows for 8 assigned (sec 14) | sec 16 | sec 5a (claim: C1-C5), 5c (create: X1-X3), exact `gh` and ClickUp commands | sec 13 | sec 11 | sec 12 |
| R05 | 14 rows for the assigned test files (sec 11.1) + 16-cell level matrix with a test id per cell (sec 11.2) | sec 6 ledger (13 rows) | sec 7 "No GitHub write", per-script grep evidence | sec 8 | sec 9 | sec 10 (32 rows) |
| R06 | current + removed test tables (A3, B10) | B16 (b) | B16 (c): removed code reads only; no command line in the contract text ("no command line found") | B16 (d) | B16 (e) | B16 (f) 10 gates |

Findings against this table: none are missing. R05 Key Takeaways line says "16 test files" while its table has 14 rows (F-11). Status words are extended in several files beyond the four allowed ("BUILT as prose only", "BUILT-ON, claim-installed only", "RETIRED by design", "BUILT-ON as code but dead"); the four words are always present as the head word, so this needs only normalising at assembly (F-07).

### 5.3 Does each area answer the lead's seven required questions

| Question | Where answered |
|---|---|
| What GitHub writes exist, with exact commands | R04 sec 5a (assign, two comments, ClickUp PUT; `gh issue edit`, `gh issue comment`, `gh api -X PATCH`), 5c (create path); R01/R02/R03 "no write" for the watcher; R05/R06 "no write" |
| What triggers each piece | R01 sec 14, R02 (d), R03 (d) and F.2 (negative search results), R04 sec 13, R05 sec 8, R06 (d); "no trigger found in snapshot" is used where nothing exists |
| State stores | R01 sec 15, R02 3.1/(e), R03 sec D, R04 sec 11, R05 sec 9, R06 (e) |
| Gates | each file's (f) |
| Live versus off | each file's (b); `enabled: false` and no scheduler decided in R01 sec 12 and R03 F.2 |
| Test files | section 2.4 above |
| What is not built or removed | R01 DC-1..8, R02 N-1..7, R03 rows 1-10, R04 rows 1-8, R05 DC-1..9, R06 D1-D5 |

## 6. Cross-reference check and contradictions (checklist item 6)

### 6.1 Topics covered by several agents

| Topic | Files | Consistent? | Notes |
|---|---|---|---|
| Who reads or writes `dispatch.json` | R01 sec 15, R02 sec 5, R03 sec D, R06 B14 (old coordinator reads) | yes | all state: only `issue_watch` (cycle, cli, record) touches it; `status` is the lock-free reader; R02 also finds the docs-only `slo_numbers` snippet and the unbuilt wake-routing design in `orchestrator.md:115, 358`; R06 describes the removed coordinator reading it read-only (historical) |
| Shim detection (`W-LAUNCH-NOT-CCSESSION`) | R04 8.4, 8.7, 8.8; R05 sec 5.2, 5.3 | yes | same constants (`SHIM_MARKERS`, `SHIM_TITLE`, 5 tries, 2.0 s), same finding "detection only, level travels by files" |
| `install_l2` | R04 8.6; R05 5.4, sec 12 | yes | single caller `orca_worktree.py:1754`; both say the hook goes into `<git-common-dir>/hooks/pre-push`; R04 records the "worktree's pre-push" wording as stale, R05 repeats the correct path |
| `pending` / `publish_pending` | R04 8.7, 8.8, Defect 1; R05 sec 8, 9, 12, DC-1; R06 D3, D4 | yes in substance | R05's grep result omits `tests/hooks/test_launch_level_guard_worker.py:287` (F-04) |
| WC-17 and "Issue pipeline duties" | R03 E.1, E.7, Gap 4; R05 Gaps 7; R06 A1, A4, B11 | yes | all say removed; R06 gives old text and line numbers; the surviving no-`--to` bullet is at contract l.66 in R05 and R06 |
| 35-call GitHub budget and the 37 worst case | R01 sec 5, R02 1.6, R03 E.5 | yes | R03 E.7 row "13" leaves "37 vs cap 35" as [UNVERIFIED: owned by research 02]; R02 1.6 resolves it (35 per-issue + 2 shared = 37) (F-12) |
| `enabled` default false and "BUILT-OFF" | R01 sec 10, 12; R02 7b; R03 (b) F.2; R06 B16 | yes | one value (`cycle.py:228`), one gate (`:685-686`) |
| No scheduler, dispatcher, `COORD-`, zero-setup install | R01 sec 12 items 12, 14; R02 (d); R03 F.2; R06 Gaps 8 | yes | all write "not found in snapshot"; none cites the owner's chat notes as fact (rule in the brief respected) |
| Watcher launch prompt carries `--pipeline none` | R01 sec 17 row 26, R02 2.2, R03 E.1, R04 sec 13 | yes | `launch.py:33, 92`; doc rows that omit it: `issue-watcher.md:15, 41`, `issue-watcher-setup.md:616-619` |
| `status` health and exit 1 forever while `enabled: false` | R01 (health stamp), R03 C.1 | yes | |
| Level and guard classes | R04 8.8, 10; R05 1.5, 11.2 | yes | R04 flags the `/sc:task` prompt/guard mismatch; R05 independently shows the regex without `sc:task` |

### 6.2 Contradictions between research files

No hard contradiction of fact exists between two research files. The soft ones:

1. **Tag disagreement on one doc row** (F-03): `issue-watcher.md:827` "skew tolerance 300 s": R01 sec 17 row 22 says `[CODE-VERIFIED]` (number matches `predicates.SKEW_TOLERANCE_S`), R01 Gaps 7 and Stale list say `[CODE-CONTRADICTED, refined]` and "ambiguous", R03 E.5 and Gap 1 say flatly `[CODE-CONTRADICTED]`. Same facts, three labels.
2. **`pending` caller list** (F-04): R04 names `tests/hooks/test_launch_level_guard_worker.py:287` as the only caller and quotes the test at :273; R05 sec 12 reports one docstring hit at `test_launch_level_guard.py:165` and the `test_issue_orca_worktree.py` pins, and does not mention the `:287` call. I confirmed R04 by `grep`.
3. **Date of the removal** (F-05): R06 B16 says commit `01e7a9e23` was made 2026-11-19 18:02 -0600; research-notes and the task wording say "Removed on 2026-11-20". Both are right in different zones (00:02 UTC on 2026-11-20).
4. **Count of test files in R05**: Key Takeaways says 16, the table has 14 rows (F-11).
5. **"No hit" breadth in R01 sec 12 item 14**: says the search for `zero-setup|zero setup` over `src, docs, plugins, scripts, .github` finds nothing; one unrelated hit exists at `docs/swarm/user-guide.md:35` ("with zero setup", a swarm sentence). The conclusion (nothing about an issue-pipeline zero-setup watcher) stands (F-09).

## 7. Compiled gaps and findings (checklist item 7)

Gaps from all six files were merged and de-duplicated. The research files' own gaps fall in three groups, none of which blocks synthesis:

- **Evidence limits that cannot be closed from a read-only snapshot** (all labelled [UNVERIFIED] and carried to Section 14 of the final document as the research notes require): no live-test record and all 19 `_assumed_shape` fixtures unconfirmed (R01 Gaps 10-11, R02 Gaps 1-2, R03 Gaps 11-16); PR numbers #447, #448, #425, #394, #441, #442 and "never run live" cannot be checked (R01 Gap 9, R03 Gap 11, R04 Gap 12); whether any host runs `issue-watch once`, sets `enabled: true`, or runs a coordinator (R01 Gap 12, R02 Gap 3, R03 Gap 13); OB-H1..3 and OB-CTX not run, 12 skipped tests (R05); identity hook and L2 hook not executed (R05 "Not run"); tests read by name and header, none run (R01 Gap 17, R02 Gap 6, R04 Gap 10, R05 sec 11).
- **Open owner questions** (not defects of the research): R01 Gaps 14-16, R02 Gaps 7-10, R03 Gaps 17-20, R04 Gaps 4-6 and 14-15, R05 questions 1-7, R06 Gaps 9-10. They belong in the document's Section 14 or an open-questions list.
- **Defect candidates and not-built capabilities** (R01 DC-1..8, R02 D-1..4 and N-1..7, R03 rows 1-10, R04 rows 1-8, R05 DC-1..9, R06 D1-D5): complete, with evidence and recorded-decision column. The distinct set, de-duplicated across files, is: dead `MAX_LAUNCHES_PER_CYCLE`; `status` does not read `audit.jsonl` and `slo_numbers` has no caller; `LaunchOutcome.detail`, `launch_login`, `launch_account_id` written but never read; `record.disabled_present` dead; no scheduler; no live-test record; `agent-work-report` reads `orchestrator_repo` from a config whose validator rejects the key; `orca_worktree.py pending` has no production caller; IR-7 refusal off; IR-3 `pipeline.json` not built; default `--pipeline` pick and the OB-H ship gate prose only; coordinator hand-off after a `none` claim, release verb, brief builder and launch marker for coordinator-started workers unbuilt; guard does not recognise `orca-ide` (observed); `launch-prompt.md:23` names `/sc:task` which the guard does not accept; removed plan-approval gate with five duties unreplaced.

### 7.1 Findings table

Severity rule: BLOCKING = a required deliverable or a scope item is missing, or a claim is false. MINOR = accuracy, consistency or presentation issue that the assembler can fix from information already in the research files or the snapshot.

| ID | Severity | Research file and section | Gap or error | Evidence | Remediation |
|---|---|---|---|---|---|
| F-01 | MINOR | R04 sec 2 ("return contract :105-150") | The skill's return contract is named but its field list is not written out: only counts (9 base, 10 claim, 3 create fields). The brief lists "return contract" for area 04, and Section 8 (API and Integration) of the final document will want the names. | `SKILL.md:107-150` holds the three YAML blocks (`status, mode, issue_number, issue_url, dir, clickup_status, labels_applied, labels_missing, next_steps_path`; claim adds `pipeline_level, submit, worktree_status, worktree_path, worktree_branch, worktree_match_key, worktree_warning, launch_status, launch_warning, enforcement_hook`; create adds `issue_type, complexity_field, classification_missing`) and the `--pipeline none` rule that `worktree_status` is `not_requested` and `launch_status` is `not_requested`. The counts in R04 are right. | Have the Section 8 writer copy the three field lists and the `none` semantics from `SKILL.md:105-150` (re-read live), or add a short return-contract table to R04. |
| F-02 | MINOR | R01, R03 (design-doc sections not assigned) | `docs/designs/issue-watcher.md` sections 2, 3, 5, 9, 11, 12, 13, 15, 16, 17 were not doc-checked against code by anyone, so the final contradiction table would be silent on them. Sampling shows real drift. | `issue-watcher.md:772` and `:787` list `tests/issue_watch/stubs/gh` and `stubs/orca` (dir does not exist; `ls tests/issue_watch` shows `fixtures/` only; the PATH stubs come from the `stub_path` fixture, `conftest.py:1108`, per R01 sec 11); `:766` says "six verbs" (rows `reset <N>` and `reset --rate-limit` are one verb; code has five, `test_cli.py:279`); `:767` says main.py "two lines after line 561" (live: `main.py:577-579`; R03 records the same drift only for two other docs). Section 9.1 T1-T17 control table maps threats to tests that R02/R03 do cover. | Add one row group to the contradiction table (synth-06) for these three items and state that sections 2, 3, 5, 9, 11-13, 15-17 were only sampled. Optional: a 30-line doc-check pass over those sections by the R03 agent. |
| F-03 | MINOR | R01 sec 17 row 22, R01 Gaps 7, R03 E.5 and Gap 1 | One doc row carries three different tags (`[CODE-VERIFIED]`, `[CODE-CONTRADICTED, refined]`, `[CODE-CONTRADICTED]`). | `issue-watcher.md:827` "skew tolerance 300 s, equals the cadence"; `predicates.py:17` `SKEW_TOLERANCE_S = 300` (used by the claim-marker window, `marker_in_window`, `predicates.py:274-296` per R01); `cycle.py:44` `SKEW_WARN_S = 60`; the same doc says 60 at `:510`. | Assembler uses one ruling: "[CODE-CONTRADICTED as labelled]: 300 s is the claim-marker window (`predicates.SKEW_TOLERANCE_S`); the clock-skew warning is 60 s (`cycle.py:44, 774`, doc 7.5 `:510`); the defaults-table label 'skew tolerance' is ambiguous". |
| F-04 | MINOR | R05 sec 12 row 1 and DC-1 | The `pending` caller search lists a docstring hit and the `test_issue_orca_worktree.py` pins but omits the test that runs it for the guard chain. R04 has it right. | `tests/hooks/test_launch_level_guard_worker.py:287` runs `[sys.executable, str(SCRIPT), "pending", "--level", "worktree"]` (verified by `grep`); R05's regex did not match that argv form. | State in the final document: "no production caller; test callers are `test_launch_level_guard_worker.py:287` and `test_issue_orca_worktree.py:2475-2498`" (R04 8.7). |
| F-05 | MINOR | R06 B16 (b) versus research-notes appendix title | Removal date appears as 2026-11-19 (R06, git local time) and 2026-11-20 (research-notes). | `git show -s --format=%ci 01e7a9e23` = `2026-11-19 18:02:35 -0600`, which is 00:02 UTC on 2026-11-20. | Write "2026-11-19 18:02 -0600 (2026-11-20 UTC), PR #682" once, and use it everywhere. |
| F-06 | MINOR | `research-notes.md` EXISTING_FILES (planning input, not a research file) | Two numbers there are wrong; no research file repeats them. If an assembler copies from research-notes it would publish false values. | Templates folder: `ls | wc -l` = 15, not 17 (R04 sec 7 right). Watcher package: line counts `1406+960+865+370+312+404+348+130 = 4,795`, not "4,389" (`wc -l` of the eight modules; `__init__.py` is empty). | Synth agents take counts from the research files or re-run `wc -l`; do not copy "4,389" or "17 templates". |
| F-07 | MINOR | R02 7b, R04 sec 16, R05 sec 6, R06 D5 | Status words go beyond the four: "BUILT as prose only", "BUILT-ON but conditional on env", "BUILT-ON, claim-installed only", "BUILT-OFF (constant, not enabled:false)", "BUILT-ON as code but dead", "RETIRED by design". | The brief fixes BUILT-ON / BUILT-OFF (enabled:false) / NOT BUILT / REMOVED. | In the ledger use one of the four words and put the qualifier in an "evidence" or "note" column (for example `IR7_REFUSE = False` is BUILT-OFF with the note "constant, not config"). |
| F-08 | MINOR | R05 sec 5 | `skills/ccsession-tag` files other than `ccsession-orca` and `session-start.sh` get little text: the `ccsession` wrapper body, `hooks/session-name.sh` and `unseed-env.py` appear only as registered or invoked names and through test names; the key fact (no launch level anywhere in the directory) is established by a whole-directory `grep`. | R05 5.1-5.2; Gaps 7 (session-start.sh read, bare `python3`); R05 sec 11 row for `test_ccsession_tag.py` | Final document should describe the shim by `ccsession-orca` (read in full) and the grep result, and not describe the other files beyond one line. No new reading required. |
| F-09 | MINOR | R01 sec 12 item 14 | Negative search claim is slightly broader than the result. | `grep -i "zero-setup|zero setup"` over the snapshot has one hit: `docs/swarm/user-guide.md:35` ("with zero setup", unrelated). `COORD-` has no hit. | Word it "no hit relating to the issue pipeline"; keep "not found in snapshot" for `COORD-`, dispatcher, zero-setup watcher. |
| F-10 | MINOR | R03 sec G and deliverables block; R05 sec 12 and observation run; R01 sec 11-17 | Some sections end without a Key Takeaways line. Content is complete. | read | None required; the assembler writes its own takeaways. |
| F-11 | MINOR | R05 sec 11 Key Takeaways | Says "16 test files plus claim-side pins" but the table in 11.1 has 14 rows (14 files plus the claim-side list in a note). | R05 11.1 | Use 14 in the final matrix. |
| F-12 | MINOR | R03 E.7 row for setup sec 13 | "at most 37 in a busy one" left [UNVERIFIED: owned by research 02]; R02 1.6 and R01 sec 5 verify it (35 per-issue cap plus 2 shared = 37; `github.py:46`, `cycle.py:580-585`). | R02 1.6, R01 sec 5 | Use R02/R01 and tag the setup-doc sentence [CODE-VERIFIED]. |

Count: 0 BLOCKING, 12 MINOR.

### 7.2 Why none of the twelve is BLOCKING

- Required deliverables (a) to (f) are present in all six files with evidence (section 5.2).
- Every scope item in the SUGGESTED_PHASES table is traced; the only items touched lightly (F-01 return-contract names, F-08 shim sibling files) are one-line details the assembler can complete from named line ranges.
- No claim I re-read was false (section 4.1: 0 of 38; section 4.2: 0 mismatches in 42 files).
- F-02 is a coverage hole in unassigned design sections, not in an assigned scope item.

## 8. Depth assessment (checklist item 8)

**Expected depth:** Standard tier, with the lead's cross-cutting additions (test files, triggers, state stores, gates, launch levels, guard layers, live-vs-off, GitHub writes). Standard expects file-level understanding with key function documentation; the lead asks for traced, not listed, items.

| Item class in scope | Traced or only listed? | Evidence |
|---|---|---|
| Public verbs: watcher 5 (`once`, `status`, `check-config`, `init-state`, `reset`); `orca_worktree.py` 5 (`preflight`, `worktree`, `prompt`, `launch`, `pending`); `launch-job-identity.sh` 5 subcommands; removed `issue-pipeline` 10 | traced (arguments, reads, writes, exit codes, behaviour) | R03 A.4-A.6; R04 8.1-8.9; R05 2.1; R06 B6 |
| GitHub-writing commands | traced with exact argv and actor and wave | R04 5a (C1-C5), 5c (X1-X3); "no write" proofs for watcher, guard, removed code by named greps |
| State files | traced (writer, readers, mode, format) | R01 sec 15, R02 3.1 and 5, R03 sec D, R04 sec 11, R05 sec 9, R06 (e) |
| Guard class words (18) and levels (W, WA, F, FS) | traced; 16-cell matrix with a test id per cell and an observed result per cell (44 payloads) | R05 1.2, 1.5, 11.2, observation run |
| Exit codes | traced: watcher 0/1/2/3/4/5/6/7/75 with precedence and per-reason source; `origin_repo.py` 1/3/4; `clickup_claim.py` 2; `orca_worktree.py` 0/2; guard 0/2; identity 0/2; L2 hook 0/1/2 | R01 8.5, R03 A.5, R04 9a, R05 1.1, 2, 3 |
| Closed vocabularies | traced: 59 reasons each with raise site; 13 STOP codes; 12 warning codes (8 + 4); 11 plan-hash refusal words (removed); 3 L2 words | R01 sec 8, R04 sec 9, R05 sec 3, R06 B2 |
| Transitions T-1..T-13 | traced one by one to function and caller | R02 3.4, R01 3.1 |
| Crash points C1-C5 and write-ahead order | traced and test-pinned | R02 3.5, test_crash_injection row |
| Removed code | traced from `git show 01e7a9e23^` with line numbers, safety properties and a data-flow reconstruction | R06 B1-B16 |
| Live-vs-off | decided per piece with evidence | R01 sec 12, R02 7b, R03 (b), R04 sec 16, R05 sec 6, R06 B16 |

**Missing depth elements:** the SKILL.md return-contract field names (F-01); doc-checking of design sections that were not assigned (F-02). Neither lowers the traced status of the assigned scope.

**Observation (not a gap):** R05 ran the guard script on 44 payloads in a sandbox `HOME` inside the task folder and reports that every result matched its reading of the code; the identity hook, the L2 hook, the claim and the installers were not executed and are labelled READ-ONLY-READING. I did not re-run the observation (read-only role); I checked that the sandbox folder exists with `run-guard-observation.sh`, `run-guard-extra.sh`, `observation-output.txt`, `out/` and `home/`.

---

## 9. Checks performed (counts)

| Check | Count |
|---|---|
| Research files read completely | 6 of 6 (3,021 lines) |
| Other inputs read | `research-notes.md` (131 lines), `phase-2-output-summary.md`, task-file prompt lines 754-795 |
| Scope files and test files checked for a research row (section 2) | 20 watcher tests + conftest + fixtures, 9 launch hook tests, 5 install/ccsession/core tests, 8 skills/commands/cli claim tests, contract test and removed tests; 100 percent covered |
| Source citations re-read in the live snapshot (section 4.1) | 38 listed (about 110 individual line numbers), 0 failed |
| Test files re-counted (lines and tests) | 42, 0 mismatches |
| Known staleness warnings confirmed (section 3) | 8 of 8 (14 sub-items) |
| Doc files opened to check a research claim | `issue-watcher.md` (sec 4.1, 7, 9, 11-14 samples), `issue-watcher-setup.md` (l.170, 616-619), `issue-pipeline-fu1.md` (l.64), `sc-issue-command.md`, `sc-issue-claim-pipeline-flag.md`, `sc-issue-launch-level-hook.md`, `issue-pipeline-guard-g2.md`, `orchestrator.md:368` |
| Git read-only commands | `show -s`, `ls-tree`, `show <rev>:<path>` against `01e7a9e23` |
| Cross-file topics compared (section 6) | 10 topics; 0 hard contradictions, 5 soft inconsistencies |
| Findings | 12: 0 BLOCKING, 12 MINOR |
| Writes | this report only; nothing under the snapshot; no `/tmp` script |

---

## Verdict: PASS

**BLOCKING findings: 0.** PASS rule from the brief: "no BLOCKING findings (MINOR findings, if any, listed as notes)". The twelve MINOR findings (F-01 to F-12) are notes for the Phase 5 synthesis writers and the assembler; none needs a research agent to re-run. Items worth acting on before synthesis starts: F-01 (copy the return-contract field lists from `SKILL.md:105-150`), F-02 (three design-doc drifts for the contradiction table), F-03 (one ruling on the skew row), F-06 (do not copy the two wrong numbers from `research-notes.md`).

Status: Complete
