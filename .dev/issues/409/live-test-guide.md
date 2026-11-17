# Live test: `superclaude observe` (PR #503)

Run this from a real terminal (not inside Claude Code) before merging. Time: about 20 minutes.
Every step has a pass line. Write PASS or FAIL and a note next to each.

## What you are testing

A read-only terminal screen that shows Orca's worker list. It calls only
`orca orchestration worker-list --json --limit 100` (plus optional `--run` and `--cursor`),
once every 15 seconds, at most 5 calls per read. No key or option sends anything to Orca.

## 0. Setup (once)

```bash
cd /home/coder/workspaces/worktrees/IronClaude/issue-409-mvp
git fetch origin && git checkout ironbelly/issue-409-mvp && git pull --ff-only
uv sync                                   # installs the branch in editable mode
uv run superclaude observe --help         # lists --once --width --ascii --fixture --run --snapshot
orca --version                            # must work; the observer finds orca on PATH
```

Pass: help text prints with all six options; `orca --version` prints a version.

Use a terminal at least 80 columns by 24 rows. Use a second terminal for the "Orca side" steps.

## 1. Offline replay (no Orca at all)

```bash
uv run superclaude observe --once --fixture base
uv run superclaude observe --once --fixture base --width 80
uv run superclaude observe --once --fixture injection --ascii
```

| # | Acceptance criterion | Pass when |
|---|---|---|
| 1.1 | Output is labelled as fake | First line contains `SYNTHETIC FIXTURE base, not Orca data` |
| 1.2 | Widths hold | With `--width 80` no line is longer than 80 columns (`... --width 80 \| awk '{ if (length($0)>80) bad=1 } END { print bad?"FAIL":"PASS" }'`) |
| 1.3 | Hostile text is inert | `injection` output has no escape characters: `... \| grep -c $'\x1b'` prints `0` |
| 1.4 | Counts show both numbers | Counts read like `shown x/y`, `collected n`, `reported T`; nothing says only a bare total |

## 2. Live read, once

```bash
uv run superclaude observe --once --snapshot /tmp/observe-live.json
```

| # | Acceptance criterion | Pass when |
|---|---|---|
| 2.1 | Real data, not fixture | No `SYNTHETIC FIXTURE` line; worker ids match `orca orchestration worker-list --json` in your other terminal |
| 2.2 | Next-action is verbatim | A row's next-action text equals Orca's `projection.nextAction.kind` for the same worker |
| 2.3 | Unknown is never zero | Any field Orca omits prints `unknown`, never `0`, `false` or blank |
| 2.4 | Gap notice is present | The notice that questions are not read (question source UNVERIFIED) is on screen |
| 2.5 | Snapshot is valid | `jq '.schemaVersion, (.rows\|length)' /tmp/observe-live.json` prints a version and a row count equal to the collected count; file mode is 600 (`stat -c %a /tmp/observe-live.json`) |
| 2.6 | Snapshot holds no secrets | `grep -ci -E 'token\|password\|secret' /tmp/observe-live.json` prints `0`; no message bodies or prompts |
| 2.7 | Read-only | Nothing changed in Orca: compare `orca orchestration worker-list --json` before and after (same workers, same states) |

## 3. Live screen (interactive)

```bash
uv run superclaude observe
```

| # | Do this | Pass when |
|---|---|---|
| 3.1 | Watch 30 seconds | Screen redraws without visible flicker or blinking (this is a human-only check, nothing automated covers it) |
| 3.2 | `j` / `k` or Down / Up | Selection moves one worker at a time and stays on the same worker id if rows reorder |
| 3.3 | `Enter` | Inspector opens with every id in full and wrapped, absent fields read `unknown (absent in source)` |
| 3.4 | In the inspector, `d` then `u` | Fields scroll; a line says `n more fields below (d)` / `n fields above (u)`; on a 24-row terminal nothing is cut off and the selected worker does not change |
| 3.5 | `Esc` | Back to the list |
| 3.6 | `/` type part of an id, `Enter` | List narrows; counts show filtered and global totals (`k of n`) |
| 3.7 | `h` | Historical rows toggle; the hidden count is shown beforehand (`k historical hidden (h)`) |
| 3.8 | `m` | Marks "now"; later a changed worker is starred and the line `changed since HH:MM (n)` appears |
| 3.9 | `e` | A text record is written under `${XDG_STATE_HOME:-~/.local/state}/` (the screen says where) and a snapshot beside it; files are mode 600 |
| 3.10 | `q`, and separately Ctrl-C | Terminal returns to normal: cursor visible, typed characters echo, no raw mode left behind. Test again after Ctrl-Z then `fg` |

## 4. Failure and freshness behaviour

| # | Do this | Pass when |
|---|---|---|
| 4.1 | Start the observer with no Orca on PATH: `mkdir -p /tmp/emptybin && PATH=/tmp/emptybin .venv/bin/superclaude observe --once` | Prints `worker-list NOT AVAILABLE (no Orca CLI validated)` and `collected unknown / reported unknown`; no stack trace; no zeros shown (checked on this branch; exit code is 0, so judge by the text) |
| 4.2 | Start live, then stop the Orca runtime or block it for about 60 seconds, then restore it | The freshness cell goes `STALE` after about 45 s with values kept as last read ("as of HH:MM:SS"), never reported as failed or cleared; recovers to `OK` once Orca answers |
| 4.3 | Resize the terminal to 80, then 79 columns | At 80 the full layout still fits; below 80 it reads `terminal too narrow (min 80)` and still shows the gap notice |
| 4.4 | `NO_COLOR=1 uv run superclaude observe --once` | No colour escape codes in the output (`\| grep -c $'\x1b'` prints `0`) |
| 4.5 | One Run only: `uv run superclaude observe --once --run <a real run id>` | Only that Run's workers appear; a value starting with `-` is rejected, not passed to Orca |

## 5. Load check

While 3.x is running, in another terminal: `ps -ef | grep 'orchestration worker-list' | grep -v grep`.
Pass: at most one worker-list call at a time, about one read every 15 seconds. Running two observers doubles the load; that is expected.

## Known gaps (do not fail the merge on these; they are stated on the PR)

- Your dated selection record (acceptance AC-S in `acceptance-tests.md`) is not part of this PR.
- The 80-column footer cuts the key list.
- Three Low review notes are open: the discovery probe bypasses the argv checks (`adapter.py:301`), a run id ending in a newline passes the pattern (`adapter.py:37`), and two exports in the same second share a file name (`export.py:192`).

## Merge decision

Merge when sections 1, 2 and 3 pass fully and 4.1, 4.2 and 4.4 pass. Any FAIL in 2.5 to 2.7 or 3.10
(wrong snapshot, secrets, a write to Orca, a broken terminal) blocks the merge.

Running this live against Orca is also your confirmation of "production integration" under
`release-gates.md` (reading 1). Record that decision in your selection record if you want AC-S to be satisfied.
