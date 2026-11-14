"""Redesign 5 (coverage deflection) harness library. Paths can be redirected by env for tests."""
import json
import os
import time
from pathlib import Path

R5 = Path(__file__).resolve().parents[2]
EVAL_DEFAULT = R5.parents[1] / "20261111-a1"
PKGS = (
    "TASK-WF-designSpec-20261107-075614",
    "TASK-WF-makeTheAliasOnly-20261105-051649",
    "TASK-WF-design-20261108-041415",
)
ALLOWED_MODELS = {"muse-ember-1.0", "gpt-6-luna", "claude-haiku-5-5", "claude-sonnet-5-5", "grok-4.7"}


def cfg() -> Path:
    return Path(os.environ.get("R5_CONFIG", R5 / "config"))


def out() -> Path:
    return Path(os.environ.get("R5_OUT", R5))


def eval_dir() -> Path:
    return Path(os.environ.get("R5_EVAL", EVAL_DEFAULT))


def sb() -> Path:
    return Path(os.environ.get("R5_SB", "/tmp/evalsb-collab-r5"))


def now_ms() -> int:
    return int(time.time() * 1000)


def read_json(p, default=None):
    try:
        return json.loads(Path(p).read_text())
    except (OSError, ValueError):
        return default


def read_jsonl(p) -> list:
    out_ = []
    try:
        for line in Path(p).read_text().splitlines():
            if line.strip():
                try:
                    out_.append(json.loads(line))
                except ValueError:
                    pass
    except OSError:
        pass
    return out_


def append_jsonl(p, obj) -> None:
    p = Path(p)
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, "a") as f:
        f.write(json.dumps(obj, separators=(",", ":")) + "\n")


def write_json(p, obj) -> None:
    p = Path(p)
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_name(p.name + ".tmp")
    tmp.write_text(json.dumps(obj, indent=1) + "\n")
    tmp.replace(p)
