"""Behaviour tests of src/superclaude/skills/sc-fixcheck/scripts/fixcheck.py (issue #346)."""

import hashlib
import importlib.util
import subprocess
import sys
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parents[2] / "src/superclaude/skills/sc-fixcheck/scripts/fixcheck.py"


def _load():
    old = sys.dont_write_bytecode
    sys.dont_write_bytecode = True  # keep scripts/__pycache__ out of the skill folder
    try:
        spec = importlib.util.spec_from_file_location("fixcheck_under_test", SCRIPT)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    finally:
        sys.dont_write_bytecode = old
    return module


fc = _load()


def sha(data):
    return hashlib.sha256(data.encode() if isinstance(data, str) else data).hexdigest()


def report_text(spec_text, rows, review=1, extra=""):
    body = "\n".join(rows)
    return (
        "# Review\n\nfindings...\n\n```fixbudget\n"
        f"review: {review} of 3\nreviewed_sha256: {sha(spec_text)}\nrefs: SPEC\n"
        f"# id | severity | grade | budget\n{body}\n{extra}```\n\nverdict: FAIL\n"
    )


def ledger_text(report_name, entries, deferred=()):
    out = [f"report: {report_name}"]
    for num, fields in entries:
        out.append(f"## L{num}")
        out.extend(f"{k}: {v}" for k, v in fields.items())
    if deferred:
        out.append("## deferred")
        out.extend(deferred)
    return "# Disposition\n\n```fixledger\n" + "\n".join(out) + "\n```\n"


def run(capsys, *argv):
    code = fc.main([str(a) for a in argv])
    return code, capsys.readouterr().out


def listing(path):
    return sorted(str(p.relative_to(path)) for p in path.rglob("*"))


SPEC = "# Spec\n\nThe service stores records. It keeps a log.\n"


@pytest.fixture
def review_dir(tmp_path):
    spec = tmp_path / "spec.md"
    spec.write_text(SPEC)
    report = tmp_path / "review-1.md"
    report.write_text(report_text(SPEC, ["F1 | MAJOR | blocking | std"]))
    return tmp_path


# --- Task 1: hash, input parsing, ledger lookup, snapshot ---


def test_hash_prints_sha256_of_bytes(tmp_path, capsys):
    f = tmp_path / "a.md"
    f.write_bytes(b"hello\r\nworld\n")
    code, out = run(capsys, "hash", "--file", f)
    assert code == 0
    assert out.strip() == hashlib.sha256(b"hello\r\nworld\n").hexdigest()
    assert len(out.strip()) == 64


def test_hash_via_uv_no_project_isolated_needs_no_superclaude(tmp_path):
    f = tmp_path / "a.md"
    f.write_text("text\n")
    plain = subprocess.run(
        ["uv", "run", "--no-project", "python", "-I", str(SCRIPT), "hash", "--file", str(f)],
        capture_output=True, text=True, check=False,
    )
    assert plain.returncode == 0, plain.stderr
    assert plain.stdout.strip() == hashlib.sha256(b"text\n").hexdigest()
    probe = (
        "import importlib.util, sys\n"
        "sys.dont_write_bytecode = True\n"
        f"spec = importlib.util.spec_from_file_location('fc', {str(SCRIPT)!r})\n"
        "m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)\n"
        f"assert m.main(['hash', '--file', {str(f)!r}]) == 0\n"
        "assert not [k for k in sys.modules if k.split('.')[0] == 'superclaude'], 'superclaude imported'\n"
    )
    iso = subprocess.run(
        ["uv", "run", "--no-project", "python", "-I", "-c", probe],
        capture_output=True, text=True, check=False,
    )
    assert iso.returncode == 0, iso.stderr


def test_missing_and_empty_file_exit_3(tmp_path, capsys):
    assert run(capsys, "hash", "--file", tmp_path / "nope.md")[0] == 3
    empty = tmp_path / "empty.md"
    empty.write_text("  \n")
    assert run(capsys, "hash", "--file", empty)[0] == 3


def test_usage_error_exits_2(capsys):
    assert fc.main(["hash"]) == 2
    assert fc.main(["bogus"]) == 2


def test_no_fixbudget_block_exits_3(review_dir, capsys):
    (review_dir / "review-1.md").write_text("# Review\nno block\n")
    code, _ = run(capsys, "snapshot", "--spec", review_dir / "spec.md", "--report", review_dir / "review-1.md")
    assert code == 3


@pytest.mark.parametrize(
    "rows, extra",
    [
        (["F1 | MAJOR | blocking | override", "F2 | CRITICAL | blocking | override"],
         "override-reason: F1 needs more\noverride-reason: F2 needs more\n"),
        (["F1 | MAJOR | blocking | override"], ""),
        (["F1 | MAJOR | minor | override"], "override-reason: F1 because\n"),
        (["F1 | MAJOR/FR-8 | blocking | gap:2"], "override-reason: F1 because\n"),
        (["F1 | MAJOR | blocking"], ""),
        (["F1 | BIG | blocking | std"], ""),
    ],
    ids=["second-override", "override-no-reason", "override-on-minor", "override-with-gap",
         "short-row", "bad-severity"],
)
def test_bad_fixbudget_rows_exit_3(tmp_path, capsys, rows, extra):
    spec = tmp_path / "spec.md"
    spec.write_text(SPEC)
    report = tmp_path / "review-1.md"
    report.write_text(report_text(SPEC, rows, extra=extra))
    assert run(capsys, "snapshot", "--spec", spec, "--report", report)[0] == 3
    assert not (tmp_path / ".fixcheck").exists()


def test_reviser_brief_id_must_be_blocking(tmp_path, capsys):
    spec = tmp_path / "spec.md"
    spec.write_text(SPEC)
    report = tmp_path / "review-1.md"
    text = report_text(SPEC, ["F1 | MAJOR | blocking | std", "F2 | MAJOR | minor | -"])
    report.write_text(text + "\n> Reviser brief, fix budget on. Fix only these blocking ids: F1, F2. Every other\n")
    assert run(capsys, "snapshot", "--spec", spec, "--report", report)[0] == 3
    report.write_text(text + "\n> Reviser brief, fix budget on. Fix only these blocking ids: F1. Every other\n")
    assert run(capsys, "snapshot", "--spec", spec, "--report", report)[0] == 0


def test_grade_conflict_is_budget_zero_not_error():
    fb = fc.parse_fixbudget(report_text(SPEC, ["F3 | MAJOR/FR-8 | minor | -", "F4 | CRITICAL | minor | -"]))
    for fid in ("F3", "F4"):
        row = fb["rows"][fid]
        assert row.conflict is True
        assert row.cls == "m"
        assert set(row.limits().values()) == {0}


def test_ledger_lookup_finds_the_single_matching_file(review_dir):
    (review_dir / "disposition.md").write_text(
        ledger_text("review-1.md", [(1, {"finding": "F1", "op": "delete", "old": "It keeps a log."})])
    )
    (review_dir / "other.md").write_text(ledger_text("review-0.md", [(1, {"finding": "F1", "op": "delete", "old": "x"})]))
    assert fc.find_ledger(review_dir / "review-1.md").name == "disposition.md"


