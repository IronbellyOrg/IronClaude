dbc6c007553df880bd8b6aeea3c8ea3665f2e234
## Family legacy-final-evidence (from review r1-1, finding F1.1)
- Defect form: the legacy-run bullet of the new recovery subsection states where a re-review blocker is recorded in words that differ from the plan's quoted instruction ("recorded in the `FINAL:` evidence and the summary").
- Search command: grep -n -F -e 'blocker found by the re-review' -- src/superclaude/skills/sc-implement-protocol/refs/qa.md plugins/superclaude/skills/sc-implement-protocol/refs/qa.md
- Before-output:
  - src/superclaude/skills/sc-implement-protocol/refs/qa.md:379: "... A blocker found by the re-review is reported in the summary and appends no `blocked` line, because the legacy FINAL never reopens a task."
  - plugins/superclaude/skills/sc-implement-protocol/refs/qa.md:379: the same line (byte-identical twin)
- Coupled sites: the same sentence in the plugins/ twin (recopy after the fix); no other line in refs/qa.md states where a legacy blocker is recorded (a second search for 'reported in the summary' finds only line 379).
- After-output (probe re-run after the fix):
  after: src/superclaude/skills/sc-implement-protocol/refs/qa.md:379:- In a legacy run, when the legacy FINAL records a saved-prompt template difference in its `FINAL:` evidence, the executor runs this recovery before it prints the final s
  after: plugins/superclaude/skills/sc-implement-protocol/refs/qa.md:379:- In a legacy run, when the legacy FINAL records a saved-prompt template difference in its `FINAL:` evidence, the executor runs this recovery before it prints the fin
  after: sentence recorded in plan and twin: 1 / 1
