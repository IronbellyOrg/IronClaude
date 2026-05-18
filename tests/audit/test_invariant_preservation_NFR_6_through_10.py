"""TEST-025 — Composite invariant-preservation fixture (T07.09 / D-0090 / R-150).

Single composite fixture exercising each of the FIVE load-bearing
invariants the Task-Builder Convergence release commits to preserve.
Per ``phase-7-tasklist.md`` line 403:

    "Composite fixture exercising all 5 invariants (self-contained-item,
     evidence-bound-item, persistent-artifact, zero-trust QA,
     parallel-research) per Negative Criteria."

Roadmap row R-150 names this fixture and binds its surface to
NFR-CONV.6..10. Each invariant has its own dedicated fixture and test
module already landed earlier in Phase-7 (T07.04, T07.05, T07.07,
T07.08, plus the M6 parallel-research test); TEST-025 is the
**composite preservation gate** that re-exercises one named surface per
invariant in a single pytest run. The point is not to duplicate the
per-invariant catalogues but to fail loudly the moment any one of the
five surfaces drifts — a single grep-able run that names each
invariant the release commits to preserve.

Invariant → surface re-exercised:

  1. NFR-CONV.6 self-contained-item — Q-DM-1 five-field schema:
     ``{Context, Action, Output, Verification, Completion gate}``.
     Re-exercise: TB-Add-1..8 catalogue against the full-fields fixture
     emits only PASS verdicts; the field-stripped twin produces a
     TB-Add-1 FAIL naming the stripped field.
     Detector source: ``test_nfr_conv_6_self_contained.py``.

  2. NFR-CONV.7 evidence-bound-item — per-item Context fields carry
     ``file:line`` citations or ``<!-- evidence-absence: ... -->``
     justifications.
     Re-exercise: TB-Add-8 verdict matrix bare-path=FAIL /
     file-line=PASS / justified-absence=PASS over the M2 ``##
     Execution Context``-bearing fixtures.
     Detector source: ``test_evidence_bound_tb_add_8.py``.

  3. NFR-CONV.8 persistent-`.dev/tasks/`-artifact — the canonical
     subdirectory set ``{research, qa, synthesis, reviews,
     phase-outputs}`` is present in the working-tree's ``.dev/tasks/``
     layout. ``phase-outputs/`` is the on-disk physical name for the
     logical ``adversarial`` bucket per D-0087 §3.1. No rename, no
     replacement.
     Evidence source: ``.dev/releases/current/task-builder-merge/artifacts/D-0087/evidence.md``.

  4. NFR-CONV.9 zero-trust QA — the verbatim PASS/FAIL definitions in
     ``src/superclaude/agents/rf-qa.md`` are byte-identical to the
     frozen baseline (anchor: ``rf-qa.md:141-142`` pre-PR-03 /
     ``:144-145`` post-PR-03; the test asserts the *bytes*, not the
     line numbers); a 1-LOW-finding fixture scores FAIL.
     Detector source: ``test_nfr_conv_9_zero_trust.py``.

  5. NFR-CONV.10 parallel-research — on one partition's escalation
     ladder exhaust the remaining N-1 sibling partitions overlap (in
     wall-clock time) with the exhausted partition's synthesis. A
     serialized spawn-log is rejected with
     ``INV-021-cohort-serialization-violation``; a concurrent spawn-log
     is accepted.
     Detector source: ``test_dnsp_does_not_serialize_cohort.py``.

The composite gate operates as five independent assertions: any one
invariant regressing produces a named FAIL in the pytest output.

Run: ``uv run pytest tests/audit/test_invariant_preservation_NFR_6_through_10.py -v``
"""

from __future__ import annotations

from pathlib import Path

import pytest

from tests.audit.test_dnsp_does_not_serialize_cohort import (
    SYM_COHORT_SERIALIZATION,
    build_canonical_overlap_spawn_log,
    build_serialized_spawn_log,
    check_inv_021_n_minus_1_concurrency,
)
from tests.audit.test_evidence_bound_tb_add_8 import (
    BARE_PATH_FIXTURE,
    FILE_LINE_FIXTURE,
    JUSTIFIED_ABSENCE_FIXTURE,
    tb_add_8,
)
from tests.audit.test_nfr_conv_6_self_contained import (
    FULL_FIELDS_FIXTURE,
    STRIPPED_FIXTURE,
    SCHEMA_FIELDS,
    _aggregate,
    run_all_tb_add,
    tb_add_1,
)
from tests.audit.test_nfr_conv_9_zero_trust import (
    FAIL_BULLET,
    FIX_ONE_LOW,
    PASS_BULLET,
    RF_QA_SRC,
    SEVERITY_TRIPLE,
    _score_rf_qa_verdict,
)

