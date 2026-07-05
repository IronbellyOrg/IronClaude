"""T04.14 -- AC-011 no-scoring/dedup/reorder boundary test (R-098 / D-0080).

Pins the AC-011 neutrality boundary: every recipe in :data:`REGISTRY`
preserves all findings verbatim. No scoring, dedup, reordering, or
filtering transforms are applied. The boundary is enforced by feeding
each recipe a fixture with N findings (including a deliberate duplicate
and a known order via embedded sentinel tokens) and asserting the
output retains exactly N rows, in body order, with duplicates intact.

Coverage matrix
===============

All 6 REGISTRY recipes are exercised:

* ``bare-review-v1``      -- findings table (``| F-NN | ... |``).
* ``findings_table_v1``   -- findings table (4-col input -> 5-col output).
* ``hypothesis_table_v1`` -- hypothesis table (``| H-NN | ... |``).
* ``verdict_only_v1``     -- supporting Gaps / Concerns rows preserved
                             inside the ``## Notes`` section.
* ``passthrough``         -- byte-identity (raw body unchanged).
* ``custom``              -- dispatcher slot; exercised via
                             :func:`load_custom_py` with a fixture
                             recipe so dynamically-loaded recipes are
                             bound by the same neutrality boundary.

Per recipe the boundary is asserted along three axes:

* **Count** -- N findings in -> N findings out. Asserted via row-ID
  enumeration (``F-NN`` / ``H-NN``), frontmatter counts
  (``finding_count`` / ``hypothesis_count``), or substring presence.
* **Order** -- output emits findings in the same order as the body.
  Sentinel tokens (``TOKEN-A`` through ``TOKEN-D``) appear in a known
  sequence in the fixture; the test asserts the rendered output
  contains them at strictly-increasing offsets.
* **Duplicates** -- identical input rows are NOT collapsed; the
  duplicate row is retained verbatim (``TOKEN-A`` deliberately appears
  twice in each fixture, at positions 1 and N).

Grep co-check (T04.14 validation)
---------------------------------

``grep -RnE "sort|dedup|score|filter" src/superclaude/cli/swarm/recipes/``
is the manual reviewer's spot check; current matches are all docstring
/ comment occurrences that *document* the AC-011 contract rather than
*violate* it. The behavioural assertions below are the load-bearing
gate -- a regression that introduces real judging logic (a ``.sort``,
``set(...)``, or threshold filter) would show up as a failing count,
order, or duplicate test in this file.

FR-012 alignment
----------------

The same neutrality boundary applies to the M5 merge module; this
suite is the recipe-side gate. Tests should remain shape-stable so
that an analogous merge-side suite (separate task) can mirror the
fixture pattern.
"""

from __future__ import annotations

import sys
import types
from typing import Any

import pytest

from superclaude.cli.swarm.recipes import (
    CUSTOM_PY_PREFIX,
    REGISTRY,
    NormalizedResult,
    Recipe,
    load_custom_py,
)
from superclaude.cli.swarm.recipes.bare_review_v1 import BareReviewV1
from superclaude.cli.swarm.recipes.findings_table_v1 import FindingsTableV1
from superclaude.cli.swarm.recipes.hypothesis_table_v1 import HypothesisTableV1
from superclaude.cli.swarm.recipes.passthrough import Passthrough
from superclaude.cli.swarm.recipes.verdict_only_v1 import VerdictOnlyV1

FIXED_GENERATED = "2026-06-01T11:19:39Z"
FIXED_CHECKSUM = "deadbeefcafe"
FIXED_TARGET = "/tmp/example/target.py"


# ---------------------------------------------------------------------------
# Shared helpers
# ---------------------------------------------------------------------------


# Sentinel tokens used to verify ordering. TOKEN-A is the deliberate
# duplicate; TOKEN-B / TOKEN-C / TOKEN-D mark the middle rows; TOKEN-A
# is repeated at the tail so the duplicate-preservation assertion can
# look for *two* TOKEN-A occurrences in the rendered output.
TOKENS_IN_ORDER: tuple[str, ...] = (
    "TOKEN-A",
    "TOKEN-B",
    "TOKEN-C",
    "TOKEN-D",
    "TOKEN-A",
)
EXPECTED_ROW_COUNT: int = len(TOKENS_IN_ORDER)
EXPECTED_DUPLICATE_TOKEN: str = "TOKEN-A"
EXPECTED_DUPLICATE_OCCURRENCES: int = 2


