# QA Report: cmd-skill gate, cycle 1 verification (rf-qa)

**Topic:** /sc:sweep command and sc-sweep-protocol skill (issue 339, Phase 1)
**Date:** 2026-11-12
**Phase:** fix-cycle
**Fix cycle:** 1
**fix_authorization:** false (no repository file edited; experiments only on private copies under /tmp)

## Overall Verdict

PASS. All four F_0 findings (CMD-F1, CMD-F2, CMD-F3, CMD-F4) are RESOLVED on the live files, 108 of 108 cycle-0 PASS checks still pass, no new BLOCKING or MAJOR finding. `|F_1|` = 0 against `|F_0|` = 4 (strictly fewer, no regression, so neither halt guard fires). Verdict and blocking count are repeated on the last two lines.

## F_0 findings

Method: judged on the live files, not the fix log. Live files read this run: `src/superclaude/skills/sc-sweep-protocol/SKILL.md` (65 lines), `src/superclaude/commands/sweep.md` (69 lines), `src/superclaude/output-styles/pragmatic.md` lines 14 to 43, and `tests/commands/test_sweep_command.py` (599 lines, all four chunks). Mutations were run on a private copy (`mktemp -d /tmp/verify-c1-mut.*`, holding the test file, `sweep.md`, `SKILL.md` and `pragmatic.md` at the same relative layout, so the test read the copy). Baseline on the copy: 115 passed. The copy was removed by an exit trap; `ls -d /tmp/verify-c1-mut.*` afterwards: no such file or directory.

Mutation results (each applied once per file; applied-line count was 1 in every file mutated; "style-only" and "skill-only" rows prove each file is pinned on its own):

| Mutation | Scope | Failing tests | Result |
|---|---|---|---|
| M1: style `omitted only when ALL of these hold` to `omitted when ANY of these hold`; skill `when all of these hold:` to `when any of these hold:` | both | `test_style_carries_common_rule_clause[conditions-are-conjunctive]`, `test_skill_carries_common_rule_clause[conditions-are-conjunctive]` | 2 failed, 113 passed |
| M1 | style only | style test `[conditions-are-conjunctive]` | 1 failed, 114 passed |
| M1 | skill only | skill test `[conditions-are-conjunctive]` | 1 failed, 114 passed |
| M3: `(3) the command exited 0;` to `(3) the command exited 0 or 1;`; skill `- the command exited 0;` to `- the command exited 0 or 1;` | both | `[success-exit-0]` in the style and skill tests | 2 failed, 113 passed |
| M3 | style only / skill only | `[success-exit-0]` in the matching test | 1 failed, 114 passed each |
| M19: `instruction from the person, and that assignment` to `instruction from the person or a peer agent, and that assignment` | both | `[assignment-source-system-developer-or-direct-person]` in both tests | 2 failed, 113 passed |
| M19 | style only / skill only | the matching `[assignment-source-system-developer-or-direct-person]` test | 1 failed, 114 passed each |
| M2: `The exception does not cover` to `The exception also covers` | both | `[ordinary-exception-does-not-cover-the-exclusion-list]` in both tests | 2 failed, 113 passed |
| M2 | style only / skill only | the matching `[ordinary-exception-does-not-cover-the-exclusion-list]` test | 1 failed, 114 passed each |
| X1 (extra): skill `reported accurately in ordinary formatting: step 2` to `... in compact formatting: step 2` | skill | `test_skill_states_clause[failure-exhausted-designed-fallback]`, `test_skill_states_clause[failure-list-is-framed-as-ordinary-formatting]` | 2 failed, 113 passed |
| X2 (extra): skill step 5 second sentence put back to the cycle-0 text `Nothing else is printed as a result.` | skill | none | 115 passed (step 5 wording after its first sentence is not pinned; see notes) |

### CMD-F1 (MAJOR): RESOLVED

Live evidence: `tests/commands/test_sweep_command.py:204-210` holds the new pin `conditions-are-conjunctive` (style `The ordinary DONE / NEXT table is omitted only when ALL of these hold:`, skill `and only the summary counts and the report path are printed, when all of these hold:`); `:225-230` pins `success-exit-0` to the delimiter (`(3) the command exited 0;` and `- the command exited 0;`); `:191-196` ends `assignment-source-system-developer-or-direct-person` on `from the person, and that assignment is still in force`; `:197-202` ends `assignment-in-force-no-higher-conflict` on `instruction;`. Both source texts match: `pragmatic.md:23` ("omitted only when ALL of these hold", "(3) the command exited 0;", "from the person, and that assignment is still in force and conflicts with no higher-priority instruction;") and `SKILL.md:35` and `:37-39`. The cycle-0 mutations M1, M3 and M19 each now fail two tests (one per file), and each fails one test when applied to only one file (table above).

