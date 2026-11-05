```json
{"branch":"B","query_target":"terminal output of install_user_setup messages (main.py install and update)","hits":[
{"config_path":"src/superclaude/cli/main.py","config_type":"pipeline_config","framework":"click.echo (stdout, unconditional)","effective_level":"none (always printed)","snippet":"setup_success, setup_message = install_user_setup(force=force)\nclick.echo(setup_message)","location":"/home/coder/workspaces/worktrees/IronClaude/issue-330-ponytail-plugin/src/superclaude/cli/main.py:236-237"},
{"config_path":"src/superclaude/cli/main.py","config_type":"pipeline_config","framework":"click.echo (stdout, unconditional)","effective_level":"none (always printed)","snippet":"setup_success, setup_message = install_user_setup(force=True)\nclick.echo(setup_message)","location":"/home/coder/workspaces/worktrees/IronClaude/issue-330-ponytail-plugin/src/superclaude/cli/main.py:404-405"},
{"config_path":"src/superclaude/cli/install_user_setup.py","config_type":"pipeline_config","framework":"return-tuple aggregation","effective_level":"none","snippet":"return all(ok for ok, _ in results), \"\n\".join(msg for _, msg in results)","location":"/home/coder/workspaces/worktrees/IronClaude/issue-330-ponytail-plugin/src/superclaude/cli/install_user_setup.py:380-387"}],
"reachability_verdicts":[{"file_path":"src/superclaude/cli/install_user_setup.py","line":186,"verdict":"reaches_sink"}],"degraded":true}
```
No logging config, LOG_LEVEL/DEBUG env var or quiet flag affects install/update; only `doctor --verbose` exists (main.py:473).
