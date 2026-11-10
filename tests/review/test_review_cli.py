"""`superclaude review ...` command surface (PN1)."""

from __future__ import annotations

import json
from pathlib import Path

from click.testing import CliRunner

from superclaude.cli.main import main

FIX = Path(__file__).parent / "fixtures"
SEEDED = (FIX / "seeded.md").read_text()

A_S1 = "The worker retries a failed delivery up to 8 times with exponential backoff"
A_S3 = "logs the full request headers and the webhook's signing secret at INFO level"


def run(*args):
    return CliRunner().invoke(main, list(args))


def report(*findings):
    lines = [json.dumps(f) for f in findings]
    return (
        "review: 1 of 3\n\n## Findings block\n\n```findings-v1\n"
        + "\n".join(lines)
        + "\n```\n\nverdict: FAIL\n"
    )


def finding(fid, anchor, refs):
    return {
        "id": fid,
        "severity": "CRITICAL",
        "blocking": True,
        "category": "contradiction",
        "anchor": anchor,
        "refs": refs,
        "claim": "wrong",
    }


def test_review_help_lists_the_subcommands():
    res = run("review", "--help")
    assert res.exit_code == 0, res.output
    for name in ("panel", "merge", "ledger", "telemetry"):
        assert name in res.output
    assert "review" in run("--help").output


def test_panel_resolve_prints_json():
    res = run("review", "panel", "resolve", "--env", "anthropic-only", "--run-id", "x")
    assert res.exit_code == 0, res.output
    out = json.loads(res.output)
    assert [r["reviewer_id"] for r in out["reviewers"]] == [
        "t1b-1",
        "t2-1",
        "t3-1",
        "t3-2",
    ]
    assert out["reviewers"][0]["model"] == "claude-sonnet-5-5"
    rr = json.loads(
        run(
            "review",
            "panel",
            "resolve",
            "--env",
            "anthropic-only",
            "--run-id",
            "x",
            "--kind",
            "re-review",
        ).output
    )
    assert [r["reviewer_id"] for r in rr["reviewers"]] == ["t1b-1"]
    again = run(
        "review", "panel", "resolve", "--env", "anthropic-only", "--run-id", "x"
    )
    assert again.output == res.output


def test_panel_resolve_gateway_when_t3model01_is_set(monkeypatch):
    monkeypatch.setenv("T3Model01", "something")
    monkeypatch.delenv("SUPERCLAUDE_REVIEW_ENV", raising=False)
    res = run("review", "panel", "resolve", "--run-id", "x")
    assert res.exit_code == 0, res.output
    assert json.loads(res.output)["environment"] == "gateway"


def test_panel_resolve_unknown_environment_fails():
    res = run("review", "panel", "resolve", "--env", "nope", "--run-id", "x")
    assert res.exit_code != 0


def test_panel_validate_exit_codes(tmp_path):
    good = tmp_path / "good.json"
    good.write_text(
        json.dumps(
            {
                "schema": "review-panel/1",
                "template_id": "solo",
                "version": "1.0.0",
                "distinct_across_slots": False,
                "apply_to": ["first"],
                "slots": [
                    {"slot_id": "a", "tier": "tier1b", "count": 1, "strategy": "fixed"}
                ],
            }
        )
    )
    assert run("review", "panel", "validate", str(good)).exit_code == 0
    bad = tmp_path / "bad.json"
    bad.write_text(json.dumps({"schema": "review-panel/1"}))
    res = run("review", "panel", "validate", str(bad))
    assert res.exit_code == 1 and res.output.strip()
    assert (
        run("review", "panel", "validate", str(good), "--kind", "tiers").exit_code == 1
    )


