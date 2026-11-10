# Spec panel review: orca-worker-contract-spec.md

review: 1 of 3
mode: critique (first review, no --re-review, no --baseline; baseline: missing, not given)
focus: requirements, architecture
candidate: .dev/orca-command-refactor/specs/orca-worker-contract-spec.md
candidate sha256: d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d
prior report: none (first review, no prior-findings table)
lint: .dev/orca-command-refactor/review/lint-1.md, sha256 d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d (matches candidate), Checks: REF, Findings: 0. No lint id to address. No finding below relies on the lint.
reviewer model: claude-haiku-5-5
panel: Wiegers, Adzic, Cockburn (requirements); Fowler (lead), Newman, Hohpe, Nygard (architecture); Whittaker (adversarial, always active); Crispin for the guard table.

## Citation keys

- `spec:N` = `specs/orca-worker-contract-spec.md` line N (candidate).
- `INV-A:N` = `inventory/commands-a.md` line N. `INV-B:N` = `inventory/commands-b.md` line N. `CAPS:N` = `inventory/orca-capabilities.md` line N. `README:N` = `README.md` line N. All are in the workspace and were read in full.
- Paths under `src/`, `.dev/evals/`, `.dev/codegraph-migration/`, `/opt/Orca/`, `~/.claude/`, `EVIDENCE.md`, `CLAUDE.md` and the GitHub or Claude Code docs URLs are outside this sandbox. Every spec claim that rests only on those is UNVERIFIED here. I did not use such a claim as the basis for any finding.

## Scope, method and limits

- Read in full: the FIRST-REVIEW prompt (`~/.claude/rules/prompts/document_review_loop_prompts.md`), `README.md`, `review/lint-1.md`, the candidate (all 286 lines), `inventory/commands-a.md`, `inventory/commands-b.md`, `inventory/orca-capabilities.md`. Command definition (`command.md`) read in full, including Review Loop and Mandatory Output Artifacts.
- Citation check: I checked about 40 inventory citations that the spec makes in sections 1, 2, 3, 4 and 7 against the inventory files. They match, except the tasklist claim in M1, which `INV-A:14` does not support. The row totals were checked: 10 ready, 27 needs-change, 6 coordinator-only (`spec:75`) equal the sums of `INV-A:73` (5/13/3) and `INV-B:278` (5/14/3). The per-command assignment in `spec:81-125` and `spec:130-137` matches both inventory summaries.
- The FIRST-REVIEW prompt requires two first reviews in fresh contexts, then the MERGE rule. This worker is reviewer A only. I cannot brief a second reviewer from this sandbox. The coordinator must run the second review and the MERGE. This report is not a merged report.
- VERIFY (fresh-context verifier of the blocking findings) has not been run. Under the VERIFY rule, a missing reply confirms every finding. Until the coordinator runs VERIFY, treat B1 to B4 as open and unconfirmed.
- Orca was not run. The spec's live smoke runs (P0) are not part of this review.

## Guard-table and mandatory-artifact triggers

- Guard Condition Boundary Table: triggered. The spec has conditional logic in WC-2, WC-4, WC-5, WC-10, WC-12 and the `--unattended` switch (`spec:51`, `spec:60`, `spec:62`, `spec:63`, `spec:68`, `spec:70`). The table is in the section "Guard Condition Boundary Table" below. Synthesis is complete.
- Pipeline Dimensional Analysis: not triggered. The spec has no multi-stage data flow with count change. The fan-out in `spec:24` and `spec:39` is task scheduling, not data transformation.
- Quantity Flow Diagram: not produced, because Pipeline Dimensional Analysis is not triggered.
- State Variable Registry: not required. `--focus correctness` is not active.
- Whittaker attack findings: in the section "Whittaker attacks" below, and cross-referenced from M2, M3, M6 and M10.

## What holds up

- Gate resolution is three-way (default, flag, blocked) and applied per command in `spec:81-125`. This is consistent with the inventories' gate evidence (`INV-A:76-83`, `INV-B:292`).
- The coordinator-only list (`spec:130-137`) matches `INV-A:90-92` and `INV-B:283-287`, and the reasons are stated with citations.
- Section 9 gives each open decision a recommendation, and the recommendations match the constraints in `CAPS:97-101`.

## BLOCKING findings

### B1. WC-3 lets a coordinator's reply stand in for a gate answer, which reopens the /sc:implement Ruling rule

