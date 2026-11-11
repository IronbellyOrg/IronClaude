review: 1 of 3

# Spec-panel critique: orca-worker-contract-spec.md

- Command: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture`
- Candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`, sha256 `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d` (matches the hash in lint-1.md:1)
- Baseline: none given (first review, `--re-review` and `--baseline` absent)
- Reviewer model used: claude-sonnet-5-5
- Prompt followed: FIRST-REVIEW in `~/.claude/rules/prompts/document_review_loop_prompts.md:27-33` (read in full, plus the command's Review Loop section)
- Coverage: all 285 lines of the candidate read; the five inventory citations marked below and the README read. Panel: Wiegers, Adzic, Cockburn (requirements); Fowler, Newman, Hohpe, Nygard (architecture); Whittaker (always active). Source-tree citations (`cmd/...`, `sk/...`, `CLAUDE.md:N`, `src/...`) are UNVERIFIED, because the workspace holds only `.dev/orca-command-refactor/`. The `INV-A`, `INV-B` and `CAPS` citations I spot-checked are cited accurately: `INV-A:14,95,106`, `INV-B:65,105,311,323`, `CAPS:52,66-67,73,80,98,130,149,151,155-156,178,180,186-187`.

## Lint evidence

`.dev/orca-command-refactor/review/lint-1.md:3-5` reports "Checks: REF. Findings: 0. No findings." There is no lint id to confirm or dismiss. A lint result of zero does not clear the candidate, and the findings below are independent of it.

## Findings

Grading sentence format: "An implementer who follows the stated text as written builds X, and X is wrong because Y."

### === REQUIREMENTS ANALYSIS ===

**F-1 | MAJOR, blocking | Wiegers, Adzic | AC-1.1 cannot pass against the phase scope and decisions the spec itself states**
- Stated texts. AC-1.1 (spec:195) asserts that "every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`" and passes only then. Four other texts contradict it:
  - `/sc:load` has Report "none (see note)", Resume "n/a", Phase "P1 (usage line only)" (spec:112). The Decisions table says a report file for load "would be an unrequested addition" (spec:265).
  - `/sc:pr-submit` is in section 3.2 (spec:114). D3's recommended option (a) says "no pr-submit changes in Phase 4" (spec:240), and section 9 says Phases 0-3 "can proceed on the recommendations" (spec:225).
  - `/sc:implement` and `/sc:post-release` are Phase P4 (spec:109, spec:113, spec:162), yet AC-1.1 is a P1 check.
  - Section 4 says coordinator-only commands get no section (spec:128), and spec:139 says pr-submit is a worker candidate only if D3 is accepted.
- Sentence: An implementer who follows the stated text as written builds the Phase 1 gate so that load, implement, post-release and pr-submit each get an `## Unattended mode` section that names `return-contract.yaml`. That is wrong because load is specified to write no report (spec:112, spec:265), pr-submit is specified to stay untouched under the recommended D3 (spec:240), and implement and post-release are specified as P4 work awaiting D2-D4 (spec:162). If the implementer skips them, AC-1.1 fails and Phase 1 cannot pass. If the implementer adds them, the work contradicts spec:112, spec:240 and spec:265.
- Why blocking: two stated texts contradict, and the acceptance criterion cannot pass on the recommended path. The spec's P1 scope line (spec:159, "the `--unattended` flag accepted by every command in sections 3.1 and 3.2") repeats the same over-broad scope.
- Recommendation (Wiegers): scope AC-1.1 and spec:159 to the commands each phase actually changes, and state that load, and pr-submit under D3(a), are excluded.
- Priority: High. Quality impact: Phase 1 exit criterion becomes checkable.

**F-2 | MAJOR, blocking | Nygard, Wiegers | AC-C1 (every phase) forbids text that SA-2 and P0 require**
- Stated texts. SA-2 allows an Orca mention "as an example of a caller's question channel inside the contract file" (spec:147). WC-3 tells the worker session to use "the preamble's `ask` command" and gives the brief template a role (spec:61, spec:158). P0 puts `WORKER-CONTRACT.md` in `src/superclaude/core/` and adds an Orca section to `HOW-WE-WORK.md`, also in `src/superclaude/core/` (spec:52, spec:158, spec:150). AC-C1 greps `src/superclaude/core` for `orca(-ide)? (orchestration|worktree|terminal|agent)` and excludes only `skills/ccsession-tag/`. Its pass condition is "prints nothing" (spec:172). It is a common check, so it applies to every phase (spec:167).
- Sentence: An implementer who follows the stated text as written writes the contract file and the routing-guide Orca section with the literal command `orca orchestration ask` or `orca-ide orchestration ...`, as SA-2 permits. That is wrong because AC-C1 then prints those lines and every phase check fails. The alternative, writing no such literal, contradicts WC-3, the P0 brief template (spec:158) and the Orca section P0 adds to `HOW-WE-WORK.md` (spec:150), which exist to tell people and agents what to run. The spec also records that `HOW-WE-WORK.md` has zero Orca mentions today (spec:25), so the baseline hides the conflict.
- Why blocking: two stated texts contradict (SA-2 allowance versus the AC-C1 pass condition).
- Recommendation (Fowler): exclude `src/superclaude/core/WORKER-CONTRACT.md` and the Orca section of `HOW-WE-WORK.md` from AC-C1, or tighten AC-C1 to `commands`, `skills`, `agents` only, and say so in SA-2.
- Priority: High.

### === ARCHITECTURE ANALYSIS ===

The decision itself (section 1: Orca on top, commands unchanged as units of work) is consistent with the README goal (`.dev/orca-command-refactor/README.md:6`) and with its evidence. Section 1.4 states the proof gaps honestly (spec:41-45; `INV-B:323`; `CAPS:156,178,186-187`). Counts reconcile: the 3.1 table lists 10 commands, the 3.2 table 27 and section 4 lists 6, which sums to the 43 the spec claims (spec:76; 21 + 22 per `INV-A`/`INV-B` headers). No blocking architecture finding beyond F-1 and F-2.

### Guard Condition Boundary Table

Guards identified in the spec text. Classes that cannot occur for a guard are omitted with a one-line reason.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|-------|----------|-----------------|----------------|--------------|-------------------|--------|
| `--unattended` token | WC-2, spec:60 | Zero/Empty (flag absent) | no flag | false | Today's behavior unchanged (SA-1, spec:146) | OK |
| `--unattended` + `--interactive` | spec:104,108,103,110 vs spec:83-84,89 | Legitimate Edge Case | both flags | both apply | Refused for cleanup, improve, explain, roadmap, business-panel (3.2 rows); for adversarial, brainstorm, release-split the brief "never" passes it (3.1 rows), with no refusal specified | GAP |
| `--unattended` + resume flag | spec:64, spec:118 | Legitimate Edge Case | both | both apply | Stated for roadmap (spec:118); unstated elsewhere | GAP |
| `check` returns `consumer_fenced` | WC-12, spec:70 | Sentinel Value Match | `consumer_fenced` | true | Stop, no `worker_done` | OK |
| confidence threshold | task row, spec:121 | Maximum/Overflow (exactly 0.70) | 0.70 | unspecified | "below 0.70 resolves as blocked"; exactly 0.70 is not stated, which the source command may define (UNVERIFIED, `cmd/task.md` not in workspace) | GAP |
| single tool-call wait | WC-10, spec:68 | Maximum/Overflow | wait > 5 min | true | Split into waits of at most 4 minutes | OK |
| single tool-call wait | WC-10, spec:68 | Legitimate Edge Case | wait between 4 and 5 min | ambiguous | Rule says "longer than 5 minutes" triggers the split and the split target is 4 minutes; a 4.5 minute wait is neither required nor forbidden | GAP |
| `report status` to `--outcome` | WC-5, spec:63 | Zero/Empty (no report) | no file | n/a | `--outcome failed` | OK |
| output dir | WC-4, spec:62 | Zero/Empty | no `--output-dir` given | false | Unattended command with no output dir: not specified for the commands listed "add `--output`" (spec:99-125), though WC-4 says the directory is "the one the coordinator passed" | GAP |

Omitted classes: "One/Minimal" is left out for flag guards because a flag is present or absent; "Typical" rows are covered by the OK rows above.

GAP handling under FR-8/FR-9: each GAP above is a requirement the spec never states or a reading choice, not a stated text that does harm, so all are Medium (see M-5 to M-8), not blocking.

### Whittaker adversarial findings

- I can break this specification by **Divergence Attack**. The invariant at **WC-4 (spec:62, "writes `<output-dir>/return-contract.yaml`") and AC-1.1/7.2 step 3 (spec:182, spec:195)** fails when **a command's existing contract lives elsewhere**. Concrete attack: the `workflow` row writes `.dev/tasks/to-do/<id>/return-contract.yaml` (spec:92), `adversarial` is fixed to `<output>/adversarial/return-contract.yaml` (spec:83), and `cleanup-audit` writes `.claude-audit/pass<N>-summary.md` (spec:85). Before: coordinator passes `--output D` and expects `D/return-contract.yaml`. After: `worker_done --report-path D/return-contract.yaml` names a file that does not exist, and the coordinator reads nothing. Severity: Medium, because the spec's 3.1 table names the actual report location per command and the brief template can state it; it is not a stated text that does harm (see M-1).
- I can break this specification by **Sequence Attack**. The invariant at **P1 scope (spec:159) versus WC-2 (spec:60)** fails when **a coordinator dispatches a P2 or P4 command after only P1 has shipped**. Concrete attack: after P1, `/sc:task <x> --unattended` accepts the flag (spec:159) but confidence below 0.70 still prompts, because the gate conversion is P2 (spec:121, spec:160). The worker stalls with `agentWait` and no `worker_done`. Nothing in the spec tells the coordinator not to dispatch a command before its phase lands. Severity: Medium (the spec assumes sequential adoption but does not state a dispatch-readiness rule; see M-2).
- I can break this specification by **Sentinel Collision Attack**. The invariant at **WC-5 (spec:63)** fails when **a coordinator reads only the Orca outcome**. Concrete attack: a run whose contract says `partial` or an audit with verdict FAIL ends `--outcome succeeded` (spec:63, spec:263). A coordinator that branches on the outcome alone treats incomplete work as complete. Mitigated by the body's first sentence and the WC-4 file, so Medium at most; it is a documented decision, not a defect (note N-1).
- Zero/Empty, Accumulation: no further spec-level breaks found beyond the GAP rows above.

## Follow-up candidates (Medium findings, do not trigger a revision)

- **M-1 (Medium)** Report location is not uniformly `<output-dir>/return-contract.yaml`: workflow (spec:92) and cleanup-audit (spec:85) write elsewhere, adversarial gets `<output>/adversarial/` (spec:83, AC-1.4 spec:198), while WC-4 and AC 7.2 step 3 (spec:62, spec:182) state one path. Reading allowing the worse choice: implementer picks WC-4's path and breaks the existing consumers. State per-command report paths in the brief template or amend WC-4.
- **M-2 (Medium)** No rule that a coordinator dispatches a command in unattended mode only after the phase that converts its gates has landed (spec:159-162; Whittaker Sequence Attack above).
- **M-3 (Medium)** AC-C5 requires `git diff -U0 ... | grep -E '^-[^-]'` to print nothing for command files without a named defect fix (spec:176), but adding `--unattended` to a one-line `Usage` block, which SA-4 allows as a "new flag" (spec:149), rewrites an existing line and prints a `-` line. Whether the implementer adds a new line or edits the usage line is a guess; state which.
- **M-4 (Medium)** SA-3 allows new files "only in unattended mode or when the caller passes the new output flag" (spec:148), whereas WC-4 writes the contract only in unattended mode (spec:62) and AC-1.3 tests only the no-flag case (spec:197). Behavior of a plain run that passes only the new `--output` flag is unspecified.
- **M-5 (Medium)** `--unattended` combined with `--interactive` is refused for five commands (spec:102-103,108,110,118) but only avoided by the brief for adversarial, brainstorm, release-split (spec:83-84,89). Specify one rule (guard table GAP row).
- **M-6 (Medium)** Behavior of the unattended mode when `--output` / `--output-dir` is missing is not stated for the "add `--output`" commands (spec:99-125); WC-4 only says "the directory the coordinator passed" (guard table GAP row). Resolve as blocked, or default to a timestamped directory (WC-11, spec:69).
- **M-7 (Medium)** WC-10 threshold: "longer than 5 minutes" triggers the split, the target is "at most 4 minutes" (spec:68, spec:266); waits of 4 to 5 minutes are unspecified. Use one number.
- **M-8 (Medium)** The `/sc:task` threshold "below 0.70" leaves exactly 0.70 to the source command (spec:121). UNVERIFIED against `cmd/task.md`.
- **M-9 (Medium, evidence)** Every `cmd/...`, `sk/...` and `CLAUDE.md:N` citation, and the spec's own claims of 11 re-reads and a 340-citation check (spec:11, spec:285), are UNVERIFIED in this review because those files are outside the workspace. `INV-*` and `CAPS` citations spot-checked held.

## Notes (MINOR, never fail the review)

- N-1 `partial` mapping to `succeeded` is a recorded decision (spec:263); keep, but the brief template should tell coordinators to read `status` as well as `--outcome`.
- N-2 "ladder rung 2" in the Decisions table (spec:261) is undefined in the spec.
- N-3 The 3.1 heading "Ready today" overlaps with small P2 gate changes for reflect, release-split, tdd, troubleshoot (spec:88-91, spec:160); the column does say so.
- N-4 Section 1.2 E5 and spec:25 depend on greps run on 2026-11-02 that cannot be re-run here (UNVERIFIED).

## Reviser brief

Blocking finding ids only: **F-1, F-2**. Revise only text a blocking finding names. Add no rule, mechanism or section that no blocking finding calls for. Each added paragraph or table cites its finding id. Prefer deleting or narrowing to adding. Report the byte size before and after, and the bytes added and deleted per finding id. Leave Medium and minor findings alone. Return the candidate once and do not award yourself a PASS.

Brief clauses overridden: none.

verdict: FAIL
