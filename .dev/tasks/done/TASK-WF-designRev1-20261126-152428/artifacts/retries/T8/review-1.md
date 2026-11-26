350491022cacf81329f71e46bdaadd2a48c23ca6 tree=f1b13a36cc0bab0462e7cabcc6fc0c204b9c175f
AC marks: T8.AC1 met, T8.AC2 met, T8.AC3 unmet (reviewer r1-1)
F1.1 sev=blocking trigger=B1 ac=T8.AC3 at=.dev/issues/837/audit/IronHands-CLI.md:146 anchor=No command in the file is a write chk=y,n,n,n family=write-command-in-record fix=remove the three DELETE rows of the Revert commands section first=A1 origin=new: Lines 146-148 hold gh api --method DELETE commands in a table of commands, although the AC says no command in the file is a write.
