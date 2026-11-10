"""Behaviour tests for the sc-review-ledger kernel (review_ledger.py).

The script is loaded by path (as tests/skills/test_workflow_archive.py does) and
its CLI is run through subprocess in tmp_path.

Enforcement type: EXECUTABLE (script behaviour).
"""

from __future__ import annotations

import fcntl
import importlib.util
import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

_REPO = Path(__file__).resolve().parents[2]
_SCRIPT = _REPO / "src/superclaude/skills/sc-review-ledger/scripts/review_ledger.py"
_FIX = Path(__file__).resolve().parent / "fixtures" / "review-ledger"
_spec = importlib.util.spec_from_file_location("review_ledger", _SCRIPT)
rl = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(rl)

sys.path.insert(0, str(Path(__file__).resolve().parent))
from test_review_severity_rule import CANONICAL_CAP_TEXT  # noqa: E402

# ---------------------------------------------------------------- helpers


def run(cwd: Path, *args: str) -> tuple[int, dict]:
    proc = subprocess.run(
        [sys.executable, str(_SCRIPT), *args], cwd=cwd, capture_output=True, text=True
    )
    out = proc.stdout.strip().splitlines()
    return proc.returncode, (json.loads(out[-1]) if out else {})


class Loop:
    """A doc under tmp_path plus thin wrappers that track --op and --expect-seq."""

    def __init__(self, tmp: Path, doc_fixture: str = "doc-r1.md"):
        self.tmp = tmp
        self.doc = tmp / "spec.md"
        shutil.copy(_FIX / doc_fixture, self.doc)
        self.ledger = tmp / "spec.review-ledger"
        self.n = 0

    def seq(self) -> int:
        return json.loads((self.ledger / "ledger.json").read_text())["seq"]

    def state(self) -> dict:
        return json.loads((self.ledger / "ledger.json").read_text())

    def init(self, *extra) -> tuple[int, dict]:
        return run(
            self.tmp, "init", "--doc", "spec.md", "--profile", "spec-panel", *extra
        )

    def mut(
        self, cmd: str, *extra, op: str | None = None, seq: int | None = None
    ) -> tuple[int, dict]:
        self.n += 1
        return run(
            self.tmp,
            cmd,
            "--doc",
            "spec.md",
            "--op",
            op or f"op{self.n}",
            "--expect-seq",
            str(self.seq() if seq is None else seq),
            *extra,
        )

    def find(self, fixture_or_rows, **kw):
        src = self.tmp / f"find-{self.n}.json"
        if isinstance(fixture_or_rows, str):
            shutil.copy(_FIX / fixture_or_rows, src)
        else:
            src.write_text(json.dumps(fixture_or_rows))
        return self.mut("find", "--input", str(src), **kw)

    def report(
        self, name: str = "report.md", body: str = "# Review\n\n1. findings\n"
    ) -> Path:
        p = self.tmp / name
        p.write_text(body)
        return p

    def close(self, report: Path, **kw):
        return self.mut("close", "--report", str(report), **kw)

    def verdict(self) -> tuple[int, dict]:
        return run(self.tmp, "verdict", "--doc", "spec.md")

    def status(self) -> dict:
        return run(self.tmp, "status", "--doc", "spec.md")[1]

    def json_input(self, name: str, data) -> Path:
        p = self.tmp / name
        p.write_text(json.dumps(data))
        return p

    def edit(self, fixture: str | None = None, text: str | None = None) -> None:
        if fixture:
            shutil.copy(_FIX / fixture, self.doc)
        else:
            self.doc.write_text(text)

    def begin(self, *extra, **kw):
        return self.mut("begin", *extra, **kw)

    def answer(self, data, **kw):
        src = (
            self.json_input(f"answer-{self.n}.json", data)
            if not isinstance(data, Path)
            else data
        )
        return self.mut("answer", "--input", str(src), **kw)

    def round1(self, rows="find-basic.json") -> Path:
        """init, find and close review 1 (CONTINUE with find-basic.json)."""
        assert self.init()[0] == 0
        assert self.find(rows)[0] == 0
        rep = self.report("r1.md")
        assert self.close(rep)[0] == 0
        return rep


def rows_by_label(state: dict) -> dict:
    return {r["label"]: r for r in state["rows"]}


def tree_digest(*paths: Path) -> dict:
    """Every file under the given paths, name -> bytes (a dry run must leave it unchanged)."""
    out = {}
    for p in paths:
        files = [p] if p.is_file() else sorted(x for x in p.rglob("*") if x.is_file())
        for f in files:
            out[str(f)] = f.read_bytes()
    return out


# ---------------------------------------------------------------- Task 1


def test_cap_reviews_tied_to_canonical_cap_text():
    assert rl.CAP_REVIEWS == 3
    assert "(3 reviews)" in CANONICAL_CAP_TEXT


@pytest.mark.parametrize(
    "label, blocking",
    [("F1", True), ("F2", True), ("F3", True), ("F4", False), ("F5", False)],
    ids=[
        "critical",
        "fr8-minor",
        "major-with-wrong-outcome",
        "major-without-wrong-outcome",
        "minor",
    ],
)
def test_blocking_formula(tmp_path, label, blocking):
    lp = Loop(tmp_path)
    assert lp.init()[0] == 0
    code, out = lp.find("find-basic.json")
    assert code == 0, out
    row = rows_by_label(lp.state())[label]
    assert row["blocking"] is blocking
    assert row["status"] == ("open" if blocking else "deferred")


def test_init_prints_review_header_and_snapshots(tmp_path):
    lp = Loop(tmp_path)
    code, out = lp.init()
    assert code == 0 and out["review_header"] == "review: 1 of 3"
    assert (lp.ledger / "snapshots" / "r1.md").read_bytes() == lp.doc.read_bytes()
    for sub in ("snapshots", "diffs", "inputs"):
        assert (lp.ledger / sub).is_dir()


def test_init_refuses_existing_ledger(tmp_path):
    lp = Loop(tmp_path)
    lp.init()
    code, out = lp.init()
    assert code == 3 and out["error"] == "E-EXISTS"


def test_archive_existing_keeps_old_folder(tmp_path):
    lp = Loop(tmp_path)
    lp.init()
    lp.find("find-basic.json")
    old = (lp.ledger / "ledger.json").read_bytes()
    code, out = lp.init("--archive-existing")
    assert code == 0, out
    archived = Path(out["archived"])
    assert archived.is_dir() and (archived / "ledger.json").read_bytes() == old
    assert lp.state()["rows"] == []


def test_find_refuses_missing_anchor(tmp_path):
    lp = Loop(tmp_path)
    lp.init()
    rows = [
        {
            "grade": "MINOR",
            "anchor": "This sentence is not in the document.",
            "finding": "x",
        }
    ]
    code, out = lp.find(rows)
    assert code == 2 and out["error"] == "E-ANCHOR"
    assert lp.state()["rows"] == []


def test_find_refuses_repeated_anchor(tmp_path):
    lp = Loop(tmp_path)
    lp.init()
    rows = [
        {
            "grade": "MINOR",
            "anchor": "The cache is refreshed every hour.",
            "finding": "x",
        }
    ]
    code, out = lp.find(rows)
    assert code == 2 and out["error"] == "E-ANCHOR-AMBIGUOUS"


