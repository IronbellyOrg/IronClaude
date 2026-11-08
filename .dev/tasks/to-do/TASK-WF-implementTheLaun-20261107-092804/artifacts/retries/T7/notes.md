b9af89d68d7c18af63eeb5b0e513b9a01a44cc38
A1 r1-1 F1.2 note ac=scope at=src/superclaude/hooks/scripts/launch-level-guard.sh:437 chk=n,n,n,n: A="x y" git ci exits 0 because quote removal makes y the command word; the design does not require a block.
A2 r1-2 note ac=scope at=src/superclaude/hooks/scripts/launch-level-guard.sh:437 chk=n,n,n,n: option values after a wrapper are not skipped (env -u X git ci, timeout -s KILL 30 git ci, bash -x git ci pass); the design does not ask for it; affects only UNKNOWN-class subcommands because G1 still catches commit, push and merge.
