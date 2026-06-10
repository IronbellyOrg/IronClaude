"""Pipeline gate validation -- pure Python, no subprocess, no LLM invocation.

Validates step outputs against GateCriteria with tier-proportional checks:
  EXEMPT  -> always passes
  LIGHT   -> file exists + non-empty
  STANDARD -> + min lines + YAML frontmatter fields
  STRICT  -> + semantic checks (if defined)

NFR-003: No subprocess import. NFR-007: No sprint/roadmap imports.
"""

from __future__ import annotations

import logging
from pathlib import Path

from .frontmatter import extract_frontmatter
from .models import GateCriteria

_log = logging.getLogger("superclaude.pipeline.gates")


def gate_passed(
    output_file: Path,
    criteria: GateCriteria,
    *,
    envelope: object | None = None,
    repo_root: Path | None = None,
) -> tuple[bool, str | None]:
    """Validate a step's output against its gate criteria.

    Returns (True, None) on pass.
    Returns (False, reason) on failure where reason is human-readable.

    ``envelope`` and ``repo_root`` are R1.3 keyword-only optional
    parameters consumed by ``criteria.code_assertions``. They are typed
    as ``object`` / ``Path | None`` rather than the precise
    ``PipelineEnvelope`` because ``cli/pipeline/*`` must not import from
    ``cli/roadmap/*`` (NFR-007). When either is ``None`` and the criteria
    define code_assertions, the assertions are skipped -- this skip-path is
    PRESERVED (R1.6 CI-vs-runtime split decision): it is the CORRECT behavior
    for CI-only/source-tree assertions on a pipx-installed package (which has
    no ``src/`` tree at runtime) and for live callers (``execute_pipeline``)
    that validate rendered output rather than the envelope. CI-only assertions
    (``CodeAssertion.ci_only=True``) are additionally skipped even when the
    envelope IS plumbed -- they are enforced exclusively by their dedicated CI
    tests -- so only runtime-safe assertions ever fire in the live gate path.
    """
    tier = criteria.enforcement_tier

    # EXEMPT: always passes
    if tier == "EXEMPT":
        return True, None

    # LIGHT, STANDARD, STRICT: file must exist
    if not output_file.exists():
        return False, f"File not found: {output_file}"

    # LIGHT, STANDARD, STRICT: file must be non-empty
    content = output_file.read_text(encoding="utf-8")
    if len(content.strip()) == 0:
        return False, f"File empty (0 bytes): {output_file}"

    # LIGHT stops here
    if tier == "LIGHT":
        return True, None

    # STANDARD, STRICT: minimum line count
    lines = content.splitlines()
    if len(lines) < criteria.min_lines:
        return False, (
            f"Below minimum line count: {len(lines)} < {criteria.min_lines} "
            f"in {output_file}"
        )

    # STANDARD, STRICT: YAML frontmatter fields
    if criteria.required_frontmatter_fields:
        ok, reason = _check_frontmatter(
            content, criteria.required_frontmatter_fields, output_file
        )
        if not ok:
            return False, reason

    # STANDARD stops here
    if tier == "STANDARD":
        return True, None

    # STRICT: semantic checks
    if criteria.semantic_checks:
        for check in criteria.semantic_checks:
            result = check.check_fn(content)
            if result is not True:
                detail = result if isinstance(result, str) else check.failure_message
                if getattr(check, "advisory", False):
                    # Advisory: record a WARNING but do NOT fail the gate.
                    # Include the output_file so the warning is traceable back
                    # to the producing gate/artifact when many gates run in a
                    # pipeline (PR #155 review r3385326536).
                    _log.warning(
                        "Advisory gate check '%s' did not pass (non-fatal) "
                        "for %s: %s",
                        check.name,
                        output_file,
                        detail,
                    )
                    continue
                return (
                    False,
                    f"Semantic check '{check.name}' failed: {detail}",
                )

    # STRICT: code assertions (R1.3 / §MVR §2; R1.6 CI-vs-runtime split)
    if criteria.code_assertions:
        if envelope is None or repo_root is None:
            # PRESERVED skip-path (R1.6): when a caller does not plumb
            # envelope/repo_root, all code_assertions are skipped. This is the
            # CORRECT behavior -- for CI-only/source-tree assertions on a
            # pipx-installed package (no ``src/`` tree at runtime) and for live
            # callers (execute_pipeline) that gate on rendered output. NOT a
            # backward-compat shim to be deleted: runtime assertions fire only
            # when a caller (e.g. verify-implementation) plumbs the envelope.
            return True, None
        for assertion in criteria.code_assertions:
            # CI-only (source-tree/AST) assertions never fire in the live gate
            # path -- they require a ``src/`` tree absent on a pipx install and
            # are enforced by their dedicated CI tests instead. Only
            # runtime-safe (envelope-state) assertions evaluate here.
            if getattr(assertion, "ci_only", False):
                continue
            finding = assertion.check_fn(envelope, repo_root)
            if finding is not None:
                detail = (
                    getattr(finding, "description", None) or assertion.failure_message
                )
                return (
                    False,
                    f"Code assertion '{assertion.name}' failed: {detail}",
                )

    return True, None


def _check_frontmatter(
    content: str,
    required_fields: list[str | tuple[str, ...]],
    output_file: Path,
) -> tuple[bool, str | None]:
    """Validate that required YAML frontmatter fields are present.

    Parsing is delegated to the single canonical
    :func:`superclaude.cli.pipeline.frontmatter.extract_frontmatter`
    (Contract #6 — one frontmatter parser). This wrapper enforces only the
    required-field contract on the parsed top-level keys; it carries no
    parsing logic of its own.

    ``required_fields`` entries are either a string (exact key required) or a
    tuple of strings (OR-group — at least one of the aliases must appear).
    The tuple form expresses mutually exclusive aliases from the template
    contract, e.g. ``("spec_source", "spec_sources")``.
    """
    fm = extract_frontmatter(content)
    if fm is None:
        return False, f"YAML frontmatter not found in {output_file}"

    found_keys = set(fm.keys())

    for field in required_fields:
        if isinstance(field, tuple):
            if not any(alias in found_keys for alias in field):
                alias_desc = " or ".join(f"'{alias}'" for alias in field)
                return (
                    False,
                    f"Missing required frontmatter field "
                    f"(one of {alias_desc}) in {output_file}",
                )
        elif field not in found_keys:
            return (
                False,
                f"Missing required frontmatter field '{field}' in {output_file}",
            )

    return True, None
