# Verify report, docs gate cycle 1 (rf-qa, fix_authorization: false)

**Date:** 2026-11-12
**Phase:** fix-cycle (verification of `F_0` = DOC-F1, DOC-F2 and of the 131-id cycle-0 PASS set)
**Fix cycle:** 1

Method: read the live `sweep.md` (71 lines) and `SKILL.md` (66 lines) in full, the live test file (lines 1-180 and 425-614), `pragmatic.md:15-40`, the fix log, the consolidated file and the cycle ledger. Ran `uv run pytest tests/core tests/commands tests/recommend tests/skills`, `ruff check` on the two test files and `cmp` of the guide and its plugin copy. Re-ran the six sentence-removal mutations on private `/tmp` copies (deleted by an exit trap, `CLEANUP_OK` printed). No repository file was edited by me; this report is the only file written. No live Orca command was run.

## Findings (the `F_0` list)

### DOC-F1 (MAJOR): RESOLVED

Judged by the live files, not the fix log.

- `src/superclaude/commands/sweep.md:16` now says: "The report also states, as facts to review, `Safe to close`, `Removable` and `Next inspection` (what to read next); these are observations, not advice, and the coordinator or person decides."
- `src/superclaude/skills/sc-sweep-protocol/SKILL.md:66` (last sentence of `## Boundaries`) carries the same sentence.
- The sentence is true to the code: `src/superclaude/cli/sweep/report.py:42-55` `NEXT_INSPECTION` values all begin "read ..." (what to read or check, nothing more).
- It stays beside the unchanged claims `sweep.md:57` ("It adds no recommendation and takes no action"), `sweep.md:69`, `SKILL.md:61`. The reader of the five files can now tell that the three columns are observations.
- The alternative (narrow the WC-16 and routing wording) was not applied and is outside this cycle's scope; it stays an owner decision (the fix log and the consolidated file say the same). It is not a blocking finding.
- Wording constraints: `grep -n -i -w -E 'stop|retry|release|merge|removal'` on both primitives, exit 1, no hit; `grep -nP '\x{2013}|\x{2014}'` on both primitives and the test file, exit 1, no hit. `Removable` is a different word and is not matched by `_FORBIDDEN_ADVICE` (`tests/commands/test_sweep_command.py:34-36`, applied to the skill at `:168`).
- Pins that fail on removal (my own mutation run, 121 passed on the unmutated copy):
  - M1 sentence removed from the copy of `sweep.md`: `1 failed, 120 passed`, failing test `test_sweep_command_says_report_columns_are_observations_not_advice` (test line 523).
  - M2 sentence removed from the copy of `SKILL.md`: `1 failed, 120 passed`, failing test `test_sweep_skill_boundaries_say_report_columns_are_observations_not_advice` (test line 527).

### DOC-F2 (MAJOR): RESOLVED

- `sweep.md:16`: "In Phase 1 the classes stalled (proved) and fenced are not observed, so a zero count there means nothing; the report says so."
- `SKILL.md:26` (step 4): the same sentence, then "Print each of those two counts with the mark `(not observed in Phase 1)` after the number, so the caveat travels with the counts."
- The claim is true. `fenced_evidence` is assigned nowhere under `src/superclaude/cli/sweep/` (grep finds only the reads at `classify.py:198`, `:201`, `:205`, `:220`, `:221` and the default `"unreadable"` at `models.py:87`), so stalled (needs `"absent"`, `classify.py:198`) and fenced (needs `"present"`, `classify.py:220`) cannot occur in Phase 1. "The report says so" is true: `report.py:36-39` (`SP24_LINE`: "Stalled and fenced are not observed in Phase 1; a zero count does not mean none occurred.").
- The exempt reply still follows its pinned text. `SKILL.md:35` still reads "only the summary counts and the report path are printed" (case `exempt-reply-is-counts-and-path` still passes); `SKILL.md:43` now ends with "The counts in that reply are printed as step 4 prints them, so the `(not observed in Phase 1)` mark on stalled (proved) and fenced stays; the mark is part of the counts, not a gloss of a label and not advice." The number printed stays the genuine `summary` number, so no fabricated or altered figure.
- It follows the style rule at `pragmatic.md:23`: the exempt reply "contains the summary counts and the report path, without a DONE / NEXT table, without the WHAT / WHY / RECOMMENDED ACTION wrapper, without any recommendation or action advice, and without the plain-English gloss of ordinary labels". A caveat mark on two numbers is not the table, the wrapper, advice, or a definition of a label. The same "contains" wording already allowed the lower-bound statement in step 4.
- Note (minor, not blocking, not a fix item): `pragmatic.md:23` does not itself mention the mark, so only the skill states it. The two texts agree on what is printed because the style says "contains", not "only". The fix log records this residual too. Follow-up candidate only if the owner wants the style to name the mark.
- The alternative (a WC-16 sentence about the two zeros) was not applied; it stays an owner decision, not a blocking finding.
- Pins that fail on removal (my own mutation run):
  - M3 sentence removed from the copy of `sweep.md`: `1 failed, 120 passed`, failing test `test_sweep_command_says_phase1_stalled_and_fenced_zero_means_nothing` (test line 531).
  - M4 sentence removed from step 4 of the copy of `SKILL.md`: `1 failed, 120 passed`, failing test `test_sweep_skill_step4_says_phase1_stalled_and_fenced_zero_means_nothing` (test line 535).
  - M5 the "Print each of those two counts with the mark" sentence removed: `1 failed, 120 passed`, failing test `test_sweep_skill_step4_prints_the_phase1_mark_with_the_counts` (test line 539).
  - M6 the exempt-reply sentence removed: `1 failed, 120 passed`, failing test `test_sweep_exempt_reply_keeps_the_phase1_mark_on_the_counts` (test line 543).

