review: 1 of 3

# Spec-panel critique, round 1: Orca worker contract spec

## Header

- Command: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture` (command definition: `command.md`, read in full)
- Mode and prompt: critique; first review, so the FIRST-REVIEW prompt applies (`~/.claude/rules/prompts/document_review_loop_prompts.md:29-36`, read in full; `~` is the sandbox home)
- Candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`, sha256 `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d`
- Baseline: missing (first review; no `--baseline` given). Prior: none.
- Prompt file sha256: `ed219181156e47e6d70120730063e0b00081482d8a78b3d2633da188574ca829`
- Reviewer model: claude-haiku-5-5
- Panel: Requirements lead Wiegers, with Adzic and Cockburn (`command.md:133`). Architecture lead Fowler, with Newman, Hohpe and Nygard (`command.md:144`). Whittaker is active in every panel review (`command.md:83`), so his attack pass is included. Crispin, Gregory and Hightower are outside the two focus areas and are not run.
- Scope of this file: one reviewer's report. The three-reviewer fan-out, the MERGE rule and the VERIFY prompt are the coordinator's steps (`document_review_loop_prompts.md:34-35`, `:53-58`). No verifier was run, so the blocking findings below are not yet confirmed by a fresh-context verifier.
- Follow-up candidates are listed only. No issue was created or proposed to a person from this run.

## Evidence scope

- Checkable in this sandbox: the candidate; `.dev/orca-command-refactor/README.md`; the three inventories `inventory/commands-a.md`, `inventory/commands-b.md`, `inventory/orca-capabilities.md`; the review prompt file.
- Not checkable here, marked UNVERIFIED where a finding depends on them: every `src/superclaude/...`, `.dev/evals/...`, `.dev/codegraph-migration/...`, `/opt/Orca/...`, `CLAUDE.md` and `~/.claude/...` path that the candidate or an inventory cites. The inventories are used only as secondhand evidence for those paths.
- Checked: the candidate's cross-references to the README and to `INV-A`, `INV-B` and `CAPS` lines. I read the cited inventory lines and they say what the spec says they say, except where a finding below notes a mismatch. Section 3 counts: 21 + 22 = 43 commands, 10 + 27 + 6 = 43 (`candidate:76`), matching the inventory summaries (`commands-a.md:73` 5/13/3; `commands-b.md:278` 5/14/3).
- Checked by running commands in the sandbox, with stdin only and no file writes: the AC-C1 grep pattern (`candidate:172`), and how a raw `\|` parses in an unquoted shell.

## Mandatory output artifacts

- Guard Condition Boundary Table: triggered (the spec has conditional gates, a switch and outcome thresholds). It is produced below, scoped to the spec-level guards. Per-command gates are already tabled in the section 3 rows (`candidate:97-125`) and are not re-tabled. The scope statement is the one-line reason each omitted class is absent (FR-10).
- Pipeline Dimensional Analysis: not triggered. The spec describes a worker, a report file and a coordinator. It has no multi-stage data flow whose count changes between stages.
- State Variable Registry: not produced. `--focus correctness` is not active. Advisory only: the spec adds mutable state (ledger, `progress.json`, memory keys, the contract file). A later review could add `--focus correctness`.

