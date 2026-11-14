# Round 1 advocate: Variant 3 (proposal C), persona devops

## Position summary

For each of the nine PR items, the coordinator creates one Orca worktree with one top-level agent (`orca worktree create --agent`) that builds, tests, shows the person its diff, and runs `/sc:pr-submit --monitor 3` itself. This is the shortest operational path: it uses one launch per item through a documented route, it needs no handoff, and it depends on no UNVERIFIED Orca behaviour. The price is losing the supervised-worker controls, and the variant still needs a stall-detection rule.

## Steelman

**Variant 1 (supervised worker, then a coordinator-launched PR session).** At its strongest, V1 is the only variant that keeps both control layers. The code is written under the full worker contract: a brief guard, heartbeats, an admitted `worker_done` (`WORKER-CONTRACT.md:16-20`, `:59`, `:65`). Publishing is then done by a separate ordinary top-level session, which is exactly what line 243 asks for ("run in an ordinary top-level session ... never as a worker"). It is also the spec's recommended answer, so no work-item row needs rewording (merged-requirements.md:964, :975 rule 2). Its one-time check of Orca's second launch, with my variant named as the fallback (variant-1 step 1, diff U-001), is good operations practice: test the risky assumption once, before the first item, with a known way out. Agent launch in an existing worktree is also a documented verb in the installed framework ("Use `agent launch` in an existing worktree or `worktree create --agent` for a new checkout", `src/superclaude/core/CLAUDE.md`, section "Orca session launches"). Only the sequence "after `worker-start`" is unverified.

**Variant 2 (the owner opens each PR session).** At its strongest, V2 is the most literal reading of every rule. The person opens the session, so "shows them to the person and pushes only on the person's go" (`WORKER-CONTRACT.md:244`) holds by construction. The session is person-opened, the same kind as the coordinator (`WORKER-CONTRACT.md:69`), which fits "MUST run in the main orchestrating session" (`SKILL.md:47`) better than any agent the coordinator launches. It needs no unverified Orca behaviour, and the coordinator never starts a session that publishes code. For a program of nine PRs where every push needs the owner's go anyway, V2 makes that go part of the workflow instead of an interrupt.

## Strengths claimed

1. **No dependence on an unverified Orca behaviour.** V3 uses `orca worktree create --agent` once per item. This is the documented route for a top-level agent (merged-requirements.md:954; project CLAUDE.md "Parallel Development with Git Worktrees"). V1 rests on a second sequential `agent launch` in a `worker-start` worktree, which the spec itself marks UNVERIFIED (merged-requirements.md:964). I found no statement either way in the installed Orca skill stubs (`~/.claude/skills/orca-cli/SKILL.md` and `~/.claude/skills/orchestration/SKILL.md` contain no "launch" text; the full guide is loaded through the CLI, which I was told not to run). For operations, a route that might be refused at W1 is a schedule risk on all nine items at once.
2. **"Never both" holds by construction.** Merged-requirements.md:951 says a worktree gets its agent "either from `worker-start` ... or from `orca worktree create --agent` ..., never both; one worktree never holds two live agents". V3 creates exactly one agent per worktree, once. V1 must rely on a timing rule ("never runs while the worker's session is live", :964), and a timing rule has to be checked every time.
3. **Fewest moving parts per item.** One launch, one session, no handoff (diff C-003). V1 needs a worker, an admitted `worker_done`, confirmation that the worker session has ended, a second launch, and tracking and closing the second session (variant-1 "costs", last bullet). Every extra step is a place where an item can stall without anyone noticing.
4. **The author answers the reviews.** pr-submit fixes confirmed findings and pushes at `--monitor 3` (`SKILL.md:18-25`). In V3 the session that wrote the change applies those fixes. V1 and V2 give the work to a cold reader that must first re-read the change (diff X-004; variant-1 "costs", third bullet).
5. **It is the route the Round 3 invariant check recommended.** round3-invariants-V2.md:53 checked the same contract lines (`:23`, `:41`, `:243`, `SKILL.md:47`, `:19`). It called this "the only route the worker contract and the pr-submit skill both allow while D3 keeps pr-submit off workers" (confidence 85).
6. **The coordinator's watch duty is never blocked.** The coordinator only tracks each PR with `gh pr view <N> --repo IronbellyOrg/IronClaude`, which matches its role row (merged-requirements.md:962). It never runs pr-submit and never manages a second launch.
7. **No owner session per PR.** Unlike V2, the owner does not open and attend nine sessions. The owner's time is limited to approving the grant row and giving the go at the diff stop (see Concessions for what this still costs).

## Weaknesses identified in other variants

