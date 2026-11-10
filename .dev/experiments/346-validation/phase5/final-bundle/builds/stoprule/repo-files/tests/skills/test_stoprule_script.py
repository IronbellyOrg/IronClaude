"""Behaviour tests for stoprule.py, the computed stop rule of /sc:spec-panel-stoprule.

Enforcement type: EXECUTABLE (script behaviour). Pure functions are loaded by path with
importlib; exit codes are checked by running the script with sys.executable, the same way
test_issue_repo_resolution.py loads origin_repo.py. Every fixture lives in tmp_path.
"""

import hashlib
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest

_SKILL = (
    Path(__file__).resolve().parents[2]
    / "src/superclaude/skills/sc-spec-panel-stoprule-protocol"
)
_SCRIPT = _SKILL / "scripts/stoprule.py"
_spec = importlib.util.spec_from_file_location("stoprule", _SCRIPT)
sr = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(sr)

RUBRIC_TEXT = (_SKILL / "refs/rubric.md").read_text(encoding="utf-8")
OUTCOME = "An implementer following this sentence builds a kiosk that releases the locker twice and double charges the rider."


def run(*args, cwd=None):
    proc = subprocess.run(
        [sys.executable, str(_SCRIPT), *map(str, args)],
        capture_output=True,
        text=True,
        cwd=cwd,
    )
    return proc.returncode, proc.stdout + proc.stderr


def spec_lines(n=12, tag="v1"):
    return (
        "\n".join(
            f"Line {i}: the Pedalbay kiosk rule number {i} applies to every locker bay ({tag} text)."
            for i in range(1, n + 1)
        )
        + "\n"
    )


def sha12(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:12]


def claim(
    cid, quote, claimed="major", prior=None, outcome=OUTCOME, span=None, evidence=None
):
    return {
        "k": "claim",
        "id": cid,
        "claimed": claimed,
        "quote": quote,
        "span": span if span is not None else quote[:20],
        "outcome": outcome,
        "evidence": evidence or [],
        "prior": prior,
        "sites": [],
    }


def add_reviewer_lines(report, records):
    """Insert reviewer lines before the ledger's closing fence, as a reviewer would."""
    lines = report.read_text(encoding="utf-8").splitlines()
    a, b = sr.ledger_bounds(lines)
    lines[b:b] = [json.dumps(r) for r in records]
    report.write_text("\n".join(lines) + "\n", encoding="utf-8")


def replace_reviewer_lines(report, records):
    """Drop every claim/prior/checked line and write the given ones (a reviewer repair)."""
    lines = report.read_text(encoding="utf-8").splitlines()
    a, b = sr.ledger_bounds(lines)
    kept = [
        x
        for x in lines[a + 1 : b]
        if not x.strip() or json.loads(x)["k"] not in sr.REVIEWER_KINDS
    ]
    lines[a + 1 : b] = kept + [json.dumps(r) for r in records]
    report.write_text("\n".join(lines) + "\n", encoding="utf-8")


def records_of(report, kind):
    return [
        r for r in sr.load_ledger(report.read_text(encoding="utf-8")) if r["k"] == kind
    ]


def prior_report(
    tmp_path,
    spec_text,
    review=2,
    verdict="FAIL",
    rubric_text=RUBRIC_TEXT,
    finals=(),
    name="prior.md",
):
    """A prior report with a sentinel and coherent ledger (begin, claim, mark, grade, seal, final, verdict).

    finals: (id, status, quote, outcome) tuples; status 'confirmed' gives a FAIL ledger.
    """
    recs = [
        {
            "k": "begin",
            "v": 1,
            "review": review,
            "cap": 3,
            "nonce": "0" * 16,
            "spec_sha": hashlib.sha256(spec_text.encode()).hexdigest(),
            "spec_bytes": len(spec_text.encode()),
            "baseline_sha": None,
            "rubric_sha": hashlib.sha256(rubric_text.encode()).hexdigest(),
            "rubric1": hashlib.sha256(rubric_text.encode()).hexdigest(),
            "ratchet": "off",
            "changed": [],
            "hunks": [],
            "priors": {},
            "history": [],
        }
    ]
    for cid, status, quote, outcome in finals:
        recs.append(claim(cid, quote, outcome=outcome))
    for cid, status, quote, outcome in finals:
        recs.append(
            {
                "k": "mark",
                "id": cid,
                "form_ok": True,
                "issues": [],
                "late": False,
                "anchor": "off",
                "quote_lines": [1],
                "verified": [],
                "oh": sr.sha256_text(sr.norm(outcome)),
                "qh": sr.sha256_text(sr.norm(quote)),
            }
        )
    recs.append({"k": "seal", "sha256": "", "final_pass": 1})
    for cid, status, quote, outcome in finals:
        recs.append(
            {
                "k": "grade",
                "id": cid,
                "blocking": status == "confirmed",
                "q2": "na",
                "why": "fixture grade",
                "batch": "B1",
            }
        )
    for cid, status, quote, outcome in finals:
        recs.append(
            {
                "k": "final",
                "id": cid,
                "status": status,
                "oh": sr.sha256_text(sr.norm(outcome)),
                "qh": sr.sha256_text(sr.norm(quote)),
                "quote": quote,
                "outcome": outcome,
                "sites": [],
                "first": review,
                "trail": [f"r{review} open"],
            }
        )
    body = [
        "# prior review",
        "",
        sr.FENCE_OPEN,
        *[json.dumps(r) for r in recs],
        sr.FENCE_CLOSE,
        "",
    ]
    if verdict == "FAIL" and review >= 3:
        body += [
            "## Escalation to the user",
            "ESCALATION: spec-panel-stoprule review 3 of 3, verdict FAIL",
            "",
        ]
    body += [
        f"<!-- stoprule v1 review={review}/3 spec={sha12(spec_text)} rubric={sha12(rubric_text)} confirmed=1 late=0 minor=0 unconfirmed=0 reason=confirmed pre_audit=na brief=FAIL grader_model=sonnet ratchet=off ledger=000000000000 -->",
        f"verdict: {verdict}",
    ]
    path = tmp_path / name
    path.write_text("\n".join(body) + "\n", encoding="utf-8")
    return path


@pytest.fixture
def review1(tmp_path):
    """A begun review-1 report on a 12-line spec."""
    spec = tmp_path / "spec.md"
    spec.write_text(spec_lines(), encoding="utf-8")
    report = tmp_path / "report.md"
    code, out = run("begin", "--report", report, "--spec", spec)
    assert code == 0, out
    return spec, report


@pytest.fixture
def review2(tmp_path):
    """A begun review-2 report: lines 3 and 9 of the spec changed against the baseline."""
    base_text = spec_lines()
    base = tmp_path / "baseline.md"
    base.write_text(base_text, encoding="utf-8")
    new = base_text.splitlines()
    new[2] = (
        "Line 3: the Pedalbay kiosk now releases a locker only after the rider scans out (fixed text)."
    )
    new[8] = (
        "Line 9: refunds are paid to the original card within two days of the dispute (fixed text)."
    )
    spec = tmp_path / "spec.md"
    spec.write_text("\n".join(new) + "\n", encoding="utf-8")
    prior_quote = "Line 3: the Pedalbay kiosk rule number 3 applies to every locker bay"
    prior = prior_report(
        tmp_path,
        base_text,
        review=1,
        finals=[("R1-1", "confirmed", prior_quote, OUTCOME)],
    )
    report = tmp_path / "report.md"
    code, out = run(
        "begin",
        "--report",
        report,
        "--spec",
        spec,
        "--re-review",
        prior,
        "--baseline",
        base,
    )
    assert code == 0, out
    return spec, report, prior_quote


# --- pure functions --------------------------------------------------------------------


def test_norm_drops_backticks_bold_and_collapses_whitespace():
    assert sr.norm("a  `b`\n\n **c**  ") == "a b c"


def test_changed_lines_ignores_whitespace_only_changes():
    base = "alpha one\nbeta two\ngamma three\n"
    changed, hunks = sr.changed_lines(base, "alpha   one\nbeta two\ngamma three\n")
    assert changed == set() and hunks == []


def test_changed_lines_marks_lines_around_a_pure_deletion():
    base = "l1\nl2\nl3\nl4\n"
    changed, hunks = sr.changed_lines(base, "l1\nl2\nl4\n")
    assert changed == {2, 3}
    assert hunks[0]["base"] == "l3"


def test_load_ledger_reads_the_fenced_json_lines():
    text = 'intro\n```stoprule-ledger\n{"k":"begin"}\n\n{"k":"claim","id":"R1-1"}\n```\nprose\n'
    assert [r["k"] for r in sr.load_ledger(text)] == ["begin", "claim"]


