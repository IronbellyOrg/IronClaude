"""T02.02 -- COMP-006 Wave 0 preflight orchestration.

``run_preflight`` is the single Wave-0 entrypoint. It accepts an
untrusted JobSpec (dict or :class:`JobSpec`), runs the four Wave-0
phases in order, and returns a :class:`PreflightResult` carrying the
freshly-stamped :class:`Manifest` + :class:`SwarmState`, or raises a
:class:`PreflightError` whose ``failures`` list enumerates every
failing rule for the structured failure contract.

Wave 0 phases (COMP-006 -- roadmap row R-031):

    1. Schema validation (COMP-005, T02.01) -- DM-001 JSON Schema +
       §11.5 cross-field rule. Fatal on first batch: downstream phases
       touch nested dicts the schema rejected, so we abort immediately
       once any schema failure is detected.
    2. Lens resolution (COMP-022 -- LENSES dict, T02.14) +
       materialization (FR-020 lens-driven defaults expansion,
       T02.04). T02.02 lands the call site; the registry-backed
       resolver and the full default expansion land in their dedicated
       tasks. The resolver here looks up the lens in
       ``superclaude.cli.swarm.lenses.LENSES`` if present and raises
       ``KeyError`` otherwise; tests inject a stub registry via
       :func:`set_lens_resolver`.
    3. Guards: §11.5 injection-guard re-assertion (T02.07 centralises
       this across the lens / JSON-Schema / custom-prompt-dir paths),
       IMM-4 empty-target guard (T02.13 fills in the full STOP /
       failure-contract semantics), INV-005 worker-count-vs-pool
       guard (T02.10 fills in the OQ-007 resolution), INV-007 empty
       pool failure contract (T02.11 fills in the structured
       ``failed`` / ``env-missing`` emission).
    4. Manifest emit + SwarmState init -- :class:`Manifest` carries
       the resolved-lens snapshot (INV-001 / INV-016) and the
       :class:`PreflightSummary` triple
       (target_checksum, workers_requested, transport_kind);
       :class:`SwarmState` is stamped at ``state="preflight_ok"`` per
       the DM-014 enum. The state-file write itself
       (write-to-tmp + os.replace) is the COMP-011 state module's job
       (M3); T02.02 only stamps the in-memory record.

Scope split with downstream T02.* tasks:

    * T02.04 (FR-020 lens-driven defaults expansion) replaces
      :func:`materialize_lens_defaults` with the full ten-field expansion.
    * T02.05 (FR-021 custom-prompt-dir reader) and T02.07 (§11.5 guard
      across all three paths) wire the central guard helper through the
      escape-hatch + JSON-schema paths.
    * T02.10 (INV-005) fills in the OQ-007 resolution (warn-with-defaults
      vs STOP) in :func:`check_pool_size`.
    * T02.11 (INV-007) replaces :func:`check_empty_pool` with the full
      structured ``failed``/``env-missing`` contract emission.
    * T02.13 (IMM-4) hardens :func:`guard_empty_target` with the
      truncation-aware <50-non-whitespace-byte check and the no-dispatch
      guarantee.
    * T02.22 (FR-024 ``--auto-inject-guard``) wraps the custom-prompt-dir
      reader so missing §11.5 substrings can be auto-prepended on
      migration paths.

Manifest persistence: ``run_preflight`` returns the Manifest object;
when an ``output_dir`` is provided it also writes ``manifest.json``
atomically (write-to-tmp + ``os.replace``) so the M6 resume path can
read it back byte-identically (INV-016).
"""

from __future__ import annotations

import dataclasses
import hashlib
import logging
import os
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Iterable, Literal, Optional

from superclaude.cli.swarm import schema
from superclaude.cli.swarm.models import (
    CallerMetadata,
    JobSpec,
    LensEntry,
    Manifest,
    NormalizationSpec,
    PreflightSummary,
    PromptSpec,
    ResolvedLensEntry,
    SwarmState,
    TransportSpec,
    WorkerSpec,
    from_dict,
    from_json,
    to_dict,
    to_json,
)
from superclaude.cli.swarm.schema import (
    CANONICAL_INJECTION_GUARD_SENTENCE,
    SchemaValidationError,
    contains_required_substring,
)
from superclaude.cli.swarm.state import confine_path

# ---------------------------------------------------------------------------
# Constants -- rule identifiers and IMM-4 byte floor.
#
# Each rule identifier is a stable string. Tests assert on the identifier
# (not the human-facing message) so message phrasing can evolve without
# breaking the suite. The identifiers mirror the schema layer's RULE_*
# constants so a caller printing a mixed-source failure list sees a
# uniform shape.
# ---------------------------------------------------------------------------


RULE_TARGET_TOO_SMALL: str = "imm4.target_too_small"
"""IMM-4 -- target with <50 non-whitespace bytes after truncation."""

RULE_TARGET_UNREADABLE: str = "target.path.unreadable"
"""``target.path`` could not be opened for read."""

RULE_WORKERS_EXCEED_POOL: str = "inv005.workers_exceed_pool"
"""INV-005 -- ``workers.count`` exceeds configured model-pool size."""

RULE_EMPTY_POOL: str = "inv007.env_missing"
"""INV-007 -- configured model pool is empty (env-missing failure)."""

RULE_INJECTION_GUARD: str = "injection_guard.required_substring"
"""§11.5 -- required substring missing on a prompt-input path."""

RULE_UNKNOWN_LENS: str = "lens.unknown"
"""Lens name not registered in LENSES."""

RULE_CUSTOM_PROMPT_DIR_MISSING: str = "custom_prompt_dir.missing"
"""FR-021 -- custom prompt directory or a required file inside it is missing."""

RULE_CUSTOM_PROMPT_DIR_META_INVALID: str = "custom_prompt_dir.meta_invalid"
"""FR-021 -- ``meta.yaml`` cannot be parsed or is not a top-level mapping."""


MIN_TARGET_NON_WHITESPACE_BYTES: int = 50
"""IMM-4 byte floor -- mirrors :class:`Truncation` ``byte_floor`` default."""


PoolPolicy = Literal["warn", "stop"]
"""OQ-007 pool-overage policy selector.

* ``"warn"`` -- V1 ``warn-on-exceed-with-defaults``: detection logs a
  warning and the caller clamps ``workers.count`` down to the pool
  size; no :class:`PreflightError` is raised. This is the project
  default per the M1-exit OQ-007 resolution recorded in
  ``docs/swarm/oq-resolutions.md``.
* ``"stop"`` -- V2 ``STOP-before-dispatch``: detection emits a
  :class:`PreflightFailure` carrying :data:`RULE_WORKERS_EXCEED_POOL`
  and aborts Wave 0. Selectable per-call for strict callers
  (CI gates, integration smoke tests).
"""


DEFAULT_POOL_POLICY: PoolPolicy = "warn"
"""OQ-007 V1 -- ``warn-on-exceed-with-defaults`` is the project default.

The roadmap row (``.dev/releases/Current/MultiModelSwarm/roadmap.md``
line 108) marks ``warn`` as the architect-recommended resolution; the
M1-exit decision adopts it. Callers that want strict pre-dispatch
abort pass ``pool_policy="stop"`` to :func:`run_preflight` /
``policy="stop"`` to :func:`check_pool_size`.
"""


_logger = logging.getLogger(__name__)
"""Module logger -- carries the OQ-007 warn-mode clamp message.

The ``warn-with-defaults`` branch logs at WARNING level so operators
see the clamp in stderr (the default Click handler) without forcing
preflight to raise. Tests assert against
:meth:`pytest.LogCaptureFixture` records rather than stderr capture
so the assertion stays robust against logging-config changes.
"""


# ---------------------------------------------------------------------------
# Diagnostics -- the structured failure contract.
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class PreflightFailure:
    """One structured rejection reason from a Wave-0 guard.

    Fields:
        rule    -- a stable identifier from the ``RULE_*`` constants
                   above (or a :class:`SchemaValidationFailure.rule`
                   propagated verbatim when schema validation failed).
                   Tests assert on this identifier.
        path    -- dotted path to the offending field
                   (e.g. ``"target.path"``, ``"workers.count"``). Empty
                   for whole-document rejections.
        message -- human-readable summary, suitable for logging.
        reason  -- short token suitable for the M5 ResultContract
                   ``reason`` field (``"target-too-small"``,
                   ``"env-missing"``, ``"lens-unknown"``,
                   ``"schema-invalid"``, etc.). Downstream tasks
                   (T02.10 / T02.11) feed this token into the
                   ``failed`` contract emission per OQ-007 / OQ-008.
    """

    rule: str
    path: str
    message: str
    reason: str = ""


class PreflightError(Exception):
    """Raised by :func:`run_preflight` when one or more guards fail.

    Carries the full :class:`PreflightFailure` list so the executor /
    skill driver can render every failing rule in one pass and assemble
    the structured ``failed`` ResultContract without re-running
    preflight to discover later failures.

    ``env_missing_contract_path`` (T02.11 / INV-007 / OQ-008) carries
    the absolute path of the ``return-contract.yaml`` written by
    :func:`emit_env_missing_contract` when an empty configured model
    pool triggered the env-missing failure branch and ``job.output.dir``
    was creatable. ``None`` when the contract was not emitted (no empty
    pool, or output dir not creatable -- the OQ-008 bare-abort branch).
    """

    def __init__(
        self,
        failures: list[PreflightFailure],
        *,
        env_missing_contract_path: Optional[str] = None,
    ) -> None:
        if not failures:
            raise ValueError(
                "PreflightError requires at least one failure"
            )
        self.failures: list[PreflightFailure] = list(failures)
        self.env_missing_contract_path: Optional[str] = env_missing_contract_path
        rules = ", ".join(f.rule for f in failures)
        super().__init__(
            f"Preflight failed {len(failures)} rule(s): {rules}"
        )


