"""Reflect input-snapshot / output-root isolation (PR256 residual).

What this proves:
  * TEXT GUARDS: the shipped Markdown protocol states the pinned, exact-subtree
    output exclusion and the fail-closed overlap/symlink guards, and the managed
    delegate ref points at it (src == existing plugin mirror).
  * DIAGNOSTIC MODEL (not production code): a small model of the documented
    policy shows the policy is self-consistent (own writes stable, real edits
    detected, prefix collision safe, overlap/symlink fatal).

What it does NOT prove: that an LLM agent follows the protocol. The snapshot is an
inference-protocol step with no executable helper; a real co-located /sc:reflect
run is the live validation.
"""

import hashlib
import json
import os
from pathlib import Path

import pytest

_REPO = Path(__file__).resolve().parents[2]
_REFLECT = _REPO / "src/superclaude/skills/sc-reflect-protocol"
_MANAGED = "skills/sc-implement-protocol/refs/managed-workspace.md"


def _read(p):
    return p.read_text(encoding="utf-8")


# --------------------------- text guards ---------------------------------


def test_skill_defines_pinned_exact_output_root_policy():
    t = _read(_REFLECT / "SKILL.md")
    for needle in (
        "REFLECT_OUTPUT_ROOT",
        "before any write or directory creation",
        "MUST NOT re-resolve it",
        "**path components**, never string prefix",
        "output_input_overlap",
        "output_symlink_escape",
        "**exactly one subtree**",
        "same pinned `REFLECT_OUTPUT_ROOT` exclusion as at construction",
        "Overlap with an explicit input is fatal, never an exclusion",
    ):
        assert needle in t, needle
    # cache policy preserved, not widened
    assert (
        "VERIFICATION_ARTIFACT_EXCLUDES" in t and "blanket `artifacts/` exclusion" in t
    )


def test_input_resolution_carries_output_guard():
    t = _read(_REFLECT / "refs/input-resolution.md")
    assert "output_input_overlap" in t and "output_symlink_escape" in t
    assert "never string prefix" in t


def test_managed_delegate_ref_points_at_reflect_policy_and_mirror_matches():
    src = _REPO / "src/superclaude" / _MANAGED
    t = _read(src)
    assert "fresh dedicated per-run `--output` directory" in t
    assert "REFLECT_OUTPUT_ROOT" in t and "do not restate or reimplement" in t
    mirror = _REPO / "plugins/superclaude" / _MANAGED
    assert _read(mirror) == t


# ----------------- diagnostic model of the documented policy --------------

CACHE_DIRS = {"__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache"}


def _under(path: Path, root: Path) -> bool:
    return path == root or root in path.parents  # component containment


def resolve_output_root(workunit: Path, explicit_inputs, output: Path) -> Path:
    """Model of SKILL.md Step 0.4 REFLECT_OUTPUT_ROOT guard (runs before any write)."""
    if ".." in output.parts:
        raise ValueError("output_symlink_escape")
    wu = workunit.resolve()
    root = output.resolve()  # non-strict: resolves through nearest existing ancestor
    if _under(
        Path(os.path.abspath(output)), Path(os.path.abspath(workunit))
    ) and not _under(root, wu):
        raise ValueError("output_symlink_escape")
    if _under(wu, root):  # equals or contains the work unit
        raise ValueError("output_input_overlap")
    for inp in explicit_inputs:
        if _under(
            Path(inp).resolve(), root
        ):  # input at/under output; also output under input file
            raise ValueError("output_input_overlap")
    return root


def snapshot(workunit: Path, root: Path, extra=()) -> str:
    """Diagnostic inputs are named relative to the work-unit root, including extras."""
    rows = []
    for p in sorted([*workunit.rglob("*"), *extra]):
        if not p.is_file() or CACHE_DIRS & set(p.parts):
            continue
        if _under(p.resolve(), root):
            continue
        rel = os.path.relpath(p.resolve(), workunit.resolve())
        rows.append((rel, hashlib.sha256(p.read_bytes()).hexdigest()))
    return hashlib.sha256(json.dumps(rows).encode()).hexdigest()


@pytest.fixture
def pkg(tmp_path):
    wu = tmp_path / "TASK-WF-x-20261003-020000"
    (wu / "artifacts" / "reflect-post").mkdir(parents=True)
    (wu / "artifacts" / "reflect-post-previous").mkdir()
    files = {
        "tasklist": wu / "TASK-WF-x-20261003-020000.md",
        "source": wu / "source.md",
        "log": wu / "progress.md",
        "qa": wu / "artifacts" / "prior-qa.md",
        "sibling": wu / "artifacts" / "reflect-post-previous" / "REPORT.md",
    }
    for p in files.values():
        p.write_text(p.name + "\n")
    delivery = tmp_path / "delivery.py"  # linked delivery file outside the package
    delivery.write_text("x = 1\n")
    files["delivery"] = delivery
    return wu, files


