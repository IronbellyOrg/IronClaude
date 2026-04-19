"""Roadmap pipeline compression integration.

Covers the contract introduced when ``compress.py`` was wired into the
roadmap pipeline:

- ``--no-compress`` / ``compress_enabled=False`` is a transparent pass-through.
- With compression on, LLM steps consume compressed sidecars; deterministic
  steps keep reading originals.
- Sidecar paths use ``<stem>.compressed.md`` under the output directory.
- Post-step compression produces a sidecar for generate and merge outputs.
- On compression failure, the sidecar still exists (mirrored original bytes)
  so downstream steps remain runnable.
"""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import patch

import pytest

from superclaude.cli.pipeline.models import Step, StepStatus
from superclaude.cli.roadmap.executor import (
    _build_steps,
    _compress_for_llm,
    _compressed_sidecar,
    _llm_inputs_for,
    roadmap_run_step,
)
from superclaude.cli.roadmap.models import AgentSpec, RoadmapConfig


def _flatten(steps):
    out = []
    for s in steps:
        if isinstance(s, list):
            out.extend(s)
        else:
            out.append(s)
    return out


# Minimal merge output that satisfies _validate_merge_completeness.
# Tests that previously used a one-line stub for the merge step now use
# this so the new completeness gate (added with per-milestone OQs) passes.
_MERGE_MIN_COMPLETE = (
    "---\n"
    "schema_version: 1\n"
    "milestones: 1\n"
    "open_questions: 0\n"
    "---\n"
    "\n"
    "## Milestone Summary\n"
    "| ID | Title |\n"
    "|---|---|\n"
    "| M1 | Foundations |\n"
    "\n"
    "## M1: Foundations\n"
    "| # | ID | Title | Description | Comp | Deps | AC | Eff | Pri |\n"
    "|---|---|---|---|---|---|---|---|---|\n"
    "| 1 | DM-001 | Schema | desc | AUTH | - | ac | 2 | H |\n"
    "\n"
    "### Integration Points — M1\n"
    "- none\n"
    "\n"
    "### Milestone Dependencies — M1\n"
    "- none\n"
    "\n"
    "## Risk Register\n"
    "- R-1: mitigate\n"
    "\n"
    "## Success Criteria and Validation Approach\n"
    "- S-1\n"
    "\n"
    "## Decision Summary\n"
    "- d-1\n"
    "\n"
    "## Timeline Estimates\n"
    "- M1: 2w\n"
)


@pytest.fixture
def spec_file(tmp_path: Path) -> Path:
    p = tmp_path / "spec.md"
    p.write_text("# Spec\n\nFR-001 login.\nFR-002 logout.\n")
    return p


@pytest.fixture
def config_on(tmp_path: Path, spec_file: Path) -> RoadmapConfig:
    return RoadmapConfig(
        spec_file=spec_file,
        output_dir=tmp_path / "out",
        work_dir=tmp_path / "out",
        agents=[AgentSpec("opus", "architect"), AgentSpec("haiku", "architect")],
        compress_enabled=True,
    )


@pytest.fixture
def config_off(tmp_path: Path, spec_file: Path) -> RoadmapConfig:
    return RoadmapConfig(
        spec_file=spec_file,
        output_dir=tmp_path / "out",
        work_dir=tmp_path / "out",
        agents=[AgentSpec("opus", "architect"), AgentSpec("haiku", "architect")],
        compress_enabled=False,
    )


class TestSidecarPaths:
    def test_sidecar_is_in_output_dir_with_stem_suffix(self, tmp_path: Path) -> None:
        original = tmp_path / "any-input.md"
        assert _compressed_sidecar(original, tmp_path / "out") == tmp_path / "out" / "any-input.compressed.md"

    def test_sidecar_for_variant_is_adjacent(self, tmp_path: Path) -> None:
        out = tmp_path / "out"
        variant = out / "roadmap-opus-architect.md"
        assert _compressed_sidecar(variant, out) == out / "roadmap-opus-architect.compressed.md"


class TestLlmInputRouting:
    def test_routing_off_is_passthrough(self, config_off: RoadmapConfig) -> None:
        extra = config_off.output_dir / "extraction.md"
        routed = _llm_inputs_for(config_off, config_off.spec_file, extra)
        assert routed == [config_off.spec_file, extra]

    def test_routing_reroutes_spec_and_variants(self, config_on: RoadmapConfig) -> None:
        roadmap_a = config_on.output_dir / "roadmap-opus-architect.md"
        roadmap_b = config_on.output_dir / "roadmap-haiku-architect.md"
        merge = config_on.output_dir / "roadmap.md"
        routed = _llm_inputs_for(config_on, config_on.spec_file, roadmap_a, roadmap_b, merge)
        assert routed == [
            config_on.output_dir / "spec.compressed.md",
            config_on.output_dir / "roadmap-opus-architect.compressed.md",
            config_on.output_dir / "roadmap-haiku-architect.compressed.md",
            config_on.output_dir / "roadmap.compressed.md",
        ]

    def test_routing_leaves_non_rerouteable_paths_alone(self, config_on: RoadmapConfig) -> None:
        extraction = config_on.output_dir / "extraction.md"
        debate = config_on.output_dir / "debate-transcript.md"
        routed = _llm_inputs_for(config_on, extraction, debate)
        assert routed == [extraction, debate]

    def test_routing_filters_none(self, config_on: RoadmapConfig) -> None:
        assert _llm_inputs_for(config_on, config_on.spec_file, None) == [
            config_on.output_dir / "spec.compressed.md"
        ]


