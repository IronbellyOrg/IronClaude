# D1 option (c): the flag is the only switch, and the worker session refuses a brief that lacks it

Position: commands behave exactly as in option (a): only the standalone `--unattended` token switches them (`SPEC:55`). In addition, the worker session (the top-level agent that received Orca's preamble, `SPEC:61`), not the command, checks the brief before running it: if the command line in its Task has no standalone `--unattended`, or is one of the six coordinator-only commands (`SPEC:150-160`), it does not run it, and sends `worker_done --outcome failed` with the reason `brief lacks --unattended`. The coordinator then fixes the brief in a new Task (WC-6, `SPEC:70`).

Citation key: `SPEC:N` = `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md:N`; `CAPS:N` = `.dev/orca-command-refactor/inventory/orca-capabilities.md:N`; `[G] N` = line N of `orca-ide skills get orchestration` (1.4.237).

## Why a third option
Option (a) leaves one failure open: a brief without the flag makes a command prompt, and the worker stalls with no `worker_done` while Orca reports it "healthy, not failed" (`SPEC:47`; `CAPS:52`, `CAPS:129`). Option (b) closes that hole by putting Orca detection into commands, which breaks SA-2 and non-goal 1 (`SPEC:170`, `SPEC:314`) and, on the environment route, misfires on non-worker Orca terminals (observed 2026-11-02: this session has `ORCA_TERMINAL_HANDLE` set but is not among the 11 workers `orca-ide orchestration worker-list --json` lists). Option (c) closes the hole where detection is already authoritative and already Orca-aware: the worker session. Orca itself tells that session it is a worker through the preamble (`[G]` lines 38, 78-82), and the spec already gives the worker session Orca duties (WC-3, WC-5, WC-7, WC-12 at `SPEC:67-76`).

## Safety
- Same as (a) for people: no command reads the environment or the conversation, so a person's tab cannot change behaviour (SA-1, `SPEC:169`).
- A wrong brief fails fast and visibly instead of stalling: the failure is a `worker_done --outcome failed` with a reason, which is the only failure signal Orca guarantees (`CAPS:73`, "Never encode failure only in prose").
- It also stops a coordinator-only command (for example `/sc:git` or `/sc:pm`) being run by a worker, which today only section 4's prose forbids (`SPEC:151`).

## Reliability
- Deterministic: a string check on the brief's command line, decided before anything runs. Testable live with one extra 7.2 run whose brief omits the flag (pass: `worker_done --outcome failed`, no contract written, no `agentWait`).
- The worker rule is prose read by a model, like every WC row; it is one rule in one file (`WORKER-CONTRACT.md`, `SPEC:58`), not 35 command edits.

## How a person works day to day
- No change for people. Coordinators get an immediate, named failure for a forgotten flag instead of a stall they must diagnose with `worker-read` (`SPEC:238`).

## Implementation cost
- One sentence in the worker-session part of `WORKER-CONTRACT.md` plus one live check in P0 or P1. Every command-side cost and benefit of (a) is unchanged. Removing the guard later is a one-line change.
