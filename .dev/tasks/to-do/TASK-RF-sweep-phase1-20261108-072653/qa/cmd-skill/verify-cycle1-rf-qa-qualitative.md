# QA Report - Verify cycle 1, rf-qa-qualitative (cmd-skill gate)

**Date:** 2026-11-12
**Phase:** fix-cycle verification (cycle 1 of at most 2), task T255
**fix_authorization:** false (this report is the only file written; every experiment ran on a private /tmp copy that was deleted)
**Subject:** F_0 = CMD-F1, CMD-F2, CMD-F3, CMD-F4 and the 108-id cycle-0 PASS set, against the files on disk now

## Method and what changed

- Inputs read from disk now in chunks of at most 150 lines: the consolidated cycle-0 file, `fix-log-cycle1.md`, `cycle-ledger.md`, all seven `qa-*-report.md`, live `SKILL.md` (64 lines), `sweep.md` (68), the style `pragmatic.md` lines 15-45, `tests/commands/test_sweep_command.py` (599 lines, all of it), `test-sweep-command-summary.md`, `phase11-validation.md` and the tails and cites of `test-sweep-command.txt` and `step-1.15-checks.md`. The fix log was used only to know what to look at; each F_0 verdict below rests on the live files.
- Change set proved from disk: `find ... -newer consolidated-findings-cycle0.md` lists exactly `SKILL.md`, `test_sweep_command.py`, the two result files named by the fix log, the plan/ledger/prompt files and the fix log itself. `sweep.md`, `pragmatic.md`, `tests/recommend/test_routing_refresh.py`, `src/superclaude/cli/sweep/`, `docs/` and `plugins/` are not newer. `git diff -U0 -- pragmatic.md` still has 7 hunks, with the six `Except for the sweep chat-summary exception above,` qualifiers at lines 57, 62, 64, 73, 84, 94. `git diff -- tests/recommend/test_routing_refresh.py` is still the one added `"sweep"` string. `git status --short tests/skills` is empty.
- Runs (all from the repository; no source or test file was written): `uv run pytest tests/commands tests/recommend tests/skills/test_review_severity_rule.py tests/skills/test_implement_severity_static.py` gave `723 passed`; `tests/commands tests/recommend` alone `633 passed`; the sweep file `115 passed`; `tests/recommend/test_routing_refresh.py` `248 passed`; the two severity modules `90 passed`. `ruff check` printed `All checks passed!` and `ruff format --check` printed `2 files already formatted`. `grep -rn 'src/superclaude'` on `sweep.md` and the skill folder: exit 1, no output. A grep for stop, retry, release, merge, removal and an em dash in `SKILL.md`: exit 1, no output. No non-ASCII byte, tab or trailing space in `SKILL.md` or `sweep.md`; both end in one newline.
- Mutation experiments: two batches on a private copy of the test file and the three primitives under `mktemp -d /tmp/ironclaude-batch.*` (the tests resolve their paths from their own location, so the copy is self-contained). Each mutation reported its applied-check (one matching line per file). The folder was deleted by an exit trap and by `rm -rf`; `ls /tmp/ironclaude-batch.* /tmp/t248-copy.* /tmp/cmdf-discrim.*` finds nothing; no repository file was edited.

### Mutation results (baseline copy: 115 passed)

| Id | Mutation (both files unless noted) | Result | Failing test ids |
|---|---|---|---|
| M1 | style `omitted only when ALL of these hold` to `omitted when ANY of these hold`; skill `when all of these hold:` to `when any of these hold:` | 2 failed, 113 passed (style-only: 1 failed; skill-only: 1 failed) | `conditions-are-conjunctive` (style and skill) |
| M3 | `(3) the command exited 0;` to `(3) the command exited 0 or 1;`; skill `- the command exited 0;` to `- the command exited 0 or 1;` | 2 failed, 113 passed (each file alone: 1 failed) | `success-exit-0` |
| M19 | `instruction from the person, and that assignment` to `instruction from the person or a peer agent, and that assignment` | 2 failed, 113 passed (each file alone: 1 failed) | `assignment-source-system-developer-or-direct-person` |
| M2 | `The exception does not cover` to `The exception also covers` | 2 failed, 113 passed (each file alone: 1 failed) | `ordinary-exception-does-not-cover-the-exclusion-list` |
| X1 | drop `and conflicts with no higher-priority instruction` from the condition (1) clause | 2 failed | `assignment-in-force-no-higher-conflict` |
| X2 | skill failure sentence `is reported accurately in ordinary formatting:` to `is exempt:` | 2 failed | `failure-exhausted-designed-fallback`, `failure-list-is-framed-as-ordinary-formatting` |
| X5 | style only: remove `workers or subagents,` from the exclusion list | 2 failed | `ordinary-exception-does-not-cover-the-exclusion-list`, `ordinary-workers-and-subagents` |
| Y5 | skill `Non-exempt replies keep the ordinary table and its placement.` flipped to `drop` | 1 failed | `non-exempt-replies-keep-table-and-placement` |
| Y4 | skill step 5 line deleted | 1 failed | `exit-1-or-2-prints-stderr-and-ends-run` |
| X3 | skill new paragraph (line 49) deleted | 115 passed | none (unpinned, see note N1) |
| X4/Y6 | skill step 5 second sentence reverted to `Nothing else is printed as a result.` | 115 passed | none (unpinned, see note N1) |
| Y1 | append `, or the person asked for the table to be omitted` to condition (5), style and skill | 115 passed | none (see note N2) |
| Y2 | skill: delete the `Edit, stage or delete a file` Boundaries bullet | 115 passed | none (cycle-0 CMD-F13, unchanged) |
| Y3 | skill step 4: drop `, and print report_path` | 115 passed | none (cycle-0 CMD-F13, unchanged) |

