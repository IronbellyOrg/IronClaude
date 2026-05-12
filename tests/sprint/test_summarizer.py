"""TUI v2 Wave 3 (v3.7) — summarizer tests.

Covers:
- NDJSON extraction for all 5 categories (tasks, files, validations,
  reasoning, errors).
- Haiku subprocess helper: success, failure, timeout, claude-not-found.
- PhaseSummarizer.summarize end-to-end with mocked subprocess + fs.
- SummaryWorker thread safety under concurrent submits.
- SummaryWorker exception isolation (bad summarizer never crashes
  sprint).
- Markdown rendering for with-narrative and without-narrative paths.
"""

from __future__ import annotations

import json
import subprocess
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest.mock import MagicMock, patch

from superclaude.cli.sprint.models import (
    Phase,
    PhaseResult,
    PhaseStatus,
    SprintConfig,
)
from superclaude.cli.sprint.summarizer import (
    PhaseSummarizer,
    PhaseSummary,
    SummaryWorker,
    _build_phase_narrative_prompt,
    _render_phase_summary_markdown,
    extract_phase_signals,
    invoke_haiku,
)

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


def _make_config(tmp_path: Path) -> SprintConfig:
    phases = [
        Phase(
            number=1,
            file=tmp_path / "phase-1-tasklist.md",
            name="Foundation",
        )
    ]
    # The phase tasklist doesn't need real contents for these tests,
    # but the file must exist so load_sprint_config-style paths work.
    phases[0].file.write_text("# Phase 1\n\n### T01.01 -- Implement foo\n")
    index = tmp_path / "tasklist-index.md"
    index.write_text("| # | File |\n|---|------|\n| 1 | phase-1-tasklist.md |\n")
    return SprintConfig(
        index_path=index,
        release_dir=tmp_path,
        phases=phases,
    )


def _make_phase_result() -> PhaseResult:
    now = datetime.now(timezone.utc)
    return PhaseResult(
        phase=Phase(number=1, file=Path("/tmp/p1.md"), name="Foundation"),
        status=PhaseStatus.PASS,
        started_at=now - timedelta(seconds=30),
        finished_at=now,
        turns=4,
        tokens_in=100,
        tokens_out=200,
        output_bytes=1024,
        files_changed=2,
    )


def _write_ndjson(path: Path, events: list[dict]) -> Path:
    lines = [json.dumps(e) for e in events]
    path.write_text("\n".join(lines) + "\n")
    return path


# ---------------------------------------------------------------------------
# NDJSON extraction
# ---------------------------------------------------------------------------


