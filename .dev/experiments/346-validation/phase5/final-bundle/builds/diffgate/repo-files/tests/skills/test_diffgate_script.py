"""Tests for the diffgate script (issue #346).

The script is loaded by path, as tests/skills/test_workflow_archive.py does,
and run as a subprocess where an exit code is asserted.
"""

from __future__ import annotations

import ast
import difflib
import importlib.util
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
_SCRIPT = ROOT / "src/superclaude/skills/sc-diffgate/scripts/diffgate.py"
FIX = Path(__file__).resolve().parent / "fixtures" / "diffgate"
_spec = importlib.util.spec_from_file_location("diffgate", _SCRIPT)
dg = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(dg)


def run(*args, cwd=None) -> tuple[int, dict]:
    proc = subprocess.run(
        [sys.executable, str(_SCRIPT), *map(str, args)],
        capture_output=True,
        text=True,
        cwd=cwd,
        env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
    )
    lines = [x for x in proc.stdout.splitlines() if x.strip()]
    assert len(lines) == 1, (
        f"expected one JSON object, got: {proc.stdout!r} {proc.stderr!r}"
    )
    payload = json.loads(lines[0])
    assert payload["exit"] == proc.returncode
    assert {"ok", "exit", "message", "review"} <= set(payload)
    return proc.returncode, payload


def hunks(old: str, new: str, review: int = 2):
    return dg.build_hunks(old, new, review)


# --------------------------------------------------------------------------
# Task 1: stdlib only, CLI skeleton, diff engine, limits, ledger I/O


