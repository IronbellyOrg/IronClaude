# Spec panel review: orca-worker-contract-spec.md

review: 1 of 3
Command: `/sc:spec-panel-armb @.dev/orca-command-refactor/specs/orca-worker-contract-spec.md --mode critique --focus requirements,architecture`
Task: task_dca721d5b34b (Task 5, independent review). Reviewer did not write the spec. The spec was not edited.
Repo root: /home/coder/workspaces/worktrees/IronClaude/exp346-v-ponytail. `SPEC:N` = line N of `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`.

## 1. Scope and method
- Mode: critique (severity-classified findings). Focus: requirements (Wiegers lead, Adzic, Cockburn) and architecture (Fowler lead, Nygard, Newman, Hohpe). Whittaker's adversarial pass is always on. Testing, compliance and cloud experts were not convened (outside the requested focus).
- Stance: adversarial. Every load-bearing claim checked below was re-read in this worktree on 2026-11-08, not taken from the spec or the inventories.
- Grading: a CRITICAL, or a MAJOR that names a concrete wrong outcome an implementer would produce, is **blocking**; other MAJOR and all MINOR findings are notes (the command file's `Review Loop` bullet 2, as loaded for this run).
- Not done: the Improve step (no revised spec written; the brief forbids editing the spec). No live Orca run and no test run.

### Spec claims re-verified (all held)
| Claim | Where in spec | Re-read evidence |
|---|---|---|
| 43 commands in `cmd/` | SPEC:76 | `ls src/superclaude/commands/*.md` lists 44 files = 43 commands + `README.md` |
| Only `ccsession-tag` mentions Orca (E5) | SPEC:25 | `grep -rlni orca src/superclaude/{commands,skills,core,agents}` lists only `src/superclaude/skills/ccsession-tag/*` |
| AC-C1 prints nothing today | SPEC:172 | the AC-C1 grep returned no match (exit 1) |
| `KNOWN_CORE_FILES` location | SPEC:52 | `src/superclaude/cli/install_core.py:13-24` |
| auggie-review has `--post-pr`, `--no-post-pr`, `--no-remediation-offer`, `--output-dir` | SPEC:100 | `src/superclaude/commands/auggie-review.md:51-55` |
| research has `--strategy planning` | SPEC:116 | `src/superclaude/commands/research.md:25` |
| `question` is a valid wait type | SPEC:182 | `CAPS:75` (`[H:send]` line 31) |
| Missing heartbeats never authorize retry or release | context for F6 | `CAPS:111`, `CAPS:125` |

## 2. Requirements analysis (Wiegers, Adzic, Cockburn)

=== REQUIREMENTS ANALYSIS ===

**Wiegers (requirements quality).** The requirement set is well structured (each WC row names an owner and evidence), but four requirements cannot be met as written:
- WC-4 fixes the status values to `succeeded / partial / failed / blocked` (SPEC:62) and in the same row tells commands that already write a contract to "keep their fields". The existing contracts write `status: success | partial | failed` (`src/superclaude/skills/sc-adversarial-protocol/SKILL.md:436`; `src/superclaude/skills/sc-workflow-protocol/refs/return-contract.md:7`), and brainstorm adds `dry-run` (`src/superclaude/skills/sc-brainstorm-protocol/SKILL.md:341`). Both instructions cannot hold, and the 7.2 step 4 assertion (SPEC:183) rejects `success`. Finding F1, CRITICAL.
- WC-4 says the contract goes in `<output-dir>/return-contract.yaml`, "the directory the coordinator passed (`--output` / `--output-dir`)", and that it is "known before dispatch" (SPEC:62). For three commands the spec puts in scope this has no answer: `/sc:tdd` and `/sc:init-lite` take `--output` as a *file* path (`src/superclaude/commands/tdd.md:49`; `src/superclaude/commands/init-lite.md:32`), and `/sc:workflow` rejects `--output` (`E-LEGACY`, `src/superclaude/skills/sc-workflow-protocol/SKILL.md:24`) and names its folder with a generated ID (`SKILL.md:44`). Finding F2, MAJOR blocking.
- WC-6 makes the *command* responsible for a fresh output folder per run (SPEC:64), but the output folder is fixed in the Task brief at `task-create` time (SPEC:73, SPEC:180), and a retry reuses that Task (`CAPS:116`). Finding F5, MAJOR blocking.
- WC-10 forbids a single blocking tool call over 5 minutes (SPEC:68), while WC-7 keeps every command's own Agent-tool fan-out (SPEC:65). Finding F6, MAJOR blocking.

**Adzic (specification by example).** Section 7 gives runnable checks, which is good. Two examples contradict the rules they test:
- AC-2.2 runs `/sc:tdd "auth" --unattended --output <file>` and expects a contract with `status: blocked` (SPEC:200). Under WC-4 nobody can say where that contract is, because `<file>` is not a folder (F2).
- AC-0.4 requires 7.2 steps 1-3 to pass in Phase 0 (SPEC:194), but step 3 requires the report path to be "the WC-4 contract path" and the outcome to match "the contract's `status`" (SPEC:182). Phase 0 has no contract; the same row says so. Finding F3, MAJOR blocking.
- No example shows a gate that resolved as blocked being answered and the command then finishing. For cli-portify that path does not exist (F7).

**Cockburn (actors and goals).** The actors are clear: coordinator, worker session, command, person (SPEC:57-70, SPEC:73). One goal is not served: the coordinator's goal "dispatch any command that has an `## Unattended mode` section and get a report" breaks after Phase 1, because AC-1.1 requires that section on every section 3.1 and 3.2 command in Phase 1 (SPEC:195), while their gates are converted only in Phases 2-4 (SPEC:160-162). Finding F4, MAJOR blocking. The worker session's main step, "run the command", is also not defined (F8).

## 3. Architecture analysis (Fowler, Nygard, Newman, Hohpe)

=== ARCHITECTURE ANALYSIS ===

**Fowler (interfaces and boundaries).** The core decision (coordinator on top, commands as units of work, no Orca calls in commands) is sound and well argued: R1-R5 (SPEC:33-37) each cite real constraints, and the depth-1 fence is confirmed at `CAPS:97-99`. The weak point is the interface between worker session and command:
- WC-7 says the worker "runs the command directly in its own session" (SPEC:65) but not *how*. A worker receives the brief as typed text, so `/sc:x` in the brief is not a slash-command invocation; the repo rule is that a `/sc:` command loads its skill through the Skill tool (`CLAUDE.md:11`). The checks look only for an Agent-tool wrapper (SPEC:194) and for `AskUserQuestion` (SPEC:184). A worker that reads the command file and improvises the protocol passes every check, so Phase 0 can "confirm" the decision without the protocol having run. Finding F8, MAJOR blocking.
- The `--unattended` interface has no defined behaviour in the window between "flag accepted" (Phase 1, SPEC:159) and "gate converted" (Phases 2-4). F4.

**Nygard (failure modes).**
- Liveness: WC-10's 4-minute split covers poll waits, but the longest blocking calls in these commands are Agent-tool fan-outs: adversarial delegates to debate and merge agents (`src/superclaude/skills/sc-adversarial-protocol/SKILL.md:462-480`), tasklist runs one parallel Agent wave per phase file (`src/superclaude/skills/sc-tasklist-protocol/SKILL.md:1618`), troubleshoot Tier 2 runs agent subprocesses (`src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md:438`). pr-submit runs troubleshoot in its own session (`src/superclaude/skills/sc-pr-submit-protocol/SKILL.md:66,194`). The top-level session cannot heartbeat while an Agent call is open, and WC-7 forbids subagents from heartbeating. AC-4.3 "no single tool call exceeds 240 s" (SPEC:210) then fails for any Tier 2 diagnosis. The harm is bounded: missing heartbeats never authorize retry or release (`CAPS:111`, `CAPS:125`). F6.
- Retry: a retry reuses the Task and therefore the brief's output folder (`CAPS:116`; SPEC:180). For every "fresh dir" command (most of section 3.2) the retry writes into the first attempt's folder and overwrites its `return-contract.yaml`, which is exactly what WC-6 forbids. F5.
- Partial write: a contract whose `status` is missing (crash mid-write) falls into WC-5's "otherwise → succeeded" branch (SPEC:63). Part of F1.

**Newman (evolution and compatibility).** Reusing `return-contract.yaml` (SPEC:261) is the right call, but the spec changes the meaning of an existing field (`status` values) without a version bump. workflow already versions its contract (`contract_version: "1.1"`, `src/superclaude/skills/sc-workflow-protocol/refs/return-contract.md:1,6`). The fix belongs in WC-4: either accept the existing `success` value and map it, or add a separate field such as `worker_status`. F1.

**Hohpe (message flow).** The lifecycle messaging follows Orca's own guide: one `worker_done`, `ask` resumed by message ID, `check` pull, `consumer_fenced` stop (SPEC:61-63, 70; `CAPS:60`, `CAPS:66-67`, `CAPS:73`). Two gaps:
- WC-3 says the session *may* ask instead of blocking (SPEC:61), so the same gate gives the coordinator either a `question` message or a `blocked` report, at the worker's choice. That is acceptable but should be stated as the coordinator's expected handling. Note N4.
- The answer to an `ask` must come back "as a flag" (SPEC:61), but section 3 names no answer flag for several blocked gates. F7.

## 4. Adversarial analysis (Whittaker)

1. I can break this specification by **Sentinel Collision Attack**. The invariant at **WC-4 / 7.2 step 4 (SPEC:62, SPEC:183)** fails when **a command that already writes a contract keeps its own `status` field as WC-4 instructs**. Concrete attack: before: `/sc:adversarial --compare a.md b.md --depth quick --output d/ --unattended` succeeds and writes `status: "success"` (`sc-adversarial-protocol/SKILL.md:436`); step 4 runs `assert d['status'] in {'succeeded','partial','failed','blocked'}`; after: AssertionError, the live check fails a successful run. (F1)
2. I can break this specification by **Zero/Empty Attack**. The invariant at **WC-5 (SPEC:63)** fails when **the contract file exists but `status` is empty or absent**. Concrete attack: the session is killed after `return-contract.yaml` is opened and before `status` is written; on restart the worker sees a report, WC-5's "otherwise" branch applies; after: `worker_done --outcome succeeded` for a run that produced nothing. (F1)
3. I can break this specification by **Divergence Attack**. The invariant at **WC-4 "known before dispatch" (SPEC:62)** fails when **the command's `--output` is a file, not a folder**. Concrete attack: brief says `/sc:tdd "<component>" --unattended --output docs/design/TDD_X.md` (`commands/tdd.md:49`); the implementer must choose `docs/design/TDD_X.md/return-contract.yaml` (impossible, the file exists) or `docs/design/return-contract.yaml` (collides with every other TDD written to `docs/design/`); the coordinator's `test -s <contract>` (SPEC:183) checks a path no rule defines. (F2)
4. I can break this specification by **Sequence Attack**. The invariant at **WC-6 (SPEC:64)** fails when **the coordinator retries a failed Task**. Concrete attack: attempt 1 of `/sc:analyze src/ --unattended --output .dev/analyze/x/` writes `x/return-contract.yaml` with `status: failed`; `worker-start --retry-of` reuses the Task and its brief (`CAPS:116`); attempt 2 writes the same path; after: the first attempt's output is overwritten, which WC-6 forbids. (F5)
5. I can break this specification by **Sequence Attack**. The invariant at **AC-1.1 and Phase 1 scope (SPEC:159, SPEC:195)** fails when **the coordinator dispatches a Phase-3 or Phase-4 command after Phase 1 ships**. Concrete attack: after P1, `cmd/implement.md` carries an `## Unattended mode` section (AC-1.1 demands it); the coordinator dispatches `/sc:implement <plan> --unattended`; the Ruling halt is still a person prompt until P4 (SPEC:109); after: the worker parks on the prompt, Orca reports it "healthy" (`CAPS:129`), and no `worker_done` arrives, the silent stall WC-2 exists to prevent (SPEC:60). (F4)
6. I can break this specification by **Accumulation Attack**. The invariant at **WC-10 (SPEC:68)** fails when **the command's own Agent-tool fan-out takes longer than 5 minutes**. Concrete attack: `/sc:tasklist <roadmap> --unattended` reaches Stage 10.5 and opens one parallel Agent wave over N phase files (`sc-tasklist-protocol/SKILL.md:1618`); the top-level session is inside one tool call for the whole wave; WC-7 forbids the subagents from heartbeating; after: heartbeat gap > 5 minutes, WC-10 violated, AC-4.3 (SPEC:210) fails by definition. (F6)
7. I can break this specification by **Divergence Attack**. The invariant at **WC-2 (b)/(c) and AC-2.3 (SPEC:60, SPEC:201)** fails when **a gate fires on every run and has no flag to pre-answer it**. Concrete attack: cli-portify always stops at "Present to user for approval before Phase 3" and "Present final spec to user for approval before delivering" (`sc-cli-portify-protocol/SKILL.md:152,393`); the spec resolves each as blocked (SPEC:105) and defines no approval flag; the coordinator answers the `ask`, the worker re-invokes, hits the same gate; after: cli-portify can never reach `succeeded` unattended, and AC-2.3 "happy-path run per P2 command" cannot pass. (F7)
8. I can break this specification by **Sentinel Collision Attack**. The invariant at **WC-7 (SPEC:65) and AC-0.4 (SPEC:194)** fails when **the worker reads `~/.claude/commands/sc/<name>.md` and follows it from memory instead of loading the skill**. Concrete attack: transcript has no Agent call and no `AskUserQuestion`; steps 1-7 pass; after: Phase 0 records the direct route as proven although the command's protocol never loaded, and section 1 is not reopened. (F8)

## 5. Guard Condition Boundary Table
Built by Nygard, completeness-checked by Crispin's rule (6 rows per guard), attacked by Whittaker. Every GAP row maps to a finding in section 7 (FR-8: MAJOR minimum).

| Guard | Location | Input Condition | Variable Value | Guard Result | Specified Behavior | Status |
|---|---|---|---|---|---|---|
| G1 unattended switch | SPEC:51, WC-2 SPEC:60 | Zero/Empty | flag absent | false | today's behaviour, every prompt kept (SA-1, SPEC:146) | OK |
| G1 unattended switch | SPEC:51 | One/Minimal | `--unattended` on a no-gate command (analyze) | true | no-op plus contract (SPEC:159, SPEC:99) | OK |
| G1 unattended switch | SPEC:51 | Typical | `--unattended` on a converted gated command (auggie-review) | true | implies `--no-post-pr --no-remediation-offer` (SPEC:100) | OK |
| G1 unattended switch | SPEC:159, SPEC:195 | Maximum/Overflow | `--unattended` on a gated command not yet converted (implement after P1, before P4) | true | none: section exists (AC-1.1) but the gate still prompts | GAP (F4) |
| G1 unattended switch | SPEC:128 | Sentinel Value Match | `--unattended` passed to a section-4 command (`/sc:git`) | n/a | none stated | GAP (N7) |
| G1 unattended switch | D1 SPEC:228 | Legitimate Edge Case | a person types `--unattended` | true | same as worker (flag is opt-in, SPEC:217) | OK |
| G2 outcome mapping | WC-5 SPEC:63 | Zero/Empty | contract exists, `status` missing or empty | "otherwise" | `--outcome succeeded` (wrong) | GAP (F1) |
| G2 outcome mapping | WC-5 SPEC:63 | One/Minimal | no contract file | failed | `--outcome failed` | OK |
| G2 outcome mapping | WC-5 SPEC:63 | Typical | `succeeded` / `partial` | succeeded | `--outcome succeeded`; body names status | OK |
| G2 outcome mapping | WC-5 SPEC:63 | Maximum/Overflow | `failed` / `blocked` | failed | `--outcome failed` | OK |
| G2 outcome mapping | WC-4 SPEC:62, SPEC:183 | Sentinel Value Match | existing value `success` or `dry-run` | "otherwise" in WC-5, rejected by 7.2 step 4 | contradictory | GAP (F1) |
| G2 outcome mapping | WC-5 SPEC:63 | Legitimate Edge Case | audit succeeded with verdict FAIL | succeeded | `--outcome succeeded`; but WC-4 has no `verdict` field | GAP (N5) |
| G3 wait size | WC-10 SPEC:68 | Zero/Empty | no long wait | n/a | heartbeat every 5 min | OK |
| G3 wait size | WC-10 SPEC:68 | One/Minimal | poll iteration < 4 min | pass | heartbeat between iterations | OK |
| G3 wait size | WC-10 SPEC:68 | Typical | pr-submit 600 s budget over iterations | pass | already compliant if each iteration < 4 min (UNVERIFIED, SPEC:283) | OK |
| G3 wait size | WC-10 SPEC:68 | Maximum/Overflow | cli-eval run up to 3600 s | fail | split into waits of at most 4 min (SPEC:104) | OK |
| G3 wait size | WC-7 SPEC:65, WC-10 SPEC:68 | Sentinel Value Match | one Agent-tool call (fan-out wave) > 5 min | fail | none: cannot split, subagents may not heartbeat | GAP (F6) |
| G3 wait size | WC-10 SPEC:68 | Legitimate Edge Case | a call of exactly 4-5 min | pass | "at most 4 minutes" | OK |
| G4 ask and answer | WC-3 SPEC:61 | Zero/Empty | coordinator replies with an empty body | n/a | none stated | GAP (N4) |
| G4 ask and answer | WC-3 SPEC:61 | One/Minimal | one ask, answered | answered | re-invoke with the answer "as a flag" | OK |
| G4 ask and answer | WC-3 SPEC:61 | Typical | ask times out | timeout | resume the same message ID | OK |
| G4 ask and answer | WC-3 SPEC:61 | Maximum/Overflow | answer given, gate has no answer flag (cli-portify approval) | answered | none: re-invocation hits the same gate | GAP (F7) |
| G4 ask and answer | WC-3 SPEC:61 | Sentinel Value Match | worker chooses blocked instead of ask | n/a | either is allowed ("may") | OK (N4 note) |
| G4 ask and answer | D2 SPEC:233 | Legitimate Edge Case | ask is for an implement Ruling | n/a | refused under D2 (a); worker ends failed | OK |
| G5 launch readiness | WC-1 SPEC:59 | Zero/Empty | no launch prompt | ready | proceed | OK |
| G5 launch readiness | WC-1 SPEC:59 | One/Minimal | prompt with 30 s fallback | ready | passes (`EVIDENCE.md:45`) | OK |
| G5 launch readiness | WC-1 SPEC:59 | Typical | default 60 s limit | ready | proceed | OK |
| G5 launch readiness | WC-1 SPEC:59 | Maximum/Overflow | fallback > about 45 s | fail | forbidden ("well inside", SPEC:59) | OK |
| G5 launch readiness | WC-1 SPEC:59 | Sentinel Value Match | `--timeout-ms` raised per start | ready | allowed (`CAPS:45`) | OK |
| G5 launch readiness | WC-1 SPEC:59 | Legitimate Edge Case | trust or update dialog | fail | launch-setup owner (SPEC:59) | OK |
| G6 ownership fence | WC-12 SPEC:70 | Zero/Empty | `check` returns no messages | owned | continue (`CAPS:67`) | OK |
| G6 ownership fence | WC-12 SPEC:70 | One/Minimal | one follow-up | owned | read and ack | OK |
| G6 ownership fence | WC-12 SPEC:70 | Typical | checkpoint check | owned | continue | OK |
| G6 ownership fence | WC-12 SPEC:70 | Maximum/Overflow | many batches | owned | ack until count 0 (preamble) | OK |
| G6 ownership fence | WC-12 SPEC:70 | Sentinel Value Match | `consumer_fenced` | fenced | stop, no `worker_done` | OK |
| G6 ownership fence | WC-12, WC-4 | Legitimate Edge Case | fenced mid-write of the contract | fenced | none: a partial contract is left for the retry to find | GAP (part of F5) |

Synthesis gate (FR-10): all six guards are enumerated and every cell is populated; synthesis proceeds.

## 6. Quality scores
| Dimension | Score (0-10) | Reason |
|---|---|---|
| Clarity | 8 | Plain language, one owner per requirement, every gate named per command |
| Completeness | 6 | Report location, retry folder, answer flags and the interim (P1-P4) behaviour are undefined (F2, F4, F5, F7) |
| Testability | 6 | Runnable checks, but AC-0.4, AC-1.1, AC-2.3 and AC-4.3 cannot pass as written (F3, F4, F6, F7) and none detects an improvised command (F8) |
| Consistency | 5 | WC-4 contradicts itself and the existing contracts (F1); WC-7 and WC-10 conflict (F6) |
| Overall | 6.3 | The decision is sound; the contract details need one revision |

Consensus: all seven panellists agree with the decision in section 1 (Orca on top, commands stay units of work). Disagreement: Hohpe would accept WC-3's optional ask as is; Wiegers wants it made deterministic. Recorded as note N4, not blocking.

## 7. Numbered findings
Blocking findings first. "Section" is the spec section; evidence is `path:line` re-read on 2026-11-08.

| # | Finding | Severity | Blocking | Spec section | Evidence |
|---|---|---|---|---|---|
| F1 | WC-4 fixes `status` to `succeeded/partial/failed/blocked` but tells commands with a contract to keep their fields; those commands write `success` (and brainstorm `dry-run`), so the 7.2 step 4 assertion fails on a successful run, and WC-5's "otherwise → succeeded" also maps a missing or empty `status` to success. Fix: one total mapping from every existing value (and missing) to an outcome, or a new field. | CRITICAL | yes | 2.2 WC-4, WC-5; 7.2 step 4; Decisions "Status vocabulary" | SPEC:62, SPEC:63, SPEC:183, SPEC:262; `src/superclaude/skills/sc-adversarial-protocol/SKILL.md:436`; `src/superclaude/skills/sc-workflow-protocol/refs/return-contract.md:7`; `src/superclaude/skills/sc-brainstorm-protocol/SKILL.md:341` |
| F2 | The contract path `<output-dir>/return-contract.yaml` "known before dispatch" is undefined for commands whose `--output` is a file (tdd, init-lite) and for workflow, which rejects `--output`, names its folder with a generated ID and today writes no file for pre-package STOPs. AC-2.2's own tdd example has no checkable contract path. Fix: a per-command contract-path rule in section 3 (or a separate `--contract <path>` the coordinator always passes). | MAJOR | yes | 2.2 WC-4; 3.1 tdd, init-lite, workflow rows; 7.3 AC-2.2 | SPEC:62, SPEC:87, SPEC:90, SPEC:92, SPEC:200; `src/superclaude/commands/tdd.md:49`; `src/superclaude/commands/init-lite.md:32`; `src/superclaude/skills/sc-workflow-protocol/SKILL.md:24,44`; `src/superclaude/skills/sc-workflow-protocol/refs/return-contract.md:37-39` |
| F3 | AC-0.4 requires 7.2 steps 1-3 to pass in Phase 0, but step 3 requires the WC-4 contract path and an outcome matching the contract's `status`; no contract exists before Phase 1, so the Phase 0 smoke runs fail by the spec's own rule and "reopen section 1". Fix: give Phase 0 its own step-3 pass condition (report path = the command's existing report). | MAJOR | yes | 7.2 step 3; 7.3 AC-0.4 | SPEC:182, SPEC:194 |
| F4 | AC-1.1 requires an `## Unattended mode` section on every section 3.1-3.2 command in Phase 1, including brainstorm and init-lite (in no phase), the P3/P4 commands whose gates are converted later, and pr-submit, which D3 (a) keeps off workers. After P1 the coordinator would dispatch e.g. `/sc:implement --unattended`, which still prompts, giving the silent stall WC-2 exists to stop. Fix: state the interim behaviour (for example, an unconverted command under `--unattended` writes `status: blocked` and stops) or scope AC-1.1 per phase. | MAJOR | yes | 6 P1 scope; 7.3 AC-1.1; 3.2 implement, post-release, pr-submit rows; 9 D3 | SPEC:159, SPEC:195, SPEC:84, SPEC:87, SPEC:109, SPEC:113, SPEC:114, SPEC:240; `CAPS:129` |
| F5 | WC-6 gives the command the job of using a fresh folder per run, but the folder is fixed in the Task brief at `task-create`, and `--retry-of` reuses the Task, so every "fresh dir" retry overwrites the first attempt's contract. Fix: make the coordinator owner (retry brief carries a new output folder) or have the command add a run suffix. | MAJOR | yes | 2.2 WC-6; 2.3; 7.2 step 1 | SPEC:64, SPEC:73, SPEC:180; `CAPS:116` |
| F6 | WC-10 forbids a blocking tool call over 5 minutes, but WC-7 keeps the commands' Agent-tool fan-out, which is one blocking call per wave and cannot heartbeat; AC-4.3 "no single tool call exceeds 240 s" then fails whenever pr-submit's in-session troubleshoot reaches Tier 2. Fix: exempt Agent-tool calls from WC-10 and AC-4.3 and say that the coordinator treats a heartbeat gap as absence, not failure. | MAJOR | yes | 2.2 WC-7, WC-10; 7.3 AC-4.3 | SPEC:65, SPEC:68, SPEC:210; `src/superclaude/skills/sc-adversarial-protocol/SKILL.md:462-480`; `src/superclaude/skills/sc-tasklist-protocol/SKILL.md:1618`; `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md:438`; `src/superclaude/skills/sc-pr-submit-protocol/SKILL.md:66,194`; `CAPS:111,125` |
| F7 | Gates resolved "blocked" have no flag to carry the answer, so WC-3's "re-invoke with the answer as a flag" has nothing to pass. cli-portify's approval gates fire on every run, so it can never succeed unattended and AC-2.3's happy path cannot pass for it; review-translation's "pre-confirmed context input" is unnamed. Fix: name the answer flag per blocked gate in section 3, or move cli-portify to coordinator-only. | MAJOR | yes | 2.2 WC-2, WC-3; 3.2 cli-portify, review-translation rows; 7.3 AC-2.3 | SPEC:60, SPEC:61, SPEC:105, SPEC:117, SPEC:201; `src/superclaude/skills/sc-cli-portify-protocol/SKILL.md:152,393` |
| F8 | WC-7 says "run the command directly" without saying how; the brief arrives as text, the repo rule is to load the skill with the Skill tool, and no check detects a worker that only reads the command file and improvises, so Phase 0 can confirm the decision on a run where the protocol never loaded. Fix: WC-7 names the Skill-tool load, and AC-0.4 / 7.2 step 5 check the transcript for that Skill call. | MAJOR | yes | 2.2 WC-7; 7.2 step 5; 7.3 AC-0.4 | SPEC:65, SPEC:184, SPEC:194; `CLAUDE.md:11` |
| N1 | Under `--unattended` the tasklist and reflect rows auto-accept reflect's remediation offer (headless rule), while auggie-review suppresses its remediation offer and troubleshoot resolves its `--fix` offer as blocked; for tasklist this authors one remediation plan per non-passing phase where today Stage 10.5 only offers. Pick one rule for remediation offers and list the extra packages as artifacts. | MAJOR | no | 3.1 reflect row; 3.2 tasklist, auggie-review rows; 3.1 troubleshoot row | SPEC:88, SPEC:91, SPEC:100, SPEC:122; `src/superclaude/skills/sc-tasklist-protocol/SKILL.md:1631`; `src/superclaude/skills/sc-reflect-protocol/refs/remediation-handoff.md:239-243` |
| N2 | 7.2 step 6 (`git status` shows only the output folder) gives a false failure when workers share the worktree (the default) or the tree already has untracked files; compare against a snapshot taken before the run, or run live checks one at a time. | MINOR | no | 7.2 step 6 | SPEC:185; `CAPS:115` |
| N3 | AC-C1 scans `src/superclaude/core`, where SA-2 lets `WORKER-CONTRACT.md` name a caller's question channel; a literal `orca orchestration ask` example there would fail AC-C1. Exclude that file or say "no literal command". | MINOR | no | 5 SA-2; 7.1 AC-C1 | SPEC:147, SPEC:172 |
| N4 | WC-3's "may" lets the same gate yield either a `question` or a `blocked` report; say what the coordinator should expect, and what an empty reply means. | MINOR | no | 2.2 WC-3 | SPEC:61 |
| N5 | WC-5 says the body states the report's "verdict", but WC-4 defines no `verdict` field. | MINOR | no | 2.2 WC-4, WC-5 | SPEC:62, SPEC:63 |
| N6 | E3 cites `invocation_method: "skill-direct"` as proof of a worker invocation, while 1.4 says that run used an Agent-tool subagent; the value describes the subagent's call, so E3 overstates. | MINOR | no | 1.2 E3; 1.4 | SPEC:23, SPEC:43; `.dev/codegraph-migration/orchestration/README.md:31`; `.dev/codegraph-migration/decisions/P3-command-set/adversarial/return-contract.yaml:10` |
| N7 | Behaviour when `--unattended` reaches a section-4 command is not stated (for example, refuse with `status: blocked`). | MINOR | no | 4 | SPEC:128 |
| N8 | 7.2 step 2 cites `[H:worker-show]` Notes directly rather than through a CAPS line, against the spec's own citation convention; `CAPS:129` quotes it. | MINOR | no | 7.2 step 2 | SPEC:10, SPEC:181; `CAPS:129` |

## Decisions
| Decision | Options considered | Rationale |
|---|---|---|
| Skip the Improve step | Write an improved spec; review only | The brief says "Do NOT edit the spec", and Task 6 owns the revision (`.dev/orca-command-refactor/README.md:27`). |
| Experts convened | All 11; the requirements and architecture panels plus Whittaker | The command maps `--focus requirements,architecture` to Wiegers, Adzic, Cockburn, Fowler, Newman, Hohpe and Nygard; Whittaker is active in every review. |
| Grade F2-F8 blocking | Blocking; notes | Each names a concrete wrong outcome an implementer following the spec would produce (failed check, overwritten output, or silent stall), which is the command's rule for a blocking MAJOR. |
| Grade N1 as a note | Blocking; note | Auto-accepting a local remediation plan is a design choice the spec states openly and it writes no outward change; the inconsistency is real but produces no failed check by itself. |
| Repo root | Brief's worktree (exp346-v-ponytail); README's (OrcaCLICommandRefactor-Specs) | The brief names exp346-v-ponytail and all inputs exist there; spec line references are to the copy in this worktree. |

## UNVERIFIED items
1. Whether an Agent-tool fan-out in any listed command actually runs longer than 5 minutes; F6 rests on the calls being single blocking calls, not on measured durations.
2. Whether Orca uses heartbeat age in liveness (`CAPS:130`, `CAPS:182`); F6 assumes not, as the guide says absence never authorizes retry (`CAPS:125`).
3. Whether a worker that receives `/sc:<name>` as task text can trigger Claude Code's slash-command expansion itself; F8 assumes it cannot and must use the Skill tool.
4. Whether `/sc:tdd --output <dir>` is accepted (the flag is described only as "Output path for the final TDD document", `src/superclaude/commands/tdd.md:49`); if it is, F2 narrows to init-lite and workflow.
5. No live Orca run and no test run was made by this review.

## Self-audit
Checked against disk: the claims in section 1's table, every evidence path cited in section 7, the existing contract status values, workflow's `--output` and pre-package rules, cli-portify's approval lines, pr-submit's top-level and troubleshoot lines, tasklist Stage 10.5, the reflect headless rule, and all CAPS lines cited above. Not checked: the inventories' per-command verdicts beyond those rows, `HOW-WE-WORK.md` line citations, and the eleven locations the spec says its author re-read.

## Reviser brief
Blocking findings to fix: F1, F2, F3, F4, F5, F6, F7, F8.
Rules for the reviser (restated from the command's Review Loop bullet 6): revise only text a blocking finding names; add no rule, mechanism or section that no blocking finding calls for; each added paragraph or table cites its finding id; report the spec's byte size before and after. Notes N1-N8 are optional and never require a revision.

verdict: FAIL
