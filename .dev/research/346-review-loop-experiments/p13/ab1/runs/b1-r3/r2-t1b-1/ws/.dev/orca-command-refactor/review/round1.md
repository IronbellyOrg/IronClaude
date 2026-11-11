review: 1 of 3
# Merged review 1 (coordinator script; panel of 4 reviewers)
candidate: /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p13/ab1/runs/b1-r3/ws/.dev/orca-command-refactor/specs/orca-worker-contract-spec.md sha256 d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d
reviewers:
- t1b-1: report /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p13/ab1/runs/b1-r3/ws/.dev/orca-command-refactor/review/round1-t1b-1.md, block ok true
- t2-1: report /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p13/ab1/runs/b1-r3/ws/.dev/orca-command-refactor/review/round1-t2-1.md, block ok true
- t3-1: report /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p13/ab1/runs/b1-r3/ws/.dev/orca-command-refactor/review/round1-t3-1.md, block ok true
- t3-2: report /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p13/ab1/runs/b1-r3/ws/.dev/orca-command-refactor/review/round1-t3-2.md, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | yes | overlap | CRITICAL | 1.4, 2.3, 3.1, 6, 7.3, AC-0.4, AC-1.1, AC-1.4, AC-2.2, AC-3.2, AC-4.2, P0, P1, SA-1, WC-1, WC-10, WC-11, WC-2, WC-3, WC-4, WC-5, WC-6, WC-7, WC-9 | t1b-1, t2-1, t3-1, t3-2 |
| L2 | open | no | overlap | MAJOR | - | t1b-1, t2-1 |
| L3 | open | no | single | MAJOR | SA-1, WC-1, WC-10, WC-11, WC-12, WC-3, WC-6 | t1b-1 |
| L4 | open | no | overlap | MAJOR | - | t1b-1, t2-1, t3-1 |
| L5 | open | yes | overlap | CRITICAL | 5, P0, SA-2, WC-8 | t1b-1, t2-1, t3-1, t3-2 |
| L6 | open | no | overlap | MAJOR | AC-4.3, WC-10 | t1b-1, t2-1, t3-1 |
| L7 | open | yes | single | MAJOR | - | t2-1 |
| L8 | open | no | overlap | MINOR | - | t2-1, t3-1 |
| L9 | open | no | single | MAJOR | WC-8 | t2-1 |
| L10 | open | no | single | MAJOR | WC-2 | t2-1 |
| L11 | open | no | overlap | MAJOR | WC-9 | t2-1, t3-2 |
| L12 | open | no | single | MINOR | SA-1 | t2-1 |
| L13 | open | yes | overlap | MAJOR | 1.1, SA-4 | t2-1, t3-2 |
| L14 | open | no | single | MINOR | P4 | t2-1 |
| L15 | open | no | single | MINOR | AC-1.3, SA-6 | t2-1 |
| L16 | open | yes | single | MAJOR | P2 | t3-1 |
| L17 | open | no | single | MAJOR | 2.3 | t3-1 |
| L18 | open | no | single | MAJOR | WC-9 | t3-1 |
| L19 | open | no | single | MAJOR | 2.1 | t3-1 |
| L20 | open | no | single | MAJOR | 2.1, SA-4 | t3-1 |
| L21 | open | no | single | MAJOR | SA-5 | t3-1 |
| L22 | open | no | single | MAJOR | 122, WC-2 | t3-2 |

## Blocking findings

### L1

#### L1.t1b-1 (F1)

- claim: P1 scope and AC-1.1 require the flag, section and contract in all 37 commands while the phase column and P1 command list give P1 only 13, so AC-1.1 cannot pass or P1 pre-empts the D2-D4 decisions.
- anchor: "the `--unattended` flag accepted by every command in sections 3.1 and 3.2 (a no-op where a command has no gate)"
- anchor2: "every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml`"

#### L1.t1b-1 (F2)

- claim: WC-4 places the contract in a directory but tdd, init-lite and spec-panel take a file as output, so the contract location is a guess and two workers can share one file.
- anchor: "where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`)"
- anchor2: "a precise component prompt, not a bare topic; `--output <file>`"

#### L1.t1b-1 (F3)

- claim: A worker or coordinator that derives the adversarial contract path from WC-4 looks one directory too high and reports a successful run as failed.
- anchor: "Fix the contract filename to `<output>/adversarial/return-contract.yaml` (P1)"
- anchor2: "means the WC-4 file `<output-dir>/return-contract.yaml`"

