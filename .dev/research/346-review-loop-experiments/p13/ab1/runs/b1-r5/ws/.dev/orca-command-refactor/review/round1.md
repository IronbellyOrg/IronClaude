review: 1 of 3
# Merged review 1 (coordinator script; panel of 4 reviewers)
candidate: /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p13/ab1/runs/b1-r5/ws/.dev/orca-command-refactor/specs/orca-worker-contract-spec.md sha256 d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d
reviewers:
- t1b-1: report /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p13/ab1/runs/b1-r5/ws/.dev/orca-command-refactor/review/round1-t1b-1.md, block ok true
- t2-1: report /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p13/ab1/runs/b1-r5/ws/.dev/orca-command-refactor/review/round1-t2-1.md, block ok true
- t3-1: report /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p13/ab1/runs/b1-r5/ws/.dev/orca-command-refactor/review/round1-t3-1.md, block ok true
- t3-2: report /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p13/ab1/runs/b1-r5/ws/.dev/orca-command-refactor/review/round1-t3-2.md, block ok false

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | yes | overlap | CRITICAL | 2.1, 2.3, 3.1, 7.2, AC-0.1, AC-0.4, AC-1.1, AC-1.4, AC-2.2, P0, P1, P2, P4, SA-3, SA-4, WC-12, WC-2, WC-3, WC-4, WC-5, WC-6, WC-7, WC-9 | t1b-1, t2-1, t3-1, t3-2 |
| L2 | open | yes | overlap | CRITICAL | P0, SA-2, SA-5, WC-8 | t1b-1, t2-1, t3-1 |
| L3 | open | no | single | MINOR | - | t1b-1 |
| L4 | open | no | overlap | MAJOR | WC-11, WC-9 | t1b-1, t3-1 |
| L5 | open | no | overlap | MAJOR | WC-1 | t2-1, t3-1 |
| L6 | open | no | single | MAJOR | WC-10 | t2-1 |
| L7 | open | no | single | MAJOR | SA-4 | t2-1 |
| L8 | open | no | single | MAJOR | 3.2, WC-7 | t2-1 |
| L9 | open | no | single | MAJOR | 3.2 | t2-1 |
| L10 | open | no | single | MAJOR | WC-2 | t3-1 |
| L11 | open | no | single | MAJOR | - | t3-1 |
| L12 | open | no | single | MAJOR | 1.1, 2.1, SA-4 | t3-1 |
| L13 | open | no | single | MINOR | P2 | t3-1 |
| L14 | open | no | single | MINOR | - | t3-1 |
| L15 | open | no | single | MINOR | - | t3-1 |
| L16 | open | yes | single | MAJOR | 1.4 | t3-2 |

## Blocking findings

### L1

#### L1.t1b-1 (F1)

- claim: The adversarial row puts the contract one directory below the path WC-4 tells the coordinator to read, so the report path handed to worker_done does not exist.
- anchor: "Fix the contract filename to `<output>/adversarial/return-contract.yaml` (P1)"
- anchor2: "the command writes `<output-dir>/return-contract.yaml`, where `<output-dir>` is the directory the coordinator passed"

#### L1.t1b-1 (F2)

- claim: AC-1.1 requires /sc:load to name a return-contract.yaml that the spec says load must not write, so the P1 check cannot pass as written.
- anchor: "every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`"
- anchor2: "a report file would be an unrequested addition"

#### L1.t1b-1 (M2)

- claim: A retry may reuse the brief's output directory and overwrite the first attempt's contract.
- anchor: "writes each run into a fresh output directory so a re-run starts clean"

#### L1.t1b-1 (M3)

- claim: Between P1 and P2 a gated command accepts --unattended yet still prompts, stalling the worker.
- anchor: "the `--unattended` flag accepted by every command in sections 3.1 and 3.2"

#### L1.t1b-1 (M4)

- claim: No path exists for a contract written before the package directory is created.
- anchor: "Write the contract for pre-creation STOPs too (WC-4 \"every outcome\") (P1)"

#### L1.t1b-1 (M5)

- claim: Existing contracts keep their fields, so their status values may not be in the four-value set the checks assert.
- anchor: "`status` (one of `succeeded`, `partial`, `failed`, `blocked`)"

#### L1.t2-1 (F1)

- claim: Section 2.3 requires --unattended in every Task brief, but P0 runs the ready commands before the flag exists, so P0 cannot satisfy both texts.
- anchor: "the exact command line including `--unattended` and every flag section 3 lists as required"
- anchor2: "Uses only the 10 ready commands, so the coordinator gets value before any command changes"

#### L1.t2-1 (F3)

- claim: An empty or status-less contract falls into the otherwise clause and is reported as succeeded, which needs a guess about what counts as a report.
- anchor: "`--outcome succeeded` otherwise, including `partial`"

#### L1.t2-1 (F6)

