"""Tests for the issue-watch command runner (no real child except one sleeper)."""

from __future__ import annotations

import subprocess
import sys
import time

import pytest

from superclaude.cli.issue_watch import runner as runner_mod
from superclaude.cli.issue_watch.runner import (
    STDERR_CAP_BYTES,
    CommandResult,
    SubprocessRunner,
)


class RecordingRun:
    """A stand-in for ``subprocess.run`` that records calls and returns or raises."""

    def __init__(
        self,
        *,
        stdout: str = "",
        stderr: str = "",
        returncode: int = 0,
        raises: BaseException | None = None,
    ) -> None:
        self.stdout = stdout
        self.stderr = stderr
        self.returncode = returncode
        self.raises = raises
        self.calls: list[tuple[object, dict[str, object]]] = []

    def __call__(self, argv, **kwargs):
        self.calls.append((argv, kwargs))
        if self.raises is not None:
            raise self.raises
        return subprocess.CompletedProcess(
            argv, self.returncode, self.stdout, self.stderr
        )


@pytest.fixture
def fake_run(monkeypatch):
    """Install a ``RecordingRun`` as ``subprocess.run`` seen by the runner module."""

    def install(**kwargs) -> RecordingRun:
        recorder = RecordingRun(**kwargs)
        monkeypatch.setattr(runner_mod.subprocess, "run", recorder)
        return recorder

    return install


def test_str_argv_raises_type_error__nfr004(fake_run):
    """A bare string argv is refused (NFR-004: no shell string ever runs)."""
    recorder = fake_run()
    with pytest.raises(TypeError):
        SubprocessRunner().run("gh issue list", 5)  # type: ignore[arg-type]
    assert recorder.calls == []


def test_list_with_non_str_raises_type_error__nfr004(fake_run):
    """A list holding a non-str item is refused (NFR-004)."""
    recorder = fake_run()
    with pytest.raises(TypeError):
        SubprocessRunner().run(["gh", 7], 5)  # type: ignore[list-item]
    assert recorder.calls == []


@pytest.mark.parametrize("argv", [[], ()], ids=["empty-list", "empty-tuple"])
def test_empty_argv_raises_type_error_and_starts_nothing__nfr004(fake_run, argv):
    """An empty argv is refused with TypeError, never an IndexError from the OS."""
    recorder = fake_run()
    with pytest.raises(TypeError, match="non-empty list of str"):
        SubprocessRunner().run(argv, 5)  # type: ignore[arg-type]
    assert recorder.calls == []


def test_list_argv_reaches_subprocess_run_without_shell__nfr004(fake_run):
    """A list argv reaches subprocess.run with shell=False and closed stdin (NFR-004)."""
    recorder = fake_run(stdout="out", stderr="err", returncode=3)
    result = SubprocessRunner().run(["gh", "--version"], 7.5)
    assert len(recorder.calls) == 1
    argv, kwargs = recorder.calls[0]
    assert argv == ["gh", "--version"]
    assert kwargs["shell"] is False
    assert kwargs["capture_output"] is True
    assert kwargs["text"] is True
    assert kwargs["encoding"] == "utf-8"
    assert kwargs["errors"] == "replace"
    assert kwargs["stdin"] == subprocess.DEVNULL
    assert kwargs["timeout"] == 7.5
    assert isinstance(result, CommandResult)
    assert result.argv == ("gh", "--version")
    assert result.returncode == 3
    assert result.stdout == "out"
    assert result.stderr == "err"
    assert result.timed_out is False
    assert result.spawn_error is None
    assert result.duration_s >= 0.0


def test_cwd_is_passed_when_given_and_none_otherwise(fake_run):
    """cwd reaches subprocess.run when given and is None otherwise (DF-01)."""
    recorder = fake_run()
    SubprocessRunner().run(["git", "status"], 5, cwd="/some/dir")
    SubprocessRunner().run(["git", "status"], 5)
    assert recorder.calls[0][1]["cwd"] == "/some/dir"
    assert recorder.calls[1][1]["cwd"] is None


def test_short_stderr_is_kept_whole(fake_run):
    """Stderr within the cap is returned unchanged."""
    fake_run(stderr="a" * STDERR_CAP_BYTES)
    result = SubprocessRunner().run(["x"], 5)
    assert result.stderr == "a" * STDERR_CAP_BYTES


