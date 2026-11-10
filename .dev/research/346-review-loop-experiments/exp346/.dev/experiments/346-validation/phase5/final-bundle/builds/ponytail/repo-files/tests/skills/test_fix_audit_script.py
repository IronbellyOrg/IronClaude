"""Behavior tests for sc-fix-audit's fix_audit.py (issue 346, team ponytail).

Enforcement type: EXECUTABLE (script behavior on tmp_path fixtures).
"""

from __future__ import annotations

import ast
import filecmp
import importlib.util
import json
import re
import subprocess
import sys
from pathlib import Path

import pytest

_REPO = Path(__file__).resolve().parents[2]
_SKILL = _REPO / "src/superclaude/skills/sc-fix-audit"
_SCRIPT = _SKILL / "scripts/fix_audit.py"
_spec = importlib.util.spec_from_file_location("fix_audit", _SCRIPT)
fa = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(fa)

# The plan package moves from to-do/ to done/ when archived; find it in either.
_PKG_SOURCES = sorted(_REPO.glob(".dev/tasks/*/TASK-WF-spec-20261108-181547/source.md"))

R2_HEAD = "# Review\n\nreview: 2 of 3 (re-review of round 1)\n\n"
R2_TAIL = "\nverdict: FAIL\n"


def run(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(_SCRIPT), *args], capture_output=True, text=True
    )


def write(p: Path, text: str) -> Path:
    p.write_bytes(text.encode("utf-8"))
    return p


def prepare(tmp_path: Path, base: str, cur: str, report: str, disp: str | None = None):
    b = write(tmp_path / "v2.md", base)
    s = write(tmp_path / "spec.md", cur)
    r = write(tmp_path / "round2.md", report)
    d = tmp_path / "fix-audit"
    args = [
        "prepare",
        "--baseline",
        str(b),
        "--current",
        str(s),
        "--report",
        str(r),
        "--out",
        str(d),
    ]
    if disp is not None:
        args += ["--dispositions", str(write(tmp_path / "disp.md", disp))]
    res = run(*args)
    state = (
        json.loads((d / "state.json").read_text())
        if (d / "state.json").exists()
        else None
    )
    return res, d, state


def report(rows: str) -> str:
    return (
        R2_HEAD
        + "## New findings\n\n| id | severity | grade |\n|---|---|---|\n"
        + rows
        + R2_TAIL
    )


# ---------- brief and imports ----------


@pytest.mark.skipif(
    not _PKG_SOURCES, reason="plan package source.md not in this checkout"
)
def test_brief_equals_source_section_2_4():
    src = _PKG_SOURCES[0].read_text(encoding="utf-8").splitlines()
    start = src.index(
        "### 2.4 The brief handed to the ponytail auditor (exact text; stored once in `sc-fix-audit/refs/auditor-brief.md`)"
    )
    open_ = src.index("```text", start)
    close = src.index("```", open_ + 1)
    brief = (_SKILL / "refs/auditor-brief.md").read_text(encoding="utf-8").splitlines()
    assert brief == src[open_ + 1 : close]


def test_brief_has_placeholders_and_no_src_path():
    text = (_SKILL / "refs/auditor-brief.md").read_text(encoding="utf-8")
    for ph in ("<D>", "<R>", "<DISP>", "<B>", "<S>"):
        assert ph in text
    assert "src/superclaude" not in text


def test_script_imports_only_stdlib():
    allowed = {
        "__future__",
        "argparse",
        "difflib",
        "hashlib",
        "json",
        "os",
        "re",
        "sys",
        "tempfile",
        "pathlib",
    }
    tree = ast.parse(_SCRIPT.read_text(encoding="utf-8"))
    names = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names |= {a.name.split(".")[0] for a in node.names}
        elif isinstance(node, ast.ImportFrom):
            names.add(node.module.split(".")[0])
    assert names <= allowed, names - allowed


# ---------- trigger and hunks ----------


def test_empty_diff_not_triggered_writes_only_state(tmp_path):
    res, d, state = prepare(
        tmp_path, "a\nb\n", "a\nb\n", report("| N1 | MINOR | non-blocking |\n")
    )
    assert res.returncode == 0
    assert state["audit"] == "not-triggered(empty diff)"
    assert sorted(p.name for p in d.iterdir()) == ["state.json"]


def test_whitespace_only_diff_not_triggered(tmp_path):
    res, d, state = prepare(
        tmp_path,
        "a\n\nb\n",
        "a\n   \n\n\nb\n",
        report("| N1 | MINOR | non-blocking |\n"),
    )
    assert res.returncode == 0
    assert state["audit"] == "not-triggered(empty diff)"
    assert sorted(p.name for p in d.iterdir()) == ["state.json"]


@pytest.mark.parametrize(
    "rep,reason",
    [
        (
            "review: 1 of 3\n| N1 | MINOR | non-blocking |\nverdict: FAIL\n",
            "not review 2 of 3",
        ),
        (
            R2_HEAD + "| N1 | MINOR | non-blocking |\nverdict: PASS\n",
            "review 2 did not fail",
        ),
    ],
)
def test_report_trigger_rules(tmp_path, rep, reason):
    res, d, state = prepare(tmp_path, "a\n", "a\nN1 fix\n", rep)
    assert res.returncode == 0 and state["audit"] == f"not-triggered({reason})"
    assert sorted(p.name for p in d.iterdir()) == ["state.json"]


def test_insert_delete_replace_hunks():
    b = fa.split_lines("one\ntwo\nthree\nfour\n")
    s = fa.split_lines("zero\none\nTWO\nthree\n")
    tags = [(h["tag"], h["s"], h["b"]) for h in fa.hunks_of(b, s)]
    assert tags == [
        ("insert", [0, 1], [0, 0]),
        ("replace", [2, 3], [1, 2]),
        ("delete", [4, 4], [3, 4]),
    ]


