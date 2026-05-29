"""Tests for the R3-mit MCP retry-once policy (T05.23 / D-0101).

Pins the four acceptance bullets from the phase file:

* An eval carrying ``MCP_FLAKY_TAG`` (and only that tag) triggers
  retry-once on a stubbed MCP failure. On persistent failure the final
  status is ``FAIL`` with ``mcp_server_flaky`` present in
  ``outcome.artifacts``.
* Non-tagged evals do NOT retry — the NFR-REL2 default contract is
  honored (the executor's spawn/inject/observe trio fires exactly
  once).
* :class:`RetryOncePolicy` is an additive, orthogonal kwarg on
  ``EvalRunner``; wiring it does not relax the existing
  ``retry_count != 0`` rejection.
* The taxonomy of "flaky" outcomes is strictly ``FAIL``, ``ERRORED``,
  ``TIMEOUT``. ``PASS`` / ``SKIPPED`` / ``INTERRUPTED`` / ``XFAIL`` /
  ``XPASS`` do not trigger a retry.

The unit-level cases exercise :class:`RetryOncePolicy` in isolation
(eligibility, decision, annotation). The integration cases drive a
real ``EvalRunner`` with a counting executor and assert the
spawn/inject/observe trio fires the expected number of times.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, List

import pytest

from superclaude.cli.eval.config import EvalConfig
from superclaude.cli.eval.models import (
    EvalContext,
    EvalOutcome,
    EvalSpec,
    ExpectResult,
)
from superclaude.cli.eval.retry import (
    MCP_FLAKY_TAG,
    MCP_SERVER_FLAKY_ARTIFACT,
    RetryOncePolicy,
    is_flaky_outcome,
    is_mcp_flaky_tagged,
)
from superclaude.cli.eval.runner import (
    EvalRunner,
    ExecutorContext,
    LifecycleExecutor,
    ObservedRun,
)

# ---------------------------------------------------------------------------
# FakeHome — mirror of test_retry_policy.py's stand-in, but the setup()
# is callable more than once so a single instance survives the retry
# attempt's teardown -> setup cycle without raising the production
# ``HomeIsolation`` re-entry guard.
# ---------------------------------------------------------------------------


class FakeHome:
    """Re-entrant HomeIsolation stand-in for retry-policy tests."""

    def __init__(self, *, eval_id: str, home_root: Path) -> None:
        self.eval_id = eval_id
        self.home_root = home_root
        self._home_path: Path | None = None
        self.setup_count = 0
        self.teardown_count = 0

    def setup(self, *, config: EvalConfig) -> Path:
        self.setup_count += 1
        self.home_root.mkdir(parents=True, exist_ok=True)
        home = self.home_root / f"{self.eval_id}-fake-{self.setup_count}"
        home.mkdir(parents=True, exist_ok=True)
        self._home_path = home
        return home

    def teardown(self, keep: bool) -> None:
        self.teardown_count += 1
        self._home_path = None

    def env(self) -> dict[str, str]:
        return {"HOME": str(self.home_path), "CLAUDE_SESSION_ID": "sess-001"}

    @property
    def home_path(self) -> Path:
        if self._home_path is None:
            raise RuntimeError("FakeHome.setup() must be called before home_path")
        return self._home_path

    @property
    def is_set_up(self) -> bool:
        return self._home_path is not None


@dataclass
class ScriptedExecutor:
    """LifecycleExecutor whose observed exit_code is driven by a script.

    Each call to ``observe`` pops the next ``ObservedRun`` off
    ``script``. If the script is exhausted, the last entry is returned
    repeatedly — this lets the "persistent failure" case set a single
    failing entry and not have to worry about retry counts.
    """

    script: List[ObservedRun]
    spawn_count: int = 0
    inject_count: int = 0
    observe_count: int = 0
    _last: ObservedRun = field(init=False, repr=False)

    def __post_init__(self) -> None:
        if not self.script:
            raise ValueError("ScriptedExecutor requires at least one ObservedRun")
        self._last = self.script[-1]

    def spawn(self, ctx: ExecutorContext) -> None:
        self.spawn_count += 1

    def inject(self, ctx: ExecutorContext) -> None:
        self.inject_count += 1

    def observe(self, ctx: ExecutorContext) -> ObservedRun:
        index = self.observe_count
        self.observe_count += 1
        if index < len(self.script):
            return self.script[index]
        return self._last


# Static protocol conformance check — ScriptedExecutor satisfies the
# LifecycleExecutor protocol.
_PROTOCOL_CHECK: LifecycleExecutor = ScriptedExecutor(
    script=[ObservedRun(exit_code=0, stdout="", stderr="", duration_sec=0.0)]
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def scratch_root(tmp_path: Path) -> Path:
    root = tmp_path / "scratch"
    root.mkdir()
    return root


@pytest.fixture
def eval_config(scratch_root: Path) -> EvalConfig:
    return EvalConfig(allowed_scratch_roots=(scratch_root,))


@pytest.fixture
def home(scratch_root: Path) -> FakeHome:
    return FakeHome(eval_id="McpRetryEval1", home_root=scratch_root)


@pytest.fixture
def tagged_spec() -> EvalSpec:
    return EvalSpec(
        id="McpRetryEval1",
        title="mcp-flaky-eval",
        requires=(MCP_FLAKY_TAG,),
    )


@pytest.fixture
def untagged_spec() -> EvalSpec:
    return EvalSpec(
        id="McpRetryEval1",
        title="non-flaky-eval",
        requires=(),
    )


@pytest.fixture
def run_paths(tmp_path: Path) -> dict[str, Path]:
    run_dir = tmp_path / "run"
    run_dir.mkdir()
    artifacts_dir = run_dir / "artifacts"
    artifacts_dir.mkdir()
    return {
        "run_dir": run_dir,
        "artifacts_dir": artifacts_dir,
        "stdout_path": artifacts_dir / "stdout.log",
        "stderr_path": artifacts_dir / "stderr.log",
        "transcript_path": artifacts_dir / "pty.transcript",
    }


def _failing_expect() -> Callable[[EvalContext], ExpectResult]:
    def _expect(ctx: EvalContext) -> ExpectResult:
        return ExpectResult(name="boom", passed=False, message="induced fail")

    _expect.__name__ = "boom"
    return _expect


def _passing_expect() -> Callable[[EvalContext], ExpectResult]:
    def _expect(ctx: EvalContext) -> ExpectResult:
        return ExpectResult(name="ok", passed=True, message="passed")

    _expect.__name__ = "ok"
    return _expect


def _conditional_expect(home: FakeHome):
    """Return an expect that fails on first setup, passes on second.

    Used to drive the "retry recovers" case. We key off ``home.setup_count``
    because the runner calls ``home.setup`` exactly once per lifecycle.
    """

    def _expect(ctx: EvalContext) -> ExpectResult:
        if home.setup_count <= 1:
            return ExpectResult(
                name="flaky", passed=False, message="first attempt failed"
            )
        return ExpectResult(name="flaky", passed=True, message="retry recovered")

    _expect.__name__ = "flaky"
    return _expect


def _make_runner(
    *,
    home: FakeHome,
    eval_config: EvalConfig,
    executor: ScriptedExecutor,
    run_paths: dict[str, Path],
    expects: tuple = (),
    retry_policy: RetryOncePolicy | None = None,
    home_factory: Callable[[], FakeHome] | None = None,
) -> EvalRunner:
    return EvalRunner(
        home=home,  # type: ignore[arg-type]
        config=eval_config,
        executor=executor,
        run_dir=run_paths["run_dir"],
        artifacts_dir=run_paths["artifacts_dir"],
        stdout_path=run_paths["stdout_path"],
        stderr_path=run_paths["stderr_path"],
        transcript_path=run_paths["transcript_path"],
        expect_callables=expects,
        deploy_hooks=lambda _p: None,
        retry_policy=retry_policy,
        home_factory=home_factory,  # type: ignore[arg-type]
    )


# ---------------------------------------------------------------------------
# Unit tests — RetryOncePolicy in isolation
# ---------------------------------------------------------------------------


class TestRetryOncePolicyUnit:
    """Pin the policy's three decision points: eligibility, retry,
    annotate."""

    def test_constants_are_canonical(self) -> None:
        assert MCP_FLAKY_TAG == "MCP-flaky"
        assert MCP_SERVER_FLAKY_ARTIFACT == "mcp_server_flaky"
        # The class-level pin on EvalRunner must agree.
        assert EvalRunner.MCP_FLAKY_TAG == MCP_FLAKY_TAG

    def test_policy_is_eligible_for_tagged_spec(self) -> None:
        spec = EvalSpec(id="E1", title="t", requires=(MCP_FLAKY_TAG,))
        policy = RetryOncePolicy()
        assert policy.is_eligible(spec) is True

    def test_policy_is_eligible_for_tagged_spec_alongside_other_caps(self) -> None:
        """The tag may sit alongside any other capability string."""

        spec = EvalSpec(
            id="E1", title="t", requires=("mcp.tavily", MCP_FLAKY_TAG, "mcp.context7")
        )
        policy = RetryOncePolicy()
        assert policy.is_eligible(spec) is True

    def test_policy_not_eligible_for_untagged_spec(self) -> None:
        spec = EvalSpec(id="E1", title="t", requires=())
        policy = RetryOncePolicy()
        assert policy.is_eligible(spec) is False

    def test_policy_not_eligible_when_only_other_caps_present(self) -> None:
        spec = EvalSpec(id="E1", title="t", requires=("mcp.tavily", "mcp.context7"))
        policy = RetryOncePolicy()
        assert policy.is_eligible(spec) is False

    @pytest.mark.parametrize("status", ["FAIL", "ERRORED", "TIMEOUT"])
    def test_should_retry_on_flaky_status_for_tagged_spec(self, status: str) -> None:
        spec = EvalSpec(id="E1", title="t", requires=(MCP_FLAKY_TAG,))
        outcome = EvalOutcome(eval_id="E1", title="t", status=status, duration_sec=0.1)
        policy = RetryOncePolicy()
        assert policy.should_retry(spec, outcome) is True

    @pytest.mark.parametrize(
        "status", ["PASS", "SKIPPED", "INTERRUPTED", "XFAIL", "XPASS"]
    )
    def test_should_not_retry_on_non_flaky_status(self, status: str) -> None:
        spec = EvalSpec(id="E1", title="t", requires=(MCP_FLAKY_TAG,))
        outcome = EvalOutcome(eval_id="E1", title="t", status=status, duration_sec=0.1)
        policy = RetryOncePolicy()
        assert policy.should_retry(spec, outcome) is False

    def test_should_not_retry_untagged_even_on_fail(self) -> None:
        """Eligibility is the gate — a FAIL on an untagged spec stays a
        FAIL with no retry."""

        spec = EvalSpec(id="E1", title="t", requires=())
        outcome = EvalOutcome(eval_id="E1", title="t", status="FAIL", duration_sec=0.1)
        policy = RetryOncePolicy()
        assert policy.should_retry(spec, outcome) is False

    def test_annotate_adds_mcp_server_flaky_artifact(self) -> None:
        outcome = EvalOutcome(
            eval_id="E1", title="t", status="FAIL", duration_sec=0.1, artifacts={}
        )
        policy = RetryOncePolicy()
        annotated = policy.annotate(outcome)
        assert MCP_SERVER_FLAKY_ARTIFACT in annotated.artifacts
        assert annotated.artifacts[MCP_SERVER_FLAKY_ARTIFACT] == "true"
        # Every other field is preserved verbatim.
        assert annotated.status == "FAIL"
        assert annotated.eval_id == "E1"
        assert annotated.duration_sec == 0.1

    def test_annotate_preserves_existing_artifacts(self) -> None:
        outcome = EvalOutcome(
            eval_id="E1",
            title="t",
            status="FAIL",
            duration_sec=0.1,
            artifacts={"stdout": "/tmp/out.log"},
        )
        policy = RetryOncePolicy()
        annotated = policy.annotate(outcome)
        assert annotated.artifacts["stdout"] == "/tmp/out.log"
        assert annotated.artifacts[MCP_SERVER_FLAKY_ARTIFACT] == "true"

    def test_annotate_is_idempotent(self) -> None:
        """Re-applying annotate does not duplicate or overwrite."""

        outcome = EvalOutcome(
            eval_id="E1",
            title="t",
            status="FAIL",
            duration_sec=0.1,
            artifacts={MCP_SERVER_FLAKY_ARTIFACT: "true"},
        )
        policy = RetryOncePolicy()
        annotated = policy.annotate(outcome)
        # Same object identity is acceptable — the policy returns the
        # input unchanged when the artifact is already present.
        assert annotated.artifacts[MCP_SERVER_FLAKY_ARTIFACT] == "true"
        assert annotated == outcome

    def test_max_attempts_is_two(self) -> None:
        """The contract: one original attempt plus exactly one retry."""

        assert RetryOncePolicy.MAX_ATTEMPTS == 2

    def test_module_level_helpers_agree_with_policy(self) -> None:
        """``is_mcp_flaky_tagged`` and ``is_flaky_outcome`` are the
        functional building blocks the policy delegates to."""

        tagged = EvalSpec(id="E1", title="t", requires=(MCP_FLAKY_TAG,))
        untagged = EvalSpec(id="E2", title="t", requires=())
        assert is_mcp_flaky_tagged(tagged) is True
        assert is_mcp_flaky_tagged(untagged) is False

        for status in ["FAIL", "ERRORED", "TIMEOUT"]:
            outcome = EvalOutcome(
                eval_id="E1", title="t", status=status, duration_sec=0.1
            )
            assert is_flaky_outcome(outcome) is True
        for status in ["PASS", "SKIPPED", "INTERRUPTED", "XFAIL", "XPASS"]:
            outcome = EvalOutcome(
                eval_id="E1", title="t", status=status, duration_sec=0.1
            )
            assert is_flaky_outcome(outcome) is False


# ---------------------------------------------------------------------------
# Integration tests — EvalRunner + RetryOncePolicy
# ---------------------------------------------------------------------------


class TestEvalRunnerRetryIntegration:
    """Drive a real ``EvalRunner`` with a counting executor and verify
    the spawn/inject/observe trio fires the expected number of times
    under various policy + spec combinations."""

    def test_no_policy_means_no_retry_even_on_flaky_failure(
        self, tagged_spec, home, eval_config, run_paths
    ):
        """If the runner is constructed without a policy, the NFR-REL2
        default applies — no retry — even when the spec is tagged."""

        executor = ScriptedExecutor(
            script=[
                ObservedRun(exit_code=1, stdout="boom", stderr="", duration_sec=0.1)
            ]
        )
        runner = _make_runner(
            home=home,
            eval_config=eval_config,
            executor=executor,
            run_paths=run_paths,
            expects=(_failing_expect(),),
            retry_policy=None,
        )

        outcome = runner.run(tagged_spec)

        assert outcome.status == "FAIL"
        assert executor.spawn_count == 1
        assert executor.inject_count == 1
        assert executor.observe_count == 1
        assert MCP_SERVER_FLAKY_ARTIFACT not in outcome.artifacts

    def test_runner_does_not_retry_untagged_eval(
        self, untagged_spec, home, eval_config, run_paths
    ):
        """An untagged spec with a wired policy still does not retry."""

        executor = ScriptedExecutor(
            script=[
                ObservedRun(exit_code=1, stdout="boom", stderr="", duration_sec=0.1)
            ]
        )
        policy = RetryOncePolicy()
        runner = _make_runner(
            home=home,
            eval_config=eval_config,
            executor=executor,
            run_paths=run_paths,
            expects=(_failing_expect(),),
            retry_policy=policy,
        )

        outcome = runner.run(untagged_spec)

        assert outcome.status == "FAIL"
        assert executor.spawn_count == 1, (
            f"NFR-REL2 violated for untagged spec: spawn={executor.spawn_count}"
        )
        assert MCP_SERVER_FLAKY_ARTIFACT not in outcome.artifacts

    def test_runner_retries_once_on_mcp_flaky_failure(
        self, tagged_spec, home, eval_config, run_paths
    ):
        """A tagged spec that fails on first attempt retries exactly
        once. The persistent-failure path yields ``FAIL`` with the
        ``mcp_server_flaky`` artifact attached."""

        executor = ScriptedExecutor(
            script=[
                ObservedRun(exit_code=1, stdout="flake1", stderr="", duration_sec=0.1),
                ObservedRun(exit_code=1, stdout="flake2", stderr="", duration_sec=0.1),
            ]
        )
        policy = RetryOncePolicy()

        def _factory() -> FakeHome:
            # Reuse the original ``home`` instance — its setup() is
            # idempotent across calls.
            return home

        runner = _make_runner(
            home=home,
            eval_config=eval_config,
            executor=executor,
            run_paths=run_paths,
            expects=(_failing_expect(),),
            retry_policy=policy,
            home_factory=_factory,
        )

        outcome = runner.run(tagged_spec)

        assert outcome.status == "FAIL"
        assert executor.spawn_count == 2, (
            f"Expected exactly one retry; observed {executor.spawn_count} spawns"
        )
        assert executor.inject_count == 2
        assert executor.observe_count == 2
        assert outcome.artifacts.get(MCP_SERVER_FLAKY_ARTIFACT) == "true"

    def test_retry_recovery_returns_pass_with_artifact(
        self, tagged_spec, home, eval_config, run_paths
    ):
        """When the retry recovers (PASS on second attempt) the final
        outcome is PASS but the artifact is still attached so the
        Reporter can surface the flake-and-recover signal."""

        executor = ScriptedExecutor(
            script=[
                ObservedRun(exit_code=1, stdout="flake", stderr="", duration_sec=0.1),
                ObservedRun(exit_code=0, stdout="ok", stderr="", duration_sec=0.1),
            ]
        )
        policy = RetryOncePolicy()
        runner = _make_runner(
            home=home,
            eval_config=eval_config,
            executor=executor,
            run_paths=run_paths,
            expects=(_conditional_expect(home),),
            retry_policy=policy,
            home_factory=lambda: home,
        )

        outcome = runner.run(tagged_spec)

        assert outcome.status == "PASS", (
            f"Expected retry to recover; got {outcome.status}"
        )
        assert executor.spawn_count == 2
        assert executor.observe_count == 2
        # Artifact records the flake even on a recovered run.
        assert outcome.artifacts.get(MCP_SERVER_FLAKY_ARTIFACT) == "true"

    def test_retry_skips_when_first_attempt_passes(
        self, tagged_spec, home, eval_config, run_paths
    ):
        """A PASS on first attempt does not trigger a retry — the
        policy is opt-in via the spec, gated on flaky status."""

        executor = ScriptedExecutor(
            script=[ObservedRun(exit_code=0, stdout="ok", stderr="", duration_sec=0.1)]
        )
        policy = RetryOncePolicy()
        runner = _make_runner(
            home=home,
            eval_config=eval_config,
            executor=executor,
            run_paths=run_paths,
            expects=(_passing_expect(),),
            retry_policy=policy,
            home_factory=lambda: home,
        )

        outcome = runner.run(tagged_spec)

        assert outcome.status == "PASS"
        assert executor.spawn_count == 1, (
            f"Unexpected retry on PASS first attempt: spawn={executor.spawn_count}"
        )
        assert MCP_SERVER_FLAKY_ARTIFACT not in outcome.artifacts


# ---------------------------------------------------------------------------
# Compatibility — wiring the policy must not relax NFR-REL2
# ---------------------------------------------------------------------------


class TestPolicyCompatibility:
    """The R3-mit policy is orthogonal to the strict ``retry_count``
    rejection. Both invariants must coexist."""

    def test_policy_does_not_unlock_nonzero_retry_count(
        self, home, eval_config, run_paths
    ):
        """Wiring a policy still rejects ``retry_count=1``."""

        executor = ScriptedExecutor(
            script=[ObservedRun(exit_code=0, stdout="", stderr="", duration_sec=0.0)]
        )
        policy = RetryOncePolicy()
        with pytest.raises(ValueError) as excinfo:
            EvalRunner(
                home=home,  # type: ignore[arg-type]
                config=eval_config,
                executor=executor,
                run_dir=run_paths["run_dir"],
                artifacts_dir=run_paths["artifacts_dir"],
                stdout_path=run_paths["stdout_path"],
                stderr_path=run_paths["stderr_path"],
                transcript_path=run_paths["transcript_path"],
                expect_callables=(),
                deploy_hooks=lambda _p: None,
                retry_count=1,
                retry_policy=policy,
            )
        assert "NFR-REL2" in str(excinfo.value)

    def test_runner_accepts_policy_without_home_factory(
        self, tagged_spec, home, eval_config, run_paths
    ):
        """``home_factory`` is optional — a test home whose setup() is
        re-entrant works without a factory."""

        executor = ScriptedExecutor(
            script=[
                ObservedRun(exit_code=1, stdout="flake1", stderr="", duration_sec=0.1),
                ObservedRun(exit_code=1, stdout="flake2", stderr="", duration_sec=0.1),
            ]
        )
        policy = RetryOncePolicy()
        runner = _make_runner(
            home=home,
            eval_config=eval_config,
            executor=executor,
            run_paths=run_paths,
            expects=(_failing_expect(),),
            retry_policy=policy,
            home_factory=None,
        )

        outcome = runner.run(tagged_spec)

        assert outcome.status == "FAIL"
        assert executor.spawn_count == 2
        assert outcome.artifacts.get(MCP_SERVER_FLAKY_ARTIFACT) == "true"
