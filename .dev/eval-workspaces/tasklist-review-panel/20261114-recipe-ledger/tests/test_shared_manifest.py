"""DR-11: the shared copy rule. bin/copy-shared.sh against F-SIBLING fixtures, and the real manifest (TESTING 4)."""

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

RL = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RL / "fixtures" / "sibling"))
import make_sibling  # noqa: E402

SCRIPT = RL / "bin" / "copy-shared.sh"
LIST = RL / "config" / "shared-list.json"
B_PATHS = [b["path"] for b in make_sibling.load_list()["B"]]
S_PATHS = make_sibling.load_list()["S"]


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def copy(sib, dest, *args, gap=0):
    env = {k: v for k, v in os.environ.items() if not k.startswith("SW_")}
    return subprocess.run(
        [
            "bash",
            str(SCRIPT),
            "--sibling",
            str(sib),
            "--dest",
            str(dest),
            "--list",
            str(LIST),
            "--gap",
            str(gap),
            *args,
        ],
        capture_output=True,
        text=True,
        env=env,
    )


def manifest(dest):
    return json.loads((Path(dest) / "config" / "shared-manifest.json").read_text())[
        "files"
    ]


@pytest.fixture
def copied(tmp_path):
    """A fixture sibling with no Tier B file, copied once into dest."""
    sib, dest = tmp_path / "sib", tmp_path / "dest"
    make_sibling.build(sib)
    r = copy(sib, dest)
    assert r.returncode == 0, r.stderr
    return sib, dest


# ---- the real manifest of this build ----


def test_manifest_hashes_match_files():
    files = json.loads((RL / "config" / "shared-manifest.json").read_text())["files"]
    listed = {
        p
        for tier in make_sibling.load_list().values()
        for p in (x["path"] if isinstance(x, dict) else x for x in tier)
    }
    assert set(files) == listed
    for rel, e in files.items():
        if e["tier"] == "S":
            continue  # Tier S is owned by RL after the first copy and is not compared (DESIGN 3.1)
        if e["kind"] == "copied":
            assert sha(RL / rel) == e["sha256"], rel
            assert (RL / rel).stat().st_size == e["bytes"], rel
        else:
            # A built-local entry is recorded with sha256 "ABSENT" until the local file exists, so ABSENT is accepted here;
            # a recorded hash must match the file.
            assert e["sha256"] == "ABSENT" or sha(RL / rel) == e["sha256"], rel


def test_briefs_parts_match_manifest():
    files = json.loads((RL / "config" / "shared-manifest.json").read_text())["files"]
    parts = {p: e for p, e in files.items() if p.startswith("briefs/")}
    assert len(parts) == 9
    for rel, e in parts.items():
        assert e["kind"] == "copied" and sha(RL / rel) == e["sha256"], rel
    assert {p.name for p in (RL / "briefs").iterdir()} == {Path(p).name for p in parts}


def test_built_local_entries_name_a_swd_section():
    files = json.loads((RL / "config" / "shared-manifest.json").read_text())["files"]
    local = {p: e for p, e in files.items() if e["kind"] == "built-local"}
    assert set(local) <= set(B_PATHS) and local, "only Tier B files may be built-local"
    for rel, e in local.items():
        assert e["tier"] == "B" and e["swd"].startswith("SWD"), rel


# ---- the copy script against F-SIBLING ----


def test_copy_script_refuses_a_missing_tier_a_file(tmp_path):
    sib, dest = tmp_path / "sib", tmp_path / "dest"
    make_sibling.build(sib, missing_tier_a="cards/C3.json")
    r = copy(sib, dest)
    assert r.returncode == 3 and "E_MISSING: cards/C3.json" in r.stderr
    assert (
        not (dest / "cards").exists()
        and not (dest / "config" / "shared-manifest.json").exists()
    )


def test_copy_script_refuses_an_unstable_tier_b_file(tmp_path):
    sib, dest = tmp_path / "sib", tmp_path / "dest"
    make_sibling.build(sib, tier_b=["scaffold/clock.py"])
    timer = make_sibling.change_later(sib, "scaffold/clock.py", 0.3)
    r = copy(sib, dest, gap=1)
    timer.join()
    assert r.returncode == 3 and "E_UNSTABLE: scaffold/clock.py" in r.stderr
    assert (
        not (dest / "cards").exists()
        and not (dest / "config" / "shared-manifest.json").exists()
    )


