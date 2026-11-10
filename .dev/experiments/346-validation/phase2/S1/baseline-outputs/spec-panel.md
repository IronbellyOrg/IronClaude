# Spec panel review: Orca worker contract spec

Task: task_e2ba133e6cbd (Task 5, independent review). Planning only.
Command: `/sc:spec-panel @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture`
Spec under review: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (cited below as `SPEC:N`). The spec was not edited.

## Verdict
**FAIL.** 24 findings: 3 CRITICAL, 15 MAJOR, 6 MINOR (section 6). The core decision (Orca on top, commands stay Orca-free units of work) holds up and no expert disputed it. The spec fails on its failure paths and its acceptance checks:
- A blocked or failed Task cannot be retried with a new brief in Orca, so the blocked → answer → retry flow and the "fresh output directory" rule cannot work as written (finding 1).
- The new report `status` values clash with the values existing `return-contract.yaml` files already use, so a successful run fails check 7.2 step 4 (finding 2).
- The fan-out-then-merge pattern has no rule for blocked or partial inputs (finding 3).
- Several acceptance checks pass or fail for the wrong reason, two of them shown by running them (findings 5, 6, 7, 10, 14).

## 1. Panel setup
- **Input type.** Not a TDD (9 numbered `## N.` headings, no `parent_doc`/`coordinator` frontmatter, no "Technical Design Document" text: `SPEC:1-13`) and not a PRD (no personas, JTBD or PRD headings). Steps 6a-6d do not apply.
- **Mode.** Critique: each finding has severity, expert, recommendation, priority and evidence.
- **Focus.** Requirements (Wiegers lead, Adzic, Cockburn) and architecture (Fowler lead, Newman, Hohpe, Nygard). Whittaker reviews in every panel.
- **Mandatory artifacts triggered.** The Guard Condition Boundary Table is required because the spec has conditional rules (outcome mapping `SPEC:63`, `--unattended` branch `SPEC:60`, 4-minute wait limit `SPEC:68`, retry branch `SPEC:64`). Pipeline Dimensional Analysis is triggered by the fan-out-then-merge pattern at `SPEC:39`.
- **Auto-suggestion (advisory).** A later `--focus correctness` pass is recommended: the spec has numeric guards (60 s `SPEC:59`, 5 min / 4 min `SPEC:68`, depth 1 `SPEC:33`) and a fan-out/merge flow (`SPEC:39`).
- **Step 6 "Improve" not run.** The brief forbids editing the spec, and the command's own boundary is "Modify specifications without explicit user consent" (Will Not). Recommendations below are for Task 6.
- **Method.** Every finding was checked against the live file, the repo, or read-only `orca-ide ... --help` output on 2026-11-02 (CLI `1.4.237`, same as `CAPS:8`). Two regex checks were run with sample input to show the defect, not just inferred.

## 2. Requirements analysis
=== REQUIREMENTS ANALYSIS ===

**Karl Wiegers (requirements quality).** The requirement set (WC-1 to WC-12, SA-1 to SA-6) is clearly worded and almost every row carries evidence. The weak point is traceability from requirement to acceptance check. WC-1 (`SPEC:59`) has only 7.2 step 1, which never exercises a launch-path prompt. WC-6 retry (`SPEC:64`) has no check at all, WC-12 (`SPEC:70`) has none, and WC-11 (`SPEC:69`) is checked only for `/sc:save` (`SPEC:207`). Two requirements cannot be satisfied as written: WC-4's "known before dispatch" contract location fails for several commands (finding 4), and WC-4's status set collides with the status field the existing contracts already use (finding 2). "How would you validate WC-6 in production? Today you cannot: no AC drives a `--retry-of` run."

**Gojko Adzic (specification by example).** The spec gives good command-line examples (`SPEC:228`, `SPEC:194`, `SPEC:200`). It lacks a worked example of the most important new flow: gate hit → blocked contract → coordinator answer → retry with the answer. When that example is written against Orca's real verbs, it fails (finding 1). AC-2.2 (`SPEC:200`) is not deterministic because WC-3 says the worker "may" ask instead of blocking (`SPEC:61`), so the same input can end `failed/blocked` or `succeeded` (finding 11).

**Alistair Cockburn (actors and goals).** Three actors are named: command, worker session, coordinator (`SPEC:57-73`). The person who answers a blocked question is a fourth actor and appears only in D2 (`SPEC:232-236`). The coordinator's goal "dispatch work and read a report" holds, but its failure scenarios (blocked, partial, retry exhausted) are not written as use-case extensions; section 2.3 (`SPEC:72-73`) covers only the success path. The spec also does not say what the coordinator does with a `partial` result before dependent Tasks start (finding 13).

## 3. Architecture analysis
=== ARCHITECTURE ANALYSIS ===