## Guard Condition Boundary Table (spec-level guards, FR-10)

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|-------|----------|-----------------|----------------|--------------|-------------------|--------|
| `--unattended` switch | `candidate:51`, `candidate:228` | Zero/Empty: flag absent | none | false | Today's behaviour (`candidate:146`, SA-1) | OK |
| `--unattended` switch | `candidate:51` | Sentinel Value Match: the token appears inside quoted spec content or inside a path | `"--unattended"` in a quoted argument | undefined | The spec does not say whether a quoted or embedded token counts. Only `command.md:459` defines this, and that is for spec-panel alone. | GAP (M-13) |
| Contract present, status valid | `candidate:62-63` | Typical: `status: succeeded` | `succeeded` | not failed | `--outcome succeeded` | OK |
| Contract present, status `partial` | `candidate:63` | Legitimate Edge Case | `partial` | not failed | `--outcome succeeded`, with the body saying partial (`candidate:263`) | OK, mitigated by `candidate:73` (M-5) |
| Contract present, status empty, absent or unknown | `candidate:63` | Zero/Empty | `status:` empty, or `status: ok` | not failed | "otherwise" maps to `succeeded` | GAP (W-2) |
| Report absent | `candidate:63` | Zero/Empty | no file | true | `--outcome failed`, but only if the contract was checked before `worker_done` | GAP (W-1) |
| Contract path | `candidate:62`, `candidate:83` | Typical: adversarial `--output <dir>` | file at `<dir>/return-contract.yaml` or `<dir>/adversarial/return-contract.yaml` | contradictory | Two texts name different paths | GAP (B-1) |
| `agentWait` check | `candidate:181` | Zero/Empty: field absent (Orca never looked) | absent | pass as written | "never non-null" passes when absent | GAP (M-3) |
| Heartbeat wait | `candidate:68` | Legitimate Edge Case: a wait of 4 min 59 s | 299 s | exceeds 4 min | WC-10 requires at most 4 minutes | OK, because the rule is stated as "at most 4 minutes" |
| Sentinel check (AC-C1) | `candidate:172` | Sentinel Value Match: `orca-ide worktree list` in a command | the literal line | pattern does not match | Check prints nothing and passes | GAP (B-2) |
| Numeric capacity | none | Maximum/Overflow | none | none | Omitted: the spec defines no numeric capacity guard of its own. The three-failure circuit breaker is Orca's (`orca-capabilities.md:116`) and the spec does not restate it. | not applicable |

## Findings

Severity labels follow `command.md:259` (blocking only by consequence). Each finding gives the FIRST-REVIEW sentence (`document_review_loop_prompts.md:33`) where it is needed.

### === REQUIREMENTS ANALYSIS ===

#### B-1. WC-4 and the adversarial P1 fix name different contract paths (blocking)

- Expert: Wiegers (testability), with Fowler.
- Quotes: WC-4 says the command "writes `<output-dir>/return-contract.yaml`, where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`)" (`candidate:62`). The adversarial row says the brief "must pass `--output <dir>`" and the P1 fix is "Fix the contract filename to `<output>/adversarial/return-contract.yaml`" (`candidate:83`).
- Grading sentence: an implementer who follows WC-4 writes adversarial's contract to `<dir>/return-contract.yaml`, while the P1 fix (`candidate:83`) writes the same contract to `<dir>/adversarial/return-contract.yaml`. The coordinator opens the path WC-4 names (`candidate:73`, `candidate:182`), finds no file, and WC-5 maps the run to `failed` ("no report exists", `candidate:63`). The two texts contradict each other, so this is blocking.
- Acceptance check AC-1.4 (`candidate:198`) only asks that adversarial "names one fixed path". It does not say which, so it cannot decide the conflict.
- Evidence of the current state: adversarial real runs wrote the contract in two places (`commands-a.md:60`). The spec's own text carries that (`candidate:83`).
- Recommendation: choose one rule and make the other text follow it. The narrowest change is to replace the literal in WC-4 with "the fixed path named for each command in section 3", then put the exact path for each command in the section 3 rows, and make AC-1.4 check that path. Add no new mechanism.
- Priority: High. Quality impact: high. Without a fix, every adversarial worker fails at the coordinator's read step, or the coordinator reads a stale file.

#### B-2. AC-C1 cannot fail, so the SA-2 gate is non-functional (blocking)

