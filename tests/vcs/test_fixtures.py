"""Tests of the shared fixtures in conftest.py (Task 1).

The fixtures are the base of every later test of the ``vcs`` helper, so each one is
shown to build what its name says: a throwaway repository with a local bare remote, a
ledger the real archive parser accepts, a sidecar with every line form of FR-100 and
FR-120, a ``file://`` submodule, and a lazy path to the helper scripts.
"""

import re
import subprocess
import sys

import pytest

# --- the sidecar line forms (hand-copied from FR-100 and FR-120 of the requirements) ---
HEX40 = r"[0-9a-f]{40}"
HEX64 = r"[0-9a-f]{64}"
IDS = r"[0-9A-Za-z.,-]+"
SIDECAR_FORMS = {
    "run": re.compile(
        r"^run [0-9]+: commit-tasks=(on|off)( reason=revoked)? ledger-lines=[0-9]+"
        r" branch=(refs/heads/\S+|-) at=\S+ args=\"[^\"]*\""
        r" source=(\S+|inline:[0-9a-f]{8}) worktree=\S+$"
    ),
    "prepared": re.compile(
        rf"^T{IDS}: commit prepared key={HEX64} attempt=[0-9]+ parent={HEX40}"
        rf" branch=\S+ paths={HEX64} accepted=\S+(,\S+)* plan=({HEX64}|-)"
        rf" source=({HEX64}|-)$"
    ),
    "sha": re.compile(
        rf"^T{IDS}: commit (sha|recovered)={HEX40} key={HEX64} attempt=[0-9]+"
        r"( outside-changed=[0-9]+ wt=\S+)?$"
    ),
    "skipped": re.compile(
        rf"^T{IDS}: commit skipped key={HEX64} reason=(empty|mixed-authorization)$"
    ),
    "refused": re.compile(
        rf"^T{IDS}: commit (refused|uncertain) key={HEX64} attempt=[0-9]+"
        r" reason=\S+( rewritten=\S+)?$"
    ),
    "abandoned": re.compile(
        rf"^T({IDS}): commit resolved key=({HEX64}) as=abandoned"
        r' at=[0-9]{4}-[0-9]{2}-[0-9]{2} quote="((?:[^"\\]|\\.)+)"$'
    ),
    "adopted": re.compile(
        rf"^T({IDS}): commit resolved key=({HEX64}) as=adopted head={HEX40}"
        r" basis=(candidate|accepted) differs=[0-9]+"
        r' at=[0-9]{4}-[0-9]{2}-[0-9]{2} quote="((?:[^"\\]|\\.)+)"$'
    ),
}


def _kinds(line):
    return [name for name, rx in SIDECAR_FORMS.items() if rx.match(line)]


# --- repo ---------------------------------------------------------------------------
def test_repo_has_work_tree_and_local_bare_remote(repo):
    assert (repo.work / ".git").is_dir()
    assert repo.bare.is_dir() and repo.bare.name == "origin.git"
    assert repo.git("remote", "get-url", "origin").strip() == str(repo.bare)
    assert repo.git("symbolic-ref", "--short", "HEAD").strip() == "main"
    # the first commit reached the bare remote
    assert (
        repo.git("rev-parse", "HEAD").strip()
        == repo.git("-C", str(repo.bare), "rev-parse", "main").strip()
    )


def test_repo_helpers_write_and_commit(repo):
    repo.write("a/b.txt", "x\n")
    sha = repo.commit("add b")
    assert re.fullmatch(HEX40, sha)
    assert repo.git("rev-parse", "HEAD").strip() == sha
    assert repo.git("status", "--porcelain") == ""


# --- ledger_builder -------------------------------------------------------------------
def test_ledger_builder_header_only_is_accepted(ledger_builder, archive_mod):
    builder = ledger_builder()
    builder.header().write()
    recs = archive_mod._parse_ledger(builder.path)
    assert [r[0] for r in recs] == ["header"]


def test_ledger_builder_accepts_every_record_kind(ledger_builder, archive_mod):
    builder = ledger_builder()
    (
        builder.header()
        .plan()
        .start("1")
        .complete("1")
        .start("2")
        .blocked("2")
        .ruling("2")
        .complete("2", verdict="missing")
        .start("3")
        .blocked("3")
        .retry_open("3", 3)
        .retry_revert("3", 3)
        .retry_review("3", 3)
        .halt("3", 2, "budget")
        .final("pass")
        .archive("start id=TASK-WF-x-20261001-063000 token=0123456789abcdef")
        .write()
    )
    kinds = [r[0] for r in archive_mod._parse_ledger(builder.path)]
    assert kinds == [
        "header", "plan", "start", "verdict", "start", "verdict", "ruling",
        "verdict", "start", "verdict", "retry", "retry", "retry", "halt",
        "final", "archive",
    ]  # fmt: skip
    assert builder.text().endswith("\n")


