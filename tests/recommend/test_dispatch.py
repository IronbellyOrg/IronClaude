"""Tests for the Option-P deterministic hot-path dispatch + cache round-trip.

Covers the five dispatch outcomes (hit / native / 4 miss reasons) and the
critical cold-insert→warm-to-hit round-trip (the CLI `cache put` recomputing
source_hash so the next lookup validates).
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from click.testing import CliRunner

from superclaude.cli.recommend.cache import LookupCache, compute_source_hash
from superclaude.cli.recommend.commands import recommend_group
from superclaude.cli.recommend.dispatch import dispatch


def _seed(cache_path: Path, source_file: Path) -> None:
    """Seed a one-row cache validating against a real source file."""
    source_file.write_text("candidate source body\n", encoding="utf-8")
    row = {
        "key": "adversarial-review",
        "candidate": "/sc:spec-panel",
        "flags": ["--mode discussion"],
        "prompt_envelope_template": "Run: /sc:spec-panel @{inputs}",
        "rationale": "spec",
        "source_path": str(source_file),
        "source_hash": compute_source_hash(source_file.read_bytes()),
        "last_validated_at": "2026-06-03T00:00:00+00:00",
        "native_fallback": False,
        "best_model": None,
    }
    # surface_hash is computed by dispatch against the real src tree; we store the
    # SAME value so load_or_create keeps the row.
    from superclaude.cli.recommend.cache import compute_surface_hash

    cache = LookupCache(
        path=cache_path, surface_hash=compute_surface_hash(), rows=[row]
    )
    cache.save()


class TestDispatchOutcomes:
    def test_hit(self, cache_path: Path, tmp_path: Path):
        """Dispatch transports a hint; the skill must verify and bind it."""
        _seed(cache_path, tmp_path / "src.md")
        r = dispatch(
            classification_key="adversarial-review",
            native_likely=False,
            confidence_top2_delta=0.5,
            cache_path=cache_path,
        )
        assert r.outcome == "hit"
        assert r.cache_result == "hit"
        assert r.candidate == "/sc:spec-panel"
        # Raw transport deliberately does not bind this to the current request.
        assert r.recommendation == "Run: /sc:spec-panel @{inputs}"
        assert r.needs_cold_path is False
        assert set(r.to_dict()) == {
            "outcome",
            "cache_result",
            "miss_reason",
            "recommendation",
            "best_model_hint",
            "candidate",
            "needs_cold_path",
        }

    def test_native_likely(self, cache_path: Path):
        r = dispatch(
            classification_key="anything",
            native_likely=True,
            confidence_top2_delta=0.9,
            cache_path=cache_path,
        )
        assert r.outcome == "native"
        assert r.cache_result is None
        assert r.needs_cold_path is False

    def test_miss_no_key_unknown(self, cache_path: Path):
        r = dispatch(
            classification_key="unknown",
            native_likely=False,
            confidence_top2_delta=0.9,
            cache_path=cache_path,
        )
        assert r.cache_result == "miss_no_key"
        assert r.needs_cold_path is True

    def test_miss_low_confidence(self, cache_path: Path, tmp_path: Path):
        _seed(cache_path, tmp_path / "src.md")
        r = dispatch(
            classification_key="adversarial-review",
            native_likely=False,
            confidence_top2_delta=0.05,
            cache_path=cache_path,
        )
        assert r.cache_result == "miss_low_confidence"

    def test_miss_validation_stale_on_hash_drift(
        self, cache_path: Path, tmp_path: Path
    ):
        src = tmp_path / "src.md"
        _seed(cache_path, src)
        # Mutate the source file so its hash no longer matches the stored one.
        src.write_text("MUTATED body\n", encoding="utf-8")
        r = dispatch(
            classification_key="adversarial-review",
            native_likely=False,
            confidence_top2_delta=0.5,
            cache_path=cache_path,
        )
        assert r.cache_result == "miss_validation_stale"

    def test_miss_budget_exceeded(self, cache_path: Path, tmp_path: Path):
        _seed(cache_path, tmp_path / "src.md")
        r = dispatch(
            classification_key="adversarial-review",
            native_likely=False,
            confidence_top2_delta=0.5,
            cache_path=cache_path,
            budget_tokens_used=20_000,
            budget_limit=10_000,
        )
        assert r.cache_result == "miss_budget_exceeded"


class TestColdInsertWarmsToHit:
    """The critical round-trip the structural gate caught: cache put must recompute source_hash."""

    def test_cache_put_recomputes_source_hash_then_dispatch_hits(
        self, cache_path: Path, tmp_path: Path
    ):
        source_file = tmp_path / "candidate.md"
        source_file.write_text("real candidate source\n", encoding="utf-8")
        # Cold path returns a row WITHOUT source_hash (Haiku cannot hash).
        row = {
            "key": "adversarial-review",
            "candidate": "/sc:spec-panel",
            "flags": [],
            "prompt_envelope_template": "Run: /sc:spec-panel @{inputs}",
            "rationale": "spec",
            "source_path": str(source_file),
            "native_fallback": False,
            "best_model": None,
        }
        runner = CliRunner()
        res = runner.invoke(
            recommend_group,
            [
                "cache",
                "put",
                "--cache-path",
                str(cache_path),
                "--row-json",
                json.dumps(row),
            ],
        )
        assert res.exit_code == 0, res.output

        # The committed row now has a recomputed full-digest source_hash.
        from superclaude.cli.recommend.cache import compute_surface_hash

        cache = LookupCache.load_or_create(cache_path, compute_surface_hash())
        committed = cache.get_row("adversarial-review")
        assert committed["source_hash"] == compute_source_hash(source_file.read_bytes())
        assert len(committed["source_hash"]) == 64

        # And the next dispatch warms to a HIT.
        r = dispatch(
            classification_key="adversarial-review",
            native_likely=False,
            confidence_top2_delta=0.5,
            cache_path=cache_path,
        )
        assert r.outcome == "hit"


# Ordered as the case sub-lines appear in SKILL.md (verification, binding,
# rejection), so the cross-case matrix below must be exactly the identity.
_COLLISION_CASES = [
    pytest.param(
        "Review the spec using its changed backing references",
        "adversarial-review",
        "/sc:spec-panel",
        "Run: /sc:spec-panel docs/previous.md",
        "reference",
        "Cached source hash",
        "current changed delegated reference",
        "reread",
        "verification",
        id="T56-reference-only-change",
    ),
    pytest.param(
        "Critique docs/current.md without changes",
        "adversarial-review",
        "/sc:spec-panel",
        "Run: /sc:spec-panel docs/previous.md",
        "path",
        "Cached same-key envelope path",
        "current different path",
        "rebind",
        "binding",
        id="T55-same-key-new-input-path",
    ),
    pytest.param(
        "Audit completed work against its plan",
        "adversarial-review",
        "/sc:adversarial",
        "Run: /sc:adversarial --compare docs/a.md,docs/b.md",
        "objective",
        "Cached comparison hint",
        "current plan-adherence audit",
        "reject",
        "rejection",
        id="T52-comparison-is-not-adherence-audit",
    ),
    pytest.param(
        "Review PR 42 locally without posting",
        "adversarial-review",
        "/sc:adversarial",
        "Run: /sc:adversarial --compare docs/a.md,docs/b.md",
        "objective",
        "Cached comparison hint",
        "current local PR review with no posting",
        "reject",
        "rejection",
        id="T52-comparison-is-not-local-PR-review",
    ),
    pytest.param(
        "Create a Technical Design Document from docs/prd.md",
        "spec-generation",
        "/prd",
        "Run: /prd docs/raw.md",
        "objective",
        "Cached PRD-authoring hint",
        "current TDD request",
        "reject",
        "rejection",
        id="T53-PRD-authoring-is-not-TDD",
    ),
    pytest.param(
        "Critique the existing spec docs/specs/current-spec.md without rewriting it",
        "spec-generation",
        "/prd",
        "Run: /prd docs/raw.md",
        "objective",
        "Cached PRD-authoring hint",
        "current existing-spec critique",
        "reject",
        "rejection",
        id="T53-PRD-authoring-is-not-existing-spec-critique",
    ),
    pytest.param(
        "Create a Sprint bundle from docs/roadmap.md",
        "task-file-generation",
        "/task-builder",
        'Run: /task-builder "Create an MDTM task from docs/spec.md"',
        "objective",
        "Cached MDTM or roadmap hint",
        "current Sprint artifacts request",
        "reject",
        "rejection",
        id="T54-MDTM-is-not-Sprint-artifacts",
    ),
    pytest.param(
        "Assess effort without resurrecting a retired command",
        "spec-generation",
        "/sc:estimate",
        "Run: /sc:estimate docs/spec.md",
        "retired",
        "Cached retired-target hint",
        "with a valid source hash",
        "reject",
        "rejection",
        id="T48-hash-valid-retired-candidate",
    ),
]

_SOURCE_BODIES = {
    "objective": "Usage: {candidate} <inputs>\n",
    "path": "Usage: {candidate} <inputs>\n",
    "reference": "Usage: {candidate} <inputs>\nRead backing-reference.md first.\n",
    "retired": "---\ndeprecated: true\n---\nUsage: {candidate} <inputs>\n",
}


def _hot_sections() -> dict[str, str]:
    policy = (
        Path(__file__).resolve().parents[2]
        / "src/superclaude/skills/sc-recommend/SKILL.md"
    ).read_text(encoding="utf-8")
    hot = policy.split("3. **Interpret the outcome; a hit is only a hint:**", 1)[1]
    hot = hot.split("## Phase 0", 1)[0]
    verification, tail = hot.split("- If compatible and eligible,", 1)
    binding, rejection = tail.split("- If the hint is incompatible,", 1)
    rejection = rejection.split('- `outcome: "native"`', 1)[0]
    return {
        "verification": verification,
        "binding": binding,
        "rejection": rejection,
    }


def _case_lines(text: str) -> list[str]:
    return [line for line in text.splitlines() if "  - Cached " in line]


def _names_case(line: str, cached_phrase: str, current_phrase: str) -> bool:
    folded = line.casefold()
    return cached_phrase.casefold() in folded and current_phrase.casefold() in folded


@pytest.mark.parametrize(
    "current_request,key,candidate,envelope,hazard,cached_phrase,current_phrase,verb,section",
    _COLLISION_CASES,
)
def test_semantic_cache_collisions_require_consumer_guards(
    cache_path: Path,
    tmp_path: Path,
    current_request: str,
    key: str,
    candidate: str,
    envelope: str,
    hazard: str,
    cached_phrase: str,
    current_phrase: str,
    verb: str,
    section: str,
):
    """Exercise raw valid-hash hints and pin their required static consumer guards.

    No agent is run here. A transport hit is deliberately not a claim that the
    current request has been understood, rebound or safely authorized. No model
    and no specialist command runs here either; these are static transport and
    policy-text checks, while actual generation evidence stays with plan Task 8.
    """
    source = tmp_path / "candidate.md"
    reference = tmp_path / "backing-reference.md"
    reference.write_text("previous contract\n", encoding="utf-8")
    _seed(cache_path, source)
    source.write_text(_SOURCE_BODIES[hazard].format(candidate=candidate), "utf-8")
    from superclaude.cli.recommend.cache import compute_surface_hash

    cache = LookupCache.load_or_create(cache_path, compute_surface_hash())
    row = dict(cache.rows[0])
    row.update(
        key=key,
        candidate=candidate,
        flags=[],
        prompt_envelope_template=envelope,
        source_hash=compute_source_hash(source.read_bytes()),
    )
    cache.upsert_row(row)
    cache.save()
    if hazard == "reference":
        # The hashed source names this file; changing it leaves the hash valid.
        assert reference.name in source.read_text(encoding="utf-8")
        reference.write_text("changed contract\n", encoding="utf-8")
    assert compute_source_hash(source.read_bytes()) == row["source_hash"]
    result = dispatch(
        classification_key=key,
        native_likely=False,
        confidence_top2_delta=0.5,
        cache_path=cache_path,
    )
    assert result.outcome == "hit"
    assert result.recommendation == envelope
    assert result.candidate == candidate

    # The hazard is real in this fixture's data, and dispatch cannot see it.
    if hazard == "objective":
        tokens = {"--compare", "/prd", "/task-builder"} & set(envelope.split())
        assert len(tokens) == 1, envelope
        assert tokens.pop() not in current_request.split()
    elif hazard == "path":
        assert "docs/previous.md" in result.recommendation
        assert "docs/previous.md" not in current_request
    elif hazard == "retired":
        assert "deprecated: true" in source.read_text(encoding="utf-8")

    sections = _hot_sections()
    for term in (
        "retired",
        "unavailable",
        "contradictory",
        "reject it and use live Phase 0-2 discovery",
        "Do not log a hit for a rejected hint",
    ):
        assert term in sections["rejection"], current_request

    owned = [
        line
        for line in sections[section].splitlines()
        if _names_case(line, cached_phrase, current_phrase)
    ]
    assert len(owned) == 1, f"{current_request}: expected one case clause"
    assert "  - Cached " in owned[0]
    assert verb in owned[0]
    if section != "rejection":
        assert "reject" not in owned[0]
    for other, text in sections.items():
        if other != section:
            assert not [line for line in _case_lines(text) if verb in line], other


def test_collision_case_clauses_map_one_to_one():
    """Every case clause belongs to exactly one fixture, and vice versa."""
    sections = _hot_sections()
    lines = _case_lines("".join(sections.values()))
    cases = [case.values for case in _COLLISION_CASES]
    matrix = [
        [int(_names_case(line, case[5], case[6])) for line in lines] for case in cases
    ]
    size = len(cases)
    assert size == 8
    assert matrix == [[int(i == j) for j in range(size)] for i in range(size)]
