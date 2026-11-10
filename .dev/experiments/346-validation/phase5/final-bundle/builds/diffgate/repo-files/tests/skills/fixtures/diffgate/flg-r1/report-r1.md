# Spec panel critique

review: 1 of 3

Full review of the document.

## Diffgate findings

FINDING R1.1 sev=critical at=5 anchor="dispatches each command as one worker task" :: the brief does not say what the worker receives
FINDING R1.2 sev=major at=9 anchor="through the ask command" outcome="a worker waits forever on an unanswered question" :: no timeout
FINDING R1.3 sev=major at=13 anchor="with worker_done and a report path" outcome="relative paths break the coordinator read" :: path form open
FINDING R1.4 sev=critical at=17 anchor="is retried once by the coordinator" :: retry identity undefined
FINDING R1.5 sev=minor at=21 anchor="a session that runs one command" :: concurrency wording
