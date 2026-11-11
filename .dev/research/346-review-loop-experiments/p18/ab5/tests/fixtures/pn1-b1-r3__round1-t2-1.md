review: 1 of 3

# /sc:spec-panel critique: orca-worker-contract-spec.md (first review)

- Mode: `--mode critique`, `--focus requirements,architecture`. Review loop: FIRST-REVIEW prompt (`~/.claude/rules/prompts/document_review_loop_prompts.md`, read in full).
- Candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (285 lines), sha256 `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d`.
- Baseline: missing (first review; no `--baseline` or `--re-review` given).
- Reviewer model: claude-haiku-5-5. Panel: single reviewer, because `superclaude` is not installed in the sandbox (`command -v superclaude` printed nothing), so `superclaude review panel resolve` was not run. This is stated in the loop summary.
- Shorthand used for cites: `SPEC` = `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`; `INV-A` = `.dev/orca-command-refactor/inventory/commands-a.md`; `INV-B` = `.dev/orca-command-refactor/inventory/commands-b.md`; `CAPS` = `.dev/orca-command-refactor/inventory/orca-capabilities.md`; `README` = `.dev/orca-command-refactor/README.md`.

## Coverage

- Read in full: SPEC, README, INV-A, INV-B, CAPS, and the review prompt file. The sandbox holds only `.dev/orca-command-refactor/`; it has no `src/` tree, no `pyproject.toml`, no `CLAUDE.md`, no `.dev/evals/`, no `.dev/codegraph-migration/`, and no `~/.claude/` command or skill files.
- Citation checks against readable files: I checked about 40 of the `INV-A` and `INV-B` cites in SPEC (the section 3 rows, the section 4 rows and the UNVERIFIED list); each lands on the content SPEC attributes to it. I did not check the rest. Every `CAPS:N` cite I checked matches the numbered line (CAPS:44-45, 46, 52, 58-61, 64, 66-67, 68, 72-74, 76, 79, 80, 84-92, 97-103, 107-113, 115, 116, 125, 128, 130, 145, 149, 151, 155, 158, 159-161, 178, 180, 186-188). Counts agree: INV-A has 21 commands, INV-B 22, and the 43 SPEC rows split 10 / 27 / 6.
- UNVERIFIED (cannot be checked in the sandbox): every SPEC cite to `src/superclaude/...`, `.dev/evals/...`, `.dev/codegraph-migration/...`, `pyproject.toml`, `CLAUDE.md`, `~/.claude/...`, and the `[G]`, `[H:...]` guide lines that CAPS quotes but that are not in the workspace. I judged SPEC on its internal consistency and on what the inventories say, and did not rely on any UNVERIFIED cite.
- Mandatory artifacts: the Guard Condition Boundary Table is triggered (SPEC has many conditional rules, timeouts, thresholds and flags), so it is given below. Pipeline Dimensional Analysis is not triggered: SPEC's "phases" in section 6 are ordering of work, not a data flow whose count changes between stages, so no Quantity Flow Diagram is produced. `--focus correctness` is not active, so the State Variable Registry is not required.

## Guard Condition Boundary Table

