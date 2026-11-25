# Execution locus

PRINT-SITE: Issue 540 reports done.json MISSING alongside results/return-contract.yaml on lea-ironclaude-work.
RUN-SITE: src/superclaude/cli/swarm/commands.py:2145 and :2165 @ reported remote throwaway workspace; local reproduction pending
SAME-ENV: no
OBSERVE-VIA: artifact-file
CONTROL-PROOF: unknown

## Local check
PRINT-SITE: local-foreground-1 CLI stdout and artifacts/foreground/{return-contract.yaml,.swarm-state.json}; read-only filesystem check captured done_exists=false.
RUN-SITE: src/superclaude/cli/swarm/commands.py:2145-2169 @ current worktree .venv/bin/superclaude, stub transport, dedicated artifacts/home
SAME-ENV: yes
OBSERVE-VIA: same-shell
CONTROL-PROOF: unknown
re-run permitted: yes (user explicitly asked to execute the quoted diagnostic command, including simulated-worker reproduction and isolated HOME)
Historical remote evidence remains artifact-only; no remote commands were run.
