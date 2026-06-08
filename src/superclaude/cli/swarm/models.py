"""Swarm data models -- DM-001..DM-020 dataclass aggregator.

This module is the **aggregator** that re-exports every dataclass the
swarm pipeline serializes. It mirrors ``cli/sprint/models.py`` in role.

Scope split (T01.10 vs T01.13..T01.28):
    T01.10 (this task) lands the *scaffolding*: minimal ``@dataclass``
    stubs for all twenty DM-### records, ``__all__`` enumeration, and
    the ``to_dict()``/``from_dict()`` helpers + JSON round-trip used by
    every downstream test. Downstream tasks T01.13..T01.28 each pick a
    single DM-### record and replace its empty body with the full
    field set drawn from ``.dev/releases/Current/MultiModelSwarm/roadmap.md``.

DM-### inventory (mapped to roadmap rows R-011..R-029 + R-016/DM-020):
    DM-001 JobSpec               -- top-level job specification
    DM-002 WorkerSpec            -- per-worker config (count/timeout/retry)
    DM-003 TargetSpec            -- target ingestion + injection guard
    DM-004 TransportSpec         -- transport kind + env-var contract
    DM-005 PromptSpec            -- verbatim system/user_template
    DM-006 NormalizationSpec     -- recipe + on_parse_error policy
    DM-007 OutputSpec            -- output dir/filename/atomic-write
    DM-008 StatusPolicy          -- IMM-5 status determination defaults
    DM-009 RuntimeSpec           -- inline vs detached mode + sentinels
    DM-010 LensEntry             -- registry entry (13 fields)
    DM-011 ResolvedLensEntry     -- immutable lens snapshot (INV-016)
    DM-012 ResultContract        -- final caller-facing contract
    DM-013 WorkerResult          -- per-worker output entry
    DM-014 SwarmState            -- persistent ``.swarm-state.json``
    DM-015 EventRecord           -- JSONL event entry
    DM-016 Manifest              -- preflight artifact (INV-001 anchor)
    DM-017 DoneSentinel          -- terminal marker ``done.json``
    DM-018 Artifacts             -- path bundle embedded in contract
    DM-019 CallerInfo            -- caller metadata (skill/kind)
    DM-020 CallerMetadata        -- lens/caller-attached output metadata

Round-trip contract (validated by ``tests/swarm/test_models_round_trip.py``):
    For every DM-### dataclass ``X`` declared here, ``from_dict(X,
    to_dict(instance))`` returns a value equal to ``instance``. The
    helpers route through ``dataclasses.asdict`` and ``json``-compatible
    primitives, so they remain valid as downstream tasks flesh out the
    field sets -- as long as every new field is itself JSON-serializable
    (or a nested dataclass exported from this module).
"""

from __future__ import annotations

import dataclasses
import json
import typing
from dataclasses import dataclass, field
from typing import Any, Literal, Optional, Type, TypeVar

# ---------------------------------------------------------------------------
# DM-### dataclass stubs.
#
# Each class is intentionally empty at T01.10 -- field-level work is the
# responsibility of T01.13..T01.28, which replace the body of exactly one
# class per task. Keeping the stubs empty here avoids field-drift between
# the aggregator and the per-record specs in the roadmap (DM-### rows in
# ``.dev/releases/Current/MultiModelSwarm/roadmap.md``).
# ---------------------------------------------------------------------------


AmalgamationMode = Literal["raw", "normalize", "normalize+merge"]
TransportKind = Literal["openai_compat", "stub"]
RuntimeMode = Literal["inline", "detached"]
Stability = Literal["stable", "experimental"]
ResultStatus = Literal["success", "partial", "failed"]
WorkerStatus = Literal["success", "timeout", "parse_error", "proxy_error"]
CallerKind = Literal["claude", "cli", "subprocess"]
SwarmStateValue = Literal[
    "preflight_ok",
    "dispatching",
    "normalizing",
    "reducing",
    "terminal",
]
EventType = Literal[
    "worker_start",
    "worker_progress",
    "worker_done",
    "wave_transition",
    "terminal",
]


@dataclass
class JobSpec:
    """DM-001 -- top-level job specification.

    Field set drawn verbatim from the roadmap DM-001 row
    (``.dev/releases/Current/MultiModelSwarm/roadmap.md`` line 88):
    spec_version, job_id, created, caller, lens, custom_prompt_dir?,
    workers, transport, prompt, target, normalization, output,
    amalgamation_mode, status_policy, recommended_next_command_template,
    recommended_next_command_substitutions, runtime.

    Defaults exist solely so the aggregator's no-arg round-trip suite
    (``tests/swarm/test_models_round_trip.py``) keeps passing while
    downstream tasks T01.14..T01.28 fill in the nested dataclass field
    sets. Cross-field validation (NFR-006 spec_version forward-compat,
    §11.5 prompt substring, etc.) is the schema layer's job (COMP-005,
    T02.03), not this dataclass.

    Nested-dataclass defaults use ``default_factory=lambda: Cls()`` so
    forward references to classes declared later in this module resolve
    at call time rather than class-decoration time.
    """

    spec_version: str = ""
    job_id: str = ""
    created: str = ""
    caller: "CallerInfo" = field(default_factory=lambda: CallerInfo())
    lens: str = ""
    custom_prompt_dir: Optional[str] = None
    workers: "WorkerSpec" = field(default_factory=lambda: WorkerSpec())
    transport: "TransportSpec" = field(default_factory=lambda: TransportSpec())
    prompt: "PromptSpec" = field(default_factory=lambda: PromptSpec())
    target: "TargetSpec" = field(default_factory=lambda: TargetSpec())
    normalization: "NormalizationSpec" = field(
        default_factory=lambda: NormalizationSpec()
    )
    output: "OutputSpec" = field(default_factory=lambda: OutputSpec())
    amalgamation_mode: AmalgamationMode = "normalize+merge"
    status_policy: "StatusPolicy" = field(default_factory=lambda: StatusPolicy())
    recommended_next_command_template: str = ""
    recommended_next_command_substitutions: dict[str, str] = field(
        default_factory=dict
    )
    runtime: "RuntimeSpec" = field(default_factory=lambda: RuntimeSpec())


@dataclass
class RetryPolicy:
    """Nested retry-policy substructure for ``WorkerSpec`` (DM-002).

    Field set drawn from the roadmap DM-002 row
    (``.dev/releases/Current/MultiModelSwarm/roadmap.md`` line 89):
    ``retry.on_5xx:bool; retry.on_5xx_backoff_sec:int; retry.on_4xx:bool;
    retry.on_timeout:bool``. Defaults encode FR-017 / NFR-011 (5xx
    retry-once with backoff; 4xx / timeout / network no retry) and match
    ``merged-requirements.compressed.compressed.md`` L283.

    Carried inline on ``WorkerSpec`` rather than as its own DM-### record
    because the roadmap row models it as a sub-field of WorkerSpec, not
    an independent record.
    """

    on_5xx: bool = True
    on_5xx_backoff_sec: int = 2
    on_4xx: bool = False
    on_timeout: bool = False


@dataclass
class WorkerSpec:
    """DM-002 -- worker configuration dataclass.

    Field set drawn verbatim from the roadmap DM-002 row
    (``.dev/releases/Current/MultiModelSwarm/roadmap.md`` line 89):
    count:int, models:list[str], timeout_sec:int, temperature:float,
    retry.on_5xx:bool, retry.on_5xx_backoff_sec:int, retry.on_4xx:bool,
    retry.on_timeout:bool.

    Defaults:
        - ``timeout_sec=180`` per NFR-010 (per-worker hard timeout).
        - ``temperature=0.2`` per ``roadmap-haiku-architect.md`` L100
          recipe defaults.
        - ``count=4`` to match the typical LENSES ``default_workers``
          (compatible with StatusPolicy floor=2).
        - ``models=[]`` (empty list -- lens expansion fills this at
          preflight per FR-020).
        - ``retry`` defaults to FR-017 / NFR-011 policy via
          :class:`RetryPolicy`.

    Validation (``__post_init__``):
        - ``timeout_sec`` must be non-negative; negative values raise
          ``ValueError`` (acceptance criterion T01.14).

    Cross-field schema validation (count vs model pool size, etc.) is
    the COMP-005 schema layer's job (M2), not this dataclass.
    """

    count: int = 4
    models: list[str] = field(default_factory=list)
    timeout_sec: int = 180
    temperature: float = 0.2
    retry: "RetryPolicy" = field(default_factory=lambda: RetryPolicy())

    def __post_init__(self) -> None:
        if self.timeout_sec < 0:
            raise ValueError(
                f"WorkerSpec.timeout_sec must be non-negative, "
                f"got {self.timeout_sec}"
            )


@dataclass
class Truncation:
    """Nested truncation substructure for ``TargetSpec`` (DM-003).

    Field set drawn from the roadmap DM-003 row
    (``.dev/releases/Current/MultiModelSwarm/roadmap.md`` line 90):
    ``truncation.line_cap:int; truncation.byte_floor:int``. Defaults
    sourced from ``roadmap-haiku-architect.md`` L113 (FR-SPEC-005) and
    L200 (IMM-4 empty-target guard): ``line_cap=4000``, ``byte_floor=50``.

    Carried inline on ``TargetSpec`` rather than as its own DM-### record
    because the roadmap row models it as a dotted sub-field of TargetSpec,
    not an independent record.
    """

    line_cap: int = 4000
    byte_floor: int = 50


@dataclass
class Delimiters:
    """Nested delimiter substructure for ``TargetSpec`` (DM-003).

    Field set drawn from the roadmap DM-003 row
    (``.dev/releases/Current/MultiModelSwarm/roadmap.md`` line 90):
    ``delimiters.open:str; delimiters.close:str``. Defaults sourced from
    §11.5 (``merged-requirements.compressed.compressed.md`` L58) and
    T01.15 acceptance criteria: ``<<<TARGET>>>`` / ``<<<END TARGET>>>``.

    These delimiters wrap the ingested target block at preflight (COMP-005
    enforcement, M2) to enforce data-vs-instructions separation across all
    three prompt-input paths (lens / JSON-Schema / custom-prompt-dir).
    """

    open: str = "<<<TARGET>>>"
    close: str = "<<<END TARGET>>>"


