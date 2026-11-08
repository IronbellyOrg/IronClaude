2912b48a697fa9d54be994797c7af6d1262ebe85 60be49f8081f14915255cf5e303419cf76cc5422
T2.AC1 met tests/hooks/fixtures/launch_level/ob_h1/:item1-subagent-ids.json..item9-tool-names.json,README.md,log-only-probe.sh
T2.AC2 met .dev/tasks/to-do/TASK-WF-implementTheLaun-20261107-092804/artifacts/t2-test.log:40
T2.AC3 met tests/hooks/test_launch_level_observations.py:65-68
F1.1 sev=blocking trigger=B2 ac=scope at=tests/hooks/fixtures/launch_level/ob_h1/README.md:5 anchor=tests/hooks/fixtures/launch_level/live_probe.py:63-77 chk=n,y,n,n family=readme-live-probe-claim fix=reword README line 5 to say what live_probe.py records and what it cannot capture first=A1 origin=new: README says live_probe.py captures selector results only and does not overlap the items, but live_probe.py:63-77 records session_id, agent_id, agent_type, tool_name and tool_input_keys from the actual hook input.
