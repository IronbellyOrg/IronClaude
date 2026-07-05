"""T05.10 / AC-012 -- no new merge / diff / scoring engine in swarm.

Pins AC-012 (roadmap R-107): ``/sc:adversarial`` is the canonical
scored-merge pipeline in this framework; the swarm package MUST NOT
introduce scoring, ranking, diffing, judging, or dedup engines of its
own. Each Wave-3 component is intentionally too small to host one:

* COMP-010 / ``merge.py`` -- mechanical concat in slot order with a
  one-line provenance header. Body is pinned <=30 LOC by NFR-008.
* COMP-008 / ``recipes/*`` -- per-worker normalizers; every recipe must
  preserve count, order, and duplicates (AC-011, T04.14 boundary test).
* COMP-009 / ``reduce.py`` -- count-based status determination + mode
  dispatch + YAML emission. No cross-worker semantic comparison.

The audit runs in three independent layers so a single regression
cannot bypass all of them:

1. **Code-level identifier + import scan (AST).** Walks every
   ``*.py`` file in ``src/superclaude/cli/swarm/`` and rejects:

   - imports of known scoring / diff / fuzzy / embedding libraries
     (``difflib``, ``rapidfuzz``, ``fuzzywuzzy``, ``Levenshtein``,
     ``sklearn``, ``sentence_transformers``, ``faiss``,
     ``scipy.spatial``);
   - class and function definitions whose *identifiers* name a
     scoring engine (``*Scorer``, ``*Ranker``, ``*Judge``,
     ``*Adjudicator``, ``*MergeEngine``, ``*DiffEngine``,
     ``score_*``, ``rank_*``, ``judge_*``, ``dedupe_*``,
     ``deduplicate_*``, ``merge_findings*``, ``diff_findings*``,
     ``similarity_score*``).

   Identifiers in source code are how a real scoring engine has to
   land -- a contributor writing ``class FindingsRanker`` or
   ``import difflib`` cannot evade an AST check. String literals,
   docstrings, and comments are ignored: the merge module docstring
   names ``score``/``rank``/``judge`` verbatim to *document* the
   boundary, so a naive grep would always fail on the very file it
   is supposed to guard.

2. **Merge module code-token grep (tokenize).** The mechanical-merge
   module is the single highest-risk boundary, so it gets a stricter
   pass: tokenize the source, ignore STRING / COMMENT tokens, and
   assert the remaining code-token stream contains no ``rank`` /
   ``score`` / ``judge`` / ``adversarial`` substring. This mirrors
   the T05.10 validation command (``grep -RnE
   "rank|score|judge|adversarial" .../merge.py``) but excludes the
   docstring that the validation hand-wave assumes is absent.

3. **Canonical-pipeline pointer.** ``/sc:adversarial`` must remain
   referenced somewhere in the swarm package. AC-012 says swarm
   delegates scored-merge to that pipeline; if the reference were
   removed, callers would have nowhere to be pointed. The pointer
   reference is enforced separately from the forbidden-pattern scan
   so a future move of the reference between files cannot accidentally
   strip the contract.

Mutation guarantee
==================

Every detector has a paired synthetic-source mutation test that
proves the scanner fires on a fresh injection. Without these, a
regression in the AST walker (e.g. empty pattern list, typo in a
class-name regex, swallowed exception in a tokenizer) would let the
green-suite outcome become meaningless.

Dependencies (T05.10 spec): T05.05 (merge module boundary wiring).
CI surfacing: ``.github/workflows/boundary-guard.yml`` flags PR
touches to this file (Guard 3 / PR-review discipline).
"""

from __future__ import annotations

import ast
import io
import re
import tokenize
from dataclasses import dataclass
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
SWARM_DIR = REPO_ROOT / "src" / "superclaude" / "cli" / "swarm"
MERGE_PATH = SWARM_DIR / "merge.py"

# --- Forbidden imports ----------------------------------------------------

# Libraries whose presence in the swarm package would itself constitute
# a scoring / diff / ranking engine. Listed verbatim so the audit is
# auditable; submodule prefixes are matched as well (e.g. importing
# ``sklearn.metrics`` matches ``sklearn``).
FORBIDDEN_IMPORT_PREFIXES: tuple[str, ...] = (
    "difflib",
    "rapidfuzz",
    "fuzzywuzzy",
    "Levenshtein",
    "sklearn",
    "sentence_transformers",
    "faiss",
    "scipy.spatial",
)


# --- Forbidden identifier patterns ----------------------------------------