@dataclass
class InjectionGuard:
    """Nested injection-guard substructure for ``TargetSpec`` (DM-003).

    Field set drawn from the roadmap DM-003 row
    (``.dev/releases/Current/MultiModelSwarm/roadmap.md`` line 90):
    ``injection_guard.enabled:bool; injection_guard.required_substring:str``.
    Defaults sourced from ``roadmap-haiku-architect.md`` L113 (FR-SPEC-005):
    ``enabled=True``. ``required_substring`` defaults to ``""``; the
    canonical §11.5 sentence is resolved/enforced at the schema + preflight
    layer (COMP-005, T02.03) where the cross-field rule against
    ``prompt.system`` lives -- not at the dataclass level.
    """

    enabled: bool = True
    required_substring: str = ""


@dataclass
class TargetSpec:
    """DM-003 -- target ingestion config dataclass.

    Field set drawn verbatim from the roadmap DM-003 row
    (``.dev/releases/Current/MultiModelSwarm/roadmap.md`` line 90):
    ``kind:str; path:str; truncation.line_cap:int; truncation.byte_floor:int;
    delimiters.open:str; delimiters.close:str; injection_guard.enabled:bool;
    injection_guard.required_substring:str``.

    The four dotted sub-fields collapse into three nested dataclasses
    (:class:`Truncation`, :class:`Delimiters`, :class:`InjectionGuard`),
    same pattern as :class:`RetryPolicy` on :class:`WorkerSpec`.

    Defaults:
        - ``kind="file"`` -- most common ingestion path; schema layer
          (M2) constrains to ``{file, inline_text, inline_bytes_b64}``
          per ``roadmap-haiku-architect.md`` L113. The dataclass field
          is typed ``str`` to match the DM-003 row verbatim.
        - ``path=""`` -- caller supplies at construction.
        - ``truncation`` -- FR-SPEC-005 defaults (line_cap=4000,
          byte_floor=50).
        - ``delimiters`` -- §11.5 canonical wrapping
          (``<<<TARGET>>>`` / ``<<<END TARGET>>>``).
        - ``injection_guard`` -- enabled by default; required_substring
          defaults to empty (schema layer enforces canonical §11.5
          sentence at preflight, COMP-005 / T02.03).

    Cross-field validation (kind/path consistency, substring presence,
    byte-floor STOP per IMM-4) is the COMP-005 schema layer's job
    (M2 / T02.03), not this dataclass.
    """

    kind: str = "file"
    path: str = ""
    truncation: "Truncation" = field(default_factory=lambda: Truncation())
    delimiters: "Delimiters" = field(default_factory=lambda: Delimiters())
    injection_guard: "InjectionGuard" = field(
        default_factory=lambda: InjectionGuard()
    )


@dataclass
class TransportSpec:
    """DM-004 -- transport config dataclass.

    Field set drawn verbatim from the roadmap DM-004 row
    (``.dev/releases/Current/MultiModelSwarm/roadmap.md`` line 91):
    ``kind:str; base_url_env:str; api_key_env:str``.

    Defaults sourced from FR-SPEC-004 (``roadmap-haiku-architect.md`` L112)
    and AC-017 (``roadmap-sonnet-architect.md`` L73): the Phase-1 reference
    transport is ``openai_compat`` routed through the T2 proxy, with the
    base URL and API key resolved at dispatch time from ``T2ProxyUrl`` and
    ``T2ProxyKey`` env vars respectively (NFR-SEC-005 -- no provider keys
    in repo or job spec).

    Defaults:
        - ``kind="openai_compat"`` -- Phase-1 reference transport
          (FR-SPEC-004 / FR-022). The schema layer (M2) constrains to
          ``{openai_compat, stub}`` via :data:`TransportKind`; the stub
          transport (COMP-033) is the deterministic CI path.
        - ``base_url_env="T2ProxyUrl"`` -- T2 proxy URL env-var name.
        - ``api_key_env="T2ProxyKey"`` -- T2 proxy API-key env-var name.

    Validation (``__post_init__``):
        - ``kind`` must be one of the values declared by :data:`TransportKind`;
          arbitrary strings raise ``ValueError`` (T01.16 acceptance:
          ``kind="bogus"`` raises). This is the dataclass-level guard;
          schema-time enforcement is duplicated at COMP-005 (M2) for the
          JSON-Schema validator surface.
        - ``base_url_env`` and ``api_key_env`` must be non-empty strings;
          empty values raise ``ValueError`` (T01.16 acceptance: env-var
          name validation rejects empty strings). Stricter rules
          (POSIX-conformant identifier shape, no whitespace) are the
          schema layer's job (COMP-005), not this dataclass.

    Cross-field validation (transport.kind requiring transport-specific
    env vars, NFR-SEC-005 secret routing) lives in COMP-005 (M2) and the
    transport implementations in M3 (COMP-031..033).
    """

    kind: TransportKind = "openai_compat"
    base_url_env: str = "T2ProxyUrl"
    api_key_env: str = "T2ProxyKey"

    def __post_init__(self) -> None:
        allowed_kinds = typing.get_args(TransportKind)
        if self.kind not in allowed_kinds:
            raise ValueError(
                f"TransportSpec.kind must be one of {allowed_kinds}, "
                f"got {self.kind!r}"
            )
        if not isinstance(self.base_url_env, str) or not self.base_url_env:
            raise ValueError(
                "TransportSpec.base_url_env must be a non-empty string, "
                f"got {self.base_url_env!r}"
            )
        if not isinstance(self.api_key_env, str) or not self.api_key_env:
            raise ValueError(
                "TransportSpec.api_key_env must be a non-empty string, "
                f"got {self.api_key_env!r}"
            )


@dataclass
class PromptSpec:
    """DM-005 -- verbatim prompt definition dataclass.

    Field set drawn verbatim from the roadmap DM-005 row
    (``.dev/releases/Current/MultiModelSwarm/roadmap.md`` line 92):
    ``system:str(verbatim); user_template:str(verbatim); variables:dict``.

    The ``system`` and ``user_template`` fields are **verbatim** strings:
    whitespace (leading, trailing, internal, newline runs) is preserved
    exactly through the round-trip (T01.17 acceptance:
    "round-trip diff empty including newlines"). The dataclass performs
    **no** normalization, trimming, or substring enforcement -- those are
    the schema layer's job (COMP-005, T02.03) where the §11.5
    required-substring rule against ``injection_guard.required_substring``
    is enforced cross-field.

    Defaults:
        - ``system=""`` -- caller / lens supplies at construction or via
          ``FR-020`` lens-driven defaults expansion at preflight.
        - ``user_template=""`` -- caller / lens supplies; downstream
          substitution against ``variables`` happens at dispatch time
          (M3 transport layer).
        - ``variables={}`` -- empty dict; expansion at dispatch fills
          template placeholders. Values are arbitrary
          (JSON-serializable; the schema layer validates).

    Cross-field validation (the §11.5 required-substring on
    ``prompt.system`` against ``target.injection_guard.required_substring``,
    template placeholder coverage vs ``variables`` keys) is the COMP-005
    schema layer's responsibility (M2 / T02.03), not this dataclass.
    """

    system: str = ""
    user_template: str = ""
    variables: dict[str, Any] = field(default_factory=dict)


@dataclass
class OnParseError:
    """Nested parse-error policy substructure for ``NormalizationSpec`` (DM-006).

    Field set drawn from the roadmap DM-006 row
    (``.dev/releases/Current/MultiModelSwarm/roadmap.md`` line 93):
    ``on_parse_error.salvage:bool; on_parse_error.retain_raw:bool``. Defaults
    sourced from §4.1 spec block
    (``merged-requirements.compressed.compressed.md`` L310):
    ``on_parse_error: { salvage: true, retain_raw: true }``.

    Carried inline on ``NormalizationSpec`` rather than as its own DM-### record
    because the roadmap row models it as a dotted sub-field of NormalizationSpec,
    not an independent record (same pattern as :class:`RetryPolicy` on
    :class:`WorkerSpec` and :class:`Truncation` / :class:`Delimiters` /
    :class:`InjectionGuard` on :class:`TargetSpec`).

    Semantics (FR-028 / §7.4, enforced in Wave 2 -- COMP-008, M4):
        - ``salvage=True`` -- Wave 2 may promote ``parse_error -> success``
          when §7.4 salvage conditions are met (e.g. recoverable shape).
        - ``retain_raw=True`` -- raw worker output is preserved on the
          per-worker meta sidecar regardless of normalization outcome,
          so callers can audit salvage provenance.
    """

    salvage: bool = True
    retain_raw: bool = True


@dataclass
class NormalizationSpec:
    """DM-006 -- normalization config dataclass.

    Field set drawn verbatim from the roadmap DM-006 row
    (``.dev/releases/Current/MultiModelSwarm/roadmap.md`` line 93):
    ``recipe:str; template_path:str; schema_version:str; recipe_args:dict;
    on_parse_error.salvage:bool; on_parse_error.retain_raw:bool``.

    The two dotted sub-fields collapse into a nested :class:`OnParseError`
    dataclass, same pattern as :class:`RetryPolicy` on :class:`WorkerSpec`.

    Defaults:
        - ``recipe=""`` -- caller / lens supplies at construction; FR-020
          lens-driven defaults expansion at preflight populates this from
          ``LENSES[lens].recipe_name`` (§4.2 mapping).
        - ``template_path=""`` -- caller / lens supplies; preflight expands
          from ``LENSES[lens].output_template_path`` (§4.2 mapping).
        - ``schema_version="1.0"`` per §4.1 spec block default
          (``merged-requirements.compressed.compressed.md`` L308).
        - ``recipe_args={}`` -- recipe-specific kwargs; recipe owns shape.
        - ``on_parse_error`` -- §7.4 salvage policy defaults
          (``salvage=True``, ``retain_raw=True``).

    Cross-field validation (recipe-name resolution against the M4 recipe
    REGISTRY -- COMP-015 / COMP-021 -- including ``custom-py:module:func``
    dynamic loading) is the schema layer's job (COMP-005, M2) and the
    lens validator's job (COMP-023), not this dataclass. T01.19 acceptance:
    "Validation rejects unknown recipe names at schema time (covered M2)."
    """

    recipe: str = ""
    template_path: str = ""
    schema_version: str = "1.0"
    recipe_args: dict[str, Any] = field(default_factory=dict)
    on_parse_error: "OnParseError" = field(default_factory=lambda: OnParseError())


