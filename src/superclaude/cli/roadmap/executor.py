"""Roadmap executor -- orchestrates the 9-step roadmap pipeline.

Builds the step list with parallel generate group, defines
``roadmap_run_step`` as the StepRunner, and delegates to
``execute_pipeline()`` from the pipeline module.

Context isolation: each subprocess receives only its prompt via inline embedding.
No --continue, --session, --resume, or --file flags are passed (FR-003, FR-023).
--file is a cloud download mechanism and does not inject local file content.
"""

from __future__ import annotations

import dataclasses
import hashlib
import json
import logging
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable

from ..pipeline.deliverables import decompose_deliverables
from ..pipeline.executor import execute_pipeline
from ..pipeline.models import Deliverable, GateMode, PipelineConfig, Step, StepResult, StepStatus
from ..pipeline.process import ClaudeProcess
from ...compression import compress_file
from .gates import (
    ANTI_INSTINCT_GATE,
    CERTIFY_GATE,
    DEBATE_GATE,
    DEVIATION_ANALYSIS_GATE,
    DIFF_GATE,
    EXTRACT_GATE,
    EXTRACT_TDD_GATE,
    GENERATE_A_GATE,
    GENERATE_B_GATE,
    MERGE_GATE,
    REMEDIATE_GATE,
    SCORE_GATE,
    SPEC_FIDELITY_GATE,
    TEST_STRATEGY_GATE,
)
from ..audit.wiring_gate import WIRING_GATE
from .models import AgentSpec, RoadmapConfig
from .templates import ROADMAP_TEMPLATE, get_template_path
from .prompts import (
    build_debate_prompt,
    build_diff_prompt,
    build_extract_prompt,
    build_extract_prompt_tdd,
    build_generate_prompt,
    build_merge_prompt,
    build_score_prompt,
    build_spec_fidelity_prompt,
    build_test_strategy_prompt,
    build_wiring_verification_prompt,
    wrap_for_incremental_write,
)
from .certify_prompts import build_certification_prompt

_log = logging.getLogger("superclaude.roadmap.executor")


def detect_input_type(spec_file: Path) -> str:
    """Auto-detect whether an input file is a PRD, TDD, or spec.

    Uses multiple weighted signals — not dependent on any single field.

    PRD signals (checked first, threshold >= 5):
    1. Frontmatter type field containing "Product Requirements" (+3)
    2. 12 PRD-exclusive section headings (+1 each)
    3. User story pattern "As .+, I want" (+2)
    4. JTBD pattern "When I .+ I want to" (+2)
    5. prd tag in frontmatter (+2)

    TDD signals (checked second, threshold >= 5):
    1. Numbered section headings (## N. ) — TDDs have ~28, specs have ~12
    2. TDD-exclusive frontmatter fields (parent_doc, coordinator)
    3. TDD-specific section names (Data Models, API Specifications, etc.)
    4. Frontmatter type field containing "Technical Design Document"

    Returns "prd", "tdd", or "spec".
    """
    try:
        content = spec_file.read_text(encoding="utf-8", errors="replace")
    except (OSError, UnicodeDecodeError):
        return "spec"  # fallback to spec on read failure

    import re

    # ── PRD scoring (checked first) ──────────────────────────────────
    prd_score = 0

    # PRD Signal 1: Frontmatter type field (+3)
    if "Product Requirements" in content[:1000]:
        prd_score += 3

    # PRD Signal 2: 12 PRD-exclusive section headings (+1 each)
    prd_sections = [
        "User Personas", "Jobs To Be Done", "Product Vision",
        "Customer Journey", "Value Proposition", "Competitive Analysis",
        "User Stories", "User Experience Requirements",
        "Legal and Compliance", "Success Metrics and Measurement",
        "Maintenance and Ownership", "Background and Strategic Fit",
    ]
    for section in prd_sections:
        if section in content:
            prd_score += 1

    # PRD Signal 3: User story pattern (+2)
    if re.search(r"As .+, I want", content):
        prd_score += 2

    # PRD Signal 4: JTBD pattern (+2)
    if re.search(r"When I .+ I want to", content):
        prd_score += 2

    # PRD Signal 5: prd tag in frontmatter (+2)
    if re.search(r"tags:.*\bprd\b", content[:2000]):
        prd_score += 2

    if prd_score >= 5:
        _log.info("Auto-detected input type: prd (prd_score=%d)", prd_score)
        if 3 <= prd_score <= 6:
            _log.warning(
                "Borderline PRD detection score (%d) for %s — result=prd. "
                "Use --input-type to override if incorrect.",
                prd_score, spec_file,
            )
        return "prd"

    # ── TDD scoring (checked second) ─────────────────────────────────
    score = 0

    # Signal 1: Numbered section headings (## N. pattern)
    # TDDs have ~28 numbered sections; specs have ~12.
    # Threshold raised: >=20 is strong TDD signal, >=15 is moderate.
    # >=10 gets only +1 to avoid false positives from spec templates.
    numbered_headings = len(re.findall(r"^## \d+\.", content, re.MULTILINE))
    if numbered_headings >= 20:
        score += 3  # strong signal — only TDDs have this many
    elif numbered_headings >= 15:
        score += 2
    elif numbered_headings >= 10:
        score += 1  # weak — specs can have 12

    # Signal 2: TDD-exclusive frontmatter fields
    # Only count fields that specs do NOT typically have.
    # Removed feature_id, authors, quality_scores — the release-spec-template
    # also has these fields, causing false positives.
    tdd_exclusive_fields = ["parent_doc", "coordinator"]
    for field in tdd_exclusive_fields:
        if re.search(rf"^{field}:", content, re.MULTILINE):
            score += 2  # higher weight since these are truly TDD-exclusive

    # Signal 3: TDD-specific section names (8 keywords, +1 each)
    # These are section headings found in TDDs but not in specs or PRDs.
    # A typical TDD matches 5-8 of these; a spec matches 0-1.
    tdd_sections = [
        "Data Models", "API Specifications", "Component Inventory",
        "Testing Strategy", "Operational Readiness",
        "State Management", "Performance Budgets", "Accessibility Requirements",
    ]
    for section in tdd_sections:
        if section in content:
            score += 1

    # Signal 4: Frontmatter type field
    if "Technical Design Document" in content[:1000]:
        score += 2

    # Threshold: score >= 5 means TDD
    # Max possible: 3 (headings) + 4 (2 exclusive fields × 2) + 8 (section names) + 2 (type field) = 17
    # A real TDD easily scores 10+ (20+ headings=3, parent_doc+coordinator=4,
    # 5-8 section names, type field=2). A spec scores at most 1-3
    # (10-12 headings=1, no exclusive fields=0, no TDD sections=0).
    detected = "tdd" if score >= 5 else "spec"
    _log.info("Auto-detected input type: %s (score=%d)", detected, score)
    # C-103: Borderline warning for documents near the threshold
    if 3 <= score <= 6:
        _log.warning(
            "Borderline TDD detection score (%d) for %s — result=%s. "
            "Use --input-type to override if incorrect.",
            score, spec_file, detected,
        )
    return detected


def _route_input_files(
    input_files: tuple[Path, ...],
    explicit_tdd: Path | None,
    explicit_prd: Path | None,
    explicit_input_type: str,
) -> dict:
    """Route N positional files + explicit flags into pipeline slots.

    Returns dict with keys: spec_file, tdd_file, prd_file, input_type.
    Raises click.UsageError on validation failures.
    """
    import click

    # 1. Validate count
    if len(input_files) == 0:
        raise click.UsageError("At least one input file required.")
    if len(input_files) > 3:
        raise click.UsageError(
            f"Expected 1-3 input files, got {len(input_files)}. "
            "Provide at most one spec, one TDD, and one PRD."
        )

    # 3. Classify each file
    classifications: dict[Path, str] = {}
    for f in input_files:
        classifications[f] = detect_input_type(f)

    # 4. Apply explicit override for single-file mode
    if explicit_input_type != "auto" and len(input_files) == 1:
        classifications[input_files[0]] = explicit_input_type
    elif explicit_input_type != "auto" and len(input_files) > 1:
        _log.warning(
            "--input-type is ignored for multi-file mode; "
            "each file is classified by content."
        )

    # 5. Validate no duplicates
    type_counts: dict[str, list[Path]] = {}
    for f, t in classifications.items():
        type_counts.setdefault(t, []).append(f)
    for t, files in type_counts.items():
        if len(files) > 1:
            names = ", ".join(str(f) for f in files)
            raise click.UsageError(
                f"Multiple files detected as {t}: {names}. "
                "Use --input-type to disambiguate."
            )

    # 6. Validate primary input exists
    has_spec = "spec" in type_counts
    has_tdd = "tdd" in type_counts
    has_prd = "prd" in type_counts
    if not has_spec and not has_tdd:
        if has_prd:
            raise click.UsageError(
                "PRD cannot be the sole primary input; "
                "provide a spec or TDD file."
            )
        raise click.UsageError("No primary input (spec or TDD) detected.")

    # 7. Assign slots
    spec_file: Path
    tdd_file: Path | None = None
    prd_file: Path | None = None

    if has_spec:
        spec_file = type_counts["spec"][0]
        if has_tdd:
            tdd_file = type_counts["tdd"][0]
    else:
        # TDD becomes primary when no spec exists
        spec_file = type_counts["tdd"][0]

    if has_prd:
        prd_file = type_counts["prd"][0]

    # 8. Merge explicit flags (check conflicts first)
    if explicit_tdd is not None:
        if tdd_file is not None:
            raise click.UsageError(
                "--tdd-file conflicts with positional file detected as TDD; "
                "remove one."
            )
        tdd_file = explicit_tdd

    if explicit_prd is not None:
        if prd_file is not None:
            raise click.UsageError(
                "--prd-file conflicts with positional file detected as PRD; "
                "remove one."
            )
        prd_file = explicit_prd

    # 9. Determine input_type
    resolved_input_type: str
    if has_spec:
        resolved_input_type = "spec"
    else:
        resolved_input_type = "tdd"
    # Single-file explicit override already applied in step 4 via classifications
    if explicit_input_type != "auto" and len(input_files) == 1:
        resolved_input_type = explicit_input_type

    # 10. Redundancy guard
    if resolved_input_type == "tdd" and tdd_file is not None:
        _log.warning(
            "Ignoring --tdd-file: primary input is already a TDD document."
        )
        tdd_file = None

    # 11. Same-file guard
    pairs = [
        (spec_file, tdd_file, "spec_file", "tdd_file"),
        (spec_file, prd_file, "spec_file", "prd_file"),
        (tdd_file, prd_file, "tdd_file", "prd_file"),
    ]
    for a, b, name_a, name_b in pairs:
        if a is not None and b is not None and a.resolve() == b.resolve():
            raise click.UsageError(
                f"{name_a} and {name_b} point to the same file: {a}"
            )

    # 12. Return
    return {
        "spec_file": spec_file,
        "tdd_file": tdd_file,
        "prd_file": prd_file,
        "input_type": resolved_input_type,
    }


# Token-context advisory threshold (soft warning, non-fatal).
# Prompts are delivered to `claude` via stdin (see ClaudeProcess.start), so the
# Linux MAX_ARG_STRLEN = 128 KB kernel ceiling no longer applies. This threshold
# only surfaces prompts large enough to strain the model's context window.
_LARGE_PROMPT_WARN_BYTES = 500 * 1024  # 500 KB


def _compressed_sidecar(original: Path, output_dir: Path) -> Path:
    """Return the compressed-sidecar path for *original* inside *output_dir*.

    The sidecar uses the original stem plus a ``.compressed.md`` suffix so
    reviewers can visually pair the original and compressed artifacts.
    """
    return output_dir / f"{original.stem}.compressed.md"


def _gate_target(output_file: Path) -> Path:
    """Resolve the file path that gate checks should run against.

    Prefers the adjacent ``*.compressed.md`` sidecar so gate enforcement
    matches what downstream LLM steps actually consume. Falls back to the
    original path when no sidecar exists (compression disabled, step
    produces no sidecar, or deterministic tests that write only originals).
    """
    sidecar = output_file.with_name(f"{output_file.stem}.compressed.md")
    if sidecar != output_file and sidecar.exists():
        return sidecar
    return output_file


def _compress_for_llm(
    original: Path,
    doc_type: str,
    output_dir: Path,
) -> Path:
    """Compress *original* for LLM consumption and return the sidecar path.

    Uses lossless strategies only (``aggressive=False``). Idempotent: safe to
    call repeatedly; the sidecar is overwritten each time.
    """
    sidecar = _compressed_sidecar(original, output_dir)
    compress_file(original, doc_type, sidecar, aggressive=False)
    return sidecar


def _compress_pipeline_input(
    path: Path,
    doc_type: str,
    output_dir: Path,
) -> Path:
    """Compress a user-supplied pipeline input (spec/TDD/PRD) up-front.

    Writes the ``.compressed.md`` sidecar next to the roadmap output dir so
    downstream LLM steps consume the smaller variant via ``Step.inputs``. On
    compression failure, mirrors the original bytes into the sidecar so
    ``step.inputs`` still resolves to a readable file.
    """
    try:
        sidecar = _compress_for_llm(path, doc_type, output_dir)
        _log.info("Compressed %s input for LLM steps: %s", doc_type, sidecar)
        return sidecar
    except Exception as exc:  # noqa: BLE001 — degrade gracefully, never abort
        _log.warning(
            "%s compression failed (%s); mirroring original bytes to sidecar.",
            doc_type,
            exc,
        )
        sidecar = _compressed_sidecar(path, output_dir)
        sidecar.parent.mkdir(parents=True, exist_ok=True)
        sidecar.write_bytes(path.read_bytes())
        return sidecar


