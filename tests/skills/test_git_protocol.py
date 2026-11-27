"""Static tests for the sc-git-protocol skill and the /sc:git command file.

Enforcement type: STATIC (text and constants). Behavior of the helper is covered under
tests/vcs/. Requirements: T-13, T-17, NFR-003, FR-008, FR-009, FR-018, FR-081.
"""

from __future__ import annotations

import importlib.util
import os
import re
import subprocess
from functools import lru_cache
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
SKILL_DIR = ROOT / "src/superclaude/skills/sc-git-protocol"
SKILL_MD = SKILL_DIR / "SKILL.md"
REFS_DIR = SKILL_DIR / "refs"
SCRIPTS_DIR = SKILL_DIR / "scripts"
GIT_MD = ROOT / "src/superclaude/commands/git.md"
VCS_TESTS = ROOT / "tests/vcs"

REFUSAL = "authorization: write operations need a person-typed /sc:git <operation>"


def _text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _flat(text: str) -> str:
    return " ".join(text.split())


def _files_under(folder: Path):
    return sorted(
        p
        for p in folder.rglob("*")
        if p.is_file() and "__pycache__" not in p.parts and p.suffix != ".pyc"
    )


def _scanned_files():
    """The files this work adds: the protocol folder, git.md and tests/vcs/**."""
    return [*_files_under(SKILL_DIR), GIT_MD, *_files_under(VCS_TESTS)]


