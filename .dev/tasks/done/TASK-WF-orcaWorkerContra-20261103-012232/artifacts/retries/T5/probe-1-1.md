e39a3a458bb2c14a77712141e5f0812dbbaf0f36
## family=phrase-coverage (F1.1)
defect form: a phrase recorded for a rule in ./artifacts/t1-rule-phrases.md is not carried as data in tests/skills/test_worker_contract.py, so the test does not pin that rule's meaning.
search: grep -n -F -e "keeps it off workers" -- tests/skills/test_worker_contract.py .dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261103-012232/artifacts/t1-rule-phrases.md src/superclaude/core/WORKER-CONTRACT.md
before:
.dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261103-012232/artifacts/t1-rule-phrases.md:23:never-as-worker :: `/sc:agent`, `/sc:git`, `/sc:help`, `/sc:pm`, `/sc:spawn` and `/sc:swarm-wizard`, plus `/sc:pr-submit` while the answer to decision D3 keeps it off workers
src/superclaude/core/WORKER-CONTRACT.md:23:- **Never-as-worker list**: `/sc:agent`, `/sc:git`, `/sc:help`, `/sc:pm`, `/sc:spawn` and `/sc:swarm-wizard`, plus `/sc:pr-submit` while the answer to decision D3 keeps it off workers. ...
(no hit in tests/skills/test_worker_contract.py)
coupled sites: tests/skills/test_worker_contract.py RULE_PHRASES (the data table every phrase must be in); _check_never_as_worker and NEVER_AS_WORKER (the per-command list check, which stays); test_rule_check_fails_when_rule_removed (parametrized over RULE_PHRASES, so a new entry gets its negative check automatically). A full comparison of every recorded phrase against the test's string constants (AST walk) found this one phrase missing and every other phrase present.
after:
after: tests/skills/test_worker_contract.py:67:            "plus `/sc:pr-submit` while the answer to decision D3 keeps it off workers"
after: .dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261103-012232/artifacts/t1-rule-phrases.md:23:never-as-worker :: `/sc:agent`, `/sc:git`, `/sc:help`, `/sc:pm`, `/sc:spawn` and `/sc:swarm-wizard`, pl
after: src/superclaude/core/WORKER-CONTRACT.md:23:- **Never-as-worker list**: `/sc:agent`, `/sc:git`, `/sc:help`, `/sc:pm`, `/sc:spawn` and `/sc:swarm-wizard`, plus `/sc:pr-submit` while the answer to
after: AST comparison of every recorded phrase against the test's string constants: missing 0
