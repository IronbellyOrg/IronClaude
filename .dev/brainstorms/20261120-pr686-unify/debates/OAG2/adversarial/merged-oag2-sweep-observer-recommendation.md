<!-- Provenance: produced by /sc:adversarial -->
<!-- Base: Variant 1 (OURS position paper), /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/OAG2/adversarial/adversarial/variant-1-original.md -->
<!-- Incorporated from: Variant 2 (CLAY position paper) and the orchestrator check after Round 1, per refactor-plan.md -->
<!-- Merge date: 2026-11-20 -->

# Recommendation on the sweep file and the observer screen (OAG2: OA-9, OA-17)

<!-- Source: Base (original, modified) - the position paper title and scope line are rewritten as a recommendation document, per the refactor plan Overview -->
Paths below are relative to the master snapshot /home/coder/.cache/ic-snap-20261120/master (origin/master 61ac2c2e6) unless stated. OA-9 and OA-17 are owner-action ids from the unification plan. This document answers OA-9, OA-17a and OA-17b separately. Each part gives a decision, the conditions the spec must state as numbered testable rules, and the evidence.

## Recommendation in one paragraph

<!-- Source: Base (original, modified) - rewritten from the base Claim as a decision with conditions; reader selection rule from Variant 2, Section Cited facts 1 - merged per Change #1; entry allowlist and gate on the entry writer from Variant 2, Section Cited facts 4 and 5 - merged per Changes #4 and #7; label and follow-up from Variant 2, Section Cited facts 7 and 8 - merged per Change #5 -->
Keep the owner's line and add conditions to it. The sweep saves its JSON as `<UTC>-sweep.json` beside its Markdown report in `.dev/sweeps/`, and every reader uses that one file, chosen by a stated rule: the newest file whose `scope.root` equals the reader's own root, with its `window`, `observed_at` and age shown on screen (OA-9). The JSON pairs with its Markdown by the same stem and the same suffix. The observer shows entry text only from a named field allowlist, never `recommend` or `suggested`, with a length cap on block fields, and only once the entry writer exists; until then it shows titles and links only (OA-17a). The questions panel keeps its own Orca read, labelled with its handled-versus-open limit, and a tracked follow-up for one shared question id is filed but does not block the observer release (OA-17b). Clay's alternative (no file, titles and links only for good, end the questions exception before release) is not adopted, but three of its defects are real and are fixed here: the file can be read by the wrong reader, entry text needs a field list and a cap, and the questions panel needs a plan for a shared id. Clay's own views on OA-9 and OA-17 are not on record (UNVERIFIED); the alternative was argued from TOPICS.md (the debate topics list) and from Clay's merged work.

## OA-9 where the sweep JSON lives

### Decision

<!-- Source: Base (original, modified) - base Claim 1 and Mechanism; the "same stem" wording is replaced per Change #3 and "who passes which --window" is replaced by the selection rule per Change #1 -->
The sweep saves its JSON as `<UTC>-sweep.json` beside its Markdown report in `.dev/sweeps/`. One file is read by every reader (the work report, the observer and the coordinator). The sweep stays the single, stateless, read-only source of session facts. WC-16 (the worker-contract rule at `src/superclaude/core/WORKER-CONTRACT.md:287-289` that caps the coordinator's sweep to one per 5 minutes) stands. The sweep already builds the JSON v1 object (the sweep's JSON report format, version 1) and already publishes its Markdown atomically (temp file, then `os.link` to the first free name, never overwrite). The change is to publish a second file from the same `to_json` call. The observer polls that file every 15 seconds at no Orca cost and shows `observed_at`. Which file a reader takes is set by a selection rule, not by "newest file" alone (rule 4 and rule 5 below).

<!-- Source: Orchestrator verification after Round 1 - Change #2 -->
JSON v1 already holds `observed_at`, `scope.root` and `window`. No new field is needed for this decision; the missing part is the selection rule.

### What the spec must say

