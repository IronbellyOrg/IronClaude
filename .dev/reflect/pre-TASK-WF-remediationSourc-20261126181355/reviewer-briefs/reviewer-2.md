# Reviewer brief 2 (qa)

## T1 card excerpt

## Coverage
- Pass 1 ids: 0. Pass 2 inferred rows: 69 (55 from the earlier spec text plus 14 from the appended Reflect Verdict State section); all quotes re-found in the cited lines, 0 dropped.
- Deterministic containment match: 60 of 69 (coverage_pct_union 0.8696; coverage_pct null); S_dev_density 0.1304.
- Unmatched by the string rule: INF-006, INF-008, INF-016, INF-027, INF-032, INF-053, INF-054, INF-055, INF-061; on a manual read each is covered by a task or the Constraints (word-choice misses).
- coverage_degraded parsed-sparse: Tier 2 forced.
## Candidate prior-blocker status (to be confirmed by the reviewers)
- B-1 import rule: Task 2 and the Constraints now allow exactly RUN_ID_RE and parse_time, with test_ledger_imports_only_allowed_probes_names.
- B-2 Task 10 check limited to `superclaude` commands and flags.
- B-3 Task 11 ends with `git add .dev/tasks`.
- B-4 Task 6 updates the exact-text cases in tests/sweep/test_cli_contract.py.
- B-5 Task 9 updates the install test seed list.
- B-6 Tasks 1 and 3 parse times with probes.parse_time; test_time_forms_compare_correctly.
## Self-reported confidence
0.70 (uncalibrated; Tier 2 forced).

Review the PLAN (tasklist, candidate) against its SPEC (source) in a pre-execution review (UC-1). This plan was regenerated after a first review failed it with six blocking findings (B-1 to B-6, listed in the spec section "Reflect Verdict State" and summarised in the T1 card excerpt). Do two things: (a) for each of B-1 to B-6 decide resolved, open or regressed by comparing the defect with the plan text; (b) review the plan fresh for any NEW defect. You are read-only: edit and write nothing, run no shell or git, use only Read, Grep, Glob. Cite every claim as `path:line`: the line numbers are those of the real files (Read the real file and count there; the copies embedded below have extra header lines, so never cite lines from them). A claim you cannot cite is tagged [INFERRED]. Grade by what changes if the flawed text is corrected: `Blocking (Decision|Missing|Safety)` only if correcting it changes a named decision, outcome or acceptance check the plan rests on, or a required item is absent in substance, or following the text would lose data, expose a secret or act outside scope (name the affected action and evidence); `Medium:` for a real weakness nothing named rests on; `Note:` for wording or form. You may Read repo source and tests to check whether a plan claim is true. Return your card as your final reply with sections: `## Verdict` (PASS or FAIL; FAIL only on a Blocking finding), `## Prior blockers` (B-1 to B-6, one line each with resolved/open/regressed and a citation), `## Findings` (table: id | grade | claim | citations | consequence), `## Coverage check` (your verdict on each coverage row below), `## Self-reported confidence` (0 to 1) and the model you are running as.

Real files: plan = /home/coder/workspaces/worktrees/IronClaude/run-ledger/.dev/tasks/to-do/TASK-WF-remediationSourc-20261126-181052/TASK-WF-remediationSourc-20261126-181052.md ; spec = /home/coder/workspaces/worktrees/IronClaude/run-ledger/.dev/tasks/to-do/TASK-WF-remediationSourc-20261126-181052/source.md ; first review's merged findings (for reference) = /home/coder/workspaces/worktrees/IronClaude/run-ledger/.dev/reflect/pre-TASK-WF-mergedRequiremen-20261126173757/adversarial/merged-output.md

Persona lens: qa.

## Grounding hunks

codegraph run state: index_state=fresh checked_at=2026-11-26T17:33Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/run-ledger projectPath=/home/coder/workspaces/worktrees/IronClaude/run-ledger

Audit the coverage matrix AGAINST the spec body in your grounding hunks; surface any requirement-bearing span absent from the matrix (parsed or inferred) as a finding.

### .dev/tasks/to-do/TASK-WF-remediationSourc-20261126-181052/source.md (full file)
```markdown
<!-- Merged spec. Base: variant-2-sonnet-refactorer.md (Variant 2). Donor: variant-1-sonnet-architect.md (Variant 1). Plan: refactor-plan.md (14 changes). Merge date: 2026-11-26. -->
# Run ledger: requirements spec (IronbellyOrg/IronClaude#895)

Goal: `superclaude sweep run` must find Orca Run ids without a person naming them. A deterministic script (no model) rebuilds a Run ledger file from scratch every 30 minutes; a hook adds a new Run at once; sweep reads the ledger. Result file for this work: `.dev/issues/895/result.md`.

## Decisions summary
<!-- Source: Base (original, modified) - table added to satisfy the required section list; rows reflect Changes #1-#14 -->
| Q | Question | Decision |
|---|---|---|
| 1 | Code location and run | One new file `src/superclaude/cli/sweep/ledger.py`, command `superclaude sweep ledger`, attached to the existing `sweep_group` (no `main.py` change); pure `decide()`; own Orca runner, not `sweep/probes.py`. |
| 2 | How sweep consumes it | `sweep run` reads the ledger (file read, no Orca call) when no `--run` and no terminal-bound Run; explicit `--run` wins; no new flag; stale header at 90 minutes. |
| 3 | Ledger location | Fixed per-user file `${XDG_STATE_HOME:-~/.local/state}/superclaude/run-ledger.json`, override `--ledger` or env `SUPERCLAUDE_RUN_LEDGER`. Never under the repo. |
| 4 | Concurrency | Two writers (rebuild, hook `--add`): `fcntl.flock` sidecar lock, 10 s timeout then exit 3; atomic temp file + `fsync` + `os.replace`; rebuild merges hook entries newer than its own start. |
| 5 | Exact definitions | Three rules (live worktree, unfinished Task, new) over `run-list` non-legacy Runs; denylist of terminal statuses; whole-string worktree id match; paged `worker-list`; four implausible-result guards. |
| 6 | Scheduling | Recommend the system crontab every 30 minutes (`17,47`), as a repo doc for Coder#545 to adopt; nothing installed. Session cron is the fallback. |
| 7 | Hook | Delivered: PostToolUse `Bash` script via `superclaude install`; kept only if one scratch `run-create` shows the Run id in its output, else dropped with that reason and the fallback documented. Registration is Coder#545's. |

## Code layout and command surface
<!-- Source: Base (original, modified) - command renamed to `sweep ledger` and --add added per Change #3; the base's `run-ledger` command name and main.py line are replaced -->
- Builder and `decide()`: `src/superclaude/cli/sweep/ledger.py`. Tests: `tests/run_ledger/`. Hook: `run-ledger-record.sh` in the same `src/superclaude/hooks/` source folder as `require-orca-worktree-agent.sh` (exact subfolder to confirm in the code).
- Commands (subcommands of the existing `sweep` group; `main.py` untouched):
  - `superclaude sweep ledger [--ledger PATH] [--dry-run] [--json] [--accept-empty]`: rebuild. `--dry-run` prints the would-be ledger and writes nothing; `--json` prints the summary as JSON.
  - `superclaude sweep ledger --add <run_id>`: append one id (idempotent; validated with the sweep id pattern `probes.RUN_ID_RE`; merges under the lock; no Orca call).
  - No `show`, `path`, `--timeout`, `--no-ledger`, or sweep `--ledger` flag.
- A standalone script would not be on PATH after `superclaude install`; a subcommand is.
- The builder calls Orca through its own small runner (`subprocess.run([...], capture_output=True, timeout=30)`, fixed argv, no shell), never through `sweep/probes.py`, so the pinned `ALLOWED_ORCA` and `tests/sweep/test_probes_allowlist.py` stay unchanged and green. Calls used: `orca orchestration run-list --json`; `orca worktree list --json`; `orca orchestration task-list --run <id> --json`; `orca orchestration worker-list --run <id> --json --limit 100 [--cursor <c>]`.
- Orca binary: use `find_orca` in `src/superclaude/cli/issue_watch/` if its signature fits, else `shutil.which("orca")`.
- Exit codes: see "Failure and implausible-result rules".

## Ledger file and schema
<!-- Source: Base (original, modified) - schema extended with source/added_at, counts and stale-candidate fields per Changes #4, #10 -->
Orca Runs are global to the Orca server, not to a worktree; `.dev/coordinator/` in one worktree is invisible to a schedule or sweep started elsewhere and disappears with that worktree. Nothing to stage, nothing to gitignore. Version 1:
```json
{"version":1,"generated_at":"2026-11-26T18:00:00Z","orca":{"runs_listed":63,"worktrees_listed":12},
 "counts":{"live_worktree":3,"unfinished_task":9,"new":0,"hook_added":0,"main_checkout_only":0,
           "open_task_stale_7d_only":0,"blocked_only":0},
 "runs":[{"id":"run_915328e33d9a","created_at":"...","objective":"first 120 chars",
   "reasons":["live_worktree","unfinished_task","new","hook_added"],"source":"build","added_at":"...",
   "live_worktree_ids":["<repoId>::<path>"],"unfinished_task_count":0,
   "main_checkout_only":false,"stale_open_tasks_only":false}]}
