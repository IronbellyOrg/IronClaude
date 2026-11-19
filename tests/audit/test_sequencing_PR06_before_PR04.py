# ruff: noqa: N999  # intentional: filename encodes PR06-before-PR04 sequencing-inversion mitigation for R-108 / INV-010 cross-reference
"""TEST-024 — K-007 sequencing-inversion mitigation (R-108 / INV-010 / T05.15).

Phase-5 / T05.15 deliverable (D-0066). Proves the K-007 mitigation
documented at SKILL.md §A.10.5 step 8 (the *auto-richening invariant*
at L1280, citing roadmap R-069): if PR-04 (FR-CONV.3 dynamic
enumeration + verdict passthrough) lands in `src/` BEFORE PR-06
(FR-CONV.1 TB-Add-1..8 catalogue in `rf-qa.md`), the dynamic
enumeration mechanism MUST degrade gracefully (`LIVE_TB_ADD = []`)
and then MUST auto-richen — with **zero edits to SKILL.md** — the
moment the catalogue activates (PR-06 lands later).

The fixture simulates the inversion by mutating only a temp working
copy of `rf-qa.md`:

  * `inverted` scenario — `#### Structural Gate Additions` block
    removed entirely. Simulates "PR-04 already in tree, PR-06 not
    yet landed". Expected: `extract_catalogue() == []`, INV-010
    log line emits `size=0 ids=[]`, no orphan / no missing-row
    FAILs are *applicable* (consumer table is also empty in this
    scenario, see §3 below).

  * `activated` scenario — the canonical `rf-qa.md` byte-for-byte
    (catalogue present at TB-Add-1..K, K = MIN_LIVE_K). Simulates
    "PR-06 has now landed". Expected: `extract_catalogue()` returns
    the full canonical list, INV-010 log line emits `size=K`, and
    every canonical TB-Add-N from the inverted-→activated diff
    appears as an added row.

The fixture is **independent** of `_halt_emitter.py` (the M5 halt
runtime). TEST-024 is purely a structural fixture that exercises
the INV-010 catalogue-lookup pure helpers ported from
`test_dynamic_enumeration_inv_010.py` (TEST-010 / D-0038) — the
upstream sequencing-inversion guard. The reuse is deliberate: if
TEST-024 stayed green while TEST-010 (the auto-richen-on-growth
fixture) regressed, the K-007 mitigation would still be claimed but
the underlying mechanism would be broken. By sharing the same helper
surface, a regression to either side breaks both fixtures.

Acceptance reference (phase-5-tasklist.md L720-724):
- ``uv run pytest tests/audit/test_sequencing_PR06_before_PR04.py -v`` exits 0.
- Structural assertion confirms enriched checklist when catalogue activates.
- K-007 mitigation verified.
- Evidence at ``TASKLIST_ROOT/artifacts/D-0066/evidence.md``.

Source-text guards lock the SKILL.md K-007 mitigation prose
(``§A.10.5 step 8 / L1280``) against silent drift.

Run: ``uv run pytest tests/audit/test_sequencing_PR06_before_PR04.py -v``
"""

from __future__ import annotations

import hashlib
import re
from pathlib import Path
from typing import List

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]

RF_QA_SRC = REPO_ROOT / "src" / "superclaude" / "agents" / "rf-qa.md"
RF_QA_MIRROR = REPO_ROOT / ".claude" / "agents" / "rf-qa.md"
SKILL_SRC = REPO_ROOT / "src" / "superclaude" / "skills" / "task-builder" / "SKILL.md"

# Bounded-region heading the orchestrator MUST search for (SKILL.md
# §A.10.5 step 2). Identical to TEST-010's helper.
STRUCTURAL_GATE_HEADING = "#### Structural Gate Additions"

# SKILL.md §A.10.5 step 3 regex (Python `re`, MULTILINE) — identical
# to TEST-010 / D-0038.
TB_ADD_ID_RE = re.compile(r"^[0-9]+\. \*\*TB-Add-([0-9]+):", re.MULTILINE)

