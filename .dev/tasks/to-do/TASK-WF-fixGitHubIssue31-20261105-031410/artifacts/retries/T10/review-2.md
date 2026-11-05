66f369dd3f39c96c30a26fe974e68d3669b2d070 tree=8590b4ffe7770ddb4e9d0af73b2c4d1cd8107afc
AC marks (reviewer, summary): T10.AC1 unmet CHANGELOG.md:22,26 (F2.1, F2.3); T10.AC2 unmet docs/testing/v5.0.0/user/D08-ccsession.md:5 (F2.2)
F1.1 resolved
F1.2 resolved
F1.3 resolved
F1.4 resolved
F1.5 resolved
F2.1 sev=blocking trigger=B2 ac=T10.AC1 at=CHANGELOG.md:22 anchor=src/superclaude/skills/ccsession-tag/ccsession:1557 chk=n,y,n,n family=changelog-claim-vs-source fix=state the exact @LIMIT@ rule first=A2 origin=new: with no limit only a hint with "; " before @LIMIT@ loses that part; any other hint prints @LIMIT@ as typed.
F2.2 sev=blocking trigger=B2 ac=T10.AC2 at=docs/testing/v5.0.0/user/D08-ccsession.md:5 anchor=git show HEAD:src/superclaude/skills/ccsession-tag/ccsession:1422 chk=n,y,n,n family=stale-line-numbers fix=say the numbers were already off before #315 first=A2 origin=new: the header said the numbers were taken before #315; they were already off at HEAD.
F2.3 sev=blocking trigger=B2 ac=T10.AC1 at=CHANGELOG.md:26 anchor=git show HEAD:src/superclaude/skills/ccsession-tag/ccsession-orca:48,61 chk=n,y,n,n family=changelog-claim-vs-source fix=drop "still" for print mode, --version, --help and subcommands first=A2 origin=new: at HEAD those asked first on a terminal.