```
- `generated_at` is captured BEFORE the first Orca call, so the `new` rule cannot miss a Run created mid-build. `reasons` is a non-empty subset of the four names; `source` is `build` or `hook`.
- `--add` keeps `generated_at` unchanged (so sweep staleness is not masked) and writes `source:"hook"`, `reasons:["hook_added"]`, `added_at`.

## Inclusion rules
<!-- Source: Base (original, modified) - 24 h fallback per Change #5 (Variant 1 Q5), universe rule per Change #11 (Variant 1), stale-candidate report per Change #10, measured facts added -->
Universe: Runs from `run-list` only, with `legacy == 0` and `id != "run_legacy_local"` (the only `legacy:1` Run on this host). Never infer that a Run exists from `worker-list`: for an unknown Run it returns `ok:true` with zero workers, while `task-list` returns `run_not_found`. A non-legacy Run is IN if any one reason holds:
- `live_worktree`: any worker row has `resource.worktreeId` exactly equal (whole string) to an `id` in `worktree list --json` `result.worktrees[].id`. Both are `<repoId>::<absolute path>` (verified); never split, normalise, or compare bare paths. A row with no `resource` or null `worktreeId` does not match.
- `unfinished_task`: any Task whose `status` is NOT in the terminal set `{completed, failed, cancelled}`. Observed on this host: completed 644, failed 60, blocked 18, ready 12. Denylist, not allowlist: an unseen status (`pending`, `dispatched`, `in_progress`; names UNVERIFIED) keeps the Run in rather than dropping live work. `failed` is terminal (counting it would keep old Runs forever). The terminal set is one constant.
- `new`: `created_at >= previous_ledger.generated_at`. With no previous ledger, or an unreadable one, `new` means `created_at` within the last `NEW_FALLBACK_HOURS = 24` (named constant).
- A hook-added entry newer than the rebuild start is kept (see Concurrency); an older one is re-evaluated by the three rules like any other Run.
- Rules stay as the issue defines them: a worktree Orca still lists, including the main checkout, counts. No age cutoff and no main-checkout exclusion is built (over-inclusion is the safe direction); a cutoff is the owner's decision (see Open decisions).

Measured on 2026-11-26 on this host: 63 Runs listed, 62 non-legacy; 10 admitted (3 by live worktree, 9 by Task, 2 by both), not the 3 the issue assumed. Rebuild without the short-circuit took 26.1 s (about 0.18 s per Orca call; 62 `task-list` calls plus `worker-list` pages, about 8 at limit 100); sweeping every Run took 48.6 s and a 3,666-line report.

Pagination: loop `worker-list` while `result.page.hasMore` is true, passing `--cursor result.page.nextCursor` with `--limit 100`. A repeated cursor, or more than 50 pages for one Run, is a failure (exit 1). `task-list` returned all Tasks in one response (`result.tasks[]`, `count`); behaviour above 100 Tasks is UNVERIFIED.
Short-circuit: fetch Tasks first; fetch workers only for Runs not already IN by Task or `new`.

Report (stdout summary and the ledger `counts` and per-run fields): per-reason counts; Runs admitted only through the main checkout (`isMainWorktree`); Runs admitted only by `ready` or `blocked` Tasks whose `updated_at` is older than 7 days; the count of Runs held in only by `blocked` Tasks. These show the owner the cost; they change no rule.

## Failure and implausible-result rules
<!-- Source: Base (original, modified) - guard 4 clause per Change #6, exit codes per Change #7, orca-not-found text per Change #9 -->
On any of these the old ledger is left untouched, one reason goes to stderr (first word `orca-failure:` or `implausible:`), and the exit is non-zero. The whole new ledger is built in memory first; an exception before the write leaves the disk untouched.
1. Any Orca call exits non-zero, times out (30 s each), or returns JSON without `"ok": true` (`orca-failure:`). If the binary is missing or Orca is not running the text names "orca not found or Orca app not running".
2. `worktree list` returns 0 worktrees (the main checkout always exists, so 0 is a broken read) (`implausible:`).
3. `run-list` returns 0 Runs while a previous ledger exists (`implausible:`).
4. The new ledger has 0 Runs, the previous ledger had at least 1, at least 1 non-legacy Run exists, AND at least 1 non-legacy Run was created or updated within 24 h (`implausible:`). `--accept-empty` overrides this guard only, never an Orca failure.

Exit codes: 0 written; 1 Orca failure or implausible result; 2 usage (including `--add` with a malformed id); 3 lock timeout. No 20% shrink guard. Ceiling: a partial read that returns a plausible non-empty list is not caught; add a shrink guard if one is ever seen.

## Concurrency and write method
<!-- Source: Variant 1 (sonnet:architect), Section Q3/Q4 - merged per Change #4 (simplified: no separate hook-entry expiry) -->
Two writers exist (the schedule's rebuild and the hook's `--add`), so a lock is required (the base's no-lock design is replaced).
- Sidecar lock file `run-ledger.lock` beside the ledger, `fcntl.flock(LOCK_EX)`, blocking up to 10 s, then exit 3 with the ledger untouched (Linux/macOS; Windows UNVERIFIED and out of scope).
- A rebuild does all Orca reads first (about 26 s) without the lock, then takes the lock, re-reads the ledger, and writes the rebuilt set plus every entry with `source == "hook"` and `added_at >= generated_at`. A hook entry older than that is re-evaluated by the three rules. This closes the lost-append race.
- Every write: temp file `run-ledger.json.tmp.<pid>` in the same directory, `fsync`, `os.replace`; readers see the old or the new file, never half. No `.tmp` residue after a failure.
- `--add` on a missing or unreadable ledger writes nothing and exits 1 with `implausible:` (the first build picks the Run up through the 24 h `new` fallback).

## Sweep consumption
<!-- Source: Base (original, modified) - stale threshold 90 minutes, `sweep ledger` hint, docs and skill text per Changes #13, #14 (#895) -->
- `src/superclaude/cli/sweep/commands.py`: when no `--run` is given and no Run is bound to the terminal, read the ledger (`json.load`, zero Orca calls), validate each id with `probes.RUN_ID_RE`, and sweep them. Explicit `--run` always wins and the ledger is then not read (the existing flag; a person naming a Run is not the guessing problem; #895 says "from the ledger only" for the coordinator's case). No new flag; env var `SUPERCLAUDE_RUN_LEDGER` serves tests.
- Report header: "Run ids from the Run ledger built <time>". When `generated_at` is older than 90 minutes (the #895 threshold, three missed 30-minute builds) the header adds "ledger is N min old"; sweep still runs (a stale list beats none).
- Missing or corrupt ledger: exit 2 with the old "no Run bound" message plus `run "superclaude sweep ledger" first`. A malformed id in the ledger is rejected by `RUN_ID_RE`.
- Sweep's `ALLOWED_ORCA` is unchanged. The sweep skill still runs only `superclaude sweep run`, so its `Bash(superclaude sweep run:*)` permission is unchanged.
- Docs and skill text: edit `src/superclaude/commands/sc/sweep.md` (the `--run` row and the "no Run is bound" sentence) and `src/superclaude/skills/sc-sweep-protocol/SKILL.md` to say ids come from the ledger when none is given; use installed paths only inside those texts (never `src/superclaude/`); then `make sync-dev`.

## Hook
<!-- Source: Variant 1 (sonnet:architect), Section Q7 - merged per Change #1 (replaces base "drop it") and Change #2 (test and drop rule) -->
### Design
- PostToolUse, matcher `Bash`; script `run-ledger-record.sh`, delivered to `~/.claude/hooks/` by `superclaude install` (as `require-orca-worktree-agent.sh` is).
- Reads stdin JSON with `jq`; acts only when `tool_input.command` runs `orca orchestration run-create` or `worker-start`. Takes the first `run_[0-9a-f]{12}` found in the Bash result text (for `worker-start`, also in the command's `--run` value) and calls `superclaude sweep ledger --add <id>`.
- Always exits 0 (fail open, never blocks). If no id is found it appends one line to `${XDG_STATE_HOME:-~/.local/state}/superclaude/run-ledger-hook.log`; the next rebuild catches the Run through `new`.
- Registration is not ours: Coder#545 registers it (see next section for the entry). We never edit `~/.claude/settings.json`.

### Payload test and drop rule
- Before building the hook: run exactly one `orca orchestration run-create --objective "scratch Run for the run-ledger hook payload test, safe to ignore" --json`, keep its stdout as a test fixture, and check the Claude Code PostToolUse Bash payload shape (`tool_response`) in the official docs.
- Decision, written in the result: Run id present in the output means the hook is delivered; absent means the hook is dropped with that reason and the fallback is documented (the coordinator runs `superclaude sweep ledger` right after `run-create`, about 26 s, no hook). This creates exactly one Run that Orca cannot delete; flag it in the result. The run needs the owner's go (see Open decisions).
- Fixture: a recorded payload under `tests/run_ledger/fixtures/`; the hook tests below feed it. What `run-create` prints is UNVERIFIED until this run.

## Schedule and install notes doc
<!-- Source: Variant 1 (sonnet:architect), Sections Q6/Q7 - merged per Change #8 (base Q6 modified: doc for Coder#545, flock -n, PATH) -->
Ship `docs/user-guide/run-ledger.md` for Coder#545 to adopt. Nothing is installed or registered by this work. It holds:
- Schedule recommendation: system crontab, every 30 minutes at offset minutes (`17,47`), wrapped in `flock -n` on a lock file, command `superclaude sweep ledger`, with an explicit `PATH` including the directory of the Orca CLI shim; output appended to a log under `${XDG_STATE_HOME:-~/.local/state}/superclaude/`. Why: survives session and Orca restarts, needs no model, exits non-zero with a logged reason. A session-only cron dies with the session (the problem); an Orca automation adds a dependency (whether it runs non-model commands is UNVERIFIED).
- Hook registration entry for Coder: `{"matcher":"Bash","hooks":[{"type":"command","command":"~/.claude/hooks/run-ledger-record.sh"}]}` under `hooks.PostToolUse`.
- Install notes, stated plainly: in Coder the crontab is rewritten on every boot, so a hand-edited crontab is lost; the schedule and the hook registration are registered by Coder#545, not by us.
- The pre-install check (next section) and the session-cron fallback (the same line from a session cron if Orca needs a desktop session socket, UNVERIFIED).

## Pre-install check
<!-- Source: Variant 1 (sonnet:architect), Section Q6 - merged per Change #9 (A-001 QUALIFY) -->
Before the cron line is registered, `env -i HOME=$HOME PATH=<the cron PATH> superclaude sweep ledger --dry-run` must exit 0. It proves the stripped cron environment finds `superclaude` and reaches Orca (the stripped-environment call worked in the debate evidence). If it fails, the message names "orca not found or Orca app not running" (exit 1, old ledger kept). Also check `command -v superclaude` on the target host (the pipx path is UNVERIFIED there). Include this check in the doc and in the result.

## Tests
<!-- Source: Base (original, modified) - ten base tests kept, 12 added from Variant 1 per Change #12; test_new_run_in adjusted for Change #5 -->
Fake `orca` via a `monkeypatch` of the runner; no real Orca. Files under `tests/run_ledger/`. `tests/sweep/test_probes_allowlist.py` must stay unchanged and passing.
- `test_live_worktree_run_in`: worker `worktreeId` equal to a listed id gives `live_worktree`.
- `test_deleted_worktrees_only_run_out`: all worker ids absent from the list, all Tasks completed, old `created_at` gives OUT.
- `test_unfinished_task_run_in`: `ready`, `blocked`, `in_progress`, `some_unknown_status` give IN; `completed`, `failed`, `cancelled` give OUT.
- `test_new_run_in`: `created_at` after previous `generated_at`, no workers or Tasks, gives IN with `new`.
- `test_new_fallback_24h_when_no_previous_ledger`: with no or unreadable previous ledger, a Run under 24 h old is IN and an older one is OUT.
- `test_legacy_run_out`: `run_legacy_local` and any `legacy:1` Run are OUT even with a live worktree.
- `test_worktree_id_exact_match_only`: same path, different repoId, no match. `test_null_worktree_id_no_match`.
- `test_orca_failure_keeps_old_ledger`: non-zero exit, timeout, `ok:false` leave the file bytes unchanged, exit 1.
- `test_implausibly_empty_keeps_old_ledger`: guards 2 to 4; `--accept-empty` overrides guard 4 only; guard 4 needs a Run created or updated within 24 h.
- `test_worker_list_pagination`: three pages via `hasMore` and `nextCursor`; a repeated cursor fails.
- `test_atomic_write`: a failure inside `os.replace` leaves the old file and no `.tmp` residue.
- `test_add_idempotent_and_rejects_bad_id`; `test_lock_timeout_exit3`; `test_concurrent_add_and_build_no_lost_append` (multiprocessing, 20 adds during a slow build).
- `test_sweep_reads_ledger_when_no_run`: ledger ids used; explicit `--run` ignores the ledger; missing ledger gives exit 2 and the hint; malformed id rejected by `RUN_ID_RE`.
- `test_corrupt_ledger_on_sweep_gives_exit2_hint`; `test_stale_ledger_header_in_sweep` (over 90 minutes adds "ledger is N min old").
- Hook: `test_hook_extracts_run_id_from_fixture`; `test_hook_ignores_other_commands`; `test_hook_no_id_logs_and_exits_0`; `test_hook_fails_open_when_superclaude_missing` (bash with a stubbed PATH).

## Real-run acceptance and what to report
<!-- Source: Base (original, modified) - delivery steps and timings updated with measured facts and hook step per Changes #2, #10 -->
Steps: (1) edit under `src/superclaude/` only, then `make sync-dev`; never stage `.claude/`; stage `.dev/tasks` if a task package is created. (2) `uv run pytest tests/run_ledger tests/sweep -v`. (3) `uv run superclaude sweep ledger --dry-run`, then a real write to a temp `--ledger`, then `SUPERCLAUDE_RUN_LEDGER=<temp> uv run superclaude sweep run`. (4) The hook payload capture (after the owner's go). (5) Nothing installed; no commit until the owner says so.
Report in `.dev/issues/895/result.md`: ledger written (path, counts); rebuild wall time against the 26.1 s baseline; sweep time over the ledger against 48.6 s and 3,666 lines for all Runs, and that it ran without "no Run bound"; per-reason counts and the stale-candidate figures; the hook decision with the fixture evidence; that exactly one scratch Run was created (if it was); test results; the pre-install check result.

## Risks and ceilings
<!-- Source: Base (original, modified) - hook risks and lock added per Changes #1, #4, #6, #10 -->
- Hook plus lock add a second writer (highest risk). Rollback: delete the hook script and the `--add` branch; the rebuild alone still meets every other criterion.
- Unknown Task status names: the denylist keeps the Run in; a wrongly open Run only costs sweep time.
- Stale leftovers: a Run whose only open Task is a stale `blocked` or `ready` one stays in until that Task is settled (the cost is reported, no cutoff built).
- A Run with live work but a worktree Orca no longer lists, and no open Task, drops out: accepted by the issue's rule.
- A Run created and finished between two builds never enters: harmless.
- Partial read with a plausible non-empty list is not caught (no shrink guard).
- Clock: single host; an NTP step back could re-admit a few Runs as `new` (harmless).
- Cron environment lacking `orca`: caught by the pre-install check; a dead schedule shows as the 90-minute stale header.
- Helper fit of `find_orca` is UNVERIFIED until implementation. The Orca JSON shape (`legacy` int, `page` keys) is verified only on this host.

## Open decisions for the owner
<!-- Source: Base (original, modified) - section added for required list; items from Changes #2, #10 -->
1. Age cutoff for stale Runs: none is built. Of the 10 admitted, some are held only by old `ready` or `blocked` Tasks or only by the main checkout. Choose to keep (default), or give a cutoff (for example Task `updated_at` older than N days).
2. Creating the one scratch Run for the hook payload test: it cannot be deleted. Answer yes (hook decided by the fixture) or no (the hook is built from the documented payload shape with the id-absent fallback, UNVERIFIED).

## Out of scope
<!-- Source: Base (original, modified) - constraints from the seed brief restated; non-changes from the plan -->
- Constraints kept: UV only (`uv run ...`, never `python -m` or bare `pip`); edit under `src/superclaude/`, then `make sync-dev`; never stage `.claude/`; no hardcoded `src/superclaude/` paths in installed primitives (installed paths only: `~/.claude/hooks/...`, `~/.claude/skills/...`, `~/.claude/commands/sc/...`); no `orca orchestration reset`, no Run delete; no Orca link flags (`--issue`, `--pr`); no `~/.claude/settings.json` edit; no crontab edit; nothing scheduled; no commit.
- Not built: a package of modules, `show`, `path`, `--timeout`, `--no-ledger`, a sweep `--ledger` flag, a `~/.superclaude/` ledger path, a 20% shrink guard, more exit codes, excluding the main checkout, any age cutoff.
- Not touched: `sweep/probes.py` and `ALLOWED_ORCA`; Windows locking.

## Reflect Verdict State (regeneration input; appended after the first review of the plan built from the text above)
The first plan built from this spec was reviewed and failed with 6 blocking findings. The new plan must contain none of the defects below. Where this section and an earlier section disagree, this section wins.

### Blocking findings to fix
- B-1: A task check may not forbid importing `probes` while another task imports from it. The ledger module makes no Orca call through `probes` and imports only the names `RUN_ID_RE` and `parse_time` from it; a named test (an AST check of the import names) enforces this.
- B-2: A documentation check may not demand that every command and flag the doc names exists in `superclaude sweep ledger --help`, because the doc must also name `flock -n`, `env -i`, `command -v` and a crontab. The check covers `superclaude` commands and flags only.
- B-3: A step must stage the task package: after the last artifact is written, run `git add .dev/tasks` (staging is not committing). The package `./artifacts/` folder is the package's own, never the project-root `artifacts/`.
- B-4: The sweep change appends a hint to the "no Run bound" and "Orca unavailable" messages, and existing tests assert those messages exactly (tests/sweep/test_cli_contract.py, the cases that check the exact stderr text). The plan must name those test cases and update their expected text to include the hint; the spec, not the tests, decides the wording.
- B-5: Adding `run-ledger-record.sh` to `_FRESHNESS_SCRIPTS` in src/superclaude/cli/install_hooks.py breaks the existing install tests unless the hard-coded seed list of script names in tests/cli/test_install_hooks.py also names it. The hook task updates that seed list.
- B-6: Orca timestamps come in two forms, SQLite `YYYY-MM-DD HH:MM:SS` and ISO with `Z` or an offset (`probes.parse_time` reads both). Every rule that compares times (`new`, the 24 h fallback, `added_at >= generated_at`, Task age) compares parsed UTC datetimes through `probes.parse_time`, and a test feeds both forms.

### Findings that counted toward the route (the new plan must not repeat them)
- Labelled HIGH: B-4, B-5 and B-6 above.
- M-1: Where a task creates the scratch Run on the authority of the owner's brief, it quotes the brief's sentence verbatim ("first test what such a hook actually receives from run-create"), and the final report names that authority.
- M-2: `decide` takes no hook entries (none newer than `generated_at` can exist in the previous ledger). The locked merge replaces an existing row with the same Run id, names the winning row, unions the reasons and recomputes `counts` after the merge.
- M-3: When the scratch `run-create` cannot be made, the decision file ends `Decision: deliver`, marked UNVERIFIED, and records zero scratch Runs created, where the fixture came from, and an UNVERIFIED marker separate from the `Decision:` line.
- M-4: Task age comes from the Task's own timestamp. When the field is absent the stale flag is null (unavailable); it never falls back to the Run's `updated_at`.
- M-5: `main_checkout_only` means the Run is admitted only through a main-checkout worktree: its only reason is `live_worktree`, at least one worktree matched and every matched worktree is the main checkout.
- M-6: A valid ledger with an empty `runs` list is sweepable: sweep proceeds with an empty Scope and the header line, exit 0, with a named test.
- M-7: The real-run sweep runs from a terminal where the Run binding lookup fails, or the report header shows that the ledger path was taken, because the scratch Run binds the terminal that created it.
- M-8: Ledger ids are validated with `re.fullmatch` and deduplicated by reusing `_check_run_ids` or an equivalent in the ledger reader.
- M-9: The import rule of B-1 is an exact allowlist of names.

### Corrections to earlier sections
- The command file to edit is `src/superclaude/commands/sweep.md` (there is no `commands/sc/` folder in the source tree); the skill is `src/superclaude/skills/sc-sweep-protocol/SKILL.md`, whose pinned sentence "adds no flag, reads no environment variable and has no worker mode" must stay.
- Do not reuse `find_orca` from `src/superclaude/cli/issue_watch/launch.py`: it needs that package's runner and an extra `orca skills list --json` probe. Use `shutil.which("orca")`.
- The sweep-reading tests live in `tests/sweep/` because `tests/sweep/conftest.py` already fakes the Orca seams there and blocks process starts; the other new tests live in `tests/run_ledger/`.
- Source issue: IronbellyOrg/IronClaude#895; the schedule and the hook registration are Coder#545's. The result file is `.dev/issues/895/result.md`.
```

