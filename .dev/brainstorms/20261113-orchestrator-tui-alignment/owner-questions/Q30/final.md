# Q30 final: which coordinator Run may OB-04 read, and do you accept in writing that its questions may be consumed?

Terms used here: the observer (`superclaude observe`) is the read-only terminal dashboard of Orca workers (issue #409), and its coordinator-questions panel is switched off by a guard in the code. OB-04 is the one recorded live attempt of that panel in a real coordinator layout; OB-06 is the PR that switches the guard on and needs OB-04's record. OB-03 is the earlier seeded test on a throwaway Run. In Orca, a Run is one coordinated piece of work and a coordinator is the person-opened session that holds it. "Consumed" means a message is removed from the mailbox by being read, so the coordinator never sees it. Gate test Q-1 showed that only the terminal holding a Run can read its questions.

## Debate result

Winner: proposal C (a disposable representative Run the owner opens for the test, never the program's own), amended. Confidence 85 percent. All three advocates picked C (3 of 3), including the advocates assigned to A and B.

Deciding evidence:
- OB-04's own acceptance criterion requires a Run that "carries no work whose questions matter; the Run is disposable and representative (a live `--wait` listener and an ack cycle)" (`merged-requirements.md:252` (1)). Only C meets it and also produces the record OB-06 needs (`merged-requirements.md:254` (c)).
- Whether the observer's read consumes questions on a live coordinator Run is unproven both ways (X-016, 61 percent, ADJ `:144`, `:333`), so risking a real question (proposal B) is not justified.
- All three advocates found the same gap in C as written: it finishes the question-and-acknowledgement cycle before the read, so nothing is pending and the attempt would prove nothing. And a plain `check` to look for a lost question itself removes messages (ADJ `:97`).

Proposal A (hold OB-04): it cannot lose a question or produce a false record, and it is the spec's own fallback (`merged-requirements.md:252` (4)). But it never answers the question: the questions panel never ships and OB-03's result can never become a switch-on. It survives as the written fallback.

Proposal B (a real Run from the owner's ordinary work at a quiet moment): it is the most realistic layout with no setup, and it alone named a before-and-after check. But it breaks OB-04's "carries no work whose questions matter", risks a real question while consumption is unproven, and its "quiet moment" removes the pending question that makes the test meaningful.

Proposal C (disposable representative Run): it meets the criterion, adds exactly what the seeded test lacks (a live listener and an acknowledgement cycle), and puts nothing of value at risk. Its costs are setup (an owner-opened coordinator session, a test worker and its worktree, Orca reachable) and realism limited to the mechanism.

## Final recommendation

Name a disposable coordinator Run that you open only for this test, never the alignment program's own, and accept in writing that questions in it may be consumed. Run it only after the seeded test (OB-03) passes and Orca answers. First check that the observer can run at all in that coordinator's own terminal; if not, record "not usable" and hold the switch-on PR. Then start one test worker that asks one known question, and run the observer's read while that question is still unanswered. Judge loss by whether that known question still reaches the coordinator's `--wait` and is answered and acknowledged, never by a plain `check`. Record the Run id, terminal, result and Orca build string, then close the test Run, worker and worktree. Confidence 85 percent.

Strongest reason: it is the only choice that meets OB-04's own criterion and still produces the live evidence the switch-on PR needs, with nothing of value at risk.

Equals the spec's recommended answer: yes, with the test procedure tightened (read while the question is pending; loss judged against the known question; a terminal preflight; hold as the fallback).

## What would change the answer

If the preflight shows the observer cannot be used in a terminal that holds a coordinator session, OB-04 is held (proposal A) and the owner decides whether to narrow the panel's scope.

## Criticality rating

- Security or trust boundary: low
- Reversibility: easy
- Who is affected: only this program
- Needs the owner's own intent, taste or knowledge that no file holds: partly
- Cost if the answer is wrong: low
- Does it grant authority or accept a risk in writing: yes
- Debate: converged
- Suggested handling: NEEDS-HUMAN
- Reason for the suggested handling in two sentences. The question itself asks the owner to accept a risk in writing and to grant a live Orca read, and only the owner can open the person-opened test coordinator. The debate converged, so the recommendation is safe to present as is, but the acceptance must be the owner's own words.

## Debate record

- Folder: `/home/coder/workspaces/worktrees/IronClaude/issue-339-orchestrator-mode/.dev/brainstorms/20261113-orchestrator-tui-alignment/owner-questions/Q30/adversarial/` (merged answer: `../merged-output.md`)
- fallback_mode: false (three advocate agents spawned in parallel; diff analysis, scoring, plan and merge done by this worker in-context, recorded in `return-contract.yaml`)
