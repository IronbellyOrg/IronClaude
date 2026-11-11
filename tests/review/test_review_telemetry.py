"""Review telemetry: record schema, append-only files, task variables, loader and views (PN1, C8)."""

from __future__ import annotations

import copy
import json
import sqlite3
from pathlib import Path

import pytest

from superclaude.cli.review import telemetry as tel

FIX = Path(__file__).parent / "fixtures"
CLEAN = (FIX / "clean.md").read_text()


def reviewer_record(**over):
    rec = {
        "schema_version": "review-telemetry/1",
        "kind": "reviewer_run",
        "record_id": "a" * 32,
        "ts_utc": "2026-11-10T12:00:00Z",
        "run_id": "b1-r1",
        "step": "R1",
        "round": 1,
        "reviewer_id": "t3-1",
        "panel": {
            "template_id": "default",
            "template_version": "1.0.0",
            "template_sha256": "x",
            "tiers_version": "1.0.0",
            "tiers_sha256": "y",
            "environment": "anthropic-only",
            "panel_size": 4,
        },
        "slot": {
            "slot_id": "t3",
            "tier": "tier3",
            "alias": "claude-gw-tier3[1m]",
            "strategy": "random",
            "seed": "1|t3|1",
            "fallback_depth": 0,
            "stand_in": True,
        },
        "model": {
            "resolved": "claude-haiku-5-5",
            "launch": "haiku",
            "observed": "claude-haiku-5-5",
        },
        "task": {
            "doc_sha256": "d",
            "doc_bytes": 10,
            "doc_lines": 2,
            "language": "en",
            "doc_format": "markdown",
            "specialization": "software-spec",
            "sections": 1,
            "max_heading_depth": 1,
            "tables": 0,
            "table_rows": 0,
            "ids_defined": 0,
            "cross_refs": 0,
            "rfc2119": 0,
            "review_kind": "first",
        },
        "output": {
            "block_ok": True,
            "findings": 2,
            "blocking": 1,
            "by_severity": {"CRITICAL": 1, "MAJOR": 0, "MINOR": 1},
            "verdict": "FAIL",
            "verdict_mismatch": False,
        },
        "cost": {
            "tokens_in": 1,
            "tokens_cache_read": 2,
            "tokens_cache_write": 3,
            "tokens_out": 100,
            "wall_s": 1.5,
        },
        "context": {"experiment": "pn1", "arm": "b1", "replicate": 1},
    }
    rec.update(over)
    return rec


def outcome_record(**over):
    rec = {
        "schema_version": "review-telemetry/1",
        "kind": "outcome",
        "record_id": "b" * 32,
        "ts_utc": "2026-11-10T13:00:00Z",
        "run_id": "b1-r1",
        "reviewer_record_id": "a" * 32,
        "truth_basis": "theme-v1",
        "confirmed_tp": 1,
        "false_pos": None,
        "unconfirmed": 0,
        "unique_tp": 1,
        "overlap_mean_jaccard": None,
        "recall_vs_confirmed": 0.5,
        "precision": None,
        "cost_per_confirmed_tp": 100.0,
        "supersedes": None,
    }
    rec.update(over)
    return rec


def test_valid_records_pass_and_each_missing_key_fails():
    assert tel.validate_record(reviewer_record()) == []
    assert tel.validate_record(outcome_record()) == []
    base = reviewer_record()
    for key in list(base):
        bad = copy.deepcopy(base)
        del bad[key]
        assert tel.validate_record(bad), key
    for group in ("panel", "slot", "model", "task", "output", "cost"):
        for key in list(base[group]):
            bad = copy.deepcopy(base)
            del bad[group][key]
            assert tel.validate_record(bad), (group, key)
    base_o = outcome_record()
    for key in list(base_o):
        bad = copy.deepcopy(base_o)
        del bad[key]
        assert tel.validate_record(bad), key
    assert tel.validate_record(reviewer_record(kind="other"))
    assert tel.validate_record(reviewer_record(run_id="bad run id"))
    assert tel.validate_record(outcome_record(truth_basis="vibes"))
    assert tel.validate_record(reviewer_record(schema_version="x"))


def test_append_is_append_only_and_routes_by_kind(tmp_path):
    r1 = reviewer_record()
    p1 = tel.append_record(tmp_path, r1)
    first = p1.read_bytes()
    r2 = reviewer_record(record_id="c" * 32, reviewer_id="t3-2")
    p2 = tel.append_record(tmp_path, r2)
    assert p1 == p2 and p1.name == "b1-r1.jsonl"
    assert p1.parent == tmp_path / "records" / "2026" / "11"
    assert p1.read_bytes().startswith(first)
    assert len(p1.read_text().splitlines()) == 2
    po = tel.append_record(tmp_path, outcome_record())
    assert po.name == "b1-r1.outcomes.jsonl" and po.parent == p1.parent
    # a later record with another month still lands next to the first one
    p3 = tel.append_record(
        tmp_path, reviewer_record(record_id="d" * 32, ts_utc="2026-12-01T00:00:00Z")
    )
    assert p3 == p1
    with pytest.raises(ValueError):
        tel.append_record(tmp_path, reviewer_record(kind="bogus"))


