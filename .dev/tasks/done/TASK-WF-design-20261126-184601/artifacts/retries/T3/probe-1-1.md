8e79a88ec2e1170266fa505454e68c1d7dc3b4e5
family version-form-extra-tokens: the `--version` spelling of the version verb drops every token after it, so extra words are accepted while the `version` spelling refuses them.
command: grep -n -F -e --version src/superclaude/skills/sc-git-protocol/scripts/vcs_rules.py tests/vcs/test_rules.py
before:
src/superclaude/skills/sc-git-protocol/scripts/vcs_rules.py:270:    # `git version` and the `--version` form; no other option.
src/superclaude/skills/sc-git-protocol/scripts/vcs_rules.py:305:    verb = "version" if words[0] == "--version" else words[0]
src/superclaude/skills/sc-git-protocol/scripts/vcs_rules.py:311:    rest = [] if words[0] == "--version" else words[1:]
tests/vcs/test_rules.py:76:        ["--version"],
coupled sites: the `rest` computation in validate_argv and the refusal test list in tests/vcs/test_rules.py.
after:
src/superclaude/skills/sc-git-protocol/scripts/vcs_rules.py:270:    # `git version` and the `--version` form; no other option.
src/superclaude/skills/sc-git-protocol/scripts/vcs_rules.py:305:    verb = "version" if words[0] == "--version" else words[0]
tests/vcs/test_rules.py:76:        ["--version"],
tests/vcs/test_rules.py:116:        ["--version", "--build-options"],
tests/vcs/test_rules.py:117:        ["--version", "x"],