# Regex patterns matched against bare identifiers (no module prefix) of
# class / function / async-function definitions. Anchored so the patterns
# hit canonical engine names while letting through unrelated identifiers
# that happen to share a stem (``score`` inside a string is not an
# identifier; ``ranks_section`` would not match ``^rank_``).
FORBIDDEN_IDENTIFIER_PATTERNS: tuple[str, ...] = (
    r".+Scorer$",
    r".+Ranker$",
    r".+Judge$",
    r".+Adjudicator$",
    r".+MergeEngine$",
    r".+DiffEngine$",
    r"^score_",
    r"^rank_",
    r"^judge_",
    r"^dedupe_",
    r"^deduplicate_",
    r"^merge_findings",
    r"^diff_findings",
    r"^similarity_score",
)

_IDENT_RES: tuple[re.Pattern[str], ...] = tuple(
    re.compile(p) for p in FORBIDDEN_IDENTIFIER_PATTERNS
)


# --- Forbidden code-token substrings (merge.py strict pass) ---------------

# T05.10 validation grep -- enforced on the merge module's *code* tokens
# only (string literals and comments are excluded so the docstring that
# documents the boundary is not flagged as a violation of it).
MERGE_FORBIDDEN_TOKEN_SUBSTRINGS: tuple[str, ...] = (
    "rank",
    "score",
    "judge",
    "adversarial",
)


# --- Helpers --------------------------------------------------------------


@dataclass(frozen=True)
class _Hit:
    path: Path
    lineno: int
    category: str
    detail: str


def _swarm_python_files() -> list[Path]:
    """Every ``.py`` file in the swarm package, excluding caches."""
    out: list[Path] = []
    for path in sorted(SWARM_DIR.rglob("*.py")):
        if "__pycache__" in path.parts:
            continue
        out.append(path)
    return out


def _import_targets(tree: ast.AST) -> list[tuple[int, str]]:
    """Return (lineno, dotted-module-name) for every import statement."""
    out: list[tuple[int, str]] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                out.append((node.lineno, alias.name))
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                out.append((node.lineno, node.module))
    return out


def _defined_identifiers(tree: ast.AST) -> list[tuple[int, str]]:
    """Return (lineno, name) for every function / class definition."""
    out: list[tuple[int, str]] = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            out.append((node.lineno, node.name))
    return out


def _import_violation(module: str) -> str | None:
    for prefix in FORBIDDEN_IMPORT_PREFIXES:
        if module == prefix or module.startswith(prefix + "."):
            return prefix
    return None


def _identifier_violation(name: str) -> str | None:
    for pattern, regex in zip(FORBIDDEN_IDENTIFIER_PATTERNS, _IDENT_RES, strict=True):
        if regex.search(name):
            return pattern
    return None


def _scan_file(path: Path) -> list[_Hit]:
    """Run the AST-level audit on one file."""
    source = path.read_text(encoding="utf-8")
    tree = ast.parse(source, filename=str(path))
    hits: list[_Hit] = []
    for lineno, module in _import_targets(tree):
        prefix = _import_violation(module)
        if prefix is not None:
            hits.append(_Hit(path, lineno, "import", f"{module} (matches '{prefix}')"))
    for lineno, name in _defined_identifiers(tree):
        pattern = _identifier_violation(name)
        if pattern is not None:
            hits.append(
                _Hit(path, lineno, "identifier", f"{name} (matches {pattern!r})")
            )
    return hits


def _code_only_text(source: str) -> str:
    """Return only NAME / OP / NUMBER tokens (code, not strings/comments).

    String literals, comments, NL/NEWLINE, and indentation tokens are
    stripped so the merge.py grep pass sees only the executable code
    surface. This is the cleanest way to exclude the module docstring
    -- which legitimately names ``score`` / ``rank`` / ``judge`` while
    documenting the boundary -- without writing a brittle docstring-
    boundary regex.
    """
    keep_types = {tokenize.NAME, tokenize.OP, tokenize.NUMBER}
    chunks: list[str] = []
    reader = io.BytesIO(source.encode("utf-8")).readline
    for tok in tokenize.tokenize(reader):
        if tok.type in keep_types:
            chunks.append(tok.string)
    return " ".join(chunks)


# --- Audit tests: package-wide AST pass -----------------------------------


@pytest.mark.parametrize(
    "swarm_file",
    _swarm_python_files(),
    ids=lambda p: str(p.relative_to(REPO_ROOT)),
)
def test_swarm_file_has_no_scoring_engine_code(swarm_file: Path) -> None:
    """AC-012: no scoring/diff/judging engine in any swarm source file.

    Per-file parametrization so a failure points the reviewer at the
    exact file that introduced the boundary breach.
    """
    hits = _scan_file(swarm_file)
    assert not hits, (
        f"AC-012 violation in {swarm_file.relative_to(REPO_ROOT)}: "
        "scoring/diff/judging engine code introduced.\n"
        + "\n".join(f"  line {h.lineno} [{h.category}]: {h.detail}" for h in hits)
        + "\n/sc:adversarial is the canonical scored-merge pipeline; route "
        "scoring/ranking work there rather than adding it to the swarm."
    )


