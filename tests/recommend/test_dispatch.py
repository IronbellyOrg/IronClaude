"""Tests for the Option-P deterministic hot-path dispatch + cache round-trip.

Covers the five dispatch outcomes (hit / native / 4 miss reasons) and the
critical cold-insert→warm-to-hit round-trip (the CLI `cache put` recomputing
source_hash so the next lookup validates).
"""

from __future__ import annotations

import json
from pathlib import Path

from click.testing import CliRunner

from superclaude.cli.recommend.cache import LookupCache, compute_source_hash
from superclaude.cli.recommend.commands import recommend_group
from superclaude.cli.recommend.dispatch import dispatch


def _seed(cache_path: Path, source_file: Path) -> None:
    """Seed a one-row cache validating against a real source file."""
    source_file.write_text("candidate source body\n", encoding="utf-8")
    row = {
        "key": "spec-generation",
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
        _seed(cache_path, tmp_path / "src.md")
        r = dispatch(
            classification_key="spec-generation",
            native_likely=False,
            confidence_top2_delta=0.5,
            cache_path=cache_path,
        )
        assert r.outcome == "hit"
        assert r.cache_result == "hit"
        assert r.recommendation == "Run: /sc:spec-panel @{inputs}"
        assert r.needs_cold_path is False

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
            classification_key="spec-generation",
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
            classification_key="spec-generation",
            native_likely=False,
            confidence_top2_delta=0.5,
            cache_path=cache_path,
        )
        assert r.cache_result == "miss_validation_stale"

    def test_miss_budget_exceeded(self, cache_path: Path, tmp_path: Path):
        _seed(cache_path, tmp_path / "src.md")
        r = dispatch(
            classification_key="spec-generation",
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
            "key": "spec-generation",
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
        committed = cache.get_row("spec-generation")
        assert committed["source_hash"] == compute_source_hash(source_file.read_bytes())
        assert len(committed["source_hash"]) == 64

        # And the next dispatch warms to a HIT.
        r = dispatch(
            classification_key="spec-generation",
            native_likely=False,
            confidence_top2_delta=0.5,
            cache_path=cache_path,
        )
        assert r.outcome == "hit"
