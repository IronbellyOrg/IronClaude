# Q10 final: may the sweep ever read Orca's pending questions, or is that the observer's job alone

Q10 is owner question 10 of the alignment spec. The sweep (`superclaude sweep run`, the read-only report a coordinator session makes about its workers, PR #539) may run only the exact Orca commands on an owner-signed allow-list (NFR-014); `check`, the command that reads a Run's messages, is not on it. The observer (`superclaude observe`, the read-only terminal dashboard) has a question panel that would use `check --all --types question`, switched off until the owner answers Q6 and its tests pass. SW-07 is the spec's work item that corrects the sweep's wording after PR #539 merges; wave W3 is the batch of work after that merge.

## Debate result

- Winner: proposal C (the observer's alone for now; correct the sweep's text now), amended. Confidence 73 percent (mean of the advocates' verdicts: 75, 70, 75).
- Agreement: 3 of 3. The advocates for A ("yes, later") and B ("never") both chose C amended. All ten debate points had a majority; three were unanimous. In scoring, C and A were within 5 percent, and C won on the tiebreaker (8 of 10 debate points).
- Deciding evidence: whether `check --all --types question` removes messages on a live coordinator Run is unproven both ways (contradiction X-016 in ADJ, the adjudicated alignment findings document, line 333), and ADJ rules that the sweep's current text overclaims and should state only what is established (line 813). Checked on 2026-11-14: the coordinator already receives every question through its own wait, which wakes on `question` messages and handles each batch before acknowledging it (`src/superclaude/core/WORKER-CONTRACT.md:100-103`), so a sweep read would add only a second view.

Proposal A (yes, later, through one new allow-list entry after the consumption tests pass). Strength: the sweep runs inside the coordinator's own session, the only terminal that can read that Run (gate test Q-1 failed). Weaknesses: its main benefit already exists through the coordinator's own wait; the planned tests deliberately avoid the coordinator's own live Run (`merged-requirements.md:252`), which is exactly where the sweep would read; and the sweep is forbidden to act on anything it reports (worker-contract rule WC-16). Its own advocate voted C.

Proposal B (never, and change the text only once, after the seeded test). Strength: a clear permanent split (sweep: workers and worktrees; observer: questions) and a single wording change. Weaknesses: it keeps a sentence ADJ rejected in the shipped sweep for an undated time, and its proposed final sentence names the observer as the reader while that read is switched off. Its own advocate voted C, keeping B's point that any sweep read needs a new owner signature.

Proposal C (observer's alone for now; fix the text now). Strength: zero cost, matches the spec default, and depends on no live test. Weakness as drafted: it applied the same three-sentence text to two different places, one of which (`report.py:199`) is a short, true header value pinned by a test; and it had no reopen condition. Both fixed in the merged answer.

## Final recommendation

The sweep does not read questions; only the observer may, for now. After PR #539 merges, correct only the sweep's bullet that says questions "cannot be read without consuming them" (`report.py:534-535`) to: "This command reads no messages. A plain `check` consumes them. Whether `check --all --types question` consumes on a live Run is not established." Keep the header "Messages coverage: partial" (`report.py:199`), which is true. Any future sweep read needs a new owner-signed allow-list entry. Reopen Q10 when the seeded and live consumption tests have results, or if Q6 parks the observer's read; if the seeded test shows consumption, the answer becomes "neither program reads questions". Confidence 73 percent.

Single strongest reason: it removes the sweep's one unproven claim now, without depending on any live test and without widening the allow-list, and the coordinator already gets its questions through its own loop.

Equals the spec's recommended answer: partly. The answer is the same ("observer's alone for now; correct the sweep's two sentences"), but the correction applies to the bullet only, so SW-07's acceptance criterion (3), which says both lines carry the exact text (`merged-requirements.md:196`), needs rewording; and a reopen condition is added.

## What would change the answer

If the live attempt (OB-04) showed the observer's panel unusable in the real layout while the coordinator's own session could read safely, the sweep (A) would become the better place to show questions.

## Criticality rating

- Security or trust boundary: low
- Reversibility: easy
- Who is affected: only this program
- Needs the owner's own intent, taste or knowledge that no file holds: partly
- Cost if the answer is wrong: low
- Does it grant authority or accept a risk in writing: no
- Debate: converged
- Suggested handling: SAFE-FOR-AGENT-RECOMMENDATION
- Reason for the suggested handling in two sentences: The recommendation keeps the owner-signed allow-list unchanged, grants nothing, and only corrects a sentence that the adjudicated review already found overstated. The one owner-level choice, whether the sweep may ever read messages, is explicitly left for a later owner signature with a stated reopen condition.

## Debate record

- Folder: `/home/coder/workspaces/worktrees/IronClaude/issue-339-orchestrator-mode/.dev/brainstorms/20261113-orchestrator-tui-alignment/owner-questions/Q10/adversarial/`
- fallback_mode: false (three advocates spawned in parallel as separate agents; merge by a merge-executor agent; depth quick, Round 1 only)