def test_current_before_audit_is_byte_copy(tmp_path):
    cur = "line\r\nN1 fix é\r\nend"
    res, d, state = prepare(
        tmp_path,
        "line\r\nend",
        cur,
        report("| N1 | MINOR | non-blocking |\n"),
        disp="| id | Where |\n|---|---|\n",
    )
    assert res.returncode == 0 and state["audit"] == "prepared"
    assert filecmp.cmp(
        d / "current-before-audit.md", tmp_path / "spec.md", shallow=False
    )
    assert state["sha256_current"] == fa.sha256(tmp_path / "spec.md")


# ---------- id rule ----------


@pytest.mark.parametrize("tok", ["N12", "C9", "R2-1", "C-R3-15"])
def test_id_tokens_match(tok):
    assert fa.id_tokens(f"see {tok}, and ({tok}).") == [tok, tok]


@pytest.mark.parametrize(
    "text", ["12 and 345", "N12x", "xN12", "abc N", "Section", "n12"]
)
def test_id_tokens_reject_numbers_and_partial_words(text):
    assert fa.id_tokens(text) == []


def test_range_expanded():
    assert fa.id_tokens("fixes N1-N11") == [f"N{i}" for i in range(1, 12)]


def test_baseline_id_is_context_not_citation(tmp_path):
    rep = report("| N1 | MAJOR | blocking |\n| N2 | MINOR | non-blocking |\n")
    res, d, state = prepare(
        tmp_path, "rule per N1.\n", "rule per N1, now clearer (N2).\n", rep, disp=""
    )
    assert state["hunks"][0]["cited"] == ["N2"]
    assert state["hunks"][0]["class"] == "minor-only"


def test_prior_table_only_id_is_not_defined_and_makes_foreign_id(tmp_path):
    rep = (
        R2_HEAD
        + "## Prior findings\n\n| id | fixed | status |\n|---|---|---|\n| F16 | no | open |\n"
        + "## New findings\n\n| N1 | MINOR | non-blocking |\n"
        + R2_TAIL
    )
    res, d, state = prepare(tmp_path, "a\n", "a\nfix for F16\n", rep, disp="")
    assert "F16" not in state["ids"] and state["prior_only"] == ["F16"]
    assert state["hunks"][0]["class"] == "foreign-id"


def test_prior_status_row_without_heading_is_prior_only():
    parsed = fa.parse_report("| F16 | no | open |\n| N1 | MAJOR | blocking |\n")
    assert parsed["prior"] == [["F16", "open"]] and list(parsed["graded"]) == ["N1"]


# ---------- grade parse ----------


@pytest.mark.parametrize(
    "line,label,blocking",
    [
        ("| N1 | MAJOR | blocking |", "MAJOR", True),
        ("N2 (CRITICAL, blocking): the rule is missing.", "CRITICAL", True),
        ("**C9.** Severity MAJOR, blocking. The table is wrong.", "MAJOR", True),
        ("N4 (MAJOR, B): the cap is wrong", "MAJOR", True),
        ("N5 (MINOR, M): wording", "MINOR", False),
        ("| N6 | MINOR | non-blocking |", "MINOR", False),
    ],
)
def test_four_grade_formats(line, label, blocking):
    g = fa.parse_report("Key: B = blocking, M = minor\n" + line + "\n")["graded"]
    rid = fa.id_tokens(line)[0]
    assert g[rid]["label"] == label and g[rid]["blocking"] is blocking


@pytest.mark.parametrize(
    "line",
    [
        "| N7 | MAJOR | |",
        "| N7 | MAJOR | blocking | non-blocking |",
        "| N7 | MAJOR, MINOR | non-blocking |",
    ],
)
def test_unknown_or_conflicting_grade_is_blocking(line):
    assert fa.parse_report(line + "\n")["graded"]["N7"]["blocking"] is True


def test_fr8_graded_minor_is_protected_and_blocking_involved(tmp_path):
    rep = report("| N3 | MAJOR (FR-8 GAP) | non-blocking |\n")
    res, d, state = prepare(tmp_path, "a\n", "a\nN3 fix\n", rep, disp="")
    g = state["ids"]["N3"]
    assert g["blocking"] is False and g["protected"] is True and g["label"] == "MAJOR"
    assert state["hunks"][0]["class"] == "blocking-involved"


def test_critical_is_protected():
    g = fa.parse_report("| N8 | CRITICAL | non-blocking |\n")["graded"]["N8"]
    assert g["protected"] is True


# ---------- classes and guard ----------

MIXED_REPORT = report(
    "| N1 | MINOR | non-blocking |\n| N2 | MAJOR | blocking |\n| N3 | MINOR | non-blocking |\n"
).replace(
    "## New findings", "## Prior findings\n\n| F16 | no | open |\n\n## New findings"
)
MIXED_BASE = "p1\nk1\np2\nk2\np3\nk3\np4\nk4\np5\n"
MIXED_CUR = (
    "p1 N1 tweak\nk1\np2 N2 fix\nk2\np3 F16 fix\nk3\np4 plain change\nk4\np5 N3 tweak\n"
)


def test_four_classes_on_mixed_fixture(tmp_path):
    disp = "| id | Where |\n|---|---|\n| N2 | SPEC':3 |\n"
    res, d, state = prepare(tmp_path, MIXED_BASE, MIXED_CUR, MIXED_REPORT, disp=disp)
    assert res.returncode == 0, res.stderr
    assert [h["class"] for h in state["hunks"]] == [
        "minor-only",
        "blocking-involved",
        "foreign-id",
        "unattributed",
        "minor-only",
    ]
    fix_list = (d / "fix-list.md").read_text()
    assert "| H1 | 1-1 | 1-1 |" in fix_list and "minor-only" in fix_list


def test_minor_hunk_on_disposition_line_of_blocking_id_is_blocking_involved(tmp_path):
    disp = "| id | Where |\n|---|---|\n| N2 | SPEC':9 |\n"
    res, d, state = prepare(tmp_path, MIXED_BASE, MIXED_CUR, MIXED_REPORT, disp=disp)
    assert state["hunks"][4]["class"] == "blocking-involved"


