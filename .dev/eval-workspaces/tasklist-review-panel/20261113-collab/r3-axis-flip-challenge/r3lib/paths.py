"""Paths and roots (section 2.2). Test overrides are honoured only under /tmp/."""

from __future__ import annotations

import json
import os
from pathlib import Path

R3 = Path(__file__).resolve().parents[1]
REPO = Path("/home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel")
EVAL = REPO / ".dev/eval-workspaces/tasklist-review-panel/20261111-a1"
CONFIG = R3 / "config"


def _root(env: str, default: Path) -> Path:
    v = os.environ.get(env)
    if v:
        p = Path(v).resolve()
        if not str(p).startswith("/tmp/"):
            raise SystemExit(f"E_OVERRIDE: {env}={v} is outside /tmp/")
        return p
    return default


def runs_root() -> Path:
    return _root("R3_RUNS_ROOT", R3 / "runs")


def sb_root() -> Path:
    return _root("R3_SB_ROOT", Path("/tmp/evalsb-collab-r3"))


def scoring_root() -> Path:
    return _root("R3_SCORING_ROOT", R3 / "scoring")


def results_root() -> Path:
    return _root("R3_RESULTS_ROOT", R3 / "results")


def values_file(panel: str) -> Path:
    v = os.environ.get("R3_VALUES_FILE")
    if v:
        return _root("R3_VALUES_FILE", Path(v))
    return R3 / "values" / f"{panel}.json"


def claude_projects() -> Path:
    v = os.environ.get("R3_CLAUDE_PROJECTS")
    return Path(v) if v else Path.home() / ".claude/projects"


def load_json(p) -> dict:
    with open(p, encoding="utf-8") as fh:
        return json.load(fh)


def cfg(name: str):
    return load_json(CONFIG / name)


def cfg_text(name: str) -> str:
    return (CONFIG / name).read_text(encoding="utf-8")


def write_json(p, obj) -> None:
    p = Path(p)
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_name(p.name + ".tmp")
    tmp.write_text(json.dumps(obj, indent=1, sort_keys=False) + "\n", encoding="utf-8")
    os.replace(tmp, p)
