"""T1 validator assertions — R-14/R-19 acceptance test. Harness §3 T1."""

from __future__ import annotations

from pathlib import Path

import pytest

from tests.troubleshoot._assertions import (
    ValidatorInputs,
    evaluate_validator,
    fired_flags,
    fired_ids,
    load_fixture,
    validator_inputs,
)

FIX = Path(__file__).parent / "fixtures"
A_FILES = sorted(FIX.glob("assertions/A*/*/*.md"))


def _case_id(path: Path) -> str:
    return f"{path.parent.parent.name}-{path.parent.name}-{path.stem}"


@pytest.mark.parametrize("fixture_path", A_FILES, ids=[_case_id(p) for p in A_FILES])
def test_validator_fixture_fires_expected_flags(fixture_path: Path) -> None:
    """R-19 T1: each A-fixture fires exactly its expected flag set."""
    fx = load_fixture(fixture_path)
    got = fired_flags(fx)
    exp = set(fx.meta["expected_flags"] or [])
    assert got == exp, f"{fixture_path}: flags {got} != {exp}"
    ids = fired_ids(fx)
    if str(fx.meta.get("polarity")) == "pos" or "pos" in fixture_path.stem:
        assert ids, f"{fixture_path}: pos fixture fired no ids"


def test_validator_status_mapping() -> None:
    """R-14: status precedence FAIL > blocked > partial."""
    a7 = evaluate_validator(
        validator_inputs(load_fixture(FIX / "assertions/A7/io/pos.md"))
    )
    a8 = evaluate_validator(
        validator_inputs(load_fixture(FIX / "assertions/A8/io/pos.md"))
    )
    a1 = evaluate_validator(
        validator_inputs(load_fixture(FIX / "assertions/A1/io/pos.md"))
    )
    assert a7.status == "FAIL", a7.status
    assert a8.status == "blocked", a8.status
    assert a1.status == "partial", a1.status


@pytest.mark.parametrize(
    "source",
    [
        "calibration_texts",
        "card_texts",
        "candidate_fixes_text",
        "observation_text",
        "artifact_texts",
    ],
)
def test_a1_only_captured_output_grounds_headline(source: str) -> None:
    inp = ValidatorInputs(
        report="Root cause: `clone-failed`\nconfidence: 0.72", artifact_texts=[]
    )
    text = (
        "outcome=clone-failed"
        if source == "artifact_texts"
        else "Definition: clone-failed means the clone command failed."
    )
    setattr(inp, source, [text] if source.endswith("texts") else text)
    assert ("A1" in evaluate_validator(inp).ids) == (source != "artifact_texts")


@pytest.mark.parametrize(
    "corpus,expected", [(None, False), ([], True), (["outcome=clone-failed"], False)]
)
@pytest.mark.parametrize(
    "observation",
    [
        "run=42 arm=failing command=run-test\n```text\noutcome=clone-failed\n```",
        "```captured-output run=42 arm=failing command=run-test\noutcome=clone-failed\n```",
        "Analysis: clone-failed",
    ],
)
def test_a1_corpus_selection_is_explicit(
    corpus: list[str] | None, expected: bool, observation: str
) -> None:
    inp = ValidatorInputs(
        report="Root cause: `clone-failed`\nconfidence: 0.72",
        observation_text=observation,
        artifact_texts=corpus,
    )
    assert ("A1" in evaluate_validator(inp).ids) == expected


@pytest.mark.parametrize(
    "value", ["0", "-2.5", "1e3", "true", "false", "null", '"/tmp/a,b"', "'a/b,c'"]
)
def test_a6_accepts_single_literals(value: str) -> None:
    assert (
        "A6"
        not in evaluate_validator(
            ValidatorInputs(report=f"Reference-context value: {value}\n")
        ).ids
    )


@pytest.mark.parametrize(
    "value",
    [
        "",
        " ",
        "n/a",
        "true/false",
        "true, false",
        "[1]",
        "{}",
        "true if ready",
        "NaN",
        "Infinity",
        "1e999",
        "'a' 'b'",
    ],
)
def test_a6_rejects_nonliteral_or_unevidenced_values(value: str) -> None:
    assert (
        "A6"
        in evaluate_validator(
            ValidatorInputs(report=f"Reference-context value: {value}\n")
        ).ids
    )