### CMD-F2 (MAJOR): RESOLVED

Live evidence: `tests/commands/test_sweep_command.py:336-342` pins `The exception does not cover other coordinator messages, ordinary person-run invocations, workers or subagents, quoted or merely read sweep text, failures, blockers, parse errors,` for both files; it matches `pragmatic.md:25` and `SKILL.md:47` word for word. `:360-365` ends the missing-output pin on the sentence period; `:453-458` adds the framed failure sentence pin. Mutation M2 now fails two tests (one per file) and one test when applied to one file only. Extra mutation X1 (the frame word changed in the skill) fails two skill pins, so the three bare failure fragments at `:459-466` are no longer the only guard.

### CMD-F3 (MAJOR): RESOLVED

Live evidence: `SKILL.md:27` reads `5. On exit 1 or 2, print the standard error line exactly as it came and end the run. The reply keeps the ordinary formatting, and no summary and no report path are printed.` The pinned first sentence is unchanged (`test_skill_states_clause[exit-1-or-2-prints-stderr-and-ends-run]` passes). The cycle-0 contradiction is gone: `SKILL.md:47` says "Standard error stays visible for exit 1 or 2 ... Non-exempt replies keep the ordinary table and its placement" and `pragmatic.md:25` says the same, and step 5 now also says the error reply keeps the ordinary formatting, so the table is not removed by "Nothing else is printed". `SKILL.md:29` ("reported accurately in ordinary formatting") agrees. The removed words no longer appear (see the wording section).

### CMD-F4 (MAJOR): RESOLVED

Live evidence: `SKILL.md:49` reads `If the output style text loaded in this session has no sweep chat-summary exception (an installed copy that was not refreshed), nothing here is exempt and every reply keeps the ordinary formatting.` It sits in "Final reply" after the "What stays ordinary" paragraph (`:47`) and before `**Scope.**` (now `:51`). It gives the tie-breaker the finding asked for: against a stale installed style that still says "No exceptions" nothing in the skill is exempt, so the two texts cannot disagree on the table rule. It does not contradict `:33` (same rule as the style exception), `:35` (the exempt conditions) or `:51` (Scope: a rule the loaded text states, not a runtime detector); it asks for a check of the loaded text only. The test helper `_skill_parts` (`test_sweep_command.py:92-93`) splits at the four bold leads, so the new paragraph falls inside the `ordinary` part and no existing pin is disturbed (115 passed).

## Checks

All 108 ids of the cycle-0 PASS set, one row each, in the order of `cycle-ledger.md`. Basis: the four changed files (`SKILL.md`, `test_sweep_command.py`, `test-sweep-command.txt`, `test-sweep-command-summary.md`) were re-read or re-run now; every other input has a modification time earlier than the fix (`sweep.md` 06:20, `pragmatic.md` 2026-11-11, `test_routing_refresh.py` 06:21, DESIGN and the revision folder 2026-11-09, `commands.py` 05:10, the other result files 06:20 to 06:33, fix started 06:52) and the key literals were re-grepped live. Line pointers into `SKILL.md` after line 49 moved by 2 (the new paragraph) and test counts moved by 5; where a row says "pointer moved" or "count moved" the claim itself still holds.

