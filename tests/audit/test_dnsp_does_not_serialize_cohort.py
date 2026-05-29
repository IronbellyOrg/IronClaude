"""TEST-021 — cohort concurrency: N-1 sibling partitions overlap with exhausted partition's synthesis
(R-136 / T06.16 / D-0081 / INV-021).

Phase-6 / T06.16 deliverable. Codifies AC3 of T06.16:

  "TEST-021 asserts spawn-log timing shows N-1 partitions overlap
   with synthesis."

The wrapper bullets at the four sites (``rf-analyst.md``, ``rf-qa.md``,
``rf-qa-qualitative.md``, ``SKILL.md``) pin R-125 / INV-021 as the
per-cohort instantiation of the NFR-CONV.10 parallel-research
invariant:

  "When one partition's escalation ladder exhausts, the orchestrator
   MUST allow the remaining N-1 sibling partitions to continue
   executing concurrently to their own success-or-exhaust terminal
   state BEFORE the exhausted partition's synthetic-dnsp emission is
   composed AND BEFORE the merge step at SKILL.md §A.8 / §A.10 runs.
   The exhausted partition's synthesis MUST NOT block, pause,
   serialize, or reduce the parallelism of the sibling cohort;
   spawn-log timestamps MUST evidence the N-1 partitions completing
   concurrently with (overlapping in wall-clock time with) the
   exhausted partition's synthesis step."

Violations surface as ``INV-021-cohort-serialization-violation``.

This fixture models a spawn-log as a list of partition execution
windows (``start_ts``, ``exhaust_ts`` or ``success_ts``, plus a
``synthesis_start_ts``/``synthesis_end_ts`` for the exhausted
partition). A pure-Python invariant checker computes whether the
N-1 sibling execution windows OVERLAP in wall-clock time with the
exhausted partition's synthesis window. Serial spawn-logs
(siblings end strictly before synthesis starts) fail the check;
concurrent spawn-logs pass.

The wrapper-text guards lock R-125, INV-021, NFR-CONV.10, the
"concurrently to their own success-or-exhaust" phrasing, and the
``INV-021-cohort-serialization-violation`` rejection symbol against
silent drift at all four sites.

Acceptance reference (phase-6-tasklist.md L780-784):
- ``uv run pytest tests/audit/test_dnsp_all_agents_fail_bypass.py tests/audit/test_dnsp_does_not_serialize_cohort.py -v`` exits 0.
- TEST-021 asserts spawn-log timing shows N-1 partitions overlap with synthesis.
- Evidence at ``TASKLIST_ROOT/artifacts/D-0081/evidence.md``.

Run: ``uv run pytest tests/audit/test_dnsp_does_not_serialize_cohort.py -v``
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]

RF_ANALYST_SRC = REPO_ROOT / "src" / "superclaude" / "agents" / "rf-analyst.md"
RF_QA_SRC = REPO_ROOT / "src" / "superclaude" / "agents" / "rf-qa.md"
RF_QA_QUAL_SRC = REPO_ROOT / "src" / "superclaude" / "agents" / "rf-qa-qualitative.md"
SKILL_SRC = REPO_ROOT / "src" / "superclaude" / "skills" / "task-builder" / "SKILL.md"

WRAPPER_SOURCES = (RF_ANALYST_SRC, RF_QA_SRC, RF_QA_QUAL_SRC, SKILL_SRC)

# Named rejection symbol for cohort-level concurrency failures (R-125).
SYM_COHORT_SERIALIZATION = "INV-021-cohort-serialization-violation"


# ---------------------------------------------------------------------------
# Pure-Python spawn-log timing model.
# ---------------------------------------------------------------------------


@dataclass
class PartitionWindow:
    """Wall-clock execution window for a partition in a cohort.

    ``terminal`` ∈ {"success", "exhaust"} records the M5
    success-or-exhaust closure. For exhausted partitions, the
    ``synthesis_start_ts`` / ``synthesis_end_ts`` fields record the
    DNSP synthesis step that runs AFTER ``end_ts``; for successful
    partitions both synthesis fields are ``None``.
    """

    partition_id: str
    start_ts: float
    end_ts: float
    terminal: str
    synthesis_start_ts: Optional[float] = None
    synthesis_end_ts: Optional[float] = None

    def overlaps(self, other_start: float, other_end: float) -> bool:
        """True iff this partition's execution window overlaps in
        wall-clock time with [other_start, other_end). Uses
        half-open interval semantics: touching endpoints do NOT
        overlap (the synthesis step is strictly after the partition's
        own execution ends)."""
        return not (self.end_ts <= other_start or self.start_ts >= other_end)


@dataclass
class ConcurrencyCheckResult:
    ok: bool
    symbol: Optional[str] = None
    detail: Optional[str] = None
    overlapping_siblings: List[str] = field(default_factory=list)
    serialized_siblings: List[str] = field(default_factory=list)


def check_inv_021_n_minus_1_concurrency(
    cohort: List[PartitionWindow],
    exhausted_partition_id: str,
) -> ConcurrencyCheckResult:
    """Apply the R-125 / INV-021 N-1 concurrency invariant to a
    cohort spawn-log.

    Semantics per the wrapper bullet:
      - Find the named exhausted partition; it MUST have a synthesis
        window (start, end) defined and the ``terminal`` flag MUST
        be ``"exhaust"``.
      - For each of the N-1 sibling partitions, check whether the
        sibling's [start_ts, end_ts) overlaps with the exhausted
        partition's [synthesis_start_ts, synthesis_end_ts).
      - PASS iff **all** N-1 siblings overlap. If any sibling does
        NOT overlap (the sibling completed before synthesis began),
        the spawn-log evidences serialization and the rule fails
        with ``INV-021-cohort-serialization-violation``.

    The roadmap evidence row for R-136 names this exact assertion:

      ``spawn-log-timing:N-1-partitions-overlap-exhausted-partition's-synthesis``
    """
    # Find the exhausted partition.
    exhausted: Optional[PartitionWindow] = None
    siblings: List[PartitionWindow] = []
    for p in cohort:
        if p.partition_id == exhausted_partition_id:
            exhausted = p
        else:
            siblings.append(p)

    if exhausted is None:
        return ConcurrencyCheckResult(
            ok=False,
            symbol=SYM_COHORT_SERIALIZATION,
            detail=(
                f"exhausted partition {exhausted_partition_id!r} not "
                f"present in cohort spawn-log"
            ),
        )
    if exhausted.terminal != "exhaust":
        return ConcurrencyCheckResult(
            ok=False,
            symbol=SYM_COHORT_SERIALIZATION,
            detail=(
                f"partition {exhausted_partition_id!r} terminal is "
                f"{exhausted.terminal!r}, not 'exhaust' — INV-021 only "
                f"applies to exhausted partitions"
            ),
        )
    if exhausted.synthesis_start_ts is None or exhausted.synthesis_end_ts is None:
        return ConcurrencyCheckResult(
            ok=False,
            symbol=SYM_COHORT_SERIALIZATION,
            detail=(
                "exhausted partition has no recorded synthesis window — "
                "spawn-log timing evidence missing"
            ),
        )

    syn_start = exhausted.synthesis_start_ts
    syn_end = exhausted.synthesis_end_ts
    if syn_end <= syn_start:
        return ConcurrencyCheckResult(
            ok=False,
            symbol=SYM_COHORT_SERIALIZATION,
            detail=(
                f"synthesis window non-positive: start={syn_start} >= end={syn_end}"
            ),
        )

    overlapping: List[str] = []
    serialized: List[str] = []
    for s in siblings:
        if s.overlaps(syn_start, syn_end):
            overlapping.append(s.partition_id)
        else:
            serialized.append(s.partition_id)

    if serialized:
        return ConcurrencyCheckResult(
            ok=False,
            symbol=SYM_COHORT_SERIALIZATION,
            detail=(
                f"siblings serialized behind synthesis (their execution "
                f"window did not overlap synthesis [{syn_start}, "
                f"{syn_end})): {serialized}"
            ),
            overlapping_siblings=overlapping,
            serialized_siblings=serialized,
        )

    # All N-1 siblings overlapped synthesis: INV-021 holds.
    return ConcurrencyCheckResult(
        ok=True,
        overlapping_siblings=overlapping,
        serialized_siblings=[],
    )


def build_canonical_overlap_spawn_log(
    n_siblings: int = 3,
) -> Tuple[List[PartitionWindow], str]:
    """Construct a canonical spawn-log where:

      - The cohort has N = n_siblings + 1 partitions.
      - One partition exhausts early (end_ts = 10.0) and its
        synthesis window is [10.5, 12.0].
      - All sibling partitions execute on [0.0, T_i] where T_i is
        scattered across the synthesis window — every sibling
        finishes AFTER synthesis_start, so each one overlaps.

    Returns the spawn-log + the exhausted partition's id.
    """
    cohort: List[PartitionWindow] = []
    exhausted = PartitionWindow(
        partition_id="rf-analyst-partition-1",
        start_ts=0.0,
        end_ts=10.0,
        terminal="exhaust",
        synthesis_start_ts=10.5,
        synthesis_end_ts=12.0,
    )
    cohort.append(exhausted)
    # Place sibling endings across the synthesis window so every
    # sibling overlaps the synthesis interval.
    for i in range(n_siblings):
        # Sibling end times: 11.0, 11.3, 11.6, ... — all > syn_start
        # and <= syn_end.
        end_ts = 10.5 + 0.5 * (i + 1)
        cohort.append(
            PartitionWindow(
                partition_id=f"rf-analyst-partition-{i + 2}",
                start_ts=0.0,
                end_ts=end_ts,
                terminal="success",
            )
        )
    return cohort, exhausted.partition_id


def build_serialized_spawn_log(
    n_siblings: int = 3,
) -> Tuple[List[PartitionWindow], str]:
    """Construct a serialized spawn-log: every sibling finishes
    BEFORE synthesis begins (i.e., the cohort waited for synthesis
    to start). This is the contract-violating case the R-125 wrapper
    bullet explicitly names."""
    exhausted = PartitionWindow(
        partition_id="rf-analyst-partition-1",
        start_ts=0.0,
        end_ts=10.0,
        terminal="exhaust",
        synthesis_start_ts=20.0,  # gap — siblings already done
        synthesis_end_ts=22.0,
    )
    cohort: List[PartitionWindow] = [exhausted]
    for i in range(n_siblings):
        cohort.append(
            PartitionWindow(
                partition_id=f"rf-analyst-partition-{i + 2}",
                start_ts=0.0,
                end_ts=15.0,  # well before syn_start=20.0
                terminal="success",
            )
        )
    return cohort, exhausted.partition_id


# ---------------------------------------------------------------------------
# Fixtures.
# ---------------------------------------------------------------------------


@pytest.fixture(scope="module")
def wrapper_texts() -> Dict[Path, str]:
    return {p: p.read_text(encoding="utf-8") for p in WRAPPER_SOURCES}


@pytest.fixture
def overlap_spawn_log() -> Tuple[List[PartitionWindow], str]:
    return build_canonical_overlap_spawn_log()


@pytest.fixture
def serialized_spawn_log() -> Tuple[List[PartitionWindow], str]:
    return build_serialized_spawn_log()


# ---------------------------------------------------------------------------
# Source-text guards — R-125 / INV-021 / NFR-CONV.10 wording stays put.
# ---------------------------------------------------------------------------


class TestInv021WrapperTextGuards:
    """R-125 / INV-021 wording lives in the wrapper bullets at all
    four sites. The "concurrently to their own success-or-exhaust"
    phrasing and the ``INV-021-cohort-serialization-violation`` symbol
    are load-bearing — drift breaks TEST-021."""

    def test_all_wrapper_sources_exist(self):
        for p in WRAPPER_SOURCES:
            assert p.is_file(), f"missing wrapper source: {p}"

    def test_inv_021_label_named_at_every_site(self, wrapper_texts: Dict[Path, str]):
        for p, txt in wrapper_texts.items():
            assert "INV-021" in txt, (
                f"{p.name} no longer references INV-021 — N-1 cohort "
                "concurrency invariant pointer lost"
            )

    def test_r125_label_named_at_every_site(self, wrapper_texts: Dict[Path, str]):
        for p, txt in wrapper_texts.items():
            assert "R-125" in txt, (
                f"{p.name} no longer references R-125 — INV-021 driver row pointer lost"
            )

    def test_n_minus_1_phrasing_present_at_every_site(
        self, wrapper_texts: Dict[Path, str]
    ):
        for p, txt in wrapper_texts.items():
            assert "N-1" in txt, (
                f"{p.name} no longer names 'N-1' sibling cohort — "
                "INV-021 cardinality contract drift"
            )

    def test_concurrently_to_success_or_exhaust_phrasing_present(
        self, wrapper_texts: Dict[Path, str]
    ):
        # The load-bearing phrase that bins the concurrency rule to
        # the success-or-exhaust terminal state of each sibling.
        for p, txt in wrapper_texts.items():
            assert "concurrently to their own success-or-exhaust" in txt, (
                f"{p.name} no longer pins the 'concurrently to their own "
                f"success-or-exhaust' phrasing — INV-021 wording drift"
            )

    def test_spawn_log_timestamps_phrasing_present(
        self, wrapper_texts: Dict[Path, str]
    ):
        for p, txt in wrapper_texts.items():
            assert "spawn-log timestamps" in txt, (
                f"{p.name} no longer pins 'spawn-log timestamps' as the "
                "evidence channel for INV-021 — TEST-021 anchor lost"
            )

    def test_overlapping_in_wall_clock_time_phrasing_present(
        self, wrapper_texts: Dict[Path, str]
    ):
        for p, txt in wrapper_texts.items():
            assert "overlapping in wall-clock time" in txt, (
                f"{p.name} no longer pins 'overlapping in wall-clock "
                "time' as the INV-021 evidence shape"
            )

    def test_nfr_conv_10_label_named_at_every_site(
        self, wrapper_texts: Dict[Path, str]
    ):
        for p, txt in wrapper_texts.items():
            assert "NFR-CONV.10" in txt, (
                f"{p.name} no longer references NFR-CONV.10 — "
                "parallel-research invariant pointer lost"
            )

    def test_serialization_rejection_symbol_present_at_every_site(
        self, wrapper_texts: Dict[Path, str]
    ):
        for p, txt in wrapper_texts.items():
            assert SYM_COHORT_SERIALIZATION in txt, (
                f"{p.name} no longer names rejection symbol "
                f"{SYM_COHORT_SERIALIZATION!r}"
            )

    def test_no_block_pause_serialize_phrasing_present(
        self, wrapper_texts: Dict[Path, str]
    ):
        # The wrapper enumerates the forbidden behaviors: "MUST NOT
        # block, pause, serialize, or reduce the parallelism".
        for p, txt in wrapper_texts.items():
            assert "block, pause, serialize" in txt, (
                f"{p.name} no longer enumerates the 'block, pause, "
                "serialize' forbidden behaviors for INV-021"
            )

    def test_synthesis_runs_before_merge_step_at_every_site(
        self, wrapper_texts: Dict[Path, str]
    ):
        # The R-125 wording binds synthesis runs BEFORE merge step
        # at SKILL.md §A.8 / §A.10 — the ordering constraint that
        # makes the N-1 overlap window observable.
        for p, txt in wrapper_texts.items():
            assert "BEFORE the merge step" in txt, (
                f"{p.name} no longer pins synthesis runs BEFORE merge "
                "step — INV-021 ordering constraint regressed"
            )


# ---------------------------------------------------------------------------
# AC3 — Spawn-log timing shows N-1 partitions overlap synthesis.
# ---------------------------------------------------------------------------


class TestCanonicalConcurrentSpawnLogPasses:
    """Load-bearing AC3 binding: the canonical spawn-log fixture has
    all N-1 sibling partitions' execution windows overlapping the
    exhausted partition's synthesis window. The INV-021 checker
    returns ok=True."""

    def test_check_returns_ok(self, overlap_spawn_log):
        cohort, exhausted_id = overlap_spawn_log
        result = check_inv_021_n_minus_1_concurrency(cohort, exhausted_id)
        assert result.ok, (
            f"canonical concurrent spawn-log wrongly flagged: "
            f"symbol={result.symbol!r} detail={result.detail!r}"
        )
        assert result.symbol is None

    def test_all_n_minus_1_siblings_overlap(self, overlap_spawn_log):
        cohort, exhausted_id = overlap_spawn_log
        result = check_inv_021_n_minus_1_concurrency(cohort, exhausted_id)
        siblings = [p for p in cohort if p.partition_id != exhausted_id]
        assert len(result.overlapping_siblings) == len(siblings), (
            f"expected all {len(siblings)} siblings to overlap synthesis; "
            f"got {len(result.overlapping_siblings)} overlapping, "
            f"{len(result.serialized_siblings)} serialized"
        )
        assert result.serialized_siblings == []

    def test_overlap_count_equals_n_minus_1(self, overlap_spawn_log):
        cohort, exhausted_id = overlap_spawn_log
        n = len(cohort)
        result = check_inv_021_n_minus_1_concurrency(cohort, exhausted_id)
        assert len(result.overlapping_siblings) == n - 1, (
            f"expected N-1={n - 1} overlapping siblings; got "
            f"{len(result.overlapping_siblings)}"
        )

    @pytest.mark.parametrize("n_siblings", [1, 2, 3, 4, 8])
    def test_overlap_scales_with_cohort_size(self, n_siblings: int):
        cohort, exhausted_id = build_canonical_overlap_spawn_log(n_siblings)
        # build_canonical_overlap_spawn_log scatters sibling ends by
        # 0.5s starting at syn_start+0.5; widen synthesis_end to cover
        # the largest sibling end for n>3.
        if n_siblings > 3:
            for p in cohort:
                if p.synthesis_end_ts is not None:
                    p.synthesis_end_ts = 10.5 + 0.5 * n_siblings + 1.0
        result = check_inv_021_n_minus_1_concurrency(cohort, exhausted_id)
        assert result.ok, (
            f"N-1 concurrency failed for n_siblings={n_siblings}: {result.detail}"
        )
        assert len(result.overlapping_siblings) == n_siblings


# ---------------------------------------------------------------------------
# AC — Serial spawn-log is rejected as INV-021 violation.
# ---------------------------------------------------------------------------


class TestSerializedSpawnLogRejected:
    """The negative complement of AC3: a spawn-log where the
    sibling cohort completed BEFORE synthesis started evidences
    serialization and MUST be rejected as
    ``INV-021-cohort-serialization-violation``."""

    def test_serialized_spawn_log_rejected(self, serialized_spawn_log):
        cohort, exhausted_id = serialized_spawn_log
        result = check_inv_021_n_minus_1_concurrency(cohort, exhausted_id)
        assert not result.ok
        assert result.symbol == SYM_COHORT_SERIALIZATION, (
            f"serialized spawn-log should reject as "
            f"{SYM_COHORT_SERIALIZATION}: got {result.symbol!r}"
        )

    def test_all_siblings_appear_in_serialized_list(self, serialized_spawn_log):
        cohort, exhausted_id = serialized_spawn_log
        result = check_inv_021_n_minus_1_concurrency(cohort, exhausted_id)
        siblings = [p.partition_id for p in cohort if p.partition_id != exhausted_id]
        # Every sibling ended before synthesis started → all serialized.
        assert sorted(result.serialized_siblings) == sorted(siblings)
        assert result.overlapping_siblings == []

    def test_partial_serialization_rejected(self):
        # Even ONE serialized sibling out of N-1 is a violation —
        # the rule is "all N-1 overlap", not "majority".
        exhausted = PartitionWindow(
            partition_id="p-exhausted",
            start_ts=0.0,
            end_ts=10.0,
            terminal="exhaust",
            synthesis_start_ts=10.5,
            synthesis_end_ts=12.0,
        )
        sibling_concurrent = PartitionWindow(
            partition_id="p-concurrent",
            start_ts=0.0,
            end_ts=11.0,  # overlaps [10.5, 12.0)
            terminal="success",
        )
        sibling_serial = PartitionWindow(
            partition_id="p-serial",
            start_ts=0.0,
            end_ts=10.4,  # ends before syn_start=10.5
            terminal="success",
        )
        cohort = [exhausted, sibling_concurrent, sibling_serial]
        result = check_inv_021_n_minus_1_concurrency(cohort, "p-exhausted")
        assert not result.ok
        assert result.symbol == SYM_COHORT_SERIALIZATION
        assert "p-serial" in result.serialized_siblings
        assert "p-concurrent" in result.overlapping_siblings


# ---------------------------------------------------------------------------
# AC — Spawn-log shape contract checks.
# ---------------------------------------------------------------------------


class TestSpawnLogShapeContract:
    """The check rejects malformed spawn-logs (missing exhausted
    partition, wrong terminal state, missing synthesis window,
    inverted synthesis interval) before evaluating concurrency. Each
    rejection surfaces the same INV-021 symbol because they all
    represent missing evidence for the concurrency claim."""

    def test_missing_exhausted_partition_rejected(self, overlap_spawn_log):
        cohort, _ = overlap_spawn_log
        result = check_inv_021_n_minus_1_concurrency(cohort, "nonexistent-id")
        assert not result.ok and result.symbol == SYM_COHORT_SERIALIZATION

    def test_partition_with_success_terminal_rejected(self):
        # Only exhausted partitions trigger INV-021 — calling the
        # checker on a successful one is meaningless.
        cohort = [
            PartitionWindow(
                partition_id="p-success",
                start_ts=0.0,
                end_ts=5.0,
                terminal="success",
            )
        ]
        result = check_inv_021_n_minus_1_concurrency(cohort, "p-success")
        assert not result.ok and result.symbol == SYM_COHORT_SERIALIZATION

    def test_missing_synthesis_window_rejected(self):
        # Exhausted partition without synthesis_start_ts/end_ts:
        # spawn-log evidence is missing, so the rule cannot be
        # verified — rejected with the same symbol.
        cohort = [
            PartitionWindow(
                partition_id="p-exhausted",
                start_ts=0.0,
                end_ts=10.0,
                terminal="exhaust",
                synthesis_start_ts=None,
                synthesis_end_ts=None,
            )
        ]
        result = check_inv_021_n_minus_1_concurrency(cohort, "p-exhausted")
        assert not result.ok and result.symbol == SYM_COHORT_SERIALIZATION

    def test_inverted_synthesis_window_rejected(self):
        cohort = [
            PartitionWindow(
                partition_id="p-exhausted",
                start_ts=0.0,
                end_ts=10.0,
                terminal="exhaust",
                synthesis_start_ts=12.0,
                synthesis_end_ts=11.0,  # end < start
            )
        ]
        result = check_inv_021_n_minus_1_concurrency(cohort, "p-exhausted")
        assert not result.ok and result.symbol == SYM_COHORT_SERIALIZATION


# ---------------------------------------------------------------------------
# AC — Overlap semantics (half-open interval).
# ---------------------------------------------------------------------------


class TestOverlapSemantics:
    """``PartitionWindow.overlaps`` uses half-open interval semantics:
    a sibling that ends exactly at synthesis_start does NOT overlap
    (it serialized). The wrapper bullet's "overlapping in wall-clock
    time" wording requires strict overlap, not touching endpoints."""

    def test_sibling_ends_exactly_at_synthesis_start_does_not_overlap(self):
        exhausted = PartitionWindow(
            partition_id="p-exhausted",
            start_ts=0.0,
            end_ts=10.0,
            terminal="exhaust",
            synthesis_start_ts=10.0,
            synthesis_end_ts=12.0,
        )
        # Sibling ends exactly at synthesis_start; touching, not overlapping.
        sibling = PartitionWindow(
            partition_id="p-touching",
            start_ts=0.0,
            end_ts=10.0,
            terminal="success",
        )
        result = check_inv_021_n_minus_1_concurrency(
            [exhausted, sibling], "p-exhausted"
        )
        assert not result.ok
        assert "p-touching" in result.serialized_siblings

    def test_sibling_starts_exactly_at_synthesis_end_does_not_overlap(self):
        exhausted = PartitionWindow(
            partition_id="p-exhausted",
            start_ts=0.0,
            end_ts=5.0,
            terminal="exhaust",
            synthesis_start_ts=5.5,
            synthesis_end_ts=7.0,
        )
        # Sibling starts when synthesis ends.
        sibling = PartitionWindow(
            partition_id="p-late",
            start_ts=7.0,
            end_ts=10.0,
            terminal="success",
        )
        result = check_inv_021_n_minus_1_concurrency(
            [exhausted, sibling], "p-exhausted"
        )
        assert not result.ok
        assert "p-late" in result.serialized_siblings

    def test_sibling_window_fully_contains_synthesis_overlaps(self):
        exhausted = PartitionWindow(
            partition_id="p-exhausted",
            start_ts=0.0,
            end_ts=5.0,
            terminal="exhaust",
            synthesis_start_ts=5.5,
            synthesis_end_ts=7.0,
        )
        # Sibling runs from before synthesis starts to after it ends.
        sibling = PartitionWindow(
            partition_id="p-long",
            start_ts=4.0,
            end_ts=8.0,
            terminal="success",
        )
        result = check_inv_021_n_minus_1_concurrency(
            [exhausted, sibling], "p-exhausted"
        )
        assert result.ok
        assert "p-long" in result.overlapping_siblings