def test_no_document_text_in_any_record(tmp_path):
    task = tel.task_variables(CLEAN, "software-spec", "first")
    rec = reviewer_record(task={**reviewer_record()["task"], **task})
    path = tel.append_record(tmp_path, rec)
    blob = path.read_text()
    flat = " ".join(CLEAN.split())
    for i in range(0, len(flat) - 40, 7):
        assert flat[i : i + 40] not in blob


def test_task_variables_on_clean_fixture():
    t = tel.task_variables(CLEAN, "software-spec", "first")
    lines = CLEAN.splitlines()
    heads = [ln for ln in lines if ln.startswith("#")]
    assert t["sections"] == len(heads) == 6
    assert t["max_heading_depth"] == 2
    assert t["tables"] == 0 and t["table_rows"] == 0
    assert t["doc_bytes"] == len(CLEAN.encode()) == 2783
    assert t["doc_lines"] == 35
    assert t["language"] == "en" and t["doc_format"] == "markdown"
    assert t["specialization"] == "software-spec" and t["review_kind"] == "first"
    # FR-1 .. FR-8 are each defined once, as `- **FR-n` at a list-item start (hand count, read from the file),
    # and mentioned nowhere else; the file has no "section n" mention and no upper-case RFC 2119 word
    assert t["ids_defined"] == 8
    assert t["cross_refs"] == 0
    assert t["rfc2119"] == 0
    assert "section" not in CLEAN.lower()
    assert len(t["doc_sha256"]) == 64


def test_task_variables_tables_and_ids():
    doc = (
        "# T\n\n## 1 Reqs\n\n| ID | Text |\n|---|---|\n| FR-1 | The system MUST do a thing. |\n| FR-2 | See section 2.1 and FR-1. |\n\n"
        "**NFR-3** is a bold definition. It SHOULD hold, see AC-0.4.\n\n## 2.1 Sub\n\nPlain text and the P0 phase.\n"
    )
    t = tel.task_variables(doc)
    assert t["tables"] == 1 and t["table_rows"] == 2
    assert t["sections"] == 3 and t["max_heading_depth"] == 2
    assert t["ids_defined"] == 3  # FR-1, FR-2, NFR-3
    assert t["rfc2119"] == 2
    # id occurrences: FR-1, FR-2, FR-1, NFR-3, AC-0.4, P0 = 6, plus "section 2.1" = 7, minus 3 defining = 4
    assert t["cross_refs"] == 4
    assert t["specialization"] == "unspecified" and t["review_kind"] == "first"


def test_loader_is_idempotent_and_reports_bad_lines(tmp_path):
    d = tmp_path / "tel"
    tel.append_record(d, reviewer_record())
    tel.append_record(d, outcome_record())
    bad = next((d / "records").rglob("b1-r1.jsonl"))
    with open(bad, "a") as f:
        f.write("not json\n")
        f.write(json.dumps({"kind": "reviewer_run"}) + "\n")
    db = tmp_path / "t.sqlite"
    r1 = tel.load(d, db)
    assert r1["reviewer_runs"] == 1 and r1["outcomes"] == 1 and len(r1["invalid"]) == 2
    assert ":" in r1["invalid"][0]
    r2 = tel.load(d, db)
    assert r2["reviewer_runs"] == 0 and r2["outcomes"] == 0
    con = sqlite3.connect(db)
    row = con.execute(
        "select model_observed, slot_stand_in, task_doc_bytes, cost_tokens_out, output_by_severity_CRITICAL from reviewer_runs"
    ).fetchone()
    assert row == ("claude-haiku-5-5", 1, 10, 100, 1)
    assert con.execute("select count(*) from reviewer_runs").fetchone()[0] == 1


