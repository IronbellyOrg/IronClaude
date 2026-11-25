# Position CLAY, topic OAG2: sweep file and observer screen (OA-9, OA-17)

Paths below are relative to the master snapshot /home/coder/.cache/ic-snap-20261120/master (origin/master 61ac2c2e6) unless stated. "Clay's line" here is the alternative named in TOPICS.md plus what Clay's merged work (PR 684 work report, design PR 681) contains. Clay posted no text on OA-9 or OA-17 (UNVERIFIED that they hold these views); the case below is the strongest honest one for the alternative.

## Claim

1. OA-9: no sweep file is kept. Each reader (report, observer) gets its own collection with its own window, so a reader is never served a file produced for someone else.
2. OA-17a: the observer shows titles and links only. The work report keeps the text.
3. OA-17b: end the questions exception now. Design one shared questions block with one shared question id, which also ends the two question channels of D11, before the observer ships.

## Mechanism

- Report: `run.py` collects what it needs itself (`collect.py`, `clickup.py`, `sessions.py`) and passes its own window; no file contract between skills. Observer: reads Orca on its own cycle, as it does today. Neither is a client of the other.
- Observer rows for held issues are title plus `orca://` or `https://` link taken from entry files; text lives in the report page, which is the plain-English layer. Question source: one block, one id, read by observer and report alike.

## Cited facts

1. The sweep's classes depend on the producer's window: `sweep/classify.py:303-324` and `:922` (`stale = last < ctx.window_start`). A shared file stamped with a coordinator's short window gives the report a different answer than the report's own `--window` (D11: "the report passes `--window` equal to the time since the previous report"). One file is not one truth when readers need different windows.
2. The shared file would sit under one checkout root (`sweep/commands.py:99` `_check_output`: output must be inside `<root>/.dev/sweeps/`), while the watcher is designed to serve many repos (`orca repo list` dispatcher, D07). A reader of one root cannot see the others' sessions.
3. The sweep contract is read-only and its Will Not list says "Edit, stage or delete a file" (`src/superclaude/skills/sc-sweep-protocol/SKILL.md:61-62`). It already writes one report file; a second persistent artifact holding row evidence strings from Orca and transcripts (JSON `rows[].evidence`, `sweep/report.py:642-650`) enlarges what sits on disk in `.dev/sweeps/`, which is untracked (git status: `?? .dev/sweeps/`). No retention rule was found in the sweep code (UNVERIFIED that none exists elsewhere).
4. The observer's contract says navigation only: no Options, no Recommendation, no write (issue 409 item 2, as cited in D11 "Our strengths"). Entry files hold model-written `recommend`, `suggested`, `needs` and `how` slots (`skills/agent-work-report/scripts/common.py:139-141`). Showing "entry text" with no field list can put a Recommendation on the screen. Titles and links cannot.
5. `observe/sanitize.py` removes terminal controls only. My test (read-only, `uv run python -I`) shows Rich markup such as `[bold red]x[/]` and plain-text instructions pass unchanged and there is no length cap (5,000 characters stay 5,000). Its docstring leaves markup safety to the renderers (`sanitize.py:1-7`). "Always through sanitize.py" is necessary but not enough for free text from a model.
6. The package already has several text sanitizers: the observer's, the sweep report's (strips controls, escapes `\ | < > [ ]`, cuts cells at 200; `sweep/report.py:569-599`) and the report skill's (techref `OBSERVER-SWEEP-DASHBOARD-TECHNICAL-REFERENCE.md:258`). Showing entry text adds a fourth path for the same kind of untrusted text.
7. Two question channels exist: the observer reads `orchestration check --all --types question` (`observe/adapter.py:32`) while the work report's "Needs you" is its own channel (D11 "Dashboard" implication). The observer ledger cannot tell handled from open: "a question the coordinator already handled is listed again as open for as long as Orca still returns it" (`observe/questions.py:9-12`). A shared id is the only fix; shipping the panel first fixes the weakness into a released screen.
8. D11 itself says "one data source" is false until the owner accepts the exception or the sweep gains a questions block (`debates/D11/VERDICT.md`, Winning recommendation). Calling a false statement "an exception" does not make it true.

## What it costs

- Two collections: more Orca reads. The sweep (up to 90 s, `probes.py:130`) cannot run inside the observer's 15 s cycle (`collector.py:28-29`), so in practice the observer keeps its own worker-list read and the sweep's eight classes. The class word on the screen could differ from the report's.
- WC-16 would need an edit if readers other than the coordinator sweep.
- Design work for a shared question id before the observer ships.

## What it risks

- Readers disagree within a minute (the cost named in TOPICS.md). The owner's chain (watcher, orchestrator, dashboard) and issue 409's "same facts in the same way" goal are weakened.
- Titles-only makes the screen a list of links; the person opens the report for every item.

## What it gets right

- A reader gets facts built for its own window (fact 1).
- No new persistent file of Orca-derived strings and no per-root location problem.
- Free text from a model reaches the terminal only if a field list and a cap say so (facts 4 and 5).
- A shared question id is the real fix for the two-channel problem (fact 7).
