<!-- Provenance: This document was produced by /sc:adversarial -->
<!-- Base: Variant A (original, option-a.md) -->
<!-- Merge date: 2026-11-05T19:46:13+00:00 -->

<!-- Source: Base (original) -->
# D1 option (a): an explicit `--unattended` flag the coordinator writes into every brief

Position: a command switches to unattended behaviour only when its command line carries the standalone token `--unattended`. Nothing in the environment, the conversation or Orca turns it on. This is the spec's current recommendation (`SPEC:328-331`).

<!-- Source: Base (original, modified) — Change #6 per debate findings -->
Citation key: `SPEC:N` = line N of `.dev/orca-command-refactor/specs/history/spec-v4-after-round3.md` (the version before the decision); the current `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` records this decision at line 401 as "Option (c): `--unattended` is the only switch; from P1 the worker session also applies the brief guard. Commands never detect Orca."; `CAPS:N` = `.dev/orca-command-refactor/inventory/orca-capabilities.md:N`.

<!-- Source: Base (original) -->
## Safety
- It cannot switch a person's run. A person never types the flag (`SPEC:329`), and only a standalone token outside any quoted argument counts, so `/sc:troubleshoot "the worker ignores --unattended"` stays a person's run (`SPEC:55`, checked live by AC-2.8 at `SPEC:269`).
<!-- Source: Base (original, modified) — Change #1: limit the misfire claim to environment-variable detection and mark the observation unverified -->
- Environment-variable detection would misfire. This was observed in the session of 2026-11-02 and cannot be verified from the repository files: `env` showed `ORCA_TERMINAL_HANDLE` set, yet `orca-ide orchestration worker-list --json` listed 11 workers whose `agentTerminalHandle` values did not include that session's handle, so the variable was set in an Orca terminal that is not a dispatched worker. `worker-list` omits remote workers unless `--include-remote` is passed (`CAPS:127-128`). The spec left exactly this open as UNVERIFIED item 13 (`SPEC:395`) and said that if it is set in a person's tab, "prompts would vanish for a person working in Orca, breaking SA-1" (`SPEC:330`). An explicit flag is immune to it. The observation concerns the environment variable only; it does not show a preamble-based route misfiring.
<!-- Source: Base (original) -->
- The flag also turns outward defaults off (WC-9, `SPEC:73`), so a person can never lose auggie-review's posting default (`SPEC:169`) by working inside Orca.

<!-- Source: Base (original) -->
## Reliability
- Deterministic and checkable by text: the brief is plain text the coordinator writes, and AC-1.1 asserts per phase which commands carry an `## Unattended mode` section (`SPEC:257`). The live 7.2 checks then show the flag's effect (`SPEC:234-246`).
- Caller-neutral: the switch names the condition (no person), not a tool, so `claude -p`, CI or a future orchestrator can use it with no Orca present (`SPEC:54`, Decisions row at `SPEC:361`; SA-2 at `SPEC:170`).
<!-- Source: Variant B (option-b.md), Section "Strongest case for it" — merged per Change #2 -->
- Orca's own worker signal has a place, but not inside a command: Orca itself defines a worker by a live preamble with Task and Dispatch IDs (`CAPS:148`). That signal is used only in the worker session, as a refuse-only brief guard from P1, never inside a command; commands never detect Orca (current spec, line 401).
<!-- Source: Variant B (option-b.md), Section "Reliability" — merged per Change #5 -->
- No command-side headless signal exists for Orca workers. The one existing command-side headless signal (reflect: `claude --print` with no TTY; `src/superclaude/skills/sc-reflect-protocol/refs/remediation-handoff.md`, section "Headless auto-accept under `--print` (FR-9)") does not apply, because Orca launches Claude interactively with the task on the command line (`CAPS:47`). That this signal would not fire for an Orca worker is ASSUMED, not verified (spec item 9, `spec-v4-after-round3.md` line 391). UNVERIFIED.
<!-- Source: Base (original) -->
- Phase-gated: a command accepts the flag only once its gates are converted (`SPEC:187-195`), so the flag never promises behaviour the command does not have.

<!-- Source: Base (original) -->
## How a person works day to day
- Nothing changes for a person (SA-1, `SPEC:169`). The coordinator copies the command line from the brief template in `WORKER-CONTRACT.md` (`SPEC:58`, `SPEC:79`).
<!-- Source: Base (original, modified) — Change #3: known weakness stated with its pre-run guard and residual risk -->
- Known weakness: if a coordinator forgets the flag, the command prompts and the worker stalls with no `worker_done`, which Orca reports as healthy (`SPEC:47`; `CAPS:52`). The brief guard now refuses such a brief before any work: with a live preamble and every command copy carrying an `## Unattended mode` section, a line without the flag is refused (`WORKER-CONTRACT.md`, Brief guard, case 1). The brief template and the 7.2 step-3 stall proof (`SPEC:238`) remain as later catches. Residual risk: the guard depends on the model recognizing the preamble and reading every command copy.

<!-- Source: Base (original) -->
## Implementation cost
- One shared parse rule and one person-mode refusal list, written once in the contract file (`SPEC:55-58`), plus a short `## Unattended mode` section per command (`SPEC:58`). Commands are prompts, so the "parse" is applied by the model reading the rule, not by code; the quoted-argument rule exists for that reason (`SPEC:55`).
<!-- Source: Base (original, modified) — Change #4 per debate findings -->
- Changing later is cheap: any later detection belongs in the worker session as a refuse-only guard, as the brief guard is, never as a trigger inside commands.