<!-- Source: Base (original, modified) - base Mechanism and What it costs, rewritten as numbered testable rules -->
1. Write. The sweep publishes `<UTC>-sweep.json` from the same `to_json` call, with the same atomic pattern as the Markdown (temp file, then `os.link` to the first free name, never overwrite). Test: after one run both files exist, and a second run in the same second does not overwrite the first.
2. Pair. A JSON file and a Markdown file are a pair only when they share the same stem and the same suffix: `<UTC>-sweep.json` pairs with `<UTC>-sweep.md`, and `<UTC>-sweep-2.json` pairs with `<UTC>-sweep-2.md`. The `.md` link stays the commit point. The contract note (rule 8) decides what happens when the JSON cannot be written. A test pins that a pair always shares its suffix (the publish path allows suffixes up to `MAX_SUFFIX = 99`, `src/superclaude/cli/sweep/commands.py:182`). <!-- Source: Orchestrator verification after Round 1 - Change #3 -->
3. Fields. The file carries `observed_at`, `scope.root` and `window` (written as `24h`, `5m` or `90s`) from JSON v1 (`src/superclaude/cli/sweep/report.py:621-631`, `_window_text` at `report.py:95-101`). The new fields of D11 (the observability debate verdict, `debates/D11/VERDICT.md`), `session_id` and `worktree_path`, are a separate item. <!-- Source: Orchestrator verification after Round 1 - Change #2 -->
4. Observer selection. The observer reads the newest `*-sweep.json` whose `scope.root` equals its own root, and shows `window`, `observed_at` and the age on screen. <!-- Source: Variant 2, Section Cited facts 1 and Variant 2 advocate "newest file may be the report's" point - merged per Change #1 -->
5. Work report selection. The work report does not read a file whose `window` is shorter than the time since its previous report. It runs `superclaude sweep run --window <that time>` itself, which also saves a file. <!-- Source: Variant 2, Section Cited facts 1 - merged per Change #1 -->
6. Coordinator. The coordinator keeps WC-16: at most one sweep per 5 minutes. <!-- Source: Variant 2, Section Cited facts 1 - merged per Change #1 -->
7. Missing or old file. A missing or old file is its own state on screen, never "no sessions". Test: with no file the screen does not present zero sessions as fact. What age counts as old is not set here (see "Open items and UNVERIFIED"). <!-- Source: Base (original), What it risks, Staleness -->
8. Contract note. `docs/designs/observe-sweep-contract.md` (unwritten since 2026-11-13) names the file, its name pattern and one owner. This is work item S5 in the merged requirements. <!-- Source: Base (original), What it costs -->

### Evidence

<!-- Source: Base (original), Cited facts 1, 3, 4 and 5 and What it risks; fact 2 is modified per Change #6; classification-window fact from Variant 2, Section Cited facts 1 - merged per Change #1 -->
1. Today the JSON goes to standard output only: `src/superclaude/cli/sweep/commands.py:278` (`click.echo(payload)`). The Markdown is already written to disk by `_publish` (`commands.py:153-193`, atomic, never overwrites). A second file extends a path that already exists and is already tested.
2. <!-- Source: Base (original, modified) - "cannot fit" replaced by "is not guaranteed to fit" per Change #6 --> One sweep may run for up to 90 seconds: `Budget(total_s=90.0)` at `src/superclaude/cli/sweep/probes.py:130`. That figure is a cap, not a measured time. The observer's cycle may not run longer than 15 seconds: `INTERVAL = 15.0`, `CYCLE_BUDGET = 15.0` at `src/superclaude/cli/observe/collector.py:28-29`. A sweep per observer cycle is not guaranteed to fit its own budget. The case for a shared file therefore rests on cost (a second Orca-and-transcript collection per cycle) and on WC-16, not on the 90 second figure.
3. WC-16 (`src/superclaude/core/WORKER-CONTRACT.md:287-289`): at most once every 5 minutes the coordinator runs `/sc:sweep` and reads its report; "the `/sc:sweep` report is a dated local file; it is never posted". A shared file keeps one collection per window and lets any number of readers look at it.
4. The observer and the sweep share no code today: a grep of `src/superclaude/cli/observe/*.py` for "sweep" finds nothing. The observer already polls `orchestration worker-list` itself (`observe/adapter.py:29`). The question is whether a second, heavier Orca-and-transcripts collection (the sweep) is added per cycle. A saved file avoids that.
5. The sweep "Will Not: Recommend anything" (`src/superclaude/skills/sc-sweep-protocol/SKILL.md:61`) and has eight proof-based classes plus "could not determine". It is the right bottom layer; the report and the observer then do not decide session status themselves (`debates/D11/VERDICT.md`, "One data source").
6. Classification depends on the window the producer chose (`src/superclaude/cli/sweep/classify.py:303-324` and `:922`, `stale = last < ctx.window_start`). A file produced by a coordinator sweep with a short window is not what a daily report needs. This is why rule 4 and rule 5 exist, and why the window is shown on screen.
7. The file is as old as the last sweep (5 minutes or more). Rule 7 and the age on screen keep this honest.
8. The file lives under one checkout root (`<root>/.dev/sweeps/`), so a reader must be told which root. Rule 4 does this with `scope.root`. How a reader serves more than one repo is an open item.

