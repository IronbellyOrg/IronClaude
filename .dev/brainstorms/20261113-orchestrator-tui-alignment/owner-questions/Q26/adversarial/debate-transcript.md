# Adversarial Debate Transcript (Q26)

## Metadata
- Depth: quick
- Rounds completed: 1 (Round 2 skipped: depth=quick; Round 2.5 invariant probe skipped: depth=quick; Round 3 skipped: depth=quick)
- Convergence achieved: 100%
- Convergence threshold: 80%
- Focus areas: All
- Advocate count: 3, spawned in parallel as separate agents (general-purpose type, session default model): V1 architect persona, V2 analyzer persona, V3 qa persona
- Variants: V1 = proposal-A (owner-created Orca worktree), V2 = proposal-B (main checkout on a program branch), V3 = proposal-C (no coordinator yet)

## Round 1: Advocate Statements

Full statements are on disk and are not restated here: `round1-advocate-V1.md`, `round1-advocate-V2.md`, `round1-advocate-V3.md` (this folder). Summary of each:

### Variant 1 Advocate (architect)
**Position**: a home that belongs to the program alone keeps the staged ledger on its branch and keeps one live session per checkout for the program's life; its gap (is an Orca `--agent` launch "person-opened"?) is a definition the owner can settle in one sentence.
**Steelmen**: V2 is the only option that meets "a person-opened Claude session" with no interpretation and can start the ledger before Orca returns; V3 makes no irreversible move while three deciding facts are open.
**Concessions**: person-opened is UNVERIFIED (the spec calls an `--agent` session "a top-level agent", `merged-requirements.md:951`); V1 cannot start the ledger while Orca is down; V2 leads on rule wording (X-001, X-002).

### Variant 2 Advocate (analyzer)
**Position**: the only option that meets every hard requirement today (person-opened, the project's named orchestrator place, the ledger on disk on a clean branch); its weaknesses (A-001, A-002) need stated mitigations, not a different home.
**Steelmen**: V1 solves index travel and shared-workspace concurrency by construction and the project allows a human to create a worktree with an agent; V3 is the spec's own default and avoids naming a home before Orca answers.
**Concessions**: A-001 and A-002 hit V2 hardest and need a rule (no branch switch and no other work in the main checkout while the ledger is staged uncommitted); V1 has the cleaner branch; V2 departs from "(current branch)".
**New evidence**: re-read on 2026-11-14 that the docs branch is in sync with its remote and has no modified tracked files.

### Variant 3 Advocate (qa)
**Position**: lowest risk at W0 (the first wave): the spec's default, accepted by the W0 exit row ("XC-09 open, or held on Q26's default", `merged-requirements.md:860`), with a re-ask at W1 entry.
**Steelmen**: V1 is the only variant that solves A-001 and A-002 structurally; V2 is the only one certainly person-opened and the spec's recommendation.
**Concessions**: it answers nothing; the grant table off disk is a real risk because W0 already needs grant rows (`merged-requirements.md:860`); the re-ask has no mechanical trigger.
**New evidence**: in V2 any plain `git commit` in the main checkout takes the staged ledger with it; `git switch` may refuse on untracked files that the target branch tracks (raised as UNVERIFIED).
**Overall reading**: "Once Orca answers, the risk balance favours V1 if person-opened is confirmed and V2 otherwise."

### Orchestrator verification of new evidence (2026-11-14, read-only)
- V3's switch edge case is CONFIRMED. In the main checkout, origin/master (`d2d8a2d16`, 60 commits ahead of the docs branch) tracks 36 files under 4 of the 21 untracked entries (`.dev/brainstorms/20261105-024132-issue-claim-orca-worktree-flag/`, `.dev/brainstorms/20261107-190223-orchestrator-v2-worker-liveness/`, `.dev/issues/431/`, `.dev/issues/450/`); 34 of them exist untracked with identical content, 2 are absent. A throwaway-repo test with git 2.47.3 showed `git switch` aborts with "untracked working tree files would be overwritten by checkout" even when the untracked file is identical. So V2's step 1 claim that the untracked entries "stay in the folder across a branch switch" is wrong for a switch to a branch made from origin/master: the switch aborts safely until the owner moves or removes those 34 identical copies.

## Scoring Matrix

| Diff Point | Level | V1 adv | V2 adv | V3 adv | Winner | Confidence | Evidence Summary |
|------------|-------|--------|--------|--------|--------|------------|-----------------|
| S-001 | L1 | tie | tie | tie | tie | 95% | identical five-section structure |
| C-001 | L2 | V1 | V2 | V2 | V2 | 70% | only certain person-opened home that the project names; V1 advocate held out on isolation grounds |
| C-002 | L2 | V1 | V1 | V1 | V1 | 95% | a checkout that never switches keeps the staged ledger on its branch; V2 conceded |
| C-003 | L2 | V2 | V2 | V2 | V2 | 85% | git-only first step works while Orca is down; reduced from 95% because the switch needs an extra clean-up step (orchestrator verification) |
| C-004 | L2 | V1 | V1 | V1 | V1 | 92% | main checkout untouched while still unlocking the coordinator |
| X-001 | L3 | V2 | V2 | V2 | V2 | 95% | person-opened is certain only when the owner opens the session; V1 conceded |
| X-002 | L2 | V2 | V2 | V2 | V2 | 80% | follows the named place; all note it departs from "(current branch)" and the line may be an example |
| X-003 | L3 | V1 | V2 | V1 | V1 | 68% | both V1 and V2 keep grants on disk; V1's cannot travel with a branch switch; V3 off disk |
| A-001 | L3 | V1 | V1 | V1 | V1 | 95% | V1 ACCEPT, V2 QUALIFY (concedes), V3 REJECT the assumption as stated; all say only V1 makes it hold by construction |
| A-002 | L3 | V1 | V1 | V1 | V1 | 90% | V1 ACCEPT, V2 QUALIFY, V3 QUALIFY; V1 exclusive by construction |

Points won: V1 5 (C-002, C-004, X-003, A-001, A-002); V2 4 (C-001, C-003, X-001, X-002); V3 0. A-003 (Orca gate) was STATED, not promoted: V1 QUALIFY, V2 ACCEPT, V3 ACCEPT.

## Convergence Assessment
- Points resolved: 10 of 10 (8 unanimous, 2 by 2-of-3 majority: C-001, X-003)
- Alignment: 100%
- Threshold: 80%
- Taxonomy coverage: L1 1 point, L2 5 points, L3 4 points (all levels covered)
- Invariant probe gate: not applied (Round 2.5 skipped at depth quick)
- Status: CONVERGED
- Unresolved points: none
- Note: agreement is per point; the points split between V1 and V2, so the advocates converged on a conditional answer, not on one variant. Each advocate's overall winner differed (V1, V2, and V3 "for now"); the V3 advocate's overall reading matches the merged answer.
