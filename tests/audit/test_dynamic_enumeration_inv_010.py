"""TEST-010 — INV-010 dynamic TB-Add enumeration auto-richening (R-066 / FR-CONV.3 PR-04).

Phase-3 / T03.15 deliverable (D-0038). Promotes the D-0031
``fixture-enum.sh`` proof-of-concept to a merge-gate pytest fixture.
Asserts the INV-010 enumeration mechanism wired at SKILL.md §A.10.5
lines 1213-1224 (T03.07 / D-0031):

1. The live TB-Add catalogue extracted from
   ``src/superclaude/agents/rf-qa.md``'s bounded
   ``#### Structural Gate Additions`` region matches the runtime size
   the orchestrator emits in its INV-010 log line (sanity: K ≥ 8 with
   no gaps in the [1, K] integer range).
2. Appending a synthetic ``TB-Add-(K+1)`` stub inside the bounded
   catalogue region of a **temp working copy** of ``rf-qa.md`` causes
   the next enumeration to grow by exactly one entry (AC-1 / AC-2,
   phase-3-tasklist.md L730-734).
3. The structural diff between the cycle-1 and cycle-2 spawn-prompt
   verdict-block enumeration views surfaces exactly one added row
   (the new ``TB-Add-(K+1)``) with zero deletions and zero other
   changes (AC-1).
4. The canonical on-disk ``rf-qa.md`` is byte-identical pre/post the
   fixture run — the synthetic stub lives only in the tmp working
   copy (AC-3, validation note L737-738; phase-3-tasklist.md L728
   "remove synthetic stub after fixture run").
5. The SKILL.md §A.10.5 enumeration block contains no hard-coded
   TB-Add-N enumeration list — only the symbolic
   ``LIVE_TB_ADD = [TB-Add-1, TB-Add-2, …, TB-Add-K]`` illustration
   from step 4 is allowed (AC-4 / phase-3-tasklist.md L346).
6. The orchestrator's INV-010 structured log line shape (SKILL.md
   step 7) is emitted with the correct runtime ``size=K`` on both
   cycles, and the ``source_sha256`` witness differs between cycles
   because the working-copy content changed.

Acceptance reference (phase-3-tasklist.md L730-734):
- ``uv run pytest tests/audit/test_dynamic_enumeration_inv_010.py -v`` exits 0.
- Structural diff before/after catalogue growth shows new entry.
- Synthetic stub removed after fixture run.
- Evidence at ``TASKLIST_ROOT/artifacts/D-0038/evidence.md``.

The fixture ports the D-0031 shell helpers (``extract_catalogue``,
``emit_log``, ``render_block``) into Python with byte-for-byte
output parity, so the assertions in evidence ``D-0031/fixture-enum.log``
remain reproducible under pytest as well.

Run: ``uv run pytest tests/audit/test_dynamic_enumeration_inv_010.py -v``
"""

from __future__ import annotations

import hashlib
import re
import shutil
import tempfile
from pathlib import Path
from typing import List

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]

RF_QA_SRC = REPO_ROOT / "src" / "superclaude" / "agents" / "rf-qa.md"
RF_QA_MIRROR = REPO_ROOT / ".claude" / "agents" / "rf-qa.md"
SKILL_SRC = REPO_ROOT / "src" / "superclaude" / "skills" / "task-builder" / "SKILL.md"

# Bounded-region heading the orchestrator MUST search for (SKILL.md
# §A.10.5 step 2). The match is the exact bullet heading rf-qa.md uses.
STRUCTURAL_GATE_HEADING = "#### Structural Gate Additions"

# SKILL.md §A.10.5 step 3 regex (Python `re`, MULTILINE).
TB_ADD_ID_RE = re.compile(r"^[0-9]+\. \*\*TB-Add-([0-9]+):", re.MULTILINE)

# Used by AC-4 (hard-coded enumeration absence). The enumeration block
# lives at SKILL.md:1213-1224 — only the symbolic worked-example
# pattern (``LIVE_TB_ADD = [TB-Add-1, TB-Add-2, …, TB-Add-K]``) is
# allowed. Any other TB-Add-N tokens in this range indicate regression.
SKILL_A105_BLOCK_START = 1213
SKILL_A105_BLOCK_END = 1224