class TestExtractPhaseSignals:
    def test_returns_empty_dict_on_missing_file(self, tmp_path):
        out = extract_phase_signals(tmp_path / "nope.txt")
        assert out == {
            "tasks": [],
            "files_changed": [],
            "validations": [],
            "reasoning_excerpts": [],
            "errors": [],
        }

    def test_task_status_detection(self, tmp_path):
        events = [
            {
                "type": "assistant",
                "message": {
                    "content": [
                        {"type": "text", "text": "Working on T01.01 — COMPLETE"},
                    ],
                },
            },
            {
                "type": "assistant",
                "message": {
                    "content": [{"type": "text", "text": "Task T01.02 FAIL: flaky"}]
                },
            },
            {
                "type": "assistant",
                "message": {
                    "content": [{"type": "text", "text": "Touched T01.03 briefly"}]
                },
            },
        ]
        out = extract_phase_signals(_write_ndjson(tmp_path / "out.txt", events))
        by_id = {t["task_id"]: t["status"] for t in out["tasks"]}
        assert by_id["T01.01"] == "PASS"
        assert by_id["T01.02"] == "FAIL"
        assert by_id["T01.03"] == "TOUCHED"

    def test_files_changed_from_tool_use(self, tmp_path):
        events = [
            {
                "type": "assistant",
                "message": {
                    "content": [
                        {
                            "type": "tool_use",
                            "name": "Edit",
                            "input": {"file_path": "src/foo.py"},
                        }
                    ]
                },
            },
            {
                "type": "assistant",
                "message": {
                    "content": [
                        {
                            "type": "tool_use",
                            "name": "Write",
                            "input": {"file_path": "src/bar.py"},
                        }
                    ]
                },
            },
            {
                "type": "assistant",
                "message": {
                    "content": [
                        {
                            "type": "tool_use",
                            "name": "Read",
                            "input": {"file_path": "src/baz.py"},
                        }
                    ]
                },
            },
        ]
        out = extract_phase_signals(_write_ndjson(tmp_path / "out.txt", events))
        paths = {f["path"] for f in out["files_changed"]}
        # Read is not a file-changing tool → excluded.
        assert paths == {"src/foo.py", "src/bar.py"}

    def test_validation_evidence(self, tmp_path):
        events = [
            {
                "type": "assistant",
                "message": {
                    "content": [
                        {"type": "text", "text": "Running pytest... 12 passed."}
                    ]
                },
            },
            {
                "type": "assistant",
                "message": {"content": [{"type": "text", "text": "ruff passed"}]},
            },
        ]
        out = extract_phase_signals(_write_ndjson(tmp_path / "out.txt", events))
        checks = {v["check"].lower() for v in out["validations"]}
        assert "pytest" in checks
        assert "ruff" in checks

    def test_errors_from_is_error_flag(self, tmp_path):
        events = [
            {
                "type": "assistant",
                "message": {
                    "content": [
                        {"type": "tool_use", "name": "Bash", "input": {"command": "x"}},
                    ]
                },
            },
            {
                "type": "user",
                "message": {
                    "content": [
                        {
                            "type": "tool_result",
                            "tool_use_id": "id1",
                            "content": "permission denied",
                            "is_error": True,
                        }
                    ]
                },
            },
        ]
        out = extract_phase_signals(_write_ndjson(tmp_path / "out.txt", events))
        assert len(out["errors"]) == 1
        assert out["errors"][0]["tool"] == "Bash"
        assert "permission denied" in out["errors"][0]["message"]

    def test_bash_exit_code_error(self, tmp_path):
        events = [
            {
                "type": "user",
                "message": {
                    "content": [
                        {
                            "type": "tool_result",
                            "tool_use_id": "id1",
                            "content": 'exit_code: 2\nstderr: boom',
                            "is_error": False,
                        }
                    ]
                },
            }
        ]
        out = extract_phase_signals(_write_ndjson(tmp_path / "out.txt", events))
        assert len(out["errors"]) == 1

    def test_reasoning_excerpts_capped(self, tmp_path):
        events = [
            {
                "type": "assistant",
                "message": {
                    "content": [
                        {
                            "type": "text",
                            "text": "x" * 600,
                        }
                    ]
                },
            }
            for _ in range(6)
        ]
        out = extract_phase_signals(_write_ndjson(tmp_path / "out.txt", events))
        # Cap is 3 excerpts at 400 chars each.
        assert 0 < len(out["reasoning_excerpts"]) <= 3
        assert all(len(r) <= 400 for r in out["reasoning_excerpts"])

    def test_malformed_lines_skipped(self, tmp_path):
        path = tmp_path / "out.txt"
        path.write_text('not json\n{"type":"assistant","message":{"content":[{"type":"text","text":"ok"}]}}\n')
        out = extract_phase_signals(path)
        assert out["reasoning_excerpts"] == ["ok"]


# ---------------------------------------------------------------------------
# Haiku subprocess helper
# ---------------------------------------------------------------------------


class TestInvokeHaiku:
    def test_returns_empty_when_claude_not_on_path(self):
        with patch("superclaude.cli.sprint.summarizer.shutil.which", return_value=None):
            assert invoke_haiku("hello") == ""

    def test_success_returns_stdout_stripped(self):
        fake_result = MagicMock(returncode=0, stdout=b"  narrative text  ", stderr=b"")
        with (
            patch(
                "superclaude.cli.sprint.summarizer.shutil.which",
                return_value="/usr/bin/claude",
            ),
            patch(
                "superclaude.cli.sprint.summarizer.subprocess.run",
                return_value=fake_result,
            ) as run,
        ):
            out = invoke_haiku("prompt")
            assert out == "narrative text"
            call = run.call_args
            cmd = call.args[0]
            assert "--model" in cmd and "claude-haiku-4-5" in cmd
            assert "--max-turns" in cmd and "1" in cmd
            assert "--dangerously-skip-permissions" in cmd
            # stdin must be DEVNULL.
            assert call.kwargs["stdin"] == subprocess.DEVNULL
            # Env vars stripped.
            env = call.kwargs["env"]
            assert "CLAUDECODE" not in env
            assert "CLAUDE_CODE_ENTRYPOINT" not in env

    def test_nonzero_exit_returns_empty(self):
        fake_result = MagicMock(returncode=2, stdout=b"", stderr=b"boom")
        with (
            patch(
                "superclaude.cli.sprint.summarizer.shutil.which",
                return_value="/usr/bin/claude",
            ),
            patch(
                "superclaude.cli.sprint.summarizer.subprocess.run",
                return_value=fake_result,
            ),
        ):
            assert invoke_haiku("x") == ""

    def test_timeout_returns_empty(self):
        with (
            patch(
                "superclaude.cli.sprint.summarizer.shutil.which",
                return_value="/usr/bin/claude",
            ),
            patch(
                "superclaude.cli.sprint.summarizer.subprocess.run",
                side_effect=subprocess.TimeoutExpired(cmd="claude", timeout=30),
            ),
        ):
            assert invoke_haiku("x") == ""

    def test_oserror_returns_empty(self):
        with (
            patch(
                "superclaude.cli.sprint.summarizer.shutil.which",
                return_value="/usr/bin/claude",
            ),
            patch(
                "superclaude.cli.sprint.summarizer.subprocess.run",
                side_effect=OSError("nope"),
            ),
        ):
            assert invoke_haiku("x") == ""


