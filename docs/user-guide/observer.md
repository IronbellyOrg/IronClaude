# Observer Guide: the `superclaude observe` Dashboard

`superclaude observe` is a read-only terminal dashboard for the person who supervises AI worker sessions running under Orca. It answers three questions at a glance: is anything waiting on me, can I trust what I am looking at, and which worker does a question belong to. It reads Orca and shows what Orca reports. It never writes to Orca: no key and no option maps to an Orca call.

For the one-line option table see [CLI groups](cli-groups.md#superclaude-observe). For the agent-facing half of supervision (the coordinator session, the sweep report and `/sc:closeout`) see the [Orchestrator mode guide](orchestrator-mode.md).

## What you need

- Orca installed, with `orca` on your `PATH`. The observer finds it there.
- A terminal at least 80 columns wide. Below 80 it prints `terminal too narrow (min 80)` and still shows the gap notice.
- For the questions screen: the terminal that already holds the Orca Run (see [Coordinator questions](#coordinator-questions)).

No Orca? Replay a synthetic fixture instead. Its first line always says `SYNTHETIC FIXTURE <name>, not Orca data`:

```bash
superclaude observe --once --fixture base --width 116
```

## Quick start

| You want | Run |
|---|---|
| The live dashboard | `superclaude observe` |
| One Run only | `superclaude observe --run <runId>` |
| The live dashboard with the coordinator's questions | `superclaude observe --questions --run <runId>` |
| One plain-text record on standard output | `superclaude observe --once` |
| One screen as text, at a fixed width | `superclaude observe --once --width 116` (160, 116 or 80) |
| ASCII only (no box-drawing or dot glyphs) | add `--ascii` (also chosen for a terminal that is not UTF-8) |
| No colour | set `NO_COLOR=1` (any non-empty value) |
| The JSON snapshot in a file you choose | add `--snapshot FILE` |

The live screen needs a terminal on standard input. Without one it prints `interactive mode needs a terminal on standard input; use --once`.

## The screens

The observer has two screens. You do not switch between them: the questions screen appears when you start with `--questions --run <runId>`, and replaces the plain ledger.

### The worker ledger (default)

One row per worker that Orca reports. Under the header you see:

- **The gap notice.** `Human questions: source UNVERIFIED, 0 rows interpreted, not "no questions"` means the observer is not reading questions. It does not mean there are none.
- **The observation window.** `worker-list OK 0s` is the age and state of the last read of Orca's worker list (`OK`, `STALE` after about 45 seconds, or `NOT AVAILABLE`). `collected 80 / reported 80` is how many rows the observer got against how many Orca says exist. If these differ the list is partial and the screen says so. A line such as `no source: settled, frozen, cost` lists the three things Orca does not report, so the observer does not guess them.
- **The ledger table.** Columns at 116 and 80 columns: the worker's next-action kind exactly as Orca gives it (`kind`), the dispatch id, whether the worker is alive, its status and the age of the evidence. The 160-column table adds the Run and the worker state.
  - A worker shows one green `ACTIVE` badge only when its dispatch status, terminal state and outcome are `active`, `active` and `none`. Any other combination, including a missing value, is shown as three separate raw values (for example `blocked/active/none`). A value Orca did not send is shown as `unknown`, never as `0` or `none`.
  - Liveness is a dot (`o` in ASCII mode). Any state other than alive is spelled out next to the dot.
  - A frozen worker carries the frozen marker in its status cell. A worker that changed since you marked a baseline carries a star.
- **The footer.** The key list and `shown 8/54`: rows on screen against rows collected. Historical rows are hidden until you press `h`; the hidden count is shown first (`26 historical hidden (h)`).

Example, 116 columns, ASCII (from `--fixture base`, synthetic data):

```text
ORCA OBSERVER  SYNTHETIC FIXTURE base, not Orca data  scope=all                                            READ ONLY
+- COORDINATOR QUESTIONS ----------------------------------------------------------------------------------------+
| Human questions: source UNVERIFIED, 0 rows interpreted, not "no questions"  26 historical hidden (h)             |
+------------------------------------------------------------------------------------------------------------------+
+- OBSERVATION WINDOW -------------------------------------------------------------------------------------------+
| worker-list OK 0s  messages UNVERIFIED (not read)                                                                |
| collected 80 / reported 80  no source: settled, frozen, cost                                                     |
+------------------------------------------------------------------------------------------------------------------+
```

### Coordinator questions

`--questions` lists the messages of type `question` that workers sent to the coordinator in **one named Run**. Start the observer from the terminal that already holds that Run: it never runs `run-use` and never binds to a Run.

```bash
superclaude observe --questions --run run_0123456789ab
```

The screen is one stack of panes (at 160 and 116 columns; the same content without the extra panes at 80):

1. **A count strip.** `SEEN IS NOT RESOLVED` with the number of questions the observer has seen and the words `closed by evidence: unavailable`. Seen is not the same as resolved: Orca has no read marker, so an answered question stays listed. At 80 columns the strip is one line, `seen !done: N | proof-done: unavailable`.
2. **The question list.** Oldest first. Each row is the age (amber), then the question text. The title says `reasons: none in source`; a row shows a reason only when the source gave one. Rows lead; the caveats sit under them. A question that left the source window is marked `[no longer in source window]`.
3. **A `RETAIN CONTEXT` pane.** The Run the list covers, the note that answered questions stay listed, and the retention note (`retention reset at HH:MM; questions observed before this start are not retained`). When the terminal is short, this pane and then the count strip are dropped and their lines move back into the list pane, so no caveat disappears.

The list is bounded best effort: coverage is unknown, at most 100 rows are read at a time, and a burst of more than 100 rows between reads may be lost. The observer says so on screen. The questions are in this process's memory only; they are reset when the observer restarts.

### The Decision Desk

Press `n` (next) or `p` (previous) on the questions screen to select a question. The Decision Desk opens for it:

- **The question pane** (amber): the question's age and its full text, up to four lines, cut with `...` if longer. Any 32-character or longer hexadecimal run (such as a plan hash) is removed from the text on screen. Nobody reads or compares a 64-character hash, and the full text is not kept. The question text appears **only on screen**: it is never written to the plain-text record or the JSON snapshot.
- **The linked session pane** (`LINKED SESSION`): the one worker the question belongs to, if the observer can verify the link: session id, state, whether it is alive (with the age of that evidence), its next action, its status badge and its worktree. The worktree line says `(this session only)`: other sessions in the same worktree are not assumed to be affected. If the question cannot be linked to a worker, the pane says why instead of guessing.
- **The question list** stays beside or under it with the selected row marked `▸` (`>` in ASCII).

At 160 and 116 columns the desk is two columns (question and list on the left, linked session on the right at 160; question across the top over linked session and list at 116). At 80 columns the three panes are stacked. Press `Esc` to clear the selection.

If the height is too small for the desk, the desk is replaced by a one-line notice instead of a cut-off pane.

## Keys

| Key | What it does |
|---|---|
| `j` / `k` (or Down / Up) | Move the selection through the worker rows. The selection follows the worker, not the line number, when rows reorder. |
| `Enter` | Open the inspector for the selected worker: every id in full, wrapped, and `unknown (absent in source)` for any field Orca did not send. |
| `d` / `u` (in the inspector) | Scroll down and up. A line says `n more fields below (d)`. |
| `Esc` | Close the inspector (or clear the selected question). |
| `/` | Filter rows by text. `Enter` applies, counts show filtered against global totals (`k of n`). |
| `h` | Show or hide historical rows. |
| `m` | Mark now. Workers that change afterwards are starred and `changed since HH:MM (n)` appears. |
| `n` / `p` | Select the next or previous question (questions screen only). |
| `e` | Export: write the plain-text record and the JSON snapshot (see [Files](#files-it-writes)). |
| `q` or Ctrl-C | Quit. The terminal is restored; Ctrl-Z then `fg` also repaints correctly. |

There is no refresh key. The observer reads Orca once every 15 seconds, with at most 5 Orca calls per read, and repaints at least twice a second so ages move.

The shown key list is shortened to the most used keys; the others still work.

## Widths, colour and ASCII

- **Widths.** The layout depends on the terminal width: 160 columns and wider gets the full table, 116 to 159 the line form, 80 to 115 the short form, and anything below 80 the `terminal too narrow` notice. `--width 160|116|80` pins one of the three, mostly for `--once`.
- **Colour.** The observer detects colour depth from `NO_COLOR`, `TERM` and `COLORTERM`: no colour, 16 colours, 256 colours, or truecolor (`COLORTERM=truecolor` or `24bit`). In 16 colours the eight roles (amber for what needs you, cyan for counts, slate for frames, and so on) keep eight different colours.
- **`NO_COLOR`.** With `NO_COLOR` set to any non-empty value the output holds no escape codes, and the text is the same as in colour. Bold and dim are not used either, so nothing depends on colour or weight.
- **`--ascii`.** The frames become `+ - |`, the liveness dot becomes `o` and the big figure uses `#`. The output is pure ASCII.
- **Piped output.** `--once --width N` prints plain text with no escape codes when output is not a terminal.
- There is no blinking, no mouse support and no animation.

## Files it writes

| Trigger | File | Mode |
|---|---|---|
| `e` in the live screen | `observe-<timestamp>.txt` (plain-text record) and `snapshot.json`, under `${XDG_STATE_HOME:-~/.local/state}/superclaude/observe/` | 600 |
| `--snapshot FILE` | The JSON snapshot at `FILE`; in live mode it is rewritten as the data changes | 600 |
| `--once` | The plain-text record on standard output; nothing is written unless you add `--snapshot` | n/a |

The record and the snapshot hold ids, times and counts. They never hold question text, message bodies, prompts, tokens or secrets.

## What the screen will not tell you

The observer is built so that missing data is shown as missing:

- `unknown` is not `0`, `false` or `none`. A field Orca omits is printed `unknown`.
- A partial list is not a complete list. `collected n / reported T` is always on screen.
- Stale is not failed. After about 45 seconds the freshness cell says `STALE` and the values are kept as last read, with the time.
- A dirty or shared worktree is not conflict evidence. The observer never infers failure, conflict or approval from missing evidence.
- Elapsed time is not progress, and a missing cost is not zero cost. Settled, policy-frozen and cost figures are shown as unavailable because Orca does not report them.

## Troubleshooting

| You see | Meaning and fix |
|---|---|
| `worker-list NOT AVAILABLE (no Orca CLI validated)` and `collected unknown / reported unknown` | `orca` is not on `PATH`, or it did not validate. Install Orca or fix `PATH`. |
| `worker-list STALE` | The last read is older than about 45 seconds. Orca may be busy or stopped. The values shown are the last good ones. It recovers by itself. |
| `--questions needs --run <runId>: it reads the questions of one named Run only` | Add `--run`. |
| `--questions needs a live source; it cannot be combined with --fixture` | Remove `--fixture`. |
| `terminal too narrow (min 80)` | Widen the terminal to at least 80 columns. |
| A question you answered is still listed | Expected. There is no read marker, so answered questions stay listed until the observer restarts. |
| Two observers make Orca slow | The poll caps are per observer process. Run one. |

## Not built

- **Remote fleet** (`--include-remote`, rows grouped by host): not built. It is tracked as a backlog item in issue [#604](https://github.com/IronbellyOrg/IronClaude/issues/604). Every count the observer shows covers the local host only.
- **Per-session plain-English summaries, issue and pull-request links, named steps, and opening a session from the view:** not built. The observer shows the facts Orca reports and navigation only.
- **Any action.** The observer never approves, retries, terminates, dispatches, merges or messages. It also never sends anything through the issue watcher or a workspace listener.