def _llm_inputs_for(
    config: RoadmapConfig,
    *candidates: Path,
) -> list[Path]:
    """Map LLM step inputs to compressed sidecars when compression is enabled.

    Roadmap-pipeline artifacts (spec, generated variants, merge) and
    user-supplied TDD/PRD inputs are rerouted to their ``.compressed.md``
    sidecars so every LLM step consumes the smaller variant. Extraction
    metadata and other intermediate files pass through unchanged.
    Deterministic steps never call this helper — they always read originals
    to preserve exact string/ID matching.
    """
    if not config.compress_enabled:
        return [p for p in candidates if p is not None]

    # The set of pipeline artifacts that have compressed sidecars. Variant
    # roadmap paths are derived from the agent IDs so we compute them here
    # rather than hard-coding filenames.
    rerouteable: set[Path] = {config.spec_file}
    if config.tdd_file is not None:
        rerouteable.add(config.tdd_file)
    if config.prd_file is not None:
        rerouteable.add(config.prd_file)
    for agent in config.agents:
        rerouteable.add(config.output_dir / f"roadmap-{agent.id}.md")
    rerouteable.add(config.output_dir / "roadmap.md")

    out: list[Path] = []
    for p in candidates:
        if p is None:
            continue
        if p in rerouteable:
            out.append(_compressed_sidecar(p, config.output_dir))
        else:
            out.append(p)
    return out


def _ensure_sidecars_present(
    inputs: list[Path],
    config: RoadmapConfig,
) -> None:
    """Regenerate any missing ``.compressed.md`` sidecars in *inputs* in place.

    ``_llm_inputs_for`` reroutes rerouteable paths to their compressed
    sidecars at plan-build time. The sidecars are normally produced by the
    up-front pipeline-input compression pass (for spec/TDD/PRD) or by the
    post-step hook (for generate-*/merge outputs). When a prior session is
    interrupted between writing the original and its sidecar -- or the hook
    silently failed to land the sidecar -- the next step that consumes that
    input would fail with ``FileNotFoundError``. This helper repairs that
    state just-in-time: if the sidecar's original exists but the sidecar
    does not, it rebuilds the sidecar (falling back to mirroring the
    original bytes on compression failure, same guarantee as
    ``_compress_pipeline_input``).

    No-op when ``compress_enabled`` is false or when no inputs are
    rerouteable sidecars.
    """
    if not config.compress_enabled:
        return

    # Mirror the routing table used by ``_llm_inputs_for`` so we can recover
    # the original path and doc_type from a sidecar alone. Spec/TDD/PRD
    # originals typically live outside ``output_dir``, so their real path
    # cannot be derived from the sidecar's stem.
    recovery: dict[Path, tuple[Path, str]] = {
        _compressed_sidecar(config.spec_file, config.output_dir): (config.spec_file, "spec"),
    }
    if config.tdd_file is not None:
        recovery[_compressed_sidecar(config.tdd_file, config.output_dir)] = (
            config.tdd_file,
            "spec",
        )
    if config.prd_file is not None:
        recovery[_compressed_sidecar(config.prd_file, config.output_dir)] = (
            config.prd_file,
            "spec",
        )
    for agent in config.agents:
        variant = config.output_dir / f"roadmap-{agent.id}.md"
        recovery[_compressed_sidecar(variant, config.output_dir)] = (variant, "roadmap")
    merge = config.output_dir / "roadmap.md"
    recovery[_compressed_sidecar(merge, config.output_dir)] = (merge, "roadmap")

    for sidecar in inputs:
        if sidecar is None:
            continue
        if sidecar.exists():
            continue
        entry = recovery.get(sidecar)
        if entry is None:
            continue
        original, doc_type = entry
        if not original.exists():
            # Nothing to recover from; let the downstream read fail loudly
            # with the original path so the user sees which artifact is gone.
            continue
        try:
            _compress_for_llm(original, doc_type, config.output_dir)
            _log.info(
                "Self-healed missing sidecar %s from %s", sidecar, original,
            )
        except Exception as exc:  # noqa: BLE001 — degrade gracefully
            _log.warning(
                "Self-heal compression of %s failed (%s); "
                "mirroring original bytes to sidecar.",
                original,
                exc,
            )
            sidecar.parent.mkdir(parents=True, exist_ok=True)
            sidecar.write_bytes(original.read_bytes())


def _embed_inputs(
    input_paths: list[Path],
    labels: dict[Path, str] | None = None,
) -> str:
    """Read input files and return their contents as fenced code blocks.

    Each file is wrapped in a fenced block with a header. When *labels*
    is provided, the header includes the semantic role (e.g., "Primary
    input - tdd", "PRD - supplementary business context") so the LLM
    knows which file serves which purpose.

    Returns an empty string when *input_paths* is empty (no-op).
    """
    if not input_paths:
        return ""

    blocks: list[str] = []
    for p in input_paths:
        label = labels.get(p, str(p)) if labels else str(p)
        content = Path(p).read_text(encoding="utf-8")
        blocks.append(f"# {label}\n```\n{content}\n```")
    return "\n\n".join(blocks)


def _sanitize_output(output_file: Path) -> int:
    """Strip conversational preamble and leading blank lines before YAML
    frontmatter in a step output file.

    Reads the file, strips leading blank lines, finds the first ``^---``
    line, and removes everything before it.  Uses atomic write (write to
    ``.tmp`` then ``os.replace()``) to prevent partial file states.

    Returns the byte count of the stripped content (0 when file already
    starts with ``---`` and has no preamble).
    """
    import os
    import re

    try:
        raw = output_file.read_text(encoding="utf-8")
    except FileNotFoundError:
        return 0

    # Strip leading blank lines (LLMs sometimes emit \n\n before ---)
    content = raw.lstrip("\n\r\t ")

    # Already starts with frontmatter delimiter -- no preamble to strip
    if content.startswith("---"):
        if content == raw:
            return 0
        # Leading whitespace only -- write back the stripped version
        preamble_bytes = len(raw.encode("utf-8")) - len(content.encode("utf-8"))
        tmp_file = output_file.with_suffix(output_file.suffix + ".tmp")
        tmp_file.write_text(content, encoding="utf-8")
        os.replace(tmp_file, output_file)
        _log.info(
            "Stripped %d-byte leading whitespace from %s",
            preamble_bytes,
            output_file,
        )
        return preamble_bytes

    # Search for the first ^--- line (conversational preamble case)
    match = re.search(r"^---[ \t]*$", content, re.MULTILINE)
    if match is None:
        # No frontmatter found at all -- leave file unchanged
        return 0

    preamble = content[: match.start()]
    cleaned = content[match.start():]
    # Total bytes stripped = leading whitespace + conversational preamble
    preamble_bytes = len(raw.encode("utf-8")) - len(cleaned.encode("utf-8"))

    # Atomic write: tmp file + os.replace
    tmp_file = output_file.with_suffix(output_file.suffix + ".tmp")
    tmp_file.write_text(cleaned, encoding="utf-8")
    os.replace(tmp_file, output_file)

    _log.info("Stripped %d-byte preamble from %s", preamble_bytes, output_file)
    return preamble_bytes


def _inject_pipeline_diagnostics(
    output_file: Path,
    started_at: datetime,
    finished_at: datetime,
) -> None:
    """Inject executor-populated pipeline_diagnostics into extraction frontmatter.

    The LLM cannot reliably produce execution timing or environment metadata,
    so the executor injects these fields post-subprocess (FR-033).
    """
    content = output_file.read_text(encoding="utf-8").lstrip("\n\r\t ")
    if not content.startswith("---"):
        return

    # Find end of frontmatter
    end_idx = content.find("\n---", 3)
    if end_idx == -1:
        return

    # Idempotency: skip if already injected
    frontmatter = content[3:end_idx]
    if "pipeline_diagnostics:" in frontmatter:
        return

    elapsed = (finished_at - started_at).total_seconds()
    diagnostics_line = (
        f"pipeline_diagnostics: "
        f"{{elapsed_seconds: {elapsed:.1f}, "
        f'started_at: "{started_at.isoformat()}", '
        f'finished_at: "{finished_at.isoformat()}"}}'
    )

    # Insert before the closing ---
    new_content = content[:end_idx] + "\n" + diagnostics_line + content[end_idx:]
    output_file.write_text(new_content, encoding="utf-8")


def _inject_provenance_fields(
    output_file: Path,
    spec_source: str,
) -> None:
    """Inject provenance fields into test-strategy frontmatter.

    The test-strategy step's LLM output may omit provenance metadata
    (spec_source, generated, generator) since the prompt focuses on
    test strategy content. The executor injects these fields post-subprocess
    to satisfy TEST_STRATEGY_GATE required_frontmatter_fields.
    """
    content = output_file.read_text(encoding="utf-8").lstrip("\n\r\t ")
    if not content.startswith("---"):
        return

    # Find end of frontmatter
    end_idx = content.find("\n---", 3)
    if end_idx == -1:
        return

    # Idempotency: only inject fields that are missing
    frontmatter = content[3:end_idx]

    fields_to_inject = []
    if "spec_source:" not in frontmatter:
        fields_to_inject.append(f"spec_source: {spec_source}")
    if "generated:" not in frontmatter:
        generated = datetime.now(timezone.utc).isoformat()
        fields_to_inject.append(f'generated: "{generated}"')
    if "generator:" not in frontmatter:
        fields_to_inject.append("generator: superclaude-roadmap-executor")

    if not fields_to_inject:
        return  # All fields already present

    provenance_block = "\n".join(fields_to_inject)
    new_content = content[:end_idx] + "\n" + provenance_block + content[end_idx:]
    output_file.write_text(new_content, encoding="utf-8")


def _run_structural_audit(
    spec_file: Path,
    extraction_file: Path,
) -> None:
    """Run structural audit as warning-only hook after EXTRACT_GATE pass (FR-EXEC.1).

    Compares spec structural indicators against extraction requirement count.
    Logs a warning if extraction appears inadequate but never blocks the pipeline.
    """
    from .spec_structural_audit import check_extraction_adequacy
    from .gates import _parse_frontmatter

    try:
        spec_text = spec_file.read_text(encoding="utf-8")
        extraction_text = extraction_file.read_text(encoding="utf-8")
    except (FileNotFoundError, OSError) as e:
        _log.warning("Structural audit skipped: %s", e)
        return

    fm = _parse_frontmatter(extraction_text)
    if fm is None:
        _log.warning("Structural audit skipped: no frontmatter in extraction")
        return

    try:
        total_req = int(fm.get("total_requirements", "0"))
    except (ValueError, TypeError):
        _log.warning("Structural audit skipped: unparseable total_requirements")
        return

    passed, audit = check_extraction_adequacy(spec_text, total_req)
    if not passed:
        _log.warning(
            "Structural audit WARNING: extraction may be inadequate. "
            "Spec structural indicators=%d, extraction total_requirements=%d",
            audit.total_structural_indicators,
            total_req,
        )
        print(
            f"[roadmap] WARNING: Structural audit indicates possible extraction gap "
            f"(indicators={audit.total_structural_indicators}, requirements={total_req})",
            flush=True,
        )


def _run_anti_instinct_audit(
    spec_file: Path,
    roadmap_file: Path,
    output_file: Path,
) -> None:
    """Run the three anti-instinct detection modules and write audit report (FR-EXEC.3).

    Invokes obligation scanner, integration contract checker, and fingerprint
    coverage checker deterministically (no LLM). Writes anti-instinct-audit.md
    with YAML frontmatter and markdown report body.
    """
    from .obligation_scanner import scan_obligations
    from .integration_contracts import extract_integration_contracts, check_roadmap_coverage
    from .fingerprint import check_fingerprint_coverage

    try:
        spec_text = spec_file.read_text(encoding="utf-8")
        roadmap_text = roadmap_file.read_text(encoding="utf-8")
    except (FileNotFoundError, OSError) as e:
        _log.error("Anti-instinct audit failed: %s", e)
        raise

    # Module 1: Obligation scanner
    obligation_report = scan_obligations(roadmap_text)

    # Module 2: Integration contract checker
    contracts = extract_integration_contracts(spec_text)
    contract_result = check_roadmap_coverage(contracts, roadmap_text)

    # Module 3: Fingerprint coverage
    fp_total, fp_found, fp_missing, fp_ratio = check_fingerprint_coverage(
        spec_text, roadmap_text
    )

    # Build YAML frontmatter
    generated = datetime.now(timezone.utc).isoformat()
    frontmatter = (
        "---\n"
        f"undischarged_obligations: {obligation_report.undischarged_count}\n"
        f"uncovered_contracts: {contract_result.uncovered_count}\n"
        f"fingerprint_coverage: {fp_ratio:.2f}\n"
        f"total_obligations: {obligation_report.total_obligations}\n"
        f"total_contracts: {contract_result.total_count}\n"
        f"fingerprint_total: {fp_total}\n"
        f"fingerprint_found: {fp_found}\n"
        f'generated: "{generated}"\n'
        "generator: superclaude-anti-instinct-audit\n"
        "---\n"
    )

    # Build markdown body
    body_parts = [
        "\n## Anti-Instinct Audit Report\n",
        f"### Obligation Scanner\n\n"
        f"- Total obligations detected: {obligation_report.total_obligations}\n"
        f"- Discharged: {obligation_report.discharged}\n"
        f"- Undischarged (gate-relevant): {obligation_report.undischarged_count}\n",
    ]

    if obligation_report.undischarged_count > 0:
        body_parts.append("\n**Undischarged obligations:**\n")
        for o in obligation_report.obligations:
            if not o.discharged and not o.exempt and o.severity != "MEDIUM":
                body_parts.append(
                    f"- Line {o.line_number}: `{o.term}` in {o.phase} "
                    f"({o.component})\n"
                )

    body_parts.append(
        f"\n### Integration Contract Coverage\n\n"
        f"- Total contracts: {contract_result.total_count}\n"
        f"- Covered: {contract_result.total_count - contract_result.uncovered_count}\n"
        f"- Uncovered: {contract_result.uncovered_count}\n"
    )

    if contract_result.uncovered_count > 0:
        body_parts.append("\n**Uncovered contracts:**\n")
        for cov in contract_result.coverage:
            if not cov.covered:
                body_parts.append(
                    f"- {cov.contract.id}: {cov.contract.description} "
                    f"({cov.contract.spec_location})\n"
                )

    body_parts.append(
        f"\n### Fingerprint Coverage\n\n"
        f"- Total fingerprints: {fp_total}\n"
        f"- Found in roadmap: {fp_found}\n"
        f"- Coverage ratio: {fp_ratio:.2f}\n"
    )

    if fp_missing:
        body_parts.append(
            f"\n**Missing fingerprints** ({len(fp_missing)}):\n"
        )
        for name in fp_missing[:20]:  # cap at 20 for readability
            body_parts.append(f"- `{name}`\n")
        if len(fp_missing) > 20:
            body_parts.append(f"- ... and {len(fp_missing) - 20} more\n")

    content = frontmatter + "".join(body_parts)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(content, encoding="utf-8")

    _log.info(
        "Anti-instinct audit complete: obligations=%d/%d uncovered_contracts=%d "
        "fingerprint_coverage=%.2f",
        obligation_report.undischarged_count,
        obligation_report.total_obligations,
        contract_result.uncovered_count,
        fp_ratio,
    )


