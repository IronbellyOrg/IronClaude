# Q26 final: where the coordinator runs, and on which branch its ledger is staged

Terms used here: the coordinator is the person-opened Claude session that keeps the program's decision ledger and starts the program's workers (work item XC-09, "stand up the coordinator"). The ledger is the always-staged folder `.dev/tasks/<program-package>/` that holds the owner's answers and the grant table, the list of outward actions the owner has approved (work item XC-01). "Staged" means added to git's index, not committed.

## Debate result

Winner: proposal A (a dedicated program worktree the owner creates through Orca, whose agent is the coordinator), on the condition that the owner states that such a session counts as "person-opened"; otherwise proposal B. Confidence 60 percent.

Advocate agreement: on each of the 10 debated points the three advocates agreed (8 unanimous, 2 by 2 of 3), so per-point convergence was 100 percent; but the points split between A and B (A won 5, B won 4, C won 0), and each advocate's overall pick differed (A, B, and C "for now"). The headline is therefore split. The scoring tied A and B (0.853 against 0.847, inside the 5 percent band) and the tiebreaker on debate points chose A (`adversarial/base-selection.md`).

Deciding evidence:
- Staged files live in a checkout's index and move with any later branch switch; in the main checkout, the owner's everyday folder, the ledger could ride onto a docs branch or into an unrelated commit. A dedicated worktree never switches (`adversarial/diff-analysis.md` A-001; all three advocates agreed).
- Checked on 2026-11-14: switching the main checkout to a branch from `origin/master` aborts today, because 34 untracked files there have the same paths as tracked files on `origin/master` (identical content); a throwaway test with git 2.47.3 confirmed git refuses even identical untracked files (`adversarial/debate-transcript.md`, orchestrator verification). Proposal B's claim that the untracked entries simply stay across the switch is wrong.
- Against A: the coordinator must be "an Orca coordinator session the person opened" (`src/superclaude/core/WORKER-CONTRACT.md:69`; `src/superclaude/core/HOW-WE-WORK.md:402`), and the spec calls an agent started by `orca worktree create --agent` "a top-level agent" (`merged-requirements.md:951`). No source says it counts as person-opened. All three advocates gave this point to B.

Proposal A, strengths and weaknesses: it isolates the ledger and the coordinator by construction, leaves the main checkout alone, and uses the creation command the spec already prescribes (`merged-requirements.md:954`). Its weaknesses are the unverified person-opened status and that it cannot start while Orca is unreachable (Orca was unreachable on 2026-11-13, `merged-requirements.md:604`).

Proposal B, strengths and weaknesses: it is certainly person-opened, is the spec's recommendation, follows the project's "Session A: Open the main checkout" guidance (project `CLAUDE.md`), and its first step needs no Orca. Its weaknesses: the staged ledger can travel with a later switch or be swept into an unrelated commit; the owner's other sessions in the same folder would break "one worktree never holds two live agents" (`merged-requirements.md:951`); and the switch needs a clean-up of 34 identical untracked files first.

Proposal C, strengths and weaknesses: it is the spec's own default, accepted by the first-wave exit rule (`merged-requirements.md:860`), and makes no move on unverified premises. It unlocks nothing, keeps the grant table off disk where agents cannot read it although first-wave items already need grant rows, and its re-ask has no mechanical trigger.

## Final recommendation

Use a dedicated program worktree that the owner creates through Orca from `origin/master` with an agent, make that agent the coordinator, and stage the ledger there; the owner writes one sentence in the ledger saying a session they launch this way and attend counts as person-opened. If the owner will not say that, use the main checkout on a new program branch, after moving or removing the 34 untracked copies that block the switch, and keep the main checkout on that branch, with no other commits and no other Claude sessions, while the ledger is staged. If Orca is unreachable when the owner answers, record the answer and keep the ledger by hand until the first successful Orca read. Confidence 60 percent.

Strongest reason: only a checkout that never changes branch keeps an always-staged ledger where the owner put it; the main checkout is the owner's everyday workspace and cannot promise that.

Equals the spec's recommended answer: partly. The spec recommends the main checkout and lists the Orca worktree as the alternative (`merged-requirements.md:553`). The debate reverses that order because of two git facts the spec did not weigh (staged files travel with a switch; the switch currently aborts), but only if the owner settles the person-opened reading.

## What would change the answer

If the owner says an Orca-launched session does not count as person-opened (or a source is found saying so), proposal B with its three rules becomes the answer.

## Criticality rating

- Security or trust boundary: low
- Reversibility: easy
- Who is affected: only this program
- Needs the owner's own intent, taste or knowledge that no file holds: yes
- Cost if the answer is wrong: medium
- Does it grant authority or accept a risk in writing: yes
- Debate: split
- Suggested handling: NEEDS-HUMAN
- Reason for the suggested handling in two sentences. The recommended answer needs the owner to rule in writing on who counts as a person-opened coordinator, which is the authority that lets a session start workers, and it occupies the owner's own workspace. The advocates' overall picks also differed, so an agent should not choose this on the owner's behalf.

## Debate record

- Folder: `/home/coder/workspaces/worktrees/IronClaude/issue-339-orchestrator-mode/.dev/brainstorms/20261113-orchestrator-tui-alignment/owner-questions/Q26/adversarial/` (merged answer: `../merged-output.md`)
- fallback_mode: false (three advocate agents spawned in parallel; the diff analysis, scoring, plan and merge were done by this worker in-context, as recorded in `return-contract.yaml`)
