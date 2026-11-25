# Round 1 statement: advocate for Variant 1 (OURS), topic OAG2

Snapshot paths are relative to /home/coder/.cache/ic-snap-20261120/master. I re-checked these cited lines in this round (read-only): `sweep/commands.py:153-193,278`, `sweep/probes.py:130`, `observe/collector.py:28-29`, `WORKER-CONTRACT.md:287-289`, `sweep/classify.py:303-324,922`, `agent-work-report/scripts/common.py:139-141`. All match. I did not re-check `adapter.py`, `questions.py`, `sanitize.py` or the techref lines; those are taken from the papers.

## Position summary

Keep the recorded line: the sweep saves one `<UTC>-sweep.json` beside its Markdown report, the observer shows entry text taken from the living report and always passed through `sanitize.py`, and the questions panel stays as a labelled exception until a shared questions block is actually designed. Variant 2 is right about three real defects (window dependence, per-root location, sanitizer gaps), but each is a condition to write into the spec, not a reason to drop the file or the text.

## Steelman (per sub-question)

**OA-9 (no file, each reader collects for itself).** Strongest version: the sweep's classes are facts about a window, not about the world. `classify.py:303-324` and `:922` (`stale = last < ctx.window_start`) confirm it. A file written by a coordinator pass with a 5-minute window is a different answer from a daily report's window, so "one file, one truth" breaks as soon as two readers want different windows. Add that `_check_output` pins output to `<root>/.dev/sweeps/` (`commands.py:99`) while the watcher is designed for many repos, and that a second persisted artifact of Orca-derived evidence strings has no retention rule found. What it genuinely gets right: the file is only as true as the window its producer chose, and nobody has yet written down who chooses.

**OA-17a (titles and links only).** Strongest version: the observer's contract is navigation only, no Options, no Recommendation, no write. Entry files carry model-written `recommend`, `suggested`, `needs` and `how` slots (`common.py:139-141`). Free text from a model is the one input where a field list matters, and titles and links cannot carry a Recommendation. It also gets right that `sanitize.py` strips terminal controls only; its docstring (`observe/sanitize.py:1-7`) leaves markup safety to the renderer, and I accept V2's test that bracket markup and a 5,000-character string pass unchanged (not re-run by me).

**OA-17b (end the questions exception now).** Strongest version: D11 itself said "one data source" is false until the owner accepts the exception or the sweep gains a questions block, and a label does not change what the code does. The ledger cannot tell handled from open (`observe/questions.py:9-12`), so shipping the panel fixes a known weakness into a released screen; a shared question id is the only real cure and is cheapest before release. It gets right that two question channels (the observer's `orchestration check` and the report's "Needs you") are a real duplication.

## Strengths claimed

1. **The file extends a path that exists and is tested.** `_publish` (`sweep/commands.py:153-193`) already does temp file, fsync, then `os.link` to the first free name, never overwriting. The JSON today goes only to standard output (`commands.py:278`, `click.echo(payload)`). Verified. A second link of the same atomic kind is a small change.
2. **The observer cannot afford its own sweep.** `Budget.total_s` defaults to 90.0 (`sweep/probes.py:130`); the observer cycle is `INTERVAL = 15.0` and `CYCLE_BUDGET = 15.0` (`observe/collector.py:28-29`). Verified, and V2 uses the same numbers (C-002). Under "no file" the observer never shows the eight sweep classes, only its own worker-list read, so screen and report can show different class words. The file is the only route that keeps "the same facts in the same way" (issue 409 goal).
3. **WC-16 stays intact.** `WORKER-CONTRACT.md:289` allows the coordinator one `/sc:sweep` per 5 minutes and says the report "is a dated local file; it is never posted." One saved file lets any number of readers look without another collection. V2's cost section admits its option "would need an edit" to WC-16.
4. **The window objection has an in-line answer.** V1's hybrid (U-003): a reader needing another window runs `superclaude sweep run --window <since its last report>`, which also saves a file; the observer reads the newest one. That is "one writer path, stamped files", not "one file for everyone".
5. **The questions panel is built, gated and bounded.** Fixed argv `orchestration check --all --types question --run <id> --json` (`observe/adapter.py:32`), a forbidden-verb set (`adapter.py:34-50`) and two owner-cited gate constants (`observe/commands.py:67,70`), per V1. Sweep JSON v1 has no questions block (12 top-level keys, `sweep/report.py:613-640`), so V2's "design it first" needs a schema change, a new probe and tests inside a sweep that is deliberately stateless and "recommends nothing" (`sc-sweep-protocol/SKILL.md:61`).
6. **Entry text is what makes the observer "the one screen".** Without the plain-English fields (`common.py:139-141`) the person opens a second report for each item. V2 itself lists this under "What it risks".
7. **The honest-exception route is the D11 verdict.** D11 "One honest exception" said to write the exception down, not hide it. "One data source except the questions panel" is a true, qualified statement; V2's reading treats it as a false one.

## Weaknesses identified in Variant 2

