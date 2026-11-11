review: 1 of 3
# Merged review 1 (coordinator script; panel of 4 reviewers)
candidate: /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p13/ab1/runs/b1-r2/ws/.dev/orca-command-refactor/specs/orca-worker-contract-spec.md sha256 d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d
reviewers:
- t1b-1: report /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p13/ab1/runs/b1-r2/ws/.dev/orca-command-refactor/review/round1-t1b-1.md, block ok true
- t2-1: report /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p13/ab1/runs/b1-r2/ws/.dev/orca-command-refactor/review/round1-t2-1.md, block ok true
- t3-1: report /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p13/ab1/runs/b1-r2/ws/.dev/orca-command-refactor/review/round1-t3-1.md, block ok true
- t3-2: report /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p13/ab1/runs/b1-r2/ws/.dev/orca-command-refactor/review/round1-t3-2.md, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | yes | overlap | CRITICAL | 2.3, 3.1, 3.2, 4, 7.2, AC-0.4, AC-1.1, AC-1.4, AC-2.2, AC-2.3, P0, P1, P2, P4, SA-1, WC-2, WC-3, WC-4, WC-5, WC-6, WC-7 | t1b-1, t2-1, t3-1, t3-2 |
| L2 | open | no | single | MAJOR | SA-1 | t1b-1 |
| L3 | open | no | single | MAJOR | P2, P4, WC-9 | t1b-1 |
| L4 | open | no | single | MAJOR | 1.3 | t1b-1 |
| L5 | open | no | overlap | MAJOR | 1.4, WC-1 | t1b-1, t3-1 |
| L6 | open | no | single | MAJOR | WC-1, WC-10, WC-12, WC-3, WC-6 | t1b-1 |
| L7 | open | yes | overlap | MAJOR | P0, SA-2, SA-5, WC-8 | t1b-1, t2-1, t3-1, t3-2 |
| L8 | open | no | single | MAJOR | SA-4 | t1b-1 |
| L9 | open | yes | overlap | MAJOR | 1.1, 3, AC-3.1, AC-3.3, SA-4, WC-7 | t1b-1, t3-1 |
| L10 | open | no | single | MINOR | AC-2.4 | t1b-1 |
| L11 | open | yes | overlap | MAJOR | WC-11 | t2-1, t3-2 |
| L12 | open | no | overlap | MAJOR | - | t2-1, t3-1, t3-2 |
| L13 | open | no | single | MAJOR | AC-4.3, WC-10 | t2-1 |
| L14 | open | no | single | MINOR | AC-1.3, SA-3 | t2-1 |
| L15 | open | no | single | MAJOR | - | t3-1 |
| L16 | open | no | single | MINOR | AC-2.2 | t3-1 |
| L17 | open | no | overlap | MAJOR | - | t3-1, t3-2 |
| L18 | open | no | single | MINOR | - | t3-2 |
| L19 | open | no | single | MAJOR | AC-0.3, P0 | t3-2 |
| L20 | open | no | single | MAJOR | SA-6, WC-9 | t3-2 |
| L21 | open | no | single | MINOR | WC-2 | t3-2 |
| L22 | open | no | single | MAJOR | P2 | t3-2 |
| L23 | open | no | single | MAJOR | - | t3-2 |
| L24 | open | no | single | MAJOR | WC-1 | t3-2 |
| L25 | open | no | single | MAJOR | - | t3-2 |
| L26 | open | no | single | MINOR | SA-1 | t3-2 |
| L27 | open | no | single | MINOR | WC-12 | t3-2 |
| L28 | open | no | single | MINOR | AC-4.3, P2, WC-10 | t3-2 |
| L29 | open | no | single | MINOR | - | t3-2 |

## Blocking findings

### L1

#### L1.t1b-1 (F1)

- claim: AC-1.1 requires a contract-naming Unattended mode section on load (which writes no contract) and on implement, post-release and pr-submit (which the spec holds for P4 or the coordinator), so the P1 check cannot pass as written.
- anchor: "every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml`"
- anchor2: "use it as a step inside another worker's brief, not as its own Task"

