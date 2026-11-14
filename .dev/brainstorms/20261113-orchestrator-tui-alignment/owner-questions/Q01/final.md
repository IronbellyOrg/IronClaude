# Q1 final: how to fix the git-config hole in the sweep's `git status` calls, and which channels the fix covers

**Part (a) is already answered by the owner: "fix" (owner update of 2026-11-13, relayed by the team lead; not accept, not F3).** This file covers only the two open parts: (a2) the fix shape and (b) the channel scope.

Terms used here: the sweep is `superclaude sweep`, the read-only report command in the open pull request #539. INV-008 is the debate's name for the finding that the sweep's `git status` can start a program that some git configuration on this host names. F1 means fixing by neutralising (every worktree is still scanned, and no configured program can run); F2 means fixing by refusing (a worktree where a configured program could run is not scanned and is shown as `unscanned`). The six channels are the six routes measured running a program on 2026-11-13: the fsmonitor hook, clean filters, process filters, included config (`include.path`/`includeIf`), per-worktree config, and `GIT_CONFIG_*` and other inherited environment. SW-01 is the work item that records the owner's ruling on the PR's security thread; SW-02 implements it.

## Debate result

Two debates were run. The first (`adversarial/`, proposals A, B, C in this folder) compared fixing against accepting; all three advocates chose fixing (62 percent), which the owner has since decided. The second (`a2/adversarial/`, proposals in `a2/`) compared fix shapes and is the one that answers the open parts.

Winner of the shape debate: proposal A of `a2/` (F2, refuse and report `unscanned`, counting a program only when it could run for that worktree), amended, confidence 60 percent. Agreement: 3 of 3, including the advocates for "let the PR author choose" and for the combination. Convergence 100 percent. By document score the combination was 2.5 points ahead; the protocol's tiebreaker (debate points won: 7 against 1) chose F2.

Deciding evidence: refusing never alters a result, it only withholds one, so a wrong rule fails visibly, while neutralising fails silently if one route is missed (the probe already showed that turning off fsmonitor left the clean filter running). The spec's acceptance criteria require the owner's ruling to name the shape: SW-01 (1), "A dated owner ruling names F1, F2 or F3" (`merged-requirements.md:190`). And two host facts found on 2026-11-14 decide how F2 must be worded: the system git configuration (`/etc/gitconfig`) defines a git-lfs filter for every repository on this host, and this session's environment carries two `GIT_CONFIG_*` keys (`credential.*`) that name no program. A literal "refuse any worktree that defines a filter" would therefore refuse every worktree; the rule must count a program only when it could actually run for that worktree.

- **F2, refuse and report (winner).** Strength: one behaviour; results never silently wrong; the narrower counting rule keeps the git-lfs filter from refusing everything. Weakness: withholds git facts from worktrees that use only fsmonitor, for no security gain; its first draft overclaimed that refusal covers routes nobody listed (a rule can refuse only what it detects; corrected).
- **Let the #539 author pick F1 or F2.** Strength: puts the engineering choice next to the code and asked for the reasoning to be recorded in the PR (kept). Weakness: fails SW-01 (1); the author is not yet named (Q33); the security choice would be made late, inside a 1003-file PR (its advocate conceded).
- **Combination (neutralise by default, refuse where neutralising could change the answer).** Strength: keeps most git facts, and contributed the two-sided regression test (kept). Weakness: on filters it gives the same result as F2; its extra judgement, "could change the answer", is harder and unmeasured; two behaviours to build and review.

## Final recommendation

(a2) Fix by refusing (F2): a worktree where any in-scope route names a program that the sweep's `git status` could actually run for that worktree is not scanned and is reported `unscanned` with its reason; anything the check cannot classify is refused the same way; no JSON key is added. (b) All six routes are in scope as a minimum, and the ruling names any route it deliberately leaves out. The ruling also states: an environment setting counts only when it names such a program (the session's credential keys do not); the git-status scope is kept separate from the other reads that share its path list today; the regression test must fail both if a program runs and if a worktree that should be refused is scanned; the PR author records how and why in the PR, and the owner reviews it before merge. Confidence 60 percent. Strongest reason: of the two shapes, only refusing can never show a wrong git state as if it were right.

Equals the spec's recommended answer: partly. The spec recommended "F1 or F2" and "yes to all" channels; the debate picks F2, keeps "yes to all", and adds the counting rule the host facts require. The full merged text is `a2/merged-proposal.md`; the earlier fix-versus-accept text is `merged-proposal.md`.

## What would change the answer

A count showing that many of the 29 listed worktrees use only fsmonitor (so F2 would withhold their git facts for no security gain) would make the combination the better answer.

## Criticality rating

- Security or trust boundary: high
- Reversibility: easy
- Who is affected: only this program
- Needs the owner's own intent, taste or knowledge that no file holds: partly
- Cost if the answer is wrong: medium
- Does it grant authority or accept a risk in writing: yes
- Debate: converged
- Suggested handling: NEEDS-HUMAN
- Reason for the suggested handling in two sentences. The ruling authorises an edit to the owner-signed list of allowed git commands, and the spec requires the owner's own dated ruling to name the shape. The choice also trades git facts the coordinator sees against a single, visible failure mode, which is the owner's call.

## Debate record

- Shape and scope debate: `/home/coder/workspaces/worktrees/IronClaude/issue-339-orchestrator-mode/.dev/brainstorms/20261113-orchestrator-tui-alignment/owner-questions/Q01/a2/adversarial/`, fallback_mode false.
- Earlier fix-versus-accept debate (part (a), now answered): `/home/coder/workspaces/worktrees/IronClaude/issue-339-orchestrator-mode/.dev/brainstorms/20261113-orchestrator-tui-alignment/owner-questions/Q01/adversarial/`, fallback_mode false.
- In both, three advocate sub-agents and one merge-executor sub-agent were spawned; scoring and plans were done inline by this worker.
