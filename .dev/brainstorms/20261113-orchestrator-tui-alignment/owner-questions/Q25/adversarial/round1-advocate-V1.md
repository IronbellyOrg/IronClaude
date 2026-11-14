# Round 1 advocate: Variant 1 (architect persona)

Variant 1 = proposal A: a supervised worker builds the change to `worker_done`; after admission and the end of the worker's session, the coordinator launches one ordinary top-level PR session in the same worktree with `orca agent launch`, which commits named paths and runs `/sc:pr-submit --monitor 3`.

Paths below are relative to the worktree root `/home/coder/workspaces/worktrees/IronClaude/issue-339-orchestrator-mode` unless absolute. MR = `.dev/brainstorms/20261113-orchestrator-tui-alignment/merged-requirements.md`; WC = `src/superclaude/core/WORKER-CONTRACT.md`; R3 = `.dev/brainstorms/20261113-orchestrator-tui-alignment/adversarial/adversarial/`.

## Position summary

Variant 1 is the only answer that keeps the code inside the supervised-worker boundary (brief guard, heartbeats, admitted `worker_done`), puts a coordinator review between building and publishing, costs the owner no per-PR time, and needs no rewording of the spec, because MR 6.3, 6.4 rule 2 and rule 14 are already written to it. Its one real weakness is an UNVERIFIED Orca behaviour (a second, sequential `agent launch` in a `worker-start` worktree). Variant 1 bounds that risk with a one-time check before the first PR item and names Variant 3 as the fallback.

## Steelman

**Variant 2 (owner opens each PR session).** At its strongest, Variant 2 is the most conservative reading of every rule in play. A person-opened top-level session is exactly the "ordinary top-level session" of WC:243. It is the same kind of session as the coordinator, which MR line 958-962 already treats as person-opened. It meets WC:244 ("shows them to the person and pushes only on the person's go") by construction, because the person reviews the diff in the session they open. It also meets WC:240's "confirms with the person at the moment of action unless that instruction is in its live conversation", because the owner is in that conversation. The coordinator never starts a session that publishes code. It does not depend on any untested Orca behaviour. For a program where publishing is the riskiest act, putting a human hand on every publish is a defensible design.

**Variant 3 (one top-level agent per PR item, no worker).** At its strongest, Variant 3 removes the two-agent question entirely. It uses one documented Orca route once per item (`orca worktree create --agent`, which MR line 954 spells out and project CLAUDE.md:312 requires), so MR line 951's "never both" holds by construction. The author of the change also answers its reviews, so review fixes come from the agent that holds the context, not from a cold reader. It has one agent per item, so the coordinator has fewer handoffs. The Round 3 V2 advocate called it "the only route the worker contract and the pr-submit skill both allow while D3 keeps pr-submit off workers" (R3 `round3-invariants-V2.md:53`, confidence 85). That is a serious, evidence-backed position.

## Strengths claimed

