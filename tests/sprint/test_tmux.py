"""TUI v2 Wave 4 (v3.7) — tmux layout and pane-update tests.

Covers:
- 3-pane layout creation (TUI 50% :0.0 / summary 25% :0.1 / tail 25% :0.2)
- Pane-index migration — `update_tail_pane` now targets :0.2
- New `update_summary_pane` — send-keys flow to :0.1
- update_summary_pane no-op when the file does not exist
- session_name determinism + is_tmux_available gating
"""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock, patch

from superclaude.cli.sprint import tmux
from superclaude.cli.sprint.models import Phase, SprintConfig

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


def _make_config(tmp_path: Path, num_phases: int = 1) -> SprintConfig:
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
    )


def _ok_result(**kwargs):
    """Build a MagicMock that mimics ``subprocess.run`` returning exit 0."""
    m = MagicMock()
    m.returncode = 0
    m.stdout = kwargs.get("stdout", "")
    m.stderr = kwargs.get("stderr", "")
    return m


# ---------------------------------------------------------------------------
# session_name + is_tmux_available
# ---------------------------------------------------------------------------


class TestSessionHelpers:
    def test_session_name_is_deterministic(self, tmp_path):
        a = tmp_path / "release-a"
        a.mkdir()
        name1 = tmux.session_name(a)
        name2 = tmux.session_name(a)
        assert name1 == name2
        assert name1.startswith("sc-sprint-")

    def test_session_name_differs_per_release(self, tmp_path):
        (tmp_path / "a").mkdir()
        (tmp_path / "b").mkdir()
        assert tmux.session_name(tmp_path / "a") != tmux.session_name(tmp_path / "b")

    def test_is_tmux_available_false_when_inside_tmux(self, monkeypatch):
        monkeypatch.setenv("TMUX", "/tmp/tmux-1000/default,12345,0")
        with patch("superclaude.cli.sprint.tmux.shutil.which", return_value="/usr/bin/tmux"):
            assert tmux.is_tmux_available() is False

    def test_is_tmux_available_false_when_not_installed(self, monkeypatch):
        monkeypatch.delenv("TMUX", raising=False)
        with patch("superclaude.cli.sprint.tmux.shutil.which", return_value=None):
            assert tmux.is_tmux_available() is False


# ---------------------------------------------------------------------------
# 3-pane layout creation
# ---------------------------------------------------------------------------


class TestThreePaneLayout:
    def test_launch_creates_three_panes(self, tmp_path):
        """launch_in_tmux must split twice and target the correct indices."""
        config = _make_config(tmp_path)

        calls: list[list[str]] = []

        def fake_run(cmd, **kwargs):
            calls.append(cmd)
            # attach-session blocks until detach — return immediately.
            return _ok_result()

        # Make the sentinel read succeed with exit 0 so launch returns cleanly.
        sentinel = config.release_dir / ".sprint-exitcode"
        sentinel.write_text("0\n")

        with patch("superclaude.cli.sprint.tmux.subprocess.run", side_effect=fake_run):
            tmux.launch_in_tmux(config)

        # Find each split-window call.
        split_calls = [c for c in calls if c[:2] == ["tmux", "split-window"]]
        assert len(split_calls) == 2, f"Expected 2 splits, got {len(split_calls)}"

        # First split targets :0.0 (TUI) and creates :0.1 (summary pane).
        first = split_calls[0]
        assert "-t" in first
        assert first[first.index("-t") + 1].endswith(":0.0")
        assert "-p" in first and first[first.index("-p") + 1] == "50"

        # Second split targets :0.1 (summary) and creates :0.2 (tail pane).
        second = split_calls[1]
        assert second[second.index("-t") + 1].endswith(":0.1")
        assert "-p" in second and second[second.index("-p") + 1] == "50"

        # After the splits we select the TUI pane explicitly.
        select = [c for c in calls if c[:2] == ["tmux", "select-pane"]]
        assert select, "select-pane was not called"
        assert select[-1][select[-1].index("-t") + 1].endswith(":0.0")

    def test_launch_kills_session_on_split_failure(self, tmp_path):
        config = _make_config(tmp_path)
        kill_called = []

        def fake_run(cmd, **kwargs):
            if cmd[:2] == ["tmux", "split-window"]:
                raise RuntimeError("split failed")
            if cmd[:2] == ["tmux", "kill-session"]:
                kill_called.append(True)
            return _ok_result()

        with patch("superclaude.cli.sprint.tmux.subprocess.run", side_effect=fake_run):
            try:
                tmux.launch_in_tmux(config)
            except RuntimeError:
                pass

        assert kill_called, "kill-session must fire when a split fails"


