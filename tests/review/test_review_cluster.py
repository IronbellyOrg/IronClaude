"""K4 cluster_v2: path-aware clustering, the chained guard and cluster_agreement."""

from __future__ import annotations

import ast
import copy
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest
from test_review_cli import A_S1, A_S3, SEEDED, finding, report

from superclaude.cli.review import cluster as cl

SNAP = ["src/a.py", "src/b.py", "plan.md", "spec.md"]
MODULE = Path(cl.__file__)


def cit(path="src/a.py", start=10, end=None, role="source"):
    return {"role": role, "path": path, "line_start": start, "line_end": end or start}


def fnd(fid, *cits, refs=(), blocking=True, cls=None, claim="x", lens=None):
    out = {
        "id": fid,
        "severity": "MAJOR" if blocking else "MINOR",
        "blocking": blocking,
        "category": "other",
        "claim": claim,
        "refs": list(refs),
        "citations": list(cits) or [cit()],
    }
    if cls is not None:
        out["deviation_class"] = cls
    if lens is not None:
        out["lens"] = lens
    return out


def block(*findings, state="complete"):
    return {
        "ok": state == "complete",
        "state": state,
        "findings": list(findings),
        "errors": [],
    }


def rec(rid, ordinal, *findings, cal=None, state="complete"):
    return (rid, ordinal, block(*findings, state=state), cal)


def ids(result):
    return [
        [(m["reviewer_id"], m["id"]) for m in c["members"]] for c in result["clusters"]
    ]


# ------------------------------------------------------------ acceptance: spans and paths


def test_line_10_of_two_different_files_does_not_cluster():
    out = cl.cluster_v2(
        [
            rec("r1", 1, fnd("A", cit("src/a.py", 10), refs=["REQ-1"])),
            rec("r2", 2, fnd("B", cit("src/b.py", 10), refs=["REQ-1"])),
        ],
        SNAP,
    )
    assert ids(out) == [[("r1", "A")], [("r2", "B")]]


def test_same_file_within_3_lines_and_equal_refs_cluster():
    out = cl.cluster_v2(
        [
            rec("r1", 1, fnd("A", cit("src/a.py", 10), refs=["REQ-1"])),
            rec("r2", 2, fnd("B", cit("src/a.py", 13), refs=["REQ-1"])),
        ],
        SNAP,
    )
    assert ids(out) == [[("r1", "A"), ("r2", "B")]]
    assert out["clusters"][0]["reviewers"] == ["r1", "r2"]


def test_same_file_4_lines_apart_or_unequal_refs_do_not_cluster():
    apart = cl.cluster_v2(
        [
            rec("r1", 1, fnd("A", cit("src/a.py", 10))),
            rec("r2", 2, fnd("B", cit("src/a.py", 14))),
        ],
        SNAP,
    )
    assert len(apart["clusters"]) == 2
    refs = cl.cluster_v2(
        [
            rec("r1", 1, fnd("A", cit("src/a.py", 10), refs=["REQ-1"])),
            rec("r2", 2, fnd("B", cit("src/a.py", 10), refs=["REQ-2"])),
        ],
        SNAP,
    )
    assert len(refs["clusters"]) == 2


def test_chain_a_b_c_with_a_and_c_unequal_is_chained_and_listed():
    out = cl.cluster_v2(
        [
            rec("r1", 1, fnd("A", cit("src/a.py", 10))),
            rec("r2", 2, fnd("B", cit("src/a.py", 13))),
            rec("r3", 3, fnd("C", cit("src/a.py", 16))),
        ],
        SNAP,
    )
    assert ids(out) == [[("r1", "A"), ("r2", "B"), ("r3", "C")]]
    assert out["clusters"][0]["chained"] is True
    assert out["chained"] == ["C1"]
    # the only blocking cluster is chained, so nothing is counted and there is no mean
    assert out["agreement_clusters"] == [] and out["cluster_agreement"] is None


def test_a_cluster_whose_members_all_match_is_not_chained():
    out = cl.cluster_v2(
        [
            rec("r1", 1, fnd("A", cit("src/a.py", 10))),
            rec("r2", 2, fnd("B", cit("src/a.py", 11))),
        ],
        SNAP,
    )
    assert out["clusters"][0]["chained"] is False and out["chained"] == []


