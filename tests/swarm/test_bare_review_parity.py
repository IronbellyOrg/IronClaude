"""T08.11 / TEST-003 -- bare-review A/B parity gate (R-144 / D-0125).

This module pins the **end-to-end** parity contract between the legacy
``sc-bare-review`` shell pipeline and the new thin-caller path that
delegates to ``superclaude swarm run --lens bare-review``. It is the
gate the M8 migration plan (T08.07 / MIG-003) waits on before the
legacy ``scripts/*.sh`` are deleted -- if any assertion in this file
breaks, the deletion MUST be deferred and the discrepancy fixed first.

What the gate proves
====================

For ≥3 representative scenarios (all-success M==N, partial with one
timeout, salvage-promoted parse_error) the gate exercises both paths
against an identical set of canned reviewer bodies and asserts:

* **Byte-identical per-reviewer normalized markdown.** Each reviewer
  that produces a final ``.md`` body on the legacy path produces the
  byte-identical body on the new path, with a deterministic
  ``generated`` timestamp threaded through both sides so the only
  wall-clock-dependent field stays constant. ``test_recipe_bare_review``
  (T04.03) pins the same property at the per-fixture level; this gate
  composes it across realistic aggregator runs.

* **IMM-5 status determination parity.** ``success`` when M==N,
  ``partial`` when 2 ≤ M < N, ``failed`` when M < 2 -- the same
  success-first rule used by the legacy ``t2_normalize.py`` aggregator
  and by :func:`superclaude.cli.swarm.reduce.determine_status` /
  :class:`superclaude.cli.swarm.models.StatusPolicy`.

* **Aggregate contract invariants.** Both contracts carry
  ``suspect: true``, the same per-reviewer status set (modulo file
  paths -- the two pipelines write to different directories), and a
  ``recommended_next_command`` that names ``/sc:adversarial
  --suspect-source`` so consumers of the contract always know where to
  feed the suspect-flagged outputs.

Why not drive the actual CLI subprocess
=======================================

The thin-caller path -- ``swarm run --lens bare-review`` -- is itself
a wrapper that builds a :class:`JobSpec`, runs preflight, dispatches
through a :class:`Transport`, runs ``normalize_wave2``, and emits the
contract via ``reduce_wave3``. The bytes a real CLI invocation
produces are the same bytes the library pipeline produces -- the
``--transport stub`` lane is hermetic by construction. Driving the
library composition directly keeps the gate fast, deterministic, and
free of the env-var dance (``T2ProxyUrl`` / ``T2ProxyKey``) the
preflight wrapper requires; the recipe + reducer composition is the
real per-byte surface either lane will emit. ``test_commands_run.py``
already pins ``run_cmd`` registration + preflight handshake.

Legacy path
-----------

We import the standalone ``t2_normalize.py`` (no ``__init__.py`` in
``src/superclaude/skills/sc-bare-review/scripts/``) via :mod:`importlib`
and run :func:`t2_normalize.main` against a hand-staged manifest --
exactly the surface :func:`t2_preflight.sh` would have emitted on a
real run. The dispatcher (`t2_dispatch.sh`) is bypassed because it
requires a live proxy; we stage the per-reviewer ``.raw`` + ``.meta.json``
sidecars directly with the canned bodies the proxy would have returned.
This is the same loader pattern :mod:`tests.swarm.test_recipe_bare_review`
uses for its per-fixture parity gate.

Thin-caller path
----------------

We invoke :class:`superclaude.cli.swarm.recipes.bare_review_v1.BareReviewV1`
once per reviewer with the **same** canned bodies and identical args
(target / checksum / model_id / model_label / generated). For aggregate
status we apply :func:`superclaude.cli.swarm.reduce.determine_status`
with the default :class:`StatusPolicy` (floor=2, success_first=True),
which matches the IMM-5 surface the legacy script encodes inline.

Skip semantics
==============

The gate skips with a clear message when the legacy ``t2_normalize.py``
file is absent. Post-T08.07 (legacy retirement) the gate will be
removed wholesale; until then the file's presence is the migration
sequencer -- if it's gone, we're past the gate.
"""

