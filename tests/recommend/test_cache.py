"""Tests for the sc-recommend lookup-cache reader/writer.

Adapted from ``tests/roadmap/test_convergence.py::TestRegistryPersistence``
(save/reload, hash-reset). Adds atomic-write crash safety (Step 3.3).
"""

from __future__ import annotations

import hashlib
from pathlib import Path
from unittest.mock import patch

import pytest

from superclaude.cli.recommend.cache import (
    LookupCache,
    compute_source_hash,
    compute_surface_hash,
)


def _sample_rows() -> list[dict]:
    return [
        {
            "key": "spec-generation",
            "candidate": "/sc:spec-panel",
            "flags": ["--mode discussion|critique|socratic"],
            "prompt_envelope_template": "Run: /sc:spec-panel @{inputs}",
            "rationale": "spec review",
            "source_hash": "a" * 64,
            "last_validated_at": "2026-06-03T00:00:00+00:00",
            "native_fallback": False,
            "best_model": {"model": "opus", "tier": "balanced", "confidence": 0.8},
            "eval_history": [{"run_id": "r1", "eval_mode": "quick", "verdict": "ok"}],
        }
    ]


class TestLookupCachePersistence:
    """YAML round-trip, surface_hash invalidation, full-digest source hash."""

    def test_save_and_reload(self, cache_path: Path):
        """Round-trip preserves header + all row fields (incl. best_model/eval_history)."""
        cache = LookupCache(
            path=cache_path, surface_hash="surf-abc", rows=_sample_rows()
        )
        cache.save()

        loaded = LookupCache.load_or_create(cache_path, "surf-abc")
        assert loaded.schema_version == 2
        assert loaded.surface_hash == "surf-abc"
        assert len(loaded.rows) == 1
        row = loaded.rows[0]
        assert row["key"] == "spec-generation"
        assert row["candidate"] == "/sc:spec-panel"
        assert row["flags"] == ["--mode discussion|critique|socratic"]
        assert row["native_fallback"] is False
        assert row["best_model"]["model"] == "opus"
        assert row["eval_history"][0]["run_id"] == "r1"

    def test_surface_hash_invalidation_resets_rows(self, cache_path: Path):
        """Loading with a DIFFERENT surface_hash than stored discards the rows."""
        cache = LookupCache(
            path=cache_path, surface_hash="surf-OLD", rows=_sample_rows()
        )
        cache.save()

        loaded = LookupCache.load_or_create(cache_path, "surf-NEW")
        assert loaded.rows == []
        assert loaded.surface_hash == "surf-NEW"

    def test_source_hash_full_digest(self):
        """The per-row source_hash helper returns a FULL 64-char sha256 hexdigest."""
        digest = compute_source_hash(b"some candidate source bytes")
        assert len(digest) == 64
        assert digest == hashlib.sha256(b"some candidate source bytes").hexdigest()
        assert all(c in "0123456789abcdef" for c in digest)

    def test_surface_hash_is_full_digest(self, tmp_path: Path):
        """compute_surface_hash returns a full 64-char hexdigest over the glob output."""
        # Empty base dir -> hashes the empty joined string, still a full digest.
        digest = compute_surface_hash(base=tmp_path)
        assert len(digest) == 64
        assert all(c in "0123456789abcdef" for c in digest)


class TestLookupCacheRowOps:
    """get_row / upsert_row helpers used by the CLI surface."""

    def test_get_row_returns_match_or_none(self):
        cache = LookupCache(path=Path("x.yaml"), surface_hash="s", rows=_sample_rows())
        assert cache.get_row("spec-generation")["candidate"] == "/sc:spec-panel"
        assert cache.get_row("nonexistent") is None

    def test_upsert_replaces_existing_key(self):
        cache = LookupCache(path=Path("x.yaml"), surface_hash="s", rows=_sample_rows())
        cache.upsert_row({"key": "spec-generation", "candidate": "/sc:other"})
        assert len(cache.rows) == 1
        assert cache.get_row("spec-generation")["candidate"] == "/sc:other"

    def test_upsert_appends_new_key(self):
        cache = LookupCache(path=Path("x.yaml"), surface_hash="s", rows=_sample_rows())
        cache.upsert_row({"key": "tasklist-generation", "candidate": "/sc:tasklist"})
        assert len(cache.rows) == 2
        assert cache.get_row("tasklist-generation") is not None


class TestLookupCacheAtomicWrite:
    """Step 3.3 — atomic-write crash safety (os.replace failure)."""

    def test_atomic_write_no_partial_on_crash(self, cache_path: Path):
        """If os.replace raises, the original file is unchanged and no temp file lingers."""
        # Seed an initial committed cache.
        original = LookupCache(
            path=cache_path, surface_hash="surf-orig", rows=_sample_rows()
        )
        original.save()
        before = cache_path.read_text(encoding="utf-8")

        # Attempt a save whose os.replace fails mid-commit.
        mutated = LookupCache(
            path=cache_path,
            surface_hash="surf-orig",
            rows=[{"key": "should-not-land", "candidate": "/sc:nope"}],
        )
        with patch(
            "superclaude.cli.recommend.cache.os.replace",
            side_effect=OSError("simulated crash"),
        ):
            with pytest.raises(OSError):
                mutated.save()

        # Original content is intact (no partial write).
        assert cache_path.read_text(encoding="utf-8") == before
        # No stray temp file left in the directory.
        leftover = [p for p in cache_path.parent.iterdir() if p.name != cache_path.name]
        assert leftover == [], f"stray temp files: {leftover}"
