# D1 option (a): an explicit `--unattended` flag the coordinator writes into every brief

Position: a command switches to unattended behaviour only when its command line carries the standalone token `--unattended`. Nothing in the environment, the conversation or Orca turns it on. This is the spec's current recommendation (`SPEC:328-331`).

Citation key: `SPEC:N` = `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md:N`; `CAPS:N` = `.dev/orca-command-refactor/inventory/orca-capabilities.md:N`.

## Safety
- It cannot switch a person's run. A person never types the flag (`SPEC:329`), and only a standalone token outside any quoted argument counts, so `/sc:troubleshoot "the worker ignores --unattended"` stays a person's run (`SPEC:55`, checked live by AC-2.8 at `SPEC:269`).
- Detection would misfire, and that is now observed rather than hypothetical. In this session on 2026-11-02, `env` shows `ORCA_TERMINAL_HANDLE` set, yet `orca-ide orchestration worker-list --json` lists 11 workers whose `agentTerminalHandle` values do not include this session's handle: the variable is set in an Orca terminal that is not a dispatched worker. The spec left exactly this open as UNVERIFIED item 13 (`SPEC:395`) and said that if it is set in a person's tab, "prompts would vanish for a person working in Orca, breaking SA-1" (`SPEC:330`). An explicit flag is immune to it.
- The flag also turns outward defaults off (WC-9, `SPEC:73`), so a person can never lose auggie-review's posting default (`SPEC:169`) by working inside Orca.

## Reliability
- Deterministic and checkable by text: the brief is plain text the coordinator writes, and AC-1.1 asserts per phase which commands carry an `## Unattended mode` section (`SPEC:257`). The live 7.2 checks then show the flag's effect (`SPEC:234-246`).
- Caller-neutral: the switch names the condition (no person), not a tool, so `claude -p`, CI or a future orchestrator can use it with no Orca present (`SPEC:54`, Decisions row at `SPEC:361`; SA-2 at `SPEC:170`).
- Phase-gated: a command accepts the flag only once its gates are converted (`SPEC:187-195`), so the flag never promises behaviour the command does not have.

## How a person works day to day
- Nothing changes for a person (SA-1, `SPEC:169`). The coordinator copies the command line from the brief template in `WORKER-CONTRACT.md` (`SPEC:58`, `SPEC:79`).
- Known weakness: if a coordinator forgets the flag, the command prompts and the worker stalls with no `worker_done`, which Orca reports as healthy (`SPEC:47`; `CAPS:52`). The brief template and the 7.2 step-3 stall proof (`SPEC:238`) catch it, but only after the fact.

## Implementation cost
- One shared parse rule and one person-mode refusal list, written once in the contract file (`SPEC:55-58`), plus a short `## Unattended mode` section per command (`SPEC:58`). Commands are prompts, so the "parse" is applied by the model reading the rule, not by code; the quoted-argument rule exists for that reason (`SPEC:55`).
- Changing later is cheap: if detection ever becomes reliable, it can be added as an extra trigger without removing the flag.