REPO_ROOT = Path(__file__).resolve().parents[2]
DEV_TASKS_ROOT = REPO_ROOT / ".dev" / "tasks"

# NFR-CONV.8 contract — the canonical subdirectory set per D-0087 §3.1.
# 'phase-outputs' is the on-disk physical name for the logical
# 'adversarial' bucket (mapping pre-existing on master, unchanged on
# HEAD; documented in D-0087 §3.1).
CANONICAL_SUBDIRS = ("research", "qa", "synthesis", "reviews", "phase-outputs")

# Roadmap anchor — the five NFR-CONV labels this composite gate covers.
INVARIANTS = (
    ("NFR-CONV.6", "self-contained-item"),
    ("NFR-CONV.7", "evidence-bound-item"),
    ("NFR-CONV.8", "persistent-.dev/tasks/-artifact"),
    ("NFR-CONV.9", "zero-trust QA"),
    ("NFR-CONV.10", "parallel-research"),
)


# ---------------------------------------------------------------------------
# Composite-fixture wiring sanity. The five detector imports above ARE the
# composite fixture: each invariant's source-of-truth detector is loaded into
# one test module so a single pytest run exercises every surface.
# ---------------------------------------------------------------------------


class TestCompositeFixtureWiring:
    """The composite gate must wire ALL five invariants. A regression that
    drops a wire (e.g., an import lost during refactor) is the failure mode
    this class guards against."""

    def test_five_invariants_enumerated(self):
        assert len(INVARIANTS) == 5, (
            f"composite gate must cover exactly 5 invariants per R-150; "
            f"INVARIANTS list has {len(INVARIANTS)}"
        )
        labels = {label for label, _ in INVARIANTS}
        expected = {
            "NFR-CONV.6",
            "NFR-CONV.7",
            "NFR-CONV.8",
            "NFR-CONV.9",
            "NFR-CONV.10",
        }
        assert labels == expected, (
            f"composite must name NFR-CONV.6..10; got {labels}"
        )

    def test_all_detector_fixtures_resolvable(self):
        """Each invariant's source-of-truth fixture path exists on disk."""
        for fixture in (
            FULL_FIELDS_FIXTURE,
            STRIPPED_FIXTURE,
            BARE_PATH_FIXTURE,
            FILE_LINE_FIXTURE,
            JUSTIFIED_ABSENCE_FIXTURE,
            FIX_ONE_LOW,
            RF_QA_SRC,
        ):
            assert fixture.is_file(), f"missing detector fixture: {fixture}"

    def test_dev_tasks_root_exists(self):
        """NFR-CONV.8 surface — the persistent-artifact root."""
        assert DEV_TASKS_ROOT.is_dir(), (
            f"NFR-CONV.8 cannot be exercised: {DEV_TASKS_ROOT} missing"
        )


# ---------------------------------------------------------------------------
# Invariant 1 — NFR-CONV.6 self-contained-item.
# Re-exercise: full-fields fixture passes TB-Add-1..8; stripped fixture
# FAILs TB-Add-1 naming the stripped field.
# ---------------------------------------------------------------------------


class TestInvariant1_SelfContainedItem:
    """NFR-CONV.6 — Q-DM-1 five-field schema preservation."""

    INVARIANT_LABEL = "NFR-CONV.6 self-contained-item"

    def test_full_fields_fixture_all_tb_add_pass(self):
        results = run_all_tb_add(FULL_FIELDS_FIXTURE.read_text(encoding="utf-8"))
        aggregate = {check: _aggregate(results[check]) for check in results}
        fails = {k: v for k, v in aggregate.items() if v == "FAIL"}
        assert not fails, (
            f"{self.INVARIANT_LABEL}: full-fields fixture must produce zero "
            f"FAIL verdicts across TB-Add-1..8; got {fails}"
        )

    def test_stripped_fixture_fails_tb_add_1_with_named_field(self):
        results = tb_add_1(STRIPPED_FIXTURE.read_text(encoding="utf-8"))
        fails = [r for r in results if r.verdict == "FAIL"]
        assert fails, (
            f"{self.INVARIANT_LABEL}: stripped fixture must yield ≥1 "
            f"TB-Add-1 FAIL (got {[r.detail for r in results]})"
        )
        named = [
            r for r in fails if "1.1" in r.detail and "Output" in r.detail
        ]
        assert named, (
            f"{self.INVARIANT_LABEL}: TB-Add-1 FAIL must name item-ID '1.1' "
            f"AND stripped field 'Output'; got {[r.detail for r in fails]}"
        )

    def test_q_dm_1_schema_field_count(self):
        """The five-field schema names the invariant — confirm the
        composite fixture sees all five labels."""
        assert len(SCHEMA_FIELDS) == 5, (
            f"{self.INVARIANT_LABEL}: Q-DM-1 schema must have 5 fields; "
            f"got {SCHEMA_FIELDS}"
        )


