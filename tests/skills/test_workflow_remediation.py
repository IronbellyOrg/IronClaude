"""Tests for the /sc:workflow remediation routing script."""

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest

_SCRIPT = (
    Path(__file__).resolve().parents[2]
    / "src/superclaude/skills/sc-workflow-protocol/scripts/remediate.py"
)
_spec = importlib.util.spec_from_file_location("remediate", _SCRIPT)
rm = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(rm)


@pytest.mark.parametrize(
    "args,kwargs,expected",
    [
        ((0, 0, 0), {}, ("none", False)),
        ((0, 20, 30), {}, ("none", False)),
        ((3, 0, 0), {}, ("surgical", False)),
        ((4, 0, 0), {}, ("regenerate", False)),
        ((1, 5, 0), {}, ("surgical", False)),
        ((1, 6, 0), {}, ("regenerate", False)),
        ((1, 0, 9), {}, ("surgical", False)),
        ((1, 0, 10), {}, ("regenerate", False)),
        ((4, 0, 0), {"regenerated_already": True}, ("escalate", False)),
        ((1, 0, 0), {"forced": "regenerate"}, ("regenerate", True)),
        ((5, 0, 0), {"forced": "surgical"}, ("surgical", True)),
        ((2, 0, 0), {"forced": "none"}, ("none", True)),
        (
            (1, 0, 0),
            {"forced": "regenerate", "regenerated_already": True},
            ("escalate", True),
        ),
        (
            (1, 0, 0),
            {"forced": "surgical", "regenerated_already": True},
            ("surgical", True),
        ),
    ],
)
def test_route(args, kwargs, expected):
    assert rm.route(*args, **kwargs) == expected


@pytest.mark.parametrize("bad", [-1, 1.5, "2", True])
def test_route_rejects_bad_counts(bad):
    with pytest.raises(ValueError):
        rm.route(bad, 0, 0)


def _run(*args):
    return subprocess.run(
        [sys.executable, str(_SCRIPT), *args], capture_output=True, text=True
    )


def test_cli_prints_json():
    p = _run("route", "--blocking", "2", "--label-high", "1", "--medium", "0")
    assert p.returncode == 0
    assert json.loads(p.stdout) == {"route": "surgical", "forced": False}


def test_cli_forced_and_escalate():
    p = _run(
        "route",
        "--blocking",
        "1",
        "--label-high",
        "0",
        "--medium",
        "0",
        "--forced",
        "regenerate",
        "--regenerated-already",
    )
    assert json.loads(p.stdout) == {"route": "escalate", "forced": True}


@pytest.mark.parametrize("bad", ["-1", "x", "1.5"])
def test_cli_rejects_bad_counts(bad):
    p = _run("route", "--blocking", bad, "--label-high", "0", "--medium", "0")
    assert p.returncode != 0


# --------------------------------------------------------------------------
# Task 4: package copy, archive, place, restore, mark, release
# --------------------------------------------------------------------------
import hashlib  # noqa: E402
import os  # noqa: E402
import re  # noqa: E402
import shutil  # noqa: E402

OLD = "TASK-WF-authLogin-20261001-063000"
STAMP = "20261002-000000"
NEW = f"TASK-WF-authLogin-{STAMP}"
COUNTS = '{"blocking": 1, "label_high": 0, "medium": 2, "note": 3}'
BASE_CONTRACT = (
    f'contract_version: "1.1"\nstatus: success\nslug: {OLD}\n'
    f"plan_path: ./{OLD}.md\nsource_path: ./source.md\n"
)
PLAN = f"---\nschema: workflow-plan/1.2\nslug: {OLD}\n---\n# Demo\n\nOld  sentence.\nKeep me.\n"


def _kernel_ok(tmp_path):
    a, b = tmp_path / "probe-a", tmp_path / "probe-b"
    a.mkdir()
    try:
        rm._load_helper().rename_noreplace(str(a), str(b))
    except Exception:
        return False
    return True


@pytest.fixture
def repo(tmp_path):
    root = tmp_path / "checkout"
    (root / ".git").mkdir(parents=True)
    if not _kernel_ok(tmp_path):
        pytest.skip("kernel lacks renameat2 RENAME_NOREPLACE")
    return root


def make_pkg(root, contract=BASE_CONTRACT, pid=OLD):
    pkg = root / ".dev/tasks/to-do" / pid
    pkg.mkdir(parents=True)
    (pkg / f"{pid}.md").write_text(PLAN.replace(OLD, pid))
    (pkg / "source.md").write_text("the source\n")
    if contract is not None:
        (pkg / "return-contract.yaml").write_text(contract)
    return pkg