def test_unresolved_path_never_clusters_by_span():
    same = dict(refs=["REQ-1"], cls="drift")
    out = cl.cluster_v2(
        [
            rec("r1", 1, fnd("A", cit("src/zz.py", 10), **same)),
            rec("r2", 2, fnd("B", cit("src/zz.py", 10), **same)),
        ],
        SNAP,
    )
    assert len(out["clusters"]) == 2
    assert out["citations"] == {"resolved": 0, "unresolved": 2, "malformed": 0}
    assert [c["members"][0]["fp"] for c in out["clusters"]] == [None, None]
    # the same pair on a snapshot path clusters
    ok = cl.cluster_v2(
        [
            rec("r1", 1, fnd("A", cit("src/a.py", 10), **same)),
            rec("r2", 2, fnd("B", cit("src/a.py", 10), **same)),
        ],
        SNAP,
    )
    assert len(ok["clusters"]) == 1


def test_snapshot_path_match_is_exact_and_accepts_snapshot_entries():
    entries = [{"path": "src/a.py", "sha256": "0" * 64}]
    out = cl.cluster_v2(
        [
            rec("r1", 1, fnd("A", cit("./src/a.py", 10))),
            rec("r2", 2, fnd("B", cit("src/a.py", 10))),
        ],
        entries,
    )
    assert out["citations"] == {"resolved": 1, "unresolved": 1, "malformed": 0}
    assert len(out["clusters"]) == 2


def test_unresolved_citation_does_not_block_a_resolved_one():
    out = cl.cluster_v2(
        [
            rec("r1", 1, fnd("A", cit("src/zz.py", 10), cit("src/a.py", 40))),
            rec("r2", 2, fnd("B", cit("src/a.py", 42))),
        ],
        SNAP,
    )
    assert len(out["clusters"]) == 1


def test_malformed_and_converter_unresolved_citations_never_join():
    bad = {"role": "source", "path": "/abs/a.py", "line_start": 10, "line_end": 10}
    conv = {"role": "unresolved", "ref": "src/a.py:10", "reason": "no path"}
    out = cl.cluster_v2(
        [
            rec("r1", 1, fnd("A", bad)),
            rec("r2", 2, fnd("B", conv)),
            rec("r3", 3, fnd("C", cit("src/a.py", 10))),
        ],
        SNAP,
    )
    assert len(out["clusters"]) == 3
    assert out["citations"] == {"resolved": 1, "unresolved": 0, "malformed": 2}


# ------------------------------------------------------------ classes, refs, fingerprint, primary


@pytest.mark.parametrize(
    "c1, c2, joined",
    [
        ("drift", "regression", False),
        ("drift", "drift", True),
        ("drift", "none", True),
        ("drift", None, True),
        (None, None, True),
    ],
)
def test_deviation_classes_must_be_compatible(c1, c2, joined):
    out = cl.cluster_v2(
        [
            rec("r1", 1, fnd("A", cls=c1)),
            rec("r2", 2, fnd("B", cls=c2)),
        ],
        SNAP,
    )
    assert (len(out["clusters"]) == 1) is joined


def test_refs_norm_reads_claim_tokens_like_v1():
    out = cl.cluster_v2(
        [
            rec("r1", 1, fnd("A", claim="breaks REQ-7")),
            rec("r2", 2, fnd("B", refs=["REQ-7"])),
            rec("r3", 3, fnd("C", refs=["REQ-8"])),
        ],
        SNAP,
    )
    assert ids(out) == [[("r1", "A"), ("r2", "B")], [("r3", "C")]]


def test_fingerprint_of_a_citation_only_finding_uses_an_empty_section():
    out = cl.cluster_v2(
        [rec("r1", 1, fnd("A", cit("src/a.py", 10), refs=["REQ-1"], cls="drift"))],
        SNAP,
    )
    want = hashlib.sha256(b"v2|source|src/a.py||REQ-1|drift").hexdigest()
    assert out["clusters"][0]["members"][0]["fp"] == want
    none_class = cl.annotate(fnd("A", refs=["REQ-1"]), set(SNAP))
    assert none_class["fp"] == hashlib.sha256(b"v2|source|src/a.py||REQ-1|").hexdigest()