@dataclass
class PreflightResult:
    """Successful Wave-0 outcome.

    Carries the :class:`Manifest` (INV-001 / INV-016 source-of-truth
    anchor) and the :class:`SwarmState` at ``preflight_ok``, plus the
    optional on-disk ``manifest_path`` when :func:`run_preflight` was
    given an ``output_dir`` and wrote the manifest atomically.

    ``caller_metadata`` carries the DM-020 :class:`CallerMetadata`
    resolved at Wave 0 per the OQ-009 precedence (lens defaults +
    optional caller override). The Manifest's
    :class:`ResolvedLensEntry` snapshot records the lens-side
    contribution (``suspect`` / ``tier``) so the resolved metadata is
    recoverable from ``manifest.json`` alone (INV-001 / INV-016); the
    executor copies this value verbatim onto
    :class:`ResultContract.caller_metadata` at reduce time (M5).
    """

    manifest: Manifest
    state: SwarmState
    manifest_path: Optional[str] = None
    caller_metadata: CallerMetadata = dataclasses.field(
        default_factory=lambda: CallerMetadata()
    )


# ---------------------------------------------------------------------------
# Lens resolver -- pluggable so T02.04 / T02.14 can swap the registry in
# without touching :func:`run_preflight`. Tests inject stub resolvers via
# :func:`set_lens_resolver`.
# ---------------------------------------------------------------------------


_LensResolver = Callable[[str], LensEntry]


def _default_lens_resolver(name: str) -> LensEntry:
    """Look ``name`` up in ``superclaude.cli.swarm.lenses.LENSES``.

    T02.14 populates the ``LENSES`` dict; until then this resolver
    raises :class:`KeyError` for every input so :func:`run_preflight`
    surfaces ``RULE_UNKNOWN_LENS``. Tests bypass this with
    :func:`set_lens_resolver`.
    """
    try:
        from superclaude.cli.swarm import lenses as _lenses  # noqa: PLC0415
    except ImportError as exc:
        raise KeyError(name) from exc
    registry = getattr(_lenses, "LENSES", None)
    if not isinstance(registry, dict) or name not in registry:
        raise KeyError(name)
    entry = registry[name]
    if not isinstance(entry, LensEntry):
        raise KeyError(name)
    return entry


_lens_resolver: _LensResolver = _default_lens_resolver


def set_lens_resolver(resolver: Optional[_LensResolver]) -> _LensResolver:
    """Install a custom lens resolver; returns the previous resolver.

    Tests use this to inject a stub registry without touching the
    package-level ``LENSES`` import path. Pass ``None`` to restore the
    default.
    """
    global _lens_resolver
    previous = _lens_resolver
    _lens_resolver = resolver if resolver is not None else _default_lens_resolver
    return previous


def resolve_lens(name: str) -> LensEntry:
    """Resolve a lens ``name`` to its :class:`LensEntry`.

    Raises :class:`KeyError` when the lens is unknown -- caller wraps
    that in a :class:`PreflightFailure` with :data:`RULE_UNKNOWN_LENS`.
    The default resolver consults ``superclaude.cli.swarm.lenses.LENSES``;
    tests override via :func:`set_lens_resolver`.
    """
    return _lens_resolver(name)


def materialize_lens_defaults(
    job: JobSpec, lens_entry: LensEntry
) -> ResolvedLensEntry:
    """Capture the resolved-lens snapshot for the manifest.

    T02.02 scope: produce the immutable :class:`ResolvedLensEntry`
    snapshot via :meth:`ResolvedLensEntry.from_lens` so the manifest
    carries the lens binding INV-001 expects. T02.04 layers the full
    FR-020 spec-side expansion on top of this helper via
    :func:`expand_lens_defaults`, which mutates the JobSpec to populate
    every §4.2 field-default from the LensEntry before delegating to
    this snapshot factory.
    """
    return ResolvedLensEntry.from_lens(lens_entry)


# ---------------------------------------------------------------------------
# DM-020 / OQ-009 -- CallerMetadata resolution
# ---------------------------------------------------------------------------


def resolve_caller_metadata(
    source: LensEntry | ResolvedLensEntry,
    *,
    override: Optional[CallerMetadata] = None,
) -> CallerMetadata:
    """T02.25 / DM-020 -- resolve :class:`CallerMetadata` per OQ-009.

    OQ-009 resolution (recorded in ``docs/swarm/oq-resolutions.md``):
    **caller-overridable**. ``source`` -- a :class:`LensEntry` (at
    lens-driven preflight) or its :class:`ResolvedLensEntry` snapshot
    (when stamping the contract at reduce time from
    ``manifest.resolved_lens_entry``) -- supplies the default values
    for ``suspect`` and ``tier``. When ``override`` is provided, its
    field values win field-by-field per the §4.2 / FR-LENS-004 rule
    "caller-supplied values override lens defaults".

    Precedence matrix:

        - ``override`` is ``None`` -- lens values are returned verbatim
          (``CallerMetadata(suspect=source.suspect, tier=source.tier)``).
        - ``override`` is supplied -- both fields are taken from
          ``override`` regardless of the lens values, because
          dataclass-field equality cannot distinguish a caller-supplied
          ``False`` from the dataclass default ``False`` (same for
          ``""``). Callers wanting a partial override should fetch the
          lens default first via this function with ``override=None``,
          patch the field they want to change, and call again.

    Args:
        source: the :class:`LensEntry` resolved at preflight, OR the
            :class:`ResolvedLensEntry` snapshot persisted on
            ``manifest.resolved_lens_entry``. Both expose ``suspect``
            and ``tier`` with identical semantics so the executor can
            call this helper at preflight time (against the LensEntry)
            and again at reduce time (against the manifest snapshot)
            without branching on the input type.
        override: optional caller-supplied :class:`CallerMetadata`.
            When ``None`` (the default), the lens-only branch returns
            the source's values. When supplied, the caller-overridable
            branch wins per OQ-009.

    Returns:
        A fresh :class:`CallerMetadata` instance. Never mutates either
        input -- callers can safely re-use the lens snapshot across
        multiple resolutions.

    Raises:
        TypeError: ``source`` is not a :class:`LensEntry` or
            :class:`ResolvedLensEntry`; ``override`` is not ``None`` or
            a :class:`CallerMetadata`.
    """
    if not isinstance(source, (LensEntry, ResolvedLensEntry)):
        raise TypeError(
            "resolve_caller_metadata expects a LensEntry or "
            f"ResolvedLensEntry source, got {type(source).__name__}"
        )
    if override is not None and not isinstance(override, CallerMetadata):
        raise TypeError(
            "resolve_caller_metadata override must be None or a "
            f"CallerMetadata, got {type(override).__name__}"
        )
    if override is not None:
        return CallerMetadata(suspect=override.suspect, tier=override.tier)
    return CallerMetadata(suspect=source.suspect, tier=source.tier)


# ---------------------------------------------------------------------------
# FR-020 -- Lens-driven defaults expansion (T02.04)
# ---------------------------------------------------------------------------


CANONICAL_FILENAME_TEMPLATE: str = "{lens}-{index:02d}-{model_slug}.md"
"""§4.2 canonical filename template applied when the lens-driven path is in use.

Matches :class:`OutputSpec` ``filename_template`` default verbatim; carried
as a module constant so :func:`expand_lens_defaults` can detect "caller
left the default in place" via equality rather than re-stringing the
template at every call site.
"""


