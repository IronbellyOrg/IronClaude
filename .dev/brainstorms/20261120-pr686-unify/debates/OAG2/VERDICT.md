# Verdict OAG2: Sweep file and observer screen

## Question

OAG2 Sweep file and observer screen: OA-9 (where the sweep JSON is saved), OA-17 (what the observer may show). OA-9 and OA-17 are owner-action ids from the unification plan (/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/OA-TRIAGE.md). Sources named in the topic block: D11 verdict items 1 to 3 (the observability debate: one data source, one report, one dashboard), merged design K10 and K19, WC-16 (the worker-contract rule that caps the coordinator's sweep to one per 5 minutes) and the observer refresh of 15 seconds, `observe/sanitize.py`, PR 409 (the dashboard design package) and PR 684 (Clay's merged move of the work-report skill).

- OA-9 Where does the sweep JSON live? OURS: saved beside the Markdown report as `<UTC>-sweep.json`; one file all readers share; S5 adds the write; WC-16 stands (K19). CLAY or alternative: each reader (report, observer) runs its own sweep and no file is kept; readers may disagree within a minute and WC-16 must change.
- OA-17a May the observer show entry text? OURS (merged design default): show entry text from the living report, always passed through `observe/sanitize.py`; the three states (empty folder, zero rows, could not read) stay distinct. CLAY or alternative: titles and links only, no entry text on the screen (the work report keeps the text).
- OA-17b Is the observer questions panel an exception to "one data source"? OURS: keep the panel's own Orca call, labelled as an exception, until a shared questions block exists. CLAY or alternative: end the exception now; design a shared questions block (one shared question id, also ending the two question channels of D11) before the observer ships.

## Winner

HYBRID. The owner's line wins on all three sub-questions (keep the shared sweep file, show entry text, keep the labelled questions exception), and five separable Clay conditions are added to it.

Per sub-question, answered separately:
- OA-9 (where the sweep JSON lives): OURS. The file is kept; "each reader sweeps" is not adopted.
- OA-17a (may the observer show entry text): HYBRID. OURS on showing text; CLAY's field allowlist, length cap and titles-and-links fallback are added.
- OA-17b (questions panel exception): OURS on timing (keep the labelled exception); CLAY's label wording and a follow-up for one shared question id are added, and the follow-up does not block the observer release.

## Winning recommendation

The merged text is `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/OAG2/adversarial/merged-oag2-sweep-observer-recommendation.md`. The spec must say the following. Paths are relative to /home/coder/.cache/ic-snap-20261120/master (origin/master 61ac2c2e6).

**OA-9, the sweep file (OURS plus conditions).**
1. The sweep saves `<UTC>-sweep.json` beside its Markdown report in `.dev/sweeps/`, from the same `to_json` call, with the same temp-file-then-link, never-overwrite pattern (today the JSON goes to standard output only, `src/superclaude/cli/sweep/commands.py:278`; the Markdown publish is at `commands.py:153-193`). Test: after one run both files exist; a second run in the same second overwrites neither.
2. The JSON pairs with its Markdown only by the same stem and the same suffix (`<UTC>-sweep-2.json` with `<UTC>-sweep-2.md`; `MAX_SUFFIX = 99`, `commands.py:182`). The `.md` link stays the commit point. Test: a pair always shares its suffix. The contract note decides what happens when the JSON cannot be written.
3. No new field is needed to record the window and root: JSON v1 already holds `observed_at`, `scope.root` and `window` (`src/superclaude/cli/sweep/report.py:621-631`). The D11 fields `session_id` and `worktree_path` stay a separate item.
4. The observer reads the newest `*-sweep.json` whose `scope.root` equals its own root and shows `window`, `observed_at` and the age on screen. A missing or old file is its own screen state, never "no sessions". The spec sets what "old" means.
5. The work report does not read a file whose `window` is shorter than the time since its previous report; it runs `superclaude sweep run --window <that time>` itself, which also saves a file. The reason: classes depend on the window the producer chose (`src/superclaude/cli/sweep/classify.py:303-324`, `:922`).
6. The coordinator keeps WC-16 unchanged: at most one sweep per 5 minutes (`src/superclaude/core/WORKER-CONTRACT.md:287-289`).
7. The contract note `docs/designs/observe-sweep-contract.md` (unwritten since 2026-11-13) names the file, its name pattern, the selection rules above and one owner.
8. The spec does not say the 90-second sweep budget "cannot fit" the observer's 15-second cycle. It says it "is not guaranteed to fit": `Budget(total_s=90.0)` (`probes.py:130`) is a cap, not a measured time. The case for the file rests on cost (a second Orca-and-transcript collection per cycle) and on WC-16.

