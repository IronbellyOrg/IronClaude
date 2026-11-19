7e37592576e06e816ef57c9b864a8e7a6459e5fb
family desk-state-role: a desk field row misses its STATE_ROLE.
search: grep -n -F -e "_absent_role(value)" src/superclaude/cli/observe/render.py
before: the raw dispatchStatus, terminalState and outcome rows use _absent_role only
coupled sites: the workerState row and the liveness row already take STATE_ROLE
after: the three raw rows take STATE_ROLE.get((name, value)) first
