adc880232c23f71b22a83dfb626af4bb6f9a78e8
family status-retry: a retry command is printed only when the caller supplies the prompt
command: git grep -n -e "prompts" -e "argv\": None" -e "launch-prompts" -- src/superclaude/cli/issue_watch/cycle.py src/superclaude/cli/issue_watch/cli.py
before: cycle.py status_report takes prompts=None and the CLI passes none; no launch keeps a prompt
coupled sites: cycle.py _launch (writes the prompt before the launch call), cycle.py status_report (reads it), cli.py status text output, tests/issue_watch/test_cli.py status tests, tests/issue_watch/test_crash_injection.py file listing
after: cycle.py _launch calls _remember_prompt; status_report reads launch-prompts.json; the CLI prints the stored command
