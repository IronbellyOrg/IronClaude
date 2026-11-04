start=68b48ccb40439194b11344ce2cb7c162dd96fc5e tree=7141e207013417b141ee7bdff64e128edf07ff3e
T4.AC1 met .dev/tasks/to-do/TASK-WF-closeIronbellyOr-20261104-124207/artifacts/m1-install-proof.md:64-77
T4.AC2 unmet CHANGELOG.md:11 (F1.1)
T4.AC3 met CHANGELOG.md:11
T4.AC4 met .dev/tasks/to-do/TASK-WF-closeIronbellyOr-20261104-124207/artifacts/t4-checks.log:14-19
F1.1 sev=blocking trigger=B2 ac=T4.AC2 at=CHANGELOG.md:11 anchor=/tmp/ponytail-src-t14b/mode-tracker.js:64 chk=n,y,n,n family=changelog-mode-scope fix=Replace "for the current project" with session wording; correct docs/getting-started/installation.md:401 the same way covers="how to change the mode (`off`, `lite`, `full`, `ultra`)" first=A1 origin=new: Upstream says plain mode switches "stay session-scoped" (mode-tracker.js:63-64); the flag is shared (register.tsx:95-96), so "for the current project" misstates the scope.
F1.1 resolved