Guards are taken from SPEC. Input classes not listed for a guard are left out because they cannot occur for it, with the reason stated in the row where relevant.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| WC-5 outcome mapping | `SPEC:63` | Zero/Empty: no report file | no file | failed | `--outcome failed` "or no report exists" | OK |
| WC-5 outcome mapping | `SPEC:63` | Zero/Empty: contract present, `status` missing or empty | `status: ""` | undefined | No mapping for a missing status; WC-4 requires the field but says nothing about its absence | GAP (F12) |
| WC-5 outcome mapping | `SPEC:63` | Typical: `succeeded` | `succeeded` | false | `--outcome succeeded` | OK |
| WC-5 outcome mapping | `SPEC:63`, `SPEC:263` | Partial | `partial` | false | `succeeded`, with the body saying `partial` | OK |
| WC-5 outcome mapping | `SPEC:63`, `SPEC:62` | Sentinel: value outside the four-value set (for example a command's own vocabulary) | `pass` | undefined | Not specified; WC-4 says commands "keep their fields" | GAP (F12) |
| WC-5 outcome mapping | `SPEC:63` | Legitimate edge: audit verdict FAIL with status succeeded | `status: succeeded`, verdict `FAIL` | false | `--outcome succeeded` | OK |
| WC-2 gate / `--unattended` switch | `SPEC:51`, `SPEC:146` | Typical: flag absent | no flag | false | Command unchanged (SA-1) | OK |
| WC-2 gate / `--unattended` switch | `SPEC:128` | Edge: flag passed to a coordinator-only command | `--unattended` on `/sc:git` | undefined | "get no `--unattended` mode"; no rule for the flag itself | GAP (F13) |
| WC-10 wait split | `SPEC:68`, `SPEC:266` | Legitimate edge: one tool call of 4 min 59 s | 4:59 | false (not "longer than 5 minutes") | No split required; the rationale for 4 min is a margin under the 5-min cadence, which this case lacks | GAP (F23) |
| WC-10 / step 2 vs step 3 | `SPEC:181-182` | Maximum: one `check --wait` call | `--timeout-ms 900000` | true (no observation for 15 min) | Step 2 requires `worker-show` at least every 5 minutes; step 3 blocks for 900000 ms | GAP (F1) |
| WC-3 ask path | `SPEC:61`, `SPEC:62`, `SPEC:64` | Sentinel: worker asked, answered, re-invoked | answer supplied as flag | undefined which contract is reported | Re-run may write a fresh directory (WC-6); WC-4 fixes the path before dispatch | GAP (F8) |
| WC-12 `consumer_fenced` | `SPEC:70` | Typical: check returns no fence | none | false | Continue | OK |
| WC-12 `consumer_fenced` | `SPEC:70` | Sentinel: check returns `consumer_fenced` | fence set | true | Stop, send no `worker_done` | OK |

Classes left out: Maximum/Overflow for WC-5 (the outcome has no numeric input); Zero/Empty for WC-12 (the check result is one of two values).

## Expert quality scores (0-10)

| Dimension | Score | Basis |
|---|---|---|
| Clarity | 7 | Terms and citation conventions are defined (`SPEC:7-11`); some rules are stated in two places with different wording (F9, F16). |
| Completeness | 6 | Coordinator stall handling, shared-worktree code edits and an unknown `status` value are not specified (F9, F10, F12). |
| Testability | 5 | Most AC rows are concrete, but AC-C1 cannot fail as written (F3), AC-1.1 cannot pass for load (F2), and step 2 vs 3 contradict (F1). |
| Consistency | 5 | Contract scope, phase lists and the nesting claim disagree in places (F2, F4, F8). |

=== REQUIREMENTS ANALYSIS ===

**F1 (BLOCKING, MAJOR): acceptance step 2 contradicts step 3.** Wiegers (requirements), Adzic (testability).
- Issue: step 2 requires `worker-show` "at least once per 5 minutes" while the worker runs (`SPEC:181`). Step 3 then runs `check --wait ... --timeout-ms 900000` "until `worker_done` arrives" (`SPEC:182`). Following step 3 as written, the coordinator waits 15 minutes with no `worker-show`, which step 2 forbids. No step says to shorten the wait.
- Sentence test: an implementer who follows step 3 as written waits 15 minutes between observations, and that breaks step 2 with no further assumption.
- Recommendation: state the wait as at most 240000 ms per call with a `worker-show` between calls, or make step 2 apply per wait. Priority: High. Quality impact: the live check is not runnable as written.

**F2 (BLOCKING, MAJOR): load and init-lite do not satisfy WC-4 or AC-1.1.** Wiegers.
- Issue: WC-4 requires `<output-dir>/return-contract.yaml` for every unattended command (`SPEC:62`), and AC-1.1 requires every command in sections 3.1-3.2 to have a `## Unattended mode` section naming it (`SPEC:195`). The load row says its report is "none" and its change is "usage line only" (`SPEC:112`; `SPEC:159`). The init-lite row names `.dev/superclaude/context-audit.md` or `--output <file>` as its report, with "Small fix: None" (`SPEC:87`), so it has no contract, and P1 (`SPEC:159`) does not list init-lite or brainstorm. So an implementer who follows the load row and P1 as written adds only a usage line, and AC-1.1 then fails.
- Sentence test: an implementer who follows the load row and P1 as written produces no `## Unattended mode` section for load, so AC-1.1 cannot pass.
- Recommendation: give load and init-lite either a contract or an explicit exemption in WC-4 and AC-1.1, and add init-lite and brainstorm to a phase row. Priority: High. Quality impact: the P1 gate cannot be met as written.

**F3 (BLOCKING, MAJOR): AC-C1 cannot match as written.** Adzic.
- Issue: the pattern is `grep -rnE '\borca(-ide)?[[:space:]]+(orchestration\|worktree\|terminal\|agent)\b'` (`SPEC:172`). In grep -E, `\|` is a literal pipe, not alternation, so the check matches only the text `orchestration|worktree|...`. I ran the raw pattern in the sandbox on the line `x orca orchestration ask`: exit 1 (no match). The same line with `|` as alternation matched (exit 0). So AC-C1 passes on any command that calls `orca orchestration`, which is the violation SA-2 and WC-8 forbid.
- Sentence test: an implementer who runs AC-C1 as written gets no output and records a pass, even when a command contains an Orca call.
- Recommendation: write the alternation as `(orchestration|worktree|terminal|agent)` in the raw file, and add a test that the check fails on a planted call. Priority: High. Quality impact: the only mechanical gate for the central design rule is non-functional.

**F7 (MEDIUM, MAJOR): output directories are not required to be unique per Task.** Wiegers; Whittaker (see attack A1).
- Issue: WC-4 fixes the filename inside whatever directory the coordinator passes (`SPEC:62`). WC-11 says two workers must never write the same file (`SPEC:69`) and speaks only of "default output paths". Nothing requires distinct `<output-dir>` values per Task (section 2.3, `SPEC:73`, lists "the output directory" but no uniqueness rule).
- Sentence test: an implementer who passes the same `--output` to two Tasks produces two writers of one contract, and the spec does not say that is wrong; the outcome depends on a guess about the coordinator.
- Recommendation: require one unique output directory per Task in section 2.3 and in WC-11. Priority: Medium-High.

**F8 (MEDIUM, MAJOR): an answered ask has no defined contract path.** Wiegers; Whittaker (see attack A2).
- Issue: WC-3 lets the worker "re-invoke or resume the command with the answer as a flag" (`SPEC:61`). WC-6 says that a command without a resume flag "writes each run into a fresh output directory" (`SPEC:64`). WC-4 says the contract path is "known before dispatch" (`SPEC:62`, `SPEC:73`). For a fresh-dir command, the answered run writes elsewhere, and the path the coordinator holds still says `blocked`.
- Sentence test: a fresh-dir command re-invoked under WC-3 writes a new directory, and the spec does not say which contract to report. That needs a guess.
- Recommendation: state that a re-invocation after an answered ask reuses the first run's output directory and overwrites its contract, or that the worker reports the new path. Also state a bound on re-invocations, since WC-3 says "once" without a cap on the loop.
- Also: WC-3 adds a route that is not one of the "three ways" WC-2 allows (`SPEC:60`). The spec should say whether it is a fourth resolution or a form of (b).

**F9 (MEDIUM, MAJOR): no coordinator rule for a stalled worker.** Nygard (failure modes).
- Issue: section 1.4 says a stall shows as "a missing report" or `agentWait` (`SPEC:44`). Section 2.3 gives only the success path: "After `worker_done`, the coordinator opens the report file" (`SPEC:73`). Section 7.2 treats non-null `agentWait` as a failed check (`SPEC:181`), but no requirement says what the coordinator does with a parked worker: answer it, stop it, or wait. CAPS:125 says absence never authorizes stop, retry or release, so the spec needs an explicit rule.
- Sentence test: an implementer who follows section 2.3 has no action for a worker parked on a prompt, so the coordinator has to decide.
- Recommendation: add a stall branch to section 2.3 (for example: record `agentWait`, do not retry, escalate to the person) citing CAPS:125 and CAPS:129.

**F11 (MEDIUM, MAJOR): SA-1 says every prompt stays, but WC-1 changes a launch prompt for people.** Cockburn (stakeholder).
- Issue: SA-1 says that without `--unattended`, "every prompt ... stays as it is today" (`SPEC:146`). WC-1 requires any launch-path prompt to "fall back on its own well inside the readiness limit" (`SPEC:59`), which changes a person's launch behavior. WC-1 also names no file: the launch wrapper is "Launch setup, not commands" and its location is not given.
- Sentence test: an implementer who follows SA-1 literally cannot change the launch prompt that WC-1 requires, and an implementer who follows WC-1 changes a person's prompt.
- Recommendation: scope SA-1 to command prompts, and name where the launch setup lives and how a person's launch is preserved.

**F12 (MEDIUM, MAJOR): status vocabulary for existing contracts is not defined.** Wiegers; Whittaker (see attack A4).
- Issue: WC-4 says contracts keep their fields and that `status` is "one of `succeeded`, `partial`, `failed`, `blocked`" (`SPEC:62`). The inventories do not record the status values of the existing contracts (INV-B:272 names the workflow contract's `status` field without its values), so SPEC cannot be checked for whether existing values fit the four. WC-5 maps only the four values and does not say what a missing or other value maps to (`SPEC:63`).
- Sentence test: an implementer whose existing contract uses another status value cannot both keep the field and satisfy "one of" the four, and the spec gives no mapping.
- Recommendation: add a mapping table for each existing contract (or a rule that an unknown or missing value is `failed`), and record the existing vocabularies in the inventory.

**F13 (MEDIUM, MAJOR): `--unattended` passed to a coordinator-only command is unspecified.** Wiegers.
- Issue: section 4 says these six "get no `--unattended` mode" (`SPEC:128`). Nothing says what `/sc:git --unattended` does. It could ignore the flag and run the interactive path, which waits on a person, or refuse.
- Sentence test: an implementer who ignores the flag leaves a path that waits on a person; the spec does not forbid that.
- Recommendation: state that a coordinator-only command given `--unattended` refuses before any work and writes nothing.

**F16 (MINOR): WC-4 states as fact what the spec itself lists as UNVERIFIED.** Wiegers.
- Issue: WC-4 says "Orca does not check the file, so the coordinator opens it" (`SPEC:62`). CAPS:79 marks the question UNVERIFIED, and SPEC's own item 3 says "the spec assumes it does not" (`SPEC:274`).
- Recommendation: state "the coordinator opens the file, because Orca's handling is UNVERIFIED". The requirement stands either way.

**F17 (MINOR): the output flag is named three ways.** Wiegers.
- Issue: WC-4 says `--output` / `--output-dir` (`SPEC:62`); section 3.1 gives init-lite `--output <file>` (`SPEC:87`); section 7 uses `--output <dir>` (`SPEC:196`). A file is not a directory.
- Recommendation: fix one name and one type, and say which commands take a file.

**F18 (MINOR): section 1.1 says the change is "limited to" the contract, but section 3 includes other defect fixes.** Wiegers.
- Issue: section 1.1 says "What changes in the commands is limited to the worker contract in section 2" (`SPEC:16`). Section 3 and SA-4 (`SPEC:149`) add other edits, such as the roadmap drift fix and the business-panel frontmatter.
- Recommendation: change 1.1 to "the worker contract in section 2 plus the named defect fixes in section 3".

**F19 (MINOR): P4 lists pr-submit although D3 (a) recommends no change.** Cockburn.
- Issue: P4 says "pr-submit as a worker" (`SPEC:162`); D3 (a) recommends the coordinator run it and "no pr-submit changes in Phase 4" (`SPEC:240`).
- Recommendation: make pr-submit conditional on D3 in the phase row.

**F20 (MINOR): AC-1.3 tests a headless run and calls it a plain session.** Adzic.
- Issue: AC-1.3 uses `claude -p "/sc:analyze src/superclaude/cli/install_core.py"` (`SPEC:197`) as the "plain session". Print mode is the headless path SA-6 keeps separate (`SPEC:151`), so AC-1.3 does not test a person's interactive session.
- Recommendation: test one interactive run as well as one print run.

**F21 (MINOR): AC-C1 covers four verbs, but SA-2 forbids every `orca` or `orca-ide` command.** Adzic.
- Issue: SA-2 says "No command, skill or agent file runs an `orca` or `orca-ide` command" (`SPEC:147`). AC-C1 matches only `orchestration|worktree|terminal|agent` (`SPEC:172`), so `orca status`, `orca send`, `orca check`, `orca skills get` and `orca open` pass.
- Recommendation: match any `orca` or `orca-ide` followed by a word, and keep the verb list only as a note.

**F22 (MINOR): "a stall is invisible" overstates the evidence.** Wiegers.
- Issue: WC-2's evidence says a waiting worker is healthy, "so a stall is invisible" (`SPEC:60`). Step 2 of section 7.2 uses `agentWait` to see exactly that stall (`SPEC:181`), and CAPS:129 says a waiting worker is "healthy, not failed" but does not say invisible.
- Recommendation: say "a stall does not change the liveness verdict; `agentWait` shows it".

**F23 (MINOR): the WC-10 trigger does not match its rationale.** Adzic.
- Issue: WC-10 splits only calls "longer than 5 minutes" (`SPEC:68`), while section 8's decision row gives 4 minutes "a margin under the 5-minute heartbeat cadence" (`SPEC:266`). A call of 4:59 is not split, so it has no margin.
- Recommendation: split any call longer than 4 minutes, or justify 5 minutes.

=== ARCHITECTURE ANALYSIS ===

**F4 (MEDIUM, MAJOR): the nesting claim for tasklist is misstated and rests on a source that marks it UNVERIFIED.** Fowler (architecture).
- Issue: the tasklist row says "its reflect fan-out runs one layer below the worker, inside Claude Code's nesting limit, `INV-A:14`" (`SPEC:122`). Stage 10.5 runs reflect in subagents (INV-B:210), and each reflect spawns its own agents (INV-B:111), so the reflect agents are two layers below the worker, not one. INV-A:14 says three layers are allowed and that at the limit Claude Code "withholds the `Agent` tool". INV-B:210 and INV-B:314 mark nested spawning as UNVERIFIED.
- Sentence test: the conclusion "inside the limit" needs the assumption that Tier 2 reflect stays within three layers, which no source confirms.
- Recommendation: state the depth of each reflect fan-out, and make tasklist a worker only after AC-level evidence that the Agent tool is present at that depth.

**F5 (MINOR): E4 says subagents "are not counted" by Orca's limit, which CAPS:155 leaves UNVERIFIED.** Fowler.
- Issue: E4 (`SPEC:24`) reads as settled; CAPS:155 says no Orca limit on subagents was found and whether one applies is UNVERIFIED. The depth fence in CAPS:97 covers Orca dispatch only, which supports "not counted" for dispatch but not for subagents.
- Recommendation: say "not counted by the Orca depth fence, which covers Orca dispatch only".

**F6 (MEDIUM, MAJOR): the claim that heavy fan-out can be split into Tasks is not achievable for several commands.** Hohpe (integration), Fowler.
- Issue: WC-8 says "Fan-out that needs Orca records is split into separate Tasks by the coordinator" (`SPEC:66`), and section 1.3 says the coordinator "gets them by splitting the work into separate worker Tasks" (`SPEC:39`). The heavy fan-outs are inside one command: cleanup-audit runs waves of 7-8 agents over batches of files (INV-A:42), and tdd runs 2-10+ agents (INV-B:47). The coordinator cannot split those, and no command exposes a unit that could be split.
- Sentence test: an implementer who applies WC-8 to cleanup-audit has no split available, so the rule cannot be followed as written.
- Recommendation: say which commands are exempt from per-unit records and accept the lost liveness for them, or add a per-unit flag to each command.

**F9 (see Requirements).**

**F10 (MEDIUM, MAJOR): concurrent code-editing workers in one worktree are not covered.** Newman (shared state).
- Issue: section 2.3 says the brief states "the worktree placement (`CAPS:115`)" (`SPEC:73`), and CAPS:115 says workers share the current worktree by default. The inventories record that cleanup, improve, test with `--fix` and implement edit product code (INV-A:43, INV-A:52, INV-B:48, INV-A:51). WC-11 covers only "the same file" (`SPEC:69`). Two workers in one worktree can edit different files and still break each other's builds or tests.
- Sentence test: an implementer who runs cleanup and improve in one worktree, each writing different files, meets no rule, and the outcome depends on a guess.
- Recommendation: require a separate worktree for any command that edits product code, or state a serialization rule for code writers.

**F14 (MEDIUM, MAJOR): reflect's auto-accept under `--unattended` lets a command approve its own remediation.** Fowler (boundary).
- Issue: P2 says "under `--unattended`, make `--remediate` follow the existing headless auto-accept rule" (`SPEC:88`). D2 says a Ruling must not come from another agent because "the rule exists to stop an agent approving its own work" (`SPEC:236`). The reflect auto-accept is the same kind of self-approval, and WC-9 does not list it as an outward action (`SPEC:67`).
- Sentence test: the remediation hands off to a tasklist package (`sc:workflow` or task-builder, INV-B:109), not directly to code, so the risk is bounded. Whether that is acceptable needs a decision, so this is Medium.
- Recommendation: decide whether an unattended run may auto-accept remediation, and state it in WC-9 or in D2.

=== ADVERSARIAL ANALYSIS (Whittaker) ===

- **A1 (Sequence/Accumulation, on F7; MAJOR).** I can break this specification by **Sequence Attack**. The invariant at **WC-4 and WC-11 (`SPEC:62`, `SPEC:69`)** fails when **two Tasks are given the same `--output` directory**. Concrete attack: Task T1 finishes with `status: succeeded` and writes `<D>/return-contract.yaml`. Task T2 starts later with the same `<D>`, fails with `status: blocked`, and overwrites the file. The coordinator reads `<D>` for T1 and sees `blocked`, so T1 is recorded as failed.
- **A2 (Sequence, on F8; MAJOR).** I can break this specification by **Sequence Attack**. The invariant at **WC-3 and WC-6 (`SPEC:61`, `SPEC:64`)** fails when **a fresh-dir command is re-invoked after an answered ask**. Concrete attack: run 1 writes `status: blocked` to `D` and asks. The coordinator answers. Run 2, re-invoked with the answer, writes `status: succeeded` to `D2`. `worker_done --report-path` points at `D`, as WC-4 requires, so the coordinator is told the work is blocked.
- **A3 (Sentinel Collision, on F15; MINOR).** I can break this specification by **Sentinel Collision**. The invariant at **D1 (`SPEC:228`)** fails when **a person pastes a worker brief into their own session**. Concrete attack: the brief contains `--unattended`, so the person's session loses its prompts (SA-1 is violated) and any `--post-pr` in the same brief posts to GitHub from a person's session.
- **A4 (Zero/Empty, on F12; MAJOR).** I can break this specification by **Zero Attack**. The invariant at **WC-5 (`SPEC:63`)** fails when **the contract exists but `status` is absent**. Concrete attack: a command keeps its own contract with no `status` key. WC-5 has no row for this case, so the coordinator must choose between `succeeded` and `failed`. The acceptance check in step 4 (`SPEC:183`) would raise a KeyError, which catches it only at acceptance time.

Severity follows the panel scale. All four are Medium or Minor under the grading rule, and none adds a blocking finding on its own.

## Follow-up candidates (Medium and minor; not blocking)

F4, F5, F6, F7, F8, F9, F10, F11, F12, F13, F14 (Medium), and F15-F23 (minor). Per the loop rules these are listed for the user to decide whether to open an issue. Nothing has been filed.

## Findings block

```findings-v1
{"id": "F1", "severity": "MAJOR", "blocking": true, "category": "contradiction", "anchor": "ORCA orchestration check --wait --types \"worker_done,escalation,question\" --timeout-ms 900000 --json", "anchor2": "at least once per 5 minutes", "refs": ["section 7.2 step 2", "section 7.2 step 3"], "claim": "Following step 3 with its 900000 ms timeout leaves 15 minutes between worker-show observations, which step 2 forbids."}
{"id": "F2", "severity": "MAJOR", "blocking": true, "category": "unpassable-check", "anchor": "none (see note) | n/a | none: use it as a step inside another worker's brief", "anchor2": "every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml`", "refs": ["WC-4", "AC-1.1", "P1", "section 3.1 init-lite row"], "claim": "The load row and P1 give no contract and only a usage line, so AC-1.1 cannot pass for load."}
{"id": "F3", "severity": "MAJOR", "blocking": true, "category": "unpassable-check", "anchor": "grep -rnE '\\borca(-ide)?[[:space:]]+(orchestration\\|worktree\\|terminal\\|agent)\\b'", "refs": ["AC-C1", "SA-2", "WC-8"], "claim": "As written, the escaped pipe is a literal, so AC-C1 never matches, even on a command that calls orca orchestration; the check passes a violation."}
{"id": "F4", "severity": "MAJOR", "blocking": false, "category": "other", "anchor": "its reflect fan-out runs one layer below the worker, inside Claude Code's nesting limit", "refs": ["INV-A:14", "INV-B:210", "INV-B:314", "section 3.2 tasklist row"], "claim": "Reflect agents under Stage 10.5 are two layers below the worker, and the cited source only says three layers are allowed; nested spawning is UNVERIFIED."}
{"id": "F5", "severity": "MINOR", "blocking": false, "category": "other", "anchor": "Agent-tool subagents inside a worker are not Orca workers and are not counted by Orca's nesting limit", "refs": ["E4", "CAPS:155", "CAPS:97"], "claim": "The depth fence covers Orca dispatch; CAPS:155 leaves whether Orca limits subagents UNVERIFIED, so E4 states more than its source."}
{"id": "F6", "severity": "MAJOR", "blocking": false, "category": "missing-requirement", "anchor": "Fan-out that needs Orca records is split into separate Tasks by the coordinator.", "refs": ["WC-8", "section 1.3", "INV-A:42", "INV-B:47"], "claim": "Heavy in-command fan-out such as cleanup-audit and tdd cannot be split by the coordinator, and no rule covers that case."}
{"id": "F7", "severity": "MAJOR", "blocking": false, "category": "missing-requirement", "anchor": "where `<output-dir>` is the directory the coordinator passed", "anchor2": "Two workers in one worktree must never write the same file.", "refs": ["WC-4", "WC-11", "section 2.3"], "claim": "Nothing requires a unique output directory per Task, so two Tasks given one directory overwrite each other's contract."}
{"id": "F8", "severity": "MAJOR", "blocking": false, "category": "missing-requirement", "anchor": "then re-invoke or resume the command with the answer as a flag", "anchor2": "writes each run into a fresh output directory so a re-run starts clean", "refs": ["WC-2", "WC-3", "WC-4", "WC-6"], "claim": "After an answered ask, a fresh-dir re-run writes another directory, and the spec does not say which contract the worker reports."}
{"id": "F9", "severity": "MAJOR", "blocking": false, "category": "missing-requirement", "anchor": "After `worker_done`, the coordinator opens the report file", "anchor2": "the coordinator sees only through `worker-show`'s `agentWait` or a missing report", "refs": ["section 1.4", "section 2.3", "CAPS:125"], "claim": "No coordinator action is specified for a worker parked on a prompt or one that stops without a report."}
{"id": "F10", "severity": "MAJOR", "blocking": false, "category": "missing-requirement", "anchor": "the worktree placement (`CAPS:115`)", "anchor2": "Two workers in one worktree must never write the same file.", "refs": ["section 2.3", "WC-11", "INV-A:43", "INV-A:52"], "claim": "Two code-editing workers in one worktree can break each other's builds without writing the same file, and no rule covers it."}
{"id": "F11", "severity": "MAJOR", "blocking": false, "category": "contradiction", "anchor": "Without `--unattended`, every prompt, approval gate, default flag value, output path and outward default stays as it is today", "anchor2": "Any such prompt must fall back on its own well inside the readiness limit", "refs": ["SA-1", "WC-1"], "claim": "SA-1 freezes every prompt without --unattended, but WC-1 changes the launch prompt, and the spec does not say where that prompt lives."}
{"id": "F12", "severity": "MAJOR", "blocking": false, "category": "missing-requirement", "anchor": "Commands that already write a contract keep their fields and add the missing ones.", "anchor2": "`status` (one of `succeeded`, `partial`, `failed`, `blocked`)", "refs": ["WC-4", "WC-5"], "claim": "Existing contract status values are not mapped to the four-value set, and a missing or other status has no outcome."}
{"id": "F13", "severity": "MAJOR", "blocking": false, "category": "missing-requirement", "anchor": "These six are never dispatched as workers and get no `--unattended` mode.", "refs": ["section 4", "WC-2"], "claim": "The spec does not say what a coordinator-only command does when given --unattended, so it may wait on a person."}
{"id": "F14", "severity": "MAJOR", "blocking": false, "category": "safety", "anchor": "make `--remediate` follow the existing headless auto-accept rule", "anchor2": "the rule exists to stop an agent approving its own work", "refs": ["section 3.1 reflect row", "D2", "WC-9"], "claim": "Unattended reflect auto-accepts remediation, which is the self-approval that D2 forbids for implement; the bounded risk needs a decision."}
{"id": "F15", "severity": "MINOR", "blocking": false, "category": "other", "anchor": "cannot misfire on a person", "refs": ["D1", "SA-1"], "claim": "A brief that a person pastes with --unattended silences that person's prompts, so the flag is not a safe sentinel."}
{"id": "F16", "severity": "MINOR", "blocking": false, "category": "other", "anchor": "Orca does not check the file, so the coordinator opens it.", "refs": ["WC-4", "CAPS:79", "SPEC item 3"], "claim": "WC-4 states as fact what the spec's own UNVERIFIED item 3 lists as unknown."}
{"id": "F17", "severity": "MINOR", "blocking": false, "category": "other", "anchor": "(`--output` / `--output-dir`)", "anchor2": "`--output <file>`", "refs": ["WC-4", "section 3.1 init-lite row", "section 7.2"], "claim": "The output flag is named three ways and is sometimes a file, sometimes a directory."}
{"id": "F18", "severity": "MINOR", "blocking": false, "category": "other", "anchor": "What changes in the commands is limited to the worker contract in section 2", "refs": ["section 1.1", "SA-4", "section 3"], "claim": "Section 1.1 says changes are limited to the contract, but section 3 and SA-4 include other defect fixes."}
{"id": "F19", "severity": "MINOR", "blocking": false, "category": "other", "anchor": "Apply the answers to D2-D4: the implement halt path, post-release pre-authorization, pr-submit as a worker.", "refs": ["section 6 P4", "D3"], "claim": "P4 includes pr-submit although D3 (a) recommends no pr-submit change."}
{"id": "F20", "severity": "MINOR", "blocking": false, "category": "other", "anchor": "claude -p \"/sc:analyze src/superclaude/cli/install_core.py\"", "refs": ["AC-1.3", "SA-6"], "claim": "AC-1.3 calls a print-mode run a plain session, so it does not test an interactive person's session."}
{"id": "F21", "severity": "MINOR", "blocking": false, "category": "unpassable-check", "anchor": "No command, skill or agent file runs an `orca` or `orca-ide` command", "refs": ["SA-2", "AC-C1"], "claim": "AC-C1 matches four verbs only, so most orca commands pass the SA-2 check."}
{"id": "F22", "severity": "MINOR", "blocking": false, "category": "other", "anchor": "so a stall is invisible", "refs": ["WC-2", "CAPS:129", "step 2"], "claim": "A stall is visible through agentWait, so calling it invisible overstates the evidence."}
{"id": "F23", "severity": "MINOR", "blocking": false, "category": "other", "anchor": "must be split into waits of at most 4 minutes", "refs": ["WC-10", "section 8 decision row"], "claim": "A 4:59 call is not split, which contradicts the 4-minute margin rationale."}
```

Summary of blocking findings: F1, F2, F3.

Reviser brief: revise only the text named by the blocking findings F1, F2 and F3. F1 concerns `SPEC:181-182` (step 2 vs step 3). F2 concerns `SPEC:112`, `SPEC:159` and `SPEC:195` (load and init-lite against WC-4 and AC-1.1). F3 concerns `SPEC:172` (AC-C1 pattern escaping). Add no rule, mechanism or section that a finding does not call for. Prefer deleting or narrowing to adding. Cite the finding id on every addition. Report the byte size before and after, and the bytes added and deleted per finding id. Leave the Medium and minor findings alone, and do not award a PASS. This brief does not widen the review's scope and does not grade any minor finding as blocking.

verdict: FAIL