@pytest.mark.parametrize("source", ["report", "observation_text", "tasklist_text"])
def test_a6_checks_every_reference_row(source: str) -> None:
    inp = ValidatorInputs(report="Reference-context value: true\n")
    setattr(
        inp,
        source,
        getattr(inp, source)
        + "\n# Discriminator: second\nReference-context value: invalid\n",
    )
    assert "A6" in evaluate_validator(inp).ids


@pytest.mark.parametrize(
    "value,provenance,probe,expected",
    [
        (True, "manifest:1", "p1", False),
        (False, "manifest:1", "p1", True),
        ("false", "manifest:1", "p1", True),
        (None, "manifest:1", "p1", True),
        (True, "", "p1", True),
        (True, "manifest:1", "p2", True),
    ],
)
def test_a6_first_run_is_evidenced_and_probe_specific(
    tmp_path: Path, value: object, provenance: str, probe: str, expected: bool
) -> None:
    import json

    path = tmp_path / "fixture.md"
    path.write_text(
        "---\nassertion: A6\n---\n--- file: REPORT.md ---\n"
        "# Discriminator: p1\nReference-context value: n/a\n"
        "--- file: first-instrumented-run.json ---\n"
        + json.dumps({probe: {"value": value, "provenance": provenance}})
    )
    assert (
        "A6" in evaluate_validator(validator_inputs(load_fixture(path))).ids
    ) == expected


def test_a6_missing_reference_field_skips() -> None:
    assert (
        "A6"
        not in evaluate_validator(ValidatorInputs(report="No reference supplied")).ids
    )


@pytest.mark.parametrize(
    "listing,expected",
    [(None, False), ((), True), (("REPORT.md",), True), (("job-42.log",), False)],
)
def test_a8_listing_presence_through_loader(
    tmp_path: Path, listing: tuple[str, ...] | None, expected: bool
) -> None:
    path = tmp_path / "fixture.md"
    metadata = "" if listing is None else f"files_present: [{', '.join(listing)}]\n"
    path.write_text(
        "---\nassertion: A8\n" + metadata + "---\n--- file: execution-locus.md ---\n"
        "PRINT-SITE: GitHub Actions failing CI job build; harness result marker absent\n"
        "RUN-SITE: build.sh:1 @ ci-runner\nSAME-ENV: no\nOBSERVE-VIA: artifact-file\n"
    )
    inp = validator_inputs(load_fixture(path))
    assert inp.files_present == listing
    assert ("A8" in evaluate_validator(inp).ids) == expected


@pytest.mark.parametrize(
    "locus",
    [
        "OBSERVE-VIA: artifact-file\n",
        "PRINT-SITE: local service log\nRUN-SITE: service.py:1 @ laptop\nSAME-ENV: yes\nOBSERVE-VIA: artifact-file\n",
        "PRINT-SITE: CI job build\nRUN-SITE: build.sh:1 @ ci-runner\nSAME-ENV: no\nOBSERVE-VIA: local-exec\n",
    ],
)
def test_a8_requires_failing_ci_artifact_scope(locus: str) -> None:
    assert (
        "A8"
        not in evaluate_validator(
            ValidatorInputs(report="", locus_text=locus, files_present=("REPORT.md",))
        ).ids
    )


@pytest.mark.parametrize(
    "source,expected",
    [("artifact_texts", False), ("observation_text", True), ("report", True)],
)
def test_a8_only_raw_result_marker_counts(source: str, expected: bool) -> None:
    inp = ValidatorInputs(
        report="",
        locus_text="PRINT-SITE: CI job build\nRUN-SITE: build.sh:1 @ ci-runner\nSAME-ENV: no\nOBSERVE-VIA: artifact-file\n",
        files_present=(),
    )
    setattr(
        inp,
        source,
        ["RESULT: FAIL\n"] if source == "artifact_texts" else "RESULT: FAIL\n",
    )
    assert ("A8" in evaluate_validator(inp).ids) == expected