def test_no_dispositions_file_means_no_minor_only(tmp_path):
    res, d, state = prepare(tmp_path, MIXED_BASE, MIXED_CUR, MIXED_REPORT)
    assert "minor-only" not in [h["class"] for h in state["hunks"]]


@pytest.mark.parametrize(
    "cur,skipped",
    [
        (
            "p1 N1 a\nk1\np2 x\nk2\np3 N3 b\nk3\np4\nk4\np5\n",
            False,
        ),  # 1 of 3 unattributed
        (
            "p1 N1 a\nk1\np2 x\nk2\np3\nk3\np4\nk4\np5\n",
            False,
        ),  # 1 of 2: exactly half, no skip
        ("p1 N1 a\nk1\np2 x\nk2\np3 y\nk3\np4\nk4\np5\n", True),  # 2 of 3
    ],
)
def test_skip_guard(tmp_path, cur, skipped):
    res, d, state = prepare(tmp_path, MIXED_BASE, cur, MIXED_REPORT, disp="")
    assert res.returncode == 0
    assert (state["audit"] == "skipped(ids not citable)") is skipped
    assert (d / "brief.md").exists() is not skipped


def test_brief_has_paths_filled(tmp_path):
    res, d, state = prepare(tmp_path, MIXED_BASE, MIXED_CUR, MIXED_REPORT, disp="")
    brief = (d / "brief.md").read_text()
    for ph in ("<D>", "<R>", "<DISP>", "<B>", "<S>"):
        assert ph not in brief
    assert (
        str(d.resolve()) + "/audit.md" in brief
        and str((tmp_path / "disp.md").resolve()) in brief
    )


def test_unreadable_dispositions_exit_1(tmp_path):
    b = write(tmp_path / "v2.md", MIXED_BASE)
    s = write(tmp_path / "spec.md", MIXED_CUR)
    r = write(tmp_path / "round2.md", MIXED_REPORT)
    res = run(
        "prepare",
        "--baseline",
        str(b),
        "--current",
        str(s),
        "--report",
        str(r),
        "--dispositions",
        str(tmp_path / "missing.md"),
        "--out",
        str(tmp_path / "d"),
    )
    assert res.returncode == 1


# ---------- report shapes of a real review-2 report (flg-r2 style) ----------

FLG_R2_STYLE = (
    R2_HEAD
    + "## Part 1: Prior findings\n\n| id | fixed | status |\n|---|---|---|\n| F16 | no | open |\n\n"
    + "## Part 2: New findings\n\n"
    + "**N1.** MAJOR, blocking: the cap text is missing.\n"
    + "- WC-3: same output location. Not blocking because 2.3 covers it.\n"
    + "N2 (MINOR, non-blocking): wording.\n"
    + "Notes on citations (Part 2) are minor: C9 off by one, C12 and C13 stale.\n\n"
    + "| id | where | severity | blocking |\n|---|---|---|---|\n"
    + "| N7-N9 | 3.6 | MINOR | no |\n| C9, C12, C13 | Part 2 | MINOR | no |\n\n"
    + "Totals: 1 CRITICAL, 5 MAJOR; WC-3 still MINOR; the still-open non-blocking F16.\n"
    + R2_TAIL
)


def test_free_text_lines_define_no_id():
    parsed = fa.parse_report(FLG_R2_STYLE)
    assert "F16" not in parsed["graded"] and "WC-3" not in parsed["graded"]
    assert ["F16", "open"] in parsed["prior"]


def test_every_id_of_an_id_cell_is_graded():
    g = fa.parse_report(FLG_R2_STYLE)["graded"]
    for rid in ("C9", "C12", "C13", "N7", "N8", "N9"):
        assert g[rid] == {"label": "MINOR", "blocking": False, "protected": False}, rid
    assert g["N1"]["blocking"] is True and g["N2"]["blocking"] is False


def test_where_column_with_suffix_is_found():
    disp = "| id | change | Where (revised spec) |\n|---|---|---|\n| N1 | added rule | SPEC':5, SPEC':7-8 |\n| N2 | wording | SPEC':9 |\n"
    assert fa.disposition_lines(disp, {"N1"}) == {5, 7, 8}


def test_prepare_on_flg_r2_style_report(tmp_path):
    base = "p1\nk1\np2\nk2\np3\n"
    cur = "p1 C12 citation fixed\nk1\np2 F16 fix\nk2\np3 N1 rule\n"
    disp = "| id | Where (revised spec) |\n|---|---|\n| N1 | SPEC':5 |\n"
    res, d, state = prepare(tmp_path, base, cur, FLG_R2_STYLE, disp=disp)
    assert res.returncode == 0, res.stderr
    assert [h["class"] for h in state["hunks"]] == [
        "minor-only",
        "foreign-id",
        "blocking-involved",
    ]
    assert state["prior_only"] == ["F16"]


def bullet_report(marker: str) -> str:
    return (
        R2_HEAD
        + "**N9.** MINOR, non-blocking: wording.\n"
        + f"{marker} WC-3: the location rule. Not blocking because 2.3 covers it.\n"
        + R2_TAIL
    )


@pytest.mark.parametrize("marker", ["-", "*", "+"])
def test_bullet_under_a_finding_defines_no_id(marker):
    graded = fa.parse_report(bullet_report(marker))["graded"]
    assert "WC-3" not in graded
    assert graded["N9"]["blocking"] is False


def test_prepare_ignores_bullet_label_and_its_disposition_line(tmp_path):
    disp = "| id | Where |\n|---|---|\n| N9 | SPEC':1 |\n| WC-3 | SPEC':3 |\n"
    res, d, state = prepare(
        tmp_path,
        "p1\nk1\np2\n",
        "p1 N9 tweak\nk1\np2 WC-3 note\n",
        bullet_report("-"),
        disp=disp,
    )
    assert res.returncode == 0, res.stderr
    assert "WC-3" not in state["ids"]
    assert [h["class"] for h in state["hunks"]] == ["minor-only", "unattributed"]
    assert state["audit"] == "prepared"


