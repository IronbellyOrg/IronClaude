"""T04.08 -- ``passthrough`` recipe (COMP-020 / R-092 / D-0074).

Raw-mode shape: returns the worker body unchanged. This is the recipe
selected by ``amalgamation_mode == "raw"`` -- callers that opt out of
per-worker shape normalization route every worker through this recipe
so the dispatcher surface (atomic write to ``final_path`` + meta
sidecar) still fires uniformly while the body bytes stay byte-identical
to the transport-supplied raw payload.

Byte-identity contract (AC-011 / FR-LENSREG.NS / §3.3)
======================================================

The Wave-2 dispatcher persists :attr:`NormalizedResult.text` to
``final_path`` via ``str.encode("utf-8")`` (see
:func:`superclaude.cli.swarm.normalize._atomic_write_text`). The
transport-supplied ``raw_output`` is itself a ``str`` materialized via
``Path.read_text(encoding="utf-8")`` or already in-memory on
``WorkerResult.body`` -- always UTF-8 round-trippable at the recipe
boundary. Returning ``raw_output`` verbatim therefore preserves the
byte-for-byte encoding the dispatcher subsequently writes.

The recipe MUST NOT:

* Apply any transform (whitespace trim, line-ending normalization,
  case folding, alias mapping). Even trivial transforms break the
  raw-mode contract callers opt into.
* Reorder, dedup, score, or filter any portion of the body. AC-011
  forbids judging transforms across every recipe in REGISTRY; this
  recipe is the most-loaded path because every raw-mode run touches
  it, so the boundary is asserted directly inline (T04.14 also pins
  it).
* Strip leading/trailing whitespace or rewrite frontmatter. Sibling
  recipes (:mod:`bare_review_v1`, :mod:`verdict_only_v1`) do that
  selectively because they emit a canonical shape; the passthrough's
  whole purpose is to skip canonicalization.

Salvage semantics
=================

``salvaged`` is always ``False``: passthrough does not recover
structure from a parse_error body (it cannot, because it does not
inspect the body). The Wave-2 dispatcher's §7.4 salvage gate
(:func:`superclaude.cli.swarm.normalize._normalize_one`) only promotes
``parse_error -> success`` when the recipe sets ``salvaged=True``, so
raw-mode workers retain the transport's terminal classification --
which is the documented raw-mode contract (callers see exactly what
the transport returned).

Args contract
=============

The recipe accepts (and ignores) the standard recipe args dict
forwarded by :func:`superclaude.cli.swarm.normalize.normalize_wave2`.
No fields are read; the dict is accepted positionally only to satisfy
the :class:`Recipe` Protocol signature.

Empty body handling
===================

An empty / pure-whitespace raw body returns
``NormalizedResult(text=raw_output, salvaged=False, error=None)``. The
recipe does not classify "empty" as a parse failure -- raw mode is the
escape hatch where callers explicitly accept whatever the transport
emitted. The dispatcher will write a 0-byte ``final_path`` for an
empty string, which matches the byte-identity contract.
"""

from __future__ import annotations

from typing import Any

from superclaude.cli.swarm.recipes import NormalizedResult


__all__ = ["Passthrough"]


class Passthrough:
    """``passthrough`` -- raw-mode recipe; returns body unchanged.

    Implements :class:`superclaude.cli.swarm.recipes.Recipe` via the
    structural Protocol (no inheritance). Used by
    ``amalgamation_mode == "raw"`` and as the safe default when a lens
    declares no normalization.

    The recipe is intentionally trivial: every method call returns the
    input verbatim. AC-011 forbids any per-worker judging transform,
    and the raw-mode contract additionally forbids any shape transform
    -- the passthrough is therefore the only recipe where the absence
    of logic is itself the specification.
    """

    def normalize(
        self, raw_output: str, args: dict[str, Any]
    ) -> NormalizedResult:
        del args
        return NormalizedResult(text=raw_output, salvaged=False, error=None)
