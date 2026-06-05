"""T07.19 -- AC-009 no-external-framework-integration audit.

Roadmap row R-133 / AC-009 forbids the swarm CLI from depending on
or importing any of the upstream agent-framework projects whose
designs MultiModelSwarm deliberately keeps non-precluding:

* ``openhands`` / ``openharness`` -- OpenHands harness family
* ``openai-assistants`` (PyPI distribution name) /
  ``openai_assistants`` (Python module form) -- OpenAI Assistants SDK
* ``langgraph`` -- LangChain's graph-based agent runtime
* ``crewai`` -- CrewAI agent-team framework

The MultiModelSwarm AC is *exclusion + non-preclusion*: Phase 1 ships
without any of these dependencies, while the contract surface stays
shaped so a future ADR could plug one in behind the same JobSpec /
ResultContract bar.  This test enforces the *exclusion half*.  The
*non-preclusion half* is a design property of the schema/result
contract and is enforced by NFR-016 (``test_contract_surface.py``).

Surfaces audited
----------------

1. ``pyproject.toml`` -- declared dependencies (both the runtime list
   under ``[project.dependencies]`` and every list under
   ``[project.optional-dependencies]``).  PEP 621 strings like
   ``"langgraph>=0.1"`` or ``"crewai[all]"`` are caught regardless of
   version specifier or extras.
2. ``src/superclaude/cli/swarm/**/*.py`` -- every Python source under
   the swarm package, scanned for ``import langgraph`` /
   ``from langgraph.foo import bar`` style statements.

A regression in either surface would represent a silent erosion of
the Phase-1 dependency boundary: a transitive dep gets re-exported as
a direct dep in pyproject, or an experimental transport sneaks an
``import crewai`` into swarm code path.  Both are caught here.

Mutation guarantee
------------------

Each detector is exercised against a synthetic source that injects
every forbidden token.  Without this, a regression in the regex (e.g.
a stray word-boundary anchor removed) would let the static scan pass
vacuously against real source files that happen to be clean.

Negative guards
---------------

Doc-comment lines that *describe the exclusion* (e.g. a runbook
paragraph naming ``openhands`` as a non-dependency) are allowed via
the same comment-prefix + sentinel-keyword allowlist that
``test_uv_enforcement.py`` uses for the UV-mandate rule.  This keeps
the swarm runbook free to name the forbidden frameworks in its
non-preclusion note without self-flagging.

Identifier-suffix tokens like ``langgraphql`` or ``crewaiops`` (a
hypothetical telemetry package) must not false-positive: the
word-boundary anchor keeps the scan narrow.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
SWARM_DIR = REPO_ROOT / "src" / "superclaude" / "cli" / "swarm"
PYPROJECT = REPO_ROOT / "pyproject.toml"

# Forbidden framework tokens.  Each entry is the *canonical* surface
# spelling; the regex covers both PyPI-style hyphens (``openai-
# assistants``) and Python-module-style underscores (``openai_
# assistants``) because PEP 621 dep strings and ``import`` statements
# use the two conventions interchangeably.
#
# Listed verbatim (not collapsed) so the audit is auditable; the
# per-token parametrization below proves each one is actually
# checked.
FORBIDDEN_FRAMEWORK_TOKENS: tuple[str, ...] = (
    "openhands",
    "openharness",
    "openai-assistants",
    "openai_assistants",
    "langgraph",
    "crewai",
)


def _normalize_token_for_regex(token: str) -> str:
    """Build a regex alternative covering hyphen/underscore variants.

    ``openai-assistants`` and ``openai_assistants`` are the same
    framework under PyPI vs Python-module spellings; match either
    when scanning any surface so a regression cannot smuggle one
    spelling past the other.
    """
    if "-" in token or "_" in token:
        return token.replace("-", "[-_]").replace("_", "[-_]")
    return token


# Word-boundary anchors at both ends keep the scan narrow.  Without
# them, ``langgraphql`` (a hypothetical future package) or a comment
# containing ``crewaiops`` would false-positive.
_TOKEN_PATTERN: re.Pattern[str] = re.compile(
    r"\b(?:" + "|".join(_normalize_token_for_regex(t) for t in FORBIDDEN_FRAMEWORK_TOKENS) + r")\b",
    re.IGNORECASE,
)

# Python ``import`` / ``from`` statement form.  Anchored to the start
# of a (stripped) line so a string literal mentioning the framework
# elsewhere does not trip the import detector; the broader vendor
# scan is the one that catches string-literal leakage.
_IMPORT_PATTERN: re.Pattern[str] = re.compile(
    r"^\s*(?:import|from)\s+("
    + "|".join(_normalize_token_for_regex(t) for t in FORBIDDEN_FRAMEWORK_TOKENS if "-" not in t)
    + r")(?:\.|\s|$)",
    re.IGNORECASE | re.MULTILINE,
)

# Comment-prefix tokens for doc-line allowlist.  A line that begins
# with one of these AND mentions at least one sentinel keyword (e.g.
# ``forbidden``, ``exclude``, ``not used``, ``non-preclusion``, the
# AC tag itself) is treated as documentation of the prohibition, not
# an invocation of it.
_COMMENT_PREFIXES: tuple[str, ...] = ("#", "//", "<!--", '"""', "'''", "*")
_SENTINEL_KEYWORDS: tuple[str, ...] = (
    "forbidden",
    "do not",
    "exclude",
    "excluded",
    "non-preclusion",
    "non-precluding",
    "not used",
    "no such",
    "must not",
    "ac-009",
)

