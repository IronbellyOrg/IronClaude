{
"branch":"B",
"query_target":"src/superclaude/cli/swarm/lenses/refactor_find.py and immediate recommendation pipeline",
"hits":[
{"config_path":"src/superclaude/cli/swarm/commands.py","config_type":"file","framework":"Swarm RuntimeSpec","effective_level":"Unobserved runtime level; generated spec declares info","snippet":"\"runtime\": {\"mode\": \"inline\", \"log_level\": \"info\"}","location":"commands.py:931-937; models.py:617-619; schema.py:387-398"},
{"config_path":"src/superclaude/cli/swarm/config.py","config_type":"file","framework":"SwarmConfig","effective_level":"INFO source default; from_env passes explicit log_level argument, not log-level env lookup","snippet":"log_level: str = \"INFO\"; log_level=log_level","location":"config.py:110-153"},
{"config_path":"src/superclaude/cli/swarm/logging_.py","config_type":"file","framework":"Custom dual-format Logger","effective_level":"No severity threshold in inspected constructor/log_event","snippet":"with open(self.jsonl_path, \"a\") as jsonl_fh: jsonl_fh.write(jsonl_line)","location":"logging_.py:81-116,145-158; commands.py:1844-1857"}
],
"reachability_verdicts":[
{"file_path":"src/superclaude/cli/swarm/lenses/refactor_find.py","line":53,"verdict":"reaches_sink","detail":"Lens constant copied at commands.py:929, substituted at :2141 and sent directly to reducer :2145-2157."},
{"file_path":"src/superclaude/cli/swarm/reduce.py","line":672,"verdict":"reaches_sink","detail":"Renders recommendation, stores ResultContract at :697, emits at :701-702. Disk policy :651 depends on output_dir/emit_to_disk, not log level. emit_contract:371-375 writes YAML."},
{"file_path":".dev/troubleshoot/bug-swarm-refactor-find-recommends-unavailable-20261123170314/stub-run/return-contract.yaml","line":64,"verdict":"reaches_sink","detail":"Actual parent-captured stub CLI artifact includes stale command, literal existing-review and three final paths. Stub only, not a paid/live transport. Parent bytes: event log 1559, contract 4221."}
],
"degraded":false,
"provenance":"One Augment query IronbellyOrg/IronClaude master; Read relevant sources; no .env read, no shell or writes by worker. Parent canonicalized descriptive config_type/verdict strings to documented enums while preserving meanings here. Recommendation is a direct contract artifact independent of log-level control."
}
