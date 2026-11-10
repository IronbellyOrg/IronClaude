review: 1 of 3

# Spec-panel critique: Orca worker contract spec (review 1 of 3)

## Header

- Candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (285 lines)
- Candidate SHA-256: `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d`
- Baseline: missing (first review, no `--re-review`). Prior report: none.
- Reviewer model: claude-haiku-5-5
- Command: `/sc:spec-panel --mode critique --focus requirements,architecture`, FIRST-REVIEW prompt of `~/.claude/rules/prompts/document_review_loop_prompts.md` (read in full, sandbox copy at `home/.claude/rules/prompts/document_review_loop_prompts.md`).
- Panel (command.md Focus Areas): requirements = Wiegers (lead), Adzic, Cockburn; architecture = Fowler (lead), Newman, Hohpe, Nygard; Whittaker active in every panel review.
- Verdict: FAIL (3 blocking findings, F1 to F3).

Citation keys: `spec:N` = `ws/.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` line N. `INV-A:N`, `INV-B:N`, `CAPS:N` = `ws/.dev/orca-command-refactor/inventory/commands-a.md`, `commands-b.md`, `orca-capabilities.md` line N. `README:N` = `ws/.dev/orca-command-refactor/README.md` line N. Anything cited to a file outside the workspace (src/, .claude/, ~/.claude, .dev/evals, .dev/codegraph-migration, /opt/Orca, GitHub) is UNVERIFIED here, and so is the spec's own citation of it.

## Coverage