def top_keys(text):
    return [
        ln.split(":", 1)[0] for ln in text.splitlines() if re.match(r"^[A-Za-z_]+:", ln)
    ]


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def repaired_copy(root, old=OLD, new=NEW):
    info = rm.prepare(root, old, new)
    copy = Path(info["copy_dir"])
    f = copy / f"{new}.md"
    f.write_text(f.read_text().replace("Old  sentence.", "New sentence."))
    return info, copy


def review_file(tmp_path):
    p = tmp_path / "REPORT.md"
    p.write_text("# review\nfinding B1\n")
    return p


@pytest.mark.parametrize("taken", [None, "archive", "done", "to-do"])
def test_end_to_end_surgical(repo, tmp_path, taken):
    pkg = make_pkg(repo)
    tasks = repo / ".dev/tasks"
    if taken:
        (tasks / taken / f"TASK-WF-authLogin-{STAMP}").mkdir(parents=True)
    old_sha = sha(pkg / f"{OLD}.md")
    new = rm.reserve(repo, OLD, now=STAMP)
    assert new == (NEW if taken is None else NEW + "-2")
    assert (tasks / "to-do" / new).is_dir() and not os.listdir(tasks / "to-do" / new)
    info, copy = repaired_copy(repo, new=new)
    assert info["old_plan_sha256"] == old_sha
    assert f"slug: {new}" in (copy / f"{new}.md").read_text()  # gate rule on the copy
    rm.archive(repo, pkg, new)
    arch = tasks / "archive" / OLD
    assert sha(arch / f"{OLD}.md") == old_sha
    assert not (tasks / "to-do" / OLD).exists()
    rm.place(repo, OLD, new, str(copy), COUNTS, str(review_file(tmp_path)))
    rm.mark(tasks / "to-do" / new, fix_cycles=1)
    newp = tasks / "to-do" / new
    contract = (newp / "return-contract.yaml").read_text()
    assert 'contract_version: "1.1"' in contract
    assert f"supersedes: {OLD}" in contract
    assert "remediation_route: surgical" in contract
    assert "fix_cycles: 1" in contract
    acontract = (arch / "return-contract.yaml").read_text()
    assert f"superseded_by: {new}" in acontract
    assert "## Revision 1" in (newp / "source.md").read_text()
    assert OLD in (newp / "source.md").read_text()
    assert (newp / "source.md").read_text().startswith("the source\n")
    for name in ("plan.diff", "prior-findings.md", "old-plan.md", "revision-log.md"):
        assert (newp / "artifacts" / name).is_file()
    assert sha(newp / "artifacts/old-plan.md") == old_sha
    diff = (newp / "artifacts/plan.diff").read_text()
    assert "-Old  sentence." in diff and "+New sentence." in diff
    for c in (contract, acontract):
        keys = top_keys(c)
        assert len(keys) == len(set(keys))


def test_revision_number_increments(repo, tmp_path):
    pkg = make_pkg(repo)
    (pkg / "source.md").write_text("src\n\n## Revision 1\n\nold\n")
    new = rm.reserve(repo, OLD, now=STAMP)
    _, copy = repaired_copy(repo, new=new)
    rm.archive(repo, pkg, new)
    rm.place(repo, OLD, new, str(copy), COUNTS, str(review_file(tmp_path)))
    assert (
        "## Revision 2" in (repo / ".dev/tasks/to-do" / new / "source.md").read_text()
    )


def test_archive_none_appends_one_unrecorded_line(repo):
    pkg = make_pkg(repo)
    rm.archive(repo, pkg, "none")
    text = (repo / ".dev/tasks/archive" / OLD / "return-contract.yaml").read_text()
    assert text.count("replacement id is unrecorded") == 1
    assert "superseded_by" not in text
    assert text.count("SUPERSEDED") == 1


@pytest.mark.parametrize("word", ["SUPERSEDED", "superseded", "Superseded"])
def test_existing_superseded_gets_no_second_item(repo, word):
    contract = BASE_CONTRACT + f'unresolved:\n  - "{word} by hand"\nhandoff: none\n'
    pkg = make_pkg(repo, contract)
    rm.archive(repo, pkg, "none")
    out = (repo / ".dev/tasks/archive" / OLD / "return-contract.yaml").read_text()
    assert out == contract