from __future__ import annotations

import importlib.util
import json
import sys
import types
from pathlib import Path
from typing import Any

import pytest
import yaml

from superclaude.cli.swarm.lenses import LENSES
from superclaude.cli.swarm.models import StatusPolicy, WorkerResult
from superclaude.cli.swarm.recipes.bare_review_v1 import BareReviewV1
from superclaude.cli.swarm.reduce import determine_status

# ---------------------------------------------------------------------------
# Fixture corpus -- same files :mod:`tests.swarm.test_recipe_bare_review`
# uses for its byte-identity gate.
# ---------------------------------------------------------------------------


FIXTURES_DIR = Path(__file__).parent / "fixtures" / "bare_review_v1"

REPO_ROOT = Path(__file__).resolve().parents[2]
LEGACY_SCRIPT = (
    REPO_ROOT
    / "src"
    / "superclaude"
    / "skills"
    / "sc-bare-review"
    / "scripts"
    / "t2_normalize.py"
)

# Pinned timestamp + checksum so both pipelines stamp identical
# frontmatter on every reviewer. Real runs differ by wall-clock; this
# gate neutralises the only non-mechanical frontmatter field.
FIXED_GENERATED: str = "2026-06-01T17:59:55Z"
FIXED_CHECKSUM: str = "abcd1234efef"
CALLER_LABEL: str = "parity-gate"
ELAPSED_MS: int = 12345


# A "reviewer plan" describes one slot's input to both pipelines.
# Each entry pairs the on-disk fixture filename (or ``""`` for slots
# that produce no raw body, e.g. timeouts) with the upstream worker
# status the dispatcher would have stamped.
ReviewerPlan = list[tuple[str, str]]


# ---------------------------------------------------------------------------
# Scenarios -- ≥3 representative targets per T08.11 acceptance.
# ---------------------------------------------------------------------------
#
# (scenario_id, plan, expected_status)
#
# * ``all-success``        -- M==N==3; all three reviewers succeed.
# * ``partial-with-timeout`` -- M=2, N=3; one slot timed out (no raw
#                              body, no final.md). IMM-5 -> partial.
# * ``salvage-promoted``   -- M==3 after §7.4 promotes a parse_error
#                              slot whose body still parses cleanly.

SCENARIOS: list[tuple[str, ReviewerPlan, str]] = [
    (
        "all-success",
        [
            ("basic_findings.raw.txt", "success"),
            ("verdict_only.raw.txt", "success"),
            ("odd_cites.raw.txt", "success"),
        ],
        "success",
    ),
    (
        "partial-with-timeout",
        [
            ("basic_findings.raw.txt", "success"),
            ("verdict_only.raw.txt", "success"),
            # Slot 3 timed out -- the dispatcher would have written a
            # meta.json with status=timeout and no .raw body.
            ("", "timeout"),
        ],
        "partial",
    ),
    (
        "salvage-promoted",
        [
            ("basic_findings.raw.txt", "success"),
            ("verdict_only.raw.txt", "success"),
            # §7.4 promotion: the upstream marked this slot parse_error
            # but the body parses cleanly so the recipe + legacy script
            # both promote it to success.
            ("salvage.raw.txt", "parse_error"),
        ],
        "success",
    ),
]


# Slug helper -- mirrors the legacy bash ``slug`` function so legacy
# and recipe paths name reviewers identically. The legacy script's
# slug routine lowercases + collapses non-[a-z0-9] runs to ``-`` and
# trims leading/trailing dashes.
def _slug_model(model_id: str) -> str:
    cleaned = []
    prev_dash = False
    for ch in model_id.lower():
        if ch.isalnum():
            cleaned.append(ch)
            prev_dash = False
        else:
            if not prev_dash:
                cleaned.append("-")
                prev_dash = True
    out = "".join(cleaned).strip("-")
    return out or "m"


def _model_id(index: int) -> str:
    return f"parity-model-{index:02d}"


def _model_label(index: int) -> str:
    return f"Parity Model {index:02d}"


# ---------------------------------------------------------------------------
# Skip guard -- legacy script must still be present for the gate to run.
# ---------------------------------------------------------------------------


