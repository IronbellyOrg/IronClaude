## Label A
blocking: no
sentence: The harm needs assumptions: the doc never says the contract file or HOW-WE-WORK Orca section contains the 'orca orchestration' pattern; the '\|' is a markdown table escape for a pipe, not a literal pipe in the command.
evidence: document.md:164-170 (SA-2, AC-C1 inside a table cell using '\|'); P0 row (line ~158) adds Orca section without stating verb text.
confidence: low

## Label B
blocking: no
sentence: An implementer who writes an orca orchestration example into WORKER-CONTRACT.md as SA-2 permits then fails AC-C1, but that needs the assumed example; the literal backslash-pipe makes AC-C1 vacuous rather than impossible to pass.
evidence: Line 147 (SA-2): 'The only allowed mention of Orca in a changed command is as an example ... inside the contract file.' Line 158 (P0) adds src/superclaude/core/WORKER-CONTRACT.md. Line 172 (AC-C1): grep -rnE with '(orchestration\|worktree\|terminal\|agent)' and 'prints nothing'.
confidence: high
