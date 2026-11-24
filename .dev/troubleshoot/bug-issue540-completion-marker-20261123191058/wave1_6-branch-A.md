<!-- Branch A schema: branch, query_target, hits(file_path,line,call_type,framework,level,snippet,richness,distance_to_symptom,captured_bytes), degraded. -->
{
"branch":"A",
"query_target":"src/superclaude/cli/swarm/commands.py::run_cmd:2095-2178 and immediate logger/state calls",
"hits":[
{"file_path":"src/superclaude/cli/swarm/commands.py","line":2173,"call_type":"print","framework":"click.echo","level":null,"snippet":"click.echo(f\"swarm run: dispatched job (mode={mode}, workers=..., results=...)\")","richness":"minimal","distance_to_symptom":"in_function","captured_bytes":null},
{"file_path":"src/superclaude/cli/swarm/dispatch.py","line":497,"call_type":"logger_call","framework":"custom Logger.log_event / EventRecord","level":null,"snippet":"logger.log_event(EventRecord(event_type=\"wave_transition\", payload={\"from\":\"dispatching\",\"to\":\"dispatched\",\"results_collected\":len(results),\"success_count\":success_count}))","richness":"rich","distance_to_symptom":"immediate_callee_before_completion_continuation","captured_bytes":null},
{"file_path":"src/superclaude/cli/swarm/logging_.py","line":156,"call_type":"logger_call","framework":"custom JSONL sink","level":null,"snippet":"with open(self.jsonl_path, \"a\") as jsonl_fh: jsonl_fh.write(jsonl_line)","richness":"rich","distance_to_symptom":"immediate_logger_implementation","captured_bytes":1559},
{"file_path":"src/superclaude/cli/swarm/logging_.py","line":158,"call_type":"logger_call","framework":"custom Markdown sink","level":null,"snippet":"with open(self.md_path, \"a\") as md_fh: md_fh.write(md_line)","richness":"rich","distance_to_symptom":"immediate_logger_implementation","captured_bytes":999}
],
"degraded":false,
"observations":[
"commands.py:2095-2178 contains one stdout diagnostic, no logger or exception handler; reduces, writes terminal state, prints summary, exits. Summary does not report marker presence/path/status/publication.",
"reduce.py:677-704 constructs contract, emits at :702, returns at :704; no marker call or marker diagnostic.",
"reduce.py:371-375 atomically writes contract (parent measured4825 bytes), not a log stream.",
"commands.py:2164-2169 and :790-796 call state.py:164-174 to timestamp and atomically replace state (parent measured104 bytes), not marker publication and not log bytes.",
"commands.py:1844-1856 binds log sinks; logging_.py:145-158 fills UTC event timestamps. Captured bytes belong to whole streams, not individual events."
],
"pending_observations":["stdout and individual event byte counts unobserved (null)","Branch B owns reachability/filtering; nonempty streams alone do not prove marker publication"]
}
