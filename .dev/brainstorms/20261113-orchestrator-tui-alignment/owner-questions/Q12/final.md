# Q12 final: should the observer get a routing entry

Q12 is owner question 12 in the merged requirements (merged-requirements.md:539). Proposal A is "no entry for now"; proposal B is "one sentence in the guide's prose Orca section, not a table row"; proposal C is "one routing-table row, in its own small PR after PR #539 (the sweep PR) merges".

## Debate result

Winner: proposal C, confidence 78 percent. Advocates agreed 2 of 3 on their unassigned pick (the variant each would choose if not assigned one): two picked C, one picked B, none picked A. Every scored diff point had a majority, so the debate converged (adversarial/debate-transcript.md, "Convergence Assessment").

The evidence that decided it:
- `/sc:recommend`, the command people are told to run when unsure which tool fits, reads only three marked blocks of the routing guide: the level table, the routing table and the other-commands table, "never by line number or heading text" (src/superclaude/skills/sc-recommend/SKILL.md:50-54, re-read). A bullet in the prose "Orca coordination" section is outside all three, so it is not routable. All three advocates agreed on this point.
- The test cost proposal C named for itself is probably smaller than stated. INV-029, an invariant-probe finding, says a command-line-only entry fits neither table without a test edit. That holds for the other-commands table, which pins its member list (tests/core/test_how_we_work_routing_table.py:297-298). For the routing table, the test looks up only text that starts with a backtick and a slash (same file, line 105), and the `resume` row already has a plain terminal step (src/superclaude/core/HOW-WE-WORK.md:376). This is a reading, not a test run: UNVERIFIED until the routing tests run on the PR branch.
- The observer is merged (PRs #503 and #514) and no guide, user guide or command file names it today (grep, 2026-11-14).

Proposal A (no entry for now). Strength: changes nothing, cannot collide with PR #539, and avoids writing an entry twice while the observer's coordinator-questions panel is still off (owner question Q6). Weakness: the tool stays invisible with no dated trigger to revisit; the "person only" sentence (INV-013, an invariant-probe finding that only a coordinator or person should run the observer) is written nowhere; its own advocate picked B when unassigned.

Proposal B (prose bullet). Strength: verified to need no test edit, because the tests read only the marked blocks (test file lines 22-24); puts "person only" beside the existing never-as-worker bullet (HOW-WE-WORK.md:405). Weakness: not routable by `/sc:recommend` (verified above), and it rewrites the spec's planned work item OB-07 (the routing-row PR) for a smaller result.

Proposal C (routing-table row). Strength: the only placement both people and `/sc:recommend` use; keeps OB-07 as written; matches the source review's advice "the routing row only, in its own small PR" (variant-5-original.md:258-259). Weakness: it left "which table" open and overstated its own test cost; both are fixed in the merged answer.

## Final recommendation

Answer: yes, one row in the routing table (not the other-commands table) for `superclaude observe`, copied byte-for-byte to the plugin mirror, in its own small PR after PR #539 merges; the worker runs the routing tests before naming any test edit; the row describes only what works on master today and says "Coordinator or person only, never a worker", the same words the `/sc:sweep` entry uses (HOW-WE-WORK.md:335). Confidence: 78 percent. Strongest reason: only a routing-table row is read by `/sc:recommend`, so it is the only entry that makes the tool findable by both people and the recommender. Equals the spec's recommended answer: yes, with the table named and the test-edit claim narrowed (merged-proposal.md).

## What would change the answer

If the routing tests, run on the PR branch, reject a terminal-only row and the fix would loosen a pinned test, proposal B (a prose bullet with no test edit) becomes the better first step.

## Criticality rating

- Security or trust boundary: low
- Reversibility: easy
- Who is affected: only this program
- Needs the owner's own intent, taste or knowledge that no file holds: no
- Cost if the answer is wrong: low
- Does it grant authority or accept a risk in writing: no
- Debate: converged
- Suggested handling: SAFE-FOR-AGENT-RECOMMENDATION
- Reason for the suggested handling in two sentences. It is one reversible row in a guide file, the debate converged, and the question needs no owner taste or private knowledge. The only trust element is the "person only" sentence, which the recommended answer adds rather than relaxes, and the PR itself still needs the owner's separate grant row to open.

## Debate record

- Folder: /home/coder/workspaces/worktrees/IronClaude/issue-339-orchestrator-mode/.dev/brainstorms/20261113-orchestrator-tui-alignment/owner-questions/Q12/adversarial/
- fallback_mode: false (three spawned advocate sub-agents; the diff analysis and the merge were done by this worker directly, as recorded in return-contract.yaml; the protocol skill was loaded by a Skill call at Q11 in this session and applied as written)