_MERGE_TAIL_SECTIONS = (
    "## Risk Register",
    "## Success Criteria and Validation Approach",
    "## Decision Summary",
    "## Timeline Estimates",
)


def _validate_merge_completeness(output_file: Path) -> list[str]:
    """Inspect a merge-step output file and return a list of missing or
    schema-violating items.

    An empty list means the file is structurally complete. The merge step
    writes section-by-section via tool calls and can be silently truncated
    if the LLM's turn budget runs out mid-sequence; callers use this list
    to fail the step and trigger retry.

    Checks performed:

    - Every ``## M{N}:`` milestone declared in the Milestone Summary table
      has a corresponding body section.
    - Required tail headings are present (Risk Register, Success
      Criteria, Decision Summary, Timeline Estimates).
    - Each milestone body has the 9-column deliverable table header,
      ``### Integration Points — M{N}`` and
      ``### Milestone Dependencies — M{N}``.
    - No row in any 9-column deliverable table has an ``OQ-xxx`` value
      in the ``ID`` column (OQs are decisions, not deliverables).
    - If the frontmatter ``open_questions:`` count is > 0 but no
      ``### Open Questions — M{N}`` subsection appears anywhere, flag it.
    - No global ``## Open Questions`` heading at the document tail.
    """
    import re

    try:
        text = output_file.read_text(encoding="utf-8")
    except FileNotFoundError:
        return [f"output file '{output_file}' does not exist"]

    missing: list[str] = []

    # Extract milestone IDs from the Milestone Summary table. Each row
    # begins with "| M{N} |" — we gather every such ID to cross-check
    # against body sections.
    summary_ids = set(re.findall(r"^\|\s*(M\d+)\s*\|", text, re.MULTILINE))
    body_ids = set(re.findall(r"^##\s+(M\d+):", text, re.MULTILINE))
    for mid in sorted(summary_ids, key=lambda s: int(s[1:])):
        if mid not in body_ids:
            missing.append(f"milestone body section '## {mid}:' missing")

    # Required tail headings
    for heading in _MERGE_TAIL_SECTIONS:
        if heading not in text:
            missing.append(f"tail section '{heading}' missing")

    # Per-milestone required subsections and deliverable-table presence
    for mid in sorted(body_ids, key=lambda s: int(s[1:])):
        if f"### Integration Points — {mid}" not in text:
            missing.append(f"'### Integration Points — {mid}' missing")
        if f"### Milestone Dependencies — {mid}" not in text:
            missing.append(f"'### Milestone Dependencies — {mid}' missing")

    # OQ-xxx anti-rule: no OQ-xxx rows in the 9-column deliverable table.
    # The schema is `| # | ID | Title | Description | Comp | Deps | AC | Eff | Pri |`
    # (10 pipes per row). The per-milestone `### Open Questions — M{N}`
    # subsection table has only 6 columns (7 pipes), so we match only
    # rows with at least 7 more pipes after the ID column.
    oq_row_re = re.compile(
        r"^\|\s*\d+\s*\|\s*(OQ-\d+)\s*\|(?:[^\n|]*\|){7,}",
        re.MULTILINE,
    )
    oq_rows = oq_row_re.findall(text)
    if oq_rows:
        missing.append(
            "deliverable table contains OQ-xxx rows (OQs must live in "
            f"per-milestone subsections only): {sorted(set(oq_rows))}"
        )

    # Global Open Questions section is forbidden
    if re.search(r"^##\s+Open Questions\s*$", text, re.MULTILINE):
        missing.append(
            "global '## Open Questions' section present — OQs must be "
            "per-milestone subsections only"
        )

    # Frontmatter OQ count vs presence of any per-milestone subsection
    fm_match = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
    if fm_match is not None:
        oq_count_match = re.search(
            r"^open_questions:\s*(\d+)\s*$",
            fm_match.group(1),
            re.MULTILINE,
        )
        if oq_count_match and int(oq_count_match.group(1)) > 0:
            if not re.search(
                r"^###\s+Open Questions\s+—\s+M\d+\s*$",
                text,
                re.MULTILINE,
            ):
                missing.append(
                    "frontmatter declares open_questions > 0 but no "
                    "'### Open Questions — M{N}' subsection is present"
                )

    return missing


