"""Sheet renderer (DESIGN 6, DD-6; TESTING DD-6 row): item JSON, sheet text, cap, class label only. No repository, no model."""

import json
import re
from pathlib import Path

from scaffold import briefs
from sweep import assign, plan, render

PLANS = Path(__file__).resolve().parents[1] / "fixtures" / "plans"
CLASSES = ("C4", "C8", "C5", "C2", "C1", "C6", "C7")
EXTRACTOR = {
    "C4": "E2",
    "C8": "E3",
    "C5": "E4",
    "C2": "E5",
    "C1": "E1",
    "C6": "E1",
    "C7": "E7",
}
ROUTE = {"C4": "search", "C8": "search", "C5": "search", "C6": "search"}
E2_EVIDENCE = [  # the entries attach_e2 makes for the DESIGN 4.3 example
    {"path": "plan", "line": 85, "text": 'the task orders the heading "Retry policy"'},
    {
        "path": "plan",
        "line": 85,
        "text": "pattern 'retry-policy' (case-sensitive) against ordered string 'Retry policy': NO MATCH",
    },
    {
        "path": "plan",
        "line": 85,
        "text": "after lowercasing and collapsing hyphens, spaces and underscores: MATCH",
    },
    {
        "path": "docs/ops.md",
        "line": 0,
        "text": "base checkout: git grep -c -F -e 'retry-policy' -- docs/ops.md gives 0",
    },
]


def row(n, cls="C4", priority=None, evidence=None, **over):
    r = {
        "item_id": f"S{n}",
        "class": cls,
        "extractor": EXTRACTOR[cls],
        "kind": "pattern",
        "anchor_text": f"Criterion {n} says the heading is present.",
        "location": {"task": "T4", "line_start": 200 + n, "line_end": 200 + n},
        "evidence": evidence if evidence is not None else [],
        "priority": 90 - n if priority is None else priority,
        "route": ROUTE.get(cls, "read"),
        "experimental": False,
    }
    r.update(over)
    return r


def assignment(rows, seed=0, panel="primary"):
    return assign.assign(rows, panel, seed=seed)


def test_sheet_text_in_brief_and_file_equal(tmp_path):
    rows = [
        row(n, CLASSES[n % 7], evidence=E2_EVIDENCE if n % 2 else [])
        for n in range(1, 9)
    ]
    a = assignment(rows, seed=5)
    sheets = render.render_sheets(rows, a)
    render.write(tmp_path, sheets)
    assert sorted(p.name for p in (tmp_path / "sheets").iterdir()) == sorted(
        f"{rid}.{ext}" for rid in a.reviewers for ext in ("md", "json")
    )
    doc = {"cand_sb": "/tmp/sb/cand/candidate.md", "sha": "0" * 64}
    checked = 0
    for rid, sheet in sheets.items():
        path = tmp_path / "sheets" / f"{rid}.md"
        file_text = path.read_text(encoding="utf-8")
        assert file_text == sheet.text and file_text
        brief = briefs.render("SS", doc, {"path": str(path), "text": file_text}, None)[
            "text"
        ]
        marker = "\n\n## SWEEP SHEET ITEMS\n\n"
        assert brief.count(marker) == 1
        assert brief.split(marker, 1)[1] == file_text
        assert str(path) in brief.split(marker, 1)[0]
        checked += 1
    assert checked == len(a.reviewers) == 3