# ---------- rows that grade nothing (repair of review r3-1) ----------

NOISE_REPORT = (
    R2_HEAD
    + "## 0. Evidence checks\n\n| id | where | result |\n|---|---|---|\n"
    + "| Y13 | sk/task/SKILL.md:47 | downstream offers are non-blocking |\n\n"
    + "## Decisions\n\n| decision | grade | why |\n|---|---|---|\n"
    + "| Grade N8 (AC-C5 vs Usage lines) as MAJOR | MAJOR; minor | split |\n\n"
    + "## New findings\n\n| id | severity | blocking |\n|---|---|---|\n"
    + "| N8 | MAJOR | yes |\n| N9 | MINOR | no |\n"
    + R2_TAIL
)


def test_row_without_severity_label_is_not_graded():
    graded = fa.parse_report(NOISE_REPORT)["graded"]
    assert "Y13" not in graded


def test_free_text_first_cell_defines_no_id():
    graded = fa.parse_report(NOISE_REPORT)["graded"]
    assert "AC-C5" not in graded
    assert graded["N8"]["blocking"] is True and graded["N9"]["blocking"] is False


def test_prepare_hunk_citing_unlabelled_row_id_is_unattributed(tmp_path):
    disp = "| id | Where |\n|---|---|\n| N8 | SPEC':9 |\n"
    res, d, state = prepare(
        tmp_path,
        "p1\nk1\np2\n",
        "p1 Y13 fix\nk1\np2 N9 tweak\n",
        NOISE_REPORT,
        disp=disp,
    )
    assert res.returncode == 0, res.stderr
    assert [h["class"] for h in state["hunks"]] == ["unattributed", "minor-only"]


# ---------- check (K1-K10) ----------

CK_BASE = "alpha one\nk1\nbeta two\nk2\ngamma three\nk3\ndelta four\nk4\n"
CK_CUR = (
    "alpha one extra N1 words\nk1\nbeta two N2 needed rule\nk2\n"
    "gamma three changed\nk3\ndelta four N3 gap fix\nk4\n"
)
CK_REPORT = report(
    "| N1 | MINOR | non-blocking |\n| N2 | MAJOR | blocking |\n"
    "| N3 | MAJOR (FR-8 GAP) | non-blocking |\n"
)
CK_ROWS = {
    "N1": "| N1 | H1 | minor | minor | no | delete all | revert | the added words change no behaviour at all |",
    "N2": "| N2 | H2 | blocking | blocking | yes | none | keep | without it a reader applies the wrong rule |",
    "-": "| - | H3 | - | minor | no | none | keep | wording only |",
    "N3": "| N3 | H4 | minor | minor | yes | drop one word | shrink | the gap note is needed, one word is extra |",
}
CK_EDITS = [
    {"id": "N3", "hunk": "H4", "op": "delete", "old": "N3 gap fix", "new": "N3 gap"}
]


def audit_md(
    rows=None,
    edits=None,
    head="auditor: ponytail-review\nauditor-isolation: own-session\n",
):
    rows = CK_ROWS if rows is None else rows
    edits = CK_EDITS if edits is None else edits
    text = (
        head
        + "| id | hunks | claimed | validated | necessary | smaller alternative | verdict | evidence |\n"
    )
    text += "|---|---|---|---|---|---|---|---|\n" + "\n".join(rows.values()) + "\n"
    if edits:
        text += "\n```json\n" + json.dumps(edits) + "\n```\n"
    return text


@pytest.fixture
def prepped(tmp_path):
    res, d, state = prepare(
        tmp_path, CK_BASE, CK_CUR, CK_REPORT, disp="| id | Where |\n|---|---|\n"
    )
    assert res.returncode == 0, res.stderr
    assert [h["class"] for h in state["hunks"]] == [
        "minor-only",
        "blocking-involved",
        "unattributed",
        "blocking-involved",
    ]
    return d


def check(d: Path, text: str):
    (d / "audit.md").write_text(text, encoding="utf-8")
    spec = Path(json.loads((d / "state.json").read_text())["current"])
    before = fa.sha256(spec)
    res = run("check", "--dir", str(d))
    assert fa.sha256(spec) == before, "check must never write the spec"
    log = (d / "check.log").read_text() if (d / "check.log").exists() else ""
    return res, log, json.loads((d / "state.json").read_text())


def test_valid_audit_is_check_ok(prepped):
    res, log, state = check(prepped, audit_md())
    assert res.returncode == 0, log
    assert log.splitlines()[0] == "CHECK_OK" and state["audit"] == "checked"


def test_downgrade_is_logged_and_passes(prepped):
    rows = dict(
        CK_ROWS, N2="| N2 | H2 | blocking | minor | no | none | keep | wording |"
    )
    res, log, _ = check(prepped, audit_md(rows))
    assert res.returncode == 0, log
    assert "DOWNGRADE N2" in log.splitlines() and "CHECK_OK" in log


def _without(key):
    return {k: v for k, v in CK_ROWS.items() if k != key}


