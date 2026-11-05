# Tier 1 observation (round 3)

## Trace probe (2026-11-04T16:44:46Z, same-shell, local worktree, command: bash /home/coder/workspaces/worktrees/IronClaude/bare-python-hook-357/.dev/troubleshoot/bug-pr359-round3-hook-findings-20261104164446/trace-probe.sh src/superclaude/hooks/scripts/block-bare-python.sh)
```
== python3() { uv run python "$@"; }; echo ready
cmdword=python3
python3
hook_exit=2
== {fd}>/dev/null python3 -c 1
cmdword={fd}
hook_exit=0
```

## Bash behaviour observation (2026-11-04T16:44:46Z, same-shell, fake python3 first on PATH, bash 5.2.37(1)-release)
```
python3() { uv run python "$@"; }; echo ready => ready 
{fd}>/dev/null python3 -c 1 => FAKE-PY ran 
{fd}>/dev/null; echo fd=$fd => fd= 
```

## Reference rows (2026-11-04T16:47:54Z, same-shell, command: hook run per input)
```
hook_exit=2 | 2>/dev/null python3 -c 1
hook_exit=2 | f() { python3 x.py; }
```
