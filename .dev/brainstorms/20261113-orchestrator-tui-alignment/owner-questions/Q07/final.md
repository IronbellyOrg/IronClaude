# Q7 final: who writes the pass record, and saving the owner records that exist only in a side worktree

Q7 is owner question 7 of the alignment spec. The "pass record" is the owner's dated statement (2026-11-12) that approves switching on the observer's coordinator-questions read; the observer is `superclaude observe`, the read-only terminal dashboard of Orca workers. The "sibling worktree" is the separate checkout `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp`, where several owner records exist only as untracked files or unpushed local commits. OB-nn ids are the observer's work items in the spec: OB-01 saves the owner records, OB-06 is the pull request that switches the questions read on, OB-08 corrects the #409 issue text. The ledger (XC-01) is the program's dated decision record.

## Debate result

- Winner: proposal B, merged with parts of A and C (save every record now in a records-only pull request, the pass record included, after the owner re-reads them; the owner commits by default; archive allowed; a dated "do not clean" entry today). Confidence 65 percent.
- Agreement: 2 of 3 on the headline. The advocates for A and B both chose a B-led combination (70 percent each); the advocate for C chose an A-led combination (70 percent) with the same core. On the ten debate points, all ten had a majority; saving the records now (not waiting for the switch-on) and keeping the archive option were unanimous. The 65 percent is discounted from 70 for the remaining split on who makes the commit.
- Deciding evidence: under the spec as written, the pass record reaches master only inside OB-06 (prerequisite (d), `merged-requirements.md:254`), and OB-06 may never open (its default is "not opened" if Q6, the switch-on scope question, is unanswered). Meanwhile the pass record sits in two unpushed local commits that no remote branch holds, and both commits carry an automated co-author trailer (`git log` of `1ae72e1a1` and `f104ca51a` in the sibling, read 2026-11-14), so git cannot show who typed the text (ADJ INV-014; ADJ is the adjudicated alignment findings document, `alignment-findings-adjudicated.md`, and INV-014 is its invariant-probe finding 14, line 478). Cleaning the sibling first deletes the records the switch-on must cite (`merged-requirements.md:264`).

Proposal A (owner writes or re-confirms the pass record and personally commits the other records in wave W1, the first batch of work after intake). Strength: matches the spec rows OB-01 and OB-06 exactly and keeps the rule that agents may cite owner records but never write them (sibling `release-gates.md:22`). Weakness: it lets the sibling be cleaned after OB-01 while the pass record is still only in the sibling, so the record can be lost if the switch-on is parked; A's own advocate conceded this and moved to B.

Proposal B (one dated owner sentence plus a records-only pull request now, byte for byte). Strength: saves every record, the pass record included, independent of the switch-on, with a byte check and "clean only after the merge is verified". Weaknesses: as written an agent session does the commit, which sits against the written rule (B's own advocate voted against B on that point); it drops the spec's archive option; and it requires rewording OB-06 (d) and ADJ line 191.

Proposal C (move nothing; dated freeze; ask again later). Strength: costs nothing now and is the only answer that starts protection today, with a full inventory including `handoff-mvp-brainstorm.md`, which the spec does not name. Weakness: leaves the only copies on one disk for an open-ended time; the freeze is an instruction, not a guard; OB-08 (the #409 correction) stays blocked. Its own advocate voted for A amended with C's freeze.

## Final recommendation

Yes to both, sooner and safer than the spec says. Today, record a dated "do not clean `issue-409-mvp`" entry naming every at-risk file. Then the owner re-reads the files, writes one dated sentence saying they are the owner's text, and commits them unchanged (the pass record included) to master in a small records-only pull request, or names an archive; a session the owner names does the copy only if the owner explicitly rules that acceptable. The switch-on pull request later cites the pass record by its master path. Confidence 65 percent.

Single strongest reason: it is the only answer that removes the single-disk loss risk for every record, the pass record included, whether or not the switch-on ever happens.

Equals the spec's recommended answer: partly. It keeps "yes, both, before the sibling worktree is cleaned", but saves the pass record now in its own pull request instead of inside the switch-on pull request, which needs OB-06 prerequisite (d) reworded to "already on master and cited".

## What would change the answer

If the owner does not want these personal records in the repository at all, the archive route (or C's freeze as a bridge) becomes the whole answer; and if the owner refuses to reword OB-06 (d), plain A becomes best, provided OB-01 also saves the pass record before any cleaning.

## Criticality rating

- Security or trust boundary: low
- Reversibility: easy
- Who is affected: only this program
- Needs the owner's own intent, taste or knowledge that no file holds: yes
- Cost if the answer is wrong: medium
- Does it grant authority or accept a risk in writing: yes
- Debate: converged
- Suggested handling: NEEDS-HUMAN
- Reason for the suggested handling in two sentences: Only the owner can confirm that the files are their own text and only the owner can perform or delegate the commit of their own records, so an agent cannot answer this on the owner's behalf. The answer also puts a written authorship statement on record and may delegate a commit of owner text, which the rule of thumb reserves for a person.

## Debate record

- Folder: `/home/coder/workspaces/worktrees/IronClaude/issue-339-orchestrator-mode/.dev/brainstorms/20261113-orchestrator-tui-alignment/owner-questions/Q07/adversarial/`
- fallback_mode: false (three advocates spawned in parallel as separate agents; merge by a merge-executor agent; depth quick, Round 1 only)