def test_equal_fingerprints_match_only_with_non_empty_refs():
    with_refs = cl.cluster_v2(
        [
            rec("r1", 1, fnd("A", cit("src/a.py", 10), refs=["REQ-1"])),
            rec("r2", 2, fnd("B", cit("src/a.py", 200), refs=["REQ-1"])),
        ],
        SNAP,
    )
    assert len(with_refs["clusters"]) == 1
    no_refs = cl.cluster_v2(
        [
            rec("r1", 1, fnd("A", cit("src/a.py", 10))),
            rec("r2", 2, fnd("B", cit("src/a.py", 200))),
        ],
        SNAP,
    )
    assert len(no_refs["clusters"]) == 2


@pytest.mark.parametrize(
    "lens, roles, want",
    [
        ("reflect-pre", ["spec", "plan"], 1),
        ("reflect-post", ["plan", "diff", "source"], 1),
        ("reflect-post", ["plan", "source"], 1),
        ("spec", ["plan", "spec"], 1),
        (None, ["spec", "plan"], 0),
        ("reflect-pre", ["spec", "source"], 0),
    ],
)
def test_primary_citation_rule(lens, roles, want):
    f = fnd("A", *[cit("plan.md", 1, role=r) for r in roles], lens=lens)
    assert cl.annotate(f, set(SNAP))["primary_citation"]["index"] == want


def test_finding_without_citations_has_no_primary_and_stays_alone():
    anchor_only = {
        "id": "A",
        "severity": "MAJOR",
        "blocking": True,
        "category": "other",
        "anchor": "an anchor quote of enough length",
        "claim": "x",
        "refs": ["REQ-1"],
    }
    out = cl.cluster_v2(
        [rec("r1", 1, anchor_only), rec("r2", 2, dict(anchor_only, id="B"))], SNAP
    )
    assert len(out["clusters"]) == 2
    assert out["clusters"][0]["members"][0]["primary_citation"] is None


# ------------------------------------------------------------ cluster_agreement, support, representative


def test_cluster_agreement_is_1_with_no_blocking_clusters_and_two_valid_blocks():
    empty = ("r2", 2, block(), {})
    out = cl.cluster_v2(
        [rec("r1", 1, fnd("A", blocking=False), cal={"A": 0.9}), empty], SNAP
    )
    assert out["valid_blocks"] == 2 and out["blocking_clusters"] == 0
    assert out["cluster_agreement"] == 1.0


def test_cluster_agreement_is_null_with_fewer_than_two_valid_blocks():
    one = cl.cluster_v2(
        [
            rec("r1", 1, fnd("A", blocking=False)),
            rec("r2", 2, fnd("B", blocking=False), state="invalid"),
        ],
        SNAP,
    )
    assert one["valid_blocks"] == 1 and one["cluster_agreement"] is None
    assert one["invalid_reviewers"] == ["r2"]
    assert cl.cluster_v2([], SNAP)["cluster_agreement"] is None


def test_support_and_agreement_from_calibrated_confidences():
    out = cl.cluster_v2(
        [
            rec("r1", 1, fnd("A"), cal={"A": 0.9}),
            rec(
                "r2",
                2,
                fnd("B"),
                fnd("B2", cit("src/a.py", 11)),
                cal={"B": 0.6, "B2": 0.3},
            ),
            rec("r3", 3, fnd("C", cit("src/b.py", 50)), cal={"C": 0.8}),
        ],
        SNAP,
    )
    first, second = out["clusters"]
    # r1 (0.9) and r2 (max of 0.6, 0.3) over the weights 0.9 + 0.6 + 0.8
    assert first["support"] == pytest.approx(1.5 / 2.3)
    assert first["member_scores"] == [0.9, 0.6, 0.3]
    assert second["support"] == pytest.approx(0.8 / 2.3)
    assert out["cluster_agreement"] == pytest.approx(0.5)
    assert out["agreement_clusters"] == ["C1", "C2"]


def test_support_below_1_differs_from_the_count_based_value():
    out = cl.cluster_v2(
        [
            rec("r1", 1, fnd("A"), cal={"A": 0.4}),
            rec("r2", 2, fnd("B", cit("src/b.py", 1)), cal={"B": 0.8}),
        ],
        SNAP,
    )
    first, second = out["clusters"]
    # weights 0.4 + 0.8; dividing by 2 reviewers would give 0.2 and 0.4
    assert first["support"] == pytest.approx(1 / 3) != 0.4 / 2
    assert second["support"] == pytest.approx(2 / 3) != 0.8 / 2
    assert first["disputed"] is True and second["disputed"] is False
    assert out["cluster_agreement"] == pytest.approx(0.5)