# --- begin -----------------------------------------------------------------------------


def test_begin_review1_opens_ledger_with_nonce_and_prints_rubric(review1):
    spec, report = review1
    begin = records_of(report, "begin")[0]
    assert (
        begin["review"] == 1 and begin["ratchet"] == "off" and len(begin["nonce"]) == 16
    )
    int(begin["nonce"], 16)


def test_begin_exits_4_on_prior_review3_fail(tmp_path):
    spec_text = spec_lines()
    spec = tmp_path / "spec.md"
    spec.write_text(spec_text, encoding="utf-8")
    prior = prior_report(
        tmp_path,
        spec_text,
        review=3,
        verdict="FAIL",
        finals=[
            ("R3-1", "confirmed", "Line 2: the Pedalbay kiosk rule number 2", OUTCOME)
        ],
    )
    code, out = run(
        "begin",
        "--report",
        tmp_path / "r4.md",
        "--spec",
        spec,
        "--re-review",
        prior,
        "--baseline",
        spec,
    )
    assert code == 4
    assert "ESCALATION: spec-panel-stoprule review 3 of 3, verdict FAIL" in out
    assert not (tmp_path / "r4.md").exists()


def test_begin_exits_4_with_loop_ended_on_prior_review3_pass(tmp_path):
    spec_text = spec_lines()
    spec = tmp_path / "spec.md"
    spec.write_text(spec_text, encoding="utf-8")
    prior = prior_report(tmp_path, spec_text, review=3, verdict="PASS")
    code, out = run(
        "begin",
        "--report",
        tmp_path / "r4.md",
        "--spec",
        spec,
        "--re-review",
        prior,
        "--baseline",
        spec,
    )
    assert code == 4 and "loop already ended" in out


def test_begin_exits_5_on_rubric_drift(tmp_path):
    spec_text = spec_lines()
    spec = tmp_path / "spec.md"
    spec.write_text(spec_text, encoding="utf-8")
    prior = prior_report(tmp_path, spec_text, review=1)
    drifted = tmp_path / "rubric.md"
    drifted.write_text(RUBRIC_TEXT + "B4 extra rule\n", encoding="utf-8")
    code, out = run(
        "--rubric",
        drifted,
        "begin",
        "--report",
        tmp_path / "r.md",
        "--spec",
        spec,
        "--re-review",
        prior,
        "--baseline",
        spec,
    )
    assert code == 5 and "rubric" in out


def test_begin_exits_5_on_baseline_hash_mismatch(tmp_path):
    spec_text = spec_lines()
    spec = tmp_path / "spec.md"
    spec.write_text(spec_text, encoding="utf-8")
    prior = prior_report(tmp_path, spec_text, review=1)
    other = tmp_path / "other.md"
    other.write_text(spec_lines(tag="other"), encoding="utf-8")
    code, out = run(
        "begin",
        "--report",
        tmp_path / "r.md",
        "--spec",
        spec,
        "--re-review",
        prior,
        "--baseline",
        other,
    )
    assert code == 5 and "baseline" in out


def test_begin_exits_5_on_re_review_report_without_sentinel(tmp_path):
    spec = tmp_path / "spec.md"
    spec.write_text(spec_lines(), encoding="utf-8")
    prior = tmp_path / "plain.md"
    prior.write_text("# a plain spec-panel report\n\nverdict: FAIL\n", encoding="utf-8")
    code, out = run(
        "begin",
        "--report",
        tmp_path / "r.md",
        "--spec",
        spec,
        "--re-review",
        prior,
        "--baseline",
        spec,
    )
    assert code == 5 and "sentinel" in out


def test_begin_derives_review_number_from_prior_sentinel(review2):
    spec, report, _ = review2
    begin = records_of(report, "begin")[0]
    assert begin["review"] == 2 and begin["ratchet"] == "on"
    assert begin["changed"] == [3, 9]
    assert "R1-1" in begin["priors"]


# --- seal ------------------------------------------------------------------------------


def test_non_verbatim_quote_exits_3_then_ends_minor_form(review1):
    spec, report = review1
    add_reviewer_lines(
        report, [claim("R1-1", "Line 2: the Pedalbay kiosk rule number two applies")]
    )
    code, out = run("seal", "--report", report, "--spec", spec)
    assert code == 3 and "quote-not-found" in out
    code, out = run("seal", "--report", report, "--spec", spec)
    assert code == 0, out
    mark = records_of(report, "mark")[0]
    assert mark["form_ok"] is False and "quote-not-found" in mark["issues"]
    assert records_of(report, "seal")


def test_non_unique_quote_exits_3(review1):
    spec, report = review1
    add_reviewer_lines(report, [claim("R1-1", "the Pedalbay kiosk rule number")])
    code, out = run("seal", "--report", report, "--spec", spec)
    assert code == 3 and "quote-not-unique" in out


def test_short_quote_fails(review1):
    spec, report = review1
    add_reviewer_lines(report, [claim("R1-1", "Line 4: the", span="Line 4")])
    code, out = run("seal", "--report", report, "--spec", spec)
    assert code == 3 and "quote-too-short" in out


def test_short_outcome_fails(review1):
    spec, report = review1
    add_reviewer_lines(
        report,
        [
            claim(
                "R1-1",
                "Line 4: the Pedalbay kiosk rule number 4",
                outcome="this is wrong",
            )
        ],
    )
    code, out = run("seal", "--report", report, "--spec", spec)
    assert code == 3 and "outcome-too-short" in out


def test_valid_claim_seals_first_time_with_ratchet_off(review1):
    spec, report = review1
    add_reviewer_lines(
        report, [claim("R1-1", "Line 4: the Pedalbay kiosk rule number 4 applies")]
    )
    code, out = run("seal", "--report", report, "--spec", spec)
    assert code == 0, out
    mark = records_of(report, "mark")[0]
    assert (
        mark["form_ok"]
        and not mark["late"]
        and mark["anchor"] == "off"
        and mark["quote_lines"] == [4]
    )
    seal = records_of(report, "seal")[0]
    assert seal["sha256"] == sr.reviewer_hash(sr.load_ledger(report.read_text()))


def test_quote_outside_changed_lines_without_prior_is_late_found(review2):
    spec, report, _ = review2
    add_reviewer_lines(
        report,
        [
            claim("R2-1", "Line 5: the Pedalbay kiosk rule number 5 applies"),
            claim("R2-2", "now releases a locker only after the rider scans out"),
            {"k": "checked", "lines": "9"},
            {
                "k": "prior",
                "id": "R1-1",
                "status": "resolved",
                "resolved_by": "now releases a locker only after the rider scans out",
            },
        ],
    )
    code, out = run("seal", "--report", report, "--spec", spec)
    assert code == 0, out
    marks = {m["id"]: m for m in records_of(report, "mark")}
    assert marks["R2-1"]["late"] is True and marks["R2-1"]["anchor"] == "none"
    assert marks["R2-2"]["late"] is False and marks["R2-2"]["anchor"] == "changed"


def test_valid_and_invalid_prior_links(tmp_path):
    base_text = spec_lines()
    base = tmp_path / "baseline.md"
    base.write_text(base_text, encoding="utf-8")
    new = base_text.splitlines()
    new[8] = (
        "Line 9: refunds are paid to the original card within two days of the dispute (fixed text)."
    )
    spec = tmp_path / "spec.md"
    spec.write_text("\n".join(new) + "\n", encoding="utf-8")
    prior_quote = "Line 5: the Pedalbay kiosk rule number 5 applies"
    prior = prior_report(
        tmp_path,
        base_text,
        review=1,
        finals=[("R1-1", "confirmed", prior_quote, OUTCOME)],
    )
    report = tmp_path / "report.md"
    assert (
        run(
            "begin",
            "--report",
            report,
            "--spec",
            spec,
            "--re-review",
            prior,
            "--baseline",
            base,
        )[0]
        == 0
    )
    add_reviewer_lines(
        report,
        [
            claim(
                "R2-1", prior_quote, prior="R1-1"
            ),  # same quote and outcome hash: valid link
            claim(
                "R2-2", "Line 6: the Pedalbay kiosk rule number 6 applies", prior="R1-1"
            ),  # quote changed, unchanged line: invalid
            claim(
                "R2-3", "Line 7: the Pedalbay kiosk rule number 7 applies", prior="R9-9"
            ),  # unknown id: invalid
            {"k": "checked", "lines": "9"},
        ],
    )
    code, out = run("seal", "--report", report, "--spec", spec)
    assert code == 0, out
    marks = {m["id"]: m for m in records_of(report, "mark")}
    assert marks["R2-1"]["anchor"] == "prior" and marks["R2-1"]["late"] is False
    assert marks["R2-2"]["late"] is True and marks["R2-3"]["late"] is True


