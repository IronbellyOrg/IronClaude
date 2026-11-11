070b5c110c47c9b4b6c478c2cdfd97ded5908394
family ac5-xdg-not-exercised: defect form: an AC names a temporary XDG_STATE_HOME but no test sets it
command: grep -n -F -e XDG_STATE_HOME -- tests/observe/test_commands.py src/superclaude/cli/observe/commands.py
before:
coupled sites: commands.py run_interactive state_directory default (state_dir()), tests/observe/test_commands.py interactive tests
after:
tests/observe/test_commands.py:476:    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path))
