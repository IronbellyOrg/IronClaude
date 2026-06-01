"""Contract #10 — Anti-instinct allowlist recurrence regression tests.

Pins documented MultiModelSwarm false-positive seed cases against the
Layer 6 phrase allowlist in ``obligation_scanner._ALLOWLIST_PHRASES``.

Source authority:
    - BUILD-REQUEST §R0 item 2, §Contract item #10
    - master:§Recurrence #6 (scaffold-vocabulary FP class)
    - /config/workspace/IronClaude/.dev/releases/Current/MultiModelSwarm/anti-instinct-remediation.md §1
    - phase-outputs/discovery/multimodelswarm-fp-seeds.md (Phase 3 Step 3.1)

Contract #1 invariant: MUST FAIL pre-fix, MUST PASS post-fix.
Negative-test guard: ``test_valid_obligation_still_flagged`` proves the
allowlist did not silently mask a real obligation.
Provenance guard: ``test_allowlist_provenance`` enforces the documentation
invariant on ``_ALLOWLIST_PHRASES`` (Step 3.3 (e)).

UV-only: ``uv run pytest tests/roadmap/test_anti_instinct_recurrence.py -v``.
"""

from __future__ import annotations

import inspect

import pytest

from superclaude.cli.roadmap import obligation_scanner
from superclaude.cli.roadmap.obligation_scanner import (
    _ALLOWLIST_PHRASES,
    _is_allowlisted,
    scan_obligations,
)

# --- Contract #10: FP fixtures (MUST FAIL pre-fix, MUST PASS post-fix) ---


@pytest.mark.parametrize(
    "recurrence_case",
    [
        ("anti_instinct", "multimodelswarm_fp_case"),
        ("anti_instinct", "stub_worker_parallelism_fp_case"),
        ("anti_instinct", "module_path_fp_case"),
    ],
    indirect=True,
)
def test_multimodelswarm_fp_demoted(recurrence_case):
    """The 3 documented MultiModelSwarm FP seed cases must NOT emit HIGH findings.

    Each fixture encodes a verbatim historical false positive from
    ``.dev/releases/Current/MultiModelSwarm/`` lines 207/211/213 + module
    path. Pre-fix the SCAFFOLD-term regex matched bare ``stub`` and emitted
    a HIGH undischarged obligation. Post-fix the Layer 6 allowlist absorbs
    the match via ``_is_allowlisted`` and the obligation is never emitted.

    Contract #10 invariant: ``expected_high_findings == 0`` AND
    ``expected_undischarged_count == 0``.
    """
    input_path, expected = recurrence_case
    content = input_path.read_text(encoding="utf-8")

    report = scan_obligations(content)

    high_findings = [o for o in report.obligations if o.severity == "HIGH"]

    assert len(high_findings) == expected["expected_high_findings"], (
        f"Fixture {expected['fixture']}: expected "
        f"{expected['expected_high_findings']} HIGH findings, got "
        f"{len(high_findings)}. Allowlist phrase(s) "
        f"{expected['expected_allowlist_phrases_matched']} should have "
        f"absorbed the SCAFFOLD match. Findings: "
        f"{[(o.term, o.context) for o in high_findings]}"
    )
    assert report.undischarged_count == expected["expected_undischarged_count"], (
        f"Fixture {expected['fixture']}: expected "
        f"{expected['expected_undischarged_count']} undischarged, got "
        f"{report.undischarged_count}"
    )
    assert report.total_obligations == expected["expected_total_obligations"], (
        f"Fixture {expected['fixture']}: expected "
        f"{expected['expected_total_obligations']} total obligations, got "
        f"{report.total_obligations}. Allowlist may have leaked."
    )


# --- Anti-regression guard: allowlist did NOT over-broaden ---