#### L1.t1b-1 (F2)

- claim: WC-4 builds the contract path from an output directory, but AC-2.2 and the tdd and init-lite rows pass a file or no output at all, so the contract the check must read has no defined location.
- anchor: "where `<output-dir>` is the directory the coordinator passed"
- anchor2: "/sc:tdd \"auth\" --unattended --output <file>"

#### L1.t1b-1 (F3)

- claim: AC-0.4 requires 7.2 step 3 to pass in P0, but step 3 demands the WC-4 contract path and contract status, which P0 says do not exist until P1, so the P0 gate fails for the wrong reason.
- anchor: "steps 1-3 and 5-7 pass; step 4 uses the command's existing report file"
- anchor2: "its report path is the WC-4 contract path"

#### L1.t1b-1 (F4)

- claim: A stale contract from an earlier attempt in the same directory is read as the retry's report because nothing requires it to be replaced at start.
- anchor: "`--outcome failed` when the report says `failed` or `blocked`, or no report exists"

#### L1.t1b-1 (F7)

- claim: Nobody is assigned to create the fresh directory on a retry, and a coordinator-fixed directory is the opposite of fresh.
- anchor: "writes each run into a fresh output directory so a re-run starts clean"
- anchor2: "so the report path is known before dispatch (WC-4)"

#### L1.t1b-1 (F13)

- claim: A workflow stop before the package exists has no package directory to hold the contract, and no other location is given.
- anchor: "Write the contract for pre-creation STOPs too (WC-4 \"every outcome\")"

#### L1.t1b-1 (F14)

- claim: WC-3 allows ask where AC-2.2 expects worker_done failed and a blocked contract, so a compliant run can fail the check.
- anchor: "the session may instead ask the coordinator once with the preamble's `ask` command"

#### L1.t1b-1 (F16)

- claim: Keeping existing fields conflicts with the fixed four-value status set if an existing contract uses another status word (existing contracts not checkable here).
- anchor: "Commands that already write a contract keep their fields and add the missing ones."

#### L1.t1b-1 (F17)

- claim: An unverified assumption is stated as a fact.
- anchor: "Orca does not check the file, so the coordinator opens it."

#### L1.t2-1 (F1)

- claim: A brief built per section 2.3 passes --unattended to ready commands that do not accept it until P1, so the P0 smoke runs cannot follow both section 2.3 and section 3.1.
- anchor: "the exact command line including `--unattended` and every flag section 3 lists as required"
- anchor2: "`--output <dir>`; never `--interactive`"

#### L1.t2-1 (F2)

- claim: Section 3.1 says the ready commands change only by small fixes, but AC-1.1 requires every section 3.1 and 3.2 command, including Phase 2 to 4 commands, to have an Unattended mode section in Phase 1.
- anchor: "The only command changes are the small fixes in the last column."
- anchor2: "every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml`"

#### L1.t2-1 (F3)

- claim: For /sc:troubleshoot the existing report is REPORT.md, which has no YAML status or command keys, so the step 4 assertion cannot pass as AC-0.4 requires.
- anchor: "step 4 uses the command's existing report file, since the contract arrives in P1."
- anchor2: "`test -s <contract>` and `uv run python -c"

#### L1.t2-1 (F4)

- claim: pr-submit is a needs-change row in P4 and in the count of 27, but the recommended D3 option makes no pr-submit change.
- anchor: "outward actions per open decision D3"
- anchor2: "no pr-submit changes in Phase 4."

#### L1.t2-1 (F5)

- claim: WC-2 allows three gate resolutions, while reflect's auto-accept is a fourth, and the spec does not say whether it counts as a documented default.
- anchor: "Each gate resolves one of three ways, listed per command in section 3"
- anchor2: "make `--remediate` follow the existing headless auto-accept rule"

#### L1.t2-1 (F6)

- claim: WC-4 places the contract in a directory the coordinator passed, but tdd and init-lite take --output as a file, so the contract location is undefined.
- anchor: "where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`)"
- anchor2: "a precise component prompt, not a bare topic; `--output <file>`"

