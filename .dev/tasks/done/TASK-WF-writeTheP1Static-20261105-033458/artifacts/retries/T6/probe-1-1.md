5e9b062753b8b34b6b60e7f0aac181bf7badad47
family: report-dir-path-rules (F1.1)
defect form: the path rules for --report-dir in the Unattended mode section list fewer excluded directories than the plan skeleton
search: grep -n -e 'report directory known' -- src/superclaude/commands/cleanup-audit.md
before:
95:- **Report directory.** `--report-dir <dir>` only: the command has no directory flag, and its audit output stays in the fixed `.claude-audit/`. Without `--report-dir` the run is refused before any 
coupled sites: the Report directory bullet in src/superclaude/commands/cleanup-audit.md (line 95); no other sentence in the touched files states these rules
after:
95:- **Report directory.** `--report-dir <dir>` only: the command has no directory flag, and its audit output stays in the fixed `.claude-audit/`. Without `--report-dir` the run is refused before any work and the refusal is printed in chat only. A directory in
