### M5 MAJOR, graded Medium. AC-C1 conflicts with SA-2 and with what P0 puts into `core/`
- Issue: AC-C1 (S:172) requires the grep over `src/superclaude/core` to print nothing; SA-2 (S:147) allows an Orca mention in the contract file as an example of a question channel; P0 (S:158) adds `WORKER-CONTRACT.md` (section 2 rules, which name `worker_done`, `heartbeat`, `ask`, `check`) and an Orca section to `HOW-WE-WORK.md`, both under `core/`. Whether either file contains a line matching `orca <orchestration|worktree|terminal|agent>` is left to the author. The pattern also misses `ORCA orchestration ...` (placeholder form used in S:180-186), `orca-ide skills ...`, `orca status`, `orca open`.
- Expert: Wiegers (testability). Priority: Medium.
- Grading sentence: An implementer who follows the stated text as written may write `orca orchestration ask` in the contract file as SA-2 permits and then fail AC-C1 in P0; needs the guess that the author writes the literal command, so Medium.
- Recommendation: scope AC-C1 to `commands/`, `skills/`, `agents/` and exclude the two named core files, or ban literal commands in them.

=== ARCHITECTURE ANALYSIS ===
Experts: Fowler (lead), Nygard, Newman, Hohpe.
