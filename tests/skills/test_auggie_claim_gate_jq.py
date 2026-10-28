"""Run the claim-gate invariant program (the one fenced jq block) against fixture pairs.

Reads the canonical src/ ref and runs the real jq binary. A missing jq is a test failure
that names jq, never a skip (REQ-042, AT-25).
"""

from __future__ import annotations

import re
import shutil
import subprocess
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]
REF = REPO / "src/superclaude/skills/sc-auggie-review-protocol/refs/claim-gate.md"
FIXTURES = Path(__file__).resolve().parent / "fixtures/auggie_claim_gate/jq"
FINAL_LINE = "checks | all(.[]; .)"
DIAG_LINE = "checks | with_entries(select(.value | not)) | keys"

REQUIRED_INVARIANTS = [f"J{n}" for n in range(1, 23)]
SHAPE_CASES = {
    "invalid-shape-missing-run_status",
    "invalid-shape-missing-findings_count",
    "invalid-shape-missing-evidence_sources",
}
REQUIRED_VALID = {
    "valid-heading-defect",
    "valid-nit-defect",
    "valid-crosscut-pathline",
    "valid-crosscut-nested-subbullets",
    "valid-not-established-line",
    "valid-fenced-def-excerpt",
    "valid-quoted-id-paragraph",
    "valid-pr-head-mismatch",
    "valid-coverage-incomplete-partial",
    "valid-all-chunks-skipped",
    "valid-nonempty-zero-defects",
    "valid-single-defect",
    "valid-critical-crosscutting-heading",
    "valid-structural-mechanical",
    "valid-merged-does-not-block",
    "valid-remediation-ids-order",
    "valid-jq-exit-zero",
    "valid-jq-exit-null",
}


def jq_path() -> str:
    path = shutil.which("jq")
    if path is None:
        pytest.fail("jq is not on PATH: the claim-gate invariant tests need the real jq binary", pytrace=False)
    return path


def jq_block() -> str:
    text = REF.read_text(encoding="utf-8")
    blocks = re.findall(r"^```jq\n(.*?)^```$", text, flags=re.S | re.M)
    assert len(blocks) == 1, f"expected exactly one fenced jq block in {REF.name}, found {len(blocks)}"
    return blocks[0]


def pair_names(prefix: str) -> list[str]:
    return sorted(p.name[: -len(".candidates.json")] for p in FIXTURES.glob(f"{prefix}-*.candidates.json"))


def run_jq(program: str, name: str, tmp_path: Path) -> subprocess.CompletedProcess[str]:
    prog = tmp_path / "gate.jq"
    prog.write_text(program, encoding="utf-8")
    return subprocess.run(
        [
            jq_path(), "-e", "-n",
            "--slurpfile", "ledger", str(FIXTURES / f"{name}.candidates.json"),
            "--rawfile", "review", str(FIXTURES / f"{name}.REVIEW.md"),
            "-f", str(prog),
        ],
        capture_output=True, text=True, timeout=30,
    )


def failing_keys(name: str, tmp_path: Path) -> list[str]:
    block = jq_block()
    assert block.rstrip("\n").endswith(FINAL_LINE), "the jq block must end in the single boolean expression"
    diag = block.rstrip("\n")[: -len(FINAL_LINE)] + DIAG_LINE + "\n"
    res = run_jq(diag, name, tmp_path)
    assert res.returncode == 0, f"{name}: diagnostic run failed: {res.stderr}"
    import json
    return json.loads(res.stdout)


def mapped_key(name: str) -> str:
    m = re.match(r"invalid-j(\d+)-", name)
    if m:
        return f"J{int(m.group(1))}"
    assert name.startswith("invalid-shape-"), f"unmapped invalid fixture: {name}"
    return "SHAPE"


def test_exactly_one_fenced_jq_block_and_final_boolean():
    block = jq_block()
    assert "'" not in block, "the program must contain no single-quote character"
    assert ".jq_exit" not in block and "jq_exit]" not in block, "the program must never read jq_exit"
    assert block.rstrip("\n").splitlines()[-1] == FINAL_LINE


@pytest.mark.parametrize("name", pair_names("valid"))
def test_valid_pair_passes(name, tmp_path):
    """AT-08: every valid-* ledger/report pair exits 0."""
    res = run_jq(jq_block(), name, tmp_path)
    assert res.returncode == 0, f"{name}: jq exit {res.returncode}: {res.stderr}; failing: {failing_keys(name, tmp_path)}"


@pytest.mark.parametrize("name", pair_names("invalid"))
def test_invalid_pair_fails_on_its_invariant(name, tmp_path):
    """AT-09, AT-27: every invalid-* pair exits non-zero and fails the invariant it is named for."""
    res = run_jq(jq_block(), name, tmp_path)
    assert res.returncode == 1, f"{name}: expected jq exit 1 (false), got {res.returncode}: {res.stderr}"
    key = mapped_key(name)
    assert key in failing_keys(name, tmp_path), f"{name}: expected {key} among the failing checks"


def test_fixture_map_covers_every_invariant_and_shape_cases():
    names = pair_names("invalid")
    covered = {mapped_key(n) for n in names}
    assert set(REQUIRED_INVARIANTS) <= covered, f"uncovered invariants: {sorted(set(REQUIRED_INVARIANTS) - covered)}"
    assert SHAPE_CASES <= set(names)
    for key in ("J9", "J13", "J16"):
        assert any(mapped_key(n) == key for n in names), f"no invalid fixture for {key}"
    assert REQUIRED_VALID <= set(pair_names("valid")), sorted(REQUIRED_VALID - set(pair_names("valid")))
    for n in pair_names("valid") + names:
        assert (FIXTURES / f"{n}.REVIEW.md").is_file() and (FIXTURES / f"{n}.candidates.json").is_file()


def test_j9_j13_j16_each_have_valid_and_invalid_fixture():
    """AT-27: J9, J13 and J16 each have a valid and an invalid fixture."""
    valid = set(pair_names("valid"))
    assert {"valid-heading-defect", "valid-pr-head-mismatch", "valid-coverage-incomplete-partial"} <= valid
    invalid = pair_names("invalid")
    for key in ("J9", "J13", "J16"):
        assert [n for n in invalid if mapped_key(n) == key]


def test_missing_jq_fails_with_message_naming_jq(monkeypatch):
    """REQ-042: hiding jq from the lookup fails with a message that names jq (not a skip)."""
    monkeypatch.setattr(shutil, "which", lambda *_a, **_k: None)
    with pytest.raises(pytest.fail.Exception, match="jq"):
        jq_path()
