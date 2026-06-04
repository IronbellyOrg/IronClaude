"""Tests for the --eval grader, aggregation, and pipeline finalize round-trip."""

from __future__ import annotations

import json
from pathlib import Path

from superclaude.cli.recommend.cache import LookupCache, compute_surface_hash
from superclaude.cli.recommend.eval_aggregate import (
    MODE_MATRIX,
    aggregate_by_model,
    make_run_record,
)
from superclaude.cli.recommend.eval_grader import check, grade_text
from superclaude.cli.recommend.eval_pipeline import finalize_eval


class TestGrader:
    def test_five_assertion_types(self):
        text = "Run: /sc:spec-panel for the spec"
        assert check({"type": "string_contains", "value": "spec-panel"}, text)[0]
        assert check({"type": "string_not_contains", "value": "tasklist"}, text)[0]
        assert check({"type": "regex_match", "value": r"/sc:\w+"}, text)[0]
        assert check({"type": "regex_match_not", "value": r"DELEGATE"}, text)[0]
        assert check({"type": "max_length_check", "value": 1000}, text)[0]

    def test_grade_text_pass_rate(self):
        g = grade_text(
            eval_id="spec-generation",
            eval_name="spec",
            configuration="opus",
            assertions=[
                {"text": "has panel", "type": "string_contains", "value": "spec-panel"},
                {"text": "no fab", "type": "string_contains", "value": "MISSING"},
            ],
            text="Run: /sc:spec-panel",
        )
        assert g["pass_rate"] == 0.5
        assert g["expectations"][0]["passed"] is True
        assert g["expectations"][1]["passed"] is False


class TestAggregate:
    def test_mode_matrix_panels(self):
        assert MODE_MATRIX["quick"] == {"models": ["opus"], "runs_per_model": 1}
        assert MODE_MATRIX["deep"]["models"] == ["opus", "sonnet", "haiku"]

    def test_aggregate_by_model(self):
        g = grade_text(
            eval_id="k",
            eval_name="k",
            configuration="opus",
            assertions=[{"text": "t", "type": "string_contains", "value": "x"}],
            text="x",
        )
        runs = [
            make_run_record(
                eval_id="k",
                eval_name="k",
                model="opus",
                run_number=1,
                grading=g,
                timing={"total_tokens": 100, "total_duration_seconds": 5},
            )
        ]
        agg = aggregate_by_model(runs)
        assert agg["opus"]["pass_rate"] == 1.0
        assert agg["opus"]["mean_tokens"] == 100
        assert agg["opus"]["n_runs"] == 1


class TestFinalizeRoundTrip:
    def test_finalize_writes_results_and_patches_row(
        self, cache_path: Path, tmp_path: Path
    ):
        # Seed a lookup row for the key.
        cache = LookupCache(
            path=cache_path,
            surface_hash=compute_surface_hash(),
            rows=[
                {
                    "key": "spec-generation",
                    "candidate": "/sc:spec-panel",
                    "best_model": None,
                }
            ],
        )
        cache.save()

        g = grade_text(
            eval_id="spec-generation",
            eval_name="spec",
            configuration="opus",
            assertions=[{"text": "t", "type": "string_contains", "value": "panel"}],
            text="panel",
        )
        runs = [
            make_run_record(
                eval_id="spec-generation",
                eval_name="spec",
                model="opus",
                run_number=1,
                grading=g,
                timing={"total_tokens": 90_000, "total_duration_seconds": 70},
            )
        ]
        eval_runs_dir = tmp_path / "eval-runs" / "iteration-1"
        results = finalize_eval(
            key="spec-generation",
            iteration=1,
            mode="quick",
            runs=runs,
            eval_runs_dir=eval_runs_dir,
            cache_path=cache_path,
        )

        # results JSON written
        rj = eval_runs_dir / "row-spec-generation-results.json"
        assert rj.exists()
        on_disk = json.loads(rj.read_text())
        assert on_disk["key"] == "spec-generation"
        assert on_disk["eval_mode"] == "quick"

        # lookup row patched with best_model + eval_history
        reloaded = LookupCache.load_or_create(cache_path, compute_surface_hash())
        row = reloaded.get_row("spec-generation")
        # single-model panel -> best_model present (confidence 1.0, not suppressed)
        assert row["best_model"] is not None
        assert row["best_model"]["model"] == "opus"
        assert len(row["eval_history"]) == 1
        assert row["eval_history"][0]["eval_mode"] == "quick"
        assert results["models_tested"] == ["opus"]