@pytest.mark.parametrize("count", [0, 2])
def test_ledger_lookup_zero_or_two_matches_exit_3(review_dir, count):
    for i in range(count):
        (review_dir / f"disp-{i}.md").write_text(
            ledger_text("review-1.md", [(1, {"finding": "F1", "op": "delete", "old": "It keeps a log."})])
        )
    with pytest.raises(fc.FixcheckError) as err:
        fc.find_ledger(review_dir / "review-1.md")
    assert err.value.code == 3


@pytest.mark.parametrize(
    "fields",
    [
        {"finding": "F1", "op": "move", "old": "x", "new": "y"},
        {"finding": "F1", "op": "add", "anchor": "x", "new": "y"},
        {"finding": "F1", "op": "replace", "new": "y"},
        {"finding": "F1", "op": "delete", "old": "x", "depends": "L9"},
    ],
    ids=["bad-op", "add-without-considered", "replace-without-old", "unknown-depends"],
)
def test_malformed_ledger_exit_3(fields):
    with pytest.raises(fc.FixcheckError) as err:
        fc.parse_ledger(ledger_text("review-1.md", [(1, fields)]))
    assert err.value.code == 3


def test_ledger_parses_entries_and_deferred():
    led = fc.parse_ledger(ledger_text(
        "review-1.md",
        [(1, {"finding": "F1", "op": "add", "anchor": "It keeps a log.", "new": "Logs rotate daily.",
              "considered": "nothing to delete"}),
         (2, {"finding": "F2", "op": "narrow", "old": "The service stores records.", "new": "The service stores",
              "depends": "L1"})],
        deferred=["F7: escalated: needs about 140 words"],
    ))
    assert led["report"] == "review-1.md"
    assert [(e.num, e.finding, e.op) for e in led["entries"]] == [(1, "F1", "add"), (2, "F2", "narrow")]
    assert led["deferred"] == {"F7": "needs about 140 words"}


def test_snapshot_stale_spec_exits_4_and_writes_nothing(review_dir, capsys):
    (review_dir / "spec.md").write_text(SPEC + "changed\n")
    before = listing(review_dir)
    code, _ = run(capsys, "snapshot", "--spec", review_dir / "spec.md", "--report", review_dir / "review-1.md")
    assert code == 4
    assert listing(review_dir) == before


def test_snapshot_writes_exactly_base_n(review_dir, capsys):
    before = listing(review_dir)
    code, _ = run(capsys, "snapshot", "--spec", review_dir / "spec.md", "--report", review_dir / "review-1.md")
    assert code == 0
    assert sorted(set(listing(review_dir)) - set(before)) == [".fixcheck", ".fixcheck/base-1.md"]
    assert (review_dir / ".fixcheck/base-1.md").read_text() == SPEC


# --- Task 2: diffing, attribution, scoring and the check report ---

BASE = """# Service spec

## Storage

The service stores each record in the primary database table. Records are written once and read many times.

The cache layer keeps recent records in memory for faster reads. Old entries leave the cache after one hour.

Backups run at night on a separate host machine.

| field | type |
|---|---|
| id | integer |
| name | text |

## Logging

The service writes one log line per request. Log lines go to standard output.
"""
CACHE = "The cache layer keeps recent records in memory for faster reads."
OLD = "Old entries leave the cache after one hour."
BACKUP = "Backups run at night on a separate host machine."
LOGOUT = "Log lines go to standard output."
MAJOR = "F1 | MAJOR | blocking | std"


def filler(n, stem="filler"):
    return " ".join(f"{stem}{i}" for i in range(n))


def case(tmp_path, revised, rows, entries, deferred=(), base=BASE):
    (tmp_path / "base.md").write_text(base)
    (tmp_path / "spec.md").write_text(revised)
    (tmp_path / "review-1.md").write_text(report_text(base, rows))
    (tmp_path / "disposition.md").write_text(ledger_text("review-1.md", entries, deferred))
    return tmp_path


def check(d, capsys, *extra):
    return run(capsys, "check", "--baseline", d / "base.md", "--revised", d / "spec.md",
               "--report", d / "review-1.md", *extra)


def finding_line(out, fid):
    return next(line for line in out.splitlines() if line.startswith(f"finding {fid} "))


def test_clean_in_budget_fix_exits_0(tmp_path, capsys):
    new = "Old entries leave the cache after thirty minutes."
    d = case(tmp_path, BASE.replace(OLD, new), [MAJOR],
             [(1, {"finding": "F1", "op": "replace", "old": OLD, "new": new})])
    code, out = check(d, capsys)
    assert code == 0, out
    assert "status=fixed" in finding_line(out, "F1")
    assert out.strip().endswith("FIXCHECK exit=0")
    assert "result: ok" in out


def test_81_added_words_on_major_exits_1_gross(tmp_path, capsys):
    text = filler(81) + "."
    d = case(tmp_path, BASE.replace(LOGOUT, LOGOUT + "\n\n" + text), [MAJOR],
             [(1, {"finding": "F1", "op": "add", "anchor": LOGOUT, "new": text, "considered": "no delete fits"})])
    code, out = check(d, capsys)
    assert code == 1
    assert "gross 81>80" in finding_line(out, "F1")
    assert "OVER-BUDGET F1" in out


def test_net_51_at_gross_60_exits_1(tmp_path, capsys):
    text = filler(60) + "."
    d = case(tmp_path, BASE.replace(BACKUP, text), [MAJOR],
             [(1, {"finding": "F1", "op": "replace", "old": BACKUP, "new": text})])
    code, out = check(d, capsys)
    line = finding_line(out, "F1")
    assert code == 1
    assert "gross=60" in line and "net 51>50" in line and "gross 60>" not in line


def test_one_word_minor_edit_exits_1(tmp_path, capsys):
    old = "Records are written once and read many times."
    new = "Records are written once and read several times."
    d = case(tmp_path, BASE.replace(old, new), [MAJOR, "F2 | MAJOR | minor | -"],
             [(1, {"finding": "F2", "op": "narrow", "old": old, "new": new})])
    code, out = check(d, capsys)
    assert code == 1
    assert "status=MINOR-EDIT" in finding_line(out, "F2")
    assert "MINOR-EDIT F2" in out


@pytest.mark.parametrize(
    "added, reason",
    [
        ("## Retention", "heading 1>0"),
        ("Each request carries a trace header and a request number.", None),
        ("The service must log errors and must retry writes.", "normative 2>1"),
        ("Retries stop if the queue is full or if the disk fails.", "condition 2>1"),
    ],
    ids=["heading", "control", "second-must", "second-condition"],
)
def test_forbidden_elements_each_have_their_own_reason(tmp_path, capsys, added, reason):
    d = case(tmp_path, BASE.replace(LOGOUT, LOGOUT + "\n\n" + added), [MAJOR],
             [(1, {"finding": "F1", "op": "add", "anchor": LOGOUT, "new": added, "considered": "nothing to cut"})])
    code, out = check(d, capsys)
    if reason is None:
        assert code == 0, out
    else:
        assert code == 1, out
        assert reason in finding_line(out, "F1")


