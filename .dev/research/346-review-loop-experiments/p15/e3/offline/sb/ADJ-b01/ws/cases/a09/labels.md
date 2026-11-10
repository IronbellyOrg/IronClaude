## Label A
blocking: no
sentence: An implementer who follows AC-C1 (line 172) and P0 (line 158) hits a conflict only if the contract file or the HOW-WE-WORK Orca section contains a literal 'orca orchestration|worktree|terminal|agent' command string, which the document does not state ('will naturally write' is the finding's assumption); the vacuous-pipe claim needs the raw-escape reading, while the cell uses \| for table pipes throughout.
evidence: L172: AC-C1; L147 SA-2: mention allowed 'as an example of a caller's question channel inside the contract file'; L158: P0 adds an Orca section to HOW-WE-WORK.md
confidence: low

## Label B
blocking: no
sentence: Fails: the first branch needs the implementer to write an Orca verb into core files, and SA-2 permits only a mention in the contract file without saying whether a command-form string is allowed, so whether AC-C1 then fails is a guess. The second branch (stripping Orca verbs) is a choice the implementer makes, not what the text states. No stated text is determinately wrong.
evidence: Line 147 (SA-2): 'The only allowed mention of Orca in a changed command is as an example of a caller's question channel inside the contract file.' Line 172 (AC-C1) scans src/superclaude/core. Line 158 (P0) places the contract in src/superclaude/core/WORKER-CONTRACT.md.
confidence: low
