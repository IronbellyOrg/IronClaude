# QA Report - Research Gate (Evidence Quality)

**Topic:** IronClaude issue-to-work pipeline technical reference
**Date:** 2026-11-20
**Phase:** research-gate
**Lens:** evidence-quality
**Fix authorization:** false
**Status:** Complete (see the final Verdict line)

---

## Scope and method

- Research files read completely (all six, every line): `01-watcher-decision-engine.md` (656 lines), `02-watcher-io-github-launch-record.md` (473), `03-watcher-operator-surface-and-setup.md` (497), `04-claim-flow-and-orca-worktree.md` (497), `05-guard-stack-and-ccsession.md` (500), `06-coordinator-text-and-removed-code.md` (398). Directory: `/home/coder/workspaces/IronClaude/.dev/tasks/to-do/TASK-TECHREF-issue-pipeline-20261120-040158/research/`. No `gap-fill-*.md` file exists.
- Source of truth: the read-only snapshot `/home/coder/.cache/ic-snap-20261120/master` (origin/master 61ac2c2e6; `git rev-parse 61ac2c2e6` resolves to `61ac2c2e6effc24baa5ccef2a71a0a08d85bd5cd`). Removed code only via read-only `git -C /home/coder/workspaces/IronClaude show 01e7a9e23^:<path>`. Nothing was written under the snapshot (not even a probe file); the only files written by this run are this report and short-lived scripts and a throwaway HOME under `/tmp/ironclaude-batch.*`, removed after each call.
- Method: every citation was re-read from the live snapshot by line (`sed -n`, `grep -n`, `wc -l`, `grep -c 'def test_'`, direct Read of the code), adversarially, assuming at least some were wrong. The adversarial stance is a posture, not a quota: only defects with evidence are reported.
- Independent re-execution (beyond reading): I re-ran the unmodified launch-level guard from the snapshot path against fresh bound sessions in a private `/tmp` HOME (18 payloads: 3 binds plus 15 decisions) to check the research-05 level-matrix and `orca-ide` claims; all results matched (see section "Independent re-execution").
- Snapshot integrity (research 05 claims it never changed the snapshot): `find $SNAP -newer research/05-guard-run-sandbox/run-guard-observation.sh -type f` returned 0 files and there is no `__pycache__` or `.pytest_cache` under the snapshot.

---

## Sample table of re-verified citations

`SNAP` = `/home/coder/.cache/ic-snap-20261120/master`; `P` = `SNAP/src/superclaude/cli/issue_watch`. "Actual" quotes or summarises the text I read. MATCH means the claim is true at the cited location; MISMATCH means wrong value, wrong location with a false claim, or false statement. A trivially moved line number on a true claim would be MINOR (none found except as listed under Findings).

### Research 01 (watcher decision engine)

