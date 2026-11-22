# QA Report - Lens Evidence Quality (Gate 3)

**QA phase:** lens-evidence-quality
**Lens:** evidence quality
**Document under review:** /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/techref/ISSUE-TO-WORK-PIPELINE-TECHNICAL-REFERENCE.md
**Source root:** /home/coder/.cache/ic-snap-20261120/master (read-only)
**Fix authorization:** false
**Date:** 2026-11-20
Status: Complete

---

## Re-verification table (sampled citations)

Source root for every row: `/home/coder/.cache/ic-snap-20261120/master` (read only). Rows in the Appendix B block use `git -C /home/coder/workspaces/IronClaude show 01e7a9e23^:<path>`. Short names: P = `src/superclaude/cli/issue_watch`, OW = `src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py`, GD = `src/superclaude/hooks/scripts/launch-level-guard.sh`, WC = `src/superclaude/core/WORKER-CONTRACT.md`.

### Sections 4, 5, 8, 9, 10, 11 (and the Section 1 to 3 statistics)

| # | Claim (section) | Citation | Source text read | Result |
|---|---|---|---|---|
| 1 | Real cycle stops `not_enabled` (4.1, 5.1) | P/cycle.py:685-686 | `if not deps.config.enabled and not self.dry_run: raise _Stop("not_enabled")` | MATCH |
| 2 | `enabled` defaults false (9.1) | P/cycle.py:228 | `enabled = raw.get("enabled", False)` | MATCH |
| 3 | 14 module constants, `MAX_LAUNCHES_PER_CYCLE` unread (5.1.7, 11.1) | P/cycle.py:33-47, 35; `grep -rn MAX_LAUNCHES_PER_CYCLE src tests` | 14 constants at 34-47; only hit is `cycle.py:35` | MATCH |
| 4 | One launch per cycle, `launching` then `halt` (4.1) | P/cycle.py:1028, 833-834 | `c.launching = True`; `if c.launching: self.halt = True  # S1` | MATCH |
| 5 | Dry-run stops before any probe (4.1, 5.1.1.2) | P/cycle.py:1029-1035 | `if self.dry_run: ... return "launched", None` | MATCH |
| 6 | Gates E1-E10 line ranges (4.1, 5.1.1.1) | P/cycle.py:919-947 | state checks, G4/G3 reads, day cap, owner, marker at the cited lines | MATCH |
| 7 | Pending saved before launch; restore on cut-off (4.1, 10.3) | P/cycle.py:1091-1099 | `mark_pending`, `_save()  # FR-010`, restore on `launch_allowed()` false | MATCH |
| 8 | Skew warning threshold 60 s (4.1, 11.1) | P/cycle.py:44, 774 | `SKEW_WARN_S = 60`; `if skew > SKEW_WARN_S` | MATCH |
| 9 | `SKEW_TOLERANCE_S` 300 is the marker window (5.1.8, 11.1) | P/predicates.py:17, 295 | `SKEW_TOLERANCE_S = 300`; `when >= pending_at - timedelta(seconds=SKEW_TOLERANCE_S)` | MATCH |
| 10 | Exit precedence 2,6,7,5,3,4; 75 only alone (5.1.1, 10.1) | P/cycle.py:462-482 | `_PRECEDENCE = (2, 6, 7, 5, 3, 4)`, `resolve_exit` | MATCH |
| 11 | `_TOP_KEYS` holds 8 keys; unknown key rejected (9.1, 5.1.8 #8) | P/cycle.py:58-69, 216-220 | 8-key frozenset; `unknown = set(raw) - _TOP_KEYS` | MATCH |
| 12 | Five `"gh"` list literals at 177, 183, 204, 231, 255 (4.5, 5.1.2) | `grep -n '"gh"' P/github.py` | hits at 177, 183, 204, 231, 255 | MATCH |
| 13 | Call budget 35 cap, 3 reserved, 37 per cycle (1, 5.1.2, 11.1) | P/github.py:40-49, 437-463, 557-577 | `CALL_CAP = 35`, `RESERVED_CALLS = 3`; non-reserved cap 32; `spend_shared` never refuses | MATCH |
| 14 | Repo literal and origin literal (1, 9.4) | P/github.py:37; P/launch.py:50 | `REPO = "IronbellyOrg/IronClaude"`; `ORIGIN_REPO = "ironbellyorg/ironclaude"` | MATCH |
| 15 | Prompt pattern and 12-element argv (4.4, 5.1.3, 8.1) | P/launch.py:33, 84-92, 95-116 | `PROMPT_PATTERN ... --pipeline none$`; argv list of 12 items | MATCH |
| 16 | `dispatch.json` 7 keys, 6 states, 17-field entry (5.1.3, 6) | P/record.py:120-131, 34-36, 69-88 | `_STORE_KEYS` 7 names; `ENTRY_STATES` 6; `Entry` fields at 72-88 (17 lines) | MATCH |
| 17 | `DISABLED` uses `os.path.lexists` (5.1.3, 6, 9.3) | P/record.py:421-423 | `return os.path.lexists(self.state_dir / DISABLED_FILE)` | MATCH |
| 18 | `reset` refuses `claimed` (14.1.1) | P/record.py:448 | `_RESETTABLE = frozenset({"abandoned", "unknown"})` | MATCH |
| 19 | `reset --rate-limit --forfeit-guarantee` silently accepts (5.1.8, 14.3.1 Q-09) | P/cli.py:309-313 | `if by_issue == rate_limit: refuse`; `if by_issue and not forfeit_guarantee: refuse` (no check of the flag when `--rate-limit`) | MATCH |
| 20 | REASON_TABLE has 59 words, kinds 27/17/9/1/4/1 (5.1.6, 10.2) | P/audit.py:26-102 (regex count) | cycle 27, skip 17, entry 9, note 1, warning 4, total 59 (the operator word sits on its own line) | MATCH |
| 21 | Argv builders at stated lines (4.5, 8.1) | P/github.py:175-177, 180-183, 201-207, 223-225, 252-258 | `argv_user`, `argv_discover`, `_argv_rest_page` (`--method GET`), `argv_comments`, `argv_reread` | MATCH |
| 22 | ClickUp one PUT and skip rules (4.5, 9.3) | `.../scripts/clickup_claim.py:232-237, 164-169` | `request("PUT", .../task/{id}, token, {"assignees": {"add": [user_id]}})`; `no_token` / `no_workspace` skipped | MATCH |
| 23 | Claim C1 assign command (4.5, 8.1) | `.../refs/claim.md:48` | `gh issue edit <N> --repo <R> --add-assignee @me` | MATCH |
| 24 | Default level rule is prose (5.2) | `.../refs/claim.md:81` | rule text (bug `full`, simple/medium feature <=16 h `full`, else `worktree`) | MATCH |
| 25 | Stale doc: "as the worktree's pre-push hook", "Before anything else" (4.3, 5.2, 14 X-23) | `.../refs/claim.md:125` | both phrases present on line 125 | MATCH |
| 26 | IR-7 refusal is a constant set False (2.3, 5.2, 14 D-19) | OW:822, 818-822, 1757-1758 | `IR7_REFUSE = False  # ... owner decision 2026-11-08`; comment says "owner decision OD-3" | MATCH |
| 27 | `pending` verb, no production caller (2.3, 5.2) | OW:1515-1523, 1886-1893; `tests/hooks/test_launch_level_guard_worker.py:287` | `cmd_pending`; parser `pending`; test runs `"pending", "--level", "worktree"` | MATCH |
| 28 | Governed launch argv with marker (4.3, 8.1) | OW:1776-1779 | `argv += [f"path:{wt}", "--surface", "terminal", "--prompt"]`, marked prompt, `--json` | MATCH |
| 29 | 23 governed tool names (5.2 launch order step 4) | OW:841-867 | 23 quoted entries counted | MATCH |
| 30 | Typed approval regex accepts `/sc:implement` and `/task` only (4.3, 5.3, 14 D-23) | GD:347; `grep -c 'sc:task' GD` | `^[[:space:]]*/(sc:implement\|task)([[:space:]]\|$)`; count 0 | MATCH |
| 31 | `/sc:task` named as releasing line in template (4.3, 5.3) | `.../templates/launch-prompt.md:23` | "first line starts `/sc:implement`, `/sc:task` or `/task`" | MATCH |
| 32 | Guard decision grid and precedence (5.3) | GD:783-803, 799, 807-808 | `for LL_C in BIG TAMPER MERGE ...`; grid cases; `ll_deny LL-BROKEN` default | MATCH |
| 33 | IMPL classes are implement/task/cleanup (5.3, 14 KW-6) | GD:409; `ls src/superclaude/commands` | `implement \| task \| cleanup) ... IMPL`; improve/spawn/build absent | MATCH |
| 34 | Guard matches basename `orca` only (5.3, 14 D-25) | GD:457; `grep -c orca-ide GD` | case arm `orca)`; count 0; `probes.py:43` default `orca-ide` | MATCH |
| 35 | Orca allow-list (5.3) | GD:480-491 | list of status/help/--version/worktree/terminal/orchestration verbs | MATCH |
| 36 | Hook registrations and timeouts (5.3, 8.4) | `src/superclaude/hooks/hooks.json:63-71, 115-134` and a structure scan of the whole file | guard on UserPromptSubmit and PreToolUse, identity on Bash, timeout 5 each; other events as tabulated | MATCH |
| 37 | Hook script list in installer (5.3, 13.1.6) | `src/superclaude/cli/install_hooks.py:42-97, 90, 93, 96, 282-289` | list ends with launch scripts at 90/93/96; skip-if-exists unless `force` | MATCH |
| 38 | Installer call sites (8.1, 9.2) | `src/superclaude/cli/main.py:211, 219, 406, 412` | `wire_ccsession()`; `install_hooks(force=force)`; `install_hooks(force=True)` | MATCH |
| 39 | Identity hook returns 0 for non-Bash tools (14.1.1, 5.3) | `.../launch-job-identity.sh:442-444` | `if isinstance(tool, str) and tool != 'Bash': return 0` | MATCH |
| 40 | L2 protected refs and ordinary exit (5.3, 9.2) | `.../launch-level-pre-push.sh:17, 188` | `L2_PROTECTED=(refs/heads/main refs/heads/master)`; `[[ $L2_ACTOR != ordinary ]] \|\| exit 0` | MATCH |
| 41 | WC-2..WC-16 rule lines, section headings (5.4) | WC:31, 32, 40-47, 53, 59-64, 72, 287; headings 9, 27, 49, 68, 299 | each rule or heading found at the cited line | MATCH |
| 42 | "grant row" occurs once in the contract (5.4, 14 D-31) | WC:57; `grep -c 'grant row' WC` | count 1, line 57 | MATCH |
| 43 | No WC-17 / "Issue pipeline duties" in snapshot contract (2.3, 5.4) | `grep -c 'WC-17\|Issue pipeline duties' WC`; `wc -l` | 0; 339 lines | MATCH |
| 44 | `CHANGELOG.md:17` records the removal; `:9` names `orchestrator_repo` (2.3, 14) | CHANGELOG.md:9, 17 | line 17 "issue-pipeline command group ... removed"; line 9 `orchestrator_repo` key | MATCH |
| 45 | Architecture doc says no contract rule starts the worker (5.4, 14.1.1) | docs/architecture/SUPERVISED-ORCHESTRATION-TECHNICAL-REFERENCE.md:268 | "removed in issue 655, PR D; the orchestrator design replaces them, and until it lands no contract rule says who starts that worker" | MATCH (quoted with elision) |
| 46 | Default state dir (6, 9.3) | P/cycle.py:187-192 | `XDG_STATE_HOME` else `~/.local/state`, plus `superclaude/issue-watch` | MATCH |
| 47 | Network FS deny list (9.1) | P/cycle.py:50-52 | `{"nfs","nfs4","cifs","smb3","sshfs","fuse.sshfs","9p"}` | MATCH |
| 48 | Size constants: rotation, stderr cap, approvers cap (11.1) | P/audit.py:106-107; P/runner.py:15; P/cycle.py:75 | `ROTATE_BYTES = 5*1024*1024`, `_ROTATIONS = 4`; `STDERR_CAP_BYTES = 500`; `_APPROVERS_MAX_BYTES = 1024*1024` | MATCH |
| 49 | L2 self-test timeout 30 s (11.1) | OW:1078, 1178 | line 1078 `L2_SELFTEST_TIMEOUT = 30.0`; line 1178 is `L2_PACKAGED_MAX = (` | LINE-MOVED (companion line is a different constant, see M-03) |
| 50 | `ccsession-models.json` tier keys at 85, 93, 104, 113 (13.1.7) | `.../ccsession-models.json` | `tier1b`, `tier2`, `tier2b`, `tier3` at those lines | MATCH |
| 51 | Agent frontmatter: tools line 5, model line 6, t3 effort line 7 (3.1, 5.2) | `src/superclaude/agents/issue-worker-t{1,2,3}.md:5-7` | `tools: Read, Grep, Glob, Write, Bash`; `model: claude-gw-tier1b/tier2/tier2b`; `effort: low` (t3) | MATCH |
| 52 | Plugin scripts byte-identical, plugin hooks.json differs (5.3, 8.4) | `cmp` on 3 scripts; `diff hooks.json` | 3 identical; diff shows ccsession-tag, `pragmatic-subagent.js` and `async` differences | MATCH |
| 53 | File lengths in Sections 1, 3.1 (watcher 4,795; guard 808; identity 582; pre-push 208; hooks.json 192/154; WC 339; issue.md 117; SKILL 197; OW 1906) | `wc -l` on each | all equal the stated counts | MATCH |
| 54 | Statistics: tests/issue_watch 20 files, 19,801 lines, 867 tests; guard tests 17 files, 24,388 lines, 921 tests | `wc -l`, `grep -c 'def test_'` over each file, summed | 19,801; 867; 24,388; 921 (plain grep) | MATCH |

### Section 14 (14.1.2, 14.2.1, 14.3.1)

| # | Claim | Citation | Source text read | Result |
|---|---|---|---|---|
| 55 | KW-2: design names `max_launches_per_cycle` default | DES:380, 819 | line 380 `max_launches_per_cycle 1`; line 819 same | MATCH |
| 56 | KW-3 / X-6 / X-7: design prompt lacks `--pipeline none`; capture sheet | DES:15, 41; SET:616-619; SET:170, 575 | DES:15 `--prompt "/sc:issue --claim <N>"`; SET:616-619 launch rows; SET:170 and 575 mention `--pipeline none` | MATCH |
| 57 | KW-4: runbook runs removed commands | docs/designs/issue-pipeline-fu1.md:64-66 | `uv run superclaude issue-pipeline plan-hash ...`; `plan_hash.py` | MATCH |
| 58 | KW-5 / X-25: guard-g2 design line numbers, route A | docs/designs/issue-pipeline-guard-g2.md:13, 22; g2-no-to.md:7, 48 | `:471-472`, `:473`, `:474`, `:703` embedded; "address block at lines 500-549"; "rule WC-17" | MATCH |
| 59 | KW-6: six IMPL skills, typed `approved` row | docs/designs/sc-issue-launch-level-hook.md:106, 123, 179, 189, 236, 391 | six skills on 106/236/391; row 34 at 123; `:189` says only `/sc:implement\|task` releases | MATCH |
| 60 | KW-7: T3 pinned to `claude-gw-tier3` in design | docs/designs/sc-issue-command.md:3, 58, 107, 129, 391, 423, 449 | each line names tier3 or "Design only" | MATCH |
| 61 | X-8 / D-08: skill reads `orchestrator_repo` from the poll config | skills/agent-work-report/scripts/common.py:22-40; tests/skills/test_agent_work_report.py:2979-3000 | `POLL_CONFIG`, `json.loads(...)["orchestrator_repo"]`; test writes `{"orchestrator_repo": ...}` | MATCH |
| 62 | X-13 `_ORCA_CLIS` at line 36, X-20 parity lines | src/superclaude/cli/install_user_setup.py:36, 216-219, 247-270; tests/issue_watch/test_find_orca_parity.py:13-18 | `_ORCA_CLIS = ("orca-ide", "orca")`; `_find_orca` at 247-270; docstring names 216-217 and 219 | MATCH |
| 63 | X-15 architecture doc registers watcher at `main.py:563-565` | docs/architecture/...:1059; src/superclaude/cli/main.py:577-579 | doc says 563-565; code is 577-579 | MATCH (stale doc, correctly tagged) |
| 64 | X-23 `tiers.md` heading appears twice | `.../refs/tiers.md:32, 44` | `## E-TIER-UNAVAILABLE (default D4)` at both lines | MATCH |
| 65 | X-24 model-alias doc lines and a fourth allowed location | docs/reference/model-aliases.md:12, 18; tests/skills/test_model_alias_policy.py:38-44, 50, 104-119 | doc text; `TIER_TEXT_ALLOWED`, `TIER_TEXT_DIRS` | MATCH |
| 66 | D-09 / D-10 / D-11 dead and write-only fields | P/record.py:748-750, 548-568, 180, 185; P/launch.py:58-70 | `disabled_present`; `launch_login` stored and validated; `LAUNCH_DETAILS` | MATCH |
| 67 | D-12 retry argv only printed | P/launch.py:119-132; P/cycle.py:1308-1312 | `retry_argv(...)`; `if entry.state == "unknown" ... argv = launch.retry_argv(` | MATCH |
| 68 | D-19 owner decision words | OW:818-822 | "owner decision OD-3" and "2026-11-08" | MATCH |
| 69 | D-25 orca-ide default in sweep probes | src/superclaude/cli/sweep/probes.py:43 | `ORCA_BINARY_DEFAULT = "orca-ide"` | MATCH |
| 70 | D-31 / B.5 "grant row" twice in the old contract | `git show 01e7a9e23^:WC`, lines 57 and 300 | both lines contain "grant row" | MATCH |
| 71 | U-3 `COORD-` has no hits outside `.git` and `.dev` | `grep -rIn 'COORD-' . --exclude-dir=.git --exclude-dir=.dev` | no output | MATCH |
| 72 | U-8 "739 tests" claim vs 59 `def test_` | arch doc :208; `grep -c 'def test_' tests/skills/test_worker_contract.py` | doc line says `(739 tests)`; file has 59 | MATCH |
| 73 | D-01 / D-02 `status` ignores audit | P/cycle.py:1279-1281 | "`audit` is accepted for the fixed signature and not read" | MATCH |

### Appendix A and Appendix B

| # | Claim | Citation | Source text read | Result |
|---|---|---|---|---|
| 74 | A.1 to A.4: 48 rows, Lines and Tests per file | `wc -l` and `grep -c 'def test_'` on all 47 test files plus fixture dir | every Lines and Tests figure equals the table (guard file 4631 lines, 163 plain / 162 strict; literal at `:4615`) | MATCH |
| 75 | 19 `_assumed_shape` fixtures, 12,059 bytes, all labelled | `ls`, `cat \| wc -c`, `grep -l '"_assumed_shape": true'` | 19; 12059; 19 | MATCH |
| 76 | Observation test skips 12 live cases | tests/hooks/test_launch_level_observations.py:79, 84 | `_PENDING` = 9 + 3 entries; `pytest.skip(...has not been run)` | MATCH |
| 77 | Test function names at cited lines (e.g. `test_grid_policy` :3394, `test_design_table_holds_all_eighteen_ids` :1712, `test_precedence_order` :4520, `test_ir7_shipped_switch_is_off` :639) | `sed -n` at each cited line across 12 test files | function names match the claim in every sampled case | MATCH (about 100 lines sampled) |
| 78 | B.1 removed package: 10 files, 1,597 lines | `git ls-tree -r --name-only 01e7a9e23^ -- src/superclaude/cli/issue_pipeline/`; `git show ... \| wc -l` per file | 10 files: 5+62+416+74+395+90+161+66+301+27 = 1,597 | MATCH |
| 79 | B.2 verb decorators at lines 61, 76, 96, 108, 117, 134, 161, 179, 200, 335; exit consts 29-32; group 56-58 | `git show 01e7a9e23^:.../cli.py` | each `@issue_pipeline_group.command("...")` at the cited line | MATCH |
| 80 | B.4 `release.py:3-4, 57-62`; B.3 `approval_line.py:18-21, 50-51`; `plan_hash.py:24-36` (11 words), `reads.py:42` | `git show 01e7a9e23^:<path>` | docstring "coordinator calls this..."; `SHORT = "approved"`, bare refusal; 11 reason words; `_MARKER = ...sc:stage:plan...` | MATCH |
| 81 | B.5 old contract: WC-17 at :59, "Issue pipeline duties" :291-300, `COORD-` absent | `git show 01e7a9e23^:WC` | WC-17 at 59; heading at 291; duties 295-300; `grep -c COORD-` 0 | MATCH |
| 82 | B.6 old guard TAMPER case at :441-444, normaliser :428 | `git show 01e7a9e23^:GD` | comment 441-443; `case $T in *release-worker* ...` at 444 | MATCH |
| 83 | B.1 old `main.py:581, 583` | `git show 01e7a9e23^:src/superclaude/cli/main.py` | import at 581, `add_command(... "issue-pipeline")` at 583 | MATCH |
| 84 | B.8 removed tests: 116 tests, 2,391 lines, 10 files; contract test 3,181 lines / 61 tests; guard-worker test 330 lines | `git show 01e7a9e23^:<each file>` | sums 116 and 2,391; 3181 / 61; 330 | MATCH |
| 85 | B header: commit date and quoted message | `git log -1 --format=... 01e7a9e23`; message body | `2026-11-19 18:02:35 -0600`; "Nothing ran this code: the issue watcher has" present | MATCH |
| 86 | B.8 `test_stage_status.py:451` pins "never calls orca" | `git show 01e7a9e23^:tests/issue_pipeline/test_stage_status.py` line 451 | `def test_the_command_only_reads_and_never_calls_orca(` | MATCH |

Totals: 86 rows (several rows bundle 5 to 100 individual line checks). Rows 1 to 54 sample Sections 1 to 5 and 8 to 11 (54 rows, at least 25 required); rows 55 to 73 sample Section 14 (19 rows, at least 10 required); rows 74 to 86 sample Appendix A and B (13 rows, at least 10 required). One LINE-MOVED row (49), no MISMATCH row.

## Findings

No BLOCKING finding. I looked for fabricated paths, citations that do not support their claim, untagged doc-only claims and unevidenced core claims, and found none that I could evidence. Seven MINOR notes follow (wording, citation placement, scope hedging). M-01 is the closest to blocking and is explained in full.

| ID | Severity | Location | Issue | Evidence (source path:line) | Required fix |
|---|---|---|---|---|---|
| M-01 | MINOR | Section 14.1.1 row "After a `--pipeline none` claim no code or contract rule starts a worker" (Planned Fix: "none (D-16)"); Section 14.1.1 row 1 (Planned Fix: FU-2 cron entry); D-16, D-18, D-21; Section 14.3 row "Binding coordinator-started workers"; Appendix B.9 | The snapshot holds an owner-approved design, `docs/designs/orchestrator.md`, that is not cited anywhere in the reference. It says one system replaces the watcher poller and the plan-approval gate (`:33`), records "assignment is the only trigger" (`:73`), answers whether a `worker-start` worker is under the #442 gate: "No ... never governed" (DQ7, `:117`; `:975`), and lists the removal of WC-17 and `issue_pipeline` as PR D (`:991`, `:1017`). Section 1 (line 218) declares "the rewrite design" out of scope, and most "No decision found" sentences are hedged "in the files this reference cites", so they are literally true. But the unhedged cell "Planned Fix: none (D-16)" and the FU-2 "Planned Fix" are contradicted by a file in the snapshot, and the reference itself cites `docs/architecture/SUPERVISED-ORCHESTRATION-TECHNICAL-REFERENCE.md:268`, which says "the orchestrator design replaces them". The design has no code in the snapshot (no `/sc:orchestrator` command or skill under `src/superclaude/`), so every NOT BUILT status stays correct. | `docs/designs/orchestrator.md:3, 33, 73, 117, 975, 991, 1017`; `docs/architecture/SUPERVISED-ORCHESTRATION-TECHNICAL-REFERENCE.md:268`; reference line 218 | Name the file in the Section 1 out-of-scope sentence and change "Planned Fix: none" to "none in the files in scope; a design that replaces this flow exists in `docs/designs/orchestrator.md` (not built)". |
| M-02 | MINOR | Section 14.2.1 D-15 and 14.3 row "FU-8 auto-retry ..." | The quoted sentence "None of these is built by this work" is attributed to `DES:862-871` / `DES:856-871` together with `SET:673-686` / `SET:669-686`. In the snapshot it occurs once, at `docs/designs/issue-watcher-setup.md:671`, which is inside the SET range of the second row but not inside the SET range of D-15 (673-686), and is not in the DES range at all. | `grep -n "None of these is built by this work" docs/designs/*.md` returns only `docs/designs/issue-watcher-setup.md:671` | Cite `SET:671` for the quote; drop it from the DES range. |
| M-03 | MINOR | Section 11.1, row "Claim command timeouts" | The citation list `orca_worktree.py:88-91, 798-800, 1078, 1178` includes `:1178`, which is `L2_PACKAGED_MAX = (`, not a timeout. The 30 s L2 self-test timeout is `:1078` (`L2_SELFTEST_TIMEOUT = 30.0`). The stated value is right. | `OW:1078`, `OW:1178` | Remove `1178` from the row. |
| M-04 | MINOR | Section 11.1, row `MAX_CANDIDATES` | "(design `k = min(10, 8)`)" is a design-sourced statement with no path:line. It is correct; it is at `docs/designs/issue-watcher.md:391`. | `docs/designs/issue-watcher.md:391` | Add `DES:391` and the [UNVERIFIED]/design tag as used elsewhere. |
| M-05 | MINOR | Section 4.2 intro sentence | "only the three helper scripts are code (`SK/SKILL.md:35`)": line 35 says `orca_worktree.py` is "the only file that calls `orca`". The point that no program orders the waves is at `SKILL.md:80-92`, which Section 5.2 cites correctly. | `.../sc-issue-protocol/SKILL.md:35`, `:80-92` | Cite `SKILL.md:80-92` in 4.2 as well. |
| M-06 | MINOR | Section 4.1 table step 6 vs Section 5.1.1 table step 6 | Section 4.1 lists the origin check failure as `origin_mismatch`, 2 and the read as "none (not budgeted)". Code also stops with `gh_timeout` (exit 3) when no time is left for the git call (`cycle.py:716-720`); Section 5.1.1 states this correctly. The two tables disagree by one word. | `P/cycle.py:716-722` | Add "no time left: `gh_timeout`, 3" to the 4.1 row. |
| M-07 | MINOR | Section 12.1 row "Governed sessions fail closed, ordinary sessions fail open" | Pin column quotes two phrases as if they were test names: "ordinary sessions never blocked", "fail-closed resolution". Neither string exists in `tests/hooks/test_launch_level_guard.py`; the file has section comments "isolation and fail-closed cases that concern binding" (`:651`) and "PreToolUse resolution: isolation and fail-closed (Task 5)" (`:1522`). The behaviour is pinned; only the quoted labels are not literal. | `tests/hooks/test_launch_level_guard.py:651, 1522` | Replace the quoted phrases with `:651` and `:1522`, or unquote them. |

## Checks performed

| # | Lens check | Result | Method and counts |
|---|---|---|---|
| 1 | Substantive claims carry inline `path:line` | PASS (notes M-04, M-05, M-07) | Read all 2,369 lines. Core sections 2, 4, 5, 8 to 11 and 14 cite a path with a line or line range, or name a closed test or constant, for each fact row. Claims with no line anchor are file-level test pins (for example `test_cli.py` "exactly five commands" at `:279` exists as `test_the_group_lists_exactly_the_five_commands__df06`), design-sourced numbers (M-04) and the quoted test labels in M-07. None is a core behavioural claim. |
| 2 | Every cited path exists in the snapshot | PASS | `grep -oE` over the document gave 139 distinct path tokens. 118 exist as written; 7 are glob or placeholder forms (`<name>.sh`, `issue-worker-t*.md`, `launch-*.sh`, `_assumed_shape/*.json`, `{skills,commands,agents}`); 14 are reported missing, all explained: 1 intentionally absent file stated as absent (`docs/designs/issue-watcher-live-test.md`), 4 are the `scripts/...` tails of `SK/scripts/...` shorthand (the full paths exist), 1 is the template name `issue-worker-tN.md` (parent directory exists), 8 are removed-code paths in Appendix B or labelled `@01e7a9e23^` (`issue_pipeline/`, `brief.py`, `plan_hash.py`, `release.py`, `tests/issue_pipeline/`, `test_stage_status.py`, `tests/cli/test_issue_pipeline_registered.py`), all present at `01e7a9e23^` (`git ls-tree` lists the 10 package files and 17 test-side entries). About 40 further files named only through shorthand (`P/`, `SK/`, `H/`, `OW`, `GD`, `ID`, `PP`, `HJ`, `WC`, `DES`, `SET`, `T/`) were opened or measured with `wc -l`. No path is missing. |
| 3 | Re-verify at least 50 citations (25 from 4-5 and 8-11, 10 from 14, 10 from Appendix A and B) | PASS | 86 table rows above; 54 / 19 / 13 rows in the three groups; 85 MATCH, 1 LINE-MOVED, 0 MISMATCH. Beyond the table, about 330 further individual lines were read in the same passes (cycle.py, github.py, record.py, audit.py, launch.py, cli.py, predicates.py, orca_worktree.py, guard, identity hook, pre-push hook, hooks.json, claim.md, SKILL.md, issue.md, tiers.md, clickup_claim.py, origin_repo.py, WORKER-CONTRACT.md, design documents, about 100 test lines) with no mismatch. |
| 4 | Cited line numbers lie within the file length | PASS | Scripted bound check: 172 distinct full-path `path:line[-line]` citations, none past end of file (only the 3 Appendix B old-tree paths could not be resolved in the snapshot, expected). Shorthand forms `P/<module>.py:N`, `OW`, `GD`, `GUARD`, `HJ`, `ID`, `PP`, `WC`, `WCT`, `DES`, `SET`, `SK/...`, `claim.md`, `SKILL.md`, `issue.md`, `tiers.md`, `H/`, `HK/`, `T/test_*.py:N` were bound-checked the same way: no citation is past end of file. |
| 5 | Evidence is specific (function, constant, argv) | PASS | Every sampled row names a constant, function, argv list, regex or test function; the doc quotes argv arrays and regexes literally and they match the source. |
| 6 | Doc-sourced claims tagged; no [UNVERIFIED] claim stated as fact outside Section 14 | PASS (note M-04) | Doc-versus-code differences carry [CODE-CONTRADICTED] or [STALE DOC] and each one I opened is right (KW-1 to KW-8, X-1 to X-28 sampled: 19 rows). Design-only claims (PR numbers #447/#448, FU-1 recorded lines, "about 100 ms" L2 cost, tier model order, "739 tests") are tagged [UNVERIFIED] where stated. The one untagged design-sourced figure is `k = min(10, 8)` (M-04). |
| 7 | No hallucinated paths (parent directories exist) | PASS | Extension Guide new-file paths (`src/superclaude/hooks/scripts/<name>.sh`, `plugins/superclaude/hooks/scripts/<name>.sh`, `src/superclaude/agents/issue-worker-tN.md`, templates under `sc-issue-protocol/templates/`) all have existing parent directories. |
| 8 | No fact taken from memory notes or chat ("zero-setup watcher", "COORD-", "dispatcher", "grant rows") | PASS | All 14 lines of the document that contain `zero-setup`, `COORD-` or `dispatcher` are negative statements ("not found in snapshot", "0 hits", "no dispatcher"). Re-ran `grep -rIn 'COORD-' <snapshot> --exclude-dir=.git --exclude-dir=.dev`: no output. `grep -rIiln 'zero-setup'`: no file. `dispatcher` hits are in swarm and eval code and tests, unrelated. "grant row" appears once in the contract (`WORKER-CONTRACT.md:57`) and in `issue-pipeline-fu1.md:24, 26`, as the document says. |

Additional checks outside the numbered list: (a) negative claims re-run against the snapshot: no `release-worker` in `src`/`tests`/`plugins`; no `pipeline.json` in `src`/`plugins`; no `orca-ide` or `sc:task` in the guard; no `WC-17`/"Issue pipeline duties" in the contract; no `issue-watch*.json` file; `MAX_LAUNCHES_PER_CYCLE` only at `cycle.py:35`; no `worker-start` call in Python under `src/superclaude/cli` outside swarm event names; no `subprocess`/`gh`/`git`/`orca` literal in `cycle.py`. All hold. (b) The observation-run claim (44 payloads, `orca-ide` exit 0) was checked against `research/05-guard-run-sandbox/observation-output.txt`: 40 `CASE` payloads plus 4 `EXTRA` lines, with `orca-ide terminal send` and `orca-ide orchestration send --to ...` at exit 0 and `orca terminal send` at exit 2. I did not re-run the guard (the safety rules forbid writing a sandbox home outside the report). (c) Section 15.2 spot-check commands: items 2, 3, 5, 6, 8, 9, 10, 13, 14, 16, 17 and 18 re-run by equivalent commands; every expected result held.

**Confidence:** Verified: 8/8 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
**Tool engagement:** Read: 11 (task block, 8 chunks of the document, 2 report reads) | Grep: 0 | Glob: 0 | Bash: about 55 (batched `sed -n`, `grep`, `wc`, `cmp`, `diff`, `git show`, `git ls-tree`, all read-only; no file created outside this report)
**Unverifiable items:** none. Runtime behaviour of Orca, `gh` and the live observations OB-H1..3 is outside the lens (the document tags them [UNVERIFIED]).
**Limits of this review:** 86 table rows plus roughly 330 further lines is a sample, not all of the roughly 1,900 line citations in the document. The sample was spread across every section, weighted to high-risk spots (constants, counts, negative claims, doc-versus-code rows, removed code), and found no defect that changes a claim's truth.

## Verdict: PASS

Blocking findings: 0. Minor notes: 7 (M-01 to M-07).

Status: Complete