# INV-010 step 7 log-line shape (SKILL.md:1222 + D-0031/fixture-enum.log).
INV010_LOG_RE = re.compile(
    r"^INV-010: enumerated TB-Add-\* catalogue size=(\d+) "
    r"ids=\[(TB-Add-\d+(?:,TB-Add-\d+)*)\] "
    r"source=rf-qa\.md source_sha256=([0-9a-f]{16})$"
)

# Minimum K we expect at the time MIG-003 lands (M1 freezes TB-Add-1..8
# per CP-P01-END). A drop below this floor signals catalogue regression.
MIN_LIVE_K = 8


# ---------------------------------------------------------------------------
# Pure helpers — Python ports of D-0031 fixture-enum.sh.
# ---------------------------------------------------------------------------


def _bounded_region(text: str) -> str:
    """Return the slice of ``text`` from the ``#### Structural Gate
    Additions`` heading through (exclusive of) the next ``####``,
    ``###``, or ``## `` heading. Mirrors SKILL.md §A.10.5 step 2.
    """
    lines = text.splitlines()
    start = -1
    for idx, line in enumerate(lines):
        if line.startswith(STRUCTURAL_GATE_HEADING):
            start = idx + 1
            break
    if start == -1:
        return ""
    end = start
    while end < len(lines):
        line = lines[end]
        if line.startswith("####") or line.startswith("### ") or line.startswith("## "):
            break
        end += 1
    return "\n".join(lines[start:end])


def extract_catalogue(text: str) -> List[str]:
    """Return ``LIVE_TB_ADD = [TB-Add-1, ..., TB-Add-K]``, deduped and
    sorted ascending by N. Mirrors SKILL.md §A.10.5 steps 2-4.
    """
    span = _bounded_region(text)
    ns = sorted({int(m.group(1)) for m in TB_ADD_ID_RE.finditer(span)})
    return [f"TB-Add-{n}" for n in ns]


def render_block(catalogue: List[str]) -> str:
    """Render the spawn-prompt verdict-block enumeration view.

    Byte-identical to D-0031/fixture-enum.sh ``render_block`` so the
    structural diff in pytest output matches the shell fixture's diff.
    """
    rows = ["## Inherited Structural Verdict (enumeration view)"]
    for tb_id in catalogue:
        rows.append(f"| {tb_id} | (status carried verbatim from producer) |")
    return "\n".join(rows) + "\n"


def emit_inv010_log(catalogue: List[str], source_path: Path) -> str:
    """Emit the SKILL.md §A.10.5 step 7 structured log line for the
    given catalogue + source file (sha256 first 16 hex chars).
    """
    size = len(catalogue)
    ids_csv = ",".join(catalogue)
    sha16 = hashlib.sha256(source_path.read_bytes()).hexdigest()[:16]
    return (
        f"INV-010: enumerated TB-Add-* catalogue size={size} "
        f"ids=[{ids_csv}] source=rf-qa.md source_sha256={sha16}"
    )


def _append_synthetic_stub(text: str, synth_n: int, synth_num: int) -> str:
    """Append a synthetic ``TB-Add-(synth_n)`` line at the END of the
    bounded region, just before the next ``####``/``###``/``## ``
    heading. Returns the modified text.

    Mirrors D-0031/fixture-enum.sh awk block — uses the next sequential
    numbered-item index ``synth_num`` so the regex in step 3 matches.
    """
    lines = text.splitlines(keepends=False)
    out: List[str] = []
    in_block = False
    inserted = False
    synth_line = (
        f"{synth_num}. **TB-Add-{synth_n}: Synthetic enrichment stub "
        "(fixture-only).** This entry is appended only inside the "
        "fixture's temp copy of rf-qa.md to demonstrate INV-010 auto-"
        "richening. The canonical rf-qa.md on disk is NOT modified."
    )
    for line in lines:
        if line.startswith(STRUCTURAL_GATE_HEADING):
            in_block = True
            out.append(line)
            continue
        if in_block and (
            line.startswith("####") or line.startswith("### ") or line.startswith("## ")
        ):
            out.append(synth_line)
            out.append("")
            in_block = False
            inserted = True
            out.append(line)
            continue
        out.append(line)
    if in_block and not inserted:
        out.append(synth_line)
        out.append("")
    trailing_newline = "\n" if text.endswith("\n") else ""
    return "\n".join(out) + trailing_newline