def test_new_id_tag_fails_with_id(tmp_path, capsys):
    new = "Old entries leave the cache after one hour (F3)."
    d = case(tmp_path, BASE.replace(OLD, new), [MAJOR],
             [(1, {"finding": "F1", "op": "replace", "old": OLD, "new": new})])
    code, out = check(d, capsys)
    assert code == 1
    assert "id 1>0" in finding_line(out, "F1")


def test_second_table_row_exits_1(tmp_path, capsys):
    rows = "| owner | string |\n| created | date |"
    d = case(tmp_path, BASE.replace("| name | text |", "| name | text |\n" + rows), [MAJOR],
             [(1, {"finding": "F1", "op": "add", "anchor": "| name | text |", "new": "owner string created date",
                   "considered": "the table needs both"})])
    code, out = check(d, capsys)
    assert code == 1
    assert "table-row 2>1" in finding_line(out, "F1")


def test_unattributed_hunk_exits_1(tmp_path, capsys):
    new = "Old entries leave the cache after thirty minutes."
    revised = BASE.replace(OLD, new).replace(BACKUP, "Backups run at noon on a separate host machine.")
    d = case(tmp_path, revised, [MAJOR], [(1, {"finding": "F1", "op": "replace", "old": OLD, "new": new})])
    code, out = check(d, capsys)
    assert code == 1
    assert "unattributed - revised:9-9" in out and "reason=no ledger entry" in out
    assert "UNATTRIBUTED h2" in out


def test_quote_not_in_baseline_exits_1(tmp_path, capsys):
    new = "Old entries leave the cache after thirty minutes."
    d = case(tmp_path, BASE.replace(OLD, new), [MAJOR],
             [(1, {"finding": "F1", "op": "replace", "old": "Old entries expire after one hour.", "new": new})])
    code, out = check(d, capsys)
    assert code == 1
    assert "reason=quote not in baseline (L1)" in out


def test_short_partial_quote_counts_as_not_in_baseline(tmp_path, capsys):
    old = "The service stores each record in the primary database table."
    new = "The service stores each record in the main database table."
    d = case(tmp_path, BASE.replace(old, new), [MAJOR],
             [(1, {"finding": "F1", "op": "narrow", "old": "stores each record", "new": new})])
    code, out = check(d, capsys)
    assert code == 1
    assert "reason=quote not in baseline (L1)" in out


def test_mislabelled_op_exits_1(tmp_path, capsys):
    new = "Old entries leave the cache after one hour of idle time."
    d = case(tmp_path, BASE.replace(OLD, new), [MAJOR],
             [(1, {"finding": "F1", "op": "narrow", "old": OLD, "new": new})])
    code, out = check(d, capsys)
    assert code == 1
    assert "op L1 narrow!=replace" in out and "MISLABELLED F1" in out


def test_unanswered_blocking_id_does_not_change_exit(tmp_path, capsys):
    new = "Old entries leave the cache after thirty minutes."
    d = case(tmp_path, BASE.replace(OLD, new), [MAJOR, "F5 | MAJOR | blocking | std"],
             [(1, {"finding": "F1", "op": "replace", "old": OLD, "new": new})])
    code, out = check(d, capsys)
    assert code == 0, out
    assert "status=unanswered" in finding_line(out, "F5")


def test_whitespace_only_growth_over_6144_bytes_exits_1(tmp_path, capsys):
    revised = BASE.replace("\n\n", "\n" + " " * 1200 + "\n\n")
    assert len(revised.encode()) - len(BASE.encode()) > 6144
    d = case(tmp_path, revised, [MAJOR], [(1, {"finding": "F1", "op": "delete", "old": OLD})])
    code, out = check(d, capsys)
    assert code == 1
    assert "hunks=0" in out and "RAW-SIZE" in out


def test_hunk_lines_carry_entry_and_range_and_are_deterministic(tmp_path, capsys):
    new1 = "Old entries leave the cache after thirty minutes."
    new2 = "Log lines go to standard error."
    d = case(tmp_path, BASE.replace(OLD, new1).replace(LOGOUT, new2), [MAJOR, "F2 | CRITICAL | blocking | std"],
             [(1, {"finding": "F1", "op": "replace", "old": OLD, "new": new1}),
              (2, {"finding": "F2", "op": "replace", "old": LOGOUT, "new": new2})])
    code1, out1 = check(d, capsys)
    code2, out2 = check(d, capsys)
    assert code1 == code2 == 0
    assert out1 == out2
    assert "h1 L1 F1 revised:7-7 +2/-2" in out1
    assert "h2 L2 F2 revised:18-18 +1/-1" in out1


def test_neighbouring_sentences_are_credited_to_both_entries(tmp_path, capsys):
    new1 = "The cache layer keeps recent records in memory for quicker reads."
    new2 = "Old entries leave the cache after two hours."
    d = case(tmp_path, BASE.replace(CACHE, new1).replace(OLD, new2), [MAJOR, "F2 | MAJOR | blocking | std"],
             [(1, {"finding": "F1", "op": "replace", "old": CACHE, "new": new1}),
              (2, {"finding": "F2", "op": "replace", "old": OLD, "new": new2})])
    code, out = check(d, capsys)
    assert code == 0, out
    assert "h1 L1 F1 revised:7-7" in out and "h2 L2 F2 revised:7-7" in out
    assert "status=fixed" in finding_line(out, "F1") and "status=fixed" in finding_line(out, "F2")


def test_moved_text_counts_zero(tmp_path, capsys):
    para = "The service writes one log line per request. Log lines go to standard output.\n"
    revised = BASE.replace(para, "").replace("## Storage\n", "## Storage\n\n" + para)
    d = case(tmp_path, revised, [MAJOR], [], deferred=["F1: escalated: needs a rule change"])
    code, out = check(d, capsys)
    assert code == 0, out
    assert "hunks=0" in out and "moved=2" in out and "cycle_words=0/600" in out


def test_path_line_token_adds_zero_words(tmp_path, capsys):
    new = "Log lines go to src/log.py:12 standard output."
    d = case(tmp_path, BASE.replace(LOGOUT, new), [MAJOR],
             [(1, {"finding": "F1", "op": "narrow", "old": LOGOUT, "new": new})])
    code, out = check(d, capsys)
    assert code == 0, out
    assert "h1 L1 F1 revised:18-18 +0/-0" in out


def test_delete_over_80_words_is_free_of_the_gross_cap(tmp_path, capsys):
    long = " ".join(f"word{i}" for i in range(90)) + "."
    base = BASE + "\n" + long + "\n"
    d = case(tmp_path, BASE, [MAJOR], [(1, {"finding": "F1", "op": "delete", "old": long})], base=base)
    code, out = check(d, capsys)
    assert code == 0, out
    assert "+0/-90" in out and "status=fixed" in finding_line(out, "F1")


def test_check_with_explicit_ledger_and_lookup_agree(tmp_path, capsys):
    new = "Old entries leave the cache after thirty minutes."
    d = case(tmp_path, BASE.replace(OLD, new), [MAJOR],
             [(1, {"finding": "F1", "op": "replace", "old": OLD, "new": new})])
    assert check(d, capsys) == check(d, capsys, "--ledger", d / "disposition.md")


