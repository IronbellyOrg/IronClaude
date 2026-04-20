"""Validation executor -- orchestrates the validation pipeline.

Reads pipeline outputs (roadmap.md, test-strategy.md, extraction.md),
routes by agent count (single-agent reflection vs. multi-agent adversarial),
applies gates, and writes validation reports.

Reuses ``execute_pipeline()`` and ``ClaudeProcess`` from the pipeline module.
No new subprocess abstractions (per roadmap constraint).

Context isolation: each subprocess receives only its prompt via inline embedding.
--file is a cloud download mechanism and does not inject local file content.
"""

from __future__ import annotations

import json
import logging
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable

from ..pipeline.executor import execute_pipeline
from ..pipeline.models import PipelineConfig, Step, StepResult, StepStatus
from ..pipeline.process import ClaudeProcess
from .executor import read_state
from .models import ValidateConfig
from .validate_gates import ADVERSARIAL_MERGE_GATE, REFLECT_GATE
from .validate_prompts import build_merge_prompt, build_reflect_prompt

_log = logging.getLogger("superclaude.roadmap.validate_executor")

# Token-context advisory threshold (soft warning, non-fatal).
# Prompts are delivered via stdin in ClaudeProcess.start, bypassing the Linux
# MAX_ARG_STRLEN ceiling. This threshold only surfaces prompts that may strain
# the model's context window.
_LARGE_PROMPT_WARN_BYTES = 500 * 1024  # 500 KB

# Required input files for validation
_REQUIRED_INPUTS = ("roadmap.md", "test-strategy.md", "extraction.md")


def _embed_inputs(input_paths: list[Path]) -> str:
    """Read input files and return their contents as fenced code blocks."""
    if not input_paths:
        return ""
    blocks: list[str] = []
    for p in input_paths:
        content = Path(p).read_text(encoding="utf-8")
        blocks.append(f"# {p}\n```\n{content}\n```")
    return "\n\n".join(blocks)


def _sanitize_output(output_file: Path) -> int:
    """Strip conversational preamble before YAML frontmatter."""
    import os
    import re

    try:
        content = output_file.read_text(encoding="utf-8")
    except FileNotFoundError:
        return 0

    if content.lstrip().startswith("---"):
        return 0

    match = re.search(r"^---[ \t]*$", content, re.MULTILINE)
    if match is None:
        return 0

    preamble = content[: match.start()]
    cleaned = content[match.start() :]
    preamble_bytes = len(preamble.encode("utf-8"))

    tmp_file = output_file.with_suffix(output_file.suffix + ".tmp")
    tmp_file.write_text(cleaned, encoding="utf-8")
    os.replace(tmp_file, output_file)

    _log.info("Stripped %d-byte preamble from %s", preamble_bytes, output_file)
    return preamble_bytes


