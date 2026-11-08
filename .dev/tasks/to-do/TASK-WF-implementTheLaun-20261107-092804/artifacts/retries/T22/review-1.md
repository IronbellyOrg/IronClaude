c3ed6e792050896f66c62b4b57c965eb7909edf1 eaffc48e0554e53ff6ef798cc7411dd7399cedef
T22.AC1 met docs/designs/sc-issue-launch-level-hook.md:1
T22.AC2 met docs/designs/sc-issue-claim-pipeline-flag.md:1
T22.AC3 met ./artifacts/final-check.md:1
T22.AC4 met ./artifacts/final-check.md:1
T22.AC5 met ./artifacts/final-check.md:1
F1.1 sev=blocking trigger=B2 ac=scope at=docs/designs/sc-issue-launch-level-hook.md:1 anchor="the U1 ship gate of design section 7" chk=n,y,n,n family=docs-stale-claim fix=reword every ship-gate sentence to attribute item 1 and item 5 to U1 and OB-H2 and OB-H3 to sections 11 and 14 first=A1 origin=new: the ship-gate sentence in the five documents and the design attributed OB-H2 and OB-H3 to U1 and dropped item 5.
F1.2 sev=blocking trigger=B2 ac=scope at=docs/designs/sc-issue-claim-pipeline-flag.md:133 anchor="It does not claim the hook is registered or effective" chk=n,y,n,n family=docs-stale-claim fix=update the stale statements of the pipeline-flag design (section 6 text and heading, 8.4 step 3, files table, line 3 status, line 30, output contract) first=A1 origin=new: several statements still described the old behaviour and named enforcement_status().
F1.3 sev=blocking trigger=B2 ac=scope at=docs/user-guide/commands.md:381 anchor="enforces the level" chk=n,y,n,n family=docs-stale-claim fix=say it checks the listed routes and is not universal prevention first=A1 origin=new: the user guide sentence overstated the guard.
F1.4 sev=minor trigger=none ac=scope at=docs/designs/sc-issue-launch-level-hook.md:1 anchor=the claim refuses when the guard is missing or not effective chk=n,n,n,n family=docs-stale-claim fix=add the claim-process-only limit first=A1 origin=new: fixed in the same pass.
F1.5 sev=minor trigger=none ac=scope at=docs/designs/sc-issue-launch-level-hook.md:1 anchor=IR-1 to IR-7 detection chk=n,n,n,n family=docs-stale-claim fix=say IR-1, IR-2 and IR-4 to IR-7 first=A1 origin=new: fixed in the same pass.
