# Q18 final: a channel copying the observer snapshot to the TUIBBS host?

Q18 asks whether to build a channel that copies the observer snapshot (the JSON file the read-only worker dashboard `superclaude observe` rewrites every cycle, kept private with file mode 0600) from the Coder workspace to the separate SSH host where TUIBBS runs (TUIBBS is the owner's separate TUI platform).

## Debate result

Winner: proposal A (no channel now; the channel item, CO-04, opens only when the observer reaches its release 4, the remote fleet, or when the owner states that a TUIBBS screen is planned). Confidence 70 percent. The advocates agreed 3 of 3: the advocates for B and C both judged A best overall (70, 72 and 65 percent). Convergence 91 percent (10 of 11 points; one wording point, how the contract note mentions a future off-host copy, split three ways and was resolved by the orchestrator in the merge plan). On the scoring rubric B edged A by 2 points (0.876 against 0.856) because B lists the design pieces in more detail; A was selected by the tiebreaker, debate points won (8 against 2).

Evidence that decided it:
- The owner's own record says the observer "may become a TUIBBS module" and marks it "Background, not deciding" (ADJ line 306, quoting a record in a sibling worktree that was not re-read today, UNVERIFIED as to exact wording). A records exactly that; B turns it into a "yes" and C into a "no" that the record does not contain. Both of their advocates conceded this.
- The spec says no transport is chosen until Q4 (what "TUI Panel" means), Q18 and the real authentication behaviour are settled (merged-requirements.md line 375), and Q4's working reading is the observer itself, single-host, at about 70 to 75 percent, with TUIBBS at about 15 percent (line 531).
- Waiting is cheap: if TUIBBS later becomes the reader, "the contract still holds; only the transport changes" (line 1177).

Proposal A (not yet). Strength: matches the record, the spec default (line 545) and the single-host scope (lines 145, 453); keeps CO-04's written preconditions (transport, identity envelope, age rule, re-sanitising) attached to the item; smallest cost if wrong. Weakness: it did not mention data exposure; its "owner statement" trigger is only prompted through Q4 (line 1177); it overclaimed that a later channel needs no change to the snapshot file (identity and age pieces may need new fields).

Proposal B (yes, design the channel now). Strength: the snapshot was shaped for this reader (ADJ line 91), designing the seam once on paper avoids two ad hoc transports, and it alone named the data exposure: copying a mode 0600 file off the workspace widens who can read it (ADJ line 244). Weakness: it needs an owner statement nobody has, runs against the spec's ordering (line 375), and designs one end of a channel whose other end has no document ("No document in TUIBBS mentions Coder or Orca", round2-rebuttal-V5.md line 20).

Proposal C (no, drop the item). Strength: the smallest attack surface and a clean basis for closing Coder#477 (the workspace listener issue in the IronbellyOrg/Coder repository) under Q3 (ADJ line 773). Weakness: no source supports "no"; deleting CO-04 also deletes its written security preconditions, so a future channel would start from nothing.

Merged answer: OUT/Q18/merged-proposal.md (A plus: who may read a copy, and whether the whole snapshot or only part leaves the host, as a fifth required piece of the CO-04 design; Coder#477 wording "no channel exists; one is deferred"; the overclaim removed; a guard sentence in the contract note that any future off-host copy is read-only and waits for CO-04's design; the ledger as the authoritative record). The merge-executor flagged two leftover "four pieces" counts; the orchestrating session corrected them to five and recorded the edit in merge-log.md.

## Final recommendation

No copy channel now. Keep CO-04 deferred until observer release 4 or until you state that a TUIBBS screen is planned. When it opens, its design must name five things before any code: transport, identity of the source workspace, an age rule, re-cleaning of untrusted text, and who may read the copy (including whether the whole snapshot or only part leaves the host). Tell Coder#477 that no channel exists and one is deferred.

Confidence: 70 percent.

Single strongest reason: the only fact that could justify a yes or a no is your own plan for TUIBBS, and your recorded position is "background, not deciding"; deferring with written triggers keeps every option open at almost no cost.

Equals the spec's recommended answer: yes. The merged additions (the fifth design piece and the guard sentence) refine it.

## What would change the answer

If you state that a TUIBBS screen is planned (or answer Q4 with "TUIBBS"), proposal B becomes the right answer, and the CO-04 design should start with the five pieces above. If you state that no TUIBBS screen will be built, proposal C becomes right, provided the five pieces are kept as a standing rule for any future off-host copy.

## Criticality rating

- Security or trust boundary: high
- Reversibility: easy
- Who is affected: other people or repos
- Needs the owner's own intent, taste or knowledge that no file holds: yes
- Cost if the answer is wrong: low
- Does it grant authority or accept a risk in writing: no
- Debate: converged
- Suggested handling: NEEDS-HUMAN
- Reason for the suggested handling in two sentences. The deciding fact is whether the owner plans a TUIBBS screen, which no file holds, and the question decides whether a private file may ever cross to another host, with the answer echoed on an issue in the separate IronbellyOrg/Coder repository. The default if unanswered already does the safe thing, so a delayed answer costs nothing.

## Debate record

- Folder: /home/coder/workspaces/worktrees/IronClaude/issue-339-orchestrator-mode/.dev/brainstorms/20261113-orchestrator-tui-alignment/owner-questions/Q18/adversarial/ (diff-analysis.md, round1-advocate-1.md to round1-advocate-3.md, debate-transcript.md, base-selection.md, refactor-plan.md, merge-log.md, return-contract.yaml)
- fallback_mode: false (three advocate sub-agents and a merge-executor sub-agent were spawned; the diff analysis, scoring and refactor plan were done by this worker session in the orchestrator role)
