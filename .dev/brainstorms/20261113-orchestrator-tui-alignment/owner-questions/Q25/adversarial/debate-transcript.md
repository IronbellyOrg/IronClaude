# Adversarial Debate Transcript (Q25)

## Metadata
- Depth: quick
- Rounds completed: 1 (Round 2 skipped: depth=quick; Round 2.5 invariant probe skipped: --depth quick; Round 3 skipped: depth=quick)
- Convergence achieved: 91% on diff points (10 of 11); overall advocate preference split 1-1-1
- Convergence threshold: 80%
- Focus areas: All
- Advocate count: 3, spawned as parallel sub-agents (general-purpose agent type; personas architect, security, devops)
- Agent failures: none

## Round 1: Advocate Statements

### Variant 1 Advocate (proposal-A, worker then coordinator-launched PR session; architect)
File: `round1-advocate-V1.md`. Position: keeps the code inside the supervised-worker boundary, puts a coordinator review between building and publishing, costs no per-PR owner time, and the spec's 6.3 and 6.4 rules 2 and 14 are already written to it. Concessions: the UNVERIFIED second launch is a high-impact risk (falls back to variant 3); cold reader; at `--monitor 3` the review-fix phase is unsupervised in every variant; two agents and a handoff per item; variant 2 meets the contract's "confirm at the moment of action" most cleanly. Overall: V1.

### Variant 2 Advocate (proposal-B, owner-opened PR session; security)
File: `round1-advocate-V2.md`. Position: the only route where the instruction to publish is in the live conversation of the publishing session (`WORKER-CONTRACT.md:240` exception), and the coordinator, which reads untrusted text, stays out of the publish path. Concessions: nine owner-attended sessions; the skill's "main orchestrating session" is a technical rule, not a person rule (`SKILL.md:47-49`); the person's review covers only the first push, later fix pushes go out without asking at `--monitor 3`; cold reader; if the owner opens the session through Orca in a `worker-start` worktree, the same unverified question may apply (a plain terminal avoids it). Overall: V2 on the authority question; V1 or V3 if throughput weighs more.

### Variant 3 Advocate (proposal-C, one top-level agent per PR item; devops)
File: `round1-advocate-V3.md`. Position: shortest operational path, one documented launch per item, no handoff, no unverified Orca behaviour. Concessions: loses supervised-worker controls; stall detection before the PR exists is unsolved ("Orca idle notices" not documented in files read: UNVERIFIED); the diff stop binds only by prompt with permission checks off; nine rows plus 6.3 and 6.4 must change; the author fixing its own findings is self-review. Overall: V3.

### Shared assumption A-001: all three QUALIFY with the same reading
`WORKER-CONTRACT.md:243` is the specific PR rule and covers the push, reply and resolve that pr-submit performs; the gap is the first commit of the worker's uncommitted changes (`:245` gives worktree commits to the coordinator; 6.4 rule 14 gives them to the PR session). All three: the `GRANT(<item>,pr-submit)` row must name the commit, and the D3 text should state that the PR session's commit and push are delegated outward actions. Variant 2 meets `:240`'s "instruction in its live conversation" without that amendment.

## Scoring Matrix

Positions (V1 adv, V2 adv, V3 adv).

| Diff Point | Level | Positions | Winner | Confidence | Evidence Summary |
|---|---|---|---|---|---|
| S-001 | L1 | tie x3 | tie | 95% | Same layout |
| C-001 | L2 | V1, V2, V3 | unresolved | 50% | Each prefers its own starter of the PR session |
| C-002 | L2 | V1, V1/V2, V1 | Variant 1 | 85% | Supervised worker for the code; V3 conceded the loss |
| C-003 | L2 | V3, V3, V3 | Variant 3 | 92% | One agent per item; unanimous |
| C-004 | L3 | V2, V2, V2 | Variant 2 | 92% | Person sees the diff in the publishing session by construction; unanimous |
| C-005 | L2 | V1, V1/V2, V1 | Variant 1 | 85% | No spec rows change |
| X-001 | L3 | V3, V2/V3, V2/V3 | Variant 3 | 85% | No unverified Orca behaviour; V1 conceded |
| X-002 | L3 | V1, V1/V2, V1 | Variant 1 | 85% | Keeps brief guard, heartbeats, admitted `worker_done` without owner cost |
| X-003 | L3 | V1/V3, V1, V1/V3 | Variant 1 | 80% | One confirmation, no per-PR owner time |
| X-004 | L2 | V3, V3, V3 | Variant 3 | 92% | Author answers its own reviews; unanimous |
| A-001 | L3 | V2, V2, tie | Variant 2 | 68% | Only V2 meets the contract's live-conversation exception without amendment |

## Convergence Assessment
- Points resolved: 10 of 11
- Alignment: 91%
- Threshold: 80%
- Taxonomy coverage: L1 1, L2 5, L3 5; all covered
- Invariant probe gate: not applied (quick depth)
- Status: CONVERGED on diff points; overall preference SPLIT (each advocate kept its own variant)
- Unresolved points: C-001
- Points won: V1 4 (C-002, C-005, X-002, X-003), V3 3 (C-003, X-001, X-004), V2 2 (C-004, A-001)
