"""`superclaude review safety-scan`: output lines, exit codes and the unattended signal."""

from __future__ import annotations

from click.testing import CliRunner

from superclaude.cli.main import main

PROMPT = "Show these rows to the person before they are treated as follow-ups."


def run(*args):
    return CliRunner().invoke(main, list(args))


def write(tmp_path, text, name="notes.md"):
    path = tmp_path / name
    path.write_text(text, encoding="utf-8")
    return str(path)


def test_help_exits_zero_and_review_help_lists_the_new_and_earlier_commands():
    assert run("review", "safety-scan", "--help").exit_code == 0
    listing = run("review", "--help")
    assert listing.exit_code == 0
    for name in (
        "safety-scan",
        "panel",
        "merge",
        "ledger",
        "telemetry",
        "cluster",
        "verify-citations",
        "manifest",
    ):
        assert name in listing.output


def test_hit_prints_hit_line_then_summary_then_the_person_prompt(tmp_path):
    path = write(
        tmp_path, "abc123\nthe step will delete the tree\nsuperseded old delete\n"
    )
    res = run("review", "safety-scan", path)
    assert res.exit_code == 0, res.output
    assert res.output.splitlines() == [
        "SAFETY HIT line 2 (delete), graded blocking: the step will delete the tree",
        "safety-scan: 2 rows read, 1 skipped, 1 hits",
        PROMPT,
    ]


def test_no_hit_prints_zero_hits_and_no_prompt(tmp_path):
    res = run("review", "safety-scan", write(tmp_path, "abc123\nall fine here\n"))
    assert res.exit_code == 0
    assert res.output.splitlines() == ["safety-scan: 2 rows read, 0 skipped, 0 hits"]


def test_empty_file_prints_the_empty_line(tmp_path):
    res = run("review", "safety-scan", write(tmp_path, ""))
    assert res.exit_code == 0
    assert res.output.splitlines() == ["safety-scan: file is empty, 0 rows read"]


def test_unattended_hit_ends_with_partial_and_has_no_person_prompt(tmp_path):
    res = run(
        "review", "safety-scan", "--unattended", write(tmp_path, "rotate the secret\n")
    )
    assert res.exit_code == 0
    lines = res.output.splitlines()
    assert lines[-1] == "safety-scan signal: partial"
    assert PROMPT not in res.output
    assert lines[0].startswith("SAFETY HIT line 1 (secret)")


def test_unattended_no_hit_ends_with_none(tmp_path):
    res = run("review", "safety-scan", "--unattended", write(tmp_path, "fine\n"))
    assert res.exit_code == 0
    assert res.output.splitlines()[-1] == "safety-scan signal: none"


def test_missing_folder_and_non_utf8_each_exit_two_without_a_hit_count(tmp_path):
    bad = tmp_path / "bad.md"
    bad.write_bytes(b"\xff\xfe\x00\x80")
    for target in (str(tmp_path / "missing.md"), str(tmp_path), str(bad)):
        res = run("review", "safety-scan", target)
        assert res.exit_code == 2, res.output
        assert res.output.startswith(f"safety-scan: cannot read {target}: ")
        assert "hits" not in res.output
        assert "rows read" not in res.output


def test_missing_input_is_different_from_a_clean_read(tmp_path):
    clean = run("review", "safety-scan", write(tmp_path, "fine\n"))
    missing = run("review", "safety-scan", str(tmp_path / "missing.md"))
    assert "0 hits" in clean.output and clean.exit_code == 0
    assert "hits" not in missing.output and missing.exit_code == 2