def _benign_args(
    *,
    status: str = "success",
    lens: str = "refactor-find",
    tier: str = "T2-code",
    suspect: bool = False,
) -> dict[str, Any]:
    return {
        "status": status,
        "target": FIXED_TARGET,
        "target_checksum": FIXED_CHECKSUM,
        "target_truncated": False,
        "model_id": "m",
        "model_label": "M",
        "caller_label": "",
        "elapsed_ms": 12345,
        "generated": FIXED_GENERATED,
        "lens": lens,
        "tier": tier,
        "suspect": suspect,
    }


def _assert_tokens_in_order(text: str, tokens: tuple[str, ...]) -> None:
    """Each token appears at a strictly-increasing offset in ``text``.

    Order-preservation is asserted by scanning forward through the
    rendered output: ``find(token, cursor)`` starting at the previous
    match's end. If any token is missing, or any pair is out of order,
    the assertion fails with a diagnostic that names the offending
    pair so a recipe regression that reorders rows is easy to debug.
    """
    cursor = 0
    for i, token in enumerate(tokens):
        idx = text.find(token, cursor)
        assert idx != -1, (
            f"token {token!r} (position {i}) missing from rendered output "
            f"after cursor {cursor}; tokens already located: "
            f"{list(tokens[:i])}\n--- output ---\n{text}"
        )
        cursor = idx + len(token)


def _assert_duplicate_preserved(
    text: str,
    token: str = EXPECTED_DUPLICATE_TOKEN,
    occurrences: int = EXPECTED_DUPLICATE_OCCURRENCES,
) -> None:
    """The duplicate token appears at least ``occurrences`` times."""
    actual = text.count(token)
    assert actual >= occurrences, (
        f"duplicate token {token!r} appears {actual} times in rendered "
        f"output; AC-011 requires duplicate rows to be preserved "
        f"(expected >= {occurrences}).\n--- output ---\n{text}"
    )


# ---------------------------------------------------------------------------
# Fixture bodies (per-recipe inputs with N rows + a deliberate duplicate)
# ---------------------------------------------------------------------------


def _bare_review_body() -> str:
    """5-row findings table in bare-review-v1 shape with a duplicate."""
    return (
        "---\n"
        "schema_version: 1.0\n"
        "---\n"
        "\n"
        "## Findings\n"
        "\n"
        "| ID | Sev | Claim | Cite | SelfConf |\n"
        "|----|-----|-------|------|----------|\n"
        "| F-01 | high | TOKEN-A first claim | foo.py:1 | 50 |\n"
        "| F-02 | high | TOKEN-B second claim | foo.py:2 | 60 |\n"
        "| F-03 | high | TOKEN-C third claim | foo.py:3 | 70 |\n"
        "| F-04 | high | TOKEN-D fourth claim | foo.py:4 | 80 |\n"
        "| F-05 | high | TOKEN-A first claim | foo.py:1 | 50 |\n"
        "\n"
        "## Verdict\n"
        "Verdict text.\n"
    )


def _findings_table_body() -> str:
    """5-row findings_table_v1 input (4-col cleanup table) with a duplicate."""
    return (
        "## Cleanups\n"
        "\n"
        "| File:line | Cleanup | Rationale | Patch sketch |\n"
        "|-----------|---------|-----------|---------------|\n"
        "| foo.py:1 | TOKEN-A first cleanup | rationale 1 | patch 1 |\n"
        "| foo.py:2 | TOKEN-B second cleanup | rationale 2 | patch 2 |\n"
        "| foo.py:3 | TOKEN-C third cleanup | rationale 3 | patch 3 |\n"
        "| foo.py:4 | TOKEN-D fourth cleanup | rationale 4 | patch 4 |\n"
        "| foo.py:1 | TOKEN-A first cleanup | rationale 1 | patch 1 |\n"
        "\n"
        "## Notes\n"
        "Five rows including a deliberate duplicate at the tail.\n"
    )


def _hypothesis_table_body() -> str:
    """5-row hypothesis_table_v1 input (5-col table) with a duplicate."""
    return (
        "## Hypotheses\n"
        "\n"
        "| Cause | Supporting | Falsifying | Confidence | Next probe |\n"
        "|-------|------------|------------|------------|------------|\n"
        "| TOKEN-A first cause | s1 | f1 | 70 | n1 |\n"
        "| TOKEN-B second cause | s2 | f2 | 60 | n2 |\n"
        "| TOKEN-C third cause | s3 | f3 | 50 | n3 |\n"
        "| TOKEN-D fourth cause | s4 | f4 | 40 | n4 |\n"
        "| TOKEN-A first cause | s1 | f1 | 70 | n1 |\n"
        "\n"
        "## Notes\n"
        "Five hypotheses including a deliberate duplicate at the tail.\n"
    )


