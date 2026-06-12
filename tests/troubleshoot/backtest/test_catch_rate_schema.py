"""Schema-fidelity tests for the catch-rate report contract.

Mirrors ``tests/cli/eval/test_summary_schema.py`` + ``test_run_report.py``: module-scoped
``schema``/``validator`` fixtures (``Draft202012Validator.check_schema`` then ``.validate()``), a
required-field-set pin, enum pins, valid/invalid reference fixtures, AND a round-trip that validates
the REAL ``render_catch_rate_json`` output (not a hand-built dict) against the schema. Adds the
NFR-1 anti-vacuity assertions: a CATCH count alone never earns ``complete``. The report is written
ONLY to ``tmp_path`` (never under ``docs/`` -- the root ``_pollution_snapshot`` guard).
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator
from jsonschema.exceptions import ValidationError

from tests.troubleshoot.backtest.catch_rate import (
    BACKTEST_STATUS_VALUES,
    CatchRateReport,
    EscapeResult,
    build_catch_rate_report,
    unresolved_card_paths,
)
from tests.troubleshoot.backtest.catch_rate_report import (
    CatchRateContractViolation,
    render_catch_rate_json,
    write_catch_rate_report,
)
from tests.troubleshoot.backtest.schemas import load_catch_rate_schema

FIXTURE_DIR = Path(__file__).parent / "fixtures" / "catch_rate"


@pytest.fixture(scope="module")
def schema() -> dict:
    return dict(load_catch_rate_schema())


@pytest.fixture(scope="module")
def validator(schema: dict) -> Draft202012Validator:
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema)


def _load_fixture(name: str) -> dict:
    with (FIXTURE_DIR / name).open(encoding="utf-8") as fh:
        return json.load(fh)


def _escapes_from(payload: dict) -> tuple[EscapeResult, ...]:
    return tuple(
        EscapeResult(
            escape_id=e["escape_id"],
            wave=e["wave"],
            verdict=e["verdict"],
            negative_witness=e["negative_witness"],
            card_path=e["card_path"],
            detail=e.get("detail", ""),
        )
        for e in payload["escapes"]
    )


# (a) schema is well-formed draft-2020-12 -----------------------------------------------------------
def test_backtest_catch_rate_schema_is_well_formed() -> None:
    Draft202012Validator.check_schema(load_catch_rate_schema())


# (b) the REAL producer output validates against the schema -----------------------------------------
def test_backtest_render_output_validates_against_schema(
    validator: Draft202012Validator,
) -> None:
    escapes = (
        EscapeResult("E1", "H1", "MISS", True, None, "old misses, new not yet proven"),
        EscapeResult("E2", "H3", "CATCH", True, "refs/unmask-and-sweep.md", "caught"),
        EscapeResult("E3", "H3", "CATCH", True, "refs/unmask-and-sweep.md", "caught"),
        EscapeResult("E4", "H2", "MISS", True, None, "old misses"),
        EscapeResult(
            "E5", "H4", "CATCH", True, "refs/effective-input-proof.md", "caught"
        ),
    )
    report = build_catch_rate_report(
        run_id="rt-001",
        generated_at="2026-06-12T00:00:00Z",
        contract_version="1.0.0",
        escapes=escapes,
        proxy_limitation="NEW=CATCH is a documentation-presence proxy.",
    )
    payload = json.loads(render_catch_rate_json(report))
    validator.validate(payload)  # raises ValidationError on any contract drift
    assert payload["backtest_status"] == "partial"
    assert payload["caught"] == 3 and payload["missed"] == 2


# (c) pin required set (order-sensitive) + enums + this schema's OWN escapeId pattern ----------------
def test_backtest_schema_pins_required_set_and_enums(schema: dict) -> None:
    assert schema["required"] == [
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
    ]
    assert tuple(schema["$defs"]["backtestStatus"]["enum"]) == (
        "not_run",
        "partial",
        "complete",
    )
    assert tuple(BACKTEST_STATUS_VALUES) == ("not_run", "partial", "complete")
    assert tuple(schema["$defs"]["escapeResult"]["properties"]["verdict"]["enum"]) == (
        "CATCH",
        "MISS",
    )
    # escape-id pattern is sourced from THIS schema's OWN $defs.escapeId (NOT summary.schema.json,
    # which carries no escape-id/eval-id pattern $def at all).
    assert schema["$defs"]["escapeId"]["pattern"] == "^E[0-9]+$"


# (d) __post_init__ invariant + writer contract violation ------------------------------------------
def test_backtest_post_init_raises_on_mismatched_status() -> None:
    escapes = tuple(
        EscapeResult(f"E{i}", "H1", "CATCH", True, f"refs/c{i}.md") for i in range(1, 6)
    )
    # Claiming not_run while a full all-CATCH set derives complete must raise.
    with pytest.raises(ValueError):
        CatchRateReport(
            run_id="x",
            generated_at="t",
            contract_version="1",
            backtest_status="not_run",
            total_escapes=5,
            caught=5,
            missed=0,
            catch_rate=1.0,
            escapes=escapes,
            proxy_limitation="p",
        )


def test_backtest_contract_violation_when_counts_unbalanced() -> None:
    # _check guards the writer independently of the model's __post_init__; a duck-typed report whose
    # caught+missed != total_escapes must raise CatchRateContractViolation (mapped to exit 2).
    import types

    bogus = types.SimpleNamespace(
        run_id="x",
        caught=3,
        missed=1,
        total_escapes=5,  # 3 + 1 != 5
        escapes=(),
    )
    with pytest.raises(CatchRateContractViolation):
        render_catch_rate_json(bogus)  # type: ignore[arg-type]


# (e) derivation: complete / partial(+missing ids) / not_run ---------------------------------------
def test_backtest_derivation_complete_partial_not_run() -> None:
    full = tuple(
        EscapeResult(f"E{i}", "H1", "CATCH", True, f"refs/c{i}.md") for i in range(1, 6)
    )
    rc = build_catch_rate_report(
        run_id="x",
        generated_at="t",
        contract_version="1",
        escapes=full,
        proxy_limitation="p",
    )
    assert rc.backtest_status == "complete"
    assert rc.missing_escape_ids() == ()

    mixed = (EscapeResult("E1", "H1", "MISS", True, None),) + full[1:]
    rp = build_catch_rate_report(
        run_id="x",
        generated_at="t",
        contract_version="1",
        escapes=mixed,
        proxy_limitation="p",
    )
    assert rp.backtest_status == "partial"
    assert "E1" in rp.missing_escape_ids()

    r0 = build_catch_rate_report(
        run_id="x",
        generated_at="t",
        contract_version="1",
        escapes=(),
        proxy_limitation="p",
    )
    assert r0.backtest_status == "not_run"


# (f) ANTI-VACUITY edge cases: all-CATCH but missing witness/card -> partial, NOT complete ----------
def test_backtest_anti_vacuity_all_catch_missing_witness_is_partial() -> None:
    payload = _load_fixture("all_catch_missing_witness.json")
    escapes = _escapes_from(payload)
    report = build_catch_rate_report(
        run_id="av-1",
        generated_at="t",
        contract_version="1",
        escapes=escapes,
        proxy_limitation="p",
    )
    assert report.backtest_status == "partial", (
        "all-CATCH with a missing witness must NOT be complete"
    )
    assert "E1" in report.missing_escape_ids()


def test_backtest_anti_vacuity_all_catch_missing_card_is_partial() -> None:
    escapes = (EscapeResult("E1", "H1", "CATCH", True, None),) + tuple(
        EscapeResult(f"E{i}", "H1", "CATCH", True, f"refs/c{i}.md") for i in range(2, 6)
    )
    report = build_catch_rate_report(
        run_id="av-2",
        generated_at="t",
        contract_version="1",
        escapes=escapes,
        proxy_limitation="p",
    )
    assert report.backtest_status == "partial", (
        "all-CATCH with a null card_path must NOT be complete"
    )
    assert "E1" in report.missing_escape_ids()


def test_backtest_complete_claim_with_null_card_raises() -> None:
    # card_path EXPLICITLY participates in the invariant: a complete-claimed escape with null
    # card_path is an invariant violation, not a silent downgrade.
    escapes = tuple(
        EscapeResult(f"E{i}", "H1", "CATCH", True, None) for i in range(1, 6)
    )
    with pytest.raises(ValueError):
        CatchRateReport(
            run_id="x",
            generated_at="t",
            contract_version="1",
            backtest_status="complete",
            total_escapes=5,
            caught=5,
            missed=0,
            catch_rate=1.0,
            escapes=escapes,
            proxy_limitation="p",
        )


# (g) proxy_limitation is serialized to JSON (not docstring-only) -----------------------------------
def test_backtest_proxy_limitation_is_serialized() -> None:
    report = build_catch_rate_report(
        run_id="x",
        generated_at="t",
        contract_version="1",
        escapes=(EscapeResult("E1", "H1", "MISS", True, None),),
        proxy_limitation="documentation-presence proxy note",
    )
    payload = json.loads(render_catch_rate_json(report))
    assert payload["proxy_limitation"] == "documentation-presence proxy note"


@pytest.mark.parametrize("blank", ["", "   ", "\t", "\n  \t"])
def test_backtest_proxy_limitation_empty_or_whitespace_raises(blank: str) -> None:
    # NEGATIVE witness for the __post_init__ proxy_limitation honesty guard (catch_rate.py:158-166,
    # OVERSELL-2): an empty or whitespace-only caveat must raise ValueError so the JSON SoT can never
    # ship a blanked NEW=CATCH documentation-presence-proxy caveat. Uses a valid not_run shape
    # (escapes=(), all counts 0) so ONLY the blank proxy_limitation triggers the raise.
    with pytest.raises(ValueError):
        CatchRateReport(
            run_id="x",
            generated_at="t",
            contract_version="1",
            backtest_status="not_run",
            total_escapes=0,
            caught=0,
            missed=0,
            catch_rate=0.0,
            escapes=(),
            proxy_limitation=blank,
        )


# (h) unresolved_card_paths: real on-disk existence gate (pure helper, model stays IO-free) ---------
def test_backtest_unresolved_card_paths_existing_vs_fabricated(tmp_path: Path) -> None:
    # (i) every card_path resolves to a real file under base_dir -> () (no unresolved cards).
    (tmp_path / "refs").mkdir()
    real_cards = []
    for i in range(1, 6):
        rel = f"refs/c{i}.md"
        (tmp_path / rel).write_text("landed impl ref", encoding="utf-8")
        real_cards.append(rel)
    full = tuple(
        EscapeResult(f"E{i}", "H1", "CATCH", True, real_cards[i - 1])
        for i in range(1, 6)
    )
    report_ok = build_catch_rate_report(
        run_id="u-1",
        generated_at="t",
        contract_version="1",
        escapes=full,
        proxy_limitation="p",
    )
    assert unresolved_card_paths(report_ok, base_dir=tmp_path) == ()

    # (ii) a fabricated card_path (no file on disk) is returned as unresolved; a null card_path on a
    # non-fully-caught escape is skipped (not surfaced as an unresolved existing-ref).
    fabricated = "refs/does-not-exist.md"
    mixed = (
        EscapeResult("E1", "H1", "MISS", True, None),
        EscapeResult("E2", "H1", "CATCH", True, fabricated),
    ) + tuple(
        EscapeResult(f"E{i}", "H1", "CATCH", True, real_cards[i - 1])
        for i in range(3, 6)
    )
    report_bad = build_catch_rate_report(
        run_id="u-2",
        generated_at="t",
        contract_version="1",
        escapes=mixed,
        proxy_limitation="p",
    )
    assert unresolved_card_paths(report_bad, base_dir=tmp_path) == (fabricated,)


# reference fixtures: valid validate; invalid raise ------------------------------------------------
def test_backtest_valid_fixtures_validate(validator: Draft202012Validator) -> None:
    validator.validate(_load_fixture("valid_minimal.json"))
    validator.validate(_load_fixture("valid_full.json"))


@pytest.mark.parametrize("bad", ["invalid_bad_status.json", "invalid_bad_verdict.json"])
def test_backtest_invalid_fixtures_fail_validation(
    validator: Draft202012Validator, bad: str
) -> None:
    with pytest.raises(ValidationError):
        validator.validate(_load_fixture(bad))


# writer round-trip to tmp_path (NEVER docs/) ------------------------------------------------------
def test_backtest_writer_emits_to_tmp_path_only(tmp_path: Path) -> None:
    report = build_catch_rate_report(
        run_id="w-1",
        generated_at="t",
        contract_version="1.0.0",
        escapes=(EscapeResult("E1", "H1", "MISS", True, None),),
        proxy_limitation="proxy",
    )
    written = write_catch_rate_report(report, tmp_path)
    assert (tmp_path / "catch-rate.json").exists()
    assert "docs" not in str(written["catch-rate.json"].parent)
    payload = json.loads((tmp_path / "catch-rate.json").read_text(encoding="utf-8"))
    assert payload["run_id"] == "w-1"