| File | Citation | Claimed | Actual | MATCH/MISMATCH |
|---|---|---|---|---|
| 01 | `P/cycle.py:34-47` (values in the section 1 table) | MAX_CANDIDATES 10, MAX_LAUNCHES_PER_CYCLE 1, DAY_CAP 6, GH_TIMEOUT_S 20.0, PROBE 10.0, GIT 10.0, LAUNCH_TIMEOUT 120.0, DEADLINE_TOTAL 240.0, GH_FLOOR 5.0, LAUNCH_CUTOFF 120.0, SKEW_WARN_S 60, HEALTH_AGE_S 900, STALE_AGE_S 86400, DISCOVERY_WARN 80 | `sed -n 34,47p` prints exactly those names and values | MATCH (all 14 values) |
| 01 | Key Takeaways line 34 (count of those constants) | "13 constants at lines 34-47; 12 are read, `MAX_LAUNCHES_PER_CYCLE` is dead" | lines 34-47 are 14 assignments (the file's own section 1 table has 14 rows); 13 are read, 1 is dead | MISMATCH (BLOCKING, finding B-1) |
| 01 | `cycle.py:35` + whole-snapshot grep | `MAX_LAUNCHES_PER_CYCLE` is read nowhere; only the definition | `grep -rniE 'MAX_LAUNCHES_PER_CYCLE'` outside `.dev/`: cycle.py plus 3 docs (`docs/architecture/SUPERVISED-...md`, `docs/designs/orchestrator.md`, `docs/designs/issue-watcher.md`); no `src/` or `tests/` read | MATCH |
| 01 | `cycle.py:462-482` | `_PRECEDENCE = (2, 6, 7, 5, 3, 4)`; 75 only when the sole non-zero condition | `_PRECEDENCE = (2, 6, 7, 5, 3, 4)`, `_LOCK_HELD_EXIT = 75`, `if set(conditions) - {0} == {_LOCK_HELD_EXIT}: return _LOCK_HELD_EXIT` | MATCH |
| 01 | `cycle.py:816-817, 833-834` | `halt` loop break; `if c.launching: self.halt = True` (S1, DF-50) | line 816 `if self.halt:`, 817 `break`, 833 `if c.launching:`, 834 `self.halt = True  # S1: nothing after a launch-step outcome (DF-50)` | MATCH |
| 01 | `audit.py:26-102` REASON_TABLE count and tally | 59 entries: cycle 27 (7+5+5+2+2+1+1+4), skip 17, entry 9, note 1, warning 4, skip/warning 1 | `grep -cE '^    "[a-z_-]+": \("'` = 59; kind/exit tally: cycle 0:4, 1:1, 2:7, 3:5, 4:2, 5:2, 6:5, 75:1 (=27); entry 5+4 (=9); skip 17; note 1; warning 3+1 (=4); `operator_reset` skip/warning | MATCH |
| 01 | `record.py:434-443` | MAX_ATTEMPTS 3, BACKOFF 10 min, LEASE 60 min, DAY_CAP_WINDOW 24 h | `MAX_ATTEMPTS = 3`, `BACKOFF = timedelta(minutes=10)`, `LEASE = timedelta(minutes=60)`, `DAY_CAP_WINDOW = timedelta(hours=24)` | MATCH |
| 01 | `github.py:40-49, 376, 486` | PAGE_SIZE 100, PAGE_CAP 5, CALL_CAP 35, RESERVED_CALLS 3, RATE_LIMIT_MAX_WAIT_S 3600, DISCOVERY_BOUND 100 | same values at lines 40, 43, 46, 49, 376, 486 | MATCH |
| 01 | `predicates.py:14,17,20,57` | CLAIM_MARKER, SKEW_TOLERANCE_S 300, MAX_ISSUE_NUMBER 999_999_999, OPERATION_ID_PATTERN | `CLAIM_MARKER = "<!-- sc:issue:claim -->"`, `SKEW_TOLERANCE_S = 300`, `MAX_ISSUE_NUMBER = 999_999_999`, `OPERATION_ID_PATTERN = re.compile(r"^[A-Za-z0-9._:-]{1,128}$")` | MATCH |
| 01 | `github.py:175-262` argv G1-G7 | seven argv lists (`gh api user --include`; `gh issue list --repo ... -L 100`; REST `--method GET ... -F per_page=100 -F page=<P> --jq`; graphql `-f query= -F number=`; re-read) | `argv_user` `["gh","api","user","--include"]`; `argv_discover` ends `"--json","number,labels,assignees,state","-L","100"`; `_argv_rest_page` has `"--method","GET"`; `_argv_graphql` has `"-f",f"query=..."`, `"-F",f"number=..."`; `argv_reread` `--method GET repos/{REPO}/issues/{n} --jq` | MATCH |
| 01 | `github.py:557-589` | `_call` returns None on missing timeout or refused budget; `_NO_CALL` (`budget_exhausted`) at 588 | line 571-575 `timeout = timeout_for(); if timeout is None: return None`; `if budget is not None and not budget.spend(reserved): return None`; 588 `_NO_CALL = Read(None, "budget_exhausted", "budget_exhausted")`, 589 `_SHARED_NO_CALL = Read(None, "gh_timeout", "timeout")` | MATCH |
| 01 | `cycle.py:915-961` gate order E1-E15 | `_examine` order: claimed/pending skip, marker read for launched/unknown/abandoned-with-pending_at, tombstone reclaim, backoff reclaim, day cap, owner, G4, G3, approval, own-marker claim, G5, unchanged_since, G6, project_check, `_launch` | read lines 915-961: exactly that order (lines 920, 922-931, 932-933, 934-935, 936-937, 938-940, 941-943, 944, 945, 946-947, 948, 949-956, 957, 958-960, 961) | MATCH |
| 01 | `cycle.py:1028-1112` launch step | L0 `c.launching = True` 1028; dry-run return 1029-1035; `orca_not_found` stamp 1052; `_fail(c,"prompt_invalid")` 1056; `disabled_mid_cycle` 1064; `origin_mismatch` 1075; `pending` saved 1091-1092 "durable before the launch call"; `launcher.launch` 1099 | all lines read and match (e.g. 1092 `self._save()  # FR-010: durable before the launch call`, 1099 `outcome = d.launcher.launch(orca, cfg.worktree, prompt, LAUNCH_TIMEOUT_S)`) | MATCH |
| 01 | `tests/issue_watch/` counts | test_cycle 4982 lines/237 tests; test_predicates 732/44; test_audit 849/46; test_marker_contract 53/3; conftest 1155/0 | `wc -l` and `grep -cE '^\s*(async )?def test_'`: 4982/237, 732/44, 849/46, 53/3, 1155/0 | MATCH |
| 01 | test names + lines (16 sampled) | e.g. `test_s1_case_a_...` (3721), `test_ten_skipping_candidates_stop_at_32_calls_...` (4445), `test_reasons_pin_59_names__ac14_fr020_nfr006` (test_audit.py:214) | each `sed -n <line>p` printed the named `def` | MATCH (16 of 16) |
| 01 | `docs/designs/issue-watcher.md:173, 510, 827` | 173: "7 with 5 ... 7 with 3"; 510: skew warning > 60 s; 827: "skew tolerance \| 300 s" | lines read; 173 contains "the combinations that can occur are 7 with 5 (a `failed` entry was written, ..."; 510 `\| Clock skew warning \| \|local now − Date header\| > 60 s`; 827 `\| skew tolerance \| 300 s \| equals the cadence \|` | MATCH |
| 01 | `cycle.py:1195-1202` | `state_dir_unwritable` raises OSError so only the stderr fallback is written; `rotate_if_needed` only when locked | 1195 `if self.stop_reason == "state_dir_unwritable":`, 1196 `raise OSError("state_dir_unwritable")  # stderr only (FR-020)`, 1197 `if locked:`, 1198 `self.deps.audit.rotate_if_needed()`, 1202 `audit.stderr_fallback(...)` | MATCH |
| 01 | file count of `issue-watch` mentions | "20 files outside tests/ and .dev/" | `grep -rlIE 'issue-watch\|issue_watch'` excluding `.git`, `.dev`, `tests` = 20 files | MATCH |

### Research 02 (watcher I/O, GitHub calls, launch, record)

| File | Citation | Claimed | Actual | MATCH/MISMATCH |
|---|---|---|---|---|
| 02 | `P/launch.py:95-116` | 12-element launch argv `orca agent launch --agent claude --worktree path:<wt> --surface terminal --prompt <p> --json` | list literal lines 104-115 = 12 elements (`orca`, `"agent"`, `"launch"`, `"--agent"`, `ORCA_AGENT`, `"--worktree"`, `"path:..."`, `"--surface"`, `"terminal"`, `"--prompt"`, `prompt`, `"--json"`); 111-112 `"--surface"`, `"terminal"`; 115 `"--json"` | MATCH |
| 02 | `launch.py:33, 84-92` | `PROMPT_PATTERN = ^/sc:issue --claim [1-9][0-9]{0,8} --pipeline none$`; f-string at 92 | line 33 exactly that regex; 92 `return f"/sc:issue --claim {n} --pipeline none"`; 90-91 `type(n) is not int or not 1 <= n <= MAX_ISSUE_NUMBER` | MATCH |
| 02 | `launch.py:6, 177, 352-356` | `find_orca` and the launcher cache nothing | line 6 "This module writes no state and caches nothing"; 177 "The result is not cached here."; `OrcaLauncher.__init__` stores only `self._runner = runner` (356) | MATCH |
| 02 | `record.py:69-88`, `120-131` | `Entry` has 17 fields; store top-level 7 keys | 17 field lines (issue ... last_reason); `_STORE_KEYS` 120-130, `_ENTRY_KEYS = frozenset(Entry.__dataclass_fields__)` 131 | MATCH |
| 02 | `record.py:421-431` | `disabled()` is `os.path.lexists`; `disabled_since()` uses `os.stat` (follows symlinks) | 423 `return os.path.lexists(self.state_dir / DISABLED_FILE)`; 428 `mtime = os.stat(self.state_dir / DISABLED_FILE).st_mtime`, 429-430 `except FileNotFoundError: return None` | MATCH |
| 02 | `runner.py:10, 15, 70-130` | only `import subprocess`; `STDERR_CAP_BYTES = 500` | line 10 `import subprocess`; 15 `STDERR_CAP_BYTES = 500`; 87 `raise TypeError("argv must be a non-empty list of str")`; 91 `subprocess.run(` | MATCH |
| 02 | `swarm/atomic.py:14-39` | `write_prepared_bytes`: mkstemp in same dir, write, flush, fsync, `os.replace`, unlink on `Exception` | function read in full; identical | MATCH |
| 02 | `install_user_setup.py:36, 247-253` | `_ORCA_CLIS = ("orca-ide", "orca")` loop in `_find_orca` | line 36 `_ORCA_CLIS = ("orca-ide", "orca")`; 247 `def _find_orca()`, 253 `for name in _ORCA_CLIS:` | MATCH |
| 02 | fixtures dir | 19 files, 12,059 bytes; pinned by `test_github.py:575-583` | `ls \| wc -l` = 19; `cat * \| wc -c` = 12059; test line 577 `assert len(files) == 19` | MATCH |
| 02 | fixture use lines (21 sampled) | e.g. `test_github.py:1383` loads `gh_issue_list.json`; `conftest.py:788` loads `gh_api_user_include_429.json`; `test_launch.py:632` loads `orca_launch_success.json` | each sampled line prints the named `load("...")` call | MATCH (21 of 21) |
| 02 | test files lines/tests | test_github 2161/141; test_launch 952/66; test_record 2377/147; test_concurrency 275/6; test_crash_injection 373/6; test_find_orca_parity 288/10; test_origin_parity 179/7; test_runner 226/16; parametrize counts 47/21/53/6/5/1 | `wc -l` + `grep -c`: identical for all eight; `grep -c 'pytest.mark.parametrize'`: 47, 21, 53, 6, 5, 1 | MATCH |
| 02 | `audit.py:32-99` reason lines | origin_mismatch 32; gh_auth_failed 43; gh_timeout 44; gh_non_json 45; project_read_failed 46; truncated 48; rate_limited 51; lock_held 54; disabled 59; not_enabled 61; already_dispatched 76; budget_exhausted 79; prompt_invalid 84; reset_refused 99 | `grep -nE` gives 32, 33 (orca_not_found), 54, 57, 61, 76-80, 84-92, 99 as claimed; enumerated gaps for the rest are consistent with the printed table | MATCH |
| 02 | `docs/designs/orchestrator.md:368` | shows `MAX_LAUNCHES_PER_CYCLE` as `(35)` | line 368: `\| cycle.py \| MAX_LAUNCHES_PER_CYCLE (35) \| remove \| replaced by the new-since-last-poll rule ...` | MATCH |
| 02 | `test_find_orca_parity.py:13-18` cites `install_user_setup.py:216-219` | stale; real location 247-270 (`topics` read at 265, `any(...)` at 268) | docstring cites 216-219 and 219; `install_user_setup.py` lines 265 `topics = json.loads(probe.stdout).get("topics", [])` (inside the try) and 268 `if probe.returncode == 0 and any(t.get("name") == "orca-cli" for t in topics):` | MATCH (the stale-doc claim is true) |
| 02 | `record.py:748-750`, `test_record.py:861,870` | `disabled_present` is defined and only tests call it | `grep -rn 'disabled_present'` over `*.py`: record.py:748, test_record.py:861, 864, 870 only | MATCH |

### Research 03 (operator surface and setup)

| File | Citation | Claimed | Actual | MATCH/MISMATCH |
|---|---|---|---|---|
| 03 | `P/cli.py:31, 34-38` | `_DEFAULT_CONFIG = "~/.config/superclaude/issue-watch.json"`; `_EXIT_UNHEALTHY=1`, `_EXIT_CRASH=1`, `_EXIT_CONFIG=2`, `_EXIT_STORE=6`, `_EXIT_LOCK_HELD=75` | identical at those lines | MATCH |
| 03 | `cycle.py:71-75` | `_LABEL_MAX` 50; `_PROJECT_ID` `PVT_[A-Za-z0-9_-]{1,64}`; `_APPROVER_LINE` `[1-9][0-9]{0,19}`; `_ACCOUNT_ID_MAX` 10**20-1; `_APPROVERS_MAX_BYTES` 1 MiB | `_LABEL_MAX = 50`, `_PROJECT_ID = re.compile(r"PVT_[A-Za-z0-9_-]{1,64}")`, `_APPROVER_LINE = re.compile(r"[1-9][0-9]{0,19}")`, `_ACCOUNT_ID_MAX = 10**20 - 1`, `_APPROVERS_MAX_BYTES = 1024 * 1024` | MATCH |
| 03 | `cycle.py:1225-1406` SLO reducer | window 7 d; excluded {disabled, not_enabled}; p95 nearest rank `ceil(0.95 n)-1`; claimed share `at <= c < end` with `end = at + record.LEASE`; due iff `hit or now >= end` | read in full: `_SLO_WINDOW = timedelta(days=7)`, `_SLO_EXCLUDED_REASONS`, `waits[-(-95 * len(waits) // 100) - 1]`, `hit = any(at <= c < end ...)`, `if hit or now >= end:` | MATCH |
| 03 | `cycle.py:1251-1259`, `1270-1335` | `_is_stale`: `unknown` or `abandoned`+`pending_orphan`, older than 86400 s strict; `status_report` reads only `dispatch.json` and DISABLED mtime; `audit` argument unused | read in full; docstring 1279-1281 "``audit`` is accepted for the fixed signature and not read" | MATCH |
| 03 | `cli.py:77-91, 111-137, 164-182, 282-348` | verb line ranges and behaviours (`once` prints `cycle:`/`exit:` 130-131; `status` `platform=False` 169; `reset` arg checks 309-313; reset rotates=False on lock held 331) | each cited line printed the described statement | MATCH |
| 03 | `main.py:577-579` | deferred import and `main.add_command(issue_watch_group, name="issue-watch")` | lines 577 and 579 exact | MATCH |
| 03 | `docs/designs/issue-watcher.md:120, 125, 137, 154-155` | `once` exits "0, 2, 3, 4, 5, 6, 7, 75" (no 1); `reset --rate-limit` "0, 6, 75" (no 2); label rule omits comma/quote/dash; approvers rule omits 1 MiB/UTF-8 | all four lines read; text as claimed | MATCH |
| 03 | `docs/designs/issue-watcher-setup.md:170, 616-619, 53, 92, 93` | 170 names WORKER-CONTRACT "Issue pipeline duties"; 616-619 launch prompt without `--pipeline none`; 53 lists `reset`; 93 label rules complete | lines read as claimed | MATCH |
| 03 | `WORKER-CONTRACT.md:68` and absence greps | section 4 is "Coordinator rules"; 0 hits for `WC-17`, "issue pipeline", `watcher`, `COORD-`, `adopt`, `claim` | `grep -c` returned 0 for each; line 68 `## 4. Coordinator rules` | MATCH |
| 03 | test files lines/tests | cli 1672/60; cli_e2e 443/4; slo_helper 421/14; no_shell 266/9; no_text 971/22; security_invariants 1013/16; module_boundaries 413/13 | identical | MATCH |
| 03 | test names + lines (34 sampled) | e.g. `test_the_group_lists_exactly_the_five_commands__df06` (test_cli.py:279), `test_no_string_constant_of_github_py_contains_mutation` (test_security_invariants.py:894) | each printed the named `def` | MATCH (34 of 34) |
| 03 | `docs/designs/orchestrator.md:343, 992, 1022, 1381, 269`; `common.py:22-40`; `tests/skills/test_agent_work_report.py:2979-3000` | automation design 4.8, cron removal row, live-test record file, "Dropped: plan-approval gate", `orchestrator_repo` read from the poll config | all lines exist with that content; `common.py` reads `json.loads(path.read_text())["orchestrator_repo"]` from `~/.config/superclaude/issue-watch.json`; `_TOP_KEYS` (cycle.py:58-69) lacks that key and unknown keys raise at 216-220 | MATCH |
| 03 | `test_slo_helper.py` caller count | "tests/issue_watch/test_slo_helper.py only: 8 hits" | `grep -c 'slo_numbers' test_slo_helper.py` = 8 (the wider pattern `slo_numbers\|SloNumbers` gives 11 lines); production callers 0 (only `cycle.py:1339, 1359, 1401`) | MATCH |
| 03 | `dispatcher` hit count (F.2) | "114 hits in 35 files" | `grep -rI dispatcher` over `src docs plugins scripts`: 35 files, 114 lines | MATCH |
| 03 | "9 files" with the word `cron` in src/plugins/scripts/.github | 9 | `grep -rIliw cron` over those four trees = 9 files | MATCH |

### Research 04 (claim flow and Orca worktree)

| File | Citation | Claimed | Actual | MATCH/MISMATCH |
|---|---|---|---|---|
| 04 | `orca_worktree.py:822, 791-800` | `IR7_REFUSE = False`; `PENDING_PARTS`; `SHIM_TRIES = 5`; `SHIM_INTERVAL = 2.0`; `SHIM_TITLE` regex | line 822 `IR7_REFUSE = False  # IR-7: turn on only after the #442 observations pass (owner decision 2026-11-08)`; 791, 797-800 as claimed | MATCH |
| 04 | `orca_worktree.py:841-867` | `GOVERNED_TOOLS` = 14 names + 9 `mcp__x__*` = 23 | tuple read: 14 plain names, 9 `mcp__x__...` entries | MATCH |
| 04 | `orca_worktree.py:684-700` | `orca worktree create --repo path:<main> --name issue-<N> --base-branch <base> --no-parent --comment "sc:issue <R>#<N>" --json` | list literal exactly those elements, no `--agent`, `--issue`, `--pr` | MATCH |
| 04 | `orca_worktree.py:1776-1779, 210-223, 314-330` | launch argv with `[sc-launch:v1:<nonce>] Read .dev/issues/<N>/launch-prompt.md and follow it.`; preflight `orca status --json`; list `--limit 500` | lines read as claimed | MATCH |
| 04 | `orca_worktree.py:230-239` and `802-817` | 8 worktree warning codes in rank order; REMEDY has 4 launch codes | `WARNING_ORDER` 8 entries in the claimed order; REMEDY 802-817 | MATCH |
| 04 | `SK/templates/` count | 15 files (not 17) | `ls \| wc -l` = 15 | MATCH |
| 04 | agent files `model:` lines | t1 `claude-gw-tier1b`, t2 `claude-gw-tier2`, t3 `claude-gw-tier2b` at line 6; t3 `effort: low` line 7; tools line 5 | `sed -n 5,7p`: as claimed | MATCH |
| 04 | agent file sizes (section 3 table, "Lines" column) | "36" for each of `issue-worker-t1.md`, `-t2.md`, `-t3.md` | `wc -l` = 35 for each of the three (last line 35 is the "Return value" bullet) | MISMATCH (BLOCKING, finding B-2) |
| 04 | `launch-level-guard.sh:347` vs `launch-prompt.md:23` | guard regex has `sc:implement` and `task` only; prompt names `/sc:task` | line 347 `LL_RE_APR='^[[:space:]]*/(sc:implement\|task)([[:space:]]\|$)'`; `grep -c 'sc:task'` guard = 0; prompt line 23 "...first line starts `/sc:implement`, `/sc:task` or `/task`." Re-executed: prompt `/sc:task x` created no `.ok`; `/task x` created it | MATCH |
| 04 | test files lines/tests | test_issue_protocol 1055/62; orca_worktree 2501/109; repo_resolution 291/18; worker_agents 559/24; t1_fallback 69/8; l2_install 716/26; test_issue_command 212/15; issue_body_templates 97/5 | identical; classes 0/1/0/0/0/1/0/0 | MATCH |
| 04 | `clickup_claim.py:74, 232-237`; `origin_repo.py:61-63, 45-50` | `DEFAULT_MAX_PAGES = 20`; only write is `PUT /task/{id}` assignees add; exits 1/3/4 | lines read as claimed | MATCH |
| 04 | `pending` callers in `src/` | only `orca_worktree.py` itself; test caller `tests/hooks/test_launch_level_guard_worker.py:287` | `grep -rnE 'orca_worktree\.py[" ]+pending\|cmd_pending\|publish_pending\|pending --level' src`: only lines 7, 8, 1488, 1515, 1518, 1726, 1750, 1761, 1893 of orca_worktree.py; test line 287 `[sys.executable, str(SCRIPT), "pending", "--level", "worktree"]` | MATCH |
| 04 | `ccsession-models.json` tier keys | tier1b 85, tier2 93, tier2b 104, tier3 113 | `grep -nE` identical | MATCH |
| 04 | "SCRIPT imported from tests/skills/test_issue_orca_worktree.py:281" | citation of where `SCRIPT` comes from | the import statement is `tests/hooks/test_launch_level_guard_worker.py:281` (`from tests.skills.test_issue_orca_worktree import SCRIPT`); `tests/skills/test_issue_orca_worktree.py:281` is `NUMBER = 302` | location mislabelled, claim true, MINOR (M-3) |
| 04 | test names + lines (31 sampled) | e.g. `test_la1_launch_argument_list_is_exact` (1328), `test_ir7_shipped_switch_is_off` (test_issue_l2_install.py:639) | each printed the named `def` (the only non-def hit is the SCRIPT cite above) | MATCH (30 of 31) |

### Research 05 (guard stack and ccsession)

| File | Citation | Claimed | Actual | MATCH/MISMATCH |
|---|---|---|---|---|
| 05 | `launch-level-guard.sh:783-803` level grid | IMPL/TURN block at W only; COMMIT/PUSH/SUBMIT/SKILL block at W, WA, F, allow at FS; REPO, PUSHFORM, PROTECTED, MERGE, GHWRITE, UNKNOWN, MCP, ESCAPE, TAMPER, BIG block at all four | read lines 783-803: `IMPL:WA \| IMPL:F \| IMPL:FS \| TURN:WA ...;;`, `SUBMIT:FS \| COMMIT:FS \| PUSH:FS \| SKILL:FS) ;;`, then the deny rows exactly as claimed; precedence list `BIG TAMPER MERGE GHWRITE PROTECTED ESCAPE MCP UNKNOWN SUBMIT REPO PUSH PUSHFORM COMMIT TURN IMPL SKILL` (16 classes) | MATCH |
| 05 | guard `:408-413` skill classifier | `implement \| task \| cleanup` -> IMPL; `pr-submit` -> SUBMIT; `issue` -> ESCAPE; empty -> SKILL | lines 408-413 exact | MATCH |
| 05 | guard `:318, 347-359, 372-376, 299-305, 265-272` | marker regex `\[sc-launch:v1:([0-9a-f]{32})\]`; approval regex; `mv` to `.take-<sid>`; `ln`; level words | each cited line printed as claimed | MATCH |
| 05 | `hooks.json` (192 lines) registrations | guard on UserPromptSubmit (timeout 5) and PreToolUse (matcher line 116); identity on PreToolUse `Bash` after the guard (125-134); no `onFailure` | `grep -nE` shows commands/timeouts at lines 67-68, 120-121, 130-131; matcher at 116 | MATCH |
| 05 | plugin copies | plugin hooks.json 154 lines, differs by ccsession-tag entries, `pragmatic-subagent.js`, `async: true`; 3 launch scripts byte-identical | `diff` shows exactly those differences; `cmp -s` identical for all three scripts | MATCH |
| 05 | script sizes | guard 808, identity 582, pre-push 208, install_hooks 614, install_ccsession 161, ccsession-orca 263 | `wc -l` identical | MATCH |
| 05 | pre-push hook lines | shebang `#!/bin/bash -p` (1), version line (2), `L2_PROTECTED=(refs/heads/main refs/heads/master)` (17), actor/exit 197-208 | lines read as claimed; line 208 `exit 1` | MATCH |
| 05 | `test_launch_level_observations.py:79-84` | `_PENDING` = 12 cases (OB-H1 items 1-9, OB-H2, OB-H3, OB-CTX); body `pytest.skip(...)` | line 79 `_PENDING = [f"OB-H1 item {n}" for n in range(1, 10)] + ["OB-H2", "OB-H3", "OB-CTX"]`; line 84 `pytest.skip(f"{item}: needs a real governed session and has not been run")` | MATCH |
| 05 | test files lines/tests | guard 4631/162; l2_tokens 160/7; registration 127/7; with_identity 212/5; worker 300/11; job_identity 1530/56 (2 classes); pre_push 1194/34 (2); pre_push_records 230/8 (1); observations 84/6; install_hooks 1246/37; install_ccsession 417/22; ccsession_tag 7101/277 (1); ccsession_tiers 3821/149 (4); launch_guidance 62/3; governed 56/1 | identical for all fifteen | MATCH |
| 05 | test names + lines (50 sampled) | e.g. `test_grid_policy` (3394), `test_design_table_holds_all_eighteen_ids` (1712), `test_ir7_shipped_switch_is_off` | each printed the named `def` | MATCH (50 of 50) |
| 05 | `orca-ide` not recognised by the guard (EXTRA-2/3) | `orca-ide terminal send` exits 0 | independent re-run in my own temp HOME: `sw \| orca-ide terminal send --text hi -> rc=0`; `orca terminal send` -> rc=2 | MATCH |
| 05 | `cli/sweep/probes.py:43` | `ORCA_BINARY_DEFAULT = "orca-ide"` | line 43 exact | MATCH |
| 05 | Observation run totals (section "Observation run") | 44 payloads (40 in `run-guard-observation.sh` + 4 in `run-guard-extra.sh`), 16 of them the level matrix | `observation-output.txt` prints `CASES: 40` and four `EXTRA` lines; `out/` holds 40 case names plus `extra`; the 16 `M-*` cases are present | MATCH |
| 05 | Key Takeaways line 355 (count of test files) | "16 test files plus claim-side pins cover the area" | section 11.1 table has 14 rows (`grep -cE '^\| (hooks\|cli\|unit\|core)/'` = 14); the claim-side pins named below it are 3 further files; no reading gives 16 | MISMATCH (BLOCKING, finding B-3) |
| 05 | design `sc-issue-launch-level-hook.md:106, 123, 189, 236, 391` | six-skill IMPL list; row 34 typed `approved`; line 189 only `/(sc:implement\|task)` | lines read as claimed | MATCH |

### Research 06 (coordinator text and removed code)

| File | Citation | Claimed | Actual | MATCH/MISMATCH |
|---|---|---|---|---|
| 06 | `WORKER-CONTRACT.md` structure | 339 lines; `## 1. Terms` 9, `## 2` 27, `## 3` 49, `## 4. Coordinator rules` 68, `## 5` 299; WC-6 at 72, WC-16 at 287; no WC-1, no WC-17 | `grep -n` identical; `grep -c 'WC-17'` = 0 | MATCH |
| 06 | `WORKER-CONTRACT.md:23, 57, 66, 242-243` | `/sc:issue` on never-as-worker list; "grant row"; "Messages carry no `--to`"; progress posts are coordinator actions | lines printed as claimed | MATCH |
| 06 | `tests/skills/test_worker_contract.py` | 3,220 lines, 59 tests; `RULE_PHRASES` at 25; last test at 3216 | `wc -l` 3220; `grep -c` 59; line 25 `RULE_PHRASES = {`; 3216 `def test_the_no_to_rule_sits_in_the_worker_session_duties():` | MATCH |
| 06 | commit `01e7a9e23` | 2026-11-19 18:02:35 -0600, PR 682; 36 files; contract +1/-12 | `git log -1`: `2026-11-19 18:02:35 -0600 refactor: retire the old plan-approval gate (issue 655, PR D) (#682)`; stat: 36 files, 35 insertions, 4599 deletions; WORKER-CONTRACT.md `13 +---` | MATCH |
| 06 | removed package line counts | 5/62/416/74/395/90/161/66/301/27 (=1,597) | `git show 01e7a9e23^:<path> \| wc -l` identical for all ten | MATCH |
| 06 | removed tests | 10 files: lines 78/88/135/424/224/116/295/89/466/476, tests 2/3/9/21/12/10/10/7/29/13 (=116); registration test 15 lines/1 test | `git show ... \| wc -l` and `grep -cE '^\s*def test_'` identical | MATCH |
| 06 | `plan_hash.py` | 11 closed reason words (24-36); 8-byte big-endian length framing (87-89) | REASONS tuple lists the 11 words; `digest.update(len(raw).to_bytes(8, "big") + raw)` | MATCH |
| 06 | `approval_line.py` | `SHORT = "approved"`, `_LONG` regex `approved (ap-([1-9][0-9]*)-plan-([0-9a-f]{12})) plan-sha256=([0-9a-f]{64})`; check order malformed, bare, plan-hash reason, mismatch, ok | lines 18-26, 29-30, 43-62 as claimed | MATCH |
| 06 | `release.py` | creates `<store>/sessions/<sid>.ok` with `O_WRONLY\|O_CREAT\|O_EXCL\|O_NOFOLLOW`, 0o600; first 13 bytes must be `worktree`/`worktree\n` | lines 53-64 as claimed | MATCH |
| 06 | `cli.py` @`01e7a9e23^` | 10 verbs; exit constants 29-32 | decorators at 61, 76, 96, 108, 117, 134, 161, 179, 200, 335 (10); `_EXIT_REFUSED=1`, `_EXIT_CONFIG=2`, `_EXIT_LOCK_HELD=75` | MATCH |
| 06 | old guard `:428, 441-444` | TAMPER case for `release-worker`, `issue-pipeline*adopt-`, `*record-`, `issue_pipeline*release`, `*approval_record*` | line 444 `case $T in *release-worker* \| *release_worker* \| *issue-pipeline*adopt-* \| *issue-pipeline*record-* \| *issue_pipeline*release* \| *issue_pipeline*approval_record*) LL_CLASSES+='TAMPER ' ;; esac`; old file 811 lines | MATCH |
| 06 | old `WORKER-CONTRACT.md` | 350 lines; WC-17 at l.59; "### Issue pipeline duties" l.291-300 with six bullets; "grant row" twice; no `COORD-` | `git show` + `sed`: as claimed | MATCH |
| 06 | old tests changed | `test_worker_contract.py` 3181 lines/61 tests (current 3220/59); guard-worker test 330/13 (current 300/11); `RULE_PHRASES` keys `issue-pipeline-duties` (423) and `wc17-plan-approval` (436); `from superclaude.cli.issue_pipeline import release` at l.15 | identical | MATCH |
| 06 | old `main.py` | registration lines 581 and 583 (pipeline), 577-579 (watch) | printed lines 577-583 as claimed | MATCH |
| 06 | `CHANGELOG.md:17`; `SUPERVISED-ORCHESTRATION-TECHNICAL-REFERENCE.md:268` | removal recorded; "no contract rule says who starts that worker" | CHANGELOG line 17 exact; line 268 contains "The contract's coordinator duties for this hand-off (the section "Issue pipeline duties") were removed in issue 655, PR D; the or..." (read to 500 characters) | MATCH |

Totals of the sample table: 93 rows covering 480+ individual re-read citations (rows marked "N of N" aggregate the individual lines). Rows per research file: 01 = 18, 02 = 15, 03 = 15, 04 = 15, 05 = 15, 06 = 15 (the requirement was at least 6 per file and at least 40 in total). Result: 89 rows MATCH, 3 rows MISMATCH (B-1, B-2, B-3: wrong counts, BLOCKING by the grading rule), 1 row MATCH with a mislabelled location on a true claim (M-3, MINOR).

---

## Test-pin table verification (process step 4)

Every test-pin row in the six files was checked (not just 3 per file): path exists, `wc -l`, and `grep -cE '^\s*(async )?def test_'`; classes via `grep -cE '^class '`.

| Research file | Rows checked | Result |
|---|---|---|
| 01 | 5 (test_cycle, test_predicates, test_audit, test_marker_contract, conftest) | all line and test counts equal |
| 02 | 11 (github, launch, record, concurrency, crash_injection, find_orca_parity, origin_parity, runner, fixtures dir; plus parametrize counts 47/21/53/6/5/1) | all equal |
| 03 | 7 (cli, cli_e2e, slo_helper, no_shell, no_text, security_invariants, module_boundaries) | all equal |
| 04 | 8 (issue_protocol 1055/62, orca_worktree 2501/109, repo_resolution 291/18, worker_agents 559/24, t1_fallback 69/8, l2_install 716/26, issue_command 212/15, issue_body_templates 97/5) | all equal |
| 05 | 15 hook, installer, ccsession and guidance test files | all equal |
| 06 | 12 (current `test_worker_contract.py` 3220/59, `test_launch_level_guard_worker.py` 300/11, ten removed files 78..476 lines with 2..29 tests, registration test 15/1; old `test_worker_contract.py` 3181/61 and old guard-worker test 330/13 via `git show`) | all equal; the 116-test sum is exact |

No test was executed by this QA run (no pytest: it would write caches), so "pins" means what the tests assert by reading; the research files make the same statement.

## Independent re-execution (guard, read-only on the snapshot)

I ran `bash /home/coder/.cache/ic-snap-20261120/master/src/superclaude/hooks/scripts/launch-level-guard.sh` with `env -i HOME=<private /tmp dir> PATH=/usr/bin:/bin`, binding three sessions through the real marker path (`pending/<nonce>` + `[sc-launch:v1:<nonce>]` prompt). Results, all equal to the research 04/05 claims:

| Payload | Level | Exit | Research claim |
|---|---|---|---|
| Skill `sc:implement` | W / F | 2 / 0 | IMPL blocked at W only |
| `git commit -m x` | FS / F | 0 / 2 | COMMIT allowed only at FS |
| `git push origin main` | FS | 2 | PROTECTED at every level |
| `git push -u origin feature` | FS | 0 | canonical push allowed at FS |
| `gh pr merge 5 --repo IronbellyOrg/IronClaude` | FS | 2 | MERGE at every level |
| `orca terminal send --text hi` | W | 2 | ESCAPE |
| `orca-ide terminal send --text hi` | W | 0 | the guard does not recognise `orca-ide` (DC-5) |
| `orca orchestration send --type heartbeat --body hi --json` | W | 0 | G2 rule 2 allows without `--to` |
| `orca orchestration send --to run:r1 --body hi` | W | 2 | `--to` blocked |
| prompt `/sc:task x` at W | W | no `.ok` file | `/sc:task` does not release (contradicts `launch-prompt.md:23`) |
| prompt `/task x` at W | W | `.ok` file created | typed approval path |
| `git commit` / Skill `sc:implement` after approval | WA | 2 / 0 | WA allows IMPL, still blocks COMMIT |

The throwaway HOME under `/tmp/ironclaude-batch.*` was removed by the script's `rm -rf` after each call.

## Checks performed (10-item research gate checklist)

| # | Check | Result | Evidence |
|---|---|---|---|
| 1 | File inventory | PASS | six files `01`..`06`, each has `**Status:** Complete` (line 4) and a `## Summary` section (01 line 654, 02 line 470, 03 line 494, 04 line 494, 05 line 499, 06 line 396); no `gap-fill-*.md` exists |
| 2 | Evidence density | PASS (Dense, above 80 percent) | every table row and section carries path:line; 480+ citations re-read; 3 wrong counts (B-1..B-3) and 1 mislabelled location (M-3) found, no wrong path, argv, constant value, exit code, state name, reason word or field name found |
| 3 | Scope coverage of research-notes EXISTING_FILES | PASS | every listed file/group is discussed: watcher modules (01 cycle/predicates/audit, 02 github/launch/record/runner, 03 cli and config); claim command, skill, refs, three scripts, three agents, templates (04); guard, identity, pre-push, hooks.json, install_hooks, install_ccsession, ccsession-orca (05); WORKER-CONTRACT and removed tree (06); every test group in the notes has a pin row |
| 4 | Documentation cross-validation | PASS | doc-sourced claims carry [CODE-VERIFIED], [CODE-CONTRADICTED] or [UNVERIFIED]; I re-read the code for 70+ sampled [CODE-VERIFIED] and [CODE-CONTRADICTED] claims (for example the `/sc:task` approval mismatch, plugin hooks.json diff, exit-7 combination argument, WC-17 removal) and all were true |
| 5 | Contradictions between files | PASS | none unresolved: constants and the dead `MAX_LAUNCHES_PER_CYCLE` agree across 01/02/03; `pending` has no production caller in 02, 04, 05; `IR7_REFUSE = False` agrees in 04/05; prompt `--pipeline none` agrees in 01-04; the "20 files" (01) versus "16 files" (03) counts cover different scopes (03 excludes the package and the two design docs and includes two test files) and both reproduce |
| 6 | Gap severity | PASS | all [UNVERIFIED] gaps are external or live behaviour (Orca reply shapes, `gh` stderr text, PR numbers, owner-run live test) and are tagged; the one content gap, templates and create-mode files not read (04 Gap 9), is MINOR because the reference is about the claim flow |
| 7 | Depth appropriate for Standard | PASS | file-level coverage plus traced flows: one full poll cycle with 15 ordered gates (01), claim waves 0-8 with actors (04), the guard binding state machine and level grid (05), removed approval flow end to end (06) |
| 8 | Integration points | PASS | watcher to Orca argv to claim marker to later G4 read (02, 01); claim to `pending/<nonce>` to guard (04, 05); hooks.json and installer to settings.json (05); config file shared with `agent-work-report` (01, 03) |
| 9 | Patterns and conventions | PASS | closed vocabularies, write-ahead `pending`, single subprocess module, exit 0/2 hooks, level by files not env, plugin byte-identity, extension recipes in 01, 02, 04 |
| 10 | Incremental writing | PASS (structural evidence only) | forward references and appended sections (03 B.1 "see B.8", 04 section 8.7 "listed in 8.8", 05 "Observation run" after section 12), per-section Key Takeaways; file mtimes (05:31 to 05:35) cannot show start times, so this rests on structure |

## Findings

All findings are about the six research files unless stated. BLOCKING items are one-line fixes, but they are wrong counts in prose that a synthesis agent can copy into the reference, and the grading rule lists wrong counts as BLOCKING.

| ID | Severity | Research file and location | Claim as written | Evidence (source path:line) | Required fix |
|---|---|---|---|---|---|
| B-1 | BLOCKING | `research/01-watcher-decision-engine.md`, section 1 Key Takeaways, line 34 | "13 constants at lines 34-47; 12 are read, `MAX_LAUNCHES_PER_CYCLE` is dead" | `SNAP/src/superclaude/cli/issue_watch/cycle.py:34-47` is 14 assignments (`sed -n 34,47p`); the file's own section 1 table (lines 12-27) has 14 rows; 13 are read (HEALTH_AGE_S at 1327 and STALE_AGE_S at 1259 only by the status report) and 1 is dead | change to "14 constants at lines 34-47; 13 are read (two of them, `HEALTH_AGE_S` and `STALE_AGE_S`, only by the status report); `MAX_LAUNCHES_PER_CYCLE` is dead (cycle.py:35 only)"; also check the research-notes line 22 wording and any synthesis text that says 13 or 12 |
| B-2 | BLOCKING | `research/04-claim-flow-and-orca-worktree.md`, section 3 table, "Lines" column, rows `issue-worker-t1.md`, `-t2.md`, `-t3.md` | each file has "36" lines | `wc -l SNAP/src/superclaude/agents/issue-worker-t1.md` = 35, `-t2` = 35, `-t3` = 35 | change all three to 35 |
| B-3 | BLOCKING | `research/05-guard-stack-and-ccsession.md`, section 11 Key Takeaways, line 355 | "16 test files plus claim-side pins cover the area" | section 11.1 has 14 rows, one per test file of the assignment (guard 5, identity 1, pre-push 2, observations 1, install_hooks 1, install_ccsession 1, ccsession_tag 1, ccsession_tiers 1, launch_guidance 1); the claim-side pins listed under the table are 3 more files (`test_issue_l2_install.py`, `test_issue_orca_worktree.py`, `test_require_orca_worktree_agent_governed.py`) | change to "14 test files in the table plus 3 claim-side pin files" (or drop the number) |
| M-3 | MINOR | `research/04-...md`, section 8.7 "Callers of `pending`" | "SCRIPT imported from tests/skills/test_issue_orca_worktree.py:281" | the import statement is `tests/hooks/test_launch_level_guard_worker.py:281`; `tests/skills/test_issue_orca_worktree.py:281` is `NUMBER = 302`; the claim itself (the only caller of `pending` is a test) is true | write "imported at tests/hooks/test_launch_level_guard_worker.py:281" |
| M-4 | MINOR | `research-notes.md` (not one of the six files; read for checklist item 3) lines 19, 27, 39 | "4,389 lines in 8 modules"; `REASON_TABLE` "l.24-96"; templates "(17 files)" | module line counts sum to 4,795 (404+348+1406+960+370+312+865+130, `wc -l`); `REASON_TABLE` is `audit.py:26-102`; `ls templates` = 15 (research 04 already says so) | correct the three figures in `research-notes.md`, or tell synthesis agents to take figures only from the research files |
| M-5 | MINOR (propagation risk) | `research/02` (9 lines), `03` (12), `05` (12), `06` (6), `01` (1) mention `docs/designs/orchestrator.md` | e.g. 02 section N-4, rows D-2 and gap 12; 03 F.2 "Orca automation" row and defect row 3; 05 DC-1 "recorded decision ... orchestrator.md:117 (DQ7)"; 06 D1, D2, D5 | `research-notes.md` line 13 and the task prompts forbid describing the rewrite design anywhere in the reference; 02 N-4 itself says "PR 686 / Clay design is out of scope"; `orchestrator.md:3` header: "approved by the owner (Clay) ... holds no implementation code" | no change to the research files is needed (they cite it only as evidence); synthesis briefs must not carry those rows, and any "recorded decision" column that rests only on `orchestrator.md` must be reworded to "no decision found in the files this reference cites" |

No finding in the "fabricated or non-existent path" class: every cited path exists in the snapshot (or, for the removed tree, in `01e7a9e23^`), and no cited line number lies beyond its file length.

Notes that are not findings: (a) research 01 reads some test bodies selectively (its Gap 17) and 02 to 06 did not run any test; the research files say so; (b) `sc-issue-command.md` still says "Design only" and other stale-doc rows were all confirmed true by me (status line 3, T3 pin, Wave 0 text at 154-158); (c) 05's claim that the plugin `hooks.json` differs from `src` by more than the scope hint said is true (three differences, reproduced with `diff`).

## Summary

- Checks passed: 10 / 10 checklist items; findings: 3 BLOCKING (B-1, B-2, B-3), 3 MINOR (M-3, M-4, M-5)
- Citations re-verified: 480+ (93 rows in the sample table; at least 15 per file); MATCH 89 rows, MISMATCH 3 rows, 1 row mislabelled location
- Re-execution of the unmodified guard: 18 payloads, all equal to the research claims
- Fixes applied: 0 (fix authorization is false; no research file was modified)

## Confidence Gate

- **Confidence:** Verified: 10/10 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 27 | Grep: 9 | Glob: 1 | Bash: 31 (26 multi-check batch scripts under `/tmp`, removed after each call, plus 5 single-purpose calls). Web research: none (no external claim needed it; tavily_search: 0 | tavily_extract: 0 | web_search_fallback: 0 | web_fetch_fallback: 0).
- UNCHECKED items: none. UNVERIFIABLE items: none for the checklist. Limits of this review (not checklist items): I did not run the repository test suites, did not re-run the identity hook, the L2 pre-push hook, `orca`, `gh` or any live tool, and did not re-read every one of the several thousand line citations: the sample covered every argv, constant block, exit-code table, reason-table tally, level-matrix cell, test-pin row and count, removed-tree line count and the highest-risk doc-vs-code contradictions.

## Recommendations

1. Fix B-1, B-2 and B-3 in the three research files (one line each), then re-run only a diff check of those three lines; no other re-verification is needed because nothing else was wrong.
2. Correct `research-notes.md` (M-4) or instruct synthesis agents to prefer the research files over the notes for numbers.
3. Keep the `orchestrator.md`-based rows out of the synthesis briefs (M-5).

## Verdict: FAIL

3 BLOCKING findings (B-1, B-2, B-3), all wrong counts; every other claim checked was true.

Status: Complete
