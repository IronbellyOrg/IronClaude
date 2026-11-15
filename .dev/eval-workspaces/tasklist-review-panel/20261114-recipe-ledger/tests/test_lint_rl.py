"""REQ-07: the copied AO-1 lint (scaffold/lint.py) over the RL files, against the invented F-LINT-GT ground truth."""

import json
import os
import shutil

import pytest
from helpers import SW

from scaffold import lint

GT = SW / "fixtures" / "gt" / "lint-gt.json"
PHRASE = (
    "requalified before every dockside"  # four words of the invented L1 description
)
NAME = "quillfern-dock-4"  # the invented doc_id
FOLDERS = ("recipes", "config", "briefs", "cards", "fixtures")


def run(*paths):
    return lint.main(["--gt-glob", str(GT), *map(str, paths)])


def test_seeded_phrase_in_recipe_fails(tmp_path, capsys):
    folder = tmp_path / "recipes"
    shutil.copytree(SW / "recipes", folder)
    assert run(folder) == 0
    path = folder / "recipes.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    entry = data["recipes"]["C3"]
    entry["text"] = entry["text"].replace(" Write at most", f" {PHRASE}. Write at most")
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")
    capsys.readouterr()
    assert run(folder) == 1
    out = capsys.readouterr().out
    assert "recipes.json" in out and "phrase" in out and "dockside" not in out


def test_seeded_name_in_lenses_fails(tmp_path, capsys):
    real = SW / "config" / "lenses.json"
    lenses = tmp_path / "config" / "lenses.json"
    lenses.parent.mkdir()
    if real.is_file():
        shutil.copy(real, lenses)
    else:  # config/lenses.json is written by a later task; the lint only reads text
        lenses.write_text('{"panels": {}}\n', encoding="utf-8")
    assert run(lenses.parent) == 0
    data = json.loads(lenses.read_text(encoding="utf-8"))
    data["note"] = f"see {NAME} for the lens"
    lenses.write_text(json.dumps(data), encoding="utf-8")
    capsys.readouterr()
    assert run(lenses.parent) == 1
    out = capsys.readouterr().out
    assert "lenses.json" in out and "name" in out and "quillfern" not in out


def test_rl_files_clean_on_synthetic_gt(capsys):
    folders = [SW / f for f in FOLDERS if (SW / f).is_dir()]
    assert SW / "recipes" in folders and SW / "cards" in folders
    assert run(*folders) == 0, capsys.readouterr().out


@pytest.mark.freeze
def test_real_recipes_against_real_gt():
    """Written, not run by the build. A maintainer gives the real ground-truth glob in LINT_REAL_GT_GLOB (never hard-coded)."""
    pattern = os.environ.get("LINT_REAL_GT_GLOB")
    assert pattern, "LINT_REAL_GT_GLOB is not set: a maintainer must pass the real glob"
    folders = [str(SW / f) for f in FOLDERS if (SW / f).is_dir()]
    assert lint.main(["--gt-glob", pattern, *folders]) == 0