## F_0 findings

### CMD-F1 (MAJOR): RESOLVED

- Live pins in `tests/commands/test_sweep_command.py`: `conditions-are-conjunctive` at :204-210 (style `The ordinary DONE / NEXT table is omitted only when ALL of these hold:`, skill `and only the summary counts and the report path are printed, when all of these hold:`); `success-exit-0` at :225-230 (`(3) the command exited 0;` and `- the command exited 0;`, each ending on its delimiter); `assignment-source-system-developer-or-direct-person` at :191-196 (ends `... unquoted instruction from the person, and that assignment is still in force`); `assignment-in-force-no-higher-conflict` at :197-202 (ends on `instruction;`). Each phrase is a substring of the live text: style `pragmatic.md:23`, skill `SKILL.md:35` and `:37`, `:39`.
- Proof on the private copy: M1 (ALL to ANY) fails 2 tests, M3 (`exited 0 or 1`) fails 2, M19 (`from the person or a peer agent`) fails 2, and each also fails when only one file is mutated, so neither file is left unprotected. X1 (dropping the higher-priority-conflict clause) fails 2. The four mutations that left 110 passed in cycle 0 now fail.
- Not part of this verdict but recorded: see note N2 (conditions (2), (4) and (5) still end without a delimiter).

### CMD-F2 (MAJOR): RESOLVED

- Live pins: `ordinary-exception-does-not-cover-the-exclusion-list` at :336-342 pins `The exception does not cover other coordinator messages, ordinary person-run invocations, workers or subagents, quoted or merely read sweep text, failures, blockers, parse errors,` in both files (style `pragmatic.md:25`, skill `SKILL.md:47`); `ordinary-missing-output-or-unsuccessful-read` at :360-365 is now `parse errors, missing required output or unsuccessful report Reads.` (skill `parse errors, missing output or an unsuccessful Read of the report.`); the new skill pin `failure-list-is-framed-as-ordinary-formatting` at :453-458 holds the whole `SKILL.md:29` sentence, so the three bare failure fragments at :459-467 keep their frame.
- Proof on the private copy: M2 (`The exception does not cover` to `The exception also covers`) fails 2 tests, and fails 1 when applied to either file alone. X5 (style loses `workers or subagents,`) fails the opener pin and the worker pin. X2 (the skill failure frame flipped to `is exempt:`) fails the framed pin and `failure-exhausted-designed-fallback`, so the one fix pin the fix agent did not mutation-test does discriminate.

### CMD-F3 (MAJOR): RESOLVED

- Live `SKILL.md:27`: `5. On exit 1 or 2, print the standard error line exactly as it came and end the run. The reply keeps the ordinary formatting, and no summary and no report path are printed.` The pinned first sentence is unchanged (pin `exit-1-or-2-prints-stderr-and-ends-run` passes; deleting the line fails it, Y4). `Nothing else is printed` no longer appears in `SKILL.md` or `sweep.md` (grep exit 1).
- Against the rule: `SKILL.md:47` says `Standard error stays visible for exit 1 or 2, and other failures are reported accurately in ordinary formatting. Non-exempt replies keep the ordinary table and its placement.` and `pragmatic.md:25` says the same. Step 5 now says an exit 1 or 2 reply keeps the ordinary formatting, so a coordinator reads one answer from both places: stderr text, ordinary formatting with its table, no counts, no path. The contradiction is gone. No forbidden word and no em dash was introduced (grep exit 1); the skill test file passes.
- Limit: the new second sentence has no pin (note N1). That is not a defect in the finding as filed, which asked for a text change only.

### CMD-F4 (MAJOR): RESOLVED

