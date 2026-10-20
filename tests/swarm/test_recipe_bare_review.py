"""``bare-review-v1`` recipe tests (R-088 / COMP-016 / D-0070).

Legacy-independent recipe coverage (post M8/M9 migration -- WS-C retires the
legacy ``t2_normalize.py``):

1. **Recipe salvage-flag semantics**: the recipe's ``salvaged`` flag is True iff
   the input status was ``parse_error`` and the recipe recovered non-empty text
   (the §7.4 promotion in semantic form).

2. **REGISTRY surface**: the ``bare-review-v1`` slot resolves to a
   Recipe-conforming object (no longer the M2-era ``None`` sentinel),
   and the Wave-2 dispatcher routes a worker through it end-to-end
   (raw read → recipe call → atomic ``final_path`` write → meta sidecar
   emission → salvage promotion on ``parse_error``).

The legacy-vs-recipe **byte-identity** A/B parity (formerly here as
``test_legacy_vs_recipe_byte_identical``, which imported the standalone legacy
``t2_normalize.py`` via importlib) is now provided by the permanent
**CLI-vs-frozen-golden** gate in ``tests/swarm/test_bare_review_parity.py``: it
drives ``superclaude swarm run --lens bare-review`` and asserts byte-equality
against a golden frozen from the real legacy output -- so the parity coverage
survives the WS-C deletion of the legacy script (this file no longer depends on
it at run time).
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from superclaude.cli.swarm.models import WorkerResult
from superclaude.cli.swarm.normalize import normalize_wave2
from superclaude.cli.swarm.recipes import REGISTRY, NormalizedResult, Recipe
from superclaude.cli.swarm.recipes.bare_review_v1 import BareReviewV1

# ---------------------------------------------------------------------------
# Fixture corpus
# ---------------------------------------------------------------------------


FIXTURES_DIR = Path(__file__).parent / "fixtures" / "bare_review_v1"

FIXED_GENERATED = "2026-06-01T11:19:39Z"
FIXED_CHECKSUM = "deadbeefcafe"
FIXED_TARGET = "/tmp/example/target.py"


# Each fixture: (filename, worker_status). The worker_status mirrors
# what ``t2_dispatch`` would have stamped on the meta sidecar; the
# recipe uses it to decide §7.4 salvage; the legacy script reads it
# from the meta JSON sidecar.
FIXTURES: list[tuple[str, str]] = [
    ("basic_findings.raw.txt", "success"),
    ("salvage.raw.txt", "parse_error"),
    ("verdict_only.raw.txt", "success"),
    ("freeform_fallback.raw.txt", "success"),
    ("odd_cites.raw.txt", "success"),
]


def _run_recipe(
    raw_text: str,
    status: str,
    elapsed_ms: int,
    model_id: str,
    model_label: str,
    caller_label: str,
) -> NormalizedResult:
    """Call BareReviewV1.normalize() with deterministic args."""
    recipe = BareReviewV1()
    args: dict[str, Any] = {
        "status": status,
        "target": FIXED_TARGET,
        "target_checksum": FIXED_CHECKSUM,
        "target_truncated": False,
        "model_id": model_id,
        "model_label": model_label,
        "caller_label": caller_label,
        "elapsed_ms": elapsed_ms,
        "generated": FIXED_GENERATED,
    }
    return recipe.normalize(raw_text, args)


# ---------------------------------------------------------------------------
# 1 -- Recipe salvage-flag semantics (byte-identity parity now lives in the
# CLI-vs-frozen-golden gate at tests/swarm/test_bare_review_parity.py)
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("filename,status", FIXTURES)
def test_recipe_salvage_flag_matches_status_transition(filename: str, status: str):
    """Recipe's ``salvaged`` flag is True iff input status was
    ``parse_error`` and the recipe recovered non-empty text. Mirrors the
    legacy §7.4 promotion in semantic (not byte) form."""
    raw_text = (FIXTURES_DIR / filename).read_text(encoding="utf-8")
    result = _run_recipe(raw_text, status, 0, "m", "M", "")
    if status == "parse_error" and result.text:
        assert result.salvaged is True
    else:
        assert result.salvaged is False


def _make_tmp_dir(tmp_path: Path) -> Path:
    legacy_dir = tmp_path / "legacy"
    legacy_dir.mkdir(parents=True, exist_ok=True)
    return legacy_dir


# ---------------------------------------------------------------------------
# 2 -- REGISTRY surface
# ---------------------------------------------------------------------------


def test_registry_resolves_bare_review_v1_to_recipe():
    """T04.03 acceptance: the slot is no longer ``None``."""
    entry = REGISTRY["bare-review-v1"]
    assert entry is not None
    assert isinstance(entry, Recipe)
    assert isinstance(entry, BareReviewV1)


def test_registry_bare_review_v1_protocol_callable():
    """The registered recipe accepts the canonical Protocol signature."""
    recipe = REGISTRY["bare-review-v1"]
    assert recipe is not None
    result = recipe.normalize(
        "## Findings\n\n## Verdict\nok\n",
        {"target": "/x.py", "generated": FIXED_GENERATED, "status": "success"},
    )
    assert isinstance(result, NormalizedResult)
    assert "T2-Bare Review" in result.text


# ---------------------------------------------------------------------------
# 3 -- Dispatcher integration: end-to-end through normalize_wave2
# ---------------------------------------------------------------------------


def _make_worker(
    tmp_path: Path,
    index: int,
    *,
    status: str,
    body: str,
) -> WorkerResult:
    raw_path = tmp_path / f"worker-{index:02d}.raw.md"
    raw_path.write_text(body, encoding="utf-8")
    return WorkerResult(
        index=index,
        path=str(tmp_path / f"worker-{index:02d}.md"),
        raw_path=str(raw_path),
        meta_path=str(tmp_path / f"worker-{index:02d}.meta.json"),
        final_path=str(tmp_path / f"worker-{index:02d}.final.md"),
        model_id=f"model-{index}",
        model_label=f"Model {index}",
        bytes=len(body.encode("utf-8")),
        status=status,
        http_code=200 if status == "success" else None,
        attempts=1,
        elapsed_ms=42,
    )


def test_dispatcher_routes_success_worker_through_bare_review_v1(tmp_path):
    """normalize_wave2 picks the registered recipe and writes the
    rendered body to final_path; meta sidecar records the recipe."""
    body = (FIXTURES_DIR / "basic_findings.raw.txt").read_text(encoding="utf-8")
    worker = _make_worker(tmp_path, 0, status="success", body=body)

    [out] = normalize_wave2(
        [worker],
        "bare-review-v1",
        recipe_args={
            "status": "success",
            "target": FIXED_TARGET,
            "target_checksum": FIXED_CHECKSUM,
            "target_truncated": False,
            "model_id": worker.model_id,
            "model_label": worker.model_label,
            "caller_label": "dispatcher-test",
            "elapsed_ms": worker.elapsed_ms,
            "generated": FIXED_GENERATED,
        },
    )

    assert out.status == "success"
    final_text = Path(worker.final_path).read_text(encoding="utf-8")
    assert "T2-Bare Review" in final_text
    assert "F-01" in final_text
    assert "deadbeefcafe" in final_text

    meta = json.loads(Path(worker.meta_path).read_text(encoding="utf-8"))
    assert meta["recipe"] == "bare-review-v1"
    assert meta["salvaged"] is False
    assert meta["status"] == "success"


def test_dispatcher_promotes_parse_error_via_salvage_flag(tmp_path):
    """A parse_error worker whose body is recoverable is promoted to
    success per §7.4. The recipe sets ``salvaged=True``; the dispatcher
    flips the status."""
    body = (FIXTURES_DIR / "salvage.raw.txt").read_text(encoding="utf-8")
    worker = _make_worker(tmp_path, 1, status="parse_error", body=body)

    [out] = normalize_wave2(
        [worker],
        "bare-review-v1",
        recipe_args={
            "status": "parse_error",
            "target": FIXED_TARGET,
            "target_checksum": FIXED_CHECKSUM,
            "target_truncated": False,
            "model_id": worker.model_id,
            "model_label": worker.model_label,
            "caller_label": "",
            "elapsed_ms": worker.elapsed_ms,
            "generated": FIXED_GENERATED,
        },
    )

    assert out.status == "success"
    meta = json.loads(Path(worker.meta_path).read_text(encoding="utf-8"))
    assert meta["salvaged"] is True
    assert meta["status"] == "success"


def test_dispatcher_keeps_parse_error_when_body_is_unrecoverable(tmp_path):
    """A parse_error worker with no findings AND no verdict stays
    parse_error; the recipe returns empty text and the dispatcher does
    not promote."""
    body = "this body has no findings table and no verdict heading\n"
    worker = _make_worker(tmp_path, 2, status="parse_error", body=body)

    [out] = normalize_wave2(
        [worker],
        "bare-review-v1",
        recipe_args={
            "status": "parse_error",
            "target": FIXED_TARGET,
            "target_checksum": FIXED_CHECKSUM,
            "target_truncated": False,
            "model_id": worker.model_id,
            "model_label": worker.model_label,
            "caller_label": "",
            "elapsed_ms": worker.elapsed_ms,
            "generated": FIXED_GENERATED,
        },
    )

    assert out.status == "parse_error"
    meta = json.loads(Path(worker.meta_path).read_text(encoding="utf-8"))
    assert meta["salvaged"] is False
    assert meta["status"] == "parse_error"
    # Recipe surfaces the recovery failure via error field.
    assert meta.get("error", "")
    assert not Path(worker.final_path).exists()


# ---------------------------------------------------------------------------
# 3b -- FR-028 regression: per-worker status threads through the SHARED
# recipe_args path. The production caller forwards ONE shared recipe_args
# dict to every worker (no per-worker ``status`` key); the dispatcher must
# inject ``worker.status`` per call so the recipe's §7.4 salvage gate sees
# the real upstream status. These tests deliberately OMIT ``status`` from
# recipe_args -- before the fix the recipe defaulted to ``"success"`` and
# never entered the salvage branch, so a recoverable parse_error reviewer
# was silently left failed (M undercount -> aggregate ``partial``).
# ---------------------------------------------------------------------------


def test_dispatcher_threads_per_worker_status_for_salvage(tmp_path):
    """parse_error worker + recoverable body is PROMOTED to success even
    when recipe_args carries no ``status`` key (real shared-args shape)."""
    body = (FIXTURES_DIR / "salvage.raw.txt").read_text(encoding="utf-8")
    worker = _make_worker(tmp_path, 7, status="parse_error", body=body)

    # NOTE: no "status" key -- this is the production shared-args shape.
    [out] = normalize_wave2(
        [worker],
        "bare-review-v1",
        recipe_args={
            "target": FIXED_TARGET,
            "target_checksum": FIXED_CHECKSUM,
            "target_truncated": False,
            "model_id": worker.model_id,
            "model_label": worker.model_label,
            "caller_label": "",
            "elapsed_ms": worker.elapsed_ms,
            "generated": FIXED_GENERATED,
        },
    )

    assert out.status == "success"
    meta = json.loads(Path(worker.meta_path).read_text(encoding="utf-8"))
    assert meta["salvaged"] is True
    assert meta["status"] == "success"


def test_dispatcher_unrecoverable_parse_error_stays_failed_shared_args(tmp_path):
    """parse_error worker with no findings AND no verdict stays
    parse_error even when recipe_args omits ``status`` (shared-args
    shape) -- per-worker status is threaded, salvage gate rejects."""
    body = "this body has no findings table and no verdict heading\n"
    worker = _make_worker(tmp_path, 8, status="parse_error", body=body)

    # NOTE: no "status" key -- production shared-args shape.
    [out] = normalize_wave2(
        [worker],
        "bare-review-v1",
        recipe_args={
            "target": FIXED_TARGET,
            "target_checksum": FIXED_CHECKSUM,
            "target_truncated": False,
            "model_id": worker.model_id,
            "model_label": worker.model_label,
            "caller_label": "",
            "elapsed_ms": worker.elapsed_ms,
            "generated": FIXED_GENERATED,
        },
    )

    assert out.status == "parse_error"
    meta = json.loads(Path(worker.meta_path).read_text(encoding="utf-8"))
    assert meta["salvaged"] is False
    assert meta["status"] == "parse_error"
    assert not Path(worker.final_path).exists()


def test_dispatcher_shared_args_mixed_statuses(tmp_path):
    """ONE shared recipe_args dict (no ``status`` key) drives a mixed
    batch: the success worker stays success, the recoverable parse_error
    worker is promoted, and the unrecoverable parse_error worker stays
    failed. Proves the per-worker injection is per-call, not global."""
    ok_body = (FIXTURES_DIR / "basic_findings.raw.txt").read_text(encoding="utf-8")
    salvage_body = (FIXTURES_DIR / "salvage.raw.txt").read_text(encoding="utf-8")
    dead_body = "no findings table and no verdict heading\n"

    w_ok = _make_worker(tmp_path, 10, status="success", body=ok_body)
    w_salvage = _make_worker(tmp_path, 11, status="parse_error", body=salvage_body)
    w_dead = _make_worker(tmp_path, 12, status="parse_error", body=dead_body)

    shared_args = {
        "target": FIXED_TARGET,
        "target_checksum": FIXED_CHECKSUM,
        "target_truncated": False,
        "caller_label": "",
        "generated": FIXED_GENERATED,
    }
    outs = normalize_wave2(
        [w_ok, w_salvage, w_dead],
        "bare-review-v1",
        recipe_args=shared_args,
    )

    assert [o.status for o in outs] == ["success", "success", "parse_error"]
    # Shared dict not mutated by the per-worker status injection.
    assert "status" not in shared_args


# ---------------------------------------------------------------------------
# 4 -- AC-011 boundary -- findings preserved verbatim (no scoring/dedup)
# ---------------------------------------------------------------------------


def test_recipe_preserves_all_findings_including_duplicates():
    """AC-011: recipes MUST NOT dedupe or reorder findings. T04.14 lands
    the full boundary suite; this is the bare_review_v1 slice."""
    raw = (
        "## Findings\n\n"
        "| ID | Sev | Claim | Cite | SelfConf |\n"
        "|----|-----|-------|------|----------|\n"
        "| F-01 | crit | duplicate claim text | x.py:1 | 50 |\n"
        "| F-02 | crit | duplicate claim text | x.py:1 | 50 |\n"
        "| F-03 | high | second unique row | x.py:2 | 60 |\n"
        "| F-04 | crit | duplicate claim text | x.py:1 | 50 |\n"
        "\n## Verdict\nok\n"
    )
    result = _run_recipe(raw, "success", 0, "m", "M", "")
    # 4 row ids present, in input order (renumbered F-01..F-04 by the
    # renderer but preserving count + order).
    assert result.text.count("duplicate claim text") == 3
    assert result.text.count("second unique row") == 1
    # Renumbered row IDs are sequential 1..N (legacy behavior).
    assert "| F-01 |" in result.text
    assert "| F-04 |" in result.text


# ---------------------------------------------------------------------------
# 5 -- Phase-2 characterization (cleanup-debt item 2.7, panel G5): bare and
# cross-facade primitive behavior pinned from the UNCHANGED implementations.
# Every case goes through the ORIGINAL recipe-module names (the facades);
# clocks are frozen by supplying ``generated`` or by patching the original
# module's ``iso_now`` / ``datetime`` -- never a shared leaf module.
# ---------------------------------------------------------------------------

import datetime as _dt  # noqa: E402
import hashlib  # noqa: E402
import importlib  # noqa: E402

RECIPE_MODULES = [
    "bare_review_v1",
    "findings_table_v1",
    "hypothesis_table_v1",
    "verdict_only_v1",
]
RECIPE_CLASSES = {
    "bare_review_v1": "BareReviewV1",
    "findings_table_v1": "FindingsTableV1",
    "hypothesis_table_v1": "HypothesisTableV1",
    "verdict_only_v1": "VerdictOnlyV1",
}
EXPECTED_ALL = {
    "bare_review_v1": [
        "BareReviewV1",
        "SEV_ALIASES",
        "EMPTY_CITE",
        "FINDING_ID",
        "iso_now",
        "yaml_str",
        "strip_frontmatter",
        "normalize_sev",
        "normalize_cite",
        "parse_conf",
        "parse_findings",
        "extract_section",
        "render_markdown",
    ],
    "findings_table_v1": [
        "FindingsTableV1",
        "DIVIDER_CELL_RE",
        "FALLBACK_NOTES_CAP",
        "CLAIM_CAP",
        "DETAIL_CAP",
        "iso_now",
        "yaml_str",
        "strip_frontmatter",
        "parse_findings_table",
        "extract_notes",
        "render_markdown",
    ],
    "hypothesis_table_v1": [
        "HypothesisTableV1",
        "DIVIDER_CELL_RE",
        "CAUSE_CAP",
        "EVIDENCE_CAP",
        "NEXT_STEP_CAP",
        "FALLBACK_NOTES_CAP",
        "iso_now",
        "yaml_str",
        "strip_frontmatter",
        "parse_confidence",
        "parse_hypothesis_table",
        "extract_notes",
        "render_markdown",
    ],
    "verdict_only_v1": [
        "VerdictOnlyV1",
        "VERDICT_ALIASES",
        "CANONICAL_VERDICTS",
        "VERDICT_LABEL_CAP",
        "RATIONALE_CAP",
        "NOTES_CAP",
        "iso_now",
        "yaml_str",
        "strip_frontmatter",
        "parse_confidence",
        "parse_verdict",
        "extract_section",
        "render_markdown",
    ],
}
PATCHED_CLOCK = "2031-02-03T04:05:06Z"
STUB_NOW = _dt.datetime(2030, 1, 2, 3, 4, 5, tzinfo=_dt.timezone.utc)


def _mod(name: str):
    return importlib.import_module(f"superclaude.cli.swarm.recipes.{name}")


def _generated_line(text: str) -> str:
    return next(line for line in text.split("\n") if line.startswith("generated:"))


def _line_after(text: str, heading: str) -> str:
    lines = text.split("\n")
    return lines[lines.index(heading) + 1]


# 5a -- exported lookup seam (G5.55): exact __all__ and name resolution ------


@pytest.mark.parametrize("module_name", RECIPE_MODULES)
def test_facade_all_is_exact_and_resolvable(module_name: str):
    mod = _mod(module_name)
    assert mod.__all__ == EXPECTED_ALL[module_name]
    for name in mod.__all__:
        assert getattr(mod, name) is not None
    # module-local clock bindings exist (seam for datetime patching)
    assert mod.datetime is _dt.datetime
    assert mod.timezone is _dt.timezone


@pytest.mark.parametrize("module_name", RECIPE_MODULES)
def test_facade_yaml_str_and_strip_frontmatter_patch_is_effective(
    module_name: str, monkeypatch
):
    """Callers resolve the facade-module globals at call time (G5.55)."""
    mod = _mod(module_name)
    seen: list[str] = []
    real_strip = mod.strip_frontmatter

    def _spy(text: str) -> str:
        seen.append(text)
        return real_strip(text)

    monkeypatch.setattr(mod, "yaml_str", lambda v: '"<PATCHED>"')
    monkeypatch.setattr(mod, "strip_frontmatter", _spy)
    cls = getattr(mod, RECIPE_CLASSES[module_name])
    result = cls().normalize("some text", {"status": "success", "generated": "G"})
    assert seen == ["some text"]
    assert 'generated: "<PATCHED>"' in result.text


@pytest.mark.parametrize("module_name", ["bare_review_v1", "verdict_only_v1"])
def test_facade_extract_section_patch_is_effective(module_name: str, monkeypatch):
    mod = _mod(module_name)
    calls: list[tuple[str, int]] = []
    real = mod.extract_section

    def _spy(text: str, heading: str, cap: int) -> str:
        calls.append((heading, cap))
        return real(text, heading, cap)

    monkeypatch.setattr(mod, "extract_section", _spy)
    cls = getattr(mod, RECIPE_CLASSES[module_name])
    cls().normalize("## Verdict\nok\n", {"status": "success", "generated": "G"})
    assert calls  # normalize routed through the patched facade global
    if module_name == "bare_review_v1":
        assert calls == [("Verdict", 300), ("Notes", 200)]


# 5b -- clock seam (G5.30) across the four facades ------------------------


@pytest.mark.parametrize("module_name", RECIPE_MODULES)
def test_facade_iso_now_reads_module_local_datetime(module_name: str, monkeypatch):
    mod = _mod(module_name)
    seen: list[Any] = []

    class _StubDatetime:
        @classmethod
        def now(cls, tz=None):
            seen.append(tz)
            return STUB_NOW

    monkeypatch.setattr(mod, "datetime", _StubDatetime)
    assert mod.iso_now() == "2030-01-02T03:04:05Z"
    assert seen == [mod.timezone.utc]
    cls = getattr(mod, RECIPE_CLASSES[module_name])
    text = cls().normalize("some text", {"status": "success"}).text
    assert _generated_line(text) == 'generated: "2030-01-02T03:04:05Z"'


@pytest.mark.parametrize("module_name", RECIPE_MODULES)
@pytest.mark.parametrize(
    "extra,expected",
    [
        ({}, PATCHED_CLOCK),
        ({"generated": None}, PATCHED_CLOCK),
        ({"generated": ""}, PATCHED_CLOCK),
        ({"generated": FIXED_GENERATED}, FIXED_GENERATED),
    ],
    ids=["absent", "none", "empty", "supplied"],
)
def test_facade_generated_supplied_or_module_iso_now_fallback(
    module_name: str, extra: dict, expected: str, monkeypatch
):
    mod = _mod(module_name)
    monkeypatch.setattr(mod, "iso_now", lambda: PATCHED_CLOCK)
    cls = getattr(mod, RECIPE_CLASSES[module_name])
    text = cls().normalize("some text", {"status": "success", **extra}).text
    assert _generated_line(text) == f'generated: "{expected}"'


# 5c -- YAML scalar escaping (G5.29) across the four facades ---------------

YAML_CASES = [
    ("", '""'),
    ('a"b', '"a\\"b"'),
    ("a\\b", '"a\\\\b"'),
    ('\\"', '"\\\\\\""'),  # backslash escaped before quote
    ("é", '"é"'),
    ("line1\nline2", '"line1\nline2"'),  # newline NOT escaped today
    (0, '"0"'),
    (False, '"False"'),
]


@pytest.mark.parametrize("module_name", RECIPE_MODULES)
@pytest.mark.parametrize("value,expected", YAML_CASES)
def test_facade_yaml_str(module_name: str, value, expected: str):
    assert _mod(module_name).yaml_str(value) == expected


# 5d -- literal frontmatter split (G5.11-G5.16) across the four facades ----

FRONTMATTER_CASES = [
    ("", ""),
    ("a", "a"),
    (" \n---\nx: 1\n---\nbody", "\nbody"),
    ("---\nx: 1", "---\nx: 1"),
    ("---x---body", "body"),
    ("---x---body---tail", "body---tail"),
    ("body\n---\nx---z", "body\n---\nx---z"),
    ("---\n---\n", "\n"),
    ("   ---a---b", "b"),
]


@pytest.mark.parametrize("module_name", RECIPE_MODULES)
@pytest.mark.parametrize("text,expected", FRONTMATTER_CASES)
def test_facade_strip_frontmatter(module_name: str, text: str, expected: str):
    assert _mod(module_name).strip_frontmatter(text) == expected


# 5e -- section extraction (G5.17-G5.24, G5.28) ---------------------------

SECTION_CASES = [
    # (text, heading, cap, expected)
    ("plain", "Notes", 200, ""),
    ("## Notes\n## Other\nx", "Notes", 200, ""),
    ("## Notes\n## Notes\nsecond", "Notes", 200, ""),  # first (empty) wins
    ("## nOtEs\na", "Notes", 200, "a"),
    ("## Notes\na  b\n## Other\nc", "Notes", 200, "a b"),
    ("## Notes\na  b\n", "Notes", 200, "a b"),
    ("## Notes\nfirst\n## Notes\nsecond", "Notes", 200, "first"),
    ("## Notes\na", "Notes", 0, ""),
    ("## Notes\nabc", "Notes", -1, "ab"),
    ("## Notes\n a   b ", "Notes", 3, "a b"),
    ("#Notes\nx", "Notes", 200, "x"),
    ("## Notes extra\nx", "Notes", 200, ""),
    ("## Notes\na\n#tag\nb", "Notes", 200, "a #tag b"),
    ("## a.b\nx", "a.b", 10, "x"),
    ("## axb\nx", "a.b", 10, ""),  # heading is regex-escaped
    ("## Notes\n" + "é" * 5, "Notes", 3, "ééé"),  # code points
]


@pytest.mark.parametrize("module_name", ["bare_review_v1", "verdict_only_v1"])
@pytest.mark.parametrize("text,heading,cap,expected", SECTION_CASES)
def test_facade_extract_section(
    module_name: str, text: str, heading: str, cap: int, expected: str
):
    assert _mod(module_name).extract_section(text, heading, cap) == expected


@pytest.mark.parametrize("module_name", ["findings_table_v1", "hypothesis_table_v1"])
@pytest.mark.parametrize(
    "text,heading,cap,expected",
    [c for c in SECTION_CASES if c[1] == "Notes" and c[2] == 200],
)
def test_facade_extract_notes_matches_section_semantics(
    module_name: str, text: str, heading: str, cap: int, expected: str
):
    assert _mod(module_name).extract_notes(text) == expected


# 5f -- bare parse_conf (G5.2-G5.10): no-digit -> '' (distinct from the
# hypothesis/verdict parse_confidence qualitative passthrough) -------------

BARE_CONF_CASES = [
    ("", ""),
    ("  ", ""),
    ("0", "0"),
    ("confidence 73%", "73"),
    ("100", "100"),
    ("101", "100"),
    ("-1", "1"),
    ("12.5 then 99", "12"),
    (" high  confidence ", ""),
    ("٣٧", "37"),  # Unicode Nd digits accepted by \d and int()
    ("007", "7"),
    ("9" * 4300, "100"),
]


@pytest.mark.parametrize("cell,expected", BARE_CONF_CASES)
def test_bare_parse_conf(cell: str, expected: str):
    from superclaude.cli.swarm.recipes.bare_review_v1 import parse_conf

    assert parse_conf(cell) == expected


def test_bare_parse_conf_preserves_int_conversion_error():
    """G5.10: baseline int() limit error propagates (no new fallback)."""
    from superclaude.cli.swarm.recipes.bare_review_v1 import parse_conf

    with pytest.raises(ValueError, match=r"Exceeds the limit \(4300 digits\)"):
        parse_conf("9" * 4301)
    with pytest.raises(ValueError, match=r"Exceeds the limit"):
        BareReviewV1().normalize(
            "| F-1 | high | c | x:1 | " + "9" * 4301 + " |\n",
            {"generated": FIXED_GENERATED},
        )


def test_bare_conversion_error_at_dispatcher_seam(tmp_path):
    """G5.10: the dispatcher's existing recipe-exception handling records
    parse_error with the original ValueError text and writes no final."""
    body = "| F-1 | high | claim | x:1 | " + "9" * 4301 + " |\n"
    worker = _make_worker(tmp_path, 20, status="success", body=body)
    [out] = normalize_wave2(
        [worker], "bare-review-v1", recipe_args={"generated": FIXED_GENERATED}
    )
    assert out.status == "parse_error"
    meta = json.loads(Path(worker.meta_path).read_text(encoding="utf-8"))
    assert meta["status"] == "parse_error"
    assert meta["salvaged"] is False
    assert meta["salvage_reason"] == "rejected_no_recipe_signal"
    assert meta["error"].startswith(
        "ValueError: Exceeds the limit (4300 digits) for integer string conversion"
    )
    assert not Path(worker.final_path).exists()


# 5g -- bare row acceptance / severity / cite (G5.32, G5.33) ---------------


def test_bare_parse_findings_row_acceptance_and_order():
    from superclaude.cli.swarm.recipes.bare_review_v1 import parse_findings

    rows = "\n".join(
        [
            "no pipe at all",
            "| F-1 | high | four cells | x:1 |",
            "| X-1 | high | bad id | x:1 | 50 |",
            "| F-1 | high |   | x:1 | 50 |",
            "| F-1 | critical | valid dash one | x:1 | 50 |",
            "| f1 | MAJOR  | lower no dash | none | 7 |",
            "| F-01 | unknown | zero padded | N/A | high |",
            "| F-2 | nit | dashes cite | -- | 101 |",
            "| F-3 | info | trims cite |  src/a.py:9  | -1 |",
            "| ID | Sev | Claim | Cite | SelfConf |",
            "|----|-----|-------|------|----------|",
            "  | F-4 | blocker | indented row | x:4 | 12.5 then 99 | extra |",
        ]
    )
    assert parse_findings(rows) == [
        {"sev": "crit", "claim": "valid dash one", "cite": "x:1", "conf": "50"},
        {"sev": "high", "claim": "lower no dash", "cite": "none", "conf": "7"},
        {"sev": "med", "claim": "zero padded", "cite": "none", "conf": ""},
        {"sev": "nit", "claim": "dashes cite", "cite": "none", "conf": "100"},
        {"sev": "nit", "claim": "trims cite", "cite": "src/a.py:9", "conf": "1"},
        {"sev": "crit", "claim": "indented row", "cite": "x:4", "conf": "12"},
    ]


@pytest.mark.parametrize(
    "cell,expected",
    [
        ("critical", "crit"),
        ("unknown", "med"),
        (" MAJOR ", "high"),
        ("", "med"),
        ("Trivial", "nit"),
    ],
)
def test_bare_normalize_sev(cell: str, expected: str):
    from superclaude.cli.swarm.recipes.bare_review_v1 import normalize_sev

    assert normalize_sev(cell) == expected


@pytest.mark.parametrize(
    "cell,expected",
    [
        ("none", "none"),
        ("N/A", "none"),
        ("--", "none"),
        (" x:1 ", "x:1"),
        ("", "none"),
        ("na", "none"),
        ("-", "none"),
    ],
)
def test_bare_normalize_cite(cell: str, expected: str):
    from superclaude.cli.swarm.recipes.bare_review_v1 import normalize_cite

    assert normalize_cite(cell) == expected


# 5h -- bare caps 120/300/200 (+ freeform 300) at k-1/k/k+1 code points
# (G5.25-G5.27) ------------------------------------------------------------


@pytest.mark.parametrize("delta", [-1, 0, 1], ids=["k-1", "k", "k+1"])
def test_bare_claim_cap_120_code_points(delta: int):
    from superclaude.cli.swarm.recipes.bare_review_v1 import parse_findings

    n = 120 + delta
    [row] = parse_findings("| F-1 | high | " + "é" * n + " | x:1 | 50 |")
    assert row["claim"] == "é" * min(n, 120)
    assert len(row["claim"].encode("utf-8")) == 2 * min(n, 120)


@pytest.mark.parametrize("delta", [-1, 0, 1], ids=["k-1", "k", "k+1"])
@pytest.mark.parametrize("heading,cap", [("Verdict", 300), ("Notes", 200)])
def test_bare_section_caps_code_points(heading: str, cap: int, delta: int):
    n = cap + delta
    other = "Notes" if heading == "Verdict" else "Verdict"
    raw = f"## {heading}\n" + "é" * n + f"\n## {other}\nx\n"
    text = BareReviewV1().normalize(raw, {"generated": FIXED_GENERATED}).text
    value = _line_after(text, f"## {heading}")
    assert value == "é" * min(n, cap)
    assert len(value.encode("utf-8")) == 2 * min(n, cap)


@pytest.mark.parametrize("delta", [-1, 0, 1], ids=["k-1", "k", "k+1"])
def test_bare_freeform_verdict_cap_300_code_points(delta: int):
    n = 300 + delta
    text = (
        BareReviewV1()
        .normalize("é" * n, {"status": "success", "generated": FIXED_GENERATED})
        .text
    )
    assert _line_after(text, "## Verdict") == "é" * min(n, 300)


# 5i -- bare normalize status / salvage / fallback (G5.1, G5.49-G5.52) -----

_BARE_FM = (
    '---\nschema_version: "1.0"\ntier: "T2"\nsuspect: true\n'
    'reviewer_model_id: ""\nreviewer_model_label: ""\ntarget: ""\n'
    'target_checksum: ""\ntarget_truncated: false\n'
    'generated: "2026-06-01T11:19:39Z"\ncaller_label: ""\nelapsed_ms: 0\n'
)
_BARE_HEAD = (
    "---\n\n# T2-Bare Review — \n\n## Findings\n\n"
    "| ID | Sev | Claim | Cite | SelfConf |\n"
    "|----|-----|-------|------|----------|\n"
)


@pytest.mark.parametrize(
    "raw,status,text,salvaged,error",
    [
        ("", "success", "", False, "empty raw body"),
        (" \n ", "parse_error", "", False, "empty raw body"),
        (
            "no table and no verdict heading\n",
            "parse_error",
            "",
            False,
            "no findings or verdict",
        ),
        (
            "## Verdict\nlooks fine\n",
            "parse_error",
            _BARE_FM + "finding_count: 0\n" + _BARE_HEAD + "\n## Verdict\nlooks fine\n",
            True,
            None,
        ),
        (
            "| F-1 | high | c | x:1 | 5 |\n",
            "parse_error",
            _BARE_FM
            + "finding_count: 1\n"
            + _BARE_HEAD
            + "| F-01 | high | c | x:1 | 5 |\n\n## Verdict\n(no verdict returned)\n",
            True,
            None,
        ),
        (
            "just   some\nfree text",
            "success",
            _BARE_FM
            + "finding_count: 0\n"
            + _BARE_HEAD
            + "\n## Verdict\njust some free text\n",
            False,
            None,
        ),
        (
            "---\nx: 1\n---\n   \n",
            "success",
            _BARE_FM
            + "finding_count: 0\n"
            + _BARE_HEAD
            + "\n## Verdict\n(no structured findings returned)\n",
            False,
            None,
        ),
        (
            "| F-1 | crit | c | x:1 | 90 |\n## Verdict\nok\n## Notes\nn\n",
            "success",
            _BARE_FM
            + "finding_count: 1\n"
            + _BARE_HEAD
            + "| F-01 | crit | c | x:1 | 90 |\n\n## Verdict\nok\n\n## Notes\nn\n",
            False,
            None,
        ),
    ],
    ids=[
        "empty",
        "whitespace",
        "parse_error_nothing",
        "parse_error_verdict_only",
        "parse_error_finding_only",
        "success_freeform",
        "success_whitespace_after_strip",
        "success_structured",
    ],
)
def test_bare_normalize_status_matrix(raw, status, text, salvaged, error):
    result = BareReviewV1().normalize(
        raw, {"status": status, "generated": FIXED_GENERATED}
    )
    assert result.text == text
    assert result.salvaged is salvaged
    assert result.error == error


@pytest.mark.parametrize(
    "value,expected",
    [(0, 0), (None, 0), ("bad", 0), ("42", 42), (42.9, 42), (-3, -3), ([], 0)],
    ids=["zero", "none", "bad", "str42", "float", "negative", "empty_list"],
)
def test_bare_elapsed_conversion(value, expected: int):
    """G5.31: int()/``or 0`` fallback with TypeError/ValueError -> 0."""
    text = (
        BareReviewV1()
        .normalize("x", {"elapsed_ms": value, "generated": FIXED_GENERATED})
        .text
    )
    assert f"\nelapsed_ms: {expected}\n" in text


def test_bare_render_markdown_field_types_and_order():
    """G5.54: bool before int, yaml_str otherwise, key order preserved."""
    from superclaude.cli.swarm.recipes.bare_review_v1 import render_markdown

    out = render_markdown(
        "slug",
        {"a": False, "b": 0, "c": "é", "d": True, "e": 5, "f": 'q"\\'},
        [],
        "",
        "",
    )
    assert out == (
        '---\na: false\nb: 0\nc: "é"\nd: true\ne: 5\nf: "q\\"\\\\"\n---\n\n'
        "# T2-Bare Review — slug\n\n## Findings\n\n"
        "| ID | Sev | Claim | Cite | SelfConf |\n"
        "|----|-----|-------|------|----------|\n\n"
        "## Verdict\n(no verdict returned)\n"
    )


# 5j -- frozen serialized fixture outputs (byte oracle for C03 parity) -----

FIXTURE_SHA256 = {
    "basic_findings.raw.txt": "c5a8ce35487c20934a1d1003ef3c4cf3092bb526bc10f32dbc2a01fc98d5ad02",
    "salvage.raw.txt": "bd40fcaf30a62b34da4ee7d9b8aecd4d87f5dbe4257e54219a2667b10a39ece8",
    "verdict_only.raw.txt": "9d17e4ec6f9d7bb6677054845e5be8d79c588190cf3977874613c81c88ff9386",
    "freeform_fallback.raw.txt": "7b803c3e91f06f5a76894157264fb9ec3017600cb4887d97fb7d688feabe05fe",
    "odd_cites.raw.txt": "a25a651ec19b66bba417b4d0068b94bf68feb19dc92277dd3a8c15d2d4680cfa",
}


@pytest.mark.parametrize("filename,status", FIXTURES)
def test_bare_fixture_output_bytes_frozen(filename: str, status: str):
    raw_text = (FIXTURES_DIR / filename).read_text(encoding="utf-8")
    result = _run_recipe(raw_text, status, 0, "m", "M", "")
    digest = hashlib.sha256(result.text.encode("utf-8")).hexdigest()
    assert digest == FIXTURE_SHA256[filename]