1. **V1 puts a single unverified fact on the critical path of all nine items.** The spec gives no default if Orca refuses the second launch other than "the owner is asked again" (variant-1 step 1). In that case the program falls back to V3 anyway, after losing the setup work. V1's own text names V3 as "the natural fallback". If the fallback is the route that is known to work, it is the safer primary route.
2. **V1 doubles the sessions the coordinator owns.** "`orca agent launch` by the coordinator is a session start the coordinator owns; it must track and close each one" (variant-1 costs). That is up to 18 sessions to supervise instead of 9, and the coordinator must also confirm that each worker session has ended before the launch (merged-requirements.md:964 "never runs while the worker's session is live"). Proving that a session has ended is itself an Orca state read that the spec does not define.
3. **V1's claim of "no owner time" is overstated.** The diff marks X-003 as "No (one confirmation)" for V1. But `WORKER-CONTRACT.md:244` still makes the coordinator show the person every unseen worker change and push "only on the person's go", which happens once per PR in V1 too (variant-1 step 2). Owner time per PR is about the same in V1 and V3.
4. **V2 makes owner availability the throughput limit.** "Owner latency is the real schedule" (merged-requirements.md:523, cited by variant-2). The pr-submit loop is attended and stays open until the reviews land (`SKILL.md:43-45`: "closing the session loses it"). The owner would hold nine attended sessions, and any time the owner is away has the same effect as the default "no PR is opened ... the lane is held" (question.md:15).
5. **V2 and V1 both put a cold reader on review fixes**, which raises the chance that a pr-submit round is spent re-learning the change instead of fixing it (diff X-004).

## Concessions

1. **V3 gives up the supervised-worker controls for the code.** There is no brief guard, no heartbeats and no `worker_done` for the coordinator to admit (variant-3 costs; diff X-002). This is a real loss of evidence for the coordinator. V1 and V2 are better on this point.
2. **Stall detection is unresolved.** V3 tracks agents with `gh pr view` and "Orca idle notices" (variant-3 step 4, from round3-invariants-V2.md:53 item 4). I found no documentation of Orca idle notices for agents launched with `worktree create --agent` in the files I was allowed to read: UNVERIFIED. Before the PR is open, `gh pr view` shows nothing, so an agent that drifts or hangs before opening its PR is invisible until someone looks. V3 needs an explicit rule here, for example a deadline per item after which the coordinator does a read-only look at the worktree and asks the owner.
3. **The diff stop before the push binds the agent only by its prompt.** Line 244 speaks of "worker commits". V3's commits are not worker commits, so the contract does not mechanically force the stop. It holds only because the prompt and the grant row say so, and permission checks are off on this host (variant-3 costs; INV-011). V2's construction ("the person opened the session") is stronger.
4. **Nine work-item rows must be reworded** (diff C-005), and the role rows in 6.3 and guardrail 6.4 rule 2 must change too (round3-invariants-V2.md:53 item 5). V1 needs no spec edit.
5. **"Ordinary top-level session" is satisfied, but not in V2's literal sense.** A coordinator-created agent is top-level and not a worker, but the person did not open it, so it is weaker than V2 against `SKILL.md:47` ("main orchestrating session"). V1 has the same weakness.
6. **The author answering its own reviews is also self-review.** The independent check still comes from the Augment and Codex reviewers and from the spec's independent reviewer role (merged-requirements.md:969), not from the agent.

## Shared assumption responses (A-001)

**QUALIFY.** `WORKER-CONTRACT.md:240` ("The coordinator performs every git and GitHub outward action") sits in the coordinator rules. Line 243 in the same section carves out PRs specifically: "PRs go only through `/sc:pr-submit --monitor 3`, run in an ordinary top-level session as decision D3 states". The skill itself pushes, replies and resolves (`SKILL.md:18-25`). So the push, reply and resolve that pr-submit performs are covered by the specific PR rule, not barred by the general one, in all three variants. What stays unreconciled is the commit before pr-submit runs. Line 245 lets the coordinator commit only when no worker runs there, while 6.4 rule 14 (merged-requirements.md:987) gives the commit to the PR session. That gap is real for V1 and V2, which commit worker changes. It is narrower for V3, because no worker ever runs in the worktree and the commits are the agent's own, not "worker commits". It is still not stated anywhere in the contract. Every variant should record the commit as a named action in its `GRANT(<item>,pr-submit)` row, and the D3 text should state that the PR session's commit and push are coordinator-delegated outward actions.

## Per-point verdicts

| Point | Superior | Reason |
|---|---|---|
| S-001 | tie | All three use the same five-section layout. |
| C-001 | V3 | One documented `worktree create --agent` launch, compared with V1's unverified second launch and V2's manual owner session. |
| C-002 | V1 | A supervised worker keeps the brief guard, heartbeats and admitted `worker_done` (V2 is equal here; V3 loses them). |
| C-003 | V3 | One agent per item means the fewest handoffs and sessions to track. |
| C-004 | V2 | The person sees the diff by construction; in V3 the stop holds only by the prompt. |
| C-005 | V1 | No spec rows change (V2 is equal); V3 rewords nine rows plus 6.3 and 6.4. |
| X-001 | tie | V2 and V3 both avoid the unverified second launch; V1 alone depends on it. |
| X-002 | V1 | Keeps the worker controls for code (V2 is equal); this is V3's main loss. |
| X-003 | tie | V1 and V3 both need only the owner's per-push go (`WORKER-CONTRACT.md:244`); V2 adds a whole attended session per PR. |
| X-004 | V3 | The author fixes the review findings with no cold re-read. |
| A-001 | tie | No variant reconciles line 240/245 with 6.4 rule 14; V3's gap is only slightly narrower (no worker commits). |

Overall: V3