def test_carried_open_lists_open_critical_and_major(tmp_path, capsys):
    new = "Old entries leave the cache after thirty minutes."
    rows = ["F1 | MAJOR | blocking | std", "F2 | CRITICAL | blocking | std", "F3 | MAJOR | minor | -",
            "F4 | MINOR | minor | -", "F5 | CRITICAL | blocking | std", "F6 | MAJOR/FR-8 | minor | -"]
    d = case(tmp_path, BASE.replace(OLD, new), rows,
             [(1, {"finding": "F5", "op": "replace", "old": OLD, "new": new})],
             deferred=["F1: escalated: needs about 140 words"])
    code, out = check(d, capsys)
    assert code == 0, out
    assert "carried-open: n=4 F1(escalated) F2(unanswered) F3(minor) F6(GRADE-CONFLICT)" in out
    assert "GRADE-CONFLICT F6" in out
    assert "escalated: F1 (needs about 140 words)" in out


def test_plain_check_writes_nothing(tmp_path, capsys):
    new = "Old entries leave the cache after one hour of idle time."
    d = case(tmp_path, BASE.replace(OLD, new), [MAJOR],
             [(1, {"finding": "F1", "op": "narrow", "old": OLD, "new": new})])
    before = {p: p.read_bytes() for p in d.iterdir()}
    listing_before = listing(d)
    check(d, capsys)
    assert listing(d) == listing_before
    assert {p: p.read_bytes() for p in d.iterdir()} == before


def test_check_on_mismatched_baseline_exits_4(tmp_path, capsys):
    d = case(tmp_path, BASE, [MAJOR], [(1, {"finding": "F1", "op": "delete", "old": OLD})])
    (d / "base.md").write_text(BASE + "drift\n")
    assert check(d, capsys)[0] == 4


# --- Task 3: check --enforce ---


def enforce(d, capsys, *extra):
    return check(d, capsys, "--enforce", *extra)


def test_enforce_restores_over_budget_and_unattributed_and_keeps_in_budget(tmp_path, capsys):
    new = "Old entries leave the cache after thirty minutes."
    big = filler(81) + "."
    revised = (BASE.replace(OLD, new).replace(LOGOUT, LOGOUT + "\n\n" + big)
               .replace(BACKUP, "Backups run at noon on a separate host machine."))
    d = case(tmp_path, revised, [MAJOR, "F2 | MAJOR | blocking | std"],
             [(1, {"finding": "F1", "op": "replace", "old": OLD, "new": new}),
              (2, {"finding": "F2", "op": "add", "anchor": LOGOUT, "new": big, "considered": "no cut fits"})])
    code, out = enforce(d, capsys)
    assert code == 0, out
    assert (d / "spec.md").read_text() == BASE.replace(OLD, new)
    assert "ENFORCE reverted=F2 " in out and "restored-baseline=no" in out
    assert "status=reverted" in finding_line(out, "F2") and "status=fixed" in finding_line(out, "F1")


def test_enforce_reverts_depends_partners_whole(tmp_path, capsys):
    new = "Old entries leave the cache after thirty minutes."
    big = filler(81) + "."
    d = case(tmp_path, BASE.replace(OLD, new).replace(LOGOUT, LOGOUT + "\n\n" + big),
             [MAJOR, "F2 | MAJOR | blocking | std"],
             [(1, {"finding": "F1", "op": "replace", "old": OLD, "new": new, "depends": "L2"}),
              (2, {"finding": "F2", "op": "add", "anchor": LOGOUT, "new": big, "considered": "no cut fits"})])
    code, out = enforce(d, capsys)
    assert code == 0, out
    assert (d / "spec.md").read_text() == BASE
    assert "ENFORCE reverted=F1,F2 " in out


def test_second_enforce_changes_nothing(tmp_path, capsys):
    big = filler(81) + "."
    d = case(tmp_path, BASE.replace(LOGOUT, LOGOUT + "\n\n" + big), [MAJOR],
             [(1, {"finding": "F1", "op": "add", "anchor": LOGOUT, "new": big, "considered": "no cut fits"})])
    assert enforce(d, capsys)[0] == 0
    first = (d / "spec.md").read_bytes()
    code, out = enforce(d, capsys)
    assert code == 0
    assert (d / "spec.md").read_bytes() == first
    assert "ENFORCE reverted=- hunks=- restored-baseline=no" in out


def test_enforce_without_ledger_or_with_empty_ledger_exits_3(tmp_path, capsys):
    revised = BASE.replace(OLD, "Old entries leave the cache after thirty minutes.")
    d = case(tmp_path, revised, [MAJOR], [])
    assert enforce(d, capsys)[0] == 3  # ledger block with no entries
    (d / "disposition.md").unlink()
    assert enforce(d, capsys)[0] == 3  # no ledger file at all
    assert (d / "spec.md").read_text() == revised


def test_enforce_on_mismatched_baseline_exits_4_and_leaves_spec(tmp_path, capsys):
    revised = BASE.replace(OLD, "Old entries leave the cache after thirty minutes.")
    d = case(tmp_path, revised, [MAJOR], [(1, {"finding": "F1", "op": "delete", "old": OLD})])
    (d / "base.md").write_text(BASE + "drift\n")
    assert enforce(d, capsys)[0] == 4
    assert (d / "spec.md").read_text() == revised


def paragraphs(prefix, n_paras, n_words):
    return [" ".join(f"{prefix}{p}w{w}" for w in range(n_words)) + "." for p in range(n_paras)]


def test_cycle_cap_reverts_blocking_major_before_critical_largest_first(tmp_path, capsys):
    olds = paragraphs("p", 7, 40)
    sizes = [110, 110, 110, 110, 78, 60, 50]  # F1-F4 CRITICAL (net 70), F5-F7 MAJOR; total 628 > 600
    news = [" ".join(f"n{p}w{w}" for w in range(size)) + "." for p, size in enumerate(sizes)]
    base = "# Doc\n\n" + "\n\n".join(olds) + "\n"
    revised = "# Doc\n\n" + "\n\n".join(news) + "\n"
    rows = [f"F{k} | CRITICAL | blocking | std" for k in range(1, 5)] + \
           [f"F{k} | MAJOR | blocking | std" for k in range(5, 8)]
    entries = [(k + 1, {"finding": f"F{k + 1}", "op": "replace", "old": olds[k], "new": news[k]}) for k in range(7)]
    d = case(tmp_path, revised, rows, entries, base=base)
    code, out = check(d, capsys)
    assert code == 1 and "CYCLE words 628>600" in out, out
    code, out = enforce(d, capsys)
    assert code == 0, out
    assert "ENFORCE reverted=F5 " in out
    assert (d / "spec.md").read_text() == revised.replace(news[4], olds[4])