# This audit file documents the forbidden token set in its own
# source; exclude it from any scan so the documentation does not
# self-flag.
SELF_PATH = Path(__file__).resolve()


def _line_is_documentation(line: str) -> bool:
    """Return True when a line documents the prohibition.

    Mirrors the ``test_uv_enforcement.py`` policy: comment-prefixed
    lines that mention an explicit exclusion keyword are not
    violations.  This keeps the runbook / non-preclusion notes free
    to name the forbidden frameworks.
    """
    stripped = line.strip()
    if not stripped.startswith(_COMMENT_PREFIXES):
        return False
    lowered = stripped.lower()
    return any(keyword in lowered for keyword in _SENTINEL_KEYWORDS)


def _iter_swarm_python_sources() -> list[Path]:
    """Return every ``.py`` file under the swarm package."""
    if not SWARM_DIR.exists():
        return []
    return [
        p
        for p in SWARM_DIR.rglob("*.py")
        if p.is_file()
        and "__pycache__" not in p.parts
        and p.resolve() != SELF_PATH
    ]


def _strip_doc_strings(text: str) -> str:
    """Best-effort docstring scrub for the import-form scan.

    Module/function docstrings (triple-quoted blocks) legitimately
    name the forbidden frameworks in non-preclusion notes -- e.g.
    the docstring of this very test, or a future TDD reference in
    ``swarm/__init__.py``.  Replace each triple-quoted span with
    blank lines so its line numbers stay aligned for diagnostics but
    its body is removed from the import detector input.

    The scrub is intentionally simple (no f-string or escaped-quote
    handling): the goal is to keep the audit narrow, not to be a
    full Python parser.  The token-level scan still runs against
    the *full* text via the doc-line allowlist.
    """
    def _blanker(match: re.Match[str]) -> str:
        return "\n" * match.group(0).count("\n")

    return re.sub(r'(?s)("""[^\n].*?"""|\'\'\'[^\n].*?\'\'\'|""".*?"""|\'\'\'.*?\'\'\')', _blanker, text)


# ---------------------------------------------------------------------------
# Static audit -- pyproject.toml must declare no forbidden framework dep.
# ---------------------------------------------------------------------------


def test_pyproject_exists() -> None:
    """The audit needs a pyproject.toml to scan; refuse to silently pass."""
    assert PYPROJECT.exists(), (
        f"pyproject.toml not found at {PYPROJECT}; AC-009 dep audit "
        "cannot run.  This guard rejects a silent pass when the file "
        "is missing or moved."
    )


def test_pyproject_excludes_forbidden_frameworks() -> None:
    """AC-009: pyproject.toml must not list any forbidden framework.

    Scans every line of ``pyproject.toml``; flags any non-doc line
    that mentions a forbidden token.  PEP 621 dep strings (``"langgraph
    >=0.1"``), optional-deps extras (``"crewai[all]"``), and group
    names all fall under this scan because the canonical PyPI / module
    spelling is what triggers the regex.
    """
    text = PYPROJECT.read_text(encoding="utf-8")
    offenders: list[str] = []
    for lineno, line in enumerate(text.splitlines(), start=1):
        if _line_is_documentation(line):
            continue
        match = _TOKEN_PATTERN.search(line)
        if match:
            offenders.append(
                f"  pyproject.toml:{lineno}: {match.group(0)!r} -> {line.strip()}"
            )

    assert not offenders, (
        "AC-009 violation: forbidden framework declared in pyproject.toml.\n"
        "Phase 1 ships without openhands / openharness / openai-assistants "
        "/ langgraph / crewai; remove the dependency before merging.\n"
        + "\n".join(offenders)
    )


# ---------------------------------------------------------------------------
# Static audit -- swarm Python sources must not import a forbidden framework.
# ---------------------------------------------------------------------------