@pytest.mark.parametrize("superseded_by", ["none", NEW])
@pytest.mark.parametrize(
    "tail",
    [
        # another package's "superseded" mentioned mid-sentence in an unresolved item
        'unresolved:\n  - "Written for X; another package is superseded."\nhandoff: none\n',
        # only the superseded_by key, no warning item
        "superseded_by: other-id\nhandoff: none\n",
    ],
)
def test_unrelated_superseded_mention_still_gets_the_warning(repo, tail, superseded_by):
    contract = BASE_CONTRACT + tail
    pkg = make_pkg(repo, contract)
    rm.archive(repo, pkg, superseded_by)
    out = (repo / ".dev/tasks/archive" / OLD / "return-contract.yaml").read_text()
    assert len(re.findall(r'^\s*- "SUPERSEDED', out, re.M)) == 1
    keys = top_keys(out)
    assert len(keys) == len(set(keys))
    rm.restore(repo, OLD)
    back = repo / ".dev/tasks/to-do" / OLD / "return-contract.yaml"
    assert back.read_text() == contract


def test_inline_list_warning_gets_no_second_item(repo):
    contract = BASE_CONTRACT + 'unresolved: ["SUPERSEDED by hand", "x"]\n'
    pkg = make_pkg(repo, contract)
    rm.archive(repo, pkg, "none")
    out = (repo / ".dev/tasks/archive" / OLD / "return-contract.yaml").read_text()
    assert out == contract


def test_comma_inside_one_quoted_inline_item_is_not_a_warning(repo):
    # one item whose text contains ", superseded": not a second item, not a warning
    contract = (
        BASE_CONTRACT + 'unresolved: ["unrelated, superseded by another package"]\n'
    )
    pkg = make_pkg(repo, contract)
    rm.archive(repo, pkg, "none")
    out = (repo / ".dev/tasks/archive" / OLD / "return-contract.yaml").read_text()
    assert out.count("SUPERSEDED") == 1
    rm.restore(repo, OLD)
    back = repo / ".dev/tasks/to-do" / OLD / "return-contract.yaml"
    assert back.read_text() == contract


@pytest.mark.parametrize(
    "tail",
    [
        "unresolved: []\nhandoff: none\n",
        "",
        'unresolved:\n  - "one"\nhandoff: none\n',
        'unresolved:\n  - "one"\n  - "two"\n',
        "handoff: none\nunresolved:\n- one\nreflect: ok\n",
        'unresolved: ["x"]\nreflect: ok\n',
        "unresolved:\nreflect: ok\n",
    ],
)
@pytest.mark.parametrize("newline", [True, False])
def test_unresolved_forms_and_restore_is_byte_identical(repo, tmp_path, tail, newline):
    contract = BASE_CONTRACT + tail
    if not newline:
        contract = contract.rstrip("\n")
    pkg = make_pkg(repo, contract)
    new = rm.reserve(repo, OLD, now=STAMP)
    rm.archive(repo, pkg, new)
    arch = repo / ".dev/tasks/archive" / OLD
    text = (arch / "return-contract.yaml").read_text()
    assert text.count("SUPERSEDED by") == 1
    keys = top_keys(text)
    assert len(keys) == len(set(keys))
    other = [
        k
        for k in keys
        if k not in top_keys(contract) and k not in ("superseded_by", "unresolved")
    ]
    assert other == []
    if "handoff: none" in tail and "unresolved:\n- one" in tail:
        assert '- one\n- "SUPERSEDED' in text  # same list style, list followed by keys
        assert text.index("SUPERSEDED by") < text.index("reflect: ok")
    # failed place (copy dir missing) -> release -> restore
    with pytest.raises(rm.RemediateError):
        rm.place(
            repo, OLD, new, str(tmp_path / "nope"), COUNTS, str(review_file(tmp_path))
        )
    rm.release(repo, new)
    assert not (repo / ".dev/tasks/to-do" / new).exists()
    rm.restore(repo, OLD)
    back = repo / ".dev/tasks/to-do" / OLD
    assert (back / "return-contract.yaml").read_text() == contract
    assert not (back / "artifacts").exists()
    assert (
        "SUPERSEDED" not in (back / "return-contract.yaml").read_text()
        or "SUPERSEDED" in contract
    )
    assert not (repo / ".dev/tasks/archive" / OLD).exists()