def test_weight_is_the_reviewers_best_finding_even_outside_the_cluster():
    out = cl.cluster_v2(
        [
            rec(
                "r1",
                1,
                fnd("A", cit("src/a.py", 10)),
                fnd("A2", cit("src/b.py", 1)),
                cal={"A": 0.5, "A2": 0.9},
            ),
            rec("r2", 2, fnd("B", cit("src/a.py", 11)), cal={"B": 0.5}),
        ],
        SNAP,
    )
    assert ids(out) == [[("r1", "A"), ("r2", "B")], [("r1", "A2")]]
    first, second = out["clusters"]
    # denominator is w(r1) = 0.9 (A2, outside C1) + w(r2) = 0.5
    assert first["support"] == pytest.approx(1.0 / 1.4)
    assert second["support"] == pytest.approx(0.9 / 1.4)


def test_support_is_1_when_every_reviewer_is_in_with_its_best_finding():
    out = cl.cluster_v2(
        [
            rec(
                "r1",
                1,
                fnd("A"),
                fnd("A2", cit("src/b.py", 1)),
                cal={"A": 0.6, "A2": 0.3},
            ),
            rec("r2", 2, fnd("B"), cal={"B": 0.7}),
        ],
        SNAP,
    )
    first, second = out["clusters"]
    assert first["support"] == pytest.approx(1.0)
    assert second["support"] == pytest.approx(0.3 / 1.3)


def test_reviewer_with_an_empty_block_has_weight_0():
    out = cl.cluster_v2(
        [
            rec(
                "r1",
                1,
                fnd("A"),
                fnd("A2", cit("src/b.py", 1)),
                cal={"A": 0.8, "A2": 0.4},
            ),
            rec("r2", 2),
        ],
        SNAP,
    )
    # denominator is w(r1) = 0.8 + w(r2) = 0
    assert [c["support"] for c in out["clusters"]] == pytest.approx([1.0, 0.5])
    assert out["uncalibrated"] == []
    assert out["cluster_agreement"] == pytest.approx(0.75)


@pytest.mark.parametrize(
    "r1_conf, r2",
    [
        (0.9, rec("r2", 2, fnd("B", cit("src/b.py", 1)), cal={})),
        (0.0, rec("r2", 2, fnd("B", cit("src/b.py", 1)), cal={"B": 0.0})),
        (0.0, rec("r2", 2)),
    ],
    ids=["uncalibrated-finding", "zero-weights", "zero-weight-and-empty-block"],
)
def test_unknown_denominator_makes_every_support_null(r1_conf, r2):
    out = cl.cluster_v2([rec("r1", 1, fnd("A"), cal={"A": r1_conf}), r2], SNAP)
    # r1's cluster is fully calibrated, yet the denominator is unknown
    assert out["clusters"][0]["member_scores"] == [r1_conf]
    assert all(c["support"] is None for c in out["clusters"])
    assert out["uncalibrated"] == [c["cluster_id"] for c in out["clusters"]]
    assert out["cluster_agreement"] is None


def test_uncalibrated_member_gives_no_support_and_is_listed():
    out = cl.cluster_v2(
        [
            rec("r1", 1, fnd("A"), cal={"A": 0.9}),
            rec("r2", 2, fnd("B"), cal={}),
            rec("r3", 3, fnd("C", cit("src/b.py", 1)), cal=None),
        ],
        SNAP,
    )
    assert [c["support"] for c in out["clusters"]] == [None, None]
    assert out["uncalibrated"] == ["C1", "C2"]
    assert out["uncalibrated_findings"] == [
        {"reviewer_id": "r2", "id": "B"},
        {"reviewer_id": "r3", "id": "C"},
    ]
    assert out["cluster_agreement"] is None


