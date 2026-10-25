"""Tests for the ``sc_cite_check`` block of refs/retry.md (the parent's citation line count).

Each case extracts the fenced bash block from the shipped reference and runs it, so
the text the parent executes is the text these tests check. The fixtures differ only
in their final newline, which is where the Read tool's phantom line N+1, ``wc -l``
and ``awk 'END{print NR}'`` disagree.
"""

import re
import subprocess
import textwrap
from pathlib import Path

import pytest

_RETRY_REF = (
    Path(__file__).resolve().parents[2]
    / "src/superclaude/skills/sc-implement-protocol/refs/retry.md"
)


def block() -> str:
    text = _RETRY_REF.read_text(encoding="utf-8")
    blocks = [
        b
        for b in re.findall(r"```bash\n(.*?)```", text, re.S)
        if "sc_cite_check()" in b
    ]
    assert len(blocks) == 1
    return textwrap.dedent(blocks[0])


def check(code, cwd, name, a, b):
    """Run ``sc_cite_check name a b`` from ``code``; return (exit code, stdout)."""
    p = subprocess.run(
        ["bash", "-c", code + '\nsc_cite_check "$@"', "_", name, str(a), str(b)],
        cwd=cwd,
        capture_output=True,
        text=True,
    )
    return p.returncode, p.stdout.strip()


@pytest.fixture
def files(tmp_path):
    (tmp_path / "x.log").write_bytes(b"a\nb\nc\n")  # 3 lines, final newline
    (tmp_path / "y.log").write_bytes(b"a\nb\nc")  # wc -l says 2, awk says 3
    (tmp_path / "z.log").write_bytes(b"a\nb\n\n")  # line 3 is a real empty line
    (tmp_path / "a=b").write_bytes(b"a\nb\nc\n")  # looks like an awk assignment
    (tmp_path / "-x").write_bytes(b"a\nb\nc")  # looks like an option, no final newline
    (tmp_path / "nul.log").write_bytes(b"a\nb\0")  # ends in a NUL byte, no newline
    return tmp_path


CASES = [
    ("x.log", 1, 3, 0, "OK x.log:1-3"),
    ("x.log", 3, 3, 0, "OK x.log:3-3"),
    ("x.log", 1, 4, 0, "CLAMPED x.log:1-4 -> 1-3"),
    ("x.log", 4, 4, 1, "FAIL x.log:4-4 (file has 3 lines)"),
    ("x.log", 1, 5, 1, "FAIL x.log:1-5 (file has 3 lines)"),
    ("x.log", 0, 3, 1, "FAIL x.log:0-3 (file has 3 lines)"),
    ("y.log", 1, 3, 0, "OK y.log:1-3"),
    ("y.log", 1, 4, 1, "FAIL y.log:1-4 (file has 3 lines)"),
    ("z.log", 1, 3, 0, "OK z.log:1-3"),
    ("z.log", 1, 4, 0, "CLAMPED z.log:1-4 -> 1-3"),
    ("z.log", 1, 5, 1, "FAIL z.log:1-5 (file has 3 lines)"),
    ("nope.log", 1, 1, 1, "FAIL nope.log (missing)"),
    ("a=b", 1, 3, 0, "OK a=b:1-3"),
    ("x.log", "01", "03", 0, "OK x.log:01-03"),
    (
        "x.log",
        1,
        18446744073709551619,
        1,
        "FAIL x.log:1-18446744073709551619 (file has 3 lines)",
    ),
    ("-x", 1, 4, 1, "FAIL -x:1-4 (file has 3 lines)"),
    ("nul.log", 1, 3, 1, "FAIL nul.log:1-3 (file has 2 lines)"),
]


@pytest.mark.parametrize("name,a,b,rc,out", CASES)
def test_cite_check(files, name, a, b, rc, out):
    assert check(block(), files, name, a, b) == (rc, out)


def test_mutant_without_the_clamp_branch(files):
    code = "\n".join(ln for ln in block().splitlines() if "CLAMPED" not in ln)
    assert code != block()
    assert check(block(), files, "x.log", 1, 4)[0] == 0
    assert check(code, files, "x.log", 1, 4)[0] == 1


def test_mutant_counting_with_wc(files):
    code = block().replace("awk 'END{print NR}' < \"$f\"", 'wc -l < "$f"')
    assert code != block()
    assert check(block(), files, "y.log", 1, 3)[0] == 0
    assert check(code, files, "y.log", 1, 3)[0] == 1


def test_step_4_text_names_the_count_and_the_clamp():
    text = _RETRY_REF.read_text(encoding="utf-8")
    assert "one Read per citation" not in text
    step4 = text.split("4. **Parent check**", 1)[1].split("5. **Procedure step 5", 1)[0]
    prose = re.sub(r"```bash\n.*?```", "", step4, flags=re.S)
    assert "awk 'END{print NR}'" in prose
    assert "citation clamped: f:a-b -> a-N (Read phantom line)" in prose


_ADVISER = (
    Path(__file__).resolve().parents[2]
    / "src/superclaude/agents/implement-retry-adviser.md"
)


def phantom_rule_present(agent_text: str) -> bool:
    """True when the adviser's rules list carries the Read phantom-line rule."""
    return "extra empty line" in agent_text and "last line that has text" in agent_text


def test_adviser_carries_the_phantom_line_rule():
    text = _ADVISER.read_text(encoding="utf-8")
    assert phantom_rule_present(text)
    # in-test mutant: the same text with the rule sentence deleted from the string only
    rule = next(ln for ln in text.splitlines() if "extra empty line" in ln)
    assert not phantom_rule_present(text.replace(rule + "\n", ""))