### New findings

None. No new BLOCKING or MAJOR finding. The two new sentences and four pins introduce no wording-constraint breach and no contradiction with a pinned phrase (all 121 cases pass).

## Commands and evidence behind the Checks table

| # | Command | Result |
|---|---|---|
| 1 | `uv run pytest tests/core tests/commands tests/recommend tests/skills` | `2647 passed in 55.95s` (exit 0) |
| 2 | `uv run ruff check tests/core/test_how_we_work_routing_table.py tests/commands/test_sweep_command.py` | `All checks passed!` |
| 3 | `cmp src/superclaude/core/HOW-WE-WORK.md plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md` | exit 0, `CMP_OK` |
| 4 | `grep -n -i -w -E 'stop\|retry\|release\|merge\|removal'` on `sweep.md` and `SKILL.md` | exit 1, no hit |
| 5 | `grep -nP '\x{2013}\|\x{2014}'` on `sweep.md`, `SKILL.md`, `test_sweep_command.py` | exit 1, no hit |
| 6 | `grep -rn 'src/superclaude' sweep.md SKILL.md` | exit 1, no hit |
| 7 | `grep -nP '[^\x00-\x7F]\|TODO\|TBD\|FIXME'` on the three subject files | exit 1, no hit |
| 8 | Mutations M1 to M6 on private `/tmp` copies (a baseline copy gave `121 passed`) | each gave `1 failed, 120 passed`, the failing test is the one named under DOC-F1 and DOC-F2; copy folder deleted (`CLEANUP_OK`) |
| 9 | `grep -rn 'chat-summary\|sc-sweep-protocol' src/superclaude/cli/sweep` | no hit |
| 10 | `~/.claude/output-styles/pragmatic.md` (installed style): `grep -c chat-summary` / `grep -c 'No exceptions'` | `0` / `1` (installed copy untouched) |
| 11 | `git diff --numstat -- src/superclaude/output-styles/pragmatic.md` | `11 7` (bounded style diff unchanged from the cycle-0 figure) |
| 12 | `git status --short` | `sweep.md`, `SKILL.md` and `test_sweep_command.py` are untracked (so `git diff` shows nothing for them); the two severity modules and every other file named in the checks are not in the modified list except those the work itself edits |

Wording constraint of the command and skill tests: every new sentence is free of the words stop, retry, release, merge and removal and of the em dash (rows 4 and 5). `Removable` is not matched by the whole-word regex. The six new tests (`tests/commands/test_sweep_command.py:523-544`, case count 115 to 121 confirmed by the run) each have a pin that fails when its sentence is removed (rows 8, M1 to M6). The sentence "Print each of those two counts with the mark ..." and the exempt-reply sentence are the only places the mark text appears in step 4 and in the exempt-reply part, so removal is caught.

Limits stated honestly:

- `sweep.md`, `SKILL.md` and the test file are untracked, so `git diff` cannot show the fix. I judged them by reading the live files and by the tests. `SKILL.md` line numbers 1-25, 27-42 and 44-65 did not move (lines 26 and 43 grew; line 66 is new). `sweep.md` lines after 15 moved by 2 (new paragraph at 16, blank at 17).
- I did not recompute the 71 protected-file hashes (the baseline was taken by the executor before the fix agent ran and I did not rely on it). For each cycle-0 check about a protected file I re-read the cited content where the check quotes it, or confirmed the claim through a passing test, `cmp`, or a grep (rows 1 to 11). A check about a saved artifact or scratch run of the cycle-0 agents (for example M11 to M22 mutations, `/tmp` copies, `git diff` readings) cannot be re-run; for those the table says "not re-run" and confirms that nothing the check relied on was changed by the fix (the fix touched only the five files named in the fix log, none of which those checks relied on except through moved line numbers or counts).
- Counts that moved: the test total (115 to 121), the four-folder total (2641 to 2647), `sweep.md` line numbers (+2 after line 15). Checks that quote these are PASS because their claim still holds in substance.