@pytest.mark.parametrize("value", [float("nan"), float("inf"), 1.5, -0.1, True, "0.9"])
def test_unusable_confidence_counts_as_uncalibrated_and_is_reported(value):
    out = cl.cluster_v2(
        [
            rec("r1", 1, fnd("A"), cal={"A": value}),
            rec("r2", 2, fnd("B", cit("src/b.py", 1)), cal={"B": 1}),
        ],
        SNAP,
    )
    assert out["uncalibrated_findings"] == [{"reviewer_id": "r1", "id": "A"}]
    assert any("'A'" in p["msg"] for p in out["problems"])
    json.dumps(out, allow_nan=False)


def test_chained_cluster_excluded_from_agreement_count():
    out = cl.cluster_v2(
        [
            rec("r1", 1, fnd("A", cit("src/a.py", 10)), cal={"A": 0.2}),
            rec("r2", 2, fnd("B", cit("src/a.py", 13)), cal={"B": 0.2}),
            rec(
                "r3",
                3,
                fnd("C", cit("src/a.py", 16)),
                fnd("D", cit("src/b.py", 1)),
                cal={"C": 0.2, "D": 0.9},
            ),
        ],
        SNAP,
    )
    assert out["chained"] == ["C1"] and out["agreement_clusters"] == ["C2"]
    assert out["cluster_agreement"] == pytest.approx(0.9 / 1.3)


def test_representative_is_highest_confidence_with_ties_by_resolution_order():
    records = [
        rec("late", 5, fnd("L", claim="late claim"), cal={"L": 0.7}),
        rec("early", 2, fnd("E", claim="early claim"), cal={"E": 0.7}),
        rec("low", 1, fnd("W", claim="low claim"), cal={"W": 0.1}),
    ]
    out = cl.cluster_v2(records, SNAP)
    c = out["clusters"][0]
    assert [m["reviewer_id"] for m in c["members"]] == ["low", "early", "late"]
    assert c["representative"] == {"reviewer_id": "early", "id": "E"}
    assert c["claim"] == "early claim"


def test_uncalibrated_member_ranks_below_calibrated_for_representative():
    out = cl.cluster_v2(
        [
            rec("r1", 1, fnd("A", claim="first"), cal={}),
            rec("r2", 2, fnd("B", claim="second"), cal={"B": 0.1}),
        ],
        SNAP,
    )
    assert out["clusters"][0]["claim"] == "second"


def test_blocking_any_all_and_disputed():
    split = cl.cluster_v2(
        [
            rec("r1", 1, fnd("A", blocking=True), cal={"A": 0.9}),
            rec("r2", 2, fnd("B", blocking=False), cal={"B": 0.9}),
        ],
        SNAP,
    )["clusters"][0]
    assert split["blocking_any"] is True and split["blocking_all"] is False
    assert split["support"] == pytest.approx(1.0) and split["disputed"] is True

    agreed = cl.cluster_v2(
        [
            rec("r1", 1, fnd("A"), cal={"A": 0.9}),
            rec("r2", 2, fnd("B"), cal={"B": 0.9}),
        ],
        SNAP,
    )["clusters"][0]
    assert agreed["blocking_all"] is True and agreed["disputed"] is False

    low = cl.cluster_v2(
        [
            rec("r1", 1, fnd("A"), cal={"A": 0.4}),
            rec("r2", 2, fnd("B", cit("src/b.py", 1)), cal={"B": 0.9}),
        ],
        SNAP,
    )["clusters"][0]
    assert low["support"] == pytest.approx(0.4 / 1.3) and low["disputed"] is True

    classes = cl.cluster_v2(
        [
            rec("r1", 1, fnd("A", cls="drift"), cal={"A": 0.9}),
            rec("r2", 2, fnd("B", cls="none"), cal={"B": 0.9}),
        ],
        SNAP,
    )["clusters"][0]
    assert classes["disputed"] is True


# ------------------------------------------------------------ records, robustness, purity


def test_bare_list_is_a_valid_block_and_invalid_block_findings_are_not_clustered():
    out = cl.cluster_v2(
        [
            ("r1", 1, [fnd("A")], {}),
            rec("r2", 2, fnd("B"), state="truncated"),
            ("r3", 3, {"state": "complete", "findings": "nope"}, {}),
        ],
        SNAP,
    )
    assert out["complete_reviewers"] == ["r1"]
    assert out["invalid_reviewers"] == ["r2", "r3"]
    assert ids(out) == [[("r1", "A")]]