_A10_PROOF = (
    "## Emitter search\nemitters-found: 2\nalready-read-files: 3\nusable-capture-routes: 0\n"
    "channels searched: producer, wrapper, artifacts\n"
    "channel exclusions: producer cannot be edited; wrapper cannot access datum; artifacts omit datum\n"
    "candidate exclusions: src/a:1, src/a:2 are production emitters; a.log, b.log, c.log omit datum\n"
)

_A10_ZERO_PROOF = (
    "## Emitter search\nemitters-found: 0\nalready-read-files: 0\nusable-capture-routes: 0\n"
    "channels searched: producer, wrapper, artifacts\n"
    "channel exclusions: no emits; wrapper cannot access datum; no artifacts retained\n"
)


@pytest.mark.parametrize(
    "proof,expected",
    [
        ("## Emitter search\nemitters-found: 0\nalready-read-files: 0\n", True),
        (_A10_PROOF, False),
        (_A10_ZERO_PROOF, False),
        (_A10_ZERO_PROOF.replace("channels searched:", "unrelated:"), True),
        (_A10_ZERO_PROOF.replace("channel exclusions:", "unrelated:"), True),
        (_A10_PROOF.replace("routes: 0", "routes: 01"), True),
        (_A10_PROOF.replace("routes: 0", "routes: 0junk"), True),
        (_A10_PROOF.replace("routes: 0", "routes: 1"), True),
        (_A10_PROOF.replace("found: 2", "found: -1"), True),
        (_A10_PROOF.replace("files: 3", "files: unknown"), True),
        (_A10_PROOF.replace("channels searched:", "unrelated:"), True),
        (_A10_PROOF.replace("channel exclusions:", "unrelated:"), True),
        (_A10_PROOF.replace("candidate exclusions:", "unrelated:"), True),
        (_A10_PROOF.replace("emitters-found:", "## Elsewhere\nemitters-found:"), True),
    ],
)
def test_a10_requires_scoped_route_exhaustion(proof: str, expected: bool) -> None:
    inp = ValidatorInputs(
        report="", tasklist_text="capability-verdict: blocked\n" + proof
    )
    assert ("A10" in evaluate_validator(inp).ids) == expected


@pytest.mark.parametrize("verdict", ["n/a", "blocked-on-authorization"])
def test_a10_permission_is_not_capability_failure(verdict: str) -> None:
    assert (
        "A10"
        not in evaluate_validator(
            ValidatorInputs(report="", tasklist_text=f"capability-verdict: {verdict}\n")
        ).ids
    )


@pytest.mark.parametrize(
    "corpus,expected", [(None, False), ([], True), (["outcome=not-clone-failed"], True)]
)
def test_a1_omitted_corpus_skips_only_observation_clause(
    corpus: list[str] | None, expected: bool
) -> None:
    inp = ValidatorInputs(
        report="Root cause: `clone-failed`\nconfidence: 0.72", artifact_texts=corpus
    )
    assert ("A1" in evaluate_validator(inp).ids) == expected
    inp.calibration_texts = ["calibrated: 0.42"]
    assert "A1" in evaluate_validator(inp).ids
    inp.calibration_texts = ["calibrated: 0.72"]
    inp.report += "\n## Grounding Gaps\n`clone-failed` pending\n"
    assert "A1" in evaluate_validator(inp).ids


def test_a1_generated_prose_outside_capture_is_not_observation() -> None:
    inp = ValidatorInputs(
        report="Root cause: `clone-failed`\nconfidence: 0.72",
        observation_text="Definition: clone-failed\nAnalysis: clone-failed\n",
        artifact_texts=[],
    )
    assert "A1" in evaluate_validator(inp).ids


def test_a6_first_run_does_not_leak_to_next_probe() -> None:
    inp = ValidatorInputs(
        report="# Discriminator: p1\nReference-context value: n/a\n# Discriminator: p2\nReference-context value: n/a\n",
        first_instrumented_run={"p1": {"value": True, "provenance": "manifest:1"}},
    )
    assert "A6" in evaluate_validator(inp).ids
