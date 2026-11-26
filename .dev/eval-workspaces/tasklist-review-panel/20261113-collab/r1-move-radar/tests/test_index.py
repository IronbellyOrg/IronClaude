"""T-2: radar-index.sh on the fixture candidate."""

from conftest import PKG, TOOLS, jload, run


def test_index_fixture(fake_sb, root):
    r = run(["bash", str(TOOLS / "radar-index.sh"), PKG, "--root", str(root), "--sb", str(fake_sb)])
    assert r.returncode == 0, r.stderr
    ix = jload(root / "index" / f"{PKG}.json")
    assert ix["tasks"] == ["T1", "T2", "T3"]
    # a path inside Task 2's section maps to T2 only
    assert ix["task_of_path"]["docs/guide.md"] == ["T2"]
    # a path created by a Task (parent dir exists) is kept and mapped
    assert ix["task_of_path"]["src/app/merge_guard.py"] == ["T1"]
    assert ix["task_of_path"]["src/app/core.py"] == ["T1"]  # the Constraints mention belongs to no Task
    assert sorted(ix["criterion_greps"]) == ["HOW-WE-WORK", "merge_guard"]
    assert ix["root_files"] == ["CHANGELOG.md", "Makefile"]
    assert "tests/app/test_core.py" in ix["paths"] and "tests/app/test_other.py" not in ix["paths"]
    # shorthand references resolve to the full path, never to a root-level path that does not exist
    assert ix["task_of_path"]["src/app/scripts/old.sh"] == ["T2"]  # existing file, named as scripts/old.sh
    assert ix["task_of_path"]["src/app/scripts/tool.sh"] == ["T1", "T2"]  # Task-created file, shorthand in T2
    assert "scripts/old.sh" not in ix["paths"] and "scripts/tool.sh" not in ix["paths"]
    assert "merge_guard" in ix["keys"] and "core" in ix["keys"]
    assert all(len(k) >= 4 for k in ix["keys"])  # stems shorter than 4 are dropped
