review: 1 of 3

# Whole-document audit: orca-worker-contract-spec.md (spec-panel, critique mode)

- command: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture`
- label: whole-document audit of the final spec, a first review of the whole document (FIRST-REVIEW prompt, `~/.claude/rules/prompts/document_review_loop_prompts.md:27-32`)
- candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`
- candidate sha256: `64ace65d5ab1437b097ef30b7325e413a6e90e0ea575952d431a0fa4c73ce23e`
- baseline: none given (not a re-review; `--re-review`/`--baseline` absent)
- reviewer model used: claude-sonnet-5-5
- mode flags: `--unattended` not passed; `--iterations` ignored (one review)

## Coverage
Read in full: the command definition (`command.md`), the shared README (`README.md:1-38`), the review-loop prompts, the candidate (all 285 lines), and the three inventories at the lines the candidate cites (`commands-a.md:30-120`, `commands-b.md` rows 31-52 and 276-323, `orca-capabilities.md` lines 40-188). Cross-checked: the 10/27/6 split and the phase membership counts, the WC-4/WC-5/WC-6/WC-10 chain, the SA and AC rules against each other, and the D1-D5 gating of the phases. Not checked: any file outside the workspace. Every citation to `CLAUDE.md:N`, `src/superclaude/**`, `Makefile`, `pyproject.toml`, `~/.claude/**`, `.dev/codegraph-migration/**`, `.dev/evals/**` and `/opt/Orca/**` is UNVERIFIED here, because none of those files is inside the workspace. Citations to `INV-A:N`, `INV-B:N` and `CAPS:N` were checked against the inventories where listed below.

Experts applied in review order for the focus areas: Wiegers, Adzic, Cockburn (requirements); Fowler, Nygard, Whittaker, Newman, Hohpe (architecture). Whittaker is always active.

---

=== REQUIREMENTS ANALYSIS ===

### B-1 (CRITICAL as labelled, graded blocking) WC-4 defines the report path as a directory, but the spec's own commands and acceptance check pass a file
- Expert: Wiegers (consistency), Adzic (example), Whittaker (FR-2.2 divergence attack)
- Grading sentence: An implementer who follows the stated text as written builds a contract at `<output-dir>/return-contract.yaml` where `<output-dir>` is "the directory the coordinator passed (`--output` / `--output-dir`)" (spec line 62), and X is wrong because for `/sc:tdd` and `/sc:init-lite` the coordinator is told to pass `--output <file>` (spec lines 87, 90), so the path becomes `<file>/return-contract.yaml`, which cannot be created under a regular file, and the spec names no other location.
- Where the texts collide:
  - WC-4 (spec line 62): output dir is a directory; the contract is `<output-dir>/return-contract.yaml`.
  - 3.1 `tdd` and `init-lite` (spec lines 87, 90): `--output <file>`; their "Report today" is the file itself; no contract row is added for either.
  - AC-2.2 (spec line 200): `/sc:tdd "auth" --unattended --output <file>` must end with "contract `status: blocked` with a non-empty `blocked_question`". The contract location for this run is stated nowhere, so the check cannot be run as written.
  - Same shape for `spec-panel` (3.2 row, "add `--output`", spec line 120): the command definition in this audit treats `--output` as file-valued (`command.md:460`, "`--output` is file-valued"), so the directory reading of WC-4 does not apply to it either.
- Recommendation: state one rule for where the contract goes when the command's output flag names a file (for example, beside that file), or name a separate directory flag for the contract, and use it in WC-4 and AC-2.2.
- Priority: High. Quality impact: removes the one acceptance check (AC-2.2) that is currently unrunnable for a P2 command.

---

### Medium findings (warnings; follow-up candidates, none blocks)

**M-1 WC-4 vs WC-6: "fresh dir" and "path known before dispatch" can both hold only if the coordinator picks the directory.** WC-4 says the report path is known before dispatch (spec line 62). WC-6 lets a command satisfy retry safety by "writes each run into a fresh output directory" (spec line 64), and 3.2 gives "fresh dir" for 21 commands. If the command creates the fresh directory (for example a timestamped subdirectory), the coordinator cannot know the contract path; if the coordinator supplies it, a `worker-start --retry-of` retry that reuses the Task brief reuses the same directory. The text does not say which. Grade Medium: the implementer picks between two readings the text allows. Also `cleanup-audit` has a fixed output directory (spec line 85), so "fresh dir" cannot apply to it, which the spec acknowledges only as "one audit per worktree at a time".

