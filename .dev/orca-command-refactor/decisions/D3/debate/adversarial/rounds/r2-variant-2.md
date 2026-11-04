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
