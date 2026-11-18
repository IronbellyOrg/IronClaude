"""Reverse scan: the old definition of "blocking" must appear in no Markdown file.

The old sentence followed the opening of the review severity rule's first bullet
("Grade every review finding as blocking or minor."). The opening stays in the new
bullet, so the scan matches only the old sentence that came after it. The scan walks
the directory tree, not `git ls-files`, so an unstaged file is scanned too. It reads
only `*.md` files, so Python code under `src/superclaude/cli/` is never matched.
"""

from __future__ import annotations

from pathlib import Path

_REPO = Path(__file__).resolve().parents[2]
_ROOTS = ("src/superclaude", "plugins/superclaude")

OLD_SENTENCE = (
    "Blocking is a real defect: wrong behaviour, a false claim, a missing "
    "required deliverable, or a security or data-loss risk"
)


def _flat(text: str) -> str:
    return " ".join(text.split())


def files_with_old_sentence(base: Path, roots=_ROOTS) -> list[str]:
    """Repo-relative paths of Markdown files under the roots that hold the old sentence."""
    hits: list[str] = []
    for root in roots:
        folder = base / root
        if not folder.is_dir():
            continue
        for path in sorted(folder.rglob("*.md")):
            try:
                text = path.read_text(encoding="utf-8")
            except (OSError, UnicodeDecodeError):
                continue
            if OLD_SENTENCE in _flat(text):
                hits.append(str(path.relative_to(base)))
    return hits


def test_the_old_sentence_is_in_no_markdown_file():
    assert files_with_old_sentence(_REPO) == []


def test_a_markdown_file_holding_the_old_sentence_fails_the_scan(tmp_path):
    folder = tmp_path / "src/superclaude/agents"
    folder.mkdir(parents=True)
    (folder / "x.md").write_text(
        "- Grade every review finding as blocking or minor.\n"
        "  Blocking is a real defect: wrong behaviour, a false claim,\n"
        "  a missing required deliverable, or a security or data-loss risk.\n",
        encoding="utf-8",
    )
    assert files_with_old_sentence(tmp_path) == ["src/superclaude/agents/x.md"]


def test_a_python_file_under_cli_holding_the_old_sentence_passes(tmp_path):
    folder = tmp_path / "src/superclaude/cli"
    folder.mkdir(parents=True)
    (folder / "x.py").write_text(f'TEXT = "{OLD_SENTENCE}"\n', encoding="utf-8")
    assert files_with_old_sentence(tmp_path) == []


def test_a_file_with_only_the_opening_sentence_passes(tmp_path):
    folder = tmp_path / "plugins/superclaude/skills"
    folder.mkdir(parents=True)
    (folder / "y.md").write_text(
        "- Grade every review finding as blocking or minor. Grade each finding "
        "by what changes if the flawed text is corrected.\n",
        encoding="utf-8",
    )
    assert files_with_old_sentence(tmp_path) == []