**Martin Fowler (interfaces and boundaries).** The central boundary is sound and well argued: the coordinator orchestrates and commands stay Orca-free (`SPEC:16`, `SPEC:28-37`), and it is backed by real limits (depth 1 at `CAPS:97-98`; `worker_done` bound to the pane at `CAPS:76`). Three interface problems:
1. The report contract (WC-4) reuses the filename `return-contract.yaml` but redefines its `status` values. Existing producers write `success | partial | failed` (`src/superclaude/skills/sc-workflow-protocol/refs/return-contract.md:7`; `src/superclaude/skills/sc-adversarial-protocol/SKILL.md:436`), and reflect also uses `stopped-precondition` (`src/superclaude/skills/sc-reflect-protocol/SKILL.md:250`). WC-4 requires `succeeded` while saying existing commands "keep their fields" (`SPEC:62`), and check 7.2 step 4 asserts the new values (`SPEC:183`). That is one field name with two meanings (finding 2).
2. The rules for the worker session (heartbeat, ask, check, worker_done: WC-3, WC-5, WC-10, WC-12) are written into an IronClaude core file (`SPEC:52`), but the Orca preamble already defines them for each dispatch (`CAPS:130`: cadence comes from the preamble). That gives two sources of truth tied to one Orca version (finding 19).
3. The contract file and the new Orca section in the routing guide live in `src/superclaude/core/` (`SPEC:52`, `SPEC:158`), and AC-C1 scans exactly that folder for `orca orchestration` (`SPEC:172`). The phase's own deliverable trips the phase's own check (finding 5).

**Sam Newman (evolution).** WC-4 sets no schema version, but workflow's contract already carries `contract_version: "1.1"` (`src/superclaude/skills/sc-workflow-protocol/refs/return-contract.md:6`). A coordinator reading contracts across phases P1-P4 cannot tell which field set to expect (finding 22). Rollout order by risk (`SPEC:156-162`) is good. But P1 makes every command accept `--unattended` before its gates are converted in P2-P4 (`SPEC:159`), so for those phases the flag promises behaviour the command does not have (finding 9).

**Gregor Hohpe (integration and messages).** The message exchange is a pointer (`--report-path`) plus a 3-sentence body, with Orca not reading the file (`CAPS:79`). That is a clean claim-check pattern. Two gaps:
- **Retry carries no new data.** `worker-start --retry-of` needs `--task` naming the failed Task (`orca-ide orchestration worker-start --help`, output line 47), and `task-update` can change only `--status` and `--result` (`orca-ide orchestration task-update --help`, output line 3). The Task spec (the brief) cannot change on retry, so WC-3's "re-invoke ... with the answer as a flag" and WC-6's "fresh output directory" have no channel except a follow-up `send --to dispatch:<id>` (`CAPS:66`), which the spec never mentions (finding 1).
- **Partial results release dependents.** `partial` maps to `succeeded` (`SPEC:63`, `SPEC:263`), and a valid `worker_done` settles the Task (`CAPS:77`), so dependent Tasks become ready (`CAPS:86-90`) on a partial deliverable without anyone checking it (finding 13).

**Michael Nygard (failure modes).** Detection of a silent stall is the weakest part. 7.2 step 2 relies only on `agentWait` sampled once per 5 minutes (`SPEC:181`), but the spec's own main stall case is a command ending its turn on a chat question (`SPEC:44`). Orca's stated positive proof of a stall is "a transcript whose final agent turn sent no `worker_done`" (`CAPS:126`). Whether `agentWait` is set for a turn that ended on a chat question is UNVERIFIED (finding 16). WC-10's liveness rule covers poll waits but not Agent-tool fan-out, which WC-7 keeps unchanged (`SPEC:65`) and which can hold the session for longer than 5 minutes with no way to heartbeat (finding 8). No per-command time budget exists, and Orca's Dispatch time limit is UNVERIFIED (`SPEC:282`).

## 4. Adversarial analysis (Whittaker)
=== ADVERSARIAL ANALYSIS ===

**A1. Sequence attack (CRITICAL, finding 1).** I can break this specification by **Sequence Attack**. The invariant at **WC-6 / WC-3 (`SPEC:61`, `SPEC:64`)** fails when **the coordinator retries a blocked or failed Task**. Concrete attack: (1) Task T has brief `/sc:tdd "auth" --unattended --output .dev/tdd/auth.md`. (2) The worker hits the topic-only gate and writes `status: blocked` (`SPEC:90`), outcome `failed`. (3) The coordinator gets the person's answer and runs `worker-start --task T --retry-of <dispatch>`; Orca requires the same Task (`worker-start --help` line 47), whose spec cannot be edited (`task-update --help` line 3). (4) The retry worker receives the same brief: no answer flag, same output path. State after: the same gate fires again and the first attempt's contract is overwritten. A Task can never get past a blocked gate by retry, and it hits the 3-failure circuit breaker only through start failures (`CAPS:80`), so the loop is bounded only by the coordinator's patience.

