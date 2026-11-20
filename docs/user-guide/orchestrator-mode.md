# Orchestrator Mode Guide: Coordinator, Workers, Sweep and Closeout

Orchestrator mode is how one person supervises many AI sessions without entering each one. One session, the **coordinator**, plans the work and hands each unit to a **worker** through Orca. The person watches from the [observer dashboard](observer.md) and from a dated sweep report, and closes finished work with `/sc:closeout`.

This guide covers what each piece does and how to use it. The rules the coordinator and workers follow are in `~/.claude/WORKER-CONTRACT.md` (installed from `src/superclaude/core/WORKER-CONTRACT.md`); the routing guide is [How We Work](how-we-work.md). The design of the sweep is in `docs/designs/orchestrator-mode.md`.

## The pieces

| Piece | Who uses it | What it does | Writes anything? |
|---|---|---|---|
| Coordinator session | You open it | Plans the work, creates one Orca Task per unit, starts one worker per Task, reads each worker's report, does every push, PR, merge and comment | Yes, outward actions are the coordinator's alone |
| Worker session | Orca starts it for a Task | Runs one IronClaude command and reports with a contract file and a `worker_done` message | Only its own report directory (and a local commit only when the brief grants it) |
| `superclaude observe` | You | Read-only dashboard of the workers and the coordinator's questions | Only the record and snapshot files you ask for |
| `/sc:sweep` (`superclaude sweep run`) | The coordinator or you | One read-only report on a Run, its worktrees and sessions | One dated report file |
| `/sc:closeout` | The coordinator or you | Settles a pull request that already merged: the issue, the work report entry and the worker's Orca task | Comments and a close on GitHub; updates the entry and task |

## Roles in one minute

- **The coordinator is a session you opened.** It is never a session that Orca started as a worker. It creates the Orca Tasks and writes each Task's brief from the template in the worker contract, with a guard line first and the command on its own `Command:` line.
- **Each worker runs one command**, at the top level of its own session, never inside a subagent. Commands never call Orca themselves: fan-out is the coordinator's job.
- **Workers run `--unattended`.** The brief gives each command `--unattended` and exactly one report directory. In that mode the command never stops to ask you a question, writes a `return-contract.yaml` on every outcome, and pushes, merges and opens nothing.
- **Questions go to the coordinator.** A worker that needs a decision sends one message to the coordinator (once per Task). Those messages are what the observer's questions screen lists.
- **Orca creates the worktrees** at its default location. Do not create them with raw `git worktree add`.
- **PRs go through `/sc:pr-submit --monitor 3`**, on `IronbellyOrg/IronClaude` only.
- Some commands are never workers: `/sc:pr-submit`, `/sc:sweep` and `/sc:closeout` stay with the coordinator or the person.

## Watching a run

Open the dashboard from the terminal that holds the coordinator's Run:

```bash
superclaude observe --questions --run <runId>
```

Use the [observer guide](observer.md) for keys and for what each screen means. It shows the workers, how fresh the data is, and the questions waiting on you with the linked worker.

For a written record, run the sweep.

## `/sc:sweep`: one read-only report

```bash
/sc:sweep [--run <id>]... [--window <N>h|<N>d] [--root <dir>] [--output <dir>]
# or without the slash command:
superclaude sweep run [--run <id>]... [--window 6h] [--root <dir>] [--output <dir>]
```

| Option | Default | Meaning |
|---|---|---|
| `--run <id>` | the Run bound to this terminal | An Orca Run id (`run_` plus 12 lowercase hex digits). Repeat for several Runs. With no bound Run and no `--run` it exits with a message asking for one. |
| `--window <N>h\|<N>d` | `6h` | How far back a session counts as active (at most `720h` or `30d`). Open Tasks, questions and unread reports are listed whatever their age. |
| `--root <dir>` | the checkout above the current folder | The checkout root; it must hold `.git`. |
| `--output <dir>` | `<root>/.dev/sweeps/` | That folder or one below it. |

**What it reads:** Orca through a fixed allowlist of read-only commands, `git status` in each worktree (no optional locks), Claude Code session transcripts, and the `return-contract.yaml` and `progress.md` files of the sessions it finds. It changes nothing in Orca, in git or in any worktree. The one file it adds is the report.

**What you get:**