# ---------------------------------------------------------------------------
# Invariant 2 — NFR-CONV.7 evidence-bound-item.
# Re-exercise: TB-Add-8 verdict matrix (bare=FAIL / file-line=PASS /
# justified-absence=PASS).
# ---------------------------------------------------------------------------


class TestInvariant2_EvidenceBoundItem:
    """NFR-CONV.7 — per-item Context evidence binding."""

    INVARIANT_LABEL = "NFR-CONV.7 evidence-bound-item"

    def test_bare_path_fixture_fails_tb_add_8(self):
        results = tb_add_8(BARE_PATH_FIXTURE.read_text(encoding="utf-8"))
        fails = [r for r in results if r.verdict == "FAIL"]
        assert fails, (
            f"{self.INVARIANT_LABEL}: bare-path fixture must produce ≥1 "
            f"TB-Add-8 FAIL (got {[(r.item_id, r.verdict, r.reason) for r in results]})"
        )

    def test_file_line_fixture_all_pass(self):
        results = tb_add_8(FILE_LINE_FIXTURE.read_text(encoding="utf-8"))
        assert results, (
            f"{self.INVARIANT_LABEL}: file:line fixture must contain ≥1 Context item"
        )
        assert all(r.verdict == "PASS" for r in results), (
            f"{self.INVARIANT_LABEL}: file:line fixture must produce only PASS "
            f"(got {[(r.item_id, r.verdict, r.reason) for r in results]})"
        )

    def test_justified_absence_fixture_all_pass(self):
        results = tb_add_8(JUSTIFIED_ABSENCE_FIXTURE.read_text(encoding="utf-8"))
        assert results, (
            f"{self.INVARIANT_LABEL}: justified-absence fixture must contain "
            f"≥1 Context item"
        )
        assert all(r.verdict == "PASS" for r in results), (
            f"{self.INVARIANT_LABEL}: justified-absence fixture must produce "
            f"only PASS (got {[(r.item_id, r.verdict, r.reason) for r in results]})"
        )


# ---------------------------------------------------------------------------
# Invariant 3 — NFR-CONV.8 persistent-.dev/tasks/-artifact.
# Re-exercise: the canonical subdir set {research, qa, synthesis, reviews,
# phase-outputs} is present in the working-tree's `.dev/tasks/` layout.
# Backed by D-0087 §3.1 (pre/post diff = empty).
# ---------------------------------------------------------------------------


class TestInvariant3_PersistentArtifact:
    """NFR-CONV.8 — `.dev/tasks/<task-id>/` directory layout preservation."""

    INVARIANT_LABEL = "NFR-CONV.8 persistent-.dev/tasks/-artifact"

    @pytest.fixture(scope="class")
    def observed_subdirs(self) -> frozenset:
        """Collect the set of *immediate* subdirectory names directly under
        each ``<task-id>/`` directory in ``.dev/tasks/{to-do,done}/``.

        Returns a frozenset over all such names. The NFR-CONV.8 contract
        requires this set to be a superset of CANONICAL_SUBDIRS — every
        canonical bucket name must appear somewhere in the live tree
        (else a rename has occurred).
        """
        names: set[str] = set()
        for bucket in ("to-do", "done"):
            bucket_dir = DEV_TASKS_ROOT / bucket
            if not bucket_dir.is_dir():
                continue
            for task_dir in bucket_dir.iterdir():
                if not task_dir.is_dir():
                    continue
                if not task_dir.name.startswith("TASK-"):
                    continue
                for child in task_dir.iterdir():
                    if child.is_dir():
                        names.add(child.name)
        return frozenset(names)

    def test_canonical_subdirs_all_present(self, observed_subdirs: frozenset):
        missing = [name for name in CANONICAL_SUBDIRS if name not in observed_subdirs]
        assert not missing, (
            f"{self.INVARIANT_LABEL}: canonical subdir(s) {missing} missing "
            f"from live `.dev/tasks/` tree — INV-018 / NFR-CONV.8 violated. "
            f"Observed: {sorted(observed_subdirs)}"
        )

    def test_canonical_subdir_set_unchanged_by_rename(
        self, observed_subdirs: frozenset
    ):
        """Cross-check: every canonical name has its exact byte-string
        present (no case change, no plural-form drift)."""
        for name in CANONICAL_SUBDIRS:
            assert name in observed_subdirs, (
                f"{self.INVARIANT_LABEL}: canonical name {name!r} not present "
                f"byte-identically — a rename or case change has occurred"
            )

    def test_task_id_naming_pattern_preserved(self):
        """Per D-0087 §3.2 the task-id naming pattern is
        ``TASK-{TYPE}-YYYYMMDD-...`` for one of the known TYPEs.
        Every task directory in ``.dev/tasks/{to-do,done}/`` must
        match that pattern."""
        import re

        pattern = re.compile(
            r"^TASK-(E2E|PRD|RESEARCH|RF|TDD|RC|MERGE|SC)"
            r"(-track-\d+)?-\d{8}",
        )
        bad: list[str] = []
        for bucket in ("to-do", "done"):
            bucket_dir = DEV_TASKS_ROOT / bucket
            if not bucket_dir.is_dir():
                continue
            for task_dir in bucket_dir.iterdir():
                if not task_dir.is_dir():
                    continue
                if not task_dir.name.startswith("TASK-"):
                    continue
                if not pattern.match(task_dir.name):
                    bad.append(task_dir.name)
        assert not bad, (
            f"{self.INVARIANT_LABEL}: task-id naming pattern drifted; "
            f"non-matching dirs: {bad[:5]}"
        )