- claim: A retry that reuses the coordinator's output directory overwrites the first attempt, and no rule says who makes the fresh directory.
- anchor: "writes each run into a fresh output directory so a re-run starts clean"
- anchor2: "where `<output-dir>` is the directory the coordinator passed"

#### L1.t2-1 (F7)

- claim: Step 4 requires YAML with status and command, which a REPORT.md from troubleshoot cannot satisfy, and AC-0.4 does not define the replacement pass condition.
- anchor: "step 4 uses the command's existing report file, since the contract arrives in P1"
- anchor2: "`test -s <contract>` and `uv run python -c"

#### L1.t2-1 (F8)

- claim: The optional ask path makes the AC-2.2 expected outcome depend on the worker's choice rather than on the spec.
- anchor: "the session may instead ask the coordinator once with the preamble's `ask` command"
- anchor2: "contract `status: blocked` with a non-empty `blocked_question`"

#### L1.t2-1 (F9)

- claim: No rule covers an unattended run that has no output directory, so the contract path is undefined for that case.
- anchor: "In unattended mode the command writes `<output-dir>/return-contract.yaml`"

#### L1.t2-1 (F12)

- claim: P1 accepts the flag on gated and outward-default commands before their unattended behavior exists, so a P1 run can take outward actions.
- anchor: "accepted by every command in sections 3.1 and 3.2"

#### L1.t2-1 (F13)

- claim: The flag does not reach the protocol skills where the gates live, and the acceptance check covers only the command files.
- anchor: "Each changed command adds a short `## Unattended mode` section"
- anchor2: "every command in sections 3.1-3.2 has a `## Unattended mode` section"

#### L1.t2-1 (F15)

- claim: The coordinator has no policy for a missing worker_done, an unanswered ask, or a non-consumer_fenced check result, so a worker can wait indefinitely.
- anchor: "After `worker_done`, the coordinator opens the report file"
- anchor2: "On an `ask` timeout it resumes the same message ID"

#### L1.t2-1 (F16)

- claim: An absent agentWait field counts as a pass, though Orca's guide says absence means the field was never read.
- anchor: "`observation.agentWait` is never non-null"

#### L1.t2-1 (F17)

- claim: The contract has no schema version, so mixed writers cannot be told apart.
- anchor: "It follows the return-contract pattern several commands already use"

#### L1.t2-1 (F18)

- claim: The contract status and the Orca outcome are two sources of truth, and only the test run compares them.
- anchor: "The first sentence of the body states the report's status and verdict"

#### L1.t3-1 (F1)

- claim: An implementer who runs AC-0.4 as written on /sc:troubleshoot gets a REPORT.md report that fails step 3's contract-path condition and step 4's YAML parse, so the P0 gate can never pass.
- anchor: "step 4 uses the command's existing report file, since the contract arrives in P1"
- anchor2: "its report path is the WC-4 contract path"

#### L1.t3-1 (F2)

- claim: An implementer who follows the init-lite row unchanged lets a --retry-of attempt overwrite the first attempt's report at the same --output path, which WC-6 forbids.
- anchor: "A retry worker (`worker-start --retry-of`) must not corrupt the first attempt's output."
- anchor2: "Re-run overwrites its marked report"

#### L1.t3-1 (F3)

- claim: An implementer who follows WC-4 for /sc:tdd with --output <file> writes the contract to <file>/return-contract.yaml, which cannot be created.
- anchor: "the directory the coordinator passed (`--output` / `--output-dir`)"
- anchor2: "a precise component prompt, not a bare topic; `--output <file>`"

#### L1.t3-1 (F4)

- claim: An implementer who follows WC-3 at the implement E-HALT-QA gate sends the Ruling question through ask and re-invokes implement with the coordinator's reply, recording an agent message as the Ruling.
- anchor: "re-invoke or resume the command with the answer as a flag"
- anchor2: "The worker stops, writes the halt to its ledger and contract, and ends `failed`."

#### L1.t3-1 (F5)

- claim: An implementer who follows §2.1 and the brainstorm row of §3.1 adds no Unattended mode section to brainstorm, so AC-1.1 fails as written.
- anchor: "every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml`"
- anchor2: "Each changed command adds a short `## Unattended mode` section"

#### L1.t3-1 (F8)

- claim: WC-4 requires a path known before dispatch, but research and workflow produce their contract path at run time, and no location is given for workflow pre-creation STOPs.
- anchor: "so the report path is known before dispatch (WC-4)"
- anchor2: "contract naming the generated `claudedocs/research_*.md` path"

#### L1.t3-1 (F9)

- claim: A contract with a missing or unknown status maps to --outcome succeeded, so a failed run can be reported as success.
- anchor: "`--outcome succeeded` otherwise, including `partial`"
- anchor2: "One report file, known before dispatch, written on every outcome."

#### L1.t3-1 (F10)

