0aab14fa4c4e70147b80d5df0fffdf7ce2aadc13
family=dimension-sources
defect form: a SessionRow dimension filled from an Orca or contract field that research/09 Gap 2 does not list as its source.
command: grep -n -E 'lifecycle=|health=|result=|freshness=|freshness_age_s=|evidence_packet=|phase=|approval=|admission=|tests_review=' -- src/superclaude/cli/sweep/classify.py
before-output (state reviewed in review 1):
906 lifecycle=_lifecycle(o) [outcome, liveness, status]; 907 health=_health(o, contract) [contract failed, orca outcome failed, liveness live/exited]; 908 result=_result(contract) [contract worker_status; blocked prints null: listed]; 936-937 freshness / freshness_age_s from the transcript last activity [listed: transcript time for a person-started session]; evidence_packet, phase, approval, admission, tests_review not set (defaults: correct).
coupled sites: _lifecycle (lines 801-807) and _health (810-817) only; result and freshness match their Gap 2 rows.
after: _lifecycle uses the Orca outcome only; _health uses the failed contract only; call site 907 passes the contract only.
