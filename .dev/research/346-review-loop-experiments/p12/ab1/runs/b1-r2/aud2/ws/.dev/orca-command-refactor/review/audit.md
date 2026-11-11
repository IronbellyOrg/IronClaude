review: 1 of 3

# Audit: /sc:spec-panel --mode critique --focus requirements,architecture

- candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`
- candidate sha256: `e867c6d99ac7d3695eb8d12653c0adb84cc8683d98189276c8b5f83a5fe17627`
- baseline: not given (first review of the whole document; `--re-review` and `--baseline` absent, so no `baseline: missing` note is needed)
- reviewer model actually used: claude-sonnet-5-5
- mode: critique, focus requirements + architecture; Whittaker active (always on). Prompt followed: FIRST-REVIEW in `~/.claude/rules/prompts/document_review_loop_prompts.md:27-32`.
- labelled whole-document audit of the final spec. Citation form: `SPEC:N` = line N of the candidate; `INV-A:N`, `INV-B:N`, `CAPS:N` = lines of `inventory/commands-a.md`, `commands-b.md`, `orca-capabilities.md`; `README:N` = `.dev/orca-command-refactor/README.md`.

## Coverage (what was and was not checked)

- Read in full: command definition, FIRST-REVIEW prompt, README, the candidate (286 lines).
- Cross-checked against the inventories (the only checkable evidence): command counts (21 + 22 = 43; 10 ready, 27 needs-change, 6 coordinator-only recount to the same totals from the 3.1, 3.2 and 4 tables and from `INV-A:73`, `INV-B:278`); the per-phase command lists in SPEC:156-162 against the phase column of SPEC:99-125 (15 P2, 9 P1 plus 3 ready fixes, 4 P3, 3 P4 all agree); every `INV-A:N`/`INV-B:N` row citation I sampled (3, 13-14, 35-55, 62, 65-66, 68, 76-83, 90-98, 106, 113, 118, 120; `INV-B:3, 31-52, 65, 105, 107-125, 267-323`); the `CAPS:44-52, 58-80, 84-92, 97-103, 107-116, 126-131, 145-161, 177-188` quotes. All matched.
- UNVERIFIED (not checkable in this sandbox, taken as the candidate states them): every `src/superclaude/...` line (`sk/`, `cmd/`), `CLAUDE.md:N`, `src/superclaude/cli/install_core.py`, `EVIDENCE.md:N`, `.dev/codegraph-migration/...:N`, `HOW-WE-WORK.md:N`, `Makefile`, `pyproject.toml:38`, and the candidate's own claim that it re-read 11 locations (SPEC:11). One discrepancy to resolve at source: SPEC:65 and `INV-A:95` cite the pr-submit top-level rule at `sk/sc-pr-submit-protocol/SKILL.md:37-39`, while `CAPS:161` quotes the same rule at `:47-49` of the installed `~/.claude` copy; different files may differ in line numbers (UNVERIFIED which is right for `src/`).
- Not done: no command was run, no Orca call was made, nothing in the candidate was edited.

## Expert panel (selected by focus)

Requirements: Wiegers (lead), Adzic, Cockburn. Architecture: Fowler (lead), Newman, Hohpe, Nygard. Adversarial: Whittaker (after Fowler, Nygard). Crispin, Gregory and Hightower were not selected by the focus areas; testing and operations points raised below are attributed to the experts who raised them.

Panel summary: the decision (SPEC:13-45) is well argued, internally traceable and honest about its gaps (SPEC:41-45, 271-285). The per-command table is consistent with the inventories. The weaknesses are in the contract mechanics: a few places where two stated texts or a stated check cannot both hold in an edge case, and several unstated restrictions. No finding meets the blocking bar (see grading below).

## Grading note

Each finding below passed the FIRST-REVIEW grading check (`document_review_loop_prompts.md:31`). None yields a sentence "an implementer who follows the stated text as written builds X, and X is wrong because Y" that holds with no further assumption, so none is blocking. Where the label is MAJOR but the sentence needs a guess or the defect is an unstated requirement, the finding is graded Medium and sits under follow-up candidates. There are no CRITICAL findings.

---

=== REQUIREMENTS ANALYSIS ===

### F-01 (Medium, label MAJOR) Brief must carry `--unattended`, but the flag does not exist for any command until P1/P2
- Expert: Wiegers (consistency), Cockburn (actor/goal).
- Texts: SPEC:73 says the coordinator's brief states "the exact command line including `--unattended`"; SPEC:79 says the 10 ready commands run "now if the brief uses the stated flags"; the `--unattended` flag and section are added in P1 (SPEC:159) and gates in P2 (SPEC:160); AC-0.4 (SPEC:194) runs three commands directly, and its flags omit `--unattended`.
- Wrong outcome if read literally: a P0 brief built per SPEC:73 passes a flag no command defines yet; whether the command ignores it, rejects it, or treats it as free text is not stated. The implementer must guess; hence Medium.
- Recommendation: state in SPEC:73 that `--unattended` is required in briefs only from P1 onward (per command, when its row's phase is done), and that P0 briefs use the SPEC:81-92 "Brief must pass" column alone.
- Priority: Medium. Quality impact: Consistency +1.

### F-02 (Medium, label MAJOR) Contract location for file-valued `--output` can collide between parallel workers
- Expert: Whittaker (Accumulation/Sequence), Wiegers.
- Texts: WC-4 puts the contract in "the directory of the file when `--output` is a file" (SPEC:62); WC-11 forbids two workers writing the same file (SPEC:69); rows with file-valued output: tdd (SPEC:90), init-lite (SPEC:87), spec-panel (SPEC:120), explain/document (output path unspecified, SPEC:107-108).
- Attack: workers A and B run `/sc:tdd ... --output docs/tdd/a.md` and `--output docs/tdd/b.md`. Both write `docs/tdd/return-contract.yaml`; the second overwrites the first; the coordinator reads the wrong status for A.
- Why Medium: SPEC:73 tells the coordinator to state the output directory, so a careful coordinator passes distinct directories, but nothing says the directory must be unique per Task, and for file-valued `--output` the coordinator's natural choice is a shared folder.
- Recommendation: add to WC-4 or WC-11 one sentence: the output directory (or the contract file's parent) must be unique per Task; or name the contract `<output-stem>.return-contract.yaml` when `--output` is a file.
- Priority: Medium. Quality impact: Testability +0.5.

### F-03 (Medium) "Written on every outcome" is unsatisfiable when no usable output directory is known; behaviour for that case is not stated
- Expert: Whittaker (Zero/Empty), Wiegers.
- Texts: WC-4 says the file is "written on success, failure, blocked and partial outcomes, including stops before any other output exists" (SPEC:62); many 3.2 rows say only "add a report path" without saying whether it is required in unattended mode (SPEC:99-125). No row or WC states what happens when `--unattended` is passed without any output flag, or the directory cannot be created.
- Attack: `/sc:analyze src/x --unattended` with no output flag. Contract location is undefined, so the command cannot write the "blocked/failed" file the spec says always exists; WC-5 then maps "no report exists" to `--outcome failed` (SPEC:63), which hides the real cause.
- Recommendation: in WC-4 state that an unattended run with no usable output directory refuses before any work, printing the refusal in chat only (the same pattern the reviewed command file already uses, `command.md:460`), and add the case to AC-2.2.
- Priority: Medium. Quality impact: Completeness +0.5.

### F-04 (Medium) Closed `status` vocabulary conflicts with "keep their fields" for existing contracts
- Expert: Wiegers (traceability), Adzic (example).
- Texts: WC-4 requires `status` to be one of four values (SPEC:62, 262) and also says commands that already write a contract "keep their fields and add the missing ones" (SPEC:62). AC step 4 asserts `d['status'] in {'succeeded','partial','failed','blocked'}` for every command, workflow included (SPEC:183, 92). `INV-B:272` only says workflow's contract has a `status` field and is written "including `failed`"; the actual value set of workflow, brainstorm, reflect, adversarial contracts is not recorded anywhere I could check (UNVERIFIED). If any existing value differs (for example `success`), "keep their fields" and the assertion cannot both hold.
- Recommendation: record the existing `status` vocabularies in the inventory or add to WC-4 a mapping rule (existing value to the four-value set, or an added `unattended_status` field). Add the question to the UNVERIFIED list (SPEC:271-285 does not have it).
- Priority: Medium. Quality impact: Consistency +0.5.

### F-05 (Medium) `partial` maps to `succeeded`, which releases dependent Tasks, and `partial` is not defined per command
- Expert: Cockburn (goal), Hohpe (message semantics).
- Texts: WC-5 and Decisions (SPEC:63, 263); Orca keeps dependents of a failed Task blocked (`CAPS:90`), so a `succeeded` outcome lets the coordinator start dependents. The spec never defines what `partial` means for any command (which deliverables must exist).
- Risk: an auditing run that skipped half its passes reports `partial`, Orca marks the Task completed, and a dependent worker starts on incomplete input. SPEC:263 mitigates by keeping `partial` in the first body sentence and SPEC:73 says the coordinator opens the report, so this relies on the coordinator reading before dispatching dependents, which is a guess.
- Recommendation: add one line to SPEC:73: the coordinator must read the contract `status` before starting any dependent Task, and treats `partial` as not-yet-satisfied unless the brief says otherwise.
- Priority: Medium. Quality impact: Completeness +0.5.

### F-06 (Medium) Sentinel collision: `--unattended` inside free-text input
- Expert: Whittaker (Sentinel Collision).
- Texts: D1 (a) selects an explicit flag (SPEC:228) and SA-1 requires identical behaviour without it (SPEC:146); the spec does not say how the flag is recognised. Free-text commands take a topic or quoted content (`/sc:tdd "<topic>"`, `/sc:troubleshoot "login fails"`, SPEC:228, 90-91).
- Attack: `/sc:troubleshoot "users type --unattended into the form and it fails"` run by a person. If the command scans the whole argument string, the person's session silently loses every prompt and gate, breaking SA-1.
- Recommendation: add to section 2.1 (or D1 (a)) that the switch counts only as a standalone argument token outside any quoted argument.
- Priority: Medium. Quality impact: Correctness (SA-1) +0.5.

### F-07 (Medium) Permission and trust dialogs are not covered by WC-1 or WC-2
- Expert: Cockburn (secondary actor), Nygard (failure mode).
- Texts: WC-1 covers launch-path prompts (SPEC:59); WC-2 covers prompts a command raises itself (SPEC:60). A worker session can still park on a Claude Code tool-permission prompt (for example a Write or Bash outside its allowed set). Orca reports such a worker as "waiting, healthy, not failed" (`CAPS:52`, `CAPS:129`), and the spec's own Section 1.4 (2) calls this the silent-stall mode. The coordinator brief (SPEC:73) names output directory, authorized actions and worktree, but not the worker's permission mode.
- Recommendation: add to SPEC:73 that the brief must state or the launch setup must fix the worker permission mode so that no tool prompt fires for the declared outputs; and let the SPEC:181 `agentWait` check catch the rest.
- Priority: Medium. Quality impact: Completeness +0.5.

### F-08 (Medium) A retry of `/sc:roadmap` without the resume flag starts fresh in the same directory
- Expert: Whittaker (Sequence), Nygard.
- Texts: WC-6 requires a retry worker not to corrupt the first attempt's output and says commands with a resume flag either resume when it is given or, without one, write a fresh directory (SPEC:64). The roadmap row says "resume only when passed" and AC-3.2 expects "starts fresh" with an existing `<dir>/.session-memory.md` and no resume flag (SPEC:118, 205). That start-fresh happens in the same `<dir>`, which overwrites the first attempt's state files.
- Why Medium: it depends on the coordinator passing the same `--output` on a retry; SPEC:73 does not forbid or require it.
- Recommendation: state in the roadmap row (or WC-6) that without the resume flag the command writes into a new subdirectory, or that the coordinator must pass a new `--output` on any retry.
- Priority: Medium. Quality impact: Consistency +0.3.

### F-09 (Medium) The fan-out example in 1.3 does not say how the consumer handles fewer inputs than workers (count divergence)
- Expert: Fowler, Whittaker (Pipeline Dimensional Analysis, FR-17 to FR-19).
- Text: SPEC:39 gives "several `/sc:troubleshoot` workers, then one `/sc:adversarial` worker on their reports" as the way to get per-unit records. Workers can end `blocked`, `failed`, or `partial` (WC-2, WC-5), so the report count M may be below the worker count N. `/sc:adversarial` takes 2-10 artifacts (skill listing; the inventory column for adversarial is `INV-A:35`). The spec does not say whether the coordinator dispatches the consumer on fewer than N reports, retries, or stops. See the Quantity Flow Diagram below.
- The heuristic grades a mismatch CRITICAL only when the spec assumes count conservation. The text assumes nothing either way, so this is a missing requirement and is graded Medium.
- Recommendation: add one sentence to SPEC:39 or SPEC:73: the coordinator dispatches the consumer only on the reports whose contract `status` is `succeeded`, and stops if fewer than the consumer's minimum remain.
- Priority: Medium. Quality impact: Completeness +0.3.

=== ARCHITECTURE ANALYSIS ===

### F-10 (Medium) Tasklist row asserts the nested reflect depth fits Claude Code's nesting limit without counting it, and passes `--unattended` into a nested remediation chain
- Expert: Fowler, Newman, Nygard.
- Texts: SPEC:122 says the Stage 10.5 reflect fan-out "runs one layer below the worker, inside Claude Code's nesting limit, `INV-A:14`", and makes it pass `--unattended` to each reflect so the headless auto-accept rule applies. `INV-A:14` says nesting goes to three layers below the main conversation, with the Agent tool withheld at the limit. `INV-B:295` recommends removing this nested fan-out, and `INV-B:314`, `INV-B:322` record that who answers the nested remediation offer and whether a subagent can spawn agents are UNVERIFIED. Reflect itself fans out (Tier 1 two agents, Tier 2 two to three reviewers plus an adversarial merge, `INV-B:111`), so layers are worker, tasklist subagent, reflect agents, adversarial agents. The spec does not count them.
- The row therefore treats an unverified depth claim as settled, and turns on an auto-accepted remediation chain (reflect handing off to workflow or task-builder, `INV-B:109`) N times inside subagents with no report path in the contract.
- Recommendation: list the depth count in the row, add the question to the UNVERIFIED list, and consider `--no-reflect` in the brief (the row already notes it is ready today) as the default for workers.
- Priority: Medium. Quality impact: Completeness +0.5.

### F-11 (Medium) AC-C1 scans `src/superclaude/core`, where P0 adds Orca-describing text
- Expert: Fowler (boundary), Wiegers (testability).
- Texts: AC-C1 greps `src/superclaude/{commands,skills,agents,core}` for `orca(-ide) orchestration|worktree|terminal|agent` and requires no output (SPEC:172). P0 adds `src/superclaude/core/WORKER-CONTRACT.md` with a coordinator brief template and an Orca section in `core/HOW-WE-WORK.md` (SPEC:158, 150). SA-2 allows an Orca mention only "inside the contract file" (SPEC:147). If either new file writes a literal `orca-ide orchestration ...` command, AC-C1 fails on the spec's own deliverables.
- Recommendation: exclude `core/WORKER-CONTRACT.md` and the Orca section of `core/HOW-WE-WORK.md` from AC-C1, or state that both files refer to Orca commands only as "the preamble's `ask`/`send` command". Note SPEC:61 already does the second for WC-3.
- Priority: Medium. Quality impact: Testability +0.5.

### F-12 (Medium) SA-1 says output paths stay exactly as today; P3 reconciles output filenames
- Expert: Fowler (interface consistency), Wiegers.
- Texts: SA-1 and the section 5 lead sentence ("exactly today's behaviour", SPEC:142, 146) against P3 reconciling `validate/validation-report.md` with `02-consolidated-report.md`, the roadmap flag surface and the validate-tests default target (SPEC:118, 124-125, 161). SA-4 (SPEC:149) allows these as documented-defect fixes, so the intent is clear; the conflict is only in the absolute wording of SA-1 and of the "hard requirement" sentence.
- Recommendation: add "except the defect fixes named in SA-4" to SA-1.
- Priority: Medium. Quality impact: Consistency +0.3.

### F-13 (Medium) Evidence entry E3 cites the "skill-direct" contract as proof while 1.4 says the PR #329 run was subagent-wrapped
- Expert: Fowler, Wiegers (evidence).
- Texts: E3 (SPEC:23) cites `invocation_method: "skill-direct"` for "it has worked before"; 1.4 (1) says the brief told workers to run `/sc:adversarial` "through an Agent-tool subagent", so the run "proves the nested route, not the direct route" (SPEC:43). `INV-A:13` treats "skill-direct" as the direct route. The two paragraphs do not reconcile the field value with the brief. The decision stays supported either way because P0 tests it (SPEC:158), so this is a wording defect in the evidence table.
- Recommendation: in E3 say which route the contract field names and that the brief used a subagent, or drop the field as evidence.
- Priority: Low-Medium. Quality impact: Clarity +0.2.

=== ADVERSARIAL ANALYSIS (Whittaker) ===

Format per the command: attack, invariant location, trigger, trace.

- A-1 **Sentinel Collision**: invariant "`--unattended` marks a no-person caller" (SPEC:51, 228). Triggering condition: the token appears inside free text. Trace: before, a person runs `/sc:troubleshoot "... --unattended ..."` with prompts on; after, the gate list collapses and SA-1 (SPEC:146) fails. See F-06.
- A-2 **Accumulation**: invariant "contract at the output directory" (SPEC:62) and "two workers never write the same file" (SPEC:69). Trigger: two Tasks, file-valued `--output` in one folder. Trace: contract A written, contract B overwrites, coordinator reads B for A. See F-02.
- A-3 **Zero/Empty**: invariant "contract written on every outcome" (SPEC:62). Trigger: no output flag. Trace: no path, no file, WC-5 reports `failed` without cause. See F-03.
- A-4 **Sequence**: invariant "a retry must not corrupt the first attempt" (SPEC:64). Trigger: roadmap retried with the same `--output` and no resume flag. Trace: `.session-memory.md` present, then "starts fresh" (SPEC:205), file replaced. See F-08.
- A-5 **Divergence**: invariant "split long waits to at most 4 minutes" (SPEC:68). The text requires splitting a call "longer than 5 minutes" into waits "of at most 4 minutes"; a single call of 4.5 minutes is neither required to be split nor allowed (above 4). Minor (the Decisions row at SPEC:266 shows the intent is a 4-minute margin). Fix by saying "any call longer than 4 minutes".
- A-6 **Divergence**: `partial` versus `succeeded` (SPEC:63): the boundary between a partial deliverable and a failed one is undefined per command. See F-05.

## Guard Condition Boundary Table

Guards identified in the candidate (thresholds, flags, status mapping). Classes that cannot occur are left out with a one-line reason.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|-------|----------|-----------------|----------------|--------------|-------------------|--------|
| `--unattended` present | SPEC:51, 228, 146 | Zero/Empty | flag absent | false | today's behaviour, no new files (SA-1, SA-3) | OK |
| `--unattended` present | SPEC:51, 228 | Sentinel Value Match | token inside quoted free text | unspecified | not stated | GAP (F-06, Medium) |
| output directory known | SPEC:62, 73 | Zero/Empty | no output flag | unspecified | not stated | GAP (F-03, Medium) |
| output directory known | SPEC:62 | Legitimate Edge Case | `--output` is a file, shared folder | true | contract in the file's directory; collision not addressed | GAP (F-02, Medium) |
| `status` in four-value set | SPEC:62, 183, 262 | Legitimate Edge Case | existing contract with another value | unspecified | "keep their fields" vs closed set | GAP (F-04, Medium) |
| `partial` to `succeeded` | SPEC:63, 263 | Legitimate Edge Case | partial deliverable | true | `succeeded`, `partial` named in body | OK (see F-05 follow-up) |
| no report exists | SPEC:63 | Zero/Empty | contract absent | true | `--outcome failed` | OK |
| wait split (4 and 5 minutes) | SPEC:68, 266 | Maximum/Overflow | single call 4 to 5 minutes | unspecified | neither required nor allowed | GAP (A-5, Minor) |
| wait split | SPEC:68 | Typical | 3-minute poll | false | no split needed | OK |
| nesting depth 1 | SPEC:33, 66 | Maximum/Overflow | worker calls `worker-start` | true | refused `nested_worker_depth_exceeded` (call sites UNVERIFIED, SPEC:33, 276) | OK |
| readiness limit 60 s | SPEC:59 | Maximum/Overflow | prompt fallback above about 45 s | true | fails again (`EVIDENCE.md:56` via `CAPS:49`) | OK |
| task confidence below 0.70 | SPEC:121 | Typical | 0.50 | true | blocked | OK |
| task confidence below 0.70 | SPEC:121 | Legitimate Edge Case | 0.70 to 0.89 | false | not stated (`cmd/task.md` not checkable) | GAP (UNVERIFIED, Minor) |
| `--monitor 1` refused | SPEC:114 | Legitimate Edge Case | `--monitor 0, 2, 3` | false | not stated, pr-submit stays coordinator-side by default (D3 a) | OK |
| `ask` timeout | SPEC:61 | Maximum/Overflow | timeout | true | resume same message ID (`CAPS:60`); default value UNVERIFIED (SPEC:281) | OK |
| `consumer_fenced` | SPEC:70 | Legitimate Edge Case | fenced mid-run | true | stop, no `worker_done` | OK |
| nesting-depth check for tasklist | SPEC:122 | Maximum/Overflow | reflect Tier 2 under a subagent | unspecified | "inside the limit" asserted, not counted | GAP (F-10, Medium) |

Blank-behavior rule (FR-9): the blank cells above are the GAP rows; all are graded Medium or Minor under the consequence rule because each needs a guess about what an implementer picks, or is a missing requirement rather than a stated text that does harm.

## Quantity Flow Diagram (Pipeline Dimensional Analysis)

Triggered by the coordinator split in SPEC:39 and the per-phase pipeline of SPEC:154-162. Counts below are the candidate's own.

```text
[Commands in cmd/: 43] --> [Inventory verdict split] --> [10 ready] + [27 needs-change] + [6 coordinator-only]  (sum 43, conserved: SPEC:76, INV-A:73, INV-B:278)
[27 needs-change] --> [Phase split] --> P1: 9 + P2: 11 + P3: 4 + P4: 3  (sum 27, conserved: SPEC:99-125)
[10 ready] --> [fix phase] --> P1 fixes: 3 + P2: 4 + no fix: 3  (sum 10, conserved: SPEC:83-92)
[N troubleshoot workers] --> [M reports with status succeeded (M <= N)] --> [Consumer: 1 adversarial worker, expects 2-10 artifacts]  <-- MISMATCH when M < 2 or M < N (F-09)
[unattended run] --> [contract file: exactly 1 per Task] --> [coordinator reads 1] ; with file-valued --output, K Tasks in one folder yield 1 file, not K  <-- MISMATCH (F-02)
```

## Minor notes (never fail the review)

- N-1: SPEC:196 (AC-1.2) says "each P1 command", while the P1 Commands column (SPEC:159) lists 9 plus 3 fixes and the P1 scope says "every command in sections 3.1 and 3.2 except load". Brainstorm, init-lite and workflow carry the section in P1 but are in no P1 command list. Say "every command carrying the section".
- N-2: `agentWait` in 7.2 step 2 passes when the field is "never non-null" (SPEC:181); `CAPS:129` says an absent field means Orca never looked. Require a present `null`.
- N-3: SPEC:85 and the reflect row (SPEC:88) leave `docs/memory/reflect/deviation-patterns-<slug>.md`, a tracked file written by reflect UC-2 (`INV-B:114`), outside WC-9 and WC-11. Two reflect workers on the same slug write one tracked file. Add a one-line note to the reflect row.
- N-4: SPEC:139 says `/sc:load` and `/sc:recommend` are better on the coordinator side, yet `recommend` gets P2 work and appears in AC-1.1/2.1 assertions. Fine, but say so in the row.
- N-5: UNVERIFIED item 14 (SPEC:285) credits a validator pass over about 340 citations; the audit could not reproduce it, only the inventory-side subset above.
- N-6: SPEC:65 and SPEC:161 cite pr-submit `SKILL.md:37-39`; `CAPS:161` cites `:47-49` for an installed copy. Check both.

## Follow-up candidates (Medium and minor)

Medium: F-01, F-02, F-03, F-04, F-05, F-06, F-07, F-08, F-09, F-10, F-11, F-12, F-13.
Minor: A-5, N-1 to N-6, and the task 0.70-0.89 band (UNVERIFIED).

Per the command, the session that runs a review asks the user once per loop whether to open an issue for these; this run is a sandboxed worker with no user channel, so no question was asked and no issue was created. They are recorded only.

## Brief clauses overridden

None. The brief did not widen scope past the whole-document first review, and no minor or Medium finding was graded blocking.

## Reviser brief

None. There are no blocking finding ids, so there is nothing for a reviser to repair.

verdict: PASS