def test_find_refuses_bad_shape(tmp_path):
    lp = Loop(tmp_path)
    lp.init()
    code, out = lp.find(
        [{"grade": "SEVERE", "anchor": "Logs are kept for seven days.", "finding": "x"}]
    )
    assert code == 2 and out["error"] == "E-SCHEMA"
    code, out = lp.find({"rows": []})
    assert code == 2 and out["error"] == "E-SCHEMA"


def test_second_find_refused_e_phase(tmp_path):
    lp = Loop(tmp_path)
    lp.init()
    assert lp.find("find-basic.json")[0] == 0
    code, out = lp.find(
        [
            {
                "grade": "MINOR",
                "anchor": "Logs are kept for seven days.",
                "finding": "again",
            }
        ]
    )
    assert code == 3 and out["error"] == "E-PHASE"


def test_empty_find_commits_zero_rows(tmp_path):
    lp = Loop(tmp_path)
    lp.init()
    code, out = lp.find("find-empty.json")
    assert code == 0 and out["counts"]["rows"] == 0
    assert lp.state()["seq"] == 2


def test_find_reads_one_ledger_input_block_from_a_report(tmp_path):
    lp = Loop(tmp_path)
    lp.init()
    rows = json.loads((_FIX / "find-basic.json").read_text())
    rep = lp.report(
        "r1.md", "# Review\n\n```ledger-input\n" + json.dumps(rows) + "\n```\n"
    )
    code, out = lp.mut("find", "--input", str(rep))
    assert code == 0, out
    assert out["counts"]["rows"] == 5


@pytest.mark.parametrize("blocks", [0, 2])
def test_find_report_needs_exactly_one_block(tmp_path, blocks):
    lp = Loop(tmp_path)
    lp.init()
    rep = lp.report("r1.md", "# Review\n" + "\n```ledger-input\n[]\n```\n" * blocks)
    code, out = lp.mut("find", "--input", str(rep))
    assert code == 2 and out["error"] == "E-SCHEMA"


def test_hand_edit_is_refused_and_file_unchanged(tmp_path):
    lp = Loop(tmp_path)
    lp.init()
    path = lp.ledger / "ledger.json"
    edited = path.read_text().replace('"round": 1', '"round": 2', 1)
    path.write_text(edited)
    code, out = lp.find("find-basic.json", seq=1)
    assert code == 3 and out["error"] == "E-TAMPERED"
    assert path.read_text() == edited
    code, out = run(tmp_path, "status", "--doc", "spec.md")
    assert code == 3 and out["error"] == "E-TAMPERED"


