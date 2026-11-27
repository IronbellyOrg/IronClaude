# Reviewer brief 1 (analyzer)

## T1 card excerpt

## Coverage (Step 1B)
- Pass 1 (ID_REGEX): 0 parsed ids in spec and tasklist.
- Pass 2: 55 inferred rows, every one quote-pinned (all 55 quotes re-found in the cited spec lines, 0 dropped).
- Deterministic containment match: 45 of 55 matched (coverage_pct_union 0.8182; coverage_pct null because parsed_total is 0).
- 10 rows came back unmatched by the string rule: INF-006, INF-008, INF-010, INF-016, INF-027, INF-028, INF-032, INF-041, INF-053, INF-054. On a manual read each one is covered by a named task or by the plan's `## Constraints` section (matcher false negatives from word choice); the reviewers must re-check this.
- `coverage_degraded: parsed-sparse` (inferred 55 > parsed 0): table-wide pre-filter, forces Tier 2. S_dev_density 0.1818 (deterministic) and S_domains >= 3 (code, tests, docs and hook script) also point to Tier 2.

## Candidate findings (to be confirmed or refuted by the reviewers)
- F1 Medium: `decide()` in Task 1 takes `hook_entries` and keeps hook-added entries, and Task 3 `merge_hook_entries` also keeps hook entries under the lock. A hook entry newer than `generated_at` cannot exist in the previous ledger when `decide` runs, so Task 1's carry-over rule is redundant with Task 3, and two code paths that both add hook entries risk duplicate ledger rows unless the merge dedupes by Run id. Evidence: plan Task 1 (the sentence on `hook_entries`), plan Task 3 (`merge_hook_entries`), spec lines 51 and 75.
- F2 Note: spec line 85 names `src/superclaude/commands/sc/sweep.md`; the real file is `src/superclaude/commands/sweep.md`. The plan's Task 7 uses the real path, so the plan is right and the spec snapshot is wrong.
- F3 Medium: spec line 97 says the scratch `run-create` "needs the owner's go" and line 151 lists it as an open decision; plan Task 8 runs it on the authority of the brief. The plan says so in one clause; the executor must not read the spec line as a blocker or as a license without that clause.
- F4 Note: the spec lists the sweep-consumption tests under `tests/run_ledger/` (lines 114 and 127); plan Task 6 puts them in `tests/sweep/` because `tests/sweep/conftest.py` already fakes the Orca seams there. The plan does not call this a deviation.
- F5 Note: the spec says use `find_orca` "if its signature fits" (line 27); plan Task 2 decides it does not fit and uses `shutil.which("orca")`, with the reason. Consistent with the spec's condition.

## Self-reported confidence
0.70 (card not calibrated in this run: Tier 2 is forced by the parse-density pre-filter whatever the score, so the Tier 1 calibration could not change the route; the reviewer cards are calibrated blind).

Audit the TASKLIST (plan) against the SPEC for a pre-execution review (UC-1). You are read-only: edit and write nothing, run no shell or git, use only Read, Grep, Glob on the paths given. Cite every claim as `path:line` (re-Read the lines first); a claim you cannot cite must be tagged [INFERRED]. Grade each finding by what changes if the flawed text is corrected: `Blocking (Decision|Missing|Safety)` only when correcting it would change a named decision, outcome or acceptance check the plan rests on, or a required item is absent in substance, or following the text would lose data, expose a secret or act outside the declared scope (name the affected action and the evidence); `Medium:` for a real weakness nothing named rests on; `Note:` for wording, form or a wrong label on a true statement. Report a zero-finding result only with what you checked. Return your card as your final reply with sections: `## Verdict` (PASS or FAIL, one line, FAIL only on a Blocking finding), `## Findings` (table: id | grade | claim | citations | consequence), `## Coverage check` (your verdict on each coverage row below), `## Self-reported confidence` (0 to 1, one line).

Persona lens: analyzer.

## Grounding hunks

codegraph run state: index_state=fresh checked_at=2026-11-26T17:33Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/run-ledger projectPath=/home/coder/workspaces/worktrees/IronClaude/run-ledger

