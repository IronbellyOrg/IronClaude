# Zellij check (optional, not a gate)

Status: NOT RUN in a live Zellij pane. Zellij is never a dependency of the observer, and the observer may read `ZELLIJ` only as a hint.

## What was checked (2026-11-18)

- `zellij --version` on this machine: `zellij 0.44.2` (installed at `/usr/local/bin/zellij`).
- `zellij action dump-screen --help` on that release lists: `-a, --ansi` (keep ANSI styling), `-f, --full` (full scrollback), `-p, --pane-id <PANE_ID>` and `--path <PATH>`. The online docs describe a newer release, so the flags above are the ones to use on 0.44.2.
- `ZELLIJ` is not set in the session that built this change, so there was no Zellij pane to dump.

## What was not done and why

Running the observer in a Zellij pane and dumping it with `zellij action dump-screen --ansi` needs an interactive terminal with a live Zellij session. An agent cannot drive a live Zellij session, so the check was not run agentically; colour, box-glyph and wide-glyph fidelity inside Zellij are UNVERIFIED. The owner did not decline the check (owner ruling 2026-11-18: record it as a note, not as a decline); it stays open for a person to run with the steps below.

## If the owner wants it

1. In a Zellij 0.44.2 session, in a pane of at least 160 columns: `superclaude observe --fixture base` (and again with `--questions`).
2. From another pane: `zellij action dump-screen --ansi --path /tmp/observe-zellij.ansi` with the observer pane focused (or `--pane-id <id>`).
3. Compare the dump with `.dev/tasks/to-do/TASK-WF-redesignSpec-20261118-043319/artifacts/gates/final/160/ledger.truecolor.ansi`: colour depth kept (truecolor, 256 or 16), box glyphs `╭╮╰╯┏┓┗┛` intact, `█` and `●` one cell wide, no `?` where a wide glyph stood.
4. Record the result in this file.