# ---------------------------------------------------------------------------
# Invariant 4 — NFR-CONV.9 zero-trust QA.
# Re-exercise: PASS/FAIL bullet strings are byte-identical in rf-qa.md;
# 1-LOW-finding fixture scores FAIL.
# ---------------------------------------------------------------------------


class TestInvariant4_ZeroTrustQA:
    """NFR-CONV.9 — rf-qa.md PASS/FAIL definitions + 1-LOW gate."""

    INVARIANT_LABEL = "NFR-CONV.9 zero-trust QA"

    @pytest.fixture(scope="class")
    def rf_qa_text(self) -> str:
        return RF_QA_SRC.read_text(encoding="utf-8")

    def test_pass_bullet_byte_identical(self, rf_qa_text: str):
        assert PASS_BULLET in rf_qa_text, (
            f"{self.INVARIANT_LABEL}: PASS bullet drifted from frozen baseline"
        )

    def test_fail_bullet_byte_identical(self, rf_qa_text: str):
        assert FAIL_BULLET in rf_qa_text, (
            f"{self.INVARIANT_LABEL}: FAIL bullet drifted from frozen baseline"
        )

    def test_severity_triple_intact(self, rf_qa_text: str):
        for label in SEVERITY_TRIPLE:
            assert label in rf_qa_text, (
                f"{self.INVARIANT_LABEL}: severity label {label!r} missing"
            )

    def test_one_low_finding_scores_fail(self):
        report = FIX_ONE_LOW.read_text(encoding="utf-8")
        verdict = _score_rf_qa_verdict(report)
        assert verdict == "FAIL", (
            f"{self.INVARIANT_LABEL}: 1-LOW-finding fixture must score FAIL "
            f"per rf-qa.md:145; got {verdict}"
        )


# ---------------------------------------------------------------------------
# Invariant 5 — NFR-CONV.10 parallel-research.
# Re-exercise: cohort-concurrency checker rejects serialized spawn-logs and
# accepts concurrent ones (INV-021 / R-125).
# ---------------------------------------------------------------------------


class TestInvariant5_ParallelResearch:
    """NFR-CONV.10 — cohort never serialises behind synthesis."""

    INVARIANT_LABEL = "NFR-CONV.10 parallel-research"

    def test_concurrent_spawn_log_accepted(self):
        cohort, exhausted_id = build_canonical_overlap_spawn_log(n_siblings=3)
        result = check_inv_021_n_minus_1_concurrency(cohort, exhausted_id)
        assert result.ok, (
            f"{self.INVARIANT_LABEL}: canonical overlap spawn-log rejected: "
            f"symbol={result.symbol} detail={result.detail}"
        )
        assert len(result.overlapping_siblings) == 3, (
            f"{self.INVARIANT_LABEL}: expected 3 overlapping siblings; "
            f"got {result.overlapping_siblings}"
        )
        assert not result.serialized_siblings

    def test_serialized_spawn_log_rejected(self):
        cohort, exhausted_id = build_serialized_spawn_log(n_siblings=3)
        result = check_inv_021_n_minus_1_concurrency(cohort, exhausted_id)
        assert not result.ok, (
            f"{self.INVARIANT_LABEL}: serialized spawn-log must be rejected"
        )
        assert result.symbol == SYM_COHORT_SERIALIZATION, (
            f"{self.INVARIANT_LABEL}: rejection symbol must be "
            f"{SYM_COHORT_SERIALIZATION!r}; got {result.symbol!r}"
        )
        assert len(result.serialized_siblings) == 3, (
            f"{self.INVARIANT_LABEL}: all 3 siblings should be flagged "
            f"serialized; got {result.serialized_siblings}"
        )