@dataclass
class OutputSpec:
    """DM-007 -- output config dataclass.

    Field set drawn verbatim from the roadmap DM-007 row
    (``.dev/releases/Current/MultiModelSwarm/roadmap.md`` line 94):
    ``dir:str; filename_template:str; lens_name:str; atomic_write:bool;
    emit_meta_sidecar:bool``.

    Defaults sourced from §4.1 spec block
    (``merged-requirements.compressed.compressed.md`` L312-L318) and FR-020
    lens-driven defaults expansion (L347-L348):

        - ``dir=""`` -- caller supplies an absolute path at construction;
          schema layer (COMP-005, M2) validates non-empty + abs-path shape,
          and the output writer (M3) enforces path-confinement against the
          job's output root (NFR-013). T01.20 explicitly defers path
          confinement to M3.
        - ``filename_template="{lens}-{index:02d}-{model_slug}.md"`` --
          §4.1 canonical template. FR-020 expansion re-applies this same
          value when a registry lens is in use; carrying it as the
          dataclass default keeps custom-prompt-dir / JSON-Schema callers
          on the same naming convention without requiring expansion.
        - ``lens_name=""`` -- propagated from the job's ``lens`` field at
          preflight (FR-020 / §4.2 mapping), not supplied at dataclass
          construction. The empty default lets the round-trip suite build
          a no-arg instance.
        - ``atomic_write=True`` -- IMM-6 alignment (T01.20 acceptance).
          Every output write goes through write-to-tmp + ``os.replace``
          with a deterministic filename so a mid-write kill never leaves a
          partial file and rerun is idempotent (FR-027, COMP-011).
        - ``emit_meta_sidecar=True`` -- §4.1 default. Per-worker meta
          sidecar (``*.meta.json``) carries provenance (transport, model,
          attempts, status, raw retention pointer when ``retain_raw=True``
          on :class:`OnParseError`).

    Cross-field validation (path confinement of ``dir`` and rendered
    filename against the job's output root per NFR-013, template-placeholder
    coverage for ``{lens}``/``{index}``/``{model_slug}``) is the output
    writer's job in M3, not this dataclass. T01.20 acceptance:
    "Path-confinement validation deferred to M3 (NFR-013)."
    """

    dir: str = ""
    filename_template: str = "{lens}-{index:02d}-{model_slug}.md"
    lens_name: str = ""
    atomic_write: bool = True
    emit_meta_sidecar: bool = True


@dataclass
class StatusPolicy:
    """DM-008 -- status determination policy dataclass.

    Field set drawn verbatim from the roadmap DM-008 row
    (``.dev/releases/Current/MultiModelSwarm/roadmap.md`` line 95):
    ``floor:int; success_first:bool; partial_threshold:int``.

    Defaults sourced from IMM-5 (``.dev/releases/Current/MultiModelSwarm/
    roadmap.md`` line 313):

        - ``floor=2`` -- minimum successful worker count for ``partial``
          status. Below this floor the job is ``failed`` regardless of M
          (``M<2`` -> failed).
        - ``success_first=True`` -- IMM-5 tie-break for ``M==N==2``
          resolves to ``success`` (not ``partial``) when this flag is on.
        - ``partial_threshold=2`` -- ``2 <= M < N`` window produces
          ``partial`` status. Lower bound mirrors ``floor``; carried as
          a separate field so callers can tune partial-vs-failed
          independently from the failed-floor (T01.21 acceptance).

    IMM-5 status matrix (enforced by Wave 3 reduce -- COMP-009, M5):
        - ``M == N``                   -> ``success``
        - ``2 <= M < N``               -> ``partial``
        - ``M < 2``                    -> ``failed``
        - ``M == N == 2 && success_first`` -> ``success`` (tie-break)

    Cross-field validation (consistency between ``floor`` and
    ``partial_threshold``, non-negative window) is the COMP-005 schema
    layer's job (M2), not this dataclass.
    """

    floor: int = 2
    success_first: bool = True
    partial_threshold: int = 2


@dataclass
class OnCompletion:
    """Nested completion-side policy substructure for ``RuntimeSpec`` (DM-009).

    Field set drawn from the roadmap DM-009 row
    (``.dev/releases/Current/MultiModelSwarm/roadmap.md`` line 96):
    ``on_completion.write_done_sentinel:bool;
    on_completion.print_contract_to_stdout:bool``. Defaults sourced from
    §4.1 spec block (``merged-requirements.compressed.compressed.md`` L334)
    and FR-SPEC-007 (``roadmap-haiku-architect.md`` L115):
    ``on_completion: { write_done_sentinel: true, print_contract_to_stdout: true }``.

    Carried inline on ``RuntimeSpec`` rather than as its own DM-### record
    because the roadmap row models it as a dotted sub-field of RuntimeSpec,
    not an independent record (same pattern as :class:`RetryPolicy` on
    :class:`WorkerSpec` and :class:`OnParseError` on :class:`NormalizationSpec`).

    Semantics (FR-029 / §10, enforced in M7 -- COMP-013):
        - ``write_done_sentinel=True`` -- on terminal status the executor
          writes a ``done.json`` (DM-017) atomically; absent in detached
          runs would mean ``swarm attach`` cannot tell the job finished.
        - ``print_contract_to_stdout=True`` -- the final ResultContract
          (DM-012) is printed to stdout so non-Claude callers
          (``subprocess.run(...)``, FR-030) can parse it without reading
          artifacts off disk.
    """

    write_done_sentinel: bool = True
    print_contract_to_stdout: bool = True


@dataclass
class RuntimeSpec:
    """DM-009 -- runtime config dataclass.

    Field set drawn verbatim from the roadmap DM-009 row
    (``.dev/releases/Current/MultiModelSwarm/roadmap.md`` line 96):
    ``mode:enum(inline/detached); log_level:str;
    on_completion.write_done_sentinel:bool;
    on_completion.print_contract_to_stdout:bool``.

    The two dotted sub-fields collapse into a nested :class:`OnCompletion`
    dataclass, same pattern as :class:`RetryPolicy` on :class:`WorkerSpec`.

    Defaults sourced from §4.1 spec block
    (``merged-requirements.compressed.compressed.md`` L331-L334) and
    FR-SPEC-007 (``roadmap-haiku-architect.md`` L115):

        - ``mode="inline"`` -- T01.22 acceptance (M7 detached mode is
          opt-in). Inline runs return the contract synchronously to the
          caller; detached runs are tmux-backed and survive caller death
          (AC-008 / AC-013 / FR-014).
        - ``log_level="info"`` -- §4.1 spec block default. Schema layer
          (COMP-005, M2) validates against a closed enum (debug/info/
          warn/error); the dataclass field is typed ``str`` to match the
          DM-009 row verbatim.
        - ``on_completion`` -- §4.1 defaults (write_done_sentinel=True,
          print_contract_to_stdout=True) via :class:`OnCompletion`.

    Validation (``__post_init__``):
        - ``mode`` must be one of the values declared by :data:`RuntimeMode`;
          arbitrary strings raise ``ValueError`` (T01.22 acceptance:
          "Mode-validation test"). This is the dataclass-level guard;
          schema-time enforcement is duplicated at COMP-005 (M2) for the
          JSON-Schema validator surface.

    Cross-field validation (mode=detached requiring tmux availability per
    AC-008, log_level enum membership, on_completion semantics) is the
    COMP-005 schema layer's job (M2) and the tmux wrapper's job in M7
    (COMP-014), not this dataclass.
    """

    mode: RuntimeMode = "inline"
    log_level: str = "info"
    on_completion: "OnCompletion" = field(default_factory=lambda: OnCompletion())

    def __post_init__(self) -> None:
        allowed_modes = typing.get_args(RuntimeMode)
        if self.mode not in allowed_modes:
            raise ValueError(
                f"RuntimeSpec.mode must be one of {allowed_modes}, "
                f"got {self.mode!r}"
            )


@dataclass
class LensEntry:
    """DM-010 -- lens registry entry dataclass.

    Field set drawn verbatim from the roadmap DM-010 row
    (``.dev/releases/Current/MultiModelSwarm/roadmap.md`` line 97):
    ``name:str; description:str; system_prompt_fragment:str;
    user_template:str; output_template_path:str; recipe_name:str;
    default_workers:int; default_target_line_cap:int; suspect:bool;
    tier:str; recommended_next_command_template:str; acceptance_notes:str;
    stability:enum(stable/experimental)``.

    Anti-instinct remediation row 17a (roadmap line 151,
    FR-LENSREG.NS / T02.21) appends a sixth lens-validator contract
    field, ``normalizer_strategy:str``. The field names the prompt's
    expected output shape; the COMP-023 validator's sixth assertion
    rejects any entry whose ``normalizer_strategy`` is empty or does
    not resolve against a registered recipe. The roadmap §6.4 lens
    registry row links to this field by deliverable D-0043.

    LensEntry is the schema-bearing registry record consumed by Wave 0
    preflight (FR-020 lens-driven defaults expansion) and snapshot into
    :class:`Manifest` via :class:`ResolvedLensEntry` (INV-001 / INV-016).
    Each built-in lens (COMP-024..030) ships an instance assembled in
    ``cli/swarm/lenses/<name>.py`` and registered into the ``LENSES``
    dict (COMP-022). The lens validator (COMP-023, T03+ U-008) enforces
    cross-field assertions (file refs resolve, recipe_name registered,
    ``suspect`` ↔ ``suspect_files`` coupling in next-command template,
    name uniqueness, §11.5 substring in ``system_prompt_fragment``) at
    ``swarm validate-lenses`` time -- not at dataclass construction.

    Defaults:
        - ``name=""`` / ``description=""`` / ``system_prompt_fragment=""``
          / ``user_template=""`` / ``output_template_path=""``
          / ``recipe_name=""`` / ``tier=""``
          / ``recommended_next_command_template=""`` / ``acceptance_notes=""``
          -- each built-in lens (COMP-024..030) supplies these at module
          load. The empty defaults exist so the aggregator's no-arg
          round-trip suite keeps passing.
        - ``default_workers=3`` -- matches the most common built-in lens
          (bare_review, refactor_find, spec_completeness, feasibility_probe,
          doc_completeness all use 3; edge_case_hunt + troubleshoot_hypothesis
          override to 4 per COMP-024..030 rows). Compatible with
          :class:`StatusPolicy` ``floor=2``.
        - ``default_target_line_cap=4000`` -- mirrors :class:`Truncation`
          default (FR-SPEC-005). Lenses may override per their domain
          (e.g. doc_completeness may carry a higher cap).
        - ``suspect=False`` -- conservative default; lenses opt in
          explicitly (bare_review is the canonical ``suspect=True`` lens
          per COMP-024). The suspect flag triggers the §FR-020 /
          NFR-012 review discipline and propagates into
          ``CallerMetadata`` (DM-020) per OQ-009 precedence.
        - ``stability="stable"`` -- conservative default; experimental
          lenses (refactor_find per COMP-025) opt in explicitly.

    Validation (``__post_init__``):
        - ``stability`` must be one of the values declared by
          :data:`Stability`; arbitrary strings raise ``ValueError``.
          This is the dataclass-level guard; the M2 schema layer
          (COMP-005) duplicates this constraint at JSON-Schema time and
          the lens validator (COMP-023) reinforces it at
          ``swarm validate-lenses`` time.

    Cross-field validation (§11.5 substring in ``system_prompt_fragment``,
    ``suspect`` ↔ ``{suspect_files}`` placeholder coupling in
    ``recommended_next_command_template``, ``recipe_name`` resolution
    against the M4 recipe REGISTRY, ``normalizer_strategy`` resolution
    against the same registry per FR-LENSREG.NS / T02.21) is the
    COMP-023 lens validator's job, not this dataclass.
    """

    name: str = ""
    description: str = ""
    system_prompt_fragment: str = ""
    user_template: str = ""
    output_template_path: str = ""
    recipe_name: str = ""
    normalizer_strategy: str = ""
    default_workers: int = 3
    default_target_line_cap: int = 4000
    suspect: bool = False
    tier: str = ""
    recommended_next_command_template: str = ""
    acceptance_notes: str = ""
    stability: Stability = "stable"

    def __post_init__(self) -> None:
        allowed_stability = typing.get_args(Stability)
        if self.stability not in allowed_stability:
            raise ValueError(
                f"LensEntry.stability must be one of {allowed_stability}, "
                f"got {self.stability!r}"
            )