def roadmap_run_step(
    step: Step,
    config: PipelineConfig,
    cancel_check: Callable[[], bool],
) -> StepResult:
    """Execute a single roadmap step as a Claude subprocess.

    Builds argv with context isolation, launches process, waits with
    timeout, and returns StepResult.
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

    # Anti-instinct: run deterministic audit directly, no Claude subprocess.
    # Gate evaluation happens via ANTI_INSTINCT_GATE in execute_pipeline.
    if step.id == "anti-instinct":
        spec_file = config.spec_file if hasattr(config, 'spec_file') else None
        merge_file = config.output_dir / "roadmap.md" if hasattr(config, 'output_dir') else None
        if spec_file and merge_file:
            _run_anti_instinct_audit(spec_file, merge_file, step.output_file)
        return StepResult(
            step=step,
            status=StepStatus.PASS,
            attempt=1,
            started_at=started_at,
            finished_at=datetime.now(timezone.utc),
        )

    # Spec-fidelity in convergence mode: run convergence engine instead of LLM.
    # Structural checkers -> semantic layer -> convergence evaluation -> remediation.
    if step.id == "spec-fidelity" and hasattr(config, "convergence_enabled") and config.convergence_enabled:
        return _run_convergence_spec_fidelity(step, config, started_at)

    # Deviation-analysis: run deterministic analysis directly, no Claude subprocess.
    if step.id == "deviation-analysis":
        return _run_deviation_analysis(step, config, started_at)

    # Remediate: run remediation pipeline directly, no Claude subprocess.
    if step.id == "remediate":
        return _run_remediate_step(step, config, started_at)

    # Wiring-verification: run static analysis directly, no Claude subprocess.
    # Returns PASS unconditionally; gate evaluation is handled separately by
    # the trailing gate runner (section 5.7.1).
    if step.id == "wiring-verification":
        from ..audit.wiring_gate import run_wiring_analysis, emit_report
        from ..audit.wiring_config import WiringConfig

        wiring_config = WiringConfig(rollout_mode="soft")
        source_dir = Path("src/superclaude") if Path("src/superclaude").exists() else Path(".")
        report = run_wiring_analysis(wiring_config, source_dir)
        step.output_file.parent.mkdir(parents=True, exist_ok=True)
        emit_report(report, step.output_file)
        return StepResult(
            step=step,
            status=StepStatus.PASS,
            attempt=1,
            started_at=started_at,
            finished_at=datetime.now(timezone.utc),
        )

    # Inline embedding: read input files into the prompt instead of --file flags
    # --file is broken (cloud download mechanism, not local file injector) so
    # inline embedding is always used regardless of composed prompt size.
    # Build semantic role labels so the LLM knows which file is which (C-25).
    labels: dict[Path, str] | None = None
    if isinstance(config, RoadmapConfig):
        labels = {}
        if config.spec_file:
            labels[config.spec_file] = f"{config.spec_file} [Primary input - {config.input_type}]"
            # When compression is enabled, step.inputs references the compressed
            # sidecar instead of the original spec. Label it with the same
            # semantic role so the LLM still knows this is the primary input.
            if config.compress_enabled:
                spec_cmp = _compressed_sidecar(config.spec_file, config.output_dir)
                labels[spec_cmp] = (
                    f"{spec_cmp} [Primary input - {config.input_type}, compressed]"
                )
        if config.tdd_file:
            labels[config.tdd_file] = f"{config.tdd_file} [TDD - supplementary technical context]"
            if config.compress_enabled:
                tdd_cmp = _compressed_sidecar(config.tdd_file, config.output_dir)
                labels[tdd_cmp] = (
                    f"{tdd_cmp} [TDD - supplementary technical context, compressed]"
                )
        if config.prd_file:
            labels[config.prd_file] = f"{config.prd_file} [PRD - supplementary business context]"
            if config.compress_enabled:
                prd_cmp = _compressed_sidecar(config.prd_file, config.output_dir)
                labels[prd_cmp] = (
                    f"{prd_cmp} [PRD - supplementary business context, compressed]"
                )
    if isinstance(config, RoadmapConfig):
        _ensure_sidecars_present(step.inputs, config)
    embedded = _embed_inputs(step.inputs, labels=labels)
    if embedded:
        composed = step.prompt + "\n\n" + embedded
        if len(composed.encode("utf-8")) > _LARGE_PROMPT_WARN_BYTES:
            _log.warning(
                "Step '%s': composed prompt is %d bytes (> %d); may strain model context window",
                step.id,
                len(composed.encode("utf-8")),
                _LARGE_PROMPT_WARN_BYTES,
            )
        effective_prompt = composed
        extra_args: list[str] = []
    else:
        effective_prompt = step.prompt
        extra_args = []

    # Wrap prompt for incremental writing when tool_write_mode is enabled
    if step.tool_write_mode:
        effective_prompt = wrap_for_incremental_write(
            effective_prompt,
            output_path=step.output_file,
            template_path=step.template_path,
        )

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
        tool_write_mode=step.tool_write_mode,
    )

    proc.start()

    # Poll for cancellation while waiting
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

    # tool_write_mode: validate the LLM wrote the output file via tools
    if step.tool_write_mode:
        if not proc.validate_tool_write_output():
            return StepResult(
                step=step,
                status=StepStatus.FAIL,
                attempt=1,
                gate_failure_reason=(
                    f"Step '{step.id}' tool_write_mode: output file "
                    f"'{step.output_file}' missing or empty after subprocess exit"
                ),
                started_at=started_at,
                finished_at=finished_at,
            )

        # Merge step: the LLM writes the final roadmap section-by-section
        # via incremental Edit calls. If its turn budget runs out before
        # the tail sections land, validate_tool_write_output() accepts the
        # partial file (non-empty). _validate_merge_completeness() catches
        # the truncation and structural violations so the retry machinery
        # can re-run the step instead of silently passing.
        if step.id == "merge":
            missing = _validate_merge_completeness(step.output_file)
            if missing:
                return StepResult(
                    step=step,
                    status=StepStatus.FAIL,
                    attempt=1,
                    gate_failure_reason=(
                        f"Step '{step.id}' output is structurally "
                        f"incomplete; retry will regenerate. Missing: "
                        + "; ".join(missing)
                    ),
                    started_at=started_at,
                    finished_at=finished_at,
                )
    else:
        # Sanitize output: strip conversational preamble before gate validation
        _sanitize_output(step.output_file)

    # Inject executor-populated fields into extract step frontmatter (FR-033)
    if step.id == "extract" and step.output_file.exists():
        _inject_pipeline_diagnostics(step.output_file, started_at, finished_at)
        # FR-EXEC.1: Structural audit hook (warning-only, never blocks)
        # NOTE: _run_structural_audit() is warning-only and uses spec heading patterns.
        # TDD heading structure differs (28 numbered sections vs spec FR/NFR headings).
        # Do not rely on structural audit results for TDD correctness.
        # See open question C-2 (structural_checkers.py investigation needed).
        if hasattr(config, 'spec_file'):
            _run_structural_audit(config.spec_file, step.output_file)

    # Inject provenance fields into test-strategy output
    if step.id == "test-strategy" and step.output_file.exists():
        spec_source = (
            config.spec_file.name if hasattr(config, "spec_file") else "unknown"
        )
        _inject_provenance_fields(step.output_file, spec_source)

    # Post-step compression: build a sidecar for artifacts that downstream LLM
    # steps consume via Step.inputs. Gate checks run on the ORIGINAL output
    # file (which is preserved unchanged); only the sidecar is derived here.
    # Downstream Step.inputs reference the sidecar path, so on compression
    # failure we mirror the original bytes into the sidecar to keep the
    # pipeline runnable.
    if (
        isinstance(config, RoadmapConfig)
        and config.compress_enabled
        and step.output_file.exists()
        and (step.id.startswith("generate-") or step.id == "merge")
    ):
        try:
            sidecar = _compress_for_llm(step.output_file, "roadmap", config.output_dir)
            _log.info("Compressed %s output: %s", step.id, sidecar)
        except Exception as exc:
            _log.warning(
                "Compression of %s output failed (%s); mirroring original to "
                "sidecar path so downstream steps can still read it.",
                step.id, exc,
            )
            sidecar = _compressed_sidecar(step.output_file, config.output_dir)
            sidecar.parent.mkdir(parents=True, exist_ok=True)
            sidecar.write_bytes(step.output_file.read_bytes())

    # Process completed successfully; gate check happens in execute_pipeline
    return StepResult(
        step=step,
        status=StepStatus.PASS,
        attempt=1,
        started_at=started_at,
        finished_at=finished_at,
    )


def _run_convergence_spec_fidelity(
    step: Step,
    config: RoadmapConfig,
    started_at: datetime,
) -> StepResult:
    """Run spec-fidelity via convergence engine (FR-7).

    Wires: structural checkers -> semantic layer -> convergence engine -> remediation.
    Steps 1-7 and step 9 are unaffected by convergence mode.

    This replaces the single-shot LLM call for spec-fidelity when
    convergence_enabled=True.
    """
    from .convergence import (
        DeviationRegistry,
        ConvergenceResult,
        execute_fidelity_with_convergence,
        handle_regression,
    )
    from .structural_checkers import run_all_checkers
    from .semantic_layer import run_semantic_layer
    from .remediate_executor import execute_remediation
    from .fidelity_checker import run_fidelity_check

    spec_path = config.spec_file
    roadmap_path = config.output_dir / "roadmap.md"

    # Initialize registry and ledger
    spec_hash = hashlib.sha256(spec_path.read_bytes()).hexdigest()
    registry = DeviationRegistry.load_or_create(
        config.output_dir / "deviation-registry.json",
        release_id=config.output_dir.name,
        spec_hash=spec_hash,
    )

    # Get TurnLedger from sprint models
    try:
        from ..sprint.models import TurnLedger
        from .convergence import MAX_CONVERGENCE_BUDGET, CHECKER_COST, REMEDIATION_COST
        ledger = TurnLedger(
            initial_budget=MAX_CONVERGENCE_BUDGET,
            minimum_allocation=CHECKER_COST,
            minimum_remediation_budget=REMEDIATION_COST,
            reimbursement_rate=0.8,
        )
    except ImportError:
        _log.warning("TurnLedger not available; convergence engine may not function")
        return StepResult(
            step=step,
            status=StepStatus.FAIL,
            attempt=1,
            gate_failure_reason="TurnLedger import failed",
            started_at=started_at,
            finished_at=datetime.now(timezone.utc),
        )

    def _run_checkers(reg: DeviationRegistry, run_number: int) -> None:
        """Run structural checkers + semantic layer + fidelity checker, merge into registry."""
        structural_findings = run_all_checkers(str(spec_path), str(roadmap_path))
        reg.merge_findings(structural_findings, [], run_number)

        # Run semantic layer if Claude is available
        try:
            semantic_result = run_semantic_layer(
                spec_path=str(spec_path),
                roadmap_path=str(roadmap_path),
                output_dir=config.output_dir,
                structural_findings=structural_findings,
                registry=reg,
            )
            if semantic_result and semantic_result.findings:
                reg.merge_findings([], semantic_result.findings, run_number)
        except Exception as exc:
            _log.warning("Semantic layer failed: %s (continuing with structural only)", exc)

        # Run fidelity checker (FR-5.2): verify spec FRs have codebase evidence
        try:
            source_dir = Path("src/superclaude") if Path("src/superclaude").exists() else Path(".")
            fidelity_findings = run_fidelity_check(
                spec_path=str(spec_path),
                source_dir=str(source_dir),
            )
            if fidelity_findings:
                reg.merge_findings(fidelity_findings, [], run_number)
                _log.info("Fidelity checker found %d implementation gaps", len(fidelity_findings))
        except Exception as exc:
            _log.warning("Fidelity checker failed: %s (continuing without fidelity layer)", exc)

    def _run_remediation(reg: DeviationRegistry) -> None:
        """Run remediation on active HIGH findings."""
        from .models import Finding
        active_highs = reg.get_active_highs()
        if not active_highs:
            return

        # Convert registry dicts to Finding dataclass instances
        # (registry stores JSON dicts, execute_remediation expects Finding objects)
        finding_objects = []
        for d in active_highs:
            finding_objects.append(Finding(
                id=d.get("stable_id", ""),
                severity=d.get("severity", "HIGH"),
                dimension=d.get("dimension", ""),
                description=d.get("description", ""),
                location=d.get("location", ""),
                evidence="",
                fix_guidance="",
                files_affected=d.get("files_affected", []),
                status=d.get("status", "ACTIVE"),
            ))

        # Group by file using Finding objects
        findings_by_file: dict[str, list] = {}
        for finding in finding_objects:
            for f in finding.files_affected:
                findings_by_file.setdefault(f, []).append(finding)

        execute_remediation(
            findings_by_file=findings_by_file,
            config=config,
            output_dir=config.output_dir,
            allow_regeneration=getattr(config, "allow_regeneration", False),
        )

    result = execute_fidelity_with_convergence(
        registry=registry,
        ledger=ledger,
        run_checkers=_run_checkers,
        run_remediation=_run_remediation,
        handle_regression_fn=handle_regression,
        max_runs=3,
        spec_path=spec_path,
        roadmap_path=roadmap_path,
    )

    finished_at = datetime.now(timezone.utc)

    # Write convergence result to spec-fidelity output file
    _write_convergence_report(step.output_file, result, registry)

    status = StepStatus.PASS if result.passed else StepStatus.FAIL
    gate_reason = None if result.passed else (result.halt_reason or "Convergence did not pass")

    return StepResult(
        step=step,
        status=status,
        attempt=1,
        gate_failure_reason=gate_reason,
        started_at=started_at,
        finished_at=finished_at,
    )


def _write_convergence_report(
    output_file: Path,
    result,
    registry,
) -> None:
    """Write a spec-fidelity report from convergence results."""
    output_file.parent.mkdir(parents=True, exist_ok=True)

    high_count = result.final_high_count
    passed = result.passed

    lines = [
        "---",
        f"high_severity_count: {high_count}",
        "medium_severity_count: 0",
        "low_severity_count: 0",
        f"total_deviations: {high_count}",
        f"validation_complete: {'true' if passed else 'false'}",
        f"tasklist_ready: {'true' if passed else 'false'}",
        "---",
        "",
        "# Spec Fidelity Report (Convergence Mode)",
        "",
        f"**Convergence Result**: {'PASS' if passed else 'FAIL'}",
        f"**Runs Completed**: {result.run_count}",
        f"**Final HIGH Count**: {high_count}",
        "",
    ]

    if result.structural_progress_log:
        lines.append("## Structural Progress")
        for entry in result.structural_progress_log:
            lines.append(f"- {entry}")
        lines.append("")

    if result.halt_reason:
        lines.append("## Halt Reason")
        lines.append(result.halt_reason)
        lines.append("")

    output_file.write_text("\n".join(lines), encoding="utf-8")


def _run_deviation_analysis(
    step: Step,
    config: PipelineConfig,
    started_at: datetime,
) -> StepResult:
    """Execute deviation-analysis step deterministically (no Claude subprocess).

    Reads the DeviationRegistry from the output directory, aggregates findings
    by deviation_class, validates cross-field consistency, and writes
    gate-compliant output (.md with YAML frontmatter and .json sidecar).
    """
    out = config.output_dir if hasattr(config, "output_dir") else Path(".")
    registry_json = out / "deviation-registry.json"

    try:
        if registry_json.exists():
            raw = json.loads(registry_json.read_text(encoding="utf-8"))
            records = raw if isinstance(raw, list) else raw.get("findings", [])
        else:
            records = []

        # Aggregate by deviation_class
        slip_count = sum(1 for r in records if r.get("deviation_class") == "SLIP")
        intentional_count = sum(1 for r in records if r.get("deviation_class") == "INTENTIONAL")
        pre_approved_count = sum(1 for r in records if r.get("deviation_class") == "PRE_APPROVED")
        ambiguous_count = sum(1 for r in records if r.get("deviation_class") == "AMBIGUOUS")
        total_analyzed = slip_count + intentional_count + pre_approved_count + ambiguous_count

        # Build routing lists
        import re
        routing_fix = [r.get("stable_id") or r.get("id", "") for r in records if r.get("deviation_class") == "SLIP"]
        routing_no_action = [r.get("stable_id") or r.get("id", "") for r in records if r.get("deviation_class") == "PRE_APPROVED"]

        routing_fix_str = ", ".join(routing_fix) if routing_fix else ""
        routing_no_action_str = ", ".join(routing_no_action) if routing_no_action else ""

        # Validate cross-field consistency before writing
        if total_analyzed != len(routing_fix) + len(routing_no_action) + intentional_count + ambiguous_count:
            _log.warning("Deviation analysis: cross-field consistency check failed")

        _write_deviation_analysis_output(
            step.output_file,
            total_analyzed=total_analyzed,
            slip_count=slip_count,
            intentional_count=intentional_count,
            pre_approved_count=pre_approved_count,
            ambiguous_count=ambiguous_count,
            routing_fix_roadmap=routing_fix_str,
            routing_no_action=routing_no_action_str,
            records=records,
        )

        return StepResult(
            step=step,
            status=StepStatus.PASS,
            attempt=1,
            started_at=started_at,
            finished_at=datetime.now(timezone.utc),
        )
    except Exception as exc:
        _log.error("Deviation analysis failed: %s", exc)
        return StepResult(
            step=step,
            status=StepStatus.FAIL,
            attempt=1,
            gate_failure_reason=f"Deviation analysis error: {exc}",
            started_at=started_at,
            finished_at=datetime.now(timezone.utc),
        )


def _write_deviation_analysis_output(
    output_file: Path,
    *,
    total_analyzed: int,
    slip_count: int,
    intentional_count: int,
    pre_approved_count: int,
    ambiguous_count: int,
    routing_fix_roadmap: str,
    routing_no_action: str,
    records: list[dict],
) -> None:
    """Write gate-compliant spec-deviations.md and .json sidecar."""
    import os

    # Build markdown with YAML frontmatter
    lines = [
        "---",
        "schema_version: 1",
        f"total_analyzed: {total_analyzed}",
        f"slip_count: {slip_count}",
        f"intentional_count: {intentional_count}",
        f"pre_approved_count: {pre_approved_count}",
        f"ambiguous_count: {ambiguous_count}",
        f"ambiguous_deviations: {ambiguous_count}",
        f"routing_fix_roadmap: {routing_fix_roadmap}",
        f"routing_no_action: {routing_no_action}",
        "analysis_complete: true",
        "---",
        "",
        "# Deviation Analysis Report",
        "",
        f"Total deviations analyzed: {total_analyzed}",
        f"- SLIP: {slip_count}",
        f"- INTENTIONAL: {intentional_count}",
        f"- PRE_APPROVED: {pre_approved_count}",
        f"- AMBIGUOUS: {ambiguous_count}",
        "",
    ]

    if records:
        lines.append("## Deviation Details")
        lines.append("")
        for r in records:
            dev_id = r.get("stable_id") or r.get("id", "UNKNOWN")
            dev_class = r.get("deviation_class", "UNCLASSIFIED")
            desc = r.get("description", "")
            lines.append(f"### {dev_id} [{dev_class}]")
            lines.append(f"- Description: {desc}")
            lines.append(f"- Location: {r.get('location', '')}")
            lines.append("")

    output_file.parent.mkdir(parents=True, exist_ok=True)

    # Write .md
    md_content = "\n".join(lines)
    tmp_md = output_file.with_suffix(".md.tmp")
    tmp_md.write_text(md_content, encoding="utf-8")
    os.replace(str(tmp_md), str(output_file))

    # Write .json sidecar
    json_file = output_file.with_suffix(".json")
    sidecar = {
        "schema_version": 1,
        "total_analyzed": total_analyzed,
        "slip_count": slip_count,
        "intentional_count": intentional_count,
        "pre_approved_count": pre_approved_count,
        "ambiguous_count": ambiguous_count,
        "routing_fix_roadmap": routing_fix_roadmap,
        "routing_no_action": routing_no_action,
        "records": records,
    }
    tmp_json = json_file.with_suffix(".json.tmp")
    tmp_json.write_text(json.dumps(sidecar, indent=2), encoding="utf-8")
    os.replace(str(tmp_json), str(json_file))


def _run_remediate_step(
    step: Step,
    config: PipelineConfig,
    started_at: datetime,
) -> StepResult:
    """Execute remediate step: read deviation JSON, generate tasklist.

    Reads spec-deviations.json sidecar, converts to Finding objects,
    generates remediation tasklist, writes .md and .json sidecar.
    """
    from .remediate import deviations_to_findings, generate_remediation_tasklist

    out = config.output_dir if hasattr(config, "output_dir") else Path(".")
    deviation_json = out / "spec-deviations.json"

    try:
        if deviation_json.exists():
            raw = json.loads(deviation_json.read_text(encoding="utf-8"))
            records = raw.get("records", []) if isinstance(raw, dict) else raw
        else:
            records = []

        findings = deviations_to_findings(records)

        # Read source report for hash
        source_report_path = str(out / "spec-fidelity.md")
        try:
            source_report_content = Path(source_report_path).read_text(encoding="utf-8")
        except OSError:
            source_report_content = ""

        tasklist_md = generate_remediation_tasklist(
            findings, source_report_path, source_report_content
        )

        step.output_file.parent.mkdir(parents=True, exist_ok=True)

        # Write .md
        import os
        tmp_md = step.output_file.with_suffix(".md.tmp")
        tmp_md.write_text(tasklist_md, encoding="utf-8")
        os.replace(str(tmp_md), str(step.output_file))

        # Write .json sidecar
        json_file = step.output_file.with_suffix(".json")
        sidecar = {
            "findings": [
                {
                    "id": f.id,
                    "severity": f.severity,
                    "description": f.description,
                    "location": f.location,
                    "fix_guidance": f.fix_guidance,
                    "files_affected": f.files_affected,
                    "status": f.status,
                    "deviation_class": f.deviation_class,
                }
                for f in findings
            ]
        }
        tmp_json = json_file.with_suffix(".json.tmp")
        tmp_json.write_text(json.dumps(sidecar, indent=2), encoding="utf-8")
        os.replace(str(tmp_json), str(json_file))

        return StepResult(
            step=step,
            status=StepStatus.PASS,
            attempt=1,
            started_at=started_at,
            finished_at=datetime.now(timezone.utc),
        )
    except Exception as exc:
        _log.error("Remediate step failed: %s", exc)
        return StepResult(
            step=step,
            status=StepStatus.FAIL,
            attempt=1,
            gate_failure_reason=f"Remediate error: {exc}",
            started_at=started_at,
            finished_at=datetime.now(timezone.utc),
        )


def build_certify_step(
    config: RoadmapConfig,
    findings: list | None = None,
    context_sections: dict[str, str] | None = None,
) -> Step:
    """Build a certify Step for execution via execute_pipeline().

    The certify step runs as a standard Step (not ClaudeProcess directly)
    per spec section 2.5. It uses CERTIFY_GATE for output validation.

    Parameters
    ----------
    config:
        RoadmapConfig with output_dir.
    findings:
        List of Finding objects to certify. If None, an empty prompt is built.
    context_sections:
        Pre-extracted context sections per finding location (NFR-011).
    """
    from .models import Finding

    out = config.output_dir
    certification_report = out / "certification-report.md"

    prompt = build_certification_prompt(
        findings=findings or [],
        context_sections=context_sections or {},
    )

    return Step(
        id="certify",
        prompt=prompt,
        output_file=certification_report,
        gate=CERTIFY_GATE,
        timeout_seconds=300,
        inputs=[out / "remediation-tasklist.md"],
        retry_limit=1,
    )


def _build_steps(config: RoadmapConfig) -> list[Step | list[Step]]:
    """Build the 9-step pipeline with parallel generate group.

    Returns a list where each element is either a single Step (sequential)
    or a list[Step] (parallel group).
    """
    out = config.output_dir

    # Agent specs
    agent_a = config.agents[0]
    agent_b = config.agents[1] if len(config.agents) > 1 else config.agents[0]

    # Output paths
    extraction = out / "extraction.md"
    roadmap_a = out / f"roadmap-{agent_a.id}.md"
    roadmap_b = out / f"roadmap-{agent_b.id}.md"
    diff_file = out / "diff-analysis.md"
    debate_file = out / "debate-transcript.md"
    score_file = out / "base-selection.md"
    merge_file = out / "roadmap.md"
    test_strat = out / "test-strategy.md"
    spec_fidelity_file = out / "spec-fidelity.md"
    deviation_file = out / "spec-deviations.md"
    remediation_file = out / "remediation-tasklist.md"
    certification_file = out / "certification-report.md"

    # Resolve roadmap template for incremental-write steps
    try:
        _roadmap_template = get_template_path(ROADMAP_TEMPLATE)
    except FileNotFoundError:
        _roadmap_template = None

    # Load retrospective content if configured (missing file handled gracefully)
    retrospective_content: str | None = None
    if config.retrospective_file is not None and config.retrospective_file.is_file():
        try:
            retrospective_content = config.retrospective_file.read_text(
                encoding="utf-8"
            )
        except OSError:
            retrospective_content = None

    # When the primary input is itself a TDD, config.tdd_file is None (see
    # _route_input_files redundancy guard). Treat config.spec_file as the
    # effective TDD for LLM prompt builders that gate TDD-specific sections on
    # `tdd_file is not None`, so the TDD-aware blocks still fire when the TDD
    # is the sole input. Also used to ensure the raw TDD reaches step inputs
    # where needed (e.g., generate step, which otherwise only sees extraction).
    effective_tdd_file = config.tdd_file if config.tdd_file is not None else (
        config.spec_file if config.input_type == "tdd" else None
    )

    steps: list[Step | list[Step]] = [
        # Step 1: Extract
        # TDD input routing: --input-type tdd uses dedicated TDD extraction sections
        Step(
            id="extract",
            prompt=(
                build_extract_prompt_tdd(
                    config.spec_file,
                    retrospective_content=retrospective_content,
                    tdd_file=config.tdd_file,
                    prd_file=config.prd_file,
                )
                if config.input_type == "tdd"
                else build_extract_prompt(
                    config.spec_file,
                    retrospective_content=retrospective_content,
                    tdd_file=config.tdd_file,
                    prd_file=config.prd_file,
                )
            ),
            output_file=extraction,
            gate=EXTRACT_TDD_GATE if config.input_type == "tdd" else EXTRACT_GATE,
            timeout_seconds=1800 if config.input_type == "tdd" else 300,
            inputs=_llm_inputs_for(config, config.spec_file, config.tdd_file, config.prd_file),
            retry_limit=1,
        ),
        # Steps 2a+2b: Generate (parallel)
        [
            Step(
                id=f"generate-{agent_a.id}",
                prompt=build_generate_prompt(agent_a, extraction, tdd_file=effective_tdd_file, prd_file=config.prd_file),
                output_file=roadmap_a,
                gate=GENERATE_A_GATE,
                timeout_seconds=900,
                inputs=[extraction] + _llm_inputs_for(config, effective_tdd_file, config.prd_file),
                retry_limit=1,
                model=agent_a.model,
                tool_write_mode=_roadmap_template is not None,
                template_path=_roadmap_template,
            ),
            Step(
                id=f"generate-{agent_b.id}",
                prompt=build_generate_prompt(agent_b, extraction, tdd_file=effective_tdd_file, prd_file=config.prd_file),
                output_file=roadmap_b,
                gate=GENERATE_B_GATE,
                timeout_seconds=900,
                inputs=[extraction] + _llm_inputs_for(config, effective_tdd_file, config.prd_file),
                retry_limit=1,
                model=agent_b.model,
                tool_write_mode=_roadmap_template is not None,
                template_path=_roadmap_template,
            ),
        ],
        # Step 3: Diff
        Step(
            id="diff",
            prompt=build_diff_prompt(roadmap_a, roadmap_b),
            output_file=diff_file,
            gate=DIFF_GATE,
            timeout_seconds=300,
            inputs=_llm_inputs_for(config, roadmap_a, roadmap_b),
            retry_limit=1,
        ),
        # Step 4: Debate
        Step(
            id="debate",
            prompt=build_debate_prompt(diff_file, roadmap_a, roadmap_b, config.depth),
            output_file=debate_file,
            gate=DEBATE_GATE,
            timeout_seconds=600,
            inputs=[diff_file] + _llm_inputs_for(config, roadmap_a, roadmap_b),
            retry_limit=1,
        ),
        # Step 5: Score
        Step(
            id="score",
            prompt=build_score_prompt(debate_file, roadmap_a, roadmap_b, tdd_file=effective_tdd_file, prd_file=config.prd_file),
            output_file=score_file,
            gate=SCORE_GATE,
            timeout_seconds=300,
            inputs=[debate_file] + _llm_inputs_for(config, roadmap_a, roadmap_b, effective_tdd_file, config.prd_file),
            retry_limit=1,
        ),
        # Step 6: Merge
        Step(
            id="merge",
            prompt=build_merge_prompt(score_file, roadmap_a, roadmap_b, debate_file, tdd_file=effective_tdd_file, prd_file=config.prd_file),
            output_file=merge_file,
            gate=MERGE_GATE,
            timeout_seconds=600,
            inputs=[score_file] + _llm_inputs_for(config, roadmap_a, roadmap_b, effective_tdd_file, config.prd_file) + [debate_file],
            retry_limit=1,
            tool_write_mode=_roadmap_template is not None,
            template_path=_roadmap_template,
        ),
        # Step 7: Anti-Instinct Audit (non-LLM deterministic step)
        Step(
            id="anti-instinct",
            prompt="",  # non-LLM step; prompt unused
            output_file=out / "anti-instinct-audit.md",
            gate=ANTI_INSTINCT_GATE,
            timeout_seconds=30,
            inputs=[config.spec_file, merge_file],
            retry_limit=0,
        ),
        # Step 8: Test Strategy
        Step(
            id="test-strategy",
            prompt=build_test_strategy_prompt(merge_file, extraction, tdd_file=effective_tdd_file, prd_file=config.prd_file),
            output_file=test_strat,
            gate=TEST_STRATEGY_GATE,
            timeout_seconds=300,
            inputs=_llm_inputs_for(config, merge_file, effective_tdd_file, config.prd_file) + [extraction],
            retry_limit=1,
        ),
        # Step 8: Spec Fidelity (after test-strategy, FR-008 through FR-010)
        Step(
            id="spec-fidelity",
            prompt=build_spec_fidelity_prompt(config.spec_file, merge_file, tdd_file=effective_tdd_file, prd_file=config.prd_file),
            output_file=spec_fidelity_file,
            gate=None if config.convergence_enabled else SPEC_FIDELITY_GATE,
            timeout_seconds=600,
            inputs=_llm_inputs_for(config, config.spec_file, merge_file, config.tdd_file, config.prd_file),
            retry_limit=1,
        ),
        # Step 9: Wiring Verification (section 5.7, shadow mode trailing gate)
        Step(
            id="wiring-verification",
            prompt=build_wiring_verification_prompt(
                merge_file, config.spec_file.name
            ),
            output_file=out / "wiring-verification.md",
            gate=WIRING_GATE,
            timeout_seconds=60,
            inputs=_llm_inputs_for(config, merge_file) + [spec_fidelity_file],
            retry_limit=0,
            gate_mode=GateMode.TRAILING,
        ),
        # Step 10: Deviation Analysis (deterministic, no LLM)
        Step(
            id="deviation-analysis",
            prompt="",  # non-LLM step; prompt unused
            output_file=deviation_file,
            gate=DEVIATION_ANALYSIS_GATE,
            timeout_seconds=300,
            inputs=[spec_fidelity_file, merge_file],
            retry_limit=0,
        ),
        # Step 11: Remediate (deterministic, no LLM)
        Step(
            id="remediate",
            prompt="",  # non-LLM step; prompt unused
            output_file=remediation_file,
            gate=REMEDIATE_GATE,
            timeout_seconds=600,
            inputs=[deviation_file, spec_fidelity_file, merge_file],
            retry_limit=0,
        ),
        # Step 12 (certify) constructed dynamically by roadmap_run_step after remediate
    ]

    return steps


def _format_halt_output(results: list[StepResult], config: RoadmapConfig) -> str:
    """Format HALT diagnostic output per spec section 6.2."""
    failed = [r for r in results if r.status in (StepStatus.FAIL, StepStatus.TIMEOUT)]
    passed = [r for r in results if r.status == StepStatus.PASS]
    cancelled = [r for r in results if r.status == StepStatus.CANCELLED]

    if not failed:
        return ""

    fail = failed[-1]
    step = fail.step

    # Calculate file details if output exists
    file_info = ""
    if step and step.output_file.exists():
        content = step.output_file.read_text(encoding="utf-8")
        byte_count = len(content.encode("utf-8"))
        line_count = len(content.splitlines())
        file_info = f"  Output size: {byte_count} bytes ({line_count} lines)\n"
    elif step:
        file_info = "  Output file: not created\n"

    elapsed = f"{fail.duration_seconds:.0f}s"

    lines = [
        f"ERROR: Roadmap pipeline halted at step '{step.id}' (attempt {fail.attempt}/2)",
        f"  Gate failure: {fail.gate_failure_reason}",
        f"  Output file: {step.output_file}",
        file_info.rstrip(),
        f"  Step timeout: {step.timeout_seconds}s | Elapsed: {elapsed}",
        "",
        f"Completed steps: {', '.join(f'{r.step.id} (PASS, attempt {r.attempt})' for r in passed) or 'none'}",
        f"Failed step:     {step.id} ({fail.status.value}, attempt {fail.attempt})",
    ]

    # Collect skipped steps
    all_step_ids = _get_all_step_ids(config)
    executed_ids = {r.step.id for r in results}
    skipped_ids = [sid for sid in all_step_ids if sid not in executed_ids]
    if cancelled:
        skipped_ids = [r.step.id for r in cancelled] + skipped_ids

    if skipped_ids:
        lines.append(f"Skipped steps:   {', '.join(skipped_ids)}")

    lines.extend(
        [
            "",
            "To retry from this step:",
            f"  superclaude roadmap run {config.spec_file} --resume",
            "",
            "To inspect the failing output:",
            f"  cat {step.output_file}",
        ]
    )

    return "\n".join(lines)


def _get_all_step_ids(config: RoadmapConfig) -> list[str]:
    """Get all step IDs in pipeline order."""
    agent_a = config.agents[0]
    agent_b = config.agents[1] if len(config.agents) > 1 else config.agents[0]
    return [
        "extract",
        f"generate-{agent_a.id}",
        f"generate-{agent_b.id}",
        "diff",
        "debate",
        "score",
        "merge",
        "anti-instinct",
        "test-strategy",
        "spec-fidelity",
        "wiring-verification",
        "deviation-analysis",
        "remediate",
        "certify",
    ]


def _print_terminal_halt(
    output_dir: Path,
    remaining_findings: list,
    attempt_count: int,
    spec_patch_budget_exhausted: bool = False,
    file=None,
) -> None:
    """Print terminal halt message to stderr with finding details (SC-6).

    Outputs:
    - Attempt count and remaining failing finding count
    - Per-finding details (ID, severity, description)
    - Manual-fix instructions including certification report path and resume command

    Args:
        output_dir: Pipeline output directory (for certification report path)
        remaining_findings: List of Finding objects that failed remediation
        attempt_count: Number of remediation attempts made
        spec_patch_budget_exhausted: If True, note that spec-patch budget is also exhausted
        file: Output stream (defaults to sys.stderr)
    """
    if file is None:
        file = sys.stderr

    certify_path = output_dir / "certification-report.md"

    lines = [
        "",
        "=" * 72,
        "TERMINAL HALT: Remediation budget exhausted",
        "=" * 72,
        f"Attempt count: {attempt_count}",
        f"Remaining failing findings: {len(remaining_findings)}",
        "",
    ]

    if remaining_findings:
        lines.append("Failing findings:")
        for finding in remaining_findings:
            severity = getattr(finding, "severity", "UNKNOWN")
            description = getattr(finding, "description", "")
            finding_id = getattr(finding, "id", "UNKNOWN")
            lines.append(f"  - {finding_id} [{severity}]: {description}")
        lines.append("")

    lines.extend(
        [
            "Manual fix required:",
            f"  1. Review certification report: {certify_path}",
            "  2. Fix remaining findings manually",
            "  3. Resume pipeline with:",
            f"     superclaude roadmap run --resume",
            "",
        ]
    )

    if spec_patch_budget_exhausted:
        lines.extend(
            [
                "Note: Both the remediation budget and the spec-patch cycle budget",
                "are exhausted. Full dual-budget recovery is deferred to v2.26.",
                "# TODO(v2.26): implement dual-budget-exhaustion recovery mechanism",
                "",
            ]
        )

    lines.append("=" * 72)

    print("\n".join(lines), file=file, flush=True)


def _check_annotate_deviations_freshness(
    output_dir: Path,
    roadmap_file: Path,
    gate_pass_state: dict[str, bool] | None = None,
) -> bool:
    """Check if spec-deviations.md hash matches current roadmap.md (SC-8).

    Reads roadmap_hash from spec-deviations.md frontmatter and compares
    against sha256(roadmap.md). Fail-closed for all error conditions.

    On hash mismatch, resets spec-fidelity and deviation-analysis gate
    pass state to force re-run (FR-084).

    Returns:
        True if hash matches (fresh), False for any failure or mismatch.
    """
    spec_deviations = output_dir / "spec-deviations.md"

    # Case 1: spec-deviations.md not found
    if not spec_deviations.exists():
        _log.warning("Freshness check: spec-deviations.md not found")
        return False

    # Case 2: Read error
    try:
        content = spec_deviations.read_text(encoding="utf-8")
    except OSError as e:
        _log.warning("Freshness check: read error for spec-deviations.md: %s", e)
        return False

    # Case 3: Empty file
    if not content.strip():
        _log.warning("Freshness check: spec-deviations.md is empty")
        return False

    # Case 4: Corrupt/missing frontmatter
    stripped = content.lstrip()
    if not stripped.startswith("---"):
        _log.warning("Freshness check: spec-deviations.md has no frontmatter")
        return False

    rest = stripped[3:].lstrip("\n")
    end_idx = rest.find("\n---")
    if end_idx == -1:
        _log.warning("Freshness check: spec-deviations.md has corrupt frontmatter")
        return False

    # Parse roadmap_hash from frontmatter
    saved_hash: str | None = None
    for line in rest[:end_idx].splitlines():
        line = line.strip()
        if line.startswith("roadmap_hash:"):
            saved_hash = line.split(":", 1)[1].strip()
            break

    # Case 5: roadmap_hash field missing or empty
    if not saved_hash:
        _log.warning(
            "Freshness check: roadmap_hash field missing or empty in spec-deviations.md"
        )
        return False

    # Case 6: roadmap.md not found
    if not roadmap_file.exists():
        _log.warning("Freshness check: roadmap.md not found at %s", roadmap_file)
        return False

    # Case 7: roadmap.md read error
    try:
        roadmap_content = roadmap_file.read_bytes()
    except OSError as e:
        _log.warning("Freshness check: read error for roadmap.md: %s", e)
        return False

    # Case 8: Hash comparison
    current_hash = hashlib.sha256(roadmap_content).hexdigest()
    if saved_hash != current_hash:
        _log.warning(
            "Freshness check: hash mismatch -- saved=%s current=%s",
            saved_hash[:12],
            current_hash[:12],
        )
        # FR-084: reset gate pass state for downstream steps
        if gate_pass_state is not None:
            for key in ("spec-fidelity", "deviation-analysis"):
                if key in gate_pass_state:
                    gate_pass_state[key] = False
        return False

    return True


def _check_remediation_budget(
    output_dir: Path,
    max_attempts: int = 2,
) -> bool:
    """Check if remediation budget allows another attempt (SC-6).

    Reads remediation_attempts from .roadmap-state.json.
    If attempts >= max_attempts, calls _print_terminal_halt and returns False.

    Non-integer remediation_attempts is coerced to 0 with a WARNING log.

    Args:
        output_dir: Pipeline output directory containing .roadmap-state.json
        max_attempts: Maximum allowed remediation attempts (default 2)

    Returns:
        True if budget allows another attempt, False if exhausted.
    """
    state_file = output_dir / ".roadmap-state.json"
    state = read_state(state_file)

    attempts = 0
    if state is not None:
        raw = state.get("remediation_attempts", 0)
        try:
            attempts = int(raw)
        except (ValueError, TypeError):
            _log.warning("Non-integer remediation_attempts %r coerced to 0", raw)
            attempts = 0

    if attempts >= max_attempts:
        _print_terminal_halt(
            output_dir=output_dir,
            remaining_findings=[],
            attempt_count=attempts + 1,
        )
        return False

    return True


def _print_step_start(step: Step) -> None:
    """Print progress output when a step starts."""
    print(f"[roadmap] Starting step: {step.id}", flush=True)


def _print_step_complete(step: Step, result: StepResult) -> None:
    """Print progress output when a step completes."""
    duration = f"{result.duration_seconds:.0f}s"
    if result.status == StepStatus.PASS:
        print(
            f"[roadmap] Step {step.id}  PASS (attempt {result.attempt}, {duration})",
            flush=True,
        )
    else:
        print(
            f"[roadmap] Step {step.id}  {result.status.value} (attempt {result.attempt}, {duration})",
            flush=True,
        )
        if result.gate_failure_reason:
            print(f"           Reason: {result.gate_failure_reason}", flush=True)


def _dry_run_output(steps: list[Step | list[Step]]) -> None:
    """Print step plan and gate criteria for --dry-run."""
    step_num = 0
    for entry in steps:
        if isinstance(entry, list):
            for s in entry:
                step_num += 1
                _print_step_plan(step_num, s, parallel=True)
        else:
            step_num += 1
            _print_step_plan(step_num, entry)


def _print_step_plan(num: int, step: Step, parallel: bool = False) -> None:
    """Print a single step's plan entry."""
    par_label = " (parallel)" if parallel else ""
    print(f"Step {num}{par_label}: {step.id}")
    print(f"  Output: {step.output_file}")
    print(f"  Timeout: {step.timeout_seconds}s")
    if step.model:
        print(f"  Model: {step.model}")
    if step.gate:
        print(f"  Gate tier: {step.gate.enforcement_tier}")
        print(f"  Gate min_lines: {step.gate.min_lines}")
        if step.gate.required_frontmatter_fields:
            print(
                f"  Gate frontmatter: {', '.join(step.gate.required_frontmatter_fields)}"
            )
        if step.gate.semantic_checks:
            checks = [c.name for c in step.gate.semantic_checks]
            print(f"  Semantic checks: {', '.join(checks)}")
    print()