1. **It does not deliver its own premise.** V2's cost section admits the observer "keeps its own worker-list read" because a sweep cannot fit 15 s. So "each reader gets its own collection" is not what happens for the observer: it gets a partial collection (no classes) while the report gets a full one. That is the "readers disagree" outcome V2 lists as a risk, chosen on purpose.
2. **The window argument supports stamped files, not no files.** Window dependence (`classify.py:303-324,922`) is handled by showing the file's window and age, which V1 does for age (U-001: `observed_at`, STALE after 45 s per the diff analysis). Deleting the file removes the observer's only route to the classes.
3. **Per-root location is a spec item, not a veto.** `_check_output` (`commands.py:99`) keeps output inside one root; V1 names this ("a reader must be told which root"). A watcher that already loops over repos could read each repo's `.dev/sweeps/` (my inference, not something D07 states). V2 offers no alternative location either.
4. **The disk-footprint argument is thin.** `.dev/sweeps/` already holds the Markdown report built from the same rows. V2 itself marks "no retention rule" UNVERIFIED, and if true it applies to the Markdown too: a gap to fix once for the folder, not a cost of the JSON.
5. **Titles-only costs the goal.** It sends the person from "the one screen" to the report for every item, which V2 admits. A field allowlist gives the safety V2 wants at far lower cost.
6. **Ending the exception now needs a design that does not exist.** A shared question id needs the worker contract, the report and the observer to agree on one id. V2 gives no schema and no owner, and puts it on the critical path of the observer release.
7. **Its sanitizer finding argues for a fix, not for removing text.** Bracket markup and long strings passing `sanitize.py` is cured by a length cap and `rich.Text` built from data (V1's stated mechanism), not by showing nothing.

## Concessions

- **C-003 is a real gap in V1.** V1 says the spec "must say who passes which `--window`" and does not say it. Until it does, a coordinator file with a short window can mislead a daily-report reader. The window start and end must be recorded in the file and a reader must have a rule to re-run on a mismatch.
- **Collision suffix.** `_publish` names reports `<stem>.md`, then `<stem>-2.md` and on (`commands.py:182`). A JSON sibling "with the same stem" must follow whichever suffix won, or the pair desyncs. V1 called this "about one function"; it is somewhat more.
- **C-008 stands.** `sanitize.py` is necessary, not sufficient. Entry text needs a length cap and a field allowlist as well. V1's "always through sanitize.py" alone was too thin.
- **C-007.** `recommend` and `suggested` must not appear on a navigation-only screen. The observer shows a listed subset only.
- **A-001 is a real hole.** The techref says the only entry writer, `superclaude orchestrator report-entry`, is designed and absent (`OBSERVER-SWEEP-DASHBOARD-TECHNICAL-REFERENCE.md:805,820`). V1 assumed entry files exist. I take the diff analysis's citation as given and did not re-verify it.
- **C-010 / U-006.** The ledger limit (`questions.py:9-12`) is a true weakness in V1's OA-17b position. The label must say the panel may list a handled question as open, not only "separate source".
- **U-005 (multi-repo)** is a design point V1 did not solve.

## Shared assumption responses

- **A-001 (entry files exist for the observer to read): QUALIFY.** They exist as a designed format and as files moved by `run.py`, but the writer is not built, so OA-17a holds only once the writer lands; the spec should gate "entry text on the screen" on that and keep the empty-folder state distinct.
- **A-002 (the observer will be changed to read the sweep file or entry files at all): ACCEPT.** True for both sides; V1 says so (no shared code today). The change is the point of the topic, one reader for the file and one for entry folders.
- **A-003 (the 90 s `Budget(total_s)` is how long a sweep takes): QUALIFY.** `probes.py:130` is a cap (verified, `total_s: float = 90.0`), not a measurement, so "cannot fit in 15 s" should read "may not fit". Even a typical 5 s sweep is a heavier second collection per cycle, and WC-16's 5-minute rule is unaffected, so V1 does not depend on the 90 s figure.
- **A-004 (the screen is read by a person, not an agent): ACCEPT.** The observer is a terminal dashboard for a person, which makes the "plain-text instruction passes" finding (V2 fact 5) a low practical risk; if a model ever reads the screen, the cap and field list matter more.

## Per-point verdicts

| Point | Winner | Confidence | One-line evidence |
|---|---|---|---|
| C-001 (does a sweep JSON file exist) | V1, with a window stamp added | 72% | Observer cannot run a sweep in 15 s (`collector.py:28-29` vs `probes.py:130`), so no file means no classes on screen; `_publish` already exists (`commands.py:153-193`). |
| C-003 (window dependence) | V2 on the diagnosis, hybrid on the fix | 65% | `classify.py:303-324,922` makes classes window-bound and V1 left it open; fix is the window recorded in the file plus a reader-run `--window` (U-003). |
| C-006 (entry text on the observer) | V1 with a field allowlist and cap | 60% | The one-screen goal needs the plain-English fields; `recommend` and `suggested` (`common.py:139-141`) must be excluded by list. Titles-only is the fallback while the entry writer is absent (A-001). |
| C-009 (questions exception) | V1 for the observer release, V2 for the follow-up | 68% | Panel is built and gated (`adapter.py:32,34-50`, `commands.py:67,70`); sweep JSON has no questions block (`report.py:613-640`). A shared id is the right next step but has no design. |

## Hybrid I would endorse

1. Write the JSON as a sibling of the `.md`, following whichever suffix won, with the window start and end inside it.
2. The observer reads the newest file, shows `observed_at` and age, and treats missing or old as its own state, never "no sessions".
3. The report runs its own `sweep run --window` and reads that file (this nearly erases X-002).
4. Observer entry text: a listed subset of fields (no `recommend`, no `suggested`), a length cap, `rich.Text` from data. Titles and links only until the entry writer exists (A-001).
5. The questions panel stays, labelled with the handled-versus-open limit, and a shared question id is filed as the next design item.
