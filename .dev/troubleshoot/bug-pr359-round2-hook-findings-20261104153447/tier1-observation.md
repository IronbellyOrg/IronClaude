# Tier 1 observation (round 2)

## Trace probe (2026-11-04T15:35:13Z, same-shell, local worktree, command: bash /home/coder/workspaces/worktrees/IronClaude/bare-python-hook-357/.dev/troubleshoot/bug-pr359-round2-hook-findings-20261104153447/trace-probe.sh src/superclaude/hooks/scripts/block-bare-python.sh)
```
== \[\[ a \]\]; python3 x
hook_exit=0
== < <(printf "") python3 -c 1
cmdword=printf
hook_exit=0
== echo $(( `python3 -c 1` + 1 ))
cmdword=echo
hook_exit=0
```
Reading: for the escaped `\[\[` input no command word is printed at all (the word opened the test context and the rest of the line was swallowed); for the process-substitution input only `printf` is chosen; for the arithmetic input only `echo` is chosen. The hook exits 0 for all three.

## Bash behaviour observation (2026-11-04T15:35:13Z, same-shell, fake python3 first on PATH, bash 5.2.37(1)-release)
```
\[\[ a \]\]; python3 x => bash: line 1: [[: command not found FAKE-PY ran 
< <(printf "") python3 -c 1 => FAKE-PY ran 
echo $(( `python3 -c 1` + 1 )) => bash: line 1: FAKE-PY ran + 1 : syntax error in expression (error token is "ran + 1 ") 
"[[" a ]]; python3 x => bash: line 1: [[: command not found FAKE-PY ran 
```
