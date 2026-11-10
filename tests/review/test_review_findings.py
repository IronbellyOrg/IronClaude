"""findings-v1 / fixmap-v1 parsing and the anchor, fingerprint and cluster rules (PN1, C4-C5)."""

from __future__ import annotations

import difflib
import json

from superclaude.cli.review import findings as fnd

DOC = """# Title

## 1. Purpose

Intro text for the document.

## 2. Requirements

- **FR-1 Alpha.** The worker sends a request and waits at most
  10 seconds for a response from the endpoint.
- **FR-2 Beta.** A failed attempt is retried at most 5 times.

## 3. Operations

Retry the delivery up to 8 times with backoff, then mark it failed.
"""


def line(**kw):
    base = {
        "id": "F1",
        "severity": "CRITICAL",
        "blocking": True,
        "category": "contradiction",
        "anchor": "A failed attempt is retried at most 5 times",
        "refs": ["FR-2"],
        "claim": "c",
    }
    base.update(kw)
    return json.dumps(base)


def report(*lines, heading="## Findings block", info="findings-v1"):
    body = "\n".join(lines)
    return f"review: 1 of 3\n\nbody text\n\n{heading}\n\n```{info}\n{body}\n```\n"


# --- C4.1 -------------------------------------------------------------------


def test_parse_good_block():
    r = fnd.parse_block(report(line(), line(id="F2", severity="MINOR", blocking=False)))
    assert r["ok"] is True and r["errors"] == []
    assert [f["id"] for f in r["findings"]] == ["F1", "F2"]
    assert r["priors"] == []


def test_empty_block_means_no_findings():
    r = fnd.parse_block(report())
    assert r["ok"] is True and r["findings"] == []


def test_missing_heading_and_missing_block():
    assert fnd.parse_block("review: 1 of 3\nnothing here\n")["ok"] is False
    r = fnd.parse_block("review: 1 of 3\n\n## Findings block\n\nno fence\n")
    assert r["ok"] is False and r["findings"] == []
    r = fnd.parse_block(report(line(), info="json"))
    assert r["ok"] is False


def test_bad_json_line_keeps_good_lines():
    r = fnd.parse_block(report(line(), "{not json", line(id="F3")))
    assert r["ok"] is False
    assert [f["id"] for f in r["findings"]] == ["F1", "F3"]
    assert (
        len(r["errors"]) == 1 and "line" in r["errors"][0] and "msg" in r["errors"][0]
    )


def test_minor_blocking_is_an_error():
    r = fnd.parse_block(report(line(severity="MINOR", blocking=True)))
    assert r["ok"] is False and r["findings"] == []
    assert any("MINOR" in e["msg"] for e in r["errors"])


def test_field_validation():
    assert fnd.parse_block(report(line(anchor="short")))["ok"] is False  # < 12 chars
    assert fnd.parse_block(report(line(anchor="x" * 201)))["ok"] is False
    assert fnd.parse_block(report(line(category="weird")))["ok"] is False
    assert fnd.parse_block(report(line(severity="HIGH")))["ok"] is False
    assert fnd.parse_block(report(line(refs=["a"] * 9)))["ok"] is False
    assert fnd.parse_block(report(line(claim="x" * 301)))["ok"] is False
    assert fnd.parse_block(report(line(id="bad id")))["ok"] is False
    assert fnd.parse_block(report(line(), line()))["ok"] is False  # duplicate id
    assert fnd.parse_block(report(line(blocking="yes")))["ok"] is False
    ok = fnd.parse_block(report(line(anchor2="  another   quote here  ")))
    assert ok["ok"] is True


def test_last_of_two_blocks_wins():
    text = report(line(id="A1")) + "\n" + "```findings-v1\n" + line(id="B1") + "\n```\n"
    r = fnd.parse_block(text)
    assert [f["id"] for f in r["findings"]] == ["B1"]
    assert r["ok"] is False and any("more than one" in e["msg"] for e in r["errors"])


