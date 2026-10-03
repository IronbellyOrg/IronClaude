"""Distribution + lifecycle smoke for workflow task packages.

What this proves (executable, real processes/filesystem):
  * the implement skill ships scripts/ through the real installer and the copied
    helper runs under the documented UV invocation shape (skill-base path, no repo src)
  * canonical workflow/implement command Markdown equals the committed plugin copies
  * positive + negative lifecycle driven through the helper's real CLI

What it does NOT prove: that an LLM agent follows the Markdown protocol. That is
exercised separately by the real inference smoke run recorded under the bootstrap
evidence directory.
"""

import filecmp
import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

import superclaude
from superclaude.cli.install_skill import install_skill_command

_REPO = Path(__file__).resolve().parents[2]
_SRC_SKILL = _REPO / "src/superclaude/skills/sc-implement-protocol"
ID = "TASK-WF-smokeHello-20261001-070000"
PLAN = f"{ID}.md"  # tasklist filename == full package directory basename + .md


def _require_worktree_code():
    assert Path(superclaude.__file__).resolve().is_relative_to(_REPO), (
        f"tests import superclaude from {superclaude.__file__}, not this checkout ({_REPO}); "
        "run with PYTHONPATH=<checkout>/src"
    )


def test_plugin_commands_match_canonical():
    for name in ("workflow.md", "implement.md"):
        assert filecmp.cmp(
            _REPO / "src/superclaude/commands" / name,
            _REPO / "plugins/superclaude/commands" / name,
            shallow=False,
        ), name


def test_installer_ships_scripts_and_documented_invocation_runs(tmp_path):
    _require_worktree_code()
    ok, msg = install_skill_command("sc-implement-protocol", tmp_path / "skills")
    assert ok, msg
    base = tmp_path / "skills" / "sc-implement-protocol"
    helper = base / "scripts" / "archive_workspace.py"
    assert filecmp.cmp(
        helper, _SRC_SKILL / "scripts/archive_workspace.py", shallow=False
    )
    assert (base / "refs/managed-workspace.md").is_file()
    uv = shutil.which("uv")
    if uv is None:
        pytest.skip("uv not on PATH")
    cmd = [uv, "run", "--no-project", "python", str(helper), "--help"]
    out = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    assert out.returncode == 0 and "--clear-marker" in out.stdout, out.stderr


def _package(root: Path):
    (root / ".git").mkdir(parents=True)
    pkg = root / ".dev/tasks/to-do" / ID
    (pkg / "artifacts").mkdir(parents=True)
    plan = (
        f"---\nschema: workflow-plan/1.2\nsource: ./source.md\nslug: {ID}\n---\n"
        "# Hello\n\nSource: ./source.md\n\n## Task 1: Add greet()\n\nAcceptance criteria:\n"
        "- greet() returns hello\n"
    )
    (pkg / PLAN).write_text(plan)
    (pkg / "source.md").write_text("add greet\n")
    (pkg / "return-contract.yaml").write_text(
        f'contract_version: "1.1"\nstatus: success\nslug: {ID}\nplan_path: ./{PLAN}\n'
        "source_path: ./source.md\nhandoff_action: none\nhandoff_output_path: null\n"
    )
    (root / "greet.py").write_text("def greet():\n    return 'hello'\n")
    (pkg / "artifacts/t1.log").write_text("greet() == 'hello'\n")

    def h(p):
        return hashlib.sha256(p.read_bytes()).hexdigest()

    (pkg / "progress.md").write_text(
        f"# implement ledger — source: ./{PLAN} — created: 2026-10-01T07:00:00Z\n"
        f"PLAN: sha256={h(pkg / PLAN)} source_sha256={h(pkg / 'source.md')}\n"
        f"T1: start sha={'0' * 40}\n"
        "T1: complete verdict=compliant ac=T1.AC1 evidence=greet.py:2,T1.AC1@./artifacts/t1.log:1 "
        "extras=lint:skip,typecheck:skip,test:pass files=greet.py\n"
    )
    return pkg


def _helper(root, pkg, *extra):
    script = _SRC_SKILL / "scripts/archive_workspace.py"
    return subprocess.run(
        [
            sys.executable,
            str(script),
            "--root",
            str(root),
            "--package",
            str(pkg),
            *extra,
        ],
        capture_output=True,
        text=True,
    )


def test_positive_lifecycle_archives_with_valid_links(tmp_path):
    root = tmp_path / "repo"
    pkg = _package(root)
    state = json.loads(_helper(root, pkg, "--print-state").stdout)["state"]
    with open(pkg / "progress.md", "a") as f:
        f.write(f"FINAL: pass evidence=greet.py:2 state={state}\n")
    res = _helper(root, pkg)
    assert res.returncode == 0, res.stderr
    done = root / ".dev/tasks/done" / ID
    assert json.loads(res.stdout) == {"status": "archived", "path": str(done)}
    assert not pkg.exists() and not (done / ".archiving").exists()
    contract = (done / "return-contract.yaml").read_text()
    for link in (f"./{PLAN}", "./source.md"):
        assert f": {link}" in contract and (done / link).is_file()
    assert (done / "artifacts/t1.log").is_file()
    assert (root / "greet.py").is_file()  # delivery stays canonical, not in the package
    assert (
        _helper(root, pkg).returncode == 0
    )  # stale to-do invocation -> already-archived


def test_negative_failed_final_stays_in_to_do(tmp_path):
    root = tmp_path / "repo"
    pkg = _package(root)
    state = json.loads(_helper(root, pkg, "--print-state").stdout)["state"]
    with open(pkg / "progress.md", "a") as f:
        f.write(f"FINAL: issues evidence=greet.py:2 state={state}\n")
    res = _helper(root, pkg)
    assert res.returncode == 1 and res.stderr.startswith("E-ARCHIVE-FINAL")
    assert (pkg / PLAN).is_file() and not (root / ".dev/tasks/done" / ID).exists()
    assert not (pkg / ".archiving").exists()