| Check id | Result | Evidence (read or run now) |
|---|---|---|
| qa-command-contract-report:C1 | PASS | `sweep.md:2` is `name: sweep` (grep). |
| qa-command-contract-report:C2 | PASS | `sweep.md:9` is `allowed-tools: Skill` (grep); no other tool listed. |
| qa-command-contract-report:C3 | PASS | `sweep.md:8` argument-hint equals the literal at DESIGN 7.6 (`orchestrator-mode.md:655`, read); one such line; frontmatter delimiters at 1 and 10. |
| qa-command-contract-report:C4 | PASS | `sweep.md:3` is one line and holds none of stop, retry, release, merge, removal (read; whole-file grep exit 1). |
| qa-command-contract-report:C5 | PASS | Headings read now: 12 title, 18 Triggers, 22 Usage, 31 Options, 42 Activation, 57 Boundaries; same order as before. |
| qa-command-contract-report:C6 | PASS | `sweep.md:44-47` MANDATORY block, `> Skill sc:sweep-protocol` at `:45`; `SKILL.md:2` is `name: sc:sweep-protocol`. |
| qa-command-contract-report:C7 | PASS | `sweep.md:49` installed path, `:53` project copy, `:55` "Skills read `~/.claude/skills/` first." |
| qa-command-contract-report:C8 | PASS | `commands.py:27` `DEFAULT_WINDOW = "6h"`, `:228` `default=DEFAULT_WINDOW` (grep); `sweep.md:35-38` states the four defaults. |
| qa-command-contract-report:C9 | PASS | OQ-2 record line 34 Chosen `<root>/.dev/sweeps/`, OQ-5 record line 34 Chosen `6h` (files `OQ-2-GQ-10-...` and `OQ-5-GQ-61-...`, unchanged since 2026-11-09); `.gitignore:256` `.dev/sweeps/`; `sweep.md:36,38`; `sweep.md` has no chat-format rule (whole file read). |
| qa-command-contract-report:C10 | PASS | `commands.py:28` `MAX_WINDOW_HOURS = 720`, `:92` `dict.fromkeys`; `probes.py:44` `RUN_ID_RE`, `:358` "no Run bound: pass --run <id>" (grep); matches `sweep.md:35-38`. |
| qa-command-contract-report:C11 | PASS | grep for `unattended`, `--caller`, `src/superclaude` in `sweep.md` and `SKILL.md`: no match; `sweep.md:40` "no worker mode". |
| qa-command-contract-report:C12 | PASS | Same grep: no `src/superclaude/` path; the core doc is named `~/.claude/WORKER-CONTRACT.md` (`sweep.md:16`). |
| qa-command-contract-report:C15 | PASS | `sweep.md:55` against `SKILL.md:15`, `:23-27` and the no-recommendation bullet (pointer moved: now `:61`, was `:59`); same behaviour stated. |
| qa-command-contract-report:C16 | PASS | `models.py:31` `CLASSES`, `report.py:209` "Unscanned" column (grep); both unchanged since 02:4x; `sweep.md:14` classes still named. |
| qa-command-contract-report:C17 | PASS | `sweep.md:57-68` Will and Will Not read now; DESIGN 7.6 Skill bullet (`:663`) "prints no recommendation, proposes no action and never edits, stages or deletes a file" agrees. |
| qa-command-contract-report:C18 | PASS | Run now: `723 passed` for tests/commands, tests/recommend and the two severity modules (633 + 90); `ruff check` "All checks passed!"; `ruff format --check` "2 files already formatted". Count moved (628 and 718 before, +5 new cases); claim holds. |
| qa-command-contract-report:C20 | PASS | `git diff -- tests/recommend/test_routing_refresh.py` is the one line `_POST_REFRESH_ADDITIONS = {"graph", "impact", "issue", "sweep"}` (`:33`), equal to DESIGN `:719` row R5 (read); file unchanged by the fix. |
| qa-command-contract-report:C21 | PASS | Saved artifacts. `step-1.14-checks.md` (06:20:27) and `r5-routing-refresh.txt` (06:22:00) are unchanged and `sweep.md` (06:20:21) is unchanged, so their cited lines still equal disk. `test-sweep-command.txt` now reads `115 passed`, exit 0 (115 PASSED lines, 0 FAILED, ERROR or SKIPPED), equal to the summary's 14 + 74 + 15 + 12 = 115 and to my run. Count moved with the fix; claim holds. |
| qa-command-contract-report:C22 | PASS | `pragmatic.md` unchanged (2026-11-11); `:22` holds the scoped exception, `git grep HEAD` shows `:22` was "No exceptions"; 7 hunks; six qualifiers at lines 57, 62, 64, 73, 84, 94 (grep); the command prescribes no reply format (read). |
| qa-skill-contract-report:C1 | PASS | `SKILL.md:4` is the literal at DESIGN `:661` (read) and `_SKILL_TOOLS` (`test_sweep_command.py:30-33`); the literal test passes. |
| qa-skill-contract-report:C2 | PASS | Five steps at `SKILL.md:23-27` in order (step 5 reworded, still present; deleting it fails a pin on a copy). |
| qa-skill-contract-report:C3 | PASS | `SKILL.md:23` and `:24` both say "Bash timeout 120000 ms"; `test_sweep_skill_step_timeout_120000[1,2]` pass. |
| qa-skill-contract-report:C4 | PASS | `SKILL.md:24`: only on "command not found", `--frozen --no-sync`, "no step runs the command a third time". |
| qa-skill-contract-report:C5 | PASS | `SKILL.md:25` takes only `report_path` and `summary`; `report.py` unchanged since 02:42. |
| qa-skill-contract-report:C6 | PASS | `SKILL.md:25` chunks of at most 150 lines until `Report complete`; `report.py:520` last line `Report complete` (grep). |
| qa-skill-contract-report:C7 | PASS | `pragmatic.md:23-24` against `SKILL.md:37` and `:45` read now: same assignment rule (lines unchanged by the fix). |
| qa-skill-contract-report:C8 | PASS | `SKILL.md:38-43`: loaded invocation, exit 0, parse, Read, final reply only (unchanged). |
| qa-skill-contract-report:C9 | PASS | `SKILL.md:45` person-run exclusion and person request in an assigned coordinator (unchanged). |
| qa-skill-contract-report:C10 | PASS | `SKILL.md:29`, `:45`, `:47`, `:27`; step 5 now says the error reply keeps the ordinary formatting, consistent with `:47` (CMD-F3). |
| qa-skill-contract-report:C11 | PASS | `SKILL.md:45` and Scope (pointer moved: `:51`, was `:49`) say not a runtime detector; the new `:49` sentence asks only to look at the loaded style text and grants no role, right or detector. |
| qa-skill-contract-report:C12 | PASS | `## Boundaries` now `:53-64` (pointer moved): recommends nothing (`:61`), no edit, stage or delete (`:62`), report text is data (`:63`), no tool beyond the two Bash forms and Read (`:64`). |
| qa-skill-contract-report:C13 | PASS | Live file: no `src/superclaude` (grep exit 1), no non-ASCII (count 0), no em or en dash and none of stop, retry, release, merge, removal (grep exit 1), including both new sentences. |
| qa-skill-contract-report:C14 | PASS | `SKILL.md:19` four flags, no environment variable, no worker mode; `commands.py` unchanged since 05:10. |
| qa-skill-contract-report:C15 | PASS | OQ-6 option (b) exception: `pragmatic.md:22-26` and `SKILL.md:31-51` (range end moved from 49); defaults `sweep.md:33-38`, `commands.py:27`; records unchanged. |
| qa-skill-contract-report:C16 | PASS | Run now: `633` for tests/commands plus tests/recommend (was 628; +5), ruff check and format clean. |
| qa-skill-contract-report:C17 | PASS | Saved artifacts. `step-1.15-checks.md` is unchanged (06:23:58); its cites to `SKILL.md:29` and `:37` to `:47` still match; its rows S1 and S3 cite `SKILL.md:49` for Scope, which moved to `:51` (pointer drift only, see notes). The raw test file now shows 115, not 110 (count moved, equals summary and my run). `phase11-validation.md` still shows the pre-fix 718 (snapshot, see notes). |
| qa-skill-contract-report:C18 | PASS | `SKILL.md:1-11` frontmatter and extended-metadata comment, `:15` "No other skill calls this one", Will and Will Not at `:55-64`; the house files are unchanged (`git status` empty). |
| qa-skill-contract-report:C19 | PASS | Routing diff is the same one line (`test_routing_refresh.py:33`). |
| qa-skill-contract-report:C20 | PASS | Scratch run of cycle 0, not re-runnable (the experiments mutated the pre-fix `SKILL.md` and test file, which the fix changed). The claim concerns the skill text; I ran equivalent probes on a private copy: deleting step 5 fails `[exit-1-or-2-prints-stderr-and-ends-run]` (1 failed), deleting the Boundaries "Edit, stage or delete" bullet still gives 115 passed (the same MINOR survivor, CMD-F13). |

