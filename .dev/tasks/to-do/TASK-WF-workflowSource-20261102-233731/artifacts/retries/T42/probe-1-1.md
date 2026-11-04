247e399a9ce196927a16b1a6189e68fa6f7e16b7
family=worktree-branch-checked-out
defect form: git worktree add <path> <branch> recipe for a branch that is usually checked out elsewhere (master)
command: grep -n -e "git worktree add" -- CONTRIBUTING.md KNOWLEDGE.md
before:
CONTRIBUTING.md:29:git worktree add .dev/worktrees/master-check master
coupled sites: git worktree list (main clone on [master]); CLAUDE.md worktree examples use -b <new branch> (not affected)
after:
CONTRIBUTING.md:30:git worktree add --detach .dev/worktrees/master-check master
