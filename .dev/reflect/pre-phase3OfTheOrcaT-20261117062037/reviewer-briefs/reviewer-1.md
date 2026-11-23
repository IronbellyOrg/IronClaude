# Reviewer 1, persona: analyzer

Read /home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/reflect/pre-phase3OfTheOrcaT-20261117062037/reviewer-briefs/common.md first and follow it.

Your lens: does the plan match the real code? For each task, open the files and symbols it names and check that the described change is possible exactly as written: the names, signatures, line numbers, dataclass fields (frozen, defaults, field order), who constructs and who reads each type, the import graph (circular imports), the render height budget, the key handling, and the existing tests the plan says will keep passing. Look especially for a step that would break an existing test or invariant (for example the R1 golden surface, the rule that a parsed Question keeps no payload, the snapshot byte-identity claim, the regex-pinned guard line) and for an acceptance criterion that cannot hold given the real code. Cite file:line.
