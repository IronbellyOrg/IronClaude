review: 1 of 3
# Merged review 1 (coordinator script; panel of 4 reviewers)
candidate: /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p13/ab1/runs/b1-r1/ws/.dev/orca-command-refactor/specs/orca-worker-contract-spec.md sha256 d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d
reviewers:
- t1b-1: report /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p13/ab1/runs/b1-r1/ws/.dev/orca-command-refactor/review/round1-t1b-1.md, block ok true
- t2-1: report /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p13/ab1/runs/b1-r1/ws/.dev/orca-command-refactor/review/round1-t2-1.md, block ok true
- t3-1: report /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p13/ab1/runs/b1-r1/ws/.dev/orca-command-refactor/review/round1-t3-1.md, block ok true
- t3-2: report /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p13/ab1/runs/b1-r1/ws/.dev/orca-command-refactor/review/round1-t3-2.md, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | yes | overlap | CRITICAL | 2.1, 2.3, 3, 3.1, 3.2, 6, 7.2, AC-0.4, AC-1.1, AC-1.2, P0, P1, P2, P4, SA-2, WC-11, WC-4, WC-9 | t1b-1, t2-1, t3-1, t3-2 |
| L2 | open | yes | overlap | CRITICAL | 2.3, 3.1, 4, AC-2, AC-2.2, SA-3, WC-2, WC-3, WC-4, WC-5, WC-6 | t1b-1, t2-1, t3-1, t3-2 |
| L3 | open | no | single | MAJOR | AC-4.3, WC-10 | t1b-1 |
| L4 | open | no | overlap | MAJOR | 3.2, AC-4.3, WC-10 | t1b-1, t3-2 |
| L5 | open | no | overlap | MAJOR | 3.2, WC-7 | t1b-1, t3-2 |
| L6 | open | no | single | MINOR | - | t1b-1 |
| L7 | open | no | overlap | MAJOR | 1.4, WC-7 | t1b-1, t3-2 |
| L8 | open | no | single | MINOR | WC-1 | t1b-1 |
| L9 | open | yes | overlap | MAJOR | SA-2, WC-8 | t2-1, t3-2 |
| L10 | open | yes | single | MAJOR | AC-1.1, WC-4, WC-5 | t2-1 |
| L11 | open | no | overlap | MAJOR | SA-6, WC-9 | t2-1, t3-1 |
| L12 | open | no | overlap | MAJOR | - | t2-1, t3-1 |
| L13 | open | no | single | MAJOR | SA-1 | t3-1 |
| L14 | open | no | single | MINOR | - | t3-1 |
| L15 | open | no | single | MAJOR | 3.2, AC-2.2, AC-2.4, P2, WC-2, WC-9 | t3-2 |
| L16 | open | no | single | MAJOR | 1.3 | t3-2 |

## Blocking findings

### L1

#### L1.t1b-1 (F1)

- claim: AC-1.1 requires /sc:load to carry a return-contract.yaml section while its row and the Decisions table say it gets no report file, so the P1 check cannot pass.
- anchor: "every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml`"
- anchor2: "a report file would be an unrequested addition"

#### L1.t1b-1 (F3)

- claim: AC-0.4 excuses only step 4 of the live check although step 3 also needs a WC-4 contract that does not exist until P1, so the P0 gate that blocks every later phase cannot pass.
- anchor: "steps 1-3 and 5-7 pass; step 4 uses the command's existing report file, since the contract arrives in P1"
- anchor2: "its report path is the WC-4 contract path"

#### L1.t1b-1 (F5)

- claim: After P1 alone, --unattended is accepted but inert on commands whose outward defaults are only turned off in P2 or P4.
- anchor: "the `--unattended` flag accepted by every command in sections 3.1 and 3.2 (a no-op where a command has no gate)"
- anchor2: "any default that pushes, opens a PR, posts to GitHub, installs, provisions or calls a paid external run is off"

#### L1.t1b-1 (F9)

- claim: Whether the new core files may contain a command-shaped Orca example decides if AC-C1 passes, and the spec does not say.
- anchor: "The only allowed mention of Orca in a changed command is as an example of a caller's question channel inside the contract file."
- anchor2: "add an Orca section to `HOW-WE-WORK.md` and its two mirrored copies"