### .dev/tasks/to-do/TASK-WF-remediationSourc-20261126-181052/TASK-WF-remediationSourc-20261126-181052.md (full file)
```markdown
---
schema: workflow-plan/1.2
source: ./source.md
strategy: systematic
depth: standard
slug: TASK-WF-remediationSourc-20261126-181052
version: "1"
priority: Medium
created_date: "2026-11-26"
---

# Run ledger for /sc:sweep: rebuild script, sweep input, hook file, install notes

Source: ./source.md
Goal: `superclaude sweep run` finds its Orca Run ids from a Run ledger file that a deterministic `superclaude sweep ledger` command rebuilds, a hook file appends new Runs at once, and a doc gives Coder (Coder#545) the schedule and hook registration to adopt. Source issue: IronbellyOrg/IronClaude#895. This plan replaces a first plan that failed review; its blocking findings are listed in the last section of `./source.md` and are fixed below.

## Constraints

- UV only: run tests and scripts with `uv run pytest ...` and `uv run python ...`; never `python -m`, bare `python script.py` or `pip install`.
- Edit under `src/superclaude/` (plus `tests/`, `docs/`, and the one hook mirror under `plugins/superclaude/hooks/scripts/`), then run `make sync-dev`; never stage `.claude/` contents; no text in an installed command, skill or hook may tell an agent to read a `src/superclaude/...` path (use `~/.claude/...` installed paths).
- `src/superclaude/cli/sweep/ledger.py` makes no Orca call through `src/superclaude/cli/sweep/probes.py` (its pinned `ALLOWED_ORCA` list and `tests/sweep/test_probes_allowlist.py` stay unchanged and passing). It may import exactly two names from `probes`: `RUN_ID_RE` and `parse_time`; a test enforces this. `src/superclaude/cli/main.py` is not edited.
- Not allowed: `orca orchestration reset`, deleting a Run, Orca link flags (`--issue`, `--pr`), editing `~/.claude/settings.json`, installing a crontab, scheduling anything, adding the hook to `src/superclaude/hooks/hooks.json` (Coder#545 registers it), committing, pushing, opening a pull request, or writing to any GitHub issue or Project without the owner's go. Staging `.dev/tasks` with `git add` is required and is not committing.
- Pytest tests fake Orca and never start it. The real Orca calls of this plan are: read-only list calls made once to check data shapes (Task 1 reads one `task-list` reply, Task 8 reads `run-current`), the one scratch `run-create` of Task 8, and the commands of Task 11. None is part of pytest.
- Behaviour decisions are fixed by the source (`./source.md`): do not add a package of modules, `show`, `path`, `--timeout`, `--no-ledger`, a sweep `--ledger` flag, a `~/.superclaude/` path, a shrink guard, extra exit codes, a main-checkout exclusion or an age cutoff.

## Phase 1: Ledger builder

## Task 1: Add the pure inclusion rules to a new `src/superclaude/cli/sweep/ledger.py`

Create `src/superclaude/cli/sweep/ledger.py` with the constants `TERMINAL_STATUSES = frozenset({"completed", "failed", "cancelled"})`, `NEW_FALLBACK_HOURS = 24`, `STALE_TASK_DAYS = 7`, `LEGACY_RUN_ID = "run_legacy_local"`, `LEDGER_VERSION = 1`, and a pure module-level function `decide(runs, workers_by_run, tasks_by_run, live_worktrees, previous, generated_at)` that does no I/O and takes no hook entries (a hook entry newer than `generated_at` cannot exist in the previous ledger; the locked merge of Task 3 owns hook entries). It returns the ledger `runs` entries plus the `counts` block of the schema in `./source.md` (sections "Ledger file and schema" and "Inclusion rules"). Every comparison of times parses both sides to UTC datetimes with `parse_time` imported from `src/superclaude/cli/sweep/probes.py` (Orca emits both the SQLite form, a date and a time separated by a space, and the ISO form with `Z` or an offset; never compare the raw strings). Rules: only Runs from `run-list` with `legacy == 0` and `id != "run_legacy_local"`; `live_worktree` when a worker row's `resource.worktreeId` equals, as a whole string, an `id` of `worktree list --json` (a row with no `resource` or a null `worktreeId` never matches); `unfinished_task` when any Task status is not in `TERMINAL_STATUSES` (denylist: unknown statuses count as unfinished); `new` when `created_at >= previous.generated_at`, or, with no usable previous ledger, when `created_at` is within the last `NEW_FALLBACK_HOURS`. Per entry also set `live_worktree_ids`, `unfinished_task_count`, `main_checkout_only` (true only when the Run's only reason is `live_worktree`, at least one worktree matched and every matched worktree has `isMainWorktree` true), and `stale_open_tasks_only` (admitted only by `ready` or `blocked` Tasks that are older than `STALE_TASK_DAYS` by the Task's own timestamp; when `task-list` rows carry no such timestamp the flag is null for that Run and is never taken from the Run's `updated_at`; read one real `orca orchestration task-list --run <id> --json` reply once to see which field exists and record the field name in a code comment), plus the `blocked_only` count in `counts`. Put the comment `shortcut: no age cutoff and no main-checkout exclusion (over-inclusion is the safe direction), add one only if the owner decides` next to the rules. Create `tests/run_ledger/__init__.py` and `tests/run_ledger/test_rules.py`.

Acceptance criteria:
- `uv run pytest tests/run_ledger/test_rules.py -v` passes with these named tests: `test_live_worktree_run_in`, `test_deleted_worktrees_only_run_out`, `test_unfinished_task_run_in` (parametrised: `ready`, `blocked`, `in_progress` and an unknown status are IN; `completed`, `failed`, `cancelled` are OUT), `test_new_run_in`, `test_new_fallback_24h_when_no_previous_ledger` (a Run under 24 h old is IN, an older one OUT), `test_legacy_run_out` (both `run_legacy_local` and a `legacy:1` Run, even with a live worktree), `test_worktree_id_exact_match_only` (same path, different repoId gives no match), `test_null_worktree_id_no_match`, `test_time_forms_compare_correctly` (a SQLite-form `created_at` and an ISO `generated_at` compare in the right order), `test_main_checkout_only_requires_only_reason_and_a_match` (a Run with no matched worktree, and a Run with a main-checkout match plus an unfinished Task, are both false), `test_stale_flag_is_null_without_task_timestamp`.
- `decide` has no `subprocess`, file or `click` call in its body; the test file calls it with plain dicts and no monkeypatching.

## Task 2: Add the Orca reader and the implausible-result guards to `src/superclaude/cli/sweep/ledger.py`

Depends on: Task 1

Add to `src/superclaude/cli/sweep/ledger.py` a small Orca runner (`subprocess.run(argv, capture_output=True, timeout=30)` with a fixed argv list and no shell) resolved with `shutil.which("orca")` (an absolute path only; do not reuse `find_orca` from `src/superclaude/cli/issue_watch/launch.py`, because it needs that package's Runner object and an extra `orca skills list --json` probe), and a function `build_ledger(runner, previous, now)` that calls only `orca orchestration run-list --json`, `orca worktree list --json`, `orca orchestration task-list --run <id> --json` and `orca orchestration worker-list --run <id> --json --limit 100 [--cursor <c>]`, never through `probes`. Take `generated_at` before the first Orca call. Fetch Tasks first and fetch workers only for Runs not already IN by Task or `new`. Page `worker-list` while `result.page.hasMore` is true using `result.page.nextCursor`; a repeated cursor or more than 50 pages for one Run is a failure. The Run list comes from `run-list` only (an unknown Run returns ok with zero workers from `worker-list`, so existence is never inferred from it). Raise `OrcaFailure` (message starts `orca-failure:`) for a non-zero exit, a timeout, JSON without `"ok": true` or a missing binary (message names "orca not found or Orca app not running"), and `Implausible` (message starts `implausible:`) for: `worktree list` returning 0 worktrees; `run-list` returning 0 Runs while a previous ledger exists; a new ledger with 0 Runs while the previous had at least 1, at least 1 non-legacy Run exists and at least 1 non-legacy Run was created or updated within 24 h (this guard alone is bypassed by an `accept_empty` argument). Add the comment `shortcut: a partial read that returns a plausible non-empty list is not caught, add a shrink guard if one is ever seen`. Create `tests/run_ledger/test_build.py`, `tests/run_ledger/test_imports.py` and `tests/run_ledger/conftest.py` (an autouse fixture that fails any test starting a process unless the test carries the `integration` marker, same idea as `tests/sweep/conftest.py`).

Acceptance criteria:
- `uv run pytest tests/run_ledger/test_build.py tests/run_ledger/test_imports.py -v` passes with these named tests using a fake runner: `test_worker_list_pagination` (three pages), `test_repeated_cursor_fails`, `test_page_cap_fails`, `test_orca_failure_raises` (non-zero exit, timeout, `ok:false`), `test_missing_binary_message`, `test_empty_worktree_list_implausible`, `test_empty_run_list_with_previous_implausible`, `test_zero_included_implausible_needs_recent_run`, `test_accept_empty_overrides_only_the_zero_included_guard`, `test_generated_at_taken_before_first_call`, `test_workers_not_fetched_for_runs_already_in`, and `test_ledger_imports_only_allowed_probes_names` (an AST check that the only names imported from `superclaude.cli.sweep.probes` are `RUN_ID_RE` and `parse_time`).
- The module issues no Orca argv outside the four templates above.

## Task 3: Add the ledger file store to `src/superclaude/cli/sweep/ledger.py`

Depends on: Task 1

Add to `src/superclaude/cli/sweep/ledger.py`: `ledger_path(cli_value)` resolving, in order, the `--ledger` value, the environment variable `SUPERCLAUDE_RUN_LEDGER`, then `${XDG_STATE_HOME:-~/.local/state}/superclaude/run-ledger.json` (never under the repository); `read_ledger(path)` returning the parsed dict or `None` when the file is missing or not valid ledger JSON of `version` 1, with ids validated by `re.fullmatch(RUN_ID_RE, id)` and duplicate ids collapsed in first-seen order (the same rule as `_check_run_ids` in `src/superclaude/cli/sweep/commands.py`); a context manager `locked(path, timeout=10)` using `fcntl.flock(LOCK_EX)` on a sidecar `run-ledger.lock` in the same folder, raising `LockTimeout` after 10 s; `write_atomic(path, data)` writing `run-ledger.json.tmp.<pid>` in the same folder, `fsync`, then `os.replace`, and removing the temp file when anything fails; `merge_hook_entries(new_ledger, current_ledger, generated_at)` that keeps every current entry with `source == "hook"` and `added_at >= generated_at`, replaces an existing row with the same Run id (the build row wins its fields, the reasons are unioned and `hook_added` is added), and recomputes `counts` after the merge; and `add_run(path, run_id, now)` that validates the id, takes the lock, appends `{"id", "source": "hook", "reasons": ["hook_added"], "added_at"}` if absent (idempotent), keeps `generated_at` unchanged, and refuses (raises) when the ledger is missing or unreadable. Create `tests/run_ledger/test_store.py`.

Acceptance criteria:
- `uv run pytest tests/run_ledger/test_store.py -v` passes with: `test_path_precedence_flag_env_xdg`, `test_atomic_write_leaves_old_file_and_no_tmp_on_failure` (monkeypatch `os.replace` to raise), `test_lock_timeout`, `test_corrupt_ledger_reads_as_none`, `test_read_ledger_rejects_trailing_junk_in_id_and_dedupes`, `test_add_idempotent_and_rejects_bad_id`, `test_add_on_missing_ledger_refuses`, `test_add_keeps_generated_at`, `test_merge_replaces_same_id_unions_reasons_and_recomputes_counts`, `test_concurrent_add_and_build_no_lost_append` (multiprocessing: 20 adds while a slow rebuild runs, all 20 present afterwards, no duplicate ids).
- A comment says `shortcut: fcntl is Linux and macOS only, add msvcrt locking if Windows is ever needed`.

## Task 4: Add the `sweep ledger` command and register it on the existing `sweep` group

Depends on: Task 2, Task 3

In `src/superclaude/cli/sweep/ledger.py` add a `click` command named `ledger` (function `ledger_command`) with options `--ledger PATH`, `--dry-run`, `--json`, `--accept-empty`, `--add RUN_ID`. Without `--add`: build with `build_ledger`, then take the lock, re-read the ledger, call `merge_hook_entries`, and write atomically; `--dry-run` prints the would-be ledger and writes nothing; the stdout summary (or the `--json` object) gives per-reason counts, the number of Runs admitted only through the main checkout, only by stale `ready` or `blocked` Tasks, and held in only by `blocked` Tasks. With `--add`: call `add_run`, no Orca call. On any failure the old ledger file is untouched and one reason goes to stderr starting with `orca-failure:` or `implausible:`. Exit codes: 0 written, 1 `OrcaFailure` or `Implausible` (and `--add` on a missing or unreadable ledger, reason `implausible:`), 2 usage (including a malformed `--add` id), 3 `LockTimeout`. In `src/superclaude/cli/sweep/commands.py`, directly after the `sweep_group` definition (:215), import `ledger_command` from `.ledger` and call `sweep_group.add_command(ledger_command)`; if `ruff` flags the mid-module import (rule E402), add a line-level `# noqa: E402` with the reason. Create `tests/run_ledger/test_cli.py` using `click.testing.CliRunner` on `sweep_group` with a fake runner.

