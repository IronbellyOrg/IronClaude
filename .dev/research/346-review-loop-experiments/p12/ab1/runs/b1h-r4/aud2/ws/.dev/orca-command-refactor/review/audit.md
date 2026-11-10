review: 1 of 3

# Spec-panel critique: orca-worker-contract-spec.md (whole-document audit)

- Command: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture`
- Candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`
- sha256 (candidate): `005c14750dde7985fd4ffcf42529a7b23cc2ca06ed4169b3ad679316a9e00f9a`
- baseline: missing (first review of the full document; no `--re-review`, no `--baseline`)
- Reviewer model: Sonnet 5.5 (`claude-sonnet-5-5`)
- Prompt followed: FIRST-REVIEW prompt, `~/.claude/rules/prompts/document_review_loop_prompts.md:27-32` (read in full).
- Panel (fixed order, focus requirements + architecture): Wiegers (lead requirements), Adzic, Cockburn, Fowler (lead architecture), Nygard, Whittaker, Newman, Hohpe. Crispin, Gregory and Hightower were not active under these focus areas.

## Coverage

- Read in full: the candidate (309 lines), `.dev/orca-command-refactor/README.md`, `~/.claude/rules/prompts/document_review_loop_prompts.md`, `command.md`.
- Checked against the evidence I can open: `inventory/commands-a.md` and `inventory/orca-capabilities.md` (spot lines cited below), `inventory/commands-b.md` (spot lines).
- UNVERIFIED: every citation to `cmd/`, `sk/`, `src/`, `CLAUDE.md`, `EVIDENCE.md`, `.dev/codegraph-migration/...` and the Orca install files. None of them exists in this workspace (only `.dev/orca-command-refactor/` does). I checked the spec's internal consistency and its use of the three inventories, not the underlying source lines. The spec's own self-attestations (re-read of 11 locations, line 11; 340 citations re-checked by an `evidence-validator`, line 309) are likewise UNVERIFIED here.
- Not triggered: Pipeline Dimensional Analysis (no multi-stage data flow with count divergence; the phases are an ordering, not a data pipeline) and the correctness-focus artifacts (State Variable Registry; focus not requested).
- Not covered: the second half of the per-command verdicts (whether each command's gate list is complete) beyond the rows cited.

## Brief handling

No brief clause was overridden. The brief asks for a whole-document first review, which is how this run is graded; Medium and minor findings below do not affect the verdict.

## Prior-findings table

Not applicable (first review).

=== REQUIREMENTS ANALYSIS ===

### F-1 [MAJOR, blocking] WC-4 places the contract under "the output directory", but the brief tells tdd and spec-panel to pass a file
- Experts: Wiegers (consistency), Adzic (example does not run), Whittaker (FR-2.3 sentinel/type collision: a file path used as a directory).
- Grading sentence: An implementer who follows the stated text as written builds a contract at `<output-dir>/return-contract.yaml` with `<output-dir>` equal to the value of `--output` (`specs/orca-worker-contract-spec.md:62`), and for `/sc:tdd` that value is a file (`:89` "`--output <file>`", `:224` "`/sc:tdd "auth" --unattended --output <file>`"), so the implementer builds `<file>/return-contract.yaml`, a path under a regular file that cannot be created, and that is wrong because AC-2.2 (`:224`) and the live check (`:199-200`, `test -s <contract>`) require a contract with `status: blocked` that does exist.
- Same defect for `/sc:spec-panel`: row `:119` says "add `--output`; contract" with no statement whether the value is a file or directory. The command text supplied for this run already defines `--output` as file-valued (`command.md:23`, `command.md:460` "`--output` is file-valued") and gives it a different contract location, `<report-dir>/return-contract.yaml` with `--report-dir` (`command.md:460-461`). WC-4 names only `--output` / `--output-dir` (`:62`). The spec resolves the file-versus-directory clash for exactly one command, init-lite (`:86`), and gives no general rule for the rest.
- Location of the failing invariant: WC-4 (`:62`) versus section 3.1 tdd row (`:89`) and section 3.2 spec-panel row (`:119`).
- Concrete attack (sentinel/type collision): brief `/sc:tdd "auth" --unattended --output .dev/tdd/auth.md`. State before: no contract. WC-4 text says write `.dev/tdd/auth.md/return-contract.yaml`. After the TDD is written to `.dev/tdd/auth.md` the create fails, so the "written on every outcome" rule (`:62`) cannot hold for the most common outcome.
- Recommendation: state one rule in WC-4 for file-valued `--output` (for example, contract beside the file as `<file-stem>.return-contract.yaml`, or a separate required directory flag), and apply it to tdd and spec-panel in the rows.
- Priority: High.

### F-2 [MAJOR, blocking] `--unattended` is required on every command in P1, but the gate conversions that make it safe arrive in P2 to P4 (or never)
- Experts: Wiegers, Cockburn (the actor, a coordinator, relies on the flag), Nygard (the failure is a silent stall).
- Grading sentence: An implementer who follows the stated text as written adds `--unattended` and an `## Unattended mode` section naming `return-contract.yaml` to all 36 commands in P1 (`:160` "accepted by every command in sections 3.1 and 3.2"; `:219` AC-1.1 asserts the section for every command in 3.1-3.2), and builds, for example, a `/sc:task`, `/sc:tdd` or `/sc:pr-submit` that accepts the flag while its confidence prompt, topic clarification or `[yes / no]` offer still waits for a person until P2 or P4, and that is wrong because WC-2 (`:60`) says that under `--unattended` the command never prompts or ends its turn on a question; the two stated texts contradict at every point between P1 and the later phase.
- It is not only a transient state: for `/sc:pr-submit`, D3 recommends option (a), the coordinator or person runs it and there are "no pr-submit changes in Phase 4" (`:264`), and section 4 says it is a worker "only if the user accepts D3" (`:140`), yet AC-1.1 (`:219`) and P1 (`:160`) require its `## Unattended mode` section now. Under D3 (a) the final text of pr-submit advertises an unattended mode with a contract that no phase ever makes true.
- The spec's one hedge, "(a no-op where a command has no gate)" (`:160`), covers only commands without a gate, so it does not rescue the gated ones; and "Phases 1-3 need no user decision" (`:155`) is false for the D4 and D3 dependent rows that P1 already touches.
- Location: section 6 P1 row (`:160`) versus WC-2 (`:60`), AC-1.1 (`:219`), D3 (`:262-266`).
- Concrete attack (sequence attack, FR-2.4): after P1 merges and before P2, the coordinator follows section 2.3 and sends `/sc:task "..." --unattended`. Confidence is 0.62. The command accepts the flag, takes the interactive branch, and parks on a prompt. `worker-show` reports `agentWait` (healthy, not failed, `CAPS:129`), and the Task hangs, the failure mode WC-2 exists to prevent.
- Recommendation: in P1 add the flag and section only for commands whose gate resolutions are also delivered in P1 (the section 3.2 "no gate" rows), or make the flag refuse (exit `blocked`) on a gated command until its phase lands; scope AC-1.1 to the commands each phase delivers; and drop pr-submit from the P1/AC-1.1 set until D3 is answered.
- Priority: High.

### F-3 [Medium, follow-up] `cleanup-audit` is called ready today, but no contract path is defined for it
- Row `:85` gives no contract location; WC-4's "Where section 3 names a different fixed path" (`:62`) does not apply, and the command has no output-dir flag (`:85` "`--pass <N>`", "output dir is fixed"). Nothing says where `return-contract.yaml` goes after P1, so the live check's step 4 (`:200`) and the `worker_done --report-path` have no value. This needs the implementer to guess a path. Wiegers.

### F-4 [Medium, follow-up] D4 gates P2 rows, but the text says P1-P3 need no decision
- `:155` and `:249` say P0-P3 proceed on recommendations. D4 (`:268`) lists auggie-review `--post-pr` and task `commit`/`push`, both P2 rows (`:99`, `:120`). The recommendation (a) is stated, so a guess is not needed; the dependency is stated twice differently. Cockburn.

### F-5 [Medium, follow-up] spec-panel row appears stale against the command text supplied for this run
- Row `:119` and INV-B:182 say "no path or `--output` flag exists". The command definition for this audit (`command.md:23`) already lists `--output <file>`, `--unattended`, `--report-dir` and a full `## Unattended mode` section with `return-contract.yaml` (`command.md:455-465`), and the `target_release` blocked-gate (`command.md:463`) that row `:119` asks to add. If that is the current state of the file, the row asks for work already done and the flag name differs (`--report-dir`, not `--output`). I cannot tell which version `cmd/spec-panel.md:22` is (UNVERIFIED). Adzic.

### F-6 [Medium, follow-up] The "is there evidence" statement for tasklist hides an open question
- Row `:121` states the reflect fan-out "runs one layer below the worker, inside Claude Code's nesting limit, `INV-A:14`". INV-B:210 (and INV-B:46) marks nested spawning "UNVERIFIED", says the fan-out "must run at the worker's top level", and notes who answers reflect's offer inside a subagent is unstated (INV-B:209). INV-A:14 supports only the documented three-layer limit. The spec asserts the inventory's open question as settled and does not list it in the UNVERIFIED items (`:295-309`). Fowler, Nygard.

### F-7 [Medium, follow-up] AC-C5 as written fails any command that adds a flag to its Usage line
- `:177` and `:192` require `git diff -U0 ... | grep -E '^-[^-]'` to print nothing for edits "without a named defect fix". Adding `[--unattended]` to an existing Usage line (the usual place a flag is documented, for example `command.md:22-23`) produces a `-` line, so the check fails for a conforming edit; SA-4 (`:150`) calls flags additive. The implementer must pick between a separate usage line or a false failure. Crispin-style check, reported under Wiegers.

### F-8 [Medium, follow-up] AC-C1 can fail the P0 deliverable itself
- AC-C1 (`:183`) greps `src/superclaude/core` for `orca(-ide)? orchestration|worktree|terminal|agent`. P0 adds an Orca section to `HOW-WE-WORK.md` and a `WORKER-CONTRACT.md` with a coordinator brief template (`:159`). SA-2 allows only an Orca mention "as an example of a caller's question channel" (`:148`) and the grep matches any `orca orchestration ...` text. Whether the P0 text trips it depends on wording the spec does not constrain. A scope sentence (which files are exempt) is missing. Fowler.

### F-9 [Medium, follow-up] P1 command list omits init-lite and pre-lists the flag work for index-repo twice
- `:160` names fixes to "adversarial, cleanup-audit, index-repo, workflow" but the init-lite per-run output directory is also P1 (`:86`), and index-repo's `--output` is the section 3.2 P1 change (`:111`), not a "small fix to a ready command" (it moved to needs-change, `:292`). Counts in section 3 are still consistent (9 + 27 + 6 + load = 43, rows counted at `:83-91`, `:98-124`, `:133-138`).

=== ARCHITECTURE ANALYSIS ===

Architecture sound in its main line: Orca on top, commands as units, no Orca calls inside commands (`:16`, `:29-39`, `:237`), evidence honestly bounded in 1.4 (`:41-45`). The R1 to R5 rejection reasons are consistent with CAPS (`orca-capabilities.md` section 5 lines 97-101; section 9 lines 140-152 in the inventory), and the claim that Agent-tool subagents are outside Orca's depth fence is cited correctly to CAPS section 10 (`orca-capabilities.md:153-156`) with the UNVERIFIED caveat kept (`:45`, `:296-299`). Findings F-1, F-2 and F-6 above are the architecture-relevant defects.

### Guard Condition Boundary Table
Guards found: `--unattended` switch; confidence `< 0.70` (task); WC-10 wait `> 4 min` against 5-minute heartbeat; nesting depth `1`; `check` -> `consumer_fenced`; AC-2.4 counts unchanged. Classes left out are named with a reason.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| `--unattended` | spec:60, 160 | Zero/Empty | flag absent | false | standalone behavior unchanged (SA-1, `:147`) | OK |
| `--unattended` | spec:60, 160, 219 | Legitimate Edge Case | flag present on a gated command before its phase lands | true | contradicts WC-2; behavior unspecified | GAP (F-2, blocking) |
| `--unattended` | spec:140, 264 | Legitimate Edge Case | flag on pr-submit when D3 = (a) | true | section required by AC-1.1 but never made true | GAP (F-2, blocking) |
| WC-4 output dir | spec:62, 89, 119 | Legitimate Edge Case | `--output` is a file path | n/a | no rule; `<file>/return-contract.yaml` impossible | GAP (F-1, blocking) |
| WC-4 output dir | spec:62, 85 | Zero/Empty | command has no output flag (cleanup-audit) | n/a | path unspecified | GAP (F-3, Medium) |
| confidence `< 0.70` | spec:120 | Typical | 0.62 | true | blocked, contract written | OK |
| confidence `< 0.70` | spec:120 | Sentinel Value Match | exactly 0.70 | false | not stated in spec (inherited from `cmd/task.md:80`, UNVERIFIED) | UNVERIFIED |
| WC-10 wait split | spec:68 | Typical | 600 s pr-submit budget | true | split at 4 min | OK |
| WC-10 wait split | spec:68, 113 | Legitimate Edge Case | one poll script run longer than 4 min | true | "poll script runtime UNVERIFIED" | UNVERIFIED (spec:307) |
| WC-10 wait split | spec:68 | Maximum/Overflow | eval timeout 3600 s | true | split into waits of at most 4 min | OK |
| nesting depth `1` | spec:66, 33 | Maximum/Overflow | worker calls `worker-start` | true | refused; WC-8 forbids | OK |
| nesting depth `1` | spec:66 | Legitimate Edge Case | worker calls `task-create` | unknown | forbidden by WC-8 either way; Orca behavior UNVERIFIED (spec:300) | OK |
| `check` returns `consumer_fenced` | spec:70 | Typical | fenced | true | stop, no `worker_done` | OK |
| AC-2.4 review/comment counts | spec:226 | Zero/Empty | PR with 0 reviews | n/a | `length` = 0 before and after, passes | OK |

Left out for the one-line reason given: "Maximum" for `--unattended` and `consumer_fenced` (boolean-valued, no capacity), "One/Minimal" for the depth guard (depth 0 is the coordinator, not a worker case).

FR-8 / FR-9 applied: the four GAP rows are graded in F-1 and F-2 (blocking) and F-3 (Medium). FR-10: table is complete.

### Whittaker attacks (summary)
- Sentinel collision (FR-2.3): file path versus directory for `--output` (F-1).
- Sequence attack (FR-2.4): P1-before-P2 state (F-2).
- Divergence attack (FR-2.2): `partial` maps to `succeeded` (WC-5, `:63`, decision `:287`) while a `partial` run of an audit with a FAIL verdict also maps to `succeeded` (`:63`); the coordinator cannot tell "audit passed" from "audit failed" except by reading the body sentence. Specified deliberately; noted, not graded.
- Zero/empty attack: no `ask` timeout value is specified (`:305`); WC-3 relies on message ID resume, so the empty case is handled.
- Accumulation attack: none found; no counter or buffer in scope.

## Minor notes (do not affect the verdict)

- Revision tags such as `[M2]`, `[M4]`, `[M6]`, `[M7]`, `[M8]`, `[M9]`, `[N2]` appear inside normative text (for example `:62`, `:73`, `:76`, `:173`) and are never defined in the spec; `review/disposition.md` is not in the workspace.
- Live check step 5 (`:201`) searches the transcript for the string `AskUserQuestion`; a transcript that echoes command text containing the word would give a false failure. A tool-call match would be tighter.
- P0 adds `tests/skills/test_worker_contract.py` (`:159`) while AC-C3 (`:175`) requires new tests to pass at the end of P0 and AC-1.1 (`:219`) asserts content that exists only after P1; the P0 content of that file is unstated.
- The spec states the 43-command split correctly (`:76`); "10 / 27 / 6" in the Decisions row (`:292`) is the inventories' split and is explained.

## Follow-up candidates (Medium and minor; none triggers a revision)

F-3, F-4, F-5, F-6, F-7, F-8, F-9, and the four minor notes above. The session that ran this review would ask the user once whether to open an issue for them; this run was dispatched with a final-reply-only contract and no way to ask, so it creates none and only records the list.

## Reviser brief

Blocking finding ids: F-1, F-2.

Rules for the reviser (restating the Reviser contract, Review Loop bullet 6): revise only text a blocking finding names; add no rule, mechanism or section that no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, and the bytes added and deleted per finding id. Leave Medium and minor findings alone, return the candidate once, and do not award yourself a PASS.

verdict: FAIL