def test_duplicate_reviewer_id_is_skipped_and_reported():
    out = cl.cluster_v2(
        [rec("r1", 2, fnd("A")), rec("r1", 1, fnd("B", cit("src/b.py", 1)))], SNAP
    )
    assert ids(out) == [[("r1", "B")]]
    assert any("duplicate reviewer_id" in p["msg"] for p in out["problems"])


MALFORMED = [
    None,
    5,
    "text",
    {},
    [None],
    [("r1",)],
    [("r1", "1", [], {})],
    [(7, 1, [], {})],
    [("r1", True, [], {})],
    [("r1", 1, None, None)],
    [("r1", 1, [None, {"id": 5}, {"id": ""}], "cal")],
    [
        (
            "r1",
            1,
            [
                {"id": "a", "citations": "x"},
                {"id": "a"},
                {
                    "id": "b",
                    "citations": [
                        None,
                        {"role": "source", "path": 3, "line_start": "1"},
                        {
                            "role": "source",
                            "path": "src/a.py",
                            "line_start": 0,
                            "line_end": 1,
                        },
                        {
                            "role": "source",
                            "path": "src/a.py",
                            "line_start": 5,
                            "line_end": 2,
                        },
                        {
                            "role": "source",
                            "path": "src/a.py",
                            "line_start": 1,
                            "line_end": 1,
                            "quote": "short",
                        },
                    ],
                    "refs": [1, None, ["REQ-1"]],
                    "claim": 7,
                    "anchor": ["x"],
                    "blocking": "yes",
                    "deviation_class": ["drift"],
                    "lens": {"x": 1},
                },
                {"id": "c", "refs": "REQ-1", "citations": [cit()]},
            ],
            {"a": float("nan"), "b": True, ("t",): 1},
        ),
        ("r2", 2, [{"id": "d", "citations": [cit()]}], {"d": 0.5}),
    ],
]


@pytest.mark.parametrize("records", MALFORMED)
@pytest.mark.parametrize(
    "snapshot", [SNAP, None, 3, "src/a.py", [None, {"path": 3}, "src/a.py"]]
)
def test_malformed_input_never_raises(records, snapshot):
    out = cl.cluster_v2(records, snapshot)
    json.dumps(out, allow_nan=False)
    assert isinstance(out["clusters"], list)
    kept = cl.clusters_kept(records, snapshot, [("r1", "a"), ["r2", "d"], None])
    json.dumps(kept, allow_nan=False)


def test_malformed_input_is_reported():
    out = cl.cluster_v2(MALFORMED[-1], [None, "src/a.py"])
    msgs = " | ".join(p["msg"] for p in out["problems"])
    for part in (
        "snapshot entry 0 has no path string",
        "duplicate finding id 'a'",
        "calibration for 'a' is not a number from 0 to 1",
    ):
        assert part in msgs
    assert out["citations"]["malformed"] == 5
    bad = cl.cluster_v2([("r1", "1", [], {}), ("r2", 1, [], "cal"), 3], 3)
    msgs = " | ".join(p["msg"] for p in bad["problems"])
    for part in (
        "snapshot_file_list is not a list of paths",
        "ordinal must be an integer",
        "calibration_map is not a mapping; treated as empty",
        "a record must be (reviewer_id, ordinal, block, calibration_map)",
    ):
        assert part in msgs
    assert (
        "reviewer_records is not a list of records"
        in cl.cluster_v2(5, SNAP)["problems"][0]["msg"]
    )


def test_inputs_are_not_changed_and_output_is_deterministic():
    records = [
        rec("r2", 2, fnd("B", cit("src/a.py", 12), refs=["REQ-1"]), cal={"B": 0.4}),
        rec(
            "r1",
            1,
            fnd("A", cit("src/a.py", 10), refs=["REQ-1"]),
            fnd("Z", cit("src/b.py", 3)),
            cal={"A": 0.8},
        ),
        rec("r3", 3, fnd("C", cit("src/b.py", 4)), cal={"C": 0.5}),
    ]
    before = copy.deepcopy(records)
    first = json.dumps(cl.cluster_v2(records, SNAP), sort_keys=False)
    assert records == before
    assert json.dumps(cl.cluster_v2(records, list(reversed(SNAP)))) == first
    shuffled = [records[2], records[0], records[1]]
    assert json.dumps(cl.cluster_v2(shuffled, SNAP)) == first
    assert ids(json.loads(first)) == [
        [("r1", "A"), ("r2", "B")],
        [("r1", "Z"), ("r3", "C")],
    ]


