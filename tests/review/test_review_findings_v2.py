"""findings-v2 line checker and block parser (Task 1 of the reflect Tier 2 panel plan)."""

from __future__ import annotations

import copy
import json

import pytest
from test_review_findings import line, report

from superclaude.cli.review import findings as fnd
from superclaude.cli.review import findings_v2 as v2

CIT = {"role": "plan", "path": "docs/plan.md", "line_start": 3, "line_end": 5}

# Copied from tests/review/test_review_rules_text.py:68 with the placeholders filled.
RULE_EXAMPLE = {
    "id": "F1",
    "severity": "CRITICAL",
    "blocking": True,
    "category": "contradiction",
    "anchor": "A failed attempt is retried at most 5 times",
    "anchor2": "Retry the delivery up to 8 times",
    "refs": ["AC-0.4"],
    "claim": "Section 2 and section 3 give different retry limits.",
}

# The anchor, anchor2, claim and refs of test_review_findings.py:202-207 (test_refs_norm).
REFS_TEXT = {
    "anchor": "see ac-0.4 and AC-1.2.",
    "anchor2": "P1 and SHA-256 and WC-4",
    "claim": "FR-2 conflicts",
    "refs": ["5.1", "fr-9", "AC-0.4"],
}

V1_LINES = [
    line(),
    line(id="F2", severity="MINOR", blocking=False),
    line(anchor2="  another   quote here  "),
    line(**REFS_TEXT),
    line(id="F3"),
    line(id="A1"),
    line(refs=["FR-9"]),
    line(refs=[]),
    line(claim="first wording"),
    line(anchor="alpha beta gamma delta", refs=[]),
    line(anchor="text that is not in the document"),
    json.dumps(RULE_EXAMPLE),
]


def v2report(*lines):
    return report(*lines, info="findings-v2")


def base(**kw):
    obj = json.loads(line())
    obj.update(kw)
    return obj


def err(obj, **kw):
    return v2.check_finding(obj, set(), **kw)


# --- (a) v1 compatibility ---------------------------------------------------


@pytest.mark.parametrize("raw", V1_LINES)
def test_v1_line_passes_v2_unchanged(raw):
    obj = json.loads(raw)
    assert set(obj) <= set(v2.V1_FIELDS)
    v1res = fnd.parse_block(report(raw))
    assert v1res["ok"] is True
    snapshot = copy.deepcopy(obj)
    assert v2.check_finding(obj, set()) is None
    assert obj == snapshot
    v2res = v2.parse_block(v2report(raw))
    assert v2res["ok"] is True and v2res["state"] == "complete"
    assert v2res["findings"] == [dict(snapshot, refs=snapshot.get("refs", []))]
    assert v2res["findings"] == v1res["findings"]


def test_v2_uses_its_own_info_string():
    r = v2.parse_block(report(line()))  # a findings-v1 fence
    assert r["state"] == "invalid" and r["findings"] == []
    assert "findings-v2" in r["errors"][0]["msg"]
    missing = v2.parse_block("no heading\n")
    assert missing["state"] == "invalid" and "heading" in missing["errors"][0]["msg"]


# --- (b) the stated limit ---------------------------------------------------


def test_calibrated_confidence_passes_v1_and_fails_v2():
    raw = line(calibrated_confidence=0.7)
    assert fnd.parse_block(report(raw))["ok"] is True
    assert "calibrated_confidence" in err(json.loads(raw))
    r = v2.parse_block(v2report(raw))
    assert r["state"] == "invalid" and r["findings"] == []


# --- (c) prior lines --------------------------------------------------------


def test_prior_lines_are_rejected():
    prior = json.dumps({"prior": "L3", "status": "resolved"})
    assert fnd.parse_block(report(line(), prior))["ok"] is True
    r = v2.parse_block(v2report(line(), prior))
    assert r["ok"] is False and r["state"] == "invalid"
    assert [f["id"] for f in r["findings"]] == ["F1"]
    assert "prior" in r["errors"][0]["msg"]
    assert "priors" not in r