class TestBuildStepsWithCompression:
    def test_llm_steps_see_compressed_paths(self, config_on: RoadmapConfig) -> None:
        steps = _flatten(_build_steps(config_on))
        sc_spec = config_on.output_dir / "spec.compressed.md"
        sc_a = config_on.output_dir / "roadmap-opus-architect.compressed.md"
        sc_b = config_on.output_dir / "roadmap-haiku-architect.compressed.md"
        sc_merge = config_on.output_dir / "roadmap.compressed.md"

        by_id = {s.id: s for s in steps}
        assert sc_spec in by_id["extract"].inputs
        assert sc_a in by_id["diff"].inputs and sc_b in by_id["diff"].inputs
        assert sc_a in by_id["debate"].inputs and sc_b in by_id["debate"].inputs
        assert sc_a in by_id["score"].inputs and sc_b in by_id["score"].inputs
        assert sc_a in by_id["merge"].inputs and sc_b in by_id["merge"].inputs
        assert sc_merge in by_id["spec-fidelity"].inputs
        assert sc_merge in by_id["test-strategy"].inputs
        assert sc_merge in by_id["wiring-verification"].inputs

    def test_deterministic_steps_keep_originals(self, config_on: RoadmapConfig) -> None:
        steps = _flatten(_build_steps(config_on))
        by_id = {s.id: s for s in steps}
        merge = config_on.output_dir / "roadmap.md"
        assert config_on.spec_file in by_id["anti-instinct"].inputs
        assert merge in by_id["anti-instinct"].inputs
        assert merge in by_id["deviation-analysis"].inputs
        assert merge in by_id["remediate"].inputs


class TestPostStepCompression:
    """Exercises the block at the end of roadmap_run_step that writes sidecars
    for ``generate-*`` and ``merge`` outputs."""

    def _fake_passing_process(self, output_text: str):
        """Patch ClaudeProcess so no real subprocess runs; write output_text to
        the step's output_file and report exit code 0."""

        class _FakeProc:
            def __init__(self, *, prompt, output_file, error_file, **_kw):
                self.output_file = output_file
                self._process = None  # bypass the cancel-poll loop

            def start(self):
                Path(self.output_file).parent.mkdir(parents=True, exist_ok=True)
                Path(self.output_file).write_text(output_text)

            def wait(self):
                return 0

            def validate_tool_write_output(self):
                return True

            def terminate(self):
                pass

        return _FakeProc

    def _ensure_inputs(self, step: Step) -> None:
        """Pre-create any upstream inputs the step depends on.

        ``roadmap_run_step`` calls ``_embed_inputs`` which reads every path in
        ``step.inputs``. These tests drive individual steps in isolation, so
        upstream artifacts (e.g. ``extraction.md``, ``base-selection.md``,
        compressed sidecars) do not yet exist -- synthesize placeholders.
        """
        for p in step.inputs:
            if p is None:
                continue
            path = Path(p)
            if path.exists():
                continue
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(f"# stub {path.name}\n")

    def _run_step(self, step: Step, config: RoadmapConfig, output_text: str) -> None:
        self._ensure_inputs(step)
        fake = self._fake_passing_process(output_text)
        with patch("superclaude.cli.roadmap.executor.ClaudeProcess", fake):
            result = roadmap_run_step(step, config, cancel_check=lambda: False)
        assert result.status == StepStatus.PASS

    def test_generate_step_produces_sidecar(self, config_on: RoadmapConfig) -> None:
        steps = _flatten(_build_steps(config_on))
        gen_a = next(s for s in steps if s.id == "generate-opus-architect")
        self._run_step(gen_a, config_on, "# Roadmap A\n\nM1 | 2w | foo\n")
        assert (config_on.output_dir / "roadmap-opus-architect.compressed.md").exists()

    def test_merge_step_produces_sidecar(self, config_on: RoadmapConfig) -> None:
        steps = _flatten(_build_steps(config_on))
        merge = next(s for s in steps if s.id == "merge")
        self._run_step(merge, config_on, _MERGE_MIN_COMPLETE)
        assert (config_on.output_dir / "roadmap.compressed.md").exists()

    def test_no_sidecar_when_compression_disabled(self, config_off: RoadmapConfig) -> None:
        steps = _flatten(_build_steps(config_off))
        gen_a = next(s for s in steps if s.id == "generate-opus-architect")
        self._run_step(gen_a, config_off, "# Roadmap A\n\n")
        assert not (config_off.output_dir / "roadmap-opus-architect.compressed.md").exists()

    def test_compression_failure_mirrors_original_to_sidecar(
        self, config_on: RoadmapConfig
    ) -> None:
        steps = _flatten(_build_steps(config_on))
        merge = next(s for s in steps if s.id == "merge")
        self._ensure_inputs(merge)

        fake = self._fake_passing_process(_MERGE_MIN_COMPLETE)
        with patch("superclaude.cli.roadmap.executor.ClaudeProcess", fake), patch(
            "superclaude.cli.roadmap.executor._compress_for_llm",
            side_effect=RuntimeError("boom"),
        ):
            result = roadmap_run_step(merge, config_on, cancel_check=lambda: False)

        assert result.status == StepStatus.PASS
        sidecar = config_on.output_dir / "roadmap.compressed.md"
        assert sidecar.exists()
        assert sidecar.read_text() == merge.output_file.read_text()


class TestCompressForLlmHelper:
    def test_compress_for_llm_writes_sidecar(self, tmp_path: Path, spec_file: Path) -> None:
        out = tmp_path / "out"
        out.mkdir()
        sidecar = _compress_for_llm(spec_file, "spec", out)
        assert sidecar == out / "spec.compressed.md"
        assert sidecar.exists()
        assert sidecar.read_text().strip().startswith("# Spec")