def expand_lens_defaults(
    spec: JobSpec, registry: dict[str, LensEntry]
) -> ResolvedLensEntry:
    """FR-020 -- expand lens-driven defaults onto ``spec`` in place.

    Resolves ``spec.lens`` against ``registry`` and applies the §4.2
    field-default mapping (``merged-requirements.compressed.compressed.md``
    L337-L353). Caller-supplied values win: a field that already carries
    a non-empty / non-default value is preserved verbatim and the lens
    value is **not** copied over. Empty strings, ``None`` placeholders,
    and the dataclass numeric defaults that match the LensEntry baseline
    are treated as "caller did not override -- fall through to the lens".

    The function mutates ``spec`` and returns the immutable
    :class:`ResolvedLensEntry` snapshot via :func:`materialize_lens_defaults`;
    the snapshot is what the manifest persists for INV-001 / INV-016.

    The ten fields expanded onto the JobSpec (§4.2):

        1. ``prompt.system``                          ← ``lens.system_prompt_fragment``
        2. ``prompt.user_template``                   ← ``lens.user_template``
        3. ``normalization.recipe``                   ← ``lens.recipe_name``
        4. ``normalization.template_path``            ← ``lens.output_template_path``
        5. ``workers.count``                          ← ``lens.default_workers`` (overridable)
        6. ``target.truncation.line_cap``             ← ``lens.default_target_line_cap`` (overridable)
        7. ``output.filename_template``               ← canonical ``"{lens}-{index:02d}-{model_slug}.md"``
        8. ``output.lens_name``                       ← ``lens.name``
        9. ``recommended_next_command_template``      ← ``lens.recommended_next_command_template``
       10. (snapshot-only) ``suspect`` / ``tier``     ← ``lens.suspect`` / ``lens.tier``

    The snapshot-only items (suspect, tier) flow through
    :class:`ResolvedLensEntry` rather than a JobSpec field because
    JobSpec carries no ``caller_metadata`` block; the executor stamps
    them onto the :class:`ResultContract` at reduce time via
    :func:`resolve_caller_metadata` (T02.25 / DM-020), which honours
    the OQ-009 caller-overridable precedence.

    Args:
        spec: a :class:`JobSpec` instance. Mutated in place.
        registry: lens name → :class:`LensEntry`. Typically
            ``superclaude.cli.swarm.lenses.LENSES`` (T02.14) but tests
            inject a stub registry directly.

    Returns:
        :class:`ResolvedLensEntry` mirroring the resolved lens entry on
        all nine snapshot fields (DM-011); ready to embed in
        :class:`Manifest`.

    Raises:
        PreflightError: ``spec.lens`` is not registered in ``registry``;
            the failure carries :data:`RULE_UNKNOWN_LENS` so callers can
            assemble the structured failure contract uniformly with the
            other Wave-0 rejections.
    """
    if not isinstance(spec, JobSpec):
        raise TypeError(
            f"expand_lens_defaults expects a JobSpec, got {type(spec).__name__}"
        )
    if not isinstance(registry, dict):
        raise TypeError(
            "expand_lens_defaults expects a dict registry, got "
            f"{type(registry).__name__}"
        )

    name = spec.lens
    lens_entry = registry.get(name)
    if not isinstance(lens_entry, LensEntry):
        raise PreflightError(
            [
                PreflightFailure(
                    rule=RULE_UNKNOWN_LENS,
                    path="lens",
                    message=(
                        f"Unknown lens: {name!r}. Lens must be registered in "
                        "the LENSES registry (COMP-022 / T02.14)."
                    ),
                    reason="lens-unknown",
                )
            ]
        )

    # --- Prompt block (strings: empty = "fall through to lens") ----------
    if not spec.prompt.system:
        spec.prompt.system = lens_entry.system_prompt_fragment
    if not spec.prompt.user_template:
        spec.prompt.user_template = lens_entry.user_template

    # --- Normalization block --------------------------------------------
    if not spec.normalization.recipe:
        spec.normalization.recipe = lens_entry.recipe_name
    if not spec.normalization.template_path:
        spec.normalization.template_path = lens_entry.output_template_path

    # --- Workers (count overridable per §4.2) ---------------------------
    # The WorkerSpec dataclass default is 4 (the typical lens count); a
    # caller leaving the default in place AND the lens carrying a
    # different value gets the lens value. Callers that want an explicit
    # value matching the dataclass default can re-assert it after
    # expansion. count<=0 also falls through to the lens.
    if spec.workers.count <= 0 or spec.workers.count == 4:
        spec.workers.count = lens_entry.default_workers

    # --- Target truncation (line_cap overridable per §4.2) --------------
    if (
        spec.target.truncation.line_cap <= 0
        or spec.target.truncation.line_cap == 4000
    ):
        spec.target.truncation.line_cap = lens_entry.default_target_line_cap

    # --- Output block (filename_template + lens_name) --------------------
    if (
        not spec.output.filename_template
        or spec.output.filename_template == CANONICAL_FILENAME_TEMPLATE
    ):
        spec.output.filename_template = CANONICAL_FILENAME_TEMPLATE
    if not spec.output.lens_name:
        spec.output.lens_name = lens_entry.name

    # --- recommended_next_command_template -------------------------------
    if not spec.recommended_next_command_template:
        spec.recommended_next_command_template = (
            lens_entry.recommended_next_command_template
        )

    return materialize_lens_defaults(spec, lens_entry)


# ---------------------------------------------------------------------------
# FR-021 -- ``--custom-prompt-dir`` escape hatch (T02.05)
#
# When ``lens == 'custom'`` and ``custom_prompt_dir`` is set, preflight
# reads three files from the directory:
#
#     <dir>/system.txt   -- loaded as ``prompt.system`` (verbatim)
#     <dir>/user.txt     -- loaded as ``prompt.user_template`` (verbatim)
#     <dir>/meta.yaml    -- parsed as a YAML mapping; supplies template
#                            variables and any caller-side metadata
#
# The §11.5 substring check applies identically to the lens-driven and
# JSON-Schema-validated paths (closes INV-003 / INV-014). The reader
# returns the three values as a tuple; callers apply them onto a
# :class:`PromptSpec` (and the variables onto ``prompt.variables``)
# before manifest emit, so the three files round-trip into the Manifest
# snapshot via the normal preflight pipeline.
#
# The reader uses :func:`enforce_injection_guard` -- the same helper the
# lens-driven path uses -- so a missing §11.5 substring produces a
# byte-identical structured failure on both paths (INV-014 parity).
# T02.07 lifts that helper into a single central function called from
# all three prompt-input paths; until then, ``enforce_injection_guard``
# below is already the single source of truth for the substring check.
#
# T02.22 (FR-024 ``--auto-inject-guard``) wraps the reader so legacy
# callers can opt into auto-prepending the canonical §11.5 sentence on
# ``system.txt`` reads -- the migration path documented in §11.5 of the
# merged-requirements compressed spec.
# ---------------------------------------------------------------------------


_CUSTOM_PROMPT_DIR_FILES: tuple[str, str, str] = (
    "system.txt",
    "user.txt",
    "meta.yaml",
)
"""Three files the custom-prompt-dir reader expects under the supplied path.

Order matters: tests assert that the failure list reports missing files
in this order so a caller wiring the failures into the structured
``failed`` ResultContract sees a deterministic shape regardless of
filesystem traversal order.
"""


def auto_inject_guard(
    system: str,
    *,
    canonical_sentence: str = CANONICAL_INJECTION_GUARD_SENTENCE,
) -> str:
    """FR-024 -- prepend the canonical §11.5 sentence to ``system`` if missing.

    T02.22 backward-compatibility helper for the ``--auto-inject-guard``
    flag. When a legacy ``--custom-prompt-dir`` user's ``system.txt``
    lacks the §11.5 framing sentence, this helper prepends
    :data:`schema.CANONICAL_INJECTION_GUARD_SENTENCE` so the downstream
    :func:`enforce_injection_guard` substring check passes. The flag is
    explicitly **opt-in** (default ``False`` on
    :func:`read_custom_prompt_dir`) so absent-flag callers preserve the
    full §11.5 required-substring enforcement -- there is no silent
    bypass.

    Idempotent: when ``canonical_sentence`` already appears anywhere in
    ``system``, ``system`` is returned verbatim (no double-prepend on
    repeated calls or on already-compliant prompts).

    Args:
        system: the raw ``system.txt`` contents read by
            :func:`read_custom_prompt_dir` (or any caller that wants to
            opt into the same backward-compat path).
        canonical_sentence: the §11.5 sentence to prepend. Defaults to
            :data:`schema.CANONICAL_INJECTION_GUARD_SENTENCE`; exposed
            as a parameter so tests can pin a custom sentence without
            patching the module-level constant. Empty string disables
            the helper (returns ``system`` verbatim) so callers can
            pass through user-supplied overrides without a separate
            guard.

    Returns:
        ``system`` verbatim when the canonical sentence is already
        present (or when the sentence is empty); otherwise the
        canonical sentence followed by ``"\\n\\n"`` (single blank line
        separator preserves prompt readability when the original
        ``system.txt`` started with content) and the original
        ``system`` payload. When the original payload is empty, only
        the canonical sentence is returned (no trailing newline
        artefacts).

    Migration path (documented for legacy ``--custom-prompt-dir`` users):

        1. Add the canonical §11.5 sentence verbatim to the top of
           ``system.txt``. The sentence is exported from
           :data:`schema.CANONICAL_INJECTION_GUARD_SENTENCE` and is
           stable across spec_version 1.0.
        2. While migrating, pass ``--auto-inject-guard`` to
           ``superclaude swarm run`` so preflight prepends the sentence
           automatically and the §11.5 substring check passes.
        3. Once every legacy ``system.txt`` has been updated, drop the
           flag; default behavior preserves §11.5 enforcement with no
           silent bypass.

    Mutating the canonical sentence (or this helper) breaks the
    backward-compat invariant; the §11.5 substring rule lives at the
    schema layer (:func:`schema.contains_required_substring`) so a
    single source-of-truth predicate evaluates the substring check on
    every prompt-input path.
    """
    if not canonical_sentence:
        return system
    if canonical_sentence in system:
        return system
    if not system:
        return canonical_sentence
    separator = "\n\n" if not system.startswith("\n") else "\n"
    return f"{canonical_sentence}{separator}{system}"


# Module-private alias so :func:`read_custom_prompt_dir` can call the helper
# without colliding with its same-named keyword argument (shadowing inside
# the function body would otherwise force a getattr / globals() lookup).
_apply_auto_inject_guard = auto_inject_guard