def test_prior_lines():
    prior = json.dumps({"prior": "L3", "status": "resolved"})
    r = fnd.parse_block(
        report(line(), prior, json.dumps({"prior": "L4", "status": "open"}))
    )
    assert r["ok"] is True
    assert r["priors"] == [
        {"prior": "L3", "status": "resolved"},
        {"prior": "L4", "status": "open"},
    ]
    bad = fnd.parse_block(report(json.dumps({"prior": "L3", "status": "maybe"})))
    assert bad["ok"] is False


# --- C4.2 -------------------------------------------------------------------


def test_parse_fixmap_block():
    items = [
        {"id": "L1", "action": "applied", "reason": "r"},
        {"id": "L2", "action": "rejected", "reason": "no"},
    ]
    text = (
        "Done.\n\n## Fix map\n\n```fixmap-v1\n"
        + "\n".join(json.dumps(i) for i in items)
        + "\n```\n"
    )
    r = fnd.parse_fixmap(text)
    assert r["ok"] is True and r["items"] == items


def test_fixmap_table_fallback():
    text = "| id | action |\n|---|---|\n| F1 | Applied in 2.1 |\n| F2 | rejected: no |\n| **F3** | applied |\n"
    r = fnd.parse_fixmap(text)
    assert r["ok"] is False
    assert [i["id"] for i in r["items"]] == ["F1", "F3"]
    assert all(i["action"] == "applied" for i in r["items"])


def test_fixmap_bad_action_is_an_error():
    text = '## Fix map\n\n```fixmap-v1\n{"id": "L1", "action": "maybe", "reason": "r"}\n{"id": "L2", "action": "applied", "reason": "r"}\n```\n'
    r = fnd.parse_fixmap(text)
    assert r["ok"] is False and [i["id"] for i in r["items"]] == ["L2"]


# --- C5 ---------------------------------------------------------------------


def test_flat_and_locate_across_a_line_wrap():
    assert fnd.flat("a  b\n c") == "a b c"
    spans = fnd.locate(DOC, "waits at most 10 seconds for a response")
    assert spans == [(8, 10)]
    assert fnd.locate(DOC, "no such text anywhere") == []
    assert fnd.locate(DOC, "") == []
    two = fnd.locate("x line\nx line\n", "x line")
    assert two == [(0, 1), (1, 2)]


def test_section_of():
    lines = DOC.splitlines()
    assert fnd.section_of(DOC, 0) == "top" or fnd.section_of(DOC, 0) == "title"
    assert fnd.section_of(DOC, lines.index("Intro text for the document.")) == "1"
    assert fnd.section_of(DOC, 9) == "2"
    text = "Preface\n\n## Open Questions (v2)\n\nbody\n\n### 3.2.1 Deep\n\nbody\n"
    assert fnd.section_of(text, 4) == "open-questions-v2-"
    assert fnd.section_of(text, 7) == "3.2.1"
    assert fnd.section_of("no heading at all\n", 0) == "top"


def test_refs_norm():
    f = {
        "anchor": "see ac-0.4 and AC-1.2.",
        "anchor2": "P1 and SHA-256 and WC-4",
        "claim": "FR-2 conflicts",
        "refs": ["5.1", "fr-9", "AC-0.4"],
    }
    got = fnd.refs_norm(f)
    assert got == sorted(set(got))
    assert "SHA-256" not in got
    assert {"5.1", "AC-0.4", "AC-1.2", "P1", "WC-4", "FR-2"} <= set(got)
    assert "FR-9" not in got  # lower-case ids are not matches


def test_annotate_and_fingerprint_stable_when_only_claim_wording_changes():
    a = fnd.annotate(json.loads(line(claim="first wording")), DOC)
    b = fnd.annotate(json.loads(line(claim="a completely different wording")), DOC)
    assert a["fp"] == b["fp"] and len(a["fp"]) == 16
    assert a["span"] is not None and a["anchor_status"] == "found"
    c = fnd.annotate(json.loads(line(refs=["FR-9"])), DOC)
    assert c["fp"] != a["fp"]
    m = fnd.annotate(json.loads(line(anchor="text that is not in the document")), DOC)
    assert m["anchor_status"] == "missing" and m["span"] is None
    assert m["fp"] == fnd.fingerprint("none", m["refs_norm"])


