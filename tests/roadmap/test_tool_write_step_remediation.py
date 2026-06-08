"""R1.4 Step 9.11 remediation tool-write: PARITY-ONLY (NO schema/template/render).

The remediation step is a special case among the R1.4 dual-write steps. It gets
the LIGHTWEIGHT surface-consistency pieces (a ``tool_write`` kwarg on the prompt
builder + a ``RoadmapConfig.tool_write_remediate`` flag + a ``--tool-write-remediate``
CLI flag) but DELIBERATELY gets NO schema, NO Jinja template, NO registry entry,
and NO executor render hook.

Why parity-only and not full tool-write:

The remediation agent EDITS the target roadmap files DIRECTLY (in place), and
success is verified by a file-content diff against a ``.pre-remediate`` snapshot
-- the agent's ``remediate-{stem}.md`` stdout transcript is never parsed, is not
gate-bearing, and is not rendered from a template. There is therefore no
renderable markdown substrate to invert into a tool-write JSON contract.

Crucially, ``build_remediation_prompt`` is a file-EDIT-INSTRUCTION prompt: it
emits NO roadmap-ID-bearing artifact, so it carries no ``roadmap_ids`` to
constrain. The §MVR §3 / Contract #3 phantom-ID subset check is a NO-OP here and
is intentionally NOT applied.

Evidence for the N/A render determination (cited file:line):

* ``remediate_executor.py:217`` -- ``_run_agent_for_file`` builds the remediation
  prompt and spawns a ClaudeProcess whose effect is in-place edits to the target
  file; the ``output_file`` (``remediate-{stem}.md``) captures the agent's
  stdout transcript only.
* ``remediate_executor.py:100-145`` -- ``.pre-remediate`` snapshots are taken
  before the agent runs and restored on failure.
* ``remediate_executor.py:365-394`` -- ``_check_diff_size`` measures success by
  comparing the snapshot against the EDITED target file content -- proof the
  step's product is the file edit, not a parsed/rendered artifact.
* ``remediate_executor.py:563`` -- ``update_remediation_tasklist`` writes the
  REMEDIATE_GATE artifact (``remediation-tasklist.md``) DETERMINISTICALLY from
  the ``Finding`` objects (code-authored, not LLM-authored), so there is no LLM
  markdown substrate to invert into a tool-write contract there either.

FLAG (R1.6): ``remediate_parser.py`` is a DELETION CANDIDATE (it parses
validation reports into Findings -- an INPUT parser superseded by structured
sidecars), but MUST NOT be deleted now; dual-write must run >= 3 release cycles
first.

These tests lock both the parity-only surface AND the N/A render determination so
a future contributor neither (a) silently adds a half-wired remediation render
path nor (b) breaks the byte-identical default-prompt guarantee.
"""

from __future__ import annotations

import inspect

from superclaude.cli.roadmap.models import Finding, RoadmapConfig
from superclaude.cli.roadmap.remediate_prompts import build_remediation_prompt
from superclaude.cli.roadmap.tool_writer import TOOL_WRITE_REGISTRY


def _sample_findings() -> list[Finding]:
    """A representative set of findings for prompt-parity assertions."""
    return [
        Finding(
            id="F-001",
            severity="BLOCKING",
            dimension="Structure",
            description="Missing acceptance criteria for M1.",
            location="roadmap.md:M1",
            evidence="Expected AC block; found none.",
            fix_guidance="Add an acceptance-criteria bullet list under M1.",
            files_affected=["roadmap.md"],
        ),
        Finding(
            id="F-002",
            severity="WARNING",
            dimension="Traceability",
            description="Deliverable D3 has no owner.",
            location="roadmap.md:D3",
            evidence="owner field absent.",
            fix_guidance="Assign an owner to D3.",
            files_affected=["roadmap.md"],
        ),
    ]


# --- N/A render determination: NO schema / template / registry entry ---------


def test_remediation_has_no_tool_write_registry_entry() -> None:
    """N/A render: remediation is intentionally absent from the tool-write registry.

    No registry entry => no schema_name / template_name / render hook. The
    parity-only surface lives entirely in the prompt builder + config flag, never
    in the deterministic render path.
    """
    assert "remediate" not in TOOL_WRITE_REGISTRY
    assert "remediation" not in TOOL_WRITE_REGISTRY


# --- Parity-only surface: prompt builder kwarg + config flag -----------------


def test_remediation_prompt_builder_has_tool_write_kwarg() -> None:
    """build_remediation_prompt gains an additive ``tool_write`` kwarg (last param).

    Surface-consistency with the other R1.4 dual-write prompt builders. The kwarg
    defaults to False and is the LAST positional parameter (additive, no
    reordering of target_file/findings).
    """
    params = list(inspect.signature(build_remediation_prompt).parameters)
    assert params == ["target_file", "findings", "tool_write"]
    tw = inspect.signature(build_remediation_prompt).parameters["tool_write"]
    assert tw.default is False


def test_remediation_prompt_default_is_byte_identical_to_tool_write_false() -> None:
    """LOAD-BEARING: default prompt == tool_write=False prompt, byte-for-byte.

    The additive kwarg must not perturb the production (default) prompt at all.
    """
    findings = _sample_findings()
    target = "roadmap.md"
    assert build_remediation_prompt(target, findings) == build_remediation_prompt(
        target, findings, tool_write=False
    )


def test_remediation_prompt_no_roadmap_ids_contract3_constraint() -> None:
    """No §MVR §3 / Contract #3 phantom-ID subset check applies to remediate.

    remediate is a file-edit-instruction prompt that emits NO roadmap-ID-bearing
    artifact, so the phantom-ID kill is a NO-OP here. Assert that NEITHER the
    default nor the tool_write=True prompt injects any roadmap_ids / id-subset /
    Contract #3 language: there are no IDs to constrain.
    """
    findings = _sample_findings()
    target = "roadmap.md"
    for prompt in (
        build_remediation_prompt(target, findings),
        build_remediation_prompt(target, findings, tool_write=True),
    ):
        lowered = prompt.lower()
        assert "roadmap_ids" not in lowered
        assert "phantom" not in lowered
        assert "contract #3" not in lowered
        assert "id subset" not in lowered
        assert "id-subset" not in lowered


def test_remediation_prompt_tool_write_true_preserves_default_prefix() -> None:
    """tool_write=True only APPENDS; it never mutates the byte-identical default body.

    The structured-output hint (surface-consistency only) is appended after the
    default body, so the default prompt is a strict prefix of the tool_write=True
    prompt.
    """
    findings = _sample_findings()
    target = "roadmap.md"
    default_prompt = build_remediation_prompt(target, findings)
    tw_prompt = build_remediation_prompt(target, findings, tool_write=True)
    assert tw_prompt.startswith(default_prompt)


def test_roadmap_config_tool_write_remediate_default_false() -> None:
    """RoadmapConfig.tool_write_remediate exists and defaults to False (opt-in)."""
    field = RoadmapConfig.__dataclass_fields__["tool_write_remediate"]
    assert field.default is False