- Severity (panel): MAJOR, graded blocking under Review Loop bullet 2, because it names a safety-boundary risk.
- Location: `spec:61` (WC-3), `spec:109` (implement row), `spec:218` (non-goal 6), `spec:233-236` (D2).
- Grading sentence: an implementer who follows WC-3 as written, at an implement halt, asks the coordinator with `ask`, then re-invokes or resumes `/sc:implement` "with the answer as a flag". The coordinator's reply then serves as the Ruling. That is another agent's message, which `refs/qa.md:238` says is not acceptance (quoted in `INV-A:66`). The spec itself keeps this rule (`spec:109`, `spec:218`) and recommends D2(a) (`spec:236`).
- Also: WC-3 names an answer flag but no command defines one. The implement row (`spec:109`) gives none. So the path has no interface, and an implementer would invent one.
- Fix direction: exclude the implement Ruling from WC-3, and state that a coordinator reply is never a Ruling.

### B2. The contract path rule in WC-4 assumes a directory and a known path. Section 3 rows contradict it

- Location: `spec:62` says `<output-dir>` is "the directory the coordinator passed (`--output` / `--output-dir`)". `spec:73` says the report path is "known before dispatch (WC-4)".
- Contradicted by:
  - `spec:87` init-lite takes `--output <file>`.
  - `spec:90` tdd takes `--output <file>`, and `spec:200` (AC-2.2) uses `--output <file>` for tdd.
  - `spec:85` cleanup-audit has a fixed output dir (`.claude-audit/`) and no flag (`INV-A:42`). The row says so.
  - `spec:86` index-repo has no output flag, and its location is "implied" (`INV-A:53`).
  - `spec:92` workflow writes `.dev/tasks/to-do/<id>/`, where `<id>` is made at run time (`INV-B:52`, `INV-B:272`).
  - `spec:116` research writes a timestamped path "generated at run time" (`INV-B:132`).
- Grading sentence: an implementer who follows WC-4 for tdd passes `--output <file>` and writes `<file>/return-contract.yaml`, which cannot be created. For cleanup-audit and index-repo there is no directory to pass, so the coordinator cannot open the contract before dispatch, as `spec:73` requires.
- Fix direction: define the contract location for file-valued outputs (for example, a sibling file), and give cleanup-audit, index-repo, workflow and research an explicit output directory flag.

### B3. Section 2.3 requires `--unattended` in every brief, but P0 and AC-0.4 run three commands before the flag exists

- Location: `spec:73` (the brief "states the exact command line including `--unattended`"), `spec:180` (7.2 step 1 takes the brief "per section 2.3"), `spec:194` (AC-0.4 runs `/sc:troubleshoot`, `/sc:workflow`, `/sc:adversarial` with no flag), `spec:158` (P0 adds only the contract document, the KNOWN_CORE_FILES entry and the test file), `spec:159` (P1 adds the `--unattended` flag to every command).
- Grading sentence: an implementer who follows `spec:73` and `spec:180` in P0 passes `--unattended` to three commands that do not accept it until P1. AC-0.4 then fails at argument parsing. Following AC-0.4 literally breaks `spec:73`.
- Fix direction: state that P0 briefs omit `--unattended`, and that section 2.3 applies from P1.

### B4. The 7.2 step 6 check requires `git status` to show only output-dir files, but gate-converted commands edit product files on their happy path

- Location: `spec:185` (7.2 step 6, pass condition), `spec:201` (AC-2.3 applies 7.2 to every P2 command with every required flag).
- Commands whose happy path writes outside the output directory, by their own rows:
  - `spec:103` cleanup applies items the file allows without approval, which are edits (`INV-A:43`).
  - `spec:110` improve (`INV-A:52`).
  - `spec:121` task edits code.
  - `spec:105` cli-portify writes to `src/superclaude/cli/<name>/` by default (`INV-A:45`).
  - `spec:109` implement "Edits product files" (`INV-A:51`).
  - `spec:107` document inline mode edits source files (`INV-A:47`).
- Grading sentence: an implementer who runs AC-2.3 for cleanup with every required flag gets applied edits to tracked product files. Step 6 then fails, and AC-2.3 cannot pass as written.
- Fix direction: step 6 should pass when `git status` shows only the output directory, the command's documented artifacts, and files the brief authorizes the command to edit.

## MEDIUM findings (follow-up candidates, not blocking)

M1. Tasklist verdict rests on an unverified nesting claim and cites a line that does not support it. Labelled MAJOR, graded Medium because the wrong outcome needs a depth assumption. `spec:122` says the reflect fan-out "runs one layer below the worker, inside Claude Code's nesting limit, `INV-A:14`". `INV-A:14` states the general limit only. `INV-B:210` and `INV-B:314` mark nested spawning UNVERIFIED. `INV-B:215` says the per-phase reflect fan-out "must run at the worker's top level, not inside subagents", and `INV-B:295` lists it as needs-change. If Stage 10.5 reflect subagents sit at the depth limit, Claude Code "withholds the `Agent` tool" (`INV-A:14`), and the reviews would be silently missing. Fix direction: change the row to needs-change, or mark the claim UNVERIFIED and add an acceptance check.