@pytest.mark.parametrize(
    "rows,edits,rule",
    [
        pytest.param(_without("N2"), None, "K3", id="missing-row"),
        pytest.param(
            dict(CK_ROWS, X="| N99 | H1 | minor | minor | no | none | keep | x |"),
            None,
            "K3",
            id="invented-id",
        ),
        pytest.param(
            dict(
                CK_ROWS,
                N2="| N2 | H2 | minor | blocking | yes | none | keep | without it a reader applies the wrong rule |",
            ),
            None,
            "K4",
            id="wrong-claimed",
        ),
        pytest.param(
            dict(
                CK_ROWS,
                N2="| N2 | H2 | blocking | minor | no | none | revert | it only restates an earlier rule here |",
            ),
            None,
            "K6",
            id="revert-blocking-involved",
        ),
        pytest.param(
            dict(
                CK_ROWS,
                **{
                    "-": "| - | H3 | - | minor | no | none | revert | only wording, no behaviour changes |"
                },
            ),
            None,
            "K6",
            id="revert-unattributed",
        ),
        pytest.param(
            dict(
                CK_ROWS,
                N3="| N3 | H4 | minor | minor | no | none | revert | graded minor by the report itself |",
            ),
            [],
            "K6",
            id="revert-protected-fr8",
        ),
        pytest.param(
            None,
            [
                {
                    "id": "N3",
                    "hunk": "H4",
                    "op": "delete",
                    "old": "delta four N3 gap fix",
                    "new": "four N3 gap fix",
                }
            ],
            "K7",
            id="delete-baseline-token",
        ),
        pytest.param(
            dict(
                CK_ROWS,
                N2="| N2 | H2 | blocking | blocking | yes | trim | shrink | without it a reader applies the wrong rule |",
            ),
            CK_EDITS
            + [
                {
                    "id": "N2",
                    "hunk": "H2",
                    "op": "delete",
                    "old": "N2 needed rule",
                    "new": "needed rule",
                }
            ],
            "K7",
            id="delete-drops-blocking-id",
        ),
        pytest.param(
            None,
            [
                {
                    "id": "N3",
                    "hunk": "H4",
                    "op": "restore",
                    "old": "N3 gap fix",
                    "new": "",
                }
            ],
            "K8",
            id="restore-in-blocking-involved",
        ),
        pytest.param(
            dict(
                CK_ROWS,
                N1="| N1 | H1 | minor | minor | no | restore | shrink | the added words change nothing |",
            ),
            CK_EDITS
            + [
                {
                    "id": "N1",
                    "hunk": "H1",
                    "op": "restore",
                    "old": "extra N1 words",
                    "new": "one",
                }
            ],
            "K8",
            id="restore-non-aligned",
        ),
        pytest.param(
            None,
            CK_EDITS
            + [
                {
                    "id": "N3",
                    "hunk": "H4",
                    "op": "delete",
                    "old": "gap fix",
                    "new": "gap",
                }
            ],
            "K9",
            id="overlapping-rows",
        ),
    ],
)
def test_check_failures(prepped, rows, edits, rule):
    res, log, state = check(prepped, audit_md(rows, edits))
    assert res.returncode == 1
    assert any(ln.startswith(f"CHECK_FAIL {rule} ") for ln in log.splitlines()), log
    assert state["audit"] == "skipped(check failed)"


def test_changed_spec_sha_fails_k1(prepped):
    spec = Path(json.loads((prepped / "state.json").read_text())["current"])
    spec.write_bytes(spec.read_bytes() + b"edited by hand\n")
    (prepped / "audit.md").write_text(audit_md(), encoding="utf-8")
    before = fa.sha256(spec)
    res = run("check", "--dir", str(prepped))
    assert res.returncode == 1 and fa.sha256(spec) == before
    assert "CHECK_FAIL K1 spec sha256 changed" in (prepped / "check.log").read_text()


# ---------- apply ----------


def apply_(d: Path):
    return run("apply", "--dir", str(d))


def spec_of(d: Path) -> Path:
    return Path(json.loads((d / "state.json").read_text())["current"])


def test_apply_reverts_and_shrinks(prepped):
    (prepped / "audit.md").write_text(audit_md(), encoding="utf-8")
    res = apply_(prepped)
    assert res.returncode == 0, res.stdout + res.stderr
    assert "audit: applied(reverted=1, shrunk=1, kept=2)" in res.stdout
    text = spec_of(prepped).read_text()
    assert text.splitlines()[0] == "alpha one"  # H1 back to the exact baseline line
    assert "delta four N3 gap\n" in text and "beta two N2 needed rule" in text
    log = (prepped / "apply-log.md").read_text()
    assert f"sha256 before: {fa.sha256(prepped / 'current-before-audit.md')}" in log
    assert f"sha256 after: {fa.sha256(spec_of(prepped))}" in log
    assert "changed lines vs baseline before: 4" in log
    assert "changed lines vs baseline after: 3" in log
    assert (prepped / "closed-minor.txt").read_text() == "N1 MINOR\n"
    assert json.loads((prepped / "state.json").read_text())["audit"].startswith(
        "applied("
    )


def test_revert_restores_exact_baseline_bytes(tmp_path):
    base = "keep\r\nold line é\r\nend"
    cur = "keep\r\nold line é N1 tweak\r\nend"
    res, d, _ = prepare(
        tmp_path, base, cur, report("| N1 | MINOR | non-blocking |\n"), disp=""
    )
    rows = {
        "N1": "| N1 | H1 | minor | minor | no | none | revert | the added words change nothing at all |"
    }
    (d / "audit.md").write_text(audit_md(rows, []), encoding="utf-8")
    assert apply_(d).returncode == 0
    assert spec_of(d).read_bytes() == base.encode("utf-8")


@pytest.mark.parametrize(
    "base,cur",
    [
        ("a\r\nb gap\r\nc\r\n", "a\r\nb N3 gap fix\r\nc\r\n"),  # CRLF
        ("é a\nb gap\nü c\n", "é a\nb N3 gap fix\nü c\n"),  # non-ASCII UTF-8
        ("a\nb gap\nc", "a\nb N3 gap fix\nc"),  # no trailing newline
    ],
)
def test_bytes_outside_the_edit_round_trip(tmp_path, base, cur):
    """Only the edited span changes; line endings, encoding and the last newline stay."""
    rep = report("| N3 | MAJOR (FR-8 GAP) | non-blocking |\n")
    res, d, _ = prepare(tmp_path, base, cur, rep, disp="")
    rows = {
        "N3": "| N3 | H1 | minor | minor | yes | drop a word | shrink | one added word is extra |"
    }
    edits = [
        {"id": "N3", "hunk": "H1", "op": "delete", "old": "N3 gap fix", "new": "N3 gap"}
    ]
    (d / "audit.md").write_text(audit_md(rows, edits), encoding="utf-8")
    res = apply_(d)
    assert res.returncode == 0 and "audit: applied(" in res.stdout, res.stdout
    assert spec_of(d).read_bytes() == cur.replace("N3 gap fix", "N3 gap").encode(
        "utf-8"
    )


