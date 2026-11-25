# Diagnosability tasklist (informational, invocation-site only, not applied by troubleshoot)

discriminator-required: no
round: not counted (no discriminator rows)
re-run permitted: yes (read-only listing commands)

## Emitter search

- datum: time spent per phase of `ccsession --here` / `--ask` listing
- emitters-found: 0 (existing code never reports phase time; see wave1_6-branch-A.md)
- already-read-files: 3 (ccsession, ccsession-orca, hooks/session-start.sh)
- usable-capture-routes: 1 (external `bash -x` with a PS4 timestamp at the invocation, already used)
- exclusions: hooks do not call the listing path (session-start.sh:45, session-name.sh:202-212)

## Tasks

### Task 1 (executed, result in tier1-observation.md): time-stamped trace at the invocation site
Command (read-only, from a checkout with a large session list): `PS4='+T ${EPOCHREALTIME} ${FUNCNAME[0]:-main} ' bash -x ~/.local/bin/ccsession --here >/dev/null 2>/tmp/ccs-xtrace.log`, then sum the gap between consecutive trace lines per function. Expected observation: self time per function and process counts. Done 2026-11-17: session_home 12.16 s, list_sessions loop 5.12 s, format_epoch 2.68 s, session_transcript 2.03 s, session_place 1.95 s, get_btime 1.22 s, get_mtime 1.20 s, 1756 `date`, 878 `stat`, 477 `ls`.

### Task 2 (pending, optional): confirm per-process cost with strace
Command (read-only): `strace -f -c -o /tmp/ccs-strace.txt ~/.local/bin/ccsession --here >/dev/null 2>&1`. Expected observation: syscall counts dominated by clone/execve/statx/openat; sys time was 13.6 s of 19.4 s CPU in the plain run.

### Task 3 (pending, after a fix): re-measure with the same commands
Run Task 1 and `time ccsession --here` on the same machine and store; compare with 27.07 s wall (user 5.82 s, sys 13.57 s) and 14.47 s for `--list`.