@dataclass
class ResolvedLensEntry:
    """DM-011 -- immutable lens snapshot captured in manifest.json.

    Field set drawn verbatim from the roadmap DM-011 row
    (``.dev/releases/Current/MultiModelSwarm/roadmap.md`` line 98):
    ``name:str; system_prompt_fragment:str; user_template:str;
    recipe_name:str; default_workers:int; suspect:bool; tier:str;
    recommended_next_command_template:str; stability:str``.

    ResolvedLensEntry is the **immutable snapshot** of the LensEntry
    selected at Wave 0 preflight. It is embedded into :class:`Manifest`
    (DM-016, T01.27) and persisted as part of ``manifest.json`` so the
    INV-001 / INV-016 source-of-truth contract holds: once a job is
    accepted, the exact lens fragment + template + recipe binding used
    to drive workers is preserved byte-for-byte regardless of any later
    edits to the LensEntry registry (COMP-022). M6 resume reads this
    snapshot rather than re-resolving the lens.

    The DM-011 field set is intentionally **narrower** than DM-010
    (LensEntry): registry-only metadata that does not affect execution
    is omitted from the snapshot. The four LensEntry fields excluded
    here are:

        - ``description`` -- human-facing registry metadata, not used at
          dispatch.
        - ``output_template_path`` -- already expanded into
          :class:`NormalizationSpec` ``template_path`` at preflight, so
          the manifest carries the resolved path on NormalizationSpec.
        - ``default_target_line_cap`` -- already expanded into
          :class:`Truncation` ``line_cap`` at preflight.
        - ``acceptance_notes`` -- COMP-023 lens-validator advisory text,
          not consumed at runtime.

    Defaults:
        - All fields default to the empty / zero / ``False`` / ``"stable"``
          values mirroring LensEntry's defaults, so the aggregator's
          no-arg round-trip suite (``tests/swarm/test_models_round_trip.py``)
          continues to pass. Real instances are built via
          :meth:`from_lens` at preflight, never via no-arg construction.
        - ``default_workers=3`` mirrors LensEntry's default (most common
          built-in lens count; compatible with StatusPolicy floor=2).

    Typing note:
        The roadmap row spells ``stability`` as ``str``, but every legal
        value flows in from a LensEntry where ``stability`` is the
        :data:`Stability` Literal. Carrying the Literal here too keeps
        the snapshot's type contract aligned with its source and lets
        the same out-of-enum guard (``__post_init__``) reject any
        manually-constructed snapshot that drifts from the LensEntry
        invariant. The JSON round-trip is unaffected (Literal serializes
        as its string value).

    Validation (``__post_init__``):
        - ``stability`` must be one of the values declared by
          :data:`Stability`; arbitrary strings raise ``ValueError``.
          Mirrors the LensEntry guard so a manually-constructed snapshot
          cannot smuggle an out-of-enum value into ``manifest.json``.
    """

    name: str = ""
    system_prompt_fragment: str = ""
    user_template: str = ""
    recipe_name: str = ""
    default_workers: int = 3
    suspect: bool = False
    tier: str = ""
    recommended_next_command_template: str = ""
    stability: Stability = "stable"

    def __post_init__(self) -> None:
        allowed_stability = typing.get_args(Stability)
        if self.stability not in allowed_stability:
            raise ValueError(
                f"ResolvedLensEntry.stability must be one of {allowed_stability}, "
                f"got {self.stability!r}"
            )

    @classmethod
    def from_lens(cls, entry: "LensEntry") -> "ResolvedLensEntry":
        """Build a snapshot from a :class:`LensEntry` at Wave 0 preflight.

        Copies only the nine fields named on the DM-011 roadmap row. The
        four LensEntry registry-only fields (``description``,
        ``output_template_path``, ``default_target_line_cap``,
        ``acceptance_notes``) are intentionally not propagated -- they
        either don't affect execution (``description`` /
        ``acceptance_notes``) or are already expanded into nested
        :class:`NormalizationSpec` / :class:`Truncation` fields at
        preflight (``output_template_path`` /
        ``default_target_line_cap``).

        The result is a fresh, independently-owned dataclass instance:
        editing the originating LensEntry after this call does not
        mutate the snapshot. This is the INV-001 / INV-016 anchor --
        ``manifest.json`` carries the exact lens definition used at
        dispatch even if the registry is hot-reloaded mid-run.
        """
        return cls(
            name=entry.name,
            system_prompt_fragment=entry.system_prompt_fragment,
            user_template=entry.user_template,
            recipe_name=entry.recipe_name,
            default_workers=entry.default_workers,
            suspect=entry.suspect,
            tier=entry.tier,
            recommended_next_command_template=entry.recommended_next_command_template,
            stability=entry.stability,
        )


@dataclass
class ContractTarget:
    """Nested target substructure for ``ResultContract`` (DM-012).

    Field set drawn from the roadmap DM-012 row
    (``.dev/releases/Current/MultiModelSwarm/roadmap.md`` line 99):
    ``target.path:str; target.checksum:str; target.truncated:bool;
    target.truncation_line_cap:int``. Defaults sourced from §5 Result
    Contract Schema (``merged-requirements.compressed.compressed.md`` L377-L381):
    ``path``/``checksum`` are caller-supplied at contract-emit time,
    ``truncated`` defaults False, ``truncation_line_cap`` mirrors the
    :class:`Truncation` default (FR-SPEC-005 / 4000).

    Carried inline on :class:`ResultContract` rather than as its own
    DM-### record because the roadmap row models the four ``target.*``
    sub-fields as a single dotted block (same pattern as :class:`RetryPolicy`
    on :class:`WorkerSpec` and :class:`Truncation` / :class:`Delimiters` /
    :class:`InjectionGuard` on :class:`TargetSpec`).

    This record describes the **post-execution snapshot** of the target
    that was actually fanned out to workers (path of the ingested file,
    sha256 checksum truncated to 12 hex chars per §5, whether the
    Wave-0 truncation policy fired, and the line cap that policy used).
    It is intentionally narrower than :class:`TargetSpec` (which carries
    the *intent* at job-spec time, including delimiters + injection-guard
    policy) so the contract surface remains stable as TargetSpec evolves.
    """

    path: str = ""
    checksum: str = ""
    truncated: bool = False
    truncation_line_cap: int = 4000


