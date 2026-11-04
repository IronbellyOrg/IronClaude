# D1 option (b): the command detects that it runs as an Orca worker

Position: a command switches to unattended behaviour by itself when it sees it is an Orca worker, either through `ORCA_TERMINAL_HANDLE` or through the worker preamble with Task and Dispatch IDs in the conversation (`SPEC:330`). No flag in the brief is needed.

Citation key: `SPEC:N` = `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md:N`; `CAPS:N` = `.dev/orca-command-refactor/inventory/orca-capabilities.md:N`; `[G] N` = line N of `orca-ide skills get orchestration` (1.4.237).

## Strongest case for it
- **Orca itself defines a worker by the preamble.** Its role table says a session whose "current prompt contains a live injected preamble with Task and Dispatch IDs" is a "Dispatched worker", and a session with "No live preamble" is an "Ordinary terminal agent" (`[G]` lines 38, 41; `CAPS:148`). Preamble detection uses Orca's own rule, not a guess.
- **A coordinator cannot forget it.** Under (a), a brief without `--unattended` makes the command prompt, and the worker stalls silently: Orca reports a waiting worker as "healthy, not failed" (`CAPS:52`, `CAPS:129`; `SPEC:47`). Detection removes that whole failure class.
- **Shorter briefs and no new flag on 35 commands** (`SPEC:189-195`).

## Safety
- Environment detection is unsafe, and that is now observed. On 2026-11-02 this session has `ORCA_TERMINAL_HANDLE` set, but its handle is not among the 11 `agentTerminalHandle` values `orca-ide orchestration worker-list --json` reports. The variable is therefore set in an Orca terminal that is not a dispatched worker, which is the case the spec flagged (`SPEC:330`, UNVERIFIED item 13 at `SPEC:395`). A person running `/sc:cleanup --interactive` in their own Orca tab would lose its approval prompts and outward defaults, breaking SA-1 (`SPEC:169`).
- Preamble detection is safer for people (a person's own session has no preamble, `[G]` line 41), but it relies on the model noticing prose in its context, and the worker preamble arrives on the same command line as the task (`CAPS:47`), so the two are hard to tell apart in a test.

## Reliability
- Not mechanically testable: there is no token to grep, and a wrong guess by the model is invisible until a run stalls or a prompt disappears (`SPEC:330`).
- It ties every command to Orca: the spec's non-goal 1 forbids "Orca-specific branching" in commands (`SPEC:314`) and SA-2 keeps commands Orca-free because they run in other projects (`SPEC:170`; `CLAUDE.md:74`). It also does nothing for other callers with no person (`claude -p`, CI), which (a) covers.
- The repo's one precedent detects headlessness from `claude --print` with no TTY (`src/superclaude/skills/sc-reflect-protocol/refs/remediation-handoff.md:239-242`), but Orca launches Claude interactively with the task on the command line (`CAPS:47`), so that signal would not fire for a worker (`SPEC:391`).

## How a person works day to day
- No flag to remember for coordinators. For people, the risk is a silent loss of prompts in Orca tabs if the environment route is used.

## Implementation cost
- Low per brief, higher per command: each command needs detection text that names Orca, and AC-C1's grep (`SPEC:205-212`) would need an exception. Undoing it later means touching every command again.