## Checks

131 rows, one per id of the cycle-0 PASS set. The first word of each result cell is the verdict. "Moved" means a line number or count quoted by the cycle-0 check changed because of the fix; the claim itself still holds. Evidence tags: T = the full test run (2647 passed, row 1 above); G = the grep rows 4 to 7; R = I re-read the live text; U = the cited file is not among the five the fix edited and its quoted content was re-read or is covered by a passing test or `cmp`; N = a saved artifact or scratch run that cannot be re-run (confirmed that nothing it relied on was changed by the fix).

| Check id | Result |
|---|---|
| qa-primitive-path-report:C1 | PASS (item 13.9). R, G: `sweep.md` now 71 lines, no `src/superclaude/` path (grep exit 1). |
| qa-primitive-path-report:C2 | PASS (item 13.9). R, G: `SKILL.md` now 66 lines, no `src/superclaude/` path (grep exit 1). |
| qa-primitive-path-report:C3 | PASS (item 13.9). U: `git diff -U0` of `WORKER-CONTRACT.md` shows hunks at lines 23 and 275-278 only; no added content line holds `src/superclaude` (the two grep hits are the `+++ b/src/superclaude/core/...` diff headers). |
| qa-primitive-path-report:C4 | PASS (item 13.9). U: the guide diff holds only the hunks at lines 334 and 405; `cmp` of the guide and its plugin copy exit 0. |
| qa-primitive-path-report:C5 | PASS (item 13.9). R: `sweep.md:51` installed path first, `:55` project copy second, introduced by "When a project checkout holds its own copy" (moved +2). |
| qa-primitive-path-report:C6 | PASS (item 13.9). R: `SKILL.md:15` names `~/.claude/commands/sc/sweep.md` first and the project `.claude/commands/sc/sweep.md` second (line unchanged). |
| qa-primitive-path-report:C7 | PASS (item 13.9). U/R: core-doc references in both primitives are `~/.claude/WORKER-CONTRACT.md` (`sweep.md:18`, `:22`); the fix added no new path. |
| qa-primitive-path-report:C8 | PASS (item 13.9). R: `SKILL.md:33` still names `~/.claude/output-styles/pragmatic.md` as an "installed as" statement; `SKILL.md:43` and `:66` added no path. |
| qa-primitive-path-report:C9 | PASS (item 13.9). R: both primitives reach package behaviour only through `superclaude sweep run` (`SKILL.md:15`, `:23`, `:24`); new sentences add no package path. |
| qa-primitive-path-report:C10 | PASS (item 13.9). U: `cmp` of the guide and plugin copy exit 0; no sweep primitive is mirrored under `plugins/` with a `src/` path (the fix touched no plugin file). |
| qa-primitive-path-report:C11 | PASS (item 13.9). T: related tests pass; `test_sweep_no_src_superclaude_path` (`test_sweep_command.py:162-164`) still pins the rule; count moved (1187 to the new totals). |
| qa-command-skill-report:C1 | PASS (item 13.10). R: frontmatter `sweep.md:2,3,8,9` unchanged; `argument-hint` equals the string at DESIGN `orchestrator-mode.md:655`. |
| qa-command-skill-report:C2 | PASS (item 13.10). R: headings title, Triggers (`:20`), Usage (`:24`), Options (`:33`), Activation (`:44`), Boundaries (`:59`) in order; the new paragraph is under the title, so no heading changed (lines moved +2). |
| qa-command-skill-report:C3 | PASS (item 13.10). R: Activation block `sweep.md:44-49`: MANDATORY, `> Skill sc:sweep-protocol`, "Pass the user's flags unchanged", "Do NOT proceed using only this command file" (moved +2). |
| qa-command-skill-report:C4 | PASS (item 13.10). R: `sweep.md:51` and `:55` name the two surfaces; `:57` says skills read `~/.claude/` first (moved +2). |
| qa-command-skill-report:C5 | PASS (item 13.10). R: first sentence of `sweep.md:22` equals the OQ-3 addendum text (grep of the full sentence in `OQ-3-addendum-wc16-wait-timeout-decision.md` finds it); "Nothing starts it automatically." follows (moved from `:20`). |
| qa-command-skill-report:C6 | PASS (item 13.10). R, T: no `## Unattended mode` and no `--unattended` in `sweep.md`; never-as-worker named at `sweep.md:18` and `:42` (moved +2); `WORKER-CONTRACT.md:23` lists `/sc:sweep`; `test_sweep_command_has_no_unattended_mode` passes. |
| qa-command-skill-report:C7 | PASS (item 13.10). R: `SKILL.md:4` unchanged and equals the test literal `_SKILL_TOOLS` (`test_sweep_command.py:30-33`). |
| qa-command-skill-report:C8 | PASS (item 13.10). R: steps 1-5 at `SKILL.md:23-27` in order, timeout 120000 ms on steps 1 and 2, fallback only on "command not found", `--frozen --no-sync` literal, no third run; step 4 grew by two sentences but its other content is unchanged. |
| qa-command-skill-report:C9 | PASS (item 13.10). R: step 3 takes only `report_path` and `summary`; step 4 still prints `total`, `visible`, `historical`, `bound_reached`, per-class `counts`, `report_path`; the added mark is text after two numbers, not a new key. |
| qa-command-skill-report:C10 | PASS (item 13.10). R: `SKILL.md:27` unchanged (stderr as it came, run ends, ordinary format, no summary or path). |
| qa-command-skill-report:C11 | PASS (item 13.10). R, G: `SKILL.md:55-64` and `sweep.md:59-70` recommend nothing and add no tool; the two new sentences say the report columns are observations, not advice (`sweep.md:16`, `SKILL.md:66`). Moved +2 in `sweep.md`. |
| qa-command-skill-report:C12 | PASS (item 13.10). G: no `src/superclaude/` string in either primitive (grep exit 1). |
| qa-command-skill-report:C13 | PASS (item 13.10). G: no stop, retry, release, merge or removal word in either primitive after the fix (grep exit 1). |
| qa-command-skill-report:C14 | PASS (item 13.10). R: the Options table (`sweep.md:35-40`, moved +2) is unchanged; the CLI sources it quotes are unchanged (`src/superclaude/cli/sweep/` has no edit by the fix). |
| qa-command-skill-report:C15 | PASS (item 13.10). T: the DESIGN 7.6 test bullet groups (two literals, two Activation paths, PATH-first, command-not-found, `--no-sync`, 120000, no Unattended heading, no `src/superclaude/`, no advice words) are at `test_sweep_command.py:106-168`; no existing pin was removed (121 = 115 + 6 new). |
| qa-command-skill-report:C17 | PASS (item 13.10). R, T: the seven table-mandate sites in `pragmatic.md` and the tests `test_style_*` and `_SIX_QUALIFIED_SITES` (`test_sweep_command.py:552-614`) pass; `pragmatic.md` numstat `11 7` (unchanged). |
| qa-command-skill-report:C18 | PASS (item 13.10). U: `git diff --numstat` of `pragmatic.md` is `11 7`, the cycle-0 figure; the fix log lists it as unedited. |
| qa-command-skill-report:C19 | PASS (item 13.10). R: `pragmatic.md:23-24` against `SKILL.md:35-45`: the same explicit-assignment rule, five success conditions and final-reply-only exemption; the added `SKILL.md:43` sentence adds the caveat mark to the counts and changes none of them (see DOC-F2 note). |
| qa-command-skill-report:C20 | PASS (item 13.10). T: positive-case pins (`test_sweep_command.py:183-242`, `:304-322`) still pass in both files. |
| qa-command-skill-report:C21 | PASS (item 13.10). T: exclusion pins (`:275` onward) still pass in both files. |
| qa-command-skill-report:C22 | PASS (item 13.10). R, T: `SKILL.md:27` and `:29` unchanged; the pins at `:366-373` and `:445-472` pass. |
| qa-command-skill-report:C25 | PASS (item 13.10). R: tool lists unchanged (`SKILL.md:4`, `sweep.md:9`); scope clause at `SKILL.md:51` and `pragmatic.md:26` present; installed `~/.claude/output-styles/pragmatic.md` still has 0 `chat-summary` matches and still has "No exceptions". |
| qa-command-skill-report:C26 | PASS (item 13.10). G: `grep -rn 'chat-summary\|sc-sweep-protocol' src/superclaude/cli/sweep` finds nothing; the summary keys the skill reads exist at `report.py` as before (the fix did not touch `cli/sweep/`). |
| qa-command-skill-report:C27 | PASS (item 13.10). R: the test file still imports only `re`, `Path`, `pytest` (`test_sweep_command.py:19-22`); the six new tests read `_COMMAND` and `_SKILL` only. |
| qa-command-skill-report:C28 | PASS (item 13.10). T: moved counts, 121 tests in `test_sweep_command.py` (was 115), 2647 in the four folders (was 2641), ruff clean; the two severity modules are not in `git status` (unmodified). |
| qa-command-skill-report:C29 | PASS (item 13.10). N: the 14 cycle-0 mutations M1 to M10 and M19 to M22 were on `/tmp` copies and are not re-run; the fix changed no pinned clause (all 115 earlier cases still pass inside the 121), and my M1 to M6 add six new mutations that are caught. |
| qa-command-skill-report:C30 | PASS (item 13.10). R: `test-sweep-command.txt` tail `--- exit code --- 0` and 121 `PASSED` lines; the summary states `passed 121`, `14 + 74 + 15 + 12 + 6 = 121`; its anchors C:51 and C:55 equal `sweep.md:51` and `:55`; K:4, 23, 24, 25, 27, 29, 31-51, 61, 63, 64 equal the live `SKILL.md` lines (counts and anchors moved, claims hold). I counted 15 skill-only pins in the test file. |
| qa-command-skill-report:C31 | PASS (item 13.10). U: `WORKER-CONTRACT.md:277` opens the WC-16 text ("The coordinator keeps watching ... On every coo..."), `HOW-WE-WORK.md:405` bullet present, `cmp` exit 0; none of these was edited by the fix. |
| qa-command-skill-report:C32 | PASS (item 13.10). G: no TODO, TBD, FIXME and no non-ASCII byte in `sweep.md`, `SKILL.md`, the test file (grep exit 1). |
| qa-contract-rule-report:C1 | PASS (item 13.11). U, T: WC-16 text in `WORKER-CONTRACT.md` (hunk lines 275-278) not edited by the fix; `tests/skills/test_worker_contract.py` passes in the 2647. |
| qa-contract-rule-report:C2 | PASS (item 13.11). U, R: the diff hunk is `@@ -274,0 +275,4 @@` (after the fan-in paragraph), the WC-16 body is at line 277 and `### Worked example` follows at line 279; the fix did not edit the file. |
| qa-contract-rule-report:C3 | PASS (item 13.11). U: no lock sentence added (the diff adds 4 lines at 275-278 and one change at line 23). |
| qa-contract-rule-report:C4 | PASS (item 13.11). U: the diff has no hunk at lines 110 or 151. |
| qa-contract-rule-report:C5 | PASS (item 13.11). U: the diff has exactly two hunks (line 23, lines 275-278). |
| qa-contract-rule-report:C6 | PASS (item 13.11). R: line 23 lists `/sc:sweep` in the never-as-worker list; hunk is `@@ -23 +23 @@`, one line. |
| qa-contract-rule-report:C7 | PASS (item 13.11). T: `RULE_PHRASES["WC-16"]` pin test passes; `tests/skills/test_worker_contract.py` is not in the fix log's edited files. |
| qa-contract-rule-report:C8 | PASS (item 13.11). T: `NEVER_AS_WORKER` pin passes. |
| qa-contract-rule-report:C9 | PASS (item 13.11). T: renamed test passes. |
| qa-contract-rule-report:C10 | PASS (item 13.11). T: the `"sweep" not in UNATTENDED_COMMANDS` assertion passes. |
| qa-contract-rule-report:C11 | PASS (item 13.11). R, T: the never-as-worker phrase pin matches the live line 23; passes. |
| qa-contract-rule-report:C12 | PASS (item 13.11). U: the fix log lists `tests/skills/` as not touched; I did not recount the five pin edits, and nothing the fix edited is in that module. |
| qa-contract-rule-report:C13 | PASS (item 13.11). T: the test module's key checks pass; the fix did not edit it. |
| qa-contract-rule-report:C14 | PASS (item 13.11). T: `UNATTENDED_EXPECT` test passes; not edited. |
| qa-contract-rule-report:C15 | PASS (item 13.11). U: the developer guide diff is one changed line (`git diff --numstat` `1 1`); not edited by the fix. |
| qa-contract-rule-report:C16 | PASS (item 13.11). T: 2647 passed, ruff clean (moved from 2641). |
| qa-contract-rule-report:C17 | PASS (item 13.11). U: the WC-16 claims about sweep (read-only, no heartbeat update, no `--agent-wait`) agree with the unchanged CLI; the new `sweep.md` and `SKILL.md` sentences add nothing about WC-16. |
| qa-contract-rule-report:C18 | PASS (item 13.11). R, U: the guide bullet at `HOW-WE-WORK.md:405` and WC-16 are present; `cmp` exit 0. |
| qa-contract-rule-report:C19 | PASS (item 13.11). T: the negative tests for pins 1 and 2 pass; not edited. |
| qa-contract-rule-report:C20 | PASS (item 13.11). U: no count wording for the list changed; the fix touched none of it. |
| qa-routing-rows-report:C1 | PASS (item 13.12). R: `HOW-WE-WORK.md:334` holds the R1 row (`/sc:sweep` ... "Writes one dated report under `.dev/sweeps/`"). |
| qa-routing-rows-report:C2 | PASS (item 13.12). R: the R2 bullet is at `HOW-WE-WORK.md:405`; the diff hunk is `@@ -403,0 +405 @@`. |
| qa-routing-rows-report:C3 | PASS (item 13.12). R, U: the R2 bullet and WC-16 are unchanged and agree; the new sentences in the primitives do not touch cadence. |
| qa-routing-rows-report:C5 | PASS (item 13.12). U: `cmp` of the guide and plugin copy exit 0. |
| qa-routing-rows-report:C6 | PASS (item 13.12). T: `tests/commands/test_routing_plugin_parity.py` passes. |
| qa-routing-rows-report:C7 | PASS (item 13.12). T: `_OTHER_COMMANDS` membership test passes (`tests/core/test_how_we_work_routing_table.py`, 1 added line). |
| qa-routing-rows-report:C8 | PASS (item 13.12). T: `tests/recommend/test_routing_refresh.py` passes (2 changed lines). |
| qa-routing-rows-report:C9 | PASS (item 13.12). U: `docs/user-guide/commands.md` diff is one added line (`git diff --stat`); not edited by the fix. |
| qa-routing-rows-report:C10 | PASS (item 13.12). U, T: R7 list matches `WORKER-CONTRACT.md:23`; the guide-list test passes. |
| qa-routing-rows-report:C11 | PASS (item 13.12). U: CHANGELOG diff is 10 added lines (`### sweep: ...`, `#### Added (sweep)`); the fix did not edit it. |
| qa-routing-rows-report:C12 | PASS (item 13.12). R: the guide diff hunks are only at lines 334 and 405 (`git diff -U0`); the level table is untouched. |
| qa-routing-rows-report:C13 | PASS (item 13.12). U: the guide diff deletes no line (hunks `@@ -333,0 +334 @@` and `@@ -403,0 +405 @@` are pure additions). The cycle-0 check also counted the R5 set line and the R7 list line in the test and contract files; those are unedited by the fix. |
| qa-routing-rows-report:C14 | PASS (item 13.12). G: the lines added to `docs/user-guide/commands.md` hold none of the five words (whole-word grep count 0); the R1 row text at `HOW-WE-WORK.md:334` as read above holds none; the sweep primitives also hold none. |
| qa-routing-rows-report:C15 | PASS (item 13.12). U: `git status` shows no `.claude/` path modified for this work and no `WC-14` added; the CHANGELOG diff and `.gitignore` diff (2 added lines) are as before. |
| qa-routing-rows-report:C16 | PASS (item 13.12). T: moved counts, all four test folders pass (2647), `test_sweep_command.py` 121 passed, ruff clean. |
| qa-routing-rows-report:C17 | PASS (item 13.12). N: the mutation runs of the cycle-0 agent on `/tmp` copies are not re-run; the fix touched none of the files those mutations changed (the guide, plugin copy, the two test modules). |
| qa-routing-rows-report:C18 | PASS (item 13.12). R: `pragmatic.md:22` carries the scoped sweep exception, "No exceptions" is gone from it (`test_style_old_unqualified_table_sentence_is_gone` passes), and `SKILL.md` and `sweep.md` stay consistent with a summary-only reply. |
| qa-routing-rows-report:C19 | PASS (item 13.12). U: `.gitignore:256` still reads `.dev/sweeps/`; `git diff --stat` shows `.gitignore` 2 added lines; `.dev/tasks/` not ignored (unchanged). |
| qa-readonly-claims-report:C1 | PASS (item 13.13). U/R: code read-only claims about `probes.py` and `commands.py` are unchanged (the fix did not touch `cli/sweep/`); the two new sentences say the report columns are observations, which agrees. |
| qa-readonly-claims-report:C2 | PASS (item 13.13). R: "the report is the one file it adds" at `sweep.md:14` is unchanged; `commands.py:_publish` untouched. |
| qa-readonly-claims-report:C3 | PASS (item 13.13). R: `sweep.md:9` `allowed-tools: Skill` equals DESIGN 7.6. |
| qa-readonly-claims-report:C4 | PASS (item 13.13). R: `SKILL.md:4` equals the DESIGN 7.6 literal and the test constant. |
| qa-readonly-claims-report:C5 | PASS (item 13.13). R: skill steps `SKILL.md:23-27` match DESIGN 7.6 steps 1 to 5; step 4's two added sentences do not change what is relayed. |
| qa-readonly-claims-report:C6 | PASS (item 13.13). G, R: no stop, retry, release, merge, removal in either primitive; the new text says the columns are not advice. |
| qa-readonly-claims-report:C7 | PASS (item 13.13). R: `report.py:42-55` `NEXT_INSPECTION` values all start "read ...", so "observations, not advice" in the new sentences is true; "recommends nothing" still holds. |
| qa-readonly-claims-report:C8 | PASS (item 13.13). U: R1 (`HOW-WE-WORK.md:334`), R6, R7, R8 (CHANGELOG), `.gitignore:256` are unedited by the fix; `cmp` exit 0. |
| qa-readonly-claims-report:C9 | PASS (item 13.13). U: the R2 bullet at `HOW-WE-WORK.md:405` is unedited. |
| qa-readonly-claims-report:C10 | PASS (item 13.13). U: WC-16 at `WORKER-CONTRACT.md:277` unedited; `sweep.md:22` still carries the 5-minute cap and the WC-16 pointer (moved from `:20`). |
| qa-readonly-claims-report:C11 | PASS (item 13.13). R, U: `sweep.md:18` and `:70` (moved) say a worker never runs it; `sweep.md:42` says there is no worker mode; `WORKER-CONTRACT.md:23` lists `/sc:sweep`. |
| qa-readonly-claims-report:C12 | PASS (item 13.13). R: the style exception (`pragmatic.md:22-26`) and the skill's `## Final reply` state the same conditions; the added mark sentence is a chat-presentation caveat and adds no advice, tool, write or JSON change. |
| qa-readonly-claims-report:C13 | PASS (item 13.13). R: option and flag claims at `sweep.md:35-40` (moved +2) are unchanged and the CLI sources are unedited. |
| qa-readonly-claims-report:C14 | PASS (item 13.13). T, N: the phase validation records are not edited by the fix; my own run reproduces their PASS facts (tests pass, ruff clean, no `src/superclaude` hit). |
| qa-reader-clarity-report:C2 | PASS (item 13.14). R: flags, defaults, limits at `sweep.md:35-40` unchanged against the unedited CLI (note RC-9, minor, untouched). |
| qa-reader-clarity-report:C4 | PASS (item 13.14). R: "the report is the one file it adds" unchanged (note RC-10, minor, untouched). |
| qa-reader-clarity-report:C5 | PASS (item 13.14). R: steps 1-5 unchanged in exit codes and JSON keys; the last report line `Report complete` still named at `SKILL.md:25` (note RC-11, minor, untouched). |
| qa-reader-clarity-report:C6 | PASS (item 13.14). R: step 4 prints the same fields; the new text now explains the two Phase-1 counts; `visible`, `historical` and `bound_reached` are still unglossed (note RC-6, minor, untouched). |
| qa-reader-clarity-report:C7 | PASS (item 13.14). R: `SKILL.md:31-51` against `pragmatic.md:22-26`; "person-run exclusion" at `SKILL.md:45` is as before (note RC-7, minor, untouched). |
| qa-reader-clarity-report:C8 | PASS (item 13.14). R: command, skill and contract still agree on "coordinator or person, never worker" (`sweep.md:18`, `:42`; `SKILL.md:15`; `WORKER-CONTRACT.md:23`). |
| qa-reader-clarity-report:C9 | PASS (item 13.14). U: WC-16 text unedited by the fix (notes RC-3, RC-4, RC-5, minor, untouched). |
| qa-reader-clarity-report:C11 | PASS (item 13.14). U: routing rows, R2 bullet, plugin mirror, user-guide row, developer-guide list are unedited and `cmp` exit 0 (notes RC-8, RC-11, minor, untouched). |
| qa-reader-clarity-report:C12 | PASS (item 13.14). U: CHANGELOG entry and `.gitignore:256` unedited (note RC-10, minor, untouched). |
| qa-reader-clarity-report:C13 | PASS (item 13.14). T: moved counts, the 442 and 742 subsets are covered by the new run of 2647 passed. |
| qa-coordinator-cadence-report:C1 | PASS (item 13.15). U: WC-16 cadence, `WORKER-CONTRACT.md:277` and line 110, unedited by the fix. |
| qa-coordinator-cadence-report:C2 | PASS (item 13.15). U: WC-16 trigger "wake or wait timeout" and line 110 unedited. |
| qa-coordinator-cadence-report:C3 | PASS (item 13.15). R: `sweep.md:22` (moved from `:20`) carries "at most once every 5 minutes (WC-16 in `~/.claude/WORKER-CONTRACT.md`)"; the cap attaches to the coordinator. |
| qa-coordinator-cadence-report:C4 | PASS (item 13.15). U: WC-16 additive wording and line 110 unedited. |
| qa-coordinator-cadence-report:C5 | PASS (item 13.15). R: `HOW-WE-WORK.md:405` states the 5-minute cap and "beside" the sweep; unedited. |
| qa-coordinator-cadence-report:C6 | PASS (item 13.15). U: R2 bullet byte-identical to DESIGN row R2 and the plugin copy (`cmp` exit 0); unedited by the fix. |
| qa-coordinator-cadence-report:C8 | PASS (item 13.15). U: contract line 110 and WC-16 unedited; the CLI allowlist unedited. |
| qa-coordinator-cadence-report:C9 | PASS (item 13.15). R: no other primitive line states a different cadence; the two new sentences in `sweep.md:16` and `SKILL.md:26,43,66` say nothing about cadence. |
| qa-coordinator-cadence-report:C10 | PASS (item 13.15). R: `SKILL.md:64` still forbids scheduling ("or schedule anything"); WC-16's "not a scheduler" agrees. |
| qa-coordinator-cadence-report:C13 | PASS (item 13.15). T: moved count, the four named modules pass inside the 2647. |
| qa-conventions-report:C1 | PASS (item 13.16). R: `sweep.md:1-10` frontmatter keys and order unchanged. |
| qa-conventions-report:C2 | PASS (item 13.16). R: title, Triggers, Usage, Options, Activation, Boundaries with `**Will:**` and `**Will Not:**` unchanged in order; the new paragraph sits under the title. |
| qa-conventions-report:C3 | PASS (item 13.16). R: Options table with `--window <N>h\|<N>d` and "There is no worker mode and no flag for one." (`sweep.md:35-42`) unchanged. |
| qa-conventions-report:C5 | PASS (item 13.16). R: `SKILL.md:1-11` frontmatter and extended-metadata comment unchanged. |
| qa-conventions-report:C6 | PASS (item 13.16). R: `SKILL.md` headings Inputs, Steps, Final reply, Boundaries (with Will and Will Not) unchanged; the Boundaries section now ends with one added sentence (`SKILL.md:66`), which does not change the Will or Will Not form. |
| qa-conventions-report:C8 | PASS (item 13.16). R, T: the test file keeps the `_REPO`, `_COMMAND`, `_SKILL` constants and `test_sweep_*` names (the six new tests follow them); ruff check on the two test files passes (moved: four-file count not re-run, two-file ruff re-run). |
| qa-conventions-report:C10 | PASS (item 13.16). R: `WORKER-CONTRACT.md:23` lists `/sc:sweep` in alphabetical position on one line; unedited by the fix. |
| qa-conventions-report:C11 | PASS (item 13.16). U: WC-16 heading and position unedited (hunk lines 275-278). |
| qa-conventions-report:C12 | PASS (item 13.16). U, T: `test_worker_contract.py` unedited by the fix; passes. |
| qa-conventions-report:C13 | PASS (item 13.16). U: the guide row and bullet unedited; `cmp` exit 0. |
| qa-conventions-report:C14 | PASS (item 13.16). U, T: `_OTHER_COMMANDS` and `_POST_REFRESH_ADDITIONS` edits unedited; tests pass (moved count). |
| qa-conventions-report:C15 | PASS (item 13.16). U: `docs/user-guide/commands.md` row unedited. |
| qa-conventions-report:C18 | PASS (item 13.16). U: CHANGELOG heading form unedited; the fix log says `CHANGELOG.md` was not edited. |
| qa-conventions-report:C20 | PASS (item 13.16). U: `.gitignore:255-256` unedited (`.dev/sweeps/` at line 256). |
| qa-conventions-report:C21 | PASS (item 13.16). U, T: `pragmatic.md` unedited (numstat `11 7`); the six qualified sites and the "four sub-bullets" statement are pinned by tests that pass. |
| qa-conventions-report:C22 | PASS (item 13.16). R: the four-part titles of `## Final reply` match the style's four sub-bullets; the skill names `~/.claude/output-styles/pragmatic.md`. |
| qa-conventions-report:C23 | PASS (item 13.16). G: no `src/superclaude/` path and no en or em dash in `sweep.md`, `SKILL.md`, the test file (greps exit 1). |
| qa-conventions-report:C24 | PASS (item 13.16). T: moved counts, `test_sweep_command.py` 121 passed (was 115), four folders 2647 passed (the five-file run of 1189 is covered); `ruff check src/superclaude/cli/main.py` not re-run (`main.py` is not among the fix's files). |
| qa-conventions-report:C25 | PASS (item 13.16). U: `git status --short` shows no `.claude/` path modified or staged for sweep. |

## Summary

- `F_0` findings: DOC-F1 RESOLVED, DOC-F2 RESOLVED. `|F_1|` = 0 (blocking and MAJOR open findings).
- Cycle-0 PASS set: 131 of 131 ids still PASS; none regressed.
- New BLOCKING or MAJOR findings: none.
- Notes (minor, no fix pass): `pragmatic.md:23` does not name the `(not observed in Phase 1)` mark, only the skill does (follow-up candidate if the owner wants the style to say so); "(proved)" is still not defined in `sweep.md` (already outside the DOC-F2 fix text); the minor findings DOC-F3 to DOC-F32 are unchanged and not rechecked.
- The WC-16 alternatives for DOC-F1 and DOC-F2 stay with the owner (owner-approved text); they are not open blocking findings.
- Confidence: Verified: 133 of 133 (131 check ids, DOC-F1, DOC-F2) | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%. The checks tagged U or N rest on the five-file scope in the fix log plus re-read content, not on a recomputed hash baseline (stated above).
- Tool engagement: Read: 10 | Grep: 3 | Glob: 0 | Bash: 10 (tests, greps, six mutation runs on private /tmp copies, all deleted).

Verdict: PASS
Blocking count: 0