- Expert: Adzic (acceptance checks as examples), with Wiegers.
- Quotes: AC-C1 is `grep -rnE '\borca(-ide)?[[:space:]]+(orchestration\|worktree\|terminal\|agent)\b' ... \| grep -v ...`, "prints nothing (SA-2, WC-8)" (`candidate:172`). SA-2 says the rule is "a hard requirement on every phase" (`candidate:142`). AC-C1 is listed under "Common checks (every phase)" (`candidate:169`).
- Grading sentence: an implementer who runs AC-C1 as written, after putting `orca-ide worktree list` into a command file, gets empty output and records SA-2 and WC-8 as passed. That command then fails with `runtime_unavailable` outside Orca (`orca-capabilities.md:147`). This is checkable in the sandbox. The pattern inside single quotes is ERE, where `\|` is a literal pipe, so the alternation never matches: `printf 'orca-ide worktree list\n' | grep -nE '\borca(-ide)?[[:space:]]+(orchestration\|worktree\|terminal\|agent)\b'` printed nothing and exited 1. The corrected form with `|` matched the same line and exited 0.
- A second defect in the same line: in the raw source, the `\|` before `grep -v` is not a shell pipe. In an unquoted shell `\|` passes a literal `|` argument (run in the sandbox: `echo a \| cat` printed `a | cat`). The second stage therefore fails with an error and never filters. The table-escape convention (`\|` renders as `|` in a GFM table cell) explains the author's intent, but the worker reads the raw source, so the command as written is wrong in both places. The same `\|` shell-pipe form appears in AC-C4 (`candidate:175`), AC-C5 (`candidate:176`) and AC-0.3 (`candidate:193`).
- Recommendation: write the pipes and the alternation as plain `|` inside each code span, and move each check out of the table cell into a fenced block, so the raw text and the rendered text agree. Add a positive control to AC-C1: the check must match a planted line (for example `orca-ide worktree list`) before it is trusted.
- Priority: High. Quality impact: high for SA-2 and WC-8, which are the only mechanical gates for them.

#### M-1. Section 1.4 says no direct-route run exists, but E3 cites one (follow-up)

- Expert: Wiegers.
- Quotes: E3 says that in the codegraph run "Orca workers invoked `/sc:adversarial`, and that work landed as PR #329", and cites a return contract with `invocation_method: "skill-direct"` (`candidate:23`). Section 1.4 says "The only end-to-end proof is the PR #329 run, and its brief told workers to run `/sc:adversarial` through an Agent-tool subagent ... so it proves the nested route, not the direct route" (`candidate:43`).
- The two texts conflict only if the P3 contract belongs to the PR #329 run. The spec does not say that and the contract is not checkable here (UNVERIFIED). `commands-a.md:13` and `commands-a.md:35` treat the skill-direct run as direct-route proof.
- Recommendation: state which run the P3 contract comes from, and whether it is direct-route proof. If it is, remove "the only end-to-end proof" from `candidate:43`. Otherwise drop the `skill-direct` citation from E3 (`candidate:23`).
- Priority: Medium. Quality impact: moderate, because Phase 0 (`candidate:158`, AC-0.4 at `candidate:194`) tests the direct route regardless.

#### M-2. WC-3 assumes a flag exists for every gate (follow-up)

- Expert: Cockburn (stakeholder and actor for the answer).
- Quotes: "re-invoke or resume the command with the answer as a flag" (`candidate:61`). Section 3 names answer flags for few gates. The tdd topic clarification (`candidate:90`) and the cleanup approval items (`candidate:103`) have none.
- Recommendation: narrow WC-3 to "where section 3 names an answer flag for that gate; otherwise the gate resolves as blocked under WC-2(c)".
- Priority: Medium. Quality impact: low to moderate. WC-3 is "may", so WC-2(c) still covers the gap.

#### M-3. The agentWait check passes when Orca never looked (follow-up)

