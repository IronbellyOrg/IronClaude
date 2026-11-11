review: 1 of 3

# Whole-document audit: orca-worker-contract-spec.md (first review, critique mode)

Command run: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture`. This is a labelled whole-document audit of the final spec: a first review of the whole document, per the FIRST-REVIEW prompt in `~/.claude/rules/prompts/document_review_loop_prompts.md:27-32`.

## Header
- candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (285 lines), sha256 `06020a7826f57dcd282a3b34507468f8ee1a370773f0665ff1254c475d92b7fd`
- baseline: not given. `--re-review` not given. This is a first review of the full document, so no `baseline: missing` note applies (command.md:258).
- reviewer model actually used: Sonnet 5.5 (`claude-sonnet-5-5`)
- panel (command.md:131-147, 101-113): Wiegers (lead), Adzic, Cockburn for requirements; Fowler (lead), Nygard, Newman, Hohpe for architecture; Whittaker (adversarial, always active, command.md:83); Crispin and Gregory were consulted only for acceptance-check completeness.
- grading: by consequence (command.md:259). Blocking needs a sentence that holds with no further assumption (prompts file:31).

## Coverage
- Read in full: the candidate (spec:1-285), `README.md`, `inventory/orca-capabilities.md:40-188`, `inventory/commands-a.md:1-34, 56-120`, `inventory/commands-b.md` rows for pr-submit, reflect, tasklist, research, task, test, troubleshoot, load and lines 270-323.
- Checked against the inventories: every `INV-A:N`, `INV-B:N` and `CAPS:N` citation I sampled (about 45) resolves to the claimed content. The 10 / 27 / 6 split is internally consistent: section 3.1 has 10 rows, section 3.2 has 27, section 4 has 6, 43 in total. The phase lists in section 6 partition exactly: P1 15 (6 ready and 9 changed), P2 15 (4 ready and 11 changed), P3 4, P4 3, 37 in total.
- UNVERIFIED (no file in the workspace to check): every citation to `src/`, `.claude`, `CLAUDE.md`, `.dev/evals/ccsession-orca-e2e-20261026/EVIDENCE.md`, `.dev/codegraph-migration/...` and the greps in spec:25. This includes spec:11, which claims 11 locations were re-read, and spec:285, which claims a 340-citation check found 9 defects that were fixed. I accept the inventories' own statements of what they read (`INV-A:106`, `INV-B:320`) only as claims.
- Not covered: the `--focus correctness` outputs (State Variable Registry) were not requested.

=== REQUIREMENTS ANALYSIS ===

### F1 (blocking, MAJOR, Wiegers + Adzic): AC-1.2 and WC-4 cannot pass for commands that have no output flag
- Stated texts. AC-1.2 (spec:196) runs the live check "on each P1 command other than `load` with `--unattended --output <dir>`". WC-4 (spec:62) puts the contract at `<output-dir>/return-contract.yaml`, "the directory the coordinator passed". But the section 3.1 rows for two P1 commands give no such flag: cleanup-audit "output dir is fixed" (spec:85) and index-repo "State the output location" (spec:86). Neither row adds `--output`, and neither gives a contract path, even though WC-4 says only adversarial and workflow have their own paths. The troubleshoot row is the same: WC-6 says its "timestamped default directory" is "the output path the brief names" and that "the coordinator makes [it] new for every attempt" (spec:64), yet `cmd/troubleshoot.md:56` has no output flag (`INV-B:242`) and a default directory the coordinator cannot name, so WC-4's "known before dispatch" fails (spec:62, 73).
- Sentence. An implementer who follows the stated text as written builds cleanup-audit and index-repo with `--unattended` and a contract at "`<output-dir>`", and the AC-1.2 run `/sc:cleanup-audit --unattended --output <dir>` is rejected or ignored because no such flag exists. The acceptance criterion cannot pass for those commands, and the troubleshoot contract has no defined location.
- Evidence: spec:62, 64, 85, 86, 91, 196; `INV-B:242` ("default `.dev/troubleshoot/<slug>-<timestamp>/`, `cmd/troubleshoot.md:56`"; `return-contract.yaml` only with `--caller task-unified`).
- Recommendation: for each of cleanup-audit, index-repo and troubleshoot, state the contract path (a fixed one such as `.claude-audit/return-contract.yaml`, or add an output flag), and narrow AC-1.2 and AC-2.2 to "`--output <dir>` where the command accepts it". Prefer narrowing over adding. Priority High. Quality impact: Testability and Consistency.

### F2 (blocking, MAJOR, Nygard + Newman): WC-3's answer path leaves the Task DAG stuck
- Stated texts. WC-3 (spec:61): a blocked worker ends `failed`, and "the coordinator answers by starting a new Task whose brief carries the answer". Section 4 and spec:136 tell the coordinator to build the work as a Task DAG with `task-create --deps`. The spec's own cited Orca facts say a failed Task keeps its dependents blocked until a `--retry-of` replacement completes it (`CAPS:90`; `[G:recovery]` 142-144), and a Task that cannot start returns `task_not_startable` (`CAPS:88`). WC-6 (spec:64) uses `--retry-of` for retries, but WC-3 does not.
- Sentence. An implementer who follows WC-3 as written builds a coordinator that answers every blocked worker with a new, unrelated Task, and that is wrong because the original Task stays `failed`, so every Task that depends on it never becomes ready (`CAPS:88, 90`).
- Evidence: spec:61, 64, 136; `CAPS:80, 88, 90, 116`.
- Recommendation: change WC-3 to "starts a replacement worker with `worker-start --task <the blocked task> --retry-of <dispatch_id>` whose brief carries the answer", keeping WC-6's new-output-path rule, and say that a replacement for a Task with dependents must use `--retry-of`. Priority High. Quality impact: Consistency, Completeness.

Findings F1 and F2 are the only blocking findings. Everything below is Medium or minor and never fails the review (command.md:259).

=== ARCHITECTURE ANALYSIS ===

No blocking architectural defect. The decision (Orca on top, commands as units) is supported by `CAPS:97-103, 155-161`, and the rejected alternative (section 1.3 R1-R5) is cited line by line. Fowler's single-responsibility check passes: the shared rules sit in one core file (spec:52, 264), and each command lists only its own gate resolutions. Hohpe: the message pattern is clean (one `worker_done`, a report path as a pointer, `CAPS:79`; the coordinator opens the file, spec:73). The Medium points follow.

## Whittaker adversarial section (command.md:76-82)
Each finding uses the FR-3 template.

- I can break this specification by **Sequence Attack**. The invariant at **WC-4/WC-6 (spec:62, 64)**, "written on every outcome" with a new path per attempt, fails when **a command with a fixed output path (cleanup-audit `.claude-audit/`, index-repo `PROJECT_INDEX.md`, spec:69, 85-86) is re-run after a crash**. Concrete attack: attempt 1 writes `status: succeeded`; attempt 2 starts on the same fixed path and dies before overwriting; the worker reads the stale file and reports `succeeded`. The spec relies on "one such worker per worktree at a time" (WC-11) and "no readable report" (WC-5) but never requires deleting a prior contract at start. Severity MAJOR but the sentence needs a crash and a missing delete rule, so it is Medium (M4).
- I can break this specification by **Zero/Empty Attack**. The invariant at **section 4 (spec:128)**, "get no `--unattended` mode", fails when **a brief passes `--unattended` to a section-4 command**. Concrete attack: coordinator writes `/sc:git commit --unattended`; the spec defines no behaviour (refuse, ignore, or act). Medium (M3).
- I can break this specification by **Sentinel Collision Attack**. WC-5 (spec:63) treats a non-empty `blocked_question` as failure even when `status` is `succeeded`; a command that quotes a question in a report field as data collides with the control signal. Minor.
- **Accumulation/Divergence**: WC-5 maps `partial` to `succeeded` (spec:63, 263). Orca then settles the Task as completed (`CAPS:77`) and its dependents become ready. The spec relies on the coordinator opening the report first (spec:73). That holds only if the coordinator starts dependents itself, which `CAPS:92` supports. Minor note.

## Guard Condition Boundary Table
Guards found: the WC-5 status mapping, the WC-4 output path, the WC-10 wait split, task's confidence threshold, the circuit breaker, the nesting depth, and the `--unattended` switch. Classes left out are explained in the lines under the table.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|-------|----------|-----------------|----------------|--------------|-------------------|--------|
| WC-5 status check | spec:63 | Zero/Empty | no report file, `status` missing | true | outcome `failed` | OK |
| WC-5 status check | spec:63 | One/Minimal | `status: partial` | true | outcome `succeeded`, body says partial | OK |
| WC-5 status check | spec:63 | Typical | `status: succeeded` | true | outcome `succeeded` | OK |
| WC-5 status check | spec:63 | Sentinel Value Match | `status: succeeded` with non-empty `blocked_question` | true | outcome `failed` | OK |
| WC-5 status check | spec:63, 64, 85-86 | Legitimate Edge Case | stale contract from an earlier attempt at a fixed path | false | not specified | GAP (M4, Medium) |
| WC-4 output path | spec:62 | Zero/Empty | output path missing | true | command writes nothing, worker ends `failed` (yet "written on every outcome" in the same row) | OK (wording conflict noted in M2) |
| WC-4 output path | spec:62, 85-86, 91 | Legitimate Edge Case | command has no output flag (cleanup-audit, index-repo, troubleshoot, research, task, save) | false | no contract location stated | GAP (F1 blocking for P1 commands and troubleshoot; M2 for the rest) |
| WC-10 wait split | spec:68 | Typical | a 3-minute wait | false | no split needed | OK |
| WC-10 wait split | spec:68 | Maximum/Overflow | a single tool call over 5 minutes | true | split into waits of at most 4 minutes | OK |
| WC-10 wait split | spec:114, 283 | Legitimate Edge Case | pr-submit poll script run time | unknown | "UNVERIFIED", re-check at P4 | GAP (acknowledged, Medium) |
| task confidence | spec:121 | Typical | 0.69 | true | blocked | OK |
| task confidence | spec:121 | Legitimate Edge Case | exactly 0.70 | false | inherited from `cmd/task.md:93` ("below 0.70") | OK |
| circuit breaker | spec:61, 64 | Maximum/Overflow | third consecutive failed start of a Task | true | Task failed (`CAPS:116`); WC-3 gives no path other than a new Task | GAP (F2, blocking) |
| nesting depth | spec:33, 66 | Maximum/Overflow | a command calls `worker-start` at depth 1 | true | refused with `nested_worker_depth_exceeded`; WC-8 forbids the call | OK |
| `--unattended` switch | spec:51, 128 | Zero/Empty | flag absent | false | standalone behaviour unchanged (SA-1) | OK |
| `--unattended` switch | spec:128 | Legitimate Edge Case | flag passed to a section-4 command | unknown | not specified | GAP (M3, Medium) |

Classes left out, with the one-line reason: One/Minimal and Zero/Empty for the wait split and the circuit breaker (a wait of zero or a count of zero cannot trigger either guard); Sentinel Value Match for the nesting depth and the confidence threshold (no sentinel value is defined for either); Maximum/Overflow for the WC-5 status check (the status set is a closed list of four values).
FR-10 completeness: every guard listed has a row or a reason. FR-8 and FR-9 grading: the three GAP rows that name a concrete wrong outcome are F1 and F2; the rest are Medium and appear under follow-up candidates.

## Quantity Flow Diagram (Pipeline Dimensional Analysis, command.md:360-394)
The only multi-stage count flow is the command partition. No stage assumes count conservation, so there is no FR-19 mismatch.

```text
[Source: 43 commands (21 INV-A:3 + 22 INV-B:3)] --> [Stage 1: verdict split] --> [10 ready + 27 needs-change + 6 coordinator-only = 43]
                                                                                    |
                                                                                    v
                                                    [Stage 2: phase partition: 37 workers = P1 15 + P2 15 + P3 4 + P4 3]
                                                                                    |
                                                                                    v
                                        [Consumer: section 7 checks per phase; 6 coordinator-only never reach a phase]