Acceptance criteria:
- `uv run pytest tests/run_ledger/test_cli.py -v` passes with: `test_orca_failure_keeps_old_ledger` (file bytes and mtime unchanged, exit 1, stderr starts `orca-failure:`), `test_implausibly_empty_keeps_old_ledger` (exit 1, stderr starts `implausible:`), `test_accept_empty_overrides_guard_not_orca_failure`, `test_dry_run_writes_nothing`, `test_summary_reports_stale_and_blocked_counts`, `test_add_exit_codes` (0 added, 2 malformed id, 1 missing ledger), `test_lock_timeout_exit_3`, `test_first_build_with_no_previous_ledger_uses_24h_fallback`.
- `uv run pytest tests/sweep/test_cli_registration.py tests/sweep/test_cli_contract.py tests/sweep/test_readonly.py tests/sweep/test_probes_allowlist.py -v` still passes (Task 6 changes the expected message text in `test_cli_contract.py`; until then this check runs before Task 6 and must pass unchanged): `superclaude sweep --help` lists both `run` and `ledger`, importing `superclaude.cli.sweep` still does not import `commands` until `sweep_group` is read, `src/superclaude/cli/main.py` has no diff, and `uv run ruff check src/superclaude/cli/sweep/ledger.py src/superclaude/cli/sweep/commands.py` is clean.