# --- (d) listed rules -------------------------------------------------------


def test_finding_needs_anchor_or_citations():
    obj = base()
    del obj["anchor"]
    assert "anchor or citations" in err(obj)
    assert "anchor or citations" in err(dict(obj, anchor=None, citations=None))
    assert err(dict(obj, citations=[CIT])) is None


def test_minor_cannot_block():
    assert "MINOR" in err(base(severity="MINOR", blocking=True))


@pytest.mark.parametrize(
    ("severity", "blocking", "ok"),
    [
        ("CRITICAL", True, True),
        ("MAJOR", True, True),
        ("MINOR", False, True),
        ("CRITICAL", False, False),
        ("MAJOR", False, False),
    ],
)
def test_reflect_severity_mapping(severity, blocking, ok):
    obj = base(severity=severity, blocking=blocking)
    res = err(dict(obj, reflect_category="risk", category="safety"))
    assert (res is None) is ok
    if not ok:
        assert "must be blocking" in res
    assert err(obj) is None  # no reflect_category: v1 rules only


def test_duplicate_id_rejected():
    assert "duplicate" in v2.check_finding(base(), {"F1"})
    r = v2.parse_block(v2report(line(), line()))
    assert r["state"] == "invalid" and len(r["findings"]) == 1


def test_calibrated_confidence_rejected_even_when_null():
    assert "calibrated_confidence" in err(base(calibrated_confidence=None))


def test_deviation_class_required_for_reflect_post():
    assert "deviation_class" in err(base(lens="reflect-post"))
    assert "deviation_class" in err(base(), lens="reflect-post")
    assert err(base(lens="reflect-post", deviation_class="drift")) is None
    assert err(base(deviation_class="drift"), lens="reflect-post") is None
    assert err(base(lens="reflect-pre")) is None
    r = v2.parse_block(v2report(line()), lens="reflect-post")
    assert r["state"] == "invalid" and "deviation_class" in r["errors"][0]["msg"]


def test_line_lens_must_equal_argument_lens():
    assert "differs" in err(base(lens="reflect-pre"), lens="reflect-post")
    assert err(base(lens="reflect-pre"), lens="reflect-pre") is None


def test_empty_block_completion():
    empty = v2report()
    assert v2.parse_block(empty)["state"] == "invalid"
    assert v2.parse_block(empty, observed_rows=["R1"])["state"] == "invalid"
    assert (
        v2.parse_block(empty, assigned_rows=[], observed_rows=["R1"])["state"]
        == "invalid"
    )
    partial = v2.parse_block(empty, assigned_rows=["R1", "R2"], observed_rows=["R1"])
    assert partial["state"] == "invalid" and partial["ok"] is False
    assert "coverage observation" in partial["errors"][0]["msg"]
    full = v2.parse_block(
        empty, assigned_rows=["R1", "R2"], observed_rows=["R2", "R1", "R3"]
    )
    assert full == {"ok": True, "state": "complete", "findings": [], "errors": []}


@pytest.mark.parametrize(
    ("quote", "ok"),
    [
        ("absent", True),
        (None, True),
        ("x" * 11, False),
        ("x" * 12, True),
        ("x" * 200, True),
        ("x" * 201, False),
    ],
)
def test_citation_quote_optional_and_12_to_200(quote, ok):
    cit = dict(CIT) if quote == "absent" else dict(CIT, quote=quote)
    res = err(base(citations=[cit]))
    assert (res is None) is ok
    if not ok:
        assert "citation quote" in res


# --- (e) one passing and one failing case per table row ---------------------