# ---------------------------------------------------------------------------
# Composite verdict — the gate's headline assertion. If every invariant
# class above passed, the composite gate emits a single aggregated PASS
# trace listing each invariant by name. If any class FAILed pytest will
# have already stopped this test from running.
# ---------------------------------------------------------------------------


class TestCompositeAggregateVerdict:
    """Single aggregated assertion that names each invariant. When this
    test PASSes, all 5 invariants are preserved at the per-surface
    detector level."""

    def test_all_five_invariants_pass(self):
        verdicts = {}

        # NFR-CONV.6 — full-fields fixture has zero FAILs across TB-Add-1..8.
        r6 = run_all_tb_add(FULL_FIELDS_FIXTURE.read_text(encoding="utf-8"))
        v6 = "PASS" if all(_aggregate(r6[c]) == "PASS" for c in r6) else "FAIL"
        verdicts["NFR-CONV.6"] = v6

        # NFR-CONV.7 — bare/file-line/absence verdict matrix.
        bare = "FAIL" if any(r.verdict == "FAIL"
                              for r in tb_add_8(BARE_PATH_FIXTURE.read_text(encoding="utf-8"))) else "PASS"
        fl = "PASS" if all(r.verdict == "PASS"
                            for r in tb_add_8(FILE_LINE_FIXTURE.read_text(encoding="utf-8"))) else "FAIL"
        absc = "PASS" if all(r.verdict == "PASS"
                              for r in tb_add_8(JUSTIFIED_ABSENCE_FIXTURE.read_text(encoding="utf-8"))) else "FAIL"
        v7 = "PASS" if (bare, fl, absc) == ("FAIL", "PASS", "PASS") else "FAIL"
        verdicts["NFR-CONV.7"] = v7

        # NFR-CONV.8 — canonical subdir set is a subset of the live tree.
        live: set[str] = set()
        for bucket in ("to-do", "done"):
            bucket_dir = DEV_TASKS_ROOT / bucket
            if not bucket_dir.is_dir():
                continue
            for task_dir in bucket_dir.iterdir():
                if not task_dir.is_dir():
                    continue
                if not task_dir.name.startswith("TASK-"):
                    continue
                for child in task_dir.iterdir():
                    if child.is_dir():
                        live.add(child.name)
        v8 = "PASS" if all(n in live for n in CANONICAL_SUBDIRS) else "FAIL"
        verdicts["NFR-CONV.8"] = v8

        # NFR-CONV.9 — PASS/FAIL bullets byte-identical + 1-LOW scores FAIL.
        rf_qa_text = RF_QA_SRC.read_text(encoding="utf-8")
        bullets_ok = PASS_BULLET in rf_qa_text and FAIL_BULLET in rf_qa_text
        one_low = _score_rf_qa_verdict(FIX_ONE_LOW.read_text(encoding="utf-8"))
        verdicts["NFR-CONV.9"] = "PASS" if (bullets_ok and one_low == "FAIL") else "FAIL"

        # NFR-CONV.10 — concurrent accepts AND serialized rejects.
        cohort_ok, ex_ok = build_canonical_overlap_spawn_log(n_siblings=3)
        ok_res = check_inv_021_n_minus_1_concurrency(cohort_ok, ex_ok)
        cohort_bad, ex_bad = build_serialized_spawn_log(n_siblings=3)
        bad_res = check_inv_021_n_minus_1_concurrency(cohort_bad, ex_bad)
        verdicts["NFR-CONV.10"] = (
            "PASS"
            if (ok_res.ok and not bad_res.ok
                and bad_res.symbol == SYM_COHORT_SERIALIZATION)
            else "FAIL"
        )

        expected = {label: "PASS" for label, _ in INVARIANTS}
        assert verdicts == expected, (
            f"composite invariant-preservation gate failed: {verdicts}; "
            f"expected all PASS"
        )