# INV-010 step 7 log-line shape (SKILL.md L1279). When the catalogue
# is absent, `size=0` and `ids=[]` (empty literal). When present,
# `size>=MIN_LIVE_K` and `ids=[TB-Add-1,...,TB-Add-K]`.
INV010_LOG_PRESENT_RE = re.compile(
    r"^INV-010: enumerated TB-Add-\* catalogue size=(\d+) "
    r"ids=\[(TB-Add-\d+(?:,TB-Add-\d+)*)\] "
    r"source=rf-qa\.md source_sha256=([0-9a-f]{16})$"
)
INV010_LOG_EMPTY_RE = re.compile(
    r"^INV-010: enumerated TB-Add-\* catalogue size=0 "
    r"ids=\[\] "
    r"source=rf-qa\.md source_sha256=([0-9a-f]{16})$"
)

# Minimum K floor for the *activated* scenario. The M1 PR-06 contract-freeze
# (TB-Add-1..8 per CP-P01-END) was SUPERSEDED by 804eb4f4, which intentionally
# removed TB-Add-2 (item-count bounds, incompatible with 100-250+ item task
# files). TB-Add IDs are stable, leaving a permanent gap (live: 1, 3-8 = 7).
# A drop below 7 signals catalogue regression.
MIN_LIVE_K = 7


# ---------------------------------------------------------------------------
# Pure helpers — Python ports of D-0031 fixture-enum.sh, identical to
# TEST-010's surface so a regression in either side breaks both.
# ---------------------------------------------------------------------------


def _bounded_region(text: str) -> str:
    """Return the slice of ``text`` from ``#### Structural Gate
    Additions`` through (exclusive of) the next ``####``/``###``/``## ``
    heading. Mirrors SKILL.md §A.10.5 step 2.

    Returns the empty string when the heading is absent — the K-007
    "PR-04 before PR-06" inverted-sequencing case.
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

    When the bounded region is absent (inverted-sequencing scenario),
    returns an empty list — the documented K-007 degraded state.
    """
    span = _bounded_region(text)
    ns = sorted({int(m.group(1)) for m in TB_ADD_ID_RE.finditer(span)})
    return [f"TB-Add-{n}" for n in ns]


def render_block(catalogue: List[str]) -> str:
    """Render the spawn-prompt verdict-block enumeration view.

    Identical to TEST-010's helper so the structural diff is
    directly comparable across the two fixtures.
    """
    rows = ["## Inherited Structural Verdict (enumeration view)"]
    for tb_id in catalogue:
        rows.append(f"| {tb_id} | (status carried verbatim from producer) |")
    return "\n".join(rows) + "\n"


def emit_inv010_log(catalogue: List[str], source_path: Path) -> str:
    """Emit the SKILL.md §A.10.5 step 7 structured log line for the
    given catalogue + source file (sha256 first 16 hex chars).

    Identical to TEST-010's helper; produces ``ids=[]`` literal when
    the catalogue is empty (the K-007 inverted-sequencing case).
    """
    size = len(catalogue)
    ids_csv = ",".join(catalogue)
    sha16 = hashlib.sha256(source_path.read_bytes()).hexdigest()[:16]
    return (
        f"INV-010: enumerated TB-Add-* catalogue size={size} "
        f"ids=[{ids_csv}] source=rf-qa.md source_sha256={sha16}"
    )


def _strip_catalogue_block(text: str) -> str:
    """Remove the ``#### Structural Gate Additions`` bounded region
    from ``text`` — simulating "PR-04 already merged into the snapshot
    of `src/`, but PR-06 not yet". Everything else (the preceding A.10
    text, the trailing sections, the H-Check counterparts, etc.) is
    preserved byte-for-byte so the only difference between the inverted
    and activated scenarios is the catalogue's presence.

    Returns the modified text. The canonical source is never touched —
    the call sites operate only on temp / in-memory copies.
    """
    lines = text.splitlines(keepends=False)
    out: List[str] = []
    in_block = False
    found = False
    for line in lines:
        if not in_block and line.startswith(STRUCTURAL_GATE_HEADING):
            in_block = True
            found = True
            continue
        if in_block and (
            line.startswith("####") or line.startswith("### ") or line.startswith("## ")
        ):
            in_block = False
            out.append(line)
            continue
        if in_block:
            continue
        out.append(line)
    # Preserve trailing newline if the original had one.
    trailing_newline = "\n" if text.endswith("\n") else ""
    assert found, (
        "fixture invariant violated: canonical rf-qa.md does NOT contain "
        f"{STRUCTURAL_GATE_HEADING!r} — the inverted-sequencing simulation "
        "cannot proceed without a known starting point"
    )
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


