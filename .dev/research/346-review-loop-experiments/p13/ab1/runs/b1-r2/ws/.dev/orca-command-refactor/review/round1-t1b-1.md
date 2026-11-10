review: 1 of 3

# Spec-panel review, round 1: Orca worker contract spec

- candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (285 lines)
- candidate sha256: `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d`
- baseline: not given (first review of the full document); prior report: not given
- command / mode / focus: `/sc:spec-panel --mode critique --focus requirements,architecture`; format standard (critique buckets)
- reviewer model actually used: Sonnet 5.5 (`claude-sonnet-5-5`), one reviewer, one fresh context
- review prompt followed: FIRST-REVIEW prompt of `~/.claude/rules/prompts/document_review_loop_prompts.md` (read in full). The `superclaude review panel resolve` and `superclaude review merge` commands were not run: the sandbox has no `superclaude` CLI and none was probed, so this is a single-reviewer report (the prompt allows this and asks that it be stated).
- evidence base: `.dev/orca-command-refactor/README.md` (read first), `inventory/commands-a.md` (INV-A), `inventory/commands-b.md` (INV-B), `inventory/orca-capabilities.md` (CAPS). Nothing else was read.

## Coverage

Covered: all 285 lines of the candidate; every `INV-A:n`, `INV-B:n` and `CAPS:n` citation against the three inventories (about 120 line citations, all land on the claimed content, no wrong line found); the 10 / 27 / 6 split and the per-phase command lists against the inventory verdict tables (counts agree: 5+5 ready, 13+14 needs-change, 3+3 coordinator-only, and the P1/P2/P3/P4 command lists add up to the 27 rows plus the four ready-command fixes); every acceptance check in section 7 for whether it can pass as written.

Not covered, marked UNVERIFIED (no such file in the sandbox): every `src/superclaude/...` path:line cited directly (`sk/`, `cmd/`, `install_core.py:13-24`, `tests/`, `Makefile`, `pyproject.toml:38`), every `CLAUDE.md:n` and `HOW-WE-WORK.md:n` citation, `.dev/evals/ccsession-orca-e2e-20261026/EVIDENCE.md`, `.dev/codegraph-migration/...`, the grep result claimed in E5, the "11 locations re-read" claim (line 11) and the "340 citations re-read" claim (UNVERIFIED item 14, line 285). Where the spec cites such a line through an inventory line (for example `INV-A:35`), the inventory line was checked and the underlying source line is still UNVERIFIED.

Mandatory artifacts: Guard Condition Boundary Table (triggered; below) and Quantity Flow Diagram (triggered; below). The State Variable Registry is only required under `--focus correctness`, which was not requested, so it is not produced.

Minor-finding policy: Medium and minor findings never fail this review (see `follow-up candidates`). No brief clause was overridden: the brief did not widen scope or grade a minor finding as blocking.

## Panel and method

Requirements focus: Wiegers (lead), Adzic, Cockburn. Architecture focus: Fowler (lead), Newman, Hohpe, Nygard. Whittaker is active in every review and ran after Fowler and Nygard. Crispin, Gregory and Hightower are outside the requested focus areas and did not speak.

Each blocking finding below passes the grading check: an implementer who follows the stated text as written builds X, and X is wrong because Y, with no further assumption.

## Grading summary

| Id | Where | Grade | Short claim |
|---|---|---|---|
| F1 | AC-1.1 (line 195) vs P1 scope (159), load row (112), section 4 (128), P4 gating (154, 162) | blocking | The P1 check cannot pass: it demands a contract-naming `## Unattended mode` section on commands the same spec says get none, or get it only after user decisions |
| F2 | WC-4 (line 62) vs 3.1 `--output <file>` rows and AC-2.2 (line 200) | blocking | The contract path is defined as `<output-dir>/return-contract.yaml`, but the spec's own examples pass a file or no output at all |
| F3 | AC-0.4 (line 194) vs 7.2 step 3 (line 182) | blocking | The P0 gate requires "steps 1-3 pass", and step 3 requires a WC-4 contract that P0 says does not exist yet |
| F4-F16 | various | Medium (a few MINOR) | Listed under follow-up candidates; none triggers a revision |

