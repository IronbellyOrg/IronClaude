## Flag review for this issue

This issue was filed with the flags the user gave. A check at `standard` depth chose differently; the reasons are below. The issue was not reclassified.

| Flag | User's flag | Worker's choice | Reason for the difference |
|---|---|---|---|
| `--mode` | bug | bug | same |
| `--type` | skill | command | The empty-description check is owned by the command file `src/superclaude/commands/issue.md:51-56` (STOP "--create needs a description"), which runs before skill Activation (`src/superclaude/commands/issue.md:108-114`). The named `src/superclaude/skills/sc-issue-protocol/scripts/create_issue.py` was not found in the checkout; the skill's scripts are `origin_repo.py`, `clickup_claim.py` and `orca_worktree.py` (`src/superclaude/skills/sc-issue-protocol/SKILL.md:33-35`). |

<!-- sc:issue:create-review -->