**M-2 `--unattended` and the contract are not scheduled for four ready commands, yet 2.3 puts `--unattended` in every brief.** 2.3 (spec line 73) says the brief states "the exact command line including `--unattended`". 3.1 gives `brainstorm` and `init-lite` no change (spec lines 84, 87), and `index-repo` only a location statement (line 86). The P1 row (spec line 159) adds the flag to commands "listed in this row" and lists `cleanup-audit`, `index-repo`, `adversarial`, `workflow` only as "fixes". Result: these commands receive a flag no phase teaches them, and WC-4 ("written on every outcome") has no row delivering it for `init-lite`, `index-repo`, `brainstorm` (it already writes one), `cleanup-audit`. AC-1.2 (spec line 196) runs "each P1 command with `--unattended --output <dir>`", which would include `index-repo`. Medium: the worse reading (pass the flag, have it silently ignored or treated as input text) is a guess.

**M-3 `pr-submit` carries a stated "Will Not: run headless" that D3(b) and the 3.2 row do not reconcile.** The inventory records "Will Not: run headless / imply a daemon" (`commands-b.md:90`, citing `cmd/pr-submit.md:85` and `SKILL.md:225`, UNVERIFIED here). The 3.2 row (spec line 114) and D3(b) (spec line 241) give pr-submit an `--unattended` mode without addressing that prohibition. The recommendation D3(a) avoids the problem, and `pr-submit` is counted among the 27 "needing a change" although under D3(a) it gets no change and is not dispatched (spec lines 76, 139, 159). Medium: it matters only if the user picks D3(b).

**M-4 The PR #329 evidence is used both as proof and as not-proof of the direct route.** E3 (spec line 23) cites `invocation_method: "skill-direct"` in a return contract as support. Section 1.4(1) (spec line 43) says the same run's brief had workers use an Agent-tool subagent, so it "proves the nested route, not the direct route". `commands-a.md:35` reads the same field as "Proven as a direct Orca-worker skill call". The spec does not reconcile the field with the brief. The honest gap statement is present; the E3 row should not cite the field as support without saying what it means. Both sources are outside the workspace (`.dev/codegraph-migration/**`): UNVERIFIED.

**M-5 WC-5 maps outcomes from the report's `status`, but defines nothing for a report that exists and is unusable.** The mapping covers four status values and "no report exists" (spec line 63). It is silent on an empty file, invalid YAML, a missing `status` key, or a `status` outside the four values. Only the 7.2 step 4 check (spec line 183) detects these, and that is an acceptance test, not a worker rule. An implementer of the worker session has no stated outcome for that case. Medium (an undefined state, not a stated text that does harm).

**M-6 AC-C5 and SA-4 conflict with documenting the new flags in an existing Usage line.** SA-4 (spec line 149) and AC-C5 (spec line 176) require edits with no removed lines, except named defect fixes. Adding `--unattended` or `--output` to an existing `Usage` line removes that line from the diff. Neither rule says to add a second line. The command definition used for this audit does exactly that (two Usage lines, `command.md:22-23`), but the spec never states the technique. Medium: the check can fail on a correct edit.

**M-7 Guard window in WC-10.** The trigger is a single blocking call "longer than 5 minutes", the required split is "at most 4 minutes" (spec line 68). A 4 to 5 minute call is allowed by the trigger and yet exceeds the 4-minute limit that AC-4.3 enforces ("no single tool call exceeds 240 s", spec line 210). Medium: two numbers for one limit; make the trigger "longer than 4 minutes".

**M-8 Scope coverage of "43 commands in `cmd/`" is not checkable and may be incomplete.** The count is the sum of the two inventories' scope lists (`commands-a.md:3`, `commands-b.md:3`). This session's skill listing also shows `/sc:issue` (described as creating an Orca worktree and launching an agent), `/sc:graph` and `/sc:impact`, which appear in neither scope list. Whether they exist in `src/superclaude/commands/` is UNVERIFIED here. If they do, E5 ("no command, skill, agent or core file calls Orca today", spec line 25) and the AC-C1 baseline ("prints nothing", spec line 172) are wrong, and the 43 is short. A one-line directory listing in the spec would close this.