## Phase 2: Sweep reads the ledger

## Task 5: Add `run_source` to `SweepContext` and print it in the report header

Depends on: Task 4

In `src/superclaude/cli/sweep/models.py` add `run_source: str | None = None` as the last field of the frozen dataclass `SweepContext` (:75), and in `src/superclaude/cli/sweep/report.py` make `_header` (:182) append `sanitize(ctx.run_source)` as one more header line when it is not None. Callers that must keep working unchanged: the one `SweepContext(...)` construction in each of `src/superclaude/cli/sweep/commands.py`, `tests/sweep/test_classify.py`, `tests/sweep/test_probes_allowlist.py`, `tests/sweep/test_readonly.py` and `tests/sweep/test_report.py`. Add two tests to `tests/sweep/test_report.py`: `test_header_has_no_run_source_line_by_default` and `test_header_prints_run_source_line_when_set`.

Acceptance criteria:
- `uv run pytest tests/sweep -v` passes, including both new tests; no existing golden or snapshot in `tests/sweep/` changes.
- A report built with `run_source=None` is byte-identical to the report before this change.

## Task 6: Make `superclaude sweep run` fall back to the ledger when no Run is given or bound

Depends on: Task 5

In `run` of `src/superclaude/cli/sweep/commands.py` (:242), replace the `if not runs:` block (:264-266) so that it first tries `probes.bind_run(budget)` and, on `probes.BindingError`, reads the ledger with `ledger.read_ledger(ledger.ledger_path(None))`; when the ledger is usable, use its ids (already validated with `re.fullmatch` and deduplicated by `read_ledger`) as `runs`, including a ledger whose `runs` list is empty (sweep proceeds with an empty Scope and the header line, exit 0); when the ledger is missing or corrupt, exit 2 with the original BindingError message followed by ` run "superclaude sweep ledger" first`. An explicit `--run` still wins and the ledger is then not read. Build `run_source` as `Run ids from the Run ledger built <generated_at>`, and when `generated_at` is more than `LEDGER_STALE_MINUTES = 90` (new constant in `src/superclaude/cli/sweep/ledger.py`) old add ` . ledger is N min old`; pass it as the sixth argument of `SweepContext`. No new flag and no Orca call for reading the ledger. The hint changes two messages that existing tests assert exactly: update the expected stderr in the cases of `tests/sweep/test_cli_contract.py` that check `no Run bound: pass --run <id>` (about lines 478-490) and the Orca-unavailable text `Orca unavailable (binary not found: orca-ide); no Run binding could be established: pass --run <id>` (about lines 375-389), so both end with the hint; the spec decides the wording, the tests follow it. Add an autouse fixture to `tests/sweep/conftest.py` that points `SUPERCLAUDE_RUN_LEDGER` at a non-existent temporary file so no test reads a real ledger. Create `tests/sweep/test_ledger_input.py` reusing the Orca seams of `tests/sweep/test_cli_contract.py`.