M2. WC-5 maps a FAIL audit and a `partial` report to `succeeded`, and the verdict lives only in prose. Labelled MAJOR, graded Medium. `spec:63` maps an audit with verdict FAIL to `--outcome succeeded`, and `partial` to `succeeded`. It also says the first sentence of the body "states the report's status and verdict". The spec cites `CAPS:73` as support, and that line says "Never encode failure only in prose". `CAPS:90` says a failed Task keeps dependents blocked, so a succeeded settlement releases them. The wrong outcome (dependents run on a FAIL audit) needs the coordinator to skip the report that `spec:73` tells it to open. Fix direction: add a `verdict` field to the contract and require the coordinator to gate dependents on it, or map a FAIL verdict to `failed`.

M3. WC-3 has no bound on the wait for an `ask` reply. `spec:61` says "wait" with no limit. The default `ask --timeout-ms` is UNVERIFIED (`CAPS:68`). A waiting worker is healthy (`CAPS:52`), so nothing reclaims a worker whose coordinator never replies. Fix direction: state a bounded timeout and the outcome when it expires.

M4. The WC-10 wait split covers two commands only. `spec:68` makes the 4-minute split a general rule. Only cli-eval (`spec:104`) and pr-submit (`spec:114`) are named. Other commands with single blocking calls above 5 minutes are not listed, for example test (`spec:123`), build (`spec:101`), post-release VM steps (`spec:113`, `INV-B:84`) and roadmap's Claude subprocesses (`INV-B:151`). Fix direction: list every command, or make the split a per-command acceptance check.

M5. Reflect remediation under `--unattended` is unauthorised, and the headless rule is ambiguous. `spec:88` says `--unattended` makes `--remediate` "follow the existing headless auto-accept rule". `spec:151` (SA-6) says that rule keys on `claude --print`, and that `--unattended` "reuses it and does not replace it". `INV-B:109` says an Orca worker is not `--print`. So either the worker auto-applies code remediation without an offer, or it does not. WC-9 (`spec:67`) covers only outward actions, so no rule requires the brief to authorise local code edits. The tasklist row (`spec:122`) passes `--unattended` to reflect too. This is a missing restriction, so it is Medium. Fix direction: state which rule applies and require explicit brief authorisation for remediation edits, as D4 does for outward actions.

M6. A fenced worker can still write a contract at the shared path. Whittaker sequence attack, see below. `spec:70` (WC-12) says a fenced worker "stops without sending `worker_done`". `spec:62` (WC-4) requires a contract on every outcome. `spec:64` (WC-6) reuses the output directory when a command resumes from disk. A replacement worker and the fenced worker can then both write `<output-dir>/return-contract.yaml`. Graded Medium because the wrong outcome needs the same-directory assumption. Fix direction: forbid a fenced worker from writing the contract.

M7. Tool-approval prompts are not covered. WC-1 (`spec:59`) and WC-2 (`spec:60`) cover startup prompts, AskUserQuestion and chat yes/no. They do not cover Claude Code tool-permission prompts (Bash, MCP, file write). `CAPS:44-52` covers only startup and questions. The spec does not say how a worker launches Claude (permission mode or allowlist). `spec:22` (E2) claims a worker "has the same tools as a command a person runs", which is UNVERIFIED here. A permission prompt would park the worker silently. The `agentWait` check (`spec:181`) would detect it, but nothing prevents it. Fix direction: add a launch permission requirement to WC-1 or WC-2, and mark E2 UNVERIFIED.

M8. Section 1.1 understates the command changes. `spec:16` says command changes are "limited to the worker contract in section 2". Section 3 and SA-4 (`spec:149`) also require drift reconciliation (roadmap, validate-roadmap, validate-tests), a frontmatter fix (business-panel), a tool addition (explain), a usage-line fix (load) and a default-target fix (validate-tests). SA-4 names them, so this is a scope statement only. Fix direction: say "the section 2 contract plus the defect fixes named in section 3".

