# Findings to adjudicate

### X1

- anchor: "It has worked before: in the codegraph planning run"
- anchor2: "The only end-to-end proof is the PR #329 run"
- refs: P3
- claim: The direct route is cited as proven in E3 and unproven in section 1.4, and the spec does not say whether the P3 run and the PR #329 run are the same.

### X2

- anchor: "After `worker_done`, the coordinator opens the report file, then releases or reuses the worker"
- refs: -
- claim: The coordinator's next step after partial and blocked is undefined, including who answers a blocked_question and whether partial may start dependents.

### X3

- anchor: "make `--remediate` follow the existing headless auto-accept rule"
- anchor2: "Stage 10.5 passes `--unattended` to each reflect so the headless rule applies"
- refs: SA-6, WC-9
- claim: Under --unattended, reflect accepts its own remediation offer, and WC-9 does not cover self-accepted remediation, so the authority rule that D2 states for implement is absent for reflect.

### X4

- anchor: "Independent citation check: a fresh `evidence-validator` agent"
- refs: -
- claim: The claimed evidence-validator pass is not reproducible from the workspace; noted without action.

### X5

- anchor: "Only defects that stop a command working as a worker are in scope"
- anchor2: "move the frontmatter out of its code block"
- refs: -
- claim: The same frontmatter defect is out of scope for agent under 8.8 and in scope for business-panel under 3.2, with the need still UNVERIFIED.

### X6

- anchor: "What changes in the commands is limited to the worker contract in section 2"
- refs: SA-4
- claim: The scope sentence in 1.1 omits the defect fixes in section 3 that SA-4 names.

### X7

- anchor: "no pr-submit changes in Phase 4"
- anchor2: "keep the inventories' 10 / 27 / 6 split"
- refs: P4
- claim: The recommended D3 makes pr-submit coordinator-only, but the 10/27/6 split and the phase plan still count and schedule pr-submit as a worker.

### X8

- anchor: "`target_release` required as a flag for TDD inputs, else blocked"
- refs: -
- claim: The spec-panel row asks for --output and a new contract, but the supplied command definition already has both, under --report-dir, so the row and INV-B:182 are stale or the repo copy differs.

### X9

- anchor: "It has worked before: in the codegraph planning run"
- refs: WC-7
- claim: E3 presents a precedent that used the Agent-tool route WC-7 forbids as support for the direct route, with the caveat only in section 1.4.

### X10

- anchor: "contract for both pipelines (today a chat table)"
- anchor2: "`run` requires `--suite` and the safety flags in the brief, else blocked"
- refs: 2.3, WC-11, WC-4, WC-6
- claim: Several 3.2 commands have no output flag or fixed location, so the contract path is not known before dispatch and cli-eval's fresh-directory rule cannot hold.

### X11

- anchor: "These run as workers now if the brief uses the stated flags"
- anchor2: "the topic-only clarification and nested"
- refs: 3.1, SA-2, WC-2
- claim: Ready-today commands can still stop on /task questions that only the unattended mode resolves, so they are not ready as the heading states.

### X12

- anchor: "every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml`"
- anchor2: "use it as a step inside another worker's brief, not as its own Task"
- refs: 2.2, 2.3, AC-0.4, AC-1.1, AC-1.2, AC-1.4, P0, P1, P2, WC-2, WC-4, WC-5, WC-6, WC-7
- claim: AC-1.1 and AC-1.2 require an unattended section and a contract file for every 3.1-3.2 command, while the load row says it writes no report and is not its own Task, so the P1 check cannot pass.

### X13

- anchor: "Phase 1 needs a pre-confirmed context input in the brief"
- anchor2: "add a resume input, or fresh run"
- refs: AC-2.2
- claim: The review-translation gate needs an input that the command does not define, and the cli-eval flags assumed by AC-2.2 are not shown to exist.

### X14

- anchor: "a precise component prompt, not a bare topic"
- refs: -
- claim: tdd and release-split are called ready, but nested /task and tasklist-input prompts stay outside the brief's control.

### X15

- anchor: "dispatch only inside an IronClaude checkout (hardcoded template path)"
- refs: P2
- claim: cli-portify keeps a src/superclaude lookup that the repo rule forbids for installed primitives, and P2 edits that file without fixing it.

### X16

- anchor: "installed to `~/.claude/WORKER-CONTRACT.md`"
- refs: -
- claim: Every Unattended section depends on an installed contract file with no fallback, so a missing file leaves the rules undefined.

### X17

- anchor: "(orchestration\\|worktree\\|terminal\\|agent)"
- anchor2: "The only allowed mention of Orca in a changed command is as an example"
- refs: P0, SA-2, WC-8
- claim: The AC-C1 pattern uses an escaped pipe that grep -E reads as a literal, so it can pass after an Orca call is added, and it scans core files that SA-2 allows to mention Orca.

### X18

- anchor: "then one `/sc:adversarial` worker on their reports"
- refs: -
- claim: A fan-in consumer wired to a subset of N reports has no defined behaviour, so it can receive N-k reports where it expects N.

### X19

- anchor: "file location unnamed"
- refs: AC-1.1
- claim: AC-1.1 requires each Unattended section to name return-contract.yaml, but the cli-portify row does not give the location.

### X20

- anchor: "installed to `~/.claude/WORKER-CONTRACT.md`"
- anchor2: "proposed as `src/superclaude/core/WORKER-CONTRACT.md`"
- refs: 2.1, AC-1.2
- claim: The live checks need the installed contract file, but the spec does not require superclaude install before them, so they fail in a bare dev checkout.

### X21

- anchor: "`observation.agentWait` is never non-null"
- anchor2: "Pass:** `observation.agentWait` is never non-null"
- refs: -
- claim: The step 2 pass condition is met when the coordinator never looks at agentWait, because an absent field passes.

### X22

- anchor: "installed to `~/.claude/WORKER-CONTRACT.md`"
- anchor2: "'WORKER-CONTRACT.md' in KNOWN_CORE_FILES"
- refs: AC-0.1
- claim: No check confirms that an installed command can read the installed contract file.

### X23

- anchor: "Two workers in one worktree must never write the same file"
- anchor2: "`PROJECT_INDEX.md` (location implied)"
- refs: 2.1, AC-2.2, P1, SA-1, SA-3, SA-4, WC-1, WC-10, WC-11, WC-12, WC-2, WC-3, WC-7
- claim: Two index-repo workers in the default shared worktree both write PROJECT_INDEX.md, so one run's output is overwritten, which WC-11 forbids, while the row still lists index-repo as ready with no constraint.
