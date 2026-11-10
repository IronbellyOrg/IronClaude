review: 1 of 3

# Spec panel review, round 1: Orca worker contract spec

| Header field | Value |
|---|---|
| Command | `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture` |
| Candidate | `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (285 lines, 57763 bytes) |
| Candidate SHA-256 | `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d` |
| Baseline / prior report | none given; this is a first review of the full document (`--re-review` and `--baseline` absent, so no `baseline: missing` note) |
| Reviewer model actually used | Sonnet 5.5 (`claude-sonnet-5-5`) |
| Prompt followed | FIRST-REVIEW prompt, `~/.claude/rules/prompts/document_review_loop_prompts.md:27-32` (home resolves to the sandbox `home/`) |
| Panel | Wiegers (lead), Adzic, Cockburn (requirements); Fowler (lead), Nygard, Newman, Hohpe (architecture); Whittaker (adversarial, active in every review). Crispin, Gregory and Hightower are not in the two requested focus areas and were not engaged. |

Abbreviations: `SPEC:N` = line N of the candidate. `INV-A:N`, `INV-B:N`, `CAPS:N` = line N of `.dev/orca-command-refactor/inventory/commands-a.md`, `commands-b.md`, `orca-capabilities.md`. `README:N` = `.dev/orca-command-refactor/README.md`.

## What I covered

- Read in full: the candidate, `README.md`, the three inventory files, and the review-loop prompts file.
- Checked every `INV-A:`, `INV-B:` and `CAPS:` line citation in SPEC sections 1 to 4 and the Decisions table against the inventory files. Each pointed at the content the spec describes. The per-command rows (`SPEC:83-92`, `SPEC:99-125`, `SPEC:132-137`) match the inventory verdicts. The totals also match: 43 commands = 10 ready + 27 needing change + 6 coordinator-only (`SPEC:76`; `INV-A:73`; `INV-B:278`).
- Checked the spec's internal consistency: requirements WC-1 to WC-12 against the per-command rows, the phase table (`SPEC:156-162`), the acceptance checks (`SPEC:167-210`), the standalone requirements SA-1 to SA-6 (`SPEC:146-151`) and the open decisions D1 to D5 (`SPEC:227-253`).
- UNVERIFIED in this sandbox, because the files are not in the workspace: every `cmd/`, `sk/` and `ag/` citation not quoted by an inventory, `CLAUDE.md:*`, `src/superclaude/cli/install_core.py:*`, `pyproject.toml:38`, `src/superclaude/core/HOW-WE-WORK.md:*`, `Makefile:*`, `.dev/codegraph-migration/*`, `.dev/evals/ccsession-orca-e2e-20261026/EVIDENCE.md:*` (only the lines `CAPS:49` quotes are confirmed), and the spec's own grep claims at `SPEC:25`. I did not re-run those greps. The spec's statement that 11 locations were re-read (`SPEC:11`) and that 340 citations were validated (`SPEC:285`) is likewise unchecked here.
- Not covered: testing-strategy and cloud-native depth (outside the requested focus), and whether any claim about Orca internals is right (only `CAPS` is checkable).

## Guard Condition Boundary Table

Trigger: the spec contains thresholds and conditional gates (readiness limit, ask timeout, wait size, confidence threshold, depth fence, outcome mapping, the `--unattended` switch, the output-directory precondition). Constructed before synthesis. Responsibility: Nygard builds, Crispin's completeness check is folded in, Whittaker attacks the entries. Status `GAP` rows are graded in the findings (FR-8) and each blank or implicit "Specified Behavior" is graded in the same way (FR-9).

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| `unattended_switch` | SPEC:51, SPEC:228 | Zero/Empty | flag absent | false | Standalone behaviour unchanged (SPEC:146) | OK |
| `unattended_switch` | SPEC:51, SPEC:228 | One/Minimal | `--unattended` as its own token | true | Unattended mode on (SPEC:51) | OK |
| `unattended_switch` | SPEC:51, SPEC:228 | Sentinel Value Match | topic text that contains the string `--unattended`, for example `/sc:tdd "add --unattended to the CLI"` | unspecified | Token versus substring rule never stated; D1 claims it "cannot misfire on a person" (SPEC:228) | GAP (M-04) |
| `unattended_switch` | SPEC:60, SPEC:83-84, SPEC:89 | Legitimate Edge Case | `--unattended` together with `--interactive` | unspecified for adversarial, brainstorm, release-split; true (refused) for cleanup, improve, test (SPEC:103, SPEC:110, SPEC:123) | "never `--interactive`" is a brief instruction only (SPEC:83-84, SPEC:89), not a refusal rule | GAP (M-05) |
| `output_dir_precondition` | SPEC:62 (WC-4) | Zero/Empty | `--unattended` with no output directory | unspecified | WC-4 defines `<output-dir>` only as "the directory the coordinator passed"; post-release says "else blocked" (SPEC:113) but the blocked contract has no place to be written | GAP (M-01) |
| `output_dir_precondition` | SPEC:62 (WC-4) | Legitimate Edge Case | `--output <file>` (tdd SPEC:90, init-lite SPEC:87, AC-2.2 SPEC:200) | unspecified | A file is not a directory; contract location is not stated | GAP (M-01) |
| `output_dir_precondition` | SPEC:62 (WC-4) | Maximum/Overflow | output directory not creatable or not writable | unspecified | WC-4 says written "on every outcome" (SPEC:62) but gives no fallback | GAP (M-01) |
| `output_dir_precondition` | SPEC:62 (WC-4) | Typical | coordinator passes a writable directory | true | `<output-dir>/return-contract.yaml` (SPEC:62) | OK |
| `outcome_mapping` | SPEC:63 (WC-5) | Zero/Empty | no report file | n/a | `--outcome failed` (SPEC:63) | OK |
| `outcome_mapping` | SPEC:63 (WC-5) | Zero/Empty | report file present but empty or unparseable | unspecified | "`--outcome succeeded` otherwise" (SPEC:63) maps it to success | GAP (M-02) |
| `outcome_mapping` | SPEC:63 (WC-5) | Typical | `succeeded` | true | `succeeded` (SPEC:63) | OK |
| `outcome_mapping` | SPEC:63, SPEC:263 | Legitimate Edge Case | `partial`; audit with verdict FAIL | true | `succeeded`, first sentence of the body says `partial` (SPEC:63, SPEC:263) | OK |
| `outcome_mapping` | SPEC:63 (WC-5) | Sentinel Value Match | `blocked` | true | `failed` (SPEC:63; AC-2.2 SPEC:200) | OK |
| `outcome_mapping` | SPEC:62, SPEC:262 | Legitimate Edge Case | existing contract whose `status` uses another vocabulary ("keep their fields", SPEC:62) | unspecified | Four-value set required by SPEC:262 conflicts with "keep their fields" | GAP (M-02) |
| `wait_split` | SPEC:68 (WC-10) | Typical | blocking call of 2 minutes | false | no split needed (SPEC:68) | OK |
| `wait_split` | SPEC:68, SPEC:210 | Legitimate Edge Case | blocking call of 4.5 minutes | false under WC-10 (not longer than 5); true under AC-4.3 (exceeds 240 s) | Requirement and acceptance check use different thresholds | GAP (M-07) |
| `wait_split` | SPEC:68, SPEC:104 | Maximum/Overflow | eval of 3600 s | true | split into waits of at most 4 minutes (SPEC:68, SPEC:104) | OK |
| `wait_split` | SPEC:65, SPEC:68 | Maximum/Overflow | one Agent-tool fan-out call longer than 5 minutes (tdd, cleanup-audit, post-release, tasklist) | unspecified | WC-10 names only polls and evals; a blocking subagent call cannot be split | GAP (M-07) |
| `confidence_threshold` | SPEC:121; INV-B:199 | Zero/Empty | confidence 0.00 | true | blocked (SPEC:121) | OK |
| `confidence_threshold` | SPEC:121; INV-B:199 | Legitimate Edge Case | confidence exactly 0.70 | false | not blocked ("below 0.70", SPEC:121) | OK |
| `confidence_threshold` | SPEC:121 | Typical | confidence 0.85 | false | proceeds (SPEC:121) | OK |
| `nested_depth` | SPEC:33, SPEC:66; CAPS:97 | Zero/Empty | coordinator at depth 0 | n/a | may start workers (CAPS:97) | OK |
| `nested_depth` | SPEC:33, SPEC:66 | One/Minimal | worker at depth 1 calls `worker-start` | true | refused; WC-8 forbids the call (SPEC:66) | OK |
| `nested_depth` | SPEC:249-253 | Maximum/Overflow | setting raised to 2 or more (D5 option b) | n/a | WC-8 still forbids the call (SPEC:66); D5 keeps depth 1 | OK |
| `ask_wait` | SPEC:61 (WC-3) | One/Minimal | answer arrives before timeout | false | worker continues (SPEC:61) | OK |
| `ask_wait` | SPEC:61 (WC-3) | Maximum/Overflow | `ask` times out | true | resume same message ID, no duplicate (SPEC:61; CAPS:60) | OK |
| `ask_wait` | SPEC:61 (WC-3) | Legitimate Edge Case | coordinator never answers | n/a | Orca treats a waiting worker as healthy (CAPS:129); the coordinator owns the `question` wait (CAPS:63); no spec change needed | OK |
| `readiness_limit` | SPEC:59 (WC-1) | Typical | launch prompt falls back in 30 s | false | passes (CAPS:49) | OK |
| `readiness_limit` | SPEC:59 (WC-1) | Maximum/Overflow | launch prompt waits longer than the limit | true | "well inside the readiness limit" (SPEC:59) is not a number | GAP (M-09) |

Classes left out, one line each: `unattended_switch` Maximum/Overflow, because a flag has no capacity; `output_dir_precondition` Sentinel Value Match, because no sentinel directory name is defined; `wait_split` Zero/Empty, because a wait of zero seconds needs no split; `nested_depth` Sentinel Value Match, because the depth is a plain integer (a malformed setting falls back to 1, `CAPS:100`); `ask_wait` Zero/Empty and Sentinel Value Match, because an empty question is the worker's own text, not a spec input; `confidence_threshold` Maximum/Overflow, because a confidence above 1.0 cannot occur; `readiness_limit` Zero/Empty, because "no prompt" is the passing case in WC-1; `outcome_mapping` Maximum/Overflow, because the status set is fixed at four values.

Table status: complete, so synthesis may proceed (FR-10).

## Quantity Flow Diagram (Pipeline Dimensional Analysis, FR-17 to FR-21)

Trigger: the spec sorts commands into groups and then assigns them to phases; the count after the second stage is smaller than the count after the first (Fowler identifies, Whittaker attacks).

```text
[Source: 43 commands (SPEC:76; INV-A:3 + INV-B:3)]
  --> [Stage 1: sort by verdict]
        coordinator-only 6 (SPEC:128-137), worker-capable 37 = ready 10 (SPEC:81-92) + needs change 27 (SPEC:97-125)
  --> [Stage 2: assign to phases (SPEC:156-162)]
        P0 0 (reuses 3 ready commands for smoke runs), P1 13 (9 listed + 4 fixed, SPEC:159),
        P2 15 (SPEC:160), P3 4 (SPEC:161), P4 3 (SPEC:162)  => 35 assigned
        unassigned: brainstorm (SPEC:84), init-lite (SPEC:87)  <-- MISMATCH 37 vs 35
  --> [Consumer A: AC-1.1 (SPEC:195) expects a `## Unattended mode` section in all 37]
  --> [Consumer B: P1 scope sentence (SPEC:159) expects the flag in all 37]
  --> [Consumer C: phase table expects 35]
```

Severity: a dimensional mismatch is CRITICAL under FR-19. It is graded below by consequence (finding F-01).

## === REQUIREMENTS ANALYSIS ===

### F-01 (CRITICAL, blocking) AC-1.1 cannot pass as written

- Expert: Wiegers (traceability), with Fowler (count flow) and Whittaker (divergence attack).
- Where: `SPEC:195` (AC-1.1) against `SPEC:112`, `SPEC:265`, `SPEC:159`, `SPEC:84`, `SPEC:87`, `SPEC:240`, `SPEC:154`.
- Grading sentence: an implementer who follows the stated text as written builds a P1 whose own acceptance test fails, and the test is wrong to fail only because the spec contradicts itself.
- The contradiction, with no further assumption:
  1. AC-1.1 passes only if "every command in sections 3.1-3.2 has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`" (`SPEC:195`). That is 37 commands.
  2. `/sc:load` is one of the 37 (`SPEC:112`). Its Report cell says "none (see note)", the note says to use it "as a step inside another worker's brief, not as its own Task", and the Decisions table rejects a report file for it: "a report file would be an unrequested addition" (`SPEC:265`). A `load` section that names `return-contract.yaml` contradicts both.
  3. The phase table does not give two of the 37 to any phase: brainstorm (`SPEC:84`, fix "None") and init-lite (`SPEC:87`, fix "None") appear in no phase command list (`SPEC:158-162`). P1 does say the flag is "accepted by every command in sections 3.1 and 3.2" (`SPEC:159`), but P2 to P4 commands are the ones whose sections carry their gate resolutions (`SPEC:99-125`, phase column), and `SPEC:154` forbids starting a later phase until the earlier phase's checks pass.
  4. `/sc:pr-submit` is in the 37 (`SPEC:114`). The recommended decision D3(a) says "no pr-submit changes in Phase 4" and that the command is a worker candidate only if D3 is accepted otherwise (`SPEC:139-140`, `SPEC:240`). AC-1.1 still demands its section at P1.
- Concrete attack (Whittaker, divergence): P1 is done exactly as `SPEC:159` lists it (13 commands edited). `uv run pytest tests/skills/test_worker_contract.py` runs AC-1.1 and iterates over the 37. State trace before: 13 commands carry the section. After: the test finds 24 commands without it, among them `load`, for which the spec forbids a contract file. P1 cannot pass, so P2 to P4 never start (`SPEC:154`).
- Recommendation: narrow AC-1.1 to the commands each phase actually edits (the P1 list in `SPEC:159`), and say in the `load` row that it is exempt from the contract-section assertion. Do not add new commands to P1. Delete rather than add text where possible. Name a phase for brainstorm and init-lite or exempt them in the same sentence.
- Priority: High. Quality impact: restores the ability to pass P1 (Testability 4 to 7).

### M-01 (Medium) The contract location is undefined when `--output` is a file, absent, or unwritable

- Expert: Wiegers, Adzic.
- Where: `SPEC:62` (WC-4) against `SPEC:87` (init-lite `--output <file>`), `SPEC:90` (tdd `--output <file>`), `SPEC:85-86` (cleanup-audit and index-repo have a fixed or no output location), `SPEC:92` and `INV-B:272` (workflow writes into a package directory whose `<id>` is generated at run time and writes no contract for pre-creation stops), `SPEC:113` (post-release "else blocked").
- Why Medium: WC-4 says `<output-dir>` is "the directory the coordinator passed (`--output` / `--output-dir`)" and that the path is "known before dispatch" (`SPEC:62`, `SPEC:73`). For file-valued flags there are two readings (the file's parent directory, or a new directory flag); the text does not say which, so the harm needs a guess. AC-2.2 (`SPEC:200`) runs tdd with `--output <file>` and then checks "contract `status: blocked`", so the check cannot locate the contract. For a blocked run with no output directory (post-release, `SPEC:113`) the question has nowhere to be written, so it is lost; WC-5 then reports `failed` with no question (`SPEC:63`).
- Recommendation: add one sentence to WC-4 giving a rule for each case (file-valued flag, no flag, unwritable directory), and say where the question goes when no directory is writable (the worker's `ask`, `SPEC:61`).
- Priority: Medium.

### M-02 (Medium) WC-5 maps an unparseable or out-of-set status to success

- Expert: Whittaker (zero/empty attack), Nygard.
- Where: `SPEC:63` ("`--outcome succeeded` otherwise") with `SPEC:62` ("keep their fields") and `SPEC:262` (fixed four-value set).
- Why Medium: only an empty, truncated or out-of-vocabulary status reaches the "otherwise" branch, and WC-4 says the file is written on every outcome, so the harm needs a crash or a legacy vocabulary. The inventories do not list the value sets of the existing `status` fields (`INV-B:272`, `INV-A:97`), so whether "keep their fields" and the four-value set collide is UNVERIFIED.
- Recommendation: state that an unreadable file or a status outside the four values is treated like "no report", that is `--outcome failed`.
- Priority: Medium.

### M-03 (Medium) WC-6 and stale contracts on retry

- Expert: Nygard, Wiegers.
- Where: `SPEC:64` (WC-6: a command "writes each run into a fresh output directory") against `SPEC:62` (the path is known before dispatch), `SPEC:63` ("no report exists" is the only failure signal), `CAPS:116` (retry workers).
- Why Medium: it is not stated who creates the fresh directory. If the command does, the contract is not at the path the coordinator was given; if the brief does, WC-6 is not a command requirement. A retry that reuses the first attempt's directory and dies early leaves the first attempt's `status: succeeded` file in place, and WC-5 then reads it. The text allows both readings.
- Recommendation: say that the coordinator supplies a fresh directory per attempt, or that the command deletes or overwrites a stale contract before doing any other work.
- Priority: Medium.

### M-04 (Medium) How the switch is recognised is not stated

- Expert: Whittaker (sentinel collision), Cockburn.
- Where: `SPEC:51`, `SPEC:228`.
- Why Medium: D1(a) says a flag "cannot misfire on a person". Commands that take free text (tdd, troubleshoot, workflow, research, task) can receive the string `--unattended` inside the topic, and the spec has no rule that only a standalone argument token counts. This is a requirement the document never states.
- Recommendation: one sentence in section 2.1 or the contract file: the mode is on only when `--unattended` is a standalone argument token outside any quoted text.
- Priority: Medium.

### M-05 (Medium) `--unattended` with `--interactive` is refused only for some commands

- Expert: Wiegers, Whittaker (divergence).
- Where: `SPEC:60` (WC-2: "never calls `AskUserQuestion`") against `SPEC:83-84`, `SPEC:89` (brief-level "never `--interactive`" for adversarial, brainstorm, release-split; `INV-A:35`, `INV-A:39`, `INV-B:37`) and the refusals at `SPEC:103`, `SPEC:110`, `SPEC:123`.
- Why Medium: a brief that passes both flags to adversarial would reach four `AskUserQuestion` checkpoints (`INV-A:35`). That needs the coordinator to violate its own brief template (`SPEC:73`), so it is a missing restriction, not a stated text that does harm.
- Recommendation: one rule in the contract file: under `--unattended`, `--interactive` is refused for every command that has it.
- Priority: Medium.

### M-06 (Medium) The WC-9 authorisations name flags that do not exist

- Expert: Wiegers, Nygard.
- Where: `SPEC:67` (WC-9: "the command's own explicit flag"), `SPEC:100` (auggie-review `--post-pr`), `SPEC:113` (post-release), `SPEC:121` (task commit and push), `SPEC:244-247` (D4).
- Why Medium: `INV-A:38` and `INV-B:85` show only the opt-out forms (`--no-post-pr`, `--no-remediation-offer`) or confirmations; no positive authorising flag is inventoried, and the spec never says these flags are new. A command cannot check that the brief quoted the user's instruction (D4(a), `SPEC:245`). The spec lists the flags as if they exist.
- Recommendation: list the new authorising flags once, in the contract file, and mark them as additions to the commands.
- Priority: Medium.

### M-09 (Medium) WC-1 "well inside the limit" has no number

- Expert: Wiegers (SMART criteria).
- Where: `SPEC:59`.
- Why Medium: the evidence shows a 30 s fallback passes and a longer wait fails against a 45 s limit used in that test (`CAPS:49`); the spec text gives no figure, and the only check is a pass or fail of the launch (`SPEC:180`).
- Recommendation: state a figure (for example half the limit in force) or cite the 30 s that worked.
- Priority: Low.

## === ARCHITECTURE ANALYSIS ===

### M-07 (Medium) WC-10 cannot be applied to blocking subagent calls, and its thresholds disagree

- Expert: Nygard (failure modes), Whittaker (accumulation), Fowler.
- Where: `SPEC:68` (WC-10), `SPEC:114` (pr-submit row: "under 4 minutes"), `SPEC:210` (AC-4.3: "no single tool call exceeds 240 s"), `CAPS:130`, `CAPS:182`.
- Why Medium: three separate issues, none needing a wrong guess. (1) WC-10 requires a split of any call longer than five minutes, but a fan-out call (tdd, cleanup-audit, post-release, tasklist, `SPEC:99-125` with `INV-A:42`, `INV-B:221`) blocks the top-level session until its subagents return, and there is no way to split it; the spec offers no rule for those. (2) The requirement's threshold (more than 5 minutes) and the pr-submit and AC-4.3 threshold (4 minutes or 240 s) differ, so a 4.5 minute call meets WC-10 and fails AC-4.3. (3) The benefit is unproven: whether heartbeat age affects Orca's liveness verdict is UNVERIFIED (`CAPS:182`), and AC-4.3 would also fail on pr-submit's chained troubleshoot fan-out (`INV-B:91`).
- Recommendation: state that WC-10 covers waits the command controls (polls, sleeps, evals) and not subagent calls, and use one threshold in WC-10 and AC-4.3.
- Priority: Medium.

### M-08 (Medium) tasklist drops a change its source required, on evidence the other inventory marks UNVERIFIED

- Expert: Fowler (count and nesting), Newman.
- Where: `SPEC:122` (tasklist: "none ... inside Claude Code's nesting limit, `INV-A:14`") against `INV-B:215` ("the per-phase reflect fan-out must run at the worker's top level, not inside subagents"), `INV-B:210` and `INV-B:314` (nested spawning UNVERIFIED), `INV-B:209` (`needs_human_decision` items HALT), and `SPEC:268` ("nothing read ... contradicts a verdict").
- Why Medium: the spec takes the claim in `INV-A:14` (docs allow three layers) over `INV-B:314` without recording the choice or listing it in its UNVERIFIED section (`SPEC:271-285`). Whether the spec's tasklist row is wrong depends on which reading is true, which is a guess. The row also resolves the remediation offer through the headless rule but leaves the `needs_human_decision` HALT (`INV-B:209`) without a gate resolution, although WC-2 requires one (`SPEC:60`).
- Recommendation: add the nesting question to the UNVERIFIED list, record the choice in Decisions, and give the HALT one of the three WC-2 resolutions.
- Priority: Medium.

### M-10 (Medium) The common check AC-C1 can fail the phase that adds the Orca routing text

- Expert: Fowler, Wiegers.
- Where: `SPEC:172` (AC-C1 scans `src/superclaude/core` and requires no match), `SPEC:158` (P0 adds an Orca section to `HOW-WE-WORK.md` and a contract file in `core/`), `SPEC:147` (SA-2 allows an Orca mention "inside the contract file"), `SPEC:25` (E5: the guide has no Orca text today).
- Why Medium: AC-C1 matches `orca` or `orca-ide` followed by `orchestration`, `worktree`, `terminal` or `agent`. A routing section or a contract example that uses those words, as SA-2 allows, fails the phase's own pass condition (`SPEC:167`). Whether the new text uses those words is not specified, so this needs a guess. The spec also writes the pipes in AC-C1 as `\|` inside a markdown table; copied raw into a shell, the pattern and the second `grep` do not work, and the check can pass without checking anything.
- Recommendation: scan only the commands, skills and agents folders (the scope SA-2 states), and give the check as a code block.
- Priority: Medium.

### M-11 (Medium) Several requirements have no acceptance check

- Expert: Wiegers (verification), Adzic (examples).
- Where: `SPEC:61` (WC-3), `SPEC:64` (WC-6), `SPEC:69` (WC-11, tested only for `save` at `SPEC:207`), `SPEC:70` (WC-12) against `SPEC:167-210`. Also `SPEC:194` says "no Agent-tool wrapper, verified in the step-5 transcript", but step 5 searches only for `AskUserQuestion` (`SPEC:184`).
- Why Medium: the missing checks are requirements the document never tests, and none leads to a stated wrong outcome. The step-5 claim is a mismatch between two stated texts, but the wrapper check is a one-line addition.
- Recommendation: one check for the `ask` round trip (WC-3), one for a retry into a used directory (WC-6), and add the wrapper search to step 5.
- Priority: Medium.

## Expert consensus and disagreements

- Wiegers, Adzic, Cockburn agree that the primary actor (an Orca coordinator briefing a worker) and the goal (a command that finishes without a person and leaves one readable file) are clearly stated (`SPEC:16`, `SPEC:73`), and that the 27-row table is concrete and traceable to the inventories. They disagree with the spec only where the acceptance checks do not match the rows (F-01, M-01).
- Fowler, Newman, Hohpe agree with the layering decision: the coordinator plans, commands stay units of work, shared rules live in one installed file (`SPEC:16`, `SPEC:52`, `SPEC:264`). The rejected alternative is argued from checkable facts (`CAPS:97-103`, `CAPS:147-150`; `SPEC:28-39`). Hohpe notes the contract file is the only integration surface and that its location and status vocabulary are exactly where M-01 and M-02 sit.
- Nygard and Whittaker agree on the failure-path coverage the spec gets right: blocked runs still leave a file, the worker never asks through a local prompt, and nothing outward is on by default (`SPEC:60`, `SPEC:67`). They place the remaining weakness in the stale-file and unreadable-file paths (M-02, M-03).
- Residual disagreement: none between experts. Whittaker would grade M-02 higher if a crash during the contract write is credible; with no evidence of that in the inventories it stays Medium.

## Adversarial analysis (Whittaker, in the required template)

1. I can break this specification by **Divergence Attack**. The invariant at **AC-1.1 (SPEC:195)** fails when **the `load` row says there is no report file (SPEC:112) while the test demands a `return-contract.yaml` section in every command**. Concrete attack: P1 is finished per `SPEC:159`; the test iterates 37 commands; 24 lack the section, `load` among them, and for `load` the spec forbids adding one (`SPEC:265`). The phase gate (`SPEC:154`) then blocks P2 to P4. CRITICAL, blocking (F-01).
2. I can break this specification by **Zero/Empty Attack**. The invariant at **WC-5 (SPEC:63)** fails when **the contract file exists but is empty or unparseable**. Concrete attack: the command dies while writing; the worker finds the file; "succeeded otherwise" sends `--outcome succeeded`; the Task settles complete and its dependents become ready (`CAPS:34`). MAJOR label, Medium by consequence (M-02).
3. I can break this specification by **Sentinel Collision Attack**. The invariant at **section 2.1 (SPEC:51)** fails when **the topic contains the string `--unattended`**. Concrete attack: a person runs `/sc:tdd "add --unattended to the CLI"`; if the command matches by substring it skips its clarification question. MINOR to MAJOR label, Medium (M-04).
4. I can break this specification by **Sequence Attack**. The invariant at **WC-6 and WC-5 (SPEC:64, SPEC:63)** fails when **a retry reuses the first attempt's output directory**. Concrete attack: attempt 1 writes `status: succeeded`; attempt 2 is started with `--retry-of` into the same directory and dies before overwriting; the worker finds a report and sends `succeeded`. MAJOR label, Medium (M-03).
5. Accumulation Attack: no finding beyond M-07; the only counters in the spec are Orca's own (three consecutive failures, `CAPS:80`), and the spec does not change them.

## Follow-up candidates (Medium and minor; none triggers a revision)

Medium: M-01 (contract location), M-02 (unparseable status maps to success), M-03 (fresh directory and stale contract), M-04 (switch recognition), M-05 (`--interactive` combination), M-06 (authorising flags do not exist), M-07 (WC-10 scope and thresholds), M-08 (tasklist nesting and HALT), M-09 (WC-1 figure), M-10 (AC-C1 scope and form), M-11 (missing acceptance checks).

Minor notes:

- N-01: `SPEC:16` says command changes are "limited to the worker contract in section 2", but section 3 and SA-4 add drift fixes (roadmap, validate-roadmap, validate-tests, explain, business-panel, load; `SPEC:149`).
- N-02: `SPEC:154` says phases 1 to 3 need no user decision, but D4 touches auggie-review and task, which are P2 rows (`SPEC:244`, `SPEC:100`, `SPEC:121`), and every phase depends on D1 (`SPEC:51`). The spec does say phases 0 to 3 can proceed on the recommendations (`SPEC:225`).
- N-03: UNVERIFIED item 14 (`SPEC:285`) is a process note about a past citation check, not an unverified fact.
- N-04: step 6 of the live check (`SPEC:185`) expects only files under the output directory, which does not hold for commands that edit product files (cleanup, improve, document, implement; `SPEC:103`, `SPEC:107`, `SPEC:109`, `SPEC:110`), nor when two workers share a worktree (`SPEC:69`).
- N-05: P1 makes the flag accepted before the gates of P2 to P4 commands are resolved (`SPEC:159` against `SPEC:100-125`), so for a window a gated command accepts `--unattended` and still prompts. The spec's own rule says nothing about what the flag does then.
- N-06: `/sc:load` is described both as one of the 37 workers and as a step inside another worker's brief (`SPEC:112`, `SPEC:265`), which differs from "one worker runs one command" (`SPEC:16`).

Issue offer: the review-loop rule says the session that ran the review asks the user once whether to open an issue for the follow-up candidates. This worker was told to reply with a single `DONE` line, so it asked nothing and created nothing. The coordinator should ask.

## Brief clauses overridden

None. The brief narrowed the scope to the candidate and the inventories, which this review respected. It did not ask for any minor or Medium finding to be graded as blocking.

## Reviser brief

Repair only the blocking findings F-01 in the revised candidate `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`. This restates the Reviser contract: revise only text a blocking finding names; add no rule, mechanism or section that no blocking finding calls for; cite the finding id on every added paragraph or table; prefer deleting or narrowing to adding; report the byte size before and after, and the bytes added and deleted per finding id; leave minor and Medium findings alone; return the candidate once and do not award yourself a PASS.

- F-01: make `SPEC:195` (AC-1.1) agree with `SPEC:112`, `SPEC:159` and the phase table, so that the assertion covers only the commands each phase edits and `load` is exempt from the contract-section check.

verdict: FAIL