def read_custom_prompt_dir(
    path: str | os.PathLike[str],
    *,
    required_substring: str = "",
    auto_inject_guard: bool = False,
) -> tuple[str, str, dict[str, Any]]:
    """FR-021 -- read the three-file custom prompt directory.

    Reads ``<path>/system.txt``, ``<path>/user.txt``, and
    ``<path>/meta.yaml`` and returns the trio
    ``(system, user_template, meta)``. ``system`` and ``user_template``
    are returned verbatim (no normalisation); ``meta`` is the parsed
    YAML mapping (empty file → ``{}``).

    Args:
        path: directory containing the three prompt files. Tests pass a
            ``tmp_path`` fixture; production callers pass the value of
            ``--custom-prompt-dir`` after the schema layer asserted
            ``lens == 'custom'`` (FR-021 cross-field rule).
        required_substring: §11.5 substring that must appear inside
            ``system.txt``. Defaults to ``""`` (guard disabled) so unit
            tests can read the directory without forcing every fixture
            through the guard; production callers pass
            ``job.target.injection_guard.required_substring`` so the
            check is byte-identical to the lens path
            (:func:`enforce_injection_guard`).
        auto_inject_guard: T02.22 / FR-024 backward-compat opt-in.
            When ``True``, the canonical §11.5 sentence is prepended to
            the ``system.txt`` contents via :func:`auto_inject_guard`
            **before** the substring check fires, so legacy custom
            prompt directories whose ``system.txt`` lacks §11.5 framing
            can migrate without a hard preflight failure. Defaults to
            ``False`` so the absent-flag path preserves the full §11.5
            substring enforcement (no silent bypass). Idempotent: when
            the canonical sentence is already present, the prepend is a
            no-op.

    Returns:
        ``(system, user_template, meta)`` -- two strings + a dict that
        round-trip onto a :class:`PromptSpec` via
        ``spec.prompt.system = system``,
        ``spec.prompt.user_template = user_template``,
        ``spec.prompt.variables = meta.get("variables", {})``. The full
        dict is returned (not just ``variables``) so callers preserve
        additional caller-side metadata for the Manifest snapshot
        without re-reading the file.

    Raises:
        PreflightError: the directory does not exist, one of the three
            files is missing or unreadable, ``meta.yaml`` is not a YAML
            mapping, or ``system.txt`` is missing
            ``required_substring``. ``failures`` carries every reason
            in one pass so the caller assembles one structured failure
            contract instead of looping (INV-014 parity with the lens
            path's batch reporting).
    """
    base = Path(path)
    failures: list[PreflightFailure] = []

    if not base.exists():
        raise PreflightError(
            [
                PreflightFailure(
                    rule=RULE_CUSTOM_PROMPT_DIR_MISSING,
                    path="custom_prompt_dir",
                    message=(
                        f"custom_prompt_dir does not exist: {str(base)!r}. "
                        "FR-021 requires a directory containing system.txt, "
                        "user.txt, and meta.yaml."
                    ),
                    reason="custom-prompt-dir-missing",
                )
            ]
        )
    if not base.is_dir():
        raise PreflightError(
            [
                PreflightFailure(
                    rule=RULE_CUSTOM_PROMPT_DIR_MISSING,
                    path="custom_prompt_dir",
                    message=(
                        f"custom_prompt_dir is not a directory: {str(base)!r}."
                    ),
                    reason="custom-prompt-dir-missing",
                )
            ]
        )

    contents: dict[str, str] = {}
    for filename in _CUSTOM_PROMPT_DIR_FILES:
        file_path = base / filename
        try:
            contents[filename] = file_path.read_text(encoding="utf-8")
        except FileNotFoundError:
            failures.append(
                PreflightFailure(
                    rule=RULE_CUSTOM_PROMPT_DIR_MISSING,
                    path=f"custom_prompt_dir/{filename}",
                    message=(
                        f"{filename} is missing under custom_prompt_dir "
                        f"({str(base)!r}). FR-021 requires all three files."
                    ),
                    reason="custom-prompt-dir-missing",
                )
            )
        except OSError as exc:
            failures.append(
                PreflightFailure(
                    rule=RULE_CUSTOM_PROMPT_DIR_MISSING,
                    path=f"custom_prompt_dir/{filename}",
                    message=(
                        f"{filename} under custom_prompt_dir is unreadable: "
                        f"{exc}."
                    ),
                    reason="custom-prompt-dir-missing",
                )
            )

    if failures:
        raise PreflightError(failures)

    system_txt = contents["system.txt"]
    user_txt = contents["user.txt"]
    meta_txt = contents["meta.yaml"]

    # FR-024 / T02.22 -- when the caller opts in via ``--auto-inject-guard``,
    # prepend the canonical §11.5 sentence so the substring check below
    # passes for legacy ``system.txt`` files that predate §11.5 framing.
    # When the flag is absent, ``system_txt`` flows through unchanged and
    # the substring check enforces §11.5 verbatim (no silent bypass).
    if auto_inject_guard:
        system_txt = _apply_auto_inject_guard(system_txt)

    # §11.5 substring check on system.txt -- identical helper to the
    # lens path so the failure shape is byte-identical (INV-014).
    failures.extend(
        enforce_injection_guard(
            system=system_txt,
            required_substring=required_substring,
            path_label="custom_prompt_dir/system.txt",
        )
    )

    # meta.yaml parse -- empty file → empty dict, top-level non-mapping
    # rejected. PyYAML is a pinned dependency (pyproject.toml).
    import yaml  # local import keeps the module-level import set tight

    meta: dict[str, Any] = {}
    if meta_txt.strip():
        try:
            parsed = yaml.safe_load(meta_txt)
        except yaml.YAMLError as exc:
            failures.append(
                PreflightFailure(
                    rule=RULE_CUSTOM_PROMPT_DIR_META_INVALID,
                    path="custom_prompt_dir/meta.yaml",
                    message=f"meta.yaml is not valid YAML: {exc}.",
                    reason="custom-prompt-dir-meta-invalid",
                )
            )
            parsed = None
        if parsed is not None:
            if not isinstance(parsed, dict):
                failures.append(
                    PreflightFailure(
                        rule=RULE_CUSTOM_PROMPT_DIR_META_INVALID,
                        path="custom_prompt_dir/meta.yaml",
                        message=(
                            "meta.yaml must be a top-level YAML mapping; got "
                            f"{type(parsed).__name__}."
                        ),
                        reason="custom-prompt-dir-meta-invalid",
                    )
                )
            else:
                meta = parsed

    if failures:
        raise PreflightError(failures)

    return system_txt, user_txt, meta


# ---------------------------------------------------------------------------
# Guards
# ---------------------------------------------------------------------------


def _count_non_whitespace_bytes(payload: bytes) -> int:
    """Return the count of bytes in ``payload`` that are not ASCII whitespace.

    IMM-4 specifies "<50 non-whitespace bytes". ASCII whitespace covers
    the SP / TAB / CR / LF / FF / VT bytes; multibyte UTF-8 sequences
    count as their constituent bytes (the rule is byte-level, not
    codepoint-level).
    """
    whitespace = b" \t\r\n\f\v"
    return sum(1 for byte in payload if byte not in whitespace)


def _truncate_target(
    target_bytes: bytes, line_cap: int
) -> tuple[bytes, bool]:
    """Truncate ``target_bytes`` to the first ``line_cap`` lines.

    Returns the (possibly-truncated) bytes and a ``was_truncated`` flag.
    Line endings are preserved verbatim via ``splitlines(keepends=True)``
    so the sha256 checksum stamped on :class:`PreflightSummary` reflects
    exactly the byte block that downstream phases consume
    (``post-truncation, pre-delimiter wrapping`` per :class:`PreflightSummary`).

    ``line_cap <= 0`` disables truncation; the original bytes are
    returned and ``was_truncated`` is ``False``. This matches the
    schema layer's expectation that a non-positive cap is "off".
    """
    if line_cap <= 0:
        return target_bytes, False
    lines = target_bytes.splitlines(keepends=True)
    if len(lines) <= line_cap:
        return target_bytes, False
    return b"".join(lines[:line_cap]), True


def guard_empty_target(
    target_bytes: bytes,
    *,
    path_label: str = "target.path",
    byte_floor: int = MIN_TARGET_NON_WHITESPACE_BYTES,
) -> list[PreflightFailure]:
    """IMM-4 -- reject targets with fewer than ``byte_floor`` non-whitespace bytes.

    Callers in :func:`run_preflight` pass the post-truncation byte block
    so the count reflects what the dispatched workers would actually see
    (``Truncation`` ``line_cap`` is applied before this guard runs, and
    ``byte_floor`` is sourced from ``job.target.truncation.byte_floor``).
    Returning a non-empty failure list causes :func:`run_preflight` to
    raise :class:`PreflightError` and STOP before any worker dispatch --
    the no-dispatch guarantee verified by the mock-dispatcher test in
    ``tests/swarm/test_imm4_empty_target.py``.

    ``byte_floor`` defaults to :data:`MIN_TARGET_NON_WHITESPACE_BYTES`
    (the IMM-4 / FR-SPEC-005 default of 50) so direct callers that do
    not have a :class:`Truncation` instance in scope still get the
    canonical rule.
    """
    non_ws = _count_non_whitespace_bytes(target_bytes)
    if non_ws >= byte_floor:
        return []
    return [
        PreflightFailure(
            rule=RULE_TARGET_TOO_SMALL,
            path=path_label,
            message=(
                f"Target has {non_ws} non-whitespace byte(s) after "
                f"truncation; IMM-4 requires ≥{byte_floor}. STOP before "
                f"dispatch."
            ),
            reason="target-too-small",
        )
    ]


def check_empty_pool(
    pool: Iterable[str], *, path_label: str = "workers.models"
) -> list[PreflightFailure]:
    """INV-007 -- empty configured model pool produces env-missing.

    Detection-only helper: returns a :class:`PreflightFailure` carrying
    :data:`RULE_EMPTY_POOL` and ``reason="env-missing"`` when ``pool``
    is empty (or contains only empty strings), or ``[]`` when at least
    one model is configured. The structured ``failed``/``env-missing``
    contract emission lives in :func:`emit_env_missing_contract`
    (T02.11 / OQ-008); :func:`run_preflight` wires both together so the
    contract is written before the :class:`PreflightError` raises when
    the OQ-008 "output dir creatable" branch applies.
    """
    pool_list = [m for m in pool if m]
    if pool_list:
        return []
    return [
        PreflightFailure(
            rule=RULE_EMPTY_POOL,
            path=path_label,
            message=(
                "Configured model pool is empty (INV-007). Emit "
                "failed/env-missing contract when output dir is "
                "creatable; bare abort otherwise (OQ-008)."
            ),
            reason="env-missing",
        )
    ]


