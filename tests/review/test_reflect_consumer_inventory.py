"""Tests for scripts/reflect_consumer_inventory.py (reflect return-contract consumer inventory)."""

from __future__ import annotations

import importlib.util
import os
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts" / "reflect_consumer_inventory.py"
_spec = importlib.util.spec_from_file_location("reflect_consumer_inventory", SCRIPT)
inv = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(inv)

SKILL = "src/superclaude/skills/sc-reflect-protocol/SKILL.md"


def _write(root: Path, rel: str, body: str | bytes) -> Path:
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    if isinstance(body, bytes):
        path.write_bytes(body)
    else:
        path.write_text(body, encoding="utf-8")
    return path


def _tree(root: Path) -> None:
    _write(
        root, SKILL, "merge_method: x\nmerge_method again\ncontract_version\nplain\n"
    )
    _write(root, "src/superclaude/cli/reflect/contract.py", "x = 'merge_method'\n")
    _write(root, "src/superclaude/cli/reflect/ensemble.py", "reviewer_cards = []\n")
    _write(
        root,
        "src/superclaude/skills/task-builder/SKILL.md",
        "merge_method: adversarial\n",
    )
    _write(root, "tests/cli/reflect/fixtures/c.yaml", "citations_dropped: 0\n")
    _write(root, "tests/roadmap/test_merge.py", "convergence_score = 1\n")
    _write(
        root, "src/superclaude/skills/sc-roadmap-protocol/SKILL.md", "merge_method\n"
    )
    _write(root, "docs/notes.md", "adversarial_convergence_score: 0.9\n")
    _write(root, "scripts/other.py", "print('nothing here')\n")
    _write(
        root,
        ".dev/eval-workspaces/sc-reflect/grader.py",
        "def grade():\n    return 1\n",
    )
    _write(root, "src/superclaude/x/__pycache__/m.pyc", "merge_method\n")
    _write(root, "src/blob.bin", b"merge_method\x00\x01")


def _hit_rows(text: str) -> dict[str, list[str]]:
    section = text.split("## Hit files", 1)[1].split("## Files not searched", 1)[0]
    rows = {}
    for line in section.splitlines():
        if line.startswith("| `"):
            cells = [c.strip() for c in line.strip("|").split("|")]
            rows[cells[0].strip("`")] = cells[1:]
    return rows


def _run(root: Path, out: Path) -> str:
    assert inv.main(["--root", str(root), "--out", str(out)]) == 0
    return out.read_text(encoding="utf-8")


def test_classification_rules() -> None:
    assert inv.classify(SKILL)[0] == "producer"
    assert (
        inv.classify(
            "src/superclaude/skills/sc-reflect-protocol/refs/report-template.md"
        )[0]
        == "producer"
    )
    assert inv.classify("src/superclaude/cli/reflect/ensemble.py")[0] == "producer"
    assert inv.classify("src/superclaude/cli/reflect/contract.py")[0] == "validator"
    assert inv.classify("src/superclaude/skills/task-builder/SKILL.md")[0] == "consumer"
    assert (
        inv.classify(
            "src/superclaude/skills/sc-reflect-protocol/refs/ops-integration.md"
        )[0]
        == "consumer"
    )
    assert inv.classify("src/superclaude/cli/sprint/executor.py")[0] == "consumer"
    assert inv.classify(".dev/eval-workspaces/sc-reflect/grader.py")[0] == "consumer"
    assert inv.classify("tests/cli/reflect/fixtures/any.yaml")[0] == "consumer"
    assert inv.classify("tests/roadmap/test_x.py")[0] == "not in scope"
    assert inv.classify("docs/guides/RoadMap-guide.md")[0] == "not in scope"
    refs = "src/superclaude/skills/sc-reflect-protocol/refs/"
    assert inv.classify(refs + "input-resolution.md")[:2] == ("producer", "named")
    assert inv.classify(refs + "reflection-rubric.md")[:2] == ("producer", "named")
    assert inv.classify("src/superclaude/skills/task/SKILL.md")[:2] == (
        "consumer",
        "named",
    )
    assert inv.classify(
        "src/superclaude/skills/sc-tasklist-protocol/templates/phase-template.md"
    )[:2] == ("consumer", "named")
    assert inv.classify("src/superclaude/skills/sc-task-protocol/SKILL.md")[:2] == (
        "consumer",
        "named",
    )
    assert inv.classify("tests/cli/reflect/fixtures/any.yaml")[1] == "named"
    # With no text only the path rules can fire; the fallback is a cue-based consumer.
    assert inv.classify("src/superclaude/cli/reflect/runner.py")[:2] == (
        "consumer",
        "cue",
    )
    # First match wins: the tests/cli/reflect/ prefix rule comes before the roadmap rule.
    assert inv.classify("tests/cli/reflect/roadmap_case.yaml")[0] == "consumer"
    assert (
        inv.classify("src/superclaude/skills/sc-roadmap-protocol/SKILL.md")[0]
        == "not in scope"
    )