### .dev/tasks/to-do/TASK-WF-mergedRequiremen-20261126-173239/TASK-WF-mergedRequiremen-20261126-173239.md:1-140
```markdown
---
schema: workflow-plan/1.2
source: ./source.md
strategy: systematic
depth: standard
slug: TASK-WF-mergedRequiremen-20261126-173239
version: "1"
priority: Medium
created_date: "2026-11-26"
---

# Run ledger for /sc:sweep: rebuild script, sweep input, hook file, install notes

Source: ./source.md
Goal: `superclaude sweep run` finds its Orca Run ids from a Run ledger file that a deterministic `superclaude sweep ledger` command rebuilds, a hook file appends new Runs at once, and a doc gives Coder (Coder#545) the schedule and hook registration to adopt. Source issue: IronbellyOrg/IronClaude#895.

## Constraints

- UV only: run tests and scripts with `uv run pytest ...` and `uv run python ...`; never `python -m`, bare `python script.py` or `pip install`.
- Edit under `src/superclaude/` (plus `tests/`, `docs/`, and the one hook mirror under `plugins/superclaude/hooks/scripts/`), then run `make sync-dev`; never stage `.claude/` contents; no text in an installed command, skill or hook may tell an agent to read a `src/superclaude/...` path (use `~/.claude/...` installed paths).
- The ledger builder never calls Orca through `src/superclaude/cli/sweep/probes.py`: `ALLOWED_ORCA` and `tests/sweep/test_probes_allowlist.py` stay unchanged and passing. `src/superclaude/cli/main.py` is not edited.
- Not allowed: `orca orchestration reset`, deleting a Run, Orca link flags (`--issue`, `--pr`), editing `~/.claude/settings.json`, installing a crontab, scheduling anything, adding the hook to `src/superclaude/hooks/hooks.json` (Coder#545 registers it), committing, pushing, opening a pull request, or writing to any GitHub issue or Project without the owner's go.
- Pytest tests fake Orca and never start it. The only real Orca calls of this plan are the one scratch `run-create` of Task 8 and the real run of Task 11; neither is part of pytest.
- Behaviour decisions are fixed by the source (`./source.md`): do not add a package of modules, `show`, `path`, `--timeout`, `--no-ledger`, a sweep `--ledger` flag, a `~/.superclaude/` path, a shrink guard, extra exit codes, a main-checkout exclusion or an age cutoff.

## Phase 1: Ledger builder

## Task 1: Add the pure inclusion rules to a new `src/superclaude/cli/sweep/ledger.py`

Create `src/superclaude/cli/sweep/ledger.py` with the constants `TERMINAL_STATUSES = frozenset({"completed", "failed", "cancelled"})`, `NEW_FALLBACK_HOURS = 24`, `STALE_TASK_DAYS = 7`, `LEGACY_RUN_ID = "run_legacy_local"`, `LEDGER_VERSION = 1`, and a pure module-level function `decide(runs, workers_by_run, tasks_by_run, live_worktrees, previous, generated_at, hook_entries)` that does no I/O and returns the ledger `runs` entries plus the `counts` block of the schema in `./source.md` (sections "Ledger file and schema" and "Inclusion rules"). Rules: only Runs from `run-list` with `legacy == 0` and `id != "run_legacy_local"`; `live_worktree` when a worker row's `resource.worktreeId` equals, as a whole string, an `id` of `worktree list --json` (a row with no `resource` or a null `worktreeId` never matches); `unfinished_task` when any Task status is not in `TERMINAL_STATUSES` (denylist: unknown statuses count as unfinished); `new` when `created_at >= previous.generated_at`, or, with no usable previous ledger, when `created_at` is within the last `NEW_FALLBACK_HOURS`; a hook entry (`source == "hook"`) with `added_at >= generated_at` is kept as `hook_added`, an older one is re-evaluated like any Run. Also set per entry `live_worktree_ids`, `unfinished_task_count`, `main_checkout_only` (every matched worktree has `isMainWorktree` true), `stale_open_tasks_only` (admitted only by `ready` or `blocked` Tasks older than `STALE_TASK_DAYS`; read the Task age from the `task-list --json` field that exists, verified against one real `orca orchestration task-list --run <id> --json` call, falling back to the Run's `updated_at`), and the `blocked_only` count in `counts`. Put the comment `shortcut: no age cutoff and no main-checkout exclusion (over-inclusion is the safe direction), add one only if the owner decides` next to the rules. Create `tests/run_ledger/__init__.py` and `tests/run_ledger/test_rules.py`.

Acceptance criteria:
- `uv run pytest tests/run_ledger/test_rules.py -v` passes with these named tests: `test_live_worktree_run_in`, `test_deleted_worktrees_only_run_out`, `test_unfinished_task_run_in` (parametrised: `ready`, `blocked`, `in_progress` and an unknown status are IN; `completed`, `failed`, `cancelled` are OUT), `test_new_run_in`, `test_new_fallback_24h_when_no_previous_ledger` (a Run under 24 h old is IN, an older one OUT), `test_legacy_run_out` (both `run_legacy_local` and a `legacy:1` Run, even with a live worktree), `test_worktree_id_exact_match_only` (same path, different repoId gives no match), `test_null_worktree_id_no_match`, `test_main_checkout_only_and_stale_flags`.
- `decide` has no import of `subprocess`, `os` file calls or `click` inside its body; the test file calls it with plain dicts and no monkeypatching.

## Task 2: Add the Orca reader and the implausible-result guards to `src/superclaude/cli/sweep/ledger.py`

Depends on: Task 1

Add to `src/superclaude/cli/sweep/ledger.py` a small Orca runner (`subprocess.run(argv, capture_output=True, timeout=30)` with a fixed argv list and no shell) resolved with `shutil.which("orca")` (an absolute path only; do not reuse `find_orca` from `src/superclaude/cli/issue_watch/launch.py`, because it needs that package's Runner object and an extra `orca skills list --json` probe), and a function `build_ledger(runner, previous, now)` that calls only `orca orchestration run-list --json`, `orca worktree list --json`, `orca orchestration task-list --run <id> --json` and `orca orchestration worker-list --run <id> --json --limit 100 [--cursor <c>]`. Take `generated_at` before the first Orca call. Fetch Tasks first and fetch workers only for Runs not already IN by Task or `new`. Page `worker-list` while `result.page.hasMore` is true using `result.page.nextCursor`; a repeated cursor or more than 50 pages for one Run is a failure. The Run list comes from `run-list` only (an unknown Run returns ok with zero workers from `worker-list`, so existence is never inferred from it). Raise `OrcaFailure` (message starts `orca-failure:`) for a non-zero exit, a timeout, JSON without `"ok": true` or a missing binary (message names "orca not found or Orca app not running"), and `Implausible` (message starts `implausible:`) for: `worktree list` returning 0 worktrees; `run-list` returning 0 Runs while a previous ledger exists; a new ledger with 0 Runs while the previous had at least 1, at least 1 non-legacy Run exists and at least 1 non-legacy Run was created or updated within 24 h (this guard alone is bypassed by an `accept_empty` argument). Add the comment `shortcut: a partial read that returns a plausible non-empty list is not caught, add a shrink guard if one is ever seen`. Create `tests/run_ledger/test_build.py` and `tests/run_ledger/conftest.py` (an autouse fixture that fails any test starting a process unless the test carries the `integration` marker, same idea as `tests/sweep/conftest.py`).

Acceptance criteria:
- `uv run pytest tests/run_ledger/test_build.py -v` passes with these named tests using a fake runner: `test_worker_list_pagination` (three pages), `test_repeated_cursor_fails`, `test_page_cap_fails`, `test_orca_failure_raises` (non-zero exit, timeout, `ok:false`), `test_missing_binary_message`, `test_empty_worktree_list_implausible`, `test_empty_run_list_with_previous_implausible`, `test_zero_included_implausible_needs_recent_run`, `test_accept_empty_overrides_only_the_zero_included_guard`, `test_generated_at_taken_before_first_call`, `test_workers_not_fetched_for_runs_already_in`.
- The module issues no Orca argv outside the four templates above, and `src/superclaude/cli/sweep/probes.py` is not imported by `ledger.py`.

## Task 3: Add the ledger file store to `src/superclaude/cli/sweep/ledger.py`

Depends on: Task 1

Add to `src/superclaude/cli/sweep/ledger.py`: `ledger_path(cli_value)` resolving, in order, the `--ledger` value, the environment variable `SUPERCLAUDE_RUN_LEDGER`, then `${XDG_STATE_HOME:-~/.local/state}/superclaude/run-ledger.json` (never under the repository); `read_ledger(path)` returning the parsed dict or `None` when the file is missing or not valid ledger JSON of `version` 1; a context manager `locked(path, timeout=10)` using `fcntl.flock(LOCK_EX)` on a sidecar `run-ledger.lock` in the same folder, raising `LockTimeout` after 10 s; `write_atomic(path, data)` writing `run-ledger.json.tmp.<pid>` in the same folder, `fsync`, then `os.replace`, and removing the temp file when anything fails; `merge_hook_entries(new_ledger, current_ledger, generated_at)` keeping every current entry with `source == "hook"` and `added_at >= generated_at`; and `add_run(path, run_id, now)` that validates the id with `probes.RUN_ID_RE` (import only that name from `src/superclaude/cli/sweep/probes.py`), takes the lock, appends `{"id", "source": "hook", "reasons": ["hook_added"], "added_at"}` if absent (idempotent), keeps `generated_at` unchanged, and refuses (raises) when the ledger is missing or unreadable. Create `tests/run_ledger/test_store.py`.

Acceptance criteria:
- `uv run pytest tests/run_ledger/test_store.py -v` passes with: `test_path_precedence_flag_env_xdg`, `test_atomic_write_leaves_old_file_and_no_tmp_on_failure` (monkeypatch `os.replace` to raise), `test_lock_timeout`, `test_corrupt_ledger_reads_as_none`, `test_add_idempotent_and_rejects_bad_id`, `test_add_on_missing_ledger_refuses`, `test_add_keeps_generated_at`, `test_concurrent_add_and_build_no_lost_append` (multiprocessing: 20 adds while a slow rebuild runs, all 20 present afterwards).
- Windows locking is not handled; a comment says `shortcut: fcntl is Linux and macOS only, add msvcrt locking if Windows is ever needed`.

## Task 4: Add the `sweep ledger` command and register it on the existing `sweep` group

Depends on: Task 2, Task 3

In `src/superclaude/cli/sweep/ledger.py` add a `click` command named `ledger` (function `ledger_command`) with options `--ledger PATH`, `--dry-run`, `--json`, `--accept-empty`, `--add RUN_ID`. Without `--add`: build with `build_ledger`, then take the lock, call `merge_hook_entries`, and write atomically; `--dry-run` prints the would-be ledger and writes nothing; the stdout summary (or the `--json` object) gives per-reason counts, the number of Runs admitted only through the main checkout, only by stale `ready` or `blocked` Tasks, and held in only by `blocked` Tasks. With `--add`: call `add_run`, no Orca call. On any failure the old ledger file is untouched and one reason goes to stderr starting with `orca-failure:` or `implausible:`. Exit codes: 0 written, 1 `OrcaFailure` or `Implausible` (and `--add` on a missing or unreadable ledger, reason `implausible:`), 2 usage (including a malformed `--add` id), 3 `LockTimeout`. In `src/superclaude/cli/sweep/commands.py`, directly after the `sweep_group` definition (:215), import `ledger_command` from `.ledger` and call `sweep_group.add_command(ledger_command)`. Create `tests/run_ledger/test_cli.py` using `click.testing.CliRunner` on `sweep_group` with a fake runner.

Acceptance criteria:
- `uv run pytest tests/run_ledger/test_cli.py -v` passes with: `test_orca_failure_keeps_old_ledger` (file bytes and mtime unchanged, exit 1, stderr starts `orca-failure:`), `test_implausibly_empty_keeps_old_ledger` (exit 1, stderr starts `implausible:`), `test_accept_empty_overrides_guard_not_orca_failure`, `test_dry_run_writes_nothing`, `test_summary_reports_stale_and_blocked_counts`, `test_add_exit_codes` (0 added, 2 malformed id, 1 missing ledger), `test_lock_timeout_exit_3`, `test_first_build_with_no_previous_ledger_uses_24h_fallback`.
- `uv run pytest tests/sweep/test_cli_registration.py tests/sweep/test_cli_contract.py tests/sweep/test_readonly.py tests/sweep/test_probes_allowlist.py -v` still passes: `superclaude sweep --help` lists both `run` and `ledger`, importing `superclaude.cli.sweep` still does not import `commands` until `sweep_group` is read, and `src/superclaude/cli/main.py` has no diff.

## Phase 2: Sweep reads the ledger

## Task 5: Add `run_source` to `SweepContext` and print it in the report header

Depends on: Task 4

In `src/superclaude/cli/sweep/models.py` add `run_source: str | None = None` as the last field of the frozen dataclass `SweepContext` (:75), and in `src/superclaude/cli/sweep/report.py` make `_header` (:182) append `sanitize(ctx.run_source)` as one more header line when it is not None. Callers that must keep working unchanged: the one `SweepContext(...)` construction in each of `src/superclaude/cli/sweep/commands.py`, `tests/sweep/test_classify.py`, `tests/sweep/test_probes_allowlist.py`, `tests/sweep/test_readonly.py` and `tests/sweep/test_report.py`. Add two tests to `tests/sweep/test_report.py`: `test_header_has_no_run_source_line_by_default` and `test_header_prints_run_source_line_when_set`.

Acceptance criteria:
- `uv run pytest tests/sweep -v` passes, including both new tests; no existing golden or snapshot in `tests/sweep/` changes.
- A report built with `run_source=None` is byte-identical to the report before this change.

## Task 6: Make `superclaude sweep run` fall back to the ledger when no Run is given or bound

Depends on: Task 5

In `run` of `src/superclaude/cli/sweep/commands.py` (:242), replace the `if not runs:` block (:264-266) so that it first tries `probes.bind_run(budget)` and, on `probes.BindingError`, reads the ledger with `ledger.read_ledger(ledger.ledger_path(None))`; when the ledger is usable, validate every id with `probes.RUN_ID_RE` (a malformed id is a usage error, exit 2) and use them as `runs`; when the ledger is missing or corrupt, exit 2 with the original BindingError message plus ` run "superclaude sweep ledger" first`. An explicit `--run` still wins and the ledger is then not read. Build `run_source` as `Run ids from the Run ledger built <generated_at>`, and when `generated_at` is more than `LEDGER_STALE_MINUTES = 90` (new constant in `src/superclaude/cli/sweep/ledger.py`) old add ` . ledger is N min old`; pass it as the sixth argument of `SweepContext`. No new flag and no Orca call for reading the ledger. Add an autouse fixture to `tests/sweep/conftest.py` that points `SUPERCLAUDE_RUN_LEDGER` at a non-existent temporary file so no test reads a real ledger. Create `tests/sweep/test_ledger_input.py` reusing the Orca seams of `tests/sweep/test_cli_contract.py`.

Acceptance criteria:
- `uv run pytest tests/sweep -v` passes with these new named tests: `test_sweep_reads_ledger_when_no_run_and_no_binding`, `test_explicit_run_ignores_ledger`, `test_missing_ledger_exit_2_with_hint`, `test_corrupt_ledger_exit_2_with_hint`, `test_malformed_id_in_ledger_rejected`, `test_stale_ledger_over_90_minutes_adds_age_to_header`, `test_fresh_ledger_header_has_no_age`.
- The existing tests that expect `no Run bound: pass --run <id>` (`tests/sweep/test_probes_allowlist.py:831` and `:886`, and the exit-2 cases of `tests/sweep/test_cli_contract.py`) still pass, and `probes.ALLOWED_ORCA` has no diff.

## Task 7: Update the sweep command and skill text

Depends on: Task 6

Edit `src/superclaude/commands/sweep.md` (the `--run <id>` row of the Options table and the sentence "When no Run is bound and none is named, the command exits ...") so they say that, with no `--run` and no bound Run, the Run ids come from the Run ledger built by `superclaude sweep ledger`, and that a missing ledger exits with a hint. Edit `src/superclaude/skills/sc-sweep-protocol/SKILL.md` near line 19 the same way, keeping the pinned phrase "adds no flag, reads no environment variable and has no worker mode" (required by `tests/commands/test_sweep_command.py:497`) and keeping the skill limited to the one command `superclaude sweep run`. Use installed paths only; no `src/superclaude/` path inside either text. Then run `make sync-dev`.

Acceptance criteria:
- `uv run pytest tests/commands/test_sweep_command.py -v` passes.
- `make verify-sync` reports no difference, and `git status` shows no staged or modified `.claude/` file other than what `make sync-dev` writes (those are never staged).

## Phase 3: Hook file

## Task 8: Capture what `run-create` gives a PostToolUse hook and record the decision

Run exactly one `orca orchestration run-create --objective "scratch Run for the run-ledger hook payload test, safe to ignore" --json` (the brief orders this test; Orca cannot delete the Run, so say so in the decision file; if the call cannot be made, build the fixture from the documented shape and mark the result UNVERIFIED). Save its stdout as `tests/run_ledger/fixtures/run_create_stdout.json`. Read the official Claude Code hooks documentation (context7 or `claude-code-guide`) for the PostToolUse payload of the Bash tool and write `tests/run_ledger/fixtures/posttooluse_run_create.json` with that payload shape (`tool_name`, `tool_input.command`, `tool_response`) wrapping the captured output. Run `orca orchestration run-current` before and after and note whether this terminal is now bound to the scratch Run. Write `./artifacts/hook-decision.md` stating: the captured output, whether a `run_[0-9a-f]{12}` id is in it, the payload shape source, the decision (deliver the hook, or drop it with the reason and the documented fallback of running `superclaude sweep ledger` right after `run-create`), and that exactly one scratch Run was created.

Acceptance criteria:
- `./artifacts/hook-decision.md` exists and ends with a line `Decision: deliver` or `Decision: drop`, with the evidence above.
- `tests/run_ledger/fixtures/run_create_stdout.json` and `tests/run_ledger/fixtures/posttooluse_run_create.json` exist and parse as JSON; no other Run was created and no Run was deleted.

## Task 9: Add the hook script, list it for install, mirror it, and test it

Depends on: Task 4, Task 8

If `./artifacts/hook-decision.md` says `Decision: drop`, create no script, write nothing to the installer, and record in `./artifacts/hook-decision.md` that this task was skipped for that reason; Task 10 then documents the fallback instead. Otherwise create `src/superclaude/hooks/scripts/run-ledger-record.sh` (executable, `set -u`, fail open: always exit 0, never blocks): read stdin JSON with `jq`; act only when `.tool_input.command` runs `orca orchestration run-create` or `orca orchestration worker-start`; take the first `run_[0-9a-f]{12}` found in the Bash result text (`.tool_response`, string or object) and, for `worker-start`, also in the command's `--run` value; call `superclaude sweep ledger --add <id>` silently; when no id is found append one line to `${XDG_STATE_HOME:-$HOME/.local/state}/superclaude/run-ledger-hook.log`; a missing `jq` or `superclaude` also exits 0. Add a header comment in the style of `src/superclaude/hooks/scripts/require-orca-worktree-agent.sh` and the comment `shortcut: the command is matched with a simple pattern, not a full shell tokenizer, a quoted mention can add a harmless extra id`. Add `"run-ledger-record.sh"` with a one-line comment ("PostToolUse(Bash) Run-ledger appender; not registered in hooks.json, Coder#545 registers it") to `_FRESHNESS_SCRIPTS` in `src/superclaude/cli/install_hooks.py` (:42-97). Copy the script byte-for-byte, executable, to `plugins/superclaude/hooks/scripts/run-ledger-record.sh`. Do not touch `src/superclaude/hooks/hooks.json`. Add `tests/run_ledger/test_hook.py` (runs the script with `bash`, a stubbed `PATH`, and the fixtures of Task 8; mark the tests `integration` so the autouse process guard lets them through) and add `test_run_ledger_record_script_is_packaged_listed_and_mirrored` to `tests/cli/test_install_hooks.py` following the pattern at :854-860, plus an assertion that `hooks.json` contains no `run-ledger-record`.

Acceptance criteria:
- `uv run pytest tests/run_ledger/test_hook.py tests/cli/test_install_hooks.py -v` passes with `test_hook_extracts_run_id_from_fixture` (the stub `superclaude` receives `sweep ledger --add <id>`), `test_hook_ignores_other_commands`, `test_hook_no_id_logs_and_exits_0`, `test_hook_fails_open_when_superclaude_missing`, and the new install test.
- `make verify-sync` still passes (every script under `src/superclaude/hooks/scripts/` is a member of `_FRESHNESS_SCRIPTS` and no member is stale) and `source` and `mirror` of the script are byte-equal.

## Phase 4: Install notes for Coder

## Task 10: Write `docs/user-guide/run-ledger.md` for Coder#545 to adopt

Depends on: Task 4, Task 9

Create `docs/user-guide/run-ledger.md` holding: what the ledger is and where it lives (`${XDG_STATE_HOME:-~/.local/state}/superclaude/run-ledger.json`); the schedule recommendation for Coder#545 (system crontab, every 30 minutes at offset minutes such as `17,47`, wrapped in `flock -n` on a lock file, command `superclaude sweep ledger`, with an explicit `PATH` that includes the directory of the Orca CLI shim, output appended to a log under `${XDG_STATE_HOME:-~/.local/state}/superclaude/`), with the reasons from `./source.md` (survives session and Orca restarts, no model, logged non-zero exit; a session-only cron dies with the session; whether an Orca automation can run a non-model command is UNVERIFIED); the hook registration entry `{"matcher":"Bash","hooks":[{"type":"command","command":"~/.claude/hooks/run-ledger-record.sh"}]}` under `hooks.PostToolUse` (or, when Task 9 was skipped, the paragraph that says the hook was dropped, why, and the fallback); the plain statement that in Coder the crontab is rewritten on every boot so a hand-edited crontab is lost and that the schedule and the hook registration are registered by Coder#545, not by this work; the pre-install check `env -i HOME=$HOME PATH=<the cron PATH> superclaude sweep ledger --dry-run` must exit 0 and the `command -v superclaude` check; the session-cron fallback; and the stale warning (90 minutes) the sweep prints when the schedule dies. The doc must not tell the reader to run `crontab -e`.

Acceptance criteria:
- `docs/user-guide/run-ledger.md` exists, names the command `superclaude sweep ledger`, the exact hook registration entry (or the drop paragraph), the pre-install check and the Coder#545 ownership statement, and contains no `crontab -e` instruction and no `src/superclaude/` path.
- Every command and flag the doc names exists in `uv run superclaude sweep ledger --help`.

## Phase 5: Real-run report

## Task 11: Run the real acceptance and write `.dev/issues/895/result.md`

Depends on: Task 7, Task 9, Task 10

Run `uv run pytest tests/run_ledger tests/sweep tests/commands/test_sweep_command.py tests/cli/test_install_hooks.py -v` and save the output to `./artifacts/pytest.log` (a failing test is reported with its output, never hidden). Against the real Orca Runs run `uv run superclaude sweep ledger --dry-run`, then a real write with `uv run superclaude sweep ledger --ledger <temporary path>` timed with `time` (copy the written ledger to `./artifacts/ledger.json`); then `SUPERCLAUDE_RUN_LEDGER=<that path> uv run superclaude sweep run` from a checkout whose terminal has no Run bound (or with the bound-Run lookup failing), timing it and recording the line count of the report it wrote and that it ran without `no Run bound`. Run the pre-install check of Task 10 once with `env -i`. Write `.dev/issues/895/result.md` containing the lines `outcome:` (succeeded, partial or failed, with a one-sentence reason), `artifacts:` (every file this plan wrote, repo-relative), `pull_request: none`, and the report: the ledger path and per-reason counts and stale-candidate figures; the rebuild wall time against the 26.1 s baseline; the sweep wall time over the ledger against 48.6 s and 3,666 lines for all Runs; the hook decision with the fixture evidence and the one scratch Run created; test results; the pre-install check result; and the two open decisions for the owner (age cutoff for stale Runs, and that the schedule and hook registration are left to Coder#545). Do not commit, push or open a pull request.

Acceptance criteria:
- `.dev/issues/895/result.md` exists with `outcome:`, `artifacts:` and `pull_request: none`, and states the measured rebuild time, the measured sweep time and report line count, the ledger counts, and every failing test with its output (or that none failed).
- `./artifacts/pytest.log` and `./artifacts/ledger.json` exist; no Run was deleted, `orca orchestration reset` was not run, nothing was installed or scheduled, and no file was committed.
```