# ---------------------------------------------------------------------------
# INV-007 / OQ-008 -- ``failed``/``env-missing`` contract emission
# ---------------------------------------------------------------------------


ENV_MISSING_CONTRACT_FILENAME: str = "return-contract.yaml"
"""§5 / line 535 -- canonical filename for the ``write-on-failure`` contract.

The same filename is used by the M5 reduce path on the success / partial
branches; the env-missing branch reuses it so callers (skills, CI gates)
have one path to read regardless of terminal status. The status field
inside disambiguates: ``"failed"`` here vs. ``"success"`` / ``"partial"``
post-dispatch.
"""


ENV_MISSING_REASON: str = "env-missing"
"""OQ-008 / INV-007 canonical reason token.

Mirrors :class:`PreflightFailure.reason` populated by
:func:`check_empty_pool` so the on-disk contract and the in-memory
failure list agree on the classifier string. Downstream operators
(OPS-002 readiness check, M9) grep this token to distinguish env-missing
from other ``failed`` terminal states.
"""


def emit_env_missing_contract(
    job: JobSpec,
    *,
    failures: Iterable[PreflightFailure] = (),
) -> Optional[str]:
    """INV-007 / OQ-008 -- write a ``failed``/``env-missing`` contract.

    Two-branch behavior per the OQ-008 resolution
    (``docs/swarm/oq-resolutions.md``):

        * **Output dir creatable** (``job.output.dir`` non-empty and
          :meth:`pathlib.Path.mkdir` succeeds with ``parents=True``):
          builds a structured failure envelope, serializes it as YAML,
          and writes it atomically (write-to-tmp + ``os.replace``) to
          ``<job.output.dir>/return-contract.yaml``. Returns the
          absolute path so :func:`run_preflight` can attach it to the
          raised :class:`PreflightError` for diagnostics.
        * **Output dir not creatable** (``job.output.dir`` empty, or
          ``mkdir`` raises :class:`OSError` / :class:`PermissionError`
          / :class:`NotADirectoryError`): returns ``None``. No file is
          written, no exception is raised. The caller's
          :class:`PreflightError` still carries :data:`RULE_EMPTY_POOL`
          so callers see the failure; the bare abort means we do not
          fabricate state on disk under a path we cannot own.

    Envelope shape -- a YAML mapping mirroring :class:`ResultContract`
    fields (DM-012) plus two envelope keys specific to the env-missing
    classifier:

        * ``status: "failed"`` -- IMM-5 alignment (``M < 2`` always fails;
          here ``M == 0`` because no dispatch occurred).
        * ``reason: "env-missing"`` -- INV-007 / OQ-008 token; downstream
          operators distinguish env-missing from other ``failed`` terminal
          states by this key. Not (yet) a :class:`ResultContract` field;
          carried as an envelope-level key so :class:`ResultContract`'s
          19-field surface stays intact until OPS-002 (M9) adds a typed
          reason field upstream.
        * ``preflight_failures: [...]`` -- structured
          :class:`PreflightFailure` list from the calling
          :func:`run_preflight` so callers see every failing rule in
          one pass (mirrors :class:`PreflightError.failures`).
        * Remaining keys (``contract_version``, ``job_id``, ``caller``,
          ``lens``, ``target``, ``workers_requested``,
          ``workers_succeeded``, ``workers_failed``, ``output_files``,
          ``amalgamation_mode``, ``merged_path``, ``caller_metadata``,
          ``recommended_next_command``, ``artifacts``, ``started``,
          ``finished``, ``elapsed_ms``, ``lens_source``) mirror the
          job spec / dataclass defaults via :func:`to_dict` so the
          contract is grep-compatible with a successful contract.

    Args:
        job: the :class:`JobSpec` carrying ``output.dir`` (write
            target), ``job_id``, ``caller``, ``lens``, ``workers``,
            ``amalgamation_mode``, and ``target.path``. Read-only.
        failures: optional iterable of :class:`PreflightFailure`
            instances to embed as ``preflight_failures``. Typically the
            output of :func:`check_empty_pool` plus any other guards
            that fired in the same Wave-0 pass.

    Returns:
        Absolute path to the written ``return-contract.yaml`` on the
        creatable branch; ``None`` on the bare-abort branch.

    Side effects:
        Writes ``<job.output.dir>/return-contract.yaml`` atomically on
        the creatable branch. No write on the bare-abort branch.
        Never raises -- both branches are recovery-shaped so the
        calling :class:`PreflightError` carries the canonical failure.
    """
    output_dir = (job.output.dir or "").strip()
    if not output_dir:
        # Bare abort -- no output.dir means we cannot place the contract
        # without inventing a path the caller never asked for.
        return None

    out = Path(output_dir)
    try:
        out.mkdir(parents=True, exist_ok=True)
    except (OSError, NotADirectoryError, PermissionError):
        # OQ-008 bare-abort branch: output dir cannot be created, so we
        # do not fabricate state on disk. The PreflightError still
        # surfaces RULE_EMPTY_POOL.
        return None

    failure_list = [
        {
            "rule": f.rule,
            "path": f.path,
            "message": f.message,
            "reason": f.reason,
        }
        for f in failures
    ]

    workers_requested = int(job.workers.count or 0)
    envelope: dict[str, Any] = {
        "contract_version": "1.0",
        "status": "failed",
        "reason": ENV_MISSING_REASON,
        "job_id": job.job_id,
        "started": "",
        "finished": "",
        "elapsed_ms": 0,
        "caller": {
            "skill": job.caller.skill,
            "skill_version": job.caller.skill_version,
            "invocation_label": job.caller.invocation_label,
            "kind": job.caller.kind,
        },
        "lens": job.lens,
        "lens_source": "registry" if job.lens and job.lens != "custom" else (
            "custom" if job.lens == "custom" else ""
        ),
        "target": {
            "path": job.target.path,
            "checksum": "",
            "truncated": False,
            "truncation_line_cap": job.target.truncation.line_cap,
        },
        "workers_requested": workers_requested,
        "workers_succeeded": 0,
        "workers_failed": 0,
        "output_files": [],
        "amalgamation_mode": job.amalgamation_mode,
        "merged_path": None,
        "caller_metadata": {"suspect": False, "tier": ""},
        "recommended_next_command": "",
        "artifacts": {
            "manifest_path": "",
            "state_path": "",
            "event_log_jsonl": "",
            "event_log_md": "",
            "done_sentinel": "",
        },
        "preflight_failures": failure_list,
    }

    import yaml  # local import keeps the module-level import set tight

    payload = yaml.safe_dump(
        envelope, sort_keys=True, default_flow_style=False
    )

    target_path = confine_path(out / ENV_MISSING_CONTRACT_FILENAME, out)
    fd, tmp_name = tempfile.mkstemp(
        prefix=".return-contract-", suffix=".yaml.tmp", dir=str(out)
    )
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(tmp_name, target_path)
    except OSError:
        # Best-effort cleanup; on write failure, fall back to bare abort
        # so the caller's PreflightError still surfaces the empty-pool
        # rule without a half-written contract on disk.
        try:
            os.unlink(tmp_name)
        except FileNotFoundError:
            pass
        return None

    return str(target_path.resolve())


def workers_exceed_pool(workers_count: int, pool: Iterable[str]) -> bool:
    """INV-005 -- detection-only helper.

    Returns ``True`` when ``workers_count`` strictly exceeds the size
    of the **non-empty** ``pool``. An empty pool is INV-007's domain
    (:func:`check_empty_pool`); this helper returns ``False`` so the
    two guards never double-report.

    Surfaced separately from :func:`check_pool_size` so the
    ``run_preflight`` orchestrator can branch on the OQ-007 policy
    (warn-with-defaults vs STOP) without re-implementing the size
    comparison or having to inspect a failure list to decide whether
    to clamp.
    """
    pool_list = [m for m in pool if m]
    if not pool_list:
        return False
    return workers_count > len(pool_list)