@dataclass(frozen=True)
class ResultContract:
    """DM-012 -- final job result contract dataclass.

    Field set drawn verbatim from the roadmap DM-012 row
    (``.dev/releases/Current/MultiModelSwarm/roadmap.md`` line 99):
    ``contract_version:str; status:enum; job_id:str; started:str;
    finished:str; elapsed_ms:int; caller:CallerInfo; lens:str;
    lens_source:str; target.path:str; target.checksum:str;
    target.truncated:bool; target.truncation_line_cap:int;
    workers_requested:int; workers_succeeded:int; workers_failed:int;
    output_files:list[WorkerResult]; amalgamation_mode:str;
    merged_path:str?; caller_metadata:CallerMetadata;
    recommended_next_command:str; artifacts:Artifacts``.

    The four dotted ``target.*`` sub-fields collapse into a single
    nested :class:`ContractTarget` dataclass, same pattern as
    :class:`RetryPolicy` on :class:`WorkerSpec` and :class:`OnCompletion`
    on :class:`RuntimeSpec`. After the collapse the contract carries
    **19 top-level keys** -- one per record listed in the acceptance
    block of T01.25 (the validation line referring to "18 top-level
    keys" is an off-by-one in the phase tasklist; the acceptance
    enumeration itself names 19 records, and the field-completeness
    test below pins 19 to match the enumeration).

    ResultContract is the **caller-facing terminal artifact** emitted at
    Wave 3 reduce (COMP-009, M5) per FR-018. It is written to
    ``return-contract.yaml`` and -- when ``RuntimeSpec.on_completion.
    print_contract_to_stdout`` is True -- printed to stdout so non-Claude
    callers (``subprocess.run(...)``, FR-030) can parse it without reading
    artifacts off disk. The done-sentinel (:class:`DoneSentinel`,
    DM-017) points back at the contract path so detached / tmux callers
    (FR-014) can locate it after the executor exits.

    Defaults:
        - ``contract_version="1.0"`` -- §5 spec block default
          (``merged-requirements.compressed.compressed.md`` L366).
          Mirrors the manifest contract_version (T01.27) so a
          ``return-contract.yaml`` and its manifest carry the same
          schema version.
        - ``status="success"`` -- conservative default so the no-arg
          round-trip suite (``tests/swarm/test_models_round_trip.py``)
          keeps passing. Real instances are constructed at Wave 3 reduce
          where IMM-5 (M==N -> success; 2 <= M < N -> partial; M < 2 ->
          failed; M==N==2 && success_first -> success) determines the
          value (COMP-009).
        - ``job_id`` / ``started`` / ``finished`` -- caller / executor
          supplies at contract-emit time; empty defaults satisfy the
          no-arg round-trip.
        - ``elapsed_ms=0`` -- executor stamps the finished-minus-started
          delta at contract-emit time.
        - ``caller`` -- defaults to a stub :class:`CallerInfo` (fields
          land in T01.28). The CallerInfo carried here is the same
          caller record copied from the originating :class:`JobSpec`.
        - ``lens="" / lens_source=""`` -- §5 spec block notes both may
          be null when the job was driven by a JSON-Schema spec without
          a registered lens. Empty string represents "not set" so the
          dataclass field can stay typed ``str`` to match the roadmap
          row verbatim (rather than ``Optional[str]``). Schema layer
          (M2) validates lens_source against ``{"", "registry",
          "custom"}`` at contract-emit time.
        - ``target`` -- defaults to a stub :class:`ContractTarget`;
          real values stamped at reduce.
        - ``workers_requested`` / ``workers_succeeded`` /
          ``workers_failed`` -- counts stamped at reduce; default 0.
          INV-005 invariant: ``workers_succeeded + workers_failed ==
          workers_requested`` (enforced at the emitter, not this
          dataclass).
        - ``output_files=[]`` -- list of :class:`WorkerResult` entries
          stamped by the dispatcher (M3). Empty default satisfies the
          no-arg round-trip; the round-trip helpers (``from_dict``)
          recurse into ``list[<dataclass>]`` payloads so populated lists
          rebuild as dataclass instances rather than raw dicts.
        - ``amalgamation_mode="normalize+merge"`` -- mirrors
          :class:`JobSpec` default per §4.1 (full pipeline). The roadmap
          row spells the type as ``str``, but every legal value here
          flows in from JobSpec where the field is :data:`AmalgamationMode`;
          carrying the Literal here keeps the contract's type contract
          aligned with its source and lets schema-time validation
          (COMP-005, M2) catch any drift before the contract is emitted.
        - ``merged_path=None`` -- §5 spec block: null when
          ``amalgamation_mode != "normalize+merge"`` or workers_succeeded
          < 2. The roadmap row spells this as ``merged_path:str?`` --
          modeled here as ``Optional[str]``.
        - ``caller_metadata`` -- defaults to a stub :class:`CallerMetadata`
          (DM-020 lands in M2). FR-020 expansion stamps ``suspect`` and
          ``tier`` from the resolved lens at preflight; caller-supplied
          values override per OQ-009 precedence.
        - ``recommended_next_command=""`` -- the **rendered** template
          (substitutions applied), in contrast to JobSpec's
          ``recommended_next_command_template`` (unrendered). Stamped at
          reduce so the caller can act on a deterministic command string.
        - ``artifacts`` -- defaults to a stub :class:`Artifacts`
          (DM-018 lands in T01.28). The artifact bundle (manifest_path,
          state_path, event_log_jsonl, event_log_md, done_sentinel) is
          stamped at reduce so callers have a single struct enumerating
          the on-disk artefacts.

    Validation (``__post_init__``):
        - ``status`` must be one of the values declared by
          :data:`ResultStatus`; arbitrary strings raise ``ValueError``
          (T01.25 acceptance: ``status`` is a Literal). This is the
          dataclass-level guard; schema-time enforcement is duplicated
          at COMP-005 (M2) for the JSON-Schema validator surface and
          at COMP-009 (M5) where IMM-5 stamps the value.

    Cross-field validation -- the INV-005 worker-count invariant
    (``workers_succeeded + workers_failed == workers_requested``), the
    IMM-5 status/M/N matrix, the ``merged_path`` non-null implication on
    ``amalgamation_mode == "normalize+merge"``, and FR-018 field-presence
    -- is the COMP-009 reduce layer's job (M5), not this dataclass.

    Round-trip: the aggregator's ``from_dict`` recurses into nested
    dataclass fields (CallerInfo, ContractTarget, CallerMetadata,
    Artifacts) **and** into ``list[<dataclass>]`` fields (output_files)
    so populated ResultContract instances round-trip losslessly via JSON
    (``from_json(to_json(x)) == x``). The byte-identical guarantee
    (``to_json`` sorts keys) is required by INV-016 / FR-018 so a
    contract written once and read back is bit-identical.
    """

    contract_version: str = "1.0"
    status: ResultStatus = "success"
    job_id: str = ""
    started: str = ""
    finished: str = ""
    elapsed_ms: int = 0
    caller: "CallerInfo" = field(default_factory=lambda: CallerInfo())
    lens: str = ""
    lens_source: str = ""
    target: "ContractTarget" = field(default_factory=lambda: ContractTarget())
    workers_requested: int = 0
    workers_succeeded: int = 0
    workers_failed: int = 0
    output_files: list["WorkerResult"] = field(default_factory=list)
    amalgamation_mode: AmalgamationMode = "normalize+merge"
    merged_path: Optional[str] = None
    caller_metadata: "CallerMetadata" = field(default_factory=lambda: CallerMetadata())
    recommended_next_command: str = ""
    artifacts: "Artifacts" = field(default_factory=lambda: Artifacts())

    def __post_init__(self) -> None:
        allowed_status = typing.get_args(ResultStatus)
        if self.status not in allowed_status:
            raise ValueError(
                f"ResultContract.status must be one of {allowed_status}, "
                f"got {self.status!r}"
            )


@dataclass
class WorkerResult:
    """DM-013 -- per-worker output entry dataclass.

    Field set drawn verbatim from the roadmap DM-013 row
    (``.dev/releases/Current/MultiModelSwarm/roadmap.md`` line 100):
    ``index:int; path:str; raw_path:str; meta_path:str; final_path:str;
    model_id:str; model_label:str; bytes:int; status:enum; http_code:int?;
    attempts:int; elapsed_ms:int``.

    WorkerResult is the per-worker entry the dispatcher (M3 -- COMP-007)
    emits for every worker fanned out from Wave 1; instances are collected
    into :class:`ResultContract` ``output_files`` at Wave 3 reduce
    (COMP-009, M5). The :class:`Transport` Protocol (COMP-031, T01.11)
    returns one of these per call so transports stay swappable behind a
    single contract.

    The status Literal :data:`WorkerStatus` admits the four values listed
    in §5 Result Contract Schema (``merged-requirements.compressed.compressed.md``
    L395): ``success`` / ``timeout`` / ``parse_error`` / ``proxy_error``.
    The §7.4 salvage policy on :class:`OnParseError` may promote
    ``parse_error -> success`` at Wave 2 (COMP-008, M4); the dataclass
    itself does not encode that promotion.

    Defaults (all empty / zero so the aggregator's no-arg round-trip
    suite -- ``tests/swarm/test_models_round_trip.py`` -- keeps passing
    while real instances are stamped at dispatch / normalize time):
        - ``index=0`` -- worker slot index in the fan-out (0..N-1).
          Drives ``filename_template`` substitution at output write time
          (``{lens}-{index:02d}-{model_slug}.md``).
        - ``path=""`` -- the canonical output path emitted by the worker
          (post-normalization when ``amalgamation_mode`` includes
          ``normalize``; same as ``raw_path`` for raw-only mode).
        - ``raw_path=""`` -- the per-worker raw output path
          (``*.raw.<ext>``). Retained when
          ``NormalizationSpec.on_parse_error.retain_raw=True`` so the
          caller can audit salvage provenance regardless of Wave 2
          outcome.
        - ``meta_path=""`` -- the per-worker meta sidecar
          (``*.meta.json``). Carries transport / model / attempts /
          http_code / elapsed_ms / status so M3 dispatch and M6 resume
          have a single source of per-worker truth (FR-027, INV-005,
          INV-016 surface alignment).
        - ``final_path=""`` -- the per-worker post-normalization file
          consumed by Wave 3 reduce / merge. Diverges from ``path`` only
          when normalization rewrites under a different deterministic
          filename (recipe-specific; M4 recipes own the shape).
        - ``model_id=""`` -- the transport-supplied model identifier
          (e.g. ``gpt-5-codex``, ``claude-haiku-4.5``). Sourced from the
          dispatched ``WorkerSpec.models`` slot, post-expansion.
        - ``model_label=""`` -- the human-facing model label printed in
          the merge provenance header (M5 merge, COMP-009) and event log
          (COMP-012). May diverge from ``model_id`` when a deployment
          alias is in use.
        - ``bytes=0`` -- worker output byte count (raw or post-normalize
          depending on which file ``path`` points at). Used by event
          recording (COMP-012) and the IMM-4 empty-target STOP surface
          analogue at the output side.
        - ``status="success"`` -- conservative default so the no-arg
          round-trip suite keeps passing. Real instances are stamped by
          the transport (M3 -- COMP-031..033) per FR-017 outcome
          recording.
        - ``http_code=None`` -- DM-013 spells this ``http_code:int?``;
          modeled as ``Optional[int]`` because the stub transport
          (COMP-033, M3) bypasses the HTTP path entirely and the §7.4
          parse-error salvage path may emit a WorkerResult without a
          terminal HTTP status. None represents "no transport HTTP
          response recorded".
        - ``attempts=1`` -- attempt count. The FR-017 retry policy
          allows exactly one retry on 5xx; canonical values are 1
          (no retry) or 2 (5xx retried once). Stamped by the dispatcher.
        - ``elapsed_ms=0`` -- per-worker wall-clock elapsed (start of
          first attempt to terminal status), in milliseconds. Stamped
          by the dispatcher.

    Validation (``__post_init__``):
        - ``status`` must be one of the values declared by
          :data:`WorkerStatus`; arbitrary strings raise ``ValueError``
          (T01.26 acceptance: Literal enums match roadmap exactly). The
          schema layer (COMP-005, M2) and the transport implementations
          (COMP-031..033, M3) duplicate this constraint at their
          respective surfaces; this is the dataclass-level guard.

    Cross-field validation -- INV-005 worker-count invariant
    (``workers_succeeded + workers_failed == workers_requested``),
    consistency between ``raw_path`` / ``path`` / ``final_path`` under
    each ``amalgamation_mode``, ``http_code`` non-null implications by
    ``status`` -- is the COMP-007 dispatcher (M3) and COMP-009 reduce
    layer's (M5) job, not this dataclass.
    """

    index: int = 0
    path: str = ""
    raw_path: str = ""
    meta_path: str = ""
    final_path: str = ""
    model_id: str = ""
    model_label: str = ""
    bytes: int = 0
    status: WorkerStatus = "success"
    http_code: Optional[int] = None
    attempts: int = 1
    elapsed_ms: int = 0

    def __post_init__(self) -> None:
        allowed_status = typing.get_args(WorkerStatus)
        if self.status not in allowed_status:
            raise ValueError(
                f"WorkerResult.status must be one of {allowed_status}, "
                f"got {self.status!r}"
            )


