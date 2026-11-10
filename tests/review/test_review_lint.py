"""Tests for ``superclaude review lint`` (PN2, #346): deterministic requirements lint.

One small positive and one negative inline sample per check, plus schema, ordering,
determinism, CLI behavior and the exit codes. Pinned regressions on real documents
live in ``test_review_lint_pinned.py``.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from click.testing import CliRunner

from superclaude.cli.review.lint import (
    CHECKS,
    SCHEMA,
    parse_checks,
    render_json,
    render_md,
    run_lint_text,
)
from superclaude.cli.review.lint_cmd import command as lint_command


def _flags(text: str, check: str) -> list[dict]:
    result = run_lint_text(text, checks=(check,))
    return [f for f in result["findings"] if f["check"] == check]


# --- REF ---------------------------------------------------------------------

REF_BASE = """\
## 1. Rules

| ID | Requirement |
|---|---|
| WC-1 | Write the report. |
| WC-2 | Follow {ref}. |
"""


def test_ref_flags_an_undefined_id():
    found = _flags(REF_BASE.format(ref="WC-9"), "REF")
    assert [f["lint_id"] for f in found] == ["LINT-REF-1"]
    assert found[0]["class"] == "fact"
    assert found[0]["lines"] == [6, 6]
    assert "WC-9" in found[0]["message"]


def test_ref_accepts_a_defined_id():
    assert _flags(REF_BASE.format(ref="WC-1"), "REF") == []


def test_ref_accepts_ids_defined_by_bold_line_start_and_heading_number():
    text = "## 2. Rules\n\n**FR-1 Name.** text\n\nSee FR-1 and section 2.\n"
    assert _flags(text, "REF") == []


def test_ref_flags_an_undefined_section_and_accepts_a_defined_one():
    bad = "## 1. A\n\nSee section 4.1 for details.\n"
    good = "## 1. A\n\nSee section 4.1 for details.\n\n### 4.1 Details\n"
    assert len(_flags(bad, "REF")) == 1
    assert _flags(good, "REF") == []


def test_ref_flags_a_missing_step():
    base = "### 7.2 Live check\n\n1. one\n2. two\n3. three\n\n## 8. Use\n\nRun {ref}.\n"
    assert _flags(base.format(ref="7.2 step 3"), "REF") == []
    assert len(_flags(base.format(ref="7.2 step 9"), "REF")) == 1


def test_ref_ignores_sha_tokens():
    assert _flags("## 1. A\n\nUses SHA-256 here.\n", "REF") == []


# --- COUNT -------------------------------------------------------------------

COUNT_TABLE = """\
### 3.1 Ready ({n})

| Command | Note |
|---|---|
| a | x |
| b | y |
| c | z |
"""


def test_count_heading_count_versus_table_rows():
    assert len(_flags(COUNT_TABLE.format(n=4), "COUNT")) == 1
    assert _flags(COUNT_TABLE.format(n=3), "COUNT") == []
    flag = _flags(COUNT_TABLE.format(n=4), "COUNT")[0]
    assert flag["class"] == "fact"
    assert flag["lines"] == [1, 1]
    assert flag["other_lines"] == [3, 7]


def test_count_parenthetical_parts_must_sum():
    base = "## 1. A\n\nThe 43 commands in `cmd/` ({a} in `X:3`, 22 in `Y:3`) are listed.\n"
    assert len(_flags(base.format(a=20), "COUNT")) == 1
    assert _flags(base.format(a=21), "COUNT") == []


def test_count_split_into_parts_must_sum():
    base = "## 1. A\n\nThe 43 commands split into 10 ready, {b} changing and 6 other.\n"
    assert len(_flags(base.format(b=26), "COUNT")) == 1
    assert _flags(base.format(b=27), "COUNT") == []


def test_count_all_n_next_to_a_list():
    base = "## 1. A\n\nThe checks are all {n} items:\n\n- one\n- two\n- three\n"
    assert len(_flags(base.format(n=4), "COUNT")) == 1
    assert _flags(base.format(n=3), "COUNT") == []


# --- KV ----------------------------------------------------------------------

KV_BASE = """\
## 1. First

The `timeout` = 10 seconds.

## 2. Second

