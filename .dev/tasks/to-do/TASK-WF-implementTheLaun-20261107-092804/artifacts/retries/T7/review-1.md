b9af89d68d7c18af63eeb5b0e513b9a01a44cc38 ac747634ec2e6920e6ff10a441cf71c4d0bd99e5
T7.AC1 met src/superclaude/hooks/scripts/launch-level-guard.sh:495-505
T7.AC2 met src/superclaude/hooks/scripts/launch-level-guard.sh:522-542
T7.AC3 met src/superclaude/hooks/scripts/launch-level-guard.sh:419-420
T7.AC4 met src/superclaude/hooks/scripts/launch-level-guard.sh:455-478
T7.AC5 met tests/hooks/test_launch_level_guard.py:1
F1.1 sev=blocking trigger=B4 ac=scope at=src/superclaude/hooks/scripts/launch-level-guard.sh:437 anchor="one of the wrapper basenames `env sudo nohup exec" chk=n,n,n,y family=g3-wrapper-basename fix=match wrappers and shells by ${w##*/} and add oracle rows for path-qualified wrappers covers="one of the wrapper basenames `env sudo nohup exec" first=A1 origin=new: the wrapper and shell skip compared the raw word, so /usr/bin/env git ci escaped the UNKNOWN class.
F1.2 sev=note trigger=none ac=scope at=src/superclaude/hooks/scripts/launch-level-guard.sh:437 anchor=docs/designs/sc-issue-launch-level-hook.md:149 chk=n,n,n,n family=g3-assignment-value fix=none first=A1 origin=new: A="x y" git ci exits 0 because quote removal makes y the command word; the design does not require a block.