- Expert: Adzic.
- Quotes: step 2 pass condition is "`observation.agentWait` is never non-null" (`candidate:181`). `orca-capabilities.md:129` says "An absent field means it never looked", and `orca-capabilities.md:129` also says null means Orca looked and found no wait.
- Grading sentence: an implementer following step 2 as written sees an absent field, reads it as "never non-null", and passes a worker that Orca never checked. Step 5 (`candidate:184`, transcript search for `AskUserQuestion`) is a backstop, so the consequence is limited.
- Recommendation: require the field to be present and null at least once (for example, the last `worker-show` before `worker_done`), and keep step 5 as the backstop.
- Priority: Medium. Quality impact: moderate.

#### M-4. Section 2.3 and the P0 smoke runs disagree on `--unattended` (follow-up)

- Expert: Wiegers.
- Quotes: section 2.3 says each Task's brief states "the exact command line including `--unattended`" (`candidate:73`). P0 runs three ready commands "invoked directly" (`candidate:158`), and the section 3.1 "Brief must pass" column does not list `--unattended` (`candidate:81-92`). The flag itself is only added in P1 (`candidate:159`).
- A coordinator who follows 2.3 in P0 passes a flag that does not exist yet. The spec does not say that 2.3 starts at P1.
- Recommendation: state in 2.3 that the `--unattended` requirement applies from P1, and that P0 briefs omit it.
- Priority: Medium. Quality impact: low, because the P0 runs are smoke tests.

#### M-5. WC-5 maps `partial` to `succeeded` (follow-up)

- Expert: Wiegers.
- Quotes: "`--outcome succeeded` otherwise, including `partial`" (`candidate:63`), with the decision at `candidate:263`.
- The design choice is recorded and the body's first sentence still says `partial` (`candidate:263`). The coordinator is required to open the report (`candidate:73`). No acceptance check tests what the coordinator does with a `succeeded` Task whose contract says `partial`.
- Recommendation: add one check to section 7.2 step 3 that a `partial` contract is read and not treated as complete. This is an addition, so it needs a finding id in the revision.
- Priority: Medium. Quality impact: moderate.

#### M-6. WC-1 has no owner phase or acceptance check (follow-up)

- Expert: Adzic.
- Quotes: WC-1 says "Launch setup, not commands" owns it (`candidate:59`), and cites the 45-second failure at `EVIDENCE.md:39`. Sections 6 and 7 (`candidate:158-162`, `candidate:191-210`) contain no phase, check or wrapper change for it. The only live check that would catch it is the readiness step 1 (`candidate:180`), which passes only once the agent is ready.
- Note: the readiness failure is an external fact (`commands-a.md:17`), and `EVIDENCE.md` is outside this sandbox (UNVERIFIED).
- Recommendation: either give WC-1 a phase and a check, or mark it out of scope for this spec with the owner named.
- Priority: Medium. Quality impact: high if the wrapper is not fixed. Every worker start depends on it.

#### M-7. WC-6 has no resume or fresh-directory rule for several rows (follow-up)

- Expert: Wiegers.
- Quotes: WC-6 requires that a retry "resumes from its on-disk state when given its resume flag, or ... writes each run into a fresh output directory" (`candidate:64`). Rows marked "n/a" (`candidate:112`, `candidate:124-125`) and init-lite, whose re-run "overwrites its marked report" (`candidate:87`), meet neither.
- Recommendation: for each such row, state the rule, or state that the command writes nothing to overwrite.
- Priority: Medium. Quality impact: low to moderate.

#### M-8. Reflect's `--unattended` headless trigger is undefined (follow-up)

- Expert: Cockburn.
- Quotes: P2 says "Under `--unattended`, make `--remediate` follow the existing headless auto-accept rule" (`candidate:88`). SA-6 says that rule keys on `claude --print` and must keep working "exactly as today" (`candidate:151`). The spec's UNVERIFIED item 9 says an Orca worker is assumed not to be headless (`candidate:280`).
- The spec does not say which trigger `--unattended` uses, and does not say whether an auto-accepted remediation counts as a WC-2(a) default or an outward action under WC-9 (`candidate:67`).
- Recommendation: state the trigger, and classify the auto-accept under WC-2 or WC-9.
- Priority: Medium. Quality impact: moderate.