def _verdict_only_body() -> str:
    """Verdict + 5-row supporting Gaps table with a duplicate row.

    verdict_only_v1 doesn't render a Findings table -- it folds Gaps /
    Concerns sections into the ``## Notes`` section verbatim. The
    AC-011 check here is therefore: every token from the supporting
    table reaches the notes block in order, and the duplicate row is
    preserved (TOKEN-A appears twice).
    """
    return (
        "## Verdict\n"
        "no -- substantive gaps remain.\n"
        "\n"
        "## Gaps\n"
        "\n"
        "- TOKEN-A first gap matters\n"
        "- TOKEN-B second gap matters\n"
        "- TOKEN-C third gap matters\n"
        "- TOKEN-D fourth gap matters\n"
        "- TOKEN-A first gap matters\n"
    )


# ---------------------------------------------------------------------------
# 1 -- bare-review-v1 boundary
# ---------------------------------------------------------------------------


class TestBareReviewV1Boundary:
    """``bare-review-v1`` preserves all findings -- AC-011 axis tests."""

    def test_all_five_findings_present_in_output(self):
        result = BareReviewV1().normalize(_bare_review_body(), _benign_args())
        assert result.error is None
        # The recipe auto-assigns F-01..F-NN, so all 5 input rows render.
        for i in range(1, EXPECTED_ROW_COUNT + 1):
            assert f"| F-{i:02d} |" in result.text, (
                f"row F-{i:02d} missing from bare-review-v1 output -- "
                "recipe filtered a finding (AC-011 violation)\n"
                f"--- output ---\n{result.text}"
            )
        # No phantom F-06; recipe did not duplicate / add rows.
        assert f"| F-{EXPECTED_ROW_COUNT + 1:02d} |" not in result.text

    def test_findings_emitted_in_body_order(self):
        result = BareReviewV1().normalize(_bare_review_body(), _benign_args())
        _assert_tokens_in_order(result.text, TOKENS_IN_ORDER)

    def test_duplicate_finding_retained(self):
        result = BareReviewV1().normalize(_bare_review_body(), _benign_args())
        _assert_duplicate_preserved(result.text)

    def test_finding_count_frontmatter_matches_input_count(self):
        result = BareReviewV1().normalize(_bare_review_body(), _benign_args())
        assert f"finding_count: {EXPECTED_ROW_COUNT}" in result.text


# ---------------------------------------------------------------------------
# 2 -- findings_table_v1 boundary
# ---------------------------------------------------------------------------


class TestFindingsTableV1Boundary:
    """``findings_table_v1`` preserves all findings -- AC-011 axis tests."""

    def test_all_five_findings_present_in_output(self):
        result = FindingsTableV1().normalize(_findings_table_body(), _benign_args())
        assert result.error is None
        for i in range(1, EXPECTED_ROW_COUNT + 1):
            assert f"| F-{i:02d} |" in result.text, (
                f"row F-{i:02d} missing from findings_table_v1 output -- "
                "recipe filtered a finding (AC-011 violation)\n"
                f"--- output ---\n{result.text}"
            )
        assert f"| F-{EXPECTED_ROW_COUNT + 1:02d} |" not in result.text

    def test_findings_emitted_in_body_order(self):
        result = FindingsTableV1().normalize(_findings_table_body(), _benign_args())
        _assert_tokens_in_order(result.text, TOKENS_IN_ORDER)

    def test_duplicate_finding_retained(self):
        result = FindingsTableV1().normalize(_findings_table_body(), _benign_args())
        _assert_duplicate_preserved(result.text)

    def test_finding_count_frontmatter_matches_input_count(self):
        result = FindingsTableV1().normalize(_findings_table_body(), _benign_args())
        assert f"finding_count: {EXPECTED_ROW_COUNT}" in result.text


# ---------------------------------------------------------------------------
# 3 -- hypothesis_table_v1 boundary
# ---------------------------------------------------------------------------


