# Adversarial Debate Transcript

## Metadata
- Decision: D3, "Should `/sc:pr-submit` run as an Orca worker at all?" (`.dev/orca-command-refactor/specs/orca-worker-contract-spec.md:339-343`)
- Pipeline: `/sc:adversarial` Mode A, end of Step 2 (assembled by the debate-orchestrator, non-advocating), 2026-11-02T16:25:11Z
- Variants: Variant 1 = option (a), coordinator or person only (`variant-1-original.md`); Variant 2 = option (b), worker with pre-authorization (`variant-2-original.md`); Variant 3 = option (c), unsupervised orca-cli handoff to a person-owned agent tab (`variant-3-original.md`)
- Depth: standard
- Rounds completed: 2 (Round 1 advocate statements, Round 2 rebuttals), plus Round 2.5 invariant probe (`invariant-probe.md`)
- Round 3: skipped, because depth is standard (Round 3 runs only at depth deep)
- Convergence achieved: 100% (27 of 27 diff points agreed, all unanimous); status BLOCKED_BY_INVARIANTS (see Convergence Assessment)
- Convergence threshold: 80% (0.80, default)
- Focus areas: All
- Advocate count: 3
- Diff points scored: 27 = S-001..S-006 (6) + C-001..C-013 (13) + X-001..X-005 (5) + promoted shared assumptions A-004, A-005, A-006 (3). A-001 (CONTRADICTED) and the STATED assumptions A-002, A-003, A-007, A-008 are not promoted diff points in `diff-analysis.md`, so they are outside the denominator. Advocates V2 and V3 gave A-001 a Round 2 position ("equal"); V1 accepted A-001 in Round 1. All three now argue "attended", not "headless".
- Rule for agreement: a point is agreed when at least 2 of 3 advocates name the same answer in their Round 2 "Final per-point positions" table (no Round 1 fallback was needed: all three Round 2 tables cover every scored point). A qualified answer such as "equal (V1, V3)" is its own answer (V1 and V3 jointly superior to V2) and matches only the same qualified answer.

## Round 1: Advocate Statements

### Variant 1 Advocate (option a, coordinator or person only)
<!-- Verbatim copy of `rounds/r1-variant-1.md` (heading levels as in the source file). -->

# D3 Round 1: advocate for Variant 1 (option a, coordinator or person only)

## Position summary
`/sc:pr-submit` is designed to run with a person attending it, and at its default it pushes without asking. So it should run only in the coordinator's session or a person's own session, with no Phase 4 changes (`SPEC:341`), as the spec recommends (`SPEC:343`). A person who wants parallel monitoring can still open one tab per PR under (a). What (a) excludes is an agent starting that outward loop with nobody attending.

Citation keys follow the variants (`SPEC`, `PRC`, `PRS`, `HWW`, `CAPS`, `[CLI]`, `[G]`). All were re-read on 2026-11-02.

## Steelman
### Variant 2 (option b, worker with pre-authorization)
- **Throughput.** Several PRs are monitored at once, each in its own worktree. The coordinator is never held in waits of up to 600 s (`PRC:49`) across up to 5 rounds (`PRC:47`).
- **Heartbeats fit.** The 600 s is a total budget over repeated cycles of one poll followed by a sleep (`PRS:56-80`). The worker can send a heartbeat between cycles (`SPEC:74`, `SPEC:137`).
- **Structured result and resume.** The coordinator gets `worker_done` plus a contract (WC-4, WC-5). The run-log plus `--resume` (`PRS:43-45`, `PRC:56`) fits WC-6. V2 is also the most candid variant about its own costs.

### Variant 3 (option c, unsupervised handoff tab)
- **Parallel with pr-submit unchanged.** Each run is an ordinary top-level session, so `PRS:47-49`, every HALT and every guard (`PRC:28`, `PRC:85`) hold as written.
- **Orca's own route.** Unsupervised starts go through `orca-cli`, with no Run, Task or Dispatch (`[G] 39`). `agent launch --prompt` exists (`[CLI] 49-52`). The cost is one spec sentence, and the coordinator stays free.

## Strengths claimed
1. **It stays attended, as designed.** I accept A-001: the question is whether a person is attending, not "headless". The skill runs "an **attended, in-session** poll loop" (`PRS:19`, `PRS:43`), and monitored runs "are attended in-session loops, not daemons" (`HWW:223`). Unattended mode is for a caller with "no person at the keyboard" (`SPEC:54`). A pr-submit worker is exactly the case the command excludes. Option (a) needs no reinterpretation.
2. **Outward authority stays with a person.** The mandatory PR path "pushes the fixes without asking, and replies to and resolves the review comments it fixed" (`CLAUDE.md:50`). This is "the full mutating/publishing loop" (`HWW:221`, `HWW:307`). Under (a), every step starts from a session a person directs, so no brief has to carry that authority.
3. **It works under every D4 answer; (b) does not.** Under D4 (c) a worker never pushes (`.dev/orca-command-refactor/decisions/D4/option-c.md:3`), and D4 (b) is "Never" (`SPEC:347`). Either way, a pr-submit worker caps at monitor 2. The repo requires monitor 3 (`CLAUDE.md:50`), and in that conflict the routing guide says "disclose the policy conflict and withhold execution" (`HWW:223`). So (b) is usable only under D4 (a).
4. **HALTs reach the person who can act on them.** `pr_head_mismatch` says "follow the recovery steps in the HALT message" (`PRC:28`). Under (a) that message appears in the person's own session, with no contract and no new Task.
5. **No unverified parts.** It does not rely on poll-script runtime (`SPEC:394`), AC-4.3 (`SPEC:276`), Dispatch run-time bounds (`SPEC:393`), or slash commands passed as a prompt (V3).
6. **The top-level rule is met.** Correction: I drop `CAPS:161`, which is about workers. The coordinator is the person's own coordinator session (`SPEC:316`), so `PRS:47-49` holds directly.
7. **Zero cost and reversible.** There are no pr-submit edits and no AC-4.3, and 35 rather than 36 commands accept `--unattended` (`SPEC:195-197`). (b) or (c) can still be adopted later.

## Weaknesses identified
### Variant 2
1. **It removes the person the command assumes.** V2 concedes it "either rewrites that boundary or treats the worker's session as 'attended' when no person watches it". The first option changes `PRS:43` and `HWW:223`. The second empties the word "attended".
2. **Its D4 dependency is misstated.** "D4 (a) or (c)" is WRONG (spot-check 6). Under D4 (b) or (c), (b) caps at monitor 2, and against `CLAUDE.md:50` the guide says to withhold execution (`HWW:223`). Its benefit exists only under D4 (a).
3. **It pushes with nobody watching** (`CLAUDE.md:50`). The guards in `PRC:85` limit *which* commit is pushed. They do not judge *whether* a fix is right.
4. **HALT recovery is slower.** A HALT becomes a blocked contract plus a new Task (WC-6, `SPEC:70`), which V2 admits.
5. **Highest cost, and it rests on unverified parts.** It needs the P4 row (`SPEC:137`) and AC-4.3 (`SPEC:276`), and it depends on UNVERIFIED items 11 and 12 (`SPEC:393-394`).