def test_uncovered_hunk_is_recorded_as_uncovered(review2):
    spec, report, _ = review2
    add_reviewer_lines(
        report, [claim("R2-1", "now releases a locker only after the rider scans out")]
    )
    code, out = run("seal", "--report", report, "--spec", spec)
    assert code == 3 and "uncovered-hunk" in out
    code, out = run("seal", "--report", report, "--spec", spec)
    assert code == 0, out
    assert [u["hunk"] for u in records_of(report, "uncovered")] == [[9, 9]]


def test_claim_dropped_between_seals_keeps_its_form_line(review1):
    spec, report = review1
    add_reviewer_lines(
        report,
        [
            claim(
                "R1-1",
                "Line 2: the Pedalbay kiosk rule number two applies",
                claimed="major",
                prior="N7",
            ),
            claim(
                "R1-2",
                "Line 4: the Pedalbay kiosk rule number 4 applies",
                claimed="critical",
            ),
        ],
    )
    assert run("seal", "--report", report, "--spec", spec)[0] == 3
    replace_reviewer_lines(
        report,
        [
            claim(
                "R1-2",
                "Line 4: the Pedalbay kiosk rule number 4 applies",
                claimed="critical",
            )
        ],
    )
    code, out = run("seal", "--report", report, "--spec", spec)
    assert code == 0, out
    forms = {f["id"]: f for f in records_of(report, "form") if "id" in f}
    assert forms["R1-1"]["claimed"] == "major" and forms["R1-1"]["prior"] == "N7"
    assert [m["id"] for m in records_of(report, "mark")] == ["R1-2"]


def test_evidence_path_with_dotdot_is_refused(review1, tmp_path):
    spec, report = review1
    (tmp_path / "secret.txt").write_text("Line 1 secret\n", encoding="utf-8")
    ev = [{"path": "../secret.txt", "line": 1, "text": "Line 1 secret"}]
    add_reviewer_lines(
        report,
        [
            claim(
                "R1-1", "Line 4: the Pedalbay kiosk rule number 4 applies", evidence=ev
            )
        ],
    )
    code, out = run(
        "--root", tmp_path / "sub", "seal", "--report", report, "--spec", spec
    )
    assert code == 3 and "evidence-path-refused" in out


def test_evidence_is_read_back_and_live_entries_are_unverified(review1, tmp_path):
    spec, report = review1
    (tmp_path / "notes.md").write_text(
        "a\nb\nthe retry limit is five\nc\n", encoding="utf-8"
    )
    ev = [
        {"path": "notes.md", "line": 2, "text": "the retry limit is five"},
        {"live": "wc -l notes.md", "saw": "4"},
    ]
    add_reviewer_lines(
        report,
        [
            claim(
                "R1-1", "Line 4: the Pedalbay kiosk rule number 4 applies", evidence=ev
            )
        ],
    )
    code, out = run("--root", tmp_path, "seal", "--report", report, "--spec", spec)
    assert code == 0, out
    assert records_of(report, "mark")[0]["verified"] == [True, False]


def test_seal_refuses_a_second_seal(review1):
    spec, report = review1
    add_reviewer_lines(
        report, [claim("R1-1", "Line 4: the Pedalbay kiosk rule number 4 applies")]
    )
    assert run("seal", "--report", report, "--spec", spec)[0] == 0
    assert run("seal", "--report", report, "--spec", spec)[0] == 5


# --- Task 4: grade-prep, apply-grades, audit-prep, apply-audit --------------------------

CANARIES = _SKILL / "refs/canaries.json"


def many_claims(n, prefix="R1"):
    return [
        claim(
            f"{prefix}-{i}",
            f"Line {i}: the Pedalbay kiosk rule number {i} applies",
            claimed="major" if i % 2 else "critical",
        )
        for i in range(1, n + 1)
    ]


def sealed(report, spec, claims, *extra):
    """Add the claims and seal; a repairable first seal is followed by the final one."""
    add_reviewer_lines(report, claims)
    code, out = run(*extra, "seal", "--report", report, "--spec", spec)
    if code == 3:
        code, out = run(*extra, "seal", "--report", report, "--spec", spec)
    assert code == 0, out
    return sr.load_ledger(report.read_text(encoding="utf-8"))


def reply_for(
    batch, blocking=True, wrong_canary=False, why="the quote and outcome meet B1 to B3"
):
    lines = []
    for cid, item in batch["map"].items():
        value = item["answer"] if "canary" in item else blocking
        if wrong_canary and "canary" in item:
            value = not value
        lines.append(
            json.dumps({"cid": cid, "blocking": value, "q2": "na", "why": why})
        )
    return "\n".join(lines) + "\n"


def apply(report, tmp_path, batch, text, *extra):
    path = (
        tmp_path / f"reply-{batch['batch']}-{len(list(tmp_path.glob('reply-*')))}.txt"
    )
    path.write_text(text, encoding="utf-8")
    return run(
        "apply-grades",
        "--report",
        report,
        "--batch",
        batch["batch"],
        "--reply",
        path,
        *extra,
    )


def test_batches_hold_at_most_6_claims_and_exactly_2_canaries(tmp_path):
    spec = tmp_path / "spec.md"
    spec.write_text(spec_lines(14), encoding="utf-8")
    report = tmp_path / "report.md"
    assert run("begin", "--report", report, "--spec", spec)[0] == 0
    records = sealed(report, spec, many_claims(14))
    batches = sr.build_batches(records, CANARIES)
    assert [sum("claim" in i for i in b["map"].values()) for b in batches] == [6, 6, 2]
    for b in batches:
        canaries = [i for i in b["map"].values() if "canary" in i]
        assert sorted(c["answer"] for c in canaries) == [False, True]
    assert sorted(
        i["claim"] for b in batches for i in b["map"].values() if "claim" in i
    ) == sorted(f"R1-{i}" for i in range(1, 15))


def test_printed_batch_has_no_label_spec_path_or_claimed_key(review1):
    spec, report = review1
    ev = [
        {
            "path": "spec.md",
            "line": 4,
            "text": "Line 4: the Pedalbay kiosk rule number 4",
        }
    ]
    root = ("--root", spec.parent)
    sealed(
        report,
        spec,
        [
            claim(
                "R1-1",
                "Line 4: the Pedalbay kiosk rule number 4 applies",
                claimed="critical",
                evidence=ev,
            ),
            claim(
                "R1-2",
                "Line 6: the Pedalbay kiosk rule number 6 applies",
                claimed="major",
            ),
        ],
        *root,
    )
    assert records_of(report, "mark")[0]["verified"] == [True]
    code, out = run(*root, "grade-prep", "--report", report)
    assert code == 0, out
    assert "the spec under review, line 4" in out
    assert "claimed" not in out and str(spec) not in out and "spec.md" not in out
    assert "critical" not in out and "major" not in out
    assert "R1-1" not in out and "R1-2" not in out
    assert "RUBRIC v1 (frozen" in out and "C1" in out


def test_same_seed_gives_same_batch_order(review1):
    spec, report = review1
    records = sealed(report, spec, many_claims(9))
    assert sr.build_batches(records, CANARIES) == sr.build_batches(records, CANARIES)
    assert (
        run("grade-prep", "--report", report)[1]
        == run("grade-prep", "--report", report)[1]
    )


def test_frozen_prior_is_never_batched(review2):
    spec, report, prior_quote = review2
    records = sealed(
        report,
        spec,
        [
            claim("R2-1", "now releases a locker only after the rider scans out"),
            {"k": "checked", "lines": "9"},
            {"k": "prior", "id": "R1-1", "status": "open", "resolved_by": None},
        ],
    )
    batched = [
        i["claim"]
        for b in sr.build_batches(records, CANARIES)
        for i in b["map"].values()
        if "claim" in i
    ]
    assert batched == ["R2-1"]
    assert sr.frozen_priors(records) == {"R1-1": "unresolved-prior"}
    out = run("grade-prep", "--report", report)[1]
    assert "R1-1" not in out and out.count("\n=== BATCH B") == 1
    # 1 claim + 2 canaries; the prior's quote appears only as R2-1's baseline hunk text
    assert out.count("\nquote: ") == 3 and f"quote: {prior_quote}" not in out


def test_good_reply_confirms_and_minor_grades(review1, tmp_path):
    spec, report = review1
    records = sealed(report, spec, many_claims(2))
    batch = sr.build_batches(records, CANARIES)[0]
    code, out = apply(report, tmp_path, batch, reply_for(batch, blocking=True))
    assert code == 0, out
    statuses = sr.claim_statuses(sr.load_ledger(report.read_text()))
    assert {s["status"] for s in statuses.values()} == {"confirmed"}
    raw = records_of(report, "grade-raw")[0]
    assert raw["sha256"] == sr.sha256_text(raw["text"])


