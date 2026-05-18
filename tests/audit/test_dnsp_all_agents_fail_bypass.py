"""TEST-020 — all-agents-fail bypass: zero partitions → no synthetic, rf-team-lead.md:417 activates
(R-135 / T06.16 / D-0081).

Phase-6 / T06.16 deliverable. Codifies AC2 of T06.16:

  "TEST-020 asserts no synthetic block emitted and rf-team-lead activation."

The wrapper bullets at the four sites (``rf-analyst.md``,
``rf-qa.md``, ``rf-qa-qualitative.md``, ``SKILL.md``) pin R-122
guard precedence as three mutually-exclusive cohort-outcome paths:

  - **Path A** (``success_count == 0``) — zero partitions succeeded.
    The orchestrator MUST activate the byte-stable
    ``rf-team-lead.md:417`` max-3-cycles HALT-and-ask-user escalation
    and MUST NOT emit any synthetic-dnsp block.
  - **Path B** (``success_count >= 1`` AND ``exhaust_count >= 1``) —
    mixed cohort. The orchestrator MUST emit one synthetic-dnsp block
    per exhausted partition into the normal output stream alongside
    the real findings from the successful partitions (strictly
    additive — never replacement).
  - **Path C** (``success_count == N`` AND ``exhaust_count == 0``) —
    all partitions succeeded. The orchestrator MUST NOT emit any
    synthetic and runs the baseline merge.

Any cohort outcome that satisfies more than one path's precondition
OR none (e.g., ``success_count == 0`` AND ``exhaust_count == 0`` —
every partition must terminate in success-or-exhaust under the M5
escalation-ladder semantics) is a contract violation and surfaces as
``R-122-guard-precedence-violation``.

The rf-team-lead.md:417 line is byte-stable across the M6 landing
under COMP-006-M6 (sha256 ``51725c0ffa151c3403701f21910d7f5cf122639f3a0e7fa9ae3cafe82701a0a0``).
TEST-020 verifies the sha256 at runtime so a regression that mutates
the escalation line breaks the fixture immediately.

Acceptance reference (phase-6-tasklist.md L780-784):
- ``uv run pytest tests/audit/test_dnsp_all_agents_fail_bypass.py tests/audit/test_dnsp_does_not_serialize_cohort.py -v`` exits 0.
- TEST-020 asserts no synthetic block emitted and rf-team-lead activation.
- Evidence at ``TASKLIST_ROOT/artifacts/D-0081/evidence.md``.

Run: ``uv run pytest tests/audit/test_dnsp_all_agents_fail_bypass.py -v``
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]

RF_ANALYST_SRC = REPO_ROOT / "src" / "superclaude" / "agents" / "rf-analyst.md"
RF_QA_SRC = REPO_ROOT / "src" / "superclaude" / "agents" / "rf-qa.md"
RF_QA_QUAL_SRC = (
    REPO_ROOT / "src" / "superclaude" / "agents" / "rf-qa-qualitative.md"
)
SKILL_SRC = REPO_ROOT / "src" / "superclaude" / "skills" / "task-builder" / "SKILL.md"
RF_TEAM_LEAD_SRC = (
    REPO_ROOT / "src" / "superclaude" / "agents" / "rf-team-lead.md"
)

WRAPPER_SOURCES = (RF_ANALYST_SRC, RF_QA_SRC, RF_QA_QUAL_SRC, SKILL_SRC)

# Frozen sha256 of rf-team-lead.md:417 per COMP-006-M6 preservation
# gate (D-0079 / T06.14). The wrapper bullet at R-122 pins this hash
# verbatim — drift here breaks the Path A activation contract.
RF_TEAM_LEAD_LINE_417_SHA256 = (
    "51725c0ffa151c3403701f21910d7f5cf122639f3a0e7fa9ae3cafe82701a0a0"
)

# Named rejection symbol for cohort-level path-selection failures
# (R-122). Distinct from per-emission wire-shape rejection symbols
# pinned in TEST-018; the wrapper bullet calls this out explicitly.
SYM_GUARD_PRECEDENCE = "R-122-guard-precedence-violation"


# ---------------------------------------------------------------------------
# Pure-Python cohort-outcome path selector (encodes R-122 semantics).
# ---------------------------------------------------------------------------


@dataclass
class CohortOutcome:
    """A partition cohort's terminal state at the orchestrator boundary.

    ``success_count`` + ``exhaust_count`` MUST sum to ``N`` (every
    partition must terminate in success-or-exhaust under M5
    escalation-ladder semantics).
    """

    n_partitions: int
    success_count: int
    exhaust_count: int


@dataclass
class PathSelection:
    """Outcome of the R-122 cohort-level path selector.

    On a valid cohort outcome, exactly one of ``path`` ∈ {"A", "B",
    "C"} is set. ``activates_rf_team_lead_417`` is True ONLY on
    Path A. ``emits_synthetic`` is True ONLY on Path B. On a
    contract-violating cohort outcome, ``ok`` is False and ``symbol``
    is ``R-122-guard-precedence-violation``.
    """

    ok: bool
    path: Optional[str] = None
    activates_rf_team_lead_417: bool = False
    emits_synthetic: bool = False
    symbol: Optional[str] = None
    detail: Optional[str] = None


def select_cohort_path(outcome: CohortOutcome) -> PathSelection:
    """Apply the R-122 three-path guard precedence to a cohort outcome.

    Implements the wrapper bullet verbatim:

      - Path A: ``success_count == 0`` (and by closure
        ``exhaust_count == n_partitions``) → activate
        ``rf-team-lead.md:417``, NO synthetic.
      - Path B: ``success_count >= 1 AND exhaust_count >= 1`` → emit
        synthetic alongside real findings.
      - Path C: ``exhaust_count == 0`` (and by closure
        ``success_count == n_partitions``) → no synthetic, baseline.
      - Reject: any cohort outcome with sum != n_partitions (every
        partition must terminate; sum mismatch means the cohort is
        internally inconsistent).
    """
    n = outcome.n_partitions
    s = outcome.success_count
    x = outcome.exhaust_count

    # M5 termination closure: every partition must terminate in
    # success-or-exhaust. A cohort with sum != n is malformed.
    if n <= 0 or s < 0 or x < 0:
        return PathSelection(
            ok=False,
            symbol=SYM_GUARD_PRECEDENCE,
            detail=f"negative or zero cardinality: n={n} s={s} x={x}",
        )
    if s + x != n:
        return PathSelection(
            ok=False,
            symbol=SYM_GUARD_PRECEDENCE,
            detail=(
                f"cohort termination closure violated: "
                f"success({s}) + exhaust({x}) != n_partitions({n})"
            ),
        )

    # Path A — zero successes.
    if s == 0:
        # exhaust_count == n by closure
        return PathSelection(
            ok=True,
            path="A",
            activates_rf_team_lead_417=True,
            emits_synthetic=False,
        )
    # Path C — zero exhausts.
    if x == 0:
        return PathSelection(
            ok=True,
            path="C",
            activates_rf_team_lead_417=False,
            emits_synthetic=False,
        )
    # Path B — mixed cohort.
    return PathSelection(
        ok=True,
        path="B",
        activates_rf_team_lead_417=False,
        emits_synthetic=True,
    )


# ---------------------------------------------------------------------------
# Synthetic-block emission helpers — encode the Path A NO-SYNTHETIC rule.
# ---------------------------------------------------------------------------


def synthetic_blocks_for_cohort(
    outcome: CohortOutcome,
) -> List[Dict[str, Any]]:
    """Return the synthetic-dnsp block list the orchestrator emits
    for a given cohort outcome under R-122 path selection. Path A
    and Path C return ``[]``; Path B returns one stub block per
    exhausted partition.
    """
    sel = select_cohort_path(outcome)
    if not sel.ok:
        raise AssertionError(
            f"cannot emit synthetics from a contract-violating cohort: "
            f"{sel.symbol}: {sel.detail}"
        )
    if not sel.emits_synthetic:
        return []
    # Path B: one synthetic block per exhausted partition.
    return [
        {
            "severity": "HIGH",
            "source": "synthetic-dnsp",
            "partition_idx": i,
        }
        for i in range(outcome.exhaust_count)
    ]


def activates_rf_team_lead_417(outcome: CohortOutcome) -> bool:
    """Return whether Path A's rf-team-lead.md:417 escalation activates
    for the given cohort outcome. Mirrors ``select_cohort_path``;
    extracted as a named API so the AC2 wording binds directly to the
    assertion."""
    sel = select_cohort_path(outcome)
    return sel.ok and sel.activates_rf_team_lead_417


# ---------------------------------------------------------------------------
# Fixtures.
# ---------------------------------------------------------------------------


@pytest.fixture(scope="module")
def wrapper_texts() -> Dict[Path, str]:
    return {p: p.read_text(encoding="utf-8") for p in WRAPPER_SOURCES}


@pytest.fixture(scope="module")
def rf_team_lead_text() -> str:
    return RF_TEAM_LEAD_SRC.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def all_fail_cohort() -> CohortOutcome:
    """Canonical TEST-020 input: every partition exhausted, zero
    successes. The R-122 path selector routes this to Path A
    (activates rf-team-lead.md:417, no synthetic)."""
    return CohortOutcome(n_partitions=4, success_count=0, exhaust_count=4)


# ---------------------------------------------------------------------------
# Source-text guards — R-122 wording and sha256 stay put.
# ---------------------------------------------------------------------------


class TestR122WrapperTextGuards:
    """The R-122 three-path table lives in the wrapper bullets at all
    four sites; the ``rf-team-lead.md:417`` byte-stability claim and
    the sha256 pin are load-bearing. A reword breaks TEST-020, so
    lock the strings."""

    def test_all_wrapper_sources_exist(self):
        for p in WRAPPER_SOURCES:
            assert p.is_file(), f"missing wrapper source: {p}"

    def test_rf_team_lead_source_exists(self):
        assert RF_TEAM_LEAD_SRC.is_file(), (
            f"missing rf-team-lead.md: {RF_TEAM_LEAD_SRC}"
        )

    def test_r122_label_named_at_every_site(
        self, wrapper_texts: Dict[Path, str]
    ):
        for p, txt in wrapper_texts.items():
            assert "R-122" in txt, (
                f"{p.name} no longer references R-122 — all-agents-fail "
                "guard precedence pointer lost"
            )

    def test_path_a_label_present_at_every_site(
        self, wrapper_texts: Dict[Path, str]
    ):
        for p, txt in wrapper_texts.items():
            assert "Path A" in txt, (
                f"{p.name} no longer labels Path A (zero-success → "
                "rf-team-lead.md:417)"
            )

    def test_path_b_label_present_at_every_site(
        self, wrapper_texts: Dict[Path, str]
    ):
        for p, txt in wrapper_texts.items():
            assert "Path B" in txt, (
                f"{p.name} no longer labels Path B (mixed-cohort synthetic)"
            )

    def test_path_c_label_present_at_every_site(
        self, wrapper_texts: Dict[Path, str]
    ):
        for p, txt in wrapper_texts.items():
            assert "Path C" in txt, (
                f"{p.name} no longer labels Path C (all-success baseline)"
            )

    def test_rf_team_lead_417_pointer_present_at_every_site(
        self, wrapper_texts: Dict[Path, str]
    ):
        for p, txt in wrapper_texts.items():
            assert "rf-team-lead.md:417" in txt, (
                f"{p.name} no longer names rf-team-lead.md:417 — Path A "
                "destination pointer lost"
            )

    def test_rf_team_lead_417_sha256_pin_present_at_every_site(
        self, wrapper_texts: Dict[Path, str]
    ):
        for p, txt in wrapper_texts.items():
            assert RF_TEAM_LEAD_LINE_417_SHA256 in txt, (
                f"{p.name} no longer pins the rf-team-lead.md:417 "
                f"sha256 {RF_TEAM_LEAD_LINE_417_SHA256!r} — COMP-006-M6 "
                "preservation marker missing"
            )

    def test_guard_rejection_symbol_present_at_every_site(
        self, wrapper_texts: Dict[Path, str]
    ):
        for p, txt in wrapper_texts.items():
            assert SYM_GUARD_PRECEDENCE in txt, (
                f"{p.name} no longer names rejection symbol "
                f"{SYM_GUARD_PRECEDENCE!r}"
            )

    def test_mutual_exclusivity_phrasing_present_at_every_site(
        self, wrapper_texts: Dict[Path, str]
    ):
        for p, txt in wrapper_texts.items():
            assert "mutually exclusive" in txt or "mutually-exclusive" in txt, (
                f"{p.name} no longer phrases the three paths as "
                "mutually exclusive — R-122 contract drift"
            )

    def test_zero_successes_and_zero_exhausts_rejected_in_text(
        self, wrapper_texts: Dict[Path, str]
    ):
        # The wrapper bullet explicitly names the "(0 success, 0 exhaust)
        # → contract violation" case so the path table is exhaustive.
        for p, txt in wrapper_texts.items():
            assert "success-or-exhaust" in txt, (
                f"{p.name} no longer pins the M5 success-or-exhaust "
                "termination closure used by R-122 reject path"
            )


class TestRfTeamLead417ByteStability:
    """rf-team-lead.md:417 is the Path A destination. A regression
    that mutated this line would break the all-agents-fail
    escalation contract; TEST-020 verifies its sha256 at runtime."""

    def test_line_417_sha256_matches_pinned_value(self, rf_team_lead_text: str):
        lines = rf_team_lead_text.splitlines(keepends=True)
        # 1-indexed line 417 → 0-indexed lines[416]
        assert len(lines) >= 417, (
            f"rf-team-lead.md too short ({len(lines)} lines); cannot "
            "verify line 417"
        )
        line_417 = lines[416]
        # COMP-006-M6 pin matches `sed -n '417p' rf-team-lead.md |
        # sha256sum` — sed emits the line with its trailing newline,
        # so the canonical hash covers the LF byte. Preserve that
        # convention exactly (do NOT strip the newline).
        sha = hashlib.sha256(line_417.encode("utf-8")).hexdigest()
        assert sha == RF_TEAM_LEAD_LINE_417_SHA256, (
            f"rf-team-lead.md:417 sha256 drift: got {sha!r}, "
            f"expected {RF_TEAM_LEAD_LINE_417_SHA256!r}. "
            f"Line 417: {line_417!r}"
        )

    def test_line_417_names_max_3_cycles(self, rf_team_lead_text: str):
        line_417 = rf_team_lead_text.splitlines()[416]
        assert "max 3 cycles per phase" in line_417, (
            f"rf-team-lead.md:417 no longer names the max-3-cycles "
            f"contract: {line_417!r}"
        )

    def test_line_417_names_halt_and_ask_user(self, rf_team_lead_text: str):
        line_417 = rf_team_lead_text.splitlines()[416]
        assert "HALT and ask user" in line_417, (
            f"rf-team-lead.md:417 no longer names the HALT-and-ask-user "
            f"escalation: {line_417!r}"
        )


# ---------------------------------------------------------------------------
# AC2.1 — Path A: zero-successes → no synthetic block, rf-team-lead activates.
# ---------------------------------------------------------------------------


class TestPathAActivatesRfTeamLeadNoSynthetic:
    """Canonical AC2 binding: a zero-successes cohort routes down
    Path A, activates ``rf-team-lead.md:417``, and emits zero
    synthetic-dnsp blocks."""

    def test_path_selector_returns_path_a(self, all_fail_cohort):
        sel = select_cohort_path(all_fail_cohort)
        assert sel.ok, f"valid all-fail cohort wrongly rejected: {sel}"
        assert sel.path == "A", (
            f"expected Path A on zero-success cohort, got {sel.path!r}"
        )

    def test_path_a_activates_rf_team_lead_417(self, all_fail_cohort):
        sel = select_cohort_path(all_fail_cohort)
        assert sel.activates_rf_team_lead_417, (
            "Path A MUST activate rf-team-lead.md:417 fix-cycle escalation"
        )
        # And the dedicated helper agrees with the path selector.
        assert activates_rf_team_lead_417(all_fail_cohort)

    def test_path_a_emits_zero_synthetic_blocks(self, all_fail_cohort):
        # AC2 wording: "no synthetic block emitted".
        sel = select_cohort_path(all_fail_cohort)
        assert not sel.emits_synthetic, (
            "Path A MUST NOT emit synthetic-dnsp blocks — informationally "
            "equivalent to escalation"
        )
        blocks = synthetic_blocks_for_cohort(all_fail_cohort)
        assert blocks == [], (
            f"Path A emitted synthetic blocks despite zero-success: "
            f"{blocks!r}"
        )

    @pytest.mark.parametrize("n", [1, 2, 3, 5, 8])
    def test_path_a_scales_with_cohort_size(self, n: int):
        # An all-exhaust cohort of any size N>=1 routes to Path A.
        outcome = CohortOutcome(n_partitions=n, success_count=0, exhaust_count=n)
        sel = select_cohort_path(outcome)
        assert sel.path == "A"
        assert sel.activates_rf_team_lead_417
        assert not sel.emits_synthetic
        assert synthetic_blocks_for_cohort(outcome) == []


# ---------------------------------------------------------------------------
# AC2.2 — Path B: mixed cohort emits synthetic, does NOT activate rf-team-lead.
# ---------------------------------------------------------------------------


class TestPathBEmitsSyntheticNoEscalation:
    """Mixed cohorts (>=1 success AND >=1 exhaust) take Path B; the
    R-122 wrapper bullet pins this as mutually exclusive with Path A,
    so rf-team-lead.md:417 MUST NOT activate on Path B."""

    @pytest.mark.parametrize(
        "n,s,x",
        [
            (2, 1, 1),
            (3, 1, 2),
            (3, 2, 1),
            (4, 2, 2),
            (5, 3, 2),
        ],
    )
    def test_mixed_cohort_routes_to_path_b(self, n, s, x):
        outcome = CohortOutcome(n_partitions=n, success_count=s, exhaust_count=x)
        sel = select_cohort_path(outcome)
        assert sel.ok, f"valid mixed cohort wrongly rejected: {sel}"
        assert sel.path == "B", (
            f"expected Path B on mixed cohort (n={n},s={s},x={x}), got "
            f"{sel.path!r}"
        )

    def test_path_b_does_not_activate_rf_team_lead(self):
        outcome = CohortOutcome(n_partitions=4, success_count=2, exhaust_count=2)
        sel = select_cohort_path(outcome)
        assert not sel.activates_rf_team_lead_417, (
            "Path B MUST NOT activate rf-team-lead.md:417 — that is "
            "Path A's destination only (mutual exclusivity)"
        )

    def test_path_b_emits_one_synthetic_per_exhaust(self):
        outcome = CohortOutcome(n_partitions=5, success_count=2, exhaust_count=3)
        blocks = synthetic_blocks_for_cohort(outcome)
        assert len(blocks) == 3, (
            f"Path B emit count != exhaust_count: got {len(blocks)}, "
            f"expected 3"
        )
        for b in blocks:
            assert b["severity"] == "HIGH"
            assert b["source"] == "synthetic-dnsp"


# ---------------------------------------------------------------------------
# AC2.3 — Path C: all-success baseline, no synthetic, no escalation.
# ---------------------------------------------------------------------------


class TestPathCBaselineMerge:
    """All-partitions-succeeded routes to Path C; no synthetic emits
    and rf-team-lead.md:417 does NOT activate (mutual exclusivity)."""

    @pytest.mark.parametrize("n", [1, 2, 3, 5])
    def test_all_success_routes_to_path_c(self, n: int):
        outcome = CohortOutcome(n_partitions=n, success_count=n, exhaust_count=0)
        sel = select_cohort_path(outcome)
        assert sel.path == "C"
        assert not sel.activates_rf_team_lead_417
        assert not sel.emits_synthetic
        assert synthetic_blocks_for_cohort(outcome) == []


# ---------------------------------------------------------------------------
# AC — R-122 reject: malformed cohort outcomes fire R-122-guard-precedence-violation.
# ---------------------------------------------------------------------------


class TestR122GuardPrecedenceViolations:
    """Cohort outcomes that don't satisfy exactly one path's
    precondition MUST be rejected with
    ``R-122-guard-precedence-violation`` — the wrapper explicitly
    names the (0 success, 0 exhaust) case as the canonical example."""

    def test_zero_success_zero_exhaust_rejected(self):
        # Three-partition cohort with no terminal state — every
        # partition must terminate per M5 semantics.
        outcome = CohortOutcome(n_partitions=3, success_count=0, exhaust_count=0)
        sel = select_cohort_path(outcome)
        assert not sel.ok
        assert sel.symbol == SYM_GUARD_PRECEDENCE, (
            f"(0,0) cohort should reject as {SYM_GUARD_PRECEDENCE}: {sel}"
        )

    def test_oversubscribed_cohort_rejected(self):
        # Sum > n: impossible — only n partitions can terminate.
        outcome = CohortOutcome(n_partitions=2, success_count=2, exhaust_count=1)
        sel = select_cohort_path(outcome)
        assert not sel.ok and sel.symbol == SYM_GUARD_PRECEDENCE, (
            f"oversubscribed cohort should reject as "
            f"{SYM_GUARD_PRECEDENCE}: {sel}"
        )

    def test_undersubscribed_cohort_rejected(self):
        # Sum < n: some partitions haven't terminated yet.
        outcome = CohortOutcome(n_partitions=4, success_count=1, exhaust_count=1)
        sel = select_cohort_path(outcome)
        assert not sel.ok and sel.symbol == SYM_GUARD_PRECEDENCE, (
            f"undersubscribed cohort should reject as "
            f"{SYM_GUARD_PRECEDENCE}: {sel}"
        )

    def test_negative_counts_rejected(self):
        outcome = CohortOutcome(n_partitions=3, success_count=-1, exhaust_count=4)
        sel = select_cohort_path(outcome)
        assert not sel.ok and sel.symbol == SYM_GUARD_PRECEDENCE

    def test_zero_partition_cohort_rejected(self):
        outcome = CohortOutcome(n_partitions=0, success_count=0, exhaust_count=0)
        sel = select_cohort_path(outcome)
        assert not sel.ok and sel.symbol == SYM_GUARD_PRECEDENCE

    def test_emit_helper_refuses_invalid_cohort(self):
        outcome = CohortOutcome(n_partitions=3, success_count=0, exhaust_count=0)
        with pytest.raises(AssertionError) as excinfo:
            synthetic_blocks_for_cohort(outcome)
        assert SYM_GUARD_PRECEDENCE in str(excinfo.value)


# ---------------------------------------------------------------------------
# AC — Mutual exclusivity: at most one path per cohort outcome.
# ---------------------------------------------------------------------------


class TestPathMutualExclusivity:
    """The R-122 wrapper bullet asserts the three paths are mutually
    exclusive. Verify the selector NEVER returns a state where
    ``emits_synthetic`` and ``activates_rf_team_lead_417`` are both
    true — that combination would be Path A AND Path B simultaneously,
    a contract violation."""

    @pytest.mark.parametrize(
        "n,s,x",
        [
            (1, 0, 1),  # Path A
            (1, 1, 0),  # Path C
            (2, 1, 1),  # Path B
            (3, 0, 3),  # Path A
            (3, 3, 0),  # Path C
            (4, 2, 2),  # Path B
            (10, 9, 1),  # Path B
        ],
    )
    def test_at_most_one_path_action_active(self, n, s, x):
        outcome = CohortOutcome(n_partitions=n, success_count=s, exhaust_count=x)
        sel = select_cohort_path(outcome)
        assert sel.ok
        # Mutual exclusivity: activates_rf_team_lead_417 (Path A) AND
        # emits_synthetic (Path B) cannot both be true.
        assert not (sel.activates_rf_team_lead_417 and sel.emits_synthetic), (
            f"Path A and Path B actions both active for (n={n},s={s},x={x})"
        )

    def test_path_a_implies_no_synthetic(self, all_fail_cohort):
        sel = select_cohort_path(all_fail_cohort)
        assert sel.path == "A"
        # Tautological — but binds the AC wording at the API surface.
        assert sel.activates_rf_team_lead_417
        assert not sel.emits_synthetic

    def test_path_b_implies_no_rf_team_lead(self):
        outcome = CohortOutcome(n_partitions=3, success_count=2, exhaust_count=1)
        sel = select_cohort_path(outcome)
        assert sel.path == "B"
        assert sel.emits_synthetic
        assert not sel.activates_rf_team_lead_417


# ---------------------------------------------------------------------------
# AC — Execution-log binding: Path A's execution log shows the HALT path.
# (Source-text guard: the wrapper bullet pins both "HALT" and the
# escalation activation; the roadmap evidence row names
# "execution-log:shows-HALT-path".)
# ---------------------------------------------------------------------------


class TestPathAExecutionLogHaltBinding:
    """The R-135 roadmap evidence row names
    ``execution-log:shows-HALT-path`` — Path A activates the
    rf-team-lead.md:417 max-3-cycles HALT-and-ask-user escalation.
    Bind the HALT verb to the rf-team-lead source so a regression
    breaking the HALT activation breaks TEST-020."""

    def test_rf_team_lead_417_contains_halt(self, rf_team_lead_text: str):
        line_417 = rf_team_lead_text.splitlines()[416]
        assert "HALT" in line_417, (
            f"rf-team-lead.md:417 no longer contains the HALT activation "
            f"verb — Path A execution-log binding broken: {line_417!r}"
        )

    def test_skill_md_documents_zero_success_routes_to_rf_team_lead(
        self, wrapper_texts: Dict[Path, str]
    ):
        skill_text = wrapper_texts[SKILL_SRC]
        # SKILL.md §A.8 merge step explicitly states "when zero
        # partitions succeeded the merge step is skipped and
        # rf-team-lead.md:417 activates instead".
        assert (
            "zero partitions succeeded" in skill_text
            and "rf-team-lead.md:417" in skill_text
        ), (
            "SKILL.md no longer documents the zero-partitions-succeeded "
            "→ rf-team-lead.md:417 activation under R-122 Path A"
        )