#### L1.t1b-1 (F4)

- claim: An empty, truncated or unknown-status contract falls into the otherwise branch and is reported succeeded, and the contract has no verdict field for FAIL audits.
- anchor: "`--outcome succeeded` otherwise, including `partial` and including an audit whose verdict is FAIL"

#### L1.t1b-1 (F5)

- claim: In Phase 0 step 3 still demands a WC-4 contract path that none of the three smoke commands writes, and a failure there reopens section 1.
- anchor: "steps 1-3 and 5-7 pass; step 4 uses the command's existing report file, since the contract arrives in P1"
- anchor2: "its report path is the WC-4 contract path"

#### L1.t1b-1 (F6)

- claim: A retry in the same directory without a resume flag starts fresh over the earlier output, and an old contract that is never reset can be read as the retry's result.
- anchor: "A retry worker (`worker-start --retry-of`) must not corrupt the first attempt's output."
- anchor2: "starts fresh, no `[Y/n]` in the transcript, contract written"

#### L1.t1b-1 (F7)

- claim: A worker that takes the permitted ask path sends no worker_done, so AC-2.2 fails on allowed behaviour, and the limit 'once' is undefined.
- anchor: "the session may instead ask the coordinator once with the preamble's `ask` command"
- anchor2: "`worker_done --outcome failed`; contract `status: blocked` with a non-empty `blocked_question`"

#### L1.t1b-1 (F9)

- claim: Several rows rely on an authorising flag that does not exist, and 'paid external run' is undefined, so WC-9 cannot be applied as written.
- anchor: "It turns on only through the command's own explicit flag written in the brief."
- anchor2: "EXEMPT `commit`/`push` refused unless authorized (WC-9)"

#### L1.t1b-1 (F11)

- claim: WC-11 forbids shared files while rows accept fixed paths and timestamp keys, and the one-at-a-time constraint is missing from what the coordinator owes.
- anchor: "Two workers in one worktree must never write the same file."
- anchor2: "output dir is fixed, so one audit per worktree at a time (WC-11)"

#### L1.t1b-1 (F12)

- claim: No requirement covers the worker's own tool-permission prompts, which stall like AskUserQuestion and show only as agentWait.
- anchor: "Nothing in the launch path (wrapper, hook, startup command) may wait on a person before Claude's input box is ready."

#### L1.t1b-1 (F13)

- claim: Existing status words may conflict with the fixed four-value set, there is no contract version, and blocked shares a word with Orca's Task status.
- anchor: "Commands that already write a contract keep their fields and add the missing ones."
- anchor2: "mapped to Orca's two outcomes in WC-5"

#### L1.t1b-1 (F17)

- claim: P1 is labelled no-gate yet lists commands that refuse a mode, and run-scoped README rule 31 is cited as a product reason.
- anchor: "P1. Report files and commands with no gate"
- anchor2: "per-command outward actions in column (f) of the inventories"

#### L1.t2-1 (F2)

- claim: The load row and P1 give no contract and only a usage line, so AC-1.1 cannot pass for load.
- anchor: "none (see note) | n/a | none: use it as a step inside another worker's brief"
- anchor2: "every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml`"

#### L1.t2-1 (F7)

- claim: Nothing requires a unique output directory per Task, so two Tasks given one directory overwrite each other's contract.
- anchor: "where `<output-dir>` is the directory the coordinator passed"
- anchor2: "Two workers in one worktree must never write the same file."

#### L1.t2-1 (F8)

- claim: After an answered ask, a fresh-dir re-run writes another directory, and the spec does not say which contract the worker reports.
- anchor: "then re-invoke or resume the command with the answer as a flag"
- anchor2: "writes each run into a fresh output directory so a re-run starts clean"

#### L1.t2-1 (F10)

- claim: Two code-editing workers in one worktree can break each other's builds without writing the same file, and no rule covers it.
- anchor: "the worktree placement (`CAPS:115`)"
- anchor2: "Two workers in one worktree must never write the same file."

#### L1.t2-1 (F11)

- claim: SA-1 freezes every prompt without --unattended, but WC-1 changes the launch prompt, and the spec does not say where that prompt lives.
- anchor: "Without `--unattended`, every prompt, approval gate, default flag value, output path and outward default stays as it is today"
- anchor2: "Any such prompt must fall back on its own well inside the readiness limit"

#### L1.t2-1 (F12)