### Variant 3
1. **It misuses the handoff route.** In a full handoff "the original agent stops", and the route excludes requests to "monitor, wait for results, track completion" (`[CLI] 27`). The row V3 cites ends "and do not monitor completion" (`[G] 39`). Yet V3's coordinator reads the run-log later (X-004).
2. **One citation is overstated.** `CAPS:52`'s "no time limit" concerns startup only, and a started worker that waits on a prompt is "healthy, not failed" (spot-check 4). So it does not set (c) apart from (b). A tab the coordinator launches is also not shown to be "a person's own launch tab".
3. **Its authorization has no anchor.** D4 covers "a worker's outward actions" (`SPEC:345`). A handoff tab is not a worker, so nothing in the spec governs an agent starting an outward loop (X-005).
4. **It is attended in name only.** N visible tabs, nobody shown watching (A-004), and each one pushes without asking (`CLAUDE.md:50`).
5. **It adds little beyond (a).** A person can already open N tabs under (a). V3 adds only an agent doing the typing, which is the step that moves the start away from a person. The launch example is `--agent codex` (`[CLI] 52`), and Claude slash-command prompts are UNVERIFIED (V3's own words).

## Concessions
1. **(a) is serial and holds the coordinator.** Waits run up to 600 s (`PRC:49`) over 2 rounds by default and up to 5 (`PRC:47`), and the coordinator cannot answer workers meanwhile. V2 and V3 are better here (C-005).
2. **"Parallel PRs are rarely needed" has no source** (X-002). `SPEC:343` makes (a) conditional on there being no real need. If that need is shown, I judge (c) less risky than (b), once its Weakness 3 gap is closed.
3. **Under (a), "attended" depends on the person reading the coordinator's session** (A-004). Option (a) only puts the loop where the person already looks.
4. **V2 and V3 meet the PR-head checkout precondition more naturally** (A-006). Under (a), the command must run from the change's worktree, or it halts with `pr_head_mismatch` (`PRC:28`).
5. **V2 is more candid** (S-006) and ties resume to WC-6, which V1 did not.

## Shared assumption responses
| A-NNN | Response | Reason |
|---|---|---|
| A-001 | ACCEPT | The correction is right: the repo's headless signal is `claude --print` with no TTY (`SPEC:391`), and Orca starts Claude interactively (`CAPS:47`). The question is whether a person is attending (`PRS:19`, `PRS:43`, `HWW:223`) versus "no person at the keyboard" (`SPEC:54`). V1's case is restated on that basis in Strength 1 and still holds. |
| A-002 | ACCEPT | All three satisfy `PRS:47-49`. For V1 the support is that the coordinator is the person's own session (`SPEC:316`), not `CAPS:161`, which concerns workers. |
| A-003 | QUALIFY | The guards in `PRC:85` stay unchanged everywhere. Under (b), however, the gate exits change: `--monitor 1` is refused and operator HALTs become blocked contracts (`SPEC:56`, `SPEC:137`). Only (a) and (c) leave the whole state machine as it is. |
| A-004 | QUALIFY | It is true that none of the variants proves someone is watching. The options still differ in degree. Under (b), nobody watches by definition (`SPEC:54`). Under (c), a person would have to watch N tabs. Under (a), the loop is in the one session the person already reads. |
| A-005 | QUALIFY | It applies to every option. A lost session is recovered with `--resume <run-log>` (`PRC:56`, `PRS:44`). Only (b) adds the unknown limit on a Dispatch's total run time (`SPEC:393`). |
| A-006 | ACCEPT | It is a real precondition (`PRC:28-30`, `HWW:223`). It favours V2 and V3, which already sit in the change's worktree. V1 must run from the PR-head checkout (Concession 4). |
| A-007 | ACCEPT | `CLAUDE.md:50` requires monitor 3. Combined with `HWW:223`, this is what makes (b) depend on D4 (a) (Strength 3). |
| A-008 | ACCEPT | One change per worktree and branch, with one PR each, is how all three would get parallelism. |

## Per-point positions
| ID | Superior approach | Reason |
|---|---|---|
| S-001 | equal | Section layout does not affect the decision. |
| S-002 | equal | V1 cites the repo's policy (`HWW`, `CLAUDE.md`); V3 cites Orca's guides. Each covers its own claims, and V3 has one overstated citation (`CAPS:52`). |
| S-003 | V1 | One session and no new topology; the start of the outward loop stays with a person. |
| S-004 | V1 | No pr-submit changes (V3 matches this but adds a new launch route). |
| S-005 | V1 | It is the spec's option (a) and its recommendation (`SPEC:341`, `SPEC:343`). |
| S-006 | V2 | Most candid about its own weaknesses (conceded). |
| C-001 | V1 | Attended as designed (`PRS:43`, `HWW:223`); V3 keeps the text but not the attending person. |
| C-002 | V1 | Pushes and thread actions start from a session a person is directing (`CLAUDE.md:50`, `HWW:221`). |
| C-003 | V1 | The person reads the HALT where it happens (`PRC:28`); no contract and no new Task. |
| C-004 | V3 | Parallel without changing pr-submit (conceded; V2 is also parallel but changes the command). |
| C-005 | V3 | The coordinator stays free with no worker machinery (conceded; V2 is equal on this point). |
| C-006 | V1 | The result is already in the session that needs it; V3 has no signal at all. |
| C-007 | V1 | No dependence on UNVERIFIED item 12 (`SPEC:394`) or AC-4.3. |
| C-008 | V1 | Works under every D4 answer; (b) works only under D4 (a) (`HWW:223`, `CLAUDE.md:50`). |
| C-009 | V1 | Zero cost (`SPEC:195-197`); V3 is close behind. |
| C-010 | equal | `--resume` works the same in all three (`PRC:56`); V2 explains it best. |
| C-011 | equal | All three meet `PRS:47-49`. |
| C-012 | V1 | One place to look, versus N tabs or contracts plus re-dispatch. |
| C-013 | V1 | Explicitly reversible to (b) or (c). |
| X-001 | V1 | A worker with no person at the keyboard (`SPEC:54`) cannot be the attended loop described in `PRS:43`. |
| X-002 | equal | No variant cites evidence either way; V1's claim is unsourced (conceded), and `SPEC:343` leaves the question to the person. |
| X-003 | V1 | Operator HALTs are written for a person to act on (`PRC:28`). |
| X-004 | V1 | V3 contradicts "do not monitor completion" (`[G] 39`, `[CLI] 27`). |
| X-005 | V1 | No decision is needed about who starts the loop; D4 (`SPEC:345`) does not cover V3's coordinator-started tab. |
| A-004 | V1 | Attention is concentrated in the one session the person already reads. |
| A-005 | equal | `--resume` is the recovery path in all three; (b) adds only an unknown Dispatch limit. |
| A-006 | V3 | The change's worktree is already at the PR head (V2 is equal; conceded). |

### Variant 2 Advocate (option b, worker with pre-authorization)
<!-- Verbatim copy of `rounds/r1-variant-2.md` (heading levels as in the source file). -->

# D3 Round 1: Variant 2 advocate (option (b), worker with pre-authorization)

Citation key: `SPEC:N` = `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md:N`; `PRS:N` = `src/superclaude/skills/sc-pr-submit-protocol/SKILL.md:N`; `PRC:N` = `src/superclaude/commands/pr-submit.md:N`; `HWW:N` = `src/superclaude/core/HOW-WE-WORK.md:N`; `CAPS:N` = `.dev/orca-command-refactor/inventory/orca-capabilities.md:N`; `D4c:N` = `.dev/orca-command-refactor/decisions/D4/option-c.md:N`; `[CLI] N` / `[G] N` = line N of `orca-ide skills get orca-cli` / `orca-ide skills get orchestration`. All re-read on 2026-11-02.

## Position summary
When a person wants several PRs reviewed at once and wants the run to know when each is done, (b) is the only option that delivers it through Orca's supervised route, with a completion signal, a contract and pr-submit's state machine (FSM) and guards unchanged; Orca's own role table sends "monitor, wait for results, track completion" to the supervised loop (`[G] 37`). **Correction to my original:** full strength (`--monitor 3`, push/reply/resolve) needs D4 (a) only. D4 (c) forbids any worker push or PR (`D4c:3`), and D4 (b) forbids all outward changes (`SPEC:347`), so under either, (b) caps at `--monitor 2` on an existing PR (`--pr <N>`), leaving fixes uncommitted for the coordinator (`PRS:273`).

## Steelman
### Variant 1 (option (a), coordinator or person only)
(a) is the spec's recommendation (`SPEC:341`, `SPEC:343`) and costs nothing: no pr-submit edits, no AC-4.3 run, 35 rather than 36 commands with `--unattended` (`SPEC:195`). It keeps the repo's mandatory PR path (`CLAUDE.md:50`) and every outward step of the full loop (`HWW:221`) in the session where the person already talks to the coordinator, so HALTs written for an operator (`PRC:28`) land in front of one. It carries no UNVERIFIED piece (`SPEC:394`), and it is reversible: choosing (b) later costs the same as now. If a typical Orca run ends in one PR, (a) is the cheapest correct answer.

### Variant 3 (option (c), unsupervised handoff tab)
(c) gets (b)'s parallelism while changing nothing in pr-submit, through Orca's unsupervised route (`[G] 39`; `agent launch --prompt`, `[CLI] 49-52`). Each run is an ordinary top-level session in a visible tab, so the attended framing (`PRS:43-45`) holds without argument, run-log and `--resume` work as today (`PRC:55-56`), and the cost is one spec sentence. It rightly lets only the person's instruction start an outward loop.

## Strengths claimed
1. **The "attended" boundary is about detachment, not about a person staring at the screen, and a worker meets it.** The skill defines its own term in the next sentences: "closing the session loses it. Durability comes from the write-ahead JSONL run-log + `--resume`, never from detachment ... Do NOT imply a background daemon" (`PRS:43-45`), and "Never hand a side effect to a background shell, detached loop, or subagent" (`PRS:83-84`). An Orca worker is none of those: it is a top-level, interactive Claude session in its own terminal (`CAPS:161`; prompt passed on the command line, `CAPS:47`), not headless by the repo's own test (`SPEC:391`); `CAPS:161` says so for pr-submit by name. I withdraw my original's "rewrites that boundary"; what remains is a one-line clarification of "Will Not: run headless" (`PRC:85`).
2. **It is the route Orca itself prescribes for this job.** PR monitoring is exactly "monitor, wait for results, track completion", which Orca assigns to the supervised coordinator loop (`[G] 37`) and explicitly excludes from full handoffs (`[CLI] 27`). (b) is the only option that is both parallel and on that route.
3. **The coordinator learns the outcome.** A `worker_done` plus a contract in `--output-dir` that points at a markdown summary and `monitor-run-<PR>.jsonl` (`SPEC:137`, `SPEC:276`) gives the coordinator the terminal `status` (`PRC:58`) of each PR, so it can report which PRs are clean. (a) gets this only serially; (c) not at all.
4. **HALTs wait in place, as in (c).** The spec row lets the worker raise an operator HALT through `ask` or `escalation` (`SPEC:137`); a worker parked on a prompt "is healthy, not failed" (`CAPS:52`), and Orca never releases on a question or a late heartbeat (`CAPS:111`). The person can answer it in the coordinator or open the worker's terminal.
5. **Nothing in pr-submit's safety core changes.** The FSM, ordinal gates and guards stay (no upstream or protected-branch push, no force-push, only the cycle's one fix commit, `PRC:85`); `--monitor 1` is refused because its y/n proposal needs a person (`SPEC:137`; `PRS:272`).
6. **The heartbeat fits without new waits.** The 600 s default is a cumulative budget over poll-then-sleep iterations (`PRS:56-80`; `PRC:49`), so WC-10's 4-minute rule (`SPEC:74`) is met if one iteration stays short, which AC-4.3 measures (`SPEC:276`).

## Weaknesses identified
### Variant 1
1. **"Parallel PR monitoring is rarely needed" has no source** (diff X-002). It is the hinge of the spec's own recommendation ("(a), unless parallel PR monitoring is a real need", `SPEC:343`), yet nobody has measured it.
2. **The coordinator is blocked for long stretches.** Each wait is up to 600 s by default (`PRC:49`), the CI wait may need more ("size it to the full check run", same line), and there is an initial review wait, one re-review wait per round (up to `--max-rounds`, hard cap 5, `PRC:47`) and a CI wait (`PRS:51-54`). During each, other workers' `ask`s go unanswered in that turn. V1 names this but does not size it.
3. **"One hop from a person" assumes someone watches the coordinator** (A-004). In a long Orca run the coordinator is often unwatched too, so (a) gets the same "attended" status as a worker, not a stronger one.
4. **"Headless" is the wrong ground.** V1's decisive reason equates `--unattended` with "run headless" (`PRC:85`, `SPEC:54`); the diff analysis marks that CONTRADICTED (A-001; `SPEC:391`).

