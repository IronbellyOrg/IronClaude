review: 1 of 3
# Merged review 1 (coordinator script; panel of 4 reviewers)
candidate: /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p13/ab1/runs/b1-r6/ws/.dev/orca-command-refactor/specs/orca-worker-contract-spec.md sha256 d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d
reviewers:
- t1b-1: report /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p13/ab1/runs/b1-r6/ws/.dev/orca-command-refactor/review/round1-t1b-1.md, block ok true
- t2-1: report /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p13/ab1/runs/b1-r6/ws/.dev/orca-command-refactor/review/round1-t2-1.md, block ok true
- t3-1: report /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p13/ab1/runs/b1-r6/ws/.dev/orca-command-refactor/review/round1-t3-1.md, block ok true
- t3-2: report /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p13/ab1/runs/b1-r6/ws/.dev/orca-command-refactor/review/round1-t3-2.md, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | yes | overlap | CRITICAL | 2.2, 2.3, AC-0.4, AC-1.1, AC-1.2, AC-1.4, P0, P1, P2, WC-2, WC-4, WC-5, WC-6, WC-7 | t1b-1, t2-1, t3-1, t3-2 |
| L2 | open | yes | overlap | MAJOR | 2.1, AC-2.2, P1, SA-1, SA-3, SA-4, WC-1, WC-10, WC-11, WC-12, WC-2, WC-3, WC-7 | t2-1, t3-1, t3-2 |
| L3 | open | no | overlap | MAJOR | - | t2-1, t3-2 |
| L4 | open | no | single | MAJOR | SA-6, WC-9 | t2-1 |
| L5 | open | no | single | MAJOR | P4 | t2-1 |
| L6 | open | no | overlap | MAJOR | AC-2.2 | t2-1, t3-1 |
| L7 | open | no | single | MINOR | - | t2-1 |
| L8 | open | no | overlap | MAJOR | - | t2-1, t3-2 |
| L9 | open | no | single | MINOR | WC-7 | t2-1 |
| L10 | open | no | single | MINOR | AC-1.1 | t2-1 |
| L11 | open | no | single | MAJOR | 3.1, SA-2, WC-2 | t3-1 |
| L12 | open | no | single | MAJOR | 2.3, WC-11, WC-4, WC-6 | t3-1 |
| L13 | open | yes | overlap | MAJOR | P0, SA-2, WC-8 | t3-1, t3-2 |
| L14 | open | no | single | MINOR | 2.1, AC-1.2 | t3-1 |
| L15 | open | no | overlap | MAJOR | - | t3-1, t3-2 |
| L16 | open | no | single | MAJOR | P3 | t3-2 |
| L17 | open | no | single | MAJOR | SA-4 | t3-2 |
| L18 | open | no | single | MAJOR | - | t3-2 |
| L19 | open | no | single | MAJOR | - | t3-2 |
| L20 | open | no | single | MAJOR | - | t3-2 |
| L21 | open | no | single | MAJOR | P2 | t3-2 |
| L22 | open | no | single | MINOR | AC-0.1 | t3-2 |
| L23 | open | no | single | MINOR | - | t3-2 |

## Blocking findings

### L1

#### L1.t1b-1 (F1)

- claim: AC-1.1 and AC-1.2 require an unattended section and a contract file for every 3.1-3.2 command, while the load row says it writes no report and is not its own Task, so the P1 check cannot pass.
- anchor: "every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml`"
- anchor2: "use it as a step inside another worker's brief, not as its own Task"

#### L1.t1b-1 (F2)

- claim: WC-4 puts the contract at a coordinator-passed directory known before dispatch, but workflow writes it under a generated id path, adversarial in a subdirectory, and tdd/init-lite take a file for --output, so an implementer following WC-4 builds a wrong or unknowable path.
- anchor: "where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`)"
- anchor2: "`.dev/tasks/to-do/<id>/return-contract.yaml`"

#### L1.t1b-1 (F3)