**OA-17a, entry text on the observer (HYBRID).**
1. The observer shows entry fields only from a named allowlist (the owner or the spec fills it). `recommend` and `suggested` are never shown, because entry files hold those model-written slots (`src/superclaude/skills/agent-work-report/scripts/common.py:139-141`) and the observer is navigation only. `how` stays hidden until the owner has reviewed what it holds.
2. Every shown field goes through `sanitize()` and is built as `rich.Text` from data, never parsed as markup. Block fields have a length cap the spec sets (the renderer clips single lines by width, `src/superclaude/cli/observe/render.py:158-160,325`, but its wrap helper "never truncates", `render.py:85`).
3. While the entry writer `superclaude orchestrator report-entry` is absent (it is: `report-entry` appears only in the report skill and the closeout scripts, and `cli/main.py` has no orchestrator group), the observer shows titles and links only. The three states (empty folder, zero rows, could not read) stay distinct.
4. Tests: a fixture with `recommend` and `suggested` filled shows neither; a 5,000-character field shows at most the cap; `[bold red]x[/]` shows literally.

**OA-17b, the questions panel (OURS on timing, CLAY on direction).**
1. The panel keeps its fixed read (`orchestration check --all --types question --run <id> --json`, `src/superclaude/cli/observe/adapter.py:32`, shape check at `adapter.py:111`, forbidden verbs at `adapter.py:34-50`, gate constants at `src/superclaude/cli/observe/commands.py:67,70`).
2. The screen label reads "questions read from Orca directly; a question already handled can appear as open", because the ledger cannot tell handled from open (`src/superclaude/cli/observe/questions.py:9-12`).
3. The spec and the screen say "one source for session facts (the sweep); the questions panel is the one exception", never the unqualified "one data source".
4. A tracked follow-up exists for one shared question id (which would also end the two question channels of D11). The owner names who owns it. It is not a precondition of the observer release; the sweep JSON has no questions block today (`report.py:613-640`).

## Strongest points

OURS:
1. The observer cannot give the person sweep classes without a file: a sweep may run up to 90 seconds as a cap (`src/superclaude/cli/sweep/probes.py:130`) against a 15-second observer cycle (`src/superclaude/cli/observe/collector.py:28-29`), and the observer imports nothing from the sweep today. The Clay advocate conceded "no file" leaves the screen without classes (`adversarial/adversarial/round1-advocate-V2.md`, Concessions 1).
2. The file and the panel use what is already built: the JSON is already echoed (`commands.py:278`), the Markdown already publishes atomically (`commands.py:153-193`), the questions read is fixed, gated and bounded (`adapter.py:32,34-50,111`; `commands.py:67,70`), and the sweep JSON has no questions block (`report.py:613-640`), so ending the exception first needs a design that does not exist (conceded, same file, Concessions 3).
3. The owner's rules hold: the sweep "Will Not: Recommend anything" (`src/superclaude/skills/sc-sweep-protocol/SKILL.md:61`), WC-16 stays unchanged, and a plain-English screen is what the person asked for on issue 409 (the observer TUI dashboard issue; `common.py:139-141` fields; D11 "One dashboard").

CLAY:
1. Classes depend on the window the producer chose (`classify.py:303-324`, `:922`), so "the newest file" alone can hand a reader a file made for another reader's window. Both advocates accepted this; it produced the reader selection rule.
2. Entry text needs a field allowlist and cap: entry files hold model-written `recommend` and `suggested` slots (`common.py:139-141`), `sanitize.py` removes terminal controls only and leaves bracket markup and long text unchanged (my read-only test; docstring `observe/sanitize.py:1-7`), and the wrap helper never truncates (`render.py:85`).
3. The questions ledger lists a handled question as open (`observe/questions.py:9-12`) and two question channels exist (D11); the label and a shared-id follow-up fix that honestly. The Clay advocate also dropped three of Clay's points (no file, titles-only for good, end the exception first) when the evidence went against them.

