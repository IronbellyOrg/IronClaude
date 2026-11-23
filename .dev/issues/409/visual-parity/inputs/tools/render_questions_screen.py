import json, sys
from superclaude.cli.observe.collector import Collector
from superclaude.cli.observe.adapter import LiveSource
from superclaude.cli.observe.render import screen_lines
from superclaude.cli.observe.terminal import resolve_policy
from superclaude.cli.observe.view import Session, Key, apply_key, build_view
from tests.observe.conftest import (FakeClock, FakeDiscover, FakeRunner, make_envelope, make_rows,
    make_question_rows, make_question_envelope, question_payload, routed_runner_responses, QRUN)
clock = FakeClock()
rows = make_rows(6, 2)
for r, d in zip(rows, ["w-001","w-002","w-003","w-004","w-005","w-006"]):
    r["dispatchId"] = d; r["resource"] = {"worktreeId": "wt-" + d[-1]}
q = []
for i, (d, t) in enumerate([("w-001","Choose schema compatibility policy"),("w-002","Confirm deployment window"),("w-003","Name the release reviewer")]):
    q += make_question_rows(1, start=i, payload=question_payload(d, t))
worker = (0, json.dumps(make_envelope(rows, total=6)))
msg = (0, json.dumps(make_question_envelope(q)))
runner = FakeRunner([], [routed_runner_responses(worker, msg)])
col = Collector(LiveSource(runner, FakeDiscover([], "/opt/fake/orca")), clock, run_id=QRUN, questions=True, link=True)
result = col.run_once()
sess = Session()
view = build_view(result, sess, clock)
sess, _ = apply_key(sess, Key("text","n"), view, clock)
width = int(sys.argv[1]); height = int(sys.argv[2])
for l in screen_lines(build_view(result, sess, clock), resolve_policy({}, "utf-8", {"ascii": False}, width, height)):
    print(l)
