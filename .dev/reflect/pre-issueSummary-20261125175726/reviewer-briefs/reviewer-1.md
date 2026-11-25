## T1 card excerpt

F2 (Task 6, plan:98-103; deploy path missing). A live Claude process started through the installed launcher runs the copy under `~/.claude/skills/ccsession-tag/`, not the checkout: `ccsession-orca` finds `ccsession` as the file next to its own resolved path (`ccsession-orca:54`), the installer links `~/.local/bin/ccsession` to the installed skill copy (`tests/unit/test_install_ccsession.py:47-55`, `README.md:46-60`: `superclaude install` or `./update.sh` refreshes it). Task 6 reads the switch from a process "started through ccsession after the change" but nothing in Tasks 1-6 says how the changed launcher gets to that installed path (an install or update step, or running the checkout's launcher by absolute path). Without it, Task 6's environment check shows no switch on the coordinator's real route and its acceptance criterion (plan:101) cannot pass for the right reason. Suggested grade: Blocking (Decision: the live acceptance check rests on it) or at least Medium.

F3 (Task 2, plan:46; false stated reason). Task 2 adds a header line "near lines 143-154 ... so `ccsession --help` readers see it". `show_help` prints the header only up to the line `# The wrapper always runs` (`ccsession:2271`), and that line is line 143 (`ccsession:143`); lines 143-154 are never printed by `--help`. The stated purpose cannot be met at the stated place, and the acceptance criterion (plan:51) only checks that `--help` exits 0, so nothing catches it. Fix: place the line before line 143 (the options block ends at line 136) and add "`--help` output contains it" to the acceptance criteria. Suggested grade: Medium (nothing else rests on it).

F4 (Task 3, plan:60; helper cannot "build on" `_label_run`). `_label_run` writes its own fake Claude that prints only its argv (`tests/unit/test_ccsession_tag.py:1343-1347`) and takes no parameter to swap it, so a helper that prints the one variable must copy that setup rather than build on it. Wording only; an implementer will see it at once. Suggested grade: Note.

F6 (Task 6, plan:98-102; owner-run steps). Sending a message to a live coordinator's inbox and relaunching the owner's coordinator are actions this implementing session may not be allowed to take (the launch level of an `/sc:issue` session forbids messaging other sessions), and the plan lets Task 6 end "not run" with a reason, so the outcome is safe; the plan does not say who runs the live steps. Suggested grade: Note.

### What holds (checked)

- The six exec sites are `ccsession:2448, 2450, 2509, 2511, 2516, 2518`; `export CCSESSION_ORIGIN` is at `ccsession:2438`; the "No topic" block starts at `ccsession:2440`; the env file is sourced at `ccsession:1082-1086` (before tier setup at 2365-2369), so one forced export between 2438 and 2440 reaches every launch. A precedent for forcing a value after the env file exists at `ccsession:1087-1093` (`CCSESSION_PERMISSIONS`).
- The switch is absent from the repo outside `.dev/` (Grep: no match). `ic` execs `claude` directly at `src/superclaude/scripts/ic:128,130`. `WORKER-CONTRACT.md:100-102` holds the coordinator wait the plan preserves.
- Test anchors resolve: `_offline_model_data` (`tests/unit/test_ccsession_tag.py:39`, deletes names at 63-85), `_LAUNCH_CASES` (1465-1472), `_orca_env` (1820), `_orca_no_tty` (1977), `_launch` and `_launch_env` (`tests/unit/test_ccsession_tiers.py:368, 389`), `test_tier_flag_and_named_model` (592, uses `--tier tier0`, `--model gpt-6-astra`).
- Scope: Part 1 only, no settings or installer change, no coordinator-role inference, forced value over shell and env file, no universal-coverage claim, no memory pressure forced: all stated in Constraints (plan:19-27).

### Risk surface

Blast radius: one unconditional export reaches every Claude started by `ccsession` and `ccsession-orca` and everything those processes spawn; the plan documents the session-wide effect (Task 5). No existing test asserts on this variable, so a regression would pass silently without Task 3's tests.

## Grounding hunks

codegraph run state: index_state=fresh checked_at=2026-11-25T17:52:59Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/issue-765 projectPath=/home/coder/workspaces/worktrees/IronClaude/issue-765 (the index reports an interrupted run, so caller rows are leads only; the launcher and wrapper are extensionless bash files that the index does not cover, so use Read, Grep and Glob on them)

Citation rule: every hunk line below starts with its real line number in the named file (`  123| text`). Cite `<file>:<line>` with those numbers, or Read the file yourself; never cite a line number of this brief.

### .dev/tasks/to-do/TASK-WF-issueSummary-20261125-175231/TASK-WF-issueSummary-20261125-175231.md:1-104

````text
    1| ---
    2| schema: workflow-plan/1.2
    3| source: ./source.md
    4| strategy: systematic
    5| depth: standard
    6| slug: TASK-WF-issueSummary-20261125-175231
    7| version: "1"
    8| priority: Medium
    9| created_date: "2026-11-25"
   10| ---
   11| 
   12| # Start every ccsession Claude process with the low-memory reap switch set (issue 765, Part 1)
   13| 
   14| Source: ./source.md
   15| Goal: Every Claude Code process that `ccsession` starts (new, resumed, tagged, untagged, with or without a model, directly or through `ccsession-orca`) has `CLAUDE_CODE_DISABLE_BG_SHELL_PRESSURE_REAP=1` in its initial environment whatever the shell or `~/.claude/ccsession.env` held, the scope and override decision is recorded, the session-wide effect and its limits are documented, and a live coordinator launch shows the switch in the process environment and its message watch still receiving messages.
   16| 
   17| ## Constraints
   18| 
   19| - Part 1 only. Part 2 of the old issue body (research, guard, sampler, browser stops, the eight plan problems) is dropped and is not planned, built or estimated here.
   20| - The base branch is `origin/integration`, not `master`. The switch is absent from `src/` at integration commit `a6fec24480e8cc65abbb16b194625e2ea52238c7`; a Grep of the repo outside `.dev/` found no match.
   21| - Implement in `src/superclaude/` and `tests/`. The `.claude/` mirror is generated by `make sync-dev` and its contents are never edited by hand and never staged.
   22| - Launch-time environment only. No settings change (`src/superclaude/cli/user_settings_defaults.json` stays untouched), no installer change (`wire_ccsession` copies the launcher unchanged), no automatic watch restart, and the coordinator wait contract at `src/superclaude/core/WORKER-CONTRACT.md` lines 100-104 is preserved as written.
   23| - No coordinator-only predicate exists in the launcher: `CCSESSION_ORIGIN` records who chose a name, not the coordinator role. Do not infer a role from a label or from `CCSESSION_ORIGIN`.
   24| - A shell value or env-file value must never leave a ccsession launch without `=1`. An earlier suggestion to respect overrides is not owner approval to weaken this.
   25| - Direct `ic` (`src/superclaude/scripts/ic` lines 128 and 130) and a bare `claude` start bypass ccsession. Do not widen this issue into launcher work for them, and do not claim universal coverage.
   26| - Tests capture only the named non-secret switch, never a full environment dump, and stay isolated from the developer's own environment values.
   27| - The live check reads only the exact switch from the process environment and never forces memory pressure on the shared host.
   28| 
   29| ## Phase 1: Record the scope and override decision
   30| 
   31| ## Task 1: Trace the real launch route and record the scope and override decision
   32| 
   33| Write `./artifacts/scope-decision.md` in this package. Trace, by reading the live files, how a coordinator's Claude process is started: Orca's configured Claude command reaches `src/superclaude/skills/ccsession-tag/ccsession-orca` (ends in `exec "$CCSESSION" --name "$name" --shim --claude-args "$@"` at line 261 or the untagged `exec` at line 263), which execs `src/superclaude/skills/ccsession-tag/ccsession`, whose six `exec "$CLAUDE_BIN"` sites are at lines 2448, 2450, 2509, 2511, 2516 and 2518 (untagged, resumed and new-label launches, each with and without `--model "$PROFILE_MODEL"`). Record that the user env file is sourced at lines 1082-1086, before tier and profile setup, so a value set there or in the shell reaches the exec sites unless the launcher sets it afterwards; and that `CCSESSION_ORIGIN` (lines 2428-2438) tracks who chose a name, not the coordinator role. Record the decision: protect all ccsession launches, because no verified coordinator-role signal exists in the launcher; and the override policy: the launcher sets the value to `1` unconditionally after the env file is sourced, replacing any shell or env-file value. List the bypass routes (`src/superclaude/scripts/ic`, bare `claude`, an Orca Claude command left as plain `claude`) as not covered.
   34| 
   35| Acceptance criteria:
   36| - `./artifacts/scope-decision.md` exists and names the decision "all ccsession launches" with the reason that no coordinator-role signal exists, citing `ccsession` lines 2428-2438.
   37| - The file states the override policy (forced to `1` after the env file is sourced) and names the three uncovered routes, with `src/superclaude/scripts/ic` lines 128 and 130 cited for the direct exec.
   38| - Every `file:line` it cites was re-read in this task and matches the live file; the six exec lines are listed individually.
   39| 
   40| ## Phase 2: Set the switch in the launcher
   41| 
   42| ## Task 2: Export the switch in the launcher before every Claude exec
   43| 
   44| Depends on: Task 1
   45| 
   46| In `src/superclaude/skills/ccsession-tag/ccsession`, add one unconditional `export CLAUDE_CODE_DISABLE_BG_SHELL_PRESSURE_REAP=1` with a short comment (what the switch stops, that it is forced over any shell or env-file value, and that it applies to every ccsession launch) directly after `export CCSESSION_ORIGIN` at line 2438 and before the "No topic" block at line 2440, so one statement reaches all six exec sites and runs after the env file (lines 1082-1086), tier or profile setup (lines 2365-2369) and the shim token step. Add one line to the header comment block near lines 143-154 stating the same scope so `ccsession --help` readers see it. Do not edit `ccsession-orca`, `src/superclaude/scripts/ic`, the installer or any settings default.
   47| 
   48| Acceptance criteria:
   49| - A fake Claude started through `ccsession` in each of the six launch forms sees `CLAUDE_CODE_DISABLE_BG_SHELL_PRESSURE_REAP` equal to `1` (checked by the tests of Tasks 3 and 4).
   50| - With `CLAUDE_CODE_DISABLE_BG_SHELL_PRESSURE_REAP=0` in the shell, and with `export CLAUDE_CODE_DISABLE_BG_SHELL_PRESSURE_REAP=0` in the file named by `CCSESSION_ENV_FILE`, the fake Claude still sees `1`.
   51| - `git diff --stat` shows `ccsession` as the only non-test source file changed by this task, and `ccsession --help` still exits 0.
   52| - The fast-path commands that exit above line 2438 (`--help`, `--list`, `--sync-name` and the others) are unchanged in behavior.
   53| 
   54| ## Phase 3: Regression tests
   55| 
   56| ## Task 3: Cover every launch line, conflicting values and the Orca wrapper in the ccsession tag tests
   57| 
   58| Depends on: Task 2
   59| 
   60| In `tests/unit/test_ccsession_tag.py`: add `CLAUDE_CODE_DISABLE_BG_SHELL_PRESSURE_REAP` to the names the autouse fixture `_offline_model_data` deletes (lines 63-85) so a developer or coordinator shell cannot leak a value into any test. Add a helper that builds on `_label_run` (lines 1333-1373) with a fake Claude that prints only that one variable as JSON, and parametrize it over the existing `_LAUNCH_CASES` (lines 1465-1472: untagged `-p x` without and with `--profile claude`; new label `demo` and resumed label `demo` (saved transcript), each without and with `--profile claude`), so all six exec lines are covered, for three starting states: variable unset, shell value `0`, and an env file (`CCSESSION_ENV_FILE`) that exports `0`. Add one test through the real wrapper using `_orca_env` and `_orca_no_tty` (lines 1820 and following) with the fake Claude record extended by the one variable, covering both the named exec (`CCSESSION_NAME` set) and the untagged exec of `ccsession-orca`, with a shell value of `0`. Put `reap` in every new test function name so `-k reap` selects exactly these.
   61| 
   62| Acceptance criteria:
   63| - `uv run pytest tests/unit/test_ccsession_tag.py -k reap -v` runs one case per launch form and starting state (six forms by three states) plus the two wrapper cases, and all pass.
   64| - Temporarily removing the export added in Task 2 makes those new tests fail (each launch form fails in the unset state), then restoring it makes them pass again.
   65| - The existing tests in the file still pass, including the argv assertions of `test_every_launch_restores_grep_and_glob` (the new variable is an environment change only and adds no argument).
   66| - No test prints or asserts on a full environment; only the one named variable is captured.
   67| 
   68| ## Task 4: Cover tier and model selection in the tier launch tests
   69| 
   70| Depends on: Task 2
   71| 
   72| In `tests/unit/test_ccsession_tiers.py`: extend the fake Claude written by `_launch_env` (lines 389-453) to also record `os.environ.get("CLAUDE_CODE_DISABLE_BG_SHELL_PRESSURE_REAP", "")`, and make `_launch_env` drop that variable from the copied developer environment next to the existing `CLAUDE_CODE_MAX_CONTEXT_TOKENS` handling (lines 430-436). Add tests using `_launch` (lines 368-386): a default-tier launch (as in `test_default_tier_sets_model_and_tier_window`), a launch with `"work", "--tier", "tier0"` and one with `"work", "--model", "gpt-6-astra"` (the arguments `test_tier_flag_and_named_model` at line 592 already uses), and a default-tier launch with `CLAUDE_CODE_DISABLE_BG_SHELL_PRESSURE_REAP="0"` passed through `_launch`'s extra environment; each asserts the recorded value is `1`. Put `reap` in every new test function name so `-k reap` selects exactly these.
   73| 
   74| Acceptance criteria:
   75| - `uv run pytest tests/unit/test_ccsession_tiers.py -k reap -v` passes with all four tests (default tier, `--tier tier0`, `--model gpt-6-astra`, conflicting `0`), and the existing assertions of `test_default_tier_sets_model_and_tier_window` (context, compact, base URL) are unchanged and still pass.
   76| - `uv run pytest tests/unit/test_ccsession_tag.py tests/unit/test_ccsession_tiers.py tests/unit/test_install_ccsession.py -q` passes with no new failure (the install test file is the symlink regression surface for the unchanged launcher and wrapper).
   77| - `uv run ruff check` and `uv run ruff format --check` report nothing for the two changed test files (`ccsession` is a shell file and is outside Ruff).
   78| 
   79| ## Phase 4: Documentation and mirror sync
   80| 
   81| ## Task 5: Document scope, session-wide effect and limits in the README, then sync the dev mirror
   82| 
   83| Depends on: Task 3, Task 4
   84| 
   85| In `src/superclaude/skills/ccsession-tag/README.md`, add a subsection "Low-memory protection for the message watch" directly after "Tab title in Orca" (ends at line 609, before "## Tiers (Coder workspaces)" at line 613), and add one cross-reference sentence in the Orca section (lines 392-426) beside the Orca command configuration. State: every ccsession launch (new, resumed, tagged, untagged, through `ccsession-orca`) starts Claude Code with the switch set to `1`; the reason is that the launcher has no verified coordinator-role signal; the value is forced and overrides a shell or `~/.claude/ccsession.env` value; the effect is session-wide, so every background command in that Claude process, not only the message watch, is exempt from Claude Code's low-memory cleanup; a process's environment is fixed at start, so an already running session stays unprotected until it is relaunched (a resume through ccsession starts a new process and is protected); and the routes that bypass ccsession (`ic`, bare `claude`, an Orca Claude command not set to `ccsession-orca`) are not covered. Then run `make sync-dev` and `make verify-sync`.
   86| 
   87| Acceptance criteria:
   88| - The README subsection exists after "Tab title in Orca" and states each of the six points above; it does not claim universal coverage, and it describes the effect only as far as `./artifacts/scope-decision.md` supports.
   89| - `make verify-sync` exits 0 after `make sync-dev`, and `git status --short` shows no path under `.claude/` other than the already tracked `.claude/settings.json` as changed or untracked.
   90| - `grep -rn 'src/superclaude' src/superclaude/skills/ccsession-tag/README.md` adds no new hit introduced by this task.
   91| 
   92| ## Phase 5: Live proof and recorded limits
   93| 
   94| ## Task 6: Record live launch and message-watch evidence and its limits
   95| 
   96| Depends on: Task 5
   97| 
   98| Write `./artifacts/live-proof.md`. Identify the actual coordinator launch route in use (Orca Settings, Agents, Claude, Command set to `ccsession-orca`, or not) and record how it was read; if it cannot be read, mark it UNVERIFIED. For a Claude process started through ccsession after the change (a fresh launch and a resumed launch, in an existing terminal or the owner's relaunched coordinator; create no worktree), read only the exact switch from its environment, for example `tr '\0' '\n' < /proc/<pid>/environ | grep -x 'CLAUDE_CODE_DISABLE_BG_SHELL_PRESSURE_REAP=1'`, and record the output line only. For the coordinator, record that an Orca message sent to its inbox was received and that the wait `orca orchestration check --wait --types status,dispatch,worker_done,merge_ready,escalation,handoff,decision_gate,question,heartbeat --timeout-ms 300000` renewed across at least two five-minute cycles. Do not force memory pressure. List what was not run (the installed Claude runtime gate and any low-memory behavior are not re-proved) and each bypass route found.
   99| 
  100| Acceptance criteria:
  101| - `./artifacts/live-proof.md` exists and holds, for the fresh and the resumed launch, the single matching environment line and the date and time it was read, with no other environment content.
  102| - It records the message sent, the time it was received and two consecutive five-minute wait cycles, or states plainly "not run" with the reason (for example no live coordinator or Orca access) and marks the plan outcome partial for that item; live access availability is Not known yet and an unrun check is never reported as passed.
  103| - It lists the limits: low-memory behavior not exercised, the installed runtime gate not re-proved, and every route that bypasses ccsession.
  104| 
````

### src/superclaude/skills/ccsession-tag/ccsession:126-146

````text
  126| #                             tier models are unchanged. Any other non-empty value
  127| #                             exits 2 on every ccsession call, --help included. Read
  128| #                             from the shell environment, not from
  129| #                             ~/.claude/ccsession.env; stays exported to nested
  130| #                             launches. Flags you pass to Claude, and a
  131| #                             CC_CLAUDE_FLAGS set in the shell or the env file,
  132| #                             still apply
  133| #   ccsession --refresh-models
  134| #                             Check now for the latest profiles and model list
  135| #   ccsession --models-status Show which model data is in use and when it was checked
  136| #   ccsession --help          Show this help
  137| #
  138| # Profiles and the shim's model list come from ccsession-models.json. Every
  139| # launch checks IronClaude for a newer copy (at most ~2 seconds, cached in
  140| # ~/.cache/ccsession/). Private add-on profiles skip it; set
  141| # CCSESSION_MODELS_REFRESH=0 to skip it everywhere.
  142| #
  143| # The wrapper always runs claude with --allowedTools=Grep and, unless
  144| # CCSESSION_PERMISSIONS=default is set, with --dangerously-skip-permissions.
  145| # On macOS, Linux, and WSL, Claude Code leaves the Grep and
  146| # Glob tools out by default. Naming either one in --allowedTools when the
````

### src/superclaude/skills/ccsession-tag/ccsession:1080-1093

````text
 1080| # Source per-user env (proxy base URL, auth tokens, etc.) before launching
 1081| # claude. Keep this file out of version control — it holds secrets.
 1082| CCSESSION_ENV_FILE="${CCSESSION_ENV_FILE:-$HOME/.claude/ccsession.env}"
 1083| if [ "$CCSESSION_SKIP_ENV_FILE" != 1 ] && [ -f "$CCSESSION_ENV_FILE" ]; then
 1084|   # shellcheck disable=SC1090
 1085|   . "$CCSESSION_ENV_FILE"
 1086| fi
 1087| # CCSESSION_PERMISSIONS comes from the shell only: undo a change the env file made,
 1088| # so a nested ccsession sees the value this launch used.
 1089| if [ -n "$_cc_permissions" ]; then
 1090|   export CCSESSION_PERMISSIONS="$_cc_permissions"
 1091| else
 1092|   unset CCSESSION_PERMISSIONS
 1093| fi
````

### src/superclaude/skills/ccsession-tag/ccsession:2268-2272

````text
 2268| }
 2269| 
 2270| show_help() {
 2271|   awk 'NR >= 2 { if ($0 ~ /^# The wrapper always runs/) exit; sub(/^# ?/, ""); print }' "$0"
 2272|   if [ "$TIER_MODE" = 1 ]; then
````

### src/superclaude/skills/ccsession-tag/ccsession:2423-2452

````text
 2423| # Who chose this launch's name, for the hook's new-session marker (R2.2). A launch
 2424| # rule only: --sync-name and the other fast-path commands exit above this point,
 2425| # which matters because Claude Code sets CLAUDECODE for its hook processes too.
 2426| # Inside Claude Code the launch is an agent's; else a value ccsession-orca handed
 2427| # over is kept; else a person on a terminal, and an agent with none.
 2428| if [ -n "${CLAUDECODE:-}" ]; then
 2429|   CCSESSION_ORIGIN=agent
 2430| else
 2431|   case "${CCSESSION_ORIGIN:-}" in
 2432|     human | agent) ;;
 2433|     *)
 2434|       if [ -t 0 ] && [ -t 1 ]; then CCSESSION_ORIGIN=human; else CCSESSION_ORIGIN=agent; fi
 2435|       ;;
 2436|   esac
 2437| fi
 2438| export CCSESSION_ORIGIN
 2439| 
 2440| # No topic (bare --shim and/or --profile) starts a normal untagged session.
 2441| if [ "$NAME_GIVEN" != 1 ] && { [ "$#" -eq 0 ] || [[ "${1:-}" == -* ]]; }; then
 2442|   set -- "$@" ${CLAUDE_PASSTHROUGH[@]+"${CLAUDE_PASSTHROUGH[@]}"}
 2443|   # A label inherited from a ccsession session around this one is not ours.
 2444|   unset CLAUDE_TOPIC CCSESSION_TOPIC_CWD
 2445|   echo "[ccsession] Starting untagged session" >&2
 2446|   orca_terminal_title
 2447|   if [ -n "${PROFILE_MODEL:-}" ]; then
 2448|     exec "$CLAUDE_BIN" $CC_CLAUDE_FLAGS ${CC_SETTINGS_ARGS[@]+"${CC_SETTINGS_ARGS[@]}"} --model "$PROFILE_MODEL" "$@"
 2449|   else
 2450|     exec "$CLAUDE_BIN" $CC_CLAUDE_FLAGS ${CC_SETTINGS_ARGS[@]+"${CC_SETTINGS_ARGS[@]}"} "$@"
 2451|   fi
 2452| fi
