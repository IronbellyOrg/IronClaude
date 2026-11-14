# Verify, docs gate cycle 1 (qualitative verifier)

Verifier: rf-qa-qualitative, `fix_authorization: false`. Prompt: `qa/docs/prompts/T301-prompt.md`.

## Scope and method

- Judged the two `F_0` findings against the live files, not the fix log. Re-read `sweep.md` (70 lines now), `SKILL.md` (66 lines now), `pragmatic.md:22-26`, the new pins in `tests/commands/test_sweep_command.py:511-544`, and the Phase 1 code the new sentences describe (`classify.py`, `report.py`, `models.py` under `src/superclaude/cli/sweep/`).
- Change set confirmed from disk: `find src tests docs plugins CHANGELOG.md .gitignore Makefile pyproject.toml -newer qa-primitive-path-report.md` lists only `sweep.md`, `SKILL.md` and `test_sweep_command.py`. `pragmatic.md` is dated 2026-11-11 20:29, `WORKER-CONTRACT.md` and DESIGN 2026-11-12 13:35, the guide and its plugin copy 13:52 and 13:53, all older than every cycle-0 report. `cmp` of the guide and the plugin copy exits 0.
- Experiments ran only on private copies under a `mktemp -d /tmp/ironclaude-batch.*` folder, deleted by an exit trap (checked: gone; the older `/tmp/ironclaude-batch.ptdj0orr` is not mine and was left alone). No live Orca command was run.
- Runs of mine: `uv run pytest tests/core tests/commands tests/recommend tests/skills -v` gave `2647 passed in 54.93s`; `uv run ruff check` on the two test files: `All checks passed!`; `uv run ruff format --check` on the same two files: `2 files already formatted`; the two severity modules: `90 passed`; `ruff check src/superclaude/cli/main.py`: clean.

## Findings

### DOC-F1 (MAJOR): RESOLVED

- `src/superclaude/commands/sweep.md:16` now says: "The report also states, as facts to review, `Safe to close`, `Removable` and `Next inspection` (what to read next); these are observations, not advice, and the coordinator or person decides." The same sentence is at `src/superclaude/skills/sc-sweep-protocol/SKILL.md:66`, the last line of `## Boundaries`.
- The sentence is true of the report: the columns exist at `report.py:402-404`, `:419` (`NEXT_INSPECTION`) and `:454` (`Removable`); `classify.py:447-496` gives them only the values "no" or "could not determine" with a stated observed reason (never "yes"); every `NEXT_INSPECTION` value starts with "read" (`report.py:42-55`, comment at `:41`: "what to read or check, nothing more").
- It does not contradict the flat claims it qualifies: `sweep.md:69` and `SKILL.md:61` forbid advice or a next step "of its own" to the report or reply, and the new sentence says the columns are observations that the coordinator or person acts on or not. Read-only claims elsewhere (WC-16 at `WORKER-CONTRACT.md:277`, guide `HOW-WE-WORK.md:334`, `CHANGELOG.md:12`) are untouched and still true.
- Words: `grep -n -i -w -E 'stop|retry|release|merge|removal'` on both primitives exits 1 (no hit); no en or em dash in either file or the test file (`grep -P`, exit 1). `Removable` and `close` are not matched by the whole-word regex.
- Pins: `test_sweep_command_says_report_columns_are_observations_not_advice` and `test_sweep_skill_boundaries_say_report_columns_are_observations_not_advice` (`test_sweep_command.py:523-528`). My own mutations on a private copy: removing the sentence from the command copy (M1) fails the first, removing it from the skill copy (M2) fails the second, weakening "observations, not advice" to "notes" (M7) fails the first; baseline copy 121 passed.
- The alternative fix (narrowing WC-16 and the routing wording) was not applied and was never required; the owner-approved text is unchanged.

### DOC-F2 (MAJOR): RESOLVED

