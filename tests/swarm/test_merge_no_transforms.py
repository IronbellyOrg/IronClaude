"""T05.11 -- AC-011 no-transforms boundary variant for the merge path
(R-109 / D-0090).

Pins the AC-011 neutrality boundary at the M5 merge surface:
:func:`superclaude.cli.swarm.merge.mechanical_merge` performs **no
scoring, deduplication, reordering, rewriting, or filtering of worker
findings**, even when the caller selects ``amalgamation_mode =
normalize+merge``. Every worker body is concatenated verbatim, in
slot-index order, with the one-line provenance header
``## From {model_label} ({elapsed_ms}ms)`` prepended -- nothing else.

Complementary to ``tests/swarm/test_merge_mechanical_only.py`` (T05.09,
NFR-009), which fixes the 3-worker concat / provenance-header shape.
This file is the AC-011 surface specifically: it mirrors the
finding-shaped fixture pattern used by
``tests/swarm/test_recipe_no_judging.py`` (T04.14) on the *recipe*
side, so the merge-side gate fails for the same reason and on the same
axes if scoring or judging logic ever leaks into ``merge.py``.

Axes asserted (per recipe-side T04.14 contract, ported to merge):

* **Count** -- N findings in -> N findings out. Row IDs ``F-NN`` are
  enumerated in the merged output and the count must match the input
  set (duplicates included).
* **Order** -- sentinel tokens ``TOKEN-A`` through ``TOKEN-D`` appear
  in a known sequence inside each worker body; the merged output must
  contain them at strictly-increasing offsets so any sort / rerank /
  rewrite shows up as a failing offset chain.
* **Duplicates (cross-worker)** -- ``TOKEN-A`` appears in BOTH worker
  bodies. AC-011 forbids cross-worker dedup, so the merged output must
  contain ``TOKEN-A`` at least once per worker body. Any set-based
  dedup would collapse this to a single occurrence and trip the
  assertion.
* **Duplicates (within-worker)** -- ``F-01`` appears twice inside the
  same worker body (positions 1 and N). AC-011 forbids within-section
  dedup as well; the merged output must keep the duplicate row intact.

The recipe-side AC-011 sweep (T04.14) and this merge-side variant
together cover the FR-012 / AC-011 contract end-to-end: recipes do not
judge findings, and the merge step that stitches recipe outputs into a
single document does not judge them either.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from superclaude.cli.swarm.merge import mechanical_merge
from superclaude.cli.swarm.models import WorkerResult

# Sentinel tokens used to lock body order across the merged document.
# Naming mirrors tests/swarm/test_recipe_no_judging.py (T04.14) so the
# two AC-011 surfaces stay shape-aligned.
TOKEN_A = "TOKEN-A"
TOKEN_B = "TOKEN-B"
TOKEN_C = "TOKEN-C"
TOKEN_D = "TOKEN-D"


WORKER0_BODY = (
    "| ID | Finding | Severity | Confidence |\n"
    "|----|---------|----------|------------|\n"
    f"| F-01 | {TOKEN_A} duplicate-finding row | high | 0.9 |\n"
    f"| F-02 | {TOKEN_B} bug in handler | medium | 0.7 |\n"
    f"| F-03 | {TOKEN_C} leaky abstraction | low | 0.5 |\n"
    f"| F-01 | {TOKEN_A} duplicate-finding row | high | 0.9 |\n"
)

WORKER1_BODY = (
    "| ID | Finding | Severity | Confidence |\n"
    "|----|---------|----------|------------|\n"
    f"| F-10 | {TOKEN_A} same-issue-as-worker0 | high | 0.85 |\n"
    f"| F-11 | {TOKEN_D} distinct second-worker finding | medium | 0.6 |\n"
)


def _write_worker(
    tmp_path: Path,
    *,
    index: int,
    model_label: str,
    elapsed_ms: int,
    body: str,
) -> WorkerResult:
    final_path = tmp_path / f"worker-{index:02d}.final.md"
    final_path.write_text(body, encoding="utf-8")
    return WorkerResult(
        index=index,
        path=str(final_path),
        raw_path=str(tmp_path / f"worker-{index:02d}.raw.md"),
        meta_path=str(tmp_path / f"worker-{index:02d}.meta.json"),
        final_path=str(final_path),
        model_id=f"model-id-{index}",
        model_label=model_label,
        bytes=len(body.encode("utf-8")),
        status="success",
        attempts=1,
        elapsed_ms=elapsed_ms,
    )


@pytest.fixture()
def two_workers_with_duplicates(tmp_path: Path) -> list[WorkerResult]:
    """Two-worker fixture with an intentional cross-worker duplicate
    (``TOKEN-A`` in both bodies) and an intentional within-worker
    duplicate (``F-01`` repeated inside worker 0). Either dedup form
    is an AC-011 violation."""
    return [
        _write_worker(
            tmp_path,
            index=0,
            model_label="gpt-5-codex",
            elapsed_ms=1111,
            body=WORKER0_BODY,
        ),
        _write_worker(
            tmp_path,
            index=1,
            model_label="claude-haiku-4.5",
            elapsed_ms=2222,
            body=WORKER1_BODY,
        ),
    ]


# --- Axis 1: count ---------------------------------------------------------


def test_ac011_merge_preserves_total_finding_count(
    two_workers_with_duplicates: list[WorkerResult],
) -> None:
    """N findings in -> N findings out, across both workers.

    Worker 0 contributes 4 rows (F-01, F-02, F-03, F-01 duplicate);
    worker 1 contributes 2 rows (F-10, F-11). The merged output must
    surface all 6 rows. Any dedup -- cross-worker or within-worker --
    drops the count below 6 and trips this assertion.
    """
    merged = mechanical_merge(two_workers_with_duplicates)
    row_count = sum(
        1
        for line in merged.splitlines()
        if line.startswith("| F-") and "| Finding |" not in line
    )
    assert row_count == 6, (
        "AC-011 forbids dedup/filter in merge; expected 6 finding rows "
        f"(4 from worker 0 + 2 from worker 1), got {row_count}.\n\n"
        f"Merged output was:\n{merged}"
    )


# --- Axis 2: order ---------------------------------------------------------


def test_ac011_merge_preserves_worker_section_order(
    two_workers_with_duplicates: list[WorkerResult],
) -> None:
    """Worker 0's section must appear before worker 1's in the merged
    output. AC-011 forbids reorder across workers; only slot-index
    ordering is permitted, and worker 0 < worker 1."""
    merged = mechanical_merge(two_workers_with_duplicates)
    pos_worker0_header = merged.find("## From gpt-5-codex (1111ms)")
    pos_worker1_header = merged.find("## From claude-haiku-4.5 (2222ms)")
    assert -1 < pos_worker0_header < pos_worker1_header, (
        "merged output must place worker 0 (slot index 0) before "
        f"worker 1 (slot index 1); got positions "
        f"worker0={pos_worker0_header}, worker1={pos_worker1_header}"
    )


def test_ac011_merge_preserves_within_section_order(
    two_workers_with_duplicates: list[WorkerResult],
) -> None:
    """Within worker 0's section the sentinel tokens must appear in
    authored order ``TOKEN_A -> TOKEN_B -> TOKEN_C``. Any sort,
    severity rerank, or confidence reorder shuffles these and the
    offset chain breaks."""
    merged = mechanical_merge(two_workers_with_duplicates)
    pos_a = merged.find(TOKEN_A)
    pos_b = merged.find(TOKEN_B)
    pos_c = merged.find(TOKEN_C)
    assert -1 < pos_a < pos_b < pos_c, (
        "AC-011 forbids within-section reorder; expected "
        f"TOKEN_A < TOKEN_B < TOKEN_C, got "
        f"A={pos_a}, B={pos_b}, C={pos_c}"
    )


def test_ac011_merge_preserves_within_section_order_when_sort_would_reorder(
    tmp_path: Path,
) -> None:
    """Defence-in-depth: a single-worker body whose lines would land
    in a different order under lexicographic sort. If merge ever
    introduces a ``.sort()``, the offset chain below collapses."""
    body = "zebra-finding\nalpha-finding\nmango-finding\n"
    worker = _write_worker(
        tmp_path,
        index=0,
        model_label="m",
        elapsed_ms=10,
        body=body,
    )
    merged = mechanical_merge([worker])
    pos_zebra = merged.find("zebra-finding")
    pos_alpha = merged.find("alpha-finding")
    pos_mango = merged.find("mango-finding")
    assert -1 < pos_zebra < pos_alpha < pos_mango, (
        "lexicographic order would yield alpha < mango < zebra; "
        "merge must preserve authored order instead. Got "
        f"zebra={pos_zebra}, alpha={pos_alpha}, mango={pos_mango}"
    )


# --- Axis 3: duplicates (cross-worker) ------------------------------------


def test_ac011_merge_does_not_deduplicate_across_workers(
    two_workers_with_duplicates: list[WorkerResult],
) -> None:
    """``TOKEN_A`` appears in both worker bodies (worker 0 row F-01,
    worker 1 row F-10). AC-011 forbids cross-worker dedup; the merged
    output must keep both occurrences (plus the worker-0 within-section
    duplicate -> 3 total)."""
    merged = mechanical_merge(two_workers_with_duplicates)
    occurrences = merged.count(TOKEN_A)
    assert occurrences == 3, (
        "AC-011 forbids cross-worker dedup; expected TOKEN_A 3 times "
        "(twice in worker 0, once in worker 1), got "
        f"{occurrences} occurrence(s).\n\nMerged output was:\n{merged}"
    )


# --- Axis 4: duplicates (within-worker) -----------------------------------


def test_ac011_merge_does_not_deduplicate_within_section(
    two_workers_with_duplicates: list[WorkerResult],
) -> None:
    """``F-01`` is intentionally repeated inside worker 0's body. A
    within-section ``set(...)`` or ``drop_duplicates`` would collapse
    this. AC-011 forbids it; the row must survive verbatim, twice."""
    merged = mechanical_merge(two_workers_with_duplicates)
    f01_rows = sum(1 for line in merged.splitlines() if line.startswith("| F-01 |"))
    assert f01_rows == 2, (
        "AC-011 forbids within-section dedup; expected the duplicate "
        f"F-01 row to appear twice, got {f01_rows}.\n\n"
        f"Merged output was:\n{merged}"
    )


# --- Axis 5: verbatim body ------------------------------------------------


def test_ac011_merge_preserves_each_worker_body_verbatim(
    two_workers_with_duplicates: list[WorkerResult],
) -> None:
    """Each worker body must appear in the merged output without any
    rewrite, paraphrase, or reformat. Trailing-newline normalization
    via ``rstrip()`` is the only permitted shape change inside a
    section, so ``WORKERN_BODY.rstrip()`` is the assertion target."""
    merged = mechanical_merge(two_workers_with_duplicates)
    assert WORKER0_BODY.rstrip() in merged, (
        "worker 0 body was modified by merge; AC-011 forbids rewrite. "
        f"Merged output was:\n{merged}"
    )
    assert WORKER1_BODY.rstrip() in merged, (
        "worker 1 body was modified by merge; AC-011 forbids rewrite. "
        f"Merged output was:\n{merged}"
    )


def test_ac011_merge_adds_no_structural_headings_beyond_provenance(
    two_workers_with_duplicates: list[WorkerResult],
) -> None:
    """The only level-2 headings the merge step is permitted to emit
    are the per-worker provenance headers (``## From {label} ({ms}ms)``).
    Any extra ``## `` heading would represent a cross-worker synthesis
    section -- explicitly disallowed by AC-011 and the merge.py
    docstring."""
    merged = mechanical_merge(two_workers_with_duplicates)
    h2_count = merged.count("\n## ") + (1 if merged.startswith("## ") else 0)
    assert h2_count == 2, (
        "merge must emit exactly one '## ' heading per worker section "
        f"(2 total for 2 workers); got {h2_count}.\n\n"
        f"Merged output was:\n{merged}"
    )
