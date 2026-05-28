"""TEST-018 — twice-exhaust synthetic-dnsp emission (R-133 / T06.15 / D-0080).

Phase-6 / T06.15 deliverable. Codifies the AC1 row of T06.15:

  "TEST-018 asserts all 5 fixed fields populated; severity HIGH;
   source synthetic-dnsp."

Per the DM-003-M6 contract (T06.02 / D-0069) the synthetic-dnsp
finding has a 7-field schema:

  1. ``severity``              — fixed-value invariant, byte-literal ``HIGH``
  2. ``source``                — fixed-value invariant, byte-literal ``synthetic-dnsp``
  3. ``affected_range``        — verbatim ``assigned_files`` slice (dynamic, never blank)
  4. ``evidence``              — spawn-log path or evidence-absence stub (dynamic, never blank)
  5. ``recommendation``        — fixed string ``Manual review required — partition agent failed twice``
  6. ``dedup_key``             — 2-tuple ``(assigned_files_range, escalation_ladder_exhaust_point)``
  7. ``found_n_times``         — int, default ``1``; +1 on within-cycle collapse

T06.15 binds the "all 5 fixed fields populated" claim of the AC to
fields 1-5 (severity + source + affected_range + evidence +
recommendation — the five fields the wrapper bullet enumerates as
"fixed or dynamic-but-never-blank" baseline content; dedup_key and
found_n_times are the two additional 7-field-schema entries that
TEST-019 covers).

The fixture builds a canonical "twice-exhaust" emission (the
partition agent failed retry-1 and exhausted retry-2; the
``escalation_ladder_exhaust_point`` is the closed-vocabulary value
``retry-2``), feeds it through a pure-Python validator that encodes
the four wrapper-level rejection contracts from T06.03–T06.05
(``DM-003-fixed-field-invariant-violation``,
``DM-003-dynamic-field-invariant-violation``,
``DM-003-recommendation-invariant-violation``,
``DM-003-dedup-key-shape-violation``,
``DM-003-found-n-times-invariant-violation``), and asserts the
positive emission passes AND each negative-path tweak that drops or
corrupts a fixed/dynamic field is rejected with the named symbol.

The wrapper-text guards lock the 4 source-of-truth files
(``rf-analyst.md``, ``rf-qa.md``, ``rf-qa-qualitative.md``,
``SKILL.md``) against silent drift on the literal ``HIGH``,
``synthetic-dnsp``, ``Manual review required — partition agent
failed twice``, and 7-field-schema strings, so a regression to one
of these literals breaks this fixture.

Acceptance reference (phase-6-tasklist.md L734-738):
- ``uv run pytest tests/audit/test_dnsp_twice_exhaust.py tests/audit/test_dnsp_dedup_collapse.py -v`` exits 0.
- TEST-018 asserts all 5 fixed fields populated; severity HIGH; source synthetic-dnsp.
- Evidence at ``TASKLIST_ROOT/artifacts/D-0080/evidence.md``.

Run: ``uv run pytest tests/audit/test_dnsp_twice_exhaust.py -v``
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Optional

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]

RF_ANALYST_SRC = REPO_ROOT / "src" / "superclaude" / "agents" / "rf-analyst.md"
RF_QA_SRC = REPO_ROOT / "src" / "superclaude" / "agents" / "rf-qa.md"
RF_QA_QUAL_SRC = (
    REPO_ROOT / "src" / "superclaude" / "agents" / "rf-qa-qualitative.md"
)
SKILL_SRC = REPO_ROOT / "src" / "superclaude" / "skills" / "task-builder" / "SKILL.md"

WRAPPER_SOURCES = (RF_ANALYST_SRC, RF_QA_SRC, RF_QA_QUAL_SRC, SKILL_SRC)

# Closed vocabulary for the escalation_ladder_exhaust_point field
# (API-003-M6 / R-121). The wrapper bullet pins these five literals
# as the only legal second-element values for dedup_key.
EXHAUST_POINT_VOCAB = frozenset(
    {
        "retry-1",
        "retry-2",
        "gap-fill-round-1",
        "gap-fill-round-2",
        "gap-fill-round-3",
    }
)

# Fixed-value literals pinned by the wrapper bullet (R-113 + R-114 +
# R-117). Byte-exact, case-sensitive — drift here is a contract break.
FIXED_SEVERITY = "HIGH"
FIXED_SOURCE = "synthetic-dnsp"
FIXED_RECOMMENDATION = "Manual review required — partition agent failed twice"

# Named rejection symbols pinned by the wrapper bullets at T06.03,
# T06.04, T06.05. These are the surface contract — drift breaks this
# fixture and downstream evidence packs.
SYM_FIXED_FIELD = "DM-003-fixed-field-invariant-violation"
SYM_DYNAMIC_FIELD = "DM-003-dynamic-field-invariant-violation"
SYM_RECOMMENDATION = "DM-003-recommendation-invariant-violation"
SYM_DEDUP_KEY_SHAPE = "DM-003-dedup-key-shape-violation"
SYM_FOUND_N_TIMES = "DM-003-found-n-times-invariant-violation"


# ---------------------------------------------------------------------------
# Pure-Python validator — encodes the wrapper rejection contracts.
# ---------------------------------------------------------------------------


@dataclass
class ValidationResult:
    """Outcome of validating a candidate synthetic-dnsp emission.

    A passing validation has ``ok == True`` and ``symbol is None``;
    a rejection has ``ok == False`` and ``symbol`` set to one of the
    named DM-003 / API-003 rejection symbols pinned by the wrapper
    bullets. ``field`` records the field that failed (for diagnostics).
    """

    ok: bool
    symbol: Optional[str] = None
    field: Optional[str] = None
    detail: Optional[str] = None


REQUIRED_FIELDS = (
    "severity",
    "source",
    "affected_range",
    "evidence",
    "recommendation",
    "dedup_key",
    "found_n_times",
)

FIXED_FIELDS = ("severity", "source")
DYNAMIC_FIELDS = ("affected_range", "evidence")


def validate_dnsp_emission(record: Dict[str, Any]) -> ValidationResult:
    """Validate a candidate synthetic-dnsp finding against the
    7-field DM-003-M6 contract.

    Encodes the wrapper-level rejection contracts from T06.03
    (R-113 + R-114), T06.04 (R-115 + R-116), and T06.05
    (R-117 + R-118 + R-119), all of which are pinned at all four
    wrapper sites per D-0070, D-0071, D-0072.

    Order of checks follows wrapper enumeration: schema → fixed
    fields → dynamic fields → recommendation → dedup_key shape +
    vocabulary → found_n_times shape.
    """
    # Schema-presence: all 7 fields named.
    for fname in REQUIRED_FIELDS:
        if fname not in record:
            return ValidationResult(
                ok=False,
                symbol=SYM_FIXED_FIELD if fname in FIXED_FIELDS
                else SYM_DYNAMIC_FIELD if fname in DYNAMIC_FIELDS
                else SYM_RECOMMENDATION if fname == "recommendation"
                else SYM_DEDUP_KEY_SHAPE if fname == "dedup_key"
                else SYM_FOUND_N_TIMES,
                field=fname,
                detail=f"required field {fname!r} missing",
            )

    # Fixed-field invariants (R-113 + R-114).
    if record["severity"] != FIXED_SEVERITY:
        return ValidationResult(
            ok=False, symbol=SYM_FIXED_FIELD, field="severity",
            detail=f"severity={record['severity']!r} != {FIXED_SEVERITY!r}",
        )
    if record["source"] != FIXED_SOURCE:
        return ValidationResult(
            ok=False, symbol=SYM_FIXED_FIELD, field="source",
            detail=f"source={record['source']!r} != {FIXED_SOURCE!r}",
        )

    # Dynamic-field never-blank invariants (R-115 + R-116).
    for fname in DYNAMIC_FIELDS:
        val = record[fname]
        if not isinstance(val, str) or val.strip() == "":
            return ValidationResult(
                ok=False, symbol=SYM_DYNAMIC_FIELD, field=fname,
                detail=f"{fname} is blank/whitespace/non-string",
            )

    # Recommendation byte-exact (R-117).
    if record["recommendation"] != FIXED_RECOMMENDATION:
        return ValidationResult(
            ok=False, symbol=SYM_RECOMMENDATION, field="recommendation",
            detail=f"recommendation={record['recommendation']!r} != "
                   f"{FIXED_RECOMMENDATION!r}",
        )

    # dedup_key 2-tuple shape + closed vocabulary (R-118 + R-121).
    dk = record["dedup_key"]
    if not isinstance(dk, list) or len(dk) != 2:
        return ValidationResult(
            ok=False, symbol=SYM_DEDUP_KEY_SHAPE, field="dedup_key",
            detail=f"dedup_key not 2-element list: {dk!r}",
        )
    if not isinstance(dk[0], str) or dk[0].strip() == "":
        return ValidationResult(
            ok=False, symbol=SYM_DEDUP_KEY_SHAPE, field="dedup_key",
            detail=f"dedup_key[0] (range) is blank: {dk[0]!r}",
        )
    if dk[1] not in EXHAUST_POINT_VOCAB:
        return ValidationResult(
            ok=False, symbol=SYM_DEDUP_KEY_SHAPE, field="dedup_key",
            detail=f"dedup_key[1]={dk[1]!r} not in vocabulary "
                   f"{sorted(EXHAUST_POINT_VOCAB)}",
        )

    # found_n_times int default 1 + positive (R-119).
    fnt = record["found_n_times"]
    if not isinstance(fnt, int) or isinstance(fnt, bool):
        return ValidationResult(
            ok=False, symbol=SYM_FOUND_N_TIMES, field="found_n_times",
            detail=f"found_n_times is not int: {fnt!r}",
        )
    if fnt < 1:
        return ValidationResult(
            ok=False, symbol=SYM_FOUND_N_TIMES, field="found_n_times",
            detail=f"found_n_times={fnt} < 1",
        )

    return ValidationResult(ok=True)


def build_twice_exhaust_emission(
    *,
    assigned_files_range: str = "${TASK_DIR}research/03-auth.md, 04-cache.md",
    exhaust_point: str = "retry-2",
    evidence_path: str = (
        "${TASK_DIR}qa/spawn-log-rf-analyst-partition-2.txt"
    ),
) -> Dict[str, Any]:
    """Construct the canonical TEST-018 emission: a partition agent
    has failed retry-1 and exhausted retry-2 (the "twice-exhaust"
    case named in the AC). Defaults align with the example output
    block at ``rf-analyst.md:77-87`` (post-T06.05 byte-exact
    recommendation; dedup_key vocabulary value ``retry-2``).
    """
    return {
        "severity": FIXED_SEVERITY,
        "source": FIXED_SOURCE,
        "affected_range": assigned_files_range,
        "evidence": evidence_path,
        "recommendation": FIXED_RECOMMENDATION,
        "dedup_key": [assigned_files_range, exhaust_point],
        "found_n_times": 1,
    }


# ---------------------------------------------------------------------------
# Fixtures.
# ---------------------------------------------------------------------------


@pytest.fixture(scope="module")
def twice_exhaust_emission() -> Dict[str, Any]:
    return build_twice_exhaust_emission()


@pytest.fixture(scope="module")
def wrapper_texts() -> Dict[Path, str]:
    return {p: p.read_text(encoding="utf-8") for p in WRAPPER_SOURCES}


# ---------------------------------------------------------------------------
# Source-text guards — wrapper-bullet literals stay put.
# ---------------------------------------------------------------------------


class TestWrapperContractTextGuards:
    """The four wrapper sites must keep naming the literals + the
    rejection symbols this fixture depends on. A reword would
    invalidate the runtime assertions, so lock the strings via grep.
    """

    def test_all_wrapper_sources_exist(self):
        for p in WRAPPER_SOURCES:
            assert p.is_file(), f"missing wrapper source: {p}"

    def test_synthetic_dnsp_sentinel_present_at_every_site(
        self, wrapper_texts: Dict[Path, str]
    ):
        for p, txt in wrapper_texts.items():
            assert FIXED_SOURCE in txt, (
                f"{p.name} no longer names the literal {FIXED_SOURCE!r} "
                "sentinel — operator-inspection contract broken"
            )

    def test_high_severity_literal_present_at_every_site(
        self, wrapper_texts: Dict[Path, str]
    ):
        for p, txt in wrapper_texts.items():
            assert "HIGH" in txt, (
                f"{p.name} no longer names the literal HIGH severity — "
                "DM-003 severity contract drift"
            )

    def test_recommendation_byte_exact_at_every_site(
        self, wrapper_texts: Dict[Path, str]
    ):
        for p, txt in wrapper_texts.items():
            assert FIXED_RECOMMENDATION in txt, (
                f"{p.name} no longer contains the byte-exact "
                f"recommendation literal {FIXED_RECOMMENDATION!r}"
            )

    def test_dm_003_schema_named_at_every_site(
        self, wrapper_texts: Dict[Path, str]
    ):
        # The "DM-003" schema label is the load-bearing pointer
        # tying the wrapper to the M1 contract-freeze entity. The
        # three agent sites elaborate this as "7-field DM-003
        # contract"; SKILL.md describes it via component invariants
        # ("DM-003 emitter rejection contract", "DM-003 contract
        # row"). The shared anchor is the literal "DM-003".
        for p, txt in wrapper_texts.items():
            assert "DM-003" in txt, (
                f"{p.name} no longer references the DM-003 schema — "
                "M1 contract-freeze pointer regressed"
            )

    def test_seven_field_phrasing_present_at_agent_sites(
        self, wrapper_texts: Dict[Path, str]
    ):
        # The "7-field DM-003 contract" phrasing appears at the three
        # agent sites — SKILL.md uses a longer rationale-style
        # description instead. Locking the agent-site phrasing keeps
        # the schema-cardinality claim auditable from the wrapper.
        agent_sites = (RF_ANALYST_SRC, RF_QA_SRC, RF_QA_QUAL_SRC)
        for p in agent_sites:
            txt = wrapper_texts[p]
            assert "7-field DM-003 contract" in txt, (
                f"{p.name} no longer pins '7-field DM-003 contract' "
                "phrase — schema cardinality assertion regressed"
            )

    def test_twice_exhaust_trigger_named_at_every_agent_site(
        self, wrapper_texts: Dict[Path, str]
    ):
        # The trigger phrase that scopes WHEN a synthetic-dnsp emits:
        # "after the single retry AND exhausts its escalation ladder".
        # The three agent sites all use this exact phrasing; SKILL.md
        # phrases the same condition slightly differently (it scopes
        # the merge step, not the emission trigger).
        # NOTE (2026-05-24): markdownlint MD013 reflow per
        # TASK-RF-20260523-234320-markdownlint-remediation may split this
        # phrase across a line-break + indentation. Normalise whitespace
        # before the substring check so the audit remains content-pinned
        # without being byte-pinned to a specific line wrap.
        agent_sites = (RF_ANALYST_SRC, RF_QA_SRC, RF_QA_QUAL_SRC)
        for p in agent_sites:
            txt = wrapper_texts[p]
            normalised = " ".join(txt.split())
            assert (
                "fails after the single retry AND exhausts its escalation ladder"
                in normalised
            ), (
                f"{p.name} no longer names the twice-exhaust trigger "
                "('fails after the single retry AND exhausts its "
                "escalation ladder') — TEST-018 cannot bind"
            )

    def test_rejection_symbols_present_at_every_site(
        self, wrapper_texts: Dict[Path, str]
    ):
        symbols = (
            SYM_FIXED_FIELD,
            SYM_DYNAMIC_FIELD,
            SYM_RECOMMENDATION,
            SYM_DEDUP_KEY_SHAPE,
            SYM_FOUND_N_TIMES,
        )
        for p, txt in wrapper_texts.items():
            for sym in symbols:
                assert sym in txt, (
                    f"{p.name} no longer names rejection symbol {sym!r} — "
                    "wrapper contract drifted"
                )

    def test_closed_vocabulary_named_at_every_site(
        self, wrapper_texts: Dict[Path, str]
    ):
        # Every literal of the closed vocabulary appears in the
        # wrapper bullet (and any nearby example block).
        for p, txt in wrapper_texts.items():
            for val in sorted(EXHAUST_POINT_VOCAB):
                assert val in txt, (
                    f"{p.name} no longer names vocabulary value {val!r}"
                )


# ---------------------------------------------------------------------------
# AC — Positive emission has all 5 fixed/dynamic fields + valid 7-field shape.
# ---------------------------------------------------------------------------


class TestTwiceExhaustEmissionPasses:
    """Canonical TEST-018 positive path. The twice-exhaust emission
    populates all 7 fields; all 5 fixed/dynamic baseline fields
    (severity, source, affected_range, evidence, recommendation)
    are non-empty + carry the literal values where the wrapper
    pins them; the validator returns ok=True with no symbol."""

    def test_validator_returns_ok(self, twice_exhaust_emission):
        result = validate_dnsp_emission(twice_exhaust_emission)
        assert result.ok, (
            f"twice-exhaust positive emission rejected: symbol="
            f"{result.symbol!r} field={result.field!r} "
            f"detail={result.detail!r}"
        )
        assert result.symbol is None

    def test_severity_is_high_literal(self, twice_exhaust_emission):
        assert twice_exhaust_emission["severity"] == FIXED_SEVERITY, (
            f"severity={twice_exhaust_emission['severity']!r} != "
            f"{FIXED_SEVERITY!r} (R-113 pin)"
        )

    def test_source_is_synthetic_dnsp_literal(self, twice_exhaust_emission):
        assert twice_exhaust_emission["source"] == FIXED_SOURCE, (
            f"source={twice_exhaust_emission['source']!r} != "
            f"{FIXED_SOURCE!r} (R-114 pin)"
        )

    def test_all_five_fixed_fields_populated(self, twice_exhaust_emission):
        """The AC1 row of T06.15: 'all 5 fixed fields populated'."""
        five_fields = (
            "severity", "source", "affected_range", "evidence",
            "recommendation",
        )
        for fname in five_fields:
            val = twice_exhaust_emission[fname]
            assert isinstance(val, str), (
                f"field {fname} is not a string: {val!r}"
            )
            assert val.strip() != "", (
                f"field {fname} is blank/whitespace — AC1 violated"
            )

    def test_recommendation_byte_exact(self, twice_exhaust_emission):
        assert (
            twice_exhaust_emission["recommendation"] == FIXED_RECOMMENDATION
        ), "recommendation drift — R-117 byte-exact pin broken"

    def test_dedup_key_is_two_tuple_yaml_list(self, twice_exhaust_emission):
        dk = twice_exhaust_emission["dedup_key"]
        assert isinstance(dk, list), f"dedup_key is not a list: {dk!r}"
        assert len(dk) == 2, f"dedup_key length != 2: {dk!r}"

    def test_dedup_key_second_element_in_vocabulary(
        self, twice_exhaust_emission
    ):
        dk = twice_exhaust_emission["dedup_key"]
        assert dk[1] in EXHAUST_POINT_VOCAB, (
            f"dedup_key exhaust_point {dk[1]!r} not in "
            f"vocabulary {sorted(EXHAUST_POINT_VOCAB)}"
        )

    def test_twice_exhaust_carries_retry_2(self, twice_exhaust_emission):
        # The canonical "twice-exhaust" case lands at retry-2 — the
        # partition tried, failed, retried, failed again.
        dk = twice_exhaust_emission["dedup_key"]
        assert dk[1] == "retry-2", (
            f"twice-exhaust canonical exhaust_point != 'retry-2': {dk[1]!r}"
        )

    def test_found_n_times_default_is_one(self, twice_exhaust_emission):
        assert twice_exhaust_emission["found_n_times"] == 1, (
            f"found_n_times default != 1 on first emission: "
            f"{twice_exhaust_emission['found_n_times']!r} — R-119 broken"
        )


# ---------------------------------------------------------------------------
# AC — Negative paths: each fixed/dynamic field corruption triggers
# the named rejection symbol per the wrapper contract.
# ---------------------------------------------------------------------------


class TestNegativePathRejectionSymbols:
    """For each of the 5 fixed/dynamic fields, mutating it in a way
    that violates the wrapper contract MUST be rejected by the
    validator with the named symbol from the wrapper text. This is
    the load-bearing assertion behind "all 5 fixed fields populated"
    — populated is verified by the positive path; the negative path
    proves the populated-ness is enforced, not coincidental.
    """

    def test_missing_severity_rejected_as_fixed_field(self):
        rec = build_twice_exhaust_emission()
        del rec["severity"]
        result = validate_dnsp_emission(rec)
        assert not result.ok and result.symbol == SYM_FIXED_FIELD, (
            f"missing severity should reject as {SYM_FIXED_FIELD}: {result}"
        )

    def test_severity_low_rejected_as_fixed_field(self):
        rec = build_twice_exhaust_emission()
        rec["severity"] = "LOW"
        result = validate_dnsp_emission(rec)
        assert not result.ok and result.symbol == SYM_FIXED_FIELD, (
            f"severity LOW should reject as {SYM_FIXED_FIELD}: {result}"
        )

    def test_source_lowercase_rejected_as_fixed_field(self):
        rec = build_twice_exhaust_emission()
        rec["source"] = "Synthetic-DNSP"
        result = validate_dnsp_emission(rec)
        assert not result.ok and result.symbol == SYM_FIXED_FIELD, (
            f"case-mutated source should reject as {SYM_FIXED_FIELD}: {result}"
        )

    def test_blank_affected_range_rejected_as_dynamic_field(self):
        rec = build_twice_exhaust_emission()
        rec["affected_range"] = "   "
        result = validate_dnsp_emission(rec)
        assert not result.ok and result.symbol == SYM_DYNAMIC_FIELD, (
            f"blank affected_range should reject as {SYM_DYNAMIC_FIELD}: "
            f"{result}"
        )

    def test_blank_evidence_rejected_as_dynamic_field(self):
        rec = build_twice_exhaust_emission()
        rec["evidence"] = ""
        result = validate_dnsp_emission(rec)
        assert not result.ok and result.symbol == SYM_DYNAMIC_FIELD, (
            f"blank evidence should reject as {SYM_DYNAMIC_FIELD}: {result}"
        )

    def test_recommendation_with_suffix_rejected(self):
        # The pre-T06.05 wrapper drift suffixed ` on this range`;
        # T06.05 removed it and pinned the byte-exact literal.
        rec = build_twice_exhaust_emission()
        rec["recommendation"] = FIXED_RECOMMENDATION + " on this range"
        result = validate_dnsp_emission(rec)
        assert not result.ok and result.symbol == SYM_RECOMMENDATION, (
            f"suffix-extended recommendation should reject as "
            f"{SYM_RECOMMENDATION}: {result}"
        )

    def test_dedup_key_three_element_rejected(self):
        rec = build_twice_exhaust_emission()
        rec["dedup_key"] = [
            "${TASK_DIR}research/03-auth.md",
            "retry-2",
            "spurious-third-element",
        ]
        result = validate_dnsp_emission(rec)
        assert not result.ok and result.symbol == SYM_DEDUP_KEY_SHAPE, (
            f"3-element dedup_key should reject as {SYM_DEDUP_KEY_SHAPE}: "
            f"{result}"
        )

    def test_dedup_key_non_vocabulary_exhaust_point_rejected(self):
        rec = build_twice_exhaust_emission()
        rec["dedup_key"] = [
            "${TASK_DIR}research/03-auth.md",
            "second retry",  # free-form description, not vocabulary
        ]
        result = validate_dnsp_emission(rec)
        assert not result.ok and result.symbol == SYM_DEDUP_KEY_SHAPE, (
            f"non-vocabulary exhaust_point should reject as "
            f"{SYM_DEDUP_KEY_SHAPE}: {result}"
        )

    def test_found_n_times_zero_rejected(self):
        rec = build_twice_exhaust_emission()
        rec["found_n_times"] = 0
        result = validate_dnsp_emission(rec)
        assert not result.ok and result.symbol == SYM_FOUND_N_TIMES, (
            f"found_n_times=0 should reject as {SYM_FOUND_N_TIMES}: {result}"
        )

    def test_found_n_times_string_rejected(self):
        rec = build_twice_exhaust_emission()
        rec["found_n_times"] = "1"
        result = validate_dnsp_emission(rec)
        assert not result.ok and result.symbol == SYM_FOUND_N_TIMES, (
            f"stringified found_n_times should reject as "
            f"{SYM_FOUND_N_TIMES}: {result}"
        )


# ---------------------------------------------------------------------------
# Cross-checks: every closed-vocabulary exhaust_point produces a
# valid twice-exhaust-style emission (the vocabulary is fully wired,
# not just "retry-2").
# ---------------------------------------------------------------------------


class TestVocabularyIsFullyWired:
    """Each of the five closed-vocabulary exhaust_point values can
    underpin a valid synthetic-dnsp emission. A regression that
    dropped one of them from the vocabulary would render the
    associated escalation-ladder step undetectable."""

    @pytest.mark.parametrize("exhaust_point", sorted(EXHAUST_POINT_VOCAB))
    def test_each_vocabulary_value_yields_valid_emission(
        self, exhaust_point: str
    ):
        rec = build_twice_exhaust_emission(exhaust_point=exhaust_point)
        result = validate_dnsp_emission(rec)
        assert result.ok, (
            f"vocabulary value {exhaust_point!r} unexpectedly rejected: "
            f"{result}"
        )

    def test_vocabulary_size_is_exactly_five(self):
        assert len(EXHAUST_POINT_VOCAB) == 5, (
            f"closed vocabulary cardinality changed: "
            f"{sorted(EXHAUST_POINT_VOCAB)}"
        )
