review: 1 of 3
# Merged review 1 (coordinator script; panel of 4 reviewers)
candidate: /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p13/ab1/runs/b1-r4/ws/.dev/orca-command-refactor/specs/orca-worker-contract-spec.md sha256 d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d
reviewers:
- t1b-1: report /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p13/ab1/runs/b1-r4/ws/.dev/orca-command-refactor/review/round1-t1b-1.md, block ok true
- t2-1: report /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p13/ab1/runs/b1-r4/ws/.dev/orca-command-refactor/review/round1-t2-1.md, block ok false
- t3-1: report /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p13/ab1/runs/b1-r4/ws/.dev/orca-command-refactor/review/round1-t3-1.md, block ok true
- t3-2: report /tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p13/ab1/runs/b1-r4/ws/.dev/orca-command-refactor/review/round1-t3-2.md, block ok true

## Ledger

| lid | status | blocking | confidence | severity | refs | reviewers |
|---|---|---|---|---|---|---|
| L1 | open | yes | overlap | CRITICAL | 2.1, 2.3, 3.1, 3.2, 7.2, AC-0.4, AC-1.1, AC-1.2, AC-2.2, AC-4.3, P0, P1, P2, P3, P4, WC-1, WC-10, WC-12, WC-2, WC-3, WC-4, WC-5, WC-6, WC-7, WC-9 | t1b-1, t2-1, t3-1, t3-2 |
| L2 | open | yes | single | MAJOR | AC-0.3, SA-1, SA-4 | t1b-1 |
| L3 | open | no | overlap | MAJOR | - | t1b-1, t3-1, t3-2 |
| L4 | open | yes | overlap | MAJOR | P0, SA-2, WC-8 | t1b-1, t2-1, t3-1, t3-2 |
| L5 | open | yes | single | MAJOR | AC-1.2, AC-2.3, P1, P2 | t2-1 |
| L6 | open | no | overlap | MAJOR | - | t2-1, t3-1, t3-2 |
| L7 | open | no | overlap | MAJOR | - | t2-1, t3-2 |
| L8 | open | no | overlap | MAJOR | 1.1, 3.2, SA-3, SA-4 | t3-1, t3-2 |
| L9 | open | no | single | MAJOR | WC-9 | t3-1 |
| L10 | open | no | single | MAJOR | 2.1 | t3-1 |
| L11 | open | no | single | MAJOR | SA-5 | t3-1 |
| L12 | open | no | single | MINOR | 4 | t3-1 |
| L13 | open | no | single | MAJOR | 2.3, P0 | t3-1 |
| L14 | open | no | single | MAJOR | 1.4, 3.1 | t3-2 |
| L15 | open | no | single | MAJOR | SA-6 | t3-2 |
| L16 | open | no | single | MINOR | 3.2 | t3-2 |

## Blocking findings

### L1

#### L1.t1b-1 (F1)

- claim: WC-4 builds the contract path under a directory taken from --output, but tdd and init-lite pass --output as a file, so the contract is written under a regular file and the AC-2.2 contract check cannot pass.
- anchor: "`<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`)"
- anchor2: "a precise component prompt, not a bare topic; `--output <file>`"

#### L1.t1b-1 (F2)

- claim: AC-1.1 forces a return-contract section onto /sc:load while its row and the Decisions table say it gets no report file.
- anchor: "every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml`"
- anchor2: "none: use it as a step inside another worker's brief, not as its own Task"

#### L1.t1b-1 (F3)

- claim: After P1, commands whose gates convert only in P2-P4 accept --unattended yet still prompt, so a worker stalls silently and no P1 check catches it.
- anchor: "the `--unattended` flag accepted by every command in sections 3.1 and 3.2"
- anchor2: "Under `--unattended` the command never calls `AskUserQuestion`"

#### L1.t1b-1 (M1)

- claim: A wait of 4 to 5 minutes passes WC-10 but fails AC-4.3.
- anchor: "must be split into waits of at most 4 minutes"
- anchor2: "no single tool call exceeds 240 s"

#### L1.t1b-1 (M2)

- claim: Order of ask, blocked contract and worker_done is not fixed.
- anchor: "the session may instead ask the coordinator once with the preamble's `ask` command"

#### L1.t1b-1 (M3)

- claim: Behavior with no output directory under --unattended is not stated.
- anchor: "where `<output-dir>` is the directory the coordinator passed"

#### L1.t1b-1 (M4)