@dataclass
class SwarmState:
    """DM-014 -- persistent ``.swarm-state.json`` dataclass.

    Field set drawn verbatim from the roadmap DM-014 row
    (``.dev/releases/Current/MultiModelSwarm/roadmap.md`` line 101):
    ``state:enum(preflight_ok/dispatching/normalizing/reducing/terminal);
    job_id:str; updated:str``.

    SwarmState is the **wave-level coarse state** persisted to
    ``.swarm-state.json`` via the state module (COMP-011, M3) using
    write-to-tmp + ``os.replace`` so transitions are never partial
    (T03 acceptance: "state transitions via tmp+os.replace; never
    partial"). Resume (M6 -- FR-015) reads this file to short-circuit
    to the appropriate wave; the manifest (DM-016, T01.27) is the
    finer-grained per-job source-of-truth.

    The state Literal :data:`SwarmStateValue` admits the five values from
    the roadmap row, in execution order:

        - ``preflight_ok``    -- Wave 0 finished (target ingested, lens
                                 resolved, manifest emitted); ready to
                                 dispatch.
        - ``dispatching``     -- Wave 1 in progress (transport calls
                                 fanning out via :class:`Transport`).
        - ``normalizing``     -- Wave 2 in progress (recipes converting
                                 raw outputs to canonical shape per
                                 :class:`NormalizationSpec`).
        - ``reducing``        -- Wave 3 in progress (IMM-5 status
                                 determination, merge if applicable,
                                 result contract emission).
        - ``terminal``        -- Job finished (any of ``success`` /
                                 ``partial`` / ``failed`` on the result
                                 contract). The done sentinel
                                 (:class:`DoneSentinel`, T01.28) is
                                 written immediately after this state.

    Defaults:
        - ``state="preflight_ok"`` -- conservative default representing
          "Wave 0 done, awaiting Wave 1". Lets the no-arg round-trip
          suite construct a stub while making the dataclass safe to
          inspect before the dispatcher overwrites the state.
        - ``job_id=""`` -- caller / executor stamps at construction;
          mirrors :class:`ResultContract.job_id` so the two artifacts
          agree.
        - ``updated=""`` -- ISO 8601 timestamp of the last transition;
          stamped by the state module on every write.

    Validation (``__post_init__``):
        - ``state`` must be one of the values declared by
          :data:`SwarmStateValue`; arbitrary strings raise
          ``ValueError`` (T01.26 acceptance: Literal enums match
          roadmap exactly). The schema layer (COMP-005, M2) and the
          state module (COMP-011, M3) duplicate this guard.
    """

    state: SwarmStateValue = "preflight_ok"
    job_id: str = ""
    updated: str = ""

    def __post_init__(self) -> None:
        allowed_states = typing.get_args(SwarmStateValue)
        if self.state not in allowed_states:
            raise ValueError(
                f"SwarmState.state must be one of {allowed_states}, "
                f"got {self.state!r}"
            )


@dataclass
class EventRecord:
    """DM-015 -- JSONL event entry dataclass.

    Field set drawn verbatim from the roadmap DM-015 row
    (``.dev/releases/Current/MultiModelSwarm/roadmap.md`` line 102):
    ``event_type:enum(worker_start/worker_progress/worker_done/
    wave_transition/terminal); timestamp:str; worker_index:int?;
    payload:dict``.

    EventRecord is the **per-event append-only entry** emitted by the
    logging_ module (COMP-012, M3) into ``event-log.jsonl`` (and
    cross-rendered to ``event-log.md`` for humans). Appends are
    lock-coordinated (T04 acceptance: "JSONL appends lock-coordinated")
    so concurrent transport workers do not interleave bytes. The
    Markdown log is rendered from the same record stream so the two
    artifacts cannot drift.

    The event_type Literal :data:`EventType` admits the five values from
    the roadmap row, in lifecycle order:

        - ``worker_start``      -- transport call dispatched for the
                                   worker named in ``worker_index``.
        - ``worker_progress``   -- intermediate progress (transport
                                   chunk, normalize step, etc.);
                                   ``worker_index`` set when scoped to a
                                   single worker.
        - ``worker_done``       -- terminal :class:`WorkerResult` is
                                   available for ``worker_index``;
                                   payload typically carries the
                                   serialized WorkerResult or a status
                                   summary.
        - ``wave_transition``   -- coarse Wave 0/1/2/3 transition;
                                   ``worker_index`` is ``None`` (event
                                   is not per-worker).
        - ``terminal``          -- job reached terminal status; mirrors
                                   :class:`SwarmState.state="terminal"`.

    ``worker_index`` is :data:`Optional[int]` because the
    ``wave_transition`` and ``terminal`` event types are not
    per-worker; the field is ``None`` for those events and an integer
    in the 0..N-1 slot range for the three ``worker_*`` events. The
    Optional reflects the DM-015 row's ``worker_index:int?`` shape.

    ``payload`` is a free-form ``dict[str, Any]`` because event types
    carry heterogeneous fields (transport http_code on ``worker_start``,
    normalize recipe name on ``worker_progress``, etc.). Cross-field
    payload validation belongs to the logging_ module (COMP-012) and
    the M3 dispatcher (COMP-007), not this dataclass. The dict must be
    JSON-serializable; the round-trip helpers (``to_json`` /
    ``from_json``) rely on that.

    Defaults:
        - ``event_type="worker_start"`` -- conservative default
          representing the first per-worker event. Lets the no-arg
          round-trip suite construct a stub.
        - ``timestamp=""`` -- ISO 8601 timestamp; stamped by the
          logging_ module at append time.
        - ``worker_index=None`` -- Optional, defaults None so the
          ``wave_transition`` / ``terminal`` shapes work out-of-the-box.
        - ``payload={}`` -- empty dict; event-type-specific keys are
          stamped by the emitter.

    Validation (``__post_init__``):
        - ``event_type`` must be one of the values declared by
          :data:`EventType`; arbitrary strings raise ``ValueError``
          (T01.26 acceptance: Literal enums match roadmap exactly).
          The schema layer (COMP-005, M2) and the logging_ module
          (COMP-012, M3) duplicate this guard.

    Cross-field validation -- ``worker_index`` non-None implications by
    ``event_type`` (worker_* events require an index, wave_transition /
    terminal require None), payload-shape constraints per event_type --
    is the COMP-012 logging_ module's job (M3), not this dataclass.
    """

    event_type: EventType = "worker_start"
    timestamp: str = ""
    worker_index: Optional[int] = None
    payload: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        allowed_event_types = typing.get_args(EventType)
        if self.event_type not in allowed_event_types:
            raise ValueError(
                f"EventRecord.event_type must be one of {allowed_event_types}, "
                f"got {self.event_type!r}"
            )


@dataclass
class PreflightSummary:
    """Nested preflight substructure for ``Manifest`` (DM-016).

    Field set drawn from the roadmap DM-016 row
    (``.dev/releases/Current/MultiModelSwarm/roadmap.md`` line 103):
    ``preflight.target_checksum:str; preflight.workers_requested:int;
    preflight.transport_kind:str``.

    Carried inline on :class:`Manifest` rather than as its own DM-### record
    because the roadmap row models the three ``preflight.*`` sub-fields as
    a single dotted block (same pattern as :class:`RetryPolicy` on
    :class:`WorkerSpec`, :class:`OnCompletion` on :class:`RuntimeSpec`, and
    :class:`ContractTarget` on :class:`ResultContract`).

    Semantics (FR-016 / INV-016, stamped at Wave 0 preflight -- COMP-005 +
    COMP-006, M2 / M3):
        - ``target_checksum`` -- sha256 hex digest of the ingested target
          block (post-truncation, pre-delimiter wrapping) so resume can
          confirm the on-disk target still matches what was dispatched.
          Defaults to ``""`` so the no-arg round-trip stub stays valid.
        - ``workers_requested`` -- count actually dispatched at Wave 1
          (mirrors :class:`ResultContract.workers_requested` post-FR-020
          expansion). Defaults to 0.
        - ``transport_kind`` -- copied verbatim from
          :class:`TransportSpec.kind` at preflight so the manifest carries
          a stable view even if a future config layer rewrites the
          transport between resume and dispatch. Defaults to ``""`` so the
          no-arg round-trip stub stays valid (constrained to
          :data:`TransportKind` values at schema time, COMP-005 M2).
    """

    target_checksum: str = ""
    workers_requested: int = 0
    transport_kind: str = ""