def test_model_scores_arithmetic_and_supersession(tmp_path):
    d = tmp_path / "tel"
    tel.append_record(d, reviewer_record(record_id="1" * 32))
    tel.append_record(d, reviewer_record(record_id="2" * 32, reviewer_id="t3-2"))
    s = reviewer_record(record_id="3" * 32, reviewer_id="t1b-1", run_id="b1-r1")
    s["slot"] = {**s["slot"], "slot_id": "t1b", "tier": "tier1b", "stand_in": False}
    s["model"] = {
        "resolved": "claude-sonnet-5-5",
        "launch": "sonnet",
        "observed": "claude-sonnet-5-5",
    }
    s["cost"] = {**s["cost"], "tokens_out": 300}
    tel.append_record(d, s)
    tel.append_record(
        d,
        outcome_record(
            record_id="o1" + "0" * 30,
            reviewer_record_id="1" * 32,
            confirmed_tp=2,
            false_pos=1,
            unique_tp=1,
            precision=2 / 3,
            recall_vs_confirmed=0.5,
        ),
    )
    tel.append_record(
        d,
        outcome_record(
            record_id="o2" + "0" * 30,
            reviewer_record_id="2" * 32,
            confirmed_tp=1,
            false_pos=0,
            unique_tp=0,
            precision=1.0,
            recall_vs_confirmed=0.25,
        ),
    )
    tel.append_record(
        d,
        outcome_record(
            record_id="o3" + "0" * 30,
            reviewer_record_id="3" * 32,
            confirmed_tp=3,
            false_pos=None,
            unique_tp=2,
            precision=None,
            recall_vs_confirmed=0.75,
        ),
    )
    db = tmp_path / "t.sqlite"
    tel.load(d, db)
    con = sqlite3.connect(db)
    con.row_factory = sqlite3.Row
    rows = {
        (r["model_observed"], r["slot_tier"], r["slot_stand_in"]): r
        for r in con.execute("select * from model_scores")
    }
    h = rows[("claude-haiku-5-5", "tier3", 1)]
    assert (
        h["n_runs"] == 2
        and h["sum_confirmed_tp"] == 3
        and h["sum_false_pos"] == 1
        and h["sum_unique_tp"] == 1
    )
    assert abs(h["mean_precision"] - (2 / 3 + 1.0) / 2) < 1e-9
    assert abs(h["mean_recall_vs_confirmed"] - 0.375) < 1e-9
    assert abs(h["cost_per_confirmed_tp"] - 200 / 3) < 1e-9
    so = rows[("claude-sonnet-5-5", "tier1b", 0)]
    assert (
        so["n_runs"] == 1
        and so["sum_confirmed_tp"] == 3
        and abs(so["cost_per_confirmed_tp"] - 100.0) < 1e-9
    )
    # a correction supersedes the first outcome of record 1: the old one leaves the view
    tel.append_record(
        d,
        outcome_record(
            record_id="o4" + "0" * 30,
            reviewer_record_id="1" * 32,
            confirmed_tp=5,
            false_pos=0,
            unique_tp=1,
            precision=1.0,
            recall_vs_confirmed=0.9,
            supersedes="o1" + "0" * 30,
            ts_utc="2026-11-10T14:00:00Z",
        ),
    )
    tel.load(d, db)
    con = sqlite3.connect(db)
    con.row_factory = sqlite3.Row
    h = next(
        r
        for r in con.execute("select * from model_scores")
        if r["model_observed"] == "claude-haiku-5-5"
    )
    assert h["sum_confirmed_tp"] == 6 and h["sum_false_pos"] == 0
    # nothing was removed from the table itself
    assert con.execute("select count(*) from outcomes").fetchone()[0] == 4


def test_stratum_tag_is_optional_validated_stored_and_never_pooled(tmp_path):
    assert tel.validate_record(reviewer_record(stratum="haiku")) == []
    assert tel.validate_record(outcome_record(stratum="sonnet")) == []
    assert tel.validate_record(reviewer_record(stratum="gpt"))
    d = tmp_path / "tel"
    tel.append_record(d, reviewer_record(record_id="1" * 32, stratum="sonnet"))
    tel.append_record(
        d, reviewer_record(record_id="2" * 32, reviewer_id="t3-2", stratum="haiku")
    )
    tel.append_record(
        d,
        outcome_record(
            record_id="o1" + "0" * 30,
            reviewer_record_id="1" * 32,
            confirmed_tp=1,
            stratum="sonnet",
        ),
    )
    tel.append_record(
        d,
        outcome_record(
            record_id="o2" + "0" * 30,
            reviewer_record_id="2" * 32,
            confirmed_tp=5,
            stratum="haiku",
        ),
    )
    db = tmp_path / "t.sqlite"
    tel.load(d, db)
    con = sqlite3.connect(db)
    rows = con.execute(
        "select stratum, n_runs, sum_confirmed_tp from model_scores order by stratum"
    ).fetchall()
    assert rows == [("haiku", 1, 5), ("sonnet", 1, 1)]
    assert con.execute(
        "select stratum from outcomes order by record_id"
    ).fetchall() == [("sonnet",), ("haiku",)]


def test_outcome_with_a_conflicting_stratum_is_excluded_and_counted(tmp_path):
    """Review finding (Augment): model_scores must never pool outcomes of another stratum."""
    d = tmp_path / "tel"
    tel.append_record(d, reviewer_record(record_id="1" * 32, stratum="sonnet"))
    tel.append_record(
        d,
        outcome_record(
            record_id="o1" + "0" * 30,
            reviewer_record_id="1" * 32,
            confirmed_tp=1,
            stratum="sonnet",
        ),
    )
    tel.append_record(  # tagged haiku, attached to a sonnet reviewer run
        d,
        outcome_record(
            record_id="o2" + "0" * 30,
            reviewer_record_id="1" * 32,
            confirmed_tp=5,
            stratum="haiku",
        ),
    )
    tel.append_record(  # untagged: inherits the reviewer run's stratum
        d,
        outcome_record(
            record_id="o3" + "0" * 30,
            reviewer_record_id="1" * 32,
            confirmed_tp=2,
        ),
    )
    db = tmp_path / "t.sqlite"
    counts = tel.load(d, db)
    assert counts["stratum_conflicts"] == 1
    con = sqlite3.connect(db)
    rows = con.execute(
        "select stratum, sum_confirmed_tp from model_scores order by stratum"
    ).fetchall()
    assert rows == [("sonnet", 3)]  # 1 + 2, never the haiku-tagged 5
