### F-01 BLOCKING: AC-C1 cannot pass as written (Wiegers)
- Locations: `spec:172` (AC-C1 greps `src/superclaude/core`), `spec:158` (P0 adds an Orca section to `core/HOW-WE-WORK.md`), `spec:150` (SA-5 says the routing guide gains an Orca section), `spec:147` (SA-2 allows an Orca mention in the core contract file), `spec:52` (contract file lives in `core`).
- Sentence: An implementer who follows P0 and SA-2 writes Orca commands into the core guide and the contract file, AC-C1 then prints those lines, and the P0 check cannot pass.
- Evidence: AC-C1 excludes only `skills/ccsession-tag/` (`spec:172`).
- Recommendation: Narrow AC-C1 to commands, skills and agents, which is the scope SA-2 uses (`spec:147`), or list the core lines that are allowed to name Orca.
- Priority: High.
