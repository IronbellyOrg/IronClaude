"""Loop-guard fence-post for the ``sc:pr-submit`` core (INV-001) — the P0 module.

The round counter increments by EXACTLY 1 at the single FSM transition
``S5_AWAITING_REREVIEW → S2_CLASSIFY`` when ``review_observed AND
sha_attributed_to_our_push``, and increments nowhere else; it is monotonic (a
vanished re-review does NOT decrement); the HALT gate uses ``round_counter >=
max_rounds`` (INV-5, ``>=`` not ``>``); the user-facing label is ``round_counter +
1``; and ``max_rounds=N`` yields exactly N pushes. The off-by-one here is the spec's
named P0 defect (T-626-OFF-BY-ONE).

NFR-6 / AC-9 core purity (T-N50): ZERO shell or version-control command tokens —
the counter is pure arithmetic over already-observed events.
"""

from __future__ import annotations

from dataclasses import dataclass

DEFAULT_MAX_ROUNDS = 2
HARD_CAP_MAX_ROUNDS = 5


def should_halt(round_counter: int, max_rounds: int) -> bool:
    """The round-budget HALT gate: ``round_counter >= max_rounds`` (INV-5, ``>=`` not ``>``).

    Evaluated BEFORE opening each fix cycle. At ``max_rounds=2`` the gate fires once
    the counter reaches 2 — so exactly 2 cycles (and exactly 2 pushes) occur, never 3
    (the canonical off-by-one, T-626).
    """
    return round_counter >= max_rounds


def user_label(round_counter: int) -> int:
    """The user-facing round label = ``round_counter + 1`` (first cycle reads as "round 1")."""
    return round_counter + 1


@dataclass
class RoundCounter:
    """A monotonic round counter with the single INV-001 increment edge.

    Call :meth:`on_rereview` ONLY at the ``S5_AWAITING_REREVIEW → S2_CLASSIFY`` edge;
    it increments by exactly 1 iff the re-review was observed AND attributed to our
    push. No other method increments it, and it never decrements.
    """

    value: int = 0
    max_rounds: int = DEFAULT_MAX_ROUNDS

    def on_rereview(
        self, *, review_observed: bool, sha_attributed_to_our_push: bool
    ) -> bool:
        """Tick the counter iff both conditions hold (the SINGLE increment site).

        Returns True if the counter incremented this call. A re-review that is not
        attributed to our push does NOT increment (it is not a completed cycle).
        """
        if review_observed and sha_attributed_to_our_push:
            self.value += 1
            return True
        return False

    def vanished_rereview(self) -> None:
        """A previously-counted re-review vanished — the counter does NOT decrement (INV-4).

        Monotonicity is irrevocable: this is intentionally a no-op (T-VANISHED-MONO).
        """
        # Intentionally no decrement — the counter is monotonic.
        return None

    def should_halt(self) -> bool:
        """Whether the round budget is exhausted (``value >= max_rounds``)."""
        return should_halt(self.value, self.max_rounds)

    @property
    def label(self) -> int:
        """The user-facing label (``value + 1``)."""
        return user_label(self.value)
