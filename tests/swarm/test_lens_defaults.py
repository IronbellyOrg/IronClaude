"""T02.04 -- FR-020 lens-driven defaults expansion tests.

Covers :func:`preflight.expand_lens_defaults` against the §4.2 mapping
(``merged-requirements.compressed.compressed.md`` L337-L353):

    - Empty / default JobSpec fields fall through to the lens entry.
    - Caller-supplied non-empty values win and are preserved verbatim.
    - Unknown lens raises :class:`PreflightError` with
      :data:`RULE_UNKNOWN_LENS`.
    - The returned :class:`ResolvedLensEntry` snapshot mirrors the
      LensEntry on all nine DM-011 fields (verbatim, including
      ``suspect`` / ``tier`` which flow through the snapshot rather
      than a JobSpec field).
"""

from __future__ import annotations

import pytest

from superclaude.cli.swarm.models import (
    JobSpec,
    LensEntry,
    ResolvedLensEntry,
)
from superclaude.cli.swarm.preflight import (
    CANONICAL_FILENAME_TEMPLATE,
    RULE_UNKNOWN_LENS,
    PreflightError,
    expand_lens_defaults,
)

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


def _bare_review_lens() -> LensEntry:
    """Mirror the T02.02 fixture so the expansion contract is checked end-to-end."""
    return LensEntry(
        name="bare-review",
        description="bare review skeleton",
        system_prompt_fragment="Review with care. <<<GUARD>>>",
        user_template="Review: {{target}}",
        output_template_path="/abs/path/to/template.j2",
        recipe_name="bare-review-v1",
        default_workers=3,
        default_target_line_cap=8000,
        suspect=True,
        tier="T2",
        recommended_next_command_template="sc:reflect on {job_id} {suspect_files}",
        acceptance_notes="",
        stability="stable",
    )


@pytest.fixture
def bare_review_registry() -> dict[str, LensEntry]:
    return {"bare-review": _bare_review_lens()}


def _minimal_jobspec() -> JobSpec:
    """JobSpec whose lens-relevant fields are at dataclass defaults.

    Used to exercise the "fall through to lens" branch on every §4.2
    mapping target. Caller fills the lens slot only; the rest is left
    at the empty / dataclass-default values that the expansion treats
    as "caller did not override".
    """
    return JobSpec(lens="bare-review")


# ---------------------------------------------------------------------------
# Happy path -- the ten §4.2 mappings
# ---------------------------------------------------------------------------


def test_expand_populates_prompt_block(bare_review_registry) -> None:
    spec = _minimal_jobspec()
    expand_lens_defaults(spec, bare_review_registry)
    lens = bare_review_registry["bare-review"]
    assert spec.prompt.system == lens.system_prompt_fragment
    assert spec.prompt.user_template == lens.user_template


def test_expand_populates_normalization_block(bare_review_registry) -> None:
    spec = _minimal_jobspec()
    expand_lens_defaults(spec, bare_review_registry)
    lens = bare_review_registry["bare-review"]
    assert spec.normalization.recipe == lens.recipe_name
    assert spec.normalization.template_path == lens.output_template_path


def test_expand_populates_workers_count(bare_review_registry) -> None:
    spec = _minimal_jobspec()
    # WorkerSpec default is 4 -- the expansion treats this as "fall through".
    assert spec.workers.count == 4
    expand_lens_defaults(spec, bare_review_registry)
    assert spec.workers.count == 3  # lens default_workers


def test_expand_populates_truncation_line_cap(bare_review_registry) -> None:
    spec = _minimal_jobspec()
    # Truncation default is 4000; the lens fixture sets 8000 so the
    # expansion path is observable.
    assert spec.target.truncation.line_cap == 4000
    expand_lens_defaults(spec, bare_review_registry)
    assert spec.target.truncation.line_cap == 8000


def test_expand_populates_output_block(bare_review_registry) -> None:
    spec = _minimal_jobspec()
    expand_lens_defaults(spec, bare_review_registry)
    assert spec.output.filename_template == CANONICAL_FILENAME_TEMPLATE
    assert spec.output.lens_name == "bare-review"


def test_expand_populates_recommended_next_command_template(
    bare_review_registry,
) -> None:
    spec = _minimal_jobspec()
    expand_lens_defaults(spec, bare_review_registry)
    lens = bare_review_registry["bare-review"]
    assert (
        spec.recommended_next_command_template == lens.recommended_next_command_template
    )


# ---------------------------------------------------------------------------
# Snapshot
# ---------------------------------------------------------------------------


def test_expand_returns_resolved_lens_snapshot(bare_review_registry) -> None:
    spec = _minimal_jobspec()
    snapshot = expand_lens_defaults(spec, bare_review_registry)
    assert isinstance(snapshot, ResolvedLensEntry)
    lens = bare_review_registry["bare-review"]
    # All nine DM-011 fields mirror the LensEntry verbatim.
    assert snapshot.name == lens.name
    assert snapshot.system_prompt_fragment == lens.system_prompt_fragment
    assert snapshot.user_template == lens.user_template
    assert snapshot.recipe_name == lens.recipe_name
    assert snapshot.default_workers == lens.default_workers
    assert snapshot.suspect is True
    assert snapshot.tier == "T2"
    assert (
        snapshot.recommended_next_command_template
        == lens.recommended_next_command_template
    )
    assert snapshot.stability == lens.stability


