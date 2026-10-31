**Phase 3 (adopt codegraph), group B: agents: done**

- Commit: fd249cc9 on branch feat/codegraph-adoption
- Changed:
  - src/superclaude/agents/troubleshoot-analyst.md (roster gains codegraph search, node, callers, impact; working rule 1 points to the guide, codegraph before the Grep floor)
  - src/superclaude/agents/reflect-reviewer.md (same four names; verification step points to the guide)
  - src/superclaude/agents/reuse-auditor.md (search, node, callers; fingerprint facets F1 and F4 and the auggie-unavailable fallback put codegraph above the unchanged Grep floor)
  - src/superclaude/agents/auggie-reviewer.md (search, node, callers; tool list and boundaries name codegraph; "Do not run the codegraph CLI through Bash")
  - tests/troubleshoot/test_diagnostic_worker_contract.py (pinned analyst roster plus two new rejected mutants: the codegraph wildcard and an unlisted codegraph tool)
  - tests/agents/test_codegraph_rosters.py (new, 10 tests)
- Checks run and result:
  - `uv run pytest tests/troubleshoot/test_diagnostic_worker_contract.py tests/agents`: PASS, 64 passed.
  - Extra run of the reflect, auggie-review and troubleshoot tests that read these agents: 693 passed.
  - No `codegraph_explore`, codegraph wildcard or `Bash(codegraph *)` in any agent: PASS.
  - The agents have no plugin or root copies, so there were no twins to change.
- Decisions made on my own:
  - Each agent's guide line also says it calls codegraph only when the brief says the index is fresh, passes the brief's project path, and falls back to Grep when codegraph is unusable or empty (standing rules 2-4 of the spec, kept in one sentence).
- Left for later / blocked: none (the briefs that pass the index state to these agents are edited with the skills that own them, in groups C and E)
- Next group: C, troubleshoot and other skills
