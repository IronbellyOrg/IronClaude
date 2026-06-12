"""Catch-rate report model -- frozen dataclasses + field tuples + invariant guard + to_dict SoT.

Mirrors the ``src/superclaude/cli/eval/models.py`` ``RunSummary`` idiom (models.py:835-946): frozen
dataclasses, an explicit ``_*_FIELDS`` ordering tuple, a ``__post_init__`` invariant guard that
re-derives the load-bearing field and raises ``ValueError`` on a mismatch (so a misreporting producer
fails loudly), and a ``to_dict()`` that walks the field tuple as the single serialization source of
truth.

NFR-1 / RELEASE-SPEC sec 4.5 + sec 5.4 backtest_status contract:
  enum = {not_run, partial, complete}, default not_run.
  Derivation is ANTI-VACUITY-TIGHTENED (sec 5.4 / research/07): a CATCH *count* alone must NOT earn
  ``complete``. ``complete`` requires, for ALL five escapes, the conjunction of three facts:
  verdict == CATCH AND a truthy ``negative_witness`` AND a non-null ``card_path``. If any escape is
  missing ANY of those three, a replay-that-ran derives ``partial`` (and the report surfaces the
  escape ids missing any of {CATCH, negative_witness, card_path}); no replay (no escapes) -> not_run.
  ``backtest_status`` is SEPARATE from any run-level verdict: a clean run does not earn production
  signoff until the corpus is ``complete`` (sec 5.4 separation invariant).

PRODUCER-ASSERTED bookkeeping contract (NOT executed-gate observations):
  This model is a BOOKKEEPING CONTRACT over claims the producer asserts; it is not itself an
  executed gate. All three ``is_fully_caught`` conjuncts -- ``verdict == CATCH``, a truthy
  ``negative_witness``, and a non-null ``card_path`` -- are PRODUCER-ASSERTED, not observations this
  model executes. The data invariant this model enforces on ``card_path`` is NON-NULLNESS only; it
  does NOT stat the filesystem. Card EXISTENCE (the impl ref having actually landed) is enforced
  UPSTREAM -- by the Phase 4 ``requires_impl_ref`` skip-guard and by the aggregation, which only sets
  ``card_path`` from a ref it has already verified to exist. Callers that want a real existence gate
  use the module-level :func:`unresolved_card_paths` helper (pure, IO done OUTSIDE the frozen model).
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

# Per-escape verdict tokens (the EscapeResult.verdict enum; matches the JSON Schema verdict $def).
VERDICT_CATCH = "CATCH"
VERDICT_MISS = "MISS"

# backtest_status enum (RELEASE-SPEC sec 4.5). DEFAULT is not_run.
STATUS_NOT_RUN = "not_run"
STATUS_PARTIAL = "partial"
STATUS_COMPLETE = "complete"
BACKTEST_STATUS_VALUES: tuple[str, ...] = (
    STATUS_NOT_RUN,
    STATUS_PARTIAL,
    STATUS_COMPLETE,
)

_ESCAPE_RESULT_FIELDS: tuple[str, ...] = (
    "escape_id",
    "wave",
    "verdict",
    "negative_witness",
    "card_path",
    "detail",
)

_CATCH_RATE_FIELDS: tuple[str, ...] = (
    "run_id",
    "generated_at",
    "contract_version",
    "backtest_status",
    "total_escapes",
    "caught",
    "missed",
    "catch_rate",
    "escapes",
    "proxy_limitation",
)


@dataclass(frozen=True)
class EscapeResult:
    """One per-escape differential outcome (E1..E5).

    Fields:
        escape_id: Canonical escape id (E1..E5).
        wave: The H-wave the escape maps to in RELEASE-SPEC sec 8.3. H1..H4 are the waves the E1-E5
            escapes actually map to; the full wave taxonomy is H0..H5 (see ``ReplayEscape.wave`` in
            ``git_replay.py``) -- the narrower range here is a subset, not a contradiction.
        verdict: ``CATCH`` (the new H-gate would catch this escape) | ``MISS`` (not proven caught).
        negative_witness: PRODUCER-ASSERTED claim that the OLD=MISS negative witness (un-hardened
            protocol misses) was observed for this escape -- a precondition for, but NOT sufficient
            for, ``complete``.
        card_path: PRODUCER-ASSERTED path to the NEW=CATCH proof surface (the impl-ref card).
            ``None`` until the producer records a landed ref. The model's data invariant is
            NON-NULLNESS only (a null ``card_path`` blocks ``complete``, anti-vacuity); the model does
            NOT stat the path. Card EXISTENCE is enforced upstream (Phase 4 ``requires_impl_ref``
            skip-guard + aggregation setting ``card_path`` only from a verified-existing ref); use
            :func:`unresolved_card_paths` for a real on-disk existence check.
        detail: Human-readable note on the observed differential.
    """

    escape_id: str
    wave: str
    verdict: str
    negative_witness: bool
    card_path: str | None
    detail: str = ""

    def __post_init__(self) -> None:
        if self.verdict not in (VERDICT_CATCH, VERDICT_MISS):
            raise ValueError(
                f"EscapeResult.verdict must be one of {(VERDICT_CATCH, VERDICT_MISS)}, "
                f"got {self.verdict!r}"
            )

    def is_fully_caught(self) -> bool:
        """True iff this escape satisfies ALL three complete-conjuncts (CATCH + witness + card)."""
        return (
            self.verdict == VERDICT_CATCH
            and bool(self.negative_witness)
            and self.card_path is not None
        )

    def to_dict(self) -> dict[str, Any]:
        return {name: getattr(self, name) for name in _ESCAPE_RESULT_FIELDS}


def _derive_backtest_status(escapes: tuple[EscapeResult, ...]) -> str:
    """Derive backtest_status from the escape records (ANTI-VACUITY-TIGHTENED, sec 5.4 / research/07).

    - no escapes (no replay ran)                                         -> ``not_run``
    - ALL escapes satisfy CATCH AND negative_witness AND card_path != None -> ``complete``
    - a replay ran but the all-three-for-all condition is unmet           -> ``partial``
    """
    if not escapes:
        return STATUS_NOT_RUN
    if all(e.is_fully_caught() for e in escapes):
        return STATUS_COMPLETE
    return STATUS_PARTIAL


def _missing_escape_ids(escapes: tuple[EscapeResult, ...]) -> tuple[str, ...]:
    """Escape ids missing ANY of {CATCH, negative_witness, card_path} (surfaced for ``partial``)."""
    return tuple(e.escape_id for e in escapes if not e.is_fully_caught())


@dataclass(frozen=True)
class CatchRateReport:
    """Aggregate catch-rate report driving ``backtest_status`` (NFR-1).

    Field order matches ``_CATCH_RATE_FIELDS`` (the JSON Schema ``required`` order). ``proxy_limitation``
    is a SERIALIZED field (not docstring-only) so the NEW=CATCH documentation-presence-proxy caveat
    always reaches the JSON artifact and is never silently dropped.
    """

    run_id: str
    generated_at: str
    contract_version: str
    backtest_status: str
    total_escapes: int
    caught: int
    missed: int
    catch_rate: float
    escapes: tuple[EscapeResult, ...] = ()
    proxy_limitation: str = ""

    def __post_init__(self) -> None:
        # 0. proxy_limitation must be present AND honest (non-empty, not whitespace-only): the caveat
        #    is required-present by the schema, and this guard makes it required-HONEST so the JSON
        #    SoT can never ship an empty caveat (OVERSELL-2). IO-free -- a pure string check.
        if not self.proxy_limitation or not self.proxy_limitation.strip():
            raise ValueError(
                "CatchRateReport: proxy_limitation must be a non-empty, non-whitespace string -- "
                "the NEW=CATCH documentation-presence-proxy caveat may not be dropped or blanked"
            )
        # 1. Count accounting must balance.
        if self.caught + self.missed != self.total_escapes:
            raise ValueError(
                f"CatchRateReport: caught({self.caught}) + missed({self.missed}) != "
                f"total_escapes({self.total_escapes})"
            )
        # 2. When escapes are provided, their cardinality must match the denominator.
        if self.escapes and len(self.escapes) != self.total_escapes:
            raise ValueError(
                f"CatchRateReport: len(escapes)({len(self.escapes)}) != "
                f"total_escapes({self.total_escapes})"
            )
        # 3. backtest_status must equal the anti-vacuity derivation (the load-bearing invariant).
        derived = _derive_backtest_status(self.escapes)
        if self.backtest_status != derived:
            raise ValueError(
                f"CatchRateReport: backtest_status({self.backtest_status!r}) != derived "
                f"({derived!r}) from escapes -- a CATCH count alone never earns 'complete'; each "
                "escape must carry CATCH AND negative_witness AND a non-null card_path"
            )
        # 4. card_path EXPLICITLY participates: a 'complete'-claimed escape with a null card_path
        #    (or missing witness / not CATCH) is an invariant violation, not a silent downgrade.
        if self.backtest_status == STATUS_COMPLETE:
            for e in self.escapes:
                if e.card_path is None:
                    raise ValueError(
                        f"CatchRateReport: backtest_status 'complete' but escape {e.escape_id} has "
                        "card_path=None -- card_path must be non-null for every escape claimed "
                        "toward 'complete' (anti-vacuity)"
                    )
                if not e.is_fully_caught():
                    raise ValueError(
                        f"CatchRateReport: backtest_status 'complete' but escape {e.escape_id} does "
                        "not satisfy CATCH AND negative_witness AND card_path"
                    )

    def missing_escape_ids(self) -> tuple[str, ...]:
        """Escape ids missing ANY of {CATCH, negative_witness, card_path} (for ``partial`` listing)."""
        return _missing_escape_ids(self.escapes)

    def production_signoff(self, run_level_verdict: str) -> str:
        """Production-facing signoff -- stays ``advisory`` until ``complete`` (sec 5.4 separation).

        ``backtest_status`` is SEPARATE from the run-level ``pipeline_hardening_verdict``: a clean
        run-level ``pass`` does NOT earn production signoff until the E1-E5 corpus is ``complete``.
        Only ``complete`` may MIRROR the run-level verdict; ``not_run`` / ``partial`` render
        ``advisory`` regardless of how green the run-level verdict is.
        """
        if self.backtest_status == STATUS_COMPLETE:
            return run_level_verdict
        return "advisory"

    def to_dict(self) -> dict[str, Any]:
        """Deterministic JSON-serialisable mapping; walks ``_CATCH_RATE_FIELDS`` (the SoT)."""
        payload: dict[str, Any] = {}
        for name in _CATCH_RATE_FIELDS:
            value = getattr(self, name)
            if name == "escapes":
                payload[name] = [item.to_dict() for item in value]
            else:
                payload[name] = value
        return payload


def build_catch_rate_report(
    *,
    run_id: str,
    generated_at: str,
    contract_version: str,
    escapes: tuple[EscapeResult, ...],
    proxy_limitation: str,
) -> CatchRateReport:
    """Construct a ``CatchRateReport`` from escape records, deriving the counts + status + rate.

    Convenience factory so callers never hand-compute (and risk desyncing) ``caught``/``missed``/
    ``catch_rate``/``backtest_status`` -- they are derived here and re-checked by ``__post_init__``.
    """
    total = len(escapes)
    caught = sum(1 for e in escapes if e.verdict == VERDICT_CATCH)
    missed = total - caught
    catch_rate = (caught / total) if total else 0.0
    return CatchRateReport(
        run_id=run_id,
        generated_at=generated_at,
        contract_version=contract_version,
        backtest_status=_derive_backtest_status(escapes),
        total_escapes=total,
        caught=caught,
        missed=missed,
        catch_rate=catch_rate,
        escapes=escapes,
        proxy_limitation=proxy_limitation,
    )


def unresolved_card_paths(
    report: CatchRateReport, *, base_dir: Path | str
) -> tuple[str, ...]:
    """Return the ``card_path`` values of escapes whose card does NOT exist under ``base_dir``.

    The REAL, testable existence gate that the frozen model deliberately does NOT perform: the model
    enforces ``card_path`` NON-NULLNESS only (it is IO-free); this pure module-level helper does the
    on-disk check OUTSIDE the model so ``__post_init__`` never touches the filesystem.

    For each escape with a non-null ``card_path``, resolves ``Path(base_dir) / card_path`` and
    includes that ``card_path`` in the result iff the resolved path does NOT exist. Escapes whose
    ``card_path is None`` are skipped (their missing-ness is already surfaced by the anti-vacuity
    derivation as ``partial``, not as an unresolved existing-ref). An empty tuple means every recorded
    card resolves to a real file -- i.e. ``complete`` is backed by landed impl refs.
    """
    root = Path(base_dir)
    unresolved: list[str] = []
    for e in report.escapes:
        if e.card_path is None:
            continue
        if not (root / e.card_path).exists():
            unresolved.append(e.card_path)
    return tuple(unresolved)