def test_entries_limit_revert_scores_zero_entries_afterwards(tmp_path, capsys):
    sentences = [CACHE, OLD, BACKUP, LOGOUT, "The service writes one log line per request."]
    revised, entries = BASE, []
    for k, s in enumerate(sentences, 1):
        new = s[:-1] + " today."
        revised = revised.replace(s, new)
        entries.append((k, {"finding": "F1", "op": "replace", "old": s, "new": new}))
    d = case(tmp_path, revised, [MAJOR], entries)
    code, out = check(d, capsys)
    assert code == 1 and "entries 5>4" in finding_line(out, "F1")
    code, out = enforce(d, capsys)
    assert code == 0, out
    assert "entries=0" in finding_line(out, "F1") and "status=reverted" in finding_line(out, "F1")
    code, out = check(d, capsys)
    assert code == 0 and "status=reverted" in finding_line(out, "F1")
    assert (d / "spec.md").read_text() == BASE


def test_enforce_writes_no_file_other_than_the_spec(tmp_path, capsys):
    big = filler(81) + "."
    d = case(tmp_path, BASE.replace(LOGOUT, LOGOUT + "\n\n" + big), [MAJOR],
             [(1, {"finding": "F1", "op": "add", "anchor": LOGOUT, "new": big, "considered": "no cut fits"})])
    before = {p.name: p.read_bytes() for p in d.iterdir()}
    listing_before = listing(d)
    assert enforce(d, capsys)[0] == 0
    assert listing(d) == listing_before
    after = {p.name: p.read_bytes() for p in d.iterdir()}
    assert {k for k in after if after[k] != before[k]} == {"spec.md"}


def test_enforce_write_failure_exits_5_and_leaves_spec(tmp_path, capsys, monkeypatch):
    big = filler(81) + "."
    revised = BASE.replace(LOGOUT, LOGOUT + "\n\n" + big)
    d = case(tmp_path, revised, [MAJOR],
             [(1, {"finding": "F1", "op": "add", "anchor": LOGOUT, "new": big, "considered": "no cut fits"})])
    listing_before = listing(d)

    def refuse(*_):
        raise PermissionError(13, "Permission denied")

    monkeypatch.setattr(fc.os, "replace", refuse)
    assert enforce(d, capsys)[0] == 5
    assert (d / "spec.md").read_text() == revised
    assert listing(d) == listing_before


def test_hash_and_plain_check_are_read_only(tmp_path, capsys):
    """Owner ruling msg_9e319d331e9b: review sessions run only calls that write nothing."""
    new = "Old entries leave the cache after one hour of idle time."
    d = case(tmp_path, BASE.replace(OLD, new), [MAJOR], [(1, {"finding": "F1", "op": "narrow", "old": OLD, "new": new})])
    before = {p: p.read_bytes() for p in d.iterdir()}
    run(capsys, "hash", "--file", d / "spec.md")
    check(d, capsys)
    assert {p: p.read_bytes() for p in d.iterdir()} == before


SENTS = [
    "Alpha nodes hold the primary copy of each shard.",
    "Beta nodes keep a warm replica for reads.",
    "Gamma jobs compact old segments at night.",
    "Delta checks run before each deploy step.",
    "Epsilon tokens expire after a fixed period.",
    "Zeta logs are kept for thirty days.",
    "Eta alerts page the on-call engineer.",
    "Theta dashboards show latency by region.",
]
ROWS = ["| a | one |", "| b | two |"]
FENCE = "```\nuv run thing\n```"
# a fence and a table sit between two paragraphs, so edits reach the lines around both
PROP_BASE = ("# Prop\n\n" + " ".join(SENTS[:4]) + "\n\n" + FENCE + "\n\n| key | value |\n|---|---|\n" + "\n".join(ROWS)
             + "\n\n" + " ".join(SENTS[4:]) + "\n")
VOCAB = ["must", "only", "if", "when", "AC-9", "(F7)", "`grep x | wc`", "## Note", "plain", "words", "here"]


def join_line(text, target):
    """Join the line holding `target` onto the line before it (an undeclared whitespace-only edit)."""
    at = text.find(target)
    if at <= 0 or text[at - 1] != "\n":
        return text
    k = at
    while k and text[k - 1] == "\n":
        k -= 1
    return text[:k] + " " + text[at:]


def random_edit(rng, text, target):
    """Apply one random edit around `target`; return (text, (kind, old, new)) or (text, None) when undeclarable."""
    words = " ".join(rng.choice(VOCAB) for _ in range(rng.randint(1, 60)))
    if target == FENCE:
        return join_line(text, target), None
    if target in ROWS:
        cell = target.split("|")[2].strip()
        kind = rng.choice(["cell", "addrow", "delrow", "join", "cut"])
        if kind == "cell":
            return text.replace(target, target.replace(cell, "changed")), ("replace", target, "changed")
        if kind == "addrow":
            return text.replace(target, target + "\n| z | extra |"), ("add", target, "z extra")
        if kind == "join":
            return join_line(text, target), None
        if kind == "cut":
            return text.replace(target, target.split("|")[1].strip()), None
        return text.replace(target + "\n", ""), ("delete", target, "")
    s = target
    kind = rng.choice(["replace", "narrow", "delete", "add", "prefix", "move", "space", "join", "fence", "stray"])
    if kind == "replace":
        new = s[:-1] + " " + words + "."
    elif kind == "narrow":
        new = " ".join(s.split()[: max(2, len(s.split()) - 3)]) + "."
    elif kind == "delete":
        new = ""
    elif kind == "add":
        new = s + "\n\n" + words + "."
    elif kind == "prefix":
        new = "Plain words here. " + s  # a new sentence at the start of the line, undeclared
        return text.replace(s, new), None
    elif kind == "move":
        return text.replace(s + " ", "").replace(s, "") + "\n" + s + "\n", None
    elif kind == "stray":
        return text.replace(s, s + "\n\n```"), None  # an undeclared fence line mid-text
    elif kind == "fence":
        return text.replace(s, s + "\n\n```"), ("add", s, "```")  # a declared fix that opens an unmatched fence
    elif kind == "join":
        return join_line(text, s), None
    else:
        return text.replace(s, s + " " * rng.randint(1, 4000)), None
    return text.replace(s, new), (kind, s, new)


def kept_slices(d):
    """Check view before --enforce, in the context --enforce judges in (undeclared fence lines removed):
    the revised text of every attributed hunk, and the findings --enforce may revert for a stated reason
    (over budget or minor edit, a depends: entry, a moved unit)."""
    base_data, base_text = fc.read_text(d / "base.md")
    _, rev_text = fc.read_text(d / "spec.md")
    fb = fc.parse_fixbudget((d / "review-1.md").read_text())
    ledger = fc.load_ledger(d / "review-1.md", None)[2]
    rev_text, res, _, _ = fc.remove_stray_fences(base_data, base_text, rev_text, fb, ledger)
    slices = [(h.entry.finding, rev_text[h.r[0].start:h.r[-1].end]) for h in res["hunks"] if h.entry and h.r]
    allowed = {f for f, p in res["per"].items() if p["status"] in ("OVER", "MINOR-EDIT")}
    allowed |= {e.finding for e in ledger["entries"] if e.depends}
    allowed |= {h.entry.finding for h in res["hunks"] if h.entry and (
        any(i in res["moved_b"] for i in range(h.i1, h.i2)) or any(j in res["moved_r"] for j in range(h.j1, h.j2)))}
    fences = {f for f, p in res["per"].items()  # findings whose own hunks change the number of fence lines
              if sum(sum(u.kind == "fence" for u in h.r) - sum(u.kind == "fence" for u in h.b) for h in p["hunks"])}
    return slices, allowed, fences