#### M-9. The status vocabulary of existing contracts is not checked (follow-up, UNVERIFIED)

- Expert: Wiegers.
- Quotes: WC-4 says commands "that already write a contract keep their fields and add the missing ones" (`candidate:62`), and that `status` takes one of four values. The decisions table says the four-value set is fixed (`candidate:262`). The candidate cites no existing contract's status values. `commands-b.md:272` names the workflow contract's fields but not its status values.
- If an existing contract uses other status values, "keep their fields" and the fixed set conflict. The conflict cannot be checked here (UNVERIFIED).
- Recommendation: cite the status values of each existing contract, and state the mapping for any that differ.
- Priority: Medium. Quality impact: moderate.

#### M-10. The plugin mirror is unresolved, and AC-C2 does not cover it (follow-up)

- Expert: Wiegers (testability), with Adzic.
- Quotes: UNVERIFIED item 8 says the update rule for `plugins/superclaude/commands/` "was not read" and each phase must resolve it "before editing" (`candidate:279`). AC-C2 checks only `make verify-sync` (`candidate:173`).
- Recommendation: resolve the mirror rule in the spec, or add a check that covers it. Do not leave it to each phase plan.
- Priority: Medium. Quality impact: moderate.

#### M-11. The 43-command scope is not checkable here, and two commands are not in either inventory (follow-up, UNVERIFIED)

- Expert: Wiegers.
- Quotes: "The 43 commands in `cmd/`" (`candidate:76`) comes from the inventory headers (`commands-a.md:3`, `commands-b.md:3`). The sandbox has no `cmd/` directory, so the count of 43 is UNVERIFIED as a count of the real directory.
- The session's own skill listing names `sc:graph`, `sc:impact` and `sc:issue` as commands. None appears in either inventory scope. This comes from the session listing, not from a file I could check (UNVERIFIED), so it is a question for the spec's author, not a finding of fact.
- Recommendation: confirm the command list against the directory, and add or exclude the three names with a reason.
- Priority: Medium. Quality impact: moderate. A missing command would be a silent gap in the section 3 and section 4 classification.

#### M-13. The `--unattended` switch has no rule for quoted or embedded tokens (follow-up)

- Expert: Whittaker (FR-2.3, sentinel collision), with Wiegers.
- Quotes: the switch is "`--unattended`" as a flag the caller passes (`candidate:51`, D1 at `candidate:228`). The spec does not say whether the token inside a quoted argument, a path, or a spec body switches the mode.
- Trace: a spec whose body contains the literal text `--unattended` could, under a loose reader, switch a person's interactive run to unattended mode and remove its gates. `command.md:459` settles this for spec-panel only.
- Recommendation: restate the `command.md:459` rule once in the shared contract, for every command: the switch counts only as a standalone argument token outside quoted text.
- Priority: Medium. Quality impact: low to moderate, and it touches SA-1.

#### M-12. SA-3 and the adversarial P1 fix can conflict (follow-up)

- Expert: Wiegers.
- Quotes: SA-3 says "A standalone default run writes the same files it writes today" (`candidate:148`). The P1 fix moves the adversarial contract to a fixed path (`candidate:83`, `candidate:159`). SA-4 allows named defect fixes "that correct a documented defect" (`candidate:149`).
- SA-4 is a carve-out, so this is resolved in principle. SA-3 still states no exception. Read literally, a standalone run's output changes.
- Recommendation: add "except the defect fixes named in section 3 under SA-4" to SA-3.
- Priority: Medium. Quality impact: low.

### === ARCHITECTURE ANALYSIS ===

#### A-1. A worker that exits before `worker_done` has no coordinator rule (follow-up)

