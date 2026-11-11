## Label A
blocking: no
sentence: AC-C1 only matches the literal forms 'orca orchestration|worktree|terminal|agent', and the document never says the contract file or the HOW-WE-WORK Orca section contains those strings (SA-2 only allows a mention of Orca, WC-3 refers to 'the preamble's ask command'); the claimed failure needs a guess about the content an implementer writes.
evidence: L172 AC-C1 grep over src/superclaude/core; L147 SA-2 'only allowed mention of Orca ... inside the contract file'; L158 P0 adds WORKER-CONTRACT.md and an Orca section; L61 WC-3
confidence: low

## Label B
blocking: no
sentence: An implementer who follows P0 and SA-2 writes an Orca section into HOW-WE-WORK.md and an Orca example into WORKER-CONTRACT.md; whether AC-C1 then prints a line depends on wording the text does not fix (SA-2 names no command text), and wording that avoids the grep pattern passes. The check is passable as written, so the text does not make it impossible, though the SA-2 and AC-C1 scopes are muddled.
evidence: line 147 (SA-2: 'The only allowed mention of Orca ... as an example of a caller's question channel inside the contract file'); line 158 (P0: add Orca section to HOW-WE-WORK.md, add WORKER-CONTRACT.md to core); line 172 (AC-C1 grep over src/superclaude/core, prints nothing); line 52 (contract file lives in core)
confidence: low
