"""Roadmap CLI commands -- Click command group for ``superclaude roadmap``.

Defines the ``superclaude roadmap`` command with all flags per spec FR-009.
"""

from __future__ import annotations

import sys
from pathlib import Path

import click


@click.group("roadmap")
def roadmap_group():
    """Generate project roadmaps from specification files.

    Orchestrates an 8-step pipeline: extract, generate (x2 parallel),
    diff, debate, score, merge, and test-strategy. Each step runs as
    a fresh Claude subprocess with file-on-disk gates between steps.

    Examples:
        superclaude roadmap run spec.md
        superclaude roadmap run spec.md --agents sonnet:security,sonnet:qa
        superclaude roadmap run spec.md --depth deep
        superclaude roadmap run spec.md --dry-run
        superclaude roadmap run spec.md --resume
    """
    pass


@roadmap_group.command()
@click.argument(
    "input_files", nargs=-1, required=True, type=click.Path(exists=True, path_type=Path)
)
@click.option(
    "--agents",
    default=None,
    help=(
        "Comma-separated agent specs: model[:persona]. "
        "Default: opus:architect,sonnet:architect"
    ),
)
@click.option(
    "--output",
    "output_dir",
    type=click.Path(path_type=Path),
    default=None,
    help="Output directory for all artifacts. Default: parent dir of spec-file.",
)
@click.option(
    "--depth",
    type=click.Choice(["quick", "standard", "deep"], case_sensitive=False),
    default=None,
    help="Debate round depth: quick=1, standard=2, deep=3. Default: standard.",
)
@click.option(
    "--resume",
    is_flag=True,
    help=(
        "Skip steps whose outputs already pass their gates. "
        "Re-run from the first failing step."
    ),
)
@click.option(
    "--dry-run",
    is_flag=True,
    help="Print step plan and gate criteria, then exit without launching subprocesses.",
)
@click.option(
    "--model",
    default="",
    help="Override model for all steps. Default: per-agent model for generate steps.",
)
@click.option(
    "--max-turns",
    type=int,
    default=100,
    help="Max agent turns per claude subprocess. Default: 100.",
)
@click.option(
    "--debug",
    is_flag=True,
    help="Enable debug logging to output_dir/roadmap-debug.log.",
)
@click.option(
    "--no-validate",
    is_flag=True,
    help="Skip post-pipeline validation step.",
)
@click.option(
    "--allow-regeneration",
    is_flag=True,
    default=False,
    help="Allow patches that exceed the diff-size threshold (FR-9). Use with caution.",
)
@click.option(
    "--no-convergence",
    is_flag=True,
    default=False,
    help="Disable the spec-fidelity convergence engine (use single-shot LLM check instead).",
)
@click.option(
    "--retrospective",
    type=click.Path(exists=False, path_type=Path),
    default=None,
    help=(
        "Path to a retrospective file from a prior release cycle. "
        "Content is framed as advisory 'areas to watch' in extraction. "
        "Missing file is not an error -- extraction proceeds normally."
    ),
)
@click.option(
    "--input-type",
    type=click.Choice(["auto", "tdd", "spec"], case_sensitive=False),
    default="auto",
    help="Input file type. auto=detect from content (PRD, TDD, or spec), tdd/spec=force type. PRD files are auto-detected when passed as positional arguments. Default: auto.",
)
@click.option(
    "--tdd-file",
    type=click.Path(exists=True, path_type=Path),
    default=None,
    help=(
        "Path to a TDD file for supplementary technical context enrichment. "
        "When the primary input is a spec, the TDD provides data models, "
        "API endpoints, component inventory, and test strategy detail. "
        "Ignored if the primary input is itself a TDD (use --input-type spec to force)."
    ),
)
@click.option(
    "--prd-file",
    type=click.Path(exists=True, path_type=Path),
    default=None,
    help=(
        "Path to a PRD file for supplementary business context enrichment. "
        "The PRD provides personas, success metrics, compliance requirements, "
        "and scope boundaries. Works with both spec and TDD primary inputs. "
        "Auto-wired from .roadmap-state.json on --resume if not specified."
    ),
)
@click.option(
    "--no-compress",
    "no_compress",
    is_flag=True,
    default=False,
    help=(
        "Disable markdown compression of LLM inputs (spec, variants, merge). "
        "Compression is lossless (strategies S-01..S-22) and applied only to "
        "LLM-consumed content; deterministic steps always read originals."
    ),
)
@click.option(
    "--allow-cosmetic-remediation/--no-allow-cosmetic-remediation",
    "allow_cosmetic_remediation",
    default=True,
    help=(
        "Auto-fix pure-cosmetic gate failures (heading shape, dash variants, "
        "whitespace, smart-quotes, table padding) before halting the pipeline. "
        "Semantic failures (missing milestones, placeholder leaks, OQ-xxx in "
        "deliverables) always halt. Default: on."
    ),
)
@click.option(
    "--strict-no-remediation",
    "strict_no_remediation",
    is_flag=True,
    default=False,
    help=(
        "Disable cosmetic-failure auto-remediation entirely. Equivalent to "
        "--no-allow-cosmetic-remediation; explicit alias for high-stakes runs "
        "where any drift should halt for human review."
    ),
)
@click.option(
    "--tool-write-extract",
    "tool_write_extract",
    is_flag=True,
    default=False,
    help=(
        "R1.4 dual-write: extract step emits structured JSON rendered "
        "deterministically to markdown (opt-in; markdown path remains default "
        "until cutover)."
    ),
)
@click.option(
    "--tool-write-extract-tdd",
    "tool_write_extract_tdd",
    is_flag=True,
    default=False,
    help="R1.4 dual-write: TDD-input extract step emits structured JSON rendered to markdown (opt-in).",
)
@click.option(
    "--tool-write-generate",
    "tool_write_generate",
    is_flag=True,
    default=False,
    help="R1.4 dual-write: generate step emits structured JSON (with generation-time phantom-ID rejection) rendered to markdown (opt-in).",
)
@click.option(
    "--tool-write-diff",
    "tool_write_diff",
    is_flag=True,
    default=False,
    help="R1.4 dual-write: diff step emits structured JSON rendered to markdown (opt-in).",
)
@click.option(
    "--tool-write-debate",
    "tool_write_debate",
    is_flag=True,
    default=False,
    help="R1.4 dual-write: debate step (PRESERVED adversarial-debate mechanism) emits structured JSON rendered to markdown (opt-in).",
)
@click.option(
    "--tool-write-score",
    "tool_write_score",
    is_flag=True,
    default=False,
    help="R1.4 dual-write: score step emits structured JSON rendered to markdown (opt-in).",
)
@click.option(
    "--tool-write-merge",
    "tool_write_merge",
    is_flag=True,
    default=False,
    help="R1.4 dual-write: merge step (SECOND primary phantom-ID source) emits structured JSON with generation-time phantom-ID rejection, rendered to markdown (opt-in).",
)
@click.option(
    "--tool-write-spec-fidelity",
    "tool_write_spec_fidelity",
    is_flag=True,
    default=False,
    help="R1.4 dual-write: spec-fidelity step emits structured JSON rendered to markdown (opt-in; single-shot path only -- convergence mode is unaffected).",
)
@click.option(
    "--tool-write-test-strategy",
    "tool_write_test_strategy",
    is_flag=True,
    default=False,
    help="R1.4 dual-write: test-strategy step (secondary) emits structured JSON rendered to markdown (opt-in).",
)
@click.option(
    "--tool-write-certify",
    "tool_write_certify",
    is_flag=True,
    default=False,
    help="R1.4 dual-write: certify step (secondary) emits structured JSON rendered to markdown (opt-in).",
)
@click.pass_context
def run(
    ctx: click.Context,
    input_files: tuple[Path, ...],
    agents: str | None,
    output_dir: Path | None,
    depth: str | None,
    resume: bool,
    dry_run: bool,
    model: str,
    max_turns: int,
    debug: bool,
    no_validate: bool,
    allow_regeneration: bool,
    no_convergence: bool,
    retrospective: Path | None,
    input_type: str,
    tdd_file: Path | None,
    prd_file: Path | None,
    no_compress: bool,
    allow_cosmetic_remediation: bool,
    strict_no_remediation: bool,
    tool_write_extract: bool,
    tool_write_extract_tdd: bool,
    tool_write_generate: bool,
    tool_write_diff: bool,
    tool_write_debate: bool,
    tool_write_score: bool,
    tool_write_merge: bool,
    tool_write_spec_fidelity: bool,
    tool_write_test_strategy: bool,
    tool_write_certify: bool,
) -> None:
    """Run the roadmap generation pipeline on INPUT_FILES.

    INPUT_FILES accepts 1-3 markdown files (spec, TDD, PRD) in any order.
    Content type is auto-detected. Use --input-type to override for single files.

    Examples:
        superclaude roadmap run spec.md
        superclaude roadmap run spec.md tdd.md
        superclaude roadmap run spec.md tdd.md prd.md
    """
    if len(input_files) > 3:
        raise click.UsageError(
            f"Expected 1-3 input files, got {len(input_files)}. "
            "Provide at most one spec, one TDD, and one PRD."
        )
    from .executor import _route_input_files, execute_roadmap
    from .models import AgentSpec, RoadmapConfig

    # Route positional files + explicit flags into pipeline slots
    routing = _route_input_files(
        input_files,
        explicit_tdd=tdd_file,
        explicit_prd=prd_file,
        explicit_input_type=input_type,
    )

    # Detect whether --agents and --depth were explicitly provided
    agents_explicit = (
        ctx.get_parameter_source("agents") == click.core.ParameterSource.COMMANDLINE
    )
    depth_explicit = (
        ctx.get_parameter_source("depth") == click.core.ParameterSource.COMMANDLINE
    )

    # Parse agents only when explicitly provided
    agent_specs = (
        [AgentSpec.parse(a.strip()) for a in agents.split(",")]
        if agents is not None
        else None
    )

    # Resolve output directory
    resolved_output = output_dir if output_dir is not None else input_files[0].parent

    # Resolve retrospective file (missing file is not an error)
    retro_path = None
    if retrospective is not None:
        retro_path = Path(retrospective).resolve()
        if not retro_path.is_file():
            click.echo(
                f"[roadmap] Retrospective file not found: {retro_path} "
                "(proceeding without retrospective context)",
                err=True,
            )
            retro_path = None

    # --strict-no-remediation overrides --allow-cosmetic-remediation when
    # both are provided. The strict alias exists so high-stakes invocations
    # can be self-evidently strict without inverting a default-on flag.
    cosmetic_remediation_on = allow_cosmetic_remediation and not strict_no_remediation

    # Build config kwargs — only include agents/depth when explicitly provided,
    # so RoadmapConfig's own defaults apply when user omitted them.
    config_kwargs: dict = {
        "spec_file": routing["spec_file"].resolve(),
        "output_dir": resolved_output.resolve(),
        "work_dir": resolved_output.resolve(),
        "dry_run": dry_run,
        "max_turns": max_turns,
        "model": model,
        "debug": debug,
        "retrospective_file": retro_path,
        "allow_regeneration": allow_regeneration,
        "convergence_enabled": not no_convergence,
        "input_type": routing["input_type"],
        "tdd_file": routing["tdd_file"].resolve() if routing["tdd_file"] else None,
        "prd_file": routing["prd_file"].resolve() if routing["prd_file"] else None,
        "compress_enabled": not no_compress,
        "allow_cosmetic_remediation": cosmetic_remediation_on,
        "tool_write_extract": tool_write_extract,
        "tool_write_extract_tdd": tool_write_extract_tdd,
        "tool_write_generate": tool_write_generate,
        "tool_write_diff": tool_write_diff,
        "tool_write_debate": tool_write_debate,
        "tool_write_score": tool_write_score,
        "tool_write_merge": tool_write_merge,
        "tool_write_spec_fidelity": tool_write_spec_fidelity,
        "tool_write_test_strategy": tool_write_test_strategy,
        "tool_write_certify": tool_write_certify,
    }
    if agent_specs is not None:
        config_kwargs["agents"] = agent_specs
    if depth is not None:
        config_kwargs["depth"] = depth

    config = RoadmapConfig(**config_kwargs)

    # User feedback: show resolved routing
    resolved_type = routing["input_type"]
    click.echo(
        f"[roadmap] Input type: {resolved_type} "
        f"(spec={routing['spec_file']}, tdd={routing['tdd_file']}, prd={routing['prd_file']})",
        err=True,
    )

    execute_roadmap(
        config,
        resume=resume,
        no_validate=no_validate,
        agents_explicit=agents_explicit,
        depth_explicit=depth_explicit,
    )


