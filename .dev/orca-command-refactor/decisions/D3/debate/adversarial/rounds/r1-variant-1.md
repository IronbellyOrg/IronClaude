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