#### L1.t2-1 (F8)

- claim: AC-0.4 says the no-wrapper rule is verified in step 5, but step 5 only searches for AskUserQuestion, so the WC-7 rule has no check.
- anchor: "each run directly by the worker (no Agent-tool wrapper, verified in the step-5 transcript)"
- anchor2: "search the transcript for `AskUserQuestion`"

#### L1.t2-1 (F11)

- claim: No requirement gives a retry a new output directory, so a coordinator that reuses --output on retry can corrupt the first attempt's output.
- anchor: "A retry worker (`worker-start --retry-of`) must not corrupt the first attempt's output."
- anchor2: "the output directory, so the report path is known before dispatch (WC-4)"

#### L1.t2-1 (F12)

- claim: WC-5 maps any status outside the four-value set to succeeded, which the spec never states as intended.
- anchor: "`status` (one of `succeeded`, `partial`, `failed`, `blocked`)"
- anchor2: "`--outcome failed` when the report says `failed` or `blocked`, or no report exists"

#### L1.t3-1 (F1)

- claim: WC-4 puts adversarial's contract at `<output-dir>/return-contract.yaml` while the 3.1 fix puts it at `<output>/adversarial/return-contract.yaml`, so the coordinator's known path and the 7.2 step 4 check disagree for the same run.
- anchor: "Fix the contract filename to `<output>/adversarial/return-contract.yaml` (P1)"
- anchor2: "In unattended mode the command writes `<output-dir>/return-contract.yaml`"

#### L1.t3-1 (F2)

- claim: For tdd (and init-lite, whose row also passes `--output <file>`) WC-4 cannot write `<output-dir>/return-contract.yaml` because the value is a file, so the blocked contract AC-2.2 requires has no location the coordinator can open.
- anchor: "a precise component prompt, not a bare topic; `--output <file>`"
- anchor2: "the directory the coordinator passed (`--output` / `--output-dir`)"

#### L1.t3-1 (F3)

- claim: WC-3 lets a coordinator answer a blocked implement Ruling and resume with that answer as a flag, which is the relayed Ruling D2 leaves to the user and qa.md:238 (quoted at INV-A:66) forbids.
- anchor: "the session may instead ask the coordinator once with the preamble's `ask` command"
- anchor2: "stop with the halt recorded in the ledger and the contract as blocked"

#### L1.t3-1 (F4)

- claim: AC-0.4 says step 3 passes in P0, but step 3 requires the WC-4 contract path and its status, which P0 does not create, so the P0 gate cannot pass as written.
- anchor: "steps 1-3 and 5-7 pass; step 4 uses the command's existing report file"
- anchor2: "its report path is the WC-4 contract path"

#### L1.t3-1 (F6)

- claim: 3.1 gives brainstorm no change, but P1 and AC-1.1 require the --unattended flag and an Unattended mode section for every 3.1 command, so AC-1.1 fails for brainstorm.
- anchor: "The only command changes are the small fixes in the last column."
- anchor2: "the `--unattended` flag accepted by every command in sections 3.1 and 3.2"

#### L1.t3-1 (M7)

- claim: No phase row names release-split, tdd, troubleshoot or init-lite as getting a WC-4 contract, yet AC-2.3 step 4 requires one for P2 commands.
- anchor: "The WC-4 contract in unattended mode"
- anchor2: "7.2 passes with `--outcome succeeded`"

#### L1.t3-1 (M8)

- claim: The workflow package id is created at run time and workflow has no output flag, so the coordinator cannot state the contract path before dispatch as 2.3 requires.
- anchor: "`.dev/tasks/to-do/<id>/return-contract.yaml`"
- anchor2: "so the report path is known before dispatch (WC-4)"

#### L1.t3-2 (F1)

- claim: WC-3 lets a coordinator answer re-invoke a halted implement run, which D2(a) and the implement row forbid, and qa.md:238 bars as a Ruling.
- anchor: "then re-invoke or resume the command with the answer as a flag"
- anchor2: "on `E-HALT-QA` or `E-NO-RULING`, stop with the halt recorded in the ledger"

