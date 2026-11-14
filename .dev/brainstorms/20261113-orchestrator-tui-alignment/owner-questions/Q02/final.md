# Q2 final: the watcher's claim level and written acceptance of permission-free sessions for its first live test

Terms used here: the watcher is the issue watcher (issue #331, rollout issue #450), a poller that starts a Claude session running `/sc:issue --claim <N>` when an issue is approved. `--pipeline none` makes that claim stop after assigning the issue and posting comments; the default level, `worktree`, also creates a worktree `issue-<N>` and starts a second governed agent that stops at a plan. FU-1 is the watcher's first live test on one test issue. WA-01 is the small watcher code change, WA-02 the edits to issue #450, WA-04 the live test itself. OB-H1, OB-H2 and OB-H3 are the claim command's hook gates (ship gates) from its launch-level design.

## Debate result

Winner: proposal C (`--pipeline none`, and a written acceptance of permission-free sessions for the one test issue only), confidence 72 percent (mean of the advocates' neutral recommendations: 70, 75, 70). Agreement: 3 of 3, including the advocates for A and B. Convergence 100 percent (13 of 13 points). Note on the protocol: the document-score step chose proposal B as the frame because it was the most complete on preconditions, but B lost every core point 3 of 3, so the merge replaced B's answer with C's (`adversarial/base-selection.md`, `adversarial/refactor-plan.md` Change 1).

Deciding evidence: `--pipeline none` matches the owner's recorded design decision D2, "claim-only ... The claim stops at `next-steps.md`" (`docs/designs/issue-watcher.md:44`), and the built default is a confirmed accident (ADJ line 372, 91 percent); it halves the permission-free sessions; a one-issue acceptance is bounded and authorises no later issue (`merged-requirements.md:572`).

- **Proposal A (claim-only, decline the acceptance, FU-1 waits).** Strength: the only option that does not rely on the assumption that a permission-free session makes only the writes the claim intends. Weakness: blocks all learning and everything downstream with no end condition; a permission-on unattended session may not be feasible, and Orca's own default flags may also need changing (`README.md:578`, UNVERIFIED). Kept as the fallback if a precondition cannot be met.
- **Proposal B (keep the default `worktree` level, gated on the ship gates).** Strength: the only proposal that named the ship gates as FU-1 preconditions and said plainly FU-1 waits (won that point). Weakness: ratifies an accident against the owner's recorded decision, doubles the permission-free sessions, creates unowned worktrees and agents per approval, and its "what an approval most plausibly wants" has no source.
- **Proposal C (claim-only, one-issue acceptance).** Strength: matches D2, one session, unblocks the cron schedule, the sweep's machine-started label and the deferred handoff design work once FU-1 runs. Weakness: it said "FU-1 can run" while the gate that binds a claim at any level, OB-H1 item 5, is recorded "Pending, none run" (`docs/designs/sc-issue-launch-level-hook.md:625`); it omitted the live-test grant row (`merged-requirements.md:331`, `:719`), Orca availability and Q20. The merge added all four.

All three advocates rejected two shared assumptions: that Q2 alone covers FU-1's outward writes (a separate `GRANT(WA-04,live-test)` row is required), and that the FU-1 write list bounds what a permission-free session could do (it is the intended list, not a limit).

## Final recommendation

Set the watcher to `--pipeline none` and accept in writing, for the one FU-1 test issue only, that its session runs with permission checks off; the acceptance covers whatever that one session does on the test issue, not only the listed writes. FU-1 then waits until OB-H1 item 5 has passed, the live-test grant row is recorded, Orca answers on this host and Q20 is answered. Writing the test issue's text yourself shrinks the untrusted-input risk. Confidence 72 percent. Strongest reason: it is the answer the owner already recorded as design decision D2, with the smallest permission-free exposure that still lets the live test happen.

Equals the spec's recommended answer: yes, with additions the debate found missing from both the spec row and the proposals: the four FU-1 preconditions (one of them, OB-H1 item 5, recorded as not yet run) and the acceptance wording. The full merged text is `merged-proposal.md`.

## What would change the answer

If the owner states that an approved issue should produce a ready plan waiting for a person (so design decision D2 no longer reflects intent) and OB-H1 items 1 and 5, OB-H2 and OB-H3 are shown passed, proposal B becomes the better answer.

## Criticality rating

- Security or trust boundary: high
- Reversibility: easy
- Who is affected: only this program
- Needs the owner's own intent, taste or knowledge that no file holds: partly
- Cost if the answer is wrong: medium
- Does it grant authority or accept a risk in writing: yes
- Debate: converged
- Suggested handling: NEEDS-HUMAN
- Reason for the suggested handling in two sentences. The second half of the question is, by definition, the owner's written acceptance that a session reads untrusted issue text with permission checks off, which no agent may give. The claim level could be recommended safely, but it is bundled with that acceptance and with the owner's own reading of what an approval should deliver.

## Debate record

- Adversarial folder: `/home/coder/workspaces/worktrees/IronClaude/issue-339-orchestrator-mode/.dev/brainstorms/20261113-orchestrator-tui-alignment/owner-questions/Q02/adversarial/`
- fallback_mode: false (three advocate sub-agents and one merge-executor sub-agent were spawned; scoring and the plan were done inline by this worker)