- Live `SKILL.md:49`: `If the output style text loaded in this session has no sweep chat-summary exception (an installed copy that was not refreshed), nothing here is exempt and every reply keeps the ordinary formatting.` It sits at the end of "Final reply", before `**Scope.**` (now :51). It gives the tie-breaker the finding asked for: against a stale style, nothing is exempt.
- The case is real on this machine: `~/.claude/output-styles/pragmatic.md` has `grep -c 'sweep chat-summary exception'` = 0 and line 22 still reads `EVERY response includes a DONE / NEXT table. No exceptions.`; the canonical `src/superclaude/output-styles/pragmatic.md:22-26` carries the exception. No HOME or installed file was touched by the fix (`pragmatic.md` is not newer than the cycle-0 consolidation).
- No pin is disturbed: the paragraph falls inside the `ordinary` part that `_skill_parts()` builds (`**What stays ordinary.**` to `**Scope.**`), and all 115 tests pass. `SKILL.md:33` and `:49` do not contradict each other (:33 says where the style is installed, :49 says what to do when the installed copy is old).

## Other findings (none BLOCKING, none MAJOR)

New BLOCKING or MAJOR findings: none. The passage re-read and the experiments produced notes only. The first two are Medium follow-up candidates (real but non-blocking weaknesses, no fix pass); the rest are MINOR.

- **N1 (Medium follow-up candidate): the two skill text fixes have no regression pin.** `tests/commands/test_sweep_command.py:445-447` pins only the first sentence of step 5; the added sentence at `SKILL.md:27` and the whole paragraph at `SKILL.md:49` are free text. Reverting step 5 to `Nothing else is printed as a result.` (X4/Y6) or deleting the stale-style paragraph (X3) still gives `115 passed`, so CMD-F3 and CMD-F4 could silently come back. A pin for each sentence would close it; the cycle-0 findings asked for text only, so this is not a failure of the fix.
- **N2 (Medium follow-up candidate): the conjunction pins stop at conditions (1) and (3).** `loaded-skill-for-actual-invocation` (:218-224), `success-stdout-parsed-for-counts-and-path` (:231-237) and `success-report-read` (:238-242) are still open-ended substrings. Appending `, or the person asked for the table to be omitted` to condition (5) in both files (Y1) still gives `115 passed`. M1, M3 and M19 are closed; an escape clause added to the end of an unpinned condition is not. Ending each of those pins on its delimiter (`(5) the report at that path was Read successfully.` and the skill `- the report at that path was Read successfully.`, plus the `;` forms for (2) and (4)) would close it.
- **N3 (MINOR): `test-sweep-command-summary.md:19` overstates the cycle-1 proof.** It says the 5 new cases were each shown to fail, but its list holds two tightened pins (`success-exit-0`, `assignment-source-...`) and omits the fifth new case, `failure-list-is-framed-as-ordinary-formatting` (the fix log admits it was not mutation-tested). The claim is true in effect (X2 above) but the sentence does not match its own list.
- **N4 (MINOR): stale pointers in two result files.** `step-1.15-checks.md:65` and `:67` (rows S1, S3) cite `SKILL.md:49` for the scope rule; it is now at `SKILL.md:51`, and line 49 holds the new paragraph. `phase11-validation.md:62` still records `718 passed` for the item 11.5 run (a dated snapshot taken before the fix); the live total is 723 and `fix-log-cycle1.md:75` and `:88` record it. Both claims were true when written; a later gate that reads either file as the final state will see a mismatch.
- **N5 (MINOR): readers' notes on the new passages.** `SKILL.md:49` is the one paragraph in "Final reply" without a bold lead-in. Step 5 says "the standard error line" (one line) although the command can print several (cycle-0 CMD-F23, unchanged). `(3) the command exited 0;` breaks if someone renumbers the style conditions, with no comment saying so. `failure-exhausted-designed-fallback` (:448-452) is now a prefix of the new framed pin, so one change fails two ids.
- **Carried from cycle 0, unchanged:** `sweep.md:16` still says `/sc:sweep` is on the never-as-worker list; `src/superclaude/core/WORKER-CONTRACT.md` has no `sc:sweep` entry (`grep -n 'sc:sweep'` finds nothing; item 12.2 is open). Cycle 0 recorded this as MINOR CMD-F5 and graded the check ids that touch it as noted forward references (CMD-F5 says it becomes BLOCKING at the final gate if item 12.2 does not land). The MINOR findings CMD-F5 to CMD-F36 were not re-checked by design.

## Passage re-read as the intended reader