def _save_state(
    config: RoadmapConfig,
    results: list[StepResult],
    remediate_metadata: dict | None = None,
    certify_metadata: dict | None = None,
) -> None:
    """Write .roadmap-state.json to output_dir via atomic tmp + os.replace().

    Preserves existing ``validation``, ``fidelity_status``, ``remediate``,
    and ``certify`` keys if present. Accepts optional remediate/certify
    metadata dicts for Phase 6 state finalization.

    Defense-in-depth guards:
    - No-progress guard: skip write when no steps passed (prevents corruption
      from broken resumes that fail immediately).
    - Agent-mismatch guard: preserve original agents in state when no generate
      steps ran (prevents overwriting correct agent config with wrong agents).
    """
    state_file = config.output_dir / ".roadmap-state.json"

    # No-progress guard: if the results list is empty (no steps were even
    # attempted), do not write state. This prevents corruption from broken
    # resumes that produce zero results. Any non-empty results list indicates
    # the pipeline made progress and state should be recorded.
    step_results = [r for r in results if r.step]
    if not step_results:
        _log.info("State not saved: no step results in this run")
        return

    # Preserve existing keys across state rewrites
    existing = read_state(state_file)

    # Agent-mismatch guard: if agents differ from state and no generate steps
    # ran, preserve original agents to prevent corruption
    if existing is not None:
        saved_agents = existing.get("agents", [])
        current_agents = [
            {"model": a.model, "persona": a.persona} for a in config.agents
        ]
        if saved_agents and saved_agents != current_agents:
            generate_ran = any(
                r.step
                and r.step.id.startswith("generate-")
                and r.status == StepStatus.PASS
                for r in results
            )
            if not generate_ran:
                _log.warning(
                    "Agents differ from state file and no generate steps ran; "
                    "preserving original agents in state"
                )
                return

    existing_validation = existing.get("validation") if existing else None
    existing_fidelity = existing.get("fidelity_status") if existing else None
    existing_remediate = existing.get("remediate") if existing else None
    existing_certify = existing.get("certify") if existing else None

    spec_hash = hashlib.sha256(config.spec_file.read_bytes()).hexdigest()

    state = {
        "schema_version": 1,
        "spec_file": str(config.spec_file),
        "tdd_file": str(config.tdd_file) if config.tdd_file else None,
        "prd_file": str(config.prd_file) if config.prd_file else None,
        "input_type": config.input_type,
        "spec_hash": spec_hash,
        "agents": [{"model": a.model, "persona": a.persona} for a in config.agents],
        "depth": config.depth,
        "last_run": datetime.now(timezone.utc).isoformat(),
        "steps": {
            r.step.id: {
                "status": r.status.value,
                "attempt": r.attempt,
                "output_file": str(r.step.output_file),
                "started_at": r.started_at.isoformat(),
                "completed_at": r.finished_at.isoformat(),
            }
            for r in results
            if r.step
        },
    }

    # Merge with existing state (preserve steps not in this run)
    if existing:
        existing_steps = existing.get("steps", {})
        for step_id, step_data in existing_steps.items():
            if step_id not in state["steps"]:
                state["steps"][step_id] = step_data

    if existing_validation is not None:
        state["validation"] = existing_validation

    # Derive fidelity_status from spec-fidelity step result
    fidelity_result = next(
        (r for r in results if r.step and r.step.id == "spec-fidelity"),
        None,
    )
    if fidelity_result is not None:
        state["fidelity_status"] = _derive_fidelity_status(fidelity_result)
    elif existing_fidelity is not None:
        state["fidelity_status"] = existing_fidelity

    # Remediate metadata (spec §3.1)
    if remediate_metadata is not None:
        state["remediate"] = remediate_metadata
    elif existing_remediate is not None:
        state["remediate"] = existing_remediate

    # Certify metadata (spec §3.1)
    if certify_metadata is not None:
        state["certify"] = certify_metadata
    elif existing_certify is not None:
        state["certify"] = existing_certify

    write_state(state, state_file)