def test_bad_grader_reply_and_wrong_canary_are_rejected(review1, tmp_path):
    spec, report = review1
    records = sealed(report, spec, many_claims(2))
    batch = sr.build_batches(records, CANARIES)[0]
    code, out = apply(report, tmp_path, batch, "the claims look fine to me\n")
    assert code == 3 and "rejected" in out
    code, out = apply(report, tmp_path, batch, reply_for(batch, wrong_canary=True))
    assert code == 0 and "rejected twice" in out
    rejects = records_of(report, "grade-reject")
    assert (
        "not a JSON line" in rejects[0]["reason"]
        and "wrong canary" in rejects[1]["reason"]
    )


def test_over_25_word_why_is_rejected(review1, tmp_path):
    spec, report = review1
    records = sealed(report, spec, many_claims(1))
    batch = sr.build_batches(records, CANARIES)[0]
    code, out = apply(
        report, tmp_path, batch, reply_for(batch, why=" ".join(["word"] * 26))
    )
    assert code == 3 and "25 words" in out


def test_two_bad_replies_leave_claims_unconfirmed(review1, tmp_path):
    spec, report = review1
    records = sealed(report, spec, many_claims(3))
    batch = sr.build_batches(records, CANARIES)[0]
    assert apply(report, tmp_path, batch, "{}\n")[0] == 3
    assert apply(report, tmp_path, batch, "{}\n")[0] == 0
    statuses = sr.claim_statuses(sr.load_ledger(report.read_text()))
    assert {s["status"] for s in statuses.values()} == {"unconfirmed"}
    assert (
        run("grade-prep", "--report", report)[1].strip()
        == "grade-prep: nothing to grade"
    )


def test_late_found_claim_graded_blocking_stays_late_found(review2, tmp_path):
    spec, report, _ = review2
    records = sealed(
        report,
        spec,
        [
            claim(
                "R2-1",
                "Line 5: the Pedalbay kiosk rule number 5 applies",
                claimed="critical",
            ),
            claim("R2-2", "now releases a locker only after the rider scans out"),
            {"k": "checked", "lines": "9"},
            {
                "k": "prior",
                "id": "R1-1",
                "status": "resolved",
                "resolved_by": "now releases a locker",
            },
        ],
    )
    batch = sr.build_batches(records, CANARIES)[0]
    assert apply(report, tmp_path, batch, reply_for(batch, blocking=True))[0] == 0
    statuses = sr.claim_statuses(sr.load_ledger(report.read_text()))
    assert statuses["R2-1"] == {"status": "late-found", "late_grade": True, "q2": "na"}
    assert statuses["R2-2"]["status"] == "confirmed"


def test_audit_real_true_turns_a_claim_into_confirmed_audit(review1, tmp_path):
    spec, report = review1
    records = sealed(
        report,
        spec,
        many_claims(2) + [claim("R1-9", "Line 9: the Pedalbay kiosk rule number nine")],
    )
    batch = sr.build_batches(records, CANARIES)[0]
    assert apply(report, tmp_path, batch, reply_for(batch, blocking=False))[0] == 0
    code, out = run("audit-prep", "--report", report, "--spec", spec)
    assert code == 0, out
    assert "=== AUDIT ===" in out and "1: Line 1:" in out
    items = sr.audit_items(sr.load_ledger(report.read_text()))
    assert sorted(i.get("id") for i in items.values() if "id" in i) == [
        "R1-1",
        "R1-2",
        "R1-9",
    ]
    assert sum("hunk" in i for i in items.values()) == 2
    reply = tmp_path / "audit.txt"
    reply.write_text(
        "\n".join(
            json.dumps({"aid": a, "real": items[a].get("id") == "R1-2", "why": "audit"})
            for a in items
        )
        + "\n"
    )
    code, out = run("apply-audit", "--report", report, "--reply", reply)
    assert code == 0, out
    statuses = sr.claim_statuses(sr.load_ledger(report.read_text()))
    assert statuses["R1-2"]["status"] == "confirmed-audit"
    assert (
        statuses["R1-1"]["status"] == "minor"
        and statuses["R1-9"]["status"] == "minor-form"
    )


def test_audit_prep_refuses_when_a_claim_is_confirmed(review1, tmp_path):
    spec, report = review1
    records = sealed(report, spec, many_claims(1))
    batch = sr.build_batches(records, CANARIES)[0]
    assert apply(report, tmp_path, batch, reply_for(batch, blocking=True))[0] == 0
    code, out = run("audit-prep", "--report", report, "--spec", spec)
    assert code == 5 and "confirmed" in out


def test_missing_auditor_reply_is_recorded_invalid(review1, tmp_path):
    spec, report = review1
    records = sealed(report, spec, many_claims(1))
    batch = sr.build_batches(records, CANARIES)[0]
    assert apply(report, tmp_path, batch, reply_for(batch, blocking=False))[0] == 0
    code, out = run("apply-audit", "--report", report)
    assert code == 0 and "invalid" in out
    assert records_of(report, "audit-raw")[0]["valid"] is False


# --- owner ruling: --dry-run writes nothing ----------------------------------------------


def snapshot(folder):
    return {p: p.read_bytes() for p in sorted(folder.rglob("*")) if p.is_file()}


def test_dry_run_writes_nothing_for_every_writing_subcommand(tmp_path):
    spec = tmp_path / "spec.md"
    spec.write_text(spec_lines(), encoding="utf-8")
    report = tmp_path / "report.md"
    before = snapshot(tmp_path)
    code, out = run("begin", "--report", report, "--spec", spec, "--dry-run")
    assert code == 0 and "nothing written" in out and snapshot(tmp_path) == before
    assert run("begin", "--report", report, "--spec", spec)[0] == 0
    add_reviewer_lines(
        report,
        [
            claim("R1-1", "Line 2: the Pedalbay kiosk rule number two applies"),
            claim("R1-2", "Line 4: the Pedalbay kiosk rule number 4 applies"),
        ],
    )
    before = snapshot(tmp_path)
    code, out = run("seal", "--report", report, "--spec", spec, "--dry-run")
    assert code == 3 and "quote-not-found" in out and snapshot(tmp_path) == before
    assert run("seal", "--report", report, "--spec", spec)[0] == 3
    assert run("seal", "--report", report, "--spec", spec)[0] == 0
    records = sr.load_ledger(report.read_text())
    batch = sr.build_batches(records, CANARIES)[0]
    good = tmp_path / "good.txt"
    good.write_text(reply_for(batch, blocking=False), encoding="utf-8")
    before = snapshot(tmp_path)
    code, out = run(
        "apply-grades",
        "--report",
        report,
        "--batch",
        batch["batch"],
        "--reply",
        good,
        "--dry-run",
    )
    assert code == 0 and "nothing written" in out and snapshot(tmp_path) == before
    assert (
        run(
            "apply-grades",
            "--report",
            report,
            "--batch",
            batch["batch"],
            "--reply",
            good,
        )[0]
        == 0
    )
    items = sr.audit_items(sr.load_ledger(report.read_text()))
    audit = tmp_path / "audit.txt"
    audit.write_text(
        "\n".join(json.dumps({"aid": a, "real": False, "why": "no"}) for a in items)
        + "\n"
    )
    before = snapshot(tmp_path)
    code, out = run("apply-audit", "--report", report, "--reply", audit, "--dry-run")
    assert code == 0 and "nothing written" in out and snapshot(tmp_path) == before
    for sub in (
        ("grade-prep", "--report", report),
        ("audit-prep", "--report", report, "--spec", spec),
    ):
        before = snapshot(tmp_path)
        assert run(*sub, "--dry-run")[0] == 0 and snapshot(tmp_path) == before


def test_usage_error_exits_5():
    assert run("begin")[0] == 5


def test_audit_real_true_on_an_unclaimed_hunk_is_a_confirmed_audit_defect(
    review1, tmp_path
):
    spec, report = review1
    records = sealed(report, spec, many_claims(1))
    batch = sr.build_batches(records, CANARIES)[0]
    assert apply(report, tmp_path, batch, reply_for(batch, blocking=False))[0] == 0
    items = sr.audit_items(sr.load_ledger(report.read_text()))
    reply = tmp_path / "audit.txt"
    reply.write_text(
        "\n".join(
            json.dumps({"aid": a, "real": a == "H1", "why": "audit"}) for a in items
        )
        + "\n"
    )
    code, out = run("apply-audit", "--report", report, "--reply", reply)
    assert code == 0, out
    assert "claims reinstated as confirmed-audit: none" in out
    assert "unclaimed hunks judged real (confirmed-audit defects): H1 (lines" in out
    records = sr.load_ledger(report.read_text())
    assert [a["hunk"] for a in sr.audit_hunks_real(records)] == [items["H1"]["hunk"]]
    assert sr.claim_statuses(records)["R1-1"]["status"] == "minor"