#### L1.t3-2 (F2)

- claim: AC-0.4 cannot pass in P0: the brief needs a flag P1 adds, the step 3 path does not exist until P1, and step 4 expects YAML from a Markdown report.
- anchor: "the exact command line including `--unattended`"
- anchor2: "its report path is the WC-4 contract path"

#### L1.t3-2 (F4)

- claim: WC-4 requires a contract path known before dispatch, but workflow has no output flag and research and workflow names are generated at run time.
- anchor: "where `<output-dir>` is the directory the coordinator passed"
- anchor2: "contract naming the generated `claudedocs/research_*.md` path"

#### L1.t3-2 (F6)

- claim: Succeeded settles a Task complete, so a dependent can start after a FAIL audit, unless the coordinator checks the contract, which §2.3 does not require.
- anchor: "including an audit whose verdict is FAIL (the audit itself succeeded)"

#### L1.t3-2 (F16)

- claim: The WC-4 contract has no schema version, although the existing workflow contract has one.
- anchor: "It follows the return-contract pattern several commands already use"

#### L1.t3-2 (F19)

- claim: A retry reuses the Task brief and so the same output directory, which WC-6 says must be fresh.
- anchor: "writes each run into a fresh output directory so a re-run starts clean"
- anchor2: "the output directory, so the report path is known before dispatch"

#### L1.t3-2 (F23)

- claim: A blocked stop after partial edits leaves no list of changed files, so the coordinator cannot tell what to revert.
- anchor: "the command writes its report with `status: blocked` and the exact question, and stops"

#### L1.t3-2 (F24)

- claim: A zero-byte report and an out-of-set status are not mapped.
- anchor: "when the report says `failed` or `blocked`, or no report exists"

### L7

#### L7.t1b-1 (F11)

- claim: AC-C1 greps src/superclaude/core, where the P0 contract file and routing-guide Orca section may legitimately name orca commands.
- anchor: "prints nothing (SA-2, WC-8)"
- anchor2: "The only allowed mention of Orca in a changed command is as an example of a caller's question channel inside the contract file."

#### L7.t2-1 (F9)

- claim: AC-C1 scans src/superclaude/core, where P0 must add an Orca section and where SA-2 permits Orca mentions, so the common check can fail on text the spec requires or allows.
- anchor: "prints nothing (SA-2, WC-8)"
- anchor2: "The only allowed mention of Orca in a changed command is as an example"

#### L7.t3-1 (M1)

- claim: In grep -E, `\|` is a literal pipe, so AC-C1 never matches real orca invocations and passes vacuously; AC-C4 has the same escaping.
- anchor: "(orchestration\\|worktree\\|terminal\\|agent)"

#### L7.t3-2 (F3)

- claim: In grep -E the escaped bar is literal, so AC-C1 never matches an Orca call and passes vacuously, letting a command break standalone use.
- anchor: "(orchestration\\|worktree\\|terminal\\|agent)\\b"

#### L7.t3-2 (F20)

- claim: SA-2 is worded so that the rule for changed commands points at the contract file, which is not a changed command.
- anchor: "The only allowed mention of Orca in a changed command is as an example"

### L9

#### L9.t1b-1 (F15)

- claim: The spec does not say how a session whose first message is a preamble starts a slash command.
- anchor: "one worker (a top-level Claude session in its own Orca terminal) runs one command"

#### L9.t3-1 (F5)

- claim: Reading 1.1 as the scope bound skips the defect fixes section 3 and SA-4 require (roadmap, validate-roadmap, validate-tests, explain, business-panel, load), so AC-3.1 and AC-3.3 cannot pass.
- anchor: "What changes in the commands is limited to the worker contract in section 2"
- anchor2: "Existing lines change only where section 3 names a defect fix"

#### L9.t3-1 (M5)

- claim: The cli-portify checkout restriction changes an existing line but is not on SA-4's closed list of permitted fixes, so AC-C5 cannot be applied to it.
- anchor: "dispatch only inside an IronClaude checkout (hardcoded template path)"
- anchor2: "Existing lines change only where section 3 names a defect fix"

