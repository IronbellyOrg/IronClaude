# Round 1 statement, advocate for Variant 2 (CLAY), topic OAG2

Paths are relative to the read-only snapshot /home/coder/.cache/ic-snap-20261120/master unless stated. I re-read the cited lines for this statement; where one is wrong or unconfirmed I say so.

## Position summary

Clay's strongest points are not "no file" or "titles only" as slogans. They are three separable requirements: a shared sweep file must carry the window and root it was made for, entry text on the observer needs a field list and a length cap and not only `sanitize.py`, and the questions panel needs a plan for one shared question id. They are right on the facts behind all three; they are weaker on the remedies. A hybrid built on the owner's line (file kept, plus those guards) is better than either paper as written.

## Steelman of Variant 1 (the owner's line)

**OA-9 (one JSON file beside the Markdown).** Strongest version: the observer cannot run its own sweep. `Budget(total_s=90.0)` is at `src/superclaude/cli/sweep/probes.py:130` (confirmed) and the observer cycle is `INTERVAL = 15.0`, `CYCLE_BUDGET = 15.0` at `src/superclaude/cli/observe/collector.py:28-29` (confirmed). So "each reader collects for itself" is not available to the observer. The sweep already writes its Markdown atomically, and today the JSON is only echoed to standard output (`sweep/commands.py:278`, confirmed: `click.echo(payload)`), so the JSON file is a second write on a path that exists. One writer, one source of classes, stateless and zero-token, WC-16 untouched (`src/superclaude/core/WORKER-CONTRACT.md` WC-16: at most once every 5 minutes; "the `/sc:sweep` report is a dated local file; it is never posted"). What it genuinely gets right: a file is the only cheap way to give the screen sweep classes at all.

**OA-17a (show entry text, through sanitize).** Strongest version: the person asked on issue 409 for plain-English state, what, done, todo, needs, how on one screen. A titles-only screen turns the observer into a list of links and sends the person to a second report for every item, which defeats "the one screen". Terminal safety is real: the sanitizer strips ESC, CSI, OSC, control and bidi characters and carriage returns, and its docstring says renderers build `rich.text.Text` from data and never parse worker text as markup (`observe/sanitize.py:1-7`, confirmed). It also gets right that V1 lists the Recommendation risk itself, so it is not blind to it.

**OA-17b (keep the questions panel, label the exception).** Strongest version: the panel is built, tested and gated. `QUESTION_TEMPLATE = ("orchestration", "check", "--all", "--types", "question")` is at `observe/adapter.py:32` (confirmed), followed by a forbidden-prefix set. The sweep JSON v1 has no questions block. Ending the exception "now" means designing a block that does not exist, before shipping a screen that is otherwise ready. D11 already ruled "write the exception down honestly". Shipping the labelled read is the smaller, reversible step.

## Strengths claimed (for Variant 2)

1. **A reader gets facts built for its own window.** Classes depend on the producer's `window_start`. Confirmed: `sweep/classify.py:303-324` returns idle when `last < ctx.window_start` (evidence text "is before window_start") and person_active when `last >= ctx.window_start`; `classify.py:922` has `stale = last < ctx.window_start`. The same transcript is idle under a 5-minute coordinator window and person_active under a one-day report window. V1 concedes the risk (V1 "What it risks", bullet 2), but its mechanism says "the observer then reads the newest file" after the report has also saved a file with its own window. The newest file may then be the report's, and the screen shows classes for the wrong window. That is a gap in V1's own mitigation, not only a risk.
2. **One file under one root, while the watcher is meant for many repos.** `_check_output` in `sweep/commands.py` (about line 99) confines output to `<root>/.dev/sweeps/` (confirmed). A reader of one checkout cannot see another repo's sessions. V1 notes "a reader must be told which root" and gives no rule.
3. **Entry text needs a field list and a cap; `sanitize.py` alone is not enough.** The entry-file slots include `recommend`, `suggested`, `needs`, `how` (`skills/agent-work-report/scripts/common.py:137-141`, confirmed: "state, next, what, state_text, done, todo, happened, recommend, needs, how, plus suggested and priority_why"). The observer is navigation only. V1's Claim 2 says "shows entry text" with no list, though its risks section says a list is needed.
4. **The sanitizer is a control-character filter, not a content filter.** Its docstring: "Markup safety is not this module's job" (confirmed, `sanitize.py:3-5`). That supports Clay's finding that Rich markup and plain instructions pass. I did not re-run Clay's 5,000-character test; I saw no length cap in the part of the module I read. UNVERIFIED by me: exact cap behavior.
5. **The ledger cannot tell handled from open.** Confirmed at `observe/questions.py:9-14`: "a question the coordinator already handled is listed again as open for as long as Orca still returns it. `seen` is not `resolved`, and neither is 'handled'." A shipped panel shows a known false-open state unless a shared id comes later. V1 does not mention it (C-010).
6. **A second persisted file has no retention rule I could find.** My grep of `sweep/*.py` for retention, prune, keep_last and max_files found no hit (UNVERIFIED that none exists elsewhere). The Markdown is already one file per run, and the JSON adds one more per run, holding `rows[].evidence`. This is a modest point, see concessions.
7. **Two freshness meanings on one screen.** The observer marks its own source STALE after 45 s (`observe/view.py:33-34`, confirmed `STALE_SECONDS = 45.0`) while a sweep file is at least 5 minutes old by WC-16. V1 answers with "shows `observed_at` and an age", which is adequate only if the spec says what the screen word is for a file older than 45 s.

## Weaknesses identified in Variant 1