# ---------------------------------------------------------------------------
# PhaseSummarizer
# ---------------------------------------------------------------------------


class TestPhaseSummarizer:
    def test_summarize_writes_markdown_file(self, tmp_path):
        config = _make_config(tmp_path)
        phase = config.phases[0]
        pr = _make_phase_result()
        pr.phase = phase

        # Seed NDJSON output so extract has something to find.
        output_path = config.output_file(phase)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        _write_ndjson(
            output_path,
            [
                {
                    "type": "assistant",
                    "message": {
                        "content": [
                            {"type": "text", "text": "T01.01 COMPLETE"},
                            {
                                "type": "tool_use",
                                "name": "Edit",
                                "input": {"file_path": "src/foo.py"},
                            },
                        ]
                    },
                }
            ],
        )

        summarizer = PhaseSummarizer(config)
        with patch(
            "superclaude.cli.sprint.summarizer.invoke_haiku",
            return_value="Narrative text",
        ):
            summary = summarizer.summarize(phase, pr)

        assert isinstance(summary, PhaseSummary)
        assert summary.narrative == "Narrative text"
        assert any(t["task_id"] == "T01.01" for t in summary.tasks)
        assert any(f["path"] == "src/foo.py" for f in summary.files_changed)

        # Markdown file written.
        target = config.results_dir / f"phase-{phase.number}-summary.md"
        assert target.exists()
        text = target.read_text()
        assert "Phase 1 Summary" in text
        assert "Narrative text" in text
        assert "T01.01" in text
        assert "src/foo.py" in text

    def test_summarize_tolerates_narrative_failure(self, tmp_path):
        config = _make_config(tmp_path)
        phase = config.phases[0]
        pr = _make_phase_result()
        pr.phase = phase

        output_path = config.output_file(phase)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text("")

        summarizer = PhaseSummarizer(config)
        with patch(
            "superclaude.cli.sprint.summarizer.invoke_haiku",
            side_effect=RuntimeError("boom"),
        ):
            summary = summarizer.summarize(phase, pr)

        assert summary.narrative == ""
        target = config.results_dir / f"phase-{phase.number}-summary.md"
        assert target.exists()
        assert "Narrative unavailable" in target.read_text()

    def test_prompt_mentions_phase_stats(self, tmp_path):
        config = _make_config(tmp_path)
        phase = config.phases[0]
        pr = _make_phase_result()
        pr.phase = phase
        summary = PhaseSummary(phase=phase, phase_result=pr)
        prompt = _build_phase_narrative_prompt(summary)
        assert "Phase 1" in prompt
        assert "4 turns" in prompt
        assert "PASS" in prompt

    def test_render_markdown_without_narrative(self, tmp_path):
        config = _make_config(tmp_path)
        phase = config.phases[0]
        pr = _make_phase_result()
        pr.phase = phase
        summary = PhaseSummary(phase=phase, phase_result=pr)
        text = _render_phase_summary_markdown(summary)
        assert "Narrative unavailable" in text
        assert "No task IDs found" in text


# ---------------------------------------------------------------------------
# SummaryWorker
# ---------------------------------------------------------------------------


