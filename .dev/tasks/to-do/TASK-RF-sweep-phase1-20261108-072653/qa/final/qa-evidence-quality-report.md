# QA Final Gate: Evidence-Quality Lens

Reviewer: qa-final (evidence-quality lens). fix_authorization: false.
Date: 2026-11-12

## Findings

Method: every Orca fact in `src/superclaude/cli/sweep/*.py`, `sweep.md`, `SKILL.md`, the WC-16 text, `HOW-WE-WORK.md`, `CHANGELOG.md` and DESIGN was traced to `artifacts/readonly-probe.md`, `phase-outputs/discovery/1.0a-facts.md`, a file in `tests/sweep/fixtures/` (re-read with `jq`, not taken from SOURCES.md) or a file line at HEAD. OQ-13 (task file line 3032) lists: live field names and time format, where `completedAt` is written, the session-to-Dispatch join key, the `page.nextCursor` shape. Repository facts (31 `UNATTENDED_EXPECT` entries, 168 `src/superclaude` hits) were recounted on disk.

### BLOCKING

**EQ-F1. The Orca agent-wait field, the live value names `live` and `in_progress`, and the wait-time keys are coded as known. The capture records them as STILL UNVERIFIED.**

- Evidence of the gap:
  - `phase-outputs/discovery/1.0a-facts.md:16` (row 6): `agentWait` is ABSENT from all 5 `worker-show` outputs (all 5 workers had exited); the value `in_progress` "was not seen"; the row ends "Behaviour until closed applies: Rule 5 cannot match; rows fall to the fallback". The same file's field table (line 35) says "`agentWait` ... live name UNVERIFIED".
  - `jq` over `tests/sweep/fixtures/captured-worker-show-1.json` shows `result.observation = {"status":"exited","exactWorker":true}` and no `agentWait` key anywhere; `grep -c agentWait tests/sweep/fixtures/captured-*.json` returns 0 for every file. `liveness.verdict` is only ever `exited`, `dispatch.status` only ever `completed` in all 5 fixtures.
  - DESIGN `docs/designs/orchestrator-mode.md:996` (open item 6): until closed, "Rule 5 cannot match; rows fall to the fallback".
- What the code does instead:
  - `src/superclaude/cli/sweep/probes.py:461-474` searches two guessed places (`projection` and the result root) for a key `agentWait`; `probes.py:477-488` reads a wait time from six guessed keys (`since`, `waitingSince`, `timestamp`, `at`, `createdAt`, `startedAt`); the comments at lines 461 and 477 admit "not observed" and "not captured live yet".
  - `classify.py:225-235` (Rule 4a) classifies a session as `waiting on a person` whenever the guessed value is non-null, with the evidence text "agent_wait is non-null (worker-show agentWait)".
  - `classify.py:250-262` (Rule 5) classifies `working` when `liveness_verdict == "live"`, `status == "in_progress"`, and the guessed key is present and null. Neither string value was ever observed. This is the opposite of the DESIGN "cannot match" behaviour and nothing in the code gates it.
  - DESIGN line 491 states these names were "captured at step 1.0a"; the capture shows they were not.
- No tell-tale for the reader: the report caveat (`report.py:36-39` SP24_LINE), `sweep.md:16` and `SKILL.md:26` say only "stalled and fenced are not observed in Phase 1". Nothing tells the reader that `working` and the Orca wait signal were never seen live. `tests/sweep/test_classify.py:277-282` builds Rule 5 inputs from these names with no marker that they are guesses.
- Why it matters: Rule 4a can print a false `waiting on a person` row if the real `agentWait` key exists with another meaning (a non-null object that is not a wait). OQ-13 says "No code item may treat these as facts before `artifacts/readonly-probe.md` records them"; the probe file does not record them.
- Smallest fix: until a read-only capture of a live worker records the names (then add a `captured-*` fixture and update 1.0a-facts row 6), make Rule 4(a) and Rule 5 not match, as DESIGN item 6 requires, and delete the guessed `_WAIT_TIME_KEYS` list. Alternative if the owner wants the rules live: capture one live worker's `worker-show` and `worktree ps --agent-wait` output into `readonly-probe.md` and pin the observed names.