- Read in full: the spec, README, `orca-capabilities.md` (188 lines), `commands-a.md` (120 lines), `command.md`, and the rules prompt file. Read `commands-b.md` lines 1-60 and 280-323 and grep-located the rows and notes it cites.
- Checked against the workspace: about 30 `CAPS:` cites in spec sections 1, 2, 8, 9 and the UNVERIFIED list. Every one points at a line that carries the cited fact (for example `CAPS:44-45` 60 s default and `--timeout-ms`; `CAPS:73` `--outcome` mandatory; `CAPS:79` report-file handling UNVERIFIED; `CAPS:97-102` depth 1; `CAPS:99` settings; `CAPS:156` and `CAPS:187` PR #329 unverified). Also checked: `INV-A:76-83`, `INV-A:90`, `INV-A:94-98`, `INV-A:97`, `INV-B:272`, `INV-B:292-299`, `INV-B:301`, `INV-B:311`, `INV-B:323`, and the summary counts. All matched.
- Counts: INV-A summary is 5 ready, 13 needs-change, 3 coordinator-only (`INV-A:73`); INV-B is 5 ready, 14 needs-change, 3 coordinator-only (`INV-B:280-289`). Spec sections 3.1 (10), 3.2 (27) and 4 (6) account for all 43 commands, consistent with those counts.
- Not checked: the command and skill files under `src/`, the evidence under `.dev/evals` and `.dev/codegraph-migration`, and the Orca binary. Those citations are UNVERIFIED here.
- The command's Pipeline Dimensional Analysis trigger was evaluated (see the section below). The Guard Condition Boundary Table was produced because the spec has conditional logic.

## Blocking findings

### F1 (blocking, MAJOR, unpassable-check): AC-0.4 cannot pass as written for /sc:troubleshoot in P0

- `spec:194` requires steps 1-3 and 5-7 of the live check to pass for `/sc:troubleshoot` in P0, and says step 4 "uses the command's existing report file".
- `spec:182` (step 3) requires the `worker_done` report path to be "the WC-4 contract path" and the outcome to match "the contract's `status`".
- `spec:91` says troubleshoot's report today is `REPORT.md` and it writes no contract. `spec:158` says the contract arrives only in P1.
- `spec:183` (step 4) parses the file as YAML and reads `d['status']`, which a Markdown report cannot satisfy.
- Sentence: An implementer who follows the stated text as written runs step 3 on `/sc:troubleshoot` in P0 and requires a contract path that does not exist yet, and that is wrong because the spec's own rows say there is no contract until P1, so AC-0.4 cannot pass for that command.

### F2 (blocking, MAJOR, contradiction): the load row contradicts WC-4 and AC-1.1

- `spec:62` (WC-4) requires that in unattended mode the command writes `<output-dir>/return-contract.yaml`, for every command in sections 3.1 and 3.2 (`spec:195`, AC-1.1 requires the `## Unattended mode` section of each to name it).
- `spec:112` gives load's report as "none (see note)" and its change as "usage line only". `spec:159` (P1) repeats that.
- `spec:265` justifies the omission: "a report file would be an unrequested addition". That reasoning is not in WC-4, and WC-4 has no exception.
- `INV-B:31` and `INV-B:65` support the fact that load writes no file, so the conflict is between the spec's own rules.
- Sentence: An implementer who follows the load row builds a load command with no contract, and that is wrong because WC-4 and AC-1.1 both require one, so AC-1.1 fails for load.

### F3 (blocking, MAJOR, contradiction): the adversarial contract path contradicts WC-4

- `spec:62` defines the path as `<output-dir>/return-contract.yaml`, where `<output-dir>` is "the directory the coordinator passed".
- `spec:83` says the brief passes `--output <dir>`, and the P1 fix is "`<output>/adversarial/return-contract.yaml`".
- `spec:198` (AC-1.4) requires adversarial to "name one fixed path" without saying which one.
- `INV-A:35` and `INV-A:60` say adversarial's output goes under `<output>/adversarial/`, and that real runs wrote the contract in two different places.
- Sentence: An implementer who follows WC-4 writes the adversarial contract at `<dir>/return-contract.yaml`, and that is wrong because the P1 row for the same command, and therefore the coordinator's reader, puts it at `<dir>/adversarial/return-contract.yaml`.

## Follow-up candidates (Medium and minor; not blocking)

The coordinator asks the user once whether to open an issue for these. None is created here.

### F4 (MAJOR label, Medium, missing-requirement; Fowler/Hohpe): a partial run settles as succeeded, and dependents may start on it

- `spec:263` and `spec:63` (WC-5) map `partial` to `--outcome succeeded`.
- `CAPS:77` says a valid `worker_done` settles the Task. `CAPS:88` says dependents stay blocked until the dependency completes. `CAPS:86` describes the ready-wave pattern, in which the coordinator starts whatever `task-list --ready` shows.
- `spec:73` requires the coordinator to open the report after `worker_done`, but says nothing about dependents waiting for the contract status.
- Medium because the wrong outcome needs the coordinator to start dependents before it reads the contract.

### F5 (Medium, missing-requirement; Wiegers/Fowler): who creates the "fresh" output directory

- `spec:64` (WC-6) says a command "writes each run into a fresh output directory so a re-run starts clean".
- `spec:62` (WC-4) and `spec:73` (2.3) say the coordinator passes the output directory and it is known before dispatch.
- The spec does not say whether the command or the brief chooses the fresh directory. If the command does, the WC-4 path is not known before dispatch. If the coordinator does, WC-6 misattributes the duty. Resume commands with no prior state are also unspecified.

### F6 (MAJOR label, Medium; Whittaker, Sequence Attack): a stale contract can turn a crashed run into a reported success

- I can break this specification by **Sequence Attack**. The invariant at **WC-5 `spec:63`, "or no report exists"** fails when **a re-run writes nothing and an earlier run's contract is still in the output directory**. Concrete attack: run 1 finishes and writes `status: succeeded`; the coordinator re-dispatches the Task to the same directory (`spec:64` permits `--retry-of`); run 2 crashes before writing its contract; WC-5 finds the old file, so the worker sends `--outcome succeeded`.
- The spec never requires clearing or versioning the contract before a run.
- Related degenerate input (Zero/Empty): an empty or unparseable contract is neither "failed or blocked" nor clearly "succeeded", so WC-5 does not map it.

### F7 (MAJOR label, Medium, missing-requirement; Adzic/Cockburn): the WC-3 ask route cannot carry the answer for free-text gates

- `spec:61` (WC-3) says the session "may" ask the coordinator and then "re-invoke or resume the command with the answer as a flag". No flag exists for free-text gates, such as the tdd topic clarification (`spec:90`) or the cli-eval W0 confirmation (`spec:104`).
- Because WC-3 is optional ("may"), the expected outcome in AC-2.2 (`spec:200`: `worker_done --outcome failed`, contract `blocked`) is not deterministic.
- Whether a legitimate `ask` sets `observation.agentWait` is UNVERIFIED. If it does, AC-2.2 step 2 (`spec:181`) fails on a correct run. `CAPS:129` describes agentWait as a prompt "only a human can answer", which is not what `ask` is.

### F8 (MAJOR label, Medium, missing-requirement; Newman/Nygard): tool-permission prompts are not covered, and E2's "same tools" claim is not evidenced

- `spec:22` (E2) claims that a command run by a worker "has the same tools as a command a person runs". Its cited evidence (`CAPS:161`, `EVIDENCE.md:45`, which is outside the workspace) shows only that the agent reached `input_accepted`. It shows nothing about tools or permission mode.
- WC-2 (`spec:60`) covers `AskUserQuestion` and chat questions only. No requirement sets the worker's permission mode or handles per-tool approval prompts (Bash, Write, `gh`). Such a prompt is a person-blocking step that WC-2 does not address.
- `CAPS:52` and `CAPS:129` show that such a stall is visible only through agentWait.
- `CAPS:50` says Orca pre-accepts trust for Claude. That is trust only, not tool approval.

### F9 (MAJOR label, Medium, missing-requirement; Adzic): the "ready today" heading conflicts with the rows it covers

- `spec:78-79` says the ten commands "run as workers now if the brief uses the stated flags".
- The tdd row (`spec:90`) says that its `/task` "ask the user" lines resolve as blocked only "Under `--unattended`", which is a P2 change. The ready-today brief does not pass `--unattended`.
- `INV-B:47` says rare questions are handled "via `ask`". Commands cannot call `ask` (`spec:147` SA-2, `spec:66` WC-8), so that mechanism does not exist in the spec.
- Medium because the stall needs the question to fire, which is an assumption about the input.

### F10 (MAJOR label, Medium, missing-requirement; Fowler): several commands have no defined contract location

- `spec:62` and `spec:73` require a known output directory for every Task. Several 3.2 rows give no output flag or location: cli-eval (`spec:104`), cli-portify (`spec:105`, "file location unnamed"), research (`spec:116`), review-translation (`spec:117`), roadmap (`spec:118`), save (`spec:119`), task (`spec:121`), tasklist (`spec:122`), pr-submit (`spec:114`, "beside `monitor-run-<PR>.jsonl`"), implement (`spec:109`, "beside the ledger"), validate-roadmap (`spec:124`), validate-tests (`spec:125`).
- cli-eval's paths are fixed (`INV-A:44` cites `.dev/eval-workspaces/cli-eval/` and `.dev/eval-runs/<date>/<run-id>/`), so its "fresh dir" entry (`spec:104`) cannot be met, and WC-11's timestamped default (`spec:69`) does not apply.

### F11 (MAJOR label, Medium, missing-requirement; Hohpe): long Agent-tool calls have no heartbeat rule

- `spec:68` (WC-10) applies only to a command step that "blocks a single tool call for longer than 5 minutes" and requires splitting it. `spec:65` (WC-7) says a command's own Agent-tool fan-out "stays as it is".
- A single Agent call that runs 10 minutes is therefore not covered. `INV-A:65` says the cli-eval eval can run 3600 s, and `CAPS:130` gives the 5-minute heartbeat cadence.
- Whether an in-progress Agent call blocks heartbeats is UNVERIFIED.

### F12 (MAJOR label, Medium, other; Crispin-style check design): AC-C1 passes vacuously as written, and its scope conflicts with SA-2 and P0

- `spec:172` (AC-C1) uses `(orchestration\|worktree\|terminal\|agent)`. In grep -E, `\|` is a literal pipe, not alternation, so the pattern matches almost nothing and the check passes even when an Orca call is added. Markdown table rendering may hide the escape, so the raw text is what an implementer copies.
- AC-C1 scans `src/superclaude/core`, which contains the contract file (`spec:52`) and the P0 HOW-WE-WORK Orca section (`spec:158`). SA-2 (`spec:147`) permits an Orca mention "inside the contract file" only, and the AC has no exemption.

### F13 (MINOR, missing-requirement; Wiegers, testability): "well inside the readiness limit" has no number

- `spec:59` (WC-1) says the fallback must fire "well inside the readiness limit (default 60 s)". Its evidence says a 30 s fallback passes and "above about 45 s it fails again". The spec does not state a bound, so two implementers can choose 30 s and 50 s.

### F14 (MINOR, missing-requirement): the cli-eval safety flags are not named

- `spec:104` says `run` requires `--suite` "and the safety flags in the brief, else blocked", but the spec never names them. The gate cannot be implemented or tested as written.

### F15 (MINOR, missing-requirement): unattended switch rules are not stated

- `spec:228` (D1) recommends an explicit `--unattended` flag. The spec does not say what happens when `--unattended` and `--interactive` are both passed, or whether a token inside quoted content counts.
- The spec-panel command has such a rule (`command.md:459`, "standalone argument token outside any quoted argument"), but the spec gives no shared rule for the other commands.

### F16 (MINOR, other): a fact is stated that the evidence marks UNVERIFIED

- `spec:62` says "Orca does not check the file, so the coordinator opens it". `CAPS:79` marks Orca's handling of the file UNVERIFIED, and `spec:274` (UNVERIFIED item 3) says "the spec assumes it does not". The design holds either way, but the wording should match the evidence.

### F17 (MINOR, missing-requirement): the contract's install path is absent in a dev checkout

- `spec:52` installs the contract to `~/.claude/WORKER-CONTRACT.md`. The spec's live checks (`spec:196`, AC-1.2) need that installed file, and the spec does not state that `superclaude install` must run first. Whether `make sync-dev` copies core files is UNVERIFIED here.

### F18 (MINOR, other): the index row asks a command to state an unverified fact

- `spec:111` requires the command to "state that knowledge-base mode does not wait". `spec:277` (UNVERIFIED item 6) says whether it waits is unknown. The rule asks the implementer to write a claim the spec itself cannot support.

### F19 (MINOR, other; Whittaker, Zero/Empty): the step 2 pass condition is satisfied by absence

- `spec:181` (7.2 step 2) passes when `observation.agentWait` is "never non-null". `CAPS:129` says a null value means Orca looked and found no wait, while an absent field means it never looked. The check therefore passes when the coordinator never looked, which the step itself requires it to do.

## Mandatory output artifact: Guard Condition Boundary Table

Triggered: the spec has conditional logic and threshold checks (WC-1 to WC-12, the 0.70 gate in row `spec:121`, the `--suite` gate in `spec:104`). Each guard is enumerated below. Classes that cannot occur are left out with a reason. Status GAP generates the finding named in the last column.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|-------|----------|-----------------|----------------|--------------|-------------------|--------|
| G1 WC-5 outcome | `spec:63` | Zero/Empty (empty or unparseable contract) | `""` | neither rule applies | not stated | GAP (F6) |
| G1 WC-5 outcome | `spec:63` | Typical | `status: succeeded` | succeeded | `--outcome succeeded` | OK |
| G1 WC-5 outcome | `spec:63` | Sentinel Value Match | `status: blocked` | failed | `--outcome failed` | OK |
| G1 WC-5 outcome | `spec:63` | Legitimate Edge Case | `status: partial` | succeeded | maps to succeeded; dependents not addressed | GAP (F4) |
| G1 WC-5 outcome | `spec:63` | Stale contract from an earlier run | prior `status: succeeded` | succeeded | "no report exists" never true | GAP (F6) |
| G1 WC-5 outcome | `spec:63` | Maximum/Overflow | N/A | N/A | `status` is a four-value enum, so there is no overflow | OK (reason) |
| G2 WC-6 resume or fresh | `spec:64` | Zero/Empty (output dir exists, empty) | empty dir | fresh or resume not decided | who creates the dir is unstated | GAP (F5) |
| G2 WC-6 resume or fresh | `spec:64` | One/Minimal (resume flag, no prior state) | no ledger | unspecified | not stated | GAP (F5) |
| G2 WC-6 resume or fresh | `spec:64` | Typical | resume flag, prior state | resumes | per-command rows in section 3 | OK |
| G2 WC-6 resume or fresh | `spec:64` | Sentinel (resume flag on a command with none) | `--resume` on analyze | not accepted | section 3 names the mode per command | OK |
| G2 WC-6 resume or fresh | `spec:64` | Legitimate Edge (retry into a directory holding a prior contract) | prior `succeeded` | stale contract | not addressed | GAP (F6) |
| G3 WC-2 gate resolution | `spec:60` | Zero/Empty (gate with no default, no flag) | none | blocked (c) | write contract with `status: blocked` | OK |
| G3 WC-2 gate resolution | `spec:60` | One/Minimal (flag supplied once) | one flag | answer used (b) | caller's flag | OK |
| G3 WC-2 gate resolution | `spec:60` | Typical (documented default) | default present | default (a) | section 3 default | OK |
| G3 WC-2 gate resolution | `spec:60` | Sentinel (`--unattended` with `--interactive`) | both | unspecified in WC-2 | section 3 refuses `--interactive` for some commands only | GAP (F15) |
| G3 WC-2 gate resolution | `spec:60` | Legitimate Edge (free-text gate, no flag) | tdd topic | blocked, then ask | no flag to carry the answer | GAP (F7) |
| G3 WC-2 gate resolution | `spec:60` | Maximum/Overflow | N/A | N/A | no numeric threshold in WC-2 | OK (reason) |
| G4 WC-1 startup timing | `spec:59` | Zero/Empty (fallback 0 s) | 0 s | prompt never shown | not forbidden | OK |
| G4 WC-1 startup timing | `spec:59` | Typical (30 s fallback) | 30 s | ready within 60 s | `EVIDENCE.md:45` | OK |
| G4 WC-1 startup timing | `spec:59` | Maximum/Overflow (45 s to 60 s) | 50 s | ambiguous | "well inside" unbounded | GAP (F13) |
| G4 WC-1 startup timing | `spec:59` | Sentinel | N/A | N/A | no sentinel value in the guard | OK (reason) |
| G5 WC-10 wait split | `spec:68` | One/Minimal (1 s tool call) | 1 s | no split | rule not triggered | OK |
| G5 WC-10 wait split | `spec:68` | Boundary (exactly 5 min) | 300 s | no split ("longer than 5 minutes") | not split | OK |
| G5 WC-10 wait split | `spec:68` | Typical (4 min Bash wait) | 240 s | split not required | heartbeat between iterations | OK |
| G5 WC-10 wait split | `spec:68` | Maximum/Overflow (Agent call of 10 min) | 600 s | exempt (WC-7) | no heartbeat rule | GAP (F11) |
| G5 WC-10 wait split | `spec:68` | Zero/Empty | N/A | N/A | no wait | OK (reason) |
| G6 WC-12 fence | `spec:70` | Zero/Empty (check returns nothing) | empty | not fenced | `CAPS:67` | OK |
| G6 WC-12 fence | `spec:70` | Typical (`consumer_fenced`) | fenced | stop, no `worker_done` | as stated | OK |
| G6 WC-12 fence | `spec:70` | Legitimate Edge (fence after contract written) | fenced after contract | no `worker_done` | coordinator reads only after `worker_done` (`spec:73`) | OK |
| G7 task confidence | `spec:121` | Zero (0.00) | 0.00 | blocked | "below 0.70 resolves as blocked" | OK |
| G7 task confidence | `spec:121` | Boundary (0.70) | 0.70 | proceeds | not below 0.70 | OK |
| G7 task confidence | `spec:121` | Typical (0.85) | 0.85 | proceeds | band not stated for task (`INV-B:45`) | OK |
| G7 task confidence | `spec:121` | Sentinel | N/A | N/A | no sentinel value | OK (reason) |
| G8 cli-eval run | `spec:104` | Zero/Empty (no `--suite`) | none | blocked | as stated | OK |
| G8 cli-eval run | `spec:104` | One/Minimal (`--suite`, no safety flags) | one flag | undefined | "the safety flags" unnamed | GAP (F14) |
| G8 cli-eval run | `spec:104` | Typical (both present) | both | proceeds | as stated | OK |
| G8 cli-eval run | `spec:104` | Legitimate Edge (canonical source missing) | missing | STOP, blocked | 3.2 row | OK |
| G9 WC-9 outward flag | `spec:67` | Zero/Empty (no flag) | none | off | as stated | OK |
| G9 WC-9 outward flag | `spec:67` | Typical (flag with quoted user instruction) | flag | on | D4 (a) | OK |
| G9 WC-9 outward flag | `spec:67` | Sentinel (flag without authorization) | flag | on | enforcement is the coordinator's, D4 open | OK (D4 open) |
| G10 WC-3 ask or blocked | `spec:61` | Zero/Empty (no preamble) | no preamble | ask unavailable, blocked | WC-2 (c) | OK |
| G10 WC-3 ask or blocked | `spec:61` | Typical (preamble and gate) | preamble | ask | optional ("may") | GAP (F7) |
| G10 WC-3 ask or blocked | `spec:61` | Legitimate Edge (ask timeout) | timeout | resume same message ID | `CAPS:60` | OK |
| G11 7.2 step 2 agentWait | `spec:181` | Zero/Empty (field absent) | absent | pass | `CAPS:129`: absent means never looked | GAP (F19) |
| G11 7.2 step 2 agentWait | `spec:181` | Typical (null) | null | pass | as stated | OK |
| G11 7.2 step 2 agentWait | `spec:181` | Legitimate Edge (non-null during ask) | non-null | fail | UNVERIFIED whether ask sets it | GAP (F7) |

Pipeline Dimensional Analysis: not triggered. No stage in the spec changes an item count that a downstream consumer must reconcile. Per-command fan-out (E4, `spec:24`) is internal to commands and out of scope. No Quantity Flow Diagram is required.

## Whittaker attack findings (adversarial probing)

- F6 (Sequence Attack): stale contract, see above.
- Divergence Attack on WC-5 (`spec:63`): the boundary between `partial` and `succeeded` is the same boundary that makes dependents start (F4).
- Zero/Empty Attack on WC-4 (`spec:62`): a command that fails before writing any output (for example at the `--output` check) must write the contract with `status: failed`; the spec requires this (WC-4 "including stops before any other output exists") but gives no fallback when the contract write itself fails. Covered by F6's no-report branch.
- Sentinel Collision on `blocked` (`spec:63`): WC-5 maps `blocked` to `failed`, so the coordinator cannot tell a gate stop from a crash without reading the contract. The spec says this is intentional (WC-4 and 2.3). Not a finding.

## Checks that passed

- The Orca facts used in WC-1, WC-3, WC-5, WC-8, WC-10, D1, D5 and the UNVERIFIED list match the cited `CAPS:` lines.
- Section counts (10 / 27 / 6 = 43) match both inventories.
- The workflow row (`spec:92`) and the workflow fact that a contract is not written for pre-creation STOPs (`INV-B:272`) are consistent.
- The implement halt rule (D2) matches `INV-A:66` and `INV-A:81`.

## Decisions

Simple choices made for this review: the FIRST-REVIEW grading check was applied to every finding; blocking was given only where the sentence needed no added assumption (F1 to F3). Medium and minor findings were kept out of the Reviser brief.

## Findings block

```findings-v1
{"id": "F1", "severity": "MAJOR", "blocking": true, "category": "unpassable-check", "anchor": "steps 1-3 and 5-7 pass; step 4 uses the command's existing report file", "anchor2": "its report path is the WC-4 contract path", "refs": ["AC-0.4", "7.2 step 3", "WC-4", "3.1 troubleshoot"], "claim": "AC-0.4 requires step 3 to match a WC-4 contract path that troubleshoot does not write until P1, so the criterion cannot pass in P0."}
{"id": "F2", "severity": "MAJOR", "blocking": true, "category": "contradiction", "anchor": "In unattended mode the command writes `<output-dir>/return-contract.yaml`", "anchor2": "| load | no gate | none (see note) | n/a |", "refs": ["WC-4", "AC-1.1", "3.2 load", "2.2"], "claim": "The load row writes no contract, while WC-4 and AC-1.1 require every 3.2 command to write and name one, so AC-1.1 fails for load."}
{"id": "F3", "severity": "MAJOR", "blocking": true, "category": "contradiction", "anchor": "Fix the contract filename to `<output>/adversarial/return-contract.yaml` (P1)", "anchor2": "where `<output-dir>` is the directory the coordinator passed", "refs": ["WC-4", "3.1 adversarial", "AC-1.4"], "claim": "WC-4 puts the adversarial contract at the brief's output directory root, while the P1 row puts it under an adversarial subdirectory, so the coordinator reads a different path than the one the worker writes."}
{"id": "F4", "severity": "MAJOR", "blocking": false, "category": "missing-requirement", "anchor": "A partial run left a usable deliverable; `failed` would tell the coordinator the work is lost", "anchor2": "After `worker_done`, the coordinator opens the report file, then releases or reuses the worker", "refs": ["WC-5", "2.3"], "claim": "A partial run settles its Task as succeeded, so dependents may start on incomplete output before the coordinator reads the contract."}
{"id": "F5", "severity": "MAJOR", "blocking": false, "category": "missing-requirement", "anchor": "writes each run into a fresh output directory so a re-run starts clean", "anchor2": "the output directory, so the report path is known before dispatch", "refs": ["WC-4", "WC-6", "2.3"], "claim": "The spec does not say whether the command or the brief creates the fresh directory, so the contract path may not be known before dispatch."}
{"id": "F6", "severity": "MAJOR", "blocking": false, "category": "missing-requirement", "anchor": "or no report exists; `--outcome succeeded` otherwise", "anchor2": "The worker passes the contract path as `worker_done --report-path`", "refs": ["WC-4", "WC-5", "WC-6"], "claim": "A re-run that crashes before writing its contract leaves an earlier succeeded contract, which WC-5 reports as a success."}
{"id": "F7", "severity": "MAJOR", "blocking": false, "category": "missing-requirement", "anchor": "then re-invoke or resume the command with the answer as a flag", "anchor2": "Each gate resolves one of three ways", "refs": ["WC-2", "WC-3", "AC-2.2", "7.2 step 2"], "claim": "The optional ask route has no flag to carry free-text answers, and AC-2.2 expects a fixed outcome even though the route is optional."}
{"id": "F8", "severity": "MAJOR", "blocking": false, "category": "missing-requirement", "anchor": "so a command run by a worker has the same tools as a command a person runs", "anchor2": "No person-blocking step in unattended mode", "refs": ["E2", "WC-2", "WC-1"], "claim": "Tool-permission approval prompts are a person-blocking step that WC-2 does not cover, and the claim that workers have the same tools is not evidenced."}
{"id": "F9", "severity": "MAJOR", "blocking": false, "category": "missing-requirement", "anchor": "These run as workers now if the brief uses the stated flags", "anchor2": "the topic-only clarification and nested", "refs": ["3.1", "WC-2", "SA-2"], "claim": "Ready-today commands can still stop on /task questions that only the unattended mode resolves, so they are not ready as the heading states."}
{"id": "F10", "severity": "MAJOR", "blocking": false, "category": "missing-requirement", "anchor": "contract for both pipelines (today a chat table)", "anchor2": "`run` requires `--suite` and the safety flags in the brief, else blocked", "refs": ["WC-4", "WC-6", "WC-11", "2.3", "3.2 cli-eval"], "claim": "Several 3.2 commands have no output flag or fixed location, so the contract path is not known before dispatch and cli-eval's fresh-directory rule cannot hold."}
{"id": "F11", "severity": "MAJOR", "blocking": false, "category": "missing-requirement", "anchor": "A command step that blocks a single tool call for longer than 5 minutes", "anchor2": "A command's own Agent-tool fan-out stays as it is.", "refs": ["WC-10", "WC-7"], "claim": "A single Agent-tool call running longer than the heartbeat cadence has no split or heartbeat rule, so the coordinator may treat a working worker as stalled."}
{"id": "F12", "severity": "MAJOR", "blocking": false, "category": "other", "anchor": "(orchestration\\|worktree\\|terminal\\|agent)", "anchor2": "The only allowed mention of Orca in a changed command is as an example", "refs": ["AC-C1", "SA-2", "WC-8", "P0"], "claim": "The AC-C1 pattern uses an escaped pipe that grep -E reads as a literal, so it can pass after an Orca call is added, and it scans core files that SA-2 allows to mention Orca."}
{"id": "F13", "severity": "MINOR", "blocking": false, "category": "missing-requirement", "anchor": "Any such prompt must fall back on its own well inside the readiness limit", "anchor2": "passes with a 30 s fallback; above about 45 s it fails again", "refs": ["WC-1"], "claim": "The fallback bound is not a number, so two implementers can choose fallbacks that pass or fail the readiness limit."}
{"id": "F14", "severity": "MINOR", "blocking": false, "category": "missing-requirement", "anchor": "`run` requires `--suite` and the safety flags in the brief", "anchor2": "else blocked; the W0", "refs": ["3.2 cli-eval", "AC-2.2"], "claim": "The safety flags are never named, so the cli-eval gate cannot be implemented or tested."}
{"id": "F15", "severity": "MINOR", "blocking": false, "category": "missing-requirement", "anchor": "Explicit `--unattended` flag in the brief (recommended)", "anchor2": "Without `--unattended`, every prompt, approval gate", "refs": ["D1", "SA-1", "2.1"], "claim": "The spec gives no rule for combining --unattended with --interactive or for a token inside quoted content, so commands may disagree on the mode."}
{"id": "F16", "severity": "MINOR", "blocking": false, "category": "other", "anchor": "Orca does not check the file, so the coordinator opens it.", "anchor2": "Orca's handling of the file is UNVERIFIED", "refs": ["WC-4", "UNVERIFIED 3"], "claim": "The spec states as fact that Orca ignores the report file, which its own evidence marks unverified."}
{"id": "F17", "severity": "MINOR", "blocking": false, "category": "missing-requirement", "anchor": "installed to `~/.claude/WORKER-CONTRACT.md`", "anchor2": "proposed as `src/superclaude/core/WORKER-CONTRACT.md`", "refs": ["2.1", "AC-1.2"], "claim": "The live checks need the installed contract file, but the spec does not require superclaude install before them, so they fail in a bare dev checkout."}
{"id": "F18", "severity": "MINOR", "blocking": false, "category": "other", "anchor": "state that knowledge-base mode does not wait (whether it does is UNVERIFIED)", "anchor2": "whether it does is UNVERIFIED", "refs": ["3.2 index", "WC-2"], "claim": "The index row requires the command to state a fact the spec itself marks unverified."}
{"id": "F19", "severity": "MINOR", "blocking": false, "category": "other", "anchor": "`observation.agentWait` is never non-null", "anchor2": "Pass:** `observation.agentWait` is never non-null", "refs": ["7.2 step 2", "CAPS:129"], "claim": "The step 2 pass condition is met when the coordinator never looks at agentWait, because an absent field passes."}
```

## Reviser brief

Blocking finding ids: F1, F2, F3.

Restated rule (review bullet 6): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, and the bytes added and deleted per finding id. Medium and minor findings are not in this brief and are not to be edited.

## Summary for the coordinator

- Verdict: FAIL. Blocking: F1 (AC-0.4 P0 check), F2 (load row vs WC-4), F3 (adversarial contract path).
- Follow-up candidates (not blocking, for the user's once-per-loop question): F4 to F19.
- Reviewer model: claude-haiku-5-5. No edits were made to the candidate or any other file.

verdict: FAIL