- **Step 5 (`SKILL.md:27`).** A coordinator new to the project learns what an error prints: the stderr text as it came, the ordinary format, no counts, no path, and the run ends. It reads without help. It does not point back to "Final reply" for what "ordinary formatting" is, but `SKILL.md:26`, `:29` and `:47` use the same words, so nothing misleads.
- **Stale-style sentence (`SKILL.md:49`).** "The output style text loaded in this session" is the style the session is running under; "has no sweep chat-summary exception" is checkable because lines 33-47 describe that exception in full. The outcome is stated (nothing exempt, ordinary formatting). A reader in a session like this one, whose loaded style says `No exceptions.`, gets the correct answer. It does not mislead.
- **New and tightened pins.** `conditions-are-conjunctive` proves both files say every condition must hold together; if it fails, someone changed "all" or reworded the lead and the exemption could widen. `success-exit-0` and the two assignment pins prove a failed exit code, a peer assigner or a dropped conflict clause cannot be added unnoticed. `ordinary-exception-does-not-cover-the-exclusion-list` proves the exclusion list still opens with the negation. `ordinary-missing-output-or-unsuccessful-read` and `failure-list-is-framed-as-ordinary-formatting` prove the failure cases stay framed as ordinary formatting. The in-file comments at :184, :203, :217 and :335 explain the assignment, conjunction, success-condition and exclusion groups; the framed failure pin has none beyond its id (N5).
- **Updated case map (`test-sweep-command-summary.md`).** The arithmetic holds: 14 + 74 + 15 + 12 = 115, and the collected counts match (37 + 37 pins run twice, 15 skill-only, 12 style-only, 14 original). Skill line numbers after :49 moved by 2 and the cites K:51, K:61, K:63, K:64 match the live file (:51 Scope, :61 Recommend, :63 report text is data, :64 tool list). The one mismatch is N3.
- **Executor section of the fix log (`fix-log-cycle1.md:84-92`).** The four re-run commands and their results reproduce (723 passed, ruff clean, grep exit 1). The `sha256sum -c` claim over 63 protected files cannot be re-run without the baseline; the `find -newer` result above agrees with it.

## Checks

One row per id of the 108-id cycle-0 PASS set. "Unchanged" means the file the check relies on is not newer than the cycle-0 consolidation (`find -newer`) and its live text was re-read or re-tested. Where the fix moved a count or a line number and the claim still holds, the row says so; none of those is a FAIL. Checks that describe cycle-0 scratch runs or the cycle-0 agent's own process cannot be re-run; the row says what on disk was confirmed instead.