@pytest.mark.parametrize(
    "recurrence_case",
    [("anti_instinct", "valid_obligation_case")],
    indirect=True,
)
def test_valid_obligation_still_flagged(recurrence_case):
    """A genuine scaffolding obligation MUST still emit HIGH + undischarged.

    Fixture: ``Build stub authentication module`` (imperative verb +
    scaffold term, no discharge in any later milestone). If the Layer 6
    allowlist over-broadened, this fixture would stop emitting HIGH.

    The phrase ``Build stub authentication module`` is explicitly NOT in
    ``_ALLOWLIST_PHRASES`` per Contract #10's "allowlist subtracts from FPs
    only" rule.
    """
    input_path, expected = recurrence_case
    content = input_path.read_text(encoding="utf-8")

    report = scan_obligations(content)

    high_findings = [o for o in report.obligations if o.severity == "HIGH"]

    assert report.total_obligations >= expected["expected_min_total_obligations"], (
        f"Fixture {expected['fixture']}: expected ≥"
        f"{expected['expected_min_total_obligations']} total obligations, got "
        f"{report.total_obligations}. Allowlist OVER-BROADENED — Contract #10 "
        f"REGRESSION."
    )
    assert len(high_findings) >= expected["expected_min_high_findings"], (
        f"Fixture {expected['fixture']}: expected ≥"
        f"{expected['expected_min_high_findings']} HIGH findings, got "
        f"{len(high_findings)}. Allowlist OVER-BROADENED — Contract #10 "
        f"REGRESSION."
    )
    assert report.undischarged_count >= expected["expected_min_undischarged_count"], (
        f"Fixture {expected['fixture']}: expected ≥"
        f"{expected['expected_min_undischarged_count']} undischarged, got "
        f"{report.undischarged_count}. Allowlist OVER-BROADENED — Contract "
        f"#10 REGRESSION."
    )
    # The genuine-obligation phrase MUST NOT be in the allowlist.
    forbidden_phrase = expected["expected_phrase_NOT_in_allowlist"].lower()
    assert not any(forbidden_phrase in p.lower() for p in _ALLOWLIST_PHRASES), (
        f"Allowlist contains forbidden phrase '{forbidden_phrase}' that "
        f"would mask a genuine scaffolding obligation. Contract #10 "
        f"REGRESSION."
    )


# --- Provenance guard: documentation invariant on _ALLOWLIST_PHRASES ---


def test_allowlist_provenance():
    """The ``_ALLOWLIST_PHRASES`` declaration MUST cite its source authority.

    Step 3.3 (e): the comment block immediately above the
    ``_ALLOWLIST_PHRASES`` definition in ``obligation_scanner.py`` must
    reference ``BUILD-REQUEST §R0 item 2``, ``Contract #10``, and
    ``master:§Recurrence #6`` so the allowlist remains traceable to its
    historical evidence chain. The comment is contract documentation, not
    optional cosmetic prose.
    """
    source = inspect.getsource(obligation_scanner)
    # Locate the allowlist block — guard against false positives elsewhere in
    # the file by checking the substring window around the constant.
    decl_anchor = "_ALLOWLIST_PHRASES: frozenset[str]"
    assert decl_anchor in source, (
        "Allowlist constant declaration not found — Contract #10 regression."
    )
    # The provenance comment block sits in the ~50 lines immediately above
    # the declaration. Pull a window and assert the required citations.
    decl_idx = source.index(decl_anchor)
    # ~60 lines of context above the declaration is generous; the design
    # places the comment block immediately above.
    window_start = max(0, decl_idx - 4000)
    window = source[window_start:decl_idx]

    for citation in (
        "BUILD-REQUEST §R0 item 2",
        "Contract #10",
        "master:§Recurrence #6",
    ):
        assert citation in window, (
            f"_ALLOWLIST_PHRASES provenance comment missing required "
            f"citation '{citation}'. Step 3.3 (e) — Contract #10 "
            f"documentation invariant."
        )


# --- Helper-level coverage: _is_allowlisted contract ---


