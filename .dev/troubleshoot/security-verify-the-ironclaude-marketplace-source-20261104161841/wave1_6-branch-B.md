```json
{"branch":"B","query_target":"install_plugins message path and claude subprocess output","hits":[
{"config_path":"src/superclaude/cli/main.py","config_type":"pipeline_config","framework":"click","effective_level":"unconditional (stdout)","snippet":"click.echo(setup_message)","location":"src/superclaude/cli/main.py:236-237"},
{"config_path":"src/superclaude/cli/main.py","config_type":"pipeline_config","framework":"click","effective_level":"unconditional (stdout)","snippet":"click.echo(setup_message)","location":"src/superclaude/cli/main.py:404-405"},
{"config_path":"src/superclaude/cli/install_user_setup.py","config_type":"pipeline_config","framework":"none","effective_level":"every message joined","snippet":"\"\\n\".join(msg for _, msg in results)","location":"src/superclaude/cli/install_user_setup.py:393"},
{"config_path":"src/superclaude/cli/install_user_setup.py","config_type":"pipeline_config","framework":"subprocess","effective_level":"captured, discarded","snippet":"subprocess.run(..., capture_output=True, ...); only returncode read","location":"src/superclaude/cli/install_user_setup.py:363-372"}],
"reachability_verdicts":[{"file_path":"src/superclaude/cli/install_user_setup.py","line":380,"verdict":"reaches_sink"},{"file_path":"src/superclaude/cli/install_user_setup.py","line":363,"verdict":"filtered_out"}],"degraded":true}
```