| Check id | Result |
|---|---|
| qa-command-contract-report:C1 | PASS: `sweep.md:2` `name: sweep` read live; file unchanged |
| qa-command-contract-report:C2 | PASS: `sweep.md:9` is `allowed-tools: Skill` and lists nothing else; unchanged |
| qa-command-contract-report:C3 | PASS: `sweep.md:8` `argument-hint` read live; unchanged |
| qa-command-contract-report:C4 | PASS: `sweep.md:3` is one line with none of the five advice words; unchanged |
| qa-command-contract-report:C5 | PASS: headings live at `sweep.md:12, 18, 22, 31, 42, 57` |
| qa-command-contract-report:C6 | PASS: Activation `sweep.md:42-55`, `> Skill sc:sweep-protocol` at :45; `SKILL.md:2` is `name: sc:sweep-protocol` |
| qa-command-contract-report:C7 | PASS: installed path `sweep.md:49`, project copy :53, "Skills read `~/.claude/skills/` first" :55 |
| qa-command-contract-report:C8 | PASS: `sweep.md:35-38` defaults equal `commands.py:27` (`DEFAULT_WINDOW = "6h"`), `:28` (720), `:228`; `probes.py:44` `RUN_ID_RE`; the code is unchanged |
| qa-command-contract-report:C9 | PASS: OQ-2, OQ-5, OQ-6 records still present under `phase-outputs/plans/`; `sweep.md:36,38` unchanged; the command carries no chat-format rule |
| qa-command-contract-report:C10 | PASS: window limit `commands.py:28`, run id `probes.py:44`, no-Run message `probes.py:236`; code and `sweep.md:35-38` unchanged |
| qa-command-contract-report:C11 | PASS: `test_sweep_command_has_no_unattended_mode` passes live on `sweep.md` |
| qa-command-contract-report:C12 | PASS: `grep -rn 'src/superclaude'` exit 1; `test_sweep_no_src_superclaude_path[sweep.md]` passes |
| qa-command-contract-report:C15 | PASS: `sweep.md:55` still matches the skill (`SKILL.md:15`, `:23-27`, and the no-recommendation bullet now at `:61`, moved from :59); pointer drift only |
| qa-command-contract-report:C16 | PASS: class and report claims against `models.py`, `report.py` (`:520` `Report complete` read live); the code is unchanged |
| qa-command-contract-report:C17 | PASS: Boundaries `sweep.md:57-68` read live, unchanged |
| qa-command-contract-report:C18 | PASS: `tests/commands tests/recommend` 633 passed, with the severity modules 723 passed, ruff check and format clean (counts moved by the 5 new cases, the claim "green" holds) |
| qa-command-contract-report:C20 | PASS: `git diff -- tests/recommend/test_routing_refresh.py` is still the one added `"sweep"` string at :33; DESIGN row R5 (`orchestrator-mode.md:719`) equals it; 248 passed |
| qa-command-contract-report:C21 | PASS: `test-sweep-command.txt` collected 115, 115 passed, exit 0 (regenerated by the fix), summary 14 + 74 + 15 + 12 = 115 equals the live run; `r5-routing-refresh.txt` 248 equals live; `step-1.14-checks.md` cites into `sweep.md` unchanged |
| qa-command-contract-report:C22 | PASS: 7 hunks in `git diff -U0 -- pragmatic.md`, exception at :22-26, six qualifiers at :57, 62, 64, 73, 84, 94; file unchanged |
| qa-skill-contract-report:C1 | PASS: `SKILL.md:4` unchanged and equal to `_SKILL_TOOLS`; its test passes |
| qa-skill-contract-report:C2 | PASS: five steps still at `SKILL.md:23-27` in order (step 5 reworded, same behaviour) |
| qa-skill-contract-report:C3 | PASS: 120000 ms at :23 and :24; test passes |
| qa-skill-contract-report:C4 | PASS: `:24` unchanged; fallback tests pass |
| qa-skill-contract-report:C5 | PASS: `:25` unchanged; `report.py:670` keys live |
| qa-skill-contract-report:C6 | PASS: `:25` unchanged; `report.py:520` `Report complete` |
| qa-skill-contract-report:C7 | PASS: `SKILL.md:37`, `:45` unchanged; `pragmatic.md:23-24` unchanged; pins pass |
| qa-skill-contract-report:C8 | PASS: `SKILL.md:38-43` unchanged |
| qa-skill-contract-report:C9 | PASS: `SKILL.md:45` unchanged |
| qa-skill-contract-report:C10 | PASS: exclusions at :29, :45, :47 unchanged; :27 now says ordinary formatting, which agrees with :47 and `pragmatic.md:25` (cycle-0 note F2 is CMD-F3, resolved) |
| qa-skill-contract-report:C11 | PASS: `:45` unchanged; the "not a runtime detector" scope clause now at `:51` (moved from :49); new `:49` grants no role and adds no detector |
| qa-skill-contract-report:C12 | PASS: Boundaries now `SKILL.md:53-64` (moved by 2): recommends nothing :61, edit/stage/delete ban :62, report text is data :63, tool limit :64 |
| qa-skill-contract-report:C13 | PASS: grep for stop, retry, release, merge, removal and an em dash exit 1; no non-ASCII byte; no `src/superclaude`; the two new sentences were included |
| qa-skill-contract-report:C14 | PASS: flags at `SKILL.md:19` unchanged; `commands.py` unchanged |
| qa-skill-contract-report:C15 | PASS: OQ-6 (b) exception is at `pragmatic.md:22-26` and `SKILL.md:31-51` (range grew by 2); defaults `sweep.md:33-38`, `commands.py:27` |
| qa-skill-contract-report:C16 | PASS: 633 and 723 passed, ruff clean |
| qa-skill-contract-report:C17 | PASS: evidence still matches the disk except moved counts and pointers: `test-sweep-command.txt` 115 equals live; `step-1.15-checks.md:65,67` cite `SKILL.md:49` for the scope rule, now :51; `phase11-validation.md:62` keeps the pre-fix 718 (note N4); claims true, pointers only |
| qa-skill-contract-report:C18 | PASS: `SKILL.md:1-11` frontmatter and metadata comment, :15 "No other skill calls this one", Will and Will Not blocks read live |
| qa-skill-contract-report:C19 | PASS: routing diff is the one-line `{"graph", "impact", "issue", "sweep"}` change |
| qa-skill-contract-report:C20 | PASS: cycle-0 scratch run; re-run on a new copy gives the same outcome (baseline passes, step 5 deleted fails 1, Boundaries bullet deleted passes 115, `report_path` clause dropped passes 115) |
| qa-test-coverage-report:C1 | PASS: process claim, not re-runnable; I re-read every input the check lists (command, skill, style, test file, addendum, DESIGN 7.6 and R5, result files) in chunks of at most 150 lines, and DESIGN, addendum, OQ records and the CLI code are unchanged |
| qa-test-coverage-report:C2 | PASS: tests at `test_sweep_command.py:106-112` unchanged and pass |
| qa-test-coverage-report:C3 | PASS: dual-surface tests :114-128 unchanged and pass |
| qa-test-coverage-report:C4 | PASS: PATH-first, fallback, literal and timeout tests :131-152 pass against `SKILL.md:23-24` |
| qa-test-coverage-report:C5 | PASS: :155-159 unchanged and pass |
| qa-test-coverage-report:C6 | PASS: :162-164 pass; grep exit 1 |
| qa-test-coverage-report:C7 | PASS: :167-168 pass; grep exit 1 |
| qa-test-coverage-report:C8 | PASS: routing diff one line, `orchestrator-mode.md:719` equals it, 248 passed live, `r5-routing-refresh.txt` records 248 |
| qa-test-coverage-report:C11 | PASS: `files-reports-tool-output-quotes-peers-never-establish` and `no-fabricated-summary-no-hidden-error-no-other-command` pass against `SKILL.md:29,45` and `pragmatic.md:24` |
| qa-test-coverage-report:C12 | PASS: seven table sites still pinned; 7 style hunks, six qualifiers at the six lines, qualifier tests pass |
| qa-test-coverage-report:C13 | PASS: `test_style_non_exempt_defaults_examples_and_none_row_are_kept` and the no-leak test pass |
| qa-test-coverage-report:C14 | PASS: the agreement holds at the new counts: raw 115 = summary 115 = live 115, severity 90 = live 90, 633 + 90 = 723 = live and fix log; only `phase11-validation.md:62` keeps the pre-fix 718 (note N4) |
| qa-test-coverage-report:C15 | PASS: `git status --short tests/skills` and `git diff --stat HEAD -- tests/skills` are empty |
| qa-test-coverage-report:C16 | PASS: docstring `test_sweep_command.py:13-17` read live and disclaims live adherence; summary "Static-only limits" now at `test-sweep-command-summary.md:125-127`; step-7.10 limits paragraph present near :98 |
| qa-test-coverage-report:C19 | PASS: ruff check and format --check clean on both test files |
| qa-test-coverage-report:C20 | PASS: `sweep.md:35-38` against `commands.py:27-28,228`; unchanged |