| qa-test-coverage-report:C1 | PASS | Process check on cycle-0 reading; not re-runnable. Every input it names exists on disk, was not changed by the fix (except the four files above) and was read in chunks of at most 150 lines in this run. |
| qa-test-coverage-report:C2 | PASS | `test_sweep_command.py:106-111` assert exact equality with `_COMMAND_TOOLS` and `_SKILL_TOOLS` (`:29-33`); `sweep.md:9` and `SKILL.md:4` match. |
| qa-test-coverage-report:C3 | PASS | `_PROJECT_COPY` at `:37`, tests `:119-128` unchanged. Private copy: removing the `sweep.md` project-copy bullet fails `test_sweep_activation_names_project_copy_as_separate_path` (1 failed, 114 passed). |
| qa-test-coverage-report:C4 | PASS | `:131-152` path-first order, "command not found" only, fallback literal, timeout 120000 on each step (unchanged, all pass). |
| qa-test-coverage-report:C5 | PASS | `:155-159` no Unattended mode heading and no `--unattended` in the command. |
| qa-test-coverage-report:C6 | PASS | `:162-164` no `src/superclaude/` in either file. |
| qa-test-coverage-report:C7 | PASS | `:167-168` with `_FORBIDDEN_ADVICE` (`:34-36`) passes on the live skill (no match). |
| qa-test-coverage-report:C8 | PASS | One-line routing diff; `test_routing_refresh.py:647-648` `assert shipped - _POST_REFRESH_ADDITIONS == active` is not vacuous with `sweep.md` present; run now: tests/recommend passes (363 passed with the sweep file). |
| qa-test-coverage-report:C11 | PASS | Injected-report and peer pins present: `:289-297` (never establish or extend), `:487-490` (report text is data), `:468-472` (no fabricated summary). |
| qa-test-coverage-report:C12 | PASS | `:514-587` and the six-site list `:539-576`; exactly 6 qualifier occurrences, at lines 57, 62, 64, 73, 84, 94, none in 22-26 (grep). |
| qa-test-coverage-report:C13 | PASS | `:589-600` default examples, columns, None row, length budget and no leak into Work discipline (unchanged, pass). |
| qa-test-coverage-report:C14 | PASS | Raw file 115 = summary 115 (14 + 74 + 15 + 12, recounted from the test file) = my run 115; severity modules 90 (723 minus 633). `phase11-validation.md` still shows the pre-fix 718: snapshot of the earlier run; the post-fix 723 is in `fix-log-cycle1.md` and my run (count moved by +5, claim holds). |
| qa-test-coverage-report:C15 | PASS | `git status --short -- tests/skills` is empty. |
| qa-test-coverage-report:C16 | PASS | Test docstring `:13-16` says the tests do not prove live model behaviour; the summary's "Static-only limits" is now at `:125-127` (pointer moved, was `:120`) with the same disclaimer; `step-7.10-style-exception.md` unchanged (2026-11-11). |
| qa-test-coverage-report:C19 | PASS | `ruff check` and `ruff format --check` on the two test files clean (run now). |
| qa-test-coverage-report:C20 | PASS | `sweep.md:35-38` against `commands.py:27-28`, `:44-48`, `:228` (grep); unchanged. |
| qa-readonly-claims-report:C1 | PASS | `sweep.md:9` `allowed-tools: Skill`, equal to DESIGN 7.6 and no wider than `graph.md:9`. |
| qa-readonly-claims-report:C2 | PASS | `SKILL.md:4` literal; body names only the two Bash forms and Read (`SKILL.md:64`, pointer moved from `:62`). |
| qa-readonly-claims-report:C3 | PASS | `sweep.md:14`, `:55`, `:66` and `SKILL.md:15`, `:62` (pointer moved from `:60`) against `commands.py` `_publish` (unchanged since 05:10): one report, JSON on stdout. |
| qa-readonly-claims-report:C4 | PASS | Option table `sweep.md:35-38` against `commands.py:27-28`, `:48`, `:92`, `:228` and `probes.py:44`, `:358` (grep). |
| qa-readonly-claims-report:C5 | PASS | OQ-2 and OQ-5 records (Chosen lines 34, unchanged) against `sweep.md:25,33-38` and `commands.py:27`. |
| qa-readonly-claims-report:C6 | PASS | Whole-file grep for the five words: `sweep.md` and `SKILL.md` no match; `pragmatic.md` has hits only outside lines 22-26 (lines 94, 123, 146, 180, 187, 201); no Orca write verb in the three primitives (read). |
| qa-readonly-claims-report:C7 | PASS | `probes.py:62` and `:292-297` `git --no-optional-locks`, `GIT_OPTIONAL_LOCKS=0` (grep). |
| qa-readonly-claims-report:C8 | PASS | `SKILL.md:23-29`: path-first, fallback only on "command not found", timeout 120000 each, only `report_path` and `summary`, 150-line chunks, no third run. |
| qa-readonly-claims-report:C9 | PASS | `pragmatic.md:23-25` and `SKILL.md:35-47` grant no role or action right; the new `:49` sentence only narrows the exception. |
| qa-readonly-claims-report:C10 | PASS | Scope clauses `pragmatic.md:26` and `SKILL.md:51` (pointer moved); `grep -rn -i chat-summary src/superclaude/cli/sweep` no match; `main.py:567-569` registers the group only. |
| qa-readonly-claims-report:C11 | PASS | Success needs exit 0, parsed stdout and a successful Read (`SKILL.md:36-41`); stderr visible and no fabricated summary (`:29`, `:47`); step 5 now also keeps ordinary formatting. |
| qa-readonly-claims-report:C12 | PASS | Style diff against HEAD: 7 hunks (`git diff -U0`), 11 lines added and 7 removed; file unchanged since 2026-11-11, ASCII, six qualified restatements (grep). |
| qa-readonly-claims-report:C13 | PASS | `git grep HEAD` shows `pragmatic.md:22` was "No exceptions"; working `:22` holds the scoped exception. |
| qa-readonly-claims-report:C14 | PASS | Exception no broader than OQ-6 (b) and the addendum (`design-addendum.md:13-19,35`, read): final successful reply only, top-level coordinator assignment. |
| qa-readonly-claims-report:C15 | PASS | `test_sweep_command.py` reads the real files (`_REPO`, `_COMMAND`, `_SKILL`, `_STYLE`, `:24-27`), pins both, docstring `:13-16` states the static-only limit; 115 cases, run now. The cycle-0 count of 110 on a scratch copy moved by +5; claim holds. |
| qa-readonly-claims-report:C16 | PASS | `test_routing_refresh.py:33` adds only `"sweep"`; the diff is the single line (read). |
| qa-readonly-claims-report:C17 | PASS | Saved result files: `step-1.14-checks.md`, `step-1.15-checks.md`, `step-7.10-style-exception.md`, `r5-routing-refresh.txt` and `phase11-validation.md` are unchanged (mtimes before the fix); `test-sweep-command.txt` and `test-sweep-command-summary.md` were regenerated and agree (115, K-lines at 19, 24, 25, 27, 29, 33, 35 to 51, 61, 63, 64 equal the live `SKILL.md`). `step-1.15-checks.md` rows S1 and S3 still cite `SKILL.md:49` (pointer drift, see notes). |
| qa-readonly-claims-report:C18 | PASS | `sweep.md:44-47` Activation, `SKILL.md:2` `name: sc:sweep-protocol`, no Unattended mode section, no `src/superclaude/` path (greps). |
| qa-readonly-claims-report:C19 | PASS | Unchanged forward-reference state: `WORKER-CONTRACT.md:23` still lists agent, git, help, issue, pm, spawn, swarm-wizard (and pr-submit) and not `/sc:sweep`; `git status` of that file is clean, so item 12.2 has not landed. Nothing the check relied on changed; CMD-F5 stays an open MINOR note (it becomes BLOCKING only if item 12.2 does not land before merge). |
| qa-readonly-claims-report:C20 | PASS | The tests pin the skill advice regex and the new pins; the gaps for the command and the style (CMD-F17) are unchanged MINOR notes. |

