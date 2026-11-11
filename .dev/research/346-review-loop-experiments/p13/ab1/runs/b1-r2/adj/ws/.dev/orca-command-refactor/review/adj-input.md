# Findings to adjudicate

### X1

- anchor: "Orca keeps those records only for workers the coordinator starts"
- refs: -
- claim: CAPS:158 is the provenance rule, which only partly supports the claim it is cited for.

### X2

- anchor: "written only in unattended mode or when the caller passes the new output flag"
- refs: AC-1.3, SA-3
- claim: SA-3 depends on a new output flag that the spec never defines, so it is unclear whether a standalone --output run writes the contract.

### X3

- anchor: "Default output paths carry a timestamp or the slug the coordinator passes"
- anchor2: "`PROJECT_INDEX.md` (location implied)"
- refs: WC-11
- claim: WC-11 forbids two workers writing one file, but index-repo and init-lite keep fixed default output paths and stay ready with no brief flags.

### X4

- anchor: "prompt is replaced by the explicit resume flag (resume only when passed)"
- refs: SA-1
- claim: It is unclear whether the roadmap prompt change applies only under --unattended, which SA-1 requires.

### X5

- anchor: "The worker runs `check` at natural checkpoints and once before `worker_done`"
- refs: WC-12
- claim: Ordinary follow-ups have no stated handling.

### X6

- anchor: "installed to `~/.claude/WORKER-CONTRACT.md`"
- refs: WC-2
- claim: Commands point to an installed file that may be absent after a partial or older install, and no fallback is stated.

### X7

- anchor: "`run` requires `--suite` and the safety flags in the brief, else blocked"
- refs: AC-2.2
- claim: The safety flags are never named, so an implementer must guess which flags make the run non-blocked.

### X8

- anchor: "make `--remediate` follow the existing headless auto-accept rule"
- anchor2: "`--unattended` reuses it and does not replace it"
- refs: SA-6, WC-9
- claim: It is unstated whether --unattended triggers reflect's headless auto-accept, which runs remediation that can change code.

### X9

- anchor: "`gh api repos/IronbellyOrg/IronClaude/pulls/<PR>/reviews --jq length`"
- refs: AC-2.4
- claim: The count covers one page only, so an added comment on a PR with 30 or more can leave it unchanged.

### X10

- anchor: "It turns on only through the command's own explicit flag written in the brief."
- refs: P2, P4, WC-9
- claim: task commit/push, post-release and pr-submit have no named explicit flag, and the auggie-review and task authorizations sit in P2 while the spec gates only P4 on D2-D4.

### X11

- anchor: "dispatch only inside an IronClaude checkout (hardcoded template path)"
- refs: P2
- claim: The hardcoded src/superclaude template path is flagged but unscheduled, and no AC checks for such paths.

### X12

- anchor: "the smoke runs test the decision before anything is built on it"
- anchor2: "Write `src/superclaude/core/WORKER-CONTRACT.md`"
- refs: AC-0.3, P0
- claim: P0 builds the contract and routing-guide edits before the smoke runs that test the decision, so a failed test leaves the edits behind.

### X13

- anchor: "must be split into waits of at most 4 minutes"
- anchor2: "no single tool call exceeds 240 s"
- refs: AC-4.3, WC-10
- claim: WC-10 splits only calls longer than 5 minutes, but AC-4.3 forbids any call over 240 s, so a 4.5-minute call passes one and fails the other.

### X14

- anchor: "the 600 s default is a cumulative per-wait budget"
- refs: AC-4.3, P2, WC-10
- claim: The pr-submit wait check is unverifiable until the poll runtime is measured, and P2 has no check for it.

### X15

- anchor: "`observation.agentWait` is never non-null"
- refs: -
- claim: The step 2 pass also holds when the field is absent, which means Orca never looked, so a stalled worker can pass.

### X16

- anchor: "--unattended --output .dev/troubleshoot/login/"
- refs: -
- claim: The D1 example passes --output to /sc:troubleshoot, which no section 3 row names as a flag.

### X17

- anchor: "A phase passes only when every check in its block and every common check passes."
- refs: WC-1, WC-10, WC-12, WC-3, WC-6
- claim: WC-1, WC-3, WC-6 and WC-12 have no acceptance check, and WC-10 is checked for pr-submit only.

### X18

- anchor: "stays a worker candidate only if the user accepts open decision D3"
- anchor2: "**Coordinator or person only (recommended).**"
- refs: -
- claim: pr-submit is counted as a worker candidate although D3 recommends coordinator-only, so the 10/27/6 counts depend on an open decision.

### X19

- anchor: "prints nothing (SA-2, WC-8)"
- anchor2: "The only allowed mention of Orca in a changed command is as an example of a caller's question channel inside the contract file."
- refs: P0, SA-2, SA-5, WC-8
- claim: AC-C1 greps src/superclaude/core, where the P0 contract file and routing-guide Orca section may legitimately name orca commands.

### X20

- anchor: "Agent-tool subagents inside a worker are not Orca workers and are not counted by Orca's nesting limit."
- anchor2: "has no proven limit, but no proof of none either"
- refs: -
- claim: E4 states as established a fact that CAPS:155 marks UNVERIFIED and section 1.4 concedes.

### X21

- anchor: "prints nothing: edits are additive"
- refs: SA-4
- claim: Adding a flag to an existing Usage line shows as a deleted line, so AC-C5 can fail on a purely additive change.

### X22

- anchor: "every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml`"
- anchor2: "use it as a step inside another worker's brief, not as its own Task"
- refs: 2.3, 3.1, 3.2, 4, 7.2, AC-0.4, AC-1.1, AC-1.4, AC-2.2, AC-2.3, P0, P1, P2, P4, SA-1, WC-2, WC-3, WC-4, WC-5, WC-6, WC-7
- claim: AC-1.1 requires a contract-naming Unattended mode section on load (which writes no contract) and on implement, post-release and pr-submit (which the spec holds for P4 or the coordinator), so the P1 check cannot pass as written.

### X23

- anchor: "then one `/sc:adversarial` worker on their reports"
- refs: 1.3
- claim: The join step is unspecified when blocked or failed workers leave fewer reports than workers, down to below the 2-artifact minimum of /sc:adversarial.

### X24

- anchor: "one worker (a top-level Claude session in its own Orca terminal) runs one command"
- refs: 1.1, 3, AC-3.1, AC-3.3, SA-4, WC-7
- claim: The spec does not say how a session whose first message is a preamble starts a slash command.

### X25

- anchor: "Launch setup, not commands"
- refs: WC-1
- claim: WC-1 has an owner outside every phase and no AC checks readiness.

### X26

- anchor: "How `plugins/superclaude/commands/` (which holds copies such as"
- refs: -
- claim: Command edits can leave the plugins mirror out of step, and no AC checks the mirror.

### X27

- anchor: "A command's own `AskUserQuestion` or chat question comes *after* readiness, so it does not fail `worker-start`"
- refs: 1.4, WC-1
- claim: The sandbox evidence does not show that a first-action question cannot block readiness when Claude receives its task on the command line.

### X28

- anchor: "its reflect fan-out runs one layer below the worker, inside Claude Code's nesting limit"
- refs: -
- claim: The nesting-limit claim rests on an external doc quote and is stated as fact, while INV-B:210 and INV-B:314 mark subagent-to-agent spawning as UNVERIFIED.

### X29

- anchor: "the behaviour a command switches to when its caller passes `--unattended`"
- refs: SA-1
- claim: The text does not say that a quoted argument containing the text --unattended is not the switch.
