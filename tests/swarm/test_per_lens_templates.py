"""T04.13 -- per-lens output template tests (R-097 / COMP-035 / D-0079).

Covers three layers:

1. **Presence + path resolution**: each of the 6 non-custom bundled
   lenses has an ``output_template_path`` on its :class:`LensEntry`
   that points into ``src/superclaude/cli/swarm/lenses/templates/`` and
   resolves to an existing readable file (validator U-008
   :func:`_check_file_refs` contract, COMP-023). The templates
   directory MUST contain at least 6 ``*-output.md`` files.

2. **Recipe ↔ template alignment**: each template documents the
   canonical column header (for table-shape recipes) or section
   heading (for the verdict-only recipe) that the bound recipe's
   ``render_markdown`` emits. Plus the template explicitly names the
   recipe module it pairs with, so contributors editing the recipe
   know which template to update.

3. **Render-against-fixture**: feeding the lens's representative raw
   fixture through its bound recipe with deterministic args produces
   output whose markers (canonical table header / verdict section /
   frontmatter ``lens:`` field) are all present -- i.e. no
   "unbound vars" symptom.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest

from superclaude.cli.swarm.lenses import LENS_NAMES, get_lens
from superclaude.cli.swarm.recipes import REGISTRY


REPO_ROOT = Path(__file__).resolve().parents[2]
TEMPLATES_DIR = (
    REPO_ROOT
    / "src"
    / "superclaude"
    / "cli"
    / "swarm"
    / "lenses"
    / "templates"
)
FIXTURES_ROOT = Path(__file__).parent / "fixtures"


# The 6 non-custom lenses + their bound recipe + the canonical header
# (or section anchor) the rendered output emits. The alignment test
# greps each template for these markers.
LENS_TEMPLATE_SPECS: list[tuple[str, str, str, str, str]] = [
    # (lens_name, template_filename, recipe_name,
    #  canonical_marker_in_template, fixture_filename_under_recipe)
    (
        "refactor-find",
        "refactor-find-output.md",
        "findings_table_v1",
        "| ID | Locator | Finding | Detail | Action |",
        "refactor_find.raw.txt",
    ),
    (
        "edge-case-hunt",
        "edge-case-hunt-output.md",
        "findings_table_v1",
        "| ID | Locator | Finding | Detail | Action |",
        "edge_case_hunt.raw.txt",
    ),
    (
        "doc-completeness",
        "doc-completeness-output.md",
        "findings_table_v1",
        "| ID | Locator | Finding | Detail | Action |",
        "doc_completeness.raw.txt",
    ),
    (
        "troubleshoot-hypothesis",
        "troubleshoot-hypothesis-output.md",
        "hypothesis_table_v1",
        "| ID | Cause | Evidence | Confidence | Next Step |",
        "troubleshoot_hypothesis.raw.txt",
    ),
    (
        "spec-completeness",
        "spec-completeness-output.md",
        "verdict_only_v1",
        "## Verdict",
        "spec_completeness.raw.txt",
    ),
    (
        "feasibility-probe",
        "feasibility-probe-output.md",
        "verdict_only_v1",
        "## Verdict",
        "feasibility_probe.raw.txt",
    ),
]


# ---------------------------------------------------------------------------
# 1 -- Templates dir contains 6+ files; non-custom lens names are covered.
# ---------------------------------------------------------------------------


def test_templates_directory_has_six_or_more_files():
    """Validation: ``ls templates/ | wc -l`` reports >= 6 (task AC)."""
    assert TEMPLATES_DIR.is_dir(), (
        f"Templates dir missing: {TEMPLATES_DIR}"
    )
    template_files = sorted(TEMPLATES_DIR.glob("*-output.md"))
    assert len(template_files) >= 6, (
        f"Expected >= 6 *-output.md templates, found "
        f"{len(template_files)}: {[p.name for p in template_files]}"
    )


def test_six_non_custom_lenses_are_specified():
    """The 6 non-custom lenses (excluding bare-review which has its own
    skill-side template + custom which is escape-hatch) are all
    represented in :data:`LENS_TEMPLATE_SPECS`."""
    specced = {spec[0] for spec in LENS_TEMPLATE_SPECS}
    expected = set(LENS_NAMES) - {"bare-review", "custom"}
    assert specced == expected, (
        f"Specced lens set {specced} drifted from non-custom registry "
        f"{expected}"
    )


# ---------------------------------------------------------------------------
# 2 -- U-008 validator contract: every spec'd template path resolves.
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "lens_name,template_filename,recipe_name,marker,fixture_name",
    LENS_TEMPLATE_SPECS,
)
def test_template_path_resolves_for_each_lens(
    lens_name: str,
    template_filename: str,
    recipe_name: str,
    marker: str,
    fixture_name: str,
):
    """U-008 :func:`_check_file_refs` -- output_template_path is a
    non-empty string that resolves to a readable file under the
    canonical templates directory."""
    entry = get_lens(lens_name)
    assert entry.output_template_path, (
        f"Lens {lens_name!r}: output_template_path is empty"
    )
    template_path = Path(entry.output_template_path)
    assert template_path.is_file(), (
        f"Lens {lens_name!r}: template {template_path} does not resolve"
    )
    # Path pinned to the canonical templates dir.
    assert template_path.name == template_filename
    assert template_path.parent.resolve() == TEMPLATES_DIR.resolve()


# ---------------------------------------------------------------------------
# 3 -- Recipe <-> template alignment: every template names its recipe
#      module and documents the canonical column-header / section
#      anchor the recipe emits.
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "lens_name,template_filename,recipe_name,marker,fixture_name",
    LENS_TEMPLATE_SPECS,
)
def test_template_documents_bound_recipe(
    lens_name: str,
    template_filename: str,
    recipe_name: str,
    marker: str,
    fixture_name: str,
):
    """The template names its bound recipe module so contributors
    editing the recipe know which template to update."""
    entry = get_lens(lens_name)
    assert entry.recipe_name == recipe_name, (
        f"Lens {lens_name!r}: recipe_name {entry.recipe_name!r} "
        f"drifted from expected {recipe_name!r}"
    )
    body = (TEMPLATES_DIR / template_filename).read_text(encoding="utf-8")
    assert recipe_name in body, (
        f"Template {template_filename} does not name its bound recipe "
        f"{recipe_name!r}; alignment broken"
    )


@pytest.mark.parametrize(
    "lens_name,template_filename,recipe_name,marker,fixture_name",
    LENS_TEMPLATE_SPECS,
)
def test_template_documents_canonical_marker(
    lens_name: str,
    template_filename: str,
    recipe_name: str,
    marker: str,
    fixture_name: str,
):
    """The template documents the canonical column-header (for
    table-shape recipes) or section anchor (for verdict-only) that the
    bound recipe's ``render_markdown`` emits."""
    body = (TEMPLATES_DIR / template_filename).read_text(encoding="utf-8")
    assert marker in body, (
        f"Template {template_filename} missing canonical marker "
        f"{marker!r} -- recipe<->template alignment broken"
    )


