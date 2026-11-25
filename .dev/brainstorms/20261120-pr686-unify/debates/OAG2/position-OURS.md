# Position OURS, topic OAG2: sweep file and observer screen (OA-9, OA-17)

Paths below are relative to the master snapshot /home/coder/.cache/ic-snap-20261120/master (origin/master 61ac2c2e6) unless stated.

## Claim

1. OA-9: the sweep saves its JSON as `<UTC>-sweep.json` beside its Markdown report in `.dev/sweeps/`. One file, read by every reader (work report, observer, coordinator). The sweep stays the single, stateless, read-only source of session facts and WC-16 (at most one sweep per 5 minutes on a coordinator wake) stands.
2. OA-17a: the observer shows entry text from the living report, always through `observe/sanitize.py`. The three states (empty folder, zero rows, could not read) stay distinct.
3. OA-17b: the observer questions panel keeps its own Orca call, labelled as an honest exception to "one data source", until a shared questions block exists.

## Mechanism

- The sweep already builds the JSON v1 object and already publishes its Markdown atomically (temp file, then `os.link` to the first free name, never overwrite). The change is to publish a second file with the same stem from the same `to_json` call. The observer polls that file every 15 seconds at no Orca cost and shows `observed_at`. The work report reads the same file for session facts.
- Entry text reaches the screen only through `sanitize()` and `rich.Text` built from data (never parsed as markup).
- The questions panel continues to use its fixed argv template; nothing else about it changes.

## Cited facts

1. Today the JSON goes to standard output only: `src/superclaude/cli/sweep/commands.py:278` (`click.echo(payload)`). The Markdown is already written to disk by `_publish` (`commands.py:153-193`, atomic, never overwrites). A second file extends a path that already exists and is already tested.
2. One sweep may run for up to 90 seconds: `Budget(total_s=90.0)` at `src/superclaude/cli/sweep/probes.py:130`. The observer's cycle may not run longer than 15 seconds: `INTERVAL = 15.0`, `CYCLE_BUDGET = 15.0` at `src/superclaude/cli/observe/collector.py:28-29`. A sweep per observer cycle cannot fit its own budget, so "each reader runs its own sweep" is not available to the observer without redefining one of the two budgets.
3. WC-16 (`src/superclaude/core/WORKER-CONTRACT.md:287-289`): at most once every 5 minutes the coordinator runs `/sc:sweep` and reads its report; "the `/sc:sweep` report is a dated local file; it is never posted". A shared file keeps one collection per window and lets any number of readers look at it.
4. The observer and the sweep share no code today: a grep of `src/superclaude/cli/observe/*.py` for "sweep" finds nothing. The observer already polls `orchestration worker-list` itself (`observe/adapter.py:29`). The question is whether a second, heavier Orca-and-transcripts collection (the sweep) is added per cycle. A saved file avoids that.
5. The sweep "Will Not: Recommend anything" (`src/superclaude/skills/sc-sweep-protocol/SKILL.md:61`) and has eight proof-based classes plus "could not determine". It is the right bottom layer; the report and the observer then do not decide session status themselves (`debates/D11/VERDICT.md`, "One data source").
6. The sanitizer works on hostile terminal input. I ran `observe/sanitize.py` on samples (read-only, `uv run python -I`): a CSI colour code, an OSC 8 hyperlink, a bidi override (U+202E), a zero-width space, a C1 byte and CR/CRLF are all removed or turned into one space. This closes the D11 "unverified: handles arbitrary entry-file text" item for terminal-control content only. Its docstring says renderers build `rich.text.Text` from data and never parse worker text as markup (`observe/sanitize.py:1-7`).
7. Entry files carry the plain-English fields the person asked for on issue 409 (state, what, done, todo, needs, how; `skills/agent-work-report/scripts/common.py:139-141`). Showing them is what makes the observer "the one screen" (D11 "One dashboard"). A titles-only screen sends the person back to a second report.
8. The questions panel is a fixed read: one argv template `orchestration check --all --types question --run <id> --json` (`observe/adapter.py:32`, shape checked by `_is_question_shape`, `adapter.py:111`); the forbidden set blocks `--ack`, `--wait`, `--peek`, `send`, `reply` and more (`adapter.py:34-50`); two gate constants are `True` with cited owner records (`observe/commands.py:67,70`). It is built, tested and gated. The sweep JSON v1 has no questions block (12 top-level keys, `sweep/report.py:613-640`), so ending the exception now needs a design that does not exist yet. That the read is non-consuming is the tech reference's reading (R4), not tested live (UNVERIFIED).
9. D11 already ruled that the exception be written down honestly, not hidden (`debates/D11/VERDICT.md`, "One honest exception"). Keeping it labelled applies that verdict.

## What it costs

- One new write in the sweep (about one function, same atomic pattern) and a test; a contract note `docs/designs/observe-sweep-contract.md` (unwritten since 2026-11-13) that names the file, its name pattern and one owner. Work item S5 in the merged requirements.
- A one-line label on the observer screen for the questions exception.

## What it risks

- Staleness: the file is as old as the last sweep (5 minutes or more). Mitigation: the screen shows `observed_at` and an age; a missing or old file is its own state, never "no sessions".
- The window problem: classification depends on the window the producer chose (`sweep/classify.py:303-324` and `:922`, `stale = last < ctx.window_start`). A file produced by a coordinator sweep with a short window is not what a daily report needs. The spec must say who passes which `--window`.
- The file lives under one checkout root (`<root>/.dev/sweeps/`), so a reader must be told which root.
- Entry text is model-written and includes `recommend` and `suggested` slots (`common.py:139-141`); showing every field would put a Recommendation on a screen that is "navigation only". The spec must list which entry fields the observer shows.

## What it gets right

- It keeps the owner's rules: stateless zero-token sweep, WC-16, "recommend nothing", observer without writes.
- It uses what is built (JSON v1, atomic publish, sanitizer, gated questions read) instead of a design not yet drawn.
- It answers the sources' own caveat: "one data source" is honest because the exception is named.
- Where a reader needs a different window (the work report), the shared-file rule lets it run `superclaude sweep run --window <time since its last report>`, which also saves a file; the observer then reads the newest file. One writer path stays.