def _inputs(files):
    return [
        files["tasklist"],
        files["source"],
        files["log"],
        files["qa"],
        files["delivery"],
    ]


def test_own_writes_stable_initially_and_on_recompute(pkg):
    wu, files = pkg
    out = wu / "artifacts" / "reflect-post"
    root = resolve_output_root(wu, _inputs(files), out)
    first = snapshot(wu, root)
    (out / "artifacts").mkdir()
    (out / "artifacts" / "input-snapshot.yaml").write_text("s\n")
    (out / "audit.log").write_text("a\n")
    (out / "REPORT.md").write_text("r\n")
    assert snapshot(wu, root) == first
    (wu / "__pycache__").mkdir()
    (wu / "__pycache__" / "m.pyc").write_bytes(b"\0")  # cache policy preserved
    assert snapshot(wu, root) == first


@pytest.mark.parametrize(
    "name", ["tasklist", "source", "log", "qa", "sibling", "delivery"]
)
def test_real_edits_still_detected(pkg, name):
    wu, files = pkg
    root = resolve_output_root(wu, _inputs(files), wu / "artifacts" / "reflect-post")
    extra = [files["delivery"]]
    before = snapshot(wu, root, extra)
    files[name].write_text("changed\n")
    assert snapshot(wu, root, extra) != before


def test_prefix_collision_sibling_not_excluded(pkg):
    wu, files = pkg
    root = resolve_output_root(wu, _inputs(files), wu / "artifacts" / "reflect-post")
    assert not _under(files["sibling"].resolve(), root)
    before = snapshot(wu, root)
    (wu / "artifacts" / "reflect-post-previous" / "new.md").write_text("n\n")
    assert snapshot(wu, root) != before


def test_overlap_and_escape_fail_closed(pkg, tmp_path):
    wu, files = pkg
    for bad in (wu, wu / "artifacts"):  # equals / contains work unit or explicit input
        with pytest.raises(ValueError, match="output_input_overlap"):
            resolve_output_root(wu, _inputs(files), bad)
    # output holding an explicitly referenced prior report
    with pytest.raises(ValueError, match="output_input_overlap"):
        resolve_output_root(
            wu, [*_inputs(files), files["sibling"]], files["sibling"].parent
        )
    # explicit input under output
    with pytest.raises(ValueError, match="output_input_overlap"):
        resolve_output_root(
            wu,
            [wu / "artifacts" / "reflect-post" / "spec.md"],
            wu / "artifacts" / "reflect-post",
        )
    # symlink escape and parent traversal
    outside = tmp_path / "elsewhere"
    outside.mkdir()
    (wu / "artifacts" / "link").symlink_to(outside, target_is_directory=True)
    with pytest.raises(ValueError, match="output_symlink_escape"):
        resolve_output_root(wu, _inputs(files), wu / "artifacts" / "link" / "run")
    with pytest.raises(ValueError, match="output_symlink_escape"):
        resolve_output_root(
            wu, _inputs(files), wu / "artifacts" / ".." / "artifacts" / "reflect-post"
        )
    # symlink aliasing the work unit itself must not widen the excluded subtree
    (tmp_path / "alias").symlink_to(wu, target_is_directory=True)
    with pytest.raises(ValueError, match="output_input_overlap"):
        resolve_output_root(wu, _inputs(files), tmp_path / "alias")


def test_external_output_parent_traversal_is_rejected(pkg, tmp_path):
    wu, files = pkg
    with pytest.raises(ValueError, match="output_symlink_escape"):
        resolve_output_root(wu, _inputs(files), tmp_path / "outside" / ".." / "run")


def test_recorded_move_maps_pinned_root_without_retargeting(pkg, tmp_path):
    wu, files = pkg
    pinned = resolve_output_root(wu, _inputs(files), wu / "artifacts" / "current")
    before = snapshot(wu, pinned)
    pinned.mkdir()
    (pinned / "REPORT.md").write_text("own output\n")
    destination = tmp_path / "done" / wu.name
    destination.parent.mkdir()
    suffix = pinned.relative_to(wu)
    wu.rename(destination)  # disposable fixture, not the production archive operation
    mapped = destination / suffix
    assert snapshot(destination, mapped) == before
    assert not pinned.exists()


def test_external_explicit_input_changes_remain_visible(pkg, tmp_path):
    wu, files = pkg
    extra = tmp_path / "delivery.txt"
    extra.write_text("before\n")
    root = resolve_output_root(wu, [*_inputs(files), extra], wu / "artifacts" / "run")
    before = snapshot(wu, root, [extra])
    extra.write_text("after\n")
    assert snapshot(wu, root, [extra]) != before