def _derive_fidelity_status(result: StepResult) -> str:
    """Derive fidelity_status enum from a spec-fidelity StepResult.

    Returns one of: 'pass', 'fail', 'skipped', 'degraded'.
    """
    if result.status == StepStatus.PASS:
        # Check if the output indicates degraded mode
        if result.step and result.step.output_file.exists():
            content = result.step.output_file.read_text(encoding="utf-8")
            if "validation_complete: false" in content:
                return "degraded"
        return "pass"
    if result.status == StepStatus.SKIPPED:
        return "skipped"
    if result.status in (StepStatus.FAIL, StepStatus.TIMEOUT):
        return "fail"
    return "skipped"


def generate_degraded_report(
    output_file: Path,
    failed_agent: str,
    failure_reason: str,
) -> None:
    """Generate a degraded fidelity report when the agent fails.

    Produces a report with validation_complete=false and
    fidelity_check_attempted=true so the SPEC_FIDELITY_GATE
    can distinguish degraded from clean passes (NFR-007).

    The degraded report names the failed agent and reason in the body.
    """
    report = (
        "---\n"
        "high_severity_count: 0\n"
        "medium_severity_count: 0\n"
        "low_severity_count: 0\n"
        "total_deviations: 0\n"
        "validation_complete: false\n"
        "fidelity_check_attempted: true\n"
        "tasklist_ready: false\n"
        "---\n"
        "\n"
        "## Degraded Fidelity Report\n"
        "\n"
        "Spec-fidelity validation could not be completed.\n"
        "\n"
        f"**Failed Agent**: {failed_agent}\n"
        f"**Failure Reason**: {failure_reason}\n"
        "\n"
        "This is a degraded report produced after agent failure and retry "
        "exhaustion. No deviations were analyzed. The pipeline continues "
        "in degraded mode with validation_complete=false.\n"
        "\n"
        "### Recommended Actions\n"
        "\n"
        "1. Investigate the agent failure\n"
        "2. Re-run the spec-fidelity step manually\n"
        "3. Review the roadmap against the specification\n"
    )
    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(report, encoding="utf-8")


