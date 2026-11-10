# Spec panel critique: orca-worker-contract-spec.md

review: 1 of 3

- Command: `/sc:spec-panel --mode critique --focus requirements,architecture` (first review, FIRST-REVIEW prompt of `~/.claude/rules/prompts/document_review_loop_prompts.md`)
- Candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`, sha256 `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d`
- Baseline: missing (first review). Prior report: missing (first review).
- Reviewer model: claude-haiku-5-5 (Haiku 5.5), one reviewer in this run. The FIRST-REVIEW prompt asks for three reviews and a MERGE by the coordinator; this file is one of those three reports. The MERGE and the VERIFY pass are the coordinator's steps and have not been run here.
- Panel for this focus: Wiegers (lead, requirements), Adzic, Cockburn; Fowler (lead, architecture), Nygard, Newman, Hohpe; Whittaker (active in every panel review).
- Citation conventions: `spec:N` = line N of the candidate. `INV-A:N`, `INV-B:N`, `CAPS:N` = lines of the three inventories under `.dev/orca-command-refactor/inventory/`, which I read in full. `README:N` = `.dev/orca-command-refactor/README.md`. `command.md:N` = the sandbox copy of the `/sc:spec-panel` definition. Anything that cites a file I could not open in this sandbox (`src/`, `.dev/evals/`, `.dev/codegraph-migration/`, `~/.claude/`) is marked UNVERIFIED.

## Coverage

- Read in full: the candidate (286 lines), `README.md`, `inventory/commands-a.md`, `inventory/commands-b.md`, `inventory/orca-capabilities.md`, `command.md`, and the FIRST-REVIEW prompt file.
- Checked by re-running a command: the AC-C1 grep pattern (F2), with a one-line probe file that I removed afterwards.
- Spot-checked against the inventories: the CAPS line citations in spec §1-§2 (for example `spec:44-45`, `spec:52`, `spec:58-61`, `spec:64`, `spec:66-67`, `spec:73-74`, `spec:79-80`, `spec:97-103`, `spec:107-113`, `spec:130`, `spec:145-149`, `spec:155-161`, `spec:178`, `spec:186-188`), and the INV-A/INV-B row citations (`spec:52` / `INV-A:35-55`, `INV-A:76-83`, `INV-B:292`, `INV-A:90`, `INV-B:285-286`, `INV-B:311`, `INV-B:323`, `INV-A:106`, `INV-B:320`, `INV-B:272`, `INV-B:301`). All of these matched the cited line. The spec's cited `src/`, `.dev/evals/` and `.dev/codegraph-migration/` files are not in this sandbox, so they are UNVERIFIED here.
- Section counts checked: 10 ready (§3.1 lists 10 rows), 27 needs-change (§3.2 lists 27 rows), 6 coordinator-only (§4 lists 6). Total 43, matching `spec:75`. The inventories' own summaries give 5+13+3 = 21 and 5+14+3 = 22, which sums to the same totals.

## Expert analysis

### === REQUIREMENTS ANALYSIS ===

**F1. WC-4 says the report path is known before dispatch, but two §3 rows make it unknown or unnamed. [BLOCKING]**
- Issue: WC-4 requires that in unattended mode the command writes `<output-dir>/return-contract.yaml`, where `<output-dir>` is passed by the coordinator (`spec:62`). §2.3 relies on this: the path "is known before dispatch" (`spec:73`). The §3.1 workflow row leaves the contract at `.dev/tasks/to-do/<id>/return-contract.yaml` (`spec:92`), and the P1 fix for workflow only adds pre-creation STOP contracts (`spec:92`, `spec:159`). The inventory says that package id is generated per run with "Fresh package each run" (`INV-B:52`, `INV-B:272`). The §3.2 research row names "contract naming the generated `claudedocs/research_*.md` path" and adds no output flag (`spec:116`; `INV-B:38` for the generated name). The cli-portify row says "file location unnamed" (`spec:105`; `INV-A:45`).
- Sentence that holds with no further assumption: an implementer who follows WC-4 and §2.3 has the coordinator pass `--output` and read `<output-dir>/return-contract.yaml`. An implementer who follows the workflow row keeps the contract at a per-run `<id>` path, so the file is not at the path the coordinator passed, and `worker_done --report-path` cannot be checked against WC-4.
- Expert attribution: Fowler (interface contract), Wiegers (traceability of the WC-4 rule to each row).
- Recommendation: either give workflow, research and cli-portify an `--output` (or `--output-dir`) flag that WC-4 can use, or write an explicit exception list in WC-4 with the path each one uses and how the coordinator learns it. Add an acceptance check that the path matches the brief for each §3.1 and §3.2 row.
- Priority: High. Quality impact: high (the coordinator cannot read the report for three commands as specified).

**F2. AC-C1 cannot fail on a real violation. [BLOCKING]**
- Issue: AC-C1 is the only mechanical check for SA-2 and WC-8. It uses `grep -rnE '\borca(-ide)?[[:space:]]+(orchestration\|worktree\|terminal\|agent)\b'` (`spec:172`). In an ERE, `\|` is a literal bar, not alternation, so the group only matches the text `orchestration|worktree|terminal|agent`.
- Checked: on a one-line probe file containing `orca orchestration task-create`, the spec's pattern printed nothing and exited 1. The same pattern with an unescaped `|` matched the line (exit 0). So AC-C1 passes on a tree that calls Orca from a command.
- Sentence that holds with no further assumption: an implementer who runs AC-C1 as written, on a command file that contains `orca orchestration worker-start`, gets empty output and records a PASS, so SA-2 and WC-8 are not enforced.
- Expert attribution: Wiegers (acceptance criteria must be testable), Adzic (executable checks).
- Recommendation: change the group to `(orchestration|worktree|terminal|agent)` with `-E`, or use `grep -rnE '\borca(-ide)?[[:space:]]+(orchestration|worktree|terminal|agent)\b'`. Add a negative fixture that the check must flag, so the check is proven to fail once.
- Priority: High. Quality impact: high (the gate that enforces the no-Orca rule passes whatever the commands say).

**F3. A retry can overwrite or misread the first attempt's contract. [BLOCKING]**
- Issue: WC-3 lets a worker re-invoke or resume the command after an answer (`spec:61`). WC-6 says a re-run "writes each run into a fresh output directory" when the command has no resume flag (`spec:64`). §2.3 lists what the coordinator owes each brief and does not include a fresh output directory on retry (`spec:73`). The contract has no field that binds it to a dispatch or Task (`spec:62` lists `status`, `command`, `report_path`, `artifacts`, `blocked_question`). WC-5 maps "no report exists" to `failed` (`spec:63`).
- Sentence that holds with no further assumption: an implementer who follows §2.3 passes the same `--output` on a retry. A retry that crashes before writing its own contract leaves attempt 1's `return-contract.yaml` in that directory (for example `status: succeeded`). WC-5 treats it as the report and maps it to `succeeded`, so a failed retry is recorded as a success and the first attempt's output is overwritten.
- Whittaker (FR-2.4 Sequence Attack): I can break this specification by **re-running after an ask timeout**. The invariant at **spec:61 (WC-3) and spec:64 (WC-6)** fails when **the re-run uses the same output directory and the command has no resume flag**. Concrete attack: **attempt 1 writes `status: succeeded` to `D/return-contract.yaml`; attempt 2 is re-invoked with `--output D` and crashes before writing; WC-5 reads the file from attempt 1 and sends `worker_done --outcome succeeded`; `D` now holds attempt 2's partial files over attempt 1's.**
- Expert attribution: Nygard (failure modes and recovery), Newman (contract binding across service evolution), Whittaker (sequence attack).
- Recommendation: state in §2.3 that a retry brief gets a new output directory (or a timestamped subdirectory the command creates), and that the contract is removed or renamed before a run starts. Add `dispatch_id` (or `task_id`) to the WC-4 field list and make WC-5 ignore a contract whose id does not match the preamble.
- Priority: High. Quality impact: high (data loss and a false success).

**F4. The spec-panel row conflicts with the command definition on `--output`. [BLOCKING]**
- Issue: WC-4 treats `--output` as a directory flag (`spec:62`). The §3.2 spec-panel row says "add `--output`; contract" and "`target_release` required as a flag" (`spec:120`). The command definition already has `--output <file>`, `--unattended`, `--report-dir <dir>` and `--target-release` in its usage line (`command.md:23`), accepts `--target-release` in any run (`command.md:37`), and says `--report-dir <dir>` is the report directory and "`--output` is file-valued" (`command.md:459-460`). The inventory row this spec relies on says spec-panel has no `--output` (`INV-B:43`, citing `cmd/spec-panel.md:22`, UNVERIFIED here, because that file is not in this sandbox).
- Sentence that holds with no further assumption: an implementer who follows WC-4 gives spec-panel `--output <dir>`, and `--output` then means a directory in one place and a file in the command definition (`command.md:23`, `:460`). The contract is written to the wrong place or the file is written into a directory.
- Expert attribution: Wiegers (requirement conflicts), Fowler (interface consistency).
- Recommendation: rename the WC-4 flag to the one each command uses, or add a per-command flag table (for spec-panel: `--report-dir`). Correct the spec-panel row (`spec:120`) to say that `--target-release` and `--unattended` already exist and that the change is only the contract. Re-check the other §3.2 rows against their current command files before P1.
- Priority: High. Quality impact: high (wrong directory or overwritten file for a command already in use).

### === ARCHITECTURE ANALYSIS ===

**F5. (Medium) WC-10 cannot be met during Agent-tool waits.**
- Issue: WC-10 requires a heartbeat every 5 minutes and splits only "a command step that blocks a single tool call" (`spec:68`). Fan-out commands wait on Agent-tool (Task) calls that can run for many minutes (`INV-A:14`; `INV-A:42`, `INV-B:46`), and the spec does not split those. The consequence depends on whether Orca uses heartbeat age in the liveness verdict, which is UNVERIFIED (`CAPS:130`).
- Expert attribution: Nygard, Hightower (not in this focus, noted only).
- Recommendation: state that a command with Agent-tool fan-out must return to the top level between calls, or that its fan-out is split into Orca Tasks (§1.3 already says so), or verify the Orca liveness rule before P2.
- Priority: Medium. Quality impact: medium.

**F6. (Medium) WC-9 is written as final while open decision D4 is unresolved.**
- Issue: WC-9 says an outward action turns on "only through the command's own explicit flag written in the brief" (`spec:67`). D4 recommends a stricter rule: the flag is honoured only when the user's own instruction names the action (`spec:245`). The two cannot both be implemented; WC-9 as written would need an edit if D4 is answered (a).
- Expert attribution: Wiegers (requirement stated in two forms), Cockburn (the actor who authorizes).
- Recommendation: write WC-9 with a placeholder that points to D4, or state the rule with "pending D4".
- Priority: Medium. Quality impact: medium.

**F7. (Medium) Flag and mode inconsistency between §2.3 and §3.1.**
- Issue: §2.3 says each brief carries "the exact command line including `--unattended`" (`spec:73`). The §3.1 "ready today" rows say the brief "must pass" only the listed flags, with no `--unattended` (`spec:83-92`). P0 runs three of them with no `--unattended` (`spec:158`, `spec:194`). Both can be followed, but the spec does not say which runs are unattended.
- Expert attribution: Cockburn (actors and preconditions), Wiegers.
- Recommendation: state that §3.1 rows are standalone-ready, and that unattended use requires `--unattended` and the flags listed in §3.2.
- Priority: Medium. Quality impact: medium.

**F8. (Medium) No rule for a missing output directory under `--unattended`.**
- Issue: WC-4 says the contract is written "on every outcome, including stops before any other output exists" (`spec:62`), but the spec gives no rule for a run started with `--unattended` and no output directory. The command definition refuses such a run before any work and prints the refusal in chat (`command.md:459-460`), so the rule exists in one place and not in the spec.
- Expert attribution: Wiegers, Nygard.
- Recommendation: add to WC-2 or WC-4 a fourth resolution for a missing output directory, which is "refuse before work, print in chat" (the command.md behaviour), and list it in each §3 row.
- Priority: Medium. Quality impact: medium.

**F9. (Medium) Sentinel collision: how `--unattended` is detected.**
- Issue: §2.1 defines unattended mode as "the behaviour a command switches to when its caller passes `--unattended`" (`spec:51`), and D1 recommends the flag (`spec:228`). The spec does not say whether `--unattended` inside quoted specification content, a quoted brief or a pasted document counts. The command definition does: it counts only when `--unattended` is a standalone token outside any quoted argument (`command.md:459`).
- Whittaker (FR-2.3 Sentinel Collision Attack): I can break this specification by **a quoted spec that mentions the flag**. The invariant at **spec:51 and spec:228 (D1)** fails when **the flag text appears inside quoted content**. Concrete attack: **`/sc:spec-panel "Document the --unattended flag for workers" --mode critique`: a token-blind detector switches to unattended mode, skips the gates and writes a contract the person did not ask for.**
- Expert attribution: Whittaker, Wiegers.
- Recommendation: adopt the command.md token rule in WC-2 (or state it in §2.1) and add a fixture with the flag inside quotes.
- Priority: Medium. Quality impact: medium.

**F10. (Medium) The contract outcome rules leave some statuses unmapped.**
- Issue: WC-5 defines four cases: `failed`/`blocked` maps to failed, no report maps to failed, and everything else maps to succeeded (`spec:63`). The rule does not say what happens to a 0-byte file, an unknown `status` value, or a file with `status: succeeded` and a non-empty `blocked_question`. The last one can drop a blocked gate silently.
- Whittaker (FR-2.1 Zero/Empty; FR-2.3 Sentinel): I can break this specification by **a contract with a question but a success status**. The invariant at **spec:63 (WC-5)** fails when **`blocked_question` is set and `status` is not `blocked`**. Concrete attack: **a command writes `status: partial` with `blocked_question: "overwrite?"`, WC-5 maps it to `succeeded`, and the coordinator starts the dependent Task.**
- Expert attribution: Whittaker, Wiegers.
- Recommendation: make WC-5 total: unknown status, empty file and a question with a non-blocked status each map to `failed` (or are rejected by a validator step in 7.2).
- Priority: Medium. Quality impact: medium.

**F11. (Medium) `partial` maps to `succeeded`, and nothing stops dependents from starting.**
- Issue: the decision says a partial run is `succeeded` because "a partial run left a usable deliverable" (`spec:263`). Ready Tasks are the ones whose dependencies have settled (`CAPS:86`), and Orca does not start them itself (`CAPS:92`), so the coordinator decides when a dependent starts. §2.3 does not tell the coordinator to read `status` before starting a dependent. A dependent such as `/sc:implement` can therefore run on partial output.
- Expert attribution: Fowler (dependency semantics), Hohpe (message semantics).
- Recommendation: add to §2.3 that dependents start only when the contract `status` is `succeeded`, or add a `partial` gate for each Task that depends on a partial worker.
- Priority: Medium. Quality impact: medium.

**F12. (Medium) `--output` / `--output-dir` naming is not uniform across the commands in §3.**
- Issue: WC-4 says the coordinator passes `--output` or `--output-dir` (`spec:62`). The inventories name `--output-dir` for auggie-review and pr-submit (`INV-A:38`, `INV-B:92`), `--output <dir>` for adversarial and brainstorm (`spec:83-84`), a fixed `.claude-audit/` for cleanup-audit (`spec:85`), and the command definition uses `--report-dir` (`command.md:459`). A single brief template (P0, `spec:158`) cannot be written until one name or a table is chosen.
- Expert attribution: Fowler.
- Recommendation: choose one flag name for the contract directory, and map each existing name to it in §3.
- Priority: Medium. Quality impact: medium.

**F13. (Medium) The tasklist fan-out depth is stated wrongly.**
- Issue: `spec:122` says the reflect fan-out "runs one layer below the worker, inside Claude Code's nesting limit, `INV-A:14`". INV-A:14 states the three-layer limit and does not mention tasklist. The inventory for tasklist says that Stage 10.5 runs N subagents, each of which runs `/sc:reflect` and spawns its own agents, which is subagent-to-agent nesting (`INV-B:46`, `INV-B:210`, UNVERIFIED whether it works). That is two layers below the worker, not one.
- Expert attribution: Newman (service boundaries and depth), Fowler.
- Recommendation: correct the claim to two layers and make tasklist's Stage 10.5 a P2 item with a check that nested reflect reaches its agents, or move reflect out of the subagent.
- Priority: Medium. Quality impact: medium.

**F14. (Medium) Counts and the verdict for `/sc:pr-submit` disagree.**
- Issue: the §3.2 table lists pr-submit as needs-change with a P4 phase (`spec:114`, `spec:162`), and the counts in `spec:75` include it in the 27. The D3 recommendation is that pr-submit is not a worker at all (`spec:240`), and §4 says six commands are never dispatched and that pr-submit is a worker candidate only if D3 is (b) (`spec:139`).
- Expert attribution: Cockburn (the outcome of each row), Wiegers.
- Recommendation: mark pr-submit as "needs-change if D3 (b), otherwise coordinator-only" in §3.2 and in the counts.
- Priority: Medium. Quality impact: low.

**F15. (Medium) The depth-1 refusal is stated as fact in §1.3 R1.**
- Issue: R1 says a command that calls `worker-start` "would be refused" with `nested_worker_depth_exceeded` (`spec:33`). The same row says which call sites enforce the check were not traced, and the capabilities file marks it UNVERIFIED (`CAPS:103`). The other reasons for rejecting the alternative (R2, R3, R5) do not depend on this.
- Expert attribution: Fowler.
- Recommendation: move "would be refused" to the UNVERIFIED list (item 5 at `spec:276` already covers it) and keep R2, R3 and R5 as the grounds.
- Priority: Medium. Quality impact: low.

**F16. (Medium) WC-2 says gates resolve "one of three ways", and WC-3 adds a fourth path.**
- Issue: WC-2 lists three resolutions (`spec:60`). WC-3 allows a worker to ask the coordinator and then re-invoke the command with the answer as a flag (`spec:61`). The answer path is in fact resolution (b) after a wait, but the text does not say so, and WC-6 then applies to the re-invoke.
- Expert attribution: Wiegers.
- Recommendation: state in WC-3 that the answer path is resolution (b), so WC-2 stays exhaustive.
- Priority: Medium. Quality impact: low.

**F17. (Medium) The Ruling in D2 and the implement row are not in the same state.**
- Issue: the §3.2 implement row says the halt path is "contract blocked, carrying the Ruling question" (`spec:109`), while D2 (a) says the worker "ends `failed`" (`spec:234`). WC-5 maps `blocked` to `failed` (`spec:63`), so both are consistent, but the row does not say that the coordinator then has no `ask` answer to use.
- Expert attribution: Wiegers.
- Recommendation: align the row with D2 (a) wording.
- Priority: Medium. Quality impact: low.

**Follow-up candidates (Medium and minor, not blocking):** F5 to F17 above. Minor notes: the spec-panel evidence row `INV-B:43` is UNVERIFIED here (see F4); the `src/`, `.dev/evals/` and `~/.claude/` citations in §1, §2.1 and §7 are UNVERIFIED because those files are outside this sandbox; `spec:52` cites `install_core.py:4,33` and `KNOWN_CORE_FILES` lines, UNVERIFIED here.

## Guard Condition Boundary Table (mandatory; the spec contains conditional logic)

Trigger: WC-2, WC-3, WC-4, WC-5, WC-6, WC-9, WC-10, WC-12 and SA-3 contain guards. Table is complete for the guards enumerated; classes that cannot occur for a guard are left out with a reason under the table.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|-------|----------|-----------------|----------------|--------------|-------------------|--------|
| WC-5 outcome | spec:63 | Zero/Empty | no `return-contract.yaml`, or a 0-byte file | no report: true; empty file: unspecified | "no report exists" maps to failed; an empty file is not addressed | GAP (F10, Medium) |
| WC-5 outcome | spec:63 | One/Minimal | `status: succeeded`, no `blocked_question` | succeeded | `--outcome succeeded` | OK |
| WC-5 outcome | spec:63 | Typical | `status: partial` | partial | succeeded (spec:263); no dependent-start rule in spec:73 | GAP (F11, Medium) |
| WC-5 outcome | spec:63 | Maximum/Overflow (unknown value) | `status: ok` | not in the four-value set | none stated | GAP (F10, Medium) |
| WC-5 outcome | spec:63 | Sentinel Value Match | `status: succeeded` with non-empty `blocked_question` | both set | none stated; the question is dropped | GAP (F10, Medium) |
| WC-2 (c) gate | spec:60 | Zero/Empty | required flag absent or empty | gate: true | blocked, with the question in the contract | OK |
| WC-4 directory | spec:62 | Zero/Empty | `--unattended` with no output directory | contract path undefined | none stated; command.md:459-460 refuses before work | GAP (F8, Medium) |
| WC-6 retry | spec:64 | Typical | retry with the same `<output-dir>` as attempt 1 | directory non-empty: true | "fresh output directory" required; no step creates it | GAP (F3, blocking) |
| WC-6 resume | spec:64 | Legitimate Edge Case | resume flag given to a command with no resume flag (research, save) | no resume flag | unspecified | GAP (F1, blocking; research row) |
| WC-9 outward | spec:67 | Sentinel Value Match | the flag text inside quoted content | token vs quote: unspecified | no token rule in spec; command.md:459 has one | GAP (F9, Medium) |
| WC-9 outward | spec:67 | Legitimate Edge Case | user asks for a push but the brief does not quote it | authorization source open | WC-9 uses the brief flag; D4 requires the user's words | GAP (F6, Medium) |
| WC-10 wait | spec:68 | Maximum/Overflow | one Agent-tool call longer than 5 minutes | heartbeat due: true | only Bash waits are split | GAP (F5, Medium) |
| WC-10 wait | spec:68 | Typical | Bash wait split to 4 minutes | below 5 minutes | OK | OK |
| WC-3 ask timeout | spec:61 | Zero/Empty | ask times out with no answer | pending: true | resume the same message ID; default timeout UNVERIFIED (CAPS:68) | GAP (minor, UNVERIFIED) |
| WC-12 check | spec:70 | Zero/Empty | `check` returns no rows | fenced: false | continue | OK |
| WC-12 check | spec:70 | Typical | `check` returns `consumer_fenced` | fenced: true | stop without `worker_done` | OK |
| SA-3 standalone | spec:148 | Typical | plain run, no flag | unattended: false | no contract written | OK |
| SA-3 standalone | spec:148 | Legitimate Edge Case | output flag only, no `--unattended` | output: true | contract written, as SA-3 allows | OK |

Left out, with the reason: WC-12 Maximum (the check has no count), WC-3 Maximum (the timeout is a single value), WC-10 Zero (a zero-length wait is not a wait), SA-3 Maximum (no count is involved).

## Whittaker findings (adversarial; FR-2 methodologies)

- FR-2.4 Sequence: F3 (retry into an existing directory; stale contract).
- FR-2.3 Sentinel: F9 (`--unattended` inside quoted content).
- FR-2.1 Zero/Empty: F10 (empty contract, unknown status).
- FR-2.2 Divergence: WC-2 and WC-3 meet at the answer path (F16). Under the boundary between "ask" and "blocked", the spec says both (`spec:60`, `spec:61`).
- FR-2.5 Accumulation: WC-11 says "two workers in one worktree must never write the same file" (`spec:69`), but a per-session memory key written by each of two workers in one `.superclaude/memory/` is not bounded by any rule. UNVERIFIED consequence; recorded as a note only.

## Pipeline Dimensional Analysis

Not triggered. The spec describes a fan-out of Tasks and one contract per worker, and no stage changes an item count (no filter, aggregation or dedup stage). No Quantity Flow Diagram is required.

## Decisions (this reviewer's)

| Decision | Options | Rationale |
|---|---|---|
| Blocking threshold | Grade all MAJOR as blocking; grade by the sentence test in the prompt | Sentence test. F1 to F4 each pass it with no further assumption; the other MAJOR-labelled points need a guess and are Medium. |
| AC-C1 severity | Note only; blocking | Blocking under the sentence test: the check prints nothing on a violation I wrote to a probe file (F2), so the SA-2 and WC-8 gate cannot fail. The prompt's example ("cannot pass") is the mirror case, but the test reaches the same outcome with no further assumption. |
| Inventory baseline for spec-panel | Trust `INV-B:43`; trust the sandbox `command.md` | Trust the command file in this sandbox, which the brief names as the command definition, and mark the inventory row UNVERIFIED. |

## Verdict summary

- Blocking: F1, F2, F3, F4 (four open blocking findings).
- Medium: F5 to F17 (follow-up candidates; not in the Reviser brief).
- The VERIFY prompt is for the coordinator. These findings are unconfirmed until a fresh verifier checks them.

Reviser brief (blocking finding ids only; restates bullet 6 of the command): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, and the bytes added and deleted per finding id.
- F1: WC-4 (`spec:62`), §2.3 (`spec:73`), workflow row (`spec:92`), research row (`spec:116`), cli-portify row (`spec:105`).
- F2: AC-C1 pattern (`spec:172`).
- F3: WC-3 (`spec:61`), WC-5 (`spec:63`), WC-6 (`spec:64`), §2.3 (`spec:73`).
- F4: WC-4 `--output` (`spec:62`), spec-panel row (`spec:120`).

verdict: FAIL