| qa-reader-clarity-report:C1 | PASS | `SKILL.md:37` and `:45` still separate a real assignment from invocation, role labels and data claims (lines unchanged). |
| qa-reader-clarity-report:C2 | PASS | `SKILL.md:45` and `:47` separate ordinary person-started sessions from a person request inside an assigned coordinator (unchanged; the wording note CMD-F26 stays MINOR). |
| qa-reader-clarity-report:C5 | PASS | `SKILL.md:51` (Scope) and `:19` add no flag, variable, worker mode or detector. The new `:49` sentence tells the reader to look at the loaded style text, not at a runtime signal, so it implies no detector or power. |
| qa-reader-clarity-report:C6 | PASS | `sweep.md:55` ("adds no recommendation and takes no action") and `SKILL.md:15`, `:27`, `:29`, `:47` do not contradict each other; step 5 and `:47` now agree on ordinary formatting for exit 1 or 2. |
| qa-reader-clarity-report:C8 | PASS | No claim wider than the CLI was added; `sweep.md` is unchanged and the fix added none (CMD-F22, CMD-F28 stay MINOR notes). |
| qa-reader-clarity-report:C9 | PASS | `sweep.md:35-38` against `commands.py:27-28`, `:44-48`, `:228` (grep). |
| qa-reader-clarity-report:C10 | PASS | The cycle-0 figure "358 passed" (110 sweep + 248 routing) is a saved scratch count; the same two files now give `363 passed` (115 + 248), ruff clean, and the R5 diff is the same one line. Count moved; claim holds. |
| qa-reader-clarity-report:C11 | PASS | Process check; this run relied on files read now (SKILL.md, command, style lines 14-43, test file, fix log, result files), not on the other lens reports for the F_0 judgments. |
| qa-conventions-report:C1 | PASS | `sweep.md:2-9` key order name, description, category, complexity, mcp-servers, personas, argument-hint, allowed-tools (read); `graph.md` unchanged (`git status` empty). |
| qa-conventions-report:C2 | PASS | `SKILL.md:1-11` frontmatter order and the extended-metadata comment (read). |
| qa-conventions-report:C3 | PASS | Heading order at 12, 18, 22, 31, 42, 57; no Unattended heading (greps). |
| qa-conventions-report:C5 | PASS | Bold Will and Will Not in `sweep.md:59-68` and `SKILL.md:55-64`. |
| qa-conventions-report:C6 | PASS | `SKILL.md:13` H1 and `:15` "Backs `/sc:sweep` (...)" and "No other skill calls this one"; only `sweep.md` names `sc-sweep-protocol` in the skills and commands folders (grep). |
| qa-conventions-report:C7 | PASS | Closing section `## Boundaries` now at `:53` (pointer moved); the note CMD-F32 is unchanged. |
| qa-conventions-report:C8 | PASS | `SKILL.md:4` uses the colon-star form pinned by DESIGN and the test (CMD-F31 note unchanged). |
| qa-conventions-report:C9 | PASS | `_REPO`, `_COMMAND`, `_SKILL`, `_text`, `_frontmatter`, `_section` at `test_sweep_command.py:24-69`, `test_sweep_*` names; `test_graph_command.py` unchanged. |
| qa-conventions-report:C12 | PASS | Run now: `633` in tests/commands plus tests/recommend (was 628, +5); `ruff check` and `ruff format --check` clean. |
| qa-conventions-report:C13 | PASS | `test_routing_refresh.py:33` adds `"sweep"` in the same one-line way as graph, impact, issue. |
| qa-conventions-report:C14 | PASS | Options table against `commands.py:27-28`, `:44-51`, `:226-240` (unchanged since 05:10). |
| qa-conventions-report:C15 | PASS | `find plugins -iname '*sweep*' -o -iname '*sc-graph*' -o -iname 'graph.md'` prints nothing: no plugin mirror for graph or sweep. |
| qa-conventions-report:C16 | PASS | Live files: non-ASCII count 0, tab or trailing-space count 0 for both, no em or en dash; `tail -c 2` shows `r`/`g` then newline, so each ends with exactly one newline (new text included). |
| qa-primitive-path-report:C1 | PASS | `grep -rn 'src/superclaude'` over `sweep.md` and the skill folder: exit 1, no output (run now). |
| qa-primitive-path-report:C2 | PASS | grep for `.py`, `cli/`, `pm_agent`, `contracts/`, `examples/` in both primitives: no match; the package is reached only through `superclaude sweep run`. |
| qa-primitive-path-report:C3 | PASS | `sweep.md:49` installed path first, `:51-53` project copy labelled and second. |
| qa-primitive-path-report:C4 | PASS | `sweep.md:55` "Skills read `~/.claude/skills/` first." |
| qa-primitive-path-report:C5 | PASS | `SKILL.md:15` names `~/.claude/commands/sc/sweep.md` first and the project `.claude/commands/sc/sweep.md` second (unchanged). |
| qa-primitive-path-report:C6 | PASS | `SKILL.md:33` names `~/.claude/output-styles/pragmatic.md` as informational ("installed as"), not a lookup; `Makefile` has only `sync-dev:` at `:109` and no `output-styles` target, and `.claude/output-styles` is absent. The new `:49` sentence names no path. |
| qa-primitive-path-report:C7 | PASS | `pragmatic.md:23-26` name the skill as `sc-sweep-protocol` with no path (read); the style file is unchanged. |
| qa-primitive-path-report:C8 | PASS | `sweep.md:45` `> Skill sc:sweep-protocol` equals `SKILL.md:2` `name: sc:sweep-protocol`. |
| qa-primitive-path-report:C9 | PASS | `--root` and `--output` statements `sweep.md:37-38` against `commands.py:64-123` (unchanged since 05:10). |
| qa-primitive-path-report:C13 | PASS | Run now: 723 passed (633 + 90) and ruff clean (cycle-0 figure 358 for the two sweep-related files is now 363). |
| qa-primitive-path-report:C14 | PASS | `pragmatic.md:22` holds the scoped exception, not the unqualified mandate (read); HEAD `:22` was "No exceptions". |
| qa-primitive-path-report:C15 | PASS | Process check on cycle 0; not re-runnable. Now: `git status` shows no repository change from this review and the review wrote only the cycle-0 report; `ls -d /tmp/cmdf*`, `/tmp/*copy*` and my own `/tmp/verify-c1*` show no scratch directory (the two loose files `/tmp/t208-protected-before.sha` and `/tmp/t223-full.txt` belong to the executor, not to a review copy). |