- Expert: Nygard (failure modes), with Hohpe.
- Quotes: WC-4 says the contract is written "on every outcome" (`candidate:62`), and WC-5 says `worker_done` is sent "exactly once" (`candidate:63`). Neither says what the coordinator does when the worker process exits with no contract and no `worker_done`.
- Orca's view of that case is in `orca-capabilities.md:37` (`live`, `unverifiable`, `exited`) and `orca-capabilities.md:126` (what proves a stall). The spec never maps those verdicts onto its contract.
- Recommendation: add one sentence to section 2.3: on `exited` with no `worker_done`, the coordinator treats the Task as failed and follows Orca's recovery steps (`orca-capabilities.md:111-112`), and does not read a contract.
- Priority: Medium. Quality impact: moderate.

#### A-2. The installed contract is a hard dependency with no fallback (follow-up)

- Expert: Newman (boundaries and installed-path rules).
- Quotes: each changed command's "## Unattended mode" section "points to the installed contract path" (`candidate:52`), which is `~/.claude/WORKER-CONTRACT.md`. WC-4 and section 2.2 depend on it.
- An older install, or a machine without the file, leaves a dangling reference. The spec defines no behaviour for a missing contract file. Installation of core files is UNVERIFIED (`candidate:52`, `src/superclaude/cli/install_core.py`, not checkable here).
- Recommendation: state what an unattended command does when the contract file is missing. The likeliest answer is to block with a clear message, not to guess the rules.
- Priority: Medium. Quality impact: low to moderate.

#### A-3. WC-11 covers shared fixed outputs only for `/sc:save` (follow-up)

- Expert: Fowler.
- Quotes: WC-11 says two workers in one worktree must not write the same file, and that default output paths carry a timestamp or slug (`candidate:69`). CAPS:115 says workers share the current worktree by default (`orca-capabilities.md:115`). Fixed outputs remain: cleanup-audit's `.claude-audit/` (`candidate:85`), and index-repo's `PROJECT_INDEX.md` (`candidate:86`), where the candidate says only that the location should be stated.
- AC-3.4 tests `/sc:save` only (`candidate:207`). No check covers the fixed-output commands.
- Recommendation: list each fixed output in the section 3 row, and state the rule for two workers that share it (one at a time, or a required distinct output path).
- Priority: Medium. Quality impact: moderate.

#### A-4. The heartbeat rule depends on an unmeasured poll duration (follow-up, UNVERIFIED)

- Expert: Nygard.
- Quotes: WC-10 needs each pr-submit poll-plus-sleep iteration "under 4 minutes" (`candidate:114`), and UNVERIFIED item 12 says the poll duration is unknown (`candidate:283`). AC-4.3 (`candidate:210`) depends on it.
- Recommendation: state the poll-duration budget as a requirement with a measured value, or move pr-submit under D3 (`candidate:238-242`) so the rule is not needed for it.
- Priority: Medium. Quality impact: moderate, and it depends on D3.

### === ADVERSARIAL ANALYSIS (Whittaker) ===

#### W-1. Sequence attack: `worker_done` before the contract is written (follow-up)

- Expert: Whittaker (FR-2.4, sequence).
- Invariant: a `failed` result is recorded when the report is missing. The spec states it in WC-5 (`candidate:63`).
- Trace: the worker sends `worker_done --outcome succeeded` before writing the contract. WC-5 says `worker_done` is sent exactly once (`candidate:63`). Orca settles the Task on a valid `worker_done` (`orca-capabilities.md:77`). The contract is then missing, but the Task is already settled as succeeded, so the "no report exists" rule never applies.
- The spec does not order the two events. WC-4 says the contract is written on every outcome (`candidate:62`), and the 7.2 step order checks the contract after `worker_done` (`candidate:182-183`).
- Recommendation: add the ordering invariant to WC-5: the contract is written and non-empty before `worker_done` is sent.
- Priority: Medium. Quality impact: moderate.

#### W-2. Zero attack: an empty or unknown status maps to success (follow-up)