## === REQUIREMENTS ANALYSIS ===

### F1. AC-1.1 cannot pass: its scope contradicts the load row, section 4 and the P4 decision gate (CRITICAL, blocking)

- Expert: Wiegers (testability, traceability), Adzic (the example the check should pass), Cockburn (who owns each phase).
- Text in conflict:
  - Line 195, AC-1.1 (phase P1): the test "asserts that every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`".
  - Line 159, P1 scope: "the `--unattended` flag accepted by every command in sections 3.1 and 3.2".
  - Line 112, the `load` row: Report (WC-4) is "none (see note)", "use it as a step inside another worker's brief, not as its own Task", Phase "P1 (usage line only)". Line 159 repeats "load (usage line only)".
  - Line 154: "Phases 1-3 need no user decision; Phase 4 waits for answers to D2-D4." Line 162 puts implement, post-release and pr-submit in P4 because each "needs the user's decision first".
  - Line 240 (D3 (a), the recommendation): pr-submit runs at the coordinator or person only, "no pr-submit changes in Phase 4"; line 128 says coordinator-only commands get no `--unattended` mode.
- Wrong outcome: An implementer who follows the `load` row changes only its Usage line, and an implementer who follows P4 gating leaves implement, post-release and pr-submit alone until D2-D4 are answered. The P1 test then fails for load, implement, post-release and pr-submit. The only way to make it pass is to give `load` a section naming a contract it never writes (against WC-4 and line 112), and to write gate resolutions for implement, post-release and pr-submit before the user has decided what they are (against line 154), and, if D3 (a) is chosen, to give a section to a command the spec treats as coordinator-only. P1 is the gate for P2 (line 154, "Later phases do not start until the earlier phase's checks in section 7 pass").
- Recommendation (narrow, no new rule): restrict AC-1.1 and the P1 flag scope to the commands P1 actually edits (the 9 P1 commands plus the 4 ready-command fixes, and load excluded), and let each later phase's own AC cover its commands. Cite F1 on the change.
- Priority: High. Quality impact: acceptance-test pass rate for P1, and the P1-to-P2 ordering.

### F2. WC-4 defines the contract path from an output directory the spec's own examples do not have (CRITICAL, blocking)

- Expert: Adzic (concrete example fails), Wiegers (consistent definition), Hohpe (the coordinator must find the file).
- Text in conflict:
  - Line 62, WC-4: the command "writes `<output-dir>/return-contract.yaml`, where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`)", and the file is written "including stops before any other output exists".
  - Line 87 (init-lite) and line 90 (tdd): the brief passes `--output <file>`. Line 120 (spec-panel): "add `--output`" with no statement whether it is a file or a directory. Line 104 (cli-eval): no output flag in the row at all.
  - Line 200, AC-2.2, which tests the blocked path: "`/sc:tdd "auth" --unattended --output <file>` with a bare topic; `/sc:cli-eval run --unattended` with no `--suite`", with pass condition "contract `status: blocked` with a non-empty `blocked_question`".
- Wrong outcome: For the first AC-2.2 example, WC-4 gives `<file>/return-contract.yaml`, where `<file>` is a file path. A file cannot contain a child, so the write fails or goes nowhere the spec names, and the pass condition "contract `status: blocked`" has no file to read. For the second example no directory was passed at all, so `<output-dir>` is undefined and the contract has no location. The same hole exists for any unattended run that omits `--output` (nothing says it is refused, and WC-4 says the file is written on every outcome). The phrase "known before dispatch" (WC-4, line 73) cannot hold either.
- Recommendation: state one path rule that works for file-valued and absent `--output`: for a file-valued flag the contract sits beside the file (same directory) or at a flag the brief names; say what an unattended run does when no output location is given (blocked, with the contract written to a stated fallback). Cite F2 on the added sentence.
- Priority: High. Quality impact: the central deliverable of the spec (a report the coordinator can open) has no defined path for at least tdd, init-lite, spec-panel and cli-eval.

### F3. The P0 gate demands a WC-4 contract that P0 does not create (MAJOR label, grades blocking: an acceptance criterion cannot pass)