#### L1.t1b-1 (F12)

- claim: P1 names 13 commands but its scope and AC-1.1 cover 37, so brainstorm and init-lite are in no phase cell.
- anchor: "analyze, build, business-panel, design, document, explain, index, test, load (usage line only); fixes to adversarial, cleanup-audit, index-repo, workflow"
- anchor2: "every command in sections 3.1-3.2 has a `## Unattended mode` section"

#### L1.t1b-1 (F14)

- claim: The term paid external run is not defined.
- anchor: "calls a paid external run is off"

#### L1.t2-1 (F2)

- claim: AC-0.4 step 3 needs a WC-4 contract, which only arrives in P1, so P0 cannot pass as written.
- anchor: "its report path is the WC-4 contract path"
- anchor2: "steps 1-3 and 5-7 pass"

#### L1.t2-1 (F5)

- claim: brainstorm and init-lite are listed as needing no change, but P1 and AC-1.1 require the flag and a contract for both, and no phase lists them.
- anchor: "The only command changes are the small fixes in the last column."
- anchor2: "`--unattended` flag accepted by every command in sections 3.1 and 3.2"

#### L1.t2-1 (F9)

- claim: cleanup-audit's fixed output directory lets two concurrent workers overwrite each other's checkpoint, which WC-11 forbids.
- anchor: "output dir is fixed, so one audit per worktree at a time"
- anchor2: "must never write the same file"

#### L1.t3-1 (F1)

- claim: An implementer who follows AC-1.1 adds a return-contract.yaml to /sc:load, which the load row and the Decisions table say must not get a report file, so the test and the load design cannot both pass.
- anchor: "every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml`"
- anchor2: "a report file would be an unrequested addition"

#### L1.t3-1 (F2)

- claim: An implementer who runs AC-0.4 on /sc:troubleshoot finds REPORT.md rather than the YAML contract that step 4 parses, and on /sc:adversarial there is no fixed contract path, so the P0 gate cannot close as written.
- anchor: "step 4 uses the command's existing report file, since the contract arrives in P1"
- anchor2: "test -s <contract>"

#### L1.t3-2 (F1)

- claim: AC-1.1 at P1 requires an Unattended section in every 3.1-3.2 command, but brainstorm, init-lite, tdd and release-split get none in P1, so the P1 check cannot pass.
- anchor: "every command in sections 3.1-3.2 has a"

#### L1.t3-2 (F2)

- claim: AC-0.4 step 4 asserts YAML keys status and command, but /sc:troubleshoot without --caller task-unified writes only REPORT.md, and the pass condition gives no replacement check, so the P0 gate cannot pass for that command.
- anchor: "step 4 uses the command's existing report file"

#### L1.t3-2 (F3)

- claim: Section 2.3 requires every brief to carry --unattended, but the P0 smoke runs use ready commands whose briefs omit it and whose commands do not accept it until P1.
- anchor: "the exact command line including `--unattended`"
- anchor2: "run three ready commands as real Orca workers, invoked directly"

#### L1.t3-2 (F15)

- claim: index-repo's default PROJECT_INDEX.md is a fixed path that section 3.1 keeps ready with only a location fix, so two workers in one worktree write the same file, which WC-11 forbids.
- anchor: "Default output paths carry a timestamp or the slug the coordinator passes"

### L2

#### L2.t1b-1 (F2)

- claim: WC-4 puts the contract inside a directory the coordinator passes, but tdd and init-lite take a file-valued --output and adversarial and workflow fix other paths, so the contract location is contradictory.
- anchor: "where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`)"
- anchor2: "--unattended --output <file>` with a bare topic"

#### L2.t1b-1 (F4)

- claim: WC-3 lets a coordinator answer become a flag for gates that D2 and D4 reserve for the person.
- anchor: "then re-invoke or resume the command with the answer as a flag"
- anchor2: "The worker stops, writes the halt to its ledger and contract, and ends `failed`."

#### L2.t1b-1 (F7)

