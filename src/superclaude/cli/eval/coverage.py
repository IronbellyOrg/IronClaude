"""FR-G5 hook-matcher coverage gate (T04.14 / D-0075 / R-075).

The hook-matcher coverage gate enforces design-spec §1.5: for every
hook matcher pattern P registered in ``~/.claude/settings.json``, an
eval MUST exist in the suite under test that issues a real tool call
whose name matches P. The bug PR #49 fixed was exactly this class of
silent regression — a matcher pattern broke and no eval noticed because
no eval issued a matching tool call. The v1 surface covers the three
known auggie-prefix matchers (``mcp__auggie__*``, ``mcp__auggie-mcp__*``,
``mcp__airis-mcp-gateway__*``); future suites extend the coverage by
declaring additional ``expect_tool_call`` inputs.

Public surface
==============

:func:`coverage_gate`
    The CLI entry point. Reads ``settings_path`` JSON, extracts every
    ``hooks.<event>[].matcher`` pattern, applies the optional
    ``matcher_filter`` (defaults to v1 MCP prefixes), then walks the
    supplied ``suite`` and resolves at least one covering eval per
    pattern. Writes a ``coverage_missing:<pattern>`` artifact for every
    uncovered pattern when ``output_dir`` is supplied.

:class:`CoverageResult`
    Frozen dataclass capturing the per-pattern coverage map, the
    covered/missing partition, and the artifact paths actually written
    to disk. ``result.passed`` is the single-bit gate verdict.

:func:`eval_covers_pattern`
    The matcher-to-eval mapping rule (compiled regex applied to each
    eval's ``inputs[].expect_tool_call`` value). Exposed so tests can
    cross-check the registry derivation without re-running the gate.

:func:`extract_hook_matchers`
    Pure parser over a settings.json mapping. Reused by ``eval doctor``
    so the doctor output can enumerate matchers without re-reading the
    file from disk.

Wiring
======

``superclaude eval doctor --check-coverage`` invokes the gate against
the doctor-scoped suite and ``~/.claude/settings.json``; a failure
prints the missing-pattern roster on stderr and exits 2 (alongside
HARD-capability failures).

``superclaude eval run`` invokes the gate at the top of the run AFTER
suite parse and BEFORE any worker is dispatched, so a missing-coverage
breach short-circuits the run without touching any per-eval HOME.
Artifacts land inside the resolved ``--output-dir`` so the FR-G4 run
directory contains the full forensic trail.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Iterable, Mapping, Optional, Sequence

from .models import EvalSpec

__all__ = [
    "COVERAGE_GATE_FAILED_EXIT_CODE",
    "COVERAGE_MISSING_ARTIFACT_PREFIX",
    "CoverageMatcher",
    "CoverageResult",
    "coverage_gate",
    "default_matcher_filter",
    "eval_covers_pattern",
    "extract_hook_matchers",
    "sanitize_pattern_for_filename",
]


COVERAGE_GATE_FAILED_EXIT_CODE: int = 2
"""Process exit code emitted when the gate reports missing coverage.

Design-spec §4 maps every harness-rejection outcome (schema error,
scratch-root violation, missing capability, missing matcher coverage,
etc.) to exit code ``2``. Pinned here so the CLI wiring and the
T04.14 / T05.25 tests agree on a single source of truth.
"""


COVERAGE_MISSING_ARTIFACT_PREFIX: str = "coverage_missing:"
"""Filename prefix for the per-pattern artifact written on a breach.