- claim: WC-4 gives no order for writing the contract and sending worker_done, so the coordinator can open a missing file.
- anchor: "It is written on success, failure, blocked and partial outcomes, including stops before any other output exists."
- anchor2: "The worker passes the contract path as `worker_done --report-path`."

#### L1.t3-1 (F11)

- claim: Ask retries have no cap and the checks define no coordinator action for a parked worker or a check timeout, so a Dispatch can wait indefinitely.
- anchor: "On an `ask` timeout it resumes the same message ID and never creates a duplicate."
- anchor2: "observation.agentWait` is never non-null"

#### L1.t3-1 (F12)

- claim: The spec does not say what an unattended command does when ~/.claude/WORKER-CONTRACT.md is not installed.
- anchor: "installed to `~/.claude/WORKER-CONTRACT.md`"
- anchor2: "a command switches to when its caller passes `--unattended`"

#### L1.t3-1 (F13)

- claim: The spec-panel row asks to add --output, but the sandbox command definition already has --output and an unattended section, so the row is stale (UNVERIFIED which copy is current).
- anchor: "`target_release` required as a flag for TDD inputs, else blocked"
- anchor2: "the improved-spec step stays off unless the brief asks"

#### L1.t3-2 (F1)

- claim: An absent, misspelled or empty contract status is sent as --outcome succeeded, so the coordinator treats undelivered work as completed.
- anchor: "--outcome succeeded` otherwise, including `partial`"

#### L1.t3-2 (F2)

- claim: Section 2.3 requires --unattended in every brief, but P0 and AC-0.4 run the ready commands without it because the flag does not exist until P1.
- anchor: "the exact command line including `--unattended` and every flag section 3 lists as required"
- anchor2: "7.2 live check on `/sc:troubleshoot"

#### L1.t3-2 (F4)

- claim: AC-0.4 claims the no-wrapper rule is verified in step 5, but step 5 checks only for AskUserQuestion, so WC-7 is never tested.
- anchor: "verified in the step-5 transcript"
- anchor2: "search the transcript for `AskUserQuestion`"

### L2

#### L2.t1b-1 (M1)

- claim: The grep over core may fail on the Orca text P0 adds to core files, depending on a wording the spec does not fix.
- anchor: "prints nothing (SA-2, WC-8)"

#### L2.t2-1 (F2)

- claim: AC-C1 uses backslash-pipe under grep -E, which matches literal pipes, so the check never matches an Orca call and always passes.
- anchor: "(orchestration\\|worktree\\|terminal\\|agent)"

#### L2.t3-1 (F17)

- claim: AC-C1 scans src/superclaude/core, so the contract file or the routing-guide Orca section fails it in P0 wherever it names an Orca command.
- anchor: "The only allowed mention of Orca in a changed command is as an example of a caller's question channel inside the contract file."
- anchor2: "prints nothing (SA-2, WC-8)"

### L16

#### L16.t3-2 (F3)

- claim: Section 1.4 says PR #329 is the only end-to-end proof and no direct-route run was observed, while E3 cites a skill-direct worker contract.
- anchor: "The only end-to-end proof is the PR #329 run"
- anchor2: "invocation_method: \"skill-direct\""

## Other findings

- L3 (MINOR, open, single): Phase gating by user decision is stated two ways and D1 and D4 touch earlier phases.
- L4 (MAJOR, open, overlap): Reflect's default tracked-file write and folder move are not covered by any unattended rule.
- L5 (MAJOR, open, overlap): The fallback has no numeric bound, so an implementer cannot tell whether a 50 s fallback is compliant.
- L6 (MAJOR, open, single): The split trigger is 5 minutes while the rationale wants 4 minutes of margin, so a 4:30 or 5:00 call is left unsplit.
- L7 (MAJOR, open, single): The diff filter misses removed blank lines and removed lines beginning with two dashes, so non-additive edits pass.
- L8 (MAJOR, open, single): The tasklist row keeps reflect fan-out in subagents against INV-B's needs-change verdict, and its depth is not counted against the three-layer limit.
- L9 (MAJOR, open, single): The 27-command count and the pr-submit row assume D3 option (b), while the spec recommends option (a), so the classification is not stable.
- L10 (MAJOR, open, single): The tasklist HALT on needs_human_decision items has no resolution, so a tasklist worker can stop without worker_done.
- L11 (MAJOR, open, single): The tasklist nesting claim is not counted: at the depth limit the reflect Agent tool is withheld and the fan-out fails silently, and the inventory's required change is dropped without a recorded decision.
- L12 (MAJOR, open, single): The scope statement says only the contract changes commands, but §3.2 requires other changes such as the roadmap flag reconciliation.
- L13 (MINOR, open, single): Reflect is labelled ready today, but its row requires a P2 change.
- L14 (MINOR, open, single): E4 presents as evidence a point the inventory marks UNVERIFIED.
- L15 (MINOR, open, single): Many citations point to files outside the workspace, so this review could not check them.

## Reviser brief

Blocking finding ids: L1, L2, L16.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