def test_property_enforce_then_check_exits_0(tmp_path, capsys):
    rng = __import__("random").Random(346)
    for n in range(200):
        d = tmp_path / f"c{n}"
        d.mkdir()
        rows = ["F1 | CRITICAL | blocking | std", "F2 | MAJOR | blocking | std", "F3 | MAJOR | minor | -",
                "F4 | MAJOR/FR-8 | blocking | gap:2"]
        text, entries = PROP_BASE, []
        for target in rng.sample(SENTS + ROWS + [FENCE], rng.randint(1, 4)):
            text, edit = random_edit(rng, text, target)
            if edit is None or rng.random() < 0.15:
                continue  # an edit the ledger does not declare
            kind, old, new = edit
            fields = {"finding": rng.choice(["F1", "F2", "F3", "F4", "F9"]),
                      "op": rng.choice(["delete", "narrow", "replace", "add"]) if rng.random() < 0.2 else kind}
            if fields["op"] == "add":
                fields.update(anchor=old, considered="nothing else fits")
            else:
                fields["old"] = old if rng.random() > 0.1 else "Text that is not in the baseline at all."
            if fields["op"] != "delete":
                fields["new"] = " ".join((new or "gone").split()[:10])
            if entries and rng.random() < 0.2:
                fields["depends"] = f"L{entries[-1][0]}"
            entries.append((len(entries) + 1, fields))
        if not entries:
            entries = [(1, {"finding": "F1", "op": "delete", "old": SENTS[0]})]
        if text == PROP_BASE:
            text += "Extra words appear here.\n"
        case(d, text, rows, entries, base=PROP_BASE)
        before, allowed, fences = kept_slices(d)
        code, out = enforce(d, capsys)
        assert code == 0, (n, out)
        reverted = set(out.split("ENFORCE reverted=", 1)[1].split(" ", 1)[0].split(",")) - {"-"}
        structure = set(out.split(" structure=", 1)[1].split(" ", 1)[0].split(",")) - {"-"}
        recheck = set(out.split(" recheck=", 1)[1].split(" ", 1)[0].split(",")) - {"-"}
        if "restored-baseline=no" in out:
            assert structure <= fences, (n, out)  # a structure revert only hits a finding whose hunks change the fence count
            assert reverted <= allowed | structure | recheck, (n, reverted, allowed, out)  # every revert has a stated reason
            final = (d / "spec.md").read_text()
            for fid, piece in before:
                assert fid in reverted or piece in final, (n, fid, piece, out)  # kept fixes survive byte for byte
        else:
            assert "restored-baseline=yes reason=raw-size" in out, (n, out)
        code, out = check(d, capsys)
        assert code == 0, (n, out)


def test_enforce_keeps_breaks_next_to_a_kept_deletion(tmp_path, capsys):
    """Review r1-1 F1.1: a reverted sentence after a kept deletion keeps its paragraph break."""
    a, b = "Alpha nodes hold the primary copy.", "Beta nodes keep a warm replica."
    g, g2 = "Gamma jobs compact old segments at night.", "Gamma jobs compact old segments."
    base = f"# Doc\n\n{a} {b}\n\n{g}\n"
    big = filler(90) + "."
    d = case(tmp_path, f"# Doc\n\n{big}\n\n{g2}\n",
             [MAJOR, "F2 | MAJOR | blocking | std", "F3 | MAJOR | blocking | std"],
             [(1, {"finding": "F1", "op": "delete", "old": a}),
              (2, {"finding": "F2", "op": "replace", "old": b, "new": big}),
              (3, {"finding": "F3", "op": "narrow", "old": g, "new": g2})], base=base)
    code, out = enforce(d, capsys)
    assert code == 0, out
    assert "ENFORCE reverted=F2 " in out and "restored-baseline=no" in out
    assert (d / "spec.md").read_text() == f"# Doc\n\n{b}\n\n{g2}\n"


def test_enforce_reverts_dependant_of_an_unattributed_entry(tmp_path, capsys):
    """Review r1-1 F1.2: an entry reverted because its hunk is unattributed takes its dependants with it."""
    new1 = "Old entries leave the cache after thirty minutes."
    new2 = "Backups run at noon on a separate host machine."
    d = case(tmp_path, BASE.replace(OLD, new1).replace(BACKUP, new2), [MAJOR, "F2 | MAJOR | blocking | std"],
             [(1, {"finding": "F1", "op": "replace", "old": OLD, "new": new1, "depends": "L2"}),
              (2, {"finding": "F2", "op": "replace", "old": BACKUP, "new": "Words that never appear anywhere."})])
    code, out = enforce(d, capsys)
    assert code == 0, out
    assert "ENFORCE reverted=F1 " in out
    assert (d / "spec.md").read_text() == BASE


def test_enforce_restores_the_baseline_tail(tmp_path, capsys):
    """Review r1-1 F1.3: reverting an appended paragraph restores the baseline's final newline."""
    base = "# Doc\n\nOne para.\n\nTwo para.\n"
    d = case(tmp_path, "# Doc\n\nOne para.\n\nTwo para.\n\nNew para here.", [MAJOR],
             [(1, {"finding": "F1", "op": "delete", "old": "One para."})], base=base)
    assert enforce(d, capsys)[0] == 0
    assert (d / "spec.md").read_text() == base


def test_enforce_reverts_an_unpaired_neighbour_edit_without_duplicating_it(tmp_path, capsys):
    """Property seed 1 case 159: an undeclared rewrite next to a declared fix is reverted in place."""
    zeta, eta = "Zeta logs are kept for thirty days.", "Eta alerts page the on-call engineer."
    revised = PROP_BASE.replace(zeta, "Zeta logs are kept.").replace(eta, "Eta alerts page.")
    d = case(tmp_path, revised, [MAJOR, "F2 | MAJOR | blocking | std"],
             [(1, {"finding": "F2", "op": "narrow", "old": zeta, "new": "Zeta logs are kept."})], base=PROP_BASE)
    code, out = check(d, capsys)
    assert code == 1 and "UNATTRIBUTED" in out
    code, out = enforce(d, capsys)
    assert code == 0 and "restored-baseline=no" in out, out
    assert (d / "spec.md").read_text() == PROP_BASE.replace(zeta, "Zeta logs are kept.")


def test_enforce_reverts_an_insertion_that_replaces_undeclared_deletions(tmp_path, capsys):
    """Property seed 9 case 198: a declared insertion inside a gap of undeclared deletions goes with them."""
    eta, theta = "Eta alerts page the on-call engineer.", "Theta dashboards show latency by region."
    revised = PROP_BASE.replace(f" {eta} {theta}", " Eta alerts page.")
    d = case(tmp_path, revised, [MAJOR, "F4 | MAJOR/FR-8 | blocking | gap:2"],
             [(1, {"finding": "F4", "op": "add", "anchor": eta, "new": "Eta alerts page.",
                   "considered": "nothing else fits"})], base=PROP_BASE)
    code, out = enforce(d, capsys)
    assert code == 0 and "restored-baseline=no" in out, out
    assert (d / "spec.md").read_text() == PROP_BASE


