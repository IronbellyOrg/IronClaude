**M-12 (MAJOR, graded Medium) AC-C1 can fail on content the candidate asks for.** Experts: Fowler, Adzic.
- Sentence: an implementer who follows P0 adds an Orca section to `HOW-WE-WORK.md` and writes the contract file with a question-channel example (SPEC:158, SPEC:147, SPEC:150), both under `src/superclaude/core`, which AC-C1 requires to print nothing for `orca orchestration ...` and similar (SPEC:172); SA-2 allows the mention "inside the contract file" (SPEC:147).
- Why Medium: it fails only if the text includes a literal command of those four verbs.
- Recommendation: exclude the contract file and routing guide from AC-C1, or forbid literal command lines there. Also the checks in 7.1 are written with `\|` in a table, which is only correct once rendered; copied raw they do not run.