Acceptance criteria:
- `uv run pytest tests/sweep -v` passes with these new named tests: `test_sweep_reads_ledger_when_no_run_and_no_binding`, `test_explicit_run_ignores_ledger`, `test_missing_ledger_exit_2_with_hint`, `test_corrupt_ledger_exit_2_with_hint`, `test_empty_runs_ledger_sweeps_with_empty_scope_exit_0`, `test_malformed_id_in_ledger_rejected`, `test_duplicate_ids_in_ledger_swept_once`, `test_stale_ledger_over_90_minutes_adds_age_to_header`, `test_fresh_ledger_header_has_no_age`.
- The updated cases in `tests/sweep/test_cli_contract.py` assert the new text with the hint, every other case there still passes unchanged, and `probes.ALLOWED_ORCA` has no diff.

## Task 7: Update the sweep command and skill text

Depends on: Task 6

Edit `src/superclaude/commands/sweep.md` (the `--run <id>` row of the Options table and the sentence "When no Run is bound and none is named, the command exits ...") so they say that, with no `--run` and no bound Run, the Run ids come from the Run ledger built by `superclaude sweep ledger`, and that a missing ledger exits with a hint. Edit `src/superclaude/skills/sc-sweep-protocol/SKILL.md` near line 19 the same way, keeping the pinned phrase "adds no flag, reads no environment variable and has no worker mode" (required by `tests/commands/test_sweep_command.py:497`) and keeping the skill limited to the one command `superclaude sweep run`. Use installed paths only; no `src/superclaude/` path inside either text. Then run `make sync-dev`.

Acceptance criteria:
- `uv run pytest tests/commands/test_sweep_command.py -v` passes.
- `make verify-sync` reports no difference, and `git status` shows no staged or modified `.claude/` file other than what `make sync-dev` writes (those are never staged).

## Phase 3: Hook file

## Task 8: Capture what `run-create` gives a PostToolUse hook and record the decision

Run exactly one `orca orchestration run-create --objective "scratch Run for the run-ledger hook payload test, safe to ignore" --json`. Authority: the owner's brief to this agent orders the test, in these words: "first test what such a hook actually receives from run-create"; copy that sentence into `./artifacts/hook-decision.md` as the authority. Orca cannot delete the Run, so say so there. Save its stdout as `tests/run_ledger/fixtures/run_create_stdout.json`. Read the official Claude Code hooks documentation (context7 or `claude-code-guide`) for the PostToolUse payload of the Bash tool and write `tests/run_ledger/fixtures/posttooluse_run_create.json` with that payload shape (`tool_name`, `tool_input.command`, `tool_response`) wrapping the captured output. Run `orca orchestration run-current` before and after and note whether this terminal is now bound to the scratch Run. If the `run-create` call cannot be made, create no Run, build the fixtures from the documented shape and record the number of scratch Runs created as zero, where each fixture came from, and a separate line `Status: UNVERIFIED`. Write `./artifacts/hook-decision.md` stating: the authority sentence, the captured output (or the reason it could not be captured), whether a `run_[0-9a-f]{12}` id is in it, the payload shape source, the number of scratch Runs created, and the decision, as the last line `Decision: deliver` or `Decision: drop`; the UNVERIFIED case ends `Decision: deliver` (the hook is built from the documented shape with the id-absent fallback), and `drop` is chosen only when a real capture shows no Run id in the output, with the reason and the documented fallback of running `superclaude sweep ledger` right after `run-create`.