def test_imports_are_stdlib_only():
    tree = ast.parse(_SCRIPT.read_text(encoding="utf-8"))
    names = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names.update(a.name.split(".")[0] for a in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            names.add(node.module.split(".")[0])
    assert names - {"__future__"} <= set(sys.stdlib_module_names), names


def test_help_exits_zero():
    proc = subprocess.run(
        [sys.executable, str(_SCRIPT), "--help"], capture_output=True, text=True
    )
    assert proc.returncode == 0
    assert "begin" in proc.stdout and "fixcheck" in proc.stdout


def test_constants():
    assert (dg.CAP_REVIEWS, dg.MERGE_GAP, dg.VIA_CAP, dg.FORMAT) == (
        3,
        2,
        2,
        "diffgate/1",
    )
    assert dg.PROFILES["spec-panel"]["sev"] == ("critical", "major", "minor")


def test_whitespace_only_change_gives_no_hunk():
    old = "alpha beta gamma\nsecond line here\n"
    new = "alpha   beta gamma  \nsecond line here\n"
    hs, ignored = hunks(old, new)
    assert hs == [] and len(ignored) == 1


def test_pure_reflow_gives_no_hunk():
    old = "one two three four\nfive six seven\neight nine\n"
    new = "one two three\nfour five six seven eight\nnine\n"
    hs, ignored = hunks(old, new)
    assert hs == [] and ignored


def test_list_merge_reflow_is_structural():
    old = "intro\n- first item text\n- second item text\nend\n"
    new = "intro\n- first item text - second item text\nend\n"
    hs, _ = hunks(old, new)
    assert len(hs) == 1 and hs[0]["structural"] is True
    assert hs[0]["changed"] == [] and hs[0]["removed"] == []


def test_one_changed_word_in_long_line_gives_that_word_only():
    words = [f"w{i:03d}" for i in range(59)] + ["xxxxx"]  # 59*4 + 5 + 59 spaces
    old_line = " ".join(words)
    assert len(old_line) == 300
    new_words = list(words)
    new_words[40] = "CHANGED"
    hs, _ = hunks(old_line + "\n", " ".join(new_words) + "\n")
    assert len(hs) == 1
    assert [s[3] for s in hs[0]["changed"]] == ["CHANGED"]
    line, start, end, text = hs[0]["changed"][0]
    assert " ".join(new_words)[start:end] == "CHANGED" and line == 1


def test_pure_deletion_is_anchorable_on_the_old_side():
    old = "keep one\ndelete this whole line please\nkeep two\n"
    new = "keep one\nkeep two\n"
    hs, _ = hunks(old, new)
    assert len(hs) == 1
    assert hs[0]["changed"] == []
    assert [s[3] for s in hs[0]["removed"]] == [
        "delete",
        "this",
        "whole",
        "line",
        "please",
    ]
    assert hs[0]["removed"][0][0] == 2  # old-side line number


def test_merge_gap_two_merges_three_splits():
    base = [f"line {i} text" for i in range(1, 11)]
    two = list(base)
    two[1], two[3] = "line 2 CHANGED", "line 4 CHANGED"  # lines 2 and 4: 2 apart
    three = list(base)
    three[1], three[4] = "line 2 CHANGED", "line 5 CHANGED"  # lines 2 and 5: 3 apart
    old = "\n".join(base) + "\n"
    h2, _ = hunks(old, "\n".join(two) + "\n")
    h3, _ = hunks(old, "\n".join(three) + "\n")
    assert [h["id"] for h in h2] == ["H2.1"]
    assert [h["id"] for h in h3] == ["H2.1", "H2.2"]
    # the gap line 3 is never eligible
    assert {s[0] for s in h2[0]["changed"]} == {2, 4}


def test_320_line_input_keeps_an_exact_diff():
    # 320 lines alternating two texts, with one line inserted at the top. In
    # the new input (321 lines) both texts are "popular" elements, so the
    # default autojunk=True reports one block replacing every line.
    base = ["row text alpha", "row text beta"] * 160
    new = ["inserted line"] + base
    junk = difflib.SequenceMatcher(None, base, new, autojunk=True).get_opcodes()
    assert junk == [("replace", 0, 320, 0, 321)]  # the default misaligns
    hs, _ = hunks("\n".join(base) + "\n", "\n".join(new) + "\n")
    assert len(hs) == 1 and hs[0]["new"] == [1, 1]
    assert [s[3] for s in hs[0]["changed"]] == ["inserted", "line"]
    assert hs[0]["removed"] == []


def test_hunk_ids_section_and_render_surface():
    old = (FIX / "v1.md").read_text(encoding="utf-8")
    new = (FIX / "v2.md").read_text(encoding="utf-8")
    hs, _ = hunks(old, new)
    assert [h["id"] for h in hs] == ["H2.1", "H2.2", "H2.3"]
    assert hs[1]["section"] == "3. Storage"
    priors = [{"id": "R1.1", "sev": "critical", "at": "12", "text": "price rule"}]
    text = dg.render_surface(2, hs, priors, new, old, owners={"H2.1": ["R1.1"]})
    assert "### H2.1 (section: 2. Requirements; owners: R1.1)" in text
    assert "| R1.1 | critical | 12 | price rule |" in text
    assert "coverage:" in text


def test_surface_warns_above_half_coverage():
    old = "a b\nc d\n"
    new = "x y\nz w\n"
    hs, _ = hunks(old, new)
    assert "warning: above 50%" in dg.render_surface(2, hs, [], new, old)


def test_input_over_the_limits_exits_2(tmp_path):
    big = tmp_path / "big.md"
    big.write_text("x\n" * (dg.MAX_LINES + 5), encoding="utf-8")
    code, out = run("begin", "--dir", tmp_path / "d", "--doc", big)
    assert code == 2 and "limit" in out["message"]
    assert not (tmp_path / "d").exists()
    exact = tmp_path / "exact.md"
    exact.write_text("x\n" * dg.MAX_LINES, encoding="utf-8")
    assert dg.read_text(exact).count("\n") == dg.MAX_LINES  # at the limit, not over
    report = tmp_path / "report.md"
    report.write_text(
        "review: 1 of 3\n## Diffgate findings\n"
        + 'FINDING R1.1 sev=minor at=1 anchor="xxxxxxxxxxxx" :: t\n'
        * (dg.MAX_MACHINE_LINES + 1),
        encoding="utf-8",
    )
    code, out = run("check", "--dir", tmp_path / "d", "--report", report)
    assert code == 2 and "machine line limit" in out["message"]
    assert not (tmp_path / "d").exists()


def test_missing_or_empty_file_exits_3_and_names_it(tmp_path):
    code, out = run("begin", "--dir", tmp_path / "d", "--doc", tmp_path / "nope.md")
    assert code == 3 and "nope.md" in out["message"]
    empty = tmp_path / "empty.md"
    empty.write_text("  \n", encoding="utf-8")
    code, out = run("check", "--dir", tmp_path / "d", "--report", empty)
    assert code == 3 and "empty.md" in out["message"]


def test_usage_error_is_one_json_object(tmp_path):
    code, out = run("begin", "--dir", tmp_path)
    assert code == 2 and "usage" in out["message"]


def test_save_ledger_refuses_symlink_and_leaves_no_temp(tmp_path):
    d = tmp_path / "d"
    d.mkdir()
    target = tmp_path / "elsewhere.json"
    target.write_text("{}", encoding="utf-8")
    (d / "ledger.json").symlink_to(target)
    with pytest.raises(dg.Stop):
        dg.save_ledger(d, {"format": dg.FORMAT})
    assert target.read_text(encoding="utf-8") == "{}"
    assert sorted(p.name for p in d.iterdir()) == ["ledger.json"]


def test_save_ledger_fails_on_a_live_lock(tmp_path):
    d = tmp_path / "d"
    d.mkdir()
    (d / ".lock").write_text(str(os.getpid()), encoding="utf-8")  # a running pid
    with pytest.raises(dg.Stop) as exc:
        dg.save_ledger(d, {"format": dg.FORMAT})
    assert exc.value.code == dg.EXIT_ORDER
    assert sorted(p.name for p in d.iterdir()) == [".lock"]


def test_stale_lock_is_removed_and_reported(tmp_path):
    d = tmp_path / "d"
    d.mkdir()
    proc = subprocess.run(
        [sys.executable, "-c", "import os; print(os.getpid())"],
        capture_output=True,
        text=True,
    )
    dead = int(proc.stdout)  # that process has exited
    (d / ".lock").write_text(str(dead), encoding="utf-8")
    dg.NOTICES.clear()
    dg.save_ledger(d, {"format": dg.FORMAT})
    assert any("stale lock" in n for n in dg.NOTICES)
    assert sorted(p.name for p in d.iterdir()) == ["ledger.json"]
    assert dg.load_ledger(d) == {"format": dg.FORMAT}


def test_fixture_documents_exist():
    for name in ("v1.md", "v2.md", "v3.md"):
        assert (FIX / name).read_text(encoding="utf-8").strip()


# --------------------------------------------------------------------------
# Task 2: report grammar, checker rules C1 to C12, derivation, proxy_all

V1, V2, V3 = ((FIX / f"v{i}.md").read_text(encoding="utf-8") for i in (1, 2, 3))
PRIORS_R1 = [
    {"id": "R1.1", "sev": "critical", "at": [12, 12], "text": "price rule incomplete"},
    {"id": "R1.2", "sev": "major", "at": [19, 19], "text": "retention too short"},
    {"id": "R1.3", "sev": "major", "at": [30, 30], "text": "422 names nothing"},
]
RESOLVED_ALL = (
    "PRIOR R1.1 resolved by=H2.1\nPRIOR R1.2 resolved by=H2.2\n"
    "PRIOR R1.3 resolved by=H2.3\n"
)


def ctx2(**kw):
    base = {
        "review": 2,
        "doc": V2,
        "old": V1,
        "hunks": dg.build_hunks(V1, V2, 2)[0],
        "priors": PRIORS_R1,
    }
    base.update(kw)
    return dg.make_ctx(**base)


def report(n: int, block: str, prose: str = "") -> str:
    return f"# Panel report\n\nreview: {n} of 3\n\n{prose}\n\n## Diffgate findings\n\n{block}"


def rules(errors) -> set:
    return {e["rule"] for e in errors}


def test_valid_report_is_accepted():
    errors, res = dg.evaluate(
        (FIX / "report-good.md").read_text(encoding="utf-8"), ctx2()
    )
    assert errors == [] and res is not None
    assert res["verdict"] == "FAIL" and res["verdict_line"] == "verdict: FAIL"
    assert res["blocking_ids"] == ["R2.1", "R1.3"]
    assert {f["id"]: f["origin"] for f in res["findings"]} == {
        "R2.1": "changed",
        "R2.2": "changed",
    }
    assert res["acceptance"] == "clean" and res["proxy_all"] == 2


def test_anchor_not_on_the_cited_lines_is_rejected():
    errors, res = dg.evaluate(
        (FIX / "report-bad-anchor.md").read_text(encoding="utf-8"), ctx2()
    )
    assert res is None and "C5" in rules(errors)
    assert not any(e["structural"] for e in errors)


def test_quote_on_the_unchanged_occurrence_is_rejected():
    old = "old words only on this line\nfiller line\nthe new rule text here\n"
    new = "the new rule text here\nfiller line\nthe new rule text here\n"
    ctx = dg.make_ctx(
        review=2, doc=new, old=old, hunks=dg.build_hunks(old, new, 2)[0], priors=[]
    )
    line = 'FINDING R2.1 sev=minor at={} hunk=H2.1 anchor="the new rule text here" :: x'
    errors, _ = dg.evaluate(report(2, line.format(1)), ctx)
    assert errors == []
    errors, res = dg.evaluate(report(2, line.format(3)), ctx)
    assert res is None and "C6" in rules(errors)


def test_fabricated_hunk_is_rejected():
    block = (
        RESOLVED_ALL
        + 'FINDING R2.1 sev=minor at=12 hunk=H2.9 anchor="negative or missing with" :: x'
    )
    errors, res = dg.evaluate(report(2, block), ctx2())
    assert res is None and "C6" in rules(errors)


def test_unanchored_critical_is_deferred_and_never_blocking():
    errors, res = dg.evaluate(
        (FIX / "report-unanchored.md").read_text(encoding="utf-8"), ctx2()
    )
    assert errors == []
    assert res["verdict"] == "PASS" and res["blocking"] == 0
    assert [(d["id"], d["sev"], d["reason"]) for d in res["deferred"]] == [
        ("R2.1", "critical", "pre-existing")
    ]
    assert res["acceptance"] == "scoped" and res["proxy_all"] == 1


def test_cites_adds_no_blocker():
    block = (
        RESOLVED_ALL
        + 'FINDING R2.1 sev=critical at=17 cites=R1.1 anchor="Widgets are stored in one table" :: more'
    )
    errors, res = dg.evaluate(report(2, block), ctx2())
    assert errors == [] and res["blocking"] == 0 and res["verdict"] == "PASS"
    assert res["findings"][0]["origin"] == "unchanged"
    on_changed = block.replace(
        'at=17 cites=R1.1 anchor="Widgets are stored in one table"',
        'at=12 cites=R1.1 anchor="negative or missing with"',
    )
    errors, res = dg.evaluate(report(2, on_changed), ctx2())
    assert errors == [] and res["findings"][0]["origin"] == "changed"
    assert {f["origin"] for f in res["findings"]} <= {"changed", "unchanged"}


def test_deferred_blocking_grade_minor_makes_acceptance_scoped():
    block = (
        RESOLVED_ALL
        + 'FINDING R2.1 sev=minor fr=8 at=17 anchor="Widgets are stored in one table" :: g'
    )
    errors, res = dg.evaluate(report(2, block), ctx2())
    assert errors == [] and res["deferred"][0]["reason"] == "pre-existing"
    assert res["acceptance"] == "scoped" and res["proxy_all"] == 0


def test_via_anchor_on_changed_text_is_rejected():
    block = (
        RESOLVED_ALL
        + 'FINDING R2.1 sev=major at=12 via=H2.1 via_quote="or missing with status 400" '
        'anchor="negative or missing with" outcome="x" :: on the changed line'
    )
    errors, res = dg.evaluate(report(2, block), ctx2())
    assert res is None and "C6" in rules(errors)


def test_c3_edited_spec_exits_5_without_an_error_list():
    with pytest.raises(dg.Stop) as exc:
        dg.evaluate(
            report(2, RESOLVED_ALL + "FINDINGS none\n"), ctx2(spec_sha=dg.sha256(V3))
        )
    assert exc.value.code == dg.EXIT_ORDER and "C3" in exc.value.message
    errors, res = dg.evaluate(
        report(2, RESOLVED_ALL + "FINDINGS none\n"), ctx2(spec_sha=dg.sha256(V2))
    )
    assert errors == [] and res["verdict"] == "PASS"


def test_third_via_is_deferred_via_cap():
    via = (
        'FINDING R2.{j} sev=major at=13 via=H2.1 via_quote="or missing with status 400" '
        'anchor="Deleting a widget removes it" outcome="lists go stale" :: v{j}\n'
    )
    block = RESOLVED_ALL + "".join(via.format(j=j) for j in (1, 2, 3))
    errors, res = dg.evaluate(report(2, block), ctx2())
    assert errors == []
    assert [d["id"] for d in res["deferred"] if d["reason"] == "via-cap"] == ["R2.3"]
    assert res["blocking_ids"] == ["R2.1", "R2.2"]
    assert all(f["origin"] == "unchanged" for f in res["findings"])


def test_missing_prior_line_is_rejected():
    block = "PRIOR R1.1 resolved by=H2.1\nPRIOR R1.2 resolved by=H2.2\nFINDINGS none\n"
    errors, res = dg.evaluate(report(2, block), ctx2())
    assert res is None and any(e["rule"] == "C9" and e["id"] == "R1.3" for e in errors)


def test_resolved_without_by_is_rejected():
    block = "PRIOR R1.1 resolved\nPRIOR R1.2 resolved by=H2.2\nPRIOR R1.3 resolved by=H2.3\nFINDINGS none\n"
    errors, res = dg.evaluate(report(2, block), ctx2())
    assert res is None and "C10" in rules(errors)


def test_withdrawn_is_legal_only_after_declined():
    block = (
        "PRIOR R1.1 resolved by=H2.1\n"
        'PRIOR R1.2 withdrawn quote="kept for thirty days" reason="declined: rule exists"\n'
        "PRIOR R1.3 resolved by=H2.3\nFINDINGS none\n"
    )
    errors, res = dg.evaluate(report(2, block), ctx2())
    assert res is None and "C9" in rules(errors)
    errors, res = dg.evaluate(report(2, block), ctx2(declined={"R1.2"}))
    assert errors == [] and res["verdict"] == "PASS"
    assert res["acceptance"] == "scoped" and res["proxy_all"] == 1


def test_major_with_dash_outcome_is_minor():
    block = (
        RESOLVED_ALL
        + 'FINDING R2.1 sev=major at=12 hunk=H2.1 anchor="negative or missing with" outcome="-" :: x'
    )
    errors, res = dg.evaluate(report(2, block), ctx2())
    assert errors == [] and res["blocking"] == 0 and res["verdict"] == "PASS"
    assert res["findings"][0]["demoted"] is True


def test_prose_id_missing_from_the_block_is_structural():
    errors, res = dg.evaluate(
        (FIX / "report-structural.md").read_text(encoding="utf-8"), ctx2()
    )
    assert res is None
    assert any(e["structural"] and e["rule"] == "C2b" for e in errors)
    errors, res = dg.evaluate("review: 2 of 3\nno block here\n", ctx2(), degrade=True)
    assert res is None and any(e["structural"] for e in errors)


def test_findings_none_passes_when_no_prior_blocker_is_open():
    errors, res = dg.evaluate(
        report(1, "FINDINGS none\n"), dg.make_ctx(review=1, doc=V1)
    )
    assert errors == [] and res["verdict"] == "PASS" and res["blocking"] == 0


def test_review_one_critical_without_hunk_blocks_and_is_never_deferred():
    line = 'FINDING R1.1 sev=critical at=12 anchor="price is negative with status 400" :: x'
    errors, res = dg.evaluate(report(1, line), dg.make_ctx(review=1, doc=V1))
    assert errors == []
    assert res["blocking"] == 1 and res["verdict"] == "FAIL" and res["deferred"] == []
    assert res["findings"][0]["origin"] == "full"
    for extra in ("hunk=H1.1", "cites=R0.1"):
        bad = line.replace("at=12", f"at=12 {extra}")
        errors, res = dg.evaluate(report(1, bad), dg.make_ctx(review=1, doc=V1))
        assert res is None and "C2" in rules(errors)


def test_review_one_degraded_finding_keeps_its_grade():
    line = 'FINDING R1.1 sev=critical at=13 anchor="price is negative with status 400" :: x'
    errors, res = dg.evaluate(
        report(1, line), dg.make_ctx(review=1, doc=V1), degrade=True
    )
    assert "C5" in rules(errors)
    assert res["deferred"] == [] and res["blocking"] == 1 and res["degraded"] is True
    assert res["findings"][0]["unanchored"] is True


def test_review_two_all_resolved_with_findings_none_passes():
    errors, res = dg.evaluate(report(2, RESOLVED_ALL + "FINDINGS none\n"), ctx2())
    assert errors == [] and res["verdict"] == "PASS"
    errors, res = dg.evaluate(report(2, "FINDINGS none\n"), ctx2())
    assert res is None and "C9" in rules(errors)


def test_side_old_numbers_over_the_previous_snapshot():
    old = "keep one\ndelete this whole line please\nkeep two\n"
    new = "keep one\nkeep two\n"
    ctx = dg.make_ctx(
        review=2,
        doc=new,
        old=old,
        hunks=dg.build_hunks(old, new, 2)[0],
        priors=[{"id": "R1.1", "sev": "critical"}],
    )
    line = (
        "PRIOR R1.1 resolved by=H2.1\n"
        'FINDING R2.1 sev=major at=2 hunk=H2.1 {side}anchor="delete this whole line" '
        'outcome="the rule is gone" :: x'
    )
    errors, res = dg.evaluate(report(2, line.format(side="side=old ")), ctx)
    assert errors == [] and res["blocking_ids"] == ["R2.1"]
    errors, res = dg.evaluate(report(2, line.format(side="")), ctx)
    assert res is None and "C5" in rules(errors)


def test_prose_may_name_earlier_review_ids():
    prose = "R1.2 (blocking, now fixed) and R1.4 (a review-1 minor) were re-read."
    errors, res = dg.evaluate(
        report(2, RESOLVED_ALL + "FINDINGS none\n", prose), ctx2()
    )
    assert errors == [] and res["verdict"] == "PASS"


def test_degraded_report_defers_and_opens():
    text = (FIX / "report-degraded.md").read_text(encoding="utf-8")
    errors, res = dg.evaluate(text, ctx2())
    assert res is None and errors
    errors, res = dg.evaluate(text, ctx2(), degrade=True)
    assert res["degraded"] is True
    assert [(d["id"], d["reason"]) for d in res["deferred"]] == [("R2.1", "unanchored")]
    assert {p["id"]: p["status"] for p in res["priors"]}["R1.2"] == "open"


def test_proxy_all_counts_deferred_demoted_and_withdrawn():
    block = (
        "PRIOR R1.1 resolved by=H2.1\n"
        'PRIOR R1.2 withdrawn quote="kept for thirty days" reason="declined"\n'
        "PRIOR R1.3 resolved by=H2.3\n"
        'FINDING R2.1 sev=critical at=17 anchor="Widgets are stored in one table" :: d\n'
        'FINDING R2.2 sev=major at=12 hunk=H2.1 anchor="negative or missing with" outcome="-" :: m\n'
    )
    errors, res = dg.evaluate(report(2, block), ctx2(declined={"R1.2"}))
    assert errors == []
    assert res["blocking"] == 0 and res["proxy_ids"] == ["R1.2", "R2.1", "R2.2"]


def test_proxy_all_is_cumulative_over_the_loop():
    r1 = report(
        1,
        'FINDING R1.1 sev=critical at=12 anchor="price is negative with status 400" :: c\n'
        'FINDING R1.2 sev=major at=19 anchor="kept for seven days" outcome="-" :: m\n',
    )
    _, res1 = dg.evaluate(r1, dg.make_ctx(review=1, doc=V1))
    assert res1["blocking_ids"] == ["R1.1"] and set(res1["held"]) == {"R1.2"}
    r2 = report(
        2,
        "PRIOR R1.1 resolved by=H2.1\n"
        'FINDING R2.1 sev=critical at=17 anchor="Widgets are stored in one table" :: d\n',
    )
    _, res2 = dg.evaluate(
        r2, ctx2(priors=[PRIORS_R1[0]], held=res1["held"], scoped=res1["scoped"])
    )
    assert set(res2["held"]) == {"R1.2", "R2.1"}
    ctx3 = dg.make_ctx(
        review=3,
        doc=V3,
        old=V2,
        hunks=dg.build_hunks(V2, V3, 3)[0],
        priors=[],
        held=res2["held"],
        scoped=res2["scoped"],
    )
    _, res3 = dg.evaluate(report(3, "FINDINGS none\n"), ctx3)
    assert res3["verdict"] == "PASS" and res3["blocking"] == 0
    assert res3["proxy_ids"] == ["R1.2", "R2.1"] and res3["acceptance"] == "scoped"


def test_report_fixtures_exist():
    for name in ("good", "bad-anchor", "unanchored", "structural", "degraded"):
        assert (FIX / f"report-{name}.md").read_text(encoding="utf-8").strip()


# --------------------------------------------------------------------------
# Task 3: fix map rules M1 to M3

SHA2 = dg.sha256(V2)


def fix_hunks():
    return dg.build_hunks(V1, V2, 2)[0]


def fixmap(*lines, sha=SHA2) -> str:
    return "\n".join([f"doc_sha: {sha}", *lines]) + "\n"


def test_fixmap_hunk_with_two_blocking_owners_is_accepted():
    m = fixmap("H2.1 R1.1,R1.2", "H2.2 R1.2", "H2.3 R1.3")
    res = dg.check_fixmap(m, fix_hunks(), ["R1.1", "R1.2", "R1.3"], SHA2)
    assert res["accepted"] and res["owners"]["H2.1"] == ["R1.1", "R1.2"]
    assert res["hunks_by_id"]["R1.2"] == ["H2.1", "H2.2"]
    assert res["bytes_by_id"]["R1.1"] > 0


def test_fixmap_with_a_stale_doc_sha_is_rejected():
    m = fixmap("H2.1 R1.1", "H2.2 R1.2", "H2.3 R1.3", sha=dg.sha256(V1))
    res = dg.check_fixmap(m, fix_hunks(), ["R1.1", "R1.2", "R1.3"], SHA2)
    assert not res["accepted"] and res["stale"]


def test_fixmap_hunk_owned_only_by_a_minor_is_unmapped():
    m = fixmap("H2.1 R1.1", "H2.2 R1.4", "H2.3 R1.3", "declined R1.2 not a defect")
    res = dg.check_fixmap(m, fix_hunks(), ["R1.1", "R1.2", "R1.3"], SHA2)
    assert not res["accepted"] and res["unmapped"] == ["H2.2"]
    assert any(e.startswith("M1") for e in res["errors"])


def test_fixmap_blocking_id_without_hunk_or_decline_is_rejected():
    m = fixmap("H2.1 R1.1", "H2.2 R1.1", "H2.3 R1.3")
    res = dg.check_fixmap(m, fix_hunks(), ["R1.1", "R1.2", "R1.3"], SHA2)
    assert not res["accepted"] and any("M2: R1.2" in e for e in res["errors"])
    ok = dg.check_fixmap(
        m + "declined R1.2 the cited rule does not exist\n",
        fix_hunks(),
        ["R1.1", "R1.2", "R1.3"],
        SHA2,
    )
    assert ok["accepted"] and ok["declined"] == {
        "R1.2": "the cited rule does not exist"
    }


def test_fixmap_unknown_hunk_or_id_is_rejected():
    blocking = ["R1.1", "R1.2", "R1.3"]
    m = fixmap("H2.1 R1.1", "H2.2 R1.2", "H2.3 R1.3", "H2.9 R1.1")
    assert any(
        "unknown hunk H2.9" in e
        for e in dg.check_fixmap(m, fix_hunks(), blocking, SHA2)["errors"]
    )
    m = fixmap("H2.1 R1.1", "H2.2 R1.2", "H2.3 R1.3", "declined R1.7 gone")
    res = dg.check_fixmap(m, fix_hunks(), blocking, SHA2)
    assert not res["accepted"] and any("R1.7" in e for e in res["errors"])


def test_inline_tags_prefill_the_candidate_lines():
    cand = dg.candidates(fix_hunks())
    assert cand == {"H2.1": ["R1.1"], "H2.2": ["R1.2"], "H2.3": ["R1.3"]}
    text = dg.candidate_map(fix_hunks(), SHA2)
    assert text.splitlines() == [
        f"doc_sha: {SHA2}",
        "H2.1 R1.1",
        "H2.2 R1.2",
        "H2.3 R1.3",
    ]
    res = dg.check_fixmap(text, fix_hunks(), ["R1.1", "R1.2", "R1.3"], SHA2)
    assert res["accepted"]


def test_fixmap_block_inside_a_disposition_file():
    disposition = (
        "# Disposition\n\n| finding | action |\n|---|---|\n| R1.1 | applied H2.9 |\n\n"
        "## Diffgate fixmap\n\n```text\n"
        + fixmap("H2.1 R1.1", "H2.2 R1.2", "H2.3 R1.3")
        + "```\n\n## Notes\n\nH2.9 R1.7 is prose, not a map line.\n"
    )
    res = dg.check_fixmap(disposition, fix_hunks(), ["R1.1", "R1.2", "R1.3"], SHA2)
    assert res["accepted"], res["errors"]


# --------------------------------------------------------------------------
# Task 4: begin, check, fixcheck, status, replay, dry runs, the flg-r1 loop

FLG = FIX / "flg-r1"


def snapshot_tree(root: Path) -> dict:
    out = {}
    for p in sorted(root.rglob("*")):
        if p.is_file():
            st = p.stat()
            out[str(p.relative_to(root))] = (
                st.st_size,
                st.st_mtime_ns,
                dg.sha256(p.read_text(encoding="utf-8", errors="replace")),
            )
    return out


class Loop:
    """A loop directory under tmp_path driven through the subprocess interface."""

    def __init__(self, tmp_path: Path, v1: str = V1):
        self.root = tmp_path
        tmp_path.mkdir(parents=True, exist_ok=True)
        self.d = tmp_path / "dg"
        self.spec = tmp_path / "spec.md"
        self.spec.write_text(v1, encoding="utf-8")

    def doc(self, text: str) -> None:
        self.spec.write_text(text, encoding="utf-8")

    def file(self, name: str, text: str) -> Path:
        p = self.root / name
        p.write_text(text, encoding="utf-8")
        return p

    def begin(self, n=None):
        extra = ["--expect-round", n] if n is not None else []
        return run("begin", "--dir", self.d, "--doc", self.spec, *extra, cwd=self.root)

    def check(self, text: str, name="report.md", dry=False):
        p = self.file(name, text)
        return run(
            "check",
            "--dir",
            self.d,
            "--report",
            p,
            *(["--dry-run"] if dry else []),
            cwd=self.root,
        )

    def fixcheck(self, map_text=None, dry=False):
        args = ["fixcheck", "--dir", self.d, "--doc", self.spec]
        if map_text is not None:
            args += ["--map", self.file("disposition.md", map_text)]
        return run(*args, *(["--dry-run"] if dry else []), cwd=self.root)

    def status(self):
        return run("status", "--dir", self.d, cwd=self.root)


R1_REPORT = report(
    1,
    'FINDING R1.1 sev=critical at=12 anchor="price is negative with status 400" :: c\n'
    'FINDING R1.2 sev=major at=19 anchor="kept for seven days" outcome="audits fail" :: m\n'
    'FINDING R1.3 sev=major at=30 anchor="rejected with status 422" outcome="clients guess" :: m\n',
)
MAP_R1 = fixmap("H2.1 R1.1", "H2.2 R1.2", "H2.3 R1.3")


def loop_at_review_two(tmp_path) -> Loop:
    lp = Loop(tmp_path)
    assert lp.begin(1)[0] == 0
    assert lp.check(R1_REPORT)[0] == 0
    lp.doc(V2)
    assert lp.fixcheck(MAP_R1)[0] == 0
    assert lp.begin(2)[0] == 0
    return lp


def test_begin_review_one_writes_snapshot_and_no_surface(tmp_path):
    lp = Loop(tmp_path)
    code, out = lp.begin(1)
    assert code == 0 and out["review"] == 1 and out["surface"] is None
    assert sorted(p.name for p in lp.d.iterdir()) == ["doc-r1.md", "ledger.json"]
    assert lp.status()[1]["state"] == "open"


def test_begin_review_two_needs_an_accepted_fix_map(tmp_path):
    lp = Loop(tmp_path)
    lp.begin(1)
    assert lp.begin(2)[0] == 5  # no accepted check yet
    lp.check(R1_REPORT)
    lp.doc(V2)
    code, out = lp.begin(2)
    assert code == 5 and "fix map" in out["message"]
    assert lp.fixcheck(fixmap("H2.1 R1.1", "H2.2 R1.2", "H2.3 R1.4"))[0] == 1
    code, out = lp.begin(2)  # a rejected fix map is no accepted fix map
    assert code == 5 and "fix map" in out["message"]
    assert lp.fixcheck(MAP_R1)[0] == 0
    # begin re-runs the fix-map check authoritatively: a recorded map that no
    # longer owns every hunk exits 1 and opens nothing
    path = lp.d / "ledger.json"
    led = json.loads(path.read_text(encoding="utf-8"))
    led["reviews"]["1"]["fix"]["map"] = fixmap("H2.1 R1.1", "H2.2 R1.2")
    path.write_text(json.dumps(led), encoding="utf-8")
    code, out = lp.begin(2)
    assert code == 1 and out["unmapped"] == ["H2.3"]
    assert not (lp.d / "doc-r2.md").exists()


def test_spec_edited_after_fixcheck_makes_begin_exit_5(tmp_path):
    lp = Loop(tmp_path)
    lp.begin(1)
    lp.check(R1_REPORT)
    lp.doc(V2)
    assert lp.fixcheck(MAP_R1)[0] == 0
    assert lp.status()[1]["state"] == "fixed"
    lp.doc(V2 + "\nA late edit.\n")
    assert lp.begin(2)[0] == 5


def test_check_on_an_edited_spec_exits_5_without_reject_file(tmp_path):
    lp = Loop(tmp_path)
    lp.begin(1)
    lp.doc(V2)
    code, _ = lp.check(R1_REPORT)
    assert code == 5 and not list(lp.d.glob("reject-r*.txt"))


def test_fourth_review_and_review_after_pass_exit_4(tmp_path):
    lp = Loop(tmp_path)
    lp.begin(1)
    code, out = lp.check(report(1, "FINDINGS none\n"))
    assert code == 0 and out["verdict"] == "PASS" and out["halt"] == "pass"
    code, out = lp.begin(2)
    assert code == 4 and out["halt"] == "pass"
    lp2 = loop_at_review_two(tmp_path / "b")
    lp2.check(
        report(
            2,
            'PRIOR R1.1 open quote="or missing"\nPRIOR R1.2 resolved by=H2.2\nPRIOR R1.3 resolved by=H2.3\nFINDINGS none\n',
        )
    )
    lp2.doc(V3)
    assert lp2.fixcheck(fixmap("H3.1 R1.1", "H3.2 R1.1", sha=dg.sha256(V3)))[0] == 0
    assert lp2.begin(3)[0] == 0
    code, out = lp2.check(
        report(3, 'PRIOR R1.1 open quote="or missing"\nFINDINGS none\n')
    )
    assert code == 0 and out["verdict"] == "FAIL" and out["halt"] == "escalate"
    code, out = lp2.begin(4)
    assert code == 4 and out["halt"] == "escalate"


def test_wrong_expect_round_exits_5(tmp_path):
    lp = Loop(tmp_path)
    assert lp.begin(2)[0] == 5
    lp.begin(1)
    lp.check(R1_REPORT)
    lp.doc(V2)
    lp.fixcheck(MAP_R1)
    assert lp.begin(3)[0] == 5
    assert lp.begin(2)[0] == 0


def test_second_structural_failure_sets_invalid(tmp_path):
    lp = Loop(tmp_path)
    lp.begin(1)
    code, out = lp.check("review: 1 of 3\nno block\n")
    assert code == 1 and out["halt"] is None
    code, out = lp.begin(1)  # one more begin on the same snapshot
    assert code == 0
    code, out = lp.check("review: 1 of 3\nstill no block\n")
    assert code == 1 and out["halt"] == "invalid"
    assert lp.status()[1]["state"] == "invalid"
    assert lp.begin(1)[0] == 4


def test_second_failing_submission_degrades(tmp_path):
    lp = loop_at_review_two(tmp_path)
    bad = (FIX / "report-degraded.md").read_text(encoding="utf-8")
    code, out = lp.check(bad)
    assert code == 1 and (lp.d / "reject-r2.txt").exists()
    code, out = lp.check(bad)
    assert code == 0 and out["degraded"] is True and out["deferred"] == ["R2.1"]


def test_third_failing_fixcheck_records_fix_rejected(tmp_path):
    lp = Loop(tmp_path)
    lp.begin(1)
    lp.check(R1_REPORT)
    lp.doc(V2)
    stale = fixmap("H2.1 R1.1", sha=dg.sha256(V1))
    assert lp.fixcheck(stale, dry=True)[0] == 1  # a dry run is not counted
    assert lp.fixcheck(stale)[0] == 1
    assert lp.fixcheck(stale)[0] == 1
    code, out = lp.fixcheck(stale)
    assert code == 1 and out["halt"] == "escalate" and "fix-rejected" in out["message"]
    led = json.loads((lp.d / "ledger.json").read_text(encoding="utf-8"))
    assert led["reviews"]["1"]["fix"]["fix_rejected"] is True
    _, st = lp.status()
    assert st["state"] == "closed" and st["halt"] == "escalate"
    assert lp.begin(2)[0] == 4


def test_hand_edited_ledger_makes_begin_exit_6(tmp_path):
    lp = Loop(tmp_path)
    lp.begin(1)
    lp.check(R1_REPORT)
    lp.doc(V2)
    lp.fixcheck(MAP_R1)
    path = lp.d / "ledger.json"
    led = json.loads(path.read_text(encoding="utf-8"))
    led["reviews"]["1"]["check"]["result"]["proxy_all"] = 0
    path.write_text(json.dumps(led), encoding="utf-8")
    code, out = lp.begin(2)
    assert code == 6 and "replay" in out["message"]


def test_accepted_fail_exits_0_with_the_verdict_line(tmp_path):
    lp = Loop(tmp_path)
    lp.begin(1)
    code, out = lp.check(R1_REPORT)
    assert code == 0 and out["accepted"] is True
    assert out["verdict_line"] == "verdict: FAIL" and out["blocking"] == 3
    assert out["proxy_all"] == 3
    result = json.loads((lp.d / "result-r1.json").read_text(encoding="utf-8"))
    assert result["proxy_all"] == 3
    brief = (lp.d / "reviser-brief-r1.md").read_text(encoding="utf-8")
    assert "R1.1" in brief and "fixcheck --dry-run" in brief
    close = (lp.d / "close-r1.md").read_text(encoding="utf-8")
    assert close.rstrip().splitlines()[-1] == "verdict: FAIL"


def test_appended_close_block_does_not_break_replay(tmp_path):
    lp = Loop(tmp_path)
    lp.begin(1)
    p = lp.file("report.md", R1_REPORT)
    assert run("check", "--dir", lp.d, "--report", p)[0] == 0
    with p.open("a", encoding="utf-8") as fh:  # the coordinator's append
        fh.write((lp.d / "close-r1.md").read_text(encoding="utf-8") + "\nmore text\n")
    lp.doc(V2)
    lp.fixcheck(MAP_R1)
    code, out = lp.begin(2)
    assert code == 0 and out["hunks"] == ["H2.1", "H2.2", "H2.3"]


def test_degraded_review_replays_as_degraded(tmp_path):
    lp = Loop(tmp_path)
    lp.begin(1)
    bad = R1_REPORT.replace("at=19", "at=20")
    assert lp.check(bad)[0] == 1
    code, out = lp.check(bad)
    assert code == 0 and out["degraded"] is True
    lp.doc(V2)
    assert lp.fixcheck(MAP_R1)[0] == 0
    assert lp.begin(2)[0] == 0


def test_step_order_guards(tmp_path):
    lp = Loop(tmp_path)
    assert lp.check(R1_REPORT)[0] == 5  # no ledger
    assert lp.fixcheck(MAP_R1)[0] == 5  # no ledger
    lp.begin(1)
    assert lp.fixcheck(MAP_R1)[0] == 5  # before an accepted check
    assert lp.check(R1_REPORT)[0] == 0
    before = (lp.d / "result-r1.json").read_bytes()
    code, _ = lp.check(report(1, "FINDINGS none\n"), name="softer.md")
    assert code == 5 and (lp.d / "result-r1.json").read_bytes() == before


def test_deferred_md_keeps_labels_and_the_disclosure_sentence(tmp_path):
    lp = loop_at_review_two(tmp_path)
    code, out = lp.check((FIX / "report-unanchored.md").read_text(encoding="utf-8"))
    assert code == 0 and out["verdict"] == "PASS" and out["acceptance"] == "scoped"
    text = (lp.d / "deferred.md").read_text(encoding="utf-8")
    assert dg.DEFERRED_SENTENCE in text and "| R2.1 | critical | pre-existing |" in text
    close = (lp.d / "close-r2.md").read_text(encoding="utf-8")
    assert (
        "## Deferred (pre-existing, not looped on)" in close and "scoped PASS:" in close
    )


def test_dry_runs_write_nothing(tmp_path):
    lp = Loop(tmp_path)
    lp.begin(1)
    bad = lp.file("bad.md", R1_REPORT.replace("at=19", "at=20"))
    good = lp.file("good.md", R1_REPORT)
    for path, want in ((bad, 1), (good, 0)):
        before = snapshot_tree(tmp_path)
        code, out = run(
            "check", "--dir", lp.d, "--report", path, "--dry-run", cwd=tmp_path
        )
        assert code == want and out["dry_run"] is True
        assert snapshot_tree(tmp_path) == before
    led = json.loads((lp.d / "ledger.json").read_text(encoding="utf-8"))
    assert led["reviews"]["1"]["finding_rejects"] == 0  # not a repair turn
    assert lp.check(R1_REPORT)[0] == 0
    lp.doc(V2)
    disp = lp.file("disposition.md", MAP_R1)
    stale = lp.file("stale.md", fixmap("H2.1 R1.1", sha=dg.sha256(V1)))
    for args, want in (([], 0), (["--map", disp], 0), (["--map", stale], 1)):
        before = snapshot_tree(tmp_path)
        code, out = run(
            "fixcheck",
            "--dir",
            lp.d,
            "--doc",
            lp.spec,
            *args,
            "--dry-run",
            cwd=tmp_path,
        )
        assert code == want and out["dry_run"] is True
        assert snapshot_tree(tmp_path) == before
    code, out = run(
        "fixcheck", "--dir", lp.d, "--doc", lp.spec, "--dry-run", cwd=tmp_path
    )
    assert out["candidates"][1:] == ["H2.1 R1.1", "H2.2 R1.2", "H2.3 R1.3"]


def test_status_is_read_only_and_names_the_next_step(tmp_path):
    lp = Loop(tmp_path)
    assert lp.status()[1]["state"] == "none"
    lp.begin(1)
    before = snapshot_tree(tmp_path)
    code, out = lp.status()
    assert code == 0 and out["state"] == "open" and "check" in out["next"]
    assert snapshot_tree(tmp_path) == before
    (lp.d / ".lock").write_text(str(os.getpid()), encoding="utf-8")
    assert lp.status()[1]["lock"]["running"] is True


def test_spec_unchanged_and_nothing_written_outside_dir(tmp_path):
    lp = Loop(tmp_path)
    outside = {}

    def mark():
        return {
            k: v for k, v in snapshot_tree(tmp_path).items() if not k.startswith("dg/")
        }

    def step(fn, *a):
        nonlocal outside
        spec_before = lp.spec.read_bytes()
        before = mark()
        fn(*a)
        assert lp.spec.read_bytes() == spec_before
        after = mark()
        # only the inputs this test itself wrote may differ outside --dir
        assert {k for k in after if after.get(k) != before.get(k)} <= {
            "report.md",
            "disposition.md",
        }

    step(lp.begin, 1)
    step(lp.check, R1_REPORT)
    step(lp.status)
    lp.doc(V2)
    step(lp.fixcheck, MAP_R1)
    step(lp.begin, 2)


def test_flg_r1_shaped_loop(tmp_path):
    lp = Loop(tmp_path, (FLG / "doc-v1.md").read_text(encoding="utf-8"))
    assert lp.begin(1)[0] == 0
    code, out = lp.check((FLG / "report-r1.md").read_text(encoding="utf-8"))
    assert code == 0 and out["blocking"] == 4 and out["verdict"] == "FAIL"
    lp.doc((FLG / "doc-v2-minorfix.md").read_text(encoding="utf-8"))
    code, out = lp.fixcheck((FLG / "map-r1-minorfix.md").read_text(encoding="utf-8"))
    assert code == 1 and out["unmapped"] == ["H2.5"]
    lp.doc((FLG / "doc-v2.md").read_text(encoding="utf-8"))
    code, out = lp.fixcheck((FLG / "map-r1.md").read_text(encoding="utf-8"))
    assert code == 0 and out["mapped"] == ["H2.1", "H2.2", "H2.3", "H2.4"]
    kept = (lp.d / "fixmap-r1.txt").read_text(encoding="utf-8").splitlines()
    assert kept[0].startswith("doc_sha: ") and kept[1:] == [
        f"H2.{j} R1.{j}" for j in range(1, 5)
    ]
    assert lp.begin(2)[0] == 0
    code, out = lp.check((FLG / "report-r2.md").read_text(encoding="utf-8"))
    assert code == 0 and out["blocking"] == 4
    lp.doc((FLG / "doc-v3.md").read_text(encoding="utf-8"))
    assert lp.fixcheck((FLG / "map-r2.md").read_text(encoding="utf-8"))[0] == 0
    assert lp.begin(3)[0] == 0
    code, out = lp.check((FLG / "report-r3.md").read_text(encoding="utf-8"))
    assert code == 0 and out["verdict"] == "FAIL" and out["halt"] == "escalate"
    assert out["blocking"] == 4 and out["proxy_all"] == 5
    result = json.loads((lp.d / "result-r3.json").read_text(encoding="utf-8"))
    assert {k: len(v) for k, v in result["chains"].items()} == {
        "R3.1": 3,
        "R3.2": 3,
        "R3.3": 3,
        "R3.4": 3,
    }
    assert result["chains"]["R3.1"] == ["R1.1", "R2.1", "R3.1"]
    assert not (lp.d / "reviser-brief-r3.md").exists()
    close = (lp.d / "close-r3.md").read_text(encoding="utf-8")
    for j in range(1, 5):
        assert f"R1.{j} -> R2.{j} -> R3.{j}" in close
    assert "## Deferred (pre-existing, not looped on)" in close
    assert "halt: escalate" in close
    assert close.rstrip().splitlines()[-1] == "verdict: FAIL"
    assert lp.begin(4)[0] == 4
    # the cap does not rest on the closed flag alone: a ledger reopened by
    # hand fails the replay instead of opening a fourth review
    path = lp.d / "ledger.json"
    led = json.loads(path.read_text(encoding="utf-8"))
    led.update(closed=False, halt=None)
    led["reviews"]["3"]["fix"] = {
        "accepted": True,
        "doc_sha": dg.sha256(lp.spec.read_text(encoding="utf-8")),
        "map": "",
        "owners": {},
        "declined": {},
    }
    path.write_text(json.dumps(led), encoding="utf-8")
    code, out = lp.begin(4)
    assert code == 6 and "closed or halt" in out["message"]
    assert not (lp.d / "doc-r4.md").exists()


# --------------------------------------------------------------------------
# Task 5: the sc-diffgate skill contract (expected blocks are literals here)

SKILL_MD = _SCRIPT.parents[1] / "SKILL.md"
SPEC_TABLE = "| Subcommand | Writes | Extra stdout fields |\n|---|---|---|\n| `begin --dir D --doc F [--expect-round N]` | `ledger.json`, `doc-r<N>.md`, `surface-r<N>.md` (N of 2 or more); for N of 2 or more it first re-runs the fix-map check against `doc-r<N-1>.md` and the current spec, and any unmapped hunk exits 1 with the unmapped list and opens nothing | `surface`, `hunks`, `ignored`, `coverage`, `priors` |\n| `check --dir D --report R` | `result-r<N>.json`, `reviser-brief-r<N>.md`, `deferred.md`; or `reject-r<N>.txt` | `accepted`, `verdict`, `verdict_line`, `acceptance` (`clean` or `scoped`), `blocking`, `deferred`, `degraded`, `halt` |\n| `fixcheck --dir D --doc F [--map M]` | ledger fix record; pre-fills map candidates from inline `R<N>.<j>` tags; exits 1 when the map's `doc_sha` line differs from the spec; the third failure in one cycle records `fix-rejected` | `hunks`, `mapped`, `declined`, `withdrawn` candidates, `bytes_by_id`, `hunks_by_id`, `unmapped` |\n| `status --dir D` | nothing | `state` (`open`, `checked`, `fixed`, `closed`, `invalid`), `next` (the one command that should run next) |"
SPEC_EXIT_CODES = "Exit codes: 0 done (includes an accepted review whose verdict is FAIL); 1 input rejected (`check`: bad report; `fixcheck` or `begin`: unmapped or unknown hunks); 2 usage error or an input over the limits; 3 an input file missing, unreadable or empty; 4 loop closed (`halt: pass`, `halt: escalate`, `halt: invalid`); 5 steps out of order (no accepted check or fix map for the current spec hash, spec edited during a review, or `--expect-round` differs); 6 ledger corrupt or disagreeing with the replay of the recorded report."
SPEC_REPORT_BLOCK = 'Report block, under the heading `## Diffgate findings`, one line per item, keyword at column 1:\n\n```text\nPRIOR R1.5 resolved by=H2.2\nPRIOR R1.9 open quote="still lets WC-7 skip the command file"\nPRIOR R1.7 withdrawn quote="..." reason="declined in fixmap-r1.txt: the cited rule does not exist"\nFINDING R2.1 sev=major at=60-63 hunk=H2.2 anchor="appears in that worker\'s worker-read output" outcome="correct launcher runs are recorded as WC-1 not exercised" :: AC-0.4 reads the wrong source\nFINDING R2.2 sev=major at=312 via=H2.3 via_quote="7.2 step 1 --worktree current" anchor="places the worker in the current worktree" outcome="..." :: H2.3 now assumes an own worktree\nFINDING R2.3 sev=minor at=140 cites=R1.9 anchor="..." :: more evidence for R1.9\n```\n'
SPEC_LINE_FORMS = 'Line forms: `PRIOR <id> resolved by=H<k>.<n>`; `PRIOR <id> open quote="..."`; `PRIOR <id> regressed by=H<k>.<n> quote="..."`; `PRIOR <id> withdrawn quote="..." reason="..."`; `FINDING <id> sev=<critical|major|minor> at=<line or a-b> hunk=H<k>.<n> anchor="..." [outcome="..."] :: text`, with optional `via=H<k>.<n> via_quote="..."`, `cites=<id>`, `fr=8|9|10` and `side=old` (a finding that anchors through `via=` or `cites=` omits `hunk=`); or the single line `FINDINGS none`. Quoted values are JSON strings (`json.loads` on the token). `at=` refers to lines of `doc-r<N>.md`, 1-based and inclusive. Finding ids are `R<N>.<j>`, `j` from 1 with no gap. The reviewer writes no `verdict:` line.'


def _flat(text: str) -> str:
    return " ".join(text.split())


def test_skill_frontmatter():
    text = SKILL_MD.read_text(encoding="utf-8")
    head = text.split("---")[1]
    assert "\nname: sc-diffgate\n" in head and "\nallowed-tools: Read, Bash\n" in head
    assert "description:" in head


def test_skill_carries_the_spec_blocks_verbatim():
    flat = _flat(SKILL_MD.read_text(encoding="utf-8"))
    for block in (SPEC_TABLE, SPEC_EXIT_CODES, SPEC_REPORT_BLOCK, SPEC_LINE_FORMS):
        assert _flat(block) in flat


def test_skill_states_the_additions_separately():
    flat = _flat(SKILL_MD.read_text(encoding="utf-8"))
    assert "`check` also prints `proxy_all`, the owner-decision count" in flat
    assert "accept `--dry-run`, which runs every validation of the real call" in flat
    assert "writes no file anywhere" in flat
    assert "## Who runs what" in SKILL_MD.read_text(encoding="utf-8")
    assert (
        "run only the read-only calls `status`, `check --dry-run` and `fixcheck --dry-run`"
        in flat
    )


def test_skill_installs_under_its_own_name():
    from superclaude.cli.install_skill import list_available_skills
    from superclaude.cli.install_skills import _has_corresponding_command

    assert _has_corresponding_command("sc-diffgate") is False
    assert "sc-diffgate" in list_available_skills()


def test_skill_folder_names_no_repository_source_path():
    for path in SKILL_MD.parent.rglob("*"):
        if path.is_file() and "__pycache__" not in path.parts:
            assert "src/superclaude" not in path.read_text(encoding="utf-8"), path