pytestmark = pytest.mark.skipif(
    not LEGACY_SCRIPT.exists(),
    reason=(
        f"Legacy t2_normalize.py missing at {LEGACY_SCRIPT}. "
        f"This is expected post-T08.07 / MIG-003 legacy retirement; "
        f"until then the file's presence is the migration sequencer."
    ),
)


# ---------------------------------------------------------------------------
# Legacy loader -- importlib-driven module load (no __init__.py available).
# ---------------------------------------------------------------------------


def _load_legacy() -> types.ModuleType:
    """Import ``t2_normalize.py`` as a module via :mod:`importlib`."""
    spec = importlib.util.spec_from_file_location(
        "t2_normalize_legacy_for_parity_t0811", str(LEGACY_SCRIPT)
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# ---------------------------------------------------------------------------
# Target fixture -- a real on-disk target so the legacy script's slug
# derivation has a basename to consume.
# ---------------------------------------------------------------------------


def _write_target(tmp_path: Path) -> Path:
    """Write a small, non-trivial target the legacy slug routine can chew on."""
    target = tmp_path / "target.py"
    target.write_text(
        "# parity-gate target -- exercised by both A/B paths\n"
        + "def hello(name: str) -> str:\n"
        + "    return f'hello {name}'\n"
        + "# padding to clear the IMM-4 byte-floor guard cleanly\n" * 4,
        encoding="utf-8",
    )
    return target


# ---------------------------------------------------------------------------
# Legacy aggregator driver -- stage manifest + per-reviewer sidecars,
# invoke ``t2_normalize.main``, read final.md files + contract.
# ---------------------------------------------------------------------------


def _stage_legacy_manifest(
    tmp_path: Path,
    target: Path,
    plan: ReviewerPlan,
) -> tuple[Path, list[dict[str, Any]]]:
    """Return ``(manifest_path, reviewer_records)`` for the legacy driver.

    The records describe every slot's on-disk paths so the post-run
    assertions can read the produced ``.md`` files back without
    re-deriving filename conventions.
    """
    tmp_path.mkdir(parents=True, exist_ok=True)
    reviewers: list[dict[str, Any]] = []
    for index, (fixture_name, status) in enumerate(plan, start=1):
        model_id = _model_id(index)
        model_label = _model_label(index)
        base = f"bare-review-{index:02d}-{_slug_model(model_id)}"
        raw_path = tmp_path / f"{base}.md.raw"
        meta_path = tmp_path / f"{base}.meta.json"
        final_path = tmp_path / f"{base}.md"

        # Stage the .raw body for slots that have one. Timeouts and
        # proxy errors carry no .raw -- the legacy normalizer reads
        # the meta sidecar's status, sees the hard-failure branch,
        # and produces no final.md.
        if fixture_name:
            raw_text = (FIXTURES_DIR / fixture_name).read_text(encoding="utf-8")
            raw_path.write_text(raw_text, encoding="utf-8")
        # For non-success statuses, t2_dispatch may still write a stub
        # body for triage -- we emulate the dispatcher's "no body on
        # timeout" branch by skipping the write entirely.

        meta_path.write_text(
            json.dumps(
                {
                    "status": status,
                    "elapsed_ms": ELAPSED_MS,
                    "http_code": 200 if status == "success" else None,
                    "attempts": 1,
                    "model_id": model_id,
                }
            ),
            encoding="utf-8",
        )

        reviewers.append(
            {
                "index": index,
                "model_id": model_id,
                "model_label": model_label,
                "raw_path": str(raw_path),
                "meta_path": str(meta_path),
                "final_path": str(final_path),
                "_fixture": fixture_name,
                "_status": status,
            }
        )

    manifest_path = tmp_path / "manifest.json"
    contract_path = tmp_path / "return-contract.yaml"
    manifest = {
        "contract_version": "1.0",
        "target": str(target.resolve()),
        "target_checksum": FIXED_CHECKSUM,
        "target_truncated": False,
        "caller_label": CALLER_LABEL,
        "reviewers_requested": len(plan),
        "contract_path": str(contract_path),
        "reviewers": [
            {
                "index": r["index"],
                "model_id": r["model_id"],
                "model_label": r["model_label"],
                "raw_path": r["raw_path"],
                "meta_path": r["meta_path"],
                "final_path": r["final_path"],
            }
            for r in reviewers
        ],
    }
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
    return manifest_path, reviewers


def _run_legacy(
    monkeypatch: pytest.MonkeyPatch,
    manifest_path: Path,
) -> tuple[str, dict[str, Any]]:
    """Invoke ``t2_normalize.main`` in-process. Returns (stdout, contract)."""
    legacy = _load_legacy()
    # Pin the wall-clock so frontmatter `generated` is deterministic --
    # the only non-mechanical field in the rendered .md body.
    monkeypatch.setattr(legacy, "iso_now", lambda: FIXED_GENERATED)
    monkeypatch.setattr(
        sys, "argv", ["t2_normalize.py", "--manifest", str(manifest_path)]
    )
    exit_code = legacy.main()
    assert exit_code == 0, f"legacy main() exited non-zero: {exit_code}"

    # The legacy script writes the contract YAML at the path the
    # manifest carries. Read it back so the assertions can compare
    # against the new-path contract.
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    contract_path = Path(manifest["contract_path"])
    contract_text = contract_path.read_text(encoding="utf-8")
    contract = yaml.safe_load(contract_text)
    return contract_text, contract


# ---------------------------------------------------------------------------
# Thin-caller (recipe + reducer) driver. Produces per-reviewer markdown
# via :class:`BareReviewV1` with identical args, then applies the IMM-5
# determination via :func:`determine_status`.
# ---------------------------------------------------------------------------


def _run_thin_caller(
    target: Path,
    plan: ReviewerPlan,
) -> tuple[list[dict[str, Any]], str]:
    """Drive the new pipeline. Returns (per-reviewer records, status).

    Each record carries the rendered markdown ``text``, the upstream
    worker status post-salvage, and the model/index identity bits the
    parity assertions key on.
    """
    recipe = BareReviewV1()
    records: list[dict[str, Any]] = []
    for index, (fixture_name, status) in enumerate(plan, start=1):
        model_id = _model_id(index)
        model_label = _model_label(index)

        # Hard-failure slots (timeout / proxy_error) skip the recipe
        # entirely on the new path -- the dispatcher's hard-failure
        # branch never invokes the recipe (see normalize._normalize_one).
        if status in ("timeout", "proxy_error") or not fixture_name:
            records.append(
                {
                    "index": index,
                    "model_id": model_id,
                    "model_label": model_label,
                    "text": "",
                    "status": status if status != "success" else "proxy_error",
                    "salvaged": False,
                }
            )
            continue

        raw_text = (FIXTURES_DIR / fixture_name).read_text(encoding="utf-8")
        args: dict[str, Any] = {
            "status": status,
            "target": str(target.resolve()),
            "target_checksum": FIXED_CHECKSUM,
            "target_truncated": False,
            "model_id": model_id,
            "model_label": model_label,
            "caller_label": CALLER_LABEL,
            "elapsed_ms": ELAPSED_MS,
            "generated": FIXED_GENERATED,
        }
        result = recipe.normalize(raw_text, args)

        # §7.4 salvage: parse_error -> success when the body is
        # recoverable. Mirrors normalize._normalize_one's promotion.
        resolved_status = status
        if status == "parse_error" and result.text and result.salvaged:
            resolved_status = "success"
        elif status == "parse_error" and not result.text:
            # Genuinely unparseable -- stays parse_error.
            resolved_status = "parse_error"

        records.append(
            {
                "index": index,
                "model_id": model_id,
                "model_label": model_label,
                "text": result.text,
                "status": resolved_status,
                "salvaged": bool(result.salvaged),
            }
        )

    # IMM-5 reduction via the canonical reducer.
    success_count = sum(1 for r in records if r["status"] == "success")
    status = determine_status(
        workers_succeeded=success_count,
        workers_requested=len(plan),
        policy=StatusPolicy(),
    )
    return records, status


# ---------------------------------------------------------------------------
# Lens metadata -- the new path's recommended_next_command template
# comes from the bundled lens registry. Asserts on the template (rather
# than a rendered string) keep the gate decoupled from the M5 reducer's
# substitution wiring while still pinning the operator-visible surface.
# ---------------------------------------------------------------------------


def _lens_next_command_template() -> str:
    entry = LENSES["bare-review"]
    return entry.recommended_next_command_template


# ---------------------------------------------------------------------------
# 1 -- Per-reviewer markdown byte-equality.
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "scenario_id,plan,expected_status",
    SCENARIOS,
    ids=[s[0] for s in SCENARIOS],
)
def test_legacy_vs_thin_caller_byte_identical_markdown(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    scenario_id: str,
    plan: ReviewerPlan,
    expected_status: str,
) -> None:
    """Both paths emit byte-identical normalized markdown per reviewer.

    The frontmatter ``generated`` field is the only wall-clock-dependent
    surface; both paths consume :data:`FIXED_GENERATED` so the byte
    comparison is mechanical. Slots without a final.md (timeouts,
    unrecoverable parse_errors) appear as empty strings on both sides
    and are compared equal-to-empty.
    """
    target = _write_target(tmp_path)
    legacy_dir = tmp_path / "legacy"
    manifest_path, reviewers = _stage_legacy_manifest(legacy_dir, target, plan)
    _run_legacy(monkeypatch, manifest_path)

    new_records, _ = _run_thin_caller(target, plan)

    assert len(new_records) == len(reviewers), (
        f"scenario {scenario_id}: thin-caller produced {len(new_records)} "
        f"records vs legacy {len(reviewers)}"
    )

    for legacy_rev, new_rec in zip(reviewers, new_records, strict=True):
        assert legacy_rev["index"] == new_rec["index"]
        final_path = Path(legacy_rev["final_path"])
        legacy_text = (
            final_path.read_text(encoding="utf-8") if final_path.exists() else ""
        )
        new_text = new_rec["text"]
        assert new_text == legacy_text, (
            f"scenario {scenario_id} slot {legacy_rev['index']}: "
            f"per-reviewer markdown differs.\n"
            f"  legacy bytes: {len(legacy_text)}\n"
            f"  new    bytes: {len(new_text)}\n"
            f"  fixture: {legacy_rev['_fixture']!r} "
            f"upstream status: {legacy_rev['_status']!r}"
        )