The `timeout` = {v} seconds.
"""


def test_kv_same_key_two_values_in_different_sections():
    found = _flags(KV_BASE.format(v=30), "KV")
    assert found and all(f["class"] == "possible" for f in found)
    assert _flags(KV_BASE.format(v=10), "KV") == []


def test_kv_same_section_is_not_a_conflict():
    text = "## 1. First\n\nThe `timeout` = 10 here.\n\nThe `timeout` = 30 there.\n"
    assert _flags(text, "KV") == []


def test_kv_quantity_with_unit_and_head_word():
    base = "## 1. A\n\nA failed call is retried at most 5 times.\n\n## 2. B\n\nA failed call is retried at most {n} times.\n"
    assert len(_flags(base.format(n=8), "KV")) == 1
    assert _flags(base.format(n=5), "KV") == []


def test_kv_table_cells_are_not_bindings():
    """Tuning pass 2: table cells carry column semantics, so a table row never binds a key."""
    base = (
        "## 1. A\n\n| Key | Value |\n|---|---|\n| `mode` | fast |\n\n"
        "## 2. B\n\n| Key | Value |\n|---|---|\n| `mode` | {v} |\n"
    )
    assert _flags(base.format(v="slow"), "KV") == []


def test_kv_quantity_needs_two_shared_head_words():
    base = (
        "## 1. A\n\nA failed delivery is retried at most 5 times.\n\n"
        "## 2. B\n\nThe worker retries a failed delivery up to {n} times.\n"
    )
    assert len(_flags(base.format(n=8), "KV")) == 1
    other = "## 1. A\n\nA failed call is retried at most 5 times.\n\n## 2. B\n\nA nightly job runs 8 times.\n"
    assert _flags(other, "KV") == []


# --- PHASE -------------------------------------------------------------------

PHASE_DOC = """\
## 6. Phased rollout

| Phase | Scope |
|---|---|
| **P0. Base** | Write the document.{p0} |
| **P2. Later** | Add the WC-9 contract. |

## 7. Acceptance