**M-9 D1 and D4 gate more phases than 6 admits.** Section 6 says Phases 1-3 need no user decision (spec line 154) and 9 says Phases 0-3 can proceed on the recommendations (line 225). D4 is said to affect auggie-review `--post-pr` and task `commit`/`push` (spec line 244), both P2. If the user answers D4(b) "Never", the P2 flag design changes. D1(b) would invalidate P0. Medium: say that P2 rework is possible, or state that the P2 rows already satisfy both D4 answers (they only turn defaults off).

**M-10 `research` under `--unattended` is not checked against WC-9.** WC-9 (spec line 67) switches off "calls a paid external run". `/sc:research` is web search by nature (spec line 116 pins only `--strategy planning`). Whether search counts as a paid external call is not stated. Medium.

---

### Minor notes
- N-1 SA-2 (spec line 147) says the only allowed Orca mention "in a changed command" is "inside the contract file"; the contract file is a core file, not a command. Reword.
- N-2 AC-C1 (spec line 172) is case-sensitive and matches only four subcommands; the spec's own placeholder `ORCA orchestration worker-start` (section 7.2) would pass it, and WC-8 forbids `worker-start`/`dispatch`/`task-create` by name.
- N-3 Within P2, `tasklist` (Stage 10.5 passes `--unattended` to reflect) depends on `reflect` getting the flag in the same phase; the order inside P2 is not stated (spec lines 122, 160).
- N-4 Section 3.1 `tdd` "ready" row relies on a topic-only STOP that resolves as blocked only after P2, so `tdd` is not "ready today" for a bare topic; the row says so in its brief column.

---

=== ARCHITECTURE ANALYSIS ===

Verdict on the decision: the structure (coordinator on top; commands stay units; one shared contract file; no Orca calls inside commands) is internally coherent and its main evidence holds against the inventories. Checks that passed:
- Counts reconcile. 43 = 10 + 27 + 6 (spec line 76); 27 = 9 (P1) + 11 (P2, section 3.2) + 4 (P3) + 3 (P4); the P2 row lists 15 because it adds the four ready commands reflect, release-split, tdd, troubleshoot (spec line 160). Inventory totals match: 5+5 ready, 13+14 needs-change, 3+3 coordinator-only (`commands-a.md:73`, `commands-b.md:278`).
- Section 4 matches the inventories: agent, git, help (`commands-a.md:87-92`), pm, spawn, swarm-wizard (`commands-b.md:282-287`).
- R1 depth-1 reasoning is quoted faithfully (`orca-capabilities.md:97-99,103`) and marked UNVERIFIED where the enforcing call sites were not traced. R3 and WC-5 agree with `orca-capabilities.md:73,76`.
- 1.4's narrowing of the 60-second evidence to the pre-input prompt matches `orca-capabilities.md:52,129`.

Architecture findings are the Medium items above: M-1 (retry and report-path ownership), M-2 (contract coverage per command), M-3 (pr-submit prohibition), M-4 (evidence framing), M-8 (scope and E5).

Fowler: the single contract file referenced by installed path respects the repo's installed-path rule (spec lines 52, 264); no objection. Nygard: failure modes are covered by `blocked`/`failed`, the circuit-breaker note (spec line 263) and release steps (7.2 step 7); the unaddressed case is M-5. Newman: only the version of `--unattended` across phases matters; SA-3 and SA-4 handle compatibility (but see M-6). Hohpe: the integration is a file hand-off plus one `worker_done`; sound, subject to B-1.

---

