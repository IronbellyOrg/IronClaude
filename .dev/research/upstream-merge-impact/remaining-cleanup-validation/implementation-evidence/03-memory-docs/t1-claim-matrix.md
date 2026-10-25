# Task 1 claim matrix (live source, read 2026-10-24)

| Corrected claim (both guides) | Live source |
|---|---|
| Dir order: explicit arg > non-empty REFLEXION_OUTPUT_DIR > CWD/docs/memory | src/superclaude/pm_agent/reflexion.py:68-74 |
| Files: solutions_learned.jsonl + sibling mistakes dir; both dirs created in ctor | reflexion.py:76-82 |
| record_error sets timestamp, appends the dict as one JSON line, no redaction/validation | reflexion.py:127-132 |
| Mistake doc only when root_cause or solution truthy; name test_name-DATE.md; same-day overwrite | reflexion.py:135-136, 264-267, 316 |
| Signature = error_type, message (digits->N, first 100 chars), test_name joined with `" \| "` | reflexion.py:153-170 |
| _search_mindbase is a stub returning None; no MindBase backend | reflexion.py:172-184 |
| First matching row in file order; bad JSON lines skipped; returns solution/root_cause/prevention/timestamp (None if absent); no ranking/status/solved filter | reflexion.py:198-219 |
| Match = lowercase whitespace-token sets, intersection/union >= 0.7 (inclusive); empty set = no match | reflexion.py:221-244 |
| get_statistics "solution_reuse_rate" = % rows with a solution | reflexion.py:343-351 |
| Pytest recorder: only @pytest.mark.reflexion + call-phase exception; fields test_name,test_file,error_type,error_message,traceback; no lookup, no solution | src/superclaude/pytest_plugin.py:172-196 |
| reflexion_pattern fixture sets env var + memory_dir to tmp_path | pytest_plugin.py:71-93 |
| Repo tests redirect writes to tmp_path; session guard on docs/mistakes + solutions_learned.jsonl size | tests/conftest.py:28-79, 82-117 |
| Exports ReflexionPattern from superclaude and superclaude.pm_agent | src/superclaude/__init__.py:13,19; src/superclaude/pm_agent/__init__.py:12,18 |
| No other caller in src (no session-start load, no PM auto-capture) | grep of src for ReflexionPattern/get_solution/record_error/REFLEXION_OUTPUT_DIR: only pytest_plugin.py + reflexion.py + exports |
| PM agent definition has no reflexion reference | grep -i reflexion src/superclaude/agents/pm-agent.md: no hits |
| Explicit-API example is isolated: tempfile dir nested as <tmp>/docs/memory so the sibling mistakes dir also stays inside it; nothing written to repo paths | reflexion.py:76-82; plan 03-memory-docs.md:19 |
| Bad-line sentence: non-object JSON line breaks get_statistics (record.get) and can break get_solution; non-string signature fields break only signature building | reflexion.py:153-170, 341-344 |
| Test-suite sentence: conftest sets REFLEXION_OUTPUT_DIR per test (explicit memory_dir still wins) | tests/conftest.py:116-117; reflexion.py:68-71 |
| Isolated snippet was run once (`uv run python t1-snippet-run.py`, the exact guide snippet plus one print line): output `snippet-ok known= None` in t1-snippet-run.out:2; repo stayed clean | reflexion.py:84-136 |
| Lookup stops at the first matching row (so a no-match lookup reads every line) | reflexion.py:202-219 |
| MindBase hook is a stub that always returns None; storage is the local file only | reflexion.py:101-104, 172-184 |
| Empty signature word-set never matches; lookup with none of the three keys matches nothing | reflexion.py:238-239 |
| Message-only JWT pair is 4/8 = 0.50, no match (old 87.5% claim wrong); other pairs 9/10 and 6/12 | reflexion.py:235-244; t1-sigcalc.out |
| Pytest recorder triggers when call.excinfo is set (any call-phase exception) | src/superclaude/pytest_plugin.py:179-196 |
| Mistake document fields and non-empty root_cause/solution trigger | reflexion.py:135, 264-316 |
| Bad rows: non-object JSON breaks get_statistics (record.get) and can break get_solution; non-string signature fields break only get_solution; earlier match returns first | reflexion.py:155-170, 338-346 |
| REFLEXION_OUTPUT_DIR must be non-empty to take effect | reflexion.py:69-71 |
| Constructor creates memory dir and sibling mistakes dir | reflexion.py:80-82 |
| Sample file uses the old ts/task/mistake/evidence/rule/fix layout | docs/memory/reflexion.jsonl.example:1-15 |
| Existing solutions_learned.jsonl rows are pattern-style (no signature keys) | docs/memory/solutions_learned.jsonl:1-4 |
| Nothing but the pytest recorder calls record_error; nothing calls get_solution | src/superclaude/pytest_plugin.py:185-196; grep of src |
| PM agent definition restores context from Serena memory at session start and tells the agent to create docs/mistakes files (neither uses ReflexionPattern) | src/superclaude/agents/pm-agent.md:11,32-35,91 |
| The repository tracks docs/memory/solutions_learned.jsonl | t1-tracked-files.out:9 (git ls-files docs/memory) |
| record_error sets timestamp itself (a caller value is replaced); mistake file name falls back to unknown | reflexion.py:128, 264-266 |
| Exactly-0.70 boundary pair is a match (7 shared / 10 distinct); other pairs 9/10, 6/12, 4/8 | reflexion.py:235-244; t1-sigcalc.out |
| "No token-savings, latency, file-size, error-recurrence or search-time figures have been measured": reflexion.py has only docstring design targets and no timing/token-counting code; get_statistics reports only the share of rows with a solution | reflexion.py:6-12, 343-351; t1-unmeasured.out:1-9 |
| "Earlier versions of this guide quoted percentages and timings (removed)": the original guide had <10% recurrence, 500 tokens, 75-95% savings, <30 seconds; the original README had <10ms/<50ms/<200ms search times | t1-removed-figures.out:2-6, 8-10 |
| Every repo path and link named in either guide exists (docs/FAQ.md is the one pre-existing missing link, restored footer, owned by Task 4; tests/unit/test_reflexion.py, tests/unit/test_reflexion_pollution_guard.py and the pm-agent-autonomous-reflection.md link target all exist) | t1-link-check.out:1-16 |
| README backup now goes to $HOME (outside the repo) and the permission tip is read-only (ls -l); no recipe in either guide writes inside the repo or changes data-file modes | docs/memory/README.md (tar, ls -l recipes); verified by `grep -n 'chmod\|mv \|rm \|>>' ` showing only the two inherited .gitignore echo lines |

Worked examples recomputed with plain set arithmetic (t1-sigcalc.py in this folder, no memory code imported):
- ValueError/invalid port value N in config/test_load_config vs "...config file...": 9/10 = 0.90 match
- vs timeout/settings variant: 6/12 = 0.50 no match
- Old message-only JWT example: 4 shared / 8 union = 50% (not 87.5%)