- claim: Existing contract status values are not mapped to the four-value set, and a missing or other status has no outcome.
- anchor: "Commands that already write a contract keep their fields and add the missing ones."
- anchor2: "`status` (one of `succeeded`, `partial`, `failed`, `blocked`)"

#### L1.t2-1 (F16)

- claim: WC-4 states as fact what the spec's own UNVERIFIED item 3 lists as unknown.
- anchor: "Orca does not check the file, so the coordinator opens it."

#### L1.t2-1 (F17)

- claim: The output flag is named three ways and is sometimes a file, sometimes a directory.
- anchor: "(`--output` / `--output-dir`)"
- anchor2: "`--output <file>`"

#### L1.t2-1 (F22)

- claim: A stall is visible through agentWait, so calling it invisible overstates the evidence.
- anchor: "so a stall is invisible"

#### L1.t3-1 (F1)

- claim: WC-4 requires a report path known before dispatch, but workflow, research and init-lite rows give paths that are generated, file-valued or undefined.
- anchor: "One report file, known before dispatch, written on every outcome."
- anchor2: "contract naming the generated `claudedocs/research_*.md` path"

#### L1.t3-1 (F2)

- claim: Section 3.1 says ready commands change only by small fixes, but P1 and AC-1.1 require the unattended flag and section in each of them.
- anchor: "The only command changes are the small fixes in the last column."
- anchor2: "the `--unattended` flag accepted by every command in sections 3.1 and 3.2"

#### L1.t3-1 (F5)

- claim: An unknown, mis-cased or empty report status maps to succeeded by the otherwise rule, so a failed run is reported as done.
- anchor: "`--outcome succeeded` otherwise, including `partial`"
- anchor2: "Commands that already write a contract keep their fields and add the missing ones."

#### L1.t3-1 (F6)

- claim: E3 cites a skill-direct worker contract as evidence, while section 1.4 and UNVERIFIED 1 say no direct-route run was observed.
- anchor: "The only end-to-end proof is the PR #329 run"
- anchor2: "invocation_method: \"skill-direct\""

#### L1.t3-1 (F12)

- claim: Ask resumption and the stall wait have no bound and no escalation rule.
- anchor: "On an `ask` timeout it resumes the same message ID and never creates a duplicate."
- anchor2: "is a silent stall with no `worker_done`"

#### L1.t3-1 (F13)

- claim: Fixed default paths for index-repo and init-lite let two workers in one worktree overwrite each other's output.
- anchor: "Default output paths carry a timestamp or the slug the coordinator passes"
- anchor2: "`PROJECT_INDEX.md` (location implied)"

#### L1.t3-1 (F14)

- claim: WC-1 has no owning phase or check, and WC-3, WC-6, WC-10 (cli-eval) and WC-11 have no acceptance check.
- anchor: "Launch setup, not commands"
- anchor2: "7.2 live check on each P1 command with `--unattended --output <dir>`"

#### L1.t3-1 (F20)

- claim: Stated as fact, but its own evidence marks Orca's check UNVERIFIED.
- anchor: "Orca does not check the file, so the coordinator opens it."

#### L1.t3-2 (F1)

- claim: A correct P0 run of troubleshoot or workflow fails step 4, because REPORT.md is not YAML and the workflow contract lists no command key (INV-B:242, INV-B:272).
- anchor: "assert d['status'] in {'succeeded','partial','failed','blocked'}; assert d['command']"
- anchor2: "step 4 uses the command's existing report file, since the contract arrives in P1."

#### L1.t3-2 (F2)

- claim: AC-1.1 demands the section in all 37 commands of 3.1-3.2, but P1 covers 13 and the section 3 intro gives it only to changed commands, so P1 cannot pass as written.
- anchor: "the test asserts that every command in sections 3.1-3.2 has a `## Unattended mode` section"
- anchor2: "Every changed command also gains the `## Unattended mode` section"

#### L1.t3-2 (F4)

- claim: A retry of init-lite with the same --output file overwrites the first attempt's report, which WC-6 forbids.
- anchor: "Re-run overwrites its marked report"
- anchor2: "must not corrupt the first attempt's output"

#### L1.t3-2 (F5)

- claim: Two index-repo workers in one worktree both write the fixed default PROJECT_INDEX.md, which WC-11 forbids, yet the spec ranks index-repo ready with brief flags none.
- anchor: "Default output paths carry a timestamp or the slug the coordinator passes"
- anchor2: "`PROJECT_INDEX.md` (location implied)"

