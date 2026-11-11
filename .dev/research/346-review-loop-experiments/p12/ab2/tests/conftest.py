import json
import pathlib
import shutil
import sys

import pytest

AB = pathlib.Path("/tmp/claude-0/-home-user-IronClaude/a6884237-9a8e-5417-a03f-8e5a29d7c57f/scratchpad/p12/ab2")
SP = AB.parents[1]
P11 = SP/"p11"
sys.path.insert(0, str(AB))


@pytest.fixture()
def h(tmp_path, monkeypatch):
    import harness
    (tmp_path/"ab").mkdir()
    shutil.copy(AB/"decision.json", tmp_path/"ab"/"decision.json")
    monkeypatch.setattr(harness, "AB", tmp_path/"ab")
    monkeypatch.setattr(harness, "RUNS", tmp_path/"ab"/"runs")
    harness.RUNS.mkdir()
    monkeypatch.setenv("AB_TASKS_GLOB", str(tmp_path/"no-transcripts"/"*.output"))
    monkeypatch.setattr(harness, "TASKS_GLOB", str(tmp_path/"no-transcripts"/"*.output"))
    return harness