```

=== FOLLOW-UP CANDIDATES (Medium and minor) ===
These never trigger a revision and never fail a review (command.md:259). Per command.md:260, the session that ran this review asks the user once whether to open an issue for them; this worker cannot ask and creates none. Pending: the coordinator asks.

Medium
- M1 (Medium, Wiegers): WC-3 ends every gate as `failed` and routes the answer through a new brief, while Orca's own guidance says to use the preamble `ask` and to "resume the same message ID" (`CAPS:61, 58-60`). No row in Decisions (spec:255-269) records why `ask` was rejected for command gates, and `INV-A:96` proposed "off switch or `ask`". A reader needs a guess to see the rationale. Recommendation: add one decision row.
- M2 (Medium, Adzic): the contract location is also unnamed for research (spec:116), task (spec:121), save (spec:119), cli-portify (spec:105, "file location unnamed") and recommend (spec:115, "a file"). Separately, WC-4 says "written on every outcome" (spec:62) but also "if the required output path is missing the command writes nothing"; the second sentence should be stated as the single exception.
- M3 (Medium, Whittaker): `--unattended` passed to a section-4 command (spec:128) is unspecified. Also unspecified is how the flag is recognised (a standalone argument versus quoted content); the command definition under audit handles this, the spec does not.
- M4 (Medium, Whittaker): no rule deletes or ignores a prior contract at a fixed path before a run (spec:69, 85-86; WC-11 depends on one worker at a time).
- M5 (Medium, Crispin): WC-1 (spec:59) has "well inside the readiness limit" with no number, and no phase or acceptance check covers it. The cited evidence gives 30 s passing and about 45 s failing (`CAPS:49`). Add a number and an owner.
- M6 (Medium, Nygard): no coordinator-side deadline for the silent stall that spec:44 itself names. Step 3 of 7.2 (spec:182) loops "until `worker_done` arrives" with no overall bound, and Orca's total-run-time bound is UNVERIFIED (spec:282).
- M7 (Medium, Fowler): the tasklist row (spec:122) says its reflect fan-out "runs one layer below the worker, inside Claude Code's nesting limit (`INV-A:14`)". `INV-B:213` counts a deeper chain (reflect subagent, then reviewers, then adversarial agents) and marks nested spawning UNVERIFIED (`INV-B:314`, item 1). Count the layers or mark it UNVERIFIED.
- M8 (Medium, Cockburn): before the contract exists (P0, and ready commands until their phase), WC-5's mapping covers only the contract. AC-0.4 (spec:194) says to check the outcome "against that file's own verdict" without a rule.
- M9 (Medium, Newman): the `## Unattended mode` sections point to `~/.claude/WORKER-CONTRACT.md` (spec:52), but whether the plugin mirror gets that core file is UNVERIFIED (spec:279). A command in an install without the file has no fallback. The contract also has `version: 1` but no compatibility rule between an old installed file and a new command.
- M10 (Medium, Fowler): remediation offers get three different treatments. reflect auto-accepts under `--unattended` (spec:88), which starts a corrective handoff with no person; troubleshoot resolves its `--fix` offer as blocked (spec:91); auggie-review turns its offer off (spec:100). The spec gives no common rule, and WC-9 covers only outward actions.
- M11 (Medium, Gregory): the pr-submit command states "Will Not: run headless" (`INV-B:90`, `cmd/pr-submit.md:85`); the P4 row (spec:114) adds `--unattended` without reconciling that line. D3 recommends not doing it, so this matters only under D3 (b).