@dataclass(frozen=True)
class Manifest:
    """DM-016 -- preflight artifact / INV-001 / INV-016 source-of-truth anchor.

    Field set drawn verbatim from the roadmap DM-016 row
    (``.dev/releases/Current/MultiModelSwarm/roadmap.md`` line 103):
    ``contract_version:str; job_id:str;
    resolved_lens_entry:ResolvedLensEntry; preflight.target_checksum:str;
    preflight.workers_requested:int; preflight.transport_kind:str``.

    The three dotted ``preflight.*`` sub-fields collapse into a single
    nested :class:`PreflightSummary` dataclass, same pattern as
    :class:`RetryPolicy` on :class:`WorkerSpec` and :class:`ContractTarget`
    on :class:`ResultContract`.

    Manifest is the **durable source-of-truth artifact** emitted at Wave 0
    preflight (FR-016, COMP-006) and persisted to ``manifest.json``. INV-001
    guarantees that M6 resume rehydrates the lens binding from
    ``manifest.resolved_lens_entry`` rather than re-resolving against the
    current LENSES registry (the latter may have been hot-edited since the
    job was accepted). INV-016 reinforces this by requiring the manifest to
    round-trip byte-identically -- a manifest written once and read back
    must be bit-identical so the source-of-truth contract holds across
    process boundaries (executor exits, ``swarm attach`` re-reads, M6 resume
    rehydrates).

    Defaults:
        - ``contract_version="1.0"`` -- mirrors :class:`ResultContract`
          (T01.25) so the manifest and its terminal contract carry the same
          schema version. Caller / executor stamps this at preflight emit.
        - ``job_id=""`` -- caller / executor stamps a UUIDv4 (or
          deterministic UUIDv5 for testing) at preflight; mirrors
          :class:`ResultContract.job_id` and :class:`SwarmState.job_id` so
          the three artifacts agree.
        - ``resolved_lens_entry`` -- defaults to a stub
          :class:`ResolvedLensEntry`; real instances are built via
          :meth:`ResolvedLensEntry.from_lens` at preflight (FR-016 / FR-020
          lens-driven defaults expansion). The default-stub path exists so
          the aggregator's no-arg round-trip suite
          (``tests/swarm/test_models_round_trip.py``) continues to pass.
        - ``preflight`` -- defaults to a stub :class:`PreflightSummary`;
          real values (target_checksum, workers_requested, transport_kind)
          stamped at Wave 0 preflight emit (COMP-006).

    Round-trip:
        The aggregator's ``from_dict`` recurses into nested dataclass-typed
        fields (``resolved_lens_entry`` -> :class:`ResolvedLensEntry`,
        ``preflight`` -> :class:`PreflightSummary`) so a populated Manifest
        round-trips losslessly via JSON (``from_json(to_json(x)) == x``).
        Combined with ``to_json`` ``sort_keys=True``, two encodings of the
        same Manifest are byte-identical -- the INV-016 source-of-truth
        guarantee. The ``resolved_lens_entry`` snapshot is preserved
        verbatim through the round-trip (T01.27 acceptance:
        "resolved_lens_entry preserved verbatim").

    Cross-field validation -- ``contract_version`` semver compatibility
    against the schema layer's recognized versions (NFR-006), ``job_id``
    UUID shape, ``preflight.target_checksum`` sha256 hex shape,
    ``preflight.transport_kind`` membership in :data:`TransportKind` -- is
    the COMP-005 schema layer's job (M2) and the COMP-006 preflight
    emitter's job (M3), not this dataclass.
    """

    contract_version: str = "1.0"
    job_id: str = ""
    resolved_lens_entry: "ResolvedLensEntry" = field(
        default_factory=lambda: ResolvedLensEntry()
    )
    preflight: "PreflightSummary" = field(
        default_factory=lambda: PreflightSummary()
    )
    # F-P2-2 -- persist the resolved DM-020 CallerMetadata on the manifest so a
    # caller-supplied OQ-009 override (suspect / tier) provided at Wave 0 is
    # recoverable from ``manifest.json`` alone (INV-001 / INV-016), not only
    # in-memory on PreflightResult. Realises the "future work" noted in the
    # OQ-009 resolution: the lens-side contribution is already recoverable via
    # ``resolved_lens_entry`` (DM-011 suspect/tier), but a caller override that
    # diverged from the lens default was previously lost on executor restart.
    # Versioned by the manifest's own ``contract_version`` and defaulted, so
    # manifests written before this field existed still load (``from_dict``
    # applies the default for the absent key) -- additive, backward-compatible,
    # no-arg-construction safe, round-trip lossless via the nested-dataclass
    # helpers.
    caller_metadata: "CallerMetadata" = field(
        default_factory=lambda: CallerMetadata()
    )


@dataclass(frozen=True)
class DoneSentinel:
    """DM-017 -- terminal ``done.json`` marker dataclass.

    Field set drawn verbatim from the roadmap DM-017 row
    (``.dev/releases/Current/MultiModelSwarm/roadmap.md`` line 104):
    ``atomic_write:bool(true); terminal_status:str; contract_path:str``.

    DoneSentinel is the **terminal marker** written atomically to
    ``done.json`` immediately after :class:`SwarmState.state` flips to
    ``terminal``. FR-029 / FR-014 require the sentinel so detached /
    tmux callers (``swarm attach`` / ``subprocess.run(...)`` per FR-030)
    can tell the job finished without polling the executor process.

    The sentinel is the smallest possible struct that lets a caller
    locate the full :class:`ResultContract`: ``terminal_status`` is the
    IMM-5 final verdict, ``contract_path`` points at
    ``return-contract.yaml``. The contract itself carries the rich
    artifact bundle (:class:`Artifacts`, DM-018) so the sentinel does
    not need to re-list every per-job path.

    The roadmap row spells ``terminal_status`` as ``str``, but every
    legal value flows in from :class:`ResultContract.status` where the
    field is the :data:`ResultStatus` Literal. Carrying the Literal here
    too keeps the sentinel's type contract aligned with the contract it
    points at, and lets the same out-of-enum guard reject any manually
    constructed sentinel that drifts from the IMM-5 matrix. The JSON
    round-trip is unaffected (Literal serializes as its string value).
    This mirrors the pattern used on :class:`ResolvedLensEntry.stability`
    (roadmap row ``str``, dataclass field :data:`Stability`).

    Defaults:
        - ``atomic_write=True`` -- DM-017 row spells this ``bool(true)``,
          encoding the always-on default. The write itself uses
          write-to-tmp + ``os.replace`` (IMM-6 / COMP-011) so a mid-write
          kill never leaves a partial sentinel and rerun is idempotent.
        - ``terminal_status="success"`` -- conservative default so the
          no-arg round-trip suite (``tests/swarm/test_models_round_trip.py``)
          keeps passing. Real instances are stamped at Wave 3 reduce
          (COMP-009, M5) where IMM-5 determines the value.
        - ``contract_path=""`` -- executor stamps the absolute path to
          ``return-contract.yaml`` at sentinel-emit time; empty default
          satisfies the no-arg round-trip.

    Validation (``__post_init__``):
        - ``terminal_status`` must be one of the values declared by
          :data:`ResultStatus`; arbitrary strings raise ``ValueError``.
          This mirrors the :class:`ResultContract.status` guard so a
          manually constructed sentinel cannot smuggle an out-of-enum
          value into ``done.json``.

    Cross-field validation -- ``contract_path`` existence on disk and
    consistency with :class:`Artifacts`-listed paths -- is the COMP-013
    executor / M7 detached-mode layer's job, not this dataclass.
    """

    atomic_write: bool = True
    terminal_status: ResultStatus = "success"
    contract_path: str = ""

    def __post_init__(self) -> None:
        allowed_status = typing.get_args(ResultStatus)
        if self.terminal_status not in allowed_status:
            raise ValueError(
                f"DoneSentinel.terminal_status must be one of {allowed_status}, "
                f"got {self.terminal_status!r}"
            )


@dataclass
class Artifacts:
    """DM-018 -- path bundle embedded in :class:`ResultContract` dataclass.

    Field set drawn verbatim from the roadmap DM-018 row
    (``.dev/releases/Current/MultiModelSwarm/roadmap.md`` line 105):
    ``manifest_path:str; state_path:str; event_log_jsonl:str;
    event_log_md:str; done_sentinel:str``.

    Artifacts is the **path-bundle struct** embedded in
    :class:`ResultContract.artifacts` (DM-012) at Wave 3 reduce
    (COMP-009, M5). It gives callers a single struct enumerating every
    on-disk artifact a job produces, so non-Claude callers
    (``subprocess.run(...)``, FR-030) can locate them without re-deriving
    paths from the output directory layout.

    Each field is the **absolute path** to its artifact:

        - ``manifest_path``    -- ``manifest.json`` (:class:`Manifest`,
                                  DM-016) -- INV-001 / INV-016 source-of-truth.
        - ``state_path``       -- ``.swarm-state.json`` (:class:`SwarmState`,
                                  DM-014) -- wave-level coarse state.
        - ``event_log_jsonl``  -- ``event-log.jsonl`` -- :class:`EventRecord`
                                  (DM-015) append-only stream.
        - ``event_log_md``     -- ``event-log.md`` -- the same record stream
                                  cross-rendered for humans (COMP-012).
        - ``done_sentinel``    -- ``done.json`` (:class:`DoneSentinel`,
                                  DM-017) -- terminal marker. Note the
                                  field is the *path* (``str``), not a
                                  :class:`DoneSentinel` instance --
                                  matches the roadmap row's
                                  ``done_sentinel:str``.

    Defaults:
        - All five fields default to ``""`` so the aggregator's no-arg
          round-trip suite (``tests/swarm/test_models_round_trip.py``)
          keeps passing. Real instances are stamped at Wave 3 reduce
          where the executor knows every artifact's absolute path.

    Cross-field validation -- each path's existence on disk, the
    NFR-013 path-confinement guarantee against the job's output root,
    and consistency with :class:`DoneSentinel.contract_path` -- is the
    COMP-009 reduce layer's job (M5) and the COMP-013 executor's job
    (M7), not this dataclass.
    """

    manifest_path: str = ""
    state_path: str = ""
    event_log_jsonl: str = ""
    event_log_md: str = ""
    done_sentinel: str = ""


@dataclass
class CallerInfo:
    """DM-019 -- caller metadata dataclass.

    Field set drawn verbatim from the roadmap DM-019 row
    (``.dev/releases/Current/MultiModelSwarm/roadmap.md`` line 106):
    ``skill:str?; skill_version:str?; invocation_label:str;
    kind:enum(claude/cli/subprocess)``.

    CallerInfo is the **identity block** every job carries on
    :class:`JobSpec.caller` and every contract carries on
    :class:`ResultContract.caller` (the executor copies it verbatim
    from the job at Wave 0 preflight, so the two artifacts agree).
    FR-SPEC-002 specifies the four fields; NFR-COMPAT-001 marks
    ``kind`` as informational only (never used for routing).

    The four fields:

        - ``skill``            -- name of the invoking sc-skill (e.g.
                                  ``"sc-bare-review"``). Optional --
                                  ``None`` when the caller is a raw CLI
                                  invocation or arbitrary subprocess
                                  without a registered skill identity.
        - ``skill_version``    -- the skill's version string when the
                                  caller is a skill (mirrors the
                                  skill's ``SKILL.md`` ``version`` field).
                                  Optional for the same reason as
                                  ``skill``.
        - ``invocation_label`` -- a short human-readable label the
                                  caller assigns to the run (e.g.
                                  ``"bare-review-after-T01.27"``).
                                  Surfaces in the event log and the
                                  final contract; not a unique
                                  identifier (the ``job_id`` plays that
                                  role). Required (defaults to ``""``
                                  for the no-arg round-trip stub; real
                                  instances supply it).
        - ``kind``              -- transport-of-invocation enum: which
                                  surface launched the job. Defined by
                                  :data:`CallerKind` as ``"claude"``
                                  (the Claude Code harness invoked via
                                  the skill / slash command), ``"cli"``
                                  (direct ``superclaude swarm run`` on
                                  the terminal), or ``"subprocess"``
                                  (an arbitrary process invoking via
                                  ``subprocess.run(...)`` per FR-030).
                                  Informational only -- the executor
                                  does not branch on it (NFR-COMPAT-001).

    Defaults:
        - ``skill=None`` / ``skill_version=None`` -- Optional, defaults
          ``None`` so the no-arg round-trip suite constructs a stub
          without inventing a skill identity.
        - ``invocation_label=""`` -- caller supplies at construction;
          empty default satisfies the no-arg round-trip.
        - ``kind="cli"`` -- conservative default representing a direct
          terminal invocation. Real instances supply the value matching
          their launch surface (skill -> ``"claude"``, cron / harness ->
          ``"subprocess"``).

    Validation (``__post_init__``):
        - ``kind`` must be one of the values declared by
          :data:`CallerKind`; arbitrary strings raise ``ValueError``
          (T01.28 acceptance: "CallerInfo.kind Literal enforced"). The
          schema layer (COMP-005, M2) duplicates this guard at the
          FR-SPEC-002 caller-block validation surface.

    Cross-field validation -- ``skill_version`` non-null implication
    when ``skill`` is non-null (the two are paired), ``invocation_label``
    non-empty for non-stub instances, ``kind`` consistency with the
    actual launch surface -- is the COMP-005 schema layer's job (M2),
    not this dataclass.
    """

    skill: Optional[str] = None
    skill_version: Optional[str] = None
    invocation_label: str = ""
    kind: CallerKind = "cli"

    def __post_init__(self) -> None:
        allowed_kinds = typing.get_args(CallerKind)
        if self.kind not in allowed_kinds:
            raise ValueError(
                f"CallerInfo.kind must be one of {allowed_kinds}, "
                f"got {self.kind!r}"
            )