1. **It matches the spec as already merged, with no rewording.** MR 6.4 rule 2 (line 975) reads: "A worker makes and tests the change and stops at `worker_done`; only after the coordinator admits `worker_done` and the worker's session has ended does the PR session open or attach the PR in that worktree." MR 6.3 (line 964) defines the PR session row this way, and MR 6.4 rule 14 (line 987) gives the commit to the PR session. Variant 1 is the recommended answer at MR line 552. Variant 3 must reword nine work-item rows plus 6.3 and 6.4 (its own "What it costs", lines 23-25). Architecturally, Variant 1 is the low-churn option.
2. **It keeps the supervised-worker controls on the code.** The worker is bound by the brief guard (WC:23), WC-9 (no outward action, WC:41), WC-13 (no Orca fan-out, WC:62), heartbeats and liveness supervision (WC:46, :65), and the WC-5 `worker_done` mapping (WC:59). The coordinator then reads the result from disk before anything is published (MR line 962, "reads workers' results from disk"). Variant 3 gives all of this up. Its own risk list says so (variant-3 lines 23-24, 29), and R3 `invariant-probe.md:9` notes that a `worktree create --agent` session "is not a worker, sends no `worker_done`, is not bound by WC-13".
3. **It separates building from publishing, with a review step between them.** Least privilege: the agent that writes code cannot push, and the agent that pushes did not write unreviewed code. The coordinator shows the person any unseen diff at that boundary. This is the literal actor that WC:244 names ("the coordinator shows them to the person"); in Variant 3 the agent shows its own diff, and in Variant 2 the owner looks without the coordinator.
4. **It needs no owner time per PR.** The owner confirms the arrangement once and approves each `GRANT(<item>,pr-submit)` row, which every variant needs anyway (question.md line 19). MR line 523, "Owner latency is the real schedule", makes Variant 2's per-PR attendance a direct schedule cost across nine PR items.
5. **Its unverified premise has documentation support, and it carries a check and a fallback.** `src/superclaude/core/CLAUDE.md:48-49` documents "Use `agent launch` in an existing worktree or `worktree create --agent` for a new checkout". The same file (line 57-58) and project CLAUDE.md:312 say "The eligible session that creates a worktree owns its agent(s)", plural, which reads as expecting more than one agent over a worktree's life. What stays UNVERIFIED is the narrower case: a second launch in a worktree that `worker-start` created, after the worker has ended. The Orca guides are served only by the binary (`~/.claude/skills/orca-cli/SKILL.md`, `orchestration/SKILL.md`: "This file is a discovery stub"), so I could not read them under this round's no-orca rule. Variant 1 step 1 (variant-1 line 9) tests this once before the first PR item and falls back to Variant 3 (diff-analysis U-001, rated High).
6. **It keeps the coordinator's watch free.** The coordinator launches the session and polls `gh pr view` at wakes; it never runs the attended loop (`~/.claude/skills/sc-pr-submit-protocol/SKILL.md:19,43-47`; MR line 962). Variant 3 shares this property. Variant 2 also keeps it, at the cost of owner attendance.

## Weaknesses identified in other variants

1. **Variant 2's "no Orca dependence" claim is weaker than it looks.** If the owner opens the PR session through Orca into the `worker-start` worktree, that is the same second-agent-in-a-worker-worktree case as Variant 1, now unchecked (UNVERIFIED either way). If the owner opens it outside Orca (a plain terminal in the path), Orca does not track it, and the coordinator learns of it only through `gh pr view`. Variant 2 does not say which of the two it means (variant-2 line 10).
2. **Variant 2 makes owner presence the throughput limit.** Nine PR items (question.md line 19), each with an attended poll loop that "cannot survive its own session" (SKILL.md:43-45), means nine owner-attended sessions. Variant 2 admits that "Lanes stall whenever the owner is away, the same effect as the default" (variant-2 line 25). The default is "No PR is opened ... the lane is held" (question.md line 15), so while the owner is away Variant 2 behaves like no answer at all.
3. **Variant 3 removes supervision from the code-writing phase.** The top-level agent runs with permission checks off on this host (variant-3 line 24, INV-011; MR 6.4 rule 10 for the FU-1 case). It is not bound by WC-13, so its prompt is the only thing that stops it from creating worktrees or launching agents. Liveness is unsolved, as its own "What stays unresolved" states (variant-3 line 29). R3 `invariant-probe.md:9` adds, citing owner memory, that such a session "does not appear in the Orca queue".
4. **Variant 3 moves the WC:244 check into the agent being checked.** "The agent ... stops and shows the person its diff" (variant-3 line 11) makes the publisher responsible for its own gate. WC:244 names the coordinator as the one who shows unseen commits, and WC:240 puts outward actions under coordinator control.
5. **Variant 3 has the widest blast radius in the spec.** Its rewording covers nine rows plus 6.3 (Worker and PR session rows) and 6.4 rules 2 and 14, all late in a merged and QA'd spec. Every reword is a new place for drift.