#### L1.t3-2 (F7)

- claim: AC-0.4 says the no-Agent-tool-wrapper condition is verified in step 5, but step 5 passes on the absence of AskUserQuestion alone, so a subagent-wrapped run passes P0.
- anchor: "no Agent-tool wrapper, verified in the step-5 transcript"
- anchor2: "no `AskUserQuestion` call"

#### L1.t3-2 (F8)

- claim: An empty contract or a misspelt status falls under otherwise and is sent as succeeded, which can release dependent Tasks.
- anchor: "`--outcome succeeded` otherwise, including `partial`"
- anchor2: "`--outcome failed` when the report says `failed` or `blocked`, or no report exists"

#### L1.t3-2 (F9)

- claim: WC-1 assigns the launch path to an owner that no phase or check covers.
- anchor: "Any such prompt must fall back on its own well inside the readiness limit"
- anchor2: "Launch setup, not commands"

#### L1.t3-2 (F11)

- claim: A FAIL audit is sent as succeeded, so dependents can start unless the coordinator reads the report first, which is a process rule rather than a Task rule.
- anchor: "including an audit whose verdict is FAIL (the audit itself succeeded)"

#### L1.t3-2 (F14)

- claim: Step 6 fails any run while another worker or the coordinator has an edit in the shared worktree.
- anchor: "only files under the brief's output directory"
- anchor2: "Two workers in one worktree must never write the same file."

#### L1.t3-2 (F15)

- claim: A worker that blocks in a permitted WC-3 ask may show a non-null agentWait, so step 2 fails a permitted path; the Orca behaviour is UNVERIFIED.
- anchor: "`observation.agentWait` is never non-null"
- anchor2: "the session may instead ask the coordinator once with the preamble's"

#### L1.t3-2 (F16)

- claim: The shared contract has no version and keeps per-command fields, so one file name can carry several schemas.
- anchor: "Commands that already write a contract keep their fields and add the missing ones"

#### L1.t3-2 (F18)

- claim: Ready-today status for adversarial and workflow rests on a contract path and a staging behaviour the spec does not confirm.
- anchor: "These run as workers now if the brief uses the stated flags"
- anchor2: "Fix the contract filename to `<output>/adversarial/return-contract.yaml` (P1)"

#### L1.t3-2 (F19)

- claim: Two cleanup-audit tasks can run in one worktree because no dependency or gate encodes the one-at-a-time rule.
- anchor: "output dir is fixed, so one audit per worktree at a time (WC-11)"

#### L1.t3-2 (F20)

- claim: A command with two unresolved gates has no rule for which question the blocked contract carries.
- anchor: "writes its report with `status: blocked` and the exact question"

### L5

#### L5.t1b-1 (F15)

- claim: AC-C1 scans core files that Phase 0 must fill with Orca text, and its escaped pipes make the grep pattern match nothing when copied.
- anchor: "prints nothing (SA-2, WC-8)"
- anchor2: "add an Orca section to `HOW-WE-WORK.md` and its two mirrored copies"

#### L5.t2-1 (F3)

- claim: As written, the escaped pipe is a literal, so AC-C1 never matches, even on a command that calls orca orchestration; the check passes a violation.
- anchor: "grep -rnE '\\borca(-ide)?[[:space:]]+(orchestration\\|worktree\\|terminal\\|agent)\\b'"

#### L5.t2-1 (F21)

- claim: AC-C1 matches four verbs only, so most orca commands pass the SA-2 check.
- anchor: "No command, skill or agent file runs an `orca` or `orca-ide` command"

#### L5.t3-1 (F3)

- claim: AC-C1 runs in every phase over src/superclaude/core and forbids Orca orchestration text that P0 requires there, so P0 cannot pass.
- anchor: "add an Orca section to `HOW-WE-WORK.md` and its two mirrored copies"
- anchor2: "src/superclaude/agents src/superclaude/core"

#### L5.t3-1 (F4)

- claim: AC-C1 matches only four orca subcommands, so a command running orca-ide status passes; in raw form the escaped alternation matches nothing.
- anchor: "No command, skill or agent file runs an `orca` or `orca-ide` command"
- anchor2: "prints nothing (SA-2, WC-8)"

#### L5.t3-2 (F6)

- claim: The AC-C1 grep uses an escaped alternation in an ERE, matches a literal pipe, and printed nothing on a positive control in the sandbox, so SA-2 is never checked.
- anchor: "(orchestration\\|worktree\\|terminal\\|agent)"