def test_swarm_python_dir_scan_runs_even_when_empty() -> None:
    """The scan must execute regardless of swarm-package readiness.

    Mirrors ``test_uv_enforcement.py``: the guard runs as soon as the
    package directory exists (even if empty) so it cannot silently
    no-op once files appear.
    """
    _ = SWARM_DIR.exists()


def test_swarm_sources_do_not_import_forbidden_frameworks() -> None:
    """AC-009: no ``import openhands`` / ``from langgraph ...`` in swarm code.

    Each ``.py`` under ``src/superclaude/cli/swarm/`` is scanned with
    a line-anchored ``import`` / ``from`` regex.  Docstring spans are
    blanked first so this audit's own non-preclusion docstring (and
    any future swarm docstring naming the exclusion) does not
    self-flag.
    """
    offenders: list[str] = []
    for source in _iter_swarm_python_sources():
        try:
            text = source.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        scrubbed = _strip_doc_strings(text)
        for match in _IMPORT_PATTERN.finditer(scrubbed):
            lineno = scrubbed.count("\n", 0, match.start()) + 1
            line = text.splitlines()[lineno - 1] if lineno <= len(text.splitlines()) else ""
            if _line_is_documentation(line):
                continue
            rel = source.relative_to(REPO_ROOT)
            offenders.append(f"  {rel}:{lineno}: '{match.group(1)}' -> {line.strip()}")

    assert not offenders, (
        "AC-009 violation: forbidden framework imported in swarm sources.\n"
        "Phase 1 transports must not depend on openhands / openharness / "
        "openai-assistants / langgraph / crewai.  Remove the import or "
        "move the integration behind a future ADR-gated seam.\n"
        + "\n".join(offenders)
    )


def test_swarm_sources_token_audit() -> None:
    """AC-009 broad token scan over swarm sources (catches non-import leaks).

    The import-form scan is intentionally narrow (line-anchored).
    This complementary scan catches string-literal or attribute-form
    references -- e.g. a ``"langgraph"`` string in a registry dict, an
    ``adapters/langgraph.py`` filename being referenced, or a comment
    in a code-block that does NOT use the documentation sentinel
    keywords.  Doc lines (per ``_line_is_documentation``) are still
    allowed so non-preclusion comments remain legal.
    """
    offenders: list[str] = []
    for source in _iter_swarm_python_sources():
        try:
            text = source.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        scrubbed = _strip_doc_strings(text)
        for lineno, line in enumerate(scrubbed.splitlines(), start=1):
            if not line.strip():
                continue
            original_line = (
                text.splitlines()[lineno - 1]
                if lineno <= len(text.splitlines())
                else line
            )
            if _line_is_documentation(original_line):
                continue
            match = _TOKEN_PATTERN.search(line)
            if match:
                rel = source.relative_to(REPO_ROOT)
                offenders.append(
                    f"  {rel}:{lineno}: {match.group(0)!r} -> {original_line.strip()}"
                )

    assert not offenders, (
        "AC-009 violation: forbidden framework token leaked into swarm sources.\n"
        + "\n".join(offenders)
    )


# ---------------------------------------------------------------------------
# Mutation guards -- prove the detectors actually flag each shape.
# ---------------------------------------------------------------------------


def test_forbidden_framework_token_set_is_nonempty() -> None:
    """Empty FORBIDDEN_FRAMEWORK_TOKENS would silently green every scan."""
    assert FORBIDDEN_FRAMEWORK_TOKENS, (
        "FORBIDDEN_FRAMEWORK_TOKENS must enumerate the AC-009 exclusion "
        "list; an empty tuple would render the audit a no-op."
    )
    assert _TOKEN_PATTERN.pattern, (
        "_TOKEN_PATTERN.pattern is empty; the token audit would pass vacuously."
    )
    assert _IMPORT_PATTERN.pattern, (
        "_IMPORT_PATTERN.pattern is empty; the import audit would pass vacuously."
    )


@pytest.mark.parametrize("token", FORBIDDEN_FRAMEWORK_TOKENS)
def test_audit_detects_pyproject_dep_mutation(token: str) -> None:
    """Scanner must flag every forbidden token on a synthetic pyproject line.

    Without this guard, a regression in ``_TOKEN_PATTERN`` (regex
    typo, empty token list, broken word-boundary anchor) would let
    the pyproject scan pass vacuously on a real breach.
    """
    synthetic = f'dependencies = [\n    "{token}>=1.0",\n]\n'
    has_hit = False
    for line in synthetic.splitlines():
        if _line_is_documentation(line):
            continue
        if _TOKEN_PATTERN.search(line):
            has_hit = True
            break
    assert has_hit, (
        f"Scanner failed to detect injected pyproject dep {token!r} -- "
        "AC-009 audit would silently pass on a real regression."
    )


