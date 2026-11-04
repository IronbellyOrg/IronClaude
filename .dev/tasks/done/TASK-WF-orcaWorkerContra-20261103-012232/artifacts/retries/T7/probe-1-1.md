feef7cef998a2b6175e6e9063e9cc2bc9a3dd0eb
## family=incomplete-call-site-enumeration (F1.1)
defect form: the trace states its list of depth-check call sites is complete ("No other code path calls the check.") while the bundle has a call site the list omits.
search: grep -n -F -e "No other code path" -e "call sites are" -- .dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261103-012232/artifacts/ac-0.7-depth-trace.md
before:
.dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261103-012232/artifacts/ac-0.7-depth-trace.md:30:Every call of `resolveChildDispatchDepth`, `createDispatchContext` and `createStartingWorkerDispatch` in `out/` is in `BUNDLE` (a recursive `grep -rln` for the three names lists only that file). The call sites are `BUNDLE:650` col 3344 (`createDispatchContext`), `BUNDLE:2443` col 321 (`createStartingWorkerDispatch`), `BUNDLE:2548` col 7735 (dispatch dry run), `BUNDLE:578` col 24175 and `BUNDLE:590` col 23752 (worker start). No other code path calls the check.
coupled sites: the per-call table rows (worker-start, dispatch, low-level dispatch) cite the same call sites and stay correct; the enumeration was re-derived mechanically by a regex scan of BUNDLE for `.resolveChildDispatchDepth(`, `.createDispatchContext(` and `.createStartingWorkerDispatch(`, which gives seven call sites: 578:24175, 590:23752 (createStartingWorkerDispatch), 650:3344, 2443:321, 2548:7735 (resolveChildDispatchDepth), 2548:9095, 2548:19170 (createDispatchContext). The old sentence also labelled 650:3344 and 2443:321 by the wrong function (they are the resolveChildDispatchDepth calls inside createDispatchContext and createStartingWorkerDispatch) and omitted 2548:9095 and 2548:19170.
after:
after: (no hit: the completeness sentence is replaced by the seven-row call-site table)