# ---------------------------------------------------------------------------
# Caller-supplied values win (§4.2 override semantics)
# ---------------------------------------------------------------------------


def test_caller_supplied_prompt_system_preserved(bare_review_registry) -> None:
    spec = _minimal_jobspec()
    spec.prompt.system = "Caller-supplied system prompt."
    expand_lens_defaults(spec, bare_review_registry)
    assert spec.prompt.system == "Caller-supplied system prompt."


def test_caller_supplied_recipe_preserved(bare_review_registry) -> None:
    spec = _minimal_jobspec()
    spec.normalization.recipe = "caller-recipe-v2"
    expand_lens_defaults(spec, bare_review_registry)
    assert spec.normalization.recipe == "caller-recipe-v2"


def test_caller_supplied_workers_count_preserved(bare_review_registry) -> None:
    spec = _minimal_jobspec()
    spec.workers.count = (
        5  # explicitly different from both dataclass default (4) and lens default (3)
    )
    expand_lens_defaults(spec, bare_review_registry)
    assert spec.workers.count == 5


def test_caller_supplied_line_cap_preserved(bare_review_registry) -> None:
    spec = _minimal_jobspec()
    spec.target.truncation.line_cap = 1234
    expand_lens_defaults(spec, bare_review_registry)
    assert spec.target.truncation.line_cap == 1234


def test_caller_supplied_lens_name_preserved(bare_review_registry) -> None:
    spec = _minimal_jobspec()
    spec.output.lens_name = "caller-named-lens"
    expand_lens_defaults(spec, bare_review_registry)
    assert spec.output.lens_name == "caller-named-lens"


def test_caller_supplied_next_command_template_preserved(
    bare_review_registry,
) -> None:
    spec = _minimal_jobspec()
    spec.recommended_next_command_template = "sc:custom-followup"
    expand_lens_defaults(spec, bare_review_registry)
    assert spec.recommended_next_command_template == "sc:custom-followup"


# ---------------------------------------------------------------------------
# Unknown lens
# ---------------------------------------------------------------------------


def test_unknown_lens_raises_structured_failure(bare_review_registry) -> None:
    spec = JobSpec(lens="no-such-lens")
    with pytest.raises(PreflightError) as excinfo:
        expand_lens_defaults(spec, bare_review_registry)
    assert [f.rule for f in excinfo.value.failures] == [RULE_UNKNOWN_LENS]
    failure = excinfo.value.failures[0]
    assert failure.reason == "lens-unknown"
    assert failure.path == "lens"
    assert "no-such-lens" in failure.message


def test_empty_registry_raises_unknown_lens() -> None:
    spec = JobSpec(lens="bare-review")
    with pytest.raises(PreflightError) as excinfo:
        expand_lens_defaults(spec, {})
    assert excinfo.value.failures[0].rule == RULE_UNKNOWN_LENS


# ---------------------------------------------------------------------------
# Type guards
# ---------------------------------------------------------------------------


def test_non_jobspec_raises_typeerror(bare_review_registry) -> None:
    with pytest.raises(TypeError):
        expand_lens_defaults({"lens": "bare-review"}, bare_review_registry)  # type: ignore[arg-type]


def test_non_dict_registry_raises_typeerror() -> None:
    spec = _minimal_jobspec()
    with pytest.raises(TypeError):
        expand_lens_defaults(spec, [_bare_review_lens()])  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# Cross-check: every §4.2 spec-side mapping fires in a single expansion
# ---------------------------------------------------------------------------


def test_single_expansion_populates_every_listed_field(bare_review_registry) -> None:
    """Pin every §4.2 spec-side mapping in one fixture so the matrix is
    auditable from one assertion block."""
    spec = _minimal_jobspec()
    snapshot = expand_lens_defaults(spec, bare_review_registry)
    lens = bare_review_registry["bare-review"]
    # 1-2 prompt
    assert spec.prompt.system == lens.system_prompt_fragment
    assert spec.prompt.user_template == lens.user_template
    # 3-4 normalization
    assert spec.normalization.recipe == lens.recipe_name
    assert spec.normalization.template_path == lens.output_template_path
    # 5 workers.count
    assert spec.workers.count == lens.default_workers
    # 6 target.truncation.line_cap
    assert spec.target.truncation.line_cap == lens.default_target_line_cap
    # 7 output.filename_template
    assert spec.output.filename_template == CANONICAL_FILENAME_TEMPLATE
    # 8 output.lens_name
    assert spec.output.lens_name == lens.name
    # 9 recommended_next_command_template
    assert (
        spec.recommended_next_command_template == lens.recommended_next_command_template
    )
    # 10 snapshot-only suspect / tier
    assert snapshot.suspect is lens.suspect
    assert snapshot.tier == lens.tier
