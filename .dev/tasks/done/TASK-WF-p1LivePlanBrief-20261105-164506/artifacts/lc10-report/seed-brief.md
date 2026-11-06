---
topic: "how a coordinator should name report directories for parallel workers"
domain: process
strategy: systematic
depth: quick
proposals_target: 2
handoff_target: none
created: 2026-11-05T19:56:00Z
---

# Seed Brief: how-a-coordinator-should-name-report-directories-for-parallel-workers

## Problem Statement

An Orca coordinator hands each worker a Task with exactly one report directory, and the worker writes `<report-dir>/return-contract.yaml` there. Two workers must never write the same file, and a retry must never reuse the first attempt's directory. The contract fixes those two rules but names no pattern for the directory itself, so each brief invents one. The question is which naming pattern a coordinator should use, and what it must record.

## Known Context

- Dialogue ran unattended (no person at the keyboard): the answers below come from the repository and the worker contract, not from a person. Quick depth, one batch.
- Q1 (what hurts): the rules say "unique to this Task" (`~/.claude/WORKER-CONTRACT.md` WC-4, WC-11, section 4) but give no format. Nothing in the contract names a slug or a number scheme for directories.
- Q2 (who is affected): the coordinator writes the brief before dispatch; the worker only receives the path; the person reads reports afterwards.
- Q3 (tried before): the contract's own worked example uses `.dev/tdd/auth-1/` for the first try and `.dev/tdd/auth-2/` for the retry. The P1 live plan uses one fixed directory per check, `.dev/p1-live/<command-name>/`.
- Q4 (current health measure): none stated. Collisions are caught only after the fact, because a command refuses a directory that already holds a `return-contract.yaml`.
- Existing conventions found in the repository (see `enrichment/codebase-context.md`): `.dev/brainstorms/<ts>-<slug>/` (brainstorm default), `.dev/reflect/` (reflect), `TASK-WF-<subject>-<YYYYMMDD>-<HHMMSS>` (workflow package, UTC, camelCase subject of at most 16 characters, `-2` to `-9` on collision), nested `<report-dir>/nested/<command>-<n>/` (nested commands).
- A report directory sits inside the worker's own worktree under `.dev/`. A worker in a child worktree gets an absolute path inside that child.

## Constraints

- Exactly one report directory per Task; both `--output` and `--report-dir` together are refused.
- A directory that already holds a `return-contract.yaml`, is inside `.git/` or `.codegraph/`, or is under a distributable skill, agent or command folder of `.claude/` is refused.
- Every retry is a new Task with its own directory (WC-6); an unchanged command line apart from the directory value does not count as new work after three failed starts, and the coordinator makes that comparison itself because Orca counts failures per Task.
- The path must be known before dispatch, so it cannot contain anything only the worker learns (for example a run-time timestamp of the worker).
- Directories under `.dev/tasks` are always staged by the coordinator; other `.dev/` report directories are not part of that rule.

## Success Criteria

- Two Tasks dispatched at the same moment never get the same directory, without either worker having to look at the other.
- Someone reading a directory name can tell which Task and which attempt wrote it, and which command ran.
- A retry's directory differs from the original's, and the old contract stays untouched.
- The coordinator can derive the whole name from information it already holds when it writes the brief.

## Open Questions

- Should the name carry the Orca Task ID (guaranteed unique, but opaque) or a readable command slug plus a counter (readable, but the coordinator must keep the counter)?
- Should the attempt number live in the name (`-1`, `-2`, as in the contract's worked example) or in a parent folder per logical piece of work?
- Where does the date belong: in the name (matches `TASK-WF-*`) or not at all, since git history and the contract carry it?
- Does a fixed per-check name (the P1 live plan style) stay valid once a check is re-run, or does it need an attempt suffix from the start?

## Enrichment Context

Codebase enrichment ran at quality tier `fallback_1` (auggie unavailable; codegraph, Grep, Read). Research enrichment is off under `--unattended`. Full notes: `enrichment/codebase-context.md`.

- The contract demands unique, pre-dispatch, per-Task directories but fixes no format (WC-4, WC-6, WC-11).
- Existing generated names pair a readable subject with a timestamp or counter (`.dev/brainstorms/<ts>-<slug>/`, `TASK-WF-<subject>-<YYYYMMDD>-<HHMMSS>`); only the hand-written P1 live plan uses a bare subject.
- Nothing derives a directory from the Orca Task ID; whether the ID is known before the spec is stored is UNVERIFIED.
