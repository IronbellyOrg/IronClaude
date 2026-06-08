"""T02.28 -- AC-013 no-Claude-Code-isms grep audit CI gate.

Enforces roadmap row R-059 (AC-013) -- the contract surface of the
swarm CLI must remain caller-agnostic. Job-spec, result-contract,
CLI, and monitoring-contract files MUST NOT mention any Claude Code
tool name. A swarm job is dispatched via ``subprocess.run`` from any
process (Claude, a shell, a CI bot); leaking Claude-tool tokens into
the contract surface implies non-Claude callers cannot use it.

This is the Phase-2 audit; Phase 7 (T07.15 / NFR-016) extends the same
audit with vendor strings (``claude.ai``, ``anthropic``) plus the
detached-survival check. Keep the two tests independent so a Phase-7
regression cannot silently mask a Phase-2 breach.

Mutation guarantee
------------------
The audit MUST fail when a Claude-tool token is injected into any
contract-surface file. ``test_audit_detects_mutation`` proves the
detector itself works by scanning a synthetic source string carrying
each forbidden token in turn, so a future "scan returns empty" bug
cannot make the green-suite outcome meaningless.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
SWARM_DIR = REPO_ROOT / "src" / "superclaude" / "cli" / "swarm"

# Contract surfaces per AC-013. Each entry is (relative path, role) so
# the failure message can name what category of contract was breached.
# Job spec  -- DM-001 JSON Schema + JobSpec/nested dataclasses.
# Result    -- DM-012 ResultContract + DM-017 DoneSentinel records.
# CLI       -- Click group + subcommands (operator surface).
# Monitor   -- DM-014 SwarmState + DM-015 EventRecord persistence.
CONTRACT_SURFACE_FILES: tuple[tuple[str, str], ...] = (
    ("schema.py", "job-spec"),
    ("models.py", "job-spec/result-contract"),
    ("commands.py", "CLI"),
    ("__init__.py", "CLI"),
    ("state.py", "monitoring"),
    ("logging_.py", "monitoring"),
)

# Claude Code tool names. Forbidden as identifiers, attribute accesses,
# or bare tokens in any contract surface. Listed verbatim so the audit
# is auditable; do NOT rewrite as a single regex literal -- the
# per-token parametrization is what proves each token is checked.
FORBIDDEN_CLAUDE_TOKENS: tuple[str, ...] = (
    "Task",
    "WebFetch",
    "WebSearch",
    "TodoWrite",
    "NotebookEdit",
    "Read",
    "Edit",
    "Bash",
    "Glob",
    "Grep",
    "Skill",
    "ExitPlanMode",
    "EnterPlanMode",
)

# Word-boundary regex catches the bare token while letting compound
# identifiers (``Reader``, ``BashOperator``, ``Editable``) through. The
# AC targets the canonical Claude-tool surface, not every word that
# happens to share a prefix.
_FORBIDDEN_RE: re.Pattern[str] = re.compile(
    r"\b(" + "|".join(re.escape(tok) for tok in FORBIDDEN_CLAUDE_TOKENS) + r")\b"
)


def _scan_for_forbidden(text: str) -> list[tuple[int, str, str]]:
    """Return (lineno, token, stripped-line) tuples for every hit."""
    hits: list[tuple[int, str, str]] = []
    for lineno, line in enumerate(text.splitlines(), start=1):
        match = _FORBIDDEN_RE.search(line)
        if match is not None:
            hits.append((lineno, match.group(1), line.strip()))
    return hits


@pytest.mark.parametrize(
    "rel_path,role",
    CONTRACT_SURFACE_FILES,
    ids=[f"{role}:{rel}" for rel, role in CONTRACT_SURFACE_FILES],
)
def test_contract_surface_has_no_claude_tool_names(
    rel_path: str, role: str
) -> None:
    """AC-013: zero Claude tool names in contract-surface files.

    Each surface category (job spec / result contract / CLI / monitor)
    is scanned in its own parametrization so a failure message points
    directly at the role that broke caller-agnosticism.
    """
    source = SWARM_DIR / rel_path
    assert source.exists(), (
        f"Contract surface file missing: {source.relative_to(REPO_ROOT)} "
        f"(role={role}). AC-013 audit cannot run without it."
    )
    hits = _scan_for_forbidden(source.read_text(encoding="utf-8"))
    assert not hits, (
        f"AC-013 violation in {role} surface "
        f"({source.relative_to(REPO_ROOT)}): Claude tool tokens leaked.\n"
        + "\n".join(f"  line {ln}: '{tok}' -> {body}" for ln, tok, body in hits)
    )


@pytest.mark.parametrize("token", FORBIDDEN_CLAUDE_TOKENS)
def test_audit_detects_mutation(token: str) -> None:
    """Mutation guard: prove the scanner catches each forbidden token.

    Without this, a regression that breaks ``_scan_for_forbidden`` (e.g.
    a regex typo, an accidental ``re.escape`` swap, an empty token list)
    would let the surface scan pass vacuously. The synthetic source
    inserts one token at a time and asserts the scanner flags it.
    """
    synthetic = f"def handler():\n    invoke('{token}')\n    return None\n"
    hits = _scan_for_forbidden(synthetic)
    assert any(tok == token for _, tok, _ in hits), (
        f"Scanner failed to detect injected Claude token '{token}' -- "
        "AC-013 audit would silently pass on a real regression."
    )


def test_forbidden_token_set_is_nonempty() -> None:
    """Guard against an empty FORBIDDEN_CLAUDE_TOKENS shipping by accident.

    A future refactor that strips the tuple to ``()`` would make the
    regex match nothing and silently green every surface scan.
    """
    assert FORBIDDEN_CLAUDE_TOKENS, (
        "FORBIDDEN_CLAUDE_TOKENS must enumerate the Claude-tool surface; "
        "an empty tuple would render AC-013 audit a no-op."
    )


def test_contract_surface_set_covers_acceptance_roles() -> None:
    """AC-013 names four surface categories; the file table must cover them."""
    roles = {role for _, role in CONTRACT_SURFACE_FILES}
    required = {"job-spec", "CLI", "monitoring"}
    # ``job-spec/result-contract`` covers both job-spec and result.
    has_result = any("result-contract" in role for role in roles)
    missing = required - {r for role in roles for r in role.split("/")}
    assert not missing, f"AC-013 surface roles missing coverage: {missing}"
    assert has_result, "AC-013 requires result-contract coverage in surface set"
