# Q19 final: which of the reviewer's four asks comes first, and in which program?

Q19 asks which of four improvements a reviewer requested on issue #409 (the observer dashboard) on 2026-11-11 should be built first, and whether the observer (`superclaude observe`, the read-only terminal dashboard of agent workers) or the sweep (the coordinator's read-only report, Orchestrator mode Phase 1, still in the open PR #539) carries it. The four asks are: Fleet Quilt and Decision Desk (two of the twenty synthetic design images in the #409 package), Loop Detector or Mission Pulse (named steps with green, yellow, red), and a plain-English summary with issue and PR links.

## Debate result

Winner: proposal C's direction (Fleet Quilt or Decision Desk first, in the observer, started after the contract note and the shared capture), merged with proposal A's finding as the second ask. Confidence 55 percent. The advocates split 2 of 3: the advocates for B and C judged C best (60 and 55 percent); the advocate for A kept A (60 percent). On the 11 scored points they agreed on 10 (91 percent), but the points divided between A and C: C won the "which ask", "which program" and "fit with the reviewer's order" points; A won the data-source, release-gate and sweep-rule points. The scoring tiebreaker (points won, 5 against 4) made A the merge base, and the merge plan rebuilt its answer around C's direction. This is recorded as a split.

Evidence that decided it:
- The asks are screen designs (ADJ line 93), and the reviewer was looking at the dashboard. The sweep's report is "a dated local file; it is never posted" (WORKER-CONTRACT.md line 288), and the recommended answer to Q17 keeps sweep facts off the dashboard for now (merged-requirements.md line 544). So A's summary would not reach the person who asked.
- Review 01, the source of A's data finding, itself says to "choose the direction first among Fleet Quilt, Decision Desk, Signal Bridge, then add only the fields those need" (review 01 line 167, cited by advocate 2).
- But only A's ask has a known, deterministic source today: the task title and `Command:` lines from the Orca Task brief, which the sweep already reads, and step states from the handoff files workers must write (review 01 lines 84 and 86; WORKER-CONTRACT.md line 64). That is why it is kept as the second ask rather than dropped.

Proposal A (summary and named steps first, in the sweep). Strength: the only buildable-now ask, with no release 3 gate and no language model. Weakness: lands in a report the reviewer never sees, blends two asks, departs from the spec and review 05, and needs a new file read for the sweep whose allow-list status is UNVERIFIED.

Proposal B (pick no first ask yet). Strength: honest that every release 3 input is open (QUESTION-LINK "Not established", review 05 line 66; questions read dark and the AC-S record missing, ADJ line 187). Weakness: identical to the default (merged-requirements.md line 546), ties the choice to gates only Decision Desk needs, and leaves the reviewer without an answer. Its own advocate judged C better.

Proposal C (Fleet Quilt or Decision Desk first, in the observer). Strength: follows the spec (line 546), review 05 (D7) and review 01's direction-first order, meets condition (2) of observer release 3 (OB-09, line 257), and designs against confirmed field meanings. Weakness: leaves a choice of two; Decision Desk waits for QUESTION-LINK and two other gates; Fleet Quilt has no recorded data source, so "first" does not mean "soon".

All three advocates flagged that the priority "Fleet Quilt and Decision Desk first" is review 05's reading of the reviewer's comment; review 01 verified the comment exists (review 01 line 34) but no source read shows the reviewer ranking the asks.

Merged answer: OUT/Q19/merged-proposal.md.

## Final recommendation

Name Fleet Quilt as the first ask, built in the observer as a new release row, started after the contract note is final and the shared read-only capture is recorded; its first step is writing down what data it reads. Record the plain-English summary with named steps as the second ask, whose data the sweep can prepare as a Phase 2 follow-up after PR #539 merges (shown on the dashboard only if Q17 later says yes). Before recording this, re-read the reviewer's 2026-11-11 comment on #409 to confirm the order.

Confidence: 55 percent.

Single strongest reason: the reviewer asked for dashboard screens, and only an observer screen reaches them; Fleet Quilt is the screen candidate that does not wait on the unestablished QUESTION-LINK gate.

Equals the spec's recommended answer: partly. The spec says "Fleet Quilt or Decision Desk first, in the observer, after the note and the shared capture"; this recommendation picks Fleet Quilt within that and adds the summary as a recorded second ask.

## What would change the answer

If the reviewer's comment, re-read, shows the summary and links mattered most, proposal A becomes the better first ask. If QUESTION-LINK is established soon, Decision Desk overtakes Fleet Quilt, because its data question is then answered.

## Criticality rating

- Security or trust boundary: none
- Reversibility: easy
- Who is affected: only this program
- Needs the owner's own intent, taste or knowledge that no file holds: yes
- Cost if the answer is wrong: low
- Does it grant authority or accept a risk in writing: no
- Debate: split
- Suggested handling: NEEDS-HUMAN
- Reason for the suggested handling in two sentences. Which screen comes first is a product priority that rests on what the reviewer and the owner value, and no file records a ranking. The advocates split 2 of 3 and the scoring and the majority pointed at different proposals, so an agent should not settle it.

## Debate record

- Folder: /home/coder/workspaces/worktrees/IronClaude/issue-339-orchestrator-mode/.dev/brainstorms/20261113-orchestrator-tui-alignment/owner-questions/Q19/adversarial/ (diff-analysis.md, round1-advocate-1.md to round1-advocate-3.md, debate-transcript.md, base-selection.md, refactor-plan.md, merge-log.md, return-contract.yaml)
- fallback_mode: false (three advocate sub-agents and a merge-executor sub-agent were spawned; the diff analysis, scoring and refactor plan were done by this worker session in the orchestrator role)