def test_swarm_audit_covers_every_python_file() -> None:
    """Coverage guard: the parametrize input must be non-empty.

    A future refactor that moves the swarm package or breaks
    :func:`_swarm_python_files` would silently green every check by
    feeding zero files into the parametrize loop. Pin a floor so the
    audit can never become a no-op.
    """
    files = _swarm_python_files()
    assert files, (
        f"No swarm .py files discovered under {SWARM_DIR.relative_to(REPO_ROOT)}; "
        "AC-012 audit cannot run with an empty file set."
    )
    # merge.py must be in there -- it is the file the boundary protects.
    assert MERGE_PATH in files, (
        f"merge.py missing from swarm file enumeration ({MERGE_PATH}); "
        "AC-012 cannot be enforced without it."
    )


# --- Audit tests: merge.py code-token strict pass -------------------------


@pytest.mark.parametrize("forbidden", MERGE_FORBIDDEN_TOKEN_SUBSTRINGS)
def test_merge_code_tokens_omit_forbidden_substring(forbidden: str) -> None:
    """merge.py code tokens must not contain ``rank|score|judge|adversarial``.

    Mirrors the T05.10 validation grep but excludes string literals
    and comments so the boundary-documenting docstring does not fire.
    A regression that wires a scoring call (``self.score_findings(...)``,
    ``rank_by_severity(...)``) into the merge body lands as a NAME token
    and is caught here.
    """
    source = MERGE_PATH.read_text(encoding="utf-8")
    code = _code_only_text(source).lower()
    assert forbidden not in code, (
        f"merge.py code tokens contain forbidden substring {forbidden!r} -- "
        "AC-012 violation. The mechanical-merge module must not host any "
        "scoring / ranking / judging operation; route it to /sc:adversarial."
    )


# --- Audit tests: canonical-pipeline pointer ------------------------------


def test_sc_adversarial_referenced_in_swarm_package() -> None:
    """AC-012 acceptance: ``/sc:adversarial`` must be named in the package.

    Swarm delegates scored-merge to ``/sc:adversarial``; if no swarm
    file references it, the contract has lost its forward pointer and a
    caller wanting scored-merge has nowhere to be routed. This positive
    assertion complements the forbidden-pattern scan above.
    """
    references: list[Path] = []
    for path in _swarm_python_files():
        if "/sc:adversarial" in path.read_text(encoding="utf-8"):
            references.append(path)
    assert references, (
        "/sc:adversarial not referenced anywhere in the swarm package "
        f"({SWARM_DIR.relative_to(REPO_ROOT)}). AC-012 requires the "
        "canonical scored-merge pipeline pointer to remain discoverable "
        "to callers (typically via a lens's recommended_next_command or "
        "the merge module's boundary docstring)."
    )


# --- Mutation guards: prove the detectors fire on fresh injections --------


def _scan_synthetic(source: str) -> list[_Hit]:
    """Run the AST audit against an in-memory source string."""
    tree = ast.parse(source)
    hits: list[_Hit] = []
    fake_path = Path("<synthetic>")
    for lineno, module in _import_targets(tree):
        prefix = _import_violation(module)
        if prefix is not None:
            hits.append(_Hit(fake_path, lineno, "import", module))
    for lineno, name in _defined_identifiers(tree):
        pattern = _identifier_violation(name)
        if pattern is not None:
            hits.append(_Hit(fake_path, lineno, "identifier", name))
    return hits


@pytest.mark.parametrize("forbidden_module", FORBIDDEN_IMPORT_PREFIXES)
def test_audit_detects_forbidden_import(forbidden_module: str) -> None:
    """Each forbidden import prefix must trip the AST audit.

    Without this, a regression in :func:`_import_violation` (e.g. a
    typo, an emptied tuple, a swapped ``startswith``) would let the
    package-wide scan green on a real ``import difflib``.
    """
    synthetic = f"import {forbidden_module}\n"
    hits = _scan_synthetic(synthetic)
    assert any(h.category == "import" for h in hits), (
        f"AC-012 audit failed to detect injected import "
        f"{forbidden_module!r}; the import-prefix check is broken."
    )


