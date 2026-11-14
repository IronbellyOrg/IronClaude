# Q3 final: keep, narrow or close Coder#477 (the workspace listener issue)

Terms used here: Coder#477 is an open issue in the separate repository `IronbellyOrg/Coder`, titled "Workspace listener, monitor registration and secure prompt routing for every Coder workspace". The watcher is IronClaude's issue watcher (issue #331), built as a poller inside each workspace with no listener (its design decision D1, option A). The observer is `superclaude observe`, the read-only terminal dashboard of Orca workers (issue #409); its planned release R4 would read a remote fleet. TUIBBS is the owner's separate TUI platform on another host. Texts A, B and C are the ready-made replies in ADJ Part 6.3 (narrow, keep, close). CO-01 is the work item that posts the reply.

## Debate result

Winner: proposal A (narrow to read-only workspace status and identity, with no prompt routing), confidence 55 percent. Agreement: 2 of 3 advocates recommended it when neutral (60 and 55 percent); the advocate for proposal C recommended closing at 55 percent, but only if the owner answers Q4 with "single-host" and Q18 with "no TUIBBS channel yet". All three ranked proposal B (keep) last, at about 5 percent or less. Every debate point reached at least a 2-of-3 majority (convergence 100 percent on points).

Deciding evidence: the owner commented on Coder#477 on 2026-11-13, "Ensure this aligns with Orchestrator and TUI Panel" (read-only `gh issue view`, 2026-11-14), which asks for alignment, and only narrowing answers it concretely. Narrowing removes every route that could start a permission-free session (checklist item 9) and keeps the one real gap (the observer cannot see another workspace). The ADJ ranks narrow at about 65 percent and keep as "the least defensible" (ADJ lines 283, 605).

- **Proposal A (narrow).** Strength: keeps the visibility gap and the owner's alignment request, removes the send route, makes the nine-item checklist a test requirement for any later build. Weakness: text A is not paste-ready (an "owner decides" age, an UNVERIFIED owner-token route, a name that must match the contract note); it designs for readers that do not exist yet (it depends on observer R4); and it effectively replaces the issue's problem statement, because the issue's written body served only the watcher.
- **Proposal B (keep with guards).** Strength: the only proposal that writes strong guards onto prompt routing (fixed request list, one-use expiring grants, separate read and request credentials, refuse rather than queue). Weakness: contradicts the owner's recorded watcher design with no recorded revisit condition (`docs/designs/issue-watcher.md:39`, `:49`); largest attack surface; blocked on a grant format that does not exist; a listener cannot start a stopped workspace. Its text stays on record in ADJ Part 6.3.
- **Proposal C (close).** Strength: fewest owner decisions, honest that nothing in IronClaude waits on #477, clear reopen conditions tied to R4 or a TUIBBS task. Weakness: goes against the owner's comment of one day earlier; text C, called paste-ready, still holds "[link to the comment holding option A]" (ADJ line 661); once closed, the gap is easy to miss.

## Final recommendation

Narrow Coder#477 to read-only workspace status and identity with no prompt, command or session-start route, posted as text A after its placeholders are filled, with the one-line Q4 answer. If, when answering Q4, you say the observer stays single-host for good and no TUIBBS screen or remote reader is planned, close it instead with text C (after fixing its link placeholder) and its two reopen conditions. Each post needs its own grant row naming each write, including the state change if closing. Confidence 55 percent. Strongest reason: it is the only option that answers your own request that #477 align with the Orchestrator and the TUI panel while removing the remote path to permission-free sessions.

Equals the spec's recommended answer: yes ("Narrow; close if single-host and TUIBBS not near"), with additions: narrowing replaces the issue's problem statement, text C's link placeholder must be fixed, and the grant row must name a close. The full merged text is `merged-proposal.md`.

## What would change the answer

An owner statement that the observer stays single-host and that no TUIBBS screen or remote reader is planned makes proposal C (close) the better answer.

## Criticality rating

- Security or trust boundary: low
- Reversibility: easy
- Who is affected: other people or repos
- Needs the owner's own intent, taste or knowledge that no file holds: yes
- Cost if the answer is wrong: low
- Does it grant authority or accept a risk in writing: no
- Debate: converged
- Suggested handling: NEEDS-HUMAN
- Reason for the suggested handling in two sentences. The answer writes to an issue in another repository and turns on what the owner meant by a comment posted one day earlier, which only the owner knows. The advocates' overall pick was also 2 of 3, with close preferred if the owner's plans for TUIBBS and a second host are what the third advocate assumed.

## Debate record

- Adversarial folder: `/home/coder/workspaces/worktrees/IronClaude/issue-339-orchestrator-mode/.dev/brainstorms/20261113-orchestrator-tui-alignment/owner-questions/Q03/adversarial/`
- fallback_mode: false (three advocate sub-agents and one merge-executor sub-agent were spawned; scoring and the plan were done inline by this worker)