def test_report_roles_counts_and_lines(tmp_path: Path) -> None:
    _tree(tmp_path)
    text = _run(tmp_path, tmp_path / "out.md")
    rows = _hit_rows(text)
    words = list(inv.WORDS)
    skill = rows[SKILL]
    assert skill[0] == "producer"
    assert skill[1] == "named"
    assert skill[2] == "3"  # lines holding a word
    assert skill[3 + words.index("merge_method")] == "2"
    assert skill[3 + words.index("contract_version")] == "1"
    assert rows["src/superclaude/cli/reflect/contract.py"][0] == "validator"
    assert rows["src/superclaude/cli/reflect/ensemble.py"][0] == "producer"
    assert rows["src/superclaude/skills/task-builder/SKILL.md"][0] == "consumer"
    assert rows["tests/cli/reflect/fixtures/c.yaml"][0] == "consumer"
    assert rows["tests/roadmap/test_merge.py"][0] == "not in scope"
    assert (
        rows["src/superclaude/skills/sc-roadmap-protocol/SKILL.md"][0] == "not in scope"
    )
    notes = rows["docs/notes.md"]
    assert notes[:2] == ["consumer", "cue"]  # key outside a fenced block: no write cue
    # convergence_score counts include adversarial_convergence_score occurrences.
    assert notes[3 + words.index("adversarial_convergence_score")] == "1"
    assert notes[3 + words.index("convergence_score")] == "1"
    assert "scripts/other.py" not in rows
    assert "src/superclaude/x/__pycache__/m.pyc" not in rows  # excluded directory
    assert "src/blob.bin" not in rows  # binary, not searched
    assert (
        "- Hit files by role: producer 2, validator 1, consumer 3, not in scope 2."
        in text
    )
    assert "- Hit files by basis: named 5, cue 3." in text
    assert "unclassified" not in text
    assert (
        "- Not searched: binary 1, unreadable 0, non-regular 0, symlinked directories not followed 0."
        in text
    )
    assert "- Missing scan roots: none." in text
    assert "`src/blob.bin`" in text.split("## Files not searched", 1)[1]
    assert str(tmp_path) not in text


def _roles(root: Path, files: dict[str, str]) -> dict[str, tuple[str, str]]:
    """Write a synthetic tree, run the script, return {path: (role, basis)} from the hit table."""
    for rel, body in files.items():
        _write(root, rel, body)
    rows = _hit_rows(_run(root, root / "out.md"))
    return {rel: (cells[0], cells[1]) for rel, cells in rows.items()}


def test_cue_rule_test_files_are_consumers(tmp_path: Path) -> None:
    # Write cues inside tests and fixtures do not make them producers.
    roles = _roles(
        tmp_path,
        {
            "tests/unit/check.py": "merge_method = 'x'\n",
            "src/pkg/test_build.py": "assert c['merge_method'] == 'x'\n",
            "src/pkg/build_test.py": "merge_method = 'x'\n",
            "src/pkg/conftest.py": "merge_method = 'x'\n",
            ".dev/eval-workspaces/e/fixtures/c.yaml": "merge_method: adversarial\n",
        },
    )
    assert set(roles.values()) == {("consumer", "cue")}
    assert len(roles) == 5


