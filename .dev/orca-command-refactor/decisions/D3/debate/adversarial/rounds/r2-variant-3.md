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