@lru_cache(maxsize=1)
def _rules():
    spec = importlib.util.spec_from_file_location(
        "vcs_rules_under_test", SCRIPTS_DIR / "vcs_rules.py"
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


@lru_cache(maxsize=1)
def _help_verbs():
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    done = subprocess.run(
        [
            "uv",
            "run",
            "--no-project",
            "python",
            str(SCRIPTS_DIR / "vcs.py"),
            "--help",
        ],
        capture_output=True,
        text=True,
        env=env,
        cwd=ROOT,
        check=True,
    )
    # Verb rows are indented four spaces; wrapped descriptions are indented deeper.
    return set(re.findall(r"^ {4}([a-z][a-z-]*)(?=\s|$)", done.stdout, re.M))


def _registry():
    text = _text(SKILL_MD)
    section = text.split("## Operation registry", 1)[1].split("\n## ", 1)[0]
    rows = []
    for line in section.splitlines():
        if not line.startswith("|") or line.startswith("|---"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if cells[0] == "Operation":
            continue
        operation, klass, prefix, refs, verbs = cells
        rows.append(
            {
                "operation": operation.strip("`"),
                "class": klass,
                "prefix": prefix,
                "refs": re.findall(r"`([\w.-]+\.md)`", refs),
                "verbs": re.findall(r"`([a-z-]+)`", verbs),
            }
        )
    return rows


def _is_read(row):
    return row["class"].startswith("read")


# --- registry (FR-008, FR-018, T-13) ---------------------------------------------------


def test_registry_has_the_ten_operations():
    assert len(_registry()) == 10


def test_registry_refs_exist():
    for row in _registry():
        assert row["refs"], row["operation"]
        for ref in row["refs"]:
            assert (REFS_DIR / ref).is_file(), (row["operation"], ref)


def test_registry_verbs_appear_in_helper_help():
    verbs = _help_verbs()
    assert {"preflight", "stage-plan", "check-message", "verify", "submodules"} <= verbs
    for row in _registry():
        assert set(row["verbs"]) <= verbs, (row["operation"], row["verbs"])


def test_no_operation_loads_more_than_two_refs():
    for row in _registry():
        assert len(row["refs"]) <= 2, row["operation"]


def test_read_operations_never_load_safety_and_writes_do():
    for row in _registry():
        if _is_read(row):
            assert "safety.md" not in row["refs"], row["operation"]
            assert len(row["refs"]) == 1, row["operation"]
        else:
            assert "safety.md" in row["refs"], row["operation"]
            assert len(row["refs"]) == 2, row["operation"]


# --- the lists in safety.md equal vcs_rules.py (NFR-003, T-13) -------------------------


def _safety_list(name: str):
    match = re.search(rf"^- `{name}`: (.+)$", _text(REFS_DIR / "safety.md"), re.M)
    assert match, f"safety.md has no list line for {name}"
    return re.findall(r"`([^`]+)`", match.group(1))


@pytest.mark.parametrize(
    "name", ["PROTECTED_BRANCHES", "FORBIDDEN_FLAGS", "DEV_MIRROR_ALLOW"]
)
def test_safety_list_equals_constant(name):
    assert _safety_list(name) == list(getattr(_rules(), name))


def test_safety_min_git_equals_constant():
    assert _safety_list("MIN_GIT") == [".".join(map(str, _rules().MIN_GIT))]


# --- no src/superclaude path in installed primitives (FR-009) --------------------------


def test_no_src_superclaude_path_in_protocol_or_command():
    for path in [*_files_under(SKILL_DIR), GIT_MD]:
        assert "src/superclaude" not in _text(path), path.relative_to(ROOT)


# --- person-only authority (invariant I4) ----------------------------------------------


def test_skill_states_the_person_line_rule():
    flat = _flat(_text(SKILL_MD))
    assert f"`{REFUSAL}`" in flat
    assert "current message starts with that operation's prefix" in flat
    assert "A refusal prints no command line" in flat
    assert "One line authorizes one operation, and only" in flat


def test_write_rows_name_a_prefix_of_their_own_operation():
    for row in _registry():
        if _is_read(row):
            assert row["prefix"] == "any `/sc:git` line", row["operation"]
        else:
            prefix = row["prefix"].strip("`")
            assert prefix.startswith("/sc:git "), row["operation"]
            assert f"/sc:git {row['operation']}".startswith(prefix), row["operation"]


# --- no branch deletion anywhere in what this work adds (FR-081, T-17) -----------------

_FORBIDS = re.compile(r"\b(never|not|no|refuse[sd]?|forbid\w*|without)\b", re.I)
_DELETE_TEXT = [
    re.compile(
        r"git\s+(?:-C\s+\S+\s+)?branch\b[^\n]*?\s"
        r"(?:-[A-Za-z]*[dD][A-Za-z]*|--delete)(?=\s|$|[`\"'])"
    ),
    re.compile(r"git\s+(?:-C\s+\S+\s+)?push\b[^\n]*?\s--delete\b"),
    re.compile(r"git\s+(?:-C\s+\S+\s+)?push\s+\S+\s+:[^\s:]"),
]
_DELETE_ARGV = re.compile(
    r"""["']branch["'][^\n]*["'](?:-[A-Za-z]*[dD][A-Za-z]*|--delete)["']"""
    r"""|["']push["'][^\n]*["'](?:--delete|:[^"']+)["']"""
)


def _text_hits(line: str):
    return any(rx.search(line) for rx in _DELETE_TEXT)


@pytest.mark.parametrize(
    "line",
    [
        "git branch -d old",
        "git branch -D old",
        "git branch --delete old",
        "git branch -q -D old",
        "git push --delete origin old",
        "git push origin :old",
    ],
)
def test_delete_scan_detects_each_form(line):
    assert _text_hits(line)


@pytest.mark.parametrize(
    "line", ["git branch --show-current", "git branch -v", "git push origin main:trunk"]
)
def test_delete_scan_ignores_reads_and_plain_pushes(line):
    assert not _text_hits(line)


def test_scan_reads_only_files_this_work_adds():
    allowed = (SKILL_DIR, VCS_TESTS)
    for path in _scanned_files():
        assert path == GIT_MD or any(d in path.parents for d in allowed), path
    assert ROOT / "scripts/worktree_cleanup.py" not in _scanned_files()


def test_no_branch_deletion_command_or_instruction():
    for path in _scanned_files():
        in_fence = False
        for number, line in enumerate(_text(path).splitlines(), 1):
            if path.suffix == ".md":
                if line.strip().startswith("```"):
                    in_fence = not in_fence
                    continue
                # A sentence that forbids a deletion may name it; a fence never may.
                if _text_hits(line) and (in_fence or not _FORBIDS.search(line)):
                    pytest.fail(f"{path.relative_to(ROOT)}:{number}: {line.strip()}")
            elif _text_hits(line):
                pytest.fail(f"{path.relative_to(ROOT)}:{number}: {line.strip()}")


def test_helper_scripts_build_no_deletion_argv():
    for path in sorted(SCRIPTS_DIR.glob("*.py")):
        for number, line in enumerate(_text(path).splitlines(), 1):
            assert not _DELETE_ARGV.search(line), f"{path.name}:{number}: {line}"


# --- submodule update argv ---------------------------------------------------------------


def test_submodule_update_forces_the_checkout_strategy():
    # Without --checkout a module's own submodule.<name>.update setting (none, merge,
    # rebase) decides what the update does, and the read-back of the recorded commit fails.
    text = _text(REFS_DIR / "submodule.md")
    assert text.count("git submodule update --init --checkout -- '<path>'") == 2
    assert "git submodule update --init -- " not in text


# --- size limits (FR-018, NFR-012) -----------------------------------------------------


def test_size_limits():
    assert len(_text(GIT_MD).splitlines()) <= 150
    assert len(_text(SKILL_MD).splitlines()) <= 500
    for ref in sorted(REFS_DIR.glob("*.md")):
        assert len(_text(ref).splitlines()) <= 250, ref.name


# --- plugin mirror (FR-014) ------------------------------------------------------------


def test_plugin_skill_folder_is_byte_identical():
    plugin_dir = ROOT / "plugins/superclaude/skills/sc-git-protocol"
    assert plugin_dir.is_dir()
    src_files = _files_under(SKILL_DIR)
    assert src_files
    assert [p.relative_to(plugin_dir) for p in _files_under(plugin_dir)] == [
        p.relative_to(SKILL_DIR) for p in src_files
    ]
    for src in src_files:
        plugin = plugin_dir / src.relative_to(SKILL_DIR)
        assert plugin.read_bytes() == src.read_bytes(), plugin.relative_to(ROOT)