def test_cue_rule_write_makes_producer(tmp_path: Path) -> None:
    files = {
        "src/a/dict_key.py": "out = {'merge_method': m}\n",
        "src/a/subscript.py": 'out["reviewer_cards"] = cards\n',
        "src/a/assign.py": "self.citations_dropped = 0\n",
        "src/a/kwarg.py": "build(contract_version='1.8.0')\n",
        "src/a/annotated.py": "convergence_score: float = 0.0\n",
        "docs/c.json": '{"t2_vendor_diversity":"full"}\n',
        "docs/c.yaml": "  - calibrator_diversity: degraded\n",
        "docs/c.yml": "reviewer_cards:\n  - a\n",
        "docs/fenced.md": "Text\n```yaml\nmerge_method: adversarial\n```\n",
        "docs/fenced_json.md": '~~~\n{"merge_method": "x"}\n~~~\n',
    }
    roles = _roles(tmp_path, files)
    assert roles == {rel: ("producer", "cue") for rel in files}


def test_cue_rule_write_cue_needs_its_form(tmp_path: Path) -> None:
    # Near misses of the write cues fall through to the later rules.
    roles = _roles(
        tmp_path,
        {
            "docs/prose.md": "merge_method: adversarial outside a fence\n",
            "docs/closed.md": "```\nother: 1\n```\nmerge_method: x\n",
            "docs/notes.txt": "merge_method: adversarial\n",
            "src/a/read.py": "m = c.get('merge_method')\n",
            "docs/c.yaml": "note: merge_method is read here\n",
        },
    )
    assert set(roles.values()) == {("consumer", "cue")}
    assert len(roles) == 5


def test_cue_rule_check_makes_validator(tmp_path: Path) -> None:
    files = {
        "src/v/eq.py": "if c.get('merge_method') == 'adversarial':\n    pass\n",
        "src/v/ne.py": "ok = c.get('merge_method') != 'panel'\n",
        "src/v/lt.py": "bad = c['adversarial_convergence_score'] < 0.80\n",
        "src/v/ge.py": "good = c.get('convergence_score') >= 0.8\n",
        "src/v/assert_.py": "assert 'reviewer_cards' in c\n",
        "src/v/raise_.py": "raise ValueError('citations_dropped missing')\n",
    }
    roles = _roles(tmp_path, files)
    assert roles == {rel: ("validator", "cue") for rel in files}


def test_cue_rule_order_and_fallback(tmp_path: Path) -> None:
    roles = _roles(
        tmp_path,
        {
            # Write cue and check cue in one file: the write rule comes first.
            "src/o/both.py": "out = {'merge_method': m}\nassert out.get('merge_method') == m\n",
            # A check cue counts in .py files only.
            "docs/check.md": "fail if adversarial_convergence_score < 0.80\n",
            # The check cue must be on a line that names a word.
            "src/o/apart.py": "m = c.get('merge_method')\nassert m == 'x'\n",
        },
    )
    assert roles == {
        "src/o/both.py": ("producer", "cue"),
        "docs/check.md": ("consumer", "cue"),
        "src/o/apart.py": ("consumer", "cue"),
    }


def test_negative_statements_hold(tmp_path: Path) -> None:
    _tree(tmp_path)
    text = _run(tmp_path, tmp_path / "out.md")
    assert '- No `contract_version == "1.8.0"` equality exists in `src/`' in text
    assert (
        "`.dev/eval-workspaces/sc-reflect/grader.py` has no match for any of the nine words or for `convergence`."
        in text
    )