Minor notes
- n1: the pr-submit top-level rule is cited at `SKILL.md:37-39` in the spec, `INV-A:10`, and `INV-B:90`, but at `SKILL.md:47-49` in `CAPS:161` (the installed copy under `~/.claude`). The poll loop range is `46-64` at spec:68 and `41-64` at spec:239. The cited line numbers differ between copies of the same text.
- n2: spec:154 says "Phases 1-3 need no user decision", but D4 (spec:244) lists auggie-review `--post-pr` and task `commit`/`push`, both in P2; spec:225 resolves this by proceeding on the recommendations.
- n3: AC-1.3 (spec:197) says "in a scratch worktree" without naming how it is created; the repo rule allows project worktrees only through Orca with an agent (`CLAUDE.md` Parallel Development section, UNVERIFIED line).
- n4: AC-C5 (spec:176) fails on any deleted line, so appending a flag to an existing Usage line would fail it; the spec does not say flags go on a new line.
- n5: adding Write to explain's tools (spec:108) and moving business-panel's frontmatter (spec:102) are listed as "defect fixes" under SA-4 (spec:149), but they change what the command may do or how it loads in a standalone session; SA-1 (spec:146) says nothing changes. The spec marks the second UNVERIFIED.
- n6: spec:285 reports a 340-citation check by a separate agent; I could not verify it, and it is a statement of process, not evidence.

=== SYNTHESIS ===
Consensus: the decision and the rejected alternatives are well evidenced; the 43-command partition is exact; the inventories support the cited lines I could check. Disagreement: none among the experts. Two defects block: the contract location and acceptance command for commands with no output flag (F1), and the replacement-Task path that strands dependents (F2). Quality scores (0-10): Clarity 7, Completeness 6, Testability 6, Consistency 6.

Reviser brief
- Blocking ids: F1, F2.
- Revise only text a blocking finding names (F1: spec:62, 64, 85-86, 91, 196, and AC-2.2 at spec:200 only if it passes `--output` to a command without one; F2: spec:61).
- Add no rule, mechanism or section that no blocking finding calls for; each added paragraph or table cites its finding id.
- Prefer deleting or narrowing to adding; report the byte size before and after, and the bytes added and deleted per finding id.
- Leave Medium and minor findings (M1-M11, n1-n6) alone; do not apply them.

verdict: FAIL
