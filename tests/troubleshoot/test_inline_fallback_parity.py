"""T13 inline-fallback parity — R-14/R-19 acceptance test. Harness §6.

There is one executable assertion engine; 'agent path == inline path' is
satisfied by construction when that engine's output equals every fixture's
declared expectation and its registry equals every prose surface (assertion 1).
"""

from __future__ import annotations

import re
from pathlib import Path

from tests.troubleshoot._assertions import (
    FLAGS,
    CalibratorInputs,
    ValidatorInputs,
    evaluate_calibrator,
    evaluate_validator,
    fired_flags,
    load_fixture,
)

FIX = Path(__file__).parent / "fixtures"
REPO_ROOT = Path(__file__).resolve().parents[2]
REG = FIX / "regression" / "sysbox-20260918"

ROW = re.compile(
    r"^\|\s*(?P<id>A(?:10|[1-9])|C(?:3b|[1-8]))\s*\|\s*(?P<trigger>[^|]+?)\s*\|\s*`(?P<flag>[^`]+)`\s*\|",
    re.M,
)
CITE = re.compile(r"refs/agent-assertions\.md")

EXPECTED_IDS = {
    "GLM-RUN2": {"A1", "A3", "A4", "A5", "C2", "C3"},
    "Fable-D3": set(),
    "Astra-A3": {"A1", "A10"},
}

SURFACES = (
    REPO_ROOT
    / "src/superclaude/skills/sc-troubleshoot-protocol/refs/agent-assertions.md",
    REPO_ROOT / "src/superclaude/agents/evidence-validator.md",
    REPO_ROOT / "src/superclaude/agents/confidence-calibrator.md",
    REPO_ROOT / "src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md",
)


def parse_flag_table(text: str) -> dict[str, tuple[str, str]]:
    return {m["id"]: (m["trigger"].strip(), m["flag"]) for m in ROW.finditer(text)}


def load_regression(param: str) -> tuple[ValidatorInputs, CalibratorInputs | None]:
    d = REG / param
    files = {p.name: p.read_text() for p in d.iterdir() if p.is_file()}
    names = tuple(sorted(files))
    if param == "GLM-RUN2":
        cal = files["run2-tier2-root-cause-analyst-calibration.md"]
        card = files["run2-tier2-root-cause-analyst-hypothesis.md"]
        vin = ValidatorInputs(
            report=files["REPORT-RUN2.md"],
            calibration_texts=[cal],
            candidate_fixes_text=files["candidate-fixes.md"],
            card_texts=[card],
            files_present=names,
        )
        cin = CalibratorInputs(card=card, calibrated=0.42)
        return vin, cin
    if param == "Fable-D3":
        vin = ValidatorInputs(
            report=files["REPORT.md"],
            candidate_fixes_text=files["candidate-fixes.md"],
            files_present=names,
        )
        return vin, None
    vin = ValidatorInputs(
        report=files["REPORT.md"],
        tasklist_text=files["diagnosability-tasklist.md"],
        observation_text=files["tier1-observation.md"],
        files_present=names,
    )
    return vin, None


def test_flag_table_parity_across_surfaces() -> None:
    """R-14 T13: (id, trigger, flag) matches FLAGS or the surface cites the ref."""
    ref_table = {f.id: (f.trigger, f.flag) for f in FLAGS}
    assert set(ref_table) == {
        "A1",
        "A2",
        "A3",
        "A4",
        "A5",
        "A6",
        "A7",
        "A8",
        "A9",
        "A10",
        "C1",
        "C2",
        "C3",
        "C3b",
        "C4",
        "C5",
        "C6",
        "C7",
        "C8",
    }
    for surface in SURFACES:
        text = surface.read_text()
        parsed = parse_flag_table(text)
        assert parsed == ref_table or CITE.search(text), surface


def test_evaluator_matches_every_fixture_expectation() -> None:
    """R-19 T13: evaluator output equals every fixture expected_flags / expected ids."""
    for path in sorted(FIX.glob("assertions/**/*.md")):
        fx = load_fixture(path)
        got = fired_flags(fx)
        exp = set(fx.meta["expected_flags"] or [])
        assert got == exp, f"{path}: {got} != {exp}"
    for param, expected in EXPECTED_IDS.items():
        vin, cin = load_regression(param)
        ids = evaluate_validator(vin).ids
        if cin is not None:
            ids |= evaluate_calibrator(cin).ids
        assert ids == expected, (param, ids, expected)


def test_skill_fallback_names_every_flag_or_cites_ref() -> None:
    """R-14 T13: SKILL fallback names every flag token or cites the ref."""
    skill = (
        REPO_ROOT / "src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md"
    ).read_text()
    bases = {f.flag.split(":")[0] for f in FLAGS}
    if CITE.search(skill):
        return
    for tok in bases:
        assert tok in skill, tok