## Clay strengths to adopt

1. **Window-aware reader selection.** What: the observer shows the file's `window`, `observed_at` and age and reads the newest file for its own root; the work report runs its own `--window` when a file's window is too short. Why: a verified gap in OURS (`classify.py:303-324,922`); the newest file may have been made for another reader. Merge: add as rules 4 and 5 of OA-9; the shared file stays.
2. **Entry field allowlist, length cap and titles-and-links fallback.** What: show only named fields, never `recommend` or `suggested`, cap block fields, titles and links only while the entry writer is absent. Why: entry files hold recommendation slots and the sanitizer has no cap (`common.py:139-141`; tested). Merge: keeps OURS's "show entry text" and adds a guard; Clay's permanent titles-only is not adopted.
3. **Questions label with the handled-versus-open limit, and the qualified sentence.** What: label text and "one source for session facts; the questions panel is the one exception". Why: a handled question can show as open (`questions.py:9-12`) and the unqualified sentence is false (D11). Merge: replaces OURS's one-line label; the exception itself stays.
4. **Follow-up for one shared question id.** What: a tracked item that also ends the two question channels. Why: the only real fix for the open-versus-handled limit. Merge: filed, owner named by the owner, not a release blocker.
5. **Multi-root note.** What: the file sits under one checkout root (`commands.py:99`) while the watcher serves many repos. Why: a real design question OURS left as "a reader must be told which root". Merge: recorded as an open item; rule 4 matches on `scope.root`; the multi-repo reading itself is an inference (UNVERIFIED).
6. **"Views not on record" disclaimer.** What: Clay posted no text on OA-9 or OA-17. Why: honesty about whose argument was tested. Merge: carried in Unverified below.

