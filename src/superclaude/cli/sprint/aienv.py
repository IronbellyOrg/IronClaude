"""``~/.aienv`` model-alias reader for provider-exhaustion re-routing (P5).

When a sprint subprocess halts on an *all-account cooldown* (every account for
ONE model is cooling down via the provider), re-spawning is futile — the only
re-route that helps is a *model switch*: point the resume at a DIFFERENT model
alias whose accounts are not exhausted. This module reads the operator's
already-exported model aliases and suggests the next distinct one.

Reader design (OQ-1, operator-DECIDED: option A — os.environ reader)
-------------------------------------------------------------------
The aliases live in ``~/.aienv`` as ``export NAME=value`` lines, but that file
is a *bash* file ``source``d only by the ``scripts/ic`` wrapper; no Python in
the repo parses it as text. The canonical Python convention
(:mod:`superclaude.cli.swarm.config`) instead reads the *already-exported*
``os.environ`` — and the sprint child inherits those exports via
``os.environ.copy()`` in ``process.py``. This module follows that convention:
it reads the three Anthropic model slots and the numbered proxy slots straight
from the environment (or an injected mapping for tests, so a unit test never
touches the real ``~/.aienv``).

Rejected alternative (option B — documented, NOT shipped): a ``~/.aienv``
file-parser that regexes ``export NAME=value`` lines. It would match the spec's
literal "parse ~/.aienv" wording and work even when the vars are not exported
into the current process, but it is new machinery with no prior art in the repo
and duplicates the bash ``source`` semantics already provided by ``scripts/ic``.
Recorded here for provenance only; the os.environ reader is the shipped design.
"""

from __future__ import annotations

import os
from typing import Mapping, Optional

from superclaude.cli.swarm.config import T2_MODEL_ENV_PREFIX, T2_MODEL_MAX_SLOTS

__all__ = ["suggest_alternate_model"]

# The three Anthropic model slots set by ``scripts/ic`` (ic:61-63, exported at
# ic:98) and read by Claude Code. Ordered OPUS → SONNET → HAIKU (most → least
# capable) so an exhausted ``opus`` rotates down to ``sonnet`` first. The short
# alias each slot maps to is the ``--model`` value an operator would pass.
_ANTHROPIC_SLOTS: tuple[tuple[str, str], ...] = (
    ("ANTHROPIC_DEFAULT_OPUS_MODEL", "opus"),
    ("ANTHROPIC_DEFAULT_SONNET_MODEL", "sonnet"),
    ("ANTHROPIC_DEFAULT_HAIKU_MODEL", "haiku"),
)


def _load_aliases(env: Optional[Mapping[str, str]] = None) -> dict[str, str]:
    """Read the available model aliases from the environment in priority order.

    Mirrors :meth:`SwarmConfig._collect_t2_models` (os.environ reader, option A):
    enumerates the three Anthropic slots (``ANTHROPIC_DEFAULT_{OPUS,SONNET,
    HAIKU}_MODEL``) then the numbered proxy slots ``T2Model01``..``T2Model0N``
    (reusing :data:`T2_MODEL_ENV_PREFIX` / :data:`T2_MODEL_MAX_SLOTS` from
    ``swarm.config`` to avoid drift). Empty / unset slots are skipped so the
    result is dense and insertion-ordered (most-capable / lowest-index first).

    Returns an ordered mapping of ``alias -> resolved_model_id`` where the alias
    is the short ``--model`` token (``opus``/``sonnet``/``haiku`` for the
    Anthropic slots, the slot name itself — e.g. ``T2Model01`` — for the proxy
    slots) and the value is the resolved model id exported for that slot.

    ``env`` defaults to ``os.environ``; pass an explicit mapping in tests to
    keep the read deterministic and away from the real ``~/.aienv``.
    """
    env_map: Mapping[str, str] = env if env is not None else os.environ
    aliases: dict[str, str] = {}
    for slot_var, alias in _ANTHROPIC_SLOTS:
        value = env_map.get(slot_var)
        if value:
            aliases[alias] = value
    for index in range(1, T2_MODEL_MAX_SLOTS + 1):
        slot_name = f"{T2_MODEL_ENV_PREFIX}{index}"
        value = env_map.get(slot_name)
        if value:
            aliases[slot_name] = value
    return aliases


def suggest_alternate_model(
    failed_model_or_alias: str,
    *,
    env: Optional[Mapping[str, str]] = None,
) -> str | None:
    """Suggest the next DISTINCT model alias to re-route to after exhaustion.

    The all-account-cooldown body embeds the *resolved* model id (e.g.
    ``claude-opus-4-8``); the halt UX needs an alternate ``--model`` token to put
    in the resume command. This maps the failed model — matched by its alias
    (``opus``, ``T2Model01``) OR by its resolved id (``claude-opus-4-8``) — to its
    position in the ordered alias set, then returns the next alias whose alias
    name AND resolved model both differ (so we never re-route to the identical
    model under a second name).

    Prefix-agnostic over the numbered slots: it walks whatever aliases
    :func:`_load_aliases` discovered, in priority order, so ``opus`` rotates to
    ``sonnet`` and ``T2Model01`` rotates to ``T2Model02``.

    Returns ``None`` (never a fabricated alias, edge case #7) when the failed
    model is unknown OR no distinct alternate exists. ``env`` is the injectable
    seam (defaults to ``os.environ``) so tests never read the real ``~/.aienv``.
    """
    items = list(_load_aliases(env).items())

    failed_idx: int | None = None
    for idx, (alias, resolved) in enumerate(items):
        if failed_model_or_alias in (alias, resolved):
            failed_idx = idx
            break
    if failed_idx is None:
        return None

    failed_alias, failed_resolved = items[failed_idx]
    for alias, resolved in items[failed_idx + 1 :]:
        if alias != failed_alias and resolved != failed_resolved:
            return alias
    return None