- claim: The four statuses are not defined and may clash with the values existing contracts already use.
- anchor: "`status` (one of `succeeded`, `partial`, `failed`, `blocked`)"
- anchor2: "Commands that already write a contract keep their fields and add the missing ones."

#### L2.t1b-1 (F8)

- claim: No behavior is given for --unattended without an output directory, on a coordinator-only command, as a refusal, or inside quoted content.
- anchor: "including stops before any other output exists"
- anchor2: "These six are never dispatched as workers and get no `--unattended` mode."

#### L2.t1b-1 (F10)

- claim: Fresh-directory re-runs can make the pre-announced report path stale or overwrite the first attempt, and retries and ask resumes have no cap.
- anchor: "writes each run into a fresh output directory so a re-run starts clean"
- anchor2: "so the report path is known before dispatch (WC-4)"

#### L2.t1b-1 (F13)

- claim: WC-4 and SA-3 give different conditions for writing the contract.
- anchor: "The new contract file and report files are written only in unattended mode or when the caller passes the new output flag."
- anchor2: "In unattended mode the command writes"

#### L2.t1b-1 (F19)

- claim: The contract has no version field.
- anchor: "It follows the return-contract pattern several commands already use and carries at least"

#### L2.t2-1 (F1)

- claim: WC-3 lets a blocked worker ask the coordinator and re-invoke with the answer, so the implement halt can receive a Ruling before D2 is decided, which the Ruling rule forbids.
- anchor: "the session may instead ask the coordinator once with"
- anchor2: "stop with the halt recorded in the ledger and the contract as blocked"

#### L2.t2-1 (F6)

- claim: init-lite overwrites its report on retry, which replaces the first attempt's report that WC-6 says must be kept.
- anchor: "Re-run overwrites its marked report"
- anchor2: "must not corrupt the first attempt"

#### L2.t2-1 (F7)

- claim: WC-4 defines the contract location through an output directory that tdd (file), workflow (none) and adversarial (subfolder) do not provide.
- anchor: "where `<output-dir>` is the directory the coordinator passed"
- anchor2: "a precise component prompt, not a bare topic; `--output <file>`"

#### L2.t2-1 (F8)

- claim: A fresh directory chosen by the command is unknown before dispatch, so WC-4 and WC-6 conflict on retry.
- anchor: "writes each run into a fresh output directory so a re-run starts clean"
- anchor2: "One report file, known before dispatch, written on every outcome"

#### L2.t2-1 (F11)

- claim: A contract with status not blocked but a non-empty blocked_question has no outcome rule, so a waiting worker can be sent as succeeded.
- anchor: "`--outcome succeeded` otherwise, including `partial`"

#### L2.t2-1 (F12)

- claim: A partial or unparseable contract has no atomic-write rule and no coordinator handling rule.
- anchor: "It is written on success, failure, blocked and partial outcomes"

#### L2.t2-1 (F14)

- claim: Re-invocation and ask cycles have no bound, so a command can block and re-ask indefinitely.
- anchor: "then re-invoke or resume the command with the answer as a flag"
- anchor2: "On an `ask` timeout it resumes the same message ID"

#### L2.t2-1 (F15)

- claim: The contract has no version field, and AC-2.x checks only two fields, so per-command contract evolution is unguarded.
- anchor: "carries at least: `status` (one of `succeeded`, `partial`, `failed`, `blocked`)"

#### L2.t3-1 (F3)

- claim: An implementer who dispatches /sc:workflow with --handoff none and no output directory gets a contract path that exists only after the package id is created, so the coordinator cannot know the report path before dispatch as WC-4 requires.
- anchor: "`--handoff none` | `.dev/tasks/to-do/<id>/return-contract.yaml`"
- anchor2: "One report file, known before dispatch, written on every outcome."

#### L2.t3-1 (F4)

- claim: An implementer who passes the same --output on a retry gives a command with no resume flag a directory the first attempt already wrote, so it either overwrites that output, which WC-6 forbids, or writes elsewhere, which WC-4's known-before-dispatch path forbids.
- anchor: "writes each run into a fresh output directory so a re-run starts clean"
- anchor2: "is the directory the coordinator passed"

