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
