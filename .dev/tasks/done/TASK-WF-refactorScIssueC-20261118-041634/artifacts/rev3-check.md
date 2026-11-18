# Second fresh check of the plan (2026-11-18), and revision 3

Checker: a second fresh read-only reviewer agent (reflect-reviewer class, alias sonnet; the first checker used opus). It had not seen the plan, did not write it, ran no tests and did not run the schema validator. It was told which five fixes to verify and to hunt for new defects independently.

Verdict on revision 2: FAIL, one blocking defect and one medium.
- Blocking: `tests/skills/test_model_alias_policy.py:191-196` (`test_issue_chains_use_the_default_brainstorm_models`) asserts at least 3 `/sc:brainstorm` spans in `refs/chains.md`. Task 1 removes the simple-feature one and leaves 2, so the test would fail, and no task edited or ran that file. The first pre-check, the first review and the first checker all missed it. The orchestrator re-read the test and the file (3 spans today) and confirmed it.
- Medium: Task 4's Wave 8 addition could be read as going inside the command text that `tests/skills/test_issue_protocol.py:460` pins (`orca_worktree.py" launch --number <N> --source <D> --level <L>`). Confirmed by re-reading the test.
- Note: Task 9 (HOW-WE-WORK.md line 328) was not named in the amended `source.md`.

The five late fixes of revision 2 were verified right and to match the real files: the Impact cell at architecture reference line 1557; the file name and lines 66, 78, 87 and 274 in `docs/designs/sc-issue-claim-pipeline-flag.md`; the Notes-list bullet in `docs/designs/sc-issue-command.md` (lines 245-249); the `launch` entry of `worktree.json` as the source of an already-launched level (`orca_worktree.py:1626-1629`; the `already_launched` output at :1713-1721 carries no level); and line 274 stating the old `--submit` condition. The checker found no scope creep on `--submit`, no contradiction among Tasks 3, 4, 5 and 7, and valid front matter and package files.

Revision 3 applies, in a scratch copy then replacing the package: Task 2 also changes `test_issue_chains_use_the_default_brainstorm_models` to at least 2 and its acceptance command now also runs `tests/skills/test_model_alias_policy.py`; Task 4 puts the Wave 8 sentence after the unchanged command line (in `refs/claim.md` and in SKILL.md line 92) and its acceptance says so; `source.md` now names the two chain-row tests and the routing-guide line 328 with its mirror; the grounding file records the missed test. A search of `tests/` for other readers of `chains.md` found only `test_issue_protocol.py`, `test_model_alias_policy.py` and a comment in `test_issue_worker_agents.py`.

Revision 2 is kept in artifacts/plan-rev2-before-checker-b.md and the revision 2 to 3 change set in artifacts/plan-rev2-to-rev3.diff. Revision 3 has not itself been re-reviewed by a third checker.