## OA-17a what the observer may show

### Decision

<!-- Source: Base (original, modified) - base Claim 2 "shows entry text ... always through sanitize.py" is replaced by an allowlist, cap and fallback per Change #4; the condition on the entry writer is added per Change #7 -->
The observer shows entry fields from a named allowlist, once the entry writer exists. `recommend` and `suggested` are never shown. `how` is not shown until the owner has reviewed what it holds (UNVERIFIED). Every shown field is `rich.Text` built from data after `sanitize()`, and block fields have a length cap. While the entry writer (`superclaude orchestrator report-entry`) is absent, the observer shows titles and links only. The three states (empty folder, zero rows, could not read) stay distinct. OA-17a text on screen is conditional on the entry writer landing.

### What the spec must say

<!-- Source: Variant 2, Section Claim 2 and Cited facts 3, 4 and 5 - merged per Change #4; rule 6 also per Change #7; rule 7 is Base (original) -->
1. Allowlist. The spec names the entry fields the observer shows. A field that is not on the list is not shown. The full contents of the list are for the owner or the spec (see "Open items and UNVERIFIED").
2. Never shown. `recommend` and `suggested` are never shown. Test: a fixture with `recommend` and `suggested` filled shows neither.
3. Held back. `how` is not shown until the owner has reviewed what it holds (UNVERIFIED).
4. Safe rendering. Every shown field goes through `sanitize()` and is built as `rich.Text` from data, never parsed as markup. Test: bracket markup such as `[bold red]x[/]` shows literally.
5. Cap. Block fields have a length cap; the spec sets the value. Test: a 5,000-character field shows at most the cap.
6. Fallback. While the entry writer is absent the observer shows titles and links only.
7. Three states. An empty folder, zero rows and "could not read" stay three distinct states on screen.

### Evidence

<!-- Source: Base (original), Cited facts 6 and 7; facts 3 to 6 below are Variant 2, Section Cited facts 4 and 5 - merged per Change #4; fact 7 is Variant 2 fact on the entry writer - merged per Change #7 -->
1. Entry files carry the plain-English fields the person asked for on issue 409 (the observer TUI dashboard design issue): state, what, done, todo, needs, how (`src/superclaude/skills/agent-work-report/scripts/common.py:139-141`). Showing them is what makes the observer "the one screen" (D11, "One dashboard"). A titles-only screen sends the person back to a second report.
2. The sanitizer works on hostile terminal input. Run read-only (`uv run python -I`) on samples, `observe/sanitize.py` removes or turns into one space a CSI colour code, an OSC 8 hyperlink, a bidi override (U+202E), a zero-width space, a C1 byte and CR or CRLF. This closes the D11 item "unverified: handles arbitrary entry-file text" for terminal-control content only. Its docstring says renderers build `rich.text.Text` from data and never parse worker text as markup (`observe/sanitize.py:1-7`).
3. The same entry lines (`common.py:139-141`) also hold model-written `recommend` and `suggested` slots. The observer's contract is navigation only: no Options, no Recommendation, no write (issue 409 item 2, as cited in D11, "Our strengths"). Showing every field would put a Recommendation on that screen.
4. The sanitizer removes terminal controls only. Rich markup such as `[bold red]x[/]` and plain-text instructions pass unchanged, and `sanitize()` has no length cap (5,000 characters stay 5,000; tested read-only by the orchestrator when the position papers were written; the Variant 2 advocate did not re-run it). "Always through sanitize.py" is necessary but not enough for free text from a model.
5. The renderer clips lines by display width (`src/superclaude/cli/observe/render.py:158-160,325`), but its wrap helper never truncates (`render.py:85`). A single-line field is therefore bounded by width; a block field is not. The cap is needed for block fields.
6. Risk to the person is low with a human reader, and an allowlist plus cap cost little if a model ever reads the screen (shared assumption A-004 of the debate, accepted by both advocates).
7. The entry writer (`superclaude orchestrator report-entry`) is absent today (the observer technical reference, lines 805 and 820, as cited in the debate). Both advocates qualified the premise that entry text is available to show, so OA-17a text on screen waits for the writer and the empty-folder state is kept.

## OA-17b the questions panel

### Decision