def test_sheet_cap_16000_trims_lowest_priority():
    evidence = [
        {"path": f"tests/test_{k}.py", "line": 10 + k, "text": f"{k}" * 160}
        for k in range(5)
    ]
    rows = [
        row(n, CLASSES[n % 7], priority=100 - n, evidence=evidence)
        for n in range(1, 21)
    ]
    items = [render.item_json(r, 2) for r in rows]
    whole = render._text(items)
    assert len(whole) > render.SHEET_CAP  # the fixture overflows
    text, trimmed, shown = render.sheet_text(items)
    assert trimmed and len(text) <= render.SHEET_CAP
    assert text.split("\n")[0] == "Items assigned to you: " + ", ".join(
        r["item_id"] for r in rows
    )
    kept = [len(it["evidence"]) for it in shown]
    assert kept[0] == 5  # the highest priority is untouched
    assert (
        kept[-1] == 0 and "Tool output: none" in text
    )  # the lowest priority lost every entry
    # entries go from the lowest priority up: kept counts never rise toward lower priority, and the cut item is a prefix
    assert kept == sorted(kept, reverse=True)
    for it in shown:
        assert it["evidence"] == evidence[: len(it["evidence"])]
    # one more removal than needed would have been too many: the last removal was needed
    again, again_trimmed, _ = render.sheet_text(shown)
    assert again == text and not again_trimmed
    # the same data through render_sheets records the flag in the sheet JSON
    a = assign.assign(rows[:12], "primary", seed=1)
    s = render.render_sheets(rows[:12], a)
    assert {x.trimmed for x in s.values()} <= {True, False}
    j = json.loads(render.dumps(next(iter(s.values())).to_json()))
    assert j["sheet_trimmed"] in (True, False) and j["chars"] <= render.SHEET_CAP
    # a sheet under the cap is untouched
    small = [render.item_json(row(1, evidence=E2_EVIDENCE), 2)]
    t2, tr2, _ = render.sheet_text(small)
    assert not tr2 and t2 == render._text(small)


def test_class_label_only_no_hint():
    rows = [row(n, CLASSES[n % 7], evidence=E2_EVIDENCE) for n in range(1, 8)]
    rows[0].update(
        {"class": "C4", "extractor": "E2", "kind": "pattern", "priority": 95}
    )
    a = assignment(rows)
    for sheet in render.render_sheets(rows, a).values():
        t = sheet.text
        assert re.search(r"\(class C\d\)", t)
        assert not re.search(r"\bE[1-7]\b", t)  # no extractor name
        assert not re.search(r"priority|\bkind\b|\broute\b|\bextractor\b", t)
        assert not re.search(
            r"\b(8[3-9]|9[0-5])\b", t.replace("plan line 85", "")
        )  # no rank value
        assert not re.search(
            r"expected|should (fail|pass)|is a defect|will fail", t, re.I
        )
        assert "«" not in t and "pattern_kind" not in t
    one = render.sheet_text([render.item_json(rows[0], 2)])[0]
    assert "### S1   (class C4)" in one
    for word in ("E2", "95", "priority", "experimental", "extractor"):
        assert word not in one


def test_e2_evidence_prints_the_design_example():
    r = row(
        3,
        evidence=E2_EVIDENCE,
        anchor_text="`grep -c 'retry-policy' docs/ops.md` prints at least 1",
    )
    text = render.sheet_text([render.item_json(r, 2)])[0]
    assert text.split("\n", 2)[2] == "\n".join(
        [
            "### S3   (class C4)",
            "Where: Task 4 (plan lines 203-203)",
            "Text:  \"`grep -c 'retry-policy' docs/ops.md` prints at least 1\"",
            "Tool output:",
            '  - plan line 85: the task orders the heading "Retry policy"',
            "  - pattern 'retry-policy' (case-sensitive) against ordered string 'Retry policy': NO MATCH",
            "  - after lowercasing and collapsing hyphens, spaces and underscores: MATCH",
            "  - base checkout: git grep -c -F -e 'retry-policy' -- docs/ops.md gives 0",
            "Question: " + render.question_for(r | {"evidence": E2_EVIDENCE}),
            "Reply with one line in the ledger-v1 block: item S3, verdict OK, PROBLEM or UNSURE.",
        ]
    )
    repo_line = render._evidence_lines(
        [{"path": "tests/test_x.py", "line": 12, "text": "refers to it"}]
    )
    assert repo_line == ["  - tests/test_x.py:12: refers to it"]