def test_missing_contract_gets_minimal_partial_and_restore_removes_it(repo):
    pkg = make_pkg(repo, contract=None)
    rm.archive(repo, pkg, "none")
    arch = repo / ".dev/tasks/archive" / OLD
    text = (arch / "return-contract.yaml").read_text()
    assert "status: partial" in text and 'contract_version: "1.1"' in text
    assert text.count("unrecorded") == 1
    assert (arch / "artifacts/archive-undo.txt").is_file()
    rm.restore(repo, OLD)
    back = repo / ".dev/tasks/to-do" / OLD
    assert not (back / "return-contract.yaml").exists()
    assert not (back / "artifacts").exists()


def test_restore_keeps_preexisting_artifacts_dir(repo):
    pkg = make_pkg(repo)
    (pkg / "artifacts").mkdir()
    (pkg / "artifacts/keep.txt").write_text("k")
    rm.archive(repo, pkg, "none")
    rm.restore(repo, OLD)
    back = repo / ".dev/tasks/to-do" / OLD
    assert os.listdir(back / "artifacts") == ["keep.txt"]
    assert (back / "return-contract.yaml").read_text() == BASE_CONTRACT


def test_reserve_collision_suffixes_and_exhaustion(repo):
    make_pkg(repo)
    tasks = repo / ".dev/tasks"
    (tasks / "archive" / NEW).mkdir(parents=True)
    assert rm.reserve(repo, OLD, now=STAMP) == NEW + "-2"
    for n in range(3, 10):
        (tasks / "done" / f"{NEW}-{n}").mkdir(parents=True, exist_ok=True)
    with pytest.raises(rm.RemediateError) as e:
        rm.reserve(repo, OLD, now=STAMP)
    assert e.value.code == "E-PACKAGE-COLLISION"
    # only the one leaf created earlier remains new
    assert sorted(p.name for p in (tasks / "to-do").iterdir()) == sorted(
        [OLD, NEW + "-2"]
    )


def test_reserve_uses_real_clock_id_rule(repo):
    make_pkg(repo)
    new = rm.reserve(repo, OLD)
    assert re.match(r"^TASK-WF-authLogin-\d{8}-\d{6}(-[2-9])?$", new)


def test_place_fails_when_leaf_missing_or_not_empty(repo, tmp_path):
    pkg = make_pkg(repo)
    new = rm.reserve(repo, OLD, now=STAMP)
    _, copy = repaired_copy(repo, new=new)
    rm.archive(repo, pkg, new)
    rev = str(review_file(tmp_path))
    leaf = repo / ".dev/tasks/to-do" / new
    (leaf / "stray.txt").write_text("x")
    with pytest.raises(rm.RemediateError) as e:
        rm.place(repo, OLD, new, str(copy), COUNTS, rev)
    assert e.value.code == "E-REMEDIATE-LEAF"
    with pytest.raises(rm.RemediateError):  # release refuses foreign content
        rm.release(repo, new)
    assert (leaf / "stray.txt").exists()
    (leaf / "stray.txt").unlink()
    leaf.rmdir()
    with pytest.raises(rm.RemediateError) as e:
        rm.place(repo, OLD, new, str(copy), COUNTS, rev)
    assert e.value.code == "E-REMEDIATE-LEAF"


def test_place_refuses_while_old_package_is_still_in_to_do(repo, tmp_path):
    pkg = make_pkg(repo)
    tasks = repo / ".dev/tasks"
    plan_sha, contract = (
        sha(pkg / f"{OLD}.md"),
        (pkg / "return-contract.yaml").read_text(),
    )
    new = rm.reserve(repo, OLD, now=STAMP)
    _, copy = repaired_copy(repo, new=new)
    with pytest.raises(rm.RemediateError) as e:  # no rm.archive call
        rm.place(repo, OLD, new, str(copy), COUNTS, str(review_file(tmp_path)))
    assert e.value.code == "E-REMEDIATE-SOURCE"
    assert sha(pkg / f"{OLD}.md") == plan_sha
    assert (pkg / "return-contract.yaml").read_text() == contract
    assert not (tasks / "archive").exists() or not os.listdir(tasks / "archive")
    assert os.listdir(tasks / "to-do" / new) == []


def test_archive_never_overwrites_existing_destination(repo):
    pkg = make_pkg(repo)
    dest = repo / ".dev/tasks/archive" / OLD
    dest.mkdir(parents=True)
    (dest / "marker").write_text("keep")
    before = (pkg / "return-contract.yaml").read_text()
    with pytest.raises(rm.RemediateError):
        rm.archive(repo, pkg, "none")
    assert (dest / "marker").read_text() == "keep" and os.listdir(dest) == ["marker"]
    assert (pkg / "return-contract.yaml").read_text() == before