@roadmap_group.command("accept-spec-change")
@click.argument("output_dir", type=click.Path(exists=True, path_type=Path))
def accept_spec_change(output_dir: Path) -> None:
    """Update spec_hash after accepted deviation records.

    When the spec file is edited to formalize an accepted deviation
    (documentation sync, not a functional change), this command updates
    the stored spec_hash so --resume can proceed without a full cascade.

    Requires at least one dev-*-accepted-deviation.md file with
    disposition: ACCEPTED and spec_update_required: true as evidence.

    Note: .roadmap-state.json requires exclusive write access during
    execution. Do not run concurrent roadmap operations on the same
    output directory.

    OUTPUT_DIR is the directory containing .roadmap-state.json.

    Examples:
        superclaude roadmap accept-spec-change ./output
    """
    from .spec_patch import prompt_accept_spec_change

    sys.exit(prompt_accept_spec_change(output_dir.resolve()))


@roadmap_group.command()
@click.argument("output_dir", type=click.Path(exists=True, path_type=Path))
@click.option(
    "--agents",
    default="opus:architect",
    help=(
        "Comma-separated agent specs: model[:persona]. "
        "Default: opus:architect (single-agent for cost efficiency)."
    ),
)
@click.option(
    "--model",
    default="",
    help="Override model for all validation steps.",
)
@click.option(
    "--max-turns",
    type=int,
    default=100,
    help="Max agent turns per claude subprocess. Default: 100.",
)
@click.option(
    "--debug",
    is_flag=True,
    help="Enable debug logging.",
)
@click.option(
    "--tool-write-reflect",
    "tool_write_reflect",
    is_flag=True,
    default=False,
    help="R1.4 dual-write: reflect step (secondary) emits structured JSON rendered to markdown (opt-in; single-agent path only).",
)
def validate(
    output_dir: Path,
    agents: str,
    model: str,
    max_turns: int,
    debug: bool,
    tool_write_reflect: bool,
) -> None:
    """Validate roadmap pipeline outputs in OUTPUT_DIR.

    OUTPUT_DIR must contain roadmap.md, test-strategy.md, and extraction.md
    from a prior ``roadmap run``.

    Examples:
        superclaude roadmap validate ./output
        superclaude roadmap validate ./output --agents opus:architect,sonnet:qa
    """
    from .models import AgentSpec, ValidateConfig
    from .validate_executor import execute_validate

    agent_specs = [AgentSpec.parse(a.strip()) for a in agents.split(",")]

    config = ValidateConfig(
        output_dir=output_dir.resolve(),
        agents=agent_specs,
        work_dir=output_dir.resolve(),
        max_turns=max_turns,
        model=model,
        debug=debug,
        tool_write_reflect=tool_write_reflect,
    )

    counts = execute_validate(config)

    # Surface results as CLI output (exit 0 per NFR-006)
    blocking = counts.get("blocking_count", 0)
    warning = counts.get("warning_count", 0)
    info = counts.get("info_count", 0)

    if blocking > 0:
        click.echo(
            click.style(f"WARNING: {blocking} blocking issue(s) found", fg="yellow")
        )
    if warning > 0:
        click.echo(f"Warnings: {warning}")
    if info > 0:
        click.echo(f"Info: {info}")

    click.echo(
        f"\n[validate] Complete: {blocking} blocking, {warning} warning, {info} info"
    )