def test_negative_statements_contradicted(tmp_path: Path) -> None:
    _tree(tmp_path)
    _write(tmp_path, "src/pkg/lint.py", "ok = c.get(\"contract_version\") == '1.8.0'\n")
    _write(
        tmp_path, "src/pkg/doc.md", "| `'1.8.0' == contract_version` | yaml_field |\n"
    )
    _write(
        tmp_path, "src/pkg/yaml.md", 'contract_version: "1.8.0"\n'
    )  # not an equality
    _write(
        tmp_path, "tests/eq.py", 'assert c["contract_version"] == "1.8.0"\n'
    )  # outside src/
    _write(
        tmp_path,
        ".dev/eval-workspaces/sc-reflect/grader.py",
        "# convergence and merge_method\n",
    )
    text = _run(tmp_path, tmp_path / "out.md")
    assert (
        '- CONTRADICTED: 2 line(s) in `src/` hold a `contract_version == "1.8.0"` equality:'
        in text
    )
    assert "  - `src/pkg/lint.py:1` (code)" in text
    assert "  - `src/pkg/doc.md:1` (prose)" in text
    assert "  - Python code lines among them: 1." in text
    assert "src/pkg/yaml.md:1" not in text
    assert "tests/eq.py:1" not in text
    assert (
        "- CONTRADICTED: `.dev/eval-workspaces/sc-reflect/grader.py` matches: `merge_method` 1, `convergence` 1."
        in text
    )


def test_grader_missing_is_unverified(tmp_path: Path) -> None:
    _write(tmp_path, "src/a.md", "merge_method\n")
    text = _run(tmp_path, tmp_path / "out.md")
    assert (
        "- `.dev/eval-workspaces/sc-reflect/grader.py` was not found (UNVERIFIED)."
        in text
    )
    assert (
        "- Missing scan roots: `tests/`, `scripts/`, `.dev/eval-workspaces/`, `docs/`."
        in text
    )
    assert "| `src/superclaude/cli/sprint/executor.py` | consumer |" in text
    assert "| no (UNVERIFIED) | no match |" in text


def test_odd_files_are_counted_not_fatal(tmp_path: Path) -> None:
    _tree(tmp_path)
    (tmp_path / "docs" / "broken.md").symlink_to(tmp_path / "does-not-exist")
    (tmp_path / "src" / "linked").symlink_to(
        tmp_path / "docs", target_is_directory=True
    )
    fifo = False
    if hasattr(os, "mkfifo"):
        os.mkfifo(tmp_path / "scripts" / "pipe")
        fifo = True
    text = _run(tmp_path, tmp_path / "out.md")
    nonregular = 1 if fifo else 0
    assert (
        f"- Not searched: binary 1, unreadable 1, non-regular {nonregular}, symlinked directories not followed 1."
        in text
    )
    tail = text.split("## Files not searched", 1)[1]
    assert "- Unreadable: `docs/broken.md`." in tail
    assert "- Symlinked directories: `src/linked`." in tail
    # The symlinked directory is not followed, so docs/notes.md is not counted twice.
    assert "src/linked/notes.md" not in text


def test_two_runs_identical_and_out_in_scan_root_skipped(tmp_path: Path) -> None:
    a, b = tmp_path / "a", tmp_path / "b"
    _tree(a)
    _tree(b)
    out = a / "docs" / "inventory.md"  # inside a scan root, holds the words
    first = _run(a, out)
    second = _run(a, out)
    assert first == second
    assert "docs/inventory.md" not in _hit_rows(second)
    # Same tree content under another root and another --out path gives the same bytes.
    assert _run(b, tmp_path / "elsewhere" / "inv.md") == first


def test_default_out(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    assert inv.default_out(tmp_path) == Path("artifacts") / "consumer-inventory.md"
    (tmp_path / inv.PACKAGE).mkdir(parents=True)
    assert (
        inv.default_out(tmp_path)
        == tmp_path / inv.PACKAGE / "artifacts" / "consumer-inventory.md"
    )
    _write(tmp_path, SKILL, "merge_method\n")
    monkeypatch.chdir(tmp_path)
    assert inv.main(["--root", str(tmp_path)]) == 0
    assert (tmp_path / inv.PACKAGE / "artifacts" / "consumer-inventory.md").is_file()


def test_missing_root_exits_2(tmp_path: Path) -> None:
    assert (
        inv.main(["--root", str(tmp_path / "nope"), "--out", str(tmp_path / "o.md")])
        == 2
    )
