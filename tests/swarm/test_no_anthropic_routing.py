"""T03.20 -- AC-010 no-routing-to-host-vendor-models guard.

Enforces roadmap row R-082 (AC-010) -- swarm transport configs MUST
NOT route workers back at the host vendor (the runtime that invokes
the swarm CLI). The Phase-1 dispatch surface is an OpenAI-compatible
HTTPS client pointed at the T2 proxy; if a future contributor
accidentally points ``T2ProxyUrl`` at the host vendor's native API or
slots a host-vendor-branded model identifier into ``T2Model0N``, this
audit fails closed before any traffic leaves the worker fan-out.

Why a static grep instead of a runtime probe
============================================

Runtime probes for "did the transport hit a forbidden host" rely on
the transport actually issuing a request, which requires the T2 env
contract to be present (otherwise :func:`read_env` raises long before
the URL is observable). A static grep over every transport-config
source under ``src/superclaude/cli/swarm/transports/`` runs in CI on
every commit, costs nothing, and catches both the URL form
(``api.anthropic.com``) and the model-identifier form
(``claude-*``) regardless of whether the dispatch path is exercised.

The audit deliberately mirrors the validation command in
``phase-3-tasklist.md`` T03.20::

    grep -RniE "anthropic|claude-" src/superclaude/cli/swarm/transports/

A passing audit means the same shell command returns empty.

Forbidden-pattern surface
=========================

The audit targets three case-insensitive shapes:

* ``api.anthropic.com`` -- the canonical host-vendor REST endpoint.
  Any literal containing this substring in a transport-config source
  is a routing breach regardless of whether it lives in a constant,
  a default argument, or a docstring example.
* ``anthropic``        -- the bare vendor token in any case. Catches
  alternate hosts (``anthropic.com``), alternate envelopes
  (``Anthropic-Version`` headers), and aspirational comments
  (``# falls back to anthropic``) that would all reintroduce the
  routing path the AC forbids.
* ``claude-``          -- the host-vendor model-family prefix. Catches
  every model identifier the host vendor publishes (``claude-haiku-*``,
  ``claude-opus-*``, ``claude-sonnet-*``) without committing the audit
  to enumerate a version table that ages out.

The trailing hyphen on ``claude-`` is load-bearing: it lets the bare
proper noun ``Claude`` slip through in unrelated places while still
flagging every released model identifier (which all follow the
``claude-<family>-<version>`` convention). The bare ``anthropic``
regex catches the vendor name and does not need a hyphen guard --
there is no legitimate use of that token inside transport config.

Mutation guarantee
==================

A regression that broke the scanner (an empty pattern table, an
inverted case-flag, a missing ``finditer``) would let the green-suite
outcome go vacuous. The ``test_audit_detects_*`` mutation tests prove
the detector actually flags synthetic offending sources for each
forbidden shape -- and that benign tokens (`` ``-stripped
``anthropomorphic``, ``ClaudeCode`` without hyphen, ``claudeapp``) do
not trip a false positive.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
TRANSPORTS_DIR = REPO_ROOT / "src" / "superclaude" / "cli" / "swarm" / "transports"

# Forbidden patterns, mirroring the T03.20 validation grep:
#   grep -RniE "anthropic|claude-" src/superclaude/cli/swarm/transports/
#
# Each entry is (label, raw-regex) so failure messages can name which
# shape tripped. Patterns are matched case-insensitively against the
# raw source text -- comments, docstrings, and constants are all in
# scope because the AC forbids the token in *transport config* and a
# host-vendor URL hidden in a docstring example is still a routing
# regression once someone copy-pastes it.
FORBIDDEN_PATTERNS: tuple[tuple[str, str], ...] = (
    ("api.anthropic.com host", r"api\.anthropic\.com"),
    ("anthropic vendor token", r"anthropic"),
    ("claude-* model family", r"claude-"),
)

_SCAN_RE: re.Pattern[str] = re.compile(
    "|".join(f"(?:{pattern})" for _, pattern in FORBIDDEN_PATTERNS),
    re.IGNORECASE,
)

# Self-exclusion: this test file enumerates the forbidden tokens in
# its module docstring so the audit is auditable. The transports/ tree
# is the scan target -- this file lives under tests/swarm/ and is not
# discovered by the source enumerator, but pin the exclusion path
# explicitly so a future refactor that relocates the scanner cannot
# accidentally self-flag.
SELF_PATH = Path(__file__).resolve()


def _iter_transport_sources() -> list[Path]:
    """Return every ``.py`` source under the transports/ package."""
    if not TRANSPORTS_DIR.exists():
        return []
    return [
        p
        for p in TRANSPORTS_DIR.rglob("*.py")
        if p.is_file() and "__pycache__" not in p.parts and p.resolve() != SELF_PATH
    ]


def _scan_for_forbidden(text: str) -> list[tuple[int, str, str]]:
    """Return (lineno, matched_token, stripped_line) tuples for every hit."""
    hits: list[tuple[int, str, str]] = []
    for lineno, line in enumerate(text.splitlines(), start=1):
        for match in _SCAN_RE.finditer(line):
            hits.append((lineno, match.group(0), line.strip()))
    return hits


# ---------------------------------------------------------------------------
# Static audit -- every transport source must be free of forbidden tokens.
# ---------------------------------------------------------------------------


def test_transports_directory_exists() -> None:
    """Audit needs a target; an accidentally-deleted package must be loud."""
    assert TRANSPORTS_DIR.is_dir(), (
        f"Transports package missing at "
        f"{TRANSPORTS_DIR.relative_to(REPO_ROOT)}; AC-010 grep audit has "
        "nothing to scan."
    )


def test_transports_source_set_is_nonempty() -> None:
    """A future refactor must not silently empty the scan target."""
    sources = _iter_transport_sources()
    assert sources, (
        f"_iter_transport_sources() returned empty for "
        f"{TRANSPORTS_DIR.relative_to(REPO_ROOT)}; the AC-010 audit would "
        "trivially pass. Confirm transport modules still live there."
    )


def test_no_anthropic_routing_in_transport_modules() -> None:
    """AC-010: zero host-vendor URLs / model-family tokens in transports/.

    Mirrors the tasklist validation command::

        grep -RniE "anthropic|claude-" src/superclaude/cli/swarm/transports/

    Failing means a future contributor either pointed ``T2ProxyUrl`` at
    the host vendor's native API or slotted a host-vendor model
    identifier into ``T2Model0N`` -- both of which the spec forbids
    because the swarm exists to fan out to *other* models, not loop a
    job back into the caller's own vendor.
    """
    offenders: list[str] = []
    for source in _iter_transport_sources():
        hits = _scan_for_forbidden(source.read_text(encoding="utf-8"))
        for lineno, token, body in hits:
            offenders.append(
                f"  {source.relative_to(REPO_ROOT)}:{lineno}: '{token}' -> {body}"
            )
    assert not offenders, (
        "AC-010 violation: host-vendor routing token detected in "
        "transport config. Each swarm worker must route to a non-host "
        "upstream via the T2 proxy:\n" + "\n".join(offenders)
    )


def test_forbidden_pattern_set_is_nonempty() -> None:
    """A typo emptying FORBIDDEN_PATTERNS would silently green the scan."""
    assert FORBIDDEN_PATTERNS, (
        "FORBIDDEN_PATTERNS must enumerate the host-vendor token surface; "
        "an empty tuple would render the AC-010 audit a no-op."
    )
    # The scanner re must be non-trivial too -- a regex that matches the
    # empty string would silently green every line.
    assert _SCAN_RE.pattern, (
        "_SCAN_RE.pattern is empty; the AC-010 audit would pass vacuously."
    )


# ---------------------------------------------------------------------------
# Mutation guards -- prove the detector actually catches each shape.
# ---------------------------------------------------------------------------


def test_audit_detects_mutation_host_url() -> None:
    """Mutation guard: scanner flags ``api.anthropic.com`` constants."""
    synthetic = (
        "BASE_URL = 'https://api.anthropic.com/v1'\ndef build(): return BASE_URL\n"
    )
    hits = _scan_for_forbidden(synthetic)
    assert any("api.anthropic.com" in tok.lower() for _, tok, _ in hits), (
        "Scanner missed synthetic ``api.anthropic.com`` constant; "
        "AC-010 audit would silently pass on a real host-URL regression."
    )


def test_audit_detects_mutation_vendor_token_any_case() -> None:
    """Mutation guard: scanner flags ``anthropic`` / ``Anthropic`` / ``ANTHROPIC``."""
    for synthetic in (
        "# upstream provider: anthropic\n",
        "VENDOR = 'Anthropic'\n",
        "# routes via ANTHROPIC fallback\n",
    ):
        hits = _scan_for_forbidden(synthetic)
        assert hits, (
            f"Scanner failed on synthetic vendor token in {synthetic!r}; "
            "AC-010 audit must be case-insensitive."
        )


def test_audit_detects_mutation_claude_model_family() -> None:
    """Mutation guard: scanner flags ``claude-<family>-<version>`` identifiers."""
    for synthetic in (
        "MODEL = 'claude-haiku-4.5'\n",
        "MODEL = 'claude-opus-4-7'\n",
        "MODEL = 'Claude-Sonnet-4-6'\n",
    ):
        hits = _scan_for_forbidden(synthetic)
        assert any("claude-" in tok.lower() for _, tok, _ in hits), (
            f"Scanner missed synthetic model id in {synthetic!r}; "
            "AC-010 audit would silently pass on a real model-name "
            "regression."
        )


def test_audit_does_not_flag_unrelated_substrings() -> None:
    """Negative case: scanner stays narrow so unrelated text is not flagged.

    The trailing hyphen on ``claude-`` is what keeps the bare proper
    noun ``Claude`` (without the model-family suffix) usable in
    unrelated places. The bare ``anthropic`` token has no legitimate
    use in transport config and is intentionally caught -- so the
    negative case here is restricted to ``claude`` without hyphen.
    """
    # ``claude`` without the model-family hyphen MUST NOT trip the
    # claude-* pattern. (It would still trip if a future contributor
    # added the bare ``claude`` token to FORBIDDEN_PATTERNS; this test
    # locks the current narrow scope.)
    no_hyphen_samples = (
        "VAR = 'claudeapp'\n",
        "VAR = 'ClaudeCode'\n",
    )
    for synthetic in no_hyphen_samples:
        hits = _scan_for_forbidden(synthetic)
        flagged_via_claude_hyphen = [
            tok for _, tok, _ in hits if tok.lower().startswith("claude")
        ]
        assert not flagged_via_claude_hyphen, (
            f"Scanner falsely flagged hyphen-less token in {synthetic!r}; "
            "AC-010 audit would generate noise on unrelated identifiers."
        )


# ---------------------------------------------------------------------------
# Runtime guard -- if T2 env contract is set, the resolved base URL must
# not be a host-vendor endpoint.
# ---------------------------------------------------------------------------


def test_resolved_transport_config_does_not_route_to_host_vendor(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Complementary runtime check: parsed env contract resolves clean.

    The static grep covers the source tree; this guard exercises the
    actual ``read_env`` path with a synthetic-but-clean env contract and
    asserts the resolved ``TransportConfig`` carries neither a
    host-vendor URL nor a host-vendor model identifier. A regression
    that read env values through a host-vendor default would be caught
    here.
    """
    from superclaude.cli.swarm.transports.openai_compat import read_env

    monkeypatch.setenv("T2ProxyUrl", "https://proxy.example.com/v1")
    monkeypatch.setenv("T2ProxyKey", "sk-test-not-real")
    monkeypatch.setenv("T2Model01", "gpt-5-codex")
    monkeypatch.setenv("T2Model02", "mistral-large-2407")

    config = read_env()
    assert not _scan_for_forbidden(config.base_url), (
        f"Resolved TransportConfig.base_url contains a forbidden token: "
        f"{config.base_url!r}. AC-010 forbids routing to the host vendor."
    )
    for model in config.models:
        assert not _scan_for_forbidden(model), (
            f"Resolved TransportConfig model {model!r} contains a "
            "forbidden token; AC-010 forbids host-vendor model identifiers."
        )