def test_second_apply_is_already_applied(prepped):
    (prepped / "audit.md").write_text(audit_md(), encoding="utf-8")
    assert apply_(prepped).returncode == 0
    after = spec_of(prepped).read_bytes()
    log = (prepped / "apply-log.md").read_bytes()
    res = apply_(prepped)
    assert res.returncode == 0 and res.stdout.strip() == "already applied"
    assert (
        spec_of(prepped).read_bytes() == after
        and (prepped / "apply-log.md").read_bytes() == log
    )


def test_no_temp_file_left(prepped):
    (prepped / "audit.md").write_text(audit_md(), encoding="utf-8")
    assert apply_(prepped).returncode == 0
    assert not [
        p.name for p in spec_of(prepped).parent.iterdir() if p.name.endswith(".tmp")
    ]


def test_bad_last_row_leaves_spec_untouched(prepped):
    edits = CK_EDITS + [
        {"id": "N3", "hunk": "H4", "op": "delete", "old": "not in the spec", "new": ""}
    ]
    (prepped / "audit.md").write_text(audit_md(None, edits), encoding="utf-8")
    assert apply_(prepped).returncode == 1
    assert (
        spec_of(prepped).read_bytes()
        == (prepped / "current-before-audit.md").read_bytes()
    )


def test_apply_stop_guard_writes_nothing(prepped, monkeypatch, capsys):
    """Even if the check let a bad row through, apply's own exact-once guard stops."""
    edits = CK_EDITS + [
        {"id": "N3", "hunk": "H4", "op": "delete", "old": "k1\n", "new": ""}
    ]
    edits[-1]["old"] = "k"  # occurs several times in S
    (prepped / "audit.md").write_text(audit_md(None, edits), encoding="utf-8")
    real = fa.run_checks

    def lenient(d, state):
        _, logs, parsed = real(d, state)
        return [], logs, parsed

    monkeypatch.setattr(fa, "run_checks", lenient)
    assert fa.main(["apply", "--dir", str(prepped)]) == 1
    assert "APPLY_STOP: nothing written" in capsys.readouterr().out
    assert (
        spec_of(prepped).read_bytes()
        == (prepped / "current-before-audit.md").read_bytes()
    )
    assert not (prepped / "apply-log.md").exists()


def test_shared_hunk_is_not_reverted_and_not_closed(tmp_path):
    base = "one\nk\ntwo\n"
    cur = "one N1 N2 words\nk\ntwo N1 more\n"
    rep = report("| N1 | MINOR | non-blocking |\n| N2 | MINOR | non-blocking |\n")
    res, d, state = prepare(tmp_path, base, cur, rep, disp="")
    assert [h["class"] for h in state["hunks"]] == ["minor-only", "minor-only"]
    rows = {
        "N1": "| N1 | H1, H2 | minor | minor | no | none | revert | the added words change nothing at all |",
        "N2": "| N2 | H1 | minor | minor | yes | none | keep | wording only |",
    }
    (d / "audit.md").write_text(audit_md(rows, []), encoding="utf-8")
    res = apply_(d)
    assert res.returncode == 0, res.stdout
    log = (d / "apply-log.md").read_text()
    assert "REVERT_SHARED N1" in log.splitlines()
    assert spec_of(d).read_text() == "one N1 N2 words\nk\ntwo\n"  # H2 reverted, H1 kept
    assert (d / "closed-minor.txt").read_text() == ""


def test_every_apply_log_row_has_id_and_bytes(prepped):
    (prepped / "audit.md").write_text(audit_md(), encoding="utf-8")
    assert apply_(prepped).returncode == 0
    rows = [
        ln
        for ln in (prepped / "apply-log.md").read_text().splitlines()
        if ln.split(" ", 1)[0] in ("applied", "already", "SKIP", "STOP")
    ]
    assert len(rows) == 4  # H1 revert, N2 keep, - keep, N3 edit
    for ln in rows:
        assert re.search(r" bytes [0-9]+ -> [0-9]+$", ln), ln
        assert ln.split()[1] in ("N1", "N2", "N3", "-"), ln


# ---------- verdict ----------


def r3(prior_rows: str, new_rows: str = "", last: str = "verdict: PASS") -> str:
    text = "# Review 3\n\nreview: 3 of 3\n\n"
    if prior_rows:
        text += (
            "## Prior findings\n\n| id | fixed | status |\n|---|---|---|\n"
            + prior_rows
            + "\n"
        )
    text += (
        "## New findings\n\n| id | severity | grade |\n|---|---|---|\n"
        + new_rows
        + "\n"
        + last
        + "\n"
    )
    return text


def verdict(d: Path, text: str, rule: str = "427"):
    rep = d.parent / "round3.md"
    rep.write_text(text, encoding="utf-8")
    res = run("verdict", "--dir", str(d), "--report", str(rep), "--report-rule", rule)
    lines = (d / "final-verdict.md").read_text().splitlines()
    assert lines[-1] in ("verdict: PASS", "verdict: FAIL")
    return res, lines


@pytest.fixture
def applied(prepped):
    """CK fixture after apply: N1 (MINOR) reverted and closed, N2 kept, N3 shrunk."""
    (prepped / "audit.md").write_text(audit_md(), encoding="utf-8")
    assert apply_(prepped).returncode == 0
    return prepped