### MINOR (notes, not rechecked, do not fail the gate)

**EQ-F2. Project-folder key rule has no recorded evidence.** `probes.py:1002-1004` maps a worktree path to `~/.claude/projects/<key>` by replacing every non-alphanumeric character with `-`, and `probes.py:1367-1368` depends on it. `1.0a-facts.md:23` (row 16) still says UNVERIFIED and "not covered by any probe section". Partial support exists: the saved live check (`artifacts/sweep-live-check-1.4-rerun-9.14.json`, `sources[]`) shows `claude project -home-coder-workspaces-...` folders found with file counts, and `ls ~/.claude/projects` on this host shows `--dev-` for `.dev` paths. Those do not appear in any evidence file for the dot and underscore cases, and `tests/sweep/conftest.py:288` builds its fixtures with the same regex, so no test can catch a wrong rule. A wrong rule fails safe (`no folder`). Fix: record the `ls` observation in the probe file or 1.0a-facts row 16.

**EQ-F3. DESIGN still says UNVERIFIED for facts the capture closed.** `docs/designs/orchestrator-mode.md:30` (old build suffix `780594c521aa`, dated 2026-11-08 so true when written), `:457` ("`session_join` ... None until step 1.0a names the field"; item 23 UNVERIFIED), `:521` (id regexes "UNVERIFIED today"), `:1013` (item 23, "no path-B join is made") and the whole section 17 ("Total: 23 open items") were not updated for rows 1, 2, 4, 5, 7, 8, 10, 11, 15, 22, 23 that `1.0a-facts.md` marks CLOSED. The code follows 1.0a-facts, so DESIGN and code now disagree on the join behaviour. Fix: add a pointer from section 17 to `phase-outputs/discovery/1.0a-facts.md` as the closure record.

**EQ-F4. A follow-up from 1.0a-facts was applied only in part.** `1.0a-facts.md:48` says item 10.5 must test the live string `1.4.245-aidev02.9cfecdd30b2a`. `tests/sweep/test_report.py:908` still uses the old suffix `780594c521aa`. The comparison rule (`report.py:146`, text before the first `-`) is right and the other two cases (`1.4.246`, missing file) are present, so behaviour is covered.

**EQ-F5. "creator not observable" is wider than the evidence.** `report.py:283` (heading), `classify.py:245` (evidence text) and DESIGN `:624` say the Task creator is not observable. `1.0a-facts.md:17` (row 7) and `jq '.result.tasks[0]|keys' captured-task-list.json` show `created_by_terminal_handle`, `created_by_pane_key` on every completed Task. It was never observed on a ready Task (the captured `--ready` list is empty), and Phase 1 does not read the field, so "not read in Phase 1" would be exact. Fix: reword.

**EQ-F6. Three things are coded or documented from text, not capture, and the code comment does not say so.** (a) The bound `run-current` output (row 3): `probes.py:231-240` accepts exactly one `run_<12 hex>` in plain text; `sweep.md:27,37` document the bound-Run default; `tests/sweep/test_probes_allowlist.py:759-762` honestly states no test pins the bound shape. (b) The `runtime_unavailable` marker (`probes.py:271-273`, row 9, DESIGN item 9) comes from SPEC text and synthetic tests only. (c) The effect of `uv run --frozen --no-sync` (DESIGN item 18; `SKILL.md:24`, `SKILL.md:4`): step 1.29 ran only `pipx run`; the flags exist in `uv run --help` (uv 0.11.8, checked now) but the form was never run. All three fail safe and are disclosed in DESIGN section 17 or the tests.

### Verified with evidence (no finding)

