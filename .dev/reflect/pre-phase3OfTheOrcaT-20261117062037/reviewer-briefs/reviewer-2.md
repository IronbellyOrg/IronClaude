# Reviewer 2, persona: qa

Read /home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/reflect/pre-phase3OfTheOrcaT-20261117062037/reviewer-briefs/common.md first and follow it.

Your lens: is each requirement in source.md actually proven by an acceptance criterion that a reviewer can check, and would the stated checks fail if the behaviour were wrong? For every INF row, find the acceptance bullet that proves it, or say it is unproven. Check the safety claims (read-only argv log, no raw payload or body kept, question text never in the snapshot or the record, injection and markup inert, unknown never shown as zero) for a real test, not only a constraint. Check that tasks are independently reviewable (a task's reviewer sees only that task and the Constraints), that "Depends on" is correct, that test names and files exist or are created by an earlier task, and that no acceptance bullet is vague or circular.
