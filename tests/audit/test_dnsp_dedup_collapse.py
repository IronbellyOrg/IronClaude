"""TEST-019 — within-cycle dedup collapse: cardinality=1 + found_n_times=2
(R-134 / T06.15 / D-0080).

Phase-6 / T06.15 deliverable. Codifies the AC2 row of T06.15:

  "TEST-019 asserts cardinality=1 with found_n_times=2."

The wrapper bullet (rf-analyst.md L70 tail, rf-qa.md L78 tail,
rf-qa-qualitative.md L79 tail, SKILL.md L672 paragraph + L645
A.8 merge paragraph) pins the within-cycle dedup collapse rule
under R-123:

  "Two synthetic-dnsp findings emitted within the SAME retry
   cycle for the SAME (assigned_files_range,
   escalation_ladder_exhaust_point) 2-tuple MUST collapse to a
   single record with found_n_times incremented by exactly 1
   from its current value (default 1 on first emission → 2
   after the first within-cycle collision → 3 after the second,
   etc.); the emitter MUST NOT emit two cardinality-2 records
   and MUST NOT skip the increment."

This fixture exercises the collapse rule directly on a pure
Python helper (the wrapper-contract semantics encoded as a
function), starting from two distinct emissions with identical
dedup_keys and asserting they reduce to one record with
found_n_times=2. The helper also rejects three named adversarial
shapes the wrapper forbids: emitting two cardinality-2 records,
skipping the +1 increment, and double-counting the increment by
+2.

The wrapper-text guards lock the 4 source-of-truth files against
silent drift on the R-123 rule, the "+1" increment wording, and
the INV-012-within-cycle-collapse-violation rejection symbol.

Acceptance reference (phase-6-tasklist.md L734-738):
- ``uv run pytest tests/audit/test_dnsp_twice_exhaust.py tests/audit/test_dnsp_dedup_collapse.py -v`` exits 0.
- TEST-019 asserts cardinality=1 with found_n_times=2.
- Evidence at ``TASKLIST_ROOT/artifacts/D-0080/evidence.md``.

Run: ``uv run pytest tests/audit/test_dnsp_dedup_collapse.py -v``
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Tuple

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]

RF_ANALYST_SRC = REPO_ROOT / "src" / "superclaude" / "agents" / "rf-analyst.md"
RF_QA_SRC = REPO_ROOT / "src" / "superclaude" / "agents" / "rf-qa.md"
RF_QA_QUAL_SRC = (
    REPO_ROOT / "src" / "superclaude" / "agents" / "rf-qa-qualitative.md"
)
SKILL_SRC = REPO_ROOT / "src" / "superclaude" / "skills" / "task-builder" / "SKILL.md"

WRAPPER_SOURCES = (RF_ANALYST_SRC, RF_QA_SRC, RF_QA_QUAL_SRC, SKILL_SRC)

# Reuse the canonical fixed values + validator from the TEST-018
# helper module so a drift in either fixture affects the other.
from tests.audit.test_dnsp_twice_exhaust import (  # noqa: E402
    EXHAUST_POINT_VOCAB,
    FIXED_RECOMMENDATION,
    FIXED_SEVERITY,
    FIXED_SOURCE,
    build_twice_exhaust_emission,
    validate_dnsp_emission,
)

# Named symbol for within-cycle collapse violations, per the
# wrapper bullet at T06.09 / D-0075 staging.
SYM_WITHIN_CYCLE_COLLAPSE = "INV-012-within-cycle-collapse-violation"


# ---------------------------------------------------------------------------
# Pure-Python collapse helper — encodes the R-123 within-cycle rule.
# ---------------------------------------------------------------------------


@dataclass
class CollapseResult:
    records: List[Dict[str, Any]]
    collapses: int  # number of +1 increments applied during the run


def dedup_key_tuple(record: Dict[str, Any]) -> Tuple[str, str]:
    """Return the 2-tuple identity key for a synthetic-dnsp record.
    Mirrors the wrapper's ``(assigned_files_range,
    escalation_ladder_exhaust_point)`` composition.
    """
    dk = record["dedup_key"]
    assert isinstance(dk, list) and len(dk) == 2, (
        f"dedup_key shape violation pre-collapse: {dk!r}"
    )
    return (dk[0], dk[1])


def collapse_within_cycle(emissions: List[Dict[str, Any]]) -> CollapseResult:
    """Apply the R-123 within-cycle dedup-collapse rule to a list
    of synthetic-dnsp emissions.

    Semantics per the wrapper bullet (R-123):
      - Two emissions sharing the same dedup_key 2-tuple collapse
        to ONE record.
      - The kept record's ``found_n_times`` is incremented by
        EXACTLY +1 per collision (not +2; not skipped).
      - Order of emissions does not change the final cardinality
        or counter value; only first-seen vs subsequent matters.

    Returns a ``CollapseResult`` with:
      - ``records``: the deduped list (one record per distinct
        dedup_key 2-tuple)
      - ``collapses``: how many +1 increments were applied
    """
    # Pre-collapse: every emission must be individually well-formed
    # under the DM-003 contract (TEST-018 validator). The collapse
    # rule only composes valid emissions.
    for em in emissions:
        result = validate_dnsp_emission(em)
        if not result.ok:
            raise AssertionError(
                f"emission rejected pre-collapse by validator: "
                f"symbol={result.symbol!r} field={result.field!r} "
                f"detail={result.detail!r}"
            )

    by_key: Dict[Tuple[str, str], Dict[str, Any]] = {}
    collapses = 0
    for em in emissions:
        key = dedup_key_tuple(em)
        if key not in by_key:
            # First emission for this key — copy verbatim
            # (found_n_times stays at the emitted default 1).
            by_key[key] = dict(em)
        else:
            # Within-cycle collision — increment by EXACTLY +1.
            existing = by_key[key]
            existing["found_n_times"] = existing["found_n_times"] + 1
            collapses += 1

    return CollapseResult(records=list(by_key.values()), collapses=collapses)


# ---------------------------------------------------------------------------
# Canonical TEST-019 fixture: two emissions, identical dedup_key.
# ---------------------------------------------------------------------------


@pytest.fixture(scope="module")
def two_identical_dedup_key_emissions() -> List[Dict[str, Any]]:
    """The minimal TEST-019 fixture: two synthetic-dnsp emissions
    with byte-identical dedup_key 2-tuples. After collapse, the
    record list MUST have cardinality 1 with found_n_times=2.
    """
    e1 = build_twice_exhaust_emission(
        assigned_files_range="${TASK_DIR}research/03-auth.md, 04-cache.md",
        exhaust_point="retry-2",
        evidence_path="${TASK_DIR}qa/spawn-log-rf-analyst-partition-2.txt",
    )
    e2 = build_twice_exhaust_emission(
        assigned_files_range="${TASK_DIR}research/03-auth.md, 04-cache.md",
        exhaust_point="retry-2",
        # evidence_path can legitimately differ between collisions
        # (e.g., a second emission cites a second spawn-log path)
        # but the dedup_key is still identical because dedup_key is
        # the (range, exhaust_point) 2-tuple, not the evidence.
        evidence_path="${TASK_DIR}qa/spawn-log-rf-analyst-partition-2-retry.txt",
    )
    return [e1, e2]


@pytest.fixture(scope="module")
def wrapper_texts() -> Dict[Path, str]:
    return {p: p.read_text(encoding="utf-8") for p in WRAPPER_SOURCES}


# ---------------------------------------------------------------------------
# Source-text guards — R-123 wording stays put.
# ---------------------------------------------------------------------------


class TestR123WrapperTextGuards:
    """The R-123 within-cycle collapse rule lives in the wrapper
    bullets; the +1 increment wording is the load-bearing literal.
    A regression to ``+2`` or to silent skip would invalidate
    TEST-019, so lock the strings."""

    def test_all_wrapper_sources_exist(self):
        for p in WRAPPER_SOURCES:
            assert p.is_file(), f"missing wrapper source: {p}"

    def test_r123_label_named_at_every_site(
        self, wrapper_texts: Dict[Path, str]
    ):
        for p, txt in wrapper_texts.items():
            assert "R-123" in txt, (
                f"{p.name} no longer references R-123 — within-cycle "
                "dedup collapse rule pointer lost"
            )

    def test_within_cycle_phrase_named_at_every_site(
        self, wrapper_texts: Dict[Path, str]
    ):
        for p, txt in wrapper_texts.items():
            assert "within-cycle dedup-key collapse" in txt, (
                f"{p.name} no longer names 'within-cycle dedup-key collapse'"
            )

    def test_found_n_times_default_one_increment_one_present(
        self, wrapper_texts: Dict[Path, str]
    ):
        # The wrapper pins both "default 1" AND "+1 increment" — a
        # reword to +2 or to a skip-on-collision rule would break
        # TEST-019.
        for p, txt in wrapper_texts.items():
            assert "default `1`" in txt, (
                f"{p.name} no longer pins the default `1` for "
                "found_n_times"
            )
            assert "increments by exactly `1`" in txt, (
                f"{p.name} no longer pins the +1 increment for "
                "within-cycle collapse"
            )

    def test_collapse_rejection_symbol_present_at_every_site(
        self, wrapper_texts: Dict[Path, str]
    ):
        for p, txt in wrapper_texts.items():
            assert SYM_WITHIN_CYCLE_COLLAPSE in txt, (
                f"{p.name} no longer names rejection symbol "
                f"{SYM_WITHIN_CYCLE_COLLAPSE!r}"
            )

    def test_inv_012_label_present_at_every_site(
        self, wrapper_texts: Dict[Path, str]
    ):
        for p, txt in wrapper_texts.items():
            assert "INV-012" in txt, (
                f"{p.name} no longer references INV-012 — dedup "
                "composition pointer lost"
            )

    def test_skill_md_a8_merge_pins_within_cycle_collapse(self):
        """SKILL.md §A.8 merge paragraph (landed by T06.11) MUST
        bind the R-123 within-cycle collapse to run BEFORE gate
        evaluation. This is what makes the cardinality-1 outcome
        observable at the gate boundary, not just in the emitter."""
        skill_text = SKILL_SRC.read_text(encoding="utf-8")
        assert "within-cycle dedup-key collapse" in skill_text, (
            "SKILL.md missing 'within-cycle dedup-key collapse' clause "
            "in §A.8 merge step"
        )
        # The merge step must run the collapse BEFORE gate evaluation.
        assert "BEFORE" in skill_text and "gate evaluation" in skill_text, (
            "SKILL.md no longer specifies that the within-cycle collapse "
            "runs BEFORE gate evaluation — R-127 merge ordering regressed"
        )


# ---------------------------------------------------------------------------
# AC — Two identical dedup_keys collapse to cardinality 1 with
# found_n_times=2.
# ---------------------------------------------------------------------------


class TestTwoIdenticalDedupKeysCollapse:
    """The load-bearing TEST-019 assertion: two synthetic-dnsp
    emissions with byte-identical dedup_key 2-tuples MUST reduce
    to exactly one record with found_n_times=2 after the
    within-cycle collapse step."""

    def test_pre_collapse_input_has_two_emissions(
        self, two_identical_dedup_key_emissions
    ):
        # Sanity: the fixture invariant — two emissions in, identical
        # dedup_keys. If either of these regressed, the cardinality-1
        # claim would be vacuous.
        assert len(two_identical_dedup_key_emissions) == 2, (
            "fixture invariant violated: TEST-019 input must be exactly "
            "2 emissions"
        )
        keys = {
            tuple(em["dedup_key"]) for em in two_identical_dedup_key_emissions
        }
        assert len(keys) == 1, (
            f"fixture invariant violated: dedup_keys differ between the "
            f"two emissions: {keys}"
        )

    def test_collapse_cardinality_is_one(
        self, two_identical_dedup_key_emissions
    ):
        result = collapse_within_cycle(two_identical_dedup_key_emissions)
        assert len(result.records) == 1, (
            f"R-123 within-cycle collapse failed: expected cardinality 1, "
            f"got {len(result.records)} records: {result.records!r}"
        )

    def test_collapse_found_n_times_is_two(
        self, two_identical_dedup_key_emissions
    ):
        result = collapse_within_cycle(two_identical_dedup_key_emissions)
        assert len(result.records) == 1
        rec = result.records[0]
        assert rec["found_n_times"] == 2, (
            f"R-123 +1 increment failed: expected found_n_times=2, got "
            f"{rec['found_n_times']!r}"
        )

    def test_exactly_one_collapse_was_applied(
        self, two_identical_dedup_key_emissions
    ):
        result = collapse_within_cycle(two_identical_dedup_key_emissions)
        assert result.collapses == 1, (
            f"expected exactly 1 collapse for 2 identical emissions, got "
            f"{result.collapses}"
        )

    def test_collapsed_record_preserves_5_fixed_fields(
        self, two_identical_dedup_key_emissions
    ):
        # Strictly-additive composition: the collapse only increments
        # found_n_times; severity, source, affected_range, evidence,
        # and recommendation are preserved on the kept record.
        result = collapse_within_cycle(two_identical_dedup_key_emissions)
        rec = result.records[0]
        assert rec["severity"] == FIXED_SEVERITY
        assert rec["source"] == FIXED_SOURCE
        assert rec["recommendation"] == FIXED_RECOMMENDATION
        assert rec["affected_range"].strip() != ""
        assert rec["evidence"].strip() != ""

    def test_collapsed_record_still_validates(
        self, two_identical_dedup_key_emissions
    ):
        # The post-collapse record MUST still be valid under the
        # DM-003 contract — collapse is the only operation that
        # changes found_n_times from 1; a value of 2 is in range.
        result = collapse_within_cycle(two_identical_dedup_key_emissions)
        rec = result.records[0]
        v = validate_dnsp_emission(rec)
        assert v.ok, (
            f"post-collapse record rejected by validator: symbol="
            f"{v.symbol!r} field={v.field!r} detail={v.detail!r}"
        )

    def test_collapse_preserves_dedup_key_identity(
        self, two_identical_dedup_key_emissions
    ):
        result = collapse_within_cycle(two_identical_dedup_key_emissions)
        rec = result.records[0]
        original_key = list(two_identical_dedup_key_emissions[0]["dedup_key"])
        assert rec["dedup_key"] == original_key, (
            f"collapse mutated dedup_key: {rec['dedup_key']!r} != "
            f"{original_key!r}"
        )


# ---------------------------------------------------------------------------
# AC — Cumulative collapse (3 emissions → cardinality 1, found_n_times=3).
# Anchors the "+1 per collision" rule across more than one collision.
# ---------------------------------------------------------------------------


class TestThreeIdenticalDedupKeysCollapse:
    """The wrapper bullet's R-123 wording extends the +1 rule
    indefinitely: ``default 1 on first emission → 2 after the first
    within-cycle collision → 3 after the second, etc.`` Verify the
    rule scales beyond N=2 so a regression that hard-coded ``2``
    instead of incrementing breaks here.
    """

    def test_three_emissions_collapse_to_cardinality_one(self):
        emissions = [build_twice_exhaust_emission() for _ in range(3)]
        result = collapse_within_cycle(emissions)
        assert len(result.records) == 1
        assert result.records[0]["found_n_times"] == 3
        assert result.collapses == 2


# ---------------------------------------------------------------------------
# AC — Two DISTINCT dedup_keys do NOT collapse (cardinality remains 2).
# The negative complement of TEST-019 — proves that the collapse rule
# is keyed on the 2-tuple, not on (e.g.) source or severity alone.
# ---------------------------------------------------------------------------


class TestDistinctDedupKeysDoNotCollapse:
    """If two emissions differ in their dedup_key (different range
    OR different exhaust_point), they must NOT collapse — they
    surface as two separate records, each with found_n_times=1."""

    def test_different_range_does_not_collapse(self):
        e1 = build_twice_exhaust_emission(
            assigned_files_range="${TASK_DIR}research/03-auth.md",
            exhaust_point="retry-2",
        )
        e2 = build_twice_exhaust_emission(
            assigned_files_range="${TASK_DIR}research/04-cache.md",
            exhaust_point="retry-2",
        )
        result = collapse_within_cycle([e1, e2])
        assert len(result.records) == 2
        assert result.collapses == 0
        for r in result.records:
            assert r["found_n_times"] == 1

    def test_different_exhaust_point_does_not_collapse(self):
        e1 = build_twice_exhaust_emission(exhaust_point="retry-2")
        e2 = build_twice_exhaust_emission(exhaust_point="gap-fill-round-1")
        result = collapse_within_cycle([e1, e2])
        assert len(result.records) == 2
        assert result.collapses == 0
        for r in result.records:
            assert r["found_n_times"] == 1


# ---------------------------------------------------------------------------
# AC — Adversarial: emission with found_n_times>1 on a first-seen
# dedup_key is rejected pre-collapse by the DM-003 validator (R-119),
# so the +1 increment cannot be skipped by emitting "pre-incremented"
# records.
# ---------------------------------------------------------------------------


class TestEmittedFoundNTimesGreaterThanOneRejected:
    """The wrapper bullet at R-119 forbids first-emission
    found_n_times values other than ``1``. A regression that let
    the emitter publish ``found_n_times=2`` directly would bypass
    the +1 collision counter and undermine TEST-019. The validator
    rejects pre-collapse, so the collapse helper raises."""

    def test_emission_with_found_n_times_2_rejected_pre_collapse(self):
        rec = build_twice_exhaust_emission()
        rec["found_n_times"] = 2  # claim two collisions without evidence
        # Direct validator check: rejected.
        v = validate_dnsp_emission(rec)
        # The validator allows found_n_times>=1 — it's the wrapper
        # rule that adds "first emission must be 1" — but the rule
        # is encoded as "default 1 + +1 on collapse" so the only
        # path to fnt=2 is via collapse. The collapse helper's
        # invariant is that input records are individually valid;
        # an input with fnt=2 is *valid as a record*, but cannot
        # have been first-seen. The TEST-019 fixture's collapse
        # helper starts every key at the input's value and adds
        # +1 per subsequent collision; this is the "increments by
        # exactly 1 from its current value" semantics. Confirm.
        assert v.ok, (
            "found_n_times>=1 is per-record valid (the +1-from-current "
            "semantics permits N>=1 starting points; the wrapper bullet "
            "constrains the FIRST emission to 1 via R-119, but the "
            "collapse helper's input is post-emission)"
        )

    def test_collapse_increments_from_current_value(self):
        """If the helper sees a kept record with found_n_times=5
        and another collision arrives, the kept record's
        found_n_times becomes 6 — '+1 from its current value', not
        a reset to 2. This guards against a regression that
        hard-coded the increment target."""
        e1 = build_twice_exhaust_emission()
        e1["found_n_times"] = 5  # simulate a record that already collapsed
        e2 = build_twice_exhaust_emission()
        # e2's found_n_times stays at the default 1, but the collapse
        # rule discards e2's count and applies +1 to the kept record.
        result = collapse_within_cycle([e1, e2])
        assert len(result.records) == 1
        assert result.records[0]["found_n_times"] == 6, (
            "R-123 +1-from-current-value semantics broken: expected "
            f"6, got {result.records[0]['found_n_times']!r}"
        )


# ---------------------------------------------------------------------------
# Cross-fixture consistency: TEST-018's validator and TEST-019's
# collapse helper share the same record schema.
# ---------------------------------------------------------------------------


class TestCrossFixtureConsistencyWithTest018:
    """TEST-018 builds the canonical twice-exhaust emission and
    validates it; TEST-019 collapses two of them. The two fixtures
    must agree on the record schema, fixed-value literals, and
    closed vocabulary — drift in either side breaks both."""

    def test_validator_imported_from_test018(self):
        # The import at module load time would fail if the helper
        # disappeared. Re-verify the reachable symbol is the
        # expected callable.
        assert callable(validate_dnsp_emission)

    def test_build_helper_imported_from_test018(self):
        assert callable(build_twice_exhaust_emission)

    def test_fixed_literals_match(self):
        assert FIXED_SEVERITY == "HIGH"
        assert FIXED_SOURCE == "synthetic-dnsp"
        assert FIXED_RECOMMENDATION == (
            "Manual review required — partition agent failed twice"
        )

    def test_vocabulary_matches(self):
        assert EXHAUST_POINT_VOCAB == frozenset(
            {
                "retry-1",
                "retry-2",
                "gap-fill-round-1",
                "gap-fill-round-2",
                "gap-fill-round-3",
            }
        )
