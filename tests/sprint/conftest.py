"""Shared fixtures for the sprint test suite.

Hermetic-narrative guard
------------------------
Many sprint tests patch ``subprocess.Popen`` at the shared-module level
(``patch("superclaude.cli.pipeline.process.subprocess.Popen")``), which mutates
the *global* ``subprocess.Popen`` attribute. When ``claude`` is on PATH, the
phase-summarizer's narrative step (``PhaseSummarizer.narrate -> invoke_sonnet ->
subprocess.run``) spawns a real subprocess that *also* resolves to the patched
``Popen``, consuming an extra fake-factory call. For fakes whose factory indexes
by call count (e.g. ``test_output_monitor_lifecycle``'s ``config.phases[n-1]``),
that extra call corrupts the count and raises ``IndexError``; for the others it
surfaces as a swallowed "does not support the context manager protocol" warning.

This autouse fixture neutralises the leak for the whole suite by stubbing the
narrative step (which is best-effort and always swallowed in production anyway).
Modules that test the narrative path itself opt out so their assertions still run
against the real implementation.
"""

import pytest

# Modules that exercise invoke_sonnet / narrate / PhaseSummarizer directly and
# therefore must keep the real (un-stubbed) narrative implementation.
_NARRATIVE_TEST_MODULES = {
    "test_summarizer",
    "test_retrospective",
    "test_backward_compat_regression",
}


@pytest.fixture(autouse=True)
def _stub_phase_narrative(request, monkeypatch):
    """Prevent the summarizer narrative from spawning the real ``claude`` subprocess.

    See module docstring for the leak this closes. Narrative-testing modules
    opt out via ``_NARRATIVE_TEST_MODULES``.
    """
    if request.module.__name__.split(".")[-1] in _NARRATIVE_TEST_MODULES:
        return
    _noop_narrative = lambda *args, **kwargs: ""  # noqa: E731
    monkeypatch.setattr(
        "superclaude.cli.sprint.summarizer.invoke_sonnet",
        _noop_narrative,
    )
    # ``retrospective.py`` does ``from .summarizer import invoke_sonnet``, which
    # binds the name at import time into its own module namespace. Patching only
    # the ``summarizer`` symbol above leaves ``retrospective.invoke_sonnet``
    # pointing at the real implementation, so ``RetrospectiveGenerator.narrate``
    # can still spawn a real ``claude`` subprocess and consume a call-count-indexed
    # patched ``subprocess.Popen``. Neutralise that second binding too.
    monkeypatch.setattr(
        "superclaude.cli.sprint.retrospective.invoke_sonnet",
        _noop_narrative,
    )