RESOLVED = "| N2 | yes | resolved |\n| N3 | yes | resolved |\n"


def test_clean_review3_passes(applied):
    res, lines = verdict(applied, r3(RESOLVED))
    assert res.returncode == 0 and lines[-1] == "verdict: PASS"
    assert "open blocking: none" in lines


def test_report_fail_never_becomes_pass(applied):
    res, lines = verdict(applied, r3(RESOLVED, last="verdict: FAIL"))
    assert lines[-1] == "verdict: FAIL"


@pytest.mark.parametrize("status", ["open", "regressed"])
def test_prior_blocking_open_or_regressed_stays_open(applied, status):
    res, lines = verdict(
        applied,
        r3(f"| N2 | no | {status} |\n| N3 | yes | resolved |\n", last="verdict: FAIL"),
    )
    assert "open blocking: N2" in lines and lines[-1] == "verdict: FAIL"


def test_listed_open_minor_id_does_not_count_and_closed_one_is_named(applied):
    res, lines = verdict(applied, r3(RESOLVED + "| N1 | no | open |\n"))
    assert res.returncode == 0 and lines[-1] == "verdict: PASS"
    assert "closed-minor, listed open: N1" in lines and "open blocking: none" in lines


def test_closed_id_graded_blocking_disagrees(applied):
    res, lines = verdict(
        applied, r3(RESOLVED, "| N1 | MAJOR | blocking |\n", last="verdict: FAIL")
    )
    assert res.returncode == 2 and lines[-1] == "verdict: FAIL"
    assert any(ln.startswith("consistency: DISAGREE") for ln in lines)


def test_unparseable_table_exits_2_fail(applied):
    res, lines = verdict(applied, "review: 3 of 3\nno tables here\nverdict: PASS\n")
    assert res.returncode == 2 and lines[-1] == "verdict: FAIL"


def test_427_disagreeing_report_line_gives_stricter_line(applied):
    res, lines = verdict(
        applied,
        r3("| N2 | no | open |\n| N3 | yes | resolved |\n", last="verdict: PASS"),
    )
    assert res.returncode == 2 and lines[-1] == "verdict: FAIL"
    assert any(ln.startswith("consistency: DISAGREE") for ln in lines)


def test_any_severity_prints_t09_line(applied):
    res, lines = verdict(
        applied,
        r3(RESOLVED, "| R3-1 | MINOR | non-blocking |\n", last="verdict: FAIL"),
        "any-severity",
    )
    assert "t09-verdict: verdict: FAIL" in lines
    # no cross-check (no DISAGREE, exit 0), but the report's FAIL is never turned into a PASS
    assert res.returncode == 0 and lines[-1] == "verdict: FAIL"
    assert not any(ln.startswith("consistency:") for ln in lines)
    res, lines = verdict(applied, r3(RESOLVED, last="verdict: PASS"), "any-severity")
    assert "t09-verdict: verdict: PASS" in lines and lines[-1] == "verdict: PASS"


def _owner(lines):
    new = int(
        next(ln for ln in lines if ln.startswith("review-3 new critical+major:")).split(
            ": "
        )[1]
    )
    own = int(
        next(
            ln for ln in lines if ln.startswith("review-3 critical+major (owner count")
        ).split(": ")[1]
    )
    return new, own


def _run_audit(tmp_path, rep_rows, rows, edits=None):
    res, d, state = prepare(
        tmp_path,
        "a one\nk\nb two\n",
        "a one N1 extra\nk\nb two N2 rule\n",
        report(rep_rows),
        disp="",
    )
    (d / "audit.md").write_text(audit_md(rows, edits or []), encoding="utf-8")
    apply_(d)
    return d


NEW_CM = "| R3-1 | MAJOR | blocking |\n"


def test_owner_count_reverted_major_adds_one(tmp_path):
    d = _run_audit(
        tmp_path,
        "| N1 | MAJOR | non-blocking |\n| N2 | MAJOR | blocking |\n",
        {
            "N1": "| N1 | H1 | minor | minor | no | none | revert | the added words change nothing at all |",
            "N2": "| N2 | H2 | blocking | blocking | yes | none | keep | without it the rule is wrong for readers |",
        },
    )
    assert (d / "closed-minor.txt").read_text() == "N1 MAJOR\n"
    res, lines = verdict(d, r3("| N2 | yes | resolved |\n", NEW_CM, "verdict: FAIL"))
    assert _owner(lines) == (1, 2)
    assert "held open (deferred or demoted): N1 MAJOR" in lines


def test_owner_count_downgrade_critical_adds_one(tmp_path):
    d = _run_audit(
        tmp_path,
        "| N1 | MINOR | non-blocking |\n| N2 | CRITICAL | blocking |\n",
        {
            "N1": "| N1 | H1 | minor | minor | yes | none | keep | wording only |",
            "N2": "| N2 | H2 | blocking | minor | no | none | keep | wording only |",
        },
    )
    assert "DOWNGRADE N2" in (d / "check.log").read_text()
    res, lines = verdict(d, r3("| N2 | yes | resolved |\n", NEW_CM, "verdict: FAIL"))
    assert _owner(lines) == (1, 2)


def test_owner_count_reverted_minor_adds_nothing(applied):
    assert (applied / "closed-minor.txt").read_text() == "N1 MINOR\n"
    res, lines = verdict(applied, r3(RESOLVED, NEW_CM, "verdict: FAIL"))
    assert _owner(lines) == (1, 1)


def test_owner_count_equal_when_audit_skipped(tmp_path):
    rep = report("| N1 | MAJOR | non-blocking |\n")
    res, d, state = prepare(tmp_path, "a\nk\nb\n", "a x\nk\nb y\n", rep, disp="")
    assert (
        state["audit"] == "skipped(ids not citable)" and not (d / "check.log").exists()
    )
    res, lines = verdict(d, r3("| N1 | no | open |\n", NEW_CM, "verdict: FAIL"))
    new, own = _owner(lines)
    assert new == own == 1


