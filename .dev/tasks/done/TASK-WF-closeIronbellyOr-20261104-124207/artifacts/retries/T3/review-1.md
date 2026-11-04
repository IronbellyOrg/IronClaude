start=235bb29732e5681bbc6e23842700f369c166175e tree=64a175a16efc50f8cf29fb6233c3f53a93846115
T3.AC1 met docs/getting-started/installation.md:354; ./artifacts/t3-checks.log:1-2
T3.AC2 met docs/getting-started/installation.md:362-364
T3.AC3 unmet docs/getting-started/installation.md:398 (F1.1)
T3.AC4 met ./artifacts/t3-checks.log:10-12
F1.1 sev=blocking trigger=B1 ac=T3.AC3 at=docs/getting-started/installation.md:398 anchor="the `ledger` option set to `false`" chk=y,n,n,n family=ledger-off-wording fix=Write "set Ponytail's `ledger` option to `false` in `/config` (the row is titled \"Task board\")" first=A1 origin=new: The block says "to off" and never uses the literal `false` the AC and brief require for the ledger option.
F1.2 sev=blocking trigger=B4 ac=scope at=docs/getting-started/installation.md:413-415 anchor="do not only run `claude plugin uninstall` (the next install reinstalls it); a project `.claude/settings.json` that enables it wins over the user value." chk=n,n,n,y family=optout-incomplete fix=Add the uninstall warning and the project-override sentence after "as `true`." first=A1 origin=new: The opt-out paragraph keeps only the "do not delete the key" half.
F1.3 sev=blocking trigger=B4 ac=scope at=docs/getting-started/installation.md:385-390 anchor="An Orca worker may mention that offer in its reply; it changes no settings by itself." chk=n,n,n,y family=statusline-note-incomplete fix=Add "it changes no settings by itself" after "may mention the offer in its reply" first=A1 origin=new: The worker sentence is present, but the "changes no settings by itself" clause is not.
F1.1 resolved
F1.2 resolved
F1.3 resolved
