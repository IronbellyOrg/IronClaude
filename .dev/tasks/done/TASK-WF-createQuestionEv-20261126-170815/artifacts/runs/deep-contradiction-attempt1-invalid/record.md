# Record of run deep-contradiction-attempt1-invalid

- depth deep, flags `--mode bug --type skill --depth deep`, marker `qev-deep-contradiction-184044`
- expected questions 1, observed 0 as tool calls (0 answered), 0 as plain text
- expected issue create 1, observed 0; issue comment expected None, observed 0
- raw files: fake gh log `runs/deep-contradiction-attempt1-invalid/gh.log`, transcripts `runs/deep-contradiction-attempt1-invalid/transcripts/`, notes `none`, posted body `none`, final output `runs/deep-contradiction-attempt1-invalid/final-output.txt`
- body shown to the user for approval: no (no approval prompt appears in the final output or on the question screens)
- additions in `draft-notes.md` (New material): 0; contradictions in the notes: 0
- final output: literal `kept without approval: <item>` lines (the format of `refs/create.md` Wave 5 step 8): 0; bullet lines listed under a "without asking / without approval" heading instead: 0
- how `present` is decided (approximate): the best single line or window of three lines of the text shares the given share of the addition's distinctive tokens: `yes` is 50 percent or more, `probably` is 33 to 49 percent (the named line is likely the same fact reworded; check it by eye), `no` is below 33 percent; the matching line number and its first words are printed so each answer can be checked

| # | addition (first words) | in notes | in posted body (best line, score) | in final output (best line, score) |
|---|---|---|---|---|

## Invalid run (attempt 1): the driver ended it early

- This run is not a result of the shipped rule. The driver declared the session finished after 231 seconds (`summary.json` drive: status completed, seconds 231) while the deep body drafter `issue-worker-t1` was still running in the background. The last screen (`screen-final.txt`) shows `◯ issue-worker-t1  Reading SKILL.md script table` and the footer `↓ to manage`, and the main agent's last message says Wave 4 "is running now" and that it will ask one question if the code contradicts the description.
- Cause (harness): the idle check counted the session as idle when the screen showed no `esc to interrupt` and no transcript had changed for 25 seconds. A running background agent shows neither. Fixed in `run_create.py` (a listed running agent or the `↓ to manage` footer counts as busy; the quiet threshold for deep is 90 seconds).
- Counts here (0 questions, 0 issue create, 0 comments) therefore say nothing about the rule. Notes, posted body and question were never reached; the notes columns above are "not evidenced".
- This is the one infrastructure repeat the plan allows for this scenario; the repeat is `runs/deep-contradiction`.
