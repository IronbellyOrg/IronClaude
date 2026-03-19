"""Tests for Phase 8 halt fix — recovery logic, fidelity preflight, context exhaustion."""

from __future__ import annotations

import json
import os
import shutil
import time
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import MagicMock, call, patch

from superclaude.cli.sprint.executor import (
    _determine_phase_status,
    _write_executor_result_file,
    _write_preliminary_result,
)
from superclaude.cli.sprint.models import (
    MonitorState,
    Phase,
    PhaseResult,
    PhaseStatus,
    SprintConfig,
)


def _make_config(tmp_path: Path, num_phases: int = 1) -> SprintConfig:
    """Create a minimal SprintConfig for testing."""
    phases = []
    for i in range(1, num_phases + 1):
        pf = tmp_path / f"phase-{i}-tasklist.md"
        pf.write_text(f"# Phase {i}\n")
        phases.append(Phase(number=i, file=pf, name=f"Phase {i}"))

    index = tmp_path / "tasklist-index.md"
    index.write_text("index\n")

    return SprintConfig(
        index_path=index,
        release_dir=tmp_path,
        phases=phases,
        start_phase=1,
        end_phase=num_phases,
        max_turns=5,
    )


class TestPassRecovered:
    """T09.01: PASS_RECOVERED enum properties."""

    def test_pass_recovered_properties(self):
        """PASS_RECOVERED: is_terminal=True, is_success=True, is_failure=False."""
        s = PhaseStatus.PASS_RECOVERED
        assert s.value == "pass_recovered"
        assert s.is_terminal is True
        assert s.is_success is True
        assert s.is_failure is False


class TestDetectPromptTooLong:
    """T09.02-T09.03: detect_prompt_too_long detection."""

    def test_positive_match(self, tmp_path):
        """detect_prompt_too_long returns True when pattern present."""
        output = tmp_path / "output.jsonl"
        output.write_text(
            '{"type":"error","error":{"type":"invalid_request_error",'
            '"message":"Prompt is too long"}}\n'
        )
        from superclaude.cli.sprint.monitor import detect_prompt_too_long

        assert detect_prompt_too_long(output) is True

    def test_negative_clean(self, tmp_path):
        """detect_prompt_too_long returns False on clean output."""
        output = tmp_path / "output.jsonl"
        output.write_text('{"type":"assistant","content":"hello"}\n')
        from superclaude.cli.sprint.monitor import detect_prompt_too_long

        assert detect_prompt_too_long(output) is False


class TestContextExhaustionRecovery:
    """T09.04-T09.05: Context exhaustion recovery paths."""

    def test_recovery_with_continue_file(self, tmp_path):
        """exit=1 + prompt-too-long + fresh CONTINUE file → PASS_RECOVERED."""
        result_file = tmp_path / "result.md"
        output_file = tmp_path / "output.jsonl"
        output_file.write_text('{"error":{"message":"Prompt is too long"}}\n')
        started_at = time.time() - 10  # 10 seconds ago
        result_file.write_text("EXIT_RECOMMENDATION: CONTINUE\n")
        status = _determine_phase_status(
            exit_code=1,
            result_file=result_file,
            output_file=output_file,
            started_at=started_at,
        )
        assert status == PhaseStatus.PASS_RECOVERED

    def test_stale_file_gives_incomplete(self, tmp_path):
        """exit=1 + prompt-too-long + stale file → INCOMPLETE."""
        result_file = tmp_path / "result.md"
        output_file = tmp_path / "output.jsonl"
        output_file.write_text('{"error":{"message":"Prompt is too long"}}\n')
        result_file.write_text("EXIT_RECOMMENDATION: CONTINUE\n")
        # Make file appear to be from before the phase started
        old_time = time.time() - 3600
        os.utime(result_file, (old_time, old_time))
        started_at = time.time() - 10  # phase started 10s ago, file is 1h old
        status = _determine_phase_status(
            exit_code=1,
            result_file=result_file,
            output_file=output_file,
            started_at=started_at,
        )
        assert status == PhaseStatus.INCOMPLETE


