"""bin/build-sandbox.sh (R-03) on a throwaway fixture repo."""
import json

from conftest import BIN, PKGS, run

PKG = PKGS[2]


def test_leak_dirs_absent(world):
    r = run(["bash", str(BIN / "build-sandbox.sh"), PKG], env=world.env)
    assert r.returncode == 0, r.stderr
    tar = world.sbr / f"base/{PKG}.tar"
    names = run(["tar", "-tf", str(tar)]).stdout.splitlines()
    assert any(n.endswith("src/app.py") for n in names)
    for leak in (".dev/tasks/done", ".dev/eval-workspaces", ".dev/research", ".dev/reflect"):
        assert not any(leak in n for n in names), leak
    assert r.stdout.strip() == run(["sha256sum", str(tar)]).stdout.split()[0]


def test_missing_base_sha_exits_2(world):
    m = json.loads(world.manifest.read_text())
    del m["base_sha"][PKG]
    world.manifest.write_text(json.dumps(m))
    assert run(["bash", str(BIN / "build-sandbox.sh"), PKG], env=world.env).returncode == 2


def test_second_run_is_noop(world):
    run(["bash", str(BIN / "build-sandbox.sh"), PKG], env=world.env, check=True)
    tar = world.sbr / f"base/{PKG}.tar"
    st = tar.stat().st_mtime_ns
    r = run(["bash", str(BIN / "build-sandbox.sh"), PKG], env=world.env)
    assert r.returncode == 0 and tar.stat().st_mtime_ns == st