@pytest.fixture(scope="module")
def skill_canonical_pre_sha() -> str:
    return hashlib.sha256(SKILL_SRC.read_bytes()).hexdigest()


@pytest.fixture
def sequencing_scenario(tmp_path: Path, rf_qa_canonical_text: str):
    """Run the K-007 sequencing-inversion scenario and return per-state
    artefacts for the assertion classes below.

    Two states are constructed in `tmp_path` (the canonical on-disk
    `rf-qa.md` and SKILL.md are never touched):

    - ``inverted`` — `rf-qa.md` with the Structural Gate Additions
      block REMOVED. Models "PR-04 already in tree, PR-06 not yet".
    - ``activated`` — `rf-qa.md` byte-for-byte canonical. Models
      "PR-06 has now landed."
    """
    inverted_text = _strip_catalogue_block(rf_qa_canonical_text)
    activated_text = rf_qa_canonical_text

    inverted_path = tmp_path / "rf-qa.inverted.md"
    activated_path = tmp_path / "rf-qa.activated.md"
    inverted_path.write_text(inverted_text, encoding="utf-8")
    activated_path.write_text(activated_text, encoding="utf-8")

    cat_inverted = extract_catalogue(inverted_text)
    cat_activated = extract_catalogue(activated_text)

    log_inverted = emit_inv010_log(cat_inverted, inverted_path)
    log_activated = emit_inv010_log(cat_activated, activated_path)

    block_inverted = render_block(cat_inverted)
    block_activated = render_block(cat_activated)

    return {
        "inverted_text": inverted_text,
        "activated_text": activated_text,
        "inverted_path": inverted_path,
        "activated_path": activated_path,
        "cat_inverted": cat_inverted,
        "cat_activated": cat_activated,
        "log_inverted": log_inverted,
        "log_activated": log_activated,
        "block_inverted": block_inverted,
        "block_activated": block_activated,
        "k_inverted": len(cat_inverted),
        "k_activated": len(cat_activated),
    }


# ---------------------------------------------------------------------------
# Static schema / source guards — the K-007 mitigation prose stays put.
# ---------------------------------------------------------------------------