**A2. Divergence attack (CRITICAL, finding 2).** I can break this specification by **Divergence Attack**. The invariant at **WC-4 status set (`SPEC:62`) and 7.2 step 4 (`SPEC:183`)** fails when **a command that already writes a contract keeps its field, as WC-4 requires**. Concrete attack: `/sc:workflow ... --handoff none` succeeds and writes `status: success` (`src/superclaude/skills/sc-workflow-protocol/refs/return-contract.md:7,27`). Step 4 asserts `d['status'] in {'succeeded','partial','failed','blocked'}` → `AssertionError`. WC-5 (`SPEC:63`) has no rule for `success`, so the worker's outcome is undefined. Before: run succeeded. After: the check reports failure, or the worker guesses.

**A3. Zero/empty attack (MAJOR, finding 12).** I can break this specification by **Zero/Empty Attack**. The invariant at **WC-2 (c) and WC-4 (`SPEC:60`, `SPEC:62`)** fails when **the brief passes `--unattended` but no `--output`**. Concrete attack: `/sc:analyze src/ --unattended`. `analyze` gets an output flag only in P1 (`SPEC:99`) and the spec makes no flag mandatory. The blocked rule says "write its report with `status: blocked`", but `<output-dir>` is empty, so there is no contract path. Result: the command either invents a path (breaking "known before dispatch") or writes nothing (WC-5 then says `failed` with no reason).

**A4. Sentinel collision attack (MAJOR, finding 17).** I can break this specification by **Sentinel Collision Attack**. The invariant at **D1 (a) "cannot misfire on a person" (`SPEC:228`)** fails when **the literal text `--unattended` appears inside a quoted argument**. Concrete attack: a person runs `/sc:troubleshoot "the worker ignores --unattended"`. Commands are prompt text read by the model, and the spec gives no rule that only a token outside quotes counts. If the model treats it as the flag, prompts and outward defaults silently change for a person (SA-1, `SPEC:146`).

**A5. Accumulation attack (MAJOR, finding 8).** I can break this specification by **Accumulation Attack**. The invariant at **WC-10 (`SPEC:68`)** fails when **a command's own Agent-tool fan-out runs longer than 5 minutes**. Concrete attack: `/sc:troubleshoot` escalates to Tier 2, where "2-4 specialist agents fan out in parallel" at a cost of "+4-15 min" (`src/superclaude/commands/troubleshoot.md:76`); WC-7 keeps that fan-out unchanged (`SPEC:65`). The top-level session is waiting on subagents and cannot run the heartbeat Bash call. The spec bounds only "a poll wait, a long eval". Heartbeat gaps grow with fan-out size and are not bounded anywhere.

**A6. Divergence attack on flags (MAJOR, finding 18).** I can break this specification by **Divergence Attack**. The invariant at **section 3.1 "never `--interactive`" (`SPEC:83-84`, `SPEC:89`)** fails when **a brief carries both `--unattended` and `--interactive`**. Cleanup, improve, roadmap, explain and business-panel say "refused" (`SPEC:102-103`, `SPEC:108`, `SPEC:110`, `SPEC:118`); adversarial, brainstorm and release-split rely only on the brief author. Which flag wins is unspecified for them.

### Pipeline dimensional analysis (Fowler + Whittaker)
The only multi-stage data flow is the coordinator pattern at `SPEC:39`: N `/sc:troubleshoot` workers, then one `/sc:adversarial` worker on their reports.

```text
[Coordinator: N troubleshoot Tasks] --> [N workers settle]
        |                                    |
        |            outcome split per WC-5 (SPEC:63):
        |            S succeeded (incl. partial), F failed/blocked;  S + F = N
        v                                    v
[adversarial Task, --deps on all N]  <-- starts only when every dep completed (CAPS:88-90)
        |
        +-- if F > 0: stays blocked until each failed Task is retried to success;
        |             retry repeats the same brief (finding 1) -> may never unblock
        +-- if F = 0 but P of S are partial: consumes S reports, P of them partial,
                      with no check (finding 13)                        <-- MISMATCH
[Consumer: /sc:adversarial expects 2-10 existing files]  (src/superclaude/commands/adversarial.md:15,39)
```

Consistency check: the spec assumes all N reports reach the merge step as complete deliverables. With N = 3, one `blocked` and one `partial`: the merge Task is blocked indefinitely, or, if the coordinator drops the blocked Task's dependency, it merges 2 artifacts of which 1 is partial. The spec defines neither path. Under FR-19 this is CRITICAL (finding 3). The command-count flow itself is conserved: 44 files in `src/superclaude/commands/` minus `README.md` = 43 = 10 + 27 + 6 (`SPEC:76`; rows at `SPEC:83-92`, `SPEC:99-125`, `SPEC:132-137`).