# --- Task 5: status, verdict, finalize, check --------------------------------------------


def reply_by(batch, decide, why="graded under B1 to B3"):
    """A valid reply: canaries answered correctly, claims by decide(claim_id)."""
    lines = []
    for cid, item in batch["map"].items():
        value = item["answer"] if "canary" in item else decide(item["claim"])
        lines.append(
            json.dumps({"cid": cid, "blocking": value, "q2": "na", "why": why})
        )
    return "\n".join(lines) + "\n"


def grade_all(report, tmp_path, decide):
    records = sr.load_ledger(report.read_text(encoding="utf-8"))
    for batch in sr.build_batches(records, CANARIES):
        code, out = apply(report, tmp_path, batch, reply_by(batch, decide))
        assert code == 0, out


def audit_none_real(report, tmp_path):
    items = sr.audit_items(sr.load_ledger(report.read_text(encoding="utf-8")))
    path = tmp_path / "audit-reply.txt"
    path.write_text(
        "\n".join(
            json.dumps({"aid": a, "real": False, "why": "not blocking"}) for a in items
        )
        + "\n",
        encoding="utf-8",
    )
    code, out = run("apply-audit", "--report", report, "--reply", path)
    assert code == 0, out


def finalize(report, *extra):
    code, out = run("finalize", "--report", report, *extra)
    assert code == 0, out
    return report.read_text(encoding="utf-8")


def full_review(tmp_path, n, spec_text, claims, decide, prior=None, baseline=None):
    """Run begin, seal, grading, the audit when due and finalize; return (report, spec path)."""
    spec = tmp_path / f"spec-r{n}.md"
    spec.write_text(spec_text, encoding="utf-8")
    report = tmp_path / f"report-r{n}.md"
    args = ["begin", "--report", report, "--spec", spec]
    if prior:
        args += ["--re-review", prior, "--baseline", baseline]
    code, out = run(*args)
    assert code == 0, out
    sealed(report, spec, claims)
    grade_all(report, tmp_path, decide)
    if not sr.audit_blockers(sr.load_ledger(report.read_text())):
        audit_none_real(report, tmp_path)
    finalize(report)
    return report, spec


def test_verdict_table_pass_needs_the_audit_and_ignores_minor_form(review1, tmp_path):
    spec, report = review1
    sealed(
        report,
        spec,
        many_claims(2) + [claim("R1-9", "Line 9: the Pedalbay kiosk rule number nine")],
    )
    grade_all(report, tmp_path, lambda cid: False)
    assert (
        sr.compute_verdict(sr.load_ledger(report.read_text()))["reason"] == "incomplete"
    )  # no audit yet
    audit_none_real(report, tmp_path)
    v = sr.compute_verdict(sr.load_ledger(report.read_text()))
    assert (v["value"], v["reason"], v["pre_audit"]) == (
        "PASS",
        "none",
        "PASS",
    )  # minor-form never makes it incomplete


def test_verdict_table_fail_reasons(review2, tmp_path):
    spec2, report2, _ = review2
    sealed(
        report2,
        spec2,
        [
            claim("R2-1", "now releases a locker only after the rider scans out"),
            {"k": "checked", "lines": "9"},
            {"k": "prior", "id": "R1-1", "status": "open", "resolved_by": None},
        ],
    )
    grade_all(report2, tmp_path, lambda cid: False)
    assert (
        sr.compute_verdict(sr.load_ledger(report2.read_text()))["reason"]
        == "unresolved-prior"
    )
    recs = sr.load_ledger(report2.read_text())
    graded = [r if r["k"] != "grade" else dict(r, blocking=True) for r in recs]
    assert sr.compute_verdict(graded)["reason"] == "confirmed"
    unconf = [r for r in recs if r["k"] not in ("grade", "grade-raw")]
    unconf = [r if r["k"] != "prior" else dict(r, status="resolved") for r in unconf]
    assert sr.compute_verdict(unconf)["reason"] == "incomplete"  # an ungraded claim
    uncovered = [r for r in recs if r["k"] != "prior"] + [
        {"k": "uncovered", "hunk": [9, 9]}
    ]
    uncovered = [r for r in uncovered if r["k"] != "checked"]
    assert (
        sr.compute_verdict(
            uncovered + [{"k": "prior", "id": "R1-1", "status": "resolved"}]
        )["reason"]
        == "incomplete"
    )


def test_status_and_verdict_subcommands_print_the_computed_state(review1, tmp_path):
    spec, report = review1
    sealed(report, spec, many_claims(1))
    grade_all(report, tmp_path, lambda cid: True)
    assert run("status", "--report", report)[1].strip() == "R1-1: confirmed"
    assert (
        run("verdict", "--report", report)[1].strip()
        == "verdict: FAIL reason=confirmed"
    )


def test_check_passes_on_a_fresh_report_and_is_repeatable(review1, tmp_path):
    spec, report = review1
    sealed(report, spec, many_claims(2))
    grade_all(report, tmp_path, lambda cid: cid == "R1-2")
    text = finalize(report)
    assert text.rstrip().splitlines()[-1] == "verdict: FAIL"
    sentinel = sr.parse_sentinel(text)
    assert (
        sentinel["review"] == "1/3"
        and sentinel["confirmed"] == "1"
        and sentinel["reason"] == "confirmed"
    )
    first_run = run("check", "--report", report, "--spec", spec)
    assert first_run[0] == 0, first_run[1]
    assert run("check", "--report", report) == first_run[:1] + (first_run[1],)
    assert report.read_text(encoding="utf-8") == text


def test_ledger_edited_after_seal_makes_check_exit_6(review1, tmp_path):
    spec, report = review1
    sealed(report, spec, many_claims(1))
    grade_all(report, tmp_path, lambda cid: True)
    text = finalize(report)
    report.write_text(
        text.replace("double charges the rider", "charges the rider once"),
        encoding="utf-8",
    )
    code, out = run("check", "--report", report)
    assert code == 6 and "sealed hash" in out


def test_grade_raw_changed_after_apply_grades_makes_check_exit_6(review1, tmp_path):
    spec, report = review1
    sealed(report, spec, many_claims(1))
    grade_all(report, tmp_path, lambda cid: True)
    text = finalize(report)
    report.write_text(
        text.replace("graded under B1 to B3", "graded under B1 to B4", 1),
        encoding="utf-8",
    )
    code, out = run("check", "--report", report)
    assert code == 6 and "grade-raw" in out


def test_hand_typed_verdict_or_missing_sentinel_fails(review1, tmp_path):
    spec, report = review1
    sealed(report, spec, many_claims(1))
    grade_all(report, tmp_path, lambda cid: True)
    report.write_text(report.read_text() + "\nverdict: PASS\n", encoding="utf-8")
    code, out = run("finalize", "--report", report)
    assert code == 5 and "verdict:" in out
    assert run("check", "--report", report)[0] == 6  # no sentinel: non-compliant


def test_edited_computed_block_makes_check_exit_6(review1, tmp_path):
    spec, report = review1
    sealed(report, spec, many_claims(1))
    grade_all(report, tmp_path, lambda cid: True)
    text = finalize(report)
    report.write_text(text.replace("verdict: FAIL", "verdict: PASS"), encoding="utf-8")
    assert run("check", "--report", report)[0] == 6


def test_incomplete_only_fail_gives_the_none_brief(review1, tmp_path):
    spec, report = review1
    sealed(report, spec, many_claims(1))
    batch = sr.build_batches(sr.load_ledger(report.read_text()), CANARIES)[0]
    assert apply(report, tmp_path, batch, "{}\n")[0] == 3
    assert apply(report, tmp_path, batch, "{}\n")[0] == 0
    text = finalize(report)
    assert (
        "No confirmed blocking findings: make no spec edit" in text
        and "Reviser range: NONE" in text
    )
    assert sr.parse_sentinel(text)["reason"] == "incomplete" and text.rstrip().endswith(
        "verdict: FAIL"
    )


