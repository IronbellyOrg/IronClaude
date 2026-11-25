## Bug Summary

Opening a new plain Claude tab through `ccsession-orca` runs `ccsession --ask`, which builds the saved-session list before it asks for a name. With 477 saved names the list takes 22.5 to 27.1 s (measured) and prints nothing until it is complete, which reproduces the reported 20 seconds. The root cause and the remediation are in "Troubleshoot findings" below (status: partial).

## Environment (OS, version)

- OS: Linux 6.8.0-147-generic (Coder workspace), 28 cores; bash 5.2.37, GNU coreutils; `LANG=C.UTF-8`, `LC_ALL` unset.
- Version: `ccsession` of origin/master 10f6ec670 (2072 lines; the installed copy `~/.claude/skills/ccsession-tag/ccsession` is byte-identical; the file is unchanged through e3e9d636a). A checkout cut before that holds an older 1902-line copy, so its line numbers differ.
- Store: 19 name lists, 589 topic files (477 in this repo's list), 437 workspace folders, 1741 transcripts, 23 GB under `~/.claude/projects`.

## Current Behavior

`time ccsession --here` (the list that `--ask` shows): 27.069 s real, 5.823 s user, 13.566 s sys at load average 11.9, and 22.471 to 24.663 s at lower load; `time ccsession --list`: 14.473 s. The terminal shows nothing until the whole list is built (`ccsession:1718`); then the 30 s question starts inside Orca's 60 s readiness window. The reported 5-10% CPU was not reproduced: 19.4 s CPU over 27.1 s wall is about 0.7 of one core, about 2.5% of this 28-core machine.

## Expected Behavior

The list is built in a few seconds, with a number of process spawns that does not grow per saved name, and with no change to any output text, exit code (0, 1, 3, 130), row order, here/gone/other classification, or the rule "Listing never writes any file". Derived, not yet measured: about 14.6 s after Stage 1 and about 2.7 to 4.6 s after Stage 2 on this store (see "Success measure and gates").

## Steps to Reproduce

1. On a machine with a large `~/.claude/projects` store: `time ccsession --here >/dev/null`.
2. Per-function time: `PS4='+T ${EPOCHREALTIME} ${FUNCNAME[0]:-main} ' bash -x ~/.local/bin/ccsession --here >/dev/null 2>/tmp/ccs-xtrace.log`, then sum the gap between consecutive trace lines per function.
3. Locale effect: alternate `time ccsession --here` and `time env LC_ALL=C ccsession --here`, three times each.

All three are read-only (listing writes no file).

## Impact Assessment (Severity, Blast Radius)

- Severity: medium. Every new plain Claude tab waits 22 to 27 s with a silent terminal; no data is lost.
- Blast Radius: every `ccsession-orca` terminal open and every `ccsession --ask`, `--here` and `--list` on a machine with a large list. The Coder New Terminal hook was not checked.

## Error Messages

```text
None: the terminal is silent until the list is built.
```

## Codebase Context

Line numbers below are of the installed copy (identical to origin/master 10f6ec670); the details are in "Troubleshoot findings".

- `ccsession-orca:204` calls `ccsession --ask`; `ask_session_name` shows the list through `show_saved worktree` (`ccsession:1715-1735`), which captures `list_sessions` whole (`ccsession:1718`).
- `list_sessions` (`ccsession:1554-1663`): per row, `head -n 1` (1594), `session_transcript` (1599, `ls -t "$PROJECTS_DIR"/*/<uuid>.jsonl`, 1482), `session_home` (1607, the `head | tail | grep | awk` pipeline, 1396-1397), `session_place` (1608), `get_btime` and `get_mtime` (1610, 1611), two `format_epoch` (1616, 1617: `date -r` first, which fails on GNU, then `date -d`, 1535-1536).
- `local ... LC_ALL=C` at 1383 and 1403 is not exported, so `grep` runs in the user's UTF-8 locale.

## Related Issues

None found (scout search "ccsession launch slow").

## Testing Notes

See "Tests" and "Success measure and gates" below.

