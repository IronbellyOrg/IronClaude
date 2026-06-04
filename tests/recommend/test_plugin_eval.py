"""Tests for the plugin eval gate (precondition HARD-BLOCK + adoption gate + row patch).

Closes the F4 remediation's "untested" half: the plugin_eval helpers were correct in
isolation but had no durable test. All tests use tmp_path — never the real
.claude/cache/sc-recommend-plugin.yaml.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from superclaude.cli.recommend.cache import LookupCache, compute_surface_hash
from superclaude.cli.recommend.plugin_eval import (
    PluginPreconditionError,
    evaluate_adoption,
    patch_plugin_row,
    run_preconditions,
)


class TestRunPreconditions:
    def test_hard_block_raises(self):
        """A missing mcp_server with failure_mode: hard raises PluginPreconditionError."""
        with pytest.raises(PluginPreconditionError):
            run_preconditions(
                [
                    {
                        "kind": "mcp_server_installed",
                        "server": "definitely-not-installed-xyz",
                        "failure_mode": "hard",
                        "failure_message": "install the server first",
                    }
                ]
            )

    @pytest.mark.parametrize("mode", ["warn", "skip"])
    def test_warn_and_skip_do_not_raise(self, mode: str):
        """warn/skip preconditions are returned as issues without raising."""
        issues = run_preconditions(
            [
                {
                    "kind": "binary_available",
                    "binary": "definitely-not-a-real-binary-xyz",
                    "failure_mode": mode,
                    "failure_message": "optional dependency",
                }
            ]
        )
        assert len(issues) == 1
        assert issues[0]["failure_mode"] == mode

    def test_satisfied_precondition_returns_empty(self, tmp_path: Path):
        """A satisfied file_present precondition yields no issues."""
        f = tmp_path / "present.txt"
        f.write_text("x", encoding="utf-8")
        assert run_preconditions([{"kind": "file_present", "path": str(f)}]) == []


class TestEvaluateAdoption:
    def test_pass_rate_gain_is_positive(self):
        v = evaluate_adoption(
            {"pass_rate": 0.95, "mean_tokens": 1000},
            {"pass_rate": 0.80, "mean_tokens": 1000},
        )
        assert v["adoption_status"] == "evaluated_positive"
        assert v["pass_rate_delta"] == 0.15
        assert v["regressed"] is False

    def test_token_drop_is_positive(self):
        v = evaluate_adoption(
            {"pass_rate": 0.80, "mean_tokens": 700},
            {"pass_rate": 0.80, "mean_tokens": 1000},
        )
        assert v["adoption_status"] == "evaluated_positive"
        assert v["token_delta"] == -0.3

    def test_pass_rate_regression_is_negative_even_with_token_drop(self):
        v = evaluate_adoption(
            {"pass_rate": 0.70, "mean_tokens": 500},
            {"pass_rate": 0.80, "mean_tokens": 1000},
        )
        assert v["adoption_status"] == "evaluated_negative"
        assert v["regressed"] is True


class TestPatchPluginRow:
    def test_patch_round_trip(self, tmp_path: Path):
        """patch_plugin_row writes adoption_status + a one-entry eval_history, reloadable."""
        plugin_path = tmp_path / "sc-recommend-plugin.yaml"
        verdict = evaluate_adoption(
            {"pass_rate": 0.95, "mean_tokens": 800},
            {"pass_rate": 0.80, "mean_tokens": 1000},
        )
        patch_plugin_row(plugin_path=plugin_path, key="notion-mcp", verdict=verdict)

        cache = LookupCache.load_or_create(plugin_path, compute_surface_hash())
        row = cache.get_row("notion-mcp")
        assert row is not None
        assert row["adoption_status"] == "evaluated_positive"
        assert len(row["eval_history"]) == 1
        assert row["eval_history"][0]["verdict"] == "evaluated_positive"
        # The write landed under tmp_path, never the real .claude/cache/.
        assert plugin_path.exists()
        assert tmp_path in plugin_path.parents