class TestHypothesisTableV1Boundary:
    """``hypothesis_table_v1`` preserves all hypotheses -- AC-011 axis tests."""

    def _args(self) -> dict[str, Any]:
        return _benign_args(lens="troubleshoot-hypothesis", tier="T2-tshoot")

    def test_all_five_hypotheses_present_in_output(self):
        result = HypothesisTableV1().normalize(_hypothesis_table_body(), self._args())
        assert result.error is None
        for i in range(1, EXPECTED_ROW_COUNT + 1):
            assert f"| H-{i:02d} |" in result.text, (
                f"row H-{i:02d} missing from hypothesis_table_v1 output -- "
                "recipe filtered a hypothesis (AC-011 violation)\n"
                f"--- output ---\n{result.text}"
            )
        assert f"| H-{EXPECTED_ROW_COUNT + 1:02d} |" not in result.text

    def test_hypotheses_emitted_in_body_order(self):
        result = HypothesisTableV1().normalize(_hypothesis_table_body(), self._args())
        _assert_tokens_in_order(result.text, TOKENS_IN_ORDER)

    def test_duplicate_hypothesis_retained(self):
        result = HypothesisTableV1().normalize(_hypothesis_table_body(), self._args())
        _assert_duplicate_preserved(result.text)

    def test_hypothesis_count_frontmatter_matches_input_count(self):
        result = HypothesisTableV1().normalize(_hypothesis_table_body(), self._args())
        assert f"hypothesis_count: {EXPECTED_ROW_COUNT}" in result.text


# ---------------------------------------------------------------------------
# 4 -- verdict_only_v1 boundary
# ---------------------------------------------------------------------------


class TestVerdictOnlyV1Boundary:
    """``verdict_only_v1`` preserves supporting rows -- AC-011 axis tests.

    The recipe does not render a Findings table -- the verdict label
    is reformatted (alias-mapped) and the supporting Gaps / Concerns
    content is folded into the ``## Notes`` section verbatim. The
    AC-011 check is therefore: every supporting token reaches the
    notes block in order, and the duplicate row is preserved.
    """

    def _args(self) -> dict[str, Any]:
        return _benign_args(lens="spec-completeness", tier="T2-spec")

    def test_all_supporting_tokens_present_in_output(self):
        result = VerdictOnlyV1().normalize(_verdict_only_body(), self._args())
        assert result.error is None
        # Each unique token reaches the rendered output.
        for token in {"TOKEN-A", "TOKEN-B", "TOKEN-C", "TOKEN-D"}:
            assert token in result.text, (
                f"supporting token {token!r} missing from verdict_only_v1 "
                f"output -- recipe dropped a supporting row (AC-011 "
                f"violation)\n--- output ---\n{result.text}"
            )

    def test_supporting_tokens_emitted_in_body_order(self):
        result = VerdictOnlyV1().normalize(_verdict_only_body(), self._args())
        _assert_tokens_in_order(result.text, TOKENS_IN_ORDER)

    def test_duplicate_supporting_row_retained(self):
        result = VerdictOnlyV1().normalize(_verdict_only_body(), self._args())
        _assert_duplicate_preserved(result.text)


# ---------------------------------------------------------------------------
# 5 -- passthrough boundary
# ---------------------------------------------------------------------------


class TestPassthroughBoundary:
    """``passthrough`` is the strongest AC-011 case: byte-identity."""

    def test_findings_table_returned_byte_identical(self):
        body = _findings_table_body()
        result = Passthrough().normalize(body, _benign_args())
        assert result.text == body, (
            "passthrough mutated the body -- AC-011 / raw-mode contract "
            "requires byte identity"
        )

    def test_findings_emitted_in_body_order(self):
        result = Passthrough().normalize(_findings_table_body(), _benign_args())
        _assert_tokens_in_order(result.text, TOKENS_IN_ORDER)

    def test_duplicate_finding_retained(self):
        result = Passthrough().normalize(_findings_table_body(), _benign_args())
        _assert_duplicate_preserved(result.text)


# ---------------------------------------------------------------------------
# 6 -- custom-py dispatcher boundary
# ---------------------------------------------------------------------------


class TestCustomPyDispatcherBoundary:
    """Custom-py-loaded recipes are bound by the same AC-011 contract.

    The ``custom`` REGISTRY slot is a routing dispatcher; the real
    recipe is materialized via :func:`load_custom_py`. The boundary
    test here registers a fixture recipe that simply echoes the body
    (the AC-011 minimum -- preserve everything) and asserts the
    loader-resolved recipe upholds count / order / duplicate
    preservation.

    A custom recipe that violates AC-011 (e.g. by sorting rows or
    de-duplicating) would be flagged by the recipe's own author-side
    tests; this suite verifies only that the dispatcher slot does not
    silently strip rows on the way into / out of the loader, and that
    a Recipe-Protocol-conforming fixture round-trips findings intact.
    """

    def test_dispatcher_slot_does_not_call_loader_unprompted(self):
        """Calling REGISTRY['custom'] directly must raise loudly.

        The dispatcher slot is a routing hint, not a usable recipe;
        invoking ``.normalize`` directly raises :class:`RuntimeError`
        rather than silently passing-through or returning an empty
        body. A silent passthrough would mask the AC-011 boundary by
        making it look like the loader handled the call.
        """
        entry = REGISTRY["custom"]
        assert isinstance(entry, Recipe)
        with pytest.raises(RuntimeError):
            entry.normalize(_findings_table_body(), _benign_args())

    def test_loaded_fixture_recipe_preserves_findings(self, monkeypatch):
        module_name = "superclaude_test_t04_14_no_judging_fixture"
        module = types.ModuleType(module_name)

        class FixtureRecipe:
            """Echoes the body verbatim -- the AC-011 minimum."""

            def normalize(
                self, raw_output: str, args: dict[str, Any]
            ) -> NormalizedResult:
                del args
                return NormalizedResult(text=raw_output, salvaged=False, error=None)

        module.FixtureRecipe = FixtureRecipe  # type: ignore[attr-defined]
        monkeypatch.setitem(sys.modules, module_name, module)

        recipe = load_custom_py(f"{CUSTOM_PY_PREFIX}{module_name}:FixtureRecipe")
        assert isinstance(recipe, Recipe)

        body = _findings_table_body()
        result = recipe.normalize(body, _benign_args())
        assert result.text == body
        _assert_tokens_in_order(result.text, TOKENS_IN_ORDER)
        _assert_duplicate_preserved(result.text)