def build_remediate_metadata(
    status: str,
    scope: str,
    findings_total: int,
    findings_actionable: int,
    findings_fixed: int,
    findings_failed: int,
    findings_skipped: int,
    agents_spawned: int,
    tasklist_file: str,
) -> dict:
    """Build remediate metadata dict for state schema §3.1.

    Parameters map 1:1 to .roadmap-state.json ``remediate`` entry fields.
    """
    return {
        "status": status,
        "scope": scope,
        "findings_total": findings_total,
        "findings_actionable": findings_actionable,
        "findings_fixed": findings_fixed,
        "findings_failed": findings_failed,
        "findings_skipped": findings_skipped,
        "agents_spawned": agents_spawned,
        "tasklist_file": tasklist_file,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


def build_certify_metadata(
    status: str,
    findings_verified: int,
    findings_passed: int,
    findings_failed: int,
    certified: bool,
    report_file: str,
) -> dict:
    """Build certify metadata dict for state schema §3.1.

    Parameters map 1:1 to .roadmap-state.json ``certify`` entry fields.
    """
    return {
        "status": status,
        "findings_verified": findings_verified,
        "findings_passed": findings_passed,
        "findings_failed": findings_failed,
        "certified": certified,
        "report_file": report_file,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


def derive_pipeline_status(state: dict) -> str:
    """Derive the overall pipeline status from state transitions.

    State transitions at each boundary:
    - post-validate: validated | validated-with-issues
    - post-remediate: remediated
    - post-certify: certified | certified-with-caveats

    Returns one of: 'pending', 'validated', 'validated-with-issues',
    'remediated', 'certified', 'certified-with-caveats'.
    """
    certify = state.get("certify")
    if certify is not None:
        if certify.get("certified", False):
            return "certified"
        return "certified-with-caveats"

    remediate = state.get("remediate")
    if remediate is not None:
        return "remediated"

    validation = state.get("validation")
    if validation is not None:
        if validation.get("status") == "pass":
            return "validated"
        if validation.get("status") == "fail":
            return "validated-with-issues"

    return "pending"


def write_state(state: dict, path: Path) -> None:
    """Write state dict to path atomically via tmp file + os.replace()."""
    import os as _os

    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(state, indent=2), encoding="utf-8")
    _os.replace(str(tmp), str(path))


def read_state(path: Path) -> dict | None:
    """Read state from path with graceful recovery on missing/malformed files."""
    if not path.exists():
        return None
    try:
        text = path.read_text(encoding="utf-8")
        if not text.strip():
            return None
        return json.loads(text)
    except (json.JSONDecodeError, OSError):
        return None


def apply_decomposition_pass(deliverables: list[Deliverable]) -> list[Deliverable]:
    """Post-generation decomposition pass for the roadmap pipeline.

    Runs after deliverable generation, before output formatting.
    Splits behavioral deliverables into Implement/Verify pairs.

    Idempotent: running twice produces identical results because
    already-decomposed deliverables (IDs ending .a/.b) are skipped.

    Preserves milestone-internal ordering: deliverables within each
    milestone maintain their relative order after decomposition.
    """
    return decompose_deliverables(deliverables)


def _restore_from_state(
    config: RoadmapConfig,
    agents_explicit: bool,
    depth_explicit: bool,
) -> RoadmapConfig:
    """Restore agent/depth specs from .roadmap-state.json when not explicit.

    On --resume, if the user did not explicitly pass --agents or --depth,
    restore the values from the state file so the pipeline uses the same
    configuration as the original run.
    """
    state_file = config.output_dir / ".roadmap-state.json"
    state = read_state(state_file)
    if state is None:
        if not agents_explicit or not depth_explicit:
            print(
                "WARNING: --resume with no state file found. "
                "Using defaults for unspecified options.",
                file=sys.stderr,
                flush=True,
            )
        _log.info("No state file found; using CLI agents for fresh run")
        return config

    # Restore agents from state if user did not explicitly pass --agents
    if not agents_explicit:
        saved_agents = state.get("agents")
        if saved_agents and isinstance(saved_agents, list):
            try:
                restored = [
                    AgentSpec(model=a["model"], persona=a["persona"])
                    for a in saved_agents
                ]
            except (KeyError, TypeError) as exc:
                _log.warning(
                    "Malformed agents in state file (%s); using CLI agents", exc
                )
                return config

            if restored != config.agents:
                agent_str = ", ".join(f"{a.model}:{a.persona}" for a in restored)
                print(
                    f"[roadmap] Restoring agents from state file: {agent_str}",
                    flush=True,
                )
            config.agents = restored
        else:
            _log.warning("State file has no agents key; using CLI agents")

    # Restore depth from state if user did not explicitly pass --depth
    if not depth_explicit:
        saved_depth = state.get("depth")
        if saved_depth:
            if saved_depth != config.depth:
                print(
                    f"WARNING: --depth mismatch.\n"
                    f"  State file depth: {saved_depth}\n"
                    f"  Current depth:    {config.depth}\n"
                    f"  Using state file depth: {saved_depth}\n",
                    file=sys.stderr,
                    flush=True,
                )
            config.depth = saved_depth

    # Restore input_type from state (C-91) — so auto-detection doesn't re-run
    saved_input_type = state.get("input_type")
    if saved_input_type and saved_input_type != "auto":
        if config.input_type == "auto":
            _log.info("Restored input_type from state: %s", saved_input_type)
            config.input_type = saved_input_type

    # Auto-wire tdd_file from state if user did not explicitly pass --tdd-file
    if config.tdd_file is None:
        saved_tdd = state.get("tdd_file")
        if saved_tdd:
            tdd_path = Path(saved_tdd)
            if tdd_path.is_file():
                _log.info("Auto-wired --tdd-file from state: %s", tdd_path)
                config.tdd_file = tdd_path
            else:
                _log.warning("State file references tdd_file %s but file not found; skipping", saved_tdd)
        # Note: When input_type=tdd and tdd_file is null in state, the spec_file
        # IS the TDD. The supplementary --tdd-file slot is intentionally empty
        # (redundancy guard nulls it). All prompt builders receive spec_file as
        # their primary input, so no fallback wiring is needed here.

    # Auto-wire prd_file from state if user did not explicitly pass --prd-file (C-27)
    if config.prd_file is None:
        saved_prd = state.get("prd_file")
        if saved_prd:
            prd_path = Path(saved_prd)
            if prd_path.is_file():
                _log.info("Auto-wired --prd-file from state: %s", prd_path)
                config.prd_file = prd_path
            else:
                _log.warning("State file references prd_file %s but file not found; skipping", saved_prd)
    else:
        # C-27: Explicit --prd-file on CLI overrides state — log if different
        saved_prd = state.get("prd_file")
        if saved_prd and str(config.prd_file) != saved_prd:
            _log.info(
                "CLI --prd-file %s overrides state prd_file %s",
                config.prd_file, saved_prd,
            )

    return config


def execute_roadmap(
    config: RoadmapConfig,
    resume: bool = False,
    no_validate: bool = False,
    auto_accept: bool = False,
    agents_explicit: bool = True,
    depth_explicit: bool = True,
) -> None:
    """Execute the roadmap generation pipeline.

    Builds the step list, handles --dry-run and --resume, then
    delegates to execute_pipeline() with roadmap_run_step.

    After all 9 steps pass, auto-invokes validation unless
    --no-validate is set or --resume halted on a failed step.

    Note: --no-validate does NOT skip the spec-fidelity step
    (FR-010, AC-005). It only skips the post-pipeline validation
    subsystem.

    Args:
        auto_accept: When True, the spec-patch resume cycle skips the
            interactive prompt and proceeds automatically if evidence is
            found. When False (default), the cycle prompts the user.
            This is an internal parameter, not exposed on the CLI.
        agents_explicit: Whether --agents was explicitly passed on the CLI.
        depth_explicit: Whether --depth was explicitly passed on the CLI.
    """
    config.output_dir.mkdir(parents=True, exist_ok=True)

    # On --resume with defaulted agents/depth, restore from state file
    if resume:
        config = _restore_from_state(
            config,
            agents_explicit=agents_explicit,
            depth_explicit=depth_explicit,
        )

    # Apply hardcoded defaults for any still-None fields (non-resume or no state)
    if not config.agents:
        config.agents = [AgentSpec("opus", "architect"), AgentSpec("haiku", "architect")]
    if not config.depth:
        config.depth = "standard"

    # FR-2.24.1.11: Recursion guard — local variable, per-invocation
    _spec_patch_cycle_count = 0

    # FR-2.24.1.9 Condition 3: Capture spec hash at function entry
    initial_spec_hash = hashlib.sha256(config.spec_file.read_bytes()).hexdigest()

    # Route input files through centralized routing logic
    routing = _route_input_files(
        input_files=(config.spec_file,),
        explicit_tdd=config.tdd_file,
        explicit_prd=config.prd_file,
        explicit_input_type=config.input_type,
    )
    config = dataclasses.replace(
        config,
        spec_file=routing["spec_file"],
        tdd_file=routing["tdd_file"],
        prd_file=routing["prd_file"],
        input_type=routing["input_type"],
    )
    _log.info(
        "Routing: spec=%s tdd=%s prd=%s type=%s",
        config.spec_file, config.tdd_file, config.prd_file, config.input_type,
    )

    # Compress the spec once up-front so every LLM step that reads it gets the
    # smaller sidecar via Step.inputs. Skipped on --dry-run (no subprocesses
    # run) and when --no-compress was passed. Deterministic auditors continue
    # to read config.spec_file (the original). On compression failure we
    # mirror the original bytes into the sidecar so step.inputs still resolve.
    if config.compress_enabled and not config.dry_run:
        _compress_pipeline_input(config.spec_file, "spec", config.output_dir)
        # Supplementary TDD/PRD inputs are compressed with the ``spec`` pipeline
        # (same document class: structured requirements) so downstream LLM steps
        # consume the smaller sidecar alongside the compressed spec.
        if config.tdd_file is not None:
            _compress_pipeline_input(config.tdd_file, "spec", config.output_dir)
        if config.prd_file is not None:
            _compress_pipeline_input(config.prd_file, "spec", config.output_dir)

    steps = _build_steps(config)

    # --dry-run: print plan and exit
    if config.dry_run:
        _dry_run_output(steps)
        return

    # --resume: check which steps already pass their gates
    if resume:
        from ..pipeline.gates import gate_passed

        steps = _apply_resume(steps, config, gate_passed)

    # Execute pipeline
    results = execute_pipeline(
        steps=steps,
        config=config,
        run_step=roadmap_run_step,
        on_step_start=_print_step_start,
        on_step_complete=_print_step_complete,
    )

    # Save state
    _save_state(config, results)

    # Check for failures
    failures = [r for r in results if r.status in (StepStatus.FAIL, StepStatus.TIMEOUT)]
    if failures:
        # FR-2.24.1.9: Check if spec-fidelity failed and auto-resume is possible
        spec_fidelity_failed = any(
            r.step
            and r.step.id == "spec-fidelity"
            and r.status in (StepStatus.FAIL, StepStatus.TIMEOUT)
            for r in results
        )

        if spec_fidelity_failed:
            resumed = _apply_resume_after_spec_patch(
                config=config,
                results=results,
                auto_accept=auto_accept,
                initial_spec_hash=initial_spec_hash,
                cycle_count=_spec_patch_cycle_count,
            )
            if resumed:
                _spec_patch_cycle_count += 1
                # Cycle complete — resumed pipeline ran to completion or failure
                # inside _apply_resume_after_spec_patch. If it returned True,
                # we're done (either success or failure was handled internally).
                return

        halt_msg = _format_halt_output(results, config)
        print(halt_msg, file=sys.stderr)
        sys.exit(1)

    print(f"\n[roadmap] Pipeline complete: {len(results)} steps passed", flush=True)

    # Auto-invoke validation after successful pipeline completion
    if no_validate:
        print("[roadmap] Validation skipped (--no-validate)", flush=True)
        _save_validation_status(config, "skipped")
        return

    # Check if validation already completed (--resume path)
    if resume:
        state_file = config.output_dir / ".roadmap-state.json"
        state = read_state(state_file)
        if state and "validation" in state:
            saved = state["validation"]
            if saved.get("status") in ("pass", "fail"):
                print(
                    f"[roadmap] Validation already completed ({saved['status']}), skipping",
                    flush=True,
                )
                return

    _auto_invoke_validate(config)


def _find_qualifying_deviation_files(
    config: RoadmapConfig,
    results: list[StepResult],
) -> list:
    """Find deviation files written after spec-fidelity started.

    Returns qualifying DeviationRecord objects, or empty list if
    conditions are not met.

    Implementation detail — not specified in the spec. Extracted for
    testability of the three-condition detection gate.
    """
    from .spec_patch import scan_accepted_deviation_records

    state_file = config.output_dir / ".roadmap-state.json"
    state = read_state(state_file)
    if state is None:
        return []

    # Get spec-fidelity started_at timestamp
    steps_state = state.get("steps", {})
    fidelity_state = steps_state.get("spec-fidelity", {})
    started_at_str = fidelity_state.get("started_at")

    # Fail-closed: if started_at is absent, condition not met
    if not started_at_str:
        return []

    try:
        started_at_ts = datetime.fromisoformat(started_at_str).timestamp()
    except (ValueError, TypeError):
        return []

    # Scan all deviation records
    all_records = scan_accepted_deviation_records(config.output_dir)
    if not all_records:
        return []

    # Filter to records written AFTER spec-fidelity started.
    # Strict > (not >=): a record with mtime == started_at was written before
    # or exactly at step start, so it cannot be evidence of a subprocess fix.
    # Caveat: HFS+ and some NFS mounts have 1-second mtime resolution, so
    # records created within the same second as started_at may be missed.
    qualifying = [r for r in all_records if r.mtime > started_at_ts]
    return qualifying


def _apply_resume_after_spec_patch(
    config: RoadmapConfig,
    results: list[StepResult],
    auto_accept: bool,
    initial_spec_hash: str,
    cycle_count: int,
) -> bool:
    """Attempt a single spec-patch auto-resume cycle after spec-fidelity FAIL.

    Evaluates the three-condition detection gate (FR-2.24.1.9):
      1. Recursion guard: cycle_count == 0
      2. Qualifying deviation files exist with mtime > started_at
      3. Spec file hash changed since run started (initial_spec_hash)

    If all conditions pass, executes the six-step disk-reread sequence
    (FR-2.24.1.10) and re-runs the pipeline via _apply_resume.

    Single-writer assumption: no concurrent writer modifies
    .roadmap-state.json between the reread and write steps.

    Returns True if the cycle was attempted (regardless of outcome),
    False if conditions were not met.
    """
    # FR-2.24.1.11: Recursion guard
    if cycle_count >= 1:
        print(
            "[roadmap] Spec-patch cycle already exhausted "
            f"(cycle_count={cycle_count}). Proceeding to normal failure.",
            flush=True,
        )
        return False

    # FR-2.24.1.9 Condition 2: Qualifying deviation files
    qualifying = _find_qualifying_deviation_files(config, results)
    if not qualifying:
        return False

    # FR-2.24.1.9 Condition 3: Spec hash changed since run started
    current_hash = hashlib.sha256(config.spec_file.read_bytes()).hexdigest()
    if current_hash == initial_spec_hash:
        return False

    # All three conditions met — enter the cycle
    # FR-2.24.1.12: Cycle entry logging
    print(
        f"[roadmap] Spec patched by subprocess. "
        f"Found {len(qualifying)} accepted deviation record(s).",
        flush=True,
    )
    print(
        "[roadmap] Triggering spec-hash sync and resume (cycle 1/1).",
        flush=True,
    )

    # FR-2.24.1.10: Six-step disk-reread sequence
    state_file = config.output_dir / ".roadmap-state.json"

    # Step 1: Re-read state from disk
    _fresh_state = read_state(state_file)  # noqa: F841

    # Step 2: Recompute spec hash
    new_hash = hashlib.sha256(config.spec_file.read_bytes()).hexdigest()

    # Step 3: Atomic write of new hash
    try:
        # Read again for fresh copy, update only spec_hash, write atomically
        fresh_for_write = read_state(state_file) or {}
        fresh_for_write["spec_hash"] = new_hash
        write_state(fresh_for_write, state_file)
    except OSError as exc:
        print(
            f"[roadmap] ERROR: Failed to update spec_hash during "
            f"auto-resume cycle: {exc}. Falling through to normal failure.",
            file=sys.stderr,
            flush=True,
        )
        return True  # Cycle was attempted but failed — don't retry

    # Step 4: Re-read state from disk AGAIN (this is what _apply_resume gets)
    post_write_state = read_state(state_file)
    if post_write_state is None:
        print(
            "[roadmap] ERROR: Could not re-read state after write. "
            "Falling through to normal failure.",
            file=sys.stderr,
            flush=True,
        )
        return True

    # Step 5: Resolve input_type before rebuild (same pattern as execute_roadmap)
    routing = _route_input_files(
        input_files=(config.spec_file,),
        explicit_tdd=config.tdd_file,
        explicit_prd=config.prd_file,
        explicit_input_type=config.input_type,
    )
    config = dataclasses.replace(
        config,
        spec_file=routing["spec_file"],
        tdd_file=routing["tdd_file"],
        prd_file=routing["prd_file"],
        input_type=routing["input_type"],
    )

    # Step 5b: Rebuild steps
    steps = _build_steps(config)

    # Step 6: Apply resume with post-write state
    from ..pipeline.gates import gate_passed

    steps = _apply_resume(steps, config, gate_passed)

    # Re-execute pipeline from the resumed point
    resumed_results = execute_pipeline(
        steps=steps,
        config=config,
        run_step=roadmap_run_step,
        on_step_start=_print_step_start,
        on_step_complete=_print_step_complete,
    )

    # Save state from resumed run
    _save_state(config, resumed_results)

    # FR-2.24.1.12: Cycle completion logging
    print("[roadmap] Spec-patch resume cycle complete.", flush=True)

    # Check if resumed pipeline also failed
    resumed_failures = [
        r for r in resumed_results if r.status in (StepStatus.FAIL, StepStatus.TIMEOUT)
    ]
    if resumed_failures:
        # FR-2.24.1.13: Normal failure on cycle exhaustion
        # Use second-run results only
        halt_msg = _format_halt_output(resumed_results, config)
        print(halt_msg, file=sys.stderr)
        sys.exit(1)

    # Resumed pipeline succeeded
    print(
        f"\n[roadmap] Pipeline complete: {len(resumed_results)} steps passed",
        flush=True,
    )
    return True


def _save_validation_status(
    config: RoadmapConfig,
    status: str,
) -> None:
    """Update .roadmap-state.json with validation status.

    Adds or updates the ``validation`` key without modifying existing state.

    Parameters
    ----------
    config:
        RoadmapConfig with output_dir.
    status:
        One of "pass", "fail", or "skipped".
    """
    state_file = config.output_dir / ".roadmap-state.json"
    state = read_state(state_file)
    if state is None:
        state = {}
    state["validation"] = {
        "status": status,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    write_state(state, state_file)


def _auto_invoke_validate(config: RoadmapConfig) -> None:
    """Auto-invoke validation after a successful roadmap pipeline run.

    Inherits --model, --max-turns, --debug from the parent roadmap config.
    Default agent count for roadmap-run invocation is 2 (dual-agent for rigor).
    """
    from .models import AgentSpec, ValidateConfig
    from .validate_executor import execute_validate

    # Default to 2 agents for roadmap-run auto-invocation (dual-agent for rigor per OQ-1)
    validate_agents = config.agents[:2] if len(config.agents) >= 2 else config.agents

    validate_config = ValidateConfig(
        output_dir=config.output_dir,
        agents=validate_agents,
        work_dir=config.output_dir,
        max_turns=config.max_turns,
        model=config.model,
        debug=config.debug,
    )

    print("\n[roadmap] Auto-invoking validation...", flush=True)

    try:
        counts = execute_validate(validate_config)
        blocking = counts.get("blocking_count", 0)
        warning = counts.get("warning_count", 0)
        info = counts.get("info_count", 0)
        print(
            f"[validate] Complete: {blocking} blocking, {warning} warning, {info} info",
            flush=True,
        )
        validation_status = "fail" if blocking > 0 else "pass"
        _save_validation_status(config, validation_status)
    except FileNotFoundError as exc:
        _log.error("Validation skipped: %s", exc)
        print(f"[validate] Skipped: {exc}", file=sys.stderr, flush=True)
        _save_validation_status(config, "skipped")


def check_remediate_resume(
    config: RoadmapConfig,
    gate_fn: Callable,
) -> bool:
    """Check if the remediate step can be skipped on --resume.

    Returns True (skip) when:
    1. remediation-tasklist.md exists
    2. Passes REMEDIATE_GATE
    3. source_report_hash matches current validation report SHA-256

    Returns False (re-run needed) otherwise.
    """
    from .gates import REMEDIATE_GATE

    tasklist_file = config.output_dir / "remediation-tasklist.md"
    if not tasklist_file.exists():
        return False

    passed, _reason = gate_fn(_gate_target(tasklist_file), REMEDIATE_GATE)
    if not passed:
        return False

    # Hash check: verify tasklist was generated from current validation report
    if not _check_tasklist_hash_current(tasklist_file, config.output_dir):
        print(
            "[roadmap] Remediation tasklist stale (hash mismatch), will re-run remediate",
            flush=True,
        )
        return False

    return True


def check_certify_resume(
    config: RoadmapConfig,
    gate_fn: Callable,
) -> bool:
    """Check if the certify step can be skipped on --resume.

    Returns True (skip) when:
    1. certification-report.md exists
    2. Passes CERTIFY_GATE

    Returns False (re-run needed) otherwise.
    """
    from .gates import CERTIFY_GATE

    report_file = config.output_dir / "certification-report.md"
    if not report_file.exists():
        return False

    passed, _reason = gate_fn(_gate_target(report_file), CERTIFY_GATE)
    return passed


def _check_tasklist_hash_current(
    tasklist_file: Path,
    output_dir: Path,
) -> bool:
    """Check if remediation tasklist's source_report_hash matches current report.

    Reads the YAML frontmatter source_report_hash and compares against
    SHA-256 of the validation report file. Returns False on mismatch
    (fail closed).
    """
    from .gates import _parse_frontmatter

    content = tasklist_file.read_text(encoding="utf-8")
    fm = _parse_frontmatter(content)
    if fm is None:
        return False

    saved_hash = fm.get("source_report_hash", "")
    if not saved_hash:
        return False

    # Find the validation report (source_report field)
    source_report = fm.get("source_report", "")
    if source_report:
        report_path = Path(source_report)
        if not report_path.is_absolute():
            report_path = output_dir / report_path
    else:
        # Default to reflect-merged.md or merged-validation-report.md
        report_path = output_dir / "reflect-merged.md"
        if not report_path.exists():
            report_path = output_dir / "merged-validation-report.md"

    if not report_path.exists():
        return False

    current_hash = hashlib.sha256(report_path.read_bytes()).hexdigest()
    return saved_hash == current_hash


def _step_needs_rerun(
    step: Step,
    gate_fn: Callable,
    dirty_outputs: set[Path],
    force_extract: bool,
    state_paths: dict[str, Path],
) -> tuple[bool, str]:
    """Determine if a single step needs re-running.

    A step needs re-run if:
    1. force_extract and step is 'extract', OR
    2. Any of its input files are in the dirty set, OR
    3. Its own gate check fails (using state-recorded paths when available).

    Returns:
        (needs_rerun: bool, reason: str)
    """
    if force_extract and step.id == "extract":
        return True, "spec file changed; forcing extract rerun"

    # If any input was re-generated, must re-run
    if any(inp in dirty_outputs for inp in (step.inputs or [])):
        deps = [str(inp) for inp in (step.inputs or []) if inp in dirty_outputs]
        return True, f"input dependency regenerated: {deps}"

    # Defense-in-depth: use state-recorded path for gate check
    check_path = state_paths.get(step.id, step.output_file)
    if check_path != step.output_file:
        _log.info(
            "Resume: step '%s' using state-recorded path %s "
            "(config-derived: %s)",
            step.id,
            check_path,
            step.output_file,
        )

    # Check own gate against the compressed sidecar when present.
    if step.gate:
        passed, reason = gate_fn(_gate_target(check_path), step.gate)
        if passed:
            return False, "gate passes"
        # Log the failure reason with diagnostic hint
        if reason and "File not found" in reason:
            print(
                f"[roadmap] {step.id}: output missing ({check_path.name})\n"
                f"  Hint: Were different --agents used in the original run?",
                file=sys.stderr,
                flush=True,
            )
        else:
            print(f"[roadmap] {step.id}: gate failed -- {reason}", flush=True)
        return True, f"gate failed: {reason}"

    # No gate defined -- must run
    return True, "no gate defined"


def _apply_resume(
    steps: list[Step | list[Step]],
    config: RoadmapConfig,
    gate_fn: Callable,
) -> list[Step | list[Step]]:
    """Apply --resume logic: skip steps whose outputs pass gates.

    Uses dependency tracking: if a step's inputs include the output of a
    step that will be re-run, it must also re-run regardless of gate status.

    Includes state-driven path resolution and parallel group semantics.
    """
    state_file = config.output_dir / ".roadmap-state.json"
    state = read_state(state_file)
    force_extract = False

    # State-driven path resolution: build lookup step_id -> recorded output_file
    state_paths: dict[str, Path] = {}
    if state is not None:
        saved_hash = state.get("spec_hash", "")
        current_hash = hashlib.sha256(config.spec_file.read_bytes()).hexdigest()
        if saved_hash and saved_hash != current_hash:
            print(
                f"WARNING: spec-file has changed since last run.\n"
                f"  Last hash: {saved_hash[:12]}...\n"
                f"  Current:   {current_hash[:12]}...\n"
                f"Forcing re-run of extract step.",
                file=sys.stderr,
                flush=True,
            )
            force_extract = True

        # Extract recorded output paths from state
        for step_id, step_data in state.get("steps", {}).items():
            recorded_path = step_data.get("output_file")
            if recorded_path:
                state_paths[step_id] = Path(recorded_path)

    skipped = 0
    result: list[Step | list[Step]] = []
    dirty_outputs: set[Path] = set()  # files that will be regenerated

    for entry in steps:
        if isinstance(entry, list):
            # Parallel group: check each step, re-run entire group if any needs it
            group_needs_rerun = False
            rerun_reasons: list[str] = []

            for s in entry:
                needs, reason = _step_needs_rerun(
                    s, gate_fn, dirty_outputs, force_extract, state_paths,
                )
                if needs:
                    group_needs_rerun = True
                    rerun_reasons.append(f"{s.id}: {reason}")

            if group_needs_rerun:
                _log.info(
                    "Parallel group [%s] marked for rerun: %s",
                    ", ".join(s.id for s in entry),
                    "; ".join(rerun_reasons),
                )
                result.append(entry)
                # Mark all group outputs as dirty (atomic group completion)
                for s in entry:
                    dirty_outputs.add(s.output_file)
            else:
                skipped += len(entry)
                print(
                    f"[roadmap] Skipping {', '.join(s.id for s in entry)} (gates pass)",
                    flush=True,
                )
        else:
            # Single step
            needs, reason = _step_needs_rerun(
                entry, gate_fn, dirty_outputs, force_extract, state_paths,
            )

            if needs:
                _log.info("Step '%s' marked for rerun: %s", entry.id, reason)
                dirty_outputs.add(entry.output_file)
                result.append(entry)
            else:
                skipped += 1
                print(f"[roadmap] Skipping {entry.id} (gate passes)", flush=True)

    if skipped > 0:
        print(f"[roadmap] Skipped {skipped} steps (gates pass)", flush=True)

    if not result:
        print("[roadmap] All steps already pass gates. Nothing to do.", flush=True)

    return result