- claim: The workflow contract path contains a generated id, so it is not known before dispatch.
- anchor: "One report file, known before dispatch, written on every outcome."
- anchor2: "`.dev/tasks/to-do/<id>/return-contract.yaml`"

#### L1.t1b-1 (M6)

- claim: No contract version or mapping from existing contracts' status values.
- anchor: "`status` (one of `succeeded`, `partial`, `failed`, `blocked`)"

#### L1.t2-1 (F1)

- claim: An implementer who follows WC-3 as written re-invokes /sc:implement with the coordinator's answer as the Ruling, which the qa.md:238 rule forbids while D2 is open.
- anchor: "the session may instead ask the coordinator once with the preamble's `ask` command, wait, then re-invoke or resume the command with the answer as a flag"
- anchor2: "the Ruling rule itself is unchanged (see open decision D2)"

#### L1.t2-1 (F2)

- claim: An implementer who follows WC-4 as written cannot name a pre-dispatch contract path for tdd (file output), workflow (per-run id) or adversarial (subdirectory), which the 2.3 rule requires.
- anchor: "where `<output-dir>` is the directory the coordinator passed"
- anchor2: "Fix the contract filename to `<output>/adversarial/return-contract.yaml`"

#### L1.t2-1 (F4)

- claim: An implementer who runs AC-1.1 at the end of P1 gets failures for commands P2-P4 have not yet edited and for the three commands that have no contract.
- anchor: "every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml`"
- anchor2: "the `--unattended` flag accepted by every command in sections 3.1 and 3.2"

#### L1.t2-1 (F6)

- claim: A partial deliverable can settle as succeeded and make its dependents ready, which harms only if the coordinator skips the contract.
- anchor: "`--outcome succeeded` otherwise, including `partial`"
- anchor2: "A partial run left a usable deliverable"

#### L1.t2-1 (F7)

- claim: The spec gives no rule for choosing the fresh directory on a retry, so the pre-dispatch report path cannot be known for a retry.
- anchor: "A command either resumes from its on-disk state when given its resume flag, or, if it has none, writes each run into a fresh output directory so a re-run starts clean"
- anchor2: "so the report path is known before dispatch (WC-4)"

#### L1.t2-1 (F8)

- claim: A contract with a missing or unknown status falls into the success branch, which the spec leaves undefined.
- anchor: "`--outcome failed` when the report says `failed` or `blocked`, or no report exists"
- anchor2: "`--outcome succeeded` otherwise, including `partial`"

#### L1.t2-1 (F10)

- claim: AC-0.4 says step 5 verifies the absence of an Agent-tool wrapper, but step 5 only searches for AskUserQuestion.
- anchor: "each run directly by the worker (no Agent-tool wrapper, verified in the step-5 transcript)"
- anchor2: "search the transcript for `AskUserQuestion`"

#### L1.t2-1 (F12)

- claim: A single tool call of exactly 300 s is neither split nor covered by a heartbeat, so the 5-minute cadence has a gap at the boundary.
- anchor: "A command step that blocks a single tool call for longer than 5 minutes"
- anchor2: "The worker sends a heartbeat every 5 minutes while working."

#### L1.t2-1 (F13)

- claim: The hardcoded template path is a required change that no phase schedules.
- anchor: "dispatch only inside an IronClaude checkout (hardcoded template path)"
- anchor2: "Each default-on gate resolves per its section 3 row; WC-10 wait splitting for cli-eval."

#### L1.t3-1 (F1)

- claim: An implementer who follows WC-3 relays a coordinator answer as the implement Ruling, which the D2(a) recommendation and the rule quoted at INV-A:66 forbid.
- anchor: "then re-invoke or resume the command with the answer as a flag"
- anchor2: "The worker stops, writes the halt to its ledger and contract, and ends `failed`."

#### L1.t3-1 (F2)

- claim: The order of ask, resume and worker_done is undefined, so a worker can send failed first and lose the Dispatch the resume needs.
- anchor: "the session may instead ask the coordinator once with the preamble's"
- anchor2: "`--outcome failed` when the report says `failed` or `blocked`"

#### L1.t3-1 (F3)

- claim: A worker whose permission mode prompts on a non-allowlisted tool call parks on a person-only prompt that WC-2 does not cover.
- anchor: "never calls `AskUserQuestion`, never ends its turn on a chat question"
- anchor2: "so a command run by a worker has the same tools as a command a person runs"

#### L1.t3-1 (F5)

