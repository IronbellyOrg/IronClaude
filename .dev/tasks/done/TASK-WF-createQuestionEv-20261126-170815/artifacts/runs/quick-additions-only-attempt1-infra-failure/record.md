# Record of run quick-additions-only-attempt1-infra-failure

- depth quick, flags `--depth quick`, marker `qev-quick-additions-only-175745`
- expected questions 0, observed 0 as tool calls (0 answered), 0 as plain text
- expected issue create 1, observed 1; issue comment expected 0, observed 0
- raw files: fake gh log `runs/quick-additions-only-attempt1-infra-failure/gh.log`, transcripts `runs/quick-additions-only-attempt1-infra-failure/transcripts/`, notes `none`, posted body `runs/quick-additions-only-attempt1-infra-failure/gh-posted/posted-issue-990001-1795716000963.md`, final output `runs/quick-additions-only-attempt1-infra-failure/final-output.txt`
- body shown to the user for approval: no (no approval prompt appears in the final output or on the question screens)
- additions in `draft-notes.md` (New material): 0; contradictions in the notes: 0
- final output: literal `kept without approval: <item>` lines (the format of `refs/create.md` Wave 5 step 8): 6; bullet lines listed under a "without asking / without approval" heading instead: 6
- how `present` is decided (approximate): the best single line or window of three lines of the text shares the given share of the addition's distinctive tokens: `yes` is 50 percent or more, `probably` is 33 to 49 percent (the named line is likely the same fact reworded; check it by eye), `no` is below 33 percent; the matching line number and its first words are printed so each answer can be checked

| # | addition (first words) | in notes | in posted body (best line, score) | in final output (best line, score) |
|---|---|---|---|---|

## Infrastructure failure (attempt 1)

- This folder is the first attempt of the quick additions-only run. It is an infrastructure failure, not a model result. The real command line is in `prompt.txt` (`--mode feature --type cli --depth quick`); the flags line at the top of this record says only `--depth quick` because no summary of the first attempt was saved.
- Cause: the model session completed, then the harness crashed in its own post-processing (`read_files_report`) with this line, quoted from `logs/quick-additions-only-attempt1.out` line 14: `PermissionError: [Errno 13] Permission denied: '/root/.claude/commands/sc/analyze.md'`. The harness read a file under a home folder it cannot access; the model never chose this.
- Not saved: `draft-notes.md` and `issue-body.md`, because the crash came before the copy of the run's issue folder and the repeat reused the same clone folder. So the notes columns above are "not evidenced": 0 additions listed means "no notes file was saved", not "no additions".
- Fork activity: not recorded. The crash came before the fork check was written, so this run has no fork result (the field is empty, not a clean result). Reported to the lead as a finding; no STOP was written.
- Counts, re-derived from `gh.log` and the transcripts (see `summary.json`): questions 0, `issue create` 1, `issue comment` 0, unknown gh calls 0.
- The repeat that replaced it, and the run that counts for the matrix: `runs/quick-additions-only`.
