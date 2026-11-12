# Wave 1.6 Branch B (log-config inspection), returned by troubleshoot-analyst, persisted by parent on receipt 2026-11-08T01:57Z

```json
{"branch":"B","query_target":"logging, verbosity and run-record config for orca_worktree.py and the claim return contract","hits":[
{"config_path":"SC_ORCA_TIMEOUT","config_type":"env_var","framework":"stdlib subprocess","effective_level":"n/a (timeout)","snippet":"TIMEOUT_ENV = \"SC_ORCA_TIMEOUT\"","location":"orca_worktree.py:69,99"},
{"config_path":"SC_ORCA_SHIM_INTERVAL","config_type":"env_var","framework":"none","effective_level":"n/a (polling interval)","snippet":"SHIM_INTERVAL_ENV = \"SC_ORCA_SHIM_INTERVAL\"","location":"orca_worktree.py:702"},
{"config_path":"subprocess stderr handling","config_type":"file","framework":"capture_output=True","effective_level":"first stderr line on failure only","snippet":"for line in self.err.splitlines(): ... return line.strip()","location":"orca_worktree.py:86-95,115-134"},
{"config_path":"stdout emit","config_type":"file","framework":"json.dumps","effective_level":"one JSON result","snippet":"print(json.dumps(payload))","location":"orca_worktree.py:172-175"},
{"config_path":"orca worktree create --json","config_type":"file","framework":"Orca CLI","effective_level":"captured then dropped on success","snippet":"if not created.ok and not created.timed_out: out.fail(...)","location":"orca_worktree.py:594-613"},
{"config_path":".dev/issues/<N>/worktree.json","config_type":"file","framework":"JSON record","effective_level":"path, status, launch; no terminal handle","snippet":"record: dict = {\"path\": path, \"status\": status}","location":"orca_worktree.py:474-491,840-845"},
{"config_path":"worktree git-dir launch mirror","config_type":"file","framework":"JSON","effective_level":"path, launch","snippet":"body = json.dumps({\"path\": wt, \"launch\": entry}, indent=2)","location":"orca_worktree.py:848-856"},
{"config_path":"$HOME/.claude/state/launch-level/pending/<nonce>","config_type":"file","framework":"one-word file","effective_level":"level word only","snippet":"PENDING_PARTS = (...)","location":"orca_worktree.py:699,728-729,957"},
{"config_path":"launch result 'terminal'","config_type":"file","framework":"stdout JSON","effective_level":"launched agent's handle only","snippet":"handle = find_handle(data)","location":"orca_worktree.py:951-954,976,1003"},
{"config_path":"SKILL.md return contract","config_type":"pipeline_config","framework":"YAML","effective_level":"worktree_status, launch_status; no terminal list","snippet":"worktree_status: created | reused | failed ...","location":"SKILL.md:105-134"},
{"config_path":"pyproject.toml [tool.pytest.ini_options]","config_type":"file","framework":"pytest","effective_level":"no log settings","snippet":"addopts = [\"-v\", \"--strict-markers\", \"--tb=short\"]","location":"pyproject.toml:107-116"}
],
"reachability_verdicts":[
{"file_path":"src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py","line":608,"verdict":"filtered_out"},
{"file_path":"src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py","line":612,"verdict":"reaches_sink"},
{"file_path":"src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py","line":491,"verdict":"reaches_sink"},
{"file_path":"src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py","line":845,"verdict":"reaches_sink"},
{"file_path":"src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py","line":1003,"verdict":"reaches_sink"},
{"file_path":"pyproject.toml","line":112,"verdict":"unknown"}
],
"degraded":true}
```

Worker conclusion: no logging setup; no record stores the seeded terminal; to see stray terminals someone must list the worktree's terminals at run time or keep the create output. Not read: clickup_claim.py, origin_repo.py, long lines in refs/claim.md.
