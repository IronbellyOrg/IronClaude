# Q24 final: who runs the shared read-only capture and the join comparison?

Three live Orca tasks need a named runner. Orca is the local app that runs agent workers. The tasks are: the shared read-only capture (XC-03, wave W1: read-only Orca commands recording a few fields nobody has seen yet), the one-time join comparison (XC-04, wave W3: matching the observer's worker ids against a sweep's row ids on one real Run, after PR #539 merges), and the observer's seeded consumption test (OB-03, wave W1: it writes test messages to a throwaway Run under its own permission row). The observer is the built dashboard `superclaude observe` (issue #409). The sweep is the coordinator's read-only report (PR #539).

## Debate result

Winner: proposal A (a fresh, dedicated session in its own master-based Orca worktree, not the 409 session), with additions, confidence 65 percent. Agreement: 2 of 3 advocates judged A best overall. The proposal B advocate conceded owner time and chose A. The proposal C advocate held to C, with A as its fallback. Point agreement 8 of 10 (80 percent, at the threshold); unresolved: who runs the seeded test, and whether any agent should hold live-read rows at all. A scored 0.910 against C's 0.887 and won on the tiebreaker of debate points.

Deciding evidence:
- The join comparison must run the sweep "on master code" (merged-requirements.md line 452), but the 409 session's worktree `issue-409-mvp` is on an unmerged branch (`f104ca51a`; `origin/master` is not an ancestor: line 234).
- That worktree holds unpushed commits and records that must survive until the owner commits or archives them (lines 249, 264).
- Whether the 409 session is still alive is unverified.
- ADJ's "one sitting" no longer holds, because the comparison moved to W3 (line 861). ADJ is the adjudicated findings file `.dev/reviews/orchestrator-tui-alignment-20261113/adversarial/alignment-findings-adjudicated.md`.

The proposals:
- **Proposal A (fresh master-based session).** Strength: it exists on demand, fits the master-code requirement natively, and cannot damage the 409 evidence. Weakness: more coordinator work and no observer history. Its own step "remove the worktree" would have deleted the sweep report (`sweep/commands.py:235-241`); this is fixed in the merge.
- **Proposal B (owner by hand).** Strength: no agent holds live-read authority, and it fits the owner authoring the seeded-test record. Weakness: three live sittings of the owner's time, which is this program's bottleneck (line 523), and no defined master-code environment for the comparison.
- **Proposal C (the 409 session).** Strength: a record of running these probes safely (Task 16 and 17 samples, `.dev/issues/409/bmad/spec-orca-observer/release-gates.md:43,45`), and it knows the observer's fields. Weakness: no fallback if it has ended, an unmerged worktree, evidence at risk, and one session would hold three permission rows, one of them a write.

Finding shared by all three advocates: the Q-1 failure (2026-11-11) blocked only the mailbox read `orca orchestration check --all ... --run <id>` (`.dev/tasks/to-do/TASK-WF-release2OfTheOrc-20261111-203306/artifacts/q1-result.md`). It did not block `worker-list`. So a terminal that holds no Run can probably still list another Run's workers, but this is UNVERIFIED and should be the capture's first recorded read.

## Final recommendation

The coordinator creates a fresh master-based Orca worktree with its own agent (for example `orca-capture`). That session runs the read-only capture in W1 and the join comparison in W3, each under its own live-read permission row. It does this from a terminal it has read back as holding no Run, and its first recorded read is one `worker-list --run <id>` of another terminal's Run. It is handed the observer's verified field list and may ask the 409 session questions, but the 409 session runs nothing. The sweep report is copied into the ledger package before the worktree is removed. The seeded test stays with the owner, who also writes its record, unless the owner names another runner in writing.

Confidence 65 percent. Strongest reason: it is the only runner that is certain to exist, runs on master code as the comparison requires, and cannot touch the 409 worktree's unsaved evidence. Equals the spec's recommended answer: no. The spec names the 409 session and "one sitting"; the debate found the sitting is now two waves apart, and the 409 worktree is on an unmerged branch. Merged text: `merged-proposal.md`.

## What would change the answer

If W0 intake (XC-10) confirms the 409 session is alive, holds no Run, and can run the installed sweep against master from a folder outside its worktree, then proposal C (the spec's answer, with this proposal as fallback) becomes as good and saves a worktree.

## Criticality rating

- Security or trust boundary: low
- Reversibility: easy
- Who is affected: only this program
- Needs the owner's own intent, taste or knowledge that no file holds: partly
- Cost if the answer is wrong: medium
- Does it grant authority or accept a risk in writing: no
- Debate: converged
- Suggested handling: NEEDS-HUMAN
- Reason for the suggested handling in two sentences. The answer decides which actor makes live Orca calls and who runs the one test that writes messages, which is a delegation choice. The recommendation also departs from the spec's answer, and the debate only just reached its agreement threshold. Only the owner knows whether the 409 session is alive and how much of their own time they will spend.

## Debate record

- Adversarial folder: `.dev/brainstorms/20261113-orchestrator-tui-alignment/owner-questions/Q24/adversarial/` (diff-analysis.md, round1-advocate-V1/V2/V3.md, debate-transcript.md, base-selection.md, refactor-plan.md, merge-log.md, return-contract.yaml); merged text `Q24/merged-proposal.md`.
- fallback_mode: false. The three advocates and the merge executor were spawned as sub-agents; diff analysis, scoring and base selection were done by this worker in the debate-orchestrator role.
