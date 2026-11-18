"""The default review panel is chosen by the pointer file review-default.json, not by a file name in code."""

from __future__ import annotations

import json
import shutil
from pathlib import Path

import pytest

from superclaude.cli.review import panel as pnl

DATA = Path(pnl.__file__).parent / "data"


@pytest.fixture(autouse=True)
def _no_user_overrides(tmp_path, monkeypatch):
    """No project or home review-panel.json and no environment variable can shadow the packaged default."""
    monkeypatch.setenv("HOME", str(tmp_path / "home"))
    monkeypatch.delenv("SUPERCLAUDE_REVIEW_PANEL", raising=False)
    monkeypatch.chdir(tmp_path)


@pytest.fixture
def data_copy(tmp_path, monkeypatch):
    """A temporary copy of the packaged data folder that the loader reads instead of the real one."""
    root = tmp_path / "pkg"
    shutil.copytree(DATA, root / "data")
    monkeypatch.setattr(pnl.resources, "files", lambda _package: root)
    return root / "data"


def _point(data_copy, **fields):
    ptr = {"schema": "review-default/1", "template": "wonsol", **fields}
    (data_copy / "review-default.json").write_text(json.dumps(ptr))


def test_default_resolves_to_a_template_by_reference():
    name = json.loads((DATA / "review-default.json").read_text())["template"]
    assert pnl.default_template_name() == name
    assert pnl.load_panel()["template_id"] == name == "wonsol"


@pytest.mark.parametrize(
    "env, models, stand_ins",
    [
        (
            "anthropic-only",
            ["claude-sonnet-5-5", "claude-haiku-5-5", "claude-haiku-5-5"],
            [False, True, True],
        ),
        (
            "gateway",
            ["muse-wonder-1.0", "gpt-6.1-sol", "muse-ember-1.0"],
            [False, False, False],
        ),
    ],
)
def test_three_reviewer_default_resolves_in_both_environments(env, models, stand_ins):
    panel = pnl.load_panel()
    assert sum(s["count"] for s in panel["slots"]) == 3
    for run_id in ("t1", "t2", "t3"):
        out = pnl.resolve(panel, pnl.load_tiers(), env, run_id)
        assert [r["reviewer_id"] for r in out["reviewers"]] == [
            "t5a-1",
            "t5b-1",
            "t5c-1",
        ]
        assert [r["model"] for r in out["reviewers"]] == models
        assert [r["stand_in"] for r in out["reviewers"]] == stand_ins


def test_editing_the_pointer_switches_the_default_with_no_code_change(data_copy):
    assert pnl.load_panel()["template_id"] == "wonsol"
    _point(data_copy, template="classic")
    panel = pnl.load_panel()
    assert panel["template_id"] == "classic"
    assert sum(s["count"] for s in panel["slots"]) == 4


@pytest.mark.parametrize(
    "fields",
    [
        {"template": "no-such-template"},
        {"template": "Bad Name"},
        {"template": 5},
        {"schema": "review-default/2"},
    ],
)
def test_a_bad_pointer_is_rejected_and_names_the_pointer_file(data_copy, fields):
    _point(data_copy, **fields)
    with pytest.raises(ValueError, match="review-default.json"):
        pnl.load_panel()


def test_a_project_panel_file_still_overrides_the_pointer(tmp_path):
    (tmp_path / ".superclaude").mkdir()
    own = pnl.load_panel("@live7")
    own["template_id"] = "from-project"
    (tmp_path / ".superclaude" / "review-panel.json").write_text(json.dumps(own))
    assert pnl.load_panel()["template_id"] == "from-project"