ROWS = [
    # (row, passing overrides, failing overrides, check_finding kwargs)
    ("id", {"id": "F.1-a"}, {"id": "bad id"}, {}),
    ("severity", {"severity": "MAJOR"}, {"severity": "HIGH"}, {}),
    ("blocking", {"blocking": False}, {"blocking": "yes"}, {}),
    ("category", {"category": "other"}, {"category": "weird"}, {}),
    (
        "reflect_category",
        {"reflect_category": "risk", "category": "safety"},
        {"reflect_category": "risk", "category": "contradiction"},
        {},
    ),
    (
        "reflect_category enum",
        {"reflect_category": "risk", "category": "other"},
        {"reflect_category": "style"},
        {},
    ),
    (
        "reflect_category deviation",
        {
            "reflect_category": "deviation",
            "category": "other",
            "deviation_class": "none",
        },
        {"reflect_category": "deviation", "category": "other"},
        {},
    ),
    ("claim", {"claim": "x" * 300}, {"claim": "x" * 301}, {}),
    ("refs", {"refs": ["a"] * 8}, {"refs": ["a"] * 9}, {}),
    ("anchor", {"anchor": "x" * 12}, {"anchor": "x" * 11}, {}),
    (
        "anchor with citations",
        {"anchor": None, "citations": [CIT]},
        {"anchor": "short", "citations": [CIT]},
        {},
    ),
    ("anchor2", {"anchor2": "y" * 12}, {"anchor2": "short"}, {}),
    ("citations count", {"citations": [CIT] * 8}, {"citations": [CIT] * 9}, {}),
    ("citations empty", {"citations": [CIT]}, {"citations": []}, {}),
    ("citations type", {"citations": [CIT]}, {"citations": CIT}, {}),
    (
        "citation role",
        {"citations": [dict(CIT, role="artifact")]},
        {"citations": [dict(CIT, role="code")]},
        {},
    ),
    (
        "citation lines",
        {"citations": [dict(CIT, line_start=4, line_end=4)]},
        {"citations": [dict(CIT, line_start=5, line_end=4)]},
        {},
    ),
    (
        "citation line_start",
        {"citations": [dict(CIT, line_start=1)]},
        {"citations": [dict(CIT, line_start=0)]},
        {},
    ),
    (
        "citation line bool",
        {"citations": [dict(CIT, line_start=1, line_end=1)]},
        {"citations": [dict(CIT, line_start=True, line_end=1)]},
        {},
    ),
    (
        "deviation_class",
        {"deviation_class": "regression"},
        {"deviation_class": "minor"},
        {},
    ),
    (
        "coverage_rows",
        {"coverage_rows": ["R1"]},
        {"coverage_rows": ["R9"]},
        {"assigned_rows": {"R1", "R2"}},
    ),
    ("coverage_rows no slice", {"coverage_rows": []}, {"coverage_rows": ["R1"]}, {}),
    (
        "coverage_rows type",
        {"coverage_rows": ["R1"]},
        {"coverage_rows": "R1"},
        {"assigned_rows": ["R1"]},
    ),
    ("self_confidence", {"self_confidence": 1}, {"self_confidence": 1.5}, {}),
    ("self_confidence low", {"self_confidence": 0.0}, {"self_confidence": -0.1}, {}),
    (
        "self_confidence nan",
        {"self_confidence": 0.5},
        {"self_confidence": float("nan")},
        {},
    ),
    (
        "self_confidence inf",
        {"self_confidence": 0.5},
        {"self_confidence": float("inf")},
        {},
    ),
    ("self_confidence bool", {"self_confidence": 0.5}, {"self_confidence": True}, {}),
    ("lens", {"lens": "spec"}, {"lens": "post"}, {}),
    ("channel", {"channel": "advisory"}, {"channel": "noise"}, {}),
]


@pytest.mark.parametrize(("row", "good", "bad", "kw"), ROWS, ids=[r[0] for r in ROWS])
def test_table_row(row, good, bad, kw):
    assert err(base(**good), **kw) is None
    assert isinstance(err(base(**bad), **kw), str)


def test_lens_argument_must_be_a_lens():
    assert err(base(), lens="spec") is None
    assert "lens must be" in err(base(), lens="post")


def test_coverage_rows_outside_slice_and_without_slice():
    assert "not in the assigned" in err(
        base(coverage_rows=["R9"]), assigned_rows=["R1"]
    )
    assert "no Coverage slice" in err(base(coverage_rows=["R1"]))
    r = v2.parse_block(v2report(line(coverage_rows=["R1"])), assigned_rows=["R1"])
    assert r["state"] == "complete"
    r = v2.parse_block(v2report(line(coverage_rows=["R1"])))
    assert r["state"] == "invalid"


