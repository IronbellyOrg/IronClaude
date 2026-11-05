# Tier 1 observation
Captured 2026-11-04T15:03:43Z, run: same-shell, arm: local worktree, command: bash /home/coder/workspaces/worktrees/IronClaude/bare-python-hook-357/.dev/troubleshoot/bug-pr359-bare-python-hook-findings-20261104150317/probe.sh src/superclaude/hooks/scripts/block-bare-python.sh
Output file: /home/coder/workspaces/worktrees/IronClaude/bare-python-hook-357/.dev/troubleshoot/bug-pr359-bare-python-hook-findings-20261104150317/probe-baseline.out (verbatim below)

```
== finding 1 (ANSI-C) ==
hook_exit=0 scanner_out=<none>   | $'\160ython3' -c 1
hook_exit=0 scanner_out=<none>   | $'\x70ython3' -c 1
hook_exit=0 scanner_out=<none>   | $'\u0070ython3' -c 1
hook_exit=2 scanner_out=python3  | $'python3' -c 1
== finding 2 (long options) ==
hook_exit=0 scanner_out=<none>   | timeout --signal TERM 30 python3 x
hook_exit=0 scanner_out=<none>   | timeout --kill-after 5 30 python3 x
hook_exit=0 scanner_out=<none>   | sudo --user U python3 x
hook_exit=0 scanner_out=<none>   | nice --adjustment 5 python3 x
hook_exit=0 scanner_out=<none>   | env --unset X python3 x
hook_exit=0 scanner_out=<none>   | env --chdir D python3 x
hook_exit=2 scanner_out=python3  | timeout --signal=TERM 30 python3 x
hook_exit=2 scanner_out=python3  | timeout -s TERM 30 python3 x
== finding 3 ([[ ]]) ==
hook_exit=2 scanner_out=python   | [[ "$tool" =~ ^(python|python3|pip|pip3)$ ]] && echo matched
hook_exit=2 scanner_out=python3  | [[ -n x ]] && python3 x
```

Reading: in every case hook_exit tracks scanner_out exactly (empty scanner output -> exit 0, a printed word -> exit 2). The jq, awk and empty-input exits are not involved; the defect is inside the awk scanner.

## Trace probe (2026-11-04T15:07:48Z, same-shell, command: bash /home/coder/workspaces/worktrees/IronClaude/bare-python-hook-357/.dev/troubleshoot/bug-pr359-bare-python-hook-findings-20261104150317/trace-probe.sh src/superclaude/hooks/scripts/block-bare-python.sh)
```
== $'\160ython3' -c 1
cmdword=160ython3
== timeout --signal TERM 30 python3 x
cmdword=30
== [[ "$tool" =~ ^(python|python3|pip|pip3)$ ]] && echo matched
cmdword=[[
cmdword=python
python
```

## Bash behaviour observation (2026-11-04T15:08:37Z, same-shell, fake python3 at /tmp/bbp-fake.YgdROK first on PATH, bash 5.2.37(1)-release)
```
ansi-octal: FAKE-PYTHON3 ran: -c 1
timeout-long: FAKE-PYTHON3 ran: x
nice-long: FAKE-PYTHON3 ran: x
env-long: FAKE-PYTHON3 ran: x
dbl-bracket: matched
```

## sudo/time options and awk %c (2026-11-04T15:16:29Z, same-shell)
```
  -C, --close-from=num          close all file descriptors >= num
  -D, --chdir=directory         change the working directory before running
  -g, --group=group             run command as the specified group name or ID
  -h, --host=host               run command on host (if supported by plugin)
  -p, --prompt=prompt           use the specified password prompt
  -R, --chroot=directory        change the root directory before running command
  -r, --role=role               create SELinux security context with specified
  -t, --type=type               create SELinux security context with specified
  -T, --command-timeout=timeout terminate command after the specified time limit
  -U, --other-user=user         in list mode, display privileges for user
  -u, --user=user               run command (or edit file) as specified user
time: GNU time not installed (bash keyword only)
awk=mawk 1.3.4 20250131 %c(112)=p
```
