# Record of run deep-flag-preserved

- depth deep, flags `--mode bug --type cli --depth deep`, marker `qev-deep-flag-preserved-190117`
- expected questions 0, observed 0 as tool calls (0 answered), 0 as plain text
- expected issue create 1, observed 1; issue comment expected 1, observed 1
- raw files: fake gh log `runs/deep-flag-preserved/gh.log`, transcripts `runs/deep-flag-preserved/transcripts/`, notes `runs/deep-flag-preserved/dev-issues/990001/draft-notes.md`, posted body `runs/deep-flag-preserved/gh-posted/posted-issue-990001-1795720067637.md`, final output `runs/deep-flag-preserved/final-output.txt`
- body shown to the user for approval: no (no approval prompt appears in the final output or on the question screens)
- additions in `draft-notes.md` (New material): 18; contradictions in the notes: 0
- final output: literal `kept without approval: <item>` lines (the format of `refs/create.md` Wave 5 step 8): 0; bullet lines listed under a "without asking / without approval" heading instead: 0
- how `present` is decided (approximate): the best single line or window of three lines of the text shares the given share of the addition's distinctive tokens: `yes` is 50 percent or more, `probably` is 33 to 49 percent (the named line is likely the same fact reworded; check it by eye), `no` is below 33 percent; the matching line number and its first words are printed so each answer can be checked