## 5. Guard condition boundary table
Nygard built it, Crispin checked it for completeness, Whittaker attacked the entries. Every GAP row maps to a finding of MAJOR or higher (FR-8). All cells are filled, so synthesis is not blocked (FR-10).

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| G1 `--unattended` present | `SPEC:51,60` | Zero/Empty | flag absent | false | Today's behaviour, every prompt kept (SA-1, `SPEC:146`) | OK |
| G1 | `SPEC:60,62` | One/Minimal | `--unattended` with no `--output` | true | Blocked contract must be written to an output dir that was not given; unspecified | GAP (finding 12) |
| G1 | `SPEC:60` | Typical | `--unattended --output <dir>` + required flags | true | Gates resolve per section 3 rows | OK |
| G1 | `SPEC:83-89`, `SPEC:102-118` | Maximum/Overflow | `--unattended --interactive` | true | Refused for 5 commands; unspecified for adversarial, brainstorm, release-split | GAP (finding 18) |
| G1 | `SPEC:228` | Sentinel Value Match | `"... --unattended ..."` inside a quoted argument | ambiguous | No parsing rule | GAP (finding 17) |
| G1 | `SPEC:228` | Legitimate Edge Case | a person types `--unattended` in their own session | true | Unattended behaviour applies; outward defaults off (WC-9). Safe direction | OK |
| G2 WC-5 outcome mapping | `SPEC:63` | Zero/Empty | no contract file | n/a | `--outcome failed` | OK |
| G2 | `SPEC:62-63` | One/Minimal | `status: success` (existing vocabulary) | no rule matches | Unspecified; 7.2 step 4 asserts failure | GAP (finding 2) |
| G2 | `SPEC:63` | Typical | `status: succeeded` | succeeded | `--outcome succeeded` | OK |
| G2 | `SPEC:63`, `SPEC:263` | Maximum/Overflow | `status: partial` with dependents | succeeded | Task settles; dependents start on partial output; no coordinator check | GAP (finding 13) |
| G2 | `SPEC:61`, `SPEC:200` | Sentinel Value Match | gate hit, worker uses `ask` instead of `blocked` | either | Outcome differs by worker choice; AC-2.2 expects `failed` | GAP (finding 11) |
| G2 | `SPEC:63` | Legitimate Edge Case | audit command, verdict FAIL | succeeded | `--outcome succeeded`, body states verdict | OK |
| G3 WC-10 single blocking call ≤ 4 min | `SPEC:68` | Zero/Empty | command has no long wait | n/a | Heartbeat every 5 min from the session | OK |
| G3 | `SPEC:68` | One/Minimal | one 240 s wait | allowed | Heartbeat between waits | OK |
| G3 | `SPEC:68`, `SPEC:114` | Typical | pr-submit poll-then-sleep iteration | allowed if < 4 min | Per-iteration runtime UNVERIFIED (`SPEC:283`) but rule stated | OK |
| G3 | `SPEC:65,68` | Maximum/Overflow | Agent-tool fan-out > 5 min | not covered | Unspecified | GAP (finding 8) |
| G3 | `SPEC:61` | Sentinel Value Match | blocked inside `ask` | exempt | No heartbeat while in `ask` (`CAPS:64`) | OK |
| G3 | `SPEC:104` | Legitimate Edge Case | cli-eval eval up to 3600 s | must split | Split into waits ≤ 4 min | OK |
| G4 retry (WC-6) | `SPEC:64` | Zero/Empty | first attempt, no retry | n/a | Normal run | OK |
| G4 | `SPEC:64` | One/Minimal | retry of a command with a resume flag | resume needs the flag in the brief | Task spec cannot change on retry (`worker-start --help` line 47) | GAP (finding 1) |
| G4 | `SPEC:64` | Typical | retry of a "fresh dir" command | same brief, same dir | "fresh output directory" impossible without a new brief | GAP (finding 1) |
| G4 | `SPEC:64` | Maximum/Overflow | 3 consecutive start failures | circuit breaker | Task failed by Orca (`CAPS:116`) | OK |
| G4 | `SPEC:61` | Sentinel Value Match | retry carrying the coordinator's answer | no channel | Unspecified | GAP (finding 1) |
| G4 | `SPEC:64` | Legitimate Edge Case | retry while the first attempt is `unverifiable` (may still be writing) | unspecified | Orca forbids retry on absence (`CAPS:125`); spec silent | GAP (finding 1) |

## 6. Numbered findings
Severity: CRITICAL = provably wrong; MAJOR = ambiguous, incomplete or unsatisfiable under attack; MINOR = clearer wording needed, behaviour inferable. `SPEC:N` = line N of the spec. Ranked most severe first.