- A report at `<root>/.dev/sweeps/<YYYYMMDD-HHMMSS>-sweep.md` ending with `Report complete`. Twelve sections: header, source coverage, waiting on a person (two lists), could not determine, retained problems, sessions, worktrees, historical, shift brief, what could not be determined, and a footer.
- Every session lands in one of eight classes: `waiting on a person`, `stalled (proved)`, `fenced`, `working`, `finished`, `idle`, `person session (active)` and `could not determine`.
- One JSON object on standard output with the schema version, scope, window, rows, worktrees, `summary` and `report_path`.
- Exit codes: `0` published; `1` internal error or publish failure (message starts with `[sweep <stage>]`); `2` usage error, nothing written.

**The coordinator runs it for you.** Rule WC-16 has the coordinator run `/sc:sweep` on every wake, at most once every 5 minutes, and read the report before it acts. You can also type it yourself. The sweep adds to the coordinator's own liveness check; it does not replace it.

**Limits to read before you trust a count:**

- `stalled (proved)` and `fenced` are never observed yet, so a zero there means nothing. The counts carry the mark `(not observed in Phase 1)`.
- `working` is never produced yet, because the live names of Orca's agent-wait field were never captured. Healthy workers read `could not determine`.
- `Safe to close` and `Removable` never say `yes`. `Next inspection` and the other advisory columns are observations, not advice. You or the coordinator decides.
- Remote hosts are never scanned, so every total is a lower bound.

The follow-up work is tracked in issue [#534](https://github.com/IronbellyOrg/IronClaude/issues/534).

## `/sc:closeout`: settle a merged pull request

Run it after a pull request merged, whether the coordinator or a person merged it:

```bash
/sc:closeout 673
/sc:closeout #673 --issue 606
/sc:closeout 673 --dispatch <id> --entry-key <key>
```

| Argument | Required | Meaning |
|---|---|---|
| `<PR>` | yes | A pull request number or its URL on the origin repo; a URL for another repo is refused |
| `--issue <N>` | no | The issue to settle, when the pull request names none or more than one |
| `--dispatch <id>` | no | The worker's Dispatch id, used only to find the worker's task |
| `--entry-key <key>` | no | The work report entry key; default `<owner>__<repo>__<issue number>` |

What it does, in order:

1. Reads the pull request state first. Only a merged pull request goes on; any other state stops the run with nothing written.
2. Decides whether the issue is done by reading the issue's own criteria (Fix approach, Test plan, acceptance criteria or a "Done when" list) against what the pull request delivered. The words `Fixes`, `Closes` and `Refs` decide nothing. A done issue is closed once with a note saying why and who merged. An issue that is not done stays open with one short note of what remains, and the unmet criteria come back in the result. A case it cannot tell is escalated.
3. Settles the work report entry and sets the worker's Orca task to completed, each after a read. If the report command or the Run is missing, that item says so and is escalated, not skipped.

It prints one YAML result block last, with the status of the issue, the entry and the task. It never merges, never reopens an issue, never edits or deletes a comment, and never stops or messages a worker. "Completed" means merged: it never says "deployed".

## A typical session

1. Open a coordinator session in the project checkout and bind its Orca Run.
2. In another terminal on the same Run, start `superclaude observe --questions --run <runId>`.
3. The coordinator creates Tasks and workers. Watch the ledger for workers that are not alive or are blocked, and the questions screen for anything waiting on you. Answer questions through the coordinator, not through the observer: the observer cannot send anything.
4. When you want a written snapshot, `/sc:sweep`. Read the report path it prints.
5. When a pull request merges, `/sc:closeout <PR>`.

## What is not built

- **Sub-orchestrator mode** (Orchestrator mode Phase 2) is not planned in detail yet. Later phases recorded in the Phase 1 research (a `/sc:close` cleanup command, resume of timed-out sessions, a trust layer for cross-session messages, an orchestrator of orchestrators) are not scheduled.
- **Remote hosts:** neither the sweep nor the observer reads other hosts. Remote fleet for the observer is backlog issue [#604](https://github.com/IronbellyOrg/IronClaude/issues/604).
- **Acting from the dashboard:** the observer shows and never acts. Approving, dispatching and merging stay with the coordinator and you.

## Related

- [Observer guide](observer.md), [Commands reference: `/sc:sweep` and `/sc:closeout`](commands.md), [CLI groups](cli-groups.md), [How We Work](how-we-work.md)
- Technical background: `docs/designs/orchestrator-mode.md`, `docs/architecture/SUPERVISED-ORCHESTRATION-TECHNICAL-REFERENCE.md`