### .dev/tasks/to-do/TASK-WF-mergedRequiremen-20261126-173239/artifacts/codegraph-grounding.md:1-40
```markdown
# Codegraph grounding (workflow Wave 1, 2 and 4)

## Run state
- index_state: fresh (codegraph_status: 4157 files, 58323 nodes, "Changes since index: 0 added, 0 modified, 0 removed")
- checked_at: 2026-11-26T17:33Z
- worktree_root: the run-ledger worktree (`.dev/tasks/to-do/` package root's checkout)
- projectPath: the same checkout root
- access mode: MCP tools (`codegraph_status`, `codegraph_node`, `codegraph_search`, `codegraph_callers`)
- graph tokens: none

## Resolved symbols (each confirmed by a bounded read of the file range)
- `src/superclaude/cli/sweep/commands.py`: `sweep_group` (:215), `run` (:242), `_check_run_ids` (:87), `_check_output`, `_publish`; in `run`, `if not runs:` calls `probes.bind_run(budget)` at :264-266 and `SweepContext(now, span, now - span, checkout, runs)` is built at :267.
- `src/superclaude/cli/sweep/probes.py`: `bind_run` (:397) raises `BindingError("no Run bound: pass --run <id>")` for no binding and a second message when Orca is unavailable; `ALLOWED_ORCA` (:49) pins ten call templates and has no `run-list`.
- `src/superclaude/cli/sweep/models.py`: `SweepContext` frozen dataclass (:75) with fields `now, window, window_start, root, runs`.
- `src/superclaude/cli/sweep/report.py`: `_header` (:182) builds the header lines from `ctx`; `render` (:608), `to_json` (:613).
- `src/superclaude/cli/sweep/__init__.py`: lazy `__getattr__` loads `commands` only when `sweep_group` is read; `src/superclaude/cli/main.py:585-587` imports it and calls `main.add_command(sweep_group, name="sweep")`.
- `src/superclaude/cli/install_hooks.py`: `_FRESHNESS_SCRIPTS` (:42-97) lists every script under `src/superclaude/hooks/scripts/`; `_copy_scripts` (:254) copies only the listed names; `_merge_settings` (:301) registers hooks from `src/superclaude/hooks/hooks.json`.
- `src/superclaude/hooks/scripts/require-orca-worktree-agent.sh` is the pattern for a hook script; its test `tests/cli/test_install_hooks.py:854` asserts it is listed, executable and byte-equal to `plugins/superclaude/hooks/scripts/require-orca-worktree-agent.sh`.
- `src/superclaude/cli/issue_watch/launch.py`: `find_orca(runner, which, timeout)` (:212) needs an `issue_watch` Runner and runs `orca skills list --json`; not reused (decision in Task 2).
- Command file is `src/superclaude/commands/sweep.md` (not under `commands/sc/`); skill is `src/superclaude/skills/sc-sweep-protocol/SKILL.md`.

## Dependents
- `SweepContext` is constructed in `src/superclaude/cli/sweep/commands.py` and in `tests/sweep/test_classify.py`, `tests/sweep/test_probes_allowlist.py`, `tests/sweep/test_readonly.py`, `tests/sweep/test_report.py` (one call each); it is read by `classify.py`, `probes.py`, `report.py`. A new field with a default keeps all five calls valid.
- `sweep_group` is used by `src/superclaude/cli/main.py:585-587`, `tests/sweep/test_cli_contract.py`, `tests/sweep/test_cli_registration.py` (asserts `commands` is not imported until `sweep_group` is read, and `run` is in `sweep --help`), `tests/sweep/test_readonly.py`.
- `tests/sweep/conftest.py` has an autouse fixture that fails any test that starts a process; tests that need `bash` (the hook tests) therefore live outside `tests/sweep/`.
- `bind_run` callers: `commands.run`, `tests/sweep/test_probes_allowlist.py:831` and `:886`.
- `_FRESHNESS_SCRIPTS` consumers: `_copy_scripts`, `Makefile` verify-sync (lines 308-325: every `src/superclaude/hooks/scripts/*.sh` must be a member, and no stale member), `tests/cli/test_install_hooks.py` per-script tests, `src/superclaude/cli/doctor.py` and `install_user_setup.py` through `install_hooks`.
- Skill text is pinned: `tests/commands/test_sweep_command.py:497` requires the phrase "adds no flag, reads no environment variable and has no worker mode" to stay in the skill.

## Pre-check
Run after the plan passed the gate (2026-11-26, advisory, read-only; no plan edit).
- Files the tasks name that exist: `src/superclaude/cli/sweep/{commands,models,report,probes,__init__}.py`, `src/superclaude/cli/install_hooks.py`, `src/superclaude/hooks/scripts/`, `plugins/superclaude/hooks/scripts/`, `src/superclaude/commands/sweep.md`, `src/superclaude/skills/sc-sweep-protocol/SKILL.md`, `tests/sweep/{conftest,test_cli_contract,test_cli_registration,test_readonly,test_probes_allowlist,test_report}.py`, `tests/cli/test_install_hooks.py`, `tests/commands/test_sweep_command.py`, `docs/user-guide/`, `Makefile` (verify-sync). Files the tasks create (do not exist yet): `src/superclaude/cli/sweep/ledger.py`, `tests/run_ledger/*`, `src/superclaude/hooks/scripts/run-ledger-record.sh`, its plugin mirror, `docs/user-guide/run-ledger.md`, `.dev/issues/895/result.md`.
- Symbols that resolve: `sweep_group`, `run`, `_check_run_ids`, `probes.bind_run`, `probes.BindingError`, `probes.RUN_ID_RE` (used at commands.py:90), `SweepContext`, `_header`, `_FRESHNESS_SCRIPTS`, `_copy_scripts`.
- Corrected during planning: the command file is `src/superclaude/commands/sweep.md` (the brief said `commands/sc/sweep.md`); there is no plugin mirror of the sweep command or skill, so Task 7 needs only `make sync-dev`.
- Dependents no task names (advisory): `docs/user-guide/cli-groups.md` and `docs/user-guide/orchestrator-mode.md` mention `superclaude sweep`; they are not changed by the plan and can be synced by `/sc:post-release`. Count: 2 unnamed dependents, 0 missing files, 0 unresolved symbols.
```

## Coverage slice

Rows the deterministic matcher left unmatched (you own these): re-check each against the plan and the spec at .dev/tasks/to-do/TASK-WF-mergedRequiremen-20261126-173239/source.md (Read it).

| Requirement | Spec citation | Match | Best task | Quote |
|---|---|---|---|---|
| INF-006 | source.md:23 | none | 9 (ratio 0.538) | append one id (idempotent; validated with the sweep id pattern `probes.RUN_ID_RE`; merges under the lock; no O |
| INF-008 | source.md:26 | none | 3 (ratio 0.5) | never through `sweep/probes.py`, so the pinned `ALLOWED_ORCA` and `tests/sweep/test_probes_allowlist.py` stay  |
| INF-010 | source.md:42 | none | 2 (ratio 0.571) | `generated_at` is captured BEFORE the first Orca call, so the `new` rule cannot miss a Run created mid-build. |
| INF-016 | source.md:51 | none | 1 (ratio 0.556) | A hook-added entry newer than the rebuild start is kept (see Concurrency); an older one is re-evaluated by the |
| INF-027 | source.md:74 | none | 4 (ratio 0.5) | blocking up to 10 s, then exit 3 with the ledger untouched |
| INF-028 | source.md:75 | none | 1 (ratio 0.55) | A rebuild does all Orca reads first (about 26 s) without the lock, then takes the lock, re-reads the ledger, a |
| INF-032 | source.md:82 | none | 6 (ratio 0.421) | When `generated_at` is older than 90 minutes (the #895 threshold, three missed 30-minute builds) the header ad |
| INF-041 | source.md:97 | none | 3 (ratio 0.5) | Run id present in the output means the hook is delivered; absent means the hook is dropped with that reason |
| INF-053 | source.md:155 | none | 11 (ratio 0.471) | no `orca orchestration reset`, no Run delete; no Orca link flags (`--issue`, `--pr`); no `~/.claude/settings.j |
| INF-054 | source.md:156 | none | 2 (ratio 0.556) | Not built: a package of modules, `show`, `path`, `--timeout`, `--no-ledger`, a sweep `--ledger` flag |