- Expert: Whittaker (FR-2.1, zero and empty).
- Invariant: WC-5 maps `failed` and `blocked` to failure, and "otherwise" to success (`candidate:63`).
- Trace: a contract exists and its `status:` is empty, or holds a value the command's own older vocabulary used (see M-9). The "otherwise" clause makes the Task succeed. WC-4 says `status` is "one of" four values (`candidate:62`), but the mapping does not reject other values.
- Recommendation: map any value outside the four to `failed`, and say so in WC-5.
- Priority: Medium. Quality impact: moderate. A malformed contract silently counts as success.

## Minor notes (not blocking, not revision triggers)

- N-1. The count of 27 "needing a change" (`candidate:76`) includes pr-submit (`candidate:114`), which D3(a) would make coordinator-only (`candidate:240`). The counts would then move. State that the count is conditional on D3.
- N-2. WC-4 states as fact that "Orca does not check the file" (`candidate:62`). The spec itself lists this as UNVERIFIED (`candidate:274`, UNVERIFIED item 3), and `orca-capabilities.md:79` says the same. Change "does not" to "is assumed not to".
- N-3. Line 11 says that 11 load-bearing locations were re-read and that an evidence-validator checked about 340 citations (`candidate:285`). Neither claim is checkable here (UNVERIFIED).
- N-4. The section 3 header defines "Contract" as `<output-dir>/return-contract.yaml` (`candidate:76`), which is the B-1 conflict. It should be corrected with B-1, not separately.

## Decisions

| Decision | Options considered | Rationale |
|---|---|---|
| Blocking set | (1) B-1 and B-2 only; (2) add M-series items | Blocking requires a sentence that holds with no further assumption (`document_review_loop_prompts.md:33`). B-1 is a direct contradiction between two stated texts. B-2 is a check that does not run as written, verified in the sandbox. The M-series each needs a reading or a missing rule. |
| B-2 severity | MAJOR and blocking; MAJOR and Medium | Kept blocking: the source text as a worker reads it has both `\|` defects, and SA-2 is a hard requirement on every phase (`candidate:142`). A reader who knows the GFM table convention can read the intent, but the source does not carry it. |
| Guard table scope | (1) full table of every per-command gate; (2) spec-level guards only | Per-command gates are already in section 3 (`candidate:97-125`). Re-tabling them would duplicate it. The table scope is stated above. |
| Whittaker included | include; omit | Whittaker is active in every panel review (`command.md:83`), so his pass is included even though focus names only two areas. |
| Single reviewer | run three; run one | The FIRST-REVIEW fan-out needs three fresh contexts (`document_review_loop_prompts.md:34`). This worker can produce one report. The MERGE and VERIFY steps are left to the coordinator, as stated in the Scope section above. |

## Coverage

- Read in full: `command.md`; `document_review_loop_prompts.md`; the candidate; the README; `commands-a.md`; `commands-b.md`; `orca-capabilities.md`.
- Checked by command: the AC-C1 pattern (stdin only); the raw `\|` parse in an unquoted shell; the candidate's line numbers, by Read output with line numbers.
- Not checked, UNVERIFIED: every citation to a path outside the workspace, and the inventories' citations to those paths. Findings that depend on them are marked above.
- Focus coverage: requirements (Wiegers, Adzic, Cockburn) and architecture (Fowler, Newman, Hohpe, Nygard), plus Whittaker.

## Reviser brief

Blocking finding ids for the reviser: **B-1** and **B-2** only.

Restated rule (`command.md:263`): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, and the bytes added and deleted per finding id. Follow-up candidates M-1 to M-13, A-1 to A-4, W-1, W-2 and N-1 to N-4 are not part of this brief (`command.md:264`).

## Follow-up candidates (for the coordinator's one question per loop, `command.md:260`)

M-1 to M-13, A-1 to A-4, W-1, W-2, N-1 to N-4. No issue is created from this run. The question to the user, whether to open an issue for these, is for the coordinator, and nothing here has been sent.

verdict: FAIL
