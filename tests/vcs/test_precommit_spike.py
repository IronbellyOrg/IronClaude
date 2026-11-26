"""Spike: does the hook emulator behave like the real pre-commit framework (FR-118)?

Marked ``real_framework`` and skipped when ``pre-commit`` is not on ``PATH``. To run it:
``uv run --with pre-commit pytest tests/vcs/test_precommit_spike.py -q`` (uv puts the
framework's script on ``PATH`` for that run). Both sides run the same action script and
the same scenarios on identical throwaway repositories, and the observable results
(exit status, HEAD moved, file contents, number of saved patches) must be equal.

The real framework needs no network here: the hook is a ``repo: local`` hook with
``language: system``. Other pre-commit versions and git versions are UNVERIFIED.
"""

from __future__ import annotations

import shutil
import subprocess

import pytest

from .conftest import HookEmulator, Repo

pytestmark = pytest.mark.real_framework

if shutil.which("pre-commit") is None:
    pytest.skip("pre-commit is not on PATH", allow_module_level=True)

PERSON_EDIT = "person edit outside the commit set\n"


def _prepare(root, name, kind):
    """A repo whose pre-commit hook is the emulator (kind='emulator') or the real one."""
    repo = Repo(root / name)
    emulator = HookEmulator(repo, root / f"{name}-hook")
    if kind == "real":
        config = (
            "repos:\n- repo: local\n  hooks:\n  - id: emu-action\n"
            "    name: emu-action\n"
            f"    entry: sh {emulator.action_script}\n"
            "    language: system\n    pass_filenames: false\n    always_run: true\n"
        )
        repo.write(".pre-commit-config.yaml", config)
    for rel in ("a.txt", "b.txt", "c.txt"):
        repo.write(rel, rel[0] + "\n")
    repo.commit("add files")
    if kind == "real":
        done = subprocess.run(
            ["pre-commit", "install", "--overwrite"],
            cwd=repo.work, capture_output=True, text=True,
        )  # fmt: skip
        assert done.returncode == 0, done.stderr
    repo.write("a.txt", "a changed by the task\n")
    return repo, emulator


def _observe(repo, emulator, patch_dir, action, assume_unchanged, c_edit):
    head = repo.git("rev-parse", "HEAD").strip()
    if assume_unchanged:
        repo.git("update-index", "--assume-unchanged", "b.txt")
    repo.write("b.txt", PERSON_EDIT)
    if c_edit:
        repo.write("c.txt", "visible unstaged edit\n")
    emulator.set_action(action, "a.txt")
    done = emulator.commit(["a.txt"])
    read = lambda n: (repo.work / n).read_text(encoding="utf-8")  # noqa: E731
    return {
        "returncode": done.returncode,
        "head_moved": repo.git("rev-parse", "HEAD").strip() != head,
        "a": read("a.txt"),
        "b": read("b.txt"),
        "c": read("c.txt"),
        "patches": len(list(patch_dir.glob("patch*"))) if patch_dir.is_dir() else 0,
    }


SCENARIOS = {
    "success-with-outside-edit": ("pass", False, False),
    "hook-exits-1": ("exit1", False, False),
    "hook-rewrites-and-exits-1": ("rewrite_exit1", False, False),
    "hook-rewrites-and-stages": ("rewrite_add", False, False),
    "assume-unchanged-with-other-edit": ("pass", True, True),
    "assume-unchanged-alone": ("pass", True, False),
}


@pytest.mark.parametrize("scenario", sorted(SCENARIOS))
def test_emulator_matches_the_real_framework(scenario, tmp_path, monkeypatch):
    action, assume, c_edit = SCENARIOS[scenario]
    real_home = tmp_path / "pre-commit-home"
    monkeypatch.setenv("PRE_COMMIT_HOME", str(real_home))

    emu_repo, emu = _prepare(tmp_path, "emu", "emulator")
    real_repo, real = _prepare(tmp_path, "real", "real")

    assert "pre-commit" in (real_repo.work / ".git/hooks/pre-commit").read_text()
    expected = _observe(emu_repo, emu, emu.cache, action, assume, c_edit)
    actual = _observe(real_repo, real, real_home, action, assume, c_edit)

    assert actual == expected
    if scenario == "success-with-outside-edit":  # the equality is not vacuous
        assert actual["patches"] == 1 and actual["b"] == PERSON_EDIT


def test_sigkill_leaves_the_edit_only_in_the_saved_patch_on_both(tmp_path, monkeypatch):
    real_home = tmp_path / "pre-commit-home"
    monkeypatch.setenv("PRE_COMMIT_HOME", str(real_home))
    seen = {}
    for kind in ("emulator", "real"):
        repo, hook = _prepare(tmp_path, kind, kind)
        head = repo.git("rev-parse", "HEAD").strip()
        repo.write("b.txt", PERSON_EDIT)
        hook.kill_group(hook.start_blocked_commit(["a.txt"]))
        patch_dir = hook.cache if kind == "emulator" else real_home
        patches = list(patch_dir.glob("patch*"))
        seen[kind] = (
            repo.git("rev-parse", "HEAD").strip() == head,
            (repo.work / "b.txt").read_text(encoding="utf-8"),
            [PERSON_EDIT.strip() in p.read_text(encoding="utf-8") for p in patches],
        )
    assert seen["emulator"] == seen["real"] == (True, "b\n", [True])