def validate_run_step(
    step: Step,
    config: PipelineConfig,
    cancel_check: Callable[[], bool],
) -> StepResult:
    """Execute a single validation step as a Claude subprocess.

    Mirrors ``roadmap_run_step`` from ``executor.py``: builds argv,
    launches process, waits with timeout, sanitizes output.
    """
    started_at = datetime.now(timezone.utc)

    if config.dry_run:
        _log.info("[dry-run] Would execute step '%s'", step.id)
        return StepResult(
            step=step,
            status=StepStatus.PASS,
            attempt=1,
            started_at=started_at,
            finished_at=datetime.now(timezone.utc),
        )

    # Prompt + inputs are composed inline and delivered via stdin downstream.
    embedded = _embed_inputs(step.inputs)
    if embedded:
        composed = step.prompt + "\n\n" + embedded
        if len(composed.encode("utf-8")) > _LARGE_PROMPT_WARN_BYTES:
            _log.warning(
                "validate_executor: composed prompt is %d bytes (> %d);"
                " may strain model context window",
                len(composed.encode("utf-8")),
                _LARGE_PROMPT_WARN_BYTES,
            )
        effective_prompt = composed
        extra_args: list[str] = []
    else:
        effective_prompt = step.prompt
        extra_args = []

    proc = ClaudeProcess(
        prompt=effective_prompt,
        output_file=step.output_file,
        error_file=step.output_file.with_suffix(".err"),
        max_turns=config.max_turns,
        model=step.model or config.model,
        permission_flag=config.permission_flag,
        timeout_seconds=step.timeout_seconds,
        output_format="text",
        extra_args=extra_args,
    )

    proc.start()

    while proc._process is not None and proc._process.poll() is None:
        if cancel_check():
            proc.terminate()
            return StepResult(
                step=step,
                status=StepStatus.CANCELLED,
                attempt=1,
                gate_failure_reason="Cancelled by external signal",
                started_at=started_at,
                finished_at=datetime.now(timezone.utc),
            )
        time.sleep(1)

    exit_code = proc.wait()
    finished_at = datetime.now(timezone.utc)

    if exit_code == 124:
        return StepResult(
            step=step,
            status=StepStatus.TIMEOUT,
            attempt=1,
            gate_failure_reason=f"Step '{step.id}' timed out after {step.timeout_seconds}s",
            started_at=started_at,
            finished_at=finished_at,
        )

    if exit_code != 0:
        return StepResult(
            step=step,
            status=StepStatus.FAIL,
            attempt=1,
            gate_failure_reason=f"Step '{step.id}' exited with code {exit_code}",
            started_at=started_at,
            finished_at=finished_at,
        )

    _sanitize_output(step.output_file)

    return StepResult(
        step=step,
        status=StepStatus.PASS,
        attempt=1,
        started_at=started_at,
        finished_at=finished_at,
    )


def _validate_input_files(output_dir: Path) -> tuple[list[Path], Path | None, Path | None, Path | None]:
    """Validate required input files and resolve original source inputs from state.

    Returns
    -------
    tuple of:
        pipeline_paths: list of 3 required pipeline output paths
            (roadmap.md, test-strategy.md, extraction.md)
        spec_file: original spec file path (from .roadmap-state.json), or None
        tdd_file: original TDD file path, or None
        prd_file: original PRD file path, or None

    Raises FileNotFoundError if any of the 3 required pipeline files is missing.
    """
    pipeline_paths = []
    for name in _REQUIRED_INPUTS:
        p = output_dir / name
        if not p.exists():
            raise FileNotFoundError(f"Required validation input not found: {p}")
        pipeline_paths.append(p)

    # Resolve original source inputs from pipeline state
    spec_file: Path | None = None
    tdd_file: Path | None = None
    prd_file: Path | None = None

    state = read_state(output_dir / ".roadmap-state.json")
    if state is not None:
        for key, attr in (("spec_file", "spec_file"), ("tdd_file", "tdd_file"), ("prd_file", "prd_file")):
            raw = state.get(key)
            if raw is not None:
                p = Path(raw)
                if p.exists():
                    if key == "spec_file":
                        spec_file = p
                    elif key == "tdd_file":
                        tdd_file = p
                    else:
                        prd_file = p
                else:
                    _log.warning(
                        "Source input %s=%s from .roadmap-state.json not found; "
                        "validation will skip input-aware dimensions",
                        key, raw,
                    )

    return pipeline_paths, spec_file, tdd_file, prd_file


def _build_single_agent_steps(
    config: ValidateConfig,
    validate_dir: Path,
    input_paths: list[Path],
    *,
    spec_file: Path | None = None,
    tdd_file: Path | None = None,
    prd_file: Path | None = None,
) -> list[Step | list[Step]]:
    """Build steps for single-agent validation (1 agent -> reflect -> report)."""
    roadmap, test_strategy, extraction = input_paths

    # Include original source inputs so the LLM can validate coverage
    all_inputs = list(input_paths)
    for f in (spec_file, tdd_file, prd_file):
        if f is not None:
            all_inputs.append(f)

    return [
        Step(
            id="reflect",
            prompt=build_reflect_prompt(
                str(roadmap),
                str(test_strategy),
                str(extraction),
                spec_file=str(spec_file) if spec_file else None,
                tdd_file=str(tdd_file) if tdd_file else None,
                prd_file=str(prd_file) if prd_file else None,
            ),
            output_file=validate_dir / "validation-report.md",
            gate=REFLECT_GATE,
            timeout_seconds=600,
            inputs=all_inputs,
            retry_limit=1,
            model=config.agents[0].model,
        ),
    ]