def test_failed_place_release_restore_leaves_no_new_package(
    repo, tmp_path, monkeypatch
):
    pkg = make_pkg(repo)
    new = rm.reserve(repo, OLD, now=STAMP)
    _, copy = repaired_copy(repo, new=new)
    rm.archive(repo, pkg, new)

    def boom(*a):
        raise RuntimeError("diff failed")

    monkeypatch.setattr(rm, "_diff_w", boom)
    with pytest.raises(RuntimeError):
        rm.place(repo, OLD, new, str(copy), COUNTS, str(review_file(tmp_path)))
    leaf = repo / ".dev/tasks/to-do" / new
    assert os.listdir(leaf)  # half filled
    assert rm.release(repo, new)["status"] == "released"
    rm.restore(repo, OLD)
    todo = sorted(p.name for p in (repo / ".dev/tasks/to-do").iterdir())
    assert todo == [OLD]
    assert not list((repo / ".dev/tasks/archive").iterdir())
    assert (
        repo / ".dev/tasks/to-do" / OLD / "return-contract.yaml"
    ).read_text() == BASE_CONTRACT


def test_release_removes_empty_leaf_and_is_idempotent(repo):
    make_pkg(repo)
    new = rm.reserve(repo, OLD, now=STAMP)
    assert rm.release(repo, new)["status"] == "released"
    assert rm.release(repo, new)["status"] == "absent"


def test_mark_regenerate_writes_link_fields(repo):
    pkg = make_pkg(repo)
    rm.mark(
        pkg,
        supersedes="TASK-WF-authLogin-20260901-000000",
        route_name="regenerate",
        finding_counts=COUNTS,
    )
    text = (pkg / "return-contract.yaml").read_text()
    assert "supersedes: TASK-WF-authLogin-20260901-000000" in text
    assert "remediation_route: regenerate" in text
    assert (
        'finding_counts: {"blocking": 1, "label_high": 0, "medium": 2, "note": 3}'
        in text
    )
    with pytest.raises(rm.RemediateError):  # the three go together
        rm.mark(pkg, supersedes="TASK-WF-authLogin-20260901-000000")


def test_mark_review_fail_replaces_and_never_duplicates(repo):
    pkg = make_pkg(repo, BASE_CONTRACT + "review_verdict: PASS\nfix_cycles: 0\n")
    rm.mark(pkg, review_fail=True, open_blockers="B1, B2", fix_cycles=2)
    rm.mark(pkg, review_fail=True, open_blockers="B2", fix_cycles=2, superseded_by=NEW)
    text = (pkg / "return-contract.yaml").read_text()
    keys = top_keys(text)
    assert len(keys) == len(set(keys))
    assert "review_verdict: FAIL" in text and 'open_blockers: ["B2"]' in text
    assert "fix_cycles: 2" in text and f"superseded_by: {NEW}" in text
    with pytest.raises(rm.RemediateError):
        rm.mark(pkg, review_fail=True)  # no blockers named
    with pytest.raises(rm.RemediateError):
        rm.mark(pkg, open_blockers="B1")  # blockers without FAIL


def test_mark_without_contract_creates_minimal_regenerate_links(repo):
    pkg = make_pkg(repo, contract=None)
    old = "TASK-WF-authLogin-20260901-000000"
    rm.mark(pkg, supersedes=old, route_name="regenerate", finding_counts=COUNTS)
    text = (pkg / "return-contract.yaml").read_text()
    keys = top_keys(text)
    assert keys == [
        "contract_version",
        "status",
        "slug",
        "supersedes",
        "remediation_route",
        "finding_counts",
    ]
    assert 'contract_version: "1.1"' in text and "status: partial" in text
    assert f"slug: {OLD}" in text and f"supersedes: {old}" in text
    assert "remediation_route: regenerate" in text


def test_mark_review_fail_without_contract_creates_minimal_contract(repo):
    pkg = make_pkg(repo, contract=None)
    rm.mark(pkg, review_fail=True, open_blockers="B1,B2", fix_cycles=0)
    text = (pkg / "return-contract.yaml").read_text()
    keys = top_keys(text)
    assert len(keys) == len(set(keys))
    assert "status: partial" in text and f"slug: {OLD}" in text
    assert "review_verdict: FAIL" in text and 'open_blockers: ["B1", "B2"]' in text