Cycle-0 ids that are not in the PASS set (17 of 125: command-contract C13, C14, C19; test-coverage C9, C10, C17, C18; reader-clarity C3, C4, C7; conventions C4, C10, C11, C17; primitive-path C10, C11, C12) were not part of this re-check. The four test-coverage and reader-clarity ones tied to F_0 (test-coverage C9, C10, C17, C18; reader-clarity C3, C4, C7) are covered by the CMD-F1 to CMD-F4 verdicts above.

Result: 108 PASS, 0 FAIL (108 rows).

## New findings

No new BLOCKING or MAJOR finding. The fix did not add a defect that fails a cycle-0 PASS check, and no cycle-0 PASS check now fails (108 of 108 PASS).

Notes (MINOR, recorded, never rechecked and never a fix pass on their own):

| Id | Where | Note |
|---|---|---|
| N1 | `phase-outputs/test-results/step-1.15-checks.md` rows S1 and S3 | They cite `SKILL.md:49` for the Scope sentence. The fix put the new CMD-F4 paragraph at `:49` and Scope moved to `:51`. The claim is true; only the line pointer moved. |
| N2 | `phase-outputs/test-results/phase11-validation.md:62` | It still shows `718 passed`, the run before the fix. The post-fix run is 723 (`fix-log-cycle1.md`, and my run). A snapshot, not a false claim. |
| N3 | CMD-F5 carried | `src/superclaude/core/WORKER-CONTRACT.md:23` still does not list `/sc:sweep` and the file is unmodified, so the sentence at `sweep.md:16` stays a forward reference to plan item 12.2. It becomes BLOCKING only if item 12.2 does not land before merge (as `consolidated-findings-cycle0.md` already says). CMD-F6 to CMD-F36 were not touched by the fix and were not rechecked. |