- `sweep.md:16` says: "In Phase 1 the classes stalled (proved) and fenced are not observed, so a zero count there means nothing; the report says so." Skill step 4 (`SKILL.md:26`) says the same sentence and adds: "Print each of those two counts with the mark `(not observed in Phase 1)` after the number, so the caveat travels with the counts."
- It is true. `fenced_evidence` is assigned nowhere under `src/superclaude/cli/sweep/` (only read at `classify.py:198`, `:205`, `:220`; default `"unreadable"` at `models.py:87`), and `C_STALLED` is returned only at `classify.py:203` (needs `fenced_evidence == "absent"`) and `C_FENCED` only at `classify.py:221` (needs `"present"`). "The report says so" is true: `SP24_LINE` ("Stalled and fenced are not observed in Phase 1; a zero count does not mean none occurred.", `report.py:36-39`) is printed unconditionally at the top of the Sessions section (`report.py:392`).
- The step-4 instruction can be followed: `counts` holds all eight classes, zeros included (`classify.py:961`, `report.py:665`), so a "stalled (proved)" and a "fenced" number always exist to mark. The number stays the genuine summary number; only the mark is added.
- Exempt reply: `SKILL.md:35` still reads "only the summary counts and the report path are printed" (pinned case `exempt-reply-is-counts-and-path`, `test_sweep_command.py:251-254`, passes) and the five conditions, the final-reply-only rule and the exclusions are unchanged. The added sentence at `SKILL.md:43` says the mark "is part of the counts, not a gloss of a label and not advice". Against the style rule (`pragmatic.md:23`): the reply still has no DONE / NEXT table, no WHAT / WHY / RECOMMENDED ACTION wrapper, no recommendation and no gloss of a label; the style says the reply "contains the summary counts and the report path" and `pragmatic.md:26` keeps the truthfulness rules in force, which is what the mark serves. `pragmatic.md` is unchanged (diff vs HEAD: 11 insertions, 7 deletions, same as cycle 0). See note DOC-N1 for the one wording gap.
- Pins: `test_sweep_command_says_phase1_stalled_and_fenced_zero_means_nothing`, `test_sweep_skill_step4_says_phase1_stalled_and_fenced_zero_means_nothing`, `test_sweep_skill_step4_prints_the_phase1_mark_with_the_counts`, `test_sweep_exempt_reply_keeps_the_phase1_mark_on_the_counts` (`test_sweep_command.py:531-544`). My mutations: M3 (command sentence removed), M4 (step 4 sentence removed), M5 (mark sentence removed), M6 (exempt-reply sentence removed) and M8 (step 4 reworded to "a zero count there is fine") each fail exactly one named test, 120 others pass.
- The alternative (a WC-16 sentence saying the two zeros carry no meaning) was not applied; it is not required and stays an owner decision.

### Cycle-0 FAIL rows tied to the two findings

`qa-reader-clarity-report:C1` (terms defined for a newcomer), `:C3` ("recommends nothing" against the report content) and `:C10` (WC-16 and class wording against what Phase 1 can output) failed in cycle 0 because of RC-2, RC-1 and RC-2. They are not in the 131 PASS set. With DOC-F1 and DOC-F2 resolved as above, the claims those three checks made are now met in `sweep.md` and the skill; `:C1` still has the minor gap of note DOC-N2.

## Checks

131 ids, the cycle-0 PASS set of `cycle-ledger.md`. "Moved" means a line number or a count in the check's text changed (`sweep.md` lines from 16 on moved by +2, `SKILL.md` lines 1 to 64 did not move, test count 115 to 121, four-folder count 2641 to 2647) and the claim still holds in substance. "Scratch" means the check described a saved artifact or scratch run that cannot be re-run; for those I confirmed from disk that nothing the check relied on changed.