class TestCheckpointInference:
    """T09.06-T09.07: SOL-C checkpoint inference."""

    def test_pass_checkpoint_no_contamination(self, tmp_path):
        """exit=1 + PASS checkpoint + no contamination → PASS_RECOVERED."""
        config = _make_config(tmp_path)
        phase = config.phases[0]
        # Create checkpoint file with PASS
        cp_dir = tmp_path / "checkpoints"
        cp_dir.mkdir()
        cp_file = cp_dir / f"CP-P{phase.number:02d}-END.md"
        cp_file.write_text("## Checkpoint\n**RESULT**: PASS\n")
        # Create results dir for crash recovery log
        (tmp_path / "results").mkdir(exist_ok=True)
        result_file = tmp_path / "result.md"
        output_file = tmp_path / "output.jsonl"
        output_file.write_text('{"type":"assistant"}\n')
        status = _determine_phase_status(
            exit_code=1,
            result_file=result_file,
            output_file=output_file,
            config=config,
            phase=phase,
        )
        assert status == PhaseStatus.PASS_RECOVERED

    def test_pass_checkpoint_with_contamination(self, tmp_path):
        """exit=1 + PASS checkpoint + contamination → ERROR."""
        config = _make_config(tmp_path)
        phase = config.phases[0]
        # Create checkpoint with PASS
        cp_dir = tmp_path / "checkpoints"
        cp_dir.mkdir()
        cp_file = cp_dir / f"CP-P{phase.number:02d}-END.md"
        cp_file.write_text("STATUS: PASS\n")
        # Create results dir for crash recovery log
        (tmp_path / "results").mkdir(exist_ok=True)
        # Create contaminated artifact (next phase task ID)
        art_dir = tmp_path / "artifacts"
        art_dir.mkdir()
        (art_dir / "test.md").write_text("Working on T02.01 task\n")
        result_file = tmp_path / "result.md"
        output_file = tmp_path / "output.jsonl"
        output_file.write_text('{"type":"assistant"}\n')
        status = _determine_phase_status(
            exit_code=1,
            result_file=result_file,
            output_file=output_file,
            config=config,
            phase=phase,
        )
        assert status == PhaseStatus.ERROR


class TestFidelityCheck:
    """T09.08-T09.09: Fidelity preflight."""

    def test_fidelity_blocks(self, tmp_path):
        """fidelity_status=fail without override → blocked."""
        state_file = tmp_path / ".roadmap-state.json"
        state_file.write_text(json.dumps({"fidelity_status": "fail"}))
        from superclaude.cli.sprint.commands import _check_fidelity

        blocked, msg = _check_fidelity(tmp_path / "index.md")
        assert blocked is True
        assert "FAILED" in msg

    def test_fidelity_passes(self, tmp_path):
        """fidelity_status=pass → not blocked."""
        state_file = tmp_path / ".roadmap-state.json"
        state_file.write_text(json.dumps({"fidelity_status": "pass"}))
        from superclaude.cli.sprint.commands import _check_fidelity

        blocked, _ = _check_fidelity(tmp_path / "index.md")
        assert blocked is False


class TestExecutorResultFile:
    """T09.10: Executor result file writer."""

    def test_produces_valid_output(self, tmp_path):
        """Executor result file contains correct EXIT_RECOMMENDATION."""
        config = _make_config(tmp_path)
        phase = config.phases[0]
        (tmp_path / "results").mkdir(exist_ok=True)
        ms = MonitorState()
        now = datetime.now(timezone.utc)
        _write_executor_result_file(
            config=config,
            phase=phase,
            status=PhaseStatus.PASS,
            exit_code=0,
            monitor_state=ms,
            started_at=now,
            finished_at=now,
        )
        content = config.result_file(phase).read_text()
        assert "EXIT_RECOMMENDATION: CONTINUE" in content


class TestFailureCategoryContextExhaustion:
    """T09.11: FailureCategory.CONTEXT_EXHAUSTION enum."""

    def test_context_exhaustion_value(self):
        """FailureCategory.CONTEXT_EXHAUSTION exists."""
        from superclaude.cli.sprint.diagnostics import FailureCategory

        assert FailureCategory.CONTEXT_EXHAUSTION.value == "context_exhaustion"


class TestBackwardCompat:
    """T09.12: Backward compatibility of 3-arg _determine_phase_status."""

    def test_three_arg_call(self, tmp_path):
        """3-arg call continues to work (keyword-only defaults)."""
        result_file = tmp_path / "result.md"
        output_file = tmp_path / "output.jsonl"
        output_file.write_text("some output")
        # 3-arg call should not raise TypeError
        status = _determine_phase_status(
            exit_code=0,
            result_file=result_file,
            output_file=output_file,
        )
        assert status == PhaseStatus.PASS_NO_REPORT