# ---------------------------------------------------------------------------
# 7 -- REGISTRY coverage guard
# ---------------------------------------------------------------------------


# Per-recipe-name (recipe instance, body builder). Each non-custom slot
# wires straight to the per-class fixture body; ``custom`` is covered by
# :class:`TestCustomPyDispatcherBoundary` above and excluded here so the
# parametrize loop does not invoke the dispatcher directly (which raises
# by design -- see ``test_dispatcher_slot_does_not_call_loader_unprompted``).
_BOUNDARY_RECIPES: tuple[tuple[str, Recipe, str], ...] = (
    ("bare-review-v1", REGISTRY["bare-review-v1"], _bare_review_body()),
    ("findings_table_v1", REGISTRY["findings_table_v1"], _findings_table_body()),
    (
        "hypothesis_table_v1",
        REGISTRY["hypothesis_table_v1"],
        _hypothesis_table_body(),
    ),
    ("verdict_only_v1", REGISTRY["verdict_only_v1"], _verdict_only_body()),
    ("passthrough", REGISTRY["passthrough"], _findings_table_body()),
)


@pytest.mark.parametrize(
    "name,recipe,body",
    _BOUNDARY_RECIPES,
    ids=[entry[0] for entry in _BOUNDARY_RECIPES],
)
def test_all_non_dispatcher_recipes_preserve_token_order(
    name: str, recipe: Recipe, body: str
):
    """Cross-recipe sanity: every non-dispatcher REGISTRY entry passes
    the order axis on its dedicated fixture body.

    The per-class TestXxxBoundary suites above pin count / order /
    duplicate preservation per recipe with bespoke fixtures. This
    parametrized check is the REGISTRY-level coverage guard: if a
    contributor adds a new non-dispatcher slot and forgets to thread it
    into the boundary tests, the parametrize tuple will be missing the
    entry and a missing-recipe-name assertion below catches it.
    """
    args = _benign_args(
        lens=(
            "troubleshoot-hypothesis"
            if name == "hypothesis_table_v1"
            else ("spec-completeness" if name == "verdict_only_v1" else "refactor-find")
        ),
        tier=(
            "T2-tshoot"
            if name == "hypothesis_table_v1"
            else ("T2-spec" if name == "verdict_only_v1" else "T2-code")
        ),
    )
    result = recipe.normalize(body, args)
    assert isinstance(result, NormalizedResult)
    _assert_tokens_in_order(result.text, TOKENS_IN_ORDER)
    _assert_duplicate_preserved(result.text)


def test_boundary_matrix_covers_all_non_dispatcher_registry_slots():
    """REGISTRY enumeration vs the parametrize tuple stay in sync.

    Coverage guard: if a contributor adds a 7th non-dispatcher recipe,
    this assertion fails until they extend ``_BOUNDARY_RECIPES`` above.
    The ``custom`` dispatcher slot is the only exclusion (its boundary
    is exercised via :class:`TestCustomPyDispatcherBoundary`).
    """
    covered = {name for name, _recipe, _body in _BOUNDARY_RECIPES}
    expected = set(REGISTRY) - {"custom"}
    assert covered == expected, (
        f"AC-011 boundary matrix out of sync with REGISTRY:\n"
        f"  covered : {sorted(covered)}\n"
        f"  expected: {sorted(expected)}\n"
        f"Add the missing slot to _BOUNDARY_RECIPES at the bottom of "
        f"tests/swarm/test_recipe_no_judging.py."
    )