- claim: AC-0.4 requires 7.2 step 3 to pass in P0, but step 3 needs the WC-4 contract path and --unattended, neither of which exists until P1, so the P0 smoke check cannot pass.
- anchor: "steps 1-3 and 5-7 pass; step 4 uses the command's existing report file, since the contract arrives in P1"
- anchor2: "its report path is the WC-4 contract path"

#### L1.t2-1 (F3)

- claim: A partial report becomes a succeeded Task that releases dependents with no status check required, and unknown status values are not mapped.
- anchor: "`--outcome succeeded` otherwise, including `partial`"

#### L1.t2-1 (F5)

- claim: The adversarial row places its contract in an adversarial subfolder while WC-4 places it at the output directory root, and the spec does not say which output directory applies.
- anchor: "Fix the contract filename to `<output>/adversarial/return-contract.yaml`"
- anchor2: "In unattended mode the command writes `<output-dir>/return-contract.yaml`"

#### L1.t2-1 (F12)

- claim: AC-0.4 says the top-level property is verified in step 5, but step 5 only searches for AskUserQuestion, so the Agent-tool wrapping that WC-7 forbids has no check.
- anchor: "no Agent-tool wrapper, verified in the step-5 transcript"
- anchor2: "search the transcript for `AskUserQuestion`"

#### L1.t2-1 (F17)

- claim: A blocked gate is reported as failed, but Orca's breaker does not count a worker's own failed report, so a coordinator can re-dispatch a blocked command without limit.
- anchor: "`--outcome failed` when the report says `failed` or `blocked`"
- anchor2: "A retry worker (`worker-start --retry-of`) must not corrupt the first attempt's output"

#### L1.t2-1 (F23)

- claim: A retry needs a fresh output directory and so a new contract path, which the spec does not tell the coordinator to read.
- anchor: "A retry worker (`worker-start --retry-of`) must not corrupt the first attempt's output"

#### L1.t2-1 (F26)

- claim: WC-4 requires a contract for stops before output exists, but a contract needs an output directory, and a brief without one gets no file.
- anchor: "including stops before any other output exists"

#### L1.t3-1 (F1)

- claim: AC-0.4 requires step 3 to match a WC-4 contract path that troubleshoot does not write until P1, so the criterion cannot pass in P0.
- anchor: "steps 1-3 and 5-7 pass; step 4 uses the command's existing report file"
- anchor2: "its report path is the WC-4 contract path"

#### L1.t3-1 (F2)

- claim: The load row writes no contract, while WC-4 and AC-1.1 require every 3.2 command to write and name one, so AC-1.1 fails for load.
- anchor: "In unattended mode the command writes `<output-dir>/return-contract.yaml`"
- anchor2: "| load | no gate | none (see note) | n/a |"

#### L1.t3-1 (F3)

- claim: WC-4 puts the adversarial contract at the brief's output directory root, while the P1 row puts it under an adversarial subdirectory, so the coordinator reads a different path than the one the worker writes.
- anchor: "Fix the contract filename to `<output>/adversarial/return-contract.yaml` (P1)"
- anchor2: "where `<output-dir>` is the directory the coordinator passed"

#### L1.t3-1 (F4)

- claim: A partial run settles its Task as succeeded, so dependents may start on incomplete output before the coordinator reads the contract.
- anchor: "A partial run left a usable deliverable; `failed` would tell the coordinator the work is lost"
- anchor2: "After `worker_done`, the coordinator opens the report file, then releases or reuses the worker"

#### L1.t3-1 (F5)

- claim: The spec does not say whether the command or the brief creates the fresh directory, so the contract path may not be known before dispatch.
- anchor: "writes each run into a fresh output directory so a re-run starts clean"
- anchor2: "the output directory, so the report path is known before dispatch"

#### L1.t3-1 (F6)

- claim: A re-run that crashes before writing its contract leaves an earlier succeeded contract, which WC-5 reports as a success.
- anchor: "or no report exists; `--outcome succeeded` otherwise"
- anchor2: "The worker passes the contract path as `worker_done --report-path`"

