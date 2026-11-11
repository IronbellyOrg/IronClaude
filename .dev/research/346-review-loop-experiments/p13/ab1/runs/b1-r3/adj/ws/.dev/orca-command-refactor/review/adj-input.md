# Findings to adjudicate

### X1

- anchor: "What changes in the commands is limited to the worker contract in section 2"
- refs: 1.1, SA-4
- claim: Section 1.1 says changes are limited to the contract, but section 3 and SA-4 include other defect fixes.

### X2

- anchor: "make `--remediate` follow the existing headless auto-accept rule"
- anchor2: "the rule exists to stop an agent approving its own work"
- refs: WC-9
- claim: Unattended reflect auto-accepts remediation, which is the self-approval that D2 forbids for implement; the bounded risk needs a decision.

### X3

- anchor: "Under `--unattended`, the `--depth deep` short-input STOP and the `--fix` offer resolve as blocked (P2)"
- anchor2: "These run as workers now if the brief uses the stated flags"
- refs: P2
- claim: The troubleshoot brief rule allows a --depth deep short-input STOP that asks a person, so a stated brief can stall without worker_done.

### X4

- anchor: "prints nothing (SA-2, WC-8)"
- anchor2: "add an Orca section to `HOW-WE-WORK.md` and its two mirrored copies"
- refs: 5, P0, SA-2, WC-8
- claim: AC-C1 scans core files that Phase 0 must fill with Orca text, and its escaped pipes make the grep pattern match nothing when copied.

### X5

- anchor: "the `--unattended` flag accepted by every command in sections 3.1 and 3.2 (a no-op where a command has no gate)"
- anchor2: "every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml`"
- refs: 1.4, 2.3, 3.1, 6, 7.3, AC-0.4, AC-1.1, AC-1.4, AC-2.2, AC-3.2, AC-4.2, P0, P1, SA-1, WC-1, WC-10, WC-11, WC-2, WC-3, WC-4, WC-5, WC-6, WC-7, WC-9
- claim: P1 scope and AC-1.1 require the flag, section and contract in all 37 commands while the phase column and P1 command list give P1 only 13, so AC-1.1 cannot pass or P1 pre-empts the D2-D4 decisions.

### X6

- anchor: "Agent-tool subagents inside a worker are not Orca workers and are not counted by Orca's nesting limit"
- refs: -
- claim: The depth fence covers Orca dispatch; CAPS:155 leaves whether Orca limits subagents UNVERIFIED, so E4 states more than its source.

### X7

- anchor: "points to the installed contract path, so the shared rules are written once"
- refs: 2.1, SA-4
- claim: A command run against an install without WORKER-CONTRACT.md has no specified behaviour.

### X8

- anchor: "claude -p \"/sc:analyze src/superclaude/cli/install_core.py\""
- refs: AC-1.3, SA-6
- claim: AC-1.3 calls a print-mode run a plain session, so it does not test an interactive person's session.

### X9

- anchor: "Fan-out that needs Orca records is split into separate Tasks by the coordinator."
- refs: WC-8
- claim: Heavy in-command fan-out such as cleanup-audit and tdd cannot be split by the coordinator, and no rule covers that case.

### X10

- anchor: "`run` requires `--suite` and the safety flags in the brief, else blocked"
- anchor2: "posting returns only with an explicit `--post-pr` in the brief"
- refs: -
- claim: The --suite and --post-pr flags are not shown to exist in the inventories, and the no-command-calls-Orca premise and the 43-command scope need a re-check.

### X11

- anchor: "posting returns only with an explicit `--post-pr` in the brief (WC-9)"
- anchor2: "`--unattended` implies `--no-post-pr` and `--no-remediation-offer`"
- refs: WC-9
- claim: The row requires an explicit --post-pr flag that is not evidenced, while its required-change column says none.

### X12

- anchor: "How `plugins/superclaude/commands/` (which holds copies such as `agent.md`"
- anchor2: "`make verify-sync` | exits 0 (SA-5)"
- refs: SA-5
- claim: The plugin mirror is not assigned to any phase and no check compares it, so it can drift while verify-sync passes.

### X13

- anchor: "Apply the answers to D2-D4: the implement halt path, post-release pre-authorization, pr-submit as a worker."
- refs: P4
- claim: P4 includes pr-submit although D3 (a) recommends no pr-submit change.

### X14

- anchor: "the topic-only clarification and nested `/task`"
- refs: 122, WC-2
- claim: No row edits the task skill and no rule says how --unattended reaches nested skills, so tdd keeps its nested ask lines.

### X15

- anchor: "cannot misfire on a person"
- refs: SA-1
- claim: A brief that a person pastes with --unattended silences that person's prompts, so the flag is not a safe sentinel.

### X16

- anchor: "After `worker_done`, the coordinator opens the report file, then releases or reuses the worker"
- anchor2: "A partial run left a usable deliverable; `failed` would tell the coordinator the work is lost."
- refs: 2.3
- claim: No rule for blocked re-dispatch or for dependents of a partial Task, which Orca settles as complete.

### X17

- anchor: "A phase passes only when every check in its block and every common check passes."
- refs: SA-1, WC-1, WC-10, WC-11, WC-12, WC-3, WC-6
- claim: WC-1, WC-3, WC-6 and WC-12 have no acceptance check, and WC-10, WC-11 and SA-1 are checked for one or two commands only.

### X18

- anchor: "ORCA orchestration check --wait --types \"worker_done,escalation,question\" --timeout-ms 900000 --json"
- anchor2: "at least once per 5 minutes"
- refs: -
- claim: Following step 3 with its 900000 ms timeout leaves 15 minutes between worker-show observations, which step 2 forbids.

### X19

- anchor: "A command's own `AskUserQuestion` or chat question comes *after* readiness, so it does not fail `worker-start`"
- refs: -
- claim: The claim is asserted although the task is passed as a startup argument, and it is missing from the UNVERIFIED list.

### X20

- anchor: "It is testable by grep and cannot misfire on a person."
- anchor2: "Explicit `--unattended` flag in the brief (recommended)"
- refs: 2.1
- claim: The sentinel token inside quoted prompt text is not excluded, so the cannot-misfire claim is unsupported.

### X21

- anchor: "These six are never dispatched as workers and get no `--unattended` mode."
- refs: WC-2
- claim: The spec does not say what a coordinator-only command does when given --unattended, so it may wait on a person.

### X22

- anchor: "must be split into waits of at most 4 minutes so the session can heartbeat between them"
- anchor2: "no single tool call exceeds 240 s"
- refs: AC-4.3, WC-10
- claim: A 270 s call obeys WC-10 and fails AC-4.3.
