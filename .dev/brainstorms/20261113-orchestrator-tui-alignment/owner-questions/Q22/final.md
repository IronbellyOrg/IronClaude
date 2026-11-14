# Q22 final: what age makes a snapshot or workspace record stale?

The snapshot is the JSON file `snapshot.json` that the observer (`superclaude observe`, the read-only terminal dashboard of Orca workers, issue #409) writes. A workspace record is the read-only status record a future Coder feature (issue Coder#477 in the separate Coder repository, not built) would publish per workspace. Neither file has a "still alive" flag, so a reader can only judge it by its `generatedAt` time.

## Debate result

Winner: proposal A (a rule, not a number), as refined in the debate, confidence 70 percent. Agreement: 2 of 3 advocates judged proposal A best overall (the proposal B advocate conceded its own interim rule is defective and backed A); the proposal C advocate preferred C's number for the observer but proposed the same hybrid as the proposal A advocate. Every one of the 10 debate points had a majority (convergence 100 percent by majority). Proposal A scored 0.928 against C's 0.891 and won on the tiebreaker of debate points (6 to 3).

Deciding evidence, checked in the code on 2026-11-14: the observer rewrites the snapshot once per cycle "after failures too" (`src/superclaude/cli/observe/commands.py:294-297`), polls every 15 s and waits up to 60 s after errors, with a cycle of up to 15 s (`collector.py:28-30`). So a live observer can leave a gap of about 75 s between writes (an inference from these constants, not a measurement). The snapshot also already carries the observer's own data-freshness verdict in `source.status` and `source.observedAt` (`view.py:543-553`), so the file's age measures whether the writer is alive, a different question from whether the data is fresh.

- **Proposal A (stale = older than three producer intervals).** Strength: reuses the rule the observer already applies to its own feed (`view.py:32-34`), sets numbers per producer when each is designed, keeps the interval in the contract note so no new key enters the file. Weakness: as first written, 45 s marks a live observer's file stale during error backoff.
- **Proposal B (no number now, keep the interim rule).** Strength: no reader exists yet (the Coder implementation CO-03 and the TUIBBS copy channel CO-04 are deferred), so nothing is fixed against a guess. Weakness: the interim "older than one cycle" rule (about 15 s) flickers with ordinary timing; its own advocate conceded this.
- **Proposal C (one fixed number, 2 minutes).** Strength: one plain number; 120 s is above the observer's worst live write gap. Weakness: the 2 minutes for the Coder record is a guess against a producer that does not exist, and it leaves the TUIBBS channel about 45 s for transport.

## Final recommendation

Answer with a rule: a snapshot or workspace record is stale when its `generatedAt` age exceeds the larger of three times its producer's normal writing interval and that producer's longest normal gap between writes (error backoff included). For the observer snapshot that is about 75 s today. Readers always print the age, show file age and data age separately, and print "age unknown" (never "current") when the computed age is negative or implausible; the Coder record and the TUIBBS copy channel get their numbers when each is designed. Confidence 70 percent. Strongest reason: it is the only answer that matches how the one real producer actually writes, without guessing numbers for producers that do not exist. Equals the spec's recommended answer: no. The spec recommended "the owner's number" with no value; this gives a rule that yields the number (merged text: `merged-proposal.md`).

## What would change the answer

If you want one plain number in the Coder issue text above all else, proposal C (one number, at least 2 minutes) is better; and if a measurement shows the observer's real write gap is much longer than 75 s, the observer number moves with it.

## Criticality rating

- Security or trust boundary: none
- Reversibility: easy
- Who is affected: other people or repos
- Needs the owner's own intent, taste or knowledge that no file holds: partly
- Cost if the answer is wrong: low
- Does it grant authority or accept a risk in writing: no
- Debate: converged
- Suggested handling: NEEDS-HUMAN
- Reason for the suggested handling in two sentences. The rule itself is grounded in code and reversible, but the spec explicitly reserves this as "the owner's number", how quickly the owner wants a dead writer flagged is a matter of taste, and the answer ends up in text posted to another repository's issue (Coder#477). An agent can safely draft the rule, but the owner should confirm it.

## Debate record

- Adversarial folder: `.dev/brainstorms/20261113-orchestrator-tui-alignment/owner-questions/Q22/adversarial/` (diff-analysis.md, round1-advocate-V1/V2/V3.md, debate-transcript.md, base-selection.md, refactor-plan.md, merge-log.md, return-contract.yaml); merged text `Q22/merged-proposal.md`.
- fallback_mode: false (three advocates and the merge executor were spawned as sub-agents; diff analysis, scoring and base selection were done by this worker in the debate-orchestrator role).