# ---------------------------------------------------------------------------
# AC — NFR-CONV.10 binding (parallel-research invariant).
# ---------------------------------------------------------------------------


class TestNfrConv10ParallelResearchBinding:
    """The R-125 wrapper bullet pins INV-021 as 'the per-cohort
    instantiation of the NFR-CONV.10 parallel-research invariant'.
    A violation of INV-021 is therefore a violation of NFR-CONV.10
    at the cohort scope — the spawn-log evidence is the binding."""

    def test_serialized_spawn_log_degrades_nfr_conv_10(self):
        cohort, exhausted_id = build_serialized_spawn_log(n_siblings=3)
        result = check_inv_021_n_minus_1_concurrency(cohort, exhausted_id)
        assert not result.ok, (
            "serialization is the NFR-CONV.10 degradation signal — the "
            "fixture's serialized spawn-log MUST be flagged"
        )
        assert "synthesis" in (result.detail or "")

    def test_concurrent_spawn_log_preserves_nfr_conv_10(self):
        cohort, exhausted_id = build_canonical_overlap_spawn_log(n_siblings=4)
        # Widen synthesis_end to cover all 4 siblings.
        for p in cohort:
            if p.synthesis_end_ts is not None:
                p.synthesis_end_ts = 13.0
        result = check_inv_021_n_minus_1_concurrency(cohort, exhausted_id)
        assert result.ok
        assert len(result.overlapping_siblings) == 4

    def test_skill_md_a8_pins_synthesis_runs_before_merge(self):
        # SKILL.md §A.8 merge step pinned by R-127 / T06.11; the
        # within-cycle collapse runs BEFORE gate evaluation, and the
        # INV-021 wording in the same SKILL.md text binds synthesis
        # composition BEFORE the merge step. The TEST-021 evidence
        # binding requires both wordings to coexist.
        skill_text = SKILL_SRC.read_text(encoding="utf-8")
        assert "BEFORE the merge step" in skill_text
        assert "INV-021" in skill_text