# ---------------------------------------------------------------------------
# 2 -- Aggregate IMM-5 status parity (success / partial / failed).
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "scenario_id,plan,expected_status",
    SCENARIOS,
    ids=[s[0] for s in SCENARIOS],
)
def test_legacy_vs_thin_caller_aggregate_status(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    scenario_id: str,
    plan: ReviewerPlan,
    expected_status: str,
) -> None:
    """Both pipelines classify the run with the same IMM-5 status.

    The status floor (2) + success-first policy is shared between the
    legacy script's inline if/elif/else and :func:`determine_status`.
    A drift here would mean a real-world run was reported one way to
    legacy consumers and another way to the new contract surface.
    """
    target = _write_target(tmp_path)
    legacy_dir = tmp_path / "legacy"
    manifest_path, _ = _stage_legacy_manifest(legacy_dir, target, plan)
    _, legacy_contract = _run_legacy(monkeypatch, manifest_path)

    _, new_status = _run_thin_caller(target, plan)

    assert legacy_contract["status"] == new_status == expected_status, (
        f"scenario {scenario_id}: status drift -- "
        f"legacy={legacy_contract['status']!r}, "
        f"new={new_status!r}, expected={expected_status!r}"
    )


# ---------------------------------------------------------------------------
# 3 -- Per-reviewer status set parity (M / N + per-slot status).
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "scenario_id,plan,expected_status",
    SCENARIOS,
    ids=[s[0] for s in SCENARIOS],
)
def test_legacy_vs_thin_caller_per_reviewer_status(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    scenario_id: str,
    plan: ReviewerPlan,
    expected_status: str,
) -> None:
    """Per-slot status agrees across the two pipelines.

    Each scenario's plan dictates the upstream status; the post-salvage
    status (parse_error -> success on recoverable bodies) must match
    on both sides. The legacy contract serializes the per-slot status
    under ``output_files[].status``; the thin caller carries it on
    each :class:`WorkerResult` (mirrored on the in-test record dict).
    """
    target = _write_target(tmp_path)
    legacy_dir = tmp_path / "legacy"
    manifest_path, _ = _stage_legacy_manifest(legacy_dir, target, plan)
    _, legacy_contract = _run_legacy(monkeypatch, manifest_path)

    new_records, _ = _run_thin_caller(target, plan)

    legacy_statuses = [f["status"] for f in legacy_contract["output_files"]]
    new_statuses = [r["status"] for r in new_records]
    assert legacy_statuses == new_statuses, (
        f"scenario {scenario_id}: per-slot status set differs -- "
        f"legacy={legacy_statuses!r}, new={new_statuses!r}"
    )

    legacy_succeeded = sum(1 for s in legacy_statuses if s == "success")
    new_succeeded = sum(1 for s in new_statuses if s == "success")
    assert legacy_succeeded == new_succeeded, (
        f"scenario {scenario_id}: M (workers_succeeded) drift -- "
        f"legacy={legacy_succeeded}, new={new_succeeded}"
    )
    # And M agrees with the legacy contract's own counter.
    assert legacy_contract["reviewers_succeeded"] == legacy_succeeded
    assert legacy_contract["reviewers_requested"] == len(plan)


