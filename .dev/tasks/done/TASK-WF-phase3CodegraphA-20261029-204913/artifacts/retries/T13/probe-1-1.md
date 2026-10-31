9c7fb5c2f278ff95bb7ac6a7340852a54987fd3c
family=doc-accuracy
defect form: helper or record text that names a different shell than the runner uses
command: grep -n -F -e "/bin/sh" -e "SHELL" -- .dev/tasks/to-do/TASK-WF-phase3CodegraphA-20261029-204913/artifacts/t13-mkrun.py .dev/codegraph-migration/experiments/P3-T11-smoke.md .dev/codegraph-migration/decisions/P3X-execution-log.md
before:
.dev/tasks/to-do/TASK-WF-phase3CodegraphA-20261029-204913/artifacts/t13-mkrun.py:5:`/bin/sh -c`; a leading `@` only suppresses the echo; `$$` becomes `$`.
.dev/tasks/to-do/TASK-WF-phase3CodegraphA-20261029-204913/artifacts/t13-mkrun.py:16:SHELL = next((ln.split(":=", 1)[1].strip() for ln in lines if re.match(r"^SH
.dev/tasks/to-do/TASK-WF-phase3CodegraphA-20261029-204913/artifacts/t13-mkrun.py:39:    rc = subprocess.run([SHELL, "-c", cmd]).returncode
.dev/codegraph-migration/experiments/P3-T11-smoke.md:15:`make` is not installed on this host (`/bin/bash: make: command not found`, exit 127). The two recipes w
.dev/codegraph-migration/decisions/P3X-execution-log.md:78:| 2026-10-31 | T13 | Run the `sync-dev` and `verify-sync` recipes with a small runner (`artifacts/t13
coupled sites: smoke file check (1) paragraph; decision-log T13 make-substitute row
after:
.dev/tasks/to-do/TASK-WF-phase3CodegraphA-20261029-204913/artifacts/t13-mkrun.py:5:`<SHELL> -c`, where SHELL is the Makefile's `SHELL :=` value (default `/bin/s
.dev/tasks/to-do/TASK-WF-phase3CodegraphA-20261029-204913/artifacts/t13-mkrun.py:17:SHELL = next((ln.split(":=", 1)[1].strip() for ln in lines if re.match(r"^SH
.dev/tasks/to-do/TASK-WF-phase3CodegraphA-20261029-204913/artifacts/t13-mkrun.py:40:    rc = subprocess.run([SHELL, "-c", cmd]).returncode
.dev/codegraph-migration/experiments/P3-T11-smoke.md:15:`make` is not installed on this host (`/bin/bash: make: command not found`, exit 127). The two recipes w
.dev/codegraph-migration/decisions/P3X-execution-log.md:78:| 2026-10-31 | T13 | Run the `sync-dev` and `verify-sync` recipes with a small runner (`artifacts/t13