#### L1.t3-1 (F16)

- claim: The spec states as fact that Orca ignores the report file, which its own evidence marks unverified.
- anchor: "Orca does not check the file, so the coordinator opens it."
- anchor2: "Orca's handling of the file is UNVERIFIED"

#### L1.t3-2 (F1)

- claim: The P0 smoke runs are built from a brief that must carry --unattended, but the commands do not accept that flag until P1 or P2, so AC-0.4 cannot pass as written.
- anchor: "These run as workers now if the brief uses the stated flags"
- anchor2: "the exact command line including `--unattended`"

#### L1.t3-2 (F2)

- claim: brainstorm and init-lite have no change in section 3.1, but P1 and AC-1.1 require them to accept the flag and carry the section, so their briefs cannot pass the flag.
- anchor: "The only command changes are the small fixes in the last column."
- anchor2: "the `--unattended` flag accepted by every command in sections 3.1 and 3.2"

#### L1.t3-2 (F4)

- claim: A contract with a missing, unknown or unparseable status is sent as --outcome succeeded, so the coordinator reads a success for an unreadable result.
- anchor: "`--outcome succeeded` otherwise, including `partial`"

#### L1.t3-2 (F11)

- claim: Implement resumes without a flag, which WC-6 does not allow, and retry briefs are not required to use a new output directory.
- anchor: "resumes from its on-disk state when given its resume flag"
- anchor2: "`--resume` (implicit when a ledger matches)"

#### L1.t3-2 (F13)

- claim: A missing output directory under --unattended has no rule, so the report path is unknown before dispatch.
- anchor: "where `<output-dir>` is the directory the coordinator passed"

#### L1.t3-2 (F14)

- claim: The exactly-once rule has no retry rule for a lost response, although Orca provides --retry-request.
- anchor: "The worker sends `worker_done` exactly once"

#### L1.t3-2 (F17)

- claim: Step 5 checks only AskUserQuestion, yet AC-0.4 says it verifies WC-7, and WC-2 forbids more prompt types.
- anchor: "search the transcript for `AskUserQuestion`"
- anchor2: "verified in the step-5 transcript"

#### L1.t3-2 (F24)

- claim: Existing contracts keep their fields, but WC-4 fixes a four-value status set, and no mapping is given for existing status values.
- anchor: "Commands that already write a contract keep their fields and add the missing ones"
- anchor2: "`status` (one of `succeeded`, `partial`, `failed`, `blocked`)"

### L2

#### L2.t2-1 (F1)

- claim: Two index-repo workers in the default shared worktree both write PROJECT_INDEX.md, so one run's output is overwritten, which WC-11 forbids, while the row still lists index-repo as ready with no constraint.
- anchor: "Two workers in one worktree must never write the same file"
- anchor2: "`PROJECT_INDEX.md` (location implied)"

#### L2.t2-1 (F2)

- claim: No requirement covers tool-permission prompts, so a worker parked on a Bash or Write approval stalls like a question and is not caught by WC-1 or WC-2.
- anchor: "a command run by a worker has the same tools as a command a person runs"

#### L2.t2-1 (F4)

- claim: WC-3 lets a blocked gate wait on ask, which sends no worker_done, while AC-2.2 requires a failed worker_done with status blocked, so the two paths cannot both pass.
- anchor: "the session may instead ask the coordinator once"
- anchor2: "`worker_done --outcome failed`; contract `status: blocked`"

#### L2.t2-1 (F10)

- claim: The scope of WC-2 to WC-12 is not stated, and read strictly WC-10 and WC-11 change standalone wait sizes and default output paths that SA-1 keeps unchanged.
- anchor: "Default output paths carry a timestamp or the slug the coordinator passes"
- anchor2: "Without `--unattended`, every prompt, approval gate"

#### L2.t2-1 (F14)

- claim: The fallback budget for a startup prompt is given as well inside the 60 s limit with no number, so an implementer cannot test it.
- anchor: "well inside the readiness limit"