- 31 `UNATTENDED_EXPECT` entries: `tests/skills/test_worker_contract.py:1575` asserts it and the dict at 448-756 holds 31 keys; `sweep` is excluded (`:1333`); DESIGN `:696` states the same.
- 168 `src/superclaude` hits: 168 now (`grep -rn ... | wc -l`) and 168 at the base (`git grep ... $BASE`); 0 hits in the new and edited primitives; `step-1.28-grep.md` agrees.
- DESIGN anchors checked at the base: `main.py` 563/565/568, `_check_p2_set` 1556 and the 31 assertion 1564, `ccsession:1889`, `recommend/__init__.py:12-20`.
- Orca fields used and observed: `dispatch.assigneeHandle`, `dispatch.dispatchedAt` (`YYYY-MM-DD HH:MM:SS`), `dispatch.completedAt` (ISO with `Z` and ms), `dispatch.status`, `projection.liveness.verdict`, `projection.outcome`, `projection.parent`, `projection.resource.terminalState`, `projection.nextAction.kind`, `terminal.worktreePath` (all present in `captured-worker-show-1.json`); `result.page` = `{limit 100, total, hasMore, nextCursor}`; `worktrees[].path`; unknown-Run shapes (`worker-list` exit 0 empty, `task-list` exit 1 `run_not_found`).
- Join: for all 5 workers, `assigneeHandle` equals tab-map line 3 and `assigneePaneKey` with `:` as `+` equals the tab-map file name (checked with `jq` and shell compare, 5 of 5).
- Version rule: `report.py:146` matches row 15 of 1.0a-facts; `probes.py:67` reads the file the probe read (`readonly-probe.md:999`).
- Phase 14 failures: argument holds. `.venv/bin` and site-packages hold no `ruff` (empty listing), `pyproject.toml:54` pins `ruff==0.15.20`, `git diff --stat $BASE` over `src/superclaude/cli/eval`, `tests/cli/eval`, `tests/hooks`, `src/superclaude/hooks` is empty, and the 1 MB test asserts `worst < 1.0` s (`tests/hooks/test_launch_level_guard.py:1280`), a timing limit.
- Re-run now: `uv run pytest tests/sweep tests/commands/test_sweep_command.py tests/skills/test_worker_contract.py tests/core/test_how_we_work_routing_table.py tests/recommend/test_routing_refresh.py` gives 1763 passed; `ruff check` and `ruff format --check` clean on the sweep package and its tests; `make verify-sync` reports all in sync.

## Checks

| Check | Subject | Result |
|---|---|---|
| C1 | Join key (`assigneeHandle` = tab-map line 3; pane key `:` as `+` = file name), 5 of 5 fixtures | PASS |
| C2 | Time fields and forms (`dispatchedAt`, `completedAt`), where `completedAt` is written | PASS (completed rows only; failed/circuit_broken unobserved, not used by code) |
| C3 | `worker-list` page object and `nextCursor` shape; no cursor template used | PASS |
| C4 | Unknown-Run shapes for `worker-list` and `task-list` | PASS |
| C5 | Worktree path field, version-file read and prefix comparison rule | PASS |
| C6 | Orca fields the parser reads exist in captured fixtures (`projection.*`, `terminal.worktreePath`, `dispatch.*`) | PASS |
| C7 | OQ-13 names (`agentWait`, live value names, wait-time keys) not treated as known by code | FAIL (EQ-F1) |
| C8 | Project-folder key rule evidenced | PASS with note (EQ-F2, MINOR) |
| C9 | DESIGN agrees with the closure record `1.0a-facts.md` | FAIL, MINOR only (EQ-F3) |
| C10 | 1.0a-facts follow-up for the live version string applied | FAIL, MINOR only (EQ-F4) |
| C11 | Task-creator statements match capture | FAIL, MINOR only (EQ-F5) |
| C12 | Unobserved shapes (bound `run-current`, `runtime_unavailable`, `uv run --frozen --no-sync`) disclosed | PASS with note (EQ-F6, MINOR) |
| C13 | 31 `UNATTENDED_EXPECT` entries | PASS |
| C14 | 168 `src/superclaude` count, now and at base; 0 hits in new primitives | PASS |
| C15 | DESIGN and 1.0a-facts line anchors checked at the base | PASS |
| C16 | Phase 14 failure argument (3 failures pre-existing or environment-caused) | PASS |
| C17 | Re-run of tests, ruff check, ruff format --check, `make verify-sync` | PASS |

Verdict: FAIL
Blocking count: 1
