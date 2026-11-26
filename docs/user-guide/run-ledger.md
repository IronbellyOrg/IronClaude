# Run ledger

The Run ledger is a small JSON file that lists the Orca Runs worth sweeping. `/sc:sweep` reads its Run ids from it when you name no Run and none is bound to the terminal. Orca keeps every Run for ever and has no open or settled status, so without the ledger the sweep either needs `--run <id>` or has to read every Run (on one host, reading all 62 Runs took 48.6 s and printed a 3,666-line report).

Source issue: IronbellyOrg/IronClaude#895. The schedule and the hook registration below are adopted and registered by Coder issue 545, not by this work: nothing here installs, schedules or registers anything.

## What it is and where it lives

- Built by `superclaude sweep ledger`. It is deterministic: it makes four kinds of read-only Orca call (`run-list`, `worktree list`, `task-list`, `worker-list`) and runs no model.
- File: `${XDG_STATE_HOME:-~/.local/state}/superclaude/run-ledger.json`. Use `--ledger <path>` or the environment variable `SUPERCLAUDE_RUN_LEDGER` to point somewhere else. It is never written inside a repository, so there is nothing to stage or ignore.
- A Run is kept when any one of these holds (the legacy Run `run_legacy_local` is always left out):
  - a worker of the Run used a worktree that Orca still lists, the main checkout included;
  - the Run has a Task whose status is not `completed`, `failed` or `cancelled`;
  - the Run was created since the previous build (24 hours back when there is no readable previous ledger).
- It is rebuilt from scratch every time, so a settled Run drops out on the next build. No age cutoff exists: a Run held in only by an old `ready` or `blocked` Task stays until that Task is settled. `superclaude sweep ledger --dry-run` prints how many Runs are in that state, so the owner can decide on a cutoff.
- Safe failure: on any Orca failure, or on a result that looks broken (no worktrees listed, no Runs listed while a ledger exists, or zero Runs kept while recent Runs exist), the old ledger is left untouched, one reason starting `orca-failure:` or `implausible:` goes to stderr, and the exit code is 1. Exit 2 is a usage error and exit 3 is a lock timeout. `--accept-empty` overrides only the zero-Runs check.
- `superclaude sweep ledger --add <run_id>` appends one Run to the existing ledger at once, with no Orca call. The hook below uses it.

## Schedule for Coder#545 to register

Recommended: a system crontab entry, every 30 minutes at off-peak minutes, wrapped in `flock -n`, with an explicit `PATH` that holds the folder of the Orca CLI shim and of `superclaude`, appending output to a log under `${XDG_STATE_HOME:-~/.local/state}/superclaude/`:

```text
PATH=<folder of superclaude>:<folder of the Orca CLI shim>:/usr/local/bin:/usr/bin:/bin
17,47 * * * * flock -n "$HOME/.local/state/superclaude/run-ledger.cron.lock" superclaude sweep ledger >> "$HOME/.local/state/superclaude/run-ledger.cron.log" 2>&1
```

Why a system crontab:

- it survives Claude sessions and Orca restarts;
- it needs no model;
- a failed build exits non-zero and its reason lands in the log.

A cron that lives only inside a Claude session dies with the session, which is the problem being fixed. Whether an Orca automation can run a non-model command is UNVERIFIED, so it is not recommended.

Fallback if Orca needs a desktop session socket that a plain cron job lacks (UNVERIFIED): run the same command line from a session cron.

In Coder the crontab is rewritten on every boot, so a hand-edited crontab is lost; the entry has to be part of what Coder generates. That is the work of Coder#545.

When the schedule dies, `/sc:sweep` still runs from the old ledger, and its report header says `ledger is N min old` once the ledger is over 90 minutes old (three missed 30-minute builds).

## Hook registration for Coder#545 to register

The hook script is `run-ledger-record.sh`. The installer puts it in `~/.claude/hooks/`; it is deliberately not registered by the installer. After a Bash call that ran `orca orchestration run-create` or `orca orchestration worker-start`, it appends that Run to the ledger at once with `superclaude sweep ledger --add <id>`. It never blocks (it always exits 0, and prints nothing), and when it finds no Run id it appends one line to `${XDG_STATE_HOME:-~/.local/state}/superclaude/run-ledger-hook.log`; the next build then picks the Run up through its 24-hour "created since" rule.

Registration entry, under `hooks.PostToolUse` in Claude Code's `settings.json`:

```json
{"matcher":"Bash","hooks":[{"type":"command","command":"~/.claude/hooks/run-ledger-record.sh"}]}
```

Evidence for the design: one real `run-create` call printed the new Run's id in its result (`result.run.id`), so a hook can read it. The hook's input shape is taken from the Claude Code hooks reference; the `tool_response` of a live Bash call was not captured, so the script accepts it as a string or an object. A scratch Run (`run_e97be8837462`) was created for that test; Orca cannot delete it.

## Pre-install check

Before the cron line is registered, on the target host:

```text
command -v superclaude
env -i HOME=$HOME PATH=<the cron PATH> superclaude sweep ledger --dry-run
```

`command -v superclaude` must print a path, and the second command must exit 0. It proves the stripped cron environment finds `superclaude` and reaches Orca. If it fails, the message says `orca not found or Orca app not running` (exit 1, old ledger kept). Where `superclaude` lives on the target host (for example a pipx folder) is UNVERIFIED until this is run there.

## After an Orca database reset

An Orca reset removes every Run, so `run-list` returns none while an old ledger still exists. Every build then exits `implausible:` and keeps the old file. Remove the old ledger file by hand once; the next build starts from the 24-hour rule.
