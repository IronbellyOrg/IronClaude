Implementer claims (not evidence):
- Built scripts/worktree_cleanup.py with a Runner whose check_allowed is a positive allowlist by program (git, gh, orca, tar, xargs, the landed check) with banned shapes refused inside allowed verbs.
- Chose to compare whole option tokens for git push, a fixed deny set, because the plan lists the banned shapes by name.
- Added tests/worktree_cleanup/{__init__,conftest,test_runner}.py with a recording runner and refusal tests per banned shape.
- Believed T2.AC1, T2.AC3 and T2.AC4 met by --help, main(argv, runner, env), the ast scans and the notice block.
- Believed T2.AC2 met for the shapes named in the plan; the review shows token-level matching misses bundled and abbreviated push flags.
- The A2 fix pass limited the credential to gh, the landed check and git network verbs; the plan names gh and git push only.
