"""K7 and the Task 1 skeleton: no ignored code folder, readable config files (TESTING section 4)."""

import json
import subprocess

from helpers import REPO, REVIEWERS, SW

GENERATED = {
    "results",
    "runs",
    "scoring",
    "__pycache__",
    ".pytest_cache",
    ".ruff_cache",
}
CODE_SUFFIXES = {".py", ".sh"}


def code_folders():
    out = []
    for d in [SW, *SW.rglob("*")]:
        if not d.is_dir() or GENERATED & set(d.relative_to(SW).parts):
            continue
        if any(f.suffix in CODE_SUFFIXES for f in d.iterdir() if f.is_file()):
            out.append(d)
    return out


def test_no_ignored_folder_names():
    folders = code_folders()
    assert {d.name for d in folders} >= {
        "bin",
        "tests",
        "scaffold",
        "sweep",
        "analysis",
    }
    ignored = []
    for d in folders:
        r = subprocess.run(
            ["git", "-C", str(REPO), "check-ignore", "-q", "--", str(d)],
            capture_output=True,
        )
        if r.returncode == 0:
            ignored.append(str(d.relative_to(SW)))
    assert ignored == []
    assert not [d for d in SW.rglob("lib") if d.is_dir()]


def test_package_files_are_empty_and_present():
    for p in ("scaffold", "sweep", "analysis"):
        f = SW / p / "__init__.py"
        assert f.is_file() and f.stat().st_size == 0, p


def test_ruff_toml_extends_repo_config():
    assert (
        SW / "ruff.toml"
    ).read_text().strip() == 'extend = "../../../../pyproject.toml"'
    assert (SW / "ruff.toml").parent.joinpath(
        "../../../../pyproject.toml"
    ).resolve() == REPO / "pyproject.toml"
    assert (REPO / "pyproject.toml").is_file()


def load(name):
    return json.loads((SW / "config" / name).read_text(encoding="utf-8"))


def test_panel_caps():
    panels = load("panels.json")["panels"]
    caps = {k: tuple(v[r]["cap"] for r in ("S", "L1", "L2")) for k, v in panels.items()}
    assert caps == {"primary": (8, 8, 8), "haiku": (6, 9, 9), "sonnet": (6, 9, 9)}
    for name, c in caps.items():
        assert sum(c) == 24, name
    assert panels["haiku"]["S"]["classes"] == ["C4", "C5", "C8"]
    assert (
        panels["primary"]["S"]["classes"] == panels["sonnet"]["S"]["classes"] == "any"
    )


def test_panel_models_are_reviewer_models():
    for p in load("panels.json")["panels"].values():
        for role in ("S", "L1", "L2"):
            assert p[role]["model"] in REVIEWERS


def test_packages_point_at_real_files():
    pk = load("packages.json")
    assert list(pk["packages"]) == pk["order"] and len(pk["order"]) == 3
    for doc, v in pk["packages"].items():
        assert (REPO / v["candidate"]).is_file(), doc
        assert (REPO / v["source"]).is_file(), doc
        assert len(v["base"]) == 40 and v["masked_paths"], doc


def test_values_per_panel_document_and_model():
    v = load("values.json")
    docs = set(load("packages.json")["packages"])
    for panel in load("panels.json")["panels"]:
        assert set(v["b"][panel]) == docs
        assert all(x > 0 for x in v["b"][panel].values())
    assert set(v["c"]) == set(REVIEWERS)
    assert v["kill_s"] == {"cap_s": 15, "frac_of_b": 0.10}
    assert v["hang_s"]["factor"] == 1.5


def test_values_selection_constants():
    v = load("values.json")
    assert (v["K"], v["K_single"], v["cap"]) == (8, 12, 12)