1. Its window mitigation is incomplete: nothing requires the file to record `window_start` or root, and the "newest file" rule can pick a file made for another reader (`classify.py:303-324`, `:922`).
2. Its OA-17a claim omits the field list its own risk section calls necessary, so a builder could ship `recommend` on a navigation-only screen (`common.py:137-141`).
3. It treats `sanitize.py` as the text guard while the module disclaims markup safety (`sanitize.py:3-5`), and its fact 6 closes only terminal-control content.
4. It omits the open-versus-handled limit of the questions ledger (`questions.py:9-14`), so a label that says only "own Orca call" would not tell the person that listed questions may already be handled.
5. It prices the writer (one function) but not the reader: `observe/` contains no reference to "sweep" and no reader of `.dev/coordinator/orchestrated/` (my grep: no hit). The file is read by code that does not exist yet.
6. The file serves the coordinator's 5-minute cadence, so with no coordinator running there may be no fresh file. V1 covers this with "a missing or old file is its own state", which is right but is new observer logic.

## Concessions

1. **"No file" gives the observer no classes.** The observer has no sweep classes today (my grep of `observe/` found no sweep reference and no class constants). V2's cost line, "the observer keeps its own worker-list read and the sweep's eight classes", is wrong as worded: the observer does not have the eight classes and cannot compute them in 15 s. Under "no file" the screen shows its own worker-list states, which may differ from the report's. That loses "same facts in the same way".
2. **Titles-only is a heavy cut.** The person asked for plain-English text on one screen (issue 409). The Recommendation risk is better solved with a field allowlist than with removing text.
3. **Ending the questions exception before the observer ships is a design that does not exist.** The sweep JSON has no questions block (12 top-level keys at `sweep/report.py:613-640` per V1; I did not recount). It should be a follow-up with an owner, not a precondition.
4. Clay posted no text on OA-9 or OA-17 (V2's own disclaimer). This is the best case for the alternative, not Clay's stated view.
5. V2 fact 3 (a second artifact "enlarges what sits on disk") is weak. The Will Not line (`sc-sweep-protocol/SKILL.md:61-62`: "Edit, stage or delete a file, or run any command other than the two forms in steps 1 and 2") governs the skill session, not the command's own report write. V1 is right on X-001.
6. Separate collections would need either a second classifier or two class vocabularies, a cost V2 names but does not price.

## Shared assumption responses

- **A-001 (entry files exist for the observer to read): QUALIFY.** The only writer, `superclaude orchestrator report-entry`, is named in the work-report scripts (`run.py`, `check.py`, `common.py`) and the techref calls it designed and absent (I did not re-read the techref lines), and `observe/` has no reader of `.dev/coordinator/orchestrated/`. Both OA-17 positions describe a source that may be empty, so the spec needs an explicit "folder empty or writer absent" state.
- **A-002 (the observer will be changed to read the sweep file or entry files): ACCEPT.** `observe/` imports nothing from `sweep/` and reads no entry file today, so either line is new observer work. This is why the "built and tested" argument fits the questions read only, not the file read.
- **A-003 (the 90 s `Budget(total_s)` is how long a sweep takes): QUALIFY.** It is a cap, not a measurement: `probes.py:130` sets `total_s: float = 90.0`, and `adapter.py:60-62` says the per-call timeout is "UNVERIFIED until the first permitted live read measures it". The safe claim is that a per-cycle sweep cannot be guaranteed to fit 15 s, and WC-16 caps runs at once per 5 minutes regardless.
- **A-004 (the screen is read by a person, not by an agent): QUALIFY.** A person is the intended reader, so "plain-text instructions pass" is a low risk today. If an agent ever reads pane text or a screenshot, it becomes a prompt-injection path, and a field list and cap cost almost nothing.

## Per-point verdicts

| Point | Winner | Confidence | One-line evidence |
|---|---|---|---|
| C-001 (file or no file) | V1 (the file), with a Clay guard | 70% | Observer cannot sweep per 15 s cycle (`probes.py:130` vs `collector.py:28-29`); "no file" leaves the observer without classes. Guard: file records window and root. |
| C-003 (window dependence) | V2 on diagnosis; hybrid on remedy | 75% | `classify.py:303-324`, `:922`: same row is idle or person_active by window. V1's "newest file" is unsafe unless the file says which window it used. |
| C-006 (entry text on screen) | Hybrid: show text through a field allowlist, a length cap and `sanitize.py`, with no `recommend` or `suggested` | 70% | V1 right on "one screen" (issue 409); V2 right that `common.py:137-141` slots include recommendations. Titles-only is the safe fallback if no allowlist is written. |
| C-009 (questions exception) | V1 on timing (ship the labelled read); V2 on direction (plan the shared id) | 65% | Panel is built and gated (`adapter.py:32`); no shared block exists. The label must carry the handled-versus-open limit (`questions.py:9-14`). |

## Hybrid I recommend

Sweep JSON saved beside the report (owner's line). The file body records `window_start`, who passed the window, and the root. The observer shows file age and its own STALE rule. The screen shows allowlisted entry fields only (state, what, done, todo, needs; not `recommend` or `suggested`), each capped in length and rendered as `rich.Text` from data. The questions panel keeps its own read with a label that includes the handled-versus-open limit. A tracked follow-up issue covers the shared question id.

Separable Clay benefits, clearest first: (1) window and root recorded in the file, (2) entry field allowlist and cap, (3) the handled-versus-open limit on the label, (4) a follow-up for the shared question id. Not separable and I do not press: "no file at all" and "end the exception before shipping".