def check_pool_size(
    workers_count: int,
    pool: Iterable[str],
    *,
    path_label: str = "workers.count",
    policy: PoolPolicy = "stop",
) -> list[PreflightFailure]:
    """INV-005 -- ``workers.count`` must not exceed the configured pool size.

    OQ-007 resolution (M1 exit, recorded in
    ``docs/swarm/oq-resolutions.md``): both branches are supported via
    the ``policy`` parameter so callers can pick the semantics that
    match their context.

        * ``policy="stop"`` (V2) -- detection emits a
          :class:`PreflightFailure` with :data:`RULE_WORKERS_EXCEED_POOL`
          and the caller aborts Wave 0. This is the default for the
          helper itself so direct callers (tests, ad-hoc validation
          scripts) get the strict-by-default behavior the schema layer
          assumes.
        * ``policy="warn"`` (V1, OQ-007 architect-recommended) --
          detection returns ``[]`` so the helper does not block Wave 0
          on its own; :func:`run_preflight` separately uses
          :func:`workers_exceed_pool` to clamp ``workers.count`` to
          ``len(pool)`` and emit a WARNING log line. Tests verifying
          warn semantics should drive the end-to-end behavior through
          :func:`run_preflight` rather than this helper.

    The two-mode design preserves the existing direct-call contract
    (``check_pool_size(5, ["a", "b", "c"]) -> failure list``) while
    letting :func:`run_preflight`'s ``pool_policy`` kwarg select the
    project default (V1 warn-with-defaults).

    Empty-pool detection is INV-007's job (:func:`check_empty_pool`);
    this helper skips the comparison when the pool is empty so the two
    guards do not double-report. The empty-pool guard wins; this guard
    is silent on an empty pool regardless of ``policy``.

    Raises:
        ValueError: ``policy`` is not one of ``"warn"`` / ``"stop"``.
    """
    if policy not in ("warn", "stop"):
        raise ValueError(
            f"check_pool_size: policy must be 'warn' or 'stop', got "
            f"{policy!r}."
        )
    if not workers_exceed_pool(workers_count, pool):
        return []
    if policy == "warn":
        # Detection-only: the OQ-007 V1 clamp + warning live at the
        # ``run_preflight`` call site so the helper stays pure (no
        # side effects, no JobSpec mutation).
        return []
    pool_list = [m for m in pool if m]
    return [
        PreflightFailure(
            rule=RULE_WORKERS_EXCEED_POOL,
            path=path_label,
            message=(
                f"workers.count={workers_count} exceeds configured "
                f"model-pool size={len(pool_list)} (INV-005). Resolution "
                "per OQ-007 V2 STOP."
            ),
            reason="workers-exceed-pool",
        )
    ]


def enforce_injection_guard(
    system: str,
    required_substring: str,
    *,
    path_label: str = "prompt.system",
) -> list[PreflightFailure]:
    """§11.5 -- ``system`` must contain ``required_substring``.

    T02.02 landed the helper at this call site; T02.07 promoted it to
    the **single enforcement code path** for the §11.5 substring rule
    across the three prompt-input paths -- lens-driven
    (``run_preflight`` re-asserts after ``expand_lens_defaults``),
    JSON-Schema (``schema._injection_substring_failures`` and this
    helper both delegate to :func:`schema.contains_required_substring`),
    and custom-prompt-dir (``read_custom_prompt_dir`` calls this
    helper directly on ``system.txt`` contents). A mutation of the
    underlying predicate breaks all three paths simultaneously; that
    is what the T02.07 parametrized test pins.

    An empty ``required_substring`` is treated as "guard disabled" --
    the schema layer (T02.01) rejects ``enabled=True`` with an empty
    substring under :data:`schema.RULE_INJECTION_REQUIRED`, so this
    helper does not duplicate that check.
    """
    if contains_required_substring(system, required_substring):
        return []
    return [
        PreflightFailure(
            rule=RULE_INJECTION_GUARD,
            path=path_label,
            message=(
                f"{path_label} must contain the §11.5 required substring; "
                f"missing: {required_substring!r}."
            ),
            reason="injection-guard",
        )
    ]


# ---------------------------------------------------------------------------
# Target wrapping + bypass neutralization (T02.07 / NFR-003)
# ---------------------------------------------------------------------------


_BYPASS_NEUTRALIZER: str = "​"
"""Zero-width space inserted into bare occurrences of the close delimiter.

The character renders invisibly to a human reader and to most LLM
tokenizers (treated as whitespace or a no-op), but breaks the exact
byte-level match that a worker would use to detect the end of the
target block. Picked over alternatives (backslash escape, bracketing,
HTML entities) because it preserves the visual content of the wrapped
target while neutralising the bypass: a target that contained
``<<<END TARGET>>>`` literally now contains ``<<<END\\u200bTARGET>>>``
inside the wrapped body, so the worker's parser sees only the outer
delimiter as the boundary marker.
"""


DEFAULT_OPEN_DELIM: str = "<<<TARGET>>>"
"""§11.5 canonical open delimiter -- mirrors :class:`Delimiters.open`."""


DEFAULT_CLOSE_DELIM: str = "<<<END TARGET>>>"
"""§11.5 canonical close delimiter -- mirrors :class:`Delimiters.close`."""


def _neutralize_bypass(target: str, close_delim: str) -> str:
    """Escape bare ``close_delim`` occurrences inside ``target``.

    Inserts :data:`_BYPASS_NEUTRALIZER` after the third character of the
    close delimiter wherever the literal sequence appears, breaking the
    exact-match boundary a malicious target would rely on while leaving
    the surrounding bytes intact. When the close delimiter does not
    appear, returns ``target`` verbatim (no allocation).

    The choice of "after character 3" is arbitrary but deterministic
    and matches the standard §11.5 canonical close (``<<<`` prefix);
    callers that override delimiters get the ZWSP inserted at the same
    offset regardless of delimiter content because the goal is just to
    break the exact match, not to be semantically pretty.
    """
    if not close_delim or close_delim not in target:
        return target
    # Insert ZWSP after the 3rd character -- breaks the exact match
    # without losing any byte of the original close marker. For the
    # canonical ``<<<END TARGET>>>`` this yields ``<<<​END TARGET>>>``.
    if len(close_delim) <= 3:
        # Pathologically short delimiter: just prepend ZWSP.
        neutralised = _BYPASS_NEUTRALIZER + close_delim
    else:
        neutralised = close_delim[:3] + _BYPASS_NEUTRALIZER + close_delim[3:]
    return target.replace(close_delim, neutralised)


def wrap_target_with_delimiters(
    target: str | bytes,
    *,
    open_delim: str = DEFAULT_OPEN_DELIM,
    close_delim: str = DEFAULT_CLOSE_DELIM,
) -> str:
    """T02.07 -- wrap ``target`` in §11.5 delimiters with bypass neutralization.

    Returns the string ``f"{open_delim}\\n{target}\\n{close_delim}"``
    with one rewrite: every occurrence of ``close_delim`` inside the
    body is replaced with a visually-identical but exact-match-broken
    variant (see :func:`_neutralize_bypass`). The wrapped target carries
    the §11.5 data/instructions separation that the canonical sentence
    in ``prompt.system`` references; without the bypass rewrite, a
    target that contains the literal close marker could trick a worker
    into treating the trailing bytes as instructions (NFR-003 / T02.26
    pins this property).

    ``target`` accepts ``bytes`` for ergonomics at the dispatch site
    (where target_loader returns raw bytes); UTF-8 is decoded with
    ``errors="replace"`` so non-UTF-8 payloads do not crash the
    wrapper -- the replacement char is itself benign and continues to
    sit inside the delimited body. Production transport layers should
    feed ``str`` payloads after their own decoding pass; the ``bytes``
    fast path exists so preflight call sites can stay symmetric with
    the target_loader contract.
    """
    if isinstance(target, bytes):
        body = target.decode("utf-8", errors="replace")
    else:
        body = target
    body = _neutralize_bypass(body, close_delim)
    return f"{open_delim}\n{body}\n{close_delim}"


# ---------------------------------------------------------------------------
# Manifest persistence helpers
# ---------------------------------------------------------------------------


def _target_checksum(target_bytes: bytes) -> str:
    """sha256 hex digest of the ingested target block.

    Per :class:`PreflightSummary` semantics: ``post-truncation,
    pre-delimiter wrapping``. T02.13 wires the truncation step into
    :func:`run_preflight` so the bytes passed here have already been
    capped at ``Truncation.line_cap`` lines.
    """
    return hashlib.sha256(target_bytes).hexdigest()


def emit_manifest(
    resolved_lens_entry: ResolvedLensEntry,
    target_checksum: str,
    transport_kind: str,
    *,
    output_dir: str | os.PathLike[str],
    job_id: str = "",
    workers_requested: int = 0,
    contract_version: str = "1.0",
) -> Path:
    """T06.05 / FR-016 -- atomic Wave-0 manifest emit.

    Assembles a :class:`Manifest` from the three positional FR-016
    inputs (the verbatim :class:`ResolvedLensEntry` snapshot plus the
    two :class:`PreflightSummary` scalars derivable independently from
    the resolved spec) and writes it atomically to
    ``<output_dir>/manifest.json`` via the existing
    :func:`write_manifest` helper (write-to-tmp + ``os.replace``).

    The signature mirrors the phase-6-tasklist deliverable line
    ``emit_manifest(resolved_lens_entry, target_checksum,
    transport_kind) -> Path`` -- the three semantic inputs are
    positional and named verbatim from the deliverable; the remaining
    Manifest scalars (``output_dir``, ``job_id``, ``workers_requested``,
    ``contract_version``) are keyword-only so they cannot drift into
    positional callsites that would shadow the deliverable contract.

    Args:
        resolved_lens_entry: the DM-011 snapshot captured at Wave 0 by
            :func:`materialize_lens_defaults` /
            :meth:`ResolvedLensEntry.from_lens`. Stamped verbatim onto
            :attr:`Manifest.resolved_lens_entry` so resume reads the
            same bytes (INV-001 / INV-016).
        target_checksum: sha256 hex digest of the post-truncation,
            pre-delimiter-wrapping target block (see
            :func:`_target_checksum` and :class:`PreflightSummary`).
            Empty string is valid only for the no-arg round-trip stub
            case; production callsites compute it from the truncated
            target bytes.
        transport_kind: copied verbatim from
            :class:`TransportSpec.kind` so the manifest carries a
            stable view even if a future config layer rewrites the
            transport between resume and dispatch.
        output_dir: directory under which ``manifest.json`` is written
            atomically. Created with ``parents=True`` by
            :func:`write_manifest`.
        job_id: stamped onto :attr:`Manifest.job_id`; mirrors the
            executor's UUID assignment so the manifest /
            :class:`ResultContract` / :class:`SwarmState` triple agree.
        workers_requested: the FR-020-expanded count actually
            dispatched at Wave 1; stamped onto
            :attr:`PreflightSummary.workers_requested`.
        contract_version: schema version. Defaults to ``"1.0"`` to
            match the :class:`Manifest` /:class:`ResultContract`
            convention.

    Returns:
        :class:`Path` -- the resolved absolute path to the written
        ``manifest.json``. Path object (not ``str``) per the
        deliverable contract; callers needing a string can call
        :meth:`Path.__fspath__` or ``str(path)`` directly.

    Side effects:
        Writes ``<output_dir>/manifest.json`` atomically. The full
        :class:`ResolvedLensEntry` snapshot (system_prompt_fragment,
        user_template, recipe_name, default_workers, suspect, tier,
        recommended_next_command_template, stability, name) is
        embedded verbatim so a ``yq``/``jq`` query on any snapshot
        field returns a non-null value (acceptance criterion).
    """
    if not isinstance(resolved_lens_entry, ResolvedLensEntry):
        raise TypeError(
            "emit_manifest expects a ResolvedLensEntry snapshot, got "
            f"{type(resolved_lens_entry).__name__}"
        )
    manifest = Manifest(
        contract_version=contract_version,
        job_id=job_id,
        resolved_lens_entry=resolved_lens_entry,
        preflight=PreflightSummary(
            target_checksum=target_checksum,
            workers_requested=workers_requested,
            transport_kind=transport_kind,
        ),
    )
    written = write_manifest(manifest, output_dir)
    return Path(written)


