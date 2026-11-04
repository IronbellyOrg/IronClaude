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