````

### src/superclaude/skills/ccsession-tag/ccsession-orca:44-55

````text
   44| # ccsession sits next to the real script; resolve the ~/.local/bin symlink.
   45| # Plain readlink in a loop because older macOS readlink has no -f.
   46| _self="$0"
   47| while [ -L "$_self" ]; do
   48|   _link="$(readlink "$_self")"
   49|   case "$_link" in
   50|     /*) _self="$_link" ;;
   51|     *) _self="$(dirname "$_self")/$_link" ;;
   52|   esac
   53| done
   54| CCSESSION="$(cd "$(dirname "$_self")" && pwd)/ccsession"
   55| 
````

### src/superclaude/skills/ccsession-tag/README.md:590-613

````text
  590| `ccsession --check-name <name>` exits 0 when the name is valid, else 1.
  591| 
  592| ### Tab title in Orca
  593| 
  594| In any Orca terminal (`ORCA_PANE_KEY` set), ccsession sets the tab title to
  595| `<label> · Claude Code`, or `Claude Code` for an untagged session, and starts
  596| Claude Code with `CLAUDE_CODE_DISABLE_TERMINAL_TITLE=1` so it keeps that title.
  597| Orca's web and mobile server treats a pane as running Claude only while its
  598| title contains the word "claude"; Claude Code's own title is its AI
  599| conversation name, so without this a resumed session dropped out of the Orca
  600| Web sidebar and the phone. Other terminals keep Claude Code's own titles.
  601| 
  602| Because Claude Code's own title is off, a `/rename` reaches the tab through
  603| Orca: at your next message the hook sets the tab title to
  604| `<new name> · Claude Code` (`orca terminal rename`). When you leave Claude Code
  605| (or, after a crash, at the next ccsession launch in that tab) ccsession takes
  606| that title off again, but only while the tab still shows it: a name you typed
  607| into Orca since is kept. Renaming the tab in Orca still works, but only
  608| changes the tab: Claude Code and ccsession never see that name, so use
  609| `/rename` to rename a session.
  610| 
  611| ---
  612| 
  613| ## Tiers (Coder workspaces)
````

### Makefile:10-16

````text
   10| 	@echo "   Run 'make verify' to check installation"
   11| 
   12| # Run tests
   13| test:
   14| 	@echo "Running tests..."
   15| 	uv run pytest
   16| 
````

### Makefile:46-51

````text
   46| 
   47| # Linting
   48| lint: lint-architecture
   49| 	@echo "Running linter..."
   50| 	uv run ruff check .
   51| 
````

### .gitignore:125-129

````text
  125| tmp/
  126| .cache/
  127| .claude/*
  128| !.claude/settings.json
  129| # (R3) Lookup-cache tracked artifacts — user-authorized exception (merged-requirements.md Gitignore Exception)
````

### tests/unit/test_ccsession_tag.py:1333-1373

````text
 1333| def _label_run(
 1334|     tmp_path: Path,
 1335|     transcript: bool,
 1336|     args: tuple[str, ...] = ("demo",),
 1337|     extra_env: dict[str, str] | None = None,
 1338| ) -> tuple[subprocess.CompletedProcess[str], bool]:
 1339|     """Run ccsession on a saved label; return the finished process and whether the label stayed."""
 1340|     home = tmp_path / "home"
 1341|     work = tmp_path / "work"
 1342|     work.mkdir(parents=True)
 1343|     fake = tmp_path / "claude-args"
 1344|     fake.write_text(
 1345|         "#!/usr/bin/env python3\nimport json, sys\nprint(json.dumps(sys.argv[1:]))\n"
 1346|     )
 1347|     fake.chmod(0o700)
 1348|     projects = home / ".claude" / "projects"
 1349|     topics = projects / str(work.resolve()).replace("/", "-") / "topics"
 1350|     topics.mkdir(parents=True)
 1351|     (topics / "demo.txt").write_text("abc12345-0000-0000-0000-000000000000\n")
 1352|     if transcript:
 1353|         other = projects / "-some-project"
 1354|         other.mkdir()
 1355|         (other / "abc12345-0000-0000-0000-000000000000.jsonl").write_text("{}\n")
 1356|     env = os.environ.copy()
 1357|     env.update(
 1358|         {
 1359|             "HOME": str(home),
 1360|             "CLAUDE_BIN": str(fake),
 1361|             "CCSESSION_ENV_FILE": str(tmp_path / "none.env"),
 1362|             **(extra_env or {}),
 1363|         }
 1364|     )
 1365|     result = subprocess.run(
 1366|         [str(SKILL_DIR / "ccsession"), *args],
 1367|         env=env,
 1368|         cwd=work,
 1369|         text=True,
 1370|         capture_output=True,
 1371|         check=True,
 1372|     )
 1373|     return result, (topics / "demo.txt").exists()
````

### tests/unit/test_ccsession_tag.py:1465-1472

````text
 1465| _LAUNCH_CASES = [
 1466|     (("-p", "x"), False),
 1467|     (("--profile", "claude", "-p", "x"), False),
 1468|     (("demo",), False),
 1469|     (("demo",), True),
 1470|     (("--profile", "claude", "demo"), False),
 1471|     (("--profile", "claude", "demo"), True),
 1472| ]
````

### tests/unit/test_install_ccsession.py:47-56

````text
   47| def test_wire_creates_symlink_and_env(home):
   48|     ok, msg = wire_ccsession(home)
   49|     assert ok, msg
   50|     skill = home / ".claude/skills/ccsession-tag"
   51|     dest = home / ".local/bin/ccsession"
   52|     env = home / ".claude/ccsession.env"
   53|     assert dest.is_symlink() and dest.resolve() == (skill / "ccsession").resolve()
   54|     orca = home / ".local/bin/ccsession-orca"
   55|     assert orca.is_symlink() and orca.resolve() == (skill / "ccsession-orca").resolve()
   56|     assert (skill / "ccsession-orca").stat().st_mode & 0o111
````


## Coverage slice

| Requirement | Card ID | Status | Grounding |
|---|---|---|---|
| INF-005: start every coordinator's Claude process with `CLAUDE_CODE_DISABLE_BG_SHELL_PRESSURE_REAP=1` in its initial... | Task 5 | covered (containment) | source.md:11 |
| INF-006: Change the ccsession launcher | Task 1 | covered (containment) | source.md:11 |
| INF-007: record whether protection covers coordinators only or all ccsession launches | none (lexical) | unmatched by the lexical rule | source.md:11 |
| INF-008: document the session-wide effect and the need to launch a new process | Task 5 | covered (containment) | source.md:11 |
| INF-009: verify fresh and resumed launches | none (lexical) | unmatched by the lexical rule | source.md:11 |
| INF-010: Part 2 is dropped entirely, including research, guard, sampler, browser stops and the eight plan problems; ... | none (lexical) | unmatched by the lexical rule | source.md:11 |
| INF-011: Use `origin/integration`, not the old body's `master` | none (lexical) | unmatched by the lexical rule | source.md:11 |
| INF-012: Recommend all ccsession launches because there is no verified coordinator-role signal in the launcher | Task 1 | covered (containment) | source.md:13 |
| INF-013: The plan must record its decision | Task 1 | covered (containment) | source.md:13 |
| INF-014: ensure a conflicting inherited or env-file value cannot leave a protected coordinator without `=1` | none (lexical) | unmatched by the lexical rule | source.md:13 |
| INF-015: do not treat earlier suggestions to respect overrides as owner approval to weaken the final requirement | none (lexical) | unmatched by the lexical rule | source.md:13 |
| INF-016: Direct `ic` and bare Claude launches bypass ccsession, so verify the actual coordinator launch route rather... | Task 1 | covered (containment) | source.md:13 |
| INF-017: 2 hours to trace the real route and record scope/override policy | Task 1 | covered (containment) | source.md:15 |
| INF-018: 1 hour for the shared export and README | none (lexical) | unmatched by the lexical rule | source.md:15 |
| INF-019: 2 hours for branch/configuration regression tests | none (lexical) | unmatched by the lexical rule | source.md:15 |
| INF-020: 1 hour for checks and synchronization | none (lexical) | unmatched by the lexical rule | source.md:15 |
| INF-021: 2 hours for live launch/message evidence and recording limitations | none (lexical) | unmatched by the lexical rule | source.md:15 |
| INF-022: The earlier 32-hour complex estimate included the now-dropped research and no longer applies | none (lexical) | unmatched by the lexical rule | source.md:15 |
| INF-023: Cover untagged/raw-resume, labeled resume and new-label launches, both with and without an explicit model. | none (lexical) | unmatched by the lexical rule | source.md:21 |
| INF-024: the shared pre-exec location after 2438 and before 2440 reaches all six Claude exec sites | Task 2 | covered (containment) | source.md:21 |
| INF-025: do not infer roles from labels | none (lexical) | unmatched by the lexical rule | source.md:22 |
| INF-026: Verify the coordinator's actual configuration during live proof. | Task 5 | covered (containment) | source.md:23 |
| INF-027: Add scope, session-wide effect, override behavior, bypasses and treatment of existing sessions. | none (lexical) | unmatched by the lexical rule | source.md:24 |
| INF-028: Add coverage for unset/conflicting shell and env-file values, new/resumed and tagged/untagged launches, and... | Task 3 | covered (containment) | source.md:25 |
| INF-029: Extend targeted capture to prove tier/model/profile selection does not remove protection. | none (lexical) | unmatched by the lexical rule | source.md:26 |
| INF-030: Keep tests isolated from developer environment values. | Task 3 | covered (containment) | source.md:26 |
| INF-031: Run alongside the two launch-test files | Task 4 | covered (containment) | source.md:27 |
| INF-032: installer changes are not required by the recommended launch-only approach | none (lexical) | unmatched by the lexical rule | source.md:27 |
| INF-033: no settings change is planned | Task 6 | covered (containment) | source.md:28 |
| INF-034: Document this boundary | none (lexical) | unmatched by the lexical rule | source.md:29 |
| INF-035: do not expand this issue into unrelated launcher work without a scope decision | none (lexical) | unmatched by the lexical rule | source.md:29 |
| INF-036: Preserve the contract; the fix is launch-time environment, not automatic watch restart. | none (lexical) | unmatched by the lexical rule | source.md:30 |
| INF-037: Check only the exact switch in `/proc/<pid>/environ`, never the full environment | Task 6 | covered (containment) | source.md:31 |
| INF-038: verify receipt and watch renewal across at least two five-minute cycles | Task 6 | covered (containment) | source.md:31 |
| INF-039: Do not force memory pressure on the shared host. | Task 6 | covered (containment) | source.md:31 |
| INF-040: Implement in `src/`, not generated `.claude/` mirrors. | none (lexical) | unmatched by the lexical rule | source.md:32 |
| INF-041: Run the three targeted test files, the required broader regression/lint/format gates and sync checks | none (lexical) | unmatched by the lexical rule | source.md:32 |