def write_manifest(manifest: Manifest, output_dir: str | os.PathLike[str]) -> str:
    """Atomically write ``manifest.json`` under ``output_dir``.

    Uses write-to-tmp + ``os.replace`` so a mid-write kill never leaves
    a partial manifest and rerun is idempotent (IMM-6 / NFR-002). The
    JSON payload uses ``to_json`` (``sort_keys=True``) so resume reads
    a byte-identical bundle back (INV-016).

    NFR-013 / AC-014 confinement: the resolved ``manifest.json`` target
    is run through :func:`~superclaude.cli.swarm.state.confine_path`
    before any directory or file is created. A symlink-poisoned
    ``output_dir`` whose resolved root differs from its lexical form
    therefore cannot be exploited to write the manifest outside the
    job's ``--output`` tree.

    Returns the absolute path to the written ``manifest.json``.
    """
    out = Path(output_dir)
    target = confine_path(out / "manifest.json", out)
    out.mkdir(parents=True, exist_ok=True)
    payload = to_json(manifest)
    # Reserve a tmp file in the same directory so ``os.replace`` stays
    # atomic across filesystem boundaries.
    fd, tmp_name = tempfile.mkstemp(
        prefix=".manifest-", suffix=".json.tmp", dir=str(out)
    )
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(tmp_name, target)
    except Exception:
        # Best-effort cleanup; do not mask the original exception.
        try:
            os.unlink(tmp_name)
        except FileNotFoundError:
            pass
        raise
    return str(target.resolve())


# ---------------------------------------------------------------------------
# Spec coercion
# ---------------------------------------------------------------------------


def _coerce_dict(spec: dict[str, Any] | JobSpec) -> dict[str, Any]:
    if isinstance(spec, JobSpec):
        return to_dict(spec)
    if isinstance(spec, dict):
        return spec
    raise TypeError(
        f"run_preflight expects a dict or JobSpec, got {type(spec).__name__}"
    )


def _coerce_jobspec(spec_dict: dict[str, Any]) -> JobSpec:
    return from_dict(JobSpec, spec_dict)


def _failures_from_schema_error(
    err: SchemaValidationError,
) -> list[PreflightFailure]:
    return [
        PreflightFailure(
            rule=f.rule,
            path=f.path,
            message=f.message,
            reason="schema-invalid",
        )
        for f in err.failures
    ]


def _default_target_loader(path: str) -> bytes:
    """Read the file at ``path`` and return its bytes verbatim."""
    return Path(path).read_bytes()


# ---------------------------------------------------------------------------
# run_preflight -- the Wave 0 entrypoint
# ---------------------------------------------------------------------------


def run_preflight(
    job_spec: dict[str, Any] | JobSpec,
    *,
    target_loader: Optional[Callable[[str], bytes]] = None,
    pool: Optional[Iterable[str]] = None,
    output_dir: Optional[str | os.PathLike[str]] = None,
    pool_policy: PoolPolicy = DEFAULT_POOL_POLICY,
    caller_metadata_override: Optional[CallerMetadata] = None,
) -> PreflightResult:
    """Execute Wave 0 against ``job_spec``; return :class:`PreflightResult`.

    On success the result carries the freshly-stamped Manifest +
    SwarmState (state=``preflight_ok``); when ``output_dir`` is
    supplied, the manifest is also written to ``manifest.json``
    atomically and the on-disk path is returned on
    ``result.manifest_path``.

    On failure the function raises :class:`PreflightError` whose
    ``failures`` list enumerates every failing rule -- the executor
    feeds those into the structured ``failed`` ResultContract per the
    INV-007 / OQ-008 emission rules (T02.11) and the IMM-4 STOP
    contract (T02.13).

    Args:
        job_spec: dict (typically a YAML/JSON document) or
            :class:`JobSpec` instance.
        target_loader: optional callable mapping ``target.path`` to the
            raw target bytes. Defaults to a file read. Tests pass a
            closure to inject deterministic byte payloads.
        pool: optional iterable of model identifiers representing the
            configured T2 pool. Defaults to ``job_spec.workers.models``.
            T02.10 will refine this to read the proxy env contract
            (AC-017) directly.
        output_dir: optional directory where ``manifest.json`` is
            written atomically. When omitted, the manifest is returned
            in-memory only -- the executor (M3 / COMP-013) calls
            :func:`write_manifest` later.
        pool_policy: OQ-007 resolution selector for the INV-005
            worker-count vs model-pool guard. Defaults to
            :data:`DEFAULT_POOL_POLICY` (``"warn"`` -- V1
            warn-with-defaults). Strict callers pass ``"stop"`` to get
            the V2 STOP-before-dispatch semantics. See
            ``docs/swarm/oq-resolutions.md`` for the resolution record.
        caller_metadata_override: optional :class:`CallerMetadata`
            payload that overrides the lens-default ``suspect`` /
            ``tier`` per OQ-009 (caller-overridable). When ``None``
            (the default), the resolved metadata mirrors the lens
            entry; when supplied, every field on ``override`` wins
            field-by-field per :func:`resolve_caller_metadata`. See
            ``docs/swarm/oq-resolutions.md`` for the OQ-009 record.
    """
    # ----- Phase 1: schema validation (fatal on first batch) -------------
    spec_dict = _coerce_dict(job_spec)
    try:
        schema.validate_or_raise(spec_dict)
    except SchemaValidationError as err:
        raise PreflightError(_failures_from_schema_error(err)) from err

    job: JobSpec = _coerce_jobspec(spec_dict)

    failures: list[PreflightFailure] = []

    # ----- Phase 2: lens resolution + materialization --------------------
    try:
        lens_entry = resolve_lens(job.lens)
    except KeyError:
        # Without a resolved lens we cannot materialize the manifest
        # snapshot; abort here so the caller's diagnostics include the
        # unknown-lens reason without trailing guard noise.
        raise PreflightError(
            [
                PreflightFailure(
                    rule=RULE_UNKNOWN_LENS,
                    path="lens",
                    message=(
                        f"Unknown lens: {job.lens!r}. Lens must be "
                        "registered in superclaude.cli.swarm.lenses.LENSES "
                        "(T02.14) or supplied via set_lens_resolver."
                    ),
                    reason="lens-unknown",
                )
            ]
        ) from None

    resolved = materialize_lens_defaults(job, lens_entry)

    # DM-020 / OQ-009 -- resolve CallerMetadata from the lens entry,
    # honouring the caller-overridable precedence. The resolved value
    # is attached to PreflightResult so the executor can stamp it onto
    # ``ResultContract.caller_metadata`` at reduce time (M5) without
    # re-resolving against the manifest snapshot.
    resolved_caller_metadata = resolve_caller_metadata(
        lens_entry, override=caller_metadata_override
    )

    # ----- Phase 3: guards (§11.5 / IMM-4 / INV-005 / INV-007) -----------

    # §11.5 -- the schema layer already enforces the cross-field rule
    # against ``target.injection_guard.required_substring``; this site
    # re-asserts so the lens-derived ``system_prompt_fragment`` (which
    # may diverge from ``prompt.system`` once T02.04 expands defaults)
    # also passes the check. T02.07 centralises both call sites.
    failures.extend(
        enforce_injection_guard(
            system=job.prompt.system,
            required_substring=job.target.injection_guard.required_substring,
            path_label="prompt.system",
        )
    )

    # IMM-4 -- load the target bytes; surface unreadable targets as a
    # structured failure rather than letting the FileNotFoundError
    # bubble up (callers want one shape for diagnostics).
    loader = target_loader if target_loader is not None else _default_target_loader
    target_bytes: bytes = b""
    target_load_ok = False
    try:
        target_bytes = loader(job.target.path)
    except FileNotFoundError as exc:
        failures.append(
            PreflightFailure(
                rule=RULE_TARGET_UNREADABLE,
                path="target.path",
                message=(
                    f"target.path is not readable: {exc.strerror or exc}."
                ),
                reason="target-unreadable",
            )
        )
    except OSError as exc:
        failures.append(
            PreflightFailure(
                rule=RULE_TARGET_UNREADABLE,
                path="target.path",
                message=f"target.path read failed: {exc}.",
                reason="target-unreadable",
            )
        )
    else:
        target_load_ok = True

    # IMM-4 (T02.13) -- truncate first, then count. The checksum stamped
    # on PreflightSummary (Phase 4 below) is taken from the truncated
    # block so resume / dispatch see byte-identical inputs. The byte
    # floor comes from ``target.truncation.byte_floor`` so callers can
    # tighten the rule per-spec without touching this site.
    if target_load_ok:
        target_bytes, _was_truncated = _truncate_target(
            target_bytes, job.target.truncation.line_cap
        )
        failures.extend(
            guard_empty_target(
                target_bytes,
                byte_floor=job.target.truncation.byte_floor,
            )
        )

    # INV-005 / INV-007 -- pool-size guards. INV-007 reports first so the
    # empty-pool case does not also surface as workers_exceed_pool.
    pool_seq = list(pool) if pool is not None else list(job.workers.models)
    empty_pool_failures = check_empty_pool(pool_seq)
    failures.extend(empty_pool_failures)
    if not empty_pool_failures and workers_exceed_pool(
        job.workers.count, pool_seq
    ):
        # OQ-007 resolution branch. ``warn`` (V1, default) clamps the
        # JobSpec workers.count to the pool size and logs WARNING so
        # downstream phases (manifest emit, dispatch) see a coherent
        # pool/worker ratio. ``stop`` (V2) emits the structured
        # failure via ``check_pool_size`` and aborts Wave 0.
        if pool_policy == "warn":
            original_count = job.workers.count
            job.workers.count = len(pool_seq)
            _logger.warning(
                "INV-005 / OQ-007 V1 warn-with-defaults: "
                "workers.count=%d exceeds configured pool size=%d; "
                "clamping workers.count to %d for job_id=%s.",
                original_count,
                len(pool_seq),
                job.workers.count,
                job.job_id,
            )
        else:
            failures.extend(
                check_pool_size(
                    job.workers.count, pool_seq, policy="stop"
                )
            )

    if failures:
        # INV-007 / OQ-008 -- when the empty-pool guard fired, attempt
        # to write a ``failed``/``env-missing`` ``return-contract.yaml``
        # to ``job.output.dir`` before raising. The contract path is
        # attached to the PreflightError so the executor / skill driver
        # can surface it without re-running preflight.
        env_missing_contract_path: Optional[str] = None
        if any(f.rule == RULE_EMPTY_POOL for f in failures):
            env_missing_contract_path = emit_env_missing_contract(
                job, failures=failures
            )
        raise PreflightError(
            failures, env_missing_contract_path=env_missing_contract_path
        )

    # ----- Phase 4: Manifest emit + SwarmState init ----------------------
    manifest = Manifest(
        contract_version="1.0",
        job_id=job.job_id,
        resolved_lens_entry=resolved,
        preflight=PreflightSummary(
            target_checksum=_target_checksum(target_bytes),
            workers_requested=job.workers.count,
            transport_kind=job.transport.kind,
        ),
    )
    state = SwarmState(
        state="preflight_ok",
        job_id=job.job_id,
        # ``updated`` is stamped at write-time by the COMP-011 state
        # module (M3 -- T03.* tasks). Leaving it empty here preserves
        # the no-arg round-trip stub.
        updated="",
    )

    manifest_path: Optional[str] = None
    if output_dir is not None:
        manifest_path = write_manifest(manifest, output_dir)

    return PreflightResult(
        manifest=manifest,
        state=state,
        manifest_path=manifest_path,
        caller_metadata=resolved_caller_metadata,
    )