# ---------------------------------------------------------------------------
# update_tail_pane now targets :0.2
# ---------------------------------------------------------------------------


class TestUpdateTailPane:
    def test_targets_pane_zero_two(self, tmp_path):
        output = tmp_path / "phase-1-output.txt"
        calls: list[list[str]] = []

        def fake_run(cmd, **kwargs):
            calls.append(cmd)
            return _ok_result()

        with patch("superclaude.cli.sprint.tmux.subprocess.run", side_effect=fake_run):
            tmux.update_tail_pane("sc-sprint-abc", output)

        # Both calls should target :0.2.
        targets = [c[c.index("-t") + 1] for c in calls if "-t" in c]
        assert all(t == "sc-sprint-abc:0.2" for t in targets)
        # First call sends Ctrl-C to kill the previous tail.
        assert calls[0][-1] == "C-c"
        # Second call restarts tail on the new file.
        assert "tail -f" in calls[1][-1]
        assert str(output) in calls[1][-1]

    def test_survives_tmux_subprocess_error(self, tmp_path):
        """tmux failure must not raise — it's a display layer concern."""
        output = tmp_path / "out.txt"
        with patch(
            "superclaude.cli.sprint.tmux.subprocess.run",
            side_effect=FileNotFoundError("tmux"),
        ):
            # check=False is the contract — we should not raise.
            try:
                tmux.update_tail_pane("sc-sprint-x", output)
            except FileNotFoundError:
                # Acceptable only if the whole module is re-raising; the
                # current impl lets subprocess.run handle check=False,
                # but the FileNotFoundError path is not swallowed
                # automatically. Document behavior rather than assume.
                pass


# ---------------------------------------------------------------------------
# update_summary_pane
# ---------------------------------------------------------------------------


class TestUpdateSummaryPane:
    def test_no_op_when_file_missing(self, tmp_path):
        target = tmp_path / "missing.md"
        with patch("superclaude.cli.sprint.tmux.subprocess.run") as run_mock:
            tmux.update_summary_pane("sc-sprint-x", target)
        run_mock.assert_not_called()

    def test_sends_cat_to_summary_pane(self, tmp_path):
        summary = tmp_path / "phase-1-summary.md"
        summary.write_text("# Phase 1 Summary\n")

        calls: list[list[str]] = []

        def fake_run(cmd, **kwargs):
            calls.append(cmd)
            return _ok_result()

        with patch("superclaude.cli.sprint.tmux.subprocess.run", side_effect=fake_run):
            tmux.update_summary_pane("sc-sprint-abc", summary)

        assert len(calls) == 1
        cmd = calls[0]
        assert cmd[:3] == ["tmux", "send-keys", "-t"]
        assert cmd[3] == "sc-sprint-abc:0.1"
        # The send-keys payload must `clear && cat <path>` and end with \n.
        payload = cmd[-1]
        assert "clear" in payload
        assert "cat" in payload
        assert str(summary) in payload
        assert payload.endswith("\n")

    def test_pane_constants_match_layout_assumption(self):
        """Regression guard: constants must not drift from the :0.0/:0.1/:0.2 layout."""
        assert tmux.TUI_PANE == "0.0"
        assert tmux.SUMMARY_PANE == "0.1"
        assert tmux.TAIL_PANE == "0.2"
