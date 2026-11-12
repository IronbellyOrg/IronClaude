"""Recorded reflect card converter (Task 2 of the reflect Tier 2 panel plan)."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from superclaude.cli.review import card_convert as cc
from superclaude.cli.review import findings_v2 as v2

FIX = Path(__file__).parent / "fixtures" / "reflect_cards"
PLAN = ".dev/tasks/to-do/TASK-X/TASK-X.md"
SPEC = ".dev/tasks/to-do/TASK-X/source.md"


def fixture(name: str, **kw) -> dict:
    fmt = "markdown" if name.endswith(".md") else "yaml"
    return cc.convert_card((FIX / name).read_text(encoding="utf-8"), fmt=fmt, **kw)


def card(evidence, *, severity="blocking", extra: str = "", head: str = "") -> dict:
    entry = {"id": "F1", "severity": severity, "claim": "c", "evidence": evidence}
    text = head + "findings:\n  - " + json.dumps(entry) + "\n" + extra
    return cc.convert_card(text, fmt="yaml", plan_path=PLAN, spec_path=SPEC)


def cits(result: dict) -> list[dict]:
    return [c for f in result["findings"] for c in f["citations"]]


def all_fixture_results() -> list[dict]:
    return [
        fixture(p.name, plan_path=PLAN, spec_path=SPEC) for p in sorted(FIX.iterdir())
    ]


# --- acceptance criterion 1: the three ref kinds -------------------------------------------


def test_stoprule_fixture_converts_three_refs_with_roles_and_paths():
    r = fixture("synthetic-stoprule.yaml")
    assert r["plan_path_source"] == "card" and r["spec_path_source"] == "card"
    f1 = r["findings"][0]
    assert f1["citations"] == [
        {"role": "plan", "path": PLAN, "line_start": 57, "line_end": 57},
        {"role": "spec", "path": SPEC, "line_start": 62, "line_end": 62},
        {"role": "source", "path": "src/x.py", "line_start": 451, "line_end": 462},
    ]
    assert v2.check_finding(dict(f1), set()) is None
    assert r["problems"] == []
    assert r["counts"]["share"] == 1.0


def test_no_citation_carries_a_quote():
    for r in all_fixture_results():
        assert all("quote" not in c for c in cits(r))


def test_spec_alias_and_plan_range():
    r = card("spec:9; plan:30-33")
    assert cits(r) == [
        {"role": "spec", "path": SPEC, "line_start": 9, "line_end": 9},
        {"role": "plan", "path": PLAN, "line_start": 30, "line_end": 33},
    ]


# --- acceptance criterion 2: unresolved refs are kept and counted --------------------------


@pytest.mark.parametrize(
    "ref, reason",
    [
        ("DESIGN:359-360", "no path:line ref"),
        ("plan Task 3", "no path:line ref"),
        ("/etc/x.py:3", "citation path must be repo-relative"),
        ("a/../b.py:3", "citation path must be repo-relative"),
        ("src/x.py:0", "line_start and line_end"),
        ("src/x.py:9-3", "line_start and line_end"),
    ],
)
def test_unresolvable_ref_is_kept_as_unresolved_and_counted(ref, reason):
    r = card(["plan:5", ref])
    c = cits(r)
    assert len(c) == 2 and c[0]["role"] == "plan"
    assert c[1]["role"] == "unresolved" and c[1]["ref"] == ref
    assert reason in c[1]["reason"]
    assert r["counts"] == {
        "units": 1,
        "converted": 0,
        "unconverted": 1,
        "refs": 2,
        "refs_resolved": 1,
        "refs_unresolved": 1,
        "share": 0.0,
    }
    assert r["problems"] == [{"id": "F1", "reason": "1 unresolved citation(s)"}]


def test_non_text_refs_are_unresolved_not_dropped():
    r = card(["plan:5", 7, {"a": 1}, ["x"], None])
    roles = [c["role"] for c in cits(r)]
    assert roles == ["plan", "unresolved", "unresolved", "unresolved"]
    assert r["counts"]["refs_unresolved"] == 3


def test_missing_paths_make_plan_and_spec_refs_unresolved():
    r = cc.convert_card(
        "findings:\n  - {id: F1, severity: minor, evidence: [plan:5, source.md:6, a.py:1]}\n",
        fmt="yaml",
    )
    c = cits(r)
    assert [x["reason"] for x in c[:2]] == ["no plan path", "no spec path"]
    assert c[2]["role"] == "source"
    assert r["plan_path"] is None and r["plan_path_source"] is None


# --- acceptance criterion 3: share per card and in total -----------------------------------


def test_share_is_reported_per_card_and_in_total():
    results = all_fixture_results()
    for r in results:
        c = r["counts"]
        assert c["units"] == c["converted"] + c["unconverted"]
        assert c["share"] == (c["converted"] / c["units"] if c["units"] else None)
    total = cc.summarize(results)
    assert total["cards"] == len(results) == 6
    units = sum(r["counts"]["units"] for r in results)
    converted = sum(r["counts"]["converted"] for r in results)
    assert (total["units"], total["converted"]) == (units, converted)
    assert total["unconverted"] == units - converted
    assert total["share"] == converted / units
    for shape, bucket in total["by_shape"].items():
        mine = [r for r in results if r["shape"] == shape]
        assert bucket["cards"] == len(mine)
        assert bucket["units"] == sum(r["counts"]["units"] for r in mine)


def test_empty_findings_list_has_no_share_and_summary_of_nothing_is_none():
    r = cc.convert_card("findings: []\n", fmt="yaml")
    assert r["shape"] == "yaml-blocking-minor"
    assert r["counts"]["units"] == 0 and r["counts"]["share"] is None
    assert cc.summarize([])["share"] is None
    assert cc.summarize([r])["share"] is None


# --- acceptance criterion 4: priority and markdown cards are counted -----------------------


def test_priority_card_is_counted_in_the_share():
    r = fixture("yaml-priority.yaml", plan_path=PLAN, spec_path=SPEC)
    assert r["shape"] == "yaml-other-severity"
    assert r["counts"]["units"] == 8
    assert {f["severity"] for f in r["findings"]} == {"MAJOR", "MINOR"}
    assert [f["blocking"] for f in r["findings"][:3]] == [True, True, False]
    total = cc.summarize([r])
    assert total["by_shape"]["yaml-other-severity"]["units"] == 8
    assert total["units"] == 8


def test_markdown_table_card_is_counted_in_the_share():
    r = fixture("markdown-table.md", plan_path=PLAN, spec_path=SPEC)
    assert r["shape"] == "markdown-table"
    assert r["counts"]["units"] == 7
    first = r["findings"][0]
    assert first["id"] == "1" and first["deviation_class"] == "necessary"
    assert first["severity"] == "MINOR"
    assert first["citations"][0] == {
        "role": "spec",
        "path": SPEC,
        "line_start": 79,
        "line_end": 79,
    }
    # location column: "plan:52, :552, :556-566"
    assert first["citations"][1:4] == [
        {"role": "plan", "path": PLAN, "line_start": 52, "line_end": 52},
        {"role": "plan", "path": PLAN, "line_start": 552, "line_end": 552},
        {"role": "plan", "path": PLAN, "line_start": 556, "line_end": 566},
    ]
    assert cc.summarize([r])["by_shape"]["markdown-table"]["units"] == 7


def test_markdown_card_in_unlisted_shape_lowers_the_share():
    listed = fixture("synthetic-stoprule.yaml")
    unlisted = fixture("markdown-lines.md")
    assert unlisted["shape"] == "unlisted"
    assert unlisted["counts"]["units"] == 1 and unlisted["counts"]["converted"] == 0
    total = cc.summarize([listed, unlisted])
    assert total["units"] == listed["counts"]["units"] + 1
    assert total["share"] < 1.0
    assert total["by_shape"]["unlisted"] == {
        "cards": 1,
        "units": 1,
        "converted": 0,
        "share": 0.0,
    }


# --- card-format table: shapes -------------------------------------------------------------


@pytest.mark.parametrize(
    "name, shape",
    [
        ("synthetic-stoprule.yaml", "yaml-blocking-minor"),
        ("yaml-blocking-minor.yaml", "yaml-blocking-minor"),
        ("yaml-priority.yaml", "yaml-other-severity"),
        ("yaml-deviation-class.yaml", "yaml-other-severity"),
        ("markdown-table.md", "markdown-table"),
        ("markdown-lines.md", "unlisted"),
    ],
)
def test_one_fixture_per_shape(name, shape):
    assert fixture(name)["shape"] == shape


def test_entry_without_severity_makes_the_card_other_severity():
    r = cc.convert_card("findings:\n  - {id: F1, evidence: a.py:1}\n", fmt="yaml")
    assert r["shape"] == "yaml-other-severity"
    assert r["problems"] == [
        {"id": "F1", "reason": "severity must be CRITICAL, MAJOR or MINOR"}
    ]


def test_deviation_class_card_reads_class_and_severity_words():
    r = fixture("yaml-deviation-class.yaml")
    assert [f["severity"] for f in r["findings"]] == ["MINOR"] * 4
    # plan-gap is not a findings-v2 deviation class, so none is set
    assert all("deviation_class" not in f for f in r["findings"])
    r = card("a.py:1", severity="medium")
    assert r["shape"] == "yaml-other-severity"


def test_first_finding_list_wins():
    text = (
        "findings: null\n"
        "returned_findings:\n  - {id: A1, severity: minor, evidence: a.py:1}\n"
        "deviations:\n  - {id: B1, severity: minor, evidence: a.py:2}\n"
    )
    assert [f["id"] for f in cc.convert_card(text, fmt="yaml")["findings"]] == ["A1"]


def test_markdown_category_column_sets_reflect_category():
    text = "| id | Category | Evidence | Severity |\n|---|---|---|---|\n| C1 | coverage | a.py:3 | HIGH |\n"
    r = cc.convert_card(text, fmt="markdown")
    f = r["findings"][0]
    assert (f["reflect_category"], f["category"]) == ("coverage", "missing-requirement")
    assert (f["severity"], f["blocking"]) == ("MAJOR", True)
    assert r["problems"] == []


@pytest.mark.parametrize("key", ["returned_findings", "deviations"])
def test_other_finding_containers(key):
    text = f"{key}:\n  - {{n: 1, severity: LOW, class: Drift, finding: x, location: 'plan:116 (Task 6)'}}\n"
    r = cc.convert_card(text, fmt="yaml", plan_path=PLAN)
    f = r["findings"][0]
    assert f["id"] == "1" and f["deviation_class"] == "drift"
    assert f["citations"] == [
        {"role": "plan", "path": PLAN, "line_start": 116, "line_end": 116}
    ]
    assert r["counts"]["converted"] == 1


@pytest.mark.parametrize("key", cc.REF_KEYS)
def test_every_ref_key_is_read(key):
    text = f"findings:\n  - {{id: F1, severity: minor, {key}: 'a.py:3'}}\n"
    r = cc.convert_card(text, fmt="yaml")
    assert cits(r) == [
        {"role": "source", "path": "a.py", "line_start": 3, "line_end": 3}
    ]


def test_unknown_ref_key_is_not_read():
    r = cc.convert_card(
        "findings:\n  - {id: F1, severity: minor, plan_ref: 'a.py:3'}\n", fmt="yaml"
    )
    assert cits(r) == []
    assert r["problems"][0]["reason"] == "citations must be a list of 1 to 8 citations"


# --- splitting ------------------------------------------------------------------------------


def test_comma_and_semicolon_splitting_with_continuations():
    r = card("plan:33,60; tests/x.py:519-527,559-568; source.md:70, :72")
    assert [
        (c["role"], c["path"], c["line_start"], c["line_end"]) for c in cits(r)
    ] == [
        ("plan", PLAN, 33, 33),
        ("plan", PLAN, 60, 60),
        ("source", "tests/x.py", 519, 527),
        ("source", "tests/x.py", 559, 568),
        ("spec", SPEC, 70, 70),
        ("spec", SPEC, 72, 72),
    ]


def loc(r: dict) -> list[tuple]:
    return [
        (c["role"], c.get("path"), c.get("line_start"), c.get("line_end"))
        for c in cits(r)
    ]


def test_line_breaks_and_continuation_does_not_cross_a_semicolon():
    r = card("a.py:1\nb.py:2; 3")
    assert loc(r) == [("source", "a.py", 1, 1), ("source", "b.py", 2, 2)]


def test_continuation_needs_a_token_before_it():
    c = cits(card("plan Task 3, 60"))
    assert c == [
        {"role": "unresolved", "ref": "plan Task 3, 60", "reason": "no path:line ref"}
    ]


def test_continuation_followed_by_prose_is_prose():
    assert loc(card("a.py:12, 3 tests fail")) == [("source", "a.py", 12, 12)]


def test_tokens_inside_quotes_backticks_brackets_and_before_a_dot():
    r = card(["`a.py:4`", "'plan:7 (Task 2)'", "**b.py:5**.", "[c.py:6]"])
    assert [(c["path"], c["line_start"]) for c in cits(r)] == [
        ("a.py", 4),
        (PLAN, 7),
        ("b.py", 5),
        ("c.py", 6),
    ]


def test_prose_before_and_after_a_ref_is_ignored():
    assert loc(card("docs/x.md:163 some quoted text")) == [
        ("source", "docs/x.md", 163, 163)
    ]
    assert loc(card("see plan:57 for the step")) == [("plan", PLAN, 57, 57)]
    assert loc(card("POST-REFLECT-TASK.md:576: Status set to Blocked")) == [
        ("source", "POST-REFLECT-TASK.md", 576, 576)
    ]


def test_two_refs_in_one_string():
    r = card("plan line 59 differs: src/a/audit.py:26-102 and source.md:62 disagree")
    assert loc(r) == [("source", "src/a/audit.py", 26, 102), ("spec", SPEC, 62, 62)]
    assert r["counts"]["converted"] == 1


def test_string_without_a_ref_is_one_unresolved_citation_holding_it():
    text = "Task 4  body and\n the decisive-case criterion"
    c = cits(card(["plan:1", text, "   "]))
    assert c[1:] == [
        {
            "role": "unresolved",
            "ref": "Task 4 body and the decisive-case criterion",
            "reason": "no path:line ref",
        }
    ]


@pytest.mark.parametrize(
    "text",
    [
        "Note: src/x.py: see the reason table",
        "https://example.com:8080/a.py",
        "verified at 12:48Z",
        "src/x.py:12abc",
        "src/x.py:12/3",
        "a.py:1.5",
        "PLAN:36; tasklist:20; DESIGN:359-360",
        "Task:3",
        "x:a.py:3",
    ],
)
def test_colon_in_prose_that_is_not_path_digits_is_not_a_citation(text):
    c = cits(card(text))
    assert c == [{"role": "unresolved", "ref": text, "reason": "no path:line ref"}]


# --- severity, category, risk and claim -------------------------------------------------------


@pytest.mark.parametrize(
    "word, severity, blocking",
    [
        ("blocking", "MAJOR", True),
        ("BLOCKER", "MAJOR", True),
        ("major", "MAJOR", True),
        ("HIGH", "MAJOR", True),
        ("must-fix", "MAJOR", True),
        ("P1", "MAJOR", True),
        ("critical", "CRITICAL", True),
        ("p0", "CRITICAL", True),
        ("minor", "MINOR", False),
        ("MEDIUM", "MINOR", False),
        ("low", "MINOR", False),
        ("should-fix", "MINOR", False),
        ("important", "MINOR", False),
        ("nit", "MINOR", False),
        ("info", "MINOR", False),
        ("P2", "MINOR", False),
        ("p3", "MINOR", False),
    ],
)
def test_severity_table(word, severity, blocking):
    f = card("a.py:1", severity=word)["findings"][0]
    assert (f["severity"], f["blocking"]) == (severity, blocking)


def test_unknown_severity_word_leaves_the_finding_unconverted():
    r = card("a.py:1", severity="P")
    assert r["findings"][0]["severity"] is None
    assert r["counts"]["converted"] == 0


def test_priority_is_used_only_without_severity():
    text = "findings:\n  - {id: F1, severity: minor, priority: P1, evidence: a.py:1}\n"
    f = cc.convert_card(text, fmt="yaml")["findings"][0]
    assert f["severity"] == "MINOR"


@pytest.mark.parametrize(
    "label, category",
    [
        ("ordering", "other"),
        ("acceptance", "unpassable-check"),
        ("coverage", "missing-requirement"),
        ("Contradiction", "contradiction"),
    ],
)
def test_category_mapping(label, category):
    text = f"findings:\n  - {{id: F1, severity: blocking, kind: {label}, claim: c, evidence: a.py:1}}\n"
    r = cc.convert_card(text, fmt="yaml")
    f = r["findings"][0]
    assert f["category"] == category and f["reflect_category"] == label.lower()
    assert r["problems"] == []


def test_deviation_maps_to_other_with_class_and_needs_a_class():
    ok = "findings:\n  - {id: F1, severity: minor, type: deviation, deviation_class: drift, evidence: a.py:1}\n"
    f = cc.convert_card(ok, fmt="yaml")["findings"][0]
    assert (f["category"], f["deviation_class"]) == ("other", "drift")
    bad = (
        "findings:\n  - {id: F1, severity: minor, type: deviation, evidence: a.py:1}\n"
    )
    r = cc.convert_card(bad, fmt="yaml")
    assert r["problems"] == [
        {"id": "F1", "reason": "reflect_category deviation needs deviation_class"}
    ]


def test_unmapped_label_gives_other_without_reflect_category():
    text = "findings:\n  - {id: F1, severity: minor, kind: false-coverage, evidence: a.py:1}\n"
    f = cc.convert_card(text, fmt="yaml")["findings"][0]
    assert f["category"] == "other" and "reflect_category" not in f


@pytest.mark.parametrize(
    "claim, category",
    [
        ("A security token is printed to the log.", "safety"),
        ("This is unsafe for concurrent runs.", "safety"),
        ("The step can lose data on retry.", "safety"),
        ("A data-loss path exists.", "safety"),
        ("Credentials leak into the report.", "safety"),
        ("The safety check is skipped.", "safety"),
        ("Task 4 may run slowly on large inputs.", "other"),
    ],
)
def test_risk_rule(claim, category):
    text = "findings:\n  - " + json.dumps(
        {
            "id": "F1",
            "severity": "minor",
            "category": "risk",
            "claim": claim,
            "evidence": "a.py:1",
        }
    )
    r = cc.convert_card(text, fmt="yaml")
    assert r["findings"][0]["category"] == category
    assert r["problems"] == []


def test_risk_fixture_uses_safety():
    f = fixture("synthetic-stoprule.yaml")["findings"][1]
    assert (f["reflect_category"], f["category"]) == ("risk", "safety")


def test_long_claim_is_flattened_and_cut_to_300():
    text = "findings:\n  - " + json.dumps(
        {
            "id": "F1",
            "severity": "minor",
            "claim": "word \n " * 200,
            "evidence": "a.py:1",
        }
    )
    f = cc.convert_card(text, fmt="yaml")["findings"][0]
    assert len(f["claim"]) == 300 and "\n" not in f["claim"]
    assert f["claim"].endswith("...")


def test_more_than_eight_citations_is_unconverted_but_all_are_kept():
    r = card("; ".join(f"a.py:{n}" for n in range(1, 11)))
    assert len(cits(r)) == 10 and r["counts"]["refs_resolved"] == 10
    assert r["problems"][0]["reason"] == "citations must be a list of 1 to 8 citations"


def test_ids_keep_valid_card_ids_and_replace_bad_or_duplicate_ones():
    text = (
        "findings:\n"
        "  - {id: R2-F1, severity: minor, evidence: a.py:1}\n"
        "  - {id: R2-F1, severity: minor, evidence: a.py:2}\n"
        "  - {id: 'bad id!', severity: minor, evidence: a.py:3}\n"
        "  - {id: true, severity: minor, evidence: a.py:4}\n"
        "  - {id: F2, severity: minor, evidence: a.py:5}\n"
    )
    ids = [f["id"] for f in cc.convert_card(text, fmt="yaml")["findings"]]
    # the card's F2 is taken by entry 2's replacement id, so entry 5 gets F5
    assert ids == ["R2-F1", "F2", "F3", "F4", "F5"]
    text = "findings:\n  - {id: F2, severity: minor, evidence: a.py:1}\n  - {id: '!', severity: minor, evidence: a.py:2}\n"
    assert [f["id"] for f in cc.convert_card(text, fmt="yaml")["findings"]] == [
        "F2",
        "F2-1",
    ]


def test_converted_real_findings_pass_the_v2_checker():
    for r in all_fixture_results():
        bad = {p["id"] for p in r["problems"]}
        seen: set[str] = set()
        for f in r["findings"]:
            if f["id"] not in bad:
                assert v2.check_finding(dict(f), seen) is None
                seen.add(f["id"])


# --- plan and spec path sources ----------------------------------------------------------------


def _run(tmp_path: Path, card_text: str, snapshot: str | None, name="r-1-card.yaml"):
    cards = tmp_path / "run" / "reviewer-cards"
    cards.mkdir(parents=True)
    (cards / name).write_text(card_text, encoding="utf-8")
    if snapshot is not None:
        (tmp_path / "run" / "artifacts").mkdir()
        (tmp_path / "run" / "artifacts" / "input-snapshot.yaml").write_text(
            snapshot, encoding="utf-8"
        )
    return cc.convert_card_file(cards / name)


CARD = "findings:\n  - {id: F1, severity: minor, evidence: [plan:5, source.md:6]}\n"
SNAP_JSON = json.dumps(
    {
        "file_list": [
            {"path": ".dev/tasks/to-do/T-1/T-1.md", "sha256": "x"},
            {"path": ".dev/tasks/to-do/T-1/source.md", "sha256": "y"},
            {"path": "README.md", "sha256": "z"},
        ]
    }
)


def test_snapshot_paths_used_when_card_has_no_fields(tmp_path):
    r = _run(tmp_path, CARD, SNAP_JSON)
    assert (r["plan_path"], r["plan_path_source"]) == (
        ".dev/tasks/to-do/T-1/T-1.md",
        "snapshot",
    )
    assert (r["spec_path"], r["spec_path_source"]) == (
        ".dev/tasks/to-do/T-1/source.md",
        "snapshot",
    )
    assert r["counts"]["converted"] == 1


def test_card_fields_win_over_snapshot_per_path(tmp_path):
    r = _run(tmp_path, "plan: p/p.md\n" + CARD, SNAP_JSON)
    assert (r["plan_path"], r["plan_path_source"]) == ("p/p.md", "card")
    assert r["spec_path_source"] == "snapshot"
    assert cits(r)[0]["path"] == "p/p.md"


def test_no_snapshot_and_no_fields_leaves_refs_unresolved(tmp_path):
    r = _run(tmp_path, CARD, None)
    assert [c["reason"] for c in cits(r)] == ["no plan path", "no spec path"]
    assert r["counts"]["share"] == 0.0


def test_snapshot_yaml_forms_and_root_plan(tmp_path):
    nested = (
        "input_snapshot:\n  files:\n"
        "    - {path: a/T-2/T-2.md, sha256: x}\n    - {path: a/T-2/source.md, sha256: y}\n"
    )
    p = tmp_path / "s1.yaml"
    p.write_text(nested, encoding="utf-8")
    assert cc.snapshot_paths(p) == ("a/T-2/T-2.md", "a/T-2/source.md")
    root = "file_list:\n  - path: TASK-WF-x-1.md\n  - path: source.md\n  - path: NOTES.md\n"
    p.write_text(root, encoding="utf-8")
    assert cc.snapshot_paths(p) == ("TASK-WF-x-1.md", "source.md")


def test_snapshot_with_two_plans_or_specs_gives_none(tmp_path):
    p = tmp_path / "s.yaml"
    p.write_text(
        "file_list:\n  - path: a/A/A.md\n  - path: b/B/B.md\n"
        "  - path: a/source.md\n  - path: b/source.md\n",
        encoding="utf-8",
    )
    assert cc.snapshot_paths(p) == (None, None)


@pytest.mark.parametrize(
    "content",
    [
        None,
        "",
        "[1, 2]",
        "file_list: 3",
        "file_list: [1, {path: 2}]",
        ": : :\n\t-",
        "\x00\xff",
    ],
)
def test_snapshot_paths_never_raise(tmp_path, content):
    p = tmp_path / "s.yaml"
    if content is not None:
        p.write_text(content, encoding="utf-8")
    assert cc.snapshot_paths(p) == (None, None)


# --- robustness: unlisted shapes are counted, never raised ------------------------------------


@pytest.mark.parametrize(
    "text, fmt",
    [
        ("", "yaml"),
        ("   \n", "yaml"),
        ("not: [yaml", "yaml"),
        ("- a\n- list\n", "yaml"),
        ("42", "yaml"),
        ("findings: null\n", "yaml"),
        ("findings: {a: 1}\n", "yaml"),
        ("[" * 5000 + "]" * 5000, "yaml"),
        ("\x00\x01\xff", "yaml"),
        ("# Heading\n\nprose only\n", "markdown"),
        ("| a | evidence |\n|---|---|\n| 1 | a.py:1 |\n", "markdown"),
        ("findings: []\n", None),
        ("findings: []\n", "toml"),
        (None, "yaml"),
    ],
)
def test_unlisted_inputs_count_as_one_unconverted_unit(text, fmt):
    r = cc.convert_card(text, fmt=fmt)
    assert r["shape"] == "unlisted"
    assert r["counts"]["units"] == 1 and r["counts"]["converted"] == 0
    assert r["counts"]["share"] == 0.0
    assert r["problems"][0]["id"] is None


def test_non_mapping_entries_count_as_unconverted_findings():
    r = cc.convert_card(
        "findings:\n  - 1\n  - null\n  - x\n  - {id: F1, severity: minor, evidence: a.py:1}\n",
        fmt="yaml",
    )
    assert r["counts"]["units"] == 4 and r["counts"]["converted"] == 1
    assert [p["reason"] for p in r["problems"]] == [
        "entry 1 is not a mapping",
        "entry 2 is not a mapping",
        "entry 3 is not a mapping",
    ]


def test_wrong_typed_fields_do_not_raise():
    text = (
        "plan: [1]\nspec: 3\nfindings:\n"
        "  - {id: [1], severity: 3, category: [risk], claim: {a: 1}, evidence: {plan: 5}}\n"
        "  - {}\n"
    )
    r = cc.convert_card(text, fmt="yaml")
    assert r["plan_path_source"] is None and r["counts"]["units"] == 2
    assert r["counts"]["converted"] == 0


def test_huge_card_does_not_raise():
    text = "findings:\n" + "".join(
        f"  - {{id: F{n}, severity: minor, evidence: 'a.py:{n}'}}\n"
        for n in range(1, 3001)
    )
    r = cc.convert_card(text, fmt="yaml")
    assert r["counts"]["units"] == 3000 and r["counts"]["converted"] == 3000
    long_ref = "x" * 100_000
    c = cits(card(long_ref))
    assert len(c[0]["ref"]) == cc.MAX_REF_TEXT


def test_markdown_table_short_rows_and_second_table(tmp_path):
    text = (
        "| # | Class | Evidence | Sev |\n|---|---|---|---|\n| 1 | Drift |\n\n"
        "| id | evidence | severity |\n| :-- | :-- | --: |\n| Q-1 | a.py:2 | low |\n"
    )
    r = cc.convert_card(text, fmt="markdown")
    assert r["counts"]["units"] == 2 and r["counts"]["converted"] == 1
    assert r["findings"][1]["id"] == "Q-1"


def test_card_file_suffixes_and_missing_file(tmp_path):
    assert cc.convert_card_file(tmp_path / "nope.yaml")["shape"] == "unlisted"
    other = tmp_path / "card.txt"
    other.write_text("findings: []\n", encoding="utf-8")
    assert cc.convert_card_file(other)["shape"] == "unlisted"
    yml = tmp_path / "card.YML"
    yml.write_text("findings: []\n", encoding="utf-8")
    assert cc.convert_card_file(yml)["shape"] == "yaml-blocking-minor"
    md = tmp_path / "card.md"
    md.write_text("| evidence | sev |\n|---|---|\n| a.py:1 | low |\n", encoding="utf-8")
    assert cc.convert_card_file(md)["shape"] == "markdown-table"
    bad = tmp_path / "bin.yaml"
    bad.write_bytes(b"\xff\xfe\x00findings")
    assert cc.convert_card_file(bad)["shape"] == "unlisted"
