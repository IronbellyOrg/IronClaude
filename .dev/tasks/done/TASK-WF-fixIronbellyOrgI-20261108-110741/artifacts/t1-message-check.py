import subprocess, sys
from pathlib import Path
import pytest
sys.path.insert(0, "/home/coder/workspaces/worktrees/IronClaude/issue-443/tests/unit")
import test_ccsession_tiers as t

class P:  # a refused launch
    returncode = 1
    stdout = ""
    stderr = "[ccsession] ERROR: refused"

@pytest.mark.parametrize("port,expect", [(40000, "shim_base_port=40000"), (None, "shim_base_port=unobserved")])
def test_message(tmp_path, monkeypatch, port, expect):
    seen = {}
    def fake_run(cmd, **kw):
        seen["env"] = kw["env"]
        return P()
    monkeypatch.setattr(subprocess, "run", fake_run)
    with pytest.raises(AssertionError) as e:
        t._real_launch(tmp_path, port, upstream="http://127.0.0.1:33361")
    msg = str(e.value)
    print(msg.splitlines()[0])
    assert "gateway_port=33361" in msg and expect in msg and "upstream=http://127.0.0.1:33361" in msg and "[ccsession] ERROR: refused" in msg
    assert seen["env"]["ANTHROPIC_BASE_URL"] == "http://127.0.0.1:33361"
    assert ("CC_SHIM_PORT" in seen["env"]) == (port is not None)

def test_bad_url(tmp_path, monkeypatch):
    monkeypatch.setattr(subprocess, "run", lambda cmd, **kw: P())
    with pytest.raises(AssertionError) as e:
        t._real_launch(tmp_path, 1, upstream="http://127.0.0.1:notaport")
    assert "gateway_port=unobserved" in str(e.value)