@dataclass
class CallerMetadata:
    """DM-020 -- lens/caller-attached output metadata.

    Field set drawn verbatim from the roadmap DM-020 row
    (``.dev/releases/Current/MultiModelSwarm/roadmap.md`` line 160):
    ``suspect:bool(from lens or caller); tier:str``. Resolution
    precedence follows the OQ-009 architect resolution (recorded in
    ``docs/swarm/oq-resolutions.md``): the lens entry supplies the
    default values; a caller-supplied override (when present) wins
    field-by-field, matching the §4.2 lens-driven-defaults expansion
    rule that "caller-supplied values override lens defaults"
    (FR-LENS-004).

    The two fields:

        - ``suspect`` -- whether the lens (or caller) marks this run as
          "suspect" -- e.g. the bare_review lens (COMP-024) sets this
          ``True`` so the §FR-020 / NFR-012 review discipline applies.
          Propagates from :class:`LensEntry.suspect` at preflight via
          :func:`preflight.resolve_caller_metadata`; caller-supplied
          values override.
        - ``tier`` -- the lens's tier classifier string (e.g. ``"T1"``,
          ``"T2"``). Propagates from :class:`LensEntry.tier`; caller
          overrides win.

    Wiring: :class:`ResultContract.caller_metadata` (DM-012) carries
    the resolved value stamped at Wave 3 reduce (COMP-009, M5). The
    Manifest's :class:`ResolvedLensEntry` snapshot already carries the
    lens-side ``suspect`` / ``tier`` values (DM-011) so the lens
    contribution to ``caller_metadata`` is recoverable from
    ``manifest.json`` alone (INV-001 / INV-016).

    Defaults:
        - ``suspect=False`` -- conservative default. Lenses opt in via
          :attr:`LensEntry.suspect=True`; callers opt in by supplying
          the override at preflight.
        - ``tier=""`` -- caller / lens supplies at construction; empty
          default satisfies the no-arg round-trip suite.
    """

    suspect: bool = False
    tier: str = ""


# ---------------------------------------------------------------------------
# Round-trip helpers.
#
# ``to_dict``/``from_dict`` are intentionally generic: they route through
# ``dataclasses.asdict`` (which handles nested dataclasses recursively)
# and ``json``-compatible primitives. They stay valid as downstream tasks
# add fields, provided each new field is either JSON-serializable or a
# nested dataclass exported from this module.
# ---------------------------------------------------------------------------


T = TypeVar("T")


def to_dict(instance: Any) -> dict[str, Any]:
    """Convert a swarm dataclass instance to a plain ``dict``.

    Uses :func:`dataclasses.asdict`, which recursively converts nested
    dataclasses, tuples, and lists. The returned dict is JSON-safe iff
    every leaf field is JSON-safe (str / int / float / bool / None /
    list / dict / nested dataclass). Validation of leaf JSON-safety is
    the responsibility of the round-trip test, not this helper.

    Raises:
        TypeError: ``instance`` is not a dataclass instance.
    """
    if not dataclasses.is_dataclass(instance) or isinstance(instance, type):
        raise TypeError(
            f"to_dict expects a dataclass instance, got {type(instance).__name__}"
        )
    return dataclasses.asdict(instance)


def from_dict(cls: Type[T], data: dict[str, Any]) -> T:
    """Reconstruct a swarm dataclass instance from a plain ``dict``.

    Recurses into nested dataclass-typed fields so JobSpec (T01.13) and
    other records with nested DM-### dataclasses round-trip losslessly
    via ``to_dict`` (which uses ``dataclasses.asdict`` -- flattens
    nested dataclasses to dicts). Without this recursion, ``cls(**data)``
    would assign raw dicts to dataclass-typed fields and break the
    ``restored == instance`` contract enforced by the round-trip suite.

    Behavior:
        - Skips fields absent from ``data`` (constructor default applies).
        - For dataclass-typed fields whose payload is a ``dict``,
          recursively rebuilds the nested instance.
        - For ``Optional[X]`` where X is a dataclass, recurses only when
          the payload is a non-None dict (None passes through).
        - All other field types pass through unchanged.

    Raises:
        TypeError: ``cls`` is not a dataclass type.
    """
    if not dataclasses.is_dataclass(cls) or not isinstance(cls, type):
        raise TypeError(
            f"from_dict expects a dataclass type, got {cls!r}"
        )
    # Resolve string annotations (PEP 563 `from __future__ import annotations`
    # leaves them as strings; get_type_hints evaluates them in module scope).
    hints = typing.get_type_hints(cls)
    kwargs: dict[str, Any] = {}
    for f in dataclasses.fields(cls):
        if f.name not in data:
            continue
        value = data[f.name]
        field_type = hints.get(f.name)
        nested_cls = _nested_dataclass_type(field_type)
        list_item_cls = _list_dataclass_item_type(field_type)
        if nested_cls is not None and isinstance(value, dict):
            kwargs[f.name] = from_dict(nested_cls, value)
        elif list_item_cls is not None and isinstance(value, list):
            # list[<dataclass>] -- rebuild each entry as the nested type
            # so equality holds against the original list. Non-dict
            # entries pass through unchanged (matches the scalar path).
            kwargs[f.name] = [
                from_dict(list_item_cls, item) if isinstance(item, dict) else item
                for item in value
            ]
        else:
            kwargs[f.name] = value
    return cls(**kwargs)  # type: ignore[call-arg]


def _nested_dataclass_type(field_type: Any) -> Optional[type]:
    """Return the dataclass type for ``field_type`` if it is one (or ``Optional[dc]``).

    Handles the two annotation shapes JobSpec uses today: bare
    ``CallerInfo`` and ``Optional[str]`` (``Union[str, None]``). Returns
    ``None`` for non-dataclass annotations so the caller skips recursion.
    """
    if field_type is None:
        return None
    if isinstance(field_type, type) and dataclasses.is_dataclass(field_type):
        return field_type
    # Optional[X] / Union[X, None]: unwrap and check the non-None arm.
    origin = typing.get_origin(field_type)
    if origin is typing.Union:
        args = [a for a in typing.get_args(field_type) if a is not type(None)]
        if len(args) == 1 and isinstance(args[0], type) and dataclasses.is_dataclass(args[0]):
            return args[0]
    return None


def _list_dataclass_item_type(field_type: Any) -> Optional[type]:
    """Return ``X`` if ``field_type`` is ``list[X]`` where X is a dataclass.

    Added in T01.25 to support :class:`ResultContract.output_files`
    (``list[WorkerResult]``). Without this, ``from_dict`` would assign
    the raw payload (a ``list[dict]``) and break the
    ``restored == instance`` round-trip contract once WorkerResult
    carries fields (T01.26). Returns ``None`` for non-list-of-dataclass
    annotations so the caller skips list recursion.

    Only handles the plain ``list[<dataclass>]`` shape; ``Optional[list[X]]``
    and other compound shapes can be added if a future DM-### record
    needs them.
    """
    if field_type is None:
        return None
    origin = typing.get_origin(field_type)
    if origin is list:
        args = typing.get_args(field_type)
        if (
            len(args) == 1
            and isinstance(args[0], type)
            and dataclasses.is_dataclass(args[0])
        ):
            return args[0]
    return None


def to_json(instance: Any) -> str:
    """Serialize a swarm dataclass instance to a JSON string.

    Thin convenience over ``json.dumps(to_dict(instance))`` with
    ``sort_keys=True`` so byte-identical round-trips are achievable
    (INV-016 manifests rely on this in T01.27).
    """
    return json.dumps(to_dict(instance), sort_keys=True)


def from_json(cls: Type[T], payload: str) -> T:
    """Deserialize a swarm dataclass instance from a JSON string."""
    return from_dict(cls, json.loads(payload))


# ---------------------------------------------------------------------------
# Public surface.
#
# Tests assert ``len(models.__all__) >= 20``. Adding a new DM-### record
# requires both a class declaration above AND an entry below; the parity
# is enforced by ``tests/swarm/test_models_round_trip.py``.
# ---------------------------------------------------------------------------


__all__: list[str] = [
    # DM-001..DM-009 -- top-level job spec + nested config records.
    "JobSpec",
    "WorkerSpec",
    "TargetSpec",
    "TransportSpec",
    "PromptSpec",
    "NormalizationSpec",
    "OutputSpec",
    "StatusPolicy",
    "RuntimeSpec",
    # DM-010..DM-011 -- lens registry + manifest snapshot.
    "LensEntry",
    "ResolvedLensEntry",
    # DM-012..DM-015 -- result + per-worker + persistent state + events.
    "ResultContract",
    "WorkerResult",
    "SwarmState",
    "EventRecord",
    # DM-016..DM-019 -- preflight + terminal markers + caller metadata.
    "Manifest",
    "DoneSentinel",
    "Artifacts",
    "CallerInfo",
    # DM-020 -- output-side caller metadata.
    "CallerMetadata",
    # Nested substructures (not DM-### records, but part of the public surface).
    "RetryPolicy",
    "Truncation",
    "Delimiters",
    "InjectionGuard",
    "OnParseError",
    "OnCompletion",
    "ContractTarget",
    "PreflightSummary",
    # Literal type aliases (T01.13+ -- per-record Literals exported for tests).
    "AmalgamationMode",
    "TransportKind",
    "RuntimeMode",
    "Stability",
    "ResultStatus",
    "WorkerStatus",
    "SwarmStateValue",
    "EventType",
    "CallerKind",
    # Round-trip helpers.
    "to_dict",
    "from_dict",
    "to_json",
    "from_json",
]