Not from Clay but found in this debate and added: JSON v1 already holds the window and root (both papers treated it as a gap); the JSON and Markdown must pair by the same suffix (the Variant 1 advocate's concession).

## Our strengths that must be kept

- One shared sweep file as the one source of session facts: stateless, zero-token, read-only, eight proof-based classes with "could not determine".
- WC-16 unchanged (one coordinator sweep per 5 minutes); the sweep recommends nothing; the observer is navigation only with no write.
- The plain-English screen (entry text), not a permanent list of links.
- The questions panel's fixed, gated read and its labelled exception; no precondition that delays the observer.
- The three distinct observer states (empty folder, zero rows, could not read) and the rule that a missing or old file is never shown as "no sessions".
- The UNVERIFIED discipline: nothing unproven decides an outcome (for example the 90-second figure is a cap, not a measured time).

## Actions

| Action | Type | Target | Order or dependency |
|---|---|---|---|
| Write the contract note: the file, its name pattern and pairing rule, the selection rules (observer and work report), one owner | DOC | `docs/designs/observe-sweep-contract.md` (unwritten since 2026-11-13) | First |
| Save `<UTC>-sweep.json` beside the Markdown with the same suffix; add the pairing test | LOCAL CHANGE | `src/superclaude/cli/sweep/commands.py` (`_publish` and `run`), sweep contract test | After the note |
| Add `session_id` and `worktree_path` (empty allowed) to the JSON v1 row (carried from D11) | LOCAL CHANGE | `src/superclaude/cli/sweep/report.py` (`to_json`) | After the note; separate item |
| Observer reader: newest `*-sweep.json` for its root; show `window`, `observed_at`, age; old or missing as its own state | LOCAL CHANGE | `src/superclaude/cli/observe/` (new; no sweep reader exists today) | After the file is saved |
| Work report runs its own `sweep run --window` and reads that file (D11 side-by-side run still applies) | LOCAL CHANGE | `src/superclaude/skills/agent-work-report/scripts/sessions.py` | After the file is saved and the D11 side-by-side run |
| Entry field allowlist, length cap, `rich.Text` rendering; titles and links only until the entry writer exists | LOCAL CHANGE | `src/superclaude/cli/observe/render.py` and the spec | With the observer reader |
| Owner names the allowlist contents, the cap value, whether `how` may show, and what "old" means | DECISION | the spec's open items | Before the matching code |
| Questions label text and the qualified "one source for session facts" sentence | LOCAL CHANGE | `src/superclaude/cli/observe/render.py` and the spec | With the observer release |
| File a follow-up for one shared question id; the owner names its owner (recommendation only, nothing posted here) | DECISION | a new issue (not created) | Any time; not a release blocker |
| Record OA-9, OA-17a and OA-17b as settled to this answer | DOC | merged requirements OA section | Now |
| Keep PR 684 (Clay's merged work-report move); no change from this verdict | PR KEEP | PR 684 | Now |

## Implications

- **Watcher.** None. The poll reads neither the sweep file nor the observer.
- **Coordinator or orchestrator.** WC-16 is unchanged. The work report now makes its own sweep run with its own window, so the report adds a collection outside the coordinator's five-minute cap (WC-16 binds the coordinator's loop, not the report).
- **Dashboard.** The observer needs a new reader: today it reads Orca `worker-list` directly and has no reference to the sweep or to entry files (grep of `observe/*.py`). Because the entry writer (PR B of Clay's design) is absent, the first release shows titles and links only and the empty-folder state.
- **Claim pipeline.** None.
- **What breaks.** Nothing already built: no reader of the new file exists yet. Risk: a JSON and Markdown pair with different suffixes would give a reader the wrong pair; the pairing test guards it.
- **What the owner must know.** (1) JSON v1 already carries window, root and time, so no schema change is needed for the selection rule. (2) The sanitizer has no length cap but the renderer clips single lines; block fields are the gap. (3) Clay's views on these three questions are not on record; Clay's own advocate dropped three of Clay's points when the evidence went against them, so this ruling should not be read as a Clay decision. (4) Quick depth: one debate round, no invariant probe.

## Confidence

78 percent overall: OA-9 about 85, OA-17a about 72, OA-17b about 75. It would drop if the owner wants titles and links only on the observer, if a measured sweep turned out to take well under 15 seconds and the owner prefers one run per observer cycle (cost and WC-16 would then carry the case alone), or if the entry writer's slots differ from `common.py:139-141`. It would rise with a live measurement of the sweep's real run time and an owner ruling on the allowlist. The two advocates are the same model as the orchestrator and the Clay advocate was told a separable Clay benefit counts, so their agreement is weaker evidence than it looks; the one-round quick depth and the skipped invariant probe add to that.

## Unverified

- Clay's own views on OA-9 and OA-17 (no text by Clay on these was found; the alternative was argued from TOPICS.md and Clay's merged work).
- How long a sweep really takes (90 seconds is a cap; the observer's per-call timeout is itself marked "UNVERIFIED until the first permitted live read" at `observe/adapter.py:60-62`).
- That the observer's questions read is non-consuming (the technical reference's reading, not tested live).
- Whether a retention rule for `.dev/sweeps/` exists anywhere (none found in the sweep code).
- Whether a watcher serving many repos can read each repo's `.dev/sweeps/` (an inference by the OURS advocate, not stated by D07).
- What the entry field `how` holds and whether it is safe to show.
- That `observe/sanitize.py` is enough for every kind of text (tested only on terminal-control, bidi, zero-width and CR samples).
- Whether ruling-level facts in D11 (for example the 72 percent confidence there) still hold; this debate did not re-run D11.
- Verified in this run from code, no longer unverified: the entry writer `report-entry` is absent (appears only in the report skill and closeout scripts; `cli/main.py` has no orchestrator group); JSON v1 holds `observed_at`, `scope.root`, `window`.

## Debate artifacts

Folder: /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/OAG2/
- Position papers: `position-OURS.md`, `position-CLAY.md`
- Merged recommendation: `adversarial/merged-oag2-sweep-observer-recommendation.md`
- Worker contract: `adversarial/return-contract.yaml`
- In `adversarial/adversarial/`: `diff-analysis.md`, `round1-advocate-V1.md`, `round1-advocate-V2.md`, `debate-transcript.md`, `base-selection.md`, `base-selection-pass2.md`, `refactor-plan.md`, `merge-log.md`, `return-contract.yaml`, `variant-1-original.md`, `variant-2-original.md`
- No `invariant-probe.md`: Round 2.5 is skipped at quick depth. The adversarial skill ran (Skill `sc:adversarial` then `sc:adversarial-protocol`) with nested subagents: two advocates, one rubric pass-2 evaluator and one merge-executor.