M9. WC-5 has no mapping for status values outside the four-value set, and existing contract vocabularies are not compared. `spec:63` and the Decisions table (`spec:262`) fix four values. `spec:62` says commands "keep their fields", but does not say whether existing values (for example workflow's `status`, `INV-B:272`) map onto the four. Those vocabularies were not read (UNVERIFIED). Whittaker legitimate-edge case, see the guard table. Fix direction: list each existing status value and its mapping.

M10. WC-4 does not require the worker to create `<output-dir>`. `spec:62` requires a contract "including stops before any other output exists". A write into a directory that does not exist fails, and the reason for the early stop is lost. Whittaker zero-or-empty attack, see below. Fix direction: require the directory to be created before the contract is written.

M11. `--unattended` with no output directory has no specified behaviour. `spec:62` and the switch in `spec:51` do not say what happens when the brief passes `--unattended` without `--output`. The contract then lands at a default path the coordinator cannot predict (`spec:73`). Guard-table row G2 (FR-9 blank). Fix direction: state a refusal, or a blocked outcome.

M12. Standalone-use check is thin. SA-1 (`spec:146`) is a "hard requirement on every phase" (`spec:142`). It is checked by two command runs (`spec:197`) and one manual check (`spec:203`). Fix direction: add a static assertion that no contract or report file is written without `--unattended` for every changed command.

M13. AC-C1 (`spec:172`) scans `src/superclaude/core`, but P0 edits that directory (`spec:158`: WORKER-CONTRACT.md and the HOW-WE-WORK Orca section). SA-2 (`spec:147`) permits one Orca example in the contract file. The check would fail on the permitted example, and on any Orca wording in the routing guide. Fix direction: exclude the two files from AC-C1, or forbid Orca command text in them.

M14. Post-release install gating is incomplete. `spec:113` gates "real-target install". WC-9 (`spec:67`) gates "installs" in general. `INV-B:84` says the skill also runs a throwaway venv, a container and `pipx install .`. AC-4.2 (`spec:209`) asserts "no install". Fix direction: say whether the throwaway install is off under `--unattended`.

M15. The index P1 change asserts unverified behaviour. `spec:111` says to "state that knowledge-base mode does not wait". `INV-A:54` and `spec:277` (UNVERIFIED item 6) leave that open. Fix direction: verify first, or drop the statement.

M16. WC-4 says "Orca does not check the file" as fact (`spec:62`, last sentence). `CAPS:79` and `spec:274` (UNVERIFIED item 3) say that is unknown. The design does not depend on the answer, so this is a wording fix. Graded Medium, and listed here so it is not lost.

## MINOR notes

N1. WC-5 requires the body's first sentence to state status and verdict (`spec:63`), but no acceptance check tests it (Wiegers, testability).
N2. WC-4 and WC-5 do not say the contract is written before `worker_done` is sent (Hohpe, ordering). Add one sentence.
N3. `spec:11` says the worker re-read 11 locations on 2026-11-02. Those citations are outside the sandbox. UNVERIFIED here.
N4. `spec:105` notes that cli-portify only works inside an IronClaude checkout. The note is accurate, but the brief should say so.
N5. `spec:75` counts and the per-command rows are consistent with the inventories. No action needed. Recorded as a check.

## Whittaker attacks

Format: "I can break this specification by **[attack]**. The invariant at **[location]** fails when **[condition]**. Concrete attack: **[scenario]**."

1. I can break this specification by **Sequence Attack (FR-2.4)**. The invariant at **WC-4 and WC-12 (spec:62, spec:70)** fails when **a worker is fenced after it started writing its contract, and a replacement worker resumes into the same output directory (WC-6, spec:64)**. Concrete attack: worker A runs `/sc:adversarial --output D`, is fenced by a reassigned Dispatch, and still writes `D/return-contract.yaml` as `succeeded`. Worker B, started from the same directory, later writes `blocked`. The coordinator reads A's file. Severity MAJOR. Graded Medium (M6).

2. I can break this specification by **Zero/Empty Attack (FR-2.1)**. The invariant at **WC-4, "including stops before any other output exists" (spec:62)** fails when **`<output-dir>` does not exist yet**. Concrete attack: `/sc:analyze --unattended --output .dev/new/` with `.dev/new/` absent stops at input validation. The contract write fails because the directory is missing. WC-5 then sends `failed` with "no report exists", and the reason is lost. Severity MAJOR. Graded Medium (M10).

3. I can break this specification by **Divergence Attack (FR-2.2)**. The invariant at **WC-5 (spec:63)** fails when **the report's status and verdict disagree with each other, or the status is `partial`**. Concrete attack: an audit writes `status: partial` with `verdict: FAIL`. WC-5 sends `--outcome succeeded` for both. Dependents that wait on the audit are released (`CAPS:90`). Severity MAJOR. Graded Medium (M2).

4. I can break this specification by **Accumulation Attack (FR-2.5)**. The invariant at **WC-3 (spec:61)** fails when **the coordinator never answers an `ask`**. Concrete attack: a worker asks at an unanswered gate and waits. The worker is healthy (`CAPS:52`), so it neither sends `worker_done` nor is reclaimed, and nothing bounds the wait. Severity MAJOR. Graded Medium (M3).

5. I can break this specification by **Sentinel Collision Attack (FR-2.3)**. The invariant at **the `--unattended` switch (spec:51, spec:228)** fails when **a person types the flag in their own session**. Concrete attack: a person runs `/sc:tdd "auth" --unattended` in an interactive session. Every gate resolves as blocked, and no prompt appears, with no warning. D1(a) says a person "never types it" but states no consequence. Severity MINOR. Covered by guard-table row G1 (GAP).

## Guard Condition Boundary Table

Triggered by conditional logic in WC-2, WC-4, WC-5, WC-10, WC-12 and the `--unattended` switch. Owners: Nygard (lead), Crispin (completeness), Whittaker (attacks). Status: OK or GAP. A GAP row carries the finding that covers it.

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| `--unattended` switch | spec:51, spec:228 | Zero/Empty (flag absent) | none | false | SA-1: today's behaviour, spec:146 | OK |
| `--unattended` switch | spec:51 | Typical (flag in brief) | `--unattended` | true | per-command rows in section 3 | OK |
| `--unattended` switch | spec:228 | Sentinel Value Match (person types it) | `--unattended` | true | D1(a) says "a person never types it"; no behaviour stated for when one does | GAP, Medium (Whittaker attack 5) |
| Contract path | spec:62 | Zero/Empty (no output flag) | none | n/a | no default and no refusal stated | GAP, Medium (M11) |
| Contract path | spec:62, spec:87, spec:90 | Legitimate Edge (`--output` names a file) | `<file>` | path would be `<file>/return-contract.yaml` | not stated; contradicts WC-4 | GAP, blocking (B2) |
| Contract path | spec:62 | Typical (`--output` names a directory) | `<dir>` | writes `<dir>/return-contract.yaml` | stated | OK |
| Outcome mapping | spec:63 | Zero/Empty (no report) | none | failed | stated ("no report exists") | OK |
| Outcome mapping | spec:63, spec:263 | One/Minimal (status `partial`) | `partial` | succeeded | stated, with rationale | OK |
| Outcome mapping | spec:63 | Sentinel (audit with verdict FAIL) | FAIL | succeeded | verdict only in body prose | GAP, Medium (M2) |
| Outcome mapping | spec:63 | Legitimate Edge (status outside the four values) | e.g. `completed` | not stated | not specified | GAP, Medium (M9) |
| Ask wait | spec:61 | Zero/Empty (no coordinator reply) | none | waits | no bound | GAP, Medium (M3) |
| Heartbeat wait | spec:68 | Maximum (single tool call over 300 s, commands outside cli-eval and pr-submit) | about 360 s | no heartbeat during the call | split rule names two commands | GAP, Medium (M4) |
| Heartbeat wait | spec:68 | Typical (240 s or less) | 240 s | no split needed | stated | OK |
| Fence | spec:70 | Sentinel (`consumer_fenced` while the contract is due) | fenced | contract written or not | silent | GAP, Medium (M6) |
| Outward authorisation | spec:67 | Zero/Empty (no authorisation in brief) | false | outward actions off | stated for outward actions | OK for outward actions; GAP for local code edits, Medium (M5) |
| Confidence gate | spec:121 | Boundary (confidence exactly 0.70) | 0.70 | not below threshold, so proceeds | "below 0.70" implies it | OK |

Classes left out, with reasons: the switch is boolean, so Maximum and Legitimate Edge do not apply. The fence and ask guards have no numeric threshold, so Maximum applies only to the heartbeat row.

## Follow-up candidates (for the session's one user question per loop; none created here)

Medium: M1, M2, M3, M4, M5, M6, M7, M8, M9, M10, M11, M12, M13, M14, M15, M16.
Minor: N1, N2, N3, N4, N5.

Note on the MERGE: M1 to M16 come from reviewer A only. The second first review is not run.

## Reviser brief

Blocking finding ids: B1, B2, B3, B4.

Restated rule (Review Loop bullet 6): revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; prefer deleting or narrowing to adding; report the byte size before and after, and the bytes added and deleted per finding id. Medium and minor findings are not in this brief and must not be edited under it.

Brief clauses overridden: none.

Pending before revision: the coordinator runs the second first review and the MERGE, then VERIFY (fresh context) on these ids. Only confirmed ids go to REVISE.

verdict: FAIL
