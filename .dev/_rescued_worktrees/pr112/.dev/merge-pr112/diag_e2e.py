import sys, os, json, tempfile, pathlib
sys.path.insert(0, os.getcwd())
from unittest.mock import patch
import importlib
m = importlib.import_module("tests.sprint.test_e2e_success")

tmp = pathlib.Path(tempfile.mkdtemp())
config = m._make_config(tmp)
factory = m._popen_factory_all_pass(config)
with (
    patch("superclaude.cli.sprint.executor.shutil.which", return_value="/usr/bin/claude"),
    patch("superclaude.cli.pipeline.process.subprocess.Popen", side_effect=factory),
    patch("superclaude.cli.pipeline.process.os.setpgrp"),
    patch("superclaude.cli.sprint.notify._notify"),
):
    m.execute_sprint(config)

events = [json.loads(l) for l in config.execution_log_jsonl.read_text().strip().split("\n")]
print("total events =", len(events))
for i, e in enumerate(events):
    extra = {k: e[k] for k in ("phase", "phase_name", "outcome", "status") if k in e}
    print(f"  [{i}] {e['event']:18} {extra}")