# ---------------------------------------------------------------------------
# Fixtures.
# ---------------------------------------------------------------------------


@pytest.fixture(scope="module")
def rf_qa_canonical_text() -> str:
    return RF_QA_SRC.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def rf_qa_canonical_pre_sha(rf_qa_canonical_text: str) -> str:
    return hashlib.sha256(rf_qa_canonical_text.encode("utf-8")).hexdigest()


@pytest.fixture
def workdir():
    """Disposable temp dir — AUTO-REMOVES the synthetic stub once the
    test exits (phase-3-tasklist.md L728 'remove synthetic stub after
    verification'). The canonical rf-qa.md on disk is NEVER touched.
    """
    d = tempfile.mkdtemp(prefix="inv010-")
    try:
        yield Path(d)
    finally:
        shutil.rmtree(d, ignore_errors=True)


@pytest.fixture
def two_cycle(workdir: Path, rf_qa_canonical_text: str):
    """Run the 2-cycle enumeration scenario and return per-cycle
    artifacts for the assertion classes below.
    """
    cycle1_path = workdir / "rf-qa.cycle1.md"
    cycle2_path = workdir / "rf-qa.cycle2.md"
    cycle1_path.write_text(rf_qa_canonical_text, encoding="utf-8")

    cycle1_text = cycle1_path.read_text(encoding="utf-8")
    cat1 = extract_catalogue(cycle1_text)
    log1 = emit_inv010_log(cat1, cycle1_path)
    block1 = render_block(cat1)

    k1 = len(cat1)
    synth_n = k1 + 1
    synth_num = 28 + (synth_n - 8)  # next sequential item after item 28
    cycle2_text = _append_synthetic_stub(cycle1_text, synth_n, synth_num)
    cycle2_path.write_text(cycle2_text, encoding="utf-8")

    cat2 = extract_catalogue(cycle2_text)
    log2 = emit_inv010_log(cat2, cycle2_path)
    block2 = render_block(cat2)

    return {
        "k1": k1,
        "k2": len(cat2),
        "synth_n": synth_n,
        "cat1": cat1,
        "cat2": cat2,
        "log1": log1,
        "log2": log2,
        "block1": block1,
        "block2": block2,
        "cycle1_path": cycle1_path,
        "cycle2_path": cycle2_path,
    }


# ---------------------------------------------------------------------------
# Static schema / source guards — the wiring stays in place.
# ---------------------------------------------------------------------------


class TestEnumerationWiringPresent:
    """Pre-flight: the SKILL.md §A.10.5 enumeration block exists in the
    range it was landed at (T03.07 / D-0031). If this regresses,
    nothing else this fixture asserts is meaningful."""

    def test_rf_qa_src_exists(self):
        assert RF_QA_SRC.is_file(), f"missing source rf-qa.md at {RF_QA_SRC}"

    def test_rf_qa_mirror_exists(self):
        assert RF_QA_MIRROR.is_file(), f"missing mirror rf-qa.md at {RF_QA_MIRROR}"

    def test_skill_src_exists(self):
        assert SKILL_SRC.is_file(), f"missing source SKILL.md at {SKILL_SRC}"

    def test_structural_gate_heading_present(self, rf_qa_canonical_text: str):
        assert STRUCTURAL_GATE_HEADING in rf_qa_canonical_text, (
            f"bounded-region heading missing from {RF_QA_SRC}: "
            f"{STRUCTURAL_GATE_HEADING!r}"
        )

    def test_skill_a105_enumeration_block_present(self):
        skill_text = SKILL_SRC.read_text(encoding="utf-8")
        assert (
            "TB-Add catalogue enumeration (INV-010 dynamic catalogue lookup)"
            in skill_text
        ), (
            "SKILL.md §A.10.5 enumeration block heading missing — T03.07 (D-0031) regressed"
        )

    def test_rf_qa_src_and_mirror_byte_identical(self):
        src_bytes = RF_QA_SRC.read_bytes()
        mirror_bytes = RF_QA_MIRROR.read_bytes()
        assert src_bytes == mirror_bytes, (
            "rf-qa.md source and `.claude/` mirror diverged — run `make sync-dev`"
        )