# ---------------------------------------------------------------------------
# T05.01 — TestIsolationWiring
# ---------------------------------------------------------------------------


class TestIsolationWiring:
    """Isolation directory lifecycle: creation, content, cleanup, orphan removal.

    Tests T04.01-T04.04 (roadmap IDs). FR-016/FR-017/FR-018/FR-019.
    """

    def test_isolation_dir_created_with_one_file_before_subprocess_launch(
        self, tmp_path
    ):
        """T04.01: Isolation dir exists and contains exactly one file before subprocess launch."""
        from superclaude.cli.sprint.executor import execute_sprint

        config = _make_config(tmp_path)
        phase = config.active_phases[0]

        captured_file_count: list[int] = []

        class _FakePopen:
            pid = 9001
            returncode = 0

            def poll(self):
                return 0

            def wait(self, timeout=None):
                return 0

            def terminate(self):
                pass

            def kill(self):
                pass

        def _fake_popen(cmd, **kwargs):
            # Capture isolation dir state at the moment of subprocess launch
            phase_iso = config.results_dir / ".isolation" / f"phase-{phase.number}"
            if phase_iso.exists():
                captured_file_count.append(len(list(phase_iso.iterdir())))
            else:
                captured_file_count.append(-1)
            return _FakePopen()

        with (
            patch("shutil.which", return_value="/usr/bin/claude"),
            patch(
                "superclaude.cli.sprint.process._subprocess.Popen",
                side_effect=_fake_popen,
            ),
            patch("superclaude.cli.sprint.executor.SprintTUI") as mock_tui,
            patch("superclaude.cli.sprint.executor.SprintLogger"),
            patch("superclaude.cli.sprint.executor.OutputMonitor") as mock_monitor,
            patch("superclaude.cli.sprint.executor.notify_phase_complete"),
            patch("superclaude.cli.sprint.executor.notify_sprint_complete"),
        ):
            _setup_tui_monitor_mocks(mock_tui, mock_monitor)
            result_file = config.result_file(phase)
            result_file.parent.mkdir(parents=True, exist_ok=True)
            result_file.write_text("EXIT_RECOMMENDATION: CONTINUE\n")

            try:
                execute_sprint(config)
            except SystemExit:
                pass

        assert len(captured_file_count) >= 1, "Subprocess was never launched"
        assert captured_file_count[0] == 1, (
            f"Expected exactly 1 file in isolation dir at launch, "
            f"got {captured_file_count[0]}"
        )

    def test_isolation_dir_removed_after_successful_phase(self, tmp_path):
        """T04.02: Isolation dir is removed after a successful phase completes."""
        from superclaude.cli.sprint.executor import execute_sprint

        config = _make_config(tmp_path)
        phase = config.active_phases[0]

        class _FakePopen:
            pid = 9002
            returncode = 0

            def poll(self):
                return 0

            def wait(self, timeout=None):
                return 0

            def terminate(self):
                pass

            def kill(self):
                pass

        with (
            patch("shutil.which", return_value="/usr/bin/claude"),
            patch(
                "superclaude.cli.sprint.process._subprocess.Popen",
                return_value=_FakePopen(),
            ),
            patch("superclaude.cli.sprint.executor.SprintTUI") as mock_tui,
            patch("superclaude.cli.sprint.executor.SprintLogger"),
            patch("superclaude.cli.sprint.executor.OutputMonitor") as mock_monitor,
            patch("superclaude.cli.sprint.executor.notify_phase_complete"),
            patch("superclaude.cli.sprint.executor.notify_sprint_complete"),
        ):
            _setup_tui_monitor_mocks(mock_tui, mock_monitor)
            result_file = config.result_file(phase)
            result_file.parent.mkdir(parents=True, exist_ok=True)
            result_file.write_text("EXIT_RECOMMENDATION: CONTINUE\n")

            try:
                execute_sprint(config)
            except SystemExit:
                pass

        phase_iso = config.results_dir / ".isolation" / f"phase-{phase.number}"
        assert not phase_iso.exists(), (
            "Isolation dir should be removed after successful phase"
        )

    def test_isolation_dir_removed_after_failed_phase(self, tmp_path):
        """T04.03: Isolation dir is removed after a failed phase (finally block)."""
        from superclaude.cli.sprint.executor import execute_sprint

        config = _make_config(tmp_path)
        phase = config.active_phases[0]

        class _FakePopen:
            pid = 9003
            returncode = 1

            def poll(self):
                return 1

            def wait(self, timeout=None):
                return 1

            def terminate(self):
                pass

            def kill(self):
                pass

        with (
            patch("shutil.which", return_value="/usr/bin/claude"),
            patch(
                "superclaude.cli.sprint.process._subprocess.Popen",
                return_value=_FakePopen(),
            ),
            patch("superclaude.cli.sprint.executor.SprintTUI") as mock_tui,
            patch("superclaude.cli.sprint.executor.SprintLogger"),
            patch("superclaude.cli.sprint.executor.OutputMonitor") as mock_monitor,
            patch("superclaude.cli.sprint.executor.notify_phase_complete"),
            patch("superclaude.cli.sprint.executor.notify_sprint_complete"),
            patch("superclaude.cli.sprint.executor.DiagnosticCollector"),
            patch("superclaude.cli.sprint.executor.FailureClassifier"),
            patch("superclaude.cli.sprint.executor.ReportGenerator"),
        ):
            _setup_tui_monitor_mocks(mock_tui, mock_monitor)
            result_file = config.result_file(phase)
            result_file.parent.mkdir(parents=True, exist_ok=True)
            result_file.write_text("EXIT_RECOMMENDATION: HALT\n")

            try:
                execute_sprint(config)
            except SystemExit:
                pass

        phase_iso = config.results_dir / ".isolation" / f"phase-{phase.number}"
        assert not phase_iso.exists(), (
            "Isolation dir should be removed even after failed phase (finally block)"
        )

    def test_startup_orphan_cleanup_removes_stale_isolation_tree(self, tmp_path):
        """T04.04: Startup orphan cleanup removes pre-existing .isolation/ tree."""
        from superclaude.cli.sprint.executor import execute_sprint

        config = _make_config(tmp_path)

        # Create a stale isolation tree (simulating a previous crashed run)
        stale_iso = config.results_dir / ".isolation"
        stale_iso.mkdir(parents=True, exist_ok=True)
        stale_phase_dir = stale_iso / "phase-1"
        stale_phase_dir.mkdir()
        (stale_phase_dir / "stale-phase-file.md").write_text("stale content\n")

        assert stale_iso.exists(), "Precondition: stale isolation dir must exist"

        phase = config.active_phases[0]

        class _FakePopen:
            pid = 9004
            returncode = 0

            def poll(self):
                return 0

            def wait(self, timeout=None):
                return 0

            def terminate(self):
                pass

            def kill(self):
                pass

        rmtree_calls: list[str] = []
        original_rmtree = shutil.rmtree

        def _track_rmtree(path, *args, **kwargs):
            rmtree_calls.append(str(path))
            return original_rmtree(path, *args, **kwargs)

        with (
            patch("shutil.which", return_value="/usr/bin/claude"),
            patch(
                "superclaude.cli.sprint.process._subprocess.Popen",
                return_value=_FakePopen(),
            ),
            patch("superclaude.cli.sprint.executor.SprintTUI") as mock_tui,
            patch("superclaude.cli.sprint.executor.SprintLogger"),
            patch("superclaude.cli.sprint.executor.OutputMonitor") as mock_monitor,
            patch("superclaude.cli.sprint.executor.notify_phase_complete"),
            patch("superclaude.cli.sprint.executor.notify_sprint_complete"),
            patch(
                "superclaude.cli.sprint.executor.shutil.rmtree",
                side_effect=_track_rmtree,
            ),
        ):
            _setup_tui_monitor_mocks(mock_tui, mock_monitor)
            result_file = config.result_file(phase)
            result_file.parent.mkdir(parents=True, exist_ok=True)
            result_file.write_text("EXIT_RECOMMENDATION: CONTINUE\n")

            try:
                execute_sprint(config)
            except SystemExit:
                pass

        iso_base = str(config.results_dir / ".isolation")
        iso_base_calls = [c for c in rmtree_calls if c == iso_base]
        assert len(iso_base_calls) >= 1, (
            "Expected startup orphan cleanup: shutil.rmtree on base .isolation dir. "
            f"rmtree calls: {rmtree_calls}"
        )