class TestK007MitigationDocumented:
    """Pre-flight: the SKILL.md §A.10.5 step 8 *auto-richening
    invariant* — the documented K-007 mitigation — exists and names
    R-069 explicitly. If this regresses, the fixture has nothing to
    verify; assert presence before exercising the helpers.
    """

    def test_rf_qa_src_exists(self):
        assert RF_QA_SRC.is_file(), f"missing source rf-qa.md at {RF_QA_SRC}"

    def test_rf_qa_mirror_exists(self):
        assert RF_QA_MIRROR.is_file(), f"missing mirror rf-qa.md at {RF_QA_MIRROR}"

    def test_skill_src_exists(self):
        assert SKILL_SRC.is_file(), f"missing source SKILL.md at {SKILL_SRC}"

    def test_skill_names_k_007_explicitly(self):
        skill_text = SKILL_SRC.read_text(encoding="utf-8")
        assert "K-007" in skill_text, (
            "SKILL.md no longer references K-007 — the mitigation prose "
            "for the PR-04 / PR-06 sequencing inversion has regressed"
        )

    def test_skill_names_r_069_explicitly(self):
        skill_text = SKILL_SRC.read_text(encoding="utf-8")
        assert "R-069" in skill_text, (
            "SKILL.md no longer references R-069 — the auto-richening "
            "invariant has lost its roadmap pointer"
        )

    def test_skill_auto_richening_invariant_present(self):
        skill_text = SKILL_SRC.read_text(encoding="utf-8")
        assert "Auto-richening invariant" in skill_text, (
            "SKILL.md no longer contains the 'Auto-richening invariant' "
            "header — the K-007 mitigation step 8 has been deleted/renamed"
        )

    def test_skill_zero_edits_clause_present(self):
        """The mitigation explicitly forbids SKILL.md edits when the
        catalogue grows — the 'zero edits to this SKILL.md' clause
        is the load-bearing wording. A reword would invalidate the
        K-007 mitigation; lock it via grep.
        """
        skill_text = SKILL_SRC.read_text(encoding="utf-8")
        assert "zero edits" in skill_text, (
            "SKILL.md no longer contains the 'zero edits' clause — the "
            "K-007 mitigation has been weakened. The invariant requires "
            "that catalogue activation in rf-qa.md triggers auto-richening "
            "WITHOUT any SKILL.md edits."
        )

    def test_skill_inv_010_label_present(self):
        skill_text = SKILL_SRC.read_text(encoding="utf-8")
        assert "INV-010" in skill_text, (
            "SKILL.md no longer references INV-010 — the dynamic catalogue "
            "lookup mechanism that mitigates K-007 has been deleted"
        )

    def test_rf_qa_src_and_mirror_byte_identical(self):
        src_bytes = RF_QA_SRC.read_bytes()
        mirror_bytes = RF_QA_MIRROR.read_bytes()
        assert src_bytes == mirror_bytes, (
            "rf-qa.md source and `.claude/` mirror diverged — run "
            "`make sync-dev` before continuing"
        )


# ---------------------------------------------------------------------------
# Inverted-state behaviour: PR-04 landed, PR-06 not yet — catalogue empty.
# ---------------------------------------------------------------------------


class TestInvertedSequencingEmptyCatalogue:
    """The 'PR-04 lands first' state. The dynamic enumeration MUST
    return an empty list with no exception, no orchestrator crash,
    and no FAIL emission — degraded but not broken. This is the
    K-007 degradation path; the activation path is exercised below.
    """

    def test_inverted_text_lacks_catalogue_heading(self, sequencing_scenario):
        assert STRUCTURAL_GATE_HEADING not in sequencing_scenario["inverted_text"], (
            "fixture setup violation: inverted-state rf-qa.md still "
            "contains the catalogue heading; _strip_catalogue_block "
            "did not remove the bounded region"
        )

    def test_inverted_extract_catalogue_is_empty(self, sequencing_scenario):
        cat = sequencing_scenario["cat_inverted"]
        assert cat == [], (
            "K-007 inverted-state extract_catalogue() returned non-empty "
            f"list {cat} — the dynamic enumeration is leaking entries "
            "even when the bounded region is absent"
        )

    def test_inverted_log_line_matches_empty_shape(self, sequencing_scenario):
        m = INV010_LOG_EMPTY_RE.match(sequencing_scenario["log_inverted"])
        assert m, (
            "INV-010 log line malformed in inverted state: "
            f"{sequencing_scenario['log_inverted']!r} — expected "
            "size=0 ids=[] (empty literal)"
        )

    def test_inverted_block_renders_header_only(self, sequencing_scenario):
        """The verdict-block enumeration view contains only the header
        line when the catalogue is empty — no orphan TB-Add rows leak
        through. This is the consumer-visible degraded state.
        """
        block = sequencing_scenario["block_inverted"]
        assert block.startswith(
            "## Inherited Structural Verdict (enumeration view)\n"
        ), f"inverted block missing header: {block!r}"
        # Only one line of content (the header) + trailing newline.
        non_empty = [ln for ln in block.splitlines() if ln.strip()]
        assert len(non_empty) == 1, (
            f"inverted-state verdict-block contains orphan TB-Add rows: {non_empty}"
        )

    def test_inverted_no_tb_add_tokens_anywhere_in_log_or_block(
        self, sequencing_scenario
    ):
        """Belt-and-braces: no `TB-Add-N` token should appear ANYWHERE
        in either the log line or the rendered block when the catalogue
        is absent. Catches the regression where the enumeration falls
        back to a hard-coded default list.
        """
        log = sequencing_scenario["log_inverted"]
        block = sequencing_scenario["block_inverted"]
        log_tokens = re.findall(r"TB-Add-\d+", log)
        block_tokens = re.findall(r"TB-Add-\d+", block)
        assert log_tokens == [], (
            f"K-007 leak: inverted-state log line contains TB-Add tokens "
            f"{log_tokens} — enumeration fell back to a hard-coded list"
        )
        assert block_tokens == [], (
            f"K-007 leak: inverted-state block view contains TB-Add tokens "
            f"{block_tokens} — enumeration fell back to a hard-coded list"
        )