| # | Finding | Severity | Spec section | Evidence (path:line) | Expert | Recommendation | Priority |
|---|---|---|---|---|---|---|---|
| 1 | A retry cannot carry a new brief. `worker-start --retry-of` must name the same failed Task, and a Task's spec cannot be edited, so WC-6's "fresh output directory" and WC-3's "re-invoke with the answer as a flag" have no channel. A retry repeats the same brief and output path, overwrites the first attempt's contract, and hits the same gate again. The spec also does not forbid a retry while the first attempt is still `unverifiable`. | CRITICAL | 2.2 WC-3, WC-4, WC-6 | `SPEC:61`, `SPEC:62`, `SPEC:64`; `orca-ide orchestration worker-start --help` (output line 47: "--retry-of needs --task naming the failed Task (--spec creates a new one)"); `orca-ide orchestration task-update --help` (output line 3: only `--status`, `--result`); `CAPS:66`, `CAPS:116`, `CAPS:125` | Hohpe, Whittaker | Define the answer/retry path explicitly: either a new Task (`--spec`) per retry with a new output dir and the answer flag, or a follow-up `send --to dispatch:<id>` carrying the answer. Add an AC that drives one blocked → answered → retried run. | High |
| 2 | WC-4's status set (`succeeded/partial/failed/blocked`) collides with the `status` field existing contracts already write (`success/partial/failed`, plus reflect's `stopped-precondition`), while WC-4 says those commands "keep their fields". 7.2 step 4 then fails a successful workflow or adversarial run, and WC-5 has no rule for `success`. | CRITICAL | 2.2 WC-4, WC-5; 7.2 step 4 | `SPEC:62`, `SPEC:63`, `SPEC:183`, `SPEC:261`; `src/superclaude/skills/sc-workflow-protocol/refs/return-contract.md:7`; `src/superclaude/skills/sc-adversarial-protocol/SKILL.md:436`; `src/superclaude/skills/sc-reflect-protocol/SKILL.md:250` | Fowler, Whittaker | Use a new field name (for example `worker_status`) or map the existing values explicitly, and state the mapping in WC-5. | High |
| 3 | Fan-out then merge (N troubleshoot workers → 1 adversarial) assumes all N complete reports reach the merge. With Orca deps, one `blocked` worker keeps the merge Task blocked (and finding 1 means a retry may never clear it); a `partial` one is merged unchecked. The spec defines neither path. Classified CRITICAL under the panel's pipeline rule (FR-19). | CRITICAL | 1.3 (closing paragraph) | `SPEC:39`; `CAPS:88-90`; `src/superclaude/commands/adversarial.md:15` (2-10 files) | Fowler, Whittaker | State the coordinator's merge rule: minimum count of `succeeded` (non-partial) inputs, and what happens to blocked or partial inputs. | High |
| 4 | WC-4 says the contract is `<output-dir>/return-contract.yaml` with a directory the coordinator passes and knows before dispatch. Several section 3 rows break this: workflow retired `--output` (a STOP) and puts the contract under a generated `<id>`; cleanup-audit writes only to fixed `.claude-audit/`; implement writes beside the ledger; pr-submit beside `monitor-run-<PR>.jsonl`; research names a generated `claudedocs/research_*.md`. | MAJOR | 2.2 WC-4; 3.1; 3.2 | `SPEC:62`, `SPEC:85`, `SPEC:92`, `SPEC:109`, `SPEC:114`, `SPEC:116`; `src/superclaude/skills/sc-workflow-protocol/refs/return-contract.md:3,39`; `src/superclaude/commands/cleanup-audit.md:31,112` | Wiegers, Fowler | Either require a coordinator-passed output dir for every command (and add it where missing) or let WC-4 allow a documented derived path the coordinator can compute before dispatch. | High |
| 5 | AC-C1 scans `src/superclaude/core` for `orca orchestration ...`, but P0 puts the worker contract file (which must describe `ask`, `heartbeat`, `check`, `worker_done`) and a new Orca section of `HOW-WE-WORK.md` in that folder. SA-2 even allows an Orca example in the contract file. P0's own deliverables fail P0's common check. | MAJOR | 5 SA-2; 6 P0; 7.1 AC-C1 | `SPEC:147`, `SPEC:158`, `SPEC:172`; `SPEC:52` | Fowler, Wiegers | Exclude the two named core files from AC-C1, or restrict AC-C1 to commands, skills and agents. | High |
| 6 | Copied from the raw markdown, the AC-C1 regex contains `\|`, which `grep -E` reads as a literal pipe, so the check prints nothing and passes even when a violation exists. Test: `printf 'orca orchestration send\n' \| grep -cE '...(orchestration\|worktree...)...'` printed `0`; the unescaped form printed `1`. The same raw `\|` appears in AC-C4, AC-C5 and AC-0.3. The rendered table shows the right text, so agents reading the source are the ones misled. | MAJOR | 7.1 AC-C1, AC-C4, AC-C5; 7.3 AC-0.3 | `SPEC:172`, `SPEC:175`, `SPEC:176`, `SPEC:193`; test run in this review (Bash, 2026-11-02) | Crispin (via Wiegers), Whittaker | Move shell checks out of table cells into fenced code blocks so they can be copied verbatim. | High |
| 7 | AC-C5 and AC-0.3 use `grep -E '^-[^-]'` to prove edits are additive. A removed markdown bullet shows as `-- item` and a removed blank line as `-`; neither matches. Test: input `-- removed bullet`, `-plain removed`, `-` matched only `-plain removed`. Deleting list items or routing bullets passes as "additive". | MAJOR | 5 SA-4, SA-5; 7.1 AC-C5; 7.3 AC-0.3 | `SPEC:176`, `SPEC:193`; test run in this review | Whittaker | Use `git diff --numstat` and require the deletions column to be 0, or match `^-` and exclude only the `^--- ` header. | High |
| 8 | WC-10 bounds only poll waits and long evals. Agent-tool fan-out, which WC-7 keeps unchanged, holds the top-level session for minutes (troubleshoot Tier 2: "+4-15 min") with no way to heartbeat, and commands may not call Orca (SA-2). No AC checks heartbeats except for pr-submit. | MAJOR | 2.2 WC-7, WC-10; 5 SA-2; 7.3 AC-4.3 | `SPEC:65`, `SPEC:68`, `SPEC:147`, `SPEC:210`; `src/superclaude/commands/troubleshoot.md:76`; `CAPS:130` (whether heartbeat age affects liveness is UNVERIFIED) | Nygard, Whittaker | Either accept heartbeat gaps during fan-out and say so (with the coordinator told not to treat them as death, matching `CAPS:125`), or require fan-out to be launched in a way that returns control within 4 minutes. | Medium |
| 9 | P1 makes every command in 3.1-3.2 accept `--unattended` ("a no-op where a command has no gate"), but 22 commands are changed only in P2-P4, 19 of them to convert a gate (15 in P2, roadmap in P3, 3 in P4). From P1 until then, `--unattended` is accepted by commands that still prompt, so WC-2's promise is false and a coordinator dispatching them stalls. It also conflicts with D3 (a), which says no pr-submit changes. | MAJOR | 6 P1-P4; 9 D3 | `SPEC:159`, `SPEC:160-162`, `SPEC:60`, `SPEC:240` | Newman, Wiegers | Add `--unattended` to a command only in the phase that converts its gates, and list which commands accept it after each phase. | High |
| 10 | AC-1.1 (run in P1) requires every command in 3.1-3.2 to have a `## Unattended mode` section naming `return-contract.yaml`. That includes `/sc:load`, which writes no report by design, all P2-P4 commands not yet changed, and pr-submit, which D3 (a) leaves unchanged. AC-1.1 cannot pass in P1. | MAJOR | 7.3 AC-1.1; 3.2 load row; 9 D3 | `SPEC:195`, `SPEC:112`, `SPEC:159`, `SPEC:240` | Crispin (via Wiegers) | Scope AC-1.1 to the commands each phase changes, and exempt load (and pr-submit under D3 (a)). | High |
| 11 | WC-3 lets the worker "may" ask the coordinator instead of blocking. AC-2.2 expects `failed` with `status: blocked` for the same input. Whether the check passes depends on a worker choice. | MAJOR | 2.2 WC-3; 7.3 AC-2.2 | `SPEC:61`, `SPEC:200` | Adzic | Make the choice fixed by the brief (for example `--on-gate block|ask`) or have AC-2.2 accept both outcomes with their exact expected traces. | Medium |
| 12 | `--unattended` with no output dir: WC-2 (c) requires writing a blocked contract, but WC-4 has no directory. Behaviour unspecified. | MAJOR | 2.2 WC-2, WC-4 | `SPEC:60`, `SPEC:62`, `SPEC:99` | Whittaker | Make the output flag mandatory under `--unattended` and define a chat-only failure (and `--outcome failed`) when it is missing. | High |
| 13 | `partial` maps to `succeeded`, which settles the Task and lets dependent Tasks start on a partial deliverable; the spec gives the coordinator no rule to check before releasing dependents. | MAJOR | 2.2 WC-5; Decisions (`partial` row); 2.3 | `SPEC:63`, `SPEC:263`, `SPEC:73`; `CAPS:77`, `CAPS:86-90` | Hohpe, Cockburn | Add to 2.3: before starting dependents, the coordinator reads the contract and treats `partial` as needing a decision. | Medium |
| 14 | 7.2 step 6 passes only if `git status --short` shows nothing outside the brief's output dir. WC-11 explicitly allows two workers in one worktree, and the worktree can already be dirty (this worktree shows `?? .dev/orca-command-refactor/`), so the check false-fails. | MAJOR | 7.2 step 6; 2.2 WC-11 | `SPEC:185`, `SPEC:69`; `CAPS:115`; `git status --short` in this review | Crispin (via Nygard) | Take a `git status --porcelain` snapshot before dispatch and compare only the difference, or run live checks one worker per worktree. | Medium |
| 15 | Traceability gaps: WC-1 (launch prompt) has no AC that exercises a launch prompt; WC-6 (retry) has no AC; WC-12 (`check`, `consumer_fenced`) has no AC; WC-11 is checked only for `/sc:save`. | MAJOR | 2.2; 7 | `SPEC:59`, `SPEC:64`, `SPEC:69`, `SPEC:70`, `SPEC:180-186`, `SPEC:207` | Wiegers | Add a requirement-to-AC table and one AC per uncovered requirement. | Medium |
| 16 | Stall detection relies on `agentWait` sampled once per 5 minutes. The spec's own main stall is a turn that ends on a chat question; Orca's positive stall proof is a final transcript turn with no `worker_done`. Whether `agentWait` is set for an ended turn is UNVERIFIED, and sampling cannot prove "never". | MAJOR | 1.4 (2); 7.2 step 2 | `SPEC:44`, `SPEC:181`; `CAPS:126`, `CAPS:129` | Nygard | Add the transcript final-turn check (`worker-read --source transcript`) to 7.2 step 2. | Medium |
| 17 | `--unattended` detection has no parse rule: the literal text inside a quoted argument (`/sc:troubleshoot "worker ignores --unattended"`) could switch a person's run to unattended, contrary to D1 (a)'s "cannot misfire on a person" and SA-1. Raised to MAJOR because it is a GAP row (FR-8). | MAJOR | 2.1 Unattended mode; 9 D1 | `SPEC:51`, `SPEC:228`, `SPEC:146` | Whittaker | State that only a standalone token outside quoted arguments counts. | Low |
| 18 | `--unattended` combined with `--interactive`: refused for cleanup, improve, roadmap, explain and business-panel, but unspecified for adversarial, brainstorm and release-split, which rely on the brief author. | MAJOR | 3.1; 3.2 | `SPEC:83`, `SPEC:84`, `SPEC:89`, `SPEC:102-103`, `SPEC:108`, `SPEC:110`, `SPEC:118` | Whittaker | Put one rule in the contract file: `--unattended` always refuses `--interactive` and similar person-mode flags. | Low |
| 19 | Worker-session rules (heartbeat cadence, `ask`, `check`, `worker_done`) are copied into an IronClaude core file although the Orca preamble already supplies them per dispatch; two sources of truth that can drift across Orca versions. | MINOR | 2.1 Contract file; 2.2 WC-3, WC-5, WC-10, WC-12 | `SPEC:52`, `SPEC:10`; `CAPS:8`, `CAPS:130` | Fowler | Keep only command-side rules in the contract file and point to the preamble for worker-session duties. | Low |
| 20 | AC-0.1 checks that `WORKER-CONTRACT.md` is in `KNOWN_CORE_FILES`, but that set only filters the installed-file listing; the installer copies every `*.md` in `core/` anyway. The AC does not prove installation. | MINOR | 2.1; 7.3 AC-0.1 | `SPEC:52`, `SPEC:191`; `src/superclaude/cli/install_core.py:12-13,53,152` | Wiegers | Add an install check (install to a temp dir and assert the file exists). | Low |
| 21 | "Ready today" includes reflect, release-split, tdd and troubleshoot, which need P2 gate changes, and P0 smoke-runs troubleshoot whose short-input STOP is one of those gates. The label overstates readiness. | MINOR | 3.1; 6 P0 | `SPEC:79`, `SPEC:88-91`, `SPEC:158` | Cockburn | Rename to "ready with brief constraints" and state the constraint for each P0 smoke run. | Low |
| 22 | WC-4 sets no schema version, while workflow's contract already has `contract_version: "1.1"`. The coordinator cannot tell old from new contracts across phases. | MINOR | 2.2 WC-4 | `SPEC:62`; `src/superclaude/skills/sc-workflow-protocol/refs/return-contract.md:6` | Newman | Add a required `contract_version` field. | Low |
| 23 | AC-1.3 checks SA-3 with `claude -p`, the non-interactive print mode the spec itself treats as a separate headless signal (reflect), not a person's plain session. | MINOR | 7.3 AC-1.3; 5 SA-3 | `SPEC:197`, `SPEC:280`, `SPEC:151` | Crispin (via Adzic) | Say the check covers file creation only, and pair it with the manual SA-1 check style of AC-2.5. | Low |
| 24 | 7.2 step 5 searches the `worker-read` transcript for `AskUserQuestion`; whether that transcript includes tool-call names is UNVERIFIED (the guide says only that it is the hook-reported transcript). | MINOR | 7.2 step 5 | `SPEC:184`; `CAPS:131` | Nygard | Verify the transcript format in P0 before relying on the check. | Low |