Acceptance criteria:
- `./artifacts/hook-decision.md` exists, quotes the authority sentence, states the number of scratch Runs created (one, or zero with `Status: UNVERIFIED`) and ends with a line `Decision: deliver` or `Decision: drop`.
- `tests/run_ledger/fixtures/run_create_stdout.json` and `tests/run_ledger/fixtures/posttooluse_run_create.json` exist and parse as JSON; at most one Run was created and no Run was deleted.

## Task 9: Add the hook script, list it for install, mirror it, and test it

Depends on: Task 4, Task 8

If `./artifacts/hook-decision.md` ends `Decision: drop`, create no script, write nothing to the installer, and record in `./artifacts/hook-decision.md` that this task was skipped for that reason; Task 10 then documents the fallback instead. Otherwise create `src/superclaude/hooks/scripts/run-ledger-record.sh` (executable, `set -u`, fail open: always exit 0, never blocks): read stdin JSON with `jq`; act only when `.tool_input.command` runs `orca orchestration run-create` or `orca orchestration worker-start`; take the first `run_[0-9a-f]{12}` found in the Bash result text (`.tool_response`, string or object) and, for `worker-start`, also in the command's `--run` value; call `superclaude sweep ledger --add <id>` silently; when no id is found append one line to `${XDG_STATE_HOME:-$HOME/.local/state}/superclaude/run-ledger-hook.log`; a missing `jq` or `superclaude` also exits 0. Add a header comment in the style of `src/superclaude/hooks/scripts/require-orca-worktree-agent.sh` and the comment `shortcut: the command is matched with a simple pattern, not a full shell tokenizer, a quoted mention can add a harmless extra id`. Add `"run-ledger-record.sh"` with a one-line comment ("PostToolUse(Bash) Run-ledger appender; not registered in hooks.json, Coder#545 registers it") to `_FRESHNESS_SCRIPTS` in `src/superclaude/cli/install_hooks.py` (:42-97). The install tests seed a hard-coded list of script names (about lines 89-108 of `tests/cli/test_install_hooks.py`) and assert `ok` from `install_hooks(...)`, which fails for a listed script missing from that seed: add the new name to that seed list. Copy the script byte-for-byte, executable, to `plugins/superclaude/hooks/scripts/run-ledger-record.sh`. Do not touch `src/superclaude/hooks/hooks.json`. Add `tests/run_ledger/test_hook.py` (runs the script with `bash`, a stubbed `PATH`, and the fixtures of Task 8; mark the tests `integration` so the autouse process guard lets them through) and add `test_run_ledger_record_script_is_packaged_listed_and_mirrored` to `tests/cli/test_install_hooks.py` following the pattern at :854-860, plus an assertion that `hooks.json` contains no `run-ledger-record`.

Acceptance criteria:
- `uv run pytest tests/run_ledger/test_hook.py tests/cli/test_install_hooks.py -v` passes with `test_hook_extracts_run_id_from_fixture` (the stub `superclaude` receives `sweep ledger --add <id>`), `test_hook_ignores_other_commands`, `test_hook_no_id_logs_and_exits_0`, `test_hook_fails_open_when_superclaude_missing`, the new install test, and every existing install test (none fails for the seed list).
- `make verify-sync` still passes (every script under `src/superclaude/hooks/scripts/` is a member of `_FRESHNESS_SCRIPTS` and no member is stale) and `source` and `mirror` of the script are byte-equal.

## Phase 4: Install notes for Coder

## Task 10: Write `docs/user-guide/run-ledger.md` for Coder#545 to adopt

Depends on: Task 4, Task 9

Create `docs/user-guide/run-ledger.md` holding: what the ledger is and where it lives (`${XDG_STATE_HOME:-~/.local/state}/superclaude/run-ledger.json`); the schedule recommendation for Coder#545 (system crontab, every 30 minutes at offset minutes such as `17,47`, wrapped in `flock -n` on a lock file, command `superclaude sweep ledger`, with an explicit `PATH` that includes the directory of the Orca CLI shim, output appended to a log under `${XDG_STATE_HOME:-~/.local/state}/superclaude/`), with the reasons from `./source.md` (survives session and Orca restarts, no model, logged non-zero exit; a session-only cron dies with the session; whether an Orca automation can run a non-model command is UNVERIFIED); the hook registration entry `{"matcher":"Bash","hooks":[{"type":"command","command":"~/.claude/hooks/run-ledger-record.sh"}]}` under `hooks.PostToolUse` (or, when Task 9 was skipped, the paragraph that says the hook was dropped, why, and the fallback); the plain statement that in Coder the crontab is rewritten on every boot so a hand-edited crontab is lost and that the schedule and the hook registration are registered by Coder#545, not by this work; the pre-install check `env -i HOME=$HOME PATH=<the cron PATH> superclaude sweep ledger --dry-run` must exit 0 and the `command -v superclaude` check; the session-cron fallback; the stale warning (90 minutes) the sweep prints when the schedule dies; and that after an Orca database reset `run-list` returns no Runs while an old ledger exists, so every build exits `implausible:` until the old ledger file is removed by hand. The doc must not tell the reader to run `crontab -e`.

Acceptance criteria:
- `docs/user-guide/run-ledger.md` exists, names the command `superclaude sweep ledger`, the exact hook registration entry (or the drop paragraph), the pre-install check and the Coder#545 ownership statement, and contains no `crontab -e` instruction and no `src/superclaude/` path.
- Every `superclaude` command and flag the doc names exists in `uv run superclaude sweep ledger --help` or `uv run superclaude sweep run --help`; other tools the doc names (`flock`, `env`, `command`) are outside this check.

## Phase 5: Real-run report

## Task 11: Run the real acceptance, write `.dev/issues/895/result.md`, and stage the package

Depends on: Task 7, Task 9, Task 10