| Check id | Result | Basis |
|---|---|---|
| qa-primitive-path-report:C1 | PASS (moved) | `sweep.md` is 70 lines; `grep 'src/superclaude'` exit 1 |
| qa-primitive-path-report:C2 | PASS (moved) | `SKILL.md` is 66 lines; same grep exit 1 |
| qa-primitive-path-report:C3 | PASS | `WORKER-CONTRACT.md` not newer than the cycle-0 reports (13:35); no path added |
| qa-primitive-path-report:C4 | PASS | guide and plugin copy `cmp` exit 0, both sha256 `a70220e0...`; not newer than the reports |
| qa-primitive-path-report:C5 | PASS (moved) | `sweep.md:51` installed skill path first, `:53-55` project `.claude/` copy as dev-checkout copy |
| qa-primitive-path-report:C6 | PASS | `SKILL.md:15` names `~/.claude/commands/sc/sweep.md` first, project `.claude/` copy second; unchanged |
| qa-primitive-path-report:C7 | PASS (moved) | core-doc paths still `~/.claude/WORKER-CONTRACT.md` (`sweep.md:18`, `:22`); `Makefile` and installer files not newer than the reports |
| qa-primitive-path-report:C8 | PASS | `SKILL.md:33` still names the installed style path as information only; installer code unchanged |
| qa-primitive-path-report:C9 | PASS | steps 1 and 2 are still the only commands; the new sentences add no command or path |
| qa-primitive-path-report:C10 | PASS | `cmp` exit 0; `git status` shows no sweep primitive under `plugins/` |
| qa-primitive-path-report:C11 | PASS (moved) | 2647 passed; `test_sweep_no_src_superclaude_path` still at `test_sweep_command.py:162-164` |
| qa-command-skill-report:C1 | PASS | `sweep.md:2,3,8,9` read: `name: sweep`, one-line description, `argument-hint`, `allowed-tools: Skill`; unchanged |
| qa-command-skill-report:C2 | PASS (moved) | Title, `## Triggers` (`:20`), `## Usage` (`:24`), `## Options` (`:33`) in the same order; new paragraph sits before Triggers |
| qa-command-skill-report:C3 | PASS (moved) | Activation block `sweep.md:44-49` unchanged |
| qa-command-skill-report:C4 | PASS (moved) | `sweep.md:49-57` installed path first, project copy second, "Skills read `~/.claude/skills/` first" |
| qa-command-skill-report:C5 | PASS (moved) | `sweep.md:22` first sentence unchanged, "Nothing starts it automatically." kept |
| qa-command-skill-report:C6 | PASS (moved) | no `## Unattended mode` and no `--unattended` (read all 70 lines); never-as-worker at `:18`, `:42`; WC-16 file unchanged |
| qa-command-skill-report:C7 | PASS | `SKILL.md:4` unchanged and equals `test_sweep_command.py:30-33` literal |
| qa-command-skill-report:C8 | PASS | `SKILL.md:23-27,29` read: five steps, 120000 on steps 1 and 2, fallback only on "command not found"; step 4 only gained sentences |
| qa-command-skill-report:C9 | PASS | step 3 takes only `report_path` and `summary`; keys printed still exist; `counts` holds all eight classes (`classify.py:961`, `report.py:665`) |
| qa-command-skill-report:C10 | PASS | step 5 at `SKILL.md:27` unchanged |
| qa-command-skill-report:C11 | PASS | Will Not list `SKILL.md:59-64` unchanged; new sentences state facts and "observations, not advice"; no tool added |
| qa-command-skill-report:C12 | PASS | `grep -rn 'src/superclaude'` on both primitives exit 1 |
| qa-command-skill-report:C13 | PASS | whole-word grep for stop, retry, release, merge, removal exit 1 on skill and on command |
| qa-command-skill-report:C14 | PASS (moved) | Options table now `sweep.md:35-40`, eight-class sentence `:14`, both unchanged; CLI code not newer than the reports |
| qa-command-skill-report:C15 | PASS (moved) | all 121 tests pass; the 115 older cases are present (121 = 115 + 6, 2647 = 2641 + 6) |
| qa-command-skill-report:C17 | PASS (moved) | `pragmatic.md` unchanged (dated 2026-11-11 20:29, `git diff --stat`: 11 insertions, 7 deletions); the style tests now sit after `test_sweep_command.py:547` |
| qa-command-skill-report:C18 | PASS (moved) | same: style file and its seven hunks unchanged; its bounded-diff test passes |
| qa-command-skill-report:C19 | PASS | `SKILL.md:35-45` keeps the same five conditions and final-reply-only rule; line 43 only gained the mark sentence; `pragmatic.md:23-24` unchanged |
| qa-command-skill-report:C20 | PASS | the positive-case pins are unchanged and pass (no existing pin edited; test count is old plus six) |
| qa-command-skill-report:C21 | PASS | exclusion pins unchanged and pass; `SKILL.md:47` unchanged |
| qa-command-skill-report:C22 | PASS | `SKILL.md:27,29` unchanged; stderr and failure pins pass |
| qa-command-skill-report:C25 | PASS | tool lists unchanged (`SKILL.md:4`, `sweep.md:9`); `~/.claude/output-styles/pragmatic.md` dated 2026-11-11 16:25, 0 matches for `chat-summary`; no `~/.claude/skills/sc-sweep-protocol` and no `~/.claude/commands/sc/sweep.md` (re-checked live) |
| qa-command-skill-report:C26 | PASS | `grep -rn 'chat-summary\|sc-sweep-protocol' src/superclaude/cli/sweep` exit 1; that folder not newer than the reports |
| qa-command-skill-report:C27 | PASS | new tests only call `_text`, `_section`, `_step`, `_skill_parts` on the real files; module imports are `re`, `Path`, `pytest` |
| qa-command-skill-report:C28 | PASS (moved) | mine: 121 passed in the file run, 2647 passed in the four folders, ruff check and format check clean, severity modules unchanged (not newer) and 90 passed |
| qa-command-skill-report:C29 | PASS (scratch) | cycle-0 mutations cannot be re-run; the pinned sentences they hit are untouched (the fix only added sentences, no existing pin changed) and my eight new mutations all behaved as expected (baseline copy 121 passed, each mutation one named failure) |
| qa-command-skill-report:C30 | PASS (moved, scratch) | raw `test-sweep-command.txt` ends `121 passed`, exit code 0, 121 PASSED lines, 0 FAILED or ERROR; summary table says 121; anchors `C:51` and `C:55` match `sweep.md:51` and `:55`, `C:9` and all `K:` and `S:` anchors unchanged; I did not recount the 14 + 74 + 15 + 12 case split (total 121 = 115 + 6 matches the run) |
| qa-command-skill-report:C31 | PASS | `WORKER-CONTRACT.md` and DESIGN unchanged since 13:35, guide `:405` bullet present (`grep`), `cmp` exit 0 |
| qa-command-skill-report:C32 | PASS | no TODO, TBD, FIXME and no non-ASCII byte in `sweep.md`, `SKILL.md` or `test_sweep_command.py` (`grep -P`, exit 1 on all three) |
| qa-contract-rule-report:C1 | PASS | `WORKER-CONTRACT.md` and DESIGN dated 13:35, older than the reports; not edited by the fix |
| qa-contract-rule-report:C2 | PASS | same file, unchanged |
| qa-contract-rule-report:C3 | PASS | same file, unchanged |
| qa-contract-rule-report:C4 | PASS | same file, unchanged |
| qa-contract-rule-report:C5 | PASS | same file, unchanged |
| qa-contract-rule-report:C6 | PASS | same file, unchanged |
| qa-contract-rule-report:C7 | PASS | `tests/skills/test_worker_contract.py` dated 07:13, unchanged |
| qa-contract-rule-report:C8 | PASS | same test file, unchanged |
| qa-contract-rule-report:C9 | PASS | same test file, unchanged |
| qa-contract-rule-report:C10 | PASS | same test file, unchanged |
| qa-contract-rule-report:C11 | PASS | same test file, unchanged |
| qa-contract-rule-report:C12 | PASS | same test file, unchanged |
| qa-contract-rule-report:C13 | PASS | same test file, unchanged |
| qa-contract-rule-report:C14 | PASS | same test file, unchanged |
| qa-contract-rule-report:C15 | PASS | developer guide dated 07:14, unchanged |
| qa-contract-rule-report:C16 | PASS (moved) | now 2647 passed (was 2641) and ruff clean |
| qa-contract-rule-report:C17 | PASS | WC-16 and the CLI unchanged; the new "not observed in Phase 1" claim agrees with the code (`classify.py:198-221`, `models.py:87`) |
| qa-contract-rule-report:C18 | PASS | WC-16 owner-approved text and R2 bullet unchanged; guide and plugin copy equal |
| qa-contract-rule-report:C19 | PASS | negative tests unchanged and pass |
| qa-contract-rule-report:C20 | PASS | no contract or guide text changed |
| qa-routing-rows-report:C1 | PASS | guide row at `HOW-WE-WORK.md:334` read, unchanged (dated 13:52) |
| qa-routing-rows-report:C2 | PASS | R2 bullet at `HOW-WE-WORK.md:405` read, unchanged |
| qa-routing-rows-report:C3 | PASS | R2 and WC-16 both unchanged |
| qa-routing-rows-report:C5 | PASS | `cmp` exit 0 |
| qa-routing-rows-report:C6 | PASS | parity test passes in the 2647 run |
| qa-routing-rows-report:C7 | PASS | `tests/core/test_how_we_work_routing_table.py` dated 13:52, unchanged, passes |
| qa-routing-rows-report:C8 | PASS | `tests/recommend/test_routing_refresh.py` dated 06:21, unchanged, passes |
| qa-routing-rows-report:C9 | PASS | `commands.md:116` read: the `/sc:sweep` row, four cells, unchanged (dated 13:53) |
| qa-routing-rows-report:C10 | PASS | developer guide and contract line unchanged |
| qa-routing-rows-report:C11 | PASS | `CHANGELOG.md` dated 13:54, unchanged |
| qa-routing-rows-report:C12 | PASS | guide unchanged since the report; `src/superclaude/core/CLAUDE.md` not newer |
| qa-routing-rows-report:C13 | PASS | no row removed or reworded since the report |
| qa-routing-rows-report:C14 | PASS | rows `HOW-WE-WORK.md:334` and `commands.md:116` read; none of the five words in either (`commands.md` hits for "merge" are other commands' rows) |
| qa-routing-rows-report:C15 | PASS | `git status --short -- .claude` empty; no `WC-14` added |
| qa-routing-rows-report:C16 | PASS (moved) | routing modules pass; sweep test file now 121 passed instead of 115; ruff check and format check clean |
| qa-routing-rows-report:C17 | PASS (scratch) | cycle-0 mutation copies cannot be re-run; guide, plugin copy and routing tests are byte-unchanged, so the result stands |
| qa-routing-rows-report:C18 | PASS | `pragmatic.md` unchanged; the summary-only reply with the `(not observed in Phase 1)` mark does not conflict with any routing row |
| qa-routing-rows-report:C19 | PASS | `git check-ignore -v .dev/sweeps/x.md` matches `.gitignore:256` (exit 0); `.dev/tasks/to-do/x.md` not ignored (exit 1) |
| qa-readonly-claims-report:C1 | PASS | `src/superclaude/cli/sweep/` not newer than the reports; read-only code claims unchanged |
| qa-readonly-claims-report:C2 | PASS | `_publish` and the one-report claim unchanged; `sweep.md:14` first lines unchanged (new text is a separate paragraph) |
| qa-readonly-claims-report:C3 | PASS | `sweep.md:9` `allowed-tools: Skill` unchanged |
| qa-readonly-claims-report:C4 | PASS | `SKILL.md:4` unchanged |
| qa-readonly-claims-report:C5 | PASS | skill steps unchanged in structure; keys relayed still exist |
| qa-readonly-claims-report:C6 | PASS | five words: no hit; the new `Safe to close` is a column name inside a sentence that says it is an observation, not a recommendation (see DOC-N3, DOC-N4) |
| qa-readonly-claims-report:C7 | PASS | `classify.py:447-496` re-read: values only "no" or "could not determine"; `NEXT_INSPECTION` values all "read ..." |
| qa-readonly-claims-report:C8 | PASS | guide rows, plugin copy, `commands.md:116`, CHANGELOG and `.gitignore:255-256` unchanged; `cmp` exit 0 |
| qa-readonly-claims-report:C9 | PASS | R2 bullet unchanged |
| qa-readonly-claims-report:C10 | PASS | WC-16 unchanged; `sweep.md:22` still carries the 5-minute cap and the WC-16 pointer |
| qa-readonly-claims-report:C11 | PASS (moved) | `WORKER-CONTRACT.md:23` and developer guide unchanged; `sweep.md:18` and `:70` still say a worker never runs it, `:42` "There is no worker mode" |
| qa-readonly-claims-report:C12 | PASS | style rule unchanged; skill Final reply keeps the same conditions, exclusions and chat-presentation-only scope (`SKILL.md:51`) |
| qa-readonly-claims-report:C13 | PASS (moved) | Options table unchanged (now `sweep.md:35-40`); `commands.py` and `probes.py` not newer |
| qa-readonly-claims-report:C14 | PASS (scratch) | `phase11/12/13-validation.md` dated 06:33, 07:16, 13:56, unchanged; the re-run commands they record still pass (my runs above) |
| qa-reader-clarity-report:C2 | PASS | Options table and limits unchanged; CLI not newer |
| qa-reader-clarity-report:C4 | PASS | `sweep.md:14` "the report is the one file it adds" unchanged; `_publish` unchanged (RC-10 note stays minor) |
| qa-reader-clarity-report:C5 | PASS | steps 1 to 5 against exit codes, JSON keys and the last report line "Report complete" (`SKILL.md:25`): unchanged; the added mark does not touch them |
| qa-reader-clarity-report:C6 | PASS | step 4 field list unchanged (RC-6 note stays minor) |
| qa-reader-clarity-report:C7 | PASS | skill `## Final reply` against `pragmatic.md:22-26`: still agree (see DOC-N1 for the one gap) |
| qa-reader-clarity-report:C8 | PASS (moved) | command `:18`, `:42`, skill `:19` and contract line 23 still agree: coordinator or person, never a worker |
| qa-reader-clarity-report:C9 | PASS | WC-16 text unchanged (RC-3 to RC-5 notes stay minor) |
| qa-reader-clarity-report:C11 | PASS | guide, plugin copy, `commands.md:116` and developer guide unchanged and equal to the command's claims |
| qa-reader-clarity-report:C12 | PASS | CHANGELOG, `.gitignore:256` and behaviour unchanged |
| qa-reader-clarity-report:C13 | PASS (moved) | test subsets still pass inside the 2647 run (counts differ by the six new tests only) |
| qa-coordinator-cadence-report:C1 | PASS | WC-16 and contract line 110 unchanged |
| qa-coordinator-cadence-report:C2 | PASS | same |
| qa-coordinator-cadence-report:C3 | PASS (moved) | `sweep.md:22` (was 20) carries the 5-minute cap, names WC-16, attaches to the coordinator |
| qa-coordinator-cadence-report:C4 | PASS | WC-16 additive wording unchanged |
| qa-coordinator-cadence-report:C5 | PASS | guide `:405` unchanged |
| qa-coordinator-cadence-report:C6 | PASS | guide, DESIGN, plugin copy unchanged; `cmp` exit 0 |
| qa-coordinator-cadence-report:C8 | PASS | contract line 110 and WC-16 unchanged; `worktree ps` still not called by the CLI |
| qa-coordinator-cadence-report:C9 | PASS | the new sentences state no cadence; CHANGELOG, `commands.md:116`, developer guide and skill carry no other cadence |
| qa-coordinator-cadence-report:C10 | PASS | `SKILL.md:64` still forbids "schedule anything"; WC-16 unchanged |
| qa-coordinator-cadence-report:C13 | PASS (moved) | the four test files pass in the 2647 run |
| qa-conventions-report:C1 | PASS | `sweep.md:1-10` frontmatter keys and order unchanged |
| qa-conventions-report:C2 | PASS (moved) | heading order unchanged; the new paragraph is under the title, before Triggers |
| qa-conventions-report:C3 | PASS (moved) | Options table, escaped pipe and closing "There is no worker mode and no flag for one." (`:42`) unchanged |
| qa-conventions-report:C5 | PASS | `SKILL.md:1-11` frontmatter and extended-metadata comment unchanged |
| qa-conventions-report:C6 | PASS | skill headings unchanged (new text is in step 4, the Final reply paragraph and Boundaries, no new heading) |
| qa-conventions-report:C8 | PASS | test location, naming, constants and style kept; the six new tests follow the same pure file-content style; ruff check and format check pass |
| qa-conventions-report:C10 | PASS | contract line 23 and developer guide unchanged |
| qa-conventions-report:C11 | PASS | WC-16 heading and placement unchanged |
| qa-conventions-report:C12 | PASS | `test_worker_contract.py` unchanged |
| qa-conventions-report:C13 | PASS | guide and plugin copy equal (`cmp` exit 0); rows unchanged |
| qa-conventions-report:C14 | PASS (moved) | `_OTHER_COMMANDS` and refresh-set edits unchanged; related tests pass in the 2647 run |
| qa-conventions-report:C15 | PASS | `commands.md:116` unchanged |
| qa-conventions-report:C18 | PASS | `CHANGELOG.md` unchanged (dated 13:54) |
| qa-conventions-report:C20 | PASS | `.gitignore:255-256` unchanged; `git check-ignore` matches line 256 |
| qa-conventions-report:C21 | PASS | `pragmatic.md` unchanged, so its qualifier count and no-dash result stand; no dash in the fix's added text |
| qa-conventions-report:C22 | PASS | skill still has the four titled parts (Exempt reply, What establishes the assignment, What stays ordinary, Scope) and names the installed style path |
| qa-conventions-report:C23 | PASS | no `src/superclaude/` path and no en or em dash in `sweep.md`, `SKILL.md`, `test_sweep_command.py` (greps exit 1) |
| qa-conventions-report:C24 | PASS (moved) | file run 121 passed, four folders 2647 passed, `ruff check src/superclaude/cli/main.py` passed |
| qa-conventions-report:C25 | PASS | `git status --short -- .claude` empty |

The id list above equals the 131 ids of the "Cycle-0 PASS set" section of `consolidated-findings-cycle0.md` (compared with `sort` and `diff`: identical, no duplicate). Result: 131 PASS, 0 FAIL.

## New findings

No new BLOCKING or MAJOR finding. Four MINOR notes from the reader pass; none makes a claim false, none fails the gate and none needs a fix pass.

| Id | Severity | Where | Note |
|---|---|---|---|
| DOC-N1 | MINOR | `pragmatic.md:23` against `SKILL.md:26`, `:43` | The style says the exempt reply "contains the summary counts and the report path" and never mentions the `(not observed in Phase 1)` mark; only the skill states it. Not a conflict: the mark breaks none of the style's exclusions (no table, no wrapper, no advice, no gloss of a label) and `pragmatic.md:26` keeps the truthfulness rules in force. A person who reads only the style will not know the mark exists. The fix log records the same residual and the style file was out of this cycle's scope. |
| DOC-N2 | MINOR | `sweep.md:14`, `:16`; `SKILL.md:26` | `fenced` and `(proved)` are never defined in the command or the skill, and `fenced` is not among the example classes in `sweep.md:14`. A newcomer cannot say what the two classes mean, but the sentence still tells them what matters: a zero there means nothing. |
| DOC-N3 | MINOR | `sweep.md:16`; `SKILL.md:66` | The sentence calls `Safe to close` and `Removable` "facts to review" but does not say that Phase 1 never answers "yes" for either (`classify.py:447-496`, docstring at `:472`). A reader can still picture a green-light "yes". Optional fix: add "in Phase 1 the answer is `no` or `could not determine`, never `yes`". |
| DOC-N4 | MINOR | `sweep.md:16` against `:69`; `SKILL.md:66` against `:61` | `Next inspection (what to read next)` points to a next read, while the Will Not lists say the skill adds no "next step of its own". Reconciled by the words "of its own" and by the values, which are read-only pointers (`report.py:41-55`); no false claim. |

## Reader pass (the changed passages read as a newcomer)

- Report columns (`sweep.md:16`, `SKILL.md:66`): a newcomer now learns three things in one sentence: the report has `Safe to close`, `Removable` and `Next inspection`; they are observations to review, not advice; the coordinator or person decides. That is enough to remove the cycle-0 contradiction with "recommends nothing". What the reader does not learn is that Phase 1 never answers "yes" (DOC-N3).
- Stalled and fenced (`sweep.md:16`, `SKILL.md:26`): a newcomer learns that a zero for either class means nothing in Phase 1 and that the report says so. That matches what the code and the report do. The two class names stay undefined (DOC-N2).
- Step 4 (`SKILL.md:26`): the instruction is concrete (mark exactly those two counts, keep the real number) and can be carried out, because both counts always exist in `summary.counts`. It does not mislead.
- Exempt reply (`SKILL.md:43` with `:35`): the reply is still counts and a path. The only additions to the plain counts are the `(not observed in Phase 1)` mark on two numbers and the pre-existing lower-bound statement from step 4. Nothing in the reply tells the coordinator what to do, so it stays free of advice. The paragraph says plainly that the mark is part of the counts and not a gloss, so a coordinator model has a stated reason to keep it. The style file does not mention the mark (DOC-N1).
- Nothing in the four passages makes a claim that the code or the report contradicts.

## Self-Audit

**(a) Reliance list: rf-qa PASS items skipped for structural re-check:**
- No `## Inherited Structural Verdict` block was supplied in the spawn prompt, so I ran standalone (no structural PASS item was skipped on that basis).
- For the 131 cycle-0 PASS ids I relied on the cycle-0 result only where I could prove the input of that check did not change (mtime older than every cycle-0 report, `cmp` exit 0, sha256 of the guide pair). That reliance is stated per row in the Checks table.

**(b) Independent semantic checks (at least one required):**
- DOC-F2 truth check: traced `fenced_evidence` and `C_STALLED` and `C_FENCED` through `src/superclaude/cli/sweep/` (Grep): assigned nowhere, so both classes stay 0; confirmed `SP24_LINE` is printed unconditionally (`report.py:392`) and `counts` always has both keys (`classify.py:961`, `report.py:665`).
- DOC-F1 truth check: read `classify.py:447-496` and `report.py:41-55`: the columns only ever hold "no" or "could not determine" and read-pointers, so "observations, not advice" is accurate.
- The six new pins plus two extra probes (M7, M8): eight mutations and a baseline on a private `/tmp` copy (baseline 121 passed; M1 to M8 each fail exactly one named test, 120 pass). The cycle-0 report's "pins exist" result was not enough; the pins had to bite.
- Style conflict check: read `pragmatic.md:22-26` against `SKILL.md:35-43` for the exempt reply (result: no exclusion breached, DOC-N1 note).
- Whole-suite re-run: 2647 passed in the four folders, 90 passed in the two severity modules, ruff check and format check clean.

**Confidence (computed):** Verified: 133/133 (131 checks + DOC-F1 + DOC-F2) | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%. "Verified" here covers two kinds of evidence: a live re-read or re-run (the whole `sweep.md` and `SKILL.md`, the gate tests, the code traces, the mutation runs, `ls`, `cmp`, `grep`) and, for many contract, routing and convention rows, proof that the file the cycle-0 check read is unchanged. Four rows rest on saved or scratch artifacts of cycle 0 and are marked "scratch": `qa-command-skill-report:C29`, `:C30`, `qa-routing-rows-report:C17`, `qa-readonly-claims-report:C14`.

**Tool engagement:** Read: 15 | Grep: 12 | Glob: 0 | Bash: 9 (three of the Bash calls were batched scripts that each closed many rows at once). Read + Grep + Glob is 27, below 133 checks, which the agent rules mark as suspect; the gap is explained by the batched `find`, `cmp`, `grep`, `pytest` and mutation runs that covered many ids per call, and I state it here rather than hide it.

**Zero-finding reasoning:** no new blocking or major finding because the fix is three added sentences and a six-test addition; each sentence was traced to code, each test was shown to fail when its sentence is removed, and the style, WC-16, the guide, DESIGN and CHANGELOG were proved unchanged.

## Verdict

Verdict: PASS
Blocking count: 0