# ------------------------------------------------------------ second pass


def test_clusters_kept_recomputes_over_kept_findings_only():
    records = [
        rec("r1", 1, fnd("A", cit("src/a.py", 10)), cal={"A": 0.9}),
        rec("r2", 2, fnd("B", cit("src/a.py", 13)), cal={"B": 0.9}),
        rec("r3", 3, fnd("C", cit("src/a.py", 16)), cal={"C": 0.9}),
    ]
    raw = cl.cluster_v2(records, SNAP)
    assert raw["chained"] == ["C1"]
    kept = cl.clusters_kept(records, SNAP, [("r1", "A"), ("r3", "C")])
    assert ids(kept) == [[("r1", "A")], [("r3", "C")]]
    assert kept["chained"] == [] and kept["valid_blocks"] == 3
    # r2 keeps no finding, so w(r2) = 0: each support is 0.9 / (0.9 + 0 + 0.9) = 0.5
    assert [c["support"] for c in kept["clusters"]] == pytest.approx([0.5, 0.5])
    assert kept["uncalibrated"] == [] and kept["cluster_agreement"] == pytest.approx(
        0.5
    )
    nothing = cl.clusters_kept(records, SNAP, None)
    assert nothing["clusters"] == [] and nothing["cluster_agreement"] == 1.0
    assert any("nothing kept" in p["msg"] for p in nothing["problems"])


# ------------------------------------------------------------ v1 merge unaffected, names


_MERGE = """
import json, sys
if sys.argv[1] == "with":
    import superclaude.cli.review.cluster
from click.testing import CliRunner
from superclaude.cli.main import main
res = CliRunner().invoke(main, sys.argv[2:])
print(json.dumps({"exit": res.exit_code, "output": res.output,
                  "loaded": "superclaude.cli.review.cluster" in sys.modules}))
"""


def test_review_merge_v1_output_is_byte_identical_with_and_without_the_module(tmp_path):
    doc = tmp_path / "spec.md"
    doc.write_text(SEEDED)
    r1, r2 = tmp_path / "r1.md", tmp_path / "r2.md"
    r1.write_text(report(finding("F1", A_S1, ["FR-3"])))
    r2.write_text(report(finding("G1", A_S3, ["FR-4"])))
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    runs = {}
    for mode in ("without", "with"):
        d = tmp_path / mode
        d.mkdir()
        args = [
            "review", "merge",
            "--ledger", str(d / "ledger.json"),
            "--doc", str(doc),
            "--round", "1",
            "--report", f"t1b-1={r1}",
            "--report", f"t2-1={r2}",
            "--out", str(d / "merged.md"),
        ]  # fmt: skip
        proc = subprocess.run(
            [sys.executable, "-c", _MERGE, mode, *args],
            capture_output=True,
            text=True,
            env=env,
            check=True,
        )
        res = json.loads(proc.stdout.strip().splitlines()[-1])
        assert res["exit"] == 0, res["output"]
        assert res["loaded"] is (mode == "with")
        runs[mode] = (
            res["output"],
            (d / "ledger.json").read_bytes(),
            (d / "merged.md").read_bytes(),
        )
    assert runs["with"] == runs["without"]


def test_field_is_named_cluster_agreement_and_the_old_name_is_absent():
    old = "panel_" + "agreement_score"
    for path in (MODULE, Path(__file__)):
        assert old not in path.read_text(encoding="utf-8")
    out = cl.cluster_v2([], SNAP)
    assert "cluster_agreement" in out and old not in json.dumps(out)


def test_module_does_not_import_v1_cluster():
    tree = ast.parse(MODULE.read_text(encoding="utf-8"))
    imported = {
        alias.name
        for node in ast.walk(tree)
        if isinstance(node, ast.ImportFrom)
        and node.module
        and "findings" in node.module
        for alias in node.names
    }
    assert imported == {"refs_norm", "_check_citation"}
    assert "findings.cluster" not in MODULE.read_text(encoding="utf-8")