def test_enforce_restores_a_deleted_sentence_after_a_table_row(tmp_path, capsys):
    """Review r2-1 F2.1, input word for word: the restored sentence keeps the table and its break intact."""
    base = ("# Doc\n\n| k | v |\n|---|---|\n| a | one |\n\nLambda workers retry three times. Mu reports go out "
            "each Monday.\n\nOld entries leave the cache after one hour.\n")
    new = "Old entries leave the cache after thirty minutes."
    revised = base.replace("Lambda workers retry three times. ", "").replace(OLD, new)
    d = case(tmp_path, revised, [MAJOR], [(1, {"finding": "F1", "op": "replace", "old": OLD, "new": new})], base=base)
    code, out = enforce(d, capsys)
    assert code == 0 and "restored-baseline=no" in out, out
    assert (d / "spec.md").read_text() == base.replace(OLD, new)


def test_enforce_reverts_dependant_of_an_entry_whose_quote_is_not_in_the_baseline(tmp_path, capsys):
    """Review r2-1 F2.2: L2's quote is not in the baseline, so L2 is reverted and so is L1, which depends on it."""
    new1 = "The cache layer keeps recent records in memory for quicker reads."
    new2 = "Backups run at noon on a separate host machine."
    d = case(tmp_path, BASE.replace(CACHE, new1).replace(BACKUP, new2), [MAJOR, "F2 | MAJOR | blocking | std"],
             [(1, {"finding": "F1", "op": "replace", "old": CACHE, "new": new1, "depends": "L2"}),
              (2, {"finding": "F2", "op": "replace", "old": "Backups happen weekly on the main host.", "new": new2})])
    code, out = enforce(d, capsys)
    assert code == 0, out
    assert "ENFORCE reverted=F1 " in out
    assert (d / "spec.md").read_text() == BASE


def test_enforce_reverts_dependant_of_an_entry_that_changed_nothing(tmp_path, capsys):
    new1 = "Old entries leave the cache after thirty minutes."
    d = case(tmp_path, BASE.replace(OLD, new1), [MAJOR, "F2 | MAJOR | blocking | std"],
             [(1, {"finding": "F1", "op": "replace", "old": OLD, "new": new1, "depends": "L2"}),
              (2, {"finding": "F2", "op": "delete", "old": BACKUP})])
    code, out = enforce(d, capsys)
    assert code == 0 and "ENFORCE reverted=F1 " in out, out
    assert (d / "spec.md").read_text() == BASE


@pytest.mark.parametrize(
    "undeclared",
    [("| name | text |", "| name | string |"),
     ("| name | text |", "| name | text |\n| owner | string |"),
     ("| id | integer |\n", "")],
    ids=["cell-rewrite", "added-row", "deleted-row"],
)
def test_enforce_reverts_table_edits_and_keeps_a_fix_elsewhere(tmp_path, capsys, undeclared):
    new = "Old entries leave the cache after thirty minutes."
    d = case(tmp_path, BASE.replace(OLD, new).replace(*undeclared), [MAJOR],
             [(1, {"finding": "F1", "op": "replace", "old": OLD, "new": new})])
    code, out = enforce(d, capsys)
    assert code == 0 and "restored-baseline=no" in out, out
    assert (d / "spec.md").read_text() == BASE.replace(OLD, new)


def test_enforce_restores_the_whole_baseline_only_for_raw_size(tmp_path, capsys):
    """Trailing spaces keep every line break, so nothing but the raw size check sees them."""
    new = "Old entries leave the cache after thirty minutes."
    revised = BASE.replace(OLD, new).replace("\n\n", " " * 1200 + "\n\n")
    d = case(tmp_path, revised, [MAJOR], [(1, {"finding": "F1", "op": "replace", "old": OLD, "new": new})])
    code, out = enforce(d, capsys)
    assert code == 0 and "restored-baseline=yes reason=raw-size" in out, out
    assert (d / "spec.md").read_text() == BASE


def test_enforce_restores_added_blank_lines_and_keeps_the_fix(tmp_path, capsys):
    """Whitespace that adds line breaks between unchanged words is put back to the baseline's, so the raw
    size stays in bounds and the in-budget fix is kept. The one gap next to the fix's own changed words
    is not between two unchanged words, so it keeps the revision's extra line (spaces only)."""
    new = "Old entries leave the cache after thirty minutes."
    revised = BASE.replace(OLD, new).replace("\n\n", "\n" + " " * 1200 + "\n\n")
    d = case(tmp_path, revised, [MAJOR], [(1, {"finding": "F1", "op": "replace", "old": OLD, "new": new})])
    code, out = enforce(d, capsys)
    assert code == 0 and "restored-baseline=no" in out and "line-breaks=" in out, out
    final = (d / "spec.md").read_text()
    assert final.replace(new + "\n" + " " * 1200 + "\n\n", new + "\n\n") == BASE.replace(OLD, new)


def test_enforce_undoes_joined_table_rows_and_paragraphs(tmp_path, capsys):
    """F5.2's undetected joins: plain check reports no hunk, but --enforce restores the line breaks."""
    new = "Old entries leave the cache after thirty minutes."
    revised = (BASE.replace(OLD, new).replace("| id | integer |\n| name | text |", "| id | integer | | name | text |")
               .replace("host machine.\n\n| field", "host machine. | field"))
    d = case(tmp_path, revised, [MAJOR], [(1, {"finding": "F1", "op": "replace", "old": OLD, "new": new})])
    code, out = enforce(d, capsys)
    assert code == 0 and "line-breaks=2" in out, out
    assert (d / "spec.md").read_text() == BASE.replace(OLD, new)


ROW_BASE = BASE.replace("| name | text |", "| name | text |\n| c | three |")
FENCE_BASE = ("# Doc\n\nAlpha text here.\n\n```\nuv run thing\n```\n\nBeta text here. Gamma more text.\n\n"
              "Old entries leave the cache after one hour.\n")
HEADING_BASE = "# Doc\n\nText here now.\n\n## Note\n\nOld entries leave the cache after one hour.\n"


@pytest.mark.parametrize(
    "base, undeclared",
    [(FENCE_BASE, ("Alpha text here.\n\n```", "Alpha text here. ```")),
     (ROW_BASE, ("| c | three |", "c")),
     (HEADING_BASE, ("Text here now.\n\n## Note", "Text here now. ## Note"))],
    ids=["fence-join", "row-cut", "heading-join"],
)
def test_enforce_restores_whitespace_changes_of_structure(tmp_path, capsys, base, undeclared):
    """Review r3-1 F3.1: a whitespace change that alters a unit's kind is a hunk, so --enforce restores it."""
    new = "Old entries leave the cache after thirty minutes."
    d = case(tmp_path, base.replace(OLD, new).replace(*undeclared), [MAJOR],
             [(1, {"finding": "F1", "op": "replace", "old": OLD, "new": new})], base=base)
    code, out = enforce(d, capsys)
    assert code == 0 and "restored-baseline=no" in out, out
    assert (d / "spec.md").read_text() == base.replace(OLD, new)
    assert check(d, capsys)[0] == 0