@pytest.mark.parametrize(
    "engine_class",
    [
        "FindingsScorer",
        "ClaimRanker",
        "FindingJudge",
        "WorkerAdjudicator",
        "WaveMergeEngine",
        "WaveDiffEngine",
    ],
)
def test_audit_detects_forbidden_class_identifier(engine_class: str) -> None:
    """Each canonical engine class-name suffix must trip the audit.

    A contributor adding ``class FindingsScorer`` to any swarm file
    must be caught regardless of which file they put it in; this
    proves the identifier-suffix regexes are wired and the AST walker
    actually visits class definitions.
    """
    synthetic = f"class {engine_class}:\n    pass\n"
    hits = _scan_synthetic(synthetic)
    assert any(h.category == "identifier" and engine_class in h.detail for h in hits), (
        f"AC-012 audit failed to detect injected class {engine_class!r}; "
        "the identifier-suffix regexes are broken."
    )


@pytest.mark.parametrize(
    "engine_function",
    [
        "score_findings",
        "rank_workers",
        "judge_outputs",
        "dedupe_rows",
        "deduplicate_sections",
        "merge_findings_v2",
        "diff_findings_smart",
        "similarity_score_pairs",
    ],
)
def test_audit_detects_forbidden_function_identifier(engine_function: str) -> None:
    """Each canonical engine function-name prefix must trip the audit."""
    synthetic = f"def {engine_function}():\n    return None\n"
    hits = _scan_synthetic(synthetic)
    assert any(
        h.category == "identifier" and engine_function in h.detail for h in hits
    ), (
        f"AC-012 audit failed to detect injected function {engine_function!r}; "
        "the identifier-prefix regexes are broken."
    )


@pytest.mark.parametrize("forbidden", MERGE_FORBIDDEN_TOKEN_SUBSTRINGS)
def test_code_only_text_keeps_forbidden_substring_from_real_code(
    forbidden: str,
) -> None:
    """Synthetic source proves the tokenizer strips strings but keeps code.

    Mutation guard for :func:`_code_only_text`: a synthetic body that
    puts each forbidden substring inside both a string literal AND a
    real identifier must produce a code-only text containing the
    identifier (caught) but not the string (ignored).
    """
    synthetic = (
        f'"""docstring uses {forbidden} to document the boundary."""\n'
        "def f():\n"
        f"    x = {forbidden}_local\n"
        "    return x\n"
    )
    code_only = _code_only_text(synthetic).lower()
    assert forbidden in code_only, (
        f"_code_only_text dropped identifier containing {forbidden!r}; "
        "the tokenizer is filtering NAME tokens by mistake."
    )


@pytest.mark.parametrize("forbidden", MERGE_FORBIDDEN_TOKEN_SUBSTRINGS)
def test_code_only_text_excludes_docstring_substring(forbidden: str) -> None:
    """Strings/docstrings must NOT leak into the code-only text.

    Complementary mutation guard: source where the forbidden word
    appears *only* in a docstring / string literal must produce a
    code-only text that does not contain the word. Without this, the
    code-token grep would fire on every file with a documenting
    docstring -- including merge.py itself.
    """
    synthetic = (
        f'"""this docstring mentions {forbidden} only in prose."""\n'
        "def f():\n"
        f'    note = "the word {forbidden} appears in this string"\n'
        "    return note\n"
    )
    code_only = _code_only_text(synthetic).lower()
    assert forbidden not in code_only, (
        f"_code_only_text leaked string/docstring substring {forbidden!r} "
        "into the code-only text; the tokenizer is not stripping STRING "
        "tokens and the merge.py grep pass would false-positive on the "
        "boundary docstring."
    )


def test_forbidden_pattern_sets_are_nonempty() -> None:
    """Guard against an empty pattern tuple shipping by accident.

    Pattern tuples that become ``()`` would make every audit a no-op:
    no imports flagged, no identifiers flagged, no code-token grep.
    The mutation tests above each iterate a tuple, so an empty tuple
    would also produce zero parametrize cases and silently skip.
    """
    assert FORBIDDEN_IMPORT_PREFIXES, (
        "FORBIDDEN_IMPORT_PREFIXES must enumerate the scoring/diff library "
        "surface; an empty tuple would render the AC-012 import audit a no-op."
    )
    assert FORBIDDEN_IDENTIFIER_PATTERNS, (
        "FORBIDDEN_IDENTIFIER_PATTERNS must enumerate the scoring/diff "
        "identifier surface; an empty tuple would render the AC-012 "
        "identifier audit a no-op."
    )
    assert MERGE_FORBIDDEN_TOKEN_SUBSTRINGS, (
        "MERGE_FORBIDDEN_TOKEN_SUBSTRINGS must enumerate the merge.py "
        "code-token grep surface; an empty tuple would render the strict "
        "merge.py pass a no-op."
    )