def test_mark_without_contract_or_package_dir_still_fails(repo, tmp_path):
    with pytest.raises(rm.RemediateError) as e:
        rm.mark(tmp_path / "nope", fix_cycles=1)
    assert e.value.code == "E-REMEDIATE-CONTRACT"


def test_mark_fails_on_duplicate_key(repo):
    pkg = make_pkg(repo, BASE_CONTRACT + "fix_cycles: 1\nfix_cycles: 2\n")
    with pytest.raises(rm.RemediateError):
        rm.mark(pkg, fix_cycles=3)


def _install_without_sibling(tmp_path):
    skills = tmp_path / "skills"
    dest = skills / "sc-workflow-protocol/scripts"
    dest.mkdir(parents=True)
    shutil.copy(_SCRIPT, dest / "remediate.py")
    return dest / "remediate.py"


def test_missing_sibling_helper_moves_nothing(repo, tmp_path):
    pkg = make_pkg(repo)
    script = _install_without_sibling(tmp_path)
    p = subprocess.run(
        [
            sys.executable,
            str(script),
            "archive",
            "--root",
            str(repo),
            "--package",
            str(pkg),
            "--superseded-by",
            "none",
        ],
        capture_output=True,
        text=True,
    )
    assert p.returncode == 1 and "E-REMEDIATE-HELPER" in p.stderr
    assert pkg.is_dir() and not (repo / ".dev/tasks/archive").exists()
    assert (pkg / "return-contract.yaml").read_text() == BASE_CONTRACT


def test_installed_layout_finds_sibling_helper(repo, tmp_path):
    pkg = make_pkg(repo)
    script = _install_without_sibling(tmp_path)
    helper_dir = tmp_path / "skills/sc-implement-protocol/scripts"
    helper_dir.mkdir(parents=True)
    shutil.copy(rm.HELPER_PATH, helper_dir / "archive_workspace.py")
    p = subprocess.run(
        [
            sys.executable,
            str(script),
            "archive",
            "--root",
            str(repo),
            "--package",
            str(pkg),
            "--superseded-by",
            "none",
        ],
        capture_output=True,
        text=True,
    )
    assert p.returncode == 0, p.stderr
    assert (repo / ".dev/tasks/archive" / OLD).is_dir()


def test_platform_without_renameat2_moves_nothing(repo, monkeypatch):
    pkg = make_pkg(repo)
    monkeypatch.setattr(sys, "platform", "darwin")
    with pytest.raises(rm.RemediateError) as e:
        rm.archive(repo, pkg, "none")
    monkeypatch.undo()
    assert e.value.code == "E-ARCHIVE-PLATFORM"
    assert pkg.is_dir() and not (repo / ".dev/tasks/archive" / OLD).exists()
    assert (pkg / "return-contract.yaml").read_text() == BASE_CONTRACT


def test_cli_reserve_prepare_archive_flow(repo):
    pkg = make_pkg(repo)
    r = _run("reserve", "--root", str(repo), "--old-id", OLD)
    assert r.returncode == 0
    new = r.stdout.strip()
    assert re.match(r"^TASK-WF-authLogin-\d{8}-\d{6}(-[2-9])?$", new)
    p = _run("prepare", "--root", str(repo), "--old-id", OLD, "--new-id", new)
    info = json.loads(p.stdout)
    assert Path(info["copy_dir"]).name == new
    assert info["old_plan_sha256"] == sha(pkg / f"{OLD}.md")
    assert Path(info["tmp_dir"]).name.startswith("sc-workflow-revise.")
    a = _run(
        "archive", "--root", str(repo), "--package", str(pkg), "--superseded-by", new
    )
    assert a.returncode == 0 and json.loads(a.stdout)["status"] == "archived"
    bad = _run(
        "archive", "--root", str(repo), "--package", str(pkg), "--superseded-by", "none"
    )
    assert bad.returncode == 1 and "E-REMEDIATE" in bad.stderr


_SKILL_DIR = _SCRIPT.parents[1]