class TestSummaryWorker:
    def test_concurrent_submit_is_thread_safe(self):
        """Many concurrent submissions must not lose or race entries."""
        summarizer = MagicMock()

        def fake_summarize(phase, phase_result):
            # Force a visible interleave so the lock is stressed.
            import time as _time

            _time.sleep(0.001)
            return PhaseSummary(phase=phase, phase_result=phase_result)

        summarizer.summarize.side_effect = fake_summarize
        worker = SummaryWorker(summarizer)

        phases = [Phase(number=i, file=Path(f"/tmp/p{i}.md")) for i in range(1, 25)]
        pr = _make_phase_result()
        threads = [worker.submit(p, pr) for p in phases]
        for t in threads:
            t.join(timeout=5)

        summaries = worker.get_summaries()
        assert set(summaries.keys()) == {p.number for p in phases}
        assert summarizer.summarize.call_count == len(phases)

    def test_summarize_exception_never_propagates(self):
        """A blowing-up summarizer must not take the worker down."""
        summarizer = MagicMock()
        summarizer.summarize.side_effect = RuntimeError("explode")
        worker = SummaryWorker(summarizer)

        phase = Phase(number=1, file=Path("/tmp/p1.md"))
        thread = worker.submit(phase, _make_phase_result())
        thread.join(timeout=5)

        # Worker dict is untouched; no entry was committed.
        assert worker.get_summaries() == {}

    def test_wait_blocks_until_all_done(self):
        summarizer = MagicMock()
        summarizer.summarize.return_value = PhaseSummary(
            phase=Phase(number=1, file=Path("/tmp/p1.md")),
            phase_result=_make_phase_result(),
        )
        worker = SummaryWorker(summarizer)

        phases = [Phase(number=i, file=Path(f"/tmp/p{i}.md")) for i in range(1, 4)]
        for p in phases:
            worker.submit(p, _make_phase_result())
        worker.wait(timeout=5)
        for t in worker._threads:
            assert not t.is_alive()

    def test_get_summaries_returns_snapshot(self):
        """Returned dict must be independent of internal storage."""
        summarizer = MagicMock()
        summarizer.summarize.return_value = PhaseSummary(
            phase=Phase(number=1, file=Path("/tmp/p1.md")),
            phase_result=_make_phase_result(),
        )
        worker = SummaryWorker(summarizer)
        worker.submit(Phase(number=1, file=Path("/tmp/p1.md")), _make_phase_result())
        worker.wait(timeout=5)
        snapshot = worker.get_summaries()
        # Mutating the snapshot must not affect the worker.
        snapshot.clear()
        assert worker.get_summaries()

    # ------------------------------------------------------------------
    # TUI v2 Wave 4 (v3.7, F9): on_summary_ready callback fanout
    # ------------------------------------------------------------------

    def test_on_summary_ready_fires_once_with_committed_summary(self):
        phase = Phase(number=1, file=Path("/tmp/p1.md"))
        committed = PhaseSummary(phase=phase, phase_result=_make_phase_result())

        summarizer = MagicMock()
        summarizer.summarize.return_value = committed

        received: list[PhaseSummary] = []

        def on_ready(s: PhaseSummary) -> None:
            received.append(s)

        worker = SummaryWorker(summarizer, on_summary_ready=on_ready)
        thread = worker.submit(phase, _make_phase_result())
        thread.join(timeout=5)

        assert received == [committed]
        assert worker.get_summaries()[1] is committed

    def test_on_summary_ready_exception_does_not_crash_worker(self):
        phase = Phase(number=1, file=Path("/tmp/p1.md"))
        summarizer = MagicMock()
        summarizer.summarize.return_value = PhaseSummary(
            phase=phase, phase_result=_make_phase_result()
        )

        def on_ready(_: PhaseSummary) -> None:
            raise RuntimeError("tmux gone")

        worker = SummaryWorker(summarizer, on_summary_ready=on_ready)
        thread = worker.submit(phase, _make_phase_result())
        thread.join(timeout=5)

        # Summary still committed — callback failure is isolated.
        assert 1 in worker.get_summaries()

    def test_on_summary_ready_not_called_when_summarize_raises(self):
        summarizer = MagicMock()
        summarizer.summarize.side_effect = RuntimeError("boom")
        received: list[PhaseSummary] = []

        def on_ready(s: PhaseSummary) -> None:
            received.append(s)

        worker = SummaryWorker(summarizer, on_summary_ready=on_ready)
        thread = worker.submit(
            Phase(number=1, file=Path("/tmp/p1.md")), _make_phase_result()
        )
        thread.join(timeout=5)

        assert received == []
        assert worker.get_summaries() == {}

    def test_summarizer_write_sets_summary_path(self, tmp_path):
        config = _make_config(tmp_path)
        phase = config.phases[0]
        pr = _make_phase_result()
        pr.phase = phase

        # Empty NDJSON — extractors return empty lists; we only care
        # about the path stamping contract.
        config.output_file(phase).parent.mkdir(parents=True, exist_ok=True)
        config.output_file(phase).write_text("")

        summarizer = PhaseSummarizer(config)
        with patch(
            "superclaude.cli.sprint.summarizer.invoke_haiku", return_value=""
        ):
            summary = summarizer.summarize(phase, pr)

        assert summary.path is not None
        assert summary.path.name == f"phase-{phase.number}-summary.md"
        assert summary.path.exists()