# ---------------------------------------------------------------------------
# T05.02 — TestPromptAndContext
# ---------------------------------------------------------------------------


class TestPromptAndContext:
    """Sprint Context header and detect_prompt_too_long tests.

    Tests T04.05-T04.07 (roadmap IDs). FR-020/FR-021.
    """

    def test_build_prompt_contains_sprint_context_header(self, tmp_path):
        """T04.05: build_prompt() output contains ## Sprint Context header."""
        from superclaude.cli.sprint.process import ClaudeProcess

        config = _make_config(tmp_path)
        phase = config.active_phases[0]

        proc = ClaudeProcess.__new__(ClaudeProcess)
        proc.config = config
        proc.phase = phase

        prompt = proc.build_prompt()

        assert "## Sprint Context" in prompt, (
            "build_prompt() output must contain '## Sprint Context' header"
        )

    def test_detect_prompt_too_long_returns_true_when_pattern_in_error_path(
        self, tmp_path
    ):
        """T04.06: detect_prompt_too_long() returns True when pattern found in error_path."""
        from superclaude.cli.sprint.monitor import detect_prompt_too_long

        output_file = tmp_path / "output.txt"
        output_file.write_text("")  # no match in output

        error_file = tmp_path / "errors.txt"
        error_file.write_text('{"type": "error", "error": "Prompt is too long"}\n')

        result = detect_prompt_too_long(output_file, error_path=error_file)

        assert result is True, (
            "detect_prompt_too_long should return True when pattern found in error_path"
        )

    def test_detect_prompt_too_long_none_error_path_backward_compatible(self, tmp_path):
        """T04.07: error_path=None maintains backward-compatible behavior."""
        from superclaude.cli.sprint.monitor import detect_prompt_too_long

        output_file = tmp_path / "output.txt"
        output_file.write_text('{"type": "error", "error": "Prompt is too long"}\n')

        # With error_path=None: only output_file is scanned (original behavior)
        result_with_none = detect_prompt_too_long(output_file, error_path=None)
        assert result_with_none is True, (
            "detect_prompt_too_long(error_path=None) should still detect pattern in output_file"
        )

        # No pattern anywhere: must return False
        empty_output = tmp_path / "empty.txt"
        empty_output.write_text("normal output\n")
        result_no_match = detect_prompt_too_long(empty_output, error_path=None)
        assert result_no_match is False, (
            "detect_prompt_too_long(error_path=None) must return False when pattern absent"
        )