| qa-readonly-claims-report:C1 | PASS: `sweep.md:9` is `Skill` only; unchanged |
| qa-readonly-claims-report:C2 | PASS: `SKILL.md:4` unchanged; body names only the two Bash forms and Read, now at `:64` (was :62) |
| qa-readonly-claims-report:C3 | PASS: write claims at `sweep.md:14,55,66` and `SKILL.md:15`, `:62` (was :60) unchanged in meaning; `commands.py` unchanged; the "true on exit 0" caveat is cycle-0 CMD-F22, untouched |
| qa-readonly-claims-report:C4 | PASS: option table against `commands.py` and `probes.py:44`; both unchanged, `DEFAULT_WINDOW`, `MAX_WINDOW_HOURS`, `RUN_ID_RE` read live |
| qa-readonly-claims-report:C5 | PASS: OQ-2 and OQ-5 records unchanged; `sweep.md:25,33-38` and `commands.py:27` agree |
| qa-readonly-claims-report:C6 | PASS: no stop, retry, release, merge or removal word anywhere in `SKILL.md` (grep exit 1); the new `:27` and `:49` sentences add none; the only delete or schedule words are the existing bans at `:51`, `:62`, `:64` |
| qa-readonly-claims-report:C7 | PASS: read-only claim against `probes.py`; file unchanged |
| qa-readonly-claims-report:C8 | PASS: steps 1 to 4 unchanged at `SKILL.md:23-26`; step 5 changed only in what the reply looks like |
| qa-readonly-claims-report:C9 | PASS: grants no role or right: `pragmatic.md:23-25`, `SKILL.md:35-47` unchanged; new `:49` can only remove the exemption |
| qa-readonly-claims-report:C10 | PASS: scope clauses `pragmatic.md:26` and `SKILL.md:51` (moved from :49); `grep -rn 'chat-summary' src/superclaude/cli/sweep` finds nothing; the CLI is unchanged |
| qa-readonly-claims-report:C11 | PASS: success needs exit 0, parse and Read (`SKILL.md:37-41`); stderr stays visible (:27, :29, :47); no fabricated summary (:29) |
| qa-readonly-claims-report:C12 | PASS: `pragmatic.md` unchanged since cycle 0; 7 hunks vs HEAD; `test_style_old_unqualified_table_sentence_is_gone` passes |
| qa-readonly-claims-report:C13 | PASS: the old unqualified mandate is absent (that test) and live `pragmatic.md:22` holds the scoped exception |
| qa-readonly-claims-report:C14 | PASS: exception no broader than OQ-6 (b) and the addendum (`design-addendum.md:13,19,21` read live): final successful reply only, top-level coordinator assignment |
| qa-readonly-claims-report:C15 | PASS: the test file reads the real sources and states its static limit (docstring :13-16); 115 cases in the file, 633 in the repository run (counts moved by the fix) |
| qa-readonly-claims-report:C16 | PASS: routing diff adds only `"sweep"` |
| qa-readonly-claims-report:C17 | PASS: result files match the disk after the fix, except moved counts and pointers (`step-1.15-checks.md:65,67` cite :49 for the scope rule now at :51, and `phase11-validation.md` keeps 718; notes N3, N4); the claims in them are true |
| qa-readonly-claims-report:C18 | PASS: house-pattern Activation and `name: sc:sweep-protocol`; no Unattended section; no `src/superclaude/` path |
| qa-readonly-claims-report:C19 | PASS: carried from cycle 0 on the same basis (forward reference, CMD-F5); `sweep.md:16` is unchanged and `WORKER-CONTRACT.md` still has no `sc:sweep` entry, so the sentence stays ahead of its file until item 12.2 lands; flagged under "Carried from cycle 0" |
| qa-readonly-claims-report:C20 | PASS: cycle-0 mutation runs cannot be re-run; nothing they relied on changed for the command and the style, and the skill-side behaviour is re-confirmed (a `Retry` or flipped-rule edit in the skill fails, see Y5); the command and style gaps remain cycle-0 CMD-F17 |
| qa-reader-clarity-report:C1 | PASS: assignment versus invocation, labels and data claims at `SKILL.md:37`, `:45` unchanged |
| qa-reader-clarity-report:C2 | PASS: `SKILL.md:45`, `:47` unchanged |
| qa-reader-clarity-report:C5 | PASS: no undefined detector or new power; `:51` says "not a runtime detector, identity check or flag"; `:49` asks the reader only to look at the style text it was given and can only remove the exemption |
| qa-reader-clarity-report:C6 | PASS: `sweep.md:55`, `:61-67` against the reworded step 5 and the new `:49`: no contradiction |
| qa-reader-clarity-report:C8 | PASS: no claim wider than the CLI; the new step 5 wording describes only what the skill prints |
| qa-reader-clarity-report:C9 | PASS: options table against `commands.py` defaults and limits; unchanged |
| qa-reader-clarity-report:C10 | PASS: sweep file 115 passed and routing file 248 passed (363 together; cycle 0 had 358); ruff clean; routing diff one line |
| qa-reader-clarity-report:C11 | PASS: process claim, not re-runnable; this review likewise rests on live files and ran its own experiments |
| qa-conventions-report:C1 | PASS: `sweep.md:2-9` key order name, description, category, complexity, mcp-servers, personas, argument-hint, allowed-tools; unchanged |
| qa-conventions-report:C2 | PASS: `SKILL.md:1-11` frontmatter order and the extended-metadata comment read live |
| qa-conventions-report:C3 | PASS: heading order unchanged; no Unattended heading |
| qa-conventions-report:C5 | PASS: `sweep.md:57-68` bold Will and Will Not; unchanged |
| qa-conventions-report:C6 | PASS: skill H1 at `SKILL.md:13`, "Backs `/sc:sweep`" intro and "No other skill calls this one" at :15 |
| qa-conventions-report:C7 | PASS: skill closes with `## Boundaries` (now `:53`) as before |
| qa-conventions-report:C8 | PASS: `allowed-tools` syntax at `SKILL.md:4` unchanged and spec-pinned |
| qa-conventions-report:C9 | PASS: helpers `_REPO`, `_COMMAND`, `_SKILL`, `_text`, `_frontmatter`, `_section` read live at `test_sweep_command.py:24-69`; the fix added pins only (file grew 572 to 599 lines inside `_COMMON_PINS` and `_SKILL_ONLY_PINS`) |
| qa-conventions-report:C12 | PASS: 633 passed, ruff check and format clean |
| qa-conventions-report:C13 | PASS: `test_routing_refresh.py:33` one-line change |
| qa-conventions-report:C14 | PASS: defaults `sweep.md:35-38` equal `commands.py:27-28,228` |
| qa-conventions-report:C15 | PASS: `find plugins -iname '*sweep*'` finds nothing |
| qa-conventions-report:C16 | PASS: no em dash, en dash (no non-ASCII byte), tab or trailing space in `sweep.md` or `SKILL.md`; each ends in exactly one newline (checked after the fix) |
| qa-primitive-path-report:C1 | PASS: no `src/superclaude/` text in either file (grep exit 1); both path tests pass |
| qa-primitive-path-report:C2 | PASS: no `.py`, `cli/`, `pm_agent`, `contracts/` or `examples/` token in either file (grep exit 1); the new sentences include none |
| qa-primitive-path-report:C3 | PASS: `sweep.md:49-53` installed path first, project copy labelled after |
| qa-primitive-path-report:C4 | PASS: `sweep.md:55` lookup order |
| qa-primitive-path-report:C5 | PASS: `SKILL.md:15` names both command surfaces, installed first |
| qa-primitive-path-report:C6 | PASS: `SKILL.md:33` still informational ("installed as"), unchanged; the new `:49` names no path |
| qa-primitive-path-report:C7 | PASS: `pragmatic.md` unchanged; it names the skill as `sc-sweep-protocol` without a path |
| qa-primitive-path-report:C8 | PASS: `sweep.md:45` `> Skill sc:sweep-protocol` equals `SKILL.md:2` `name: sc:sweep-protocol` |
| qa-primitive-path-report:C9 | PASS: `sweep.md:37-38` against `commands.py`; both unchanged |
| qa-primitive-path-report:C13 | PASS: tests and ruff green (115 + 248 in the two files, 633 and 723 in the wider runs) |
| qa-primitive-path-report:C14 | PASS: `pragmatic.md:22` holds the scoped exception, not the unqualified mandate |
| qa-primitive-path-report:C15 | PASS: cycle-0 claim about the cycle-0 agent; confirmed from disk that no QA scratch folder remains (`/tmp/ironclaude-batch.*`, `/tmp/t248-copy.*`, `/tmp/cmdf-discrim.*` absent) and `git status` shows no stray repository file beyond the expected deliverables and no `.claude/` path |