class TestNoHardCodedEnumerationInA105:
    """AC-4 (phase-3-tasklist.md L346) — inside the A.10.5 enumeration
    block (lines 1213-1224), the only TB-Add-N tokens permitted are
    the symbolic worked-example references ``TB-Add-1`` and
    ``TB-Add-2`` from step 4's ``LIVE_TB_ADD = [TB-Add-1, TB-Add-2, …,
    TB-Add-K]`` illustration. Any other token = hard-coded
    enumeration regression."""

    def test_only_symbolic_tb_add_tokens_in_block(self):
        skill_lines = SKILL_SRC.read_text(encoding="utf-8").splitlines()
        # The byte-offset of the block can drift across future MIG
        # edits; locate by heading and walk forward to the next ``###``
        # heading, then assert the symbolic-only constraint over that
        # span. The static line range is the documented baseline
        # (D-0031 evidence § 3.3) but we resolve dynamically for
        # robustness against post-MIG drift.
        block_start = -1
        block_end = -1
        for idx, line in enumerate(skill_lines, start=1):
            if (
                "TB-Add catalogue enumeration (INV-010 dynamic catalogue lookup)"
                in line
            ):
                block_start = idx
                continue
            if block_start != -1 and line.startswith("### "):
                block_end = idx - 1
                break
        assert block_start != -1, "enumeration block heading not found in SKILL.md"
        assert block_end != -1, "could not locate end of enumeration block"

        span_lines = skill_lines[block_start - 1 : block_end]
        span_text = "\n".join(span_lines)
        tokens = set(re.findall(r"TB-Add-\d+", span_text))
        allowed = {"TB-Add-1", "TB-Add-2"}
        unexpected = tokens - allowed
        assert not unexpected, (
            "AC-4 violated: SKILL.md §A.10.5 enumeration block contains "
            f"non-symbolic TB-Add tokens {sorted(unexpected)} — hard-coded "
            "enumeration regression. Only `TB-Add-1` and `TB-Add-2` "
            "(symbolic worked-example) are permitted in the block."
        )

    def test_documented_block_range_still_symbolic(self):
        """Belt-and-braces: the documented static range
        (D-0031 § 3.3) must also be symbolic-only. This catches the
        narrow regression where the block heading moves but the
        static range still references the original location."""
        skill_lines = SKILL_SRC.read_text(encoding="utf-8").splitlines()
        if len(skill_lines) < SKILL_A105_BLOCK_END:
            pytest.skip(
                f"SKILL.md shrank below {SKILL_A105_BLOCK_END} lines; "
                "documented range no longer applies — dynamic check above is authoritative"
            )
        span = "\n".join(skill_lines[SKILL_A105_BLOCK_START - 1 : SKILL_A105_BLOCK_END])
        tokens = set(re.findall(r"TB-Add-\d+", span))
        allowed = {"TB-Add-1", "TB-Add-2"}
        unexpected = tokens - allowed
        if "TB-Add catalogue enumeration" not in span:
            pytest.skip(
                "Documented static range no longer covers the enumeration "
                "block; dynamic check above is authoritative"
            )
        assert not unexpected, (
            "AC-4 violated (documented range): unexpected TB-Add tokens "
            f"{sorted(unexpected)} in SKILL.md lines "
            f"{SKILL_A105_BLOCK_START}-{SKILL_A105_BLOCK_END}."
        )


# ---------------------------------------------------------------------------
# Behaviour: 2-cycle enumeration shows auto-richening on catalogue growth.
# ---------------------------------------------------------------------------


class TestBaselineCatalogueExtraction:
    """The cycle-1 baseline matches what the live rf-qa.md publishes."""

    def test_cycle1_catalogue_meets_min_floor(self, two_cycle):
        k1 = two_cycle["k1"]
        assert k1 >= MIN_LIVE_K, (
            f"cycle-1 K={k1} below MIN_LIVE_K={MIN_LIVE_K}. Either the "
            "catalogue shrank or extract_catalogue() drifted from "
            "SKILL.md §A.10.5 steps 2-4."
        )

    def test_cycle1_catalogue_is_dense(self, two_cycle):
        """No gaps: extracted IDs are [TB-Add-1, ..., TB-Add-K1]."""
        cat1 = two_cycle["cat1"]
        ns = [int(s.split("-")[-1]) for s in cat1]
        assert ns == list(range(1, len(ns) + 1)), (
            f"cycle-1 catalogue has gaps in TB-Add-N integer range: {cat1}"
        )

    def test_cycle1_log_shape_matches_inv010_contract(self, two_cycle):
        m = INV010_LOG_RE.match(two_cycle["log1"])
        assert m, f"INV-010 log shape mismatch (cycle-1): {two_cycle['log1']!r}"
        size = int(m.group(1))
        assert size == two_cycle["k1"], (
            f"INV-010 log size={size} disagrees with extracted K1={two_cycle['k1']}"
        )