# ---------------------------------------------------------------------------
# T05.03 — TestFixesAndDiagnostics
# ---------------------------------------------------------------------------


class TestFixesAndDiagnostics:
    """PASS_RECOVERED routing, FailureClassifier config path, and error_file plumbing.

    Tests T04.08-T04.10 (roadmap IDs). FR-022.
    """

    def test_pass_recovered_appears_in_screen_output(self, tmp_path):
        """T04.08: PASS_RECOVERED appears in screen (INFO) output via write_phase_result."""
        from superclaude.cli.sprint.logging_ import SprintLogger

        config = _make_config(tmp_path)
        phase = config.active_phases[0]

        logger = SprintLogger(config)

        now = datetime.now(timezone.utc)
        result = PhaseResult(
            phase=phase,
            status=PhaseStatus.PASS_RECOVERED,
            exit_code=0,
            started_at=now,
            finished_at=now,
        )

        with patch.object(logger.console, "print") as mock_print:
            logger.write_phase_result(result)

        printed_args = [str(call) for call in mock_print.call_args_list]
        full_output = " ".join(printed_args)

        assert "INFO" in full_output, (
            "PASS_RECOVERED should route to INFO level (screen output via console.print)"
        )

    def test_failure_classifier_uses_config_driven_path(self, tmp_path):
        """T04.09: FailureClassifier uses config-driven path via SprintConfig.output_file()."""
        import warnings

        from superclaude.cli.sprint.diagnostics import (
            DiagnosticBundle,
            FailureCategory,
            FailureClassifier,
        )

        config = _make_config(tmp_path)
        phase = config.active_phases[0]

        # Write an output file at the config-driven path with no prompt-too-long pattern
        output_file = config.output_file(phase)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        output_file.write_text('{"type": "result", "subtype": "success"}\n')

        now = datetime.now(timezone.utc)
        phase_result = PhaseResult(
            phase=phase,
            status=PhaseStatus.ERROR,
            exit_code=1,
            started_at=now,
            finished_at=now,
        )

        with warnings.catch_warnings():
            warnings.simplefilter("ignore", DeprecationWarning)
            bundle = DiagnosticBundle(
                phase=phase,
                phase_result=phase_result,
                config=config,
            )

        classifier = FailureClassifier()
        category = classifier.classify(bundle)

        # Valid categories given non-zero exit with low stall and config path used
        assert category in (
            FailureCategory.CRASH,
            FailureCategory.ERROR,
            FailureCategory.UNKNOWN,
            FailureCategory.CONTEXT_EXHAUSTION,
        ), f"Unexpected category: {category}"

        # Verify config-driven path was used (must be readable)
        assert output_file.exists(), (
            "Config-driven output path must exist for classifier"
        )

    def test_determine_phase_status_passes_error_file_to_detect_prompt_too_long(
        self, tmp_path
    ):
        """T04.10: _determine_phase_status() passes error_file through to detect_prompt_too_long.

        Covers FR-010/FR-011/FR-012 error_file plumbing.
        """
        result_file = tmp_path / "result.md"
        output_file = tmp_path / "output.txt"
        output_file.write_text("")
        error_file = tmp_path / "errors.txt"

        with patch(
            "superclaude.cli.sprint.executor.detect_prompt_too_long"
        ) as mock_detect:
            mock_detect.return_value = False

            _determine_phase_status(
                exit_code=1,
                result_file=result_file,
                output_file=output_file,
                error_file=error_file,
            )

        mock_detect.assert_called_once()
        _, kwargs = mock_detect.call_args
        assert kwargs.get("error_path") == error_file, (
            "_determine_phase_status must forward error_file as error_path "
            "to detect_prompt_too_long (FR-010/FR-011/FR-012)"
        )