Run `uv run pytest tests/run_ledger tests/sweep tests/commands/test_sweep_command.py tests/cli/test_install_hooks.py -v` and save the output to `./artifacts/pytest.log` (a failing test is reported with its output, never hidden). Against the real Orca Runs run `uv run superclaude sweep ledger --dry-run`, then a real write with `uv run superclaude sweep ledger --ledger <temporary path>` timed with `time` (copy the written ledger to `./artifacts/ledger.json`); then `SUPERCLAUDE_RUN_LEDGER=<that path> uv run superclaude sweep run`, timed, from a terminal where the Run binding lookup fails (the scratch Run of Task 8 may have bound this terminal; check with `orca orchestration run-current` first and use another checkout's terminal if it is bound), recording the line count of the report it wrote, that the report header line says the Run ids came from the Run ledger (this proves the ledger path was taken), and that it ran without `no Run bound`. Run the pre-install check of Task 10 once with `env -i`. Write `.dev/issues/895/result.md` containing the lines `outcome:` (succeeded, partial or failed, with a one-sentence reason), `artifacts:` (every file this plan wrote, repo-relative), `pull_request: none`, and the report: the ledger path and per-reason counts and stale-candidate figures; the rebuild wall time against the 26.1 s baseline; the sweep wall time over the ledger against 48.6 s and 3,666 lines for all Runs; the hook decision with the fixture evidence and the number of scratch Runs created and the authority sentence; test results; the pre-install check result; and the owner decisions: the age cutoff for stale Runs, and that the schedule and hook registration are left to Coder#545. Finally, as the last action, run `git add .dev/tasks` (staging is not committing). Do not commit, push or open a pull request.

Acceptance criteria:
- `.dev/issues/895/result.md` exists with `outcome:`, `artifacts:` and `pull_request: none`, and states the measured rebuild time, the measured sweep time and report line count, the ledger counts, and every failing test with its output (or that none failed).
- `./artifacts/pytest.log` and `./artifacts/ledger.json` exist; `git status` shows the `.dev/tasks` package staged and nothing committed; no Run was deleted, `orca orchestration reset` was not run, and nothing was installed or scheduled.
```

## Coverage slice

All 69 inferred rows (Pass 1 found 0 labeled ids).

| Requirement | Spec citation | Match | Task(s) or best | Quote |
|---|---|---|---|---|
| INF-001 | source.md:10 | containment | 1 | One new file `src/superclaude/cli/sweep/ledger.py`, command `superclaude sweep ledger`, at |
| INF-002 | source.md:11 | containment | 6 | `sweep run` reads the ledger (file read, no Orca call) when no `--run` and no terminal-bou |
| INF-003 | source.md:12 | containment | 3 | Fixed per-user file `${XDG_STATE_HOME:-~/.local/state}/superclaude/run-ledger.json`, overr |
| INF-004 | source.md:13 | containment | 3 | `fcntl.flock` sidecar lock, 10 s timeout then exit 3; atomic temp file + `fsync` + `os.rep |
| INF-005 | source.md:22 | containment | 4 | `--dry-run` prints the would-be ledger and writes nothing; `--json` prints the summary as  |
| INF-006 | source.md:23 | none | 2 (0.538) | append one id (idempotent; validated with the sweep id pattern `probes.RUN_ID_RE`; merges  |
| INF-007 | source.md:24 | containment | 1 | No `show`, `path`, `--timeout`, `--no-ledger`, or sweep `--ledger` flag. |
| INF-008 | source.md:26 | none | 2 (0.5) | never through `sweep/probes.py`, so the pinned `ALLOWED_ORCA` and `tests/sweep/test_probes |
| INF-009 | source.md:27 | containment | 2 | use `find_orca` in `src/superclaude/cli/issue_watch/` if its signature fits, else `shutil. |
| INF-010 | source.md:42 | containment | 8 | `generated_at` is captured BEFORE the first Orca call, so the `new` rule cannot miss a Run |
| INF-011 | source.md:43 | containment | 3 | `--add` keeps `generated_at` unchanged (so sweep staleness is not masked) |
| INF-012 | source.md:47 | containment | 1 | Never infer that a Run exists from `worker-list` |
| INF-013 | source.md:48 | containment | 1 | any worker row has `resource.worktreeId` exactly equal (whole string) to an `id` in `workt |
| INF-014 | source.md:49 | containment | 1 | any Task whose `status` is NOT in the terminal set `{completed, failed, cancelled}`. |
| INF-015 | source.md:50 | containment | 1 | With no previous ledger, or an unreadable one, `new` means `created_at` within the last `N |
| INF-016 | source.md:51 | none | 1 (0.444) | A hook-added entry newer than the rebuild start is kept (see Concurrency); an older one is |
| INF-017 | source.md:52 | containment | 1 | No age cutoff and no main-checkout exclusion is built (over-inclusion is the safe directio |
| INF-018 | source.md:56 | containment | 2 | A repeated cursor, or more than 50 pages for one Run, is a failure (exit 1). |
| INF-019 | source.md:57 | containment | 2 | Short-circuit: fetch Tasks first; fetch workers only for Runs not already IN by Task or `n |
| INF-020 | source.md:59 | containment | 1 | Runs admitted only by `ready` or `blocked` Tasks whose `updated_at` is older than 7 days;  |
| INF-021 | source.md:63 | containment | 4 | the old ledger is left untouched, one reason goes to stderr (first word `orca-failure:` or |
| INF-022 | source.md:64 | containment | 2 | Any Orca call exits non-zero, times out (30 s each), or returns JSON without `"ok": true`  |
| INF-023 | source.md:65 | containment | 1 | `worktree list` returns 0 worktrees (the main checkout always exists, so 0 is a broken rea |
| INF-024 | source.md:66 | containment | 2 | `run-list` returns 0 Runs while a previous ledger exists (`implausible:`). |
| INF-025 | source.md:67 | containment | 2 | `--accept-empty` overrides this guard only, never an Orca failure. |
| INF-026 | source.md:69 | containment | 4 | Exit codes: 0 written; 1 Orca failure or implausible result; 2 usage (including `--add` wi |
| INF-027 | source.md:74 | none | 4 (0.5) | blocking up to 10 s, then exit 3 with the ledger untouched |
| INF-028 | source.md:75 | containment | 3 | A rebuild does all Orca reads first (about 26 s) without the lock, then takes the lock, re |
| INF-029 | source.md:76 | containment | 3 | temp file `run-ledger.json.tmp.<pid>` in the same directory, `fsync`, `os.replace`; reader |
| INF-030 | source.md:77 | containment | 4 | `--add` on a missing or unreadable ledger writes nothing and exits 1 with `implausible:` |
| INF-031 | source.md:81 | containment | 6 | validate each id with `probes.RUN_ID_RE`, and sweep them. Explicit `--run` always wins and |
| INF-032 | source.md:82 | none | 6 (0.474) | When `generated_at` is older than 90 minutes (the #895 threshold, three missed 30-minute b |
| INF-033 | source.md:83 | containment | 6 | Missing or corrupt ledger: exit 2 with the old "no Run bound" message plus `run "superclau |
| INF-034 | source.md:84 | containment | 6 | Sweep's `ALLOWED_ORCA` is unchanged. |
| INF-035 | source.md:85 | containment | 7 | edit `src/superclaude/commands/sc/sweep.md` (the `--run` row and the "no Run is bound" sen |
| INF-036 | source.md:90 | containment | 10 | PostToolUse, matcher `Bash`; script `run-ledger-record.sh`, delivered to `~/.claude/hooks/ |
| INF-037 | source.md:91 | containment | 9 | acts only when `tool_input.command` runs `orca orchestration run-create` or `worker-start` |
| INF-038 | source.md:92 | containment | 9 | Always exits 0 (fail open, never blocks). |
| INF-039 | source.md:93 | containment | 7 | We never edit `~/.claude/settings.json`. |
| INF-040 | source.md:96 | containment | 8 | run exactly one `orca orchestration run-create --objective "scratch Run for the run-ledger |
| INF-041 | source.md:97 | containment | 8 | Run id present in the output means the hook is delivered; absent means the hook is dropped |
| INF-042 | source.md:98 | containment | 8 | a recorded payload under `tests/run_ledger/fixtures/` |
| INF-043 | source.md:102 | containment | 10 | Ship `docs/user-guide/run-ledger.md` for Coder#545 to adopt. Nothing is installed or regis |
| INF-044 | source.md:103 | containment | 10 | every 30 minutes at offset minutes (`17,47`), wrapped in `flock -n` on a lock file |
| INF-045 | source.md:104 | containment | 10 | Hook registration entry for Coder: |
| INF-046 | source.md:105 | containment | 10 | in Coder the crontab is rewritten on every boot, so a hand-edited crontab is lost |
| INF-047 | source.md:110 | containment | 10 | `env -i HOME=$HOME PATH=<the cron PATH> superclaude sweep ledger --dry-run` must exit 0. |
| INF-048 | source.md:119 | containment | 1 | `test_new_fallback_24h_when_no_previous_ledger`: with no or unreadable previous ledger, a  |
| INF-049 | source.md:126 | containment | 3 | `test_add_idempotent_and_rejects_bad_id`; `test_lock_timeout_exit3`; `test_concurrent_add_ |
| INF-050 | source.md:129 | containment | 9 | `test_hook_extracts_run_id_from_fixture`; `test_hook_ignores_other_commands`; `test_hook_n |
| INF-051 | source.md:133 | containment | 7 | edit under `src/superclaude/` only, then `make sync-dev`; never stage `.claude/` |
| INF-052 | source.md:134 | containment | 11 | Report in `.dev/issues/895/result.md`: ledger written (path, counts); rebuild wall time ag |
| INF-053 | source.md:155 | none | 11 (0.471) | no `orca orchestration reset`, no Run delete; no Orca link flags (`--issue`, `--pr`); no ` |
| INF-054 | source.md:156 | none | 2 (0.556) | Not built: a package of modules, `show`, `path`, `--timeout`, `--no-ledger`, a sweep `--le |
| INF-055 | source.md:157 | none | 3 (0.571) | Not touched: `sweep/probes.py` and `ALLOWED_ORCA`; Windows locking. |
| INF-056 | source.md:163 | containment | 2 | The ledger module makes no Orca call through `probes` and imports only the names `RUN_ID_R |
| INF-057 | source.md:164 | containment | 4 | The check covers `superclaude` commands and flags only. |
| INF-058 | source.md:165 | containment | 11 | run `git add .dev/tasks` (staging is not committing) |
| INF-059 | source.md:166 | containment | 6 | update their expected text to include the hint |
| INF-060 | source.md:167 | containment | 9 | The hook task updates that seed list. |
| INF-061 | source.md:168 | none | 1 (0.5) | compares parsed UTC datetimes through `probes.parse_time`, and a test feeds both forms. |
| INF-062 | source.md:172 | containment | 8 | it quotes the brief's sentence verbatim |
| INF-063 | source.md:173 | containment | 1 | `decide` takes no hook entries |
| INF-064 | source.md:174 | containment | 8 | the decision file ends `Decision: deliver`, marked UNVERIFIED |
| INF-065 | source.md:175 | containment | 1 | it never falls back to the Run's `updated_at` |
| INF-066 | source.md:176 | containment | 1 | its only reason is `live_worktree` |
| INF-067 | source.md:177 | containment | 6 | sweep proceeds with an empty Scope and the header line, exit 0 |
| INF-068 | source.md:178 | containment | 11 | or the report header shows that the ledger path was taken |
| INF-069 | source.md:179 | containment | 3 | Ledger ids are validated with `re.fullmatch` |