#### L2.t2-1 (F15)

- claim: release-split has a fixed default output beside the spec and no output constraint, so two runs on one spec write the same files, which WC-11 forbids.
- anchor: "spec-shaped input; default `--r1-scope`; never `--interactive`"

#### L2.t2-1 (F16)

- claim: The brief must state worktree placement, but no rule by command class exists, so code-writing workers can share one worktree and edit the same files.
- anchor: "and the worktree placement (`CAPS:115`)"

#### L2.t2-1 (F18)

- claim: An appended Unattended section overrides gate text that stays in the command body, so one file carries two instructions for the same gate and the override is tested only live.
- anchor: "Command-file edits in Phases 1-3 are additive"
- anchor2: "Each gate resolves one of three ways, listed per command in section 3"

#### L2.t2-1 (F21)

- claim: The heartbeat requirement rests on a cadence from the preamble, and its role in liveness is unverified, so its value to the design is unproven.
- anchor: "The worker sends a heartbeat every 5 minutes while working"

#### L2.t3-1 (F7)

- claim: The optional ask route has no flag to carry free-text answers, and AC-2.2 expects a fixed outcome even though the route is optional.
- anchor: "then re-invoke or resume the command with the answer as a flag"
- anchor2: "Each gate resolves one of three ways"

#### L2.t3-1 (F8)

- claim: Tool-permission approval prompts are a person-blocking step that WC-2 does not cover, and the claim that workers have the same tools is not evidenced.
- anchor: "so a command run by a worker has the same tools as a command a person runs"
- anchor2: "No person-blocking step in unattended mode"

#### L2.t3-1 (F11)

- claim: A single Agent-tool call running longer than the heartbeat cadence has no split or heartbeat rule, so the coordinator may treat a working worker as stalled.
- anchor: "A command step that blocks a single tool call for longer than 5 minutes"
- anchor2: "A command's own Agent-tool fan-out stays as it is."

#### L2.t3-1 (F13)

- claim: The fallback bound is not a number, so two implementers can choose fallbacks that pass or fail the readiness limit.
- anchor: "Any such prompt must fall back on its own well inside the readiness limit"
- anchor2: "passes with a 30 s fallback; above about 45 s it fails again"

#### L2.t3-1 (F15)

- claim: The spec gives no rule for combining --unattended with --interactive or for a token inside quoted content, so commands may disagree on the mode.
- anchor: "Explicit `--unattended` flag in the brief (recommended)"
- anchor2: "Without `--unattended`, every prompt, approval gate"

#### L2.t3-1 (F18)

- claim: The index row requires the command to state a fact the spec itself marks unverified.
- anchor: "state that knowledge-base mode does not wait (whether it does is UNVERIFIED)"
- anchor2: "whether it does is UNVERIFIED"

#### L2.t3-2 (F5)

- claim: WC-2 names three resolutions, and WC-3 adds an ask path whose effect on resolution and outcome is not stated.
- anchor: "Each gate resolves one of three ways"
- anchor2: "the session may instead ask the coordinator once"

#### L2.t3-2 (F6)

- claim: The same-tools claim is unsupported, and tool-permission approvals, which can park a worker, are not covered by WC-2.
- anchor: "has the same tools as a command a person runs"

#### L2.t3-2 (F10)

- claim: SA-3 forbids a standalone run writing different files, while SA-4 permits renaming a contract as a defect fix, and the spec does not state which rule wins.
- anchor: "A standalone default run writes the same files it writes today."
- anchor2: "or correct a documented defect"

#### L2.t3-2 (F12)

- claim: No general rule covers a brief that passes both --unattended and --interactive, so a stall is possible.
- anchor: "`--interactive` refused"
- anchor2: "Under `--unattended` the command never calls `AskUserQuestion`"

#### L2.t3-2 (F18)

- claim: WC-10 does not state whether a top-level Agent-tool wait, which also blocks heartbeats, is covered.
- anchor: "A command step that blocks a single tool call for longer than 5 minutes"

### L13

