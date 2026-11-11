review: 1 of 3

# Spec-panel critique: Orca worker-contract spec (round 1)

- candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`
- candidate sha256: d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d
- baseline: not applicable (first review; no `--baseline` or `--re-review` given)
- prior report: none
- reviewer model: claude-haiku-5-5
- mode: critique; focus: requirements, architecture; brief: FIRST-REVIEW prompt of `~/.claude/rules/prompts/document_review_loop_prompts.md`
- Whittaker (adversarial) is active in every panel review and is included below. Focus `correctness` is not active, so the State Variable Registry is not mandatory.

## Coverage and method

- Read in full: the spec-panel command definition supplied for this run (`command.md` in the run folder, outside the repo workspace), `.dev/orca-command-refactor/README.md`, the candidate spec, `inventory/commands-a.md`, `inventory/commands-b.md`, `inventory/orca-capabilities.md`, and the review-loop prompts file.
- Not opened (outside the workspace, so UNVERIFIED): `src/superclaude/**`, the project `CLAUDE.md`, `.claude/**`, `.dev/evals/**`, `.dev/codegraph-migration/**`, `~/.claude/rules/**` beyond the prompts file, and the Orca guide text. Where an inventory quotes one of these lines, I cite the inventory line instead and mark the underlying fact as inherited.
- Line numbers are for the candidate unless a file is named. `INV-A:n` = `.dev/orca-command-refactor/inventory/commands-a.md:n`, `INV-B:n` = `.../commands-b.md:n`, `CAPS:n` = `.../orca-capabilities.md:n`.
- No Orca command was run, nothing was committed, and only this file was written.

## Grading applied

- Blocking: a sentence that holds with no further assumption (two stated texts contradict, a stated text causes data loss or breaks a safety boundary, or an acceptance check cannot pass as written).
- Medium: the wrong outcome needs a guess, or the spec never states the requirement. Listed under follow-up candidates.
- Minor: a note.
- Open blocking findings: F1 only. Verdict is FAIL.

## Mandatory output artifacts

### Guard Condition Boundary Table

Triggered: the spec has gate, threshold and outcome conditions (WC-1 to WC-12, D1). Rows list the input classes that can occur; a class that cannot occur is left out with its reason in the note below the table. No cell is blank (FR-9). Each GAP cell carries its finding id (FR-8).

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| WC-5 outcome mapping | line 63 | Zero/Empty | no report file | no report exists: true | `--outcome failed` | OK |
| WC-5 outcome mapping | line 63 | One/Minimal | report status `partial` | succeeded | `--outcome succeeded`; dependents then start (CAPS:34) | GAP (F3) |
| WC-5 outcome mapping | line 63 | Typical | report status `succeeded` | succeeded | `--outcome succeeded` | OK |
| WC-5 outcome mapping | line 63 | Maximum/Overflow | status outside the four values | not defined | not specified; unknown values also go to F3 | GAP (F3) |
| WC-5 outcome mapping | line 63 | Sentinel Value Match | audit verdict FAIL with status `succeeded` | succeeded | `--outcome succeeded` (audit itself succeeded) | OK |
| WC-5 outcome mapping | line 63 | Legitimate Edge | status `blocked` | failed | `--outcome failed`; a worker's own failed report does not trip the breaker (CAPS:80, CAPS:116) | GAP (F17) |
| WC-2 gate resolution | line 60 | Zero/Empty | no default and no flag | blocked | write blocked contract and stop; WC-3 may instead ask | GAP (F4) |
| WC-2 gate resolution | line 60 | One/Minimal | flag supplied in brief | not blocked | proceed | OK |
| WC-2 gate resolution | line 60 | Typical | documented default | default used | proceed | OK |
| WC-2 gate resolution | line 60 | Sentinel Value Match | `--interactive` passed under `--unattended` | refused | stated per row in section 3 (e.g. line 103) | OK |
| WC-2 gate resolution | line 60 | Legitimate Edge | gate needs an answer input that the command does not define | blocked forever | not specified (review-translation row, line 117) | GAP (F11) |
| WC-4 contract write | line 62 | Zero/Empty | no output directory | no file written | "written on every outcome" (line 62) | GAP (F26) |
| WC-4 contract write | line 62 | One/Minimal | output directory given; first gate blocks | contract `status: blocked` | write and stop | OK |
| WC-4 contract write | line 62 | Sentinel Value Match | output directory is the repo root, shared with another run (index-repo) | file overwritten | WC-11 forbids the same file (line 69) | GAP (F1) |
| WC-4 contract write | line 62 | Legitimate Edge | adversarial output directory versus its subfolder | path ambiguous | line 83 vs line 62 | GAP (F5) |
| WC-1 readiness | line 59 | Typical | fallback answers at 30 s (cited EVIDENCE:45, outside workspace) | under 60 s | OK | OK |
| WC-1 readiness | line 59 | Maximum/Overflow | fallback at 45 s (cited EVIDENCE:56, outside workspace) | start fails again at about 45 s | "well inside" has no number | GAP (F14) |
| WC-10 wait split | line 68 | Typical | single tool call of 240 s | under 5 min | no split | OK |
| WC-10 wait split | line 68 | Maximum/Overflow | single tool call of 300 s | must split | split into at most 4 min | OK |
| WC-6 retry | line 64 | Zero/Empty | retry with no resume flag | fresh directory | report path changes; coordinator must update it | GAP (F23) |
| WC-12 consumer_fenced | line 70 | Sentinel Value Match | `check` returns `consumer_fenced` | stop, no `worker_done` | CAPS:67 | OK |
| Unattended switch (D1) | lines 51, 228 | Sentinel Value Match | `--unattended` quoted inside spec content | not a switch (spec-panel only, command.md:459) | not specified for other commands | GAP (F10) |

Classes left out: WC-6 Maximum (no numeric limit applies), WC-12 Typical (same as the sentinel row).

### Pipeline Dimensional Analysis

Triggered: the spec describes multi-stage flows whose counts can change (classification of the 43 commands; worker to coordinator to dependent Tasks, with N reports feeding one consumer at line 39).

- Stage annotation: inventories A and B give 21 + 22 = 43 commands (`INV-A:3`, `INV-B:3`). Partition: 10 ready (A 5 + B 5), 27 needing change (A 13 + B 14), 6 coordinator-only (A 3 + B 3). Sum 10 + 27 + 6 = 43, so the partition conserves count (checked against the inventory rows, not the repo; UNVERIFIED that the repo holds exactly 43 files).
- Downstream consumer: the example at line 39 feeds several troubleshoot reports to one adversarial worker. Divergence point: a failed or blocked report leaves the consumer blocked (CAPS:90), so the consumer runs on N reports or not at all. The spec defines no rule for a consumer wired to a subset (F22).

Quantity Flow Diagram:

```text
[43 commands: inventory A 21 + inventory B 22]  N=43
   --> [classify] --> [ready 10 (A5+B5)] [needs change 27 (A13+B14)] [coordinator-only 6 (A3+B3)]
       check: 10 + 27 + 6 = 43  (conserved)

[Task 1..N, one worker each] --> [worker_done + contract: N reports]  N
   --> [coordinator reads report] --> [dependent consumer, wired to all N]  expects N
                                  --> [dependent wired to subset]          expects N, receives N-k  <-- divergence (F22)
```

## === REQUIREMENTS ANALYSIS ===

### F1 (blocking, MAJOR): index-repo is listed as ready with no constraint, but WC-11 forbids the clash it creates

- Issue: WC-11 (line 69) says "Two workers in one worktree must never write the same file." The index-repo row (line 86) marks it ready today with no brief flag, and its output is a fixed `PROJECT_INDEX.md` ("location implied", INV-A:53). Placement defaults to the current worktree (CAPS:115).
- Grading check: "An implementer who follows the index-repo row as written dispatches two index-repo workers in the default placement, and both write PROJECT_INDEX.md, which WC-11 says must never happen." This needs no assumption beyond the placement default the spec itself cites. The output location is inferred (UNVERIFIED), but the clash holds for any fixed name.
- Expert: Wiegers (verdict and rule disagree), Nygard (silent overwrite of a coordinator-read output).
- Recommendation: give index-repo a per-run `--output` directory, or add the one-audit-per-worktree constraint that the cleanup-audit row already uses (line 85). Mark it needs-change until then.
- Priority: High. Quality impact: High (one run's output is lost without a signal).

### F2 (Medium, MAJOR): tool-permission prompts are not covered

- Issue: line 22 (E2) asserts "a command run by a worker has the same tools as a command a person runs". No requirement covers Claude Code tool-approval prompts (Bash, Write, MCP). A worker parked on such a prompt reports as `agentWait` (CAPS:52, CAPS:129), which 7.2 step 2 (line 181) treats as a failure, but WC-1 covers only startup and WC-2 covers only command gates.
- Why Medium: the stall depends on the worker's permission mode, which the spec never states (UNVERIFIED whether dispatched workers prompt). This is a requirement the spec does not state.
- Expert: Wiegers (missing requirement), Nygard (silent stall).
- Recommendation: add WC-13 requiring the brief to name the permission mode and the allowed tool set, and list tool-approval prompts in WC-2.
- Priority: High. Quality impact: High if confirmed.

### F3 (Medium, MAJOR): partial maps to succeeded, which releases dependents

- Issue: WC-5 (line 63) maps `partial` to `--outcome succeeded`. Orca then marks the Task complete and makes dependents ready (CAPS:34, CAPS:86). Section 2.3 (line 73) has the coordinator open the report but not check status before starting dependents. Unknown status values (for example `complete`) are not mapped at all.
- Why Medium: the wrong outcome (a dependent consumes partial output) needs the assumption that dependents need complete output. The decision row (line 263) accepts this trade-off, but the coordinator rule is missing.
- Expert: Hohpe (delivery semantics), Nygard (failure propagation).
- Recommendation: state that a `partial` Task releases only dependents marked as tolerant of partial input; map unknown status values to `failed`.
- Priority: High. Quality impact: Medium.

### F4 (Medium, MAJOR): WC-3 leaves the gate outcome undetermined, and AC-2.2 requires one of the two paths

- Issue: WC-3 (line 61) says "the session may instead ask the coordinator once", then "re-invoke or resume the command with the answer as a flag". AC-2.2 (line 200) requires `worker_done --outcome failed` and `status: blocked`. A worker that takes the ask path sends no `worker_done` and stalls at `agentWait`, so AC-2.2 fails.
- Why Medium: the implementer must choose which path applies; the text does not say when the ask path is used.
- Expert: Adzic (example and check disagree), Wiegers (ambiguous requirement).
- Recommendation: decide one rule. Either a blocked gate always writes a blocked contract and stops (and the coordinator re-dispatches with the answer), or ask is used only when the Task is still open. Make AC-2.2 match.
- Priority: High. Quality impact: Medium.

### F5 (Medium, MAJOR): the adversarial contract path contradicts WC-4

- Issue: row line 83 says "Fix the contract filename to `<output>/adversarial/return-contract.yaml`". WC-4 (line 62) says "In unattended mode the command writes `<output-dir>/return-contract.yaml`". Which path applies depends on whether adversarial's output directory is the passed directory or its subfolder. The spec does not say. AC-1.4 (line 198) expects one fixed path, but does not check the directory.
- Why Medium: the difference depends on how `<output-dir>` is read for adversarial.
- Expert: Wiegers (one contract rule), Hohpe (contract naming).
- Recommendation: write the adversarial path in WC-4 terms (for example `<output>/return-contract.yaml` with `<output>` as the passed directory) and have AC-1.4 check the full path.
- Priority: Medium. Quality impact: Medium.

### F6 (Medium, MAJOR): the spec-panel row is stale against the command definition supplied for this run

- Issue: row line 120 says spec-panel needs `--output` and a contract added. INV-B:182 says "no path or `--output` flag exists". The spec-panel definition supplied for this run already has `[--output <file>]` and `[--unattended]` in its usage line (command.md:22-23), and an "Unattended mode" section that uses `--report-dir` and writes `<report-dir>/return-contract.yaml` (command.md:455-466). It also uses `--report-dir`, not the `--output` / `--output-dir` named in WC-4.
- Why Medium: the repo copy `src/superclaude/commands/spec-panel.md` is outside the workspace (UNVERIFIED which version is current). If the supplied definition is current, the row and INV-B:182 are wrong, and the flag naming differs from WC-4.
- Expert: Wiegers (traceability to evidence), Fowler (one model for unattended commands).
- Recommendation: re-read the repo copy before planning Phase 2 for spec-panel; reconcile flag names (`--report-dir` against `--output-dir`) and the contract location in WC-4.
- Priority: High (accuracy of the plan). Quality impact: Medium.

### F7 (Medium, MAJOR): `--unattended` makes reflect accept its own remediation

- Issue: row line 88 says that under `--unattended`, `--remediate` should "follow the existing headless auto-accept rule instead of the `[yes / no]` prompt". Row line 122 says Stage 10.5 passes `--unattended` to each reflect "so the headless rule applies". The headless rule auto-accepts for auto-fixable registers and skips the gates (INV-B:109, quoting remediation-handoff.md:239-247, outside workspace). Section 9 D2 (line 236) says a rule of this kind "exists to stop an agent approving its own work". WC-9 (line 67) covers only outward actions, so reflect's own acceptance is not covered.
- Why Medium: the harm depends on what the remediation handoff does. The reflect skill (per the inventory) creates a package that a person or `/sc:implement` runs, which limits the harm, but the spec does not say so and does not state the authority rule for unattended remediation.
- Expert: Fowler (authority boundary), Wiegers (rule missing from WC-9).
- Recommendation: state the authority rule for unattended remediation (for example, reflect records the offer as blocked and the coordinator decides), and extend WC-9 to self-accepted remediation. Consider making this a D-item.
- Priority: High. Quality impact: High if the handoff executes code.

### F8 (Medium, MAJOR): the tasklist nesting claim is asserted but not established

- Issue: row line 122 says reflect's fan-out "runs one layer below the worker, inside Claude Code's nesting limit, `INV-A:14`". INV-A:14 gives the three-layer rule. Reflect's own Tier 1 and Tier 2 agents (INV-B:210; `cmd/reflect.md:142-143` quoted in INV-B) sit one or two layers deeper. INV-B:314 (UNVERIFIED item 1) marks nested spawning as unverified.
- Why Medium: the depth count is plausible but not shown, and the inventory that gives the rule marks the nested case unverified.
- Expert: Fowler (fan-out depth), Nygard (failure at the limit withdraws the Agent tool, INV-A:14).
- Recommendation: state the computed depth for the tasklist to reflect to adversarial path, or move Stage 10.5 to coordinator-owned Tasks, which the spec itself prefers (line 73; section 1.3).
- Priority: Medium. Quality impact: Medium.

### F9 (Medium, MAJOR): pr-submit is counted as a worker though the recommended D3 removes it

- Issue: D3 (line 240) recommends "Coordinator or person only" with "no pr-submit changes in Phase 4". Phase 4 (line 162) still schedules pr-submit, section 3 (line 75) counts 27 needing change including it, and the Decisions table (line 268) keeps "10 / 27 / 6".
- Why Medium: D3 is open, so the implementer cannot tell whether the count is final. The stated texts disagree, but no wrong build follows until the user answers D3.
- Expert: Wiegers (counts and recommendation must agree), Cockburn (who owns the outward action).
- Recommendation: report the counts both ways (with and without D3 option b), and mark pr-submit as coordinator-only in section 4 under the recommendation.
- Priority: Medium. Quality impact: Low.

### F10 (Medium, MAJOR): the scope of the section 2.2 rules is not stated, and WC-10 and WC-11 would change standalone behaviour

- Issue: section 2.2 (line 55) does not say which WC rules apply only under `--unattended`. WC-10 (line 68) says a command step "must be split" and WC-11 (line 69) says "Default output paths carry a timestamp or the slug the coordinator passes". SA-1 (line 146) says that without `--unattended`, output paths and default flags "stay as it is today".
- Why Medium: the reader must guess whether WC-10 and WC-11 are unattended-only. Under the strict reading, they break SA-1.
- Expert: Cockburn (actor and scope of each rule), Wiegers (missing restriction).
- Recommendation: put a scope tag on each WC row (worker session, `--unattended` only, or always), and tie WC-10 and WC-11 to `--unattended`.
- Priority: High. Quality impact: Medium.

### F11 (Medium, MAJOR): gates depend on inputs that the commands do not define

- Issue: the review-translation row (line 117) says Phase 1 "needs a pre-confirmed context input in the brief", but its "Other required change" column says "add a resume input, or fresh run" and the change is not defined. INV-B:39 shows no such input. The cli-eval row (line 104) and AC-2.2 (line 200) assume `--suite` and safety flags exist; the inventory does not show them (INV-A:44, UNVERIFIED).
- Why Medium: the gate can be resolved only once a flag exists, so the implementer must invent one.
- Expert: Adzic (example input), Cockburn (the answer has to reach the command).
- Recommendation: list each answer-input flag for each gate, with its command line, and mark flags that do not exist as needing a change.
- Priority: High. Quality impact: Medium.

### F12 (Medium, MAJOR): AC-0.4 claims a check that its cited step does not perform

- Issue: AC-0.4 (line 194) says each run is direct "(no Agent-tool wrapper, verified in the step-5 transcript)". Step 5 (line 184) only searches the transcript for `AskUserQuestion`. WC-7 (line 65) has no test.
- Why Medium: a reviewer can still check the transcript by hand, but the criterion as written does not verify what it claims.
- Expert: Adzic (check and property must match).
- Recommendation: add a step that asserts the first tool call of the worker is the command itself, or that no Agent tool call wraps it.
- Priority: Medium. Quality impact: Medium.

### F13 (MINOR): several needs-change verdicts rest on behaviour the inventories mark UNVERIFIED

- Issue: row line 111 (index) says "(whether it does is UNVERIFIED)". Row line 102 (business-panel) and row line 108 (explain) have the same issue (INV-A:113, UNVERIFIED item 6, line 277).
- Recommendation: state that these verdicts are provisional, and add a check that resolves each one.
- Priority: Low. Quality impact: Low.

### F14 (MINOR): "well inside the readiness limit" has no number

- Issue: WC-1 (line 59) says a prompt must "fall back on its own well inside the readiness limit (default 60 s)". The cited evidence shows 30 s passes and above about 45 s fails (EVIDENCE:45, EVIDENCE:56, outside workspace; CAPS:44-45 inside).
- Recommendation: state the fallback budget as a number, for example 30 s.
- Priority: Low. Quality impact: Low.

### F15 (Medium, MAJOR): release-split defaults to a fixed folder, which is the F1 problem in a different form

- Issue: row line 89 (release-split) gives no output constraint. The default output is `<spec-dir>/release-split/` (INV-B:122, `cmd/release-split.md:53` quoted there). Two runs on one spec in one worktree write the same files, which WC-11 forbids.
- Why Medium: it needs two runs on the same spec, which the coordinator would normally avoid.
- Recommendation: add `--output` to the brief constraint in the row, as adversarial does.
- Priority: Medium. Quality impact: Medium.

### F25 (MINOR): the cli-portify contract file location is unnamed, while AC-1.1 requires the name

- Issue: row line 105 says "file location unnamed". AC-1.1 (line 195) requires each command's Unattended section to name `return-contract.yaml`, which cli-portify cannot satisfy without a location.
- Recommendation: name the location in the row.
- Priority: Low. Quality impact: Low.

## === ARCHITECTURE ANALYSIS ===

### F16 (Medium, MAJOR): no placement rule for code-writing workers

- Issue: section 2.3 (line 73) says the brief states "the worktree placement (`CAPS:115`)", but the spec gives no rule by command class. CAPS:115 says the default is the current worktree. Code-writing commands (cleanup, improve, implement, document; INV-A:43, INV-A:52, INV-A:51, INV-A:47) can then edit the same tree in parallel. The project `CLAUDE.md` worktree rule (outside workspace, UNVERIFIED) requires an Orca-created worktree for parallel sessions.
- Why Medium: the clash needs two code-writing workers placed in one worktree, which the spec allows but does not forbid.
- Expert: Fowler (isolation), Nygard (shared-state failure).
- Recommendation: require a separate Orca worktree (`orca worktree create --agent claude`) for any command that writes product source, and leave the current worktree only for report-only commands.
- Priority: High. Quality impact: High.

### F17 (Medium, MAJOR): blocked is reported as failed, so the circuit breaker does not stop repeated blocked runs

- Issue: WC-5 (line 63) maps `blocked` to `--outcome failed`. Orca's breaker counts failed worker-start attempts, not a worker's own failed report (CAPS:80, CAPS:116). A coordinator that re-dispatches a blocked command with the same brief has no automatic stop. WC-6 (line 64) allows retry with `--retry-of`.
- Why Medium: the loop needs a coordinator that retries without a change to the brief. The spec does not forbid this.
- Expert: Nygard (stop condition), Hohpe (retry semantics).
- Recommendation: rule that a blocked Task is not retried until its blocked question is answered, and that the coordinator records the answer in the brief before retry.
- Priority: High. Quality impact: Medium.

### F18 (Medium, MAJOR): an appended Unattended section can contradict the gate text it overrides

- Issue: SA-4 (line 149) forbids editing the body of a command file, except for named defect fixes, and requires a new `## Unattended mode` section. The gate text stays in the body (for example the "Ask the user" lines in section 3), so one file carries two instructions for the same gate. Compliance is tested only live (AC-2.2, line 200).
- Why Medium: the override works only if the model follows the later section, which the spec does not evaluate.
- Expert: Fowler (overlay versus in-place change), Newman (contract drift between files).
- Recommendation: add a short gate-marker convention (for example an `Unattended:` line next to each gate) in the body, or add a static test that fails when a gate's body text lacks a pointer to the Unattended section.
- Priority: Medium. Quality impact: Medium.

### F19 (Medium, MAJOR): two commands are replaced by direct CLI calls, against the stated goal

- Issue: row line 124 (validate-roadmap) says "until then the coordinator dispatches `superclaude roadmap validate`". Row line 137 (swarm-wizard) says "Dispatches a worker that runs `uv run superclaude swarm run ...`". README line 6 states that commands stay the units of work. No decision records this change.
- Why Medium: the spec makes the switch quietly, without a decision entry.
- Expert: Newman (service boundary), Hohpe (unit of work).
- Recommendation: record this as a decision (D6), with the command and the CLI as alternatives.
- Priority: Medium. Quality impact: Medium.

### F20 (MINOR): the shared contract is an install-time dependency with no fallback

- Issue: line 52 installs the contract to `~/.claude/WORKER-CONTRACT.md`, and every Unattended section points to it. If the file is absent (older install, plugin install, UNVERIFIED mirror at `plugins/superclaude/commands/`, spec open item 8 at line 279), the rule set is undefined.
- Recommendation: each command section should carry its own minimum rule set, or fail closed (`status: blocked`) when the contract file is absent.
- Priority: Medium. Quality impact: Low.

### F21 (MINOR): the heartbeat requirement rests on a cadence that is not verified to matter

- Issue: WC-10 (line 68) says "The worker sends a heartbeat every 5 minutes while working". CAPS:130 says the cadence comes from the preamble, and whether Orca uses heartbeat age in liveness is UNVERIFIED (CAPS:130; spec open item 13 area). The stall check in 7.2 uses `agentWait` instead.
- Recommendation: keep the heartbeat as a requirement, but state that it is not relied on for liveness until verified.
- Priority: Low. Quality impact: Low.

### F22 (Medium, MAJOR): a consumer wired to a subset of N reports has no defined behaviour

- Issue: the example at line 39 feeds several troubleshoot reports to "one `/sc:adversarial` worker on their reports". CAPS:90 keeps dependents blocked when a dependency fails, so the consumer runs only when all N succeed. The spec does not forbid wiring the consumer to a subset. If the coordinator does, the consumer receives N-k reports where it expects N.
- Why Medium: a mismatch needs the coordinator to wire a subset, which the spec neither allows nor forbids. Under FR-19 a confirmed mismatch would be CRITICAL.
- Expert: Hohpe (fan-in), Nygard (partial success).
- Recommendation: state that fan-in consumers wait for all N, or define the subset rule and its count check.
- Priority: Medium. Quality impact: Medium.

### F23 (MINOR): a retry changes the report path, and the spec does not say so

- Issue: WC-6 (line 64) requires a fresh output directory for retry, but WC-4 (line 62) says the report path is "known before dispatch". After a retry, the path differs.
- Recommendation: state that a retry's brief carries a new contract path, and that the coordinator reads only the path in the latest `worker_done`.
- Priority: Low. Quality impact: Low.

### F24 (MINOR): the precedent for Orca workers ran the forbidden route

- Issue: E3 (line 23) says "It has worked before: in the codegraph planning run, Orca workers invoked `/sc:adversarial`". Section 1.4 (line 43) admits the precedent used an Agent-tool subagent, which WC-7 forbids. The table reads as proof while the caveat sits in 1.4.
- Recommendation: mark E3 as partial evidence in the table, and reference 1.4.
- Priority: Low. Quality impact: Low.

## ADVERSARIAL ANALYSIS (Whittaker)

Three attacks, in the required form. Each has a finding id above.

- I can break this specification by **Zero/Empty Attack**. The invariant at WC-4 (line 62) fails when the brief omits the output directory. Concrete attack: the brief omits `--output`; the worker runs; no directory exists, so no `return-contract.yaml` is written; WC-5 (line 63) then sends `--outcome failed` with no report, and the coordinator cannot tell a blocked gate from a crash. Severity: MAJOR. See F26.
- I can break this specification by **Sequence Attack**. The invariant at WC-3 (line 61), "re-invoke or resume the command with the answer as a flag", fails when the gate has no answer flag. Concrete attack: the review-translation worker asks at Phase 1; the coordinator replies; no input exists to receive the reply (line 117), so the reply is discarded or the worker stalls at `agentWait`. Severity: MAJOR. See F4 and F11.
- I can break this specification by **Accumulation Attack**. The invariant at WC-5 (line 63), "blocked becomes failed", fails when the coordinator re-dispatches the same blocked command. Concrete attack: each dispatch returns a worker's own failed report; CAPS:80 says that does not trip the breaker; no count stops the loop. Severity: MAJOR. See F17.

## Quality metrics

| Dimension | Score (0-10) | Basis |
|---|---|---|
| Clarity | 6 | Terms "partial", "blocked", "ask" and "gate" are used in more than one sense (F3, F4) |
| Completeness | 6 | Permission, placement and scope rules are missing (F2, F10, F16) |
| Testability | 5 | Most checks are concrete; AC-0.4 and the WC-3 path cannot be tested as written (F4, F12) |
| Consistency | 4 | Contract paths, counts and the D3 recommendation disagree (F1, F5, F9) |

## Blocking findings

- F1 only. See the grading check under F1.

## Follow-up candidates (Medium and minor)

Medium findings and minor notes never trigger a revision and never fail the review. The coordinator asks the user once whether to open an issue for them. No issue has been created.

- Medium: F2, F3, F4, F5, F6, F7, F8, F9, F10, F11, F12, F15, F16, F17, F18, F19, F22, F26.
- Minor: F13, F14, F20, F21, F23, F24, F25.

## Reviser brief

Blocking finding ids for this round: F1.

Revise only the text that F1 names (the index-repo row, line 86). Add no rule, mechanism or section that F1 does not call for. Prefer deleting or narrowing to adding. Every added paragraph or table cites F1. Report the byte size before and after, and the bytes added and deleted for F1. Medium and minor findings are out of scope. Do not award a PASS.

## Medium finding F26 (WC-4 with no output directory)

- Issue: WC-4 (line 62) says the contract is written "including stops before any other output exists" (line 62). A contract needs a directory, and a brief without `--output` gives no directory. The spec-panel refusal path (command.md:460) writes nothing and prints in chat, which the coordinator cannot read (INV-A:17).
- Why Medium: the requirement is missing a rule for the no-directory case; the outcome (`failed` with no report, WC-5) is defined.
- Expert: Cockburn (the coordinator is the actor who omits the flag), Nygard (no report on a refusal).
- Recommendation: state that the brief must always carry the output directory, and that a missing directory is a blocked brief at dispatch, not a worker outcome.
- Priority: High. Quality impact: Medium.

## Findings block

```findings-v1
{"id": "F1", "severity": "MAJOR", "blocking": true, "category": "contradiction", "anchor": "Two workers in one worktree must never write the same file", "anchor2": "`PROJECT_INDEX.md` (location implied)", "refs": ["WC-11", "3.1 index-repo row line 86", "CAPS:115", "INV-A:53"], "claim": "Two index-repo workers in the default shared worktree both write PROJECT_INDEX.md, so one run's output is overwritten, which WC-11 forbids, while the row still lists index-repo as ready with no constraint."}
{"id": "F2", "severity": "MAJOR", "blocking": false, "category": "missing-requirement", "anchor": "a command run by a worker has the same tools as a command a person runs", "refs": ["WC-1", "WC-2", "CAPS:52", "CAPS:129", "7.2 step 2 line 181"], "claim": "No requirement covers tool-permission prompts, so a worker parked on a Bash or Write approval stalls like a question and is not caught by WC-1 or WC-2."}
{"id": "F3", "severity": "MAJOR", "blocking": false, "category": "missing-requirement", "anchor": "`--outcome succeeded` otherwise, including `partial`", "refs": ["WC-5 line 63", "2.3 line 73", "CAPS:34", "CAPS:86", "CAPS:90"], "claim": "A partial report becomes a succeeded Task that releases dependents with no status check required, and unknown status values are not mapped."}
{"id": "F4", "severity": "MAJOR", "blocking": false, "category": "contradiction", "anchor": "the session may instead ask the coordinator once", "anchor2": "`worker_done --outcome failed`; contract `status: blocked`", "refs": ["WC-2 line 60", "WC-3 line 61", "AC-2.2 line 200"], "claim": "WC-3 lets a blocked gate wait on ask, which sends no worker_done, while AC-2.2 requires a failed worker_done with status blocked, so the two paths cannot both pass."}
{"id": "F5", "severity": "MAJOR", "blocking": false, "category": "contradiction", "anchor": "Fix the contract filename to `<output>/adversarial/return-contract.yaml`", "anchor2": "In unattended mode the command writes `<output-dir>/return-contract.yaml`", "refs": ["3.1 adversarial row line 83", "WC-4 line 62", "AC-1.4 line 198"], "claim": "The adversarial row places its contract in an adversarial subfolder while WC-4 places it at the output directory root, and the spec does not say which output directory applies."}
{"id": "F6", "severity": "MAJOR", "blocking": false, "category": "other", "anchor": "`target_release` required as a flag for TDD inputs, else blocked", "refs": ["3.2 spec-panel row line 120", "INV-B:182", "command.md:22-23 and 455-466 (outside repo; repo copy UNVERIFIED)"], "claim": "The spec-panel row asks for --output and a new contract, but the supplied command definition already has both, under --report-dir, so the row and INV-B:182 are stale or the repo copy differs."}
{"id": "F7", "severity": "MAJOR", "blocking": false, "category": "safety", "anchor": "make `--remediate` follow the existing headless auto-accept rule", "anchor2": "Stage 10.5 passes `--unattended` to each reflect so the headless rule applies", "refs": ["3.1 reflect row line 88", "3.2 tasklist row line 122", "D2 line 236", "WC-9 line 67", "SA-6 line 151", "INV-B:109"], "claim": "Under --unattended, reflect accepts its own remediation offer, and WC-9 does not cover self-accepted remediation, so the authority rule that D2 states for implement is absent for reflect."}
{"id": "F8", "severity": "MAJOR", "blocking": false, "category": "other", "anchor": "inside Claude Code's nesting limit", "refs": ["INV-A:14", "INV-B:210", "INV-B:314 UNVERIFIED item 1"], "claim": "The tasklist row asserts that reflect fan-out stays inside the nesting limit, but the depth is not computed and the inventory that gives the rule marks nested spawning unverified."}
{"id": "F9", "severity": "MAJOR", "blocking": false, "category": "contradiction", "anchor": "no pr-submit changes in Phase 4", "anchor2": "keep the inventories' 10 / 27 / 6 split", "refs": ["D3 line 240", "P4 row line 162", "section 3 line 75", "Decisions line 268"], "claim": "The recommended D3 makes pr-submit coordinator-only, but the 10/27/6 split and the phase plan still count and schedule pr-submit as a worker."}
{"id": "F10", "severity": "MAJOR", "blocking": false, "category": "missing-requirement", "anchor": "Default output paths carry a timestamp or the slug the coordinator passes", "anchor2": "Without `--unattended`, every prompt, approval gate", "refs": ["WC-10 line 68", "WC-11 line 69", "SA-1 line 146", "section 2.2 intro line 55"], "claim": "The scope of WC-2 to WC-12 is not stated, and read strictly WC-10 and WC-11 change standalone wait sizes and default output paths that SA-1 keeps unchanged."}
{"id": "F11", "severity": "MAJOR", "blocking": false, "category": "missing-requirement", "anchor": "Phase 1 needs a pre-confirmed context input in the brief", "anchor2": "add a resume input, or fresh run", "refs": ["3.2 review-translation row line 117", "INV-B:39", "3.2 cli-eval row line 104", "AC-2.2 line 200"], "claim": "The review-translation gate needs an input that the command does not define, and the cli-eval flags assumed by AC-2.2 are not shown to exist."}
{"id": "F12", "severity": "MAJOR", "blocking": false, "category": "other", "anchor": "no Agent-tool wrapper, verified in the step-5 transcript", "anchor2": "search the transcript for `AskUserQuestion`", "refs": ["AC-0.4 line 194", "7.2 step 5 line 184", "WC-7 line 65"], "claim": "AC-0.4 says the top-level property is verified in step 5, but step 5 only searches for AskUserQuestion, so the Agent-tool wrapping that WC-7 forbids has no check."}
{"id": "F13", "severity": "MINOR", "blocking": false, "category": "other", "anchor": "(whether it does is UNVERIFIED)", "refs": ["3.2 index row line 111", "INV-A:54", "section 3 line 102 and line 108", "UNVERIFIED item 6 line 277"], "claim": "Several needs-change verdicts rest on behaviour the inventories mark UNVERIFIED, so those verdicts are provisional."}
{"id": "F14", "severity": "MINOR", "blocking": false, "category": "missing-requirement", "anchor": "well inside the readiness limit", "refs": ["WC-1 line 59", "CAPS:44-45", "EVIDENCE:45 and EVIDENCE:56 outside workspace"], "claim": "The fallback budget for a startup prompt is given as well inside the 60 s limit with no number, so an implementer cannot test it."}
{"id": "F15", "severity": "MAJOR", "blocking": false, "category": "missing-requirement", "anchor": "spec-shaped input; default `--r1-scope`; never `--interactive`", "refs": ["3.1 release-split row line 89", "INV-B:122", "WC-11 line 69"], "claim": "release-split has a fixed default output beside the spec and no output constraint, so two runs on one spec write the same files, which WC-11 forbids."}
{"id": "F16", "severity": "MAJOR", "blocking": false, "category": "missing-requirement", "anchor": "and the worktree placement (`CAPS:115`)", "refs": ["2.3 line 73", "CAPS:115", "WC-11 line 69", "project CLAUDE.md worktree rule (outside workspace, UNVERIFIED)"], "claim": "The brief must state worktree placement, but no rule by command class exists, so code-writing workers can share one worktree and edit the same files."}
{"id": "F17", "severity": "MAJOR", "blocking": false, "category": "other", "anchor": "`--outcome failed` when the report says `failed` or `blocked`", "anchor2": "A retry worker (`worker-start --retry-of`) must not corrupt the first attempt's output", "refs": ["WC-5 line 63", "WC-6 line 64", "CAPS:80", "CAPS:116"], "claim": "A blocked gate is reported as failed, but Orca's breaker does not count a worker's own failed report, so a coordinator can re-dispatch a blocked command without limit."}
{"id": "F18", "severity": "MAJOR", "blocking": false, "category": "other", "anchor": "Command-file edits in Phases 1-3 are additive", "anchor2": "Each gate resolves one of three ways, listed per command in section 3", "refs": ["SA-4 line 149", "WC-2 line 60", "AC-2.2 line 200"], "claim": "An appended Unattended section overrides gate text that stays in the command body, so one file carries two instructions for the same gate and the override is tested only live."}
{"id": "F19", "severity": "MAJOR", "blocking": false, "category": "other", "anchor": "the coordinator dispatches `superclaude roadmap validate`", "anchor2": "Dispatches a worker that runs `uv run superclaude swarm run ...`", "refs": ["3.2 validate-roadmap row line 124", "section 4 swarm-wizard line 137", "README line 6"], "claim": "validate-roadmap and swarm-wizard are replaced by direct CLI calls, which breaks the stated rule that commands are the units of work, with no decision recorded."}
{"id": "F20", "severity": "MINOR", "blocking": false, "category": "missing-requirement", "anchor": "installed to `~/.claude/WORKER-CONTRACT.md`", "refs": ["section 2.1 line 52", "spec open item 8 line 279"], "claim": "Every Unattended section depends on an installed contract file with no fallback, so a missing file leaves the rules undefined."}
{"id": "F21", "severity": "MINOR", "blocking": false, "category": "other", "anchor": "The worker sends a heartbeat every 5 minutes while working", "refs": ["WC-10 line 68", "CAPS:130"], "claim": "The heartbeat requirement rests on a cadence from the preamble, and its role in liveness is unverified, so its value to the design is unproven."}
{"id": "F22", "severity": "MAJOR", "blocking": false, "category": "missing-requirement", "anchor": "then one `/sc:adversarial` worker on their reports", "refs": ["section 1.3 line 39", "CAPS:90"], "claim": "A fan-in consumer wired to a subset of N reports has no defined behaviour, so it can receive N-k reports where it expects N."}
{"id": "F23", "severity": "MINOR", "blocking": false, "category": "missing-requirement", "anchor": "A retry worker (`worker-start --retry-of`) must not corrupt the first attempt's output", "refs": ["WC-6 line 64", "WC-4 line 62", "2.3 line 73"], "claim": "A retry needs a fresh output directory and so a new contract path, which the spec does not tell the coordinator to read."}
{"id": "F24", "severity": "MINOR", "blocking": false, "category": "other", "anchor": "It has worked before: in the codegraph planning run", "refs": ["E3 line 23", "section 1.4 line 43"], "claim": "E3 presents a precedent that used the Agent-tool route WC-7 forbids as support for the direct route, with the caveat only in section 1.4."}
{"id": "F25", "severity": "MINOR", "blocking": false, "category": "missing-requirement", "anchor": "file location unnamed", "refs": ["3.2 cli-portify row line 105", "AC-1.1 line 195"], "claim": "AC-1.1 requires each Unattended section to name return-contract.yaml, but the cli-portify row does not give the location."}
{"id": "F26", "severity": "MAJOR", "blocking": false, "category": "missing-requirement", "anchor": "including stops before any other output exists", "refs": ["WC-4 line 62", "WC-5 line 63", "command.md:460 outside repo"], "claim": "WC-4 requires a contract for stops before output exists, but a contract needs an output directory, and a brief without one gets no file."}
```

verdict: FAIL
