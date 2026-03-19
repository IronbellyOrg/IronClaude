"""Tests for --resume agent/depth state restoration and dependency-aware resume logic.

Covers Bug 1 (agent restoration), Bug 2 (gate diagnostics), Bug 3 (dependency-aware
_apply_resume), and Bug 4 (_save_state defense-in-depth guards).
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

import pytest

from superclaude.cli.pipeline.models import GateCriteria, Step, StepResult, StepStatus
from superclaude.cli.roadmap.executor import (
    _apply_resume,
    _restore_from_state,
    _save_state,
    _step_needs_rerun,
    read_state,
)
from superclaude.cli.roadmap.models import AgentSpec, RoadmapConfig


def _make_gate() -> GateCriteria:
    return GateCriteria(
        required_frontmatter_fields=[],
        min_lines=1,
        enforcement_tier="LIGHT",
    )


def _make_step(
    id: str,
    output_file: Path,
    gate: GateCriteria | None = None,
    inputs: list[Path] | None = None,
) -> Step:
    return Step(
        id=id,
        prompt=f"prompt for {id}",
        output_file=output_file,
        gate=gate,
        timeout_seconds=300,
        inputs=inputs or [],
    )


def _make_result(step: Step, status: StepStatus = StepStatus.PASS) -> StepResult:
    return StepResult(
        step=step,
        status=status,
        attempt=1,
        started_at=datetime.now(timezone.utc),
        finished_at=datetime.now(timezone.utc),
    )


_UNSET = object()


def _make_config(tmp_path: Path, agents=_UNSET, depth=_UNSET) -> RoadmapConfig:
    spec = tmp_path / "spec.md"
    if not spec.exists():
        spec.write_text("# Spec\nSome content\n")
    kwargs: dict = {
        "spec_file": spec,
        "output_dir": tmp_path,
        "work_dir": tmp_path,
    }
    if agents is not _UNSET:
        kwargs["agents"] = agents
    if depth is not _UNSET:
        kwargs["depth"] = depth
    return RoadmapConfig(**kwargs)


# ===========================================================================
# Bug 1: Agent Restoration Tests
# ===========================================================================


class TestRestoreFromState:
    """Tests for _restore_from_state: agent and depth restoration on resume."""

    def test_restores_agents_from_state(self, tmp_path):
        """Resume without --agents restores original agents from state."""
        state = {
            "schema_version": 1,
            "agents": [
                {"model": "opus", "persona": "architect"},
                {"model": "haiku", "persona": "analyzer"},
            ],
            "spec_hash": "abc123",
        }
        (tmp_path / ".roadmap-state.json").write_text(json.dumps(state))

        config = _make_config(
            tmp_path,
            agents=[AgentSpec("opus", "architect"), AgentSpec("haiku", "architect")],
        )

        restored = _restore_from_state(config, agents_explicit=False, depth_explicit=True)
        assert restored.agents[1].persona == "analyzer"
        assert restored.agents[1].model == "haiku"

    def test_explicit_agents_override_state(self, tmp_path):
        """When --agents is passed explicitly, it overrides state file."""
        state = {
            "agents": [
                {"model": "opus", "persona": "architect"},
                {"model": "haiku", "persona": "analyzer"},
            ],
        }
        (tmp_path / ".roadmap-state.json").write_text(json.dumps(state))

        config = _make_config(
            tmp_path,
            agents=[AgentSpec("sonnet", "security"), AgentSpec("haiku", "qa")],
        )

        restored = _restore_from_state(config, agents_explicit=True, depth_explicit=True)
        assert restored.agents[0].persona == "security"
        assert restored.agents[0].model == "sonnet"

    def test_missing_state_file_graceful(self, tmp_path):
        """Missing state file falls back to current config agents."""
        config = _make_config(
            tmp_path,
            agents=[AgentSpec("opus", "architect"), AgentSpec("haiku", "architect")],
        )

        restored = _restore_from_state(config, agents_explicit=False, depth_explicit=False)
        assert restored.agents == config.agents

    def test_restores_depth_from_state(self, tmp_path):
        """Resume without --depth restores original depth from state."""
        state = {
            "agents": [{"model": "opus", "persona": "architect"}],
            "depth": "deep",
        }
        (tmp_path / ".roadmap-state.json").write_text(json.dumps(state))

        config = _make_config(tmp_path)
        restored = _restore_from_state(config, agents_explicit=False, depth_explicit=False)
        assert restored.depth == "deep"

    def test_explicit_depth_overrides_state(self, tmp_path):
        """When --depth is passed explicitly, it overrides state file."""
        state = {
            "agents": [{"model": "opus", "persona": "architect"}],
            "depth": "deep",
        }
        (tmp_path / ".roadmap-state.json").write_text(json.dumps(state))

        config = _make_config(
            tmp_path,
            agents=[AgentSpec("opus", "architect")],
            depth="standard",
        )
        restored = _restore_from_state(config, agents_explicit=True, depth_explicit=True)
        assert restored.depth == "standard"

    def test_malformed_agents_in_state(self, tmp_path, caplog):
        """Malformed agents in state file falls back to CLI agents."""
        state = {
            "agents": [{"model": "opus"}],  # missing "persona" key
        }
        (tmp_path / ".roadmap-state.json").write_text(json.dumps(state))

        original_agents = [AgentSpec("opus", "architect")]
        config = _make_config(tmp_path, agents=original_agents)

        restored = _restore_from_state(config, agents_explicit=False, depth_explicit=True)
        assert restored.agents == original_agents

    def test_corrupted_state_file_graceful(self, tmp_path):
        """Corrupted state file falls back to CLI agents."""
        (tmp_path / ".roadmap-state.json").write_text("NOT VALID JSON{{{")

        original_agents = [AgentSpec("opus", "architect")]
        config = _make_config(tmp_path, agents=original_agents)

        restored = _restore_from_state(config, agents_explicit=False, depth_explicit=False)
        assert restored.agents == original_agents

    def test_double_resume_stability(self, tmp_path):
        """Run, resume, resume again -- agents stable across all three."""
        original_agents = [
            AgentSpec("opus", "architect"),
            AgentSpec("haiku", "analyzer"),
        ]
        spec = tmp_path / "spec.md"
        spec.write_text("# Spec")

        # First run saves state
        config1 = RoadmapConfig(
            agents=original_agents,
            depth="deep",
            output_dir=tmp_path,
            work_dir=tmp_path,
            spec_file=spec,
        )
        extract_step = _make_step("extract", tmp_path / "extraction.md")
        gen_step = _make_step("generate-opus-architect", tmp_path / "roadmap-opus-architect.md")
        results1 = [_make_result(extract_step), _make_result(gen_step)]
        _save_state(config1, results1)

        # First resume (omit agents/depth to simulate Click defaulting)
        config2 = RoadmapConfig(
            output_dir=tmp_path, work_dir=tmp_path, spec_file=spec,
        )
        restored2 = _restore_from_state(config2, agents_explicit=False, depth_explicit=False)
        assert restored2.agents == original_agents
        assert restored2.depth == "deep"

        # Save state again with restored config
        _save_state(restored2, results1)

        # Second resume
        config3 = RoadmapConfig(
            output_dir=tmp_path, work_dir=tmp_path, spec_file=spec,
        )
        restored3 = _restore_from_state(config3, agents_explicit=False, depth_explicit=False)
        assert restored3.agents == original_agents
        assert restored3.depth == "deep"


# ===========================================================================
# Bug 2: Gate Diagnostics Tests
# ===========================================================================


class TestGateDiagnostics:
    """Tests for gate failure diagnostic messages."""

    def test_file_not_found_hint(self, tmp_path, capsys):
        """Gate failure on missing file emits diagnostic hint."""
        gate = _make_gate()
        step = _make_step(
            "generate-haiku-architect",
            tmp_path / "roadmap-haiku-architect.md",
            gate=gate,
        )

        def mock_gate(path, criteria):
            return (False, f"File not found: {path}")

        needs, reason = _step_needs_rerun(step, mock_gate, set(), False, {})
        captured = capsys.readouterr()

        assert needs is True
        assert "output missing" in captured.err
        assert "Hint" in captured.err


# ===========================================================================
# Bug 3: Dependency-Aware Resume Tests
# ===========================================================================


class TestStepNeedsRerun:
    """Tests for _step_needs_rerun helper."""

    def test_force_extract(self, tmp_path):
        """Force extract returns True with reason."""
        step = _make_step("extract", tmp_path / "extraction.md", _make_gate())
        needs, reason = _step_needs_rerun(step, lambda p, c: (True, ""), set(), True, {})
        assert needs is True
        assert "spec file changed" in reason

    def test_dirty_input_dependency(self, tmp_path):
        """Step with dirty input dependency needs rerun."""
        input_file = tmp_path / "extraction.md"
        step = _make_step(
            "generate-a",
            tmp_path / "gen-a.md",
            _make_gate(),
            inputs=[input_file],
        )

        needs, reason = _step_needs_rerun(
            step, lambda p, c: (True, ""), {input_file}, False, {},
        )
        assert needs is True
        assert "dependency" in reason.lower() or "regenerated" in reason.lower()

    def test_gate_passes(self, tmp_path):
        """Step whose gate passes does not need rerun."""
        step = _make_step("extract", tmp_path / "extraction.md", _make_gate())

        needs, reason = _step_needs_rerun(
            step, lambda p, c: (True, ""), set(), False, {},
        )
        assert needs is False
        assert "gate passes" in reason

    def test_state_driven_path_resolution(self, tmp_path):
        """Uses state-recorded path instead of config-derived path for gate check."""
        config_path = tmp_path / "roadmap-haiku-architect.md"  # wrong
        state_path = tmp_path / "roadmap-haiku-analyzer.md"  # correct
        state_path.write_text("valid output\n")

        step = _make_step("generate-haiku", config_path, _make_gate())

        def gate_fn(path, criteria):
            if path.exists():
                return (True, "")
            return (False, f"File not found: {path}")

        needs, reason = _step_needs_rerun(
            step, gate_fn, set(), False,
            {"generate-haiku": state_path},
        )
        assert needs is False

    def test_no_gate_needs_rerun(self, tmp_path):
        """Step without a gate always needs rerun."""
        step = _make_step("step-no-gate", tmp_path / "out.md", gate=None)
        needs, reason = _step_needs_rerun(step, lambda p, c: (True, ""), set(), False, {})
        assert needs is True
        assert "no gate" in reason


class TestApplyResumeDependencyAware:
    """Tests for the dependency-aware _apply_resume."""

    def test_skips_independent_passing_steps(self, tmp_path):
        """Steps after a failure are still skipped if their gates pass
        and they don't depend on regenerated outputs."""
        gate = _make_gate()
        extraction = tmp_path / "extraction.md"
        extraction.write_text("x\n")

        roadmap_a = tmp_path / "roadmap-a.md"
        # roadmap_a does NOT exist - gate will fail

        test_strat = tmp_path / "test-strategy.md"
        test_strat.write_text("x\n")

        steps = [
            _make_step("extract", extraction, gate),
            [_make_step("generate-a", roadmap_a, gate, inputs=[extraction])],
            _make_step(
                "test-strategy", test_strat, gate,
                inputs=[tmp_path / "roadmap.md"],  # depends on merge, NOT generate
            ),
        ]

        config = _make_config(
            tmp_path,
            agents=[AgentSpec("opus", "architect")],
            depth="standard",
        )

        def gate_fn(path, criteria):
            if path.exists() and path.stat().st_size > 0:
                return (True, "")
            return (False, f"File not found: {path}")

        result = _apply_resume(steps, config, gate_fn)
        result_ids = []
        for s in result:
            if isinstance(s, list):
                result_ids.extend(x.id for x in s)
            else:
                result_ids.append(s.id)

        # extract passes (file exists), generate fails (no file), test-strategy passes
        # because its input (roadmap.md) is NOT in dirty set
        assert "extract" not in result_ids
        assert "generate-a" in result_ids
        assert "test-strategy" not in result_ids

    def test_dirty_propagation_through_chain(self, tmp_path):
        """When step 1 re-runs, dependent steps re-run transitively."""
        gate = _make_gate()
        step1_out = tmp_path / "step1.md"
        # step1 doesn't exist - will fail gate
        step2_out = tmp_path / "step2.md"
        step2_out.write_text("valid output\n")
        step3_out = tmp_path / "step3.md"
        step3_out.write_text("valid output\n")

        steps = [
            _make_step("step1", step1_out, gate, inputs=[]),
            _make_step("step2", step2_out, gate, inputs=[step1_out]),
            _make_step("step3", step3_out, gate, inputs=[step2_out]),
        ]

        config = _make_config(
            tmp_path,
            agents=[AgentSpec("opus", "architect")],
            depth="standard",
        )

        def gate_fn(path, criteria):
            if path.exists() and path.stat().st_size > 0:
                return (True, "")
            return (False, f"File not found: {path}")

        result = _apply_resume(steps, config, gate_fn)
        result_ids = [s.id if isinstance(s, Step) else [x.id for x in s] for s in result]
        assert "step1" in str(result_ids)
        assert "step2" in str(result_ids)
        assert "step3" in str(result_ids)

    def test_parallel_group_reruns_if_any_member_fails(self, tmp_path):
        """If any step in a parallel group needs rerun, entire group reruns."""
        gate = _make_gate()
        gen_a = tmp_path / "gen-a.md"
        gen_a.write_text("valid\n")
        gen_b = tmp_path / "gen-b.md"
        # gen_b doesn't exist

        steps = [
            [
                _make_step("generate-a", gen_a, gate),
                _make_step("generate-b", gen_b, gate),
            ],
        ]

        config = _make_config(
            tmp_path,
            agents=[AgentSpec("opus", "architect")],
            depth="standard",
        )

        def gate_fn(path, criteria):
            if path.exists() and path.stat().st_size > 0:
                return (True, "")
            return (False, f"File not found: {path}")

        result = _apply_resume(steps, config, gate_fn)
        assert len(result) == 1
        assert isinstance(result[0], list)

    def test_state_driven_path_in_apply_resume(self, tmp_path):
        """_apply_resume gate-checks state-recorded paths, not config-derived paths."""
        gate = _make_gate()
        state_path = tmp_path / "roadmap-haiku-analyzer.md"
        state_path.write_text("valid output\n")

        config_path = tmp_path / "roadmap-haiku-architect.md"  # wrong path

        spec = tmp_path / "spec.md"
        spec.write_text("# Spec")
        spec_hash = hashlib.sha256(spec.read_bytes()).hexdigest()

        state = {
            "spec_hash": spec_hash,
            "steps": {
                "generate-haiku": {
                    "output_file": str(state_path),
                    "status": "PASS",
                },
            },
        }
        (tmp_path / ".roadmap-state.json").write_text(json.dumps(state))

        steps = [_make_step("generate-haiku", config_path, gate, inputs=[])]

        config = _make_config(
            tmp_path,
            agents=[AgentSpec("haiku", "analyzer")],
            depth="standard",
        )

        def gate_fn(path, criteria):
            if path.exists():
                return (True, "")
            return (False, f"File not found: {path}")

        result = _apply_resume(steps, config, gate_fn)
        # Should pass because state-recorded path exists
        assert len(result) == 0