#### L13.t3-1 (F12)

- claim: The AC-C1 pattern uses an escaped pipe that grep -E reads as a literal, so it can pass after an Orca call is added, and it scans core files that SA-2 allows to mention Orca.
- anchor: "(orchestration\\|worktree\\|terminal\\|agent)"
- anchor2: "The only allowed mention of Orca in a changed command is as an example"

#### L13.t3-2 (F3)

- claim: In grep -E the escaped pipe is a literal, so AC-C1 prints nothing for any input and cannot fail, leaving SA-2 and WC-8 without a working check.
- anchor: "(orchestration\\|worktree\\|terminal\\|agent)"

#### L13.t3-2 (F21)

- claim: SA-2 and P0 permit Orca mentions in core files that AC-C1 would reject once fixed.
- anchor: "The only allowed mention of Orca in a changed command"
- anchor2: "add an Orca section to `HOW-WE-WORK.md`"

## Other findings

- L3 (MAJOR, open, overlap): The spec-panel row asks for --output and a new contract, but the supplied command definition already has both, under --report-dir, so the row and INV-B:182 are stale or the repo copy differs.
- L4 (MAJOR, open, single): Under --unattended, reflect accepts its own remediation offer, and WC-9 does not cover self-accepted remediation, so the authority rule that D2 states for implement is absent for reflect.
- L5 (MAJOR, open, single): The recommended D3 makes pr-submit coordinator-only, but the 10/27/6 split and the phase plan still count and schedule pr-submit as a worker.
- L6 (MAJOR, open, overlap): The review-translation gate needs an input that the command does not define, and the cli-eval flags assumed by AC-2.2 are not shown to exist.
- L7 (MINOR, open, single): Every Unattended section depends on an installed contract file with no fallback, so a missing file leaves the rules undefined.
- L8 (MAJOR, open, overlap): A fan-in consumer wired to a subset of N reports has no defined behaviour, so it can receive N-k reports where it expects N.
- L9 (MINOR, open, single): E3 presents a precedent that used the Agent-tool route WC-7 forbids as support for the direct route, with the caveat only in section 1.4.
- L10 (MINOR, open, single): AC-1.1 requires each Unattended section to name return-contract.yaml, but the cli-portify row does not give the location.
- L11 (MAJOR, open, single): Ready-today commands can still stop on /task questions that only the unattended mode resolves, so they are not ready as the heading states.
- L12 (MAJOR, open, single): Several 3.2 commands have no output flag or fixed location, so the contract path is not known before dispatch and cli-eval's fresh-directory rule cannot hold.
- L14 (MINOR, open, single): The live checks need the installed contract file, but the spec does not require superclaude install before them, so they fail in a bare dev checkout.
- L15 (MAJOR, open, overlap): The step 2 pass condition is met when the coordinator never looks at agentWait, because an absent field passes.
- L16 (MAJOR, open, single): The direct route is cited as proven in E3 and unproven in section 1.4, and the spec does not say whether the P3 run and the PR #329 run are the same.
- L17 (MAJOR, open, single): The scope sentence in 1.1 omits the defect fixes in section 3 that SA-4 names.
- L18 (MAJOR, open, single): The same frontmatter defect is out of scope for agent under 8.8 and in scope for business-panel under 3.2, with the need still UNVERIFIED.
- L19 (MAJOR, open, single): The coordinator's next step after partial and blocked is undefined, including who answers a blocked_question and whether partial may start dependents.
- L20 (MAJOR, open, single): tdd and release-split are called ready, but nested /task and tasklist-input prompts stay outside the brief's control.
- L21 (MAJOR, open, single): cli-portify keeps a src/superclaude lookup that the repo rule forbids for installed primitives, and P2 edits that file without fixing it.
- L22 (MINOR, open, single): No check confirms that an installed command can read the installed contract file.
- L23 (MINOR, open, single): The claimed evidence-validator pass is not reproducible from the workspace; noted without action.

## Reviser brief

Blocking finding ids: L1, L2, L13.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