#### L5.t3-2 (F10)

- claim: P0 writes the contract, the routing-guide section and a test file before its smoke runs, which its own rationale says must come first.
- anchor: "the smoke runs test the decision before anything is built on it"

#### L5.t3-2 (F17)

- claim: AC-C1 also scans src/superclaude/core, where P0 adds an Orca section, and no exemption covers it.
- anchor: "src/superclaude/commands src/superclaude/skills src/superclaude/agents src/superclaude/core"
- anchor2: "The only allowed mention of Orca in a changed command"

### L7

#### L7.t2-1 (F1)

- claim: Following step 3 with its 900000 ms timeout leaves 15 minutes between worker-show observations, which step 2 forbids.
- anchor: "ORCA orchestration check --wait --types \"worker_done,escalation,question\" --timeout-ms 900000 --json"
- anchor2: "at least once per 5 minutes"

### L13

#### L13.t2-1 (F18)

- claim: Section 1.1 says changes are limited to the contract, but section 3 and SA-4 include other defect fixes.
- anchor: "What changes in the commands is limited to the worker contract in section 2"

#### L13.t3-2 (F3)

- claim: Section 1.1 limits command changes to the section 2 contract, while section 3 and SA-4 require the explain tools, roadmap, validate-tests and cli-portify edits, so an implementer following 1.1 skips required changes.
- anchor: "What changes in the commands is limited to the worker contract in section 2"
- anchor2: "add Write to its tools (only Read/Grep/Glob, TodoWrite, Task today)"

### L16

#### L16.t3-1 (F7)

- claim: The troubleshoot brief rule allows a --depth deep short-input STOP that asks a person, so a stated brief can stall without worker_done.
- anchor: "Under `--unattended`, the `--depth deep` short-input STOP and the `--fix` offer resolve as blocked (P2)"
- anchor2: "These run as workers now if the brief uses the stated flags"

## Other findings

- L2 (MAJOR, open, overlap): The claim is asserted although the task is passed as a startup argument, and it is missing from the UNVERIFIED list.
- L3 (MAJOR, open, single): WC-1, WC-3, WC-6 and WC-12 have no acceptance check, and WC-10, WC-11 and SA-1 are checked for one or two commands only.
- L4 (MAJOR, open, overlap): The --suite and --post-pr flags are not shown to exist in the inventories, and the no-command-calls-Orca premise and the 43-command scope need a re-check.
- L6 (MAJOR, open, overlap): A 270 s call obeys WC-10 and fails AC-4.3.
- L8 (MINOR, open, overlap): The depth fence covers Orca dispatch; CAPS:155 leaves whether Orca limits subagents UNVERIFIED, so E4 states more than its source.
- L9 (MAJOR, open, single): Heavy in-command fan-out such as cleanup-audit and tdd cannot be split by the coordinator, and no rule covers that case.
- L10 (MAJOR, open, single): The spec does not say what a coordinator-only command does when given --unattended, so it may wait on a person.
- L11 (MAJOR, open, overlap): Unattended reflect auto-accepts remediation, which is the self-approval that D2 forbids for implement; the bounded risk needs a decision.
- L12 (MINOR, open, single): A brief that a person pastes with --unattended silences that person's prompts, so the flag is not a safe sentinel.
- L14 (MINOR, open, single): P4 includes pr-submit although D3 (a) recommends no pr-submit change.
- L15 (MINOR, open, single): AC-1.3 calls a print-mode run a plain session, so it does not test an interactive person's session.
- L17 (MAJOR, open, single): No rule for blocked re-dispatch or for dependents of a partial Task, which Orca settles as complete.
- L18 (MAJOR, open, single): The row requires an explicit --post-pr flag that is not evidenced, while its required-change column says none.
- L19 (MAJOR, open, single): The sentinel token inside quoted prompt text is not excluded, so the cannot-misfire claim is unsupported.
- L20 (MAJOR, open, single): A command run against an install without WORKER-CONTRACT.md has no specified behaviour.
- L21 (MAJOR, open, single): The plugin mirror is not assigned to any phase and no check compares it, so it can drift while verify-sync passes.
- L22 (MAJOR, open, single): No row edits the task skill and no rule says how --unattended reaches nested skills, so tdd keeps its nested ask lines.

## Reviser brief

Blocking finding ids: L1, L5, L7, L13, L16.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