# ---------------------------------------------------------------------------
# 4 -- Render against fixture: feeding each lens's raw fixture through
#      its bound recipe with deterministic args produces output that
#      contains the canonical marker and the lens label in the
#      frontmatter -- i.e. no "unbound vars" symptom.
# ---------------------------------------------------------------------------


FIXED_GENERATED = "2026-06-01T11:19:39Z"
FIXED_CHECKSUM = "deadbeefcafe"
FIXED_TARGET = "/tmp/example/target.md"


def _recipe_args(lens_name: str, tier: str) -> dict[str, Any]:
    return {
        "status": "success",
        "target": FIXED_TARGET,
        "target_checksum": FIXED_CHECKSUM,
        "target_truncated": False,
        "model_id": "m",
        "model_label": "M",
        "caller_label": "",
        "elapsed_ms": 12345,
        "generated": FIXED_GENERATED,
        "lens": lens_name,
        "tier": tier,
        "suspect": False,
    }


@pytest.mark.parametrize(
    "lens_name,template_filename,recipe_name,marker,fixture_name",
    LENS_TEMPLATE_SPECS,
)
def test_recipe_renders_template_marker_against_fixture(
    lens_name: str,
    template_filename: str,
    recipe_name: str,
    marker: str,
    fixture_name: str,
):
    """Recipe output rendered against the lens fixture contains the
    canonical marker the template documents AND the lens label in
    frontmatter."""
    fixture_path = FIXTURES_ROOT / recipe_name / fixture_name
    raw = fixture_path.read_text(encoding="utf-8")

    entry = get_lens(lens_name)
    recipe = REGISTRY.get(recipe_name)
    assert recipe is not None, (
        f"Recipe {recipe_name!r} missing from REGISTRY"
    )

    args = _recipe_args(lens_name, entry.tier)
    result = recipe.normalize(raw, args)

    assert result.error is None, (
        f"Lens {lens_name!r} fixture render errored: {result.error!r}"
    )
    text = result.text
    assert text, f"Lens {lens_name!r} produced empty render"
    # Canonical marker the template documents must appear in the
    # rendered output.
    assert marker in text, (
        f"Lens {lens_name!r} render missing canonical marker "
        f"{marker!r}; template documents a shape the recipe does not "
        f"emit"
    )
    # Frontmatter binds lens label -- proves the template's
    # ``lens: "..."`` slot is wired through the recipe's args.
    assert f'lens: "{lens_name}"' in text, (
        f"Lens {lens_name!r} render missing frontmatter "
        f"lens: \"{lens_name}\""
    )
