"""Tests for sprint provider-exhaustion recovery policy."""

from __future__ import annotations

import pytest

from superclaude.cli.sprint.monitor import ProviderFailure
from superclaude.cli.sprint.recovery_policy import Action, SessionResetPolicy


@pytest.mark.unit
@pytest.mark.parametrize(
    ("signal", "attempt", "expected"),
    [
        (ProviderFailure.ALL_ACCOUNT_COOLDOWN, 0, Action.HALT_MODEL_SWITCH),
        (ProviderFailure.ALL_ACCOUNT_COOLDOWN, 5, Action.HALT_MODEL_SWITCH),
        (ProviderFailure.SINGLE_ACCOUNT_LIMIT, 0, Action.RETRY_NEW_SESSION),
        (ProviderFailure.SINGLE_ACCOUNT_LIMIT, 7, Action.RETRY_NEW_SESSION),
        (ProviderFailure.SINGLE_ACCOUNT_LIMIT, 8, Action.HALT_MODEL_SWITCH),
        (ProviderFailure.OPERATION_TIMEOUT, 0, Action.CONTINUE),
        (ProviderFailure.NONE, 0, Action.CONTINUE),
    ],
)
def test_session_reset_policy_decide_truth_table(signal, attempt, expected):
    policy = SessionResetPolicy(max_session_resets=8)

    assert policy.decide(signal, attempt) is expected