## 7. Expert consensus and disagreements
**Consensus.**
- The core decision (Orca coordinates, commands stay units of work and never call Orca) is well supported and should stand: depth 1 (`CAPS:97-98`), pane-bound `worker_done` (`CAPS:76`), standalone use (`SPEC:34`). No expert found evidence against it.
- The evidence-strength section (`SPEC:41-45`) is honest, and starting with live smoke runs in P0 (`SPEC:158`, `SPEC:194`) is the right order.
- The spec's weak area is the failure path (blocked, retry, partial), not the happy path. Findings 1, 2, 3, 11, 12 and 13 all sit there.
- The acceptance checks need a pass of their own: findings 5, 6, 7, 10 and 14 are checks that pass or fail for the wrong reason.

**Disagreements.**
- *Finding 8 severity.* Nygard rates it MAJOR because a heartbeat gap is the only liveness signal the spec asks for. Fowler would rate it MINOR because whether Orca uses heartbeat age at all is UNVERIFIED (`CAPS:130`) and Orca forbids acting on absence (`CAPS:125`). Kept MAJOR: the spec states WC-10 as a requirement it cannot meet.
- *Finding 13.* Hohpe wants `partial` mapped to `failed`; Cockburn prefers keeping `succeeded` and adding a coordinator check. The recommendation follows Cockburn, which keeps the spec's own reasoning at `SPEC:263`.
- *Finding 19.* Newman would accept the duplication as convenient for people reading one file; Fowler holds that copies of Orca's rules will drift. Kept MINOR.