## Guard Condition Boundary Table
Trigger: the spec contains thresholds and guards. Rows are the guards that matter; classes that cannot occur are left out with a reason.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|-------|----------|-----------------|----------------|--------------|-------------------|--------|
| report path from output flag | WC-4, spec line 62 | Typical (flag is a directory) | `--output <dir>` | true | contract at `<dir>/return-contract.yaml` | OK |
| report path from output flag | WC-4 vs 3.1 tdd/init-lite, AC-2.2 | Legitimate Edge Case (flag is a file) | `--output out.md` | undefined | none stated | GAP (B-1) |
| report-status mapping | WC-5, spec line 63 | Typical | `status: succeeded/partial/failed/blocked` | mapped | `succeeded` or `failed` | OK |
| report-status mapping | WC-5 | Zero/Empty (empty or unparseable file; missing `status`) | `""`, `null` | undefined | none stated | GAP (M-5) |
| report-status mapping | WC-5 | Sentinel Value Match (`status` outside the set) | `"timeout"` | undefined | none stated | GAP (M-5) |
| wait-split threshold | WC-10, spec line 68 | Maximum/Overflow (call of 4 to 5 minutes) | 270 s | false (not over 5 min) | allowed by trigger, over the 4 min limit and AC-4.3 | GAP (M-7) |
| wait-split threshold | WC-10 | Typical (over 5 minutes) | 600 s | true | split into waits of at most 4 min | OK |
| readiness limit | WC-1, spec line 59 | Maximum (fallback near the limit) | 45 s | true (fails) | stated: fallback "well inside" 60 s, 30 s passes, about 45 s fails | OK |
| confidence gate | task row, spec line 121 | Typical (below 0.70) | 0.69 | true | blocked | OK |
| confidence gate | task row | Legitimate Edge Case (0.70 to 0.89) | 0.80 | n/a | not stated in the spec; inventory lists only the below-0.70 prompt (`commands-b.md:199`) | OK (no prompt at the source; not a gap) |
| `--monitor` ordinal | pr-submit row, spec line 114 | Typical | `--monitor 1` | true | refused under `--unattended` | OK |
| `--monitor` ordinal | pr-submit row | Typical | `--monitor 0`/`2` | false | not stated | OK (no gate at those ordinals per `commands-b.md:89`) |
| retry circuit breaker | WC-6, `orca-capabilities.md:116,80` | Maximum (third failure) | 3 | true | Task failed; a worker's own `failed` report does not count | OK |
| fresh-directory resume | WC-6 vs WC-4 | Legitimate Edge Case (retry reuses the brief) | same `--output` | undefined | not stated | GAP (M-1) |

Classes omitted: Zero/Empty and One/Minimal for the heartbeat, readiness and breaker guards, because those are Orca-side values the spec only quotes.

Pipeline dimensional note: the pipeline (43 inventoried, 10/27/6 split, phase assignment) conserves counts at every stage (reconciled above). The only count divergence is within the 10 ready commands: 4 have a P1 fix, 4 a P2 gate fix, and `brainstorm` and `init-lite` have none (M-2).

---

## Follow-up candidates
Medium: M-1, M-2, M-3, M-4, M-5, M-6, M-7, M-8, M-9, M-10.
Minor: N-1, N-2, N-3, N-4.
The session that ran this review asks the user once per loop whether to open an issue for these; the question was not asked in this sandbox run and no issue was created.

## UNVERIFIED citations (cannot be checked inside the workspace)
All `CLAUDE.md:N` lines (16, 50, 72-83, 74, 76, 157, 334, 408); `src/superclaude/cli/install_core.py:4,13-24,33`; `src/superclaude/core/CLAUDE.md:65`; `src/superclaude/core/HOW-WE-WORK.md:22,171,249,254` and the `grep -ci orca` result (E5); `Makefile:68-74`; `pyproject.toml:38`; every `cmd/*.md` and `sk/**` line in section 3 and 4 (the spec says 11 were re-read by its author; not re-read here); `.dev/codegraph-migration/**`, `.dev/evals/ccsession-orca-e2e-20261026/EVIDENCE.md`, `/opt/Orca/**`. The `INV-*` and `CAPS:*` citations listed under Coverage were checked and found as cited.

## Brief clauses overridden
None. The brief asked for no widening of scope, and no minor or Medium finding was graded blocking.

## Reviser brief
Repair only the blocking findings B-1 in the revised candidate `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`. Prefer deleting or narrowing text when the requirements are still met. Add no rule, mechanism or section that a listed finding does not call for, and cite the finding id on every addition. Report the byte size before and after, and the bytes added and deleted per finding id. Leave minor and Medium findings alone. Return the candidate once and do not award yourself a PASS.

verdict: FAIL
