"""Tool-write substrate for roadmap LLM steps (R1.4 / BUILD-REQUEST §MVR §3).

Each of the roadmap pipeline's LLM steps is migrated from a free-form,
markdown-emitting prompt into a *tool-write* generator: the model is asked
to return **structured JSON** conforming to a JSON Schema, that JSON is
validated against the schema, and the human-facing markdown artifact is
rendered **deterministically** from the JSON via a Jinja2 template. This
inverts ``llm-as-black-box-producer`` (master:§Flaw 2) -- the LLM no longer
authors the gate-bearing substrate string directly; it emits typed data and
deterministic code renders the artifact.

This module is the shared scaffolding consumed by all 9 primary + 3 secondary
step migrations in Phase 9 (R1.4):

* :class:`ToolDefinition`   -- binds a step name to its input/output JSON
                              schemas and its render template path.
* :func:`load_schema`       -- resolve + parse a schema from
                              ``templates/tool_schemas/<name>``.
* :func:`validate_tool_output` -- JSON -> ``list[str]`` of schema violations
                              (empty list == PASS).
* :func:`render_tool_output`   -- JSON -> markdown via Jinja2.

The migration runs side-by-side with the legacy markdown path for >=3 release
cycles per Vector A; ``cli/pipeline/models.py:Step.tool_write_mode`` selects
the path and ``Step.template_path`` carries the render template.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

# Directory anchors -- the tool-write templates live as a sibling tree to this
# module (NOT under ``superclaude.examples`` which ``templates.py`` resolves).
_THIS_DIR = Path(__file__).resolve().parent
TEMPLATES_DIR = _THIS_DIR / "templates"
TOOL_SCHEMAS_DIR = TEMPLATES_DIR / "tool_schemas"


@dataclass(frozen=True)
class ToolDefinition:
    """Binds a pipeline step to its tool-write contract.

    Parameters
    ----------
    name:
        Step name, e.g. ``"extract"`` or ``"generate"``. Matches the schema
        filename stem and the render-template stem.
    input_schema:
        JSON Schema describing the structured *inputs* handed to the step's
        tool (kept for symmetry / future tool-call wiring; may be empty).
    output_schema:
        JSON Schema the model's structured output MUST validate against
        before the markdown artifact is rendered.
    render_template:
        Absolute path to the Jinja2 template that renders the markdown
        artifact from the validated output.
    """

    name: str
    input_schema: dict
    output_schema: dict
    render_template: Path


def load_schema(name: str) -> dict:
    """Load and parse a JSON schema from ``templates/tool_schemas/<name>``.

    Parameters
    ----------
    name:
        Schema filename, e.g. ``"extract.schema.json"``.

    Returns
    -------
    dict
        The parsed JSON schema.

    Raises
    ------
    FileNotFoundError
        If the schema file does not exist.
    """
    schema_path = TOOL_SCHEMAS_DIR / name
    if not schema_path.exists():
        raise FileNotFoundError(
            f"Tool schema '{name}' not found at {schema_path}. "
            f"Available: {sorted(p.name for p in TOOL_SCHEMAS_DIR.glob('*.json'))}"
        )
    return json.loads(schema_path.read_text(encoding="utf-8"))


def validate_tool_output(tool_output: dict, schema: dict) -> list[str]:
    """Validate ``tool_output`` against ``schema``.

    Returns a list of human-readable validation error strings. An **empty
    list means the output is valid** (PASS). Each error is prefixed with the
    JSON path of the offending element so the message is actionable.

    The JSON Schema draft is auto-selected from the schema's ``$schema`` key
    (falling back to the latest supported draft) so callers may author
    schemas at any draft level.
    """
    from jsonschema import validators

    validator_cls = validators.validator_for(schema)
    validator = validator_cls(schema)

    errors: list[str] = []
    for err in sorted(
        validator.iter_errors(tool_output),
        key=lambda e: list(map(str, e.absolute_path)),
    ):
        loc = "/".join(str(p) for p in err.absolute_path) or "<root>"
        errors.append(f"{loc}: {err.message}")
    return errors


def render_tool_output(tool_output: dict, template_path: Path) -> str:
    """Render the markdown artifact from structured ``tool_output``.

    Uses Jinja2 with :class:`~jinja2.StrictUndefined` so any reference to a
    field absent from ``tool_output`` raises rather than rendering an empty
    string -- this keeps the rendered artifact faithful to the validated
    data and surfaces template/schema drift loudly.

    Autoescaping is **disabled** because the output is markdown, not HTML.

    Parameters
    ----------
    tool_output:
        The validated structured output (passed as the template's root
        context, so template variables map 1:1 to top-level output keys).
    template_path:
        Absolute path to the ``.md.j2`` template.

    Returns
    -------
    str
        The rendered markdown artifact.
    """
    from jinja2 import Environment, FileSystemLoader, StrictUndefined

    template_path = Path(template_path)
    env = Environment(
        loader=FileSystemLoader(str(template_path.parent)),
        undefined=StrictUndefined,
        trim_blocks=True,
        lstrip_blocks=True,
        autoescape=False,
        keep_trailing_newline=True,
    )
    template = env.get_template(template_path.name)
    return template.render(**tool_output)


# ---------------------------------------------------------------------------
# Tool-write registry + per-step orchestration (R1.4 Step 9.2 onward).
#
# ``ToolWriteSpec`` binds a pipeline ``step_id`` to (a) the ``RoadmapConfig``
# opt-in flag that enables tool-write for that step, (b) the JSON schema the
# model's structured output must validate against, and (c) the Jinja2 template
# that renders the markdown artifact. ``TOOL_WRITE_REGISTRY`` is the single
# lookup the executor consults; ``render_step_tool_write`` is the deterministic
# validate-then-render entry point.
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class ToolWriteSpec:
    """Binds a pipeline step to its tool-write flag, schema, and template.

    Parameters
    ----------
    step_id:
        Pipeline ``Step.id`` this spec governs, e.g. ``"extract"``.
    config_flag:
        Name of the ``RoadmapConfig`` boolean opt-in field that enables
        tool-write for this step, e.g. ``"tool_write_extract"``. The executor
        reads it via ``getattr(config, spec.config_flag, False)``.
    schema_name:
        Schema filename under ``templates/tool_schemas/`` resolved by
        :func:`load_schema`, e.g. ``"extract.schema.json"``.
    template_name:
        Render-template filename under ``templates/`` resolved relative to
        :data:`TEMPLATES_DIR`, e.g. ``"extract.md.j2"``.
    """

    step_id: str
    config_flag: str
    schema_name: str
    template_name: str


# Per-step tool-write registry. R1.4 Step 9.2 lands the ``extract`` entry as
# the pattern-establishing migration; Steps 9.3-9.11 add the remaining primary
# + secondary steps (generate, merge, validate, etc.) by appending keys here.
TOOL_WRITE_REGISTRY: dict[str, ToolWriteSpec] = {
    "extract": ToolWriteSpec(
        step_id="extract",
        config_flag="tool_write_extract",
        schema_name="extract.schema.json",
        template_name="extract.md.j2",
    ),
    # R1.4 Step 9.3: the TDD-input extract path builds a Step with the SAME
    # ``Step.id == "extract"`` as the spec-extract path (see executor
    # _build_steps), so this entry is keyed ``"extract_tdd"`` (NOT step.id) to
    # avoid colliding with the spec-extract entry above. ``step_id`` is still
    # the real ``"extract"`` Step.id; the executor resolves THIS key by
    # ``config.input_type == "tdd"`` before the registry lookup.
    "extract_tdd": ToolWriteSpec(
        step_id="extract",
        config_flag="tool_write_extract_tdd",
        schema_name="extract_tdd.schema.json",
        template_name="extract_tdd.md.j2",
    ),
    # R1.4 Step 9.4: the generate step (PRIMARY phantom-ID source,
    # master:§Top-3 #3). The executor builds TWO parallel generate Steps whose
    # ids are ``generate-{agent.id}`` (e.g. ``generate-opus-architect``), NOT the
    # literal ``"generate"``; the executor's registry-key resolver maps any
    # ``generate-*`` step.id to THIS ``"generate"`` key before the lookup.
    "generate": ToolWriteSpec(
        step_id="generate",
        config_flag="tool_write_generate",
        schema_name="generate.schema.json",
        template_name="generate.md.j2",
    ),
    # R1.4 Step 9.5: the diff step (SIMPLE comparative analysis). Its Step.id IS
    # the literal "diff", so the executor's registry-key resolver falls through
    # to ``_tw_key = step.id`` and routes it to the PLAIN render_step_tool_write
    # (NOT the id-check variant) -- diff carries no roadmap_ids and therefore has
    # no §MVR §3 / Contract #3 phantom-ID subset constraint.
    "diff": ToolWriteSpec(
        step_id="diff",
        config_flag="tool_write_diff",
        schema_name="diff.schema.json",
        template_name="diff.md.j2",
    ),
    # R1.4 Step 9.6: the debate step -- part of the PRESERVED adversarial-debate
    # mechanism (semantic_layer.py stays byte-untouched; ONLY the prompt/output
    # contract is rewritten). Its Step.id IS the literal "debate", so the
    # executor's registry-key resolver falls through to ``_tw_key = step.id`` and
    # routes it to the PLAIN render_step_tool_write (NOT the id-check variant) --
    # debate carries no roadmap_ids and therefore has no §MVR §3 / Contract #3
    # phantom-ID subset constraint.
    "debate": ToolWriteSpec(
        step_id="debate",
        config_flag="tool_write_debate",
        schema_name="debate.schema.json",
        template_name="debate.md.j2",
    ),
    # R1.4 Step 9.7: the score step (SIMPLE evaluation -- selects a base variant
    # and scores both). Its Step.id IS the literal "score", so the executor's
    # registry-key resolver falls through to ``_tw_key = step.id`` and routes it
    # to the PLAIN render_step_tool_write (NOT the id-check variant) -- score
    # carries no roadmap_ids and therefore has no §MVR §3 / Contract #3
    # phantom-ID subset constraint. CONTRACT #8: variant_scores are 0-100
    # evaluation points; convergence thresholds are NEVER baked into the schema
    # or template -- they are sourced from superclaude.contracts at runtime.
    "score": ToolWriteSpec(
        step_id="score",
        config_flag="tool_write_score",
        schema_name="score.schema.json",
        template_name="score.md.j2",
    ),
    # R1.4 Step 9.8: the merge step (SECOND primary phantom-ID source,
    # master:§Top-3 #3 -- it consumes two candidate roadmaps + diff + debate +
    # score and produces the FINAL merged roadmap). Its Step.id IS the literal
    # "merge", so the executor's registry-key resolver falls through to
    # ``_tw_key = step.id`` and resolves to THIS key. Like generate, merge MUST
    # enforce generator-side phantom-ID rejection: the executor routes "merge"
    # (alongside "generate") to render_step_tool_write_with_id_check, deriving
    # spec_ids from the extract sidecar -- a roadmap_id absent from the spec
    # (e.g. FR-99) is REJECTED AT GENERATION TIME (§MVR §3 / Contract #3).
    "merge": ToolWriteSpec(
        step_id="merge",
        config_flag="tool_write_merge",
        schema_name="merge.schema.json",
        template_name="merge.md.j2",
    ),
    # R1.4 Step 9.9: the spec-fidelity step (convergence-loop CORE). Its Step.id
    # IS the literal "spec-fidelity" (hyphenated), so the executor's registry-key
    # resolver falls through to ``_tw_key = step.id`` and resolves to THIS key --
    # hence the key is hyphenated to match step.id, NOT "spec_fidelity". Routes to
    # the PLAIN render_step_tool_write (NOT the id-check variant): spec-fidelity
    # carries no roadmap_ids and therefore has no MVR-3 / Contract #3 phantom-ID
    # subset constraint. IMPORTANT: when config.convergence_enabled is True the
    # executor short-circuits to _run_convergence_spec_fidelity BEFORE the
    # tool-write dispatch, so this entry is exercised only on the single-shot
    # (non-convergence) path; convergence.py / semantic_layer.py stay PRESERVE.
    "spec-fidelity": ToolWriteSpec(
        step_id="spec-fidelity",
        config_flag="tool_write_spec_fidelity",
        schema_name="spec_fidelity.schema.json",
        template_name="spec_fidelity.md.j2",
    ),
    # R1.4 Step 9.11: the test-strategy step (SECONDARY LLM step). Its Step.id IS
    # the literal "test-strategy" (hyphenated), so the executor's registry-key
    # resolver falls through to ``_tw_key = step.id`` and resolves to THIS key --
    # hence the key is hyphenated to match step.id. Routes to the PLAIN
    # render_step_tool_write (NOT the id-check variant): test-strategy carries no
    # roadmap_ids and therefore has no §MVR §3 / Contract #3 phantom-ID subset
    # constraint. CONTRACT #8: interleave_ratio is a test:work milestone ratio,
    # never a convergence threshold.
    "test-strategy": ToolWriteSpec(
        step_id="test-strategy",
        config_flag="tool_write_test_strategy",
        schema_name="test_strategy.schema.json",
        template_name="test_strategy.md.j2",
    ),
    # R1.4 Step 9.11: the certify step (SECONDARY LLM step, terminal verification).
    # Its Step.id IS the literal "certify", so the executor's registry-key resolver
    # falls through to ``_tw_key = step.id`` and resolves to THIS key. certify is
    # built dynamically post-remediate (_run_certify_after_remediate) and run via
    # roadmap_run_step, so the executor dispatch (executor.py:1233) applies. Routes
    # to the PLAIN render_step_tool_write (NOT the id-check variant): certify
    # carries no roadmap_ids. PRESERVE: the R1.3 CodeAssertion (assert_step_reachable)
    # on CERTIFY_GATE is unaffected -- tool-write only changes how the markdown is
    # produced, not the dispatch reachability of the step.
    "certify": ToolWriteSpec(
        step_id="certify",
        config_flag="tool_write_certify",
        schema_name="certify.schema.json",
        template_name="certify.md.j2",
    ),
    # R1.4 Step 9.11: the validate reflect step (SECONDARY validate-subsystem LLM
    # step). Its Step.id IS the literal "reflect" in the single-agent path (the
    # multi-agent path uses "reflect-{agent.id}" and the "adversarial-merge"
    # variant -- those are out of scope for this entry). The reflect step runs
    # under the validate sub-executor (validate_run_step), NOT roadmap_run_step,
    # so the tool-write render hook is added to validate_run_step (which reads the
    # flag from ValidateConfig.tool_write_validate_reflect). Routes to the PLAIN
    # render_step_tool_write: reflect carries no roadmap_ids.
    "reflect": ToolWriteSpec(
        step_id="reflect",
        config_flag="tool_write_validate_reflect",
        schema_name="reflect.schema.json",
        template_name="reflect.md.j2",
    ),
}


def validate_id_subset(
    roadmap_ids: list[str],
    spec_ids: set[str] | list[str],
    accepted_deviations: set[str] | list[str] | None = None,
) -> list[str]:
    """Enforce the §MVR §3 / Contract #3 generator-side subset constraint.

    Every id surfaced into a roadmap MUST be drawn from the spec's universe of
    ids (the ``spec_ids`` the extract step DEFINED) plus any explicitly
    ``accepted_deviations``. Formally::

        roadmap_ids ⊆ set(spec_ids) ∪ set(accepted_deviations)

    This constraint is **load-bearing at the generate/merge steps** (where the
    LLM can hallucinate ids absent from the spec) and is the **identity** at the
    extract step (extract is the SOURCE of ``spec_ids``, so the inclusion is
    trivially satisfied there).

    Returns a list of error strings, one per ``roadmap_id`` not contained in the
    allowed universe. An **empty list means PASS**.
    """
    allowed = set(spec_ids) | set(accepted_deviations or [])
    return [
        f"roadmap_id '{rid}' not in spec_ids ∪ accepted_deviations"
        for rid in roadmap_ids
        if rid not in allowed
    ]


def _parse_and_validate(
    step_id: str,
    json_text: str,
) -> tuple[ToolWriteSpec | None, dict | None, list[str]]:
    """Look up the step spec, parse ``json_text``, and schema-validate it.

    Shared front half of the tool-write back end (used by both
    :func:`render_step_tool_write` and
    :func:`render_step_tool_write_with_id_check`). Returns
    ``(spec, parsed, errors)``:

    * ``errors`` non-empty -> a hard failure (unknown step, JSON syntax error,
      or schema violation); ``parsed`` may be ``None``. Callers MUST short-
      circuit WITHOUT writing any artifact.
    * ``errors == []`` -> ``spec`` and ``parsed`` are both populated and the
      object is schema-valid; the caller proceeds to render.
    """
    spec = TOOL_WRITE_REGISTRY.get(step_id)
    if spec is None:
        return None, None, [f"no tool-write spec for step {step_id}"]

    try:
        parsed = json.loads(json_text)
    except json.JSONDecodeError as exc:
        return spec, None, [f"invalid JSON: {exc}"]

    schema = load_schema(spec.schema_name)
    errors = validate_tool_output(parsed, schema)
    if errors:
        return spec, parsed, errors
    return spec, parsed, []


def _persist_and_render(spec: ToolWriteSpec, parsed: dict, output_path: Path) -> None:
    """Write the JSON sidecar and render the markdown artifact (PASS path).

    Persists the structured JSON sidecar (durable typed substrate) to
    ``output_path.with_suffix(".json")``, then renders the human-facing
    markdown deterministically from it and writes it to ``output_path``.
    """
    sidecar_path = output_path.with_suffix(".json")
    sidecar_path.write_text(
        json.dumps(parsed, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    markdown = render_tool_output(parsed, TEMPLATES_DIR / spec.template_name)
    output_path.write_text(markdown, encoding="utf-8")


def render_step_tool_write(
    step_id: str,
    json_text: str,
    output_path: Path,
) -> list[str]:
    """Validate a step's structured JSON and render its markdown artifact.

    The deterministic tool-write back end: given the raw JSON ``json_text`` the
    LLM emitted for ``step_id``, this

    1. looks up the step's :class:`ToolWriteSpec` in
       :data:`TOOL_WRITE_REGISTRY`;
    2. parses ``json_text`` (a JSON syntax error short-circuits to an error);
    3. validates the parsed object against the step schema via
       :func:`validate_tool_output` (schema violations short-circuit -- **no
       file is written** on failure);
    4. on PASS, writes the parsed JSON pretty-printed to the durable structured
       sidecar ``output_path.with_suffix(".json")``, then renders the markdown
       artifact via :func:`render_tool_output` and writes it to ``output_path``.

    Returns a list of error strings; an **empty list means success** (both the
    sidecar and the markdown artifact were written).
    """
    spec, parsed, errors = _parse_and_validate(step_id, json_text)
    if errors:
        # Do NOT write any artifact on failure -- the executor surfaces the
        # errors as a gate failure and the markdown path is never polluted.
        return errors

    # PASS: persist the structured JSON sidecar and render the markdown.
    _persist_and_render(spec, parsed, output_path)  # type: ignore[arg-type]
    return []


def render_step_tool_write_with_id_check(
    step_id: str,
    json_text: str,
    output_path: Path,
    spec_ids: set[str] | list[str],
    accepted_deviations: set[str] | list[str] | None = None,
    require_spec_ids: bool = False,
) -> list[str]:
    """Generator-side tool-write back end with phantom-ID rejection (Contract #3).

    Identical to :func:`render_step_tool_write` -- look up the spec, parse,
    schema-validate, then persist+render -- but inserts the load-bearing
    §MVR §3 / Contract #3 SET-membership gate BETWEEN schema validation and
    rendering: the ``roadmap_ids`` array extracted from the parsed JSON MUST be
    a subset of ``spec_ids ∪ accepted_deviations`` (enforced via
    :func:`validate_id_subset`). A phantom id (e.g. ``FR-99`` that the
    extraction never defined) is **REJECTED AT GENERATION TIME** -- the markdown
    artifact and the JSON sidecar are NOT written, exactly as for a schema
    violation.

    If ``spec_ids`` is empty/falsy the subset check is **skipped** (the
    inclusion is vacuously the identity -- acceptable when the upstream extract
    step is not itself in tool-write mode and therefore exposed no spec_ids
    sidecar).

    ``require_spec_ids`` (default ``False``) is an optional self-defending guard
    for callers that KNOW a non-empty spec universe must exist (the generate and
    merge steps, which source their universe from the always-written
    ``spec_id_registry.json``). When ``require_spec_ids`` is ``True`` AND the
    effective ``spec_ids`` set is empty/falsy, the function refuses to render and
    returns a hard error WITHOUT writing any artifact -- rather than silently
    taking the vacuous identity skip and emitting an unconstrained roadmap. When
    ``require_spec_ids`` is ``False`` the legitimate identity skip is preserved
    byte-for-byte (extract-like callers that expose no spec_ids sidecar), so all
    existing callers' behavior is unchanged.

    Returns a list of error strings; an **empty list means success**.
    """
    spec, parsed, errors = _parse_and_validate(step_id, json_text)
    if errors:
        return errors

    # Phantom-ID rejection: roadmap_ids ⊆ spec_ids ∪ accepted_deviations.
    if not spec_ids:
        if require_spec_ids:
            # Self-defending: the caller (generate/merge) asserted a non-empty
            # spec universe is REQUIRED, but none was supplied. Refuse to render
            # an unconstrained roadmap -- do NOT write any artifact.
            return ["require_spec_ids=True but spec_ids universe is empty"]
        # require_spec_ids is False: legitimate identity skip (extract-like
        # callers expose no spec_ids sidecar -- the inclusion is vacuous).
    else:
        roadmap_ids = parsed.get("roadmap_ids", []) if parsed else []  # type: ignore[union-attr]
        id_errors = validate_id_subset(roadmap_ids, spec_ids, accepted_deviations)
        if id_errors:
            # Phantom id present -- do NOT write any artifact (generation-time
            # rejection). This is the Contract #3 generator-side gate.
            return id_errors

    _persist_and_render(spec, parsed, output_path)  # type: ignore[arg-type]
    return []