def test_wave5_merges_into_existing_contract_and_keeps_review_verdict():
    skill = (_SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
    contract = (_SKILL_DIR / "refs/return-contract.md").read_text(encoding="utf-8")
    wave5 = skill.split("## Wave 5", 1)[1].split("## Will / Will Not", 1)[0]
    assert "merges into the contract that `place` and `mark` already wrote" in wave5
    assert "never replaces the file" in wave5
    assert "final placed package" in wave5
    assert "`review_verdict`" in wave5.split("keeps every line of", 1)[1]
    assert "every rewrite merges into the existing file" in contract
    assert "`review_verdict`" in contract.split("keeps every other line", 1)[1]
    assert skill.index("## Wave 4R") < skill.index("## Wave 5")
    assert skill.index("## Wave 4 ") < skill.index("## Wave 4R")
    assert "never edit, delete, or regenerate" not in skill
    head = skill.split("---", 2)[1]
    assert "Agent" in head and "Task" in head


def test_revise_waives_source_and_enters_wave_4r_directly():
    parse = (_SKILL_DIR / "refs/input-parse.md").read_text(encoding="utf-8")
    skill = (_SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
    assert "With `--revise` the source requirement is waived" in parse
    assert "STOP `E-BAD-FLAG`" in parse.split("With `--revise`", 1)[1].split("\n", 1)[0]
    wave0 = skill.split("## Wave 0", 1)[1].split("## Wave 1", 1)[0]
    assert "the source requirement is waived" in wave0
    assert "Waves 0 to 4 are skipped" in wave0
    assert "enters Wave 4R directly with `<old-id>` = the given package" in wave0


_IMPL_DIR = (
    Path(__file__).resolve().parents[2] / "src/superclaude/skills/sc-implement-protocol"
)


def test_implement_refuses_review_verdict_fail_before_ledger():
    m = (_IMPL_DIR / "refs/managed-workspace.md").read_text(encoding="utf-8")
    detection = m.split("## Detection", 1)[1].split("## Location resolution", 1)[0]
    assert "`review_verdict: FAIL`" in detection
    assert "STOP `E-MANAGED-REVIEW-FAIL`" in detection
    assert "`open_blockers`" in detection
    assert "before any write and before the ledger step" in detection
    assert m.index("E-MANAGED-REVIEW-FAIL") < m.index("## Ledger, artifacts, pins")


def test_review_fail_code_listed_in_every_managed_stop_list():
    skill = (_IMPL_DIR / "SKILL.md").read_text(encoding="utf-8")
    qa = (_IMPL_DIR / "refs/qa.md").read_text(encoding="utf-8")
    assert "| `E-MANAGED-REVIEW-FAIL` |" in skill
    assert "`E-MANAGED-CONFLICT`, `E-MANAGED-REVIEW-FAIL`" in qa
    plugin = (
        Path(__file__).resolve().parents[2]
        / "plugins/superclaude/skills/sc-implement-protocol"
    )
    for rel in ("SKILL.md", "refs/qa.md", "refs/managed-workspace.md"):
        assert (plugin / rel).read_bytes() == (_IMPL_DIR / rel).read_bytes(), rel


def test_contract_pin_and_locations_unchanged():
    m = (_IMPL_DIR / "refs/managed-workspace.md").read_text(encoding="utf-8")
    assert '`contract_version: "1.1"`' in m and 'contract_version: "1.2"' not in m
    arch = (_IMPL_DIR / "scripts/archive_workspace.py").read_text(encoding="utf-8")
    assert 'contract.get("contract_version") != "1.1"' in arch
    assert (
        "<checkout>/.dev/tasks/to-do/<slug>/<slug>.md` or `<checkout>/.dev/tasks/done/<slug>/<slug>.md`"
        in m
    )
    assert 'tasks / "archive"' not in arch and '"tasks" / "archive"' not in arch
    assert (
        "archive/"
        not in m.split("## Location resolution", 1)[1].split("## Ledger", 1)[0]
    )


def test_archive_refuses_symlinked_archive_dir(repo, tmp_path):
    pkg = make_pkg(repo)
    outside = tmp_path / "outside"
    outside.mkdir()
    (repo / ".dev/tasks/archive").symlink_to(outside)
    with pytest.raises(rm.RemediateError) as e:
        rm.archive(repo, pkg, "none")
    assert e.value.code == "E-REMEDIATE-ROOT"
    assert pkg.is_dir() and not os.listdir(outside)


def test_restore_refuses_symlinked_todo_dir(repo, tmp_path):
    pkg = make_pkg(repo)
    rm.archive(repo, pkg, "none")
    todo = repo / ".dev/tasks/to-do"
    todo.rmdir()
    outside = tmp_path / "outside"
    outside.mkdir()
    todo.symlink_to(outside)
    with pytest.raises(rm.RemediateError) as e:
        rm.restore(repo, OLD)
    assert e.value.code == "E-REMEDIATE-ROOT"
    assert (repo / ".dev/tasks/archive" / OLD).is_dir() and not os.listdir(outside)


def test_archive_refuses_preexisting_undo_file_and_keeps_it(repo):
    pkg = make_pkg(repo)
    undo = pkg / "artifacts" / rm.UNDO_NAME
    undo.parent.mkdir()
    undo.write_bytes(b"precious\x00bytes")
    with pytest.raises(rm.RemediateError) as e:
        rm.archive(repo, pkg, "none")
    assert e.value.code == "E-REMEDIATE-CONFLICT"
    assert undo.read_bytes() == b"precious\x00bytes"
    assert not (repo / ".dev/tasks/archive" / OLD).exists()


def test_archive_rollback_deletes_only_undo_file_it_created(repo, monkeypatch):
    pkg = make_pkg(repo)
    (pkg / "artifacts").mkdir()
    (pkg / "artifacts" / "keep.txt").write_text("keep")

    def boom(*a, **k):
        raise OSError("contract write failed")

    monkeypatch.setattr(rm, "_write_atomic", boom)
    with pytest.raises(rm.RemediateError) as e:
        rm.archive(repo, pkg, "none")
    assert "rolled back" in e.value.msg
    assert (pkg / "artifacts" / "keep.txt").read_text() == "keep"
    assert not (
        pkg / "artifacts" / rm.UNDO_NAME
    ).exists()  # the run's own file is removed


def test_archive_rollback_removes_partial_undo_file_with_existing_artifacts(
    repo, monkeypatch
):
    pkg = make_pkg(repo)
    (pkg / "artifacts").mkdir()
    (pkg / "artifacts" / "keep.txt").write_text("keep")
    real = rm._write_new

    def partial(path, data):
        Path(path).write_text("par")  # created, then the write fails
        raise OSError("disk full")

    monkeypatch.setattr(rm, "_write_new", partial)
    with pytest.raises(rm.RemediateError) as e:
        rm.archive(repo, pkg, "none")
    assert "rolled back" in e.value.msg
    assert not (pkg / "artifacts" / rm.UNDO_NAME).exists()
    monkeypatch.setattr(rm, "_write_new", real)
    rm.archive(repo, pkg, "none")  # retry succeeds
    assert (repo / ".dev/tasks/archive" / OLD).is_dir()


def test_write_new_removes_its_partial_file_but_never_a_preexisting_one(tmp_path):
    p = tmp_path / "f.txt"
    with pytest.raises(TypeError):
        rm._write_new(p, 123)  # open succeeds, write fails
    assert not p.exists()
    p.write_bytes(b"mine")
    with pytest.raises(FileExistsError):
        rm._write_new(p, "x")
    assert p.read_bytes() == b"mine"


def test_place_finds_review_inside_old_package_after_archive(repo):
    pkg = make_pkg(repo)
    (pkg / "artifacts").mkdir()
    report = pkg / "artifacts" / "REPORT.md"
    report.write_text("# inside\n")
    new = rm.reserve(repo, OLD, now=STAMP)
    _, copy = repaired_copy(repo, new=new)
    rm.archive(repo, pkg, new)
    assert not report.exists()
    rm.place(repo, OLD, new, str(copy), COUNTS, str(report))
    leaf = repo / ".dev/tasks/to-do" / new
    assert (leaf / "artifacts/prior-findings.md").read_text() == "# inside\n"


def test_place_still_fails_for_nonexistent_review_elsewhere(repo, tmp_path):
    pkg = make_pkg(repo)
    new = rm.reserve(repo, OLD, now=STAMP)
    _, copy = repaired_copy(repo, new=new)
    rm.archive(repo, pkg, new)
    with pytest.raises(rm.RemediateError) as e:
        rm.place(repo, OLD, new, str(copy), COUNTS, str(tmp_path / "nope.md"))
    assert e.value.code == "E-REMEDIATE-SOURCE"


def test_remediation_ref_coordinator_supplies_diff():
    ref = (_SKILL_DIR / "refs/remediation.md").read_text(encoding="utf-8")
    sec = ref.split("## 4. The re-review brief", 1)[1].split("## 5.", 1)[0]
    assert "The coordinator runs `diff -w <baseline> <candidate>` itself" in sec
    assert 'stands in for the prompt\'s "Run diff -w" step' in sec
    assert "runs no commands" in sec
    assert "It runs `diff -w" not in sec