# ===========================================================================
# Bug 4: _save_state Defense-in-Depth Tests
# ===========================================================================


class TestSaveStateGuards:
    """Tests for _save_state no-progress and agent-mismatch guards."""

    def test_no_progress_no_write(self, tmp_path):
        """_save_state does not write when results list is empty (no steps attempted)."""
        original = {"agents": [{"model": "opus", "persona": "architect"}]}
        state_file = tmp_path / ".roadmap-state.json"
        state_file.write_text(json.dumps(original))
        mtime_before = state_file.stat().st_mtime

        config = _make_config(
            tmp_path, agents=[AgentSpec("opus", "architect")], depth="standard",
        )
        results: list = []  # Empty results — no steps were attempted

        _save_state(config, results)

        # State file should not have been modified
        assert state_file.stat().st_mtime == mtime_before

    def test_preserves_agents_when_no_generate_ran(self, tmp_path):
        """If no generate steps ran, state preserves original agents."""
        original_state = {
            "agents": [
                {"model": "opus", "persona": "architect"},
                {"model": "haiku", "persona": "analyzer"},
            ],
            "schema_version": 1,
        }
        state_file = tmp_path / ".roadmap-state.json"
        state_file.write_text(json.dumps(original_state))

        # Config with different agents (wrong agents loaded by bug)
        config = _make_config(
            tmp_path,
            agents=[AgentSpec("opus", "architect"), AgentSpec("haiku", "architect")],
            depth="standard",
        )

        # Only extract ran (no generate steps)
        step = _make_step("extract", tmp_path / "extraction.md")
        results = [_make_result(step, StepStatus.PASS)]

        _save_state(config, results)

        saved = json.loads(state_file.read_text())
        # Should preserve original "analyzer", not overwrite with "architect"
        assert saved["agents"][1]["persona"] == "analyzer"

    def test_allows_write_when_generate_ran(self, tmp_path):
        """When generate steps ran successfully, agents are updated."""
        original_state = {
            "agents": [
                {"model": "opus", "persona": "architect"},
                {"model": "haiku", "persona": "analyzer"},
            ],
        }
        state_file = tmp_path / ".roadmap-state.json"
        state_file.write_text(json.dumps(original_state))

        new_agents = [AgentSpec("sonnet", "security"), AgentSpec("haiku", "qa")]
        config = _make_config(tmp_path, agents=new_agents, depth="standard")

        gen_step = _make_step("generate-sonnet-security", tmp_path / "gen.md")
        results = [_make_result(gen_step, StepStatus.PASS)]

        _save_state(config, results)

        saved = json.loads(state_file.read_text())
        assert saved["agents"][0]["persona"] == "security"
        assert saved["agents"][1]["persona"] == "qa"

    def test_merges_existing_steps(self, tmp_path):
        """Steps from previous run are preserved when not in current results."""
        existing = {
            "schema_version": 1,
            "agents": [{"model": "opus", "persona": "architect"}],
            "steps": {
                "extract": {"status": "PASS", "output_file": str(tmp_path / "extraction.md")},
                "generate-opus-architect": {"status": "PASS", "output_file": str(tmp_path / "gen.md")},
            },
        }
        state_file = tmp_path / ".roadmap-state.json"
        state_file.write_text(json.dumps(existing))

        config = _make_config(
            tmp_path, agents=[AgentSpec("opus", "architect")], depth="standard",
        )

        # Only diff ran in this resume
        diff_step = _make_step("diff", tmp_path / "diff.md")
        results = [_make_result(diff_step, StepStatus.PASS)]

        _save_state(config, results)

        saved = json.loads(state_file.read_text())
        # Should have all three steps
        assert "extract" in saved["steps"]
        assert "generate-opus-architect" in saved["steps"]
        assert "diff" in saved["steps"]