def test_is_allowlisted_matches_seed_phrases():
    """Every phrase in ``_ALLOWLIST_PHRASES`` must satisfy ``_is_allowlisted``.

    Catches a future regression where someone edits the helper but forgets
    to update the constant (or vice versa).
    """
    for phrase in _ALLOWLIST_PHRASES:
        # Embed the phrase in a representative roadmap-table context.
        line = f"|6|COMP-033|{phrase}|some description|module|deps|ac|S|P0|"
        assert _is_allowlisted(line), (
            f"_is_allowlisted failed to match allowlist phrase '{phrase}' "
            f"in roadmap-table context."
        )


@pytest.mark.parametrize(
    "recurrence_case",
    [("anti_instinct", "imperative_verb_with_allowlist_phrase_case")],
    indirect=True,
)
def test_imperative_verb_overrides_allowlist(recurrence_case):
    """M8 fix-up — imperative verb + SCAFFOLD term overrides Layer 6 allowlist.

    Source authority: sc:reflect UC-2 Phase-3 validation, MEDIUM Finding
    ``M8 — substring-match FN`` at
    ``/config/workspace/IronClaude/.dev/reflect/phase-3-r0.2-uc2-validation/REPORT.md``.

    Pre-fix: the Layer 6 short-circuit at ``obligation_scanner.py:280`` runs
    before the imperative-verb checks and silently allowlists a line like
    ``|1|FR-001|Build stub transport now|temporary stub transport — must be
    replaced in M2|...|`` because the substring ``stub transport`` matches
    ``_ALLOWLIST_PHRASES``. The line emits zero obligations.

    Post-fix: ``_is_allowlisted`` consults
    ``_ALLOWLIST_IMPERATIVE_OVERRIDE_RE`` and returns ``False`` when the line
    pairs an imperative verb (build / create / set up / generate / write /
    add / implement / stand up) with a SCAFFOLD term. The line is no longer
    short-circuited and emits 3 HIGH undischarged obligations (2x ``stub`` +
    1x ``temporary``), matching the genuine-scaffolding signal in the row.

    Contract #1 invariant: MUST FAIL pre-fix, MUST PASS post-fix.
    Contract #10 invariant: allowlist subtracts from FPs only — never masks
    a genuine obligation.
    """
    input_path, expected = recurrence_case
    content = input_path.read_text(encoding="utf-8")

    report = scan_obligations(content)

    high_findings = [o for o in report.obligations if o.severity == "HIGH"]

    assert report.total_obligations == expected["expected_total_obligations"], (
        f"Fixture {expected['fixture']}: expected "
        f"{expected['expected_total_obligations']} total obligations, got "
        f"{report.total_obligations}. M8 fix may have regressed — the "
        f"imperative-verb override should bypass the Layer 6 allowlist."
    )
    assert len(high_findings) == expected["expected_high_findings"], (
        f"Fixture {expected['fixture']}: expected "
        f"{expected['expected_high_findings']} HIGH findings, got "
        f"{len(high_findings)}. M8 — substring-match FN regression. "
        f"Findings: {[(o.term, o.context) for o in high_findings]}"
    )
    assert report.undischarged_count == expected["expected_undischarged_count"], (
        f"Fixture {expected['fixture']}: expected "
        f"{expected['expected_undischarged_count']} undischarged, got "
        f"{report.undischarged_count}. M8 — substring-match FN regression."
    )


def test_is_allowlisted_rejects_unrelated_scaffold_prose():
    """``_is_allowlisted`` MUST return False for unrelated scaffold prose.

    Guards against accidentally promoting the substring match to a regex or
    a too-broad token match.
    """
    unrelated_lines = [
        "Build stub authentication module",
        "Replace mocked steps with real implementations",
        "The placeholder config will be wired up in M3",
        "Add a fake service client for external calls",
    ]
    for line in unrelated_lines:
        assert not _is_allowlisted(line), (
            f"_is_allowlisted incorrectly matched unrelated line '{line}' — "
            f"allowlist over-broadened. Contract #10 REGRESSION."
        )