- claim: Brainstorm and init-lite are in no phase, so the flag and init-lite's contract are never added.
- anchor: "the `--unattended` flag accepted by every command in sections 3.1 and 3.2"

#### L1.t3-1 (F6)

- claim: A retry of init-lite with the same --output overwrites the first attempt's report, which WC-6 forbids, while the row still reads ready.
- anchor: "Re-run overwrites its marked report"
- anchor2: "must not corrupt the first attempt"

#### L1.t3-1 (F7)

- claim: Commands with fixed or absent output flags have no defined directory for return-contract.yaml.
- anchor: "is the directory the coordinator passed"

#### L1.t3-1 (F8)

- claim: Orca settles a partial or FAIL-verdict Task as completed, so ready dependents start on invalid input.
- anchor: "A partial run left a usable deliverable"
- anchor2: "including an audit whose verdict is FAIL (the audit itself succeeded)"

#### L1.t3-1 (F9)

- claim: A single Agent-tool fan-out call can block past the 5-minute heartbeat with no split rule.
- anchor: "A command step that blocks a single tool call for longer than 5 minutes"

#### L1.t3-1 (F13)

- claim: A fenced attempt still writing its contract can overwrite the retry's contract with a stale status.
- anchor: "if `check` returns `consumer_fenced` it stops without sending `worker_done`"
- anchor2: "the command writes `<output-dir>/return-contract.yaml`"

#### L1.t3-1 (F15)

- claim: A malformed, missing or unknown-status contract has no outcome mapping, so the coordinator can read an unsafe status.
- anchor: "It is written on success, failure, blocked and partial outcomes"
- anchor2: "carries at least"

#### L1.t3-1 (F16)

- claim: A coordinator that retries a blocked Task with an unchanged brief repeats the gate without limit, since Orca never trips a breaker on failed reports.
- anchor: "The contract only works if the brief carries what the command would otherwise ask a person"

#### L1.t3-1 (F18)

- claim: A gate can be mis-resolved while AC-1.1 still passes, since the test checks only that the heading exists.
- anchor: "the test asserts that every command in sections 3.1-3.2 has"

#### L1.t3-1 (F19)

- claim: A worker that reads an empty check as consumer_fenced stops without sending worker_done while still live.
- anchor: "The worker runs `check` at natural checkpoints and once before `worker_done`"

#### L1.t3-2 (F1)

- claim: AC-0.4 requires steps 1-3 to pass in P0, but step 3 requires the WC-4 contract path and the contract arrives only in P1, so a P0 troubleshoot run that reports REPORT.md cannot pass.
- anchor: "its report path is the WC-4 contract path"
- anchor2: "step 4 uses the command's existing report file, since the contract arrives in P1"

#### L1.t3-2 (M1)

- claim: WC-3 requires an answer flag that no section 3 row defines, and the step 2 check fails a worker parked on an ask.
- anchor: "re-invoke or resume the command with the answer as a flag"
- anchor2: "a non-null value means the worker is parked on a prompt only a person can answer"

#### L1.t3-2 (M2)

- claim: An unattended run without --output has no defined contract path, and nothing refuses it.
- anchor: "In unattended mode the command writes"

#### L1.t3-2 (M3)

- claim: The fixed WC-4 path and the WC-6 fresh directory cannot both hold for a retry, and a retry in a reused directory can report a stale succeeded outcome.
- anchor: "writes each run into a fresh output directory so a re-run starts clean"
- anchor2: "is the directory the coordinator passed"

#### L1.t3-2 (M6)

- claim: The 3.2 rows have no required-flags column, so a coordinator cannot build the brief the section requires.
- anchor: "every flag section 3 lists as required"

#### L1.t3-2 (M11)

- claim: The shared installed contract has no version, no fallback when the install is missing, and no rule for existing contract versions.
- anchor: "one shared document, proposed as"
- anchor2: "Commands that already write a contract keep their fields and add the missing ones"

#### L1.t3-2 (M12)

- claim: Five worker-session rules have no repo artifact and the brief template does not require the coordinator to restate them.
- anchor: "What the coordinator owes each worker"

#### L1.t3-2 (M13)

- claim: A mid-run tool-permission prompt stalls a worker and is treated as healthy, and neither WC-1 nor WC-2 covers it.
- anchor: "No person-blocking step in unattended mode."
- anchor2: "Nothing in the launch path"

#### L1.t3-2 (M16)