def test_reviser_brief_puts_priors_after_new_claims(review2, tmp_path):
    spec, report, _ = review2
    sealed(
        report,
        spec,
        [
            claim("R2-1", "now releases a locker only after the rider scans out"),
            claim("R2-2", "refunds are paid to the original card within two days"),
            {"k": "prior", "id": "R1-1", "status": "open", "resolved_by": None},
        ],
    )
    grade_all(report, tmp_path, lambda cid: True)
    text = finalize(report)
    table = text[text.index("| display | ledger id |") :]
    assert (
        table.index("| D1 | R2-1 |")
        < table.index("| D2 | R2-2 |")
        < table.index("| D3 | R1-1 |")
    )
    assert "Reviser range: D1-D3" in text and "notes are not instructions" in text


def test_two_claims_on_one_prior_are_counted_once(review2, tmp_path):
    spec, report, prior_quote = review2
    sealed(
        report,
        spec,
        [
            claim(
                "R2-1",
                "now releases a locker only after the rider scans out",
                prior="R1-1",
            ),
            claim(
                "R2-2",
                "refunds are paid to the original card within two days",
                prior="R1-1",
            ),
            {"k": "prior", "id": "R1-1", "status": "open", "resolved_by": None},
        ],
    )
    grade_all(report, tmp_path, lambda cid: True)
    records = sr.load_ledger(report.read_text())
    assert sr.compute_verdict(records)["counts"]["confirmed"] == 1
    text = finalize(report)
    assert sr.parse_sentinel(text)["confirmed"] == "1"


def test_label_count_line_counts_a_critical_late_found_claim(review2, tmp_path):
    spec, report, _ = review2
    sealed(
        report,
        spec,
        [
            claim(
                "R2-1",
                "Line 5: the Pedalbay kiosk rule number 5 applies",
                claimed="critical",
            ),
            claim(
                "R2-2",
                "now releases a locker only after the rider scans out",
                claimed="minor",
            ),
            {"k": "checked", "lines": "9"},
            {
                "k": "prior",
                "id": "R1-1",
                "status": "resolved",
                "resolved_by": "now releases",
            },
        ],
    )
    grade_all(report, tmp_path, lambda cid: False)
    audit_none_real(report, tmp_path)
    text = finalize(report)
    assert (
        "label-count critical+major (owner measure, includes deferred, demoted and withdrawn): 1"
        in text
    )
    assert (
        "R2-1: late-found" in text
        and "## PASS with known debt" in text
        and text.rstrip().endswith("verdict: PASS")
    )


def test_review3_escalation_holds_cap_sentence_and_unadjudicated_items(tmp_path):
    v1 = spec_lines(12, "v1")
    r1, s1 = full_review(
        tmp_path,
        1,
        v1,
        [claim("R1-1", "Line 3: the Pedalbay kiosk rule number 3 applies")],
        lambda cid: True,
    )
    v2 = v1.replace(
        "Line 3: the Pedalbay kiosk rule number 3 applies to every locker bay (v1 text).",
        "Line 3: lockers release only after the rider scans out at the kiosk (fix one).",
    )
    r2, s2 = full_review(
        tmp_path,
        2,
        v2,
        [
            claim(
                "R2-1", "lockers release only after the rider scans out at the kiosk"
            ),
            {
                "k": "prior",
                "id": "R1-1",
                "status": "resolved",
                "resolved_by": "lockers release only after",
            },
        ],
        lambda cid: True,
        prior=r1,
        baseline=s1,
    )
    v3 = v2.replace(
        "lockers release only after the rider scans out at the kiosk (fix one).",
        "lockers release after the rider scans out or after a two hour timeout (fix two).",
    )
    r3, s3 = full_review(
        tmp_path,
        3,
        v3,
        [
            claim(
                "R3-1",
                "lockers release after the rider scans out or after a two hour timeout",
                claimed="critical",
            ),
            claim(
                "R3-2", "Line 6: the Pedalbay kiosk rule number six", claimed="major"
            ),
            claim(
                "R3-3",
                "Line 7: the Pedalbay kiosk rule number 7 applies",
                claimed="major",
            ),
            {"k": "prior", "id": "R2-1", "status": "open", "resolved_by": None},
        ],
        lambda cid: cid != "R3-3",
        prior=r2,
        baseline=s2,
    )
    text = r3.read_text(encoding="utf-8")
    esc = text[text.index("## Escalation to the user") :]
    assert (
        esc.splitlines()[1]
        == "ESCALATION: spec-panel-stoprule review 3 of 3, verdict FAIL"
    )
    assert (
        sr.CAP_SENTENCE
        == "at most 2 fix cycles (3 reviews), then escalate to the user with the open blocking findings"
    )
    assert sr.CAP_SENTENCE in esc and "This command will not run review 4." in esc
    section_c = esc[
        esc.index("(c) Unadjudicated items, not audited in the run:") : esc.index(
            "(d) "
        )
    ]
    assert "R3-2 (minor-form)" in section_c
    assert "## Reviser brief" not in text and sr.parse_sentinel(text)["review"] == "3/3"
    assert "| R2-1 | 2 | r2 open, r3 open |" in esc
    assert run("check", "--report", r3, "--spec", s3)[0] == 0
    code, out = run(
        "begin",
        "--report",
        tmp_path / "r4.md",
        "--spec",
        s3,
        "--re-review",
        r3,
        "--baseline",
        s3,
    )
    assert (
        code == 4
        and "ESCALATION: spec-panel-stoprule review 3 of 3, verdict FAIL" in out
    )


def test_review3_escalation_lists_a_grader_demoted_claim(tmp_path):
    v1 = spec_lines(12, "v1")
    r1, s1 = full_review(
        tmp_path,
        1,
        v1,
        [claim("R1-1", "Line 3: the Pedalbay kiosk rule number 3 applies")],
        lambda cid: True,
    )
    v2 = v1.replace(
        "rule number 3 applies to every locker bay (v1 text).",
        "rule number 3 now waits for the scan out (fix one).",
    )
    r2, s2 = full_review(
        tmp_path,
        2,
        v2,
        [
            claim("R2-1", "rule number 3 now waits for the scan out"),
            {
                "k": "prior",
                "id": "R1-1",
                "status": "resolved",
                "resolved_by": "now waits",
            },
        ],
        lambda cid: True,
        prior=r1,
        baseline=s1,
    )
    v3 = v2.replace(
        "now waits for the scan out (fix one).",
        "waits for the scan out or a two hour timeout (fix two).",
    )
    r3, _ = full_review(
        tmp_path,
        3,
        v3,
        [
            claim("R3-1", "rule number 3 waits for the scan out or a two hour timeout"),
            {"k": "prior", "id": "R2-1", "status": "open", "resolved_by": None},
        ],
        lambda cid: False,
        prior=r2,
        baseline=s2,
    )
    text = r3.read_text(encoding="utf-8")
    section_c = text[text.index("(c) Unadjudicated items") : text.index("(d) ")]
    assert "R3-1 (minor)" in section_c


def test_begin_exits_5_on_prior_verdict_mismatch(tmp_path):
    spec_text = spec_lines()
    spec = tmp_path / "spec.md"
    spec.write_text(spec_text, encoding="utf-8")
    prior = prior_report(
        tmp_path,
        spec_text,
        review=1,
        verdict="PASS",
        finals=[
            ("R1-1", "confirmed", "Line 2: the Pedalbay kiosk rule number 2", OUTCOME)
        ],
    )
    code, out = run(
        "begin",
        "--report",
        tmp_path / "r.md",
        "--spec",
        spec,
        "--re-review",
        prior,
        "--baseline",
        spec,
    )
    assert code == 5 and "recomputed verdict" in out


def test_finalize_and_check_dry_run_write_nothing(review1, tmp_path):
    spec, report = review1
    sealed(report, spec, many_claims(1))
    grade_all(report, tmp_path, lambda cid: True)
    before = snapshot(tmp_path)
    code, out = run("finalize", "--report", report, "--dry-run")
    assert code == 0 and "nothing written" in out and "verdict: FAIL" in out
    assert snapshot(tmp_path) == before
    finalize(report)
    before = snapshot(tmp_path)
    for sub in ("check", "status", "verdict"):
        assert run(sub, "--report", report, "--dry-run")[0] == 0
    assert snapshot(tmp_path) == before


def edit_ledger(report, kind, change):
    """Rewrite every ledger record of one kind with change(record) (a tamper in the test)."""
    lines = report.read_text(encoding="utf-8").splitlines()
    a, b = sr.ledger_bounds(lines)
    for n in range(a + 1, b):
        if lines[n].strip() and json.loads(lines[n])["k"] == kind:
            new = change(json.loads(lines[n]))
            lines[n] = "" if new is None else sr.dump(new)
    report.write_text("\n".join(lines) + "\n", encoding="utf-8")


