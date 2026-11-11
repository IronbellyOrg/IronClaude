## Label A
blocking: no
sentence: An implementer who runs AC-C1 (line 172) gets the pipe-alternation reading only if the table escape \| is taken as a literal; the same cell uses \| for its shell pipes, so the intended reading is plain pipes and the vacuity needs the worse of two readings. The SA-2 conflict also needs the contract file to contain a literal 'orca orchestration|worktree|terminal|agent' string, which no stated text requires.
evidence: L172: AC-C1 pattern with `\|` and `\| grep -v` in a table cell; L147 SA-2: "only allowed mention of Orca ... as an example of a caller's question channel inside the contract file"; L158 P0 deliverables
confidence: low

## Label B
blocking: no
sentence: Fails: whether AC-C1 misses an Orca call depends on reading the raw markdown '\|' as a literal pipe. Read as the rendered table cell it is alternation and matches. Choosing the raw reading is a guess about the worse of two readings, and the result is a weak gate, not an acceptance criterion that cannot pass.
evidence: Line 172 (AC-C1): '\borca(-ide)?[[:space:]]+(orchestration\|worktree\|terminal\|agent)\b' with 'prints nothing'. Line 147 (SA-2) permits an Orca mention inside the contract file; this does not by itself contradict the pattern.
confidence: low