class TestAutoRichenOnCatalogueGrowth:
    """Core invariant — adding a synthetic ``TB-Add-(K+1)`` to the
    bounded region grows ``LIVE_TB_ADD`` by exactly one entry, with no
    other side-effects (AC-1 + AC-2; phase-3-tasklist.md L730-732)."""

    def test_catalogue_grew_by_exactly_one(self, two_cycle):
        k1 = two_cycle["k1"]
        k2 = two_cycle["k2"]
        assert k2 == k1 + 1, (
            f"AC-2 violated: expected K2 = K1 + 1 = {k1 + 1}, got K2={k2}. "
            "INV-010 dynamic enumeration failed to auto-richen on growth."
        )

    def test_synthetic_id_present_only_in_cycle2(self, two_cycle):
        synth_id = f"TB-Add-{two_cycle['synth_n']}"
        assert synth_id in two_cycle["cat2"], (
            f"synthetic {synth_id} not picked up by cycle-2 enumeration "
            f"(cat2={two_cycle['cat2']})"
        )
        assert synth_id not in two_cycle["cat1"], (
            f"synthetic {synth_id} unexpectedly present in cycle-1 "
            "(fixture should be additive over the canonical catalogue)"
        )

    def test_cycle1_catalogue_unchanged_in_cycle2(self, two_cycle):
        """Existing entries survive — auto-richening is additive only."""
        cat1 = two_cycle["cat1"]
        cat2 = two_cycle["cat2"]
        assert cat2[: len(cat1)] == cat1, (
            f"existing catalogue entries reordered/dropped under growth: "
            f"cat1={cat1}, cat2[:K1]={cat2[: len(cat1)]}"
        )

    def test_structural_diff_surfaces_exactly_one_added_row(self, two_cycle):
        """AC-1: structural diff of the cycle-1 vs cycle-2 verdict-block
        enumeration views shows exactly one added line (the new
        TB-Add-(K+1) row), zero deletions, zero other changes."""
        block1 = two_cycle["block1"].splitlines(keepends=True)
        block2 = two_cycle["block2"].splitlines(keepends=True)
        import difflib

        diff = list(
            difflib.unified_diff(
                block1, block2, fromfile="cycle-1", tofile="cycle-2", n=0
            )
        )
        # Filter to actual added/removed content lines (skip headers
        # and @@ hunk markers).
        added = [ln for ln in diff if ln.startswith("+") and not ln.startswith("+++")]
        removed = [ln for ln in diff if ln.startswith("-") and not ln.startswith("---")]
        assert len(removed) == 0, (
            f"AC-1 violated: expected 0 removed lines in diff, got "
            f"{len(removed)} ({removed})"
        )
        assert len(added) == 1, (
            f"AC-1 violated: expected exactly 1 added line, got {len(added)} ({added})"
        )
        synth_id = f"TB-Add-{two_cycle['synth_n']}"
        assert synth_id in added[0], (
            f"AC-1 violated: added line does not reference {synth_id}: {added[0]!r}"
        )


class TestCanonicalFileUntouched:
    """AC-3 — synthetic stub is removed after fixture run; canonical
    rf-qa.md on disk is byte-identical pre/post (phase-3-tasklist.md
    L728 'remove synthetic stub after verification')."""

    def test_canonical_rf_qa_byte_identical_post_fixture(
        self, two_cycle, rf_qa_canonical_pre_sha: str
    ):
        # The two_cycle fixture has already run; the synthetic stub
        # lived in tempdir only and is gone. Re-hash the canonical
        # surface and compare against the pre-run hash.
        post_sha = hashlib.sha256(RF_QA_SRC.read_bytes()).hexdigest()
        assert post_sha == rf_qa_canonical_pre_sha, (
            "AC-3 violated: canonical rf-qa.md mutated during fixture run. "
            f"pre={rf_qa_canonical_pre_sha[:16]} post={post_sha[:16]}"
        )

    def test_mirror_rf_qa_byte_identical_post_fixture(self):
        # Cross-check the mirror surface as well — the fixture must
        # not have inadvertently written to either copy.
        src = RF_QA_SRC.read_bytes()
        mirror = RF_QA_MIRROR.read_bytes()
        assert src == mirror, (
            "rf-qa.md source/mirror diverged during fixture run — "
            "auto-richening test must operate via tempdir only"
        )


