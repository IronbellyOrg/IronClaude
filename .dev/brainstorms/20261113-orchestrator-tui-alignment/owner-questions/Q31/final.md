# Q31 final: does the owner's 10-minute recurring check apply to this program's coordinator?

Terms used here: the coordinator is the Claude session that runs this program and supervises its worker sessions. WC-16 is the worker contract's coordinator-loop rule (`src/superclaude/core/WORKER-CONTRACT.md:288`): re-arm the Orca wait whenever it expires, and run the status sweep at most once every 5 minutes. Orca is the app that runs agent sessions and carries their messages. The ledger (work item XC-01) is the program's on-disk record of owner answers.

## Debate result

Winner: proposal C ("yes, read-only, for this program's coordinator"), confidence 70 percent (the mean of the three advocates' own overall judgments: 75, 65, 70). The three advocates agreed 3 of 3, including the advocates assigned to argue for A and for B. Per-point agreement was 14 of 14 points by majority, 8 of 14 unanimous.

Deciding evidence: the order exists because "Peer sessions (interactive, not Orca workers) do not appear in the Orca message queue at all" (memory `coordinator-never-stop-polling.md`). This program will have such peers: the pull request sessions of Q25 (the question about who runs PR submission) and the #539 author session of Q33. WC-16 sees person-started sessions only through `/sc:sweep` (the read-only status report command), and the spec records `/sc:sweep` as "not runnable" until PR #539 merges and the install route of Q29 runs (`merged-requirements.md` line 1031). So in the early waves only a timer-driven check sees those peers go idle.

- **Proposal A (no, WC-16 loop only).** Strength: the whole cadence is auditable from one checked-in file, with no 7-day cron expiry and no question about whether a cron fire triggers the sweep pass. Weakness: it overrides a standing owner order on the strength of a WC-16 sentence ("Phase 1 adds this duty, not a scheduler") that the spec itself reads as "not a ban on the owner's check" (line 1016) and probe finding INV-010 (`adversarial/adversarial/invariant-probe.md:18`) reads the same way. Its own advocate conceded it leaves non-worker peers unwatched.
- **Proposal B (yes, and write it into the worker contract for every coordinator).** Strength: it fixes the root cause INV-010 found, that the order lives only in memory, the lowest source tier. Weakness: it turns a one-program question into a change to an installed core file that every project receives, adds a PR during a program whose bottleneck is owner latency (line 523), and leaves the report style and cron expiry handling open. Its own advocate conceded the contract change should be a separate item.
- **Proposal C (yes, read-only, this program).** Strength: it answers at the scope asked, handles the cron's real limits (job id and 7-day expiry kept in the ledger, re-created on expiry or resume), applies the 2026-11-09 order to report only decisions, and keeps the spec's limit "Q31 does not authorize `/sc:sweep` above WC-16's cap or any write" (line 579). Weakness: the rule stays in memory and the ledger, and it can silently stop if a re-creation is missed. The merge corrected one overstatement and added that the cron fires only while the coordinator is idle (`Q31/merged-output.md`).

## Final recommendation

Answer "yes, read-only, for this program's coordinator", confidence 70 percent. Strongest reason: it is the only option that watches the program's non-worker sessions before the sweep command is runnable, and that unwatched-peer failure is exactly why the owner gave the order. This equals the spec's recommended answer ("Yes, read-only"). The debate adds four clarifications: the check runs only while the coordinator is idle, idle subscriptions send no message, the ledger entry for the cron job is the coordinator's own note, and putting the rule into the worker contract is a separate later decision.

## What would change the answer

If the owner says the 2026-11-05 order has been withdrawn or narrowed since it was given (the note is 9 days old and is the lowest source tier), proposal A becomes better. If the owner wants every future coordinator bound by it, proposal B becomes better.

## Criticality rating

- Security or trust boundary: low
- Reversibility: easy
- Who is affected: only this program
- Needs the owner's own intent, taste or knowledge that no file holds: yes
- Cost if the answer is wrong: low
- Does it grant authority or accept a risk in writing: no
- Debate: converged
- Suggested handling: NEEDS-HUMAN
- Reason for the suggested handling in two sentences: The question asks the owner to confirm their own standing order, which lives only in a memory note, and the spec says it "does not pick an answer from memory either way", so an agent answer would be the silent pick the question exists to avoid. The stakes are low and the default is safe, so it is a quick one-line answer for the owner.

## Debate record

- Folder: `/home/coder/workspaces/worktrees/IronClaude/issue-339-orchestrator-mode/.dev/brainstorms/20261113-orchestrator-tui-alignment/owner-questions/Q31/adversarial/` (diff-analysis.md, round1-advocate-1/2/3.md, debate-transcript.md, base-selection.md, refactor-plan.md, merge-log.md, return-contract.yaml); merged text: `Q31/merged-output.md`.
- fallback_mode: false. The three advocates and the merge step ran as spawned agents. The diff, scoring and plan were done by the orchestrating session, and both scoring passes ran in that one context, so they were not independent.