# ---------------------------------------------------------------------------
# T06.01 -- INV-001 resume-from-manifest rehydration
# ---------------------------------------------------------------------------


def resume_mode(
    manifest_path: str | os.PathLike[str],
    *,
    force_relens: bool = False,
) -> JobSpec:
    """INV-001 -- rehydrate a :class:`JobSpec` from a persisted manifest.

    Reads ``manifest.json`` from ``manifest_path`` and reconstructs a
    :class:`JobSpec` whose lens-derived fields come from the manifest's
    ``resolved_lens_entry`` snapshot. The live LENSES registry is **not**
    consulted -- any edits made between the original Wave-0 emit and
    this resume call are silently ignored, satisfying INV-001 /
    INV-016 (the manifest is the durable source-of-truth).

    The returned JobSpec carries the subset of fields recoverable from
    the manifest alone:

        * ``job_id`` -- from :attr:`Manifest.job_id`.
        * ``lens`` -- the lens name from the resolved snapshot.
        * ``workers.count`` -- :attr:`PreflightSummary.workers_requested`.
        * ``transport.kind`` -- :attr:`PreflightSummary.transport_kind`.
        * ``prompt.system`` -- :attr:`ResolvedLensEntry.system_prompt_fragment`.
        * ``prompt.user_template`` -- :attr:`ResolvedLensEntry.user_template`.
        * ``normalization.recipe`` -- :attr:`ResolvedLensEntry.recipe_name`.
        * ``recommended_next_command_template`` -- from snapshot.

    Fields not recoverable from the manifest alone (``target.path``,
    ``output.dir``, ``transport.base_url_env``, custom prompts, etc.)
    take their dataclass defaults. The resume-driving caller
    (``run_cmd --resume`` in T06.04) layers in the remaining context
    from the on-disk job directory (worker ``.meta.json`` files,
    state file, persisted job-spec snapshot per T06.05).

    Args:
        manifest_path: filesystem path to ``manifest.json`` previously
            written by :func:`write_manifest`.
        force_relens: T06.07 / FR-025 opt-in override. When ``True``,
            the lens name is read from the manifest but every
            lens-derived field (``prompt.system``,
            ``prompt.user_template``, ``normalization.recipe``,
            ``recommended_next_command_template``) is re-resolved from
            the live LENSES registry via :func:`resolve_lens`. This is
            the escape hatch for operators who explicitly want
            mutation visibility on resume. Non-lens manifest fields
            (``job_id``, ``workers.count``, ``transport.kind``) still
            come from the manifest so the slot fan-out and transport
            binding stay aligned with the original job. Raises
            :class:`KeyError` when the lens name is no longer
            registered.

    Returns:
        :class:`JobSpec` rehydrated from the manifest snapshot (default)
        or with lens-derived fields re-resolved from the live registry
        (``force_relens=True``).
    """
    payload = Path(manifest_path).read_text(encoding="utf-8")
    manifest: Manifest = from_json(Manifest, payload)
    snapshot: ResolvedLensEntry = manifest.resolved_lens_entry

    if force_relens:
        live_entry: LensEntry = resolve_lens(snapshot.name)
        live_snapshot: ResolvedLensEntry = ResolvedLensEntry.from_lens(
            live_entry
        )
        return JobSpec(
            job_id=manifest.job_id,
            lens=live_snapshot.name,
            workers=WorkerSpec(count=manifest.preflight.workers_requested),
            transport=TransportSpec(kind=manifest.preflight.transport_kind),
            prompt=PromptSpec(
                system=live_snapshot.system_prompt_fragment,
                user_template=live_snapshot.user_template,
            ),
            normalization=NormalizationSpec(recipe=live_snapshot.recipe_name),
            recommended_next_command_template=(
                live_snapshot.recommended_next_command_template
            ),
        )

    return JobSpec(
        job_id=manifest.job_id,
        lens=snapshot.name,
        workers=WorkerSpec(count=manifest.preflight.workers_requested),
        transport=TransportSpec(kind=manifest.preflight.transport_kind),
        prompt=PromptSpec(
            system=snapshot.system_prompt_fragment,
            user_template=snapshot.user_template,
        ),
        normalization=NormalizationSpec(recipe=snapshot.recipe_name),
        recommended_next_command_template=(
            snapshot.recommended_next_command_template
        ),
    )


# ---------------------------------------------------------------------------
# Public surface
# ---------------------------------------------------------------------------


__all__ = [
    "CANONICAL_FILENAME_TEMPLATE",
    "DEFAULT_CLOSE_DELIM",
    "DEFAULT_OPEN_DELIM",
    "DEFAULT_POOL_POLICY",
    "ENV_MISSING_CONTRACT_FILENAME",
    "ENV_MISSING_REASON",
    "MIN_TARGET_NON_WHITESPACE_BYTES",
    "PoolPolicy",
    "PreflightError",
    "PreflightFailure",
    "PreflightResult",
    "RULE_CUSTOM_PROMPT_DIR_META_INVALID",
    "RULE_CUSTOM_PROMPT_DIR_MISSING",
    "RULE_EMPTY_POOL",
    "RULE_INJECTION_GUARD",
    "RULE_TARGET_TOO_SMALL",
    "RULE_TARGET_UNREADABLE",
    "RULE_UNKNOWN_LENS",
    "RULE_WORKERS_EXCEED_POOL",
    "auto_inject_guard",
    "check_empty_pool",
    "check_pool_size",
    "emit_env_missing_contract",
    "emit_manifest",
    "enforce_injection_guard",
    "expand_lens_defaults",
    "guard_empty_target",
    "materialize_lens_defaults",
    "read_custom_prompt_dir",
    "resolve_caller_metadata",
    "resolve_lens",
    "resume_mode",
    "run_preflight",
    "set_lens_resolver",
    "workers_exceed_pool",
    "wrap_target_with_delimiters",
    "write_manifest",
    "truncate_target",
]


# Public alias so test modules can import without the leading underscore.
truncate_target = _truncate_target