# ---------------------------------------------------------------------------
# Activated-state behaviour: PR-06 lands later — catalogue auto-richens.
# ---------------------------------------------------------------------------


class TestCatalogueActivationAutoRichens:
    """Core K-007 mitigation assertion: once PR-06 lands (the
    canonical rf-qa.md state), the dynamic enumeration auto-richens
    to the full catalogue WITHOUT any SKILL.md edits.

    The activated scenario uses the canonical rf-qa.md byte-for-byte;
    the inverted scenario differs only by the absence of the bounded
    region. The delta between the two is the *isolated* effect of
    PR-06 landing.
    """

    def test_activated_extract_catalogue_meets_min_floor(self, sequencing_scenario):
        k = sequencing_scenario["k_activated"]
        assert k >= MIN_LIVE_K, (
            f"activated K={k} below MIN_LIVE_K={MIN_LIVE_K}. Either the "
            "canonical catalogue shrank or extract_catalogue() drifted "
            "from SKILL.md §A.10.5 steps 2-4"
        )

    def test_activated_extract_catalogue_is_well_formed(self, sequencing_scenario):
        """IDs are unique and strictly ascending. Contiguity is NOT required:
        TB-Add-2's intentional removal (804eb4f4) leaves a permanent stable-ID
        gap (live catalogue: 1, 3-8); the runtime enumeration mechanism
        (dedupe + sort-by-N) is contiguity-agnostic. Asserts the real
        invariant (no duplicates, sorted), not the superseded [1..K] form."""
        cat = sequencing_scenario["cat_activated"]
        ns = [int(s.split("-")[-1]) for s in cat]
        assert ns == sorted(set(ns)), (
            f"activated catalogue has duplicate or unsorted TB-Add-N IDs: {cat}"
        )

    def test_activated_log_line_matches_present_shape(self, sequencing_scenario):
        m = INV010_LOG_PRESENT_RE.match(sequencing_scenario["log_activated"])
        assert m, (
            "INV-010 log line malformed in activated state: "
            f"{sequencing_scenario['log_activated']!r}"
        )
        size = int(m.group(1))
        assert size == sequencing_scenario["k_activated"], (
            f"INV-010 log size={size} disagrees with extracted "
            f"K_activated={sequencing_scenario['k_activated']}"
        )

    def test_activation_grew_catalogue_by_exactly_k(self, sequencing_scenario):
        """The delta between inverted and activated states is exactly K
        new TB-Add entries (the full canonical catalogue). The inverted
        state was empty; the activated state is the full catalogue.
        """
        delta = sequencing_scenario["k_activated"] - sequencing_scenario["k_inverted"]
        assert delta == sequencing_scenario["k_activated"], (
            f"K-007 mitigation broken: activation delta={delta} != "
            f"K_activated={sequencing_scenario['k_activated']}. The "
            "inverted state must be the empty set so the activation "
            "delta == the full catalogue"
        )

    def test_structural_diff_surfaces_every_canonical_tb_add(self, sequencing_scenario):
        """The unified diff between the inverted (header-only) and
        activated (full catalogue) verdict-block enumeration views
        surfaces every canonical TB-Add-N as an added line, with zero
        removed lines and zero other changes. This is the AC-2 row
        ("structural assertion confirms enriched checklist when
        catalogue activates") from phase-5-tasklist.md L722.
        """
        block_inverted = sequencing_scenario["block_inverted"].splitlines(keepends=True)
        block_activated = sequencing_scenario["block_activated"].splitlines(
            keepends=True
        )
        import difflib

        diff = list(
            difflib.unified_diff(
                block_inverted,
                block_activated,
                fromfile="inverted",
                tofile="activated",
                n=0,
            )
        )
        added = [ln for ln in diff if ln.startswith("+") and not ln.startswith("+++")]
        removed = [ln for ln in diff if ln.startswith("-") and not ln.startswith("---")]
        assert len(removed) == 0, (
            f"K-007 AC-2 violated: expected 0 removed lines in diff, got "
            f"{len(removed)} ({removed}) — catalogue activation should be "
            "strictly additive"
        )
        assert len(added) == sequencing_scenario["k_activated"], (
            f"K-007 AC-2 violated: expected exactly "
            f"{sequencing_scenario['k_activated']} added lines, got "
            f"{len(added)}. Diff: {added}"
        )
        # Every added line references a distinct TB-Add-N from the
        # activated catalogue, in order.
        for line, tb_id in zip(added, sequencing_scenario["cat_activated"]):
            assert tb_id in line, (
                f"K-007 AC-2 ordering/labeling violated: expected added line "
                f"to reference {tb_id}, got {line!r}"
            )