def test_deleted_uncovered_record_makes_check_exit_6(review2, tmp_path):
    spec, report, _ = review2
    sealed(
        report,
        spec,
        [
            claim("R2-1", "now releases a locker only after the rider scans out"),
            {
                "k": "prior",
                "id": "R1-1",
                "status": "resolved",
                "resolved_by": "now releases",
            },
        ],
    )
    assert records_of(report, "uncovered")
    edit_ledger(report, "uncovered", lambda r: None)
    grade_all(report, tmp_path, lambda cid: False)
    audit_none_real(report, tmp_path)
    finalize(report)
    code, out = run("check", "--report", report, "--spec", spec)
    assert code == 6


def test_flipped_audit_record_makes_check_exit_6(review1, tmp_path):
    spec, report = review1
    sealed(report, spec, many_claims(1))
    grade_all(report, tmp_path, lambda cid: False)
    items = sr.audit_items(sr.load_ledger(report.read_text()))
    reply = tmp_path / "audit.txt"
    reply.write_text(
        "\n".join(
            json.dumps({"aid": a, "real": a == "A1", "why": "real"}) for a in items
        )
        + "\n"
    )
    assert run("apply-audit", "--report", report, "--reply", reply)[0] == 0
    edit_ledger(report, "audit", lambda r: dict(r, real=False))
    text = finalize(report)
    assert text.rstrip().endswith("verdict: PASS")  # the tamper fooled finalize ...
    code, out = run("check", "--report", report)
    assert code == 6  # ... but not check


def test_edited_mark_or_begin_record_makes_check_exit_6(review2, tmp_path):
    spec, report, _ = review2
    sealed(
        report,
        spec,
        [
            claim("R2-1", "Line 5: the Pedalbay kiosk rule number 5 applies"),
            {"k": "checked", "lines": "1-12"},
            {
                "k": "prior",
                "id": "R1-1",
                "status": "resolved",
                "resolved_by": "now releases",
            },
        ],
    )
    grade_all(report, tmp_path, lambda cid: True)
    finalize(report)
    assert run("check", "--report", report)[0] == 0
    clean = report.read_text(encoding="utf-8")
    edit_ledger(report, "mark", lambda r: dict(r, quote_lines=[3]))
    assert run("check", "--report", report)[0] == 6
    report.write_text(clean, encoding="utf-8")
    edit_ledger(report, "begin", lambda r: dict(r, changed=r["changed"] + [5]))
    assert run("check", "--report", report)[0] == 6


# --- Task 6: recorder subcommands -------------------------------------------------------


def graded_report(review1, tmp_path, decide=lambda cid: True):
    spec, report = review1
    sealed(report, spec, many_claims(2))
    grade_all(report, tmp_path, decide)
    return spec, report


def transcript_with(tmp_path, texts, tool="Agent"):
    """A session transcript: one tool_use per text (named tool) and its tool_result."""
    path = tmp_path / "session.jsonl"
    rows = [
        {
            "type": "assistant",
            "message": {
                "content": [{"type": "text", "text": "dispatching graders"}]
                + [
                    {"type": "tool_use", "id": f"t{n}", "name": tool, "input": {}}
                    for n in range(len(texts))
                ]
            },
        }
    ]
    rows += [
        {
            "type": "user",
            "message": {
                "content": [
                    {
                        "type": "tool_result",
                        "tool_use_id": f"t{n}",
                        "content": [{"type": "text", "text": t}],
                    }
                ]
            },
        }
        for n, t in enumerate(texts)
    ]
    path.write_text("\n".join(json.dumps(r) for r in rows) + "\n", encoding="utf-8")
    return path


def test_verify_transcript_verified_mismatch_and_unverified(review1, tmp_path):
    spec, report = graded_report(review1, tmp_path)
    reply = records_of(report, "grade-raw")[0]["text"]
    good = transcript_with(tmp_path, ["agent said:\n" + reply + "\nagentId: x"])
    assert run("verify-transcript", "--report", report, "--transcript", good)[
        1
    ].startswith("grader-integrity: verified")
    changed = reply.replace("B1 to B3", "B1 to B4", 1)
    bad = transcript_with(tmp_path, [changed])
    assert run("verify-transcript", "--report", report, "--transcript", bad)[
        1
    ].startswith("grader-integrity: mismatch")
    code, out = run(
        "verify-transcript",
        "--report",
        report,
        "--transcript",
        tmp_path / "missing.jsonl",
    )
    assert code == 0 and out.startswith("grader-integrity: unverified")


def test_verify_transcript_counts_only_whole_agent_results(review1, tmp_path):
    spec, report = graded_report(review1, tmp_path)
    reply = records_of(report, "grade-raw")[0]["text"]
    read_back = transcript_with(tmp_path, [reply], tool="Read")
    out = run("verify-transcript", "--report", report, "--transcript", read_back)[1]
    assert (
        out.startswith("grader-integrity: unverified") and "no Agent tool result" in out
    )
    half = len(reply) // 2
    split = transcript_with(tmp_path, [reply[:half], reply[half:]])
    out = run("verify-transcript", "--report", report, "--transcript", split)[1]
    assert out.startswith("grader-integrity: mismatch")
    empty = tmp_path / "empty.jsonl"
    empty.write_text("", encoding="utf-8")
    out = run("verify-transcript", "--report", report, "--transcript", empty)[1]
    assert out.startswith("grader-integrity: unverified")


def test_check_disposition_lists_an_applied_id_outside_the_brief(review1, tmp_path):
    spec, report = graded_report(review1, tmp_path)
    finalize(report)
    disp = tmp_path / "disposition.md"
    disp.write_text(
        "| D1 | applied |\n| D2 | applied |\n| D7 | applied |\n| R1-9 | not applied |\n",
        encoding="utf-8",
    )
    code, out = run("check-disposition", "--report", report, "--disposition", disp)
    assert code == 0
    assert "brief range: D1, D2" in out and "applied outside D1..Dk: D7" in out


def test_audit_sample_is_seeded_and_keeps_every_critical_demotion(tmp_path):
    reports = []
    for n in range(2):
        folder = tmp_path / f"run{n}"
        folder.mkdir()
        spec = folder / "spec.md"
        spec.write_text(spec_lines(12), encoding="utf-8")
        report = folder / "report.md"
        assert run("begin", "--report", report, "--spec", spec)[0] == 0
        sealed(report, spec, many_claims(10))
        grade_all(report, folder, lambda cid: cid.endswith(("1", "2")))
        finalize(report)
        reports.append(report)
    a = run("audit-sample", "--report", *reports, "--seed", "7", "--owner-k", "5")
    b = run("audit-sample", "--report", *reports, "--seed", "7", "--owner-k", "5")
    assert a[0] == 0 and a == b
    items = [json.loads(x) for x in a[1].splitlines()]
    crit = {(i["report"], i["id"]) for i in items if i["stratum"] == "critical-demoted"}
    expected = set()
    for report in reports:
        recs = sr.load_ledger(report.read_text())
        claims = {c["id"]: c for c in recs if c["k"] == "claim"}
        expected |= {
            (str(report), f["id"])
            for f in recs
            if f["k"] == "final"
            and f["status"] in sr.DEMOTED
            and claims[f["id"]]["claimed"] == "critical"
        }
    assert crit == expected and expected
    assert sum(i["owner"] for i in items) == 5
    assert {i["stratum"] for i in items} >= {
        "critical-demoted",
        "non-blocking",
        "confirmed",
    }


def test_count_reports_the_owner_measure_with_deferred_and_withdrawn(review2, tmp_path):
    spec, report, _ = review2
    add_reviewer_lines(
        report,
        [
            claim(
                "R2-1",
                "now releases a locker only after the rider scans out",
                claimed="major",
            ),  # confirmed
            claim(
                "R2-2",
                "Line 5: the Pedalbay kiosk rule number 5 applies",
                claimed="critical",
            ),  # late-found
            claim(
                "R2-3",
                "refunds are paid to the original card within two days",
                claimed="major",
            ),  # grader minor
            claim(
                "R2-4", "Line 6: the Pedalbay kiosk rule number six", claimed="major"
            ),  # minor-form
            claim(
                "R2-5", "Line 7: the Pedalbay kiosk rule number seven", claimed="major"
            ),  # dropped, new
            claim(
                "R2-6",
                "Line 8: the Pedalbay kiosk rule number eight",
                claimed="major",
                prior="R1-1",
            ),  # dropped, carried
            {
                "k": "prior",
                "id": "R1-1",
                "status": "resolved",
                "resolved_by": "now releases",
            },
        ],
    )
    assert run("seal", "--report", report, "--spec", spec)[0] == 3
    replace_reviewer_lines(
        report,
        [
            r
            for r in sr.load_ledger(report.read_text())
            if r["k"] in sr.REVIEWER_KINDS and r.get("id") not in ("R2-5", "R2-6")
        ],
    )
    assert run("seal", "--report", report, "--spec", spec)[0] == 0
    grade_all(report, tmp_path, lambda cid: cid == "R2-1")
    code, out = run("count", "--report", report)
    assert code == 0
    assert out.splitlines() == [
        "m0_label_cm=5",
        "m0_deferred_cm=4",
        "m1_open_confirmed=1",
    ]


