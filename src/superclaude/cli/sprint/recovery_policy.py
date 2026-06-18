"""Session-reset recovery policy for provider/account-exhaustion (429) handling.

A 429 means ONE routed CLIProxyAPI account hit its rate-limit window; the pool
holds roughly eight accounts, and every sprint subprocess is launched with
``--no-session-persistence`` — so a fresh subprocess is a new session is a new
routing decision is a chance at a *different* account. Recovery is therefore
RE-ROUTING (re-spawn, or switch the model alias), NEVER waiting.

``SessionResetPolicy.decide`` is the pure decision the executor's re-spawn loop
consults each attempt. The loop owns the side effects (spawn, latch); the policy
is side-effect-free.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from .monitor import ProviderFailure


class Action(Enum):
    """The re-route action the executor loop takes for one attempt's signal."""

    RETRY_NEW_SESSION = "retry_new_session"  # re-spawn (rotate to another account)
    HALT_MODEL_SWITCH = "halt_model_switch"  # stop; suggest a model-alias switch
    FAIL_TASK = "fail_task"  # reserved — not returned by decide()
    CONTINUE = "continue"  # not a provider failure; fall through to the ladder


@dataclass
class SessionResetPolicy:
    """Per-run, shared-across-workers state for the bounded re-spawn loop.

    A single instance is constructed once per phase and threaded to every K>1
    worker (and the K=1 path) so the sprint-wide halt ``_latch_tripped`` and the
    reset budget are shared. The latch is checked AND tripped UNDER the executor's
    ``lock`` (the policy does NOT own a lock); ``decide`` itself is pure.

    Fields:
        max_session_resets: per-phase SHARED re-spawn cap (≈ pool size; default 8).
            The budget is consumed from the single ``_exhaustion_attempts`` counter
            shared across all of a phase's workers — NOT a fresh cap per task — which
            is what bounds a K>1 storm to ``cap + (K-1)``.
        _exhaustion_attempts: shared per-phase budget counter (claimed under lock).
        _latch_tripped: sprint-wide halt latch, lock-guarded by the caller.
    """

    max_session_resets: int = 8  # ≈ account-pool size
    _exhaustion_attempts: int = 0
    _latch_tripped: bool = False

    def decide(self, signal: ProviderFailure, attempt: int) -> Action:
        """Pure decision for one re-spawn attempt's provider-failure signal.

        Truth table (spec §4 Layer 3):
        - ``ALL_ACCOUNT_COOLDOWN`` → ``HALT_MODEL_SWITCH`` on ANY attempt (incl.
          the first): every account is already cooling down, so re-spawning is
          futile — only a model switch helps (the fast path).
        - ``SINGLE_ACCOUNT_LIMIT`` → ``RETRY_NEW_SESSION`` while
          ``attempt < max_session_resets`` (rotate to another account), else
          ``HALT_MODEL_SWITCH`` (budget exhausted — halt at ``attempt == cap``).
        - ``NONE`` / ``OPERATION_TIMEOUT`` → ``CONTINUE`` (not account exhaustion;
          fall through to the executor's normal status ladder).

        No side effects: does NOT touch the latch or any counter, and never
        returns ``FAIL_TASK`` (reserved).
        """
        if signal is ProviderFailure.ALL_ACCOUNT_COOLDOWN:
            return Action.HALT_MODEL_SWITCH
        if signal is ProviderFailure.SINGLE_ACCOUNT_LIMIT:
            if attempt < self.max_session_resets:
                return Action.RETRY_NEW_SESSION
            return Action.HALT_MODEL_SWITCH
        return Action.CONTINUE