### Variant 3
1. **It uses the handoff route for the one thing that route forbids.** Full handoffs are for when the user does not ask to "monitor, wait for results, track completion" (`[CLI] 27`); the handoff owner must "create no Run, Task, or Dispatch and do not monitor completion" (`[G] 39`). V3's "the coordinator reads the run-log file later" contradicts that (diff X-004).
2. **No completion signal** (V3's own stated weakness). With N tabs the person must poll every tab by eye.
3. **The authority problem is the same as a worker's, with less record.** The tab's only instruction is the coordinator's prompt text, which is the exact concern behind D4 (`SPEC:345`); a worker brief at least quotes the user's instruction (`SPEC:346`) and leaves a contract.
4. **Unverified and overstated pieces.** Whether `--prompt "/sc:pr-submit ..."` runs as a slash command is UNVERIFIED (V3 admits it); the cited example uses `--agent codex` (`[CLI] 52`); `CAPS:52` is about startup readiness and also says a waiting worker is healthy, so "no time limit" does not favour (c) over (b).

## Concessions
1. **(b)'s value depends on D4 (a).** Under D4 (b) or (c) the worker cannot open the PR or push (`SPEC:347`; `D4c:3`), so it runs `--monitor 2` on a PR the coordinator opened and stops at `halt_before_push` with uncommitted fixes (`PRS:273`). That still parallelizes the slow part (review wait, verification, diagnosis, local fix), but the coordinator must then push, re-trigger and wait, and a monitor-2 ceiling conflicts with the `--monitor 3` project rule (`CLAUDE.md:50`), which must be disclosed, never silently raised (`HWW:223`). If D4 is not (a), (a) or a narrow (b) is close to even.
2. **(b) is the only option with real cost:** the P4 row (`SPEC:137`, `SPEC:185`), AC-4.3 on a scratch fork PR (`SPEC:276`), the summary file and the boundary line. V1 and V3 are cheaper; V1 on cost is plainly better.
3. **UNVERIFIED pieces remain:** poll iteration runtime (`SPEC:394`) and total Dispatch runtime (`SPEC:393`). Until AC-4.3 passes, (b) is a design, not a proven route.
4. **Some HALTs need a person's hands** in the worktree (for example `pr_head_mismatch` recovery, `PRC:28`). `ask` surfaces them; it does not resolve them faster than (a).
5. **If one PR per run is the norm, (a) is better.** I therefore support (a) as the default and (b) as the opt-in when the person's instruction names parallel PR monitoring.

## Shared assumption responses
| A-NNN | Response | Reason |
|---|---|---|
| A-001 | REJECT | An Orca worker is an interactive Claude session with the prompt on the command line (`CAPS:47`), not `claude --print` with no TTY, the repo's headless signal (`SPEC:391`). The live question is "attended", which `PRS:43-45` and `PRS:83-84` define as in-session and not detached; a worker satisfies that. My original's "either rewrites that boundary" is withdrawn. |
| A-002 | ACCEPT | All options run pr-submit top-level (`PRS:47-49`); `CAPS:161` states it for an Orca worker by name. |
| A-003 | QUALIFY | FSM, ordinal gates and `PRC:85` guards are unchanged in (b); (b) only adds an entry rule refusing `--monitor 1` under `--unattended` (`SPEC:137`), because L1's y/n proposal needs a person (`PRS:272`). |
| A-004 | QUALIFY | No option guarantees a person actively watching. If "attended" means "a person can see it", a worker terminal is as visible as V3's tab or the coordinator; if it means "a person is watching", (a) and (c) fail it during long Orca runs too. (b) adds the one thing the others lack: the HALT reaches the coordinator through `ask`/`escalation` (`SPEC:137`). |
| A-005 | QUALIFY | Losing the session loses the monitor in every option (`PRS:43-45`), and `--resume` is the recovery (`PRC:56`). (b) is best placed: Orca's Task/Dispatch records which PR ran where and the contract points at the run-log (`SPEC:137`), so the coordinator knows what to resume. Total Dispatch runtime stays UNVERIFIED (`SPEC:393`). |
| A-006 | ACCEPT | A real precondition (`HWW:216`, `HWW:223`; `PRC:28-30`). For (b) the brief must name a worktree checked out at the PR head, else `pr_head_mismatch` (`PRC:28`). |
| A-007 | ACCEPT | `CLAUDE.md:50` stays in force. Under D4 (b)/(c) a worker's lower ceiling conflicts with it and must be disclosed, not silently raised (`HWW:223`); see Concession 1. |
| A-008 | ACCEPT | (b) is one Task per independent change and PR, each in its own worktree. |

## Per-point positions
| ID | Superior approach | One-line reason |
|---|---|---|
| S-001 | equal | Layout only (L1); no effect on the decision. |
| S-002 | V3 | Widest citation base, including the Orca guides that settle the handoff-versus-supervised question. |
| S-003 | V2 | Supervised parallel topology is Orca's prescribed route for monitoring and tracking completion (`[G] 37`). |
| S-004 | V1 | Zero change surface on pr-submit. |
| S-005 | equal | V1 and V2 are both spec options (`SPEC:341-342`); V3 sits outside, which is not itself a defect. |
| S-006 | V2 | States its own weaknesses most fully, which the debate can test. |
| C-001 | equal (V2, V3) | Both run pr-submit as a top-level, in-session, non-detached session (`PRS:43-45`, `PRS:83-84`); V1's "contradicts" rests on the headless misreading (A-001). |
| C-002 | V1 | Outward steps stay in the coordinator's session; V2 matches it only under D4 (a). |
| C-003 | V2 | `ask`/`escalation` parks the HALT in place and also notifies the coordinator (`SPEC:137`; `CAPS:52`). |
| C-004 | V2 | Parallel and supervised; V3 is parallel but untracked, V1 is serial. |
| C-005 | equal (V2, V3) | Both keep the coordinator free; V1 holds it for each wait (`PRC:47`, `PRC:49`). |
| C-006 | V2 | Only option with an explicit completion signal and contract (`SPEC:137`, `SPEC:276`). |
| C-007 | V2 | Gives a concrete, testable gate (AC-4.3, `SPEC:276`) instead of avoiding the question. |
| C-008 | V1 | Having no D4 dependency is simpler; V2's dependency is now stated correctly (D4 (a) only). |
| C-009 | V1 | Zero cost (`SPEC:195`). |
| C-010 | V2 | Ties `--resume` to Orca's recorded Task state, so the coordinator knows which run to resume. |
| C-011 | equal | All three satisfy `PRS:47-49`. |
| C-012 | equal | V1 suits one PR; V2 and V3 suit several; V2 adds summaries, V3 adds live tabs. |
| C-013 | V1 | States reversibility explicitly; V2 did not. |
| X-001 | V2 | A worker is not headless (`SPEC:391`) and is in-session and not detached (`PRS:43-45`, `CAPS:161`). |
| X-002 | V2 | The need is unmeasured; V1's denial is unsourced, and only V2 meets it on the supervised route. |
| X-003 | V2 | A HALT reaches a person via `ask`/`escalation` without losing the worker (`CAPS:52`, `CAPS:111`). |
| X-004 | V2 | The coordinator needs the result; V3's handoff route forbids monitoring completion (`[G] 39`, `[CLI] 27`). |
| X-005 | V2 | D4 governs a worker's outward actions (`SPEC:345`); V2 applies it to the push, V3 stretches it to a launch. |
| A-001 | V2 | My Round 1 position rejects "worker = headless" on the repo's own test (`SPEC:391`). |
| A-004 | equal | No option guarantees active watching; all rely on visibility. |
| A-005 | V2 | Orca's Task/Dispatch plus the contract tell the coordinator which run-log to resume. |
| A-006 | equal | Every option needs gh auth, the review App and a PR-head checkout (`HWW:223`). |

### Variant 3 Advocate (option c, unsupervised handoff tab)
<!-- Verbatim copy of `rounds/r1-variant-3.md` (heading levels as in the source file). -->

# D3 Round 1: advocate for Variant 3 (option c, unsupervised handoff to a person-owned agent tab)

Citation key (each line re-read 2026-11-02): `PRC:N` = `src/superclaude/commands/pr-submit.md:N`; `PRS:N` = `src/superclaude/skills/sc-pr-submit-protocol/SKILL.md:N`; `SPEC:N` = `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md:N`; `CAPS:N` = `.dev/orca-command-refactor/inventory/orca-capabilities.md:N`; `HWW:N` = `src/superclaude/core/HOW-WE-WORK.md:N`; `EVD:N` = `.dev/evals/ccsession-orca-e2e-20261026/EVIDENCE.md:N`; `[CLI] N` / `[G] N` = line N of `orca-ide skills get orca-cli` / `orca-ide skills get orchestration`; `DA` = `diff-analysis.md` in this folder.

## Position summary
pr-submit stays as written and never becomes a supervised worker. For one PR, (a) is right; when the person asks for several PRs monitored at once, the coordinator launches one person-owned agent tab per PR with `agent launch` and lets go, giving (b)'s parallelism without turning an attended command into an unattended one. Read Variant 3 as "(a) plus a person-requested parallel route", not a rival to (a).

## Steelman
### Variant 1 (option a)
(a) is the spec's recommendation (`SPEC:341`, `SPEC:343`) and costs nothing: no pr-submit edits, no AC-4.3 (`SPEC:276`), 35 rather than 36 commands under `--unattended` (`SPEC:195`). Every outward step of monitor 3 (`HWW:221`) happens in the one session where the person already talks to the coordinator. It depends on no unverified mechanism (no heartbeat sizing, `SPEC:394`; no slash-command-as-`--prompt` path) and stays reversible. It is safe by construction, not by a rule someone must remember.

### Variant 2 (option b)
(b) alone gives the coordinator a machine-readable end state per PR: `worker_done` plus a contract pointing at `monitor-run-<PR>.jsonl` and a summary (`SPEC:137`; WC-4, WC-5 at `SPEC:68-69`). A coordinator can then sequence follow-ups (merge order, a change waiting on a clean review) inside one Orca Run with provenance. It fits technically: an Orca worker is a top-level Claude session (`CAPS:161`, satisfying `PRS:47-49`), and the 600 s wait is a cumulative budget over poll-then-sleep iterations, so heartbeats fit between them (`PRS:56-80`; `SPEC:74`). Durability is the same run-log plus `--resume` (`PRS:43-44`; `PRC:56`).

## Strengths claimed
1. **The command's boundary is kept, not reinterpreted.** pr-submit "Will Not: run headless / imply a daemon" (`PRC:85`) and calls itself "an **attended, in-session** loop" (`PRS:43`). Per DA's A-001 correction the issue is "attended", not "headless": an Orca worker is not headless (`SPEC:391`; `CAPS:47`), but under `--unattended` it is a caller "that has no person at the keyboard" (`SPEC:54`). A tab the person asked for and owns is an ordinary session, not a worker (`SPEC:53`; `[G]` 41), so pr-submit runs in the mode it was written for.
2. **Orca's own routing table names this route.** "The user asks to hand off ownership or start another agent/worktree without supervision | Handoff owner | Use `orca-cli`; create no Run, Task, or Dispatch and do not monitor completion" (`[G]` 39). `agent launch` starts "a fresh agent in a worktree that already exists" with `--prompt` (`[CLI]` 49-52), via the same launch "the app's new-agent tab uses" (`[CLI]` 63); the guide covers Claude ("spawn codex/claude in a worktree", `[CLI]` 6).
3. **HALTs stay live where the run's context is (corrected claim).** DA rightly marks my `CAPS:52` use OVERSTATED: its limit is worker-start readiness only, and a started worker parked on a prompt "is healthy, not failed" (`CAPS:52`), so "no time limit" does not separate (c) from (b). I withdraw it. Its source (`EVD:35`, a tab left unanswered 82 s that Orca did not fail, close or type into) was a person's own launch; `agent launch` uses the same launch path (`[CLI]` 63), but a coordinator-started tab was not observed. The real difference is the HALT path: under (b) "operator HALTs resolve as blocked" (`SPEC:137`), the command writes a blocked contract and stops (WC-2(c), `SPEC:66`), and any follow-up is a new Task (WC-6, `SPEC:70`). Under (c) a HALT such as `pr_head_mismatch`, whose message carries operator recovery steps (`PRC:28`), is read in the session that holds the run, and the person continues there or with `--resume` (`HWW:216`).
4. **Parallelism without pr-submit edits or new verification.** (b) needs the section 3 row (`SPEC:342`), P4 work (`SPEC:185`) and AC-4.3 on a scratch fork PR (`SPEC:276`), with poll runtime UNVERIFIED (`SPEC:394`). (c) needs one spec sentence and never meets WC-10.
5. **Full monitor 3 stays available, as the repo requires.** Every PR goes through `/sc:pr-submit --monitor 3` (`CLAUDE.md:50`). Under (b) a worker reaches monitor 3 only under D4 (a); under D4 (b) or (c) it caps at monitor 2 (DA spot-check 6; `decisions/D4/option-c.md:3`, a worker never pushes). (c) is not a worker, so under any D4 option the person's tab can run the mandated loop once the person authorizes it ("Requested and authorized full loop", `HWW:221`).
6. **The coordinator stays free.** Same benefit as (b) (DA C-005): it is not held for up to 600 s per wait over `--max-rounds` cycles (`PRC:47`, `PRC:49`).

## Weaknesses identified
### Variant 1
1. **The coordinator is held during every wait**: up to 600 s per wait ("CI runs can exceed this", `PRC:49`) over up to `--max-rounds` cycles (`PRC:47`). The spec runs it "after the workers finish" (`SPEC:341`), which avoids this only when no other work is still running; any worker still blocked in `ask` (WC-3, `SPEC:67`) waits that long.
2. **"Parallel PR monitoring is rarely needed" is unsourced** (`DA` X-002), while the spec leaves it open: "(a), unless parallel PR monitoring is a real need" (`SPEC:343`). (a)'s only answer is "serially".
3. **`CAPS:161` is about Orca workers**, so it does not prove V1's coordinator claim (`DA` incidental finding), though the claim itself is true.

### Variant 2
1. **It changes what a HALT is.** HALTs are written for an operator (`PRC:28`); (b) turns them into blocked contracts (`SPEC:137`; `SPEC:66`) and each follow-up into a new Task (`SPEC:70`), which V2 admits "is slower than a person reading the HALT in place".
2. **Its D4 dependency is misstated.** Under D4 (c) a worker never pushes (`decisions/D4/option-c.md:3`; `DA` spot-check 6). Unless D4 (a) wins, (b) caps at monitor 2 (`PRC:37`), cannot run the loop `CLAUDE.md:50` mandates, and a person's session must finish every PR.
3. **It drops a ceiling**: `--monitor 1` is refused under `--unattended` (`SPEC:56`), though `HWW:219` lists it as valid.
4. **It carries the most unverified surface**: poll-iteration runtime (`SPEC:394`), WC-10 sizing (`SPEC:74`), AC-4.3 (`SPEC:276`), and a rewritten "Will Not" line. Its "already fits a worker" and its own "either rewrites that boundary or treats the worker's session as 'attended'" conflict (`DA` X-001).

## Concessions
1. **No completion signal, and none is allowed.** My "the coordinator reads the run-log file later" conflicts with the line I cited: "do not monitor completion" (`[G]` 39); the handoff route excludes requests to "monitor, wait for results, track completion" (`[CLI]` 27). Corrected: the coordinator reports the worktree id and agent handle and stops (`[CLI]` 29), and reads a run-log only on a later instruction. If the person wants outcomes tracked, (b) or serial (a) is right. V2 wins C-006 and X-004.
2. **For a single PR, (a) is as good or better**: launching a tab adds a step and a second place to look.
3. **N tabs need N times the attention.** "Visible" is not "watched" (`DA` A-004); a person can miss a HALT in one of several tabs. V1 wins A-004.
4. **D4 was the wrong hook.** D4 concerns a *worker's* outward actions (`SPEC:345`); a person-owned tab is not a worker. The governing rule is `HWW:221` ("Requested and authorized full loop") and "Push only with approval" (`HWW:215`): the coordinator launches a tab only when the person's instruction names that PR.
5. **Unverified launch details.** Whether a slash command passed as `--prompt` runs as one is UNVERIFIED; (b)'s workers share that risk (`SPEC:383`, item 1, AC-0.4). Also UNVERIFIED: whether it runs when `agent launch` opens a chat rather than a terminal (`[CLI]` 63), and `--agent claude` with `agent launch` (the `[CLI]` 52 example uses codex). A lost launch reply must be retried with `--retry-launch <operationId>`, never a fresh launch (`[CLI]` 65), or two monitors could run on one PR.

## Shared assumption responses

| ID | Response | Reason |
|---|---|---|
| A-001 | ACCEPT | "Headless" is the wrong word: the repo's headless signal is `claude --print` with no TTY (`SPEC:391`), and Orca launches Claude interactively (`CAPS:47`). The argument is "attended" (`PRS:43`; `HWW:223`) versus "no person at the keyboard" (`SPEC:54`), and Variant 3's case rests on that. |
| A-002 | ACCEPT | All three satisfy `PRS:47-49`; a launched tab is a top-level Claude session like any person-started one (`[CLI]` 63). |
| A-003 | QUALIFY | True for (a) and (c): pr-submit is untouched. For (b) the guards in `PRC:85` survive, but the HALT exit path changes (HALTs become blocked contracts) and `--monitor 1` is refused (`SPEC:137`, `SPEC:56`), so "unchanged" overstates it. |
| A-004 | QUALIFY | `PRS:43` defines "attended" against a daemon ("closing the session loses it"), not as active watching. Neither (a) nor (c) guarantees eyes on screen; the real difference is ownership and the HALT path. (c) spreads attention over N tabs, which favours (a) (Concession 3). |
| A-005 | ACCEPT | All three recover only through the write-ahead run-log and `--resume` (`PRS:43-45`; `HWW:216`). In (c) the person owns recovery and resumes in a new tab; what Orca restores after an app restart is UNVERIFIED for every option. Under (b) a lost worker is read as absence, not death (`SPEC:74`), so recovery waits for Orca's stall proofs. Total Dispatch runtime is UNVERIFIED (`SPEC:393`) but irrelevant to (c). |
| A-006 | ACCEPT | Each tab runs in that change's own worktree (`[CLI]` 49), so its checkout is the PR head; a mismatch is still caught by `pr_head_mismatch` (`PRC:28`) and the CI-wait preflight (`PRC:30`). `gh` authentication is the person's machine-wide login in (a) and (c) alike. |
| A-007 | ACCEPT | `CLAUDE.md:50` stands; D3 decides where pr-submit runs. This favours (c) over (b) under D4 (b) or (c), where (b) cannot reach monitor 3 (Strength 5). |
| A-008 | ACCEPT | Parallelism means independent changes, each with its own worktree, branch and PR; (c) launches one tab per such worktree. |

## Per-point positions

| ID | Superior approach | Reason |
|---|---|---|
| S-001 | equal | Section layout does not affect the decision. |
| S-002 | equal | Citation coverage differs, but each variant's key fits its claims; V3's pinned guide lines matter only for its own route. |
| S-003 | V3 | Gives parallel monitoring with pr-submit unchanged; for a single PR V1's topology is equally good (Concession 2). |
| S-004 | equal | V1 and V3 tie at no pr-submit change; V2 needs the full row, summary file and a reconciled boundary (`SPEC:137`, `SPEC:342`). |
| S-005 | equal | Being in or out of the spec's a/b list is not a merit; the spec explicitly leaves parallel need open (`SPEC:343`). |
| S-006 | equal | Placement of self-named weaknesses does not change the decision. |
| C-001 | V3 | Keeps the attended boundary (`PRC:85`, `PRS:43`) and still gives parallelism; V1 keeps it too but serially. |
| C-002 | V1 | Outward steps stay in the session where the person already talks to the coordinator; V3 relies on the person watching N tabs. |
| C-003 | equal | V1 and V3 both keep HALTs live for an operator in the run's own session (`PRC:28`); V2 converts them to blocked contracts and new Tasks. |
| C-004 | V3 | Parallel monitoring without changing pr-submit or verifying heartbeats; V2 reaches the same result at higher cost. |
| C-005 | equal | V2 and V3 both free the coordinator; V1 holds it up to 600 s per wait (`PRC:49`). |
| C-006 | V2 | Only V2 gives the coordinator a completion signal (`worker_done` plus contract); V3 deliberately has none (`[G]` 39). |
| C-007 | equal | V1 and V3 both avoid WC-10's unverified wait sizing (`SPEC:394`); V2 must prove it in AC-4.3. |
| C-008 | V1 | No outward-authorization step beyond the person's normal instruction; V3 needs the person to name each PR (`HWW:221`), V2 needs D4 (a). |
| C-009 | equal | V1 and V3 cost one spec sentence or nothing; V2 costs the P4 row and AC-4.3 (`SPEC:276`). |
| C-010 | equal | All three use the same write-ahead run-log and `--resume` (`PRC:55-56`). |
| C-011 | equal | All three run top-level (`PRS:47-49`). |
| C-012 | V3 | One live tab per PR shows each review loop as it runs; V2 shows only reports; V1 shows one PR at a time. |
| C-013 | equal | V1 and V3 can both move to V2 later at unchanged cost. |
| X-001 | equal | V1 and V3 agree an unattended worker does not fit the attended boundary; V2 contradicts itself on this point. |
| X-002 | V3 | Leaves the need to the person per run instead of asserting it away (V1, unsourced) or building for it permanently (V2). |
| X-003 | equal | V1 and V3 both keep the operator in place; V2's route works but is slower by its own admission. |
| X-004 | V2 | If the coordinator must track completion, only V2 is legitimate; V3 corrected to "do not monitor completion" (Concession 1). |
| X-005 | V1 | Clearest: no extra authority question. V3's D4 framing was misapplied; the governing rule is `HWW:221` (Concession 4). |
| A-001 | equal | All three should argue "attended", not "headless"; V3 accepts the correction. |
| A-004 | V1 | One session is easier to attend than N tabs (Concession 3). |
| A-005 | equal | Recovery is the same run-log plus `--resume` in every option. |
| A-006 | equal | V2 and V3 both run each PR in its own worktree at its head; V1 needs the coordinator's checkout at each PR head in turn. |

## Round 2: Rebuttals

### Variant 1 Rebuttal
<!-- Verbatim copy of `rounds/r2-variant-1.md` (heading levels as in the source file). -->

# D3 Round 2: rebuttal from the Variant 1 advocate (option a, coordinator or person only)

Citation keys as in Round 1: `SPEC:N` = `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md:N`; `PRC:N` = `src/superclaude/commands/pr-submit.md:N`; `PRS:N` = `src/superclaude/skills/sc-pr-submit-protocol/SKILL.md:N`; `HWW:N` = `src/superclaude/core/HOW-WE-WORK.md:N`; `CAPS:N` = `.dev/orca-command-refactor/inventory/orca-capabilities.md:N`; `D4c:N` = `.dev/orca-command-refactor/decisions/D4/option-c.md:N`; `[CLI] N` / `[G] N` = line N of `orca-ide skills get orca-cli` / `orca-ide skills get orchestration`; `DA` = `diff-analysis.md`. Every citation below was re-read on 2026-11-02.

## Responses to criticisms

| # | Criticism | Source | Response | Concede / hold |
|---|---|---|---|---|
| 1 | "Parallel PR monitoring is rarely needed" has no source. | V2 W1; V3 W2; DA X-002 | Correct. Nothing measures it, and `SPEC:343` makes (a) conditional on that need. Under (a) a person can still open one tab per PR themselves, but I withdraw the claim. | Concede |
| 2 | The coordinator is held for long stretches, and V1 did not size it. | V2 W2; V3 W1 | Sized: the loop waits at Wave 1, at each re-review, and at the Wave 8 CI flip (`PRS:51`), each up to 600 s by default, and CI can run longer (`PRC:49`). At the default 2 rounds (`PRC:47`) that is roughly four waits, about 40 minutes (my arithmetic). Partial defence: the spec runs pr-submit "after the workers finish" (`SPEC:341`), so in its own sequence no worker is waiting in `ask` at that point. The cost is real only when other work overlaps. | Concede the cost; hold that the spec's sequence limits it |
| 3 | "One hop from a person" assumes someone watches the coordinator. | V2 W3; DA A-004 | Partly right, and worse for my case than V2 said. At monitor 3 pr-submit "pushes the fixes without asking" (`CLAUDE.md:50`) in every option, (a) included, so nobody approves each push under (a) either. What (a) keeps is narrower: the loop and its HALTs appear in the session the person directs (`[G] 37`), and the person can interrupt it there. | Concede the wording; hold the narrower claim |
| 4 | "Headless" is the wrong ground for V1's main reason. | V2 W4; DA A-001 | Already accepted in Round 1. | Concede (unchanged) |
| 5 | A worker meets the skill's own meaning of "attended": in the session, not detached. | V2 Strength 1, X-001 | The text supports V2. `PRS:43-45` contrasts "attended, in-session" with a daemon ("closing the session loses it ... never from detachment"), and `PRS:83-84` forbids a "background shell, detached loop, or subagent". An Orca worker is none of these, and `CAPS:161` names pr-submit as able to be "an Orca worker". My claim that (b) "contradicts the command's stated design" overstated it. Two points remain. The spec's own word for the mode is "unattended" ("no person at the keyboard", `SPEC:54`). And (b) changes the operator HALT exits (`SPEC:137`). Both are costs to weigh, not a boundary violation. | Concede (X-001 moves to V2) |
| 6 | Orca sends "monitor, wait for results, track completion" to the supervised route. | V2 Strength 2 | (a) is on that route: the coordinator holds the `[G] 37` role and runs the loop itself. The guide does not require the monitoring to sit in a separate worker. | Hold |
| 7 | (a) learns each PR's outcome only one PR at a time. | V2 C-006 | True for several PRs. For one PR the outcome is already in the session. For several, (b)'s `worker_done` plus contract (`SPEC:137`) is the better mechanism. | Concede for several PRs |
| 8 | Under (b), HALTs wait in place through `ask` or `escalation`. | V2 Strength 4, C-003 | WC-3 limits this. A worker may `ask` only at a gate "that fires before the command has written any output except its blocked contract and whose answer fits an existing argument or flag". Every other gate is reported blocked (`SPEC:67`), and the follow-up is a new Task (`SPEC:70`). pr-submit's HALTs come mid-loop, after the run-log exists, or need manual recovery steps (`PRC:28`, `push_range_mismatch` at `PRC:85`). So they become blocked contracts, as V2's original admitted. | Hold |
| 9 | V1 used `CAPS:161`, which is about workers. | V3 W3; DA incidental | Already dropped. A further correction: my Round 1 replacement, `SPEC:316`, says only that the coordinator "is an Orca coordinator session". The better support is that the coordinator is a top-level session the person asked to supervise (`[G] 37`), not a subagent, so `PRS:47-49` holds. | Concede, re-sourced |
| 10 | V3 keeps the boundary and also runs in parallel; V1 runs serially. | V3 C-001 | On the boundary, the three are now equal (response 5). On parallelism V3 is better. | Concede |
| 11 | V3 leaves the parallel need to the person on each run. | V3 X-002 | (a) does too, through the "or person" branch. V3 adds an agent doing the launch on the person's instruction. | Partial concede |
| 12 | V1 names only one weakness. | DA S-006 | Round 1 added four concessions. | Concede |
| 13 | V1 states no D4 dependency. | DA C-008 | (a) needs no D4 answer, but it is not free of authority rules. The coordinator runs monitor 3 only as a "Requested and authorized full loop" (`HWW:221`) and pushes only with approval (`HWW:215`). V1 should have said so. | Concede the omission; hold the point |
| 14 | V1 is silent on durability and resume. | DA C-010 | `--resume <run-log>` works the same way in (a) (`PRC:56`, `HWW:216`). | Concede |
| 15 | V1 is silent on what an app or session restart does. | DA A-005 | Losing the coordinator loses the monitor (`PRS:43`), exactly as for a worker or a tab. Recovery is the same run-log. | Concede (no difference) |
| 16 | Under (a), the session must be at the PR head checkout. | DA A-006 | Real friction. The coordinator must run from each change's worktree, or it halts with `pr_head_mismatch` (`PRC:28`). V2 and V3 sit there already. | Concede |

## Updated assessment of other variants

### Variant 2 (option b)
**Steelman after its Round 1 defence.** V2 corrected its D4 dependency: full strength needs D4 (a) only. It withdrew "rewrites that boundary" and grounded "attended" in the skill's own text (`PRS:43-45`, `PRS:83-84`). Its position is now "(a) as the default, (b) opt-in when the person's instruction names parallel PR monitoring" (V2 Concession 5). It is the only option that is both parallel and tracked, through Orca's supervised route (`[G] 37`).

**Revised view.** My main objection, that a worker breaks the attended boundary, does not survive the text (response 5). Three objections remain, and none depends on reading "headless" or "attended". (1) Monitor 3 works only under D4 (a). Under D4 (b) or (c) a worker never pushes (`SPEC:347`, `D4c:3`), and a monitor-2 ceiling against the repo's monitor-3 rule must be disclosed and execution withheld (`HWW:223`). (2) Its HALT advantage is smaller than claimed, because WC-3 turns most pr-submit HALTs into blocked contracts plus a new Task (response 8). (3) It is the only option with a build cost and unverified parts (`SPEC:276`, `SPEC:393-394`). (b) is now a legitimate later option, not a wrong one. It should wait until three things hold: tracked parallel monitoring is shown to be needed, D4 resolves to (a), and AC-4.3 passes.

### Variant 3 (option c)
**Steelman after its Round 1 defence.** V3 now presents itself as "(a) plus a person-requested parallel route" (V3 Position). It withdrew the overstated `CAPS:52` reading and accepted "do not monitor completion" (`[G] 39`): the coordinator reports the handle and stops (`[CLI] 29`). It moved its authority anchor from D4 to `HWW:221` and `HWW:215`, so the person must name each PR. That closes the gap I set as my Round 1 condition (my Concession 2, V1 Weakness 3 on V3).

**Revised view.** With those corrections, (c) is (a)'s "or person" branch with the coordinator doing the launch. The launched tab is an ordinary session, not a worker (`SPEC:53`, `[G] 41`), so pr-submit runs exactly as written. I no longer object to (c) in principle. Two limits remain. (1) It covers only a hand-off request. A person who asks the coordinator to "monitor" or "track completion" belongs on the coordinator route (`[G] 37`, `[CLI] 27`), meaning (a) run serially, or later (b). (2) Its launch path is unverified for this use. Whether `--prompt "/sc:pr-submit ..."` runs as a slash command in a Claude tab, and whether it runs when the launch opens a chat instead of a terminal (`[G] 43-45`, `[CLI] 63`), are both UNVERIFIED, and the guide's example uses `--agent codex` (`[CLI] 52`). A lost reply must be retried with `--retry-launch` (`[CLI] 65`); otherwise two monitors could run on one PR.

## New evidence

1. **WC-3 limits (b)'s HALT route.** `ask` is allowed only before any output exists except the blocked contract, and only when the answer fits an existing argument or flag (`SPEC:67`). pr-submit's HALTs happen mid-loop or need manual recovery (`PRC:28`, `PRC:85`), so under (b) they end as blocked contracts and a new Task (`SPEC:70`).
2. **Monitor 3 pushes without asking in every option** (`CLAUDE.md:50`). The real safety difference between the options is where a person can see and interrupt the loop, and who authorized it starting (`HWW:215`, `HWW:221`), not whether each push is approved. This narrows my own Round 1 claim.
3. **`CAPS:161` names pr-submit**: "Such a command can still be an Orca worker, because an Orca worker is a top-level Claude session". This supports V2 on technical fit.
4. **`SPEC:316` does not say the coordinator is the person's own session.** That is a correction to my Round 1 Strength 6. The coordinator role exists because the user explicitly asks for supervision (`[G] 37`). That is enough for the top-level rule.
5. **Wait sizing for (a)**: three kinds of wait (`PRS:51`), each up to 600 s by default (`PRC:49`), and 2 rounds by default with a cap of 5 (`PRC:47`).
6. **Orca routes a "monitor" request to the coordinator** (`[G] 37`). That bounds (c) to requests worded as a hand-off.

## Updated shared assumption responses

| A-NNN | Round 1 | Round 2 | Reason |
|---|---|---|---|
| A-004 | QUALIFY | ACCEPT the definition; QUALIFY the degree | `PRS:43-45` defines "attended" by contrast with a daemon: the loop is in a session and dies with it. On that definition a worker's terminal, a handoff tab and the coordinator are all attended (V2 and V3 both argued this). Where the person's attention actually sits still differs by degree: one session they direct, N tabs, or worker reports. That still favours (a) for a single PR. |

## Final per-point positions

| ID | Superior approach | Changed since R1? | One-line reason |
|---|---|---|---|
| S-001 | equal | no | Section layout does not affect the decision. |
| S-002 | equal | no | Each citation key fits its own claims. |
| S-003 | V1 | no | One session is the right default shape. V3's tabs are an acceptable extension of it for a person-requested hand-off. |
| S-004 | equal (V1, V3) | yes | Neither changes pr-submit; only V2 needs the section 3 row (`SPEC:137`). |
| S-005 | equal | yes | Being one of the spec's two options is not a merit in itself (V2 and V3 both argued this). |
| S-006 | V2 | no | Most candid about its own costs. |
| C-001 | equal | yes | All three keep the in-session, not-detached meaning of `PRS:43-45`. V2 needs only a one-line clarification of `PRC:85`. |
| C-002 | V1 | no (narrowed) | Monitor 3 pushes without asking everywhere (`CLAUDE.md:50`). (a) keeps the loop in the session the person directs and works under every D4 answer. |
| C-003 | equal (V1, V3) | yes | Both keep HALTs live in the session running the loop. Under V2, WC-3 makes them blocked contracts (`SPEC:67`, `SPEC:70`). |
| C-004 | V3 | no | Parallel with pr-submit unchanged. V2 is parallel and tracked but costs more and needs D4 (a). |
| C-005 | equal (V2, V3) | no | Both free the coordinator. (a) holds it for about 40 minutes at defaults (`PRS:51`, `PRC:47-49`). |
| C-006 | V2 | yes | For several PRs only `worker_done` plus a contract gives a structured result (`SPEC:137`). (a) has it only serially, V3 not at all. |
| C-007 | equal (V1, V3) | yes | Neither depends on the unverified poll runtime (`SPEC:394`) or on AC-4.3. |
| C-008 | V1 | no | Needs no D4 answer. Its authority comes from `HWW:215` and `HWW:221`, as V3's now does. |
| C-009 | equal (V1, V3) | yes | No cost versus one spec sentence; V2 needs the P4 row and AC-4.3. |
| C-010 | equal | no | `--resume` works the same in all three (`PRC:56`). |
| C-011 | equal | no | All meet `PRS:47-49`. |
| C-012 | equal | yes | One session suits one PR; one live tab per PR suits several. |
| C-013 | equal (V1, V3) | yes | Both can move to (b) later at unchanged cost. |
| X-001 | V2 | yes | The skill defines "attended" against detachment (`PRS:43-45`, `PRS:83-84`), and `CAPS:161` names pr-submit as worker-capable. |
| X-002 | equal | no | Unmeasured. V1's denial is withdrawn, and `SPEC:343` leaves the call to the person. |
| X-003 | equal (V1, V3) | yes | Both keep an operator at the HALT. V2's `ask` route is mostly closed by WC-3 (`SPEC:67`). |
| X-004 | equal (V1, V2) | yes | Both legitimately give the coordinator the result. V3 may not monitor completion (`[G] 39`). |
| X-005 | V1 | no | No extra authority question. V3 now uses the same `HWW:221` rule. |
| A-004 | V1 | no | All three are attended in the skill's sense. One session the person directs is easier to attend than N tabs or reports. |
| A-005 | equal | no | Losing the session loses the monitor everywhere, and the run-log restores it. |
| A-006 | equal (V2, V3) | no | Each already sits in the PR's worktree. (a) must run from each PR head checkout (`PRC:28`). |

## Overall recommendation

Keep (a) as D3's answer and the default: the coordinator, or the person, runs `/sc:pr-submit --monitor 3` from the change's worktree once the workers finish, with no Phase 4 change to pr-submit. Add one sentence to D3 adopting (c) as the parallel route. When the person explicitly asks to hand off several PRs and names each one (`HWW:215`, `HWW:221`), the coordinator launches one person-owned agent tab per PR with `agent launch`. It creates no Task and does not track completion (`[G] 39`). This route is used only after a smoke test shows that a Claude tab runs the slash command from `--prompt`. Record (b) as a later option rather than a rejected one. The "attended" objection no longer blocks it, but it should be adopted only when tracked parallel monitoring is shown to be needed, D4 resolves to (a), and AC-4.3 passes. Until then it is the most expensive option and the most conditional.

### Variant 2 Rebuttal
<!-- Verbatim copy of `rounds/r2-variant-2.md` (heading levels as in the source file). -->

# D3 Round 2: rebuttal from the Variant 2 advocate (option b, worker with pre-authorization)

Citation keys as in Round 1: `SPEC:N` = `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md:N`; `PRC:N` = `src/superclaude/commands/pr-submit.md:N`; `PRS:N` = `src/superclaude/skills/sc-pr-submit-protocol/SKILL.md:N`; `HWW:N` = `src/superclaude/core/HOW-WE-WORK.md:N`; `CAPS:N` = `.dev/orca-command-refactor/inventory/orca-capabilities.md:N`; `D4c:N` = `.dev/orca-command-refactor/decisions/D4/option-c.md:N`; `[CLI] N` / `[G] N` = line N of `orca-ide skills get orca-cli` / `orca-ide skills get orchestration`; `DA` = `diff-analysis.md`. Every citation below was re-read on 2026-11-02.

## Responses to criticisms

| # | Criticism | Source | Response | Concede / hold |
|---|---|---|---|---|
| 1 | A pr-submit worker removes the attending person the command assumes; V2 must rewrite "Will Not: run headless" or empty the word "attended". | V1 R1 W1; V3 R1 W4; DA X-001 | Withdrawn in my Round 1 and now accepted by V1 (V1 R2 response 5). The skill defines "attended" against detachment: "closing the session loses it ... never from detachment ... Do NOT imply a background daemon" (`PRS:43-45`); "Never hand a side effect to a background shell, detached loop, or subagent" (`PRS:83-84`). A worker is a top-level interactive session (`CAPS:161` names pr-submit). What remains is a one-line clarification of `PRC:85`. | Hold (V1 concurs) |
| 2 | V2 misstated its D4 dependency as "D4 (a) or (c)". | DA spot-check 6; V1 R1 W2; V3 R1 W2 | Correct; conceded in Round 1. Full strength needs D4 (a) only: D4 (c) forbids any worker push or PR (`D4c:3`), D4 (b) forbids all outward changes (`SPEC:347`). | Concede (unchanged) |
| 3 | Under D4 (b) or (c), a monitor-2 worker conflicts with the monitor-3 rule, and the guide says to withhold execution. | V1 R1 W2; V1 R2 view (1) | Stronger than my Round 1 Concession 1 allowed. `HWW:223`: "if that conflicts with the requested lower ceiling, disclose the policy conflict and withhold execution". The PR must still be opened by `/sc:pr-submit --monitor 3` (`CLAUDE.md:50`), and that run already holds the loop, which is option (a). So outside D4 (a), (b) has no role; my "(a) or a narrow (b) is close to even" is withdrawn. | Concede |
| 4 | Under (b) an operator HALT becomes a blocked contract plus a new Task; my Round 1 claim that HALTs "wait in place" via `ask`/`escalation` is closed by WC-3. | V1 R1 W4; V3 R1 W1; V1 R2 response 8 | V1 is right. WC-3 allows `ask` only at a gate "that fires before the command has written any output except its blocked contract and whose answer fits an existing argument or flag" (`SPEC:67`); WC-2 then stops the command (`SPEC:66`). pr-submit's HALTs need hands in the worktree (checkout, separating files) and fire mid-loop (`PRS:268`, `PRS:274`), so neither condition holds. The row's "the worker may use `ask` or `escalation`" (`SPEC:137`) contradicts WC-3, and I relied on the row. Partial counter: in every option these HALTs end the run as `terminal_halted` and say "re-run with `--pr <N>`" (`PRS:268`, `PRS:274`), so nothing waits in place under (a) or (c) either. The real gap is one hop: the message lands in a contract the coordinator reads, not in the person's session. | Concede the claim; hold that the gap is one routing hop |
| 5 | At monitor 3 the worker pushes with nobody watching; `PRC:85` guards limit which commit is pushed, not whether the fix is right. | V1 R1 W3; DA C-002 | V1 has since agreed that monitor 3 "pushes the fixes without asking" in every option (`CLAUDE.md:50`; V1 R2 new evidence 2). What (b) loses is live interruption in the session the person already directs. Orca recognises user-taken-over worker terminals (`CAPS:109`), but nothing makes a person look. | Concede the narrower point |
| 6 | (b) carries the highest cost and the only unverified parts: P4 row, AC-4.3, poll runtime, Dispatch runtime. | V1 R1 W5; V3 R1 W4; DA C-009 | True: `SPEC:137`, `SPEC:185`, `SPEC:276`, UNVERIFIED items 11-12 (`SPEC:393-394`). | Concede |
| 7 | (b) drops a valid ceiling: `--monitor 1` is refused under `--unattended`, though `HWW:219` lists it. | V3 R1 W3 | Monitor 1 exists to "PROPOSE 'fix these? y/n'" (`PRS:272`), a question only a person answers, and the spec refuses every person-mode flag the same way (`SPEC:56`). A person keeps monitor 1 in their own session (SA-1, `SPEC:169`). | Hold |
| 8 | Orca's "monitor ... track completion" row (`[G] 37`) does not require a separate worker; (a) is on that route too. | V1 R2 response 6 | Correct for one PR: the coordinator holding the loop is the `[G] 37` role. My claim narrows to: (b) is the only option that is both parallel and on that route. | Partial concede |
| 9 | V2's original said nothing on reversibility. | DA C-013 | Fair. (b) is additive under SA-1 (`SPEC:169`); choosing (a) now leaves (b) available later at the same cost, as V1 and V3 say. | Concede |
| 10 | Only (b) adds an unknown bound on a Dispatch's total run time. | V1 R1 A-005 | True (`SPEC:393`). It cancels my Round 1 claim that Task records make (b) "best placed" for resume. | Concede |
| 11 | Original V2's "already fits a worker" contradicts its own "either rewrites that boundary". | DA X-001; V3 R1 W4 | Resolved by withdrawing the second phrase in Round 1 (row 1). | Concede the original; hold the current position |

## Updated assessment of other variants

### Variant 1 (option a)
**Steelman after its rebuttal.** V1 dropped its unsourced "rarely needed" claim and its headless reading, sized its own weakness at roughly four waits of up to 600 s at defaults (`PRS:51`, `PRC:47-49`), and narrowed its safety claim to where a person can see and interrupt the loop. It works under every D4 answer, needs nothing built, and sits on Orca's coordinator route (`[G] 37`).

**Revised view.** Rows 3 and 4 remove the two things I said (b) did better apart from parallel monitoring. (a) is the right default. Its remaining costs, a held coordinator when other work overlaps and the need to run from each PR's head checkout (`PRC:28`), bite only with several PRs.

### Variant 3 (option c)
**Steelman after Round 1.** V3 now presents itself as a person-requested hand-off beside (a): the coordinator launches one tab per named PR (`[CLI] 49-52`), reports the handle and stops (`[CLI] 29`), with authority from `HWW:215` and `HWW:221` rather than D4. pr-submit runs unchanged under every D4 answer.

**Revised view.** I withdraw my Round 1 objection that it uses the hand-off route for what that route forbids: corrected, it does not monitor completion, as `[G] 39` requires. Two limits remain. It fits only when the person words the request as a hand-off; "monitor" or "track completion" belongs on the coordinator route (`[G] 37`, `[CLI] 27`). And its launch is unverified for this use (a `--prompt` slash command in a Claude tab; a launch that may open a chat instead of a terminal, `[G] 43-45`). For parallel monitoring without a completion signal, (c) is cheaper and safer than (b).

## New evidence

1. **pr-submit's operator HALTs end the run in every option.** The head-mismatch, fix-commit and push-range HALTs set `terminal_halted` and tell the operator to fix the checkout and "re-run with `--pr <N>`" (`PRS:268`, `PRS:274`). No option keeps a HALT "waiting"; they differ only in where the message lands and who runs the re-run.
2. **The spec contradicts itself on pr-submit HALTs.** The row says "operator HALTs resolve as blocked (the worker may use `ask` or `escalation`)" (`SPEC:137`); WC-3 allows `ask` only before any output and only when the answer fits an existing argument or flag (`SPEC:67`). Whatever D3 decides, the row should drop "`ask`", and under (b) the blocked contract should carry the HALT's recovery text in `blocked_question`.
3. **Outside D4 (a), (b) cannot run at all.** A monitor-2 ceiling against the monitor-3 rule means "disclose the policy conflict and withhold execution" (`HWW:223`; `CLAUDE.md:50`), and the PR-opening run is then the coordinator's own, which is option (a).
4. **`[G] 37` assigns "monitor ... track completion" to the coordinator role**, not to a worker. A worker is needed only for parallel tracked runs.
5. **Orca recognises user-taken-over worker terminals** (`CAPS:109`), so a person can enter a worker's terminal, but under WC-2 the command has already stopped at a HALT (`SPEC:66`), so this does not restore in-place handling.

## Updated shared assumption responses

| A-NNN | Round 1 | Round 2 | Reason |
|---|---|---|---|
| A-004 | QUALIFY | ACCEPT the definition; QUALIFY the degree, now favouring (a) | All three are attended in the `PRS:43-45` sense. Where attention actually sits differs: one session the person directs beats N tabs or N contracts for noticing a HALT. |
| A-005 | QUALIFY ("(b) best placed") | QUALIFY (no option better placed) | `--resume <run-log>` recovers every option the same way (`PRC:56`). The Task record helps the coordinator find the run-log, but (b) alone carries the unknown Dispatch run-time bound (`SPEC:393`); the two cancel out. |

## Final per-point positions

| ID | Superior approach | Changed since R1? | One-line reason |
|---|---|---|---|
| S-001 | equal | no | Section layout does not affect the decision. |
| S-002 | equal | yes | Each citation key fits its own claims; V2 added `HWW` and `CLAUDE.md` in Round 1. |
| S-003 | V1 | yes | One session is the right default shape; (b)'s topology works only under D4 (a) (`HWW:223`). |
| S-004 | equal (V1, V3) | yes | Neither changes pr-submit; only V2 needs the section 3 row (`SPEC:137`). |
| S-005 | equal | no | Being a listed spec option is not a merit in itself. |
| S-006 | V2 | no | States its own costs most fully. |
| C-001 | equal | yes | All three keep the in-session, not-detached meaning of `PRS:43-45`; V2 needs only a one-line `PRC:85` clarification. |
| C-002 | V1 | no | Monitor 3 pushes without asking everywhere (`CLAUDE.md:50`); (a) keeps it in the session the person directs, under every D4 answer. |
| C-003 | equal (V1, V3) | yes | WC-3 turns pr-submit HALTs into blocked contracts under (b) (`SPEC:67`); the gap is one routing hop (`PRS:268`, `PRS:274`). |
| C-004 | V3 | yes | Parallel with pr-submit unchanged and under every D4 answer; V2 is parallel and tracked but needs D4 (a) and the P4 build. |
| C-005 | equal (V2, V3) | no | Both free the coordinator; (a) holds it for each wait (`PRC:47-49`). |
| C-006 | V2 | no | Only `worker_done` plus a contract gives a structured result for several PRs (`SPEC:137`). |
| C-007 | equal (V1, V3) | yes | Avoiding the unverified poll runtime (`SPEC:394`) beats having to prove it in AC-4.3. |
| C-008 | V1 | no | Needs no D4 answer; authority from `HWW:215` and `HWW:221`. |
| C-009 | equal (V1, V3) | yes | Nothing or one spec sentence, versus the P4 row and AC-4.3 (`SPEC:276`). |
| C-010 | equal | yes | `--resume` works the same everywhere (`PRC:56`); the Task record is offset by `SPEC:393`. |
| C-011 | equal | no | All meet `PRS:47-49`. |
| C-012 | equal | no | One session suits one PR; tabs or contracts suit several. |
| C-013 | equal (V1, V3) | yes | Both leave (b) available later at unchanged cost; (b) is additive under SA-1. |
| X-001 | V2 | no | "Attended" is defined against detachment (`PRS:43-45`, `PRS:83-84`); `CAPS:161` names pr-submit as worker-capable. V1 concurs. |
| X-002 | equal | yes | The need is unmeasured either way; `SPEC:343` leaves it to the person. |
| X-003 | equal (V1, V3) | yes | Both put the HALT message in the session running the loop; under (b) WC-3 makes it a blocked contract (`SPEC:67`). |
| X-004 | equal (V1, V2) | yes | Both legitimately give the coordinator the result; V3 may not monitor completion (`[G] 39`). |
| X-005 | V1 | yes | No extra authority question; V3 now uses the same `HWW:221` rule, and V2 depends on D4 (a). |
| A-001 | equal | yes | All three now argue "attended", not "headless" (`SPEC:391`). |
| A-004 | V1 | yes | One directed session is easier to attend than N tabs or contracts. |
| A-005 | equal | yes | Same run-log recovery everywhere; (b)'s Task record is offset by `SPEC:393`. |
| A-006 | equal (V2, V3) | yes | Each sits in the PR's worktree at its head; (a) must run from each PR head checkout (`PRC:28`). |

## Overall recommendation

I move to V1's recommendation, with one condition added. Keep (a) as D3's answer and default: the coordinator or person runs `/sc:pr-submit --monitor 3` from the change's worktree, with no Phase 4 change to pr-submit. Adopt (c) as the person-requested parallel hand-off, only after a smoke test shows a Claude tab runs the slash command from `--prompt`. Record (b) as deferred, not rejected: the attended objection no longer applies, but (b) can run only under D4 (a) (`HWW:223`), its HALT route is one hop slower (`SPEC:67`), and it carries the only build cost and unverified parts (`SPEC:276`, `SPEC:393-394`). Adopt it only when the person needs parallel monitoring with tracked completion, D4 resolves to (a), and AC-4.3 passes. Whatever D3 decides, fix the `SPEC:137` row's "`ask` or `escalation`" wording to match WC-3.

### Variant 3 Rebuttal
<!-- Verbatim copy of `rounds/r2-variant-3.md` (heading levels as in the source file). -->

# D3 Round 2: rebuttal from the Variant 3 advocate (option c, unsupervised handoff to a person-owned agent tab)

Citation keys as in Round 1: `SPEC:N` = `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md:N`; `PRC:N` = `src/superclaude/commands/pr-submit.md:N`; `PRS:N` = `src/superclaude/skills/sc-pr-submit-protocol/SKILL.md:N`; `HWW:N` = `src/superclaude/core/HOW-WE-WORK.md:N`; `CAPS:N` = `.dev/orca-command-refactor/inventory/orca-capabilities.md:N`; `EVD:N` = `.dev/evals/ccsession-orca-e2e-20261026/EVIDENCE.md:N`; `D4c:N` = `.dev/orca-command-refactor/decisions/D4/option-c.md:N`; `[CLI] N` / `[G] N` = line N of `orca-ide skills get orca-cli` / `orca-ide skills get orchestration` (1.4.237); `DA` = `diff-analysis.md`. Every citation below was re-read on 2026-11-02.

## Responses to criticisms

| # | Criticism | Source | Response | Concede / hold |
|---|---|---|---|---|
| 1 | V3 uses the hand-off route for what it forbids: the coordinator "reads the run-log later", but the route says "do not monitor completion" and excludes "monitor, wait for results, track completion". | V1 R1 W1; V2 R1 W1; DA X-004, spot-check 3 | Conceded in Round 1 and kept. The coordinator reports the worktree id and agent handle once the prompt is delivered, then stops (`[CLI] 29`); it creates no Task (`[CLI] 31`) and does not monitor completion (`[G] 39`). It reads a run-log only on a later, separate instruction. V1 and V2 both withdrew this objection in Round 2. | Concede the original; hold the corrected form |
| 2 | The coordinator gets no completion signal; with N tabs the person polls each by eye. | V2 R1 W2; DA C-006 | True, and it is the price of the route. If the person wants outcomes tracked across several PRs, (b) is the only parallel option that gives them, and (a) gives them serially. | Concede |
| 3 | `CAPS:52` "no time limit" was overstated; it is a startup limit, a waiting worker is also "healthy", and a coordinator-launched tab is not shown to be "a person's own launch tab". | DA spot-check 4; V1 R1 W2; V2 R1 W4 | Withdrawn in Round 1. Further: pr-submit's operator HALTs do not wait at all. They end the run with `terminal_halted` and tell the operator to fix the checkout and "re-run with `--pr <N>`" (`PRS:268`, `PRS:274`). So (c)'s HALT advantage over (b) is only where the recovery text lands: in the tab that holds the run's scrollback, as under (a), not in a blocked contract one hop away (WC-2, WC-6 at `SPEC:66`, `SPEC:70`). | Concede the claim; hold the narrower point |
| 4 | Authorization has no anchor: D4 covers "a worker's outward actions" (`SPEC:345`), and a tab is not a worker. | V1 R1 W3; DA X-005 | Re-anchored in Round 1 to the routing guide: monitor 3 only as a "Requested and authorized full loop" (`HWW:221`), "Push only with approval" (`HWW:215`). That is the same rule (a)'s coordinator runs under (V1 R2 response 13). The tab is an ordinary session, not a worker: no Task/Dispatch preamble (`SPEC:53`; `[G] 41`). V1 accepted this as closing its condition. | Concede the original; hold the re-anchored form |
| 5 | "Attended" in name only: N visible tabs, nobody shown watching, each pushing without asking. | V1 R1 W4; DA A-004 | Partly conceded in Round 1 (one session beats N tabs for noticing a HALT). New fact: in the recorded Orca runs every Claude started with `--dangerously-skip-permissions` (`EVD:15`), so no option there has a per-push prompt; monitor 3 "pushes the fixes without asking" everywhere (`CLAUDE.md:50`). The real difference is where the person can see and interrupt the loop. | Concede the degree |
| 6 | V3 adds little beyond (a): a person can open N tabs themselves; V3 only lets an agent do the typing, which moves the start away from a person. | V1 R1 W5 | Concede the value is convenience, not a new capability: the coordinator already knows each change's worktree id and branch and assembles the exact command. Hold that the start does not move: the coordinator launches only the PRs the person's instruction names (`HWW:215`, `HWW:221`), and the tab's prompt is that exact command. V1 R2 now describes (c) as (a)'s "or person" branch with the coordinator launching, which is how I framed it. | Partial concede |
| 7 | The guide's `agent launch` example uses `--agent codex`; whether `--prompt "/sc:pr-submit ..."` runs as a slash command is UNVERIFIED. | V1 R1 W5, R2 limit (2); V2 R1 W4; DA spot-check 2 | Narrowed by evidence, not closed. `orca worktree create --agent claude`, which uses the same agent launch as `agent launch` (`[CLI] 63`), started Claude in a new worktree (`EVD:27`), and an agent-tab prompt reached Claude as the last argv element "byte for byte" and was answered (`EVD:23`; `CAPS:47`, `promptInjectionMode: 'argv'`). Still UNVERIFIED: whether Claude treats an argv prompt beginning with `/` as a slash command. A smoke test must settle it before use. | Concede (narrowed) |
| 8 | The launch may open a chat rather than a terminal, and whether the slash command runs there is UNVERIFIED. | V1 R2 limit (2); V2 R2 view | Correct. The person's Chat UI setting decides the surface; `--surface terminal` is passed "only when the user asked" (`[CLI] 63`; `[G] 43-45`). All evidence above was on terminal tabs. The smoke test must use the person's actual setting, or the person's instruction asks for terminal tabs. | Concede |
| 9 | A lost launch reply, retried as a fresh launch, could start two monitors on one PR. | V1 R2 limit (2) | Correct and procedural: retry only with `--retry-launch <operationId>`; if replay is unknown, inspect before relaunching (`[CLI] 65`). The D3 sentence should say so. | Concede |
| 10 | (c) fits only a request worded as a hand-off; "monitor" or "track completion" belongs on the coordinator route. | V1 R2 limit (1); V2 R2 view | Correct (`[G] 37`, `[CLI] 27`). A person who asks to have several PRs monitored and be told when each is done gets (a) serially today, or (b) later. Hold that this is a routing condition, not a defect: the D3 sentence must name the trigger (the person asks for one tab per named PR and accepts no completion tracking). | Concede the limit |
| 11 | Same authority problem as a worker's, with less record: the tab's only instruction is the coordinator's prompt, while a worker brief quotes the user. | V2 R1 W3 | Partly. The tab's prompt is the exact pr-submit invocation, and the run writes its own run-log (`PRC:55`). But nothing in the tab quotes the person's instruction. Fix: the coordinator records the instruction beside the handles in its hand-off report. | Partial concede |
| 12 | V3 is outside the spec's a/b option set. | DA S-005 | Not a defect; all three advocates now rate S-005 equal. | Hold |

## Updated assessment of other variants

### Variant 1 (option a)
**Steelman after its rebuttal.** V1 withdrew its unsourced "rarely needed" claim and its headless reading, sized its weakness (about four waits of up to 600 s at defaults, `PRS:51`, `PRC:47-49`), and narrowed its safety claim to where a person can see and interrupt the loop. It needs nothing built, works under every D4 answer, and sits on Orca's coordinator route (`[G] 37`). It now adopts (c) as its parallel extension.

**Revised view.** I agree (a) is the right default and I said so in Round 1 (my Concession 2). My remaining reservation is small: (a)'s coordinator must run from each PR's head checkout or it halts with `pr_head_mismatch` (`PRS:268`), which (c) avoids by launching in the change's own worktree. That is friction, not a reason to change the default.

### Variant 2 (option b)
**Steelman after its rebuttal.** V2 is the only option that is parallel and tracked through Orca's supervised route; its "attended" reading is grounded in the skill's own text (`PRS:43-45`, `PRS:83-84`), and `CAPS:161` names pr-submit as worker-capable. It also found a real spec defect: the `SPEC:137` row's "`ask` or `escalation`" contradicts WC-3 (`SPEC:67`).

**Revised view.** I withdraw my Round 1 claim that a worker does not fit the attended boundary; V2 and now V1 are right on X-001. My two other Round 1 objections stand and V2 has conceded both: outside D4 (a) a worker cannot run the mandated monitor 3 (`D4c:3`, `SPEC:347`, `HWW:223`), and it carries the only build cost and unverified runtime (`SPEC:276`, `SPEC:393-394`). I also withdraw "it drops a ceiling" (my R1 W3): V2 is right that monitor 1's y/n proposal needs a person (`PRS:272`), who keeps it in their own session. (b) is a legitimate deferred option, not a rejected one.

## New evidence

1. **The Claude launch path is mostly proven.** An Orca agent tab passed the prompt to Claude as the last argv element "byte for byte" and Claude answered it (`EVD:23`); `orca worktree create --agent claude` started Claude in a new worktree (`EVD:27`), through the same agent launch `agent launch` uses (`[CLI] 63`). Only a leading-`/` prompt and the chat surface remain UNVERIFIED.
2. **No per-push permission prompt in the recorded setup.** In the recorded Orca runs every Claude went through the ccsession wrapper, whose argv "always started with ... `--dangerously-skip-permissions`" (`EVD:15`); whether every host is configured so is UNVERIFIED. Safety in all three options rests on who authorized monitor 3 (`HWW:215`, `HWW:221`) and on where the loop is visible, which supports V1's R2 new evidence 2.
3. **Operator HALTs end the run in every option** (`PRS:268`, `PRS:274`), confirming V2's R2 new evidence 1. My Round 1 Strength 3 narrows to "the recovery text lands in the session holding the run".
4. **The launched tab is an ordinary session by the spec's own definition**: only a session with a Task and Dispatch preamble is a worker run (`SPEC:53`; `[G] 41`). So (c) needs no `--unattended` mode and no D4 answer.
5. **Surface and retry are explicit launch controls**: `--surface terminal` exists but is passed only on the user's request (`[CLI] 63`); a lost reply is retried with `--retry-launch <operationId>` (`[CLI] 65`). Both belong in the D3 sentence.

## Updated shared assumption responses

| A-NNN | Round 1 | Round 2 | Reason |
|---|---|---|---|
| A-004 | QUALIFY | ACCEPT the definition; QUALIFY the degree | `PRS:43-45` and `PRS:83-84` define "attended" against detachment, so a worker terminal is attended too; that removes my Round 1 Strength 1 as a reason to prefer (c) over (b). Attention still differs by degree: one directed session beats N tabs or N contracts for noticing a HALT, favouring (a) for one PR. |

## Final per-point positions

| ID | Superior approach | Changed since R1? | One-line reason |
|---|---|---|---|
| S-001 | equal | no | Section layout does not affect the decision. |
| S-002 | equal | no | Each citation key fits its own claims. |
| S-003 | V1 | yes | One session is the right default shape; V3's tabs are an extension of it for a person-requested hand-off, not a rival. |
| S-004 | equal (V1, V3) | no | Neither changes pr-submit; only V2 needs the section 3 row (`SPEC:137`). |
| S-005 | equal | no | Being a listed spec option is not a merit in itself. |
| S-006 | V2 | yes | V2 states its own costs most fully (L1; conceded). |
| C-001 | equal | yes | All three keep the in-session, not-detached meaning of `PRS:43-45`; V2 needs only a one-line `PRC:85` clarification. |
| C-002 | V1 | no | Monitor 3 pushes without asking everywhere (`CLAUDE.md:50`); (a) keeps the loop in the session the person directs. |
| C-003 | equal (V1, V3) | no | HALTs end the run everywhere (`PRS:268`, `PRS:274`); V1 and V3 put the recovery text in the session holding the run, V2 in a contract (`SPEC:66-67`). |
| C-004 | V3 | no | Parallel with pr-submit unchanged and under every D4 answer; V2 needs D4 (a) and the P4 build. |
| C-005 | equal (V2, V3) | no | Both free the coordinator; (a) holds it for each wait (`PRC:47-49`). |
| C-006 | V2 | no | Only `worker_done` plus a contract gives a structured result for several PRs; V3 may not track one (`[G] 39`). |
| C-007 | equal (V1, V3) | no | Neither depends on the unverified poll runtime (`SPEC:394`) or AC-4.3. |
| C-008 | V1 | no | No extra authority step; V3 uses the same `HWW:215`/`HWW:221` rule plus a named-PR instruction. |
| C-009 | equal (V1, V3) | no | Nothing or one spec sentence, versus the P4 row and AC-4.3 (`SPEC:276`). |
| C-010 | equal | no | `--resume` works the same everywhere (`PRC:56`). |
| C-011 | equal | no | All meet `PRS:47-49`. |
| C-012 | equal | yes | One session suits one PR; one live tab per PR suits several. |
| C-013 | equal (V1, V3) | no | Both leave (b) available later at unchanged cost. |
| X-001 | V2 | yes | "Attended" is defined against detachment (`PRS:43-45`, `PRS:83-84`); `CAPS:161` names pr-submit as worker-capable. |
| X-002 | equal | yes | Unmeasured; all three now leave the call to the person per run (`SPEC:343`). |
| X-003 | equal (V1, V3) | no | Both put the operator at the HALT text; under V2 it becomes a blocked contract (`SPEC:67`). |
| X-004 | equal (V1, V2) | yes | Both legitimately give the coordinator the result; V3 may not monitor completion (`[G] 39`). |
| X-005 | V1 | no | No extra authority question; V3 now uses the same `HWW:221` rule. |
| A-001 | equal | no | All three argue "attended", not "headless" (`SPEC:391`). |
| A-004 | V1 | no | One directed session is easier to attend than N tabs or contracts. |
| A-005 | equal | no | Same run-log plus `--resume` recovery everywhere (`PRC:56`). |
| A-006 | equal (V2, V3) | no | Each sits in the PR's worktree at its head; (a) must run from each PR head checkout (`PRS:268`). |

## Overall recommendation

I converge with V1 and V2. Keep (a) as D3's answer and default: the coordinator or the person runs `/sc:pr-submit --monitor 3` from the change's worktree after the workers finish, with no Phase 4 change to pr-submit. Add one sentence adopting (c) as the parallel route, with its conditions stated: it applies only when the person asks for one agent tab per named PR and accepts no completion tracking; authority comes from `HWW:215` and `HWW:221`, and the coordinator records the person's instruction beside each reported worktree id and handle, then stops (`[CLI] 29`, `[G] 39`); a lost launch reply is retried only with `--retry-launch` (`[CLI] 65`); and the route is enabled only after a smoke test shows a Claude tab, on the person's actual chat-or-terminal setting, runs `/sc:pr-submit` from `--prompt`. Record (b) as deferred, not rejected: it is the only option for tracked parallel monitoring, but it needs D4 (a), AC-4.3 and the P4 build. Whatever D3 decides, fix the `SPEC:137` row's "`ask` or `escalation`" wording to match WC-3 (`SPEC:67`).

## Round 2.5: Invariant Probe

Full table in `invariant-probe.md` (fault-finder, not an advocate). Summary of that file:

- 23 findings: ADDRESSED 7, UNADDRESSED 16 (HIGH 4, MEDIUM 7, LOW 5).
- HIGH and UNADDRESSED: INV-006 (the (a) sentence lacks the "requested and authorized" guard of `HWW:215` / `HWW:221`), INV-012 (nothing ensures one live monitor per PR), INV-017 (pr-submit never pushes the head branch, so (a) and (c) depend on D4 through the pre-PR commit and push), INV-023 (the consensus is necessary but not sufficient: 7 of 10 enumerated gates between "workers finish" and "a monitored loop is running" are not shown to pass for at least one route).
- MEDIUM and UNADDRESSED: INV-001, INV-002, INV-007, INV-008, INV-014, INV-015, INV-018.
- LOW and UNADDRESSED: INV-004, INV-005, INV-009, INV-011, INV-013.
- The probe's closing note: each HIGH item "can be closed by wording in the D3 sentence rather than a change of option".

## Round 3: Final Arguments

Not run. Depth is standard, so the debate stops after Round 2 (and the Round 2.5 probe). Round 3 runs only at depth deep.

## Scoring Matrix

Positions are each advocate's Round 2 "Final per-point positions" (A1 = Variant 1 advocate, A2 = Variant 2 advocate, A3 = Variant 3 advocate). "R1" shows whether the same point already had a 2-of-3 answer in Round 1. Confidence calibration (protocol "Per-Point Scoring Matrix"): unanimous 90-99%, majority 60-89%, split 50%; within the unanimous band, higher when the answer was already unanimous in Round 1, lower when it was reached only in Round 2 through a concession, and lower again when the invariant probe found a caveat in the supporting evidence. No point is given 100%.

| Diff Point | Level | A1 / A2 / A3 (Round 2) | R1 | Winner | Confidence | Evidence Summary |
|---|---|---|---|---|---|---|
| S-001 | L1 | equal / equal / equal | agreed (equal) | equal (no winner) | 98% | Section layout does not affect the decision; all three said so in both rounds. |
| S-002 | L1 | equal / equal / equal | agreed (equal) | equal (no winner) | 95% | Each citation key fits its own claims; A2 moved from V3 to equal in Round 2. |
| S-003 | L2 | V1 / V1 / V1 | split (V1 / V2 / V3) | Variant 1 | 93% | One session is the right default shape; A2 conceded (b)'s topology works only under D4 (a) (`HWW:223`) and A3 recast its tabs as an extension of (a). |
| S-004 | L2 | equal (V1, V3) ×3 | agreed (V1) | Variant 1 = Variant 3 | 95% | Neither (a) nor (c) changes pr-submit; only (b) needs the `SPEC:137` row, summary file and AC-4.3. |
| S-005 | L2 | equal / equal / equal | agreed (equal) | equal (no winner) | 95% | Being one of the spec's listed options is not a merit in itself; A1 dropped its Round 1 claim. |
| S-006 | L1 | V2 / V2 / V2 | agreed (V2) | Variant 2 | 96% | V2 states its own costs most fully; A3 moved from equal to V2. |
| C-001 | L3 | equal / equal / equal | split | equal (no winner) | 92% | All three keep the in-session, not-detached meaning of "attended" (`PRS:43-45`, `PRS:83-84`); A1 conceded its "headless" reading (A-001). |
| C-002 | L3 | V1 / V1 / V1 | agreed (V1) | Variant 1 | 97% | Monitor 3 pushes without asking in every option (`CLAUDE.md:50`), so the difference is that (a) keeps the loop in the session the person directs. |
| C-003 | L3 | equal (V1, V3) ×3 | split | Variant 1 = Variant 3 | 94% | Operator HALTs end the run with `terminal_halted` everywhere (`PRS:268`, `PRS:274`); (a) and (c) put the recovery text in the session holding the run, (b) in a blocked contract under WC-3 (`SPEC:67`). A2 conceded (R2-V2 #4). |
| C-004 | L2 | V3 / V3 / V3 | agreed (V3) | Variant 3 | 95% | (c) gives parallel monitoring with pr-submit unchanged and no build; A2 conceded (b) is parallel and tracked but needs D4 (a) and the P4 build. |
| C-005 | L3 | equal (V2, V3) ×3 | split (wording only) | Variant 2 = Variant 3 | 96% | Both free the coordinator; (a) holds it for each wait (`PRC:47-49`), which A1 conceded and sized. |
| C-006 | L3 | V2 / V2 / V2 | agreed (V2) | Variant 2 | 97% | Only `worker_done` plus a contract gives a structured result for several PRs (`SPEC:137`); A3 conceded (c) may not track completion (`[G] 39`). |
| C-007 | L3 | equal (V1, V3) ×3 | split | Variant 1 = Variant 3 | 93% | Neither depends on the UNVERIFIED poll-iteration runtime (`SPEC:394`) or AC-4.3; A2 conceded avoiding it beats having to prove it. |
| C-008 | L2 | V1 / V1 / V1 | agreed (V1) | Variant 1 | 90% | (a) needs no D4 answer for pr-submit's own pushes; authority comes from `HWW:215` / `HWW:221`. Caveat: INV-017 shows (a) and (c) still depend on D4 through the pre-PR commit and branch push, which weakens the shared premise "needs no D4 answer". |
| C-009 | L2 | equal (V1, V3) ×3 | agreed (V1) | Variant 1 = Variant 3 | 96% | Nothing or one spec sentence, versus the P4 row and AC-4.3 (`SPEC:276`). |
| C-010 | L3 | equal / equal / equal | agreed (equal) | equal (no winner) | 93% | `--resume <run-log>` recovers every option the same way (`PRC:56`); A2 withdrew "(b) best placed". Caveat: INV-002, the default run-log lives inside the worktree. |
| C-011 | L2 | equal / equal / equal | agreed (equal) | equal (no winner) | 98% | All three meet the top-level rule (`PRS:47-49`). |
| C-012 | L2 | equal / equal / equal | split | equal (no winner) | 92% | One session suits one PR; one live tab or one contract per PR suits several. |
| C-013 | L2 | equal (V1, V3) ×3 | agreed (V1) | Variant 1 = Variant 3 | 95% | Both leave (b) available later at unchanged cost; A2 conceded V2 had not stated reversibility (R2-V2 #9). |
| X-001 | L3 | V2 / V2 / V2 | split | Variant 2 | 95% | "Attended" is defined against detachment (`PRS:43-45`, `PRS:83-84`) and `CAPS:161` names pr-submit as worker-capable; A1 (R2-V1 #5) and A3 (R2-V3 revised view) conceded. |
| X-002 | L2 | equal / equal / equal | split | equal (no winner) | 92% | The need for parallel PR monitoring is unmeasured either way; A1 withdrew its unsourced "rarely needed" and `SPEC:343` leaves the call to the person. |
| X-003 | L3 | equal (V1, V3) ×3 | split | Variant 1 = Variant 3 | 94% | Both put the operator at the HALT text in the session running the loop; under (b) WC-3 makes it a blocked contract (`SPEC:67`). A2 conceded. |
| X-004 | L3 | equal (V1, V2) ×3 | agreed (V2) | Variant 1 = Variant 2 | 97% | Both legitimately give the coordinator the result; the handoff route says "do not monitor completion" (`[G] 39`), which A3 conceded in Round 1. |
| X-005 | L2 | V1 / V1 / V1 | agreed (V1) | Variant 1 | 92% | (a) raises no extra authority question; A3 moved (c)'s authority from D4 to `HWW:215` / `HWW:221`. Caveat: INV-017 (pre-PR push still couples D3 to D4). |
| A-004 | L3 | V1 / V1 / V1 | agreed (V1) | Variant 1 | 95% | All three are attended in the `PRS:43-45` sense, but one session the person directs is easier to attend than N tabs or N contracts. |
| A-005 | L3 | equal / equal / equal | agreed (equal) | equal (no winner) | 93% | Losing the session loses the monitor everywhere and the run-log restores it; (b)'s Task record is offset by the unknown Dispatch run-time bound (`SPEC:393`). Caveat: INV-002. |
| A-006 | L2 | equal (V2, V3) ×3 | agreed (equal) | Variant 2 = Variant 3 | 93% | (b) and (c) already sit in the PR's worktree at its head; (a) must run from each PR's head checkout or HALT `pr_head_mismatch` (`PRC:28`), which A1 conceded. Caveat: INV-001 (no mechanism for (a)). |

Points won (a shared win credits each named variant; "equal" credits none): Variant 1 = 12 (sole 5: S-003, C-002, C-008, X-005, A-004; shared 7: S-004, C-003, C-007, C-009, C-013, X-003, X-004). Variant 2 = 6 (sole 3: S-006, C-006, X-001; shared 3: C-005, X-004, A-006). Variant 3 = 9 (sole 1: C-004; shared 8: S-004, C-003, C-005, C-007, C-009, C-013, X-003, A-006). No winner ("equal"): 9 (S-001, S-002, S-005, C-001, C-010, C-011, C-012, X-002, A-005).

## Convergence Assessment

- Points resolved: 27 of 27 (all unanimous in Round 2)
- Alignment: 100% (27 / 27)
- Round 1 alignment, for the trend: 66.7% (18 / 27; not agreed in Round 1: S-003, C-001, C-003, C-005, C-007, C-012, X-001, X-002, X-003). Every Round 1 split was resolved in Round 2 by an explicit concession or a withdrawn claim. No point flipped winner and then flipped back, so no oscillation is flagged.
- Threshold: 80%
- Unresolved points: none

### Taxonomy coverage (AD-5 gate)

| Level | Points | Agreed | IDs |
|---|---|---|---|
| L1 (surface) | 3 | 3 | S-001, S-002, S-006 |
| L2 (structural) | 12 | 12 | S-003, S-004, S-005, C-004, C-008, C-009, C-011, C-012, C-013, X-002, X-005, A-006 |
| L3 (state mechanics) | 12 | 12 | C-001, C-002, C-003, C-005, C-006, C-007, C-010, X-001, X-003, X-004, A-004, A-005 |

All three levels have more than zero points addressed, so the taxonomy gate passes and no forced round is needed. (Tags are from `diff-analysis.md`; over all 32 S/C/X/A items the file reports L1 3, L2 14, L3 15, the difference being the five unpromoted shared assumptions.)

### Invariant probe gate (AD-1)

HIGH-severity UNADDRESSED items in `invariant-probe.md`: 4.

| ID | Category | What is unaddressed |
|---|---|---|
| INV-006 | guard_conditions | The consensus (a) sentence has no "requested and authorized" condition, although `HWW:221` allows monitor 3 only as a "Requested and authorized full loop" and `HWW:215` says "Push only with approval". |
| INV-012 | count_divergence | Nothing ensures at most one live monitor per PR; pr-submit has no PR-level lock, so a second tab or an (a) run on a handed-off PR can publish the other run's unvalidated edits in its one fix commit. |
| INV-017 | interaction_effects | pr-submit never commits the change or pushes the head branch (`PRS:267`, `PRS:274`); under D4 (b) or (c) workers do not push, so someone must commit and push before pr-submit, and "(a) and (c) need no D4 answer" does not hold. |
| INV-023 | sufficiency_challenge | "(a) default plus (c), pr-submit unchanged" alone does not give working PR monitoring: 7 of 10 gates (G1, G2, G3, G4, G6, G7, G9) are not shown to pass for at least one route, and G8 waits on an undefined smoke test. |

```text
CONVERGENCE BLOCKED: 4 HIGH-severity UNADDRESSED invariant(s) detected
Blocking items: INV-006, INV-012, INV-017, INV-023
These invariant violations must be resolved before convergence can be declared.
Action: Address the flagged items in a subsequent debate round or acknowledge as accepted risk.
```

```text
WARNING: 7 MEDIUM-severity UNADDRESSED invariant(s) detected
Items: INV-001, INV-002, INV-007, INV-008, INV-014, INV-015, INV-018
These items do not block convergence but should be reviewed.
```

LOW UNADDRESSED items (no gate action, listed for the refactoring plan): INV-004, INV-005, INV-009, INV-011, INV-013.

### Status

**Status: BLOCKED_BY_INVARIANTS.** Agreement (100%) is at or above the 80% threshold and all taxonomy levels are covered, but 4 HIGH-severity invariants are UNADDRESSED. Depth standard allows no further debate round, so `refactor-plan.md` carries one planned change or one explicit accepted-risk entry for each of INV-006, INV-012, INV-017 and INV-023.

## Advocates' final recommendations

One line each, quoted from the opening of each Round 2 "Overall recommendation" (the full text is in the Round 2 sections above):

- **Variant 1 advocate:** "Keep (a) as D3's answer and the default: the coordinator, or the person, runs `/sc:pr-submit --monitor 3` from the change's worktree once the workers finish, with no Phase 4 change to pr-submit."
- **Variant 2 advocate:** "I move to V1's recommendation, with one condition added." (The condition: "Whatever D3 decides, fix the `SPEC:137` row's "`ask` or `escalation`" wording to match WC-3.")
- **Variant 3 advocate:** "I converge with V1 and V2. Keep (a) as D3's answer and default: the coordinator or the person runs `/sc:pr-submit --monitor 3` from the change's worktree after the workers finish, with no Phase 4 change to pr-submit."

Common position of all three: (a) is the default; (c) is added by one D3 sentence as the person-requested parallel route, gated on a smoke test; (b) is recorded as deferred, not rejected, until tracked parallel monitoring is needed, D4 resolves to (a) and AC-4.3 passes; the `SPEC:137` row drops "`ask` or `escalation`".
