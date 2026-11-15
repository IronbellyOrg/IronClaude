"""K8: the sibling folder SW is read only (TESTING 4)."""

import json
import os
import re
import subprocess
import sys
from pathlib import Path

RL = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RL / "fixtures" / "sibling"))
import make_sibling  # noqa: E402

SCRIPT = RL / "bin" / "copy-shared.sh"
LIST = RL / "config" / "shared-list.json"

# A path that names the sibling: its folder name, or the shell variables SW and SIB (RL scripts use neither for anything else).
SIB_REF = r"(?:20261114-sweep-sheet|\$\{?(?:SW|SIB)\}?(?![A-Za-z_0-9]))"
WRITERS = r"(?:rm|mkdir|touch|tee|ln|rmdir|chmod|truncate|sed\s+-i\S*)"
PY_SIB_REF = r"(?:20261114-sweep-sheet|\bSW\b|\bSIB\b)"
PY_WRITE = r"(?:write_text|write_bytes|shutil\.|os\.(?:remove|rename|replace|utime)|\.unlink\(|open\([^)]*[\"'][wax])"


def write_targets_sw(line):
    """True when a shell or python line has a write command whose target is the sibling (heuristic, TESTING 4 K8)."""
    ref = re.compile(SIB_REF)
    if re.search(r">>?\s*[\"']?" + SIB_REF, line):  # redirect target
        return True
    for m in re.finditer(r"\b(cp|mv|install)\b([^|;&]*)", line):
        args = [a for a in m.group(2).split() if not a.startswith("-")]
        if args and ref.search(
            args[-1]
        ):  # the last argument is the target; an earlier one is only a source
            return True
    if re.search(r"\b" + WRITERS + r"\b[^|;&]*" + SIB_REF, line):
        return True
    return bool(re.search(PY_WRITE, line) and re.search(PY_SIB_REF, line))


def own_scripts():
    """Every script of RL that RL wrote: copies are byte copies of sibling files (in them SW means the folder they sit in)."""
    copied = {
        p
        for p, e in json.loads((RL / "config" / "shared-manifest.json").read_text())[
            "files"
        ].items()
        if e["kind"] == "copied"
    }
    out = []
    for sub in ("bin", "rl", "analysis", "scaffold", "tests/fakes", "fixtures"):
        for p in sorted((RL / sub).rglob("*")):
            if (
                p.is_file()
                and "__pycache__" not in p.parts
                and str(p.relative_to(RL)) not in copied
            ):
                if p.suffix in {".sh", ".py"} or os.access(p, os.X_OK):
                    out.append(p)
    return out


def test_detector_finds_a_write_target_under_sw():
    for bad in (
        'cp "$a" "$SW/x"',
        "echo x > $SIB/out",
        "rm -f ${SW}/a",
        "mkdir -p /h/20261114-sweep-sheet/new",
        'sed -i s/a/b/ "$SW/f"',
        'Path(SW / "x").write_text("a")',
    ):
        assert write_targets_sw(bad), bad
    for good in (
        'cp -- "$SIB/$rel" "$DEST/$rel"',
        'sha256sum -- "$SIB/$p"',
        "diff -u -- $SIB/a $DEST/a",
        "SB=/tmp/evalsb-recipe",
    ):
        assert not write_targets_sw(good), good


def test_copy_script_never_writes_the_sibling(tmp_path):
    sib, dest = tmp_path / "sib", tmp_path / "dest"
    before = make_sibling.build(sib, tier_b=["scaffold/clock.py", "bin/run-panel.sh"])
    env = {k: v for k, v in os.environ.items() if not k.startswith("SW_")}
    for extra in ([], ["--check"], ["--diff", "scaffold/clock.py"]):
        args = [
            "bash",
            str(SCRIPT),
            "--sibling",
            str(sib),
            "--dest",
            str(dest),
            "--list",
            str(LIST),
            "--gap",
            "0",
            *extra,
        ]
        r = subprocess.run(args, capture_output=True, text=True, env=env)
        assert r.returncode == 0, (extra, r.stderr)
        assert make_sibling.snapshot(sib) == before, (
            extra
        )  # no file created, removed or touched, no folder changed
        assert make_sibling.canary_unchanged(sib), extra


def test_no_script_writes_under_sw():
    scripts = own_scripts()
    assert {p.name for p in scripts} >= {
        "copy-shared.sh",
        "rl-env.sh",
        "claude",
        "make_sibling.py",
    }
    hits = [
        f"{p.relative_to(RL)}:{n}: {line.strip()}"
        for p in scripts
        for n, line in enumerate(p.read_text().splitlines(), 1)
        if not line.lstrip().startswith("#") and write_targets_sw(line)
    ]
    assert not hits, hits