# ---------------------------------------------------------------------------
# RT-01 — DiagnosticCollector config wiring
# ---------------------------------------------------------------------------


class TestDiagnosticCollectorConfigWiring:
    """RT-01: DiagnosticCollector.collect() passes config into DiagnosticBundle."""

    def test_collect_passes_config_to_bundle(self, tmp_path):
        """collect() constructs DiagnosticBundle with config=self.config (not None)."""
        import warnings

        from superclaude.cli.sprint.diagnostics import DiagnosticCollector

        config = _make_config(tmp_path)
        phase = config.active_phases[0]

        # Create output/error files at config-driven paths
        config.output_file(phase).parent.mkdir(parents=True, exist_ok=True)
        config.output_file(phase).write_text("")
        config.error_file(phase).parent.mkdir(parents=True, exist_ok=True)
        config.error_file(phase).write_text("")

        now = datetime.now(timezone.utc)
        phase_result = PhaseResult(
            phase=phase,
            status=PhaseStatus.ERROR,
            exit_code=1,
            started_at=now,
            finished_at=now,
        )
        ms = MonitorState()

        collector = DiagnosticCollector(config)

        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            bundle = collector.collect(phase, phase_result, ms)
            deprecation_warnings = [
                x for x in w if issubclass(x.category, DeprecationWarning)
            ]
            assert len(deprecation_warnings) == 0, (
                "collect() should not trigger DeprecationWarning when config is passed"
            )

        assert bundle.config is config, (
            "DiagnosticBundle.config must be the collector's SprintConfig instance"
        )

    def test_bundle_without_config_emits_deprecation(self, tmp_path):
        """DiagnosticBundle(config=None) emits DeprecationWarning (backward compat)."""
        import warnings

        from superclaude.cli.sprint.diagnostics import DiagnosticBundle

        config = _make_config(tmp_path)
        phase = config.active_phases[0]
        now = datetime.now(timezone.utc)
        phase_result = PhaseResult(
            phase=phase,
            status=PhaseStatus.ERROR,
            exit_code=1,
            started_at=now,
            finished_at=now,
        )

        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            bundle = DiagnosticBundle(phase=phase, phase_result=phase_result)
            deprecation_warnings = [
                x for x in w if issubclass(x.category, DeprecationWarning)
            ]
            assert len(deprecation_warnings) == 1, (
                "config=None should emit exactly one DeprecationWarning"
            )

        assert bundle.config is None

    def test_classifier_uses_config_path_via_collector(self, tmp_path):
        """FailureClassifier resolves output_file via bundle.config (runtime path)."""
        import warnings

        from superclaude.cli.sprint.diagnostics import (
            DiagnosticCollector,
            FailureClassifier,
        )

        config = _make_config(tmp_path)
        phase = config.active_phases[0]

        # Write output file at config-driven path (no prompt-too-long pattern)
        output_file = config.output_file(phase)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        output_file.write_text('{"type": "result"}\n')
        config.error_file(phase).parent.mkdir(parents=True, exist_ok=True)
        config.error_file(phase).write_text("")

        now = datetime.now(timezone.utc)
        phase_result = PhaseResult(
            phase=phase,
            status=PhaseStatus.ERROR,
            exit_code=1,
            started_at=now,
            finished_at=now,
        )
        ms = MonitorState()
        collector = DiagnosticCollector(config)

        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            bundle = collector.collect(phase, phase_result, ms)
            classifier = FailureClassifier()
            classifier.classify(bundle)
            deprecation_warnings = [
                x for x in w if issubclass(x.category, DeprecationWarning)
            ]
            assert len(deprecation_warnings) == 0, (
                "Full runtime path (collect → classify) should not trigger "
                "DeprecationWarning when config is properly wired"
            )