Follow-up candidates (real but non-blocking weaknesses; listed only, no fix pass): the new skill text is not pinned by any test. On a private copy, putting the cycle-0 step 5 sentence back (`Nothing else is printed as a result.`) gave 115 passed, and deleting the whole CMD-F4 paragraph (`SKILL.md:49`) gave 115 passed. Neither CMD-F3 nor CMD-F4 asked for a pin ("smallest fix" was skill text only), so this does not reopen them; a later change could undo them without a test failing.

## Wording constraint check

Question: does any sentence the fix added break a wording constraint of the skill tests (the words stop, retry, release, merge, removal, and the em dash)?

- Live `SKILL.md`: `grep -n -i -E '\b(stop|retry|release|merge|removal)\b|—|–'` prints nothing (exit 1); non-ASCII count 0 for `SKILL.md` and `sweep.md`.
- The test that enforces it, `test_sweep_skill_has_no_stop_retry_release_merge_removal_advice` (`test_sweep_command.py:167-168`), passes in the 115-case run.
- The two added sentences: `SKILL.md:27` "The reply keeps the ordinary formatting, and no summary and no report path are printed." and `SKILL.md:49` "If the output style text loaded in this session has no sweep chat-summary exception (an installed copy that was not refreshed), nothing here is exempt and every reply keeps the ordinary formatting." Neither holds a listed word, an inflected form of one (stopping, retrying, released, merging, removing), an em dash or an en dash. The only inflected neighbour in the file is `removes` at `SKILL.md:45`, which the fix did not add and the base-word regex does not match (CMD-F16 stays a MINOR note).
- The added test text (`test_sweep_command.py`) has no em dash (ruff clean; the file was not mutated by me).
- The `src/superclaude` grep over `sweep.md` and the skill folder: exit 1, no output.