def _build_multi_agent_steps(
    config: ValidateConfig,
    validate_dir: Path,
    input_paths: list[Path],
    *,
    spec_file: Path | None = None,
    tdd_file: Path | None = None,
    prd_file: Path | None = None,
) -> list[Step | list[Step]]:
    """Build steps for multi-agent validation.

    N agents -> N parallel reflections -> gate each -> adversarial merge.
    """
    roadmap, test_strategy, extraction = input_paths

    # Include original source inputs so the LLM can validate coverage
    all_inputs = list(input_paths)
    for f in (spec_file, tdd_file, prd_file):
        if f is not None:
            all_inputs.append(f)

    # Parallel reflection steps (one per agent)
    reflect_steps = []
    reflect_outputs = []
    for agent in config.agents:
        output = validate_dir / f"reflect-{agent.id}.md"
        reflect_outputs.append(output)
        reflect_steps.append(
            Step(
                id=f"reflect-{agent.id}",
                prompt=build_reflect_prompt(
                    str(roadmap),
                    str(test_strategy),
                    str(extraction),
                    spec_file=str(spec_file) if spec_file else None,
                    tdd_file=str(tdd_file) if tdd_file else None,
                    prd_file=str(prd_file) if prd_file else None,
                ),
                output_file=output,
                gate=REFLECT_GATE,
                timeout_seconds=600,
                inputs=all_inputs,
                retry_limit=1,
                model=agent.model,
            ),
        )

    # Adversarial merge step
    merge_step = Step(
        id="adversarial-merge",
        prompt=build_merge_prompt([str(p) for p in reflect_outputs]),
        output_file=validate_dir / "validation-report.md",
        gate=ADVERSARIAL_MERGE_GATE,
        timeout_seconds=600,
        inputs=reflect_outputs,
        retry_limit=1,
    )

    return [
        reflect_steps,  # parallel group
        merge_step,  # sequential after all reflections
    ]


def _parse_report_counts(report_path: Path) -> dict:
    """Parse blocking/warning/info counts from a validation report's frontmatter.

    Returns dict with blocking_count, warning_count, info_count.
    Falls back to 0 for any unparseable field.
    """
    result = {"blocking_count": 0, "warning_count": 0, "info_count": 0}

    if not report_path.exists():
        return result

    content = report_path.read_text(encoding="utf-8")
    if not content.startswith("---"):
        return result

    end_idx = content.find("\n---", 3)
    if end_idx == -1:
        return result

    frontmatter = content[3:end_idx]
    for line in frontmatter.splitlines():
        line = line.strip()
        if ":" not in line:
            continue
        key, _, val = line.partition(":")
        key = key.strip()
        val = val.strip()
        if key == "blocking_issues_count":
            try:
                result["blocking_count"] = int(val)
            except ValueError:
                pass
        elif key == "warnings_count":
            try:
                result["warning_count"] = int(val)
            except ValueError:
                pass

    # Count INFO findings from body
    body = content[end_idx + 4 :]  # skip closing ---
    info_count = 0
    for line in body.splitlines():
        if "[INFO]" in line:
            info_count += 1
    result["info_count"] = info_count

    return result


