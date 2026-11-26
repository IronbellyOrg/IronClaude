# Record of run deep-additions-only

- depth deep, flags `--mode feature --type cli --depth deep`, marker `qev-deep-additions-only-183517`
- expected questions 0, observed 0 as tool calls (0 answered), 0 as plain text
- expected issue create 1, observed 1; issue comment expected None, observed 1
- raw files: fake gh log `runs/deep-additions-only/gh.log`, transcripts `runs/deep-additions-only/transcripts/`, notes `runs/deep-additions-only/dev-issues/990001/draft-notes.md`, posted body `runs/deep-additions-only/gh-posted/posted-issue-990001-1795718356050.md`, final output `runs/deep-additions-only/final-output.txt`
- body shown to the user for approval: no (no approval prompt appears in the final output or on the question screens)
- additions in `draft-notes.md` (New material): 16; contradictions in the notes: 0
- final output: literal `kept without approval: <item>` lines (the format of `refs/create.md` Wave 5 step 8): 10; bullet lines listed under a "without asking / without approval" heading instead: 10
- how `present` is decided (approximate): the best single line or window of three lines of the text shares the given share of the addition's distinctive tokens: `yes` is 50 percent or more, `probably` is 33 to 49 percent (the named line is likely the same fact reworded; check it by eye), `no` is below 33 percent; the matching line number and its first words are printed so each answer can be checked

| # | addition (first words) | in notes | in posted body (best line, score) | in final output (best line, score) |
|---|---|---|---|---|
| 1 | Codebase pass: `/sc:analyze --depth deep` was followed from  | yes | yes (line 7 "Codebase pass note: `/sc:analyze --depth deep` was", 66%) | no (line 20 "- kept without approval: the codebase pass used Gr", 31%) |
| 2 | Added fact: the `install` command is `src/superclaude/cli/ma | yes | yes (line 38 "- `src/superclaude/cli/main.py:46` `install` comma", 50%) | no (line 12 "- kept without approval: "copied" means skills act", 15%) |
| 3 | Added fact: `install_all_skills` returns `(success, message) | yes | yes (line 39 "- `src/superclaude/cli/install_skills.py:62` `inst", 53%) | probably (line 13 "- kept without approval: the line also prints when", 42%) |
| 4 | Added fact: `superclaude update` calls the same `install_all | yes | yes (line 41 "- `src/superclaude/cli/main.py:402` `update` comma", 60%) | probably (line 14 "- kept without approval: `superclaude update` and ", 40%) |
| 5 | Added fact: existing tests stub `superclaude.cli.install_ski | yes | yes (line 54 "One backward-compatible change in the data flow be", 50%) | no (line 15 "- kept without approval: the count reaches `instal", 14%) |
| 6 | Added fact: no possible duplicate issue was found (`scout.md | yes | yes (line 44 "## Related Issues/PRs", 88%) | probably (line 3 "- **Title:** `[FEATURE] Make \`superclaude install", 38%) |
| 7 | Added fact: regression-gate commands come from the Makefile  | yes | yes (line 111 "- Regression gate: the full suite `uv run pytest`,", 53%) | no (line 6 "- **Flag-review comment:** I posted one (`#issueco", 16%) |
| 8 | Added: Priority Medium, trigger "a planned feature" from the | yes | yes (line 86 "## Priority", 62%) | yes (line 17 "- kept without approval: Priority is Medium (a pla", 50%) |
| 9 | Assumption: the printed line reads `Skills copied: <N>`; the | yes | yes (line 21 "Assumption: the line reads `Skills copied: <N>` (e", 100%) | yes (line 11 "- kept without approval: the printed line reads `S", 56%) |
| 10 | Assumption: "copied" means the skills `install_all_skills()` | yes | yes (line 21 "Assumption: the line reads `Skills copied: <N>` (e", 89%) | yes (line 12 "- kept without approval: "copied" means skills act", 79%) |
| 11 | Assumption: the line is also printed when `install` exits 1, | yes | yes (line 19 "After every install step has run, `superclaude ins", 67%) | yes (line 11 "- kept without approval: the printed line reads `S", 67%) |
| 12 | Assumption: `superclaude update` and `superclaude install -- | yes | yes (line 99 "- Step 2: In `src/superclaude/cli/install_skills.p", 86%) | yes (line 14 "- kept without approval: `superclaude update` and ", 71%) |
| 13 | Assumption: the count reaches `install` through a new option | yes | yes (line 98 "- Step 1: Branch from `integration` in an Orca-cre", 60%) | yes (line 14 "- kept without approval: `superclaude update` and ", 56%) |
| 14 | Assumption: Effort Estimate is 3 hours (one function, one ca | yes | yes (line 83 "- Effort Estimate (hours): 3 (Assumption: one func", 94%) | yes (line 15 "- kept without approval: the count reaches `instal", 50%) |
| 15 | Assumption: a reviewer may check the result with a throwaway | yes | probably (line 109 "- `tests/cli/test_update_command.py`: add a test t", 44%) | no (line 16 "- kept without approval: effort is 3 hours. By tha", 28%) |
| 16 | Assumption: the Problem Statement, User Story, Out of Scope, | yes | probably (line 1 "<!-- /sc:issue feature template (complex). Copy to", 41%) | yes (line 19 "- kept without approval: Problem Statement, User S", 59%) |

## Task 8 facts and findings

- worker that handled the run: `issue-worker-t1` (summary.json agents_spawned: issue-worker-t3 for the lookup, then issue-worker-t1 for the deep flag variant and the deep body; `read-files.txt` lists `issue-worker-t1.md` and `issue-worker-t3.md` as agent files spawned by name, both src-equal). The tier-1 worker was served; no fallback line to `issue-worker-t2` appears in the notes, the flags files or `worker_lines` (empty in `summary.json`).
- read files: every skill, worker and command file read is byte-equal to `src/` (`read-files.txt`, `src-equal=yes` lines); no installed-copy path was read (`installed_copy` null).
- gh calls (`gh.log`): unknown calls 0, other writes 0, one start-up read.
- fork activity: attributed to the run 0; the unattributed items in `summary.json` fork_activity were listed by `review_pending.py` before and after the run, found unrelated, and cleared (`/tmp/createQuestionEv-scratch/pending-cleared.log` and `logs/chain-deep2.log` / `logs/chain-deep.log`). The stop file was checked at the start of every run (`run_create.py` check) and the chain read the pending list before each run: "nothing pending". No stop condition.
- counts: expected 0 questions and 1 issue create; observed 0 questions, 1 create (`--label enhancement --type Feature`, title prefix `[FEATURE]`), 1 comment. Questions and creates match. The comment is a flag-review comment: the worker chose `--type install` against the user's `--type cli` (the comparison left it unresolved); the comment says the issue was not reclassified.
- the final output lists 10 literal `kept without approval:` lines.
- deep adversarial note (from the reviewer's note): in this run the debate ran in fallback mode: the final output says the main session "argued both sides myself instead of spawning separate advocate agents" (`final-output.txt:7`, `dev-issues/990001/adversarial/return-contract.yaml:8` `fallback_mode: true`). This run was made with the driver from before the idle-detection fix. The attempted read of `/root/.claude/skills/sc-issue-protocol/templates/scout-report.md` failed and loaded nothing (`summary.json` failed_reads).