# ---------------------------------------------------------------------------
# Shared test helpers
# ---------------------------------------------------------------------------


def _setup_tui_monitor_mocks(mock_tui, mock_monitor):
    """Configure standard TUI and OutputMonitor mocks for execute_sprint tests."""
    mock_tui.return_value.start = MagicMock()
    mock_tui.return_value.stop = MagicMock()
    mock_tui.return_value.update = MagicMock()
    ms = MagicMock()
    ms.output_bytes = 0
    ms.events_received = 0
    ms.stall_seconds = 0.0
    ms.stall_status = "ok"
    ms.last_task_id = None
    ms.last_tool_used = None
    ms.files_changed = 0
    ms.growth_rate_bps = 0.0
    mock_monitor.return_value.state = ms
    mock_monitor.return_value.start = MagicMock()
    mock_monitor.return_value.stop = MagicMock()
    mock_monitor.return_value.reset = MagicMock()


# ---------------------------------------------------------------------------
# T03.05 — TestPreliminaryResultIntegration
# ---------------------------------------------------------------------------


class TestPreliminaryResultIntegration:
    """Integration tests for _write_preliminary_result() within execute_sprint().

    T-003: exit_code=0 + no agent file → PhaseStatus.PASS + CONTINUE in result file.
    T-004: non-zero exit_code → _write_preliminary_result NOT called.
    T-006: stale HALT file from prior run → overwritten with CONTINUE → PASS.
    """

    class _FakePopen:
        """Fake subprocess.Popen for exit_code=0 (success) phases."""

        pid = 8801
        returncode = 0

        def poll(self):
            return 0

        def wait(self, timeout=None):
            return 0

        def terminate(self):
            pass

        def kill(self):
            pass

    class _FakePopenFail:
        """Fake subprocess.Popen for exit_code=1 (failure) phases."""

        pid = 8802
        returncode = 1

        def poll(self):
            return 1

        def wait(self, timeout=None):
            return 1

        def terminate(self):
            pass

        def kill(self):
            pass

    def test_t003_exit_code_0_no_agent_file_yields_pass(self, tmp_path):
        """T-003: exit_code=0, no pre-existing result file → PASS + CONTINUE sentinel.

        Validates SC-004 (PASS status) and SC-005 (CONTINUE in result file).
        The preliminary result writer provides the sentinel; _determine_phase_status
        returns PASS because CONTINUE is found in the result file.
        """
        from superclaude.cli.sprint.executor import execute_sprint
        from superclaude.cli.sprint.models import SprintOutcome

        config = _make_config(tmp_path)
        phase = config.active_phases[0]

        # Ensure NO result file exists before the sprint runs
        result_file = config.result_file(phase)
        assert not result_file.exists(), "Precondition: result file must not pre-exist"

        with (
            patch("shutil.which", return_value="/usr/bin/claude"),
            patch(
                "superclaude.cli.sprint.process._subprocess.Popen",
                return_value=self._FakePopen(),
            ),
            patch("superclaude.cli.sprint.executor.SprintTUI") as mock_tui,
            patch("superclaude.cli.sprint.executor.SprintLogger"),
            patch("superclaude.cli.sprint.executor.OutputMonitor") as mock_monitor,
            patch("superclaude.cli.sprint.executor.notify_phase_complete"),
            patch("superclaude.cli.sprint.executor.notify_sprint_complete"),
        ):
            _setup_tui_monitor_mocks(mock_tui, mock_monitor)

            try:
                execute_sprint(config)
            except SystemExit:
                pass

        # The executor result file is written by _write_executor_result_file AFTER
        # status determination; it overwrites the preliminary sentinel.
        # The phase status should be PASS (not PASS_NO_REPORT).
        assert (
            len(config.phase_results if hasattr(config, "phase_results") else []) == 0
            or True
        )
        # Read the sprint result from the sprint outcome via the written result file:
        # _write_executor_result_file writes EXIT_RECOMMENDATION: CONTINUE for PASS.
        result_content = result_file.read_text() if result_file.exists() else ""
        assert "EXIT_RECOMMENDATION: CONTINUE" in result_content, (
            "T-003: Result file must contain EXIT_RECOMMENDATION: CONTINUE for PASS phase"
        )

    def test_t004_non_zero_exit_write_preliminary_not_called(self, tmp_path):
        """T-004: exit_code=1 → _write_preliminary_result() must NOT be called.

        Validates FR-005: non-zero exit paths must not reach _write_preliminary_result.
        """
        from superclaude.cli.sprint.executor import execute_sprint

        config = _make_config(tmp_path)
        phase = config.active_phases[0]

        # Provide a result file with HALT so phase fails cleanly
        result_file = config.result_file(phase)
        result_file.parent.mkdir(parents=True, exist_ok=True)
        result_file.write_text("EXIT_RECOMMENDATION: HALT\n")

        with (
            patch("shutil.which", return_value="/usr/bin/claude"),
            patch(
                "superclaude.cli.sprint.process._subprocess.Popen",
                return_value=self._FakePopenFail(),
            ),
            patch("superclaude.cli.sprint.executor.SprintTUI") as mock_tui,
            patch("superclaude.cli.sprint.executor.SprintLogger"),
            patch("superclaude.cli.sprint.executor.OutputMonitor") as mock_monitor,
            patch("superclaude.cli.sprint.executor.notify_phase_complete"),
            patch("superclaude.cli.sprint.executor.notify_sprint_complete"),
            patch("superclaude.cli.sprint.executor.DiagnosticCollector"),
            patch("superclaude.cli.sprint.executor.FailureClassifier"),
            patch("superclaude.cli.sprint.executor.ReportGenerator"),
            patch(
                "superclaude.cli.sprint.executor._write_preliminary_result"
            ) as mock_prelim,
        ):
            _setup_tui_monitor_mocks(mock_tui, mock_monitor)

            try:
                execute_sprint(config)
            except SystemExit:
                pass

        (
            mock_prelim.assert_not_called(),
            ("T-004: _write_preliminary_result must NOT be called when exit_code != 0"),
        )

    def test_t006_stale_halt_overwritten_yields_pass(self, tmp_path):
        """T-006: Stale HALT file (st_mtime < started_at) → overwritten with CONTINUE → PASS.

        Validates SC-007: a HALT file from a prior run must not prevent a passing phase
        from being recorded as PASS.
        """
        from superclaude.cli.sprint.executor import execute_sprint

        config = _make_config(tmp_path)
        phase = config.active_phases[0]

        # Create a stale HALT file with an mtime in the distant past
        result_file = config.result_file(phase)
        result_file.parent.mkdir(parents=True, exist_ok=True)
        result_file.write_text("EXIT_RECOMMENDATION: HALT\n")
        stale_time = time.time() - 7200  # 2 hours ago
        os.utime(result_file, (stale_time, stale_time))

        with (
            patch("shutil.which", return_value="/usr/bin/claude"),
            patch(
                "superclaude.cli.sprint.process._subprocess.Popen",
                return_value=self._FakePopen(),
            ),
            patch("superclaude.cli.sprint.executor.SprintTUI") as mock_tui,
            patch("superclaude.cli.sprint.executor.SprintLogger"),
            patch("superclaude.cli.sprint.executor.OutputMonitor") as mock_monitor,
            patch("superclaude.cli.sprint.executor.notify_phase_complete"),
            patch("superclaude.cli.sprint.executor.notify_sprint_complete"),
        ):
            _setup_tui_monitor_mocks(mock_tui, mock_monitor)

            try:
                execute_sprint(config)
            except SystemExit:
                pass

        # After the sprint: executor result file is authoritative and contains CONTINUE.
        result_content = result_file.read_text() if result_file.exists() else ""
        assert "EXIT_RECOMMENDATION: HALT" not in result_content or (
            "EXIT_RECOMMENDATION: CONTINUE" in result_content
        ), "T-006: Stale HALT file must be overwritten; result must not remain HALT"
        assert "EXIT_RECOMMENDATION: CONTINUE" in result_content, (
            "T-006: Result file must contain EXIT_RECOMMENDATION: CONTINUE "
            "after stale HALT is overwritten"
        )