<!-- Source: Base (original, modified) - base Claim 3 and the cost line "A one-line label": the label text is replaced and the "one data source" sentence is qualified, per Change #5 -->
The observer questions panel keeps its own Orca call. It is labelled "questions read from Orca directly; a question already handled can appear as open" (`src/superclaude/cli/observe/questions.py:9-12`). The screen and the spec say "one source for session facts (the sweep); the questions panel is the one exception", not "one data source". A tracked follow-up is filed for one shared question id, which would also end the two question channels of D11. The owner names the owner of that follow-up. The follow-up is not a precondition of the observer release.

### What the spec must say

<!-- Source: Base (original), Mechanism and Cited facts 8; rules 2 to 4 are Variant 2, Section Claim 3 and Cited facts 7 and 8 - merged per Change #5 -->
1. Fixed read. The panel keeps its fixed argv template `orchestration check --all --types question --run <id> --json`, the shape check `_is_question_shape`, the forbidden set (`--ack`, `--wait`, `--peek`, `send`, `reply` and more) and the two gate constants. Nothing else about the panel changes.
2. Label. The label on screen reads "questions read from Orca directly; a question already handled can appear as open". Test: the label is present whenever the panel is shown.
3. Wording. The spec and the screen use the qualified sentence "one source for session facts (the sweep); the questions panel is the one exception". The unqualified "one data source" is not used.
4. Follow-up. A tracked follow-up exists for one shared question id, with a named owner (set by the owner), and the observer release does not wait on it.

### Evidence

<!-- Source: Base (original), Cited facts 8 and 9; facts 3 to 5 below are Variant 2, Section Cited facts 7 and 8 - merged per Change #5 -->
1. The questions panel is a fixed read: one argv template `orchestration check --all --types question --run <id> --json` (`src/superclaude/cli/observe/adapter.py:32`, shape checked by `_is_question_shape`, `adapter.py:111`); the forbidden set blocks `--ack`, `--wait`, `--peek`, `send`, `reply` and more (`adapter.py:34-50`); two gate constants are `True` with cited owner records (`src/superclaude/cli/observe/commands.py:67,70`). It is built, tested and gated. That the read is non-consuming is the technical reference's reading (R4), not tested live (UNVERIFIED).
2. The sweep JSON v1 has no questions block (12 top-level keys, `src/superclaude/cli/sweep/report.py:613-640`), so ending the exception now needs a design that does not exist yet.
3. D11 ruled that the exception be written down honestly, not hidden (`debates/D11/VERDICT.md`, "One honest exception"). D11 also says "one data source" is false until the owner accepts the exception or the sweep gains a questions block (`debates/D11/VERDICT.md`, "Winning recommendation"). The qualified sentence in rule 3 is true.
4. The observer ledger cannot tell handled from open: "a question the coordinator already handled is listed again as open for as long as Orca still returns it" (`observe/questions.py:9-12`). The label in rule 2 states that limit.
5. Two question channels exist: the observer reads `orchestration check --all --types question` (`observe/adapter.py:32`) while the work report's "Needs you" is its own channel (D11, "Dashboard" implication). A shared question id is the fix. Both advocates agreed the follow-up is right and that it should not sit on the observer's release path.

## What is adopted from CLAY

<!-- Source: Variant 2, Section Claim and Cited facts 1, 3, 4, 5, 7 and 8 - merged per Changes #1, #4, #5, #6 and #7 -->
| Item | Why | Change number |
|---|---|---|
| Reader selection rule: newest `*-sweep.json` with a matching `scope.root`; `window`, `observed_at` and age on screen; the work report runs its own `--window` when the file's window is too short | The newest file may have been made for another reader's window (Variant 2 fact 1; the Variant 2 advocate's point that the newest file may be the report's). The fields already exist, so the missing part is the rule | 1 |
| Entry field allowlist; `recommend` and `suggested` never shown; `how` held back until reviewed; `rich.Text` from data; length cap on block fields; titles and links only while the entry writer is absent | The sanitizer removes terminal controls only and has no cap; entry files hold model-written `recommend` and `suggested` slots (Variant 2 facts 3, 4 and 5; the Variant 1 advocate conceded the allowlist and the cap) | 4 |
| Label that states the handled-versus-open limit; qualified "one source for session facts" sentence; tracked follow-up for one shared question id, not a precondition of release | A handled question can show as open (`questions.py:9-12`), and the unqualified sentence "one data source" is false (Variant 2 facts 7 and 8; D11) | 5 |
| The 90 second argument is qualified to "is not guaranteed to fit" | Both advocates qualified it: `Budget(total_s=90.0)` is a cap, not a measured time; cost and WC-16 carry the case | 6 |
| OA-17a text on screen is conditional on the entry writer; Clay's own views are recorded as not on record (UNVERIFIED) | The entry writer is absent today; Clay posted no text on OA-9 or OA-17, so the alternative was argued from TOPICS.md and Clay's merged work | 7 |