# ---------------------------------------------------------------------------
# 4 -- Aggregate contract invariants (suspect:true + adversarial handoff).
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "scenario_id,plan,expected_status",
    SCENARIOS,
    ids=[s[0] for s in SCENARIOS],
)
def test_legacy_contract_carries_suspect_true_and_adversarial_handoff(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    scenario_id: str,
    plan: ReviewerPlan,
    expected_status: str,
) -> None:
    """Legacy contract always carries ``suspect:true`` + ``/sc:adversarial``.

    The thin caller carries the same invariants by construction: the
    bare-review lens declares ``suspect=True`` (COMP-023 assertion 5)
    and its ``recommended_next_command_template`` literally names
    ``/sc:adversarial --suspect-source``. These are the consumer-visible
    contract guarantees the M9 caller pipelines (sc:troubleshoot,
    sc:reflect, sc:auggie-review, sc:code-review) rely on to route
    bare-review output into the right downstream skill.
    """
    target = _write_target(tmp_path)
    legacy_dir = tmp_path / "legacy"
    manifest_path, _ = _stage_legacy_manifest(legacy_dir, target, plan)
    _, legacy_contract = _run_legacy(monkeypatch, manifest_path)

    assert legacy_contract["suspect"] is True, (
        f"scenario {scenario_id}: legacy contract missing suspect:true"
    )
    legacy_next_cmd = legacy_contract.get("recommended_next_command", "")
    assert "/sc:adversarial" in legacy_next_cmd, (
        f"scenario {scenario_id}: legacy recommended_next_command "
        f"missing /sc:adversarial: {legacy_next_cmd!r}"
    )
    assert "--suspect-source" in legacy_next_cmd, (
        f"scenario {scenario_id}: legacy recommended_next_command "
        f"missing --suspect-source: {legacy_next_cmd!r}"
    )

    # Thin-caller side: the bare-review lens entry advertises the same
    # invariants. Pulling them off the lens (rather than re-rendering
    # the contract via reduce_wave3) decouples the gate from the M5
    # substitution wiring while still pinning the consumer surface.
    lens_entry = LENSES["bare-review"]
    assert lens_entry.suspect is True, (
        "bare-review lens MUST declare suspect=True (COMP-023 assertion 5)"
    )
    new_template = _lens_next_command_template()
    assert "/sc:adversarial" in new_template, (
        f"bare-review lens template missing /sc:adversarial: {new_template!r}"
    )
    assert "--suspect-source" in new_template, (
        f"bare-review lens template missing --suspect-source: {new_template!r}"
    )