def test_long_stderr_is_cut_to_500_bytes(fake_run):
    """Stderr longer than 500 bytes is cut to at most 500 bytes."""
    fake_run(stderr="b" * 2000)
    result = SubprocessRunner().run(["x"], 5)
    assert result.stderr == "b" * 500


def test_stderr_cut_inside_multibyte_character_drops_the_partial_char(fake_run):
    """A multi-byte character split by the cap is dropped, never half kept."""
    fake_run(stderr="a" * 499 + "é" * 3)
    result = SubprocessRunner().run(["x"], 5)
    assert len(result.stderr.encode("utf-8")) <= 500
    assert result.stderr == "a" * 499


def test_timeout_expired_gives_timed_out_and_no_returncode(fake_run):
    """TimeoutExpired gives timed_out=True, returncode None, capped partial stderr."""
    exc = subprocess.TimeoutExpired(
        ["sleep"], 1, output=b"part", stderr=("c" * 600).encode()
    )
    fake_run(raises=exc)
    result = SubprocessRunner().run(["sleep"], 1)
    assert result.timed_out is True
    assert result.returncode is None
    assert result.spawn_error is None
    assert result.stdout == "part"
    assert result.stderr == "c" * 500


def test_timeout_expired_without_output_gives_empty_text(fake_run):
    """A timeout with no captured output gives empty strings, not None."""
    fake_run(raises=subprocess.TimeoutExpired(["sleep"], 1))
    result = SubprocessRunner().run(["sleep"], 1)
    assert result.timed_out is True
    assert result.stdout == ""
    assert result.stderr == ""


def test_spawn_error_is_the_class_name_only(fake_run):
    """A start failure gives spawn_error equal to the class name, never the message."""
    for error_class in (FileNotFoundError, PermissionError):
        fake_run(raises=error_class(2, "secret message /private/path"))
        result = SubprocessRunner().run(["nope"], 5)
        assert result.spawn_error == error_class.__name__
        assert result.returncode is None
        assert result.timed_out is False
        assert result.stdout == ""
        assert result.stderr == ""
        assert "secret" not in repr(result)
        assert "/private/path" not in repr(result)


def test_value_error_from_the_start_is_a_spawn_error_by_class_name(fake_run):
    """A ValueError at start (NUL byte) is reported, not raised, without its text."""
    fake_run(raises=ValueError("embedded null byte /private/path"))
    result = SubprocessRunner().run(["gh"], 5)
    assert result.spawn_error == "ValueError"
    assert result.returncode is None
    assert result.timed_out is False
    assert result.stdout == ""
    assert result.stderr == ""
    assert "null byte" not in repr(result)
    assert "/private/path" not in repr(result)


def test_real_nul_byte_in_argv_is_a_spawn_error_not_an_exception():
    """A real NUL in an argv item reaches the OS layer and comes back as a result."""
    result = SubprocessRunner().run(["gh\0--version"], 5)
    assert result.spawn_error == "ValueError"
    assert result.returncode is None
    assert result.timed_out is False
    assert result.argv == ("gh\0--version",)


def test_real_nul_byte_in_cwd_is_a_spawn_error_not_an_exception():
    """A real NUL in ``cwd`` is a spawn error too."""
    result = SubprocessRunner().run([sys.executable, "-c", "pass"], 5, cwd="a\0b")
    assert result.spawn_error == "ValueError"
    assert result.returncode is None


def test_real_child_non_utf8_output_is_replaced_not_raised():
    """Non-UTF-8 bytes on stdout and stderr give U+FFFD, not UnicodeDecodeError."""
    code = (
        "import sys; sys.stdout.buffer.write(b'ok\\xff\\xfe'); "
        "sys.stderr.buffer.write(b'bad\\xc3')"
    )
    result = SubprocessRunner().run([sys.executable, "-c", code], timeout=30)
    assert result.returncode == 0
    assert result.spawn_error is None
    assert result.timed_out is False
    assert result.stdout == "ok��"
    assert result.stderr == "bad�"


def test_real_child_timeout_returns_quickly__nfr008():
    """A real sleeping child is cut at the timeout and reported (DF-55 part c, NFR-008)."""
    start = time.monotonic()
    result = SubprocessRunner().run(
        [sys.executable, "-c", "import time; time.sleep(5)"], timeout=0.5
    )
    elapsed = time.monotonic() - start
    assert result.timed_out is True
    assert result.returncode is None
    assert elapsed < 4.0