Rows: 19 + 20 + 16 + 20 + 8 + 13 + 12 = 108. FAIL rows: 0.

## Summary

- F_0: CMD-F1 RESOLVED, CMD-F2 RESOLVED, CMD-F3 RESOLVED, CMD-F4 RESOLVED. Open BLOCKING or MAJOR findings: 0. New BLOCKING or MAJOR findings: 0.
- Cycle-0 PASS set: 108 of 108 ids still PASS (checks table above, 0 FAIL rows). Several rows carry a moved count or a moved line pointer (for example `qa-command-contract-report:C18`, `:C21`; `qa-skill-contract-report:C11`, `:C12`, `:C17`; `qa-test-coverage-report:C14`; `qa-readonly-claims-report:C2`, `:C10`, `:C17`) and none of them has a false claim.
- Counts after the fix: sweep file 115 passed (was 110), `tests/commands tests/recommend` 633 (was 628), with the two severity modules 723 (was 718), routing file 248, severity modules 90, ruff clean, no `src/superclaude` hit.
- Review loop position: this is review 2 of at most 3 (cycle 1 of at most 2 fix cycles); nothing is open, so no second fix cycle is needed.

### Follow-up candidates (Medium, never fail the review)

- N1: add one pin each for the reworded step 5 sentence (`SKILL.md:27`) and the stale-style paragraph (`SKILL.md:49`), so CMD-F3 and CMD-F4 cannot be reverted unnoticed.
- N2: end the pins for conditions (2), (4) and (5) of the exempt reply on their delimiter, so an escape clause appended to a condition fails a test (Y1 passes today).
- Carried: `sweep.md:16` never-as-worker claim is ahead of `src/superclaude/core/WORKER-CONTRACT.md:23` until item 12.2 lands (CMD-F5; the final and contract gates must confirm it).