def test_kind_only_change_is_an_unattributed_hunk(tmp_path, capsys):
    base = BASE.replace("| name | text |", "| name | text |\n| c |")
    d = case(tmp_path, base.replace("| c |", "c"), [MAJOR], [(1, {"finding": "F1", "op": "delete", "old": OLD})],
             base=base)
    code, out = check(d, capsys)
    assert code == 1 and "UNATTRIBUTED" in out and "+0/-0" in out, out


def test_enforce_reverts_a_kept_fix_that_changes_the_structure_after_it(tmp_path, capsys):
    """An in-budget fix that opens an unmatched fence turns later text into code; it is reverted whole,
    and an in-budget fix before it is kept."""
    first = "The service stores each record in the primary database table."
    new1 = "The service stores each record in the main database table."
    d = case(tmp_path, BASE.replace(first, new1).replace(OLD, OLD + "\n\n```"),
             [MAJOR, "F2 | MAJOR | blocking | std"],
             [(1, {"finding": "F1", "op": "add", "anchor": OLD, "new": "```", "considered": "a code block is needed"}),
              (2, {"finding": "F2", "op": "narrow", "old": first, "new": new1})])
    assert check(d, capsys)[0] == 1
    code, out = enforce(d, capsys)
    assert code == 0, out
    assert "ENFORCE reverted=F1 " in out and "structure=F1" in out
    assert (d / "spec.md").read_text() == BASE.replace(first, new1)


FENCE_FIX_BASE = ("# Doc\n\nAlpha text here now.\n\nBeta words sit here too.\n\nOld entries leave the cache after one hour.\n\n"
                  "Last line of the doc.\n")


@pytest.mark.parametrize("where", ["before", "after"])
def test_enforce_keeps_an_in_budget_fix_next_to_an_undeclared_fence(tmp_path, capsys, where):
    """Review r4-1 F4.1: an undeclared stand-alone fence next to an in-budget fix is reverted on its own."""
    new = "Old entries leave the cache after thirty minutes."
    revised = FENCE_FIX_BASE.replace(OLD, "```\n\n" + new if where == "before" else new + "\n\n```")
    d = case(tmp_path, revised, [MAJOR], [(1, {"finding": "F1", "op": "replace", "old": OLD, "new": new})],
             base=FENCE_FIX_BASE)
    code, out = enforce(d, capsys)
    assert code == 0, out
    assert "structure=-" in out and "restored-baseline=no" in out and "ENFORCE reverted=- " in out
    assert (d / "spec.md").read_text() == FENCE_FIX_BASE.replace(OLD, new)


# property seed 236 (shuffled blocks), case 144: kept table fixes read differently once a fence is reverted
RECHECK_BASE = ('# Prop\n\nAlpha nodes hold the primary copy of each shard. Beta nodes keep a warm replica for read'
    's. Gamma jobs compact old segments at night. Delta checks run before each deploy step.\n\n```\nuv r'
    'un thing\n```\n\n## Tail\n\nOne closing sentence here.\n\nEpsilon tokens expire after a fixed period. Z'
    'eta logs are kept for thirty days. Eta alerts page the on-call engineer. Theta dashboards show l'
    'atency by region.\n\n| key | value |\n|---|---|\n| a | one |\n| b | two |\n')
RECHECK_SPEC = ('# Prop\n\nAlpha nodes hold the primary copy of each shard. Beta nodes keep a warm replica for read'
    's. Gamma jobs compact old segments at night if must ## Note here here plain only `grep x | wc` h'
    'ere words AC-9 only here AC-9 plain must when here (F7) here ## Note plain only (F7) (F7) if onl'
    'y plain ## Note `grep x | wc` when when ## Note plain words only words plain `grep x | wc` must '
    'AC-9 plain ## Note only AC-9 words only only. Delta checks run before each deploy step.\n\n```\nuv '
    'run thing\n```\n\n## Tail\n\nOne closing sentence here.\n\nEpsilon tokens expire after a fixed period. '
    'Zeta logs are kept for thirty days.\n\n``` Eta alerts page the on-call engineer. Theta dashboards '
    'show latency by region.\n\n| key | value |\n|---|---|\n| a | changed |\n| b | changed |\n')


def test_enforce_judges_kept_table_fixes_after_removing_a_stray_fence(tmp_path, capsys):
    """Property case (seed 236): an undeclared fence turned the table into code; once it is removed first,
    F1's in-budget table fixes are judged in context and kept, and only the over-budget minor F3 goes."""
    rows = ["F1 | CRITICAL | blocking | std", "F2 | MAJOR | blocking | std", "F3 | MAJOR | minor | -",
            "F4 | MAJOR/FR-8 | blocking | gap:2"]
    entries = [(1, {"finding": "F1", "op": "replace", "old": "| a | one |", "new": "changed"}),
               (2, {"finding": "F1", "op": "delete", "old": "| b | two |"}),
               (3, {"finding": "F3", "op": "narrow", "old": "Gamma jobs compact old segments at night.",
                    "new": "Gamma jobs compact old segments at night if must ##"})]
    d = case(tmp_path, RECHECK_SPEC, rows, entries, base=RECHECK_BASE)
    code, out = enforce(d, capsys)
    assert code == 0, out
    assert "ENFORCE reverted=F3 " in out and "recheck=-" in out and "stray-fence-hunks=1" in out
    final = (d / "spec.md").read_text()
    assert "| a | changed |" in final and final.count("```") == RECHECK_BASE.count("```")
    code, out = check(d, capsys)
    assert code == 0 and "status=fixed" in finding_line(out, "F1"), out


S1 = "The service stores each record in the primary database table."


@pytest.mark.parametrize(
    "old, new",
    [("The service writes one log line per request.", "The service writes one log line per request today."),
     (CACHE, "The cache layer keeps recent records in memory for faster reads today.")],
    ids=["R3-exit-1", "R4-duplicate"],
)
def test_enforce_removes_an_undeclared_fence_before_judging_fixes(tmp_path, capsys, old, new):
    """Review r5-1 F5.1: an undeclared fence mid-text is removed first, so the kept fix is judged in
    context and no sentence is restored twice."""
    d = case(tmp_path, BASE.replace(S1, S1 + "\n\n```").replace(old, new), [MAJOR],
             [(1, {"finding": "F1", "op": "replace", "old": old, "new": new})])
    code, out = enforce(d, capsys)
    assert code == 0, out
    assert "ENFORCE reverted=- " in out and "stray-fence-hunks=1" in out
    assert (d / "spec.md").read_text() == BASE.replace(old, new)


def test_joined_table_rows_are_a_known_undetected_limit(tmp_path, capsys):
    """Review r5-1 F5.2: a join that keeps every unit's kind and text is no hunk (documented limit)."""
    revised = BASE.replace("| id | integer |\n| name | text |", "| id | integer | | name | text |")
    d = case(tmp_path, revised, [MAJOR], [(1, {"finding": "F1", "op": "delete", "old": OLD})])
    code, out = check(d, capsys)
    assert code == 0 and "hunks=0" in out, out
    assert "plain check does not report it" in fc.diff_hunks.__doc__
