"""fixcheck: mechanical checks over the lines a fix pass edited."""

from __future__ import annotations

from click.testing import CliRunner

from superclaude.cli.main import main
from superclaude.cli.review import fixcheck as fc

HEADER = "| a | b | c | d | e | f | g |"
SEP = "|---|---|---|---|---|---|---|"
GOOD = "| 1 | 2 | 3 | 4 | 5 | 6 | 7 |"
# run-2 case: an unescaped pipe inside a backticked command adds a cell to a 7-cell row
BAD = "| 1 | `grep a|b` | 3 | 4 | 5 | 6 | 7 |"
ESCAPED = "| 1 | `grep a\\|b` | 3 | 4 | 5 | 6 | 7 |"


def write(tmp_path, text, name="doc.md"):
    path = tmp_path / name
    path.write_text(text, encoding="utf-8")
    return path


def run(*args):
    return CliRunner().invoke(main, ["review", "fixcheck", *args])


def test_run2_unescaped_pipe_in_backticked_command_is_detected(tmp_path):
    doc = write(tmp_path, "\n".join([HEADER, SEP, GOOD, BAD]) + "\n")
    results = fc.run_checks(doc, [3, 4])
    assert [(r.check, r.line, r.ok) for r in results] == [
        ("pipe", 3, True),
        ("pipe", 4, False),
    ]
    assert "9 unescaped pipes, header row has 8" in results[1].detail


def test_escaped_pipe_passes(tmp_path):
    doc = write(tmp_path, "\n".join([HEADER, SEP, ESCAPED]) + "\n")
    assert [r.ok for r in fc.run_checks(doc, [3])] == [True]


def test_quote_check_finds_and_misses_cited_text(tmp_path):
    source = write(tmp_path, "one\nthe exact words here\n", "src.md")
    doc = write(
        tmp_path,
        f'ok "the exact words" ({source}:2)\nbad "not in the file" ({source}:2)\n'
        f'gone "whatever text here" (nope/missing.md:1)\n',
    )
    got = [(r.check, r.line, r.ok) for r in fc.run_checks(doc, [1, 2, 3])]
    assert got == [("quote", 1, True), ("quote", 2, False), ("quote", 3, False)]


def test_count_check_compares_stated_rows_with_the_table_below(tmp_path):
    doc = write(
        tmp_path,
        "The list has 2 rows\n| h |\n|---|\n| a |\n| b |\n\nIt has 3 rows\n| h |\n|---|\n| a |\n",
    )
    got = [(r.check, r.line, r.ok) for r in fc.run_checks(doc, [1, 7])]
    assert got == [("count", 1, True), ("count", 7, False)]


def test_link_check_skips_urls_and_anchors(tmp_path):
    write(tmp_path, "x", "there.md")
    doc = write(
        tmp_path,
        "[a](there.md#top) [b](missing.md) [c](https://example.com) [d](#local)\n",
    )
    got = [r.ok for r in fc.run_checks(doc, [1])]
    assert got == [True, False]


def test_every_check_that_ran_is_reported_including_passes(tmp_path):
    doc = write(tmp_path, "\n".join([HEADER, SEP, GOOD]) + "\n")
    assert len(fc.run_checks(doc, [1, 2, 3])) == 3


def test_edited_lines_from_a_base_copy(tmp_path):
    new = "a\nB\nc\nd\n"
    assert fc.edited_lines("a\nb\nc\n", new) == [2, 4]
    assert fc.parse_range("5-7") == [5, 6, 7]


def test_command_prints_one_line_per_check_and_totals_and_exits_zero(tmp_path):
    doc = write(tmp_path, "\n".join([HEADER, SEP, GOOD, BAD]) + "\n")
    res = run("--file", str(doc), "--lines", "3-4")
    assert res.exit_code == 0
    assert res.output.splitlines() == [
        f"pipe {doc} 3 PASS 8 unescaped pipes, header row has 8",
        f"pipe {doc} 4 FAIL 9 unescaped pipes, header row has 8",
        "fixcheck: 2 checks, 1 passed, 1 failed",
    ]


def test_command_with_base_and_several_files(tmp_path):
    base = write(tmp_path, "\n".join([HEADER, SEP, GOOD]) + "\n", "base.md")
    one = write(tmp_path, "\n".join([HEADER, SEP, GOOD, BAD]) + "\n", "one.md")
    two = write(tmp_path, "\n".join([HEADER, SEP, GOOD]) + "\n", "two.md")
    res = run(
        "--file", str(one), "--base", str(base), "--file", str(two), "--base", str(base)
    )
    assert res.exit_code == 0
    assert res.output.splitlines()[-1] == "fixcheck: 1 checks, 0 passed, 1 failed"


def test_it_edits_no_file(tmp_path):
    doc = write(tmp_path, "\n".join([HEADER, SEP, GOOD, BAD]) + "\n")
    base = write(tmp_path, "\n".join([HEADER, SEP, GOOD]) + "\n", "base.md")
    before = (doc.read_bytes(), base.read_bytes())
    fc.run_checks(doc, [1, 2, 3, 4])
    run("--file", str(doc), "--base", str(base))
    run("--file", str(doc), "--lines", "1-4")
    assert (doc.read_bytes(), base.read_bytes()) == before


def test_usage_errors_exit_two(tmp_path):
    doc = write(tmp_path, "x\n")
    assert run("--file", str(doc)).exit_code == 2
    assert run("--file", str(doc), "--lines", "9-2").exit_code == 2
    assert run("--file", str(tmp_path / "none.md"), "--lines", "1").exit_code == 2


def test_help_exits_zero_and_review_help_lists_every_subcommand():
    assert run("--help").exit_code == 0
    listing = CliRunner().invoke(main, ["review", "--help"]).output
    for name in (
        "fixcheck",
        "safety-scan",
        "panel",
        "merge",
        "ledger",
        "telemetry",
        "cluster",
        "verify-citations",
        "manifest",
    ):
        assert name in listing