Minor notes (no action required): N3 (summary line 19 wording), N4 (two stale pointers or counts in result files), N5 (reader notes). The MINOR findings CMD-F5 to CMD-F36 were not re-checked, as the fix scope and this task say.

## Inherited Structural Verdict - Reliance Audit and Self-Audit

No `## Inherited Structural Verdict` section was in the spawn prompt, so this review ran standalone; the 108-id cycle-0 PASS set is the list of checks to re-test, not an inherited verdict to skip.

**(a) Reliance list**
- For checks whose only inputs are files the fix did not touch (`sweep.md`, `pragmatic.md`, `src/superclaude/cli/sweep/`, DESIGN, the addendum, the OQ records, `tests/recommend`), I re-read the live text of `sweep.md`, `pragmatic.md` lines 15-45, the addendum and DESIGN 7.6 and R5, spot-checked code constants by grep, and relied on `find -newer` plus the cycle-0 agent's line evidence for the rest (for example `models.py`, `probes.py` internals). I did not re-derive every cited CLI line.
- Four rows describe cycle-0 scratch runs or the cycle-0 agent's own process and cannot be re-run: `qa-test-coverage-report:C1`, `qa-reader-clarity-report:C11`, `qa-primitive-path-report:C15`, `qa-readonly-claims-report:C20`. Each row says what on disk was confirmed instead.

**(b) Independent semantic checks (tool evidence)**
- Mutation proof that the new pins discriminate: M1, M3, M19, M2, X1, X2, X5, Y5 each fail the expected test ids, per file and for both files (two bash batches on a private /tmp copy, applied-check 1 per file).
- Counter-proof of residual gaps rather than confirmation: X3, X4/Y6 and Y1 pass all 115 tests, giving notes N1 and N2.
- Re-ran the cycle-0 skill-side mutation claims (Y2, Y3, Y4) and got the same outcome.
- Reproduced the stale-style case on this host: `~/.claude/output-styles/pragmatic.md` has 0 matches for `sweep chat-summary exception` and still says `No exceptions.` at line 22.
- Read the arithmetic of the regenerated case map (14 + 74 + 15 + 12 = 115) against `pytest --collect-only` counts, and the moved line cites K:51, K:61, K:63, K:64 against the live skill.
- Re-read `SKILL.md:27` and `:49` as a coordinator new to the project and the new pins as a maintainer (section above).

**Confidence:** Verified: 108/112 | Unverifiable: 4 | Unchecked: 0 | Confidence: 100.0% (112 = 108 check ids + 4 F_0 findings; the 4 unverifiable are the not-re-runnable rows above, for which disk confirmation is recorded)

**Tool engagement:** Read: 24 | Grep: 1 | Glob: 1 | Bash: 9 (approximate). The Read, Grep and Glob total is below the 112 items, so the review is suspect by the agent rule taken literally; the gap is covered by batched Bash calls that each ran many inspections (pytest and ruff runs, two mutation batches with 23 mutation runs in total, one multi-section live-file inspection, one result-file inspection, one changed-file and code-fact inspection, one ledger-coverage check). No web research was done, so no Tavily call was needed.

**Not done by design:** no live Orca, ccsession or Claude command; no HOME file was written; nothing proves a live model follows the exception, which the test docstring and the summary already state.

Verdict: PASS
Blocking count: 0