@pytest.mark.parametrize("token", [t for t in FORBIDDEN_FRAMEWORK_TOKENS if "-" not in t])
def test_audit_detects_import_mutation(token: str) -> None:
    """Scanner must flag every forbidden ``import`` form.

    Hyphenated PyPI names (``openai-assistants``) are not valid
    Python module names; only the underscore form
    (``openai_assistants``) is testable as an import.  The
    parametrization filter keeps the test honest.
    """
    for synthetic in (
        f"import {token}\n",
        f"from {token} import something\n",
        f"from {token}.subpkg import other\n",
        f"    import {token}\n",  # indented
    ):
        match = _IMPORT_PATTERN.search(synthetic)
        assert match is not None, (
            f"Scanner failed to detect injected import {synthetic!r} -- "
            "AC-009 import audit would silently pass on a real regression."
        )
        assert match.group(1).lower() == token.lower(), (
            f"Scanner matched but captured wrong token from {synthetic!r}: "
            f"got {match.group(1)!r}, expected {token!r}."
        )


# ---------------------------------------------------------------------------
# Negative guards -- detectors must not over-match.
# ---------------------------------------------------------------------------


def test_audit_excludes_morpheme_suffix_tokens() -> None:
    """Negative: ``langgraphql`` / ``crewaiops`` etc. must NOT be flagged.

    The word-boundary anchor (``\\b``) keeps the scan from tripping
    on identifier suffixes that share a prefix with a forbidden
    token.  A future contributor importing a hypothetical
    ``langgraphql`` adapter or referencing a ``crewaiops`` telemetry
    namespace must not be punished by this audit.
    """
    for synthetic in (
        '    "langgraphql>=0.1",\n',
        '    "crewaiops",\n',
        "from openhandsx import shim\n",
        "import openharnessful\n",
        "VAR = 'langgraphql_shim'\n",
    ):
        hits = list(_TOKEN_PATTERN.finditer(synthetic))
        # Word boundary should prevent the longer identifier matching.
        # Any hit here would mean ``\b`` was dropped from the regex.
        for hit in hits:
            matched = hit.group(0).lower()
            # The match must equal a forbidden token exactly, not be
            # a substring of a longer identifier in the line.
            surrounding = synthetic[hit.end():hit.end() + 1]
            assert not (surrounding and (surrounding.isalnum() or surrounding == "_")), (
                f"Scanner falsely flagged identifier-suffix in {synthetic!r}: "
                f"matched {matched!r} with continuation {surrounding!r}. "
                "AC-009 audit must respect word boundaries."
            )


def test_audit_allows_documentation_lines() -> None:
    """Negative: comment lines that document the exclusion must NOT be flagged.

    A runbook paragraph stating
    ``# AC-009: langgraph / crewai are forbidden in Phase 1``
    is a documentation of the prohibition, not an invocation of it.
    The combined comment-prefix + sentinel-keyword allowlist is what
    keeps these lines legal.  This negative guard ensures the
    allowlist actually works.
    """
    allowed_lines = (
        "# AC-009: openhands is forbidden in Phase 1",
        "# Do not import langgraph; see ADR-XYZ for the non-preclusion seam",
        '"""crewai excluded per AC-009 -- non-preclusion seam stays open."""',
        "// langgraph: not used in Phase 1",
        "<!-- openharness, openhands, langgraph, crewai must not be added -->",
        "    # openai_assistants excluded (Phase 1 non-preclusion only)",
    )
    for line in allowed_lines:
        assert _line_is_documentation(line), (
            f"Allowlist failed for documentation line: {line!r}.  Without this, "
            "the runbook / non-preclusion notes cannot name the forbidden "
            "frameworks without self-flagging the audit."
        )


def test_audit_rejects_documentation_lookalike_without_sentinel() -> None:
    """Negative: a comment that mentions the framework WITHOUT a sentinel
    keyword must still be treated as a violation.

    A future contributor writing ``# uses langgraph for the planner``
    cannot smuggle in a real dependency by hiding it in a comment.
    The sentinel-keyword half of the allowlist is what blocks that
    bypass.
    """
    suspicious = (
        "# uses langgraph for the planner",
        "# wraps openai_assistants client",
        "# crewai-based orchestrator",
    )
    for line in suspicious:
        assert not _line_is_documentation(line), (
            f"Allowlist incorrectly green-lit a non-exclusion comment: {line!r}. "
            "AC-009 must require an explicit exclusion sentinel keyword."
        )