def test_tamper_check_runs_before_input_and_lock(tmp_path):
    lp = Loop(tmp_path)
    lp.init()
    path = lp.ledger / "ledger.json"
    path.write_text(path.read_text().replace('"round": 1', '"round": 2', 1))
    bad = lp.report("bad.md", "# no ledger-input block here\n")
    code, out = lp.mut("find", "--input", str(bad), seq=1)
    assert code == 3 and out["error"] == "E-TAMPERED"
    code, out = lp.close(tmp_path / "missing-report.md", seq=1)
    assert code == 3 and out["error"] == "E-TAMPERED"
    with open(lp.ledger / ".lock", "a+") as fh:
        fcntl.flock(fh.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        code, out = lp.find("find-basic.json", seq=1)
    assert code == 3 and out["error"] == "E-TAMPERED"


def test_identical_retry_under_new_op_id_returns_committed_result(tmp_path):
    lp = Loop(tmp_path)
    lp.init()
    code1, out1 = lp.find("find-basic.json", op="first", seq=1)
    code2, out2 = lp.find("find-basic.json", op="second", seq=1)
    assert code1 == code2 == 0
    assert out2["seq"] == out1["seq"] == 2 and out2.get("replayed") is True
    assert lp.state()["seq"] == 2 and len(lp.state()["rows"]) == 5


def test_stale_expect_seq_exits_4(tmp_path):
    lp = Loop(tmp_path)
    lp.init()
    code, out = lp.find("find-basic.json", seq=0)
    assert code == 4 and out["error"] == "E-STALE-SEQ"


def test_second_writer_while_lock_held_exits_4(tmp_path):
    lp = Loop(tmp_path)
    lp.init()
    with open(lp.ledger / ".lock", "a+") as fh:
        fcntl.flock(fh.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        code, out = lp.find("find-basic.json")
    assert code == 4 and out["error"] == "E-LOCKED"


def test_close_continue_tail_ends_verdict_fail(tmp_path):
    lp = Loop(tmp_path)
    lp.init()
    lp.find("find-basic.json")
    rep = lp.report()
    code, out = lp.close(rep)
    assert code == 0 and out["loop_decision"] == "CONTINUE"
    text = rep.read_text()
    assert text.startswith("# Review\n\n1. findings\n")
    lines = text.rstrip("\n").splitlines()
    assert lines[-1] == "verdict: FAIL"
    assert "review: 1 of 3" in lines
    brief = next(line for line in lines if line.startswith("Blocking rows to fix:"))
    labels = rows_by_label(lp.state())
    assert brief == "Blocking rows to fix: " + ", ".join(
        labels[x]["id"] for x in ("F1", "F2", "F3")
    )
    assert "byte size before and after" in text
    code, v = lp.verdict()
    assert code == 10 and v["verdict"] == "CONTINUE"
    assert lp.state()["phase"] == "revise"


def test_review1_pass_is_pending_until_the_sweep(tmp_path):
    lp = Loop(tmp_path)
    lp.init()
    lp.find(
        [
            {
                "grade": "MINOR",
                "anchor": "Logs are kept for seven days.",
                "finding": "vague",
            }
        ]
    )
    rep = lp.report()
    code, out = lp.close(rep)
    assert code == 0 and out["loop_decision"] == "PASS"
    assert rep.read_text().rstrip("\n").splitlines()[-1] == "loop: PASS (sweep pending)"
    assert "Reviser brief" not in rep.read_text()
    code, v = lp.verdict()
    assert code == 12 and v["verdict"] == "PENDING"


def test_review1_escalate_when_snapshot_changed(tmp_path):
    lp = Loop(tmp_path)
    lp.init()
    lp.find("find-basic.json")
    (lp.ledger / "snapshots" / "r1.md").write_text("changed by hand\n")
    rep = lp.report()
    code, out = lp.close(rep)
    assert (
        code == 0
        and out["loop_decision"] == "ESCALATE"
        and out["decision"]["I"] is False
    )
    assert (
        rep.read_text().rstrip("\n").splitlines()[-1]
        == "loop: ESCALATE (sweep pending)"
    )
    assert lp.verdict()[0] == 12


def test_close_before_find_refused(tmp_path):
    lp = Loop(tmp_path)
    lp.init()
    code, out = lp.close(lp.report())
    assert code == 3 and out["error"] == "E-PHASE"


def test_no_role_flag_and_stdlib_only():
    help_text = subprocess.run(
        [sys.executable, str(_SCRIPT), "--help"], capture_output=True, text=True
    ).stdout
    assert "--role" not in help_text
    src = _SCRIPT.read_text()
    assert "subprocess" not in src and "--role" not in src
    allowed = {
        "argparse",
        "fcntl",
        "hashlib",
        "json",
        "os",
        "re",
        "sys",
        "tempfile",
        "difflib",
        "shutil",
        "pathlib",
    }
    imported = set()
    for line in src.splitlines():
        if line.startswith("import "):
            imported.add(line.split()[1].split(".")[0])
        elif line.startswith("from "):
            imported.add(line.split()[1].split(".")[0])
    assert imported <= allowed, imported - allowed


# ---------------------------------------------------------------- Task 2


def by_id(state: dict) -> dict:
    return {r["id"]: r for r in state["rows"]}


def diff_doc(lp: Loop, cycle: int = 1) -> dict:
    return json.loads((lp.ledger / "diffs" / f"c{cycle}.json").read_text())


@pytest.mark.parametrize(
    "fixture, claimers",
    [
        ("doc-r2-outside.md", []),
        ("doc-r2-fix.md", ["R1"]),
        ("doc-r2-two-rows.md", ["R2", "R3"]),
    ],
    ids=["zero-rows", "one-row", "two-rows"],
)
def test_auto_claim_zero_one_two_rows(tmp_path, fixture, claimers):
    lp = Loop(tmp_path)
    lp.round1()
    lp.edit(fixture)
    code, out = lp.begin()
    assert code == 0, out
    hunks = diff_doc(lp)["hunks"]
    assert len(hunks) == 1
    assert sorted(c["row"] for c in hunks[0]["claimed_by"]) == claimers
    assert all(c["via"] == "auto" for c in hunks[0]["claimed_by"])
    rows = by_id(lp.state())
    for rid in ("R1", "R2", "R3"):
        assert rows[rid]["status"] == ("fixed" if rid in claimers else "open")
    assert (len(out["unclaimed"]) == 1) is (not claimers)
    assert out["review_header"] == "review: 2 of 3" and lp.state()["phase"] == "verify"


def test_pure_rewrap_is_admitted_not_unclaimed(tmp_path):
    lp = Loop(tmp_path)
    lp.round1()
    lp.edit("doc-r2-rewrap.md")
    code, out = lp.begin("--revert-unclaimed")
    assert code == 0, out
    assert out["unclaimed"] == [] and out["reverted_bytes"] == 0
    assert by_id(lp.state())["R1"]["status"] == "open"
    assert lp.doc.read_text() == (_FIX / "doc-r2-rewrap.md").read_text()
    assert "Whitespace-only rewraps" in (lp.ledger / "plan-r2.md").read_text()


def test_table_row_is_its_own_admission_unit(tmp_path):
    lp = Loop(tmp_path)
    lp.round1()
    lp.edit(
        text=lp.doc.read_text().replace(
            "for 30 days.", "for 30 days, then purges them."
        )
    )
    assert lp.begin()[0] == 0
    rows = by_id(lp.state())
    assert rows["R3"]["status"] == "fixed" and rows["R2"]["status"] == "open"


def test_unclaimed_hunk_kept_without_flag_restored_with_it(tmp_path):
    for flag, expect in (
        ([], "doc-r2-outside.md"),
        (["--revert-unclaimed"], "doc-r1.md"),
    ):
        sub = tmp_path / ("flag" if flag else "noflag")
        sub.mkdir()
        lp = Loop(sub)
        lp.round1()
        lp.edit("doc-r2-outside.md")
        code, out = lp.begin(*flag)
        assert code == 0, out
        assert lp.doc.read_text() == (_FIX / expect).read_text()
        assert (lp.ledger / "snapshots" / "r2.md").read_text() == lp.doc.read_text()
        assert out["unclaimed"][0]["reverted"] is bool(flag)
        assert out["unclaimed"][0]["bytes"] == len(
            "The cache is refreshed every ten minutes."
        )


def test_failed_preimage_counts_in_x(tmp_path, monkeypatch, capsys):
    lp = Loop(tmp_path)
    lp.round1()
    lp.edit("doc-r2-outside.md")
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(rl, "reread_doc", lambda doc: "changed while begin ran\n")
    code = rl.main(
        [
            "begin",
            "--doc",
            "spec.md",
            "--op",
            "b1",
            "--expect-seq",
            str(lp.seq()),
            "--revert-unclaimed",
        ]
    )
    out = json.loads(capsys.readouterr().out.strip().splitlines()[-1])
    assert code == 0 and out["counts"]["X"] == 1
    assert out["unclaimed"][0]["reverted"] is False
    assert lp.doc.read_text() == (_FIX / "doc-r2-outside.md").read_text()
    assert lp.status()["x_items"][0]["kind"] == "revert-preimage"


def test_zero_hunk_round_writes_plan_and_counts_as_review(tmp_path):
    lp = Loop(tmp_path)
    lp.round1()
    code, out = lp.begin()
    assert code == 0 and out["hunks"] == 0
    st = lp.state()
    assert st["round"] == 2 and st["fix_cycles"] == 1
    plan = (lp.ledger / "plan-r2.md").read_text()
    assert "review: 2 of 3" in plan and "### R1:" in plan


def test_half_open_ranges_and_deletion_tombstone(tmp_path):
    assert rl.overlaps((3, 3), (3, 5)) and rl.overlaps((5, 5), (3, 5))
    assert not rl.overlaps((6, 6), (3, 5)) and not rl.overlaps((5, 7), (3, 5))
    assert rl.overlaps((4, 6), (3, 5))
    lp = Loop(tmp_path)
    lp.round1()
    lp.edit("doc-r2-delete.md")
    assert lp.begin()[0] == 0
    hunks = diff_doc(lp)["hunks"]
    deletion, last = hunks
    assert deletion["old"] == [13, 15] and deletion["new"] == [13, 13]
    assert last["old"] == [23, 24] and last["new"] == [21, 22]
    assert "R5" in last["touches"] and last["claimed_by"] == []
    r5 = by_id(lp.state())["R5"]
    assert r5["mappings"][-1]["span"] == [21, 22]


def test_anchor_relocation_missing_and_ambiguous(tmp_path):
    wrapped = "# Spec\n\nThe archive keeps every invoice\nfor seven years after payment.\n\nOther text.\n"
    lp = Loop(tmp_path)
    lp.edit(text=wrapped)
    lp.init()
    lp.find(
        [
            {
                "grade": "CRITICAL",
                "anchor": "The archive keeps every invoice for seven years after payment.",
                "finding": "retention basis missing",
            }
        ]
    )
    lp.close(lp.report())
    lp.edit(text=wrapped.replace("for seven years", "for ten years"))
    code, out = lp.begin()
    assert code == 0 and out["counts"]["X"] == 1
    assert by_id(lp.state())["R1"]["mappings"][-1] == {
        "snapshot": "r2",
        "span": None,
        "method": "missing",
    }

    sub = tmp_path / "amb"
    sub.mkdir()
    lp = Loop(sub)
    lp.round1()
    quote = "When the store is down, the service returns 503 to the caller."
    lp.edit(
        text=lp.doc.read_text().replace(
            quote + " Retries are left to the caller.", quote + " " + quote
        )
    )
    code, out = lp.begin()
    assert code == 0 and out["counts"]["X"] == 1
    assert by_id(lp.state())["R1"]["mappings"][-1]["method"] == "ambiguous"


def test_answer_refusals(tmp_path):
    lp = Loop(tmp_path)
    lp.round1()
    lp.edit(
        text=(_FIX / "doc-r2-fix.md")
        .read_text()
        .replace("every hour.", "every minute.", 1)
    )
    hunks = {h["n"]: h for h in lp.status()["provisional_hunks"]}
    assert len(hunks) == 2  # hunk 1: the cache line (13), hunk 2: R1's paragraph (17)
    code, out = lp.answer({"claims": [{"row": "R4", "action": "fixed", "hunks": [1]}]})
    assert code == 2 and out["error"] == "E-ILLEGAL"
    code, out = lp.answer(
        {"claims": [{"row": "R1", "action": "fixed", "hunks": [1, 2]}]}
    )
    assert code == 2 and out["error"] == "E-CLAIM-WIDE"
    code, out = lp.answer({"claims": [{"row": "R2", "action": "fixed", "hunks": [2]}]})
    assert code == 2 and out["error"] == "E-FIXED-NO-EDIT"
    code, out = lp.answer({"claims": [{"row": "R1", "action": "fixed", "hunks": [2]}]})
    assert code == 0, out
    code, out = lp.begin()
    assert code == 0
    claimed = [h for h in diff_doc(lp)["hunks"] if h["claimed_by"]]
    assert claimed[0]["claimed_by"] == [{"row": "R1", "via": "answer"}]


def test_answer_basic_fixture_and_disposition_block(tmp_path):
    lp = Loop(tmp_path)
    lp.round1()
    lp.edit("doc-r2-fix.md")
    data = json.loads((_FIX / "answer-basic.json").read_text())
    disposition = lp.report(
        "disposition.md",
        "# Disposition\n\n```ledger-input\n" + json.dumps(data) + "\n```\n",
    )
    code, out = lp.answer(disposition)
    assert code == 0 and out["claims"][0]["row"] == "R1" and out["gaps"]
    assert lp.begin()[0] == 0
    assert (
        "the retry bound also needs a line in section 4"
        in (lp.ledger / "plan-r2.md").read_text()
    )


def test_revert_unclaimed_in_revise_and_e_phase_in_verify(tmp_path):
    lp = Loop(tmp_path)
    lp.round1()
    lp.edit("doc-r2-outside.md")
    (hunk,) = lp.status()["provisional_hunks"]
    code, out = lp.mut("revert-unclaimed", "--hunk", hunk["key"])
    assert code == 0 and out["reverted"] == [1] and out["restored_bytes"] > 0
    assert lp.doc.read_text() == (_FIX / "doc-r1.md").read_text()
    assert lp.begin()[0] == 0
    code, out = lp.mut("revert-unclaimed")
    assert code == 3 and out["error"] == "E-PHASE"


def test_revert_unclaimed_hunk_seen_in_status_is_preimage_checked(
    tmp_path, monkeypatch, capsys
):
    lp = Loop(tmp_path)
    lp.round1()
    lp.edit("doc-r2-outside.md")
    (seen,) = lp.status()["provisional_hunks"]
    # the document changes after status: the hunk the caller saw is gone, nothing is reverted
    lp.edit(text=(_FIX / "doc-r2-fix.md").read_text())
    code, out = lp.mut("revert-unclaimed", "--hunk", seen["key"])
    assert code == 0 and out["reverted"] == [] and out["failed"] == [seen["key"]]
    assert lp.doc.read_text() == (_FIX / "doc-r2-fix.md").read_text()
    # the document changes between the diff and the write: every revert fails its preimage
    lp.edit("doc-r2-outside.md")
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(rl, "reread_doc", lambda doc: "changed meanwhile\n")
    code = rl.main(
        [
            "revert-unclaimed",
            "--doc",
            "spec.md",
            "--op",
            "r2",
            "--expect-seq",
            str(lp.seq()),
        ]
    )
    out = json.loads(capsys.readouterr().out.strip().splitlines()[-1])
    assert code == 0 and out["reverted"] == [] and out["failed"] == [1]
    assert lp.doc.read_text() == (_FIX / "doc-r2-outside.md").read_text()


def test_revert_unclaimed_refuses_e_phase_when_terminal(tmp_path):
    lp = Loop(tmp_path)
    lp.round1(rows="find-empty.json")
    code, out = lp.mut("revert-unclaimed")
    assert code == 3 and out["error"] == "E-PHASE"


def test_e_terminal_after_review1_terminal_close(tmp_path):
    lp = Loop(tmp_path)
    lp.round1(rows="find-empty.json")
    assert lp.state()["phase"] == "terminal"
    code, out = lp.begin()
    assert code == 3 and out["error"] == "E-TERMINAL"
    code, out = lp.answer({"claims": []})
    assert code == 3 and out["error"] == "E-TERMINAL"


def test_hunks_large(tmp_path):
    lp = Loop(tmp_path)
    lp.round1()
    lp.edit(text="\n".join(f"Rewritten line {i}." for i in range(30)) + "\n")
    code, out = lp.begin()
    assert code == 0 and out["hunks_large"] is True
    assert "HUNKS_LARGE" in (lp.ledger / "plan-r2.md").read_text()


def test_plan_names_open_blocking_rows_and_unclaimed_bytes(tmp_path):
    lp = Loop(tmp_path)
    lp.round1()
    lp.edit(
        text=(_FIX / "doc-r2-fix.md")
        .read_text()
        .replace("every ten", "every ten")
        .replace(
            "The cache is refreshed every hour.\n\n## 3",
            "The cache is refreshed every ten minutes.\n\n## 3",
        )
    )
    code, out = lp.begin()
    assert code == 0
    plan = (lp.ledger / "plan-r2.md").read_text()
    for rid in ("R1", "R2", "R3"):
        assert f"### {rid}:" in plan
    assert "### R4:" not in plan and "### R5:" not in plan
    (unc,) = out["unclaimed"]
    assert f"- {unc['id']}: " in plan and f"bytes {unc['bytes']}" in plan


def test_dry_run_find_and_answer_write_nothing(tmp_path):
    lp = Loop(tmp_path)
    lp.init()
    rows = json.loads((_FIX / "find-basic.json").read_text())
    rep = lp.report(
        "r1.md", "# Review\n\n```ledger-input\n" + json.dumps(rows) + "\n```\n"
    )
    before = tree_digest(lp.ledger, lp.doc, rep)
    code, out = run(
        tmp_path, "find", "--doc", "spec.md", "--input", str(rep), "--dry-run"
    )
    assert code == 0 and out["dry_run"] is True and out["counts"]["rows"] == 5
    assert tree_digest(lp.ledger, lp.doc, rep) == before
    code, out = run(
        tmp_path,
        "find",
        "--doc",
        "spec.md",
        "--input",
        str(
            lp.json_input(
                "bad.json",
                [{"grade": "MINOR", "anchor": "not in the doc", "finding": "x"}],
            )
        ),
        "--dry-run",
    )
    assert code == 2 and out["error"] == "E-ANCHOR"
    assert lp.find("find-basic.json")[0] == 0 and lp.close(rep)[0] == 0
    lp.edit("doc-r2-fix.md")
    disp = lp.report(
        "disposition.md",
        "```ledger-input\n" + (_FIX / "answer-basic.json").read_text() + "\n```\n",
    )
    before = tree_digest(lp.ledger, lp.doc, disp)
    code, out = run(
        tmp_path, "answer", "--doc", "spec.md", "--input", str(disp), "--dry-run"
    )
    assert code == 0 and out["dry_run"] is True and out["claims"][0]["row"] == "R1"
    assert tree_digest(lp.ledger, lp.doc, disp) == before


def test_repeat_revert_after_a_new_edit_is_not_a_replay(tmp_path):
    lp = Loop(tmp_path)
    lp.round1()
    lp.edit("doc-r2-outside.md")
    code, out = lp.mut("revert-unclaimed")
    assert code == 0 and out["reverted"] == [1]
    lp.edit("doc-r2-outside.md")  # the reviser makes the same edit again
    seq = lp.seq()
    code, out = lp.mut("revert-unclaimed")
    assert code == 0 and out.get("replayed") is not True and out["seq"] == seq + 1
    assert lp.doc.read_text() == (_FIX / "doc-r1.md").read_text()


def test_repeat_answer_after_a_new_edit_is_not_a_replay(tmp_path):
    lp = Loop(tmp_path)
    lp.round1()
    claim = {"claims": [{"row": "R1", "action": "fixed", "hunks": [1]}]}
    lp.edit("doc-r2-fix.md")
    assert lp.answer(claim)[0] == 0
    lp.edit(
        text=(_FIX / "doc-r2-fix.md")
        .read_text()
        .replace("at most twice", "at most three times")
    )
    seq = lp.seq()
    code, out = lp.answer(claim)
    assert code == 0 and out.get("replayed") is not True and out["seq"] == seq + 1


def test_revert_retry_after_commit_is_stale_not_a_false_replay(tmp_path):
    lp = Loop(tmp_path)
    lp.round1()
    lp.edit("doc-r2-outside.md")
    seq = lp.seq()
    assert lp.mut("revert-unclaimed", op="a", seq=seq)[0] == 0
    # the committed revert changed the document, so the same request is a new one: stale seq
    code, out = lp.mut("revert-unclaimed", op="b", seq=seq)
    assert code == 4 and out["error"] == "E-STALE-SEQ"


def test_identical_answer_retry_is_replayed_while_document_unchanged(tmp_path):
    lp = Loop(tmp_path)
    lp.round1()
    lp.edit("doc-r2-fix.md")
    claim = {"claims": [{"row": "R1", "action": "fixed", "hunks": [1]}]}
    seq = lp.seq()
    c1, o1 = lp.answer(claim, op="a", seq=seq)
    c2, o2 = lp.answer(claim, op="b", seq=seq)
    assert c1 == c2 == 0 and o2.get("replayed") is True and o2["seq"] == o1["seq"]


# ---------------------------------------------------------------- Task 3

R1_QUOTE = "When the store is down, the service returns 503 to the caller."
ONE_BLOCKER = [
    {
        "label": "F1",
        "grade": "CRITICAL",
        "anchor": R1_QUOTE,
        "finding": "no retry budget",
    }
]


def verify(lp: Loop, data, **kw):
    return lp.mut(
        "verify", "--input", str(lp.json_input(f"verify-{lp.n}.json", data)), **kw
    )


def ans(row, result, evidence=None, touched_ok="yes", **extra):
    a = {"row": row, "result": result, "touched_ok": touched_ok, **extra}
    if evidence is not None:
        a["evidence"] = evidence
    return a


R2_EV = "The service rejects a widget without an owner."
R3_EV = "The service keeps deleted widgets for 30 days."
FIX_EV = "the caller retries at most twice"


def round2(lp: Loop, rows="find-basic.json", fixture="doc-r2-fix.md", *flags):
    lp.round1(rows=rows)
    lp.edit(fixture)
    code, out = lp.begin(*flags)
    assert code == 0, out
    return out


def basic_answers(r1="resolved"):
    return {
        "answers": [
            ans("R1", r1, FIX_EV, reason="x"),
            ans("R2", "open", R2_EV, reason="not fixed"),
            ans("R3", "open", R3_EV, reason="not fixed"),
        ]
    }


def test_verify_resolved_and_open_transitions(tmp_path):
    lp = Loop(tmp_path)
    round2(lp)
    code, out = verify(lp, basic_answers())
    assert code == 0, out
    rows = by_id(lp.state())
    assert rows["R1"]["status"] == "verified" and rows["R2"]["status"] == "open"
    sub = tmp_path / "open"
    sub.mkdir()
    lp = Loop(sub)
    round2(lp)
    assert verify(lp, basic_answers(r1="open"))[0] == 0
    assert by_id(lp.state())["R1"]["status"] == "open"


@pytest.mark.parametrize(
    "answers, code_name",
    [
        (
            [ans("R1", "resolved", FIX_EV), ans("R2", "open", R2_EV, reason="x")],
            "E-INCOMPLETE",
        ),
        (
            basic_answers()["answers"][:1]
            + [ans("R2", "resolved", R2_EV), ans("R3", "open", R3_EV, reason="x")],
            "E-NOT-CHANGED",
        ),
        (
            basic_answers()["answers"]
            + [{"row": "R4", "result": "open", "touched_ok": "yes", "grade": "MINOR"}],
            "E-FROZEN",
        ),
        (
            basic_answers()["answers"]
            + [ans("R4", "open", "It keeps one record per widget.", reason="x")],
            "E-ILLEGAL",
        ),
        (
            [ans("R1", "resolved", "a quote that is not in the snapshot")]
            + basic_answers()["answers"][1:],
            "E-ANCHOR",
        ),
    ],
    ids=[
        "incomplete",
        "resolved-on-untouched-open-row",
        "frozen",
        "deferred-row",
        "evidence-not-in-snapshot",
    ],
)
def test_verify_refusals(tmp_path, answers, code_name):
    lp = Loop(tmp_path)
    round2(lp)
    before = (lp.ledger / "ledger.json").read_bytes()
    code, out = verify(lp, {"answers": answers})
    assert code == 2 and out["error"] == code_name
    assert (lp.ledger / "ledger.json").read_bytes() == before


def test_verify_reads_a_report_block(tmp_path):
    lp = Loop(tmp_path)
    round2(lp)
    rep = lp.report(
        "r2.md",
        "# Round 2\n\n```ledger-input\n" + json.dumps(basic_answers()) + "\n```\n",
    )
    assert lp.mut("verify", "--input", str(rep))[0] == 0
    assert lp.close(rep)[1]["loop_decision"] == "CONTINUE"


def test_cannot_verify_keeps_status_and_escalates(tmp_path):
    lp = Loop(tmp_path)
    round2(lp, rows=ONE_BLOCKER)
    assert verify(lp, {"answers": [ans("R1", "cannot-verify")]})[0] == 0
    assert by_id(lp.state())["R1"]["status"] == "fixed"
    code, out = lp.close(lp.report("r2.md"))
    assert out["loop_decision"] == "ESCALATE" and out["decision"]["X"] == 1


def test_outside_row_never_counts_in_u(tmp_path):
    lp = Loop(tmp_path)
    round2(lp, rows=ONE_BLOCKER)
    new = {
        "grade": "CRITICAL",
        "anchor": "Logs are kept for seven days.",
        "finding": "x",
        "wrong_outcome": "y",
    }
    code, out = verify(
        lp, {"answers": [ans("R1", "resolved", FIX_EV)], "new_rows": [new]}
    )
    assert code == 0
    row = by_id(lp.state())[out["new_rows"][0]]
    assert (
        row["scope"] == "outside"
        and row["status"] == "deferred"
        and row["blocking"] is False
    )
    assert lp.close(lp.report("r2.md"))[1]["loop_decision"] == "PASS"


def test_child_row_blocks_and_keeps_continue(tmp_path):
    lp = Loop(tmp_path)
    round2(lp, rows=ONE_BLOCKER)
    child = {
        "grade": "CRITICAL",
        "anchor": FIX_EV,
        "finding": "twice is not justified",
        "parent": "R1",
    }
    code, out = verify(
        lp,
        {
            "answers": [ans("R1", "resolved", FIX_EV, touched_ok="no")],
            "new_rows": [child],
        },
    )
    assert code == 0, out
    row = by_id(lp.state())[out["new_rows"][0]]
    assert (
        row["scope"] == "in"
        and row["origin"] == "changed"
        and row["caused_by"] == ["R1"]
    )
    assert row["blocking"] is True and row["status"] == "open"
    assert lp.close(lp.report("r2.md"))[1]["loop_decision"] == "CONTINUE"


def test_touched_ok_no_without_child_refused(tmp_path):
    lp = Loop(tmp_path)
    round2(lp, rows=ONE_BLOCKER)
    code, out = verify(
        lp, {"answers": [ans("R1", "resolved", FIX_EV, touched_ok="no")]}
    )
    assert code == 2 and out["error"] == "E-INCOMPLETE"


def _dispute_loop(lp: Loop, ruling: str | None):
    round2(lp, rows=ONE_BLOCKER)
    assert (
        verify(lp, {"answers": [ans("R1", "open", FIX_EV, reason="still unbounded")]})[
            0
        ]
        == 0
    )
    assert lp.close(lp.report("r2.md"))[1]["loop_decision"] == "CONTINUE"
    assert (
        lp.answer(
            {
                "claims": [
                    {"row": "R1", "action": "disputed", "reason": "twice is the bound"}
                ]
            }
        )[0]
        == 0
    )
    lp.edit(
        text=lp.doc.read_text().replace("at most twice", "at most twice per request")
    )
    assert lp.begin()[0] == 0
    extra = {"dispute_ruling": ruling} if ruling else {}
    assert (
        verify(
            lp,
            {"answers": [ans("R1", "resolved", "at most twice per request", **extra)]},
        )[0]
        == 0
    )
    return lp.close(lp.report("r3.md"))[1]


def test_unruled_dispute_at_review_3_counts_as_open(tmp_path):
    out = _dispute_loop(Loop(tmp_path), None)
    assert out["loop_decision"] == "ESCALATE" and out["decision"]["U"] == 1
    sub = tmp_path / "ruled"
    sub.mkdir()
    assert _dispute_loop(Loop(sub), "rejected")["loop_decision"] == "PASS"


def test_report_edited_then_close_reappends_then_begin_commits(tmp_path):
    lp = Loop(tmp_path)
    rep = lp.round1()
    rep.write_text(rep.read_text().replace("verdict: FAIL", "verdict: PASS"))
    lp.edit("doc-r2-fix.md")
    code, out = lp.begin()
    assert code == 3 and out["error"] == "E-REPORT-EDITED"
    code, out = lp.close(rep)
    assert code == 0 and out["reappended"] is True
    assert rep.read_text().rstrip("\n").splitlines()[-1] == "verdict: FAIL"
    assert lp.begin()[0] == 0
    code, out = lp.close(rep, seq=lp.seq())
    assert code == 3 and out["error"] == "E-PHASE"  # phase verify, nothing verified yet


def test_close_in_revise_with_intact_tail_is_e_phase(tmp_path):
    lp = Loop(tmp_path)
    rep = lp.round1()
    code, out = lp.close(rep)
    assert out.get("replayed") is True  # identical retry
    rep.write_text(rep.read_text())  # unchanged content, same request
    other = lp.report("other.md")
    code, out = lp.close(other)
    assert code == 3 and out["error"] == "E-PHASE"


def test_flag_in_round_2_does_not_carry_to_round_3(tmp_path):
    lp = Loop(tmp_path)
    lp.round1()
    lp.edit(
        text=(_FIX / "doc-r2-fix.md")
        .read_text()
        .replace("every ten", "x")
        .replace("every hour.\n\n## 3", "every ten minutes.\n\n## 3")
    )
    code, out = lp.begin("--revert-unclaimed")
    assert code == 0 and out["unclaimed"][0]["reverted"] is True
    assert verify(lp, basic_answers())[0] == 0
    assert lp.close(lp.report("r2.md"))[1]["loop_decision"] == "CONTINUE"
    lp.edit(
        text=lp.doc.read_text().replace(
            "every hour.\n\n## 3", "every ten minutes.\n\n## 3"
        )
    )
    code, out = lp.begin()
    assert code == 0 and out["unclaimed"] and out["unclaimed"][0]["reverted"] is False
    assert "every ten minutes." in lp.doc.read_text()


def test_three_review_loop_escalates_cap_and_rows_never_shrink(tmp_path):
    lp = Loop(tmp_path)
    round2(lp)
    grades = {r["id"]: r["grade"] for r in lp.state()["rows"]}
    counts_seen = [len(lp.state()["rows"])]
    assert verify(lp, basic_answers())[0] == 0
    assert lp.close(lp.report("r2.md"))[1]["loop_decision"] == "CONTINUE"
    counts_seen.append(len(lp.state()["rows"]))
    lp.edit(
        text=lp.doc.read_text().replace("at most twice", "at most once")
    )  # touches verified R1
    assert lp.begin()[0] == 0
    assert by_id(lp.state())["R1"]["status"] == "fixed"
    code, out = verify(
        lp,
        {
            "answers": [
                ans("R1", "regressed", "at most once"),
                ans("R2", "open", R2_EV, reason="x"),
                ans("R3", "open", R3_EV, reason="x"),
            ]
        },
    )
    assert code == 0, out
    assert by_id(lp.state())["R1"]["status"] == "reopened"
    rep = lp.report("r3.md")
    code, out = lp.close(rep)
    assert out["loop_decision"] == "ESCALATE"
    assert (
        rep.read_text().rstrip("\n").splitlines()[-1]
        == "loop: ESCALATE (sweep pending)"
    )
    counts_seen.append(len(lp.state()["rows"]))
    assert counts_seen == sorted(counts_seen)
    assert all(
        grades[r["id"]] == r["grade"] for r in lp.state()["rows"] if r["id"] in grades
    )
    code, out = lp.begin()
    assert code == 3 and out["error"] == "E-CAP"


def test_regressed_needs_a_once_verified_row(tmp_path):
    lp = Loop(tmp_path)
    round2(lp)
    code, out = verify(
        lp,
        {"answers": [ans("R1", "regressed", FIX_EV)] + basic_answers()["answers"][1:]},
    )
    assert code == 2 and out["error"] == "E-ILLEGAL"


def test_e_terminal_after_loop_ended_at_review_2(tmp_path):
    lp = Loop(tmp_path)
    round2(lp, rows=ONE_BLOCKER)
    assert verify(lp, {"answers": [ans("R1", "resolved", FIX_EV)]})[0] == 0
    assert lp.close(lp.report("r2.md"))[1]["loop_decision"] == "PASS"
    code, out = lp.begin()
    assert code == 3 and out["error"] == "E-TERMINAL"
    code, out = lp.answer({"claims": []})
    assert code == 3 and out["error"] == "E-TERMINAL"


def test_verify_dry_run_writes_nothing(tmp_path):
    lp = Loop(tmp_path)
    round2(lp)
    rep = lp.report(
        "r2.md", "```ledger-input\n" + json.dumps(basic_answers()) + "\n```\n"
    )
    before = tree_digest(lp.ledger, lp.doc, rep)
    code, out = run(
        tmp_path, "verify", "--doc", "spec.md", "--input", str(rep), "--dry-run"
    )
    assert code == 0 and out["dry_run"] is True and out["counts"]["verified"] == 1
    assert tree_digest(lp.ledger, lp.doc, rep) == before


def test_replayed_close_reappends_a_tail_lost_after_the_commit(tmp_path):
    lp = Loop(tmp_path)
    lp.init()
    lp.find("find-basic.json")
    rep = lp.report("r1.md")
    original = rep.read_text()
    seq = lp.seq()
    assert lp.close(rep, op="c", seq=seq)[0] == 0
    rep.write_text(
        original
    )  # as if the process died after the ledger commit, before the append
    code, out = lp.close(rep, op="c2", seq=seq)
    assert code == 0 and out.get("replayed") is True
    assert rep.read_text().rstrip("\n").splitlines()[-1] == "verdict: FAIL"


def _verified_r1_then_round3(lp: Loop, edit):
    round2(lp)
    assert verify(lp, basic_answers())[0] == 0
    assert lp.close(lp.report("r2.md"))[1]["loop_decision"] == "CONTINUE"
    lp.edit(text=edit(lp.doc.read_text()))
    assert lp.begin()[0] == 0


@pytest.mark.parametrize("result", ["regressed", "open"])
def test_untouched_verified_row_cannot_be_reopened(tmp_path, result):
    lp = Loop(tmp_path)
    _verified_r1_then_round3(
        lp, lambda t: t.replace("for 30 days.", "for 30 days, then purges them.")
    )
    assert by_id(lp.state())["R1"]["status"] == "verified"
    answers = [
        ans("R1", result, FIX_EV, reason="x"),
        ans("R2", "open", R2_EV, reason="x"),
        ans("R3", "resolved", "then purges them"),
    ]
    code, out = verify(lp, {"answers": answers})
    assert code == 2 and out["error"] == "E-NOT-CHANGED"


def test_open_on_a_once_verified_fixed_row_gives_reopened(tmp_path):
    lp = Loop(tmp_path)
    _verified_r1_then_round3(lp, lambda t: t.replace("at most twice", "at most once"))
    assert by_id(lp.state())["R1"]["status"] == "fixed"
    answers = [
        ans("R1", "open", "at most once", reason="once is too few"),
        ans("R2", "open", R2_EV, reason="x"),
        ans("R3", "open", R3_EV, reason="x"),
    ]
    assert verify(lp, {"answers": answers})[0] == 0
    assert by_id(lp.state())["R1"]["status"] == "reopened"


def test_resolved_on_an_unmappable_anchor_is_refused(tmp_path):
    wrapped = "# Spec\n\nThe archive keeps every invoice\nfor seven years after payment.\n\nOther text.\n"
    lp = Loop(tmp_path)
    lp.edit(text=wrapped)
    lp.init()
    lp.find(
        [
            {
                "grade": "CRITICAL",
                "anchor": "The archive keeps every invoice for seven years after payment.",
                "finding": "retention basis missing",
            }
        ]
    )
    lp.close(lp.report())
    lp.edit(text=wrapped.replace("for seven years", "for ten years"))
    assert lp.begin()[0] == 0
    row = by_id(lp.state())["R1"]
    assert row["status"] == "fixed" and row["mappings"][-1]["span"] is None
    code, out = verify(
        lp, {"answers": [ans("R1", "resolved", "for ten years after payment.")]}
    )
    assert code == 2 and out["error"] == "E-ANCHOR"
    assert verify(lp, {"answers": [ans("R1", "cannot-verify")]})[0] == 0


@pytest.mark.parametrize(
    "anchor, code_name",
    [
        ("This sentence is not in the snapshot.", "E-ANCHOR"),
        ("The cache is refreshed every hour.", "E-ANCHOR-AMBIGUOUS"),
    ],
    ids=["missing", "repeated"],
)
def test_verify_new_row_anchor_must_occur_once(tmp_path, anchor, code_name):
    lp = Loop(tmp_path)
    round2(lp, rows=ONE_BLOCKER)
    new = {"grade": "MAJOR", "anchor": anchor, "finding": "x"}
    code, out = verify(
        lp, {"answers": [ans("R1", "resolved", FIX_EV)], "new_rows": [new]}
    )
    assert code == 2 and out["error"] == code_name


# ---------------------------------------------------------------- Task 4


def review2_pass(lp: Loop):
    round2(lp, rows=ONE_BLOCKER)
    assert verify(lp, {"answers": [ans("R1", "resolved", FIX_EV)]})[0] == 0
    assert lp.close(lp.report("r2.md"))[1]["loop_decision"] == "PASS"


def sweep(lp: Loop, rows, report="sweep.md", **kw):
    src = rows if isinstance(rows, Path) else lp.json_input(f"sweep-{lp.n}.json", rows)
    rep = lp.report(report, "# Sweep\n")
    return lp.mut("sweep", "--input", str(src), "--report", str(rep), **kw), rep


def prepare(lp: Loop):
    code, out = lp.mut("sweep", "--prepare")
    assert code == 0, out
    return out


def test_verdict_pending_after_every_terminal_review(tmp_path):
    a = tmp_path / "r1"
    a.mkdir()
    lp = Loop(a)
    lp.round1(rows="find-empty.json")
    assert lp.verdict()[0] == 12
    b = tmp_path / "r2"
    b.mkdir()
    lp = Loop(b)
    review2_pass(lp)
    assert lp.verdict()[0] == 12
    c = tmp_path / "r3"
    c.mkdir()
    lp = Loop(c)
    round2(lp)
    assert verify(lp, basic_answers())[0] == 0
    lp.close(lp.report("r2.md"))
    lp.edit(
        text=lp.doc.read_text().replace(
            "for 30 days.", "for 30 days, then purges them."
        )
    )
    assert lp.begin()[0] == 0
    assert (
        verify(
            lp,
            {
                "answers": [
                    ans("R2", "open", R2_EV, reason="x"),
                    ans("R3", "resolved", "then purges them"),
                ]
            },
        )[0]
        == 0
    )
    assert lp.close(lp.report("r3.md"))[1]["loop_decision"] == "ESCALATE"
    assert lp.verdict()[0] == 12


def test_blocking_sweep_row_escalates_delivery(tmp_path):
    lp = Loop(tmp_path)
    review2_pass(lp)
    prepare(lp)
    (code, out), rep = sweep(lp, json.loads((_FIX / "sweep-rows.json").read_text()))
    assert code == 0, out
    assert out["delivery_outcome"] == "ESCALATE"
    lines = rep.read_text().rstrip("\n").splitlines()
    assert (
        lines[-1] == "verdict: FAIL"
        and "sweep" in lines
        and "review: 4 of 3" not in rep.read_text()
    )
    assert lp.verdict()[0] == 11
    rows = [r for r in lp.state()["rows"] if r["round_found"] == "sweep"]
    assert all(r["status"] == "deferred" for r in rows)
    assert {r["location"] for r in rows} <= {
        "in_claimed_span",
        "in_unclaimed_hunk",
        "outside_hunks",
    }
    assert next(r for r in rows if r["label"] == "S3")["location"] == "in_claimed_span"


@pytest.mark.parametrize("review", [1, 2])
def test_clean_sweep_after_loop_pass_gives_verdict_0(tmp_path, review):
    lp = Loop(tmp_path)
    if review == 1:
        lp.round1(rows="find-empty.json")
    else:
        review2_pass(lp)
    prepare(lp)
    (code, out), rep = sweep(lp, {"rows": []})
    assert code == 0 and out["delivery_outcome"] == "PASS"
    assert rep.read_text().rstrip("\n").splitlines()[-1] == "verdict: PASS"
    assert lp.verdict()[0] == 0


def test_second_sweep_refused(tmp_path):
    lp = Loop(tmp_path)
    lp.round1(rows="find-empty.json")
    prepare(lp)
    assert sweep(lp, {"rows": []})[0][0] == 0
    (code, out), _ = sweep(lp, {"rows": []}, report="again.md")
    assert code == 3 and out["error"] == "E-SWEEP-DONE"


def test_sweep_before_terminal_is_e_phase(tmp_path):
    lp = Loop(tmp_path)
    lp.round1()
    code, out = lp.mut("sweep", "--prepare")
    assert code == 3 and out["error"] == "E-PHASE"


def test_prepare_copies_outside_the_ledger_and_flags_post_terminal_edits(tmp_path):
    lp = Loop(tmp_path)
    lp.round1(rows="find-empty.json")
    lp.edit(text=lp.doc.read_text() + "\nAdded after the loop.\n")
    out = prepare(lp)
    copy = Path(out["copy"])
    assert copy.is_file() and lp.ledger.resolve() not in copy.resolve().parents
    assert copy.read_text() == lp.doc.read_text()
    assert out["post_terminal_edit"] is True
    assert lp.status()["metrics"]["post_terminal_edit"]["changed"] is True


def test_defer_leaves_status_unchanged(tmp_path):
    lp = Loop(tmp_path)
    lp.round1(rows="find-basic.json")
    code, out = lp.mut("defer", "--id", "R1", "--quote", "keep it")
    assert code == 3 and out["error"] == "E-PHASE"
    sub = tmp_path / "t"
    sub.mkdir()
    lp = Loop(sub)
    review2_pass(lp)
    code, out = lp.mut("defer", "--id", "R1", "--quote", "the owner accepts twice")
    assert code == 0 and out["status"] == "verified"
    r1 = by_id(lp.state())["R1"]
    assert (
        r1["status"] == "verified"
        and r1["history"][-1]["quote"] == "the owner accepts twice"
    )


def test_two_claimed_rows_get_separate_claim_bytes(tmp_path):
    lp = Loop(tmp_path)
    round2(lp, fixture="doc-r2-two-rows.md")
    cb = lp.status()["metrics"]["claim_bytes"]
    assert set(cb) == {"R2", "R3"} and len(cb["R2"]) == 1 and len(cb["R3"]) == 1


def test_headline_counts_deferred_outside_and_sweep_rows(tmp_path):
    lp = Loop(tmp_path)
    rows = [
        {
            "grade": "MAJOR",
            "anchor": "It keeps one record per widget.",
            "finding": "identity",
        },
        {
            "grade": "MAJOR",
            "anchor": R1_QUOTE,
            "finding": "no retry budget",
            "wrong_outcome": "retries forever",
        },
    ]
    round2(lp, rows=rows)
    outside = {
        "grade": "CRITICAL",
        "anchor": "Logs are kept for seven days.",
        "finding": "x",
    }
    assert (
        verify(lp, {"answers": [ans("R2", "resolved", FIX_EV)], "new_rows": [outside]})[
            0
        ]
        == 0
    )
    assert lp.close(lp.report("r2.md"))[1]["loop_decision"] == "PASS"
    prepare(lp)
    assert (
        sweep(
            lp, {"rows": [{"grade": "MAJOR", "anchor": R3_EV, "finding": "purge rule"}]}
        )[0][0]
        == 0
    )
    m = lp.status()["metrics"]
    assert (m["U3"], m["W"], m["O"], m["headline_raw"], m["deferred_floor"]) == (
        1,
        1,
        1,
        3,
        1,
    )


def test_challenge_row_counts_once_in_w(tmp_path):
    lp = Loop(tmp_path)
    review2_pass(lp)
    prepare(lp)
    row = {"grade": "MAJOR", "anchor": FIX_EV, "finding": "bound", "challenges": "R1"}
    (code, out), _ = sweep(lp, {"rows": [row]})
    assert code == 0 and out["delivery_outcome"] == "ESCALATE"
    assert lp.status()["metrics"]["W"] == 1


def test_sweep_dry_run_writes_nothing(tmp_path):
    lp = Loop(tmp_path)
    review2_pass(lp)
    prepare(lp)
    src = lp.json_input("s.json", json.loads((_FIX / "sweep-rows.json").read_text()))
    rep = lp.report("sweep.md", "# Sweep\n")
    before = tree_digest(lp.ledger, lp.doc, rep, src)
    code, out = run(
        tmp_path,
        "sweep",
        "--doc",
        "spec.md",
        "--input",
        str(src),
        "--report",
        str(rep),
        "--dry-run",
    )
    assert (
        code == 0 and out["dry_run"] is True and out["delivery_outcome"] == "ESCALATE"
    )
    assert tree_digest(lp.ledger, lp.doc, rep, src) == before


def test_help_lists_every_subcommand():
    text = subprocess.run(
        [sys.executable, str(_SCRIPT), "--help"], capture_output=True, text=True
    ).stdout
    for name in (
        "init",
        "find",
        "answer",
        "begin",
        "verify",
        "close",
        "sweep",
        "status",
        "verdict",
        "revert-unclaimed",
        "defer",
    ):
        assert name in text


# ---------------------------------------------------------------- Task 5

_SKILL_MD = _REPO / "src/superclaude/skills/sc-review-ledger/SKILL.md"


def test_skill_md_names_every_refusal_code_and_subcommand():
    text = _SKILL_MD.read_text()
    assert "name: sc-review-ledger" in text
    codes = set(__import__("re").findall(r'"(E-[A-Z-]+)"', _SCRIPT.read_text()))
    assert codes and not [c for c in sorted(codes) if c not in text]
    for name in (
        "init",
        "find",
        "answer",
        "begin",
        "verify",
        "close",
        "sweep",
        "status",
        "verdict",
        "revert-unclaimed",
        "defer",
    ):
        assert f"`{name}" in text


def test_installer_does_not_treat_the_skill_as_served_by_a_command():
    from superclaude.cli.install_skills import _has_corresponding_command

    assert _has_corresponding_command("sc-review-ledger") is False