## 8. Quality scores
Standard-format summary (findings referenced by number; full text in section 6).

```yaml
specification_review:
  original_spec: .dev/orca-command-refactor/specs/orca-worker-contract-spec.md
  review_date: 2026-11-02
  expert_panel: [Wiegers, Adzic, Cockburn, Fowler, Nygard, Whittaker, Newman, Hohpe, Crispin]
  focus_areas: [requirements, architecture]
  mode: critique
quality_assessment:
  overall_score: 5.5
  clarity: 7.5        # plain wording, evidence on almost every row
  completeness: 5.0   # failure paths (blocked, retry, partial, merge) undefined: findings 1, 3, 12, 13
  testability: 4.5    # several ACs pass or fail for the wrong reason: findings 5, 6, 7, 10, 11, 14
  consistency: 5.0    # status vocabulary, contract location, phase vs flag: findings 2, 4, 9
critical_issues: [1, 2, 3]
major_issues: [4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]
minor_issues: [19, 20, 21, 22, 23, 24]
expert_consensus: see section 7
improvement_roadmap:
  immediate: [1, 2, 3, 4, 5, 6, 7, 9, 10, 12]
  short_term: [8, 11, 13, 14, 15, 16, 17, 18]
  long_term: [19, 20, 21, 22, 23, 24]
adversarial_analysis: section 4 (A1-A6) and section 5 boundary table; GAP rows map to findings 1, 2, 8, 11, 12, 13, 17, 18
```