| # | addition (first words) | in notes | in posted body (best line, score) | in final output (best line, score) |
|---|---|---|---|---|
| 1 | Tooling: codegraph and auggie were not available to this wor | yes | yes (line 48 "Pass: `/sc:analyze --depth deep` by following `~/.", 65%) | no (line 20 "- The code tools codegraph and auggie weren't avai", 30%) |
| 2 | A-001 (adversarial/merged-flags.md, agreed qualification): t | yes | probably (line 92 "Print one final line, `Skills copied: N` (wording ", 47%) | yes (line 9 "- **Last line on every path:** the line prints aft", 53%) |
| 3 | A-002 (adversarial/merged-flags.md, agreed qualification): " | yes | yes (line 119 "- `tests/cli/test_update_command.py` (stubbed inst", 53%) | probably (line 10 "- **What "copied" means:** only newly installed sk", 37%) |
| 4 | Citation correction to A-002: merged-flags.md cites the zero | yes | probably (line 119 "- `tests/cli/test_update_command.py` (stubbed inst", 42%) | no (line 17 "- `install_all_skills` can report success and drop", 17%) |
| 5 | Observation (out of scope, not filed as a fix): src/supercla | yes | yes (line 119 "- `tests/cli/test_update_command.py` (stubbed inst", 59%) | probably (line 9 "- **Last line on every path:** the line prints aft", 33%) |
| 6 | Observation: `superclaude update` calls the same `install_al | yes | yes (line 110 "- Step 1: expose the installed count without break", 53%) | probably (line 11 "- **Proposed fix:** `install_all_skills` would rep", 47%) |
| 7 | Environment facts added to the body: package version 6.1.0 ( | yes | yes (line 9 "- OS: Not known yet (the reporter's OS is not give", 57%) | no (line 18 "- Extra code, test and environment details from th", 10%) |
| 8 | Related issues: none (scout.md: no results for `superclaude  | yes | yes (line 60 "## Related Issues", 89%) | yes (line 6 "**One disagreement with your flags.** At deep dept", 56%) |
| 9 | Test-landscape facts: tests stub `install_all_skills` with 2 | yes | yes (line 56 "- Callers that depend on the `(bool, str)` shape: ", 72%) | no (line 11 "- **Proposed fix:** `install_all_skills` would rep", 32%) |
| 10 | Proposed Solution and Fix approach design (optional `counts` | yes | yes (line 90 "## Proposed Solution", 62%) | no (line 9 "- **Last line on every path:** the line prints aft", 29%) |
| 11 | Assumption: the exact wording of the line is `Skills copied: | yes | yes (line 5 "`superclaude install` never reports how many skill", 56%) | yes (line 16 "- The line's wording, `Skills copied: N`, is my as", 67%) |
| 12 | Assumption: the count line applies to `superclaude install`  | yes | yes (line 119 "- `tests/cli/test_update_command.py` (stubbed inst", 53%) | probably (line 9 "- **Last line on every path:** the line prints aft", 47%) |
| 13 | Assumption: the return type `Tuple[bool, str]` of `install_a | yes | probably (line 110 "- Step 1: expose the installed count without break", 45%) | no (line 11 "- **Proposed fix:** `install_all_skills` would rep", 23%) |
| 14 | Assumption: severity in Impact Assessment is "low" (output o | yes | yes (line 35 "## Impact Assessment (Severity, Blast Radius)", 86%) | probably (line 18 "- Extra code, test and environment details from th", 43%) |
| 15 | Assumption: Priority is Medium, because the information is o | yes | yes (line 100 "Medium: degraded behaviour with a workaround (trig", 72%) | probably (line 12 "- **Priority:** Medium. The output is missing info", 33%) |
| 16 | Assumption: `docs/getting-started/installation.md` ("What's  | yes | yes (line 113 "- Step 4: if the install output is documented, add", 50%) | probably (line 9 "- **Last line on every path:** the line prints aft", 38%) |
| 17 | Assumption: no `make sync-dev` is needed, because the fix to | yes | yes (line 113 "- Step 4: if the install output is documented, add", 67%) | probably (line 18 "- Extra code, test and environment details from th", 44%) |
| 18 | Pushback note (not a contradiction, for the Wave 5 comment,  | yes | no (line 111 "- Step 2: print the final line in `src/superclaude", 18%) | probably (line 6 "**One disagreement with your flags.** At deep dept", 36%) |

## Task 8 facts and findings

- worker that handled the run: `issue-worker-t1` (summary.json agents_spawned: issue-worker-t3 for the lookup, then issue-worker-t1 for the deep flag variant and the deep body; `read-files.txt` lists `issue-worker-t1.md` and `issue-worker-t3.md` as agent files spawned by name, both src-equal). The tier-1 worker was served; no fallback line to `issue-worker-t2` appears in the notes, the flags files or `worker_lines` (empty in `summary.json`).
- read files: every skill, worker and command file read is byte-equal to `src/` (`read-files.txt`, `src-equal=yes` lines); no installed-copy path was read (`installed_copy` null).
- gh calls (`gh.log`): unknown calls 0, other writes 0, one start-up read.
- fork activity: attributed to the run 0; the unattributed items in `summary.json` fork_activity were listed by `review_pending.py` before and after the run, found unrelated, and cleared (`/tmp/createQuestionEv-scratch/pending-cleared.log` and `logs/chain-deep2.log` / `logs/chain-deep.log`). The stop file was checked at the start of every run (`run_create.py` check) and the chain read the pending list before each run: "nothing pending". No stop condition.
- counts: expected 0 questions, 1 issue create filed as a bug, 1 issue comment; observed 0 questions, 1 create, 1 comment. Matches.
- from the fake gh log (`gh.log`): the issue was created with the user's `--mode bug`: title prefix `[BUG]` (title `[BUG] superclaude install does not print how many skills it copied as its last line`), `--type Bug`, `--label bug` (create at 19:07:47). Then the Complexity-field POST and the pushback comment as a separate `issue comment` call (19:08:01, after the create). Number of `issue comment` calls: 1.
- deep adversarial flag check: all three flags were given, so the deep check ran. The run folder holds `dev-issues/990001/flags-user.md` (the user's variant: mode bug, type cli, decided by the user), `flags-t1.md` (the independent variant by `issue-worker-t1`: mode feature, type cli, Issue type Feature), `flags.md` (decision: the user's flags kept) and `adversarial/` (the debate; `flags.md` cites `adversarial/merged-flags.md`, convergence 100%, favouring `feature`). Two `general-purpose` agents ran as the debate advocates (summary.json agents_spawned). The disagreement was posted as the pushback comment (`gh-posted/posted-comment-990001-*.md`) and the issue was not reclassified.
- finding (form of the final output): the retained additions are listed under "The body kept these additions without your approval:" (5 bullets, not literal `kept without approval: <item>` lines); the record's keyword rule does not match the phrase "without your approval", so its count of 0 is a rule limit. Raw file: `final-output.txt:15-19`.