def test_anchor_ambiguous_flag():
    d = "alpha beta gamma delta\n\nalpha beta gamma delta\n"
    a = fnd.annotate(json.loads(line(anchor="alpha beta gamma delta", refs=[])), d)
    assert a["anchor_ambiguous"] is True and a["span"] == (0, 1)


def test_same_defect_within_and_beyond_three_lines():
    def mk(start, refs, fp="x"):
        return {"fp": fp, "span": (start, start + 1), "span2": None, "refs_norm": refs}

    assert fnd.same_defect(mk(10, ["A-1"], "p"), mk(10, ["A-1"], "q"))
    assert fnd.same_defect(
        mk(10, ["A-1"], "p"), mk(14, ["A-1"], "q")
    )  # 10..11 and 14..15: 14 <= 11 + 3
    assert not fnd.same_defect(mk(10, ["A-1"], "p"), mk(15, ["A-1"], "q"))
    assert not fnd.same_defect(
        mk(10, ["A-1"], "p"), mk(10, ["B-2"], "q")
    )  # near but different refs
    assert fnd.same_defect(mk(10, [], "p"), mk(11, [], "q"))  # both empty
    assert not fnd.same_defect(mk(10, [], "p"), mk(11, ["A-1"], "q"))
    assert fnd.same_defect(
        mk(10, ["A-1"], "same"), mk(90, ["B-2"], "same")
    )  # same fingerprint
    far = {"fp": "p", "span": (50, 51), "span2": (11, 12), "refs_norm": ["A-1"]}
    assert fnd.same_defect(mk(10, ["A-1"], "q"), far)  # anchor2 counts


def test_clusters_are_deterministic_and_complete():
    found = []
    for i, (anchor, refs) in enumerate(
        [
            ("A failed attempt is retried at most 5 times", ["FR-2"]),
            ("Intro text for the document.", ["FR-2"]),
            ("waits at most 10 seconds for a response", ["FR-1"]),
            ("A failed attempt is retried at most 5 times", ["FR-2"]),
        ]
    ):
        found.append(
            fnd.annotate(
                {
                    "id": f"F{i}",
                    "severity": "MAJOR",
                    "blocking": True,
                    "category": "other",
                    "anchor": anchor,
                    "refs": refs,
                    "claim": "c",
                },
                DOC,
            )
        )
    c1 = fnd.cluster(found)
    c2 = fnd.cluster(found)
    assert [[f["id"] for f in c] for c in c1] == [[f["id"] for f in c] for c in c2]
    assert sum(len(c) for c in c1) == 4
    assert [f["id"] for f in c1[0]] == ["F0", "F3"]
    assert [[f["id"] for f in c] for c in c1][1:] == [["F1"], ["F2"]]


def test_map_span_and_hunks_touch():
    old = ["a", "b", "c", "d", "e", "f"]
    new = ["a", "b", "X", "Y", "d", "e", "f", "g"]
    ops = difflib.SequenceMatcher(None, old, new, autojunk=False).get_opcodes()
    assert fnd.map_span((0, 2), ops) == (0, 2)
    assert fnd.map_span((3, 5), ops) == (4, 6)
    assert fnd.map_span((2, 3), ops) == (
        2,
        3,
    )  # replaced line maps to the start of its new range
    assert fnd.hunks_touch((2, 3), ops) is True
    assert fnd.hunks_touch((0, 2), ops) is False
    assert fnd.hunks_touch((3, 5), ops) is False
    assert (
        fnd.hunks_touch((4, 6), ops) is True
    )  # the zero-width insert at the end of the text touches a span ending there
    ins = difflib.SequenceMatcher(
        None, ["a", "b"], ["a", "N", "b"], autojunk=False
    ).get_opcodes()
    assert (
        fnd.hunks_touch((0, 1), ins) is True
    )  # zero-width hunk at p=1 touches spans with start <= 1 <= end
    assert fnd.hunks_touch((1, 2), ins) is True
    assert fnd.hunks_touch((2, 3), ins) is False
