# Task 3 claim matrix (live source, read 2026-10-24)

| Corrected claim (policy or reflection reference) | Live source / evidence |
|---|---|
| ReflexionPattern lives at src/superclaude/pm_agent/reflexion.py (the old superclaude/core/pm_init/reflexion_memory.py path does not exist) | src/superclaude/pm_agent/reflexion.py; t3-static-check.out (link rows) |
| Storage is solutions_learned.jsonl in the memory dir (not reflexion.jsonl); mistakes go to the sibling mistakes dir | reflexion.py:76-82, 110-136 |
| Directory precedence: memory_dir argument > non-empty REFLEXION_OUTPUT_DIR > docs/memory/ under the cwd | reflexion.py:68-74 |
| Search is word-set overlap on error_type + error_message + test_name, 0.7 inclusive (not 50% keyword), first match in file order, returns solution/root_cause/prevention/timestamp | reflexion.py:153-170, 198-244 |
| MindBase hook is a stub returning None; no MindBase backend or automatic storage | reflexion.py:101-104, 172-184 |
| Not called by the PM agent and not loaded at session start; only the pytest plugin records automatically (marked tests whose call phase raises); it does not call get_solution and adds no solution | src/superclaude/pytest_plugin.py:179-196; grep of src (no other caller); src/superclaude/agents/pm-agent.md has no reflexion reference |
| The PM agent definition itself uses Serena read_memory / write_memory, so the old ban on them is superseded | src/superclaude/agents/pm-agent.md:32-35, 54, 109-114, 245-262 |
| docs/memory/ is live storage with tracked records, so the old "do not create docs/memory/" and "remove docs/memory/ references" items are superseded | t1-tracked-files.out:1-10; reflexion.py:73-74 |
| Raw error record fields: error_type, error_message, test_name, traceback, solution, root_cause, prevention, timestamp; nothing is redacted; mistake note only when root_cause or solution is non-empty | reflexion.py:127-136, 264-316; docs/memory/reflexion.jsonl.example:1-6 |
| Reflection reference Example 4 returns sample row 1's fields for the 9/10 = 0.90 pair | docs/memory/reflexion.jsonl.example:1; t2-reader-smoke.out:1 (existing class, isolated storage); t3-static-check.out |
| Savings, recurrence and token figures in the memory paragraphs are labelled design targets, historical estimates or unverified | reflexion.py:6-12 (docstring targets only); t1-unmeasured.out |
| docs/research/reflexion-integration-2025.md and docs/architecture/pm-agent-responsibility-cleanup.md no longer exist, so their mentions are marked historical (not recreated) | t3-static-check.out (link rows); `ls` of both paths: missing |
| Unrelated MCP policy sections and unrelated reflection layers/examples are unchanged (marker counts equal HEAD) | t3-static-check.out (unrelated-marker rows) |
| Only the two Task 3 docs changed in this task; production code, tests, guards and data are unchanged | t3-hash-compare.out |