def test_no_evidence_experimental_and_c3_question():
    r = row(
        1,
        cls="C2",
        evidence=[],
        extractor="E6",
        experimental=True,
        anchor_text="The gate keys on `retired`\n  when the row is read.",
    )
    r["class"] = "C3"
    ev = [
        {
            "path": "plan",
            "line": 5,
            "text": "write-position occurrences of 'retired': 0",
        }
    ]
    with_ev = render.item_json(dict(r, evidence=ev), 1)
    assert "value 'retired'." in with_ev["question"] and "«" not in with_ev["question"]
    bare = render.item_json(r, 1)
    assert "value 'retired'." in bare["question"]  # first backticked span of the anchor
    text = render.sheet_text([bare])[0]
    assert "Tool output: none" in text
    assert (
        text.index("Tool output: none")
        < text.index(render.EXPERIMENTAL_NOTE)
        < text.index("Question:")
    )
    assert 'Text:  "The gate keys on `retired` when the row is read."' in text
    plain = render.sheet_text([render.item_json(row(2), 1)])[0]
    assert render.EXPERIMENTAL_NOTE not in plain
    assert render.sheet_text([])[0] == ""  # R7: no items, empty sheet text


def test_item_json_fields_limits_and_conventions(tmp_path):
    rows = [row(n, CLASSES[n % 7], evidence=E2_EVIDENCE) for n in range(1, 6)]
    a = assignment(rows)
    j = render.items_json(rows, a)
    assert j["seed"] == 0 and len(j["items"]) == 5
    for it in j["items"]:
        assert tuple(it) == render.ITEM_FIELDS
        assert it["replicas"] == a.replicas[it["item_id"]] == 2
        assert it["location"]["task"] == "Task 4"
        assert it["question"]
    bad = row(1, anchor_text="x" * 201)
    try:
        render.item_json(bad, 1)
    except ValueError as e:
        assert "6.1" in str(e)
    else:
        raise AssertionError("a 201-character anchor must be refused")
    sheets = render.render_sheets(rows, a)
    render.write(tmp_path, sheets)
    for rid in sheets:
        raw = (tmp_path / "sheets" / f"{rid}.json").read_text(encoding="utf-8")
        assert raw.endswith("\n") and not raw.endswith("\n\n")
        assert (
            raw
            == json.dumps(json.loads(raw), sort_keys=True, ensure_ascii=False, indent=1)
            + "\n"
        )
        assert not re.search(r'"/|[A-Za-z]:\\', raw) and str(tmp_path) not in raw
        assert json.loads(raw)["items"] == sheets[rid].items
    ids = [i for ids in a.reviewers.values() for i in ids]
    assert (
        render.render_sheets(rows, a)["t4-1"].text == sheets["t4-1"].text
    )  # deterministic
    for rid, sheet in sheets.items():
        printed = re.findall(r"^### (S\d+)", sheet.text, re.M)
        assert printed == a.reviewers[rid]
        assert sheet.text.split("\n")[0] == "Items assigned to you: " + ", ".join(
            a.reviewers[rid]
        )
    assert len(ids) == sum(len(v) for v in a.item_reviewers.values())


def test_location_names_goal_constraint_and_criterion_with_doc():
    doc = plan.parse((PLANS / "p_basic.md").read_text(encoding="utf-8"))
    crit = next(b for b in doc.of("criterion") if b["task"] == "T2")
    con = doc.of("constraint")[0]
    goal = next(b for b in doc.of("criterion") if b["id"] == "goal")
    n = int(crit["id"].rsplit(".C", 1)[1])

    def loc(b):
        return {k: b[k] for k in ("task", "line_start", "line_end")}

    got = [
        render.item_json(row(1, location=loc(b)), 1, doc=doc)["location"]
        for b in (crit, con, goal)
    ]
    assert got[0]["task"] == "Task 2" and got[0]["part"] == f"acceptance criterion {n}"
    assert got[1]["task"] == "Constraints" and "part" not in got[1]
    assert got[2]["task"] == "Goal"
    assert (
        render.item_json(
            row(1, location={"task": None, "line_start": 1, "line_end": 1}), 1
        )["location"]["task"]
        == "Plan"
    )
    text = render.sheet_text(
        [render.item_json(row(1, location=loc(crit)), 1, doc=doc)]
    )[0]
    assert f"Where: Task 2, acceptance criterion {n} (plan lines" in text