| Phase | ID | Check |
|---|---|---|
| P0 | AC-0.1 | Needs WC-9 to pass. |
"""


def test_phase_flags_a_reference_to_a_later_phase():
    found = _flags(PHASE_DOC.format(p0=""), "PHASE")
    assert len(found) == 1
    assert found[0]["class"] == "fact"
    assert "WC-9" in found[0]["message"] and "P2" in found[0]["message"]


def test_phase_accepts_a_reference_introduced_in_the_same_phase():
    assert _flags(PHASE_DOC.format(p0=" Define WC-9."), "PHASE") == []


# --- PATH --------------------------------------------------------------------

PATH_DOC = """\
| ID | Requirement |
|---|---|
| WC-4 | Write `<output-dir>/return-contract.yaml` or `.dev/tasks/<id>/return-contract.yaml`. |
| X-1 | Report is {p}. |
"""


def test_path_flags_a_same_basename_path_that_fits_no_template():
    found = _flags(PATH_DOC.format(p="`<out>/adversarial/return-contract.yaml`"), "PATH")
    assert len(found) == 1
    assert found[0]["class"] == "possible"
    assert found[0]["other_lines"] == [3, 3]


def test_path_accepts_a_path_that_fits_one_template_of_the_family():
    assert _flags(PATH_DOC.format(p="`<out>/return-contract.yaml`"), "PATH") == []
    assert _flags(PATH_DOC.format(p="`.dev/tasks/<n>/return-contract.yaml`"), "PATH") == []


def test_path_ignores_a_bare_file_name():
    assert _flags(PATH_DOC.format(p="`return-contract.yaml`"), "PATH") == []


# --- RFC ---------------------------------------------------------------------


def test_rfc_census_counts_per_section_and_never_flags():
    text = "## 1. A\n\nIt MUST work and SHOULD be fast. It MUST NOT fail.\n\n## 2. B\n\nIt MAY help.\n"
    result = run_lint_text(text, checks=("RFC",))
    assert result["findings"] == []
    census = result["census"]["rfc2119"]
    assert census["1"] == {"MUST": 2, "SHALL": 0, "SHOULD": 1, "MAY": 0}
    assert census["2"] == {"MUST": 0, "SHALL": 0, "SHOULD": 0, "MAY": 1}


# --- schema, ordering, determinism ---------------------------------------------

MIXED = REF_BASE.format(ref="WC-9") + "\n" + COUNT_TABLE.format(n=4)


def test_schema_keys_and_ordering():
    result = run_lint_text(MIXED)
    assert list(result) == ["schema", "doc_sha256", "doc_bytes", "checks", "findings", "census"]
    assert result["schema"] == SCHEMA == "review-lint/1"
    assert result["checks"] == list(CHECKS)
    assert result["doc_bytes"] == len(MIXED.encode("utf-8"))
    keys = ["lint_id", "check", "class", "lines", "quote", "other_lines", "message"]
    assert result["findings"], "mixed sample must flag something"
    for f in result["findings"]:
        assert list(f) == keys
        assert len(f["quote"]) <= 200
    order = [(f["lines"][0], f["check"]) for f in result["findings"]]
    assert order == sorted(order, key=lambda t: (t[0], CHECKS.index(t[1])))
    per_check: dict[str, list[str]] = {}
    for f in result["findings"]:
        per_check.setdefault(f["check"], []).append(f["lint_id"])
    for check, ids in per_check.items():
        assert ids == [f"LINT-{check}-{i}" for i in range(1, len(ids) + 1)]


def test_output_is_byte_identical_twice():
    a = run_lint_text(MIXED)
    b = run_lint_text(MIXED)
    assert render_json(a) == render_json(b)
    assert render_md(a) == render_md(b)


def test_md_format_first_line_and_blocks():
    result = run_lint_text(MIXED)
    md = render_md(result)
    assert md.splitlines()[0] == f"lint: superclaude review lint, review-lint/1, sha256 {result['doc_sha256']}"
    for f in result["findings"]:
        assert f"### {f['lint_id']}" in md
    assert "census" in md.lower()


def test_checks_filter_in_library():
    result = run_lint_text(MIXED, checks=("COUNT",))
    assert result["checks"] == ["COUNT"]
    assert {f["check"] for f in result["findings"]} == {"COUNT"}


def test_parse_checks():
    assert parse_checks(None) == CHECKS
    assert parse_checks("count, REF") == ("REF", "COUNT")
    with pytest.raises(ValueError):
        parse_checks("NOPE")


# --- CLI ---------------------------------------------------------------------


def _write(tmp_path: Path, text: str = MIXED) -> Path:
    p = tmp_path / "doc.md"
    p.write_text(text, encoding="utf-8")
    return p


def test_cli_json_exit_zero_and_valid(tmp_path):
    r = CliRunner().invoke(lint_command, [str(_write(tmp_path)), "--format", "json"])
    assert r.exit_code == 0
    assert json.loads(r.output)["schema"] == "review-lint/1"


def test_cli_exit_zero_even_with_findings(tmp_path):
    r = CliRunner().invoke(lint_command, [str(_write(tmp_path)), "--format", "md"])
    assert r.exit_code == 0
    assert r.output.splitlines()[0].startswith("lint: superclaude review lint, review-lint/1, sha256 ")
    assert "### LINT-" in r.output


def test_cli_out_writes_file(tmp_path):
    out = tmp_path / "sub" / "lint-1.md"
    r = CliRunner().invoke(lint_command, [str(_write(tmp_path)), "--format", "md", "--out", str(out)])
    assert r.exit_code == 0
    assert out.read_text(encoding="utf-8").startswith("lint: superclaude review lint, review-lint/1, sha256 ")


def test_cli_checks_filter(tmp_path):
    r = CliRunner().invoke(lint_command, [str(_write(tmp_path)), "--format", "json", "--checks", "COUNT"])
    data = json.loads(r.output)
    assert data["checks"] == ["COUNT"]
    assert {f["check"] for f in data["findings"]} == {"COUNT"}


def test_cli_missing_file_exit_two(tmp_path):
    r = CliRunner().invoke(lint_command, [str(tmp_path / "nope.md")])
    assert r.exit_code == 2


def test_cli_file_over_two_mb_exit_two(tmp_path):
    big = tmp_path / "big.md"
    big.write_bytes(b"x" * (2 * 1024 * 1024 + 1))
    r = CliRunner().invoke(lint_command, [str(big)])
    assert r.exit_code == 2


def test_cli_exactly_two_mb_is_accepted(tmp_path):
    ok = tmp_path / "ok.md"
    ok.write_bytes(b"x" * (2 * 1024 * 1024))
    r = CliRunner().invoke(lint_command, [str(ok), "--checks", "RFC"])
    assert r.exit_code == 0


def test_cli_reachable_as_superclaude_review_lint(tmp_path):
    from superclaude.cli.main import main

    r = CliRunner().invoke(main, ["review", "lint", str(_write(tmp_path)), "--format", "md"])
    assert r.exit_code == 0, r.output
    assert "review-lint/1" in r.output


def test_review_group_lists_lint():
    from superclaude.cli.main import main

    r = CliRunner().invoke(main, ["review", "--help"])
    assert r.exit_code == 0
    assert "lint" in r.output
