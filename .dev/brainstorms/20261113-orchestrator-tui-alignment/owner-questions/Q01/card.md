# How to fix the git-config hole in the sweep, and which routes the fix must cover

**Already answered: you chose to fix this hole (not accept it). This card asks only how, and how widely.**

## Question in one sentence
Should the fix stop the sweep from running config-named programs by refusing to scan affected worktrees, by disabling those programs, or by a mix, and which routes must it cover?

## Why you are being asked
PR #539 (the `superclaude sweep` report command) cannot merge until your ruling is posted on its security thread. The project's rules require your ruling to name the fix shape and to authorise the change to the owner-signed list of allowed git commands.

## Background you need
- The sweep runs `git status` in every worktree Orca (the local agent-orchestration app) lists. On 2026-11-13 git started a program named in configuration through six routes: the fsmonitor hook, clean filters, process filters, included config files, per-worktree config, and `GIT_CONFIG_*` and other environment settings.
- Found on 2026-11-14: this host's system git config sets up a git-lfs filter for every repository, and this session's environment carries two harmless `GIT_CONFIG_*` credential settings. A filter only runs for files a repository marks for it.
- So a rule like "refuse any worktree that has a filter configured" would refuse every worktree here.

## Your options
1. **Refuse and report, counting only programs that could actually run.** A worktree where a route names a program that could run for it is not scanned and shows as "unscanned" with the reason; anything unclear is refused too.
   - If you pick this: you post the ruling; the PR author adds a test that fails if any program runs or if a worktree that should be refused is scanned.
   - Upside: the sweep never shows a wrong git state as if it were right; one behaviour to review.
   - Downside: worktrees that use only the fsmonitor speed-up lose their git facts for no security gain.
2. **Disable by default, refuse only where disabling could change the result.**
   - If you pick this: two behaviours are built and tested.
   - Upside: keeps more git facts.
   - Downside: its key judgement ("could this change the result") is harder and unmeasured; more to review in a very large PR.
3. **Let the PR author pick at implementation time.**
   - If you pick this: you rule only the outcome; the author chooses and explains in the PR.
   - Upside: the choice is made next to the code.
   - Downside: the project's rules require your ruling to name the shape; the author is not yet named.

## What the debate found
- All three advocates, including those for options 2 and 3, recommended option 1 with amendments.
- The original draft claimed refusing also covers routes nobody listed; that was wrong and is removed.
- Every option must keep the git-status fix separate from the sweep's other reads that share the same list of paths.

## Recommendation and confidence
Option 1, 60 percent, with all six routes in scope as a minimum and any route you leave out named. This partly matches the spec, which recommended "neutralise or refuse" without choosing.

## If you do not answer
PR #539 stays open, and everything that waits on its merge stays held.

## What this answer does not authorize
Any git allow-list change beyond this fix; a merge of PR #539; the PR tool fixing this on its own; any code design (that stays with the PR author).

## How to answer
Type, for example: "Q1: option 1, all six routes" (or "Q1: option 2, all six routes" / "Q1: option 3").