# ---------------------------------------------------------------------------
# SKILL.md byte-stability under catalogue activation.
# ---------------------------------------------------------------------------


class TestSkillByteIdenticalAcrossActivation:
    """The K-007 mitigation's load-bearing claim: catalogue activation
    in rf-qa.md MUST require ZERO edits to SKILL.md. Verify this
    directly by hashing SKILL.md before any helper runs and after both
    inverted + activated state assembly — the hash MUST be identical.
    """

    def test_skill_bytes_unchanged_after_inverted_run(
        self, sequencing_scenario, skill_canonical_pre_sha: str
    ):
        # sequencing_scenario already constructed the inverted state.
        post = hashlib.sha256(SKILL_SRC.read_bytes()).hexdigest()
        assert post == skill_canonical_pre_sha, (
            "K-007 mitigation broken: SKILL.md mutated during inverted-"
            f"state construction. pre={skill_canonical_pre_sha[:16]} "
            f"post={post[:16]}"
        )

    def test_skill_bytes_unchanged_after_activated_run(
        self, sequencing_scenario, skill_canonical_pre_sha: str
    ):
        # sequencing_scenario also constructed the activated state.
        post = hashlib.sha256(SKILL_SRC.read_bytes()).hexdigest()
        assert post == skill_canonical_pre_sha, (
            "K-007 mitigation broken: SKILL.md mutated during activated-"
            f"state construction. pre={skill_canonical_pre_sha[:16]} "
            f"post={post[:16]}"
        )

    def test_skill_bytes_unchanged_at_module_exit(self, skill_canonical_pre_sha: str):
        """Final guard — independent of any fixture. The canonical
        SKILL.md surface MUST be untouched by the entire test module.
        """
        post = hashlib.sha256(SKILL_SRC.read_bytes()).hexdigest()
        assert post == skill_canonical_pre_sha, (
            "K-007 mitigation broken: SKILL.md mutated by the TEST-024 "
            f"module. pre={skill_canonical_pre_sha[:16]} "
            f"post={post[:16]}"
        )


# ---------------------------------------------------------------------------
# Canonical rf-qa.md byte-stability — only the temp copies were mutated.
# ---------------------------------------------------------------------------