### L11

#### L11.t2-1 (F7)

- claim: WC-11 forbids two workers writing one file, but index-repo and init-lite keep fixed default output paths and stay ready with no brief flags.
- anchor: "Default output paths carry a timestamp or the slug the coordinator passes"
- anchor2: "`PROJECT_INDEX.md` (location implied)"

#### L11.t3-2 (F5)

- claim: Editing commands can run as two workers in one worktree, and the later source write overwrites the earlier, which WC-11 forbids and nothing prevents.
- anchor: "Two workers in one worktree must never write the same file."

## Other findings

- L2 (MAJOR, open, single): The text does not say that a quoted argument containing the text --unattended is not the switch.
- L3 (MAJOR, open, single): task commit/push, post-release and pr-submit have no named explicit flag, and the auggie-review and task authorizations sit in P2 while the spec gates only P4 on D2-D4.
- L4 (MAJOR, open, single): The join step is unspecified when blocked or failed workers leave fewer reports than workers, down to below the 2-artifact minimum of /sc:adversarial.
- L5 (MAJOR, open, overlap): The sandbox evidence does not show that a first-action question cannot block readiness when Claude receives its task on the command line.
- L6 (MAJOR, open, single): WC-1, WC-3, WC-6 and WC-12 have no acceptance check, and WC-10 is checked for pr-submit only.
- L8 (MAJOR, open, single): Adding a flag to an existing Usage line shows as a deleted line, so AC-C5 can fail on a purely additive change.
- L10 (MINOR, open, single): The count covers one page only, so an added comment on a PR with 30 or more can leave it unchanged.
- L12 (MAJOR, open, overlap): E4 states as established a fact that CAPS:155 marks UNVERIFIED and section 1.4 concedes.
- L13 (MAJOR, open, single): WC-10 splits only calls longer than 5 minutes, but AC-4.3 forbids any call over 240 s, so a 4.5-minute call passes one and fails the other.
- L14 (MINOR, open, single): SA-3 depends on a new output flag that the spec never defines, so it is unclear whether a standalone --output run writes the contract.
- L15 (MAJOR, open, single): The nesting-limit claim rests on an external doc quote and is stated as fact, while INV-B:210 and INV-B:314 mark subagent-to-agent spawning as UNVERIFIED.
- L16 (MINOR, open, single): The safety flags are never named, so an implementer must guess which flags make the run non-blocked.
- L17 (MAJOR, open, overlap): The D1 example passes --output to /sc:troubleshoot, which no section 3 row names as a flag.
- L18 (MINOR, open, single): pr-submit is counted as a worker candidate although D3 recommends coordinator-only, so the 10/27/6 counts depend on an open decision.
- L19 (MAJOR, open, single): P0 builds the contract and routing-guide edits before the smoke runs that test the decision, so a failed test leaves the edits behind.
- L20 (MAJOR, open, single): It is unstated whether --unattended triggers reflect's headless auto-accept, which runs remediation that can change code.
- L21 (MINOR, open, single): Commands point to an installed file that may be absent after a partial or older install, and no fallback is stated.
- L22 (MAJOR, open, single): The hardcoded src/superclaude template path is flagged but unscheduled, and no AC checks for such paths.
- L23 (MAJOR, open, single): Command edits can leave the plugins mirror out of step, and no AC checks the mirror.
- L24 (MAJOR, open, single): WC-1 has an owner outside every phase and no AC checks readiness.
- L25 (MAJOR, open, single): The step 2 pass also holds when the field is absent, which means Orca never looked, so a stalled worker can pass.
- L26 (MINOR, open, single): It is unclear whether the roadmap prompt change applies only under --unattended, which SA-1 requires.
- L27 (MINOR, open, single): Ordinary follow-ups have no stated handling.
- L28 (MINOR, open, single): The pr-submit wait check is unverifiable until the poll runtime is measured, and P2 has no check for it.
- L29 (MINOR, open, single): CAPS:158 is the provenance rule, which only partly supports the claim it is cited for.

## Reviser brief

Blocking finding ids: L1, L7, L9, L11.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