Result: no wording constraint is broken.

## Confidence and tool engagement

- **Confidence:** Verified: 110/113 | Unverifiable: 3 | Unchecked: 0 | Confidence: 100.0%. Items: 108 check ids, 4 F_0 findings and the wording check. Unverifiable (cannot be re-observed; each is marked PASS in the table only because nothing it relied on changed): `qa-test-coverage-report:C1`, `qa-reader-clarity-report:C11`, `qa-primitive-path-report:C15` (statements about how the cycle-0 agents worked).
- **Tool engagement:** Read: about 25 | Grep: 2 | Glob: 0 | Bash: 10 (approximate, as issued). Read plus Grep plus Glob is below the 113 items, so by the engagement rule this review is flagged as suspect on count alone. Reason: many check ids share one source (for example one read of `SKILL.md` or one grep of `commands.py` backs several ids), and the Bash calls included one batched read-only script of 29 inspections (greps, `sed`, `stat`, `git grep`, `ls`), one call of about 10 further read-only inspections, two mutation scripts (19 pytest runs on a private copy, deleted by an exit trap) and the project's pytest, ruff and grep commands. No web research was done (no Tavily or web fallback call).
- **No repository file was edited by me.** The only file written is this report. Experiments used a private copy under `/tmp/verify-c1-mut.*`, removed afterwards (`ls -d` finds none).
- **Limits:** these results show the clauses are present in the loaded text and that the tests now fail on the four widened-eligibility mutations. They do not show that a live model follows the exception, and the installed `~/.claude/output-styles/pragmatic.md` on this host still has no sweep exception (`grep -c 'sweep chat-summary exception'` printed 0), which is the case the new `SKILL.md:49` sentence covers.

Verdict: PASS
Blocking count: 0