- Expert: Wiegers (verifiable criteria), Adzic.
- Text in conflict: Line 194, AC-0.4: pass condition "steps 1-3 and 5-7 pass; step 4 uses the command's existing report file, since the contract arrives in P1". Line 182, step 3 of 7.2: pass requires "exactly one `worker_done`; its `--outcome` matches the contract's `status` under WC-5; its report path is the WC-4 contract path". Line 158 and line 159: the WC-4 contract is added in P1.
- Wrong outcome: AC-0.4 excuses step 4 only. For `/sc:troubleshoot` (REPORT.md; `return-contract.yaml` only with `--caller task-unified`, INV-B:242) and `/sc:adversarial` (contract filename not fixed until the P1 fix, line 83), the step 3 condition "report path is the WC-4 contract path" and "matches the contract's status" cannot be met, so a literal P0 run fails. A P0 failure "reopens section 1" (line 194) and, by line 154, blocks every later phase.
- Recommendation: in AC-0.4 say that for P0 step 3 compares `--outcome` and `--report-path` with the command's existing report file (the same exception it already makes for step 4). Cite F3.
- Priority: High. Quality impact: the live baseline that the whole decision rests on (evidence gap 1, line 43) could be recorded as failed for the wrong reason.

### Medium findings, requirements (follow-up candidates, not blocking)

