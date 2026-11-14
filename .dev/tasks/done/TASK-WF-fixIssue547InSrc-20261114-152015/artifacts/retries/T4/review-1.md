d74617ddffa12304cba21c44149e1f39d6ea0e18
tree=43120bf304265c825f55889973e65544050e6a82
AC marks: T4.AC1..AC4 met (reviewer a1)
F1.1 sev=blocking trigger=B4 ac=scope at=src/superclaude/cli/sweep/probes.py:980-986 anchor="Add a one-line `# shortcut:` comment noting that a filter named only in a submodule's own config is closed by `--ignore-submodules=all`, not by this check" chk=n,n,n,y family=shortcut-comment fix=add one # shortcut: line first=A1 origin=new: the limit is only in the docstring.
F1.2 sev=blocking trigger=B4 ac=scope at=src/superclaude/cli/sweep/probes.py:68-80,988-995 anchor="Name the three template tuples as module constants next to `ALLOWED_GIT` entries by indexing (`ALLOWED_GIT[1]`, `[2]`, `[3]`), not by repeating the literals" chk=n,n,n,y family=named-constants fix=add CONFIG_LIST, LS_FILES, CHECK_ATTR constants first=A1 origin=new: the helper indexes ALLOWED_GIT inline.