@pytest.mark.parametrize(
    "path",
    ["/a", "C:/a", "\\\\srv\\a", "\\a", "a/../../b", "..", "C:a", "a\\..\\b", "", 5],
)
def test_citation_path_must_be_repo_relative(path):
    res = err(base(citations=[dict(CIT, path=path)]))
    assert isinstance(res, str) and "citation path" in res


@pytest.mark.parametrize("path", ["a", "src/x.py", "docs/a..b.md", ".dev/x/y.md"])
def test_citation_path_relative_passes(path):
    assert err(base(citations=[dict(CIT, path=path)])) is None


@pytest.mark.parametrize(
    "field",
    [
        "reflect_category",
        "citations",
        "deviation_class",
        "coverage_rows",
        "self_confidence",
        "lens",
        "channel",
        "anchor2",
    ],
)
def test_optional_field_null_is_absent(field):
    assert err(base(**{field: None})) is None


# --- (f) crash test ---------------------------------------------------------

V2_FIELDS = (
    "reflect_category",
    "citations",
    "deviation_class",
    "coverage_rows",
    "self_confidence",
    "lens",
    "channel",
)
CITATION_KEYS = ("role", "path", "line_start", "line_end", "quote")
VALUES = [None, True, 0, 1.5, float("nan"), "x", [], [1], {}, {"a": 1}]
CONTEXTS = [{}, {"lens": "reflect-post"}, {"assigned_rows": {"R1"}}]


def _variants():
    for field in v2.V1_FIELDS + V2_FIELDS:
        for value in VALUES:
            yield base(**{field: value})
    for key in CITATION_KEYS:
        for value in VALUES:
            yield base(citations=[dict(CIT, **{key: value})])


def test_check_finding_never_raises():
    for obj in _variants():
        for kw in CONTEXTS:
            snapshot = copy.deepcopy(obj)
            res = v2.check_finding(obj, set(), **kw)
            assert res is None or isinstance(res, str)
            assert json.dumps(obj) == json.dumps(snapshot)


# --- (g) channel_of and the completion states -------------------------------


def test_channel_of_defaults_to_defect():
    assert v2.channel_of({}) == "defect"
    assert v2.channel_of({"channel": None}) == "defect"
    assert v2.channel_of({"channel": "noise"}) == "defect"
    assert v2.channel_of({"channel": []}) == "defect"
    assert v2.channel_of({"channel": "advisory"}) == "advisory"
    r = v2.parse_block(v2report(line()))
    assert "channel" not in r["findings"][0]


def test_parse_block_returns_only_three_states():
    assert v2.COMPLETION_STATES == (
        "complete",
        "truncated",
        "invalid",
        "failed",
        "timed_out",
    )
    unclosed = "## Findings block\n\n```findings-v2\n" + line() + "\n{bad\n"
    texts = [v2report(line()), v2report(), unclosed, "nothing", v2report("{bad")]
    states = {v2.parse_block(t)["state"] for t in texts}
    assert states == {"complete", "truncated", "invalid"}


def test_truncated_beats_invalid_and_result_keys():
    unclosed = "## Findings block\n\n```findings-v2\n" + line() + "\n{bad\n"
    r = v2.parse_block(unclosed)
    assert set(r) == {"ok", "state", "findings", "errors"}
    assert r["state"] == "truncated" and r["ok"] is False
    assert len(r["errors"]) == 2 and len(r["findings"]) == 1
    empty_unclosed = v2.parse_block("## Findings block\n\n```findings-v2\n")
    assert empty_unclosed["state"] == "truncated"


def test_last_of_two_blocks_is_used_and_invalid():
    text = v2report(line(id="A1")) + "\n```findings-v2\n" + line(id="B1") + "\n```\n"
    r = v2.parse_block(text)
    assert [f["id"] for f in r["findings"]] == ["B1"] and r["state"] == "invalid"
