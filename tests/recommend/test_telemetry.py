"""Tests for the sc-recommend telemetry JSONL appender.

Verifies the closed 5-field event shape and the 6-value cache_result enum
validation (research/04 §2.8).
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from superclaude.cli.recommend.telemetry import EVENT_FIELDS, append_event


class TestTelemetryAppend:
    def test_append_event_writes_exactly_five_fields(self, events_path: Path):
        """A single appended event parses to EXACTLY the 5 named keys, no others."""
        append_event(
            events_path,
            mode="delegate",
            cache_result="hit",
            classification_key="spec-generation",
            duration_ms=4200,
        )
        lines = events_path.read_text(encoding="utf-8").splitlines()
        assert len(lines) == 1
        obj = json.loads(lines[0])
        assert set(obj.keys()) == set(EVENT_FIELDS)
        assert set(obj.keys()) == {
            "ts",
            "mode",
            "cache_result",
            "classification_key",
            "duration_ms",
        }
        assert obj["mode"] == "delegate"
        assert obj["cache_result"] == "hit"
        assert obj["classification_key"] == "spec-generation"
        assert obj["duration_ms"] == 4200

    def test_append_event_is_line_oriented(self, events_path: Path):
        """Two appends produce two newline-separated JSON lines."""
        append_event(
            events_path,
            mode="delegate",
            cache_result="hit",
            classification_key="spec-generation",
            duration_ms=10,
        )
        append_event(
            events_path,
            mode="delegate",
            cache_result="cold_inserted",
            classification_key="tasklist-generation",
            duration_ms=20,
        )
        lines = events_path.read_text(encoding="utf-8").splitlines()
        assert len(lines) == 2
        assert json.loads(lines[0])["cache_result"] == "hit"
        assert json.loads(lines[1])["cache_result"] == "cold_inserted"

    @pytest.mark.parametrize(
        "bad_value",
        ["miss", "HIT", "cold", "success", "", "miss_unknown"],
    )
    def test_invalid_cache_result_rejected(self, events_path: Path, bad_value: str):
        """A cache_result outside the closed 6-value enum raises ValueError."""
        with pytest.raises(ValueError):
            append_event(
                events_path,
                mode="delegate",
                cache_result=bad_value,
                classification_key="spec-generation",
                duration_ms=5,
            )
        # Nothing should have been written on rejection.
        assert not events_path.exists() or events_path.read_text() == ""

    def test_all_six_valid_cache_results_accepted(self, events_path: Path):
        """Each of the 6 valid cache_result values is accepted."""
        valid = [
            "hit",
            "miss_no_key",
            "miss_low_confidence",
            "miss_validation_stale",
            "miss_budget_exceeded",
            "cold_inserted",
        ]
        for value in valid:
            append_event(
                events_path,
                mode="delegate",
                cache_result=value,
                classification_key="k",
                duration_ms=1,
            )
        lines = events_path.read_text(encoding="utf-8").splitlines()
        assert len(lines) == len(valid)