<!-- Source: Orchestrator verification after Round 1 - Changes #2 and #3 -->
Two further changes were applied that are not from Clay. Change 2 (orchestrator check after Round 1): JSON v1 already holds `observed_at`, `scope.root` and `window`, so no field has to be added; only the selection rule is missing. Change 3 (raised by the Variant 1 advocate in Round 1, tagged here as orchestrator-origin per the merge brief): a JSON file pairs with the Markdown file of the same stem and the same suffix.

## What stays from OURS

<!-- Source: Base (original), What it gets right and Cited facts 3 to 9; rejected changes C-001, C-005, C-006 and C-009 of the refactor plan are not applied -->
- The shared file. "No sweep file, each reader collects for itself" is not adopted. The observer would get no sweep classes at all, and both advocates conceded this. The file is the only cheap route to "the same facts in the same way" (`probes.py:130` against `collector.py:28-29`).
- The owner's rules: a stateless, zero-token, read-only sweep that recommends nothing, WC-16 as it is, and an observer without writes.
- Use of what is built: JSON v1, the atomic publish, the sanitizer and the gated questions read, instead of a design not yet drawn.
- A second persisted file does not breach the read-only contract. The Will Not line in `src/superclaude/skills/sc-sweep-protocol/SKILL.md:61-62` governs the skill session, not the command's own report write, and the Markdown report is already written the same way. A retention gap for `.dev/sweeps/`, if real, covers the folder and not the JSON alone (UNVERIFIED that none exists).
- The plain-English screen. "Titles and links only, for good" is not adopted: it loses the screen the person asked for on issue 409 and sends them to a second report for every item. The allowlist gives the safety at a lower cost, and titles and links remain only as the fallback while the entry writer is absent.
- The questions panel ships with its label. Ending the exception before release is not adopted: the shared question id has no design yet, and a design that does not exist would sit on the observer's release path (the sweep JSON has no questions block, `report.py:613-640`).
- What it costs: one new write in the sweep (about one function, same atomic pattern) and a test; the contract note in OA-9 rule 8; and a one-line label on the observer screen for the questions exception (OA-17b rule 2).

## Open items and UNVERIFIED

<!-- Source: Base (original, modified) - base risks and UNVERIFIED marks kept; open items from the refactor plan and the debate Convergence Assessment; closing note on Clay's views per Change #7 -->
Open items for the owner or the spec (this document does not decide them):

1. The full contents of the entry field allowlist (OA-17a rule 1) and the length cap value (OA-17a rule 5).
2. The multi-repo rule. The file sits under one checkout root (`_check_output` in `src/superclaude/cli/sweep/commands.py:99` requires the output inside `<root>/.dev/sweeps/`), while the watcher is designed to serve many repos (D07, a decision record cited by Variant 2 for the watcher's `orca repo list` dispatcher). Rule 4 of OA-9 matches on `scope.root`; which root a reader serves when more than one repo is in play is not decided. That multi-repo reading is an inference (UNVERIFIED).
3. The owner of the shared question id follow-up (OA-17b rule 4). The owner names it.
4. What the contract note decides when the JSON cannot be written (OA-9 rule 2), and what age counts as an "old" file (OA-9 rule 7).
5. Whether the entry field `how` is safe to show, once the owner has reviewed what it holds (OA-17a rule 3).

UNVERIFIED:

- Clay's own views on OA-9 and OA-17 are not on record. The Clay alternative was argued from TOPICS.md and from Clay's merged work (PR 684, Clay's merged move of the agent-work-report skill, and PR 681, a design pull request named in the Clay position paper).
- That the questions read is non-consuming: the technical reference's reading (R4), not tested live.
- That no retention rule exists for `.dev/sweeps/` anywhere (none was found in the sweep code).
- The entry writer `superclaude orchestrator report-entry` is absent today (technical reference lines 805 and 820, as cited in the debate). OA-17a text on screen waits for it.
- The file:line citations are carried from the two position papers and the refactor plan. A pass-2 evaluator spot-checked 21 of them and found none wrong; the merge executor did not reopen the source files.
- Reading caution from the debate: the run used quick depth (Round 1 only; no rebuttals, invariant probe or Round 3), and both advocates were the same model as the orchestrator. The convergence reflects that the papers' facts held up, not independent confirmation that the hybrid is wise.

