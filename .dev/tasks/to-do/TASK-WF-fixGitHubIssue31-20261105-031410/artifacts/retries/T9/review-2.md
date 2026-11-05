0b3543fbe4c8765d9e8e6be1775ba8b430e9410c tree=d9a9fccd31b17e52f71e8b4a9ea5ab8b865aa7ca
AC marks (reviewer, summary): T9.AC1 unmet src/superclaude/skills/ccsession-tag/README.md:258,299,353,232,308,286 (F2.1-F2.6); T9.AC2 met ./artifacts/t9-readme-checks.log
F1.1 resolved
F1.2 resolved
F1.3 resolved
F1.4 resolved
F1.5 resolved
F2.1 sev=blocking trigger=B2 ac=T9.AC1 at=src/superclaude/skills/ccsession-tag/README.md:258 anchor=src/superclaude/skills/ccsession-tag/ccsession-orca:246 chk=n,y,n,n family=readme-universal-claim fix=drop "the prompt is Claude's last argument" first=A2 origin=new: Orca's arguments keep their own order; only a typed message is appended last.
F2.2 sev=blocking trigger=B2 ac=T9.AC1 at=src/superclaude/skills/ccsession-tag/README.md:299 anchor=src/superclaude/skills/ccsession-tag/ccsession:1853 chk=n,y,n,n family=readme-universal-claim fix=say ccsession-orca removes both first=A2 origin=new: a direct ccsession run passes both variables on.
F2.3 sev=blocking trigger=B2 ac=T9.AC1 at=src/superclaude/skills/ccsession-tag/README.md:353 anchor=src/superclaude/skills/ccsession-tag/ccsession:1556 chk=n,y,n,n family=readme-universal-claim fix=describe the "; ...@LIMIT@..." form only first=A2 origin=new: a @LIMIT@ outside a "; " part is left as written.
F2.4 sev=blocking trigger=B2 ac=T9.AC1 at=src/superclaude/skills/ccsession-tag/README.md:232 anchor=src/superclaude/skills/ccsession-tag/ccsession:1499 chk=n,y,n,n family=readme-universal-claim fix=add standard error first=A2 origin=new: --ask also needs standard error on a terminal.
F2.5 sev=blocking trigger=B2 ac=T9.AC1 at=src/superclaude/skills/ccsession-tag/README.md:308 anchor=src/superclaude/skills/ccsession-tag/ccsession:1824-1827 chk=n,y,n,n family=readme-universal-claim fix=add the conversation-gone case first=A2 origin=new: a saved name whose conversation is gone starts a new session.
F2.6 sev=blocking trigger=B2 ac=T9.AC1 at=src/superclaude/skills/ccsession-tag/README.md:286 anchor=src/superclaude/skills/ccsession-tag/ccsession:1818-1821 chk=n,y,n,n family=readme-universal-claim fix=drop "never" first=A2 origin=new: the label is checked against saved files only, the name is saved by the hook, the loop stops at -99.
