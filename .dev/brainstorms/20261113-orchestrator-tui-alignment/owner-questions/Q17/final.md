# Q17 final: should the observer ever show sweep facts on its Orca-ledger screen?

Q17 asks whether the observer (`superclaude observe`, the built read-only terminal dashboard of Orca workers, issue #409) should ever show facts that only the sweep has (the coordinator's read-only report from Orchestrator mode Phase 1, issue #339, in the still-open PR #539): frozen plans, safe-to-close, waiting-on-a-person and git state.

## Debate result

Winner: proposal B (no sweep-facts panel now; ask again later; only a later "yes" makes storage of the sweep's JSON a real requirement). Confidence 65 percent. The advocates agreed 3 of 3: the advocates for A and C both judged B best overall (62, 70 and 62 percent). Convergence 100 percent on the 11 scored points (9 unanimous, 2 by 2 of 3). On the scoring rubric A and B tied (0.839 against 0.835); B was selected by the tiebreaker, debate points won (9 against 3).

Evidence that decided it:
- The debate's strongest judgement on this point is scoped to "now": "Q17: no observer panel for sweep facts now", 78 percent (ADJ line 361). B matches it; A contradicts it; C stretches it to "ever", which C's own advocate conceded.
- The source disagreement (D-6) was between two reviews wanting sweep facts "eventually" and one saying "optional, later, only if wanted", with "the owner only" as the settling fact (round2-rebuttal-V5.md line 69). "Not now" contradicts neither side.
- Everything a "yes" needs is open: PR #539 is unmerged (ADJ line 78), the sweep JSON is printed to stdout only (ADJ line 131), Q9 (where the sweep JSON lives) recommends "Not now" (ADJ line 779), and Q19 (which reviewer ask comes first) has not chosen Decision Desk (merged-requirements.md line 546).

Proposal A (yes, a sweep-facts panel in observer release 3). Strength: it is right about what a person at the Decision Desk needs: the observer owns none of git, contracts, transcripts, safe-to-close, frozen plans or Task specs (ADJ line 240), and it alone named the freshness gap: sweep facts are always older than live Orca rows because the coordinator sweep is capped at once per 5 minutes, a cap and not a schedule (ADJ line 81). Weakness: it commits a requirement to an unscheduled release (OB-09, observer release 3, is deferred, merged-requirements.md line 257), against unmerged code whose JSON keys are settled only after merge (ADJ line 359), and pulls the storage decision forward against its own recommendation.

Proposal B (not now). Strength: exact fit with the evidence, no dependency on unmerged work, the one-report-file rule (NFR-001) and its two pinned tests untouched (ADJ line 83), and a later "yes" already has its display rule waiting: print the sweep's words verbatim and label the report age (ADJ line 253). Weakness: as first written, "not now" had no trigger and could drift into "never"; it did not mention the freshness gap; a person keeps two places to look.

Proposal C (never, a standing boundary). Strength: the cleanest separation; the two programs use seven shared words with different meanings and incompatible JSON shapes (ADJ lines 131, 250 to 256). Weakness: no source supports "ever"; it closes a door two reviews wanted open, is harder to reverse, and adds an unrequested rule that the sweep never reads observer output.

Merged answer: OUT/Q17/merged-proposal.md (B plus: a written re-ask trigger; the freshness gap recorded in the contract note for any later panel; one sentence asking the Decision Desk layout to leave room for a possible sweep area; Orchestrator v2, unbuilt, named as a possible home for a joined view). The merge-executor flagged one contradiction (the base's "no trigger" sentence against the added trigger); the orchestrating session reworded that sentence and recorded the edit in merge-log.md.

## Final recommendation

No sweep-facts panel on the observer screen now. Record a trigger to ask again: when Q19 picks Decision Desk or observer release 3 is scheduled, and only after PR #539 has merged. Keep the rule that any later panel prints the sweep's own words and the report's age, and add that sweep facts are always older than the live Orca rows beside them.

Confidence: 65 percent.

Single strongest reason: every input a panel would need (the merged sweep, a stored or captured copy of its JSON, a scheduled Decision Desk) is still open, and the only measured judgement on the point says "not now".

Equals the spec's recommended answer: yes. The merged additions (trigger, freshness note, layout room) refine it without changing it.

## What would change the answer

If the owner says Decision Desk is the next observer release and PR #539 has merged, proposal A becomes the better answer, because the person at that screen needs the close-or-wait facts only the sweep has.

## Criticality rating

- Security or trust boundary: none
- Reversibility: easy
- Who is affected: only this program
- Needs the owner's own intent, taste or knowledge that no file holds: partly
- Cost if the answer is wrong: low
- Does it grant authority or accept a risk in writing: no
- Debate: converged
- Suggested handling: SAFE-FOR-AGENT-RECOMMENDATION
- Reason for the suggested handling in two sentences. The recommended answer equals the spec's default, changes nothing that exists, and is reversible at no cost because nothing is built or stored. The part that does depend on the owner's taste (whether the Decision Desk should ever combine both sources) is deferred to a recorded trigger rather than decided now.

## Debate record

- Folder: /home/coder/workspaces/worktrees/IronClaude/issue-339-orchestrator-mode/.dev/brainstorms/20261113-orchestrator-tui-alignment/owner-questions/Q17/adversarial/ (diff-analysis.md, round1-advocate-1.md to round1-advocate-3.md, debate-transcript.md, base-selection.md, refactor-plan.md, merge-log.md, return-contract.yaml)
- fallback_mode: false (three advocate sub-agents and a merge-executor sub-agent were spawned; the diff analysis, scoring and refactor plan were done by this worker session in the orchestrator role)
