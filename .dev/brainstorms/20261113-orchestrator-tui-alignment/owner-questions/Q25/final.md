# Q25 final: who runs `/sc:pr-submit --monitor 3` for each program PR?

`/sc:pr-submit --monitor 3` is the project's required way to open a PR on the fork `IronbellyOrg/IronClaude`. It opens the PR, waits for the Augment and Codex reviews, and then fixes, pushes, replies to and resolves the confirmed findings without asking. Nine program items end in a PR. The rules say it never runs inside a supervised worker (an agent started by `worker-start` under the worker contract) and never inside the coordinator (the person-opened session that runs the program).

## Debate result

Winner: proposal A, with additions, confidence 55 percent. Proposal A is the spec's route: a supervised worker builds the change, then the coordinator launches a separate top-level PR session in the same worktree.

Agreement: split. Each advocate kept its own proposal overall (1-1-1), although 10 of 11 individual points had a majority. Proposal A scored 0.937, B 0.880, C 0.874, and A won the most points (4, against 3 for C and 2 for B).

Deciding evidence:
- A is the only route that keeps the supervised-worker controls for the code (brief guard, heartbeats, an admitted `worker_done`) and costs no per-PR owner time.
- The spec's role and guardrail rules are already written to A (`.dev/brainstorms/20261113-orchestrator-tui-alignment/merged-requirements.md` lines 964, 975, 987).
- Its one weakness is unverified: whether Orca allows a second, sequential `agent launch` in a worktree first created by `worker-start` (line 964).

The three proposals:
- **Proposal A (worker builds, coordinator-launched PR session publishes).**
  - Strength: supervision of the build, a review step before publishing, no rewording of the spec.
  - Weakness: it rests on the unverified Orca behaviour. The PR session did not write the change. At `--monitor 3` its review-fix pushes are unsupervised, as in every proposal.
- **Proposal B (the owner opens each PR session).**
  - Strength: the person's instruction to publish sits in the live conversation of the session that publishes. That is the worker contract's own condition for outward actions (`src/superclaude/core/WORKER-CONTRACT.md:240`). All three advocates agreed it best guarantees the person sees the diff.
  - Weakness: nine owner-attended sessions, in a program whose schedule is already set by owner latency (line 523).
- **Proposal C (one top-level agent per PR item, no worker).**
  - Strength: one documented launch per item, no unverified behaviour, and the author answers its own reviews (all three agreed on these points).
  - Weakness: it drops the worker controls. It cannot detect an agent that stalls before opening its PR. Its "show the diff first" step binds only by the prompt, on a host where permission checks are off.

Gap all three advocates found: the contract gives commits in a worktree to the coordinator (`WORKER-CONTRACT.md:245`), but the spec gives the first commit to the PR session (line 987). The pr-submit push, reply and resolve are covered by the contract's specific PR rule (`:243`); the first commit is not.

## Final recommendation

Use proposal A, with four additions:
1. Before the first PR item, check once whether Orca allows the second launch. If it does not, switch PR items to proposal C's route (one top-level agent per item created with `orca worktree create --base-branch origin/master --agent claude --prompt "<item brief>"`), with a per-item deadline after which the coordinator checks the worktree read-only and asks you.
2. The PR session shows the diff and waits for the person's go in its own conversation before the first push.
3. Each `GRANT(<item>,pr-submit)` row names the commit of the worker's changes, the PR, the re-review comment, the unasked review-fix pushes, replies and resolves. One sentence in decision D3 states that these are outward actions delegated to the PR session.
4. The PR session reads the worker's contract and handoff files first.

Confidence 55 percent. Strongest reason: it is the only route that keeps supervision of the code without spending your time on every PR. Equals the spec's recommended answer: partly. It keeps the spec's route and its named alternative as the fallback, and adds the person's go in the publishing session, the grant contents and the D3 sentence that close the commit gap. Merged text: `merged-proposal.md`.

## What would change the answer

If Orca refuses a second launch in a `worker-start` worktree, proposal C becomes the main route. If you want the instruction to publish to come from you in person on every PR, whatever it costs in time, proposal B is better.

## Criticality rating

- Security or trust boundary: high
- Reversibility: costly
- Who is affected: other people or repos
- Needs the owner's own intent, taste or knowledge that no file holds: yes
- Cost if the answer is wrong: medium
- Does it grant authority or accept a risk in writing: yes
- Debate: split
- Suggested handling: NEEDS-HUMAN
- Reason for the suggested handling in two sentences. The answer decides which session may commit, push, comment and resolve review threads on the owner's GitHub fork, which delegates publishing authority and touches a public-facing repository; pushed commits and posted comments cannot simply be taken back. The advocates also split three ways on the overall answer, and the deciding trade-off (your time against supervision and authority) is the owner's own call.

## Debate record

- Adversarial folder: `.dev/brainstorms/20261113-orchestrator-tui-alignment/owner-questions/Q25/adversarial/`. It holds diff-analysis.md, round1-advocate-V1/V2/V3.md, debate-transcript.md, base-selection.md, refactor-plan.md, merge-log.md and return-contract.yaml. Merged text: `Q25/merged-proposal.md`.
- fallback_mode: false. The three advocates and the merge executor were spawned as sub-agents; diff analysis, scoring and base selection were done by this worker in the debate-orchestrator role.