- **F4 stale contract (MAJOR label, Medium).** Expert: Whittaker (Sequence attack), Nygard. Line 63: `--outcome failed` when "the report says failed or blocked, or no report exists"; line 64: a retry "must not corrupt the first attempt's output". Attack: attempt 1 ends `status: blocked` and leaves its contract in the output directory; the retry is started with the same brief and directory, crashes before writing anything; the coordinator opens the old `blocked` file and treats it as the retry's report. Nothing requires the command to replace or remove an earlier contract at start. Needs a guess about brief reuse, so Medium. Suggested: one line, write `status: running` first or delete any earlier contract at start.
- **F5 `--unattended` as a sentinel (MAJOR label, Medium).** Expert: Whittaker (Sentinel Collision). Line 51 defines the mode by "when its caller passes `--unattended`" and D1 (line 228) recommends the flag. The spec does not say that a quoted free-text argument containing the text `--unattended` (for example `/sc:tdd "explain the --unattended switch"`) is not the switch. Whether the implementer matches tokens or substrings is a guess. Suggested: the flag counts only as a standalone argument token outside quoted content.
- **F6 no flag exists for the authorizations WC-9 depends on (MAJOR label, Medium).** Expert: Wiegers. Line 67: an outward default "turns on only through the command's own explicit flag written in the brief". Line 121 (`task` commit/push, EXEMPT keywords), line 113 (post-release VM/install/commit/PR) and line 114 (pr-submit's whole purpose is opening a PR) name no such flag, and D4 (line 245) says "passes the command's explicit flag". Also D4 (line 244) lists auggie-review and task, which are P2 commands, while line 154 says only P4 waits for D2-D4. A requirement the document never states, so Medium.
- **F7 retry directory vs "known before dispatch" (MAJOR label, Medium).** Expert: Cockburn, Nygard. Line 64 offers "a fresh output directory", while line 73 requires the brief to fix the output directory before dispatch. Nothing says who makes the fresh directory on a `--retry-of` start (the command, which breaks "known before dispatch", or the coordinator, which section 2.3 does not list). The implementer picks one of two allowed readings, so Medium.
- **F10 requirements without a check (MAJOR label, Medium).** Expert: Wiegers, Adzic. Line 167: "A phase passes only when every check in its block and every common check passes." WC-1, WC-3, WC-6 and WC-12 have no acceptance check in section 7. WC-10 is checked only for pr-submit (AC-4.3), although cli-eval carries the same wait rule (line 104, P2). An unstated check, so Medium.
- **F13 workflow's pre-creation contract has no directory (MAJOR label, Medium).** Expert: Wiegers. Line 92: "Write the contract for pre-creation STOPs too (WC-4 "every outcome")". The workflow contract lives at `.dev/tasks/to-do/<id>/return-contract.yaml`, and a pre-creation stop has no package directory yet (INV-B:272 says it is "not written for pre-creation STOPs"). AC-1.4 (line 198) only checks that the skill states it. Same family as F2.
- **F14 WC-3 allows `ask` where AC-2.2 expects a deterministic outcome (MAJOR label, Medium).** Expert: Adzic. Line 61 says the session "may instead ask the coordinator once with the preamble's `ask` command", while AC-2.2 (line 200) expects `worker_done --outcome failed` and `status: blocked` on a gate hit. Both outcomes are allowed by the text; a test run that chooses `ask` fails the check.
- **F16 status vocabulary vs "keep their fields" (MINOR).** Expert: Fowler. Line 62 "Commands that already write a contract keep their fields and add the missing ones" and the fixed four-value `status` set (line 262) cannot both hold if an existing contract uses another `status` word. The existing contracts (INV-B:272 and others) are not in the sandbox, UNVERIFIED.

## === ARCHITECTURE ANALYSIS ===

Positive findings (no defect): the decision structure is sound. Orca-on-top is supported by evidence the sandbox can check (CAPS:92, CAPS:97-103, CAPS:147-150, CAPS:159-161); the rejection reasons R1-R5 each rest on a CAPS line that says what is claimed; the spec states plainly that no direct-route end-to-end run exists (lines 43-45) and puts a live baseline first (P0). Newman and Hohpe found no hidden coupling between the commands' installed path and Orca: SA-2 and WC-8 keep Orca out of the command files.

### Medium findings, architecture (follow-up candidates, not blocking)

- **F8 join over fewer reports than workers (MAJOR label, Medium).** Expert: Fowler, Whittaker (Divergence and Accumulation attacks). Line 39 splits heavy fan-out into several worker Tasks "then one `/sc:adversarial` worker on their reports". The Quantity Flow Diagram below shows the count falling from N started workers to K reports: a worker that ends `blocked` or `failed` yields a contract with no usable report, and a failed Task keeps its dependents blocked (CAPS:90). The spec does not say what the coordinator does when K < N, and `/sc:adversarial` takes 2-10 artifacts (INV-A:35). Concrete: 3 troubleshoot workers, 2 end `blocked`, 1 report remains, below the 2-artifact minimum. The text does not assume count conservation, it is silent, so this is a missing requirement, Medium (not the CRITICAL of FR-19).
- **F9 an unsupported statement about worker-start (MAJOR label, Medium).** Expert: Nygard. Line 44: a command's own `AskUserQuestion` "comes *after* readiness, so it does not fail `worker-start`". CAPS:47 says Claude receives the task on the command line, not typed, which means the command can start running before the input box is ready; CAPS:48-49 shows only that a prompt before the box blocks readiness. Whether a first-action question blocks readiness is not shown anywhere in the sandbox evidence. The section 3 mitigations (no prompt under `--unattended`) make the wrong reading harmless in practice, so Medium. Also unstated: how a worker whose first message is a preamble (CAPS:47) runs a `/sc:` command at all (line 16 says it "runs one command"); P0 smoke runs would reveal it (F15 below).
- **F11 AC-C1 scans a directory SA-2 lets mention Orca (MAJOR label, Medium).** Expert: Fowler. Line 172: AC-C1 greps `src/superclaude/core` as well and requires "prints nothing (SA-2, WC-8)"; SA-2 (line 147) allows "an example of a caller's question channel inside the contract file", and P0 puts that file and an Orca section of the routing guide in `core` (line 158). If either text names `orca orchestration ask`, AC-C1 fails in P0. Depends on wording the implementer picks, so Medium.
- **F12 AC-C5 and Usage lines (MAJOR label, Medium).** Expert: Newman. Line 176 requires no deleted line in a command file edited without a named defect fix, yet P1-P2 add flags (`--output`, `--unattended`), and the natural place is the Usage line, whose edit shows as a deleted line. The implementer can add a new line instead, so Medium.
- **F15 how a worker starts a slash command (MAJOR label, Medium).** Expert: Cockburn. Line 16 and WC-7 say the worker "runs one command" directly in its top-level session. The prompt Orca gives starts with a preamble (CAPS:47-48, CAPS:151), not with `/sc:`; whether the command runs as a typed slash command or through the Skill tool is not stated. UNVERIFIED, and P0 covers it only implicitly.

### Minor notes

- **F17 (MINOR).** Line 62 states "Orca does not check the file" as a fact; CAPS:79 and line 274 call it UNVERIFIED.
- **F18 (MINOR).** Line 202, AC-2.4: `gh api ... --jq length` counts one page only (30 items by default), so a new comment on a PR with 30 or more can leave the count unchanged; add `--paginate`.
- **F19 (MINOR).** Line 172 and 175 hold shell pipes written as `\|` inside markdown table cells; copied from the raw file, the commands break (AC-C1 would match nothing and print nothing, a vacuous pass).
- Also noted, no id: E3 (line 23) cites `invocation_method: "skill-direct"` as support while line 43 says that run used an Agent-tool subagent; line 22 says the worker "answered", which CAPS:49 does not quote; line 128 vs line 159 label P1 "commands with no gate" although business-panel, explain, test and index get refusals there.

## === ADVERSARIAL ANALYSIS (Whittaker) ===

All five attack methodologies were applied to the invariants "a worker run always ends in exactly one readable report" and "standalone behaviour is unchanged".

- **Zero/Empty.** I can break this specification by Zero/Empty Attack. The invariant at WC-4 (line 62) fails when `--output` is absent in unattended mode. Concrete attack: `/sc:cli-eval run --unattended` with no output flag; before: no contract; after: spec requires one on "every outcome" but defines no path. Reported as F2 (blocking).
- **Divergence.** I can break this specification by Divergence Attack. The invariant at WC-5 (line 63) fails at the boundary between `partial` and `failed`: a run with some artifacts and one failed sub-step may write either, and `partial` maps to `succeeded`, so a coordinator releases dependents (CAPS:90) on a half-done result. The spec does not define when `partial` applies, and the decision row (line 263) justifies the mapping only by "usable deliverable". Not graded blocking: it needs a guess on how each command uses `partial` (follow-up, folded into F16).
- **Sentinel Collision.** I can break this specification by Sentinel Collision Attack at line 51 (`--unattended`). Concrete attack: `/sc:tdd "explain the --unattended switch" --output d.md` run by a person; if the implementer matches substrings the mode turns on and violates SA-1. Reported as F5 (Medium).
- **Sequence.** I can break this specification by Sequence Attack at WC-4/WC-6 (lines 62, 64). Concrete attack: attempt 1 writes `status: blocked`; the retry in the same directory dies before its first write; the coordinator reads the stale file. Reported as F4 (Medium). Also: `worker_done` before the contract is flushed is not excluded; WC-5 says "after" only by implication.
- **Accumulation.** I can break this specification by Accumulation Attack at the retry cap (CAPS:80, `[G:recovery]` lines 120-122, used by line 64). A command that blocks deterministically on a missing flag blocks again on every `--retry-of` with the same brief; the spec does not say the coordinator must change the brief before a retry, so the loop only ends when the Task is failed by the user. Not graded blocking (inferrable from CAPS:80 that a worker's own `failed` does not count). Note only.

## Guard Condition Boundary Table

Guards identified: G1 readiness limit (WC-1), G2 wait size and heartbeat cadence (WC-10), G3 outcome mapping (WC-5), G4 unattended switch (D1), G5 contract location (WC-4), G6 report count at a join (section 1.3). A class that cannot occur is left out with its reason on the row below the table.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| G1 readiness | WC-1, line 59 | Typical | prompt falls back at 30 s | within limit | passes (EVIDENCE.md:45 via CAPS:49) | OK |
| G1 readiness | WC-1, line 59 | Maximum/Overflow | fallback at 46 s or more | exceeds 45-60 s | worker-start fails again (CAPS:49) | OK |
| G1 readiness | line 44 | Legitimate Edge Case | command's first action is a question | unknown | "does not fail worker-start" (unsupported) | GAP (F9, Medium) |
| G2 wait size | WC-10, line 68 | Zero/Empty | wait of 0 s or no wait | n/a | not stated; a poll with `--poll-interval 0` | GAP (note, inferrable) |
| G2 wait size | WC-10, line 68 | Typical | single call of 3 min | true (<= 4 min) | heartbeat between calls | OK |
| G2 wait size | WC-10, line 68 | Maximum/Overflow | single call of 4 to 5 min, or exactly 5 min | boundary | "longer than 5 minutes" triggers the split, but the split target is 4 min | GAP (minor: 4-5 min calls neither required nor forbidden) |
| G2 wait size | AC-4.3, line 210 | Legitimate Edge Case | poll runtime + sleep > 240 s | false | UNVERIFIED (item 12, line 283) | GAP (declared UNVERIFIED) |
| G3 outcome map | WC-5, line 63 | Zero/Empty | no report file | failed | `--outcome failed` | OK |
| G3 outcome map | WC-5, line 63 | Typical | `status: succeeded` | succeeded | `--outcome succeeded` | OK |
| G3 outcome map | WC-5, line 63 | Sentinel Value Match | `status: partial` | succeeded | `--outcome succeeded`, body says partial | OK |
| G3 outcome map | WC-5, line 63 | Sentinel Value Match | `status` word outside the four values (existing contracts) | unspecified | not stated | GAP (F16, minor) |
| G3 outcome map | WC-5 / WC-6 | Legitimate Edge Case | stale earlier contract present, new run writes none | "report exists" | maps the stale status | GAP (F4, Medium) |
| G4 unattended switch | line 51 | Zero/Empty | flag absent | false | today's behaviour (SA-1) | OK |
| G4 unattended switch | line 51 | Typical | standalone `--unattended` | true | mode on | OK |
| G4 unattended switch | line 51 | Sentinel Value Match | `--unattended` inside quoted text | unspecified | not stated | GAP (F5, Medium) |
| G5 contract location | WC-4, line 62 | Zero/Empty | no `--output`, no `--output-dir` | undefined | not stated | GAP (F2, blocking) |
| G5 contract location | WC-4, line 62 | Typical | `--output <dir>` | directory | `<dir>/return-contract.yaml` | OK |
| G5 contract location | WC-4 vs line 90 | Legitimate Edge Case | `--output <file>` | file | `<file>/return-contract.yaml` (impossible) | GAP (F2, blocking) |
| G5 contract location | line 92 | Legitimate Edge Case | workflow stop before the package exists | no directory | not stated | GAP (F13, Medium) |
| G6 join count | line 39 | Zero/Empty | all N upstream workers blocked | 0 reports | not stated | GAP (F8, Medium) |
| G6 join count | line 39 | One/Minimal | 1 of 3 reports usable | below `/sc:adversarial` minimum of 2 | not stated | GAP (F8, Medium) |

Left out on purpose: G1 One/Minimal and Zero/Empty (a startup limit has no zero case: `--timeout-ms` must be a positive number, CAPS:44-45); G3 Maximum/Overflow (the outcome map has no counter); G4 Maximum/Overflow and One/Minimal (a flag is present or absent).

FR-8/FR-9 grading: the GAP rows that name a concrete wrong outcome an implementer would produce are G5 (blocking, F2). The other GAP rows are Medium or minor and are listed under follow-up candidates. No GAP row names a security, data-loss or safety-boundary risk.

## Quantity Flow Diagram (Pipeline Dimensional Analysis, Fowler and Whittaker)

Trigger: a multi-stage flow where output count can differ from input count (the Task fan-out of section 1.3 and section 2.3).

```text
[Coordinator plan: N Tasks] --> [N worker-start calls] --> [N workers run]
                                                              |
                                          K <= N contracts with status succeeded or partial
                                          (N-K end blocked or failed, CAPS:90: dependents stay blocked)
                                                              |
                                                              v
                       [Join consumer: one /sc:adversarial worker, accepts 2-10 artifacts]
                       [Consumer assumes: N reports]   <-- MISMATCH when K < N (spec silent, F8)
                       [Consumer minimum: 2 reports]   <-- MISMATCH when K < 2
```

Consistency check: the spec never states that all N reports arrive, so no stated text assumes count conservation; the divergence is an omitted requirement, graded Medium (F8). Scenario with counts: N = 3 troubleshoot workers, 2 end `blocked`, K = 1, `/sc:adversarial` needs 2.

## Expert consensus and disagreements

- Consensus: keep the decision (Orca coordinates, commands stay units of work); the three blocking findings are defects of the verification and path rules, not of the decision.
- Wiegers and Adzic: the three blocking defects are all places where an example or an acceptance check, run literally, contradicts the rule it checks.
- Fowler and Nygard: the contract path (F2) and the join behaviour (F8) are the two places where a missing interface rule would be rediscovered by every command author.
- No expert disagreement worth recording.

## follow-up candidates

Medium (warnings): F4, F5, F6, F7, F8, F9, F10, F11, F12, F13, F14, F15. Minor notes: F16, F17, F18, F19, plus the unnumbered notes under Minor notes.

The session that ran this review would ask the user once whether to open an issue for these; this is a worker run with no user in the loop, so the question was not asked and no issue was created. The list is only recorded.

## Findings block

```findings-v1
{"id": "F1", "severity": "CRITICAL", "blocking": true, "category": "unpassable-check", "anchor": "every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml`", "anchor2": "use it as a step inside another worker's brief, not as its own Task", "refs": ["AC-1.1", "P1", "WC-4", "section 4", "D3"], "claim": "AC-1.1 requires a contract-naming Unattended mode section on load (which writes no contract) and on implement, post-release and pr-submit (which the spec holds for P4 or the coordinator), so the P1 check cannot pass as written."}
{"id": "F2", "severity": "CRITICAL", "blocking": true, "category": "contradiction", "anchor": "where `<output-dir>` is the directory the coordinator passed", "anchor2": "/sc:tdd \"auth\" --unattended --output <file>", "refs": ["WC-4", "AC-2.2", "3.1", "3.2"], "claim": "WC-4 builds the contract path from an output directory, but AC-2.2 and the tdd and init-lite rows pass a file or no output at all, so the contract the check must read has no defined location."}
{"id": "F3", "severity": "MAJOR", "blocking": true, "category": "unpassable-check", "anchor": "steps 1-3 and 5-7 pass; step 4 uses the command's existing report file", "anchor2": "its report path is the WC-4 contract path", "refs": ["AC-0.4", "7.2", "P0", "P1"], "claim": "AC-0.4 requires 7.2 step 3 to pass in P0, but step 3 demands the WC-4 contract path and contract status, which P0 says do not exist until P1, so the P0 gate fails for the wrong reason."}
{"id": "F4", "severity": "MAJOR", "blocking": false, "category": "missing-requirement", "anchor": "`--outcome failed` when the report says `failed` or `blocked`, or no report exists", "refs": ["WC-5", "WC-6"], "claim": "A stale contract from an earlier attempt in the same directory is read as the retry's report because nothing requires it to be replaced at start."}
{"id": "F5", "severity": "MAJOR", "blocking": false, "category": "missing-requirement", "anchor": "the behaviour a command switches to when its caller passes `--unattended`", "refs": ["D1", "SA-1"], "claim": "The text does not say that a quoted argument containing the text --unattended is not the switch."}
{"id": "F6", "severity": "MAJOR", "blocking": false, "category": "missing-requirement", "anchor": "It turns on only through the command's own explicit flag written in the brief.", "refs": ["WC-9", "D4"], "claim": "task commit/push, post-release and pr-submit have no named explicit flag, and the auggie-review and task authorizations sit in P2 while the spec gates only P4 on D2-D4."}
{"id": "F7", "severity": "MAJOR", "blocking": false, "category": "missing-requirement", "anchor": "writes each run into a fresh output directory so a re-run starts clean", "anchor2": "so the report path is known before dispatch (WC-4)", "refs": ["WC-6", "2.3"], "claim": "Nobody is assigned to create the fresh directory on a retry, and a coordinator-fixed directory is the opposite of fresh."}
{"id": "F8", "severity": "MAJOR", "blocking": false, "category": "missing-requirement", "anchor": "then one `/sc:adversarial` worker on their reports", "refs": ["1.3", "CAPS:90"], "claim": "The join step is unspecified when blocked or failed workers leave fewer reports than workers, down to below the 2-artifact minimum of /sc:adversarial."}
{"id": "F9", "severity": "MAJOR", "blocking": false, "category": "other", "anchor": "A command's own `AskUserQuestion` or chat question comes *after* readiness, so it does not fail `worker-start`", "refs": ["1.4", "CAPS:47", "WC-1"], "claim": "The sandbox evidence does not show that a first-action question cannot block readiness when Claude receives its task on the command line."}
{"id": "F10", "severity": "MAJOR", "blocking": false, "category": "missing-requirement", "anchor": "A phase passes only when every check in its block and every common check passes.", "refs": ["section 7", "WC-1", "WC-3", "WC-6", "WC-12"], "claim": "WC-1, WC-3, WC-6 and WC-12 have no acceptance check, and WC-10 is checked for pr-submit only."}
{"id": "F11", "severity": "MAJOR", "blocking": false, "category": "other", "anchor": "prints nothing (SA-2, WC-8)", "anchor2": "The only allowed mention of Orca in a changed command is as an example of a caller's question channel inside the contract file.", "refs": ["AC-C1", "SA-2", "P0"], "claim": "AC-C1 greps src/superclaude/core, where the P0 contract file and routing-guide Orca section may legitimately name orca commands."}
{"id": "F12", "severity": "MAJOR", "blocking": false, "category": "other", "anchor": "prints nothing: edits are additive", "refs": ["AC-C5", "SA-4"], "claim": "Adding a flag to an existing Usage line shows as a deleted line, so AC-C5 can fail on a purely additive change."}
{"id": "F13", "severity": "MAJOR", "blocking": false, "category": "missing-requirement", "anchor": "Write the contract for pre-creation STOPs too (WC-4 \"every outcome\")", "refs": ["3.1", "AC-1.4", "WC-4"], "claim": "A workflow stop before the package exists has no package directory to hold the contract, and no other location is given."}
{"id": "F14", "severity": "MAJOR", "blocking": false, "category": "contradiction", "anchor": "the session may instead ask the coordinator once with the preamble's `ask` command", "refs": ["WC-3", "AC-2.2"], "claim": "WC-3 allows ask where AC-2.2 expects worker_done failed and a blocked contract, so a compliant run can fail the check."}
{"id": "F15", "severity": "MAJOR", "blocking": false, "category": "missing-requirement", "anchor": "one worker (a top-level Claude session in its own Orca terminal) runs one command", "refs": ["1.1", "WC-7", "CAPS:47"], "claim": "The spec does not say how a session whose first message is a preamble starts a slash command."}
{"id": "F16", "severity": "MINOR", "blocking": false, "category": "other", "anchor": "Commands that already write a contract keep their fields and add the missing ones.", "refs": ["WC-4", "WC-5"], "claim": "Keeping existing fields conflicts with the fixed four-value status set if an existing contract uses another status word (existing contracts not checkable here)."}
{"id": "F17", "severity": "MINOR", "blocking": false, "category": "other", "anchor": "Orca does not check the file, so the coordinator opens it.", "refs": ["WC-4", "CAPS:79"], "claim": "An unverified assumption is stated as a fact."}
{"id": "F18", "severity": "MINOR", "blocking": false, "category": "other", "anchor": "`gh api repos/IronbellyOrg/IronClaude/pulls/<PR>/reviews --jq length`", "refs": ["AC-2.4"], "claim": "The count covers one page only, so an added comment on a PR with 30 or more can leave it unchanged."}
```

## Reviser brief

Review 1 of 3. Repair only the blocking findings F1, F2, F3 in the revised candidate `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`. Prefer deleting or narrowing text when the requirements are still met. Add no rule, mechanism or section that a listed finding does not call for, and cite the finding id on every addition. Report the byte size before and after, and the bytes added and deleted per finding id. Leave minor and Medium findings alone. Return the candidate once and do not award yourself a PASS. Revise only text a blocking finding names: F1 names AC-1.1 and the P1 flag scope (lines 159 and 195); F2 names WC-4's path rule (line 62) and the examples in AC-2.2 (line 200); F3 names AC-0.4 and 7.2 step 3 (lines 182 and 194). End the revision output with the fix map (`## Fix map`, `fixmap-v1`, one line per blocking id).

verdict: FAIL