- claim: The readiness fallback is not quantified, so a fallback of 50 s passes the wording and fails in practice.
- anchor: "well inside the readiness limit"

#### L1.t3-2 (N1)

- claim: The contract need not be fully written before worker_done, so a reader can see a partial file.
- anchor: "The worker passes the contract path as"

#### L1.t3-2 (N2)

- claim: A single wait of 4.5 minutes or exactly 5 minutes is not assigned to either rule.
- anchor: "must be split into waits of at most 4 minutes"

#### L1.t3-2 (N3)

- claim: partial maps to succeeded, so a coordinator reading only Orca's outcome cannot see partial runs.
- anchor: "A partial run left a usable deliverable"

#### L1.t3-2 (N6)

- claim: Between P1 and P2 a gate command accepts --unattended and still prompts, so an early dispatch stalls.
- anchor: "the `--unattended` flag accepted by every command in sections 3.1 and 3.2"

### L2

#### L2.t1b-1 (F4)

- claim: The additive-edit check ignores deleted lines that begin with a dash because diff shows a deleted '- b' as '-- b', so an implementer deleting a bullet or --- line passes AC-C5.
- anchor: "git diff -U0 master...HEAD -- src/superclaude/commands/<name>.md \\| grep -E '^-[^-]'"

### L4

#### L4.t1b-1 (M7)

- claim: AC-C1 scans core/ where P0 adds Orca text and misses orca status/open/skills.
- anchor: "prints nothing (SA-2, WC-8)"

#### L4.t2-1 (F5)

- claim: An implementer who runs AC-C1 as written sees no output for a real orca orchestration call, because the escaped pipes are literal in grep -E, so the SA-2 check passes falsely.
- anchor: "(orchestration\\|worktree\\|terminal\\|agent)"
- anchor2: "grep -v '^src/superclaude/skills/ccsession-tag/'"

#### L4.t3-1 (F12)

- claim: AC-C1 as written never matches, so it passes whatever the commands contain.
- anchor: "prints nothing (SA-2, WC-8)"

#### L4.t3-2 (M8)

- claim: The AC-C1 pattern is a literal pipe when copied verbatim so it can pass without checking, and once it works its scope fails the contract file that SA-2 allows to mention Orca.
- anchor: "grep -v '^src/superclaude/skills/ccsession-tag/'"
- anchor2: "The only allowed mention of Orca in a changed command"

### L5

#### L5.t2-1 (F3)

- claim: An implementer who follows the phase table builds troubleshoot, tdd and release-split workers with no contract, so AC-2.3 fails on 7.2 step 4 for them.
- anchor: "the worker reports the named file until Phase 1 adds the contract"
- anchor2: "7.2 passes with `--outcome succeeded`"

## Other findings

- L3 (MAJOR, open, overlap): The row may be stale against a command definition that already has --output and --report-dir.
- L6 (MAJOR, open, overlap): E2 asserts tool parity that the cited evidence (top-level session only) does not show.
- L7 (MAJOR, open, overlap): The D1 example passes --output to troubleshoot, but section 3.1 lists no output flag for it and the inventory names only a default folder.
- L8 (MAJOR, open, overlap): A reader who trusts 1.1 underestimates the 27 command edits that change gate behaviour and drift.
- L9 (MAJOR, open, single): An unattended reflect or cleanup worker moves or edits local files with no rule limiting them.
- L10 (MAJOR, open, single): Quoted text containing the token switches unattended mode on, which the claim that it cannot misfire denies.
- L11 (MAJOR, open, single): Section 7 lets a new Unattended-mode section ship with a hard-coded src/superclaude path because no check catches it.
- L12 (MINOR, open, single): The git row uses a run-level constraint as command evidence.
- L13 (MAJOR, open, single): The promised brief template is not specified beyond the list in 2.3, so the coordinator's briefs will differ per run.
- L14 (MAJOR, open, single): The ready-today claim overstates evidence the spec itself says is missing, and tdd can stall mid-run on a /task question.
- L15 (MAJOR, open, single): Unattended reflect and tasklist auto-accept remediation by the same agent that found the defects, which D2's rationale forbids for Rulings, and the spec does not decide it.
- L16 (MINOR, open, single): pr-submit is counted as a needs-change worker while the recommended D3 makes it coordinator-only.

## Reviser brief

Blocking finding ids: L1, L2, L4, L5.

Rules for the reviser (restating the Review Loop's Reviser contract): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, with the bytes added and deleted per finding id.

verdict: FAIL