def test_downgrade_counts_even_when_the_check_failed(tmp_path):
    d = _run_audit(
        tmp_path,
        "| N1 | MINOR | non-blocking |\n| N2 | CRITICAL | blocking |\n",
        {
            "N1": "| N1 | H1 | blocking | minor | yes | none | keep | wording only |",  # wrong claimed: K4
            "N2": "| N2 | H2 | blocking | minor | no | none | keep | wording only |",
        },
    )
    state = json.loads((d / "state.json").read_text())
    assert (
        state["audit"] == "skipped(check failed)"
        and "DOWNGRADE N2" in (d / "check.log").read_text()
    )
    res, lines = verdict(d, r3("| N2 | yes | resolved |\n", NEW_CM, "verdict: FAIL"))
    assert _owner(lines) == (1, 2)
    assert "held open (deferred or demoted): N2 CRITICAL" in lines


def test_unlabelled_blocking_row_in_review3_counts_as_open(applied):
    res, lines = verdict(
        applied, r3(RESOLVED, "| R3-1 | blocking | missing anchor |\n", "verdict: PASS")
    )
    assert "open blocking: R3-1" in lines and lines[-1] == "verdict: FAIL"
    res, lines = verdict(
        applied, r3(RESOLVED, "| R3-2 | non-blocking | wording |\n", "verdict: PASS")
    )
    assert "open blocking: none" in lines and lines[-1] == "verdict: PASS"


def _major_reverted(tmp_path):
    return _run_audit(
        tmp_path,
        "| N1 | MAJOR | non-blocking |\n| N2 | MAJOR | blocking |\n",
        {
            "N1": "| N1 | H1 | minor | minor | no | none | revert | the added words change nothing at all |",
            "N2": "| N2 | H2 | blocking | blocking | yes | none | keep | without it the rule is wrong for readers |",
        },
    )


@pytest.mark.parametrize(
    "row,counts",
    [
        (
            "| N1 | MINOR | non-blocking |\n",
            (0, 1),
        ),  # relabelled minor by review 3: still held
        (
            "| N1 | MAJOR | non-blocking |\n",
            (1, 1),
        ),  # already counted by review 3: counted once
    ],
)
def test_owner_count_held_id_relisted_by_review3(tmp_path, row, counts):
    d = _major_reverted(tmp_path)
    res, lines = verdict(d, r3("| N2 | yes | resolved |\n", row, "verdict: PASS"))
    assert _owner(lines) == counts


def test_resolution_row_without_status_is_unparseable(applied):
    res, lines = verdict(
        applied,
        r3(
            "| N2 | no | partially resolved |\n| N3 | yes | resolved |\n",
            last="verdict: PASS",
        ),
    )
    assert res.returncode == 2 and lines[-1] == "verdict: FAIL"
    assert any(ln.startswith("unparseable:") and "N2" in ln for ln in lines)


def test_ungraded_review3_row_counts_as_blocking(applied):
    res, lines = verdict(
        applied, r3(RESOLVED, "| R3-1 | - | missing anchor |\n", "verdict: PASS")
    )
    assert "open blocking: R3-1" in lines and lines[-1] == "verdict: FAIL"


@pytest.mark.parametrize(
    "row", ["| R3-1 | blocking | open |\n", "| R3-1 | - | open |\n"]
)
def test_new_review3_row_with_status_word_counts_as_blocking(applied, row):
    res, lines = verdict(applied, r3(RESOLVED, row, "verdict: PASS"))
    assert "open blocking: R3-1" in lines and lines[-1] == "verdict: FAIL"


def test_review2_id_row_with_status_word_is_not_a_new_finding(applied):
    res, lines = verdict(applied, r3(RESOLVED, "| N1 | no | open |\n", "verdict: PASS"))
    assert "open blocking: none" in lines and lines[-1] == "verdict: PASS"


@pytest.mark.parametrize("rule", ["427", "any-severity"])
def test_closed_id_graded_blocking_with_status_word_disagrees(applied, rule):
    res, lines = verdict(
        applied, r3(RESOLVED, "| N1 | blocking | open |\n", "verdict: PASS"), rule
    )
    assert res.returncode == 2 and lines[-1] == "verdict: FAIL"
    assert any(ln.startswith("consistency: DISAGREE") for ln in lines)


def test_blocking_column_yes_and_no_on_closed_id(applied):
    swap = ("| id | severity | grade |", "| id | blocking | status |")
    res, lines = verdict(
        applied, r3(RESOLVED, "| N1 | yes | open |\n", "verdict: PASS").replace(*swap)
    )
    assert res.returncode == 2 and lines[-1] == "verdict: FAIL"
    assert any(ln.startswith("consistency: DISAGREE") for ln in lines)
    res, lines = verdict(
        applied, r3(RESOLVED, "| N1 | no | open |\n", "verdict: PASS").replace(*swap)
    )
    assert (
        res.returncode == 0
        and "open blocking: none" in lines
        and lines[-1] == "verdict: PASS"
    )


@pytest.mark.parametrize("rule", ["427", "any-severity"])
@pytest.mark.parametrize(
    "row", ["| N1 | blocking | open |\n", "| N1 | MINOR, B | open |\n"]
)
def test_closed_id_graded_blocking_in_resolution_table_disagrees(applied, rule, row):
    res, lines = verdict(applied, r3(RESOLVED + row, last="verdict: PASS"), rule)
    assert res.returncode == 2 and lines[-1] == "verdict: FAIL"
    assert any(ln.startswith("consistency: DISAGREE") for ln in lines)


def test_closed_id_with_bare_label_in_resolution_table_stays_a_note(applied):
    res, lines = verdict(
        applied, r3(RESOLVED + "| N1 | MINOR | open |\n", last="verdict: PASS")
    )
    assert res.returncode == 0 and lines[-1] == "verdict: PASS"
    assert "closed-minor, listed open: N1" in lines
