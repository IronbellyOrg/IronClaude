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