Testing and Gregory/Hightower lenses were outside the requested focus; Crispin's comments appear only where an acceptance check was defective.

## Decisions
| Decision | Options considered | Rationale |
|---|---|---|
| Skip step 6 "Improve" | Write an improved spec; review only | The brief says "Do NOT edit the spec" and the command's boundary forbids modifying a spec without consent. Task 6 owns the revision. |
| Output structure | Pure YAML standard format; critique-mode markdown with a YAML summary | The brief asks for a numbered findings table with path:line; critique mode groups by analysis bucket. A short YAML block keeps the standard-format keys without duplicating the findings. |
| Verdict rule | PASS with minor issues allowed; binary rule | The run's quality rules make any finding of any severity a FAIL; 3 CRITICAL findings would fail under any rule. |
| Cite Orca behaviour not in the capabilities inventory | Mark UNVERIFIED; run read-only `--help` | `orca-ide orchestration worker-start --help` and `task-update --help` are read-only and settle finding 1 with exact output lines. |
| Prove regex defects by running them | Argue from regex rules; run on sample input | A run with fixed sample input in a pipe changes nothing on disk and turns findings 6 and 7 from opinion into observed fact. |
| Severity of the pipeline finding (3) | MAJOR (it is an illustrative paragraph); CRITICAL | The command's FR-19 rule classifies any dimensional mismatch as CRITICAL; the paragraph is the spec's only stated answer to fan-out, so it is load-bearing. |
| Re-check the inventory count | Trust `SPEC:76`; count files | Counted: 44 `.md` files in `src/superclaude/commands/`, one is `README.md`, leaving 43 = 10 + 27 + 6. No finding. |

## UNVERIFIED items
1. Whether Orca sets `observation.agentWait` for a Claude turn that ended on a chat question (finding 16). Not tested: it would need a live worker.
2. Whether `worker-read --source transcript` output includes tool-call names such as `AskUserQuestion` (finding 24; `CAPS:131`).
3. Whether heartbeat age affects Orca's liveness verdict (finding 8; `CAPS:130`). This decides how serious finding 8 is in practice.
4. Whether a coordinator can attach new data to a retried Dispatch other than by `send --to dispatch:<id>` after start (finding 1). The `--help` output read here shows no such option on `worker-start` or `task-update`; other verbs were not read.
5. Spec citations not re-read in this review (carried as the spec states them): `src/superclaude/core/HOW-WE-WORK.md:171,249,254`, `cmd/pr-submit.md:49`, the per-command `INV-A`/`INV-B` lines. Re-read here and found as cited: `CLAUDE.md:16,50,74,83,157,334,408`; `pyproject.toml:38` (`pyyaml>=6.0`); `src/superclaude/cli/install_core.py:13-24`; the E5 grep (only `src/superclaude/skills/ccsession-tag/` files mention Orca; `HOW-WE-WORK.md` count 0); `CAPS` lines cited above.