class TestCanonicalRfQaUntouched:
    """The fixture mutates only `tmp_path` copies of rf-qa.md. The
    canonical on-disk source + `.claude/` mirror MUST be byte-identical
    pre/post the test module. Mirrors TEST-010's `TestCanonicalFileUntouched`.
    """

    def test_canonical_rf_qa_byte_identical_post_fixture(
        self, sequencing_scenario, rf_qa_canonical_pre_sha: str
    ):
        post_sha = hashlib.sha256(RF_QA_SRC.read_bytes()).hexdigest()
        assert post_sha == rf_qa_canonical_pre_sha, (
            "fixture mutated canonical rf-qa.md: "
            f"pre={rf_qa_canonical_pre_sha[:16]} post={post_sha[:16]}"
        )

    def test_mirror_rf_qa_byte_identical_post_fixture(self, sequencing_scenario):
        src = RF_QA_SRC.read_bytes()
        mirror = RF_QA_MIRROR.read_bytes()
        assert src == mirror, (
            "rf-qa.md source/mirror diverged during fixture run — "
            "the sequencing-inversion test must operate via tempdir only"
        )


# ---------------------------------------------------------------------------
# Helper determinism — pure-function guarantees over identical input.
# ---------------------------------------------------------------------------


class TestHelperDeterminism:
    """Belt-and-braces: the helpers are pure functions of source
    content. Two extractions over identical bytes return equal lists.
    A drift here would render the K-007 sequencing claims unverifiable
    (the "before vs after activation" comparison would be noisy).
    """

    def test_extract_catalogue_pure_on_canonical(self, rf_qa_canonical_text: str):
        a = extract_catalogue(rf_qa_canonical_text)
        b = extract_catalogue(rf_qa_canonical_text)
        assert a == b, (
            f"extract_catalogue() is not deterministic on canonical "
            f"rf-qa.md: a={a}, b={b}"
        )

    def test_extract_catalogue_pure_on_stripped(self, rf_qa_canonical_text: str):
        stripped = _strip_catalogue_block(rf_qa_canonical_text)
        a = extract_catalogue(stripped)
        b = extract_catalogue(stripped)
        assert a == b == [], (
            f"extract_catalogue() is not deterministic on stripped "
            f"rf-qa.md: a={a}, b={b}; both should be []"
        )

    def test_strip_then_strip_is_idempotent(self, rf_qa_canonical_text: str):
        """Stripping a text that has already been stripped MUST raise
        — the helper's assertion guards against silent double-stripping
        being misread as a successful inverted state.
        """
        once = _strip_catalogue_block(rf_qa_canonical_text)
        with pytest.raises(AssertionError):
            _strip_catalogue_block(once)


# ---------------------------------------------------------------------------
# Cross-fixture consistency with TEST-010 (the auto-richen-on-growth side).
# ---------------------------------------------------------------------------


class TestCrossFixtureConsistencyWithTest010:
    """TEST-010 (`test_dynamic_enumeration_inv_010.py`) covers the
    growth-by-one path (canonical catalogue + synthetic TB-Add-(K+1)).
    TEST-024 covers the activation path (empty catalogue → canonical
    catalogue). The two fixtures share the same `extract_catalogue`
    semantics by design — any divergence between them indicates that
    the K-007 mitigation lives in only one of the two scenarios.

    Lock this by re-importing TEST-010's helpers and asserting they
    agree on the activated-state catalogue.
    """

    def test_test010_and_test024_helpers_agree_on_activated_state(
        self, sequencing_scenario, rf_qa_canonical_text: str
    ):
        from tests.audit.test_dynamic_enumeration_inv_010 import (
            extract_catalogue as test010_extract,
        )

        ours = sequencing_scenario["cat_activated"]
        theirs = test010_extract(rf_qa_canonical_text)
        assert ours == theirs, (
            "TEST-010 and TEST-024 extract_catalogue() helpers disagree on "
            f"the canonical rf-qa.md: TEST-024={ours}, TEST-010={theirs}. "
            "The two K-007-adjacent fixtures must share the same lookup "
            "semantics, else the mitigation's coverage is split."
        )

    def test_test010_helper_agrees_on_inverted_state(self, sequencing_scenario):
        from tests.audit.test_dynamic_enumeration_inv_010 import (
            extract_catalogue as test010_extract,
        )

        theirs = test010_extract(sequencing_scenario["inverted_text"])
        assert theirs == [], (
            "TEST-010 helper returned non-empty list on inverted-state "
            f"rf-qa.md ({theirs}) — the absent-catalogue degradation is "
            "not consistent across the two K-007-adjacent fixtures"
        )