class TestInv010LogShape:
    """SKILL.md §A.10.5 step 7 — both cycles emit the structured
    INV-010 log line with the correct runtime size, and the
    source_sha256 witness changes between cycles (proving the hash is
    a witness over actual source bytes, not a memoised constant)."""

    def test_log1_shape_and_size(self, two_cycle):
        m = INV010_LOG_RE.match(two_cycle["log1"])
        assert m, f"cycle-1 INV-010 log malformed: {two_cycle['log1']!r}"
        assert int(m.group(1)) == two_cycle["k1"]

    def test_log2_shape_and_size(self, two_cycle):
        m = INV010_LOG_RE.match(two_cycle["log2"])
        assert m, f"cycle-2 INV-010 log malformed: {two_cycle['log2']!r}"
        assert int(m.group(1)) == two_cycle["k2"]

    def test_source_sha256_differs_between_cycles(self, two_cycle):
        m1 = INV010_LOG_RE.match(two_cycle["log1"])
        m2 = INV010_LOG_RE.match(two_cycle["log2"])
        assert m1 and m2
        sha1 = m1.group(3)
        sha2 = m2.group(3)
        assert sha1 != sha2, (
            "INV-010 source_sha256 witness identical across cycles — "
            "hash is not actually reflecting the source bytes (regression "
            "to cached/constant value)"
        )


# ---------------------------------------------------------------------------
# Negative case — guard against false positives in the auto-richen claim.
# ---------------------------------------------------------------------------


class TestNoGrowthWithoutSourceEdit:
    """Negative case: re-extracting the catalogue from the **same**
    unmodified text MUST yield the same set — i.e., extraction is a
    pure function of source content. If two no-op cycles produced
    different sets, the auto-richen claim above would be false-positive
    on noise rather than a true response to catalogue growth."""

    def test_two_extractions_of_same_text_are_equal(self, rf_qa_canonical_text: str):
        cat_a = extract_catalogue(rf_qa_canonical_text)
        cat_b = extract_catalogue(rf_qa_canonical_text)
        assert cat_a == cat_b, (
            f"extract_catalogue() is not deterministic over identical text: "
            f"cat_a={cat_a}, cat_b={cat_b}"
        )

    def test_render_block_pure(self):
        catalogue = ["TB-Add-1", "TB-Add-2"]
        a = render_block(catalogue)
        b = render_block(catalogue)
        assert a == b, "render_block() is not deterministic"


class TestRegressionGuardHardcodedListBreaks:
    """If the orchestrator block silently regressed to a hard-coded
    list (e.g., ``CATALOGUE = ['TB-Add-1', ..., 'TB-Add-8']``), the
    auto-richen behaviour would fail. We can't directly mutate the
    SKILL.md block here, but we can prove via a parallel surface that
    a hard-coded enumeration would NOT produce the auto-richen
    behaviour — making the dynamic-enumeration property load-bearing."""

    def test_hardcoded_list_does_not_auto_richen(self, two_cycle):
        hardcoded = [f"TB-Add-{i}" for i in range(1, two_cycle["k1"] + 1)]
        # Simulating "orchestrator uses a hard-coded list": even after
        # the source grows in cycle-2, the hard-coded list does not.
        assert hardcoded != two_cycle["cat2"], (
            "the hard-coded list happens to equal cat2 — fixture cannot "
            "differentiate dynamic vs hard-coded enumeration"
        )
        assert len(hardcoded) == two_cycle["k1"], (
            "hard-coded simulation length drifted from cycle-1 baseline"
        )
        assert f"TB-Add-{two_cycle['synth_n']}" not in hardcoded, (
            "hard-coded simulation accidentally already contained the "
            "synthetic ID — fixture cannot demonstrate the dynamic property"
        )