def test_count_m1_counts_a_claim_linked_to_an_open_prior_once(review2, tmp_path):
    spec, report, prior_quote = review2
    sealed(
        report,
        spec,
        [
            claim(
                "R2-1",
                "now releases a locker only after the rider scans out",
                prior="R1-1",
            ),
            {"k": "checked", "lines": "9"},
            {"k": "prior", "id": "R1-1", "status": "open", "resolved_by": None},
        ],
    )
    grade_all(report, tmp_path, lambda cid: True)
    assert run("count", "--report", report)[1].splitlines()[2] == "m1_open_confirmed=1"


def test_recorder_subcommands_write_nothing(review1, tmp_path):
    spec, report = graded_report(review1, tmp_path)
    finalize(report)
    disp = tmp_path / "d.md"
    disp.write_text("| D1 | applied |\n", encoding="utf-8")
    before = snapshot(tmp_path)
    for args in (
        (
            "verify-transcript",
            "--report",
            report,
            "--transcript",
            tmp_path / "none.jsonl",
        ),
        ("check-disposition", "--report", report, "--disposition", disp),
        ("audit-sample", "--report", report, "--seed", "1"),
        ("count", "--report", report),
    ):
        assert run(*args)[0] == 0
    assert snapshot(tmp_path) == before


def test_script_imports_only_the_allowed_standard_library_modules():
    text = _SCRIPT.read_text(encoding="utf-8")
    imports = [
        line for line in text.splitlines() if line.startswith(("import ", "from "))
    ]
    assert imports == [
        f"import {m}"
        for m in (
            "argparse",
            "difflib",
            "hashlib",
            "json",
            "pathlib",
            "random",
            "re",
            "sys",
        )
    ]
    assert (
        "subprocess" not in text
        and "urllib" not in text
        and "src/superclaude" not in text
    )


def test_count_m1_includes_an_unclaimed_hunk_the_audit_judged_real(review1, tmp_path):
    spec, report = graded_report(review1, tmp_path, decide=lambda cid: False)
    items = sr.audit_items(sr.load_ledger(report.read_text()))
    reply = tmp_path / "audit.txt"
    reply.write_text(
        "\n".join(
            json.dumps({"aid": a, "real": a == "H1", "why": "real"}) for a in items
        )
        + "\n"
    )
    assert run("apply-audit", "--report", report, "--reply", reply)[0] == 0
    text = finalize(report)
    assert sr.parse_sentinel(text)["confirmed"] == "1"
    assert run("count", "--report", report)[1].splitlines()[2] == "m1_open_confirmed=1"


def test_audit_sample_records_exact_probabilities_for_unequal_sub_strata(tmp_path):
    spec = tmp_path / "spec.md"
    spec.write_text(spec_lines(12), encoding="utf-8")
    report = tmp_path / "report.md"
    assert run("begin", "--report", report, "--spec", spec)[0] == 0
    seven = [
        claim(
            f"R1-{i}",
            f"Line {i}: the Pedalbay kiosk rule number {i} applies",
            claimed="major",
        )
        for i in range(1, 8)
    ]
    sealed(
        report,
        spec,
        seven
        + [
            claim(
                "R1-9", "Line 9: the Pedalbay kiosk rule number nine", claimed="major"
            )
        ],
    )
    grade_all(report, tmp_path, lambda cid: False)
    finalize(report)
    items = [
        json.loads(x)
        for x in run(
            "audit-sample", "--report", report, "--seed", "3", "--owner-k", "0"
        )[1].splitlines()
    ]
    assert len(items) == 2  # n = max(2, ceil(8 / 4)): one forced pick per sub-stratum
    p = {i["status"]: i["p"] for i in items}
    assert p == {"minor-form": 1.0, "minor": round(1 / 7, 4)}


# --- Task 7: control-r1 replay fixture ---------------------------------------------------

CTL = Path(__file__).resolve().parent / "fixtures/stoprule/ctl-r1"


def scaffold_review2_report(path, spec_v2_text):
    """TEST SCAFFOLDING, not a control-r1 file.

    The control-r1 round-2 report has no stoprule sentinel (it predates the script), so
    `begin --re-review` on it would exit 5. This builds a minimal review-2 report whose
    sentinel records review=2/3, spec=<sha256[:12] of spec-v2.md> and the pinned rubric,
    with a ledger whose recomputed verdict matches its last line. It stands in only for
    that missing sentinel; the spec versions and the 8 claims under test are the real
    control-r1 files.
    """
    begin = {
        "k": "begin",
        "v": 1,
        "review": 2,
        "cap": 3,
        "nonce": "0" * 16,
        "spec_sha": hashlib.sha256(spec_v2_text.encode()).hexdigest(),
        "spec_path": "spec-v2.md",
        "spec_lines": len(spec_v2_text.splitlines()),
        "spec_bytes": len(spec_v2_text.encode()),
        "baseline_sha": None,
        "rubric_sha": hashlib.sha256(RUBRIC_TEXT.encode()).hexdigest(),
        "rubric1": hashlib.sha256(RUBRIC_TEXT.encode()).hexdigest(),
        "ratchet": "off",
        "changed": [],
        "hunks": [],
        "priors": {},
        "history": [],
    }
    records = [
        begin,
        {"k": "seal", "sha256": sr.reviewer_hash([begin]), "final_pass": 1},
    ]
    verdict = sr.compute_verdict(records)["value"]
    body = [
        "# scaffold review-2 report (test scaffolding)",
        "",
        sr.FENCE_OPEN,
        *[sr.dump(r) for r in records],
        sr.FENCE_CLOSE,
        "",
        f"<!-- stoprule v1 review=2/3 spec={sha12(spec_v2_text)} rubric={sha12(RUBRIC_TEXT)} confirmed=0 late=0 minor=0 "
        f"unconfirmed=0 reason=incomplete pre_audit=na brief=FAIL grader_model=sonnet ratchet=off ledger=000000000000 -->",
        f"verdict: {verdict}",
    ]
    path.write_text("\n".join(body) + "\n", encoding="utf-8")
    return path


def test_replay_control_r1_review3_ratchet_split(tmp_path):
    v2 = (CTL / "spec-v2.md").read_text(encoding="utf-8")
    v3 = (CTL / "spec-v3.md").read_text(encoding="utf-8")
    base = tmp_path / "spec-v2.md"
    base.write_text(v2, encoding="utf-8")
    spec = tmp_path / "spec-v3.md"
    spec.write_text(v3, encoding="utf-8")
    prior = scaffold_review2_report(tmp_path / "scaffold-review2.md", v2)
    report = tmp_path / "review3.md"
    code, out = run(
        "begin",
        "--report",
        report,
        "--spec",
        spec,
        "--re-review",
        prior,
        "--baseline",
        base,
    )
    assert code == 0, out
    assert records_of(report, "begin")[0]["review"] == 3
    claims = [
        json.loads(x)
        for x in (CTL / "review3-claims.jsonl").read_text(encoding="utf-8").splitlines()
        if x.strip()
    ]
    assert len(claims) == 8 and all(c["k"] == "claim" for c in claims)
    # control claim on an unchanged line, so the late-found branch runs on the real files too
    v2_lines = set(v2.splitlines())
    control_line = next(
        x for x in v3.splitlines() if len(x) > 60 and x in v2_lines and v3.count(x) == 1
    )
    control = claim("CTRL-1", control_line[:120].rstrip(), outcome=OUTCOME)
    add_reviewer_lines(report, claims + [control])
    code, out = run("seal", "--report", report, "--spec", spec)
    if code == 3:  # uncovered real hunks: the second seal is final and records them
        code, out = run("seal", "--report", report, "--spec", spec)
    assert code == 0, out
    marks = {m["id"]: m for m in records_of(report, "mark")}
    assert all(marks[c["id"]]["form_ok"] for c in claims), {
        k: m["issues"] for k, m in marks.items()
    }
    expected = json.loads((CTL / "review3-expected.json").read_text(encoding="utf-8"))
    computed = {
        cid: ("late-found" if marks[cid]["late"] else "anchored") for cid in expected
    }
    assert computed == {cid: e["expected"] for cid, e in expected.items()}
    assert marks["CTRL-1"]["late"] is True
