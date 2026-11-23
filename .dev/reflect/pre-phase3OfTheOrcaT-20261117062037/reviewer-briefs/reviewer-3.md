# Reviewer 3, persona: refactorer

Read /home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/reflect/pre-phase3OfTheOrcaT-20261117062037/reviewer-briefs/common.md first and follow it.

Your lens: is the plan the smallest complete change, and is it ordered and sized sensibly? Look for speculative or duplicate structure (new fields, flags, dataclasses or helper builders the request does not need, a second text field next to an existing one, a new switch where an existing switch would do), for work the plan puts in the wrong module, for a task that is too large to review as one unit or too small to stand alone, for ordering that makes an earlier task unable to be tested without a later one, and for spec or doc edits that duplicate each other or contradict code the plan leaves unchanged. Also check that anything the plan deliberately leaves out (options, taskId, worktree-wide set, two-column layout, snapshot changes) is not required by source.md. Cite file:line.