def test_merge_revise_verdict_round_trip(tmp_path):
    doc = tmp_path / "spec.md"
    doc.write_text(SEEDED)
    r1 = tmp_path / "r1.md"
    r1.write_text(report(finding("F1", A_S1, ["FR-3"])))
    r2 = tmp_path / "r2.md"
    r2.write_text(report(finding("G1", A_S3, ["FR-4"])))
    ledger = tmp_path / "review" / "ledger.json"
    resolution = tmp_path / "panel.json"
    resolution.write_text(
        run(
            "review", "panel", "resolve", "--env", "anthropic-only", "--run-id", "x"
        ).output
    )
    out1 = tmp_path / "review" / "round1.md"
    res = run(
        "review",
        "merge",
        "--ledger",
        str(ledger),
        "--doc",
        str(doc),
        "--round",
        "1",
        "--report",
        f"t1b-1={r1}",
        "--report",
        f"t2-1={r2}",
        "--resolution",
        str(resolution),
        "--out",
        str(out1),
    )
    assert res.exit_code == 0, res.output
    summary = json.loads(res.output)
    assert (
        summary["verdict"] == "FAIL"
        and summary["decision"] == "REVISE"
        and summary["brief_ids"] == ["L1", "L2"]
    )
    assert summary["block_ok"] == {"t1b-1": True, "t2-1": True}
    assert out1.read_text().splitlines()[0] == "review: 1 of 3"
    assert "Blocking finding ids: L1, L2." in out1.read_text()
    assert (
        json.loads(ledger.read_text())["rounds"][0]["reviewers"][0]["model"]
        == "claude-sonnet-5-5"
    )

    v = run("review", "ledger", "verdict", "--ledger", str(ledger))
    assert v.exit_code == 10 and json.loads(v.output)["decision"] == "REVISE"

    new = tmp_path / "spec-new.md"
    new.write_text(
        SEEDED.replace(
            "up to 8 times with exponential backoff, doubling the delay after each attempt, and marks it `FAILED` after the ninth failed attempt",
            "at most 5 times",
        )
    )
    fixmap = tmp_path / "revise1.md"
    fixmap.write_text(
        '## Fix map\n\n```fixmap-v1\n{"id": "L1", "action": "applied", "reason": "r"}\n{"id": "L2", "action": "rejected", "reason": "no"}\n```\n'
    )
    res = run(
        "review",
        "ledger",
        "revise",
        "--ledger",
        str(ledger),
        "--old",
        str(doc),
        "--new",
        str(new),
        "--fixmap",
        str(fixmap),
    )
    assert res.exit_code == 0, res.output
    assert json.loads(res.output)["resolved_check"] == ["L1"]

    r3 = tmp_path / "r3.md"
    r3.write_text(report(finding("H1", A_S3, ["FR-4"])))
    out2 = tmp_path / "review" / "round2.md"
    res = run(
        "review",
        "merge",
        "--ledger",
        str(ledger),
        "--doc",
        str(new),
        "--round",
        "2",
        "--report",
        f"t1b-1={r3}",
        "--out",
        str(out2),
    )
    assert res.exit_code == 0, res.output
    assert json.loads(res.output)["cleared"] == ["L1"]
    assert out2.read_text().splitlines()[0] == "review: 2 of 3"

    cap = run("review", "ledger", "capture", "--ledger", str(ledger), "--round", "1")
    assert cap.exit_code == 0 and json.loads(cap.output)["schema"] == "review-capture/1"

    d = run(
        "review",
        "ledger",
        "defer",
        "--ledger",
        str(ledger),
        "--lid",
        "L2",
        "--reason",
        "accepted",
    )
    assert d.exit_code == 0, d.output
    v = run("review", "ledger", "verdict", "--ledger", str(ledger))
    assert (
        v.exit_code == 0 and json.loads(v.output)["decision"] == "PASS"
    )  # the only open row was deferred
    bad = run(
        "review",
        "ledger",
        "defer",
        "--ledger",
        str(ledger),
        "--lid",
        "L99",
        "--reason",
        "x",
    )
    assert bad.exit_code != 0


def test_verdict_exit_codes_pass_and_escalate(tmp_path):
    doc = tmp_path / "spec.md"
    doc.write_text(SEEDED)
    empty = tmp_path / "e.md"
    empty.write_text(report())
    ledger = tmp_path / "ledger.json"
    res = run(
        "review",
        "merge",
        "--ledger",
        str(ledger),
        "--doc",
        str(doc),
        "--round",
        "1",
        "--report",
        f"t1b-1={empty}",
        "--out",
        str(tmp_path / "m.md"),
    )
    assert res.exit_code == 0 and json.loads(res.output)["decision"] == "PASS"
    assert run("review", "ledger", "verdict", "--ledger", str(ledger)).exit_code == 0
    esc = tmp_path / "esc.json"
    for n in (1, 2, 3):
        f = tmp_path / f"f{n}.md"
        f.write_text(report(finding("F1", A_S3, ["FR-4"])))
        res = run(
            "review",
            "merge",
            "--ledger",
            str(esc),
            "--doc",
            str(doc),
            "--round",
            str(n),
            "--report",
            f"t1b-1={f}",
            "--out",
            str(tmp_path / f"m{n}.md"),
        )
        assert res.exit_code == 0, res.output
    assert run("review", "ledger", "verdict", "--ledger", str(esc)).exit_code == 11


def test_telemetry_commands(tmp_path):
    doc = tmp_path / "d.md"
    doc.write_text((FIX / "clean.md").read_text())
    res = run(
        "review", "telemetry", "taskvars", str(doc), "--specialization", "software-spec"
    )
    assert res.exit_code == 0, res.output
    tv = json.loads(res.output)
    assert (
        tv["sections"] == 6
        and tv["specialization"] == "software-spec"
        and tv["review_kind"] == "first"
    )
    rec = {
        "schema_version": "review-telemetry/1",
        "kind": "outcome",
        "record_id": "e" * 32,
        "ts_utc": "2026-11-10T13:00:00Z",
        "run_id": "r1",
        "reviewer_record_id": "a" * 32,
        "truth_basis": "theme-v1",
        "confirmed_tp": 0,
        "false_pos": None,
        "unconfirmed": 0,
        "unique_tp": 0,
        "overlap_mean_jaccard": None,
        "recall_vs_confirmed": None,
        "precision": None,
        "cost_per_confirmed_tp": None,
        "supersedes": None,
    }
    f = tmp_path / "rec.json"
    f.write_text(json.dumps(rec))
    d = tmp_path / "tel"
    assert (
        run(
            "review", "telemetry", "append", "--dir", str(d), "--record", str(f)
        ).exit_code
        == 0
    )
    assert (d / "records" / "2026" / "11" / "r1.outcomes.jsonl").is_file()
    f.write_text(json.dumps({"kind": "outcome"}))
    assert (
        run(
            "review", "telemetry", "append", "--dir", str(d), "--record", str(f)
        ).exit_code
        != 0
    )
    db = tmp_path / "x.sqlite"
    res = run("review", "telemetry", "load", "--dir", str(d), "--db", str(db))
    assert res.exit_code == 0 and db.is_file()