def test_ledger_builder_blocked_and_retry_lines_have_the_grammar_shape(ledger_builder):
    builder = ledger_builder()
    builder.header().start("4").blocked("4").retry_open("4", 3)
    lines = builder.lines
    assert lines[2].startswith("T4: blocked verdict=missing ")
    assert re.fullmatch(
        rf"T4: retry n=3 step=open checkpoint={HEX40} tier=[A-Za-z0-9_]+", lines[3]
    )


def test_ledger_builder_rejects_a_bad_header_position(ledger_builder, archive_mod):
    builder = ledger_builder()
    builder.start("1").header().write()
    with pytest.raises(archive_mod.ArchiveError):
        archive_mod._parse_ledger(builder.path)


# --- sidecar_builder ------------------------------------------------------------------
def test_sidecar_builder_writes_every_line_form(sidecar_builder):
    key = "a" * 64
    sidecar_builder.run(1, "on", ledger_lines=3)
    sidecar_builder.run(2, "off", ledger_lines=9, branch="-", revoked=True)
    sidecar_builder.prepared("1", key=key, attempt=1)
    sidecar_builder.commit("1", key=key, attempt=1, outside_changed=2, wt="refs/x/wt")
    sidecar_builder.commit("2", key=key, attempt=1, recovered=True)
    sidecar_builder.skipped("1,2", key=key, reason="empty")
    sidecar_builder.refused("1", key=key, attempt=1, reason="hook-failed")
    sidecar_builder.refused(
        "1", key=key, attempt=2, reason="hook-rewrite", rewritten="refs/x/rw",
        uncertain=True,
    )  # fmt: skip
    sidecar_builder.resolved_abandoned("1", key=key, quote='say "no"')
    sidecar_builder.resolved_adopted("1", key=key, head="b" * 40, quote="ok")
    sidecar_builder.write()

    lines = sidecar_builder.path.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 10
    assert sidecar_builder.path.name == "commits.md"
    seen = set()
    for line in lines:
        kinds = _kinds(line)
        assert len(kinds) == 1, (line, kinds)
        seen.add(kinds[0])
    assert seen == set(SIDECAR_FORMS)


def test_sidecar_builder_counts_ledger_lines_like_fr_102(tmp_path, sidecar_builder):
    ledger = tmp_path / "l.md"
    ledger.write_bytes(b"a\nb\n")
    assert sidecar_builder.ledger_k(ledger) == 2  # two newline bytes, terminated
    ledger.write_bytes(b"a\nb")
    assert sidecar_builder.ledger_k(ledger) == 2  # one newline plus one for the tail
    ledger.write_bytes(b"")
    assert sidecar_builder.ledger_k(ledger) == 0


def test_sidecar_builder_raw_lines_pass_through_for_corrupt_cases(sidecar_builder):
    sidecar_builder.raw("not a form")
    sidecar_builder.write(trailing_newline=False)
    assert sidecar_builder.path.read_text(encoding="utf-8") == "not a form"


# --- submodule_repo -------------------------------------------------------------------
def test_submodule_repo_status_line_can_be_read(submodule_repo):
    out = submodule_repo.git("submodule", "status")
    m = re.match(rf"^[ +\-U]({HEX40}) (\S+)( \(.*\))?$", out.rstrip("\n"))
    assert m, out
    assert m.group(2) == submodule_repo.sub_path
    assert (submodule_repo.work / submodule_repo.sub_path / "lib.txt").is_file()
    url = submodule_repo.git("config", "-f", ".gitmodules", "submodule.lib.url")
    assert url.strip().startswith("file://")


def test_submodule_repo_allows_file_protocol_only_in_its_own_config(
    submodule_repo, tmp_path
):
    local = submodule_repo.git("config", "--local", "protocol.file.allow")
    assert local.strip() == "always"
    # a repository the fixture did not make has no such setting
    other = tmp_path / "other"
    other.mkdir()
    subprocess.run(["git", "init", "-q", str(other)], check=True)
    done = subprocess.run(
        ["git", "-C", str(other), "config", "--get", "protocol.file.allow"],
        capture_output=True,
        text=True,
    )
    assert done.returncode != 0 and done.stdout == ""


# --- scripts_dir ------------------------------------------------------------------------
def test_use_scripts_dir_adds_path_when_present(tmp_path, monkeypatch):
    from tests.vcs.conftest import use_scripts_dir

    folder = tmp_path / "scripts"
    folder.mkdir()
    monkeypatch.setattr(sys, "path", list(sys.path))
    assert use_scripts_dir(monkeypatch, folder) == folder
    assert sys.path[0] == str(folder)


def test_use_scripts_dir_skips_when_folder_is_absent(tmp_path, monkeypatch):
    from tests.vcs.conftest import use_scripts_dir

    with pytest.raises(pytest.skip.Exception):
        use_scripts_dir(monkeypatch, tmp_path / "missing")


def test_scripts_dir_fixture_skips_until_the_folder_exists(request):
    from tests.vcs.conftest import SCRIPTS

    if not SCRIPTS.is_dir():
        with pytest.raises(pytest.skip.Exception):
            request.getfixturevalue("scripts_dir")
    else:
        assert request.getfixturevalue("scripts_dir") == SCRIPTS
        assert str(SCRIPTS) in sys.path
