8e79a88ec2e1170266fa505454e68c1d7dc3b4e5 tree=0333cd05e80463d302947341232aad212b284f98
T3.AC1 met tests/vcs/test_rules.py:25,79,96,127,137,177
T3.AC2 met src/superclaude/skills/sc-git-protocol/scripts/vcs_rules.py:1-358
F1.1 sev=blocking trigger=B4 ac=scope at=src/superclaude/skills/sc-git-protocol/scripts/vcs_rules.py:311 anchor="`version` (the `--version` form, no other option" chk=n,n,n,y family=version-form-extra-tokens fix=in validate_argv, when words[0] == "--version" raise ForbiddenArgv unless len(words) == 1, and add refusal cases to the refusal test first=A1 origin=new: `rest = [] if words[0] == "--version" else words[1:]` drops every token after `--version`; `["--version","--build-options"]` and `["--version","x"]` are accepted while `["version","x"]` is refused.