def _write_degraded_report(
    report_path: Path,
    failed_ids: list[str],
    passed_ids: list[str],
) -> None:
    """Write a degraded validation report when multi-agent validation partially fails.

    The report is unmistakably marked as incomplete:
    - YAML frontmatter with ``validation_complete: false``
    - Prominent warning banner naming failed agent(s)
    - Per OQ-2: "Silent degradation is unacceptable."
    """
    failed_list = ", ".join(failed_ids)
    passed_list = ", ".join(passed_ids) if passed_ids else "none"

    content = (
        "---\n"
        "validation_complete: false\n"
        "blocking_issues_count: 0\n"
        "warnings_count: 0\n"
        f"failed_agents: {failed_list}\n"
        f"passed_agents: {passed_list}\n"
        "---\n"
        "\n"
        "> **WARNING: DEGRADED VALIDATION REPORT**\n"
        ">\n"
        f"> The following validation agent(s) FAILED: **{failed_list}**\n"
        ">\n"
        "> This report is INCOMPLETE. Findings from failed agents are missing.\n"
        "> Re-run validation to obtain a complete report.\n"
        "\n"
        "## Status\n"
        "\n"
        "This is a degraded validation report produced because one or more\n"
        "validation agents failed during multi-agent validation.\n"
        "\n"
        f"- **Failed agents:** {failed_list}\n"
        f"- **Passed agents:** {passed_list}\n"
        "\n"
        "## Findings\n"
        "\n"
        "No consolidated findings available due to partial agent failure.\n"
        "Individual reflection files from successful agents (if any) are\n"
        "preserved in the validate/ directory.\n"
    )

    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(content, encoding="utf-8")
    _log.warning("Wrote degraded validation report to %s", report_path)


def execute_validate(config: ValidateConfig) -> dict:
    """Execute the validation pipeline.

    Reads 3 required pipeline output files (roadmap.md, test-strategy.md,
    extraction.md) and resolves original source inputs (spec, TDD, PRD)
    from .roadmap-state.json.  When source inputs are available, the
    reflect prompt includes Coverage and Proportionality dimensions that
    validate the roadmap against the actual input -- not just the extraction.

    Parameters
    ----------
    config:
        ValidateConfig with output_dir (containing pipeline outputs)
        and agents list (1 agent = single mode, N = multi-agent).

    Returns
    -------
    dict with keys:
        blocking_count: int -- total BLOCKING findings
        warning_count: int -- total WARNING findings
        info_count: int -- total INFO findings

    Raises
    ------
    FileNotFoundError
        If any of the 3 required pipeline output files is missing.
    """
    # Validate pipeline outputs exist; resolve source inputs from state
    pipeline_paths, spec_file, tdd_file, prd_file = _validate_input_files(
        config.output_dir
    )

    # Create validate/ subdirectory
    validate_dir = config.output_dir / "validate"
    validate_dir.mkdir(parents=True, exist_ok=True)

    source_kwargs = dict(spec_file=spec_file, tdd_file=tdd_file, prd_file=prd_file)

    # Route by agent count
    if len(config.agents) == 1:
        steps = _build_single_agent_steps(
            config, validate_dir, pipeline_paths, **source_kwargs
        )
    else:
        steps = _build_multi_agent_steps(
            config, validate_dir, pipeline_paths, **source_kwargs
        )

    # Execute pipeline
    results = execute_pipeline(
        steps=steps,
        config=config,
        run_step=validate_run_step,
    )

    # Check for failures and handle partial failure in multi-agent mode
    failures = [r for r in results if r.status in (StepStatus.FAIL, StepStatus.TIMEOUT)]
    report_path = validate_dir / "validation-report.md"

    if failures and len(config.agents) > 1:
        # Partial failure: some agents may have succeeded
        failed_ids = [r.step.id for r in failures if r.step]
        passed_ids = [
            r.step.id for r in results if r.status == StepStatus.PASS and r.step
        ]
        _log.error(
            "Validation partial failure: passed=%s, failed=%s",
            passed_ids,
            failed_ids,
        )
        _write_degraded_report(report_path, failed_ids, passed_ids)
    elif failures:
        _log.error(
            "Validation pipeline halted: %d step(s) failed",
            len(failures),
        )

    return _parse_report_counts(report_path)