# ---------------------------------------------------------------------------
# 5 -- Output file path discipline (per-pipeline directories, same count).
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "scenario_id,plan,expected_status",
    SCENARIOS,
    ids=[s[0] for s in SCENARIOS],
)
def test_legacy_vs_thin_caller_output_file_count(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    scenario_id: str,
    plan: ReviewerPlan,
    expected_status: str,
) -> None:
    """``output_files`` length matches between pipelines.

    Both pipelines record one entry per requested slot regardless of
    per-slot outcome (success / parse_error / timeout). The entries'
    file paths differ between pipelines (legacy writes into the
    manifest's directory; the new path writes into the JobSpec's
    ``output.dir``) but the *count* and the *status set* must agree --
    that's what consumers downstream of the bare-review contract
    depend on when they read ``len(output_files)`` for an M/N report.
    """
    target = _write_target(tmp_path)
    legacy_dir = tmp_path / "legacy"
    manifest_path, _ = _stage_legacy_manifest(legacy_dir, target, plan)
    _, legacy_contract = _run_legacy(monkeypatch, manifest_path)

    new_records, _ = _run_thin_caller(target, plan)

    assert len(legacy_contract["output_files"]) == len(new_records) == len(plan), (
        f"scenario {scenario_id}: output_files length drift -- "
        f"legacy={len(legacy_contract['output_files'])}, "
        f"new={len(new_records)}, plan={len(plan)}"
    )