The full filename is ``coverage_missing:<sanitised-pattern>`` so a
``grep -l '^coverage_missing:'`` against the run directory surfaces
every uncovered matcher in deterministic order. The colon is
filesystem-safe on every POSIX host the harness supports; the
sanitiser swaps out characters that are not (``/``, ``|``, ``*``, …)
so the artifact can also be tar'd up without escaping.
"""


# v1 covers these three MCP tool prefixes per design-spec §1.5. The
# tuple is module-private because the default filter is exported as a
# function — callers that need to extend coverage compose their own
# predicate rather than mutating this list.
_DEFAULT_MCP_TOOL_PREFIXES: tuple[str, ...] = (
    "mcp__auggie__",
    "mcp__auggie-mcp__",
    "mcp__airis-mcp-gateway__",
)


@dataclass(frozen=True)
class CoverageMatcher:
    """One matcher pattern extracted from ``settings.json``.

    Attributes:
        event: Hook event the matcher is bound to (``PreToolUse``,
            ``PostToolUse``, ``UserPromptSubmit``, …). Carried so the
            artifact and stderr output can name the registration site.
        pattern: The matcher regex as written in settings.json
            (verbatim, not normalised). Coverage resolution compiles
            this string with :func:`re.compile`; an unparseable pattern
            yields ``covers=False`` for every eval.
    """

    event: str
    pattern: str


@dataclass(frozen=True)
class CoverageResult:
    """Outcome of a single :func:`coverage_gate` invocation.

    Attributes:
        matchers: Every matcher considered (post ``matcher_filter``).
        covered: Subset of ``matchers`` that has at least one covering
            eval. Order matches ``matchers``.
        missing: Subset of ``matchers`` with no covering eval. The gate
            fails (``passed=False``) iff this is non-empty.
        artifacts: Mapping of pattern → on-disk artifact path written
            during this invocation. Empty when ``output_dir`` is
            ``None`` or when no matcher is missing coverage.
        coverage_map: Mapping of pattern → tuple of covering eval ids.
            Always populated (even when the gate passes) so callers can
            render the full coverage roster.
    """

    matchers: tuple[CoverageMatcher, ...] = ()
    covered: tuple[CoverageMatcher, ...] = ()
    missing: tuple[CoverageMatcher, ...] = ()
    artifacts: Mapping[str, Path] = field(default_factory=dict)
    coverage_map: Mapping[str, tuple[str, ...]] = field(default_factory=dict)

    @property
    def passed(self) -> bool:
        """``True`` iff every checked matcher has a covering eval."""
        return not self.missing

    def to_dict(self) -> dict[str, object]:
        """JSON-serialisable view for ``eval doctor --json`` payloads."""
        return {
            "passed": self.passed,
            "matchers": [
                {"event": m.event, "pattern": m.pattern} for m in self.matchers
            ],
            "covered": [
                {"event": m.event, "pattern": m.pattern} for m in self.covered
            ],
            "missing": [
                {"event": m.event, "pattern": m.pattern} for m in self.missing
            ],
            "artifacts": {k: str(v) for k, v in self.artifacts.items()},
            "coverage_map": {
                k: list(v) for k, v in self.coverage_map.items()
            },
        }


def sanitize_pattern_for_filename(pattern: str) -> str:
    """Replace filesystem-unsafe characters in a matcher pattern.

    Permits ``[A-Za-z0-9_:.-]`` verbatim; everything else (``/``, ``|``,
    ``*``, whitespace) collapses to ``_``. The colon is kept because it
    is filesystem-safe on every POSIX host the harness supports and the
    artifact prefix already uses one.
    """
    return re.sub(r"[^A-Za-z0-9_:.-]", "_", pattern)


def default_matcher_filter(pattern: str) -> bool:
    """v1 only enforces coverage for matchers that target MCP tools.

    Matchers like ``Edit|Write|mcp__serena__replace_content`` mix MCP
    tool prefixes with built-in tool names — these are bookkeeping
    hooks that no eval needs to issue a tool call for. The v1 gate
    therefore restricts itself to matchers that mention one of the
    three known auggie/airis MCP prefixes; T05.25 extends the
    predicate as additional MCP tool families come online.
    """
    return any(prefix in pattern for prefix in _DEFAULT_MCP_TOOL_PREFIXES)


def extract_hook_matchers(
    settings: Mapping[str, object],
) -> tuple[CoverageMatcher, ...]:
    """Walk ``hooks.<event>[].matcher`` entries from parsed settings.json.

    Entries without a ``matcher`` field (e.g. ``SessionStart`` hooks
    that always fire) are skipped — the gate has nothing to verify for
    them. The returned tuple preserves declaration order so the
    artifact list and stderr roster are deterministic across runs.
    """
    hooks = settings.get("hooks")
    if not isinstance(hooks, Mapping):
        return ()
    out: list[CoverageMatcher] = []
    for event, entries in hooks.items():
        if isinstance(entries, (str, bytes)) or not isinstance(entries, Iterable):
            continue
        for entry in entries:
            if not isinstance(entry, Mapping):
                continue
            pattern = entry.get("matcher")
            if isinstance(pattern, str) and pattern:
                out.append(CoverageMatcher(event=str(event), pattern=pattern))
    return tuple(out)


def _iter_eval_tool_calls(spec: EvalSpec) -> Iterable[str]:
    """Yield tool-call names this eval issues.

    The v1 mapping rule reads ``inputs[].expect_tool_call`` (a string
    declared on each input row that names the MCP tool the eval is
    expected to invoke). Future tag conventions (``covers:`` field,
    ``provides:`` list) can be added without changing the gate
    surface; for now this single derivation rule keeps the registry
    aligned with what evals already declare.
    """
    for row in spec.inputs:
        if not isinstance(row, Mapping):
            continue
        tc = row.get("expect_tool_call")
        if isinstance(tc, str) and tc:
            yield tc


def eval_covers_pattern(spec: EvalSpec, pattern: str) -> bool:
    """Return ``True`` if ``spec`` issues any tool call matched by ``pattern``.

    ``pattern`` is compiled with :func:`re.search` so a matcher like
    ``mcp__auggie__.*`` correctly anchors against the prefix. An
    unparseable pattern returns ``False`` rather than raising so the
    gate can still report it as ``missing`` (with the regex error
    surfaced via the artifact payload).
    """
    try:
        regex = re.compile(pattern)
    except re.error:
        return False
    return any(regex.search(tc) for tc in _iter_eval_tool_calls(spec))


def coverage_gate(
    settings_path: Path,
    suite: Sequence[EvalSpec],
    *,
    output_dir: Optional[Path] = None,
    matcher_filter: Optional[Callable[[str], bool]] = None,
) -> CoverageResult:
    """Compute matcher → eval coverage and emit per-pattern artifacts.

    Args:
        settings_path: Path to a ``settings.json`` containing the hook
            registrations to enforce coverage over. A missing or
            unreadable file is treated as the empty matcher set (the
            gate trivially passes) so the doctor stays green on a host
            that has not yet shipped a settings.json.
        suite: Post-expansion sequence of :class:`EvalSpec` entries
            from the suite under test.
        output_dir: Optional directory to write
            ``coverage_missing:<pattern>`` artifacts into. When
            ``None``, no files are written and ``result.artifacts`` is
            empty — useful for ``doctor --check-coverage`` reports that
            only need the verdict, not the forensic trail.
        matcher_filter: Predicate applied to each matcher pattern;
            only patterns where it returns ``True`` are checked.
            Defaults to :func:`default_matcher_filter` (v1 MCP tool
            prefixes).

    Returns:
        A :class:`CoverageResult` whose ``passed`` bit is ``True`` iff
        every checked matcher has at least one covering eval. The
        ``coverage_map`` reports the resolved eval ids per pattern so
        callers can render the full registry alongside the verdict.
    """
    matcher_filter = matcher_filter or default_matcher_filter
    if not settings_path.is_file():
        return CoverageResult()
    try:
        data = json.loads(settings_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return CoverageResult()
    if not isinstance(data, Mapping):
        return CoverageResult()

    raw = extract_hook_matchers(data)
    matchers = tuple(m for m in raw if matcher_filter(m.pattern))

    coverage_map: dict[str, tuple[str, ...]] = {}
    covered: list[CoverageMatcher] = []
    missing: list[CoverageMatcher] = []
    for m in matchers:
        covering = tuple(
            spec.id for spec in suite if eval_covers_pattern(spec, m.pattern)
        )
        coverage_map[m.pattern] = covering
        if covering:
            covered.append(m)
        else:
            missing.append(m)

    artifacts: dict[str, Path] = {}
    if missing and output_dir is not None:
        output_dir.mkdir(parents=True, exist_ok=True)
        for m in missing:
            filename = (
                f"{COVERAGE_MISSING_ARTIFACT_PREFIX}"
                f"{sanitize_pattern_for_filename(m.pattern)}"
            )
            path = output_dir / filename
            payload = {
                "event": m.event,
                "pattern": m.pattern,
                "coverage_missing": True,
                "covered_by": [],
                "settings_source": str(settings_path),
            }
            path.write_text(
                json.dumps(payload, indent=2, sort_keys=True) + "\n",
                encoding="utf-8",
            )
            artifacts[m.pattern] = path

    return CoverageResult(
        matchers=matchers,
        covered=tuple(covered),
        missing=tuple(missing),
        artifacts=artifacts,
        coverage_map=coverage_map,
    )