## Concessions

- **The UNVERIFIED Orca premise is a real, high-impact risk** (diff-analysis X-001, High). If Orca refuses the second launch, Variant 1 degrades to Variant 3, and the check costs one round with the owner. Variants 2 and 3 do not carry this risk.
- **The cold reader is a real cost.** The PR session did not write the change. When review findings arrive, it must re-read the diff and the worker's contract and handoff files (WC-15 writes those, WC:64, which helps but does not remove the cost). Variant 3 is better here.
- **The review-fix phase is unsupervised in Variant 1 too.** At `--monitor 3`, pr-submit edits, commits and pushes fixes. Those code changes come from a top-level PR session, not a worker, so for that phase Variant 1 has no more supervision than Variant 3. The supervision advantage covers the initial build only.
- **There are two agents per item, plus a handoff the coordinator must run, track and close** (variant-1 lines 24, 26). That is more coordinator work than Variant 3.
- **Variant 2 meets WC:244 and WC:240's "confirm at the moment of action" most cleanly,** because the person is live in the publishing session.

## Shared assumption responses (A-001)

**A-001: QUALIFY.** WC:240 ("The coordinator performs every git and GitHub outward action ... in its own conversation") and WC:243 ("PRs go only through `/sc:pr-submit --monitor 3`, run in an ordinary top-level session as decision D3 states, never as a worker") already pull against each other inside the contract. MR line 962 forbids the coordinator from running pr-submit, and SKILL.md:47 requires pr-submit to run at the top level of its own session. So under the current text, no PR path can be compliant with a literal, unqualified WC:240. WC:243 is the specific rule for PRs and should govern the PR push; WC:245 only limits when the coordinator itself commits and does not grant commits to anyone else.

This is still an unreconciled gap that all three variants share. The fix is the same for each: record in D3, or as a contract note, that the PR session performs the commit, push, reply and resolve that pr-submit makes, and only those, bounded by its `GRANT(<item>,pr-submit)` row (MR 6.4 rule 2: "lists every write the tool makes"). That grant row is the user's instruction naming the action, which WC:240 requires. Variant 2 satisfies WC:240's "confirms with the person at the moment of action" best, because the owner is live in that session. Variants 1 and 3 rely on the grant row being explicit enough to count as "that instruction".

## Per-point verdicts

| Point | Superior | Reason |
|---|---|---|
| S-001 | tie | All three use the same five-section layout. |
| C-001 | V1 | The coordinator starts the session from a documented launch verb (`core/CLAUDE.md:48`) after admitting the work. No owner bottleneck (V2), and building stays separate from publishing (unlike V3). |
| C-002 | V1 | V1 and V2 both use a supervised worker for the code, with brief guard, WC-9/13, heartbeats and `worker_done`. V1 gets this without V2's per-PR owner cost. |
| C-003 | V3 | One agent per item is simpler, with no handoff and no second-launch question. |
| C-004 | V2 | The person sees every diff in the session that publishes it, by construction. V1 matches WC:244's literal actor, but V2 fully meets the rule's purpose. |
| C-005 | V1 | V1 needs no rewording, because 6.3 and 6.4 rules 2 and 14 are already written to it. V2 needs little; V3 needs nine rows plus 6.3 and 6.4. |
| X-001 | V3 | It uses only the documented `worktree create --agent` route, with no unverified premise. V2's independence from Orca is unclear (see weakness 1). |
| X-002 | V1 | V1 keeps supervised-worker controls for the build without spending owner time. V2 keeps them too but at a schedule cost; V3 drops them. |
| X-003 | tie (V1, V3) | Neither spends owner time per PR beyond the grant row that every variant needs. |
| X-004 | V3 | The author answers its own reviews; V1 and V2 use a cold reader. |
| A-001 | V2 | All three share the gap. V2's live owner best satisfies WC:240's "confirms with the person at the moment of action"; the contract-note fix applies equally to all three. |

Overall: V1
