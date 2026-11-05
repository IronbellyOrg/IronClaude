9c7fb5c2f278ff95bb7ac6a7340852a54987fd3c tree=960e3a9f9fffd3fd5c939c05ac20b2b122efea60
T13.AC1 met: T13.AC1@CHANGELOG.md:33
T13.AC2 met: T13.AC2@.dev/tasks/to-do/TASK-WF-phase3CodegraphA-20261029-204913/artifacts/t13-sync.log:219
T13.AC3 met: T13.AC3@.dev/codegraph-migration/experiments/P3-T11-smoke.md:23
T13.AC4 met: T13.AC4@.dev/codegraph-migration/experiments/P3-T11-smoke.md:29
T13.AC5 met: T13.AC5@.dev/codegraph-migration/experiments/P3-T11-smoke.md:35
T13.AC6 met: T13.AC6@.dev/codegraph-migration/experiments/P3-T11-smoke.md:59
T13.AC7 met: T13.AC7@.dev/codegraph-migration/experiments/P3-T11-impact/return-contract.yaml:48
T13.AC8 met: T13.AC8@.dev/codegraph-migration/decisions/P3X-execution-log.md:81
F1.1 sev=blocking trigger=B2 ac=scope at=.dev/tasks/to-do/TASK-WF-phase3CodegraphA-20261029-204913/artifacts/t13-mkrun.py:5 anchor=.dev/tasks/to-do/TASK-WF-phase3CodegraphA-20261029-204913/artifacts/t13-mkrun.py:5 chk=n,y,n,n family=doc-accuracy fix=say each line runs in the Makefile's SHELL (default /bin/sh) first=A1 origin=new: the docstring says each recipe line runs in /bin/sh -c; the code runs the Makefile's SHELL (/bin/bash).
F2.1 sev=minor trigger=none ac=scope at=.dev/codegraph-migration/experiments/P3-T11-smoke.md:97 anchor=.dev/codegraph-migration/experiments/P3-T11-smoke.md:94 chk=n,n,n,n family=smoke-coverage fix=after merge and superclaude install, re-run /sc:troubleshoot once first=A1 origin=new: the real /sc:troubleshoot path loaded the stale installed skill; tier1-callers.md evidence comes only from the dev-copy run.
