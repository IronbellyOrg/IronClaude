"""Shared obligation vocabulary -- single source of truth.

Used by:
- obligation_scanner.py: detection patterns for scaffold/discharge matching
- prompts.py: LLM constraint block generation to prevent false positives

Implements FR-MOD1.1 vocabulary (11 scaffold terms, 9 discharge terms)
plus preferred-alternative mappings for prompt guidance.
"""

from __future__ import annotations

# --- FR-MOD1.1: Obligation vocabulary (11 scaffold terms) ---

SCAFFOLD_TERMS: list[str] = [
    r"\bmock(?:ed|s)?\b",
    r"\bstub(?:bed|s)?\b",
    r"\bskeleton\b",
    r"\bplaceholder\b",
    r"\bscaffold(?:ing|ed)?\b",
    r"\btemporary\b",
    r"\bhardcoded\b",
    r"\bhardwired\b",
    r"\bno-?op\b",
    r"\bdummy\b",
    r"\bfake\b",
]

# Terms that DISCHARGE an obligation (something fulfilled)
DISCHARGE_TERMS: list[str] = [
    r"\breplace\b",
    r"\bwire\s+(?:up|in|into)\b",
    r"\bintegrat(?:e|ing|ed)\b",
    r"\bconnect\b",
    r"\bswap\s+(?:out|in)\b",
    r"\bremove\s+(?:mock|stub|placeholder|scaffold)\b",
    r"\bimplement\s+real\b",
    r"\bfill\s+in\b",
    r"\bcomplete\s+(?:the\s+)?(?:skeleton|scaffold)\b",
]

# --- Preferred alternatives (human-readable, for prompt injection) ---
# Key: plain-English scaffold term (as it appears in prose)
# Value: preferred alternative verb/noun

PREFERRED_ALTERNATIVES: dict[str, str] = {
    "scaffold": "create",
    "scaffolding": "construction",
    "scaffolded": "created",
    "mock": "simulate",
    "mocked": "simulated",
    "stub": "define",
    "stubbed": "defined",
    "skeleton": "outline",
    "placeholder": "initial",
    "temporary": "interim",
    "hardcoded": "fixed-value",
    "hardwired": "direct",
    "no-op": "pass-through",
    "noop": "pass-through",
    "dummy": "sample",
    "fake": "synthetic",
}


def build_prompt_constraint_block() -> str:
    """Build a <200-token constraint block for LLM generation prompts.

    Dynamically generated from PREFERRED_ALTERNATIVES so adding a term
    to the vocabulary automatically updates all prompts.
    """
    rows = []
    seen: set[str] = set()
    for avoid, prefer in PREFERRED_ALTERNATIVES.items():
        base = avoid.rstrip("edingsz")  # rough dedup by stem
        if base not in seen:
            seen.add(base)
            rows.append(f'  "{avoid}" \u2192 "{prefer}"')

    table = "\n".join(rows)

    return (
        "\n\nVOCABULARY CONSTRAINT (obligation scanner compliance):\n"
        "The downstream anti-instinct gate flags these terms as scaffolding "
        "obligations. Use the preferred alternative instead:\n"
        f"{table}\n"
        "If you genuinely mean a temporary artifact that will be replaced later, "
        "you may use the original term \u2014 but you MUST include a discharge task "
        "(replace, integrate, wire up, remove) in a subsequent phase.\n"
    )
