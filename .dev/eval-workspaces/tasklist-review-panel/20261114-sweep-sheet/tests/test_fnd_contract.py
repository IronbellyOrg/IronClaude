"""Contract of scaffold/fnd.py with the real findings code (DESIGN 2.3; REQ-11)."""

import inspect
import json
import os
import subprocess

from click.testing import CliRunner
from helpers import REPO
from superclaude.cli.review import findings as real
from superclaude.cli.review import merge_cmd

from scaffold import fnd

ANCHOR = "The worker retries a failed delivery up to 8 times with exponential backoff"
DOC = f"# Spec\n\n{ANCHOR}, and then gives up.\n"


def pin(fn):
    """What the adapter relies on: parameter names, kinds, defaults and the return annotation."""
    sig = inspect.signature(fn)
    params = [
        (p.name, p.kind.name, p.default is p.empty) for p in sig.parameters.values()
    ]
    return fn.__name__, params, sig.return_annotation


def report(*lines):
    return (
        "review: 1 of 3\n\n## Findings block\n\n```findings-v1\n"
        + "\n".join(lines)
        + "\n```\n"
    )


def finding(fid, **extra):
    d = {
        "id": fid,
        "severity": "CRITICAL",
        "blocking": True,
        "category": "contradiction",
        "anchor": ANCHOR,
        "refs": [],
        "claim": "the retry count disagrees with the limit",
    }
    d.update(extra)
    return json.dumps(d)


def test_check_finding_signature_pin():
    assert pin(real._check_finding) == (
        "_check_finding",
        [
            ("obj", "POSITIONAL_OR_KEYWORD", True),
            ("seen", "POSITIONAL_OR_KEYWORD", True),
        ],
        "str | None",
    )


def test_blocks_after_signature_pin():
    assert pin(real._blocks_after) == (
        "_blocks_after",
        [
            ("text", "POSITIONAL_OR_KEYWORD", True),
            ("heading", "POSITIONAL_OR_KEYWORD", True),
            ("info", "POSITIONAL_OR_KEYWORD", True),
        ],
        "tuple[bool, list[tuple[int, list[tuple[int, str]], bool]]]",
    )


def test_public_helper_signatures_pinned():
    assert list(inspect.signature(real.parse_block).parameters) == ["report_text"]
    assert list(inspect.signature(real.flat).parameters) == ["s"]
    assert list(inspect.signature(real.locate).parameters) == ["text", "quote"]
    assert list(inspect.signature(real.same_defect).parameters) == ["a", "b"]


def test_pin_detects_a_signature_change():
    def _check_finding(obj, seen, extra) -> str | None: ...

    def _blocks_after(text, heading) -> tuple: ...

    assert pin(_check_finding) != pin(real._check_finding)
    assert pin(_blocks_after) != pin(real._blocks_after)


def test_adapter_reexports_the_real_objects():
    for name in (
        "parse_block",
        "flat",
        "locate",
        "same_defect",
        "_check_finding",
        "_blocks_after",
    ):
        assert getattr(fnd, name) is getattr(real, name), name


def test_lenient_lines_keeps_invalid_lines():
    good, bad = finding("F1"), "{not json"
    text = report(good, "", bad)
    assert fnd.lenient_lines(text) == [good, bad]
    assert fnd.parse_block(text)["ok"] is False


def test_lenient_lines_uses_the_last_block_and_unclosed_block():
    first = "## Findings block\n\n```findings-v1\n" + finding("A1") + "\n```\n\n"
    last = report(finding("B1"))
    assert fnd.lenient_lines(first + last) == [finding("B1")]
    assert fnd.lenient_lines(
        "## Findings block\n\n```findings-v1\n" + finding("C1")
    ) == [finding("C1")]


def test_lenient_lines_without_block_is_empty():
    assert fnd.lenient_lines("no heading here") == []
    assert fnd.lenient_lines("## Findings block\n\nnothing") == []


def keys_in(obj):
    if isinstance(obj, dict):
        for k, v in obj.items():
            yield k
            yield from keys_in(v)
    elif isinstance(obj, list):
        for v in obj:
            yield from keys_in(v)


def test_merge_accepts_class_probe_src_keys(tmp_path):
    doc = tmp_path / "doc.md"
    doc.write_text(DOC)
    rep = tmp_path / "r1.md"
    rep.write_text(
        report(finding("F1", **{"class": "C1", "probe": "P1", "src": "sheet"}))
    )
    parsed = real.parse_block(rep.read_text())
    assert parsed["ok"] and parsed["findings"][0]["class"] == "C1"
    out, ledger = tmp_path / "merged-1.md", tmp_path / "ledger.json"
    res = CliRunner().invoke(
        merge_cmd.command,
        [
            "--ledger",
            str(ledger),
            "--doc",
            str(doc),
            "--round",
            "1",
            "--report",
            f"r1={rep}",
            "--out",
            str(out),
        ],
    )
    assert res.exit_code == 0, res.output
    assert json.loads(res.output)["block_ok"] == {"r1": True}
    assert json.loads(ledger.read_text())["rows"], (
        "the finding was merged into the ledger"
    )
    merged = out.read_text()
    assert "F1" in merged or "L1" in merged
    for path in (out, ledger):
        for key in ("class", "probe", "src"):
            assert f'"{key}"' not in path.read_text(), (path.name, key)
    assert not {"class", "probe", "src"} & set(keys_in(json.loads(ledger.read_text())))


def test_existing_review_suite_passes():
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    cmd = [
        "uv",
        "run",
        "--frozen",
        "--project",
        str(REPO),
        "pytest",
        "-p",
        "no:cacheprovider",
        str(REPO / "tests" / "review"),
        "-q",
    ]
    r = subprocess.run(
        cmd, capture_output=True, text=True, env=env, cwd=REPO, timeout=300
    )
    assert r.returncode == 0, r.stdout[-2000:] + r.stderr[-1000:]
    assert " passed" in r.stdout.splitlines()[-1]
