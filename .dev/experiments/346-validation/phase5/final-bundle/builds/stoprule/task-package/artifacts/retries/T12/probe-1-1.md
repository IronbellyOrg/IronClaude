cba8f62c0ce366182fd25019a711cb3682701e92
family staging-incomplete
form: a .dev/tasks file written after the task's git add .dev/tasks stays untracked
command: grep -n -F -e 'git add .dev/tasks' -- /tmp/impl346/complete.sh
before:
9:git add .dev/tasks
untracked .dev/tasks files before the fix: 5
coupled sites: every task's artifact writes after its staging step (complete.sh stages at each complete)
after: untracked .dev/tasks files: 0