# ---------------------------------------------------------------------------
# 6 -- Sanity: legacy script + recipe both honour the deterministic
# ``generated`` injection. Without this, the byte-identity tests above
# would be a tautology.
# ---------------------------------------------------------------------------


def test_deterministic_generated_threads_through_both_pipelines(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    """Both pipelines stamp :data:`FIXED_GENERATED` on the frontmatter.

    A regression here would silently break the parity tests above
    (they would compare wall-clock-divergent bytes) -- pinning the
    threading explicitly makes the failure mode obvious instead of
    hidden behind a "1 byte differs" diff.
    """
    target = _write_target(tmp_path)
    plan: ReviewerPlan = [("basic_findings.raw.txt", "success")]
    legacy_dir = tmp_path / "legacy"
    manifest_path, reviewers = _stage_legacy_manifest(legacy_dir, target, plan)
    _run_legacy(monkeypatch, manifest_path)

    final_path = Path(reviewers[0]["final_path"])
    legacy_text = final_path.read_text(encoding="utf-8")
    assert f"generated: \"{FIXED_GENERATED}\"" in legacy_text, (
        f"legacy frontmatter missing fixed generated stamp; "
        f"got:\n{legacy_text[:400]}"
    )

    new_records, _ = _run_thin_caller(target, plan)
    new_text = new_records[0]["text"]
    assert f"generated: \"{FIXED_GENERATED}\"" in new_text, (
        f"new frontmatter missing fixed generated stamp; "
        f"got:\n{new_text[:400]}"
    )


# ---------------------------------------------------------------------------
# 7 -- WorkerResult shape parity. The thin-caller path will eventually
# present its per-slot record as a :class:`WorkerResult`; this test
# confirms the dataclass surface absorbs the parity-test record bag.
# ---------------------------------------------------------------------------


def test_thin_caller_records_round_trip_through_worker_result() -> None:
    """Each thin-caller record maps cleanly onto :class:`WorkerResult`.

    Pins the boundary the M5 executor crosses when it hands recipe
    output to the dispatcher's per-worker materializer. A drift here
    (e.g. renamed field) would mean the parity gate is asserting on a
    surface the production code path no longer carries.
    """
    record = {
        "index": 1,
        "model_id": _model_id(1),
        "model_label": _model_label(1),
        "status": "success",
        "elapsed_ms": ELAPSED_MS,
        "attempts": 1,
        "http_code": 200,
        "bytes": 4096,
    }
    worker = WorkerResult(
        index=record["index"],
        model_id=record["model_id"],
        model_label=record["model_label"],
        status=record["status"],
        elapsed_ms=record["elapsed_ms"],
        attempts=record["attempts"],
        http_code=record["http_code"],
        bytes=record["bytes"],
    )
    assert worker.status == "success"
    assert worker.model_id == record["model_id"]
    assert worker.index == 1