def test_a_stable_tier_b_file_is_copied(tmp_path):
    sib, dest = tmp_path / "sib", tmp_path / "dest"
    make_sibling.build(sib, tier_b=["scaffold/clock.py"])
    assert copy(sib, dest).returncode == 0
    e = manifest(dest)["scaffold/clock.py"]
    assert e["kind"] == "copied" and e["sha256"] == sha(
        dest / "scaffold/clock.py"
    ) == sha(sib / "scaffold/clock.py")
    assert manifest(dest)["scaffold/telemetry.py"]["kind"] == "built-local"


def test_copy_script_marks_absent_tier_b_as_built_local(copied):
    _, dest = copied
    files = manifest(dest)
    swd = {b["path"]: b["swd"] for b in make_sibling.load_list()["B"]}
    for rel in B_PATHS:
        assert files[rel]["kind"] == "built-local" and files[rel]["swd"] == swd[rel]
        assert (
            files[rel]["sha256"] == "ABSENT"
        )  # not written yet; see test_manifest_hashes_match_files
        assert not (dest / rel).exists()
    assert {e["kind"] for p, e in files.items() if p not in B_PATHS} == {"copied"}
    assert files["cards/C1.json"]["sha256"] == sha(dest / "cards/C1.json")


def test_check_reports_drift_as_warning(copied):
    sib, dest = copied
    assert copy(sib, dest, "--check").returncode == 0
    (sib / "cards" / "C2.json").write_text("the sibling changed this card\n")
    r = copy(sib, dest, "--check")
    assert (
        r.returncode == 0
        and "drift cards/C2.json" in r.stdout
        and "1 drift (warning)" in r.stdout
    )
    (dest / "cards" / "C4.json").write_text("an edited copy\n")
    r = copy(sib, dest, "--check")
    assert r.returncode == 1 and "FAIL cards/C4.json" in r.stdout


def test_diff_prints_for_built_local(copied):
    sib, dest = copied
    (dest / "scaffold").mkdir(exist_ok=True)
    (dest / "scaffold/ledgerv1.py").write_text("local build\n")
    assert (
        "the sibling has no file"
        in copy(sib, dest, "--diff", "scaffold/ledgerv1.py").stdout
    )
    (sib / "scaffold/ledgerv1.py").write_text("the sibling's build\n")
    r = copy(sib, dest, "--diff", "scaffold/ledgerv1.py")
    assert (
        r.returncode == 0
        and "-the sibling's build" in r.stdout
        and "+local build" in r.stdout
    )
    r = copy(
        sib, dest, "--check"
    )  # the sibling now has a file that RL built locally: a warning, never a swap
    assert r.returncode == 0 and "drift scaffold/ledgerv1.py" in r.stdout


def test_tier_s_file_recorded_once_and_not_checked(copied):
    sib, dest = copied
    first = manifest(dest)[S_PATHS[0]]
    assert first["kind"] == "copied" and first["sha256"] == sha(dest / S_PATHS[0])
    (dest / S_PATHS[0]).write_text("a hold-out entry was added by its author\n")
    (sib / S_PATHS[0]).write_text("the sibling changed it too\n")
    r = copy(sib, dest, "--check")
    assert (
        r.returncode == 0
        and f"drift {S_PATHS[0]}" not in r.stdout
        and "0 drift" in r.stdout
    )
    assert (
        copy(sib, dest).returncode == 0
    )  # a second copy keeps RL's file and the first record
    assert manifest(dest)[S_PATHS[0]]["sha256"] == first["sha256"]
    assert (dest / S_PATHS[0]).read_text().startswith("a hold-out entry")


def test_a_built_local_file_is_not_replaced_by_a_later_copy(copied):
    sib, dest = copied
    (dest / "scaffold/telemetry.py").write_text("local build\n")
    (sib / "scaffold/telemetry.py").write_text("the sibling's build\n")
    r = copy(sib, dest)
    assert r.returncode == 0 and "built-local and the sibling now has it" in r.stdout
    assert (dest / "scaffold/telemetry.py").read_text() == "local build\n"
    assert manifest(dest)["scaffold/telemetry.py"]["sha256"] == sha(
        dest / "scaffold/telemetry.py"
    )


def test_destination_inside_the_sibling_is_refused(tmp_path):
    sib = tmp_path / "sib"
    make_sibling.build(sib)
    r = copy(sib, sib / "rl")
    assert r.returncode == 2 and "E_DEST_IN_SIBLING" in r.stderr
