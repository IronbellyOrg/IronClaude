# Q32 final: may supervised workers make one local commit at the end of their Task?

Terms used here. A supervised worker is an agent session that Orca (the app that runs agent sessions) starts with `worker-start` to do one Task, and that reports back with `worker_done`. The PR session is the separate top-level session that later opens the pull request for that worktree (Q25 decides who runs it). WC-9 is the worker contract rule on git writes (`src/superclaude/core/WORKER-CONTRACT.md:41-44`). A grant row `GRANT(<item>,commit)` is one line in the program's decision ledger (work item XC-01) that permits one action for one work item.

## Debate result

Winner: proposal B ("no; workers never commit; the PR session commits"), confidence 65 percent (the mean of the three advocates' own judgments: 65, 70, 60). The advocates agreed 3 of 3, including the advocates assigned to argue for A and for C. Per-point agreement was 13 of 13 by majority, and 9 of 13 were unanimous.

Deciding evidence: a worker commit is allowed only when "the brief quotes, word for word, the user's instruction naming a local commit for that Task" and the worker is in "its own child worktree created by Orca" (`WORKER-CONTRACT.md:42`). Whether one standing sentence filled in by the coordinator meets the first condition is UNVERIFIED. Whether a `worker-start` worktree meets the second is also UNVERIFIED (`Q32/question.md` facts 7 and 8). A "no" depends on neither reading and adds no owner questions, which matters because the spec says "Owner latency is the real schedule" (`merged-requirements.md` line 523). The document-quality scores put all three within 5 percent of each other (0.91, 0.89, 0.87), so the debate decided. The skill run is recorded as status "partial" because of how the tie was broken (see Debate record).

- **Proposal A (no standing rule; ask the owner per Task at each dispatch).** Strength: the only "yes" path that meets WC-9 at its strictest, because the quoted words are the owner's own words for that Task. It also leaves no standing permission in the ledger. Weakness: up to nine more owner questions, one per code-changing Task (SW-07, SW-08, SW-10, SW-14, OB-06, OB-07, WA-01, WA-03, XC-07), and two commit paths in one program. Its own advocate conceded it does not give the sentence the question asks for.
- **Proposal B (no; the PR session commits).** Strength: one commit path and one review before the commit, built only from rules that are already written (`WORKER-CONTRACT.md:44` and `:245`; spec section 6.4 rule 14, line 987). It equals the default. Weakness: between the end of the worker and the PR session's commit, the change is only uncommitted files, and the spec has no general rule against cleaning a worker's worktree in that gap. The only such rules are line 898 for one named sibling worktree and line 1074 for resume. The merge adds that guard (`Q32/merged-output.md`).
- **Proposal C (yes; one standing sentence for every code-changing Task).** Strength: the change is saved as a commit the moment the worker succeeds, the commit id gives a fixed revision to review, and one answer covers all nine Tasks. Weakness: the benefit depends on the two UNVERIFIED readings above. If a strict check refuses the commit, the program ends up with B's outcome plus refused-commit reports. Its own advocate voted for B.

## Final recommendation

Answer "no: workers leave their changes uncommitted, and the PR session commits named paths". Pair it with one guard recorded in the ledger: the coordinator does not remove, clean or reuse a worker's worktree until its PR session has committed. Confidence 65 percent. Strongest reason: it is the only option that does not depend on an unverified reading of the worker contract and adds no owner questions. This equals the spec's recommended answer ("No; the PR session commits"), with the guard added. The guard closes the one real weakness the debate found.

## What would change the answer

If the gap between a worker finishing and its PR session committing turns out to be long, or a worker's uncommitted change is ever lost, the owner should prefer per-Task commits (proposal A) for the Tasks at risk. If the owner answers Q25 with the alternative (a top-level agent per PR item and no workers), Q32 governs nothing.

## Criticality rating

- Security or trust boundary: low
- Reversibility: easy
- Who is affected: only this program
- Needs the owner's own intent, taste or knowledge that no file holds: partly
- Cost if the answer is wrong: low
- Does it grant authority or accept a risk in writing: yes
- Debate: converged
- Suggested handling: NEEDS-HUMAN
- Reason for the suggested handling in two sentences: The question decides whether agents receive a git write permission, and WC-9 lets a worker commit only on the owner's own quoted words, which no agent can supply. The recommended "no" equals the default and grants nothing, so the question can safely wait until the first code-changing worker is dispatched, as the spec already plans.

## Debate record

- Folder: `/home/coder/workspaces/worktrees/IronClaude/issue-339-orchestrator-mode/.dev/brainstorms/20261113-orchestrator-tui-alignment/owner-questions/Q32/adversarial/` (diff-analysis.md, round1-advocate-1/2/3.md, debate-transcript.md, base-selection.md, refactor-plan.md, merge-log.md, return-contract.yaml); merged text: `Q32/merged-output.md`.
- fallback_mode: false. The three advocates and the merge step ran as spawned agents. The diff, scoring and plan were done by the orchestrating session, and both scoring passes ran in that one context, so they were not independent. The skill was loaded once in this session (for Q31) and followed as written for Q32 without loading it again.
- Status "partial": the protocol says to break a tie between the top two variants, but here all three were within the 5 percent band. The tie-break by debate points was applied across all three. Under the strict top-two reading, proposal C would have been the merge base. The recommendation rests on the unanimous debate vote either way.