#### L2.t3-1 (M3)

- claim: The spec does not say how a blocked worker re-invokes a command after the coordinator's answer, and a re-invoked fresh-dir command repeats its work or writes a second output, so the answered path is undefined.
- anchor: "re-invoke or resume the command with the answer as a flag"

#### L2.t3-2 (F4)

- claim: WC-4 requires the contract path to be known before dispatch, but the section 3.1 workflow row gives a per-run <id> path, so the coordinator cannot open the report as section 2.3 requires.
- anchor: "is the directory the coordinator passed"
- anchor2: "`.dev/tasks/to-do/<id>/return-contract.yaml`"

#### L2.t3-2 (F5)

- claim: WC-6 has the command write a re-run into a fresh directory, which makes the WC-4 path unknown before dispatch; if the coordinator reuses --output on retry, the first attempt's output is overwritten.
- anchor: "writes each run into a fresh output directory so a re-run starts clean"
- anchor2: "is the directory the coordinator passed"

#### L2.t3-2 (F7)

- claim: WC-3 does not name the flag carrying the answer, whether the blocked contract is replaced, or which outcome is sent after the resumed run, so implementers would send different worker_done outcomes.
- anchor: "re-invoke or resume the command with the answer as a flag"

#### L2.t3-2 (F8)

- claim: A contract with no status key or an unlisted value falls into the otherwise branch and is sent as succeeded, so a malformed report reaches the coordinator as a success.
- anchor: "`--outcome succeeded` otherwise, including `partial`"

### L9

#### L9.t2-1 (F3)

- claim: In grep -E the escaped pipe is a literal, so AC-C1 never matches an Orca call and always passes, which hides an SA-2 violation.
- anchor: "\\borca(-ide)?[[:space:]]+(orchestration\\|worktree\\|terminal\\|agent)\\b"

#### L9.t3-2 (F6)

- claim: The AC-C1 grep never matches a real orca orchestration line and matches only a literal pipe, so the common check passes whatever the commands contain and SA-2 is not enforced.
- anchor: "(orchestration\\|worktree\\|terminal\\|agent)"

### L10

#### L10.t2-1 (F4)

- claim: AC-1.1 requires a contract for load, the decision table rejects it, and WC-5 then sends a successful load run as failed.
- anchor: "use it as a step inside another worker"
- anchor2: "every command in sections 3.1-3.2 has a `## Unattended mode` section naming return-contract.yaml"

## Other findings

- L3 (MAJOR, open, single): A 4 to 5 minute call is allowed by WC-10 and fails AC-4.3.
- L4 (MAJOR, open, overlap): The pr-submit wait reading differs from the inventories and D3(b) names a wait change the row says may be unneeded.
- L5 (MAJOR, open, overlap): The nesting claim for tasklist has no layer count.
- L6 (MINOR, open, single): The re-read and validator claims cannot be reproduced from the workspace.
- L7 (MAJOR, open, overlap): E3 and 1.4(1) use the same evidence for opposite points.
- L8 (MINOR, open, single): WC-1 gives no number, no delivering phase and no check.
- L11 (MAJOR, open, overlap): Unattended reflect may auto-accept remediation that edits code, and the spec does not say the brief must authorize it; the headless trigger also changes from claude --print to a flag.
- L12 (MAJOR, open, overlap): The tasklist nesting claim rests on an UNVERIFIED docs citation and is stated as settled.
- L13 (MAJOR, open, single): The spec never names the safety flags, so an implementer cannot decide whether a given cli-eval brief passes or blocks.
- L14 (MINOR, open, single): The inventory quote of EVIDENCE.md:45 records only the ready state, so the 'answered' claim in E2 is not supported by the quoted evidence.
- L15 (MAJOR, open, single): The safety flags are not defined anywhere in the spec, so the cli-eval run gate cannot be implemented or tested as written.
- L16 (MAJOR, open, single): R1 states as fact that a nested worker-start is refused, but UNVERIFIED item 5 says call-site enforcement was not traced, so the rejection rests on an unchecked claim.

## Reviser brief

Blocking finding ids: L1, L2, L9, L10.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
